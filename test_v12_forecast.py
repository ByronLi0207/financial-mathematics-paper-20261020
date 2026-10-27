"""Constructed arrays only: no financial inputs, pilots or experiment drivers."""
import importlib
import importlib.util
from fractions import Fraction
import numpy as np
import pytest

from conditional_features import build_features
from empirical_headroom import predict as frozen_empirical
from study_core import build_label_cache, stable_mean
from v10_menu import forecast_report as frozen_report


def api():
    assert importlib.util.find_spec('v12_forecast') is not None, 'v12 forecast adapter is missing'
    return importlib.import_module('v12_forecast')


def toy():
    j = np.arange(220)
    position = 10. + .001 * j * j + .2 * np.sin(j / 7.)
    times = np.datetime64('2000-01-03') + j * np.timedelta64(7, 'D')
    cell = dict(horizon=6, window=52, refit_step=3, short_scale=6,
                long_scale=26, nominal_gap_seconds=604800)
    return dict(position=position, times=times), cell


@pytest.mark.parametrize('method', ['QR33', 'QR4'])
@pytest.mark.parametrize('penalty', [.001, .01, .1, 1., 10.])
def test_tau95_finite_forecasts_preserve_frozen_arrays_and_diagnostics(method, penalty):
    m = api(); series, cell = toy(); ids = np.arange(160, 165)
    context = m.make_context(series, cell)
    features = build_features(series['position'], series['times'], short_scale=6,
                              long_scale=26, nominal_gap_seconds=604800)
    expected = frozen_report(series['position'], series['times'], features,
        build_label_cache(series['position'], 6), ids, 6, 52, 3, method, penalty)
    got = m.predict_segment(context, ids, method, penalty)
    assert got['fit_diagnostics'] == expected['fit_diagnostics']
    for key in ('origins', 'capacity', 'refit_indices'):
        np.testing.assert_array_equal(got[key], expected[key])


@pytest.mark.parametrize('tau', [.9, .95, .99])
@pytest.mark.parametrize('method', ['QR33', 'QR4'])
def test_infinity_is_exactly_the_ordinary_empirical_report(tau, method):
    m = api(); series, cell = toy(); ids = np.arange(160, 167)
    context = m.make_context(series, cell)
    ordinary = m.predict_segment(context, ids, 'I', tau=tau)
    limit = m.predict_segment(context, ids, method, 'inf', tau=tau)
    assert limit['fit_diagnostics'] == ordinary['fit_diagnostics']
    for key in ('origins', 'capacity', 'refit_indices'):
        np.testing.assert_array_equal(limit[key], ordinary[key])


@pytest.mark.parametrize('method', ['I', 'F'])
def test_tau95_empirical_arrays_keep_original_rank_pool_and_clock(method):
    m = api(); series, cell = toy(); ids = np.arange(160, 167)
    context = m.make_context(series, cell)
    expected = frozen_empirical(series['position'], ids, 6, 52, 3)
    got = m.predict_segment(context, ids, method)
    np.testing.assert_array_equal(got['capacity'], expected[method])
    np.testing.assert_array_equal(got['refit_indices'], [160, 160, 160, 163, 163, 163, 166])
    assert [d['training_first_origin'] for d in got['fit_diagnostics']] == [103, 106, 109]
    assert [d['training_last_origin'] for d in got['fit_diagnostics']] == [154, 157, 160]
    assert [d['latest_label_end'] for d in got['fit_diagnostics']] == [160, 163, 166]


def test_tau99_w52_corrected_rank_saturates_at_pool_maximum():
    m = api(); series, cell = toy(); ids = np.arange(160, 163)
    context = m.make_context(series, cell)
    x = series['position']
    # One refit at160: independent, duplicate-preserving mature response pool.
    headrooms = [max(abs(x[k]) for k in range(i, i + 7)) - abs(x[i])
                 for i in range(103, 155)]
    expected = np.abs(x[ids]) + max(headrooms)
    for method in ('F', 'I'):
        got = m.predict_segment(context, ids, method, tau=.99)
        np.testing.assert_array_equal(got['capacity'], expected)


@pytest.mark.parametrize('tau', [.9, .99])
@pytest.mark.parametrize('method', ['QR33', 'QR4'])
def test_generic_tau_finite_solver_preserves_frozen_refit_clock(tau, method):
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    ids = np.arange(160, 164)
    got = m.predict_segment(context, ids, method, .1, tau=tau)
    np.testing.assert_array_equal(got['refit_indices'], [160, 160, 160, 163])
    assert np.isfinite(got['capacity']).all()
    assert np.all(got['capacity'] >= np.abs(series['position'][ids]))
    assert [d['training_count'] for d in got['fit_diagnostics']] == [52, 52]
    assert [d['latest_label_end'] for d in got['fit_diagnostics']] == [160, 163]
    assert all(d['duality_gap'] <= d['gap_tolerance'] for d in got['fit_diagnostics'])


