"""One bounded execution of the published R6 contract.

Importing this module opens no financial inputs and computes no labels. The
only real-data entry point is the explicit --execute command. Original model,
empirical-rank, alignment and score implementations are imported unchanged.
"""
from __future__ import annotations
import os
import sys
sys.dont_write_bytecode = True
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import re
import resource
import signal
import statistics
import subprocess
import time
import numpy as np

from conditional_sources import load_source
from conditional_study import (StudyConfig, conditional_forecast,
                               score_predictions, summarize_scores)
from empirical_headroom import predict as empirical_predict
from round2_panel_sources import align_source
from study_core import build_label_cache
from run_study import parse_thread_snapshot

ROOT = Path(__file__).resolve().parent
DESIGN = Path('protocol/supervisor-20261023/r6-design.md')
DESIGN_COMMIT = '6c0eef44c46a0ff525264b13ae1dae9b821ad3c2'
DESIGN_SHA256 = 'de301f131426ed9b185451d87e3aee1726d978dd2d55ffd322efc02477b6bbae'
PUBLIC = ROOT/'results/supervisor-20261023/r6'
PRIVATE = ROOT/'.scratch/r6-20261023/run'
FINITE_IDS = ('0.001', '0.01', '0.1', '1', '10')
ALL_IDS = FINITE_IDS + ('I',)
REPORTS = ('F', 'I', 'R0', 'R1', 'R2', 'R3')
ROW_FIELDS = ('phase','source','series_key','horizon','window','report','status',
    'reason','selected_id','origin_count','mean_pinball','mean_capacity',
    'mean_extra_allowance','strict_breach_count','strict_breach_rate',
    'mean_positive_overrun','conditional_mean_overrun',
    'conditional_overrun_denominator','conditional_overrun_undefined_reason',
    'mean_unused_allowance','percent_vs_F','trace_sha256')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value, *, exclusive=False):
    with Path(path).open('x' if exclusive else 'w') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False,
                  default=lambda x: x.item() if isinstance(x, np.generic) else dict(x))
        stream.write('\n')


def write_csv(path, rows, fields=None):
    fields = list(fields or dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('x', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader(); writer.writerows(rows)


def read_contract(path=None):
    raw = Path(path or ROOT/DESIGN).read_bytes()
    if hashlib.sha256(raw).hexdigest() != DESIGN_SHA256:
        raise ValueError('FROZEN_DESIGN_HASH_MISMATCH')
    blocks = re.findall(r'```json\s*\n(.*?)\n```', raw.decode(), re.S)
    if len(blocks) != 1:
        raise ValueError('FROZEN_CONTRACT_COUNT')
    spec = json.loads(blocks[0])
    if (spec['expected_groups'] != {'retro':30,'inspected':56}
            or spec['reports'] != list(REPORTS)
            or tuple(f'{p:g}' for p in spec['finite_penalties']) != FINITE_IDS
            or spec['common_purge'] != 24):
        raise ValueError('FROZEN_CONTRACT_IDENTITY')
    return spec


def group_inventory(spec):
    groups = []
    for phase in ('retro', 'inspected'):
        for source in ('nyfed_weekly', 'fx_hourly'):
            keys = [s['series_key'] for s in spec['weekly_series']] if source == 'nyfed_weekly' else ['fx_hourly']
            for key in keys:
                for h in spec['horizons']:
                    for w in spec['sources'][source][phase+'_windows']:
                        groups.append(dict(phase=phase,source=source,series_key=key,horizon=h,window=w))
    for phase, n in spec['expected_groups'].items():
        if sum(g['phase']==phase for g in groups) != n:
            raise ValueError('GROUP_INVENTORY_COUNT')
    return groups


def identity(group):
    return f"{group['phase']}-{group['series_key']}-h{group['horizon']}-w{group['window']}"


class LimitStop(Exception):
    def __init__(self, code):
        self.code=code; super().__init__(code)


class Guard:
    """Snapshot observations and a signal deadline; no monitoring thread."""
    def __init__(self, start, limits, progress_path):
        self.start=start; self.group_start=start; self.limits=limits
        self.progress_path=Path(progress_path); self.last_probe=-math.inf
        self.resources=dict(requested_numerical_threads=1,maximum_observed_os_threads=0,
            peak_rss_bytes=0,thread_snapshot_count=0,thread_probe_status='UNVERIFIED')

    def begin_group(self):
        self.group_start=time.monotonic()
        remaining=self.limits['run_wall_seconds']-(self.group_start-self.start)
        if remaining<=0: raise LimitStop('RUN_TIME_LIMIT')
        signal.setitimer(signal.ITIMER_REAL,min(self.limits['group_wall_seconds'],remaining))

    def __call__(self, **progress):
        current=time.monotonic(); elapsed=current-self.start
        if elapsed>=self.limits['run_wall_seconds']: raise LimitStop('RUN_TIME_LIMIT')
        if current-self.group_start>=self.limits['group_wall_seconds']: raise LimitStop('GROUP_TIME_LIMIT')
        if current-self.last_probe<.25: return
        rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if platform.system()!='Darwin': rss*=1024
        if platform.system()=='Darwin':
            probe=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],
                capture_output=True,text=True,check=True,timeout=5)
            threads=parse_thread_snapshot(probe.stdout,os.getpid())
        else:
            line=next(x for x in Path('/proc/self/status').read_text().splitlines() if x.startswith('Threads:'))
            threads=int(line.split()[1])
        self.resources.update(elapsed_seconds=elapsed,group_elapsed_seconds=current-self.group_start,
            peak_rss_bytes=max(rss,self.resources['peak_rss_bytes']),
            maximum_observed_os_threads=max(threads,self.resources['maximum_observed_os_threads']),
            thread_snapshot_count=self.resources['thread_snapshot_count']+1,
            thread_probe_status='PASS',checkpoint_utc=now(),**progress)
        self.last_probe=current; dump(self.progress_path,self.resources)
        if threads>self.limits['max_observed_threads']: raise LimitStop('RESOURCE_THREADS')
        if rss>=self.limits['max_rss_bytes']: raise LimitStop('RESOURCE_RSS')


