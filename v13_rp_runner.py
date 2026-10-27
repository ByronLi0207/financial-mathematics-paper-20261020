"""Execution of pre-specified v13 RP using unchanged forecast/cache adapters."""
from __future__ import annotations
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[_name]='1'
import argparse,hashlib,io,json,math
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from v12_inputs import load_series
from v12_forecast import make_context
from v12_runner import _guard,_failure
from v12_decomposition import MENU,select_candidate
from v13_validation_runner import attempt_cached,scalar,write_new
from v13_rp import paired_gate

ROOT=Path(__file__).resolve().parent


def trace_losses(attempt,ids,new_cache,old_cache):
    if attempt['status']!='COMPLETE':raise ValueError('COMPLETE_TRACE_REQUIRED')
    base=Path(old_cache) if attempt['cache_source']=='v12' else Path(new_cache)
    if attempt['trace_path']!='trace.npz':raise ValueError('TRACE_PATH')
    raw=(base/attempt['cache_key']/'trace.npz').read_bytes()
    if len(raw)!=attempt['trace_bytes'] or hashlib.sha256(raw).hexdigest()!=attempt['trace_sha256']:
        raise ValueError('TRACE_HASH_OR_SIZE')
    with np.load(io.BytesIO(raw),allow_pickle=False) as a:
        origins=np.array(a['origins'],copy=True);losses=np.array(a['losses'],copy=True)
    if not np.array_equal(origins,ids) or losses.shape!=ids.shape or not np.isfinite(losses).all():
        raise ValueError('FULL_ALIGNED_TRACE_REQUIRED')
    return losses


def _relative(value,reference):
    if reference is None or not math.isfinite(reference) or reference<=0:raise ValueError('POSITIVE_F_REFERENCE_REQUIRED')
    result=100*((value-reference)/reference)
    if not math.isfinite(result):raise ValueError('NONFINITE_RELATIVE_LOSS')
    return result


