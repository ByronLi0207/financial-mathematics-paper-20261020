"""Once-attempt runner checks on pinned, constructed local CSVs only."""
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
import pytest

from conditional_quantile import QuantileFitError


def api():
    assert importlib.util.find_spec('v12_runner') is not None, 'v12 runner is missing'
    return importlib.import_module('v12_runner')


def fixture(root, experiment='F1', tau=.95):
    root = root.resolve(); path = root/'toy.csv'; t = np.arange(220)
    dates = np.datetime64('2000-01-03') + t*np.timedelta64(7, 'D')
    x = 10.+.001*t*t+.2*np.sin(t/7.)
    raw = ('As Of Date,Time Series,Value (millions)\n'+''.join(
        f'{day},PDPOSGS-B,{v:.17g}\n' for day,v in zip(dates,x))).encode()
    path.write_bytes(raw)
    source = dict(path=str(path),family='bill',key='PDPOSGS-B',unit='toy units',
        N=220,raw_rows=220,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
        short_scale=6,long_scale=26,nominal_gap_seconds=604800)
    cell = dict(cell_id=f'{experiment}-TOY-W52-V4-tau{tau}',experiment=experiment,
        family='bill',source_key='PDPOSGS-B',source_index=None,period='original',
        horizon=6,window=52,refit_step=3,short_scale=6,long_scale=26,
        nominal_gap_seconds=604800,tau=tau,validation_first=130,validation_last=133,
        validation_n=4,evaluation_first=145,evaluation_last=149,evaluation_n=5,source=source)
    return cell, root/'cache', root/'output'


def tracked_predictions(monkeypatch, m, callback=None):
    real = m.predict_segment; seen=[]
    def predict(context, origins, method, penalty=None, **kwargs):
        seen.append((int(origins[0]),method,penalty))
        if callback: callback(context,origins,method,penalty)
        return real(context,origins,method,penalty,**kwargs)
    monkeypatch.setattr(m,'predict_segment',predict)
    return seen


def test_f1_seals_all_validation_choices_before_any_evaluation_and_reuses_cache(tmp_path, monkeypatch):
    m=api(); cell,cache,out=fixture(tmp_path)
    def inspect(context,ids,method,penalty):
        started=list(cache.glob('*/attempt.json'))
        assert started, 'exclusive STARTED marker must precede prediction'
        if int(ids[0])==145:
            for family in ('QR33','QR4'):
                seal=json.loads((out/cell['cell_id']/f'{family}.selection.json').read_text())
                assert seal['selection']['status']=='SELECTED'
            if method=='QR4':
                completed=json.loads((out/cell['cell_id']/'QR33.result.json').read_text())
                assert completed['status']=='COMPLETE'
    seen=tracked_predictions(monkeypatch,m,inspect)
    result=m.compute_cell(cell,'F1',cache,out)
    assert [r['method'] for r in result['rows']]==['QR33','QR4']
    assert all(r['status']=='COMPLETE' for r in result['rows'])
    assert len(result['candidates'])==24
    assert len(seen)==23  # 10 finite per segment; shared I twice; eval F once.
    assert all(r['n']==(4 if r['segment']=='validation' else 5)
               for r in result['candidates'])
    for row in result['rows']:
        assert row['actual_excess_pct']==row['relative_loss_pct']
        assert row['actual_excess_pct']==pytest.approx(
            row['selection_component_pct']+row['signal_gap_pct'])
    before=len(seen)
    again=m.compute_cell(cell,'F1',cache,out)
    assert len(seen)==before and all(r['status']=='COMPLETE' for r in again['rows'])
    for candidate in again['candidates']:
        entry=json.loads((cache/candidate['cache_key']/'terminal.json').read_text())
        trace=cache/candidate['cache_key']/entry['trace_path']
        assert hashlib.sha256(trace.read_bytes()).hexdigest()==entry['trace_sha256']
        with np.load(trace,allow_pickle=False) as z:
            assert set(z.files)=={'origins','capacity','target','floor','losses','refit_indices'}


@pytest.mark.parametrize('experiment,methods', [('F2',['QR33','QR4']),('F3',['QR33'])])
def test_later_experiments_evaluate_only_the_frozen_selection(tmp_path, experiment, methods):
    m=api();cell,cache,out=fixture(tmp_path,experiment)
    result=m.compute_cell(cell,experiment,cache,out)
    assert [r['method'] for r in result['rows']]==methods
    for method in methods:
        val=[r for r in result['candidates'] if r['method']==method and r['segment']=='validation']
        ev=[r for r in result['candidates'] if r['method']==method and r['segment']=='evaluation']
        assert len(val)==6 and len(ev)==1
        row=next(r for r in result['rows'] if r['method']==method)
        assert ev[0]['penalty']==row['selected_penalty']
        assert row['selection_component_pct'] is None and row['signal_gap_pct'] is None
        assert row['relative_loss_pct']==row['actual_excess_pct']


