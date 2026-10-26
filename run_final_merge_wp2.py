"""Once-only CFTC W520 extension; never writes inherited study directories."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PROTOCOL = 'protocol/final-merge/wp2-cftc-mechanism.md'
SEAL = 'protocol/final-merge/wp2-input-seal.json'
OUTPUT = 'results/final-merge/wp2-cftc-mechanism'
METHODS = ('F', 'QR4', 'QR33')


def now(): return datetime.now(timezone.utc).isoformat()
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_text())
def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def preflight():
    """Hash/read-only geometry checks; deliberately no forecast import/call."""
    import numpy as np
    from final_merge_wp2 import split_geometry
    sources = read(ROOT/'results/v10/cftc/sources.json')
    inherited = read(ROOT/'results/v10/cftc/manifest.json')
    roots = read(ROOT/'notes/revision-v9/wp1-breakeven.json')
    inputs = []
    paths = [PROTOCOL, 'results/v10/cftc/sources.json', 'results/v10/cftc/manifest.json',
        'results/v10/cftc/formal/units.zip', 'results/v10/cftc/formal/units-manifest.json',
        'results/v10/cftc/formal/completion.json', 'notes/revision-v9/wp1-breakeven.json',
        'run_final_merge_wp2.py', 'verify_final_merge_wp2.py', 'final_merge_wp2.py',
        'test_final_merge_wp2.py', 'inference_tests.py', 'v9_learning_curve.py']
    paths += list(inherited['code_sha256'])
    source_rows = []
    for s in sources:
        path = ROOT/s['path']
        if sha(path) != s['sha256'] or path.stat().st_size != s['bytes']:
            raise ValueError('SOURCE_HASH_MISMATCH')
        with np.load(path, allow_pickle=False) as a:
            x, t, actual = a['position'], a['model_dates'], a['actual_dates']
            if (len(x) != 877 or not np.isfinite(x).all() or t.shape != x.shape
                    or actual.shape != x.shape or np.any(np.diff(t) != np.timedelta64(7, 'D'))):
                raise ValueError('SOURCE_GEOMETRY_MISMATCH')
            geometry = split_geometry(len(x), 6, 520)
            source_rows.append(dict(source_index=s['source_index'], code=s['code'], N=len(x),
                **geometry, model_first=str(t[0]), model_last=str(t[-1]),
                actual_first=str(actual[0]), actual_last=str(actual[-1])))
        paths.append(s['path'])
        for w in (52, 260):
            for method in METHODS:
                paths.append(f"results/v10/cftc/complete-traces/s{s['source_index']:02d}-W{w}-{method}.npz")
    for path in sorted(set(paths)):
        p = ROOT/path
        inputs.append(dict(path=path, bytes=p.stat().st_size, sha256=sha(p)))
    rstar = {m:dict(point=roots['methods'][m]['point']['r_star'],
        interval=roots['methods'][m]['intervals']['all_draw_envelope']) for m in METHODS[1:]}
    seal = dict(schema='final-merge-wp2-prerun-seal-v1', created_utc=now(),
        no_model_fits=True, result_directory_exists=(ROOT/OUTPUT).exists(),
        source_count=len(sources), planned_new_cells=len(sources)*len(METHODS),
        planned_comparisons=len(sources)*3*2, horizon=6, windows=[52,260,520],
        rstar=rstar, source_geometry=source_rows, inputs=inputs,
        original_run_seconds=read(ROOT/'results/v10/cftc/formal/completion.json')['elapsed_seconds'],
        estimated_seconds=123, global_budget_seconds=1800, internal_source_seconds=90,
        hard_source_seconds=120, single_numerical_thread=True)
    if seal['result_directory_exists']:
        raise ValueError('WP2_OUTPUT_ALREADY_EXISTS_BEFORE_REGISTRATION')
    write(ROOT/SEAL, seal)
    print(json.dumps(dict(status='PASS',source_count=len(sources),input_files=len(inputs),
        all_sources_520_eligible=True,new_model_fits=0,old_result_writes=0,
        seal=SEAL,seal_sha256=sha(ROOT/SEAL)), indent=2))


def check_seal():
    seal = read(ROOT/SEAL)
    bad = [r['path'] for r in seal['inputs'] if sha(ROOT/r['path']) != r['sha256']
           or (ROOT/r['path']).stat().st_size != r['bytes']]
    if bad: raise ValueError('PREREGISTERED_INPUT_CHANGED '+str(bad))
    return seal


def worker(source_index, output):
    import numpy as np
    from conditional_features import build_features
    from conditional_quantile import QuantileFitError
    from conditional_study import score_predictions
    from study_core import build_label_cache, stable_mean
    from run_v8_wp3 import scalar_diagnostics
    from v10_menu import forecast_report, evaluate_method, _native
    from final_merge_wp2 import split_geometry
    class TimeBudget(Exception):
        code = 'SOURCE_INTERNAL_TIME_BUDGET'
    started = time.monotonic()
    check_seal()
    start=read(ROOT/OUTPUT/'start.json')
    if start['protocol_commit'] != subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip():
        raise ValueError('WORKER_REGISTRATION_COMMIT_MISMATCH')
    source = read(ROOT/'results/v10/cftc/sources.json')[source_index]
    output.mkdir(parents=True, exist_ok=False)
    write(output/'start.json',dict(source_index=source_index,code=source['code'],utc=now()))
    def checkpoint(**detail):
        if time.monotonic()-started > 90: raise TimeBudget()
    with np.load(ROOT/source['path'],allow_pickle=False) as arrays:
        x, clock = arrays['position'].copy(), arrays['model_dates'].copy()
    h,w,step = 6,520,13
    g = split_geometry(len(x),h,w)
    write(output/'splits.json', dict(N=len(x),horizon=h,window=w,refit_step=step,**g))
    validation = np.arange(g['validation_first'],g['validation_last']+1,dtype=np.int64)
    evaluation = np.arange(g['evaluation_first'],g['evaluation_last']+1,dtype=np.int64)
    design = dict(read(ROOT/'results/v10/cftc/manifest.json')['design'],
        validation_first=g['validation_first'], validation_last=g['validation_last'])
    features = build_features(x,clock,short_scale=6,long_scale=26,nominal_gap_seconds=604800)
    labels = build_label_cache(x,h)
    cache = {}
    def segment(ids,method,penalty):
        key=(method,penalty,int(ids[0]),int(ids[-1]))
        if key not in cache:
            try:
                cache[key]=forecast_report(x,clock,features,labels,ids,h,w,step,method,penalty,
                    checkpoint=checkpoint)
            except Exception as exc:
                cache[key]=exc
                raise
        r=cache[key]
        if isinstance(r,Exception): raise r
        if not np.array_equal(ids,r['origins']): raise ValueError('ORIGIN_AXIS_MISMATCH')
        return r
    def trace(ids,capacity):
        score=score_predictions(labels.peak[ids],capacity,np.abs(x[ids]),ids)
        return dict(origins=ids.copy(),capacities=score.capacities.copy(),peak=labels.peak[ids].copy(),
            floor=score.floors.copy(),pinball=score.pinball.copy(),strict_breach=score.strict_breach.copy(),
            overrun=score.overrun.copy(),unused=score.unused.copy())
    def report(segment_name,horizon,window,method,penalty):
        if (horizon,window)!=(h,w): raise ValueError('GEOMETRY_MISMATCH')
        ids=validation if segment_name=='validation' else evaluation
        prediction=segment(ids,method,penalty)
        t=trace(ids,prediction['capacity'])
        if segment_name=='validation':
            path=output/f'validation-{method}-{str(penalty)}.npz'
            with path.open('xb') as f:np.savez_compressed(f,**t)
        score=dict(mean_loss=stable_mean(t['pinball']),n=len(ids),
            strict_breach_count=int(np.count_nonzero(t['strict_breach'])),
            strict_breach_rate=float(np.mean(t['strict_breach'])))
        return score,scalar_diagnostics(prediction['fit_diagnostics'])
    methods=[]
    for method in METHODS:
        checkpoint()
        receipt=evaluate_method(design,output,w,h,method,report,checkpoint,QuantileFitError,(TimeBudget,))
        row=dict(method=method,status=receipt['status'],reason=receipt['reason'],
            selected_penalty=receipt['selected_penalty'])
        if receipt['status']=='COMPLETE':
            prediction=segment(evaluation,method,row['selected_penalty'])
            t=trace(evaluation,prediction['capacity'])
            path=output/f'trace-{method}.npz'
            with path.open('xb') as f:np.savez_compressed(f,**t)
            row.update(**receipt['evaluation'],trace_path=path.name,trace_sha256=sha(path),
                trace_bytes=path.stat().st_size)
        write(output/f'result-{method}.json',_native(row));methods.append(row)
    write(output/'complete.json',dict(ended_utc=now(),elapsed_seconds=time.monotonic()-started,
        source_index=source_index,methods=methods))


def collect(output, seal):
    import numpy as np
    from final_merge_wp2 import screen, strict_decrease, primary_status
    from v9_learning_curve import dm_hac_only
    sources=read(ROOT/'results/v10/cftc/sources.json')
    cells=[];comparisons=[]
    with zipfile.ZipFile(ROOT/'results/v10/cftc/formal/units.zip') as old:
        for source in sources:
            si=source['source_index']
            for w in (52,260,520):
                for method in METHODS:
                    origin='ARCHIVED_UNCHANGED' if w<520 else 'NEW_W520'
                    if w<520:
                        receipt=json.loads(old.read(f's{si:02d}/W{w}/result-{method}.json'))
                        trace_path=ROOT/f'results/v10/cftc/complete-traces/s{si:02d}-W{w}-{method}.npz'
                    else:
                        p=output/f'units/s{si:02d}/result-{method}.json'
                        receipt=read(p) if p.exists() else dict(status='NA',reason='SOURCE_UNCOMPLETED',
                            mean_loss=None,strict_breach_count=None,n=None,selected_penalty=None)
                        trace_path=p.parent/f'trace-{method}.npz'
                    if receipt['status']=='COMPLETE' and sha(trace_path)!=receipt['trace_sha256']:
                        raise ValueError('TRACE_RECEIPT_SHA_MISMATCH')
                    cell=dict(source_index=si,code=source['code'],window=w,horizon=6,method=method,
                        origin=origin,status=receipt['status'],reason=receipt.get('reason'),
                        n=receipt.get('n'),mean_loss=receipt.get('mean_loss'),
                        strict_breach_count=receipt.get('strict_breach_count'),
                        selected_penalty=receipt.get('selected_penalty'),
                        trace_path=str(trace_path.relative_to(ROOT)) if trace_path.exists() else None,
                        trace_sha256=sha(trace_path) if trace_path.exists() else None)
                    cells.append(cell)
                group=cells[-3:];f=group[0]
                for model in group[1:]:
                    row=dict(source_index=si,code=source['code'],window=w,horizon=6,
                        c=w/7,method=model['method'],status='NA',reason='INCOMPLETE_MATCHED_PAIR',
                        relative_loss_percent=None,reference_loss=f['mean_loss'],model_loss=model['mean_loss'],
                        reference_breach_count=f['strict_breach_count'],model_breach_count=model['strict_breach_count'],
                        dm=None,selected_penalty=model['selected_penalty'])
                    if f['status']==model['status']=='COMPLETE' and f['mean_loss']>0:
                        with np.load(ROOT/f['trace_path'],allow_pickle=False) as ft,np.load(ROOT/model['trace_path'],allow_pickle=False) as mt:
                            if not np.array_equal(ft['origins'],mt['origins']):raise ValueError('PAIR_AXIS_MISMATCH')
                            dm=dm_hac_only(mt['pinball']-ft['pinball'],6)
                        row.update(status='COMPLETE',reason=None,
                            relative_loss_percent=100*(model['mean_loss']/f['mean_loss']-1),dm=dm)
                    comparisons.append(row)
    tests={};counterexamples=[]
    for method in METHODS[1:]:
        point=seal['rstar'][method]['point']
        for name,region,predicate,threshold in [('P1',lambda c:c<point/2,lambda d:d>0,.8),
                ('P2',lambda c:c>2*point,lambda d:d<0,.6)]:
            selected=[r for r in comparisons if r['method']==method and region(r['c'])]
            key=name+'_'+method
            if not selected:tests[key]=dict(status='NOT_TESTABLE',reason='NO_REGISTERED_REGION_CELL',planned=0)
            else:
                outcomes=[None if r['relative_loss_percent'] is None else predicate(r['relative_loss_percent']) for r in selected]
                tests[key]=screen(outcomes,threshold)
                for r,v in zip(selected,outcomes):
                    if v is not True:counterexamples.append(dict(screen=key,kind='UNKNOWN' if v is None else 'COUNTEREXAMPLE',**r))
    curves=[]
    for s in sources:
        values=[next(r['relative_loss_percent'] for r in comparisons if r['source_index']==s['source_index'] and r['window']==w and r['method']=='QR4') for w in (52,260,520)]
        success=strict_decrease(values)
        curves.append(dict(source_index=s['source_index'],code=s['code'],windows=[52,260,520],relative_losses=values,strictly_decreasing=success))
        if success is not True:counterexamples.append(dict(screen='P3_QR4',kind='UNKNOWN' if success is None else 'COUNTEREXAMPLE',**curves[-1]))
    tests['P3_QR4']=screen([r['strictly_decreasing'] for r in curves],.7)
    verdict=primary_status(tests['P1_QR33']['status'],tests['P1_QR4']['status'],tests['P2_QR4']['status'])
    result=dict(schema='final-merge-wp2-results-v1',created_utc=now(),primary_verdict=verdict,
        tests=tests,cells=cells,comparisons=comparisons,curves=curves,counterexamples=counterexamples,
        method='fixed source and window counts; no multiplicity-adjusted significance claim',
        old_science_recomputed=False,independent_verification='PENDING')
    write(output/'summary.json',result)
    for name,rows in [('cells',cells),('comparisons',comparisons)]:
        flattened=[{k:(json.dumps(v,sort_keys=True) if isinstance(v,dict) else v) for k,v in r.items()} for r in rows]
        with (output/f'{name}.csv').open('x',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(flattened[0]));writer.writeheader();writer.writerows(flattened)
    print(json.dumps(dict(primary_verdict=verdict,tests=tests,cells=len(cells),comparisons=len(comparisons),
        counterexamples_or_unknown=len(counterexamples)),indent=2))


def execute():
    seal=check_seal()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)
    if branch!='final-jof' or dirty:raise ValueError('CLEAN_FINAL_JOF_REQUIRED')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    for path in (PROTOCOL,SEAL):
        committed=subprocess.check_output(['git','show',f'{head}:{path}'],cwd=ROOT)
        if committed!=(ROOT/path).read_bytes():raise ValueError('UNCOMMITTED_REGISTRATION')
    output=ROOT/OUTPUT
    output.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    write(output/'start.json',dict(utc=now(),protocol_commit=head,protocol_sha256=sha(ROOT/PROTOCOL),
        input_seal_sha256=sha(ROOT/SEAL),command=sys.argv,branch=branch))
    tasks=[]
    for source in read(ROOT/'results/v10/cftc/sources.json'):
        si=source['source_index']
        if time.monotonic()-started>=1800:
            tasks.append(dict(source_index=si,status='UNSTARTED_GLOBAL_BUDGET',elapsed_seconds=0));continue
        t=time.monotonic()
        command=[sys.executable,'-B',str(Path(__file__).resolve()),'--worker',str(si)]
        status='RETURNED';code=None
        try:
            p=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=120)
            text=p.stdout;code=p.returncode
        except subprocess.TimeoutExpired as exc:
            status='HARD_TIMEOUT';text=str(exc.stdout or '')
        write(output/f'worker-{si:02d}.json',dict(source_index=si,command=command,status=status,
            returncode=code,elapsed_seconds=time.monotonic()-t,stdout=text))
        tasks.append(dict(source_index=si,status=status,returncode=code,elapsed_seconds=time.monotonic()-t))
        print(f'source={si:02d} status={status} exit={code} elapsed={time.monotonic()-t:.3f}',flush=True)
    check_seal()
    write(output/'completion.json',dict(ended_utc=now(),elapsed_seconds=time.monotonic()-started,tasks=tasks))
    collect(output,seal)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--execute',action='store_true');parser.add_argument('--worker',type=int)
    args=parser.parse_args()
    if sum((args.preflight,args.execute,args.worker is not None))!=1:parser.error('exactly one action')
    if args.preflight:preflight()
    elif args.execute:execute()
    else:worker(args.worker,ROOT/OUTPUT/f'units/s{args.worker:02d}')
