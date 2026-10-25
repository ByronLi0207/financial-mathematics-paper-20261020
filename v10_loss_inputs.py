"""Frozen MCS input materialization from saved vectors; no acquisition or fit.

Only build_registry reads files, and only beneath its caller-supplied NEW root.
Core inputs must use the declared private-copy mapping. Returned arrays remain
private until the caller saves its sealed registry. Import performs no I/O.
"""
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import io
import json
import math
from pathlib import Path

import numpy as np
from v6_inference import pinball_losses
from v6_combinations import combine_reports


class InputError(ValueError):
    pass


def _identity(row, aliases):
    source = row.get('normalized_source') or aliases.get(row['source'], row['source'])
    return (row.get('period', 'original_evaluation'), source,
            int(row['horizon']), int(row['window']))


def _identity_dict(identity):
    return dict(zip(('period', 'normalized_source', 'horizon', 'window'), identity))


def _label(identity):
    period, source, _, _ = identity
    if source.startswith('cftc:'): return 'CFTC'
    if source == 'fx_hourly': return 'FX early2015' if period == 'early_2015' else 'FX original'
    if source == 'nyfed_weekly': return 'Treasury bills'
    if source == 'fx_daily': return 'Same-record dailyFX'
    return 'Other NYFed panels'


def _class(method_id, design):
    if method_id in design['matched_F_aliases']+design['matched_I_aliases']:
        return 'matched_historical'
    if method_id in design['other_historical_F_aliases']:
        return 'other_historical'
    if method_id in design['other_benchmark_aliases']:
        return 'other_benchmark'
    return 'conditional'


def _descriptor(method_id, row, design):
    return dict(method_id=method_id, method_class=_class(method_id, design),
                aliases=[method_id], provenance=dict(source_rows=[deepcopy(row)]))


def _safe(root, value, private=False):
    value = Path(value)
    if private and (value.is_absolute() or not value.parts or value.parts[0] != '.scratch'):
        raise InputError('CORE_COPY_MUST_BE_NEW_PRIVATE_SCRATCH')
    result = (root/value).resolve() if not value.is_absolute() else value.resolve()
    if not result.is_relative_to(root):
        raise InputError('INPUT_OUTSIDE_NEW_ROOT')
    return result


class _Snapshots:
    def __init__(self, root):
        self.root, self.cache = root, {}

    def npz(self, path, expected_bytes, expected_sha, keys, group):
        path = Path(path)
        if path not in self.cache:
            raw = path.read_bytes()
            if len(raw) != expected_bytes or hashlib.sha256(raw).hexdigest() != expected_sha:
                raise InputError('INPUT_BYTES_OR_SHA256_MISMATCH')
            self.cache[path] = dict(raw=raw, bytes=expected_bytes, sha256=expected_sha,
                                    arrays={}, groups=set())
        item = self.cache[path]
        if item['bytes'] != expected_bytes or item['sha256'] != expected_sha:
            raise InputError('CONFLICTING_INPUT_FINGERPRINTS')
        item['groups'].add(group)
        with np.load(io.BytesIO(item['raw']), allow_pickle=False) as archive:
            for key in keys:
                if key is not None and key not in item['arrays']:
                    if key not in archive.files:
                        raise InputError('MISSING_DECLARED_ARRAY:'+key)
                    value = np.array(archive[key], copy=True)
                    value.setflags(write=False)
                    item['arrays'][key] = value
        return item['arrays']

    def changed(self):
        failures = []
        for path, item in self.cache.items():
            try:
                raw = path.read_bytes()
                unchanged = len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256']
            except OSError:
                unchanged = False
            if not unchanged:
                failures.append((str(path), item['groups']))
        return failures


