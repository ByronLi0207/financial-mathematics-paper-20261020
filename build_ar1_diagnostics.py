"""Read one frozen AR attempt for eight floor/four horizon diagnostics.

Import and --help are standard-library-only and never locate private data.
Execution requires a separate exact --freeze and fresh output ID. No source
reader, fitting, prediction, forecast repair or legacy output write is invoked.
"""
from __future__ import annotations

import argparse
import ast
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib
import importlib.abc
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import re
import signal
import sys
import time
import types

ROOT=Path(__file__).resolve().parent
PLAN_PATH='protocol/revision-20261022/ar1-diagnostics-plan.json'
FREEZE_PATH='protocol/revision-20261022/ar1-diagnostics-executable-freeze.json'
READBACK_PATH='results/revision-20261022/ar1-replay/inventory-readback.json'
DESIGN_PATH='notes/revision-20261022/ar1-diagnostic-design-agent.md'
PROTECTED_PATHS=('results/revision-20261022/post-result-floor.csv','results/revision-20261022/post-result-horizon.csv')
THREAD_NAMES=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')
CORE_FILES=('conditional_quantile.py','test_conditional_quantile.py','conditional_features.py','test_conditional_features.py',
    'conditional_study.py','test_conditional_study.py','conditional_sources.py','test_conditional_sources.py',
    'run_conditional_study.py','test_run_conditional_study.py','study_core.py','test_core.py','run_study.py','test_runner.py',
    'protocol/revision-20261022/study-spec.json','protocol/revision-20261022/conditional-baseline-design.md')
AR_FILES=('run_ar1_replay.py','ar1_replay.py','reproduce_conditional.py','reproduce_conditional_diagnostics.py',
    'reconcile_conditional_replication.py','conditional_sources.py','conditional_study.py','conditional_features.py',
    'conditional_quantile.py','run_conditional_study.py','study_core.py','run_study.py',
    'results/revision-20261022/audit-builder-v01.py','test_ar1_replay.py','test_run_ar1_replay.py',
    'protocol/revision-20261022/ar1-replay-design.md','protocol/revision-20261022/ar1-replay-spec.json')
EXTRA_FILES=('protocol/revision-20261022/executable-freeze.json','protocol/revision-20261022/selection-freeze.json',
    'protocol/revision-20261022/ar1-replay-executable-freeze.json','verify_ar1_output.py','test_verify_ar1_output.py',
    'build_conditional_diagnostics.py','test_conditional_diagnostics.py','build_conditional_results.py','test_build_conditional_results.py',
    'study_data.py','study_report.py','build_ar1_diagnostics.py','test_build_ar1_diagnostics.py',PLAN_PATH,DESIGN_PATH,READBACK_PATH,*PROTECTED_PATHS)


class DiagnosticError(ValueError):
    def __init__(self,code):self.code=code;super().__init__(code)


def require(ok,code):
    if not ok:raise DiagnosticError(code)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'DIAGNOSTIC_JSON_DUPLICATE');d[k]=v
        return d
    try:
        value=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(DiagnosticError('DIAGNOSTIC_JSON_NONFINITE')))
        require(type(value) is dict,'DIAGNOSTIC_JSON_OBJECT');return value
    except (ValueError,UnicodeError,TypeError) as error:
        if isinstance(error,DiagnosticError):raise
        raise DiagnosticError('DIAGNOSTIC_JSON_INVALID') from None


def safe_read(root,path,*,within=None,cap=8*1024*1024):
    root=Path(root).absolute();p=Path(path);p=p if p.is_absolute() else root/p
    boundary=root if within is None else Path(within).absolute()
    require('..' not in p.parts and not any(x.is_symlink() for x in (p,*p.parents))
        and p.is_relative_to(root) and p.is_relative_to(boundary) and p.is_file(),'DIAGNOSTIC_FILE_BOUNDARY')
    try:
        require(p.stat().st_size<=cap,'DIAGNOSTIC_FILE_SIZE')
        with p.open('rb') as stream:raw=stream.read(cap+1)
        require(len(raw)<=cap,'DIAGNOSTIC_FILE_SIZE');return raw
    except OSError:raise DiagnosticError('DIAGNOSTIC_FILE_READ') from None


