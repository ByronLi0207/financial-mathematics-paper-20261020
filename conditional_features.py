"""Causal, source-independent peak-response predictors and completed fit pools.

No source I/O, outcome evaluation or normalization on an unspecified full series.
The caller supplies each fit's mature training rows explicitly.
"""
from dataclasses import dataclass
import math
import numpy as np
from study_core import exact_rank, order_statistic


def _readonly(x):
    y=np.array(x,copy=True);y.flags.writeable=False;return y


def _positive_int(x,name):
    if isinstance(x,(bool,np.bool_)) or not isinstance(x,(int,np.integer)) or x<=0:
        raise ValueError('invalid '+name)
    return int(x)


@dataclass(frozen=True)
class FeatureSeries:
    values: np.ndarray
    short_rms: np.ndarray
    valid_from: int


@dataclass(frozen=True)
class FeatureTransform:
    mean: np.ndarray
    scale: np.ndarray


def build_features(position,times,*,short_scale,long_scale,nominal_gap_seconds):
    x=np.asarray(position,dtype=np.float64);t=np.asarray(times)
    short_scale=_positive_int(short_scale,'short scale');long_scale=_positive_int(long_scale,'long scale')
    nominal_gap_seconds=_positive_int(nominal_gap_seconds,'nominal gap')
    valid=max(24,long_scale,short_scale)
    if x.ndim!=1 or len(x)<=valid or not np.isfinite(x).all() or t.ndim!=1 or t.shape!=x.shape or t.dtype.kind!='M':
        raise ValueError('invalid feature source')
    t=t.astype('datetime64[us]')
    if np.isnat(t).any() or np.any(t[1:]<=t[:-1]):raise ValueError('invalid feature chronology')
    values=np.full((len(x),33),np.nan);short=np.full(len(x),np.nan)
    with np.errstate(over='raise',invalid='raise'):
        delta=np.diff(x)
        scales=[]
        for length in (short_scale,long_scale):
            scale=np.full(len(x),np.nan)
            scale[length:]=np.sqrt(np.convolve(delta*delta,np.ones(length)/length,mode='valid'))
            scales.append(scale)
        short[:]=scales[0]
        for lag in range(25):values[valid:,lag]=x[valid-lag:len(x)-lag]
        values[valid:,25]=np.abs(x[valid:])
        values[valid:,26]=scales[0][valid:];values[valid:,27]=scales[1][valid:]
        hour=t.astype('datetime64[h]').astype(np.int64)%24
        weekday=(t.astype('datetime64[D]').astype(np.int64)+3)%7
        values[valid:,28]=np.sin(2*np.pi*hour[valid:]/24)
        values[valid:,29]=np.cos(2*np.pi*hour[valid:]/24)
        values[valid:,30]=np.sin(2*np.pi*weekday[valid:]/7)
        values[valid:,31]=np.cos(2*np.pi*weekday[valid:]/7)
        gaps=np.diff(t).astype('timedelta64[us]').astype(np.int64)
        values[valid:,32]=gaps[valid-1:]>(nominal_gap_seconds*1000000)
    if not np.isfinite(values[valid:]).all():raise ValueError('nonfinite features')
    return FeatureSeries(_readonly(values),_readonly(short),valid)


def fit_feature_transform(training_features):
    a=np.asarray(training_features,dtype=np.float64)
    if a.ndim!=2 or not a.shape[0] or a.shape[1]!=33 or not np.isfinite(a).all():raise ValueError('invalid training features')
    with np.errstate(over='raise',invalid='raise'):
        mean=np.mean(a,axis=0);scale=np.std(a,axis=0,ddof=0)
    # Exact repeated floats may acquire a roundoff standard deviation.
    # Identify actual constant columns without a data-dependent epsilon.
    constant=np.all(a==a[0],axis=0)
    mean[constant]=a[0,constant];scale[constant]=1.
    scale=np.where(scale==0,1.,scale)
    if not np.isfinite(mean).all() or not np.isfinite(scale).all():raise ValueError('nonfinite feature fit')
    return FeatureTransform(_readonly(mean),_readonly(scale))


