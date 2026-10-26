"""Artificial-input tests only; never load a financial series or study driver."""
import importlib
import itertools
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import statsmodels.api as sm
from statsmodels.stats.diagnostic import breaks_hansen


def api():
    assert Path(__file__).with_name('v9_nonstationarity.py').exists(), 'v9 statistical implementation is absent'
    return importlib.import_module('v9_nonstationarity')


def design(**updates):
    d = dict(phi_bound=.999, garch_persistence_bound=.999,
             garch_maxiter=2000, garch_ftol=1e-9,
             minimum_segment_transitions=104, minimum_segment_fraction=.2,
             max_breaks=2, bic_tie_tolerance=1e-10,
             fourth_moment_margin=1e-8, bootstrap_repetitions=19,
             burn_in=200, master_entropy=2026102408, rng_namespace=9,
             diagnostic_stream_tag=0, score_correlation_condition_max=1e12)
    d.update(updates)
    return d


def artificial_ar(n=405, seed=104, intercept=2., phi=.35):
    rng = np.random.default_rng(seed)
    shocks = rng.standard_t(9, size=n) * np.sqrt(7 / 9)
    y = np.empty(n)
    y[0] = intercept / (1 - phi)
    for t in range(1, n):
        y[t] = intercept + phi * y[t - 1] + shocks[t]
    return y


def params(**updates):
    d = dict(intercept=0., phi=.3, omega=.1, alpha=.03, beta=.7, nu=9.)
    d.update(updates)
    return d


def test_hansen_matches_official_statistic_and_retains_scale_invariance():
    m = api()
    y = artificial_ar()
    official = breaks_hansen(sm.OLS(y[1:], sm.add_constant(y[:-1])).fit())[0]
    assert m.hansen_statistic(y) == pytest.approx(official, rel=2e-10)
    assert m.hansen_statistic(y * 1e9) == pytest.approx(official, rel=2e-10)


@pytest.mark.parametrize('y', [np.ones(405), [0., 1., np.nan, 3., 4.], np.arange(4.), np.zeros((3, 4))])
def test_hansen_bad_or_singular_samples_raise_diagnostic_error(y):
    m = api()
    with pytest.raises(m.CalibrationError):
        m.hansen_statistic(y)


def test_score_condition_limit_is_enforced_without_ridge():
    m = api()
    with pytest.raises(m.CalibrationError):
        m.hansen_statistic(artificial_ar(), condition_max=1.)


def test_finite_fourth_moment_is_distinct_from_finite_variance():
    m = api()
    good = m.moment_qualification(params())
    assert good['qualified'] and good['nu_gt4']
    assert good['kappa'] == pytest.approx(3 * 7 / 5)
    assert good['q4'] == pytest.approx(.03 ** 2 * (3 * 7 / 5) + 2 * .03 * .7 + .7 ** 2)
    low_df = m.moment_qualification(params(nu=3.))
    assert not low_df['qualified'] and not low_df['nu_gt4']
    assert low_df['kappa'] is None and low_df['q4'] is None
    persistent = m.moment_qualification(params(alpha=.2, beta=.79, nu=5.))
    assert persistent['nu_gt4'] and not persistent['qualified'] and persistent['q4'] > 1


@pytest.mark.parametrize('change', [dict(phi=1.), dict(omega=0.), dict(alpha=-.01), dict(beta=1.), dict(nu=2.), dict(nu=np.nan)])
def test_invalid_generation_parameters_are_not_regular(change):
    m = api()
    assert not m.moment_qualification(params(**change))['qualified']


def test_fit_uses_whole_level_scale_preserves_mean_and_segment_transition_coordinates():
    m = api()
    y = artificial_ar(n=701, seed=9, intercept=7., phi=.4)
    result = m.fit_ar_garch(y, design(), start=100, stop=500)
    z = y / y.std(ddof=0)
    x, target = z[100:500], z[101:501]
    centered_x, centered_y = x - x.mean(), target - target.mean()
    expected_phi = np.clip(centered_x @ centered_y / (centered_x @ centered_x), -.999, .999)
    expected_intercept = target.mean() - expected_phi * x.mean()
    p, d = result['params'], result['diagnostics']
    assert set(p) == {'intercept', 'phi', 'omega', 'alpha', 'beta', 'nu'}
    assert p['phi'] == pytest.approx(expected_phi)
    assert p['intercept'] == pytest.approx(expected_intercept)
    assert p['intercept'] > 1  # Would disappear if level mean were subtracted.
    assert d['input_scale'] == pytest.approx(y.std(ddof=0))
    assert d['residual_scale'] == pytest.approx((target - expected_intercept - expected_phi * x).std(ddof=0))
    assert d['transition_start'] == 100 and d['transition_stop'] == 500
    assert d['optimizer']['converged']
    assert p['alpha'] + p['beta'] <= .999 + 1e-8
    assert p['omega'] > 0 and p['nu'] > 2
    assert p['omega'] == pytest.approx(d['omega_standardized_residual_units'] * d['residual_scale']**2)


