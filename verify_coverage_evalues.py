"""Independent fixed-terminal readback; financial execution is explicit only.

This checker never imports either coverage production module. It uses the
distinct integer binomial formula, saved float64 reports/targets and actual
record-origin phases. The producer's results are not inputs to hit counting.
"""
from __future__ import annotations

import argparse
import ast
import csv
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import time
import types
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
if ROOT.name=='revision-20261022' and ROOT.parent.name=='.scratch':
    ROOT=ROOT.parent.parent
SPEC = 'protocol/revision-20261022/coverage-evalue-spec.json'
FREEZE = 'protocol/revision-20261022/coverage-evalue-executable-freeze.json'
DESIGN = 'protocol/revision-20261022/coverage-evalue-design.md'
BASE = 'protocol/revision-20261022/ar1-diagnostics-reproduction-freeze.json'
METHODS = ('QR','KNN','SCALED_KNN','frozen_F','frozen_S','frozen_K','AR1_REPLAY')
NEW_FILES = (SPEC, DESIGN, 'coverage_evalues.py','test_coverage_evalues.py',
             'run_coverage_evalues.py','test_run_coverage_evalues.py')
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
SUMMARY_NAME = 'coverage-evalue-summary.csv'
PHASE_NAME = 'coverage-evalue-phases.csv'


class CheckError(ValueError):
    pass


