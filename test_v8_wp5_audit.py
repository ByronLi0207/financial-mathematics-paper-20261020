"""WP5 independent readback fixtures; no accepted FX input or fitted model."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pytest

SPEC=importlib.util.spec_from_file_location('wp5_audit',Path(__file__).parent/'notes/revision-v8/audit_wp5.py')
audit=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(audit)


def design():
    return dict(sample=dict(evaluation_first=50,evaluation_last=74,evaluation_count=25,
        feature_valid_from=25,longest_window=20,max_horizon=6,original_validation_first=81),
        clock_and_target={'horizons':[2,6]},
        methods=[dict(name='F_matched',engine='F',window=20,refit_step=4,penalty_by_horizon=None),
            dict(name='F_rolling720',engine='F',window=20,refit_step=1,penalty_by_horizon=None),
            dict(name='QR33',engine='QR33',window=20,refit_step=4,penalty_by_horizon={'2':.01,'6':.001}),
            dict(name='QR4',engine='QR4',window=20,refit_step=4,penalty_by_horizon={'2':.01,'6':.01})],
        solver={'max_iter':10000},known_exposure=dict(R6_retro_evaluation=[60,74],
            overlap_with_retro_evaluation_origins=15,R3_H24_W2880_first_scored_block=[50,53]),
        three_window_summary={'windows':[dict(name='extra_full_prefix',first=50,last=74),
            dict(name='previous_retro',first=60,last=74),dict(name='original_inspected',first=90,last=99)]})


def test_geometry_keeps_fixed_full_prefix_and_mature_labels():
    result=audit.geometry_oracle(100,design())
    assert result['evaluation_first']==50 and result['evaluation_last']==74
    assert result['evaluation_count']==25 and result['status']=='READY'
    assert result['last_target_index']==80
    assert audit.geometry_oracle(80,design())['status']=='NA_SAMPLE_SIZE'


def test_geometry_rejects_moved_endpoint_and_inconsistent_count():
    d=design();d['sample']['evaluation_count']=24
    with pytest.raises(ValueError):audit.geometry_oracle(100,d)
    d=design();d['sample']['original_validation_first']=80
    with pytest.raises(ValueError):audit.geometry_oracle(100,d)


def test_score_includes_current_state_and_ties_are_not_hits():
    result=audit.score_oracle(np.array([9.,2.,-3.,1.,4.]),np.array([0,1]),np.array([9.,2.]),2)
    assert result['peak'].tolist()==[9.,3.]
    assert result['strict_breach'].tolist()==[False,True]
    assert result['pinball'].tolist()==[0.,.95]
    assert result['mean_loss']==.475 and result['strict_breach_count']==1


def test_score_rejects_floor_violation_incomplete_target_and_dropped_issue():
    with pytest.raises(ValueError):audit.score_oracle(np.array([9.,2.,3.]),np.array([0]),np.array([8.]),2)
    with pytest.raises(ValueError):audit.score_oracle(np.array([9.,2.,3.]),np.array([1]),np.array([9.]),2)
    with pytest.raises(ValueError):audit.score_oracle(np.arange(10.),np.array([3,5]),np.array([9.,9.]),2)


def test_f_oracle_freezes_mature_own_anchor_rank_but_rolling_refits_each_issue():
    x=np.arange(100,dtype=float);ids=np.arange(50,75,dtype=np.int64)
    frozen=audit.f_oracle(x,ids,6,20,4,50)
    rolling=audit.f_oracle(x,ids,6,20,1,50)
    assert frozen['capacity'].tolist()==(ids+6).astype(float).tolist()
    assert frozen['refit_indices'].tolist()==[50+4*(i//4) for i in range(25)]
    assert rolling['refit_indices'].tolist()==ids.tolist()


def test_f_oracle_rejects_unavailable_corrected_rank():
    with pytest.raises(ValueError,match='UNAVAILABLE_CORRECTED_RANK'):
        audit.f_oracle(np.arange(100.),np.arange(50,75),6,3,4,50)


def test_dm_oracle_uses_divisor_n_bartlett_original_bandwidth_and_normal_only():
    d=np.array([1.,2.,-1.,3.,1.,-2.,4.,-1.,2.,1.]);h=2
    result=audit.normal_dm_oracle(d,h)
    L=max(h,int(4*(len(d)/100)**(2/9)));centered=d-d.mean()
    v=float(centered@centered)/len(d)
    for k in range(1,L+1):v+=2*(1-k/(L+1))*float(centered[k:]@centered[:-k])/len(d)
    statistic=math.fsum(d)/len(d)/math.sqrt(v/len(d))
    assert result['bandwidth']==L and result['lrv']==pytest.approx(v)
    assert result['dm_t']==pytest.approx(statistic)
    assert result['dm_p']==pytest.approx(math.erfc(abs(statistic)/math.sqrt(2)))
    assert not any(k.startswith('hln') for k in result)


def test_dm_constant_losses_stay_na_without_epsilon_repair():
    zero=audit.normal_dm_oracle(np.zeros(10),2)
    constant=audit.normal_dm_oracle(np.ones(10),2)
    assert zero['status']=='IDENTICAL_LOSSES' and zero['dm_t'] is None
    assert constant['status']=='ZERO_LONG_RUN_VARIANCE' and constant['dm_p'] is None


@pytest.mark.parametrize('bad',[[1.,float('nan')],[1.,float('inf')],[[1.,2.]]])
def test_dm_invalid_vectors_rejected(bad):
    with pytest.raises(ValueError):audit.normal_dm_oracle(bad,1)


def fixture_trace(method='F_matched'):
    d=design();x=np.arange(100,dtype=float);ids=np.arange(50,75,dtype=np.int64)
    step=next(m['refit_step'] for m in d['methods'] if m['name']==method)
    score=audit.score_oracle(x,ids,x[ids]+6,6)
    trace=dict(origins=ids,refit_indices=50+step*((ids-50)//step),capacity=x[ids]+6,
        **{k:score[k] for k in ('peak','floor','pinball','strict_breach')})
    return d,x,trace


def test_trace_independently_checks_complete_fixed_grid_refits_and_scores():
    d,x,trace=fixture_trace()
    assert audit.trace_errors(x,trace,6,'F_matched',d)==[]
    short={k:v[:-1] for k,v in trace.items()}
    assert any(e['code']=='TRACE_ISSUE_GRID_MISMATCH' for e in audit.trace_errors(x,short,6,'F_matched',d))
    altered=copy.deepcopy(trace);altered['refit_indices']+=1
    assert any(e['code']=='TRACE_REFIT_GRID_MISMATCH' for e in audit.trace_errors(x,altered,6,'F_matched',d))


def test_trace_replays_f_and_rejects_changed_pinball_or_nonstrict_hit():
    d,x,trace=fixture_trace()
    bad=copy.deepcopy(trace);bad['capacity']+=1
    assert any(e['code']=='F_DETERMINISTIC_REPLAY_MISMATCH' for e in audit.trace_errors(x,bad,6,'F_matched',d))
    bad=copy.deepcopy(trace);bad['pinball'][2]=1
    assert any(e['code']=='TRACE_VALUE_MISMATCH' for e in audit.trace_errors(x,bad,6,'F_matched',d))
    bad=copy.deepcopy(trace);bad['strict_breach'][2]=True
    assert any(e['code']=='TRACE_STRICT_BREACH_MISMATCH' for e in audit.trace_errors(x,bad,6,'F_matched',d))


def test_pinned_csv_verifies_bytes_hash_and_order_without_source_sort(tmp_path):
    body=b'datetime,NetPosUsd,NetUsdPnL,AbsVolume,Mid\n2014.01.02T01:00:00.000000,1,0,0,0\n2014.01.02T02:00:00.000000,-2,0,0,0\n'
    path=tmp_path/'fixture.csv';path.write_bytes(body)
    source=dict(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),expected_original_rows=2)
    x,t=audit.read_pinned_csv(path,source)
    assert x.tolist()==[1.,-2.] and len(t)==2
    with pytest.raises(ValueError,match='SOURCE_IDENTITY'):
        audit.read_pinned_csv(path,dict(source,sha256='0'*64))
    reversed_body=body.splitlines(keepends=True)
    raw=reversed_body[0]+reversed_body[2]+reversed_body[1];path.write_bytes(raw)
    with pytest.raises(ValueError,match='SOURCE_CHRONOLOGY'):
        audit.read_pinned_csv(path,dict(source,sha256=hashlib.sha256(raw).hexdigest()))


def test_overlap_is_not_independent_third_period():
    result=audit.exposure_oracle(design())
    assert result['overlap_origins']==15 and result['previous_retro_fully_nested']
    assert result['fresh_independent_third_period'] is False
    assert result['scientific_status']=='MISMATCH'
    d=design();d['known_exposure']['overlap_with_retro_evaluation_origins']=14
    with pytest.raises(ValueError):audit.exposure_oracle(d)


def test_failed_method_cannot_publish_shortened_evaluation():
    row=dict(status='FAILED',reason='NONCONVERGENCE',evaluation={'n':2})
    assert audit.failed_row_errors(row)==[{'code':'FAILED_METHOD_HAS_AGGREGATE'}]
    row['evaluation']=None
    assert audit.failed_row_errors(row)==[]


def test_relative_csv_values_and_optional_na_are_serialized_without_changes(tmp_path):
    path=tmp_path/'table.csv';path.write_text('x,z\n1.25,NA\n')
    assert audit.csv_errors(path,[dict(x=1.25,z=None)])==[]
    path.write_text('x,z\n1.2,NA\n')
    assert audit.csv_errors(path,[dict(x=1.25,z=None)])[0]['code']=='CSV_VALUES_MISMATCH'


def test_prior_scoring_metadata_verifies_completion_hash_and_full_target_union(tmp_path):
    source=tmp_path/'results/retro.json';source.parent.mkdir();d=design()
    metadata=dict(groups=[dict(group=dict(phase='retro',source='fx_hourly',horizon=6,window=20),
        selections={'R3':dict(status='SELECTED',candidates=[dict(status='COMPLETE',n=4) for _ in range(6)])},
        rows=[dict(report='R3',status='COMPLETE')],r3_fold_bounds=[[50,53]])])
    source.write_text(json.dumps(metadata));notes=tmp_path/'notes/revision-v8';notes.mkdir(parents=True)
    proof=dict(status='PASS',source='results/retro.json',source_sha256=audit.sha(source),
        R3_selection_status='SELECTED',R3_complete_candidate_count=6,R3_candidate_scored_issue_count=4,
        old_H24_target_coverage_merged=[[50,80]],new_H24_target_bounds=[50,80],
        nested_old_retro_issue_count=15,fresh_unscored_third_period=False,mismatch='MISMATCH-WP5-01')
    path=notes/'wp5-prior-exposure-proof.json';path.write_text(json.dumps(proof))
    assert audit.exposure_metadata_errors(tmp_path,d)==[]
    metadata['groups'][0]['selections']['R3']['candidates'][2]['status']='FAILED';source.write_text(json.dumps(metadata))
    assert audit.exposure_metadata_errors(tmp_path,d)==[{'code':'EXPOSURE_SOURCE_HASH_MISMATCH'}]
    proof['source_sha256']=audit.sha(source);path.write_text(json.dumps(proof))
    assert any(e['code']=='PRIOR_R3_SCORING_COMPLETION_UNVERIFIED' for e in audit.exposure_metadata_errors(tmp_path,d))


def test_maturity_diagnostics_reject_immature_label_even_with_complete_scores():
    d=design();first,last=50,74;h=6;fits=[]
    for r in range(first,last+1,4):
        fits.append(dict(refit_index=r,training_first_origin=r-h-20+1,
            training_last_origin=r-h,training_count=20,latest_label_end=r))
    report=dict(fit_diagnostics=fits,maturity=dict(refit_count=len(fits),training_first_origin_min=25,
        training_last_origin_max=68,latest_label_end_max=74,maximum_label_end_minus_refit=0))
    assert audit.fit_errors(report,h,'F_matched',d)==[]
    report['fit_diagnostics'][0]['latest_label_end']=51
    assert any(e['code']=='IMMATURE_TRAINING_LABEL' for e in audit.fit_errors(report,h,'F_matched',d))


def test_complete_constructed_bundle_and_corrupted_dm_are_checked(tmp_path):
    """Straight-line arithmetic fixture; no financial path/model fit."""
    import csv,datetime as dt,os,subprocess
    root=tmp_path/'repo';root.mkdir();d=design();d['resources']=dict(maximum_rss_bytes=2**31,
        maximum_observed_os_threads=2,worker_hard_seconds=600,global_wall_seconds=1800)
    d['original_and_sealed_modules_sha256']={}
    formal=root/'results/revision-v8/wp5';(formal/'units').mkdir(parents=True)
    private=root/'.scratch/revision-v8/wp5/fixture';private.mkdir(parents=True)
    raw=root/'.scratch/data/fixture.csv';raw.parent.mkdir(parents=True)
    with raw.open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(audit.HEADER)
        for i in range(100):writer.writerow([(dt.datetime(2000,1,1)+dt.timedelta(hours=i)).strftime('%Y.%m.%dT%H:%M:%S.%f'),i,0,0,0])
    d['input']=dict(local_private_path='.scratch/data/fixture.csv',bytes=raw.stat().st_size,
        sha256=audit.sha(raw),expected_original_rows=100)
    params={'protocol/revision-20261022/selection-freeze.json':{'cells':[
        dict(source='fx_hourly',horizon=h,window=2880,family='QR',status='SELECTED',
            parameter=audit.method_spec(d,'QR33')['penalty_by_horizon'][str(h)]) for h in (2,6)]}}
    for h in (2,6):params[f'results/revision-20261023/parsimonious/fx_hourly-h{h}-w2880.json']=dict(status='COMPLETE',selected_penalty=.01)
    hashes={}
    for name,value in params.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value));hashes[name]=audit.sha(p)
    d['forecasting']={'parameter_source_sha256':hashes}
    protocol=root/'protocol/revision-v8';protocol.mkdir(parents=True)
    protocolfile=protocol/'wp5-fixed-prefix-design.json';protocolfile.write_text(json.dumps(d))
    env=dict(os.environ,GIT_AUTHOR_NAME='Unit Test',GIT_AUTHOR_EMAIL='test@example.invalid',GIT_COMMITTER_NAME='Unit Test',GIT_COMMITTER_EMAIL='test@example.invalid')
    for cmd in (['git','init','-q'],['git','add','protocol','results'],['git','commit','-q','-m','fixture design']):
        subprocess.run(cmd,cwd=root,env=env,check=True,capture_output=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    notes=root/'notes/revision-v8';notes.mkdir(parents=True)
    oldpath=root/'results/retro.json'
    oldpath.write_text(json.dumps({'groups':[dict(group=dict(phase='retro',source='fx_hourly',horizon=6,window=20),
        selections={'R3':dict(status='SELECTED',candidates=[dict(status='COMPLETE',n=4) for _ in range(6)])},
        rows=[dict(report='R3',status='COMPLETE')],r3_fold_bounds=[[50,53]])]}))
    (notes/'wp5-prior-exposure-proof.json').write_text(json.dumps(dict(status='PASS',source='results/retro.json',source_sha256=audit.sha(oldpath),
        R3_selection_status='SELECTED',R3_complete_candidate_count=6,R3_candidate_scored_issue_count=4,
        old_H24_target_coverage_merged=[[50,80]],new_H24_target_bounds=[50,80],nested_old_retro_issue_count=15,
        fresh_unscored_third_period=False,mismatch='MISMATCH-WP5-01')))
    x,t=audit.read_pinned_csv(raw,d['input']);metadata=audit.source_metadata_oracle(x,t,d)
    source_identity=dict(accepted_csv_sha256=d['input']['sha256'],accepted_csv_bytes=d['input']['bytes'],source_verified=True)
    consistency=dict(source_identity=source_identity,source_metadata=metadata)
    manifest=dict(design=d,design_commit=commit,started_utc=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=10)).isoformat(),
        private_directory=str(private),code_hashes={},protocol_hashes={'protocol/revision-v8/wp5-fixed-prefix-design.json':audit.sha(protocolfile)})
    rows=[];traces={};ids=np.arange(50,75,dtype=np.int64)
    def dump(path,value):path.write_text(json.dumps(value))
    for h in (2,6):
        for spec in d['methods']:
            method=spec['name'];unit=f'H{h}_{method}';pub=formal/'units'/unit;pub.mkdir();priv=private/unit;priv.mkdir()
            cap=x[ids]+h+(spec['engine']!='F');score=audit.score_oracle(x,ids,cap,h)
            trace=dict(origins=ids,refit_indices=50+spec['refit_step']*((ids-50)//spec['refit_step']),capacity=cap,
                **{k:score[k] for k in ('peak','floor','pinball','strict_breach')})
            np.savez(priv/'evaluation.npz',**trace);traces[(h,method)]=trace
            trace_identity=dict(trace_sha256=audit.sha(priv/'evaluation.npz'),trace_origin_count=len(ids));dump(pub/'trace.json',trace_identity)
            fits=[]
            for refit in range(50,75,spec['refit_step']):
                fit=dict(refit_index=refit,training_first_origin=refit-h-spec['window']+1,training_last_origin=refit-h,
                    training_count=spec['window'],latest_label_end=refit)
                if spec['engine']!='F':fit.update(duality_gap=0.,gap_tolerance=1e-6,primal_residual=0.,primal_tolerance=1e-6,
                    dual_residual=0.,dual_tolerance=1e-6,iterations=1)
                fits.append(fit)
            maturity=dict(refit_count=len(fits),training_first_origin_min=fits[0]['training_first_origin'],
                training_last_origin_max=fits[-1]['training_last_origin'],latest_label_end_max=fits[-1]['latest_label_end'],maximum_label_end_minus_refit=0)
            row=dict(unit_id=unit,horizon=h,method=method,engine=spec['engine'],window=spec['window'],refit_step=spec['refit_step'],
                selected_penalty=None if spec['engine']=='F' else spec['penalty_by_horizon'][str(h)],status='COMPLETE',reason=None,
                evaluation={**{k:score[k] for k in ('n','mean_loss','strict_breach_count','strict_breach_rate')},**trace_identity},fit_diagnostics=fits,maturity=maturity)
            rows.append(row);dump(pub/'report.json',row);dump(pub/'worker-source.json',consistency)
            dump(pub/'parent-start.json',{'started_utc':'2020-01-01T00:00:00Z'})
            dump(pub/'parent-termination.json',{'ended_utc':'2020-01-01T00:00:01Z','status':'COMPLETE','returncode':0})
            dump(pub/'worker-receipt.json',dict(status='COMPLETE',code_hash_start='PASS',code_hash_end='PASS',technical_error=False,
                resources=dict(peak_rss_bytes=1000,maximum_observed_os_threads=1,thread_snapshot_count=2)))
    contrasts=[]
    for h in (2,6):
        for method in ('QR33','QR4'):
            for reference in ('F_matched','F_rolling720'):
                contrasts.append(dict(horizon=h,method=method,reference=reference,**audit.contrast_oracle(traces[(h,method)],traces[(h,reference)],h)))
    dump(formal/'manifest.json',manifest);dump(formal/'inventory.json',rows)
    summary=dict(methods=rows,contrasts=contrasts,study_status='COMPLETE',source_consistency=consistency,
        source_inventory_sha256=audit.sha(formal/'inventory.json'),normal_DM_only=True,post_result=True,exploratory=True)
    dump(formal/'summary.json',summary)
    dump(formal/'study-termination.json',dict(all_workers_terminated=True,status='COMPLETE',source_consistency=consistency,
        attempted_workers=8,completed_workers=8,method_status_counts={'COMPLETE':8},elapsed_seconds=8.,code_hash_check='PASS'))
    for filename,table in [('summary.csv',rows),('contrasts.csv',contrasts)]:
        fields=list(dict.fromkeys(k for row in table for k in row))
        with (formal/filename).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
            for row in table:writer.writerow({k:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else 'NA' if v is None else v for k,v in row.items()})
    result=audit.audit_bundle(root,formal)
    assert result['status']=='PASS',result['differences']
    assert result['difference_count']==0 and result['complete_trace_scores_checked']==8 and result['normal_DM_comparisons_checked']==8
    assert result['known_exposure']['fresh_independent_third_period'] is False
    assert '"position":' not in json.dumps(result) and '"capacity":' not in json.dumps(result)
    summary['contrasts'][0]['dm']['bandwidth']+=1;dump(formal/'summary.json',summary)
    bad=audit.audit_bundle(root,formal)
    assert bad['status']=='FAIL'
    assert any(e['code']=='CONTRAST_OR_DM_MISMATCH' and e.get('field')=='dm' for e in bad['differences'])


@pytest.mark.parametrize('change',[
    ('worker-receipt.json',None),('parent-termination.json',None),
    ('worker-receipt.json',{'status':'FAILED'}),
    ('worker-receipt.json',{'code_hash_start':'FAILED'}),
    ('worker-receipt.json',{'code_hash_end':'FAILED'}),
    ('parent-termination.json',{'status':'FAILED'}),
    ('parent-termination.json',{'returncode':1}),
])
def test_complete_trace_requires_both_final_worker_and_successful_parent(tmp_path,change):
    public=tmp_path/'unit';public.mkdir()
    values={'worker-receipt.json':dict(status='COMPLETE',code_hash_start='PASS',code_hash_end='PASS'),
        'parent-termination.json':dict(status='COMPLETE',returncode=0)}
    for name,value in values.items():(public/name).write_text(json.dumps(value))
    assert audit.completion_errors(public)==[]
    name,changed=change
    corrupt=tmp_path/'corrupt';corrupt.mkdir()
    for filename,value in values.items():
        if filename==name and changed is None:continue
        payload=dict(value,**changed) if filename==name else value
        (corrupt/filename).write_text(json.dumps(payload))
    errors=audit.completion_errors(corrupt)
    assert errors and all(e['code'] in {'COMPLETE_WORKER_RECEIPT_UNVERIFIED','COMPLETE_PARENT_RECEIPT_UNVERIFIED'} for e in errors)


def test_csv_readback_accepts_complete_large_diagnostic_field_and_restores_limit(tmp_path):
    import csv
    path=tmp_path/'large-diagnostic.csv'
    rows=[dict(method='F_rolling720',fit_diagnostics=[dict(refit_index=i,note='constructed-fixture') for i in range(6000)])]
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['method','fit_diagnostics']);writer.writeheader()
        writer.writerow(dict(method='F_rolling720',fit_diagnostics=json.dumps(rows[0]['fit_diagnostics'],sort_keys=True)))
    assert len(json.dumps(rows[0]['fit_diagnostics'],sort_keys=True))>131072
    before=path.read_bytes();limit=csv.field_size_limit()
    assert audit.csv_errors(path,rows)==[]
    assert path.read_bytes()==before and csv.field_size_limit()==limit


def test_csv_readback_enforces_explicit_field_bound_and_restores_limit(tmp_path,monkeypatch):
    import csv
    path=tmp_path/'oversize.csv';path.write_text('x\n'+('z'*1025)+'\n')
    monkeypatch.setattr(audit,'CSV_MAX_FIELD_BYTES',1024)
    before=path.read_bytes();limit=csv.field_size_limit()
    errors=audit.csv_errors(path,[dict(x='z'*1025)])
    assert errors and errors[0]['code']=='CSV_FIELD_PARSE_ERROR'
    assert path.read_bytes()==before and csv.field_size_limit()==limit


def test_csv_field_bound_is_utf8_bytes_not_only_character_count(tmp_path,monkeypatch):
    import csv
    path=tmp_path/'multibyte.csv';path.write_text('x\n'+('数'*400)+'\n')
    monkeypatch.setattr(audit,'CSV_MAX_FIELD_BYTES',1024)
    limit=csv.field_size_limit()
    errors=audit.csv_errors(path,[dict(x='数'*400)])
    assert errors and errors[0]['code']=='CSV_FIELD_BYTES_EXCEEDED'
    assert csv.field_size_limit()==limit