def compute_rp(cell,new_cache,old_cache,private,deadline):
    guard=_guard(deadline)
    row={k:v for k,v in cell.items() if k!='source'}
    row.update(source_sha256=cell['source']['sha256'],status='FAILED',rp_status='FAILED',ordinary_status='FAILED',F_status='FAILED',
        rp_reason=None,ordinary_reason=None,route=None,route_qr_indicator=None,
        long_selected_penalty=None,ordinary_selected_penalty=None,
        reference_loss=None,rp_loss=None,ordinary_loss=None,rp_relative_loss_pct=None,ordinary_relative_loss_pct=None)
    candidates=[];refs={};choices={};gate=dict(status='NOT_CALCULATED',route=None,reason=None)
    if not cell.get('eligible',True):
        row.update(status='EXCLUDED',rp_status='EXCLUDED',ordinary_status='EXCLUDED',F_status='EXCLUDED',rp_reason=cell['exclusion_reason'],ordinary_reason=cell['exclusion_reason'])
        return dict(row=row,candidates=candidates,references=refs,choices=choices,gate=gate)
    try:
        guard();context=make_context(load_series(cell['source'],ROOT),cell)
        va=np.arange(cell['validation_first'],cell['validation_last']+1,dtype=np.int64)
        ba=np.arange(cell['baseline_validation_first'],cell['baseline_validation_last']+1,dtype=np.int64)
        ev=np.arange(cell['evaluation_first'],cell['evaluation_last']+1,dtype=np.int64)
        if (len(va),len(ba),len(ev))!=(cell['validation_n'],cell['baseline_validation_n'],cell['evaluation_n']):raise ValueError('FULL_ORIGIN_GEOMETRY_REQUIRED')
        attempts={}
        for segment,ids in [('long_validation',va),('ordinary_validation',ba)]:
            owned=[]
            for penalty in MENU:
                got=attempt_cached(context,cell['source'],ids,'QR33',penalty,.95,new_cache,old_cache,guard)
                attempts[(segment,penalty)]=got
                item=scalar(got,segment,'QR33',penalty);owned.append(item);candidates.append(item)
            choices[segment]=select_candidate(owned,expected_n=len(ids))
        long=choices['long_validation'];ordinary=choices['ordinary_validation']
        row['long_selected_penalty']=long['penalty'];row['ordinary_selected_penalty']=ordinary['penalty']
        if long['status']=='SELECTED':
            fval=attempt_cached(context,cell['source'],va,'F',None,.95,new_cache,old_cache,guard)
            refs['long_validation']=scalar(fval,'long_validation','F',None)
            if fval['status']=='COMPLETE':
                selected=attempts[('long_validation',long['penalty'])]
                qloss=trace_losses(selected,va,new_cache,old_cache);floss=trace_losses(fval,va,new_cache,old_cache)
                gate=paired_gate(qloss,floss,cell['horizon'])
                gate.update(selected_validation_loss=selected['summary']['mean_loss'],F_validation_loss=fval['summary']['mean_loss'],
                    selected_trace_sha256=selected['trace_sha256'],F_trace_sha256=fval['trace_sha256'])
            else:gate=dict(status='FIT_FAILURE',route=None,reason='F_VALIDATION_FAILED:'+str(fval.get('reason')))
        else:gate=dict(status='FIT_FAILURE',route=None,reason='LONG_VALIDATION_CANDIDATE_FAILURE')
        # This on-disk seal precedes every evaluation cache read and score.
        seal=dict(choices=choices,gate=gate,references=refs,sealed_utc=datetime.now(timezone.utc).isoformat())
        write_new(Path(private)/'choices.json',seal)
        f=attempt_cached(context,cell['source'],ev,'F',None,.95,new_cache,old_cache,guard)
        refs['evaluation']=scalar(f,'evaluation','F',None);row['F_status']=f['status'];row['reference_loss']=refs['evaluation']['mean_loss']
        if ordinary['status']=='SELECTED':
            got=attempt_cached(context,cell['source'],ev,'QR33',ordinary['penalty'],.95,new_cache,old_cache,guard)
            candidates.append(scalar(got,'ordinary_evaluation','QR33',ordinary['penalty']))
            if got['status']=='COMPLETE' and f['status']=='COMPLETE':
                loss=got['summary']['mean_loss'];rel=_relative(loss,row['reference_loss'])
                row.update(ordinary_status='COMPLETE',ordinary_loss=loss,ordinary_relative_loss_pct=rel)
            else:
                failed=got if got['status']!='COMPLETE' else f
                row.update(ordinary_status='FAILED_RESOURCE' if 'RESOURCE' in failed['status'] else 'FAILED',ordinary_reason=failed.get('reason'))
        else:
            bad=next((c for c in candidates if c['segment']=='ordinary_validation' and c['status']!='COMPLETE'),{})
            row.update(ordinary_status='FAILED_RESOURCE' if 'RESOURCE' in bad.get('status','') else 'FAILED',ordinary_reason=bad.get('reason') or ordinary['reason'])
        if gate['status'] in ('AVAILABLE','UNAVAILABLE') and gate['route'] in ('F','QR'):
            if gate['route']=='F':rp=f
            else:
                rp=attempt_cached(context,cell['source'],ev,'QR33',long['penalty'],.95,new_cache,old_cache,guard)
                candidates.append(scalar(rp,'rp_evaluation','QR33',long['penalty']))
            if rp['status']=='COMPLETE' and f['status']=='COMPLETE':
                loss=rp['summary']['mean_loss'];rel=_relative(loss,row['reference_loss'])
                row.update(rp_status='COMPLETE',rp_loss=loss,rp_relative_loss_pct=rel,route=gate['route'],route_qr_indicator=int(gate['route']=='QR'),rp_reason=gate.get('reason'))
            else:
                failed=rp if rp['status']!='COMPLETE' else f
                row.update(rp_status='FAILED_RESOURCE' if 'RESOURCE' in failed['status'] else 'FAILED',rp_reason=failed.get('reason'))
        else:
            bad=next((c for c in candidates if c['segment']=='long_validation' and c['status']!='COMPLETE'),{})
            row.update(rp_status='FAILED_RESOURCE' if 'RESOURCE' in bad.get('status','') else 'FAILED',rp_reason=bad.get('reason') or gate.get('reason'))
        row.update(gate_status=gate['status'],gate_mean_difference=gate.get('mean_difference'),
            gate_standard_error=gate.get('standard_error'),gate_lrv=gate.get('lrv'),gate_bandwidth=gate.get('bandwidth'),
            choice_sealed_utc=seal['sealed_utc'],proposed_route=gate.get('route'))
        row['status']='COMPLETE' if row['rp_status']=='COMPLETE' and row['ordinary_status']=='COMPLETE' and row['F_status']=='COMPLETE' else 'FAILED'
    except Exception as exc:
        failure=_failure(exc)
        row.update(status=failure['status'],rp_reason=row.get('rp_reason') or failure['reason'],ordinary_reason=row.get('ordinary_reason') or failure['reason'],exception_type=failure.get('exception_type'))
    return dict(row=row,candidates=candidates,references=refs,choices=choices,gate=gate)


def worker(spec_path):
    spec=json.loads(Path(spec_path).read_text())
    for name,digest in spec['code_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('WORKER_CODE_CHANGED:'+name)
    result=compute_rp(spec['cell'],spec['new_cache'],spec['old_cache'],spec['private'],spec['deadline_monotonic'])
    write_new(spec['result'],result)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker',required=True);worker(p.parse_args().worker)
