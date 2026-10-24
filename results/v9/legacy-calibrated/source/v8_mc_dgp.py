"""Frozen v8 synthetic DGPs and a current-state conditional peak oracle.

No source files, calibration, model selection or experiment are performed by
this module. ``residual`` always denotes the latent unseasonalized u_t.
"""
from dataclasses import dataclass
import math

import numpy as np


_HOURLY_ANCHOR = np.datetime64('2000-01-03T00:00:00', 's')
_WEEKLY_ANCHOR = np.datetime64('2000-01-05T00:00:00', 's')


def _integer(value, name, minimum=1):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError('invalid ' + name)
    result = int(value)
    if result < minimum:
        raise ValueError('invalid ' + name)
    return result


def _finite(value, name):
    if isinstance(value, (bool, np.bool_)) or np.asarray(value).ndim:
        raise ValueError('invalid ' + name)
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError('invalid ' + name) from error
    if not math.isfinite(result):
        raise ValueError('invalid ' + name)
    return result


@dataclass(frozen=True)
class DGPParams:
    dgp: str
    c: float
    phi: float
    omega: float = 1.
    alpha: float = 0.
    beta: float = 0.
    nu: float | None = 8.
    shape: tuple = (1.,) * 24
    sigma: float = 1.
    burnin: int = 10000

    def __post_init__(self):
        if self.dgp not in ('D0', 'D1', 'D2'):
            raise ValueError('unknown DGP')
        for name in ('c', 'phi', 'omega', 'alpha', 'beta', 'sigma'):
            object.__setattr__(self, name, _finite(getattr(self, name), name))
        if self.nu is not None:
            object.__setattr__(self, 'nu', _finite(self.nu, 'nu'))
        # phi=1 is reserved for the explicitly nonstationary oracle fixture;
        # simulate() rejects it because its stationary initializer is undefined.
        if abs(self.phi) > 1 or (abs(self.phi) == 1 and self.dgp != 'D0'):
            raise ValueError('invalid AR coefficient')
        if self.omega < 0 or self.alpha < 0 or self.beta < 0 or self.alpha + self.beta >= 1:
            raise ValueError('invalid stationary GARCH parameters')
        if self.dgp != 'D0' and (self.omega == 0 or self.nu is None or self.nu <= 2):
            raise ValueError('invalid GARCH innovation distribution')
        if self.sigma <= 0 or (self.nu is not None and self.nu <= 2):
            raise ValueError('invalid innovation distribution')
        try:
            shape = tuple(_finite(value, 'hour shape') for value in self.shape)
        except TypeError as error:
            raise ValueError('invalid hour shape') from error
        if len(shape) != 24 or min(shape) <= 0:
            raise ValueError('invalid hour shape')
        object.__setattr__(self, 'shape', shape)
        burnin = _integer(self.burnin, 'burnin')
        if burnin > 1000000:
            raise ValueError('burnin exceeds frozen limit')
        object.__setattr__(self, 'burnin', burnin)


def clock(dgp, indices):
    """Known trading clock, extended to negative burn-in indices by floor.

    The retained path begins at integer index zero, independent of burn-in.
    There are 120 hourly records per trading week and a 48-hour weekend gap.
    """
    if dgp not in ('D0', 'D1', 'D2'):
        raise ValueError('unknown DGP')
    raw = np.asarray(indices)
    if raw.dtype.kind not in 'iu' or (raw.dtype.kind == 'u' and np.any(raw > np.iinfo(np.int64).max)):
        raise ValueError('clock indices must be integers')
    ids = raw.astype(np.int64, copy=False)
    # Scientific paths have at most a million burn-in observations; a broad
    # bound also prevents silent datetime/int64 arithmetic overflow.
    if np.any(np.abs(ids.astype(object)) > 10**9):
        raise ValueError('clock index overflow')
    if dgp == 'D1':
        hours = ids + 48 * np.floor_divide(ids, 120)
        return _HOURLY_ANCHOR + (hours * 3600).astype('timedelta64[s]')
    return _WEEKLY_ANCHOR + (ids * 604800).astype('timedelta64[s]')


