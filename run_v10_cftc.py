"""Preregistered official TFF replay; acquisition itself is documented browser I/O."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import csv,hashlib,json,math,os,re,signal,subprocess,sys,time,zipfile
from pathlib import Path
from run_v10_menu import committed_file,git
from run_v9_nonstationarity import atomic_json,load,save,sha,utc_now

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'results/v10/cftc'
PRIVATE=ROOT/'.scratch/v10/cftc'
PROTOCOL='protocol/v10/cftc-design.md'
DESIGN_COMMIT='acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf'
INGESTION_PROTOCOL='protocol/v10/cftc-ingestion-clarification.md'
INGESTION_COMMIT='4d46550c23a54662112979acc891ba4f903dc39c'
COUNT_PROTOCOL='protocol/v10/cftc-count-notation-clarification.md'
COUNT_COMMIT='818b942b1bc7d9cbb29329c9c1d8884376242769'
CODE=('run_v10_cftc.py','v10_cftc_data.py','v10_cftc_forecast.py','v10_cftc_summary.py')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')


def read_design():
    committed_file(ROOT/PROTOCOL,DESIGN_COMMIT,True)
    d=json.loads(re.search(r'```json\n(.*?)\n```',(ROOT/PROTOCOL).read_text(),re.S).group(1))
    for p,digest in d['inherited_or_E1_code_sha256'].items():
        if sha(ROOT/p)!=digest:raise ValueError('FROZEN_CODE_CHANGED:'+p)
    if sha(ROOT/d['source_preflight'])!=d['source_preflight_sha256']:raise ValueError('SOURCE_PREFLIGHT_CHANGED')
    provenance=committed_file(ROOT/INGESTION_PROTOCOL,INGESTION_COMMIT,True)
    clarification=json.loads(re.search(r'```json\n(.*?)\n```',(ROOT/INGESTION_PROTOCOL).read_text(),re.S).group(1))
    if clarification['original_design_commit']!=DESIGN_COMMIT or clarification['original_design_sha256']!=sha(ROOT/PROTOCOL):raise ValueError('INGESTION_ORIGINAL_DESIGN_MISMATCH')
    if sha(ROOT/clarification['initial_preparation_failure'])!=clarification['initial_failure_sha256']:raise ValueError('INITIAL_PREPARATION_FAILURE_CHANGED')
    d['ingestion_clarification']=clarification
    d['ingestion_clarification_provenance']=provenance
    count_provenance=committed_file(ROOT/COUNT_PROTOCOL,COUNT_COMMIT,True)
    count_clarification=json.loads(re.search(r'```json\n(.*?)\n```',(ROOT/COUNT_PROTOCOL).read_text(),re.S).group(1))
    if count_clarification['original_design_commit']!=DESIGN_COMMIT or count_clarification['date_clarification_commit']!=INGESTION_COMMIT:raise ValueError('COUNT_CLARIFICATION_DESIGN_MISMATCH')
    for name,digest in [('prior_universe_receipt','prior_universe_sha256'),('prior_unavailable_receipt','prior_unavailable_sha256')]:
        prior=PUBLIC/'preparation-after-clarification'/Path(count_clarification[name]).name
        if sha(prior)!=count_clarification[digest]:raise ValueError('PRESERVED_PRECOUNT_RECEIPT_CHANGED')
    d['count_notation_clarification']=count_clarification
    d['count_notation_clarification_provenance']=count_provenance
    return d


def verify_acquisition(provenance,design,root=ROOT):
    root=Path(root);entries=provenance['files'];expected=design['downloads_in_fixed_order']
    if provenance.get('status')!='ALL_REQUIRED_FILES_DOWNLOADED' or provenance.get('download_attempts')!=len(expected) or provenance.get('failed_attempts')!=0:raise ValueError('REQUIRED_ACQUISITION_UNAVAILABLE')
    if [x['url'] for x in entries]!=[x['url'] for x in expected]:raise ValueError('OFFICIAL_URL_ORDER_MISMATCH')
    stamp=datetime.fromisoformat(provenance['design_commit_time']);paths=[]
    for row in entries:
        if row['status']!='DOWNLOADED' or datetime.fromisoformat(row['started_utc'].replace('Z','+00:00'))<=stamp:raise ValueError('DOWNLOAD_FAILED_OR_PREMATURE')
        path=root/row['local_path']
        if path.is_symlink() or not path.is_file() or path.stat().st_size!=row['bytes'] or sha(path)!=row['sha256']:raise ValueError('ACQUIRED_BYTES_MISMATCH')
        paths.append(path)
    return paths


def verify_sources(sources,root=ROOT):
    for row in sources:
        path=Path(root)/row['path']
        if path.is_symlink() or not path.is_file() or path.stat().st_size!=row['bytes'] or sha(path)!=row['sha256']:raise ValueError('PREPARED_SOURCE_BYTES_CHANGED')
    return True


def split_receipt(calendar,actual_dates,design):
    from v10_cftc_data import split_indices
    N=len(calendar);h=design['horizon'];indices=split_indices(N,h)
    if len(actual_dates)!=N:raise ValueError('DATE_AXES_LENGTH_MISMATCH')
    result=dict(N=N,horizon=h,indices=indices,model_clock={},actual_dates={},training={})
    for segment in ('validation','evaluation'):
        a,b=indices[segment+'_first'],indices[segment+'_last']
        for name,values in [('model_clock',calendar),('actual_dates',actual_dates)]:
            result[name][segment]=dict(first=values[a],last=values[b],last_label_end=values[b+h])
        result['training'][segment]=[]
        for w in design['windows']:
            first=a-h-w+1
            if first<design['feature_rms_long']:raise ValueError('INSUFFICIENT_CONDITIONAL_HISTORY')
            result['training'][segment].append(dict(window=w,first_origin=first,last_origin=a-h,latest_label_end=a,training_count=w))
    return result


def recover_method_rows(directory,code,window,design,expected_origins):
    import numpy as np
    from study_core import stable_mean
    directory=Path(directory);out=[];expected=np.asarray(expected_origins,dtype=np.int64)
    for method in design['methods']:
        path=directory/f'result-{method}.json'
        row=dict(code=code,window=window,method=method,status='FAILED',mean_loss=None,strict_breach_count=None,n=None,selected_penalty=None,selected_gamma=None,reason='MISSING_OR_INTERRUPTED_METHOD')
        if path.exists():
            try:
                saved=load(path);row.update(saved,code=code,window=window,method=method)
                if saved.get('method')!=method:raise ValueError('METHOD_IDENTITY_MISMATCH')
                if saved['status']=='COMPLETE':
                    trace=directory/saved['trace_path']
                    if not trace.is_file() or trace.stat().st_size!=saved['trace_bytes'] or sha(trace)!=saved['trace_sha256']:raise ValueError('COMPLETE_TRACE_MISSING_OR_CHANGED')
                    with np.load(trace,allow_pickle=False) as z:arrays={k:np.asarray(z[k]) for k in ('origins','capacities','peak','floor','pinball','strict_breach','overrun','unused')}
                    if not np.array_equal(arrays['origins'],expected) or saved['n']!=len(expected) or any(x.shape!=expected.shape for x in arrays.values()):raise ValueError('INCOMPLETE_OR_WRONG_ORIGIN_GRID')
                    if any(not np.isfinite(x).all() for x in arrays.values()):raise ValueError('NONFINITE_COMPLETE_TRACE')
                    if np.any(arrays['capacities']<arrays['floor']) or np.any(arrays['peak']<arrays['floor']) or np.any(arrays['floor']<0) or np.any(arrays['pinball']<0):raise ValueError('INVALID_ABSOLUTE_PEAK_TRACE')
                    if stable_mean(arrays['pinball'])!=saved['mean_loss'] or int(np.count_nonzero(arrays['strict_breach']))!=saved['strict_breach_count']:raise ValueError('SAVED_TRACE_SCORE_MISMATCH')
                    row['trace_path']=str(trace.relative_to(ROOT)) if trace.is_relative_to(ROOT) else str(trace)
            except (OSError,ValueError,KeyError,TypeError) as exc:
                row.update(status='FAILED',mean_loss=None,strict_breach_count=None,n=None,reason='PERSISTED_METHOD_UNVERIFIED:'+str(exc),original_method_receipt_status=row.get('status'))
        if row['status']!='COMPLETE':row.update(mean_loss=None,strict_breach_count=None,n=None)
        out.append(row)
    return out


def prepare():
    from v10_cftc_data import read_archive,select_universe
    import numpy as np
    d=read_design();provenance=load(ROOT/'data/cftc-tff/provenance.json')
    if provenance['design_commit']!=DESIGN_COMMIT:raise ValueError('ACQUISITION_DESIGN_MISMATCH')
    paths=verify_acquisition(provenance,d);PUBLIC.mkdir(parents=True,exist_ok=True);rows=[];audits=[]
    attempt=ROOT/d['count_notation_clarification']['next_preparation_attempt'];attempt.mkdir(exist_ok=False)
    try:
        for path,owner in zip(paths,d['downloads_in_fixed_order']):
            table,audit=read_archive(path.read_bytes(),owner,d);rows.extend(table);audits.append(audit)
        universe=select_universe(rows,d)
        save(attempt/'source-audit.json',dict(archives=audits,raw_bytes_unchanged=True,source_provenance_sha256=sha(ROOT/'data/cftc-tff/provenance.json')))
        arrays=universe.pop('arrays_by_code')
        current=PUBLIC/'eligibility.json'
        if current.exists():
            expected=d['count_notation_clarification']['prior_universe_sha256']
            backup=ROOT/'.scratch/v10/eligibility.json.before-count-clarification.bak'
            if sha(current)!=expected or sha(backup)!=expected:raise ValueError('PRECOUNT_BACKUP_OR_CURRENT_METADATA_MISMATCH')
            atomic_json(current,universe,replace=True)
        else:save(current,universe)
        save(PUBLIC/'preparation-status.json',dict(status=universe['status'],selected_contract_count=len(universe['selected']),preparation_audit=str(attempt.relative_to(ROOT)),prior_attempts_preserved=True,no_forecast_run_at_preparation=True,captured_utc=utc_now()))
        if not universe['selected']:
            save(attempt/'unavailable.json',dict(status='UNAVAILABLE',reason='NO_CONTRACT_MEETS_FROZEN_UNIVERSE',no_forecast_run=True));return
        sources=[];splits={}
        for index,code in enumerate(universe['selected']):
            a=arrays[code];path=PUBLIC/'sources'/f's{index:02}.npz';path.parent.mkdir(exist_ok=True)
            with path.open('xb') as f:np.savez_compressed(f,position=np.asarray(a['position'],dtype=float),actual_dates=np.asarray(a['actual_dates'],dtype='datetime64[D]'),model_dates=np.asarray(a['model_dates'],dtype='datetime64[us]'))
            sources.append(dict(source_index=index,code=code,path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=sha(path)))
            splits[code]=split_receipt(universe['calendar'],a['actual_dates'],d)
        first=splits[universe['selected'][0]]
        save(PUBLIC/'sources.json',sources);save(PUBLIC/'splits.json',dict(first,per_contract=splits,date_axis_note=d['model_clock'],information_time=d['information_time']))
        print(json.dumps(dict(status='PREPARED',selected_contracts=len(sources),weeks=universe['N'],indices=first['indices'],actual_dates=first['actual_dates']),indent=2))
    except Exception as exc:
        if not (attempt/'source-audit.json').exists():save(attempt/'source-audit.json',dict(archives=audits,raw_bytes_unchanged=True))
        save(attempt/'preparation-failure.json',dict(status='UNAVAILABLE',reason=type(exc).__name__,message=str(exc),no_forecast_run=True,completed_archive_audits=len(audits)))
        raise


def seal():
    d=read_design();verify_acquisition(load(ROOT/'data/cftc-tff/provenance.json'),d)
    sources=load(PUBLIC/'sources.json');verify_sources(sources);files=[*CODE,*d['inherited_or_E1_code_sha256'],'run_v8_wp3.py','run_v9_nonstationarity.py','run_v10_menu.py']
    for p in files:
        if git('show','HEAD:'+p)!=(ROOT/p).read_bytes():raise ValueError('CODE_NOT_COMMITTED:'+p)
    for p in ('sources.json','splits.json','eligibility.json'):committed_file(PUBLIC/p)
    manifest=dict(schema='v10-cftc-code-seal-v1',created_utc=utc_now(),design_commit=DESIGN_COMMIT,design_provenance=committed_file(ROOT/PROTOCOL,DESIGN_COMMIT,True),code_commit=git('rev-parse','HEAD').decode().strip(),code_sha256={p:sha(ROOT/p) for p in files},design=d,sources=sources,acquisition_sha256=sha(ROOT/'data/cftc-tff/provenance.json'),prepared_sha256={p:sha(PUBLIC/p) for p in ('sources.json','splits.json','eligibility.json')})
    save(PUBLIC/'manifest.json',manifest);print(json.dumps(dict(status='SEALED',sources=len(sources),code_commit=manifest['code_commit'])))


def verify_seal(manifest):
    if manifest['design']!=read_design() or manifest['design_commit']!=DESIGN_COMMIT:raise ValueError('MANIFEST_DESIGN_CHANGED')
    committed_file(PUBLIC/'manifest.json')
    for p,digest in manifest['code_sha256'].items():
        if sha(ROOT/p)!=digest:raise ValueError('SEALED_CODE_CHANGED:'+p)
    for p,digest in manifest['prepared_sha256'].items():
        if sha(PUBLIC/p)!=digest:raise ValueError('PREPARED_INPUT_CHANGED:'+p)
    if sha(ROOT/'data/cftc-tff/provenance.json')!=manifest['acquisition_sha256']:raise ValueError('ACQUISITION_RECEIPT_CHANGED')


def worker(args):
    import numpy as np
    from run_study import RunGuard
    from run_v8_wp3 import ResourceCheckpoint
    from v10_cftc_forecast import forecast_cell
    manifest=load(PUBLIC/'manifest.json');verify_seal(manifest);d=manifest['design'];source=manifest['sources'][args.source];plan=load(PUBLIC/'formal/plan.json')
    public=Path(args.output).parent;private=Path(args.private);started=time.monotonic();guard=RunGuard(started,utc_now(),'v10-E2',public,private);checkpoint=ResourceCheckpoint(guard,plan['deadline_monotonic'],private/'resources.jsonl')
    result=dict(code=source['code'],source_index=args.source,started_utc=utc_now(),complete=False,records=[])
    try:
        path=ROOT/source['path']
        if path.stat().st_size!=source['bytes'] or sha(path)!=source['sha256']:raise ValueError('SOURCE_ARRAY_CHANGED')
        with np.load(path,allow_pickle=False) as z:position=np.array(z['position']);times=np.array(z['model_dates'])
        indices=load(PUBLIC/'splits.json')['indices'];origins=np.arange(indices['evaluation_first'],indices['evaluation_last']+1)
        checkpoint(stage='initialization')
        for window in d['windows']:
            folder=public/f'W{window}'
            try:
                forecast_cell(position,times,d,window,folder,checkpoint=checkpoint)
            finally:
                rows=recover_method_rows(folder,source['code'],window,d,origins)
                save(public/f'window-{window}.json',rows);result['records'].extend(rows)
                atomic_json(public/'progress.json',dict(records=result['records']),replace=True)
            checkpoint(stage='cell_end')
        result['complete']=True;checkpoint(stage='finalization')
    except Exception as exc:result.update(reason=getattr(exc,'code',getattr(exc,'reason',type(exc).__name__)),exception_type=type(exc).__name__,message=str(exc))
    result.update(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-started,resources=guard.resources);save(args.output,result)


def run_batch(tasks,deadline,design):
    active=[];waiting=list(tasks);finished=[]
    while waiting or active:
        now=time.monotonic()
        while waiting and len(active)<design['worker_count'] and now<deadline:
            task=waiting.pop(0);out=Path(task['output']);out.parent.mkdir(parents=True,exist_ok=False);private=Path(task['private']);private.mkdir(parents=True,exist_ok=False)
            cmd=[sys.executable,'-B',str(Path(__file__).resolve()),'worker','--source',str(task['source']),'--output',str(out),'--private',str(private)];log=(private/'console.txt').open('x');proc=subprocess.Popen(cmd,cwd=ROOT,env=dict(os.environ,**{k:'1' for k in THREADS}),stdout=log,stderr=subprocess.STDOUT,start_new_session=True);active.append(dict(task=task,proc=proc,log=log,start=time.monotonic()));now=time.monotonic()
        for item in list(active):
            now=time.monotonic();proc=item['proc'];timeout=now>=deadline or now-item['start']>=design['worker_hard_seconds']
            if proc.poll() is None and timeout:
                try:os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                proc.wait()
            if proc.poll() is not None:
                item['log'].close();task=item['task'];out=Path(task['output'])
                if not out.exists():save(out,dict(complete=False,records=[],source_index=task['source'],reason='GLOBAL_DEADLINE' if now>=deadline else ('WORKER_TIMEOUT' if timeout else 'TECHNICAL_WORKER_EXIT'),exit_code=proc.returncode))
                finished.append(dict(task=task,elapsed_seconds=now-item['start'],exit_code=proc.returncode));active.remove(item)
        if now>=deadline:
            for task in waiting:
                out=Path(task['output']);out.parent.mkdir(parents=True,exist_ok=False);save(out,dict(complete=False,records=[],source_index=task['source'],reason='GLOBAL_DEADLINE',status='NOT_RUN'));finished.append(dict(task=task,elapsed_seconds=0,exit_code=None))
            waiting=[]
        if active:time.sleep(.15)
    return finished


def formal():
    m=load(PUBLIC/'manifest.json');verify_seal(m);d=m['design'];verify_acquisition(load(ROOT/'data/cftc-tff/provenance.json'),d);verify_sources(m['sources']);base=PUBLIC/'formal';base.mkdir(exist_ok=False);PRIVATE.mkdir(parents=True,exist_ok=False)
    started=time.monotonic();save(base/'plan.json',dict(started_utc=utc_now(),started_monotonic=started,deadline_monotonic=started+d['formal_max_seconds'],worker_count=d['worker_count'],sources=len(m['sources']),design_commit=DESIGN_COMMIT));tasks=[dict(source=s['source_index'],output=str(base/'units'/f"s{s['source_index']:02}"/'result.json'),private=str(PRIVATE/f"s{s['source_index']:02}")) for s in m['sources']]
    finished=run_batch(tasks,started+d['formal_max_seconds'],d);save(base/'completion.json',dict(ended_utc=utc_now(),elapsed_seconds=time.monotonic()-started,tasks=finished))
    verify_seal(m);verify_acquisition(load(ROOT/'data/cftc-tff/provenance.json'),d);verify_sources(m['sources']);summarize_outputs()
    entries=[]
    with zipfile.ZipFile(base/'units.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted((base/'units').rglob('*')):
            if p.is_file():
                raw=p.read_bytes();name=str(p.relative_to(base/'units'));z.writestr(name,raw);entries.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    save(base/'units-manifest.json',dict(files=entries,archive_sha256=sha(base/'units.zip'),loose_files_retained=True))


def summarize_outputs():
    import numpy as np
    from v10_cftc_summary import summarize
    m=load(PUBLIC/'manifest.json');d=m['design'];indices=load(PUBLIC/'splits.json')['indices'];expected=np.arange(indices['evaluation_first'],indices['evaluation_last']+1);records=[]
    for source in m['sources']:
        unit=PUBLIC/'formal/units'/f"s{source['source_index']:02}"
        for w in d['windows']:
            rows=recover_method_rows(unit/f'W{w}',source['code'],w,d,expected)
            for row in rows:
                if row['status']=='COMPLETE':
                    source_path=ROOT/row['trace_path'];dest=PUBLIC/'complete-traces'/f"s{source['source_index']:02}-W{w}-{row['method']}.npz";dest.parent.mkdir(exist_ok=True)
                    with dest.open('xb') as f:f.write(source_path.read_bytes())
                    row['original_unit_trace_path']=row['trace_path'];row['trace_path']=str(dest.relative_to(ROOT))
            records.extend(rows)
    result=summarize(records,[s['code'] for s in m['sources']],d);save(PUBLIC/'method-inventory.json',records);save(PUBLIC/'summary.json',result)
    fields=list(result['cells'][0])
    with (PUBLIC/'cells.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,fields);writer.writeheader();writer.writerows(result['cells'])
    print(json.dumps(dict(predictions=result['predictions'],complete_method_cells=sum(r['status']=='COMPLETE' for r in records),planned_method_cells=len(records)),indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','seal','formal','worker'));p.add_argument('--source',type=int);p.add_argument('--output');p.add_argument('--private');a=p.parse_args()
    if a.command=='prepare':prepare()
    elif a.command=='seal':seal()
    elif a.command=='formal':formal()
    else:worker(a)
if __name__=='__main__':main()
