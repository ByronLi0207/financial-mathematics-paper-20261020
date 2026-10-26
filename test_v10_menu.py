"""Artificial data and callback fixtures only; no calibration or study run."""
import importlib
import importlib.util
import json

import numpy as np
import pytest

from conditional_features import build_features
from conditional_quantile import QuantileFitError
from empirical_headroom import predict as empirical_predict
from run_v8_wp3 import DriverStop
from study_core import build_label_cache
from v8_mechanism_mc import forecast_report as inherited_forecast


MENU = [.001, .01, .1, 1., 10., 'inf']
MENUS = {'QR33': list(MENU), 'QR4': list(MENU)}


def api():
    assert importlib.util.find_spec('v10_menu') is not None, 'six-menu adapter is missing'
    return importlib.import_module('v10_menu')


def artificial_input(monotone=False):
    t = np.arange(650)
    x = 1. + .01*t*t if monotone else np.sin(t/8.) + .2*np.cos(t/3.) + .003*t
    times = np.datetime64('2000-01-03T00:00') + t*np.timedelta64(1, 'h')
    features = build_features(x, times, short_scale=24, long_scale=168,
                              nominal_gap_seconds=3600)
    return x, times, features, build_label_cache(x, 6)


@pytest.mark.parametrize('method,window,penalty', [
    ('F', 52, None), ('QR33', 52, .1), ('QR4', 52, .1),
    ('QR33', 260, 10.), ('QR4', 260, 10.),
])
def test_finite_reports_keep_actual_inherited_forecast_and_diagnostics(method, window, penalty):
    x, times, features, cache = artificial_input()
    ids = np.arange(560, 587)
    expected = inherited_forecast(x, times, features, cache, ids, 6, window, 24, method, penalty)
    for entry in (api().forecast_report, api().predict_report):
        got = entry(x, times, features, cache, ids, 6, window, 24, method, penalty)
        assert set(got) == set(expected)
        for name in ('origins', 'capacity', 'refit_indices'):
            np.testing.assert_array_equal(got[name], expected[name])
        assert got['fit_diagnostics'] == expected['fit_diagnostics']