def test_fit_normalization_is_equivariant_under_positive_unit_change():
    m = api()
    y = artificial_ar(n=701, seed=43, intercept=4., phi=.2)
    original = m.fit_ar_garch(y, design())
    changed_units = m.fit_ar_garch(y * 1000, design())
    for name in params():
        assert changed_units['params'][name] == pytest.approx(original['params'][name], rel=2e-3, abs=2e-5)
    assert changed_units['diagnostics']['input_scale'] == pytest.approx(1000 * original['diagnostics']['input_scale'])


def test_ar_bound_is_profiled_and_boundary_fit_is_reported():
    m = api()
    rng = np.random.default_rng(923)
    y = np.empty(500)
    y[0] = 5.
    for t in range(1, len(y)):
        y[t] = .7 + 1.004 * y[t-1] + .2 * rng.standard_normal()
    r = m.fit_ar_garch(y, design())
    assert r['params']['phi'] == pytest.approx(.999, abs=1e-14)
    assert r['diagnostics']['status'] == 'BOUNDARY_FIT'
    assert r['diagnostics']['boundary_hits']['phi']


def test_explicit_garch_constraint_default_one_fit_and_failure_propagation(monkeypatch):
    m = api()
    from arch.univariate import ZeroMean
    calls = []
    def failed_fit(self, **kwargs):
        calls.append(kwargs)
        a, b = self.volatility.constraints()
        assert np.all(a @ np.array([.1, .1, .899]) - b >= -1e-12)
        assert np.any(a @ np.array([.1, .1, .9]) - b < -1e-5)
        return SimpleNamespace(convergence_flag=9, optimization_result=SimpleNamespace(success=False, status=9, message='artificial failure'))
    monkeypatch.setattr(ZeroMean, 'fit', failed_fit)
    with pytest.raises(m.CalibrationError) as caught:
        m.fit_ar_garch(artificial_ar(), design())
    assert caught.value.reason == 'GARCH_OPTIMIZATION_FAILED'
    assert len(calls) == 1 and 'starting_values' not in calls[0]
    assert calls[0]['options'] == {'maxiter': 2000, 'ftol': 1e-9}


def _brute_bic(y, minimum):
    z = y / y.std(ddof=0)
    M = len(y) - 1
    best = []
    for k in range(3):
        candidates = []
        for cuts in itertools.combinations(range(minimum, M - minimum + 1), k):
            ends = (0,) + cuts + (M,)
            if min(np.diff(ends)) < minimum:
                continue
            cost = 0.
            for first, stop in zip(ends[:-1], ends[1:]):
                x = np.column_stack((np.ones(stop-first), z[first:stop]))
                target = z[first+1:stop+1]
                e = target - x @ np.linalg.lstsq(x, target, rcond=None)[0]
                cost += (stop-first) * np.log(e @ e / (stop-first))
            candidates.append((cost + (3+4*k)*np.log(M), cuts))
        if candidates:
            best.append(min(candidates))
    return min(best)


def test_locator_matches_independent_global_integer_search():
    m = api()
    y = artificial_ar(n=34, seed=20)
    expected_bic, expected_cuts = _brute_bic(y, 7)
    r = m.locate_breaks(y, design(minimum_segment_transitions=7, minimum_segment_fraction=.1))
    assert tuple(r['cuts']) == expected_cuts
    assert r['selected_bic'] == pytest.approx(expected_bic, abs=2e-9)
    assert r['M'] == 33 and r['n'] == 34 and r['min_segment'] == 7
    assert sum(r['segment_lengths']) == 33
    assert len(r['bic_candidates']) == 3


def test_locator_tie_tolerance_applies_once_to_the_complete_partition():
    m = api()
    y = artificial_ar(n=34, seed=12)
    z, M, minimum, tolerance = y / y.std(), 33, 7, 1.
    costs = []
    for cuts in itertools.combinations(range(minimum, M-minimum+1), 2):
        ends = (0,) + cuts + (M,)
        if min(np.diff(ends)) < minimum:
            continue
        cost = 0.
        for first, stop in zip(ends[:-1], ends[1:]):
            x = np.column_stack((np.ones(stop-first), z[first:stop]))
            target = z[first+1:stop+1]
            residual = target-x @ np.linalg.lstsq(x, target, rcond=None)[0]
            cost += (stop-first)*np.log(residual @ residual/(stop-first))
        costs.append((cost, cuts))
    exact_best = min(x[0] for x in costs)
    expected = min(cuts for cost, cuts in costs if cost <= exact_best+tolerance)
    r = m.locate_breaks(y, design(minimum_segment_transitions=minimum,
                                minimum_segment_fraction=.1,
                                bic_tie_tolerance=tolerance))
    candidate = r['bic_candidates'][2]
    assert tuple(candidate['cuts']) == expected
    assert candidate['cost'] <= exact_best+tolerance+1e-9


