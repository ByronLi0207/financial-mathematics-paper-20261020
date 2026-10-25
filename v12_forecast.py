"""Caller-owned v12 forecast/score adapter; no source I/O or study launch.

At tau=.95 the frozen v10/empirical reports are delegated unchanged. Other
levels reuse their mature-pool, transform, response scale, solver and floor
projection, with the explicitly declared saturated corrected empirical rank.
Saturation is a sensitivity convention and supplies no coverage guarantee.
"""
from fractions import Fraction
import math
from numbers import Integral, Real

import numpy as np

from conditional_features import (build_features, completed_training_indices,
    fit_feature_transform, transform_features, response_scale, refit_origin)
from conditional_quantile import fit_quantile_ridge
from empirical_headroom import predict as empirical_predict
from study_core import build_label_cache, order_statistic, stable_mean
from v10_menu import forecast_report as frozen_report
from v6_inference import pinball_losses


def _positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral) or value < 1:
        raise ValueError('invalid ' + name)
    return int(value)


def _tau(tau):
    if isinstance(tau, (bool, np.bool_)) or not isinstance(tau, Real):
        raise ValueError('invalid tau')
    value = float(tau)
    if not math.isfinite(value) or not 0 < value < 1:
        raise ValueError('invalid tau')
    return Fraction(str(tau))


def _origins(context, origins):
    raw = np.asarray(origins)
    if (raw.ndim != 1 or not raw.size or raw.dtype.kind not in 'iu'
            or np.any(raw < 0) or np.any(raw > np.iinfo(np.int64).max)):
        raise ValueError('invalid full segment origins')
    ids = raw.astype(np.int64, copy=True)
    if (np.any(np.diff(ids) != 1)
            or int(ids[-1]) + context['cell']['horizon'] >= len(context['position'])):
        raise ValueError('invalid full segment origins')
    return ids


def make_context(series: dict, cell: dict) -> dict:
    """Own immutable source-array copies and construct reusable causal features.

    The caller owns source identity, protocol binding, segment inventory,
    resource limits and one-attempt caching; this function does no selection.
    Future labels in the cache enter only scoring, or explicitly mature pools.
    """
    names = ('horizon', 'window', 'refit_step', 'short_scale', 'long_scale',
             'nominal_gap_seconds')
    cfg = {name: _positive_integer(cell[name], name) for name in names}
    raw = np.asarray(series['position'])
    if raw.ndim != 1 or raw.dtype.kind not in 'iuf':
        raise ValueError('invalid position array')
    x = np.array(raw, dtype=np.float64, copy=True)
    times = np.array(series['times'], copy=True)
    if not np.isfinite(x).all() or times.shape != x.shape:
        raise ValueError('invalid source arrays')
    features = build_features(x, times, short_scale=cfg['short_scale'],
        long_scale=cfg['long_scale'], nominal_gap_seconds=cfg['nominal_gap_seconds'])
    labels = build_label_cache(x, cfg['horizon'])
    x.flags.writeable = False
    times.flags.writeable = False
    return dict(position=x, times=times, cell=cfg, features=features, cache=labels)


def _historical_report(context, ids, method, level, checkpoint):
    x = context['position']; cfg = context['cell']
    h, w, step = cfg['horizon'], cfg['window'], cfg['refit_step']
    if checkpoint is not None:
        checkpoint(stage='refit', method=method, issue=int(ids[0]))
    if level == Fraction(19, 20):
        p = empirical_predict(x, ids, h, w, step)
        details = [dict(refit_index=int(r),
            training_first_origin=int(p['training_first_origins'][j]),
            training_last_origin=int(p['training_last_origins'][j]),
            training_count=w, latest_label_end=int(p['latest_label_ends'][j]))
            for j, r in enumerate(p['refit_indices']) if j == 0 or r != p['refit_indices'][j-1]]
        result = dict(origins=p['origins'].copy(), capacity=p[method].copy(),
            refit_indices=p['refit_indices'].copy(), fit_diagnostics=details)
    else:
        numerator, denominator = level.numerator, level.denominator
        rank = ((w + (method == 'F')) * numerator + denominator - 1) // denominator
        if method == 'F':
            rank = min(w, rank)
        capacities = np.empty(len(ids)); refits = np.empty(len(ids), dtype=np.int64)
        details = []; previous = None
        for j, issue in enumerate(ids):
            r = refit_origin(int(issue), int(ids[0]), step)
            if r != previous:
                if previous is not None and checkpoint is not None:
                    checkpoint(stage='refit', method=method, issue=int(issue))
                pool = completed_training_indices(r, h, w, minimum_feature_index=0)
                if np.any(context['cache'].label_end[pool] > r):
                    raise ValueError('unfinished training response')
                headroom = order_statistic(context['cache'].headroom[pool], rank)
                details.append(dict(refit_index=r, training_first_origin=int(pool[0]),
                    training_last_origin=int(pool[-1]), training_count=w,
                    latest_label_end=int(context['cache'].label_end[pool[-1]])))
                previous = r
            capacities[j] = abs(x[issue]) + headroom
            refits[j] = r
        result = dict(origins=ids.copy(), capacity=capacities,
                      refit_indices=refits, fit_diagnostics=details)
    if checkpoint is not None:
        checkpoint(stage='issue', method=method, completed=len(ids))
    return result


