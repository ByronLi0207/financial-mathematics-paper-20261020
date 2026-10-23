"""D2 correction: level mean reversion and negative increment correlation.

Every quantile is a population endpoint oracle, never a fitted peak quantile.
The empirical L financial outputs and old positive-increment study are read only.
"""
import argparse
import hashlib
import json
import math
import signal
import time
from datetime import datetime, timezone
from statistics import NormalDist
import numpy as np
from round2_levy import gaussian_endpoint_variance


def _parameters(h,phi):
    if isinstance(h,(bool,np.bool_)) or not isinstance(h,(int,np.integer)) or h<1:
        raise ValueError('positive integer horizon required')
    if isinstance(phi,(bool,np.bool_)) or not isinstance(phi,(int,float,np.integer,np.floating)) or not math.isfinite(phi) or abs(phi)>=1:
        raise ValueError('stationary finite AR coefficient required')


def level_endpoint_parameters(h,phi,x=None):
    _parameters(h,phi)
    if x is None:return 0.,float(2*(1-phi**h))
    if not math.isfinite(x):raise ValueError('finite fixed starting level required')
    return float((phi**h-1)*x),float(1-phi**(2*h))


def level_increment_autocorrelation(phi,lag):
    _parameters(lag,phi)
    return float(-(1-phi)*phi**(lag-1)/2)


def absolute_gaussian_quantile(p,mu,variance):
    if not all(math.isfinite(a) for a in (p,mu,variance)) or not 0<p<1 or variance<0:
        raise ValueError('valid folded-normal probability/mean/variance required')
    if variance==0:return abs(float(mu))
    sigma=math.sqrt(variance);normal=NormalDist(mu,sigma)
    lo=0.;hi=abs(mu)+sigma*NormalDist().inv_cdf((1+p)/2)
    # The triangle bound ensures this upper bracket has CDF at least p.
    for _ in range(100):
        mid=(lo+hi)/2
        if normal.cdf(mid)-normal.cdf(-mid)<p:lo=mid
        else:hi=mid
    return hi


def _innovations(z):
    a=np.asarray(z,float)
    if a.ndim!=2 or a.shape[0]<1 or a.shape[1]<1 or not np.isfinite(a).all():
        raise ValueError('finite nonempty standardized innovation matrix required')
    return a


def level_paths(z,x,phi):
    z=_innovations(z);_parameters(z.shape[1],phi);x=np.asarray(x,float)
    if x.shape!=(len(z),) or not np.isfinite(x).all():raise ValueError('one finite starting level per path required')
    paths=np.empty((len(z),z.shape[1]+1));paths[:,0]=x
    scale=math.sqrt(1-phi**2)
    for j in range(z.shape[1]):paths[:,j+1]=phi*paths[:,j]+scale*z[:,j]
    return paths


def increment_paths(z,phi):
    z=_innovations(z);_parameters(z.shape[1],phi)
    increments=np.empty_like(z);increments[:,0]=z[:,0]
    scale=math.sqrt(1-phi**2)
    for j in range(1,z.shape[1]):increments[:,j]=phi*increments[:,j-1]+scale*z[:,j]
    return np.column_stack((np.zeros(len(z)),np.cumsum(increments,axis=1)))


def exceedance_counts(paths,threshold):
    paths=np.asarray(paths,float);threshold=np.asarray(threshold,float)
    if paths.ndim!=2 or paths.shape[1]<2 or threshold.shape!=(len(paths),) or not np.isfinite(paths).all() or not np.isfinite(threshold).all() or np.any(threshold<np.abs(paths[:,0])):
        raise ValueError('finite paths and valid L floors required')
    q=threshold-np.abs(paths[:,0])
    return int(np.sum(np.max(np.abs(paths),axis=1)>threshold)),int(np.sum(np.abs(paths[:,-1]-paths[:,0])>q))


