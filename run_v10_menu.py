"""Frozen E1 driver: inherited paths/forecasts, new six-point selector only."""
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
from run_v9_nonstationarity import atomic_json, recover_unit_outputs, save, sha, load, utc_now

ROOT=Path(__file__).resolve().parent
PROTOCOL='protocol/v10/menu-isolation-design.md'
DESIGN_COMMIT='3c5f167632a1a21ded29731a773a85ab307d3a96'
PUBLIC=ROOT/'results/v10/menu'
PRIVATE=ROOT/'.scratch/v10/menu'
THREAD_NAMES=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')
NEW_CODE=('run_v10_menu.py','v10_menu.py','v10_menu_summary.py')


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),stderr=subprocess.PIPE)


def committed_file(path,commit=None,sole=False):
    relative=str(Path(path).relative_to(ROOT))
    if commit is None:commit=git('log','-1','--format=%H','--',relative).decode().strip()
    raw=Path(path).read_bytes()
    if not commit or git('show',commit+':'+relative)!=raw or git('show','HEAD:'+relative)!=raw:raise ValueError('COMMITTED_FILE_MISMATCH:'+relative)
    git('merge-base','--is-ancestor',commit,'HEAD')
    if sole and git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()!=[relative]:raise ValueError('NOT_DESIGN_ONLY_COMMIT')
    return dict(commit=commit,commit_time=git('show','-s','--format=%cI',commit).decode().strip(),sha256=hashlib.sha256(raw).hexdigest(),path=relative)


def read_design():
    committed_file(ROOT/PROTOCOL,DESIGN_COMMIT,True)
    d=json.loads(re.search(r'```json\n(.*?)\n```',(ROOT/PROTOCOL).read_text(),re.S).group(1))
    fingerprints=dict(d['v9_forecast_source_sha256'])
    fingerprints.update({d['v9_design_path']:d['v9_design_sha256'],d['v9_calibration_path']:d['v9_calibration_sha256'],'v9_switching.py':d['v9_generator_sha256'],'v9_exposure.py':d['v9_exposure_sha256']})
    for p,digest in fingerprints.items():
        if sha(ROOT/p)!=digest:raise ValueError('FROZEN_INPUT_CHANGED:'+p)
    return d


def stage_plan(phase,repetitions=None):
    if phase=='pilot':
        if repetitions not in (None,2):raise ValueError('PILOT_REPETITIONS_FIXED')
        return dict(repetitions=2,stream_tag=1,path_phase_repetitions=2)
    if phase!='formal' or repetitions not in (16,32):raise ValueError('INVALID_FORMAL_PLAN')
    return dict(repetitions=repetitions,stream_tag=2,path_phase_repetitions=32)


def choose_configuration(pilot_rows,design):
    rows=list(pilot_rows);expected=len(design['sources'])*design['pilot_repetitions']
    valid=len(rows)==expected and all(r.get('complete') is True and isinstance(r.get('elapsed_seconds'),(float,int)) and not isinstance(r['elapsed_seconds'],bool) and math.isfinite(r['elapsed_seconds']) and r['elapsed_seconds']>0 for r in rows)
    ladder=[]
    for repetitions in design['formal_repetition_candidates']:
        projected=None
        if valid:
            costs=[r['elapsed_seconds'] for r in rows]
            projected=design['projection_safety_factor']*(repetitions/design['pilot_repetitions'])*max(sum(costs)/design['worker_count'],max(costs))+design['projection_reserve_seconds']
        ladder.append(dict(repetitions=repetitions,predicted_seconds=projected,predicted_fits=projected is not None and projected<=design['formal_max_seconds']))
    chosen=next((r for r in ladder if r['predicted_fits']),None)
    return dict(repetitions=None if chosen is None else chosen['repetitions'],projection_ladder=ladder,incomplete_pilot=not valid,status='AVAILABLE' if chosen else 'BUDGET_OR_PILOT_UNAVAILABLE')


def verify_control(new_geometry,old_geometry,new_f_points,old_f_points,new_f_score,old_f_score):
    if new_geometry!=old_geometry:raise ValueError('LEGACY_GEOMETRY_MISMATCH')
    if new_f_points is None or new_f_points!=old_f_points:raise ValueError('LEGACY_F_POINTS_MISMATCH')
    if new_f_score is None or new_f_score!=old_f_score:raise ValueError('LEGACY_F_SCORE_MISMATCH')
    return True


