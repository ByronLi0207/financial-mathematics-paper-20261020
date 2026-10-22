"""Run one separately frozen exploratory AR(1) block-replay addition.

Explicit successful replication and a fresh attempt ID are required. Import and
--help use only the standard library. No fetch, original refit, parameter menu,
old-output write, or shortened failed-cell score is provided.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import importlib.util
import math
import os
from pathlib import Path
import platform
import re
import signal
import sys
import time

import reproduce_conditional as rep
import reproduce_conditional_diagnostics as diag
import reconcile_conditional_replication as adapter

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SPEC_PATH = 'protocol/revision-20261022/ar1-replay-spec.json'
FREEZE_PATH = 'protocol/revision-20261022/ar1-replay-executable-freeze.json'
METHOD = 'AR1_REPLAY'
COMPARATORS = ('frozen_S', 'frozen_F', 'QR')
DESIGN_PATH = 'protocol/revision-20261022/ar1-replay-design.md'
DEPENDENCIES = ('run_ar1_replay.py','ar1_replay.py','reproduce_conditional.py',
    'reproduce_conditional_diagnostics.py','reconcile_conditional_replication.py',
    'conditional_sources.py','conditional_study.py','conditional_features.py',
    'conditional_quantile.py','run_conditional_study.py','study_core.py','run_study.py',
    'results/revision-20261022/audit-builder-v01.py')
TEST_FILES = ('test_ar1_replay.py','test_run_ar1_replay.py')
RESOURCES = dict(wall_seconds=540,hard_seconds=600,rss_bytes=1610612736,
    requested_threads=1,maximum_observed_os_threads=2)
NUMERICAL_CONTRACT = dict(
    fit='intercept OLS on W+H-1 unique adjacent transitions in N_a..N_r; power-of-two common scale and anchor-centered cross-products',
    normal_tolerance_multiplier=1e-10,rank=[19,20],
    phi_policy='finite unrestricted; exact1=S branch; no clipping',
    failure='whole cell; no shortened score or fallback',
    phase='post-result exploratory; original primaries unchanged')


def require(condition, code):
    if not condition:
        raise rep.ReproductionError(code)


def prepare_replica(root, replication_dir, *, archive_contract=None):
    """Read-only replica identity, independent of the old diagnostic output lock."""
    try:
        root, attempt = diag._attempt(root, replication_dir)
        archive = rep.verify_archive(root, contract=archive_contract)
        require(archive['verified_result_files'] == 69, 'ARCHIVE_INVENTORY')
        spec=archive['spec'];snapshots={}
        def read(path, *, cap=8*1024*1024, within=None):
            p=rep.project_file(root,path,within=within)
            raw=rep.read_bytes(root,p,cap=cap,within=within)
            name=str(p.relative_to(root));found=diag.file_identity(raw)
            if name in snapshots:require(found==snapshots[name]['identity'],'INPUT_SNAPSHOT_CHANGED')
            snapshots[name]=dict(identity=found,cap=cap,within_attempt=within is not None)
            return raw
        controller=rep.strict_json(read(attempt/'controller-final.json',within=attempt))
        require(type(controller.get('version')) is int and controller['version']==1
            and controller.get('status')=='REPLICATION_AUDITED' and controller.get('stop_code') is None
            and controller.get('accuracy_recomputed') is True and controller.get('selection_agrees_with_archive') is True
            and controller.get('attempt_path')==str(attempt.relative_to(root))
            and controller.get('executable_freeze_sha256')==archive['executable_freeze_sha256']
            and controller.get('archived_selection_sha256')==archive['selection_freeze_sha256']
            and all(controller.get(k)==n for k,n in (('completed_validation_cells',24),
                ('completed_evaluation_reference_cells',32),('validation_jobs_retained',24),
                ('evaluation_reference_jobs_retained',32))), 'CONTROLLER_NOT_AUDITED')
        selection_path=attempt/'selection-freeze.json'
        selection_raw=read(selection_path,within=attempt);selection_hash=rep.sha(selection_raw)
        require(controller.get('selection_path')==str(selection_path.relative_to(root))
            and controller.get('selection_sha256')==selection_hash
            and selection_hash!=archive['selection_freeze_sha256'],'SELECTION_SNAPSHOT_HASH')
        selection=rep.strict_json(selection_raw)
        def lookup(path,key):
            expected=rep.worker_directory(attempt,('validation',*key))/'public/manifest.json'
            require(path==str(expected.relative_to(root)),'NEW_VALIDATION_PATH')
            return read(expected,within=attempt)
        rep.verify_selection(selection,spec,archive['executable_freeze_sha256'],lookup)
        require(diag._matrix(selection['cells'])==diag._matrix(archive['selection']['cells'])
            and len(selection['cells'])==24 and all(c['status']=='SELECTED' for c in selection['cells']),
            'SELECTION_CHANGED')
        selected={(c['source'],c['horizon'],c['window'],c['family']):c for c in selection['cells']}
        cells,expected_rows=diag._inventory(spec,selected)
        require(spec['horizons']==[6,24],'HORIZON_INVENTORY')
        validation=diag._queue(read(attempt/'validation-queue.json',within=attempt),
            rep.phase_jobs(spec,'validation'),root,attempt)
        for queued,chosen in zip(validation,selection['cells']):
            ref=chosen['validation_receipts'][0]
            require((queued['receipt_path'],queued['receipt_sha256'])==(ref['path'],ref['sha256']),
                'VALIDATION_QUEUE_HASH')
        queue_path=attempt/'evaluation-queue.json';queue_raw=read(queue_path,within=attempt)
        require(controller.get('queue_path')==str(queue_path.relative_to(root)),'CONTROLLER_QUEUE_PATH')
        queue=diag._queue(queue_raw,cells,root,attempt)
        audit_output=attempt/'numerical-audit/public';comparison_path=audit_output/'reproduction-comparison.json'
        ca=controller['audit']
        require(ca.get('status')=='NUMERICAL_AUDIT_VERIFIED'
            and ca.get('comparison_path')==str(comparison_path.relative_to(root)),'NUMERICAL_AUDIT_PATH')
        comparison=rep.strict_json(read(comparison_path,within=attempt))
        require(type(comparison.get('version')) is int and comparison['version']==1
            and comparison.get('status')=='NUMERICAL_AUDIT_VERIFIED'
            and comparison.get('archived_selection_sha256')==archive['selection_freeze_sha256']
            and comparison.get('new_selection_sha256')==selection_hash
            and comparison.get('selection_status_parameter_matrix_identical') is True
            and comparison.get('queue_sha256')==rep.sha(queue_raw)
            and comparison.get('source_identities')=={s:{k:c[k] for k in ('sha256','bytes','record_count','native_unit')}
                for s,c in spec['sources'].items()}
            and (comparison.get('summary_rows'),comparison.get('annual_rows'),comparison.get('paired_rows'),
                comparison.get('paired_annual_rows'))==(90,372,98,388),'NUMERICAL_AUDIT_RECEIPT')
        adapter.verify_resource(comparison['audit_resources'])
        names=list(diag.TABLE_COUNTS)+[diag._receipt_name(c) for c in cells]
        exports=comparison['exports'];receipt_exports=comparison['receipts']
        require([e.get('path') for e in exports]==names and len(set(names))==38
            and [e.get('public_file') for e in receipt_exports]==names[6:],'NUMERICAL_EXPORT_INVENTORY')
        exported={}
        for entry in exports:
            name=entry['path'];raw=read(audit_output/name,within=attempt)
            require(entry==dict(path=name,**diag.file_identity(raw)),'NUMERICAL_EXPORT_HASH')
            exported[name]=raw
        tables={}
        for name,count in diag.TABLE_COUNTS.items():
            require(len(diag._rows(exported[name]))==count,'NUMERICAL_TABLE_INVENTORY')
            tables[name]=adapter.compare_csv(exported[name],read(rep.RESULTS+'/'+name))
        require(comparison.get('tables')==tables,'NUMERICAL_TABLE_COMPARISON')
        for label,key in (('exact_csv_byte_agreement','byte_identical'),('exact_csv_scalar_agreement','exact_scalar_agreement')):
            found=all(t[key] for t in tables.values())
            require(comparison.get(label) is found and ca.get(label) is found,'NUMERICAL_AGREEMENT_FLAGS')
        for queued,cell,entry in zip(queue,cells,receipt_exports):
            name=diag._receipt_name(cell);raw=read(queued['receipt_path'],within=attempt)
            require(entry==dict(public_file=name,**diag.file_identity(exported[name]))
                and queued['receipt_sha256']==rep.sha(exported[name]) and raw==exported[name],
                'AUDITED_RECEIPT_HASH')
        diag._check_labels(diag._rows(exported['evaluation-summary.csv']),expected_rows)
        return dict(root=root,attempt=attempt,archive=archive,archive_contract=archive_contract,
            spec=spec,controller=controller,comparison=comparison,selection=selection,
            selection_hash=selection_hash,selected=selected,cells=cells,queue=queue,
            expected_rows=expected_rows,summary=diag._rows(exported['evaluation-summary.csv']),
            exported_receipts={n:exported[n] for n in names[6:]},snapshots=snapshots)
    except rep.ReproductionError:raise
    except (KeyError,TypeError,ValueError,AttributeError,IndexError,OSError,OverflowError):
        raise rep.ReproductionError('AR1_REPLICA_CONTEXT') from None


def verify_inputs(inputs):
    diag.verify_snapshots(inputs)


def verify_execution(inputs):
    """Verify exact new specification/code bytes before numeric helper execution."""
    try:
        root=inputs['root'];archive=inputs['archive']
        def read(path):
            raw=rep.read_bytes(root,path)
            found=diag.file_identity(raw)
            if path in inputs['snapshots']:
                require(found==inputs['snapshots'][path]['identity'],'INPUT_SNAPSHOT_CHANGED')
            inputs['snapshots'][path]=dict(identity=found,cap=8*1024*1024,within_attempt=False)
            return raw
        spec_raw=read(SPEC_PATH);spec=rep.strict_json(spec_raw)
        require(set(spec)=={'version','experiment','design','original_executable_freeze_sha256',
            'original_selection_sha256','method','comparators','cells','resources','dependencies','numerical_contract'},
            'AR1_SPEC_KEYS')
        expected_cells=[dict(source=s,horizon=h,window=w) for s,cfg in inputs['spec']['sources'].items()
            for h in inputs['spec']['horizons'] for w in cfg['windows']]
        require(type(spec['version']) is int and spec['version']==1
            and spec['experiment']=='AR1_REPLAY_EXPLORATORY_V1' and spec['method']==METHOD
            and spec['comparators']==list(COMPARATORS) and spec['cells']==expected_cells and len(expected_cells)==8
            and spec['original_executable_freeze_sha256']==archive['executable_freeze_sha256']
            and spec['original_selection_sha256']==archive['selection_freeze_sha256']
            and spec['resources']==RESOURCES and spec['numerical_contract']==NUMERICAL_CONTRACT,'AR1_SPEC_CONTRACT')
        # JSON bools compare equal to ints in Python; reject such mislabeled limits.
        require(all(type(spec['resources'][k]) is int for k in RESOURCES)
            and all(type(c['horizon']) is int and type(c['window']) is int for c in spec['cells'])
            and type(spec['numerical_contract']['normal_tolerance_multiplier']) is float
            and all(type(v) is int for v in spec['numerical_contract']['rank']),'AR1_SPEC_TYPES')
        design=spec['design'];require(set(design)=={'path','bytes','sha256'} and design['path']==DESIGN_PATH,
            'AR1_DESIGN_IDENTITY')
        require(design==dict(path=DESIGN_PATH,**diag.file_identity(read(DESIGN_PATH))),'AR1_DESIGN_IDENTITY')
        require(set(spec['dependencies'])==set(DEPENDENCIES),'AR1_DEPENDENCY_INVENTORY')
        for name in DEPENDENCIES:
            require(spec['dependencies'][name]==diag.file_identity(read(name)),'AR1_DEPENDENCY_HASH')
        freeze_raw=read(FREEZE_PATH);freeze=rep.strict_json(freeze_raw)
        files=set(DEPENDENCIES)|set(TEST_FILES)|{DESIGN_PATH,SPEC_PATH}
        require(set(freeze)=={'version','status','created_utc','spec_path','spec_sha256','files'}
            and type(freeze['version']) is int and freeze['version']==1 and freeze['status']=='FROZEN'
            and type(freeze['created_utc']) is str
            and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',freeze['created_utc']) is not None
            and freeze['spec_path']==SPEC_PATH and freeze['spec_sha256']==rep.sha(spec_raw)
            and set(freeze['files'])==files,'AR1_EXECUTABLE_FREEZE')
        for name in files:require(freeze['files'][name]==rep.sha(read(name)),'AR1_EXECUTABLE_HASH')
        return dict(spec=spec,spec_sha256=rep.sha(spec_raw),freeze_sha256=rep.sha(freeze_raw))
    except rep.ReproductionError:raise
    except (KeyError,TypeError,ValueError,AttributeError,OSError,OverflowError):
        raise rep.ReproductionError('AR1_EXECUTABLE_FREEZE') from None


def load_sources(inputs):
    """Read only the two exact local snapshots; never fetch or repair them."""
    from conditional_sources import load_source
    from run_conditional_study import _validate_source
    sources={}
    for source_id,cfg in inputs['spec']['sources'].items():
        path=rep.project_file(inputs['root'],cfg['input_relative_path'])
        raw=rep.read_bytes(inputs['root'],path,cap=25*1024*1024)
        found=diag.file_identity(raw)
        require(found==dict(bytes=cfg['bytes'],sha256=cfg['sha256']),'SOURCE_IDENTITY')
        name=str(path.relative_to(inputs['root']))
        inputs['snapshots'][name]=dict(identity=found,cap=25*1024*1024,within_attempt=False)
        del raw
        source=load_source(path,source_id,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
        _validate_source(source,cfg,source_id)
        sources[source_id]=source
    return sources


def audit_references(inputs,sources,np,helpers,*,checkpoint=lambda **kwargs:None,arrays=lambda *values:None):
    """Audit all32 actual cells, keeping only the24 matched reference scores."""
    kept={};receipts=[];summary=[]
    for queued,cell in zip(inputs['queue'],inputs['cells']):
        phase,s,h,w,f=cell;cfg=inputs['spec']['sources'][s]
        raw=diag._consume(inputs,queued['receipt_path'])
        require(raw==inputs['exported_receipts'][diag._receipt_name(cell)],'AUDITED_RECEIPT_HASH')
        receipt=rep.strict_json(raw)
        path=rep.project_file(inputs['root'],queued['receipt_path'],within=inputs['attempt'])
        trace_path=path.parent.parent/'private/numeric-traces.npz'
        trace=diag._consume(inputs,trace_path,cap=64*1024*1024)
        methods=diag._methods(inputs['spec'],cell)
        wanted={m+'_'+name for m in methods for name in ('origins','peak','floor','refit_indices','capacity','pinball')}
        count=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
        diag._check_trace_headers(trace,wanted,np,count)
        require(receipt['artifacts']==[dict(area='private',name='numeric-traces.npz',**diag.file_identity(trace))],
            'NPZ_IDENTITY')
        del trace
        audited=adapter.audit_cell(inputs['root'],inputs['attempt'],queued,inputs['spec'],inputs['selected'],
            inputs['archive']['executable_freeze_sha256'],inputs['selection_hash'],sources[s],np,helpers,
            lambda:checkpoint(stage='audit_original_references'))
        require(audited['receipt_raw']==raw,'AUDITED_RECEIPT_HASH')
        summary.extend(audited['summary'])
        for method in COMPARATORS:
            if method in audited['scores']:
                key=(s,h,w,method)
                require(key not in kept,'REFERENCE_DUPLICATE')
                kept[key]=audited['scores'][method]
        receipts.append(dict(cell=dict(zip(('phase','source','horizon','window','family'),cell)),
            receipt_sha256=rep.sha(raw),trace_sha256=receipt['artifacts'][0]['sha256']))
        arrays(kept,sources,audited['scores'])
        checkpoint(stage='audit_original_references')
    expected={(s,h,w,m) for s,cfg in inputs['spec']['sources'].items()
        for h in inputs['spec']['horizons'] for w in cfg['windows'] for m in COMPARATORS}
    require(set(kept)==expected and len(kept)==24 and len(receipts)==32,'REFERENCE_INVENTORY')
    require(diag._rows(adapter.csv_bytes(summary))==inputs['summary'],'REFERENCE_SUMMARY_AGREEMENT')
    return kept,receipts


def run_cell(source,cfg,horizon,window,*,checkpoint=lambda **kwargs:None,arrays=lambda *values:None):
    """Serial native AR forecasts; a failure retains only a private prefix."""
    import numpy as np
    import ar1_replay as ar
    from conditional_study import score_predictions,summarize_scores
    first,last=cfg['evaluation_origin_first'],cfg['evaluation_origin_last']
    origins=np.arange(first,last+1,dtype=np.int64);capacity=[];refits=[];fits=[];history=None
    failure=None
    for t in origins:
        t=int(t);r=first+(t-first)//cfg['refit_step']*cfg['refit_step']
        try:
            # The guard invokes an OS thread probe and directory byte scan.
            # Bound the unchecked interval without spawning a probe per query.
            resource_check=history is None or history.refit!=r or (t-first)%128==0
            if resource_check:checkpoint(stage='ar1_cell',completed_origins=len(capacity))
            if history is None or history.refit!=r:
                history=ar.prepare_ar1_history(source.position,r,horizon,window)
                require((history.first_origin,history.last_origin,history.rank)==
                    (r-horizon-window+1,r-horizon,math.ceil((window+1)*19/20)), 'AR1_HISTORY_CONTRACT')
                fit=asdict(history.fit)
                require(fit['transition_count']==window+horizon-1,'AR1_FIT_TRANSITIONS')
                fits.append(dict(refit_index=r,first_origin=history.first_origin,
                    last_origin=history.last_origin,horizon=horizon,window=window,rank=history.rank,**fit))
            value=ar.predict(history,float(source.position[t]))
            require(type(value) is float and math.isfinite(value) and value>=abs(float(source.position[t])),
                'AR1_REPORT_CONTRACT')
            capacity.append(value);refits.append(r)
            # Growing scalar lists contain no NumPy allocation; RSS is measured
            # by the guard. Do not recursively rescan those lists each query.
            if resource_check:arrays(source.position,history)
        except ar.AR1Error as error:
            failure=dict(status='FAILED',code=error.code,failed_issue_index=t,refit_index=r,
                completed_origins=len(capacity),expected_origins=len(origins))
            break
    ids=origins[:len(capacity)]
    trace=dict(origins=np.asarray(ids,dtype=np.int64),capacity=np.asarray(capacity,dtype=np.float64),
        refit_indices=np.asarray(refits,dtype=np.int64))
    if failure is not None:return None,trace,fits,failure
    require(len(capacity)==len(origins),'AR1_ORIGIN_INVENTORY')
    # Independent direct source labels; no new label or forecast selection.
    peak=np.array([max(abs(float(v)) for v in source.position[int(t):int(t)+horizon+1]) for t in origins],dtype=np.float64)
    floor=np.abs(source.position[origins]);scores=score_predictions(peak,trace['capacity'],floor,origins)
    trace.update(peak=peak,floor=floor,pinball=scores.pinball)
    arrays(source.position,history,trace,scores)
    checkpoint(stage='ar1_cell_scored',completed_origins=len(capacity))
    return summarize_scores(scores),trace,fits,None


def describe_pair(left,right,issue_dates,*,horizon):
    from conditional_study import paired_comparison
    return paired_comparison(left,right,issue_dates,horizon=horizon)


def describe_scores(trace,issue_dates,horizon):
    import numpy as np
    from conditional_study import score_predictions,summarize_scores,nonoverlap_origins
    scores=score_predictions(trace['peak'],trace['capacity'],trace['floor'],trace['origins'])
    years=issue_dates.astype('datetime64[Y]');annual=[]
    for year in np.unique(years):
        mask=years==year
        part=score_predictions(trace['peak'][mask],trace['capacity'][mask],trace['floor'][mask],trace['origins'][mask])
        annual.append(dict(calendar_year=str(year),**summarize_scores(part)))
    grid=nonoverlap_origins(int(trace['origins'][0]),int(trace['origins'][-1]),horizon)
    mask=np.isin(trace['origins'],grid)
    part=score_predictions(trace['peak'][mask],trace['capacity'][mask],trace['floor'][mask],trace['origins'][mask])
    return scores,annual,dict(stride_records=horizon+1,**summarize_scores(part))


def safe_code(error):
    code=getattr(error,'code','AR1_EXECUTION_FAILED')
    return code if type(code) is str and re.fullmatch('[A-Z][A-Z0-9_]{0,63}',code) else 'AR1_EXECUTION_FAILED'


def _write_bytes(path,raw):
    with path.open('xb') as stream:stream.write(raw)
    return dict(path=path.name,**diag.file_identity(raw))


def verify_private_exports(root,destination,entries):
    for entry in entries:
        raw=rep.read_bytes(root,Path(destination)/'private'/entry['path'],within=destination,cap=64*1024*1024)
        require(entry==dict(path=entry['path'],**diag.file_identity(raw)),'AR1_PRIVATE_EXPORT_CHANGED')


def _phi_summary(fits):
    values=[r['phi'] for r in fits]
    if not values:
        return dict(completed_refit_count=0,phi_min=None,phi_max=None,phi_mean=None,
            phi_below_zero=0,phi_exactly_one=0,phi_above_one=0)
    try:mean=math.fsum(v/len(values) for v in values)
    except OverflowError:mean=None
    return dict(completed_refit_count=len(values),phi_min=min(values),phi_max=max(values),
        phi_mean=mean,phi_below_zero=sum(v<0 for v in values),phi_exactly_one=sum(v==1 for v in values),
        phi_above_one=sum(v>1 for v in values))


def execute(root,replication_dir,attempt_id,*,archive_contract=None,guard_factory=None,started=None):
    """Execute only the separately frozen8 cells; injection is synthetic-test-only."""
    started=time.monotonic() if started is None else started
    production=archive_contract is None
    require(not production or guard_factory is None,'TEST_ONLY_GUARD')
    require(not production or platform.system()=='Darwin','DARWIN_REQUIRED')
    require(type(attempt_id) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',attempt_id) is not None,
        'AR1_ATTEMPT_ID')
    inputs=prepare_replica(root,replication_dir,archive_contract=archive_contract)
    execution=verify_execution(inputs)
    require(time.monotonic()-started<540.,'RESOURCE_WALL')
    require(importlib.util.find_spec('numpy') is not None,'NUMPY_REQUIRED_NO_INSTALL')
    for name in rep.THREAD_NAMES:os.environ[name]='1'
    import numpy as np
    from run_study import RunGuard,create_attempt
    destination=inputs['attempt']/('ar1-replay-'+attempt_id)
    require(not destination.exists() and not destination.is_symlink(),'AR1_OUTPUT_EXISTS')
    try:public,private=create_attempt(destination)
    except Exception as error:raise rep.ReproductionError(safe_code(error)) from None
    guard=(RunGuard if guard_factory is None else guard_factory)(started,rep.utc_now(),destination,public,private)
    exports=[];private_exports=[];cell_receipts=[];summary=[];annual=[];sparse=[];pairs=[];paired_annual=[];paired_sparse=[]
    sources={};completed=0;failures=0
    try:
        guard(stage='ar1_start')
        sources=load_sources(inputs)
        helpers=adapter._load_helpers(inputs['root'])
        references,original_receipts=audit_references(inputs,sources,np,helpers,checkpoint=guard,arrays=guard.arrays)
        guard(stage='ar1_original_audit_complete')
        # The field inventory is independent of success/failure, including nulls.
        score_fields=tuple(helpers.summarize_scores(helpers.score_predictions(
            np.array([0.]),np.array([0.]),np.array([0.]),np.array([0],dtype=np.int64))))
        pair_fields=tuple(describe_pair(helpers.score_predictions(np.array([0.]),np.array([0.]),
            np.array([0.]),np.array([0],dtype=np.int64)),helpers.score_predictions(np.array([0.]),
            np.array([0.]),np.array([0.]),np.array([0],dtype=np.int64)),
            np.array(['2000-01-01'],dtype='datetime64[D]'),horizon=6)['all'])
        for cell in execution['spec']['cells']:
            s,h,w=(cell[k] for k in ('source','horizon','window'));cfg=inputs['spec']['sources'][s];source=sources[s]
            cell_id=f'{s}-h{h}-w{w}';guard(stage='ar1_cell_start',cell_id=cell_id)
            report,trace,fits,failure=run_cell(source,cfg,h,w,checkpoint=guard,arrays=guard.arrays)
            status='COMPLETE' if failure is None else 'FAILED'
            completed+=status=='COMPLETE';failures+=status=='FAILED'
            base=dict(source=s,native_unit=cfg['native_unit'],horizon=h,window=w,method=METHOD,
                refit_step=cfg['refit_step'],status=status,stop_code=None if failure is None else failure['code'])
            origins=np.arange(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,dtype=np.int64)
            dates=source.dates[origins];years=dates.astype('datetime64[Y]')
            meta=base|dict(expected_origin_count=len(origins),completed_origin_count=len(trace['origins']))
            summary.append(meta|{k:None for k in score_fields}|(report or {})|_phi_summary(fits))
            if failure is None:
                scores,year_rows,grid_row=describe_scores(trace,dates,h)
                annual.extend(base|row for row in year_rows);sparse.append(base|grid_row)
            else:
                scores=None
                annual.extend(base|dict(calendar_year=str(y))|{k:None for k in score_fields} for y in np.unique(years))
                sparse.append(base|dict(stride_records=h+1)|{k:None for k in score_fields})
            for comparator in COMPARATORS:
                chosen=inputs['selected'][(s,h,w,'QR')]['parameter'] if comparator=='QR' else None
                pmeta={k:v for k,v in base.items() if k!='method'}|dict(left_method=METHOD,right_method=comparator,
                    right_parameter=chosen,contrast_role='DIRECT_S' if comparator=='frozen_S' else 'CONTEXT')
                if scores is not None:
                    result=describe_pair(scores,references[s,h,w,comparator],dates,horizon=h)
                    pairs.append(pmeta|result['all']);paired_annual.extend(pmeta|row for row in result['years'])
                    paired_sparse.append(pmeta|result['nonoverlap'])
                else:
                    blank={k:None for k in pair_fields};blank['relative_difference_undefined_reason']='AR1_CELL_FAILED'
                    pairs.append(pmeta|blank)
                    paired_annual.extend(pmeta|dict(calendar_year=str(y))|blank for y in np.unique(years))
                    paired_sparse.append(pmeta|dict(stride_records=h+1)|blank)
            # Per-refit coefficients and per-origin forecasts stay private.
            fit_raw=rep.json_bytes(dict(version=1,cell=cell,status=status,fit_records=fits,failure=failure))
            fit_entry=_write_bytes(private/(cell_id+'-fits.json'),fit_raw);private_exports.append(fit_entry)
            trace_path=private/(cell_id+'-traces.npz')
            with trace_path.open('xb') as stream:np.savez_compressed(stream,**trace)
            trace_raw=rep.read_bytes(inputs['root'],trace_path,within=destination,cap=64*1024*1024)
            trace_entry=dict(path=trace_path.name,**diag.file_identity(trace_raw));private_exports.append(trace_entry)
            cell_receipt=dict(version=1,cell=cell,method=METHOD,status=status,
                stop_code=None if failure is None else failure['code'],expected_origin_count=len(origins),
                completed_origin_count=len(trace['origins']),fit_count=len(fits),source_identity={k:cfg[k]
                    for k in ('sha256','bytes','record_count','native_unit')},
                new_selection_sha256=inputs['selection_hash'],ar1_spec_sha256=execution['spec_sha256'],
                ar1_freeze_sha256=execution['freeze_sha256'],private_artifacts=[fit_entry,trace_entry])
            cell_raw=rep.json_bytes(cell_receipt);entry=_write_bytes(public/(cell_id+'-receipt.json'),cell_raw)
            exports.append(entry);cell_receipts.append(dict(cell=cell,status=status,receipt=entry))
            guard.arrays(sources,references,trace,scores)
            guard(stage='ar1_cell_retained',cell_id=cell_id,completed_origins=len(trace['origins']))
        expected_annual=sum(len(np.unique(sources[c['source']].dates[
            inputs['spec']['sources'][c['source']]['evaluation_origin_first']:
            inputs['spec']['sources'][c['source']]['evaluation_origin_last']+1].astype('datetime64[Y]')))
            for c in execution['spec']['cells'])
        require((len(summary),len(pairs),len(sparse),len(paired_sparse),len(annual),len(paired_annual))==
            (8,24,8,24,expected_annual,expected_annual*3),'AR1_EXPORT_INVENTORY')
        for name,rows in (('ar1-summary.csv',summary),('ar1-annual.csv',annual),('ar1-nonoverlap.csv',sparse),
            ('ar1-paired.csv',pairs),('ar1-paired-annual.csv',paired_annual),('ar1-paired-nonoverlap.csv',paired_sparse)):
            exports.append(_write_bytes(public/name,adapter.csv_bytes(rows)))
        guard(stage='ar1_exports_retained')
        verify_inputs(inputs)
        diag.verify_exports(inputs['root'],destination,exports)
        verify_private_exports(inputs['root'],destination,private_exports)
        guard(stage='ar1_final_readback')
        verify_inputs(inputs)
        diag.verify_exports(inputs['root'],destination,exports)
        verify_private_exports(inputs['root'],destination,private_exports)
        guard(stage='ar1_verified_before_manifest')
        require(time.monotonic()-started<540.,'RESOURCE_WALL')
        manifest=dict(version=1,status='AR1_REPLAY_COMPLETE' if failures==0 else 'AR1_REPLAY_WITH_FAILURES',
            analysis_status='POST_RESULT_EXPLORATORY',created_utc=rep.utc_now(),method=METHOD,
            original_primaries_changed=False,original_models_refitted=False,new_parameter_selection=False,
            all_cells_complete=failures==0,complete_cells=int(completed),failed_cells=int(failures),
            summary_rows=8,paired_rows=24,annual_rows=len(annual),paired_annual_rows=len(paired_annual),
            nonoverlap_rows=8,paired_nonoverlap_rows=24,audited_original_cells=32,source_snapshots_read=len(sources),
            replication_dir=str(inputs['attempt'].relative_to(inputs['root'])),attempt_id=attempt_id,
            ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
            original_executable_freeze_sha256=inputs['archive']['executable_freeze_sha256'],
            archived_selection_sha256=inputs['archive']['selection_freeze_sha256'],
            new_selection_sha256=inputs['selection_hash'],cell_receipts=cell_receipts,
            original_receipts=original_receipts,
            input_file_identities={k:v['identity'] for k,v in sorted(inputs['snapshots'].items())},
            exports=exports,private_exports=private_exports,resources=dict(guard.resources),
            runtime=dict(platform_system=platform.system(),machine=platform.machine(),
                python_version=platform.python_version(),numpy_version=np.__version__),
            resource_counter_scope='Only this AR attempt; manifest written after final measured checkpoint')
        rep.write_json(public/'ar1-replay-manifest.json',manifest,exclusive=True)
        return manifest
    except Exception as error:
        code=safe_code(error)
        failure=dict(version=1,status='STOPPED',stop_code=code,created_utc=rep.utc_now(),
            verified_execution=False,complete_cells=int(completed),failed_cells=int(failures),
            retained_cell_receipts=cell_receipts,resources=dict(guard.resources),
            shortened_failed_cell_scores_written=False,original_outputs_changed=False,
            unretained_cells=[cell for cell in execution['spec']['cells']
                if cell not in [entry['cell'] for entry in cell_receipts]])
        rep.write_json(public/'ar1-failure.json',failure,exclusive=True)
        raise rep.ReproductionError(code) from None


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replication-dir',required=True,help='Successful explicit replication-SAFEID directory')
    parser.add_argument('--attempt-id',required=True,help='Fresh AR replay output ID; existing outputs are refused')
    args=parser.parse_args(argv)
    started=time.monotonic()
    try:
        require(platform.system()=='Darwin','DARWIN_REQUIRED')
        signal.signal(signal.SIGALRM,signal.SIG_DFL)
        signal.setitimer(signal.ITIMER_REAL,600.)
        result=execute(ROOT,args.replication_dir,args.attempt_id,started=started)
        print(rep.json_bytes({k:result[k] for k in ('status','complete_cells','failed_cells','summary_rows',
            'paired_rows','resources')}).decode(),end='')
        return 0 if result['all_cells_complete'] else 1
    except rep.ReproductionError as error:
        print(rep.json_bytes(dict(status='STOPPED',stop_code=error.code,verified_execution=False)).decode(),end='')
        return 1
    finally:
        if platform.system()=='Darwin':signal.setitimer(signal.ITIMER_REAL,0.)


if __name__=='__main__':raise SystemExit(main())
