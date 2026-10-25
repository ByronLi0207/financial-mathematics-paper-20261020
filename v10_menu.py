"""Six-menu adapter for frozen E1; no calibration, source I/O or study launch.

Finite reports call the inherited WP3 function unchanged. The string ``inf``
denotes the exact ordinary empirical I report. Both selectors break exact ties
toward stronger penalties; this deliberately changes the original QR4 tie rule,
while its completed-candidate policy and QR33's required-all policy remain.
"""
from __future__ import annotations

import math
from numbers import Integral, Real
from pathlib import Path

from run_v8_wp3 import (append_status, candidate_inventory, candidate_path,
    exclusive_json, maturity_summary, method_path, scalar_diagnostics,
    selection_path, utc_now)


MENU = (.001, .01, .1, 1., 10., 'inf')


def forecast_report(position, times, features, cache, origins, horizon, window,
                    refit_step, method, penalty=None, checkpoint=None):
    """Keep the WP3 signature and result shape, with exact I at ``inf``."""
    from v8_mechanism_mc import forecast_report as inherited_report
    if not (type(penalty) is str and penalty == 'inf') or method == 'F':
        return inherited_report(position, times, features, cache, origins, horizon,
            window, refit_step, method, penalty, checkpoint=checkpoint)

    import numpy as np
    from empirical_headroom import predict
    x = np.asarray(position, dtype=np.float64)
    ids = np.asarray(origins)
    t = np.asarray(times)
    if (method not in ('QR33', 'QR4') or x.ndim != 1 or not np.isfinite(x).all()
            or ids.ndim != 1 or not ids.size or ids.dtype.kind not in 'iu'
            or np.any(np.diff(ids) != 1) or ids[0] < 0
            or int(ids[-1]) + horizon >= len(x) or t.shape != x.shape
            or t.dtype.kind != 'M' or cache.horizon != horizon):
        raise ValueError('invalid complete report input')
    if checkpoint is not None:
        checkpoint(stage='refit', method=method, issue=int(ids[0]))
    ordinary = predict(x, ids, horizon, window, refit_step)
    diagnostics = []
    previous = None
    for j, raw_refit in enumerate(ordinary['refit_indices']):
        r = int(raw_refit)
        if r != previous:
            if previous is not None and checkpoint is not None:
                checkpoint(stage='refit', method=method, issue=int(ids[j]))
            diagnostics.append(dict(refit_index=r,
                training_first_origin=int(ordinary['training_first_origins'][j]),
                training_last_origin=int(ordinary['training_last_origins'][j]),
                training_count=int(window),
                latest_label_end=int(ordinary['latest_label_ends'][j])))
            previous = r
        if checkpoint is not None and (j % 24 == 0 or j == len(ids)-1):
            checkpoint(stage='issue', method=method, completed=j+1)
    return dict(origins=ordinary['origins'].copy(), capacity=ordinary['I'].copy(),
                refit_indices=ordinary['refit_indices'].copy(), fit_diagnostics=diagnostics)


predict_report = forecast_report


def select_candidate(records, method, expected_origins, menus):
    """Six candidates; exact stronger ties and inherited method-specific failure."""
    if method not in ('QR33', 'QR4'):
        raise ValueError('unsupported conditional method')
    if isinstance(expected_origins, bool) or not isinstance(expected_origins, Integral) or expected_origins < 1:
        raise ValueError('positive expected origin count required')
    menu = list(menus[method])
    records = list(records)
    if (menu != list(MENU) or len(records) != len(menu)
            or [r.get('penalty') for r in records] != menu):
        raise ValueError('candidate menu mismatch')
    complete = []
    for index, row in enumerate(records):
        if row.get('status') not in ('COMPLETE', 'FAILED', 'INCOMPLETE'):
            raise ValueError('invalid candidate status')
        if row['status'] == 'COMPLETE':
            if row.get('origin_count') != expected_origins:
                raise ValueError('incomplete candidate labelled complete')
            loss = row.get('mean_loss')
            if isinstance(loss, bool) or not isinstance(loss, Real) or not math.isfinite(loss) or loss < 0:
                raise ValueError('finite nonnegative validation loss required')
            complete.append((index, row))
    base = dict(exact_tie=False, minimum_loss_tied_candidates=0,
                tied_penalties=[], legacy_qr4_tie_changed=False)
    if not complete or method == 'QR33' and len(complete) != len(menu):
        return dict(status='INELIGIBLE', penalty=None, **base)
    index, chosen = min(complete, key=lambda item: (item[1]['mean_loss'], -item[0]))
    tied = [menu[i] for i, row in complete if row['mean_loss'] == chosen['mean_loss']]
    return dict(status='SELECTED', penalty=menu[index],
        mean_validation_loss=float(chosen['mean_loss']), exact_tie=len(tied) > 1,
        minimum_loss_tied_candidates=len(tied), tied_penalties=tied,
        legacy_qr4_tie_changed=method == 'QR4' and len(tied) > 1)


