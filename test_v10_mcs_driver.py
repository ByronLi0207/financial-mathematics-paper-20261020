"""Artificial registries and byte fixtures only; no saved financial NPZ reads."""
from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest


def api():
    assert importlib.util.find_spec('run_v10_mcs') is not None, 'MCS driver is missing'
    return importlib.import_module('run_v10_mcs')


def method(name, floor):
    return dict(method_id=name, method_class='matched_historical' if name == 'F' else 'conditional',
        aliases=[name], provenance={'source_rows': [{'method': name, 'source': 'ARTIFICIAL'}]},
        origins=np.arange(10, 14), capacity=np.array([3., 4., 5., 6.]),
        target=np.array([4., 5., 6., 7.]), loss=np.array([.95, .95, .95, .95]),
        floor=np.ones(4) if floor else None)


def registry():
    identity = dict(period='artificial_only', normalized_source='artificial', horizon=6, window=52)
    ready = dict(identity=identity, group_label='Treasury bills', status='READY',
        methods=[method('QR4', False), method('F', True)], unavailable_methods=[],
        planned_methods=[], errors=[], alias_discrepancies=[])
    failed = dict(identity=dict(identity, window=260), group_label='Treasury bills', status='FAILED_INPUT',
        methods=[method('F', True)], planned_methods=[
            {'method_id': 'F', 'method_class': 'matched_historical', 'aliases': ['F'], 'provenance': {}},
            {'method_id': 'missingQR', 'method_class': 'conditional', 'aliases': ['missingQR'], 'provenance': {}}],
        unavailable_methods=[{'method_id': 'oldNA', 'method_class': 'conditional', 'status': 'NA', 'reason': 'known'}],
        errors=[{'method_id': 'missingQR', 'reason': 'ARTIFICIAL_MISSING_VECTOR'}], alias_discrepancies=[])
    return dict(groups=[ready, failed], counts={'comparison_groups': 2})


def test_registry_persists_only_private_vectors_and_public_metadata(tmp_path):
    m = api(); r = registry(); original = deepcopy(r)
    public = tmp_path/'results/v10/mcs'; private = tmp_path/'.scratch/v10/mcs-inputs'
    index = m.persist_registry(r, public, private, tmp_path)
    assert json.loads((public/'input-index.json').read_text()) == index
    assert not list(public.rglob('*.npz'))
    ready = index['groups'][0]
    assert [v['method_id'] for v in ready['methods']] == ['F', 'QR4']
    assert ready['methods'][0]['column_index'] == 0 and ready['methods'][1]['column_index'] == 1
    assert ready['methods'][0]['floor_key'] == 'floor_000'
    assert ready['methods'][1]['floor_key'] is None
    text = (public/'input-index.json').read_text()
    assert '3.0, 4.0, 5.0, 6.0' not in text and '0.95, 0.95' not in text
    arrays = m.load_group_arrays(ready, tmp_path)
    assert set(arrays) == {'origins', 'peak', 'loss_matrix', 'capacities_matrix', 'floor_000'}
    assert arrays['loss_matrix'].shape == (4, 2)
    np.testing.assert_array_equal(arrays['origins'], np.arange(10, 14))
    np.testing.assert_array_equal(arrays['capacities_matrix'][:, 1], original['groups'][0]['methods'][0]['capacity'])
    assert arrays['floor_000'].shape == (4,)
    assert r['groups'][0]['methods'][0]['floor'] is None


def test_failed_group_retains_all_planned_classes_and_no_matrix(tmp_path):
    m = api(); index = m.persist_registry(registry(), tmp_path/'public', tmp_path/'.scratch/private', tmp_path)
    failed = index['groups'][1]
    assert failed['status'] == 'FAILED_INPUT'
    assert [v['method_id'] for v in failed['methods']] == ['F', 'missingQR']
    assert failed['methods'][1]['method_class'] == 'conditional'
    assert failed['unavailable_methods'][0]['method_id'] == 'oldNA'
    assert failed.get('private_path') is None
    assert len(list((tmp_path/'.scratch/private').glob('*.npz'))) == 1


