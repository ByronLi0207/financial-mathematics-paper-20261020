"""Source-free QRF definition, causality and failure-preservation oracles.

No temporary-file fixtures or financial data are used by these tests.
"""
import numpy as np
import pytest
from unittest.mock import patch

from conditional_study import StudyConfig
from round2_qrf import weights_from_leaves, weighted_quantile, qrf_forecast


def source(n=190):
    i = np.arange(n)
    return 20 * np.sin(i * .23) + i * .1, np.datetime64('2019-01-02') + i * np.timedelta64(7, 'D')


def config():
    return StudyConfig(horizon=6, window=40, refit_step=7, short_scale=3,
                       long_scale=26, nominal_gap_seconds=604800)


def test_all_original_leaf_weights_are_not_quantiles_of_tree_means():
    # Query leaf 1 contains rows 0,1; query leaf 3 contains rows 1,2,3.
    train_leaves = np.array([[1, 9], [1, 3], [2, 3], [2, 3]])
    weights = weights_from_leaves(train_leaves, np.array([1, 3]))
    np.testing.assert_allclose(weights, [1/4, 5/12, 1/6, 1/6], rtol=0, atol=1e-15)
    values = np.array([0., 10., 20., 100.])
    assert weighted_quantile(values, weights, .5) == 10.
    assert weighted_quantile(values, weights, .8) == 20.
    assert weighted_quantile(values, weights, .95) == 100.
    assert 100. > 130 / 3  # The larger of the two leaf means is only 130/3.


def test_leaf_distribution_does_not_replace_original_rows_by_bootstrap_counts():
    # A bootstrap sample [0,0,0,1] could construct this one-leaf partition.
    # The declared QRF ECDF nevertheless includes all four original members.
    weights = weights_from_leaves(np.ones((4, 1), dtype=int), np.array([1]))
    np.testing.assert_array_equal(weights, [.25, .25, .25, .25])
    assert weighted_quantile([0., 10., 20., 100.], weights, .95) == 100.
    assert weighted_quantile([0., 10., 20., 100.], [3., 1., 0., 0.], .95) == 10.


def test_duplicate_responses_and_zero_mass_use_cdf_left_inverse_without_interpolation():
    assert weighted_quantile([0., 0., 100.], [.48, .48, .04], .95) == 0.
    assert weighted_quantile([0., 10., 1e10], [.5, .5, 0.], 1.) == 10.
    assert weighted_quantile([100., 10., 0.], [1., 1., 2.], .5) == 0.


@pytest.mark.parametrize('values,weights,tau', [
    ([], [], .95), ([1.], [0.], .95), ([1.], [-1.], .95),
    ([1., 2.], [1.], .95), ([np.nan], [1.], .95),
    ([1.], [np.inf], .95), ([1.], [1.], 0.), ([1.], [1.], True),
])
def test_invalid_weighted_distribution_fails_without_inventing_a_quantile(values, weights, tau):
    with pytest.raises(ValueError):
        weighted_quantile(values, weights, tau)


def test_invalid_or_unoccupied_query_leaf_is_rejected():
    with pytest.raises(ValueError):
        weights_from_leaves(np.array([[1], [1]]), np.array([2]))
    with pytest.raises(ValueError):
        weights_from_leaves(np.array([[1.5], [1.5]]), np.array([1]))
    with pytest.raises(ValueError):
        weights_from_leaves(np.array([[1, 2]]), np.array([1]))


@pytest.mark.parametrize('level', [0., -12.5])
def test_constant_headroom_returns_current_floor_and_retains_mature_fit_receipt(level):
    _, times = source()
    x = np.full(len(times), level)
    result = qrf_forecast(x, times, np.arange(100, 110), config())
    np.testing.assert_array_equal(result['capacity'], np.full(10, abs(level)))
    np.testing.assert_array_equal(result['refit_indices'], [100]*7 + [107]*3)
    assert not result['capacity'].flags.writeable
    assert len(result['refits']) == 2
    for fit in result['refits']:
        assert fit['training_last_origin'] + 6 == fit['refit_index']
        assert fit['latest_label_end'] == fit['refit_index']
        assert fit['training_count'] == 40
        assert fit['fallback'] is False
        assert len(fit['feature_transform_sha256']) == 64
        assert len(fit['forest_leaf_partition_sha256']) == 64