def failure(exc):
    result=dict(status='FAILED',reason=getattr(exc,'code',type(exc).__name__))
    if hasattr(exc,'diagnostics'): result['solver_diagnostics']=dict(exc.diagnostics)
    if hasattr(exc,'failure_context'): result['failure_context']=exc.failure_context
    return result


class CoreReports:
    """Cache exact report/segment identities, including failed attempts."""
    def __init__(self, position, dates, group, source_config, guard, folder):
        self.position=np.asarray(position); self.dates=np.asarray(dates)
        self.group=group; self.cfg=source_config; self.guard=guard; self.folder=Path(folder)
        self.cache={}; self.labels=build_label_cache(self.position,group['horizon'])

    def segment(self, candidate_id, origins, *, window=None, refit_step=None):
        ids=np.asarray(origins,dtype=np.int64)
        w=window or self.group['window']; step=refit_step or self.cfg['refit_step']
        key=(candidate_id,int(ids[0]),int(ids[-1]),w,step)
        if key in self.cache:
            result=self.cache[key]
            if isinstance(result,Exception): raise result
            return result
        self.guard(stage='segment_start',candidate_id=candidate_id)
        try:
            h=self.group['horizon']
            if candidate_id in ('I','F'):
                p=empirical_predict(self.position,ids,h,w,step)
                if (not np.array_equal(p['origins'],ids)
                        or np.any(p['latest_label_ends']>p['refit_indices'])
                        or np.any(p['refit_indices']>ids)):
                    raise ValueError('EMPIRICAL_HISTORY_MATURITY')
                details=[dict(refit_index=int(r),training_first_origin=int(p['training_first_origins'][j]),
                    training_last_origin=int(p['training_last_origins'][j]),training_count=w,
                    latest_label_end=int(p['latest_label_ends'][j]))
                    for j,r in enumerate(p['refit_indices']) if j==0 or r!=p['refit_indices'][j-1]]
                outputs={name:dict(origins=ids,capacity=p[name],floor=p['floors'],
                    refit_indices=p['refit_indices'],fit_diagnostics=details) for name in ('I','F')}
            elif candidate_id in FINITE_IDS:
                config=StudyConfig(h,w,step,self.cfg['short_scale'],self.cfg['long_scale'],self.cfg['nominal_gap_seconds'])
                p=conditional_forecast(self.position,self.dates,ids,config,'QR',float(candidate_id),checkpoint=self.guard)
                outputs={candidate_id:dict(origins=p.origins,capacity=p.capacities,floor=p.floors,
                    refit_indices=p.refit_indices,fit_diagnostics=list(p.fit_diagnostics))}
            else: raise ValueError('UNDECLARED_CANDIDATE')
            for name,result in outputs.items():
                if not np.array_equal(result['origins'],ids): raise ValueError('SEGMENT_ORIGIN_ALIGNMENT')
                for detail in result['fit_diagnostics']:
                    if (detail['training_count']!=w or detail['latest_label_end']>detail['refit_index']
                            or detail['latest_label_end']!=detail['training_last_origin']+h):
                        raise ValueError('TRAINING_POOL_MATURITY')
                scores=score_predictions(self.labels.peak[ids],result['capacity'],result['floor'],ids)
                result['scores']=scores; result['summary']=summarize_scores(scores)
                path=self.folder/f'{name}-{ids[0]}-{ids[-1]}-w{w}-d{step}.npz'
                with path.open('xb') as stream:
                    np.savez_compressed(stream,origins=ids,capacity=result['capacity'],
                        peak=self.labels.peak[ids],floor=result['floor'],pinball=scores.pinball,
                        strict_breach=scores.strict_breach,overrun=scores.overrun,unused=scores.unused,
                        refit_indices=result['refit_indices'])
                os.chmod(path,0o600)
                result.update(trace_path=path.name,trace_sha256=sha(path))
                dump(path.with_suffix('.json'),dict(candidate_id=name,window=w,refit_step=step,
                    fit_diagnostics=result['fit_diagnostics'],summary=result['summary'],
                    trace_sha256=result['trace_sha256']),exclusive=True)
                self.cache[(name,int(ids[0]),int(ids[-1]),w,step)]=result
            self.guard(stage='segment_complete',candidate_id=candidate_id)
            return self.cache[key]
        except Exception as exc:
            self.cache[key]=exc
            if candidate_id in ('I','F'):
                # The one original empirical call attempts both ranks together.
                # Its failure cannot be retried via the other public report ID.
                for name in ('I','F'):
                    self.cache[(name,int(ids[0]),int(ids[-1]),w,step)]=exc
            dump(self.folder/f'{candidate_id}-{ids[0]}-{ids[-1]}-w{w}-d{step}-FAILED.json',
                dict(candidate_id=candidate_id,origins=[int(ids[0]),int(ids[-1])],
                    expected_origin_count=len(ids),window=w,refit_step=step,
                    attempted_report_ids=['I','F'] if candidate_id in ('I','F') else [candidate_id],
                    failed_utc=now(),**failure(exc)),exclusive=True)
            partial=getattr(exc,'partial_forecast',None)
            if partial is not None and len(partial.origins):
                path=self.folder/f'{candidate_id}-{ids[0]}-{ids[-1]}-INCOMPLETE.npz'
                with path.open('xb') as stream:
                    np.savez_compressed(stream,origins=partial.origins,capacity=partial.capacities,
                                        floor=partial.floors,refit_indices=partial.refit_indices)
                os.chmod(path,0o600)
            raise