def predict_segment(context, origins, method, penalty=None, *, tau=.95, checkpoint=None):
    """Return a full fixed-parameter report, propagating failures unchanged.

    Required output keys match the frozen v10 report. No partial success,
    fallback, selected alternative, warm start or retry occurs here.
    """
    level = _tau(tau)
    ids = _origins(context, origins)
    if method not in ('F', 'I', 'QR33', 'QR4'):
        raise ValueError('undeclared forecast method')
    if checkpoint is not None and not callable(checkpoint):
        raise ValueError('invalid checkpoint')
    if method in ('F', 'I'):
        if penalty is not None:
            raise ValueError('empirical report has no ridge penalty')
        return _historical_report(context, ids, method, level, checkpoint)
    if type(penalty) is str and penalty == 'inf':
        if level == Fraction(19, 20):
            cfg = context['cell']
            return frozen_report(context['position'], context['times'], context['features'],
                context['cache'], ids, cfg['horizon'], cfg['window'], cfg['refit_step'],
                method, penalty, checkpoint=checkpoint)
        return _historical_report(context, ids, 'I', level, checkpoint)
    if (isinstance(penalty, (bool, np.bool_)) or not isinstance(penalty, Real)
            or not math.isfinite(float(penalty)) or penalty <= 0):
        raise ValueError('invalid ridge penalty')
    cfg = context['cell']
    if level == Fraction(19, 20):
        return frozen_report(context['position'], context['times'], context['features'],
            context['cache'], ids, cfg['horizon'], cfg['window'], cfg['refit_step'],
            method, penalty, checkpoint=checkpoint)

    x, features, labels = context['position'], context['features'], context['cache']
    h, w, step = cfg['horizon'], cfg['window'], cfg['refit_step']
    capacities = np.empty(len(ids)); refits = np.empty(len(ids), dtype=np.int64)
    details = []; previous = None
    for j, issue in enumerate(ids):
        issue = int(issue); r = refit_origin(issue, int(ids[0]), step)
        if r != previous:
            if checkpoint is not None:
                checkpoint(stage='refit', method=method, issue=issue)
            pool = completed_training_indices(r, h, w, minimum_feature_index=features.valid_from)
            if np.any(labels.label_end[pool] > r):
                raise ValueError('unfinished training response')
            if method == 'QR33':
                transform = fit_feature_transform(features.values[pool])
                train = transform_features(features.values[pool], transform)
            else:
                raw = features.values[pool][:, [25, 0, 26, 27]].copy()
                mu = raw.mean(axis=0); sd = raw.std(axis=0)
                constant = np.all(raw == raw[0], axis=0)
                mu[constant] = raw[0, constant]; sd[constant] = 1.
                sd[sd == 0] = 1.
                train = (raw - mu) / sd
            scale = response_scale(labels.headroom[pool], x[pool])
            def progress(detail):
                if checkpoint is not None:
                    checkpoint(stage='fit', method=method, iteration=detail['iteration'])
            fit = fit_quantile_ridge(np.column_stack((np.ones(len(pool)), train)),
                labels.headroom[pool] / scale, tau=float(level), penalty=penalty,
                checkpoint=progress)
            details.append(dict(refit_index=r, training_first_origin=int(pool[0]),
                training_last_origin=int(pool[-1]), training_count=len(pool),
                latest_label_end=int(labels.label_end[pool[-1]]),
                iterations=fit.iterations, duality_gap=fit.duality_gap,
                gap_tolerance=fit.gap_tolerance, primal_residual=fit.primal_residual,
                primal_tolerance=fit.primal_tolerance, dual_residual=fit.dual_residual,
                dual_tolerance=fit.dual_tolerance, response_scale=scale))
            previous = r
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
    return dict(origins=ids.copy(), capacity=capacities,
                refit_indices=refits, fit_diagnostics=details)


def score_report(context, origins, capacity, *, tau=.95):
    """Score exactly the supplied full aligned, finite floor-projected segment."""
    level = _tau(tau)
    ids = _origins(context, origins)
    raw = np.asarray(capacity)
    if raw.ndim != 1 or raw.dtype.kind not in 'iuf' or raw.shape != ids.shape:
        raise ValueError('invalid full score vector')
    caps = np.array(raw, dtype=np.float64, copy=True)
    peak = context['cache'].peak[ids].copy()
    floor = np.abs(context['position'][ids])
    if (not np.isfinite(caps).all() or not np.isfinite(peak).all()
            or np.any(caps < floor) or np.any(peak < floor)):
        raise ValueError('invalid score alignment or floor')
    losses = pinball_losses(peak, caps, tau=float(level))
    with np.errstate(over='raise', invalid='raise'):
        error = peak - caps
        under = np.maximum(error, 0.)
        over = np.maximum(-error, 0.)
    breaches = int(np.count_nonzero(error > 0))
    return dict(mean_loss=stable_mean(losses), n=len(ids), strict_breach_count=breaches,
        strict_breach_rate=breaches/len(ids), losses=losses, peak=peak, floor=floor,
        mean_underprediction=stable_mean(under), mean_overprediction=stable_mean(over))