def verify_seal(manifest):
    frozen_design=read_design()
    if manifest['design']!=frozen_design:raise ValueError('MANIFEST_DESIGN_MISMATCH')
    committed_file(PUBLIC/'manifest.json')
    for p,digest in manifest['code_sha256'].items():
        if sha(ROOT/p)!=digest:raise ValueError('SEALED_CODE_CHANGED:'+p)


def seal():
    d=read_design();PUBLIC.mkdir(parents=True,exist_ok=False);PRIVATE.mkdir(parents=True,exist_ok=False)
    for phase in ('pilot','formal'):
        p=d['v9_'+phase+'_archive_path']
        if sha(ROOT/p)!=d['v9_'+phase+'_archive_sha256']:raise ValueError('LEGACY_ARCHIVE_CHANGED')
    files=[*NEW_CODE,'empirical_headroom.py','run_study.py','v9_switching.py','v9_exposure.py','run_v9_nonstationarity.py',*d['v9_forecast_source_sha256']]
    for p in files:
        if git('show','HEAD:'+p)!=(ROOT/p).read_bytes():raise ValueError('CODE_NOT_COMMITTED_BEFORE_SEAL:'+p)
    manifest=dict(schema='v10-menu-code-seal-v1',created_utc=utc_now(),design_commit=DESIGN_COMMIT,design_provenance=committed_file(ROOT/PROTOCOL,DESIGN_COMMIT,True),code_commit=git('rev-parse','HEAD').decode().strip(),code_sha256={p:sha(ROOT/p) for p in files},design=d)
    save(PUBLIC/'manifest.json',manifest)
    print(json.dumps(dict(status='SEALED',created_utc=manifest['created_utc'],code_commit=manifest['code_commit'])))


def simulate_unit(calibration,rep,repetitions,stream_tag,design,public,checkpoint=None,methods=None,legacy=None):
    import numpy as np
    from v9_switching import generate_pair
    from v10_menu import forecast_report, evaluate_method
    from conditional_features import build_features
    from study_core import build_label_cache,stable_mean
    from conditional_study import score_predictions
    from conditional_quantile import QuantileFitError
    from run_v8_wp3 import scalar_diagnostics,DriverStop
    from run_study import StudyStop
    from v9_exposure import describe_geometry
    public=Path(public);public.mkdir(parents=True,exist_ok=True)
    if checkpoint is None:checkpoint=lambda **kw:None
    methods=['F',*(methods or ['QR33','QR4'])]
    timing={k:0. for k in ['generation','F','QR33','QR4']};records=[];geometry={}
    def persist():
        atomic_json(public/'progress.json',dict(records=records,seconds_by_method=timing),replace=True)
    def record(row):
        original=legacy(f"comparison-{row['arm']}-W{row['window']}-{row['method']}.json")
        row.update(original_status=original.get('status'),original_qr_mean_loss=original.get('qr_mean_loss'),original_f_mean_loss=original.get('f_mean_loss'))
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
            if arm_geometry!=legacy(f'geometry-{arm}.json'):raise ValueError('LEGACY_GEOMETRY_MISMATCH')
            atomic_json(public/f'path-hashes-{arm}.json',{key:hashlib.sha256(np.ascontiguousarray(path[key],dtype='<f8').tobytes()).hexdigest() for key in ('position','variance','innovations')})
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
                if method=='F':
                    verify_control(arm_geometry,legacy(f'geometry-{arm}.json'),evaluation_points.get('F'),legacy(f'{arm}/W{window}-F-evaluation-points.json'),outputs['F'].get('evaluation'),legacy(f'{arm}/W{window}_H{design["horizon"]}_F.json').get('evaluation'))
                    atomic_json(armdir/f'W{window}-F-control-check.json',dict(status='EXACT_MATCH',geometry=True,all_point_arrays=True,all_score_scalars=True))
                    continue
                f=outputs['F'];q=outputs[method];fe=f.get('evaluation');qe=q.get('evaluation');ok=f['status']=='COMPLETE' and q['status']=='COMPLETE' and fe is not None and qe is not None
                record(dict(rep=rep,source_id=calibration['source_id'],arm=arm,window=window,method=method,status='COMPLETE' if ok else 'FAILED',
                    qr_mean_loss=qe['mean_loss'] if ok else None,f_mean_loss=fe['mean_loss'] if ok else None,
                    qr_breaches=qe['strict_breach_count'] if ok else None,f_breaches=fe['strict_breach_count'] if ok else None,n=qe['n'] if ok else None,
                    selected_penalty=q.get('selected_penalty'),qr_reason=q.get('reason'),f_reason=f.get('reason'),exact_tie=q.get('exact_tie',False),legacy_qr4_tie_changed=q.get('legacy_qr4_tie_changed',False)))
            save(armdir/f'W{window}-evaluation-points.json',evaluation_points)
            checkpoint(stage='cell_end')
    return dict(complete=True,records=records,seconds_by_method=timing)


