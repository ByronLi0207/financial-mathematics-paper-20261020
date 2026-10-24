"""Constructed checks for v9 provenance, geometry and complete-cell reporting."""
import importlib
import json
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace
import numpy as np
import pytest


def api():
    assert Path(__file__).with_name('run_v9_nonstationarity.py').exists(), 'v9 driver API not implemented'
    return importlib.import_module('run_v9_nonstationarity')


def rep(r, q=1., f=1., status='COMPLETE'):
    return dict(rep=r,status=status,qr_mean_loss=q,f_mean_loss=f,qr_breaches=4,f_breaches=3,n=72)


def cells():
    return [dict(source_id=f's{i}',arm=a,window=w,method='QR33',status='COMPLETE',
                 relative_median_pct=(i+1 if a=='switching' else i-6))
            for i in range(13) for a in ['constant','switching'] for w in [52,260]]


def diagnostics(reject=7, unknown=0):
    rows=[dict(source_id=f's{i}',kind='weekly',status='NONREGULAR_NULL' if reject<=i<reject+unknown else 'COMPLETE',
               p_value=None if reject<=i<reject+unknown else (.001 if i<reject else .9),n=405,partition={'cuts':[200]}) for i in range(13)]
    rows += [dict(source_id='fx_daily',kind='daily',status='COMPLETE',p_value=.001,n=405,partition={'cuts':[200]}),
             dict(source_id='fx_hourly',kind='hourly',status='COMPLETE',p_value=.8,n=8109,partition={'cuts':[2000,4000]})]
    return rows


def test_prefix_excludes_poisoned_future_and_returns_readonly():
    m=api();x=np.arange(20,dtype=float);times=np.arange(20).astype('datetime64[D]')
    first=m.prefix_before_evaluation(x,times,5);x[5:]=np.nan
    second=m.prefix_before_evaluation(x,times,5)
    np.testing.assert_array_equal(first[0],second[0]);np.testing.assert_array_equal(second[0],np.arange(5))
    assert not second[0].flags.writeable and not second[1].flags.writeable


def test_complete_cell_uses_repetition_median_iqr_and_strict_wins():
    s=api().reduce_cell([rep(0,1.2),rep(1,.8)],2)
    assert s['status']=='COMPLETE';assert s['relative_median_pct']==pytest.approx(0)
    assert s['q25_pct']==pytest.approx(-10);assert s['q75_pct']==pytest.approx(10)
    assert s['win_fraction']==.5 and s['completed_repetitions']==2


@pytest.mark.parametrize('records',[ [rep(0),rep(1,status='FAILED')], [rep(0)], [rep(0),rep(0)] ])
def test_failed_missing_or_duplicate_rep_never_yields_partial_median(records):
    s=api().reduce_cell(records,2)
    assert s['status']=='FAILED' and s['relative_median_pct'] is None


def test_zero_f_loss_is_not_replaced_by_epsilon():
    s=api().reduce_cell([rep(0,0,0)],1)
    assert s['status']=='FAILED' and s['relative_median_pct'] is None


def test_incomplete_label_grid_is_not_averaged():
    row=rep(0);row['n']=71
    assert api().reduce_cell([row],1)['status']=='FAILED'


def test_primary_predictions_use_all_thirteen_source_medians():
    p=api().prediction_status(cells(),diagnostics(),[f's{i}' for i in range(13)])
    assert p['N1']['status']=='SUPPORTED' and p['N2']['status']=='SUPPORTED'
    assert p['N3']['status']=='SUPPORTED' and p['N4']['status']=='SUPPORTED'
    assert p['N2']['switching_W52_median_pct']==7 and p['N3']['constant_W52_median_pct']==0
    assert p['N1']['family_size']==13


def test_unknown_diagnostics_keep_count_bounds_and_family_size():
    p=api().prediction_status(cells(),diagnostics(6,1),[f's{i}' for i in range(13)])
    assert p['N1']['status']=='UNASSESSABLE'
    assert p['N1']['known_rejections']==6 and p['N1']['maximum_rejections']==7 and p['N1']['family_size']==13


