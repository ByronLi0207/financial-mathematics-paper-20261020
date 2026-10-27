"""Bounded same-dealer daily FX extension; parent imports only stdlib.

--run exclusively creates the single WP4 output and seals the design/code
before any data parse. --worker processes one fixed W/H cell. --summarize
reads terminated outputs; it performs no source parse or forecasting.
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
DESIGN_COMMIT='1427dc0'
DESIGN_FILES=('protocol/revision-v8/wp4-daily-fx-design.md','protocol/revision-v8/wp4-daily-fx-design.json')
SOURCE_SPEC='protocol/study-spec.json'
EXTRA_CODE=('v8_daily_fx.py','run_v8_wp4.py','test_v8_daily_fx.py','test_v8_wp4_driver.py')
FORMAL=ROOT/'results/revision-v8/wp4'
PRIVATE=ROOT/'.scratch/revision-v8/wp4'
METHODS=('F','QR33','QR4')
DriverStop=sealed.DriverStop
exclusive_json=sealed.exclusive_json
sha_file=sealed.sha_file
verify_seal=sealed.verify_seal
wait_owned_worker=sealed.wait_owned_worker
method_path=sealed.method_path
candidate_path=sealed.candidate_path
selection_path=sealed.selection_path
ResourceCheckpoint=sealed.ResourceCheckpoint
utc_now=sealed.utc_now
read_json=sealed.read_json


def create_run_directories(formal,private):
    formal,private=Path(formal),Path(private)
    sealed.no_symlinks(formal);sealed.no_symlinks(private)
    formal.parent.mkdir(parents=True,exist_ok=True)
    formal.mkdir(mode=0o700,exist_ok=False)
    private.mkdir(mode=0o700,parents=True,exist_ok=False)
    (formal/'cells').mkdir(mode=0o700)


def verify_design(root=ROOT):
    """Read only frozen design and source code, never accepted raw data."""
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
        design=json.loads((root/DESIGN_FILES[1]).read_text())
        for name,digest in design['original_and_sealed_modules_sha256'].items():
            if sha_file(root/name)!=digest:raise DriverStop('ORIGINAL_OR_SEALED_HASH_MISMATCH')
        if sha_file(root/SOURCE_SPEC)!=SPEC_SHA256:raise DriverStop('SOURCE_SPECIFICATION_HASH_MISMATCH')
        hashes[SOURCE_SPEC]=SPEC_SHA256
        source_spec=json.loads((root/SOURCE_SPEC).read_text())['source']
        expected=design['input']
        if (source_spec['expected_csv_sha256']!=expected['sha256']
                or source_spec['expected_csv_bytes']!=expected['bytes']
                or source_spec['expected_rows']!=expected['expected_original_rows']):
            raise DriverStop('SOURCE_DESIGN_MISMATCH')
    except (OSError,subprocess.SubprocessError,ValueError,KeyError,TypeError) as exc:
        raise DriverStop('DESIGN_OR_SOURCE_SPEC_UNVERIFIED') from exc
    return design,commit,hashes,source_spec


def planned_cells(design):
    for window in design['windows']:
        for horizon in design['clock_and_target']['horizons']:
            yield dict(cell_id=f'W{window}_H{horizon}',window=window,horizon=horizon)


def projection(design,geometry=None):
    geometry=geometry or design['sample']
    return dict(menus=design['menus'],validation_first=geometry['validation_first'],
        validation_last=geometry['validation_last'])


def declared_candidates(design,method,reason):
    return [dict(penalty=p,status='NOT_ATTEMPTED',reason=reason,origin_count=0,mean_loss=None)
            for p in design['menus'].get(method,[])]


def save_sample_na(design,public,cell,geometry):
    for method in METHODS:
        exclusive_json(method_path(public,cell['window'],cell['horizon'],method),
            dict(status='NA_SAMPLE_SIZE',reason=geometry['reason'],evaluation=None,
                selected_penalty=None,candidates=declared_candidates(design,method,geometry['reason']),
                fit_diagnostics=[],maturity=None,geometry=geometry))


def _validate_score(score,expected=None):
    if (type(score) is not dict or type(score.get('n')) is not int or score['n']<=0
            or expected is not None and score['n']!=expected
            or type(score.get('strict_breach_count')) is not int
            or not 0<=score['strict_breach_count']<=score['n']
            or type(score.get('mean_loss')) not in (int,float)
            or not math.isfinite(score['mean_loss']) or score['mean_loss']<0
            or score.get('strict_breach_rate')!=score['strict_breach_count']/score['n']):
        raise ValueError('invalid full evaluation score')


def build_inventory(design,formal):
    inventory=[]
    for cell in planned_cells(design):
        public=Path(formal)/'cells'/cell['cell_id']
        geometry=read_json(public/'cell-geometry.json') if (public/'cell-geometry.json').exists() else None
        for method in METHODS:
            row=dict(cell,method=method,status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',
                selected_penalty=None,evaluation=None,fit_diagnostics=[],maturity=None,geometry=geometry,
                candidates=sealed.candidate_inventory(projection(design),public,cell['window'],cell['horizon'],method))
            path=method_path(public,cell['window'],cell['horizon'],method)
            if path.exists():
                try:
                    report=read_json(path)
                    if report['status'] not in ('COMPLETE','FAILED','NA_SAMPLE_SIZE'):raise ValueError('status')
                    if report['status']=='COMPLETE':_validate_score(report['evaluation'],None if geometry is None else geometry['evaluation_count'])
                    for key in ('status','reason','selected_penalty','evaluation','fit_diagnostics','maturity','candidates'):
                        if key in report:row[key]=report[key]
                except (OSError,KeyError,TypeError,ValueError):
                    row.update(status='FAILED',reason='INVALID_METHOD_RECEIPT',evaluation=None)
            elif method_path(public,cell['window'],cell['horizon'],method,started=True).exists():
                row.update(status='FAILED',reason='INTERRUPTED_METHOD')
                path=selection_path(public,cell['window'],cell['horizon'],method)
                if path.exists():
                    selection=read_json(path);penalty=selection.get('penalty')
                    if selection.get('status')=='INELIGIBLE' and penalty is None:
                        row['reason']='VALIDATION_INELIGIBLE'
                    elif selection.get('status')!='SELECTED' or penalty not in design['menus'].get(method,[]):
                        raise DriverStop('INVALID_SELECTION_RECEIPT')
                    row['selected_penalty']=penalty
                    row['validation_selection']=selection
            # Candidate trace receipts are immutable public hashes, never private paths.
            for index,candidate in enumerate(row['candidates']):
                trace=public/f"W{cell['window']}_H{cell['horizon']}_{method}_validation-{index}.trace.json"
                if trace.exists():candidate.update(read_json(trace))
            inventory.append(row)
    return inventory


def consistency_identity(receipt):
    source=receipt['source_identity']
    return dict(source_identity={key:source[key] for key in
        ('accepted_csv_sha256','accepted_csv_bytes','source_verified')},daily_metadata=receipt['daily_metadata'])


def check_consistency(receipts):
    identities=[consistency_identity(r) for r in receipts]
    if not identities:return None
    if any(r!=identities[0] for r in identities[1:]):raise DriverStop('SOURCE_AGGREGATION_MISMATCH')
    return identities[0]


def save_private_npz(path,arrays):
    import numpy as np
    path=Path(path);sealed.no_symlinks(path)
    with open(path,'xb') as out:
        np.savez(out,**arrays);out.flush();os.fsync(out.fileno())
    return sha_file(path)


def save_trace(private,public,stem,arrays):
    count=len(arrays['origins'])
    if count<=0 or any(len(value)!=count for value in arrays.values()):raise ValueError('trace alignment')
    digest=save_private_npz(Path(private)/(stem+'.npz'),arrays)
    receipt=dict(trace_sha256=digest,trace_origin_count=count)
    exclusive_json(Path(public)/(stem+'.trace.json'),receipt)
    return receipt


def run_study():
    start=time.monotonic();started=utc_now()
    design,commit,protocol_hashes,source_spec=verify_design()
    code_files=tuple(design['original_and_sealed_modules_sha256'])+EXTRA_CODE
    code_hashes={name:sha_file(ROOT/name) for name in code_files}
    run_id=uuid.uuid4().hex;private=PRIVATE/run_id
    create_run_directories(FORMAL,private)
    deadline=start+design['resources']['global_wall_seconds']
    manifest=dict(schema='v8-wp4-driver-1',design_id=design['design_id'],design=design,
        design_commit=commit,design_commit_requested=DESIGN_COMMIT,source_spec=source_spec,
        protocol_hashes=protocol_hashes,code_hashes=code_hashes,started_utc=started,
        study_start_monotonic=start,global_deadline_monotonic=deadline,run_id=run_id,
        formal_directory=str(FORMAL),private_directory=str(private),environment=sealed.software_environment(),
        planned_workers=4,planned_method_slots=12,planned_validation_candidates=32,
        no_source_parse_before_manifest=True,randomness='none')
    manifest_path=FORMAL/'manifest.json';exclusive_json(manifest_path,manifest)
    status='COMPLETE';reason=None;attempted=0;completed=0;active=None;source_receipts=[]
    try:
        verify_seal(manifest)
        for cell in planned_cells(design):
            if time.monotonic()>=deadline:status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
            verify_seal(manifest)
            public=FORMAL/'cells'/cell['cell_id'];public.mkdir(mode=0o700)
            unit_private=private/cell['cell_id'];unit_private.mkdir(mode=0o700)
            exclusive_json(public/'parent-start.json',dict(cell,started_utc=utc_now()))
            env=dict(os.environ,**{name:'1' for name in sealed.THREAD_NAMES},PYTHONDONTWRITEBYTECODE='1')
            cmd=[sys.executable,str(ROOT/'run_v8_wp4.py'),'--worker','--window',str(cell['window']),
                '--horizon',str(cell['horizon']),'--global-deadline',repr(deadline),'--manifest',str(manifest_path)]
            sealed.append_status(FORMAL/'progress.jsonl',event='worker_start',unit_id=cell['cell_id'],status='STARTED')
            attempted+=1
            with open(public/'process.log','x',encoding='utf-8') as log:
                active=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True)
                receipt=wait_owned_worker(active,deadline,hard_seconds=design['resources']['worker_hard_seconds']);active=None
            receipt.update(cell,ended_utc=utc_now());exclusive_json(public/'parent-termination.json',receipt)
            verify_seal(manifest)
            completed+=receipt['status']=='COMPLETE'
            source_file=public/'worker-source.json'
            if source_file.exists():source_receipts.append(read_json(source_file));check_consistency(source_receipts)
            sealed.append_status(FORMAL/'progress.jsonl',event='worker_end',unit_id=cell['cell_id'],status=receipt['status'],reason=receipt['reason'])
            worker_path=public/'worker-receipt.json';worker=read_json(worker_path) if worker_path.exists() else None
            if (receipt['returncode']==2 or worker and worker.get('technical_error')
                    or receipt['reason']=='WORKER_EXIT' and worker is None and receipt['returncode']!=-signal.SIGALRM):
                status='TECHNICAL_ERROR';reason='WORKER_TECHNICAL_ERROR';break
            if worker and worker.get('source_failure'):
                status='SOURCE_FAILURE';reason=worker['reason'];break
            if receipt['reason']=='GLOBAL_DEADLINE':status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
    except KeyboardInterrupt:status='INTERRUPTED';reason='PARENT_INTERRUPTED'
    except Exception as exc:status='TECHNICAL_ERROR';reason=exc.code if isinstance(exc,DriverStop) else 'PARENT_TECHNICAL_ERROR'
    finally:
        if active is not None:sealed.kill_owned_worker(active)
        seal_status='PASS'
        try:verify_seal(manifest)
        except DriverStop as exc:seal_status=exc.code;status='TECHNICAL_ERROR';reason=exc.code
        inventory=build_inventory(design,FORMAL);exclusive_json(FORMAL/'inventory.json',inventory)
        source_consistency=check_consistency(source_receipts) if status!='TECHNICAL_ERROR' else None
        exclusive_json(FORMAL/'study-termination.json',dict(status=status,reason=reason,
            started_utc=started,ended_utc=utc_now(),elapsed_seconds=time.monotonic()-start,
            global_deadline_monotonic=deadline,attempted_workers=attempted,completed_workers=completed,
            planned_workers=4,all_workers_terminated=True,code_hash_check=seal_status,
            source_consistency=source_consistency,method_status_counts=dict(Counter(r['status'] for r in inventory))))
    print(json.dumps(dict(event='study_terminated',status=status,reason=reason)),flush=True)
    return 0 if status=='COMPLETE' else 1


def run_worker(args):
    manifest=read_json(args.manifest);verify_seal(manifest)
    if args.global_deadline!=manifest['global_deadline_monotonic']:raise DriverStop('GLOBAL_DEADLINE_MISMATCH')
    design=manifest['design']
    cells=[c for c in planned_cells(design) if (c['window'],c['horizon'])==(args.window,args.horizon)]
    if len(cells)!=1:raise DriverStop('CELL_IDENTITY')
    cell=cells[0];public=Path(manifest['formal_directory'])/'cells'/cell['cell_id']
    private=Path(manifest['private_directory'])/cell['cell_id']
    for name in sealed.THREAD_NAMES:
        if os.environ.get(name)!='1':raise DriverStop('THREAD_ENVIRONMENT')
    start=time.monotonic();started=utc_now()
    from run_study import RunGuard,StudyStop,arm_hard_deadline,SPEC_SHA256
    remaining=args.global_deadline-time.monotonic()
    if remaining<=0:raise DriverStop('GLOBAL_DEADLINE')
    arm_hard_deadline(min(design['resources']['worker_hard_seconds'],remaining))
    guard=RunGuard(start,started,cell['cell_id'],public,private)
    checkpoint=ResourceCheckpoint(guard,args.global_deadline,private/'ps-snapshots.jsonl')
    receipt=dict(cell,status='FAILED',reason=None,started_utc=started,technical_error=False,
        source_failure=False,code_hash_start='PASS',code_hash_end=None,resources=None,completed_method_reports=0)
    try:
        checkpoint(stage='initialization')
        import numpy as np
        from study_data import load_source,SourceError
        from v8_daily_fx import resample_closed_days,daily_issue_geometry
        import v8_mechanism_mc as mc
        from conditional_features import build_features
        from conditional_quantile import QuantileFitError
        from conditional_study import score_predictions
        from study_core import build_label_cache,stable_mean
        checkpoint(stage='initialization')
        if sha_file(ROOT/SOURCE_SPEC)!=SPEC_SHA256:raise DriverStop('SOURCE_SPECIFICATION_HASH_MISMATCH')
        source_spec=json.loads((ROOT/SOURCE_SPEC).read_text())['source']
        try:
            source=load_source(ROOT/design['input']['local_private_path'],source_spec,fetch=False,
                remaining_seconds=lambda:min(guard.remaining_seconds(),args.global_deadline-time.monotonic()),checkpoint=checkpoint)
        except SourceError as exc:
            receipt.update(source_failure=True,reason=exc.code,source_reason=exc.reason)
            raise DriverStop(exc.code)
        daily=resample_closed_days(source.position,source.times)
        mapping_sha=save_private_npz(private/'daily-series.npz',dict(position=daily.position,times=daily.times,
            selected_indices=daily.selected_indices,selected_raw_times=daily.selected_raw_times))
        source_receipt=dict(source_identity=source.identity,daily_metadata=daily.metadata,daily_mapping_sha256=mapping_sha)
        exclusive_json(public/'worker-source.json',source_receipt)
        geometry=daily_issue_geometry(len(daily.position),args.horizon,args.window,design)
        exclusive_json(public/'cell-geometry.json',geometry);receipt['geometry']=geometry
        if geometry['status']=='NA_SAMPLE_SIZE':
            save_sample_na(design,public,cell,geometry);receipt['completed_method_reports']=3
            receipt['status']='NA_SAMPLE_SIZE';receipt['reason']=geometry['reason']
        else:
            feature_spec=design['features'];position=daily.position;times=daily.times
            features=build_features(position,times,short_scale=feature_spec['short_rms'],
                long_scale=feature_spec['long_rms'],nominal_gap_seconds=feature_spec['nominal_gap_seconds'])
            if features.valid_from!=geometry['feature_valid_from']:raise ValueError('feature validity')
            cache=build_label_cache(position,args.horizon)
            guard.arrays(source,daily,features,cache)
            validation=np.arange(geometry['validation_first'],geometry['validation_last']+1,dtype=np.int64)
            evaluation=np.arange(geometry['evaluation_first'],geometry['evaluation_last']+1,dtype=np.int64)
            def report(segment,h,w,method,penalty):
                origins=validation if segment=='validation' else evaluation
                result=mc.forecast_report(position,times,features,cache,origins,h,w,
                    design['forecasting']['refit_step'],method,penalty,checkpoint=checkpoint)
                peak=cache.peak[origins];floor=np.abs(position[origins])
                score=score_predictions(peak,result['capacity'],floor,origins)
                breaches=int(np.count_nonzero(score.strict_breach));n=len(origins)
                stem=f'W{w}_H{h}_{method}_{segment}'
                if segment=='validation':stem+='-'+str(design['menus'][method].index(penalty))
                trace=save_trace(private,public,stem,dict(origins=origins,refit_indices=result['refit_indices'],
                    capacity=result['capacity'],peak=peak,floor=floor,pinball=score.pinball,strict_breach=score.strict_breach))
                return dict(mean_loss=stable_mean(score.pinball),n=n,strict_breach_count=breaches,
                    strict_breach_rate=breaches/n,**trace),sealed.scalar_diagnostics(result['fit_diagnostics'])
            for method in METHODS:
                sealed.evaluate_method(projection(design,geometry),public,args.window,args.horizon,method,
                    report,checkpoint,QuantileFitError,(DriverStop,StudyStop))
                receipt['completed_method_reports']+=1
            receipt['status']='COMPLETE'
        checkpoint(stage='cell_end')
    except (DriverStop,StudyStop) as exc:receipt.update(status='FAILED',reason=exc.code)
    except (ValueError,FloatingPointError) as exc:receipt.update(status='FAILED',reason='NUMERIC_OR_STRUCTURAL_FAILURE',exception_type=type(exc).__name__)
    except Exception as exc:receipt.update(status='FAILED',reason='TECHNICAL_ERROR',technical_error=True,exception_type=type(exc).__name__)
    finally:
        try:checkpoint(stage='finalization')
        except (DriverStop,StudyStop) as exc:receipt.update(status='FAILED',reason=exc.code)
        try:verify_seal(manifest);receipt['code_hash_end']='PASS'
        except DriverStop as exc:receipt.update(status='FAILED',reason=exc.code,technical_error=True,code_hash_end=exc.code)
        receipt.update(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-start,resources=guard.resources)
        exclusive_json(public/'worker-receipt.json',receipt);signal.setitimer(signal.ITIMER_REAL,0)
    return 2 if receipt['technical_error'] else (0 if receipt['status'] in ('COMPLETE','NA_SAMPLE_SIZE') else 1)


def make_contrasts(rows,design):
    indexed={(r['window'],r['horizon'],r['method']):r for r in rows};contrasts=[]
    for cell in planned_cells(design):
        for method in ('QR33','QR4'):
            row=dict(cell,method=method,reference_method='F',status='FAILED',reason=None,
                model_loss=None,reference_loss=None,relative_loss_percent=None,
                relative_loss_undefined_reason=None,n=None,model_breach_rate=None,reference_breach_rate=None)
            model=indexed[(cell['window'],cell['horizon'],method)]
            reference=indexed[(cell['window'],cell['horizon'],'F')]
            if model['status']!='COMPLETE':row['reason']='MODEL_'+(model.get('reason') or model['status'])
            elif reference['status']!='COMPLETE':row['reason']='REFERENCE_'+(reference.get('reason') or reference['status'])
            else:
                a=model['evaluation'];b=reference['evaluation'];_validate_score(a);_validate_score(b)
                if a['n']!=b['n']:row['reason']='MISMATCHED_EVALUATION_COUNTS'
                else:
                    row.update(status='COMPLETE',model_loss=a['mean_loss'],reference_loss=b['mean_loss'],n=a['n'],
                        model_breach_rate=a['strict_breach_rate'],reference_breach_rate=b['strict_breach_rate'])
                    if b['mean_loss']==0:row['relative_loss_undefined_reason']='ZERO_REFERENCE_LOSS'
                    else:row['relative_loss_percent']=100*(a['mean_loss']/b['mean_loss']-1)
            contrasts.append(row)
    return contrasts


def write_csv(path,rows):
    sealed.no_symlinks(path);keys=list(dict.fromkeys(k for row in rows for k in row))
    with open(path,'x',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=keys);writer.writeheader()
        for row in rows:writer.writerow({k:(json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else ('NA' if v is None else v)) for k,v in row.items()})


def summarize(manifest_path):
    manifest=read_json(manifest_path);formal=Path(manifest['formal_directory'])
    termination=read_json(formal/'study-termination.json')
    if not termination.get('all_workers_terminated'):raise DriverStop('STUDY_NOT_TERMINATED')
    verify_seal(manifest)
    from v8_daily_fx import classify_against_f
    rows=read_json(formal/'inventory.json');design=manifest['design'];contrasts=make_contrasts(rows,design)
    classification={method:classify_against_f(rows,method,design) for method in ('QR33','QR4')}
    result=dict(design_id=manifest['design_id'],cells=rows,contrasts=contrasts,classifications=classification,
        study_status=termination['status'],source_consistency=termination.get('source_consistency'),
        summarized_utc=utc_now(),source_inventory_sha256=sha_file(formal/'inventory.json'),
        descriptive_only=True,new_statistical_tests=False,causal_boundary=design['predeclared_interpretation']['causal_boundary'])
    exclusive_json(formal/'summary.json',result)
    write_csv(formal/'summary.csv',rows);write_csv(formal/'contrasts.csv',contrasts)
    exclusive_json(formal/'classification.json',classification)
    print(json.dumps(dict(event='summary_written',status='COMPLETE',method_slots=len(rows),contrasts=len(contrasts))),flush=True)
    return 0


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run',action='store_true');mode.add_argument('--worker',action='store_true');mode.add_argument('--summarize',action='store_true')
    parser.add_argument('--window',type=int);parser.add_argument('--horizon',type=int)
    parser.add_argument('--global-deadline',type=float);parser.add_argument('--manifest',type=Path,default=FORMAL/'manifest.json')
    args=parser.parse_args(argv)
    try:
        if args.run:return run_study()
        if args.summarize:return summarize(args.manifest)
        if any(x is None for x in (args.window,args.horizon,args.global_deadline)) or not math.isfinite(args.global_deadline):
            parser.error('--worker requires window, horizon and finite global-deadline')
        return run_worker(args)
    except (DriverStop,OSError,ValueError,KeyError) as exc:
        print(json.dumps(dict(event='driver_stopped',status='FAILED',reason=exc.code if isinstance(exc,DriverStop) else type(exc).__name__)),flush=True)
        return 2


if __name__=='__main__':raise SystemExit(main())
