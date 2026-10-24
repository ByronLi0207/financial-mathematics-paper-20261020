"""E3 common-menu extension. Original estimators and archives are read-only."""
from __future__ import annotations
import os
import sys
sys.dont_write_bytecode=True
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import resource
import signal
import subprocess
import time
from datetime import datetime,timezone
import numpy as np
from conditional_features import build_features
from conditional_quantile import QuantileFitError
from conditional_sources import load_source
from conditional_study import (StudyConfig,conditional_forecast,score_predictions,
                               summarize_scores,select_parameter)
from run_study import StudyStop,parse_thread_snapshot
from study_core import build_label_cache

ROOT=Path(__file__).resolve().parent
PRIOR=Path('/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023')
PUBLIC=ROOT/'results/supervisor-20261023/e3'
PRIVATE=ROOT/'.scratch/supervisor-20261023/e3'
PENALTIES=(.001,.01,.1,1.,10.)
CELLS=tuple((s,h,w) for s,windows in [('nyfed_weekly',(52,260)),('fx_hourly',(720,2880))]
            for h in (6,24) for w in windows)
INTERNAL_SECONDS=3600.
HARD_SECONDS=3660.
CODE_FILES=('supervisor_e3.py','conditional_study.py','conditional_features.py',
            'conditional_quantile.py','conditional_sources.py','study_core.py')


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds')
def cell_id(s,h,w):return f'{s}-h{h}-w{w}'


def dump(path,value,*,exclusive=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x' if exclusive else 'w') as stream:
        # The unchanged solver deliberately exposes MappingProxyType diagnostics.
        json.dump(value,stream,indent=2,allow_nan=False,default=dict);stream.write('\n')


def freeze_selection(rows,count):
    return select_parameter(rows,PENALTIES,expected_count=count)


def checked_trace(path,origins,peak,mean_pinball):
    with np.load(path,allow_pickle=False) as values:
        result={key:np.array(values[key],copy=True) for key in ('origins','capacity','peak','pinball')}
    if (not np.array_equal(result['origins'],origins) or not np.array_equal(result['peak'],peak)
            or any(result[k].shape!=np.asarray(origins).shape for k in result)
            or not all(np.isfinite(result[k]).all() for k in result)):
        raise ValueError('archive origin/peak alignment failed')
    error=result['peak']-result['capacity']
    actual=.95*np.maximum(error,0)+.05*np.maximum(-error,0)
    # Original score weights are float(19/20) and float(1/20).
    if not np.array_equal(actual,result['pinball']):raise ValueError('archive loss identity failed')
    mean=math.fsum(map(float,result['pinball']))/len(origins)
    if not math.isclose(mean,float(mean_pinball),rel_tol=2e-14,abs_tol=1e-12):
        raise ValueError('archive mean reconciliation failed')
    return result


def paired_loss_difference(old,new):
    if (not np.array_equal(old['origins'],new['origins'])
            or not np.array_equal(old['peak'],new['peak'])):
        raise ValueError('paired origins/peaks differ')
    difference=np.asarray(new['pinball'])-np.asarray(old['pinball'])
    if difference.ndim!=1 or not np.isfinite(difference).all():raise ValueError('invalid paired losses')
    return difference


class Guard:
    """E3-only declared wall limit; unchanged resource measurement conventions."""
    def __init__(self,folder,identity):
        self.start=time.monotonic();self.folder=folder;self.last_write=-math.inf
        self.resources=dict(started_utc=now(),elapsed_seconds=0.,peak_rss_bytes=0,
            requested_numerical_threads=1,maximum_observed_os_threads=0,
            thread_snapshot_count=0,thread_probe_status='UNVERIFIED',cell_id=identity,
            internal_wall_seconds=INTERNAL_SECONDS,hard_wall_seconds=HARD_SECONDS,
            internal_rss_bytes=1610612736,public_rss_bytes=2147483648)

    def __call__(self,**progress):
        elapsed=time.monotonic()-self.start
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        probe=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],
                             capture_output=True,text=True,check=True,timeout=5)
        threads=parse_thread_snapshot(probe.stdout,os.getpid())
        self.resources.update(elapsed_seconds=elapsed,peak_rss_bytes=max(rss,self.resources['peak_rss_bytes']),
            maximum_observed_os_threads=max(threads,self.resources['maximum_observed_os_threads']),
            thread_snapshot_count=self.resources['thread_snapshot_count']+1,thread_probe_status='PASS',
            checkpoint_utc=now(),**progress)
        if elapsed-self.last_write>=5:
            dump(self.folder/'progress.json',self.resources);self.last_write=elapsed
        if threads>2:raise StudyStop('RESOURCE_THREADS')
        if rss>=1610612736:raise StudyStop('RESOURCE_RSS')
        if elapsed>=INTERNAL_SECONDS:raise StudyStop('RESOURCE_WALL')


