"""Explicitly post-result descriptive floor/coherence checks, without refitting."""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import csv
import hashlib
import io
import json
from pathlib import Path
import signal
import sys
import time
sys.dont_write_bytecode=True
import numpy as np
import study_core as core
import run_conditional_study as runner
from run_study import RunGuard,create_attempt,arm_hard_deadline,utc_now
from build_conditional_results import (FREEZE,SELECTION,expected_cells,receipt_path,
    verified_archive,assert_same,write_csv)

ROOT=Path(__file__).resolve().parent


def load_verified_summary(path,expected):
    """Parse parameter labels from the same byte snapshot whose identity passed."""
    raw=path.read_bytes()
    assert_same((len(raw),hashlib.sha256(raw).hexdigest()),
        (expected['bytes'],expected['sha256']),'accepted summary snapshot')
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))


def _vectors(*values):
    arrays=[core._vector(x,'diagnostic vector') for x in values]
    if any(x.shape!=arrays[0].shape for x in arrays):raise ValueError('diagnostic vector alignment')
    return arrays


def floor_diagnostics(peak,capacity,floor):
    p,c,b=_vectors(peak,capacity,floor)
    if np.any(b<0) or np.any(p<b) or np.any(c<b):raise ValueError('diagnostic known floor')
    binding=c==b;breach=p>c
    n=len(p);bound=int(np.count_nonzero(binding));other=n-bound
    bound_breach=int(np.count_nonzero(binding&breach));other_breach=int(np.count_nonzero(~binding&breach))
    return dict(origin_count=n,zero_headroom_outcome_count=int(np.count_nonzero(p==b)),
        floor_binding_count=bound,floor_binding_rate=bound/n,
        floor_binding_breach_count=bound_breach,floor_binding_breach_denominator=bound,
        floor_binding_breach_rate=bound_breach/bound if bound else None,
        floor_binding_undefined_reason=None if bound else 'NO_FLOOR_BINDING_ISSUES',
        other_issue_breach_count=other_breach,other_issue_breach_denominator=other,
        other_issue_breach_rate=other_breach/other if other else None,
        other_issue_undefined_reason=None if other else 'NO_OTHER_ISSUES')


def horizon_diagnostics(short_capacity,long_capacity,short_peak,long_peak):
    c6,c24,p6,p24=_vectors(short_capacity,long_capacity,short_peak,long_peak)
    violations=int(np.count_nonzero(p6>p24))
    if violations:raise ValueError('impossible nested target order')
    with np.errstate(over='raise',invalid='raise'):positive=np.maximum(c6-c24,0.)
    crossings=int(np.count_nonzero(positive>0))
    return dict(origin_count=len(c6),short_horizon=6,long_horizon=24,
        strict_crossing_count=crossings,strict_crossing_rate=crossings/len(c6),
        maximum_positive_crossing=float(np.max(positive)),mean_positive_crossing=core.stable_mean(positive),
        target_order_violation_count=violations)


