"""Run one bounded, frozen conditional-study phase; never fetch a source.

Import and --help require only the standard library. Numeric source loading is
deferred until exact executable and, for evaluation, selection identities pass.
Public output contains scalar aggregate rows; observation traces stay private.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import time

from run_study import RunGuard, StudyStop, arm_hard_deadline, create_attempt

ROOT = Path(__file__).resolve().parent
SPEC_PATH = 'protocol/revision-20261022/study-spec.json'
FREEZE_PATH = 'protocol/revision-20261022/executable-freeze.json'
CODE_FILES = (
    'conditional_quantile.py', 'test_conditional_quantile.py',
    'conditional_features.py', 'test_conditional_features.py',
    'conditional_study.py', 'test_conditional_study.py',
    'conditional_sources.py', 'test_conditional_sources.py',
    'run_conditional_study.py', 'test_run_conditional_study.py',
    'study_core.py', 'test_core.py', 'run_study.py', 'test_runner.py',
    SPEC_PATH, 'protocol/revision-20261022/conditional-baseline-design.md')
THREAD_NAMES = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
_HASH = re.compile(r'[0-9a-f]{64}\Z')
_SAFE_CODE = re.compile(r'[A-Z][A-Z0-9_]{0,63}\Z')


class PhaseError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def _is_hash(value):
    return type(value) is str and _HASH.fullmatch(value) is not None


def _integer(value, minimum=1):
    if type(value) is not int or value < minimum:
        raise PhaseError('SPECIFICATION')
    return value


def _utc(value):
    if type(value) is not str or not value.endswith('Z'):
        raise PhaseError('FREEZE_METADATA')
    try:
        datetime.fromisoformat(value[:-1] + '+00:00')
    except ValueError:
        raise PhaseError('FREEZE_METADATA') from None


def _project_file(path, root, *, scratch=False):
    root = Path(root).absolute()
    path = Path(path)
    path = path if path.is_absolute() else root / path
    if '..' in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise PhaseError('FILE_INTEGRITY')
    try:
        path.relative_to(root / '.scratch' if scratch else root)
    except ValueError:
        raise PhaseError('FILE_INTEGRITY') from None
    if not path.is_file():
        raise PhaseError('FILE_INTEGRITY')
    return path


def _pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PhaseError('JSON_DUPLICATE_KEY')
        result[key] = value
    return result


def _read_json(path, *, cap=4 * 1024 * 1024):
    try:
        with Path(path).open('rb') as stream:
            raw = stream.read(cap + 1)
        if len(raw) > cap:
            raise PhaseError('FILE_SIZE')
        value = json.loads(raw, object_pairs_hook=_pairs_no_duplicates,
                           parse_constant=lambda _: (_ for _ in ()).throw(PhaseError('JSON_NONFINITE')))
        if type(value) is not dict:
            raise PhaseError('JSON_OBJECT_REQUIRED')
        return raw, value
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise PhaseError('FILE_INTEGRITY') from None


def _validate_spec(spec):
    if (type(spec) is not dict or spec.get('tau_numerator') != 19
            or spec.get('tau_denominator') != 20
            or not spec.get('sources') or not spec.get('horizons')
            or not spec.get('families')
            or any(f not in ('QR', 'KNN', 'SCALED_KNN') for f in spec['families'])
            or len(set(spec['families'])) != len(spec['families'])):
        raise PhaseError('SPECIFICATION')
    for h in spec['horizons']:
        _integer(h)
    penalties = spec.get('qr_penalties')
    if (type(penalties) is not list or not penalties
            or any(type(p) not in (int, float) or not math.isfinite(p) or p <= 0 for p in penalties)
            or penalties != sorted(set(penalties))):
        raise PhaseError('SPECIFICATION')
    for source_id, cfg in spec['sources'].items():
        if source_id not in ('fx_hourly', 'nyfed_weekly') or type(cfg) is not dict:
            raise PhaseError('SPECIFICATION')
        if not _is_hash(cfg.get('sha256')) or type(cfg.get('native_unit')) is not str:
            raise PhaseError('SPECIFICATION')
        for name in ('bytes', 'record_count', 'refit_step', 'short_scale',
                     'long_scale', 'nominal_gap_seconds'):
            _integer(cfg.get(name))
        for segment in ('validation', 'evaluation'):
            first = _integer(cfg.get(segment + '_origin_first'), 0)
            last = _integer(cfg.get(segment + '_origin_last'), 0)
            if last < first or last + max(spec['horizons']) >= cfg['record_count']:
                raise PhaseError('SPECIFICATION')
        if cfg['validation_origin_last'] + max(spec['horizons']) >= cfg['evaluation_origin_first']:
            raise PhaseError('SPECIFICATION')
        if not cfg.get('windows') or len(set(cfg['windows'])) != len(cfg['windows']):
            raise PhaseError('SPECIFICATION')
        for w in cfg['windows']:
            _integer(w)
            candidates = cfg['knn_candidates'][str(w)]
            if (not candidates or candidates != sorted(set(candidates))
                    or any(type(k) is not int or not 19 <= k <= w for k in candidates)):
                raise PhaseError('SPECIFICATION')
            neighbor = cfg['one_state_reference_neighbors'][str(w)]
            if neighbor is not None and (type(neighbor) is not int or not 19 <= neighbor <= w):
                raise PhaseError('SPECIFICATION')
    return spec


def verify_executable_freeze(expected_sha256, *, root=None):
    """Check every exact declared code/spec/source identity before loading data."""
    root = ROOT if root is None else Path(root)
    try:
        if not _is_hash(expected_sha256):
            raise PhaseError('EXECUTABLE_FREEZE')
        path = _project_file(FREEZE_PATH, root)
        raw, manifest = _read_json(path)
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            raise PhaseError('EXECUTABLE_FREEZE')
        if (set(manifest) != {'version', 'status', 'files', 'sources', 'created_utc'}
                or type(manifest['version']) is not int or manifest['version'] != 1
                or manifest['status'] != 'FROZEN'
                or type(manifest['files']) is not dict
                or set(manifest['files']) != set(CODE_FILES)):
            raise PhaseError('EXECUTABLE_FREEZE')
        _utc(manifest['created_utc'])
        for name in CODE_FILES:
            expected = manifest['files'][name]
            if not _is_hash(expected):
                raise PhaseError('EXECUTABLE_FREEZE')
            content = _project_file(name, root).read_bytes()
            if hashlib.sha256(content).hexdigest() != expected:
                raise PhaseError('EXECUTABLE_FREEZE')
        _, spec = _read_json(_project_file(SPEC_PATH, root))
        _validate_spec(spec)
        sources = {key: dict(sha256=value['sha256'], bytes=value['bytes'])
                   for key, value in spec['sources'].items()}
        if manifest['sources'] != sources:
            raise PhaseError('EXECUTABLE_FREEZE')
        return spec, manifest
    except (OSError, KeyError, TypeError, ValueError):
        raise PhaseError('EXECUTABLE_FREEZE') from None


def _cell(spec, source_id, horizon, window, family, phase):
    if phase not in ('validation', 'evaluation', 'references'):
        raise PhaseError('CELL_CONFIGURATION')
    if (source_id not in spec['sources'] or type(horizon) is not int
            or horizon not in spec['horizons'] or type(window) is not int
            or window not in spec['sources'][source_id]['windows']
            or (phase == 'references' and family is not None)
            or (phase != 'references' and family not in spec['families'])):
        raise PhaseError('CELL_CONFIGURATION')
    return spec['sources'][source_id]


def _candidates(spec, cfg, window, family):
    return list(spec['qr_penalties'] if family == 'QR'
                else cfg['knn_candidates'][str(window)])


def _inventory(spec):
    return [(source, horizon, window, family)
            for source, cfg in spec['sources'].items()
            for horizon in spec['horizons'] for window in cfg['windows']
            for family in spec['families']]


def _origin_identity(origins):
    values = [int(value) for value in origins]
    if (not values or values[0] < 0 or values[-1] > (1 << 63) - 1
            or any(right != left + 1 for left, right in zip(values, values[1:]))):
        raise PhaseError('ORIGIN_IDENTITY')
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.to_bytes(8, 'little', signed=True))
    return dict(count=len(values), first=values[0], last=values[-1], sha256=digest.hexdigest())


def verify_selection_freeze(path, expected_sha256, executable_sha256, spec, *, root=None):
    """Verify complete cell inventory and recompute every receipt's selection."""
    root = ROOT if root is None else Path(root)
    try:
        if not _is_hash(expected_sha256) or not _is_hash(executable_sha256):
            raise PhaseError('SELECTION_FREEZE')
        raw, selection = _read_json(_project_file(path, root))
        if (hashlib.sha256(raw).hexdigest() != expected_sha256
                or set(selection) != {'version', 'status', 'created_utc', 'executable_freeze_sha256', 'cells'}
                or type(selection['version']) is not int or selection['version'] != 1
                or selection['status'] != 'FROZEN'
                or selection['executable_freeze_sha256'] != executable_sha256
                or type(selection['cells']) is not list):
            raise PhaseError('SELECTION_FREEZE')
        _utc(selection['created_utc'])
        expected_keys = _inventory(spec)
        actual_keys = [(c['source'], c['horizon'], c['window'], c['family']) for c in selection['cells']]
        if actual_keys != expected_keys:
            raise PhaseError('SELECTION_FREEZE')
        from conditional_study import select_parameter
        result = {}
        for cell, key in zip(selection['cells'], expected_keys):
            if set(cell) != {'source', 'horizon', 'window', 'family', 'status', 'parameter', 'validation_receipts'}:
                raise PhaseError('SELECTION_FREEZE')
            source_id, horizon, window, family = key
            cfg = _cell(spec, source_id, horizon, window, family, 'validation')
            refs = cell['validation_receipts']
            if type(refs) is not list or len(refs) != 1 or set(refs[0]) != {'path', 'sha256'}:
                raise PhaseError('SELECTION_FREEZE')
            ref = refs[0]
            if (type(ref['path']) is not str or Path(ref['path']).is_absolute()
                    or not _is_hash(ref['sha256'])):
                raise PhaseError('SELECTION_FREEZE')
            raw_receipt, receipt = _read_json(_project_file(ref['path'], root, scratch=True))
            if hashlib.sha256(raw_receipt).hexdigest() != ref['sha256']:
                raise PhaseError('SELECTION_FREEZE')
            if (type(receipt.get('version')) is not int or receipt.get('version') != 1
                    or receipt.get('phase') != 'validation'
                    or receipt.get('executable_freeze_sha256') != executable_sha256
                    or receipt.get('status') not in ('COMPLETE', 'INELIGIBLE', 'STOPPED')
                    or tuple(receipt.get(k) for k in ('source', 'horizon', 'window', 'family')) != key):
                raise PhaseError('SELECTION_FREEZE')
            identity = receipt.get('source_identity')
            if (type(identity) is not dict or identity.get('sha256') != cfg['sha256']
                    or identity.get('bytes') != cfg['bytes']
                    or identity.get('record_count') != cfg['record_count']
                    or identity.get('native_unit') != cfg['native_unit']):
                raise PhaseError('SELECTION_FREEZE')
            resources = receipt.get('resources')
            if (type(resources) is not dict
                    or type(resources.get('elapsed_seconds')) not in (int, float)
                    or not math.isfinite(resources['elapsed_seconds'])
                    or resources['elapsed_seconds'] <= 0
                    or type(resources.get('peak_rss_bytes')) is not int
                    or resources['peak_rss_bytes'] <= 0
                    or type(resources.get('maximum_observed_os_threads')) is not int
                    or resources['maximum_observed_os_threads'] < 1
                    or type(resources.get('thread_snapshot_count')) is not int
                    or resources['thread_snapshot_count'] < 1
                    or resources.get('thread_probe_status') != 'PASS'):
                raise PhaseError('SELECTION_FREEZE')
            if (receipt['status'] != 'STOPPED' and
                    (resources['elapsed_seconds'] >= 540
                     or resources['peak_rss_bytes'] >= 1610612736
                     or resources['maximum_observed_os_threads'] > 2)):
                raise PhaseError('SELECTION_FREEZE')
            rows = receipt['result']['candidate_rows']
            expected_origins = _origin_identity(range(cfg['validation_origin_first'],
                                                       cfg['validation_origin_last'] + 1))
            if receipt['result'].get('origin_identity') != expected_origins:
                raise PhaseError('SELECTION_FREEZE')
            candidates = _candidates(spec, cfg, window, family)
            if type(rows) is not list or [r['parameter'] for r in rows] != candidates:
                raise PhaseError('SELECTION_FREEZE')
            incomplete = any(r.get('status') == 'INCOMPLETE' for r in rows)
            if incomplete and (receipt['status'] != 'STOPPED' or not receipt.get('stop_code')):
                raise PhaseError('SELECTION_FREEZE')
            for row in rows:
                if row.get('status') in ('FAILED', 'INCOMPLETE') and row.get('mean_pinball') is not None:
                    raise PhaseError('SELECTION_FREEZE')
            chosen = select_parameter(rows, candidates, expected_count=(
                cfg['validation_origin_last'] - cfg['validation_origin_first'] + 1))
            if (cell['status'] != chosen['status'] or cell['parameter'] != chosen['parameter']
                    or (chosen['status'] == 'SELECTED' and receipt['status'] != 'COMPLETE')
                    or (chosen['status'] == 'INELIGIBLE' and receipt['status'] == 'COMPLETE')):
                raise PhaseError('SELECTION_FREEZE')
            result[key] = dict(cell)
        return result
    except (OSError, KeyError, TypeError, ValueError):
        raise PhaseError('SELECTION_FREEZE') from None


