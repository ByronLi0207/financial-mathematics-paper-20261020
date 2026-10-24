"""Constructed boundaries for frozen WP5 driver; no actual source or study."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import time

import pytest


def driver():return importlib.import_module('run_v8_wp5')

def design():return json.loads((Path(__file__).parent/'protocol/revision-v8/wp5-fixed-prefix-design.json').read_text())


def test_parent_import_does_not_load_source_or_numerical_code():
    r=subprocess.run([sys.executable,'-c',"import run_v8_wp5,sys; assert not any(s in sys.modules for s in ('numpy','study_data','v8_backcast','v8_mechanism_mc'))"],capture_output=True,text=True)
    assert r.returncode==0,r.stderr


def test_fixed_inventory_has_eight_slots_and_no_candidates(tmp_path):
    d=driver();dd=design();units=list(d.planned_units(dd))
    assert [(u['horizon'],u['method']) for u in units]==[(h,m) for h in (6,24) for m in ('F_matched','F_rolling720','QR33','QR4')]
    assert [u['penalty'] for u in units]==[None,None,.01,.01,None,None,.001,.01]
    rows=d.build_inventory(dd,tmp_path)
    assert len(rows)==8 and {r['status'] for r in rows}=={'NOT_ATTEMPTED'}
    assert all(r['evaluation'] is None for r in rows)
    assert all('candidates' not in r for r in rows)


def test_interruption_does_not_score_partial_or_change_parameter(tmp_path):
    d=driver();dd=design();public=tmp_path/'units'/'H6_QR33';public.mkdir(parents=True)
    d.exclusive_json(public/'report.started.json',{'status':'STARTED'})
    row=d.build_inventory(dd,tmp_path)[2]
    assert row['status']=='FAILED' and row['reason']=='INTERRUPTED_METHOD'
    assert row['selected_penalty']==.01 and row['evaluation'] is None


def test_partial_complete_receipt_is_rejected_without_dropping_slot(tmp_path):
    d=driver();public=tmp_path/'units'/'H6_QR33';public.mkdir(parents=True)
    d.exclusive_json(public/'report.json',{'status':'COMPLETE','evaluation':{'n':10,'mean_loss':2.,'strict_breach_count':1,'strict_breach_rate':.1}})
    rows=d.build_inventory(design(),tmp_path)
    assert len(rows)==8
    assert rows[2]['status']=='FAILED' and rows[2]['reason']=='INVALID_METHOD_RECEIPT'
    assert rows[2]['evaluation'] is None


def test_whole_method_failure_keeps_diagnostics_and_no_evaluation(tmp_path):
    d=driver();public=tmp_path/'units'/'H24_QR33';public.mkdir(parents=True)
    d.exclusive_json(public/'report.json',{'status':'FAILED','reason':'NONCONVERGENCE','evaluation':None,'selected_penalty':.001,'failure_diagnostics':{'iterations':10000},'failure_progress':{'issue':4000}})
    row=d.build_inventory(design(),tmp_path)[6]
    assert row['selected_penalty']==.001 and row['evaluation'] is None
    assert row['failure_diagnostics']=={'iterations':10000} and row['failure_progress']=={'issue':4000}


def test_receipt_cannot_change_frozen_penalty(tmp_path):
    d=driver();public=tmp_path/'units'/'H6_QR33';public.mkdir(parents=True)
    d.exclusive_json(public/'report.json',{'status':'FAILED','reason':'NONCONVERGENCE','evaluation':None,'selected_penalty':.1})
    row=d.build_inventory(design(),tmp_path)[2]
    assert row['reason']=='INVALID_METHOD_RECEIPT' and row['selected_penalty']==.01


def test_existing_output_is_not_reused(tmp_path):
    d=driver();formal=tmp_path/'formal';formal.mkdir()
    with pytest.raises(FileExistsError):d.create_run_directories(formal,tmp_path/'private')
    assert not (tmp_path/'private').exists()


def test_sealed_source_mutation_detected(tmp_path):
    d=driver();path=tmp_path/'source.py';path.write_text('old')
    manifest={'code_hashes':{'source.py':d.sha_file(path)},'protocol_hashes':{}}
    path.write_text('new')
    with pytest.raises(d.DriverStop,match='SEALED_HASH_MISMATCH'):d.verify_seal(manifest,tmp_path)


def test_trace_only_public_fingerprint_and_exclusive(tmp_path):
    import numpy as np
    d=driver();private=tmp_path/'private';private.mkdir();public=tmp_path/'public';public.mkdir()
    arrays={'origins':np.array([1,2]),'capacity':np.array([4.,5.]),'peak':np.array([5.,4.])}
    receipt=d.save_trace(private,public,arrays)
    assert receipt=={'trace_sha256':d.sha_file(private/'evaluation.npz'),'trace_origin_count':2}
    assert set(json.loads((public/'trace.json').read_text()))=={'trace_sha256','trace_origin_count'}
    with pytest.raises(FileExistsError):d.save_trace(private,public,arrays)


def test_owned_child_global_deadline_terminates_and_reports():
    d=driver();child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(20)'],start_new_session=True)
    before=time.monotonic();receipt=d.wait_owned_worker(child,before+.1,hard_seconds=10)
    assert child.poll() is not None and receipt['reason']=='GLOBAL_DEADLINE'
    assert time.monotonic()-before<3


def test_source_identity_consistency_ignores_read_time_not_hash():
    d=driver();one={'source_identity':{'accepted_csv_sha256':'a'*64,'accepted_csv_bytes':5,'source_verified':True,'local_validation_utc':'one'},'source_metadata':{'n':8,'origin_first':1}}
    two=json.loads(json.dumps(one));two['source_identity']['local_validation_utc']='two'
    assert d.check_consistency([one,two])==d.consistency_identity(one)
    two['source_identity']['accepted_csv_sha256']='b'*64
    with pytest.raises(d.DriverStop,match='SOURCE_CONSISTENCY_MISMATCH'):d.check_consistency([one,two])


def test_parameters_are_verified_from_exact_original_files(tmp_path):
    d=driver();dd=design();freeze={'cells':[{'source':'fx_hourly','horizon':h,'window':2880,'family':'QR','status':'SELECTED','parameter':p} for h,p in ((6,.01),(24,.001))]}
    files={'protocol/revision-20261022/selection-freeze.json':freeze}
    for h in (6,24):files[f'results/revision-20261023/parsimonious/fx_hourly-h{h}-w2880.json']={'source':'fx_hourly','horizon':h,'window':2880,'selected_penalty':.01}
    for name,value in files.items():
        path=tmp_path/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
        dd['forecasting']['parameter_source_sha256'][name]=d.sha_file(path)
    assert len(d.verify_parameters(dd,tmp_path))==3
    files['protocol/revision-20261022/selection-freeze.json']['cells'][0]['parameter']=.1
    path=tmp_path/'protocol/revision-20261022/selection-freeze.json';path.write_text(json.dumps(freeze))
    dd['forecasting']['parameter_source_sha256'][str(path.relative_to(tmp_path))]=d.sha_file(path)
    with pytest.raises(d.DriverStop,match='PARAMETER_VALUE_MISMATCH'):d.verify_parameters(dd,tmp_path)


def test_summary_refuses_before_termination(tmp_path):
    d=driver();d.exclusive_json(tmp_path/'manifest.json',{'formal_directory':str(tmp_path)})
    with pytest.raises(FileNotFoundError):d.summarize(tmp_path/'manifest.json')
    assert not (tmp_path/'summary.json').exists()


def test_failure_contrasts_keep_all_eight_and_no_private_trace_read(tmp_path):
    d=driver();dd=design();rows=d.build_inventory(dd,tmp_path)
    manifest={'design':dd,'private_directory':str(tmp_path/'private')}
    contrasts=d.make_contrasts(rows,manifest)
    assert len(contrasts)==8 and all(r['status']=='FAILED' for r in contrasts)
    assert all(r['dm'] is None and r['mean_model_loss'] is None for r in contrasts)


def test_complete_trace_requires_matching_public_hash(tmp_path):
    import numpy as np
    d=driver();private=tmp_path/'private';unit=private/'H6_QR33';unit.mkdir(parents=True)
    with open(unit/'evaluation.npz','wb') as f:np.savez(f,origins=np.array([1,2]),pinball=np.array([1.,2.]),strict_breach=np.array([0,1]))
    row={'unit_id':'H6_QR33','status':'COMPLETE','evaluation':{'trace_sha256':'wrong','trace_origin_count':2,'n':2}}
    with pytest.raises(d.DriverStop,match='PRIVATE_TRACE_HASH_MISMATCH'):d.load_trace(row,private)


def _worker_fixture(tmp_path,monkeypatch,method='QR33'):
    import numpy as np
    from types import SimpleNamespace
    import study_data
    import run_study
    import v8_backcast
    d=driver();dd=design();dd['sample'].update(evaluation_first=200,evaluation_last=239,evaluation_count=40)
    formal=tmp_path/'formal';private=tmp_path/'private';uid='H6_'+method
    public=formal/'units'/uid;public.mkdir(parents=True);(private/uid).mkdir(parents=True)
    manifest={'design':dd,'design_id':'synthetic-only','formal_directory':str(formal),'private_directory':str(private),
        'source_spec':{},'global_deadline_monotonic':time.monotonic()+60,'code_hashes':{},'protocol_hashes':{}}
    path=tmp_path/'manifest.json';d.exclusive_json(path,manifest)
    source=study_data.SourceData(times=np.datetime64('2020-01-01T00:00','us')+np.arange(300)*np.timedelta64(1,'h'),
        position=1.+np.arange(300,dtype=float),identity={'accepted_csv_sha256':'a'*64,'accepted_csv_bytes':5,'source_verified':True})
    monkeypatch.setattr(study_data,'load_source',lambda *a,**kw:source)
    monkeypatch.setattr(run_study,'arm_hard_deadline',lambda *a:None)
    monkeypatch.setattr(v8_backcast,'backcast_geometry',lambda *a:{'status':'READY','evaluation_count':40})
    for name in d.sealed.THREAD_NAMES:monkeypatch.setenv(name,'1')
    class Checkpoint:
        def __init__(self,*a):pass
        def __call__(self,**kw):pass
    monkeypatch.setattr(d,'ResourceCheckpoint',Checkpoint)
    args=SimpleNamespace(manifest=path,horizon=6,method=method,global_deadline=manifest['global_deadline_monotonic'])
    return d,args,public,private/uid


def test_worker_nonconvergence_does_not_score_partial_or_try_another_penalty(tmp_path,monkeypatch):
    from conditional_quantile import QuantileFitError
    import v8_mechanism_mc
    d,args,public,private=_worker_fixture(tmp_path,monkeypatch)
    attempts=[]
    def failed(*a,**kw):
        attempts.append((a[8],a[9]));kw['checkpoint'](stage='fit',method='QR33',iteration=10000)
        raise QuantileFitError('NONCONVERGENCE',{'iterations':10000})
    monkeypatch.setattr(v8_mechanism_mc,'forecast_report',failed)
    assert d.run_worker(args)==1
    row=json.loads((public/'report.json').read_text())
    assert attempts==[('QR33',.01)]
    assert row['status']=='FAILED' and row['reason']=='NONCONVERGENCE' and row['evaluation'] is None
    assert row['failure_diagnostics']['iterations']==10000
    assert not (private/'evaluation.npz').exists()


def test_worker_completed_trace_uses_full_declared_grid_and_mature_records(tmp_path,monkeypatch):
    import numpy as np
    import v8_mechanism_mc
    d,args,public,private=_worker_fixture(tmp_path,monkeypatch)
    def completed(position,times,features,cache,origins,h,w,step,method,penalty,checkpoint):
        assert method=='QR33' and penalty==.01 and w==2880 and step==24
        return {'origins':origins,'capacity':np.abs(position[origins])+1.,'refit_indices':np.repeat(origins[0],len(origins)),
            'fit_diagnostics':[{'refit_index':200,'training_first_origin':0,'training_last_origin':194,'training_count':195,'latest_label_end':200}]}
    monkeypatch.setattr(v8_mechanism_mc,'forecast_report',completed)
    assert d.run_worker(args)==0
    row=json.loads((public/'report.json').read_text())
    assert row['status']=='COMPLETE' and row['evaluation']['n']==40
    assert row['maturity']['maximum_label_end_minus_refit']==0
    with np.load(private/'evaluation.npz',allow_pickle=False) as trace:
        assert trace['origins'].tolist()==list(range(200,240))
        assert set(trace.files)=={'origins','refit_indices','capacity','peak','floor','pinball','strict_breach'}
    assert row['evaluation']['trace_sha256']==d.sha_file(private/'evaluation.npz')


def test_finalization_resource_failure_invalidates_prepared_complete_score(tmp_path,monkeypatch):
    import numpy as np
    import v8_mechanism_mc
    d,args,public,private=_worker_fixture(tmp_path,monkeypatch)
    def completed(position,times,features,cache,origins,h,w,step,method,penalty,checkpoint):
        return {'origins':origins,'capacity':np.abs(position[origins])+1.,'refit_indices':origins,
            'fit_diagnostics':[{'refit_index':200,'training_first_origin':0,'training_last_origin':194,'training_count':195,'latest_label_end':200}]}
    monkeypatch.setattr(v8_mechanism_mc,'forecast_report',completed)
    class Checkpoint:
        def __init__(self,*a):pass
        def __call__(self,**kw):
            if kw.get('stage')=='finalization':raise d.DriverStop('RESOURCE_THREADS')
    monkeypatch.setattr(d,'ResourceCheckpoint',Checkpoint)
    assert d.run_worker(args)==1
    row=json.loads((public/'report.json').read_text())
    assert row['status']=='FAILED' and row['evaluation'] is None and row['reason']=='RESOURCE_THREADS'
    assert (private/'evaluation.npz').exists()  # retained, never falsely scored


def test_parent_manifest_sealed_before_dispatch_and_unknown_exit_stops(tmp_path,monkeypatch):
    d=driver();dd=design();formal=tmp_path/'formal';private=tmp_path/'private'
    monkeypatch.setattr(d,'FORMAL',formal);monkeypatch.setattr(d,'PRIVATE',private)
    monkeypatch.setattr(d,'verify_design',lambda:(dd,'fixture-only',{},{}))
    monkeypatch.setattr(d.sealed,'software_environment',lambda:{'fixture':True})
    attempted=[]
    class FailedChild:
        returncode=2
        def __init__(self,cmd,**kwargs):
            manifest=json.loads((formal/'manifest.json').read_text())
            assert manifest['no_source_parse_before_manifest'] and manifest['planned_workers']==8
            assert manifest['planned_validation_candidates']==0 and 'v8_backcast.py' in manifest['code_hashes']
            assert all(kwargs['env'][name]=='1' for name in d.sealed.THREAD_NAMES)
            attempted.append(cmd)
        def poll(self):return 2
        def wait(self,**kwargs):return 2
    monkeypatch.setattr(d.subprocess,'Popen',FailedChild)
    assert d.run_study()==1 and len(attempted)==1
    termination=json.loads((formal/'study-termination.json').read_text())
    assert termination['status']=='TECHNICAL_ERROR' and termination['all_workers_terminated']
    rows=json.loads((formal/'inventory.json').read_text())
    assert len(rows)==8 and rows[0]['status']=='FAILED'
    assert all(row['status']=='NOT_ATTEMPTED' for row in rows[1:])


def test_summary_only_eight_normal_comparisons_after_termination(tmp_path,monkeypatch):
    import numpy as np
    d=driver();dd=design();private=tmp_path/'private';private.mkdir();formal=tmp_path/'formal';formal.mkdir()
    rows=[]
    for unit in d.planned_units(dd):
        p=private/unit['unit_id'];p.mkdir();public=formal/unit['unit_id'];public.mkdir()
        shift={'F_matched':3.,'F_rolling720':2.,'QR33':1.,'QR4':1.5}[unit['method']]
        arrays={'origins':np.arange(200,240),'pinball':shift+np.sin(np.arange(40)/4+shift),
            'strict_breach':np.arange(40)%7==0,'peak':np.repeat(10.,40),'floor':np.repeat(2.,40)}
        trace=d.save_trace(p,public,arrays)
        rows.append(dict(unit,status='COMPLETE',evaluation=dict(n=40,**trace)))
    manifest={'design_id':'fixture-only','design':dd,'formal_directory':str(formal),'private_directory':str(private),'code_hashes':{},'protocol_hashes':{}}
    d.exclusive_json(formal/'manifest.json',manifest);d.exclusive_json(formal/'inventory.json',rows)
    d.exclusive_json(formal/'study-termination.json',{'status':'COMPLETE','all_workers_terminated':True})
    for name in d.sealed.THREAD_NAMES:monkeypatch.setenv(name,'1')
    class Checkpoint:
        def __init__(self,*a):pass
        def __call__(self,**kw):pass
    monkeypatch.setattr(d,'ResourceCheckpoint',Checkpoint)
    assert d.summarize(formal/'manifest.json')==0
    result=json.loads((formal/'summary.json').read_text())
    assert len(result['methods'])==8 and len(result['contrasts'])==8
    assert result['normal_DM_only'] and 'previously scored' in result['independence_claim']
    assert all(r['status']=='COMPLETE' and r['dm']['status']=='OK' for r in result['contrasts'])
    assert all('hln_t' not in r['dm'] and 'hln_p' not in r['dm'] for r in result['contrasts'])
    with pytest.raises(FileExistsError):d.summarize(formal/'manifest.json')


def _complete_inventory_fixture(tmp_path):
    d=driver();dd=design();public=tmp_path/'units'/'H6_QR33';public.mkdir(parents=True)
    evaluation={'n':7368,'mean_loss':2.,'strict_breach_count':10,'strict_breach_rate':10/7368,
        'trace_sha256':'a'*64,'trace_origin_count':7368}
    d.exclusive_json(public/'report.json',{'status':'COMPLETE','reason':None,'selected_penalty':.01,
        'evaluation':evaluation,'fit_diagnostics':[],'maturity':None})
    return d,dd,public


def test_complete_report_without_final_worker_receipt_is_not_accepted(tmp_path):
    d,dd,public=_complete_inventory_fixture(tmp_path)
    d.exclusive_json(public/'parent-termination.json',{'status':'FAILED','reason':'WORKER_EXIT','returncode':-14})
    row=d.build_inventory(dd,tmp_path)[2]
    assert row['status']=='FAILED' and row['evaluation'] is None
    assert row['reason']=='WORKER_COMPLETION_UNVERIFIED'


@pytest.mark.parametrize('parent',[
    None,
    {'status':'FAILED','reason':'WORKER_HARD_TIMEOUT','returncode':-9},
    {'status':'COMPLETE','reason':None,'returncode':1},
])
def test_complete_worker_without_successful_parent_receipt_is_not_accepted(tmp_path,parent):
    d,dd,public=_complete_inventory_fixture(tmp_path)
    d.exclusive_json(public/'worker-receipt.json',{'status':'COMPLETE','code_hash_start':'PASS','code_hash_end':'PASS'})
    if parent is not None:d.exclusive_json(public/'parent-termination.json',parent)
    row=d.build_inventory(dd,tmp_path)[2]
    assert row['status']=='FAILED' and row['evaluation'] is None
    assert row['reason']=='PARENT_COMPLETION_UNVERIFIED'


@pytest.mark.parametrize('worker',[
    {'status':'COMPLETE','code_hash_start':'PASS','code_hash_end':None},
    {'status':'COMPLETE','code_hash_start':'FAIL','code_hash_end':'PASS'},
])
def test_complete_worker_without_both_seals_is_not_accepted(tmp_path,worker):
    d,dd,public=_complete_inventory_fixture(tmp_path)
    d.exclusive_json(public/'worker-receipt.json',worker)
    d.exclusive_json(public/'parent-termination.json',{'status':'COMPLETE','reason':None,'returncode':0})
    row=d.build_inventory(dd,tmp_path)[2]
    assert row['status']=='FAILED' and row['evaluation'] is None
    assert row['reason']=='WORKER_COMPLETION_UNVERIFIED'


def test_complete_report_requires_worker_seals_and_parent_zero_exit(tmp_path):
    d,dd,public=_complete_inventory_fixture(tmp_path)
    d.exclusive_json(public/'worker-receipt.json',{'status':'COMPLETE','code_hash_start':'PASS','code_hash_end':'PASS'})
    d.exclusive_json(public/'parent-termination.json',{'status':'COMPLETE','reason':None,'returncode':0})
    row=d.build_inventory(dd,tmp_path)[2]
    assert row['status']=='COMPLETE' and row['evaluation']['n']==7368
