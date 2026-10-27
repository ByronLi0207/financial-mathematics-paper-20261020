"""C2 post-result four-feature ridge QR; frozen originals are imported read-only."""
import sys
sys.dont_write_bytecode=True
import os
for _n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[_n]='1'
import argparse,json,time,csv,io,math,signal
from datetime import datetime,timezone
import numpy as np
from conditional_features import build_features,completed_training_indices,response_scale
from conditional_quantile import fit_quantile_ridge,QuantileFitError
from conditional_sources import load_source
from conditional_study import score_predictions,summarize_scores
from study_core import build_label_cache
from run_study import RunGuard
from v3_revision import ROOT,RESULT,dump,write,update_ledger

def features4(x,t,short,long,gap):
    f=build_features(x,t,short_scale=short,long_scale=long,nominal_gap_seconds=gap)
    return f.values[:,[25,0,26,27]].copy(),f.valid_from

def standardize(a):
    a=np.asarray(a,float)
    if a.ndim!=2 or a.shape[1]!=4 or not np.isfinite(a).all():raise ValueError('four finite training features required')
    mu=a.mean(axis=0);sd=a.std(axis=0);constant=np.all(a==a[0],axis=0)
    mu[constant]=a[0,constant];sd[constant]=1.;sd[sd==0]=1.
    return (a-mu)/sd,mu,sd

