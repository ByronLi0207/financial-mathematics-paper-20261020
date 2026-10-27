"""Single-attempt G2 driver with committed design/code and hard process caps."""
from __future__ import annotations
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[_k]='1'
import argparse,csv,hashlib,json,re,signal,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
from v12_inputs import source_inventory
from v13_validation import g2_cells,summarize_g2
from v13_validation_runner import write_new

ROOT=Path(__file__).resolve().parent
DESIGN='protocol/v13/nyfed-validation-length-design.md'
DESIGN_COMMIT='d58464ee2bf87f01e7e2625b0888edcd2e442214'
CODE=('run_v13_validation.py','v13_validation_runner.py','v13_validation.py','test_v13_validation.py','report_v13_validation.py')


def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)


def protocol_and_seal():
    raw=(ROOT/DESIGN).read_bytes();d=json.loads(re.search(r'```json\n(.*?)\n```',raw.decode(),re.S).group(1))
    candidates=[DESIGN_COMMIT]+git('log','--format=%H','HEAD','--',DESIGN).decode().splitlines()
    accepted=None
    for commit in dict.fromkeys(candidates):
        ok=subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if ok and git('show',commit+':'+DESIGN)==raw:
            changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()
            if changed==[DESIGN]:accepted=commit;break
    if accepted is None:raise ValueError('EXACT_STANDALONE_DESIGN_ANCESTOR_REQUIRED')
    code={name:sha(ROOT/name) for name in (*CODE,*d['inherited_code_sha256'])}
    for name,digest in code.items():
        if hashlib.sha256(git('show','HEAD:'+name)).hexdigest()!=digest:raise ValueError('UNCOMMITTED_CODE:'+name)
    for name,digest in d['inherited_code_sha256'].items():
        if code[name]!=digest:raise ValueError('INHERITED_MODEL_CHANGED:'+name)
    inventory=ROOT/d['input_inventory_contract']
    if sha(inventory)!=d['input_inventory_contract_sha256']:raise ValueError('INPUT_INVENTORY_CHANGED')
    return d,dict(experiment='G2',design_path=DESIGN,design_commit=accepted,
        design_commit_time=git('show','-s','--format=%cI',accepted).decode().strip(),
        design_sha256=sha(ROOT/DESIGN),code_commit=git('rev-parse','HEAD').decode().strip(),code_sha256=code,sealed_utc=utc())


def stopped_result(cell,method,reason,started=False):
    row={k:v for k,v in cell.items() if k!='source'}
    row.update(method=method,status='FAILED_RESOURCE' if started else 'NOT_RUN_RESOURCE_LIMIT',reason=reason,
        source_sha256=cell['source']['sha256'],selected_penalty=None,actual_loss=None,reference_loss=None,relative_loss_pct=None)
    return dict(row=row,candidates=[],reference={},selection={})


def kill_child(process):
    if process.poll() is None:
        try:os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        process.wait()


