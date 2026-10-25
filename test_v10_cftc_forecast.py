"""Only constructed arrays and controlled failures; no CFTC input reads."""
from copy import deepcopy
import importlib
import importlib.util
import hashlib
import json

import numpy as np
import pytest

from conditional_quantile import QuantileFitError
from empirical_headroom import predict as empirical_predict
from run_study import StudyStop
from run_v8_wp3 import DriverStop
from study_core import build_label_cache


METHODS = ['F', 'I', 'QR4', 'QR33', 'ACI_F', 'ACI_QR33']
MENU = [.001, .01, .1, 1., 10., 'inf']


def api():
    assert importlib.util.find_spec('v10_cftc_forecast') is not None, 'CFTC forecast adapter is missing'
    return importlib.import_module('v10_cftc_forecast')


def design():
    return dict(horizon=6, windows=[52], refit_step=13, feature_rms_short=6,
        feature_rms_long=26, nominal_gap_seconds=604800, methods=list(METHODS),
        menus={'QR33': list(MENU), 'QR4': list(MENU)},
        split_formulas={'validation_n': 4, 'evaluation_n': 8},
        ancillary={'gammas': [.001, .005, .01, .05]})


def inputs(n=400):
    return np.full(n, 100.), np.datetime64('2000-01-03') + np.arange(n)*np.timedelta64(7, 'D')


def load(path):
    return json.loads(path.read_text())


def test_real_artificial_six_method_run_has_complete_traces_and_dynamic_split(tmp_path):
    m = api(); x, t = inputs(); d = design(); before = deepcopy(d)
    output = tmp_path/'cell'
    got = m.forecast_cell(x, t, d, 52, output)
    assert d == before
    assert [r['method'] for r in got['methods']] == METHODS
    assert all(r['status'] == 'COMPLETE' and r['n'] == 8 for r in got['methods'])
    assert all(r['mean_loss'] == 0. and r['strict_breach_count'] == 0 for r in got['methods'])
    assert set(got['traces']) == set(METHODS)
    for trace in got['traces'].values():
        assert set(trace) == {'origins', 'capacities', 'peak', 'floor', 'pinball', 'strict_breach', 'overrun', 'unused'}
        assert all(isinstance(a, np.ndarray) and a.shape == (8,) and np.isfinite(a).all() for a in trace.values())
        np.testing.assert_array_equal(trace['origins'], np.arange(386, 394))
        np.testing.assert_array_equal(trace['capacities'], np.full(8, 100.))
    for row in got['methods']:
        saved = load(output/f"result-{row['method']}.json")
        assert saved == row
        trace_path = output/saved['trace_path']
        assert trace_path.name == f"trace-{row['method']}.npz"
        assert trace_path.stat().st_size == saved['trace_bytes']
        assert hashlib.sha256(trace_path.read_bytes()).hexdigest() == saved['trace_sha256']
        with np.load(trace_path, allow_pickle=False) as z:
            assert set(z.files) == set(got['traces'][row['method']])
    ordinary = empirical_predict(x, np.arange(386, 394), 6, 52, 13)
    np.testing.assert_array_equal(got['traces']['F']['capacities'], ordinary['F'])
    np.testing.assert_array_equal(got['traces']['I']['capacities'], ordinary['I'])
    for method in ('QR4', 'QR33'):
        receipt = load(output/f'W52_H6_{method}.json')
        assert [r['penalty'] for r in receipt['candidates']] == MENU
        assert receipt['selected_penalty'] == 'inf'
        assert load(output/f'W52_H6_{method}.selection.json')['penalty'] == 'inf'
    for method in ('ACI_F', 'ACI_QR33'):
        receipt = load(output/f'W52_H6_{method}.json')
        assert len(receipt['candidates']) == 4
        assert receipt['selected_gamma'] == .001
        assert receipt['validation_prefix_identical'] is True
        assert receipt['feedback_consumed'] == 6
        assert load(output/f'W52_H6_{method}.selection.json')['gamma'] == .001


