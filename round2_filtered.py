"""Frozen post-result FHS and GARCH-scaled peak-headroom POT.

Source-free: callers supply positions and dates. No files, downloads, tuning,
fallback forecasts or persisted global state are used by this module.
"""
import hashlib
import math
import warnings

import numpy as np

from conditional_features import completed_training_indices, refit_origin
from conditional_study import StudyConfig


class FilteredFitError(ValueError):
    def __init__(self, code, message, detail=None):
        super().__init__(message)
        self.code = code
        self.detail = {} if detail is None else detail
        self.failure_context = {}
        self.partial_forecast = {}


def _fail(code, message, detail=None):
    raise FilteredFitError(code, message, detail)


def variance_next(variance, residual, omega, alpha, beta):
    """One explicit GARCH(1,1) step, scalar or broadcast array."""
    v = np.asarray(variance, dtype=float)
    e = np.asarray(residual, dtype=float)
    if (not np.isfinite(v).all() or np.any(v <= 0) or
            not np.isfinite(e).all() or
            not all(math.isfinite(float(p)) for p in (omega, alpha, beta)) or
            omega <= 0 or alpha < 0 or beta < 0):
        _fail('INVALID_VARIANCE_STATE', 'finite positive variance and valid parameters required')
    with np.errstate(over='raise', invalid='raise'):
        try:
            out = omega+alpha*e*e+beta*v
        except FloatingPointError as error:
            _fail('VARIANCE_OVERFLOW', str(error))
    if not np.isfinite(out).all() or np.any(out <= 0):
        _fail('INVALID_VARIANCE_STATE', 'nonfinite or nonpositive updated variance')
    return float(out) if out.ndim == 0 else out


def simulate_peak_headrooms(anchor, variance, mu, omega, alpha, beta, draws):
    """Reanchor native incremental paths and retain maximum including h=0."""
    z = np.asarray(draws, dtype=float)
    if (z.ndim != 2 or not z.shape[0] or not z.shape[1] or
            not np.isfinite(z).all() or not math.isfinite(float(anchor)) or
            not math.isfinite(float(mu))):
        _fail('INVALID_PATH_INPUT', 'finite nonempty residual paths and anchor required')
    v = np.full(z.shape[0], float(variance))
    level = np.full(z.shape[0], float(anchor))
    floor = abs(float(anchor))
    peak = np.full(z.shape[0], floor)
    # Validate initial variance even when omega/alpha/beta will not be needed.
    variance_next(v, np.zeros(len(v)), omega, alpha, beta)
    try:
        with np.errstate(over='raise', invalid='raise'):
            for h in range(z.shape[1]):
                residual = np.sqrt(v)*z[:, h]
                level += mu+residual
                peak = np.maximum(peak, np.abs(level))
                if h+1 < z.shape[1]:
                    v = variance_next(v, residual, omega, alpha, beta)
            result = peak-floor
    except FloatingPointError as error:
        _fail('PATH_OVERFLOW', str(error))
    if not np.isfinite(result).all() or np.any(result < 0):
        _fail('INVALID_PATH_OUTPUT', 'finite nonnegative path headrooms required')
    return result


def corrected_quantile(values, numerator=19, denominator=20):
    """Corrected integer rank ceil((M+1)*19/20), without interpolation."""
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or not y.size or not np.isfinite(y).all():
        _fail('INVALID_QUANTILE_INPUT', 'finite nonempty quantile sample required')
    if (isinstance(numerator, bool) or isinstance(denominator, bool) or
            not isinstance(numerator, int) or not isinstance(denominator, int) or
            not 0 < numerator < denominator):
        _fail('INVALID_RANK', 'proper positive integer quantile fraction required')
    rank = ((len(y)+1)*numerator+denominator-1)//denominator
    if rank > len(y):
        _fail('UNAVAILABLE_RANK', 'corrected empirical rank unavailable')
    return float(np.partition(y, rank-1)[rank-1])


def pot_excesses(normalized):
    """Fixed top-ten-percent threshold, strict exceedances and min20 gate."""
    y = np.asarray(normalized, dtype=float)
    if (y.ndim != 1 or not y.size or not np.isfinite(y).all() or
            np.any(y < 0)):
        _fail('INVALID_POT_INPUT', 'finite nonnegative peak-headroom sample required')
    n = len(y)
    k = n//10
    if k < 20:
        _fail('POT_STRUCTURAL_NA', 'POT structurally unavailable: top ten percent has fewer than20 rows',
              {'window': n, 'nominal_tail_count': k})
    u = float(np.partition(y, n-k-1)[n-k-1])
    excess = y[y > u]-u
    count = len(excess)
    if count < 20 or not count/n > .05:
        _fail('POT_INADEQUATE_TAIL', 'POT needs at least20 strict exceedances and tail fraction above.05',
              {'window': n, 'nominal_tail_count': k, 'threshold': u, 'tail_count': count})
    return dict(threshold=u, excesses=excess, tail_count=count,
                nominal_tail_count=k, tail_fraction=count/n, window=n)