def _scored(segment, labels, ids):
    if 'scores' not in segment:
        scores=score_predictions(labels.peak[ids],segment['capacity'],segment['floor'],ids)
        segment=dict(segment,scores=scores,summary=summarize_scores(scores))
    return segment


def run_group(group, spec, position, dates, folder, guard, *, backend_factory=CoreReports):
    progress={}
    try:
        return _run_group(group,spec,position,dates,folder,guard,backend_factory=backend_factory,progress=progress)
    except LimitStop as exc:
        exc.partial_group=interrupted_group(group,progress,exc.code)
        raise


def _run_group(group, spec, position, dates, folder, guard, *, backend_factory, progress):
    from supervisor_r6_rules import select_minimum, select_paired_one_se, rolling_folds
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    cfg=spec['sources'][group['source']]; h=group['horizon']; w=group['window']
    stop=cfg['original_validation_start'] if group['phase']=='retro' else len(position)
    x=np.asarray(position)[:stop]; times=np.asarray(dates)[:stop]
    val=np.arange(cfg[group['phase']+'_validation'][0],cfg[group['phase']+'_validation'][1]+1,dtype=np.int64)
    ev=np.arange(cfg[group['phase']+'_evaluation'][0],cfg[group['phase']+'_evaluation'][1]+1,dtype=np.int64)
    backend=backend_factory(x,times,group,cfg,guard,folder)
    labels=backend.labels if hasattr(backend,'labels') else build_label_cache(x,h)
    folds=rolling_folds(int(val[0]),int(val[-1]),w,cfg['feature_prefix'],cfg['refit_step'],purge=spec['common_purge'])
    result=progress
    result.update(group=group,raw_prefix_count=len(x),selections={},rows=[],validation_candidates=[],
        r3_fold_bounds=[list(f) for f in folds],r3_design_status='NO_EXTRA_FOLDS' if len(folds)==1 else 'PREFIX_PLUS_OUTER_VALIDATION')
    attempts={}
    def attempt(candidate, ids, **kwargs):
        key=(candidate,int(ids[0]),int(ids[-1]),kwargs.get('window'),kwargs.get('refit_step'))
        if key not in attempts:
            if np.array_equal(ids,ev): result['_active_evaluation_candidate']=candidate
            try: attempts[key]=_scored(backend.segment(candidate,ids,**kwargs),labels,ids)
            except LimitStop: raise
            except Exception as exc: attempts[key]=failure(exc)
            result.pop('_active_evaluation_candidate',None)
        return attempts[key]
    outer={}
    for candidate in ALL_IDS:
        item=attempt(candidate,val)
        outer[candidate]=None if item.get('status')=='FAILED' else item['scores'].pinball
        result['validation_candidates'].append(dict(candidate_id=candidate,
            status='FAILED' if outer[candidate] is None else 'COMPLETE',
            reason=item.get('reason'),origin_count=len(val) if outer[candidate] is not None else None,
            mean_pinball=item.get('summary',{}).get('mean_pinball')))
    selections=result['selections']
    selections['R0']=select_minimum(outer,FINITE_IDS)
    selections['R1']=select_minimum(outer,ALL_IDS)
    selections['R2']=select_paired_one_se(outer,val,h,ALL_IDS)
    if len(folds)==1:
        selections['R3']=selections['R2']
    else:
        all_origins=np.concatenate([np.arange(a,b+1,dtype=np.int64) for a,b in folds])
        fold_losses={candidate:[] for candidate in ALL_IDS}
        for a,b in folds[:-1]:
            ids=np.arange(a,b+1,dtype=np.int64)
            for candidate in ALL_IDS:
                item=attempt(candidate,ids)
                fold_losses[candidate].append(None if item.get('status')=='FAILED' else item['scores'].pinball)
        cv={candidate:None if outer[candidate] is None or any(a is None for a in fold_losses[candidate])
            else np.concatenate(fold_losses[candidate]+[outer[candidate]]) for candidate in ALL_IDS}
        selections['R3']=select_paired_one_se(cv,all_origins,h,ALL_IDS)
    primary=(group['phase']=='retro' and h==6 and
        ((group['source']=='fx_hourly' and w==2880) or (group['series_key']=='PDPOSGS-B' and w==52)))
    if primary: result['primary_selection']=select_minimum(outer,FINITE_IDS[:3])
    result['selection_frozen_utc']=now()
    dump(folder/'selection-before-evaluation.json',dict(selection_frozen_utc=result['selection_frozen_utc'],
        group=group,rules=selections,primary_selection=result.get('primary_selection'),
        validation_candidates=result['validation_candidates'],fold_bounds=result['r3_fold_bounds'],
        design_commit=DESIGN_COMMIT,design_sha256=DESIGN_SHA256),exclusive=True)
    result['evaluation_started_utc']=now()
    selected={'F':'F','I':'I',**{rule:s.get('selected_id') if s.get('status')=='SELECTED' else None for rule,s in selections.items()}}
    for report in REPORTS:
        row=dict(group,report=report,status='FAILED',reason=None,selected_id=selected[report])
        if selected[report] is None:
            row['reason']='REQUIRED_VALIDATION_CANDIDATE_FAILED'
        else:
            item=attempt(selected[report],ev)
            if item.get('status')=='FAILED': row['reason']=item['reason']
            else: row.update(status='COMPLETE',**item['summary'],trace_sha256=item['trace_sha256'])
        result['rows'].append(row)
    f=next(r for r in result['rows'] if r['report']=='F')
    for row in result['rows']:
        row['percent_vs_F']=(100*(row['mean_pinball']/f['mean_pinball']-1)
            if row['status']=='COMPLETE' and f['status']=='COMPLETE' and f['mean_pinball']>0 else None)
    if primary:
        selection=result['primary_selection']; candidate=selection.get('selected_id') if selection.get('status')=='SELECTED' else None
        item=attempt(candidate,ev) if candidate else dict(status='FAILED',reason='REQUIRED_VALIDATION_CANDIDATE_FAILED')
        reference=attempt('F',ev,window=720,refit_step=1) if group['source']=='fx_hourly' else attempt('F',ev)
        p=dict(id='FX-original-structure' if group['source']=='fx_hourly' else 'Treasury-W52-structural-analogue',
            **group,status='FAILED',selected_id=candidate,
            reference='rolling corrected F W720 d1' if group['source']=='fx_hourly' else 'frozen corrected F W52 d13',
            limitation=None if group['source']=='fx_hourly' else 'W52 structural analogue; original W260 primary not exactly replicated')
        if item.get('status')!='FAILED' and reference.get('status')!='FAILED':
            q=item['summary']['mean_pinball']; fmean=reference['summary']['mean_pinball']
            p.update(status='COMPLETE',QR_mean_pinball=q,F_mean_pinball=fmean,
                percent_vs_reference=100*(q/fmean-1) if fmean>0 else None,
                direction_replicated=q<fmean if group['source']=='fx_hourly' else q>fmean,
                QR_trace_sha256=item['trace_sha256'],F_trace_sha256=reference['trace_sha256'])
        else: p['reason']=item.get('reason') or reference.get('reason')
        result['primary_replication']=p
    result['completed_utc']=now()
    dump(folder/'group-result.json',result,exclusive=True)
    return result


