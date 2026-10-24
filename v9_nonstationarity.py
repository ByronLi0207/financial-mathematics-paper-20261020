"""Registered v9 diagnostic/calibration primitives; no import-time data I/O.

Inputs are caller-owned arrays. This module does not load financial data, run a
study, change historical modules, or retry a failed fit/bootstrap replicate.
"""
from __future__ import annotations

import copy
import importlib
import math
import warnings

import numpy as np
from arch import __version__ as arch_version
from arch.univariate import GARCH, StudentsT, ZeroMean
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.diagnostic import breaks_hansen


PARAMETER_NAMES = ('intercept', 'phi', 'omega', 'alpha', 'beta', 'nu')


class CalibrationError(ValueError):
    """An unavailable diagnostic/calibration, never a non-rejection."""
    def __init__(self, reason, details=None):
        self.reason = str(reason)
        self.details = {} if details is None else details
        super().__init__(self.reason)


def _levels(values, minimum=5):
    try:
        y = np.asarray(values, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise CalibrationError('INVALID_LEVELS') from exc
    if y.ndim != 1 or len(y) < minimum or not np.isfinite(y).all():
        raise CalibrationError('INVALID_LEVELS', {'minimum_levels': minimum})
    scale = float(y.std(ddof=0))
    if not math.isfinite(scale) or scale <= 0:
        raise CalibrationError('DEGENERATE_LEVEL_SCALE')
    return y, scale


def _integer(value, label, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise CalibrationError('INVALID_INTEGER_SETTING', {'setting': label})
    return int(value)


def _notify(checkpoint, **kwargs):
    if checkpoint is not None:
        checkpoint(**kwargs)


class _BoundedPersistenceGARCH(GARCH):
    """Add the declared persistence restriction before SLSQP optimization."""
    def __init__(self, persistence_bound):
        super().__init__(p=1, o=0, q=1)
        self.persistence_bound = float(persistence_bound)

    def constraints(self):
        a, b = super().constraints()
        # arch interprets these as a @ parameters - b >= 0.
        return np.vstack((a, [0., -1., -1.])), np.r_[b, -self.persistence_bound]


def fit_ar_garch(levels, design, start=0, stop=None):
    """One constrained AR profile fit and one constrained zero-mean GARCH fit.

    start/stop index global AR transition rows: row t has lag levels[t] and
    target levels[t+1]. Every segment retains the whole-prefix level scale.
    Returned parameters are in those normalized-level units.
    """
    y, input_scale = _levels(levels)
    M = len(y) - 1
    start = _integer(start, 'start')
    stop = M if stop is None else _integer(stop, 'stop')
    if start >= stop or stop > M or stop - start < 4:
        raise CalibrationError('INVALID_TRANSITION_INTERVAL', {'start': start, 'stop': stop, 'M': M})
    phi_bound = float(design.get('phi_bound', .999))
    persistence_bound = float(design.get('garch_persistence_bound', .999))
    if not 0 < phi_bound < 1 or not 0 < persistence_bound < 1:
        raise CalibrationError('INVALID_PARAMETER_BOUND')
    z = y / input_scale  # Deliberately preserve the original level mean.
    x, target = z[start:stop], z[start+1:stop+1]
    mx, my = float(x.mean()), float(target.mean())
    xc, yc = x - mx, target - my
    sxx = float(xc @ xc)
    if not math.isfinite(sxx) or sxx <= 0:
        raise CalibrationError('SINGULAR_AR_DESIGN')
    unconstrained_phi = float(xc @ yc / sxx)
    # Exact solution to the profiled box-constrained quadratic, not a
    # numerical fit followed by an undisclosed change to its parameters.
    candidates = [-phi_bound, phi_bound]
    if -phi_bound <= unconstrained_phi <= phi_bound:
        candidates.append(unconstrained_phi)
    phi = min(candidates, key=lambda p: float(np.sum((yc - p * xc)**2)))
    intercept = my - phi * mx
    residuals = target - intercept - phi * x
    residual_scale = float(residuals.std(ddof=0))
    if not math.isfinite(residual_scale) or residual_scale <= 0:
        raise CalibrationError('DEGENERATE_AR_RESIDUAL_SCALE')
    model = ZeroMean(residuals / residual_scale, rescale=False,
                     volatility=_BoundedPersistenceGARCH(persistence_bound),
                     distribution=StudentsT())
    options = {'maxiter': _integer(design.get('garch_maxiter', 2000), 'garch_maxiter', 1),
               'ftol': float(design.get('garch_ftol', 1e-9))}
    diagnostics = dict(input_scale=input_scale, residual_scale=residual_scale,
                       transition_start=start, transition_stop=stop,
                       transition_count=stop-start, level_mean_subtracted=False,
                       normalized_prefix_mean=float(z.mean()),
                       unconstrained_profile_phi=unconstrained_phi,
                       arch_version=arch_version,
                       restrictions={'phi_abs_max': phi_bound,
                                     'garch_persistence_max': persistence_bound,
                                     'rescale': False, 'fit_attempts': 1,
                                     'starting_values': 'library_default'},
                       optimizer_options=options.copy())
    with warnings.catch_warnings(record=True) as observed_warnings:
        warnings.simplefilter('always')
        try:
            fit = model.fit(disp='off', show_warning=False, options=options)
        except Exception as exc:
            raise CalibrationError('GARCH_FIT_EXCEPTION', {
                **diagnostics, 'exception': type(exc).__name__, 'message': str(exc)}) from exc
    optimization = fit.optimization_result
    flag = int(fit.convergence_flag)
    optimizer = dict(converged=flag == 0 and bool(optimization.success),
                     convergence_flag=flag, status=int(optimization.status),
                     message=str(optimization.message),
                     iterations=int(getattr(optimization, 'nit', 0)))
    diagnostics['optimizer'] = optimizer
    diagnostics['warnings'] = [str(w.message) for w in observed_warnings]
    if not optimizer['converged']:
        raise CalibrationError('GARCH_OPTIMIZATION_FAILED', diagnostics)
    fitted = fit.params
    p = dict(intercept=float(intercept), phi=float(phi),
             omega=float(fitted['omega'] * residual_scale**2),
             alpha=float(fitted['alpha[1]']), beta=float(fitted['beta[1]']),
             nu=float(fitted['nu']))
    if (not all(math.isfinite(v) for v in p.values()) or p['omega'] <= 0
            or min(p['alpha'], p['beta']) < 0 or p['alpha'] + p['beta'] >= 1
            or p['alpha'] + p['beta'] > persistence_bound + 1e-8 or p['nu'] <= 2):
        raise CalibrationError('INADMISSIBLE_GARCH_FIT', {**diagnostics, 'params': p})
    near = lambda value, bound: abs(value - bound) <= 1e-6
    boundary_hits = {'phi': near(abs(phi), phi_bound),
                     'garch_persistence': near(p['alpha'] + p['beta'], persistence_bound),
                     'student_df_lower': near(p['nu'], 2.05),
                     'student_df_upper': near(p['nu'], 500.)}
    diagnostics['boundary_hits'] = boundary_hits
    diagnostics['status'] = 'BOUNDARY_FIT' if any(boundary_hits.values()) else 'COMPLETE'
    diagnostics['omega_standardized_residual_units'] = float(fitted['omega'])
    return {'params': p, 'diagnostics': diagnostics}


def hansen_statistic(levels, condition_max=1e12):
    """Official Hansen joint statistic after unconstrained AR(1) OLS refit."""
    y, scale = _levels(levels)
    if not math.isfinite(condition_max) or condition_max < 1:
        raise CalibrationError('INVALID_CONDITION_LIMIT')
    z = y / scale
    x = np.column_stack((np.ones(len(z)-1), z[:-1]))
    if np.linalg.matrix_rank(x) != 2:
        raise CalibrationError('SINGULAR_AR_DESIGN')
    result = OLS(z[1:], x).fit()
    e = np.asarray(result.resid)
    scores = np.column_stack((x * e[:, None], e**2 - np.mean(e**2)))
    rms = np.sqrt(np.mean(scores**2, axis=0))
    if not np.isfinite(rms).all() or np.any(rms <= 0):
        raise CalibrationError('SINGULAR_HANSEN_SCORE')
    normalized = scores / rms
    correlation = normalized.T @ normalized / len(e)
    condition = float(np.linalg.cond(correlation))
    if (not math.isfinite(condition) or np.linalg.matrix_rank(correlation) != 3
            or condition > condition_max):
        raise CalibrationError('ILL_CONDITIONED_HANSEN_SCORE', {'condition_number': condition})
    try:
        value = float(breaks_hansen(result)[0])
    except np.linalg.LinAlgError as exc:
        raise CalibrationError('SINGULAR_HANSEN_SCORE') from exc
    if not math.isfinite(value) or value < 0:
        raise CalibrationError('NONFINITE_HANSEN_STATISTIC')
    return value


def moment_qualification(params, margin=1e-8):
    """Finite-second/fourth-moment model gate; not a real-data moment proof."""
    try:
        p = {name: float(params[name]) for name in PARAMETER_NAMES}
    except (KeyError, TypeError, ValueError):
        return dict(qualified=False, generation_admissible=False,
                    nu_gt4=False, kappa=None, q4=None, reason='INVALID_PARAMETERS')
    admissible = (all(math.isfinite(v) for v in p.values())
                  and abs(p['phi']) < 1 and p['omega'] > 0
                  and min(p['alpha'], p['beta']) >= 0
                  and p['alpha'] + p['beta'] < 1 and p['nu'] > 2)
    nu_gt4 = math.isfinite(p['nu']) and p['nu'] > 4
    kappa = 3 * (p['nu']-2) / (p['nu']-4) if nu_gt4 else None
    q4 = (p['alpha']**2 * kappa + 2*p['alpha']*p['beta'] + p['beta']**2
          if admissible and nu_gt4 else None)
    qualified = bool(admissible and nu_gt4 and q4 < 1-margin)
    reason = ('QUALIFIED' if qualified else 'INVALID_PARAMETERS' if not admissible
              else 'STUDENT_FOURTH_MOMENT_UNAVAILABLE' if not nu_gt4
              else 'GARCH_FOURTH_MOMENT_UNAVAILABLE')
    return dict(qualified=qualified, generation_admissible=bool(admissible),
                nu_gt4=bool(nu_gt4), kappa=kappa, q4=q4,
                fourth_moment_margin=float(margin), reason=reason)


def bootstrap_stability(levels, params, source_index, design, checkpoint=None):
    """One model-calibrated global p; any required numerical failure raises."""
    y, _ = _levels(levels)
    condition = float(design.get('score_correlation_condition_max', 1e12))
    observed = hansen_statistic(y, condition)
    moment = moment_qualification(params, float(design.get('fourth_moment_margin', 1e-8)))
    B = _integer(design.get('bootstrap_repetitions', 999), 'bootstrap_repetitions', 1)
    result = dict(status='NONREGULAR_NULL', statistic=observed, p_value=None,
                  exceedances=None, B=B, bootstrap_statistics=[],
                  moment=moment, rng_initial_state=None, rng_final_state=None,
                  monte_carlo_standard_error=None)
    if not moment['generation_admissible']:
        raise CalibrationError('INADMISSIBLE_NULL_PARAMETERS', {'moment': moment})
    if not moment['qualified']:
        return result
    source_index = _integer(source_index, 'source_index')
    entropy = _integer(design.get('master_entropy', 2026102408), 'master_entropy')
    namespace = _integer(design.get('rng_namespace', 9), 'rng_namespace')
    tag = _integer(design.get('diagnostic_stream_tag', 0), 'diagnostic_stream_tag')
    spawn_key = (namespace, tag, source_index)
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(entropy, spawn_key=spawn_key)))
    result['rng_initial_state'] = copy.deepcopy(rng.bit_generator.state)
    result['seed_identity'] = {'entropy': entropy, 'spawn_key': list(spawn_key), 'bit_generator': 'PCG64'}
    _notify(checkpoint, stage='bootstrap_generation', source_index=source_index, completed=0, planned=B)
    simulator = importlib.import_module('v9_switching').simulate_constant_paths
    try:
        paths = np.asarray(simulator(params, len(y), B, rng,
                                     _integer(design.get('burn_in', 20000), 'burn_in'),
                                     checkpoint=checkpoint), dtype=float)
    except Exception as exc:
        # Deadlines deliberately propagate so the driver can terminate promptly.
        if isinstance(exc, (TimeoutError, KeyboardInterrupt)):
            raise
        raise CalibrationError('BOOTSTRAP_GENERATION_FAILED', {'exception': type(exc).__name__, 'message': str(exc)}) from exc
    if paths.shape != (B, len(y)) or not np.isfinite(paths).all():
        raise CalibrationError('INVALID_BOOTSTRAP_PATH_INVENTORY', {'expected_shape': [B, len(y)], 'actual_shape': list(paths.shape)})
    statistics = []
    for index, path in enumerate(paths):
        _notify(checkpoint, stage='bootstrap_statistic', source_index=source_index, completed=index, planned=B)
        try:
            statistics.append(hansen_statistic(path, condition))
        except CalibrationError as exc:
            raise CalibrationError('BOOTSTRAP_STATISTIC_FAILED', {'replicate': index, 'cause': exc.reason,
                                                                'completed_statistics': statistics}) from exc
    exceedances = sum(value >= observed for value in statistics)
    p = (1 + exceedances) / (B + 1)
    result.update(status='COMPLETE', p_value=p, exceedances=exceedances,
                  bootstrap_statistics=statistics, rng_final_state=copy.deepcopy(rng.bit_generator.state),
                  monte_carlo_standard_error=math.sqrt(p * (1-p) / B))
    _notify(checkpoint, stage='bootstrap_complete', source_index=source_index, completed=B, planned=B)
    return result