def test_failed_cache_is_terminal_for_both_first_attempt_and_reuse(tmp_path, monkeypatch):
    m=api();cell,cache,out=fixture(tmp_path);real=m.predict_segment;failures=[]
    def fail(context,ids,method,penalty=None,**kwargs):
        if int(ids[0])==130 and method=='QR33' and penalty==.001:
            failures.append(1)
            raise QuantileFitError('TOY_FIT_FAILURE',{'iterations':10000})
        return real(context,ids,method,penalty,**kwargs)
    monkeypatch.setattr(m,'predict_segment',fail)
    for _ in range(2):
        result=m.compute_cell(cell,'F1',cache,out)
        row=next(r for r in result['rows'] if r['method']=='QR33')
        assert row['status']=='FAILED' and row['selected_penalty'] is None
        failed=next(r for r in result['candidates'] if r['method']=='QR33' and r['penalty']==.001)
        assert failed['reason']=='TOY_FIT_FAILURE'
        assert not any(r['method']=='QR33' and r['segment']=='evaluation'
                       for r in result['candidates'])
    assert len(failures)==1


@pytest.mark.parametrize('damage', ['stale_started','trace_bytes','terminal_geometry','trace_path_escape'])
def test_stale_or_corrupt_completed_entries_never_trigger_another_fit(tmp_path, monkeypatch, damage):
    m=api();cell,cache,out=fixture(tmp_path);first=m.compute_cell(cell,'F1',cache,out)
    candidate=next(r for r in first['candidates'] if r['method']=='QR33' and r['penalty']==.001)
    entry=cache/candidate['cache_key'];terminal=json.loads((entry/'terminal.json').read_text())
    if damage=='stale_started': (entry/'terminal.json').unlink()
    elif damage=='trace_bytes':
        trace=entry/terminal['trace_path'];trace.write_bytes(trace.read_bytes()+b'corrupt')
    elif damage=='terminal_geometry':
        terminal['identity']['window']=260
        (entry/'terminal.json').write_text(json.dumps(terminal))
    else:
        foreign=cache/'foreign';foreign.mkdir()
        (foreign/'trace.npz').write_bytes((entry/'trace.npz').read_bytes())
        terminal['trace_path']='../foreign/trace.npz'
        (entry/'terminal.json').write_text(json.dumps(terminal))
    seen=tracked_predictions(monkeypatch,m)
    result=m.compute_cell(cell,'F1',cache,out/'resumed')
    assert not seen
    assert next(r for r in result['rows'] if r['method']=='QR33')['status']=='FAILED'


@pytest.mark.parametrize('resource_failure', [False,True])
def test_f1_evaluation_failure_keeps_original_reason_on_method_row(tmp_path,monkeypatch,resource_failure):
    m=api();cell,cache,out=fixture(tmp_path);real=m.predict_segment
    def fail(context,ids,method,penalty=None,**kwargs):
        if int(ids[0])==145 and method=='QR33' and penalty==.001:
            if resource_failure: raise m.ResourceStop('RESOURCE_TOY_ACTIVE')
            raise QuantileFitError('TOY_EVALUATION_FAILURE',{'iterations':10000})
        return real(context,ids,method,penalty,**kwargs)
    monkeypatch.setattr(m,'predict_segment',fail)
    result=m.compute_cell(cell,'F1',cache,out)
    row=next(r for r in result['rows'] if r['method']=='QR33')
    assert row['status']==('FAILED_RESOURCE' if resource_failure else 'FAILED')
    assert row['reason']==('RESOURCE_TOY_ACTIVE' if resource_failure else 'TOY_EVALUATION_FAILURE')


def test_truncated_prediction_is_not_scored_as_a_complete_cache_entry(tmp_path, monkeypatch):
    m=api();cell,cache,out=fixture(tmp_path);real=m.predict_segment
    def short(context,ids,method,penalty=None,**kwargs):
        report=real(context,ids,method,penalty,**kwargs)
        if method=='QR33' and int(ids[0])==130:
            for key in ('origins','capacity','refit_indices'): report[key]=report[key][:-1]
        return report
    monkeypatch.setattr(m,'predict_segment',short)
    result=m.compute_cell(cell,'F1',cache,out)
    assert next(r for r in result['rows'] if r['method']=='QR33')['status']=='FAILED'
    assert all(r['status']=='FAILED' for r in result['candidates']
               if r['method']=='QR33' and r['segment']=='validation' and r['penalty']!='inf')


def test_expired_deadline_preserves_unattempted_resource_status(tmp_path, monkeypatch):
    m=api();cell,cache,out=fixture(tmp_path)
    seen=tracked_predictions(monkeypatch,m)
    result=m.compute_cell(cell,'F1',cache,out,deadline_monotonic=time.monotonic()-1)
    assert not seen
    assert all(r['status']!='COMPLETE' and 'RESOURCE' in r['reason'] for r in result['rows'])


