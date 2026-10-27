"""Bounded fixed-parameter full-prefix backcast, with no import-time data read.

--run seals manifest before source parsing and dispatches eight sequential
workers. --summarize reads terminated complete private traces for exactly the
eight declared normal-HAC comparisons; it never forecasts or retunes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

import run_v8_wp3 as sealed

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
DESIGN_COMMIT='467a995'
DESIGN_FILES=('protocol/revision-v8/wp5-fixed-prefix-design.md','protocol/revision-v8/wp5-fixed-prefix-design.json')
SOURCE_SPEC='protocol/study-spec.json'
EXTRA_CODE=('v8_backcast.py','run_v8_wp5.py','test_v8_backcast.py','test_v8_wp5_driver.py')
FORMAL=ROOT/'results/revision-v8/wp5'
PRIVATE=ROOT/'.scratch/revision-v8/wp5'
DriverStop=sealed.DriverStop
exclusive_json=sealed.exclusive_json
sha_file=sealed.sha_file
verify_seal=sealed.verify_seal
wait_owned_worker=sealed.wait_owned_worker
ResourceCheckpoint=sealed.ResourceCheckpoint
utc_now=sealed.utc_now
read_json=sealed.read_json


def create_run_directories(formal,private):
    formal,private=Path(formal),Path(private)
    sealed.no_symlinks(formal);sealed.no_symlinks(private)
    formal.parent.mkdir(parents=True,exist_ok=True)
    formal.mkdir(mode=0o700,exist_ok=False)
    private.mkdir(mode=0o700,parents=True,exist_ok=False)
    (formal/'units').mkdir(mode=0o700)


def verify_parameters(design,root=ROOT):
    root=Path(root);hashes={}
    for name,digest in design['forecasting']['parameter_source_sha256'].items():
        if sha_file(root/name)!=digest:raise DriverStop('PARAMETER_SOURCE_HASH_MISMATCH')
        hashes[name]=digest
    old=read_json(root/'protocol/revision-20261022/selection-freeze.json')['cells']
    for method in design['methods']:
        if method['engine']=='F':continue
        for h in design['clock_and_target']['horizons']:
            wanted=method['penalty_by_horizon'][str(h)]
            if method['name']=='QR33':
                matches=[row for row in old if (row.get('source'),row.get('horizon'),row.get('window'),row.get('family'))==('fx_hourly',h,2880,'QR')]
                if len(matches)!=1 or matches[0].get('status')!='SELECTED' or matches[0].get('parameter')!=wanted:
                    raise DriverStop('PARAMETER_VALUE_MISMATCH')
            else:
                row=read_json(root/f'results/revision-20261023/parsimonious/fx_hourly-h{h}-w2880.json')
                if (row.get('source'),row.get('horizon'),row.get('window'),row.get('selected_penalty'))!=('fx_hourly',h,2880,wanted):
                    raise DriverStop('PARAMETER_VALUE_MISMATCH')
    return hashes


def verify_design(root=ROOT):
    """Verify frozen design, original code, source spec and selected parameters.

    This function reads no raw source, private arrays or new financial outcome.
    """
    root=Path(root);hashes={}
    from run_study import SPEC_SHA256
    try:
        commit=subprocess.run(['git','rev-parse',DESIGN_COMMIT+'^{commit}'],cwd=root,
            capture_output=True,text=True,check=True).stdout.strip()
        for name in DESIGN_FILES:
            frozen=subprocess.run(['git','show',commit+':'+name],cwd=root,capture_output=True,check=True).stdout
            current=(root/name).read_bytes()
            if current!=frozen:raise DriverStop('DESIGN_COMMIT_MISMATCH')
            hashes[name]=hashlib.sha256(current).hexdigest()
        design=read_json(root/DESIGN_FILES[1])
        for name,digest in design['original_and_sealed_modules_sha256'].items():
            if sha_file(root/name)!=digest:raise DriverStop('ORIGINAL_OR_SEALED_HASH_MISMATCH')
        hashes.update(verify_parameters(design,root))
        if sha_file(root/SOURCE_SPEC)!=SPEC_SHA256:raise DriverStop('SOURCE_SPECIFICATION_HASH_MISMATCH')
        hashes[SOURCE_SPEC]=SPEC_SHA256
        spec=read_json(root/SOURCE_SPEC)['source'];expected=design['input']
        if (spec['expected_csv_sha256']!=expected['sha256'] or spec['expected_csv_bytes']!=expected['bytes']
                or spec['expected_rows']!=expected['expected_original_rows']):raise DriverStop('SOURCE_DESIGN_MISMATCH')
    except (OSError,subprocess.SubprocessError,ValueError,KeyError,TypeError) as exc:
        raise DriverStop('DESIGN_OR_SOURCE_SPEC_UNVERIFIED') from exc
    return design,commit,hashes,spec


def planned_units(design):
    for h in design['clock_and_target']['horizons']:
        for method in design['methods']:
            penalties=method['penalty_by_horizon']
            yield dict(unit_id=f"H{h}_{method['name']}",horizon=h,method=method['name'],
                engine=method['engine'],window=method['window'],refit_step=method['refit_step'],
                penalty=None if penalties is None else penalties[str(h)])


def _validate_score(score,expected):
    if (type(score) is not dict or type(score.get('n')) is not int or score['n']!=expected
            or type(score.get('strict_breach_count')) is not int or not 0<=score['strict_breach_count']<=expected
            or type(score.get('mean_loss')) not in (int,float) or not math.isfinite(score['mean_loss']) or score['mean_loss']<0
            or score.get('strict_breach_rate')!=score['strict_breach_count']/expected
            or type(score.get('trace_sha256')) is not str or len(score['trace_sha256'])!=64
            or score.get('trace_origin_count')!=expected):raise ValueError('invalid full evaluation score')


def build_inventory(design,formal):
    rows=[];expected=design['sample']['evaluation_count']
    for unit in planned_units(design):
        row=dict(unit,selected_penalty=unit['penalty'],status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',
            evaluation=None,fit_diagnostics=[],maturity=None)
        public=Path(formal)/'units'/unit['unit_id'];path=public/'report.json'
        if path.exists():
            try:
                report=read_json(path)
                if report.get('status') not in ('COMPLETE','FAILED','NA_SAMPLE_SIZE'):raise ValueError('status')
                if report.get('selected_penalty',unit['penalty'])!=unit['penalty']:raise ValueError('penalty')
                if report['status']=='COMPLETE':_validate_score(report['evaluation'],expected)
                elif report.get('evaluation') is not None:raise ValueError('partial score')
                for key in ('status','reason','evaluation','fit_diagnostics','maturity','failure_diagnostics','failure_diagnostics_status','failure_progress','exception_type'):
                    if key in report:row[key]=report[key]
                # A report may be flushed immediately before a signal/kill.
                # Accept a complete score only after BOTH completion receipts
                # prove the sealed worker ended and its owned parent saw exit0.
                if row['status']=='COMPLETE':
                    worker_path=public/'worker-receipt.json'
                    worker=read_json(worker_path) if worker_path.exists() else None
                    if (worker is None or worker.get('status')!='COMPLETE'
                            or worker.get('code_hash_start')!='PASS' or worker.get('code_hash_end')!='PASS'):
                        row.update(status='FAILED',reason='WORKER_COMPLETION_UNVERIFIED',evaluation=None)
                    else:
                        parent_path=public/'parent-termination.json'
                        parent=read_json(parent_path) if parent_path.exists() else None
                        if parent is None or parent.get('status')!='COMPLETE' or parent.get('returncode')!=0:
                            row.update(status='FAILED',reason='PARENT_COMPLETION_UNVERIFIED',evaluation=None)
            except (OSError,ValueError,KeyError,TypeError):row.update(status='FAILED',reason='INVALID_METHOD_RECEIPT',evaluation=None)
        elif (public/'report.started.json').exists() or (public/'parent-start.json').exists():
            row.update(status='FAILED',reason='INTERRUPTED_METHOD')
        rows.append(row)
    return rows


def consistency_identity(receipt):
    identity=receipt['source_identity']
    return dict(source_identity={k:identity[k] for k in ('accepted_csv_sha256','accepted_csv_bytes','source_verified')},
        source_metadata=receipt['source_metadata'])


def check_consistency(receipts):
    values=[consistency_identity(r) for r in receipts]
    if not values:return None
    if any(r!=values[0] for r in values[1:]):raise DriverStop('SOURCE_CONSISTENCY_MISMATCH')
    return values[0]


def save_trace(private,public,arrays):
    import numpy as np
    private,public=Path(private),Path(public)
    n=len(arrays['origins'])
    if n<=0 or any(len(a)!=n for a in arrays.values()):raise ValueError('trace alignment')
    path=private/'evaluation.npz';sealed.no_symlinks(path)
    with open(path,'xb') as out:
        np.savez(out,**arrays);out.flush();os.fsync(out.fileno())
    receipt=dict(trace_sha256=sha_file(path),trace_origin_count=n)
    exclusive_json(public/'trace.json',receipt)
    return receipt


def run_study():
    start=time.monotonic();started=utc_now()
    design,commit,protocol_hashes,spec=verify_design()
    code_files=tuple(design['original_and_sealed_modules_sha256'])+EXTRA_CODE
    code_hashes={name:sha_file(ROOT/name) for name in code_files}
    run_id=uuid.uuid4().hex;private=PRIVATE/run_id
    create_run_directories(FORMAL,private)
    deadline=start+design['resources']['global_wall_seconds']
    manifest=dict(schema='v8-wp5-driver-1',design_id=design['design_id'],design=design,
        design_commit=commit,design_commit_requested=DESIGN_COMMIT,source_spec=spec,
        protocol_hashes=protocol_hashes,code_hashes=code_hashes,started_utc=started,
        study_start_monotonic=start,global_deadline_monotonic=deadline,run_id=run_id,
        formal_directory=str(FORMAL),private_directory=str(private),environment=sealed.software_environment(),
        planned_workers=8,planned_method_slots=8,planned_comparisons=8,planned_validation_candidates=0,
        no_source_parse_before_manifest=True,randomness='none')
    manifest_path=FORMAL/'manifest.json';exclusive_json(manifest_path,manifest)
    status='COMPLETE';reason=None;attempted=0;completed=0;active=None;sources=[]
    try:
        verify_seal(manifest)
        for unit in planned_units(design):
            if time.monotonic()>=deadline:status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
            verify_seal(manifest)
            public=FORMAL/'units'/unit['unit_id'];public.mkdir(mode=0o700)
            (private/unit['unit_id']).mkdir(mode=0o700)
            exclusive_json(public/'parent-start.json',dict(unit,started_utc=utc_now()))
            env=dict(os.environ,**{name:'1' for name in sealed.THREAD_NAMES},PYTHONDONTWRITEBYTECODE='1')
            cmd=[sys.executable,str(ROOT/'run_v8_wp5.py'),'--worker','--horizon',str(unit['horizon']),
                '--method',unit['method'],'--global-deadline',repr(deadline),'--manifest',str(manifest_path)]
            sealed.append_status(FORMAL/'progress.jsonl',event='worker_start',unit_id=unit['unit_id'],status='STARTED')
            attempted+=1
            with open(public/'process.log','x',encoding='utf-8') as log:
                active=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True)
                receipt=wait_owned_worker(active,deadline,hard_seconds=design['resources']['worker_hard_seconds']);active=None
            receipt.update(unit,ended_utc=utc_now());exclusive_json(public/'parent-termination.json',receipt)
            verify_seal(manifest);completed+=receipt['status']=='COMPLETE'
            source_path=public/'worker-source.json'
            if source_path.exists():sources.append(read_json(source_path));check_consistency(sources)
            worker_path=public/'worker-receipt.json';worker=read_json(worker_path) if worker_path.exists() else None
            sealed.append_status(FORMAL/'progress.jsonl',event='worker_end',unit_id=unit['unit_id'],status=receipt['status'],reason=receipt['reason'])
            if (receipt['returncode']==2 or worker and worker.get('technical_error')
                    or receipt['reason']=='WORKER_EXIT' and worker is None and receipt['returncode']!=-signal.SIGALRM):
                status='TECHNICAL_ERROR';reason='WORKER_TECHNICAL_ERROR';break
            if worker and worker.get('source_failure'):status='SOURCE_FAILURE';reason=worker['reason'];break
            if receipt['reason']=='GLOBAL_DEADLINE':status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
    except KeyboardInterrupt:status='INTERRUPTED';reason='PARENT_INTERRUPTED'
    except Exception as exc:status='TECHNICAL_ERROR';reason=exc.code if isinstance(exc,DriverStop) else 'PARENT_TECHNICAL_ERROR'
    finally:
        if active is not None:sealed.kill_owned_worker(active)
        seal_status='PASS'
        try:verify_seal(manifest)
        except DriverStop as exc:seal_status=exc.code;status='TECHNICAL_ERROR';reason=exc.code
        rows=build_inventory(design,FORMAL);exclusive_json(FORMAL/'inventory.json',rows)
        consistency=check_consistency(sources) if status!='TECHNICAL_ERROR' else None
        exclusive_json(FORMAL/'study-termination.json',dict(status=status,reason=reason,started_utc=started,
            ended_utc=utc_now(),elapsed_seconds=time.monotonic()-start,global_deadline_monotonic=deadline,
            attempted_workers=attempted,completed_workers=completed,planned_workers=8,all_workers_terminated=True,
            code_hash_check=seal_status,source_consistency=consistency,
            method_status_counts=dict(Counter(r['status'] for r in rows))))
    print(json.dumps(dict(event='study_terminated',status=status,reason=reason)),flush=True)
    return 0 if status=='COMPLETE' else 1


def _stamp(np,value):return str(np.datetime_as_string(value,unit='us'))


def run_worker(args):
    manifest=read_json(args.manifest);verify_seal(manifest)
    if args.global_deadline!=manifest['global_deadline_monotonic']:raise DriverStop('GLOBAL_DEADLINE_MISMATCH')
    design=manifest['design'];units=[u for u in planned_units(design) if (u['horizon'],u['method'])==(args.horizon,args.method)]
    if len(units)!=1:raise DriverStop('UNIT_IDENTITY')
    unit=units[0];public=Path(manifest['formal_directory'])/'units'/unit['unit_id'];private=Path(manifest['private_directory'])/unit['unit_id']
    for name in sealed.THREAD_NAMES:
        if os.environ.get(name)!='1':raise DriverStop('THREAD_ENVIRONMENT')
    start=time.monotonic();started=utc_now()
    from run_study import RunGuard,StudyStop,arm_hard_deadline,SPEC_SHA256
    remaining=args.global_deadline-time.monotonic()
    if remaining<=0:raise DriverStop('GLOBAL_DEADLINE')
    arm_hard_deadline(min(design['resources']['worker_hard_seconds'],remaining))
    guard=RunGuard(start,started,unit['unit_id'],public,private)
    checkpoint=ResourceCheckpoint(guard,args.global_deadline,private/'ps-snapshots.jsonl')
    receipt=dict(unit,status='FAILED',reason=None,started_utc=started,technical_error=False,source_failure=False,
        code_hash_start='PASS',code_hash_end=None,resources=None)
    row=dict(status='FAILED',reason=None,evaluation=None,selected_penalty=unit['penalty'],fit_diagnostics=[],maturity=None)
    exclusive_json(public/'report.started.json',dict(status='STARTED',started_utc=started,selected_penalty=unit['penalty']))
    progress={}
    def probe(**detail):
        progress.clear();progress.update({k:v for k,v in detail.items() if type(v) in (str,int,float,bool) or v is None})
        checkpoint(**detail)
    try:
        probe(stage='initialization')
        import numpy as np
        from study_data import load_source,SourceError
        from v8_backcast import backcast_geometry
        import v8_mechanism_mc as mc
        from conditional_features import build_features
        from conditional_quantile import QuantileFitError
        from conditional_study import score_predictions
        from study_core import build_label_cache,stable_mean
        probe(stage='initialization')
        if sha_file(ROOT/SOURCE_SPEC)!=SPEC_SHA256:raise DriverStop('SOURCE_SPECIFICATION_HASH_MISMATCH')
        try:
            source=load_source(ROOT/design['input']['local_private_path'],manifest['source_spec'],fetch=False,
                remaining_seconds=lambda:min(guard.remaining_seconds(),args.global_deadline-time.monotonic()),checkpoint=probe)
        except SourceError as exc:
            receipt.update(source_failure=True,reason=exc.code,source_reason=exc.reason)
            raise DriverStop(exc.code)
        geometry=backcast_geometry(len(source.position),design)
        receipt['geometry']=geometry
        if geometry['status']!='READY':
            row.update(status='NA_SAMPLE_SIZE',reason=geometry['reason']);receipt.update(status='NA_SAMPLE_SIZE',reason=geometry['reason'])
        else:
            position,times=source.position,source.times;s=design['sample'];a,b=s['evaluation_first'],s['evaluation_last']
            source_metadata=dict(n=len(position),source_first_timestamp=_stamp(np,times[0]),source_last_timestamp=_stamp(np,times[-1]),
                origin_first=a,origin_last=b,origin_count=b-a+1,first_issue_time=_stamp(np,times[a]),last_issue_time=_stamp(np,times[b]),
                target_end_by_horizon={str(h):_stamp(np,times[b+h]) for h in design['clock_and_target']['horizons']},
                position_sha256=hashlib.sha256(np.ascontiguousarray(position,dtype='<f8').tobytes()).hexdigest(),
                times_sha256=hashlib.sha256(np.ascontiguousarray(times.astype('datetime64[us]').view('i8'),dtype='<i8').tobytes()).hexdigest())
            exclusive_json(public/'worker-source.json',dict(source_identity=source.identity,source_metadata=source_metadata))
            feature_spec=design['features'];features=build_features(position,times,short_scale=feature_spec['short_rms'],long_scale=feature_spec['long_rms'],nominal_gap_seconds=feature_spec['nominal_gap_seconds'])
            if features.valid_from!=s['feature_valid_from']:raise ValueError('feature validity')
            cache=build_label_cache(position,args.horizon);origins=np.arange(a,b+1,dtype=np.int64)
            guard.arrays(source,features,cache,origins)
            result=mc.forecast_report(position,times,features,cache,origins,args.horizon,unit['window'],unit['refit_step'],unit['engine'],unit['penalty'],checkpoint=probe)
            peak=cache.peak[origins];floor=np.abs(position[origins]);score=score_predictions(peak,result['capacity'],floor,origins)
            diagnostics=sealed.scalar_diagnostics(result['fit_diagnostics'])
            if any(d['latest_label_end']>d['refit_index'] for d in diagnostics):raise ValueError('unfinished label')
            trace=save_trace(private,public,dict(origins=origins,refit_indices=result['refit_indices'],capacity=result['capacity'],peak=peak,floor=floor,pinball=score.pinball,strict_breach=score.strict_breach))
            hits=int(np.count_nonzero(score.strict_breach));n=len(origins)
            row.update(status='COMPLETE',evaluation=dict(n=n,mean_loss=stable_mean(score.pinball),strict_breach_count=hits,strict_breach_rate=hits/n,**trace),fit_diagnostics=diagnostics,maturity=sealed.maturity_summary(diagnostics))
            receipt['status']='COMPLETE'
        probe(stage='cell_end')
    except (DriverStop,StudyStop) as exc:
        row.update(status='FAILED',reason=exc.code,evaluation=None,failure_progress=dict(progress));receipt.update(status='FAILED',reason=exc.code)
    except Exception as exc:
        # Only safe scalar diagnostics are retained; never include source values
        # or low-level exception messages in public artifacts.
        from conditional_quantile import QuantileFitError
        if isinstance(exc,QuantileFitError):
            row.update(status='FAILED',reason=exc.code,evaluation=None,failure_progress=dict(progress))
            try:row.update(failure_diagnostics=sealed.scalar_diagnostics([dict(exc.diagnostics)])[0],failure_diagnostics_status='FINITE_SCALARS')
            except ValueError:row.update(failure_diagnostics=None,failure_diagnostics_status='NONFINITE_OR_NONSCALAR')
            receipt.update(status='FAILED',reason=exc.code)
        elif isinstance(exc,(ValueError,FloatingPointError)):
            row.update(status='FAILED',reason='NUMERIC_OR_STRUCTURAL_FAILURE',evaluation=None,exception_type=type(exc).__name__,failure_progress=dict(progress));receipt.update(status='FAILED',reason=row['reason'])
        else:
            row.update(status='FAILED',reason='TECHNICAL_ERROR',evaluation=None,exception_type=type(exc).__name__,failure_progress=dict(progress));receipt.update(status='FAILED',reason='TECHNICAL_ERROR',technical_error=True)
    finally:
        try:probe(stage='finalization')
        except (DriverStop,StudyStop) as exc:
            row.update(status='FAILED',reason=exc.code,evaluation=None);receipt.update(status='FAILED',reason=exc.code)
        try:verify_seal(manifest);receipt['code_hash_end']='PASS'
        except DriverStop as exc:
            row.update(status='FAILED',reason=exc.code,evaluation=None);receipt.update(status='FAILED',reason=exc.code,technical_error=True,code_hash_end=exc.code)
        receipt.update(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-start,resources=guard.resources)
        exclusive_json(public/'report.json',row);exclusive_json(public/'worker-receipt.json',receipt);signal.setitimer(signal.ITIMER_REAL,0)
    return 2 if receipt['technical_error'] else (0 if receipt['status'] in ('COMPLETE','NA_SAMPLE_SIZE') else 1)


def load_trace(row,private):
    import numpy as np
    if row['status']!='COMPLETE':raise DriverStop('INCOMPLETE_TRACE_REQUEST')
    path=Path(private)/row['unit_id']/'evaluation.npz';sealed.no_symlinks(path)
    if sha_file(path)!=row['evaluation']['trace_sha256']:raise DriverStop('PRIVATE_TRACE_HASH_MISMATCH')
    with np.load(path,allow_pickle=False) as source:arrays={name:source[name].copy() for name in source.files}
    if len(arrays['origins'])!=row['evaluation']['n'] or len(arrays['origins'])!=row['evaluation']['trace_origin_count']:
        raise DriverStop('PRIVATE_TRACE_COUNT_MISMATCH')
    return arrays


def make_contrasts(rows,manifest):
    from v8_backcast import compare_traces
    index={(r['horizon'],r['method']):r for r in rows};out=[];traces={}
    for h in manifest['design']['clock_and_target']['horizons']:
        for method in ('QR33','QR4'):
            for reference in ('F_matched','F_rolling720'):
                result=dict(horizon=h,method=method,reference=reference,status='FAILED',reason=None,n=None,
                    mean_model_loss=None,mean_reference_loss=None,relative_change_percent=None,
                    model_breach_count=None,reference_breach_count=None,model_breach_rate=None,reference_breach_rate=None,dm=None)
                model=index[(h,method)];ref=index[(h,reference)]
                if model['status']!='COMPLETE':result['reason']='MODEL_'+(model.get('reason') or model['status'])
                elif ref['status']!='COMPLETE':result['reason']='REFERENCE_'+(ref.get('reason') or ref['status'])
                else:
                    for row in (model,ref):
                        if row['unit_id'] not in traces:traces[row['unit_id']]=load_trace(row,manifest['private_directory'])
                    a,b=traces[model['unit_id']],traces[ref['unit_id']]
                    if any(not __import__('numpy').array_equal(a[k],b[k]) for k in ('origins','peak','floor')):
                        raise DriverStop('PAIRED_TARGET_MISMATCH')
                    result.update(compare_traces(a,b,h))
                    result.update(model_trace_sha256=model['evaluation']['trace_sha256'],reference_trace_sha256=ref['evaluation']['trace_sha256'])
                result.update(model_mean_loss=result['mean_model_loss'],reference_mean_loss=result['mean_reference_loss'],
                    model_breaches=result['model_breach_count'],reference_breaches=result['reference_breach_count'])
                out.append(result)
    return out


def write_csv(path,rows):
    sealed.no_symlinks(path);keys=list(dict.fromkeys(k for row in rows for k in row))
    with open(path,'x',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=keys);writer.writeheader()
        for row in rows:writer.writerow({k:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else ('NA' if v is None else v) for k,v in row.items()})


def summarize(manifest_path):
    manifest=read_json(manifest_path);formal=Path(manifest['formal_directory'])
    termination=read_json(formal/'study-termination.json')
    if not termination.get('all_workers_terminated'):raise DriverStop('STUDY_NOT_TERMINATED')
    verify_seal(manifest)
    for name in sealed.THREAD_NAMES:
        if os.environ.get(name)!='1':raise DriverStop('THREAD_ENVIRONMENT')
    from run_study import RunGuard,StudyStop
    started=utc_now();start=time.monotonic();private=Path(manifest['private_directory'])
    guard=RunGuard(start,started,'normal_dm_summary',formal,private)
    checkpoint=ResourceCheckpoint(guard,start+540,private/'summary-ps-snapshots.jsonl')
    checkpoint(stage='initialization')
    rows=read_json(formal/'inventory.json');contrasts=make_contrasts(rows,manifest)
    checkpoint(stage='cell_end');verify_seal(manifest)
    result=dict(design_id=manifest['design_id'],methods=rows,contrasts=contrasts,study_status=termination['status'],
        source_consistency=termination.get('source_consistency'),summarized_utc=utc_now(),
        source_inventory_sha256=sha_file(formal/'inventory.json'),post_result=True,exploratory=True,
        normal_DM_only=True,multiplicity_adjustment='none; eight fixed raw descriptive comparisons',
        independence_claim='MISMATCH: previously scored and overlapping; not a fresh third validation period',
        summary_resources=guard.resources,summary_elapsed_seconds=time.monotonic()-start)
    exclusive_json(formal/'summary.json',result);write_csv(formal/'summary.csv',rows);write_csv(formal/'contrasts.csv',contrasts)
    print(json.dumps(dict(event='summary_written',status='COMPLETE',method_slots=len(rows),contrasts=len(contrasts))),flush=True)
    return 0


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run',action='store_true');mode.add_argument('--worker',action='store_true');mode.add_argument('--summarize',action='store_true')
    parser.add_argument('--horizon',type=int);parser.add_argument('--method');parser.add_argument('--global-deadline',type=float)
    parser.add_argument('--manifest',type=Path,default=FORMAL/'manifest.json');args=parser.parse_args(argv)
    try:
        if args.run:return run_study()
        if args.summarize:return summarize(args.manifest)
        if args.horizon is None or args.method is None or args.global_deadline is None or not math.isfinite(args.global_deadline):
            parser.error('--worker requires horizon, method and finite global-deadline')
        return run_worker(args)
    except (DriverStop,OSError,ValueError,KeyError) as exc:
        print(json.dumps(dict(event='driver_stopped',status='FAILED',reason=exc.code if isinstance(exc,DriverStop) else type(exc).__name__)),flush=True)
        return 2


if __name__=='__main__':raise SystemExit(main())