def require(value, code):
    if not value:
        raise CheckError(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def json_object(raw):
    def pairs(items):
        result = {}
        for key,value in items:
            require(key not in result,'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    value = json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(CheckError('NONFINITE_JSON')))
    require(type(value) is dict,'JSON_OBJECT_REQUIRED')
    return value


def read(root,path,*,cap=8*1024*1024,within=None):
    p = Path(path)
    p = p if p.is_absolute() else root/p
    boundary = root if within is None else Path(within)
    require('..' not in p.parts and p.is_relative_to(root) and p.is_relative_to(boundary)
        and not any(q.is_symlink() for q in (p,*p.parents)) and p.is_file(),'FILE_BOUNDARY')
    require(p.stat().st_size<=cap,'FILE_SIZE')
    with p.open('rb') as stream:
        raw = stream.read(cap+1)
    require(len(raw)<=cap,'FILE_SIZE')
    return raw


def identity(raw):
    return {'bytes':len(raw),'sha256':digest(raw)}


def typed_equal(left,right):
    if type(left) is not type(right):return False
    if type(left) is dict:
        return set(left)==set(right) and all(typed_equal(left[k],right[k]) for k in left)
    if type(left) is list:
        return len(left)==len(right) and all(typed_equal(a,b) for a,b in zip(left,right))
    return left==right


@lru_cache(maxsize=4096)
def integer_mixture(n,k):
    """Distinct exact formula; no production recurrence or coverage import."""
    require(type(n) is int and type(k) is int and 0<=k<=n<=10000,'COUNT_DOMAIN')
    numerator = sum(math.comb(n+1,j)*19**(k-j) for j in range(k+1))
    denominator = (n+1)*math.comb(n,k)
    return Fraction(numerator,denominator)


def scalar_phases(origins,hits,horizon):
    require(type(horizon) is int and 1<=horizon<=1000,'HORIZON_DOMAIN')
    require(len(origins)==len(hits)>0 and len(origins)<=10000,'ORIGIN_COUNT')
    require(all(type(t) is int and t>=0 for t in origins)
        and all(a<b for a,b in zip(origins,origins[1:])),'ORIGIN_ORDER')
    require(all(type(bit) is bool for bit in hits),'HIT_TYPE')
    n,k = [0]*(horizon+1),[0]*(horizon+1)
    for t,hit in zip(origins,hits):
        r = (t-origins[0])%(horizon+1)
        n[r] += 1
        k[r] += int(hit)
    phases = [(r,n[r],k[r],integer_mixture(n[r],k[r])) for r in range(horizon+1)]
    value = sum((p[3] for p in phases),Fraction())/(horizon+1)
    return phases,value


def exact_fields(row,value):
    require(row['evalue_numerator_hex']==hex(value.numerator)
        and row['evalue_denominator_hex']==hex(value.denominator),'EXACT_RATIONAL_VALUE')
    log = float(row['evalue_log10_approx'])
    expected_log = math.log10(value.numerator)-math.log10(value.denominator)
    require(math.isfinite(log) and math.isclose(log,expected_log,rel_tol=1e-13,abs_tol=1e-11),'LOG_DISPLAY')
    with localcontext() as context:
        context.prec = 50
        approximate = Decimal(row['evalue_display'])
        exact = Decimal(value.numerator)/Decimal(value.denominator)
        require(approximate.is_finite() and abs(approximate-exact)<=abs(exact)*Decimal('1e-11'),'SCIENTIFIC_DISPLAY')


def artificial_check():
    """Finite artificial checks only; never locate a financial input."""
    require(integer_mixture(0,0)==1 and integer_mixture(1,0)==Fraction(1,2)
        and integer_mixture(1,1)==Fraction(21,2),'ARTIFICIAL_CLOSED_FORMS')
    for n in range(9):
        expectation = sum((Fraction(math.comb(n,k)*19**(n-k),20**n)
            *integer_mixture(n,k) for k in range(n+1)),Fraction())
        require(expectation==1,'ARTIFICIAL_BOUNDARY_EXPECTATION')
    phases,value = scalar_phases([10,11,13],[False,True,False],3)
    require([p[1] for p in phases]==[1,1,0,1]
        and phases[2][3]==1 and value==Fraction(25,8),'ARTIFICIAL_PHASES')
    require(not (1.>1.) and math.nextafter(1.,math.inf)>1.
        and integer_mixture(3,3)>=1120 and integer_mixture(2,2)<1120,'ARTIFICIAL_EVENT_THRESHOLD')
    require(not typed_equal({'version':True},{'version':1}),'ARTIFICIAL_TYPED_BINDING')
    require('coverage_evalues' not in sys.modules
        and 'run_coverage_evalues' not in sys.modules,'PRODUCTION_STAT_IMPORT')
    return {'status':'ARTIFICIAL_CHECK_PASS','financial_inputs_read':False,
            'production_statistical_modules_imported':False}


def fixed_inputs(root,expected_hash):
    raw=read(root,FREEZE);freeze=json_object(raw)
    require(re.fullmatch('[0-9a-f]{64}',expected_hash or '') is not None
        and digest(raw)==expected_hash,'COVERAGE_FREEZE_HASH')
    require(set(freeze)=={'version','status','created_utc','base_freeze_path','base_freeze_sha256',
        'spec_path','spec_sha256','files'} and type(freeze['version']) is int and freeze['version']==1
        and freeze['status']=='FROZEN' and freeze['base_freeze_path']==BASE
        and freeze['spec_path']==SPEC and type(freeze['files']) is dict,'COVERAGE_FREEZE_SCHEMA')
    require(datetime.fromisoformat(freeze['created_utc'].replace('Z','+00:00')).tzinfo is not None,'FREEZE_TIME')
    base=json_object(read(root,BASE));names=set(base['files'])|{BASE,*NEW_FILES};pending=list(names);seen=set()
    while pending:
        name=pending.pop()
        if not name.endswith('.py') or name in seen:continue
        seen.add(name)
        for node in ast.walk(ast.parse(read(root,name),filename=name)):
            modules=([a.name for a in node.names] if isinstance(node,ast.Import) else
                [node.module] if isinstance(node,ast.ImportFrom) and not node.level and node.module else [])
            for module in modules:
                path=module.split('.')[0]+'.py'
                if (root/path).is_file() and path not in names:names.add(path);pending.append(path)
    require(set(freeze['files'])==names,'COVERAGE_FREEZE_CLOSURE')
    snapshots={n:read(root,n) for n in names}
    require(all(digest(value)==freeze['files'][n] for n,value in snapshots.items())
        and digest(snapshots[BASE])==freeze['base_freeze_sha256']
        and digest(snapshots[SPEC])==freeze['spec_sha256'],'COVERAGE_STATIC_HASH')
    # This existing helper verifies the older provenance closures only. It
    # neither imports the new coverage modules nor loads financial payloads.
    backend=types.ModuleType('_independent_old_provenance')
    backend.__file__=str(root/'reproduce_ar1_diagnostics.py')
    exec(compile(snapshots['reproduce_ar1_diagnostics.py'],backend.__file__,'exec'),backend.__dict__)
    retained=backend.preflight(root,freeze['base_freeze_sha256'])
    spec=json_object(snapshots[SPEC]);source_spec=json_object(snapshots['protocol/revision-20261022/study-spec.json'])
    require(spec['method_labels']==list(METHODS) and spec['family_size']==56
        and spec['expected_summary_rows']==56 and spec['expected_phase_rows']==896
        and spec['alpha']=={'numerator':1,'denominator':20}
        and spec['family_error_budget_delta']=={'numerator':1,'denominator':20}
        and spec['per_cell_threshold']=={'numerator':1120,'denominator':1},'FIXED_STATISTICAL_CONTRACT')
    expected=[dict(source=s,horizon=h,window=w,origin_count=c['evaluation_origin_last']-c['evaluation_origin_first']+1,
        first_origin=c['evaluation_origin_first'],last_origin=c['evaluation_origin_last'],units=c['native_unit'],refit_step=c['refit_step'])
        for s,c in source_spec['sources'].items() for h in (6,24) for w in c['windows']]
    require(spec['configurations']==expected and len(expected)==8
        and sum((c['horizon']+1)*len(METHODS) for c in expected)==896,'CONFIGURATION_INVENTORY')
    return freeze,raw,snapshots,retained,spec


def csv_rows(raw,fields,count):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8'),newline=''))
    require(reader.fieldnames==list(fields) and len(set(reader.fieldnames))==len(fields),'CSV_COLUMNS')
    rows=list(reader)
    require(len(rows)==count and all(set(r)==set(fields) and all(v is not None for v in r.values()) for r in rows),'CSV_ROWS')
    return rows


def check_run(args):
    started=time.monotonic();root=Path(args.root).absolute();script=Path(__file__).absolute()
    require(re.fullmatch('[0-9a-f]{64}',args.self_sha256 or '') is not None
        and digest(read(root,script))==args.self_sha256,'INDEPENDENT_CODE_IDENTITY')
    require(all(re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,63}',v or '') is not None
        for v in (args.ar1_attempt_id,args.coverage_attempt_id)),'ATTEMPT_ID')
    output=Path(args.output or '');output=output if output.is_absolute() else root/output
    require(output.suffix=='.json' and output.is_relative_to(root/'state/revision-20261022')
        and not output.exists() and output.parent.is_dir()
        and not any(p.is_symlink() for p in (output,*output.parents)),'EXCLUSIVE_READBACK_OUTPUT')
    for name in THREADS:os.environ[name]='1'
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(CheckError('RESOURCE_HARD_TIMEOUT')))
    signal.setitimer(signal.ITIMER_REAL,600.)
    try:
        freeze,freeze_raw,static,retained,spec=fixed_inputs(root,args.freeze_sha256)
        require('numpy' not in sys.modules,'NUMERIC_IMPORT_BEFORE_PREFLIGHT')
        sys.path.insert(0,str(root));sys.dont_write_bytecode=True
        import numpy as np
        import run_ar1_replay as runner
        import reproduce_conditional_diagnostics as diag
        import reproduce_conditional as rep
        import reconcile_conditional_replication as adapter
        import verify_ar1_output as auditor
        import run_study as resource
        require('coverage_evalues' not in sys.modules and 'run_coverage_evalues' not in sys.modules,'PRODUCTION_STAT_IMPORT')
        inputs=runner.prepare_replica(root,args.replication_dir);execution=runner.verify_execution(inputs)
        attempt=inputs['attempt'];destination=attempt/('ar1-replay-'+args.ar1_attempt_id)
        coverage=attempt/('coverage-evalues-'+args.coverage_attempt_id)
        require(coverage.is_dir() and not any(p.is_symlink() for p in (coverage,*coverage.parents)),'COVERAGE_ATTEMPT_BOUNDARY')
        guard=resource.RunGuard(started,rep.utc_now(),coverage,coverage/'public',coverage/'private')
        guard(stage='independent_coverage_start');consumed={}
        def consume(path,cap=8*1024*1024):
            p=Path(path);p=p if p.is_absolute() else root/p
            raw=read(root,p,cap=cap);found=identity(raw)
            require(p not in consumed or consumed[p]==(found,cap),'INPUT_CHANGED_DURING_CHECK')
            consumed[p]=(found,cap);return raw
        readback_path=Path(args.readback or '');readback_path=readback_path if readback_path.is_absolute() else root/readback_path
        require(readback_path.suffix=='.json' and (readback_path.is_relative_to(root/'state/revision-20261022')
            or readback_path.is_relative_to(root/'results/revision-20261022')),'UPSTREAM_READBACK_PATH')
        readback_raw=consume(readback_path)
        require(digest(readback_raw)==args.readback_sha256,'UPSTREAM_READBACK_HASH')
        readback=json_object(readback_raw);plan=retained['retained']['plan']
        expected=dict(version=2,status='AR1_INDEPENDENT_READBACK_PASS',ar1_spec_sha256=execution['spec_sha256'],
            ar1_freeze_sha256=execution['freeze_sha256'],cells=8,aggregate_rows_independently_checked=192,
            exact_fraction_fits=24,scalar_recursive_reports=24,exact_unique_csv_keys_checked=True,
            all_consumed_exports_bound_to_manifest=True,new_model_selection=False,original_models_refitted=False,
            source_values_public=False,code_sha256=digest(static['verify_ar1_output.py']))
        require(all(type(readback.get(k)) is type(v) and readback.get(k)==v for k,v in expected.items()),'UPSTREAM_V2_READBACK_SCOPE')
        require(execution['spec_sha256']==plan['ar1_spec_sha256'] and execution['freeze_sha256']==plan['ar1_freeze_sha256'],
            'UPSTREAM_SCIENTIFIC_CONTEXT')
        containers=[];header_count=0;fields=('origins','peak','floor','refit_indices','capacity','pinball')
        for queued,cell in zip(inputs['queue'],inputs['cells']):
            phase,s,h,w,family=cell;cfg=inputs['spec']['sources'][s];n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
            path=rep.worker_directory(attempt,cell)/'public/manifest.json';raw=consume(path)
            require(queued['receipt_path']==str(path.relative_to(root)) and digest(raw)==queued['receipt_sha256']
                and raw==inputs['exported_receipts'][diag._receipt_name(cell)],'ORIGINAL_RECEIPT_HASH')
            receipt=json_object(raw);result=receipt['result'];methods=diag._methods(inputs['spec'],cell)
            parameter=inputs['selected'][s,h,w,family]['parameter'] if family else None
            require(tuple(receipt[k] for k in ('phase','source','horizon','window','family'))==cell
                and receipt['executable_freeze_sha256']==inputs['archive']['executable_freeze_sha256']
                and receipt['selection_freeze_sha256']==(inputs['selection_hash'] if family else None)
                and all(receipt['source_identity'][k]==cfg[k] for k in ('sha256','bytes','record_count','native_unit')),
                'ORIGINAL_CELL_BINDING')
            adapter.verify_phase_labels(receipt,methods,parameter)
            require(result['origin_identity']==rep.origin_identity(cfg['evaluation_origin_first'],cfg['evaluation_origin_last'])
                and result['native_unit']==cfg['native_unit'],'ORIGINAL_ORIGIN_UNIT_BINDING')
            trace=consume(path.parent.parent/'private/numeric-traces.npz',64*1024*1024)
            require(receipt['artifacts']==[dict(area='private',name='numeric-traces.npz',**identity(trace))],'ORIGINAL_TRACE_HASH')
            wanted={m+'_'+f for m in methods for f in fields};diag._check_trace_headers(trace,wanted,np,n);header_count+=len(wanted)
            containers.append((s,h,w,parameter,[family] if family else ['frozen_F','frozen_S','frozen_K'],True,trace))
            guard(stage='independent_coverage_headers')
        ar_manifest_raw=consume(destination/'public/ar1-replay-manifest.json');ar_manifest=json_object(ar_manifest_raw)
        require(readback['ar1_manifest_sha256']==digest(ar_manifest_raw),'UPSTREAM_MANIFEST_IDENTITY')
        cells=execution['spec']['cells'];helpers=types.SimpleNamespace(auditor=auditor,adapter=adapter)
        public,private=retained['builder'].verify_manifest(ar_manifest,inputs,execution,args.ar1_attempt_id,cells,helpers)
        for cell in cells:
            s,h,w=(cell[k] for k in ('source','horizon','window'));cfg=inputs['spec']['sources'][s]
            stem=auditor.cell_stem(cell);n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
            def artifact(area,name):
                entry=(public if area=='public' else private)[name];raw=consume(destination/area/name,64*1024*1024)
                require(entry==dict(path=name,**identity(raw)),'AR_ARTIFACT_HASH');return raw
            trace=artifact('private',stem+'-traces.npz');auditor.check_output_headers(trace,np,n);header_count+=6
            artifact('private',stem+'-fits.json')
            receipt=json_object(artifact('public',stem+'-receipt.json'))
            auditor.verify_cell_receipt(receipt,cell,inputs,execution,
                [private[stem+'-fits.json'],private[stem+'-traces.npz']],len(range(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,cfg['refit_step'])))
            containers.append((s,h,w,None,['AR1_REPLAY'],False,trace));guard(stage='independent_coverage_headers')
        require(len(containers)==40 and header_count==588,'INPUT_INVENTORY')
        reports={};targets={};source_floors={}
        for s,h,w,parameter,methods,prefixed,raw in containers:
            cfg=inputs['spec']['sources'][s];first,last=cfg['evaluation_origin_first'],cfg['evaluation_origin_last']
            ids=np.arange(first,last+1,dtype=np.int64);refits=first+(ids-first)//cfg['refit_step']*cfg['refit_step']
            require(last+h<cfg['record_count'] and first-h-w+1>=0,'LABEL_MATURITY')
            with np.load(io.BytesIO(raw),allow_pickle=False) as saved:
                for method in methods:
                    key=(s,h,w,method);require(key not in reports,'DUPLICATE_REPORT_CELL')
                    prefix=method+'_' if prefixed else '';a={f:saved[prefix+f] for f in fields if f!='pinball'}
                    require(np.array_equal(a['origins'],ids) and np.array_equal(a['refit_indices'],refits),'PAYLOAD_ORIGINS_REFITS')
                    p,b,c=(a[f] for f in ('peak','floor','capacity'))
                    require(all(np.isfinite(v).all() for v in (p,b,c)) and bool(np.all(b>=0))
                        and bool(np.all(p>=b)) and bool(np.all(c>=b)),'PAYLOAD_FINITE_FLOOR')
                    if (s,h) in targets:require(np.array_equal(p,targets[s,h][0]) and np.array_equal(b,targets[s,h][1]),'SHARED_TARGET')
                    else:targets[s,h]=(p.copy(),b.copy())
                    if s in source_floors:require(np.array_equal(b,source_floors[s]),'SHARED_FLOOR')
                    else:source_floors[s]=b.copy()
                    if (s,6) in targets and (s,24) in targets:require(bool(np.all(targets[s,6][0]<=targets[s,24][0])),'TARGET_HORIZON_ORDER')
                    origins=list(map(int,a['origins']));hits=[float(pi)>float(ci) for pi,ci in zip(p,c)]
                    phases,value=scalar_phases(origins,hits,h)
                    reports[key]=(parameter,phases,value,sum(hits));guard(stage='independent_coverage_exact_cell')
        order=[(v['source'],v['horizon'],v['window'],m) for v in spec['configurations'] for m in METHODS]
        require(len(reports)==len(set(order))==len(order)==56 and set(reports)==set(order),'CLOSED_56_CELL_FAMILY')
        return finish_check(root,args,coverage,inputs,execution,spec,freeze,freeze_raw,static,readback_path,
            readback_raw,ar_manifest_raw,consumed,reports,order,guard,runner,diag,ar_manifest,destination,script)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0.)


