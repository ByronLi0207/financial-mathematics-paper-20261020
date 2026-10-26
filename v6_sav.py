"""Source-independent, mature-headroom SAV under the frozen v6 WP2 contract.

This is a headroom adaptation, not a literal replication of return CAViaR.
There is no source I/O, financial scoring, global fit, environment mutation or
worker launch at import. The caller supplies G_i=P_i-|N_i|, position N, the
complete segment origin vector, and the original segment's refit grid.

A worker owns resource limits. Its ``checkpoint(stage=...)`` exceptions propagate
without being converted into optimizer nonconvergence or partial forecasts.
"""
from dataclasses import dataclass
import math
from typing import Callable

import numpy as np


Checkpoint = Callable[..., None]
_BOUNDS = ((0., 100.), (0., .995), (0., 100.))
_TAU = .95


def _integer(value, name, minimum=1):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError('invalid ' + name)
    return int(value)


def _readonly(values, dtype=np.float64):
    result = np.array(values, dtype=dtype, copy=True)
    result.flags.writeable = False
    return result


def _checkpoint(callback, stage):
    if callback is not None:
        callback(stage=stage)


@dataclass(frozen=True)
class SAVConfig:
    horizon: int
    window: int
    refit_step: int
    segment_start: int

    def __post_init__(self):
        for name in ('horizon', 'window', 'refit_step'):
            object.__setattr__(self, name, _integer(getattr(self, name), name))
        object.__setattr__(self, 'segment_start', _integer(self.segment_start, 'segment start', 0))


@dataclass(frozen=True)
class SAVStart:
    index: int
    initial_coefficients: tuple
    success: bool
    eligible: bool
    status: str
    objective: float | None
    solver_objective: float | None
    nfev: int | None
    nit: int | None
    solver_status: int | None
    message: str
    coefficients: tuple | None
    bound_solutions: tuple


@dataclass(frozen=True)
class SAVRefit:
    refit_index: int
    status: str
    coefficients: np.ndarray
    scale: float
    initial_quantile: float
    objective: float
    selected_start: int | None
    starts: tuple
    initialization_origins: np.ndarray
    training_origins: np.ndarray
    training_shock_origins: np.ndarray
    path_origins: np.ndarray
    normalized_path: np.ndarray


@dataclass(frozen=True)
class SAVForecast:
    capacities: np.ndarray
    headroom_quantiles: np.ndarray
    refits: tuple
    diagnostics: dict


class SAVFitError(RuntimeError):
    """Terminal whole-cell failure; contains receipts but no partial forecasts."""
    def __init__(self, code, refit_index, diagnostics=None):
        self.code = str(code)
        self.refit_index = int(refit_index)
        self.diagnostics = {} if diagnostics is None else diagnostics
        super().__init__(f'{self.code} at SAV refit {self.refit_index}')


def sav_path(coefficients, shocks, initial_quantile):
    """Evaluate q_i=b0+b1*q_(i-1)+b2*shock_i in normalized response units.

    The caller chooses shock_i=G_(i-H)/a. This low-level function does not infer
    maturity from a shock vector. ``initial_quantile`` is q just before its path.
    """
    from scipy.signal import lfilter
    beta = np.asarray(coefficients, dtype=np.float64)
    shock = np.asarray(shocks, dtype=np.float64)
    if (beta.shape != (3,) or shock.ndim != 1 or not np.isfinite(beta).all()
            or not np.isfinite(shock).all() or np.any(shock < 0)
            or not math.isfinite(float(initial_quantile)) or initial_quantile < 0):
        raise ValueError('invalid normalized SAV recurrence input')
    if not shock.size:
        return _readonly([])
    with np.errstate(over='raise', invalid='raise'):
        path, _ = lfilter([1.], [1., -beta[1]], beta[0] + beta[2] * shock,
                          zi=[beta[1] * float(initial_quantile)])
    if not np.isfinite(path).all():
        raise ValueError('nonfinite normalized SAV recurrence')
    return _readonly(path)


def _sources(headroom, position):
    g = np.asarray(headroom, dtype=np.float64)
    x = np.asarray(position, dtype=np.float64)
    if g.ndim != 1 or x.ndim != 1 or not g.size or not x.size or len(g) > len(x):
        raise ValueError('invalid SAV source arrays')
    # Do not inspect unavailable/future response values. Only causal slices below
    # are checked for finite nonnegative G; G may end H rows before position.
    return g, x


def _mature(g, first, stop, refit, name):
    if first < 0 or stop > len(g) or stop <= first:
        raise SAVFitError('INADEQUATE_MATURE_HISTORY', refit,
                          {'slice': name, 'first': first, 'stop': stop})
    result = g[first:stop]
    if not np.isfinite(result).all() or np.any(result < 0):
        raise SAVFitError('INVALID_MATURE_HEADROOM', refit,
                          {'slice': name, 'first': first, 'stop': stop})
    return result


