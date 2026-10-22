"""Recompute AR diagnostics from one explicitly audited fresh AR attempt.

Import/help are stdlib-only. No auditor, raw reader, model or repair is run.
The retained diagnostic entry and its fixed provenance remain unchanged.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import signal
import time
import types

ROOT=Path(__file__).resolve().parent
FREEZE_PATH='protocol/revision-20261022/ar1-diagnostics-reproduction-freeze.json'
RETAINED_FREEZE='protocol/revision-20261022/ar1-diagnostics-executable-freeze.json'
DESIGN_PATH='notes/revision-20261022/ar1-diagnostics-reproduction-design.md'
REFERENCE_DIR='results/revision-20261022/ar1-diagnostics'
REFERENCE_FILES=tuple(REFERENCE_DIR+'/'+n for n in
    ('ar1-floor.csv','ar1-horizon.csv','ar1-diagnostics-audit.json','independent-readback.json'))
SEEDS=(RETAINED_FREEZE,'reproduce_ar1_diagnostics.py','test_reproduce_ar1_diagnostics.py',DESIGN_PATH,*REFERENCE_FILES)


class ReproductionError(ValueError):
    def __init__(self,code):self.code=code;super().__init__(code)


def require(ok,code):
    if not ok:raise ReproductionError(code)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def read(root,path,*,within=None,cap=8*1024*1024):
    root=Path(root).absolute();p=Path(path);p=p if p.is_absolute() else root/p
    boundary=root if within is None else Path(within).absolute()
    require('..' not in p.parts and p.is_relative_to(root) and p.is_relative_to(boundary)
        and not any(q.is_symlink() for q in (p,*p.parents)) and p.is_file(),'REPRODUCTION_FILE_BOUNDARY')
    try:
        require(p.stat().st_size<=cap,'REPRODUCTION_FILE_SIZE')
        with p.open('rb') as stream:raw=stream.read(cap+1)
        require(len(raw)<=cap,'REPRODUCTION_FILE_SIZE');return raw
    except OSError:raise ReproductionError('REPRODUCTION_FILE_READ') from None


def strict_json(raw):
    def pairs(items):
        result={}
        for k,v in items:require(k not in result,'REPRODUCTION_DUPLICATE_KEY');result[k]=v
        return result
    def bad(_):raise ReproductionError('REPRODUCTION_NONFINITE_JSON')
    try:
        value=json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
        require(type(value) is dict,'REPRODUCTION_JSON_OBJECT');return value
    except (ValueError,TypeError,UnicodeError) as error:
        if isinstance(error,ReproductionError):raise
        raise ReproductionError('REPRODUCTION_JSON_INVALID') from None


def required_freeze_paths(root=ROOT):
    root=Path(root).absolute();old=strict_json(read(root,RETAINED_FREEZE))
    require(type(old.get('files')) is dict,'REPRODUCTION_RETAINED_FREEZE')
    found=set(old['files'])|set(SEEDS);pending=list(found);seen=set()
    while pending:
        name=pending.pop()
        if not name.endswith('.py') or name in seen:continue
        seen.add(name)
        try:tree=ast.parse(read(root,name),filename=name)
        except SyntaxError:raise ReproductionError('REPRODUCTION_CODE_SYNTAX') from None
        for node in ast.walk(tree):
            modules=([a.name for a in node.names] if isinstance(node,ast.Import) else
                [node.module] if isinstance(node,ast.ImportFrom) and not node.level and node.module else [])
            for module in modules:
                local=module.split('.')[0]+'.py'
                if (root/local).is_file() and local not in found:found.add(local);pending.append(local)
    return tuple(sorted(found))


def preflight(root,freeze_hash):
    root=Path(root).absolute();raw=read(root,FREEZE_PATH)
    require(type(freeze_hash) is str and re.fullmatch('[0-9a-f]{64}',freeze_hash) is not None and sha(raw)==freeze_hash,
        'REPRODUCTION_FREEZE_IDENTITY')
    spec=strict_json(raw)
    require(set(spec)=={'version','status','created_utc','retained_freeze_path','retained_freeze_sha256',
        'design_path','design_sha256','files'} and type(spec['version']) is int and spec['version']==1
        and spec['status']=='FROZEN' and spec['retained_freeze_path']==RETAINED_FREEZE
        and spec['design_path']==DESIGN_PATH and type(spec['files']) is dict,'REPRODUCTION_FREEZE_SCHEMA')
    try:stamp=datetime.fromisoformat(spec['created_utc'].replace('Z','+00:00'))
    except (ValueError,TypeError,AttributeError):raise ReproductionError('REPRODUCTION_FREEZE_TIME') from None
    require(stamp.tzinfo is not None,'REPRODUCTION_FREEZE_TIME')
    names=required_freeze_paths(root);require(set(spec['files'])==set(names),'REPRODUCTION_FREEZE_INVENTORY')
    snapshots={n:read(root,n) for n in names}
    require(all(sha(v)==spec['files'][n] for n,v in snapshots.items()),'REPRODUCTION_CODE_IDENTITY')
    require(sha(snapshots[RETAINED_FREEZE])==spec['retained_freeze_sha256']
        and sha(snapshots[DESIGN_PATH])==spec['design_sha256'],'REPRODUCTION_CONTRACT_IDENTITY')
    builder=types.ModuleType('_checked_retained_ar_diagnostics');builder.__file__=str(root/'build_ar1_diagnostics.py')
    exec(compile(snapshots['build_ar1_diagnostics.py'],builder.__file__,'exec'),builder.__dict__)
    retained=builder.preflight(root,spec['retained_freeze_sha256'])
    expected=set(builder.required_freeze_paths(root))|set(SEEDS)
    require(expected==set(names),'REPRODUCTION_IMPORT_CLOSURE')
    reference=strict_json(snapshots[REFERENCE_DIR+'/ar1-diagnostics-audit.json'])
    expected=dict(version=1,status='AR1_DIAGNOSTICS_VERIFIED',floor_rows=8,horizon_rows=4,
        diagnostic_freeze_sha256=spec['retained_freeze_sha256'],
        ar1_manifest_sha256=retained['plan']['ar1_manifest_sha256'],
        plan=dict(path=builder.PLAN_PATH,bytes=len(retained['snapshots'][builder.PLAN_PATH]),
            sha256=sha(retained['snapshots'][builder.PLAN_PATH])),
        source_loaded=False,models_fitted=False,forecasts_repaired=False,new_model_selection=False)
    require(all(type(reference.get(k)) is type(v) and reference.get(k)==v for k,v in expected.items()),
        'REPRODUCTION_REFERENCE_AUDIT')
    require(reference.get('exports')==[dict(path=n,bytes=len(snapshots[REFERENCE_DIR+'/'+n]),
        sha256=sha(snapshots[REFERENCE_DIR+'/'+n])) for n in ('ar1-floor.csv','ar1-horizon.csv')],
        'REPRODUCTION_REFERENCE_EXPORTS')
    return dict(root=root,raw=raw,hash=freeze_hash,spec=spec,snapshots=snapshots,builder=builder,retained=retained)


def verify_static(frozen):
    require(read(frozen['root'],FREEZE_PATH)==frozen['raw'],'REPRODUCTION_FREEZE_CHANGED')
    require(all(read(frozen['root'],n)==v for n,v in frozen['snapshots'].items()),'REPRODUCTION_STATIC_CHANGED')


def fresh_readback(frozen,path,expected_hash):
    root=frozen['root'];p=Path(path);p=p if p.is_absolute() else root/p
    raw=read(root,p,within=root/'state/revision-20261022')
    require(p.suffix=='.json' and type(expected_hash) is str and re.fullmatch('[0-9a-f]{64}',expected_hash) is not None
        and sha(raw)==expected_hash,'REPRODUCTION_READBACK_IDENTITY')
    receipt=strict_json(raw);plan=frozen['retained']['plan']
    expected=dict(version=2,status='AR1_INDEPENDENT_READBACK_PASS',ar1_spec_sha256=plan['ar1_spec_sha256'],
        ar1_freeze_sha256=plan['ar1_freeze_sha256'],cells=8,aggregate_rows_independently_checked=192,
        exact_fraction_fits=24,scalar_recursive_reports=24,exact_unique_csv_keys_checked=True,
        all_consumed_exports_bound_to_manifest=True,new_model_selection=False,original_models_refitted=False,
        source_values_public=False,code_sha256=sha(frozen['snapshots']['verify_ar1_output.py']))
    require(all(type(receipt.get(k)) is type(v) and receipt.get(k)==v for k,v in expected.items()),
        'REPRODUCTION_READBACK_CONTRACT')
    return p,raw,receipt


def compare_tables(helpers,frozen,rows):
    comparisons={}
    for name,new_rows in rows.items():
        original=frozen['snapshots'][REFERENCE_DIR+'/'+name];old=helpers.diag._rows(original)
        keys=('source','horizon','window','method') if name=='ar1-floor.csv' else ('source','window','method')
        labels=('source','native_unit','window','method','status','first_source_index','last_source_index','origin_count')
        labels+=('horizon','parameter') if name=='ar1-floor.csv' else ('parameter_h6','parameter_h24','short_horizon','long_horizon')
        text=lambda value:'' if value is None else str(value)
        expected={tuple(text(row[k]) for k in keys):{k:text(row[k]) for k in labels} for row in new_rows}
        require(len(old)==len(new_rows) and all(list(row)==list(new_rows[0]) for row in old)
            and len({tuple(row.get(k) for k in keys) for row in old})==len(old)
            and all(tuple(row.get(k) for k in keys) in expected and
                all(row.get(k)==v for k,v in expected[tuple(row.get(k) for k in keys)].items()) for row in old),
            'REPRODUCTION_REFERENCE_INVENTORY')
        comparisons[name]=helpers.adapter.compare_csv(helpers.adapter.csv_bytes(new_rows),original)
    return dict(version=1,status='DIAGNOSTIC_TABLE_COMPARISON_RECORDED',tables=comparisons,
        exact_csv_byte_agreement=all(v['byte_identical'] for v in comparisons.values()),
        exact_csv_scalar_agreement=all(v['exact_scalar_agreement'] for v in comparisons.values()),
        policy='All public cells compared exactly; verification does not imply numerical agreement')


def execute(root,replication_dir,ar_id,readback_path,readback_hash,diagnostic_id,freeze_hash,
            *,context_provider=None,guard_factory=None):
    started=time.monotonic();root=Path(root).absolute();production=context_provider is None
    require(type(ar_id) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,63}',ar_id) is not None
        and type(diagnostic_id) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,63}',diagnostic_id) is not None,
        'REPRODUCTION_ATTEMPT_ID')
    require(not production or guard_factory is None,'REPRODUCTION_TEST_ONLY_GUARD')
    require(not production or platform.system()=='Darwin','REPRODUCTION_DARWIN_REQUIRED')
    if production:signal.signal(signal.SIGALRM,signal.SIG_DFL);signal.setitimer(signal.ITIMER_REAL,600.)
    try:
        frozen=preflight(root,freeze_hash);b=frozen['builder'];retained=frozen['retained']
        readback,readback_raw,receipt=fresh_readback(frozen,readback_path,readback_hash)
        require(time.monotonic()-started<540.,'RESOURCE_WALL')
        with b.load_helpers(retained,allow_preloaded=not production) as h:
            inputs,execution=(b._context if production else context_provider)(h,root,replication_dir)
            plan=retained['plan'];cells=[dict(source=s,horizon=horizon,window=w)
                for s,c in plan['sources'].items() for horizon in (6,24) for w in c['windows']]
            attempt=Path(inputs['attempt']).absolute()
            require(inputs['root']==root and attempt.is_relative_to(root) and attempt.is_dir()
                and re.fullmatch(r'\.scratch/revision-20261022/replication-[A-Za-z0-9][A-Za-z0-9_-]{0,63}',
                    str(attempt.relative_to(root))) is not None
                and not any(p.is_symlink() for p in (attempt,*attempt.parents)),'REPRODUCTION_REPLICA_BOUNDARY')
            require(execution['spec']['cells']==cells and execution['spec_sha256']==plan['ar1_spec_sha256']
                and execution['freeze_sha256']==plan['ar1_freeze_sha256']
                and inputs['archive']['executable_freeze_sha256']==plan['original_executable_freeze_sha256']
                and inputs['archive']['selection_freeze_sha256']==plan['original_selection_sha256'],
                'REPRODUCTION_CONTEXT_CONTRACT')
            destination=attempt/('ar1-replay-'+ar_id);output=attempt/('ar1-diagnostics-reproduction-'+diagnostic_id)
            public_out,private_out=h.resource.create_attempt(output)
            guard=(h.resource.RunGuard if guard_factory is None else guard_factory)(started,
                datetime.now(timezone.utc).isoformat(),output,public_out,private_out)
            written=[];floors=[];pairs=[];blobs={}
            def write(path,raw,*,public=False):
                with path.open('xb') as stream:
                    if public:written.append(path.name)
                    stream.write(raw)
                require(read(root,path,within=output)==raw,'REPRODUCTION_OUTPUT_READBACK')
            try:
                guard(stage='ar1_diagnostic_reproduction_start');h.adapter.verify_resource(receipt['resources'])
                manifest_raw=read(root,destination/'public/ar1-replay-manifest.json',within=destination)
                require(receipt.get('ar1_manifest_sha256')==sha(manifest_raw),'REPRODUCTION_READBACK_MANIFEST')
                manifest=strict_json(manifest_raw)
                public,private=b.verify_manifest(manifest,inputs,execution,ar_id,cells,h)
                summary=b.summary_inventory(h.auditor.load_verified_csv(root,destination,public['ar1-summary.csv']),cells,plan)
                def ident(raw,path):return dict(path=str(path.relative_to(root)),bytes=len(raw),sha256=sha(raw))
                binding=dict(version=1,role='INPUT_BINDING_ONLY',upstream_receipt_generated=False,
                    replication_dir=str(attempt.relative_to(root)),ar1_attempt_id=ar_id,
                    readback=ident(readback_raw,readback),manifest=ident(manifest_raw,destination/'public/ar1-replay-manifest.json'),
                    reproduction_freeze_sha256=freeze_hash,retained_freeze_sha256=frozen['spec']['retained_freeze_sha256'],
                    ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
                    original_selection_sha256=plan['original_selection_sha256'],new_selection_sha256=inputs['selection_hash'])
                binding_raw=h.rep.json_bytes(binding);binding_path=private_out/'input-binding.json';write(binding_path,binding_raw)
                vectors={};consumed=[]
                for cell in cells:
                    s,horizon,w=(cell[k] for k in ('source','horizon','window'))
                    v=b.load_cell(h,retained,inputs,execution,destination,cell,public,private)
                    row=b.floor_row(h,cell,plan['sources'][s],v)
                    require(row['floor_binding_breach_count']+row['other_issue_breach_count']==
                        int(summary[s,str(horizon),str(w)]['strict_breach_count']),'REPRODUCTION_BREACH_RECONCILIATION')
                    floors.append(row);vectors[s,horizon,w]=v;stem=h.auditor.cell_stem(cell)
                    consumed.append(dict(cell=cell,receipt=public[stem+'-receipt.json'],trace=private[stem+'-traces.npz']))
                    guard.arrays(vectors);guard(stage='ar1_diagnostic_reproduction_cell',cell_id=stem)
                require(len(floors)==8 and len({(r['source'],r['horizon'],r['window']) for r in floors})==8,
                    'REPRODUCTION_FLOOR_INVENTORY')
                pairs=b.horizon_rows(h,cells,plan,vectors)
                rows={'ar1-floor.csv':floors,'ar1-horizon.csv':pairs};comparison=compare_tables(h,frozen,rows)
                blobs={n:h.adapter.csv_bytes(r) for n,r in rows.items()}
                blobs['ar1-diagnostics-comparison.json']=h.rep.json_bytes(comparison)
                for name,raw in blobs.items():write(public_out/name,raw,public=True)
                guard(stage='ar1_diagnostic_reproduction_final')
                h.runner.verify_inputs(inputs);verify_static(frozen)
                require(read(root,readback,within=root/'state/revision-20261022')==readback_raw,
                    'REPRODUCTION_READBACK_CHANGED')
                require(read(root,destination/'public/ar1-replay-manifest.json',within=destination)==manifest_raw,
                    'REPRODUCTION_MANIFEST_CHANGED')
                h.diag.verify_exports(root,destination,manifest['exports'])
                h.runner.verify_private_exports(root,destination,manifest['private_exports'])
                require(read(root,binding_path,within=output)==binding_raw,'REPRODUCTION_BINDING_CHANGED')
                require(all(read(root,public_out/n,within=output)==raw for n,raw in blobs.items()),
                    'REPRODUCTION_EXPORT_CHANGED')
                audit=dict(version=1,status='AR1_DIAGNOSTIC_REPRODUCTION_VERIFIED',created_utc=h.rep.utc_now(),
                    floor_rows=8,horizon_rows=4,exact_csv_byte_agreement=comparison['exact_csv_byte_agreement'],
                    exact_csv_scalar_agreement=comparison['exact_csv_scalar_agreement'],input_binding=ident(binding_raw,binding_path),
                    freeze_sha256=freeze_hash,retained_freeze_sha256=frozen['spec']['retained_freeze_sha256'],
                    reference_audit=ident(frozen['snapshots'][REFERENCE_DIR+'/ar1-diagnostics-audit.json'],
                        root/REFERENCE_DIR/'ar1-diagnostics-audit.json'),input_artifacts=consumed,
                    upstream_receipt_generated=False,source_loaded=False,models_fitted=False,forecasts_repaired=False,
                    original_outputs_modified=False,new_model_selection=False,new_population_inference=False,
                    numerical_scope='Retained fresh vectors and exact public-cell comparison; upstream source/OLS/replay proof is not repeated',
                    exports=[dict(path=n,bytes=len(raw),sha256=sha(raw)) for n,raw in blobs.items()],resources=dict(guard.resources))
                write(public_out/'ar1-diagnostics-reproduction-audit.json',h.rep.json_bytes(audit),public=True)
                return audit
            except Exception as error:
                code=b.safe_code(error)
                for name in written:
                    p=public_out/name
                    if p.is_file():p.rename(private_out/('unverified-'+name))
                h.rep.write_json(private_out/'partial-aggregates.json',dict(floor_rows=floors,horizon_rows=pairs),exclusive=True)
                h.rep.write_json(public_out/'ar1-diagnostics-reproduction-failure.json',dict(version=1,status='STOPPED',
                    stop_code=code,complete_reproduction=False,shortened_segment_published=False,
                    completed_floor_rows=len(floors),completed_horizon_rows=len(pairs),resources=dict(guard.resources)),exclusive=True)
                raise ReproductionError(code) from None
    except ReproductionError:raise
    except Exception:raise ReproductionError('REPRODUCTION_FAILED') from None
    finally:
        if production:signal.setitimer(signal.ITIMER_REAL,0.)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('replication-dir','ar1-attempt-id','readback','readback-sha256','diagnostic-id','freeze'):
        parser.add_argument('--'+name,required=True)
    args=parser.parse_args(argv)
    try:
        result=execute(ROOT,args.replication_dir,args.ar1_attempt_id,args.readback,args.readback_sha256,args.diagnostic_id,args.freeze)
        print(json.dumps({k:result[k] for k in ('status','floor_rows','horizon_rows','exact_csv_scalar_agreement')},indent=2));return 0
    except ReproductionError as error:
        print(json.dumps(dict(status='STOPPED',stop_code=error.code,verified=False)));return 1


if __name__=='__main__':raise SystemExit(main())
