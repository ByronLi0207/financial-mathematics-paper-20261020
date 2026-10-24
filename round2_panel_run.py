"""E5 minimal panel-run port: expanded QR33 and empirical I, no new families.

The original alignment, QR33 segment, chronology and scoring core are retained.
All old arrays are copied and independently rescored; no attempt is retried.
"""
import os
import sys
sys.dont_write_bytecode=True
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import argparse,ast,csv,hashlib,io,json,math,re,resource,signal,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from round2_panel_sources import align_source
from conditional_study import StudyConfig,conditional_forecast,score_predictions,summarize_scores,select_parameter
from conditional_quantile import QuantileFitError
from empirical_headroom import predict as historical
from study_core import build_label_cache
from run_study import parse_thread_snapshot

ROOT=Path(__file__).resolve().parent
PRIOR=Path('/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023')
OUT=ROOT/'results/supervisor-20261023/e5'
PRIVATE=ROOT/'.scratch/supervisor-round2-20261023/e5'
OLD=PRIOR/'results/revision-20261023/round2/panel'
PREDICTION=Path('protocol/supervisor-20261023/e5-panel-prediction.md')
PREDICTION_COMMIT='8baa2f5b44327b3ba295927bd3db954f3475d35d'
PREDICTION_SHA='c9f82b37ee82dc000e6bf2590b1ef29195a0c442e7d3128536b6658d36f16d87'
MANIFEST_SHA='c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858'
SUMMARY_SHA='34134445a00354dcce3dc43de4c2adada7f2ea5403212558f90ef3480ee810f9'
GRID_SHA='9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb'
PENALTIES=(.001,.01,.1,1.,10.)
VAL=np.arange(329,381,dtype=np.int64)
EV=np.arange(405,682,dtype=np.int64)
CORE=('conditional_study.py','conditional_features.py','conditional_quantile.py','study_core.py','empirical_headroom.py','run_study.py')


def now():return datetime.now(timezone.utc).isoformat(timespec='microseconds')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,value,exclusive=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x' if exclusive else 'w') as f:json.dump(value,f,indent=2,allow_nan=False,default=dict);f.write('\n')


def segment(x,dates,origins,h,w,method,lam,guard):
    if method=='QR33':
        config=StudyConfig(h,w,13,6,26,604800);p=conditional_forecast(x,dates,origins,config,'QR',lam,checkpoint=guard);return p.capacities,list(p.fit_diagnostics)
    raise ValueError('unknown method')


def contract_check():
    original=ast.parse((PRIOR/'round2_panel_sources.py').read_text())
    port=ast.parse((ROOT/'round2_panel_sources.py').read_text())
    node=lambda tree:next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='align_source')
    assert ast.dump(node(original))==ast.dump(node(port)), 'alignment changed'
    rows=[dict(parameter=p,status='COMPLETE',origin_count=52,mean_pinball=1.) for p in PENALTIES]
    assert select_parameter(rows,PENALTIES,expected_count=52)['parameter']==10.
    rows[0]=dict(parameter=.001,status='FAILED',reason='DECLARED_FAILURE')
    assert select_parameter(rows,PENALTIES,expected_count=52)['status']=='INELIGIBLE'
    for name in CORE:assert sha(ROOT/name)==sha(PRIOR/name),name
    return dict(status='PASS',alignment_ast_identical=True,unchanged_core_sha256={n:sha(ROOT/n) for n in CORE},
                exact_tie_prefers_larger=True,failed_candidate_blocks_cell=True)


def copy_verified(source,destination,records,expected=None,private=False):
    raw=Path(source).read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if expected is not None and digest!=expected:raise ValueError('input fingerprint mismatch: '+str(source))
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True,mode=0o700 if private else 0o755)
    with destination.open('xb') as f:f.write(raw)
    if private:os.chmod(destination,0o600)
    records.append(dict(original_path=str(source),copied_path=str(destination.relative_to(ROOT)),bytes=len(raw),sha256=digest,private=private))


