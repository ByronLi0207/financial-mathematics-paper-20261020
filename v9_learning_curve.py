"""Frozen retrospective curve/HAC and exact legacy readback primitives."""
import math
import numpy as np

class BaselineMismatch(AssertionError):
    pass

def exact_arrays(actual, archived):
    count=values=0
    for key,old in archived.items():
        if key not in actual:raise BaselineMismatch('missing legacy array '+key)
        new=np.asarray(actual[key]);old=np.asarray(old)
        if new.shape!=old.shape or new.dtype!=old.dtype or new.dtype.kind not in 'bifu' or not np.isfinite(new).all() or not np.isfinite(old).all() or new.tobytes(order='C')!=old.tobytes(order='C'):
            raise BaselineMismatch('exact legacy array mismatch '+key)
        count+=1;values+=old.size
    return dict(arrays_checked=count,values_checked=int(values),mismatches=0)

def exact_tree(actual, archived, location='science'):
    if isinstance(archived,dict):
        if not isinstance(actual,dict):raise BaselineMismatch(location+' type')
        total=0
        for key,value in archived.items():
            if key not in actual:raise BaselineMismatch(location+'.'+key+' missing')
            total+=exact_tree(actual[key],value,location+'.'+key)
        return total
    if isinstance(archived,(list,tuple)):
        if not isinstance(actual,(list,tuple)) or len(actual)!=len(archived):raise BaselineMismatch(location+' length')
        return sum(exact_tree(a,b,location+f'[{i}]') for i,(a,b) in enumerate(zip(actual,archived)))
    if actual!=archived or (type(archived) in (int,float) and (type(actual) not in (int,float) or not math.isfinite(actual))):
        raise BaselineMismatch(location+' exact scalar mismatch')
    return int(type(archived) in (int,float))

def classify_curve(windows, deltas, lower, upper):
    w=list(windows);y=list(deltas)
    if len(w)!=len(y) or not w or any(a>=b for a,b in zip(w,w[1:])) or any(x<=0 for x in w) or any(v is not None and not math.isfinite(v) for v in y):raise ValueError('invalid fixed curve rows')
    roots=[];right_ids=[]
    for i in range(1,len(w)):
        if y[i-1] is not None and y[i] is not None and y[i-1]>0 and y[i]<=0:
            roots.append(w[i-1]+(w[i]-w[i-1])*y[i-1]/(y[i-1]-y[i]));right_ids.append(i)
    result=dict(windows=w,relative_losses=y,first_crossing=None,conditional_crossings=roots,multiple_crossings=len(roots)>1,first_right_endpoint_strictly_negative=None,observed_left_censoring=False,prediction_range=[lower,upper])
    if lower is None or lower<=0 or upper is None or not math.isfinite(upper) or upper<lower:
        result['prediction_status']='NOT_TESTABLE_NONDISCRIMINATING_INTERVAL';return result
    if y[0] is None:
        result['prediction_status']='NOT_TESTABLE_NA_PREFIX';return result
    if y[0]<=0:
        result.update(observed_left_censoring=True,prediction_status='INCONSISTENT_LEFT_CENSORED' if lower>w[0] else 'NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED');return result
    if roots:
        right=right_ids[0]
        if any(v is None for v in y[:right+1]):
            result['prediction_status']='NOT_TESTABLE_NA_PREFIX';return result
        root=roots[0]
        result.update(first_crossing=root,first_right_endpoint_strictly_negative=y[right]<0,prediction_status='FIRST_CUTPOINT_CONSISTENT' if lower<=root<=upper else 'FIRST_CUTPOINT_INCONSISTENT');return result
    prefix_end=next((i for i,v in enumerate(y) if v is None),len(y))
    if prefix_end and all(v>0 for v in y[:prefix_end]) and lower>=w[0] and upper<=w[prefix_end-1]:
        result['prediction_status']='INCONSISTENT_NO_CROSSING'
    else:result['prediction_status']='NOT_TESTABLE_NO_CROSSING'
    return result

def dm_hac_only(difference,horizon):
    from inference_tests import bandwidth,hac
    d=np.asarray(difference,float)
    if d.ndim!=1 or len(d)<=horizon or not np.isfinite(d).all():raise ValueError('invalid complete paired losses')
    n=len(d);lag=bandwidth(n,horizon);mean=math.fsum(map(float,d))/n
    out=dict(n=n,horizon=horizon,bandwidth=lag,direction='QR_minus_matched_F',mean_difference=mean,lrv=None,dm_t=None,dm_p=None,status='OK',nominal_post_result=True)
    if np.all(d==d[0]):
        out['lrv']=0.;out['status']='IDENTICAL_LOSSES' if d[0]==0 else 'ZERO_LONG_RUN_VARIANCE';return out
    with np.errstate(over='raise',invalid='raise'):
        variance=float(hac(d,lag)[0,0])
    out['lrv']=variance
    if not math.isfinite(variance) or variance<=0:
        out['status']='NONPOSITIVE_LONG_RUN_VARIANCE';return out
    statistic=mean/math.sqrt(variance/n)
    if not math.isfinite(statistic):out['status']='NONFINITE_STATISTIC';return out
    out.update(dm_t=statistic,dm_p=math.erfc(abs(statistic)/math.sqrt(2)))
    return out
