"""Synthetic aggregate/receipt/slot tests: no archive loader is called."""
import copy
import importlib
import importlib.util
import json

import numpy as np
import pytest


HASH = 'a' * 64
OTHER = 'b' * 64
METHODS = ('ACI_F', 'ACI_QR', 'SAV')


def api():
    assert importlib.util.find_spec('v6_wp2_summary') is not None, 'WP2 summary API is not implemented'
    return importlib.import_module('v6_wp2_summary')


def fixture():
    # All arrays are hand-created synthetic fixtures; source names only identify slots.
    spec = {'horizons': [6, 24], 'sources': {
        'fx_hourly': {'windows': [720, 2880], 'evaluation_origin_first': 100, 'evaluation_origin_last': 163},
        'nyfed_weekly': {'windows': [52, 260], 'evaluation_origin_first': 100, 'evaluation_origin_last': 163}}}
    slots = []
    cells = [(s, h, w) for s, c in spec['sources'].items() for h in spec['horizons'] for w in c['windows']]
    for s, h, w in cells:
        slots += [f'{s}:H{h}:W{w}:{m}-minus-{c}' for m in METHODS for c in ('frozen_F', 'QR')]
    slots += [f'{s}:H{h}:W{w}:ACI_QR-minus-ACI_F' for s, h, w in cells]
    freeze = {'wp2_contrast_slots': slots, 'family_sizes': {'WP2': 56}}
    x = np.arange(64)
    peak = 10. + (x % 7)
    original = {}
    new = {}
    receipts = {}
    validation = {}
    from v6_inference import summarize_scores
    for s, h, w in cells:
        for method, offset in [('frozen_F', 1. + (x % 3)), ('QR', -.5 + (x % 4)),
                               ('ACI_F', .5 + (x % 3)), ('ACI_QR', .25 + (x % 4)),
                               ('SAV', -.25 + (x % 5))]:
            key = f'{s}-h{h}-w{w}-{method}'
            trace = {'origins': np.arange(100, 164), 'capacity': peak + offset,
                     'peak': peak.copy(), 'floor': np.ones(64)}
            proof = {'sha256': HASH, 'bytes': 123, 'receipt_sha256': OTHER,
                     'receipt_bytes': 456}
            if method in METHODS:
                trace['capacities'] = trace.pop('capacity')
                new[key] = {'trace': trace, 'provenance': proof}
                metrics = summarize_scores(peak, trace['capacities'], tau=.95, origins=trace['origins'], horizon=h)
                payload = {'source': s, 'horizon': h, 'window': w, 'method': method,
                           'phase': 'evaluation', 'status': 'COMPLETE', 'scores': metrics,
                           'executable_freeze_sha256': HASH,
                           'private_artifact': {'sha256': HASH, 'bytes': 123}}
                if method.startswith('ACI_'):
                    payload.update(selected_gamma=.005, selection_freeze_sha256=HASH,
                                   validation_prefix_identical=True, diagnostics={'clip_count': 2})
                receipts[key] = {'receipt': payload, 'sha256': OTHER, 'bytes': 456}
                validation[key] = {'status': 'COMPLETE', 'receipt_sha256': HASH, 'selected_gamma': .005}
            else:
                original[key] = {'trace': trace, 'provenance': proof}
    provenance = {'executable_freeze_sha256': HASH, 'selection_freeze_sha256': HASH,
                  'design_freeze_sha256': HASH, 'spec_sha256': HASH, 'validation': validation}
    def load_new(s, h, w, method, receipt):
        return copy.deepcopy(new[f'{s}-h{h}-w{w}-{method}'])
    def load_original(s, h, w, method):
        return copy.deepcopy(original[f'{s}-h{h}-w{w}-{method}'])
    return spec, freeze, receipts, provenance, new, original, load_new, load_original