def _native(value):
    """Receipt values only: finite native JSON scalars, lists and dictionaries."""
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError('nonfinite receipt scalar')
        return value
    if isinstance(value, dict):
        return {key: _native(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_native(item) for item in value]
    item = getattr(value, 'item', None)
    if item is not None:
        scalar = item()
        if type(scalar) in (str, bool, int, float):
            return _native(scalar)
    raise ValueError('nonscalar receipt value')


def _write(path, value):
    exclusive_json(path, _native(value))


def evaluate_method(design, public, window, horizon, method, report, checkpoint,
                    fit_error, resource_errors):
    """Attempt each validation once, seal selection, evaluate its sole choice once.

    The inherited receipt names and result fields are retained. Additional tie
    fields disclose the directed original-QR4 difference; progress logs retain
    only status metadata and never contain forecast arrays.
    """
    checkpoint(stage='method_start')
    _write(method_path(public, window, horizon, method, started=True),
           dict(status='STARTED', started_utc=utc_now()))
    row = dict(status='FAILED', reason=None, selected_penalty=None, candidates=[],
               evaluation=None, fit_diagnostics=[], maturity=None)

    def expected_failure(exc):
        if isinstance(exc, fit_error):
            result = dict(reason=exc.code, failure_kind='QUANTILE_FIT_FAILURE')
            try:
                result['failure_diagnostics'] = scalar_diagnostics([dict(exc.diagnostics)])[0]
                result['failure_diagnostics_status'] = 'FINITE_SCALARS'
            except ValueError:
                result.update(failure_diagnostics=None, failure_diagnostics_status='NONFINITE_OR_NONSCALAR')
        else:
            result = dict(reason='NUMERIC_OR_STRUCTURAL_FAILURE', failure_kind=type(exc).__name__)
        if hasattr(exc, 'wp3_progress'):
            result['failure_progress'] = exc.wp3_progress
        return result

    try:
        if method != 'F':
            for index, penalty in enumerate(design['menus'][method]):
                candidate = dict(penalty=penalty, status='FAILED', origin_count=0, mean_loss=None)
                try:
                    score, diagnostics = report('validation', horizon, window, method, penalty)
                    score, diagnostics = _native(score), _native(diagnostics)
                    candidate.update(status='COMPLETE', origin_count=score['n'], mean_loss=score['mean_loss'],
                        fit_diagnostics=diagnostics, maturity=maturity_summary(diagnostics))
                except resource_errors as exc:
                    candidate.update(reason=exc.code, failure_kind='RESOURCE_INTERRUPTION')
                    _write(candidate_path(public, window, horizon, method, index), candidate)
                    raise
                except (fit_error, ValueError, FloatingPointError) as exc:
                    candidate.update(expected_failure(exc))
                except Exception as exc:
                    candidate.update(reason='TECHNICAL_ERROR', exception_type=type(exc).__name__)
                    _write(candidate_path(public, window, horizon, method, index), candidate)
                    raise
                _write(candidate_path(public, window, horizon, method, index), candidate)
                row['candidates'].append(candidate)
            expected = design['validation_last'] - design['validation_first'] + 1
            selection = select_candidate(row['candidates'], method, expected, design['menus'])
            _write(selection_path(public, window, horizon, method), selection)
            for key in ('exact_tie', 'minimum_loss_tied_candidates', 'tied_penalties', 'legacy_qr4_tie_changed'):
                row[key] = selection[key]
            if selection['status'] != 'SELECTED':
                row['reason'] = 'VALIDATION_INELIGIBLE'
            else:
                row['selected_penalty'] = selection['penalty']
        if method == 'F' or row['selected_penalty'] is not None:
            score, diagnostics = report('evaluation', horizon, window, method, row['selected_penalty'])
            score, diagnostics = _native(score), _native(diagnostics)
            row.update(status='COMPLETE', evaluation=score, fit_diagnostics=diagnostics,
                       maturity=maturity_summary(diagnostics))
    except resource_errors as exc:
        row.update(reason=exc.code, candidates=candidate_inventory(design, public, window, horizon, method))
        _write(method_path(public, window, horizon, method), row)
        raise
    except (fit_error, ValueError, FloatingPointError) as exc:
        row.update(expected_failure(exc))
    except Exception as exc:
        row.update(reason='TECHNICAL_ERROR', exception_type=type(exc).__name__,
                   candidates=candidate_inventory(design, public, window, horizon, method))
        _write(method_path(public, window, horizon, method), row)
        raise
    row = _native(row)
    _write(method_path(public, window, horizon, method), row)
    append_status(Path(public)/'progress.jsonl', event='method_end', window=int(window),
        horizon=int(horizon), method=method, status=row['status'], reason=row['reason'])
    return row
