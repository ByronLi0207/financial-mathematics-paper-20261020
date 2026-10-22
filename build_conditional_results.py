"""Reconcile accepted fixed-selection traces and export every declared contrast.

No model is fitted. Inputs are the pinned source bytes and the 32 terminal
evaluation/reference receipts. Output is aggregate-only; private traces and raw
sources are never copied to the public results folder. A failed integrity check
prevents the verified audit receipt from being written.
"""
import os
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import csv
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import signal
import sys
import time
sys.dont_write_bytecode = True
import numpy as np
import study_core as core
import run_conditional_study as runner
from conditional_sources import load_source
from conditional_study import (FAMILIES, nonoverlap_origins, paired_comparison,
                               score_predictions, summarize_scores)
from run_study import RunGuard, create_attempt, arm_hard_deadline, utc_now

ROOT = Path(__file__).resolve().parent
FREEZE = 'e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb'
SELECTION = '531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def expected_cells(spec):
    cells = [('evaluation', s, h, w, f) for s, h, w, f in runner._inventory(spec)]
    cells += [('references', s, h, w, None)
              for s, cfg in spec['sources'].items()
              for h in spec['horizons'] for w in cfg['windows']]
    return cells


def receipt_path(cell):
    phase, source, h, w, family = cell
    stem = f'eval-{source}-h{h}-w{w}-{family}-01' if phase == 'evaluation' else f'ref-{source}-h{h}-w{w}-01'
    return Path('.scratch/revision-20261022') / stem / 'public/manifest.json'


def assert_same(actual, expected, context):
    if actual != expected:
        raise ValueError('aggregate or identity mismatch: ' + context)


def verify_resource(resource):
    if not (0 < resource['elapsed_seconds'] < 540
            and 0 < resource['peak_rss_bytes'] < 1610612736
            and 1 <= resource['maximum_observed_os_threads'] <= 2
            and resource['thread_snapshot_count'] > 0
            and resource['thread_probe_status'] == 'PASS'):
        raise ValueError('resource receipt not accepted')


def independent_peak(position, origins, horizon):
    # Deliberately use direct Python maxima, not the forecast label-cache code.
    return np.array([max(abs(float(position[int(t) + j])) for j in range(horizon + 1))
                     for t in origins], dtype=np.float64)