def locate_breaks(levels, design):
    """Exact k<=2 global separate-variance AR/BIC locator, O(M) storage.

    A cut c splits transition rows [0,c) and [c,M); it is not a level index
    silently adjusted by one. Segmentation is descriptive, without p-values.
    """
    y, scale = _levels(levels)
    M = len(y)-1
    minimum = max(_integer(design.get('minimum_segment_transitions', 104), 'minimum_segment_transitions', 3),
                  int(math.ceil(float(design.get('minimum_segment_fraction', .2))*M)))
    maximum = _integer(design.get('max_breaks', 2), 'max_breaks')
    if maximum > 2:
        raise CalibrationError('UNSUPPORTED_BREAK_CAP')
    if M < minimum:
        raise CalibrationError('NO_LEGAL_PARTITION', {'M': M, 'min_segment': minimum})
    tolerance = float(design.get('bic_tie_tolerance', 1e-10))
    z = y / scale
    # Centering lag and target for sufficient-sum arithmetic does not alter
    # any intercept-inclusive segment OLS RSS or the financial input array.
    x, target = z[:-1] - z[:-1].mean(), z[1:] - z[1:].mean()
    prefix = [np.r_[0., np.cumsum(v)] for v in (x, target, x*x, target*target, x*target)]

    def costs(first, stop):
        first, stop = np.broadcast_arrays(np.asarray(first, dtype=np.int64),
                                         np.asarray(stop, dtype=np.int64))
        length = stop-first
        sx, sy, xx, yy, xy = [v[stop]-v[first] for v in prefix]
        sxx = xx - sx*sx/length
        syy = yy - sy*sy/length
        sxy = xy - sx*sy/length
        with np.errstate(divide='ignore', invalid='ignore'):
            explained = sxy*sxy/sxx
            rss = syy-explained
            cancellation_tolerance = 64*np.finfo(float).eps*np.maximum.reduce((np.abs(syy), np.abs(explained), np.ones_like(rss)))
            x_tolerance = 64*np.finfo(float).eps*np.maximum.reduce((np.abs(xx), np.abs(sx*sx/length), np.ones_like(sxx)))
        suspect = (~np.isfinite(rss) | (rss <= cancellation_tolerance)
                   | (sxx <= x_tolerance))
        for flat_index in np.flatnonzero(suspect):
            first_i, stop_i = int(first.flat[flat_index]), int(stop.flat[flat_index])
            raw_x, raw_y = y[first_i:stop_i], y[first_i+1:stop_i+1]
            centered_x = (raw_x-raw_x.mean())/scale
            centered_y = (raw_y-raw_y.mean())/scale
            # Sufficient-sum subtraction can erase a genuinely positive tiny
            # variance. Recompute suspect segments directly instead of using
            # an unregistered variance floor/positive-RSS rejection threshold.
            matrix = np.column_stack((np.ones(len(centered_x)), centered_x))
            if np.linalg.matrix_rank(matrix) < 2:
                sxx.flat[flat_index], rss.flat[flat_index] = 0., 0.
                continue
            direct_sxx = float(centered_x @ centered_x)
            residual = centered_y - (centered_x @ centered_y / direct_sxx)*centered_x
            direct_rss = float(residual @ residual)
            sxx.flat[flat_index], rss.flat[flat_index] = direct_sxx, direct_rss
        with np.errstate(divide='ignore', invalid='ignore'):
            valid = (length >= minimum) & (sxx > 0) & (rss > 0) & np.isfinite(rss)
            value = length*np.log(rss/length)
        return np.where(valid, value, np.inf)

    endpoints = np.arange(M+1)
    one = np.full(M+1, np.inf)
    one[minimum:] = costs(np.zeros(M-minimum+1, dtype=int), endpoints[minimum:])
    candidates = []
    two = None
    last_cuts = None
    last_costs = None

    def earliest_partition(k, ceiling):
        """Apply tolerance once to whole partitions, not at each DP layer."""
        if k == 0:
            return float(one[M]), ()
        if k == 1:
            cuts = np.arange(minimum, M-minimum+1)
            values = one[cuts]+costs(cuts, M)
            eligible = np.flatnonzero(values <= ceiling)
            chosen = int(eligible[0])
            return float(values[chosen]), (int(cuts[chosen]),)
        eligible_last = np.flatnonzero(two[last_cuts]+last_costs <= ceiling)
        choices = []
        for j in eligible_last:
            last = int(last_cuts[j])
            first = np.arange(minimum, last-minimum+1)
            values = one[first]+costs(first, last)+last_costs[j]
            eligible_first = np.flatnonzero(values <= ceiling)
            chosen = int(eligible_first[0])
            choices.append(((int(first[chosen]), last), float(values[chosen])))
        cuts, actual = min(choices)
        return actual, cuts

    def record(k, minimum_cost):
        if math.isfinite(float(minimum_cost)):
            cost, cuts = earliest_partition(k, float(minimum_cost)+tolerance)
            candidates.append({'k': k, 'cost': cost,
                               'bic': float(cost+(3+4*k)*math.log(M)), 'cuts': list(cuts),
                               'minimum_cost': float(minimum_cost),
                               'minimum_bic': float(minimum_cost+(3+4*k)*math.log(M))})
    record(0, one[M])
    if maximum >= 1 and M >= 2*minimum:
        two = np.full(M+1, np.inf)
        stops = list(range(2*minimum, M-minimum+1))
        if M not in stops:
            stops.append(M)
        for stop in stops:
            cuts = np.arange(minimum, stop-minimum+1)
            values = one[cuts] + costs(cuts, stop)
            best = float(values.min())
            if math.isfinite(best):
                two[stop] = best
        record(1, two[M])
        if maximum >= 2 and M >= 3*minimum:
            last_cuts = np.arange(2*minimum, M-minimum+1)
            last_costs = costs(last_cuts, M)
            values = two[last_cuts] + last_costs
            best = float(values.min())
            if math.isfinite(best):
                record(2, best)
    if not candidates:
        raise CalibrationError('NO_ADMISSIBLE_PARTITION', {'M': M, 'min_segment': minimum})
    best = min(r['minimum_bic'] for r in candidates)
    selected = min((r for r in candidates if r['minimum_bic'] <= best+tolerance), key=lambda r: r['k'])
    selected_cost, selected_cuts = earliest_partition(selected['k'], best+tolerance-(3+4*selected['k'])*math.log(M))
    cuts = list(selected_cuts)
    return dict(cuts=cuts, segment_lengths=np.diff([0]+cuts+[M]).astype(int).tolist(),
                bic_candidates=candidates, selected_bic=float(selected_cost+(3+4*selected['k'])*math.log(M)), selected_k=selected['k'],
                M=M, n=len(y), min_segment=minimum, cap_reached=selected['k'] == maximum,
                descriptive_only=True, transition_intervals=list(zip([0]+cuts, cuts+[M])),
                input_scale=scale)
