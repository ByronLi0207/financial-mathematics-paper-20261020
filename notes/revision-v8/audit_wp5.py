"""Independent fixed-prefix WP5 saved-result arithmetic/provenance audit.

Only the terminated-study entry point may read the pinned CSV/private NPZs.
The auditor never fits QR, retunes, re-evaluates an old window or calculates
an unlisted test. Pinned source/target/F-oracle routines are copied unchanged
from the independently tested WP4 audit, not from forecasting/score engines.
Public output contains aggregates and hashes only, never financial vectors.
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
HEADER=['datetime','NetPosUsd','NetUsdPnL','AbsVolume','Mid']
TERMINATION_TOLERANCE_SECONDS=5.
CSV_MAX_FIELD_BYTES=16*1024*1024

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
    """Check complete saved fields, with an explicit 16MiB UTF-8 field cap.

    Rolling-refit diagnostic JSON legitimately exceeds the CSV module's
    platform default131072-character limit. Raise that parser ceiling only
    for this read, restore it even on error, and enforce the byte cap after
    parsing. No field is truncated and no input byte is rewritten.
    """
    no_symlinks(path)
    fields=list(dict.fromkeys(k for r in rows for k in r))
    limit=csv.field_size_limit()
    try:
        # A UTF-8 field cannot contain more characters than encoded bytes;
        # this bounds parser allocation before checking the exact byte count.
        csv.field_size_limit(CSV_MAX_FIELD_BYTES)
        with open(path,newline='',encoding='utf-8') as stream:
            reader=csv.DictReader(stream,strict=True);actual=list(reader)
            if reader.fieldnames!=fields:return [problem('CSV_HEADER_MISMATCH',file=Path(path).name)]
            for row in actual:
                for value in row.values():
                    if isinstance(value,str) and len(value.encode('utf-8'))>CSV_MAX_FIELD_BYTES:
                        return [problem('CSV_FIELD_BYTES_EXCEEDED',file=Path(path).name)]
    except csv.Error:
        return [problem('CSV_FIELD_PARSE_ERROR',file=Path(path).name)]
    finally:
        csv.field_size_limit(limit)
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

def private_path(root,base,name):
    base=Path(base).absolute();base.resolve().relative_to((root/'.scratch').resolve())
    path=base/name;no_symlinks(path);return path

def load_npz(path,keys):
    no_symlinks(path)
    with np.load(path,allow_pickle=False) as data:
        if set(data.files)!=set(keys):raise ValueError('PRIVATE_NPZ_KEYS_MISMATCH')
        return {name:np.array(data[name],copy=True) for name in data.files}


def geometry_oracle(n,design):
    sample=design['sample'];first=sample['evaluation_first'];last=sample['evaluation_last']
    h=sample['max_horizon'];count=last-first+1
    if (type(n) is not int or type(first) is not int or type(last) is not int
            or count<=0 or count!=sample['evaluation_count']
            or first!=sample['feature_valid_from']+sample['longest_window']+h-1
            or last+h+1!=sample['original_validation_first']):
        raise ValueError('INVALID_FROZEN_GEOMETRY')
    reason='BACKCAST_NOT_FULLY_OBSERVED' if last+h>=n else None
    return dict(status='READY' if reason is None else 'NA_SAMPLE_SIZE',reason=reason,
        evaluation_first=first,evaluation_last=last,evaluation_count=count,last_target_index=last+h)


def method_spec(design,method):
    specs=[s for s in design['methods'] if s['name']==method]
    if len(specs)!=1:raise ValueError('UNKNOWN_OR_DUPLICATE_METHOD')
    return specs[0]


def trace_errors(position,trace,horizon,method,design):
    if set(trace)!=TRACE_KEYS:return [problem('TRACE_KEYS_MISMATCH')]
    spec=method_spec(design,method);sample=design['sample'];first=sample['evaluation_first']
    expected=np.arange(first,sample['evaluation_last']+1,dtype=np.int64)
    ids=np.asarray(trace['origins']);errors=[]
    if ids.dtype.kind not in 'iu' or not np.array_equal(ids,expected):
        return [problem('TRACE_ISSUE_GRID_MISMATCH',expected_count=len(expected),actual_count=int(ids.size))]
    if any(np.asarray(v).shape!=ids.shape for v in trace.values()):return [problem('TRACE_SHAPE_MISMATCH')]
    refits=first+spec['refit_step']*((ids-first)//spec['refit_step'])
    if np.asarray(trace['refit_indices']).dtype.kind not in 'iu' or not np.array_equal(trace['refit_indices'],refits):
        errors.append(problem('TRACE_REFIT_GRID_MISMATCH'))
    try:score=score_oracle(position,ids,trace['capacity'],horizon)
    except (ValueError,IndexError,FloatingPointError):return errors+[problem('TRACE_SCORE_INVALID')]
    for field in ('peak','floor','pinball'):
        actual=np.asarray(trace[field]);expected=score[field]
        if actual.dtype.kind not in 'iuf' or not np.isfinite(actual).all() or not np.allclose(actual,expected,rtol=1e-12,atol=1e-10):
            errors.append(problem('TRACE_VALUE_MISMATCH',field=field))
    if np.asarray(trace['strict_breach']).dtype.kind!='b' or not np.array_equal(trace['strict_breach'],score['strict_breach']):
        errors.append(problem('TRACE_STRICT_BREACH_MISMATCH'))
    if spec['engine']=='F':
        replay=f_oracle(position,ids,horizon,spec['window'],spec['refit_step'],first)
        if not np.array_equal(trace['capacity'],replay['capacity']):errors.append(problem('F_DETERMINISTIC_REPLAY_MISMATCH'))
    return errors


def normal_dm_oracle(d,horizon):
    """Independent scalar Bartlett covariance; no call to inference helpers."""
    values=np.asarray(d,dtype=np.float64)
    if (values.ndim!=1 or not np.isfinite(values).all() or type(horizon) is not int
            or horizon<1 or len(values)<=horizon):raise ValueError('INVALID_DM_INPUT')
    n=len(values);L=min(n-1,max(horizon,int(4*(n/100)**(2/9))))
    mean=math.fsum(map(float,values))/n
    # Production covariance centers by NumPy mean; preserve that definition,
    # then independently reduce lagged products with accurate scalar sums.
    centered=[float(v)-float(np.mean(values)) for v in values]
    variance=math.fsum(v*v for v in centered)/n
    for lag in range(1,L+1):
        gamma=math.fsum(centered[i]*centered[i-lag] for i in range(lag,n))/n
        variance+=2*(1-lag/(L+1))*gamma
    result=dict(n=n,horizon=horizon,bandwidth=L,mean_difference=mean,lrv=variance,dm_t=None,dm_p=None)
    if variance<=0 or all(v==values[0] for v in values):
        result['status']='IDENTICAL_LOSSES' if all(v==0 for v in values) else 'ZERO_LONG_RUN_VARIANCE'
        return result
    statistic=mean/math.sqrt(variance/n)
    result.update(status='OK',dm_t=statistic,dm_p=math.erfc(abs(statistic)/math.sqrt(2)))
    return result


def exposure_oracle(design):
    windows={r['name']:r for r in design['three_window_summary']['windows']}
    a=windows['extra_full_prefix'];b=windows['previous_retro'];c=windows['original_inspected']
    overlap=max(0,min(a['last'],b['last'])-max(a['first'],b['first'])+1)
    if overlap!=design['known_exposure']['overlap_with_retro_evaluation_origins']:
        raise ValueError('DISCLOSED_OVERLAP_MISMATCH')
    return dict(extra_full_prefix=[a['first'],a['last']],previous_retro=[b['first'],b['last']],
        original_inspected=[c['first'],c['last']],overlap_origins=overlap,
        previous_retro_fully_nested=a['first']<=b['first']<=b['last']<=a['last'],
        fresh_independent_third_period=False,scientific_status='MISMATCH',
        mismatch='MISMATCH-WP5-01',later_parameter_choice_disclosed=True)


def exposure_metadata_errors(root,design):
    """Recheck actual old completion metadata/interval union, never old arrays."""
    root=Path(root);proof=load_json(root/'notes/revision-v8/wp5-prior-exposure-proof.json')
    source=Path(proof['source'])
    if source.is_absolute() or '..' in source.parts:return [problem('EXPOSURE_SOURCE_PATH_INVALID')]
    if sha(root/source)!=proof['source_sha256']:return [problem('EXPOSURE_SOURCE_HASH_MISMATCH')]
    old=load_json(root/source);h=design['sample']['max_horizon'];w=design['sample']['longest_window']
    groups=[g for g in old['groups'] if all(g['group'].get(k)==v for k,v in
        [('phase','retro'),('source','fx_hourly'),('horizon',h),('window',w)])]
    if len(groups)!=1:return [problem('EXPOSURE_GROUP_IDENTITY_MISMATCH')]
    g=groups[0];selection=g['selections']['R3'];candidates=selection['candidates'];errors=[]
    rows=[r for r in g['rows'] if r['report']=='R3']
    if (selection['status']!='SELECTED' or len(candidates)!=6 or any(c['status']!='COMPLETE' for c in candidates)
            or len(rows)!=1 or rows[0]['status']!='COMPLETE'):
        errors.append(problem('PRIOR_R3_SCORING_COMPLETION_UNVERIFIED'))
    early,last=design['known_exposure']['R6_retro_evaluation']
    intervals=[(a,b+h) for a,b in g['r3_fold_bounds']]+[(early,last+h)];merged=[]
    for a,b in sorted(intervals):
        if merged and a<=merged[-1][1]+1:merged[-1][1]=max(merged[-1][1],b)
        else:merged.append([a,b])
    sample=design['sample'];target=[sample['evaluation_first'],sample['evaluation_last']+h]
    if merged!=[target] or proof.get('old_H24_target_coverage_merged')!=merged or proof.get('new_H24_target_bounds')!=target:
        errors.append(problem('PRIOR_TARGET_COVERAGE_UNION_MISMATCH'))
    for field,value in [('status','PASS'),('R3_selection_status',selection['status']),
            ('R3_complete_candidate_count',len(candidates)),('R3_candidate_scored_issue_count',candidates[0]['n']),
            ('nested_old_retro_issue_count',design['known_exposure']['overlap_with_retro_evaluation_origins']),
            ('fresh_unscored_third_period',False),('mismatch','MISMATCH-WP5-01')]:
        if proof.get(field)!=value:errors.append(problem('PRIOR_EXPOSURE_PROOF_FIELD_MISMATCH',field=field))
    return errors


def failed_row_errors(row):
    return [problem('FAILED_METHOD_HAS_AGGREGATE')] if row['status']!='COMPLETE' and row.get('evaluation') is not None else []


def completion_errors(public):
    """A flushed method report alone does not establish completed execution."""
    public=Path(public);errors=[]
    try:
        worker=load_json(public/'worker-receipt.json')
        if (worker.get('status')!='COMPLETE' or worker.get('code_hash_start')!='PASS'
                or worker.get('code_hash_end')!='PASS'):
            raise ValueError('WORKER_NOT_COMPLETE')
    except (OSError,ValueError,TypeError,AttributeError):
        errors.append(problem('COMPLETE_WORKER_RECEIPT_UNVERIFIED'))
    try:
        parent=load_json(public/'parent-termination.json')
        if (parent.get('status')!='COMPLETE' or type(parent.get('returncode')) is not int
                or parent['returncode']!=0):
            raise ValueError('PARENT_NOT_COMPLETE')
    except (OSError,ValueError,TypeError,AttributeError):
        errors.append(problem('COMPLETE_PARENT_RECEIPT_UNVERIFIED'))
    return errors


def fit_errors(report,horizon,method,design):
    spec=method_spec(design,method);first=design['sample']['evaluation_first'];last=design['sample']['evaluation_last']
    refs=list(range(first,last+1,spec['refit_step']));fits=report.get('fit_diagnostics',[]);errors=[]
    if len(fits)!=len(refs):return [problem('FIT_DIAGNOSTIC_COUNT_MISMATCH')]
    for detail,r in zip(fits,refs):
        expected=dict(refit_index=r,training_first_origin=r-horizon-spec['window']+1,
            training_last_origin=r-horizon,training_count=spec['window'],latest_label_end=r)
        for key,value in expected.items():
            if detail.get(key)!=value:errors.append(problem('FIT_MATURITY_MISMATCH',field=key))
        if detail.get('latest_label_end',r+1)>detail.get('refit_index',r):errors.append(problem('IMMATURE_TRAINING_LABEL'))
        if spec['engine']!='F':
            if expected['training_first_origin']<design['sample']['feature_valid_from']:errors.append(problem('INCOMPLETE_FEATURE_HISTORY'))
            for residual,tolerance in (('duality_gap','gap_tolerance'),('primal_residual','primal_tolerance'),('dual_residual','dual_tolerance')):
                if not finite(detail.get(residual)) or not finite(detail.get(tolerance)) or detail[residual]>detail[tolerance]:
                    errors.append(problem('UNCONVERGED_REPORTED_COMPLETE_FIT',field=residual))
            iteration=detail.get('iterations')
            if type(iteration) is not int or not 0<=iteration<=design['solver']['max_iter']:errors.append(problem('ITERATION_LIMIT_MISMATCH'))
    expected_maturity=dict(refit_count=len(refs),training_first_origin_min=refs[0]-horizon-spec['window']+1,
        training_last_origin_max=refs[-1]-horizon,latest_label_end_max=refs[-1],maximum_label_end_minus_refit=0)
    if report.get('maturity')!=expected_maturity:errors.append(problem('MATURITY_SUMMARY_MISMATCH'))
    return errors


def source_metadata_oracle(x,t,design):
    sample=design['sample'];first=sample['evaluation_first'];last=sample['evaluation_last']
    stamp=lambda value:str(np.datetime_as_string(value,unit='us'))
    return dict(n=len(x),source_first_timestamp=stamp(t[0]),source_last_timestamp=stamp(t[-1]),
        origin_first=first,origin_last=last,origin_count=last-first+1,
        first_issue_time=stamp(t[first]),last_issue_time=stamp(t[last]),
        target_end_by_horizon={str(h):stamp(t[last+h]) for h in design['clock_and_target']['horizons']},
        position_sha256=hashlib.sha256(np.ascontiguousarray(x,dtype='<f8').tobytes()).hexdigest(),
        times_sha256=hashlib.sha256(np.ascontiguousarray(t.astype('datetime64[us]').view('i8'),dtype='<i8').tobytes()).hexdigest())


def contrast_oracle(model,reference,horizon):
    if not np.array_equal(model['origins'],reference['origins']):raise ValueError('PAIRED_GRIDS_DIFFER')
    a=np.asarray(model['pinball']);b=np.asarray(reference['pinball']);n=len(a)
    mean=lambda v:float(v[0]) if all(x==v[0] for x in v) else math.fsum(map(float,v))/len(v)
    av,bv=mean(a),mean(b);ah=int(np.count_nonzero(model['strict_breach']));bh=int(np.count_nonzero(reference['strict_breach']))
    return dict(status='COMPLETE',reason=None,n=n,exact_shared_origins=True,
        mean_model_loss=av,mean_reference_loss=bv,
        relative_change_percent=100*(av/bv-1) if bv else None,
        model_breach_count=ah,model_breach_rate=ah/n,reference_breach_count=bh,reference_breach_rate=bh/n,
        dm=normal_dm_oracle(a-b,horizon))


def parameter_identity_errors(root,design):
    errors=[];sources=design['forecasting']['parameter_source_sha256']
    for name,digest in sources.items():
        if sha(root/name)!=digest:errors.append(problem('PARAMETER_SOURCE_HASH_MISMATCH',path=name))
    qr=load_json(root/'protocol/revision-20261022/selection-freeze.json')
    for h in design['clock_and_target']['horizons']:
        chosen=[r for r in qr['cells'] if r['source']=='fx_hourly' and r['horizon']==h and r['window']==2880 and r['family']=='QR']
        q4=load_json(root/f'results/revision-20261023/parsimonious/fx_hourly-h{h}-w2880.json')
        if (len(chosen)!=1 or chosen[0]['status']!='SELECTED'
                or chosen[0]['parameter']!=method_spec(design,'QR33')['penalty_by_horizon'][str(h)]):
            errors.append(problem('ORIGINAL_QR33_SELECTED_PARAMETER_MISMATCH',horizon=h))
        if q4['status']!='COMPLETE' or q4['selected_penalty']!=method_spec(design,'QR4')['penalty_by_horizon'][str(h)]:
            errors.append(problem('ORIGINAL_QR4_SELECTED_PARAMETER_MISMATCH',horizon=h))
    return errors


def resource_readback(root,formal,private,design):
    observations=[];errors=[];unverified=[]
    for folder in sorted((formal/'units').iterdir()):
        if not folder.is_dir():continue
        unit=folder.name;start=load_json(folder/'parent-start.json')
        end=load_json(folder/'parent-termination.json') if (folder/'parent-termination.json').exists() else None
        elapsed=None if end is None else (datetime.fromisoformat(end['ended_utc'].replace('Z','+00:00'))-datetime.fromisoformat(start['started_utc'].replace('Z','+00:00'))).total_seconds()
        worker=load_json(folder/'worker-receipt.json') if (folder/'worker-receipt.json').exists() else {}
        resources=worker.get('resources') or {};rss=resources.get('peak_rss_bytes');threads=resources.get('maximum_observed_os_threads')
        probes=resources.get('thread_snapshot_count',0);source='worker-receipt'
        if not finite(rss) or not finite(threads):
            path=private_path(root,private,unit+'/ps-snapshots.jsonl')
            if path.exists():
                saved=[json.loads(s) for s in path.read_text().splitlines() if s.strip()]
                rss=max((r['peak_rss_bytes'] for r in saved),default=None)
                threads=max((r['maximum_observed_os_threads'] for r in saved),default=None)
                probes=len(saved);source='checkpoint-sample-aggregate'
        observations.append(dict(unit_id=unit,elapsed_seconds=elapsed,peak_rss_bytes=rss,
            maximum_observed_os_threads=threads,probe_count=probes,resource_source=source))
        if not finite(rss) or not finite(threads) or not finite(elapsed) or not probes:unverified.append(unit)
        if finite(rss) and rss>design['resources']['maximum_rss_bytes']:errors.append(problem('RSS_CAP_EXCEEDED',unit_id=unit))
        if finite(threads) and threads>design['resources']['maximum_observed_os_threads']:errors.append(problem('THREAD_CAP_EXCEEDED',unit_id=unit))
        if finite(elapsed) and elapsed>design['resources']['worker_hard_seconds']+TERMINATION_TOLERANCE_SECONDS:errors.append(problem('WORKER_WALL_EXCEEDED',unit_id=unit))
        if worker:
            if worker.get('code_hash_start')!='PASS' or worker.get('code_hash_end')!='PASS':errors.append(problem('WORKER_CODE_HASH_UNVERIFIED',unit_id=unit))
            if worker.get('technical_error'):errors.append(problem('WORKER_TECHNICAL_ERROR',unit_id=unit))
    return dict(status='FAIL' if errors else 'UNVERIFIED' if unverified or not observations else 'PASS',
        attempted_worker_count=len(observations),unverified_units=unverified,observations=observations,differences=errors,
        maximum_observed_rss_bytes=max((r['peak_rss_bytes'] for r in observations if finite(r['peak_rss_bytes'])),default=None),
        maximum_observed_os_threads=max((r['maximum_observed_os_threads'] for r in observations if finite(r['maximum_observed_os_threads'])),default=None),
        maximum_observed_worker_seconds=max((r['elapsed_seconds'] for r in observations if finite(r['elapsed_seconds'])),default=None),
        termination_tolerance_seconds=TERMINATION_TOLERANCE_SECONDS)


def audit_bundle(root,formal):
    root=Path(root).absolute();formal=Path(formal).absolute();no_symlinks(root);no_symlinks(formal);formal.relative_to(root)
    termination_path=formal/'study-termination.json'
    if not termination_path.exists():raise ValueError('STUDY_NOT_TERMINATED')
    termination=load_json(termination_path)
    if termination.get('all_workers_terminated') is not True:raise ValueError('STUDY_NOT_TERMINATED')
    required=('manifest.json','inventory.json','summary.json','study-termination.json','summary.csv','contrasts.csv')
    hashes={name:sha(formal/name) for name in required};manifest=load_json(formal/'manifest.json');design=manifest['design']
    inventory=load_json(formal/'inventory.json');summary=load_json(formal/'summary.json');errors=[];private_hashes={}
    private=Path(manifest['private_directory']).absolute();private_path(root,private,'guard')
    commit=manifest['design_commit'];commit_time=None
    try:
        commit_time=subprocess.check_output(['git','show','-s','--format=%cI',commit],cwd=root,text=True).strip()
        if datetime.fromisoformat(commit_time)>=datetime.fromisoformat(manifest['started_utc'].replace('Z','+00:00')):errors.append(problem('DESIGN_NOT_BEFORE_RUN'))
        for name,digest in manifest['protocol_hashes'].items():
            frozen=subprocess.check_output(['git','show',commit+':'+name],cwd=root)
            if hashlib.sha256(frozen).hexdigest()!=digest:errors.append(problem('FROZEN_PROTOCOL_COMMIT_HASH_MISMATCH',path=name))
            if sha(root/name)!=digest:errors.append(problem('CURRENT_PROTOCOL_HASH_MISMATCH',path=name))
        if load_json(root/'protocol/revision-v8/wp5-fixed-prefix-design.json')!=design:errors.append(problem('MANIFEST_DESIGN_MISMATCH'))
    except (OSError,ValueError,subprocess.SubprocessError):errors.append(problem('DESIGN_COMMIT_UNVERIFIED'))
    for name,digest in manifest['code_hashes'].items():
        if sha(root/name)!=digest:errors.append(problem('SEALED_CODE_HASH_MISMATCH',path=name))
    for name,digest in design['original_and_sealed_modules_sha256'].items():
        if sha(root/name)!=digest:errors.append(problem('ORIGINAL_OR_SEALED_SOURCE_CHANGED',path=name))
    errors+=parameter_identity_errors(root,design)
    exposure=exposure_oracle(design);errors+=exposure_metadata_errors(root,design)
    source_path=root/design['input']['local_private_path'];source_path.resolve().relative_to((root/'.scratch').resolve())
    x,t=read_pinned_csv(source_path,design['input']);geometry=geometry_oracle(len(x),design);metadata=source_metadata_oracle(x,t,design)
    expected={(h,m['name']) for h in design['clock_and_target']['horizons'] for m in design['methods']}
    keys=[(r['horizon'],r['method']) for r in inventory]
    if len(keys)!=len(expected) or set(keys)!=expected:errors.append(problem('INVENTORY_GRID_MISMATCH'))
    traces={};fit_count=0;score_count=0;source_units=[]
    for row in inventory:
        h=row['horizon'];method=row['method'];unit=f'H{h}_{method}';public=formal/'units'/unit;priv=private/unit
        spec=method_spec(design,method);context=dict(unit_id=unit)
        if row.get('unit_id')!=unit or row.get('status') not in {'COMPLETE','FAILED','NOT_ATTEMPTED','NA_SAMPLE_SIZE'}:
            errors.append(problem('METHOD_IDENTITY_OR_STATUS_MISMATCH',**context))
        for field in ('engine','window','refit_step'):
            if row.get(field)!=spec[field]:errors.append(problem('METHOD_FIXED_SPEC_MISMATCH',field=field,**context))
        penalty=None if spec['penalty_by_horizon'] is None else spec['penalty_by_horizon'][str(h)]
        if row.get('selected_penalty')!=penalty:errors.append(problem('METHOD_FIXED_PENALTY_MISMATCH',**context))
        errors.extend(dict(e,**context) for e in failed_row_errors(row))
        if (public/'worker-source.json').exists():
            src=load_json(public/'worker-source.json');source_units.append(unit)
            identity=src.get('source_identity',{})
            if (identity.get('accepted_csv_sha256')!=design['input']['sha256'] or identity.get('accepted_csv_bytes')!=design['input']['bytes']
                    or identity.get('source_verified') is not True):errors.append(problem('WORKER_SOURCE_PIN_MISMATCH',**context))
            if src.get('source_metadata')!=metadata:errors.append(problem('WORKER_SOURCE_METADATA_MISMATCH',**context))
        if (public/'report.json').exists():
            report=load_json(public/'report.json')
            for field in ('status','reason','selected_penalty','evaluation','fit_diagnostics','maturity'):
                if row.get(field)!=report.get(field):errors.append(problem('INVENTORY_REPORT_MISMATCH',field=field,**context))
        if row['status']=='COMPLETE':
            errors.extend(dict(e,**context) for e in completion_errors(public))
            if geometry['status']!='READY':errors.append(problem('INADEQUATE_SAMPLE_LABELLED_COMPLETE',**context))
            if unit not in source_units:errors.append(problem('COMPLETE_WITHOUT_SOURCE_RECEIPT',**context))
            path=private_path(root,priv,'evaluation.npz');digest=sha(path);private_hashes[path]=digest
            record=load_json(public/'trace.json');score=row['evaluation'];trace=load_npz(path,TRACE_KEYS)
            for entry in (record,score):
                if entry.get('trace_sha256')!=digest or entry.get('trace_origin_count')!=design['sample']['evaluation_count']:
                    errors.append(problem('TRACE_PUBLIC_HASH_OR_COUNT_MISMATCH',**context))
            findings=trace_errors(x,trace,h,method,design);errors.extend(dict(e,**context) for e in findings)
            if not findings:
                replay=score_oracle(x,trace['origins'],trace['capacity'],h)
                for field in ('mean_loss','n','strict_breach_count','strict_breach_rate'):
                    if not same(score.get(field),replay[field]):errors.append(problem('TRACE_AGGREGATE_MISMATCH',field=field,**context))
                # Recompute comparisons from independently checked target/loss,
                # not merely from the potentially corrupted saved pinball.
                traces[(h,method)]=dict(origins=trace['origins'],pinball=replay['pinball'],strict_breach=replay['strict_breach'])
            errors.extend(dict(e,**context) for e in fit_errors(row,h,method,design))
            fit_count+=len(row.get('fit_diagnostics',[]));score_count+=1
    if summary.get('methods')!=inventory:errors.append(problem('SUMMARY_INVENTORY_VALUES_MISMATCH'))
    if summary.get('source_inventory_sha256')!=hashes['inventory.json']:errors.append(problem('SUMMARY_INVENTORY_HASH_MISMATCH'))
    if summary.get('study_status')!=termination['status']:errors.append(problem('SUMMARY_PROCESS_STATUS_MISMATCH'))
    consistency=None if not source_units else dict(source_identity=dict(accepted_csv_sha256=design['input']['sha256'],
        accepted_csv_bytes=design['input']['bytes'],source_verified=True),source_metadata=metadata)
    if termination.get('source_consistency')!=consistency or summary.get('source_consistency')!=consistency:
        errors.append(problem('SOURCE_CONSISTENCY_MISMATCH'))
    if (summary.get('normal_DM_only') is not True or summary.get('post_result') is not True
            or summary.get('exploratory') is not True):errors.append(problem('SUMMARY_ANALYSIS_SCOPE_MISMATCH'))
    errors+=csv_errors(formal/'summary.csv',inventory);errors+=csv_errors(formal/'contrasts.csv',summary.get('contrasts',[]))
    contrast_rows=summary.get('contrasts',[])
    contrast_keys=[(r['horizon'],r['method'],r['reference']) for r in contrast_rows]
    expected_contrasts={(h,m,f) for h in design['clock_and_target']['horizons'] for m in ('QR33','QR4') for f in ('F_matched','F_rolling720')}
    if len(contrast_keys)!=len(expected_contrasts) or set(contrast_keys)!=expected_contrasts:errors.append(problem('CONTRAST_GRID_MISMATCH'))
    dm_count=0
    for row in contrast_rows:
        h=row['horizon'];method=row['method'];ref=row['reference'];context=dict(horizon=h,method=method,reference=ref)
        if (h,method) not in traces or (h,ref) not in traces:
            if row.get('status')=='COMPLETE' or row.get('dm') is not None:errors.append(problem('UNAVAILABLE_PAIR_HAS_COMPUTED_RESULT',**context))
            continue
        recomputed=contrast_oracle(traces[(h,method)],traces[(h,ref)],h)
        for field,value in recomputed.items():
            if not same(row.get(field),value):errors.append(problem('CONTRAST_OR_DM_MISMATCH',field=field,**context))
        for alias,original in [('model_mean_loss','mean_model_loss'),('reference_mean_loss','mean_reference_loss'),('model_breaches','model_breach_count'),('reference_breaches','reference_breach_count')]:
            if alias in row and not same(row[alias],recomputed[original]):errors.append(problem('CONTRAST_ALIAS_MISMATCH',field=alias,**context))
        dm_count+=1
    resource=resource_readback(root,formal,private,design);errors+=resource['differences']
    if resource['attempted_worker_count']!=termination.get('attempted_workers'):errors.append(problem('ATTEMPTED_WORKER_COUNT_MISMATCH'))
    completed=sum(load_json(p).get('status')=='COMPLETE' for p in (formal/'units').glob('*/parent-termination.json'))
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
    return dict(schema='independent-wp5-audit-1',status='FAIL' if errors else 'UNVERIFIED' if resource['status']!='PASS' else 'PASS',
        audited_utc=datetime.now(timezone.utc).isoformat(),difference_count=len(errors),differences=errors,input_hashes=hashes,
        scope='Pinned source, fixed-grid target/loss/F/maturity/parameter and normal-HAC readback only; no QR refits or new tests.',
        source_sha256=design['input']['sha256'],original_rows_checked=len(x),source_metadata=metadata,
        complete_trace_scores_checked=score_count,fit_maturity_records_checked=fit_count,
        planned_method_slots=len(expected),actual_method_slots=len(inventory),normal_DM_comparisons_checked=dm_count,
        known_exposure=exposure,resources=resource,study_elapsed_seconds=wall,
        design_commit=commit,design_commit_time=commit_time,study_started_utc=manifest['started_utc'],
        private_npz_hashes={str(p.relative_to(private)):digest for p,digest in private_hashes.items()},
        data_privacy='Only aggregates and hashes are emitted; private vectors remain private.',
        original_primary_comparisons_modified_by_auditor=False,new_statistical_tests=False,qr_refits_performed_by_auditor=0,
        auditor_sha256=sha(Path(__file__)),process_completion_is_not_method_success=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--formal',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv);root=args.root.absolute();formal=args.formal or root/'results/revision-v8/wp5'
    output=args.output.absolute();no_symlinks(output)
    if output.exists():raise ValueError('OUTPUT_ALREADY_EXISTS')
    result=audit_bundle(root,formal);output.parent.mkdir(parents=True,exist_ok=True)
    with open(output,'x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
