"""Predeclared twelve-series Treasury panel; strict menus, immutable originals."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import argparse,csv,io,json,hashlib,signal,time
from datetime import datetime,timezone
from uuid import uuid4
import numpy as np
from v3_revision import ROOT,RESULT,dump,write
from round2_panel_sources import align_source
from conditional_study import StudyConfig,conditional_forecast,score_predictions,summarize_scores,select_parameter
from conditional_quantile import QuantileFitError
from parsimonious_v3 import forecast,features4
from empirical_headroom import predict as historical
from round2_levy import predict as levy
from study_core import build_label_cache
from run_study import RunGuard
OUT=RESULT/'round2/panel'

def segment(x,dates,origins,h,w,method,lam,guard):
    if method=='QR33':
        config=StudyConfig(h,w,13,6,26,604800);p=conditional_forecast(x,dates,origins,config,'QR',lam,checkpoint=guard);return p.capacities,list(p.fit_diagnostics)
    if method=='C2_QR4':
        f,valid=features4(x,dates,6,26,604800);return forecast(x,f,valid,build_label_cache(x,h),origins,h,w,13,lam,guard)
    raise ValueError('unknown method')

def cell(key,h,w):
    manifest=json.loads((OUT/'selection-manifest.json').read_text());assert key in manifest['eligible'];source=next(r for r in manifest['series'] if r['series_key']==key)
    raw=(ROOT/source['local_raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==source['sha256'];grid=[r['As Of Date'] for r in csv.DictReader((ROOT/'data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv').open())];x,_=align_source(raw,key,grid);dates=np.array(grid,dtype='datetime64[D]');cache=build_label_cache(x,h)
    started=time.monotonic();p=ROOT/'.scratch/round2/panel-models'/f'{key}-h{h}-w{w}'
    if p.exists():p=p.with_name(p.name+'-retry-'+uuid4().hex[:8])
    p.mkdir(parents=True,exist_ok=False);out=OUT/'cells';out.mkdir(parents=True,exist_ok=True);guard=RunGuard(started,datetime.now(timezone.utc).isoformat(),p,out,p)
    def alarm(*_):raise TimeoutError('D3 ten-minute worker limit')
    signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,590)
    val=np.arange(329,381,dtype=np.int64);ev=np.arange(405,682,dtype=np.int64);floors=np.abs(x[ev]);all_caps={};records=[]
    for method,caps in [('frozen_F',historical(x,ev,h,w,13)['F']),('Levy_L',levy(x,ev,h,w,13,checkpoint=guard)['capacity'])]:
        all_caps[method]=caps;records.append(dict(method=method,status='COMPLETE',selected_penalty=None,**summarize_scores(score_predictions(cache.peak[ev],caps,floors,ev))))
    for method,menu in [('QR33',[.001,.01,.1]),('C2_QR4',[.001,.01,.1,1.,10.])]:
        candidates=[]
        for lam in menu:
            try:
                caps,diag=segment(x,dates,val,h,w,method,lam,guard);summary=summarize_scores(score_predictions(cache.peak[val],caps,np.abs(x[val]),val));candidates.append(dict(parameter=lam,status='COMPLETE',**summary))
            except QuantileFitError as e:candidates.append(dict(parameter=lam,status='FAILED',reason=e.code))
        choice=select_parameter(candidates,menu,expected_count=len(val));record=dict(method=method,status='VALIDATION_INELIGIBLE',selected_penalty=choice['parameter'],selection=choice,candidates=candidates)
        if choice['status']=='SELECTED':
            try:
                caps,diag=segment(x,dates,ev,h,w,method,choice['parameter'],guard);record.update(status='COMPLETE',fit_diagnostics=diag,**summarize_scores(score_predictions(cache.peak[ev],caps,floors,ev)));all_caps[method]=caps
            except QuantileFitError as e:record.update(status='EVALUATION_FAILED',reason=e.code)
        records.append(record);guard(stage='panel_method_complete')
    f=next(r for r in records if r['method']=='frozen_F')
    for r in records:
        if r['status']=='COMPLETE':r.update(percent_vs_frozen_F=100*(r['mean_pinball']-f['mean_pinball'])/f['mean_pinball'] if f['mean_pinball'] else None,breaches_frozen_F=f['strict_breach_count'])
    np.savez(p/'numeric-traces.npz',origins=ev,peak=cache.peak[ev],floor=floors,**all_caps);guard(stage='panel_cell_complete')
    result=dict(series_key=key,horizon=h,window=w,post_result=True,exploratory=True,native_unit='USD millions',source_sha256=source['sha256'],selection_manifest_sha256=hashlib.sha256((OUT/'selection-manifest.json').read_bytes()).hexdigest(),validation_origins=[329,380],evaluation_origins=[405,681],records=records,resources=guard.resources)
    dump(out/f'{key}-h{h}-w{w}.json',result);signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}|dict(records=[{k:v for k,v in r.items() if k not in ('candidates','fit_diagnostics')} for r in records]),ensure_ascii=False,allow_nan=False))

def aggregate():
    manifest=json.loads((OUT/'selection-manifest.json').read_text());rows=[]
    for key in manifest['eligible']:
        for h in (6,24):
            for w in (52,260):
                r=json.loads((OUT/'cells'/f'{key}-h{h}-w{w}.json').read_text())
                for a in r['records']:rows.append({k:r[k] for k in ('series_key','horizon','window','post_result','exploratory')}|{k:v for k,v in a.items() if k not in ('candidates','fit_diagnostics','selection')})
    b=io.StringIO(newline='');keys=list(dict.fromkeys(k for r in rows for k in r));wr=csv.DictWriter(b,keys);wr.writeheader();wr.writerows(rows);write(OUT/'summary.csv',b.getvalue());print(b.getvalue())

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--series');p.add_argument('--horizon',type=int);p.add_argument('--window',type=int);p.add_argument('--aggregate',action='store_true');a=p.parse_args();aggregate() if a.aggregate else cell(a.series,a.horizon,a.window)
