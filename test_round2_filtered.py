"""Synthetic tests for the frozen exploratory GARCH-filtered reports."""
import numpy as np
import pytest
from unittest.mock import patch
import warnings

from conditional_study import StudyConfig
from round2_filtered import (
    FilteredFitError, corrected_quantile, variance_next,
    simulate_peak_headrooms, pot_excesses, gpd_nll, gpd_quantile,
    fit_peak_pot, filtered_forecast, _fit_garch,
)


def test_manual_variance_recursion():
    assert variance_next(4., -3., .5, .2, .7) == pytest.approx(5.1)


def test_simulated_peak_is_path_maximum_at_signed_anchor_and_includes_h0():
    draws = np.array([[1., -1.], [-1., -1.], [0., 0.]])
    # Constant variance 4 and drift 0: signed -3 becomes [-3,-1,-3],
    # [-3,-5,-7], [-3,-3,-3]; only the second path needs headroom.
    got = simulate_peak_headrooms(-3., 4., 0., 4., 0., 0., draws)
    np.testing.assert_array_equal(got, [0., 4., 0.])
    # An endpoint-only implementation would miss the intermediate +5 peak.
    got = simulate_peak_headrooms(3., 4., 0., 4., 0., 0., np.array([[1., -2.]]))
    np.testing.assert_array_equal(got, [2.])


def test_corrected_quantile_rank_and_unavailable_rank():
    assert corrected_quantile(np.arange(1., 21.)) == 20.
    with pytest.raises(FilteredFitError, match='unavailable'):
        corrected_quantile(np.arange(1., 6.))


def test_strict_pot_threshold_ties_and_structural_small_window():
    detail = pot_excesses(np.arange(260.))
    assert detail['threshold'] == 233.
    assert detail['tail_count'] == 26
    np.testing.assert_array_equal(detail['excesses'], np.arange(1., 27.))
    with pytest.raises(FilteredFitError, match='strict exceedances'):
        pot_excesses(np.r_[np.arange(234.), np.repeat(233., 26)])
    with pytest.raises(FilteredFitError, match='structurally'):
        pot_excesses(np.arange(52.))


def test_gpd_exponential_limit_and_support_gate():
    y = np.array([1., 2., 3.])
    assert gpd_nll(np.array([0., np.log(2.)]), y) == pytest.approx(3*np.log(2.)+3.)
    assert gpd_quantile(4., 0., 2., .1) == pytest.approx(4.+2.*np.log(2.))
    assert gpd_quantile(4., 1e-9, 2., .1) == pytest.approx(4.+2.*np.log(2.))
    assert np.isinf(gpd_nll(np.array([-.5, np.log(2.)]), y))
    assert np.isinf(gpd_nll(np.array([-.4, np.log(.1)]), y))
    with pytest.raises(FilteredFitError):
        gpd_quantile(4., .1, 2., .05)


def test_one_pot_fit_retains_optimizer_and_finite_tail():
    # Deterministic exponential quantiles, not a financial sample.
    u = (np.arange(720)+.5)/720
    fit = fit_peak_pot(-np.log1p(-u))
    assert fit['tail_count'] == 72
    assert fit['optimizer']['success']
    assert fit['optimizer']['method'] == 'Nelder-Mead'
    assert fit['xi'] > -.5
    assert np.isfinite(fit['quantile']) and fit['quantile'] > fit['threshold']


def _synthetic(count=600):
    rng = np.random.default_rng(20261023)
    shocks = rng.standard_normal(count)
    delta = np.empty(count)
    v = 1.
    for j, z in enumerate(shocks):
        delta[j] = np.sqrt(v)*z
        v = .2+.1*delta[j]**2+.7*v
    x = np.r_[0., np.cumsum(delta)]
    times = np.datetime64('2020-01-01')+np.arange(len(x))*np.timedelta64(1, 'h')
    return x, times


def test_real_garch_future_perturbation_and_frozen_issue_state():
    x, times = _synthetic()
    cfg = StudyConfig(6, 260, 4, 6, 26, 3600)
    origins = np.arange(400, 408)
    got = filtered_forecast(x, times, origins, cfg, 'FHS', source_id='synthetic-causal')
    altered = x.copy()
    altered[408:] += np.arange(len(x)-408)*100.
    shifted = times.copy()
    shifted[408:] += np.arange(1, len(x)-407)*np.timedelta64(1, 'h')
    again = filtered_forecast(altered, shifted, origins, cfg, 'FHS', source_id='synthetic-causal')
    np.testing.assert_array_equal(got['capacity'], again['capacity'])
    np.testing.assert_array_equal(got['refit_indices'], [400]*4+[404]*4)
    assert got['refits'] == again['refits']
    assert np.all(got['capacity'] >= np.abs(x[origins]))
    assert len(got['refits']) == 2
    for item in got['refits']:
        assert item['latest_label_end'] == item['refit_index']
        assert item['increment_count'] == 265
        assert item['training_count'] == 260
        assert item['garch']['optimizer']['convergence_flag'] == 0