def source(s,spec):
    cfg=spec['sources'][s]
    original=PRIOR/cfg['input_relative_path'];target=PRIVATE/'sources'/original.name
    target.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    if not target.exists():
        raw=original.read_bytes()
        if len(raw)!=cfg['bytes'] or hashlib.sha256(raw).hexdigest()!=cfg['sha256']:
            raise ValueError('source identity failed')
        descriptor=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(descriptor,'wb') as stream:stream.write(raw)
    return load_source(target,s,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])


def save_forecast(path,forecast,peak,scores):
    np.savez(path,origins=forecast.origins,capacity=forecast.capacities,peak=peak,
        floor=forecast.floors,pinball=scores.pinball,refit_indices=forecast.refit_indices)
    os.chmod(path,0o600)


def four_archive(s,h,w,data,cache,origins):
    identity=cell_id(s,h,w)
    public=PRIOR/'results/revision-20261023/parsimonious'/f'{identity}.json'
    private=PRIOR/'.scratch/v3-parsimonious'/identity/'numeric-traces.npz'
    record=json.loads(public.read_text())
    rows=[dict(parameter=r['penalty'],status=r['status'],origin_count=52 if s=='nyfed_weekly' else 1440,
               mean_pinball=r['mean_pinball']) for r in record['candidates']]
    selection=freeze_selection(rows,52 if s=='nyfed_weekly' else 1440)
    if record['status']!='COMPLETE' or selection['status']!='SELECTED' or selection['parameter']!=record['selected_penalty']:
        raise ValueError('four-predictor selection reconciliation failed')
    if len({r['mean_pinball'] for r in rows})!=len(PENALTIES):raise ValueError('four-predictor archive has exact tie')
    trace=checked_trace(private,origins,cache.peak[origins],record['evaluation']['mean_pinball'])
    scores=score_predictions(trace['peak'],trace['capacity'],np.abs(data.position[origins]),origins)
    summary=summarize_scores(scores)
    for key,value in summary.items():
        expected=record['evaluation'][key]
        if isinstance(value,float):
            if not math.isclose(value,expected,rel_tol=2e-14,abs_tol=1e-12):raise ValueError('four-predictor summary mismatch')
        elif value!=expected:raise ValueError('four-predictor summary mismatch')
    for detail in record['fit_diagnostics']:
        if not 1<=detail['iterations']<=10000 or detail['gap']>detail['gap_tolerance']:
            raise ValueError('four-predictor convergence reconciliation failed')
    target=PRIVATE/identity/'four-predictor-traces.npz'
    if not target.exists():
        target.write_bytes(private.read_bytes());os.chmod(target,0o600)
    return dict(status='VERIFIED_ARCHIVAL_REUSE',source_json_sha256=sha(public),source_trace_sha256=sha(private),
        selected_penalty=selection['parameter'],validation_candidates=rows,evaluation=summary,
        prior_resources=record['resources'],origin_count=len(origins),source_code_sha256=sha(PRIOR/'parsimonious_v3.py'),
        selection_policy_compatibility='all declared candidates complete; no exact ties; original strict selection agrees')


