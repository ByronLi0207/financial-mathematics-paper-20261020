"""Classical Levy bound plug-in: no conditional coverage claim for empirical data."""
import numpy as np

def corrected_endpoint_rank(window):
    if isinstance(window,(bool,np.bool_)) or not isinstance(window,(int,np.integer)) or window<1:raise ValueError('positive integer W required')
    return (39*(int(window)+1)+39)//40

def gaussian_endpoint_variance(h,phi):
    if int(h)!=h or h<1 or not abs(phi)<1:raise ValueError('positive H and stationary phi required')
    return float(h+2*sum((h-j)*phi**j for j in range(1,h)))

def predict(positions,origins,horizon,window,refit_step,checkpoint=None):
    for v in (horizon,window,refit_step):
        if isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) or v<1:raise ValueError('positive integer schedule required')
    o=np.asarray(origins)
    if o.ndim!=1 or not len(o) or o.dtype.kind not in 'iu' or np.any(o<0) or np.any(np.diff(o)!=1):raise ValueError('consecutive issue origins required')
    x=np.asarray(positions)
    if x.ndim!=1 or x.dtype.kind not in 'iuf' or o[-1]>=len(x):raise ValueError('invalid positions')
    x=np.asarray(x[:int(o[-1])+1],float)
    if not np.isfinite(x).all():raise ValueError('nonfinite observed position')
    rank=corrected_endpoint_rank(window)
    if rank>window or int(o[0])-horizon-window+1<0:raise ValueError('insufficient mature pool')
    cap=np.empty(len(o));refit=np.empty(len(o),np.int64);end=np.empty(len(o),np.int64);previous=None;records=[]
    for j,t in enumerate(o):
        t=int(t);r=int(o[0])+refit_step*((t-int(o[0]))//refit_step)
        if r!=previous:
            pool=np.arange(r-horizon-window+1,r-horizon+1,dtype=np.int64);endpoints=np.abs(x[pool+horizon]-x[pool]);q=float(np.sort(endpoints)[rank-1]);previous=r
            records.append(dict(refit_index=r,training_first=int(pool[0]),training_last=int(pool[-1]),latest_label_end=int(pool[-1])+horizon,one_based_rank=rank,endpoint_quantile=q))
            if checkpoint:checkpoint(stage='Levy_refit')
        cap[j]=abs(float(x[t]))+q;refit[j]=r;end[j]=r
    return dict(origins=o.copy(),capacity=cap,refit_indices=refit,latest_label_end=end,refits=records)
