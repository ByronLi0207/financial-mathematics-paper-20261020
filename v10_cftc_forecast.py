"""Caller-owned CFTC-array forecasting; no acquisition or import-time study.

Six fixed procedures share cached, once-attempted base segments. The delayed
ACI wrapper reuses saved selected validation/evaluation bases and adds only its
declared warm segment. Every complete method is persisted before proceeding.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from conditional_features import build_features
from conditional_quantile import QuantileFitError
from conditional_study import score_predictions
from empirical_headroom import predict as empirical_predict
from run_study import StudyStop
from run_v8_wp3 import DriverStop, exclusive_json, scalar_diagnostics
from study_core import build_label_cache, stable_mean
import v6_aci as aci
from v10_menu import _native, evaluate_method, forecast_report


METHODS = ('F', 'I', 'QR4', 'QR33', 'ACI_F', 'ACI_QR33')
RESOURCE_ERRORS = (StudyStop, DriverStop)


def _write(path, value):
    exclusive_json(path, _native(value))


def _reason(exc):
    return str(getattr(exc, 'code', str(exc) or type(exc).__name__))


def _empty(method, reason=None, status='FAILED', penalty=None):
    return dict(method=method, status=status, selected_penalty=penalty,
                selected_gamma=None, mean_loss=None, strict_breach_count=None,
                n=None, reason=reason)


def forecast_cell(position, times, design, window, output, checkpoint=None):
    """Run one contract/window on supplied arrays and persist each method once.

    Production counts come from the frozen design (52/260). Smaller counts in
    constructed test designs do not change the production design or its files.
    ``output`` must not exist. Returned traces contain only complete methods.
    """
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    checkpoint = checkpoint or (lambda **detail: None)
    x = np.asarray(position, dtype=float)
    clock = np.asarray(times)
    h, w, step = int(design['horizon']), int(window), int(design['refit_step'])
    vn = int(design['split_formulas']['validation_n'])
    en = int(design['split_formulas']['evaluation_n'])
    if tuple(design['methods']) != METHODS or tuple(design['ancillary']['gammas']) != aci.GAMMAS:
        raise ValueError('METHOD_OR_GAMMA_DESIGN_MISMATCH')
    if x.ndim != 1 or not np.isfinite(x).all() or clock.shape != x.shape or min(h, w, step, vn, en) < 1:
        raise ValueError('INVALID_CELL_INPUT')
    evaluation_first = len(x)-h-en
    validation_last = evaluation_first-h-1
    validation_first = validation_last-vn+1
    if validation_first < 0:
        raise ValueError('INSUFFICIENT_SPLIT_HISTORY')
    validation = np.arange(validation_first, validation_last+1, dtype=np.int64)
    evaluation = np.arange(evaluation_first, len(x)-h, dtype=np.int64)
    features = build_features(x, clock, short_scale=design['feature_rms_short'],
        long_scale=design['feature_rms_long'], nominal_gap_seconds=design['nominal_gap_seconds'])
    labels = build_label_cache(x, h)
    local_design = dict(design, validation_first=validation_first, validation_last=validation_last)
    _write(output/'splits.json', dict(N=len(x), horizon=h, window=w, refit_step=step,
        validation_first=validation_first, validation_last=validation_last, validation_n=vn,
        evaluation_first=evaluation_first, evaluation_last=int(evaluation[-1]), evaluation_n=en,
        unissued_gap_n=evaluation_first-validation_last-1,
        validation_clock_first=str(clock[validation_first]), validation_clock_last=str(clock[validation_last]),
        evaluation_clock_first=str(clock[evaluation_first]), evaluation_clock_last=str(clock[evaluation[-1]])))
    attempted = {}
    validation_traces = {}
    methods, traces, base_rows = [], {}, {}

    def trace(ids, capacities):
        ids = np.asarray(ids, dtype=np.int64)
        score = score_predictions(labels.peak[ids], capacities, np.abs(x[ids]), ids)
        return dict(origins=ids.copy(), capacities=score.capacities.copy(),
            peak=labels.peak[ids].copy(), floor=score.floors.copy(), pinball=score.pinball.copy(),
            strict_breach=score.strict_breach.copy(), overrun=score.overrun.copy(), unused=score.unused.copy())

    def summary(t):
        return dict(mean_loss=stable_mean(t['pinball']), n=int(len(t['origins'])),
            strict_breach_count=int(np.count_nonzero(t['strict_breach'])),
            strict_breach_rate=float(np.mean(t['strict_breach'])))

    def publish(row, t=None):
        if row['status'] == 'COMPLETE':
            if t is None or len(t['origins']) != en or not np.array_equal(t['origins'], evaluation):
                raise ValueError('INCOMPLETE_METHOD_TRACE')
            path = output/f"trace-{row['method']}.npz"
            with path.open('xb') as stream:
                np.savez_compressed(stream, **t)
            row = dict(row, trace_path=path.name, trace_bytes=path.stat().st_size,
                trace_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            traces[row['method']] = t
        row = _native(row)
        _write(output/f"result-{row['method']}.json", row)
        methods.append(row)
        base_rows[row['method']] = row
        return row

    def historical_diagnostics(p):
        ids = p['refit_indices']
        return [dict(refit_index=int(r), training_first_origin=int(p['training_first_origins'][j]),
            training_last_origin=int(p['training_last_origins'][j]), training_count=w,
            latest_label_end=int(p['latest_label_ends'][j])) for j, r in enumerate(ids)
            if j == 0 or r != ids[j-1]]

    def base_segment(ids, method, penalty=None):
        # These caller-created segments are consecutive. Cache failed attempts
        # too, including the F/I reports produced by one empirical call.
        suffix = (int(ids[0]), int(ids[-1]), w, step)
        key = (method, penalty, *suffix)
        if key in attempted:
            value = attempted[key]
            if isinstance(value, Exception):
                raise value
            return value
        checkpoint(stage='cftc_base_segment', method=method)
        try:
            if method in ('F', 'I'):
                p = empirical_predict(x, ids, h, w, step)
                diagnostics = historical_diagnostics(p)
                for family in ('F', 'I'):
                    attempted[(family, None, *suffix)] = dict(origins=p['origins'], capacity=p[family],
                        refit_indices=p['refit_indices'], fit_diagnostics=diagnostics)
            else:
                attempted[key] = forecast_report(x, clock, features, labels, ids, h, w, step,
                                                 method, penalty, checkpoint=checkpoint)
            value = attempted[key]
            if not np.array_equal(value['origins'], ids):
                raise ValueError('BASE_SEGMENT_ORIGIN_MISMATCH')
            return value
        except Exception as exc:
            attempted[key] = exc
            if method in ('F', 'I'):
                for family in ('F', 'I'):
                    attempted[(family, None, *suffix)] = exc
            raise

    def report(segment, horizon, report_window, method, penalty=None):
        if horizon != h or report_window != w:
            raise ValueError('REPORT_GEOMETRY_MISMATCH')
        ids = validation if segment == 'validation' else evaluation
        result = base_segment(ids, method, penalty)
        t = trace(ids, result['capacity'])
        if segment == 'validation':
            validation_traces[(method, penalty)] = t
        return summary(t), scalar_diagnostics(result['fit_diagnostics'])

    for method in METHODS[:4]:
        checkpoint(stage='cftc_method_start', method=method)
        if method in ('F', 'I'):
            row = _empty(method)
            try:
                result = base_segment(evaluation, method)
                t = trace(evaluation, result['capacity'])
                row.update(status='COMPLETE', **summary(t))
                row['reason'] = None
                row = publish(row, t)
            except RESOURCE_ERRORS:
                raise
            except Exception as exc:
                row = publish(_empty(method, _reason(exc)))
            _write(output/f'W{w}_H{h}_{method}.json', row)
        else:
            receipt = evaluate_method(local_design, output, w, h, method, report, checkpoint,
                                      QuantileFitError, RESOURCE_ERRORS)
            row = _empty(method, receipt.get('reason'), penalty=receipt.get('selected_penalty'))
            row.update(exact_tie=receipt.get('exact_tie', False),
                legacy_qr4_tie_changed=receipt.get('legacy_qr4_tie_changed', False))
            if receipt['status'] == 'COMPLETE':
                row.update(status='COMPLETE', **receipt['evaluation'])
                selected = base_segment(evaluation, method, row['selected_penalty'])
                publish(row, trace(evaluation, selected['capacity']))
            else:
                publish(row)

    def ancillary(method, base_method):
        penalty = base_rows[base_method]['selected_penalty']
        row = _empty(method, penalty=penalty)
        row.update(candidates=[], validation_prefix_identical=False, grid=None)
        try:
            if base_rows[base_method]['status'] != 'COMPLETE':
                row.update(status='NA', reason='BASE_'+base_method+'_UNAVAILABLE')
            else:
                grid = aci.initialization_grid(validation_first, h, w, step,
                    features.valid_from if base_method == 'QR33' else 0)
                row['grid'] = grid
                if grid['mature_initial_count'] < 19:
                    row.update(status='NA', reason='INSUFFICIENT_PREVALIDATION_CALIBRATION')
                else:
                    warm = np.arange(grid['pre_first'], validation_first, dtype=np.int64)
                    warm_report = base_segment(warm, base_method, penalty)
                    saved_validation = validation_traces.get((base_method, penalty))
                    if saved_validation is None:
                        validation_report = base_segment(validation, base_method, penalty)
                        saved_validation = trace(validation, validation_report['capacity'])
                    arrays = dict(origins=validation, base=saved_validation['capacities'],
                        peak=saved_validation['peak'], floor=saved_validation['floor'],
                        warm_origins=warm, warm_base=warm_report['capacity'], warm_peak=labels.peak[warm])
                    saved = {}
                    for index, gamma in enumerate(aci.GAMMAS):
                        candidate = dict(gamma=gamma, status='FAILED', origin_count=None,
                                         hits=None, mean_loss=None)
                        try:
                            result = aci.aci_stream(**arrays, horizon=h, window=w, gamma=gamma,
                                                    minimum_calibration=19, checkpoint=checkpoint)
                            t = trace(validation, result['capacities'])
                            s = summary(t)
                            candidate.update(status='COMPLETE', origin_count=s['n'],
                                hits=s['strict_breach_count'], mean_loss=s['mean_loss'],
                                initial_calibration_count=result['initial_calibration_count'])
                            saved[gamma] = result
                        except RESOURCE_ERRORS as exc:
                            candidate.update(reason=exc.code)
                            _write(output/f'W{w}_H{h}_{method}_validation-{index}.json', candidate)
                            raise
                        except Exception as exc:
                            candidate.update(reason=_reason(exc))
                        row['candidates'].append(candidate)
                        _write(output/f'W{w}_H{h}_{method}_validation-{index}.json', candidate)
                    selection = aci.select_gamma(row['candidates'], expected_count=vn)
                    _write(output/f'W{w}_H{h}_{method}.selection.json', selection)
                    row['selection'] = selection
                    if selection['status'] != 'SELECTED':
                        row.update(status='NA', reason='NO_ELIGIBLE_GAMMA')
                    else:
                        gamma = selection['gamma']
                        row['selected_gamma'] = gamma
                        original_evaluation = traces[base_method]
                        combined = dict(arrays)
                        for name, tail in [('origins', evaluation), ('base', original_evaluation['capacities']),
                                           ('peak', original_evaluation['peak']), ('floor', original_evaluation['floor'])]:
                            combined[name] = np.concatenate((arrays[name], tail))
                        result = aci.aci_stream(**combined, horizon=h, window=w, gamma=gamma,
                                                minimum_calibration=19, checkpoint=checkpoint)
                        if not np.array_equal(result['capacities'][:vn], saved[gamma]['capacities']):
                            raise ValueError('VALIDATION_PREFIX_CHANGED')
                        row['validation_prefix_identical'] = True
                        t = trace(evaluation, result['capacities'][vn:])
                        row.update(status='COMPLETE', reason=None, **summary(t),
                            initial_calibration_count=int(result['initial_calibration_count']),
                            feedback_consumed=int(result['feedback_consumed']),
                            alpha_min=float(np.min(result['alpha'][vn:])),
                            alpha_max=float(np.max(result['alpha'][vn:])),
                            clip_count=int(np.sum(result['clip_counts'][vn:])))
                        publish(row, t)
                        _write(output/f'W{w}_H{h}_{method}.json', row)
                        return
        except RESOURCE_ERRORS:
            raise
        except Exception as exc:
            row.update(status='FAILED', reason=_reason(exc))
        publish(row)
        _write(output/f'W{w}_H{h}_{method}.json', row)

    for method, base_method in [('ACI_F', 'F'), ('ACI_QR33', 'QR33')]:
        checkpoint(stage='cftc_method_start', method=method)
        ancillary(method, base_method)
    return dict(methods=methods, traces=traces)
