"""E6: reconcile the I reference and report a fixed descriptive ridge path.

The original E3 menu, selections, estimators and archives are read-only.
New per-issue arrays and detailed fit receipts remain in the private scratch
folder. Public outputs contain aggregate results, statuses and identities.
"""
from __future__ import annotations

import os
import sys
sys.dont_write_bytecode = True
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import resource
import signal
import subprocess
import time

import numpy as np
import empirical_headroom
import supervisor_e3 as e3
from conditional_quantile import QuantileFitError
from conditional_study import (StudyConfig, conditional_forecast,
                               score_predictions, summarize_scores)
from run_rank_ablation import compare_reference, reference_index
from run_study import StudyStop, parse_thread_snapshot
from study_core import build_label_cache

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT/'results/supervisor-20261023/e6'
PRIVATE = ROOT/'.scratch/supervisor-round2-20261023/e6'
RANK = ROOT/'results/revision-20261022/rank-ablation'
PRIMARIES = (('fx_hourly', 6, 2880), ('nyfed_weekly', 6, 260))
PATH_PENALTIES = (.001, .01, .1, 1., 10., 100.)
INTERNAL_SECONDS = 3540.
HARD_SECONDS = 3600.
CODE_FILES = ('supervisor_round2_e6.py', 'supervisor_e3.py',
              'empirical_headroom.py', 'run_rank_ablation.py',
              'conditional_study.py', 'conditional_features.py',
              'conditional_quantile.py', 'conditional_sources.py', 'study_core.py')
ESTIMATOR_FILES = ('conditional_study.py', 'conditional_features.py',
                   'conditional_quantile.py', 'conditional_sources.py', 'study_core.py')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value, *, exclusive=False):
    with Path(path).open('x' if exclusive else 'w') as stream:
        json.dump(value, stream, indent=2, allow_nan=False, default=dict)
        stream.write('\n')


