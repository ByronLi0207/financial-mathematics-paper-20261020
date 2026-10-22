"""Bounded, direct ridge quantile regression using NumPy and mature ADMM.

The objective is mean pinball(y-X beta) + penalty*||beta[1:]||^2/2.
X includes a column of ones; the intercept is unpenalized. Callers own
causal feature construction, scaling, label maturity and forecast projection.

Optimization references: Boyd et al. (2011), doi:10.1561/2200000016,
Sections 3.1-3.3; the quantile-regression split also appears in
Pietrosanu et al., arXiv:1709.04126v1. The ridge/mean-loss updates and
Fenchel gap below are derived for this exact objective. No source's
statistical guarantee is claimed for the fitted financial application.
"""

from dataclasses import dataclass
import math
from types import MappingProxyType

import numpy as np


MAX_ROWS = 10000
MAX_COLUMNS = 128
DUAL_DENOMINATOR = 1 << 40


class QuantileFitError(ValueError):
    """An explicit failure; diagnostics contain scalars, never a forecast."""

    def __init__(self, code, diagnostics=None):
        self.code = str(code)
        self.diagnostics = MappingProxyType(dict(diagnostics or {}))
        super().__init__(self.code)


@dataclass(frozen=True)
class QuantileFit:
    coefficients: np.ndarray
    iterations: int
    primal_objective: float
    dual_objective: float
    duality_gap: float
    primal_residual: float
    dual_residual: float
    primal_tolerance: float
    dual_tolerance: float
    gap_tolerance: float
    dual_weights: np.ndarray
    dual_grid_numerators: np.ndarray
    dual_grid_denominator: int
    dual_integer_sum: int
    dual_integer_lower: int
    dual_integer_upper: int


def _immutable(values, dtype):
    array = np.ascontiguousarray(values, dtype=dtype)
    return np.frombuffer(array.tobytes(), dtype=dtype).reshape(array.shape)


def _real_option(value, name, *, zero_allowed=False):
    if isinstance(value, (bool, np.bool_)):
        raise QuantileFitError('INVALID_OPTION', {'option': name})
    try:
        if np.ndim(value) != 0:
            raise QuantileFitError('INVALID_OPTION', {'option': name})
        value = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise QuantileFitError('INVALID_OPTION', {'option': name}) from exc
    if not math.isfinite(value) or value < 0 or (value == 0 and not zero_allowed):
        raise QuantileFitError('INVALID_OPTION', {'option': name})
    return value


def _training_arrays(X, y):
    try:
        raw_X, raw_y = np.asarray(X), np.asarray(y)
    except (TypeError, ValueError, OverflowError) as exc:
        raise QuantileFitError('INVALID_TRAINING_ARRAY') from exc
    if (raw_X.ndim != 2 or raw_y.ndim != 1
            or raw_X.shape[0] != raw_y.shape[0]
            or not 1 <= raw_X.shape[0] <= MAX_ROWS
            or not 1 <= raw_X.shape[1] <= MAX_COLUMNS
            or raw_X.dtype.kind not in 'biuf'
            or raw_y.dtype.kind not in 'biuf'):
        raise QuantileFitError('INVALID_TRAINING_SHAPE_OR_TYPE')
    try:
        design = np.array(raw_X, dtype=np.float64, order='C', copy=True)
        response = np.array(raw_y, dtype=np.float64, copy=True)
    except (TypeError, ValueError, OverflowError) as exc:
        raise QuantileFitError('INVALID_TRAINING_ARRAY') from exc
    if not np.isfinite(design).all() or not np.isfinite(response).all():
        raise QuantileFitError('NONFINITE_TRAINING_DATA')
    if not np.all(design[:, 0] == 1):
        raise QuantileFitError('INTERCEPT_COLUMN_REQUIRED')
    return design, response