def test_insufficient_upper_bound_is_not_supported():
    p=api().prediction_status(cells(),diagnostics(4,2),[f's{i}' for i in range(13)])
    assert p['N1']['status']=='NOT_SUPPORTED'


def test_failed_switching_source_invalidates_N2_but_not_N3():
    c=cells();next(r for r in c if r['source_id']=='s0' and r['arm']=='switching' and r['window']==52).update(status='FAILED',relative_median_pct=None)
    p=api().prediction_status(c,diagnostics(),[f's{i}' for i in range(13)])
    assert p['N2']['status']=='UNASSESSABLE' and p['N3']['status']=='SUPPORTED'


def test_QR4_failure_does_not_replace_QR33_primary_result():
    c=cells()+[dict(source_id='s0',arm='switching',window=52,method='QR4',status='FAILED',relative_median_pct=None)]
    assert api().prediction_status(c,diagnostics(),[f's{i}' for i in range(13)])['N2']['status']=='SUPPORTED'


def test_N4_requires_both_qualified_global_diagnostics():
    d=diagnostics();d[-1].update(status='NONREGULAR_NULL',p_value=None)
    assert api().prediction_status(cells(),d,[f's{i}' for i in range(13)])['N4']['status']=='UNASSESSABLE'


@pytest.mark.parametrize('remaining,R,methods,fits',[(1400,32,['QR33','QR4'],True),(1000,16,['QR33','QR4'],True),(500,16,['QR33'],True),(300,16,['QR33'],False)])
def test_projection_obeys_only_registered_reduction_order(remaining,R,methods,fits):
    units=[dict(complete=True,seconds_by_method={'generation':1.,'F':1.,'QR33':2.,'QR4':4.}) for _ in range(26)]
    d=dict(worker_count=4,pilot_repetitions=2,projection_safety_factor=1.35,projection_reserve_seconds=180,worker_hard_seconds=600)
    plan=api().choose_configuration(units,remaining,d)
    assert plan['repetitions']==R and plan['conditional_methods']==methods and plan['predicted_fits']==fits


def test_incomplete_pilot_selects_last_configuration_without_rule_search():
    units=[dict(complete=False,seconds_by_method={})]
    d=dict(worker_count=4,pilot_repetitions=2,projection_safety_factor=1.35,projection_reserve_seconds=180,worker_hard_seconds=600)
    plan=api().choose_configuration(units,50000,d)
    assert plan['repetitions']==16 and plan['conditional_methods']==['QR33']


def test_registered_design_is_only_the_committed_file_and_unchanged_inputs():
    d=api().read_design()
    assert d['base_pr5_commit']=='0f1f066843e0c49cf3e24bce7d72032dc189603d'
    assert d['validation_first']==3072 and d['evaluation_first']==3168 and d['horizon']==6
    assert d['windows']==[52,260] and d['global_study_seconds']==5400


def test_qualified_N4_with_failed_partition_is_unassessable():
    d=diagnostics();d[-1]['partition']=None
    assert api().prediction_status(cells(),d,[f's{i}' for i in range(13)])['N4']['status']=='UNASSESSABLE'


def test_source_adapter_uses_the_original_SourceSeries_dates_contract(monkeypatch):
    from conditional_sources import SourceSeries
    import conditional_sources
    m=api();t=np.arange(706).astype('datetime64[D]');x=np.arange(706,dtype=float)
    source=SourceSeries('nyfed_weekly',t,x,'fixture',0,{})
    monkeypatch.setattr(conditional_sources,'load_source',lambda *a,**kw:source)
    values,times,info=m.load_prefix(0,m.read_design())
    np.testing.assert_array_equal(values,x[:405]);np.testing.assert_array_equal(times,t[:405])
    assert info['last_raw_index_used']==404


def artificial_calibration(partition=True, segment_ok=True):
    p=dict(intercept=0.,phi=.5,omega=.2,alpha=.1,beta=.6,nu=8.)
    return dict(source_id='fixture-weekly',source_index=0,kind='weekly',n=405,M=404,
        whole_fit={'params':p},calibration_status='COMPLETE' if partition and segment_ok else 'FAILED_SEGMENT_FIT',
        partition={'cuts':[202],'segment_lengths':[202,202]} if partition else None,
        segment_fits=[{'params':p},{'params':dict(p,intercept=1.)}] if segment_ok else [{'params':p},{'status':'FAILED'}])


