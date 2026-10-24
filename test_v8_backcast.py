"""Constructed fixtures for the frozen WP5 prefix and descriptive HAC only."""
from fractions import Fraction
import copy
import json
import math
from pathlib import Path

import numpy as np
import pytest

import v8_backcast as module


def design():
    return json.loads((Path(__file__).parent / 'protocol/revision-v8/wp5-fixed-prefix-design.json').read_text())


def test_complete_original_geometry_and_purge():
    result = module.backcast_geometry(18576, design())
    assert result['status'] == 'READY'
    assert (result['evaluation_first'], result['evaluation_last'], result['evaluation_count']) == (3071, 10438, 7368)
    assert result['last_target_index'] == 10462
    assert result['last_target_index'] < result['original_validation_first']
    assert result['earliest_H24_W2880_training_origin'] == 168
    assert result['previous_retro_overlap_count'] == 1440
    assert result['previously_unscored'] is False


def test_unavailable_source_does_not_move_or_shorten_the_grid():
    result = module.backcast_geometry(10462, design())
    assert result['status'] == 'NA_SAMPLE_SIZE'
    assert result['reason'] == 'INCOMPLETE_DECLARED_TARGET_GRID'
    assert (result['evaluation_first'], result['evaluation_last'], result['evaluation_count']) == (3071, 10438, 7368)


@pytest.mark.parametrize('n', [True, 0, -3, 18576.0])
def test_geometry_rejects_invalid_lengths(n):
    with pytest.raises(ValueError):
        module.backcast_geometry(n, design())


@pytest.mark.parametrize('key,value', [('evaluation_first', 3072), ('evaluation_last', 10437), ('evaluation_count', 7367)])
def test_geometry_rejects_changed_declared_index_identity(key, value):
    d = design(); d['sample'][key] = value
    with pytest.raises(ValueError):
        module.backcast_geometry(18576, d)


def test_normal_dm_matches_independent_exact_rational_covariance():
    d = [0, 1, 3, 2, 8, -1, 4, 1]
    result = module.normal_dm(d, 2)
    n = len(d); mean = Fraction(sum(d), n)
    centered = [Fraction(x) - mean for x in d]
    # An independent rational computation checks divisor n and Bartlett lags.
    lrv = sum(x*x for x in centered) / n
    for lag in range(1, 3):
        gamma = sum(centered[j]*centered[j-lag] for j in range(lag, n)) / n
        lrv += 2 * (1-Fraction(lag, 3)) * gamma
    expected_t = float(mean) / math.sqrt(float(lrv)/n)
    assert result['status'] == 'OK'
    assert result['bandwidth'] == 2
    assert result['mean_difference'] == float(mean)
    assert result['lrv'] == pytest.approx(float(lrv), rel=2e-15)
    assert result['dm_t'] == pytest.approx(expected_t, rel=2e-15)
    assert result['dm_p'] == pytest.approx(math.erfc(abs(expected_t)/math.sqrt(2)), rel=2e-15)
    assert not any('hln' in key or 'holm' in key for key in result)


def test_normal_dm_opposite_difference_reverses_statistic_not_pvalue():
    values = np.array([1., -1., 3., 4., -2., 0., 5., 1.])
    left = module.normal_dm(values, 2); right = module.normal_dm(-values, 2)
    assert left['dm_t'] == -right['dm_t']
    assert left['dm_p'] == right['dm_p']


@pytest.mark.parametrize('value,status', [(0., 'IDENTICAL_LOSSES'), (3., 'ZERO_LONG_RUN_VARIANCE')])
def test_constant_differences_remain_undefined_without_epsilon_repair(value, status):
    result = module.normal_dm(np.full(12, value), 6)
    assert result['status'] == status
    assert result['dm_t'] is None and result['dm_p'] is None


@pytest.mark.parametrize('values,h', [([], 1), ([1., float('nan'), 3.], 1), ([[1., 2.]], 1), ([1., 2.], 2), ([1., 2.], True), ([1., 2., 3.], 0)])
def test_normal_dm_rejects_bad_inputs(values, h):
    with pytest.raises(ValueError):
        module.normal_dm(values, h)


def trace(losses, hits=None, start=3071):
    n = len(losses)
    return dict(origins=np.arange(start, start+n), pinball=np.array(losses, float),
                strict_breach=np.zeros(n, dtype=bool) if hits is None else np.array(hits))