def _seed(seed):
    if isinstance(seed, np.random.SeedSequence):
        # Reconstructing avoids spawn counters or worker order changing draws.
        return np.random.SeedSequence(seed.entropy, spawn_key=seed.spawn_key,
                                      pool_size=seed.pool_size)
    return np.random.SeedSequence(seed)


def _draws(rng, size, params):
    if params.dgp == 'D0':
        return rng.standard_normal(size)
    return rng.standard_t(params.nu, size=size) * math.sqrt((params.nu - 2) / params.nu)


def simulate(params, n, seed):
    """Simulate one path after the supplied, already calibrated burn-in.

    Parameters are never clipped or repaired. The caller's calibrated burn-in
    is fixed by the protocol; fixture parameters also use this same interface.
    Only retained arrays are returned, on clock indices 0,...,n-1.
    """
    if not isinstance(params, DGPParams):
        raise ValueError('DGPParams required')
    n = _integer(n, 'path length')
    if abs(params.phi) >= 1:
        raise ValueError('stationary initializer undefined')
    total = params.burnin + n
    indices = np.arange(-params.burnin, n, dtype=np.int64)
    times = clock(params.dgp, indices)
    if params.dgp == 'D1':
        hours = times.astype('datetime64[h]').astype(np.int64) % 24
        shape = np.asarray(params.shape)[hours]
    else:
        shape = np.ones(total)
    shocks = _draws(np.random.default_rng(_seed(seed)), total, params)
    position = np.empty(n)
    variance = np.empty(n)
    residual = np.empty(n)
    current = params.c / (1 - params.phi)
    current_v = params.sigma**2 if params.dgp == 'D0' else params.omega / (1 - params.alpha - params.beta)
    current_u = 0.
    try:
        for index in range(total):
            if params.dgp != 'D0':
                current_v = params.omega + params.alpha * current_u**2 + params.beta * current_v
            current_u = math.sqrt(current_v) * float(shocks[index])
            current = params.c + params.phi * current + float(shape[index]) * current_u
            if not all(map(math.isfinite, (current, current_v, current_u))) or current_v <= 0:
                raise ValueError('nonfinite DGP state')
            if index >= params.burnin:
                out = index - params.burnin
                position[out], variance[out], residual[out] = current, current_v, current_u
    except (OverflowError, FloatingPointError) as error:
        raise ValueError('DGP numerical failure') from error
    return dict(position=position, variance=variance, residual=residual,
                times=times[params.burnin:].copy())