def _expected_n(identity, design):
    period, source, horizon, window = identity
    grid = design['grid']
    if source.startswith('cftc:'): key, period_key = 'cftc', 'cftc'
    elif source == 'fx_hourly': key, period_key = 'fx_hourly', 'fx_hourly'
    elif source == 'fx_daily': key, period_key = 'fx_daily', 'fx_daily'
    else: key, period_key = 'weekly', ('nyfed_weekly' if source == 'nyfed_weekly' else 'panel')
    config = grid[key]
    if ('horizons' in config and horizon not in config['horizons']) or ('windows' in config and window not in config['windows']):
        raise InputError('OUTSIDE_DECLARED_HORIZON_WINDOW_GRID')
    if 'periods' in design and period not in design['periods'][period_key]:
        raise InputError('OUTSIDE_DECLARED_PERIOD_GRID')
    return int(config['n_by_period'][period]) if key == 'fx_hourly' else int(config['n'])


def _vector(value, n, name, nonnegative=False):
    raw = np.asarray(value)
    if raw.shape != (n,) or raw.dtype.kind not in 'iuf':
        raise InputError('INVALID_ARRAY_SHAPE_OR_TYPE:'+name)
    vector = np.asarray(raw, dtype=float)
    if not np.isfinite(vector).all() or (nonnegative and np.any(vector < 0)):
        raise InputError('NONFINITE_OR_NEGATIVE_ARRAY:'+name)
    vector.setflags(write=False)
    return vector


def _materialize(row, identity, descriptor, location, snapshots, design, counters, public=False):
    n = _expected_n(identity, design)
    first, last = row['first_origin'], row['last_origin']
    if (type(row['origin_count']) is not int or row['origin_count'] != n
            or type(first) is not int or type(last) is not int or first < 0 or last-first+1 != n):
        raise InputError('DECLARED_FULL_GRID_MISMATCH')
    keys = dict(origin=row.get('origin_key', 'origins'), capacity=row.get('capacity_key', 'capacities'),
                target=row.get('target_key', 'peak'), floor=row.get('floor_key', 'floor'),
                loss=row.get('loss_key', 'pinball'))
    path, size, digest = location
    arrays = snapshots.npz(path, size, digest, keys.values(), identity)
    raw_origins = arrays[keys['origin']]
    expected = np.arange(first, last+1, dtype=np.int64)
    if raw_origins.dtype.kind not in 'iu' or raw_origins.shape != expected.shape or not np.array_equal(raw_origins, expected):
        raise InputError('EXACT_FULL_ORIGIN_GRID_MISMATCH')
    origins = np.asarray(raw_origins, dtype=np.int64)
    capacity = _vector(arrays[keys['capacity']], n, 'capacity')
    target = _vector(arrays[keys['target']], n, 'target')
    floor = None if keys['floor'] is None else _vector(arrays[keys['floor']], n, 'floor', True)
    if floor is not None and (np.any(capacity < floor) or np.any(target < floor)):
        raise InputError('PROVIDED_FLOOR_GEOMETRY')
    if keys['loss'] is None:
        loss = pinball_losses(target, capacity, tau=.95)
        loss_origin = 'derived_from_saved_capacity_target'
        counters['derived_loss_alias_rows'] += 1
    else:
        loss = _vector(arrays[keys['loss']], n, 'loss', True)
        loss_origin = 'stored_unchanged'
        counters['stored_loss_alias_rows'] += 1
    if loss.shape != (n,) or not np.isfinite(loss).all() or np.any(loss < 0):
        raise InputError('INVALID_FULL_LOSS')
    result = dict(descriptor, origins=origins, capacity=capacity, target=target,
                  floor=floor, loss=loss)
    result['provenance'] = dict(descriptor['provenance'], copied_trace_path=str(path),
        trace_bytes=size, trace_sha256=digest, keys=keys, loss_origin=loss_origin,
        original_trace_path=row['trace_path'], public_cftc=public)
    return result


def _same(left, right):
    if not all(np.array_equal(left[k], right[k]) for k in ('origins', 'capacity', 'target', 'loss')):
        return False
    a, b = left['floor'], right['floor']
    return (a is None and b is None) or (a is not None and b is not None and np.array_equal(a, b))