def _validate_source(source, cfg, source_id):
    import numpy as np
    if (source.source_id != source_id or source.sha256 != cfg['sha256']
            or source.bytes != cfg['bytes'] or source.position.ndim != 1
            or source.dates.ndim != 1 or len(source.position) != cfg['record_count']
            or source.dates.shape != source.position.shape
            or not np.isfinite(source.position).all()
            or not np.issubdtype(source.dates.dtype, np.datetime64)
            or np.isnat(source.dates).any() or np.any(np.diff(source.dates) <= np.timedelta64(0, 'us'))
            or source.metadata.get('units') != cfg['native_unit']
            or source.metadata.get('observation_count') != cfg['record_count']):
        raise PhaseError('SOURCE_IDENTITY')
    for label, index in (('evaluation_first_date', cfg['evaluation_origin_first']),
                         ('evaluation_last_date', cfg['evaluation_origin_last'])):
        if label in cfg and source.dates[index].astype('datetime64[D]') != np.datetime64(cfg[label], 'D'):
            raise PhaseError('SOURCE_DATES')


def _public_tree(value, depth=0):
    if depth > 12:
        raise ValueError('public nesting')
    if value is None or type(value) is bool:
        return value
    if type(value) in (int, float):
        if not math.isfinite(value):
            raise ValueError('public nonfinite')
        return value
    if type(value) is str:
        if '/Users/' in value or '@' in value or '\\' in value:
            raise ValueError('public private string')
        return value
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            raise ValueError('public key')
        return {key: _public_tree(item, depth + 1) for key, item in value.items()}
    if type(value) in (tuple, list):
        if any(type(item) is not dict for item in value):
            raise ValueError('public nonrow array')
        return [_public_tree(item, depth + 1) for item in value]
    raise ValueError('public unsupported value')


