"""Constructed audit fixtures only; no study reads, draws or model fits."""
import importlib.util
import json
import math
from pathlib import Path
import statistics

import pytest

SPEC = importlib.util.spec_from_file_location(
    "independent_wp3_audit", Path(__file__).parent / "notes/revision-v8/audit_wp3.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def design():
    return dict(repetitions=4, phi=[.7], variance_persistence=[0.],
        windows=[52], horizons=[6], methods=['F', 'QR33', 'QR4'],
        evaluation_first=10, evaluation_last=13)


def inventory():
    rows=[]
    for rep, (a,b) in enumerate(((2.,1.), (1.,4.), (2.,2.), (4.,9.))):
        for method in ('F','QR33','QR4'):
            rows.append(dict(rep=rep, phi_index=0, p_index=0, phi=.7,
                variance_persistence=0., window=52, horizon=6, method=method,
                status='COMPLETE', reason=None,
                evaluation=dict(mean_loss=b if method=='F' else a,
                    strict_breach_count=rep, n=4, strict_breach_rate=rep/4)))
    return rows


def full_design():
    return dict(repetitions=32, phi=[.7,.9,.98], variance_persistence=[0.,.9,.98],
        windows=[52,260,720,2880], horizons=[6,24], methods=['F','QR33','QR4'])


def screen_rows():
    d=full_design(); out=[]
    for phi in d['phi']:
        for p in d['variance_persistence']:
            for w in d['windows']:
                for h in d['horizons']:
                    out.append(dict(phi=phi,variance_persistence=p,window=w,horizon=h,
                        method='QR33',planned_repetitions=32,complete_repetitions=32,
                        full_procedure_status='COMPLETE',relative_loss_percent=1.,
                        relative_loss_mcse=0.,win_fraction=.5))
    return out


def test_topology_rejects_duplicate_even_when_count_is_unchanged():
    rows=inventory(); rows[-1]=dict(rows[-2])
    errors=audit.inventory_errors(design(),rows)
    assert any(e['code']=='DUPLICATE_INVENTORY_IDENTITY' for e in errors)
    assert any(e['code']=='MISSING_INVENTORY_IDENTITY' for e in errors)


def test_topology_checks_frozen_physical_identity_and_unknown_status():
    rows=inventory(); rows[0]['phi']=.9; rows[1]['status']='SUCCESS'
    errors=audit.inventory_errors(design(),rows)
    assert {e['code'] for e in errors} >= {'INVENTORY_PARAMETER_MISMATCH','INVALID_METHOD_STATUS'}


def test_complete_scores_require_correct_n_and_strict_count_fraction():
    rows=inventory(); rows[0]['evaluation']['n']=3
    rows[1]['evaluation']['strict_breach_rate']=.9
    assert sum(e['code']=='INVALID_COMPLETE_SCORE' for e in audit.inventory_errors(design(),rows))==2


def test_ratio_of_means_and_delta_mcse_are_independently_recomputed():
    qr=next(r for r in audit.paired_oracle(design(),inventory()) if r['method']=='QR33')
    assert qr['relative_loss_percent']==pytest.approx(-43.75)
    ratio=9/16
    sd=statistics.stdev(a-ratio*b for a,b in ((2.,1.),(1.,4.),(2.,2.),(4.,9.)))
    assert qr['relative_loss_mcse']==pytest.approx(100*sd/(2*4))
    assert qr['win_fraction']==.5
    assert qr['win_mcse']==.25
    assert qr['model_breach_mcse']==pytest.approx(statistics.stdev([0.,.25,.5,.75])/2)


def test_failed_reference_cannot_be_paired_with_complete_model():
    rows=inventory(); rows[0].update(status='FAILED',reason='NONCONVERGENCE',evaluation=None)
    qr=next(r for r in audit.paired_oracle(design(),rows) if r['method']=='QR33')
    assert qr['complete_repetitions']==3 and qr['failed_repetitions']==1
    assert qr['full_procedure_status']=='NA'
    assert qr['full_procedure_relative_loss_percent'] is None
    assert qr['conditional_on_completion'] is True


def test_missing_pair_status_and_distinct_reasons_are_preserved():
    rows=inventory()
    rows[0].update(status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',evaluation=None)
    rows[1].update(status='FAILED',reason='INTERRUPTED_METHOD',evaluation=None)
    qr=next(r for r in audit.paired_oracle(design(),rows) if r['method']=='QR33')
    assert qr['failed_repetitions']==1 and qr['unattempted_repetitions']==0
    assert qr['failure_reasons']=={'METHOD_NOT_REACHED':1,'INTERRUPTED_METHOD':1}


def test_no_complete_pairs_do_not_create_zero_estimates():
    rows=inventory()
    for r in rows:r.update(status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',evaluation=None)
    qr=next(r for r in audit.paired_oracle(design(),rows) if r['method']=='QR33')
    assert qr['complete_repetitions']==0 and qr['unattempted_repetitions']==4
    for key in ('relative_loss_percent','model_breach_rate','win_fraction','mean_model_loss'):
        assert qr.get(key) is None


def test_single_completion_keeps_undefined_sample_mcse_null():
    rows=inventory()
    for r in rows[3:]:r.update(status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',evaluation=None)
    qr=next(r for r in audit.paired_oracle(design(),rows) if r['method']=='QR33')
    assert qr['relative_loss_percent']==100.
    assert qr['relative_loss_mcse'] is qr['model_breach_mcse'] is qr['win_mcse'] is None
    assert qr['win_mcse_worst_bound']==.5


def test_support_keeps_enough_known_target_gains_despite_other_target_missing():
    rows=screen_rows(); target=[r for r in rows if r['horizon']==6 and r['window']>=720 and r['variance_persistence']>=.9]
    for r in target[:6]:r.update(relative_loss_percent=-2.,win_fraction=.75)
    target[-1].update(complete_repetitions=31,full_procedure_status='NA')
    assert audit.support_oracle(full_design(),rows,'QR33')['status']=='SUPPORTED'


def test_outside_counterexample_has_priority_over_missing():
    rows=screen_rows(); rows[0].update(relative_loss_percent=-2.,win_fraction=.75)
    rows[-1].update(complete_repetitions=31,full_procedure_status='NA')
    assert audit.support_oracle(full_design(),rows,'QR33')['status']=='MISMATCH'


def test_support_unknown_target_only_matters_if_it_can_change_six_gain_decision():
    rows=screen_rows(); target=[r for r in rows if r['horizon']==6 and r['window']>=720 and r['variance_persistence']>=.9]
    target[-1].update(complete_repetitions=31,full_procedure_status='NA')
    assert audit.support_oracle(full_design(),rows,'QR33')['status']=='NOT_SUPPORTED'
    for r in target[:5]:r.update(relative_loss_percent=-2.,win_fraction=.75)
    assert audit.support_oracle(full_design(),rows,'QR33')['status']=='INCONCLUSIVE'


def test_maturity_checks_validation_and_evaluation_fit_rows():
    row=inventory()[1]
    row['fit_diagnostics']=[dict(refit_index=100,latest_label_end=100,training_count=52)]
    row['candidates']=[dict(status='COMPLETE',fit_diagnostics=[dict(refit_index=100,latest_label_end=101,training_count=52)])]
    errors=audit.maturity_errors([row])
    assert len(errors)==1 and errors[0]['code']=='IMMATURE_TRAINING_LABEL'


def test_numeric_comparison_does_not_equate_null_zero_or_boolean_one():
    assert audit.same_value(None,0.) is False
    assert audit.same_value(True,1) is False
    assert audit.same_value(1.,1.+1e-13) is True
    assert audit.same_value(float('nan'),float('nan')) is False


def test_resource_observations_are_measured_and_hard_caps_checked():
    d=full_design();d['resources']=dict(public_rss_bytes=2**31,maximum_observed_os_threads=2,worker_hard_wall_seconds=600)
    values=[dict(unit_id='a',peak_rss_bytes=100,maximum_observed_os_threads=1,elapsed_seconds=599.9),
            dict(unit_id='b',peak_rss_bytes=2**31+1,maximum_observed_os_threads=3,elapsed_seconds=606.)]
    out=audit.resource_oracle(d,values)
    assert out['maximum_observed_rss_bytes']==2**31+1
    assert {e['code'] for e in out['differences']}=={'RSS_CAP_EXCEEDED','THREAD_CAP_EXCEEDED','WORKER_WALL_EXCEEDED'}


def test_unmeasured_resources_are_unverified_instead_of_budget_values():
    d=full_design();d['resources']=dict(public_rss_bytes=2**31,maximum_observed_os_threads=2,worker_hard_wall_seconds=600)
    out=audit.resource_oracle(d,[dict(unit_id='a',peak_rss_bytes=None,maximum_observed_os_threads=None,elapsed_seconds=1.)])
    assert out['status']=='UNVERIFIED'
    assert out['maximum_observed_rss_bytes'] is None
    assert out['unverified_unit_ids']==['a']


def test_inflight_bundle_is_rejected_before_any_manifest_or_result_read(tmp_path):
    with pytest.raises(ValueError,match='STUDY_NOT_TERMINATED'):
        audit.audit_bundle(tmp_path,tmp_path/'formal-does-not-exist')


def test_audit_module_import_is_stdlib_only():
    import subprocess,sys
    code="import importlib.util,sys; s=importlib.util.spec_from_file_location('aud',sys.argv[1]); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);assert not any(n in sys.modules for n in ('numpy','scipy','v8_mechanism_mc','run_v8_wp3'))"
    r=subprocess.run([sys.executable,'-B','-c',code,str(Path(__file__).parent/'notes/revision-v8/audit_wp3.py')],capture_output=True,text=True)
    assert r.returncode==0,r.stderr


def test_complete_qr33_cannot_hide_a_failed_mandatory_candidate():
    d=design();d.update(validation_first=0,validation_last=3,menus={'QR33':[.001,.01,.1],'QR4':[.001,.01,.1,1.,10.]})
    row=inventory()[1];row['selected_penalty']=.01
    row['candidates']=[dict(penalty=p,status='COMPLETE',origin_count=4,mean_loss=1.) for p in d['menus']['QR33']]
    row['candidates'][0]['status']='FAILED'
    errors=audit.selection_errors(d,[row])
    assert any(e['code']=='INVALID_SELECTED_PENALTY' for e in errors)


def test_selection_ties_follow_distinct_original_menus():
    d=design();d.update(validation_first=0,validation_last=3,menus={'QR33':[.001,.01,.1],'QR4':[.001,.01,.1,1.,10.]})
    rows=[inventory()[1],inventory()[2]]
    for r in rows:
        r['selected_penalty']=.001
        r['candidates']=[dict(penalty=p,status='COMPLETE',origin_count=4,mean_loss=1.) for p in d['menus'][r['method']]]
    errors=audit.selection_errors(d,rows)
    assert len(errors)==1 and errors[0]['method']=='QR33'


def test_complete_bundle_readback_handles_full_all_unattempted_inventory(tmp_path):
    """6912 scalar slots are fixtures, not draws or financial calculations."""
    import datetime as dt,os,subprocess
    d=full_design();d.update(validation_first=10,validation_last=13,
        evaluation_first=20,evaluation_last=23,
        menus={'QR33':[.001,.01,.1],'QR4':[.001,.01,.1,1.,10.]},
        resources=dict(public_rss_bytes=2**31,maximum_observed_os_threads=2,
            worker_hard_wall_seconds=600,total_study_wall_seconds=3600))
    protocol=tmp_path/'protocol';protocol.mkdir()
    (protocol/'design.json').write_text(json.dumps(d))
    env=dict(os.environ,GIT_AUTHOR_NAME='Unit Test',GIT_AUTHOR_EMAIL='test@example.invalid',
        GIT_COMMITTER_NAME='Unit Test',GIT_COMMITTER_EMAIL='test@example.invalid')
    for cmd in (['git','init','-q'],['git','add','protocol'],['git','commit','-q','-m','fixture protocol']):
        subprocess.run(cmd,cwd=tmp_path,env=env,check=True,capture_output=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=tmp_path,text=True).strip()
    started=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=10)).isoformat()
    formal=tmp_path/'formal';formal.mkdir();(formal/'units').mkdir()
    inv=[]
    for rep,pi,gi,w,h,method in sorted(audit.inventory_keys(d)):
        inv.append(dict(rep=rep,phi_index=pi,p_index=gi,phi=d['phi'][pi],
            variance_persistence=d['variance_persistence'][gi],window=w,horizon=h,
            method=method,status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',evaluation=None,
            selected_penalty=None,candidates=[dict(penalty=p,status='NOT_ATTEMPTED') for p in d['menus'].get(method,[])]))
    (formal/'inventory.json').write_text(json.dumps(inv))
    summary=audit.paired_oracle(d,inv)
    (formal/'manifest.json').write_text(json.dumps(dict(design=d,design_commit=commit,started_utc=started,
        code_hashes={},protocol_hashes={'protocol/design.json':audit.sha(protocol/'design.json')})))
    (formal/'study-termination.json').write_text(json.dumps(dict(status='BUDGET_STOP',
        all_workers_terminated=True,method_status_counts={'NOT_ATTEMPTED':6912},
        attempted_workers=0,completed_workers=0,elapsed_seconds=0.,code_hash_check='PASS')))
    (formal/'summary.json').write_text(json.dumps(dict(cells=summary,study_status='BUDGET_STOP',
        source_inventory_sha256=audit.sha(formal/'inventory.json'))))
    (formal/'support.json').write_text(json.dumps(dict(procedures={m:audit.support_oracle(d,summary,m) for m in ('QR33','QR4')},
        broad_conditional_models_restriction='INCONCLUSIVE')))
    checked=audit.audit_bundle(tmp_path,formal)
    assert checked['difference_count']==0,checked['differences']
    assert checked['actual_inventory_count']==6912 and checked['summary_cell_count']==216
    assert checked['support']['QR33']['status']=='INCONCLUSIVE'
    summary[0]['unattempted_repetitions']=0
    (formal/'summary.json').write_text(json.dumps(dict(cells=summary,study_status='BUDGET_STOP',
        source_inventory_sha256=audit.sha(formal/'inventory.json'))))
    checked=audit.audit_bundle(tmp_path,formal)
    assert any(e['code']=='SUMMARY_VALUE_MISMATCH' for e in checked['differences'])


def test_saved_rng_states_must_match_within_repetition_without_rng_draws(tmp_path):
    units=tmp_path/'units';units.mkdir()
    for i in range(2):
        folder=units/str(i);folder.mkdir()
        (folder/'rng-receipt.json').write_text(json.dumps(dict(rep=0,normals=5,
            initial_state={'state':1},final_state={'state':2+i})))
    errors=audit.rng_receipt_errors(dict(repetitions=2,burn_in=3,retained_observations=2),tmp_path)
    assert [e['code'] for e in errors]==['COMMON_RANDOM_STATE_MISMATCH']