def install_artificial_forecast(monkeypatch, *, fail_switching=False, interrupt_qr4=False):
    import v9_switching,run_v8_wp3
    from run_study import StudyStop
    def generate(whole,segments,lengths,source,rep,R,tag,d,checkpoint=None):
        if fail_switching and len(segments)>1:raise ValueError('artificial switching overflow')
        n=d['retained_observations'];arm=dict(position=np.linspace(-1.,1.,n),variance=np.ones(n),
            innovations=np.zeros(n),regime_ids=np.zeros(n,dtype=int),transition_indices=np.array([],dtype=int),wrap_indices=np.array([],dtype=int))
        return dict(constant=arm,switching=arm,phase=rep*sum(lengths)//R,
            uniform_sha256='fixture-u',rng_initial={'fixture':0},rng_final={'fixture':1})
    def evaluate(d,public,w,h,method,report,checkpoint,fit_error,resource_errors):
        if interrupt_qr4 and method=='QR4':raise StudyStop('ARTIFICIAL_INTERRUPT')
        return dict(status='COMPLETE',reason=None,selected_penalty=.01 if method!='F' else None,
            evaluation=dict(mean_loss=1. if method=='F' else 1.1,n=72,strict_breach_count=3))
    monkeypatch.setattr(v9_switching,'generate_pair',generate)
    monkeypatch.setattr(run_v8_wp3,'evaluate_method',evaluate)


@pytest.mark.parametrize('partition,segment_ok',[(False,True),(True,False)])
def test_failed_switching_calibration_preserves_valid_constant(monkeypatch,tmp_path,partition,segment_ok):
    install_artificial_forecast(monkeypatch)
    r=api().simulate_unit(artificial_calibration(partition,segment_ok),0,2,1,api().read_design(),tmp_path/'unit')
    constant=[x for x in r['records'] if x['arm']=='constant'];switching=[x for x in r['records'] if x['arm']=='switching']
    assert len(constant)==4 and all(x['status']=='COMPLETE' for x in constant)
    assert len(switching)==4 and all(x['status']=='FAILED' for x in switching)


def test_switching_generation_failure_never_discards_constant(monkeypatch,tmp_path):
    install_artificial_forecast(monkeypatch,fail_switching=True)
    r=api().simulate_unit(artificial_calibration(),0,2,1,api().read_design(),tmp_path/'unit')
    assert len([x for x in r['records'] if x['arm']=='constant' and x['status']=='COMPLETE'])==4
    assert len([x for x in r['records'] if x['arm']=='switching' and x['status']=='FAILED'])==4


def test_resource_interruption_keeps_finished_comparison_and_early_rng_geometry(monkeypatch,tmp_path):
    from run_study import StudyStop
    install_artificial_forecast(monkeypatch,interrupt_qr4=True)
    out=tmp_path/'unit'
    with pytest.raises(StudyStop):api().simulate_unit(artificial_calibration(),0,2,1,api().read_design(),out)
    saved=json.loads((out/'comparison-constant-W52-QR33.json').read_text())
    assert saved['status']=='COMPLETE' and saved['qr_mean_loss']==1.1
    geometry=json.loads((out/'geometry-constant.json').read_text())
    assert geometry['uniform_sha256']=='fixture-u' and geometry['rng_initial']=={'fixture':0}
    assert len(geometry['regime_ids'])==3264 and 'exposure' in geometry


