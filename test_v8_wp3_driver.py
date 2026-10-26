"""Driver boundary fixtures: no study DGP, fitting, or frozen-study reads."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import time

import pytest


def driver():
    return importlib.import_module('run_v8_wp3')


def design():
    return json.loads((Path(__file__).parent / 'protocol/revision-v8/wp3-mechanism-design.json').read_text())


def test_parent_import_does_not_load_numerical_libraries():
    result = subprocess.run([sys.executable, '-c',
        "import run_v8_wp3,sys; assert not any(n in sys.modules for n in ('numpy','scipy','v8_mechanism_mc','conditional_study'))"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_planned_order_keeps_every_rep_phi_p_and_all_method_slots():
    d = driver(); units = list(d.planned_units(design()))
    assert len(units) == 288
    assert [(u['rep'], u['phi_index'], u['p_index']) for u in units[:4]] == [(0,0,0),(0,0,1),(0,0,2),(0,1,0)]
    assert (units[9]['rep'], units[-1]['rep']) == (1,31)
    inventory = d.build_inventory(design(), Path('/nonexistent/wp3-unit-fixture'))
    assert len(inventory) == 6912
    assert {r['status'] for r in inventory} == {'NOT_ATTEMPTED'}
    assert [(r['window'],r['horizon'],r['method']) for r in inventory[:4]] == [(52,6,'F'),(52,6,'QR33'),(52,6,'QR4'),(52,24,'F')]
    assert all(r['evaluation'] is None for r in inventory)


def test_exclusive_outputs_reject_duplicate_and_symlink_without_overwrite(tmp_path):
    d = driver(); path = tmp_path/'record.json'
    d.exclusive_json(path, {'status':'COMPLETE'})
    with pytest.raises(FileExistsError):
        d.exclusive_json(path, {'status':'FAILED'})
    assert json.loads(path.read_text()) == {'status':'COMPLETE'}
    link = tmp_path/'link'; link.symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(d.DriverStop, match='OUTPUT_SYMLINK'):
        d.exclusive_json(link/'escaped.json', {})
    assert not (tmp_path/'escaped.json').exists()


def test_existing_formal_directory_is_refused_before_private_creation(tmp_path):
    d = driver(); formal = tmp_path/'formal'; formal.mkdir()
    private = tmp_path/'private'
    with pytest.raises(FileExistsError):
        d.create_run_directories(formal, private)
    assert not private.exists()


def test_sealed_hash_mismatch_is_detected_before_any_numerical_work(tmp_path):
    d = driver(); (tmp_path/'module.py').write_text('original\n')
    manifest = {'code_hashes':{'module.py':d.sha_file(tmp_path/'module.py')}, 'protocol_hashes':{}}
    d.verify_seal(manifest, tmp_path)
    (tmp_path/'module.py').write_text('changed\n')
    with pytest.raises(d.DriverStop, match='SEALED_HASH_MISMATCH'):
        d.verify_seal(manifest, tmp_path)


def test_checkpoint_checks_absolute_global_deadline_even_when_ps_is_throttled(tmp_path):
    d = driver(); clock = [10.0]; stages = []
    class Guard:
        resources = {'thread_snapshot_count':1, 'maximum_observed_os_threads':1, 'peak_rss_bytes':123}
        def remaining_seconds(self): return 100
        def __call__(self, **kwargs):
            assert list(kwargs) == ['stage']
            stages.append(kwargs['stage'])
    cp = d.ResourceCheckpoint(Guard(), 10.1, tmp_path/'ps.jsonl', clock=lambda:clock[0])
    cp(stage='initialization', method='QR33', issue=1)
    clock[0] = 10.05; cp(stage='fit', iteration=500)
    assert stages == ['initialization']
    clock[0] = 10.1
    with pytest.raises(d.DriverStop, match='GLOBAL_DEADLINE'):
        cp(stage='fit', iteration=1000)
    assert stages == ['initialization']


def test_checkpoint_forces_each_cell_end_and_final_resource_measurement(tmp_path):
    d = driver(); stages = []
    class Guard:
        resources = {'thread_snapshot_count':1, 'maximum_observed_os_threads':1, 'peak_rss_bytes':123}
        def remaining_seconds(self): return 100
        def __call__(self, **kwargs): stages.append(kwargs['stage'])
    cp = d.ResourceCheckpoint(Guard(), 20, tmp_path/'ps.jsonl', clock=lambda:10)
    for stage in ('initialization','fit','cell_end','finalization'):
        cp(stage=stage)
    assert stages == ['initialization','cell_end','finalization']
    assert len((tmp_path/'ps.jsonl').read_text().splitlines()) == 3


def test_parent_timeout_kills_inflight_owned_worker_at_global_deadline(tmp_path):
    d = driver(); proc = subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'], start_new_session=True)
    before = time.monotonic()
    result = d.wait_owned_worker(proc, before + .15, hard_seconds=10)
    assert result['status'] == 'FAILED'
    assert result['reason'] == 'GLOBAL_DEADLINE'
    assert proc.poll() is not None
    assert time.monotonic() - before < 3


def test_inventory_preserves_completed_method_and_marks_interrupted_started_method(tmp_path):
    d = driver(); dd = design(); dd['repetitions'] = 1
    unit = list(d.planned_units(dd))[0]; public = tmp_path/'units'/unit['unit_id']; public.mkdir(parents=True)
    d.exclusive_json(d.method_path(public,52,6,'F'), {'status':'COMPLETE','evaluation':{'mean_loss':2.,'strict_breach_count':1,'strict_breach_rate':1/72,'n':72},'candidates':[]})
    d.exclusive_json(d.method_path(public,52,6,'QR33',started=True), {'status':'STARTED'})
    rows = d.build_inventory(dd,tmp_path)
    assert rows[0]['status'] == 'COMPLETE'
    assert rows[0]['evaluation']['mean_loss'] == 2.
    assert rows[1]['status'] == 'FAILED'
    assert rows[1]['reason'] == 'INTERRUPTED_METHOD'
    assert rows[2]['status'] == 'NOT_ATTEMPTED'


def _screen_rows():
    rows = []
    for phi in (.7,.9,.98):
        for p in (0.,.9,.98):
            for w in (52,260,720,2880):
                for h in (6,24):
                    rows.append({'method':'QR33','phi':phi,'variance_persistence':p,'window':w,'horizon':h,
                        'planned_repetitions':32,'complete_repetitions':32,'full_procedure_status':'COMPLETE',
                        'relative_loss_percent':1.,'relative_loss_mcse':0.,'win_fraction':.5})
    return rows


def test_support_requires_target_gains_and_rejects_outside_counterexample():
    d = driver(); rows = _screen_rows()
    target = [r for r in rows if r['horizon']==6 and r['window']>=720 and r['variance_persistence']>=.9]
    assert len(target) == 12
    for r in target[:6]: r.update(relative_loss_percent=-1.,win_fraction=.75)
    assert d.support_for_method(rows,'QR33')['status'] == 'SUPPORTED'
    rows[0].update(relative_loss_percent=-1.,win_fraction=.75)
    assert d.support_for_method(rows,'QR33')['status'] == 'MISMATCH'


def test_support_missing_is_inconclusive_and_two_mcse_boundary_is_strict():
    d = driver(); rows = _screen_rows()
    rows[0].update(relative_loss_percent=-2.,relative_loss_mcse=1.,win_fraction=1.)
    assert d.support_for_method(rows,'QR33')['status'] == 'NOT_SUPPORTED'
    rows[-1].update(complete_repetitions=31,full_procedure_status='NA')
    assert d.support_for_method(rows,'QR33')['status'] == 'INCONCLUSIVE'


@pytest.mark.parametrize('clear,unknown,outside_missing,outside_clear,drop_row,expected',[
    (6,1,False,False,False,'SUPPORTED'),
    (4,1,False,False,False,'NOT_SUPPORTED'),
    (5,1,False,False,False,'INCONCLUSIVE'),
    (0,6,False,False,False,'INCONCLUSIVE'),
    (6,0,True,False,False,'INCONCLUSIVE'),
    (6,1,True,True,False,'MISMATCH'),
    (6,0,False,False,True,'INCONCLUSIVE'),
],ids=['enough-known-target-gains','too-few-possible-target-gains',
       'unresolved-sixth-target-gain','all-six-needed-unresolved','outside-missing',
       'outside-counterexample-takes-precedence','missing-grid-cell'])
def test_support_classifies_only_when_missing_cells_cannot_change_decision(
        clear,unknown,outside_missing,outside_clear,drop_row,expected):
    d=driver();rows=_screen_rows()
    targets=[r for r in rows if r['horizon']==6 and r['window']>=720 and r['variance_persistence']>=.9]
    outside=[r for r in rows if r not in targets]
    for r in targets[:clear]:r.update(relative_loss_percent=-1.,win_fraction=.75)
    for r in targets[clear:clear+unknown]:r.update(complete_repetitions=31,full_procedure_status='NA')
    if outside_missing:outside[0].update(complete_repetitions=31,full_procedure_status='NA')
    if outside_clear:outside[1].update(relative_loss_percent=-1.,win_fraction=.75)
    if drop_row:rows.remove(targets[-1])
    result=d.support_for_method(rows,'QR33')
    assert result['status']==expected
    assert len(result['missing_or_unevaluable_cells'])>=unknown+outside_missing
    if unknown:
        missing=result['missing_or_unevaluable_cells']
        assert any(r['window']==targets[clear]['window'] and r['horizon']==6
            and r['phi']==targets[clear]['phi'] and r['variance_persistence']==targets[clear]['variance_persistence'] for r in missing)


def test_support_duplicate_cell_cannot_replace_missing_grid_identity():
    d=driver();rows=_screen_rows()
    targets=[r for r in rows if r['horizon']==6 and r['window']>=720 and r['variance_persistence']>=.9]
    for r in targets[:6]:r.update(relative_loss_percent=-1.,win_fraction=.75)
    # Preserve the number of target/outside rows while losing an outside identity.
    outside=[r for r in rows if r not in targets]
    rows[rows.index(outside[-1])]=dict(outside[0])
    assert d.support_for_method(rows,'QR33')['status']=='INCONCLUSIVE'


def test_summary_pairs_same_rep_reference_and_retains_missing_reasons(tmp_path):
    d = driver(); dd = design(); dd['repetitions']=2
    dd['phi']=[.7]; dd['variance_persistence']=[0.]; dd['windows']=[52]; dd['horizons']=[6]
    rows=[]
    for rep in range(2):
        for method in ('F','QR33','QR4'):
            rows.append({'rep':rep,'phi_index':0,'p_index':0,'phi':.7,'variance_persistence':0.,'window':52,'horizon':6,
                'method':method,'status':'COMPLETE','reason':None,'candidates':[],
                'evaluation':{'mean_loss': (2. if rep==0 else 6.) * (0.5 if method=='QR33' else 1.),
                    'strict_breach_rate':.25,'strict_breach_count':18,'n':72}})
    rows[-1].update(status='FAILED',reason='NONCONVERGENCE',evaluation=None)
    result = d.aggregate_inventory(dd,rows)
    qr33 = next(r for r in result if r['method']=='QR33')
    qr4 = next(r for r in result if r['method']=='QR4')
    assert qr33['relative_loss_percent'] == -50.
    assert qr33['relative_loss_mcse'] == 0.
    assert qr4['full_procedure_relative_loss_percent'] is None
    assert qr4['conditional_on_completion'] is True
    assert qr4['failure_reasons'] == {'NONCONVERGENCE':1}
    assert qr4['complete_repetitions'] == 1


def test_solver_failure_metadata_remains_scalar_and_preserves_reason_strings():
    d = driver()
    result=d.scalar_diagnostics([{'iterations':10000,'option':'max_iter','passed':False,'gap':.2}])
    assert result == [{'iterations':10000,'option':'max_iter','passed':False,'gap':.2}]
    with pytest.raises(ValueError): d.scalar_diagnostics([{'bad':[1,2]}])


def test_summary_command_requires_termination_and_writes_flat_cells(tmp_path):
    d=driver(); dd=design(); dd['repetitions']=1
    dd['phi']=[.7];dd['variance_persistence']=[0.];dd['windows']=[52];dd['horizons']=[6]
    manifest={'formal_directory':str(tmp_path),'design':dd,'code_hashes':{},'protocol_hashes':{},'design_id':'unit-fixture'}
    d.exclusive_json(tmp_path/'manifest.json',manifest)
    with pytest.raises(FileNotFoundError): d.summarize(tmp_path/'manifest.json')
    assert not (tmp_path/'summary.json').exists()
    d.exclusive_json(tmp_path/'study-termination.json',{'all_workers_terminated':True,'status':'BUDGET_STOP'})
    d.exclusive_json(tmp_path/'inventory.json',d.build_inventory(dd,tmp_path))
    assert d.summarize(tmp_path/'manifest.json')==0
    result=json.loads((tmp_path/'summary.json').read_text())
    assert len(result['cells'])==3
    assert result['cells'][0]['full_procedure_relative_loss_percent'] is None
    assert result['cells'][0]['planned_repetitions']==1
    assert (tmp_path/'summary.csv').exists()
    assert json.loads((tmp_path/'support.json').read_text())['procedures']['QR4']['status']=='INCONCLUSIVE'


def test_inflight_candidate_failure_is_not_relabelled_as_technical_error(tmp_path):
    d=driver()
    class FitError(ValueError):
        code='NONCONVERGENCE';diagnostics={'iterations':10000}
    def report(origins,h,w,method,penalty):
        raise FitError()
    row=d.evaluate_method(design(),tmp_path,52,6,'QR33',report,lambda **kw:None,
        FitError,(d.DriverStop,))
    assert row['status']=='FAILED'
    assert row['reason']=='VALIDATION_INELIGIBLE'
    assert [c['reason'] for c in row['candidates']]==['NONCONVERGENCE']*3
    assert all(c['failure_diagnostics']=={'iterations':10000} for c in row['candidates'])


def test_selected_evaluation_failure_never_tries_another_penalty(tmp_path):
    d=driver(); seen=[]
    class FitError(ValueError):
        code='EVALUATION_FAILED';diagnostics={}
    def report(origins,h,w,method,penalty):
        seen.append((origins,penalty))
        if origins=='evaluation':raise FitError()
        return {'n':72,'mean_loss':2.,'strict_breach_count':0,'strict_breach_rate':0.},[]
    row=d.evaluate_method(design(),tmp_path,52,6,'QR4',report,lambda **kw:None,
        FitError,(d.DriverStop,))
    assert row['status']=='FAILED' and row['reason']=='EVALUATION_FAILED'
    assert row['selected_penalty']==.001
    assert seen==[('validation',.001),('validation',.01),('validation',.1),('validation',1.),('validation',10.),('evaluation',.001)]


def test_resource_and_unknown_candidate_errors_are_persisted_then_propagate(tmp_path):
    d=driver()
    class FitError(ValueError):pass
    for name,exc,reason in [('resource',d.DriverStop('GLOBAL_DEADLINE'),'GLOBAL_DEADLINE'),
                            ('technical',RuntimeError('unexpected'),'TECHNICAL_ERROR')]:
        public=tmp_path/name;public.mkdir()
        def report(*args):raise exc
        with pytest.raises(type(exc)):
            d.evaluate_method(design(),public,52,6,'QR4',report,lambda **kw:None,FitError,(d.DriverStop,))
        row=json.loads(d.method_path(public,52,6,'QR4').read_text())
        assert row['reason']==reason
        assert row['candidates'][0]['reason']==reason
        assert row['candidates'][1]['status']=='NOT_ATTEMPTED'


def test_fit_failure_nonfinite_diagnostic_does_not_erase_solver_failure(tmp_path):
    d=driver()
    class FitError(ValueError):
        code='NONFINITE_ITERATE';diagnostics={'last_value':float('nan'),'iterations':50}
    def report(*args):raise FitError()
    row=d.evaluate_method(design(),tmp_path,52,6,'QR33',report,lambda **kw:None,FitError,(d.DriverStop,))
    assert row['candidates'][0]['reason']=='NONFINITE_ITERATE'
    assert row['candidates'][0]['failure_diagnostics_status']=='NONFINITE_OR_NONSCALAR'


def test_selection_is_sealed_before_evaluation_so_hard_kill_keeps_penalty(tmp_path):
    d=driver()
    class FitError(ValueError):pass
    def report(segment,h,w,method,penalty):
        if segment=='evaluation':
            selection=json.loads((tmp_path/'W52_H6_QR4.selection.json').read_text())
            assert selection['penalty']==.001
            raise d.DriverStop('GLOBAL_DEADLINE')
        return {'n':72,'mean_loss':2.,'strict_breach_count':0,'strict_breach_rate':0.},[]
    with pytest.raises(d.DriverStop):
        d.evaluate_method(design(),tmp_path,52,6,'QR4',report,lambda **kw:None,FitError,(d.DriverStop,))