def gpd_nll(parameters, excesses):
    """Zero-location GPD likelihood with the frozen xi>-.5 gate."""
    p = np.asarray(parameters, dtype=float)
    y = np.asarray(excesses, dtype=float)
    if (p.shape != (2,) or not np.isfinite(p).all() or p[0] <= -.5 or
            y.ndim != 1 or not y.size or not np.isfinite(y).all() or np.any(y <= 0)):
        return math.inf
    xi, log_beta = map(float, p)
    try:
        beta = math.exp(log_beta)
        if not math.isfinite(beta) or beta <= 0:
            return math.inf
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            if abs(xi) < 1e-7:
                value = len(y)*log_beta+float(np.sum(y/beta))
            else:
                support = 1.+xi*y/beta
                if np.any(support <= 0):
                    return math.inf
                value = len(y)*log_beta+(1.+1./xi)*float(np.sum(np.log1p(xi*y/beta)))
    except (OverflowError, FloatingPointError, ZeroDivisionError):
        return math.inf
    return value if math.isfinite(value) else math.inf


def gpd_quantile(threshold, xi, beta, tail_fraction, tau=.95):
    if (not all(math.isfinite(float(p)) for p in (threshold, xi, beta, tail_fraction, tau)) or
            threshold < 0 or xi <= -.5 or beta <= 0 or
            not 0 < tau < 1 or not 1.-tau < tail_fraction <= 1):
        _fail('INVALID_GPD_QUANTILE', 'valid GPD support and target above the threshold required')
    ratio = tail_fraction/(1.-tau)
    try:
        extra = beta*math.log(ratio) if abs(xi) < 1e-7 else beta/xi*math.expm1(xi*math.log(ratio))
        value = threshold+extra
    except (OverflowError, ZeroDivisionError):
        _fail('GPD_QUANTILE_OVERFLOW', 'nonfinite extrapolated quantile')
    if not math.isfinite(value) or value < threshold:
        _fail('INVALID_GPD_QUANTILE', 'nonfinite or below-threshold extrapolated quantile')
    if abs(xi) >= 1e-7 and not 1.+xi*(value-threshold)/beta > 0:
        _fail('INVALID_GPD_SUPPORT', 'quantile outside GPD support')
    return float(value)


def fit_peak_pot(normalized):
    """One Nelder-Mead run; failures carry all available tail diagnostics."""
    from scipy.optimize import minimize
    detail = pot_excesses(normalized)
    excess = detail.pop('excesses')
    initial = np.array([.1, math.log(float(np.mean(excess)))])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        result = minimize(gpd_nll, initial, args=(excess,), method='Nelder-Mead',
                          options={'maxiter': 3000, 'xatol': 1e-8, 'fatol': 1e-8})
    detail['warnings'] = [{'category': w.category.__name__, 'message': str(w.message)} for w in caught]
    detail['optimizer'] = dict(method='Nelder-Mead', success=bool(result.success),
                               status=int(result.status), message=str(result.message),
                               iterations=int(result.nit), evaluations=int(result.nfev),
                               objective=float(result.fun), initial=initial.tolist())
    if not result.success or not math.isfinite(float(result.fun)) or not np.isfinite(result.x).all():
        _fail('POT_OPTIMIZER_FAILED', 'single POT optimizer failed', detail)
    xi = float(result.x[0])
    try:
        beta = math.exp(float(result.x[1]))
    except OverflowError:
        _fail('POT_INVALID_PARAMETERS', 'nonfinite fitted POT scale', detail)
    if not math.isfinite(beta) or beta <= 0 or xi <= -.5 or not math.isfinite(gpd_nll(result.x, excess)):
        _fail('POT_INVALID_PARAMETERS', 'invalid fitted POT support or regularity gate', detail)
    detail.update(xi=xi, beta=beta)
    detail['quantile'] = gpd_quantile(detail['threshold'], xi, beta, detail['tail_fraction'])
    return detail


def _array_hash(values):
    return hashlib.sha256(np.asarray(values, dtype='<f8').tobytes()).hexdigest()