def test_nonfinite_source_fails_and_w52_is_rejected_before_filter_fit():
    x, times = _synthetic()
    x[1] = np.nan
    with pytest.raises(FilteredFitError, match='finite'):
        filtered_forecast(x, times, np.arange(400, 403), StudyConfig(6, 260, 4, 6, 26, 3600), 'FHS')
    clean, times = _synthetic()
    with pytest.raises(FilteredFitError, match='structurally') as caught:
        filtered_forecast(clean, times, np.arange(400, 403), StudyConfig(6, 52, 4, 6, 26, 3600), 'PEAK_POT')
    assert caught.value.failure_context['issued_origin_count'] == 0
    assert caught.value.partial_forecast['capacity'].size == 0
    assert caught.value.partial_forecast['refits'] == []


def test_peak_pot_full_future_perturbation():
    x, times = _synthetic(1100)
    cfg = StudyConfig(6, 720, 4, 6, 26, 3600)
    origins = np.arange(900, 908)
    got = filtered_forecast(x, times, origins, cfg, 'PEAK_POT')
    altered = x.copy()
    altered[908:] += np.arange(len(x)-908)*100.
    shifted = times.copy()
    shifted[908:] += np.arange(1, len(x)-907)*np.timedelta64(1, 'h')
    again = filtered_forecast(altered, shifted, origins, cfg, 'PEAK_POT')
    np.testing.assert_array_equal(got['capacity'], again['capacity'])
    assert got['refits'] == again['refits']
    assert all(item['pot']['tail_count'] >= 20 for item in got['refits'])


def test_failed_garch_retains_training_bounds_without_shortening_cell():
    x, times = _synthetic()
    x[:] = 3.
    with pytest.raises(FilteredFitError) as caught:
        filtered_forecast(x, times, np.arange(400, 408),
                          StudyConfig(6, 260, 4, 6, 26, 3600), 'FHS')
    error = caught.value
    assert error.code == 'GARCH_INVALID_SCALE'
    failed = error.failure_context['detail']['failed_refit']
    assert failed['training_first_origin'] == 135
    assert failed['training_last_origin'] == 394
    assert failed['latest_label_end'] == 400
    assert failed['increment_count'] == 265
    assert error.partial_forecast['capacity'].size == 0


@pytest.mark.parametrize('method', ['FHS', 'PEAK_POT'])
def test_future_change_inside_refit_block_preserves_earlier_issues(method):
    x, times = _synthetic(1100)
    cfg = StudyConfig(6, 720, 4, 6, 26, 3600)
    origins = np.arange(900, 908)
    original = filtered_forecast(x, times, origins, cfg, method)
    changed = x.copy()
    changed[902:] += .01*np.arange(1, len(x)-901)
    again = filtered_forecast(changed, times, origins, cfg, method)
    np.testing.assert_array_equal(original['capacity'][:2], again['capacity'][:2])
    assert original['refits'][0] == again['refits'][0]
    # Later observed state is genuinely allowed to affect later issue reports.
    assert np.any(original['capacity'][2:] != again['capacity'][2:])


@pytest.mark.parametrize('method', ['FHS', 'PEAK_POT'])
def test_unobserved_nan_nat_and_absent_outcomes_cannot_affect_reports(method):
    x, times = _synthetic(1100)
    cfg = StudyConfig(6, 720, 4, 6, 26, 3600)
    origins = np.arange(900, 908)
    full = filtered_forecast(x, times, origins, cfg, method)
    invalid_future = x.copy()
    invalid_dates = times.copy()
    invalid_future[908:] = np.nan
    invalid_dates[908:] = np.datetime64('NaT')
    future = filtered_forecast(invalid_future, invalid_dates, origins, cfg, method)
    prefix = filtered_forecast(x[:908], times[:908], origins, cfg, method)
    for result in (future, prefix):
        np.testing.assert_array_equal(full['capacity'], result['capacity'])
        np.testing.assert_array_equal(full['refit_indices'], result['refit_indices'])
        assert full['refits'] == result['refits']


@pytest.mark.parametrize('exception_type', [TimeoutError, MemoryError])
def test_interrupted_filter_preserves_attempted_mature_pool_without_retry(exception_type):
    x, times = _synthetic()
    with patch('round2_filtered._fit_garch', side_effect=exception_type('synthetic interruption')) as fit:
        with pytest.raises(FilteredFitError) as caught:
            filtered_forecast(x, times, np.arange(400, 408),
                              StudyConfig(6, 260, 4, 6, 26, 3600), 'FHS')
    assert fit.call_count == 1
    assert caught.value.code == exception_type.__name__
    attempted = caught.value.failure_context['detail']['failed_refit']
    assert attempted['refit_index'] == 400
    assert attempted['training_first_origin'] == 135
    assert attempted['latest_label_end'] == 400
    assert caught.value.partial_forecast['capacity'].size == 0


@pytest.mark.parametrize('exception_type', [TimeoutError, MemoryError])
def test_interrupted_arch_fit_keeps_actual_warning_and_original_exception_code(exception_type):
    def interrupt(*args, **kwargs):
        warnings.warn('warning before synthetic interruption', RuntimeWarning)
        raise exception_type('synthetic interruption')
    with patch('arch.arch_model') as factory:
        factory.return_value.fit.side_effect = interrupt
        with pytest.raises(FilteredFitError) as caught:
            _fit_garch(np.array([1., -1., 2., -2.]))
    assert factory.return_value.fit.call_count == 1
    assert caught.value.code == exception_type.__name__
    assert caught.value.detail['exception_type'] == exception_type.__name__
    assert caught.value.detail['warnings'] == [
        {'category': 'RuntimeWarning', 'message': 'warning before synthetic interruption'}]
