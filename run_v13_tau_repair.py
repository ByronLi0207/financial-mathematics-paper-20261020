"""One-shot G1 repair with a binding saved-forecast consistency gate."""
from __future__ import annotations
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[_k]='1'
import argparse
from datetime import datetime,timezone
import hashlib,json,re,subprocess,time
from pathlib import Path
import numpy as np
from v12_inputs import source_inventory,load_series
from v12_forecast import make_context,score_report
from v13_tau_forecast import predict_segment
from v13_tau_repair import FIT_EVENTS
from study_core import stable_mean
from v12_decomposition import select_candidate

ROOT=Path(__file__).resolve().parent
DESIGN='protocol/v13/tau-solver-repair-design.md'
DESIGN_COMMIT='bad6722d1087b6984cc00d9c4637740af72a11cb'
CODE=('run_v13_tau_repair.py','v13_tau_repair.py','v13_tau_forecast.py','test_v13_tau_repair.py')


def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')


class ResourceStop(Exception):pass


def protocol_and_seal():
    raw=(ROOT/DESIGN).read_bytes()
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
    subprocess.run(['git','merge-base','--is-ancestor',DESIGN_COMMIT,'HEAD'],cwd=ROOT,check=True)
    if git('show',DESIGN_COMMIT+':'+DESIGN)!=raw:raise ValueError('DESIGN_BYTES_CHANGED')
    names=git('diff-tree','--no-commit-id','--name-only','-r',DESIGN_COMMIT).decode().splitlines()
    if names!=[DESIGN]:raise ValueError('DESIGN_NOT_STANDALONE')
    d=json.loads(re.search(r'```json\n(.*?)\n```',raw.decode(),re.S).group(1))
    code={p:sha(ROOT/p) for p in CODE}
    for p,digest in code.items():
        if hashlib.sha256(git('show','HEAD:'+p)).hexdigest()!=digest:raise ValueError('UNCOMMITTED_CODE:'+p)
    for p,digest in d['inherited_code_sha256'].items():
        if sha(ROOT/p)!=digest:raise ValueError('INHERITED_CODE_CHANGED:'+p)
    return d,dict(head=git('rev-parse','HEAD').decode().strip(),design_commit=DESIGN_COMMIT,
        design_commit_time=git('show','-s','--format=%cI',DESIGN_COMMIT).decode().strip(),
        design_path=DESIGN,design_sha256=sha(ROOT/DESIGN),code_sha256=code,sealed_utc=utc())