def run_fixture(parts):
    spec, freeze, receipts, provenance, _new, _original, ln, lo = parts
    return api().aggregate_wp2(spec, freeze, receipts, load_new=ln,
                               load_original=lo, provenance=provenance)


def test_full_inventory_has_24_methods_16_controls_and_exact_56_frozen_slots():
    # Catches shrinking a family, dropping a source/H/W cell or inventing a contrast.
    parts = fixture()
    summary, comparisons = run_fixture(parts)
    assert len(summary['method_rows']) == 24
    assert len(summary['control_rows']) == 16
    assert len(summary['aci_pairs']) == 8
    assert comparisons['family_n'] == 56
    assert [r['slot_id'] for r in comparisons['rows']] == parts[1]['wp2_contrast_slots']
    assert all(r['direction'] == 'new_minus_control' and r['tau'] == .95 for r in comparisons['rows'])


def test_every_comparison_uses_named_matched_controls_and_original_dm_direction():
    # Catches swapping F/QR, crossing windows, reversing loss signs or mixing tau.
    parts = fixture()
    summary, comparisons = run_fixture(parts)
    row = comparisons['rows'][0]
    # ACI_F lowers an always-overforecasting F report by .5: loss changes by -.025.
    assert row['left_method'] == 'ACI_F'
    assert row['right_method'] == 'frozen_F'
    assert row['mean_difference'] == pytest.approx(-.025)
    assert row['raw_p'] == row['dm_p']
    qr = next(r for r in comparisons['rows'] if r['slot_id'].endswith('ACI_QR-minus-ACI_F'))
    assert qr['left_method'] == 'ACI_QR' and qr['right_method'] == 'ACI_F'
    assert summary['aci_pairs'][0]['wrapped_qr_minus_f_mean_loss'] == pytest.approx(qr['mean_difference'])


def test_missing_and_declared_na_keep_their_slots_with_holm_one():
    # Catches favorable row removal without conflating a declared NA with bad data.
    parts = fixture()
    del parts[2]['fx_hourly-h6-w720-ACI_F']
    parts[2]['fx_hourly-h6-w720-ACI_QR']['receipt'].update(status='NA',reason='VALIDATION_INELIGIBLE')
    parts[2]['fx_hourly-h6-w720-SAV']['receipt'].update(status='NA',reason='NO_CONVERGED_START')
    summary, comparisons = run_fixture(parts)
    assert len(comparisons['rows']) == 56
    assert summary['status'] == 'INCOMPLETE_EVALUATION_INVENTORY'
    assert len(summary['method_rows']) == 24
    selected = [r for r in comparisons['rows'] if r['source']=='fx_hourly' and r['horizon']==6 and r['window']==720]
    assert len(selected) == 7
    assert all(r['raw_p'] is None and r['bookkeeping_p']==1. for r in selected)
    assert [r['reason'] for r in summary['method_rows'][:3]] == [
        'MISSING_EVALUATION_RECEIPT','VALIDATION_INELIGIBLE','NO_CONVERGED_START']


@pytest.mark.parametrize('change,code',[
    ('private_hash','PRIVATE_ARTIFACT_IDENTITY'),
    ('receipt_score','RECEIPT_SCORE_IDENTITY'),
    ('short_origins','ORIGIN_IDENTITY'),
    ('target','TARGET_FLOOR_IDENTITY'),
    ('floor','TARGET_FLOOR_IDENTITY'),
    ('validation','VALIDATION_INELIGIBLE'),
    ('gamma','SELECTED_GAMMA_IDENTITY'),
    ('execution','EXECUTABLE_FREEZE_IDENTITY'),
])
def test_complete_input_identity_discrepancy_stops_wp_instead_of_becoming_method_na(change,code):
    # Catches publishing a scientific summary after a required admission discrepancy.
    parts = fixture()
    key='fx_hourly-h6-w720-ACI_F'
    if change=='private_hash': parts[4][key]['provenance']['sha256']=OTHER
    elif change=='receipt_score': parts[2][key]['receipt']['scores']['full_hits']+=1
    elif change=='short_origins':
        trace=parts[4][key]['trace']
        for name in tuple(trace): trace[name]=trace[name][1:]
    elif change=='target': parts[4][key]['trace']['peak'][0]+=1.
    elif change=='floor': parts[4][key]['trace']['floor'][0]+=.5
    elif change=='validation': parts[3]['validation'][key]['status']='NA'
    elif change=='gamma': parts[2][key]['receipt']['selected_gamma']=.05
    elif change=='execution': parts[2][key]['receipt']['executable_freeze_sha256']=OTHER
    with pytest.raises(getattr(api(),'DataIdentityError',ValueError),match=code): run_fixture(parts)