def write_csv(path,rows,columns):
    with Path(path).open('x',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');writer.writeheader();writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');args=parser.parse_args()
    if not args.run:raise SystemExit('Explicit --run required; imports/help perform no financial computation.')
    d,seal=protocol_and_seal();out=ROOT/'results/v13/nyfed-validation';private=ROOT/'.scratch/v13/nyfed-validation'
    out.mkdir(parents=True,exist_ok=False);private.mkdir(parents=True,exist_ok=False,mode=0o700)
    start=time.monotonic();deadline=start+d['runtime']['total_cap_seconds'];began=utc()
    write_new(out/'code-seal.json',seal);write_new(out/'formal-start.json',dict(started_utc=began,total_cap_seconds=1800))
    sources=source_inventory(ROOT);preflight=[]
    for source in sources:
        p=Path(source['path']);digest=sha(p)
        if digest!=source['sha256'] or p.stat().st_size!=source['bytes']:raise ValueError('INPUT_BYTES_CHANGED:'+source['key'])
        preflight.append(dict(family=source['family'],source_key=source['key'],sha256=digest,bytes=p.stat().st_size))
    cells=g2_cells(sources)
    if len(cells)!=d['planned_geometry_cells']:raise ValueError('G2_GRID_MISMATCH')
    write_new(out/'input-preflight.json',dict(sources=preflight,geometry_cells=cells,exclusions=[]))
    write_new(out/'resource-plan.json',dict(workers=4,threads_per_worker=1,total_cap_seconds=1800,max_cell_wall_seconds=300,trim_steps=[],planned_methods=104,hard_parent_process_termination=True))
    results=[];counter=0
    for method in ('QR33','QR4'):
        queue=list(cells);active=[]
        while queue or active:
            while queue and len(active)<4 and time.monotonic()<deadline:
                cell=queue.pop(0);job=private/f'job-{counter:03d}';job.mkdir();counter+=1
                spec=dict(cell=cell,method=method,new_cache=str(ROOT/'.scratch/v13/cache'),old_cache=str(ROOT/'.scratch/v12/cache'),
                    private=str(job),deadline_monotonic=min(deadline,time.monotonic()+300),result=str(job/'result.json'),code_sha256=seal['code_sha256'])
                write_new(job/'spec.json',spec)
                log=(job/'console.txt').open('xb')
                process=subprocess.Popen([sys.executable,'-B',str(ROOT/'v13_validation_runner.py'),'--worker',str(job/'spec.json')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                active.append(dict(process=process,cell=cell,method=method,job=job,log=log,began=time.monotonic()))
            for item in list(active):
                expired=time.monotonic()>=deadline or time.monotonic()-item['began']>=300
                if expired:kill_child(item['process'])
                if item['process'].poll() is not None:
                    item['log'].close();path=item['job']/'result.json'
                    if path.exists():result=json.loads(path.read_text())
                    else:result=stopped_result(item['cell'],item['method'],'HARD_PROCESS_CAP' if expired else 'WORKER_FAILED_NO_RESULT',True)
                    result['worker_elapsed_seconds']=time.monotonic()-item['began'];result['worker_exit_code']=item['process'].returncode
                    results.append(result);active.remove(item)
            if time.monotonic()>=deadline and queue:
                results.extend(stopped_result(c,method,'TOTAL_WALL_CAP_BEFORE_START') for c in queue);queue=[]
            if active:time.sleep(.05)
    ended=utc();elapsed=time.monotonic()-start
    rows=[r['row'] for r in results]
    rows.sort(key=lambda r:(r['method']!='QR33',r['horizon'],r['family']!='bill',r['source_key'],r['validation_n']))
    candidates=[dict(cell_id=r['row']['cell_id'],source_key=r['row']['source_key'],horizon=r['row']['horizon'],validation_n=r['row']['validation_n'],**c) for r in results for c in r['candidates']]
    write_new(out/'rows.json',rows);write_new(out/'candidates.json',candidates)
    write_new(out/'cell-results.json',results);summary=summarize_g2(rows);write_new(out/'summary.json',summary)
    write_csv(out/'rows.csv',rows,['cell_id','family','source_key','horizon','window','validation_n','evaluation_n','method','status','reason','selected_penalty','actual_loss','reference_loss','relative_loss_pct'])
    write_csv(out/'candidates.csv',candidates,['cell_id','source_key','horizon','validation_n','segment','method','penalty','status','reason','mean_loss','n','cache_key','cache_source','trace_sha256'])
    write_new(out/'runtime.json',dict(started_utc=began,ended_utc=ended,elapsed_seconds=elapsed,total_cap_seconds=1800,planned_method_cells=104,received_method_cells=len(rows),complete=sum(r['status']=='COMPLETE' for r in rows),failed=sum(r['status'].startswith('FAILED') for r in rows),not_run=sum(r['status'].startswith('NOT_RUN') for r in rows)))
    from report_v13_validation import build_report
    build_report(out)
    write_new(out/'output-manifest.json',{str(p.relative_to(out)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file()})
    print(json.dumps(dict(V3=summary['V3'],V4=summary['V4'],complete=sum(r['status']=='COMPLETE' for r in rows),planned=104,elapsed_seconds=elapsed)))


if __name__=='__main__':main()
