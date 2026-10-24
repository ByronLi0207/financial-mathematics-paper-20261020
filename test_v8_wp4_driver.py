"""Constructed WP4 driver boundaries; no accepted FX read or study fit."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import time

import pytest


def driver():return importlib.import_module('run_v8_wp4')


def design():
    return json.loads((Path(__file__).parent/'protocol/revision-v8/wp4-daily-fx-design.json').read_text())


def test_parent_import_keeps_numerical_modules_unloaded():
    r=subprocess.run([sys.executable,'-c',"import run_v8_wp4,sys; assert not any(x in sys.modules for x in ('numpy','study_data','v8_daily_fx','v8_mechanism_mc'))"],capture_output=True,text=True)
    assert r.returncode==0,r.stderr


def test_four_cells_have_twelve_methods_and_thirty_two_candidate_slots(tmp_path):
    d=driver();dd=design()
    assert [(r['window'],r['horizon']) for r in d.planned_cells(dd)]==[(52,6),(52,24),(260,6),(260,24)]
    rows=d.build_inventory(dd,tmp_path)
    assert len(rows)==12
    assert sum(len(r['candidates']) for r in rows)==32
    assert {r['status'] for r in rows}=={'NOT_ATTEMPTED'}
    assert all(r['evaluation'] is None for r in rows)
    assert all(c['status']=='NOT_ATTEMPTED' for r in rows for c in r['candidates'])


def test_sample_na_keeps_all_methods_and_declared_candidates(tmp_path):
    d=driver();dd=design();cell=list(d.planned_cells(dd))[0]
    public=tmp_path/'cells'/cell['cell_id'];public.mkdir(parents=True)
    geometry={'status':'NA_SAMPLE_SIZE','reason':'EMPTY_EVALUATION_GRID','evaluation_count':0,
        'validation_first':329,'validation_last':380,'evaluation_first':405,'evaluation_last':400}
    d.save_sample_na(dd,public,cell,geometry)
    rows=d.build_inventory(dd,tmp_path)
    assert [r['status'] for r in rows[:3]]==['NA_SAMPLE_SIZE']*3
    assert all(r['reason']=='EMPTY_EVALUATION_GRID' for r in rows[:3])
    assert [len(r['candidates']) for r in rows[:3]]==[0,3,5]
    assert all(c['status']=='NOT_ATTEMPTED' for r in rows[:3] for c in r['candidates'])
    with pytest.raises(FileExistsError):d.save_sample_na(dd,public,cell,geometry)


def test_source_and_daily_fingerprints_must_match_across_workers():
    d=driver()
    one={'source_identity':{'accepted_csv_sha256':'same','accepted_csv_bytes':5,'source_verified':True,'local_validation_utc':'earlier'},
         'daily_metadata':{'n_daily':4,'fingerprints':{'combined_sha256':'daily-a'}}}
    two=json.loads(json.dumps(one));two['source_identity']['local_validation_utc']='later'
    assert d.check_consistency([one,two])==d.consistency_identity(one)
    two['daily_metadata']['fingerprints']['combined_sha256']='daily-b'
    with pytest.raises(d.DriverStop,match='SOURCE_AGGREGATION_MISMATCH'):d.check_consistency([one,two])


def test_private_trace_is_exclusive_and_public_receipt_has_only_fingerprint(tmp_path):
    import numpy as np
    d=driver();private=tmp_path/'private';private.mkdir();public=tmp_path/'public';public.mkdir()
    arrays={'origins':np.array([405,406]),'refit_indices':np.array([405,405]),
        'capacity':np.array([4.,5.]),'peak':np.array([3.,6.]),'floor':np.array([2.,3.])}
    receipt=d.save_trace(private,public,'fixture-evaluation',arrays)
    assert receipt=={'trace_sha256':d.sha_file(private/'fixture-evaluation.npz'),'trace_origin_count':2}
    assert 'private' not in json.dumps(receipt)
    with np.load(private/'fixture-evaluation.npz') as saved:
        assert saved['origins'].tolist()==[405,406]
        assert saved['peak'].tolist()==[3.,6.]
    with pytest.raises(FileExistsError):d.save_trace(private,public,'fixture-evaluation',arrays)


def test_parent_deadline_interrupts_only_owned_inflight_process():
    d=driver();child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'],start_new_session=True)
    before=time.monotonic();receipt=d.wait_owned_worker(child,before+.1,hard_seconds=10)
    assert receipt['reason']=='GLOBAL_DEADLINE'
    assert child.poll() is not None
    assert time.monotonic()-before<3


def test_trace_fingerprint_is_reconciled_into_candidate_inventory(tmp_path):
    d=driver();dd=design();public=tmp_path/'cells'/'W52_H6';public.mkdir(parents=True)
    d.exclusive_json(d.method_path(public,52,6,'QR4',started=True),{'status':'STARTED'})
    d.exclusive_json(d.candidate_path(public,52,6,'QR4',0),{'status':'COMPLETE','penalty':.001,'mean_loss':2.,'origin_count':52})
    d.exclusive_json(public/'W52_H6_QR4_validation-0.trace.json',{'trace_sha256':'a'*64,'trace_origin_count':52})
    d.exclusive_json(d.selection_path(public,52,6,'QR4'),{'status':'SELECTED','penalty':.001})
    row=d.build_inventory(dd,tmp_path)[2]
    assert row['status']=='FAILED' and row['reason']=='INTERRUPTED_METHOD'
    assert row['selected_penalty']==.001
    assert row['candidates'][0]['trace_sha256']=='a'*64
    assert row['candidates'][1]['status']=='NOT_ATTEMPTED'


def test_ineligible_selection_survives_hard_kill_before_final_method_receipt(tmp_path):
    d=driver();dd=design();public=tmp_path/'cells'/'W52_H6';public.mkdir(parents=True)
    d.exclusive_json(d.method_path(public,52,6,'QR33',started=True),{'status':'STARTED'})
    for index,penalty in enumerate(dd['menus']['QR33']):
        d.exclusive_json(d.candidate_path(public,52,6,'QR33',index),
            {'status':'FAILED','penalty':penalty,'reason':'NONCONVERGENCE','origin_count':0,'mean_loss':None})
    d.exclusive_json(d.selection_path(public,52,6,'QR33'),{'status':'INELIGIBLE','penalty':None})
    rows=d.build_inventory(dd,tmp_path);row=rows[1]
    assert len(rows)==12
    assert row['status']=='FAILED' and row['reason']=='VALIDATION_INELIGIBLE'
    assert row['selected_penalty'] is None
    assert row['validation_selection']=={'status':'INELIGIBLE','penalty':None}
    assert [c['reason'] for c in row['candidates']]==['NONCONVERGENCE']*3


@pytest.mark.parametrize('selection',[
    {'status':'SELECTED','penalty':None},
    {'status':'SELECTED','penalty':123.},
    {'status':'INELIGIBLE','penalty':.001},
])
def test_invalid_selected_or_ineligible_penalty_is_rejected(tmp_path,selection):
    d=driver();public=tmp_path/'cells'/'W52_H6';public.mkdir(parents=True)
    d.exclusive_json(d.method_path(public,52,6,'QR33',started=True),{'status':'STARTED'})
    d.exclusive_json(d.selection_path(public,52,6,'QR33'),selection)
    with pytest.raises(d.DriverStop,match='INVALID_SELECTION_RECEIPT'):
        d.build_inventory(design(),tmp_path)


def _reports():
    rows=[]
    for w in (52,260):
        for h in (6,24):
            for m in ('F','QR33','QR4'):
                rows.append({'window':w,'horizon':h,'method':m,'status':'COMPLETE','reason':None,
                    'selected_penalty':None if m=='F' else .1,'candidates':[],
                    'evaluation':{'mean_loss':2. if m=='F' else 1.,'n':40,'strict_breach_count':2,'strict_breach_rate':.05}})
    return rows


def test_eight_contrasts_keep_full_precision_matched_counts_and_na_reference():
    d=driver();rows=_reports()
    contrasts=d.make_contrasts(rows,design())
    assert len(contrasts)==8
    assert {r['relative_loss_percent'] for r in contrasts}=={-50.}
    assert all(r['status']=='COMPLETE' and r['n']==40 for r in contrasts)
    rows[0].update(status='FAILED',reason='INTERRUPTED_METHOD',evaluation=None)
    bad=d.make_contrasts(rows,design())
    assert bad[0]['relative_loss_percent'] is None and bad[1]['relative_loss_percent'] is None
    assert bad[0]['reason']=='REFERENCE_INTERRUPTED_METHOD'
    assert sum(r['status']=='COMPLETE' for r in bad)==6


def test_zero_reference_loss_is_undefined_without_inventing_a_relative_change():
    d=driver();rows=_reports();rows[0]['evaluation']['mean_loss']=0.
    first=d.make_contrasts(rows,design())[0]
    assert first['status']=='COMPLETE' and first['relative_loss_percent'] is None
    assert first['relative_loss_undefined_reason']=='ZERO_REFERENCE_LOSS'


def test_summary_refuses_before_termination_without_creating_output(tmp_path):
    d=driver();d.exclusive_json(tmp_path/'manifest.json',{'formal_directory':str(tmp_path)})
    with pytest.raises(FileNotFoundError):d.summarize(tmp_path/'manifest.json')
    assert not (tmp_path/'summary.json').exists()


def test_existing_output_is_not_reused_and_source_code_mutation_is_detected(tmp_path):
    d=driver();formal=tmp_path/'formal';formal.mkdir()
    with pytest.raises(FileExistsError):d.create_run_directories(formal,tmp_path/'private')
    assert not (tmp_path/'private').exists()
    source=tmp_path/'sealed.py';source.write_text('old')
    seal={'code_hashes':{'sealed.py':d.sha_file(source)},'protocol_hashes':{}}
    source.write_text('new')
    with pytest.raises(d.DriverStop,match='SEALED_HASH_MISMATCH'):d.verify_seal(seal,tmp_path)


def test_transient_cell_end_resource_failure_cannot_leave_na_worker_success(tmp_path,monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    import study_data
    import run_study as original_runner
    d=driver();dd=design();formal=tmp_path/'formal';private=tmp_path/'private'
    public=formal/'cells'/'W52_H6';public.mkdir(parents=True)
    (private/'W52_H6').mkdir(parents=True)
    manifest={'design':dd,'formal_directory':str(formal),'private_directory':str(private),
        'global_deadline_monotonic':time.monotonic()+60,'code_hashes':{},'protocol_hashes':{}}
    d.exclusive_json(tmp_path/'manifest.json',manifest)
    # Only the source loader is replaced: it returns one constructed observation,
    # which must take NA geometry before features or any fit can be called.
    source=study_data.SourceData(times=np.array(['2020-01-01T12:00'],dtype='datetime64[us]'),
        position=np.array([1.]),identity={'source_verified':True})
    monkeypatch.setattr(study_data,'load_source',lambda *a,**kw:source)
    monkeypatch.setattr(original_runner,'arm_hard_deadline',lambda *a:None)
    for name in d.sealed.THREAD_NAMES:monkeypatch.setenv(name,'1')
    class Checkpoint:
        def __init__(self,*a):pass
        def __call__(self,**kw):
            if kw.get('stage')=='cell_end':raise d.DriverStop('RESOURCE_THREADS')
    monkeypatch.setattr(d,'ResourceCheckpoint',Checkpoint)
    args=SimpleNamespace(manifest=tmp_path/'manifest.json',window=52,horizon=6,
        global_deadline=manifest['global_deadline_monotonic'])
    assert d.run_worker(args)==1
    receipt=json.loads((public/'worker-receipt.json').read_text())
    assert receipt['status']=='FAILED' and receipt['reason']=='RESOURCE_THREADS'


def test_parent_seals_manifest_before_dispatch_and_stops_unknown_failure(tmp_path,monkeypatch):
    d=driver();dd=design();formal=tmp_path/'formal';private=tmp_path/'private'
    monkeypatch.setattr(d,'FORMAL',formal);monkeypatch.setattr(d,'PRIVATE',private)
    monkeypatch.setattr(d,'verify_design',lambda:(dd,'fixture-commit',{},{}))
    monkeypatch.setattr(d.sealed,'software_environment',lambda:{'fixture':True})
    dispatched=[]
    class FailedChild:
        returncode=2
        def __init__(self,cmd,**kw):
            manifest=json.loads((formal/'manifest.json').read_text())
            assert manifest['no_source_parse_before_manifest'] is True
            assert len(manifest['code_hashes'])==13
            dispatched.append(cmd)
        def poll(self):return self.returncode
        def wait(self,**kw):return self.returncode
    monkeypatch.setattr(d.subprocess,'Popen',FailedChild)
    assert d.run_study()==1
    assert len(dispatched)==1
    termination=json.loads((formal/'study-termination.json').read_text())
    assert termination['status']=='TECHNICAL_ERROR'
    assert termination['all_workers_terminated'] is True
    assert len(json.loads((formal/'inventory.json').read_text()))==12


def test_summary_writes_twelve_rows_eight_contrasts_and_separate_classifications(tmp_path):
    d=driver();dd=design();rows=_reports()
    rows[-1].update(status='FAILED',reason='NONCONVERGENCE',evaluation=None)
    d.exclusive_json(tmp_path/'manifest.json',{'formal_directory':str(tmp_path),'design':dd,
        'design_id':'constructed-only','code_hashes':{},'protocol_hashes':{}})
    d.exclusive_json(tmp_path/'study-termination.json',{'status':'COMPLETE','all_workers_terminated':True})
    d.exclusive_json(tmp_path/'inventory.json',rows)
    assert d.summarize(tmp_path/'manifest.json')==0
    result=json.loads((tmp_path/'summary.json').read_text())
    assert len(result['cells'])==12 and len(result['contrasts'])==8
    assert result['classifications']['QR33']['status']=='CONDITIONAL_GAINS_PERSIST'
    assert result['classifications']['QR4']['status']=='INCONCLUSIVE'
    assert result['new_statistical_tests'] is False
    assert (tmp_path/'summary.csv').exists() and (tmp_path/'contrasts.csv').exists()