def test_known_linear_path_has_exact_nonnegative_headroom_six():
    _, times = source()
    x = np.arange(len(times), dtype=float)
    result = qrf_forecast(x, times, np.arange(100, 110), config())
    np.testing.assert_array_equal(result['capacity'], np.arange(106., 116.))


def test_full_future_perturbation_cannot_change_reports_or_fit_fingerprints():
    x, times = source()
    x_original, times_original = x.copy(), times.copy()
    changed = x.copy()
    changed[111:] = 1e5 + np.arange(len(x) - 111)
    changed_times = times.copy()
    changed_times[111:] += np.timedelta64(9, 'D')
    origins = np.arange(100, 111)
    a = qrf_forecast(x, times, origins, config())
    b = qrf_forecast(changed, changed_times, origins, config())
    np.testing.assert_array_equal(a['capacity'], b['capacity'])
    np.testing.assert_array_equal(a['refit_indices'], b['refit_indices'])
    assert a['refits'] == b['refits']
    np.testing.assert_array_equal(x, x_original)
    np.testing.assert_array_equal(times, times_original)


def test_fixed_forest_seed_gives_identical_reports_and_fit_receipts():
    x, times = source()
    a = qrf_forecast(x, times, np.arange(100, 103), config())
    b = qrf_forecast(x, times, np.arange(100, 103), config())
    np.testing.assert_array_equal(a['capacity'], b['capacity'])
    assert a['refits'] == b['refits']


def test_checkpoint_failure_retains_only_issued_prefix_and_no_fallback():
    x, times = source()
    events = []
    def stop(**event):
        events.append(event)
        if event['stage'] == 'qrf_refit' and event['refit_index'] == 107:
            raise TimeoutError('synthetic worker stop')
    with pytest.raises(TimeoutError) as caught:
        qrf_forecast(x, times, np.arange(100, 111), config(), checkpoint=stop)
    error = caught.value
    assert error.failure_context['query_issue'] == 107
    assert error.failure_context['refit_index'] == 107
    assert error.failure_context['fallback'] is False
    np.testing.assert_array_equal(error.partial_forecast['origins'], np.arange(100, 107))
    assert len(error.partial_forecast['capacity']) == 7
    assert len(error.partial_forecast['refits']) == 1
    assert len(events) >= 2


def test_noncontiguous_origins_and_unavailable_training_features_fail_with_context():
    x, times = source()
    for origins in (np.array([100, 102]), np.arange(40, 43)):
        with pytest.raises(ValueError) as caught:
            qrf_forecast(x, times, origins, config())
        assert caught.value.failure_context['fallback'] is False
        assert len(caught.value.partial_forecast['capacity']) == 0


def test_failed_forest_fit_retains_attempted_mature_pool_instead_of_a_fake_report():
    x, times = source()
    # Simulate a numerical-library failure at the fitting boundary only.
    with patch('sklearn.ensemble.RandomForestRegressor.fit',
               side_effect=ValueError('synthetic numerical fit failure')):
        with pytest.raises(ValueError) as caught:
            qrf_forecast(x, times, np.arange(100, 103), config())
    context = caught.value.failure_context
    assert context['training_first_origin'] == 55
    assert context['training_last_origin'] == 94
    assert context['latest_label_end'] == 100
    assert context['training_count'] == 40
    assert context['response_scale'] > 0
    assert context['fallback'] is False
    assert len(caught.value.partial_forecast['capacity']) == 0
    assert caught.value.partial_forecast['refits'] == []