def test_selected_validation_and_evaluation_bases_are_not_refit_for_aci(tmp_path, monkeypatch):
    m = api(); x, t = inputs(); seen = []
    original = m.forecast_report
    def tracked(position, times, features, cache, origins, horizon, window, refit_step, method, penalty=None, checkpoint=None):
        key = (method, penalty, int(origins[0]), int(origins[-1]))
        assert key not in seen, 'an already attempted QR segment was recomputed'
        seen.append(key)
        return original(position, times, features, cache, origins, horizon, window, refit_step, method, penalty, checkpoint)
    monkeypatch.setattr(m, 'forecast_report', tracked)
    got = m.forecast_cell(x, t, design(), 52, tmp_path/'cell')
    assert next(r for r in got['methods'] if r['method'] == 'ACI_QR33')['status'] == 'COMPLETE'
    assert ('QR33', 'inf', 376, 379) in seen and ('QR33', 'inf', 386, 393) in seen
    warm = [k for k in seen if k[0] == 'QR33' and k[3] < 376]
    assert len(warm) == 1 and warm[0][1] == 'inf'


def test_mandatory_candidate_failure_blocks_qr33_and_aci_but_preserves_other_bases(tmp_path, monkeypatch):
    m = api(); x, t = inputs(); original = m.forecast_report
    def fail_one(*args, **kwargs):
        if args[8] == 'QR33' and args[9] == .001:
            raise QuantileFitError('ARTIFICIAL_NONCONVERGENCE', {'iterations': 10000})
        return original(*args, **kwargs)
    monkeypatch.setattr(m, 'forecast_report', fail_one)
    got = m.forecast_cell(x, t, design(), 52, tmp_path/'cell')
    rows = {r['method']: r for r in got['methods']}
    assert rows['QR33']['status'] == 'FAILED' and rows['QR33']['mean_loss'] is None
    assert rows['ACI_QR33']['status'] in ('NA', 'FAILED') and rows['ACI_QR33']['mean_loss'] is None
    assert all(rows[k]['status'] == 'COMPLETE' for k in ('F', 'I', 'QR4', 'ACI_F'))
    assert 'QR33' not in got['traces'] and 'ACI_QR33' not in got['traces']
    candidates = load(tmp_path/'cell'/'W52_H6_QR33.json')['candidates']
    assert len(candidates) == 6 and candidates[0]['reason'] == 'ARTIFICIAL_NONCONVERGENCE'
    assert all(r['status'] == 'COMPLETE' for r in candidates[1:])
    failed = load(tmp_path/'cell'/'result-QR33.json')
    assert failed['status'] == 'FAILED' and 'trace_path' not in failed
    assert not (tmp_path/'cell'/'trace-QR33.npz').exists()


def test_nonconstant_F_wrapper_uses_original_segments_and_carries_gap_feedback(tmp_path, monkeypatch):
    m = api(); _, times = inputs()
    u = np.arange(400)
    x = 100. + .01*u + .5*np.sin(u/8.)
    issued = []
    stream = m.aci.aci_stream
    def observed_stream(**kwargs):
        issued.append(np.array(kwargs['origins'], copy=True))
        return stream(**kwargs)
    monkeypatch.setattr(m.aci, 'aci_stream', observed_stream)
    got = m.forecast_cell(x, times, design(), 52, tmp_path/'cell')
    row = next(r for r in got['methods'] if r['method'] == 'ACI_F')
    assert row['status'] == 'COMPLETE' and row['feedback_consumed'] == 6
    validation = np.arange(376, 380); evaluation = np.arange(386, 394)
    together = np.concatenate((validation, evaluation))
    assert any(np.array_equal(v, together) for v in issued)
    assert all(not np.isin(v, np.arange(380, 386)).any() for v in issued)
    warm = np.arange(311, 376)
    labels = build_label_cache(x, 6)
    warm_base = empirical_predict(x, warm, 6, 52, 13)['F']
    validation_base = empirical_predict(x, validation, 6, 52, 13)['F']
    evaluation_base = empirical_predict(x, evaluation, 6, 52, 13)['F']
    expected = stream(origins=together, base=np.concatenate((validation_base, evaluation_base)),
        peak=labels.peak[together], floor=np.abs(x[together]), horizon=6, window=52,
        gamma=row['selected_gamma'], warm_origins=warm, warm_base=warm_base, warm_peak=labels.peak[warm])
    np.testing.assert_array_equal(got['traces']['ACI_F']['capacities'], expected['capacities'][4:])