def test_changed_private_group_bytes_are_rejected_before_loading(tmp_path):
    m = api(); index = m.persist_registry(registry(), tmp_path/'public', tmp_path/'.scratch/private', tmp_path)
    group = index['groups'][0]
    path = tmp_path/group['private_path']; path.write_bytes(path.read_bytes()+b'changed')
    with pytest.raises(ValueError): m.load_group_arrays(group, tmp_path)


def test_wrong_shape_or_array_digest_is_rejected_even_with_original_file(tmp_path):
    m = api(); index = m.persist_registry(registry(), tmp_path/'public', tmp_path/'.scratch/private', tmp_path)
    bad = deepcopy(index['groups'][0]); bad['arrays']['loss_matrix']['shape'] = [3, 2]
    with pytest.raises(ValueError): m.load_group_arrays(bad, tmp_path)
    bad = deepcopy(index['groups'][0]); bad['arrays']['origins']['sha256'] = '0'*64
    with pytest.raises(ValueError): m.load_group_arrays(bad, tmp_path)


def test_upstream_private_and_public_file_changes_are_rejected(tmp_path):
    m = api(); private = tmp_path/'.scratch/copied.npz'; private.parent.mkdir(); private.write_bytes(b'artificial-copy')
    public = tmp_path/'results/trace.npz'; public.parent.mkdir(); public.write_bytes(b'artificial-public')
    import hashlib
    inventory = {'minimum_core_private_copy_manifest': [dict(path='/old/ignored.npz', proposed_scratch_relative=str(private.relative_to(tmp_path)), bytes=private.stat().st_size, sha256=hashlib.sha256(private.read_bytes()).hexdigest())]}
    cftc = [dict(trace_path=str(public.relative_to(tmp_path)), trace_bytes=public.stat().st_size, trace_sha256=hashlib.sha256(public.read_bytes()).hexdigest())]
    assert m.verify_input_files(inventory, cftc, tmp_path)
    private.write_bytes(b'changed')
    with pytest.raises(ValueError): m.verify_input_files(inventory, cftc, tmp_path)
    private.write_bytes(b'artificial-copy'); public.write_bytes(b'changed')
    with pytest.raises(ValueError): m.verify_input_files(inventory, cftc, tmp_path)


def test_cftc_augmentation_uses_saved_split_metadata_and_literal_code():
    rows = [dict(code='00001+', window=52, method='F', status='COMPLETE', trace_path='fake')]
    got = api().augment_cftc_rows(rows, {'indices': {'evaluation_first': 611, 'evaluation_last': 870, 'evaluation_n': 260}, 'horizon': 6})
    assert got[0]['normalized_source'] == 'cftc:00001+'
    assert got[0]['family'] == 'CFTC' and got[0]['period'] == 'economic_date_replay_2021_2026'
    assert got[0]['origin_count'] == 260 and got[0]['first_origin'] == 611 and got[0]['last_origin'] == 870
    assert 'family' not in rows[0]


def test_cftc_axis_must_match_committed_E2_manifest_before_materialization(tmp_path, monkeypatch):
    m = api(); monkeypatch.setattr(m, 'ROOT', tmp_path)
    import hashlib
    paths = {'saved_inventory': 'inventory.json', 'new_cftc_inventory': 'cftc.json', 'new_cftc_eligibility': 'eligibility.json'}
    data = {'saved_inventory': {}, 'new_cftc_inventory': [{'code': 'ARTIFICIAL', 'window': 52, 'method': 'F'}], 'new_cftc_eligibility': {}}
    d = {}
    for key, relative in paths.items():
        path = tmp_path/relative; path.write_text(json.dumps(data[key]))
        d[key] = relative; d[key+'_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    folder = tmp_path/'results/v10/cftc'; folder.mkdir(parents=True)
    (folder/'splits.json').write_text(json.dumps({'indices': {'evaluation_first': 611, 'evaluation_last': 870, 'evaluation_n': 260}, 'horizon': 6}))
    (folder/'manifest.json').write_text(json.dumps({'prepared_sha256': {'splits.json': '0'*64}}))
    seen = []
    monkeypatch.setattr(m, 'committed_file', lambda path, *args: seen.append(Path(path)) or {})
    with pytest.raises(ValueError): m.metadata_inputs(d)
    assert folder/'splits.json' in seen and folder/'manifest.json' in seen