def _fit_garch(increments):
    from arch import arch_model
    delta = np.asarray(increments, dtype=float)
    try:
        with np.errstate(over='raise', invalid='raise'):
            rms = float(np.sqrt(np.mean(delta*delta)))
    except FloatingPointError as error:
        _fail('GARCH_INVALID_SCALE', str(error))
    if not math.isfinite(rms) or rms <= 0:
        _fail('GARCH_INVALID_SCALE', 'finite positive training increment RMS required')
    fitting_error = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            model = arch_model(delta/rms, mean='Constant', vol='GARCH', p=1, o=0,
                               q=1, dist='normal', rescale=False)
            fit = model.fit(update_freq=0, disp='off', options={'maxiter': 300, 'ftol': 1e-8})
        except Exception as error:
            fitting_error = error
    warning_log = [{'category': w.category.__name__, 'message': str(w.message)} for w in caught]
    if fitting_error is not None:
        code = (type(fitting_error).__name__ if isinstance(fitting_error, (TimeoutError, MemoryError))
                else 'GARCH_OPTIMIZER_ERROR')
        _fail(code, str(fitting_error),
              dict(normalization_rms=rms, warnings=warning_log,
                   exception_type=type(fitting_error).__name__))
    status = fit.optimization_result
    params = {key: float(fit.params[key]) for key in ('mu', 'omega', 'alpha[1]', 'beta[1]')}
    v = np.asarray(fit.conditional_volatility, dtype=float)**2*rms*rms
    residuals = np.asarray(fit.std_resid, dtype=float)
    native = dict(mu=params['mu']*rms, omega=params['omega']*rms*rms,
                  alpha=params['alpha[1]'], beta=params['beta[1]'])
    metadata = dict(normalization_rms=rms, normalized_parameters=params,
                    native_parameters=native,
                    warnings=warning_log,
                    optimizer=dict(convergence_flag=int(fit.convergence_flag),
                                   status=int(status.status), message=str(status.message),
                                   iterations=int(status.nit), evaluations=int(status.nfev),
                                   objective=float(status.fun)),
                    parameters_sha256=_array_hash(list(params.values())),
                    residual_pool_sha256=_array_hash(residuals),
                    conditional_variance_sha256=_array_hash(v),
                    historical_volatility_is_in_sample_at_refit=True)
    if (fit.convergence_flag != 0 or not all(math.isfinite(p) for p in native.values()) or
            native['omega'] <= 0 or native['alpha'] < 0 or native['beta'] < 0 or
            native['alpha']+native['beta'] > 1.+1e-10 or
            v.shape != delta.shape or residuals.shape != delta.shape or
            not np.isfinite(v).all() or np.any(v <= 0) or not np.isfinite(residuals).all()):
        _fail('GARCH_FIT_FAILED', 'single GARCH fit failed convergence or admissibility', metadata)
    metadata['persistence_boundary'] = native['alpha']+native['beta'] >= 1.-1e-10
    metadata['minimum_native_sigma'] = float(np.sqrt(np.min(v)))
    metadata['maximum_native_sigma'] = float(np.sqrt(np.max(v)))
    return native, v, residuals, metadata


def _headrooms(segment, horizon, window):
    peak = np.abs(segment[:window]).copy()
    for h in range(1, horizon+1):
        peak = np.maximum(peak, np.abs(segment[h:h+window]))
    return peak-np.abs(segment[:window])