def prepare(receipt):
    committed=subprocess.run(['git','show',f'{PREDICTION_COMMIT}:{PREDICTION}'],cwd=ROOT,capture_output=True,check=True).stdout
    assert hashlib.sha256(committed).hexdigest()==PREDICTION_SHA==sha(ROOT/PREDICTION)
    subprocess.run(['git','merge-base','--is-ancestor',PREDICTION_COMMIT,'HEAD'],cwd=ROOT,check=True)
    stamp=subprocess.run(['git','show','-s','--format=%cI',PREDICTION_COMMIT],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    assert datetime.fromisoformat(stamp)<datetime.fromisoformat(receipt['run_started_utc'])
    receipt.update(prediction_commit=PREDICTION_COMMIT,prediction_commit_timestamp=stamp,prediction_file_sha256=PREDICTION_SHA,
                   prediction_file=str(PREDICTION),first_model_fit_utc=None,chronology_verified_before_fit=True)
    OUT.mkdir(parents=True,exist_ok=False);PRIVATE.mkdir(parents=True,exist_ok=False,mode=0o700)
    dump(OUT/'run-receipt.json',receipt,exclusive=True)
    dump(OUT/'contract-checks.json',contract_check(),exclusive=True)
    records=[]
    for path in sorted(OLD.rglob('*')):
        if path.is_file():copy_verified(path,OUT/'inputs/panel'/path.relative_to(OLD),records,
                                       MANIFEST_SHA if path.name=='selection-manifest.json' else SUMMARY_SHA if path.name=='summary.csv' else None)
    grid_relative=Path('data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv')
    assert sha(ROOT/grid_relative)==GRID_SHA
    copy_verified(PRIOR/grid_relative,PRIVATE/'sources/PDPOSGS-B.csv',records,GRID_SHA,True)
    for name in ('round2_panel_sources.py','round2_panel_run.py'):
        copy_verified(PRIOR/name,OUT/'inputs/port-lineage'/name,records)
    for name in ('round2-D3-panel.json','round2-D3-panel.md'):
        copy_verified(PRIOR/'protocol/revision-20261023'/name,OUT/'inputs/protocol'/name,records)
    manifest=json.loads((OUT/'inputs/panel/selection-manifest.json').read_text())
    predicted=re.findall(r'^\| ([A-Z0-9-]+) \| (\d+) \| `([a-f0-9]{64})` \|$',committed.decode(),re.M)
    assert [r[0] for r in predicted]==manifest['eligible'] and len(predicted)==12
    for key,count,digest in predicted:
        s=next(r for r in manifest['series'] if r['series_key']==key)
        assert s['status']=='ELIGIBLE' and s['bytes']==int(count) and s['sha256']==digest
        copy_verified(PRIOR/s['local_raw_path'],PRIVATE/'sources'/f'{key}.csv',records,digest,True)
        for h in (6,24):
            for w in (52,260):
                identity=f'{key}-h{h}-w{w}'
                copy_verified(PRIOR/'.scratch/round2/panel-models'/identity/'numeric-traces.npz',PRIVATE/'old-traces'/f'{identity}.npz',records,private=True)
    assert len(manifest['skipped'])==2
    dump(OUT/'input-inventory.json',dict(frozen_before_first_new_fit_utc=now(),files=records,
         manifest_sha256=MANIFEST_SHA,original_summary_sha256=SUMMARY_SHA,grid_sha256=GRID_SHA),exclusive=True)
    receipt.update(input_inventory_sha256=sha(OUT/'input-inventory.json'),code_sha256={n:sha(ROOT/n) for n in (*CORE,'round2_panel_sources.py','round2_panel_run.py')},
                   python_executable=sys.executable,numpy_version=np.__version__)
    dump(OUT/'run-receipt.json',receipt)
    return manifest


class LimitStop(Exception):
    def __init__(self,code):self.code=code;super().__init__(code)


class Guard:
    def __init__(self,start,global_start,folder):
        self.start=start;self.global_start=global_start;self.folder=folder;self.last_write=-math.inf
        self.resources=dict(started_utc=now(),elapsed_seconds=0.,global_elapsed_seconds=0.,peak_rss_bytes=0,
             requested_numerical_threads=1,maximum_observed_os_threads=0,thread_snapshot_count=0,thread_probe_status='UNVERIFIED')
    def __call__(self,**progress):
        elapsed=time.monotonic()-self.start;glob=time.monotonic()-self.global_start
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        probe=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],capture_output=True,text=True,check=True,timeout=5)
        threads=parse_thread_snapshot(probe.stdout,os.getpid())
        self.resources.update(elapsed_seconds=elapsed,global_elapsed_seconds=glob,peak_rss_bytes=max(rss,self.resources['peak_rss_bytes']),
              maximum_observed_os_threads=max(threads,self.resources['maximum_observed_os_threads']),thread_snapshot_count=self.resources['thread_snapshot_count']+1,
              thread_probe_status='PASS',checkpoint_utc=now(),**progress)
        if elapsed-self.last_write>=5:dump(self.folder/'progress.json',self.resources);self.last_write=elapsed
        if glob>=10800:raise LimitStop('GLOBAL_TIME_LIMIT')
        if elapsed>=590:raise LimitStop('CELL_TIME_LIMIT')
        if rss>=2147483648:raise LimitStop('RSS_LIMIT')
        if threads!=1:raise LimitStop('THREAD_LIMIT')