def run_phases(groups, handler, seal_retro):
    results={'retro':[],'inspected':[]}
    for phase in ('retro','inspected'):
        if phase=='inspected': seal_retro(results['retro'])
        for group in groups:
            if group['phase']==phase: results[phase].append(handler(group))
    return results


def assess(rows, spec):
    weekly={rule:[r for r in rows if r['phase']=='retro' and r['source']=='nyfed_weekly' and r['report']==rule] for rule in ('R0','R2')}
    usable={rule:[r['percent_vs_F'] for r in values if r['status']=='COMPLETE' and r.get('percent_vs_F') is not None and math.isfinite(r['percent_vs_F'])] for rule,values in weekly.items()}
    needed=spec['success']['S1']['weekly_R2_complete_required']
    full={rule:len(weekly[rule])==needed and len(usable[rule])==needed for rule in weekly}
    med={rule:statistics.median(values) if full[rule] else None for rule,values in usable.items()}
    worst=max(usable['R2']) if full['R2'] else None
    s1spec=spec['success']['S1']
    s1=dict(status='PASS' if full['R2'] and worst<=s1spec['worst_percent_vs_F_max'] and med['R2']<=s1spec['median_percent_vs_F_max'] else 'NOT_MET',
        complete_required=needed,complete_count=len(usable['R2']),worst_percent_vs_F=worst,median_percent_vs_F=med['R2'])
    s2spec=spec['success']['S2']
    fraction=re.search(r'R2_percent_vs_F<=([0-9.]+)\*R0_percent_vs_F',s2spec['pass'])
    if fraction is None: raise ValueError('FROZEN_S2_FORMULA')
    retained_fraction=float(fraction.group(1))
    s2cells=[]; invalid=False
    for w in spec['success']['S2']['FX_H6_windows']:
        picked={rule:next((r for r in rows if r['phase']=='retro' and r['source']=='fx_hourly' and r['horizon']==6 and r['window']==w and r['report']==rule),None) for rule in ('R0','R2')}
        valid={rule:bool(r and r['status']=='COMPLETE' and r.get('percent_vs_F') is not None
                        and math.isfinite(r['percent_vs_F'])) for rule,r in picked.items()}
        r0=picked['R0'].get('percent_vs_F') if picked['R0'] else None
        r2=picked['R2'].get('percent_vs_F') if picked['R2'] else None
        eligible=bool(valid['R0'] and r0<0)
        required_failed=not valid['R0'] or eligible and not valid['R2']
        invalid|=required_failed
        retained=bool(eligible and valid['R2'] and r2<=retained_fraction*r0)
        s2cells.append(dict(window=w,R0_percent_vs_F=r0,R2_percent_vs_F=r2,eligible=eligible,
            half_gain_retained=retained,status='NOT_MET' if required_failed or eligible and not retained else 'PASS' if eligible else 'NOT_ELIGIBLE'))
    eligible=sum(c['eligible'] for c in s2cells)
    s2=dict(status='NOT_MET' if invalid or any(c['eligible'] and not c['half_gain_retained'] for c in s2cells)
        else 'PASS' if eligible else 'NOT_ASSESSABLE',eligible_count=eligible,cells=s2cells)
    s3=dict(status='PASS' if all(full.values()) and med['R2']<med['R0'] else 'NOT_MET',
        R0_complete_count=len(usable['R0']),R2_complete_count=len(usable['R2']),
        R0_median_percent_vs_F=med['R0'],R2_median_percent_vs_F=med['R2'])
    gate=s1['status']=='PASS' and s2['status']=='PASS'
    return dict(S1=s1,S2=s2,S3=s3,publication_gate=dict(status='METHOD_SECTION' if gate else 'ROBUSTNESS_PARAGRAPH',abstract_mention=gate),
                descriptive_only=True,pooled_tests_performed=False)


