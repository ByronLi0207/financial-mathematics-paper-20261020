"""Source-independent generic-tau engines for the frozen exploratory WP5.

The QR pipeline retains the immutable original 33-feature construction,
training-only transforms, response scale, original segment anchor, numerical
solver and acceptance defaults. One code path handles every tau, including
the .95 control. The caller owns the original complete segment origin vector,
tail admission, full validation menu, selection freeze and whole-cell NA rule.
No files or financial sources are read, and no environment is changed here.
"""
from fractions import Fraction
import math
import time

import numpy as np

import study_core as core
from conditional_features import (build_features, completed_training_indices,
    fit_feature_transform, transform_features, refit_origin, response_scale)
from conditional_quantile import fit_quantile_ridge, QuantileFitError
from conditional_study import StudyConfig, ConditionalForecast, _ids, _qr_diagnostics


def _level(tau):
    if isinstance(tau, (bool, np.bool_)) or np.ndim(tau) != 0:
        raise ValueError('INTERIOR_SCALAR_TAU_REQUIRED')
    try:
        level = tau if isinstance(tau, Fraction) else Fraction(str(tau))
        representable = float(level)
    except (ValueError, TypeError, OverflowError, ZeroDivisionError) as error:
        raise ValueError('INTERIOR_SCALAR_TAU_REQUIRED') from error
    if not 0 < level < 1 or not 0 < representable < 1:
        raise ValueError('INTERIOR_SCALAR_TAU_REQUIRED')
    return level


def forecast_qr_tau(position, times, origins, config, parameter, *, tau, checkpoint=None):
    """Original QR semantics with an explicit target level; no fallback forecast.

    Failed refits propagate QuantileFitError with the original private failure
    context/partial trace. Those rows are not a complete result to be scored.
    Caller checkpoint exceptions propagate unchanged.
    """
    level = _level(tau)
    if not isinstance(config, StudyConfig):
        raise ValueError('invalid conditional configuration')
    x = core._vector(position, 'conditional positions')
    ids = _ids(origins, len(x))
    if ids[-1] + config.horizon >= len(x):
        raise ValueError('incomplete evaluation outcome')
    if np.asarray(parameter).ndim or isinstance(parameter, (bool, np.bool_)):
        raise ValueError('invalid ridge penalty')
    parameter = float(parameter)
    if not math.isfinite(parameter) or parameter <= 0:
        raise ValueError('invalid ridge penalty')
    features = build_features(x, times, short_scale=config.short_scale, long_scale=config.long_scale,
                              nominal_gap_seconds=config.nominal_gap_seconds)
    cache = core.build_label_cache(x, config.horizon)
    caps = np.empty(len(ids)); floors = np.abs(x[ids]); refits = np.empty(len(ids), dtype=np.int64)
    diagnostics = []; previous_refit = None
    last_probe = [-math.inf]

    def fit_progress(_progress):
        now = time.monotonic()
        if checkpoint is not None and now - last_probe[0] >= .25:
            checkpoint(stage='conditional_fit')
            last_probe[0] = now

    for j, raw_t in enumerate(ids):
        t = int(raw_t); r = refit_origin(t, int(ids[0]), config.refit_step)
        if not r <= t < r + config.refit_step:
            raise ValueError('query/refit schedule mismatch')
        if r != previous_refit:
            if checkpoint is not None:
                checkpoint(stage='conditional_refit', completed_origins=j)
            pool = completed_training_indices(r, config.horizon, config.window,
                                              minimum_feature_index=features.valid_from)
            if not np.all(cache.label_end[pool] <= r):
                raise ValueError('unfinished training labels')
            transform = fit_feature_transform(features.values[pool])
            train = transform_features(features.values[pool], transform, nearest=False)
            train_g = cache.headroom[pool]; scale = response_scale(train_g, x[pool])
            detail = dict(refit_index=r, training_first_origin=int(pool[0]), training_last_origin=int(pool[-1]),
                          training_count=len(pool), latest_label_end=int(cache.label_end[pool[-1]]), response_scale=scale)
            try:
                fit = fit_quantile_ridge(np.column_stack((np.ones(len(pool)), train)), train_g / scale,
                                         tau=float(level), penalty=parameter, checkpoint=fit_progress)
            except QuantileFitError as error:
                error.failure_context = dict(detail, query_issue=t, issued_origin_count=j)
                error.partial_forecast = ConditionalForecast(core._readonly(ids[:j]), core._readonly(caps[:j]),
                    core._readonly(floors[:j]), core._readonly(refits[:j]), tuple(diagnostics), 'QR', parameter)
                raise
            detail.update(_qr_diagnostics(fit))
            diagnostics.append(detail); previous_refit = r
        query = transform_features(features.values[t:t+1], transform, nearest=False)[0]
        predicted = scale * float(fit.coefficients[0] + query @ fit.coefficients[1:])
        if not math.isfinite(predicted):
            raise ValueError('nonfinite predicted headroom')
        caps[j] = floors[j] + max(0., predicted); refits[j] = r
        if checkpoint is not None and (j % 32 == 31 or j == len(ids)-1):
            checkpoint(stage='conditional_issue', completed_origins=j+1)
    if not np.isfinite(caps).all() or np.any(caps < floors):
        raise ValueError('invalid final conditional capacity')
    return ConditionalForecast(core._readonly(ids), core._readonly(caps), core._readonly(floors),
                               core._readonly(refits), tuple(diagnostics), 'QR', parameter)


