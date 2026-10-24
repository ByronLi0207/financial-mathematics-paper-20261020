"""Registered v9 study driver; source I/O is confined to explicit worker commands."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from datetime import datetime,timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import zipfile

ROOT=Path(__file__).resolve().parent
PROTOCOL='protocol/v9/nonstationarity-design.md'
DESIGN_COMMIT='5decccb0a13ef1969629cfec695dd3459c412c4e'
PUBLIC=ROOT/'results/v9/nonstationarity'
PRIVATE=ROOT/'.scratch/v9/nonstationarity'
THREAD_NAMES=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')
NEW_CODE=('run_v9_nonstationarity.py','v9_nonstationarity.py','v9_switching.py','v9_exposure.py')


def utc_now():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')


def atomic_json(path,value,replace=False):
    """Make a complete receipt visible atomically, preserving immutable records."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    pending=path.with_name(path.name+'.pending')
    with pending.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    if replace:os.replace(pending,path)
    else:
        try:os.link(pending,path)
        finally:pending.unlink()


def recover_unit_outputs(public):
    """Recover immutable completed comparisons even when a worker was killed."""
    public=Path(public);records=[];errors=[]
    for path in sorted(public.glob('comparison-*.json')):
        try:records.append(load(path))
        except (OSError,ValueError):errors.append(path.name)
    progress={}
    try:
        if (public/'progress.json').exists():progress=load(public/'progress.json')
    except (OSError,ValueError):errors.append('progress.json')
    return dict(records=records,seconds_by_method=progress.get('seconds_by_method',{}),recovery_errors=errors)

def read_design():
    frozen=subprocess.check_output(['git','show',DESIGN_COMMIT+':'+PROTOCOL],cwd=ROOT)
    raw=(ROOT/PROTOCOL).read_bytes()
    if raw!=frozen:raise ValueError('DESIGN_COMMIT_MISMATCH')
    d=json.loads(re.search(r'```json\n(.*?)\n```',raw.decode(),re.S).group(1))
    for p,digest in d['forecast_source_sha256'].items():
        if sha(ROOT/p)!=digest:raise ValueError('FROZEN_FORECAST_CODE_CHANGED:'+p)
    if sha(ROOT/d['input_metadata'])!=d['input_metadata_sha256']:raise ValueError('INPUT_METADATA_CHANGED')
    return d


def prefix_before_evaluation(position,times,stop):
    import numpy as np
    x=np.array(position[:stop],dtype=float,copy=True);t=np.array(times[:stop],copy=True)
    if len(x)!=stop or len(t)!=stop or not np.isfinite(x).all():raise ValueError('INVALID_ELIGIBLE_PREFIX')
    x.flags.writeable=False;t.flags.writeable=False
    return x,t


def reduce_cell(records,repetitions):
    import numpy as np
    result=dict(status='FAILED',required_repetitions=repetitions,completed_repetitions=0,
                relative_median_pct=None,q25_pct=None,q75_pct=None,win_fraction=None,
                qr_breach_median=None,f_breach_median=None)
    records=list(records);ids=[r.get('rep') for r in records]
    valid=[r for r in records if r.get('status')=='COMPLETE' and r.get('n')==72
           and r.get('f_mean_loss') is not None and r['f_mean_loss']>0
           and r.get('qr_mean_loss') is not None and math.isfinite(r['qr_mean_loss']) and math.isfinite(r['f_mean_loss'])]
    result['completed_repetitions']=len(valid)
    result['failed_repetitions']=[r for r in range(repetitions) if not any(x.get('rep')==r for x in valid)]
    if len(records)!=repetitions or sorted(ids)!=list(range(repetitions)) or len(valid)!=repetitions:return result
    values=[100*(r['qr_mean_loss']/r['f_mean_loss']-1) for r in valid]
    if not all(math.isfinite(x) for x in values):return result
    result.update(status='COMPLETE',relative_median_pct=float(np.median(values)),q25_pct=float(np.quantile(values,.25)),
                  q75_pct=float(np.quantile(values,.75)),win_fraction=sum(r['qr_mean_loss']<r['f_mean_loss'] for r in valid)/repetitions,
                  qr_breach_median=float(np.median([r['qr_breaches']/r['n'] for r in valid])),
                  f_breach_median=float(np.median([r['f_breaches']/r['n'] for r in valid])))
    return result


