"""Constructed contracts for the predeclared final-merge decision rules.

These tests never read a financial source or fit a model. A change that counted
ties as wins, deleted missing cells, or accepted unmatured labels would fail.
"""
import importlib
import importlib.util
import math

import pytest


def api():
    assert importlib.util.find_spec('final_merge_wp2') is not None, 'WP2 decision/scoring adapter not implemented'
    return importlib.import_module('final_merge_wp2')


def test_fixed_split_supports_520_without_unmatured_labels():
    split = api().split_geometry(877, 6, 520)
    assert split == dict(validation_first=553, validation_last=604,
        evaluation_first=611, evaluation_last=870, first_training_origin=28,
        latest_validation_label_end=610, last_evaluation_label_end=876)


def test_insufficient_history_is_not_silently_shortened():
    with pytest.raises(ValueError, match='INSUFFICIENT'):
        api().split_geometry(870, 6, 520)


def test_fixed_denominator_missing_bounds_and_exact_threshold():
    a = api()
    assert a.screen([True]*8+[False]*2, 0.8)['status'] == 'SUPPORT'
    assert a.screen([True]*7+[False]*3, 0.8)['status'] == 'NOT_SUPPORT'
    r = a.screen([True]*7+[False]*2+[None], 0.8)
    assert r['status'] == 'NOT_TESTABLE'
    assert (r['planned'], r['complete'], r['lower'], r['upper']) == (10, 9, 0.7, 0.8)
    assert a.screen([True]*8+[None]*2, 0.8)['status'] == 'SUPPORT'


def test_primary_combination_requires_both_method_specific_p1_screens():
    a = api()
    assert a.primary_status('SUPPORT', 'SUPPORT', 'SUPPORT') == 'SUPPORT'
    assert a.primary_status('SUPPORT', 'NOT_SUPPORT', 'SUPPORT') == 'PARTLY'
    assert a.primary_status('NOT_SUPPORT', 'NOT_SUPPORT', 'NOT_SUPPORT') == 'NOT_SUPPORT'
    assert a.primary_status('SUPPORT', 'NOT_TESTABLE', 'NOT_SUPPORT') == 'NOT_TESTABLE'


def test_strict_monotonicity_rejects_ties_and_reversal():
    a = api()
    assert a.strict_decrease([3., 2., 1.]) is True
    assert a.strict_decrease([3., 2., 2.]) is False
    assert a.strict_decrease([3., 1., 2.]) is False
    assert a.strict_decrease([3., None, 1.]) is None


def test_hac_known_answer_and_undefined_cases():
    a = api()
    r = a.scalar_hac([1., 2., 3., 4.], 2)
    assert r['bandwidth'] == 2
    assert math.isclose(r['lrv'], 17/12, rel_tol=1e-14)
    assert math.isclose(r['mean_difference'], 2.5, rel_tol=1e-14)
    assert r['status'] == 'OK'
    assert a.scalar_hac([0.]*30, 6)['status'] == 'IDENTICAL_LOSSES'
    assert a.scalar_hac([2.]*30, 6)['status'] == 'ZERO_LONG_RUN_VARIANCE'


def test_separate_source_peak_floor_pinball_and_strict_breach():
    a = api()
    r = a.scalar_trace([2., -3., 4., 1., 5.], [0, 1], [4., 4.], 2)
    assert r['peak'] == [4., 4.]
    assert r['floor'] == [2., 3.]
    assert r['pinball'] == [0., 0.]
    assert r['strict_breach'] == [False, False]
    with pytest.raises(ValueError, match='FLOOR'):
        a.scalar_trace([2., -3., 4., 1., 5.], [0, 1], [1., 4.], 2)


def test_maturity_requires_exact_pool_and_feature_boundary():
    a = api()
    good = [dict(refit_index=553, training_first_origin=28,
        training_last_origin=547, training_count=520, latest_label_end=553)]
    assert a.check_maturity(good, 520, 6, conditional=True) == 1
    with pytest.raises(ValueError, match='MATURITY'):
        a.check_maturity([dict(good[0], latest_label_end=554)], 520, 6, conditional=True)
    with pytest.raises(ValueError, match='MATURITY'):
        a.check_maturity([dict(good[0], training_first_origin=27)], 520, 6, conditional=True)


@pytest.mark.parametrize('values', [[float('nan')], [True], []])
def test_invalid_screen_cells_rejected(values):
    # Booleans are allowed; a singleton True is valid, so use the rate argument
    # to exercise its distinct invalid-type branch without using financial data.
    if values == [True]:
        with pytest.raises(ValueError): api().screen(values, True)
    else:
        with pytest.raises(ValueError): api().screen(values, 0.8)
