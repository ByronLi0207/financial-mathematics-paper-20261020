"""One prospective, resource-bounded WP3 run; the parent imports only stdlib.

--run creates the sole new formal output directory and immutable manifest.
--worker is an internal one-repetition/phi/p entry point. --summarize reads
completed receipts after study termination, never simulates or refits anything.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
import math
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
DESIGN_COMMIT = '039f6f1'
PROTOCOL_FILES = ('protocol/revision-v8/wp3-mechanism-design.md',
                  'protocol/revision-v8/wp3-mechanism-design.json')
CODE_FILES = ('conditional_features.py', 'conditional_quantile.py',
              'conditional_study.py', 'study_core.py', 'parsimonious_v3.py',
              'v8_mechanism_mc.py', 'run_v8_wp3.py', 'run_study.py',
              'test_v8_wp3_core.py', 'test_v8_wp3_summary.py', 'test_v8_wp3_driver.py')
THREAD_NAMES = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
                'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS',
                'NUMBA_NUM_THREADS')
FORMAL = ROOT / 'results/revision-v8/wp3'
PRIVATE = ROOT / '.scratch/revision-v8/wp3'
METHODS = ('F', 'QR33', 'QR4')


class DriverStop(Exception):
    def __init__(self, code):
        self.code = str(code)
        super().__init__(self.code)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')


def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def no_symlinks(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise DriverStop('OUTPUT_SYMLINK')


def exclusive_json(path, value):
    path = Path(path); no_symlinks(path)
    data = (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as out:
        out.write(data)
        out.flush(); os.fsync(out.fileno())


def append_status(path, **record):
    """Progress only: scientific loss values never go into status logs."""
    allowed = {'event', 'unit_id', 'status', 'reason', 'window', 'horizon', 'method', 'pid'}
    if set(record) - allowed:
        raise DriverStop('INVALID_STATUS_FIELDS')
    no_symlinks(path)
    with open(path, 'a', encoding='utf-8') as out:
        out.write(json.dumps(dict(utc=utc_now(), **record), allow_nan=False) + '\n')


def create_run_directories(formal, private):
    formal, private = Path(formal), Path(private)
    no_symlinks(formal); no_symlinks(private)
    formal.parent.mkdir(parents=True, exist_ok=True)
    formal.mkdir(mode=0o700, exist_ok=False)
    private.mkdir(mode=0o700, parents=True, exist_ok=False)
    (formal/'units').mkdir(mode=0o700)


def verify_design(root=ROOT):
    """Compare current bytes with the pre-result commit, not a mutable digest."""
    root = Path(root); hashes = {}
    try:
        commit = subprocess.run(['git','rev-parse',DESIGN_COMMIT+'^{commit}'],
            cwd=root, capture_output=True, text=True, check=True).stdout.strip()
        for name in PROTOCOL_FILES:
            frozen = subprocess.run(['git','show',commit+':'+name], cwd=root,
                capture_output=True, check=True).stdout
            current = (root/name).read_bytes()
            if current != frozen:
                raise DriverStop('DESIGN_COMMIT_MISMATCH')
            hashes[name] = hashlib.sha256(current).hexdigest()
        design = json.loads((root/PROTOCOL_FILES[1]).read_text())
        for name, digest in design['original_modules_sha256'].items():
            if sha_file(root/name) != digest:
                raise DriverStop('ORIGINAL_MODULE_HASH_MISMATCH')
    except (OSError, subprocess.SubprocessError, ValueError, KeyError) as exc:
        raise DriverStop('DESIGN_UNVERIFIED') from exc
    return design, commit, hashes


def verify_seal(manifest, root=ROOT):
    try:
        for kind in ('code_hashes', 'protocol_hashes'):
            for name, digest in manifest[kind].items():
                if sha_file(Path(root)/name) != digest:
                    raise DriverStop('SEALED_HASH_MISMATCH')
    except (OSError, KeyError, TypeError) as exc:
        raise DriverStop('SEALED_HASH_UNVERIFIED') from exc


def planned_units(design):
    for rep in range(design['repetitions']):
        for pi, phi in enumerate(design['phi']):
            for gi, persistence in enumerate(design['variance_persistence']):
                yield dict(unit_id=f'rep-{rep:03d}_phi-{pi}_p-{gi}', rep=rep,
                    phi_index=pi, p_index=gi, phi=phi, variance_persistence=persistence)


def method_path(public, window, horizon, method, *, started=False):
    return Path(public)/f'W{window}_H{horizon}_{method}{".started" if started else ""}.json'


def candidate_path(public, window, horizon, method, index):
    return Path(public)/f'W{window}_H{horizon}_{method}_validation-{index}.json'


def selection_path(public,window,horizon,method):
    return Path(public)/f'W{window}_H{horizon}_{method}.selection.json'


def read_json(path):
    return json.loads(Path(path).read_text())


def candidate_inventory(design, public, window, horizon, method):
    rows = []
    for i, penalty in enumerate(design['menus'].get(method, [])):
        path = candidate_path(public,window,horizon,method,i)
        if path.exists():
            try:
                row = read_json(path)
                if row.get('penalty') != penalty or row.get('status') not in ('COMPLETE','FAILED','INCOMPLETE'):
                    raise ValueError('candidate receipt')
            except (OSError,ValueError,TypeError):
                row = dict(penalty=penalty,status='FAILED',reason='INVALID_CANDIDATE_RECEIPT')
        else:
            row = dict(penalty=penalty,status='NOT_ATTEMPTED',reason='CANDIDATE_NOT_REACHED')
        rows.append(row)
    return rows


def build_inventory(design, formal):
    rows = []
    for unit in planned_units(design):
        public = Path(formal)/'units'/unit['unit_id']
        for window in design['windows']:
            for horizon in design['horizons']:
                for method in METHODS:
                    row = dict(unit,window=window,horizon=horizon,method=method,
                        status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',evaluation=None,
                        selected_penalty=None,candidates=candidate_inventory(design,public,window,horizon,method))
                    path = method_path(public,window,horizon,method)
                    if path.exists():
                        try:
                            report = read_json(path)
                            if report.get('status') not in ('COMPLETE','FAILED'):
                                raise ValueError('method receipt')
                            if report['status']=='COMPLETE':
                                e = report['evaluation']
                                if (type(e['n']) is not int or e['n']!=design['evaluation_last']-design['evaluation_first']+1
                                        or type(e['strict_breach_count']) is not int
                                        or not 0<=e['strict_breach_count']<=e['n']
                                        or not math.isfinite(e['mean_loss']) or e['mean_loss']<0
                                        or e['strict_breach_rate']!=e['strict_breach_count']/e['n']):
                                    raise ValueError('invalid complete score')
                            # Frozen identity comes from planned inventory, never a receipt.
                            for key in ('status','reason','evaluation','selected_penalty','candidates','fit_diagnostics','maturity'):
                                if key in report: row[key]=report[key]
                        except (OSError,ValueError,KeyError,TypeError):
                            row.update(status='FAILED',reason='INVALID_METHOD_RECEIPT',evaluation=None)
                    elif method_path(public,window,horizon,method,started=True).exists():
                        row.update(status='FAILED',reason='INTERRUPTED_METHOD')
                        selected=selection_path(public,window,horizon,method)
                        if selected.exists():
                            try:
                                selection=read_json(selected)
                                penalty=selection.get('penalty')
                                if penalty is not None and penalty not in design['menus'][method]:
                                    raise ValueError('selection penalty')
                                row['selected_penalty']=penalty
                            except (OSError,ValueError,KeyError,TypeError):
                                row['reason']='INVALID_SELECTION_RECEIPT'
                    rows.append(row)
    return rows


class ResourceCheckpoint:
    """Always check both clocks; throttle only the expensive actual ps probe."""
    def __init__(self, guard, deadline, private_ps_path, *, clock=time.monotonic):
        self.guard, self.deadline, self.path, self.clock = guard, deadline, Path(private_ps_path), clock
        self.last_probe = -math.inf

    def __call__(self, **kwargs):
        now = self.clock()
        if now >= self.deadline:
            raise DriverStop('GLOBAL_DEADLINE')
        self.guard.remaining_seconds()
        stage = kwargs.get('stage')
        if stage not in ('initialization','cell_end','finalization') and now-self.last_probe < .25:
            return
        # forecast_report sends method/issue/iteration; RunGuard does not accept them.
        self.guard(stage=stage)
        self.last_probe = now
        no_symlinks(self.path)
        with open(self.path,'a',encoding='utf-8') as out:
            out.write(json.dumps(dict(utc=utc_now(),monotonic=now,stage=stage,
                thread_snapshot_count=self.guard.resources['thread_snapshot_count'],
                maximum_observed_os_threads=self.guard.resources['maximum_observed_os_threads'],
                peak_rss_bytes=self.guard.resources['peak_rss_bytes']),allow_nan=False)+'\n')


def kill_owned_worker(proc):
    """Only for Popen children created here with start_new_session=True."""
    if proc.poll() is None:
        try: os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError: pass
    proc.wait()


def wait_owned_worker(proc, deadline, *, hard_seconds=600):
    remaining = deadline-time.monotonic()
    if remaining <= 0:
        kill_owned_worker(proc)
        return dict(status='FAILED',reason='GLOBAL_DEADLINE',returncode=proc.returncode)
    try:
        code = proc.wait(timeout=min(float(hard_seconds),remaining))
    except subprocess.TimeoutExpired:
        kill_owned_worker(proc)
        return dict(status='FAILED',reason='GLOBAL_DEADLINE' if remaining<=hard_seconds else 'WORKER_HARD_TIMEOUT',returncode=proc.returncode)
    except BaseException:
        kill_owned_worker(proc)
        raise
    return dict(status='COMPLETE' if code==0 else 'FAILED',reason=None if code==0 else 'WORKER_EXIT',returncode=code)


def software_environment():
    versions = {}
    for name in ('numpy','pytest','scipy'):
        try: versions[name]=metadata.version(name)
        except metadata.PackageNotFoundError: versions[name]=None
    return dict(python=sys.version,executable=sys.executable,platform=platform.platform(),
        machine=platform.machine(),packages=versions,parent_pid=os.getpid(),
        requested_worker_environment={name:'1' for name in THREAD_NAMES},
        inherited_thread_environment={name:os.environ.get(name) for name in THREAD_NAMES})


def run_study():
    start=time.monotonic(); started=utc_now()
    design,commit,protocol_hashes=verify_design()
    code_hashes={name:sha_file(ROOT/name) for name in CODE_FILES}
    run_id=uuid.uuid4().hex
    private=PRIVATE/run_id
    create_run_directories(FORMAL,private)
    deadline=start+design['resources']['total_study_wall_seconds']
    manifest=dict(schema='v8-wp3-driver-1',design_id=design['design_id'],design_commit=commit,
        design_commit_requested=DESIGN_COMMIT,started_utc=started,study_start_monotonic=start,
        global_deadline_monotonic=deadline,clock='time.monotonic same host',run_id=run_id,
        formal_directory=str(FORMAL),private_directory=str(private),protocol_hashes=protocol_hashes,
        code_hashes=code_hashes,environment=software_environment(),design=design,
        planned_worker_count=design['repetitions']*len(design['phi'])*len(design['variance_persistence']),
        planned_method_count=design['repetitions']*72*3,
        no_rng_before_manifest=True)
    manifest_path=FORMAL/'manifest.json'
    exclusive_json(manifest_path,manifest)
    verify_seal(manifest)
    status='COMPLETE'; reason=None; completed=0; attempted=0
    active=None
    try:
        for unit in planned_units(design):
            if time.monotonic()>=deadline:
                status='BUDGET_STOP'; reason='GLOBAL_DEADLINE'; break
            verify_seal(manifest)
            public=FORMAL/'units'/unit['unit_id']; public.mkdir(mode=0o700)
            unit_private=private/unit['unit_id']; unit_private.mkdir(mode=0o700)
            exclusive_json(public/'parent-start.json',dict(unit,started_utc=utc_now(),
                private_ps_path=str(unit_private/'ps-snapshots.jsonl')))
            env=dict(os.environ,**{name:'1' for name in THREAD_NAMES},PYTHONDONTWRITEBYTECODE='1')
            cmd=[sys.executable,str(ROOT/'run_v8_wp3.py'),'--worker','--rep',str(unit['rep']),
                '--phi-index',str(unit['phi_index']),'--p-index',str(unit['p_index']),
                '--global-deadline',repr(deadline),'--manifest',str(manifest_path)]
            append_status(FORMAL/'progress.jsonl',event='worker_start',unit_id=unit['unit_id'],status='STARTED')
            attempted+=1
            with open(public/'process.log','x',encoding='utf-8') as log:
                active=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True)
                receipt=wait_owned_worker(active,deadline,
                    hard_seconds=design['resources']['worker_hard_wall_seconds'])
                active=None
            receipt.update(unit,ended_utc=utc_now())
            exclusive_json(public/'parent-termination.json',receipt)
            verify_seal(manifest)
            completed+=receipt['status']=='COMPLETE'
            append_status(FORMAL/'progress.jsonl',event='worker_end',unit_id=unit['unit_id'],status=receipt['status'],reason=receipt['reason'])
            worker_receipt=public/'worker-receipt.json'
            if (receipt['returncode']==2
                    or worker_receipt.exists() and read_json(worker_receipt).get('technical_error')
                    or receipt['reason']=='WORKER_EXIT' and not worker_receipt.exists()
                        and receipt['returncode']!=-signal.SIGALRM):
                status='TECHNICAL_ERROR';reason='WORKER_TECHNICAL_ERROR';break
            if receipt['reason']=='GLOBAL_DEADLINE':
                status='BUDGET_STOP';reason='GLOBAL_DEADLINE';break
    except KeyboardInterrupt:
        status='INTERRUPTED'; reason='PARENT_INTERRUPTED'
    except Exception as exc:
        status='TECHNICAL_ERROR';reason=exc.code if isinstance(exc,DriverStop) else 'PARENT_TECHNICAL_ERROR'
    finally:
        if active is not None: kill_owned_worker(active)
        seal_status='PASS'
        try: verify_seal(manifest)
        except DriverStop as exc:
            seal_status=exc.code;status='TECHNICAL_ERROR';reason=exc.code
        inventory=build_inventory(design,FORMAL)
        exclusive_json(FORMAL/'inventory.json',inventory)
        exclusive_json(FORMAL/'study-termination.json',dict(status=status,reason=reason,
            started_utc=started,ended_utc=utc_now(),elapsed_seconds=time.monotonic()-start,
            global_deadline_monotonic=deadline,attempted_workers=attempted,completed_workers=completed,
            planned_workers=manifest['planned_worker_count'],all_workers_terminated=True,
            code_hash_check=seal_status,method_status_counts=dict(Counter(r['status'] for r in inventory))))
    print(json.dumps(dict(event='study_terminated',status=status,reason=reason),allow_nan=False),flush=True)
    return 0 if status=='COMPLETE' else 1


def scalar_diagnostics(rows):
    """Copy only finite numeric scalar fit and maturity diagnostics."""
    output=[]
    for row in rows:
        clean={}
        for key,value in row.items():
            if value is None or type(value) in (str,bool):
                clean[key]=value
            elif isinstance(value,(int,float)):
                if not math.isfinite(value): raise ValueError('nonfinite diagnostic')
                clean[key]=value
            else:
                # Core uses Python scalar fields; scalar NumPy values support item().
                item=getattr(value,'item',None)
                if item is None: raise ValueError('nonscalar diagnostic')
                scalar=item()
                if type(scalar) not in (int,float) or not math.isfinite(scalar):
                    raise ValueError('nonfinite or nonscalar diagnostic')
                clean[key]=scalar
        output.append(clean)
    return output


def maturity_summary(diagnostics):
    if not diagnostics: return None
    return dict(refit_count=len(diagnostics),
        training_first_origin_min=min(d['training_first_origin'] for d in diagnostics),
        training_last_origin_max=max(d['training_last_origin'] for d in diagnostics),
        latest_label_end_max=max(d['latest_label_end'] for d in diagnostics),
        maximum_label_end_minus_refit=max(d['latest_label_end']-d['refit_index'] for d in diagnostics))


def evaluate_method(design,public,window,horizon,method,report,checkpoint,fit_error,resource_errors):
    """Run the frozen menu once and its selected evaluation once.

    report accepts a named segment and returns scalar scores/fit diagnostics.
    This boundary can be tested without generating a DGP or fitting a model.
    """
    from v8_mechanism_mc import select_candidate
    checkpoint(stage='method_start')
    exclusive_json(method_path(public,window,horizon,method,started=True),dict(status='STARTED',started_utc=utc_now()))
    row=dict(status='FAILED',reason=None,selected_penalty=None,candidates=[],evaluation=None,
        fit_diagnostics=[],maturity=None)
    def expected_failure(exc):
        if isinstance(exc,fit_error):
            result=dict(reason=exc.code,failure_kind='QUANTILE_FIT_FAILURE')
            try:
                result['failure_diagnostics']=scalar_diagnostics([dict(exc.diagnostics)])[0]
                result['failure_diagnostics_status']='FINITE_SCALARS'
            except ValueError:
                result.update(failure_diagnostics=None,failure_diagnostics_status='NONFINITE_OR_NONSCALAR')
        else:
            result=dict(reason='NUMERIC_OR_STRUCTURAL_FAILURE',failure_kind=type(exc).__name__)
        if hasattr(exc,'wp3_progress'): result['failure_progress']=exc.wp3_progress
        return result
    try:
        if method!='F':
            for index,penalty in enumerate(design['menus'][method]):
                candidate=dict(penalty=penalty,status='FAILED',origin_count=0,mean_loss=None)
                try:
                    score,diagnostics=report('validation',horizon,window,method,penalty)
                    candidate.update(status='COMPLETE',origin_count=score['n'],mean_loss=score['mean_loss'],
                        fit_diagnostics=diagnostics,maturity=maturity_summary(diagnostics))
                except resource_errors as exc:
                    candidate.update(reason=exc.code,failure_kind='RESOURCE_INTERRUPTION')
                    exclusive_json(candidate_path(public,window,horizon,method,index),candidate)
                    raise
                except (fit_error,ValueError,FloatingPointError) as exc:
                    candidate.update(expected_failure(exc))
                except Exception as exc:
                    candidate.update(reason='TECHNICAL_ERROR',exception_type=type(exc).__name__)
                    exclusive_json(candidate_path(public,window,horizon,method,index),candidate)
                    raise
                exclusive_json(candidate_path(public,window,horizon,method,index),candidate)
                row['candidates'].append(candidate)
            expected=design['validation_last']-design['validation_first']+1
            selection=select_candidate(row['candidates'],method,expected,design['menus'])
            exclusive_json(selection_path(public,window,horizon,method),selection)
            if selection['status']!='SELECTED':
                row['reason']='VALIDATION_INELIGIBLE'
            else:
                row['selected_penalty']=selection['penalty']
        if method=='F' or row['selected_penalty'] is not None:
            score,diagnostics=report('evaluation',horizon,window,method,row['selected_penalty'])
            row.update(status='COMPLETE',evaluation=score,fit_diagnostics=diagnostics,maturity=maturity_summary(diagnostics))
    except resource_errors as exc:
        row.update(reason=exc.code,candidates=candidate_inventory(design,public,window,horizon,method))
        exclusive_json(method_path(public,window,horizon,method),row)
        raise
    except (fit_error,ValueError,FloatingPointError) as exc:
        row.update(expected_failure(exc))
    except Exception as exc:
        row.update(reason='TECHNICAL_ERROR',exception_type=type(exc).__name__,
            candidates=candidate_inventory(design,public,window,horizon,method))
        exclusive_json(method_path(public,window,horizon,method),row)
        raise
    exclusive_json(method_path(public,window,horizon,method),row)
    append_status(Path(public)/'progress.jsonl',event='method_end',window=window,horizon=horizon,
        method=method,status=row['status'],reason=row['reason'])
    return row


def run_worker(args):
    # Validate the immutable manifest and clocks before importing any numerical code.
    manifest=read_json(args.manifest); verify_seal(manifest)
    if args.global_deadline!=manifest['global_deadline_monotonic']:
        raise DriverStop('GLOBAL_DEADLINE_MISMATCH')
    design=manifest['design']
    matches=[u for u in planned_units(design) if (u['rep'],u['phi_index'],u['p_index'])==(args.rep,args.phi_index,args.p_index)]
    if len(matches)!=1: raise DriverStop('WORKER_IDENTITY')
    unit=matches[0]; public=Path(manifest['formal_directory'])/'units'/unit['unit_id']
    private=Path(manifest['private_directory'])/unit['unit_id']
    for name in THREAD_NAMES:
        if os.environ.get(name)!='1': raise DriverStop('THREAD_ENVIRONMENT')
    start=time.monotonic(); started=utc_now()
    from run_study import RunGuard, StudyStop, arm_hard_deadline
    remaining=args.global_deadline-time.monotonic()
    if remaining<=0: raise DriverStop('GLOBAL_DEADLINE')
    arm_hard_deadline(min(design['resources']['worker_hard_wall_seconds'],remaining))
    guard=RunGuard(start,started,unit['unit_id'],public,private)
    checkpoint=ResourceCheckpoint(guard,args.global_deadline,private/'ps-snapshots.jsonl')
    receipt=dict(unit,started_utc=started,status='FAILED',reason=None,technical_error=False,
        initial_rng_state=None,final_rng_state=None,resources=None,code_hash_start='PASS',
        private_ps_path=str(private/'ps-snapshots.jsonl'),completed_method_reports=0)
    try:
        checkpoint(stage='initialization')
        import numpy as np
        import v8_mechanism_mc as mc
        from conditional_features import build_features
        from conditional_quantile import QuantileFitError
        from conditional_study import score_predictions
        from study_core import build_label_cache, stable_mean
        checkpoint(stage='initialization')
        z,initial,final=mc.repetition_normals(args.rep,design)
        receipt.update(initial_rng_state=initial,final_rng_state=final,
            numpy_version=np.__version__,rng_normal_count=len(z))
        exclusive_json(public/'rng-receipt.json',dict(rep=args.rep,initial_state=initial,
            final_state=final,normals=len(z),numpy_version=np.__version__,common_random_numbers=design['common_random_numbers']))
        p=unit['variance_persistence']; parameters=design['variance_parameters'][format(p,'g')]
        process=mc.simulate_level_garch(z,unit['phi'],parameters['omega'],parameters['alpha'],parameters['beta'],design['burn_in'])
        position=process['position']
        times=np.datetime64(design['retained_clock_first'])+np.arange(len(position))*np.timedelta64(design['gap_seconds'],'s')
        features=build_features(position,times,short_scale=design['short_rms'],long_scale=design['long_rms'],nominal_gap_seconds=design['gap_seconds'])
        if features.valid_from!=design['feature_valid_from']: raise ValueError('feature validity')
        caches={h:build_label_cache(position,h) for h in design['horizons']}
        guard.arrays(z,process,times,features,caches)
        validation=np.arange(design['validation_first'],design['validation_last']+1,dtype=np.int64)
        evaluation=np.arange(design['evaluation_first'],design['evaluation_last']+1,dtype=np.int64)

        def report(segment,h,w,method,penalty=None):
            origins=validation if segment=='validation' else evaluation
            result=mc.forecast_report(position,times,features,caches[h],origins,h,w,
                design['refit_step'],method,penalty,checkpoint=checkpoint)
            score=score_predictions(caches[h].peak[origins],result['capacity'],np.abs(position[origins]),origins)
            breaches=int(np.count_nonzero(score.strict_breach)); n=len(origins)
            diagnostics=scalar_diagnostics(result['fit_diagnostics'])
            return dict(mean_loss=stable_mean(score.pinball),strict_breach_count=breaches,
                strict_breach_rate=breaches/n,n=n),diagnostics

        for window in design['windows']:
            for horizon in design['horizons']:
                for method in METHODS:
                    evaluate_method(design,public,window,horizon,method,report,checkpoint,
                        QuantileFitError,(DriverStop,StudyStop))
                    receipt['completed_method_reports']+=1
                checkpoint(stage='cell_end')
        checkpoint(stage='finalization')
        receipt['status']='COMPLETE'
    except (DriverStop,StudyStop) as exc:
        receipt.update(reason=exc.code)
    except (ValueError,FloatingPointError) as exc:
        receipt.update(reason='NUMERIC_OR_STRUCTURAL_FAILURE',exception_type=type(exc).__name__)
    except Exception as exc:
        receipt.update(reason='TECHNICAL_ERROR',technical_error=True,exception_type=type(exc).__name__)
    finally:
        try:
            checkpoint(stage='finalization')
        except (DriverStop,StudyStop) as exc:
            receipt.update(status='FAILED',reason=exc.code)
        try: verify_seal(manifest);receipt['code_hash_end']='PASS'
        except DriverStop as exc:
            receipt.update(status='FAILED',reason=exc.code,technical_error=True,code_hash_end=exc.code)
        receipt.update(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-start,resources=guard.resources)
        exclusive_json(public/'worker-receipt.json',receipt)
        signal.setitimer(signal.ITIMER_REAL,0)
    return 2 if receipt['technical_error'] else (0 if receipt['status']=='COMPLETE' else 1)


def aggregate_inventory(design,inventory):
    from v8_mechanism_mc import summary_from_repetitions
    indexed={ (r['rep'],r['phi_index'],r['p_index'],r['window'],r['horizon'],r['method']):r for r in inventory }
    summaries=[]
    for pi,phi in enumerate(design['phi']):
        for gi,p in enumerate(design['variance_persistence']):
            for window in design['windows']:
                for horizon in design['horizons']:
                    for method in METHODS:
                        pairs=[];reasons=Counter(); method_counts=Counter()
                        for rep in range(design['repetitions']):
                            model=indexed[(rep,pi,gi,window,horizon,method)]
                            reference=indexed[(rep,pi,gi,window,horizon,'F')]
                            method_counts[model['status']]+=1
                            pair=dict(rep=rep,status='COMPLETE')
                            if model['status']=='COMPLETE' and reference['status']=='COMPLETE':
                                pair.update(model_loss=model['evaluation']['mean_loss'],reference_loss=reference['evaluation']['mean_loss'],
                                    model_breach_rate=model['evaluation']['strict_breach_rate'],reference_breach_rate=reference['evaluation']['strict_breach_rate'])
                            else:
                                missing=[r for r in (model,reference) if r['status']!='COMPLETE']
                                pair['status']='FAILED' if any(r['status']=='FAILED' for r in missing) else 'NOT_ATTEMPTED'
                                # F paired with itself is counted once.
                                seen=set()
                                for r in missing:
                                    key=(r['method'],r.get('reason') or r['status'])
                                    if key not in seen:
                                        reasons[key[1]]+=1;seen.add(key)
                            pairs.append(pair)
                        summary=summary_from_repetitions(pairs,design['repetitions'])
                        summary.update(phi=phi,phi_index=pi,variance_persistence=p,p_index=gi,
                            window=window,horizon=horizon,method=method,failure_reasons=dict(reasons),
                            method_status_counts=dict(method_counts),reference_method='F',
                            comparison='paired_self_reference' if method=='F' else 'paired_same_cell_and_repetition_F')
                        summaries.append(summary)
    return summaries


def support_for_method(summaries,method):
    rows=[r for r in summaries if r['method']==method]
    identity_keys=('phi','variance_persistence','window','horizon')
    def identity(row):
        return {key:row[key] for key in identity_keys}
    expected_grid={(phi,p,w,h) for phi in (.7,.9,.98) for p in (0.,.9,.98)
                   for w in (52,260,720,2880) for h in (6,24)}
    actual_grid=[tuple(row[key] for key in identity_keys) for row in rows]
    grid_complete=len(actual_grid)==72 and set(actual_grid)==expected_grid
    absent=expected_grid-set(actual_grid)
    target=[];outside=[];missing=[];clear_target=[];clear_outside=[]
    unknown_target=0;unknown_outside=0
    for row in rows:
        is_target=row['horizon']==6 and row['window']>=720 and row['variance_persistence']>=.9
        (target if is_target else outside).append(row)
        evaluable=(row['planned_repetitions']==32 and row['complete_repetitions']==32
            and row['full_procedure_status']=='COMPLETE'
            and all(row.get(k) is not None and math.isfinite(row[k]) for k in ('relative_loss_percent','relative_loss_mcse','win_fraction')))
        if not evaluable:
            missing.append(identity(row))
            if is_target:unknown_target+=1
            else:unknown_outside+=1
            continue
        if row['relative_loss_percent']+2*row['relative_loss_mcse']<0 and row['win_fraction']>=.75:
            (clear_target if is_target else clear_outside).append(identity(row))
    missing.extend(dict(zip(identity_keys,key)) for key in sorted(absent))
    if clear_outside: status='MISMATCH'
    elif not grid_complete or unknown_outside: status='INCONCLUSIVE'
    elif len(clear_target)>=6: status='SUPPORTED'
    elif len(clear_target)+unknown_target<6:status='NOT_SUPPORTED'
    else:status='INCONCLUSIVE'
    return dict(method=method,status=status,planned_cells=72,reported_cells=len(rows),
        target_cell_count=len(target),outside_cell_count=len(outside),minimum_target_clear_gains=6,
        target_clear_gain_count=len(clear_target),outside_clear_gain_count=len(clear_outside),
        target_clear_gain_cells=clear_target,outside_clear_gain_cells=clear_outside,
        missing_or_unevaluable_cells=missing,all_cells_fully_evaluable=not missing and grid_complete,
        grid_complete=grid_complete,unevaluable_target_cells=unknown_target,
        unevaluable_outside_cells=unknown_outside,
        criterion='all32complete; relative_loss_percent+2*relative_loss_mcse<0; win_fraction>=0.75',
        target_region='H=6,W>=720,p>=0.9',inferential_status='descriptive predeclared screen; no FWE guarantee')


def summarize(manifest_path):
    manifest=read_json(manifest_path); formal=Path(manifest['formal_directory'])
    termination=read_json(formal/'study-termination.json')
    if not termination.get('all_workers_terminated'):
        raise DriverStop('STUDY_NOT_TERMINATED')
    verify_seal(manifest)
    inventory=read_json(formal/'inventory.json')
    summaries=aggregate_inventory(manifest['design'],inventory)
    support={m:support_for_method(summaries,m) for m in ('QR33','QR4')}
    statuses=[v['status'] for v in support.values()]
    broad='MISMATCH' if 'MISMATCH' in statuses else ('INCONCLUSIVE' if 'INCONCLUSIVE' in statuses else ('SUPPORTED' if all(s=='SUPPORTED' for s in statuses) else 'NOT_SUPPORTED'))
    exclusive_json(formal/'summary.json',dict(design_id=manifest['design_id'],summarized_utc=utc_now(),
        study_status=termination['status'],cells=summaries,unit_of_uncertainty='independent repetition',
        incomplete_full_procedure_cells='NA; available pairs conditional on completion',
        source_inventory_sha256=sha_file(formal/'inventory.json')))
    path=formal/'summary.csv';no_symlinks(path)
    keys=list(dict.fromkeys(k for r in summaries for k in r))
    with open(path,'x',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=keys);writer.writeheader()
        for row in summaries:
            writer.writerow({k:(json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else ('NA' if v is None else v)) for k,v in row.items()})
    exclusive_json(formal/'support.json',dict(procedures=support,broad_conditional_models_restriction=broad,
        descriptive_only=True,multiple_comparison_adjusted=False,screen=manifest['design']['support_screen']))
    print(json.dumps(dict(event='summary_written',status='COMPLETE',cells=len(summaries)),allow_nan=False))
    return 0


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run',action='store_true');mode.add_argument('--worker',action='store_true')
    mode.add_argument('--summarize',action='store_true')
    parser.add_argument('--rep',type=int);parser.add_argument('--phi-index',type=int)
    parser.add_argument('--p-index',type=int);parser.add_argument('--global-deadline',type=float)
    parser.add_argument('--manifest',type=Path,default=FORMAL/'manifest.json')
    args=parser.parse_args(argv)
    try:
        if args.run:return run_study()
        if args.summarize:return summarize(args.manifest)
        if any(v is None for v in (args.rep,args.phi_index,args.p_index,args.global_deadline)) or not math.isfinite(args.global_deadline):
            parser.error('--worker requires rep, phi-index, p-index and finite global-deadline')
        return run_worker(args)
    except (DriverStop,OSError,ValueError,KeyError) as exc:
        print(json.dumps(dict(event='driver_stopped',status='FAILED',reason=exc.code if isinstance(exc,DriverStop) else type(exc).__name__)),flush=True)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