def required_freeze_paths(root=ROOT):
    """Conservative local Python closure, including bound tests' imports."""
    root=Path(root).absolute();found=set(CORE_FILES)|set(AR_FILES)|set(EXTRA_FILES);pending=list(found);seen=set()
    while pending:
        name=pending.pop()
        if not name.endswith('.py') or name in seen:continue
        seen.add(name)
        try:tree=ast.parse(safe_read(root,name),filename=name)
        except SyntaxError:raise DiagnosticError('DIAGNOSTIC_CODE_SYNTAX') from None
        for node in ast.walk(tree):
            modules=([a.name for a in node.names] if isinstance(node,ast.Import) else
                [node.module] if isinstance(node,ast.ImportFrom) and not node.level and node.module else [])
            for module in modules:
                local=module.split('.')[0]+'.py'
                if (root/local).is_file() and local not in found:found.add(local);pending.append(local)
    return tuple(sorted(found))


def preflight(root,freeze_sha):
    root=Path(root).absolute();raw=safe_read(root,FREEZE_PATH)
    require(type(freeze_sha) is str and re.fullmatch('[0-9a-f]{64}',freeze_sha) is not None and sha(raw)==freeze_sha,
        'DIAGNOSTIC_FREEZE_IDENTITY')
    freeze=strict_json(raw)
    require(set(freeze)=={'version','status','created_utc','plan_path','plan_sha256','files'}
        and type(freeze['version']) is int and freeze['version']==1 and freeze['status']=='FROZEN'
        and freeze['plan_path']==PLAN_PATH and type(freeze['files']) is dict,'DIAGNOSTIC_FREEZE_SCHEMA')
    try:stamp=datetime.fromisoformat(freeze['created_utc'].replace('Z','+00:00'))
    except (ValueError,TypeError,AttributeError):raise DiagnosticError('DIAGNOSTIC_FREEZE_TIME') from None
    require(stamp.tzinfo is not None,'DIAGNOSTIC_FREEZE_TIME')
    names=required_freeze_paths(root);require(set(freeze['files'])==set(names),'DIAGNOSTIC_FREEZE_INVENTORY')
    snapshots={}
    for name in names:
        value=safe_read(root,name)
        require(sha(value)==freeze['files'][name],'DIAGNOSTIC_CODE_IDENTITY');snapshots[name]=value
    require(sha(snapshots[PLAN_PATH])==freeze['plan_sha256'],'DIAGNOSTIC_PLAN_IDENTITY')
    plan=strict_json(snapshots[PLAN_PATH]);spec=strict_json(snapshots['protocol/revision-20261022/study-spec.json'])
    require(plan.get('version')==1 and type(plan.get('version')) is int
        and plan.get('status')=='POST_RESULT_DESIGN_FIXED_BEFORE_NEW_DIAGNOSTIC_COUNTS'
        and plan.get('method')=='AR1_REPLAY' and plan.get('floor_rows')==8 and plan.get('paired_horizon_rows')==4
        and plan.get('horizons')==[6,24] and set(plan.get('sources',{}))=={'fx_hourly','nyfed_weekly'},'DIAGNOSTIC_PLAN_SCHEMA')
    require(all(plan.get(k) is v for k,v in dict(no_source_loading=True,no_new_model_selection=True,no_refitting=True,
        no_forecast_repair=True,no_new_population_inference=True,legacy_artifacts_modified=False).items()),'DIAGNOSTIC_PLAN_SCOPE')
    resources=dict(processes=1,requested_numerical_threads=1,maximum_observed_os_threads=2,
        wall_seconds=540,hard_seconds=600,rss_bytes=1610612736)
    require(plan.get('resources')==resources and all(type(plan['resources'][k]) is int for k in resources),
        'DIAGNOSTIC_RESOURCE_CONTRACT')
    require(plan['design_note']==dict(path=DESIGN_PATH,sha256=sha(snapshots[DESIGN_PATH])),'DIAGNOSTIC_DESIGN_IDENTITY')
    require(plan['accepted_v2_readback']==dict(path=READBACK_PATH,bytes=len(snapshots[READBACK_PATH]),
        sha256=sha(snapshots[READBACK_PATH]),code_sha256=sha(snapshots['verify_ar1_output.py'])),'DIAGNOSTIC_READBACK_IDENTITY')
    for name,expected in (('protocol/revision-20261022/executable-freeze.json',CORE_FILES),
                         ('protocol/revision-20261022/ar1-replay-executable-freeze.json',AR_FILES)):
        old=strict_json(snapshots[name]);require(old.get('status')=='FROZEN' and set(old['files'])==set(expected)
            and all(old['files'][p]==sha(snapshots[p]) for p in expected),'DIAGNOSTIC_ORIGINAL_FREEZE')
    require(plan['original_executable_freeze_sha256']==sha(snapshots['protocol/revision-20261022/executable-freeze.json'])
        and plan['original_selection_sha256']==sha(snapshots['protocol/revision-20261022/selection-freeze.json'])
        and plan['ar1_freeze_sha256']==sha(snapshots['protocol/revision-20261022/ar1-replay-executable-freeze.json'])
        and plan['ar1_spec_sha256']==sha(snapshots['protocol/revision-20261022/ar1-replay-spec.json']),'DIAGNOSTIC_SCIENTIFIC_IDENTITY')
    for s,cfg in plan['sources'].items():
        original=spec['sources'][s]
        require(cfg==dict(evaluation_first=original['evaluation_origin_first'],evaluation_last=original['evaluation_origin_last'],
            windows=original['windows'],refit_step=original['refit_step'],native_unit=original['native_unit']),
            'DIAGNOSTIC_SOURCE_CONTRACT')
    return dict(root=root,freeze_sha256=freeze_sha,freeze_raw=raw,freeze=freeze,plan=plan,snapshots=snapshots)