def save_trace(path,**arrays):
    with Path(path).open('xb') as f:np.savez(f,**arrays)
    os.chmod(path,0o600)


def archived(key,h,w,x,peak):
    identity=f'{key}-h{h}-w{w}';path=OUT/'inputs/panel/cells'/f'{identity}.json';record=json.loads(path.read_text())
    assert record['selection_manifest_sha256']==MANIFEST_SHA
    scores={};caps={}
    with np.load(PRIVATE/'old-traces'/f'{identity}.npz',allow_pickle=False) as z:
        assert np.array_equal(z['origins'],EV) and np.array_equal(z['peak'],peak) and np.array_equal(z['floor'],np.abs(x[EV]))
        for method in ('frozen_F','QR33','C2_QR4'):
            a=next(r for r in record['records'] if r['method']==method);assert a['status']=='COMPLETE'
            capacity=np.array(z[method],copy=True);error=peak-capacity
            loss=.95*np.maximum(error,0)+.05*np.maximum(-error,0);mean=math.fsum(map(float,loss))/len(EV)
            assert math.isclose(mean,a['mean_pinball'],rel_tol=2e-14,abs_tol=1e-12)
            assert int((error>0).sum())==a['strict_breach_count']
            summary=summarize_scores(score_predictions(peak,capacity,np.abs(x[EV]),EV))
            assert summary['origin_count']==277
            scores[method]=summary;caps[method]=capacity
    return record,scores,caps


