"""Frozen WP3 level-AR/GARCH mechanism primitives, with no import-time I/O.

Only F, original QR33 and original-menu QR4 are calculated. Original research
modules remain unchanged. The executable study driver seals this file before
generating the fixed study repetitions; tests use separate constructed inputs.
"""
import copy
import math
import numbers
import statistics

import numpy as np

from conditional_features import (completed_training_indices,
    fit_feature_transform, transform_features, response_scale, refit_origin)
from conditional_quantile import fit_quantile_ridge
from study_core import exact_rank, order_statistic


def _integer(value, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError('invalid integer option')
    return int(value)


def _finite(value, minimum=None, maximum=None):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise ValueError('finite real scalar required')
    value = float(value)
    if not math.isfinite(value) or minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise ValueError('scalar outside finite range')
    return value


def simulate_level_garch(z, phi, omega, alpha, beta, burn_in):
    z = np.asarray(z, dtype=np.float64)
    phi, omega, alpha, beta = map(_finite, (phi, omega, alpha, beta))
    burn_in = _integer(burn_in)
    if (z.ndim != 1 or not z.size or not np.isfinite(z).all() or burn_in >= len(z)
            or abs(phi) >= 1 or omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1):
        raise ValueError('invalid stationary level-AR/GARCH input')
    level = np.empty(len(z)); variance = np.empty(len(z)); innovation = np.empty(len(z))
    previous_level = 0.
    with np.errstate(over='raise', invalid='raise'):
        for i, shock in enumerate(z):
            v = 1. if i == 0 else omega + alpha * innovation[i-1] ** 2 + beta * variance[i-1]
            if not math.isfinite(v) or v <= 0:
                raise ValueError('nonfinite or nonpositive innovation variance')
            variance[i] = v
            innovation[i] = math.sqrt(v) * shock
            level[i] = phi * previous_level + innovation[i]
            previous_level = level[i]
    if not all(np.isfinite(a).all() for a in (level, variance, innovation)):
        raise ValueError('nonfinite simulated process')
    return dict(position=level[burn_in:].copy(), variance=variance[burn_in:].copy(),
                innovations=innovation[burn_in:].copy())


def repetition_normals(rep, design):
    rep = _integer(rep)
    if rep >= design['repetitions']:
        raise ValueError('repetition outside frozen inventory')
    stream = np.random.SeedSequence(design['master_entropy'], spawn_key=(rep,))
    rng = np.random.Generator(np.random.PCG64(stream))
    initial = copy.deepcopy(rng.bit_generator.state)
    z = rng.standard_normal(design['burn_in'] + design['retained_observations'])
    return z, initial, copy.deepcopy(rng.bit_generator.state)


def select_candidate(records, method, expected_origins, menus):
    if method not in ('QR33', 'QR4'):
        raise ValueError('unsupported conditional method')
    expected_origins = _integer(expected_origins, 1)
    records = list(records)
    menu = menus[method]
    if len(records) != len(menu) or [r.get('penalty') for r in records] != menu:
        raise ValueError('candidate menu mismatch')
    complete = []
    for row in records:
        if row.get('status') not in ('COMPLETE', 'FAILED', 'INCOMPLETE'):
            raise ValueError('invalid candidate status')
        if row['status'] == 'COMPLETE':
            if row.get('origin_count') != expected_origins:
                raise ValueError('incomplete candidate labelled complete')
            _finite(row.get('mean_loss'), 0)
            complete.append(row)
    if not complete or method == 'QR33' and len(complete) != len(menu):
        return dict(status='INELIGIBLE', penalty=None)
    chosen = min(complete, key=lambda r: (r['mean_loss'],
                 -r['penalty'] if method == 'QR33' else r['penalty']))
    return dict(status='SELECTED', penalty=chosen['penalty'],
                mean_validation_loss=chosen['mean_loss'])


def forecast_report(position, times, features, cache, origins, horizon, window,
                    refit_step, method, penalty=None, checkpoint=None):
    x = np.asarray(position, dtype=np.float64)
    ids = np.asarray(origins)
    t = np.asarray(times)
    if (method not in ('F', 'QR33', 'QR4') or x.ndim != 1 or not np.isfinite(x).all()
            or ids.ndim != 1 or not ids.size or ids.dtype.kind not in 'iu'
            or np.any(np.diff(ids) != 1) or ids[0] < 0
            or int(ids[-1]) + horizon >= len(x) or t.shape != x.shape
            or t.dtype.kind != 'M' or cache.horizon != horizon):
        raise ValueError('invalid complete report input')
    window = _integer(window, 1); refit_step = _integer(refit_step, 1)
    horizon = _integer(horizon, 1)
    if method != 'F':
        _finite(penalty, 0)
        if penalty <= 0:
            raise ValueError('nonpositive ridge penalty')
    capacities = np.empty(len(ids)); refits = np.empty(len(ids), dtype=np.int64)
    diagnostics = []; last = None
    for j, raw_t in enumerate(ids):
        issue = int(raw_t); r = refit_origin(issue, int(ids[0]), refit_step)
        if r != last:
            if checkpoint is not None:
                checkpoint(stage='refit', method=method, issue=issue)
            pool = completed_training_indices(r, horizon, window,
                    minimum_feature_index=0 if method == 'F' else features.valid_from)
            if np.any(cache.label_end[pool] > r):
                raise ValueError('unfinished training response')
            d = dict(refit_index=r, training_first_origin=int(pool[0]),
                     training_last_origin=int(pool[-1]), training_count=len(pool),
                     latest_label_end=int(cache.label_end[pool[-1]]))
            if method == 'F':
                rank = exact_rank(window, 19, 20)
                if rank > window:
                    raise ValueError('unavailable corrected rank')
                historical_q = order_statistic(cache.headroom[pool], rank)
            else:
                if method == 'QR33':
                    transform = fit_feature_transform(features.values[pool])
                    train = transform_features(features.values[pool], transform)
                else:
                    # Match original features4(...).copy() reduction/layout arithmetic.
                    raw = features.values[pool][:, [25, 0, 26, 27]].copy()
                    mu = raw.mean(axis=0); sd = raw.std(axis=0)
                    constant = np.all(raw == raw[0], axis=0)
                    mu[constant] = raw[0, constant]; sd[constant] = 1.
                    sd[sd == 0] = 1.
                    train = (raw - mu) / sd
                scale = response_scale(cache.headroom[pool], x[pool])
                def progress(detail):
                    if checkpoint is not None:
                        checkpoint(stage='fit', method=method, iteration=detail['iteration'])
                fit = fit_quantile_ridge(np.column_stack((np.ones(len(pool)), train)),
                        cache.headroom[pool] / scale, tau=19/20, penalty=penalty,
                        checkpoint=progress)
                d.update(iterations=fit.iterations, duality_gap=fit.duality_gap,
                         gap_tolerance=fit.gap_tolerance, primal_residual=fit.primal_residual,
                         primal_tolerance=fit.primal_tolerance, dual_residual=fit.dual_residual,
                         dual_tolerance=fit.dual_tolerance, response_scale=scale)
            diagnostics.append(d); last = r
        if method == 'F':
            predicted = historical_q
        else:
            if method == 'QR33':
                query = transform_features(features.values[issue:issue+1], transform)[0]
            else:
                query = (features.values[issue, [25, 0, 26, 27]] - mu) / sd
            predicted = scale * float(fit.coefficients[0] + query @ fit.coefficients[1:])
        if not math.isfinite(predicted):
            raise ValueError('nonfinite predicted headroom')
        capacities[j] = abs(x[issue]) + max(0., predicted)
        refits[j] = r
        if checkpoint is not None and (j % 24 == 0 or j == len(ids)-1):
            checkpoint(stage='issue', method=method, completed=j+1)
    if not np.isfinite(capacities).all() or np.any(capacities < np.abs(x[ids])):
        raise ValueError('invalid final capacities')
    return dict(origins=ids.copy(), capacity=capacities, refit_indices=refits,
                fit_diagnostics=diagnostics)


def summary_from_repetitions(rows, planned_repetitions):
    planned = _integer(planned_repetitions, 1)
    rows = list(rows)
    if len(rows) != planned:
        raise ValueError('planned repetition inventory mismatch')
    try:
        ids = [_integer(r['rep']) for r in rows]
    except (KeyError, TypeError) as exc:
        raise ValueError('missing repetition identity') from exc
    if sorted(ids) != list(range(planned)):
        raise ValueError('duplicate, missing or unexpected repetition')
    complete = []; failed = unattempted = 0
    for row in rows:
        status = row.get('status')
        if status == 'COMPLETE':
            try:
                record = {key: _finite(row[key], 0, 1 if 'rate' in key else None)
                          for key in ('reference_loss', 'model_loss',
                                      'reference_breach_rate', 'model_breach_rate')}
            except (KeyError, TypeError) as exc:
                raise ValueError('missing complete numerical report') from exc
            complete.append(record)
        elif status == 'FAILED':
            failed += 1
        elif status == 'NOT_ATTEMPTED':
            unattempted += 1
        else:
            raise ValueError('unknown repetition status')
    count = len(complete)
    result = dict(planned_repetitions=planned, complete_repetitions=count,
                  failed_repetitions=failed, unattempted_repetitions=unattempted,
                  conditional_on_completion=count != planned,
                  full_procedure_status='COMPLETE' if count == planned else 'NA',
                  full_procedure_relative_loss_percent=None)
    fields = ('relative_loss_percent', 'relative_loss_mcse', 'model_breach_rate',
              'model_breach_mcse', 'reference_breach_rate', 'reference_breach_mcse',
              'win_fraction', 'win_mcse', 'win_mcse_worst_bound')
    result.update({key: None for key in fields})
    if not count:
        return result
    a = [r['model_loss'] for r in complete]
    b = [r['reference_loss'] for r in complete]
    mean_a, mean_b = statistics.mean(a), statistics.mean(b)
    result['mean_model_loss'] = mean_a; result['mean_reference_loss'] = mean_b
    if mean_b:
        ratio = mean_a / mean_b
        result['relative_loss_percent'] = 100 * (ratio - 1)
        if count > 1:
            residual = [x - ratio*y for x, y in zip(a, b)]
            result['relative_loss_mcse'] = 100 * statistics.stdev(residual) / (math.sqrt(count) * mean_b)
    for name in ('model', 'reference'):
        values = [r[name + '_breach_rate'] for r in complete]
        result[name + '_breach_rate'] = statistics.mean(values)
        if count > 1:
            result[name + '_breach_mcse'] = statistics.stdev(values) / math.sqrt(count)
    p = sum(x < y for x, y in zip(a, b)) / count
    result['win_fraction'] = p
    if count > 1:
        result['win_mcse'] = math.sqrt(p * (1-p) / count)
    result['win_mcse_worst_bound'] = .5 / math.sqrt(count)
    if count == planned:
        result['full_procedure_relative_loss_percent'] = result['relative_loss_percent']
    return result
