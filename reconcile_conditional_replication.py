"""Audit a new fixed-contract attempt and compare all aggregate cells.

This adapter fits no models. It reads private sources/traces only when called
by explicit replication, after immutable-archive and source-hash preflight.
All exports stay inside that new attempt. Importing this module is stdlib-only.
"""
from __future__ import annotations

import csv
import io
import math
import os
from pathlib import Path
import platform
import re
import time
import types
import zipfile

import reproduce_conditional as rep


def compare_csv(new_raw,archived_raw):
    """Report every changed scalar, including arbitrarily small float changes."""
    def parse(raw):
        reader=csv.reader(io.StringIO(raw.decode('utf-8'),newline=''))
        rows=list(reader)
        if not rows or len(set(rows[0]))!=len(rows[0]) or any(len(r)!=len(rows[0]) for r in rows[1:]):
            raise rep.ReproductionError('CSV_STRUCTURE')
        return rows[0],rows[1:]
    head,new=parse(new_raw);oldhead,old=parse(archived_raw)
    result=dict(byte_identical=new_raw==archived_raw,header_equal=head==oldhead,
        row_count_equal=len(new)==len(old),new_rows=len(new),archived_rows=len(old),differences=[])
    if result['header_equal'] and result['row_count_equal']:
        for number,(a,b) in enumerate(zip(new,old),start=1):
            for column,current,previous in zip(head,a,b):
                if current==previous:continue
                entry=dict(row=number,column=column,new=current,archived=previous,
                    absolute_numeric_difference=None,relative_numeric_difference=None)
                try:
                    x=float(current);y=float(previous)
                    if math.isfinite(x) and math.isfinite(y):
                        difference=abs(x-y)
                        entry['absolute_numeric_difference']=difference if math.isfinite(difference) else None
                        if y!=0:
                            relative=difference/abs(y)
                            entry['relative_numeric_difference']=relative if math.isfinite(relative) else None
                except (ValueError,OverflowError):pass
                result['differences'].append(entry)
    result['exact_scalar_agreement']=(result['header_equal'] and result['row_count_equal'] and not result['differences'])
    return result


def csv_bytes(rows):
    if not rows:raise rep.ReproductionError('EMPTY_PUBLIC_TABLE')
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return stream.getvalue().encode()


def verify_resource(resource):
    """Own strict resource contract; do not delegate to the older v01 checker."""
    try:
        elapsed=resource['elapsed_seconds']
        integers=('peak_rss_bytes','maximum_observed_os_threads','thread_snapshot_count')
        if (type(elapsed) not in (int,float) or not math.isfinite(elapsed) or not 0<elapsed<540
                or any(type(resource[k]) is not int or resource[k]<1 for k in integers)
                or resource['peak_rss_bytes']>=1610612736
                or resource['maximum_observed_os_threads']>2 or resource['thread_probe_status']!='PASS'):
            raise rep.ReproductionError('AUDIT_RESOURCES')
    except (KeyError,TypeError):raise rep.ReproductionError('AUDIT_RESOURCES') from None


def verify_phase_labels(receipt,methods,expected_parameter):
    """Check final public phase/method/parameter inventory independently of v01."""
    try:
        result=receipt['result']
        if (type(receipt['version']) is not int or receipt['version']!=1
                or (receipt['status'],receipt['stop_code'],result['status'],result['failure'],result['candidate_rows'])
                    !=('COMPLETE',None,'COMPLETE',None,[])
                or [r['method'] for r in result['summary_rows']]!=methods
                or any(r['parameter']!=expected_parameter for r in result['summary_rows'])
                or any((r['method'],r['parameter'])!=(methods[0],expected_parameter) for r in result['fit_diagnostics'])):
            raise rep.ReproductionError('AUDIT_PHASE_LABELS')
    except (KeyError,TypeError):raise rep.ReproductionError('AUDIT_PHASE_LABELS') from None