def main():
    started=time.monotonic();started_utc=utc_now()
    plan=ROOT/'protocol/revision-20261022/post-result-diagnostics.md';plan_raw=plan.read_bytes()
    spec,_=runner.verify_executable_freeze(FREEZE)
    runner.verify_selection_freeze(ROOT/'protocol/revision-20261022/selection-freeze.json',SELECTION,FREEZE,spec)
    attempt=ROOT/'.scratch/revision-20261022/post-result-diagnostics-01'
    public,private=create_attempt(attempt);guard=RunGuard(started,started_utc,attempt,public,private)
    arm_hard_deadline();guard(stage='post_result_diagnostics_start')
    accepted=json.loads((ROOT/'results/revision-20261022/evaluation-audit-02.json').read_bytes())
    hashes={r['public_file']:r['sha256'] for r in accepted['receipts']}
    summary_path=ROOT/'results/revision-20261022/evaluation-summary.csv'
    expected_summary=next(r for r in accepted['exports'] if r['path']=='evaluation-summary.csv')
    summary=load_verified_summary(summary_path,expected_summary)
    summary_by_key={(r['source'],int(r['horizon']),int(r['window']),r['method']):r for r in summary}
    arrays={};inputs=[];floor_rows=[]
    for cell in expected_cells(spec):
        phase,s,h,w,family=cell
        name=f'evaluation-{s}-h{h}-w{w}-{family}.json' if family else f'references-{s}-h{h}-w{w}.json'
        raw=(ROOT/'results/revision-20261022'/name).read_bytes()
        assert_same(hashlib.sha256(raw).hexdigest(),hashes[name],'accepted public receipt')
        receipt=json.loads(raw)
        assert_same(receipt['status'],'COMPLETE','diagnostic input complete')
        trace_path=ROOT/receipt_path(cell).parent.parent/'private/numeric-traces.npz'
        trace_raw=trace_path.read_bytes();artifact=receipt['artifacts'][0]
        with verified_archive(trace_raw,artifact) as archive:
            for row in receipt['result']['summary_rows']:
                method=row['method'];key=(s,h,w,method)
                ids=archive[method+'_origins'].copy();p=archive[method+'_peak'].copy()
                c=archive[method+'_capacity'].copy();b=archive[method+'_floor'].copy()
                assert_same(runner._origin_identity(ids),receipt['result']['origin_identity'],'diagnostic origins')
                metadata=summary_by_key[key]
                floor_rows.append(dict(source=s,native_unit=spec['sources'][s]['native_unit'],horizon=h,
                    window=w,method=method,parameter=metadata['parameter'])|floor_diagnostics(p,c,b))
                arrays[key]=dict(origins=ids,peak=p,capacity=c,floor=b,parameter=metadata['parameter'])
        inputs.append(dict(receipt=name,receipt_sha256=hashes[name],private_archive_sha256=artifact['sha256']))
        guard.arrays(arrays);guard(stage='diagnostic_receipt_checked')
    horizon_rows=[]
    for (s,h,w,method),short in arrays.items():
        if h!=6:continue
        long=arrays[s,24,w,method]
        if not np.array_equal(short['origins'],long['origins']) or not np.array_equal(short['floor'],long['floor']):
            raise ValueError('horizon diagnostic issue/floor mismatch')
        horizon_rows.append(dict(source=s,native_unit=spec['sources'][s]['native_unit'],window=w,method=method,
            parameter_h6=short['parameter'],parameter_h24=long['parameter'])|
            horizon_diagnostics(short['capacity'],long['capacity'],short['peak'],long['peak']))
    assert_same((len(floor_rows),len(horizon_rows)),(90,45),'complete diagnostic inventory')
    runner.verify_executable_freeze(FREEZE);assert_same(plan.read_bytes(),plan_raw,'diagnostic plan unchanged')
    output=ROOT/'results/revision-20261022'
    names=('post-result-floor.csv','post-result-horizon.csv')
    for name,rows in zip(names,(floor_rows,horizon_rows)):write_csv(output/name,rows)
    guard(stage='post_result_diagnostics_final')
    audit=dict(version=1,status='VERIFIED',created_utc=utc_now(),analysis_status='EXPLICITLY_POST_RESULT_DESCRIPTIVE',
        scope='All90accepted reports and45same-source/window/method horizon pairs; no refit or forecast repair',
        executable_freeze_sha256=FREEZE,selection_freeze_sha256=SELECTION,
        plan=dict(path=str(plan.relative_to(ROOT)),sha256=hashlib.sha256(plan_raw).hexdigest()),
        floor_rows=len(floor_rows),horizon_rows=len(horizon_rows),input_receipts=inputs,
        resources=dict(guard.resources),builder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        exports=[dict(path=name,bytes=(output/name).stat().st_size,sha256=hashlib.sha256((output/name).read_bytes()).hexdigest()) for name in names],
        output_counter_scope='Guard tree counters cover this audit attempt; export bytes are listed separately')
    with (output/'post-result-diagnostics-audit.json').open('x') as stream:json.dump(audit,stream,indent=2);stream.write('\n')
    signal.setitimer(signal.ITIMER_REAL,0)
    print(json.dumps(dict(status=audit['status'],floor_rows=len(floor_rows),horizon_rows=len(horizon_rows),resources=guard.resources),indent=2))


if __name__=='__main__':main()
