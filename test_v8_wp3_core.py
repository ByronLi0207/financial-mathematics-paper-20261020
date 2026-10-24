"""Deterministic fixtures for the frozen WP3 generator and information clock.

These are unit tests, not study repetitions or a timing/result-dependent pilot.
"""
import math

import numpy as np
import pytest

from conditional_features import build_features
from conditional_study import StudyConfig, conditional_forecast
from study_core import build_label_cache
from v8_mechanism_mc import (simulate_level_garch, repetition_normals,
                            select_candidate, forecast_report)


def test_garch_recursion_and_burnin_are_not_increment_ar():
    z = np.array([1., 0., -2., 1.])
    got = simulate_level_garch(z, .7, .1, .05, .85, 1)
    expected_variances = np.array([1., .95, 1.0975])
    expected_innovations = np.array([0., -2 * math.sqrt(.95), math.sqrt(1.0975)])
    n2 = .49 - 2 * math.sqrt(.95)
    expected_levels = np.array([.7, n2, .7 * n2 + math.sqrt(1.0975)])
    np.testing.assert_allclose(got['variance'], expected_variances, rtol=1e-14)
    np.testing.assert_allclose(got['innovations'], expected_innovations, rtol=1e-14)
    np.testing.assert_allclose(got['position'], expected_levels, rtol=1e-14)
    np.testing.assert_array_equal(z, [1., 0., -2., 1.])


def test_homoskedastic_case_preserves_unit_innovation_variance():
    z = np.array([1., -2., .5, 0.])
    got = simulate_level_garch(z, .5, 1., 0., 0., 0)
    np.testing.assert_array_equal(got['variance'], np.ones(4))
    np.testing.assert_array_equal(got['innovations'], z)
    np.testing.assert_allclose(got['position'], [1., -1.5, -.25, -.125])


@pytest.mark.parametrize('bad', [dict(phi=1.), dict(omega=0.), dict(alpha=-.01),
                                 dict(alpha=.2, beta=.9), dict(burn_in=4)])
def test_invalid_dgp_contract_is_rejected(bad):
    options = dict(phi=.7, omega=.1, alpha=.05, beta=.85, burn_in=0)
    options.update(bad)
    with pytest.raises(ValueError):
        simulate_level_garch(np.ones(4), **options)


def test_repetition_stream_is_reproducible_and_distinct():
    design = dict(master_entropy=2026102408, burn_in=2, retained_observations=5,
                  repetitions=32)
    a, initial, final = repetition_normals(0, design)
    b, initial_b, final_b = repetition_normals(0, design)
    c, _, _ = repetition_normals(1, design)
    np.testing.assert_array_equal(a, b)
    assert a.shape == (7,) and not np.array_equal(a, c)
    assert initial == initial_b and final == final_b and initial != final


MENUS = {'QR33': [.001, .01, .1], 'QR4': [.001, .01, .1, 1., 10.]}


def candidates(method, loss=1.):
    return [dict(penalty=p, status='COMPLETE', mean_loss=loss, origin_count=2)
            for p in MENUS[method]]


def test_original_selectors_keep_different_exact_tie_rules():
    assert select_candidate(candidates('QR33'), 'QR33', 2, MENUS)['penalty'] == .1
    assert select_candidate(candidates('QR4'), 'QR4', 2, MENUS)['penalty'] == .001


def test_original_qr33_failed_mandatory_candidate_blocks_selection():
    rows = candidates('QR33')
    rows[1] = dict(penalty=.01, status='FAILED', reason='NONCONVERGENCE')
    selected = select_candidate(rows, 'QR33', 2, MENUS)
    assert selected['status'] == 'INELIGIBLE' and selected['penalty'] is None


def test_original_qr4_selects_completed_candidates_without_erasing_failures():
    rows = candidates('QR4')
    rows[0] = dict(penalty=.001, status='FAILED', reason='NONCONVERGENCE')
    selected = select_candidate(rows, 'QR4', 2, MENUS)
    assert selected['status'] == 'SELECTED' and selected['penalty'] == .01
    assert rows[0]['status'] == 'FAILED' and len(rows) == 5


