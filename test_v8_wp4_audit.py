"""Independent WP4 readback fixtures; no source data, forecasts or refits."""
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

SPEC=importlib.util.spec_from_file_location('wp4_audit',Path(__file__).parent/'notes/revision-v8/audit_wp4.py')
audit=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(audit)


def spec():
    return dict(windows=[52,260],methods=['F','QR33','QR4'],
        clock_and_target={'horizons':[6,24]},
        sample=dict(validation_first=329,validation_last=380,evaluation_first=405),
        features={'valid_from':26},forecasting={'refit_step':13},
        menus={'QR33':[.001,.01,.1],'QR4':[.001,.01,.1,1.,10.]})


def rows(losses=(1.,2.,2.)):
    return [dict(window=w,horizon=h,method=method,status='COMPLETE',reason=None,
        evaluation=dict(mean_loss=loss,n=10,strict_breach_count=1,strict_breach_rate=.1),
        selected_penalty=None,candidates=[])
        for w in (52,260) for h in (6,24) for method,loss in zip(('F','QR33','QR4'),losses)]


def test_daily_rule_keeps_last_nonempty_day_and_uses_ended_day_clock():
    t=np.array(['2014-01-02T01:00','2014-01-02T03:00','2014-01-05T23:00'],dtype='datetime64[us]')
    out=audit.daily_oracle(np.array([1.,7.,-3.]),t)
    assert out['selected_indices'].tolist()==[1,2]
    assert out['position'].tolist()==[7.,-3.]
    assert out['times'].astype(str).tolist()==['2014-01-02T23:59:59.999999','2014-01-05T23:59:59.999999']
    assert out['metadata']['daily_gap_seconds_histogram']=={'259200':1}
    assert out['metadata']['n_discarded_original']==1


def test_daily_fingerprints_use_fixed_little_endian_vectors_and_prefix():
    t=np.array(['2014-01-02T01:00','2014-01-02T03:00','2014-01-05T23:00'],dtype='datetime64[us]')
    out=audit.daily_oracle(np.array([1.,7.,-3.],dtype='>f8'),t)
    arrays=(np.array([1,2],dtype='<i8').tobytes(),t[[1,2]].view('i8').astype('<i8').tobytes(),
        np.array(['2014-01-02T23:59:59.999999','2014-01-05T23:59:59.999999'],dtype='datetime64[us]').view('i8').astype('<i8').tobytes(),
        np.array([7.,-3.],dtype='<f8').tobytes())
    assert out['metadata']['fingerprints']['combined_sha256']==hashlib.sha256(b'v8-daily-v1\0'+b''.join(arrays)).hexdigest()


def test_nonincreasing_or_nonfinite_source_is_rejected_without_sorting():
    times=np.array(['2014-01-02','2014-01-01'],dtype='datetime64[us]')
    with pytest.raises(ValueError):audit.daily_oracle(np.array([1.,2.]),times)
    with pytest.raises(ValueError):audit.daily_oracle(np.array([1.,float('nan')]),np.sort(times))


def test_grid_uses_full52_validation_and_common_n_minus25_tail():
    grid=audit.geometry_oracle(780,24,260,spec())
    assert grid['validation_count']==52
    assert grid['evaluation_first']==405 and grid['evaluation_last']==755 and grid['evaluation_count']==351
    assert grid['earliest_training_origin']==46 and grid['status']=='READY'
    assert audit.geometry_oracle(429,6,52,spec())['status']=='NA_SAMPLE_SIZE'


def test_target_includes_current_and_strict_ties_are_not_breaches():
    x=np.array([9.,2.,-3.,1.,4.])
    actual=audit.score_oracle(x,np.array([0,1]),np.array([9.,2.]),2)
    assert actual['peak'].tolist()==[9.,3.]
    assert actual['strict_breach'].tolist()==[False,True]
    assert actual['pinball'].tolist()==[0.,.95]
    assert actual['mean_loss']==.475 and actual['strict_breach_count']==1


def test_floor_and_incomplete_target_are_rejected():
    with pytest.raises(ValueError):audit.score_oracle(np.array([9.,2.,3.]),np.array([0]),np.array([8.]),2)
    with pytest.raises(ValueError):audit.score_oracle(np.array([9.,2.,3.]),np.array([1]),np.array([9.]),2)


def test_scalar_score_mean_preserves_exact_constant_as_declared_in_original():
    score=audit.score_oracle(np.zeros(5),np.arange(3),np.full(3,2.),1)
    assert score['mean_loss']==.1


