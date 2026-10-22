"""Reproduce descriptive diagnostics inside one audited frozen replication.

Explicit --replication-dir is required. No model, raw-source reader, network,
installation, forecast repair or historical output write is invoked. Import and
--help use only the standard library. The numerical work reuses the published,
hash-pinned diagnostic functions on new hash-verified private trace snapshots.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import csv
import importlib.util
import inspect
import io
import math
import os
from pathlib import Path
import platform
import re
import signal
import sys
import time
import types
import zipfile

import reproduce_conditional as rep
import reconcile_conditional_replication as adapter

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
RESULTS = rep.RESULTS
PLAN = 'protocol/revision-20261022/post-result-diagnostics.md'
BUILDER = RESULTS + '/post-result-builder-v01.py'
BASE_AUDIT = RESULTS + '/post-result-diagnostics-audit.json'
DIAGNOSTIC_NAMES = ('post-result-floor.csv', 'post-result-horizon.csv')
TABLE_COUNTS = dict(zip(('evaluation-summary.csv', 'evaluation-annual.csv',
    'evaluation-nonoverlap.csv', 'paired-comparisons.csv', 'paired-annual.csv',
    'paired-nonoverlap.csv'), (90, 372, 90, 98, 388, 98)))
DIAGNOSTIC_FILES = {
    PLAN: (2818, 'd9a533ceb0e9db035f866f4c2d7516f14c8959fd6355332d39b231b1565592eb'),
    BUILDER: (7728, 'd491761af3c79a2cbda18589b07b516f44a73be9f06342cecded948042e60e1c'),
    RESULTS+'/post-result-floor.csv': (10673, 'c874905a9fcc454cf08aec69738d2bc61dc5364716c940a94f5c7211bf4e0863'),
    RESULTS+'/post-result-horizon.csv': (3847, '59bc82949da1642daed554ed0fcc2f9d16f989773a988cb11ecbd297fa6a5a5a'),
    BASE_AUDIT: (10453, 'af898abaa70e9f047b252c9ed28fd86b896670731f9a366bf8a8f7331bd63606'),
}


@dataclass(frozen=True)
class DiagnosticContract:
    """Injection seam for synthetic tests; no command-line alternate contract."""
    files: dict


def require(condition, code):
    if not condition:
        raise rep.ReproductionError(code)


def file_identity(raw):
    return dict(bytes=len(raw), sha256=rep.sha(raw))


def _contract(contract):
    return DiagnosticContract(DIAGNOSTIC_FILES) if contract is None else contract


def _attempt(root, value):
    root = Path(root).absolute()
    path = Path(value)
    path = path if path.is_absolute() else root/path
    try:
        relative = str(path.relative_to(root))
    except ValueError:
        raise rep.ReproductionError('ATTEMPT_BOUNDARY') from None
    require(re.fullmatch(r'\.scratch/revision-20261022/replication-[A-Za-z0-9][A-Za-z0-9_-]{0,63}', relative) is not None,
            'ATTEMPT_BOUNDARY')
    require('..' not in path.parts and not any(p.is_symlink() for p in (path, *path.parents)) and path.is_dir(),
            'ATTEMPT_BOUNDARY')
    return root, path


def _rows(raw):
    try:
        values = list(csv.reader(io.StringIO(raw.decode('utf-8'), newline='')))
        require(bool(values) and bool(values[0]) and len(set(values[0])) == len(values[0])
                and all(len(r) == len(values[0]) for r in values[1:]), 'CSV_STRUCTURE')
        return [dict(zip(values[0], row)) for row in values[1:]]
    except (UnicodeError, csv.Error):
        raise rep.ReproductionError('CSV_STRUCTURE') from None


def _methods(spec, cell):
    _, s, _, w, family = cell
    if family:
        return [family]
    prefixes = ('rolling', 'frozen', 'one_state') if spec['sources'][s]['one_state_reference_neighbors'][str(w)] else ('rolling', 'frozen')
    return [p+'_'+r for p in prefixes for r in ('F', 'S', 'K')]


def _receipt_name(cell):
    phase, s, h, w, family = cell
    return f'evaluation-{s}-h{h}-w{w}-{family}.json' if family else f'references-{s}-h{h}-w{w}.json'


def _matrix(cells):
    return [(c['source'], c['horizon'], c['window'], c['family'], c['status'], c['parameter']) for c in cells]


def _queue(raw, expected, root, attempt):
    data = rep.strict_json(raw)
    require(type(data.get('version')) is int and data['version'] == 1 and type(data.get('cells')) is list, 'QUEUE_INTEGRITY')
    cells = data['cells']
    require([tuple(c.get(k) for k in ('phase', 'source', 'horizon', 'window', 'family')) for c in cells] == expected,
            'QUEUE_INVENTORY')
    for row, cell in zip(cells, expected):
        path = rep.worker_directory(attempt, cell)/'public/manifest.json'
        require(row.get('receipt_path') == str(path.relative_to(root))
                and row.get('status') == 'COMPLETE' and row.get('stop_code') is None
                and type(row.get('exit_code')) is int and row['exit_code'] == 0
                and row.get('timed_out') is False
                and not row.get('controller_error') and not row.get('worker_controller_error'), 'QUEUE_TERMINAL')
    return cells


def _inventory(spec, selected):
    cells = rep.phase_jobs(spec, 'evaluation') + rep.phase_jobs(spec, 'references')
    full = []
    for cell in cells:
        _, s, h, w, family = cell
        cfg = spec['sources'][s]
        for method in _methods(spec, cell):
            parameter = (selected[s, h, w, family]['parameter'] if family else
                cfg['one_state_reference_neighbors'][str(w)] if method.startswith('one_state_') else None)
            full.append(dict(source=s, native_unit=cfg['native_unit'], horizon=h, window=w,
                method=method, parameter='' if parameter is None else str(parameter)))
    require(len(cells) == 32 and len(full) == 90 and len({(r['source'], r['horizon'], r['window'], r['method']) for r in full}) == 90,
            'DIAGNOSTIC_INVENTORY')
    return cells, full


def _check_labels(rows, expected, *, horizon=False):
    if horizon:
        wanted = []
        by_key = {(r['source'], r['horizon'], r['window'], r['method']): r for r in expected}
        for short in expected:
            if short['horizon'] != 6:
                continue
            long = by_key[short['source'], 24, short['window'], short['method']]
            wanted.append(dict(source=short['source'], native_unit=short['native_unit'], window=short['window'],
                method=short['method'], parameter_h6=short['parameter'], parameter_h24=long['parameter']))
    else:
        wanted = expected
    require(len(rows) == len(wanted), 'DIAGNOSTIC_ROW_COUNT')
    for row, meta in zip(rows, wanted):
        require(all(row.get(k) == str(v) for k, v in meta.items()), 'DIAGNOSTIC_LABELS')


def prepare(root, replication_dir, *, archive_contract=None, diagnostic_contract=None):
    """Stdlib-only, read-only preflight; every parsed input has a byte identity."""
    try:
        root, attempt = _attempt(root, replication_dir)
        destination = attempt/'post-result-diagnostics'
        require(not destination.exists() and not destination.is_symlink(), 'DIAGNOSTIC_OUTPUT_EXISTS')
        archive = rep.verify_archive(root, contract=archive_contract)
        require(archive['verified_result_files'] == 69, 'ARCHIVE_INVENTORY')
        spec = archive['spec']; contract = _contract(diagnostic_contract)
        require(set(contract.files) == set(DIAGNOSTIC_FILES), 'DIAGNOSTIC_ARCHIVE_INVENTORY')
        snapshots = {}
        def read(path, *, cap=8*1024*1024, within=None):
            p = rep.project_file(root, path, within=within)
            raw = rep.read_bytes(root, p, cap=cap, within=within)
            name = str(p.relative_to(root)); found = file_identity(raw)
            if name in snapshots:
                require(found == snapshots[name]['identity'], 'INPUT_SNAPSHOT_CHANGED')
            snapshots[name] = dict(identity=found, cap=cap,
                within_attempt=within is not None)
            return raw
        original = {}
        for name, expected in contract.files.items():
            raw = read(name)
            require((len(raw), rep.sha(raw)) == tuple(expected), 'DIAGNOSTIC_ARCHIVE_HASH')
            original[name] = raw
        base = rep.strict_json(original[BASE_AUDIT])
        require(base.get('status') == 'VERIFIED' and (base.get('floor_rows'), base.get('horizon_rows')) == (90, 45)
                and base.get('builder_sha256') == rep.sha(original[BUILDER])
                and base.get('plan') == dict(path=PLAN, sha256=rep.sha(original[PLAN]))
                and base.get('exports') == [dict(path=n, **file_identity(original[RESULTS+'/'+n])) for n in DIAGNOSTIC_NAMES],
                'DIAGNOSTIC_BASE_AUDIT')
        controller = rep.strict_json(read(attempt/'controller-final.json', within=attempt))
        require(type(controller.get('version')) is int and controller['version'] == 1
                and controller.get('status') == 'REPLICATION_AUDITED' and controller.get('stop_code') is None
                and controller.get('accuracy_recomputed') is True and controller.get('selection_agrees_with_archive') is True
                and controller.get('attempt_path') == str(attempt.relative_to(root))
                and controller.get('executable_freeze_sha256') == archive['executable_freeze_sha256']
                and controller.get('archived_selection_sha256') == archive['selection_freeze_sha256']
                and all(controller.get(k) == n for k,n in (('completed_validation_cells',24),
                    ('completed_evaluation_reference_cells',32),('validation_jobs_retained',24),('evaluation_reference_jobs_retained',32))),
                'CONTROLLER_NOT_AUDITED')
        selection_path = attempt/'selection-freeze.json'
        selection_raw = read(selection_path, within=attempt); selection_hash = rep.sha(selection_raw)
        require(controller.get('selection_path') == str(selection_path.relative_to(root))
                and controller.get('selection_sha256') == selection_hash
                and selection_hash != archive['selection_freeze_sha256'], 'SELECTION_SNAPSHOT_HASH')
        selection = rep.strict_json(selection_raw)
        def lookup(path, key):
            expected = rep.worker_directory(attempt, ('validation', *key))/'public/manifest.json'
            require(path == str(expected.relative_to(root)), 'NEW_VALIDATION_PATH')
            return read(expected, within=attempt)
        rep.verify_selection(selection, spec, archive['executable_freeze_sha256'], lookup)
        require(_matrix(selection['cells']) == _matrix(archive['selection']['cells'])
                and len(selection['cells']) == 24 and all(c['status'] == 'SELECTED' for c in selection['cells']), 'SELECTION_CHANGED')
        selected = {(c['source'], c['horizon'], c['window'], c['family']):c for c in selection['cells']}
        cells, expected_rows = _inventory(spec, selected)
        require(spec['horizons'] == [6,24], 'HORIZON_INVENTORY')
        validation = _queue(read(attempt/'validation-queue.json', within=attempt), rep.phase_jobs(spec,'validation'), root, attempt)
        for queued, chosen in zip(validation, selection['cells']):
            reference = chosen['validation_receipts'][0]
            require((queued['receipt_path'], queued['receipt_sha256']) == (reference['path'], reference['sha256']), 'VALIDATION_QUEUE_HASH')
        queue_path = attempt/'evaluation-queue.json'; queue_raw = read(queue_path, within=attempt)
        require(controller.get('queue_path') == str(queue_path.relative_to(root)), 'CONTROLLER_QUEUE_PATH')
        queue = _queue(queue_raw, cells, root, attempt)
        audit_output = attempt/'numerical-audit/public'
        comparison_path = audit_output/'reproduction-comparison.json'
        controller_audit = controller['audit']
        require(controller_audit.get('status') == 'NUMERICAL_AUDIT_VERIFIED'
                and controller_audit.get('comparison_path') == str(comparison_path.relative_to(root)), 'NUMERICAL_AUDIT_PATH')
        comparison_raw = read(comparison_path, within=attempt)
        comparison = rep.strict_json(comparison_raw)
        require(type(comparison.get('version')) is int and comparison['version'] == 1
                and comparison.get('status') == 'NUMERICAL_AUDIT_VERIFIED'
                and comparison.get('archived_selection_sha256') == archive['selection_freeze_sha256']
                and comparison.get('new_selection_sha256') == selection_hash
                and comparison.get('selection_status_parameter_matrix_identical') is True
                and comparison.get('queue_sha256') == rep.sha(queue_raw)
                and comparison.get('source_identities') == {s:{k:c[k] for k in ('sha256','bytes','record_count','native_unit')} for s,c in spec['sources'].items()}
                and (comparison.get('summary_rows'),comparison.get('annual_rows'),comparison.get('paired_rows'),comparison.get('paired_annual_rows')) == (90,372,98,388),
                'NUMERICAL_AUDIT_RECEIPT')
        adapter.verify_resource(comparison['audit_resources'])
        names = list(TABLE_COUNTS) + [_receipt_name(c) for c in cells]
        exports = comparison['exports']; receipt_exports = comparison['receipts']
        require([r.get('path') for r in exports] == names and len(set(names)) == 38
                and [r.get('public_file') for r in receipt_exports] == names[6:], 'NUMERICAL_EXPORT_INVENTORY')
        exported = {}
        for entry in exports:
            name = entry['path']; raw = read(audit_output/name, within=attempt)
            require(entry == dict(path=name, **file_identity(raw)), 'NUMERICAL_EXPORT_HASH')
            exported[name] = raw
        tables = {}
        for name,count in TABLE_COUNTS.items():
            require(len(_rows(exported[name])) == count, 'NUMERICAL_TABLE_INVENTORY')
            old = read(RESULTS+'/'+name)
            tables[name] = adapter.compare_csv(exported[name], old)
        require(comparison.get('tables') == tables, 'NUMERICAL_TABLE_COMPARISON')
        for label, key in (('exact_csv_byte_agreement','byte_identical'),('exact_csv_scalar_agreement','exact_scalar_agreement')):
            expected = all(t[key] for t in tables.values())
            require(comparison.get(label) is expected and controller_audit.get(label) is expected, 'NUMERICAL_AGREEMENT_FLAGS')
        for queued, cell, receipt_entry in zip(queue, cells, receipt_exports):
            name = _receipt_name(cell)
            require(receipt_entry == dict(public_file=name, **file_identity(exported[name]))
                    and queued['receipt_sha256'] == rep.sha(exported[name]), 'AUDITED_RECEIPT_HASH')
        summary = _rows(exported['evaluation-summary.csv'])
        _check_labels(summary, expected_rows)
        _check_labels(_rows(original[RESULTS+'/post-result-floor.csv']), expected_rows)
        _check_labels(_rows(original[RESULTS+'/post-result-horizon.csv']), expected_rows, horizon=True)
        return dict(root=root, attempt=attempt, destination=destination, archive=archive,
            archive_contract=archive_contract, diagnostic_contract=contract, original=original,
            controller=controller, comparison=comparison, selection=selection, selection_hash=selection_hash,
            selected=selected, cells=cells, expected_rows=expected_rows, queue=queue,
            summary=summary, exported_receipts={n:exported[n] for n in names[6:]}, snapshots=snapshots)
    except rep.ReproductionError:
        raise
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, OSError, OverflowError):
        raise rep.ReproductionError('DIAGNOSTIC_PREFLIGHT') from None


def load_diagnostic_helpers(root, contract=None):
    """Load real pinned helper definitions; never invoke the historical main."""
    contract = _contract(contract)
    raw = rep.read_bytes(root, BUILDER)
    require((len(raw), rep.sha(raw)) == tuple(contract.files[BUILDER]), 'DIAGNOSTIC_HELPER_HASH')
    path = rep.project_file(root, BUILDER)
    helper = types.ModuleType('_published_floor_horizon_helpers')
    helper.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), helper.__dict__)
    for name, count in (('floor_diagnostics',3),('horizon_diagnostics',4)):
        function = getattr(helper,name,None)
        require(callable(function) and len(inspect.signature(function).parameters) == count, 'DIAGNOSTIC_HELPER_INTERFACE')
    return helper


def _consume(inputs, path, *, cap=8*1024*1024):
    root = inputs['root']; attempt = inputs['attempt']
    actual = rep.project_file(root, path, within=attempt)
    raw = rep.read_bytes(root, actual, within=attempt, cap=cap)
    name = str(actual.relative_to(root)); found = file_identity(raw)
    if name in inputs['snapshots']:
        require(inputs['snapshots'][name]['identity'] == found, 'INPUT_SNAPSHOT_CHANGED')
    inputs['snapshots'][name] = dict(identity=found, cap=cap, within_attempt=True)
    return raw


def _check_trace_headers(raw, wanted, np, count):
    """Reject wrong shapes/dtypes before np.load can allocate from NPY headers."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zipped:
            entries = zipped.infolist()
            require(len(entries) == len(wanted) and len({e.filename for e in entries}) == len(entries)
                    and {e.filename for e in entries} == {n+'.npy' for n in wanted}
                    and all(not e.flag_bits & 1 and e.file_size <= 64*1024*1024 for e in entries)
                    and sum(e.file_size for e in entries) <= 128*1024*1024, 'NPZ_INVENTORY_OR_SIZE')
            for entry in entries:
                name = entry.filename[:-4]
                with zipped.open(entry) as stream:
                    version = np.lib.format.read_magic(stream)
                    require(version in ((1,0),(2,0)), 'NPZ_HEADER')
                    reader = np.lib.format.read_array_header_1_0 if version == (1,0) else np.lib.format.read_array_header_2_0
                    shape,fortran,dtype = reader(stream,max_header_size=10000)
                    wanted_dtype = np.dtype('int64') if name.endswith(('_origins','_refit_indices')) else np.dtype('float64')
                    require(shape == (count,) and dtype == wanted_dtype and not dtype.hasobject
                            and type(fortran) is bool and not fortran
                            and entry.file_size == stream.tell()+count*wanted_dtype.itemsize, 'NPZ_HEADER')
    except rep.ReproductionError:
        raise
    except (ValueError,TypeError,OverflowError,OSError,EOFError,zipfile.BadZipFile):
        raise rep.ReproductionError('NPZ_HEADER') from None