def cell(key,h,w,source,global_start,receipt):
    identity=f'{key}-h{h}-w{w}';folder=OUT/'cells'/identity;folder.mkdir(parents=True,exist_ok=False)
    private=PRIVATE/'cells'/identity;private.mkdir(parents=True,exist_ok=False,mode=0o700)
    started=time.monotonic();guard=Guard(started,global_start,folder)
    result=dict(series_key=key,horizon=h,window=w,status='INITIALIZING',post_result=True,exploratory=True,
       native_unit='USD millions',source_sha256=source['sha256'],selection_manifest_sha256=MANIFEST_SHA,
       validation_origins=[329,380],evaluation_origins=[405,681],penalties=list(PENALTIES),selected_penalty=None,candidates=[])
    def alarm(*_):raise LimitStop('GLOBAL_TIME_LIMIT' if time.monotonic()-global_start>=10800 else 'CELL_TIME_LIMIT')
    signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,min(590.,max(.001,10800-(started-global_start))))
    try:
        raw=(PRIVATE/'sources'/f'{key}.csv').read_bytes();assert hashlib.sha256(raw).hexdigest()==source['sha256']
        grid=[r['As Of Date'] for r in csv.DictReader((PRIVATE/'sources/PDPOSGS-B.csv').open())]
        x,facts=align_source(raw,key,grid);dates=np.array(grid,dtype='datetime64[D]');cache=build_label_cache(x,h)
        old,scores,caps=archived(key,h,w,x,cache.peak[EV]);result['archive_rescored']=scores
        result['fixed_p1_member']=scores['QR33']['mean_pinball']>scores['frozen_F']['mean_pinball']
        result['original_cell_json_sha256']=sha(OUT/'inputs/panel/cells'/f'{identity}.json')
        result['old_trace_sha256']=sha(PRIVATE/'old-traces'/f'{identity}.npz');result['alignment']=facts
        guard(stage='archival_inputs_verified')
        if receipt['first_model_fit_utc'] is None:
            receipt['first_model_fit_utc']=now();assert datetime.fromisoformat(receipt['prediction_commit_timestamp'])<datetime.fromisoformat(receipt['first_model_fit_utc'])
            dump(OUT/'run-receipt.json',receipt)
        for lam in PENALTIES:
            begin=time.monotonic();row=dict(parameter=lam,status='INCOMPLETE',started_utc=now())
            try:
                capacity,diag=segment(x,dates,VAL,h,w,'QR33',lam,guard)
                summary=summarize_scores(score_predictions(cache.peak[VAL],capacity,np.abs(x[VAL]),VAL))
                row.update(status='COMPLETE',**summary,fit_diagnostics=diag)
                save_trace(private/f'validation-lambda-{lam:g}.npz',origins=VAL,capacity=capacity,peak=cache.peak[VAL],floor=np.abs(x[VAL]))
            except QuantileFitError as e:
                row.update(status='FAILED',reason=e.code,solver_diagnostics=dict(e.diagnostics),failure_context=getattr(e,'failure_context',None))
                partial=getattr(e,'partial_forecast',None)
                if partial is not None and len(partial.origins):save_trace(private/f'validation-lambda-{lam:g}-INCOMPLETE.npz',origins=partial.origins,capacity=partial.capacities)
            finally:
                row['elapsed_seconds']=time.monotonic()-begin;result['candidates'].append(row);dump(folder/'result.json',result)
        selection=select_parameter(result['candidates'],PENALTIES,expected_count=len(VAL))
        result['selection']=selection;result['selected_penalty']=selection['parameter']
        result['selection_frozen_utc']=now()
        dump(folder/'selection-before-evaluation.json',dict(frozen_utc=result['selection_frozen_utc'],selection=selection,
             candidates=result['candidates'],code_sha256=receipt['code_sha256'],prediction_commit=PREDICTION_COMMIT),exclusive=True)
        if selection['status']!='SELECTED':result['status']='VALIDATION_INELIGIBLE'
        else:
            result['evaluation_started_utc']=now();assert result['selection_frozen_utc']<result['evaluation_started_utc']
            result['status']='EVALUATING';dump(folder/'result.json',result)
            capacity,diag=segment(x,dates,EV,h,w,'QR33',selection['parameter'],guard)
            empirical=historical(x,EV,h,w,13);assert np.array_equal(empirical['F'],caps['frozen_F'])
            new=summarize_scores(score_predictions(cache.peak[EV],capacity,np.abs(x[EV]),EV))
            ordinary=summarize_scores(score_predictions(cache.peak[EV],empirical['I'],np.abs(x[EV]),EV))
            save_trace(private/'numeric-traces.npz',origins=EV,peak=cache.peak[EV],floor=np.abs(x[EV]),
                       frozen_F=caps['frozen_F'],QR33=caps['QR33'],C2_QR4=caps['C2_QR4'],QR33_plus=capacity,I=empirical['I'])
            result.update(status='COMPLETE',evaluation=new,I=ordinary,fit_diagnostics=diag,
                 private_evaluation_trace_sha256=sha(private/'numeric-traces.npz'),evaluation_completed_utc=now())
        guard(stage='cell_terminal')
    except QuantileFitError as e:
        result.update(status='EVALUATION_FAILED',reason=e.code,solver_diagnostics=dict(e.diagnostics),failure_context=getattr(e,'failure_context',None))
        partial=getattr(e,'partial_forecast',None)
        if partial is not None and len(partial.origins):save_trace(private/'evaluation-INCOMPLETE.npz',origins=partial.origins,capacity=partial.capacities)
    except LimitStop as e:result.update(status='TIME_LIMIT' if 'TIME_LIMIT' in e.code else 'RESOURCE_LIMIT',reason=e.code)
    except (Exception,KeyboardInterrupt) as e:result.update(status='FAILED',reason=type(e).__name__,detail=str(e))
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        present={r['parameter'] for r in result['candidates']}
        for lam in PENALTIES:
            if lam not in present:result['candidates'].append(dict(parameter=lam,status='INCOMPLETE',reason='CELL_STOPPED_BEFORE_CANDIDATE'))
        result['resources']=guard.resources;result['resources']['final_elapsed_seconds']=time.monotonic()-started
        result['completed_utc']=now();dump(folder/'result.json',result)
    print(json.dumps(dict(cell=identity,status=result['status'],selected_penalty=result['selected_penalty'],elapsed_seconds=result['resources']['final_elapsed_seconds'])),flush=True)
    return result