def _clock_indices(dgp, times):
    """Recover only the current known clock index; never inspect future rows."""
    ts = np.asarray(times).astype('datetime64[s]')
    anchor = _HOURLY_ANCHOR if dgp == 'D1' else _WEEKLY_ANCHOR
    seconds = (ts - anchor).astype('timedelta64[s]').astype(np.int64)
    if dgp == 'D1':
        if np.any(seconds % 3600):
            raise ValueError('invalid hourly clock state')
        hours = seconds // 3600
        week_hours = hours % 168
        if np.any(week_hours >= 120):
            raise ValueError('current time lies in excluded weekend')
        ids = (hours // 168) * 120 + week_hours
    else:
        if np.any(seconds % 604800):
            raise ValueError('invalid weekly clock state')
        ids = seconds // 604800
    if not np.array_equal(clock(dgp, ids), ts):
        raise ValueError('clock mismatch')
    return ids


def oracle_reports(params, path, origins, horizon=6, paths=2000, seed=20261024,
                   batch_size=32):
    """Monte Carlo inverted-CDF .95 quantiles of the complete absolute peak.

    At t, use precisely N_t,v_t,u_t and the deterministic future clock. Each
    origin receives a distinct SeedSequence child keyed by its actual index;
    batching changes memory use without changing any random draw or report.
    A finite Monte Carlo oracle is an approximation, not a samplewise bound.
    """
    if not isinstance(params, DGPParams):
        raise ValueError('DGPParams required')
    horizon = _integer(horizon, 'horizon')
    paths = _integer(paths, 'oracle paths')
    batch_size = _integer(batch_size, 'batch size')
    raw_ids = np.asarray(origins)
    if raw_ids.ndim != 1 or not raw_ids.size or raw_ids.dtype.kind not in 'iu':
        raise ValueError('invalid oracle origins')
    if np.any(raw_ids > np.iinfo(np.int64).max) or np.any(raw_ids < 0):
        raise ValueError('invalid oracle origins')
    ids = raw_ids.astype(np.int64, copy=False)
    if np.any(np.diff(ids) <= 0):
        raise ValueError('oracle origins must increase')
    try:
        x, v, u, times = [np.asarray(path[key]) for key in ('position', 'variance', 'residual', 'times')]
    except (KeyError, TypeError) as error:
        raise ValueError('incomplete DGP state') from error
    if x.ndim != 1 or any(a.shape != x.shape for a in (v, u, times)) or ids[-1] >= len(x):
        raise ValueError('DGP state alignment mismatch')
    if times.dtype.kind != 'M' or np.isnat(times[ids]).any():
        raise ValueError('invalid current clock')
    # Only selected current states are checked: a future realized suffix can
    # be absent, changed or undefined without affecting a conditional oracle.
    current_x, current_v, current_u = [np.asarray(a[ids], dtype=float) for a in (x, v, u)]
    if not all(np.isfinite(a).all() for a in (current_x, current_v, current_u)) or np.any(current_v <= 0):
        raise ValueError('invalid current DGP state')
    clock_ids = _clock_indices(params.dgp, times[ids])
    root_seed = _seed(seed)
    result = np.empty(len(ids))
    rank_index = (19 * paths + 19) // 20 - 1
    shape = np.asarray(params.shape)
    for start in range(0, len(ids), batch_size):
        stop = min(start + batch_size, len(ids))
        count = stop - start
        draws = np.empty((count, horizon, paths))
        for j, origin in enumerate(ids[start:stop]):
            child = np.random.SeedSequence(root_seed.entropy,
                spawn_key=root_seed.spawn_key + (int(origin),), pool_size=root_seed.pool_size)
            draws[j] = _draws(np.random.default_rng(child), (horizon, paths), params)
        levels = np.broadcast_to(current_x[start:stop, None], (count, paths)).copy()
        variances = np.broadcast_to(current_v[start:stop, None], (count, paths)).copy()
        residuals = np.broadcast_to(current_u[start:stop, None], (count, paths)).copy()
        peaks = np.abs(levels)
        try:
            with np.errstate(over='raise', invalid='raise'):
                for h in range(horizon):
                    if params.dgp == 'D0':
                        variances.fill(params.sigma**2)
                    else:
                        variances = params.omega + params.alpha * residuals**2 + params.beta * variances
                    residuals = np.sqrt(variances) * draws[:, h, :]
                    multiplier = 1.
                    if params.dgp == 'D1':
                        next_times = clock('D1', clock_ids[start:stop] + h + 1)
                        next_hours = next_times.astype('datetime64[h]').astype(np.int64) % 24
                        multiplier = shape[next_hours, None]
                    levels = params.c + params.phi * levels + multiplier * residuals
                    np.maximum(peaks, np.abs(levels), out=peaks)
                result[start:stop] = np.partition(peaks, rank_index, axis=1)[:, rank_index]
        except (FloatingPointError, OverflowError) as error:
            raise ValueError('oracle numerical failure') from error
    if not np.isfinite(result).all() or np.any(result < np.abs(current_x)):
        raise ValueError('invalid oracle reports')
    return result