def prediction_status(cells,diagnostics,source_ids):
    import numpy as np
    from statsmodels.stats.multitest import multipletests
    rows={r['source_id']:r for r in diagnostics if r.get('kind')=='weekly'}
    p=[rows.get(s,{}).get('p_value') for s in source_ids]
    known=sum(v is not None and v<=.05 for v in p);unknown=sum(v is None for v in p)
    adjusted=multipletests([1. if v is None else v for v in p],method='holm')[1]
    n1='SUPPORTED' if known>=7 else ('NOT_SUPPORTED' if known+unknown<7 else 'UNASSESSABLE')
    result={'N1':dict(status=n1,known_rejections=known,maximum_rejections=known+unknown,unknown=unknown,family_size=13,
                     holm_rejections=sum(v is not None and a<=.05 for v,a in zip(p,adjusted)),holm_p_by_source=dict(zip(source_ids,map(float,adjusted))))}
    def across(arm,w):
        selected=[]
        for s in source_ids:
            found=[x for x in cells if x['source_id']==s and x['arm']==arm and x['window']==w and x['method']=='QR33']
            if len(found)!=1 or found[0]['status']!='COMPLETE' or found[0]['relative_median_pct'] is None:return None
            selected.append(found[0]['relative_median_pct'])
        return float(np.median(selected))
    a,b,c=across('switching',52),across('switching',260),across('constant',52)
    result['N2']=dict(status='UNASSESSABLE' if a is None or b is None else ('SUPPORTED' if a>5 and b>5 else 'NOT_SUPPORTED'),switching_W52_median_pct=a,switching_W260_median_pct=b)
    result['N3']=dict(status='UNASSESSABLE' if c is None else ('SUPPORTED' if -3<=c<=3 else 'NOT_SUPPORTED'),constant_W52_median_pct=c)
    daily=next((r for r in diagnostics if r.get('kind')=='daily'),None);hourly=next((r for r in diagnostics if r.get('kind')=='hourly'),None)
    valid=daily is not None and hourly is not None and all(r.get('p_value') is not None and isinstance((r.get('partition') or {}).get('cuts'),list) for r in (daily,hourly))
    dd=len(daily['partition']['cuts'])/daily['n'] if valid else None;hd=len(hourly['partition']['cuts'])/hourly['n'] if valid else None
    result['N4']=dict(status='UNASSESSABLE' if not valid else ('SUPPORTED' if daily['p_value']<=.05 and dd>hd else 'NOT_SUPPORTED'),daily_breaks_per100=None if dd is None else 100*dd,hourly_breaks_per100=None if hd is None else 100*hd,interpretation='Observation-clock density; not causal frequency identification')
    return result


def choose_configuration(units,remaining,design):
    ladder=[(32,['QR33','QR4']),(16,['QR33','QR4']),(16,['QR33'])];projections=[]
    incomplete=any(not u.get('complete',False) for u in units)
    for R,methods in ladder:
        costs=[]
        for u in units:
            t=u.get('seconds_by_method',{})
            costs.append(float(design['worker_hard_seconds']) if not u.get('complete',False)
                         else sum(float(t.get(k,0)) for k in ['generation','F',*methods]))
        base=max(sum(costs)/design['worker_count'],max(costs,default=0))
        projected=design['projection_safety_factor']*(R/design['pilot_repetitions'])*base+design['projection_reserve_seconds']
        projections.append(dict(repetitions=R,conditional_methods=methods,predicted_seconds=projected,predicted_fits=projected<=remaining))
    chosen=next((x for x in projections if x['predicted_fits']),projections[-1]) if not incomplete else projections[-1]
    return dict(**chosen,remaining_seconds=remaining,incomplete_pilot=incomplete,projection_ladder=projections)