def public_json_bytes(value):
    return (json.dumps(_public_tree(value), indent=2, allow_nan=False) + '\n').encode()


def _failure(error):
    code = getattr(error, 'code', 'QUANTILE_FIT_FAILURE')
    if type(code) is not str or not _SAFE_CODE.fullmatch(code):
        code = 'QUANTILE_FIT_FAILURE'
    scalar = lambda d: {key: value for key, value in dict(d).items()
        if type(key) is str and re.fullmatch(r'[a-z_]{1,48}', key)
        and (type(value) in (int, float) and math.isfinite(value))}
    return dict(code=code, diagnostics=scalar(getattr(error, 'diagnostics', {})),
                context=scalar(getattr(error, 'failure_context', {})))


def _retain(private, prefix, forecast, peak):
    import numpy as np
    from conditional_study import score_predictions
    if len(forecast.origins) == 0:
        return
    scores = score_predictions(peak[forecast.origins], forecast.capacities,
                               forecast.floors, forecast.origins)
    for name, values in (('origins', forecast.origins), ('capacity', forecast.capacities),
                         ('peak', peak[forecast.origins]), ('floor', forecast.floors),
                         ('refit_indices', forecast.refit_indices), ('pinball', scores.pinball)):
        private[prefix + '_' + name] = np.array(values, copy=True)