def verify_snapshots(frozen):
    require(safe_read(frozen['root'],FREEZE_PATH)==frozen['freeze_raw'],'DIAGNOSTIC_FREEZE_CHANGED')
    for name,raw in frozen['snapshots'].items():require(safe_read(frozen['root'],name)==raw,'DIAGNOSTIC_INPUT_CHANGED')


class _SnapshotFinder(importlib.abc.MetaPathFinder,importlib.abc.Loader):
    def __init__(self,root,snapshots):
        self.root=root;self.modules={Path(n).stem:(n,raw) for n,raw in snapshots.items()
            if n.endswith('.py') and '/' not in n and not n.startswith('test_') and n!='build_ar1_diagnostics.py'}
    def find_spec(self,fullname,path=None,target=None):
        if fullname in self.modules:
            return importlib.util.spec_from_file_location(fullname,self.root/self.modules[fullname][0],loader=self)
        if '.' not in fullname and (self.root/(fullname+'.py')).is_file():
            raise DiagnosticError('DIAGNOSTIC_UNBOUND_LOCAL_IMPORT')
        return None
    def create_module(self,spec):return None
    def exec_module(self,module):
        name,raw=self.modules[module.__name__];module.__file__=str(self.root/name)
        exec(compile(raw,module.__file__,'exec'),module.__dict__)


@contextmanager
def load_helpers(frozen,*,allow_preloaded=False):
    for name in THREAD_NAMES:os.environ[name]='1'
    finder=_SnapshotFinder(frozen['root'],frozen['snapshots'])
    existing={name:sys.modules[name] for name in finder.modules if name in sys.modules}
    require(allow_preloaded or not existing and 'numpy' not in sys.modules,'DIAGNOSTIC_PRELOADED_NUMERIC_CONTEXT')
    for name in existing:sys.modules.pop(name,None)
    sys.meta_path.insert(0,finder)
    try:
        import numpy as np
        import run_ar1_replay as runner
        import verify_ar1_output as auditor
        import build_conditional_diagnostics as kernels
        import build_conditional_results as results
        import run_study as resource_helpers
        import reproduce_conditional as rep
        import reconcile_conditional_replication as adapter
        import reproduce_conditional_diagnostics as diag
        yield types.SimpleNamespace(np=np,runner=runner,auditor=auditor,kernels=kernels,results=results,
            resource=resource_helpers,rep=rep,adapter=adapter,diag=diag)
    finally:
        if finder in sys.meta_path:sys.meta_path.remove(finder)
        for name in finder.modules:sys.modules.pop(name,None)
        sys.modules.update(existing)


def _id(value):
    require(type(value) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,63}',value) is not None,'DIAGNOSTIC_OUTPUT_ID')
    return value


def _context(helpers,root,replication_dir):
    inputs=helpers.runner.prepare_replica(root,replication_dir)
    return inputs,helpers.runner.verify_execution(inputs)


