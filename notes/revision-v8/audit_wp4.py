"""Independent WP4 arithmetic/provenance readback, never fitting a QR.

Only NumPy and the standard library are used. The source CSV and private NPZ
arrays may be read only by the terminated-study audit entry point. No source
values, daily mapping vectors or per-issue trajectories are written publicly.
This is saved-result readback, not independent dealer or prospective validation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import stat
import subprocess
import sys

import numpy as np

TRACE_KEYS={'origins','refit_indices','capacity','peak','floor','pinball','strict_breach'}
DAILY_KEYS={'position','times','selected_indices','selected_raw_times'}
HEADER=['datetime','NetPosUsd','NetUsdPnL','AbsVolume','Mid']
TERMINATION_TOLERANCE_SECONDS=5.


def finite(x):return type(x) in (int,float) and math.isfinite(x)


def no_symlinks(path):
    path=Path(path).absolute()
    if any(p.is_symlink() for p in (path,*path.parents)):raise ValueError('SYMLINK_REFUSED')


def sha(path):
    no_symlinks(path);digest=hashlib.sha256()
    with open(path,'rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def problem(code,**detail):return dict(code=code,**detail)


def same(a,b):
    if a is None or b is None:return a is b
    if type(a) is bool or type(b) is bool:return type(a) is type(b) and a==b
    if type(a) in (int,float) and type(b) in (int,float):
        return finite(a) and finite(b) and math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-10)
    if isinstance(a,dict) and isinstance(b,dict):return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return type(a) is type(b) and a==b


def load_json(path):
    no_symlinks(path)
    def reject(v):raise ValueError('NONFINITE_JSON')
    with open(path,encoding='utf-8') as stream:return json.load(stream,parse_constant=reject)


def csv_errors(path,rows):
    """Check the saved CSV serialization, without rewriting numeric tokens."""
    no_symlinks(path)
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with open(path,newline='',encoding='utf-8') as stream:
        reader=csv.DictReader(stream);actual=list(reader)
        if reader.fieldnames!=fields:return [problem('CSV_HEADER_MISMATCH',file=Path(path).name)]
    def token(value):
        return json.dumps(value,sort_keys=True) if isinstance(value,(dict,list)) else 'NA' if value is None else str(value)
    expected=[{k:token(row[k]) if k in row else '' for k in fields} for row in rows]
    if actual!=expected:return [problem('CSV_VALUES_MISMATCH',file=Path(path).name)]
    return []


def read_pinned_csv(path,source):
    """Independently pin bytes and parse the declared naive source clock."""
    no_symlinks(path)
    expected=source['bytes']
    if type(expected) is not int or not 0<expected<=100*1024*1024:raise ValueError('SOURCE_CONFIGURATION')
    fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
    try:
        before=os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size!=expected:raise ValueError('SOURCE_IDENTITY')
        blocks=[];remaining=expected+1
        while remaining:
            piece=os.read(fd,min(65536,remaining))
            if not piece:break
            blocks.append(piece);remaining-=len(piece)
        raw=b''.join(blocks);after=os.fstat(fd)
        if (before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_size,after.st_mtime_ns,after.st_ctime_ns):raise ValueError('SOURCE_CHANGED')
    finally:os.close(fd)
    if len(raw)!=expected or hashlib.sha256(raw).hexdigest()!=source['sha256']:raise ValueError('SOURCE_IDENTITY')
    reader=csv.reader(io.StringIO(raw.decode('utf-8'),newline=''),strict=True)
    if next(reader,None)!=HEADER:raise ValueError('SOURCE_HEADER')
    times=[];values=[];previous=None
    for row in reader:
        if len(row)!=5:raise ValueError('SOURCE_SCHEMA')
        t=datetime.strptime(row[0],'%Y.%m.%dT%H:%M:%S.%f');x=float(row[1])
        if t.tzinfo is not None or previous is not None and t<=previous:raise ValueError('SOURCE_CHRONOLOGY')
        if not math.isfinite(x):raise ValueError('SOURCE_NONFINITE')
        times.append(t);values.append(x);previous=t
    if len(times)!=source['expected_original_rows']:raise ValueError('SOURCE_ROW_COUNT')
    return np.asarray(values,dtype=np.float64),np.asarray(times,dtype='datetime64[us]')


def daily_oracle(position,times):
    x=np.asarray(position,dtype=np.float64);t=np.asarray(times).astype('datetime64[us]')
    if x.ndim!=1 or not len(x) or t.shape!=x.shape or not np.isfinite(x).all() or np.isnat(t).any() or np.any(t[1:]<=t[:-1]):raise ValueError('INVALID_SOURCE_VECTORS')
    day=t.astype('datetime64[D]')
    # Determine final rows independently with a forward dictionary overwrite.
    last={}
    for i,stamp in enumerate(day.astype('i8')):last[int(stamp)]=i
    indices=np.array(list(last.values()),dtype=np.int64)
    raw_t=t[indices];out_x=x[indices].copy()
    issue=(day[indices]+np.timedelta64(1,'D')).astype('datetime64[us]')-np.timedelta64(1,'us')
    vectors=(indices.astype('<i8').tobytes(),raw_t.view('i8').astype('<i8').tobytes(),
        issue.view('i8').astype('<i8').tobytes(),out_x.astype('<f8').tobytes())
    names=('selected_indices_sha256','selected_raw_times_sha256','issue_times_sha256','position_sha256')
    fingerprints={name:hashlib.sha256(data).hexdigest() for name,data in zip(names,vectors)}
    fingerprints['combined_sha256']=hashlib.sha256(b'v8-daily-v1\0'+b''.join(vectors)).hexdigest()
    gaps=Counter(int(v)//1_000_000 for v in np.diff(issue).astype('timedelta64[us]').astype('i8'))
    stamp=lambda a:str(np.datetime_as_string(a,unit='us'))
    metadata=dict(schema='wp4-daily-resampling-v1',n_original=len(x),n_daily=len(out_x),
        n_discarded_original=len(x)-len(out_x),source_first_timestamp=stamp(t[0]),source_last_timestamp=stamp(t[-1]),
        first_issue_time=stamp(issue[0]),last_issue_time=stamp(issue[-1]),
        daily_gap_seconds_histogram={str(k):gaps[k] for k in sorted(gaps)},fingerprints=fingerprints)
    return dict(position=out_x,times=issue,selected_indices=indices,selected_raw_times=raw_t,metadata=metadata)


def geometry_oracle(n,h,w,design):
    first=design['sample']['validation_first'];last=design['sample']['validation_last']
    start=design['sample']['evaluation_first'];finish=n-1-max(design['clock_and_target']['horizons'])
    early=first-h-w+1;valid=design['features']['valid_from']
    reason=('VALIDATION_NOT_FULLY_OBSERVED' if last+max(design['clock_and_target']['horizons'])>=n
        else 'EMPTY_EVALUATION_GRID' if finish<start else 'INSUFFICIENT_FEATURE_HISTORY' if early<valid else None)
    return dict(status='READY' if reason is None else 'NA_SAMPLE_SIZE',reason=reason,
        validation_first=first,validation_last=last,validation_count=last-first+1,
        evaluation_first=start,evaluation_last=finish,evaluation_count=max(0,finish-start+1),
        earliest_training_origin=early,feature_valid_from=valid)


def target_vector(position,horizon):
    x=np.asarray(position,dtype=np.float64)
    if x.ndim!=1 or not np.isfinite(x).all() or type(horizon) is not int or horizon<1 or len(x)<=horizon:raise ValueError('INVALID_TARGET_INPUT')
    return np.array([max(abs(float(v)) for v in x[i:i+horizon+1]) for i in range(len(x)-horizon)])


def score_oracle(position,origins,capacity,horizon):
    x=np.asarray(position,dtype=np.float64);ids=np.asarray(origins);c=np.asarray(capacity,dtype=np.float64)
    if ids.ndim!=1 or ids.dtype.kind not in 'iu' or not len(ids) or c.shape!=ids.shape or np.any(np.diff(ids)!=1) or int(ids[0])<0 or int(ids[-1])+horizon>=len(x) or not np.isfinite(c).all():raise ValueError('INVALID_TRACE_SCORE_INPUT')
    floor=np.abs(x[ids]);peak=target_vector(x,horizon)[ids]
    if np.any(c<floor):raise ValueError('FORECAST_BELOW_CURRENT_FLOOR')
    errors=peak-c;loss=.95*np.maximum(errors,0.)+.05*np.maximum(-errors,0.)
    breach=peak>c;n=len(ids)
    mean_loss=float(loss[0]) if all(v==loss[0] for v in loss) else math.fsum(float(v) for v in loss)/n
    return dict(peak=peak,floor=floor,pinball=loss,strict_breach=breach,
        mean_loss=mean_loss,n=n,
        strict_breach_count=int(breach.sum()),strict_breach_rate=int(breach.sum())/n)


def f_oracle(position,origins,horizon,window,step,segment_start):
    x=np.asarray(position,dtype=np.float64);ids=np.asarray(origins,dtype=np.int64)
    peak=target_vector(x,horizon);headroom=peak-np.abs(x[:len(peak)])
    rank=(19*(window+1)+19)//20
    if rank>window:raise ValueError('UNAVAILABLE_CORRECTED_RANK')
    capacities=[];refits=[];last=None;q=None
    for t in ids:
        r=segment_start+step*((int(t)-segment_start)//step)
        first=r-horizon-window+1;end=r-horizon
        if first<0 or end+horizon>r:raise ValueError('INVALID_MATURE_HISTORY')
        if r!=last:
            sample=sorted(float(v) for v in headroom[first:end+1])
            if len(sample)!=window:raise ValueError('INCOMPLETE_F_HISTORY')
            q=sample[rank-1];last=r
        capacities.append(abs(float(x[t]))+max(0.,q));refits.append(r)
    return dict(capacity=np.array(capacities),refit_indices=np.array(refits,dtype=np.int64),maximum_label_end_minus_refit=0)


def trace_errors(position,trace,h,w,expected_origins,segment_start,method,design):
    errors=[]
    if set(trace)!=TRACE_KEYS:return [problem('TRACE_KEYS_MISMATCH')]
    ids=np.asarray(trace['origins']);expected=np.asarray(expected_origins)
    if ids.dtype.kind not in 'iu' or not np.array_equal(ids,expected):return [problem('TRACE_ISSUE_GRID_MISMATCH',expected_count=len(expected),actual_count=int(ids.size))]
    if any(np.asarray(v).shape!=ids.shape for v in trace.values()):return [problem('TRACE_SHAPE_MISMATCH')]
    refits=segment_start+design['forecasting']['refit_step']*((ids-segment_start)//design['forecasting']['refit_step'])
    if not np.array_equal(trace['refit_indices'],refits):errors.append(problem('TRACE_REFIT_GRID_MISMATCH'))
    try:score=score_oracle(position,ids,trace['capacity'],h)
    except (ValueError,IndexError,FloatingPointError):return errors+[problem('TRACE_SCORE_INVALID')]
    for name in ('peak','floor','pinball'):
        actual=np.asarray(trace[name]);reference=score[name]
        if actual.dtype.kind not in 'iuf' or not np.isfinite(actual).all() or not np.allclose(actual,reference,rtol=1e-12,atol=1e-10):
            errors.append(problem('TRACE_VALUE_MISMATCH',field=name,mismatching_count=int(np.count_nonzero(~np.isclose(actual,reference,rtol=1e-12,atol=1e-10)))))
    if np.asarray(trace['strict_breach']).dtype.kind!='b' or not np.array_equal(trace['strict_breach'],score['strict_breach']):errors.append(problem('TRACE_STRICT_BREACH_MISMATCH'))
    if method=='F':
        replay=f_oracle(position,ids,h,w,design['forecasting']['refit_step'],segment_start)
        if not np.array_equal(trace['capacity'],replay['capacity']):errors.append(problem('F_DETERMINISTIC_REPLAY_MISMATCH'))
    return errors


def classification_oracle(rows,method,design):
    cases=[];counts=Counter();counterexamples=[]
    index={(r['window'],r['horizon'],r['method']):r for r in rows}
    for w in design['windows']:
        for h in design['clock_and_target']['horizons']:
            m=index.get((w,h,method));f=index.get((w,h,'F'))
            case=dict(window=w,horizon=h,method=method,outcome='UNAVAILABLE',
                model_status=None if m is None else m['status'],reference_status=None if f is None else f['status'],
                mean_model_loss=None,mean_F_loss=None,reason=None)
            if m is None or f is None:case['reason']='MISSING_METHOD_ROW' if m is None else 'MISSING_REFERENCE_ROW'
            elif m['status']!='COMPLETE' or f['status']!='COMPLETE':case['reason']='METHOD_OR_REFERENCE_UNAVAILABLE'
            else:
                a=m['evaluation']['mean_loss'];b=f['evaluation']['mean_loss']
                if m['evaluation']['n']!=f['evaluation']['n']:raise ValueError('PAIRED_COUNTS_DIFFER')
                label='TIE' if a==b else 'CONDITIONAL_WIN' if a<b else 'HISTORICAL_WIN'
                case.update(outcome=label,mean_model_loss=a,mean_F_loss=b)
            counts[case['outcome']]+=1;cases.append(case)
            if case['outcome']=='CONDITIONAL_WIN':counterexamples.append(dict(case))
    missing=counts['UNAVAILABLE']
    status=('INCONCLUSIVE' if missing else 'TREASURY_LIKE' if counts['HISTORICAL_WIN']>=3
        else 'CONDITIONAL_GAINS_PERSIST' if counts['CONDITIONAL_WIN']>=3 else 'MIXED')
    return dict(method=method,status=status,planned_comparisons=len(cases),complete_comparisons=len(cases)-missing,
        historical_wins=counts['HISTORICAL_WIN'],conditional_wins=counts['CONDITIONAL_WIN'],ties=counts['TIE'],
        missing_comparisons=missing,comparisons=cases,literal_hourly_counterexamples=counterexamples,descriptive_only=True)


def contrasts_oracle(rows,design):
    index={(r['window'],r['horizon'],r['method']):r for r in rows};out=[]
    for w in design['windows']:
        for h in design['clock_and_target']['horizons']:
            for method in ('QR33','QR4'):
                m=index[(w,h,method)];f=index[(w,h,'F')]
                row=dict(cell_id=f'W{w}_H{h}',window=w,horizon=h,method=method,reference_method='F',
                    status='FAILED',reason=None,model_loss=None,reference_loss=None,relative_loss_percent=None,
                    relative_loss_undefined_reason=None,n=None,model_breach_rate=None,reference_breach_rate=None)
                if m['status']!='COMPLETE':row['reason']='MODEL_'+(m.get('reason') or m['status'])
                elif f['status']!='COMPLETE':row['reason']='REFERENCE_'+(f.get('reason') or f['status'])
                elif m['evaluation']['n']!=f['evaluation']['n']:row['reason']='MISMATCHED_EVALUATION_COUNTS'
                else:
                    a=m['evaluation'];b=f['evaluation']
                    row.update(status='COMPLETE',model_loss=a['mean_loss'],reference_loss=b['mean_loss'],n=a['n'],
                        model_breach_rate=a['strict_breach_rate'],reference_breach_rate=b['strict_breach_rate'])
                    if b['mean_loss']==0:row['relative_loss_undefined_reason']='ZERO_REFERENCE_LOSS'
                    else:row['relative_loss_percent']=100*(a['mean_loss']/b['mean_loss']-1)
                out.append(row)
    return out


def selection_errors(row,design):
    method=row['method'];candidates=row.get('candidates',[])
    menu=design['menus'].get(method,[]);errors=[]
    context=dict(window=row['window'],horizon=row['horizon'],method=method)
    if [c.get('penalty') for c in candidates]!=menu:return [problem('CANDIDATE_MENU_MISMATCH',**context)]
    complete=[];n=design['sample']['validation_last']-design['sample']['validation_first']+1
    for c in candidates:
        if c.get('status') not in ('COMPLETE','FAILED','INCOMPLETE','NOT_ATTEMPTED'):
            errors.append(problem('INVALID_CANDIDATE_STATUS',**context))
        if c.get('status')=='COMPLETE':
            if c.get('origin_count')!=n or not finite(c.get('mean_loss')) or c['mean_loss']<0:
                errors.append(problem('INVALID_COMPLETE_CANDIDATE',**context,penalty=c.get('penalty')))
            else:complete.append(c)
        elif c.get('mean_loss') is not None:
            errors.append(problem('FAILED_CANDIDATE_HAS_AGGREGATE',**context,penalty=c.get('penalty')))
    if method=='F':
        if row.get('selected_penalty') is not None:errors.append(problem('REFERENCE_HAS_PENALTY',**context))
        return errors
    allowed=bool(complete) and (method=='QR4' or len(complete)==len(menu))
    choice=None
    if allowed:
        minimum=min(c['mean_loss'] for c in complete)
        ties=[c['penalty'] for c in complete if c['mean_loss']==minimum]
        choice=max(ties) if method=='QR33' else min(ties)
    selected=row.get('selected_penalty')
    if (selected is not None and selected!=choice
            or row['status']=='COMPLETE' and (not allowed or selected!=choice)):
        errors.append(problem('SELECTED_PENALTY_MISMATCH',**context))
    return errors


def fit_diagnostic_errors(report,h,w,origins,segment_start,design):
    expected_refits=np.unique(segment_start+design['forecasting']['refit_step']*((origins-segment_start)//design['forecasting']['refit_step']))
    diagnostics=report.get('fit_diagnostics',[]);errors=[]
    if len(diagnostics)!=len(expected_refits):return [problem('FIT_DIAGNOSTIC_COUNT_MISMATCH')]
    for d,r0 in zip(diagnostics,expected_refits):
        r=int(r0)
        expected=dict(refit_index=r,training_first_origin=r-h-w+1,training_last_origin=r-h,
            training_count=w,latest_label_end=r)
        for field,value in expected.items():
            if d.get(field)!=value:errors.append(problem('FIT_MATURITY_MISMATCH',field=field))
        if d.get('latest_label_end',r+1)>d.get('refit_index',r):errors.append(problem('IMMATURE_TRAINING_LABEL'))
        if expected['training_first_origin']<design['features']['valid_from']:errors.append(problem('INCOMPLETE_FEATURE_HISTORY'))
        for residual,tolerance in (('duality_gap','gap_tolerance'),('primal_residual','primal_tolerance'),('dual_residual','dual_tolerance')):
            if residual in d and (not finite(d[residual]) or not finite(d.get(tolerance)) or d[residual]>d[tolerance]):
                errors.append(problem('UNCONVERGED_REPORTED_COMPLETE_FIT',field=residual))
        if 'iterations' in d and (type(d['iterations']) is not int or not 0<=d['iterations']<=design['solver']['max_iter']):
            errors.append(problem('ITERATION_LIMIT_MISMATCH'))
    if len(expected_refits):
        maturity=dict(refit_count=len(expected_refits),training_first_origin_min=int(expected_refits[0])-h-w+1,
            training_last_origin_max=int(expected_refits[-1])-h,latest_label_end_max=int(expected_refits[-1]),
            maximum_label_end_minus_refit=0)
        if report.get('maturity')!=maturity:errors.append(problem('MATURITY_SUMMARY_MISMATCH'))
    return errors


def private_path(root,base,name):
    base=Path(base).absolute();base.resolve().relative_to((root/'.scratch').resolve())
    path=base/name;no_symlinks(path);return path


def load_npz(path,keys):
    no_symlinks(path)
    with np.load(path,allow_pickle=False) as data:
        if set(data.files)!=set(keys):raise ValueError('PRIVATE_NPZ_KEYS_MISMATCH')
        return {name:np.array(data[name],copy=True) for name in data.files}


def audit_trace(root,private,public,stem,report,x,h,w,ids,segment_start,method,design,private_hashes):
    errors=[];path=private_path(root,private,stem+'.npz');sidecar=public/(stem+'.trace.json')
    digest=sha(path);trace_record=load_json(sidecar)
    private_hashes[path]=digest
    for item in (trace_record,report):
        if item.get('trace_sha256')!=digest or item.get('trace_origin_count')!=len(ids):
            errors.append(problem('TRACE_PUBLIC_HASH_OR_COUNT_MISMATCH'))
    trace=load_npz(path,TRACE_KEYS)
    errors+=trace_errors(x,trace,h,w,ids,segment_start,method,design)
    if not errors:
        score=score_oracle(x,trace['origins'],trace['capacity'],h)
        for name in ('mean_loss','n','strict_breach_count','strict_breach_rate'):
            # Validation rows store mean_loss/origin_count, not hit aggregates.
            if name in report and not same(report[name],score[name]):errors.append(problem('TRACE_AGGREGATE_MISMATCH',field=name))
        if 'origin_count' in report and report['origin_count']!=score['n']:errors.append(problem('CANDIDATE_FULL_GRID_MISMATCH'))
        return errors,{k:score[k] for k in ('mean_loss','n','strict_breach_count','strict_breach_rate')}
    return errors,None


def resource_readback(root,formal,private,design):
    observations=[];errors=[];unverified=[]
    for folder in sorted((formal/'cells').iterdir()):
        if not folder.is_dir():continue
        unit=folder.name;start=load_json(folder/'parent-start.json')
        end=load_json(folder/'parent-termination.json') if (folder/'parent-termination.json').exists() else None
        elapsed=None if end is None else (datetime.fromisoformat(end['ended_utc'].replace('Z','+00:00'))-datetime.fromisoformat(start['started_utc'].replace('Z','+00:00'))).total_seconds()
        worker=load_json(folder/'worker-receipt.json') if (folder/'worker-receipt.json').exists() else {}
        resources=worker.get('resources') or {}
        rss=resources.get('peak_rss_bytes');threads=resources.get('maximum_observed_os_threads')
        probes_count=resources.get('thread_snapshot_count',0)
        source='worker-receipt'
        if not finite(rss) or not finite(threads):
            probe=private_path(root,private,unit+'/ps-snapshots.jsonl')
            if probe.exists():
                no_symlinks(probe);saved=[json.loads(s) for s in probe.read_text().splitlines() if s.strip()]
                rss=max((r['peak_rss_bytes'] for r in saved),default=None)
                threads=max((r['maximum_observed_os_threads'] for r in saved),default=None)
                probes_count=len(saved);source='checkpoint-sample-aggregate'
        observation=dict(cell_id=unit,elapsed_seconds=elapsed,peak_rss_bytes=rss,maximum_observed_os_threads=threads,
            resource_source=source,probe_count=probes_count)
        observations.append(observation)
        if not finite(rss) or not finite(threads) or not finite(elapsed) or not probes_count:unverified.append(unit)
        if finite(rss) and rss>design['resources']['maximum_rss_bytes']:errors.append(problem('RSS_CAP_EXCEEDED',cell_id=unit))
        if finite(threads) and threads>design['resources']['maximum_observed_os_threads']:errors.append(problem('THREAD_CAP_EXCEEDED',cell_id=unit))
        if finite(elapsed) and elapsed>design['resources']['worker_hard_seconds']+TERMINATION_TOLERANCE_SECONDS:errors.append(problem('WORKER_WALL_EXCEEDED',cell_id=unit))
        if worker:
            if worker.get('code_hash_start')!='PASS' or worker.get('code_hash_end')!='PASS':errors.append(problem('WORKER_CODE_HASH_UNVERIFIED',cell_id=unit))
            if worker.get('technical_error'):errors.append(problem('WORKER_TECHNICAL_ERROR',cell_id=unit))
    return dict(status='FAIL' if errors else 'UNVERIFIED' if unverified or not observations else 'PASS',
        attempted_worker_count=len(observations),unverified_cells=unverified,
        maximum_observed_rss_bytes=max((r['peak_rss_bytes'] for r in observations if finite(r['peak_rss_bytes'])),default=None),
        maximum_observed_os_threads=max((r['maximum_observed_os_threads'] for r in observations if finite(r['maximum_observed_os_threads'])),default=None),
        maximum_observed_worker_seconds=max((r['elapsed_seconds'] for r in observations if finite(r['elapsed_seconds'])),default=None),
        termination_tolerance_seconds=TERMINATION_TOLERANCE_SECONDS,observations=observations,differences=errors)


def audit_bundle(root,formal):
    root=Path(root).absolute();formal=Path(formal).absolute();no_symlinks(root);no_symlinks(formal)
    formal.relative_to(root)
    termination_path=formal/'study-termination.json'
    if not termination_path.exists():raise ValueError('STUDY_NOT_TERMINATED')
    termination=load_json(termination_path)
    if termination.get('all_workers_terminated') is not True:raise ValueError('STUDY_NOT_TERMINATED')
    required=('manifest.json','inventory.json','summary.json','classification.json','study-termination.json','summary.csv','contrasts.csv')
    hashes={name:sha(formal/name) for name in required}
    manifest=load_json(formal/'manifest.json');design=manifest['design']
    inventory=load_json(formal/'inventory.json');summary=load_json(formal/'summary.json');classification=load_json(formal/'classification.json')
    errors=[];private_hashes={};private=Path(manifest['private_directory']).absolute();private_path(root,private,'guard')
    commit=manifest['design_commit'];commit_time=None
    try:
        commit_time=subprocess.check_output(['git','show','-s','--format=%cI',commit],cwd=root,text=True).strip()
        if datetime.fromisoformat(commit_time)>=datetime.fromisoformat(manifest['started_utc'].replace('Z','+00:00')):errors.append(problem('DESIGN_NOT_BEFORE_RUN'))
        for name,digest in manifest['protocol_hashes'].items():
            original=subprocess.check_output(['git','show',commit+':'+name],cwd=root)
            if hashlib.sha256(original).hexdigest()!=digest:errors.append(problem('FROZEN_PROTOCOL_COMMIT_HASH_MISMATCH',path=name))
            if sha(root/name)!=digest:errors.append(problem('CURRENT_PROTOCOL_HASH_MISMATCH',path=name))
        design_path='protocol/revision-v8/wp4-daily-fx-design.json'
        if load_json(root/design_path)!=design:errors.append(problem('MANIFEST_DESIGN_MISMATCH'))
    except (OSError,ValueError,subprocess.SubprocessError):errors.append(problem('DESIGN_COMMIT_UNVERIFIED'))
    for name,digest in manifest['code_hashes'].items():
        if sha(root/name)!=digest:errors.append(problem('SEALED_CODE_HASH_MISMATCH',path=name))
    for name,digest in design['original_and_sealed_modules_sha256'].items():
        if sha(root/name)!=digest:errors.append(problem('ORIGINAL_OR_WP3_SOURCE_CHANGED',path=name))
    source_path=root/design['input']['local_private_path'];source_path.resolve().relative_to((root/'.scratch').resolve())
    x,t=read_pinned_csv(source_path,design['input']);daily=daily_oracle(x,t);daily_x=daily['position'];n=len(daily_x)
    expected_keys={(w,h,m) for w in design['windows'] for h in design['clock_and_target']['horizons'] for m in design['methods']}
    keys=[tuple(r[k] for k in ('window','horizon','method')) for r in inventory]
    if len(keys)!=len(expected_keys) or set(keys)!=expected_keys:errors.append(problem('INVENTORY_GRID_MISMATCH'))
    statuses={'COMPLETE','FAILED','NOT_ATTEMPTED','NA_SAMPLE_SIZE'}
    rescore=json.loads(json.dumps(inventory));trace_checked=set();source_cells=[];candidate_count=0;checked_scores=0;fit_checks=0
    for w in design['windows']:
        for h in design['clock_and_target']['horizons']:
            cell=f'W{w}_H{h}';public=formal/'cells'/cell;cell_private=private/cell
            geometry=geometry_oracle(n,h,w,design)
            source_record=None
            if (public/'worker-source.json').exists():
                source_record=load_json(public/'worker-source.json');source_cells.append(cell)
                if source_record.get('daily_metadata')!=daily['metadata']:errors.append(problem('DAILY_METADATA_MISMATCH',cell_id=cell))
                identity=source_record.get('source_identity',{})
                if (identity.get('accepted_csv_sha256')!=design['input']['sha256']
                        or identity.get('accepted_csv_bytes')!=design['input']['bytes'] or identity.get('source_verified') is not True):
                    errors.append(problem('WORKER_SOURCE_PIN_MISMATCH',cell_id=cell))
                daily_path=private_path(root,cell_private,'daily-series.npz');digest=sha(daily_path);private_hashes[daily_path]=digest
                if source_record.get('daily_mapping_sha256')!=digest:errors.append(problem('DAILY_MAPPING_FILE_HASH_MISMATCH',cell_id=cell))
                saved=load_npz(daily_path,DAILY_KEYS)
                for name in DAILY_KEYS:
                    a=saved[name];b=daily[name]
                    required_kind='f' if name=='position' else 'i' if name=='selected_indices' else 'M'
                    if a.dtype.kind!=required_kind or a.dtype.itemsize!=8 or a.shape!=b.shape or not np.array_equal(a,b):errors.append(problem('PRIVATE_DAILY_ARRAY_MISMATCH',cell_id=cell,field=name))
                if not (public/'cell-geometry.json').exists() or load_json(public/'cell-geometry.json')!=geometry:
                    errors.append(problem('PUBLIC_GEOMETRY_MISMATCH',cell_id=cell))
            for row in rescore:
                if (row['window'],row['horizon'])!=(w,h):continue
                method=row['method'];context=dict(cell_id=cell,method=method)
                if row.get('cell_id')!=cell or row.get('status') not in statuses:errors.append(problem('METHOD_IDENTITY_OR_STATUS_MISMATCH',**context))
                if row.get('geometry') is not None and row['geometry']!=geometry:errors.append(problem('METHOD_GEOMETRY_MISMATCH',**context))
                if geometry['status']=='NA_SAMPLE_SIZE' and row['status']=='COMPLETE':errors.append(problem('INADEQUATE_SAMPLE_LABELLED_COMPLETE',**context))
                if row['status']!='COMPLETE' and row.get('evaluation') is not None:errors.append(problem('FAILED_METHOD_HAS_AGGREGATE',**context))
                for i,candidate in enumerate(row.get('candidates',[])):
                    candidate_count+=1
                    if candidate['status']!='COMPLETE':continue
                    stem=f'{cell}_{method}_validation-{i}';ids=np.arange(geometry['validation_first'],geometry['validation_last']+1,dtype=np.int64)
                    findings,score=audit_trace(root,cell_private,public,stem,candidate,daily_x,h,w,ids,geometry['validation_first'],method,design,private_hashes)
                    errors.extend(dict(e,**context,segment='validation',candidate_index=i) for e in findings);trace_checked.add((cell,stem));checked_scores+=1
                    issues=fit_diagnostic_errors(candidate,h,w,ids,geometry['validation_first'],design);fit_checks+=len(candidate.get('fit_diagnostics',[]))
                    errors.extend(dict(e,**context,segment='validation',candidate_index=i) for e in issues)
                    if score:candidate['mean_loss']=score['mean_loss']
                errors.extend(selection_errors(row,design))
                if row['status']=='COMPLETE':
                    if source_record is None:errors.append(problem('COMPLETE_METHOD_WITHOUT_RESAMPLING_RECEIPT',**context))
                    ids=np.arange(geometry['evaluation_first'],geometry['evaluation_last']+1,dtype=np.int64);stem=f'{cell}_{method}_evaluation'
                    findings,score=audit_trace(root,cell_private,public,stem,row['evaluation'],daily_x,h,w,ids,geometry['evaluation_first'],method,design,private_hashes)
                    errors.extend(dict(e,**context,segment='evaluation') for e in findings);trace_checked.add((cell,stem));checked_scores+=1
                    issues=fit_diagnostic_errors(row,h,w,ids,geometry['evaluation_first'],design);fit_checks+=len(row.get('fit_diagnostics',[]))
                    errors.extend(dict(e,**context,segment='evaluation') for e in issues)
                    if score:row['evaluation'].update(score)
            # A complete private trace may survive a later diagnostic/report failure.
            # Check its bytes/target/grid but never relabel the failed method COMPLETE.
            if public.exists():
                for sidecar in public.glob('*.trace.json'):
                    stem=sidecar.name[:-len('.trace.json')]
                    if (cell,stem) in trace_checked:continue
                    try:
                        rest=stem[len(cell)+1:];method,segment=rest.split('_',1)
                        if method not in design['methods']:raise ValueError('UNKNOWN_TRACE_METHOD')
                        validation=segment.startswith('validation-')
                        if not validation and segment!='evaluation':raise ValueError('UNKNOWN_TRACE_SEGMENT')
                        ids=np.arange(geometry['validation_first'],geometry['validation_last']+1,dtype=np.int64) if validation else np.arange(geometry['evaluation_first'],geometry['evaluation_last']+1,dtype=np.int64)
                        findings,_=audit_trace(root,cell_private,public,stem,load_json(sidecar),daily_x,h,w,ids,
                            geometry['validation_first'] if validation else geometry['evaluation_first'],method,design,private_hashes)
                        errors.extend(dict(e,cell_id=cell,method=method,segment='saved-failed-orphan') for e in findings)
                        trace_checked.add((cell,stem));checked_scores+=1
                    except (ValueError,KeyError,OSError):errors.append(problem('UNRECOGNIZED_OR_UNREADABLE_TRACE',cell_id=cell))
    if candidate_count!=sum(len(design['menus'].get(m,[])) for _,_,m in expected_keys):errors.append(problem('CANDIDATE_SLOT_COUNT_MISMATCH'))
    if summary.get('cells')!=inventory:errors.append(problem('SUMMARY_INVENTORY_VALUES_MISMATCH'))
    if summary.get('source_inventory_sha256')!=hashes['inventory.json']:errors.append(problem('SUMMARY_INVENTORY_HASH_MISMATCH'))
    if summary.get('study_status')!=termination['status']:errors.append(problem('SUMMARY_PROCESS_STATUS_MISMATCH'))
    errors+=csv_errors(formal/'summary.csv',inventory)
    errors+=csv_errors(formal/'contrasts.csv',summary.get('contrasts',[]))
    computed_contrasts=contrasts_oracle(rescore,design)
    if not same(computed_contrasts,summary.get('contrasts')):errors.append(problem('CONTRASTS_MISMATCH'))
    computed_classification={m:classification_oracle(rescore,m,design) for m in ('QR33','QR4')}
    if not same(computed_classification,summary.get('classifications')) or not same(computed_classification,classification):errors.append(problem('CLASSIFICATION_MISMATCH'))
    consistency=None if not source_cells else dict(source_identity=dict(accepted_csv_sha256=design['input']['sha256'],accepted_csv_bytes=design['input']['bytes'],source_verified=True),daily_metadata=daily['metadata'])
    if termination.get('source_consistency')!=consistency or summary.get('source_consistency')!=consistency:errors.append(problem('SOURCE_CONSISTENCY_MISMATCH'))
    resource=resource_readback(root,formal,private,design);errors+=resource['differences']
    if resource['attempted_worker_count']!=termination.get('attempted_workers'):errors.append(problem('ATTEMPTED_WORKER_COUNT_MISMATCH'))
    completed=sum(load_json(p).get('status')=='COMPLETE' for p in (formal/'cells').glob('*/parent-termination.json'))
    if completed!=termination.get('completed_workers'):errors.append(problem('COMPLETED_WORKER_COUNT_MISMATCH'))
    if dict(Counter(r['status'] for r in inventory))!=termination.get('method_status_counts'):errors.append(problem('TERMINATION_METHOD_COUNTS_MISMATCH'))
    wall=termination.get('elapsed_seconds')
    if not finite(wall) or wall>design['resources']['global_wall_seconds']+TERMINATION_TOLERANCE_SECONDS:errors.append(problem('GLOBAL_WALL_EXCEEDED_OR_UNVERIFIED'))
    if termination.get('code_hash_check')!='PASS':errors.append(problem('TERMINATION_CODE_SEAL_UNVERIFIED'))
    if sha(source_path)!=design['input']['sha256']:errors.append(problem('RAW_SOURCE_CHANGED_DURING_AUDIT'))
    for path,digest in private_hashes.items():
        if sha(path)!=digest:errors.append(problem('PRIVATE_ARRAY_CHANGED_DURING_AUDIT',file=path.name))
    for name,digest in hashes.items():
        if sha(formal/name)!=digest:errors.append(problem('PUBLIC_INPUT_CHANGED_DURING_AUDIT',file=name))
    return dict(schema='independent-wp4-audit-1',status='FAIL' if errors else 'UNVERIFIED' if resource['status']!='PASS' else 'PASS',
        audited_utc=datetime.now(timezone.utc).isoformat(),difference_count=len(errors),differences=errors,input_hashes=hashes,
        scope='Independent resampling/target/score/F arithmetic and provenance readback, without QR fitting or new tests.',
        data_privacy='Only aggregate counts and hashes are written here; original/daily/trace arrays remain private.',
        original_rows_checked=len(x),daily_rows_checked=n,source_sha256=design['input']['sha256'],daily_fingerprints=daily['metadata']['fingerprints'],
        resampled_cells_verified=source_cells,resampling_cell_count=len(source_cells),complete_trace_scores_checked=checked_scores,
        fit_maturity_records_checked=fit_checks,planned_method_slots=len(expected_keys),actual_method_slots=len(inventory),
        planned_candidate_slots=32,actual_candidate_slots=candidate_count,contrasts_checked=len(computed_contrasts),
        classifications=computed_classification,resources=resource,study_elapsed_seconds=wall,
        design_commit=commit,design_commit_time=commit_time,study_started_utc=manifest['started_utc'],
        private_npz_hashes={str(p.relative_to(private)):d for p,d in private_hashes.items()},
        original_primary_comparisons_modified_by_auditor=False,new_statistical_tests=False,qr_refits_performed_by_auditor=0,
        auditor_sha256=sha(Path(__file__)),
        process_completion_is_not_method_success=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--formal',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv);root=args.root.absolute();formal=args.formal or root/'results/revision-v8/wp4'
    output=args.output.absolute();output.relative_to(root);no_symlinks(output)
    if output.exists():raise FileExistsError('AUDIT_OUTPUT_ALREADY_EXISTS')
    result=audit_bundle(root,formal)
    with output.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('status','difference_count','actual_method_slots','actual_candidate_slots','complete_trace_scores_checked')}))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