def verify_inputs(spec):
    committed=subprocess.run(['git','show',f'{DESIGN_COMMIT}:{DESIGN}'],cwd=ROOT,check=True,capture_output=True).stdout
    if hashlib.sha256(committed).hexdigest()!=DESIGN_SHA256: raise ValueError('PUBLISHED_DESIGN_IDENTITY')
    subprocess.run(['git','merge-base','--is-ancestor',DESIGN_COMMIT,'HEAD'],cwd=ROOT,check=True,capture_output=True)
    stamp=subprocess.run(['git','show','-s','--format=%cI',DESIGN_COMMIT],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    inputs=[]
    def check(relative,expected=None,expected_bytes=None,kind='input'):
        path=ROOT/relative; digest=sha(path); size=path.stat().st_size
        if expected and digest!=expected: raise ValueError('INPUT_HASH_MISMATCH:'+str(relative))
        if expected_bytes and size!=expected_bytes: raise ValueError('INPUT_BYTE_MISMATCH:'+str(relative))
        inputs.append(dict(path=str(relative),sha256=digest,bytes=size,kind=kind))
    check(DESIGN,DESIGN_SHA256,kind='published_design')
    for path,digest in spec['core_sha256'].items(): check(path,digest,kind='unchanged_core')
    check('notes/supervisor-20261023/r6-literature.md',spec['literature_sha256'],kind='frozen_literature')
    check('.scratch/r6-20261023/design-audit.json',spec['metadata_audit_sha256'],kind='private_metadata_audit')
    check('results/supervisor-20261023/e5/inputs/panel/selection-manifest.json',spec['panel_manifest_sha256'],kind='frozen_panel_manifest')
    for row in spec['weekly_series']: check(row['local_path'],row['raw_sha256'],row['raw_bytes'],'raw_source')
    fx=spec['sources']['fx_hourly']; check(fx['local_path'],fx['sha256'],fx['bytes'],'raw_source')
    for path in ('supervisor_r6.py','supervisor_r6_rules.py','test_supervisor_r6_runner.py','test_supervisor_r6_rules.py'):
        check(path,kind='new_execution_code')
    for path in ('.scratch/r6-20261023/published-design-binding.json','.scratch/r6-20261023/protected-before.json'):
        if (ROOT/path).is_file(): check(path,kind='parent_private_binding')
    return dict(design_commit=DESIGN_COMMIT,design_commit_timestamp=stamp,design_sha256=DESIGN_SHA256,
        checked_utc=now(),files=inputs)


def load_existing_sources(spec):
    sources={}
    bill=spec['weekly_series'][0]
    data=load_source(ROOT/bill['local_path'],'nyfed_weekly',expected_sha256=bill['raw_sha256'],expected_bytes=bill['raw_bytes'])
    sources[bill['series_key']]=(data.position,data.dates)
    grid=[str(d)[:10] for d in data.dates]
    for row in spec['weekly_series'][1:]:
        values,facts=align_source((ROOT/row['local_path']).read_bytes(),row['series_key'],grid)
        if facts['aligned_observations']!=706 or facts['imputed'] or facts['spliced']: raise ValueError('PANEL_ALIGNMENT')
        sources[row['series_key']]=(values,data.dates)
    cfg=spec['sources']['fx_hourly']
    fx=load_source(ROOT/cfg['local_path'],'fx_hourly',expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
    sources['fx_hourly']=(fx.position,fx.dates)
    return sources


def terminal_group(group, status, reason):
    result=dict(group=group,status=status,reason=reason,selections={},
        rows=[dict(group,report=r,status=status,reason=reason,selected_id=None,percent_vs_F=None) for r in REPORTS])
    if group['phase']=='retro' and group['horizon']==6 and (
            group['source']=='fx_hourly' and group['window']==2880 or
            group['series_key']=='PDPOSGS-B' and group['window']==52):
        result['primary_replication']=dict(group,
            id='FX-original-structure' if group['source']=='fx_hourly' else 'Treasury-W52-structural-analogue',
            status=status,reason=reason,selected_id=None,
            reference='rolling corrected F W720 d1' if group['source']=='fx_hourly' else 'frozen corrected F W52 d13',
            limitation=None if group['source']=='fx_hourly' else 'W52 structural analogue; original W260 primary not exactly replicated')
    return result


def interrupted_group(group, progress, reason):
    """Retain finished reports; reuse finished identical reports without fitting."""
    result=terminal_group(group,'NOT_RUN',reason)
    result.update({k:v for k,v in progress.items() if not k.startswith('_') and k!='rows'})
    finished={r['report']:r for r in progress.get('rows',[])}
    by_id={r.get('selected_id'):r for r in finished.values() if r['status']=='COMPLETE'}
    active=progress.get('_active_evaluation_candidate')
    rows=[]
    for report in REPORTS:
        if report in finished:
            rows.append(finished[report]);continue
        selection=result.get('selections',{}).get(report,{})
        candidate=report if report in ('I','F') else selection.get('selected_id')
        row=dict(group,report=report,selected_id=candidate,status='NOT_RUN',reason=reason,percent_vs_F=None)
        if candidate in by_id:
            row=dict(by_id[candidate],report=report)
        elif report not in ('I','F') and selection.get('status')=='FAILED':
            row.update(status='FAILED',reason='REQUIRED_VALIDATION_CANDIDATE_FAILED')
        elif active is not None and candidate==active:
            row['status']='TIME_LIMIT' if 'TIME_LIMIT' in reason else 'FAILED'
        rows.append(row)
    f=next(r for r in rows if r['report']=='F')
    for row in rows:
        row['percent_vs_F']=(100*(row['mean_pinball']/f['mean_pinball']-1)
            if row['status']=='COMPLETE' and f['status']=='COMPLETE' and f['mean_pinball']>0 else None)
    result.update(rows=rows,status='TIME_LIMIT' if 'TIME_LIMIT' in reason else 'FAILED',reason=reason,completed_utc=now())
    return result


def selection_rows(results):
    rows=[]
    for result in results:
        for rule in ('R0','R1','R2','R3'):
            s=result.get('selections',{}).get(rule,{})
            rows.append(dict(result['group'],rule=rule,status=s.get('status',result.get('status','NOT_RUN')),
                reason=s.get('reason',result.get('reason')),selected_id=s.get('selected_id'),best_id=s.get('best_id'),
                n=s.get('n'),bandwidth=s.get('bandwidth'),selection_frozen_utc=result.get('selection_frozen_utc'),
                r3_design_status=result.get('r3_design_status') if rule=='R3' else None))
    return rows


def seal_retro(results, public, private):
    rows=[row for result in results for row in result['rows']]
    if len(results)!=30 or len(rows)!=180: raise ValueError('RETRO_INVENTORY_INCOMPLETE')
    dump(public/'retro-cells.json',dict(sealed_utc=now(),groups=results,rows=rows),exclusive=True)
    write_csv(public/'retro-summary.csv',rows,ROW_FIELDS)
    write_csv(public/'retro-selection.csv',selection_rows(results))
    primaries=[r['primary_replication'] for r in results if 'primary_replication' in r]
    if (len(primaries)!=2 or {p['id'] for p in primaries}!=
            {'FX-original-structure','Treasury-W52-structural-analogue'}):
        raise ValueError('PRIMARY_DIAGNOSTIC_INVENTORY')
    write_csv(public/'primary-replication.csv',primaries,('id','phase','source','series_key','horizon','window',
        'status','reason','selected_id','reference','limitation','QR_mean_pinball','F_mean_pinball',
        'percent_vs_reference','direction_replicated','QR_trace_sha256','F_trace_sha256'))
    files=[p for p in (private/'retro').rglob('*') if p.is_file()]
    files += [public/name for name in ('retro-cells.json','retro-summary.csv','retro-selection.csv','primary-replication.csv')]
    inventory=[dict(path=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)]
    dump(public/'retro-seal.json',dict(status='SEALED',sealed_utc=now(),design_commit=DESIGN_COMMIT,
        group_count=30,report_row_count=180,files=inventory),exclusive=True)
    # Read-only file modes supplement the hashes; the run never rewrites these.
    for p in files+[public/'retro-seal.json']: os.chmod(p,0o400 if p.is_relative_to(private) else 0o444)
    for row in inventory:
        path=Path(row['path']); path=path if path.is_absolute() else ROOT/path
        if sha(path)!=row['sha256']: raise ValueError('RETRO_SEAL_HASH_MISMATCH')
    return inventory


def execute():
    spec=read_contract(); manifest=verify_inputs(spec)
    PUBLIC.mkdir(parents=True,exist_ok=False)
    PRIVATE.mkdir(parents=True,exist_ok=False,mode=0o700)
    (PRIVATE/'retro').mkdir(mode=0o700); (PRIVATE/'inspected').mkdir(mode=0o700)
    dump(PUBLIC/'input-manifest.json',manifest,exclusive=True)
    receipt=dict(status='PREPARING_METADATA',run_started_utc=now(),design_commit=DESIGN_COMMIT,
        design_commit_timestamp=manifest['design_commit_timestamp'],design_sha256=DESIGN_SHA256,
        input_manifest_sha256=sha(PUBLIC/'input-manifest.json'),first_retro_calculation_utc=None,
        first_inspected_calculation_utc=None,retro_sealed_utc=None,run_count=1,no_retries=True,
        python_executable=sys.executable,numpy_version=np.__version__,resource_limits=spec['resource_limits'])
    dump(PUBLIC/'run-receipt.json',receipt,exclusive=True)
    sources=load_existing_sources(spec)
    start=time.monotonic(); guard=Guard(start,spec['resource_limits'],PUBLIC/'progress.json')
    stopped=[None]
    def alarm(*_):
        raise LimitStop('RUN_TIME_LIMIT' if time.monotonic()-start>=spec['resource_limits']['run_wall_seconds'] else 'GROUP_TIME_LIMIT')
    previous=signal.signal(signal.SIGALRM,alarm)
    def handle(group):
        if stopped[0]: return terminal_group(group,'NOT_RUN',stopped[0])
        folder=PRIVATE/group['phase']/identity(group); folder.mkdir(mode=0o700)
        try:
            guard.begin_group();guard(stage='group_metadata_ready',group_id=identity(group))
            marker='first_'+('retro' if group['phase']=='retro' else 'inspected')+'_calculation_utc'
            if receipt[marker] is None:
                receipt[marker]=now();receipt['status']='RUNNING_'+group['phase'].upper()
                if datetime.fromisoformat(receipt[marker])<=datetime.fromisoformat(manifest['design_commit_timestamp']):
                    raise ValueError('DESIGN_CHRONOLOGY')
                dump(PUBLIC/'run-receipt.json',receipt)
                print(json.dumps(dict(event=marker,utc=receipt[marker],design_commit=DESIGN_COMMIT)),flush=True)
            x,dates=sources[group['series_key']]
            result=run_group(group,spec,x,dates,folder,guard)
        except LimitStop as exc:
            result=getattr(exc,'partial_group',terminal_group(group,'TIME_LIMIT' if 'TIME_LIMIT' in exc.code else 'FAILED',exc.code))
            if exc.code!='GROUP_TIME_LIMIT': stopped[0]=exc.code
            dump(folder/'terminal.json',result,exclusive=True)
        except (Exception,KeyboardInterrupt) as exc:
            result=terminal_group(group,'FAILED',getattr(exc,'code',type(exc).__name__))
            dump(folder/'terminal.json',dict(result,diagnostic=failure(exc)),exclusive=True)
            if isinstance(exc,KeyboardInterrupt): stopped[0]='INTERRUPTED'
        finally: signal.setitimer(signal.ITIMER_REAL,0)
        print(json.dumps(dict(group=identity(group),reports={r['report']:r['status'] for r in result['rows']},elapsed_seconds=time.monotonic()-start)),flush=True)
        return result
    def seal(results):
        seal_retro(results,PUBLIC,PRIVATE)
        receipt['retro_sealed_utc']=now();receipt['retro_seal_sha256']=sha(PUBLIC/'retro-seal.json')
        dump(PUBLIC/'run-receipt.json',receipt)
        print(json.dumps(dict(event='RETRO_SEALED',utc=receipt['retro_sealed_utc'])),flush=True)
    try:
        phases=run_phases(group_inventory(spec),handle,seal)
        inspected_rows=[r for g in phases['inspected'] for r in g['rows']]
        dump(PUBLIC/'inspected-cells.json',dict(groups=phases['inspected'],rows=inspected_rows),exclusive=True)
        results=phases['retro']+phases['inspected'];rows=[r for g in results for r in g['rows']]
        if len(rows)!=516: raise ValueError('FINAL_ROW_INVENTORY')
        write_csv(PUBLIC/'summary.csv',rows,ROW_FIELDS)
        write_csv(PUBLIC/'selection.csv',selection_rows(results))
        dump(PUBLIC/'assessment.json',assess(rows,spec),exclusive=True)
        archive=[]
        for path in sorted(PRIVATE.rglob('*')):
            if path.is_file(): archive.append(dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=sha(path)))
        dump(PUBLIC/'private-archive-manifest.json',dict(files=archive,raw_or_per_issue_data_public=False),exclusive=True)
        for item in manifest['files']:
            if sha(ROOT/item['path'])!=item['sha256']: raise ValueError('PROTECTED_INPUT_CHANGED')
        receipt.update(status='COMPLETE' if all(r['status']=='COMPLETE' for r in rows) else 'COMPLETE_WITH_REPORTED_FAILURES',
            completed_utc=now(),retro_rows=180,inspected_rows=336,resources=guard.resources,
            final_elapsed_seconds=time.monotonic()-start,input_hashes_unchanged=True)
        readme=('R6 follows the published design '+DESIGN_COMMIT+' (SHA-256 '+DESIGN_SHA256+').\n\n'
            'Command: '+sys.executable+' supervisor_r6.py --execute\n\n'
            'There are 30 retrospective and 56 inspected source/H/W groups, each with F/I/R0/R1/R2/R3. '
            'Selection is saved before evaluation; retrospective aggregates and private traces are sealed before inspected calculations. '
            'The original bill plus 12 archived panel series share the 706-date grid; no new data were downloaded. '
            'The retrospective sample is familiar historical data not previously found to be evaluation in the bounded repository audit; it is not external or unseen data. '
            'Public files contain aggregate metrics, statuses and hashes only. Licensed/raw inputs and per-origin capacities, peaks, losses and fit receipts remain in the ignored private run directory. '
            'No pooled tests or financial coverage guarantees are claimed. W260 has no extra R3 folds by design. '
            'Treasury primary replication is explicitly a W52 structural analogue, not exact W260 replication. '
            'Any failed candidate blocks every rule that requires it; all failed and unrun rows remain in the inventory.\n')
        (PUBLIC/'README.md').write_text(readme)
    except BaseException as exc:
        receipt.update(status='RUN_ABORTED',completed_utc=now(),reason=getattr(exc,'code',type(exc).__name__),resources=guard.resources)
        dump(PUBLIC/'run-receipt.json',receipt)
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
    dump(PUBLIC/'run-receipt.json',receipt)
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true',help='Run the one published real-data execution; existing output directories are rejected.')
    args=parser.parse_args()
    if not args.execute: parser.error('Explicit --execute is required; no calculation was performed.')
    print(json.dumps(execute()),flush=True)
