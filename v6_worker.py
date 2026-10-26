"""v6 WP2 serial cell worker. New public aggregates; private arrays stay .scratch."""
from __future__ import annotations
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib,json,math,os,platform,resource,signal,subprocess,time
from pathlib import Path
import numpy as np
from conditional_sources import load_source
from conditional_study import (StudyConfig, conditional_forecast, score_predictions,
                               summarize_scores as original_summary)
from conditional_features import completed_training_indices
import study_core as core
import v6_aci as aci
import v6_sav as sav
import v6_inference as inf

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'results/revision-20261023/v6'
PRIVATE=ROOT/'.scratch/revision-v6'
SPEC='protocol/revision-20261022/study-spec.json'
SELECTION='protocol/revision-20261022/selection-freeze.json'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def read_json(p): return json.loads(Path(p).read_text())
def write_json_new(path,value):
    # Encode completely first: a bad value must not leave a misleading receipt.
    encoded=json.dumps(value,indent=2,allow_nan=False)+'\n'
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:f.write(encoded)
def save_private(path,**arrays):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:np.savez_compressed(f,**arrays)
    return dict(bytes=p.stat().st_size,sha256=sha(p))

class Guard:
    def __init__(self):
        self.start=time.monotonic();self.started=utc();self.last=-math.inf
        self.peak=0;self.threads=0;self.snapshots=0
    def __call__(self,*args,**kwargs):
        self.peak=max(self.peak,int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*(1 if platform.system()=='Darwin' else 1024))
        elapsed=time.monotonic()-self.start
        if elapsed>540:raise RuntimeError('RESOURCE_WALL')
        if self.peak>1610612736:raise RuntimeError('RESOURCE_RSS')
        if elapsed-self.last>=1:
            from run_study import parse_thread_snapshot
            proc=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],capture_output=True,text=True,timeout=3,check=True)
            n=parse_thread_snapshot(proc.stdout,os.getpid());self.threads=max(self.threads,n)
            self.snapshots+=1;self.last=elapsed
            if n>2:raise RuntimeError('RESOURCE_THREADS')
    def summary(self):
        # No raising final probe: preserve a genuine failed experiment receipt.
        rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*(1 if platform.system()=='Darwin' else 1024)
        return dict(started_utc=self.started,ended_utc=utc(),elapsed_seconds=time.monotonic()-self.start,
            peak_rss_bytes=max(rss,self.peak),maximum_observed_os_threads=self.threads,
            thread_snapshot_count=self.snapshots,requested_numerical_threads=1,
            internal_wall_seconds=540,hard_wall_seconds=600,internal_rss_bytes=1610612736,
            hard_rss_bytes=2147483648)

