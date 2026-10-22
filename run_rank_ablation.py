"""Explicit, frozen eight-cell empirical-headroom rank ablation; no QR refit."""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
FREEZE = 'protocol/revision-20261022/rank-ablation-executable-freeze.json'
SPEC = 'protocol/revision-20261022/rank-ablation-spec.json'
THREAD_ENV = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check_frozen_files(root, entries):
    seen = set()
    for e in entries:
        name = e['path']; p = Path(name)
        if (not isinstance(name, str) or p.is_absolute() or '..' in p.parts
                or name in seen or not p.parts):
            raise ValueError('FREEZE_PATH')
        seen.add(name); p = root/p
        if any(q.is_symlink() for q in (p, *p.parents)) or not p.is_file():
            raise ValueError('FREEZE_FILE')
        raw = p.read_bytes()
        if len(raw) != e['bytes'] or sha(raw) != e['sha256']:
            raise ValueError('FREEZE_IDENTITY')


def reference_index(rows):
    out = {}
    for row in rows:
        key = (row['source'], int(row['horizon']), int(row['window']), row['method'])
        if key in out:
            raise ValueError('DUPLICATE_REFERENCE')
        out[key] = row
    return out


def compare_reference(found, expected):
    for key, value in found.items():
        token = expected[key]
        target = None if token == '' else float(token) if isinstance(value, (float,int)) else token
        if value is None:
            if token != '': raise ValueError('REFERENCE_NONE')
        elif value != target:
            raise ValueError('REFERENCE_METRIC:'+key)


def mean_contrast(left, right):
    if not all(math.isfinite(x) and x >= 0 for x in (left,right)):
        raise ValueError('INVALID_LOSS')
    return dict(difference_of_means=left-right,
        relative_mean_loss_difference_percent=100*((left-right)/right) if right else None,
        undefined_reason=None if right else 'ZERO_REFERENCE_MEAN_LOSS')