def source_inventory(design):
    meta=load(ROOT/design['input_metadata']);out=[]
    for row in meta['weekly_series']:out.append(dict(source_id=row['source_id'],kind='weekly',stop=405))
    out += [dict(source_id='fx_daily',kind='daily',stop=405),dict(source_id='fx_hourly',kind='hourly',stop=8109)]
    if len(out)!=15 or len({r['source_id'] for r in out})!=15:raise ValueError('SOURCE_INVENTORY')
    return out


def verified_bytes(path,expected_bytes,expected_sha256):
    p=ROOT/path
    if p.is_symlink() or not p.is_file():raise ValueError('INPUT_NOT_REGULAR')
    raw=p.read_bytes()
    if len(raw)!=expected_bytes or hashlib.sha256(raw).hexdigest()!=expected_sha256:raise ValueError('INPUT_FINGERPRINT')
    return raw


def load_prefix(source_index,design):
    import numpy as np
    from conditional_sources import load_source
    from round2_panel_sources import align_source
    from v8_daily_fx import resample_closed_days
    meta=load(ROOT/design['input_metadata']);row=source_inventory(design)[source_index]
    bill=meta['treasury_input'];treasury=load_source(ROOT/bill['path'],'nyfed_weekly',expected_sha256=bill['sha256'],expected_bytes=bill['bytes'])
    if row['kind']=='weekly':
        if source_index==0:x,t=treasury.position,treasury.dates
        else:
            route=next(r for r in meta['input_routes'] if r['source_id']==row['source_id'])
            raw=verified_bytes(route['destination'],route['expected_bytes'],route['expected_sha256'])
            x,alignment=align_source(raw,row['source_id'],[str(v.astype('datetime64[D]')) for v in treasury.dates]);t=treasury.dates
        source_hash=bill['sha256'] if source_index==0 else route['expected_sha256']
    else:
        route=next(r for r in meta['input_routes'] if r['source_id']=='fx_hourly')
        raw=verified_bytes(route['destination'],route['expected_bytes'],route['expected_sha256'])
        fx=load_source(ROOT/route['destination'],'fx_hourly',expected_sha256=route['expected_sha256'],expected_bytes=route['expected_bytes'])
        source_hash=route['expected_sha256'];x,t=fx.position,fx.dates
        if row['kind']=='daily':
            daily=resample_closed_days(x,t)
            if daily.metadata['fingerprints']['combined_sha256']!='a8638f97370b14308212cbaa2d82defaf7152e0f240ff9f950414a035ae744d1':raise ValueError('DAILY_AGGREGATION_CHANGED')
            x,t=daily.position,daily.times
    x,t=prefix_before_evaluation(x,t,row['stop'])
    info=dict(**row,n=len(x),M=len(x)-1,first_time=str(t[0]),last_time=str(t[-1]),input_sha256=source_hash,last_raw_index_used=row['stop']-1)
    return x,t,info


def verify_seal(manifest):
    read_design()
    for p,digest in manifest['code_sha256'].items():
        if sha(ROOT/p)!=digest:raise ValueError('STUDY_CODE_CHANGED:'+p)


def worker_runtime(manifest,public,private):
    from run_study import RunGuard
    from run_v8_wp3 import ResourceCheckpoint
    private.mkdir(parents=True,exist_ok=True);public.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();guard=RunGuard(start,utc_now(),'v9',public,private)
    checkpoint=ResourceCheckpoint(guard,manifest['deadline_monotonic'],private/'resource-snapshots.jsonl')
    checkpoint(stage='initialization')
    return guard,checkpoint


