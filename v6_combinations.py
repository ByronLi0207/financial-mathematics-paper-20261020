"""Untuned report combinations and integer-event Murphy signs; no source I/O."""
from fractions import Fraction
import math
import numpy as np
from v6_inference import pinball_losses

METHODS=('MEAN_F_QR','MEDIAN_F_QR_KNN')

def combine_reports(origins,floor,F,QR,KNN):
    raw=np.asarray(origins)
    if raw.ndim!=1 or not len(raw) or raw.dtype.kind not in 'iu' or np.any(raw>np.iinfo(np.int64).max):raise ValueError('COMPLETE_INTEGER_ISSUE_AXIS_REQUIRED')
    ids=raw.astype(np.int64,copy=False)
    if np.any(ids<0) or np.any(np.diff(ids)!=1):raise ValueError('ORIGINAL_CONTIGUOUS_ISSUE_AXIS_REQUIRED')
    def vector(value):
        x=np.asarray(value,dtype=float)
        if x.shape!=ids.shape or not np.isfinite(x).all():raise ValueError('ALIGNED_FINITE_REPORT_REQUIRED')
        return x
    b,f,q=map(vector,(floor,F,QR))
    if np.any(b<0) or np.any(f<b) or np.any(q<b):raise ValueError('FLOOR_GEOMETRY')
    mean=f/2+q/2
    out={METHODS[0]:dict(status='COMPLETE',capacity=mean,identity='EXACTLY_F' if np.array_equal(mean,f) else 'EXACTLY_QR' if np.array_equal(mean,q) else None)}
    if KNN is None:out[METHODS[1]]=dict(status='NA',reason='ORIGINAL_PLAIN_KNN_NOT_AVAILABLE')
    else:
        k=vector(KNN)
        if np.any(k<b):raise ValueError('KNN_FLOOR_GEOMETRY')
        median=np.median(np.stack((f,q,k)),axis=0)
        out[METHODS[1]]=dict(status='COMPLETE',capacity=median,identity='EXACTLY_F' if np.array_equal(median,f) else 'EXACTLY_QR' if np.array_equal(median,q) else 'EXACTLY_KNN' if np.array_equal(median,k) else None)
    for r in out.values():
        if r['status']=='COMPLETE' and (not np.isfinite(r['capacity']).all() or np.any(r['capacity']<b)):raise ValueError('NONFINITE_OR_INFEASIBLE_COMBINATION')
    return out

def murphy_exact(left,right,actual,*,tau):
    a,b,y=map(lambda x:np.asarray(x,dtype=float),(left,right,actual))
    if a.ndim!=1 or not len(a) or a.shape!=b.shape or a.shape!=y.shape or not all(np.isfinite(v).all() for v in (a,b,y)):raise ValueError('COMPLETE_ALIGNED_MURPHY_REQUIRED')
    t=Fraction(str(tau))
    if not 0<t<1 or t.denominator>1000000:raise ValueError('FINITE_DECLARED_DECIMAL_TAU_REQUIRED')
    theta=np.unique(np.concatenate((a,b,y)));n=len(y)
    def events(x):
        delta=np.zeros(len(theta)+1,dtype=np.int64)
        lower=np.minimum(x,y);upper=np.maximum(x,y)
        lo=np.searchsorted(theta,lower);hi=np.searchsorted(theta,upper)
        weight=np.where(x>y,t.denominator-t.numerator,t.numerator).astype(np.int64)
        np.add.at(delta,lo,weight);np.add.at(delta,hi,-weight)
        return np.cumsum(delta[:-1])
    an,bn=events(a),events(b);dn=an-bn;den=t.denominator*n
    pos=bool(np.any(dn>0));neg=bool(np.any(dn<0))
    ranking='CROSSING' if pos and neg else 'LEFT_DOMINATES_SAMPLE' if neg else 'RIGHT_DOMINATES_SAMPLE' if pos else 'EQUAL_SAMPLE'
    d=dn/den
    losses=pinball_losses(y,a,tau=float(t))-pinball_losses(y,b,tau=float(t))
    mean=math.fsum(map(float,losses))/n
    integral=math.fsum(map(float,np.diff(theta)*d[:-1]))
    return dict(theta=theta,left=an/den,right=bn/den,difference=d,integer_difference=dn,
        ranking=ranking,comparison_grid='ALL_UNIQUE_BREAKPOINTS_INTEGER_EVENT_SIGNS',
        breakpoint_count=len(theta),positive_breakpoints=int(np.count_nonzero(dn>0)),
        negative_breakpoints=int(np.count_nonzero(dn<0)),zero_breakpoints=int(np.count_nonzero(dn==0)),
        integral_difference=integral,pinball_difference=mean,
        integral_minus_pinball=integral-mean,elementary_weight_denominator=den,tau=float(t))