def test_control_discrepancy_stops_wp_and_cannot_create_a_reduced_family():
    # Catches demoting changed original control outcomes to unavailable comparisons.
    parts=fixture()
    parts[5]['fx_hourly-h6-w720-QR']['trace']['peak'][0]+=1.
    with pytest.raises(getattr(api(),'DataIdentityError',ValueError),match='CONTROL_TARGET_FLOOR_IDENTITY'):
        run_fixture(parts)


def test_aci_rows_show_both_loss_and_coverage_changes_without_claiming_improvement():
    # Catches presenting the method name as calibration success or omitting adverse scores.
    summary, _ = run_fixture(fixture())
    row = summary['method_rows'][0]
    assert row['wrapped_minus_base_mean_loss'] == pytest.approx(-.025)
    assert row['wrapped_minus_base_coverage_distance'] == 0.
    pair = summary['aci_pairs'][0]
    assert 'wrapped_qr_minus_f_coverage_distance' in pair
    assert 'unwrapped_qr_minus_f_mean_loss' in pair
    assert 'unwrapped_qr_minus_f_coverage_distance' in pair


def test_public_reports_are_json_safe_aggregates_with_hashes_and_no_vectors():
    # Catches leaking actuals/capacities/loss vectors or losing the audit fingerprints.
    summary, comparisons = run_fixture(fixture())
    encoded = json.dumps([summary, comparisons], allow_nan=False)
    assert HASH in encoded and OTHER in encoded
    forbidden = {'origins','capacities','capacity','peak','floor','pinball','feedback_records','state_fractions'}
    def walk(value):
        assert not isinstance(value,np.ndarray)
        if isinstance(value,dict):
            assert not (set(value)&forbidden)
            for item in value.values(): walk(item)
        elif isinstance(value,(list,tuple)):
            for item in value: walk(item)
    walk(summary); walk(comparisons)


def test_invalid_frozen_family_or_unknown_receipt_is_rejected():
    # Catches silently rebuilding an easier hypothesis family after failures.
    parts = fixture()
    parts[1]['wp2_contrast_slots'].pop()
    with pytest.raises(ValueError): run_fixture(parts)
    parts = fixture()
    parts[2]['extra-undeclared-cell'] = parts[2]['fx_hourly-h6-w720-ACI_F']
    with pytest.raises(ValueError): run_fixture(parts)


def test_public_provenance_and_diagnostics_cannot_forward_private_vectors():
    # Catches accidental publication when a loader adds private fields to metadata.
    parts=fixture()
    parts[3]['private_arrays']={'peak':np.arange(10)}
    parts[2]['fx_hourly-h6-w720-ACI_F']['receipt']['diagnostics']['capacities']=np.arange(10)
    summary,comparisons=run_fixture(parts)
    encoded=json.dumps([summary,comparisons],allow_nan=False)
    assert 'private_arrays' not in encoded
    assert 'capacities' not in encoded