def _summaries(public, method, parameter, source, forecast, peak, horizon, segment_first, phase):
    import numpy as np
    from conditional_study import nonoverlap_origins, score_predictions, summarize_scores
    scores = score_predictions(peak[forecast.origins], forecast.capacities,
                               forecast.floors, forecast.origins)
    metadata = dict(method=method, parameter=parameter)
    public['summary_rows'].append(metadata | summarize_scores(scores))
    if phase != 'validation':
        years = source.dates[forecast.origins].astype('datetime64[Y]').astype(int) + 1970
        for year in np.unique(years):
            mask = years == year
            part = score_predictions(peak[forecast.origins[mask]], forecast.capacities[mask],
                                     forecast.floors[mask], forecast.origins[mask])
            public['year_rows'].append(metadata | dict(year=int(year)) | summarize_scores(part))
        grid = nonoverlap_origins(segment_first, int(forecast.origins[-1]), horizon)
        mask = np.isin(forecast.origins, grid)
        part = score_predictions(peak[forecast.origins[mask]], forecast.capacities[mask],
                                 forecast.floors[mask], forecast.origins[mask])
        public['nonoverlap_rows'].append(metadata | summarize_scores(part))
    return scores


def execute_phase(source, spec, phase, source_id, H, W, family, selection=None, checkpoint=None):
    """Return public aggregate metadata and private numeric arrays; no file I/O.

    Quantile failures are candidate-level numerical failures. Other exceptions
    propagate unchanged, with best-known incomplete state attached when possible.
    No partial segment is ever summarized as a complete accuracy result.
    """
    import numpy as np
    import study_core as core
    from conditional_quantile import QuantileFitError
    import conditional_study as engine
    cfg = _cell(spec, source_id, H, W, family, phase)
    _validate_source(source, cfg, source_id)
    segment = 'validation' if phase == 'validation' else 'evaluation'
    first, last = cfg[segment + '_origin_first'], cfg[segment + '_origin_last']
    origins = np.arange(first, last + 1, dtype=np.int64)
    config = engine.StudyConfig(H, W, cfg['refit_step'], cfg['short_scale'],
                               cfg['long_scale'], cfg['nominal_gap_seconds'])
    public = dict(phase=phase, source=source_id, horizon=H, window=W, family=family,
        native_unit=cfg['native_unit'], status='INCOMPLETE', candidate_rows=[],
        summary_rows=[], year_rows=[], nonoverlap_rows=[], fit_diagnostics=[],
        selection=None, failure=None, origin_identity=_origin_identity(origins))
    private = {}
    cache = core.build_label_cache(source.position, H)

    def record(prefix, method, parameter, forecast):
        if not np.array_equal(forecast.origins, origins):
            raise PhaseError('INCOMPLETE_FORECAST')
        _retain(private, prefix, forecast, cache.peak)
        scores = _summaries(public, method, parameter, source, forecast, cache.peak,
                            H, first, phase)
        for row in forecast.fit_diagnostics:
            public['fit_diagnostics'].append(dict(method=method, parameter=parameter) | dict(row))
        return engine.summarize_scores(scores)

    if phase == 'validation':
        parameters = _candidates(spec, cfg, W, family)
        public['candidate_rows'] = [dict(parameter=p, status='INCOMPLETE',
            origin_count=0, mean_pinball=None, failure=None) for p in parameters]
    elif phase == 'evaluation':
        if type(selection) is not dict or selection.get('status') not in ('SELECTED', 'INELIGIBLE'):
            raise PhaseError('SELECTION_REQUIRED')
        if selection['status'] == 'INELIGIBLE':
            if selection.get('parameter') is not None:
                raise PhaseError('SELECTION_REQUIRED')
            public.update(status='INELIGIBLE', selection=dict(status='INELIGIBLE', parameter=None))
            return public, private
        if selection.get('parameter') not in _candidates(spec, cfg, W, family):
            raise PhaseError('SELECTION_REQUIRED')
        parameters = [selection['parameter']]
        public['selection'] = dict(status='SELECTED', parameter=selection['parameter'])
    else:
        parameters = []
    try:
        if phase == 'references':
            capacities = engine.historical_forecasts(source.position, origins, config,
                neighbor_count=cfg['one_state_reference_neighbors'][str(W)], checkpoint=checkpoint)
            for name, capacity in capacities.items():
                refits = (first + ((origins - first) // cfg['refit_step']) * cfg['refit_step']
                          if name.startswith('frozen_') else origins)
                forecast = engine.ConditionalForecast(origins, capacity,
                    np.abs(source.position[origins]), refits, (), name, None)
                record(name, name, None, forecast)
            public['status'] = 'COMPLETE'
        else:
            for index, parameter in enumerate(parameters):
                prefix = 'candidate_' + str(index) if phase == 'validation' else family
                try:
                    forecast = engine.conditional_forecast(source.position, source.dates,
                        origins, config, family, parameter, checkpoint=checkpoint)
                except QuantileFitError as error:
                    detail = _failure(error)
                    partial = getattr(error, 'partial_forecast', None)
                    if partial is not None:
                        _retain(private, prefix + '_partial', partial, cache.peak)
                        for row in partial.fit_diagnostics:
                            public['fit_diagnostics'].append(dict(method=family, parameter=parameter) | dict(row))
                    if phase == 'validation':
                        public['candidate_rows'][index].update(status='FAILED', failure=detail)
                        continue
                    public.update(status='FAILED', failure=detail)
                    return public, private
                metrics = record(prefix, family, parameter, forecast)
                if phase == 'validation':
                    public['candidate_rows'][index].update(status='COMPLETE',
                        origin_count=metrics['origin_count'], mean_pinball=metrics['mean_pinball'])
            if phase == 'validation':
                chosen = engine.select_parameter(public['candidate_rows'], parameters,
                                                   expected_count=len(origins))
                # Only scalar metadata enters the public selection object.
                public['selection'] = {k: v for k, v in chosen.items()
                                       if k != 'failed_candidates'}
                public['status'] = 'COMPLETE' if chosen['status'] == 'SELECTED' else 'INELIGIBLE'
            else:
                public['status'] = 'COMPLETE'
        public_json_bytes(public)
        return public, private
    except Exception as error:
        public['status'] = 'STOPPED'
        try:
            error.partial_phase_state = (public, private)
        except (AttributeError, TypeError):
            pass
        raise


def load_source(*args, **kwargs):
    """Lazy boundary so import/help and rejected freezes never load a source."""
    from conditional_sources import load_source as source_loader
    return source_loader(*args, **kwargs)


def _exclusive_write(path, data):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(data)


def _write_numeric(path, private):
    import numpy as np
    for key, values in private.items():
        if (not re.fullmatch(r'[A-Za-z0-9_]{1,64}', key) or not isinstance(values, np.ndarray)
                or values.ndim != 1 or values.dtype.kind not in 'biuf'
                or not np.isfinite(values).all()):
            raise PhaseError('PRIVATE_TRACE_INTEGRITY')
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(descriptor, 'wb') as stream:
        np.savez(stream, **private)


def _stop_code(error):
    value = getattr(error, 'code', getattr(error, 'reason', None))
    if type(value) is str and _SAFE_CODE.fullmatch(value):
        return value
    return 'STRUCTURAL_OR_NUMERIC'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('validation', 'evaluation', 'references'))
    parser.add_argument('--source', required=True, choices=('fx_hourly', 'nyfed_weekly'))
    parser.add_argument('--horizon', required=True, type=int)
    parser.add_argument('--window', required=True, type=int)
    parser.add_argument('--family', choices=('QR', 'KNN', 'SCALED_KNN'))
    parser.add_argument('--attempt-dir', required=True, type=Path)
    parser.add_argument('--freeze-sha256', required=True)
    parser.add_argument('--selection-freeze', type=Path)
    parser.add_argument('--selection-sha256')
    args = parser.parse_args(argv)
    if (args.phase == 'references') != (args.family is None):
        parser.error('--family is required only for conditional phases')
    if (args.phase == 'evaluation') != (args.selection_freeze is not None and args.selection_sha256 is not None):
        parser.error('evaluation requires --selection-freeze and --selection-sha256')
    if args.phase != 'evaluation' and (args.selection_freeze is not None or args.selection_sha256 is not None):
        parser.error('selection arguments apply only to evaluation')
    start, started_utc = time.monotonic(), utc_now()
    for name in THREAD_NAMES:
        os.environ[name] = '1'
    sys.dont_write_bytecode = True
    attempt = args.attempt_dir if args.attempt_dir.is_absolute() else ROOT / args.attempt_dir
    manifest = dict(version=1, status='STOPPED', phase=args.phase, source=args.source,
        horizon=args.horizon, window=args.window, family=args.family,
        executable_freeze_sha256=args.freeze_sha256 if _is_hash(args.freeze_sha256) else None,
        selection_freeze_sha256=args.selection_sha256 if _is_hash(args.selection_sha256) else None,
        started_utc=started_utc, ended_utc=None, source_identity=None,
        resources={}, result=None, stop_code=None, artifacts=[])
    public = private = guard = None
    traces = {}
    prior_alarm = None

    def disarm():
        if prior_alarm is not None:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, prior_alarm)

    try:
        if '..' in attempt.parts:
            raise PhaseError('OUTPUT_INTEGRITY')
        try:
            attempt.relative_to(ROOT / '.scratch')
        except ValueError:
            raise PhaseError('OUTPUT_INTEGRITY') from None
        public, private = create_attempt(attempt)
        _exclusive_write(public / 'attempt-start.json', public_json_bytes(dict(
            version=1, status='INCOMPLETE', terminal_receipt='UNVERIFIED_UNTIL_MANIFEST',
            started_utc=started_utc, phase=args.phase, source=args.source,
            horizon=args.horizon, window=args.window, family=args.family,
            executable_freeze_sha256=manifest['executable_freeze_sha256'])))
        guard = RunGuard(start, started_utc, attempt, public, private)
        prior_alarm = signal.getsignal(signal.SIGALRM)
        arm_hard_deadline()
        guard(stage='before_freeze')
        spec, _ = verify_executable_freeze(args.freeze_sha256)
        cfg = _cell(spec, args.source, args.horizon, args.window, args.family, args.phase)
        selected = None
        if args.phase == 'evaluation':
            cells = verify_selection_freeze(args.selection_freeze, args.selection_sha256,
                                            args.freeze_sha256, spec)
            selected = cells[(args.source, args.horizon, args.window, args.family)]
        guard(stage='before_source')
        source = load_source(_project_file(cfg['input_relative_path'], ROOT, scratch=True),
            args.source, expected_sha256=cfg['sha256'], expected_bytes=cfg['bytes'])
        _validate_source(source, cfg, args.source)
        manifest['source_identity'] = dict(sha256=source.sha256, bytes=source.bytes,
            record_count=len(source.position), native_unit=cfg['native_unit'],
            first_date=str(source.dates[0]), last_date=str(source.dates[-1]),
            irregular_gap_count=int(source.metadata['irregular_gap_count']))
        guard(stage='after_source')
        result, traces = execute_phase(source, spec, args.phase, args.source,
            args.horizon, args.window, args.family, selection=selected, checkpoint=guard)
        manifest['result'] = result
        manifest['status'] = result['status']
        guard.arrays(source.position, source.dates, traces)
        # A concurrent edit invalidates the attempt even if forecasting finished.
        verify_executable_freeze(args.freeze_sha256)
        guard(stage='before_output')
    except Exception as error:
        state = getattr(error, 'partial_phase_state', None)
        if state is not None:
            manifest['result'], traces = state
        manifest.update(status='STOPPED', stop_code=_stop_code(error))
    if public is None:
        disarm()
        print(json.dumps(dict(status='STOPPED', stop_code=manifest['stop_code'])))
        return 1
    try:
        if traces:
            _write_numeric(private / 'numeric-traces.npz', traces)
            raw = (private / 'numeric-traces.npz').read_bytes()
            manifest['artifacts'].append(dict(area='private', name='numeric-traces.npz',
                bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
        if guard is not None:
            if manifest['status'] != 'STOPPED':
                guard(stage='final_manifest_checkpoint')
            manifest['resources'] = dict(guard.resources)
        manifest['ended_utc'] = utc_now()
        _exclusive_write(public / 'manifest.json', public_json_bytes(manifest))
    except Exception as error:
        # Preserve an exclusive final failure receipt if final writing has not
        # already succeeded. Do not overwrite an existing terminal artifact.
        manifest.update(status='STOPPED', stop_code=_stop_code(error), ended_utc=utc_now())
        if guard is not None:
            manifest['resources'] = dict(guard.resources)
        try:
            _exclusive_write(public / 'manifest.json', public_json_bytes(manifest))
        except Exception:
            disarm()
            print(json.dumps(dict(status='STOPPED', stop_code='OUTPUT_INTEGRITY')))
            return 1
    disarm()
    print(json.dumps(dict(status=manifest['status'], stop_code=manifest['stop_code'])))
    return 0 if manifest['status'] in ('COMPLETE', 'INELIGIBLE') else 1


if __name__ == '__main__':
    raise SystemExit(main())