def test_worker_checks_code_before_loading_source_and_orders_f2_arms(tmp_path,monkeypatch):
    m=api();cell,cache,out=fixture(tmp_path,'F2');long=dict(cell,cell_id='F2-TOY-V7',validation_first=127,validation_n=7)
    spec=dict(experiment='F2',cells=[long,cell],cache_root=str(cache),output_root=str(out),
        cap_seconds=60,cell_cap_seconds=30,expected_code_sha256={'v12_runner.py':'0'*64})
    path=tmp_path/'job.json';path.write_text(json.dumps(spec))
    real=m.load_series
    def forbidden(*args,**kwargs): raise AssertionError('code gate must precede source loading')
    monkeypatch.setattr(m,'load_series',forbidden)
    with pytest.raises(ValueError,match='CODE_HASH'): m.worker_job(path)
    loads=[]
    def observed_load(*args,**kwargs):
        if loads:
            completed=json.loads((out/cell['cell_id']/'cell-result.json').read_text())
            assert completed['status']=='COMPLETE'
            assert (out/cell['cell_id']/'references.json').is_file()
        loads.append(1)
        return real(*args,**kwargs)
    monkeypatch.setattr(m,'load_series',observed_load)
    spec['expected_code_sha256']={'v12_runner.py':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}
    path.write_text(json.dumps(spec));result=m.worker_job(path)
    assert [r['cell']['validation_n'] for r in result['cells']]==[4,7]
    assert len(result['rows'])==4 and result['experiment']=='F2'
    assert all(r['status']=='COMPLETE' for r in result['rows'])


@pytest.mark.parametrize('selected', ['QR33','QR4'])
def test_f2_declared_single_method_never_calls_or_returns_the_other(tmp_path,monkeypatch,selected):
    m=api();cell,cache,out=fixture(tmp_path,'F2');cell['methods']=[selected]
    seen=tracked_predictions(monkeypatch,m)
    result=m.compute_cell(cell,'F2',cache,out)
    other='QR4' if selected=='QR33' else 'QR33'
    assert all(method!=other for _,method,_ in seen)
    assert [row['method'] for row in result['rows']]==[selected]
    assert len(result['candidates'])==7
    assert all(row['method']==selected for row in result['candidates'])
    assert len([r for r in result['candidates'] if r['segment']=='validation'])==6
    assert (out/cell['cell_id']/f'{selected}.selection.json').is_file()
    assert not (out/cell['cell_id']/f'{other}.selection.json').exists()


@pytest.mark.parametrize('experiment,methods', [
    ('F2',[]),('F2',['QR33','QR33']),('F2',['QR99']),('F2','QR33'),
    ('F1',['QR33']),('F1',['QR4']),('F3',['QR4']),('F3',['QR33','QR4']),
])
def test_method_subset_rejects_empty_duplicate_unknown_or_wrong_experiment(tmp_path,monkeypatch,experiment,methods):
    m=api();cell,cache,out=fixture(tmp_path,experiment);cell['methods']=methods
    def forbidden(*args,**kwargs): raise AssertionError('invalid method subset reached source loading')
    monkeypatch.setattr(m,'load_series',forbidden)
    with pytest.raises(ValueError,match='METHOD_SUBSET'):
        m.compute_cell(cell,experiment,cache,out)


def test_f2_subset_reuses_existing_same_method_selection_without_changing_seal(tmp_path,monkeypatch):
    m=api();cell,cache,out=fixture(tmp_path,'F2')
    m.compute_cell(cell,'F2',cache,out)
    seal=out/cell['cell_id']/'QR33.selection.json';before=seal.read_bytes()
    seen=tracked_predictions(monkeypatch,m)
    cell['methods']=['QR33']
    # A different scope uses a separate output_root. The existing per-method
    # selection/result may be verified, but the full cell receipt is immutable.
    with pytest.raises(ValueError,match='IMMUTABLE_RESULT_CHANGED:cell-result.json'):
        m.compute_cell(cell,'F2',cache,out)
    assert not seen
    assert seal.read_bytes()==before


@pytest.mark.parametrize('experiment', ['F2','F3'])
def test_nonfinite_relative_loss_ratio_cannot_be_marked_complete(tmp_path,monkeypatch,experiment):
    m=api();cell,cache,out=fixture(tmp_path,experiment)
    def constructed(context,source,ids,method,penalty,tau,cache_root,guard):
        mean=1e-320 if method=='F' else 1e100
        return dict(status='COMPLETE',reason=None,cache_key=f'{method}-{penalty}-{ids[0]}',
            summary=dict(mean_loss=mean,n=len(ids),strict_breach_count=0,strict_breach_rate=0.))
    monkeypatch.setattr(m,'_attempt',constructed)
    result=m.compute_cell(cell,experiment,cache,out)
    assert all(r['status']=='FAILED' and r['reason']=='NONFINITE_RELATIVE_LOSS'
               and r['actual_excess_pct'] is None for r in result['rows'])