def derive(inputs, np, diagnostic_helpers, *, checkpoint=lambda **kwargs:None, arrays=lambda *values:None):
    """Reconcile retained traces and derive exactly90 floor and45 horizon rows."""
    try:
        spec = inputs['archive']['spec']; stored = {}; targets = {}; floor_rows = []; input_receipts = []
        numerical = adapter._load_helpers(inputs['root'])
        require(all(callable(getattr(numerical, n, None)) for n in ('verify_method','summarize_scores')), 'NUMERICAL_HELPER_INTERFACE')
        summary_by_key = {(r['source'],int(r['horizon']),int(r['window']),r['method']):r for r in inputs['summary']}
        for queued, cell in zip(inputs['queue'], inputs['cells']):
            checkpoint(stage='diagnostic_input')
            phase,s,h,w,family = cell; cfg = spec['sources'][s]
            raw = _consume(inputs,queued['receipt_path']); name = _receipt_name(cell)
            require(raw == inputs['exported_receipts'][name] and rep.sha(raw) == queued['receipt_sha256'], 'NEW_RECEIPT_HASH')
            receipt = rep.strict_json(raw); result = receipt['result']
            require(tuple(receipt.get(n) for n in ('phase','source','horizon','window','family')) == cell
                    and receipt.get('executable_freeze_sha256') == inputs['archive']['executable_freeze_sha256']
                    and receipt.get('selection_freeze_sha256') == (inputs['selection_hash'] if family else None)
                    and receipt.get('source_identity') is not None
                    and all(receipt['source_identity'].get(n) == cfg[n] for n in ('sha256','bytes','record_count','native_unit'))
                    and result.get('native_unit') == cfg['native_unit'], 'NEW_RECEIPT_IDENTITY')
            adapter.verify_resource(receipt['resources'])
            parameter = inputs['selected'][s,h,w,family]['parameter'] if family else None
            require(not family or result.get('selection') == dict(status='SELECTED',parameter=parameter), 'NEW_RECEIPT_SELECTION')
            methods = _methods(spec,cell); adapter.verify_phase_labels(receipt,methods,parameter)
            first,last = cfg['evaluation_origin_first'],cfg['evaluation_origin_last']
            require(result.get('origin_identity') == rep.origin_identity(first,last), 'NEW_ORIGIN_IDENTITY')
            adapter.verify_fit_records(result['fit_diagnostics'],cfg,h,w,family,first,last)
            origins = np.arange(first,last+1,dtype=np.int64)
            require(len(receipt['artifacts']) == 1, 'NPZ_ARTIFACT_INVENTORY')
            trace_path = rep.project_file(inputs['root'],queued['receipt_path'],within=inputs['attempt']).parent.parent/'private/numeric-traces.npz'
            trace_raw = _consume(inputs,trace_path,cap=64*1024*1024)
            wanted = {method+'_'+n for method in methods for n in ('origins','peak','floor','refit_indices','capacity','pinball')}
            _check_trace_headers(trace_raw,wanted,np,len(origins))
            with adapter._checked_npz(trace_raw,receipt['artifacts'][0],wanted,np,numerical) as traces:
                for method, reported in zip(methods,result['summary_rows']):
                    key = (s,h,w,method)
                    require(all(traces[method+'_'+n].shape == origins.shape for n in ('origins','peak','floor','refit_indices','capacity','pinball')), 'NPZ_SHAPE')
                    p = traces[method+'_peak']; b = traces[method+'_floor']; c = traces[method+'_capacity']
                    require(np.array_equal(traces[method+'_origins'],origins), 'TRACE_ISSUES')
                    require(bool(np.all(b >= 0)) and bool(np.all(p >= b)) and bool(np.all(c >= b)), 'TRACE_KNOWN_FLOOR')
                    if (s,h) in targets:
                        expected_peak, expected_floor = targets[s,h]
                        require(np.array_equal(p,expected_peak) and np.array_equal(b,expected_floor), 'CROSS_CELL_TARGET_FLOOR')
                    else:
                        targets[s,h] = (p.copy(),b.copy())
                    refits = first + ((origins-first)//cfg['refit_step'])*cfg['refit_step'] if family or method.startswith('frozen_') else origins
                    scores = numerical.verify_method(traces,method,origins,p,b,refits)
                    metrics = numerical.summarize_scores(scores)
                    require(reported == dict(method=method,parameter=parameter)|metrics, 'TRACE_SUMMARY')
                    metadata = summary_by_key[key]
                    expected_summary = dict(source=s,native_unit=cfg['native_unit'],horizon=h,window=w,method=method,
                        parameter=cfg['one_state_reference_neighbors'][str(w)] if method.startswith('one_state_') else parameter,
                        refit_step=cfg['refit_step'] if family or method.startswith('frozen_') else 1,
                        plain_knn_full_pool_fallback=method=='KNN' and parameter==w)|metrics
                    require(metadata == {k: '' if v is None else str(v) for k,v in expected_summary.items()}, 'TRACE_EXPORTED_SUMMARY')
                    meta = {n:metadata[n] for n in ('source','native_unit','horizon','window','method','parameter')}
                    # Keep native integer labels, matching the historical CSV order.
                    meta.update(horizon=h,window=w)
                    floor_rows.append(meta|diagnostic_helpers.floor_diagnostics(p,c,b))
                    stored[key] = dict(origins=origins,peak=p.copy(),floor=b.copy(),capacity=c.copy(),parameter=metadata['parameter'])
                    arrays(stored,targets,origins,p,b,c,scores)
            input_receipts.append(dict(receipt=name,receipt_sha256=rep.sha(raw),private_archive_sha256=rep.sha(trace_raw),
                private_archive_bytes=len(trace_raw)))
            checkpoint(stage='diagnostic_receipt_checked')
        _check_labels(_rows(adapter.csv_bytes(floor_rows)),inputs['expected_rows'])
        horizon_rows = []
        for (s,h,w,method), short in stored.items():
            if h != 6:
                continue
            long = stored[s,24,w,method]
            require(np.array_equal(short['origins'],long['origins']) and np.array_equal(short['floor'],long['floor']), 'HORIZON_ISSUE_FLOOR')
            require(bool(np.all(short['peak'] <= long['peak'])), 'HORIZON_TARGET_ORDER')
            horizon_rows.append(dict(source=s,native_unit=spec['sources'][s]['native_unit'],window=w,method=method,
                parameter_h6=short['parameter'],parameter_h24=long['parameter'])|
                diagnostic_helpers.horizon_diagnostics(short['capacity'],long['capacity'],short['peak'],long['peak']))
        require((len(floor_rows),len(horizon_rows)) == (90,45), 'DIAGNOSTIC_ROW_COUNT')
        _check_labels(_rows(adapter.csv_bytes(horizon_rows)),inputs['expected_rows'],horizon=True)
        checkpoint(stage='diagnostic_rows_verified')
        return floor_rows,horizon_rows,input_receipts
    except rep.ReproductionError:
        raise
    except (KeyError,TypeError,ValueError,AttributeError,IndexError,OverflowError,FloatingPointError,OSError):
        raise rep.ReproductionError('DIAGNOSTIC_TRACE_RECONCILIATION') from None


def verify_snapshots(inputs):
    """Recheck identities, never reparse later bytes as the accepted snapshot."""
    rep.verify_archive(inputs['root'],contract=inputs['archive_contract'])
    for name, entry in inputs['snapshots'].items():
        raw = rep.read_bytes(inputs['root'],name,cap=entry['cap'],
            within=inputs['attempt'] if entry['within_attempt'] else None)
        require(file_identity(raw) == entry['identity'], 'INPUT_SNAPSHOT_CHANGED')


def verify_exports(root, destination, exports):
    """Check actual newly written bytes, including a symlink-safe boundary."""
    for entry in exports:
        path = Path(destination)/'public'/entry['path']
        raw = rep.read_bytes(root,path,within=destination)
        require(entry == dict(path=entry['path'],**file_identity(raw)), 'DIAGNOSTIC_EXPORT_CHANGED')


def reproduce(root, replication_dir, *, archive_contract=None, diagnostic_contract=None,
              guard_factory=None, started=None):
    """Write exclusively inside the selected replica; fixtures are test-only."""
    started = time.monotonic() if started is None else started
    production = archive_contract is None and diagnostic_contract is None
    require((archive_contract is None) == (diagnostic_contract is None), 'TEST_CONTRACT_PAIR')
    require(not production or guard_factory is None, 'TEST_ONLY_GUARD')
    require(not production or platform.system() == 'Darwin', 'DARWIN_REQUIRED')
    require(importlib.util.find_spec('numpy') is not None, 'NUMPY_REQUIRED_NO_INSTALL')
    inputs = prepare(root,replication_dir,archive_contract=archive_contract,diagnostic_contract=diagnostic_contract)
    require(time.monotonic()-started < 540., 'RESOURCE_WALL')
    for name in rep.THREAD_NAMES:
        os.environ[name] = '1'
    import numpy as np
    from run_study import RunGuard,create_attempt
    helpers = load_diagnostic_helpers(inputs['root'],inputs['diagnostic_contract'])
    try:
        public,private = create_attempt(inputs['destination'])
    except Exception as error:
        raise rep.ReproductionError(getattr(error,'code','OUTPUT_INTEGRITY')) from None
    guard = (RunGuard if guard_factory is None else guard_factory)(started,rep.utc_now(),inputs['destination'],public,private)
    try:
        guard(stage='diagnostic_reproduction_start')
        floor_rows,horizon_rows,receipts = derive(inputs,np,helpers,checkpoint=guard,arrays=guard.arrays)
        tables = {}; exports = []
        for name,rows in zip(DIAGNOSTIC_NAMES,(floor_rows,horizon_rows)):
            raw = adapter.csv_bytes(rows)
            tables[name] = adapter.compare_csv(raw,inputs['original'][RESULTS+'/'+name])
            with (public/name).open('xb') as stream:
                stream.write(raw)
            exports.append(dict(path=name,**file_identity(raw)))
        guard(stage='diagnostic_reproduction_exports')
        verify_snapshots(inputs)
        comparison = dict(version=1,status='DIAGNOSTIC_COMPARISON_RECORDED',created_utc=rep.utc_now(),
            floor_rows=len(floor_rows),horizon_rows=len(horizon_rows),tables=tables,
            exact_csv_byte_agreement=all(t['byte_identical'] for t in tables.values()),
            exact_csv_scalar_agreement=all(t['exact_scalar_agreement'] for t in tables.values()))
        comparison_raw = rep.json_bytes(comparison)
        with (public/'diagnostic-comparison.json').open('xb') as stream:
            stream.write(comparison_raw)
        exports.append(dict(path='diagnostic-comparison.json',**file_identity(comparison_raw)))
        verify_snapshots(inputs)
        guard(stage='diagnostic_reproduction_final')
        verify_exports(inputs['root'],inputs['destination'],exports)
        # Measure the final full input/output readbacks as well as derivation.
        guard(stage='diagnostic_verified_before_receipt')
        require(time.monotonic()-started < 540., 'RESOURCE_WALL')
        audit = dict(version=1,status='DIAGNOSTICS_REPRODUCED',created_utc=rep.utc_now(),
            analysis_status='EXPLICITLY_POST_RESULT_DESCRIPTIVE',
            scope='Trace/receipt consistency after audited frozen replication; all90floor reports and45same-source/window/method horizon pairs; no forecast repair',
            raw_sources_read=False,models_refitted=False,main_98_comparisons_changed=False,
            replication_dir=str(inputs['attempt'].relative_to(inputs['root'])),
            executable_freeze_sha256=inputs['archive']['executable_freeze_sha256'],
            archived_selection_sha256=inputs['archive']['selection_freeze_sha256'],
            new_selection_sha256=inputs['selection_hash'],verified_archived_result_files=69,
            numerical_replication_exact_byte_agreement=inputs['comparison']['exact_csv_byte_agreement'],
            numerical_replication_exact_scalar_agreement=inputs['comparison']['exact_csv_scalar_agreement'],
            floor_rows=len(floor_rows),horizon_rows=len(horizon_rows),input_receipts=receipts,
            exact_csv_byte_agreement=comparison['exact_csv_byte_agreement'],
            exact_csv_scalar_agreement=comparison['exact_csv_scalar_agreement'],tables=tables,
            input_file_identities={k:v['identity'] for k,v in sorted(inputs['snapshots'].items())},
            resources=dict(guard.resources),runtime=dict(platform_system=platform.system(),machine=platform.machine(),
                python_version=platform.python_version(),numpy_version=np.__version__),
            implementation_sha256=rep.sha(Path(__file__).read_bytes()),
            original_builder_sha256=rep.sha(inputs['original'][BUILDER]),exports=exports,
            resource_counter_scope='Only this diagnostic output directory; final audit receipt is written after the final measured checkpoint')
        rep.write_json(public/'diagnostic-reproduction-audit.json',audit,exclusive=True)
        return audit
    except Exception as error:
        code = getattr(error,'code','DIAGNOSTIC_REPRODUCTION_FAILED')
        if type(code) is not str or re.fullmatch(r'[A-Z][A-Z0-9_]{0,63}',code) is None:
            code = 'DIAGNOSTIC_REPRODUCTION_FAILED'
        # Leave any partial aggregate files and a failure receipt; never call
        # them verified or retry with altered scientific choices.
        rep.write_json(public/'diagnostic-failure.json',dict(version=1,status='STOPPED',stop_code=code,
            created_utc=rep.utc_now(),verified_diagnostics=False,raw_sources_read=False,
            resources=dict(guard.resources)),exclusive=True)
        if isinstance(error,rep.ReproductionError):
            raise
        raise rep.ReproductionError(code) from None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replication-dir',required=True,
        help='Existing .scratch/revision-20261022/replication-SAFEID with REPLICATION_AUDITED controller')
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        require(platform.system() == 'Darwin','DARWIN_REQUIRED')
        # A 600s hard alarm complements RunGuard's measured 540s internal stop.
        signal.signal(signal.SIGALRM,signal.SIG_DFL)
        signal.setitimer(signal.ITIMER_REAL,600.)
        audit = reproduce(ROOT,args.replication_dir,started=started)
        print(rep.json_bytes({k:audit[k] for k in ('status','floor_rows','horizon_rows',
            'exact_csv_byte_agreement','exact_csv_scalar_agreement','raw_sources_read','resources')}).decode(),end='')
        return 0
    except rep.ReproductionError as error:
        print(rep.json_bytes(dict(status='STOPPED',stop_code=error.code,verified_diagnostics=False)).decode(),end='')
        return 1
    finally:
        if platform.system() == 'Darwin':
            signal.setitimer(signal.ITIMER_REAL,0.)


if __name__ == '__main__':
    raise SystemExit(main())