def transform_features(features,fit,*,nearest=False):
    x=np.asarray(features,dtype=np.float64)
    if x.ndim!=2 or x.shape[1]!=33 or not np.isfinite(x).all() or not isinstance(fit,FeatureTransform):raise ValueError('invalid feature transform')
    if fit.mean.shape!=(33,) or fit.scale.shape!=(33,) or np.any(fit.scale<=0):raise ValueError('invalid fitted transform')
    with np.errstate(over='raise',invalid='raise',divide='raise'):z=(x-fit.mean)/fit.scale
    if nearest:
        z[:,:25]/=5
        for start,stop in ((26,28),(28,30),(30,32)):z[:,start:stop]/=math.sqrt(2)
    if not np.isfinite(z).all():raise ValueError('nonfinite transformed features')
    return z


def completed_training_indices(refit,horizon,window,*,minimum_feature_index):
    refit=_positive_int(refit,'refit');horizon=_positive_int(horizon,'horizon');window=_positive_int(window,'window')
    if isinstance(minimum_feature_index,bool) or not isinstance(minimum_feature_index,(int,np.integer)) or minimum_feature_index<0:raise ValueError('invalid minimum feature index')
    first=refit-horizon-window+1;stop=refit-horizon+1
    if first<minimum_feature_index:raise ValueError('inadequate completed feature history')
    return _readonly(np.arange(first,stop,dtype=np.int64))


def refit_origin(issue,segment_start,step):
    issue=_positive_int(issue,'issue');segment_start=_positive_int(segment_start,'segment start');step=_positive_int(step,'refit step')
    if issue<segment_start:raise ValueError('issue precedes segment')
    return segment_start+step*((issue-segment_start)//step)


def response_scale(headroom,anchors):
    y=np.asarray(headroom,dtype=np.float64);a=np.asarray(anchors,dtype=np.float64)
    if y.ndim!=1 or not y.size or a.shape!=y.shape or not np.isfinite(y).all() or not np.isfinite(a).all() or np.any(y<0):raise ValueError('invalid response scale input')
    try:
        with np.errstate(over='raise',invalid='raise'):
            result=max(float(np.mean(y)),float(np.mean(np.abs(a)))*1e-6,1e-12)
    except FloatingPointError as exc:
        raise ValueError('response scale overflow') from exc
    if not math.isfinite(result):raise ValueError('nonfinite response scale')
    return result


def neighbor_quantile(training_features,query,headroom,origins,k,*,numerator=19,denominator=20):
    x=np.asarray(training_features,dtype=np.float64);q=np.asarray(query,dtype=np.float64);y=np.asarray(headroom,dtype=np.float64);ids=np.asarray(origins)
    k=_positive_int(k,'neighbors')
    if (x.ndim!=2 or not x.shape[0] or q.shape!=(x.shape[1],) or y.shape!=(len(x),) or ids.shape!=(len(x),)
            or ids.dtype.kind not in 'iu' or np.any(ids[1:]<=ids[:-1]) or np.any(ids<0) or k>len(x)
            or not np.isfinite(x).all() or not np.isfinite(q).all() or not np.isfinite(y).all() or np.any(y<0)):
        raise ValueError('invalid neighbor inputs')
    rank=exact_rank(k,numerator,denominator)
    if rank>k:raise ValueError('unavailable neighbor rank')
    if np.any(ids>np.iinfo(np.int64).max):raise ValueError('origin exceeds signed index range')
    ids=ids.astype(np.int64,copy=False)
    with np.errstate(over='raise',invalid='raise'):
        delta=x-q;distance=np.einsum('ij,ij->i',delta,delta)
    if not np.isfinite(distance).all():raise ValueError('nonfinite neighbor distance')
    selected=np.lexsort((-ids,distance))[:k]
    selected=selected[np.argsort(ids[selected])]
    return order_statistic(y[selected],rank),_readonly(ids[selected])
