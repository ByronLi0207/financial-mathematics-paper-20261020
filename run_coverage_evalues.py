"""Explicit late fixed-terminal coverage diagnostic on frozen saved reports.

Import/help and absence of --execute do not load numerical payloads. Execution
fits no model, loads no raw source and makes no coverage-certification claim.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime,timezone
from fractions import Fraction
import hashlib
import importlib
import io
import json
from pathlib import Path
import platform
import re
import signal
import time
import types

ROOT=Path(__file__).resolve().parent
FREEZE_PATH='protocol/revision-20261022/coverage-evalue-executable-freeze.json'
BASE_FREEZE='protocol/revision-20261022/ar1-diagnostics-reproduction-freeze.json'
SPEC_PATH='protocol/revision-20261022/coverage-evalue-spec.json'
DESIGN_PATH='protocol/revision-20261022/coverage-evalue-design.md'
NEW_FILES=('coverage_evalues.py','test_coverage_evalues.py','run_coverage_evalues.py','test_run_coverage_evalues.py',SPEC_PATH,DESIGN_PATH)
METHODS=('QR','KNN','SCALED_KNN','frozen_F','frozen_S','frozen_K','AR1_REPLAY')
FIELDS=('origins','peak','floor','refit_indices','capacity','pinball')
PUBLIC_FILES=('coverage-evalue-summary.csv','coverage-evalue-phases.csv')
INFERENTIAL_STATUS='Post-result exploratory on inspected records; fixed-procedure null theory is not retrospective empirical 5% familywise error control'


class CoverageError(ValueError):
    def __init__(self,code):self.code=code;super().__init__(code)


def require(ok,code):
    if not ok:raise CoverageError(code)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def read(root,path,cap=8*1024*1024):
    root=Path(root).absolute();p=Path(path);p=p if p.is_absolute() else root/p
    require(p.is_relative_to(root) and '..' not in p.parts and p.is_file()
        and not any(q.is_symlink() for q in (p,*p.parents)),'COVERAGE_PATH')
    try:
        with p.open('rb') as stream:raw=stream.read(cap+1)
        require(len(raw)<=cap,'COVERAGE_FILE_SIZE');return raw
    except OSError:raise CoverageError('COVERAGE_READ') from None


def strict_json(raw):
    def pairs(items):
        value={}
        for k,v in items:require(k not in value,'COVERAGE_JSON_DUPLICATE');value[k]=v
        return value
    def bad(_):raise CoverageError('COVERAGE_JSON_NONFINITE')
    try:
        value=json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
        require(type(value) is dict,'COVERAGE_JSON_OBJECT');return value
    except (ValueError,TypeError,UnicodeError) as error:
        if isinstance(error,CoverageError):raise
        raise CoverageError('COVERAGE_JSON_INVALID') from None


def required_freeze_paths(root=ROOT):
    root=Path(root).absolute();base=strict_json(read(root,BASE_FREEZE))
    require(type(base.get('files')) is dict,'COVERAGE_BASE_FREEZE')
    found=set(base['files'])|{BASE_FREEZE,*NEW_FILES};pending=list(found);seen=set()
    while pending:
        name=pending.pop()
        if not name.endswith('.py') or name in seen:continue
        seen.add(name)
        try:tree=ast.parse(read(root,name),filename=name)
        except SyntaxError:raise CoverageError('COVERAGE_CODE_SYNTAX') from None
        for node in ast.walk(tree):
            modules=([x.name for x in node.names] if isinstance(node,ast.Import) else
                [node.module] if isinstance(node,ast.ImportFrom) and not node.level and node.module else [])
            for module in modules:
                local=module.split('.')[0]+'.py'
                if (root/local).is_file() and local not in found:found.add(local);pending.append(local)
    return tuple(sorted(found))


def validate_spec(spec,source_spec):
    expected=dict(version=1,id='fixed-terminal-coverage-20261022',status='FIXED_TERMINAL_COVERAGE_SPECIFICATION',
        family_size=56,expected_summary_rows=56,expected_phase_rows=896,maximum_origin_count=10000,maximum_horizon=1000,
        nominal_quantile=dict(numerator=19,denominator=20),alpha=dict(numerator=1,denominator=20),
        family_error_budget_delta=dict(numerator=1,denominator=20),per_cell_threshold=dict(numerator=1120,denominator=1),
        phase_spacing='H+1 recorded indices',phase_anchor='first existing evaluation origin; never reset by year',
        phase_weights='equal over all H+1 phases; empty phase value1',alternative_prior='uniform probability measure on [alpha,1]',
        event='strict stored_float64_peak > stored_float64_capacity; equality is nonbreach',
        terminal='fixed whole existing evaluation issue set, with all labels complete by last_origin+H',
        method_labels=list(METHODS),full_filtration_anytime_claim=False,new_forecast_fit=False,
        new_scoring_rule=False,new_raw_download=False,mutable_old_freezes=False)
    require(all(type(spec.get(k)) is type(v) and spec.get(k)==v for k,v in expected.items()),'COVERAGE_SPEC_CONTRACT')
    for name in ('nominal_quantile','alpha','family_error_budget_delta','per_cell_threshold'):
        require(all(type(x) is int for x in spec[name].values()),'COVERAGE_SPEC_TYPES')
    resources=dict(worker_processes=1,requested_numerical_threads=1,max_observed_threads=2,
        internal_stop_seconds=540,hard_stop_seconds=600,internal_stop_rss_bytes=1610612736,max_rss_bytes=2147483648)
    require(spec.get('resources')==resources and all(type(x) is int for x in spec['resources'].values()),'COVERAGE_RESOURCE_CONTRACT')
    configs=[dict(source=s,horizon=h,window=w,origin_count=c['evaluation_origin_last']-c['evaluation_origin_first']+1,
        first_origin=c['evaluation_origin_first'],last_origin=c['evaluation_origin_last'],units=c['native_unit'],refit_step=c['refit_step'])
        for s,c in source_spec['sources'].items() for h in (6,24) for w in c['windows']]
    require(source_spec['horizons']==[6,24] and spec.get('configurations')==configs and len(configs)==8,'COVERAGE_CONFIGURATIONS')
    for c in configs:
        require(all(type(c[k]) is int for k in ('horizon','window','origin_count','first_origin','last_origin','refit_step'))
            and 0<c['origin_count']<=10000 and 0<c['horizon']<=1000
            and c['first_origin']-c['horizon']-c['window']+1>=0
            and c['last_origin']+c['horizon']<source_spec['sources'][c['source']]['record_count'],
            'COVERAGE_DECLARED_MATURITY')
    require(sum((c['horizon']+1)*len(METHODS) for c in configs)==896,'COVERAGE_PHASE_INVENTORY')
    return spec


def preflight(root,freeze_hash):
    root=Path(root).absolute();raw=read(root,FREEZE_PATH)
    require(type(freeze_hash) is str and re.fullmatch('[0-9a-f]{64}',freeze_hash) is not None
        and sha(raw)==freeze_hash,'COVERAGE_FREEZE_IDENTITY')
    frozen=strict_json(raw)
    require(set(frozen)=={'version','status','created_utc','base_freeze_path','base_freeze_sha256','spec_path','spec_sha256','files'}
        and type(frozen['version']) is int and frozen['version']==1 and frozen['status']=='FROZEN'
        and frozen['base_freeze_path']==BASE_FREEZE and frozen['spec_path']==SPEC_PATH
        and type(frozen['files']) is dict,'COVERAGE_FREEZE_SCHEMA')
    try:stamp=datetime.fromisoformat(frozen['created_utc'].replace('Z','+00:00'))
    except (ValueError,TypeError,AttributeError):raise CoverageError('COVERAGE_FREEZE_TIME') from None
    require(stamp.tzinfo is not None,'COVERAGE_FREEZE_TIME')
    names=required_freeze_paths(root);require(set(frozen['files'])==set(names),'COVERAGE_FREEZE_INVENTORY')
    snapshots={n:read(root,n) for n in names}
    require(all(sha(raw)==frozen['files'][n] for n,raw in snapshots.items()),'COVERAGE_CODE_IDENTITY')
    require(sha(snapshots[BASE_FREEZE])==frozen['base_freeze_sha256']
        and sha(snapshots[SPEC_PATH])==frozen['spec_sha256'],'COVERAGE_FROZEN_CONTRACT')
    backend=types.ModuleType('_checked_coverage_bootstrap');backend.__file__=str(root/'reproduce_ar1_diagnostics.py')
    exec(compile(snapshots['reproduce_ar1_diagnostics.py'],backend.__file__,'exec'),backend.__dict__)
    base=backend.preflight(root,frozen['base_freeze_sha256'])
    spec=validate_spec(strict_json(snapshots[SPEC_PATH]),strict_json(snapshots['protocol/revision-20261022/study-spec.json']))
    return dict(root=root,raw=raw,hash=freeze_hash,freeze=frozen,snapshots=snapshots,backend=backend,base=base,spec=spec)


def verify_static(frozen):
    require(read(frozen['root'],FREEZE_PATH)==frozen['raw'],'COVERAGE_FREEZE_CHANGED')
    require(all(read(frozen['root'],n)==raw for n,raw in frozen['snapshots'].items()),'COVERAGE_STATIC_CHANGED')


def serialize_report(meta,result,kernel):
    require(type(result.horizon) is int and meta['horizon']==result.horizon,'COVERAGE_KERNEL_HORIZON')
    threshold=Fraction(1120);flag=result.value>=threshold
    fields=lambda value:{'evalue_'+k:v for k,v in kernel.fraction_fields(value).items()}
    summary=meta|dict(n=result.n,k=result.k,first_origin=result.first_origin,last_origin=result.last_origin,
        label_terminal_index=result.last_origin+result.horizon,phase_count=result.horizon+1,
        family_size=56,reference_threshold=1120,adjusted_reference_threshold_crossed=flag)|fields(result.value)
    phases=[meta|dict(phase=p.phase,n=p.n,k=p.k,cell_adjusted_reference_threshold_crossed=flag)|fields(p.value) for p in result.phases]
    require([p.phase for p in result.phases]==list(range(result.horizon+1))
        and sum(p.n for p in result.phases)==result.n and sum(p.k for p in result.phases)==result.k
        and sum((p.value for p in result.phases),Fraction())/(result.horizon+1)==result.value,
        'COVERAGE_KERNEL_PHASE_CONTRACT')
    return summary,phases


def collect_original(inputs,h,consume,guard):
    spec=inputs['spec'];expected=h.rep.phase_jobs(spec,'evaluation')+h.rep.phase_jobs(spec,'references')
    require(inputs['cells']==expected and len(inputs['queue'])==32,'COVERAGE_ORIGINAL_CELL_INVENTORY')
    containers=[];headers=0
    for queued,cell in zip(inputs['queue'],expected):
        phase,s,horizon,w,family=cell;cfg=spec['sources'][s]
        require(tuple(queued.get(n) for n in ('phase','source','horizon','window','family'))==cell
            and queued.get('status')=='COMPLETE' and queued.get('stop_code') is None
            and type(queued.get('exit_code')) is int and queued['exit_code']==0,'COVERAGE_QUEUE_CONTEXT')
        expected_path=h.rep.worker_directory(inputs['attempt'],cell)/'public/manifest.json'
        require(queued['receipt_path']==str(expected_path.relative_to(inputs['root'])),'COVERAGE_RECEIPT_PATH')
        raw=consume(expected_path);require(sha(raw)==queued['receipt_sha256']
            and raw==inputs['exported_receipts'][h.diag._receipt_name(cell)],'COVERAGE_RECEIPT_HASH')
        receipt=h.rep.strict_json(raw);result=receipt['result']
        require(tuple(receipt.get(n) for n in ('phase','source','horizon','window','family'))==cell
            and receipt.get('executable_freeze_sha256')==inputs['archive']['executable_freeze_sha256']
            and receipt.get('selection_freeze_sha256')==(inputs['selection_hash'] if family else None)
            and all(receipt['source_identity'].get(k)==cfg[k] for k in ('sha256','bytes','record_count','native_unit'))
            and result.get('native_unit')==cfg['native_unit'],'COVERAGE_PHASE_IDENTITY')
        h.adapter.verify_resource(receipt['resources'])
        parameter=inputs['selected'][s,horizon,w,family]['parameter'] if family else None
        require(not family or inputs['selected'][s,horizon,w,family]['status']=='SELECTED'
            and result.get('selection')==dict(status='SELECTED',parameter=parameter),'COVERAGE_SELECTED_PARAMETER')
        methods=h.diag._methods(spec,cell);h.adapter.verify_phase_labels(receipt,methods,parameter)
        first,last=cfg['evaluation_origin_first'],cfg['evaluation_origin_last']
        require(result.get('origin_identity')==h.rep.origin_identity(first,last),'COVERAGE_ORIGIN_IDENTITY')
        h.adapter.verify_fit_records(result['fit_diagnostics'],cfg,horizon,w,family,first,last)
        path=expected_path.parent.parent/'private/numeric-traces.npz';trace=consume(path,cap=64*1024*1024)
        require(receipt['artifacts']==[dict(area='private',name='numeric-traces.npz',bytes=len(trace),sha256=sha(trace))],
            'COVERAGE_TRACE_ARTIFACT')
        wanted={m+'_'+n for m in methods for n in FIELDS}
        h.diag._check_trace_headers(trace,wanted,h.np,last-first+1);headers+=len(wanted)
        chosen=[family] if family else ['frozen_F','frozen_S','frozen_K']
        containers.append(dict(source=s,horizon=horizon,window=w,parameter=parameter,methods=chosen,
            raw=trace,prefix=True,receipt_sha256=sha(raw),trace_sha256=sha(trace)))
        guard(stage='coverage_evalue_input_headers')
    return containers,headers


def collect_ar(inputs,execution,ar_id,receipt,h,consume,builder,cells,guard):
    destination=inputs['attempt']/('ar1-replay-'+ar_id)
    manifest_raw=consume(destination/'public/ar1-replay-manifest.json')
    require(receipt.get('ar1_manifest_sha256')==sha(manifest_raw),'COVERAGE_FRESH_MANIFEST_HASH')
    manifest=h.rep.strict_json(manifest_raw)
    public,private=builder.verify_manifest(manifest,inputs,execution,ar_id,cells,h)
    containers=[];fit_count=0
    for cell in cells:
        s,horizon,w=(cell[k] for k in ('source','horizon','window'));cfg=inputs['spec']['sources'][s]
        first,last=cfg['evaluation_origin_first'],cfg['evaluation_origin_last'];stem=h.auditor.cell_stem(cell)
        def get(base,entry):
            raw=consume(destination/base/entry['path'])
            require(entry==dict(path=entry['path'],bytes=len(raw),sha256=sha(raw)),'COVERAGE_AR_ARTIFACT')
            return raw
        trace=get('private',private[stem+'-traces.npz']);h.auditor.check_output_headers(trace,h.np,last-first+1)
        refits=[first+(t-first)//cfg['refit_step']*cfg['refit_step'] for t in range(first,last+1)]
        fits=h.auditor.verify_fit_inventory(h.rep.strict_json(get('private',private[stem+'-fits.json'])),cell,cfg,refits)
        fit_count+=len(fits)
        h.auditor.verify_cell_receipt(h.rep.strict_json(get('public',public[stem+'-receipt.json'])),cell,inputs,execution,
            [private[stem+'-fits.json'],private[stem+'-traces.npz']],len(fits))
        containers.append(dict(source=s,horizon=horizon,window=w,parameter=None,methods=['AR1_REPLAY'],
            raw=trace,prefix=False,receipt_sha256=public[stem+'-receipt.json']['sha256'],trace_sha256=sha(trace)))
        guard(stage='coverage_evalue_input_headers')
    require(receipt.get('fit_records_metadata_checked')==fit_count,'COVERAGE_FRESH_FIT_SCOPE')
    return containers,manifest,manifest_raw


def compute_reports(containers,spec,source_spec,h,kernel,guard):
    np=h.np;reports={};phase_rows={};targets={};floors_by_source={}
    configs={(c['source'],c['horizon'],c['window']):c for c in spec['configurations']}
    for container in containers:
        s,horizon,w=(container[k] for k in ('source','horizon','window'));cfg=configs[s,horizon,w]
        first,last=cfg['first_origin'],cfg['last_origin'];n=cfg['origin_count']
        origins=np.arange(first,last+1,dtype=np.int64);refits=first+(origins-first)//cfg['refit_step']*cfg['refit_step']
        require(bool(np.all(refits<=origins)) and int(refits[0])-horizon-w+1>=0
            and last+horizon<source_spec['sources'][s]['record_count'],'COVERAGE_LABEL_MATURITY')
        with np.load(io.BytesIO(container['raw']),allow_pickle=False) as archive:
            for method in container['methods']:
                key=(s,horizon,w,method);require(key not in reports,'COVERAGE_DUPLICATE_METHOD')
                prefix=method+'_' if container['prefix'] else ''
                arrays={name:archive[prefix+name] for name in FIELDS if name!='pinball'}
                require(all(a.shape==(n,) for a in arrays.values())
                    and np.array_equal(arrays['origins'],origins) and np.array_equal(arrays['refit_indices'],refits),
                    'COVERAGE_TRACE_ALIGNMENT')
                p,b,c=(arrays[k] for k in ('peak','floor','capacity'))
                require(all(np.isfinite(a).all() for a in (p,b,c)) and bool(np.all(b>=0))
                    and bool(np.all(p>=b)) and bool(np.all(c>=b)),'COVERAGE_TRACE_FINITE_FLOOR')
                if (s,horizon) in targets:
                    require(np.array_equal(p,targets[s,horizon][0]) and np.array_equal(b,targets[s,horizon][1]),
                        'COVERAGE_SHARED_TARGET_FLOOR')
                else:targets[s,horizon]=(p.copy(),b.copy())
                if s in floors_by_source:require(np.array_equal(b,floors_by_source[s]),'COVERAGE_CROSS_H_FLOOR')
                else:floors_by_source[s]=b.copy()
                if (s,6) in targets and (s,24) in targets:
                    require(bool(np.all(targets[s,6][0]<=targets[s,24][0])),'COVERAGE_NESTED_TARGET_ORDER')
                hits=[bool(pi>ci) for pi,ci in zip(p.tolist(),c.tolist())]
                value=kernel.phase_mixture(origins.tolist(),hits,horizon)
                require(value.n==n and value.k==sum(hits) and value.first_origin==first and value.last_origin==last,
                    'COVERAGE_KERNEL_CELL_CONTRACT')
                meta=dict(source=s,native_unit=cfg['units'],horizon=horizon,window=w,method=method,parameter=container['parameter'])
                reports[key],phase_rows[key]=serialize_report(meta,value,kernel)
                guard.arrays(arrays,targets,reports,phase_rows);guard(stage='coverage_evalue_cell',cell_id=f'{s}-h{horizon}-w{w}-{method}')
    order=[(c['source'],c['horizon'],c['window'],m) for c in spec['configurations'] for m in METHODS]
    require(len(order)==len(reports)==len(set(order))==56 and set(reports)==set(order),'COVERAGE_CLOSED_FAMILY')
    summary=[reports[k] for k in order];phases=[r for k in order for r in phase_rows[k]]
    require(len(phases)==896 and len({(r['source'],r['horizon'],r['window'],r['method'],r['phase']) for r in phases})==896,
        'COVERAGE_ALL_PHASES')
    return summary,phases


def execute(root,replication_dir,ar_id,readback_path,readback_hash,attempt_id,freeze_hash,*,execute=False,
            context_provider=None,guard_factory=None):
    if execute is not True:return dict(status='NOT_EXECUTED',financial_payload_loaded=False)
    started=time.monotonic();root=Path(root).absolute();production=context_provider is None
    require(all(type(v) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,63}',v) is not None for v in (ar_id,attempt_id)),
        'COVERAGE_ATTEMPT_ID')
    require(not production or guard_factory is None,'COVERAGE_TEST_ONLY_GUARD')
    require(not production or platform.system()=='Darwin','COVERAGE_DARWIN_REQUIRED')
    if production:signal.signal(signal.SIGALRM,signal.SIG_DFL);signal.setitimer(signal.ITIMER_REAL,600.)
    try:
        frozen=preflight(root,freeze_hash);base=frozen['base'];builder=base['builder'];spec=frozen['spec']
        readback=Path(readback_path);readback=readback if readback.is_absolute() else root/readback
        require(readback.is_relative_to(root/'state/revision-20261022') or readback.is_relative_to(root/'results/revision-20261022'),
            'COVERAGE_READBACK_PATH')
        readback_raw=read(root,readback)
        require(readback.suffix=='.json' and type(readback_hash) is str and re.fullmatch('[0-9a-f]{64}',readback_hash) is not None
            and sha(readback_raw)==readback_hash,'COVERAGE_READBACK_HASH')
        receipt=strict_json(readback_raw);plan=base['retained']['plan']
        expected=dict(version=2,status='AR1_INDEPENDENT_READBACK_PASS',ar1_spec_sha256=plan['ar1_spec_sha256'],
            ar1_freeze_sha256=plan['ar1_freeze_sha256'],cells=8,aggregate_rows_independently_checked=192,
            exact_fraction_fits=24,scalar_recursive_reports=24,exact_unique_csv_keys_checked=True,
            all_consumed_exports_bound_to_manifest=True,new_model_selection=False,original_models_refitted=False,
            source_values_public=False,code_sha256=sha(frozen['snapshots']['verify_ar1_output.py']))
        require(all(type(receipt.get(k)) is type(v) and receipt.get(k)==v for k,v in expected.items()),'COVERAGE_READBACK_SCOPE')
        require(time.monotonic()-started<540.,'RESOURCE_WALL')
        with builder.load_helpers(dict(root=root,snapshots=frozen['snapshots']),allow_preloaded=not production) as h:
            kernel=importlib.import_module('coverage_evalues')
            inputs,execution=(builder._context if production else context_provider)(h,root,replication_dir)
            attempt=Path(inputs['attempt']).absolute()
            require(inputs['root']==root and attempt.is_relative_to(root) and attempt.is_dir()
                and re.fullmatch(r'\.scratch/revision-20261022/replication-[A-Za-z0-9][A-Za-z0-9_-]{0,63}',
                    str(attempt.relative_to(root))) is not None and not any(p.is_symlink() for p in (attempt,*attempt.parents)),
                'COVERAGE_REPLICA_BOUNDARY')
            validate_spec(spec,inputs['spec'])
            cells=[{k:c[k] for k in ('source','horizon','window')} for c in spec['configurations']]
            require(execution['spec']['cells']==cells and execution['spec_sha256']==plan['ar1_spec_sha256']
                and execution['freeze_sha256']==plan['ar1_freeze_sha256']
                and inputs['archive']['executable_freeze_sha256']==plan['original_executable_freeze_sha256']
                and inputs['archive']['selection_freeze_sha256']==plan['original_selection_sha256'],'COVERAGE_CONTEXT_CONTRACT')
            output=attempt/('coverage-evalues-'+attempt_id);public_out,private_out=h.resource.create_attempt(output)
            guard=(h.resource.RunGuard if guard_factory is None else guard_factory)(started,datetime.now(timezone.utc).isoformat(),
                output,public_out,private_out)
            consumed={readback:readback_raw};written=[];summary=[];phases=[]
            def consume(path,cap=8*1024*1024):
                p=Path(path);p=p if p.is_absolute() else root/p
                raw=h.diag._consume(inputs,p,cap=cap)
                require(p not in consumed or consumed[p]==raw,'COVERAGE_CONSUMED_CHANGED');consumed[p]=raw;return raw
            def write(path,raw,public=False):
                with path.open('xb') as stream:
                    if public:written.append(path.name)
                    stream.write(raw)
                require(read(root,path)==raw,'COVERAGE_EXPORT_READBACK')
            try:
                guard(stage='coverage_evalue_start');h.adapter.verify_resource(receipt['resources'])
                original,header_count=collect_original(inputs,h,consume,guard)
                ar,manifest,manifest_raw=collect_ar(inputs,execution,ar_id,receipt,h,consume,builder,cells,guard)
                containers=original+ar;header_count+=6*len(ar)
                require(len(containers)==40 and header_count==588,'COVERAGE_INPUT_CONTAINER_INVENTORY')
                binding=dict(version=1,role='INPUT_BINDING_ONLY',upstream_receipt_generated=False,
                    replication_dir=str(attempt.relative_to(root)),ar1_attempt_id=ar_id,coverage_freeze_sha256=freeze_hash,
                    coverage_spec_sha256=sha(frozen['snapshots'][SPEC_PATH]),base_freeze_sha256=frozen['freeze']['base_freeze_sha256'],
                    original_executable_freeze_sha256=inputs['archive']['executable_freeze_sha256'],
                    archived_selection_sha256=inputs['archive']['selection_freeze_sha256'],new_selection_sha256=inputs['selection_hash'],
                    ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
                    readback=dict(path=str(readback.relative_to(root)),bytes=len(readback_raw),sha256=sha(readback_raw)),
                    ar1_manifest_sha256=sha(manifest_raw),input_container_count=40,input_header_count=588)
                binding_raw=h.rep.json_bytes(binding);binding_path=private_out/'input-binding.json';write(binding_path,binding_raw)
                summary,phases=compute_reports(containers,spec,inputs['spec'],h,kernel,guard)
                blobs={n:h.adapter.csv_bytes(rows) for n,rows in zip(PUBLIC_FILES,(summary,phases))}
                for name,raw in blobs.items():write(public_out/name,raw,True)
                guard(stage='coverage_evalue_final');h.runner.verify_inputs(inputs);verify_static(frozen)
                require(all(read(root,p,cap=64*1024*1024)==raw for p,raw in consumed.items()),'COVERAGE_FINAL_INPUT_CHANGED')
                h.diag.verify_exports(root,attempt/('ar1-replay-'+ar_id),manifest['exports'])
                h.runner.verify_private_exports(root,attempt/('ar1-replay-'+ar_id),manifest['private_exports'])
                require(read(root,binding_path)==binding_raw and all(read(root,public_out/n)==raw for n,raw in blobs.items()),
                    'COVERAGE_FINAL_OUTPUT_CHANGED')
                audit=dict(version=1,status='COVERAGE_EVALUE_COMPUTATION_VERIFIED',created_utc=h.rep.utc_now(),
                    post_result_exploratory=True,actual_inferential_status=INFERENTIAL_STATUS,
                    inference_scope='Fixed-terminal one-sided datewise conditional strict-breach upper-bound null for the declared fixed procedure family',
                    coverage_guarantee_established=False,full_filtration_anytime_claim=False,
                    summary_rows=56,phase_rows=896,family_size=56,reference_threshold=1120,
                    adjusted_reference_crossings=sum(r['adjusted_reference_threshold_crossed'] for r in summary),
                    freeze_sha256=freeze_hash,spec_sha256=sha(frozen['snapshots'][SPEC_PATH]),
                    input_binding=dict(path=str(binding_path.relative_to(root)),bytes=len(binding_raw),sha256=sha(binding_raw)),
                    input_file_identities=[dict(path=str(p.relative_to(root)),bytes=len(raw),sha256=sha(raw)) for p,raw in sorted(consumed.items())],
                    input_container_count=40,input_header_count=588,raw_sources_loaded=False,models_fitted=False,
                    predictions_repaired=False,new_parameter_selection=False,upstream_receipt_generated=False,
                    phase_scope='All H+1 phases; original first-origin anchor; no calendar reset or selected phase',
                    exact_threshold_arithmetic=True,monetary_units_pooled=False,
                    exports=[dict(path=n,bytes=len(raw),sha256=sha(raw)) for n,raw in blobs.items()],resources=dict(guard.resources))
                write(public_out/'coverage-evalue-manifest.json',h.rep.json_bytes(audit),True);return audit
            except Exception as error:
                code=builder.safe_code(error)
                for name in written:
                    p=public_out/name
                    if p.is_file():p.rename(private_out/('unverified-'+name))
                h.rep.write_json(private_out/'partial-aggregates.json',dict(summary_rows=summary,phase_rows=phases),exclusive=True)
                h.rep.write_json(public_out/'coverage-evalue-failure.json',dict(version=1,status='STOPPED',stop_code=code,
                    complete_family=False,family_size_reduced=False,shortened_segment_published=False,
                    completed_summary_rows=len(summary),completed_phase_rows=len(phases),resources=dict(guard.resources)),exclusive=True)
                raise CoverageError(code) from None
    except CoverageError:raise
    except Exception as error:
        code=getattr(error,'code','COVERAGE_FAILED')
        raise CoverageError(code if type(code) is str and re.fullmatch('[A-Z][A-Z0-9_]{0,63}',code) else 'COVERAGE_FAILED') from None
    finally:
        if production:signal.setitimer(signal.ITIMER_REAL,0.)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    for n in ('replication-dir','ar1-attempt-id','readback','readback-sha256','attempt-id','freeze'):parser.add_argument('--'+n,required=True)
    a=parser.parse_args(argv)
    try:
        result=execute(ROOT,a.replication_dir,a.ar1_attempt_id,a.readback,a.readback_sha256,a.attempt_id,a.freeze,execute=a.execute)
        print(json.dumps({k:result[k] for k in ('status','summary_rows','phase_rows') if k in result},indent=2));return 0
    except CoverageError as error:print(json.dumps(dict(status='STOPPED',stop_code=error.code,verified=False)));return 1


if __name__=='__main__':raise SystemExit(main())