def _dual_projection(raw, tau):
    """Project, then construct an exactly zero-sum dyadic feasible point."""
    lower, upper = tau - 1, tau
    left = float(np.min(raw) - upper - 1)
    right = float(np.max(raw) - lower + 1)
    for _ in range(80):
        midpoint = left + (right - left) / 2
        if np.sum(np.clip(raw - midpoint, lower, upper)) > 0:
            left = midpoint
        else:
            right = midpoint
    shifted = np.clip(raw - (left + (right - left) / 2), lower, upper)
    numerator, denominator = tau.as_integer_ratio()
    grid = DUAL_DENOMINATOR
    integer_lower = -((denominator - numerator) * grid // denominator)
    integer_upper = numerator * grid // denominator
    numbers = np.clip(np.trunc(shifted * grid), integer_lower,
                      integer_upper).astype(np.int64)
    remainder = -sum(map(int, numbers))
    for j in range(len(numbers)):
        if remainder > 0:
            increment = min(remainder, integer_upper - int(numbers[j]))
        else:
            increment = max(remainder, integer_lower - int(numbers[j]))
        numbers[j] += increment
        remainder -= increment
        if remainder == 0:
            break
    exact_sum = sum(map(int, numbers))
    if (remainder != 0 or exact_sum != 0
            or np.min(numbers) < integer_lower
            or np.max(numbers) > integer_upper):
        raise QuantileFitError('DUAL_FEASIBILITY_FAILURE')
    weights = numbers.astype(np.float64) / grid
    return weights, numbers, integer_lower, integer_upper


def _certificate(X, y, beta, scaled_dual, tau, penalty, gap_rtol):
    n = len(y)
    # rho=1/n, so nu=-n*rho*u=-u for X beta+r-y=0.
    weights, numbers, lower, upper = _dual_projection(-scaled_dual, tau)
    errors = y - X @ beta
    moment = X[:, 1:].T @ weights / n
    primal = float(np.mean(tau * np.maximum(errors, 0)
                           + (1 - tau) * np.maximum(-errors, 0))
                   + penalty * np.dot(beta[1:], beta[1:]) / 2)
    dual = float(np.mean(weights * y)
                 - np.dot(moment, moment) / (2 * penalty))
    complement = np.where(errors >= 0, (tau - weights) * errors,
                          (weights - (tau - 1)) * (-errors))
    if np.any(complement < 0):
        raise QuantileFitError('NEGATIVE_FENCHEL_COMPONENT')
    stationarity = beta[1:] - moment / penalty
    gap = float(np.mean(complement)
                + penalty * np.dot(stationarity, stationarity) / 2)
    tolerance = gap_rtol * (1 + abs(primal))
    values = (primal, dual, gap, tolerance)
    if not all(map(math.isfinite, values)):
        raise QuantileFitError('NONFINITE_CERTIFICATE')
    roundoff = 256 * np.finfo(np.float64).eps * max(1., abs(primal), abs(dual))
    if abs((primal - dual) - gap) > roundoff:
        raise QuantileFitError('GAP_IDENTITY_FAILURE')
    return {'primal_objective': primal, 'dual_objective': dual,
            'duality_gap': gap, 'gap_tolerance': tolerance,
            'weights': weights, 'numbers': numbers,
            'integer_lower': lower, 'integer_upper': upper}


def fit_quantile_ridge(X, y, tau=.95, penalty=.01, max_iter=10000,
                       atol=1e-6, rtol=1e-5, gap_rtol=1e-6,
                       checkpoint=None):
    """Return a numerically accepted immutable fit, or raise QuantileFitError.

    No preprocessing, future response or financial file is accessed here.
    Iterations require both ADMM residual conditions and a feasible-dual
    Fenchel gap. The dual point has exact dyadic box/zero-sum feasibility;
    objective calculations remain float64, not interval arithmetic.
    ``checkpoint`` is called every 50 iterations with bounded scalar
    progress. Caller exceptions propagate to permit resource cancellation.
    """
    tau = _real_option(tau, 'tau')
    if tau >= 1:
        raise QuantileFitError('INVALID_OPTION', {'option': 'tau'})
    penalty = _real_option(penalty, 'penalty')
    atol = _real_option(atol, 'atol')
    rtol = _real_option(rtol, 'rtol', zero_allowed=True)
    gap_rtol = _real_option(gap_rtol, 'gap_rtol')
    if (isinstance(max_iter, (bool, np.bool_))
            or not isinstance(max_iter, (int, np.integer))
            or not 1 <= int(max_iter) <= 10000):
        raise QuantileFitError('INVALID_OPTION', {'option': 'max_iter'})
    if checkpoint is not None and not callable(checkpoint):
        raise QuantileFitError('INVALID_OPTION', {'option': 'checkpoint'})
    max_iter = int(max_iter)
    X, y = _training_arrays(X, y)
    n, p = X.shape
    rho = 1 / n
    try:
        with np.errstate(over='raise', divide='raise', invalid='raise'):
            regularizer = np.eye(p)
            regularizer[0, 0] = 0
            system = rho * (X.T @ X) + penalty * regularizer
            right = rho * X.T
            if not np.isfinite(system).all() or not np.isfinite(right).all():
                raise QuantileFitError('NONFINITE_LINEAR_SYSTEM')
            operator = np.linalg.solve(system, right)
            if not np.isfinite(operator).all():
                raise QuantileFitError('NONFINITE_LINEAR_SOLVE')
            linear_error = float(np.linalg.norm(system @ operator - right))
            right_norm = float(np.linalg.norm(right))
            if not math.isfinite(linear_error) or not math.isfinite(right_norm):
                raise QuantileFitError('NONFINITE_LINEAR_SOLVE_RESIDUAL')
            if linear_error > 1e-9 * (1 + right_norm):
                raise QuantileFitError('LINEAR_SOLVE_RESIDUAL')
            beta = np.zeros(p)
            beta[0] = float(np.quantile(y, tau, method='inverted_cdf'))
            residual = y - X @ beta
            scaled_dual = np.zeros(n)
    except (FloatingPointError, np.linalg.LinAlgError) as exc:
        raise QuantileFitError('NUMERICAL_INITIALIZATION_FAILURE') from exc
    certificate = None
    diagnostics = {}
    for iteration in range(1, max_iter + 1):
        try:
            with np.errstate(over='raise', divide='raise', invalid='raise'):
                beta = operator @ (y - residual - scaled_dual)
                prediction = X @ beta
                value = y - prediction - scaled_dual
                previous = residual
                residual = (np.maximum(value - tau / (n * rho), 0)
                            + np.minimum(value + (1 - tau) / (n * rho), 0))
                primal_vector = prediction + residual - y
                scaled_dual = scaled_dual + primal_vector
                dual_vector = rho * (X.T @ (residual - previous))
                primal_norm = float(np.linalg.norm(primal_vector))
                dual_norm = float(np.linalg.norm(dual_vector))
                primal_tolerance = float(math.sqrt(n) * atol + rtol * max(
                    np.linalg.norm(prediction), np.linalg.norm(residual),
                    np.linalg.norm(y)))
                dual_tolerance = float(math.sqrt(p) * atol + rtol * np.linalg.norm(
                    rho * (X.T @ scaled_dual)))
                if not all(map(math.isfinite, (primal_norm, dual_norm,
                                              primal_tolerance, dual_tolerance))):
                    raise QuantileFitError('NONFINITE_ITERATE')
                diagnostics = {'iterations': iteration,
                               'primal_residual': primal_norm,
                               'dual_residual': dual_norm,
                               'primal_tolerance': primal_tolerance,
                               'dual_tolerance': dual_tolerance}
                residuals_pass = (primal_norm <= primal_tolerance
                                  and dual_norm <= dual_tolerance)
                if residuals_pass or iteration == max_iter:
                    certificate = _certificate(X, y, beta, scaled_dual, tau,
                                               penalty, gap_rtol)
        except (FloatingPointError, np.linalg.LinAlgError) as exc:
            raise QuantileFitError('NUMERICAL_ITERATION_FAILURE', diagnostics) from exc
        if checkpoint is not None and iteration % 50 == 0:
            checkpoint({'stage': 'quantile_fit', 'iteration': iteration,
                        'primal_residual': primal_norm,
                        'dual_residual': dual_norm})
        if (residuals_pass and certificate is not None
                and certificate['duality_gap'] <= certificate['gap_tolerance']):
            return QuantileFit(
                _immutable(beta, np.float64), iteration,
                certificate['primal_objective'], certificate['dual_objective'],
                certificate['duality_gap'], primal_norm, dual_norm,
                primal_tolerance, dual_tolerance, certificate['gap_tolerance'],
                _immutable(certificate['weights'], np.float64),
                _immutable(certificate['numbers'], np.int64), DUAL_DENOMINATOR,
                0, certificate['integer_lower'], certificate['integer_upper'])
    if certificate is not None:
        diagnostics.update({name: certificate[name] for name in (
            'primal_objective', 'dual_objective', 'duality_gap', 'gap_tolerance')})
    raise QuantileFitError('NONCONVERGENCE', diagnostics)
