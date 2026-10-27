"""Frozen E3 materialization and one-attempt MCS driver; no import-time study."""
from __future__ import annotations
import argparse
from copy import deepcopy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import zipfile

from run_v10_menu import committed_file, git
from run_v9_nonstationarity import atomic_json, load, save, sha, utc_now

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT/'results/v10/mcs'
PRIVATE_INPUTS = ROOT/'.scratch/v10/mcs-inputs'
PRIVATE_WORKERS = ROOT/'.scratch/v10/mcs-workers'
PROTOCOL = 'protocol/v10/mcs-design.md'
DESIGN_COMMIT = '78ea93493379ab3a93459d28e1bab84200f01539'
CODE = ('run_v10_mcs.py', 'v10_loss_inputs.py', 'v10_mcs.py', 'v10_mcs_summary.py')
SUPPORT = ('run_study.py', 'run_v8_wp3.py', 'run_v9_nonstationarity.py', 'run_v10_menu.py')
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')
ARRAY_FIELDS = ('origins', 'capacity', 'target', 'floor', 'loss')


def native(value):
    if value is None or type(value) in (str, bool, int, float):
        return value
    if isinstance(value, dict):
        return {str(k): native(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [native(v) for v in value]
    item = getattr(value, 'item', None)
    if item is not None:
        return native(item())
    raise ValueError('NONSCALAR_PUBLIC_METADATA')


def metadata(method):
    return native({k: deepcopy(v) for k, v in method.items() if k not in ARRAY_FIELDS})


def file_pin(path, root):
    path, root = Path(path), Path(root)
    return dict(path=str(path.relative_to(root)), bytes=path.stat().st_size, sha256=sha(path))


def verify_file(entry, root=ROOT, key='path'):
    path = Path(root)/entry[key]
    if path.is_symlink() or not path.is_file() or path.stat().st_size != entry['bytes'] or sha(path) != entry['sha256']:
        raise ValueError('INPUT_BYTES_CHANGED:'+str(entry[key]))
    return path


def verify_input_files(inventory, cftc_rows, root=ROOT):
    root = Path(root)
    for row in inventory['minimum_core_private_copy_manifest']:
        relative = Path(row['proposed_scratch_relative'])
        if relative.is_absolute() or not relative.parts or relative.parts[0] != '.scratch':
            raise ValueError('CORE_INPUT_NOT_NEW_PRIVATE_COPY')
        verify_file(dict(path=str(relative), bytes=row['bytes'], sha256=row['sha256']), root)
    for row in cftc_rows:
        verify_file(dict(path=row['trace_path'], bytes=row['trace_bytes'], sha256=row['trace_sha256']), root)
    return True


def augment_cftc_rows(rows, splits):
    axis = splits['indices']
    return [dict(row, family='CFTC', period='economic_date_replay_2021_2026',
        normalized_source='cftc:'+row['code'], source='cftc:'+row['code'], horizon=int(splits['horizon']),
        origin_count=int(axis['evaluation_n']), first_origin=int(axis['evaluation_first']),
        last_origin=int(axis['evaluation_last'])) for row in rows]


def array_pin(array):
    import numpy as np
    a = np.ascontiguousarray(array)
    return dict(shape=list(a.shape), dtype=a.dtype.str, sha256=hashlib.sha256(a.tobytes()).hexdigest())


def persist_registry(registry, public, private, root):
    """Write private full matrices and public metadata, never inventing floors."""
    import numpy as np
    public, private, root = Path(public), Path(private), Path(root)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(mode=0o700, parents=True, exist_ok=False)
    groups = []
    for i, original in enumerate(registry['groups']):
        group = native({k: deepcopy(v) for k, v in original.items() if k not in ('methods', 'planned_methods')})
        group.update(group_index=i, private_path=None, arrays={})
        planned = [metadata(m) for m in original.get('planned_methods', [])]
        group['planned_methods'] = planned
        if original['status'] != 'READY':
            complete_plan = planned or [metadata(m) for m in original['methods']]
            by_id = {m['method_id']: m for m in complete_plan}
            group['methods'] = [by_id[k] for k in sorted(by_id)]
            groups.append(group)
            continue
        methods = sorted(original['methods'], key=lambda m: m['method_id'])
        if not methods or len({m['method_id'] for m in methods}) != len(methods):
            raise ValueError('INVALID_READY_METHOD_INVENTORY')
        origins = np.asarray(methods[0]['origins'])
        peak = np.asarray(methods[0]['target'], dtype=float)
        n = len(origins)
        if (origins.ndim != 1 or origins.dtype.kind not in 'iu' or not n
                or np.any(np.diff(origins) != 1) or peak.shape != (n,) or not np.isfinite(peak).all()):
            raise ValueError('INVALID_READY_COMMON_AXIS')
        arrays = dict(origins=origins.astype(np.int64), peak=peak)
        descriptors = []
        for j, method in enumerate(methods):
            if not np.array_equal(method['origins'], origins) or not np.array_equal(method['target'], peak):
                raise ValueError('READY_COMMON_ORIGIN_OR_TARGET_MISMATCH')
            capacity, loss = np.asarray(method['capacity'], dtype=float), np.asarray(method['loss'], dtype=float)
            if capacity.shape != (n,) or loss.shape != (n,) or not np.isfinite(capacity).all() or not np.isfinite(loss).all() or np.any(loss < 0):
                raise ValueError('INVALID_READY_FULL_VECTOR')
            descriptor = dict(metadata(method), column_index=j, floor_key=None)
            if method.get('floor') is not None:
                floor = np.asarray(method['floor'], dtype=float)
                if floor.shape != (n,) or not np.isfinite(floor).all() or np.any(floor < 0) or np.any(capacity < floor) or np.any(peak < floor):
                    raise ValueError('INVALID_PROVIDED_FLOOR')
                descriptor['floor_key'] = f'floor_{j:03}'
                arrays[descriptor['floor_key']] = floor
            descriptors.append(descriptor)
        arrays['loss_matrix'] = np.column_stack([m['loss'] for m in methods]).astype(float)
        arrays['capacities_matrix'] = np.column_stack([m['capacity'] for m in methods]).astype(float)
        path = private/f'c{i:03}.npz'
        with path.open('xb') as stream:
            np.savez_compressed(stream, **arrays)
        path.chmod(0o600)
        pin = file_pin(path, root)
        group.update(methods=descriptors, n=n, first_origin=int(origins[0]), last_origin=int(origins[-1]),
            private_path=pin['path'], bytes=pin['bytes'], sha256=pin['sha256'],
            arrays={name: array_pin(a) for name, a in arrays.items()})
        groups.append(group)
    index = dict(schema='v10-mcs-input-index-v1', created_utc=utc_now(), groups=groups,
                 counts=native(registry['counts']), vectors_private=True, missing_floors_not_recovered=True)
    save(public/'input-index.json', index)
    return index


def load_group_arrays(group, root=ROOT):
    import numpy as np
    if group['status'] != 'READY':
        raise ValueError('GROUP_NOT_READY')
    path = verify_file(dict(path=group['private_path'], bytes=group['bytes'], sha256=group['sha256']), root)
    raw = path.read_bytes()
    if len(raw) != group['bytes'] or hashlib.sha256(raw).hexdigest() != group['sha256']:
        raise ValueError('PRIVATE_GROUP_CHANGED_DURING_READ')
    with np.load(io.BytesIO(raw), allow_pickle=False) as z:
        if set(z.files) != set(group['arrays']):
            raise ValueError('PRIVATE_ARRAY_INVENTORY_CHANGED')
        arrays = {k: np.array(z[k], copy=True) for k in z.files}
    for key, a in arrays.items():
        if array_pin(a) != group['arrays'][key] or not np.isfinite(a).all():
            raise ValueError('PRIVATE_ARRAY_SHAPE_DTYPE_OR_SHA_CHANGED:'+key)
    n, k = group['n'], len(group['methods'])
    if (arrays['origins'].shape != (n,) or arrays['origins'].dtype.kind not in 'iu'
            or not np.array_equal(arrays['origins'], np.arange(group['first_origin'], group['last_origin']+1))
            or arrays['peak'].shape != (n,) or arrays['loss_matrix'].shape != (n,k)
            or arrays['capacities_matrix'].shape != (n,k) or np.any(arrays['loss_matrix'] < 0)):
        raise ValueError('PRIVATE_FULL_GRID_MISMATCH')
    for j, method in enumerate(group['methods']):
        if method['column_index'] != j:
            raise ValueError('PRIVATE_METHOD_COLUMN_MISMATCH')
        key = method['floor_key']
        if key is not None and arrays[key].shape != (n,):
            raise ValueError('PRIVATE_PROVIDED_FLOOR_SHAPE')
    if path.read_bytes() != raw:
        raise ValueError('PRIVATE_GROUP_CHANGED_AFTER_READ')
    return arrays


def read_design():
    committed_file(ROOT/PROTOCOL, DESIGN_COMMIT, True)
    d = json.loads(re.search(r'```json\n(.*?)\n```', (ROOT/PROTOCOL).read_text(), re.S).group(1))
    for name, digest in d['unchanged_loss_and_combination_code_sha256'].items():
        if sha(ROOT/name) != digest:
            raise ValueError('FROZEN_LOSS_CODE_CHANGED:'+name)
    return d


def code_files(design):
    return list(dict.fromkeys([*CODE, *SUPPORT, *design['unchanged_loss_and_combination_code_sha256']]))


def committed_code(design):
    pins = {}
    for name in code_files(design):
        if git('show', 'HEAD:'+name) != (ROOT/name).read_bytes():
            raise ValueError('NUMERICAL_CODE_NOT_COMMITTED:'+name)
        pins[name] = sha(ROOT/name)
    return pins


def metadata_inputs(design):
    for path, digest in [(design['saved_inventory'], design['saved_inventory_sha256']),
                         (design['new_cftc_inventory'], design['new_cftc_inventory_sha256']),
                         (design['new_cftc_eligibility'], design['new_cftc_eligibility_sha256'])]:
        if sha(ROOT/path) != digest:
            raise ValueError('SOURCE_METADATA_CHANGED:'+path)
    inventory = load(ROOT/design['saved_inventory'])
    split_path = ROOT/'results/v10/cftc/splits.json'
    e2_manifest_path = ROOT/'results/v10/cftc/manifest.json'
    committed_file(split_path)
    committed_file(e2_manifest_path)
    if load(e2_manifest_path)['prepared_sha256']['splits.json'] != sha(split_path):
        raise ValueError('CFTC_AXIS_DIFFERS_FROM_SEALED_E2_SPLITS')
    splits = load(split_path)
    cftc = augment_cftc_rows(load(ROOT/design['new_cftc_inventory']), splits)
    return inventory, cftc


def prepare():
    d = read_design()
    hashes = committed_code(d)  # Must precede helper import or loss derivation.
    inventory, cftc = metadata_inputs(d)
    start_split_sha256 = sha(ROOT/'results/v10/cftc/splits.json')
    if len(inventory['minimum_core_private_copy_manifest']) != d['core_financial_trace_files'] or len(cftc) != d['new_cftc_method_cells']:
        raise ValueError('PREDECLARED_INPUT_FILE_COUNT_MISMATCH')
    verify_input_files(inventory, cftc)
    if PRIVATE_INPUTS.exists():
        raise ValueError('PRIVATE_INPUT_DESTINATION_EXISTS')
    PUBLIC.mkdir(parents=True, exist_ok=False)
    begin = utc_now()
    save(PUBLIC/'derivation-start.json', dict(materialization_started_utc=begin,
        timing_semantics='entry before build_registry; lower bound for first derived-loss call',
        cftc_splits_sha256=start_split_sha256,
        code_sha256=hashes, code_commit=git('rev-parse','HEAD').decode().strip(), design_commit=DESIGN_COMMIT))
    try:
        from v10_loss_inputs import build_registry
        registry = build_registry(inventory, cftc, d, ROOT)
        if len(registry['groups']) != d['total_expected_comparisons']:
            raise ValueError('PREDECLARED_COMPARISON_COUNT_MISMATCH')
        verify_input_files(inventory, cftc)
        if sha(ROOT/'results/v10/cftc/splits.json') != start_split_sha256:
            raise ValueError('CFTC_AXIS_CHANGED_DURING_MATERIALIZATION')
        index = persist_registry(registry, PUBLIC, PRIVATE_INPUTS, ROOT)
        if committed_code(d) != hashes:
            raise ValueError('CODE_CHANGED_DURING_DERIVATION')
        verify_input_files(inventory, cftc)
        if sha(ROOT/'results/v10/cftc/splits.json') != start_split_sha256:
            raise ValueError('CFTC_AXIS_CHANGED_AFTER_MATERIALIZATION')
        save(PUBLIC/'preparation.json', dict(status='PREPARED', materialization_started_utc=begin,
            materialization_ended_utc=utc_now(),
            timing_semantics='entry before build_registry; lower bound for first derived-loss call',
            code_sha256=hashes, counts=index['counts'],
            input_index_sha256=sha(PUBLIC/'input-index.json'), copied_manifest_sha256=sha(ROOT/d['copy_manifest']),
            cftc_splits_sha256=start_split_sha256))
        print(json.dumps(dict(status='PREPARED', groups=len(index['groups']), counts=index['counts'])))
    except Exception as exc:
        save(PUBLIC/'preparation-failure.json', dict(status='FAILED', materialization_started_utc=begin,
            materialization_ended_utc=utc_now(),
            timing_semantics='entry before build_registry; lower bound for first derived-loss call',
            reason=type(exc).__name__, message=str(exc), code_sha256=hashes))
        raise


def verify_private_index(index):
    for group in index['groups']:
        if group['status'] == 'READY':
            verify_file(dict(path=group['private_path'], bytes=group['bytes'], sha256=group['sha256']))


def seal():
    d = read_design(); hashes = committed_code(d)
    provenance = committed_file(PUBLIC/'input-index.json')
    index = load(PUBLIC/'input-index.json'); verify_private_index(index)
    inventory, cftc = metadata_inputs(d); verify_input_files(inventory, cftc)
    manifest = dict(schema='v10-mcs-seal-v1', created_utc=utc_now(), design=d, design_commit=DESIGN_COMMIT,
        design_provenance=committed_file(ROOT/PROTOCOL, DESIGN_COMMIT, True),
        code_commit=git('rev-parse','HEAD').decode().strip(), code_sha256=hashes,
        input_index_provenance=provenance, input_index_sha256=sha(PUBLIC/'input-index.json'),
        preparation_sha256=sha(PUBLIC/'preparation.json'), copied_manifest_sha256=sha(ROOT/d['copy_manifest']),
        cftc_splits_sha256=sha(ROOT/'results/v10/cftc/splits.json'))
    save(PUBLIC/'manifest.json', manifest)
    print(json.dumps(dict(status='SEALED', groups=len(index['groups']), code_commit=manifest['code_commit'])))


def verify_seal(manifest, upstream=False):
    if manifest['design'] != read_design() or manifest['design_commit'] != DESIGN_COMMIT:
        raise ValueError('MANIFEST_DESIGN_MISMATCH')
    committed_file(PUBLIC/'manifest.json')
    for name, digest in manifest['code_sha256'].items():
        if sha(ROOT/name) != digest:
            raise ValueError('SEALED_NUMERICAL_CODE_CHANGED:'+name)
    for path, digest in [(PUBLIC/'input-index.json', manifest['input_index_sha256']),
                         (PUBLIC/'preparation.json', manifest['preparation_sha256']),
                         (ROOT/manifest['design']['copy_manifest'], manifest['copied_manifest_sha256']),
                         (ROOT/'results/v10/cftc/splits.json', manifest['cftc_splits_sha256'])]:
        if sha(path) != digest:
            raise ValueError('SEALED_INPUT_METADATA_CHANGED:'+str(path))
    index = load(PUBLIC/'input-index.json')
    if upstream:
        verify_private_index(index)
        inventory, cftc = metadata_inputs(manifest['design'])
        verify_input_files(inventory, cftc)
    return index


def failed_row(group, reason, status='MCS_FAILED'):
    return dict(identity=group['identity'], group_label=group['group_label'], status=status,
        method_ids=[m['method_id'] for m in group['methods']],
        method_classes={m['method_id']:m['method_class'] for m in group['methods']},
        n=group.get('n'), seed=None, block_size=None, unique_loss_groups=[],
        included=[], excluded=[], pvalues={}, reason=reason,
        diagnostics={'library_attempts':0 if status=='FAILED_INPUT' else None})


def worker(args):
    manifest = load(PUBLIC/'manifest.json'); index = verify_seal(manifest)
    group = index['groups'][args.group]
    if group['status'] != 'READY':
        save(args.output, failed_row(group, 'REGISTRY_FAILED_INPUT', 'FAILED_INPUT')); return
    from run_study import RunGuard
    from run_v8_wp3 import ResourceCheckpoint
    from v10_mcs import compute_mcs
    started = time.monotonic(); public = Path(args.output).parent; private = Path(args.private)
    guard = RunGuard(started, utc_now(), 'v10-E3', public, private)
    plan = load(PUBLIC/'formal/plan.json')
    checkpoint = ResourceCheckpoint(guard, plan['deadline_monotonic'], private/'resources.jsonl')
    row = failed_row(group, 'WORKER_NOT_COMPLETED')
    try:
        checkpoint(stage='initialization')
        arrays = load_group_arrays(group)
        losses = {m['method_id']: arrays['loss_matrix'][:,m['column_index']] for m in group['methods']}
        row = dict(compute_mcs(losses, group['identity'], manifest['design'], checkpoint=checkpoint),
            identity=group['identity'], group_label=group['group_label'],
            method_classes={m['method_id']:m['method_class'] for m in group['methods']})
        verify_file(dict(path=group['private_path'], bytes=group['bytes'], sha256=group['sha256']))
        checkpoint(stage='finalization')
    except Exception as exc:
        row = failed_row(group, getattr(exc, 'code', type(exc).__name__)+': '+str(exc),
            'FAILED_INPUT' if isinstance(exc, (ValueError, OSError)) else 'MCS_FAILED')
    row.update(started_monotonic=started, ended_utc=utc_now(), elapsed_seconds=time.monotonic()-started,
               resources=guard.resources)
    save(args.output, native(row))


def run_batch(tasks, deadline, design, index):
    waiting, active, finished = list(tasks), [], []
    while waiting or active:
        now = time.monotonic()
        while waiting and len(active) < design['worker_count'] and now < deadline:
            task = waiting.pop(0); out = Path(task['output']); out.parent.mkdir(parents=True, exist_ok=False)
            private = Path(task['private']); private.mkdir(parents=True, exist_ok=False)
            command = [sys.executable, '-B', str(Path(__file__).resolve()), 'worker', '--group', str(task['group']), '--output', str(out), '--private', str(private)]
            log = (private/'console.txt').open('x')
            proc = subprocess.Popen(command, cwd=ROOT, env=dict(os.environ, **{k:'1' for k in THREADS}),
                stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            active.append(dict(task=task, proc=proc, log=log, start=time.monotonic())); now=time.monotonic()
        for item in list(active):
            now=time.monotonic(); proc=item['proc']; timeout=now>=deadline or now-item['start']>=design['worker_hard_seconds']
            if proc.poll() is None and timeout:
                try: os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                proc.wait()
            if proc.poll() is not None:
                item['log'].close(); task=item['task']; out=Path(task['output'])
                if not out.exists():
                    reason='GLOBAL_DEADLINE' if now>=deadline else 'WORKER_TIMEOUT' if timeout else 'TECHNICAL_WORKER_EXIT'
                    save(out, failed_row(index['groups'][task['group']], reason))
                finished.append(dict(task=task, elapsed_seconds=now-item['start'], exit_code=proc.returncode)); active.remove(item)
        if now>=deadline:
            for task in waiting:
                out=Path(task['output']); out.parent.mkdir(parents=True,exist_ok=False)
                save(out, failed_row(index['groups'][task['group']], 'GLOBAL_DEADLINE_NOT_RUN'))
                finished.append(dict(task=task, elapsed_seconds=0, exit_code=None))
            waiting=[]
        if active: time.sleep(.15)
    return finished


def formal():
    manifest=load(PUBLIC/'manifest.json'); index=verify_seal(manifest, upstream=True); d=manifest['design']
    base=PUBLIC/'formal'; base.mkdir(exist_ok=False); PRIVATE_WORKERS.mkdir(parents=True,exist_ok=False)
    started=time.monotonic(); deadline=started+d['global_mcs_max_seconds']
    save(base/'plan.json', dict(started_utc=utc_now(), started_monotonic=started, deadline_monotonic=deadline,
        worker_count=d['worker_count'], planned_groups=len(index['groups']), design_commit=DESIGN_COMMIT))
    tasks=[]
    for i, group in enumerate(index['groups']):
        out=base/'units'/f'c{i:03}'/'result.json'
        if group['status'] != 'READY':
            out.parent.mkdir(parents=True,exist_ok=False)
            save(out, failed_row(group, 'REGISTRY_FAILED_INPUT', 'FAILED_INPUT'))
        else:
            tasks.append(dict(group=i, output=str(out), private=str(PRIVATE_WORKERS/f'c{i:03}')))
    completed=run_batch(tasks, deadline, d, index)
    save(base/'completion.json', dict(ended_utc=utc_now(), elapsed_seconds=time.monotonic()-started,
        tasks=completed, planned_groups=len(index['groups'])))
    verify_seal(manifest, upstream=True)
    entries=[]
    with zipfile.ZipFile(base/'units.zip','x',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((base/'units').rglob('*')):
            if path.is_file():
                raw=path.read_bytes(); name=str(path.relative_to(base/'units')); archive.writestr(name,raw)
                entries.append(dict(path=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    save(base/'units-manifest.json', dict(files=entries, archive_sha256=sha(base/'units.zip'), loose_files_retained=True))
    records=[load(base/'units'/f'c{i:03}'/'result.json') for i in range(len(index['groups']))]
    from v10_mcs_summary import summarize
    result=summarize(records,index['groups'],d)
    save(PUBLIC/'summary.json',native(result)); save(PUBLIC/'full-cells.json',records)
    fields=('period','normalized_source','horizon','window','group_label','status','n','seed','block_size','method_ids','included','excluded','pvalues','unique_loss_groups','method_classes','reason')
    with (PUBLIC/'full-cells.csv').open('x',newline='') as stream:
        writer=csv.DictWriter(stream,fields); writer.writeheader()
        for row in records:
            flat=dict(row.get('identity',{}), **{k:row.get(k) for k in fields if k not in row.get('identity',{})})
            writer.writerow({k:json.dumps(v,ensure_ascii=True,separators=(',',':')) if isinstance(v,(list,dict)) else v for k,v in flat.items()})
    print(json.dumps(dict(status='COMPLETE_ARCHIVE', planned_groups=len(records), statuses={s:sum(r['status']==s for r in records) for s in sorted({r['status'] for r in records})})))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=('prepare','seal','formal','worker'))
    parser.add_argument('--group',type=int); parser.add_argument('--output'); parser.add_argument('--private'); args=parser.parse_args()
    {'prepare':prepare,'seal':seal,'formal':formal}.get(args.command,lambda:worker(args))()


if __name__=='__main__':
    main()
