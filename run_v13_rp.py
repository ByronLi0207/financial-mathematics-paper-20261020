"""Bounded single-attempt v13 RP study, fixed before financial computation."""
from __future__ import annotations
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[_k]='1'
import argparse,hashlib,json,re,signal,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
from v12_inputs import source_inventory
from v13_rp import rp_cells,summarize_rp
from v13_validation_runner import write_new
from run_v13_validation import write_csv

ROOT=Path(__file__).resolve().parent
DESIGN='protocol/v13/recommended-protocol-design.md'
DESIGN_COMMIT='99a912ccf6911da2f54627a7b4b57fb7541b6673'
CODE=('run_v13_rp.py','v13_rp_runner.py','v13_rp.py','report_v13_rp.py','test_v13_rp.py','v13_validation_runner.py','run_v13_validation.py','v13_validation.py')


def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)


def protocol_and_seal():
    raw=(ROOT/DESIGN).read_bytes();d=json.loads(re.search(r'```json\n(.*?)\n```',raw.decode(),re.S).group(1))
    candidates=[DESIGN_COMMIT]+git('log','--format=%H','HEAD','--',DESIGN).decode().splitlines();accepted=None
    for commit in dict.fromkeys(candidates):
        ok=subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if ok and git('show',commit+':'+DESIGN)==raw:
            if git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()==[DESIGN]:accepted=commit;break
    if accepted is None:raise ValueError('EXACT_STANDALONE_DESIGN_ANCESTOR_REQUIRED')
    code={name:sha(ROOT/name) for name in (*CODE,*d['inherited_code_sha256'])}
    for name,digest in code.items():
        if hashlib.sha256(git('show','HEAD:'+name)).hexdigest()!=digest:raise ValueError('UNCOMMITTED_CODE:'+name)
    for name,digest in d['inherited_code_sha256'].items():
        if code[name]!=digest:raise ValueError('INHERITED_MODEL_CHANGED:'+name)
    if sha(ROOT/d['input_inventory_contract'])!=d['input_inventory_contract_sha256']:raise ValueError('INPUT_INVENTORY_CHANGED')
    return d,dict(experiment='G3',design_path=DESIGN,design_commit=accepted,
        design_commit_time=git('show','-s','--format=%cI',accepted).decode().strip(),design_sha256=sha(ROOT/DESIGN),
        code_commit=git('rev-parse','HEAD').decode().strip(),code_sha256=code,sealed_utc=utc())


def stopped_result(cell,reason,started=False):
    row={k:v for k,v in cell.items() if k!='source'}
    status='FAILED_RESOURCE' if started else 'NOT_RUN_RESOURCE_LIMIT'
    row.update(status=status,rp_status=status,ordinary_status=status,F_status=status,rp_reason=reason,ordinary_reason=reason,
        source_sha256=cell['source']['sha256'],route=None,route_qr_indicator=None,long_selected_penalty=None,ordinary_selected_penalty=None,
        reference_loss=None,rp_loss=None,ordinary_loss=None,rp_relative_loss_pct=None,ordinary_relative_loss_pct=None)
    return dict(row=row,candidates=[],references={},choices={},gate={})