def verify_fit_records(rows, source_cfg, h, w, family, first, last):
    expected = list(range(first, last + 1, source_cfg['refit_step'])) if family else []
    assert_same([d['refit_index'] for d in rows], expected, 'fit schedule')
    for d in rows:
        r = d['refit_index']
        assert_same((d['training_first_origin'], d['training_last_origin'],
                     d['training_count'], d['latest_label_end']),
                    (r - h - w + 1, r - h, w, r), 'fit maturity')
        if family == 'QR':
            nonnegative = ('primal_objective','duality_gap','primal_residual','dual_residual',
                           'primal_tolerance','dual_tolerance','gap_tolerance')
            if any(type(d[k]) not in (int,float) or not math.isfinite(d[k]) or d[k]<0 for k in nonnegative):
                raise ValueError('invalid nonnegative numerical diagnostic')
            if type(d['dual_objective']) not in (int,float) or not math.isfinite(d['dual_objective']):
                raise ValueError('nonfinite dual objective')
            if type(d['iterations']) is not int or not 1<=d['iterations']<=10000:
                raise ValueError('iteration limit')
            p,q,g=d['primal_objective'],d['dual_objective'],d['duality_gap']
            if abs((p-q)-g)>256*np.finfo(np.float64).eps*max(1.,abs(p),abs(q)):
                raise ValueError('primal dual gap identity')
            numerator,denominator=float(.95).as_integer_ratio();grid=2**40
            if (d['dual_integer_lower']!=-((denominator-numerator)*grid//denominator)
                    or d['dual_integer_upper']!=numerator*grid//denominator):
                raise ValueError('dual grid box identity')
            if not (d['primal_residual'] <= d['primal_tolerance']
                    and d['dual_residual'] <= d['dual_tolerance']
                    and d['duality_gap'] <= d['gap_tolerance']
                    and d['dual_integer_sum'] == 0 and d['dual_grid_denominator'] == grid):
                raise ValueError('quantile numerical acceptance')


def verify_phase_labels(receipt, methods, expected_parameter):
    result=receipt['result']
    assert_same((receipt['status'],receipt['stop_code'],result['status'],result['failure'],result['candidate_rows']),
                ('COMPLETE',None,'COMPLETE',None,[]),'terminal fields')
    assert_same([r['method'] for r in result['summary_rows']],methods,'method inventory')
    for row in result['summary_rows']:
        assert_same(row['parameter'],expected_parameter,'summary selected parameter')
    for row in result['fit_diagnostics']:
        assert_same((row['method'],row['parameter']),(methods[0],expected_parameter),'fit selected method/parameter')


def verified_archive(raw, metadata):
    assert_same(metadata,dict(area='private',name='numeric-traces.npz',bytes=len(raw),sha256=sha(raw)),
                'private artifact identity')
    return np.load(io.BytesIO(raw),allow_pickle=False)


def verify_method(traces, method, origins, peak, floor, expected_refits):
    for name, expected in (('origins', origins), ('peak', peak), ('floor', floor),
                           ('refit_indices', expected_refits)):
        if not np.array_equal(traces[method + '_' + name], expected):
            raise ValueError('private trace mismatch: ' + method + '/' + name)
    capacity = traces[method + '_capacity']
    error = peak - capacity
    direct_loss = .95 * np.maximum(error, 0.) + .05 * np.maximum(-error, 0.)
    if not np.array_equal(traces[method + '_pinball'], direct_loss):
        raise ValueError('stored score mismatch: ' + method)
    scores = score_predictions(peak, capacity, floor, origins)
    if not np.array_equal(scores.pinball, direct_loss):
        raise ValueError('scorer arithmetic mismatch')
    return scores


def comparison_inventory(spec):
    contrasts = []
    for s, cfg in spec['sources'].items():
        for h in spec['horizons']:
            for w in cfg['windows']:
                for family in FAMILIES:
                    for rule in ('F', 'S', 'K'):
                        contrasts.append((s, h, w, family, w, 'frozen_' + rule, 'common_history'))
                for rule in ('F', 'S', 'K'):
                    contrasts.append((s, h, w, 'rolling_' + rule, w, 'frozen_' + rule, 'update_frequency'))
        if s == 'fx_hourly':
            for label in ('primary_contrast', 'h24_legacy_contrast'):
                c = cfg[label]
                contrasts.append((s, c['horizon'], c['window'], c['family'],
                                  c['reference_window'], c['reference_method'], label))
    return contrasts


def write_csv(path, rows):
    if not rows:
        raise ValueError('empty public table')
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write_or_verify(path,stream.getvalue().encode())


def write_or_verify(path,raw):
    if path.exists():
        assert_same(path.read_bytes(),raw,'existing export bytes '+path.name)
    else:
        with path.open('xb') as stream:stream.write(raw)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-number',type=int,default=1)
    args=parser.parse_args(argv)
    if not 1<=args.audit_number<=99:parser.error('audit number must be in1..99')
    started = time.monotonic(); started_utc = utc_now()
    spec, _ = runner.verify_executable_freeze(FREEZE)
    selected = runner.verify_selection_freeze(ROOT / 'protocol/revision-20261022/selection-freeze.json',
                                              SELECTION, FREEZE, spec)
    attempt = ROOT / f'.scratch/revision-20261022/evaluation-audit-{args.audit_number:02d}'
    public, private = create_attempt(attempt)
    guard = RunGuard(started, started_utc, attempt, public, private)
    arm_hard_deadline(); guard(stage='evaluation_audit_start')
    queue = json.loads((ROOT / 'state/revision-20261022/evaluation-queue-progress.json').read_bytes())
    expected = expected_cells(spec)
    assert_same([(d['phase'], d['source'], d['horizon'], d['window'], d['family'])
                 for d in queue['cells']], expected, 'queue inventory')
    sources = {s: load_source(ROOT / cfg['input_relative_path'], s,
        expected_sha256=cfg['sha256'], expected_bytes=cfg['bytes']) for s, cfg in spec['sources'].items()}
    origin_cache, peak_cache = {}, {}
    for s, source in sources.items():
        cfg = spec['sources'][s]
        origins = np.arange(cfg['evaluation_origin_first'], cfg['evaluation_origin_last'] + 1, dtype=np.int64)
        origin_cache[s] = origins
        for h in spec['horizons']:
            peak_cache[s, h] = independent_peak(source.position, origins, h)
    all_scores = {}; summary = []; annual = []; nonoverlap = []
    receipt_rows = []; receipt_raws = {}; fit_counts = {}; max_rss = 0; max_threads = 0; worker_seconds = 0.
    for cell, queued in zip(expected, queue['cells']):
        phase, s, h, w, family = cell; cfg = spec['sources'][s]; source = sources[s]
        relative = receipt_path(cell); assert_same(str(relative), queued['receipt_path'], 'queued path')
        raw = (ROOT / relative).read_bytes(); assert_same(sha(raw), queued['receipt_sha256'], 'queued hash')
        receipt = json.loads(raw)
        assert_same((receipt['status'], queued['status'], queued['stop_code'], queued['exit_code']),
                    ('COMPLETE', 'COMPLETE', None, 0), 'terminal receipt')
        assert_same(tuple(receipt[k] for k in ('phase', 'source', 'horizon', 'window', 'family')), cell, 'cell identity')
        assert_same(receipt['result']['status'], 'COMPLETE', 'phase result status')
        assert_same(receipt['executable_freeze_sha256'], FREEZE, 'executable freeze')
        assert_same(receipt['selection_freeze_sha256'], SELECTION if family else None, 'selection freeze')
        identity = receipt['source_identity']
        assert_same(receipt['result']['native_unit'],cfg['native_unit'],'result native unit')
        for name in ('sha256', 'bytes', 'record_count', 'native_unit'):
            assert_same(identity[name], cfg[name], 'source ' + name)
        verify_resource(receipt['resources'])
        origins = origin_cache[s]; peak = peak_cache[s, h]; floor = np.abs(source.position[origins])
        assert_same(receipt['result']['origin_identity'], runner._origin_identity(origins), 'origin fingerprint')
        if family:
            assert_same(receipt['result']['selection'],
                        dict(status='SELECTED', parameter=selected[s, h, w, family]['parameter']), 'selected parameter')
        methods = [family] if family else [p + '_' + r for p in
            (('rolling', 'frozen', 'one_state') if cfg['one_state_reference_neighbors'][str(w)] else ('rolling', 'frozen'))
            for r in ('F', 'S', 'K')]
        verify_phase_labels(receipt,methods,selected[s,h,w,family]['parameter'] if family else None)
        assert_same([r['method'] for r in receipt['result']['summary_rows']], methods, 'method inventory')
        year_count = len(np.unique(source.dates[origins].astype('datetime64[Y]')))
        assert_same(len(receipt['result']['year_rows']), len(methods) * year_count, 'receipt annual inventory')
        assert_same(len(receipt['result']['nonoverlap_rows']), len(methods), 'receipt grid inventory')
        trace_path = ROOT / relative.parent.parent / 'private/numeric-traces.npz'
        trace_raw = trace_path.read_bytes()
        assert_same(len(receipt['artifacts']),1,'artifact inventory')
        wanted_keys = {method + '_' + k for method in methods
                       for k in ('origins', 'peak', 'floor', 'refit_indices', 'capacity', 'pinball')}
        with verified_archive(trace_raw,receipt['artifacts'][0]) as traces:
            assert_same(set(traces.files), wanted_keys, 'private array inventory')
            for method, reported in zip(methods, receipt['result']['summary_rows']):
                expected_refits = (origins[0] + ((origins - origins[0]) // cfg['refit_step']) * cfg['refit_step']
                                   if family or method.startswith('frozen_') else origins)
                scores = verify_method(traces, method, origins, peak, floor, expected_refits)
                metrics = summarize_scores(scores)
                assert_same(dict(method=method, parameter=reported['parameter']) | metrics, reported, 'all summary')
                parameter = reported['parameter']
                if method.startswith('one_state_'):
                    parameter = cfg['one_state_reference_neighbors'][str(w)]
                meta = dict(source=s, native_unit=cfg['native_unit'], horizon=h, window=w, method=method,
                    parameter=parameter, refit_step=cfg['refit_step'] if family or method.startswith('frozen_') else 1,
                    plain_knn_full_pool_fallback=method == 'KNN' and parameter == w)
                summary.append(meta | metrics); all_scores[s, h, w, method] = scores
                date_years = source.dates[origins].astype('datetime64[Y]').astype(int) + 1970
                for year in np.unique(date_years):
                    mask = date_years == year
                    part = score_predictions(peak[mask], scores.capacities[mask], floor[mask], origins[mask])
                    metrics_year = summarize_scores(part)
                    wanted = dict(method=method, parameter=reported['parameter'], year=int(year)) | metrics_year
                    found = [r for r in receipt['result']['year_rows'] if r['method'] == method and r['year'] == int(year)]
                    assert_same(found, [wanted], 'annual summary')
                    annual.append(meta | dict(calendar_year=int(year)) | metrics_year)
                grid = nonoverlap_origins(int(origins[0]), int(origins[-1]), h); mask = np.isin(origins, grid)
                part = score_predictions(peak[mask], scores.capacities[mask], floor[mask], origins[mask])
                metrics_grid = summarize_scores(part)
                found = [r for r in receipt['result']['nonoverlap_rows'] if r['method'] == method]
                assert_same(found, [dict(method=method, parameter=reported['parameter']) | metrics_grid], 'nonoverlap summary')
                nonoverlap.append(meta | dict(stride_records=h + 1) | metrics_grid)
        verify_fit_records(receipt['result']['fit_diagnostics'], cfg, h, w, family, int(origins[0]), int(origins[-1]))
        fit_counts[family or 'references'] = fit_counts.get(family or 'references', 0) + len(receipt['result']['fit_diagnostics'])
        resource = receipt['resources']; max_rss = max(max_rss, resource['peak_rss_bytes'])
        max_threads = max(max_threads, resource['maximum_observed_os_threads']); worker_seconds += resource['elapsed_seconds']
        name = (f'evaluation-{s}-h{h}-w{w}-{family}.json' if family else f'references-{s}-h{h}-w{w}.json')
        receipt_raws[name] = raw
        receipt_rows.append(dict(public_file=name, sha256=sha(raw), bytes=len(raw), status=receipt['status'],
                                 elapsed_seconds=resource['elapsed_seconds'], peak_rss_bytes=resource['peak_rss_bytes']))
        guard.arrays(all_scores); guard(stage='evaluation_trace_audited')
    assert_same(len(summary), 90, 'summary inventory')
    assert_same(len(annual), 372, 'annual inventory')
    assert_same(len(nonoverlap), 90, 'nonoverlap inventory')
    # Preserve numerical continuity with the accepted prior FX experiment.
    historical_checks = []
    old = list(csv.DictReader((ROOT / 'results/revision-20261021/summary.csv').open()))
    for h in spec['horizons']:
        for set_id, prefix in (('full720', 'rolling_'), ('nearest360', 'one_state_')):
            for rule in ('F', 'S', 'K'):
                previous = [r for r in old if int(r['horizon']) == h and r['set_id'] == set_id and r['method_id'] == rule]
                assert_same(len(previous), 1, 'old FX reference inventory')
                current = summarize_scores(all_scores['fx_hourly', h, 720, prefix + rule])
                for key, value in current.items():
                    stored = previous[0][key]
                    parsed = None if stored == '' else (stored if isinstance(value, str) else float(stored))
                    assert_same(value, parsed, 'old FX aggregate ' + key)
                historical_checks.append(dict(horizon=h, window=720, method=prefix + rule, status='EXACT_ALL_AGGREGATES'))
    comparisons = []; comparison_years = []; comparison_nonoverlap = []
    inventory = comparison_inventory(spec)
    assert_same(len(inventory), 98, 'paired inventory')
    for s, h, lw, lm, rw, rm, category in inventory:
        left = all_scores[s, h, lw, lm]; right = all_scores[s, h, rw, rm]
        cfg = spec['sources'][s]; primary = cfg['primary_contrast']
        is_primary = (h, lw, lm, rw, rm) == (primary['horizon'], primary['window'], primary['family'],
            primary['reference_window'], primary['reference_method'])
        meta = dict(contrast_id=f'{s}-h{h}-{lm}{lw}-minus-{rm}{rw}', source=s, native_unit=cfg['native_unit'],
            horizon=h, left_window=lw, left_method=lm, right_window=rw, right_method=rm,
            contrast_category=category, declared_source_primary=is_primary, h24_legacy_contrast=category == 'h24_legacy_contrast')
        paired = paired_comparison(left, right, sources[s].dates[left.origins], horizon=h)
        # Independently form scalar paired means from the stored loss vectors.
        direct = math.fsum(float(a) - float(b) for a, b in zip(left.pinball, right.pinball)) / len(left.origins)
        assert_same(paired['all']['mean_pinball_difference'], direct, 'direct paired loss')
        assert_same(sum(y['origin_count'] for y in paired['years']), len(left.origins), 'annual count')
        weighted = math.fsum(y['origin_count'] * y['mean_pinball_difference'] for y in paired['years']) / len(left.origins)
        core._assert_mean_equal(weighted, direct, len(left.origins), max(1., abs(direct)))
        comparisons.append(meta | paired['all'])
        comparison_years.extend(meta | year for year in paired['years'])
        comparison_nonoverlap.append(meta | paired['nonoverlap'])
    assert_same(len({r['contrast_id'] for r in comparisons}), 98, 'unique paired inventory')
    assert_same(len(comparison_years), 388, 'paired annual inventory')
    assert_same(sum(r['declared_source_primary'] for r in comparisons), 2, 'primary inventory')
    for h in spec['horizons']:
        a = all_scores['nyfed_weekly', h, 52, 'KNN']; b = all_scores['nyfed_weekly', h, 52, 'frozen_F']
        if not np.array_equal(a.capacities, b.capacities):
            raise ValueError('plain full-pool KNN identity failed')
    runner.verify_executable_freeze(FREEZE)
    output = ROOT / 'results/revision-20261022'
    tables = {'evaluation-summary.csv': summary, 'evaluation-annual.csv': annual,
              'evaluation-nonoverlap.csv': nonoverlap, 'paired-comparisons.csv': comparisons,
              'paired-annual.csv': comparison_years, 'paired-nonoverlap.csv': comparison_nonoverlap}
    for name, rows in tables.items():
        write_csv(output / name, rows)
    for name, raw in receipt_raws.items():
        write_or_verify(output/name,raw)
    guard(stage='evaluation_audit_final')
    exports = [dict(path=name, bytes=(output / name).stat().st_size, sha256=sha((output / name).read_bytes()))
               for name in [*tables, *receipt_raws]]
    audit = dict(version=1, status='VERIFIED', created_utc=utc_now(),
        scope='All accepted fixed-selection evaluation and declared references; descriptive paired comparisons; no model refit',
        executable_freeze_sha256=FREEZE, selection_freeze_sha256=SELECTION,
        evaluation_cell_count=24, reference_cell_count=8, summary_rows=len(summary), annual_rows=len(annual),
        nonoverlap_method_rows=len(nonoverlap), paired_rows=len(comparisons), paired_annual_rows=len(comparison_years),
        paired_nonoverlap_rows=len(comparison_nonoverlap), historical_exact_checks=historical_checks,
        full_pool_identity_checks=2, independent_peak_checks='direct Python max(abs(position[t:t+H+1])) at every declared source/H/origin',
        maximum_worker_peak_rss_bytes=max_rss, maximum_observed_worker_threads=max_threads,
        total_reported_worker_seconds=worker_seconds, fit_counts=fit_counts, receipts=receipt_rows,
        audit_resources=dict(guard.resources), exports=exports, actual_export_bytes=sum(r['bytes'] for r in exports),
        output_counter_scope='RunGuard tree counters cover the audit attempt only; actual_export_bytes separately covers the listed public exports',
        builder_sha256=sha(Path(__file__).read_bytes()))
    audit_name='evaluation-audit.json' if args.audit_number==1 else f'evaluation-audit-{args.audit_number:02d}.json'
    audit['audit_number']=args.audit_number
    if args.audit_number>1:
        prior=output/'evaluation-audit.json'
        audit['prior_verified_audit']=dict(path=prior.name,sha256=sha(prior.read_bytes()))
        audit['existing_aggregate_and_receipt_exports']='All existing listed export bytes matched exactly; no forecast or scientific specification changed'
    with (output / audit_name).open('x') as stream:
        json.dump(audit, stream, indent=2, allow_nan=False); stream.write('\n')
    signal.setitimer(signal.ITIMER_REAL, 0)
    print(json.dumps({k: audit[k] for k in ('status', 'evaluation_cell_count', 'reference_cell_count', 'summary_rows',
        'annual_rows', 'paired_rows', 'paired_annual_rows', 'maximum_worker_peak_rss_bytes', 'maximum_observed_worker_threads',
        'total_reported_worker_seconds', 'actual_export_bytes')}, indent=2))


if __name__ == '__main__':
    main()