def test_selected_base_evaluation_failure_has_no_retry_or_ancillary_rescue(tmp_path, monkeypatch):
    m = api(); x, t = inputs(); original = m.forecast_report; failed = []
    def selected_fail(*args, **kwargs):
        if args[8] == 'QR33' and int(args[4][0]) == 386:
            failed.append(args[9])
            assert load(tmp_path/'cell'/'W52_H6_QR33.selection.json')['penalty'] == args[9]
            raise QuantileFitError('ARTIFICIAL_SELECTED_EVALUATION_FAILURE', {'iterations': 10000})
        return original(*args, **kwargs)
    monkeypatch.setattr(m, 'forecast_report', selected_fail)
    got = m.forecast_cell(x, t, design(), 52, tmp_path/'cell')
    rows = {r['method']: r for r in got['methods']}
    assert failed == ['inf']
    assert rows['QR33']['status'] == 'FAILED' and rows['QR33']['selected_penalty'] == 'inf'
    assert rows['ACI_QR33']['status'] in ('NA', 'FAILED') and rows['ACI_QR33']['mean_loss'] is None
    assert all(rows[k]['status'] == 'COMPLETE' for k in ('F', 'I', 'QR4', 'ACI_F'))


def test_gamma_failures_remain_visible_and_do_not_invalidate_complete_base(tmp_path, monkeypatch):
    m = api(); x, t = inputs()
    def no_gamma(**kwargs):
        raise ValueError('ARTIFICIAL_GAMMA_FAILURE')
    monkeypatch.setattr(m.aci, 'aci_stream', no_gamma)
    got = m.forecast_cell(x, t, design(), 52, tmp_path/'cell')
    rows = {r['method']: r for r in got['methods']}
    assert all(rows[k]['status'] == 'COMPLETE' for k in ('F', 'I', 'QR4', 'QR33'))
    for method in ('ACI_F', 'ACI_QR33'):
        assert rows[method]['status'] in ('NA', 'FAILED') and rows[method]['mean_loss'] is None
        assert method not in got['traces']
        receipt = load(tmp_path/'cell'/f'W52_H6_{method}.json')
        assert len(receipt['candidates']) == 4 and all(c['status'] != 'COMPLETE' for c in receipt['candidates'])


def test_aci_freezes_gamma_before_combined_stream_and_rejects_changed_validation_prefix(tmp_path, monkeypatch):
    m = api(); x, t = inputs(); original = m.aci.aci_stream
    def changed_prefix(**kwargs):
        result = original(**kwargs)
        if len(kwargs['origins']) > 4:
            assert list((tmp_path/'cell').glob('*ACI*.selection.json'))
            result['capacities'] = result['capacities'].copy()
            result['capacities'][0] += 1.
        return result
    monkeypatch.setattr(m.aci, 'aci_stream', changed_prefix)
    got = m.forecast_cell(x, t, design(), 52, tmp_path/'cell')
    rows = {r['method']: r for r in got['methods']}
    for method in ('ACI_F', 'ACI_QR33'):
        assert rows[method]['status'] == 'FAILED' and rows[method]['mean_loss'] is None
        assert rows[method]['reason'] == 'VALIDATION_PREFIX_CHANGED'
        assert method not in got['traces']
    assert all(rows[k]['status'] == 'COMPLETE' for k in ('F', 'I', 'QR4', 'QR33'))


def test_short_warmup_keeps_the_declared_feature_specific_eligibility(tmp_path):
    m = api(); x, t = inputs(110)
    got = m.forecast_cell(x, t, design(), 52, tmp_path/'cell')
    rows = {r['method']: r for r in got['methods']}
    assert rows['QR33']['status'] == 'COMPLETE'
    assert rows['ACI_F']['status'] == 'COMPLETE'
    assert rows['ACI_QR33']['status'] == 'NA'
    assert rows['ACI_QR33']['reason'] == 'INSUFFICIENT_PREVALIDATION_CALIBRATION'


@pytest.mark.parametrize('error_type', [StudyStop, DriverStop])
def test_resource_error_propagates_after_preserving_finished_method_receipts(tmp_path, error_type):
    m = api(); x, t = inputs()
    def checkpoint(**detail):
        if detail.get('stage') == 'cftc_method_start' and detail.get('method') == 'QR4':
            raise error_type('GLOBAL_DEADLINE')
    with pytest.raises(error_type):
        m.forecast_cell(x, t, design(), 52, tmp_path/'cell', checkpoint=checkpoint)
    assert load(tmp_path/'cell'/'W52_H6_F.json')['status'] == 'COMPLETE'
    assert load(tmp_path/'cell'/'W52_H6_I.json')['status'] == 'COMPLETE'
    for method in ('F', 'I'):
        saved = load(tmp_path/'cell'/f'result-{method}.json')
        assert saved['status'] == 'COMPLETE'
        assert (tmp_path/'cell'/saved['trace_path']).is_file()