def diagnostic_worker(args):
    d=read_design();manifest=load(args.manifest);verify_seal(manifest)
    out=Path(args.output);guard,checkpoint=worker_runtime(manifest,out.parent,Path(args.private))
    from v9_nonstationarity import fit_ar_garch,bootstrap_stability,locate_breaks,CalibrationError
    row=dict(source_inventory(d)[args.source],source_index=args.source,status='FAILED',p_value=None,partition=None,whole_fit=None,segment_fits=[],calibration_status='FAILED',started_utc=utc_now())
    try:
        x,t,info=load_prefix(args.source,d);row.update(info);checkpoint(stage='input_verified')
        try:row['partition']=locate_breaks(x,d)
        except CalibrationError as exc:row['partition_failure']=dict(reason=exc.reason,details=exc.details)
        row['whole_fit']=fit_ar_garch(x,d)
        try:row.update(bootstrap_stability(x,row['whole_fit']['params'],args.source,d,checkpoint=checkpoint))
        except CalibrationError as exc:row.update(status='FAILED_DIAGNOSTIC',reason=exc.reason,details=exc.details)
        if row['partition'] is not None:
            row['break_dates']=[str(t[k+1]) for k in row['partition']['cuts']]
        if row['kind']=='weekly' and row['partition'] is not None:
            cuts=[0,*row['partition']['cuts'],len(x)-1]
            if len(cuts)==2:row['segment_fits']=[row['whole_fit']]
            else:
                for a,b in zip(cuts,cuts[1:]):
                    try:row['segment_fits'].append(fit_ar_garch(x,d,start=a,stop=b))
                    except CalibrationError as exc:row['segment_fits'].append(dict(status='FAILED',reason=exc.reason,details=exc.details))
            row['calibration_status']='COMPLETE' if all(f.get('params') is not None for f in row['segment_fits']) else 'FAILED_SEGMENT_FIT'
        elif row['kind']!='weekly':row['calibration_status']='NOT_A_FORECAST_SOURCE'
        checkpoint(stage='finalization')
    except Exception as exc:
        if row.get('p_value') is not None:
            diagnostic_keys=('status','statistic','p_value','exceedances','B','bootstrap_statistics',
                'moment','seed_identity','rng_initial_state','rng_final_state','monte_carlo_standard_error')
            row['completed_diagnostic_evidence']={k:row[k] for k in diagnostic_keys if k in row}
        row.update(status='FAILED',p_value=None,reason=getattr(exc,'reason',getattr(exc,'code',type(exc).__name__)),exception_type=type(exc).__name__)
    row['ended_utc']=utc_now();row['resources']=guard.resources
    atomic_json(out,row)