def test_complete_pair_uses_full_common_grid_and_negative_favors_model():
    model = trace([1, 2, 1, 3, 2, 4, 1, 2], [1, 0, 0, 1, 0, 0, 0, 0])
    reference = trace([4, 5, 3, 6, 5, 7, 4, 5], [0, 0, 0, 1, 0, 0, 0, 0])
    result = module.compare_traces(model, reference, 2)
    assert result['status'] == 'COMPLETE'
    assert result['n'] == 8 and result['exact_shared_origins'] is True
    assert result['mean_model_loss'] == 2
    assert result['mean_reference_loss'] == 4.875
    assert result['relative_change_percent'] == 100*(2/4.875-1)
    assert result['model_breach_count'] == 2 and result['reference_breach_count'] == 1
    assert result['model_breach_rate'] == .25 and result['reference_breach_rate'] == .125
    assert result['dm']['mean_difference'] < 0


def test_zero_reference_mean_retains_absolute_loss_and_undefined_ratio():
    result = module.compare_traces(trace([1]*8), trace([0]*8), 2)
    assert result['relative_change_percent'] is None
    assert result['mean_model_loss'] == 1
    assert result['dm']['status'] == 'ZERO_LONG_RUN_VARIANCE'


@pytest.mark.parametrize('corruption', ['origin_shift', 'origin_gap', 'short_hit', 'bad_hit', 'negative_loss', 'nan_loss'])
def test_pair_rejects_misaligned_or_invalid_complete_trace(corruption):
    a = trace([1]*8); b = trace([2]*8)
    if corruption == 'origin_shift': b['origins'] += 1
    elif corruption == 'origin_gap': b['origins'][4] += 1
    elif corruption == 'short_hit': b['strict_breach'] = np.zeros(7)
    elif corruption == 'bad_hit': b['strict_breach'] = np.full(8, 2)
    elif corruption == 'negative_loss': b['pinball'][2] = -1
    else: b['pinball'][2] = float('nan')
    with pytest.raises(ValueError):
        module.compare_traces(a, b, 2)


def test_score_trace_preserves_ties_as_nonbreaches_and_tau_loss():
    score = module.score_trace(np.arange(3071,3074), [5.,5.,5.], [5.,4.,7.])
    assert score['n'] == 3
    assert score['strict_breach_count'] == 1
    assert score['strict_breach_rate'] == 1/3
    assert score['mean_loss'] == pytest.approx((.95+2*.05)/3, rel=1e-15)


def window_rows():
    rows = []
    for i, window in enumerate(('extra_full_prefix', 'previous_retro', 'original_inspected')):
        for reference in ('F_matched', 'F_rolling720'):
            rows.append(dict(window_name=window, method='QR33', horizon=6,
                reference=reference, status='COMPLETE', relative_change_percent=-20.
                if reference == 'F_matched' or i != 1 else 10.))
    return rows


def test_three_window_primary_rule_support_does_not_restore_independence():
    result = module.classify_three_windows(window_rows(), design())
    assert result['status'] == 'SUPPORT_WITH_LIMITS'
    assert result['matched_wins'] == 3
    assert result['rolling_signs'] == [-1, 1]
    assert result['fresh_independent_third_period'] is False
    assert result['independence_claim_status'] == 'FAIL_MISMATCH'
    assert result['previous_retro_overlap_count'] == 1440


@pytest.mark.parametrize('mutation', ['missing', 'failed', 'missing_scalar'])
def test_unavailable_required_cell_cannot_be_complete_case_support(mutation):
    rows = window_rows()
    if mutation == 'missing': rows.pop(0)
    elif mutation == 'failed': rows[0]['status'] = 'FAILED'
    else: rows[0]['relative_change_percent'] = None
    result = module.classify_three_windows(rows, design())
    assert result['status'] == 'INCONCLUSIVE'
    assert result['missing_comparisons'] == 1


@pytest.mark.parametrize('mutation', ['matched_tie', 'matched_loss', 'same_rolling_sign'])
def test_unfavorable_primary_result_cannot_be_rescued_by_secondary(mutation):
    rows = window_rows()
    if mutation == 'matched_tie': rows[0]['relative_change_percent'] = 0.
    elif mutation == 'matched_loss': rows[0]['relative_change_percent'] = 10.
    else: rows[3]['relative_change_percent'] = -20.
    rows += [dict(window_name='extra_full_prefix', method='QR4', horizon=24,
                 reference='F_matched', status='COMPLETE', relative_change_percent=-90.)]
    result = module.classify_three_windows(rows, design())
    assert result['status'] == 'MISMATCH'


def test_duplicate_primary_identity_is_an_error():
    rows = window_rows(); rows.append(copy.deepcopy(rows[0]))
    with pytest.raises(ValueError):
        module.classify_three_windows(rows, design())