def simulate_cell(model,h,phi,anchor,n,batch,seed,checkpoint=None):
    _parameters(h,phi)
    for a in (n,batch,seed):
        if isinstance(a,(bool,np.bool_)) or not isinstance(a,(int,np.integer)) or a<1:raise ValueError('positive integer simulation control required')
    if model not in ('level','increment'):raise ValueError('named mechanism required')
    if (model=='increment' and anchor!='zero') or (model=='level' and anchor not in ('stationary','absolute95','signed95')):
        raise ValueError('anchor does not match mechanism')
    streams=np.random.SeedSequence(seed).spawn(2)
    rng_x=np.random.Generator(np.random.PCG64(streams[0]));rng_z=np.random.Generator(np.random.PCG64(streams[1]))
    if model=='increment':
        x0=0.;mu=0.;variance=gaussian_endpoint_variance(h,phi);q_information='stationary_increment_endpoint'
    else:
        x0=None if anchor=='stationary' else NormalDist().inv_cdf(.975 if anchor=='absolute95' else .95)
        mu,variance=level_endpoint_parameters(h,phi);q_information='stationary_marginal_endpoint'
    thresholds=[(q_information,absolute_gaussian_quantile(.975,mu,variance),mu,variance)]
    if model=='level' and x0 is not None:
        cm,cv=level_endpoint_parameters(h,phi,x0)
        thresholds.append(('conditional_endpoint_oracle',absolute_gaussian_quantile(.975,cm,cv),cm,cv))
    counts=[[0,0] for _ in thresholds]
    for start in range(0,n,batch):
        count=min(batch,n-start);z=rng_z.standard_normal((count,h))
        if model=='increment':paths=increment_paths(z,phi)
        else:
            x=rng_x.standard_normal(count) if x0 is None else np.full(count,x0)
            paths=level_paths(z,x,phi)
        for i,(_,q,_,_) in enumerate(thresholds):
            k,e=exceedance_counts(paths,np.abs(paths[:,0])+q);counts[i][0]+=k;counts[i][1]+=e
        if checkpoint:checkpoint(stage='D2_AR_correction_batch')
    rows=[]
    for (information,q,m,v),(k,e) in zip(thresholds,counts):
        primary=information!='conditional_endpoint_oracle' and anchor!='signed95'
        rate=k/n;endpoint=e/n
        rows.append(dict(model=model,horizon=h,phi=float(phi),anchor=anchor,initial_abs_value=x0,q_information=information,
            primary_design=primary,seed=int(seed),paths=int(n),population_endpoint_mean=m,population_endpoint_variance=v,
            oracle_abs_endpoint_quantile=q,max_exceedances=k,endpoint_exceedances=e,max_exceedance_rate=rate,
            endpoint_exceedance_rate=endpoint,rate_minus_point05=rate-.05,rate_minus_five_percentage_points=100*(rate-.05),
            monte_carlo_standard_error=math.sqrt(rate*(1-rate)/n),max_rate_minus_two_endpoint_rate=rate-2*endpoint,
            stationary_reference_increment_lag1_correlation=level_increment_autocorrelation(phi,1) if model=='level' else float(phi),
            independence_premise=False,post_result=True,exploratory=True))
    return rows


def main():
    from v3_revision import ROOT,RESULT,dump,write
    from run_study import RunGuard
    import csv,io
    out=RESULT/'round2/levy-ar-correction';binding=ROOT/'protocol/revision-20261023/D2-AR-correction-binding.json'
    b=json.loads(binding.read_text())
    for filename,expected in b['sha256'].items():
        if hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()!=expected:raise ValueError('pre-execution binding changed: '+filename)
    if (out/'simulation.json').exists() or (out/'simulation.csv').exists():raise ValueError('retained correction result already exists; no overwrite or retry')
    out.mkdir(parents=True,exist_ok=True);private=ROOT/'.scratch/round2/levy-ar-correction';private.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();guard=RunGuard(start,datetime.now(timezone.utc).isoformat(),private,out,private)
    def timeout(*_):raise TimeoutError('D2 correction hard590-second budget')
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,590)
    rows=[]
    for h in (6,24):
        for family,model,phis in [(1,'level',(.68,.85,.98)),(2,'increment',(-.3,-.6))]:
            for index,phi in enumerate(phis):
                anchors=['stationary','absolute95','signed95'] if model=='level' else ['zero']
                for anchor_index,anchor in enumerate(anchors):
                    seed=20261023+300000+1000*h+100*family+10*index+anchor_index
                    rows.extend(simulate_cell(model,h,phi,anchor,100000,5000,seed,guard))
    guard(stage='D2_AR_correction_complete');signal.setitimer(signal.ITIMER_REAL,0)
    assert len(rows)==34 and sum(r['primary_design'] for r in rows)==16
    record=dict(design='frozen D2 AR correction:16 primary and18 prespecified secondary threshold rows on22 independent initialized path cells',
        protocol_sha256=b['sha256']['protocol/revision-20261023/D2-AR-correction-20261023.md'],binding_sha256=hashlib.sha256(binding.read_bytes()).hexdigest(),
        numpy_version=np.__version__,rng='SeedSequence.spawn(2), PCG64; separate initial-level and innovation streams',results=rows,resources=guard.resources)
    dump(out/'simulation.json',record)
    text=io.StringIO(newline='');writer=csv.DictWriter(text,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows);write(out/'simulation.csv',text.getvalue())
    print(json.dumps(record,ensure_ascii=False,allow_nan=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true',required=True);parser.parse_args();main()