def evaluate_segment(context,ids,penalty,guard,private,name):
    before=len(FIT_EVENTS)
    p=predict_segment(context,ids,'QR33',penalty,tau=.99,checkpoint=guard)
    scored=score_report(context,ids,p['capacity'],tau=.99)
    path=private/(name+'.npz')
    with path.open('xb') as f:np.savez_compressed(f,origins=ids,capacity=p['capacity'],losses=scored['losses'])
    return dict(status='COMPLETE',mean_loss=scored['mean_loss'],n=len(ids),
        trace_sha256=sha(path),fit_diagnostics=p['fit_diagnostics'],solver_events=FIT_EVENTS[before:])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');args=parser.parse_args()
    if not args.run:raise SystemExit('Explicit --run required; no computation during import/help.')
    d,seal=protocol_and_seal()
    out=ROOT/'results/v13/tau-repair';private=ROOT/'.scratch/v13/tau-repair'
    out.mkdir(parents=True,exist_ok=False);private.mkdir(parents=True,exist_ok=False,mode=0o700)
    start=time.monotonic();deadline=start+d['runtime']['formal_cap_seconds'];began=utc()
    write(out/'code-seal.json',seal);write(out/'formal-start.json',dict(started_utc=began,cap_seconds=1200))
    def guard(**detail):
        if time.monotonic()>=deadline:raise ResourceStop('G1_TOTAL_WALL_CAP')
    sources=source_inventory(ROOT);contexts={}
    oldrows=json.loads((ROOT/'results/v12/tau/rows.json').read_text())
    def context_for(row):
        key=(row['family'],row['source_key'],row['horizon'],row['window'])
        if key not in contexts:
            source=next(s for s in sources if s['family']==row['family'] and s['key']==row['source_key'])
            contexts[key]=make_context(load_series(source,ROOT),row)
        return contexts[key]
    tests=[]
    for j,e in enumerate(d['consistency_examples']):
        item=dict(e);begin=time.monotonic()
        try:
            guard();row=next(x for x in oldrows if x['cell_id']==e['cell_id'])
            context=context_for(row);ids=np.arange(e['query_origins'][0],e['query_origins'][1]+1)
            cached=ROOT/'.scratch/v12/cache'/e['cache_key']
            terminal=json.loads((cached/'terminal.json').read_text())
            trace=cached/'trace.npz'
            if sha(trace)!=terminal['trace_sha256']:raise ValueError('ORIGINAL_TRACE_SHA_CHANGED')
            with np.load(trace,allow_pickle=False) as a:
                loc=np.searchsorted(a['origins'],ids)
                if not np.array_equal(a['origins'][loc],ids):raise ValueError('ORIGINAL_TRACE_ALIGNMENT')
                original=a['capacity'][loc].copy()
            oldcount=len(FIT_EVENTS)
            p=predict_segment(context,ids,'QR33',e['penalty'],tau=.99,checkpoint=guard)
            err=np.abs(p['capacity']-original)/np.maximum(1.,np.abs(original))
            maximum=float(np.max(err));passed=maximum<=d['consistency_max_pointwise_relative_error']
            item.update(status='PASS' if passed else 'FAIL_PREDICTION_DIFFERENCE',
                max_pointwise_relative_error=maximum,threshold=1e-6,
                original_trace_sha256=terminal['trace_sha256'],fit_diagnostics=p['fit_diagnostics'],
                solver_events=FIT_EVENTS[oldcount:])
        except Exception as exc:item.update(status='FAILED_RESOURCE' if isinstance(exc,ResourceStop) else 'FAIL_SOLVER',reason=str(exc),diagnostics=dict(getattr(exc,'diagnostics',{})))
        item['elapsed_seconds']=time.monotonic()-begin;tests.append(item)
        write(out/f'consistency-{j:02d}.json',item)
    gate=all(x['status']=='PASS' for x in tests)
    write(out/'consistency.json',dict(status='PASS' if gate else 'FAIL',n=10,passed=sum(x['status']=='PASS' for x in tests),examples=tests))
    repairs=[]
    for i,cell in enumerate(d['cells']):
        row=dict(cell,status='NOT_RUN_CONSISTENCY_GATE' if not gate else 'FAILED',
            relative_loss_pct=None,selected_penalty=None,actual_loss=None,reference_loss=None,
            reason='REPAIR_NOT_ADOPTABLE' if not gate else None,post_failure_repair=True)
        candidates=[]
        if gate:
            try:
                context=context_for(cell);va=np.arange(cell['validation_first'],cell['validation_last']+1)
                for penalty in d['menu']:
                    candidate=dict(penalty=penalty,n=len(va))
                    try:candidate.update(evaluate_segment(context,va,penalty,guard,private,f'cell-{i}-val-{penalty}'))
                    except Exception as exc:candidate.update(status='FAILED_RESOURCE' if isinstance(exc,ResourceStop) else 'FAILED',reason=str(exc),diagnostics=dict(getattr(exc,'diagnostics',{})))
                    candidates.append(candidate)
                choice=select_candidate(candidates,expected_n=len(va));row['selected_penalty']=choice['penalty']
                write(out/f'cell-{i}-selection.json',dict(selection=choice,candidates=candidates,selected_utc=utc()))
                if choice['status']!='SELECTED':row['reason']='VALIDATION_CANDIDATE_FAILURE'
                else:
                    guard();ev=np.arange(cell['evaluation_first'],cell['evaluation_last']+1)
                    f=predict_segment(context,ev,'F',tau=.99,checkpoint=guard)
                    fs=score_report(context,ev,f['capacity'],tau=.99)
                    evaluation=evaluate_segment(context,ev,choice['penalty'],guard,private,f'cell-{i}-eval')
                    write(out/f'cell-{i}-evaluation.json',evaluation)
                    row.update(status='COMPLETE',reason=None,actual_loss=evaluation['mean_loss'],
                        reference_loss=fs['mean_loss'],relative_loss_pct=100*(evaluation['mean_loss']/fs['mean_loss']-1))
            except Exception as exc:row.update(status='FAILED_RESOURCE' if isinstance(exc,ResourceStop) else 'FAILED',reason=str(exc),diagnostics=dict(getattr(exc,'diagnostics',{})))
        row['candidates']=candidates;repairs.append(row);write(out/f'cell-{i}-result.json',row)
    combined=[dict(x) for x in oldrows if x['tau']==.99]
    for repaired in repairs:
        if repaired['status']=='COMPLETE':combined=[repaired if x['cell_id']==repaired['cell_id'] else x for x in combined]
    cftc=[x for x in combined if x['family']=='cftc'];complete=[x for x in cftc if x['status']=='COMPLETE']
    wins=sum(x['relative_loss_pct']>0 for x in complete);unknown=34-len(complete)
    q1='SUPPORTED' if wins>=29 else 'NOT_SUPPORTED' if wins+unknown<29 else 'UNDETERMINED'
    fx=[x for x in combined if x['family']=='fx']
    q2='NOT_SUPPORTED' if any(x['status']=='COMPLETE' and x['relative_loss_pct']>=0 for x in fx) else 'SUPPORTED' if all(x['status']=='COMPLETE' and x['relative_loss_pct']<0 for x in fx) else 'UNDETERMINED'
    write(out/'rows.json',repairs)
    write(out/'summary.json',dict(consistency_gate='PASS' if gate else 'FAIL',repairs=repairs,
        original_Q1='UNDETERMINED',original_Q2='UNDETERMINED',post_failure_Q1=q1,post_failure_Q2=q2,
        cftc_F_strict_wins=wins,cftc_unknown=unknown,
        interpretation='Original v12 findings unchanged; separate after-failure numerical repair only.'))
    write(out/'runtime.json',dict(started_utc=began,ended_utc=utc(),elapsed_seconds=time.monotonic()-start,formal_cap_seconds=1200))
    manifest={p.name:sha(p) for p in out.iterdir() if p.is_file()}
    write(out/'output-manifest.json',manifest)
    print(json.dumps(dict(consistency_gate=gate,post_failure_Q1=q1,post_failure_Q2=q2,elapsed_seconds=time.monotonic()-start)))


if __name__=='__main__':main()