def verify_context(frozen,inputs,execution,ar_id,readback):
    root=frozen['root'];plan=frozen['plan'];attempt=Path(inputs['attempt']).absolute()
    require(inputs['root']==root and attempt.is_relative_to(root)
        and re.fullmatch(r'\.scratch/revision-20261022/replication-[A-Za-z0-9][A-Za-z0-9_-]{0,63}',str(attempt.relative_to(root))) is not None
        and not any(p.is_symlink() for p in (attempt,*attempt.parents)) and attempt.is_dir(),'DIAGNOSTIC_REPLICA_BOUNDARY')
    cells=[dict(source=s,horizon=h,window=w) for s,c in plan['sources'].items() for h in (6,24) for w in c['windows']]
    require(execution['spec']['cells']==cells and execution['spec_sha256']==plan['ar1_spec_sha256']
        and execution['freeze_sha256']==plan['ar1_freeze_sha256']
        and inputs['archive']['executable_freeze_sha256']==plan['original_executable_freeze_sha256']
        and inputs['archive']['selection_freeze_sha256']==plan['original_selection_sha256'],'DIAGNOSTIC_CONTEXT_IDENTITY')
    chosen=Path(readback);chosen=chosen if chosen.is_absolute() else root/chosen
    require(chosen==root/READBACK_PATH,'DIAGNOSTIC_READBACK_PATH')
    return cells,attempt/('ar1-replay-'+_id(ar_id))


def validate_readback(frozen,raw_manifest):
    p=frozen['plan'];receipt=strict_json(frozen['snapshots'][READBACK_PATH])
    require(p['ar1_manifest_sha256']==sha(raw_manifest),'DIAGNOSTIC_MANIFEST_IDENTITY')
    expected=dict(version=2,status='AR1_INDEPENDENT_READBACK_PASS',ar1_manifest_sha256=sha(raw_manifest),
        ar1_spec_sha256=p['ar1_spec_sha256'],ar1_freeze_sha256=p['ar1_freeze_sha256'],cells=8,
        aggregate_rows_independently_checked=192,exact_fraction_fits=24,scalar_recursive_reports=24,
        exact_unique_csv_keys_checked=True,all_consumed_exports_bound_to_manifest=True,
        new_model_selection=False,original_models_refitted=False,source_values_public=False,
        code_sha256=p['accepted_v2_readback']['code_sha256'])
    require(all(type(receipt.get(k)) is type(v) and receipt.get(k)==v for k,v in expected.items()),'DIAGNOSTIC_READBACK_SCOPE')
    return receipt


def verify_manifest(manifest,inputs,execution,ar_id,cells,helpers):
    expected=dict(version=1,status='AR1_REPLAY_COMPLETE',analysis_status='POST_RESULT_EXPLORATORY',method='AR1_REPLAY',
        all_cells_complete=True,complete_cells=8,failed_cells=0,original_primaries_changed=False,
        original_models_refitted=False,new_parameter_selection=False,
        replication_dir=str(inputs['attempt'].relative_to(inputs['root'])),attempt_id=ar_id,
        ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
        original_executable_freeze_sha256=inputs['archive']['executable_freeze_sha256'],
        archived_selection_sha256=inputs['archive']['selection_freeze_sha256'],new_selection_sha256=inputs['selection_hash'])
    require(all(type(manifest.get(k)) is type(v) and manifest.get(k)==v for k,v in expected.items()),'DIAGNOSTIC_MANIFEST_CONTEXT')
    helpers.auditor.verify_export_inventory(manifest['exports'],manifest['private_exports'],cells)
    helpers.adapter.verify_resource(manifest['resources'])
    public={e['path']:e for e in manifest['exports']};private={e['path']:e for e in manifest['private_exports']}
    require(manifest['cell_receipts']==[dict(cell=c,status='COMPLETE',receipt=public[helpers.auditor.cell_stem(c)+'-receipt.json'])
        for c in cells],'DIAGNOSTIC_CELL_INVENTORY')
    return public,private


def validate_vectors(v,cfg,helpers):
    np=helpers.np;n=cfg['evaluation_last']-cfg['evaluation_first']+1
    ids=np.arange(cfg['evaluation_first'],cfg['evaluation_last']+1,dtype=np.int64)
    require(set(v)=={'origins','capacity','peak','floor','refit_indices','pinball'}
        and all(a.shape==(n,) for a in v.values()) and np.array_equal(v['origins'],ids),'DIAGNOSTIC_ORIGIN_ALIGNMENT')
    require(all(np.isfinite(v[k]).all() for k in ('capacity','peak','floor','pinball'))
        and np.all(v['floor']>=0) and np.all(v['peak']>=v['floor']) and np.all(v['capacity']>=v['floor']),
        'DIAGNOSTIC_TARGET_FLOOR')
    wanted=ids[0]+(ids-ids[0])//cfg['refit_step']*cfg['refit_step']
    require(np.array_equal(v['refit_indices'],wanted),'DIAGNOSTIC_REFIT_ALIGNMENT')


