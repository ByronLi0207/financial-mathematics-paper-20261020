"""Single-worker retrospective FX curve, with exact old W2880 gate first."""
from __future__ import annotations
import argparse,datetime as dt,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DESIGN_COMMIT='b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a'
PROTOCOL=('protocol/revision-v9/wp3-learning-curve.md','protocol/revision-v9/wp3-learning-curve.json')
FORMAL=ROOT/'.scratch/revision-v9/wp3-run';PRIVATE=ROOT/'.scratch/revision-v9/wp3-private'
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')
CODE=('run_v9_learning_curve.py','v9_learning_curve.py','run_conditional_study.py','v3_revision.py','run_v8_wp3.py','run_study.py')
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def read(p):return json.loads(Path(p).read_text())
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def record_candidate(public,method,index,candidate,diagnostics):
 save(Path(public)/(method+'-candidate-'+str(index)+'.json'),dict(candidate=candidate,fit_diagnostics=list(diagnostics)))
def record_selection(public,method,penalty,selection):
 save(Path(public)/(method+'-selection.json'),dict(selected_penalty=penalty,selection=selection))
def input_seals(d):
 inputs={d['raw']['path']:d['raw']['sha256'],'notes/revision-v9/wp1-breakeven.json':d['wp1_readout_sha256'],'notes/revision-v9/wp3-source-preflight.json':d['source_preflight_sha256']}
 for row in [*d['legacy_public'],*d['legacy_private']]:inputs[row['path']]=row['sha256']
 for row in d['legacy_QR4']:
  for kind in ('public','private'):inputs[row[kind]['path']]=row[kind]['sha256']
 return inputs

def verify_design():
 subprocess.run(['git','merge-base','--is-ancestor',DESIGN_COMMIT,'HEAD'],cwd=ROOT,check=True)
 for p in PROTOCOL:
  if subprocess.check_output(['git','show',DESIGN_COMMIT+':'+p],cwd=ROOT)!=(ROOT/p).read_bytes():raise ValueError('committed design MISMATCH')
 d=read(ROOT/PROTOCOL[1])
 for p,sha in {**d['source_code_sha256'],**input_seals(d)}.items():
  if digest(ROOT/p)!=sha:raise ValueError('original input/source MISMATCH '+p)
 return d

def verify_seal(m):
 for p,sha in m['sealed_files'].items():
  if digest(ROOT/p)!=sha:raise ValueError('run seal MISMATCH '+p)

def store_npz(path,arrays):
 import numpy as np
 with Path(path).open('xb') as f:np.savez(f,**arrays)

def legacy_block(source,forecast,cache,h,phase,method,parameter):
 from run_conditional_study import _summaries,_origin_identity
 block=dict(summary_rows=[],year_rows=[],nonoverlap_rows=[],fit_diagnostics=[],origin_identity=_origin_identity(forecast.origins))
 _summaries(block,method,parameter,source,forecast,cache.peak,h,int(forecast.origins[0]),phase)
 if method=='QR':block['fit_diagnostics']=[dict(method='QR',parameter=parameter,**row) for row in forecast.fit_diagnostics]
 return block

def old_phase(d,h,phase):
 return next(row for row in d['legacy_public'] if row['horizon']==h and row['phase']==phase)
def old_private(d,h,phase):
 return next(row for row in d['legacy_private'] if row['horizon']==h and row['phase']==phase)

def exact_phase_gate(d,h,phase,block,arrays,method):
 import numpy as np
 from v9_learning_curve import exact_tree,exact_arrays
 info=old_phase(d,h,phase);old=read(ROOT/info['path'])['result']
 keys=('summary_rows','year_rows','nonoverlap_rows','fit_diagnostics','origin_identity')
 expected={k:old[k] for k in keys};actual={k:block[k] for k in keys}
 if method=='F':
  for k in ('summary_rows','year_rows','nonoverlap_rows'):expected[k]=[x for x in expected[k] if x['method']=='frozen_F']
  expected['fit_diagnostics']=[];actual['fit_diagnostics']=[]
 if phase=='validation':
  expected.update(candidate_rows=old['candidate_rows'],selection=old['selection']);actual.update(candidate_rows=block['candidate_rows'],selection=block['selection'])
 elif method=='QR33':expected['selection']=old['selection'];actual['selection']=block['selection']
 scalar_count=exact_tree(actual,expected)
 filename=old_private(d,h,phase)['path']
 with np.load(ROOT/filename,allow_pickle=False) as z:
  names=[k for k in z.files if k.startswith('frozen_F_')] if method=='F' else list(z.files)
  array_receipt=exact_arrays(arrays,{k:z[k] for k in names})
 return dict(status='PASS',phase=phase,method=method,horizon=h,legacy_public=info['path'],legacy_private=filename,science_scalars_checked=scalar_count,**array_receipt)