def forecast(x,feature,valid,cache,origins,h,w,step,lam,guard):
    caps=np.empty(len(origins));diagnostics=[];last=None;scale=mu=sd=fit=None
    last_probe=[-math.inf]
    def progress(_):
        now=time.monotonic()
        if now-last_probe[0]>=.25:guard(stage='four_feature_fit');last_probe[0]=now
    for j,t in enumerate(origins):
        r=int(origins[0])+step*((int(t)-int(origins[0]))//step)
        if r!=last:
            pool=completed_training_indices(r,h,w,minimum_feature_index=valid)
            assert int(cache.label_end[pool[-1]])==r
            train,mu,sd=standardize(feature[pool]);y=cache.headroom[pool]
            scale=response_scale(y,x[pool])
            fit=fit_quantile_ridge(np.column_stack([np.ones(w),train]),y/scale,tau=.95,penalty=lam,checkpoint=progress)
            diagnostics.append(dict(refit_index=r,training_first=int(pool[0]),training_last=int(pool[-1]),latest_label_end=int(cache.label_end[pool[-1]]),iterations=fit.iterations,gap=fit.duality_gap,gap_tolerance=fit.gap_tolerance))
            last=r
        query=(feature[t]-mu)/sd;head=scale*float(fit.coefficients[0]+query@fit.coefficients[1:])
        caps[j]=abs(x[t])+max(0.,head)
        if j%100==0:guard(stage='four_feature_issue')
    return caps,diagnostics

def cell(s,h,w):
    assert all((RESULT/'inference'/(b+'-complete.json')).exists() for b in ('B1','B3','B2','B4'))
    spec=json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_text());cfg=spec['sources'][s]
    attempt=ROOT/'.scratch/v3-parsimonious'/f'{s}-h{h}-w{w}';attempt.mkdir(parents=True,exist_ok=False)
    out=RESULT/'parsimonious';out.mkdir(exist_ok=True)
    started=time.monotonic();guard=RunGuard(started,datetime.now(timezone.utc).isoformat(),attempt,out,attempt)
    def timeout(*args):raise TimeoutError('ten-minute cell budget')
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,590)
    data=load_source(ROOT/cfg['input_relative_path'],s,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
    feature,valid=features4(data.position,data.dates,cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds'])
    cache=build_label_cache(data.position,h);guard.arrays(dict(features=feature,cache=cache));guard(stage='four_feature_source')
    origins=lambda phase:np.arange(cfg[phase+'_origin_first'],cfg[phase+'_origin_last']+1,dtype=np.int64)
    val=origins('validation');ev=origins('evaluation');candidates=[]
    for lam in [.001,.01,.1,1.,10.]:
        try:
            caps,diag=forecast(data.position,feature,valid,cache,val,h,w,cfg['refit_step'],lam,guard)
            scores=score_predictions(cache.peak[val],caps,np.abs(data.position[val]),val)
            candidates.append(dict(penalty=lam,status='COMPLETE',mean_pinball=summarize_scores(scores)['mean_pinball']))
        except QuantileFitError as error:
            candidates.append(dict(penalty=lam,status='FAILED',mean_pinball=None,reason=error.code))
    eligible=[r for r in candidates if r['status']=='COMPLETE']
    result=dict(source=s,horizon=h,window=w,post_result=True,candidates=candidates,selected_penalty=None,status='ALL_CANDIDATES_FAILED')
    if eligible:
        chosen=min(eligible,key=lambda r:r['mean_pinball']);lam=chosen['penalty'];result['selected_penalty']=lam
        try:
            caps,diag=forecast(data.position,feature,valid,cache,ev,h,w,cfg['refit_step'],lam,guard)
            scores=score_predictions(cache.peak[ev],caps,np.abs(data.position[ev]),ev)
            result.update(status='COMPLETE',evaluation=summarize_scores(scores),fit_diagnostics=diag)
            np.savez(attempt/'numeric-traces.npz',origins=ev,capacity=caps,peak=cache.peak[ev],pinball=scores.pinball)
        except QuantileFitError as error:result.update(status='EVALUATION_FAILED',reason=error.code)
    guard(stage='four_feature_end');result['resources']=guard.resources;dump(out/f'{s}-h{h}-w{w}.json',result)
    signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps({k:v for k,v in result.items() if k not in ('fit_diagnostics','candidates')}))

def aggregate():
    out=RESULT/'parsimonious';data=[];old=list(csv.DictReader((ROOT/'results/revision-20261022/evaluation-summary.csv').open()))
    for s,windows in [('nyfed_weekly',[52,260]),('fx_hourly',[720,2880])]:
        for h in [6,24]:
            for w in windows:
                r=json.loads((out/f'{s}-h{h}-w{w}.json').read_text())
                row={k:r[k] for k in ('source','horizon','window','status','selected_penalty')}
                if r['status']=='COMPLETE':
                    row.update(r['evaluation'])
                    lookup=lambda m:next(x for x in old if x['source']==s and int(x['horizon'])==h and int(x['window'])==w and x['method']==m)
                    for m in ['QR','frozen_F']:
                        ref=float(lookup(m)['mean_pinball']);row['percent_vs_'+m]=100*(r['evaluation']['mean_pinball']-ref)/ref
                        row['breaches_'+m]=int(lookup(m)['strict_breach_count'])
                data.append(row)
    f=io.StringIO(newline='');keys=list(dict.fromkeys(k for r in data for k in r));writer=csv.DictWriter(f,keys);writer.writeheader();writer.writerows(data);write(out/'summary.csv',f.getvalue())
    update_ledger('C2','COMPLETE: parsimonious_v3.py and its causal/known-feature tests implement intercept+4 predictors, the specified5 penalties, original chronological validation/evaluation/refit schedules and the frozen accepted ridge-QR solver. Eight complete source/H/W cells and all40 candidate records are retained in parsimonious/, with failures explicitly ineligible. summary.csv compares each against original QR and matched F. All results are post-result/exploratory and cannot replace original primaries. Predictors and penalty menu change together, so the result is not feature-only causal identification. Resource measurements are in each receipt; private traces stay in .scratch. No original result was overwritten.')
    print(json.dumps(data))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',choices=['nyfed_weekly','fx_hourly']);p.add_argument('--horizon',type=int);p.add_argument('--window',type=int);p.add_argument('--aggregate',action='store_true');a=p.parse_args()
    aggregate() if a.aggregate else cell(a.source,a.horizon,a.window)
