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


def require(value, code):
    if not value:
        raise rep.ReproductionError(code)


def near(got, wanted, *, absolute=1e-6):
    require(math.isfinite(float(got)) and math.isfinite(float(wanted))
        and math.isclose(float(got), float(wanted), rel_tol=2e-12, abs_tol=absolute),
        'AR1_INDEPENDENT_NUMERIC_MISMATCH')


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
    if b > 0:
        near(row['relative_mean_loss_difference_percent'],100*difference/b)
    else:
        require(row['relative_mean_loss_difference_percent'] == '', 'AR1_INDEPENDENT_ZERO_REFERENCE')
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
    diag.verify_exports(root,destination,manifest['exports'])
    runner.verify_private_exports(root,destination,manifest['private_exports'])
    import numpy as np
    from run_study import RunGuard
    # Reuse existing owned directories only for read-only resource measurement.
    guard=RunGuard(started,rep.utc_now(),destination,destination/'public',destination/'private')
    guard(stage='independent_ar1_readback_start')
    sources=runner.load_sources(inputs)
    refs,_=runner.audit_references(inputs,sources,np,adapter._load_helpers(root),checkpoint=guard,arrays=guard.arrays)
    tables={name:list(csv.DictReader(io.StringIO((destination/'public'/name).read_text())))
        for name in ('ar1-summary.csv','ar1-annual.csv','ar1-nonoverlap.csv',
            'ar1-paired.csv','ar1-paired-annual.csv','ar1-paired-nonoverlap.csv')}
    counts={k:len(v) for k,v in tables.items()}
    require(list(counts.values())==[8,32,8,24,96,24],'AR1_INDEPENDENT_TABLE_COUNTS')
    checks=0;exact_fits=0;recursive_reports=0
    maximum_slope_error=0.;maximum_replay_relative_error=0.
    for cell in execution['spec']['cells']:
        s,h,w=cell['source'],cell['horizon'],cell['window'];cfg=inputs['spec']['sources'][s]
        source=sources[s];stem=f'{s}-h{h}-w{w}';n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
        trace_path=destination/'private'/(stem+'-traces.npz')
        raw=rep.read_bytes(root,trace_path,within=destination,cap=64*1024*1024)
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
        fit_data=rep.strict_json(rep.read_bytes(root,destination/'private'/(stem+'-fits.json'),within=destination))
        fits={f['refit_index']:f for f in fit_data['fit_records']}
        require(sorted(fits)==sorted(set(expected_refit)),'AR1_INDEPENDENT_FIT_INVENTORY')
        checked_refits=set()
        for j in (0,n//2,n-1):
            t,r=origins[j],expected_refit[j];fit=fits[r]
            require((fit['first_origin'],fit['last_origin'],fit['transition_count'])==
                (r-h-w+1,r-h,w+h-1),'AR1_INDEPENDENT_FIT_HISTORY')
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
                else:check_summary(row,score,groups[key])
                checks+=1
        guard(stage='independent_ar1_cell_checked',cell_id=stem)
    require(checks==192 and exact_fits==24 and recursive_reports==24,'AR1_INDEPENDENT_CHECK_INVENTORY')
    runner.verify_inputs(inputs);diag.verify_exports(root,destination,manifest['exports'])
    runner.verify_private_exports(root,destination,manifest['private_exports'])
    require(rep.read_bytes(root,destination/'public/ar1-replay-manifest.json',within=destination)==manifest_raw,
        'AR1_INDEPENDENT_MANIFEST_CHANGED')
    guard(stage='independent_ar1_readback_complete')
    receipt=dict(version=1,status='AR1_INDEPENDENT_READBACK_PASS',verified_utc=rep.utc_now(),
        ar1_manifest_sha256=rep.sha(manifest_raw),ar1_spec_sha256=execution['spec_sha256'],
        ar1_freeze_sha256=execution['freeze_sha256'],cells=8,aggregate_rows_independently_checked=checks,
        exact_fraction_fits=exact_fits,scalar_recursive_reports=recursive_reports,
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