def test_parent_worker_exit_recovers_saved_comparisons_and_source_identity(monkeypatch,tmp_path):
    m=api();manifest=tmp_path/'manifest.json'
    manifest.write_text(json.dumps(dict(design={'worker_hard_seconds':600},sources=[{'source_id':'fixture-weekly','kind':'weekly'}])))
    out=tmp_path/'unit/result.json'
    saved=dict(source_id='fixture-weekly',arm='constant',window=52,method='QR33',**rep(0))
    class DeadChild:
        returncode=-9
        def poll(self):return -9
    def launch(command,**kwargs):
        destination=Path(command[command.index('--output')+1]);(destination.parent/'comparison-constant-W52-QR33.json').write_text(json.dumps(saved))
        return DeadChild()
    monkeypatch.setattr(m.subprocess,'Popen',launch)
    m.run_batch([dict(worker='worker-forecast',source=0,rep=0,plan='fixture',output=str(out),private=str(tmp_path/'private'))],manifest,m.time.monotonic()+60,1)
    row=json.loads(out.read_text())
    assert row['complete'] is False and row['source_id']=='fixture-weekly' and row['records']==[saved]


def worker_fixture(monkeypatch,tmp_path,calibration):
    m=api();d=m.read_design();root=tmp_path/'public';path=root/'diagnostics/units/s00/result.json';path.parent.mkdir(parents=True);path.write_text(json.dumps(calibration))
    manifest=tmp_path/'manifest.json';manifest.write_text(json.dumps({'sources':[{'source_id':'fixture-weekly','kind':'weekly'}]}))
    plan=tmp_path/'plan.json';plan.write_text(json.dumps({'repetitions':2,'stream_tag':1,'conditional_methods':['QR33','QR4']}))
    monkeypatch.setattr(m,'PUBLIC',root);monkeypatch.setattr(m,'read_design',lambda:d);monkeypatch.setattr(m,'verify_seal',lambda _:None)
    monkeypatch.setattr(m,'worker_runtime',lambda *a:(SimpleNamespace(resources={}),lambda **kw:None))
    return m,SimpleNamespace(manifest=str(manifest),plan=str(plan),source=0,rep=0,output=str(tmp_path/'result.json'),private=str(tmp_path/'private'))


def test_forecast_worker_missing_source_id_uses_frozen_inventory(monkeypatch,tmp_path):
    m,args=worker_fixture(monkeypatch,tmp_path,dict(calibration_status='FAILED',whole_fit=None))
    m.forecast_worker(args)
    assert json.loads(Path(args.output).read_text())['source_id']=='fixture-weekly'


def test_daily_diagnostic_keeps_break_dates_for_reporting_without_raw_reaccess(monkeypatch,tmp_path):
    import v9_nonstationarity as stats
    m,args=worker_fixture(monkeypatch,tmp_path,{})
    monkeypatch.setattr(m,'source_inventory',lambda d:[dict(source_id='fx_daily',kind='daily',stop=405)])
    x=np.arange(7,dtype=float);times=np.datetime64('2000-01-01')+np.arange(7)*np.timedelta64(1,'D')
    monkeypatch.setattr(m,'load_prefix',lambda *a:(x,times,dict(n=7,M=6)))
    monkeypatch.setattr(stats,'locate_breaks',lambda *a:dict(cuts=[2],segment_lengths=[2,4]))
    monkeypatch.setattr(stats,'fit_ar_garch',lambda *a,**k:{'params':artificial_calibration()['whole_fit']['params']})
    monkeypatch.setattr(stats,'bootstrap_stability',lambda *a,**k:dict(status='COMPLETE',p_value=.1))
    m.diagnostic_worker(args)
    assert json.loads(Path(args.output).read_text())['break_dates']==['2000-01-04']


def temporary_plan_repository(tmp_path):
    root=tmp_path/'repo';root.mkdir();env=dict(os.environ,GIT_AUTHOR_NAME='Fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',GIT_COMMITTER_NAME='Fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid')
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,env=env,stderr=subprocess.STDOUT).decode().strip()
    git('init','-q');(root/'README').write_text('fixture\n');git('add','README');git('commit','-q','-m','fixture base')
    path=root/'results/v9/nonstationarity/run-plan.json';path.parent.mkdir(parents=True)
    plan=dict(repetitions=16,conditional_methods=['QR33'],design_commit=api().DESIGN_COMMIT,code_sha256={'fixture':'digest'})
    path.write_text(json.dumps(plan));manifest={'code_sha256':plan['code_sha256']}
    return root,path,manifest,plan,git


