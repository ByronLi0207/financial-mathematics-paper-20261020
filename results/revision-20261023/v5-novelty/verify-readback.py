"""Independent scalar readback; no fits, mutations, fetching or source edits.

Run from the repository root using the existing numeric Python. An output path
is optional; when supplied it must not exist. Private traces are verified using
the immutable public receipt's hashes. This script does not redistribute them.
"""
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks=[]
    for source,w in (('fx_hourly',2880),('nyfed_weekly',260)):
        resultpath=HERE/f'label-maturity-{source}.json'
        result=json.loads(resultpath.read_text())
        ids=np.concatenate([np.arange(b['first'],b['last']+1) for b in result['block_ranges']])
        for row in result['rows']:
            method=row['method'];prefix=method if method!='F' else 'frozen_F'
            stem=f'evaluation-{source}-h6-w{w}-{method}' if method!='F' else f'references-{source}-h6-w{w}'
            receiptpath=ROOT/'results/revision-20261022'/f'{stem}.json'
            receipt=json.loads(receiptpath.read_text())
            trace=ROOT/'.scratch/revision-20261022/replication-revision-v3-b5-full'/stem/'private/numeric-traces.npz'
            artifact=receipt['artifacts'][0]
            assert trace.stat().st_size==artifact['bytes'] and digest(trace)==artifact['sha256']
            with np.load(trace,allow_pickle=False) as z:
                oldids=z[prefix+'_origins'];indices=np.searchsorted(oldids,ids)
                assert np.array_equal(oldids[indices],ids)
                peak=z[prefix+'_peak'][indices];capacity=z[prefix+'_capacity'][indices]
                floor=z[prefix+'_floor'][indices]
                err=peak-capacity;u=np.maximum(err,0);v=np.maximum(-err,0)
                loss=.95*u+.05*v
                scalars=dict(origin_count=len(ids),mean_pinball=math.fsum(map(float,loss))/len(ids),
                    mean_capacity=math.fsum(map(float,capacity))/len(ids),
                    mean_positive_overrun=math.fsum(map(float,u))/len(ids),
                    mean_unused_allowance=math.fsum(map(float,v))/len(ids),
                    strict_breach_count=int(np.count_nonzero(err>0)))
                comparisons=[]
                for key,value in scalars.items():
                    actual=row['clean'][key]
                    error=abs(actual-value)
                    tolerance=1e-12*max(1,abs(value))
                    assert error<=tolerance,(source,method,key,actual,value)
                    comparisons.append(dict(field=key,archived_trace_readback=value,new_clean=value if error==0 else actual,
                        absolute_difference=error,tolerance=tolerance))
            checks.append(dict(source=source,method=method,public_receipt=str(receiptpath.relative_to(ROOT)),
                public_receipt_sha256=digest(receiptpath),private_trace_sha256=digest(trace),comparisons=comparisons))
    decomposition=json.loads((HERE/'gain-decomposition.json').read_text())
    r=Fraction(decomposition['original_reference_mean_pinball'])
    f=Fraction(decomposition['matched_reference_mean_pinball'])
    q=Fraction(decomposition['estimator_mean_pinball'])
    assert (f-r)+(q-f)==q-r
    example=json.loads((HERE/'motivating-window-final.json').read_text())
    src=ROOT/'.scratch/revision-20261022/nyfed-PDPOSGS-B.csv'
    assert digest(src)==example['identity']['raw_source_sha256']
    import csv
    with src.open(newline='') as stream:raw=list(csv.DictReader(stream))
    x=[float(row['Value (millions)']) for row in raw]
    e=example['example'];h=e['horizon'];r=e['refit_origin'];w=example['window']
    rank=((w+1)*19+19)//20
    headroom=[max(abs(v) for v in x[i:i+h+1])-abs(x[i]) for i in range(r-h-w+1,r-h+1)]
    capacity=abs(x[e['origin']])+sorted(headroom)[rank-1]
    assert capacity==e['report']
    assert abs(x[e['origin']+h])==e['endpoint_absolute']<=capacity<e['peak']
    assert x[e['origin']:e['origin']+h+1]==e['positions']
    earlier=[]
    for t in range(example['eligible_first_origin'],e['origin']):
        rt=example['eligible_first_origin']+13*((t-example['eligible_first_origin'])//13)
        y=[max(abs(v) for v in x[i:i+h+1])-abs(x[i]) for i in range(rt-h-w+1,rt-h+1)]
        ct=abs(x[t])+sorted(y)[rank-1]
        earlier.append(abs(x[t+h])<=ct<max(abs(v) for v in x[t:t+h+1]))
    assert not any(earlier)
    result=dict(status='PASS',readback='no model refits; independent math.fsum scalar reconstruction from hash-verified original private traces',
        checks=checks,exact_rational_gain_additivity=True,motivating_capacity_recomputed_without_forecast_engine=capacity,
        motivating_earlier_eligible_origins_checked=len(earlier),motivating_is_earliest=True,
        code_sha256=digest(ROOT/'v5_analysis.py'),test_sha256=digest(ROOT/'test_v5_analysis.py'),
        verifier_sha256=digest(Path(__file__)))
    output=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if len(sys.argv)>1:
        with Path(sys.argv[1]).open('x') as stream:stream.write(output)
    print(json.dumps(dict(status=result['status'],trace_method_checks=len(checks),
        scalar_checks=sum(len(c['comparisons']) for c in checks),
        maximum_absolute_clean_readback_difference=max(v['absolute_difference'] for c in checks for v in c['comparisons']),
        exact_rational_gain_additivity=True,motivating_is_earliest=True),indent=2))


if __name__=='__main__':main()