def test_f_replay_uses_own_anchor_headroom_corrected_rank_and_frozen13_block():
    x=np.array([0.,1.,2.,8.,0.,3.,4.,0.,7.,1.,5.,2.])
    # Refit6 pool2..4: headrooms [6,0,4], corrected rank ceil(.95*4)=4 unavailable.
    with pytest.raises(ValueError):audit.f_oracle(x,np.array([6,7,8]),2,3,2,6)


def test_f_replay_with_valid_corrected_rank_and_mature_pool():
    x=np.arange(80,dtype=float)
    ids=np.arange(50,55,dtype=np.int64)
    result=audit.f_oracle(x,ids,6,20,13,50)
    # All mature headrooms equal6 under increasing positive positions.
    assert result['capacity'].tolist()==[56.,57.,58.,59.,60.]
    assert result['refit_indices'].tolist()==[50]*5
    assert result['maximum_label_end_minus_refit']==0


def test_private_trace_must_keep_every_declared_issue_and_exact_refit_grid():
    d=spec();x=np.arange(500,dtype=float);ids=np.arange(329,381,dtype=np.int64)
    s=audit.score_oracle(x,ids,x[ids]+6,6)
    trace=dict(origins=ids,capacity=x[ids]+6,peak=s['peak'],floor=s['floor'],pinball=s['pinball'],
        strict_breach=s['strict_breach'],refit_indices=329+13*((ids-329)//13))
    assert audit.trace_errors(x,trace,6,52,ids,329,'F',d)==[]
    shorter={k:v[:-1] for k,v in trace.items()}
    assert any(e['code']=='TRACE_ISSUE_GRID_MISMATCH' for e in audit.trace_errors(x,shorter,6,52,ids,329,'F',d))
    trace['refit_indices']=trace['refit_indices']+1
    assert any(e['code']=='TRACE_REFIT_GRID_MISMATCH' for e in audit.trace_errors(x,trace,6,52,ids,329,'F',d))


def test_classification_is_per_regression_and_preserves_other_models_failures():
    data=rows();next(r for r in data if r['method']=='QR33')['status']='FAILED'
    assert audit.classification_oracle(data,'QR33',spec())['status']=='INCONCLUSIVE'
    q4=audit.classification_oracle(data,'QR4',spec())
    assert q4['status']=='TREASURY_LIKE' and q4['historical_wins']==4


def test_three_of_four_gain_and_exact_ties_have_declared_labels():
    data=rows((2.,1.,2.))
    assert audit.classification_oracle(data,'QR33',spec())['status']=='CONDITIONAL_GAINS_PERSIST'
    q4=audit.classification_oracle(data,'QR4',spec())
    assert q4['status']=='MIXED' and q4['ties']==4
    assert len(audit.classification_oracle(data,'QR33',spec())['literal_hourly_counterexamples'])==4


def test_pinned_csv_identity_and_chronology_are_independently_checked(tmp_path):
    content=b'datetime,NetPosUsd,NetUsdPnL,AbsVolume,Mid\n2014.01.02T01:00:00.000000,1,0,0,0\n2014.01.02T02:00:00.000000,-2,0,0,0\n'
    path=tmp_path/'fixture.csv';path.write_bytes(content)
    source=dict(bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),expected_original_rows=2)
    x,t=audit.read_pinned_csv(path,source)
    assert x.tolist()==[1.,-2.] and len(t)==2
    bad=dict(source,sha256='0'*64)
    with pytest.raises(ValueError,match='SOURCE_IDENTITY'):audit.read_pinned_csv(path,bad)


def test_full_constructed_bundle_schema_and_private_readback(tmp_path):
    """Monotone scalar fixture, not a simulated financial path or QR fit."""
    import csv,datetime as dt,os,subprocess
    root=tmp_path/'repo';root.mkdir();formal=root/'results/revision-v8/wp4';formal.mkdir(parents=True)
    (formal/'cells').mkdir();private=root/'.scratch/revision-v8/wp4/fixture';private.mkdir(parents=True)
    raw=root/'.scratch/data/fake.csv';raw.parent.mkdir()
    with raw.open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(audit.HEADER)
        for i in range(500):writer.writerow([(dt.datetime(2014,1,1,6)+dt.timedelta(days=i)).strftime('%Y.%m.%dT%H:%M:%S.%f'),i,0,0,0])
    d=spec();d.update(input=dict(local_private_path='.scratch/data/fake.csv',bytes=raw.stat().st_size,
        sha256=audit.sha(raw),expected_original_rows=500),solver={'max_iter':10000},
        original_and_sealed_modules_sha256={},resources=dict(maximum_rss_bytes=2**31,
        maximum_observed_os_threads=2,worker_hard_seconds=600,global_wall_seconds=1800))
    protocol=root/'protocol/revision-v8';protocol.mkdir(parents=True)
    designfile=protocol/'wp4-daily-fx-design.json';designfile.write_text(json.dumps(d))
    env=dict(os.environ,GIT_AUTHOR_NAME='Unit Test',GIT_AUTHOR_EMAIL='test@example.invalid',GIT_COMMITTER_NAME='Unit Test',GIT_COMMITTER_EMAIL='test@example.invalid')
    for cmd in (['git','init','-q'],['git','add','protocol'],['git','commit','-q','-m','fixture design']):subprocess.run(cmd,cwd=root,env=env,check=True,capture_output=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    begun=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=10)).isoformat()
    manifest=dict(design=d,design_commit=commit,started_utc=begun,private_directory=str(private),
        code_hashes={},protocol_hashes={'protocol/revision-v8/wp4-daily-fx-design.json':audit.sha(designfile)})
    x,t=audit.read_pinned_csv(raw,d['input']);daily=audit.daily_oracle(x,t)
    source=dict(accepted_csv_sha256=d['input']['sha256'],accepted_csv_bytes=d['input']['bytes'],source_verified=True)
    out=[]
    for w in d['windows']:
        for h in d['clock_and_target']['horizons']:
            cell=f'W{w}_H{h}';pub=formal/'cells'/cell;pub.mkdir();priv=private/cell;priv.mkdir()
            np.savez(priv/'daily-series.npz',**{k:daily[k] for k in audit.DAILY_KEYS})
            (pub/'worker-source.json').write_text(json.dumps(dict(source_identity=source,daily_metadata=daily['metadata'],daily_mapping_sha256=audit.sha(priv/'daily-series.npz'))))
            geo=audit.geometry_oracle(500,h,w,d);(pub/'cell-geometry.json').write_text(json.dumps(geo))
            (pub/'parent-start.json').write_text('{"started_utc":"2020-01-01T00:00:00Z"}')
            (pub/'parent-termination.json').write_text('{"ended_utc":"2020-01-01T00:00:01Z","status":"COMPLETE"}')
            (pub/'worker-receipt.json').write_text(json.dumps(dict(code_hash_start='PASS',code_hash_end='PASS',technical_error=False,
                resources=dict(peak_rss_bytes=1000,maximum_observed_os_threads=1,thread_snapshot_count=2))))
            ids=np.arange(405,476,dtype=np.int64);refit=405+13*((ids-405)//13)
            # For daily position i, every mature historical headroom and target excess is H.
            cap=ids.astype(float)+h
            arrays=dict(origins=ids,refit_indices=refit,capacity=cap,peak=cap,floor=ids.astype(float),pinball=np.zeros(len(ids)),strict_breach=np.zeros(len(ids),dtype=bool))
            stem=f'{cell}_F_evaluation';np.savez(priv/(stem+'.npz'),**arrays)
            trace=dict(trace_sha256=audit.sha(priv/(stem+'.npz')),trace_origin_count=len(ids))
            (pub/(stem+'.trace.json')).write_text(json.dumps(trace))
            fit=[dict(refit_index=int(r),training_first_origin=int(r)-h-w+1,training_last_origin=int(r)-h,training_count=w,latest_label_end=int(r)) for r in np.unique(refit)]
            maturity=dict(refit_count=len(fit),training_first_origin_min=405-h-w+1,training_last_origin_max=int(refit[-1])-h,latest_label_end_max=int(refit[-1]),maximum_label_end_minus_refit=0)
            for method in d['methods']:
                row=dict(cell_id=cell,window=w,horizon=h,method=method,status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',
                    geometry=geo,selected_penalty=None,evaluation=None,fit_diagnostics=[],maturity=None,
                    candidates=[dict(penalty=p,status='NOT_ATTEMPTED',reason='METHOD_NOT_REACHED',origin_count=0,mean_loss=None) for p in d['menus'].get(method,[])])
                if method=='F':row.update(status='COMPLETE',reason=None,evaluation=dict(mean_loss=0.,n=len(ids),strict_breach_count=0,strict_breach_rate=0.,**trace),fit_diagnostics=fit,maturity=maturity)
                out.append(row)
    consistency=dict(source_identity=source,daily_metadata=daily['metadata'])
    (formal/'manifest.json').write_text(json.dumps(manifest));(formal/'inventory.json').write_text(json.dumps(out))
    (formal/'study-termination.json').write_text(json.dumps(dict(all_workers_terminated=True,status='BUDGET_STOP',
        source_consistency=consistency,attempted_workers=4,completed_workers=4,method_status_counts={'COMPLETE':4,'NOT_ATTEMPTED':8},elapsed_seconds=4.,code_hash_check='PASS')))
    classifications={m:audit.classification_oracle(out,m,d) for m in ('QR33','QR4')};contrasts=audit.contrasts_oracle(out,d)
    summary=dict(cells=out,contrasts=contrasts,classifications=classifications,study_status='BUDGET_STOP',source_consistency=consistency,source_inventory_sha256=audit.sha(formal/'inventory.json'))
    (formal/'summary.json').write_text(json.dumps(summary));(formal/'classification.json').write_text(json.dumps(classifications))
    for name,rs in [('summary.csv',out),('contrasts.csv',contrasts)]:
        fields=list(dict.fromkeys(k for r in rs for k in r))
        with (formal/name).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
            for r in rs:writer.writerow({k:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else 'NA' if v is None else v for k,v in r.items()})
    result=audit.audit_bundle(root,formal)
    assert result['difference_count']==0,result['differences']
    assert result['status']=='PASS' and result['actual_method_slots']==12 and result['actual_candidate_slots']==32
    assert result['complete_trace_scores_checked']==4
    assert result['classifications']['QR4']['status']=='INCONCLUSIVE'
    assert '"position":' not in json.dumps(result) and '"selected_indices":' not in json.dumps(result)
    csv_path=formal/'summary.csv';csv_path.write_text(csv_path.read_text().replace('COMPLETE','ALTERED',1))
    result=audit.audit_bundle(root,formal)
    assert any(e['code']=='CSV_VALUES_MISMATCH' for e in result['differences'])


def test_distinct_validation_failure_and_tie_policies_are_read_back():
    d=spec();data=rows()
    q33=next(r for r in data if r['method']=='QR33');q4=next(r for r in data if r['method']=='QR4')
    for row in (q33,q4):
        row['selected_penalty']=.001
        row['candidates']=[dict(penalty=p,status='COMPLETE',origin_count=52,mean_loss=1.) for p in d['menus'][row['method']]]
    assert any(e['code']=='SELECTED_PENALTY_MISMATCH' for e in audit.selection_errors(q33,d))
    assert audit.selection_errors(q4,d)==[]
    q33['candidates'][0].update(status='FAILED',origin_count=0,mean_loss=None)
    q33.update(status='FAILED',selected_penalty=None)
    assert audit.selection_errors(q33,d)==[]
    q4['candidates'][0].update(status='FAILED',origin_count=0,mean_loss=None)
    q4['selected_penalty']=.01
    assert audit.selection_errors(q4,d)==[]


def test_maturity_cannot_be_relabelled_by_a_pass_summary():
    d=spec();ids=np.arange(329,381,dtype=np.int64)
    refits=np.array([329,342,355,368]);h=24;w=260
    fits=[dict(refit_index=int(r),training_first_origin=int(r)-h-w+1,training_last_origin=int(r)-h,training_count=w,latest_label_end=int(r)) for r in refits]
    summary=dict(refit_count=4,training_first_origin_min=46,training_last_origin_max=344,latest_label_end_max=368,maximum_label_end_minus_refit=0)
    report=dict(fit_diagnostics=fits,maturity=summary)
    assert audit.fit_diagnostic_errors(report,h,w,ids,329,d)==[]
    fits[0]['latest_label_end']=330
    assert any(e['code']=='IMMATURE_TRAINING_LABEL' for e in audit.fit_diagnostic_errors(report,h,w,ids,329,d))


def test_audit_entry_refuses_live_study_before_source_or_private_reads(tmp_path):
    with pytest.raises(ValueError,match='STUDY_NOT_TERMINATED'):
        audit.audit_bundle(tmp_path,tmp_path/'no-formal-run')


def test_audit_does_not_import_production_forecasting_or_scoring_code():
    import subprocess,sys
    code="import importlib.util,sys;s=importlib.util.spec_from_file_location('a',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);assert not any(k in sys.modules for k in ('v8_daily_fx','run_v8_wp4','v8_mechanism_mc','conditional_study','study_data','study_core'))"
    r=subprocess.run([sys.executable,'-B','-c',code,str(Path(__file__).parent/'notes/revision-v8/audit_wp4.py')],capture_output=True,text=True)
    assert r.returncode==0,r.stderr