def simulate_unit(calibration,rep,repetitions,stream_tag,design,public,checkpoint=None,methods=None):
    import numpy as np
    from v9_switching import generate_pair
    from v8_mechanism_mc import forecast_report
    from conditional_features import build_features
    from study_core import build_label_cache,stable_mean
    from conditional_study import score_predictions
    from conditional_quantile import QuantileFitError
    from run_v8_wp3 import evaluate_method,scalar_diagnostics,DriverStop
    from run_study import StudyStop
    from v9_exposure import describe_geometry
    public=Path(public);public.mkdir(parents=True,exist_ok=True)
    if checkpoint is None:checkpoint=lambda **kw:None
    methods=['F',*(methods or ['QR33','QR4'])]
    timing={k:0. for k in ['generation','F','QR33','QR4']};records=[];geometry={}
    def persist():
        atomic_json(public/'progress.json',dict(records=records,seconds_by_method=timing),replace=True)
    def record(row):
        atomic_json(public/f"comparison-{row['arm']}-W{row['window']}-{row['method']}.json",row)
        records.append(row);persist()
    def fail_arm(arm,reason):
        for w in design['windows']:
            for method in methods[1:]:
                record(dict(rep=rep,source_id=calibration['source_id'],arm=arm,window=w,method=method,
                    status='FAILED',qr_mean_loss=None,f_mean_loss=None,qr_breaches=None,f_breaches=None,n=None,
                    selected_penalty=None,qr_reason=reason,f_reason=reason))
    whole=(calibration.get('whole_fit') or {}).get('params')
    if whole is None:
        for arm in ('constant','switching'):fail_arm(arm,'FAILED_WHOLE_FIT')
        return dict(complete=True,reason='FAILED_WHOLE_FIT',records=records,seconds_by_method=timing)
    period=calibration.get('M')
    if period is None:period=(calibration.get('whole_fit') or {}).get('diagnostics',{}).get('transition_count')
    if period is None:
        dwell=(calibration.get('partition') or {}).get('segment_lengths',[])
        if dwell and all(isinstance(v,(int,np.integer)) and not isinstance(v,(bool,np.bool_)) and v>0 for v in dwell):period=sum(map(int,dwell))
    if not isinstance(period,int) or isinstance(period,bool) or period<1:raise ValueError('SOURCE_TRANSITION_COUNT_MISSING')
    times=np.datetime64('2000-01-03T00:00:00','us')+np.arange(design['retained_observations'])*np.timedelta64(3600,'s')
    validation=np.arange(design['validation_first'],design['validation_last']+1,dtype=np.int64)
    evaluation=np.arange(design['evaluation_first'],design['evaluation_last']+1,dtype=np.int64)
    for arm in ['constant','switching']:
        if arm=='switching' and (calibration.get('calibration_status')!='COMPLETE'
                or calibration.get('partition') is None
                or not calibration.get('segment_fits')
                or any(f.get('params') is None for f in calibration['segment_fits'])):
            fail_arm(arm,'FAILED_SWITCHING_CALIBRATION');continue
        tic=time.monotonic()
        try:
            # The valid whole fit is generated independently first. A later
            # switching failure never replaces or invalidates that control.
            segments=[whole] if arm=='constant' else [f['params'] for f in calibration['segment_fits']]
            lengths=[period] if arm=='constant' else calibration['partition']['segment_lengths']
            pair=generate_pair(whole,segments,lengths,calibration['source_index'],rep,repetitions,stream_tag,design,checkpoint=checkpoint)
            identity={key:pair[key] for key in ('phase','uniform_sha256','rng_initial','rng_final')}
            if geometry and identity!= {key:geometry[key] for key in identity}:raise ValueError('PAIRED_RANDOM_STREAM_MISMATCH')
            path=pair[arm]
            arm_geometry=dict(**identity,regime_ids=path['regime_ids'].tolist(),
                transition_indices=path['transition_indices'].tolist(),wrap_indices=path['wrap_indices'].tolist(),
                exposure=describe_geometry(path,design))
            atomic_json(public/f'geometry-{arm}.json',arm_geometry)
            geometry.update(identity);geometry[arm]=arm_geometry
            atomic_json(public/'geometry.json',geometry,replace=True)
        except (DriverStop,StudyStop):raise
        except Exception as exc:
            reason='GENERATION_FAILED:'+type(exc).__name__
            atomic_json(public/f'generation-{arm}-failure.json',dict(reason=reason,message=str(exc)))
            fail_arm(arm,reason);continue
        finally:
            timing['generation']+=time.monotonic()-tic;persist()
        x=path['position'];features=build_features(x,times,short_scale=design['feature_rms_short'],long_scale=design['feature_rms_long'],nominal_gap_seconds=3600)
        cache=build_label_cache(x,design['horizon']);armdir=public/arm;armdir.mkdir(exist_ok=False)
        for window in design['windows']:
            evaluation_points={}
            def report(segment,h,w,method,penalty=None):
                origins=validation if segment=='validation' else evaluation
                result=forecast_report(x,times,features,cache,origins,h,w,design['refit_step'],method,penalty,checkpoint=checkpoint)
                score=score_predictions(cache.peak[origins],result['capacity'],np.abs(x[origins]),origins)
                if segment=='evaluation':
                    evaluation_points[method]=dict(losses=score.pinball.tolist(),breaches=score.strict_breach.tolist(),capacities=score.capacities.tolist())
                    atomic_json(armdir/f'W{w}-{method}-evaluation-points.json',evaluation_points[method])
                return dict(mean_loss=stable_mean(score.pinball),strict_breach_count=int(np.count_nonzero(score.strict_breach)),strict_breach_rate=float(np.mean(score.strict_breach)),n=len(origins)),scalar_diagnostics(result['fit_diagnostics'])
            outputs={}
            for method in methods:
                start=time.monotonic()
                try:outputs[method]=evaluate_method(design,armdir,window,design['horizon'],method,report,checkpoint,QuantileFitError,(DriverStop,StudyStop))
                finally:timing[method]+=time.monotonic()-start;persist()
                if method=='F':continue
                f=outputs['F'];q=outputs[method];fe=f.get('evaluation');qe=q.get('evaluation');ok=f['status']=='COMPLETE' and q['status']=='COMPLETE' and fe is not None and qe is not None
                record(dict(rep=rep,source_id=calibration['source_id'],arm=arm,window=window,method=method,status='COMPLETE' if ok else 'FAILED',
                    qr_mean_loss=qe['mean_loss'] if ok else None,f_mean_loss=fe['mean_loss'] if ok else None,
                    qr_breaches=qe['strict_breach_count'] if ok else None,f_breaches=fe['strict_breach_count'] if ok else None,n=qe['n'] if ok else None,
                    selected_penalty=q.get('selected_penalty'),qr_reason=q.get('reason'),f_reason=f.get('reason')))
            save(armdir/f'W{window}-evaluation-points.json',evaluation_points)
            checkpoint(stage='cell_end')
    return dict(complete=True,records=records,seconds_by_method=timing)


