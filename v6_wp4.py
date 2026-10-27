"""WP4 state/conditional-moment diagnostics of the unchanged original primaries."""
import csv,json,math,signal
from pathlib import Path
import numpy as np
import study_core as core
from conditional_study import score_predictions,summarize_scores


def admit_primary(qr,reference,archived_row):
    for key in ('origins','peak','floor'):
        if not np.array_equal(qr[key],reference[key]):raise ValueError('PRIMARY_'+key.upper()+'_IDENTITY')
    ids=qr['origins'];a=score_predictions(qr['peak'],qr['capacity'],qr['floor'],ids);b=score_predictions(reference['peak'],reference['capacity'],reference['floor'],ids)
    qa,rb=summarize_scores(a),summarize_scores(b);d=a.pinball-b.pinball
    integers={'origin_count':len(ids),'first_source_index':int(ids[0]),'last_source_index':int(ids[-1])}
    reals={'mean_pinball_left':qa['mean_pinball'],'mean_pinball_right':rb['mean_pinball'],'mean_pinball_difference':core.stable_mean(d)}
    if any(int(archived_row[k])!=v for k,v in integers.items()) or any(float(archived_row[k])!=v for k,v in reals.items()):raise ValueError('IMMUTABLE_PRIMARY_PAIRED_ROW_IDENTITY')
    return d


def merge_analysis(base,analysis):
    if any(key in base and base[key]!=value for key,value in analysis.items()):raise ValueError('STATE_ANALYSIS_METADATA_IDENTITY')
    result=dict(base);result.update(analysis);return result


def main():
    from conditional_features import build_features,completed_training_indices,response_scale
    import v6_worker as w
    import v6_inference as inf
    from v6_states import analyze_states
    freeze_path=w.ROOT/'protocol/revision-v6/wp4-executable-freeze.json';freeze=w.read_json(freeze_path)
    for p,digest in freeze['files'].items():
        if w.sha(w.ROOT/p)!=digest:raise ValueError('WP4_EXECUTABLE_CHANGED:'+p)
    w.check_execution_freeze()
    paired_path=w.ROOT/'results/revision-20261022/paired-comparisons.csv'
    with paired_path.open(newline='') as f:paired=list(csv.DictReader(f))
    result_rows=[];slots=[]
    for source,window,refmethod,refwindow in (('fx_hourly',2880,'rolling_F',720),('nyfed_weekly',260,'frozen_F',260)):
        contrast=f'{source}-h6-QR{window}-minus-{refmethod}{refwindow}'
        guard=w.Guard()
        try:
            signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(RuntimeError('RESOURCE_HARD_WALL')))
            signal.alarm(600);guard()
            s,cfg,config,_=w.setup(source,6,window)
            qr=w.original_trace(source,6,window,'evaluation','QR',position=s.position)
            ref=w.original_trace(source,6,refwindow,'references',refmethod,position=s.position)
            matches=[r for r in paired if r['contrast_id']==contrast]
            if len(matches)!=1:raise ValueError('ORIGINAL_PRIMARY_ROW_MISSING')
            d=admit_primary(qr,ref,matches[0]);ids=qr['origins'];first=int(ids[0])
            features=build_features(s.position,s.dates,short_scale=config.short_scale,long_scale=config.long_scale,nominal_gap_seconds=config.nominal_gap_seconds)
            pool=completed_training_indices(first,6,window,minimum_feature_index=features.valid_from)
            cache=core.build_label_cache(s.position,6);a0=response_scale(cache.headroom[pool],s.position[pool])
            entry=w.trace_entry(source,6,window,'evaluation','QR');manifest=w.read_json(w.ROOT/entry['manifest_path'])
            firstfit=manifest['result']['fit_diagnostics'][0]
            if firstfit['response_scale']!=a0:raise ValueError('INITIAL_TRAINING_RESPONSE_SCALE_IDENTITY')
            public,private=analyze_states(features.short_rms,d,ids,pool,horizon=6,response_scale=a0,return_private=True)
            guard()
            proof=w.save_private(w.PRIVATE/(f'wp4-{source}.npz'),origins=ids,loss_difference=d,training_indices=pool,**private)
            row=dict(source=source,horizon=6,window=window,reference_method=refmethod,reference_window=refwindow,native_unit=cfg['native_unit'],
                contrast_id=contrast,analysis_status='post-result / exploratory',unchanged_primary_mean_difference=core.stable_mean(d),
                raw_source_sha256=s.sha256,qr_trace_sha256=qr['trace_sha256'],reference_trace_sha256=ref['trace_sha256'],private_artifact=proof,
                source_clock='Observed source-record order; Treasury downloaded-vintage economic-date replay, not public-release availability',
                state_definition='Issue-known position-increment RMS, not price or yield volatility')
            row=merge_analysis(row,public)
            guard()
        except RuntimeError as exc:
            if not str(exc).startswith('RESOURCE_'):raise
            public={name:dict(status='NA_RESOURCE',p=None,stat=None) for name in ('gw','heterogeneity')}
            row=dict(source=source,horizon=6,window=window,reference_method=refmethod,reference_window=refwindow,contrast_id=contrast,
                analysis_status='post-result / exploratory',status='NA',reason=str(exc),**public)
        finally:signal.alarm(0)
        row['resources']=guard.summary()
        row['resources']['rss_scope']='Process-lifetime high-water; both serial source diagnostics share a process, so later source RSS is conservative and can inherit a prior breach.'
        result_rows.append(row)
        for name,field in (('joint_GW','gw'),('group_heterogeneity','heterogeneity')):
            x=public[field];slots.append(dict(slot_id=contrast+':'+name,source=source,test=name,status=x['status'],raw_p=x.get('p'),stat=x.get('stat')))
    if [r['slot_id'] for r in slots]!=freeze['contrast_slots']:raise ValueError('FOUR_FIXED_SLOT_IDENTITY')
    adjusted=inf.fixed_slot_holm([r['slot_id'] for r in slots],{r['slot_id']:r['raw_p'] for r in slots})
    for r,a in zip(slots,adjusted['slots']):r.update(bookkeeping_p=a['bookkeeping_p'],holm_p=a['holm_p'],holm_component_status=a['status'])
    report=dict(status='COMPLETE_INVENTORY',analysis_status='post-result / exploratory',rows=result_rows,ranking=slots,family_n=4,raw_na_count=adjusted['raw_na_count'],resources=dict(source_worker_count=len(result_rows),peak_rss_bytes=max(r['resources']['peak_rss_bytes'] for r in result_rows),maximum_observed_os_threads=max(r['resources']['maximum_observed_os_threads'] for r in result_rows),maximum_source_worker_seconds=max(r['resources']['elapsed_seconds'] for r in result_rows)),
        execution_freeze_sha256=w.sha(freeze_path),paired_archive_sha256=w.sha(paired_path),
        limitation='Finite-instrument GW-style and group-mean HAC working references; unverified dependence/moment/covariance assumptions. Joint rejection may be only an unconditional mean advantage. No switching policy or causal state effect.')
    w.write_json_new(w.PUBLIC/'wp4-states.json',report)
    print(json.dumps(dict(status=report['status'],sources=len(result_rows),family_n=4,raw_na_count=adjusted['raw_na_count'],resources=report['resources'])))
if __name__=='__main__':main()
