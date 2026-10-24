"""Serial bounded D2 experiments; original forecasts and archives read only."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import argparse,csv,io,json,signal,time
from datetime import datetime,timezone
from uuid import uuid4
from statistics import NormalDist
import numpy as np
from v3_revision import ROOT,RESULT,write,dump
from round2_levy import predict,gaussian_endpoint_variance
from conditional_sources import load_source
from conditional_study import score_predictions,summarize_scores
from inference_tests import dm_test,holm
from run_study import RunGuard
OUT=RESULT/'round2/levy'

def guard_for(name):
    start=time.monotonic();p=ROOT/'.scratch/round2/levy'/name
    if p.exists():p=p.with_name(name+'-retry-'+uuid4().hex[:8])
    p.mkdir(parents=True,exist_ok=False);OUT.mkdir(parents=True,exist_ok=True)
    def alarm(*_):raise TimeoutError('D2 ten-minute worker limit')
    signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,590)
    return RunGuard(start,datetime.now(timezone.utc).isoformat(),p,OUT,p),p

def cell(s,h,w):
    guard,p=guard_for(f'{s}-h{h}-w{w}');spec=json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_text());cfg=spec['sources'][s]
    data=load_source(ROOT/cfg['input_relative_path'],s,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
    from run_v3_inference import traces
    reference=traces();f=reference[s,h,w,'frozen_F'];qr=reference[s,h,w,'QR'];o=f['origins'];assert np.array_equal(o,qr['origins'])
    result=predict(data.position,o,h,w,cfg['refit_step'],checkpoint=guard);scores=score_predictions(f['peak'],result['capacity'],f['floor'],o);summary=summarize_scores(scores)
    paired=[]
    for method,a in [('frozen_F',f),('QR',qr)]:
        assert np.array_equal(a['origins'],o) and np.array_equal(a['peak'],f['peak']);d=scores.pinball-a['pinball'];z=dm_test(d,h);zz=dm_test(d,h,min(len(d)-1,2*z['bandwidth']))
        paired.append(dict(source=s,window=w,left_method='Levy_L',right_method=method,contrast_id=f'{s}-h{h}-w{w}-Levy_L-minus-{method}',post_result=True,exploratory=True,relative_loss_percent=100*(summary['mean_pinball']-float(a['pinball'].mean()))/float(a['pinball'].mean()),reference_strict_breaches=int(np.sum(a['peak']>a['capacity'])),**z,double_bandwidth=zz['bandwidth'],double_dm_t=zz['dm_t'],double_dm_p=zz['dm_p'],double_hln_p=zz['hln_p']))
    np.savez(p/'numeric-traces.npz',origins=o,capacity=result['capacity'],peak=f['peak'],pinball=scores.pinball)
    guard(stage='D2_cell_complete');record=dict(source=s,horizon=h,window=w,native_unit=cfg['native_unit'],post_result=True,exploratory=True,source_sha256=cfg['sha256'],one_based_rank=result['refits'][0]['one_based_rank'],refit_count=len(result['refits']),evaluation=summary,comparisons=paired,resources=guard.resources)
    dump(OUT/f'{s}-h{h}-w{w}.json',record);signal.setitimer(signal.ITIMER_REAL,0);print(json.dumps(record,ensure_ascii=False,allow_nan=False))

def simulation():
    guard,p=guard_for('simulation');rows=[];n=100000;batch=5000
    for h in (6,24):
        for phi in (0.,.7,.85,.98):
            seed=20261023+1000*h+round(100*phi);rng=np.random.default_rng(seed);q=np.sqrt(gaussian_endpoint_variance(h,phi))*NormalDist().inv_cdf(.9875);peak_count=end_count=0
            for start in range(0,n,batch):
                z=rng.standard_normal((min(batch,n-start),h));inc=z.copy()
                for j in range(1,h):inc[:,j]=phi*inc[:,j-1]+np.sqrt(1-phi**2)*z[:,j]
                partial=np.cumsum(inc,axis=1);peak_count+=int(np.sum(np.max(np.abs(partial),axis=1)>q));end_count+=int(np.sum(np.abs(partial[:,-1])>q))
            peak=peak_count/n;end=end_count/n;row=dict(horizon=h,phi=phi,seed=seed,paths=n,stationary_increment_variance=1,oracle_abs_endpoint_quantile=q,endpoint_variance=gaussian_endpoint_variance(h,phi),max_exceedances=peak_count,endpoint_exceedances=end_count,max_exceedance_rate=peak,endpoint_exceedance_rate=end,rate_minus_point05=peak-.05,monte_carlo_standard_error=float(np.sqrt(peak*(1-peak)/n)),max_rate_minus_two_endpoint_rate=peak-2*end,independence_premise=bool(phi==0),post_result=True,exploratory=True);rows.append(row);guard(stage='D2_simulation_cell')
    guard(stage='D2_simulation_complete');dump(OUT/'simulation.json',dict(design='oracle endpoint quantile; x=0; independent stationary AR paths, not an empirical calibration experiment',results=rows,resources=guard.resources));signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps(dict(results=rows,resources=guard.resources),ensure_ascii=False,allow_nan=False))

def aggregate():
    cells=[json.loads((OUT/f'{s}-h{h}-w{w}.json').read_text()) for s,ws in [('fx_hourly',[720,2880]),('nyfed_weekly',[52,260])] for h in [6,24] for w in ws];pairs=[r for cell in cells for r in cell['comparisons']];assert len(pairs)==16
    inputs=[r['dm_p'] if r['status']=='OK' else (1. if r['status']=='IDENTICAL_LOSSES' else None) for r in pairs]
    adjusted=holm(inputs) if all(x is not None for x in inputs) else [None]*len(inputs)
    for r,p in zip(pairs,adjusted):r.update(separate_family_size=16,holm_p=None if p is None else float(p),holm_status='working-reference separate family' if p is not None else 'incomplete component test family')
    def csvout(name,rows):
        b=io.StringIO(newline='');keys=list(dict.fromkeys(k for r in rows for k in r));w=csv.DictWriter(b,keys);w.writeheader();w.writerows(rows);write(OUT/name,b.getvalue())
    summary=[{k:c[k] for k in ('source','horizon','window','native_unit','one_based_rank','refit_count','post_result','exploratory')}|c['evaluation'] for c in cells];csvout('summary.csv',summary);csvout('paired-tests.csv',pairs);print(json.dumps(dict(cells=summary,comparisons=pairs),ensure_ascii=False,allow_nan=False))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--mode',choices=['cell','simulation','aggregate'],required=True);a.add_argument('--source',choices=['fx_hourly','nyfed_weekly']);a.add_argument('--horizon',type=int);a.add_argument('--window',type=int);v=a.parse_args()
    if v.mode=='simulation':simulation()
    elif v.mode=='aggregate':aggregate()
    else:cell(v.source,v.horizon,v.window)