def worker(args):
 from run_v8_wp3 import ResourceCheckpoint,DriverStop
 from run_study import RunGuard,StudyStop,arm_hard_deadline
 m=read(args.manifest);verify_seal(m);d=m['design'];h,w=args.worker
 name=f'W{w}_H{h}';public=FORMAL/'units'/name;private=PRIVATE/name
 start=time.monotonic();started=now();deadline=m['deadline_monotonic']
 arm_hard_deadline(min(600,deadline-start));guard=RunGuard(start,started,name,public,private);checkpoint=ResourceCheckpoint(guard,deadline,private/'ps-snapshots.jsonl')
 receipt=dict(horizon=h,window=w,started_utc=started,status='FAILED',reason=None,baseline_checks=[],method_statuses={},resources=None,technical_error=False)
 try:
  checkpoint(stage='initialization')
  import numpy as np
  from conditional_sources import load_source
  from conditional_features import build_features
  from conditional_study import StudyConfig,ConditionalForecast,conditional_forecast,score_predictions,summarize_scores,select_parameter
  from conditional_quantile import QuantileFitError
  from study_core import build_label_cache
  from parsimonious_v3 import features4,forecast as forecast4
  from run_conditional_study import _retain,_failure
  from v8_mechanism_mc import forecast_report
  from v9_learning_curve import BaselineMismatch,exact_tree,exact_arrays,dm_hac_only
  cfg=d['clock'];data=load_source(ROOT/d['raw']['path'],'fx_hourly',expected_sha256=d['raw']['sha256'],expected_bytes=d['raw']['bytes'])
  x,times=data.position,data.dates;features=build_features(x,times,short_scale=cfg['short_scale'],long_scale=cfg['long_scale'],nominal_gap_seconds=cfg['nominal_gap_seconds'])
  feature4,valid4=features4(x,times,cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds']);cache=build_label_cache(x,h)
  ids={phase:np.arange(cfg[phase+'_origin_first'],cfg[phase+'_origin_last']+1,dtype=np.int64) for phase in ('validation','evaluation')}
  if len(x)!=d['raw']['record_count']:raise ValueError('source count')
  # Every pool is still checked by the original functions; this checks whole-case eligibility.
  earliest={phase:int(axis[0])-h-w+1 for phase,axis in ids.items()}
  if min(earliest.values())<features.valid_from:raise ValueError('INSUFFICIENT_MATURE_HISTORY')
  guard.arrays(x,times,features,feature4,cache);checkpoint(stage='source')
  config=StudyConfig(h,w,cfg['refit_step'],cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds'])
  resultF=forecast_report(x,times,features,cache,ids['evaluation'],h,w,cfg['refit_step'],'F',checkpoint=checkpoint)
  f=ConditionalForecast(ids['evaluation'],resultF['capacity'],np.abs(x[ids['evaluation']]),resultF['refit_indices'],tuple(resultF['fit_diagnostics']),'F',None)
  farrays={};_retain(farrays,'frozen_F',f,cache.peak);store_npz(private/'F-evaluation.npz',farrays)
  fscore=score_predictions(cache.peak[f.origins],f.capacities,f.floors,f.origins);fsummary=summarize_scores(fscore)
  fblock=legacy_block(data,f,cache,h,'evaluation','frozen_F',None) if w==2880 else None
  if w==2880:receipt['baseline_checks'].append(exact_phase_gate(d,h,'references',fblock,farrays,'F'))
  save(public/'F.json',dict(status='COMPLETE',selected_penalty=None,evaluation=fsummary,fit_diagnostics=list(f.fit_diagnostics),trace_sha256=digest(private/'F-evaluation.npz')));receipt['method_statuses']['F']='COMPLETE'
  contrasts=[]
  for method in ('QR33','QR4'):
   candidates=[];validation_arrays={};validation_blocks=[];last_diagnostics=[]
   for index,penalty in enumerate(d['menus'][method]):
    checkpoint(stage='validation_candidate')
    candidate_diagnostics=[]
    try:
     if method=='QR33':pred=conditional_forecast(x,times,ids['validation'],config,'QR',penalty,checkpoint=checkpoint)
     else:
      cap,diag=forecast4(x,feature4,valid4,cache,ids['validation'],h,w,cfg['refit_step'],penalty,checkpoint)
      refs=ids['validation'][0]+cfg['refit_step']*((ids['validation']-ids['validation'][0])//cfg['refit_step'])
      pred=ConditionalForecast(ids['validation'],cap,np.abs(x[ids['validation']]),refs,tuple(diag),'QR4',penalty)
     scores=score_predictions(cache.peak[pred.origins],pred.capacities,pred.floors,pred.origins);summary=summarize_scores(scores)
     candidate_diagnostics=list(pred.fit_diagnostics)
     _retain(validation_arrays,'candidate_'+str(index),pred,cache.peak)
     if method=='QR33':
      candidates.append(dict(parameter=penalty,status='COMPLETE',origin_count=len(pred.origins),mean_pinball=summary['mean_pinball'],failure=None))
      if w==2880:validation_blocks.append(legacy_block(data,pred,cache,h,'validation','QR',penalty))
     else:candidates.append(dict(penalty=penalty,status='COMPLETE',mean_pinball=summary['mean_pinball']))
    except QuantileFitError as error:
     partial=getattr(error,'partial_forecast',None)
     if partial is not None:
      _retain(validation_arrays,'candidate_'+str(index)+'_partial',partial,cache.peak)
      candidate_diagnostics=list(partial.fit_diagnostics)
     else:candidate_diagnostics=list(getattr(error,'diagnostics',()))
     if method=='QR33':candidates.append(dict(parameter=penalty,status='FAILED',origin_count=0,mean_pinball=None,failure=_failure(error)))
     else:candidates.append(dict(penalty=penalty,status='FAILED',mean_pinball=None,reason=error.code,failure=_failure(error)))
    record_candidate(public,method,index,candidates[-1],candidate_diagnostics)
    prefix='candidate_'+str(index)+'_'
    store_npz(private/(method+'-validation-candidate-'+str(index)+'.npz'),{k:v for k,v in validation_arrays.items() if k.startswith(prefix)})
   store_npz(private/(method+'-validation.npz'),validation_arrays)
   if method=='QR33':
    selected=select_parameter(candidates,d['menus'][method],expected_count=len(ids['validation']));penalty=selected.get('parameter')
    record_selection(public,method,penalty,selected)
    if w==2880:
     combined=dict(summary_rows=[],year_rows=[],nonoverlap_rows=[],fit_diagnostics=[],origin_identity=validation_blocks[0]['origin_identity'] if validation_blocks else {})
     for b in validation_blocks:
      for key in ('summary_rows','year_rows','nonoverlap_rows','fit_diagnostics'):combined[key].extend(b[key])
     combined.update(candidate_rows=candidates,selection={k:v for k,v in selected.items() if k!='failed_candidates'})
     receipt['baseline_checks'].append(exact_phase_gate(d,h,'validation',combined,validation_arrays,'QR33'))
   else:
    eligible=[r for r in candidates if r['status']=='COMPLETE'];penalty=min(eligible,key=lambda r:r['mean_pinball'])['penalty'] if eligible else None
    record_selection(public,method,penalty,dict(status='SELECTED' if eligible else 'INELIGIBLE',eligible_count=len(eligible)))
   report=dict(status='INELIGIBLE' if penalty is None else 'FAILED',method=method,selected_penalty=penalty,candidates=candidates,evaluation=None,fit_diagnostics=[])
   if penalty is not None:
    try:
     if method=='QR33':pred=conditional_forecast(x,times,ids['evaluation'],config,'QR',penalty,checkpoint=checkpoint)
     else:
      cap,diag=forecast4(x,feature4,valid4,cache,ids['evaluation'],h,w,cfg['refit_step'],penalty,checkpoint)
      refs=ids['evaluation'][0]+cfg['refit_step']*((ids['evaluation']-ids['evaluation'][0])//cfg['refit_step'])
      pred=ConditionalForecast(ids['evaluation'],cap,np.abs(x[ids['evaluation']]),refs,tuple(diag),'QR4',penalty)
     scores=score_predictions(cache.peak[pred.origins],pred.capacities,pred.floors,pred.origins);summary=summarize_scores(scores)
     arrays={};_retain(arrays,'QR' if method=='QR33' else 'QR4',pred,cache.peak);store_npz(private/(method+'-evaluation.npz'),arrays)
     report.update(status='COMPLETE',evaluation=summary,fit_diagnostics=list(pred.fit_diagnostics),trace_sha256=digest(private/(method+'-evaluation.npz')))
     save(public/(method+'-evaluation-before-gate.json'),report)
     if w==2880:
      if method=='QR33':
       b=legacy_block(data,pred,cache,h,'evaluation','QR',penalty);b['selection']=dict(status='SELECTED',parameter=penalty)
       receipt['baseline_checks'].append(exact_phase_gate(d,h,'evaluation',b,arrays,'QR33'))
      else:
       oldinfo=next(i for i in d['legacy_QR4'] if i['horizon']==h);old=read(ROOT/oldinfo['public']['path'])
       scalar_count=exact_tree(dict(status=report['status'],selected_penalty=penalty,candidates=candidates,evaluation=summary,fit_diagnostics=list(pred.fit_diagnostics)),{k:old[k] for k in ('status','selected_penalty','candidates','evaluation','fit_diagnostics')})
       with np.load(ROOT/oldinfo['private']['path'],allow_pickle=False) as z:checked=exact_arrays({k.removeprefix('QR4_'):v for k,v in arrays.items()},{k:z[k] for k in z.files})
       receipt['baseline_checks'].append(dict(status='PASS',method='QR4',horizon=h,science_scalars_checked=scalar_count,**checked,scope='old four evaluation vectors and public scalars; absent old validation/floor/refit vectors not claimed'))
     difference=scores.pinball-fscore.pinball;dm=dm_hac_only(difference,h)
     delta=100*(summary['mean_pinball']-fsummary['mean_pinball'])/fsummary['mean_pinball'] if fsummary['mean_pinball']>0 else None
     contrasts.append(dict(horizon=h,window=w,method=method,status='COMPLETE',relative_loss_percent=delta,mean_model_loss=summary['mean_pinball'],mean_reference_loss=fsummary['mean_pinball'],model_breaches=summary['strict_breach_count'],reference_breaches=fsummary['strict_breach_count'],n=len(pred.origins),dm=dm))
    except QuantileFitError as error:
     partial=getattr(error,'partial_forecast',None)
     if partial is not None:
      partial_arrays={};_retain(partial_arrays,method+'_partial',partial,cache.peak);store_npz(private/(method+'-partial-evaluation.npz'),partial_arrays)
     report.update(status='EVALUATION_FAILED',reason=error.code,failure=_failure(error))
   if report['status']!='COMPLETE':
    save(public/(method+'-incomplete-before-gate.json'),report)
    if w==2880:raise BaselineMismatch('legacy complete procedure now incomplete '+method)
    contrasts.append(dict(horizon=h,window=w,method=method,status=report['status'],relative_loss_percent=None,mean_model_loss=None,mean_reference_loss=fsummary['mean_pinball'],model_breaches=None,reference_breaches=fsummary['strict_breach_count'],n=0,dm=None))
   save(public/(method+'.json'),report);receipt['method_statuses'][method]=report['status'];checkpoint(stage='method_end')
  save(public/'contrasts.json',contrasts);receipt['status']='COMPLETE'
 except BaselineMismatch as error:receipt.update(status='BLOCKED',reason=str(error))
 except (DriverStop,StudyStop) as error:receipt.update(reason=error.code)
 except Exception as error:receipt.update(reason=type(error).__name__+':'+str(error),technical_error=True)
 finally:
  try:checkpoint(stage='finalization')
  except (DriverStop,StudyStop) as error:receipt.update(status='FAILED',reason=error.code)
  try:verify_seal(m)
  except Exception as error:receipt.update(status='FAILED',reason=str(error),technical_error=True)
  receipt.update(ended_utc=now(),elapsed_seconds=time.monotonic()-start,resources=guard.resources)
  save(public/'worker-receipt.json',receipt);signal.setitimer(signal.ITIMER_REAL,0)
 return 0 if receipt['status']=='COMPLETE' else (3 if receipt['status']=='BLOCKED' else 2)

def run():
 from run_v8_wp3 import wait_owned_worker,kill_owned_worker,software_environment
 d=verify_design();FORMAL.mkdir(parents=True,exist_ok=False);PRIVATE.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();remaining=(dt.datetime.fromisoformat(d['resources']['original_window_end_utc'].replace('Z','+00:00'))-dt.datetime.now(dt.timezone.utc)).total_seconds();deadline=start+min(3600,remaining)
 m=dict(schema=1,design_commit=DESIGN_COMMIT,design=d,started_utc=now(),deadline_monotonic=deadline,environment=software_environment(),sealed_files={**input_seals(d),**d['source_code_sha256'],**{p:digest(ROOT/p) for p in (*CODE,*PROTOCOL)}},no_new_forecast_before_manifest=True)
 save(FORMAL/'manifest.json',m);active=None;status='COMPLETE';reason=None;completed=[]
 try:
  for h,w in d['run_order']:
   if time.monotonic()>=deadline:status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
   verify_seal(m);name=f'W{w}_H{h}';public=FORMAL/'units'/name;private=PRIVATE/name;public.mkdir(parents=True);private.mkdir(parents=True)
   save(public/'parent-start.json',dict(horizon=h,window=w,started_utc=now()))
   command=[sys.executable,str(ROOT/'run_v9_learning_curve.py'),'--worker',str(h),str(w),'--manifest',str(FORMAL/'manifest.json')]
   env=dict(os.environ,**{key:'1' for key in THREADS},PYTHONDONTWRITEBYTECODE='1')
   with (public/'process.log').open('x') as stream:
    active=subprocess.Popen(command,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True);terminal=wait_owned_worker(active,deadline,hard_seconds=600);active=None
   save(public/'parent-termination.json',dict(ended_utc=now(),**terminal));path=public/'worker-receipt.json'
   receipt=read(path) if path.exists() else dict(status='FAILED',reason='MISSING_WORKER_RECEIPT')
   with (FORMAL/'progress.jsonl').open('a') as f:f.write(json.dumps(dict(actual_utc=now(),horizon=h,window=w,status=receipt['status'],completed_units=len(completed)+(receipt['status']=='COMPLETE')))+'\n')
   if receipt['status']!='COMPLETE':status='BLOCKED';reason=receipt['reason'];break
   completed.append([h,w])
 except BaseException as error:status='BLOCKED';reason=type(error).__name__+':'+str(error)
 finally:
  if active is not None:kill_owned_worker(active)
  save(FORMAL/'study-termination.json',dict(status=status,reason=reason,completed_units=completed,ended_utc=now(),elapsed_seconds=time.monotonic()-start,all_workers_terminated=True))
 print(json.dumps(dict(status=status,reason=reason,completed_units=len(completed))));return 0 if status=='COMPLETE' else 1

def summarize():
 from v9_learning_curve import classify_curve
 import csv
 m=read(FORMAL/'manifest.json');verify_seal(m);d=m['design'];rows=[]
 for h,w in d['run_order']:
  p=FORMAL/'units'/f'W{w}_H{h}'/'contrasts.json'
  if p.exists():rows.extend(read(p))
  else:
   for method in ('QR33','QR4'):rows.append(dict(horizon=h,window=w,method=method,status='NOT_ATTEMPTED',relative_loss_percent=None,mean_model_loss=None,mean_reference_loss=None,model_breaches=None,reference_breaches=None,n=0,dm=None))
 curves=[]
 for band in d['prediction_ranges']:
  cells=sorted([r for r in rows if r['horizon']==band['horizon'] and r['method']==band['method']],key=lambda r:r['window'])
  curves.append(dict(horizon=band['horizon'],method=band['method'],**classify_curve([r['window'] for r in cells],[r['relative_loss_percent'] for r in cells],band['lower'],band['upper'])))
 save(FORMAL/'contrasts.json',rows);save(FORMAL/'curve-predictions.json',curves)
 flat=[]
 for row in rows:
  record={k:v for k,v in row.items() if k!='dm'}
  for k,v in (row['dm'] or {}).items():record['dm_'+k]=v
  flat.append(record)
 fields=list(dict.fromkeys(k for r in flat for k in r))
 with (FORMAL/'contrasts.csv').open('x',newline='') as f:writer=csv.DictWriter(f,fields);writer.writeheader();writer.writerows(flat)
 print(json.dumps(curves,indent=2));return 0

def main():
 p=argparse.ArgumentParser();p.add_argument('--run',action='store_true');p.add_argument('--summarize',action='store_true');p.add_argument('--worker',nargs=2,type=int);p.add_argument('--manifest',type=Path);a=p.parse_args()
 if sum([a.run,a.summarize,a.worker is not None])!=1:p.error('one action required')
 return worker(a) if a.worker is not None else run() if a.run else summarize()
if __name__=='__main__':raise SystemExit(main())
