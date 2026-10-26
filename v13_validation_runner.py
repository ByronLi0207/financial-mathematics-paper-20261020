"""G2 execution adapter: unchanged v12 forecasts and read-only prior cache.

No fitting at import. Parent owns standalone design/code gates and hard caps.
"""
from __future__ import annotations
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[_name]='1'
import argparse
from datetime import datetime,timezone
import hashlib,json,math,time
from pathlib import Path
import numpy as np
from v12_inputs import load_series
from v12_forecast import make_context
from v12_runner import _identity,_read_cache,_attempt,_guard,_failure,_clean,ResourceStop
from v12_decomposition import MENU,select_candidate

ROOT=Path(__file__).resolve().parent


def write_new(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:json.dump(_clean(value),f,indent=2,allow_nan=False);f.write('\n')


def attempt_cached(context,source,ids,method,penalty,tau,new_cache,old_cache,guard):
    """Read a matching original cache without writing; new attempts only v13."""
    identity,key,normalized,p=_identity(context,source,ids,method,penalty,tau)
    try:guard()
    except ResourceStop as exc:return dict(status='NOT_RUN_RESOURCE_LIMIT',reason=exc.code,cache_key=key,cache_source=None)
    previous=Path(old_cache)/key
    if previous.exists():
        return dict(_read_cache(previous,identity,context,ids,tau),cache_key=key,cache_source='v12')
    return dict(_attempt(context,source,ids,method,penalty,tau,new_cache,guard),cache_source='v13')


def scalar(attempt,segment,method,penalty):
    return dict(segment=segment,method=method,penalty=penalty,status=attempt['status'],
        reason=attempt.get('reason'),cache_key=attempt.get('cache_key'),cache_source=attempt.get('cache_source'),
        trace_sha256=attempt.get('trace_sha256'),mean_loss=attempt.get('summary',{}).get('mean_loss'),
        n=attempt.get('summary',{}).get('n'),fit_count=len(attempt.get('fit_diagnostics',[])))


def compute_method(cell,method,new_cache,old_cache,private,deadline):
    """Six candidates, sealed choice, then matched F and selected evaluation."""
    guard=_guard(deadline)
    row={k:v for k,v in cell.items() if k!='source'}
    row.update(method=method,status='FAILED',reason=None,source_sha256=cell['source']['sha256'],
        selected_penalty=None,actual_loss=None,reference_loss=None,relative_loss_pct=None)
    candidates=[];reference={};selection={}
    try:
        guard();context=make_context(load_series(cell['source'],ROOT),cell)
        va=np.arange(cell['validation_first'],cell['validation_last']+1,dtype=np.int64)
        ev=np.arange(cell['evaluation_first'],cell['evaluation_last']+1,dtype=np.int64)
        if len(va)!=cell['validation_n'] or len(ev)!=cell['evaluation_n']:
            raise ValueError('FULL_DECLARED_ORIGINS_REQUIRED')
        for penalty in MENU:
            got=attempt_cached(context,cell['source'],va,method,penalty,cell['tau'],new_cache,old_cache,guard)
            candidates.append(scalar(got,'validation',method,penalty))
        selection=select_candidate(candidates,expected_n=len(va))
        write_new(Path(private)/'selection.json',dict(selection=selection,candidates=candidates,sealed_utc=datetime.now(timezone.utc).isoformat()))
        row['selected_penalty']=selection['penalty']
        f=attempt_cached(context,cell['source'],ev,'F',None,cell['tau'],new_cache,old_cache,guard)
        reference=scalar(f,'evaluation','F',None)
        row['reference_loss']=reference['mean_loss']
        if selection['status']!='SELECTED':
            bad=next((c for c in candidates if c['status']!='COMPLETE'),{})
            row.update(status='FAILED_RESOURCE' if 'RESOURCE' in bad.get('status','') else 'FAILED',reason=bad.get('reason') or selection['reason'])
        else:
            got=attempt_cached(context,cell['source'],ev,method,selection['penalty'],cell['tau'],new_cache,old_cache,guard)
            evaluation=scalar(got,'evaluation',method,selection['penalty']);candidates.append(evaluation)
            if got['status']!='COMPLETE' or f['status']!='COMPLETE':
                failed=got if got['status']!='COMPLETE' else f
                row.update(status='FAILED_RESOURCE' if 'RESOURCE' in failed['status'] else 'FAILED',reason=failed.get('reason'))
            elif not isinstance(row['reference_loss'],(float,int)) or row['reference_loss']<=0:
                row['reason']='POSITIVE_REFERENCE_REQUIRED'
            else:
                actual=evaluation['mean_loss'];excess=100*((actual-row['reference_loss'])/row['reference_loss'])
                if not math.isfinite(excess):raise ValueError('NONFINITE_RELATIVE_LOSS')
                row.update(status='COMPLETE',reason=None,actual_loss=actual,relative_loss_pct=excess)
    except Exception as exc:row.update(**{k:v for k,v in _failure(exc).items() if k in ('status','reason','exception_type','diagnostics')})
    return dict(row=row,candidates=candidates,reference=reference,selection=selection)


def worker(spec_path):
    spec=json.loads(Path(spec_path).read_text())
    for name,digest in spec['code_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('WORKER_CODE_CHANGED:'+name)
    result=compute_method(spec['cell'],spec['method'],spec['new_cache'],spec['old_cache'],spec['private'],spec['deadline_monotonic'])
    write_new(spec['result'],result)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',required=True)
    worker(parser.parse_args().worker)