def _scale(y, anchors, refit):
    if not np.isfinite(anchors).all():
        raise SAVFitError('INVALID_TRAINING_POSITION', refit)
    try:
        with np.errstate(over='raise', invalid='raise'):
            scale = max(float(np.mean(y)), 1e-6 * float(np.mean(np.abs(anchors))), 1e-12)
    except FloatingPointError as error:
        raise SAVFitError('NONFINITE_RESPONSE_SCALE', refit) from error
    if not math.isfinite(scale):
        raise SAVFitError('NONFINITE_RESPONSE_SCALE', refit)
    return scale


def _objective(beta, shocks, response, initial_quantile):
    residual = response - sav_path(beta, shocks, initial_quantile)
    # Match the frozen source-native scoring weights: float(19/20), float(1/20).
    return float(np.mean(np.where(residual >= 0., _TAU * residual, -.05 * residual)))


def _optional_int(value):
    try:
        return None if value is None else int(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _finite_float(value):
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return result if math.isfinite(result) else None


def _bound_solutions(coefficients):
    if coefficients is None:
        return ()
    names = ('beta0', 'beta1', 'beta2')
    # Exact optimizer bounds, without a new numerical proximity threshold.
    return tuple(names[i] + '_' + label
                 for i, pair in enumerate(_BOUNDS)
                 for bound, label in zip(pair, ('lower', 'upper'))
                 if coefficients[i] == bound)


def fit_sav_refit(headroom, position, refit, config, *, checkpoint=None):
    """Fit one original grid refit and propagate its fitted path through refit.

    Pool L..U is [r-H-W+1,r-H]. Initialization is the empirical inverse-CDF
    .95 quantile of the last at most W labels mature at L-1, ending L-H-1.
    This initialization uses ceil(.95*n), not the corrected report rank.
    Returned q values and coefficients use G/a units; capacities use source units.
    """
    from scipy.optimize import minimize
    if not isinstance(config, SAVConfig):
        raise ValueError('SAVConfig required')
    r = _integer(refit, 'refit', 0)
    if r < config.segment_start or (r - config.segment_start) % config.refit_step:
        raise ValueError('refit is outside original segment grid')
    g, x = _sources(headroom, position)
    h, w = config.horizon, config.window
    _checkpoint(checkpoint, 'sav_refit_begin')
    first = r - h - w + 1
    stop = r - h + 1
    response = _mature(g, first, stop, r, 'training')
    initial_stop = first - h
    if initial_stop <= 0:
        raise SAVFitError('NO_INITIAL_MATURE_LABELS', r,
                          {'training_first': first, 'initialization_issue': first - 1})
    initial_first = max(0, initial_stop - w)
    initial_response = _mature(g, initial_first, initial_stop, r, 'initialization')
    training_shocks = _mature(g, first - h, stop - h, r, 'training_shocks')
    if r >= len(x):
        raise SAVFitError('INADEQUATE_POSITION_HISTORY', r)
    scale = _scale(response, x[first:stop], r)
    normalized_response = response / scale
    normalized_shocks = training_shocks / scale
    # Integer arithmetic prevents ceil boundary drift for n divisible by 20.
    rank = (19 * len(initial_response) + 19) // 20
    initial_quantile = float(np.partition(initial_response, rank - 1)[rank - 1]) / scale
    starts = []
    if np.all(response == response[0]):
        beta = np.array([float(normalized_response[0]), 0., 0.])
        objective = 0.
        selected_start = None
        status = 'ANALYTIC_CONSTANT'
    else:
        best = None
        for b1 in (.2, .6, .9):
            for b2 in (.01, .1):
                index = len(starts)
                b0 = min(100., max(1e-6, initial_quantile * (1. - b1)
                                  - b2 * float(np.mean(normalized_shocks))))
                initial = (b0, b1, b2)
                _checkpoint(checkpoint, 'sav_start_begin')
                def objective_function(coefficients):
                    _checkpoint(checkpoint, 'sav_objective')
                    return _objective(coefficients, normalized_shocks,
                                      normalized_response, initial_quantile)
                result = minimize(objective_function, initial, method='Powell', bounds=_BOUNDS,
                                  options={'xtol': 1e-7, 'ftol': 1e-8,
                                           'maxiter': 1000, 'maxfev': 3000})
                raw = np.asarray(getattr(result, 'x', []), dtype=np.float64)
                legal = (raw.shape == (3,) and np.isfinite(raw).all()
                         and all(lo <= raw[i] <= hi for i, (lo, hi) in enumerate(_BOUNDS)))
                coefficients = tuple(float(v) for v in raw) if legal else None
                value = (_finite_float(_objective(raw, normalized_shocks,
                                                 normalized_response, initial_quantile))
                         if legal else None)
                solver_value = _finite_float(getattr(result, 'fun', None))
                success = bool(getattr(result, 'success', False))
                eligible = success and legal and value is not None and solver_value is not None
                start_status = ('CONVERGED' if eligible else 'NONCONVERGED' if not success
                                else 'INVALID_COEFFICIENTS' if not legal else 'NONFINITE_OBJECTIVE')
                receipt = SAVStart(index, initial, success, eligible, start_status,
                                   value, solver_value, _optional_int(getattr(result, 'nfev', None)),
                                   _optional_int(getattr(result, 'nit', None)),
                                   _optional_int(getattr(result, 'status', None)),
                                   str(getattr(result, 'message', '')), coefficients,
                                   _bound_solutions(coefficients))
                starts.append(receipt)
                # Strict '<' preserves start order on an exact objective tie.
                if eligible and (best is None or value < best[0]):
                    best = (value, index, raw.copy())
                _checkpoint(checkpoint, 'sav_start_end')
        if best is None:
            raise SAVFitError('NO_CONVERGED_START', r,
                              {'starts': tuple(starts), 'scale': scale,
                               'initial_quantile': initial_quantile,
                               'training_first': first, 'training_last': stop - 1})
        objective, selected_start, beta = best
        status = 'CONVERGED'
    # With fixed coefficients, reset and carry the path from L through actual r.
    path_shocks = _mature(g, first - h, r - h + 1, r, 'fit_through_refit_shocks') / scale
    path_origins = np.arange(first, r + 1, dtype=np.int64)
    path = sav_path(beta, path_shocks, initial_quantile)
    _checkpoint(checkpoint, 'sav_refit_end')
    return SAVRefit(r, status, _readonly(beta), scale, initial_quantile,
                    float(objective), selected_start, tuple(starts),
                    _readonly(np.arange(initial_first, initial_stop), np.int64),
                    _readonly(np.arange(first, stop), np.int64),
                    _readonly(np.arange(first - h, stop - h), np.int64),
                    _readonly(path_origins, np.int64), path)


def forecast_sav(headroom, position, origins, config, *, checkpoint=None):
    """Issue a complete continuous origin vector, or raise with no partial result.

    Refits remain anchored at config.segment_start even when origins starts later.
    Between refits each internal issue uses exactly G_(t-H), including steps
    between a refit and the first requested issue. A refit resets the fitted path.
    The caller must invalidate an evaluation cell if its validation had failed.
    """
    if not isinstance(config, SAVConfig):
        raise ValueError('SAVConfig required')
    g, x = _sources(headroom, position)
    issues = np.asarray(origins)
    if (issues.ndim != 1 or not issues.size or issues.dtype.kind not in 'iu'
            or np.any(issues > np.iinfo(np.int64).max)
            or np.any(issues < config.segment_start)
            or np.any(np.diff(issues.astype(np.int64)) != 1)):
        raise ValueError('complete consecutive segment origins required')
    issues = issues.astype(np.int64, copy=False)
    if issues[-1] >= len(x):
        raise ValueError('issue exceeds position history')
    capacities = np.empty(len(issues))
    quantiles = np.empty(len(issues))
    refit_origins = np.empty(len(issues), dtype=np.int64)
    fits = []
    current = None
    previous = None
    current_issue = None
    floor_count = 0
    for j, issue in enumerate(issues):
        t = int(issue)
        r = config.segment_start + config.refit_step * ((t - config.segment_start) // config.refit_step)
        _checkpoint(checkpoint, 'sav_issue_begin')
        if current is None or current.refit_index != r:
            current = fit_sav_refit(g, x, r, config, checkpoint=checkpoint)
            fits.append(current)
            previous = float(current.normalized_path[-1])
            current_issue = r
        if current_issue < t:
            shocks = _mature(g, current_issue + 1 - config.horizon,
                             t - config.horizon + 1, r, 'issue_shocks') / current.scale
            previous = float(sav_path(current.coefficients, shocks, previous)[-1])
            current_issue = t
        if not math.isfinite(float(x[t])):
            raise SAVFitError('INVALID_ISSUE_POSITION', r, {'issue': t})
        with np.errstate(over='raise', invalid='raise'):
            head = current.scale * previous
            report = abs(float(x[t])) + max(0., head)
        if not math.isfinite(head) or not math.isfinite(report):
            raise SAVFitError('NONFINITE_REPORT', r, {'issue': t})
        quantiles[j] = head
        capacities[j] = report
        refit_origins[j] = r
        floor_count += int(head <= 0.)
        _checkpoint(checkpoint, 'sav_issue_end')
    diagnostics = {
        'status': 'COMPLETE', 'origin_count': len(issues), 'refit_count': len(fits),
        'analytic_refit_count': sum(fit.status == 'ANALYTIC_CONSTANT' for fit in fits),
        'converged_refit_count': sum(fit.status == 'CONVERGED' for fit in fits),
        'floor_count': floor_count,
        'issue_refit_origins': _readonly(refit_origins, np.int64),
        'issue_shock_origins': _readonly(issues - config.horizon, np.int64),
    }
    return SAVForecast(_readonly(capacities), _readonly(quantiles), tuple(fits), diagnostics)