def csv_rows(path):
    with Path(path).open(newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    Path(path).write_text(stream.getvalue())


def validate_diagnostics(details, horizon, window):
    """Check existing acceptance criteria; do not alter or refit a report."""
    if not details:
        raise ValueError('EMPTY_FIT_DIAGNOSTICS')
    for fit in details:
        if (not 1 <= fit['iterations'] <= 10000
                or fit['training_count'] != window
                or fit['latest_label_end'] != fit['training_last_origin']+horizon
                or fit['latest_label_end'] > fit['refit_index']
                or fit['dual_integer_sum'] != 0):
            raise ValueError('UNACCEPTED_FIT_OR_IMMATURE_TRAINING_LABEL')
        for value, tolerance in [('primal_residual', 'primal_tolerance'),
                                 ('dual_residual', 'dual_tolerance'),
                                 ('duality_gap', 'gap_tolerance')]:
            if (not math.isfinite(fit[value]) or not math.isfinite(fit[tolerance])
                    or fit[value] < 0 or fit[tolerance] <= 0
                    or fit[value] > fit[tolerance]):
                raise ValueError('UNACCEPTED_FIT_CERTIFICATE')
    return dict(fit_count=len(details),
        maximum_iterations=max(f['iterations'] for f in details),
        maximum_primal_residual_fraction=max(f['primal_residual']/f['primal_tolerance'] for f in details),
        maximum_dual_residual_fraction=max(f['dual_residual']/f['dual_tolerance'] for f in details),
        maximum_gap_fraction=max(f['duality_gap']/f['gap_tolerance'] for f in details),
        all_training_labels_mature=True, all_fits_accepted=True)


def path_inventory():
    return [dict(source=s, horizon=h, window=w, phase=phase, parameter=lam,
                 status='INCOMPLETE', post_result_exploratory=True,
                 descriptive_only=True, new_selection_performed=False)
            for s, h, w in PRIMARIES for phase in ('validation', 'evaluation')
            for lam in PATH_PENALTIES]


def protected_manifest():
    files = [p for folder in (e3.PUBLIC, e3.PRIVATE, RANK)
             for p in folder.rglob('*') if p.is_file()]
    files += [ROOT/name for name in ESTIMATOR_FILES]
    files += [ROOT/'protocol/revision-20261022/study-spec.json']
    files += [ROOT/'results/revision-20261022/evaluation-summary.csv']
    return {str(path.relative_to(ROOT)): sha(path) for path in sorted(files)}


class Guard:
    """One whole-run deadline and the original resource observation policy."""
    def __init__(self):
        self.start = time.monotonic()
        self.last_write = -math.inf
        self.resources = dict(started_utc=now(), elapsed_seconds=0., peak_rss_bytes=0,
            requested_numerical_threads=1, maximum_observed_os_threads=0,
            thread_snapshot_count=0, thread_probe_status='UNVERIFIED',
            internal_wall_seconds=INTERNAL_SECONDS, hard_wall_seconds=HARD_SECONDS,
            internal_rss_bytes=1610612736, public_rss_bytes=2147483648,
            resources_are_snapshot_observations=True)

    def __call__(self, **progress):
        elapsed = time.monotonic()-self.start
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if platform.system() != 'Darwin':
            rss *= 1024
        probe = subprocess.run(['/bin/ps', '-M', '-p', str(os.getpid()), '-o', 'pid='],
                               capture_output=True, text=True, check=True, timeout=5)
        threads = parse_thread_snapshot(probe.stdout, os.getpid())
        self.resources.update(elapsed_seconds=elapsed,
            peak_rss_bytes=max(rss, self.resources['peak_rss_bytes']),
            maximum_observed_os_threads=max(threads, self.resources['maximum_observed_os_threads']),
            thread_snapshot_count=self.resources['thread_snapshot_count']+1,
            thread_probe_status='PASS', checkpoint_utc=now(), **progress)
        if elapsed-self.last_write >= 5:
            dump(PUBLIC/'progress.json', self.resources)
            self.last_write = elapsed
        if threads > 2:
            raise StudyStop('RESOURCE_THREADS')
        if rss >= 1610612736:
            raise StudyStop('RESOURCE_RSS')
        if elapsed >= INTERNAL_SECONDS:
            raise StudyStop('RESOURCE_WALL')


def private_reference(identity, phase, origins, peak, prediction, scores):
    path = PRIVATE/f'{identity}-{phase}-I-F.npz'
    np.savez(path, origins=origins, peak=peak, floor=prediction['floors'],
        I=prediction['I'], F=prediction['F'], I_pinball=scores['I'].pinball,
        F_pinball=scores['F'].pinball, refit_indices=prediction['refit_indices'])
    os.chmod(path, 0o600)
    return sha(path)


def reference_reports(data, cache, origins, horizon, window, step):
    prediction = empirical_headroom.predict(data.position, origins, horizon, window, step)
    if (not np.array_equal(prediction['origins'], origins)
            or np.any(prediction['latest_label_ends'] > prediction['refit_indices'])
            or np.any(prediction['refit_indices'] > origins)):
        raise ValueError('REFERENCE_POOL_ORIGIN_CONTRACT')
    scores = {m: score_predictions(cache.peak[origins], prediction[m], prediction['floors'], origins)
              for m in ('I', 'F')}
    return prediction, scores, {m: summarize_scores(scores[m]) for m in ('I', 'F')}


def prepare_table(spec, guard):
    rank_rows = reference_index(csv_rows(RANK/'summary.csv'))
    e3_rows = {(r['source'], int(r['horizon']), int(r['window'])): r
               for r in csv_rows(e3.PUBLIC/'summary.csv')}
    original_rows = reference_index(csv_rows(ROOT/'results/revision-20261022/evaluation-summary.csv'))
    table, receipts, contexts = [], [], {}
    loaded = {}
    for source, horizon, window in e3.CELLS:
        identity = e3.cell_id(source, horizon, window)
        base = dict(source=source, horizon=horizon, window=window,
                    status='INCOMPLETE', post_result_exploratory=True)
        try:
            cfg = spec['sources'][source]
            if source not in loaded:
                loaded[source] = e3.source(source, spec)
            data = loaded[source]
            if len(data.position) != cfg['record_count']:
                raise ValueError('SOURCE_RECORD_COUNT')
            cache = build_label_cache(data.position, horizon)
            origins = np.arange(cfg['evaluation_origin_first'], cfg['evaluation_origin_last']+1, dtype=np.int64)
            pred, scores, metrics = reference_reports(data, cache, origins, horizon, window, cfg['refit_step'])
            for method in ('I', 'F'):
                compare_reference(metrics[method], rank_rows[source, horizon, window, method])
            old = e3_rows[source, horizon, window]
            record_path = e3.PUBLIC/identity/'result.json'
            selection_path = e3.PUBLIC/identity/'selection-before-evaluation.json'
            record = json.loads(record_path.read_text())
            selection = json.loads(selection_path.read_text())
            if (record['status'] != 'COMPLETE' or selection['selection']['status'] != 'SELECTED'
                    or record['selected_penalty'] != selection['selection']['parameter']
                    or record['penalties'] != list(e3.PENALTIES)):
                raise ValueError('E3_SELECTION_RECEIPT')
            for name in ESTIMATOR_FILES:
                if sha(ROOT/name) != record['code_hashes'][name]:
                    raise ValueError('UNCHANGED_ESTIMATOR_IDENTITY')
            trace_path = e3.PRIVATE/identity/'numeric-traces.npz'
            if sha(trace_path) != record['private_evaluation_trace_sha256']:
                raise ValueError('E3_TRACE_HASH')
            trace = e3.checked_trace(trace_path, origins, cache.peak[origins], record['evaluation']['mean_pinball'])
            new_scores = score_predictions(trace['peak'], trace['capacity'], pred['floors'], origins)
            new_metrics = summarize_scores(new_scores)
            if new_metrics != record['evaluation']:
                raise ValueError('E3_SCORE_RECONCILIATION')
            fit_summary = validate_diagnostics(record['fit_diagnostics'], horizon, window)
            original = original_rows[source, horizon, window, 'QR']
            if (float(old['original33_mean_pinball']) != float(original['mean_pinball'])
                    or int(old['original33_breaches']) != int(original['strict_breach_count'])
                    or float(old['frozen_F_mean_pinball']) != metrics['F']['mean_pinball']
                    or float(old['extended33_mean_pinball']) != new_metrics['mean_pinball']
                    or int(old['extended33_breaches']) != new_metrics['strict_breach_count']):
                raise ValueError('E3_AGGREGATE_RECONCILIATION')
            lower, upper = empirical_headroom.ranks(window)
            base.update(status='COMPLETE', native_unit=cfg['native_unit'], origin_count=len(origins),
                extended33_selected_penalty=record['selected_penalty'],
                selected_at_extended_menu_upper_endpoint=record['selected_penalty'] == max(e3.PENALTIES),
                original33_mean_pinball=float(old['original33_mean_pinball']),
                original33_percent_vs_frozen_F=float(old['original33_percent_vs_frozen_F']),
                four_mean_pinball=float(old['four_mean_pinball']),
                four_percent_vs_frozen_F=float(old['four_percent_vs_frozen_F']),
                extended33_mean_pinball=new_metrics['mean_pinball'],
                extended33_percent_vs_frozen_F=float(old['extended33_percent_vs_frozen_F']),
                I_mean_pinball=metrics['I']['mean_pinball'],
                I_percent_vs_frozen_F=100*(metrics['I']['mean_pinball']-metrics['F']['mean_pinball'])/metrics['F']['mean_pinball'],
                I_breaches=metrics['I']['strict_breach_count'],
                extended33_breaches=new_metrics['strict_breach_count'],
                frozen_F_mean_pinball=metrics['F']['mean_pinball'],
                frozen_F_breaches=metrics['F']['strict_breach_count'],
                original33_breaches=int(old['original33_breaches']),
                rank_I=lower, rank_F=upper,
                empirical_minimizer_interval_has_I_F_endpoints=(19*window)%20 == 0)
            receipts.append(dict(source=source, horizon=horizon, window=window,
                rank_summary_metrics_exact=True, e3_evaluation_metrics_exact=True,
                selection_frozen_before_evaluation=True, unchanged_estimator_hashes=True,
                E3_result_sha256=sha(record_path), E3_selection_sha256=sha(selection_path),
                E3_trace_sha256=sha(trace_path), fit_summary=fit_summary,
                new_private_reference_sha256=private_reference(identity, 'evaluation', origins,
                    cache.peak[origins], pred, scores)))
            if (source, horizon, window) in PRIMARIES:
                contexts[source, horizon, window] = (data, cache, record, metrics)
            guard(stage='table_cell_verified', cell_id=identity)
        except (ValueError, OSError, KeyError) as error:
            base.update(status='FAILED', reason=str(error))
        table.append(base)
        write_csv(PUBLIC/'table6.csv', table)
    return table, receipts, contexts


def path_report(row, context, cfg, guard):
    source, horizon, window = row['source'], row['horizon'], row['window']
    phase, lam = row['phase'], row['parameter']
    identity = e3.cell_id(source, horizon, window)
    data, cache, record, _ = context
    origins = np.arange(cfg[phase+'_origin_first'], cfg[phase+'_origin_last']+1, dtype=np.int64)
    started = time.monotonic()
    try:
        if phase == 'validation' and lam in e3.PENALTIES:
            receipt = next(r for r in record['candidates'] if r['parameter'] == lam)
            if receipt['status'] != 'COMPLETE' or receipt['origin_count'] != len(origins):
                raise ValueError('ARCHIVED_VALIDATION_INCOMPLETE')
            path = e3.PRIVATE/identity/f'validation-lambda-{lam:g}.npz'
            trace = e3.checked_trace(path, origins, cache.peak[origins], receipt['mean_pinball'])
            details = receipt['fit_diagnostics']
            provenance = 'VERIFIED_E3_VALIDATION_REUSE'
        elif phase == 'evaluation' and lam == record['selected_penalty']:
            path = e3.PRIVATE/identity/'numeric-traces.npz'
            trace = e3.checked_trace(path, origins, cache.peak[origins], record['evaluation']['mean_pinball'])
            details = record['fit_diagnostics']
            provenance = 'VERIFIED_E3_SELECTED_EVALUATION_REUSE'
        else:
            config = StudyConfig(horizon, window, cfg['refit_step'], cfg['short_scale'],
                                 cfg['long_scale'], cfg['nominal_gap_seconds'])
            forecast = conditional_forecast(data.position, data.dates, origins, config, 'QR', lam, checkpoint=guard)
            scores = score_predictions(cache.peak[origins], forecast.capacities, forecast.floors, origins)
            path = PRIVATE/f'{identity}-{phase}-lambda-{lam:g}.npz'
            e3.save_forecast(path, forecast, cache.peak[origins], scores)
            trace = dict(capacity=forecast.capacities, peak=cache.peak[origins])
            details = forecast.fit_diagnostics
            dump(PRIVATE/f'{identity}-{phase}-lambda-{lam:g}-fit-diagnostics.json', details, exclusive=True)
            provenance = 'NEW_FIXED_PARAMETER_REPORT'
        fit_summary = validate_diagnostics(details, horizon, window)
        summary = summarize_scores(score_predictions(trace['peak'], trace['capacity'],
                                   np.abs(data.position[origins]), origins))
        row.update(status='COMPLETE', provenance=provenance, **summary,
            fit_count=fit_summary['fit_count'], maximum_iterations=fit_summary['maximum_iterations'],
            maximum_primal_residual_fraction=fit_summary['maximum_primal_residual_fraction'],
            maximum_dual_residual_fraction=fit_summary['maximum_dual_residual_fraction'],
            maximum_gap_fraction=fit_summary['maximum_gap_fraction'],
            private_trace_sha256=sha(path), E3_selected_penalty_unchanged=record['selected_penalty'])
    except QuantileFitError as error:
        row.update(status='FAILED', reason=error.code, solver_diagnostics=dict(error.diagnostics),
                   provenance='NEW_FIXED_PARAMETER_REPORT')
        dump(PRIVATE/f'{identity}-{phase}-lambda-{lam:g}-failure.json',
             dict(reason=error.code, solver_diagnostics=error.diagnostics,
                  failure_context=getattr(error, 'failure_context', None)), exclusive=True)
        partial = getattr(error, 'partial_forecast', None)
        if partial is not None and len(partial.origins):
            partial_scores = score_predictions(cache.peak[partial.origins], partial.capacities,
                                              partial.floors, partial.origins)
            e3.save_forecast(PRIVATE/f'{identity}-{phase}-lambda-{lam:g}-INCOMPLETE.npz',
                             partial, cache.peak[partial.origins], partial_scores)
    except (ValueError, OSError, KeyError) as error:
        row.update(status='FAILED', reason=str(error))
    finally:
        row['elapsed_seconds'] = time.monotonic()-started
    guard(stage='path_report_finished', cell_id=identity, phase=phase, parameter=lam)
    print(json.dumps({k:row[k] for k in ('source', 'horizon', 'window', 'phase', 'parameter', 'status')}), flush=True)


def execute():
    PUBLIC.mkdir(parents=True, exist_ok=False)
    PRIVATE.mkdir(parents=True, exist_ok=False, mode=0o700)
    os.chmod(PRIVATE, 0o700)
    guard = Guard()
    protected = protected_manifest()
    spec_path = ROOT/'protocol/revision-20261022/study-spec.json'
    spec = json.loads(spec_path.read_text())
    paths = path_inventory()
    table, receipts, references = [], [], []
    result = dict(status='STARTED', started_utc=now(), post_result_exploratory=True,
        descriptive_only_path=True, new_selection_performed=False,
        E3_penalty_menu_unchanged=list(e3.PENALTIES), descriptive_penalties=list(PATH_PENALTIES),
        sources={s:dict(sha256=c['sha256'], bytes=c['bytes'], record_count=c['record_count'])
                 for s, c in spec['sources'].items()},
        code_sha256={name:sha(ROOT/name) for name in CODE_FILES}, spec_sha256=sha(spec_path))
    dump(PUBLIC/'archive-identities-before.json', protected, exclusive=True)
    dump(PUBLIC/'path-design-before-run.json', dict(frozen_utc=now(),
        primaries=PRIMARIES, penalties=PATH_PENALTIES, phases=['validation', 'evaluation'],
        interpretation='post-result exploratory descriptive path; no new selection; lambda100 is not added to E3 menu',
        all_24_reports=paths, no_retry=True, hard_whole_run_seconds=HARD_SECONDS,
        numerical_threads=1, maximum_observed_os_threads=2, public_rss_bytes=2147483648), exclusive=True)
    old_handler = signal.getsignal(signal.SIGALRM)
    def timeout(*_):
        raise StudyStop('RESOURCE_HARD_WALL')
    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, HARD_SECONDS)
    try:
        guard(stage='initial')
        table, receipts, contexts = prepare_table(spec, guard)
        if len(table) != 8 or any(r['status'] != 'COMPLETE' for r in table):
            raise ValueError('TABLE_CELL_FAILURE')
        dump(PUBLIC/'table-verification.json', dict(status='PASS', cells=receipts), exclusive=True)
        for source, horizon, window in PRIMARIES:
            data, cache, record, evaluation_metrics = contexts[source, horizon, window]
            cfg = spec['sources'][source]
            identity = e3.cell_id(source, horizon, window)
            for phase in ('validation', 'evaluation'):
                origins = np.arange(cfg[phase+'_origin_first'], cfg[phase+'_origin_last']+1, dtype=np.int64)
                pred, scores, metrics = reference_reports(data, cache, origins, horizon, window, cfg['refit_step'])
                if phase == 'evaluation' and metrics != evaluation_metrics:
                    raise ValueError('I_REFERENCE_RECONCILIATION')
                references.append(dict(source=source, horizon=horizon, window=window, phase=phase,
                    status='COMPLETE', method='I', post_result_exploratory=True,
                    **metrics['I'], frozen_F_mean_pinball=metrics['F']['mean_pinball'],
                    private_trace_sha256=private_reference(identity, 'path-'+phase, origins,
                        cache.peak[origins], pred, scores)))
        write_csv(PUBLIC/'lambda-path-I.csv', references)
        for row in paths:
            path_report(row, contexts[row['source'], row['horizon'], row['window']],
                        spec['sources'][row['source']], guard)
            write_csv(PUBLIC/'lambda-path.csv', paths)
            dump(PUBLIC/'path-reports.json', paths)
        guard(stage='terminal')
        result['status'] = 'COMPLETE' if all(r['status'] == 'COMPLETE' for r in paths) else 'COMPLETE_WITH_PATH_FAILURES'
    except (StudyStop, subprocess.SubprocessError, ValueError, OSError, KeyError) as error:
        result.update(status='INCOMPLETE', reason=getattr(error, 'code', str(error)))
        for row in paths:
            if row['status'] == 'INCOMPLETE':
                row['reason'] = 'STOPPED_BEFORE_COMPLETE_REPORT'
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
        after = protected_manifest()
        unchanged = after == protected
        if not unchanged:
            result.update(status='FAILED_ARCHIVE_IDENTITY', reason='PROTECTED_FILE_CHANGED')
        write_csv(PUBLIC/'lambda-path.csv', paths)
        dump(PUBLIC/'path-reports.json', paths)
        if references:
            write_csv(PUBLIC/'lambda-path-I.csv', references)
        result.update(finished_utc=now(), table_cells=table, reference_rows=references,
            path_report_count=len(paths), complete_path_reports=sum(r['status']=='COMPLETE' for r in paths),
            failed_path_reports=sum(r['status']=='FAILED' for r in paths),
            incomplete_path_reports=sum(r['status']=='INCOMPLETE' for r in paths),
            reused_path_reports=sum(str(r.get('provenance', '')).startswith('VERIFIED_E3') for r in paths),
            new_path_reports=sum(r.get('provenance')=='NEW_FIXED_PARAMETER_REPORT' for r in paths),
            table_complete_cells=sum(r['status']=='COMPLETE' for r in table),
            protected_archive_files_unchanged=unchanged, protected_file_count=len(protected),
            resources=dict(guard.resources, final_elapsed_seconds=time.monotonic()-guard.start))
        dump(PUBLIC/'aggregate.json', result)
        dump(PUBLIC/'verification.json', dict(status='PASS' if unchanged and result['status']=='COMPLETE' else 'ATTENTION',
            protected_archive_files_unchanged=unchanged, protected_file_count=len(protected),
            table_expected_rows=8, table_complete_rows=result['table_complete_cells'],
            path_expected_rows=24, path_complete_rows=result['complete_path_reports'],
            reference_expected_rows=4, reference_rows=len(references),
            no_new_selection=True, E3_menu_unchanged=True, new_solver_or_tolerance=False,
            independent_data_validation=False))
        dump(PUBLIC/'environment.json', dict(python_version=sys.version, python_executable=sys.executable,
            numpy_version=np.__version__, platform=platform.platform(),
            code_sha256=result['code_sha256'], policy='existing runtime; no installation or downloads'))
    print(json.dumps(dict(status=result['status'], table_complete_cells=result['table_complete_cells'],
        complete_path_reports=result['complete_path_reports'], resources=result['resources'])), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', help='create a new, non-overwriting E6 attempt')
    args = parser.parse_args()
    if not args.run:
        parser.error('explicit --run is required')
    outcome = execute()
    raise SystemExit(0 if outcome['status'] == 'COMPLETE' else 1)
