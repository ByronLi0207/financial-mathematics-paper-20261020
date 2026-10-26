"""Post-result v5 diagnostics; no archive overwrite, tuning or source fetching.

The artificial lookahead control is deliberately invalid and cannot be used to
issue a real forecast. Default CLI operations write only new aggregate outputs.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import time

import numpy as np

from conditional_features import (build_features, fit_feature_transform,
    transform_features, response_scale, neighbor_quantile)
from conditional_quantile import fit_quantile_ridge, QuantileFitError
from conditional_sources import load_source
from conditional_study import StudyConfig, issue_historical, score_predictions, summarize_scores
import study_core as core

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results/revision-20261023/v5-novelty'
PAIRED = 'results/revision-20261022/paired-comparisons.csv'
PAIRED_HASH = 'a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def write_new(name, result):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')


def clock_blocks(first, last, step):
    """First, floor-middle, last complete block; no financial argument."""
    count = (last - first + 1) // step
    if count < 3:
        raise ValueError('at least three complete clock blocks required')
    return tuple(np.arange(first + j * step, first + (j + 1) * step, dtype=np.int64)
                 for j in (0, (count - 1) // 2, count - 1))


def training_pool(refit, horizon, window, illegal):
    end = refit if illegal else refit - horizon
    first = end - window + 1
    if min(first, horizon, window) < 0 or horizon < 1 or window < 1:
        raise ValueError('invalid pool')
    return np.arange(first, end + 1, dtype=np.int64)


def loss_decomposition(original_reference, matched_reference, estimator):
    r, f, q = map(Decimal, (original_reference, matched_reference, estimator))
    if not all(v.is_finite() and v >= 0 for v in (r, f, q)) or min(r, f) <= 0:
        raise ValueError('nonpositive reference or invalid loss')
    with localcontext() as ctx:
        ctx.prec = 60
        a, b, total = f-r, q-f, q-r
        return dict(original_reference_mean_pinball=str(r), matched_reference_mean_pinball=str(f),
            estimator_mean_pinball=str(q), length_update_difference_native=str(a),
            estimator_difference_native=str(b), total_difference_native=str(total),
            length_update_difference_percent_original_reference=str(100*a/r),
            estimator_difference_percent_original_reference=str(100*b/r),
            total_difference_percent_original_reference=str(100*total/r),
            estimator_difference_percent_matched_reference=str(100*b/f),
            exact_additivity_residual_native=str(a+b-total))


def gain_decomposition():
    path = ROOT / PAIRED
    if sha(path) != PAIRED_HASH:
        raise ValueError('paired archive hash mismatch')
    with path.open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    def selected(right_window, right_method):
        matches = [r for r in rows if r['source']=='fx_hourly' and r['horizon']=='6'
            and r['left_window']=='2880' and r['left_method']=='QR'
            and r['right_window']==str(right_window) and r['right_method']==right_method]
        if len(matches) != 1:
            raise ValueError('contrast identity mismatch')
        return matches[0]
    primary, matched = selected(720,'rolling_F'), selected(2880,'frozen_F')
    keys = ('origin_count','first_source_index','last_source_index','mean_pinball_left')
    if any(primary[k] != matched[k] for k in keys):
        raise ValueError('paired origin or estimator identity mismatch')
    result = loss_decomposition(primary['mean_pinball_right'], matched['mean_pinball_right'],
                                primary['mean_pinball_left'])
    return dict(status='COMPLETE', analysis_status='post-result / exploratory',
        scope='Descriptive bridge; joint history/update change is not a separately identified causal effect.',
        source=PAIRED, source_sha256=PAIRED_HASH, native_unit='USD',
        primary_contrast_id=primary['contrast_id'], matched_contrast_id=matched['contrast_id'],
        origin_count=int(primary['origin_count']), first_source_index=int(primary['first_source_index']),
        last_source_index=int(primary['last_source_index']), **result)


def first_endpoint_peak_disagreement(position, origins, capacities, horizon):
    x = np.asarray(position, dtype=float)
    for t, capacity in zip(origins, capacities, strict=True):
        t=int(t); capacity=float(capacity)
        if t+horizon >= len(x):
            raise ValueError('incomplete motivating outcome')
        peak=float(np.max(np.abs(x[t:t+horizon+1])))
        endpoint=abs(float(x[t+horizon]))
        if endpoint <= capacity < peak:
            return dict(origin=t, horizon=horizon, report=capacity, floor=abs(float(x[t])),
                peak=peak, endpoint_absolute=endpoint, endpoint_signed=float(x[t+horizon]),
                positions=x[t:t+horizon+1].tolist(),
                selection_rule='earliest eligible issue origin; absolute endpoint <= clean F report < sampled peak')
    return None


def issue_block(position, dates, origins, config, parameters, illegal, checkpoint=None):
    """Same original machinery, with one explicit altered training endpoint."""
    origins=np.asarray(origins, dtype=np.int64)
    if len(origins)==0 or np.any(np.diff(origins)!=1) or len(origins)>config.refit_step:
        raise ValueError('one contiguous refit block required')
    x=np.asarray(position, dtype=float); r=int(origins[0]); h=config.horizon
    cache=core.build_label_cache(x,h)
    features=build_features(x, dates, short_scale=config.short_scale, long_scale=config.long_scale,
                            nominal_gap_seconds=config.nominal_gap_seconds)
    pool=training_pool(r,h,config.window,illegal)
    if pool[0]<features.valid_from or cache.label_end[pool[-1]]>=len(x):
        raise ValueError('inadequate or incomplete label cache')
    immature=int(np.count_nonzero(cache.label_end[pool]>r))
    if immature != (h if illegal else 0):
        raise ValueError('maturity control mismatch')
    fit_transform=fit_feature_transform(features.values[pool])
    train=transform_features(features.values[pool],fit_transform,nearest=False)
    train_nearest=transform_features(features.values[pool],fit_transform,nearest=True)
    y=cache.headroom[pool]; scale=response_scale(y,x[pool])
    fit=fit_quantile_ridge(np.column_stack((np.ones(len(pool)),train)), y/scale,
        tau=.95, penalty=parameters['QR'], checkpoint=checkpoint)
    detail=dict(refit_origin=r, first_training_origin=int(pool[0]), last_training_origin=int(pool[-1]),
        training_count=len(pool), latest_label_end=int(cache.label_end[pool[-1]]),
        immature_label_count=immature, qr_iterations=fit.iterations, qr_gap=fit.duality_gap,
        qr_gap_tolerance=fit.gap_tolerance,
        qr_primal_residual=fit.primal_residual, qr_primal_tolerance=fit.primal_tolerance,
        qr_dual_residual=fit.dual_residual, qr_dual_tolerance=fit.dual_tolerance)
    query=transform_features(features.values[origins],fit_transform,nearest=False)
    query_nearest=transform_features(features.values[origins],fit_transform,nearest=True)
    floor=np.abs(x[origins]); out={k:np.empty(len(origins)) for k in ('QR','KNN','F')}
    rank=core.exact_rank(len(pool),19,20)
    fhead=core.order_statistic(y,rank)
    for j,t in enumerate(origins):
        qhead=scale*float(fit.coefficients[0]+query[j]@fit.coefficients[1:])
        khead,_=neighbor_quantile(train_nearest,query_nearest[j],y,pool,parameters['KNN'])
        out['QR'][j]=floor[j]+max(0.,qhead)
        out['KNN'][j]=floor[j]+max(0.,khead)
        out['F'][j]=floor[j]+fhead
        if checkpoint is not None:
            checkpoint(dict(stage='issue',origin=int(t)))
    if any(not np.isfinite(v).all() or np.any(v<floor) for v in out.values()):
        raise ValueError('invalid issue report')
    return out, detail


class Guard:
    def __init__(self):
        self.start=time.monotonic(); self.started_utc=utc(); self.last_probe=-math.inf
        self.peak_rss_bytes=0; self.maximum_observed_os_threads=0; self.thread_snapshots=0

    def __call__(self, _progress=None):
        elapsed=time.monotonic()-self.start
        rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if platform.system()!='Darwin': rss*=1024
        self.peak_rss_bytes=max(self.peak_rss_bytes,rss)
        if elapsed>=540: raise RuntimeError('RESOURCE_WALL')
        if rss>=2*1024**3: raise RuntimeError('RESOURCE_RSS')
        if elapsed-self.last_probe>=1:
            from run_study import parse_thread_snapshot
            proc=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],capture_output=True,text=True,check=True,timeout=3)
            n=parse_thread_snapshot(proc.stdout,os.getpid())
            self.maximum_observed_os_threads=max(self.maximum_observed_os_threads,n)
            self.thread_snapshots+=1; self.last_probe=elapsed
            if n>2: raise RuntimeError('RESOURCE_THREADS')

    def summary(self):
        self()
        return dict(started_utc=self.started_utc,ended_utc=utc(),elapsed_seconds=time.monotonic()-self.start,
            peak_rss_bytes=self.peak_rss_bytes,maximum_observed_os_threads=self.maximum_observed_os_threads,
            thread_snapshot_count=self.thread_snapshots,requested_numerical_threads=1,
            internal_wall_limit_seconds=540,hard_wall_limit_seconds=600,rss_limit_bytes=2*1024**3)


def setup(source_id):
    specpath=ROOT/'protocol/revision-20261022/study-spec.json'
    selectionpath=ROOT/'protocol/revision-20261022/selection-freeze.json'
    spec=json.loads(specpath.read_text()); cfg=spec['sources'][source_id]
    source=load_source(ROOT/cfg['input_relative_path'],source_id,
        expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
    w=cfg['primary_window']; h=6
    selected=json.loads(selectionpath.read_text())['cells']
    parameters={}
    for family in ('QR','KNN'):
        choices=[r for r in selected if (r['source'],r['horizon'],r['window'],r['family'])==(source_id,h,w,family)]
        if len(choices)!=1 or choices[0]['status']!='SELECTED':raise ValueError('original selection missing')
        parameters[family]=choices[0]['parameter']
    config=StudyConfig(h,w,cfg['refit_step'],cfg['short_scale'],cfg['long_scale'],cfg['nominal_gap_seconds'])
    identity=dict(source=source_id,raw_source_sha256=source.sha256,raw_source_bytes=source.bytes,
        spec_path=str(specpath.relative_to(ROOT)),spec_sha256=sha(specpath),
        selection_path=str(selectionpath.relative_to(ROOT)),selection_sha256=sha(selectionpath),
        code_sha256=sha(__file__),design_sha256=sha(ROOT/'notes/revision-v5-novelty/analysis-design.md'))
    return source,cfg,config,parameters,identity


def leakage_experiment(source_id):
    guard=Guard(); guard()
    source,cfg,config,params,identity=setup(source_id)
    blocks=clock_blocks(cfg['evaluation_origin_first'],cfg['evaluation_origin_last'],config.refit_step)
    ids=np.concatenate(blocks); capacities={mode:{k:[] for k in ('QR','KNN','F')} for mode in ('clean','oracle_leakage')}
    diagnostics=[]; failures=[]
    for block in blocks:
        for mode,illegal in (('clean',False),('oracle_leakage',True)):
            try:
                reports,detail=issue_block(source.position,source.dates,block,config,params,illegal,guard)
                for k in reports: capacities[mode][k].append(reports[k])
                diagnostics.append(dict(mode=mode,status='COMPLETE',**detail))
            except (QuantileFitError,RuntimeError) as exc:
                code=getattr(exc,'code',str(exc))
                failures.append(dict(mode=mode,refit_origin=int(block[0]),status='FAILED',reason=code))
                # Do not substitute a different fit or a partial score after a failed block.
                break
        if failures: break
    rows=[]
    if not failures:
        cache=core.build_label_cache(source.position,config.horizon)
        floor=np.abs(source.position[ids]); peak=cache.peak[ids]
        for family in ('QR','KNN','F'):
            means={}
            for mode in ('clean','oracle_leakage'):
                c=np.concatenate(capacities[mode][family])
                s=summarize_scores(score_predictions(peak,c,floor,ids)); means[mode]=s
            clean,illegal=means['clean'],means['oracle_leakage']
            d=illegal['mean_pinball']-clean['mean_pinball']
            rows.append(dict(method=family,parameter=params.get(family),clean=clean,oracle_leakage=illegal,
                illegal_minus_clean_mean_pinball=d,
                illegal_minus_clean_percent=100*d/clean['mean_pinball'] if clean['mean_pinball'] else None,
                interpretation='negative is optimistic apparent loss; positive is deterioration; neither is a deployable forecast'))
    result=dict(status='COMPLETE' if not failures else 'FAILED',analysis_status='post-result / exploratory',
        scope='Three preselected original clock blocks per source; deliberately invalid training labels; no tuning, no full-sample or primary claim.',
        identity=identity,horizon=config.horizon,window=config.window,refit_step=config.refit_step,
        native_unit=cfg['native_unit'],origin_count=len(ids),
        block_ranges=[dict(first=int(b[0]),last=int(b[-1]),count=len(b)) for b in blocks],
        origin_indices_sha256=hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest(),
        per_refit_immature_label_count=config.horizon,
        parameters=params,rows=rows,fit_diagnostics=diagnostics,failures=failures,resources=guard.summary())
    return result


def motivating_window():
    source,cfg,config,params,identity=setup('nyfed_weekly')
    ids=np.arange(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,dtype=np.int64)
    cache=core.build_label_cache(source.position,config.horizon)
    caps=[]; refits=[]
    for t in ids:
        r=cfg['evaluation_origin_first']+config.refit_step*((int(t)-cfg['evaluation_origin_first'])//config.refit_step)
        caps.append(issue_historical(source.position,cache,issue=int(t),refit=r,window=config.window,step=config.refit_step)[0])
        refits.append(r)
    found=first_endpoint_peak_disagreement(source.position,ids,caps,config.horizon)
    if found is not None:
        j=int(np.flatnonzero(ids==found['origin'])[0]);found['refit_origin']=int(refits[j])
        found['dates']=[str(d) for d in source.dates[found['origin']:found['origin']+config.horizon+1]]
        found['absolute_positions']=[abs(x) for x in found['positions']]
        found['dates_are']='economic dates in the downloaded vintage; not original public release timestamps'
    return dict(status='COMPLETE' if found else 'NO_QUALIFYING_WINDOW',analysis_status='post-result / exploratory',
        identity=identity,source_series_key='PDPOSGS-B',native_unit=cfg['native_unit'],
        original_source_url='https://markets.newyorkfed.org/api/pd/get/PDPOSGS-B.csv',
        eligible_first_origin=int(ids[0]),eligible_last_origin=int(ids[-1]),
        method='clean frozen F',window=config.window,example=found,
        limitation='Selected deterministic illustration; not typicality, holdout validation, or an intrarecord peak.')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=('decomposition','motivating-window','leakage'))
    parser.add_argument('--source',choices=('fx_hourly','nyfed_weekly'))
    args=parser.parse_args(argv)
    if args.operation=='decomposition':
        result=gain_decomposition();name='gain-decomposition.json'
    elif args.operation=='motivating-window':
        result=motivating_window();name='motivating-window.json'
    else:
        if args.source is None:parser.error('--source required for leakage')
        def stop(_signum,_frame):raise RuntimeError('RESOURCE_HARD_WALL')
        signal.signal(signal.SIGALRM,stop);signal.setitimer(signal.ITIMER_REAL,600)
        try:result=leakage_experiment(args.source)
        finally:signal.setitimer(signal.ITIMER_REAL,0)
        name='label-maturity-'+args.source+'.json'
    write_new(name,result)
    print(json.dumps(dict(output=str((OUT/name).relative_to(ROOT)),sha256=sha(OUT/name),
                          status=result['status']),indent=2))


if __name__=='__main__':main()