def worker(args):
    manifest=load(args.manifest);verify_seal(manifest);d=manifest['design'];plan=load(args.plan)
    from run_study import RunGuard
    from run_v8_wp3 import ResourceCheckpoint
    out=Path(args.output);public=out.parent;private=Path(args.private)
    started=time.monotonic();guard=RunGuard(started,utc_now(),'v10-E1',public,private)
    checkpoint=ResourceCheckpoint(guard,plan['deadline_monotonic'],private/'resources.jsonl')
    calibration=next(r for r in load(ROOT/d['v9_calibration_path']) if r['source_id']==d['sources'][args.source]['source_id'])
    calibration=dict(calibration,source_index=args.source)
    archive=ROOT/d['v9_'+plan['phase']+'_archive_path']
    row=dict(source_id=calibration['source_id'],source_index=args.source,rep=args.rep,started_utc=utc_now(),complete=False,records=[])
    try:
        with zipfile.ZipFile(archive) as z:
            prefix=f's{args.source:02}-r{args.rep:03}/'
            def legacy(name):return json.loads(z.read(prefix+name))
            checkpoint(stage='initialization')
            row.update(simulate_unit(calibration,args.rep,plan['path_phase_repetitions'],plan['stream_tag'],d,public,checkpoint,d['conditional_methods'],legacy))
            checkpoint(stage='finalization')
    except Exception as exc:
        row.update(recover_unit_outputs(public),complete=False,reason=getattr(exc,'code',getattr(exc,'reason',type(exc).__name__)),exception_type=type(exc).__name__,message=str(exc))
    row.update(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-started,resources=guard.resources)
    atomic_json(out,row)


def run_batch(tasks,manifest_path,deadline,design):
    active=[];waiting=list(tasks);finished=[]
    while waiting or active:
        now=time.monotonic()
        while waiting and len(active)<design['worker_count'] and now<deadline:
            task=waiting.pop(0);out=Path(task['output']);out.parent.mkdir(parents=True,exist_ok=False)
            private=Path(task['private']);private.mkdir(parents=True,exist_ok=False)
            command=[sys.executable,'-B',str(Path(__file__).resolve()),'worker','--manifest',str(manifest_path),'--source',str(task['source']),'--rep',str(task['rep']),'--plan',str(task['plan']),'--output',str(out),'--private',str(private)]
            env=dict(os.environ,**{k:'1' for k in THREAD_NAMES})
            log=(private/'console.txt').open('x');proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            active.append(dict(task=task,proc=proc,log=log,start=time.monotonic()));now=time.monotonic()
        for run in list(active):
            proc=run['proc'];now=time.monotonic();timeout=now>=deadline or now-run['start']>=design['worker_hard_seconds']
            if proc.poll() is None and timeout:
                try:os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                proc.wait()
            if proc.poll() is not None:
                run['log'].close();task=run['task'];out=Path(task['output']);elapsed=now-run['start']
                if not out.exists():
                    save(out,dict(recover_unit_outputs(out.parent),complete=False,status='FAILED',source_id=design['sources'][task['source']]['source_id'],source_index=task['source'],rep=task['rep'],elapsed_seconds=elapsed,reason='GLOBAL_DEADLINE' if now>=deadline else ('WORKER_TIMEOUT' if timeout else 'TECHNICAL_WORKER_EXIT'),exit_code=proc.returncode))
                finished.append(dict(task=task,elapsed_seconds=elapsed,exit_code=proc.returncode));active.remove(run)
        if now>=deadline:
            for task in waiting:
                out=Path(task['output']);out.parent.mkdir(parents=True,exist_ok=False)
                save(out,dict(complete=False,status='NOT_RUN',source_id=design['sources'][task['source']]['source_id'],source_index=task['source'],rep=task['rep'],records=[],elapsed_seconds=0,reason='GLOBAL_DEADLINE'))
                finished.append(dict(task=task,elapsed_seconds=0,exit_code=None))
            waiting=[]
        if active:time.sleep(.15)
    return finished