def setup(source,h,w):
    spec=read_json(ROOT/SPEC);cfg=spec['sources'][source]
    if h not in spec['horizons'] or w not in cfg['windows']:raise ValueError('CELL_NOT_DECLARED')
    s=load_source(ROOT/cfg['input_relative_path'],source,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
    config=StudyConfig(h,w,cfg['refit_step'],cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds'])
    choices=[c for c in read_json(ROOT/SELECTION)['cells'] if (c['source'],c['horizon'],c['window'],c['family'])==(source,h,w,'QR')]
    if len(choices)!=1 or choices[0]['status']!='SELECTED':raise ValueError('ORIGINAL_SELECTION_MISSING')
    return s,cfg,config,choices[0]['parameter']

def ids_for(cfg,phase):
    return np.arange(cfg[phase+'_origin_first'],cfg[phase+'_origin_last']+1,dtype=np.int64)

def trace_entry(source,h,w,phase,family):
    rows=read_json(PRIVATE/'input-inventory.json')['original_cells']
    cell=[r for r in rows if (r['source'],r['horizon'],r['window'])==(source,h,w)]
    if len(cell)!=1:raise ValueError('CELL_ADMISSION_MISSING')
    matches=[r for r in cell[0]['traces'] if (r['phase'],r['family'])==(phase,family)]
    if len(matches)!=1:raise ValueError('TRACE_ADMISSION_MISSING')
    e=matches[0];p=ROOT/e['path']
    if p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']:raise ValueError('TRACE_CHANGED')
    if sha(ROOT/e['manifest_path'])!=e['manifest_sha256']:raise ValueError('ORIGINAL_RECEIPT_CHANGED')
    return e

def original_trace(source,h,w,phase,method,*,position=None):
    family='historical_references' if phase=='references' else method
    e=trace_entry(source,h,w,phase,family)
    prefix=method
    if phase=='validation':
        selected=[x for x in read_json(ROOT/SELECTION)['cells'] if (x['source'],x['horizon'],x['window'],x['family'])==(source,h,w,method)][0]['parameter']
        menu=read_json(ROOT/SPEC)['qr_penalties'] if method=='QR' else read_json(ROOT/SPEC)['sources'][source]['knn_candidates'][str(w)]
        prefix='candidate_'+str(menu.index(selected))
    with np.load(ROOT/e['path'],allow_pickle=False) as f:
        z={k:np.array(f[prefix+'_'+k],copy=True) for k in ('origins','capacity','peak','floor','pinball')}
    cfg=read_json(ROOT/SPEC)['sources'][source]
    expected=ids_for(cfg,'evaluation' if phase=='references' else phase)
    if not np.array_equal(z['origins'],expected):raise ValueError('ORIGIN_IDENTITY')
    scored=score_predictions(z['peak'],z['capacity'],z['floor'],z['origins'])
    if not np.array_equal(scored.pinball,z['pinball']):raise ValueError('LOSS_IDENTITY')
    if position is not None:
        cache=core.build_label_cache(position,h)
        if not np.array_equal(z['peak'],cache.peak[expected]) or not np.array_equal(z['floor'],np.abs(position[expected])):
            raise ValueError('TARGET_IDENTITY')
    z['trace_sha256']=e['sha256']
    z['original_aggregate']=original_summary(scored)
    receipt=read_json(ROOT/e['manifest_path'])['result']
    if phase=='validation':
        matched=[r for r in receipt['candidate_rows'] if r['parameter']==selected]
        keys=('origin_count','mean_pinball')
    else:
        matched=[r for r in receipt['summary_rows'] if r['method']==method]
        keys=tuple(z['original_aggregate'])
    if len(matched)!=1 or any(z['original_aggregate'][k]!=matched[0][k] for k in keys):
        raise ValueError('ORIGINAL_AGGREGATE_IDENTITY')
    return z

def frozen_f(position,ids,config,checkpoint=None):
    ids=np.asarray(ids,dtype=np.int64);x=np.asarray(position,dtype=float)
    if len(ids)==0 or np.any(np.diff(ids)!=1):raise ValueError('CONTIGUOUS_F_REQUIRED')
    cache=core.build_label_cache(x,config.horizon);last=None;caps=np.empty(len(ids))
    for j,t0 in enumerate(ids):
        t=int(t0);r=int(ids[0])+((t-int(ids[0]))//config.refit_step)*config.refit_step
        if r!=last:
            pool=completed_training_indices(r,config.horizon,config.window,minimum_feature_index=0)
            q=core.order_statistic(cache.headroom[pool],core.exact_rank(len(pool),19,20));last=r
        caps[j]=abs(float(x[t]))+q
        if checkpoint is not None and j%32==0:checkpoint(stage='frozen_f')
    return caps

def aci_diagnostics(result):
    names=('alpha','calibration_counts','ranks','feedback_counts','clip_counts')
    a={k:np.asarray(result[k]) for k in names}
    n=len(a['alpha'])
    if not n or any(v.shape!=(n,) for v in a.values()):raise ValueError('ACI_DIAGNOSTIC_ALIGNMENT')
    return dict(gamma=result['gamma'],initial_calibration_count=result['initial_calibration_count'],
        alpha_min=float(a['alpha'].min()),alpha_max=float(a['alpha'].max()),
        calibration_min=int(a['calibration_counts'].min()),calibration_max=int(a['calibration_counts'].max()),
        rank_min=int(a['ranks'].min()),rank_max=int(a['ranks'].max()),
        clip_count=int(a['clip_counts'].sum()),issue_count=n,
        clipped_issue_count=int(np.count_nonzero(a['clip_counts'])),
        clipped_issue_fraction=float(np.count_nonzero(a['clip_counts'])/n),
        matured_wrapped_feedback_consumed=int(a['feedback_counts'].sum()),
        cumulative_matured_wrapped_feedback=result['feedback_consumed'])

def score(peak,caps,ids,h):return inf.summarize_scores(peak,caps,tau=.95,origins=ids,horizon=h)
def cell_name(s,h,w):return f'{s}-h{h}-w{w}'
def check_execution_freeze():
    f=read_json(ROOT/'protocol/revision-v6/wp2-executable-freeze.json')
    if sha(PRIVATE/'input-inventory.json')!=f['private_inventory_sha256']:raise ValueError('INPUT_INVENTORY_CHANGED')
    for row in read_json(PRIVATE/'input-inventory.json')['six_csv_checks']:
        for key in ('reproduced_path','archived_path'):
            if sha(ROOT/row[key])!=row['expected_sha256']:raise ValueError('ORIGINAL_AGGREGATE_CSV_CHANGED')

    for p,d in f['files'].items():
        if sha(ROOT/p)!=d:raise ValueError('EXECUTABLE_FREEZE_CHANGED:'+p)
    return sha(ROOT/'protocol/revision-v6/wp2-executable-freeze.json')

def prepare_aci(source,h,w,basekind,guard):
    s,cfg,c,lam=setup(source,h,w);ids=ids_for(cfg,'validation')
    grid=aci.initialization_grid(int(ids[0]),h,w,c.refit_step,c.long_scale if basekind=='QR' else 0)
    if grid['mature_initial_count']<19:
        return dict(status='NA',reason='INSUFFICIENT_PREVALIDATION_CALIBRATION',grid=grid),{}
    warm=np.arange(grid['pre_first'],int(ids[0]),dtype=np.int64)
    cache=core.build_label_cache(s.position,h)
    if basekind=='QR':
        warmcaps=conditional_forecast(s.position,s.dates,warm,c,'QR',lam,checkpoint=guard).capacities
        z=original_trace(source,h,w,'validation','QR',position=s.position);base=z['capacity']
    else:
        warmcaps=frozen_f(s.position,warm,c,guard);base=frozen_f(s.position,ids,c,guard)
    result=dict(status='COMPLETE',grid=grid,base=basekind,original_qr_lambda=lam if basekind=='QR' else None)
    arrays=dict(warm_origins=warm,warm_base=warmcaps,warm_peak=cache.peak[warm],
        origins=ids,base=base,peak=cache.peak[ids],floor=np.abs(s.position[ids]))
    return result,arrays

def gamma_row(g,metrics,diagnostics):
    return dict(gamma=g,status='COMPLETE',origin_count=metrics['n'],hits=metrics['full_hits'],mean_loss=metrics['mean_loss'],scores=metrics,diagnostics=diagnostics)

def sav_failure_public(diagnostics):
    z=dict(diagnostics)
    if 'starts' in z:z['starts']=[asdict(x) for x in z['starts']]
    return z

def run_aci_validation(source,h,w,basekind,guard):
    result,arrays=prepare_aci(source,h,w,basekind,guard)
    if result['status']!='COMPLETE':return result,{}
    menu=[];private=dict(arrays)
    for j,g in enumerate(aci.GAMMAS):
        try:
            z=aci.aci_stream(**arrays,horizon=h,window=w,gamma=g,checkpoint=guard)
            metrics=score(arrays['peak'],z['capacities'],arrays['origins'],h)
            menu.append(gamma_row(g,metrics,aci_diagnostics(z)))
            for k in ('capacities','alpha','calibration_counts','ranks','clip_counts','feedback_counts','score_quantiles','raw_thresholds'):
                private[f'gamma{j}_{k}']=z[k]
            private[f'gamma{j}_state_fractions']=np.array(z['state_fractions'],dtype=str)
            private[f'gamma{j}_feedback_json']=np.array(json.dumps(z['feedback_records'],allow_nan=False))
        except RuntimeError:
            raise # resource limits govern the complete cell, no misleading remainder.
        except (ValueError,ArithmeticError) as exc:
            menu.append(dict(gamma=g,status='NA',reason=type(exc).__name__,origin_count=None,hits=None,mean_loss=None))
    result.update(menu=menu,selection=aci.select_gamma(menu,expected_count=len(arrays['origins'])))
    if result['selection']['status']!='SELECTED':result['status']='NA';result['reason']='NO_ELIGIBLE_GAMMA'
    return result,private

def run_aci_evaluation(source,h,w,basekind,guard):
    selection=read_json(PUBLIC/'wp2-selection-freeze.json')
    ident=f'{cell_name(source,h,w)}-ACI_{basekind}'
    row=selection['cells'][ident]
    if row['status']!='COMPLETE':return dict(status='NA',reason='VALIDATION_INELIGIBLE',validation_status=row['status']),{}
    valpath=PUBLIC/'wp2'/('validation-'+ident+'.json')
    if sha(valpath)!=row['receipt_sha256']:raise ValueError('VALIDATION_RECEIPT_CHANGED')
    val=read_json(valpath);g=val['selection']['gamma']
    p=PRIVATE/'wp2'/('validation-'+ident+'.npz')
    if sha(p)!=val['private_artifact']['sha256']:raise ValueError('VALIDATION_TRACE_CHANGED')
    with np.load(p,allow_pickle=False) as f:arrays={k:np.array(f[k],copy=True) for k in ('warm_origins','warm_base','warm_peak','origins','base','peak','floor')};validated=np.array(f[f'gamma{aci.GAMMAS.index(g)}_capacities'],copy=True)
    s,cfg,c,lam=setup(source,h,w);ids=ids_for(cfg,'evaluation')
    method='QR' if basekind=='QR' else 'frozen_F'
    original=original_trace(source,h,w,'evaluation' if method=='QR' else 'references',method,position=s.position)
    for k,tail in (('origins',ids),('base',original['capacity']),('peak',original['peak']),('floor',original['floor'])):arrays[k]=np.concatenate((arrays[k],tail))
    z=aci.aci_stream(**arrays,horizon=h,window=w,gamma=g,checkpoint=guard)
    nv=len(validated)
    if not np.array_equal(z['capacities'][:nv],validated):raise ValueError('VALIDATION_PREFIX_CHANGED')
    caps=z['capacities'][nv:];sliced={**z}
    for k in ('alpha','calibration_counts','ranks','clip_counts','feedback_counts'):sliced[k]=z[k][nv:]
    result=dict(status='COMPLETE',selected_gamma=g,selection_freeze_sha256=sha(PUBLIC/'wp2-selection-freeze.json'),validation_prefix_identical=True,
        scores=score(original['peak'],caps,ids,h),diagnostics=aci_diagnostics(sliced),
        unwrapped_scores=score(original['peak'],original['capacity'],ids,h))
    private=dict(origins=ids,capacities=caps,peak=original['peak'],floor=original['floor'])
    for k in ('alpha','calibration_counts','ranks','clip_counts','feedback_counts','score_quantiles','raw_thresholds'):private[k]=z[k][nv:]
    private['state_fractions']=np.array(z['state_fractions'],dtype=str)
    private['feedback_json']=np.array(json.dumps(z['feedback_records'],allow_nan=False))
    return result,private

def sav_public(fit):
    # All per-origin initialization/path/shock vectors intentionally remain private.
    return dict(refit_index=fit.refit_index,status=fit.status,coefficients=fit.coefficients.tolist(),
        scale=fit.scale,initial_quantile=fit.initial_quantile,objective=fit.objective,
        selected_start=fit.selected_start,starts=[asdict(x) for x in fit.starts],
        training_count=len(fit.training_origins),training_first=int(fit.training_origins[0]),
        training_last=int(fit.training_origins[-1]),initialization_count=len(fit.initialization_origins),
        initialization_first=int(fit.initialization_origins[0]),initialization_last=int(fit.initialization_origins[-1]))

def run_sav(source,h,w,phase,guard):
    ident=f'{cell_name(source,h,w)}-SAV'
    if phase=='evaluation':
        freeze=read_json(PUBLIC/'wp2-selection-freeze.json');row=freeze['cells'][ident]
        if row['status']!='COMPLETE':return dict(status='NA',reason='VALIDATION_INELIGIBLE',validation_status=row['status']),{}
        if sha(PUBLIC/'wp2'/('validation-'+ident+'.json'))!=row['receipt_sha256']:raise ValueError('VALIDATION_RECEIPT_CHANGED')
    s,cfg,c,_=setup(source,h,w);ids=ids_for(cfg,phase);cache=core.build_label_cache(s.position,h)
    try:z=sav.forecast_sav(cache.headroom,s.position,ids,sav.SAVConfig(h,w,c.refit_step,int(ids[0])),checkpoint=guard)
    except sav.SAVFitError as exc:
        # starts are scalar fit diagnostics. Failed cells never expose partial scores.
        return dict(status='NA',reason=exc.code,failed_refit_index=exc.refit_index,fit_failure=sav_failure_public(exc.diagnostics)),{}
    result=dict(status='COMPLETE',scores=score(cache.peak[ids],z.capacities,ids,h),refit_count=len(z.refits),refits=[sav_public(r) for r in z.refits])
    private=dict(origins=ids,capacities=z.capacities,peak=cache.peak[ids],floor=np.abs(s.position[ids]),headroom_quantiles=z.headroom_quantiles)
    for j,r in enumerate(z.refits):
        for k in ('initialization_origins','training_origins','training_shock_origins','path_origins','normalized_path'):private[f'refit{j}_{k}']=getattr(r,k)
    return result,private

def run_cell(phase,source,h,w,method):
    freeze_hash=check_execution_freeze();guard=Guard()
    ident=f'{cell_name(source,h,w)}-{method}';out=PUBLIC/'wp2'/(phase+'-'+ident+'.json')
    if out.exists():raise FileExistsError('CELL_ALREADY_HAS_RECEIPT')
    started=utc();arrays={}
    try:
        guard()
        signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(RuntimeError('RESOURCE_HARD_WALL')));signal.alarm(600)
        if method=='SAV':result,arrays=run_sav(source,h,w,phase,guard)
        elif phase=='validation':result,arrays=run_aci_validation(source,h,w,method[4:],guard)
        else:result,arrays=run_aci_evaluation(source,h,w,method[4:],guard)
        guard()
    except Exception as exc:
        code=getattr(exc,'code',str(exc) if str(exc).startswith(('RESOURCE_','TRACE_','TARGET_','LOSS_','ORIGIN_','EXECUTABLE_')) else type(exc).__name__)
        result=dict(status='NA',reason=code,exception_class=type(exc).__name__);arrays={}
    finally:signal.alarm(0)
    result.update(source=source,horizon=h,window=w,method=method,phase=phase,analysis_status='post-result / exploratory',
        executable_freeze_sha256=freeze_hash,started_utc=started,ended_utc=utc(),resources=guard.summary())
    if arrays:result['private_artifact']=save_private(PRIVATE/'wp2'/(phase+'-'+ident+'.npz'),**arrays)
    result['resources']=guard.summary()
    write_json_new(out,result)
    print(json.dumps({k:result.get(k) for k in ('phase','source','horizon','window','method','status','reason','scores','resources')},allow_nan=False),flush=True)
    return result

def freeze_selection():
    check_execution_freeze();cells={};spec=read_json(ROOT/SPEC)
    for source,cfg in spec['sources'].items():
        for h in spec['horizons']:
            for w in cfg['windows']:
                for method in ('ACI_F','ACI_QR','SAV'):
                    ident=f'{cell_name(source,h,w)}-{method}';p=PUBLIC/'wp2'/('validation-'+ident+'.json');z=read_json(p)
                    cells[ident]=dict(status=z['status'],reason=z.get('reason'),receipt_sha256=sha(p),selected_gamma=z.get('selection',{}).get('gamma'))
    result=dict(status='FROZEN_BEFORE_WP2_EVALUATION',created_utc=utc(),cells=cells,cell_count=len(cells))
    write_json_new(PUBLIC/'wp2-selection-freeze.json',result);print(json.dumps(result),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=('cell','freeze'));p.add_argument('--phase',choices=('validation','evaluation'));p.add_argument('--source');p.add_argument('--horizon',type=int);p.add_argument('--window',type=int);p.add_argument('--method',choices=('ACI_F','ACI_QR','SAV'));a=p.parse_args()
    if a.operation=='freeze':freeze_selection()
    else:run_cell(a.phase,a.source,a.horizon,a.window,a.method)

if __name__=='__main__':main()