def _semantic_aliases(methods, design):
    methods = list(methods); discrepancies = []
    for canonical, allowlist in [('F', design['matched_F_aliases']), ('I', design['matched_I_aliases'])]:
        aliases = [m for m in methods if m['method_id'] in allowlist]
        if not aliases: continue
        aliases.sort(key=lambda m:m['method_id'])
        if not all(_same(aliases[0], item) for item in aliases[1:]):
            discrepancies.append(dict(canonical=canonical, aliases=[m['method_id'] for m in aliases],
                                      reason='FULL_ALIAS_VECTORS_DIFFER'))
            continue
        merged = dict(aliases[0], method_id=canonical,
                      aliases=sorted(m['method_id'] for m in aliases))
        merged['provenance'] = dict(alias_provenance=[m['provenance'] for m in aliases],
                                    semantic_rule='explicit matched aliases; exact origins/C/Y/loss/provided-floor')
        methods = [m for m in methods if m['method_id'] not in allowlist]+[merged]
    return sorted(methods, key=lambda m:m['method_id']), discrepancies


def _metadata(method):
    return {key:deepcopy(method[key]) for key in ('method_id', 'method_class', 'aliases', 'provenance')}


def build_registry(inventory, cftc_rows, design, root):
    """Load only verified NEW copies and materialize every fixed comparison.

    Known NA rows never open partial traces. Any invalid claimed-complete input
    leaves the whole comparison FAILED_INPUT, with full planned-method metadata.
    This function performs no model fit, parameter selection or MCS bootstrap.
    """
    root = Path(root).resolve()
    aliases = inventory.get('source_aliases', {})
    core = [r for r in inventory['methods'] if r.get('scope_classification') == design['core_scope']]
    cftc_rows = list(cftc_rows)
    combinations = inventory.get('reported_deterministic_combinations_not_derived', [])
    unavailable = inventory.get('unavailable_method_slots', [])
    counters = Counter(core_alias_rows=len(core), cftc_method_rows=len(cftc_rows),
        published_combination_complete_slots=sum(r['status']=='COMPLETE' for r in combinations),
        published_combination_unavailable_slots=sum(r['status']!='COMPLETE' for r in combinations),
        stored_loss_alias_rows=0, derived_loss_alias_rows=0,
        core_trace_files=len({r['trace_path'] for r in core}))
    groups = {}
    def group(identity):
        if identity not in groups:
            groups[identity] = dict(identity=_identity_dict(identity), group_label=_label(identity),
                status='READY', methods=[], planned_methods=[], unavailable_methods=[], errors=[],
                alias_discrepancies=[], claimed_complete_method_count=0)
        return groups[identity]
    mapping = {}
    for row in inventory['minimum_core_private_copy_manifest']:
        if row['path'] in mapping and mapping[row['path']] != row:
            raise InputError('DUPLICATE_COPY_MAPPING_CONFLICT')
        mapping[row['path']] = row
    snapshots = _Snapshots(root)
    raw_methods = defaultdict(dict)
    for row in [*core, *cftc_rows]:
        identity = _identity(row, aliases)
        g = group(identity)
        public = row.get('family') == 'CFTC' or identity[1].startswith('cftc:')
        method_id = row['family']+'::'+row['method']
        descriptor = _descriptor(method_id, row, design)
        g['planned_methods'].append(descriptor)
        g['claimed_complete_method_count'] += 1
        try:
            if method_id in raw_methods[identity]:
                raise InputError('DUPLICATE_METHOD_ID')
            if public:
                path = _safe(root, row['trace_path'])
                location = (path, row['trace_bytes'], row['trace_sha256'])
                if row['status'] != 'COMPLETE': raise InputError('CFTC_NOT_CLAIMED_COMPLETE')
            else:
                entry = mapping[row['trace_path']]
                path = _safe(root, entry['proposed_scratch_relative'], private=True)
                location = (path, entry['bytes'], entry['sha256'])
                if row['status'] != 'COMPLETE_SAVED_VECTOR': raise InputError('CORE_NOT_CLAIMED_COMPLETE')
            method = _materialize(row, identity, descriptor, location, snapshots, design, counters, public)
            raw_methods[identity][method_id] = method
            g['methods'].append(method)
        except Exception as exc:
            g['errors'].append(dict(method_id=method_id, reason=str(exc), exception_type=type(exc).__name__))
    for row in unavailable:
        identity = _identity(row, aliases)
        method_id = row['family']+'::'+row['method']
        group(identity)['unavailable_methods'].append(dict(_descriptor(method_id, row, design),
                                                         status=row['status'], reason=row.get('reason')))
    combo_settings = design.get('combinations', {})
    published = {}; combo_error = None
    if combinations:
        try:
            path = _safe(root, combo_settings['source'])
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != combo_settings['source_sha256']:
                raise InputError('PUBLISHED_COMBINATION_SOURCE_SHA256')
            report = json.loads(raw)
            for row in report['method_rows']:
                key = (*_identity(row, aliases), row['method'])
                if key in published: raise InputError('DUPLICATE_PUBLISHED_COMBINATION')
                published[key] = row
            expected_keys = [(*_identity(row, aliases), row['method']) for row in combinations]
            if len(set(expected_keys)) != len(expected_keys) or set(published) != set(expected_keys):
                raise InputError('PUBLISHED_COMBINATION_INVENTORY_MISMATCH')
            for inventory_row, key in zip(combinations, expected_keys):
                published_row = published[key]
                if (published_row['status'] != inventory_row['status']
                        or bool(published_row['original']) != bool(inventory_row['original'])):
                    raise InputError('PUBLISHED_COMBINATION_STATUS_OR_SCOPE')
            if path.read_bytes() != raw:
                raise InputError('PUBLISHED_COMBINATION_CHANGED_DURING_READ')
        except Exception as exc:
            combo_error = str(exc)
    recovered = {}
    for row in combinations:
        identity = _identity(row, aliases)
        g = group(identity)
        method_id = 'published_combination::'+row['method']
        descriptor = _descriptor(method_id, row, design)
        if row['status'] != 'COMPLETE':
            g['unavailable_methods'].append(dict(descriptor, status=row['status'], reason=row.get('reason')))
            continue
        g['planned_methods'].append(descriptor)
        g['claimed_complete_method_count'] += 1
        try:
            if combo_error: raise InputError(combo_error)
            old = published[(*identity, row['method'])]
            if old['status'] != 'COMPLETE' or bool(old['original']) != bool(row['original']):
                raise InputError('PUBLISHED_COMBINATION_STATUS_OR_SCOPE')
            original = bool(old['original'])
            F_id = 'original::frozen_F' if original else 'panel_legacy::frozen_F'
            QR_id = 'original::QR' if original else 'panel_legacy::QR33'
            KNN_id = 'original::KNN'
            F = raw_methods[identity][F_id]; QR = raw_methods[identity][QR_id]
            KNN = raw_methods[identity].get(KNN_id) if original else None
            constituents = [F, QR]+([KNN] if KNN is not None else [])
            if any(not np.array_equal(m['origins'], F['origins']) or not np.array_equal(m['target'], F['target'])
                   or m['floor'] is None or not np.array_equal(m['floor'], F['floor']) for m in constituents):
                raise InputError('COMBINATION_CONSTITUENT_ALIGNMENT')
            if identity not in recovered:
                recovered[identity] = combine_reports(F['origins'], F['floor'], F['capacity'], QR['capacity'],
                                                       None if KNN is None else KNN['capacity'])
            combo = recovered[identity][row['method']]
            if combo['status'] != 'COMPLETE': raise InputError('PUBLISHED_COMPLETE_COMBINATION_UNAVAILABLE')
            loss = pinball_losses(F['target'], combo['capacity'], tau=.95)
            actual_mean = math.fsum(map(float, loss))/len(loss)
            expected_mean = old['scores']['mean_loss']
            if not isinstance(expected_mean, (int,float)) or not math.isfinite(expected_mean) or not math.isclose(actual_mean, expected_mean, rel_tol=2e-14, abs_tol=1e-12):
                raise InputError('PUBLISHED_MEAN_LOSS_MISMATCH')
            method = dict(descriptor, origins=F['origins'], capacity=combo['capacity'],
                target=F['target'], floor=F['floor'], loss=loss)
            method['provenance'] = dict(descriptor['provenance'], published_source=combo_settings['source'],
                published_source_sha256=combo_settings['source_sha256'], published_row=deepcopy(old),
                constituent_methods=[F_id, QR_id]+([KNN_id] if row['method']=='MEDIAN_F_QR_KNN' else []),
                published_mean_verified=True, mean_absolute_tolerance=1e-12, mean_relative_tolerance=2e-14,
                loss_origin='derived_published_fixed_combination')
            g['methods'].append(method)
        except Exception as exc:
            g['errors'].append(dict(method_id=method_id, reason=str(exc), exception_type=type(exc).__name__))
    for path, identities in snapshots.changed():
        for identity in identities:
            group(identity)['errors'].append(dict(reason='INPUT_CHANGED_DURING_READ', trace_path=path))
    count_errors = []
    for field, observed in [('core_financial_trace_files', counters['core_trace_files']),
                            ('include_all_core_saved_alias_rows', len(core)),
                            ('new_cftc_method_cells', len(cftc_rows)),
                            ('total_expected_comparisons', len(groups)),
                            ('old_expected_comparisons', sum(not k[1].startswith('cftc:') for k in groups))]:
        if field in design and design[field] != observed:
            count_errors.append(dict(reason='EXPECTED_INVENTORY_COUNT_MISMATCH', field=field,
                                     expected=design[field], observed=observed))
    for key, observed in [('complete', counters['published_combination_complete_slots']),
                          ('unavailable', counters['published_combination_unavailable_slots'])]:
        if key in combo_settings and combo_settings[key] != observed:
            count_errors.append(dict(reason='PUBLISHED_COMBINATION_COUNT_MISMATCH', field=key,
                                     expected=combo_settings[key], observed=observed))
    output = []
    for identity in sorted(groups):
        g = groups[identity]
        methods = g['methods']
        if methods:
            reference = methods[0]
            for method in methods[1:]:
                if not np.array_equal(method['origins'], reference['origins']):
                    g['errors'].append(dict(reason='COMMON_ORIGIN_MISMATCH', method_id=method['method_id']))
                if not np.array_equal(method['target'], reference['target']):
                    g['errors'].append(dict(reason='COMMON_TARGET_MISMATCH', method_id=method['method_id']))
        if count_errors: g['errors'].extend(deepcopy(count_errors))
        if not methods and not g['errors']:
            g['errors'].append(dict(reason='NO_COMPLETE_METHOD'))
        if g['errors']:
            g['status'] = 'FAILED_INPUT'
            g['methods'] = sorted(methods, key=lambda m:m['method_id'])
        else:
            g['methods'], g['alias_discrepancies'] = _semantic_aliases(methods, design)
            g['planned_methods'] = [_metadata(m) for m in g['methods']]
        output.append(g)
    counts = dict(counters)
    counts.update(comparison_groups=len(output), ready_groups=sum(g['status']=='READY' for g in output),
        failed_input_groups=sum(g['status']=='FAILED_INPUT' for g in output),
        unavailable_methods=sum(len(g['unavailable_methods']) for g in output),
        methods_after_aliases=sum(len(g['methods']) for g in output if g['status']=='READY'),
        alias_discrepancy_groups=sum(bool(g['alias_discrepancies']) for g in output), errors=count_errors)
    return dict(groups=output, counts=counts)
