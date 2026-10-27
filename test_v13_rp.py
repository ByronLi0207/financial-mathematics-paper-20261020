"""Toy-only screens for the fixed retrospective v13 benchmark gate."""
import math
import numpy as np


def test_gate_exact_hac_bandwidth_and_standard_error():
    from v13_rp import paired_gate
    from inference_tests import bandwidth,hac
    d=np.sin(np.arange(156)/9)-.6
    out=paired_gate(d,np.zeros(156),6)
    omega=float(hac(d,bandwidth(156,6))[0,0])
    assert out['bandwidth']==bandwidth(156,6)
    assert out['lrv']==omega
    assert out['standard_error']==math.sqrt(omega/156)
    assert out['mean_difference']==math.fsum(map(float,d))/156
    assert out['route']==('QR' if -out['mean_difference']>out['standard_error'] else 'F')


def test_gate_defaults_when_equal_and_accepts_constant_strict_benefit():
    from v13_rp import paired_gate
    same=paired_gate(np.ones(52),np.ones(52),24)
    assert same['route']=='F' and same['standard_error']==0
    better=paired_gate(np.zeros(52),np.ones(52),24)
    assert better['route']=='QR' and better['standard_error']==0
    worse=paired_gate(np.ones(52),np.zeros(52),24)
    assert worse['route']=='F'


def test_gate_requires_strictly_more_than_one_standard_error():
    from v13_rp import decision_from_evidence
    assert decision_from_evidence(-1.,1.)=='F'
    assert decision_from_evidence(0.,0.)=='F'
    assert decision_from_evidence(-1.000001,1.)=='QR'


def test_nonfinite_gate_is_explicitly_unavailable_with_defaultF():
    from v13_rp import paired_gate
    out=paired_gate([0.,float('nan')],[1.,1.],1)
    assert out['status']=='UNAVAILABLE' and out['route']=='F'
    assert out['reason']=='NONFINITE_PAIRED_LOSSES'


def test_grid_contains_fixed60_weekly_and_two_feasibleFX():
    from v13_rp import rp_cells
    from v12_decomposition import CFTC_SOURCE_KEYS,PANEL_SOURCE_KEYS
    sources=[dict(family='cftc',key=k,N=877,short_scale=6,long_scale=26,nominal_gap_seconds=604800) for k in CFTC_SOURCE_KEYS]
    sources += [dict(family='bill' if i==0 else 'panel',key=k,N=706,short_scale=6,long_scale=26,nominal_gap_seconds=604800) for i,k in enumerate(('PDPOSGS-B',*PANEL_SOURCE_KEYS))]
    sources += [dict(family='fx',key='fx_hourly',N=18576,short_scale=24,long_scale=168,nominal_gap_seconds=3600)]
    cells=rp_cells(sources)
    assert len(cells)==62
    assert all(c['horizon']==6 for c in cells[:13])
    assert all(c['horizon']==24 for c in cells[13:26])
    assert sum(c['family']!='fx' for c in cells)==60
    assert len({c['cell_id'] for c in cells})==62
    assert {c['validation_n'] for c in cells if c['family']=='fx'}=={5760}
    assert min(c['validation_first']-c['horizon']-c['window']+1 for c in cells if c['family']=='fx')==330
    assert all(c['validation_last']+c['horizon']<c['evaluation_first'] for c in cells)


def toy_rows():
    from v13_rp import expected_slots
    rows=[]
    for s in expected_slots():
        rows.append(dict(s,rp_status='COMPLETE',ordinary_status='COMPLETE',F_status='COMPLETE',
            reference_loss=10.,rp_loss=10.,ordinary_loss=11.,rp_relative_loss_pct=0.,ordinary_relative_loss_pct=10.,route='F'))
    for r in rows:
        if r['family']=='fx':r.update(ordinary_loss=8.,ordinary_relative_loss_pct=-20.,rp_loss=9.,rp_relative_loss_pct=-10.,route='QR')
    return rows


def test_fixed_universe_r1_r2_and_half_gainR3():
    from v13_rp import summarize_rp
    out=summarize_rp(toy_rows())
    assert out['R1']=='SUPPORTED' and out['R2']=='SUPPORTED' and out['R3']=='SUPPORTED'
    assert out['weekly']['planned']==60 and out['weekly']['median_relative_loss_pct']==0
    assert out['weekly']['fallback_count']==60
    assert out['FX']['periods']['early2015']['half_gain_threshold_pct']==-10