def load_cell(helpers,frozen,inputs,execution,destination,cell,public,private):
    np=helpers.np;stem=helpers.auditor.cell_stem(cell);cfg=frozen['plan']['sources'][cell['source']]
    raw=helpers.auditor.verified_bytes(frozen['root'],destination,private[stem+'-traces.npz'],area='private')
    helpers.auditor.check_output_headers(raw,np,cfg['evaluation_last']-cfg['evaluation_first']+1)
    with np.load(io.BytesIO(raw),allow_pickle=False) as archive:v={k:archive[k].copy() for k in archive.files}
    validate_vectors(v,cfg,helpers)
    receipt_raw=helpers.auditor.verified_bytes(frozen['root'],destination,public[stem+'-receipt.json'],area='public')
    receipt=strict_json(receipt_raw)
    count=len(range(cfg['evaluation_first'],cfg['evaluation_last']+1,cfg['refit_step']))
    helpers.auditor.verify_cell_receipt(receipt,cell,inputs,execution,
        [private[stem+'-fits.json'],private[stem+'-traces.npz']],count)
    return v


def summary_inventory(rows,cells,plan):
    expected={(c['source'],str(c['horizon']),str(c['window'])) for c in cells};seen=set();found={}
    require(len(rows)==8,'DIAGNOSTIC_SUMMARY_INVENTORY')
    for row in rows:
        key=(row.get('source'),row.get('horizon'),row.get('window'))
        require(key in expected and key not in seen,'DIAGNOSTIC_SUMMARY_INVENTORY');seen.add(key)
        cfg=plan['sources'][key[0]];n=cfg['evaluation_last']-cfg['evaluation_first']+1
        meta=dict(method='AR1_REPLAY',native_unit=cfg['native_unit'],status='COMPLETE',stop_code='',
            refit_step=str(cfg['refit_step']),expected_origin_count=str(n),completed_origin_count=str(n),origin_count=str(n))
        require(all(row.get(k)==v for k,v in meta.items()),'DIAGNOSTIC_SUMMARY_LABELS');found[key]=row
    require(seen==expected,'DIAGNOSTIC_SUMMARY_INVENTORY');return found


def floor_row(helpers,cell,cfg,v):
    return dict(source=cell['source'],native_unit=cfg['native_unit'],horizon=cell['horizon'],window=cell['window'],
        method='AR1_REPLAY',parameter=None,status='COMPLETE',first_source_index=int(v['origins'][0]),
        last_source_index=int(v['origins'][-1]))|helpers.kernels.floor_diagnostics(v['peak'],v['capacity'],v['floor'])


def horizon_rows(helpers,cells,plan,vectors):
    np=helpers.np;rows=[]
    for cell in cells:
        if cell['horizon']!=6:continue
        s,w=cell['source'],cell['window'];short=vectors[s,6,w];long=vectors[s,24,w]
        require(all(np.array_equal(short[k],long[k]) for k in ('origins','floor','refit_indices')),
            'DIAGNOSTIC_HORIZON_ALIGNMENT')
        require(not np.any(short['peak']>long['peak']),'DIAGNOSTIC_TARGET_ORDER')
        rows.append(dict(source=s,native_unit=plan['sources'][s]['native_unit'],window=w,method='AR1_REPLAY',
            parameter_h6=None,parameter_h24=None,status='COMPLETE',first_source_index=int(short['origins'][0]),
            last_source_index=int(short['origins'][-1]))|helpers.kernels.horizon_diagnostics(
                short['capacity'],long['capacity'],short['peak'],long['peak']))
    require(len(rows)==4 and len({(r['source'],r['window'],r['method']) for r in rows})==4,'DIAGNOSTIC_HORIZON_INVENTORY')
    return rows


def safe_code(error):
    code=getattr(error,'code','DIAGNOSTIC_FAILED')
    return code if type(code) is str and re.fullmatch('[A-Z][A-Z0-9_]{0,63}',code) else 'DIAGNOSTIC_FAILED'