def kill_child(process):
    if process.poll() is None:
        try:os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        process.wait()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');args=parser.parse_args()
    if not args.run:raise SystemExit('Explicit --run required; no financial computation during import/help.')
    d,seal=protocol_and_seal();out=ROOT/'results/v13/recommended-protocol';private=ROOT/'.scratch/v13/recommended-protocol'
    out.mkdir(parents=True,exist_ok=False);private.mkdir(parents=True,exist_ok=False,mode=0o700)
    start=time.monotonic();deadline=start+d['runtime']['total_cap_seconds'];began=utc()
    write_new(out/'code-seal.json',seal);write_new(out/'formal-start.json',dict(started_utc=began,total_cap_seconds=2700))
    sources=source_inventory(ROOT);preflight=[]
    for source in sources:
        p=Path(source['path']);digest=sha(p)
        if digest!=source['sha256'] or p.stat().st_size!=source['bytes']:raise ValueError('INPUT_BYTES_CHANGED:'+source['key'])
        preflight.append(dict(family=source['family'],source_key=source['key'],sha256=digest,bytes=p.stat().st_size))
    cells=rp_cells(sources)
    if len(cells)!=62 or sum(c['family']!='fx' for c in cells)!=60:raise ValueError('FIXED_G3_GRID_MISMATCH')
    write_new(out/'input-preflight.json',dict(sources=preflight,cells=cells,exclusions=[{k:v for k,v in c.items() if k!='source'} for c in cells if not c['eligible']]))
    write_new(out/'resource-plan.json',dict(workers=4,threads_per_worker=1,total_cap_seconds=2700,max_cell_wall_seconds=300,trim_steps=[],planned_geometries=62,hard_parent_process_termination=True))
    queue=list(cells);active=[];results=[];counter=0
    while queue or active:
        while queue and len(active)<4 and time.monotonic()<deadline:
            cell=queue.pop(0);job=private/f'job-{counter:03d}';job.mkdir();counter+=1
            spec=dict(cell=cell,new_cache=str(ROOT/'.scratch/v13/cache'),old_cache=str(ROOT/'.scratch/v12/cache'),private=str(job),
                deadline_monotonic=min(deadline,time.monotonic()+300),result=str(job/'result.json'),code_sha256=seal['code_sha256'])
            write_new(job/'spec.json',spec);log=(job/'console.txt').open('xb')
            process=subprocess.Popen([sys.executable,'-B',str(ROOT/'v13_rp_runner.py'),'--worker',str(job/'spec.json')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            active.append(dict(process=process,cell=cell,job=job,log=log,began=time.monotonic()))
        for item in list(active):
            expired=time.monotonic()>=deadline or time.monotonic()-item['began']>=300
            if expired:kill_child(item['process'])
            if item['process'].poll() is not None:
                item['log'].close();path=item['job']/'result.json'
                result=json.loads(path.read_text()) if path.exists() else stopped_result(item['cell'],'HARD_PROCESS_CAP' if expired else 'WORKER_FAILED_NO_RESULT',True)
                result.update(worker_elapsed_seconds=time.monotonic()-item['began'],worker_exit_code=item['process'].returncode)
                results.append(result);active.remove(item)
        if time.monotonic()>=deadline and queue:
            results.extend(stopped_result(c,'TOTAL_WALL_CAP_BEFORE_START') for c in queue);queue=[]
        if active:time.sleep(.05)
    ended=utc();elapsed=time.monotonic()-start
    position={c['cell_id']:i for i,c in enumerate(cells)};results.sort(key=lambda x:position[x['row']['cell_id']])
    rows=[r['row'] for r in results]
    candidates=[dict(cell_id=r['row']['cell_id'],source_key=r['row']['source_key'],family=r['row']['family'],period=r['row']['period'],horizon=r['row']['horizon'],window=r['row']['window'],**c) for r in results for c in r['candidates']]
    refs=[dict(cell_id=r['row']['cell_id'],segment=segment,**{k:v for k,v in ref.items() if k!='segment'}) for r in results for segment,ref in r['references'].items()]
    write_new(out/'rows.json',rows);write_new(out/'candidates.json',candidates);write_new(out/'references.json',refs)
    write_new(out/'selections.json',[dict(cell_id=r['row']['cell_id'],choices=r['choices'],gate=r['gate'],choice_sealed_utc=r['row'].get('choice_sealed_utc')) for r in results])
    write_new(out/'cell-results.json',results);summary=summarize_rp(rows);write_new(out/'summary.json',summary)
    write_csv(out/'rows.csv',rows,['cell_id','family','source_key','period','horizon','window','validation_n','baseline_validation_n','evaluation_n','eligible','status','rp_status','ordinary_status','F_status','rp_reason','ordinary_reason','long_selected_penalty','ordinary_selected_penalty','route','route_qr_indicator','reference_loss','rp_loss','ordinary_loss','rp_relative_loss_pct','ordinary_relative_loss_pct','gate_status','gate_mean_difference','gate_standard_error','gate_bandwidth','gate_lrv','choice_sealed_utc'])
    write_csv(out/'candidates.csv',candidates,['cell_id','family','source_key','period','horizon','window','segment','method','penalty','status','reason','mean_loss','n','cache_key','cache_source','trace_sha256'])
    write_new(out/'runtime.json',dict(started_utc=began,ended_utc=ended,elapsed_seconds=elapsed,total_cap_seconds=2700,planned_geometries=62,received_geometries=len(rows),complete=sum(r['status']=='COMPLETE' for r in rows),rp_complete=sum(r['rp_status']=='COMPLETE' for r in rows),ordinary_complete=sum(r['ordinary_status']=='COMPLETE' for r in rows),failed=sum(r['status'].startswith('FAILED') for r in rows)))
    from report_v13_rp import build_report
    build_report(out)
    write_new(out/'output-manifest.json',{str(p.relative_to(out)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file()})
    print(json.dumps(dict(R1=summary['R1'],R2=summary['R2'],R3=summary['R3'],complete=sum(r['status']=='COMPLETE' for r in rows),planned=62,elapsed_seconds=elapsed)))


if __name__=='__main__':main()