def archive_units(base):
    entries=[]
    with zipfile.ZipFile(base/'units.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted((base/'units').rglob('*')):
            if path.is_file():
                raw=path.read_bytes();name=str(path.relative_to(base/'units'));z.writestr(name,raw)
                entries.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    save(base/'units-manifest.json',dict(files=entries,archive_sha256=sha(base/'units.zip'),loose_files_retained=True))


def forecast_phase(phase):
    manifest=load(PUBLIC/'manifest.json');verify_seal(manifest);d=manifest['design']
    archive=ROOT/d['v9_'+phase+'_archive_path']
    expected_archive_sha=d['v9_'+phase+'_archive_sha256']
    if sha(archive)!=expected_archive_sha:raise ValueError('LEGACY_ARCHIVE_CHANGED_BEFORE_PHASE')
    if phase=='pilot':plan=stage_plan('pilot')
    else:
        provenance=committed_file(PUBLIC/'run-plan.json',sole=True);choice=load(PUBLIC/'run-plan.json')
        if choice['code_sha256']!=manifest['code_sha256'] or choice['design_commit']!=DESIGN_COMMIT:raise ValueError('RUN_PLAN_SEAL_MISMATCH')
        if choice['repetitions'] is None:
            save(PUBLIC/'formal-unavailable.json',dict(status='UNAVAILABLE',reason=choice['status'],run_plan_provenance=provenance));return
        plan=dict(stage_plan('formal',choice['repetitions']),run_plan_provenance=provenance)
    base=PUBLIC/phase;base.mkdir(exist_ok=False)
    started=time.monotonic();stamp=utc_now();deadline=started+d[phase+'_max_seconds']
    plan.update(phase=phase,started_utc=stamp,started_monotonic=started,deadline_monotonic=deadline)
    save(base/'plan.json',plan);tasks=[]
    for rep in range(plan['repetitions']):
        for source in range(len(d['sources'])):
            identity=f's{source:02}-r{rep:03}'
            tasks.append(dict(source=source,rep=rep,plan=str(base/'plan.json'),output=str(base/'units'/identity/'result.json'),private=str(PRIVATE/phase/identity)))
    finished=run_batch(tasks,PUBLIC/'manifest.json',deadline,d)
    if sha(archive)!=expected_archive_sha:raise ValueError('LEGACY_ARCHIVE_CHANGED_DURING_PHASE')
    units=[load(row['task']['output']) for row in finished]
    completion=dict(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-started,tasks=finished,complete_units=sum(u.get('complete',False) for u in units),planned_units=len(tasks))
    save(base/'completion.json',completion);archive_units(base)
    if phase=='pilot':
        timings=[dict(u,elapsed_seconds=row['elapsed_seconds']) for u,row in zip(units,finished)]
        choice=dict(choose_configuration(timings,d),created_utc=utc_now(),design_commit=DESIGN_COMMIT,code_sha256=manifest['code_sha256'],pilot_completion=completion)
        save(PUBLIC/'run-plan.json',choice);print(json.dumps({k:v for k,v in choice.items() if k not in ('code_sha256','pilot_completion')},indent=2))
    else:make_summary()


def make_summary():
    from v10_menu_summary import summarize
    manifest=load(PUBLIC/'manifest.json');verify_seal(manifest);plan=load(PUBLIC/'run-plan.json');records=[]
    for path in sorted((PUBLIC/'formal'/'units').glob('*/result.json')):records.extend(load(path).get('records',[]))
    d=manifest['design'];summary=summarize(records,plan['repetitions'],[r['source_id'] for r in d['sources']],d)
    save(PUBLIC/'summary.json',summary);save(PUBLIC/'formal'/'replicate-scores.json',records)
    fields=list(summary['cells'][0])
    with (PUBLIC/'summary.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,fields);writer.writeheader();writer.writerows(summary['cells'])
    save(PUBLIC/'ties.json',dict(exact_ties=sum(bool(r.get('exact_tie')) for r in records),legacy_qr4_tie_changed=sum(bool(r.get('legacy_qr4_tie_changed')) for r in records),by_method={m:sum(bool(r.get('exact_tie')) for r in records if r['method']==m) for m in d['conditional_methods']}))
    print(json.dumps(dict(cells=Counter(r['status'] for r in summary['cells']),predictions=summary['predictions']),indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=('seal','pilot','formal','summarize','worker'));p.add_argument('--manifest');p.add_argument('--plan');p.add_argument('--source',type=int);p.add_argument('--rep',type=int);p.add_argument('--output');p.add_argument('--private');a=p.parse_args()
    if a.command=='seal':seal()
    elif a.command in ('pilot','formal'):forecast_phase(a.command)
    elif a.command=='summarize':make_summary()
    else:worker(a)
if __name__=='__main__':main()