def aggregate(results):
    rows=[]
    for r in results:
        row={k:r[k] for k in ('series_key','horizon','window','status')};row['selected_penalty']=r.get('selected_penalty');row['reason']=r.get('reason')
        archived_input=json.loads((OUT/'inputs/panel/cells'/f"{r['series_key']}-h{r['horizon']}-w{r['window']}.json").read_text())
        fixed_old={a['method']:a for a in archived_input['records']}
        old=r.get('archive_rescored',fixed_old)
        for name,summary in [('F',old.get('frozen_F')),('original_QR33',old.get('QR33')),('QR4_plus',old.get('C2_QR4')),
                             ('QR33_plus',r.get('evaluation') if r['status']=='COMPLETE' else None),('I',r.get('I') if r['status']=='COMPLETE' else None)]:
            row[name+'_mean_pinball']=summary['mean_pinball'] if summary else None
            row[name+'_strict_breach_count']=summary['strict_breach_count'] if summary else None
        f=row['F_mean_pinball']
        for name in ('original_QR33','QR4_plus','QR33_plus','I'):
            loss=row[name+'_mean_pinball'];row[name+'_percent_vs_F']=100*(loss-f)/f if loss is not None and f else None
        row['fixed_p1_member']=fixed_old['QR33']['mean_pinball']>fixed_old['frozen_F']['mean_pinball']
        rows.append(row)
    assert len(rows)==48
    b=io.StringIO(newline='');writer=csv.DictWriter(b,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    with (OUT/'summary.csv').open('x') as stream:stream.write(b.getvalue())
    complete=[r for r in rows if r['status']=='COMPLETE'];members=[r for r in rows if r['fixed_p1_member']]
    assert len(members)==45
    counts=[sum(r['fixed_p1_member'] and r['QR33_plus_mean_pinball']<r['original_QR33_mean_pinball'] for r in complete),
            sum(-10<=r['QR33_plus_percent_vs_F']<=10 for r in complete),sum(r['selected_penalty']>=1 for r in complete)]
    assessment={p:dict(success_count=n,fixed_denominator=d,threshold=t,supported=n>=t)
                for p,n,d,t in zip(('P1','P2','P3'),counts,(45,48,48),(40,36,25))}
    dump(OUT/'prediction-assessment.json',dict(prediction_commit=PREDICTION_COMMIT,predictions=assessment,complete_cells=len(complete),planned_cells=48,
          no_pooled_independence_test=True,post_result_exploratory=True),exclusive=True)
    return rows,assessment


def verify(results):
    maximum=0.;arrays=0;validation_segments=0;diagnostics=0
    for r in results:
        if r['status']!='COMPLETE':continue
        identity=f"{r['series_key']}-h{r['horizon']}-w{r['window']}";private=PRIVATE/'cells'/identity
        frozen=json.loads((OUT/'cells'/identity/'selection-before-evaluation.json').read_text())
        assert frozen['frozen_utc']<r['evaluation_started_utc']
        assert frozen['selection']==select_parameter(frozen['candidates'],PENALTIES,expected_count=52)
        with np.load(private/'numeric-traces.npz',allow_pickle=False) as z:
            assert np.array_equal(z['origins'],EV)
            for method,summary in [('frozen_F',r['archive_rescored']['frozen_F']),('QR33',r['archive_rescored']['QR33']),('C2_QR4',r['archive_rescored']['C2_QR4']),('QR33_plus',r['evaluation']),('I',r['I'])]:
                error=z['peak']-z[method];loss=.95*np.maximum(error,0)+.05*np.maximum(-error,0);mean=math.fsum(map(float,loss))/277
                maximum=max(maximum,abs(mean-summary['mean_pinball']));assert math.isclose(mean,summary['mean_pinball'],rel_tol=2e-14,abs_tol=1e-12)
                assert int((error>0).sum())==summary['strict_breach_count'];assert np.isfinite(z[method]).all() and (z[method]>=z['floor']).all();arrays+=1
        for candidate in r['candidates']:
            assert candidate['status']=='COMPLETE' and candidate['origin_count']==52
            with np.load(private/f"validation-lambda-{candidate['parameter']:g}.npz",allow_pickle=False) as z:
                assert np.array_equal(z['origins'],VAL);error=z['peak']-z['capacity'];mean=math.fsum(map(float,.95*np.maximum(error,0)+.05*np.maximum(-error,0)))/52
                assert math.isclose(mean,candidate['mean_pinball'],rel_tol=2e-14,abs_tol=1e-12);validation_segments+=1
        for d in [*r['fit_diagnostics'],*(d for c in r['candidates'] for d in c['fit_diagnostics'])]:
            assert d['training_count']==r['window'] and d['training_last_origin']+r['horizon']==d['latest_label_end']==d['refit_index']
            assert d['duality_gap']<=d['gap_tolerance'] and d['primal_residual']<=d['primal_tolerance'] and d['dual_residual']<=d['dual_tolerance'];diagnostics+=1
    value=dict(status='PASS',independent_saved_array_arithmetic=True,evaluation_arrays_checked=arrays,validation_segments_checked=validation_segments,
               new_fit_diagnostics_checked=diagnostics,maximum_loss_absolute_error=maximum,selection_before_evaluation=True,no_new_fit_during_verification=True)
    dump(OUT/'verification.json',value,exclusive=True);return value


def run_all():
    global_start=time.monotonic();receipt=dict(status='PREPARING',run_started_utc=now(),post_result_exploratory=True,
          limits=dict(global_seconds=10800,cell_seconds=590,max_rss_bytes=2147483648,numerical_workers=1,numerical_threads=1),command=[sys.executable,*sys.argv])
    manifest=prepare(receipt);results=[];receipt['status']='RUNNING';dump(OUT/'run-receipt.json',receipt)
    try:
        for key in manifest['eligible']:
            source=next(s for s in manifest['series'] if s['series_key']==key)
            for h in (6,24):
                for w in (52,260):
                    if time.monotonic()-global_start>=10800:
                        old=json.loads((OUT/'inputs/panel/cells'/f'{key}-h{h}-w{w}.json').read_text());scores={r['method']:{k:v for k,v in r.items() if k in ('mean_pinball','strict_breach_count')} for r in old['records']}
                        r=dict(series_key=key,horizon=h,window=w,status='NOT_RUN_TIME_LIMIT',reason='GLOBAL_TIME_LIMIT',archive_rescored=scores,
                               fixed_p1_member=scores['QR33']['mean_pinball']>scores['frozen_F']['mean_pinball'])
                    else:r=cell(key,h,w,source,global_start,receipt)
                    results.append(r)
        rows,assessment=aggregate(results);verification=verify(results)
        receipt.update(status='COMPLETE' if all(r['status']=='COMPLETE' for r in results) else 'INCOMPLETE',
             completed_cells=sum(r['status']=='COMPLETE' for r in results),planned_cells=48,predictions=assessment,
             summary_sha256=sha(OUT/'summary.csv'),verification_sha256=sha(OUT/'verification.json'))
    finally:
        receipt.update(run_completed_utc=now(),total_elapsed_seconds=time.monotonic()-global_start)
        dump(OUT/'run-receipt.json',receipt)
    print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');parser.add_argument('--check-contract',action='store_true');args=parser.parse_args()
    if args.check_contract:print(json.dumps(contract_check(),indent=2))
    elif args.run:run_all()
    else:parser.error('choose --run or --check-contract')