def verify_fit_records(rows,cfg,h,w,family,first,last):
    """Apply the tightened feasible-dual/residual contract, including all bounds."""
    try:
        expected=list(range(first,last+1,cfg['refit_step'])) if family else []
        if [d['refit_index'] for d in rows]!=expected:
            raise rep.ReproductionError('AUDIT_FIT_SCHEDULE')
        for d in rows:
            r=d['refit_index']
            fields=('refit_index','training_first_origin','training_last_origin','training_count','latest_label_end')
            if (any(type(d[k]) is not int for k in fields)
                    or (d['training_first_origin'],d['training_last_origin'],d['training_count'],d['latest_label_end'])
                        !=(r-h-w+1,r-h,w,r)):
                raise rep.ReproductionError('AUDIT_FIT_MATURITY')
            if family!='QR':continue
            nonnegative=('primal_objective','duality_gap','primal_residual','dual_residual',
                'primal_tolerance','dual_tolerance','gap_tolerance')
            if (any(type(d[k]) not in (int,float) or not math.isfinite(d[k]) or d[k]<0 for k in nonnegative)
                    or type(d['dual_objective']) not in (int,float) or not math.isfinite(d['dual_objective'])
                    or type(d['iterations']) is not int or not 1<=d['iterations']<=10000):
                raise rep.ReproductionError('AUDIT_QR_NUMERICAL')
            primal,dual,gap=d['primal_objective'],d['dual_objective'],d['duality_gap']
            if abs((primal-dual)-gap)>256*math.ulp(1.)*max(1.,abs(primal),abs(dual)):
                raise rep.ReproductionError('AUDIT_QR_DUAL_IDENTITY')
            numerator,denominator=float(.95).as_integer_ratio();grid=2**40
            integers=('dual_integer_lower','dual_integer_upper','dual_integer_sum','dual_grid_denominator')
            if (any(type(d[k]) is not int for k in integers)
                    or d['dual_integer_lower']!=-((denominator-numerator)*grid//denominator)
                    or d['dual_integer_upper']!=numerator*grid//denominator
                    or d['dual_integer_sum']!=0 or d['dual_grid_denominator']!=grid
                    or d['primal_residual']>d['primal_tolerance']
                    or d['dual_residual']>d['dual_tolerance'] or gap>d['gap_tolerance']):
                raise rep.ReproductionError('AUDIT_QR_ACCEPTANCE')
    except (KeyError,TypeError,OverflowError):raise rep.ReproductionError('AUDIT_FIT_RECORDS') from None


def _checked_npz(raw,metadata,wanted,np,helpers):
    """Bound ZIP inflation, forbid object/different dtype arrays, and hash snapshot."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zipped:
            items=zipped.infolist()
            if (len(items)!=len(wanted) or len({i.filename for i in items})!=len(items)
                    or {i.filename for i in items}!={n+'.npy' for n in wanted}
                    or any(i.file_size>64*1024*1024 or i.flag_bits&1 for i in items)
                    or sum(i.file_size for i in items)>128*1024*1024):
                raise rep.ReproductionError('NPZ_INVENTORY_OR_SIZE')
        if metadata!=dict(area='private',name='numeric-traces.npz',bytes=len(raw),sha256=rep.sha(raw)):
            raise rep.ReproductionError('NPZ_IDENTITY')
        traces=np.load(io.BytesIO(raw),allow_pickle=False)
        try:
            if set(traces.files)!=wanted:raise rep.ReproductionError('NPZ_ARRAY_INVENTORY')
            for name in traces.files:
                values=traces[name]
                dtype=np.dtype('int64') if name.endswith(('_origins','_refit_indices')) else np.dtype('float64')
                if values.ndim!=1 or values.dtype!=dtype or not np.isfinite(values).all():
                    raise rep.ReproductionError('NPZ_DTYPE_OR_FINITE')
            return traces
        except BaseException:
            traces.close();raise
    except rep.ReproductionError:raise
    except (ValueError,KeyError,TypeError,OSError,zipfile.BadZipFile):
        raise rep.ReproductionError('NPZ_INTEGRITY') from None


def audit_cell(root,attempt,queued,spec,selected,freeze_hash,selection_hash,source,np,helpers,checkpoint):
    """Reconcile one terminal cell against exact source and private array snapshot."""
    try:
        checkpoint()
        cell=tuple(queued[n] for n in ('phase','source','horizon','window','family'))
        phase,s,h,w,f=cell;cfg=spec['sources'][s]
        raw=rep.read_bytes(root,queued['receipt_path'],within=attempt)
        if rep.sha(raw)!=queued['receipt_sha256']:raise rep.ReproductionError('QUEUED_RECEIPT_HASH')
        receipt=rep.strict_json(raw)
        helpers.assert_same((queued['status'],queued['stop_code'],queued['exit_code']),('COMPLETE',None,0),'queued terminal')
        helpers.assert_same(tuple(receipt[n] for n in ('phase','source','horizon','window','family')),cell,'cell identity')
        helpers.assert_same(receipt['executable_freeze_sha256'],freeze_hash,'executable freeze')
        helpers.assert_same(receipt['selection_freeze_sha256'],selection_hash if f else None,'selection freeze')
        helpers.assert_same(receipt['result']['native_unit'],cfg['native_unit'],'native unit')
        for name in ('sha256','bytes','record_count','native_unit'):
            helpers.assert_same(receipt['source_identity'][name],cfg[name],'source '+name)
        verify_resource(receipt['resources'])
        origins=np.arange(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,dtype=np.int64)
        peak=helpers.independent_peak(source.position,origins,h);floor=np.abs(source.position[origins])
        helpers.assert_same(receipt['result']['origin_identity'],rep.origin_identity(int(origins[0]),int(origins[-1])),'origin fingerprint')
        parameter=selected[s,h,w,f]['parameter'] if f else None
        if f:
            helpers.assert_same(receipt['result']['selection'],dict(status='SELECTED',parameter=parameter),'selection')
        methods=([f] if f else [prefix+'_'+rule for prefix in
            (('rolling','frozen','one_state') if cfg['one_state_reference_neighbors'][str(w)] else ('rolling','frozen'))
            for rule in ('F','S','K')])
        verify_phase_labels(receipt,methods,parameter)
        years=source.dates[origins].astype('datetime64[Y]').astype(int)+1970
        helpers.assert_same(len(receipt['result']['year_rows']),len(methods)*len(np.unique(years)),'year inventory')
        helpers.assert_same(len(receipt['result']['nonoverlap_rows']),len(methods),'grid inventory')
        helpers.assert_same(len(receipt['artifacts']),1,'artifact inventory')
        receipt_path=rep.project_file(root,queued['receipt_path'],within=attempt)
        trace_path=receipt_path.parent.parent/'private/numeric-traces.npz'
        trace_raw=rep.read_bytes(root,trace_path,within=attempt,cap=64*1024*1024)
        wanted={method+'_'+name for method in methods
            for name in ('origins','peak','floor','refit_indices','capacity','pinball')}
        summary=[];annual=[];nonoverlap=[];scores_by_method={}
        with _checked_npz(trace_raw,receipt['artifacts'][0],wanted,np,helpers) as traces:
            for method,reported in zip(methods,receipt['result']['summary_rows']):
                expected_refits=(origins[0]+((origins-origins[0])//cfg['refit_step'])*cfg['refit_step']
                    if f or method.startswith('frozen_') else origins)
                scores=helpers.verify_method(traces,method,origins,peak,floor,expected_refits)
                metrics=helpers.summarize_scores(scores)
                helpers.assert_same(dict(method=method,parameter=reported['parameter'])|metrics,reported,'summary')
                method_parameter=(cfg['one_state_reference_neighbors'][str(w)] if method.startswith('one_state_')
                    else reported['parameter'])
                meta=dict(source=s,native_unit=cfg['native_unit'],horizon=h,window=w,method=method,
                    parameter=method_parameter,refit_step=cfg['refit_step'] if f or method.startswith('frozen_') else 1,
                    plain_knn_full_pool_fallback=method=='KNN' and method_parameter==w)
                summary.append(meta|metrics);scores_by_method[method]=scores
                for year in np.unique(years):
                    mask=years==year
                    part=helpers.score_predictions(peak[mask],scores.capacities[mask],floor[mask],origins[mask])
                    metrics_year=helpers.summarize_scores(part)
                    found=[r for r in receipt['result']['year_rows'] if r['method']==method and r['year']==int(year)]
                    helpers.assert_same(found,[dict(method=method,parameter=reported['parameter'],year=int(year))|metrics_year],'annual summary')
                    annual.append(meta|dict(calendar_year=int(year))|metrics_year)
                grid=helpers.nonoverlap_origins(int(origins[0]),int(origins[-1]),h);mask=np.isin(origins,grid)
                part=helpers.score_predictions(peak[mask],scores.capacities[mask],floor[mask],origins[mask])
                metrics_grid=helpers.summarize_scores(part)
                found=[r for r in receipt['result']['nonoverlap_rows'] if r['method']==method]
                helpers.assert_same(found,[dict(method=method,parameter=reported['parameter'])|metrics_grid],'grid summary')
                nonoverlap.append(meta|dict(stride_records=h+1)|metrics_grid)
        verify_fit_records(receipt['result']['fit_diagnostics'],cfg,h,w,f,int(origins[0]),int(origins[-1]))
        checkpoint()
        return dict(summary=summary,annual=annual,nonoverlap=nonoverlap,scores=scores_by_method,
            receipt=receipt,receipt_raw=raw,cell=cell)
    except rep.ReproductionError:raise
    except (ValueError,KeyError,TypeError,IndexError,OverflowError):
        raise rep.ReproductionError('NUMERICAL_AUDIT_FAILED') from None


def _load_helpers(root):
    """Use the published hash-verified audit's pure helpers, never its CLI."""
    relative=rep.RESULTS+'/audit-builder-v01.py'
    raw=rep.read_bytes(root,relative);size,digest=rep.ARCHIVED_RESULTS[relative]
    if len(raw)!=size or rep.sha(raw)!=digest:
        raise rep.ReproductionError('AUDIT_HELPER_HASH')
    path=rep.project_file(root,relative)
    # Execute the immutable verified byte snapshot, never reopen the path.
    helpers=types.ModuleType('_published_conditional_audit_helpers')
    helpers.__file__=str(path)
    exec(compile(raw,str(path),'exec'),helpers.__dict__)
    return helpers


def selection_snapshot(root,path,expected_hash,attempt):
    """Bind matrix/terminal evidence to the exact retained selection bytes."""
    raw=rep.read_bytes(root,path,within=attempt)
    if rep.sha(raw)!=expected_hash:
        raise rep.ReproductionError('SELECTION_SNAPSHOT_HASH')
    return rep.strict_json(raw)


def reconcile(root,attempt,queue_path,selection,archive,checkpoint):
    """Audit32 new receipts and export90 summaries/98 contrasts to this attempt."""
    root=Path(root).absolute();attempt=Path(attempt).absolute()
    try:
        # The caller owns a freshly created attempt, but each input is rechecked.
        if attempt.parent!=root/'.scratch/revision-20261022' or not re.fullmatch(r'replication-[A-Za-z0-9][A-Za-z0-9_-]{0,63}',attempt.name):
            raise rep.ReproductionError('ATTEMPT_BOUNDARY')
        if any(p.is_symlink() for p in (attempt,*attempt.parents)):
            raise rep.ReproductionError('ATTEMPT_BOUNDARY')
        checkpoint();rep.verify_archive(root);rep.replication_preflight(root,archive)
        for name in rep.THREAD_NAMES:
            # Before numeric imports; no install, optimizer or resource-guard bypass.
            os.environ[name]='1'
        import numpy as np
        helpers=_load_helpers(root)
        from conditional_sources import load_source
        from run_study import RunGuard
        spec=archive['spec'];freeze_hash=archive['executable_freeze_sha256']
        helpers.runner.verify_executable_freeze(freeze_hash,root=root)
        selected=helpers.runner.verify_selection_freeze(selection[0],selection[1],freeze_hash,spec,root=root)
        selected_path=rep.project_file(root,selection[0],within=attempt)
        new_selection=selection_snapshot(root,selected_path,selection[1],attempt)
        matrix=lambda cells:[(c['source'],c['horizon'],c['window'],c['family'],c['status'],c['parameter']) for c in cells]
        if matrix(new_selection['cells'])!=matrix(archive['selection']['cells']):
            raise rep.ReproductionError('SELECTION_CHANGED')
        audit_attempt=attempt/'numerical-audit';audit_attempt.mkdir()
        output=audit_attempt/'public';private=audit_attempt/'private';output.mkdir();private.mkdir()
        guard=RunGuard(time.monotonic(),rep.utc_now(),audit_attempt,output,private)
        guard(stage='replication_audit_start');checkpoint()
        sources={}
        for s,cfg in spec['sources'].items():
            sources[s]=load_source(rep.project_file(root,cfg['input_relative_path']),s,
                expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
            helpers.runner._validate_source(sources[s],cfg,s)
            guard.arrays(sources);guard(stage='source_audited');checkpoint()
        queue_raw=rep.read_bytes(root,queue_path,within=attempt);queue=rep.strict_json(queue_raw)
        expected=helpers.expected_cells(spec)
        helpers.assert_same([tuple(r[k] for k in ('phase','source','horizon','window','family')) for r in queue['cells']],expected,'queue inventory')
        all_scores={};summary=[];annual=[];nonoverlap=[];receipt_raws={};receipts=[]
        for cell,row in zip(expected,queue['cells']):
            phase,s,h,w,f=cell
            expected_path=rep.worker_directory(attempt,cell)/'public/manifest.json'
            helpers.assert_same(row['receipt_path'],str(expected_path.relative_to(root)),'receipt path')
            result=audit_cell(root,attempt,row,spec,selected,freeze_hash,selection[1],sources[s],np,helpers,checkpoint)
            summary.extend(result['summary']);annual.extend(result['annual']);nonoverlap.extend(result['nonoverlap'])
            all_scores.update({(s,h,w,method):score for method,score in result['scores'].items()})
            name=(f'evaluation-{s}-h{h}-w{w}-{f}.json' if f else f'references-{s}-h{h}-w{w}.json')
            receipt_raws[name]=result['receipt_raw']
            receipts.append(dict(public_file=name,sha256=rep.sha(result['receipt_raw']),bytes=len(result['receipt_raw'])))
            guard.arrays(all_scores);guard(stage='new_trace_audited');checkpoint()
        helpers.assert_same((len(summary),len(annual),len(nonoverlap)),(90,372,90),'summary inventories')
        comparisons=[];comparison_years=[];comparison_grid=[]
        inventory=helpers.comparison_inventory(spec);helpers.assert_same(len(inventory),98,'paired inventory')
        for s,h,lw,lm,rw,rm,category in inventory:
            left=all_scores[s,h,lw,lm];right=all_scores[s,h,rw,rm];cfg=spec['sources'][s]
            primary=cfg['primary_contrast']
            is_primary=(h,lw,lm,rw,rm)==(primary['horizon'],primary['window'],primary['family'],primary['reference_window'],primary['reference_method'])
            meta=dict(contrast_id=f'{s}-h{h}-{lm}{lw}-minus-{rm}{rw}',source=s,native_unit=cfg['native_unit'],
                horizon=h,left_window=lw,left_method=lm,right_window=rw,right_method=rm,
                contrast_category=category,declared_source_primary=is_primary,h24_legacy_contrast=category=='h24_legacy_contrast')
            paired=helpers.paired_comparison(left,right,sources[s].dates[left.origins],horizon=h)
            direct=math.fsum(float(a)-float(b) for a,b in zip(left.pinball,right.pinball))/len(left.origins)
            helpers.assert_same(paired['all']['mean_pinball_difference'],direct,'direct paired loss')
            helpers.assert_same(sum(y['origin_count'] for y in paired['years']),len(left.origins),'annual count')
            weighted=math.fsum(y['origin_count']*y['mean_pinball_difference'] for y in paired['years'])/len(left.origins)
            helpers.core._assert_mean_equal(weighted,direct,len(left.origins),max(1.,abs(direct)))
            comparisons.append(meta|paired['all']);comparison_years.extend(meta|year for year in paired['years'])
            comparison_grid.append(meta|paired['nonoverlap']);checkpoint()
        helpers.assert_same((len(comparisons),len(comparison_years),len(comparison_grid)),(98,388,98),'paired row inventories')
        helpers.assert_same(len({r['contrast_id'] for r in comparisons}),98,'unique contrasts')
        helpers.assert_same(sum(r['declared_source_primary'] for r in comparisons),2,'primary contrasts')
        for h in spec['horizons']:
            if not np.array_equal(all_scores['nyfed_weekly',h,52,'KNN'].capacities,
                    all_scores['nyfed_weekly',h,52,'frozen_F'].capacities):
                raise rep.ReproductionError('FULL_POOL_KNN_IDENTITY')
        tables={'evaluation-summary.csv':summary,'evaluation-annual.csv':annual,'evaluation-nonoverlap.csv':nonoverlap,
            'paired-comparisons.csv':comparisons,'paired-annual.csv':comparison_years,'paired-nonoverlap.csv':comparison_grid}
        agreement={};exports=[]
        for name,rows in tables.items():
            raw=csv_bytes(rows);old=rep.read_bytes(root,rep.RESULTS+'/'+name)
            expected_size,expected_hash=rep.ARCHIVED_RESULTS[rep.RESULTS+'/'+name]
            if len(old)!=expected_size or rep.sha(old)!=expected_hash:
                raise rep.ReproductionError('ARCHIVED_RESULT_CHANGED')
            agreement[name]=compare_csv(raw,old)
            with (output/name).open('xb') as stream:stream.write(raw)
            exports.append(dict(path=name,bytes=len(raw),sha256=rep.sha(raw)))
            checkpoint()
        for name,raw in receipt_raws.items():
            with (output/name).open('xb') as stream:stream.write(raw)
            exports.append(dict(path=name,bytes=len(raw),sha256=rep.sha(raw)))
        guard(stage='replication_audit_final');checkpoint()
        helpers.runner.verify_executable_freeze(freeze_hash,root=root)
        # Recheck the immutable original publication after all computations.
        rep.verify_archive(root)
        for s,cfg in spec['sources'].items():
            raw=rep.read_bytes(root,cfg['input_relative_path'],cap=25*1024*1024)
            if len(raw)!=cfg['bytes'] or rep.sha(raw)!=cfg['sha256']:
                raise rep.ReproductionError('RAW_SOURCE_CHANGED')
        blas=getattr(np.__config__,'CONFIG',{}).get('Build Dependencies',{}).get('blas',{})
        runtime=dict(python_version=platform.python_version(),numpy_version=np.__version__,
            platform_system=platform.system(),machine=platform.machine(),
            blas_name=blas.get('name') if type(blas.get('name')) is str else None,
            blas_version=blas.get('version') if type(blas.get('version')) is str else None)
        comparison=dict(version=1,status='NUMERICAL_AUDIT_VERIFIED',created_utc=rep.utc_now(),
            scope='New source/trace/scalar audit; every exported aggregate compared to the immutable archive without a tolerance',
            archived_selection_sha256=archive['selection_freeze_sha256'],new_selection_sha256=selection[1],
            selection_status_parameter_matrix_identical=True,queue_sha256=rep.sha(queue_raw),
            exact_csv_byte_agreement=all(v['byte_identical'] for v in agreement.values()),
            exact_csv_scalar_agreement=all(v['exact_scalar_agreement'] for v in agreement.values()),
            tables=agreement,exports=exports,receipts=receipts,audit_resources=dict(guard.resources),runtime=runtime,
            source_identities={s:{k:c[k] for k in ('sha256','bytes','record_count','native_unit')} for s,c in spec['sources'].items()},
            summary_rows=len(summary),annual_rows=len(annual),paired_rows=len(comparisons),paired_annual_rows=len(comparison_years))
        selection_snapshot(root,selected_path,selection[1],attempt)
        rep.write_json(output/'reproduction-comparison.json',comparison,exclusive=True)
        checkpoint()
        return dict(status=comparison['status'],comparison_path=str((output/'reproduction-comparison.json').relative_to(root)),
            exact_csv_byte_agreement=comparison['exact_csv_byte_agreement'],exact_csv_scalar_agreement=comparison['exact_csv_scalar_agreement'])
    except rep.ReproductionError:raise
    except (ValueError,KeyError,TypeError,IndexError,OverflowError,OSError):
        raise rep.ReproductionError('NUMERICAL_AUDIT_FAILED') from None
