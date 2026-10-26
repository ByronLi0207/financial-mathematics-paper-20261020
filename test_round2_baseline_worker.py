"""Worker regression: a successful fit must not be mislabeled NA by duplicate keys."""
import numpy as np
from round2_baselines_run import comparison_row

def test_comparison_retains_dm_status_once_and_identical_losses_are_not_failed_cells():
    loss=np.array([1.,2.,3.,4.,5.,6.,7.,8.])
    ref={'pinball':loss,'peak':np.ones(8),'capacity':np.ones(8)}
    row=comparison_row('synthetic',2,52,'FHS','frozen_F',loss,ref)
    assert row['status']=='IDENTICAL_LOSSES'
    assert row['relative_loss_percent']==0.
    assert row['dm_p'] is None
    assert row['reference_strict_breaches']==0
    assert row['left_method']=='FHS' and row['right_method']=='frozen_F'

def test_comparison_loss_direction_and_reference_hits_match_inputs():
    left=np.arange(1.,101.)*.8
    ref={'pinball':np.arange(1.,101.),'peak':np.full(100,2.),'capacity':np.r_[np.zeros(50),np.full(50,3.)]}
    row=comparison_row('synthetic',6,52,'QRF','QR',left,ref)
    assert abs(row['relative_loss_percent']+20)<1e-12
    assert row['status']=='OK' and row['dm_t']<0
    assert row['reference_strict_breaches']==50
    assert row['post_result'] and row['exploratory']


def test_qrf_checkpoint_adapter_calls_strict_guard_without_diagnostic_keywords():
    from round2_baselines_run import resource_checkpoint
    from round2_qrf import qrf_forecast
    from conditional_study import StudyConfig
    calls=[]
    def strict_guard(*,stage=None,completed_origins=None):
        calls.append((stage,completed_origins))
    x=np.arange(220,dtype=float);t=np.datetime64('2020-01-01')+np.arange(len(x))*np.timedelta64(1,'h')
    r=qrf_forecast(x,t,np.arange(100,104),StudyConfig(6,52,4,6,26,3600),checkpoint=resource_checkpoint(strict_guard))
    assert len(r['capacity'])==4
    assert calls[0]==('qrf_refit',0) and calls[-1]==('qrf_issue',4)


def _worker_fixture(monkeypatch,case):
    # Retained task-owned scratch fixtures: no teardown or removal is requested.
    import json,uuid
    from types import SimpleNamespace
    import round2_baselines_run as worker
    import round2_qrf
    import run_v3_inference
    path=worker.ROOT/'.scratch/round2'/('baseline-worker-test-'+case+'-'+uuid.uuid4().hex[:8])
    protocol=path/'protocol/revision-20261022/study-spec.json';protocol.parent.mkdir(parents=True,exist_ok=False)
    protocol.write_text((worker.ROOT/'protocol/revision-20261022/study-spec.json').read_text())
    monkeypatch.setattr(worker,'ROOT',path);monkeypatch.setattr(worker,'OUT',path/'out')
    monkeypatch.setattr(worker,'identity',lambda _: '0'*64)
    monkeypatch.setattr(worker.metadata,'version',lambda _: 'synthetic-test')
    monkeypatch.setattr(worker,'load_source',lambda *a,**k: SimpleNamespace(position=np.arange(130.),dates=np.datetime64('2020-01-01')+np.arange(130)*np.timedelta64(1,'h')))
    o=np.arange(100,108);peak=np.full(8,120.);floor=o.astype(float);cap=np.full(8,115.);loss=.95*(peak-cap)
    ref=dict(origins=o,peak=peak,floor=floor,capacity=cap,pinball=loss)
    monkeypatch.setattr(run_v3_inference,'traces',lambda:{('fx_hourly',6,720,m):ref for m in ('QR','frozen_F')})
    monkeypatch.setattr(round2_qrf,'qrf_forecast',lambda *a,**k:dict(capacity=cap.copy(),refits=[dict(refit_index=100)],refit_indices=np.full(8,100)))
    class Guard:
        def __init__(self,*a):self.resources=dict(peak_rss_bytes=1,elapsed_seconds=.01,maximum_observed_os_threads=1)
        def __call__(self,**kw):
            if case=='resource' and kw['stage']=='D1_complete_or_NA':raise RuntimeError('synthetic resource limit')
    monkeypatch.setattr(worker,'RunGuard',Guard)
    if case=='setup':
        def bad(*a,**k):raise ValueError('synthetic source identity failure')
        monkeypatch.setattr(worker,'load_source',bad)
    worker.cell('fx_hourly',6,720,'QRF')
    return json.loads((path/'out/fx_hourly-h6-w720-QRF.json').read_text())


def test_successful_worker_saves_complete_cell_and_both_comparisons(monkeypatch):
    r=_worker_fixture(monkeypatch,'complete')
    assert r['status']=='COMPLETE' and len(r['comparisons'])==2
    assert r['evaluation']['origin_count']==8
    assert all(a['status']=='IDENTICAL_LOSSES' for a in r['comparisons'])


def test_resource_failure_keeps_visible_reason_and_no_scored_cell(monkeypatch):
    r=_worker_fixture(monkeypatch,'resource')
    assert r['status']=='NA' and r['failure_reason']=='synthetic resource limit'
    assert r['failure_type']=='RuntimeError' and r['resource_failure_type']=='RuntimeError'
    assert r['evaluation'] is None and r['comparisons']==[]
    assert r['completed_origin_count']==8


def test_setup_failure_yields_retained_NA_receipt_without_partial_average(monkeypatch):
    r=_worker_fixture(monkeypatch,'setup')
    assert r['status']=='NA' and r['failure_reason']=='synthetic source identity failure'
    assert r['failure_type']=='ValueError' and r['completed_origin_count']==0
    assert r['evaluation'] is None and r['comparisons']==[]


def test_nonfinite_failed_optimizer_diagnostics_are_explicit_nulls_not_numbers():
    from round2_baselines_run import sanitize_diagnostics
    import json
    raw={'status':'NA','failure_context':{'optimizer':{'objective':float('inf'),'parameters':[float('nan'),2.,-float('inf')]}}}
    clean,events=sanitize_diagnostics(raw)
    assert clean['failure_context']['optimizer']=={'objective':None,'parameters':[None,2.,None]}
    assert [x['path'] for x in events]==['failure_context.optimizer.objective','failure_context.optimizer.parameters[0]','failure_context.optimizer.parameters[2]']
    assert [x['original_nonfinite_token'] for x in events]==['inf','nan','-inf']
    assert all(x['conversion']=='null, not a numeric estimate' for x in events)
    assert 'NaN' not in json.dumps(clean,allow_nan=False) and 'Infinity' not in json.dumps(clean,allow_nan=False)
    assert np.isnan(raw['failure_context']['optimizer']['parameters'][0])
