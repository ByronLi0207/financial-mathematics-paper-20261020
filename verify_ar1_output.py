"""Independent scalar/Fraction readback of a complete frozen AR replay.

No fitting menu, new forecast selection, fetch, repair or output overwrite.
Only aggregate numerical evidence is exported; source/fit/forecast arrays stay
in the explicit existing private attempt. See ar1-output-check-plan.md.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import io
import math
import os
from pathlib import Path
import signal
import time
import zipfile

import run_ar1_replay as runner
import reproduce_conditional as rep
import reproduce_conditional_diagnostics as diag
import reconcile_conditional_replication as adapter

TABLE_NAMES=('ar1-summary.csv','ar1-annual.csv','ar1-nonoverlap.csv',
    'ar1-paired.csv','ar1-paired-annual.csv','ar1-paired-nonoverlap.csv')


def cell_stem(cell):
    return f'{cell["source"]}-h{cell["horizon"]}-w{cell["window"]}'


def require(value, code):
    if not value:
        raise rep.ReproductionError(code)


def near(got, wanted, *, absolute=1e-6):
    require(math.isfinite(float(got)) and math.isfinite(float(wanted))
        and math.isclose(float(got), float(wanted), rel_tol=2e-12, abs_tol=absolute),
        'AR1_INDEPENDENT_NUMERIC_MISMATCH')


def verify_export_inventory(public, private, cells):
    """Manifest hashes must bind every file actually consumed, exactly once."""
    expected_public=set(TABLE_NAMES)|{cell_stem(c)+'-receipt.json' for c in cells}
    expected_private={cell_stem(c)+suffix for c in cells for suffix in ('-fits.json','-traces.npz')}
    for entries,wanted in ((public,expected_public),(private,expected_private)):
        require(type(entries) is list and len(entries)==len(wanted),'AR1_INDEPENDENT_EXPORT_INVENTORY')
        names=[]
        for e in entries:
            require(type(e) is dict and set(e)=={'path','bytes','sha256'}
                and type(e['path']) is str and e['path'] in wanted
                and type(e['bytes']) is int and 0<e['bytes']<=64*1024*1024
                and type(e['sha256']) is str and runner.re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,
                'AR1_INDEPENDENT_EXPORT_INVENTORY')
            names.append(e['path'])
        require(len(set(names))==len(names) and set(names)==wanted,'AR1_INDEPENDENT_EXPORT_INVENTORY')


def verified_bytes(root,destination,entry,*,area):
    require(area in ('public','private'),'AR1_INDEPENDENT_EXPORT_AREA')
    raw=rep.read_bytes(root,Path(destination)/area/entry['path'],within=destination,cap=64*1024*1024)
    require(entry==dict(path=entry['path'],**diag.file_identity(raw)),'AR1_INDEPENDENT_EXPORT_IDENTITY')
    return raw


def load_verified_csv(root,destination,entry):
    # Parse the same bytes whose size/hash were checked, never re-open a path.
    return diag._rows(verified_bytes(root,destination,entry,area='public'))


def verify_table_inventory(tables,cells,configs,selected,years_by_source):
    """Exact semantic key sets, independent of numerical score coincidence."""
    require(set(tables)==set(TABLE_NAMES),'AR1_INDEPENDENT_TABLE_INVENTORY')
    for name in TABLE_NAMES:
        expected={};paired='paired' in name;annual='annual' in name;sparse='nonoverlap' in name
        for cell in cells:
            s,h,w=(cell[k] for k in ('source','horizon','window'));cfg=configs[s]
            n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
            base=dict(source=s,native_unit=cfg['native_unit'],horizon=str(h),window=str(w),
                refit_step=str(cfg['refit_step']),status='COMPLETE',stop_code='')
            for method in (runner.COMPARATORS if paired else (None,)):
                for year in (years_by_source[s] if annual else (None,)):
                    key=(s,str(h),str(w),method,year);meta=base.copy()
                    if paired:
                        parameter=selected[s,h,w,'QR']['parameter'] if method=='QR' else None
                        meta.update(left_method=runner.METHOD,right_method=method,
                            right_parameter='' if parameter is None else str(parameter),
                            contrast_role='DIRECT_S' if method=='frozen_S' else 'CONTEXT')
                    else:meta['method']=runner.METHOD
                    if annual:meta['calendar_year']=str(year)
                    if sparse:meta['stride_records']=str(h+1)
                    if name=='ar1-summary.csv':meta.update(expected_origin_count=str(n),completed_origin_count=str(n))
                    require(key not in expected,'AR1_INDEPENDENT_EXPECTED_DUPLICATE')
                    expected[key]=meta
        rows=tables[name]
        require(type(rows) is list and len(rows)==len(expected),'AR1_INDEPENDENT_TABLE_INVENTORY')
        seen=set()
        for row in rows:
            key=(row.get('source'),row.get('horizon'),row.get('window'),
                row.get('right_method') if paired else None,row.get('calendar_year') if annual else None)
            require(key in expected and key not in seen,'AR1_INDEPENDENT_TABLE_INVENTORY')
            require(all(row.get(k)==v for k,v in expected[key].items()),'AR1_INDEPENDENT_TABLE_LABELS')
            seen.add(key)
        require(seen==set(expected),'AR1_INDEPENDENT_TABLE_INVENTORY')


def verify_fit_inventory(data,cell,cfg,expected_refits):
    """Check every retained refit label/acceptance scalar; do not refit it."""
    require(type(data.get('version')) is int and data['version']==1 and data.get('cell')==cell
        and data.get('status')=='COMPLETE' and data.get('failure') is None
        and type(data.get('fit_records')) is list,'AR1_INDEPENDENT_FIT_METADATA')
    rows=data['fit_records'];h,w=cell['horizon'],cell['window']
    schedule=sorted(set(expected_refits))
    require([r.get('refit_index') for r in rows]==schedule,'AR1_INDEPENDENT_FIT_INVENTORY')
    for f in rows:
        r=f['refit_index']
        integer_fields=('refit_index','first_origin','last_origin','horizon','window','rank','transition_count')
        require(all(type(f.get(k)) is int for k in integer_fields)
            and (f['first_origin'],f['last_origin'],f['horizon'],f['window'],f['rank'],f['transition_count'])==
                (r-h-w+1,r-h,h,w,(19*(w+1)+19)//20,w+h-1)
            and cfg['evaluation_origin_first']<=r<=cfg['evaluation_origin_last'],
            'AR1_INDEPENDENT_FIT_HISTORY')
        numerical=('phi','c','scale','scaled_mean_residual','scaled_regressor_residual',
            'normal_tolerance','scaled_x_mean','scaled_y_mean','scaled_x_variance')
        require(all(type(f.get(k)) in (int,float) and math.isfinite(f[k]) for k in numerical)
            and f['scale']>0 and f['scaled_x_variance']>0 and f['normal_tolerance']>0
            and 0<=f['scaled_mean_residual']<=f['normal_tolerance']
            and 0<=f['scaled_regressor_residual']<=f['normal_tolerance'],
            'AR1_INDEPENDENT_FIT_ACCEPTANCE')
    return {f['refit_index']:f for f in rows}


def verify_manifest_context(manifest,execution,inputs,attempt_id,years_by_source):
    cells=execution['spec']['cells'];annual=sum(len(years_by_source[c['source']]) for c in cells)
    expected=dict(version=1,status='AR1_REPLAY_COMPLETE',analysis_status='POST_RESULT_EXPLORATORY',
        method=runner.METHOD,original_primaries_changed=False,original_models_refitted=False,
        new_parameter_selection=False,all_cells_complete=True,complete_cells=len(cells),failed_cells=0,
        summary_rows=len(cells),paired_rows=3*len(cells),annual_rows=annual,paired_annual_rows=3*annual,
        nonoverlap_rows=len(cells),paired_nonoverlap_rows=3*len(cells),audited_original_cells=32,
        source_snapshots_read=len(inputs['spec']['sources']),
        replication_dir=str(inputs['attempt'].relative_to(inputs['root'])),attempt_id=attempt_id,
        ar1_spec_sha256=execution['spec_sha256'],ar1_freeze_sha256=execution['freeze_sha256'],
        original_executable_freeze_sha256=inputs['archive']['executable_freeze_sha256'],
        archived_selection_sha256=inputs['archive']['selection_freeze_sha256'],new_selection_sha256=inputs['selection_hash'])
    require(all(type(manifest.get(k)) is type(v) and manifest.get(k)==v for k,v in expected.items()),
        'AR1_INDEPENDENT_MANIFEST_CONTEXT')


def verify_cell_receipt(receipt,cell,inputs,execution,artifacts,fit_count):
    cfg=inputs['spec']['sources'][cell['source']]
    n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
    expected=dict(version=1,cell=cell,method=runner.METHOD,status='COMPLETE',stop_code=None,
        expected_origin_count=n,completed_origin_count=n,fit_count=fit_count,
        source_identity={k:cfg[k] for k in ('sha256','bytes','record_count','native_unit')},
        new_selection_sha256=inputs['selection_hash'],ar1_spec_sha256=execution['spec_sha256'],
        ar1_freeze_sha256=execution['freeze_sha256'],private_artifacts=artifacts)
    require(receipt==expected and all(type(receipt.get(k)) is int for k in
        ('version','expected_origin_count','completed_origin_count','fit_count')),
        'AR1_INDEPENDENT_CELL_RECEIPT')


def check_fit_summary(row,fits):
    values=[f['phi'] for f in fits]
    require(bool(values),'AR1_INDEPENDENT_FIT_SUMMARY')
    expected=dict(completed_refit_count=len(values),phi_below_zero=sum(v<0 for v in values),
        phi_exactly_one=sum(v==1 for v in values),phi_above_one=sum(v>1 for v in values))
    require(all(row.get(k)==str(v) for k,v in expected.items()),'AR1_INDEPENDENT_FIT_SUMMARY')
    near(row['phi_min'],min(values),absolute=2e-13);near(row['phi_max'],max(values),absolute=2e-13)
    try:mean=math.fsum(v/len(values) for v in values)
    except OverflowError:mean=None
    if mean is None:require(row['phi_mean']=='','AR1_INDEPENDENT_FIT_SUMMARY')
    else:near(row['phi_mean'],mean,absolute=2e-13)


def exact_ols(levels):
    """Raw rational moments, unlike the production scaled/centered moments."""
    values = [Fraction.from_float(float(z)) for z in levels]
    x, y = values[:-1], values[1:]
    n = len(x)
    denominator = n*sum(z*z for z in x)-sum(x)**2
    require(denominator > 0, 'AR1_EXACT_OLS_CONSTANT')
    phi = (n*sum(a*b for a,b in zip(x,y))-sum(x)*sum(y))/denominator
    return float(phi), float((sum(y)-phi*sum(x))/n)


def scalar_scores(peak, capacity, floor):
    over = [max(p-c, 0.) for p,c in zip(peak,capacity)]
    unused = [max(c-p, 0.) for p,c in zip(peak,capacity)]
    return dict(loss=[.95*a+.05*b for a,b in zip(over,unused)], over=over,
        unused=unused, capacity=capacity, extra=[c-b for c,b in zip(capacity,floor)],
        breach=[p>c for p,c in zip(peak,capacity)])


def average(values, indices):
    return math.fsum(values[j] for j in indices)/len(indices)


def check_summary(row, scores, indices):
    require(int(row['origin_count']) == len(indices), 'AR1_INDEPENDENT_COUNT')
    for field,key in (('mean_pinball','loss'),('mean_capacity','capacity'),
            ('mean_extra_allowance','extra'),('mean_positive_overrun','over'),
            ('mean_unused_allowance','unused')):
        near(row[field], average(scores[key],indices))
    count = sum(scores['breach'][j] for j in indices)
    require(int(row['strict_breach_count']) == count
        and int(row['conditional_overrun_denominator']) == count, 'AR1_INDEPENDENT_BREACH')
    near(row['strict_breach_rate'],count/len(indices))
    if count:
        near(row['conditional_mean_overrun'],math.fsum(scores['over'][j] for j in indices)/count)
        require(row['conditional_overrun_undefined_reason']=='','AR1_INDEPENDENT_EMPTY_EVENT')
    else:
        require(row['conditional_mean_overrun'] == ''
            and row['conditional_overrun_undefined_reason'] == 'NO_STRICT_BREACHES',
            'AR1_INDEPENDENT_EMPTY_EVENT')


def check_pair(row, left, right, indices, origins):
    require(int(row['origin_count']) == len(indices)
        and int(row['first_source_index']) == origins[indices[0]]
        and int(row['last_source_index']) == origins[indices[-1]], 'AR1_INDEPENDENT_PAIR_COUNT')
    a,b = average(left['loss'],indices),average(right['loss'],indices)
    difference = math.fsum(left['loss'][j]-right['loss'][j] for j in indices)/len(indices)
    for field,want in (('mean_pinball_left',a),('mean_pinball_right',b),
            ('mean_pinball_difference',difference)):
        near(row[field],want)
    relative=100*(difference/b) if b>0 else None
    reason='' if relative is not None and math.isfinite(relative) else (
        'ZERO_REFERENCE_MEAN_LOSS' if b<=0 else 'RELATIVE_DIFFERENCE_NOT_FINITE')
    require(row['relative_difference_undefined_reason']==reason,'AR1_INDEPENDENT_RELATIVE_REASON')
    if reason:
        require(row['relative_mean_loss_difference_percent']=='','AR1_INDEPENDENT_ZERO_REFERENCE')
    else:near(row['relative_mean_loss_difference_percent'],relative)
    for field,key in (('mean_capacity_difference','capacity'),
            ('mean_positive_overrun_difference','over'),('mean_unused_allowance_difference','unused')):
        near(row[field],math.fsum(left[key][j]-right[key][j] for j in indices)/len(indices))
    require(int(row['strict_breach_count_left']) == sum(left['breach'][j] for j in indices)
        and int(row['strict_breach_count_right']) == sum(right['breach'][j] for j in indices),
        'AR1_INDEPENDENT_PAIRED_BREACH')


def scalar_replay(position, fit, horizon, window, query):
    """Extract each residual and recurse; never use the production identity."""
    phi,c = fit['phi'],fit['c']
    first = fit['first_origin'];peaks=[];floor=abs(query)
    for i in range(first,first+window):
        value=query;peak=floor
        for j in range(i,i+horizon):
            residual=float(position[j+1])-c-phi*float(position[j])
            value=c+phi*value+residual
            peak=max(peak,abs(value))
        peaks.append(peak-floor)
    rank=(19*(window+1)+19)//20
    return floor+sorted(peaks)[rank-1]


def check_output_headers(raw, np, count):
    """The new trace has bare names; the old audit expects method prefixes."""
    wanted={'origins','capacity','refit_indices','peak','floor','pinball'}
    with zipfile.ZipFile(io.BytesIO(raw)) as zipped:
        entries=zipped.infolist()
        require(len(entries)==6 and {e.filename for e in entries}=={n+'.npy' for n in wanted}
            and all(not e.flag_bits & 1 and e.file_size<=64*1024*1024 for e in entries)
            and sum(e.file_size for e in entries)<=128*1024*1024,'AR1_OUTPUT_HEADER')
        for entry in entries:
            name=entry.filename[:-4]
            with zipped.open(entry) as stream:
                version=np.lib.format.read_magic(stream)
                require(version in ((1,0),(2,0)),'AR1_OUTPUT_HEADER')
                reader=np.lib.format.read_array_header_1_0 if version==(1,0) else np.lib.format.read_array_header_2_0
                shape,fortran,dtype=reader(stream,max_header_size=10000)
                wanted_dtype=np.dtype('int64' if name in ('origins','refit_indices') else 'float64')
                require(shape==(count,) and dtype==wanted_dtype and not dtype.hasobject
                    and type(fortran) is bool and not fortran
                    and entry.file_size==stream.tell()+count*8,'AR1_OUTPUT_HEADER')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replication-dir',required=True)
    parser.add_argument('--attempt-id',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args(argv);started=time.monotonic()
    signal.signal(signal.SIGALRM,signal.SIG_DFL);signal.setitimer(signal.ITIMER_REAL,600.)
    root=Path(__file__).resolve().parent
    for name in rep.THREAD_NAMES:os.environ[name]='1'
    inputs=runner.prepare_replica(root,args.replication_dir)
    execution=runner.verify_execution(inputs)
    require(type(args.attempt_id) is str and runner.re.fullmatch(
        r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',args.attempt_id) is not None,'AR1_ATTEMPT_ID')
    destination=inputs['attempt']/('ar1-replay-'+args.attempt_id)
    manifest_raw=rep.read_bytes(root,destination/'public/ar1-replay-manifest.json',within=destination)
    manifest=rep.strict_json(manifest_raw)
    require(manifest['status']=='AR1_REPLAY_COMPLETE' and manifest['complete_cells']==8
        and manifest['failed_cells']==0 and manifest['ar1_spec_sha256']==execution['spec_sha256']
        and manifest['ar1_freeze_sha256']==execution['freeze_sha256'],'AR1_COMPLETE_ATTEMPT_REQUIRED')
    cells=execution['spec']['cells']
    verify_export_inventory(manifest['exports'],manifest['private_exports'],cells)
    public_entries={e['path']:e for e in manifest['exports']}
    private_entries={e['path']:e for e in manifest['private_exports']}
    adapter.verify_resource(manifest['resources'])
    import numpy as np
    from run_study import RunGuard
    # Reuse existing owned directories only for read-only resource measurement.
    guard=RunGuard(started,rep.utc_now(),destination,destination/'public',destination/'private')
    guard(stage='independent_ar1_readback_start')
    sources=runner.load_sources(inputs)
    refs,reference_receipts=runner.audit_references(inputs,sources,np,adapter._load_helpers(root),
        checkpoint=guard,arrays=guard.arrays)
    years_by_source={s:sorted({str(source.dates[t])[:4] for t in
        range(inputs['spec']['sources'][s]['evaluation_origin_first'],
              inputs['spec']['sources'][s]['evaluation_origin_last']+1)}) for s,source in sources.items()}
    verify_manifest_context(manifest,execution,inputs,args.attempt_id,years_by_source)
    require(manifest['original_receipts']==reference_receipts
        and manifest['input_file_identities']=={k:v['identity'] for k,v in sorted(inputs['snapshots'].items())},
        'AR1_INDEPENDENT_INPUT_CHAIN')
    tables={name:load_verified_csv(root,destination,public_entries[name]) for name in TABLE_NAMES}
    verify_table_inventory(tables,cells,inputs['spec']['sources'],inputs['selected'],years_by_source)
    expected_receipts=[dict(cell=c,status='COMPLETE',receipt=public_entries[cell_stem(c)+'-receipt.json']) for c in cells]
    require(manifest['cell_receipts']==expected_receipts,'AR1_INDEPENDENT_CELL_INVENTORY')
    checks=0;exact_fits=0;recursive_reports=0
    maximum_slope_error=0.;maximum_replay_relative_error=0.
    all_fit_count=0
    for cell in cells:
        s,h,w=cell['source'],cell['horizon'],cell['window'];cfg=inputs['spec']['sources'][s]
        source=sources[s];stem=f'{s}-h{h}-w{w}';n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
        raw=verified_bytes(root,destination,private_entries[stem+'-traces.npz'],area='private')
        check_output_headers(raw,np,n)
        with np.load(io.BytesIO(raw),allow_pickle=False) as trace:
            origins=list(map(int,trace['origins']));capacities=list(map(float,trace['capacity']))
            require(origins==list(range(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1)),
                'AR1_INDEPENDENT_ORIGINS')
            peaks=[max(abs(float(z)) for z in source.position[t:t+h+1]) for t in origins]
            floors=[abs(float(source.position[t])) for t in origins]
            require(np.array_equal(trace['peak'],peaks) and np.array_equal(trace['floor'],floors)
                and all(c>=b for c,b in zip(capacities,floors)), 'AR1_INDEPENDENT_TARGET')
            expected_refit=[origins[0]+(t-origins[0])//cfg['refit_step']*cfg['refit_step'] for t in origins]
            require(list(map(int,trace['refit_indices']))==expected_refit,'AR1_INDEPENDENT_REFITS')
            score=scalar_scores(peaks,capacities,floors)
            for got,want in zip(trace['pinball'],score['loss']):near(got,want)
        fit_data=rep.strict_json(verified_bytes(root,destination,private_entries[stem+'-fits.json'],area='private'))
        fits=verify_fit_inventory(fit_data,cell,cfg,expected_refit)
        all_fit_count+=len(fits)
        cell_receipt=rep.strict_json(verified_bytes(root,destination,public_entries[stem+'-receipt.json'],area='public'))
        verify_cell_receipt(cell_receipt,cell,inputs,execution,
            [private_entries[stem+'-fits.json'],private_entries[stem+'-traces.npz']],len(fits))
        checked_refits=set()
        for j in (0,n//2,n-1):
            t,r=origins[j],expected_refit[j];fit=fits[r]
            if r not in checked_refits:
                phi,c=exact_ols(source.position[r-h-w+1:r+1])
                near(fit['phi'],phi,absolute=2e-13);near(fit['c'],c)
                maximum_slope_error=max(maximum_slope_error,abs(fit['phi']-phi))
                checked_refits.add(r);exact_fits+=1
            report=scalar_replay(source.position,fit,h,w,float(source.position[t]))
            near(capacities[j],report)
            maximum_replay_relative_error=max(maximum_replay_relative_error,
                abs(capacities[j]-report)/max(1.,abs(report)))
            recursive_reports+=1
        years=[str(source.dates[t])[:4] for t in origins]
        groups={'all':list(range(n)),'sparse':[j for j in range(n) if j%(h+1)==0]}
        groups.update({y:[j for j in range(n) if years[j]==y] for y in sorted(set(years))})
        matches=lambda row: (row['source'],int(row['horizon']),int(row['window']))==(s,h,w)
        for name,rows in tables.items():
            for row in filter(matches,rows):
                key=row['calendar_year'] if 'annual' in name else ('sparse' if 'nonoverlap' in name else 'all')
                if 'paired' in name:
                    reference=refs[s,h,w,row['right_method']]
                    require(list(map(int,reference.origins))==origins,'AR1_INDEPENDENT_REFERENCE_ORIGINS')
                    right=scalar_scores(peaks,list(map(float,reference.capacities)),floors)
                    check_pair(row,score,right,groups[key],origins)
                else:
                    check_summary(row,score,groups[key])
                    if name=='ar1-summary.csv':check_fit_summary(row,fit_data['fit_records'])
                checks+=1
        guard(stage='independent_ar1_cell_checked',cell_id=stem)
    require(checks==sum(len(rows) for rows in tables.values()) and exact_fits==24
        and recursive_reports==24,'AR1_INDEPENDENT_CHECK_INVENTORY')
    runner.verify_inputs(inputs);diag.verify_exports(root,destination,manifest['exports'])
    runner.verify_private_exports(root,destination,manifest['private_exports'])
    require(rep.read_bytes(root,destination/'public/ar1-replay-manifest.json',within=destination)==manifest_raw,
        'AR1_INDEPENDENT_MANIFEST_CHANGED')
    guard(stage='independent_ar1_readback_complete')
    receipt=dict(version=2,status='AR1_INDEPENDENT_READBACK_PASS',verified_utc=rep.utc_now(),
        ar1_manifest_sha256=rep.sha(manifest_raw),ar1_spec_sha256=execution['spec_sha256'],
        ar1_freeze_sha256=execution['freeze_sha256'],cells=8,aggregate_rows_independently_checked=checks,
        exact_fraction_fits=exact_fits,scalar_recursive_reports=recursive_reports,
        fit_records_metadata_checked=all_fit_count,exact_unique_csv_keys_checked=True,
        all_consumed_exports_bound_to_manifest=True,
        independent_refit_oracle_scope='first, integer midpoint and last issue per cell; 24 distinct refits',
        independent_replay_scope='first, integer midpoint and last issue per cell; 24 issued reports',
        maximum_slope_absolute_error=maximum_slope_error,
        maximum_replay_relative_error=maximum_replay_relative_error,
        new_model_selection=False,original_models_refitted=False,source_values_public=False,
        check_plan='notes/revision-20261022/ar1-output-check-plan.md',
        code_sha256=rep.sha(Path(__file__).read_bytes()),resources=dict(guard.resources))
    candidate=root/args.output
    require(not any(p.is_symlink() for p in (candidate,*candidate.parents)),
        'AR1_INDEPENDENT_OUTPUT_PATH')
    output=candidate.resolve()
    require(output.is_relative_to(root/'state/revision-20261022') and not output.exists(),
        'AR1_INDEPENDENT_OUTPUT_PATH')
    rep.write_json(output,receipt,exclusive=True)
    print(rep.json_bytes(receipt).decode(),end='')
    signal.setitimer(signal.ITIMER_REAL,0.)


if __name__=='__main__':
    main()