def write_csv(path, rows):
    if not rows: raise ValueError('EMPTY_TABLE')
    with path.open('x', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def scratch_output(root, output):
    raw = Path(output)
    if '..' in raw.parts:
        raise ValueError('NEW_SCRATCH_OUTPUT_REQUIRED')
    path = raw.absolute()
    if (root/'.scratch' not in path.parents
            or any(p.is_symlink() for p in (path, *path.parents))):
        raise ValueError('NEW_SCRATCH_OUTPUT_REQUIRED')
    return path


def execute(output):
    start=time.monotonic(); begun=datetime.now(timezone.utc).isoformat()
    output=scratch_output(ROOT, output)
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    (output/'private').mkdir(mode=0o700); (output/'public').mkdir(mode=0o700)
    audit={'status':'STARTED','started_utc':begun,'accuracy_recomputed':['I','frozen_F'],
           'QR_refitted':False,'independent_data_validation':False,'completed_cells':0}
    def save_audit():
        (output/'public/audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
    save_audit()
    def deadline(signum,frame): raise TimeoutError('RESOURCE_WALL')
    old_handler=signal.signal(signal.SIGALRM,deadline); signal.alarm(600)
    try:
        freeze_raw=(ROOT/FREEZE).read_bytes(); freeze=json.loads(freeze_raw)
        check_frozen_files(ROOT,freeze['files'])
        spec=json.loads((ROOT/SPEC).read_bytes())
        raw=(ROOT/spec['original_spec']).read_bytes()
        if sha(raw)!=spec['original_spec_sha256']: raise ValueError('ORIGINAL_SPEC_HASH')
        original=json.loads(raw)
        for k in THREAD_ENV: os.environ[k]='1'
        import numpy as np
        import empirical_headroom as method
        import conditional_study as study
        from conditional_sources import load_source
        from run_study import parse_thread_snapshot
        archive=reference_index(list(csv.DictReader(io.StringIO((ROOT/spec['original_summary']).read_text()))))
        summaries=[]; annual=[]; sparse=[]; contrasts=[]; cells=[]; maximum_threads=0
        for source,cfg in original['sources'].items():
            series=load_source(ROOT/cfg['input_relative_path'],source,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes'])
            if len(series.position)!=cfg['record_count']: raise ValueError('SOURCE_COUNT')
            ids=np.arange(cfg['evaluation_origin_first'],cfg['evaluation_origin_last']+1,dtype=np.int64)
            dates=series.dates[ids]; floor=np.abs(series.position[ids])
            for h in original['horizons']:
                # Separate target computation is never supplied to the predictor.
                peak=np.asarray([max(abs(float(v)) for v in series.position[t:t+h+1]) for t in ids])
                for w in cfg['windows']:
                    pred=method.predict(series.position,ids,h,w,cfg['refit_step'])
                    if (not np.array_equal(pred['origins'],ids) or np.any(pred['I']>pred['F'])
                            or np.any(pred['latest_label_ends']>pred['refit_indices'])
                            or np.any(pred['refit_indices']>ids)):
                        raise ValueError('FORECAST_CONTRACT')
                    scores={m:study.score_predictions(peak,pred[m],floor,ids) for m in ['I','F']}
                    metrics={m:study.summarize_scores(sc) for m,sc in scores.items()}
                    compare_reference(metrics['F'],archive[source,h,w,'frozen_F'])
                    if (np.any(scores['I'].overrun<scores['F'].overrun)
                            or np.any(scores['I'].unused>scores['F'].unused)
                            or np.any(scores['F'].strict_breach & ~scores['I'].strict_breach)):
                        raise ValueError('RANK_MONOTONICITY')
                    meta=dict(source=source,native_unit=cfg['native_unit'],horizon=h,window=w,refit_step=cfg['refit_step'])
                    for m in ['I','F']:
                        summaries.append(dict(**meta,method=m,**metrics[m]))
                        for year in np.unique(dates.astype('datetime64[Y]')):
                            mask=dates.astype('datetime64[Y]')==year
                            sc=study.score_predictions(peak[mask],pred[m][mask],floor[mask],ids[mask])
                            annual.append(dict(**meta,method=m,issue_year=str(year),**study.summarize_scores(sc)))
                        mask=(ids-ids[0])%(h+1)==0
                        sc=study.score_predictions(peak[mask],pred[m][mask],floor[mask],ids[mask])
                        sparse.append(dict(**meta,method=m,**study.summarize_scores(sc)))
                    qr=archive[source,h,w,'QR']; qmean=float(qr['mean_pinball'])
                    for name,left,right in [('QR-minus-I',qmean,metrics['I']['mean_pinball']),
                                            ('I-minus-frozen_F',metrics['I']['mean_pinball'],metrics['F']['mean_pinball']),
                                            ('QR-minus-frozen_F',qmean,metrics['F']['mean_pinball'])]:
                        row=dict(**meta,contrast=name,origin_count=len(ids),mean_loss_left=left,mean_loss_right=right,**mean_contrast(left,right))
                        row['direct_paired_difference']=float(math.fsum(map(float,scores['I'].pinball-scores['F'].pinball))/len(ids)) if name=='I-minus-frozen_F' else None
                        contrasts.append(row)
                    # Saved QR rows are not modified or relabeled as independently recomputed forecasts.
                    key=f'{source}-h{h}-w{w}'
                    np.savez(output/'private'/f'{key}.npz',origins=ids,peak=peak,floor=floor,I=pred['I'],F=pred['F'],
                             refit_indices=pred['refit_indices'],I_pinball=scores['I'].pinball,F_pinball=scores['F'].pinball)
                    thread_raw=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],capture_output=True,text=True,check=True).stdout
                    count=parse_thread_snapshot(thread_raw,os.getpid()); maximum_threads=max(maximum_threads,count)
                    rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
                    if platform.system()!='Darwin': rss*=1024
                    if maximum_threads>2 or rss>2147483648 or time.monotonic()-start>=600: raise ValueError('RESOURCE_LIMIT')
                    lo,hi=method.ranks(w)
                    cells.append(dict(**meta,origin_count=len(ids),rank_I=lo,rank_F=hi,
                                      both_empirical_minimizer_endpoints=(19*w)%20==0,
                                      changed_capacity_count=int(np.count_nonzero(pred['I']!=pred['F'])),
                                      imported_QR_summary=qr,reference_F_metrics_exact=True,
                                      private_file=f'private/{key}.npz',private_sha256=sha((output/'private'/f'{key}.npz').read_bytes()),
                                      observed_os_threads=count))
                    audit['completed_cells']=len(cells)
        if len(cells)!=8 or len(summaries)!=16 or len(contrasts)!=24: raise ValueError('COMPLETE_INVENTORY')
        for name,rows in [('summary.csv',summaries),('annual.csv',annual),('nonoverlap.csv',sparse),('contrasts.csv',contrasts)]:
            write_csv(output/'public'/name,rows)
        check_frozen_files(ROOT,freeze['files'])
        final_thread_raw=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],capture_output=True,text=True,check=True).stdout
        maximum_threads=max(maximum_threads,parse_thread_snapshot(final_thread_raw,os.getpid()))
        rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if platform.system()!='Darwin': rss*=1024
        if maximum_threads>2 or rss>2147483648 or time.monotonic()-start>=600: raise ValueError('RESOURCE_LIMIT')
        audit.update(status='COMPLETE',finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start,
                     peak_rss_bytes=rss,maximum_observed_os_threads=maximum_threads,thread_snapshot_count=len(cells)+1,
                     requested_numerical_threads=1,resources_are_snapshot_observations=True,
                     executable_freeze_sha256=sha(freeze_raw),cells=cells,
                     summary_rows=len(summaries),annual_rows=len(annual),nonoverlap_rows=len(sparse),contrast_rows=len(contrasts))
        audit['exports']=[dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted((output/'public').glob('*.csv'))]
        save_audit(); return audit
    except Exception as e:
        audit.update(status='FAILED',failure_type=type(e).__name__,failure_code=str(e)[:120],finished_utc=datetime.now(timezone.utc).isoformat())
        save_audit(); raise
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM,old_handler)


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',required=True)
    args=p.parse_args(); result=execute(args.output)
    print(json.dumps({k:result[k] for k in ('status','completed_cells','elapsed_seconds','peak_rss_bytes','maximum_observed_os_threads')}))

if __name__=='__main__': main()
