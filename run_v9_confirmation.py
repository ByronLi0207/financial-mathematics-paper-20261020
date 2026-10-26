"""Sole prospective v9 WP2 driver; one child experiment at a time."""
from __future__ import annotations
import argparse,csv,datetime as dt,hashlib,json,math,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DESIGN_COMMIT='f2ce438ccb2fcf671c849a83032ac700ac6007c6'
PROTOCOL=('protocol/revision-v9/wp2-confirmatory.md','protocol/revision-v9/wp2-confirmatory.json')
FORMAL=ROOT/'.scratch/revision-v9/wp2-run'
PRIVATE=ROOT/'.scratch/revision-v9/wp2-private'
CODE=('v9_confirmation.py','run_v9_confirmation.py','v8_mechanism_mc.py','run_v8_wp3.py','run_study.py','conditional_features.py','conditional_quantile.py','conditional_study.py','study_core.py','parsimonious_v3.py')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def save(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
def verify_design():
 subprocess.run(['git','merge-base','--is-ancestor',DESIGN_COMMIT,'HEAD'],cwd=ROOT,check=True)
 for name in PROTOCOL:
  if subprocess.check_output(['git','show',DESIGN_COMMIT+':'+name],cwd=ROOT)!=(ROOT/name).read_bytes():raise ValueError('frozen protocol MISMATCH')
 design=read(ROOT/PROTOCOL[1])
 for name,sha in design['original_modules_sha256'].items():
  if digest(ROOT/name)!=sha:raise ValueError('old source MISMATCH')
 if digest(ROOT/'notes/revision-v9/wp1-breakeven.json')!=design['wp1_readout_sha256']:raise ValueError('WP1 input MISMATCH')
 return design

def verify_seal(manifest):
 for name,sha in manifest['sealed_files'].items():
  if digest(ROOT/name)!=sha:raise ValueError('sealed code/protocol MISMATCH '+name)

def unit_name(rep,dgp,phi):return f'rep-{rep:03d}_dgp-{dgp}_phi-{phi}'
def planned_units(design):
 for rep in range(32):
  for di in range(3):
   for pi in range(2):yield rep,di,pi

def run_worker(args):
 from run_v8_wp3 import ResourceCheckpoint,evaluate_method,scalar_diagnostics,DriverStop
 from run_study import RunGuard,StudyStop,arm_hard_deadline
 manifest=read(args.manifest);verify_seal(manifest);d=manifest['design'];rep,di,pi=args.worker
 unit=unit_name(rep,di,pi);public=FORMAL/'units'/unit;private=PRIVATE/unit
 start=time.monotonic();started=now();deadline=manifest['deadline_monotonic']
 initial=read(public/'unit-start.json');windows=initial['windows']
 if any(os.environ.get(k)!='1' for k in THREADS):raise ValueError('thread environment')
 arm_hard_deadline(min(600,deadline-start));guard=RunGuard(start,started,unit,public,private)
 checkpoint=ResourceCheckpoint(guard,deadline,private/'ps-snapshots.jsonl')
 receipt=dict(rep=rep,dgp_index=di,phi_index=pi,status='FAILED',reason=None,technical_error=False,started_utc=started,window_seconds={},resources=None)
 try:
  checkpoint(stage='initialization')
  import numpy as np
  from v9_confirmation import make_process
  from v8_mechanism_mc import forecast_report
  from conditional_features import build_features
  from conditional_study import score_predictions
  from conditional_quantile import QuantileFitError
  from study_core import build_label_cache,stable_mean
  if np.__version__!='2.3.5':raise ValueError('numpy version MISMATCH')
  position,rng=make_process(rep,di,d['phi'][pi],d);save(public/'rng-receipt.json',rng)
  times=np.datetime64(d['retained_clock_first'])+np.arange(len(position))*np.timedelta64(d['gap_seconds'],'s')
  np.savez_compressed(public/'synthetic-input.npz',position=position,times=times)
  features=build_features(position,times,short_scale=d['short_rms'],long_scale=d['long_rms'],nominal_gap_seconds=d['gap_seconds'])
  if features.valid_from!=d['feature_valid_from']:raise ValueError('feature boundary')
  caches={h:build_label_cache(position,h) for h in d['horizons']};guard.arrays(position,times,features,caches)
  origins={s:np.arange(d[s+'_first'],d[s+'_last']+1,dtype=np.int64) for s in ('validation','evaluation')}
  def report(segment,h,w,method,penalty=None):
   ids=origins[segment];result=forecast_report(position,times,features,caches[h],ids,h,w,d['refit_step'],method,penalty,checkpoint=checkpoint)
   peak=caches[h].peak[ids];floor=np.abs(position[ids]);score=score_predictions(peak,result['capacity'],floor,ids)
   breaches=int(np.count_nonzero(score.strict_breach));n=len(ids)
   if segment=='evaluation':
    target=public/f'W{w}_H{h}_{method}_evaluation.npz'
    if target.exists():raise ValueError('evaluation repeated')
    np.savez_compressed(target,origins=ids,capacity=result['capacity'],peak=peak,floor=floor,refit_indices=result['refit_indices'],pinball=score.pinball,strict_breach=score.strict_breach)
   return dict(mean_loss=stable_mean(score.pinball),strict_breach_count=breaches,strict_breach_rate=breaches/n,n=n),scalar_diagnostics(result['fit_diagnostics'])
  for w in windows:
   tick=time.monotonic()
   for h in d['horizons']:
    for method in d['methods']:evaluate_method(d,public,w,h,method,report,checkpoint,QuantileFitError,(DriverStop,StudyStop))
   receipt['window_seconds'][str(w)]=time.monotonic()-tick;checkpoint(stage='cell_end')
  checkpoint(stage='finalization');receipt['status']='COMPLETE'
 except (DriverStop,StudyStop) as error:receipt.update(reason=error.code)
 except Exception as error:receipt.update(reason=type(error).__name__+':'+str(error),technical_error=True)
 finally:
  try:checkpoint(stage='finalization')
  except (DriverStop,StudyStop) as error:receipt.update(status='FAILED',reason=error.code)
  try:verify_seal(manifest)
  except Exception as error:receipt.update(status='FAILED',reason=str(error),technical_error=True)
  receipt.update(ended_utc=now(),elapsed_seconds=time.monotonic()-start,resources=guard.resources)
  save(public/'worker-receipt.json',receipt);signal.setitimer(signal.ITIMER_REAL,0)
 return 2 if receipt['technical_error'] else (0 if receipt['status']=='COMPLETE' else 1)

def run():
 from run_v8_wp3 import wait_owned_worker,kill_owned_worker,software_environment
 d=verify_design();FORMAL.mkdir(parents=True,exist_ok=False);PRIVATE.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();end_window=dt.datetime.fromisoformat(d['resources']['original_window_end_utc'].replace('Z','+00:00'))
 remaining=(end_window-dt.datetime.now(dt.timezone.utc)).total_seconds();deadline=start+min(5400,remaining)
 if remaining<=0:raise ValueError('research window ended')
 manifest=dict(schema=1,design=d,design_commit=DESIGN_COMMIT,started_utc=now(),deadline_monotonic=deadline,initial_planned_workers=192,initial_planned_selected_reports=4608,environment=software_environment(),sealed_files={name:digest(ROOT/name) for name in (*CODE,*PROTOCOL,'notes/revision-v9/wp1-breakeven.json')},no_RNG_before_manifest=True)
 save(FORMAL/'manifest.json',manifest);active=None;removed=[];status='COMPLETE';reason=None;completed=0;attempted=0;budget_done=False
 try:
  for rep,di,pi in planned_units(d):
   if time.monotonic()>=deadline:status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
   verify_seal(manifest)
   if rep==16 and not budget_done:
    from v9_confirmation import choose_reductions
    receipts=[read(p) for p in (FORMAL/'units').glob('*/worker-receipt.json')]
    if len(receipts)!=96 or any(r['status']!='COMPLETE' for r in receipts):
     status='INCOMPLETE_BEFORE_BUDGET_REVIEW';reason='FIRST16_UNIT_NOT_COMPLETE';break
    projected={w:math.fsum(r['window_seconds'].get(str(w),0.) for r in receipts) for w in d['windows']}
    overhead=max(0.,math.fsum(r['elapsed_seconds'] for r in receipts)-math.fsum(projected.values()))
    decision=choose_reductions(projected,overhead,deadline-time.monotonic());removed=decision['removed_windows'];budget_done=True
    save(FORMAL/'budget-decision.json',dict(actual_utc=now(),after_reps=list(range(16)),uses_losses=False,**decision))
    if not decision['can_continue']:status='BUDGET_STOP';reason='PROJECTED_OVERHEAD';break
   unit=unit_name(rep,di,pi);public=FORMAL/'units'/unit;private=PRIVATE/unit
   public.mkdir(parents=True);private.mkdir(parents=True)
   windows=[w for w in d['windows'] if rep<16 or w not in removed]
   save(public/'unit-start.json',dict(rep=rep,dgp_index=di,phi_index=pi,started_utc=now(),windows=windows,budget_reduced_windows=removed if rep>=16 else []))
   if not windows:continue
   env=dict(os.environ,**{k:'1' for k in THREADS},PYTHONDONTWRITEBYTECODE='1')
   command=[sys.executable,str(ROOT/'run_v9_confirmation.py'),'--worker',str(rep),str(di),str(pi),'--manifest',str(FORMAL/'manifest.json')]
   attempted+=1
   with (public/'process.log').open('x') as stream:
    active=subprocess.Popen(command,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
    terminal=wait_owned_worker(active,deadline,hard_seconds=600);active=None
   save(public/'parent-termination.json',dict(ended_utc=now(),**terminal))
   wr=public/'worker-receipt.json'
   if terminal['returncode']==2 or (wr.exists() and read(wr).get('technical_error')):
    status='TECHNICAL_ERROR';reason='WORKER_TECHNICAL_ERROR';break
   if not wr.exists() and terminal['reason']!='GLOBAL_DEADLINE':status='TECHNICAL_ERROR';reason='MISSING_WORKER_RECEIPT';break
   completed+=terminal['status']=='COMPLETE'
   with (FORMAL/'progress.jsonl').open('a') as f:f.write(json.dumps(dict(actual_utc=now(),rep=rep,dgp=di,phi=pi,status=terminal['status'],completed_units=completed,attempted_units=attempted))+'\n')
   if terminal['reason']=='GLOBAL_DEADLINE':status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
 except BaseException as error:
  status='TECHNICAL_ERROR';reason=type(error).__name__+':'+str(error)
 finally:
  if active is not None:kill_owned_worker(active)
  try:verify_seal(manifest);seal='PASS'
  except Exception as error:seal=str(error);status='TECHNICAL_ERROR';reason=seal
  save(FORMAL/'study-termination.json',dict(status=status,reason=reason,ended_utc=now(),elapsed_seconds=time.monotonic()-start,attempted_workers=attempted,completed_workers=completed,removed_windows=removed,code_seal=seal,all_workers_terminated=True))
 print(json.dumps(dict(status=status,reason=reason,attempted=attempted,completed=completed,removed_windows=removed)))
 return 0 if status=='COMPLETE' else 1

def summarize():
 from v9_confirmation import aggregate_pair,confirmation_screen
 manifest=read(FORMAL/'manifest.json');verify_seal(manifest);d=manifest['design'];term=read(FORMAL/'study-termination.json');removed=term['removed_windows']
 rows=[];summaries=[]
 for di,dgp in enumerate(d['dgp']):
  for pi,phi in enumerate(d['phi']):
   for w in d['windows']:
    planned=16 if w in removed else 32
    for h in d['horizons']:
     methods={}
     for method in d['methods']:
      records=[]
      for rep in range(planned):
       path=FORMAL/'units'/unit_name(rep,di,pi)/f'W{w}_H{h}_{method}.json'
       if path.exists():row=read(path)
       elif path.with_name(path.stem+'.started.json').exists():row=dict(status='FAILED',reason='INTERRUPTED_METHOD',evaluation=None)
       else:row=dict(status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',evaluation=None)
       if row['status']=='COMPLETE':
        e=row['evaluation']
        if e['n']!=72 or not math.isfinite(e['mean_loss']) or e['mean_loss']<0 or e['strict_breach_rate']!=e['strict_breach_count']/72:raise ValueError('invalid completed evaluation')
       record=dict(rep=rep,**row);records.append(record)
       rows.append(dict(rep=rep,dgp=dgp,phi_index=pi,window=w,horizon=h,method=method,status=row['status'],reason=row.get('reason'),source=str(path.relative_to(ROOT)),selected_penalty=row.get('selected_penalty')))
      methods[method]=records
      for rep in range(planned,32):
       path=FORMAL/'units'/unit_name(rep,di,pi)/f'W{w}_H{h}_{method}.json'
       rows.append(dict(rep=rep,dgp=dgp,phi_index=pi,window=w,horizon=h,method=method,status='BUDGET_REDUCED',reason='PREDECLARED_REMAINING_HALF_REMOVED',source=str(path.relative_to(ROOT)),selected_penalty=None))
     for method in d['methods']:
      summary=aggregate_pair(methods[method],methods['F'],planned)
      summaries.append(dict(dgp=dgp,dgp_index=di,phi=phi,phi_index=pi,window=w,horizon=h,method=method,initial_planned_repetitions=32,budget_reduced=w in removed,**summary))
 save(FORMAL/'summary.json',summaries);save(FORMAL/'inventory.json',rows)
 fields=sorted({key for row in summaries for key in row})
 with (FORMAL/'summary.csv').open('x',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(summaries)
 screen=confirmation_screen(summaries,d);save(FORMAL/'support.json',screen)
 print(json.dumps(screen,indent=2,allow_nan=False));return 0

def main():
 p=argparse.ArgumentParser();p.add_argument('--run',action='store_true');p.add_argument('--summarize',action='store_true');p.add_argument('--worker',nargs=3,type=int);p.add_argument('--manifest',type=Path);args=p.parse_args()
 if sum([args.run,args.summarize,args.worker is not None])!=1:p.error('one action required')
 return run_worker(args) if args.worker is not None else (run() if args.run else summarize())
if __name__=='__main__':raise SystemExit(main())
