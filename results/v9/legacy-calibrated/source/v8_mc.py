"""Prespecified v8 Monte Carlo orchestration; never evaluates financial outcomes."""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import argparse
import csv
import hashlib
import json
import math
import multiprocessing as mp
from pathlib import Path
import subprocess
import time
from datetime import datetime,timezone
import numpy as np
from conditional_study import StudyConfig,conditional_forecast,score_predictions,summarize_scores,select_parameter
from parsimonious_v3 import features4,forecast
from empirical_headroom import predict
from study_core import build_label_cache

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/v8/mc'
DGPS=('D0','D1','D2')
WINDOWS=(52,260,720,2880)
FEATURES=(4,33)
MENU=(.001,.01,.1,1.,10.,math.inf)
TAU=.95


def now():return datetime.now(timezone.utc).isoformat()


def write_new(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n')


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_worker_log(path,allow_truncated_final=False):
    lines=Path(path).read_text().splitlines();rows=[];truncated=False
    for j,line in enumerate(lines):
        try:rows.append(json.loads(line))
        except json.JSONDecodeError:
            if allow_truncated_final and j==len(lines)-1:truncated=True
            else:raise ValueError('CORRUPT_WORKER_RECORD') from None
    return rows,truncated


def geometry(dgp,m):
    hourly=dgp=='D1';l=168 if hourly else 26;v=1440 if hourly else 52
    a=l+2880+6-1;b=a+v+6
    return dict(validation_first=a,validation_last=a+v-1,evaluation_first=b,
        evaluation_last=b+m-1,records=b+m+6,validation_count=v,
        short_scale=24 if hourly else 6,long_scale=l,refit_step=24 if hourly else 13,
        nominal_gap_seconds=3600 if hourly else 604800)


def choose_candidate(rows,count):
    selected=select_parameter(rows,MENU,expected_count=count)
    if selected['status']!='SELECTED':raise ValueError('DECLARED_CANDIDATE_FAILED')
    return selected['parameter']


def seed(phase,dgp,rep,stream):
    return np.random.SeedSequence([20261024,phase,DGPS.index(dgp),rep,stream])


def aggregate(records,repetitions,m):
    out=[]
    for d in DGPS:
        for w in WINDOWS:
            for p in FEATURES:
                rows=[r for r in records if (r['dgp'],r['window'],r['features'])==(d,w,p)]
                good=[r for r in rows if r['status']=='COMPLETE']
                failed=[r for r in rows if r['status']=='FAILED']
                deadline=any(r['status']=='INCOMPLETE_DEADLINE' for r in rows)
                status='FAILED' if failed else ('COMPLETE' if len(good)==repetitions and len({r['rep'] for r in good})==repetitions else ('INCOMPLETE_DEADLINE' if deadline else 'INCOMPLETE'))
                row=dict(dgp=d,window=w,features=p,status=status,required_repetitions=repetitions,
                    completed_repetitions=len(good),evaluation_origins=m,qr_median_pct=None,
                    qr_q25_pct=None,qr_q75_pct=None,win_rate=None,oracle_median_pct=None,
                    i_median_pct=None,f_breach_median=None,i_breach_median=None,
                    qr_breach_median=None,oracle_breach_median=None,infinity_frequency=None,
                    failure_reasons=';'.join(sorted({r.get('reason','') for r in failed})))
                if status=='COMPLETE':
                    a=np.array([r['qr_change'] for r in good]);q=np.quantile(a,[.25,.5,.75])
                    row.update(qr_q25_pct=float(q[0]),qr_median_pct=float(q[1]),qr_q75_pct=float(q[2]),
                        win_rate=float(np.mean([r['win'] for r in good])),
                        oracle_median_pct=float(np.median([r['oracle_change'] for r in good])),
                        i_median_pct=float(np.median([r['i_change'] for r in good])),
                        infinity_frequency=float(np.mean([r['selected']=='inf' for r in good])))
                    for method in ('f','i','qr','oracle'):
                        row[method+'_breach_median']=float(np.median([r[method+'_breach'] for r in good]))
                out.append(row)
    return out


def predictions(rows):
    lookup={(r['dgp'],r['window'],r['features']):r for r in rows}
    groups={
        'P1':[lookup['D0',w,p] for w in WINDOWS for p in FEATURES],
        'P2':[lookup['D1',2880,p] for p in FEATURES],
        'P3':[lookup['D2',52,33]],
        'P4':[lookup[d,w,p] for d in ('D1','D2') for p in FEATURES for w in WINDOWS]}
    result={}
    for name,group in groups.items():
        if any(r['status']!='COMPLETE' for r in group):
            result[name]=dict(status='UNASSESSABLE',reason='REQUIRED_CELL_INCOMPLETE_OR_FAILED');continue
        values=[r['qr_median_pct'] for r in group]
        if name=='P1':passed=all(x>=-2 for x in values)
        elif name=='P2':passed=all(x < -5 for x in values)
        elif name=='P3':passed=values[0]>5
        else:
            passed=all(all(lookup[d,WINDOWS[j+1],p]['qr_median_pct']<=lookup[d,WINDOWS[j],p]['qr_median_pct'] for j in range(3)) for d in ('D1','D2') for p in FEATURES)
        result[name]=dict(status='SUPPORTED' if passed else 'NOT_SUPPORTED',observed_values=values)
    return result


def select_run_plan(pilot):
    # Jobs have already imputed missing cell work individually before totaling.
    maxima={}
    for d in DGPS:
        rows=[r for r in pilot if r['dgp']==d]
        maxima[d]={k:max([r.get(k,0.) for r in rows] or [1e9]) for k in ('validation_seconds','evaluation_seconds','oracle_seconds','simulation_seconds')}
    projections=[]
    for r,m in ((100,500),(50,500),(50,300)):
        jobs=[z['simulation_seconds']+z['validation_seconds']+(z['evaluation_seconds']+z['oracle_seconds'])*(m/500) for z in maxima.values()]
        projection=1.25*(sum(jobs)*r/4+max(jobs))
        projections.append(dict(repetitions=r,evaluation_origins=m,projected_seconds=projection))
        if projection<=5400:break
    chosen=projections[-1]
    return dict(**chosen,formal_limit_seconds=5400,workers=4,projection_safety_multiplier=1.25,
        candidates_considered=projections,pilot_job_maxima=maxima,selected_at_utc=now(),
        rule='FIRST_PROJECTED_LE_5400_ELSE_MINIMUM_WITH_HARD_STOP')


def _worker(task):
    """One DGP/repetition shares a path/oracle; writes each cell immediately."""
    from v8_mc_dgp import DGPParams,simulate,oracle_reports
    d,rep,phase,m,params,deadline,folder,failed=task
    start=time.monotonic();g=geometry(d,m)
    rows=[];log=Path(folder)/f'{d}-r{rep:03d}.jsonl'
    def guard(**_):
        if time.monotonic()>=deadline:raise TimeoutError('FORMAL_DEADLINE')
    def record(row):
        rows.append(row)
        with log.open('a') as f:f.write(json.dumps(row,allow_nan=False)+'\n');f.flush()
    base=dict(dgp=d,rep=rep)
    simulation_seconds=oracle_seconds=0.
    if all(f'{d}-{w}-{p}' in failed for w in WINDOWS for p in FEATURES):
        for w in WINDOWS:
            for p in FEATURES:record(dict(base,window=w,features=p,status='NOT_RUN_CELL_FAILED',reason=failed[f'{d}-{w}-{p}'],validation_seconds=0.,evaluation_seconds=0.))
        return dict(dgp=d,rep=rep,status='NOT_RUN_CELL_FAILED',simulation_seconds=0.,oracle_seconds=0.,wall_seconds=time.monotonic()-start,rows=rows)
    try:
        guard();par=DGPParams(**params);path=simulate(par,g['records'],seed(phase,d,rep,0))
        simulation_seconds=time.monotonic()-start
        x=path['position'];t=path['times'];cache=build_label_cache(x,6)
        val=np.arange(g['validation_first'],g['validation_last']+1)
        ev=np.arange(g['evaluation_first'],g['evaluation_last']+1)
        feature,valid=features4(x,t,g['short_scale'],g['long_scale'],g['nominal_gap_seconds'])
        st=time.monotonic();oracle=oracle_reports(par,path,ev,horizon=6,paths=2000,seed=seed(phase,d,rep,1))
        oracle_seconds=time.monotonic()-st;guard()
        oracle_score=summarize_scores(score_predictions(cache.peak[ev],oracle,np.abs(x[ev]),ev))
    except Exception as exc:
        for w in WINDOWS:
            for p in FEATURES:
                key=f'{d}-{w}-{p}';failed[key]=str(exc)
                record(dict(base,window=w,features=p,status='INCOMPLETE_DEADLINE' if isinstance(exc,TimeoutError) else 'FAILED',reason=type(exc).__name__+':'+str(exc),validation_seconds=0.,evaluation_seconds=0.))
        return dict(dgp=d,rep=rep,status='FAILED',simulation_seconds=simulation_seconds,oracle_seconds=oracle_seconds,rows=rows)
    for w in WINDOWS:
        for p in FEATURES:
            key=f'{d}-{w}-{p}';row=dict(base,window=w,features=p,validation_seconds=0.,evaluation_seconds=0.)
            if key in failed:
                record(dict(row,status='NOT_RUN_CELL_FAILED',reason=failed[key]));continue
            stage_start=time.monotonic();candidates=[];stage='validation';current_lambda=None
            try:
                guard();hv=predict(x,val,6,w,g['refit_step']);he=predict(x,ev,6,w,g['refit_step'])
                cfg=StudyConfig(6,w,g['refit_step'],g['short_scale'],g['long_scale'],g['nominal_gap_seconds'])
                def issue(ids,lam):
                    guard()
                    if math.isinf(lam):return hv['I'] if ids is val else he['I']
                    if p==4:return forecast(x,feature,valid,cache,ids,6,w,g['refit_step'],lam,guard)[0]
                    return conditional_forecast(x,t,ids,cfg,'QR',lam,checkpoint=guard).capacities
                for lam in MENU:
                    current_lambda=lam
                    caps=issue(val,lam);score=summarize_scores(score_predictions(cache.peak[val],caps,np.abs(x[val]),val))
                    candidates.append(dict(parameter=lam,status='COMPLETE',origin_count=len(val),mean_pinball=score['mean_pinball']))
                selected=choose_candidate(candidates,len(val));row['validation_seconds']=time.monotonic()-stage_start
                stage_start=time.monotonic();stage='evaluation';current_lambda=selected;qrcaps=issue(ev,selected)
                metrics={method:summarize_scores(score_predictions(cache.peak[ev],caps,np.abs(x[ev]),ev)) for method,caps in [('f',he['F']),('i',he['I']),('qr',qrcaps)]}
                metrics['oracle']=oracle_score
                f=metrics['f']['mean_pinball']
                if f<=0:raise ValueError('ZERO_F_LOSS_RELATIVE_SCORE_UNDEFINED')
                row.update(status='COMPLETE',selected='inf' if math.isinf(selected) else str(selected),
                    qr_change=100*(metrics['qr']['mean_pinball']/f-1),i_change=100*(metrics['i']['mean_pinball']/f-1),
                    oracle_change=100*(metrics['oracle']['mean_pinball']/f-1),win=metrics['qr']['mean_pinball']<f,
                    evaluation_seconds=time.monotonic()-stage_start,
                    validation_candidates=[dict(z,parameter='inf' if math.isinf(z['parameter']) else z['parameter']) for z in candidates])
                for name,score in metrics.items():row.update({name+'_loss':score['mean_pinball'],name+'_breach':score['strict_breach_rate']})
            except Exception as exc:
                row.update(status='INCOMPLETE_DEADLINE' if isinstance(exc,TimeoutError) else 'FAILED',reason=type(exc).__name__+':'+str(exc),
                    failure_stage=stage,failure_lambda='inf' if current_lambda is not None and math.isinf(current_lambda) else current_lambda,
                    failure_context=getattr(exc,'failure_context',None),
                    validation_candidates=[dict(z,parameter='inf' if math.isinf(z['parameter']) else z['parameter']) for z in candidates])
                if not row['validation_seconds']:row['validation_seconds']=time.monotonic()-stage_start
                else:row['evaluation_seconds']=time.monotonic()-stage_start
                failed[key]=row['reason']
            record(row)
    wall=time.monotonic()-start
    # Include feature/cache preparation, oracle scoring and record overhead in
    # the unscaled component of the pilot projection.
    preparation=max(simulation_seconds,wall-oracle_seconds-sum(r.get('validation_seconds',0.)+r.get('evaluation_seconds',0.) for r in rows))
    return dict(dgp=d,rep=rep,status='COMPLETE' if all(r['status']=='COMPLETE' for r in rows) else 'PARTIAL_FAILURE',
        simulation_seconds=preparation,oracle_seconds=oracle_seconds,wall_seconds=wall,rows=rows)


def execute(phase,repetitions,m,calibration,folder,limit=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=False)
    started=time.monotonic();deadline=started+limit if limit else math.inf
    context=mp.get_context('spawn');manager=context.Manager();failed=manager.dict()
    tasks=[];direct=[]
    for rep in range(repetitions):
        for d in DGPS:
            if d not in calibration['parameters']:
                for w in WINDOWS:
                    for p in FEATURES:direct.append(dict(dgp=d,rep=rep,window=w,features=p,status='FAILED',reason='DGP_CALIBRATION_FAILED',validation_seconds=0.,evaluation_seconds=0.))
            else:tasks.append((d,rep,phase,m,calibration['parameters'][d],deadline,str(folder),failed))
    write_new(folder/'receipt.json',dict(started_utc=now(),phase=phase,repetitions=repetitions,evaluation_origins=m,limit_seconds=limit,calibration_sha256=digest(OUT/'calibration.json'),design_commit='b7e548df39bc2d5dc0108a01ec8a7c2ccfbb99d4'))
    jobs=[];pool=context.Pool(4)
    pending=[pool.apply_async(_worker,(task,)) for task in tasks]
    try:
        while pending and time.monotonic()<deadline:
            ready=[p for p in pending if p.ready()]
            for p in ready:
                jobs.append(p.get());pending.remove(p)
            if ready:
                print(json.dumps(dict(phase=phase,finished_jobs=len(jobs),total_jobs=len(tasks),elapsed_seconds=round(time.monotonic()-started,1))),flush=True)
            if pending:time.sleep(.25)
        if pending:pool.terminate()
        else:pool.close()
        pool.join()
    except BaseException:
        pool.terminate();pool.join();raise
    finally:manager.shutdown()
    records=list(direct);truncated_logs=[]
    for log in sorted(folder.glob('D*-r*.jsonl')):
        read,truncated=read_worker_log(log,allow_truncated_final=bool(pending));records.extend(read)
        if truncated:truncated_logs.append(log.name)
    # Deadline-mark every missing repetition so all24cell statuses are explicit.
    present={(r['dgp'],r['window'],r['features'],r['rep']) for r in records}
    if pending:
        for d in DGPS:
            for w in WINDOWS:
                for p in FEATURES:
                    for rep in range(repetitions):
                        if (d,w,p,rep) not in present:records.append(dict(dgp=d,window=w,features=p,rep=rep,status='INCOMPLETE_DEADLINE',reason='NOT_FINISHED_AT_HARD_STOP'))
    elapsed=time.monotonic()-started
    write_new(folder/'completion.json',dict(ended_utc=now(),elapsed_seconds=elapsed,unfinished_jobs=len(pending),truncated_worker_logs_retained=truncated_logs,jobs=[{k:v for k,v in j.items() if k!='rows'} for j in jobs]))
    write_new(folder/'replicates.json',records)
    return jobs,records,elapsed


def pilot_job_times(jobs):
    cells=[r for job in jobs for r in job['rows'] if r['status']=='COMPLETE']
    result=[]
    for j in jobs:
        # Impute each uncompleted cell, never a whole eight-cell job from one cell.
        rows=j['rows'];complete=[r for r in rows if r['status']=='COMPLETE']
        same=[r for r in cells if (r['dgp']=='D1')==(j['dgp']=='D1')]
        pool=same or cells
        if not pool:
            # A completely failed pilot cannot supply a feasible projection.
            v=e=1e9
        else:
            v=sum(r.get('validation_seconds',0.) for r in complete)
            e=sum(r.get('evaluation_seconds',0.) for r in complete)
            for r in rows:
                if r['status']!='COMPLETE':
                    v+=max(r.get('validation_seconds',0.),max(x['validation_seconds'] for x in pool))
                    e+=max(r.get('evaluation_seconds',0.),max(x['evaluation_seconds'] for x in pool))
        result.append(dict(dgp=j['dgp'],rep=j['rep'],status=j['status'],validation_seconds=v,evaluation_seconds=e,
            simulation_seconds=j['simulation_seconds'],oracle_seconds=j['oracle_seconds'],imputed_cells=8-len(complete)))
    return result


def report(records,r,m):
    rows=aggregate(records,r,m)
    write_new(OUT/'summary.json',rows);write_new(OUT/'predictions.json',predictions(rows))
    with (OUT/'summary.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    text=['# Calibrated Monte Carlo main results','',f'Required repetitions: {r}; evaluation origins per repetition: {m}. All24 planned cells are reported.','',
        '|DGP|W|p|Status|QR/F median% [IQR]|QR wins|Oracle/F median%|QR breaches%|','|---|---:|---:|---|---:|---:|---:|---:|']
    for row in rows:
        if row['status']=='COMPLETE':
            values=f"{row['qr_median_pct']:.1f} [{row['qr_q25_pct']:.1f}, {row['qr_q75_pct']:.1f}]|{100*row['win_rate']:.1f}%|{row['oracle_median_pct']:.1f}|{100*row['qr_breach_median']:.1f}"
        else:values='—|—|—|—'
        text.append(f"|{row['dgp']}|{row['window']}|{row['features']}|{row['status']}|{values}|")
    text+=['','## Predictions','']+[f"- {k}: {v['status']}" for k,v in predictions(rows).items()]
    with (OUT/'main-results.md').open('x') as f:f.write('\n'.join(text)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(11,3.1),sharey=True)
    for d,ax in zip(DGPS,axes):
        for p,color,marker in ((4,'#1f77b4','o'),(33,'#d95f02','s')):
            group=[x for x in rows if x['dgp']==d and x['features']==p]
            x=np.array(WINDOWS);y=np.array([z['qr_median_pct'] if z['status']=='COMPLETE' else np.nan for z in group])
            ax.plot(x,y,color=color,marker=marker,label=f'{p} predictors')
            lo=np.array([z['qr_q25_pct'] if z['status']=='COMPLETE' else np.nan for z in group]);hi=np.array([z['qr_q75_pct'] if z['status']=='COMPLETE' else np.nan for z in group])
            ax.fill_between(x,lo,hi,color=color,alpha=.12)
        oracle=[next((z['oracle_median_pct'] for z in rows if z['dgp']==d and z['window']==w and z['status']=='COMPLETE'),np.nan) for w in WINDOWS]
        ax.plot(WINDOWS,oracle,'k--',label='Oracle');ax.axhline(0,color='grey',lw=.7);ax.set_xscale('log');ax.set_xticks(WINDOWS,labels=[str(x) for x in WINDOWS]);ax.set_xlabel('History W');ax.set_title({'D0':'Constant variance (D0)','D1':'Hourly GARCH (D1)','D2':'Weekly GARCH (D2)'}[d]);ax.grid(alpha=.15)
    axes[0].set_ylabel('Pinball loss change vs F (%)');axes[-1].legend(fontsize=8)
    fig.tight_layout();fig.savefig(OUT/'mc-main.pdf');fig.savefig(OUT/'mc-main.png',dpi=180);plt.close(fig)


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['calibrate','pilot','formal','report']);args=p.parse_args()
    if args.stage=='calibrate':
        from v8_mc_calibrate import calibrate_all
        OUT.mkdir(parents=True,exist_ok=True);write_new(OUT/'calibration.json',calibrate_all(ROOT))
    elif args.stage=='pilot':
        calibration=json.loads((OUT/'calibration.json').read_text())
        jobs,records,elapsed=execute(1,2,500,calibration,OUT/'pilot')
        times=pilot_job_times(jobs);write_new(OUT/'pilot-timing.json',times)
        plan=select_run_plan(times);plan.update(pilot_elapsed_seconds=elapsed,pilot_timing_sha256=digest(OUT/'pilot-timing.json'),protocol_sha256=digest(ROOT/'protocol/v8/mc-design.md'),code_sha256={n:digest(ROOT/n) for n in ('v8_mc.py','v8_mc_dgp.py','v8_mc_calibrate.py')})
        write_new(OUT/'run-plan.json',plan);print(json.dumps(plan),flush=True)
    elif args.stage=='formal':
        plan=json.loads((OUT/'run-plan.json').read_text())
        for name,sha in plan['code_sha256'].items():
            if digest(ROOT/name)!=sha:raise ValueError('CODE_CHANGED_AFTER_PLAN')
        if digest(ROOT/'protocol/v8/mc-design.md')!=plan['protocol_sha256']:raise ValueError('PROTOCOL_CHANGED_AFTER_PLAN')
        calibration=json.loads((OUT/'calibration.json').read_text())
        _,records,elapsed=execute(2,plan['repetitions'],plan['evaluation_origins'],calibration,OUT/'formal',limit=5400)
        report(records,plan['repetitions'],plan['evaluation_origins']);print(json.dumps(dict(formal_elapsed_seconds=elapsed,finished_utc=now())),flush=True)
    else:
        plan=json.loads((OUT/'run-plan.json').read_text());records=json.loads((OUT/'formal/replicates.json').read_text());report(records,plan['repetitions'],plan['evaluation_origins'])


if __name__=='__main__':main()