def filtered_forecast(position, times, origins, config, method,
                      source_id='synthetic', checkpoint=None):
    """Complete declared segment, otherwise explicit failure and partial trace."""
    capacity = []
    refits = []
    refit_indices = []
    ids = np.asarray(origins)
    current_t = current_r = None
    try:
        if not isinstance(config, StudyConfig) or method not in ('FHS', 'PEAK_POT'):
            _fail('INVALID_CONFIGURATION', 'valid StudyConfig and filtered method required')
        raw = np.asarray(position)
        if (ids.ndim != 1 or not ids.size or ids.dtype.kind not in 'iu' or
                np.any(ids < 0) or np.any(np.diff(ids) != 1) or
                raw.ndim != 1 or not raw.size or ids[-1] >= len(raw)):
            _fail('INVALID_ORIGINS', 'contiguous in-range issue origins required')
        ids = ids.astype(np.int64)
        # The source-free forecaster cannot inspect or require future outcomes.
        # Their availability and validity belong to the independent scorer.
        stop = int(ids[-1])+1
        x = np.asarray(raw[:stop], dtype=float)
        dates = np.asarray(np.asarray(times)[:stop], dtype='datetime64[ns]')
        if (not np.isfinite(x).all() or dates.shape != x.shape or
                np.isnat(dates).any() or np.any(dates[1:] <= dates[:-1])):
            _fail('INVALID_SOURCE', 'finite observed positions with valid chronological times required')
        if method == 'PEAK_POT' and config.window//10 < 20:
            _fail('POT_STRUCTURAL_NA', 'POT structurally unavailable: top ten percent has fewer than20 rows',
                  {'window': config.window, 'nominal_tail_count': config.window//10})
        last_r = None
        for raw_t in ids:
            t = current_t = int(raw_t)
            r = current_r = refit_origin(t, int(ids[0]), config.refit_step)
            if r != last_r:
                if checkpoint is not None:
                    checkpoint(stage='filtered_refit', completed_origins=len(capacity))
                pool = completed_training_indices(r, config.horizon, config.window,
                                                  minimum_feature_index=0)
                a, b = int(pool[0]), int(pool[-1])
                if b+config.horizon != r or np.any(pool+config.horizon > r):
                    _fail('MATURITY_VIOLATION', 'unfinished filtered training labels')
                # This slice ends at r, never the actual future outcome.
                segment = x[a:r+1]
                increments = np.diff(segment)
                item = dict(refit_index=r, training_first_origin=a, training_last_origin=b,
                            training_count=len(pool), latest_label_end=b+config.horizon,
                            increment_first_end=a+1, increment_last_end=r,
                            increment_count=len(increments))
                try:
                    params, historical_v, residual_pool, info = _fit_garch(increments)
                except Exception as error:
                    if not isinstance(error, FilteredFitError):
                        error = FilteredFitError(type(error).__name__, str(error))
                    error.detail = dict(failed_refit=item, garch_failure=error.detail)
                    raise error
                item['garch'] = info
                variance_at_issue = float(historical_v[-1])
                last_observed = r
                residual_at_issue = float(x[r]-x[r-1]-params['mu'])
                if method == 'FHS':
                    seed_text = f'20261023|{source_id}|{config.horizon}|{config.window}|{r}'
                    seed = int.from_bytes(hashlib.sha256(seed_text.encode('utf-8')).digest()[:8], 'big')
                    draws = np.random.default_rng(seed).choice(residual_pool,
                                    size=(2048, config.horizon), replace=True)
                    item.update(scenarios=2048, seed=seed, seed_input=seed_text,
                                draws_sha256=_array_hash(draws),
                                sampling='iid with replacement; frozen within refit block')
                else:
                    headroom = _headrooms(segment, config.horizon, config.window)
                    normalized = headroom/np.sqrt(historical_v[:config.window])
                    try:
                        item['pot'] = fit_peak_pot(normalized)
                    except FilteredFitError as error:
                        error.detail = dict(failed_refit=item, pot_failure=error.detail)
                        raise
                    item['pot']['normalized_headroom_sha256'] = _array_hash(normalized)
                refits.append(item)
                last_r = r
            # Fixed coefficients, but observed issue state moves forward causally.
            for end in range(last_observed+1, t+1):
                variance_at_issue = variance_next(variance_at_issue, residual_at_issue,
                    params['omega'], params['alpha'], params['beta'])
                residual_at_issue = float(x[end]-x[end-1]-params['mu'])
            last_observed = t
            future_v = variance_next(variance_at_issue, residual_at_issue,
                                    params['omega'], params['alpha'], params['beta'])
            if method == 'FHS':
                simulated = simulate_peak_headrooms(float(x[t]), future_v, params['mu'],
                    params['omega'], params['alpha'], params['beta'], draws)
                head = corrected_quantile(simulated)
            else:
                head = math.sqrt(future_v)*max(0., item['pot']['quantile'])
            value = abs(float(x[t]))+head
            if not math.isfinite(value) or value < abs(float(x[t])):
                _fail('INVALID_FILTERED_CAPACITY', 'finite capacity above current-position floor required')
            capacity.append(value)
            refit_indices.append(r)
            if checkpoint is not None and (len(capacity) % 32 == 0 or len(capacity) == len(ids)):
                checkpoint(stage='filtered_issue', completed_origins=len(capacity))
        return dict(capacity=np.asarray(capacity), refits=refits,
                    refit_indices=np.asarray(refit_indices, dtype=np.int64), origins=ids.copy())
    except Exception as error:
        if not isinstance(error, FilteredFitError):
            error = FilteredFitError(type(error).__name__, str(error))
        error.failure_context.update(method=method, query_issue=current_t, refit_index=current_r,
                                     issued_origin_count=len(capacity), detail=error.detail)
        error.partial_forecast = dict(capacity=np.asarray(capacity), refits=refits.copy(),
                                      origins=ids[:len(capacity)].copy(),
                                      refit_indices=np.asarray(refit_indices, dtype=np.int64))
        raise error
