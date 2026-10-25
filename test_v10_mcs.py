"""Artificial loss vectors only; no saved financial losses or actual MCS grids."""
import importlib
import importlib.util
import json
import warnings

import numpy as np
import pandas as pd
import pytest

from run_study import StudyStop
from run_v8_wp3 import DriverStop


def api():
    assert importlib.util.find_spec('v10_mcs') is not None, 'MCS wrapper is missing'
    return importlib.import_module('v10_mcs')


def design(reps=99):
    return dict(package='arch==8.0.0', size=.10, statistic='R', bootstrap='stationary',
                bootstrap_repetitions=reps, seed_prefix='v10-MCS-20261024|')


def identity(horizon=6):
    return dict(period='artificial_period', normalized_source='人工α', horizon=horizon, window=52)


def artificial_losses(n=256):
    rng = np.random.default_rng(4317)
    common = rng.exponential(1., n)
    return dict(good=common+.1*rng.random(n), poor=common+10.+.5*rng.random(n))


def test_real_arch_excludes_a_stochastically_different_clearly_poor_column():
    row = api().compute_mcs(artificial_losses(), identity(), design())
    assert row['status'] == 'COMPLETE'
    assert row['included'] == ['good'] and row['excluded'] == ['poor']
    assert row['pvalues']['poor'] <= .1 < row['pvalues']['good']
    assert row['n'] == 256 and row['block_size'] == 7
    assert row['seed'] == 4102530119
    assert row['diagnostics']['library_attempts'] == 1
    json.dumps(row, allow_nan=False)


def test_exact_duplicate_loss_classes_use_lexical_representative_and_unfold_all_labels(monkeypatch):
    m = api(); losses = artificial_losses(); actual = m.MCS; observed = []
    def observed_mcs(matrix, **kwargs):
        observed.append((matrix.copy(), dict(kwargs)))
        return actual(matrix, **kwargs)
    monkeypatch.setattr(m, 'MCS', observed_mcs)
    row = m.compute_mcs({'Z::same': losses['good'].copy(), 'M::poor': losses['poor'], 'A::good': losses['good']},
                        identity(), design())
    assert row['status'] == 'COMPLETE'
    assert row['method_ids'] == ['A::good', 'M::poor', 'Z::same']
    assert row['unique_loss_groups'] == [
        {'representative': 'A::good', 'members': ['A::good', 'Z::same']},
        {'representative': 'M::poor', 'members': ['M::poor']}]
    assert row['included'] == ['A::good', 'Z::same'] and row['excluded'] == ['M::poor']
    assert row['pvalues']['A::good'] == row['pvalues']['Z::same']
    assert len(observed) == 1 and observed[0][0].shape == (256, 2)
    np.testing.assert_array_equal(observed[0][0][:, 0], losses['good'])
    assert observed[0][1]['method'] == 'R' and observed[0][1]['bootstrap'] == 'stationary'


@pytest.mark.parametrize('single', [False, True])
def test_one_loss_class_is_analytic_and_never_constructs_the_library(single, monkeypatch):
    m = api()
    def forbidden(*args, **kwargs): raise AssertionError('analytic case must not call arch MCS')
    monkeypatch.setattr(m, 'MCS', forbidden)
    x = np.arange(1., 31.)
    losses = {'only': x} if single else {'z': x.copy(), 'a': x}
    row = m.compute_mcs(losses, identity(24), design())
    assert row['status'] == ('COMPLETE_SINGLE_METHOD' if single else 'COMPLETE_IDENTICAL_LOSSES')
    assert row['included'] == sorted(losses) and row['excluded'] == []
    assert row['pvalues'] == {method: 1. for method in losses}
    assert row['block_size'] == 24 and row['diagnostics']['library_attempts'] == 0


def test_same_seed_and_dict_order_reproduce_real_library_membership_and_pvalues():
    m = api(); losses = artificial_losses(128)
    first = m.compute_mcs(losses, identity(), design(49))
    second = m.compute_mcs(dict(reversed(list(losses.items()))), identity(), design(49))
    assert first == second
    assert first['status'] == 'COMPLETE'


def test_actual_arch_zero_variance_difference_is_failed_without_collapsing_unequal_losses():
    x = np.arange(1., 129.)
    row = api().compute_mcs({'a': x, 'b': x+2.}, identity(), design(17))
    assert row['status'] == 'MCS_FAILED'
    assert row['unique_loss_class_count'] == 2
    assert row['diagnostics']['library_attempts'] == 1
    assert row['diagnostics']['error_type'] == 'RuntimeWarning'


