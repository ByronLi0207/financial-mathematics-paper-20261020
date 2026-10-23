"""Finite delayed ACI-style calibration; not the canonical ACI guarantee.

No source I/O. Scores use earlier prefix base reports, feedback uses the actual
earlier wrapped report, and every outcome enters only at its H-record maturity.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction
import math
import numpy as np


GAMMAS=(.001,.005,.01,.05)
TARGET=Fraction(1,20)


class InsufficientCalibration(ValueError):
    code='INSUFFICIENT_PREVALIDATION_CALIBRATION'


def finite_rank(alpha, count):
    """Exact corrected rank on the explicitly finite alpha domain."""
    a=alpha if isinstance(alpha,Fraction) else Fraction(str(alpha))
    if type(count) is not int or count<1 or not Fraction(1,count+1)<=a<=1:
        raise ValueError('alpha outside finite corrected-rank domain')
    v=(count+1)*(1-a)
    return -(-v.numerator//v.denominator)


def initialization_grid(first,horizon,window,step,minimum_feature_index):
    values=(first,horizon,window,step,minimum_feature_index)
    if any(type(v) is not int for v in values) or min(first,minimum_feature_index)<0 or min(horizon,window,step)<1:
        raise ValueError('invalid original grid')
    minimum_refit=minimum_feature_index+horizon+window-1
    legal=first+-(-(minimum_refit-first)//step)*step
    desired=first-((window+horizon-1+step-1)//step)*step
    pre_first=max(legal,desired)
    return dict(first_legal_refit=legal,pre_first=pre_first,pre_last=first-1,
                mature_initial_count=min(window,max(0,first-horizon-pre_first+1)))


def _origins(value,name):
    raw=np.asarray(value)
    if raw.ndim!=1 or raw.dtype.kind not in 'iu' or np.any(raw<0) or np.any(raw>np.iinfo(np.int64).max):
        raise ValueError(name+' must be strictly increasing nonnegative integer origins')
    raw=raw.astype(np.int64,copy=False)
    if np.any(raw[1:]<=raw[:-1]):raise ValueError(name+' must be strictly increasing')
    return raw


def _vector(value,count,name):
    v=np.asarray(value,dtype=float)
    if v.shape!=(count,) or not np.isfinite(v).all():
        raise ValueError(name+' must be finite and aligned')
    return v


def aci_stream(*,origins,base,peak,floor,horizon,window,gamma,
               warm_origins,warm_base,warm_peak,minimum_calibration=19,checkpoint=None):
    """One causal validation/evaluation stream, allowing unissued clock gaps.

    The caller owns base-model grid/fit provenance. To carry validation state,
    concatenate exactly its issued rows and the evaluation rows after freezing
    gamma. Never manufacture reports for the intervening unissued gap.
    Per-origin return fields and feedback_records are private trace material.
    """
    ids=_origins(origins,'issued');warm=_origins(warm_origins,'warmup')
    if not len(ids) or (len(warm) and warm[-1]>=ids[0]):
        raise ValueError('nonempty issues and earlier nonoverlapping warmup required')
    if any(type(v) is not int or v<1 for v in (horizon,window,minimum_calibration)) or window<minimum_calibration:
        raise ValueError('invalid horizon/calibration budget')
    g=Fraction(str(gamma))
    if g<=0 or g>=1:raise ValueError('interior positive gamma required')
    b=_vector(base,len(ids),'base');y=_vector(peak,len(ids),'peak');f=_vector(floor,len(ids),'floor')
    wb=_vector(warm_base,len(warm),'warm base');wy=_vector(warm_peak,len(warm),'warm peak')
    if np.any(f<0) or np.any(b<f) or np.any(y<f) or np.any(wy<0) or np.any(wb<0):
        raise ValueError('invalid absolute peak/floor/base')
    all_ids=np.concatenate((warm,ids));all_b=np.concatenate((wb,b));all_y=np.concatenate((wy,y))
    n=len(ids);caps=np.empty(n);alphas=np.empty(n);counts=np.empty(n,dtype=np.int64)
    score_quantiles=np.empty(n);raw_thresholds=np.empty(n)
    ranks=np.empty(n,dtype=np.int64);feedback_counts=np.zeros(n,dtype=np.int64)
    clip_counts=np.zeros(n,dtype=np.int64);state_fractions=[];feedback_records=[]
    scores=deque(maxlen=window);score_cursor=0;hit_cursor=0;a=TARGET
    initial_count=None
    for j,t0 in enumerate(ids):
        t=int(t0)
        while score_cursor<len(all_ids) and int(all_ids[score_cursor])+horizon<=t:
            score=float(all_y[score_cursor])-float(all_b[score_cursor])
            if not math.isfinite(score):raise ValueError('nonfinite matured score')
            scores.append((int(all_ids[score_cursor]),score));score_cursor+=1
        m=len(scores)
        if initial_count is None:
            initial_count=m
            if m<minimum_calibration:
                raise InsufficientCalibration(f'{m} completed scores; need {minimum_calibration}')
        lower=Fraction(1,m+1)
        while hit_cursor<j and int(ids[hit_cursor])+horizon<=t:
            error=int(y[hit_cursor]>caps[hit_cursor])
            raw=a+g*(TARGET-error);a=min(Fraction(1),max(lower,raw))
            clipped=a!=raw;clip_counts[j]+=int(clipped)
            feedback_records.append(dict(origin=int(ids[hit_cursor]),consumed_at=t,
                issued_capacity=float(caps[hit_cursor]),strict_hit=error,
                raw_update=str(raw),projected_state=str(a),calibration_count=m,
                clipped=bool(clipped)))
            hit_cursor+=1;feedback_counts[j]+=1
        projected=min(Fraction(1),max(lower,a))
        clip_counts[j]+=int(projected!=a);a=projected
        k=finite_rank(a,m)
        if k==0:q=-math.inf;raw_threshold=-math.inf;capacity=float(f[j])
        else:
            values=np.fromiter((v for _,v in scores),dtype=float,count=m)
            q=float(np.partition(values,k-1)[k-1]);raw_threshold=float(b[j])+q;capacity=max(float(f[j]),raw_threshold)
        if not math.isfinite(capacity):raise ValueError('nonfinite wrapped report')
        caps[j]=capacity;score_quantiles[j]=q;raw_thresholds[j]=raw_threshold
        alphas[j]=float(a);counts[j]=m;ranks[j]=k;state_fractions.append(str(a))
        if checkpoint is not None and (j%32==0 or j==n-1):
            checkpoint(stage='aci_issue',completed_origins=j+1)
    return dict(origins=ids.copy(),capacities=caps,score_quantiles=score_quantiles,raw_thresholds=raw_thresholds,floor=f.copy(),alpha=alphas,calibration_counts=counts,
                ranks=ranks,feedback_counts=feedback_counts,clip_counts=clip_counts,
                state_fractions=tuple(state_fractions),feedback_records=tuple(feedback_records),
                initial_calibration_count=initial_count,feedback_consumed=hit_cursor,
                gamma=float(g),method='finite delayed ACI-style calibration')


def select_gamma(candidates,*,expected_count):
    """Coverage-first complete-procedure selection with explicit failed rows."""
    if type(expected_count) is not int or expected_count<1:
        raise ValueError('positive original validation count required')
    if len(candidates)!=len(GAMMAS) or sorted(r.get('gamma') for r in candidates)!=list(GAMMAS):
        raise ValueError('complete fixed gamma inventory required')
    eligible=[];failed=[]
    for row in candidates:
        g=row['gamma'];n=row.get('origin_count');hits=row.get('hits');loss=row.get('mean_loss')
        if row.get('status')!='COMPLETE' or n!=expected_count:
            failed.append(g);continue
        if type(hits) is not int or not 0<=hits<=n or not isinstance(loss,(float,int)) or not math.isfinite(loss) or loss<0:
            failed.append(g);continue
        distance=abs(Fraction(hits,n)-TARGET)
        eligible.append((distance,float(loss),g))
    if not eligible:return dict(status='NA',gamma=None,failed_gamma=sorted(failed))
    distance,loss,g=min(eligible)
    return dict(status='SELECTED',gamma=g,coverage_distance=float(distance),mean_loss=loss,
                failed_gamma=sorted(failed),tuning='absolute coverage distance, then pinball, then smaller gamma')
