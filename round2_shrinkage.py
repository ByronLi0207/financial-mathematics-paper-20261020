"""Selected-fit Treasury C2 readback only; all original outputs remain read-only."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import argparse,hashlib,json,math,signal,time
from datetime import datetime,timezone
import numpy as np
import parsimonious_v3 as c2
from empirical_headroom import predict
from v3_revision import ROOT,RESULT,dump
from conditional_sources import load_source
from conditional_features import completed_training_indices,response_scale
from study_core import build_label_cache
from run_study import RunGuard

def contributions(query,coefficients,scale):
    z=np.asarray(query,float);b=np.asarray(coefficients,float)
    raw=scale*(z@b[1:]);intercept=scale*b[0]
    return raw,np.maximum(0.,intercept+raw)-max(0.,intercept)

def descriptive(x):
    x=np.asarray(x,float)
    return dict(mean=float(x.mean()),mean_absolute=float(np.abs(x).mean()),maximum_absolute=float(np.abs(x).max()))

def corr(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    if np.all(a==a[0]) or np.all(b==b[0]):return None
    return float(np.corrcoef(a,b)[0,1])

def compare(left,right,peak,floor):
    left,right,peak,floor=map(lambda x:np.asarray(x,float),(left,right,peak,floor))
    d=left-right;a=peak>left;b=peak>right;union=int(np.sum(a|b));intersection=int(np.sum(a&b))
    loss=lambda cap:.95*np.maximum(peak-cap,0.)+.05*np.maximum(cap-peak,0.)
    ll,rr=loss(left),loss(right)
    return dict(capacity_difference=descriptive(d),capacity_correlation=corr(left,right),headroom_correlation=corr(left-floor,right-floor),correlation_undefined_reason='constant input' if corr(left,right) is None or corr(left-floor,right-floor) is None else '',left_breaches=int(a.sum()),right_breaches=int(b.sum()),breach_intersection=intersection,breach_union=union,breach_jaccard=intersection/union if union else None,breach_jaccard_undefined_reason='empty union' if not union else '',left_only_breaches=int(np.sum(a&~b)),right_only_breaches=int(np.sum(b&~a)),breach_xor=int(np.sum(a^b)),mean_pinball_left=float(ll.mean()),mean_pinball_right=float(rr.mean()),mean_pinball_difference=float((ll-rr).mean()),percent_pinball_difference=100*float(ll.mean()-rr.mean())/float(rr.mean()) if rr.mean() else None)

def cell(h,w):
    started=time.monotonic();utc=datetime.now(timezone.utc).isoformat();out=RESULT/'round2/shrinkage';attempt=ROOT/'.scratch/round2/shrinkage'/f'nyfed-h{h}-w{w}';attempt.mkdir(parents=True,exist_ok=False);out.mkdir(parents=True,exist_ok=True)
    guard=RunGuard(started,utc,attempt,out,attempt)
    def alarm(*_):raise TimeoutError('E9 cell ten-minute limit')
    signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,590)
    spec=json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_text());cfg=spec['sources']['nyfed_weekly'];selection=RESULT/'parsimonious'/f'nyfed_weekly-h{h}-w{w}.json';old=json.loads(selection.read_text());lam=old['selected_penalty'];assert old['status']=='COMPLETE'
    data=load_source(ROOT/cfg['input_relative_path'],'nyfed_weekly',expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes']);x=data.position
    feature,valid=c2.features4(x,data.dates,cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds']);cache=build_label_cache(x,h);ev=np.arange(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,dtype=np.int64)
    original_solver=c2.fit_quantile_ridge;fits=[]
    def capture(*args,**kwargs):
        fit=original_solver(*args,**kwargs);fits.append(fit.coefficients.copy());return fit
    c2.fit_quantile_ridge=capture
    try:caps,diagnostics=c2.forecast(x,feature,valid,cache,ev,h,w,cfg['refit_step'],lam,guard)
    finally:c2.fit_quantile_ridge=original_solver
    saved=ROOT/'.scratch/v3-parsimonious'/f'nyfed_weekly-h{h}-w{w}/numeric-traces.npz'
    with np.load(saved) as z:
        assert np.array_equal(ev,z['origins']);exact=bool(np.array_equal(caps,z['capacity']));maxdiff=float(np.abs(caps-z['capacity']).max());assert exact
    refs=predict(x,ev,h,w,cfg['refit_step']);refpath=ROOT/'.scratch/revision-20261022/replication-revision-v3-b5-full'/f'references-nyfed_weekly-h{h}-w{w}/private/numeric-traces.npz'
    with np.load(refpath) as z:
        assert np.array_equal(ev,z['frozen_F_origins']);assert np.array_equal(refs['F'],z['frozen_F_capacity']);assert np.array_equal(refs['refit_indices'],z['frozen_F_refit_indices'])
    records=[];raw_all=[];projected_all=[]
    for d,coeff in zip(diagnostics,fits,strict=True):
        r=d['refit_index'];pool=completed_training_indices(r,h,w,minimum_feature_index=valid);_,mu,sd=c2.standardize(feature[pool]);scale=response_scale(cache.headroom[pool],x[pool]);mask=refs['refit_indices']==r;query=(feature[ev[mask]]-mu)/sd
        raw,projected=contributions(query,coeff,scale);raw_all.extend(raw);projected_all.extend(projected)
        rec=dict(**d,query_count=int(mask.sum()),penalty=lam,coefficients=coeff.tolist(),slope_l2_norm=float(np.linalg.norm(coeff[1:])),maximum_absolute_slope=float(np.abs(coeff[1:]).max()),response_scale=float(scale),feature_training_mean=mu.tolist(),feature_training_sd=sd.tolist(),raw_native_slope_contribution=descriptive(raw),projected_native_slope_contribution=descriptive(projected));records.append(rec)
    assert len(records)==len(fits);floor=np.abs(x[ev]);peak=cache.peak[ev]
    result=dict(source='nyfed_weekly',horizon=h,window=w,native_unit=cfg.get('native_unit','USD millions'),post_result=True,exploratory=True,selected_penalty=lam,selection_sha256=hashlib.sha256(selection.read_bytes()).hexdigest(),source_sha256=cfg['sha256'],n=len(ev),refits=records,c2_replay_array_equal=exact,c2_replay_max_abs_difference=maxdiff,frozen_F_replay_array_equal=True,aggregate_raw_native_slope_contribution=descriptive(raw_all),aggregate_projected_native_slope_contribution=descriptive(projected_all),comparison_I=compare(caps,refs['I'],peak,floor),comparison_F=compare(caps,refs['F'],peak,floor))
    guard(stage='E9_final');result['resources']=guard.resources;dump(out/f'nyfed-h{h}-w{w}.json',result);signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps({k:v for k,v in result.items() if k!='refits'},ensure_ascii=False,allow_nan=False))
    print('Per-refit coefficients and contributions:')
    for r in records:print(json.dumps(r,allow_nan=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--horizon',type=int,choices=[6,24],required=True);p.add_argument('--window',type=int,choices=[52,260],required=True);a=p.parse_args();cell(a.horizon,a.window)