def run_cell(s,h,w):
    if (s,h,w) not in CELLS:raise ValueError('undeclared E3 cell')
    identity=cell_id(s,h,w);folder=PUBLIC/identity;folder.mkdir(parents=True,exist_ok=False)
    private=PRIVATE/identity;private.mkdir(parents=True,exist_ok=False,mode=0o700)
    spec_path=ROOT/'protocol/revision-20261022/study-spec.json'
    spec=json.loads(spec_path.read_text());cfg=spec['sources'][s]
    guard=Guard(folder,identity)
    result=dict(source=s,horizon=h,window=w,status='INITIALIZING',post_result_exploratory=True,
        feature_count_without_intercept=33,penalties=list(PENALTIES),selected_penalty=None,candidates=[],
        code_hashes={name:sha(ROOT/name) for name in CODE_FILES},spec_sha256=sha(spec_path),
        design_sha256=sha(ROOT/'results/supervisor-20261023/e3-design.md'),
        source_sha256=cfg['sha256'],source_bytes=cfg['bytes'])
    def timeout(*_):raise StudyStop('RESOURCE_HARD_WALL')
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,HARD_SECONDS)
    try:
        data=source(s,spec);cache=build_label_cache(data.position,h)
        origins=lambda phase:np.arange(cfg[phase+'_origin_first'],cfg[phase+'_origin_last']+1,dtype=np.int64)
        val,ev=origins('validation'),origins('evaluation')
        config=StudyConfig(h,w,cfg['refit_step'],cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds'])
        result['date_ranges']={phase:dict(first=str(data.dates[ids[0]]),last=str(data.dates[ids[-1]]),
             count=len(ids)) for phase,ids in [('validation',val),('evaluation',ev)]}
        result['four_predictor_archive']=four_archive(s,h,w,data,cache,ev)
        guard(stage='source_and_four_archive_verified')
        for lam in PENALTIES:
            started=time.monotonic();row=dict(parameter=lam,status='INCOMPLETE')
            try:
                forecast=conditional_forecast(data.position,data.dates,val,config,'QR',lam,checkpoint=guard)
                scores=score_predictions(cache.peak[val],forecast.capacities,forecast.floors,val)
                row.update(status='COMPLETE',origin_count=len(val),mean_pinball=summarize_scores(scores)['mean_pinball'],
                           fit_diagnostics=forecast.fit_diagnostics)
                save_forecast(private/f'validation-lambda-{lam:g}.npz',forecast,cache.peak[val],scores)
            except QuantileFitError as error:
                row.update(status='FAILED',reason=error.code,solver_diagnostics=error.diagnostics,
                           failure_context=getattr(error,'failure_context',None))
                partial=getattr(error,'partial_forecast',None)
                if partial is not None and len(partial.origins):
                    scores=score_predictions(cache.peak[partial.origins],partial.capacities,partial.floors,partial.origins)
                    save_forecast(private/f'validation-lambda-{lam:g}-INCOMPLETE.npz',partial,cache.peak[partial.origins],scores)
            finally:
                row['elapsed_seconds']=time.monotonic()-started
                result['candidates'].append(row)
                dump(folder/'result.json',result)
            print(json.dumps(dict(cell=identity,phase='validation',parameter=lam,status=row['status'],
                                  elapsed_seconds=row['elapsed_seconds'])),flush=True)
        selection=freeze_selection(result['candidates'],len(val))
        result['selection']=selection;result['selected_penalty']=selection['parameter']
        dump(folder/'selection-before-evaluation.json',dict(frozen_utc=now(),selection=selection,
            candidates=result['candidates'],code_hashes=result['code_hashes'],spec_sha256=result['spec_sha256']),exclusive=True)
        if selection['status']!='SELECTED':result['status']='INELIGIBLE'
        else:
            result['status']='EVALUATING';dump(folder/'result.json',result)
            print(json.dumps(dict(cell=identity,phase='evaluation',selected_penalty=selection['parameter'])),flush=True)
            started=time.monotonic()
            try:
                forecast=conditional_forecast(data.position,data.dates,ev,config,'QR',selection['parameter'],checkpoint=guard)
                scores=score_predictions(cache.peak[ev],forecast.capacities,forecast.floors,ev)
                result.update(status='COMPLETE',evaluation=summarize_scores(scores),fit_diagnostics=forecast.fit_diagnostics)
                save_forecast(private/'numeric-traces.npz',forecast,cache.peak[ev],scores)
                result['private_evaluation_trace_sha256']=sha(private/'numeric-traces.npz')
            except QuantileFitError as error:
                result.update(status='EVALUATION_FAILED',reason=error.code,solver_diagnostics=error.diagnostics,
                              failure_context=getattr(error,'failure_context',None))
                partial=getattr(error,'partial_forecast',None)
                if partial is not None and len(partial.origins):
                    scores=score_predictions(cache.peak[partial.origins],partial.capacities,partial.floors,partial.origins)
                    save_forecast(private/'evaluation-INCOMPLETE.npz',partial,cache.peak[partial.origins],scores)
            result['evaluation_elapsed_seconds']=time.monotonic()-started
        guard(stage='terminal')
    except (StudyStop,subprocess.SubprocessError,OSError,ValueError) as error:
        result.update(status='INCOMPLETE',reason=getattr(error,'code',type(error).__name__))
        present={r['parameter'] for r in result['candidates']}
        for lam in PENALTIES:
            if lam not in present:result['candidates'].append(dict(parameter=lam,status='INCOMPLETE',reason='CELL_STOPPED_BEFORE_CANDIDATE'))
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        result['resources']=guard.resources
        result['resources']['final_elapsed_seconds']=time.monotonic()-guard.start
        dump(folder/'result.json',result)
    print(json.dumps(dict(cell=identity,status=result['status'],selected_penalty=result['selected_penalty'],
                         resources=result['resources'])),flush=True)
    return result


def run_all():
    PRIVATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    queue=[]
    for s,h,w in CELLS:
        identity=cell_id(s,h,w);target=PUBLIC/identity/'result.json'
        if target.exists():raise ValueError('existing E3 attempt must not be silently overwritten')
        completed=subprocess.run([sys.executable,str(Path(__file__)), '--source',s,'--horizon',str(h),'--window',str(w)],
                                 timeout=HARD_SECONDS+15)
        record=json.loads(target.read_text()) if target.exists() else dict(status='NO_TERMINAL_RECEIPT')
        queue.append(dict(source=s,horizon=h,window=w,exit_code=completed.returncode,status=record['status']))
        dump(PUBLIC/'queue.json',queue)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run-all',action='store_true')
    parser.add_argument('--source',choices=('nyfed_weekly','fx_hourly'))
    parser.add_argument('--horizon',type=int);parser.add_argument('--window',type=int)
    args=parser.parse_args()
    run_all() if args.run_all else run_cell(args.source,args.horizon,args.window)