def forecast_worker(args):
    d=read_design();manifest=load(args.manifest);verify_seal(manifest);plan=load(args.plan)
    out=Path(args.output);guard,checkpoint=worker_runtime(manifest,out.parent,Path(args.private))
    calibration=load(PUBLIC/'diagnostics'/'units'/f's{args.source:02}'/'result.json')
    calibration.setdefault('source_id',manifest['sources'][args.source]['source_id'])
    calibration.setdefault('source_index',args.source)
    row=dict(source_id=calibration['source_id'],source_index=args.source,rep=args.rep,started_utc=utc_now(),complete=False,records=[])
    try:
        row.update(simulate_unit(calibration,args.rep,plan['repetitions'],plan['stream_tag'],d,out.parent,checkpoint,plan['conditional_methods']))
        checkpoint(stage='finalization')
    except Exception as exc:row.update(recover_unit_outputs(out.parent),complete=False,reason=getattr(exc,'code',getattr(exc,'reason',type(exc).__name__)),exception_type=type(exc).__name__)
    row.update(ended_utc=utc_now(),resources=guard.resources);atomic_json(out,row)


def run_batch(tasks,manifest_path,deadline,worker_count):
    manifest=load(manifest_path);active=[];waiting=list(tasks);finished=[]
    while waiting or active:
        now=time.monotonic()
        while waiting and len(active)<worker_count and now<deadline:
            task=waiting.pop(0);out=Path(task['output']);out.parent.mkdir(parents=True,exist_ok=False)
            private=Path(task['private']);private.mkdir(parents=True,exist_ok=True)
            command=[sys.executable,'-B',str(Path(__file__).resolve()),task['worker'],'--manifest',str(manifest_path),'--source',str(task['source']),'--output',str(out),'--private',str(private)]
            if 'rep' in task:command += ['--rep',str(task['rep']),'--plan',str(task['plan'])]
            env=os.environ.copy();env.update({k:'1' for k in THREAD_NAMES})
            log=(private/'console.txt').open('x');proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            active.append(dict(task=task,proc=proc,log=log,start=now));now=time.monotonic()
        for run in list(active):
            proc=run['proc'];now=time.monotonic();timeout=now>=deadline or now-run['start']>=manifest['design']['worker_hard_seconds']
            if proc.poll() is None and timeout:
                try:os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                proc.wait()
            if proc.poll() is not None:
                run['log'].close();task=run['task'];out=Path(task['output'])
                if not out.exists():
                    identity=manifest['sources'][task['source']]
                    save(out,dict(recover_unit_outputs(out.parent),complete=False,status='FAILED',source_id=identity['source_id'],kind=identity['kind'],source_index=task['source'],rep=task.get('rep'),reason='GLOBAL_DEADLINE' if now>=deadline else ('WORKER_TIMEOUT' if timeout else 'TECHNICAL_WORKER_EXIT'),exit_code=proc.returncode))
                finished.append(dict(task=task,elapsed_seconds=now-run['start'],exit_code=proc.returncode));active.remove(run)
        if now>=deadline:
            for task in waiting:
                out=Path(task['output']);out.parent.mkdir(parents=True,exist_ok=False)
                identity=manifest['sources'][task['source']]
                save(out,dict(complete=False,status='NOT_RUN',source_id=identity['source_id'],kind=identity['kind'],source_index=task['source'],rep=task.get('rep'),records=[],reason='GLOBAL_DEADLINE'))
                finished.append(dict(task=task,elapsed_seconds=0,exit_code=None))
            waiting=[]
        if active:time.sleep(.15)
    return finished