def execute(root,replication_dir,ar_id,readback,diagnostic_id,freeze_sha,*,context_provider=None,guard_factory=None):
    """Only context/measurement plumbing can be injected in synthetic fixtures."""
    started=time.monotonic();root=Path(root).absolute();_id(ar_id);_id(diagnostic_id)
    production=context_provider is None
    require(not production or guard_factory is None,'DIAGNOSTIC_TEST_ONLY_GUARD')
    require(not production or platform.system()=='Darwin','DIAGNOSTIC_DARWIN_REQUIRED')
    if production:
        signal.signal(signal.SIGALRM,signal.SIG_DFL);signal.setitimer(signal.ITIMER_REAL,600.)
    try:
        frozen=preflight(root,freeze_sha)
        require(time.monotonic()-started<540.,'RESOURCE_WALL')
        with load_helpers(frozen,allow_preloaded=not production) as helpers:
            inputs,execution=(_context if production else context_provider)(helpers,root,replication_dir)
            cells,ar_destination=verify_context(frozen,inputs,execution,ar_id,readback)
            output=inputs['attempt']/('ar1-diagnostics-'+diagnostic_id)
            require(not output.exists() and not output.is_symlink(),'DIAGNOSTIC_OUTPUT_EXISTS')
            public_out,private_out=helpers.resource.create_attempt(output)
            began=datetime.now(timezone.utc).isoformat()
            guard=(helpers.resource.RunGuard if guard_factory is None else guard_factory)(started,began,output,public_out,private_out)
            floors=[];pairs=[];written=[];vectors={};consumed=[]
            try:
                guard(stage='ar1_diagnostic_start')
                manifest_raw=safe_read(root,ar_destination/'public/ar1-replay-manifest.json',within=ar_destination)
                validate_readback(frozen,manifest_raw);manifest=strict_json(manifest_raw)
                public,private=verify_manifest(manifest,inputs,execution,ar_id,cells,helpers)
                rows=helpers.auditor.load_verified_csv(root,ar_destination,public['ar1-summary.csv'])
                summary=summary_inventory(rows,cells,frozen['plan'])
                for cell in cells:
                    s,h,w=(cell[k] for k in ('source','horizon','window'));v=load_cell(helpers,frozen,inputs,execution,ar_destination,cell,public,private)
                    row=floor_row(helpers,cell,frozen['plan']['sources'][s],v)
                    require(row['floor_binding_breach_count']+row['other_issue_breach_count']==
                        int(summary[s,str(h),str(w)]['strict_breach_count']),'DIAGNOSTIC_BREACH_RECONCILIATION')
                    floors.append(row);vectors[s,h,w]=v
                    stem=helpers.auditor.cell_stem(cell)
                    consumed.append(dict(cell=cell,receipt=public[stem+'-receipt.json'],trace=private[stem+'-traces.npz']))
                    guard.arrays(vectors);guard(stage='ar1_diagnostic_cell_checked',cell_id=stem)
                require(len(floors)==8 and len({(r['source'],r['horizon'],r['window'],r['method']) for r in floors})==8,
                    'DIAGNOSTIC_FLOOR_INVENTORY')
                pairs=horizon_rows(helpers,cells,frozen['plan'],vectors)
                guard(stage='ar1_diagnostic_statistics_complete')
                helpers.runner.verify_inputs(inputs);verify_snapshots(frozen)
                helpers.diag.verify_exports(root,ar_destination,manifest['exports'])
                helpers.runner.verify_private_exports(root,ar_destination,manifest['private_exports'])
                require(safe_read(root,ar_destination/'public/ar1-replay-manifest.json',within=ar_destination)==manifest_raw,
                    'DIAGNOSTIC_MANIFEST_CHANGED')
                blobs={name:helpers.adapter.csv_bytes(rows) for name,rows in (('ar1-floor.csv',floors),('ar1-horizon.csv',pairs))}
                # Independent public-byte readback, never export observation vectors.
                for name,raw in blobs.items():
                    with (public_out/name).open('xb') as stream:
                        written.append(name)
                        stream.write(raw)
                    require(safe_read(root,public_out/name,within=output)==raw,'DIAGNOSTIC_EXPORT_READBACK')
                guard(stage='ar1_diagnostic_final')
                helpers.runner.verify_inputs(inputs);verify_snapshots(frozen)
                helpers.diag.verify_exports(root,ar_destination,manifest['exports'])
                helpers.runner.verify_private_exports(root,ar_destination,manifest['private_exports'])
                require(safe_read(root,ar_destination/'public/ar1-replay-manifest.json',within=ar_destination)==manifest_raw,
                    'DIAGNOSTIC_MANIFEST_CHANGED')
                require(all(safe_read(root,public_out/name,within=output)==raw for name,raw in blobs.items()),
                    'DIAGNOSTIC_EXPORT_CHANGED')
                audit=dict(version=1,status='AR1_DIAGNOSTICS_VERIFIED',analysis_status='EXPLICITLY_POST_RESULT_DESCRIPTIVE',
                    created_utc=helpers.rep.utc_now(),diagnostic_freeze_sha256=freeze_sha,
                    plan=dict(path=PLAN_PATH,bytes=len(frozen['snapshots'][PLAN_PATH]),sha256=sha(frozen['snapshots'][PLAN_PATH])),
                    accepted_readback=frozen['plan']['accepted_v2_readback'],ar1_manifest_sha256=sha(manifest_raw),
                    ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
                    original_executable_freeze_sha256=frozen['plan']['original_executable_freeze_sha256'],
                    original_selection_sha256=frozen['plan']['original_selection_sha256'],new_selection_sha256=inputs['selection_hash'],
                    floor_rows=8,horizon_rows=4,input_artifacts=consumed,
                    summary_identity=public['ar1-summary.csv'],source_identities={s:{k:c[k] for k in ('sha256','bytes','record_count','native_unit')}
                        for s,c in inputs['spec']['sources'].items()},
                    full_origin_identities={s:dict(count=c['evaluation_last']-c['evaluation_first']+1,
                        first=c['evaluation_first'],last=c['evaluation_last']) for s,c in frozen['plan']['sources'].items()},
                    source_loaded=False,models_fitted=False,forecasts_repaired=False,new_model_selection=False,
                    new_population_inference=False,legacy_artifacts_modified=False,
                    numerical_scope='All retained forecast vectors; no additional source-label, OLS or replay oracle',
                    exports=[dict(path=n,bytes=len(raw),sha256=sha(raw)) for n,raw in blobs.items()],
                    code_sha256=sha(frozen['snapshots']['build_ar1_diagnostics.py']),resources=dict(guard.resources))
                audit_name='ar1-diagnostics-audit.json';audit_raw=helpers.rep.json_bytes(audit)
                with (public_out/audit_name).open('xb') as stream:
                    written.append(audit_name)
                    stream.write(audit_raw)
                require(safe_read(root,public_out/audit_name,within=output)==audit_raw,'DIAGNOSTIC_AUDIT_READBACK')
                return audit
            except Exception as error:
                code=safe_code(error)
                for name in written:
                    p=public_out/name
                    if p.is_file():p.rename(private_out/('unverified-'+name))
                helpers.rep.write_json(private_out/'partial-aggregates.json',dict(floor_rows=floors,horizon_rows=pairs),exclusive=True)
                helpers.rep.write_json(public_out/'ar1-diagnostics-failure.json',dict(version=1,status='STOPPED',stop_code=code,
                    complete_supplement=False,completed_floor_rows=len(floors),completed_horizon_rows=len(pairs),
                    shortened_segment_published=False,resources=dict(guard.resources)),exclusive=True)
                raise DiagnosticError(code) from None
    except DiagnosticError:raise
    except Exception as error:raise DiagnosticError(safe_code(error)) from None
    finally:
        if production:signal.setitimer(signal.ITIMER_REAL,0.)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replication-dir',required=True)
    parser.add_argument('--ar1-attempt-id',required=True)
    parser.add_argument('--readback',required=True)
    parser.add_argument('--diagnostic-id',required=True)
    parser.add_argument('--freeze',required=True,help='SHA-256 of the separate diagnostic executable freeze')
    args=parser.parse_args(argv)
    try:
        result=execute(ROOT,args.replication_dir,args.ar1_attempt_id,args.readback,args.diagnostic_id,args.freeze)
        print(json.dumps(dict(status=result['status'],floor_rows=result['floor_rows'],horizon_rows=result['horizon_rows']),indent=2))
        return 0
    except DiagnosticError as error:
        print(json.dumps(dict(status='STOPPED',stop_code=error.code,verified=False)));return 1


if __name__=='__main__':raise SystemExit(main())
