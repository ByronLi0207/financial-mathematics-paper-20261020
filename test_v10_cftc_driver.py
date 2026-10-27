"""Artificial acquisition and full-method persistence fixtures, no real source I/O."""
from copy import deepcopy
from datetime import date,timedelta
import hashlib,importlib,importlib.util,json
import numpy as np
import pytest


def api():
    assert importlib.util.find_spec('run_v10_cftc') is not None,'CFTC driver missing'
    return importlib.import_module('run_v10_cftc')


def acquisition(tmp_path):
    p=tmp_path/'data/cftc-tff/raw/artificial.zip';p.parent.mkdir(parents=True);p.write_bytes(b'PK-artificial-only')
    design={'downloads_in_fixed_order':[{'url':'https://www.cftc.gov/files/artificial.zip'}]}
    prov=dict(status='ALL_REQUIRED_FILES_DOWNLOADED',design_commit_time='2026-01-01T00:00:00+00:00',download_attempts=1,failed_attempts=0,files=[dict(url=design['downloads_in_fixed_order'][0]['url'],started_utc='2026-01-01T00:00:01Z',status='DOWNLOADED',local_path=str(p.relative_to(tmp_path)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())])
    return design,prov,p


def test_official_byte_identity_and_request_after_design_are_required(tmp_path):
    d,p,path=acquisition(tmp_path)
    assert api().verify_acquisition(p,d,tmp_path)==[path]


@pytest.mark.parametrize('change',[{'url':'https://example.org/artificial.zip'},{'started_utc':'2025-12-31T23:59:59Z'},{'status':'FAILED'},{'bytes':1},{'sha256':'0'*64}])
def test_changed_or_premature_acquisition_rejected(tmp_path,change):
    d,p,path=acquisition(tmp_path);p['files'][0].update(change)
    with pytest.raises(ValueError):api().verify_acquisition(p,d,tmp_path)


def test_calendar_split_names_actual_measurement_and_model_clock_separately():
    first=date(2010,1,4);cal=[(first+timedelta(weeks=i)).isoformat() for i in range(800)];actual=[(date.fromisoformat(x)+timedelta(days=1)).isoformat() for x in cal]
    d=dict(horizon=6,windows=[52,260],feature_rms_long=26)
    s=api().split_receipt(cal,actual,d)
    assert s['indices']['evaluation_first']==534 and s['indices']['evaluation_last']==793
    assert s['indices']['validation_first']==476 and s['indices']['validation_last']==527
    assert s['model_clock']['evaluation']['first']==cal[534]
    assert s['actual_dates']['evaluation']['first']==actual[534]
    assert s['indices']['validation_last']+6<s['indices']['evaluation_first']
    assert s['actual_dates']['evaluation']['last_label_end']==actual[799]


def fake_method(directory,method='F',count=4):
    from conditional_study import score_predictions
    from study_core import stable_mean
    directory.mkdir(parents=True,exist_ok=True);ids=np.arange(40,40+count);peak=np.full(count,3.);capacity=np.full(count,4.);floor=np.ones(count)
    score=score_predictions(peak,capacity,floor,ids)
    trace=directory/f'trace-{method}.npz'
    with trace.open('xb') as f:np.savez_compressed(f,origins=ids,capacities=capacity,peak=peak,floor=floor,pinball=score.pinball,strict_breach=score.strict_breach,overrun=score.overrun,unused=score.unused)
    row=dict(method=method,status='COMPLETE',mean_loss=stable_mean(score.pinball),strict_breach_count=0,n=count,selected_penalty=None,selected_gamma=None,reason=None,trace_path=trace.name,trace_bytes=trace.stat().st_size,trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest())
    (directory/f'result-{method}.json').write_text(json.dumps(row));return row,trace


def test_completed_method_survives_missing_later_methods_with_full_trace(tmp_path):
    row,trace=fake_method(tmp_path)
    got=api().recover_method_rows(tmp_path,'000001',52,{'methods':['F','I','QR33']},np.arange(40,44))
    assert len(got)==3 and got[0]['status']=='COMPLETE' and got[0]['code']=='000001'
    assert got[0]['mean_loss']==row['mean_loss']
    assert [x['status'] for x in got[1:]]==['FAILED','FAILED']
    assert all(x.get('mean_loss') is None for x in got[1:])


def test_complete_scalar_without_trace_is_not_a_complete_method(tmp_path):
    row,trace=fake_method(tmp_path);row['trace_path']='missing.npz';(tmp_path/'result-F.json').write_text(json.dumps(row))
    got=api().recover_method_rows(tmp_path,'000001',52,{'methods':['F']},np.arange(40,44))[0]
    assert got['status']=='FAILED' and got['mean_loss'] is None


def test_partial_origin_prefix_is_never_scored_as_complete(tmp_path):
    fake_method(tmp_path,count=3)
    got=api().recover_method_rows(tmp_path,'000001',52,{'methods':['F']},np.arange(40,44))[0]
    assert got['status']=='FAILED' and got['mean_loss'] is None


def test_prepared_source_bytes_are_verified_before_and_after_use(tmp_path):
    path=tmp_path/'source.npz';path.write_bytes(b'artificial-source-only')
    sources=[dict(path=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())]
    assert api().verify_sources(sources,tmp_path) is True
    path.write_bytes(b'changed-source-after-loading')
    with pytest.raises(ValueError):api().verify_sources(sources,tmp_path)
