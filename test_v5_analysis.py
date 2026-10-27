"""Predeclared, deterministic checks for the v5 exploratory analyses."""
from decimal import Decimal
import numpy as np
import pytest

import v5_analysis as v5


def test_clock_blocks_are_chosen_without_any_outcome():
    blocks = v5.clock_blocks(11927, 18551, 24)
    assert [int(b[0]) for b in blocks] == [11927, 15215, 18527]
    assert all(len(b) == 24 for b in blocks)
    assert v5.clock_blocks(405, 681, 13)[-1].tolist() == list(range(665, 678))


def test_completed_and_deliberately_illegal_pools_have_exactly_h_future_labels():
    clean = v5.training_pool(100, 6, 40, False)
    illegal = v5.training_pool(100, 6, 40, True)
    assert (clean[0], clean[-1]) == (55, 94)
    assert (illegal[0], illegal[-1]) == (61, 100)
    assert np.count_nonzero(clean + 6 > 100) == 0
    assert np.count_nonzero(illegal + 6 > 100) == 6


def test_additive_gain_uses_the_original_reference_denominator():
    result = v5.loss_decomposition('100', '110', '90')
    assert Decimal(result['length_update_difference_percent_original_reference']) == 10
    assert Decimal(result['estimator_difference_percent_original_reference']) == -20
    assert Decimal(result['total_difference_percent_original_reference']) == -10
    assert Decimal(result['estimator_difference_percent_matched_reference']) != -20
    assert result['exact_additivity_residual_native'] == '0'


def test_no_silent_zero_reference_or_negative_loss():
    with pytest.raises(ValueError): v5.loss_decomposition('0', '1', '1')
    with pytest.raises(ValueError): v5.loss_decomposition('1', '-1', '1')


def test_motivating_selection_is_first_qualified_clock_origin():
    x = np.array([1., 1., 5., 1., 1., 8., 1.])
    found = v5.first_endpoint_peak_disagreement(x, [1, 2, 3], [4., 4., 4.], 3)
    assert found['origin'] == 1
    assert found['endpoint_absolute'] == 1.
    assert found['peak'] == 5.
    assert found['selection_rule'] == 'earliest eligible issue origin; absolute endpoint <= clean F report < sampled peak'


def test_no_qualified_motivating_window_is_explicit_na():
    assert v5.first_endpoint_peak_disagreement(np.ones(7), [1, 2], [2., 2.], 3) is None


def test_leakage_predictions_causal_pool_matches_existing_engine():
    from conditional_study import conditional_forecast, StudyConfig, historical_forecasts
    rng = np.random.default_rng(111)
    x = np.cumsum(rng.normal(size=190))
    dates = np.arange('2000-01-01', '2000-07-09', dtype='datetime64[D]')
    origins = np.arange(150, 155)
    config = StudyConfig(3, 52, 5, 6, 26, 86400)
    params = {'QR': .01, 'KNN': 20}
    clean, detail = v5.issue_block(x, dates, origins, config, params, False)
    for family in ('QR', 'KNN'):
        old = conditional_forecast(x, dates, origins, config, family, params[family])
        np.testing.assert_allclose(clean[family], old.capacities, rtol=0, atol=0)
    np.testing.assert_allclose(clean['F'], historical_forecasts(x, origins, config)['frozen_F'], rtol=0, atol=0)
    assert detail['immature_label_count'] == 0


def test_resource_probe_requests_only_pid_columns(monkeypatch):
    class Result:
        stdout = str(v5.os.getpid()) + '\n'
    def probe(args, **kwargs):
        assert args[-2:] == ['-o', 'pid=']
        return Result()
    monkeypatch.setattr(v5.subprocess, 'run', probe)
    guard = v5.Guard()
    guard()
    assert guard.maximum_observed_os_threads == 1