def archive_units(phase):
    directory=PUBLIC/phase;units=directory/'units';entries=[]
    with zipfile.ZipFile(directory/'units.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(units.rglob('*')):
            if p.is_file():
                data=p.read_bytes();relative=str(p.relative_to(units));z.writestr(relative,data)
                entries.append(dict(path=relative,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    save(directory/'units-manifest.json',dict(files=entries,archive_sha256=sha(directory/'units.zip'),loose_files_retained=True))


def diagnose():
    d=read_design();PUBLIC.mkdir(parents=True,exist_ok=False);PRIVATE.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();manifest=dict(schema='v9-study-seal-v1',started_utc=utc_now(),started_monotonic=start,deadline_monotonic=start+d['global_study_seconds'],design_commit=DESIGN_COMMIT,protocol_sha256=sha(ROOT/PROTOCOL),design=d,code_sha256={p:sha(ROOT/p) for p in [*NEW_CODE,'run_study.py',*d['forecast_source_sha256']]},sources=source_inventory(d))
    save(PUBLIC/'manifest.json',manifest);tasks=[]
    for i,source in enumerate(manifest['sources']):tasks.append(dict(worker='worker-diagnosis',source=i,output=str(PUBLIC/'diagnostics'/'units'/f's{i:02}'/'result.json'),private=str(PRIVATE/'diagnostics'/f's{i:02}')))
    finished=run_batch(tasks,PUBLIC/'manifest.json',manifest['deadline_monotonic'],d['worker_count'])
    save(PUBLIC/'diagnostics'/'completion.json',dict(ended_utc=utc_now(),tasks=finished));archive_units('diagnostics')
    rows=[]
    for i in range(15):
        row=load(PUBLIC/'diagnostics'/'units'/f's{i:02}'/'result.json');row.setdefault('source_id',manifest['sources'][i]['source_id']);row.setdefault('kind',manifest['sources'][i]['kind']);rows.append(row)
    save(PUBLIC/'diagnostics.json',rows)
    print(json.dumps({'diagnostics':Counter(r.get('status') for r in rows),'calibrations':Counter(r.get('calibration_status') for r in rows),'remaining_seconds':manifest['deadline_monotonic']-time.monotonic()},default=dict))


def verify_committed_run_plan(manifest,root=ROOT,path=None):
    """Require the exact timing-only run plan in its own prior Git commit."""
    root=Path(root);path=root/'results/v9/nonstationarity/run-plan.json' if path is None else Path(path)
    relative=str(path.relative_to(root));env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,env=env,stderr=subprocess.PIPE)
    try:
        raw=path.read_bytes();commit=git('log','-1','--format=%H','--',relative).decode().strip()
        if not commit:raise ValueError('RUN_PLAN_NOT_COMMITTED')
        if git('show',commit+':'+relative)!=raw or git('show','HEAD:'+relative)!=raw:raise ValueError('RUN_PLAN_COMMITTED_BYTES_MISMATCH')
        changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()
        if changed!=[relative]:raise ValueError('RUN_PLAN_NOT_SOLE_FILE_COMMIT')
        git('merge-base','--is-ancestor',commit,'HEAD')
        plan=json.loads(raw)
        if plan.get('design_commit')!=DESIGN_COMMIT or plan.get('code_sha256')!=manifest['code_sha256']:raise ValueError('RUN_PLAN_SEAL_MISMATCH')
        stamp=git('show','-s','--format=%cI',commit).decode().strip()
    except (OSError,subprocess.SubprocessError,KeyError) as exc:raise ValueError('RUN_PLAN_NOT_COMMITTED_OR_VERIFIED') from exc
    return plan,dict(commit=commit,sha256=hashlib.sha256(raw).hexdigest(),commit_time=stamp,sole_file=relative)


def forecast_phase(phase):
    d=read_design();manifest=load(PUBLIC/'manifest.json');verify_seal(manifest)
    if phase=='pilot':plan=dict(repetitions=2,conditional_methods=['QR33','QR4'],stream_tag=1)
    else:
        plan,provenance=verify_committed_run_plan(manifest)
        plan=dict(plan,stream_tag=2,run_plan_provenance=provenance)
    base=PUBLIC/phase;base.mkdir(exist_ok=False);save(base/'plan.json',plan)
    tasks=[]
    for rep in range(plan['repetitions']):
        for i in range(13):tasks.append(dict(worker='worker-forecast',source=i,rep=rep,plan=str(base/'plan.json'),output=str(base/'units'/f's{i:02}-r{rep:03}'/'result.json'),private=str(PRIVATE/phase/f's{i:02}-r{rep:03}')))
    started=time.monotonic();deadline=min(manifest['deadline_monotonic'],started+d['pilot_max_seconds']) if phase=='pilot' else manifest['deadline_monotonic']
    save(base/'receipt.json',dict(started_utc=utc_now(),started_monotonic=started,deadline_monotonic=deadline,plan=plan))
    finished=run_batch(tasks,PUBLIC/'manifest.json',deadline,d['worker_count']);units=[load(t['task']['output']) for t in finished]
    save(base/'completion.json',dict(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-started,tasks=finished));archive_units(phase)
    if phase=='pilot':
        choice=choose_configuration(units,manifest['deadline_monotonic']-time.monotonic(),d)
        save(PUBLIC/'run-plan.json',dict(choice,created_utc=utc_now(),design_commit=DESIGN_COMMIT,code_sha256=manifest['code_sha256'],pilot_summary=Counter('complete' if x.get('complete') else 'incomplete' for x in units)))
        print(json.dumps(choice,indent=2))
    else:summarize()


def summarize():
    import numpy as np
    d=read_design();manifest=load(PUBLIC/'manifest.json');plan=load(PUBLIC/'run-plan.json');diagnostics=load(PUBLIC/'diagnostics.json');ids=[x['source_id'] for x in manifest['sources'][:13]]
    records=[]
    for p in sorted((PUBLIC/'formal'/'units').glob('*/result.json')):records += load(p).get('records',[])
    cells=[]
    for source in ids:
        for arm in ['constant','switching']:
            for w in d['windows']:
                for method in plan['conditional_methods']:
                    rows=[r for r in records if r['source_id']==source and r['arm']==arm and r['window']==w and r['method']==method]
                    cells.append(dict(source_id=source,arm=arm,window=w,method=method,**reduce_cell(rows,plan['repetitions'])))
    predictions=prediction_status(cells,diagnostics,ids)
    save(PUBLIC/'summary.json',cells);save(PUBLIC/'predictions.json',predictions)
    with (PUBLIC/'summary.csv').open('x',newline='') as f:
        keys=[k for k in cells[0] if k!='failed_repetitions'];writer=csv.DictWriter(f,keys,extrasaction='ignore');writer.writeheader();writer.writerows(cells)
    diagnostic_fields=['source_id','kind','n','status','p_value','calibration_status']
    with (PUBLIC/'diagnostics.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,diagnostic_fields,extrasaction='ignore');writer.writeheader();writer.writerows(diagnostics)
    save(PUBLIC/'formal'/'replicate-scores.json',records)
    print(json.dumps({'cells':Counter(c['status'] for c in cells),'predictions':predictions},indent=2))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['diagnose','pilot','formal','summarize','worker-diagnosis','worker-forecast']);parser.add_argument('--manifest');parser.add_argument('--source',type=int);parser.add_argument('--rep',type=int);parser.add_argument('--plan');parser.add_argument('--output');parser.add_argument('--private');args=parser.parse_args()
    if args.command=='diagnose':diagnose()
    elif args.command in ('pilot','formal'):forecast_phase(args.command)
    elif args.command=='summarize':summarize()
    elif args.command=='worker-diagnosis':diagnostic_worker(args)
    else:forecast_worker(args)
if __name__=='__main__':main()