def test_artificial_inserted_break_is_located_in_transition_units():
    m = api()
    rng = np.random.default_rng(31)
    y = np.r_[rng.normal(-8, .2, 203), rng.normal(8, .2, 202)]
    r = m.locate_breaks(y, design())
    assert len(r['cuts']) == 1
    assert abs(r['cuts'][0] - 202) <= 2
    assert all(x >= 104 for x in r['segment_lengths'])
    assert not r['cap_reached']


def test_two_variance_breaks_are_reported_with_the_cap_and_full_transition_census():
    m = api()
    rng = np.random.default_rng(79)
    y = np.r_[rng.normal(0, .1, 135), rng.normal(0, 8., 135), rng.normal(0, .1, 135)]
    r = m.locate_breaks(y, design())
    assert r['selected_k'] == 2 and r['cap_reached']
    assert abs(r['cuts'][0] - 134) <= 3 and abs(r['cuts'][1] - 269) <= 3
    assert r['transition_intervals'] == [(0, r['cuts'][0]), (r['cuts'][0], r['cuts'][1]), (r['cuts'][1], 404)]


def test_artificial_hourly_length_locator_needs_no_dense_square_matrix():
    m = api()
    r = m.locate_breaks(artificial_ar(n=8109, seed=82), design())
    assert r['M'] == 8108 and r['min_segment'] == 1622
    assert r['selected_k'] == 0


def test_no_legal_partition_and_zero_residual_variance_fail_closed():
    m = api()
    for y in (artificial_ar(n=104), np.arange(405.), np.ones(405)):
        with pytest.raises(m.CalibrationError):
            m.locate_breaks(y, design())


def test_near_deterministic_positive_noise_has_no_extra_variance_floor():
    m = api()
    rng = np.random.default_rng(240)
    y = np.zeros(405)
    for t in range(1, len(y)):
        y[t] = 1. + .9*y[t-1] + 1e-8*rng.standard_normal()
    r = m.locate_breaks(y, design())
    assert r['M'] == 404
    assert len(r['bic_candidates']) == 3
    assert all(np.isfinite(x['cost']) for x in r['bic_candidates'])


def test_nonregular_bootstrap_returns_unknown_without_importing_simulator(monkeypatch):
    m = api()
    def forbidden(*args, **kwargs):
        pytest.fail('nonregular null must not generate bootstrap paths')
    monkeypatch.setattr(importlib, 'import_module', forbidden)
    r = m.bootstrap_stability(artificial_ar(), params(nu=3.), 0, design())
    assert r['status'] == 'NONREGULAR_NULL'
    assert r['p_value'] is None and r['bootstrap_statistics'] == []


def test_known_null_bootstrap_reproducibility_and_inserted_break_rejection():
    m = api()
    rng = np.random.default_rng(177)
    y = np.r_[rng.normal(-9, .2, 150), rng.normal(9, .2, 151)]
    d = design(bootstrap_repetitions=39, burn_in=100)
    r = m.bootstrap_stability(y, params(phi=0., omega=1., alpha=0., beta=0., nu=9.), 4, d)
    repeated = m.bootstrap_stability(y, params(phi=0., omega=1., alpha=0., beta=0., nu=9.), 4, d)
    assert r['status'] == 'COMPLETE'
    assert r['B'] == 39 and len(r['bootstrap_statistics']) == 39
    assert r['p_value'] == (1+r['exceedances']) / 40
    assert r['p_value'] <= .05
    assert r['bootstrap_statistics'] == repeated['bootstrap_statistics']
    assert r['rng_initial_state'] == repeated['rng_initial_state']
    assert r['rng_final_state'] == repeated['rng_final_state']


@pytest.mark.parametrize('bad_path', ['nonfinite', 'missing_replicate', 'singular'])
def test_bootstrap_required_path_failure_never_becomes_a_p_value(monkeypatch, bad_path):
    m = api()
    import v9_switching
    def broken(params_, n, B, rng, burn_in, checkpoint=None):
        if bad_path == 'missing_replicate':
            return np.zeros((B-1, n))
        paths = np.vstack([artificial_ar(n=n, seed=j) for j in range(B)])
        if bad_path == 'nonfinite':
            paths[0, 0] = np.nan
        else:
            paths[-1] = 1.
        return paths
    monkeypatch.setattr(v9_switching, 'simulate_constant_paths', broken)
    with pytest.raises(m.CalibrationError) as caught:
        m.bootstrap_stability(artificial_ar(), params(), 0, design(bootstrap_repetitions=3))
    assert caught.value.reason in {'INVALID_BOOTSTRAP_PATH_INVENTORY', 'BOOTSTRAP_STATISTIC_FAILED'}


def test_bootstrap_checkpoint_cancellation_is_not_a_nonrejection():
    m = api()
    def stop(**kwargs):
        if kwargs['stage'] == 'bootstrap_statistic':
            raise TimeoutError('artificial deadline')
    with pytest.raises(TimeoutError, match='artificial deadline'):
        m.bootstrap_stability(artificial_ar(), params(), 0, design(bootstrap_repetitions=3), checkpoint=stop)