def finish_check(root,args,coverage,inputs,execution,spec,freeze,freeze_raw,static,readback_path,
                 readback_raw,ar_manifest_raw,consumed,reports,order,guard,runner,diag,ar_manifest,destination,script):
    from reconcile_conditional_replication import verify_resource
    public,private=coverage/'public',coverage/'private'
    require({p.name for p in public.iterdir()}=={SUMMARY_NAME,PHASE_NAME,'coverage-evalue-manifest.json'}
        and {p.name for p in private.iterdir()}=={'input-binding.json'}
        and all(p.is_file() and not p.is_symlink() for d in (public,private) for p in d.iterdir()),'COMPLETE_OUTPUT_INVENTORY')
    manifest_raw=read(root,public/'coverage-evalue-manifest.json',within=coverage);manifest=json_object(manifest_raw)
    binding_raw=read(root,private/'input-binding.json',within=coverage);binding=json_object(binding_raw)
    expected_binding=dict(version=1,role='INPUT_BINDING_ONLY',upstream_receipt_generated=False,
        replication_dir=str(inputs['attempt'].relative_to(root)),ar1_attempt_id=args.ar1_attempt_id,
        coverage_freeze_sha256=args.freeze_sha256,coverage_spec_sha256=digest(static[SPEC]),
        base_freeze_sha256=freeze['base_freeze_sha256'],
        original_executable_freeze_sha256=inputs['archive']['executable_freeze_sha256'],
        archived_selection_sha256=inputs['archive']['selection_freeze_sha256'],new_selection_sha256=inputs['selection_hash'],
        ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
        readback=dict(path=str(readback_path.relative_to(root)),**identity(readback_raw)),
        ar1_manifest_sha256=digest(ar_manifest_raw),input_container_count=40,input_header_count=588)
    require(typed_equal(binding,expected_binding),'OUTPUT_INPUT_BINDING')
    expected=dict(version=1,status='COVERAGE_EVALUE_COMPUTATION_VERIFIED',post_result_exploratory=True,
        actual_inferential_status='Post-result exploratory on inspected records; fixed-procedure null theory is not retrospective empirical 5% familywise error control',
        inference_scope='Fixed-terminal one-sided datewise conditional strict-breach upper-bound null for the declared fixed procedure family',
        coverage_guarantee_established=False,full_filtration_anytime_claim=False,summary_rows=56,phase_rows=896,
        family_size=56,reference_threshold=1120,freeze_sha256=args.freeze_sha256,spec_sha256=digest(static[SPEC]),
        input_binding=dict(path=str((private/'input-binding.json').relative_to(root)),**identity(binding_raw)),
        input_container_count=40,input_header_count=588,raw_sources_loaded=False,models_fitted=False,
        predictions_repaired=False,new_parameter_selection=False,upstream_receipt_generated=False,
        phase_scope='All H+1 phases; original first-origin anchor; no calendar reset or selected phase',
        exact_threshold_arithmetic=True,monetary_units_pooled=False)
    require(all(type(manifest.get(k)) is type(v) and manifest.get(k)==v for k,v in expected.items()),'OUTPUT_MANIFEST_SCOPE')
    require(datetime.fromisoformat(manifest['created_utc'].replace('Z','+00:00')).tzinfo is not None,'MANIFEST_TIME')
    wanted_inputs=[dict(path=str(p.relative_to(root)),**entry) for p,(entry,_) in sorted(consumed.items())]
    require(typed_equal(manifest['input_file_identities'],wanted_inputs),'OUTPUT_CONSUMED_INPUT_BINDING')
    verify_resource(manifest['resources'])
    blobs={name:read(root,public/name,within=coverage) for name in (SUMMARY_NAME,PHASE_NAME)}
    require(typed_equal(manifest['exports'],[dict(path=name,**identity(raw)) for name,raw in blobs.items()]),'OUTPUT_EXPORT_HASHES')
    meta=('source','native_unit','horizon','window','method','parameter')
    values=('evalue_numerator_hex','evalue_denominator_hex','evalue_log10_approx','evalue_display')
    summary=csv_rows(blobs[SUMMARY_NAME],meta+('n','k','first_origin','last_origin','label_terminal_index',
        'phase_count','family_size','reference_threshold','adjusted_reference_threshold_crossed')+values,56)
    phase_rows=csv_rows(blobs[PHASE_NAME],meta+('phase','n','k','cell_adjusted_reference_threshold_crossed')+values,896)
    phase_index=0;crossings=0
    require(len({tuple(r[k] for k in ('source','horizon','window','method')) for r in summary})==56
        and len({tuple(r[k] for k in ('source','horizon','window','method','phase')) for r in phase_rows})==896,
        'UNIQUE_OUTPUT_KEYS')
    for key,row in zip(order,summary):
        s,h,w,method=key;parameter,phases,value,k=reports[key];cfg=inputs['spec']['sources'][s]
        first,last=cfg['evaluation_origin_first'],cfg['evaluation_origin_last'];n=last-first+1
        label=dict(source=s,native_unit=cfg['native_unit'],horizon=str(h),window=str(w),method=method,
            parameter='' if parameter is None else str(parameter))
        flag=value>=1120;crossings+=int(flag)
        expected_row=label|dict(n=str(n),k=str(k),first_origin=str(first),last_origin=str(last),
            label_terminal_index=str(last+h),phase_count=str(h+1),family_size='56',reference_threshold='1120',
            adjusted_reference_threshold_crossed=str(flag))
        require(all(row[k]==v for k,v in expected_row.items()),'SUMMARY_LABEL_COUNT_OR_FLAG')
        exact_fields(row,value)
        require(sum(p[1] for p in phases)==n and sum(p[2] for p in phases)==k
            and sum((p[3] for p in phases),Fraction())/(h+1)==value,'PHASE_TO_CELL_TOTALS')
        for r,pn,pk,pe in phases:
            prow=phase_rows[phase_index];phase_index+=1
            expected_phase=label|dict(phase=str(r),n=str(pn),k=str(pk),cell_adjusted_reference_threshold_crossed=str(flag))
            require(all(prow[k]==v for k,v in expected_phase.items()),'PHASE_LABEL_COUNT_OR_CELL_FLAG')
            exact_fields(prow,pe)
        guard(stage='independent_coverage_table_cell')
    require(phase_index==896 and type(manifest.get('adjusted_reference_crossings')) is int
        and manifest['adjusted_reference_crossings']==crossings,'OUTPUT_AGGREGATE_REFERENCE_CROSSINGS')
    runner.verify_inputs(inputs)
    require(read(root,FREEZE)==freeze_raw and all(read(root,n)==raw for n,raw in static.items()),'FINAL_STATIC_CHANGED')
    require(all(identity(read(root,p,cap=cap))==entry for p,(entry,cap) in consumed.items()),'FINAL_INPUT_CHANGED')
    diag.verify_exports(root,destination,ar_manifest['exports']);runner.verify_private_exports(root,destination,ar_manifest['private_exports'])
    require(read(root,public/'coverage-evalue-manifest.json')==manifest_raw
        and read(root,private/'input-binding.json')==binding_raw
        and all(read(root,public/n)==raw for n,raw in blobs.items())
        and digest(read(root,script))==args.self_sha256,'FINAL_OUTPUT_OR_CHECKER_CHANGED')
    require('coverage_evalues' not in sys.modules and 'run_coverage_evalues' not in sys.modules,'PRODUCTION_STAT_IMPORT')
    guard(stage='independent_coverage_before_receipt')
    receipt=dict(version=1,status='COVERAGE_INDEPENDENT_READBACK_PASS',verified_utc=datetime.now(timezone.utc).isoformat(),
        coverage_manifest_sha256=digest(manifest_raw),coverage_freeze_sha256=args.freeze_sha256,
        coverage_spec_sha256=digest(static[SPEC]),independent_code_sha256=args.self_sha256,
        ar1_manifest_sha256=digest(ar_manifest_raw),upstream_v2_readback_sha256=digest(readback_raw),
        summary_rows_independently_checked=56,phase_rows_independently_checked=896,
        input_containers_checked=40,input_headers_checked=588,exact_semantic_keys_checked=True,
        saved_strict_peak_greater_capacity_recomputed=True,actual_origin_phase_assignment_recomputed=True,
        exact_statistical_formula='sum(comb(n+1,j)*19**(k-j),j=0..k)/((n+1)*comb(n,k))',
        all_exact_phase_and_cell_values_checked=True,adjusted_reference_crossings=crossings,
        production_statistical_modules_imported=False,raw_sources_loaded=False,models_fitted=False,
        predictions_repaired=False,new_parameter_selection=False,post_result_exploratory=True,
        actual_inferential_status=expected['actual_inferential_status'],
        exports=[dict(path=n,**identity(raw)) for n,raw in blobs.items()],resources=dict(guard.resources))
    output=Path(args.output);output=output if output.is_absolute() else root/output
    raw=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with output.open('xb') as stream:stream.write(raw)
    require(read(root,output)==raw,'RECEIPT_READBACK')
    return receipt


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--root',default=str(ROOT))
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--replication-dir')
    parser.add_argument('--ar1-attempt-id')
    parser.add_argument('--coverage-attempt-id')
    parser.add_argument('--readback')
    parser.add_argument('--readback-sha256')
    parser.add_argument('--freeze-sha256')
    parser.add_argument('--self-sha256')
    parser.add_argument('--output')
    args=parser.parse_args(argv)
    if args.self_test:
        require(not args.execute,'SELF_TEST_EXECUTION_CONFLICT')
        print(json.dumps(artificial_check(),sort_keys=True));return 0
    if not args.execute:
        print(json.dumps({'status':'NOT_EXECUTED','financial_inputs_read':False}));return 0
    print(json.dumps(check_run(args),sort_keys=True));return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        code=str(error) if isinstance(error,CheckError) else getattr(error,'code','INDEPENDENT_READBACK_FAILURE')
        if type(code) is not str or re.fullmatch('[A-Z][A-Z0-9_]{0,63}',code) is None:
            code='INDEPENDENT_READBACK_FAILURE'
        print(json.dumps({'status':'STOPPED','stop_code':code}),file=sys.stderr)
        raise SystemExit(1)