def test_r3_is_each_period_not_pooled_or_selected_best():
    from v13_rp import summarize_rp
    rows=toy_rows()
    for r in rows:
        if r['family']=='fx' and r['period']=='early2015':r['rp_relative_loss_pct']=-9.
    assert summarize_rp(rows)['R3']=='NOT_SUPPORTED'


def test_missing_weekly_slot_keeps_full_denominator_and_unknown_median():
    from v13_rp import summarize_rp
    rows=toy_rows();rows.pop(0)
    out=summarize_rp(rows)
    assert out['R1']=='UNDETERMINED' and out['R2']=='UNDETERMINED'
    assert out['weekly']['planned']==60 and out['weekly']['complete']==59
    assert out['weekly']['median_relative_loss_pct'] is None
    assert out['weekly']['fallback_fraction_of_planned']==59/60


def test_four_known_adverse_cells_fail_r2_even_with_missing_slot():
    from v13_rp import summarize_rp
    rows=toy_rows();rows.pop(0)
    for r in rows[:4]:r['rp_relative_loss_pct']=10.0001
    assert summarize_rp(rows)['R2']=='NOT_SUPPORTED'


def test_trace_loss_reader_rejects_changed_bytes(tmp_path):
    import hashlib
    from v13_rp_runner import trace_losses
    folder=tmp_path/'abc';folder.mkdir()
    np.savez_compressed(folder/'trace.npz',origins=np.arange(6),losses=np.arange(6,dtype=float))
    raw=(folder/'trace.npz').read_bytes()
    attempt=dict(status='COMPLETE',cache_key='abc',cache_source='v13',trace_sha256=hashlib.sha256(raw).hexdigest(),trace_bytes=len(raw),trace_path='trace.npz')
    assert np.array_equal(trace_losses(attempt,np.arange(6),tmp_path,tmp_path/'old'),np.arange(6))
    (folder/'trace.npz').write_bytes(raw+b'changed')
    import pytest
    with pytest.raises(ValueError,match='TRACE_HASH_OR_SIZE'):trace_losses(attempt,np.arange(6),tmp_path,tmp_path/'old')


def test_failed_long_candidate_never_counts_as_successful_defaultF(tmp_path,monkeypatch):
    import hashlib,json
    from v12_forecast import make_context
    from v12_inputs import load_series
    from v12_runner import _identity
    import v13_rp_runner as runner
    csv=tmp_path/'toy.csv';dates=np.datetime64('2020-01-01')+np.arange(180)*np.timedelta64(7,'D')
    csv.write_text('As Of Date,Time Series,Value (millions)\n'+'\n'.join(f'{d},toy,{10+np.sin(i/7)}' for i,d in enumerate(dates))+'\n')
    source=dict(family='bill',key='toy',path=str(csv),sha256=hashlib.sha256(csv.read_bytes()).hexdigest(),bytes=csv.stat().st_size,N=180,unit='toy units')
    cell=dict(experiment='G3',cell_id='toy',family='bill',source_key='toy',period='original',horizon=6,window=52,refit_step=13,short_scale=6,long_scale=26,nominal_gap_seconds=604800,tau=.95,validation_first=100,validation_last=111,validation_n=12,baseline_validation_first=100,baseline_validation_last=105,baseline_validation_n=6,evaluation_first=130,evaluation_last=139,evaluation_n=10,eligible=True,source=source)
    context=make_context(load_series(source),cell);ids=np.arange(100,112,dtype=np.int64)
    identity,key,_,_=_identity(context,source,ids,'QR33',.001,.95)
    old=tmp_path/'old';folder=old/key;folder.mkdir(parents=True)
    (folder/'terminal.json').write_text(json.dumps(dict(identity=identity,status='FAILED',reason='OLD_FAILURE')))
    real=runner.attempt_cached;checked=[]
    def evidence_before_eval(context,source,ids,*args,**kw):
        if int(ids[0])==130:
            assert (tmp_path/'private'/'choices.json').exists()
            checked.append(True)
        return real(context,source,ids,*args,**kw)
    monkeypatch.setattr(runner,'attempt_cached',evidence_before_eval)
    got=runner.compute_rp(cell,tmp_path/'new',old,tmp_path/'private',None)
    assert got['row']['rp_status']=='FAILED'
    assert got['row']['route'] is None
    assert got['row']['route_qr_indicator'] is None
    assert got['row']['F_status']=='COMPLETE'
    assert len([c for c in got['candidates'] if c['segment']=='long_validation'])==6
    assert len([c for c in got['candidates'] if c['segment']=='ordinary_validation'])==6
    assert checked
