"""Once-attempt v12 worker; parent owns protocol/code seals and scheduling."""
from __future__ import annotations
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[_name] = '1'
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import resource
import time
import numpy as np
from v12_inputs import load_series
from v12_forecast import make_context, predict_segment, score_report
from v12_decomposition import MENU, select_candidate, decompose

ROOT = Path(__file__).resolve().parent
FORECAST_CODE = ('v12_forecast.py','v10_menu.py','v8_mechanism_mc.py',
    'conditional_features.py','conditional_quantile.py','empirical_headroom.py',
    'study_core.py','v6_inference.py')
TRACE_KEYS = ('origins','capacity','target','floor','losses','refit_indices')


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _clean(value):
    if isinstance(value, np.generic): value = value.item()
    if isinstance(value, dict): return {k:_clean(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)): return [_clean(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value): return str(value)
    return value


def _write(path, value):
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    descriptor = os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'w') as stream:
        json.dump(_clean(value),stream,indent=2,allow_nan=False); stream.write('\n')


class ResourceStop(Exception):
    def __init__(self, code): self.code=code; super().__init__(code)


def _guard(deadline):
    def check(**detail):
        if deadline is not None and time.monotonic() >= deadline:
            raise ResourceStop('RESOURCE_DEADLINE')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if platform.system() != 'Darwin': rss *= 1024
        if rss >= 2*1024**3: raise ResourceStop('RESOURCE_RSS')
    return check


def _failure(exc):
    return dict(status='FAILED_RESOURCE' if isinstance(exc,ResourceStop) else 'FAILED',
        reason=str(getattr(exc,'code',str(exc) or type(exc).__name__)),
        exception_type=type(exc).__name__, diagnostics=_clean(dict(getattr(exc,'diagnostics',{}))))


def _identity(context, source, ids, method, penalty, tau):
    if penalty == 'inf': method,penalty = 'I',None
    times = context['times'].astype('datetime64[us]').astype('<i8')
    identity = dict(source_sha256=source['sha256'], source_bytes=source['bytes'],
        aligned_grid_sha256=hashlib.sha256(times.tobytes()).hexdigest(),
        panel_grid_source_sha256=source.get('grid_source',{}).get('sha256'),
        **context['cell'],tau=float(tau),method=method,penalty=penalty,
        origins_first=int(ids[0]),origins_last=int(ids[-1]),n=len(ids),
        origins_sha256=hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest(),
        forecast_code_sha256={name:_sha(ROOT/name) for name in FORECAST_CODE})
    key = hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return identity,key,method,penalty


def _summary(score):
    return {k:v for k,v in score.items() if k not in ('losses','peak','floor')}