def test_no_complete_methods_is_explicitly_unavailable_without_library(monkeypatch):
    m = api()
    def forbidden(*args, **kwargs): raise AssertionError('empty input must not call library')
    monkeypatch.setattr(m, 'MCS', forbidden)
    row = m.compute_mcs({}, identity(), design())
    assert row['status'] == 'UNAVAILABLE' and row['method_count'] == 0
    assert row['method_ids'] == [] and row['included'] == [] and row['pvalues'] == {}
    assert row['diagnostics']['library_attempts'] == 0


@pytest.mark.parametrize('kind', ['warning', 'exception'])
def test_library_runtime_failure_is_one_failed_attempt_without_retry(kind, monkeypatch):
    m = api(); attempts = []
    class Failure:
        def __init__(self, matrix, **kwargs): attempts.append(dict(kwargs))
        def compute(self):
            if kind == 'warning': warnings.warn('artificial numerical warning', RuntimeWarning)
            else: raise ValueError('artificial library exception')
    monkeypatch.setattr(m, 'MCS', Failure)
    row = m.compute_mcs(artificial_losses(50), identity(), design(17))
    assert row['status'] == 'MCS_FAILED'
    assert len(attempts) == 1 and row['diagnostics']['library_attempts'] == 1
    assert attempts[0]['reps'] == 17 and attempts[0]['method'] == 'R'
    assert row['included'] == [] and row['excluded'] == [] and row['pvalues'] == {}
    assert row['reason']


def fake_result(pvalues, included, excluded):
    class Result:
        def __init__(self, *args, **kwargs): pass
        def compute(self): pass
    Result.pvalues = pd.DataFrame({'Pvalue': pvalues}, index=range(len(pvalues)))
    Result.included, Result.excluded = included, excluded
    return Result


def test_literal_arch_boundary_excludes_pvalue_equal_to_size(monkeypatch):
    m = api(); monkeypatch.setattr(m, 'MCS', fake_result([.1, 1.], [1], [0]))
    row = m.compute_mcs(artificial_losses(50), identity(), design(11))
    assert row['status'] == 'COMPLETE'
    assert row['excluded'] == ['good'] and row['included'] == ['poor']
    assert row['pvalues']['good'] == .1


@pytest.mark.parametrize('values,included,excluded', [
    ([float('nan'), 1.], [1], [0]), ([1.01, 1.], [0, 1], []),
    ([.1, 1.], [1], []), ([.1, 1.], [0, 1], [0]),
    ([.1, 1.], [0, 1], []),
])
def test_invalid_pvalue_or_partition_fails_the_whole_set(values, included, excluded, monkeypatch):
    m = api(); monkeypatch.setattr(m, 'MCS', fake_result(values, included, excluded))
    row = m.compute_mcs(artificial_losses(50), identity(), design(11))
    assert row['status'] == 'MCS_FAILED' and row['pvalues'] == {}
    assert row['diagnostics']['library_attempts'] == 1


@pytest.mark.parametrize('losses', [
    {'a': np.array([1., float('nan')]), 'b': np.ones(2)},
    {'a': np.ones(3), 'b': np.ones(2)},
    {'a': np.array([-1., 2.]), 'b': np.ones(2)},
    {'a': np.ones((2, 1)), 'b': np.ones(2)},
])
def test_full_input_validation_rejects_nonfinite_mismatch_negative_or_matrix_without_library(losses, monkeypatch):
    m = api()
    def forbidden(*args, **kwargs): raise AssertionError('invalid inputs must not call library')
    monkeypatch.setattr(m, 'MCS', forbidden)
    row = m.compute_mcs(losses, identity(), design())
    assert row['status'] == 'FAILED_INPUT' and row['diagnostics']['library_attempts'] == 0
    assert row['included'] == [] and row['pvalues'] == {}


@pytest.mark.parametrize('error_type', [StudyStop, DriverStop])
def test_root_resource_cancellation_propagates_without_library_retry(error_type, monkeypatch):
    m = api(); attempts = []
    def forbidden(*args, **kwargs): attempts.append(1); raise AssertionError('checkpoint should stop first')
    monkeypatch.setattr(m, 'MCS', forbidden)
    def stop(**kwargs): raise error_type('GLOBAL_DEADLINE')
    with pytest.raises(error_type):
        m.compute_mcs(artificial_losses(50), identity(), design(), checkpoint=stop)
    assert attempts == []