def historical_f_tau(position, origins, config, *, tau, rolling=False, checkpoint=None):
    """Exact corrected-rank headroom F with the original rolling/frozen clock."""
    level = _level(tau)
    if not isinstance(config, StudyConfig) or not isinstance(rolling, (bool, np.bool_)):
        raise ValueError('invalid historical configuration')
    x = core._vector(position, 'historical positions'); ids = _ids(origins, len(x))
    if ids[-1] + config.horizon >= len(x):
        raise ValueError('incomplete historical outcome')
    rank = core.exact_rank(config.window, level.numerator, level.denominator)
    if rank > config.window:
        raise ValueError('UNAVAILABLE_HISTORICAL_RANK')
    cache = core.build_label_cache(x, config.horizon)
    caps = np.empty(len(ids)); previous_refit = None
    for j, raw_t in enumerate(ids):
        t = int(raw_t)
        r = t if rolling else refit_origin(t, int(ids[0]), config.refit_step)
        if r != previous_refit:
            pool = completed_training_indices(r, config.horizon, config.window, minimum_feature_index=0)
            if not np.all(cache.label_end[pool] <= r):
                raise ValueError('historical maturity mismatch')
            allowance = core.order_statistic(cache.headroom[pool], rank)
            previous_refit = r
        caps[j] = abs(float(x[t])) + allowance
        if checkpoint is not None and (j % 32 == 31 or j == len(ids)-1):
            checkpoint(stage='historical_issue', completed_origins=j+1)
    if not np.isfinite(caps).all() or np.any(caps < np.abs(x[ids])):
        raise ValueError('invalid historical capacity')
    return core._readonly(caps)


def tail_admission(windows, validation_count, *, tau, minimum_expected=5):
    """Exact nominal-tail information convention, applied before new-tau fits.

    Fractions are serialized exactly as strings. Counts are a transparent
    minimum-information convention, not an inferential calibration guarantee.
    All supplied windows remain visible, including unavailable rank rows.
    """
    level = _level(tau); tail = 1 - level
    if isinstance(windows, (int, np.integer)):
        windows = [windows]
    try:
        window_values = [core._integer(value, 'tail window', 1) for value in windows]
    except TypeError as error:
        raise ValueError('nonempty window inventory required') from error
    if not window_values:
        raise ValueError('nonempty window inventory required')
    validation_count = core._integer(validation_count, 'validation count', 1)
    if isinstance(minimum_expected, (bool, np.bool_)):
        raise ValueError('positive nominal tail minimum required')
    try:
        minimum = Fraction(str(minimum_expected))
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError('positive nominal tail minimum required') from error
    if minimum <= 0:
        raise ValueError('positive nominal tail minimum required')
    rows = []
    for window in window_values:
        expected = window * tail
        rank = core.exact_rank(window, level.numerator, level.denominator)
        rows.append(dict(window=window, rank=rank, rank_available=rank <= window,
                         nominal_tail_fraction=str(expected), nominal_tail_count=float(expected),
                         sufficient_nominal_tail=expected >= minimum))
    validation_tail = validation_count * tail
    reasons = []
    if any(not row['rank_available'] for row in rows):
        reasons.append('UNAVAILABLE_HISTORICAL_RANK')
    if validation_tail < minimum or any(not row['sufficient_nominal_tail'] for row in rows):
        reasons.append('INSUFFICIENT_NOMINAL_TAIL')
    return dict(status='ELIGIBLE' if not reasons else 'INELIGIBLE', eligible=not reasons,
                reason=reasons[0] if reasons else None, reasons=reasons,
                tau=float(level), tau_fraction=str(level), tail_probability_fraction=str(tail),
                minimum_expected_fraction=str(minimum), validation_count=validation_count,
                validation_tail_fraction=str(validation_tail), validation_tail_count=float(validation_tail),
                validation_sufficient_nominal_tail=validation_tail >= minimum, window_rows=rows,
                interpretation='Nominal minimum-information convention; no calibration guarantee')
