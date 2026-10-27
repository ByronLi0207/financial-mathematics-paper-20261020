"""Artificial driver receipts; no real saved predictions or study runs."""
import csv,hashlib,io,json,zipfile
import numpy as np
import pytest
import run_v10_cost as d

def setup(tmp_path,monkeypatch):
    monkeypatch.setattr(d,'ROOT',tmp_path);monkeypatch.setattr(d,'PUBLIC',tmp_path/'cost');d.PUBLIC.mkdir()
    protocol=tmp_path/'design.md';protocol.write_text('inventedtestprotocol');monkeypatch.setattr(d,'DESIGN',protocol)
    (tmp_path/'inventory.json').write_text('{}')
    (tmp_path/'index.json').write_text('{}');mp=tmp_path/'results/v10/mcs/manifest.json';mp.parent.mkdir(parents=True);mp.write_text('{}')
    design=dict(inventory='inventory.json',mcs_index='index.json',inventory_sha256=d.sha(tmp_path/'inventory.json'),mcs_index_sha256=d.sha(tmp_path/'index.json'),reference_id='F',grid=dict(kappa=[.05,.1],beta=[0,1],c=[1]),primary_c=1,primary_method_by_group={'Artificial':'QR'},run_limit_seconds=60)
    manifest=dict(design=design,design_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest(),code_sha256={},mcs_manifest_sha256=d.sha(mp))
    monkeypatch.setattr(d,'design',lambda:design)
    (d.PUBLIC/'manifest.json').write_text(json.dumps(manifest))
    group=dict(identity=dict(period='toy',normalized_source='invented',horizon=1,window=2),group_label='Artificial',unavailable_methods=[{'method_id':'knownNA'}])
    calls=[]
    monkeypatch.setattr(d,'committed',lambda p:None)
    monkeypatch.setattr(d,'verify_source',lambda:(calls.append('verify') or {'groups':[group]}))
    import v10_cost_inputs
    monkeypatch.setattr(v10_cost_inputs,'load_cost_group',lambda *a:dict(origins=np.array([1,2]),target=np.array([3.,5.]),floor=np.array([1.,1.]),capacities={'F':np.array([4.,4.]),'QR':np.array([3.,3.])},recovery_receipts=[]))
    return calls

def test_one_artificial_run_publishes_all_coefficients_and_full_denominators(tmp_path,monkeypatch):
    calls=setup(tmp_path,monkeypatch);d.run()
    s=json.loads((d.PUBLIC/'summary.json').read_text());assert s['comparisons']==s['complete']==1
    assert s['cost_rows']==8 and s['primary_region_rows']==4 and s['grid_points']==4
    assert calls==['verify','verify']
    with zipfile.ZipFile(d.PUBLIC/'cost-grid.csv.zip') as z:
        rows=list(csv.DictReader(io.StringIO(z.read('cost-grid.csv').decode())))
    assert len(rows)==8 and {r['method_id'] for r in rows}=={'F','QR'}
    assert all(float(r['difference'])==0 for r in rows if r['method_id']=='F')
    cells=json.loads((d.PUBLIC/'cells.json').read_text());assert cells[0]['known_na']==[{'method_id':'knownNA'}]
    with pytest.raises(FileExistsError):d.run()

def test_bad_input_is_whole_comparison_unknown_not_a_partial_subset(tmp_path,monkeypatch):
    setup(tmp_path,monkeypatch)
    import v10_cost_inputs
    def fail(*a):raise ValueError('targetmismatch')
    monkeypatch.setattr(v10_cost_inputs,'load_cost_group',fail);d.run()
    s=json.loads((d.PUBLIC/'summary.json').read_text());assert s['complete']==0 and s['unavailable']==1 and s['cost_rows']==0
    with (d.PUBLIC/'primary-regions.csv').open() as f:unknown=list(csv.DictReader(f))
    assert len(unknown)==4 and all(r['status']=='UNAVAILABLE' and r['difference']=='' for r in unknown)
    rows=json.loads((d.PUBLIC/'group-regions.json').read_text());assert len(rows)==4
    assert all(r['planned']==1 and r['complete']==0 and r['lower']==0 and r['upper']==1 for r in rows)


def test_pinned_inventory_change_stops_before_any_input_loader(tmp_path,monkeypatch):
    calls=setup(tmp_path,monkeypatch)
    (tmp_path/'inventory.json').write_text('{"changed":true}')
    with pytest.raises(AssertionError):d.run()
    assert calls==[] and not (d.PUBLIC/'run-start.json').exists()