@pytest.mark.parametrize('method', ['QR33', 'QR4'])
@pytest.mark.parametrize('window,rank', [(52, 50), (260, 247)])
def test_infinity_is_exact_ordinary_I_with_independent_rank_and_current_floor(method, window, rank, monkeypatch):
    x, times, features, cache = artificial_input(monotone=True)
    ids = np.arange(500, 527)
    expected = empirical_predict(x, ids, 6, window, 24)
    import v8_mechanism_mc
    def forbidden_fit(*args, **kwargs):
        raise AssertionError('infinity must never reach the finite solver')
    monkeypatch.setattr(v8_mechanism_mc, 'fit_quantile_ridge', forbidden_fit)
    got = api().forecast_report(x, times, features, cache, ids, 6, window, 24, method, 'inf')
    np.testing.assert_array_equal(got['capacity'], expected['I'])
    np.testing.assert_array_equal(got['origins'], ids)
    np.testing.assert_array_equal(got['refit_indices'], expected['refit_indices'])
    assert np.all(got['capacity'] < expected['F'])
    independent = []
    for issue in ids:
        refit = 500 + ((int(issue)-500)//24)*24
        pool = range(refit-6-window+1, refit-6+1)
        responses = sorted(max(abs(x[k]) for k in range(i, i+7))-abs(x[i]) for i in pool)
        independent.append(abs(x[issue]) + responses[rank-1])
    np.testing.assert_array_equal(got['capacity'], independent)
    assert [d['refit_index'] for d in got['fit_diagnostics']] == [500, 524]
    for d in got['fit_diagnostics']:
        r = d['refit_index']
        assert d['training_first_origin'] == r-6-window+1
        assert d['training_last_origin'] == r-6
        assert d['training_count'] == window
        assert d['latest_label_end'] == r


def rows(loss=1.):
    return [dict(penalty=p, status='COMPLETE', origin_count=4, mean_loss=loss) for p in MENU]


@pytest.mark.parametrize('method', ['QR33', 'QR4'])
def test_exact_tie_uses_strongest_and_near_tie_uses_actual_loss(method):
    candidates = rows()
    got = api().select_candidate(candidates, method, 4, MENUS)
    assert got['penalty'] == 'inf' and got['exact_tie'] is True
    assert got['minimum_loss_tied_candidates'] == 6
    assert got['tied_penalties'] == MENU
    assert got['legacy_qr4_tie_changed'] is (method == 'QR4')
    candidates[-1]['mean_loss'] = np.nextafter(1., 2.)
    got = api().select_candidate(candidates, method, 4, MENUS)
    assert got['penalty'] == 10.
    candidates[1]['mean_loss'] = np.nextafter(1., 0.)
    got = api().select_candidate(candidates, method, 4, MENUS)
    assert got['penalty'] == .01 and got['exact_tie'] is False


def test_failed_mandatory_qr33_is_ineligible_while_qr4_uses_completed_subset():
    candidates = rows()
    candidates[0].update(status='FAILED', origin_count=0, mean_loss=None, reason='NONCONVERGENCE')
    assert api().select_candidate(candidates, 'QR33', 4, MENUS)['status'] == 'INELIGIBLE'
    assert api().select_candidate(candidates, 'QR4', 4, MENUS)['penalty'] == 'inf'
    assert len(candidates) == 6 and candidates[0]['reason'] == 'NONCONVERGENCE'
    for c in candidates:
        c.update(status='FAILED', origin_count=0, mean_loss=None)
    assert api().select_candidate(candidates, 'QR4', 4, MENUS)['status'] == 'INELIGIBLE'


def test_complete_candidate_requires_full_finite_report_and_exact_menu():
    candidates = rows()
    candidates[0]['origin_count'] = 3
    with pytest.raises(ValueError): api().select_candidate(candidates, 'QR4', 4, MENUS)
    candidates = rows(); candidates[0]['mean_loss'] = float('nan')
    with pytest.raises(ValueError): api().select_candidate(candidates, 'QR33', 4, MENUS)
    with pytest.raises(ValueError): api().select_candidate(rows()[:-1], 'QR4', 4, MENUS)


def design():
    return dict(menus=MENUS, validation_first=0, validation_last=3)


def complete_score(loss=1.):
    return dict(n=np.int64(4), mean_loss=np.float64(loss), strict_breach_count=np.int64(0),
                strict_breach_rate=np.float64(0.))


@pytest.mark.parametrize('method,expected_status', [('QR33', 'FAILED'), ('QR4', 'COMPLETE')])
def test_evaluation_keeps_every_candidate_failure_and_uses_only_declared_selection(tmp_path, method, expected_status):
    m = api(); seen = []
    def report(segment, h, w, family, penalty):
        seen.append((segment, penalty))
        if segment == 'validation' and penalty == .001:
            raise QuantileFitError('NONCONVERGENCE', {'iterations': np.int64(10000)})
        if segment == 'evaluation':
            frozen = json.loads((tmp_path/f'W52_H6_{method}.selection.json').read_text())
            assert frozen['penalty'] == 'inf'
        return complete_score(), []
    got = m.evaluate_method(design(), tmp_path, 52, 6, method, report, lambda **k: None,
                            QuantileFitError, (DriverStop,))
    assert got['status'] == expected_status
    assert seen[:6] == [('validation', p) for p in MENU]
    assert seen[6:] == ([] if method == 'QR33' else [('evaluation', 'inf')])
    assert len(got['candidates']) == 6
    assert got['candidates'][0]['reason'] == 'NONCONVERGENCE'
    assert got['candidates'][0]['failure_diagnostics'] == {'iterations': 10000}
    saved = json.loads((tmp_path/f'W52_H6_{method}.json').read_text())
    assert saved == got
    assert type(saved['candidates'][1]['origin_count']) is int
    assert len(list(tmp_path.glob(f'W52_H6_{method}_validation-*.json'))) == 6


def test_selected_evaluation_failure_has_no_fallback_and_no_retry(tmp_path):
    m = api(); seen = []
    def report(segment, h, w, method, penalty):
        seen.append((segment, penalty))
        if segment == 'evaluation':
            assert json.loads((tmp_path/'W52_H6_QR4.selection.json').read_text())['penalty'] == 'inf'
            raise QuantileFitError('SELECTED_EVALUATION_FAILED', {'iterations': 10000})
        return complete_score(), []
    got = m.evaluate_method(design(), tmp_path, 52, 6, 'QR4', report, lambda **k: None,
                            QuantileFitError, (DriverStop,))
    assert got['status'] == 'FAILED' and got['reason'] == 'SELECTED_EVALUATION_FAILED'
    assert got['selected_penalty'] == 'inf'
    assert seen == [('validation', p) for p in MENU] + [('evaluation', 'inf')]


def test_resource_interruption_retains_attempt_and_unreached_inventory(tmp_path):
    m = api()
    def report(*args): raise DriverStop('GLOBAL_DEADLINE')
    with pytest.raises(DriverStop):
        m.evaluate_method(design(), tmp_path, 52, 6, 'QR4', report, lambda **k: None,
                          QuantileFitError, (DriverStop,))
    saved = json.loads((tmp_path/'W52_H6_QR4.json').read_text())
    assert saved['reason'] == 'GLOBAL_DEADLINE'
    assert saved['candidates'][0]['status'] == 'FAILED'
    assert [r['status'] for r in saved['candidates'][1:]] == ['NOT_ATTEMPTED']*5
