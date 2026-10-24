#!/usr/bin/env python3
"""Independent readback of a completed R6 archive; never creates forecasts.

Run only after the single authorised study run has finished.  This reader does
not import the study runner, selectors, source readers, label builders or fits.
Its sole write is an exclusive new public verification.json.  Per-origin arrays
remain private; only aggregate verification facts and file identities are emitted.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import statistics


ROOT = Path(__file__).resolve().parent
DESIGN = Path('protocol/supervisor-20261023/r6-design.md')
DESIGN_COMMIT = '6c0eef44c46a0ff525264b13ae1dae9b821ad3c2'
DESIGN_SHA256 = 'de301f131426ed9b185451d87e3aee1726d978dd2d55ffd322efc02477b6bbae'
DESIGN_TIMESTAMP = '2026-10-23T13:22:37-07:00'
FINITE = ('0.001', '0.01', '0.1', '1', '10')
CANDIDATES = FINITE + ('I',)
REPORTS = ('F', 'I', 'R0', 'R1', 'R2', 'R3')
KEYS = ('phase', 'source', 'series_key', 'horizon', 'window')
MEASURES = (
    'origin_count', 'mean_pinball', 'mean_capacity', 'mean_extra_allowance',
    'strict_breach_count', 'strict_breach_rate', 'mean_positive_overrun',
    'conditional_mean_overrun', 'conditional_overrun_denominator',
    'conditional_overrun_undefined_reason', 'mean_unused_allowance',
)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def rows(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def blank(value):
    return value is None or value == ''


def same(a, b):
    """CSV/JSON reconciliation tolerance; never used in selection eligibility."""
    if blank(a) or blank(b):
        return blank(a) and blank(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return str(a).lower() == str(b).lower()
    if isinstance(a, (dict, list, tuple)) or isinstance(b, (dict, list, tuple)):
        return a == b
    try:
        x, y = float(a), float(b)
    except (ValueError, TypeError):
        return str(a) == str(b)
    return math.isfinite(x) and math.isfinite(y) and math.isclose(x, y, rel_tol=2e-13, abs_tol=1e-11)


def time_of(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def key(row, report=False):
    result = tuple(int(row[k]) if k in ('horizon', 'window') else row[k] for k in KEYS)
    return result + ((row['report'],) if report else ())


def group_name(group):
    return f"{group['phase']}-{group['series_key']}-h{group['horizon']}-w{group['window']}"


def inventory(spec):
    answer = []
    for phase in ('retro', 'inspected'):
        for source in ('nyfed_weekly', 'fx_hourly'):
            names = [x['series_key'] for x in spec['weekly_series']] if source == 'nyfed_weekly' else ['fx_hourly']
            for name in names:
                for h in spec['horizons']:
                    for w in spec['sources'][source][phase + '_windows']:
                        answer.append(dict(phase=phase, source=source, series_key=name, horizon=h, window=w))
    return answer


def expected_folds(cfg, phase, window):
    first, last = cfg[phase + '_validation']
    earliest = cfg['feature_prefix'] + window + 23
    size = cfg['refit_step']
    end = first - 25
    prefix = []
    while end - size + 1 >= earliest:
        prefix.append([end - size + 1, end])
        end -= size + 24
    return list(reversed(prefix)) + [[first, last]]


def oracle_selection(losses, origins, horizon, candidate_ids, paired):
    """Scalar independent selection from already archived loss arrays."""
    if any(losses.get(c) is None for c in candidate_ids):
        return dict(status='FAILED', selected_id=None)
    n = len(origins)
    if not n or any(len(losses[c]) != n or any(not math.isfinite(float(x)) for x in losses[c]) for c in candidate_ids):
        return dict(status='FAILED', selected_id=None)
    means = {c: math.fsum(float(x) for x in losses[c]) / n for c in candidate_ids}
    minimum = min(means.values())
    best = next(c for c in reversed(candidate_ids) if means[c] == minimum)
    diagnostics = {c: dict(mean_loss=means[c]) for c in candidate_ids}
    if not paired:
        return dict(status='SELECTED', selected_id=best, best_id=best, n=n, candidates=diagnostics)
    bandwidth = max(horizon, math.floor(4 * (n / 100) ** (2 / 9)))
    if n <= bandwidth:
        return dict(status='FAILED', selected_id=None)
    eligible = []
    for c in candidate_ids:
        differences = [float(x) - float(y) for x, y in zip(losses[c], losses[best])]
        mean_gap = math.fsum(differences) / n
        centered = [x - mean_gap for x in differences]
        at_origin = dict(zip(origins, centered))
        gamma0 = math.fsum(x * x for x in centered) / n
        terms = []
        pairs = [n]
        for lag in range(1, bandwidth + 1):
            products = [at_origin[t] * at_origin[t - lag] for t in origins if t - lag in at_origin]
            pairs.append(len(products))
            terms.append(2 * (1 - lag / (bandwidth + 1)) * (math.fsum(products) / n))
        raw_lrv = math.fsum([gamma0, *terms])
        if not math.isfinite(raw_lrv):
            return dict(status='FAILED', selected_id=None)
        se = math.sqrt(max(raw_lrv, 0) / n)
        accepted = mean_gap <= se
        if accepted:
            eligible.append(c)
        diagnostics[c].update(paired_mean_gap=mean_gap, raw_lrv=raw_lrv,
            lrv=max(raw_lrv, 0), standard_error=se, bandwidth=bandwidth,
            eligible=accepted, lag_pair_counts=pairs,
            nw_status='NUMERICAL_LRV_CLIPPED_TO_ZERO' if raw_lrv < 0 else 'OK')
    return dict(status='SELECTED', selected_id=eligible[-1], best_id=best,
        n=n, bandwidth=bandwidth, candidates=diagnostics)


def independent_assessment(public_rows):
    indexed = {key(r, True): r for r in public_rows}
    weekly = {rule: [r for r in public_rows if r['phase'] == 'retro'
        and r['source'] == 'nyfed_weekly' and r['report'] == rule] for rule in ('R0', 'R2')}
    def usable(row):
        return row['status'] == 'COMPLETE' and not blank(row.get('percent_vs_F')) and math.isfinite(float(row['percent_vs_F']))
    values = {rule: [float(r['percent_vs_F']) for r in rr if usable(r)] for rule, rr in weekly.items()}
    full = {rule: len(weekly[rule]) == 26 and len(values[rule]) == 26 for rule in weekly}
    med = {rule: statistics.median(values[rule]) if full[rule] else None for rule in weekly}
    worst = max(values['R2']) if full['R2'] else None
    s1 = dict(status='PASS' if full['R2'] and worst <= 25 and med['R2'] <= 5 else 'NOT_MET',
        complete_required=26, complete_count=len(values['R2']), worst_percent_vs_F=worst, median_percent_vs_F=med['R2'])
    cells = []
    for window in (720, 2880):
        r0 = indexed[('retro', 'fx_hourly', 'fx_hourly', 6, window, 'R0')]
        r2 = indexed[('retro', 'fx_hourly', 'fx_hourly', 6, window, 'R2')]
        valid0, valid2 = usable(r0), usable(r2)
        p0 = float(r0['percent_vs_F']) if valid0 else None
        p2 = float(r2['percent_vs_F']) if valid2 else None
        eligible = valid0 and p0 < 0
        required_failed = not valid0 or (eligible and not valid2)
        retained = eligible and valid2 and p2 <= .5 * p0
        cells.append(dict(window=window, R0_percent_vs_F=p0, R2_percent_vs_F=p2,
            eligible=eligible, half_gain_retained=retained,
            status='NOT_MET' if required_failed or (eligible and not retained) else 'PASS' if eligible else 'NOT_ELIGIBLE'))
    eligible_count = sum(c['eligible'] for c in cells)
    s2 = dict(status='NOT_MET' if any(c['status'] == 'NOT_MET' for c in cells) else 'PASS' if eligible_count else 'NOT_ASSESSABLE',
        eligible_count=eligible_count, cells=cells)
    s3 = dict(status='PASS' if full['R0'] and full['R2'] and med['R2'] < med['R0'] else 'NOT_MET',
        R0_complete_count=len(values['R0']), R2_complete_count=len(values['R2']),
        R0_median_percent_vs_F=med['R0'], R2_median_percent_vs_F=med['R2'])
    passed = s1['status'] == s2['status'] == 'PASS'
    return dict(S1=s1, S2=s2, S3=s3,
        publication_gate=dict(status='METHOD_SECTION' if passed else 'ROBUSTNESS_PARAGRAPH', abstract_mention=passed),
        descriptive_only=True, pooled_tests_performed=False)


class Readback:
    def __init__(self, root):
        self.root = root
        self.public = root / 'results/supervisor-20261023/r6'
        self.private = root / '.scratch/r6-20261023/run'
        self.issues = []
        self.counts = Counter()
        self.file_identities = []
        self.trace_by_hash = {}
        self.trace_by_segment = {}

    def check(self, condition, code, **detail):
        self.counts['checks'] += 1
        if not condition:
            self.issues.append(dict(code=code, **detail))
        return condition

    def equal_fields(self, actual, expected, fields, context):
        for field in fields:
            self.check(same(actual.get(field), expected.get(field)), 'FIELD_MISMATCH', context=context,
                field=field, actual=actual.get(field), expected=expected.get(field))

    def compare_tree(self, actual, expected, context):
        if isinstance(expected, dict):
            if not self.check(isinstance(actual, dict), 'OBJECT_TYPE', context=context):
                return
            for field, value in expected.items():
                self.compare_tree(actual.get(field), value, context + '.' + field)
        elif isinstance(expected, list):
            if self.check(isinstance(actual, list) and len(actual) == len(expected), 'LIST_LENGTH', context=context):
                for i, (a, e) in enumerate(zip(actual, expected)):
                    self.compare_tree(a, e, f'{context}[{i}]')
        else:
            self.check(same(actual, expected), 'VALUE_MISMATCH', context=context, actual=actual, expected=expected)

    def checked_file(self, item, context):
        path = Path(item['path'])
        if not path.is_absolute():
            path = self.root / path
        if not self.check(path.is_file(), 'FILE_MISSING', context=context, path=str(path)):
            return
        got = digest(path)
        self.check(got == item['sha256'], 'FILE_HASH', context=context, path=item['path'])
        if 'bytes' in item:
            self.check(path.stat().st_size == item['bytes'], 'FILE_BYTES', context=context, path=item['path'])
        self.counts[context + '_files'] += 1

    def check_provenance(self, spec, receipt, manifest, seal):
        design_path = self.root / DESIGN
        self.check(digest(design_path) == DESIGN_SHA256, 'DESIGN_BYTES')
        for context, obj in (('run_receipt', receipt), ('input_manifest', manifest), ('retro_seal', seal)):
            self.check(obj.get('design_commit') == DESIGN_COMMIT, 'DESIGN_COMMIT', context=context)
            if context != 'retro_seal':
                self.check(obj.get('design_sha256') == DESIGN_SHA256, 'DESIGN_SHA256', context=context)
                self.check(time_of(obj['design_commit_timestamp']) == time_of(DESIGN_TIMESTAMP), 'DESIGN_COMMIT_TIME', context=context)
        for item in manifest['files']:
            self.checked_file(item, 'input')
        self.check(receipt['input_manifest_sha256'] == digest(self.public / 'input-manifest.json'), 'INPUT_MANIFEST_BINDING')
        ledger_path = self.root / '.scratch/r6-20261023/protected-before.json'
        ledger = load(ledger_path)
        self.check(ledger.get('base_head') == DESIGN_COMMIT, 'PROTECTED_BASE_HEAD')
        self.check(len(ledger['files']) == 525, 'PROTECTED_BASELINE_COUNT', actual=len(ledger['files']))
        for path, expected_hash in ledger['files'].items():
            self.checked_file(dict(path=path, sha256=expected_hash), 'protected_baseline')
        self.check(any(i['path'] == str(ledger_path.relative_to(self.root)) for i in manifest['files']), 'PROTECTED_LEDGER_INPUT_BINDING')
        input_by_path = {i['path']: i for i in manifest['files']}
        for source in spec['weekly_series']:
            entry = input_by_path.get(source['local_path'], {})
            self.check(entry.get('sha256') == source['raw_sha256'] and entry.get('bytes') == source['raw_bytes'],
                'FROZEN_WEEKLY_SOURCE_IDENTITY', path=source['local_path'])
        fx = spec['sources']['fx_hourly']
        entry = input_by_path.get(fx['local_path'], {})
        self.check(entry.get('sha256') == fx['sha256'] and entry.get('bytes') == fx['bytes'], 'FROZEN_FX_SOURCE_IDENTITY')
        design_time = time_of(DESIGN_TIMESTAMP)
        retro = time_of(receipt['first_retro_calculation_utc']) if receipt.get('first_retro_calculation_utc') else None
        inspected = time_of(receipt['first_inspected_calculation_utc']) if receipt.get('first_inspected_calculation_utc') else None
        seal_time = time_of(seal['sealed_utc'])
        receipt_seal_time = time_of(receipt['retro_sealed_utc'])
        completed = time_of(receipt['completed_utc'])
        self.check(design_time < seal_time <= receipt_seal_time <= completed, 'SEAL_TIME_ORDER')
        if retro is not None:
            self.check(design_time < retro <= seal_time, 'RETRO_TIME_ORDER')
        if inspected is not None:
            self.check(receipt_seal_time < inspected <= completed, 'INSPECTED_TIME_ORDER')
        self.check(time_of(receipt['run_started_utc']) > design_time, 'RUN_AFTER_DESIGN')
        self.check(receipt.get('run_count') == 1 and receipt.get('no_retries') is True, 'SINGLE_RUN_NO_RETRIES')
        self.check(receipt.get('input_hashes_unchanged') is True, 'RUN_INPUT_UNCHANGED_RECEIPT')
        self.check(receipt.get('resource_limits') == spec['resource_limits'], 'FROZEN_RESOURCE_LIMITS')
        resources = receipt.get('resources', {})
        self.check(resources.get('requested_numerical_threads') == 1 and
            resources.get('maximum_observed_os_threads', math.inf) <= 2 and
            resources.get('thread_probe_status') == 'PASS', 'NUMERICAL_THREAD_RECEIPT')
        self.check(resources.get('peak_rss_bytes', math.inf) < 2147483648, 'MEMORY_RECEIPT')
        self.check(seal.get('status') == 'SEALED' and seal.get('group_count') == 30 and seal.get('report_row_count') == 180, 'RETRO_SEAL_COUNTS')
        self.check(receipt.get('retro_seal_sha256') == digest(self.public / 'retro-seal.json'), 'RETRO_SEAL_BINDING')
        for item in seal['files']:
            self.checked_file(item, 'retro_seal')
        for path, expected_hash in spec['core_sha256'].items():
            self.check(digest(self.root / path) == expected_hash, 'CORE_FROZEN', path=path)

    def check_trace(self, path, meta, spec, group, np):
        with np.load(path, allow_pickle=False) as archive:
            data = {name: archive[name].copy() for name in archive.files}
        if 'peak' not in data:
            self.counts['incomplete_trace_files'] += 1
            return
        ctx = str(path.relative_to(self.root))
        required = ('origins', 'capacity', 'peak', 'floor', 'pinball', 'strict_breach', 'overrun', 'unused', 'refit_indices')
        if not self.check(all(k in data for k in required), 'TRACE_FIELDS', path=ctx):
            return
        n = len(data['origins'])
        if not self.check(n > 0 and all(data[k].shape == (n,) for k in required), 'TRACE_SHAPE', path=ctx):
            return
        ids = [int(x) for x in data['origins']]
        self.check(all(b == a + 1 for a, b in zip(ids, ids[1:])), 'TRACE_CONTIGUOUS_SEGMENT', path=ctx)
        self.check(all(np.isfinite(data[k]).all() for k in required), 'TRACE_FINITE', path=ctx)
        capacity, peak, floor = data['capacity'], data['peak'], data['floor']
        overrun = np.maximum(peak - capacity, 0.0)
        unused = np.maximum(capacity - peak, 0.0)
        pinball = .95 * overrun + .05 * unused
        breaches = peak > capacity
        for field, computed in (('pinball', pinball), ('strict_breach', breaches), ('overrun', overrun), ('unused', unused)):
            self.check(np.allclose(data[field], computed, rtol=2e-14, atol=1e-12), 'TRACE_ARITHMETIC', path=ctx, field=field)
        self.check(bool(np.all(capacity >= floor) and np.all(floor >= 0) and np.all(peak >= floor)), 'ANCHOR_PROJECTION', path=ctx)
        count = int(np.count_nonzero(breaches))
        average = lambda a: math.fsum(float(x) for x in a) / n
        total_overrun = math.fsum(float(x) for x in overrun)
        summary = dict(origin_count=n, mean_pinball=average(pinball), mean_capacity=average(capacity),
            mean_extra_allowance=average(capacity - floor), strict_breach_count=count,
            strict_breach_rate=count / n, mean_positive_overrun=total_overrun / n,
            conditional_mean_overrun=total_overrun / count if count else None,
            conditional_overrun_denominator=count,
            conditional_overrun_undefined_reason=None if count else 'NO_STRICT_BREACHES',
            mean_unused_allowance=average(unused))
        self.equal_fields(meta['summary'], summary, MEASURES, ctx + '.summary')
        trace_hash = digest(path)
        self.check(meta['trace_sha256'] == trace_hash, 'TRACE_METADATA_HASH', path=ctx)
        candidate = meta['candidate_id']
        cfg = spec['sources'][group['source']]
        w, step = int(meta['window']), int(meta['refit_step'])
        expected_refits = [ids[0] + step * ((t - ids[0]) // step) for t in ids]
        self.check(data['refit_indices'].tolist() == expected_refits, 'REFIT_RESET_SCHEDULE', path=ctx)
        refits = sorted(set(expected_refits))
        fits = meta.get('fit_diagnostics', [])
        self.check(len(fits) == len(refits), 'REFIT_DIAGNOSTIC_COUNT', path=ctx)
        for refit, fit in zip(refits, fits):
            expected = dict(refit_index=refit, training_first_origin=refit - group['horizon'] - w + 1,
                training_last_origin=refit - group['horizon'], training_count=w, latest_label_end=refit)
            self.equal_fields(fit, expected, expected, ctx + '.refit')
            minimum = 0 if candidate in ('F', 'I') else cfg['feature_prefix']
            self.check(expected['training_first_origin'] >= minimum, 'TRAINING_MATURITY', path=ctx, refit=refit)
        max_record = cfg['original_validation_start'] if group['phase'] == 'retro' else cfg['record_count']
        self.check(ids[-1] + group['horizon'] < max_record, 'TARGET_PREFIX_BOUNDARY', path=ctx)
        item = dict(path=ctx, group=group, candidate_id=candidate, window=w, refit_step=step,
            origins=ids, losses=[float(x) for x in data['pinball']], summary=summary, trace_sha256=trace_hash)
        self.trace_by_hash.setdefault(trace_hash, []).append(item)
        segment_key = (key(group), candidate, ids[0], ids[-1], w, step)
        self.check(segment_key not in self.trace_by_segment, 'DUPLICATE_SUCCESSFUL_SEGMENT', path=ctx)
        self.trace_by_segment[segment_key] = item
        self.counts['complete_trace_files'] += 1
        self.counts['archived_scored_origins'] += n

    def segment(self, group, candidate, bounds, cfg, *, window=None, step=None):
        return self.trace_by_segment.get((key(group), candidate, bounds[0], bounds[1],
            group['window'] if window is None else window, cfg['refit_step'] if step is None else step))

    def check_selection(self, receipt, expected, context):
        self.equal_fields(receipt, expected, ('status', 'selected_id'), context)
        if expected['status'] != 'SELECTED':
            return
        self.equal_fields(receipt, expected, ('best_id', 'n'), context)
        if 'bandwidth' in expected:
            self.equal_fields(receipt, expected, ('bandwidth',), context)
        actual_candidates = {r['candidate_id']: r for r in receipt.get('candidates', [])}
        for candidate, facts in expected['candidates'].items():
            self.check(candidate in actual_candidates, 'SELECTION_CANDIDATE_MISSING', context=context, candidate=candidate)
            self.equal_fields(actual_candidates.get(candidate, {}), facts, facts, context + '.' + candidate)

    def check_group(self, result, spec, seal):
        group = result['group']
        cfg = spec['sources'][group['source']]
        context = group_name(group)
        self.check([r['report'] for r in result['rows']] == list(REPORTS), 'GROUP_REPORT_INVENTORY', context=context)
        for row in result['rows']:
            self.check(key(row) == key(group), 'GROUP_ROW_IDENTITY', context=context)
        if 'raw_prefix_count' in result:
            self.check(result['raw_prefix_count'] == (cfg['original_validation_start'] if group['phase'] == 'retro' else cfg['record_count']), 'RAW_PREFIX_COUNT', context=context)
        folds = expected_folds(cfg, group['phase'], group['window'])
        if 'r3_fold_bounds' in result:
            self.check(result['r3_fold_bounds'] == folds, 'R3_FOLD_GEOMETRY', context=context)
            self.check(result['r3_design_status'] == ('NO_EXTRA_FOLDS' if len(folds) == 1 else 'PREFIX_PLUS_OUTER_VALIDATION'), 'R3_DESIGN_STATUS', context=context)
            for previous, following in zip(folds, folds[1:]):
                self.check(following[0] - previous[1] == 25 and previous[1] + group['horizon'] < following[0], 'R3_PURGED_LABEL_MATURITY', context=context)
            self.counts['groups_with_fold_geometry'] += 1
        selection_time = result.get('selection_frozen_utc')
        folder = self.private / group['phase'] / context
        if selection_time:
            frozen = load(folder / 'selection-before-evaluation.json')
            self.check(frozen['design_commit'] == DESIGN_COMMIT and frozen['design_sha256'] == DESIGN_SHA256, 'GROUP_FROZEN_DESIGN', context=context)
            self.check(frozen['group'] == group and frozen['rules'] == result['selections'], 'GROUP_FROZEN_SELECTION', context=context)
            self.check(frozen['fold_bounds'] == folds and frozen['validation_candidates'] == result['validation_candidates'], 'GROUP_FROZEN_VALIDATION', context=context)
            self.check(frozen['selection_frozen_utc'] == selection_time, 'GROUP_FROZEN_TIME', context=context)
            self.check(time_of(selection_time) < time_of(result['evaluation_started_utc']), 'SELECTION_PRECEDES_EVALUATION', context=context)
            if group['phase'] == 'inspected':
                self.check(time_of(selection_time) > time_of(seal['sealed_utc']), 'INSPECTED_SELECTION_AFTER_RETRO_SEAL', context=context)
            self.counts['frozen_selections'] += 1
        elif any(r['status'] == 'COMPLETE' for r in result['rows']):
            self.check(False, 'COMPLETE_WITHOUT_FROZEN_SELECTION', context=context)
        val = cfg[group['phase'] + '_validation']
        val_origins = list(range(val[0], val[1] + 1))
        outer = {c: self.segment(group, c, val, cfg) for c in CANDIDATES}
        for candidate_row in result.get('validation_candidates', []):
            candidate = candidate_row['candidate_id']
            trace = outer[candidate]
            self.check((candidate_row['status'] == 'COMPLETE') == (trace is not None), 'OUTER_CANDIDATE_STATUS', context=context, candidate=candidate)
            if trace:
                self.equal_fields(candidate_row, dict(origin_count=len(val_origins), mean_pinball=trace['summary']['mean_pinball']), ('origin_count', 'mean_pinball'), context + '.validation.' + candidate)
        losses = {c: t['losses'] if t else None for c, t in outer.items()}
        selections = result.get('selections', {})
        for rule, selected in selections.items():
            if rule == 'R3':
                origins = [t for a, b in folds for t in range(a, b + 1)]
                all_segments = {c: [self.segment(group, c, f, cfg) for f in folds] for c in CANDIDATES}
                pool = {c: None if any(s is None for s in ss) else [x for s in ss for x in s['losses']] for c, ss in all_segments.items()}
                expected = oracle_selection(pool, origins, group['horizon'], CANDIDATES, True)
            else:
                expected = oracle_selection(losses, val_origins, group['horizon'], FINITE if rule == 'R0' else CANDIDATES, rule == 'R2')
            self.check_selection(selected, expected, context + '.' + rule)
            self.counts['independent_selections'] += 1
        if len(folds) == 1 and 'R3' in selections:
            self.check(selections['R3'] == selections['R2'], 'NO_EXTRA_FOLDS_IDENTITY', context=context)
        by_report = {r['report']: r for r in result['rows']}
        frow = by_report['F']
        for report, row in by_report.items():
            if row['status'] == 'COMPLETE':
                trace = self.segment(group, row['selected_id'], cfg[group['phase'] + '_evaluation'], cfg)
                if self.check(trace is not None, 'SELECTED_TRACE_MISSING', context=context, report=report):
                    self.equal_fields(row, trace['summary'], MEASURES, context + '.' + report)
                    self.check(trace['trace_sha256'] == row['trace_sha256'], 'SELECTED_EVALUATION_IDENTITY', context=context, report=report)
                if report in ('F', 'I'):
                    self.check(row['selected_id'] == report, 'REFERENCE_IDENTITY', context=context, report=report)
                else:
                    self.check(selections.get(report, {}).get('selected_id') == row['selected_id'] and selections.get(report, {}).get('status') == 'SELECTED', 'PUBLIC_SELECTED_ID', context=context, report=report)
            else:
                self.check(bool(row.get('reason')), 'FAILURE_REASON_REQUIRED', context=context, report=report)
                self.check(all(blank(row.get(m)) for m in MEASURES) and blank(row.get('trace_sha256')), 'FAILURE_HAS_NO_PARTIAL_METRICS', context=context, report=report)
            expected_percent = (100 * (row['mean_pinball'] / frow['mean_pinball'] - 1)
                if row['status'] == frow['status'] == 'COMPLETE' and frow['mean_pinball'] > 0 else None)
            self.check(same(row.get('percent_vs_F'), expected_percent), 'PERCENT_VS_F', context=context, report=report)
            if report in selections and selections[report].get('status') == 'FAILED':
                self.check(row['status'] == 'FAILED' and blank(row.get('selected_id')), 'REQUIRED_CANDIDATE_FAILURE_PROPAGATION', context=context, report=report)
            self.counts['report_rows'] += 1
        for a in result['rows']:
            for b in result['rows']:
                if a.get('selected_id') and a.get('selected_id') == b.get('selected_id'):
                    self.check(a['status'] == b['status'] and same(a.get('trace_sha256'), b.get('trace_sha256')), 'SHARED_SELECTED_REPORT_CONSISTENCY', context=context)
        if 'primary_replication' in result:
            self.check_primary(result, losses, val_origins, cfg, folder)

    def check_primary(self, result, losses, val_origins, cfg, folder):
        group, p = result['group'], result['primary_replication']
        context = p['id']
        is_fx = group['source'] == 'fx_hourly'
        self.check(group['phase'] == 'retro' and group['horizon'] == 6 and
            (group['window'] == 2880 if is_fx else group['series_key'] == 'PDPOSGS-B' and group['window'] == 52), 'PRIMARY_GROUP', context=context)
        self.check(p['reference'] == ('rolling corrected F W720 d1' if is_fx else 'frozen corrected F W52 d13'), 'PRIMARY_REFERENCE', context=context)
        if not is_fx:
            self.check('original W260 primary not exactly replicated' in (p.get('limitation') or ''), 'PRIMARY_W52_LIMITATION', context=context)
        if 'primary_selection' in result:
            expected = oracle_selection(losses, val_origins, 6, FINITE[:3], False)
            self.check_selection(result['primary_selection'], expected, context + '.original_three_menu')
            frozen = load(folder / 'selection-before-evaluation.json')
            self.check(frozen['primary_selection'] == result['primary_selection'], 'PRIMARY_FROZEN_SELECTION', context=context)
            if p['status'] not in ('NOT_RUN', 'TIME_LIMIT'):
                self.check(same(p.get('selected_id'), expected.get('selected_id')), 'PRIMARY_SELECTED_ID', context=context)
        if p['status'] == 'COMPLETE':
            qr = self.segment(group, p['selected_id'], cfg['retro_evaluation'], cfg)
            fr = self.segment(group, 'F', cfg['retro_evaluation'], cfg, window=720, step=1) if is_fx else self.segment(group, 'F', cfg['retro_evaluation'], cfg)
            if self.check(qr is not None and fr is not None, 'PRIMARY_TRACES', context=context):
                self.check(qr['trace_sha256'] == p['QR_trace_sha256'] and fr['trace_sha256'] == p['F_trace_sha256'], 'PRIMARY_TRACE_HASH_BINDING', context=context)
                q, f = qr['summary']['mean_pinball'], fr['summary']['mean_pinball']
                facts = dict(QR_mean_pinball=q, F_mean_pinball=f, percent_vs_reference=100 * (q / f - 1) if f > 0 else None,
                    direction_replicated=q < f if is_fx else q > f)
                self.equal_fields(p, facts, facts, context)
                self.check(qr['candidate_id'] == p['selected_id'] and qr['window'] == group['window'], 'PRIMARY_QR_IDENTITY', context=context)
                self.check(fr['candidate_id'] == 'F' and fr['window'] == (720 if is_fx else 52) and fr['refit_step'] == (1 if is_fx else 13), 'PRIMARY_F_IDENTITY', context=context)
                self.check(qr['origins'] == fr['origins'] == list(range(*[cfg['retro_evaluation'][0], cfg['retro_evaluation'][1] + 1])), 'PRIMARY_EVALUATION_ORIGINS', context=context)
        else:
            self.check(bool(p.get('reason')), 'PRIMARY_FAILURE_REASON', context=context)
            self.check(all(blank(p.get(k)) for k in ('QR_mean_pinball', 'F_mean_pinball', 'percent_vs_reference', 'direction_replicated', 'QR_trace_sha256', 'F_trace_sha256')), 'PRIMARY_FAILURE_NO_METRICS', context=context)
        self.counts['primary_rows'] += 1

    def run(self):
        import numpy as np  # Arrays are read only here, after explicit CLI release.

        text = (self.root / DESIGN).read_text(encoding='utf-8')
        contracts = re.findall(r'```json\s*(.*?)\s*```', text, re.S)
        if len(contracts) != 1:
            raise ValueError('Expected exactly one frozen JSON contract')
        spec = json.loads(contracts[0])
        receipt = load(self.public / 'run-receipt.json')
        if receipt.get('status') not in ('COMPLETE', 'COMPLETE_WITH_REPORTED_FAILURES'):
            raise ValueError('Refusing unfinished run: ' + str(receipt.get('status')))
        manifest = load(self.public / 'input-manifest.json')
        seal = load(self.public / 'retro-seal.json')
        self.check_provenance(spec, receipt, manifest, seal)
        archive = load(self.public / 'private-archive-manifest.json')
        self.check(archive.get('raw_or_per_issue_data_public') is False, 'PRIVATE_TRACE_PUBLICATION_POLICY')
        files = archive['files']
        manifest_paths = {str((self.root / x['path']).resolve()) for x in files}
        actual_paths = {str(x.resolve()) for x in self.private.rglob('*') if x.is_file()}
        self.check(len(manifest_paths) == len(files) and manifest_paths == actual_paths, 'PRIVATE_ARCHIVE_EXACT_INVENTORY')
        expected_seal_paths = {str((self.root / x['path']).resolve()) for x in files
            if (self.private / 'retro') in (self.root / x['path']).parents}
        expected_seal_paths.update(str((self.public / name).resolve()) for name in
            ('retro-cells.json', 'retro-summary.csv', 'retro-selection.csv', 'primary-replication.csv'))
        actual_seal_paths = {str((self.root / x['path']).resolve()) for x in seal['files']}
        self.check(len(actual_seal_paths) == len(seal['files']) and actual_seal_paths == expected_seal_paths, 'RETRO_SEAL_EXACT_INVENTORY')
        expected_groups = inventory(spec)
        expected_map = {key(g): g for g in expected_groups}
        folder_map = {group_name(g): g for g in expected_groups}
        for item in files:
            self.checked_file(item, 'private_archive')
            path = self.root / item['path']
            if path.suffix == '.npz':
                meta_path = path.with_suffix('.json')
                # Incomplete interrupted arrays have no matching score receipt.
                if 'INCOMPLETE' in path.name:
                    self.counts['incomplete_trace_files'] += 1
                    continue
                if self.check(meta_path.is_file(), 'TRACE_RECEIPT_MISSING', path=item['path']):
                    group = folder_map[path.parent.name]
                    self.check_trace(path, load(meta_path), spec, group, np)
        retro = load(self.public / 'retro-cells.json')
        inspected = load(self.public / 'inspected-cells.json')
        groups = retro['groups'] + inspected['groups']
        self.check(len(retro['groups']) == 30 and len(inspected['groups']) == 56, 'PHASE_GROUP_COUNTS')
        for phase in ('retro', 'inspected'):
            phase_groups = [g for g in groups if g['group']['phase'] == phase]
            calculation_evidence = any('raw_prefix_count' in g or g.get('selections') or
                g.get('selection_frozen_utc') or g.get('evaluation_started_utc') or
                any(r['status'] == 'COMPLETE' for r in g['rows']) for g in phase_groups)
            calculation_evidence |= any(t['group']['phase'] == phase for t in self.trace_by_segment.values())
            if not receipt.get('first_' + phase + '_calculation_utc'):
                self.check(not calculation_evidence, 'MISSING_PHASE_CALCULATION_TIMESTAMP', phase=phase)
                self.counts[phase + '_not_calculated'] += 1
        got_group_keys = [key(g['group']) for g in groups]
        self.check(len(set(got_group_keys)) == 86 and set(got_group_keys) == set(expected_map), 'EXACT_GROUP_MEMBERSHIP')
        json_rows = retro['rows'] + inspected['rows']
        grouped_rows = [r for g in groups for r in g['rows']]
        self.check(json_rows == grouped_rows, 'CELL_JSON_ROW_FLATTENING')
        self.check(len(retro['rows']) == 180 and len(inspected['rows']) == 336, 'PHASE_ROW_COUNTS')
        public_rows = rows(self.public / 'summary.csv')
        expected_row_keys = {key(g) + (report,) for g in expected_groups for report in REPORTS}
        got_row_keys = [key(r, True) for r in public_rows]
        self.check(len(public_rows) == 516 and len(set(got_row_keys)) == 516 and set(got_row_keys) == expected_row_keys, 'EXACT_516_PUBLIC_ROWS')
        json_index = {key(r, True): r for r in json_rows}
        for row in public_rows:
            self.equal_fields(row, json_index[key(row, True)], row, 'summary.csv.' + str(key(row, True)))
        retro_csv = rows(self.public / 'retro-summary.csv')
        self.check(len(retro_csv) == 180 and retro_csv == [r for r in public_rows if r['phase'] == 'retro'], 'SEALED_RETRO_CSV_UNCHANGED')
        for group in groups:
            self.check_group(group, spec, seal)
        primary_rows = rows(self.public / 'primary-replication.csv')
        primary_json = {g['primary_replication']['id']: g['primary_replication'] for g in groups if 'primary_replication' in g}
        primary_ids = {'FX-original-structure', 'Treasury-W52-structural-analogue'}
        self.check(len(primary_rows) == 2 and set(primary_json) == primary_ids and {r['id'] for r in primary_rows} == primary_ids, 'EXACT_TWO_PRIMARY_ROWS')
        for row in primary_rows:
            self.equal_fields(row, primary_json[row['id']], row, 'primary-replication.csv.' + row['id'])
        computed_assessment = independent_assessment(public_rows)
        self.compare_tree(load(self.public / 'assessment.json'), computed_assessment, 'assessment')
        selection_csv = rows(self.public / 'selection.csv')
        self.check(len(selection_csv) == 344, 'SELECTION_CSV_COUNT')
        selection_index = {(key(r), r['rule']): r for r in selection_csv}
        self.check(len(selection_index) == 344, 'SELECTION_CSV_UNIQUE')
        for result in groups:
            for rule in ('R0', 'R1', 'R2', 'R3'):
                selected = result.get('selections', {}).get(rule, {})
                expected = dict(result['group'], rule=rule,
                    status=selected.get('status', result.get('status', 'NOT_RUN')),
                    reason=selected.get('reason', result.get('reason')), selected_id=selected.get('selected_id'),
                    best_id=selected.get('best_id'), n=selected.get('n'), bandwidth=selected.get('bandwidth'),
                    selection_frozen_utc=result.get('selection_frozen_utc'),
                    r3_design_status=result.get('r3_design_status') if rule == 'R3' else None)
                actual = selection_index.get((key(result['group']), rule), {})
                self.equal_fields(actual, expected, expected, 'selection.csv.' + group_name(result['group']) + '.' + rule)
        self.check(rows(self.public / 'retro-selection.csv') == [r for r in selection_csv if r['phase'] == 'retro'], 'SEALED_RETRO_SELECTION_UNCHANGED')
        self.check(receipt['retro_rows'] == 180 and receipt['inspected_rows'] == 336, 'RUN_RECEIPT_ROW_COUNTS')
        self.check((receipt['status'] == 'COMPLETE') == all(r['status'] == 'COMPLETE' for r in public_rows), 'RUN_COMPLETION_STATUS')
        public_names = ('summary.csv', 'assessment.json', 'primary-replication.csv', 'retro-cells.json',
            'inspected-cells.json', 'run-receipt.json', 'input-manifest.json', 'private-archive-manifest.json',
            'retro-seal.json', 'retro-summary.csv', 'retro-selection.csv', 'selection.csv')
        identities = [dict(path=str((self.public / n).relative_to(self.root)), bytes=(self.public / n).stat().st_size,
            sha256=digest(self.public / n)) for n in public_names]
        return dict(status='PASS' if not self.issues else 'FAIL', verified_utc=datetime.now(timezone.utc).isoformat(),
            verifier=dict(path=Path(__file__).name, sha256=digest(Path(__file__)),
                imports_study_or_selector_or_source_code=False, forecasts_or_fits_performed=False,
                labels_constructed=False, archive_arithmetic_only=True),
            design_commit=DESIGN_COMMIT, design_sha256=DESIGN_SHA256, design_commit_timestamp=DESIGN_TIMESTAMP,
            counts=dict(self.counts), row_status_counts=dict(Counter(r['status'] for r in public_rows)),
            independent_assessment=computed_assessment, public_input_identities=identities,
            private_archive_manifest_sha256=digest(self.public / 'private-archive-manifest.json'),
            protected_archive_ledger_sha256=digest(self.root / '.scratch/r6-20261023/protected-before.json'),
            retro_seal_sha256=digest(self.public / 'retro-seal.json'),
            scope='Independent stored-array arithmetic, selection, membership, failure, provenance and chronology readback; no independent refit or reconstruction of financial labels.',
            issues=self.issues)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-completed-run', action='store_true', required=True,
        help='Explicit release: the authorised single R6 run has completed')
    args = parser.parse_args()
    if not args.verify_completed_run:
        parser.error('Completed-run release required')
    checker = Readback(ROOT)
    output = checker.public / 'verification.json'
    if output.exists():
        raise FileExistsError('Refusing to overwrite existing verification.json')
    report = checker.run()
    with output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(status=report['status'], output=str(output), issues=len(report['issues']), counts=report['counts']), ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