def test_formal_requires_run_plan_already_committed_and_unchanged(tmp_path):
    root,path,manifest,plan,git=temporary_plan_repository(tmp_path)
    with pytest.raises(ValueError):api().verify_committed_run_plan(manifest,root=root,path=path)
    git('add',str(path.relative_to(root)));git('commit','-q','-m','freeze run plan')
    actual,receipt=api().verify_committed_run_plan(manifest,root=root,path=path)
    assert actual==plan and receipt['commit']==git('rev-parse','HEAD')
    path.write_text(json.dumps(dict(plan,repetitions=32)))
    with pytest.raises(ValueError):api().verify_committed_run_plan(manifest,root=root,path=path)


def test_formal_run_plan_commit_must_be_separate_and_match_sealed_code(tmp_path):
    root,path,manifest,plan,git=temporary_plan_repository(tmp_path)
    (root/'README').write_text('changed alongside plan\n');git('add','.');git('commit','-q','-m','mixed commit')
    with pytest.raises(ValueError):api().verify_committed_run_plan(manifest,root=root,path=path)


def diagnostic_artificial_fixture(monkeypatch,tmp_path):
    import v9_nonstationarity as stats
    m,args=worker_fixture(monkeypatch,tmp_path,{})
    monkeypatch.setattr(m,'source_inventory',lambda d:[dict(source_id='fixture-weekly',kind='weekly',stop=405)])
    x=np.arange(7,dtype=float);times=np.datetime64('2000-01-01')+np.arange(7)*np.timedelta64(1,'D')
    monkeypatch.setattr(m,'load_prefix',lambda *a:(x,times,dict(n=7,M=6)))
    monkeypatch.setattr(stats,'locate_breaks',lambda *a:dict(cuts=[],segment_lengths=[6]))
    monkeypatch.setattr(stats,'fit_ar_garch',lambda *a,**k:{'params':artificial_calibration()['whole_fit']['params']})
    completed=dict(status='COMPLETE',p_value=.01,statistic=4.2,B=2,bootstrap_statistics=[1.,2.],
        rng_initial_state={'fixture':0},rng_final_state={'fixture':1},moment={'qualified':True})
    monkeypatch.setattr(stats,'bootstrap_stability',lambda *a,**k:completed.copy())
    return m,args,stats,completed


def test_outer_diagnostic_resource_failure_archives_evidence_but_clears_primary_p(monkeypatch,tmp_path):
    from run_study import StudyStop
    m,args,stats,completed=diagnostic_artificial_fixture(monkeypatch,tmp_path)
    def checkpoint(**kw):
        if kw.get('stage')=='finalization':raise StudyStop('ARTIFICIAL_FINAL_RESOURCE')
    monkeypatch.setattr(m,'worker_runtime',lambda *a:(SimpleNamespace(resources={}),checkpoint))
    m.diagnostic_worker(args);row=json.loads(Path(args.output).read_text())
    assert row['status']=='FAILED' and row['p_value'] is None
    evidence=row['completed_diagnostic_evidence']
    assert all(evidence[k]==v for k,v in completed.items())
    assert row['whole_fit']['params'] is not None


def test_handled_segment_fit_failure_does_not_erase_completed_global_p(monkeypatch,tmp_path):
    m,args,stats,completed=diagnostic_artificial_fixture(monkeypatch,tmp_path)
    monkeypatch.setattr(stats,'locate_breaks',lambda *a:dict(cuts=[2],segment_lengths=[2,4]))
    def fit(*args,**kwargs):
        if kwargs:raise stats.CalibrationError('ARTIFICIAL_SEGMENT_FAILURE')
        return {'params':artificial_calibration()['whole_fit']['params']}
    monkeypatch.setattr(stats,'fit_ar_garch',fit)
    m.diagnostic_worker(args);row=json.loads(Path(args.output).read_text())
    assert row['status']=='COMPLETE' and row['p_value']==.01
    assert row['calibration_status']=='FAILED_SEGMENT_FIT' and row['whole_fit']['params'] is not None