def _read_cache(folder, identity, context, ids, tau):
    terminal = folder/'terminal.json'
    if not terminal.is_file():
        return dict(status='FAILED',reason='STALE_STARTED_OR_INCOMPLETE_CACHE')
    try:
        saved = json.loads(terminal.read_text())
        if saved['identity'] != identity: raise ValueError('CACHE_GEOMETRY_CHANGED')
        if saved['status'] != 'COMPLETE': return saved
        trace = folder/saved['trace_path']
        if saved['trace_path']!='trace.npz' or trace.stat().st_size!=saved['trace_bytes']:
            raise ValueError('CACHE_TRACE_HASH_OR_SIZE')
        raw = trace.read_bytes()
        if len(raw)!=saved['trace_bytes'] or hashlib.sha256(raw).hexdigest()!=saved['trace_sha256']:
            raise ValueError('CACHE_TRACE_HASH_OR_SIZE')
        with np.load(io.BytesIO(raw),allow_pickle=False) as archive:
            if set(archive.files)!=set(TRACE_KEYS): raise ValueError('CACHE_TRACE_KEYS')
            arrays = {k:np.array(archive[k],copy=True) for k in TRACE_KEYS}
        if any(a.shape!=ids.shape or not np.isfinite(a).all() for a in arrays.values()):
            raise ValueError('CACHE_FULL_VECTOR_REQUIRED')
        step = context['cell']['refit_step']
        if (not np.array_equal(arrays['origins'],ids)
                or not np.array_equal(arrays['refit_indices'],ids[0]+step*((ids-ids[0])//step))):
            raise ValueError('CACHE_ORIGIN_OR_REFIT_CHANGED')
        score = score_report(context,ids,arrays['capacity'],tau=tau)
        for name,key in [('target','peak'),('floor','floor'),('losses','losses')]:
            if not np.array_equal(arrays[name],score[key]): raise ValueError('CACHE_SCORE_VECTOR_CHANGED')
        if saved['summary']!=_summary(score): raise ValueError('CACHE_SUMMARY_CHANGED')
        return saved
    except Exception as exc:
        return dict(status='FAILED',reason='CACHE_VALIDATION_FAILED:'+str(exc))


def _attempt(context, source, ids, method, penalty, tau, cache_root, guard):
    identity,key,method,penalty = _identity(context,source,ids,method,penalty,tau)
    folder = Path(cache_root)/key
    try: guard()
    except ResourceStop as exc:
        return dict(status='NOT_RUN_RESOURCE_LIMIT',reason=exc.code,cache_key=key)
    if folder.exists(): return dict(_read_cache(folder,identity,context,ids,tau),cache_key=key)
    try: folder.mkdir(parents=True,exist_ok=False,mode=0o700)
    except FileExistsError:
        return dict(status='FAILED',reason='CONCURRENT_OR_STALE_CACHE',cache_key=key)
    _write(folder/'attempt.json',dict(status='STARTED',identity=identity,
        started_utc=datetime.now(timezone.utc).isoformat()))
    try:
        p = predict_segment(context,ids,method,penalty,tau=tau,checkpoint=guard)
        step = context['cell']['refit_step']
        if (not np.array_equal(p['origins'],ids)
                or not np.array_equal(p['refit_indices'],ids[0]+step*((ids-ids[0])//step))):
            raise ValueError('FULL_ORIGINS_AND_REFIT_REQUIRED')
        score = score_report(context,ids,p['capacity'],tau=tau); guard()
        path = folder/'trace.npz'
        with path.open('xb') as stream:
            np.savez_compressed(stream,origins=ids,capacity=p['capacity'],target=score['peak'],
                floor=score['floor'],losses=score['losses'],refit_indices=p['refit_indices'])
        os.chmod(path,0o600)
        result = dict(status='COMPLETE',reason=None,identity=identity,summary=_summary(score),
            fit_diagnostics=p['fit_diagnostics'],trace_path=path.name,
            trace_bytes=path.stat().st_size,trace_sha256=_sha(path))
    except Exception as exc: result = dict(identity=identity,**_failure(exc))
    _write(folder/'terminal.json',result)
    return dict(result,cache_key=key)


def _scalar(base, method, penalty, segment, attempt):
    return dict(base,method=method,penalty=penalty,segment=segment,
        status=attempt['status'],reason=attempt.get('reason'),cache_key=attempt['cache_key'],
        mean_loss=attempt.get('summary',{}).get('mean_loss'),n=attempt.get('summary',{}).get('n'))


def _method_row(base, method):
    return dict(base,method=method,status='FAILED',reason=None,selected_penalty=None,
        reference_loss=None,actual_loss=None,relative_loss_pct=None,actual_excess_pct=None,
        selection_component_pct=None,signal_gap_pct=None)


def _persist(path, value):
    value = _clean(value); path = Path(path)
    if path.exists():
        if json.loads(path.read_text())!=value:
            raise ValueError('IMMUTABLE_RESULT_CHANGED:'+path.name)
    else: _write(path,value)


def _finish(result, folder):
    for row in result['rows']: _persist(folder/f"{row['method']}.result.json",row)
    _persist(folder/'references.json',result['references'])
    _persist(folder/'cell-result.json',result)
    return result


def compute_cell(cell, experiment, cache_root, output_root, *, deadline_monotonic=None):
    """Compute one declared geometry; no protocol invention, retry or fallback."""
    if experiment not in ('F1','F2','F3') or cell.get('experiment',experiment)!=experiment:
        raise ValueError('EXPERIMENT_MISMATCH')
    fixed = ('QR33',) if experiment=='F3' else ('QR33','QR4')
    declared = cell.get('methods',fixed)
    if not isinstance(declared,(list,tuple)): raise ValueError('INVALID_METHOD_SUBSET')
    methods = tuple(declared)
    allowed = (('QR33',),('QR4',),fixed) if experiment=='F2' else (fixed,)
    if methods not in allowed: raise ValueError('INVALID_METHOD_SUBSET')
    base = {k:v for k,v in cell.items() if k not in ('source','methods')}
    base['source_sha256'] = cell['source']['sha256']
    rows = [_method_row(base,m) for m in methods]
    result = dict(cell=cell,status='FAILED',rows=rows,candidates=[],references={})
    folder = Path(output_root)/cell['cell_id']
    guard = _guard(deadline_monotonic)
    try:
        guard(); context = make_context(load_series(cell['source']),cell)
    except Exception as exc:
        failure = _failure(exc)
        for row in rows: row.update(status=failure['status'],reason=failure['reason'])
        result['references'] = {m:failure.copy() for m in ('F','I')}
        return _finish(result,folder)
    va = np.arange(cell['validation_first'],cell['validation_last']+1,dtype=np.int64)
    ev = np.arange(cell['evaluation_first'],cell['evaluation_last']+1,dtype=np.int64)
    if len(va)!=cell['validation_n'] or len(ev)!=cell['evaluation_n'] or not len(va) or not len(ev):
        raise ValueError('DECLARED_FULL_SEGMENT_COUNT_MISMATCH')
    chosen = {}
    # Seal every model's validation choice before even reference evaluation.
    for method,row in zip(methods,rows):
        candidates = [_scalar(base,method,p,'validation',_attempt(context,cell['source'],va,
            method,p,cell['tau'],cache_root,guard)) for p in MENU]
        result['candidates'].extend(candidates)
        selection = select_candidate(candidates,expected_n=cell['validation_n'])
        chosen[method] = selection
        seal = dict(cell_id=cell['cell_id'],method=method,selection=selection,
                    validation_candidates=candidates)
        path = Path(output_root)/cell['cell_id']/f'{method}.selection.json'
        if path.exists():
            saved = json.loads(path.read_text()); saved.pop('selection_frozen_utc',None)
            if saved!=seal: raise ValueError('SEALED_SELECTION_CHANGED')
        else: _write(path,dict(seal,selection_frozen_utc=datetime.now(timezone.utc).isoformat()))
        row.update(selected_penalty=selection['penalty'],selection_path=str(path))
        if selection['status']!='SELECTED':
            row['reason'] = next((r['reason'] for r in candidates if r['status']!='COMPLETE'),selection['reason'])
            if any(r['status'] in ('FAILED_RESOURCE','NOT_RUN_RESOURCE_LIMIT') for r in candidates):
                row['status']='FAILED_RESOURCE'
            _persist(folder/f'{method}.result.json',row)
    for method in ('F','I'):
        attempt = _attempt(context,cell['source'],ev,method,None,cell['tau'],cache_root,guard)
        result['references'][method] = dict(status=attempt['status'],reason=attempt.get('reason'),
            cache_key=attempt['cache_key'],**attempt.get('summary',{}))
    _persist(folder/'references.json',result['references'])
    reference = result['references']['F'].get('mean_loss')
    for method,row in zip(methods,rows):
        if chosen[method]['status']!='SELECTED': continue
        row['reference_loss'] = reference
        penalties = MENU if experiment=='F1' else (row['selected_penalty'],)
        candidates = [_scalar(base,method,p,'evaluation',_attempt(context,cell['source'],ev,
            method,p,cell['tau'],cache_root,guard)) for p in penalties]
        result['candidates'].extend(candidates)
        _persist(folder/f'{method}.evaluation-candidates.json',candidates)
        if experiment=='F1':
            row.update(decompose(candidates,row['selected_penalty'],reference))
        elif candidates[0]['status']!='COMPLETE': row['reason'] = candidates[0]['reason']
        else:
            row['actual_loss'] = candidates[0]['mean_loss']
            if reference is None or reference<=0: row['reason']='POSITIVE_REFERENCE_REQUIRED'
            else:
                excess = 100*((row['actual_loss']-reference)/reference)
                if not math.isfinite(excess): row['reason']='NONFINITE_RELATIVE_LOSS'
                else: row.update(status='COMPLETE',reason=None,actual_excess_pct=excess)
        failed = next((r for r in candidates if r['status']!='COMPLETE'),None)
        if failed is None and result['references']['F']['status']!='COMPLETE':
            failed = result['references']['F']
        if failed is not None:
            row.update(reason=failed.get('reason'),status='FAILED_RESOURCE'
                if failed['status'] in ('FAILED_RESOURCE','NOT_RUN_RESOURCE_LIMIT') else 'FAILED')
        row['relative_loss_pct'] = row['actual_excess_pct']
        _persist(folder/f'{method}.result.json',row)
    result['status'] = 'COMPLETE' if all(r['status']=='COMPLETE' for r in rows) else 'FAILED'
    return _finish(result,folder)


def worker_job(spec_path):
    """Verify the supplied code seal, then run ordered cells within job/cell caps.

    Return scalar JSON only. The parent captures/materializes this result and
    owns global deadlines, hard process termination and public summaries.
    """
    spec = json.loads(Path(spec_path).read_text()); started = time.monotonic()
    expected = spec.get('expected_code_sha256')
    if not isinstance(expected,dict) or not expected: raise ValueError('CODE_HASH_SEAL_REQUIRED')
    for name,digest in expected.items():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or _sha(ROOT/path)!=digest:
            raise ValueError('CODE_HASH_MISMATCH:'+name)
    cap = float(spec['cap_seconds']); cell_cap = float(spec.get('cell_cap_seconds',cap))
    if not all(math.isfinite(v) and v>0 for v in (cap,cell_cap)): raise ValueError('POSITIVE_CAP_REQUIRED')
    cells = list(spec['cells']); experiment = spec['experiment']
    if not cells or (experiment!='F2' and len(cells)!=1): raise ValueError('ONE_GEOMETRY_JOB_REQUIRED')
    if experiment=='F2':
        group = {(c['source']['sha256'],c['horizon'],c['window'],c['refit_step'],c['tau'],
                  c['evaluation_first'],c['evaluation_last']) for c in cells}
        if len(group)!=1 or len(cells)>2: raise ValueError('F2_SAME_SOURCE_WINDOW_REQUIRED')
        cells.sort(key=lambda c:c['validation_n'])
    results = [compute_cell(c,experiment,spec['cache_root'],spec['output_root'],
        deadline_monotonic=min(started+cap,time.monotonic()+cell_cap)) for c in cells]
    return dict(experiment=experiment,job_id=Path(spec_path).stem,
        status='COMPLETE' if all(r['status']=='COMPLETE' for r in results) else 'FAILED',
        cells=results,rows=[row for r in results for row in r['rows']],
        candidates=[row for r in results for row in r['candidates']],
        elapsed_seconds=time.monotonic()-started,expected_code_sha256=expected)


if __name__=='__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--job',required=True)
    args = parser.parse_args()
    try: value = worker_job(args.job)
    except Exception as error: value = _failure(error)
    print(json.dumps(_clean(value),allow_nan=False))