@pytest.mark.parametrize('method', ['QR33', 'QR4'])
def test_generic_solver_uses_declared_level_on_hand_computed_intercept_quantiles(method):
    m = api(); series, cell = toy()
    series['position'][:] = 10.
    series['position'][155:161] = [11., 12., 13., 14., 15., 16.]
    context = m.make_context(series, cell)
    # All training predictors are constant at origins103..154. Their completed
    # headrooms have46 zeros followed by1..6: unique .90 quantile1, .99 quantile6.
    lower = m.predict_segment(context, [160], method, .1, tau=.90)
    upper = m.predict_segment(context, [160], method, .1, tau=.99)
    # An objective-gap certificate does not promise a1e-5 capacity error.
    # Independently derive the scalar quantile's sharpness from the known
    # empirical CDF, and translate the unchanged gap tolerance to native units.
    for report, want, left_slope, right_slope in [
        (lower, 17., Fraction(9, 10)-Fraction(46, 52), Fraction(47, 52)-Fraction(9, 10)),
        (upper, 22., Fraction(99, 100)-Fraction(51, 52), Fraction(1, 100)),
    ]:
        tolerance = (21 / 52) * report['fit_diagnostics'][0]['gap_tolerance']
        tolerance /= float(min(left_slope, right_slope))
        assert abs(report['capacity'][0] - want) <= tolerance
    assert m.predict_segment(context, [160], 'I', tau=.9)['capacity'][0] == 17.
    assert m.predict_segment(context, [160], 'F', tau=.9)['capacity'][0] == 18.


@pytest.mark.parametrize('tau', [.9, .95, .99])
@pytest.mark.parametrize('method,penalty', [('F', None), ('I', None), ('QR33', .1), ('QR4', .1)])
def test_unobserved_future_values_do_not_change_issued_report(tau, method, penalty):
    m = api(); series, cell = toy(); ids = np.array([160])
    context = m.make_context(series, cell)
    changed = dict(series, position=series['position'].copy())
    changed['position'][161:] = 1000. + np.arange(59)
    other = m.make_context(changed, cell)
    left = m.predict_segment(context, ids, method, penalty, tau=tau)
    right = m.predict_segment(other, ids, method, penalty, tau=tau)
    np.testing.assert_array_equal(left['capacity'], right['capacity'])
    assert left['fit_diagnostics'] == right['fit_diagnostics']


@pytest.mark.parametrize('tau,want', [(.9, [.9, .1, 0.]), (.95, [.95, .05, 0.]), (.99, [.99, .01, 0.])])
def test_score_uses_declared_tau_strict_breaches_and_native_components(tau, want):
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    ids = np.arange(160, 163)
    x = series['position']
    peak = np.array([max(abs(x[k]) for k in range(i, i + 7)) for i in ids])
    capacity = peak + [-1., 1., 0.]
    report = m.score_report(context, ids, capacity, tau=tau)
    np.testing.assert_array_equal(report['losses'], want)
    np.testing.assert_array_equal(report['peak'], peak)
    np.testing.assert_array_equal(report['floor'], np.abs(x[ids]))
    assert report['mean_loss'] == stable_mean(want)
    assert report['n'] == 3 and report['strict_breach_count'] == 1
    assert report['strict_breach_rate'] == 1 / 3
    assert report['mean_underprediction'] == 1 / 3
    assert report['mean_overprediction'] == 1 / 3


@pytest.mark.parametrize('bad', [[], [160, 162], [160.0], [-1], [220]])
def test_prediction_rejects_empty_gapped_noninteger_or_out_of_range_origins(bad):
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    with pytest.raises(ValueError):
        m.predict_segment(context, bad, 'F')


@pytest.mark.parametrize('kind', ['shape', 'nonfinite', 'below_floor', 'unmatured'])
def test_score_rejects_incomplete_or_invalid_full_vectors(kind):
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    ids = np.arange(160, 163); cap = np.abs(series['position'][ids]) + 10.
    if kind == 'shape': cap = cap[:-1]
    if kind == 'nonfinite': cap[0] = np.nan
    if kind == 'below_floor': cap[0] = abs(series['position'][160]) - 1.
    if kind == 'unmatured': ids = np.arange(215, 218)
    with pytest.raises(ValueError):
        m.score_report(context, ids, cap, tau=.99)


def test_context_owns_inputs_and_rejects_invalid_source_or_cell():
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    expected = m.predict_segment(context, [160], 'F')['capacity'].copy()
    series['position'][:] = -999.
    np.testing.assert_array_equal(m.predict_segment(context, [160], 'F')['capacity'], expected)
    with pytest.raises(ValueError): m.make_context(series, dict(cell, refit_step=0))
    with pytest.raises(ValueError): m.make_context(dict(series, times=series['times'][::-1]), cell)
    with pytest.raises(ValueError): m.make_context(dict(series, position=[np.nan] * 220), cell)


@pytest.mark.parametrize('tau', [0., 1., np.nan, True])
def test_invalid_tau_is_rejected_before_predictions_or_scoring(tau):
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    with pytest.raises(ValueError): m.predict_segment(context, [160], 'F', tau=tau)
    with pytest.raises(ValueError): m.score_report(context, [160], [100.], tau=tau)


def test_solver_checkpoint_cancellation_propagates_without_partial_success():
    m = api(); series, cell = toy(); context = m.make_context(series, cell)
    class Cancelled(Exception): pass
    def stop(**detail): raise Cancelled('constructed cancellation')
    with pytest.raises(Cancelled):
        m.predict_segment(context, np.arange(160, 164), 'QR33', .1, tau=.99, checkpoint=stop)
