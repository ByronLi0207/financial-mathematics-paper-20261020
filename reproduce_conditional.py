"""Verify the published archive, or explicitly replicate its frozen experiment.

Default verification needs only Python's standard library, reads no raw data,
creates no files and does not recompute accuracy. Replication requires Darwin,
existing NumPy and both exact private source files at their fixed local paths.
It retains a new attempt, runs one worker at a time under a total 540-second
deadline, and never repairs sources, replaces the archive or changes parameters.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
FREEZE = 'e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb'
SELECTION = '531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7'
FREEZE_PATH = 'protocol/revision-20261022/executable-freeze.json'
SELECTION_PATH = 'protocol/revision-20261022/selection-freeze.json'
SPEC_PATH = 'protocol/revision-20261022/study-spec.json'
RESULTS = 'results/revision-20261022'
PUBLISHED_COMMIT = 'b5fa5db8d67341240ae99dda4b88b33dddeb71e3'
THREAD_NAMES = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
                'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
CODE_FILES = (
    'conditional_quantile.py', 'test_conditional_quantile.py',
    'conditional_features.py', 'test_conditional_features.py',
    'conditional_study.py', 'test_conditional_study.py',
    'conditional_sources.py', 'test_conditional_sources.py',
    'run_conditional_study.py', 'test_run_conditional_study.py',
    'study_core.py', 'test_core.py', 'run_study.py', 'test_runner.py',
    SPEC_PATH, 'protocol/revision-20261022/conditional-baseline-design.md')


class ReproductionError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ArchiveContract:
    executable_sha256: str
    selection_sha256: str
    code_files: tuple
    result_files: dict
    freeze_path: str = FREEZE_PATH
    selection_path: str = SELECTION_PATH
    spec_path: str = SPEC_PATH


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ReproductionError('JSON_DUPLICATE_KEY')
            result[key] = value
        return result
    try:
        value = json.loads(raw, object_pairs_hook=pairs,
            parse_constant=lambda _: (_ for _ in ()).throw(ReproductionError('JSON_NONFINITE')))
        if type(value) is not dict:
            raise ReproductionError('JSON_OBJECT_REQUIRED')
        return value
    except (json.JSONDecodeError, UnicodeError, TypeError):
        raise ReproductionError('JSON_INVALID') from None


def project_file(root, relative, *, within=None):
    root = Path(root).absolute()
    relative = Path(relative)
    path = relative if relative.is_absolute() else root / relative
    boundary = root if within is None else Path(within).absolute()
    if '..' in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise ReproductionError('FILE_INTEGRITY')
    try:
        path.relative_to(root); path.relative_to(boundary)
    except ValueError:
        raise ReproductionError('FILE_INTEGRITY') from None
    if not path.is_file():
        raise ReproductionError('FILE_INTEGRITY')
    return path


def read_bytes(root, relative, *, cap=8*1024*1024, within=None):
    try:
        path = project_file(root, relative, within=within)
        if path.stat().st_size > cap:
            raise ReproductionError('FILE_SIZE')
        with path.open('rb') as stream:
            raw = stream.read(cap+1)
        if len(raw) > cap:
            raise ReproductionError('FILE_SIZE')
        return raw
    except OSError:
        raise ReproductionError('FILE_INTEGRITY') from None


def inventory(spec):
    return [(s,h,w,f) for s,c in spec['sources'].items()
            for h in spec['horizons'] for w in c['windows'] for f in spec['families']]


def public_validation_name(key):
    s,h,w,f=key
    return f'{RESULTS}/validation-{s}-h{h}-w{w}-{f}.json'


def historical_validation_name(key):
    s,h,w,f=key
    return f'.scratch/revision-20261022/val-{s}-h{h}-w{w}-{f}-01/public/manifest.json'


def origin_identity(first,last):
    values=range(first,last+1)
    return dict(count=last-first+1,first=first,last=last,
        sha256=sha(b''.join(i.to_bytes(8,'little',signed=True) for i in values)))


def validation_choice(receipt,spec,key,freeze_hash):
    """Recompute frozen selection using scalars, without importing NumPy."""
    try:
        s,h,w,f=key;cfg=spec['sources'][s]
        if (type(receipt.get('version')) is not int or receipt['version']!=1
                or tuple(receipt.get(n) for n in ('source','horizon','window','family'))!=key
                or receipt.get('phase')!='validation'
                or receipt.get('executable_freeze_sha256')!=freeze_hash
                or receipt.get('selection_freeze_sha256') is not None
                or receipt.get('status') not in ('COMPLETE','INELIGIBLE','STOPPED')):
            raise ReproductionError('VALIDATION_RECEIPT')
        identity=receipt['source_identity']
        if any(identity.get(n)!=cfg[n] for n in ('sha256','bytes','record_count','native_unit')):
            raise ReproductionError('SOURCE_IDENTITY')
        resource=receipt['resources'];elapsed=resource['elapsed_seconds']
        if (type(elapsed) not in (int,float) or not math.isfinite(elapsed) or elapsed<=0
                or type(resource['peak_rss_bytes']) is not int or resource['peak_rss_bytes']<=0
                or type(resource['maximum_observed_os_threads']) is not int or resource['maximum_observed_os_threads']<1
                or type(resource['thread_snapshot_count']) is not int or resource['thread_snapshot_count']<1
                or resource['thread_probe_status']!='PASS'):
            raise ReproductionError('VALIDATION_RESOURCES')
        if receipt['status']!='STOPPED' and (elapsed>=540 or resource['peak_rss_bytes']>=1610612736
                or resource['maximum_observed_os_threads']>2):
            raise ReproductionError('VALIDATION_RESOURCES')
        result=receipt['result'];first=cfg['validation_origin_first'];last=cfg['validation_origin_last']
        if result['origin_identity']!=origin_identity(first,last):
            raise ReproductionError('VALIDATION_ORIGINS')
        candidates=spec['qr_penalties'] if f=='QR' else cfg['knn_candidates'][str(w)]
        rows=result['candidate_rows']
        if type(rows) is not list or [r['parameter'] for r in rows]!=candidates:
            raise ReproductionError('VALIDATION_CANDIDATES')
        for row in rows:
            if row['status'] not in ('COMPLETE','FAILED','INCOMPLETE'):
                raise ReproductionError('VALIDATION_CANDIDATES')
            loss=row.get('mean_pinball')
            if row['status']=='COMPLETE':
                if (type(loss) not in (int,float) or not math.isfinite(loss) or loss<0
                        or type(row['origin_count']) is not int or row['origin_count']!=last-first+1):
                    raise ReproductionError('VALIDATION_CANDIDATES')
            elif loss is not None:
                raise ReproductionError('VALIDATION_CANDIDATES')
        if any(r['status']=='INCOMPLETE' for r in rows) and (
                receipt['status']!='STOPPED' or not receipt.get('stop_code')):
            raise ReproductionError('VALIDATION_TERMINAL')
        chosen=(dict(status='INELIGIBLE',parameter=None) if any(r['status']!='COMPLETE' for r in rows)
            else dict(status='SELECTED',parameter=min(rows,key=lambda r:(r['mean_pinball'],-r['parameter']))['parameter']))
        if (chosen['status']=='SELECTED') != (receipt['status']=='COMPLETE'):
            raise ReproductionError('VALIDATION_TERMINAL')
        return chosen
    except (KeyError,TypeError,OverflowError):
        raise ReproductionError('VALIDATION_RECEIPT') from None


def verify_selection(selection,spec,freeze_hash,lookup):
    """Validate the whole selection; lookup returns exact receipt bytes."""
    try:
        if (set(selection)!={'version','status','created_utc','executable_freeze_sha256','cells'}
                or type(selection['version']) is not int or selection['version']!=1
                or selection['status']!='FROZEN' or selection['executable_freeze_sha256']!=freeze_hash):
            raise ReproductionError('SELECTION_INTEGRITY')
        _utc(selection['created_utc'])
        wanted=inventory(spec);cells=selection['cells']
        if [(c['source'],c['horizon'],c['window'],c['family']) for c in cells]!=wanted:
            raise ReproductionError('SELECTION_INVENTORY')
        for cell,key in zip(cells,wanted):
            if set(cell)!={'source','horizon','window','family','status','parameter','validation_receipts'}:
                raise ReproductionError('SELECTION_INTEGRITY')
            refs=cell['validation_receipts']
            if type(refs) is not list or len(refs)!=1 or set(refs[0])!={'path','sha256'}:
                raise ReproductionError('SELECTION_INTEGRITY')
            reference=refs[0];raw=lookup(reference['path'],key)
            if sha(raw)!=reference['sha256']:
                raise ReproductionError('SELECTION_RECEIPT_HASH')
            chosen=validation_choice(strict_json(raw),spec,key,freeze_hash)
            if chosen!={n:cell[n] for n in ('status','parameter')}:
                raise ReproductionError('SELECTION_CHOICE')
        return selection
    except (KeyError,TypeError):
        raise ReproductionError('SELECTION_INTEGRITY') from None


def _utc(value):
    try:
        if type(value) is not str or not value.endswith('Z'):
            raise ValueError()
        datetime.fromisoformat(value[:-1]+'+00:00')
    except ValueError:
        raise ReproductionError('UTC_METADATA') from None


def verify_archive(root,*,contract=None):
    """Read-only archive integrity and original scalar selection verification."""
    contract=PRODUCTION_CONTRACT if contract is None else contract
    freeze_raw=read_bytes(root,contract.freeze_path)
    if sha(freeze_raw)!=contract.executable_sha256:
        raise ReproductionError('EXECUTABLE_FREEZE_HASH')
    freeze=strict_json(freeze_raw)
    if (set(freeze)!={'version','status','created_utc','files','sources'} or freeze['version']!=1
            or freeze['status']!='FROZEN' or set(freeze['files'])!=set(contract.code_files)):
        raise ReproductionError('EXECUTABLE_FREEZE_INVENTORY')
    _utc(freeze['created_utc'])
    for name,expected in freeze['files'].items():
        if sha(read_bytes(root,name))!=expected:
            raise ReproductionError('EXECUTABLE_FILE_HASH')
    spec=strict_json(read_bytes(root,contract.spec_path))
    if freeze['sources']!={s:{n:c[n] for n in ('sha256','bytes')} for s,c in spec['sources'].items()}:
        raise ReproductionError('SPEC_SOURCE_IDENTITY')
    archived={}
    for path,(size,expected) in contract.result_files.items():
        raw=read_bytes(root,path)
        if len(raw)!=size or sha(raw)!=expected:
            raise ReproductionError('ARCHIVED_RESULT_HASH')
        archived[path]=raw
    raw=read_bytes(root,contract.selection_path)
    if sha(raw)!=contract.selection_sha256:
        raise ReproductionError('SELECTION_FREEZE_HASH')
    selection=strict_json(raw)
    def lookup(path,key):
        if path!=historical_validation_name(key):
            raise ReproductionError('ARCHIVED_RECEIPT_PATH')
        try:return archived[public_validation_name(key)]
        except KeyError:raise ReproductionError('ARCHIVED_RECEIPT_MISSING') from None
    verify_selection(selection,spec,contract.executable_sha256,lookup)
    return dict(status='ARCHIVE_VERIFIED',accuracy_recomputed=False,raw_sources_read=False,
        published_result_commit=PUBLISHED_COMMIT,verified_result_files=len(archived),
        executable_freeze_sha256=contract.executable_sha256,selection_freeze_sha256=contract.selection_sha256,
        spec=spec,selection=selection)


def replication_preflight(root,archive):
    """Fail closed on unsupported platforms and source versions, before writing."""
    if platform.system()!='Darwin':
        raise ReproductionError('DARWIN_REQUIRED')
    if importlib.util.find_spec('numpy') is None:
        raise ReproductionError('NUMPY_REQUIRED_NO_INSTALL')
    for cfg in archive['spec']['sources'].values():
        raw=read_bytes(root,cfg['input_relative_path'],cap=25*1024*1024)
        if len(raw)!=cfg['bytes'] or sha(raw)!=cfg['sha256']:
            raise ReproductionError('RAW_SOURCE_VERSION')


def json_bytes(value):
    return (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()


def write_json(path,value,*,exclusive=False):
    raw=json_bytes(value)
    if exclusive:
        with Path(path).open('xb') as stream:stream.write(raw)
    else:
        # Only the exclusively owned new attempt is mutable.
        temp=Path(path).with_suffix(Path(path).suffix+'.new')
        with temp.open('xb') as stream:stream.write(raw)
        os.replace(temp,path)


def phase_jobs(spec,phase):
    if phase!='references':return [(phase,*key) for key in inventory(spec)]
    return [(phase,s,h,w,None) for s,c in spec['sources'].items()
            for h in spec['horizons'] for w in c['windows']]


def worker_directory(attempt,job):
    phase,s,h,w,f=job
    return attempt/(f'{phase}-{s}-h{h}-w{w}'+('' if f is None else '-'+f))


@contextmanager
def controller_deadline(started,*,clock=time.monotonic):
    """Bound controller/audit work as well as child waits by one total deadline."""
    remaining=540.-(clock()-started)
    if remaining<=0:raise ReproductionError('GLOBAL_DEADLINE')
    previous=signal.getsignal(signal.SIGALRM)
    def expired(signum,frame):raise ReproductionError('GLOBAL_DEADLINE')
    signal.signal(signal.SIGALRM,expired)
    signal.setitimer(signal.ITIMER_REAL,remaining)
    try:yield
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,previous)


def subprocess_worker(root):
    """Make one synchronous child runner, killed with its process group on timeout."""
    def run(job,attempt,selection,remaining):
        phase,s,h,w,f=job
        command=[sys.executable,'-B',str(Path(root)/'run_conditional_study.py'),
            '--phase',phase,'--source',s,'--horizon',str(h),'--window',str(w),
            '--attempt-dir',str(attempt),'--freeze-sha256',FREEZE]
        if f is not None:command+=['--family',f]
        if phase=='evaluation':command+=['--selection-freeze',str(selection[0]),'--selection-sha256',selection[1]]
        environment=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
        environment.update({name:'1' for name in THREAD_NAMES})
        logs=attempt.parent/'controller-private'
        out=logs/(attempt.name+'.stdout');err=logs/(attempt.name+'.stderr')
        with out.open('xb') as stdout,err.open('xb') as stderr:
            child=subprocess.Popen(command,cwd=root,env=environment,stdout=stdout,stderr=stderr,start_new_session=True)
            try:return dict(exit_code=child.wait(timeout=remaining),timed_out=False)
            except subprocess.TimeoutExpired:
                try:os.killpg(child.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                child.wait()
                return dict(exit_code=child.returncode,timed_out=True)
            except BaseException:
                if child.poll() is None:
                    try:os.killpg(child.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                child.wait()
                raise
    return run


def run_plan(root,tag,archive,*,worker=None,clock=time.monotonic,started=None,budget=540.,reconcile=None):
    """Execute a serial plan; injectable worker/clock are for synthetic tests.

    A completed phase queue is deliberately distinct from a numerical audit.
    The command line supplies only the fixed production contract and worker.
    """
    if type(tag) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',tag) is None:
        raise ReproductionError('UNSAFE_ATTEMPT_ID')
    root=Path(root).absolute();base=root/'.scratch/revision-20261022'
    if any(p.is_symlink() for p in (base,*base.parents)):
        raise ReproductionError('FILE_INTEGRITY')
    attempt=base/('replication-'+tag)
    base.mkdir(parents=True,exist_ok=True)
    try:attempt.mkdir()
    except FileExistsError:raise ReproductionError('ATTEMPT_EXISTS') from None
    (attempt/'controller-private').mkdir()
    started=clock() if started is None else started
    worker=subprocess_worker(root) if worker is None else worker
    spec=archive['spec'];freeze_hash=archive['executable_freeze_sha256']
    validation=[];evaluation=[];selection=None
    report=dict(version=1,status='RUNNING',started_utc=utc_now(),
        executable_freeze_sha256=freeze_hash,archived_selection_sha256=archive['selection_freeze_sha256'],
        attempt_path=str(attempt.relative_to(root)),stop_code=None,accuracy_recomputed=False,
        selection_agrees_with_archive=False,completed_validation_cells=0,completed_evaluation_reference_cells=0)
    report['controller_runtime']=dict(python_version=platform.python_version(),
        platform_system=platform.system(),machine=platform.machine())
    queue_path=attempt/'evaluation-queue.json';val_path=attempt/'validation-queue.json'
    report['queue_path']=str(queue_path.relative_to(root))
    write_json(attempt/'controller-start.json',report,exclusive=True)
    def checkpoint():
        remaining=budget-(clock()-started)
        if remaining<=0:raise ReproductionError('GLOBAL_DEADLINE')
        return remaining
    def invoke(job,rows,path):
        remaining=checkpoint();directory=worker_directory(attempt,job)
        worker_error=None
        try:outcome=worker(job,directory,selection,remaining)
        except Exception as error:
            worker_error=getattr(error,'code','CONTROLLER_ERROR')
            outcome=dict(exit_code=None,timed_out=worker_error=='GLOBAL_DEADLINE')
        phase,s,h,w,f=job
        row=dict(phase=phase,source=s,horizon=h,window=w,family=f,exit_code=outcome['exit_code'],
            timed_out=outcome['timed_out'],status='NO_TERMINAL_RECEIPT',stop_code=None,
            receipt_path=str((directory/'public/manifest.json').relative_to(root)),receipt_sha256=None)
        if worker_error is not None:row['worker_controller_error']=worker_error
        try:
            raw=read_bytes(root,row['receipt_path'],within=attempt);data=strict_json(raw)
            if (tuple(data.get(n) for n in ('phase','source','horizon','window','family'))!=job
                    or data.get('executable_freeze_sha256')!=freeze_hash
                    or data.get('selection_freeze_sha256')!=(selection[1] if phase=='evaluation' else None)):
                raise ReproductionError('WORKER_RECEIPT_IDENTITY')
            row.update(status=data.get('status'),stop_code=data.get('stop_code'),receipt_sha256=sha(raw))
        except ReproductionError as error:
            row['controller_error']=error.code
        rows.append(row);write_json(path,dict(version=1,cells=rows))
        if worker_error is not None:raise ReproductionError(worker_error)
        if outcome['timed_out']:raise ReproductionError('GLOBAL_DEADLINE')
        checkpoint()
        return row
    try:
        for job in phase_jobs(spec,'validation'):invoke(job,validation,val_path)
        if any(r['exit_code']!=0 or r['status'] not in ('COMPLETE','INELIGIBLE') or r.get('controller_error') for r in validation):
            raise ReproductionError('VALIDATION_INCOMPLETE')
        cells=[]
        for row,key in zip(validation,inventory(spec)):
            raw=read_bytes(root,row['receipt_path'],within=attempt)
            if sha(raw)!=row['receipt_sha256']:raise ReproductionError('VALIDATION_RECEIPT_CHANGED')
            chosen=validation_choice(strict_json(raw),spec,key,freeze_hash)
            s,h,w,f=key
            cells.append(dict(source=s,horizon=h,window=w,family=f,**chosen,
                validation_receipts=[dict(path=row['receipt_path'],sha256=sha(raw))]))
        new_selection=dict(version=1,status='FROZEN',created_utc=utc_now(),executable_freeze_sha256=freeze_hash,cells=cells)
        def lookup(path,key):return read_bytes(root,path,within=attempt)
        verify_selection(new_selection,spec,freeze_hash,lookup)
        selected_path=attempt/'selection-freeze.json';write_json(selected_path,new_selection,exclusive=True)
        selected_raw=read_bytes(root,selected_path,within=attempt)
        report.update(selection_path=str(selected_path.relative_to(root)),selection_sha256=sha(selected_raw))
        report['completed_validation_cells']=len(cells)
        choice=lambda items:[(c['source'],c['horizon'],c['window'],c['family'],c['status'],c['parameter']) for c in items]
        if choice(cells)!=choice(archive['selection']['cells']):
            raise ReproductionError('SELECTION_CHANGED')
        report['selection_agrees_with_archive']=True;selection=(selected_path,sha(selected_raw))
        for phase in ('evaluation','references'):
            for job in phase_jobs(spec,phase):invoke(job,evaluation,queue_path)
        if any(r['exit_code']!=0 or r['status']!='COMPLETE' or r.get('controller_error') for r in evaluation):
            raise ReproductionError('EVALUATION_INCOMPLETE')
        report['completed_evaluation_reference_cells']=len(evaluation)
        report['status']='PHASES_COMPLETE_AUDIT_PENDING'
        if reconcile is not None:
            audited=reconcile(root,attempt,queue_path,selection,archive,checkpoint)
            report.update(status='REPLICATION_AUDITED',accuracy_recomputed=True,audit=audited)
        checkpoint()
    except ReproductionError as error:
        report.update(status='STOPPED',stop_code=error.code)
    except Exception as error:
        # Keep all worker files and an explicit controller failure; no favorable retry.
        code=getattr(error,'code','CONTROLLER_ERROR')
        if type(code) is not str or re.fullmatch(r'[A-Z][A-Z0-9_]{0,63}',code) is None:code='CONTROLLER_ERROR'
        report.update(status='STOPPED',stop_code=code,error_type=type(error).__name__)
    report.update(ended_utc=utc_now(),elapsed_seconds=clock()-started,
        validation_jobs_retained=len(validation),evaluation_reference_jobs_retained=len(evaluation))
    write_json(attempt/'controller-final.json',report,exclusive=True)
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',nargs='?',choices=('verify','replicate'),default='verify')
    parser.add_argument('--attempt-id',help='Required new safe identifier for explicit replication.')
    args=parser.parse_args(argv)
    if args.mode=='replicate' and args.attempt_id is None:parser.error('replicate requires --attempt-id')
    if args.mode=='verify' and args.attempt_id is not None:parser.error('--attempt-id is only valid for replicate')
    started=time.monotonic()
    try:
        archive=verify_archive(ROOT)
        if args.mode=='verify':
            report={k:v for k,v in archive.items() if k not in ('spec','selection')}
        else:
            replication_preflight(ROOT,archive)
            with controller_deadline(started):
                # Numeric imports occur only after archive and raw hashes pass.
                from reconcile_conditional_replication import reconcile
                report=run_plan(ROOT,args.attempt_id,archive,started=started,reconcile=reconcile)
        print(json.dumps(report,indent=2,allow_nan=False))
        return 0 if report['status'] in ('ARCHIVE_VERIFIED','REPLICATION_AUDITED') else 2
    except (ReproductionError,OSError) as error:
        print(json.dumps(dict(status='STOPPED',stop_code=getattr(error,'code','FILE_INTEGRITY'),
            accuracy_recomputed=False)))
        return 2


# Result identities are fixed to the independently redownloaded public commit.
# They are literal expected values, never generated from the files at runtime.
ARCHIVED_RESULTS = {
    'results/revision-20261022/EXTERNAL_DATA.md': (10933, '6c38c769951a309575ff793726b53dce85fc8095ca1fc30db2ae3c24bb15dac7'),
    'results/revision-20261022/README.md': (10611, '0716781fbaa997844049daa95b0880d806b75c08d98341de3c02f33db58eee2d'),
    'results/revision-20261022/audit-builder-v01.py': (19287, 'c896b4f901f9188ff727ff112eb074674404869815564f1679c0b4f6caf93c27'),
    'results/revision-20261022/evaluation-annual.csv': (66777, '649619c41f4f92740bf3ebf9ee58f43781ad3439751be6faed101e1be65105cf'),
    'results/revision-20261022/evaluation-audit-02.json': (19755, '0f44825f200e364bd0df3cecc9dc9175a45755fe17fd048e6ad9d238bd31288b'),
    'results/revision-20261022/evaluation-audit.json': (19438, '46e63f8a69071b80f3dfea5d67c9522d67e4c67f6a1c51256389085803f309d5'),
    'results/revision-20261022/evaluation-fx_hourly-h24-w2880-KNN.json': (84468, '9f1f2557796cd4d0a056478f8fd76c732e9789e499c61d9d212a89d98a6952ba'),
    'results/revision-20261022/evaluation-fx_hourly-h24-w2880-QR.json': (302188, '5e13a67a74c0e79735e47365811cce6c5044bb4e2c16b225e6eb409cef4385cf'),
    'results/revision-20261022/evaluation-fx_hourly-h24-w2880-SCALED_KNN.json': (86455, 'f49954f34f7213959384c77ddbe7acbd5d93850b78f6fcab68a243ff538392ae'),
    'results/revision-20261022/evaluation-fx_hourly-h24-w720-KNN.json': (84205, 'fd67e4331fb296cb3ebf1d027fbc28760114b7ce195818d12c610d3f1467a4e8'),
    'results/revision-20261022/evaluation-fx_hourly-h24-w720-QR.json': (301693, '126fe854b210246668c05025ecc650fb6a83066607bdf5bdacb5e51062dc5087'),
    'results/revision-20261022/evaluation-fx_hourly-h24-w720-SCALED_KNN.json': (86189, '1e880209362273a3c747e43aca6ed718857549f26a7c8f52ef6ad0e7cfd33f67'),
    'results/revision-20261022/evaluation-fx_hourly-h6-w2880-KNN.json': (84636, '6f991b068b1de4fcfc9009d735303c9c191eb79e3e77622f8305ef7d37728d0d'),
    'results/revision-20261022/evaluation-fx_hourly-h6-w2880-QR.json': (302089, '30f872660f7b6eabbcec884d0a8fabca0f2071f52eb861414c5750f0b053f49f'),
    'results/revision-20261022/evaluation-fx_hourly-h6-w2880-SCALED_KNN.json': (86617, '48a25a8b299be55d78520439d711e4849af687dfd49804c4e3d855c0699de88c'),
    'results/revision-20261022/evaluation-fx_hourly-h6-w720-KNN.json': (84355, '3108d2183d17b6b468853ca8953a25869d7ff08d569925c731158d217ce578d8'),
    'results/revision-20261022/evaluation-fx_hourly-h6-w720-QR.json': (301891, 'fbf8135953f3a17d1d09b8318945ae45ab322f464a191c4936de8f7cc2fb25b1'),
    'results/revision-20261022/evaluation-fx_hourly-h6-w720-SCALED_KNN.json': (86342, '396fdc133f53bbb5701023f02a0f55492ba51ad319b61e84d07440c4e6bc9200'),
    'results/revision-20261022/evaluation-nonoverlap.csv': (15512, '571485073b7136cbb66ca70799706a6ed50598d3a940933c0180a0bfe2938a8b'),
    'results/revision-20261022/evaluation-nyfed_weekly-h24-w260-KNN.json': (13106, '6f4140bc5796c1f1266a6d3b01e223d5ed1324503e0524a88b8b0b8f7f923343'),
    'results/revision-20261022/evaluation-nyfed_weekly-h24-w260-QR.json': (30442, '1c332b3a40a99cc1c4769ef5603067e1d594c809f95f38d335381df5700d74bf'),
    'results/revision-20261022/evaluation-nyfed_weekly-h24-w260-SCALED_KNN.json': (13400, '3132d219581ee2660cc73bc16a0ab1de70ea5db30214388368ba25ea7e401aab'),
    'results/revision-20261022/evaluation-nyfed_weekly-h24-w52-KNN.json': (12995, 'b2010ab68a2a7cef10d9d1904fbac7e14d334ac1cf90e034610455526072fec8'),
    'results/revision-20261022/evaluation-nyfed_weekly-h24-w52-QR.json': (30526, 'e70dd9b200836a320fd014fe1db7e354e710c07f7bb978790da899cd27bb8aeb'),
    'results/revision-20261022/evaluation-nyfed_weekly-h24-w52-SCALED_KNN.json': (13344, '80ad837bbad3aa7177e5b90d5403a11e25d1053452e7e6a1ef021b3702ef5030'),
    'results/revision-20261022/evaluation-nyfed_weekly-h6-w260-KNN.json': (13003, 'cd52fa2955c160765e8f657216c214612060ca451fc8ed503b38fdbc9edda892'),
    'results/revision-20261022/evaluation-nyfed_weekly-h6-w260-QR.json': (30552, 'a5e6c92b42707fbf8e854fd3ba17f3506a80204a5671a13d7d4a71eee8b6574b'),
    'results/revision-20261022/evaluation-nyfed_weekly-h6-w260-SCALED_KNN.json': (13369, 'daa947c09d30fd5e62f313c61203149b87d9e822961ceece260786f10c7b1d88'),
    'results/revision-20261022/evaluation-nyfed_weekly-h6-w52-KNN.json': (12967, 'c907be7e0ca0f6805c824dacfdd3eb8da39a307fc2eb24502591d0a7ba96b927'),
    'results/revision-20261022/evaluation-nyfed_weekly-h6-w52-QR.json': (30474, '960c8d57b47ac7fdd0cc4bb973b63c9aed422d8de02f1995a03aa7ef617e870f'),
    'results/revision-20261022/evaluation-nyfed_weekly-h6-w52-SCALED_KNN.json': (13350, 'd0420f55205d459345c973148a2d24d23ec463435988c7cf199fdc88ea10ba80'),
    'results/revision-20261022/evaluation-summary.csv': (17416, '2988f6239b02c0c5d4637df8ef0881de78a3d52a845c38b3c8e3726871d8be15'),
    'results/revision-20261022/paired-annual.csv': (102217, '5b0727af566cbfa935fba95c25cf2a7918dc073baa2daf8558d84984161bce40'),
    'results/revision-20261022/paired-comparisons.csv': (26918, 'a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9'),
    'results/revision-20261022/paired-nonoverlap.csv': (25807, 'b050007b8ddffc5ba5865ccad90960740d94f55d7dd7a814e88665aa3d55677d'),
    'results/revision-20261022/references-fx_hourly-h24-w2880.json': (16664, '9e4b399bb8c9b371481873d9c80c49d553cc7285bb3f72fb0b816e642cf2e25f'),
    'results/revision-20261022/references-fx_hourly-h24-w720.json': (23907, 'fc1fcacfac56f91c2bdd18eed8e480faa2e15a73db418305100fb0fff9839149'),
    'results/revision-20261022/references-fx_hourly-h6-w2880.json': (16585, '020ed4ba49c58ed6186031c821e2d7cf3d3d8187731e435fddb25b0d4637c6f2'),
    'results/revision-20261022/references-fx_hourly-h6-w720.json': (23895, '586141d8fee61af891085dc6716ab2b7b46c1d4b61c25dd52f74bc2b06cccbeb'),
    'results/revision-20261022/references-nyfed_weekly-h24-w260.json': (44209, 'cb958d2e3570be6b48f7a2ee067b26b4e2801890cbaea3f26426e0ca5cb3c113'),
    'results/revision-20261022/references-nyfed_weekly-h24-w52.json': (44264, 'bfdc62f144bebf6e240b5f4c6479416db1771430d722e52631f4ffa400488931'),
    'results/revision-20261022/references-nyfed_weekly-h6-w260.json': (43990, '1f1e88b506649444726f0fccfafa5acad077c9a054120f759a8ed42bbd97e53d'),
    'results/revision-20261022/references-nyfed_weekly-h6-w52.json': (43691, '90eaf4c29eef6cf09c1e8e295f1c26b12ee12b37dc5f4022c89d5c16dff8d9fd'),
    'results/revision-20261022/validation-audit.json': (11209, 'ac1edbc026a2356f97d6930cf27f30523fd6b9c001a0cda3724201d32822fbd3'),
    'results/revision-20261022/validation-fx_hourly-h24-w2880-KNN.json': (56329, 'dbd73a3add6945c602de0935529337ce942d63ac3b155816bc657e84a0a520ac'),
    'results/revision-20261022/validation-fx_hourly-h24-w2880-QR.json': (197612, 'a75f0f4a492509ec97e83ea5dedefe89c07e77b37fccee57b64634b631a268a2'),
    'results/revision-20261022/validation-fx_hourly-h24-w2880-SCALED_KNN.json': (57623, '1308cd01dc58ea75c6049e4d208261ab20cd5ffb3b36300004ec73498be7f2ca'),
    'results/revision-20261022/validation-fx_hourly-h24-w720-KNN.json': (56211, 'b7cee9100fd980ccb98bfc34245dab499d1a2ab187ddf579f5036cc6bc77e18a'),
    'results/revision-20261022/validation-fx_hourly-h24-w720-QR.json': (197615, '4a683da28b61016d5a72e2d1671789fa3371d8b03b27f231356b17e5f019c4f5'),
    'results/revision-20261022/validation-fx_hourly-h24-w720-SCALED_KNN.json': (57506, '69396eede0cc73cd4fc1126fce2c8b20e3506b92c4f4741a6feafcc27a2a2d19'),
    'results/revision-20261022/validation-fx_hourly-h6-w2880-KNN.json': (56358, 'da2cf0ff3e12634af8951d9d647bfb1bdef3d43fcc2afb5ce1735a14ae3a178a'),
    'results/revision-20261022/validation-fx_hourly-h6-w2880-QR.json': (197700, 'dbc56674ff3331d3f46fc2d0c90a9bca2bedaa277793b1b478909f0d3ac9aa68'),
    'results/revision-20261022/validation-fx_hourly-h6-w2880-SCALED_KNN.json': (57663, '0a7f94087942f2e94a1241bcce3cff1616a4c950e6886f58606a455f031475bf'),
    'results/revision-20261022/validation-fx_hourly-h6-w720-KNN.json': (56317, '0b319dd57b26712492942ab94cb99a1f0454922ccd23897a8c4daea09e7013e3'),
    'results/revision-20261022/validation-fx_hourly-h6-w720-QR.json': (197695, 'd4d9b2fb344c18d8bc1d5e12ee699fef80f3a853559ebd7dbb644cd8677ac5bf'),
    'results/revision-20261022/validation-fx_hourly-h6-w720-SCALED_KNN.json': (57583, 'b04634c9ecb260559b5df7a62bdf3679d79ca90c2097bba67b94ebf4b811fa6f'),
    'results/revision-20261022/validation-nyfed_weekly-h24-w260-KNN.json': (7858, 'b15900dc420759f77fb2c2113b9c0e6d3770664914151db00224dd9bad1774ce'),
    'results/revision-20261022/validation-nyfed_weekly-h24-w260-QR.json': (17370, 'e7b16e985c3db512320fa5120648e6bb913766557f49e293f126e17f546091cd'),
    'results/revision-20261022/validation-nyfed_weekly-h24-w260-SCALED_KNN.json': (8031, 'ad157fd61524c661ce6bab0d87f100e375bf8d75fe693e8640863b787f711120'),
    'results/revision-20261022/validation-nyfed_weekly-h24-w52-KNN.json': (7862, '4b1371910dd77e37db65e2df71a8bcae1539fc730956b8a8e2b6219d37c0f61c'),
    'results/revision-20261022/validation-nyfed_weekly-h24-w52-QR.json': (17359, 'a0b562f152b2842c47a1d4a19c23700ab3bc9cd875b72f92250de22c5f1c750c'),
    'results/revision-20261022/validation-nyfed_weekly-h24-w52-SCALED_KNN.json': (8001, 'a9a213be43e3febfa94da6d6897cc804f46bab586c77bda8601727af4bf3c014'),
    'results/revision-20261022/validation-nyfed_weekly-h6-w260-KNN.json': (7898, '5213b0d5881ca895dd9a3aed17c8451a7502d27ff50d3503576eb581081bc13d'),
    'results/revision-20261022/validation-nyfed_weekly-h6-w260-QR.json': (17367, 'c0c6d6aad2d7b20386a1f0838df57e2e36b403eed345829aeea076e0be809f69'),
    'results/revision-20261022/validation-nyfed_weekly-h6-w260-SCALED_KNN.json': (8007, 'cdaa3578a865e0c0f72c0cd1615d399303b0ca8d7473785b7f2d95639dc605fe'),
    'results/revision-20261022/validation-nyfed_weekly-h6-w52-KNN.json': (7878, '0e7b42fce112ac3bfd26aa438915fab85262517cf25e543d1cfdcb514b7194ef'),
    'results/revision-20261022/validation-nyfed_weekly-h6-w52-QR.json': (17368, 'a910c16527cac5cc971456af772c4e8f8d6cab0954e4daa95ab0e3f4b52d7777'),
    'results/revision-20261022/validation-nyfed_weekly-h6-w52-SCALED_KNN.json': (8011, '44716fcbfa46059ab6fed1a351e56e9d59d57a605435f873fc72d6e336d61bd7'),
    'results/revision-20261022/validation-summary.csv': (5893, '7dc2c60085ceb31f701c6ba06b4a36cb6560c48aeeaad80be78eb460df9c9ae9'),
}
PRODUCTION_CONTRACT = ArchiveContract(FREEZE,SELECTION,CODE_FILES,ARCHIVED_RESULTS)


if __name__=='__main__':
    # The deferred adapter imports this name; keep exception identity shared
    # with the CLI rather than creating a second module during replication.
    sys.modules['reproduce_conditional']=sys.modules[__name__]
    raise SystemExit(main())