def test_holm_uses_all_56_slots_for_the_smallest_available_dm_p():
    # Catches calling adjustment on a reduced list despite reporting family_n=56.
    _summary,comparisons=run_fixture(fixture())
    available=[r for r in comparisons['rows'] if r['raw_p'] is not None]
    first=min(available,key=lambda r:r['raw_p'])
    assert first['holm_p']==pytest.approx(min(1.,56*first['raw_p']))
    assert any(r['dm_p'] != r['hln_p'] and r['raw_p']==r['dm_p'] for r in available)


def test_even_matching_missing_gamma_cannot_be_admitted_as_a_frozen_selection():
    # Catches treating None==None as a legal selection from the fixed gamma menu.
    parts=fixture()
    key='fx_hourly-h6-w720-ACI_F'
    parts[3]['validation'][key]['selected_gamma']=None
    parts[2][key]['receipt']['selected_gamma']=None
    with pytest.raises(api().DataIdentityError,match='SELECTED_GAMMA_IDENTITY'):
        run_fixture(parts)


def test_main_stops_before_archive_loading_if_any_evaluation_receipt_is_missing(tmp_path,monkeypatch):
    # Catches converting unfinished execution into a completed public science report.
    import hashlib
    import sys
    from types import SimpleNamespace
    module=api()
    spec,freeze,_receipts,_prov,_new,_old,_ln,_lo=fixture()
    def write(path,value):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(value))
        return hashlib.sha256(path.read_bytes()).hexdigest()
    spec_hash=write(tmp_path/'original-spec.json',spec)
    old_selection_hash=write(tmp_path/'original-selection.json',{})
    design={**freeze,'original_spec_sha256':spec_hash,
            'original_selection_sha256':old_selection_hash,'documents':{}}
    write(tmp_path/'protocol/revision-v6/design-freeze.json',design)
    cells={}
    for source,cfg in spec['sources'].items():
        for h in spec['horizons']:
            for w in cfg['windows']:
                for method in METHODS:
                    ident=f'{source}-h{h}-w{w}-{method}'
                    receipt={'status':'NA'}
                    fingerprint=write(tmp_path/f'results/revision-20261023/v6/wp2/validation-{ident}.json',receipt)
                    cells[ident]={'status':'NA','receipt_sha256':fingerprint,'selected_gamma':None}
    write(tmp_path/'results/revision-20261023/v6/wp2-selection-freeze.json',
          {'status':'FROZEN_BEFORE_WP2_EVALUATION','cell_count':24,'cells':cells})
    def no_archive(*_args,**_kwargs):
        pytest.fail('archive loader must not run before the 24-receipt admission gate')
    fake=SimpleNamespace(SPEC='original-spec.json',SELECTION='original-selection.json',
                         check_execution_freeze=lambda:HASH,original_trace=no_archive)
    monkeypatch.setitem(sys.modules,'v6_worker',fake)
    monkeypatch.setattr(module,'__file__',str(tmp_path/'v6_wp2_summary.py'))
    with pytest.raises(module.DataIdentityError,match='INCOMPLETE_EVALUATION_INVENTORY'):
        module.main([])
    assert not (tmp_path/'results/revision-20261023/v6/wp2-summary.json').exists()
    assert not (tmp_path/'results/revision-20261023/v6/wp2-comparisons.json').exists()


def test_main_refuses_to_overwrite_an_existing_public_report(tmp_path,monkeypatch):
    # Catches overwriting a prior aggregate rather than publishing via fresh files.
    import sys
    from types import SimpleNamespace
    module=api()
    monkeypatch.setitem(sys.modules,'v6_worker',SimpleNamespace())
    monkeypatch.setattr(module,'__file__',str(tmp_path/'v6_wp2_summary.py'))
    output=tmp_path/'results/revision-20261023/v6/wp2-summary.json'
    output.parent.mkdir(parents=True)
    output.write_text('protected prior report')
    with pytest.raises(FileExistsError):module.main([])
    assert output.read_text()=='protected prior report'
    assert not (output.parent/'wp2-comparisons.json').exists()
