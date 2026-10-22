"""Audit every fixed validation candidate and freeze the full selected menu.

This auxiliary artifact builder never fits a model or evaluates the holdout.
It rechecks the pinned validation paths, private traces and native score means.
"""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import csv
import hashlib
import json
import math
from pathlib import Path
import signal
import sys
import time
sys.dont_write_bytecode=True
from run_study import RunGuard,create_attempt,arm_hard_deadline,utc_now
import run_conditional_study as runner
from conditional_study import select_parameter
from conditional_sources import load_source
import numpy as np

ROOT=Path(__file__).resolve().parent
FREEZE='e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb'


def main():
    started=time.monotonic();started_utc=utc_now()
    spec,_=runner.verify_executable_freeze(FREEZE)
    attempt=ROOT/'.scratch/revision-20261022/selection-audit-01'
    public,private=create_attempt(attempt)
    guard=RunGuard(started,started_utc,attempt,public,private)
    arm_hard_deadline();guard(stage='selection_audit_start')
    sources={}
    for source_id,cfg in spec['sources'].items():
        sources[source_id]=load_source(ROOT/cfg['input_relative_path'],source_id,
            expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
    cells=[];summary=[];receipts=[];raws={};max_rss=0;max_threads=0;worker_seconds=0.;fit_counts={}
    for source_id,h,w,family in runner._inventory(spec):
        cfg=spec['sources'][source_id];source=sources[source_id]
        first,last=cfg['validation_origin_first'],cfg['validation_origin_last']
        origins=np.arange(first,last+1,dtype=np.int64)
        if last+h>=cfg['evaluation_origin_first']:raise ValueError('validation label touches evaluation')
        relative=Path(f'.scratch/revision-20261022/val-{source_id}-h{h}-w{w}-{family}-01/public/manifest.json')
        raw=(ROOT/relative).read_bytes();receipt=json.loads(raw)
        if (receipt['phase']!='validation' or receipt['executable_freeze_sha256']!=FREEZE
            or tuple(receipt[k] for k in ('source','horizon','window','family'))!=(source_id,h,w,family)
            or receipt['status'] not in ('COMPLETE','INELIGIBLE')):raise ValueError('validation receipt incomplete')
        candidates=runner._candidates(spec,cfg,w,family)
        chosen=select_parameter(receipt['result']['candidate_rows'],candidates,expected_count=len(origins))
        actual_peak=np.array([max(abs(float(source.position[t+j])) for j in range(h+1)) for t in origins])
        artifact=receipt['artifacts']
        if len(artifact)!=1 or artifact[0]['name']!='numeric-traces.npz':raise ValueError('trace artifact inventory')
        trace_path=ROOT/relative.parent.parent/'private/numeric-traces.npz'
        trace_raw=trace_path.read_bytes()
        if len(trace_raw)!=artifact[0]['bytes'] or hashlib.sha256(trace_raw).hexdigest()!=artifact[0]['sha256']:
            raise ValueError('private trace hash mismatch')
        with np.load(trace_path,allow_pickle=False) as traces:
            for j,row in enumerate(receipt['result']['candidate_rows']):
                prefix='candidate_'+str(j)+'_'
                if row['status']!='COMPLETE':raise ValueError('failed candidates need explicit incomplete publication handling')
                if not np.array_equal(traces[prefix+'origins'],origins):raise ValueError('trace origin mismatch')
                if not np.array_equal(traces[prefix+'peak'],actual_peak):raise ValueError('independent peak mismatch')
                if not np.array_equal(traces[prefix+'floor'],np.abs(source.position[origins])):raise ValueError('floor mismatch')
                capacity=traces[prefix+'capacity'];error=actual_peak-capacity
                losses=.95*np.maximum(error,0.)+.05*np.maximum(-error,0.)
                if not np.array_equal(traces[prefix+'pinball'],losses):raise ValueError('stored native score mismatch')
                mean=math.fsum(map(float,losses))/len(origins)
                if mean!=row['mean_pinball']:raise ValueError('public mean mismatch')
                expected_refits=first+((origins-first)//cfg['refit_step'])*cfg['refit_step']
                if not np.array_equal(traces[prefix+'refit_indices'],expected_refits):raise ValueError('refit schedule mismatch')
                selected=row['parameter']==chosen['parameter']
                summary.append(dict(source=source_id,native_unit=cfg['native_unit'],horizon=h,window=w,family=family,
                    parameter=row['parameter'],status=row['status'],origin_count=len(origins),mean_pinball=mean,
                    selected=selected,plain_knn_full_pool_fallback=family=='KNN' and row['parameter']==w))
        for d in receipt['result']['fit_diagnostics']:
            r=d['refit_index']
            if (d['training_first_origin']!=r-h-w+1 or d['training_last_origin']!=r-h
                or d['training_count']!=w or d['latest_label_end']!=r):raise ValueError('fit maturity trace mismatch')
            if family=='QR' and not (d['duality_gap']<=d['gap_tolerance']
                and d['primal_residual']<=d['primal_tolerance'] and d['dual_residual']<=d['dual_tolerance']
                and d['dual_integer_sum']==0):raise ValueError('numerical acceptance mismatch')
        fit_counts[family]=fit_counts.get(family,0)+len(receipt['result']['fit_diagnostics'])
        resource=receipt['resources'];max_rss=max(max_rss,resource['peak_rss_bytes'])
        max_threads=max(max_threads,resource['maximum_observed_os_threads']);worker_seconds+=resource['elapsed_seconds']
        public_name=f'validation-{source_id}-h{h}-w{w}-{family}.json'
        raws[public_name]=raw
        digest=hashlib.sha256(raw).hexdigest()
        cells.append(dict(source=source_id,horizon=h,window=w,family=family,status=chosen['status'],parameter=chosen['parameter'],
            validation_receipts=[dict(path=str(relative),sha256=digest)]))
        receipts.append(dict(source=source_id,horizon=h,window=w,family=family,status=receipt['status'],
            public_file=public_name,sha256=digest,elapsed_seconds=resource['elapsed_seconds'],
            peak_rss_bytes=resource['peak_rss_bytes'],maximum_observed_os_threads=resource['maximum_observed_os_threads']))
        guard(stage='validation_receipt_audited')
    selection=dict(version=1,status='FROZEN',created_utc=utc_now(),executable_freeze_sha256=FREEZE,cells=cells)
    selection_path=ROOT/'protocol/revision-20261022/selection-freeze.json'
    selection_raw=(json.dumps(selection,indent=2,allow_nan=False)+'\n').encode()
    with selection_path.open('xb') as stream:stream.write(selection_raw)
    selection_sha=hashlib.sha256(selection_raw).hexdigest()
    verified=runner.verify_selection_freeze(selection_path,selection_sha,FREEZE,spec)
    if len(verified)!=24:raise ValueError('selection inventory mismatch')
    runner.verify_executable_freeze(FREEZE)
    output=ROOT/'results/revision-20261022';output.mkdir(parents=False,exist_ok=False)
    with (output/'validation-summary.csv').open('x',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    for name,raw in raws.items():
        with (output/name).open('xb') as stream:stream.write(raw)
    guard(stage='selection_audit_final')
    audit=dict(status='VERIFIED',scope='validation only; no holdout results',created_utc=utc_now(),
        executable_freeze_sha256=FREEZE,selection_freeze_sha256=selection_sha,cell_count=len(cells),candidate_count=len(summary),
        maximum_worker_peak_rss_bytes=max_rss,maximum_observed_worker_threads=max_threads,
        total_reported_worker_seconds=worker_seconds,fit_counts=fit_counts,receipts=receipts,
        selection_audit_resources=guard.resources,builder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with (output/'validation-audit.json').open('x') as stream:json.dump(audit,stream,indent=2);stream.write('\n')
    signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps({k:audit[k] for k in ('status','cell_count','candidate_count','selection_freeze_sha256',
        'maximum_worker_peak_rss_bytes','maximum_observed_worker_threads','total_reported_worker_seconds','fit_counts')},indent=2))


if __name__=='__main__':main()