def test_wrong_or_nonfinite_validation_score_cannot_be_complete():
    rows = candidates('QR33')
    rows[0]['mean_loss'] = float('nan')
    with pytest.raises(ValueError):
        select_candidate(rows, 'QR33', 2, MENUS)
    rows = candidates('QR33')
    rows[0]['origin_count'] = 1
    with pytest.raises(ValueError):
        select_candidate(rows, 'QR33', 2, MENUS)


def fixture():
    t = np.arange(330)
    x = np.sin(t / 8.) + .2 * np.cos(t / 3.) + .003 * t
    clock = np.datetime64('2000-01-03T00:00') + t * np.timedelta64(1, 'h')
    feature = build_features(x, clock, short_scale=24, long_scale=168,
                             nominal_gap_seconds=3600)
    return x, clock, feature, build_label_cache(x, 6)


def test_historical_report_freezes_pool_but_reanchors_every_issue():
    x, clock, features, cache = fixture()
    origins = np.arange(225, 231)
    got = forecast_report(x, clock, features, cache, origins, 6, 52, 24, 'F')
    pool = np.arange(168, 220)
    rank = math.ceil(19 * (52 + 1) / 20)
    q = sorted(cache.headroom[pool])[rank - 1]
    expected = np.abs(x[origins]) + q
    np.testing.assert_array_equal(got['capacity'], expected)
    np.testing.assert_array_equal(got['refit_indices'], np.full(6, 225))
    assert got['fit_diagnostics'][0]['latest_label_end'] == 225


def test_qr33_matches_original_fixed_parameter_arithmetic():
    x, clock, features, cache = fixture()
    origins = np.arange(225, 231)
    got = forecast_report(x, clock, features, cache, origins, 6, 52, 24, 'QR33', .1)
    old = conditional_forecast(x, clock, origins,
        StudyConfig(6, 52, 24, 24, 168, 3600), 'QR', .1)
    np.testing.assert_array_equal(got['capacity'], old.capacities)


def test_qr4_matches_original_fixed_parameter_arithmetic():
    import parsimonious_v3 as old_core
    x, clock, features, cache = fixture()
    origins = np.arange(225, 231)
    got = forecast_report(x, clock, features, cache, origins, 6, 52, 24, 'QR4', .1)
    feature4, valid = old_core.features4(x, clock, 24, 168, 3600)
    old, _ = old_core.forecast(x, feature4, valid, cache, origins, 6, 52, 24,
                               .1, lambda **kwargs: None)
    np.testing.assert_array_equal(got['capacity'], old)


def test_nonfinite_qr4_query_cannot_silently_become_a_floor_forecast():
    from dataclasses import replace
    x, clock, features, cache = fixture()
    values = features.values.copy()
    values[225, 25] = float('nan')
    corrupt = replace(features, values=values)
    with pytest.raises(ValueError):
        forecast_report(x, clock, corrupt, cache, np.array([225]), 6, 52, 24, 'QR4', .1)


@pytest.mark.parametrize('method', ['F', 'QR33', 'QR4'])
def test_future_positions_do_not_change_the_current_report(method):
    x, clock, features, cache = fixture()
    origins = np.array([225])
    penalty = .1 if method != 'F' else None
    first = forecast_report(x, clock, features, cache, origins, 6, 52, 24, method, penalty)
    changed = x.copy()
    changed[226:] += 1000.
    future_feature = build_features(changed, clock, short_scale=24, long_scale=168,
                                   nominal_gap_seconds=3600)
    future_cache = build_label_cache(changed, 6)
    second = forecast_report(changed, clock, future_feature, future_cache,
                             origins, 6, 52, 24, method, penalty)
    np.testing.assert_array_equal(first['capacity'], second['capacity'])
    assert first['fit_diagnostics'][0]['latest_label_end'] <= 225


def test_refit_maturity_and_frozen_query_blocks_are_explicit():
    x, clock, features, cache = fixture()
    origins = np.arange(225, 255)
    got = forecast_report(x, clock, features, cache, origins, 6, 52, 24, 'F')
    assert [d['refit_index'] for d in got['fit_diagnostics']] == [225, 249]
    assert all(d['training_count'] == 52 and d['latest_label_end'] == d['refit_index']
               for d in got['fit_diagnostics'])
    assert np.all(got['capacity'] >= np.abs(x[origins]))
