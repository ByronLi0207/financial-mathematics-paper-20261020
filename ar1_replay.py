"""Bounded, source-independent AR(1) historical residual-path replay.

No input file, model selection, source loading or financial execution occurs
here. A history owns only one mature union and at most 2880 x 25 path values.
"""
from dataclasses import dataclass
import math
import numbers

import numpy as np

import study_core as core


class AR1Error(ValueError):
    """Fixed code only: exception text never contains source values or paths."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class AR1Fit:
    phi: float
    c: float
    scale: float
    transition_count: int
    scaled_mean_residual: float
    scaled_regressor_residual: float
    normal_tolerance: float
    scaled_x_mean: float
    scaled_y_mean: float
    scaled_x_variance: float


@dataclass(frozen=True)
class AR1History:
    refit: int
    first_origin: int
    last_origin: int
    horizon: int
    window: int
    rank: int
    levels: np.ndarray
    paths: np.ndarray
    lower_increment: np.ndarray
    upper_increment: np.ndarray
    fit: AR1Fit


def _numeric_vector(values):
    try:
        raw = np.asarray(values)
        if raw.ndim != 1 or raw.dtype.kind not in 'iuf':
            raise AR1Error('AR1_INVALID_LEVELS')
        with np.errstate(over='raise', invalid='raise'):
            return np.asarray(raw, dtype=np.float64)
    except AR1Error:
        raise
    except (ValueError, TypeError, OverflowError, FloatingPointError):
        raise AR1Error('AR1_INVALID_LEVELS') from None


def _mean(values):
    # Division before a correctly rounded sum avoids an avoidable large sum.
    values = tuple(float(x) for x in values)
    if all(x == values[0] for x in values):
        return values[0]
    return math.fsum(x/len(values) for x in values)


def fit_ar1(levels):
    """Intercept-bearing centered OLS on unique adjacent transitions.

    A common power-of-two level scale and separate represented anchors preserve
    small changes on large offsets. Lost dispersion fails without a fallback.
    """
    z = _numeric_vector(levels)
    if len(z) < 3:
        raise AR1Error('AR1_INVALID_LEVELS')
    if not np.isfinite(z).all():
        raise AR1Error('AR1_NONFINITE_LEVELS')
    x, y = z[:-1], z[1:]
    if np.all(x == x[0]):
        raise AR1Error('AR1_CONSTANT_REGRESSOR')
    try:
        with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
            maximum = float(np.max(np.abs(z)))
            if not math.isfinite(maximum) or maximum <= 0:
                raise AR1Error('AR1_NONFINITE_FIT')
            # Binary division preserves represented normal spacings; cap the
            # largest exponent so the common scale itself remains finite.
            exponent = min(math.frexp(maximum)[1],1023)
            scale = math.ldexp(1.,exponent)
            u, v = x/scale, y/scale
            anchor_u, anchor_v = float(u[0]), float(v[0])
            offset_u, offset_v = u-anchor_u, v-anchor_v
            mean_u, mean_v = _mean(offset_u), _mean(offset_v)
            # Never center via a reconstructed high-offset mean: adding the
            # anchor first can round away exactly the covariance of interest.
            du, dv = offset_u-mean_u, offset_v-mean_v
            mu, mv = anchor_u+mean_u, anchor_v+mean_v
            denominator = math.fsum(float(a)*float(a) for a in du)
            variance = denominator/len(x)
            if (not math.isfinite(denominator) or denominator <= 0
                    or not math.isfinite(variance) or variance <= 0):
                raise AR1Error('AR1_DISPERSION_LOST')
            covariance = math.fsum(float(a)*float(b) for a,b in zip(du,dv))
            phi = covariance/denominator
            scaled_intercept = math.fsum((anchor_v,mean_v,-phi*anchor_u,-phi*mean_u))
            c = scale*scaled_intercept
            if not all(math.isfinite(a) for a in (mu,mv,covariance,phi,scaled_intercept,c)):
                raise AR1Error('AR1_NONFINITE_FIT')
            # Check the actual returned intercept in original units, not only
            # an internally unrounded scaled parameterization.
            returned_intercept = c/scale
            residual = v-phi*u-returned_intercept
            if not np.isfinite(residual).all():
                raise AR1Error('AR1_NONFINITE_FIT')
            mean_residual = abs(_mean(residual))
            regressor_residual = abs(_mean(float(a)*float(b) for a,b in zip(u,residual)))
            tolerance = 1e-10*max(1., _mean(np.abs(v)), _mean(np.abs(phi*u)), abs(returned_intercept))
            if not all(math.isfinite(a) for a in (mean_residual,regressor_residual,tolerance)):
                raise AR1Error('AR1_NONFINITE_FIT')
            if mean_residual > tolerance or regressor_residual > tolerance:
                raise AR1Error('AR1_NORMAL_EQUATIONS')
    except AR1Error:
        raise
    except (ArithmeticError, ValueError):
        raise AR1Error('AR1_NONFINITE_FIT') from None
    return AR1Fit(float(phi),float(c),scale,len(x),mean_residual,regressor_residual,
        tolerance,mu,mv,variance)


def _index(value, minimum, maximum=None):
    if (isinstance(value,(bool,np.bool_)) or not isinstance(value,(int,np.integer))
            or value < minimum or (maximum is not None and value > maximum)):
        raise AR1Error('AR1_INVALID_INDEX')
    return int(value)


def _immutable(values):
    array = np.ascontiguousarray(values,dtype=np.float64)
    # Immutable bytes backing prevents a caller from re-enabling writeability.
    return np.frombuffer(array.tobytes(),dtype=np.float64).reshape(array.shape)


def prepare_ar1_history(positions, refit, horizon, window):
    """Copy the W+H mature levels and fit each unique transition once."""
    refit = _index(refit,0)
    horizon = _index(horizon,1,24)
    window = _index(window,1,2880)
    rank = core.exact_rank(window,19,20)
    if rank > window:
        raise AR1Error('AR1_UNAVAILABLE_RANK')
    try:
        raw = np.asarray(positions)
    except (ValueError,TypeError):
        raise AR1Error('AR1_INVALID_LEVELS') from None
    if raw.ndim != 1 or raw.dtype.kind not in 'iuf':
        raise AR1Error('AR1_INVALID_LEVELS')
    first = refit-horizon-window+1
    if first < 0 or refit >= len(raw):
        raise AR1Error('AR1_INCOMPLETE_HISTORY')
    # Future positions do not enter conversion, finite checks or fitting.
    levels = _immutable(_numeric_vector(raw[first:refit+1]))
    fit = fit_ar1(levels)
    try:
        with np.errstate(over='raise',invalid='raise',under='ignore'):
            paths = _immutable(np.lib.stride_tricks.sliding_window_view(levels,horizon+1))
            increments = paths-paths[:,0,None]
            lower = _immutable(np.min(increments,axis=1))
            upper = _immutable(np.max(increments,axis=1))
            if (paths.shape != (window,horizon+1) or not np.isfinite(increments).all()
                    or np.any(lower > 0) or np.any(upper < 0)):
                raise AR1Error('AR1_NONFINITE_HISTORY')
    except (ArithmeticError,ValueError):
        raise AR1Error('AR1_NONFINITE_HISTORY') from None
    return AR1History(refit,first,refit-horizon,horizon,window,rank,
        levels,paths,lower,upper,fit)


def predict(history, query):
    """Issue one peak report, preserving the legacy S operation order at phi1."""
    if not isinstance(history,AR1History) or not isinstance(history.fit,AR1Fit):
        raise AR1Error('AR1_INVALID_HISTORY')
    if isinstance(query,(bool,np.bool_)) or not isinstance(query,numbers.Real):
        raise AR1Error('AR1_INVALID_QUERY')
    try:
        current = float(query)
    except (OverflowError,ValueError,TypeError):
        raise AR1Error('AR1_INVALID_QUERY') from None
    if not math.isfinite(current):
        raise AR1Error('AR1_INVALID_QUERY')
    floor = abs(current)
    phi = history.fit.phi
    if not math.isfinite(phi):
        raise AR1Error('AR1_NONFINITE_REPLAY')
    try:
        with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
            if phi == 1.:
                # Exact frozen S: translated peak -> subtract B -> rank -> add B.
                headroom = np.maximum(current+history.upper_increment,
                    -current-history.lower_increment)-floor
            else:
                powers = np.empty(history.horizon+1,dtype=np.float64)
                powers[0] = 1.
                for h in range(1,len(powers)):
                    powers[h] = powers[h-1]*phi
                if not np.isfinite(powers).all():
                    raise AR1Error('AR1_NONFINITE_REPLAY')
                replay = np.empty_like(history.paths)
                replay[:,0] = current
                offset = current-history.paths[:,0]
                replay[:,1:] = history.paths[:,1:]+offset[:,None]*powers[None,1:]
                if not np.isfinite(replay).all():
                    raise AR1Error('AR1_NONFINITE_REPLAY')
                headroom = np.max(np.abs(replay),axis=1)-floor
            if (len(headroom) != history.window or not np.isfinite(headroom).all()
                    or np.any(headroom < 0)):
                raise AR1Error('AR1_NONFINITE_REPLAY')
            if history.rank < 1 or history.rank > history.window:
                raise AR1Error('AR1_UNAVAILABLE_RANK')
            capacity = floor+core.order_statistic(headroom,history.rank)
            if not math.isfinite(capacity) or capacity < floor:
                raise AR1Error('AR1_NONFINITE_REPLAY')
    except AR1Error:
        raise
    except (ArithmeticError,ValueError,IndexError):
        raise AR1Error('AR1_NONFINITE_REPLAY') from None
    return float(capacity)
