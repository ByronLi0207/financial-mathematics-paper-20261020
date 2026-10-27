"""Bounded serial D1 workers; archived forecasts are read-only references."""
import os
for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[n]='1'
import argparse,csv,hashlib,io,json,math,signal,time,traceback
from datetime import datetime,timezone
from pathlib import Path
import importlib.metadata as metadata
import numpy as np
from v3_revision import ROOT,RESULT,write,dump
from conditional_sources import load_source
from conditional_study import StudyConfig,score_predictions,summarize_scores
from run_study import RunGuard
from inference_tests import dm_test,holm
OUT=RESULT/'round2/baselines'
METHODS=('FHS','PEAK_POT','QRF')

def identity(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(name,rows):
    f=io.StringIO(newline='');keys=list(dict.fromkeys(k for row in rows for k in row));w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows);write(OUT/name,f.getvalue())

def sanitize_diagnostics(value):
    """Preserve nonfinite diagnostic failures explicitly, never as fitted numbers."""
    events=[]
    def visit(x,path):
        if isinstance(x,(float,np.floating)) and not math.isfinite(float(x)):
            events.append(dict(path=path,original_nonfinite_token=repr(float(x)),conversion='null, not a numeric estimate'))
            return None
        if isinstance(x,dict):return {k:visit(v,path+'.'+k if path else k) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [visit(v,path+'['+str(i)+']') for i,v in enumerate(x)]
        return x
    return visit(value,''),events

def resource_checkpoint(guard):
    def check(*,stage=None,completed_origins=None,refit_index=None):
        # refit_index is algorithm diagnostics, not an accepted RunGuard key.
        guard(stage=stage,completed_origins=completed_origins)
    return check

def comparison_row(source,h,w,method,ref,loss,reference):
    diff=loss-reference['pinball'];dm=dm_test(diff,h);double=dm_test(diff,h,min(len(diff)-1,2*dm['bandwidth']))
    return dict(source=source,window=w,left_method=method,right_method=ref,contrast_id=f'{source}-h{h}-w{w}-{method}-minus-{ref}',post_result=True,exploratory=True,relative_loss_percent=100*(float(loss.mean())-float(reference['pinball'].mean()))/float(reference['pinball'].mean()),reference_strict_breaches=int(np.sum(reference['peak']>reference['capacity'])),**dm,double_bandwidth=double['bandwidth'],double_dm_t=double['dm_t'],double_dm_p=double['dm_p'],double_hln_p=double['hln_p'])

def cell(source,h,w,method):
    target=OUT/f'{source}-h{h}-w{w}-{method}.json'
    if target.exists():raise RuntimeError('D1 cell already has retained outcome: no automatic rerun')
    private=ROOT/'.scratch/round2/baselines'/f'{source}-h{h}-w{w}-{method}'
    private.mkdir(parents=True,exist_ok=False);OUT.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();guard=RunGuard(start,datetime.now(timezone.utc).isoformat(),private,OUT,private)
    def alarm(*_):raise TimeoutError('D1 hard deadline590seconds')
    signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,590)
    record=dict(source=source,horizon=h,window=w,method=method,native_unit=None,source_sha256=None,expected_origin_count=None,post_result=True,exploratory=True,private_trace=str((private/'numeric-traces.npz').relative_to(ROOT)))
    o=np.array([],dtype=np.int64)
    try:
        spec=json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_text());cfg=spec['sources'][source]
        record.update(native_unit=cfg['native_unit'],source_sha256=cfg['sha256'],protocol_sha256=identity(ROOT/'protocol/revision-20261023/round2-D1-mature-baselines.md'),code_sha256={n:identity(ROOT/n) for n in ('round2_baselines_run.py','round2_qrf.py','round2_filtered.py')},versions={n:metadata.version(n) for n in ('numpy','scipy','arch','scikit-learn')})
        data=load_source(ROOT/cfg['input_relative_path'],source,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
        config=StudyConfig(h,w,cfg['refit_step'],cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds'])
        from run_v3_inference import traces
        allv=traces();f=allv[source,h,w,'frozen_F'];qr=allv[source,h,w,'QR'];o=f['origins'];assert np.array_equal(o,qr['origins']);record['expected_origin_count']=len(o)
        guard(stage='D1_start')
        if method=='QRF':
            from round2_qrf import qrf_forecast
            result=qrf_forecast(data.position,data.dates,o,config,checkpoint=resource_checkpoint(guard))
        else:
            from round2_filtered import filtered_forecast
            result=filtered_forecast(data.position,data.dates,o,config,method,source_id=source,checkpoint=resource_checkpoint(guard))
        capacity=np.asarray(result['capacity']);assert capacity.shape==o.shape and np.isfinite(capacity).all()
        scores=score_predictions(f['peak'],capacity,f['floor'],o);summary=summarize_scores(scores);paired=[]
        for ref,a in [('frozen_F',f),('QR',qr)]:
            assert np.array_equal(o,a['origins']) and np.array_equal(f['peak'],a['peak'])
            paired.append(comparison_row(source,h,w,method,ref,scores.pinball,a))
        np.savez(private/'numeric-traces.npz',origins=o,capacity=capacity,peak=f['peak'],floor=f['floor'],pinball=scores.pinball,refit_indices=result['refit_indices'])
        record.update(status='COMPLETE',evaluation=summary,comparisons=paired,refits=result['refits'],refit_count=len(result['refits']))
    except Exception as exc:
        write(private/'failure-traceback.txt',traceback.format_exc())
        context=getattr(exc,'failure_context',{});partial=getattr(exc,'partial_forecast',{})
        if partial:
            cap=np.asarray(partial.get('capacity',[]));np.savez(private/'partial-traces.npz',capacity=cap,origins=o[:len(cap)])
        record.update(status='NA',failure_type=type(exc).__name__,failure_reason=str(exc),failure_context=context,completed_origin_count=len(partial.get('capacity',[])),completed_refits=partial.get('refits',[]),evaluation=None,comparisons=[])
    try:guard(stage='D1_complete_or_NA')
    except Exception as exc:
        record.update(status='NA',resource_failure_type=type(exc).__name__,resource_failure_reason=str(exc),failure_type=record.get('failure_type',type(exc).__name__),failure_reason=record.get('failure_reason',str(exc)),completed_origin_count=record.get('completed_origin_count',record.get('expected_origin_count') or 0),evaluation=None,comparisons=[])
    signal.setitimer(signal.ITIMER_REAL,0);record['resources']=guard.resources
    record['private_files']=[dict(name=p.name,bytes=p.stat().st_size,sha256=identity(p)) for p in sorted(private.iterdir()) if p.is_file()]
    clean,nonfinite=sanitize_diagnostics(record)
    if nonfinite:
        write(private/'nonfinite-diagnostics-repr.txt',repr(record)+'\n')
        clean['nonfinite_diagnostic_conversions']=nonfinite
    record=clean
    json.dumps(record,allow_nan=False)
    dump(target,record)
    print(json.dumps({k:v for k,v in record.items() if k not in ('refits','completed_refits','code_sha256','private_files')},ensure_ascii=False,allow_nan=False))

def aggregate():
    cells=[json.loads((OUT/f'{s}-h{h}-w{w}-{m}.json').read_text()) for s,ws in [('fx_hourly',(720,2880)),('nyfed_weekly',(52,260))] for h in (6,24) for w in ws for m in METHODS]
    summaries=[];pairs=[]
    for c in cells:
        common={k:c[k] for k in ('source','horizon','window','method','status','native_unit','post_result','exploratory')}
        summaries.append(common|(c['evaluation'] or dict(origin_count=None,mean_pinball=None,strict_breach_count=None))|dict(failure_reason=c.get('failure_reason'),failure_type=c.get('failure_type'),completed_origin_count=c.get('completed_origin_count',c['expected_origin_count']),refit_count=c.get('refit_count')))
        if c['status']=='COMPLETE':pairs+=c['comparisons']
        else:
            for ref in ('frozen_F','QR'):
                pairs.append(dict(source=c['source'],horizon=c['horizon'],window=c['window'],left_method=c['method'],right_method=ref,contrast_id=f"{c['source']}-h{c['horizon']}-w{c['window']}-{c['method']}-minus-{ref}",status='NA_CELL',failure_reason=c.get('failure_reason') or c.get('resource_failure_reason'),post_result=True,exploratory=True,dm_p=None,hln_p=None))
    assert len(cells)==24 and len(pairs)==48
    inputp=[r['dm_p'] if r['status']=='OK' else 1. for r in pairs];adjusted=holm(inputp)
    for r,p in zip(pairs,adjusted):r.update(separate_family_size=48,holm_p=float(p) if r['status']=='OK' else None,holm_missing_slot_policy='absent/degenerate component reserved as1 for adjustment only; displayed test remains NA')
    csvout('summary.csv',summaries);csvout('paired-tests.csv',pairs)
    complete=[r for r in summaries if r['status']=='COMPLETE']
    report=dict(planned_cells=24,complete_cells=len(complete),NA_cells=24-len(complete),method_counts={m:sum(r['method']==m for r in complete) for m in METHODS},separate_comparison_slots=48,original_primaries_unchanged=True,maximum_rss_bytes=max(c['resources']['peak_rss_bytes'] or 0 for c in cells),maximum_elapsed_seconds=max(c['resources']['elapsed_seconds'] or 0 for c in cells),maximum_os_threads=max(c['resources']['maximum_observed_os_threads'] or 0 for c in cells))
    dump(OUT/'summary.json',report);print(json.dumps(dict(summary=report,cells=summaries,comparisons=pairs),ensure_ascii=False,allow_nan=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['cell','aggregate'],required=True);p.add_argument('--source');p.add_argument('--horizon',type=int);p.add_argument('--window',type=int);p.add_argument('--method',choices=METHODS);a=p.parse_args()
    if a.mode=='aggregate':aggregate()
    else:cell(a.source,a.horizon,a.window,a.method)
