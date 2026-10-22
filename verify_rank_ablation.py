"""Independent scalar arithmetic readback for a retained rank-ablation attempt.

No predictor, runner, production label cache, or production scorer is imported.
The only financial parser is conditional_sources.load_source, after exact source
byte identity has been checked. Agreement verifies arithmetic on the same source;
it supplies no independent financial evidence or uncertainty estimate.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
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
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SPEC = 'protocol/revision-20261022/rank-ablation-spec.json'
FREEZE = 'protocol/revision-20261022/rank-ablation-executable-freeze.json'
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
PRIVATE_KEYS = ('origins', 'peak', 'floor', 'I', 'F', 'refit_indices', 'I_pinball', 'F_pinball')
TABLE_KEYS = ('source', 'horizon', 'window', 'method')


class Checks:
    """Count every exact assertion and retain safe issue/field mismatch labels."""
    def __init__(self):
        self.count = 0
        self.errors = []

    def check(self, condition, label):
        self.count += 1
        if not condition:
            self.errors.append(label)
        return bool(condition)


def _integer(value, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError('INVALID_INTEGER')
    return value


def exact_ranks(window):
    window = _integer(window)
    low, high = (19*window+19)//20, (19*(window+1)+19)//20
    if high > window:
        raise ValueError('UNAVAILABLE_RANK')
    return low, high


def reconstruct_cell(position, origins, horizon, window, step):
    """Scalar source windows and Python sorted at every original refit.

    Only completed windows [i, i+H] for i=r-H-W+1,...,r-H enter
    the refit cache. Each query adds its own current absolute floor after
    ranking, preserving the mandated floating-operation order.
    """
    horizon, window, step = (_integer(v) for v in (horizon, window, step))
    low, high = exact_ranks(window)
    values = [float(x) for x in position]
    if not values or not all(math.isfinite(x) for x in values):
        raise ValueError('NONFINITE_SOURCE')
    ids = list(origins)
    if (not ids or any(type(t) is not int or t < 0 for t in ids)
            or any(b != a+1 for a, b in zip(ids, ids[1:]))
            or ids[0]-horizon-window+1 < 0 or ids[-1]+horizon >= len(values)):
        raise ValueError('ORIGIN_HISTORY_OR_TARGET')
    out = {key: [] for key in PRIVATE_KEYS}
    out['latest_label_ends'] = []
    out['I_overrun'] = []; out['F_overrun'] = []
    out['I_unused'] = []; out['F_unused'] = []
    out['I_strict_breach'] = []; out['F_strict_breach'] = []
    cache = {}; headroom_count = 0
    for t in ids:
        refit = ids[0]+((t-ids[0])//step)*step
        if refit not in cache:
            train = []
            first, last = refit-horizon-window+1, refit-horizon
            for i in range(first, last+1):
                peak = max(abs(values[j]) for j in range(i, i+horizon+1))
                train.append(peak-abs(values[i]))
            ranked = sorted(train)  # Retain duplicates; no interpolator/partition.
            cache[refit] = (ranked[low-1], ranked[high-1], last+horizon)
            headroom_count += len(train)
        g_i, g_f, latest = cache[refit]
        floor = abs(values[t])
        peak = max(abs(values[j]) for j in range(t, t+horizon+1))
        out['origins'].append(t); out['peak'].append(peak); out['floor'].append(floor)
        out['refit_indices'].append(refit); out['latest_label_ends'].append(latest)
        for method, headroom in (('I', g_i), ('F', g_f)):
            capacity = floor+headroom
            error = peak-capacity
            overrun, unused = max(error, 0.), max(-error, 0.)
            loss = .95*overrun+.05*unused
            if not all(math.isfinite(x) for x in (capacity, error, overrun, unused, loss)):
                raise ValueError('NONFINITE_ARITHMETIC')
            out[method].append(capacity); out[method+'_pinball'].append(loss)
            out[method+'_overrun'].append(overrun); out[method+'_unused'].append(unused)
            out[method+'_strict_breach'].append(error > 0.)
    out['refit_count'] = len(cache)
    out['source_window_headroom_count'] = headroom_count
    return out


def summarize(rows, method, selected):
    selected = list(selected)
    if method not in ('I', 'F') or not selected:
        raise ValueError('EMPTY_OR_INVALID_SUMMARY')
    n = len(selected)
    def mean_values(values):
        values = list(values)
        return values[0] if all(value == values[0] for value in values) else math.fsum(values)/n
    mean = lambda key: mean_values(rows[key][j] for j in selected)
    breaches = sum(rows[method+'_strict_breach'][j] for j in selected)
    conditional = math.fsum(rows[method+'_overrun'][j] for j in selected)/breaches if breaches else None
    return dict(origin_count=n, mean_pinball=mean(method+'_pinball'), mean_capacity=mean(method),
                mean_extra_allowance=mean_values(rows[method][j]-rows['floor'][j] for j in selected),
                strict_breach_count=breaches, strict_breach_rate=breaches/n,
                mean_positive_overrun=mean(method+'_overrun'), conditional_mean_overrun=conditional,
                conditional_overrun_denominator=breaches,
                conditional_overrun_undefined_reason=None if breaches else 'NO_STRICT_BREACHES',
                mean_unused_allowance=mean(method+'_unused'))


def read_private_npz(path):
    """Require one non-object numeric vector per declared key, no ZIP aliases."""
    import numpy as np
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if (len(names) != len(set(names))
                or set(names) != {key+'.npy' for key in PRIVATE_KEYS}):
            raise ValueError('NPZ_KEYS')
    with np.load(path, allow_pickle=False) as saved:
        result = {}
        for key in PRIVATE_KEYS:
            vector = saved[key]
            if vector.ndim != 1 or vector.dtype.kind not in ('i', 'u', 'f'):
                raise ValueError('NPZ_VECTOR')
            if key in ('origins', 'refit_indices') and vector.dtype.kind not in ('i', 'u'):
                raise ValueError('NPZ_INDEX_DTYPE')
            if not np.isfinite(vector).all():
                raise ValueError('NPZ_NONFINITE')
            result[key] = vector.tolist()
    return result


def compare_private(saved, expected, checks, cell):
    for key in PRIVATE_KEYS:
        got = saved[key]
        want = expected[key]
        if len(got) != len(want):
            checks.check(False, cell+':'+key+':LENGTH')
        for j in range(max(len(got), len(want))):
            checks.check(j < len(got) and j < len(want) and got[j] == want[j],
                         cell+':'+key+'['+str(j)+']')


def _csv_key(row, keys):
    return tuple(str(row[key]) for key in keys)


def _same_token(token, expected):
    if expected is None:
        return token == ''
    if type(expected) is int:
        try:
            return str(int(token)) == token and int(token) == expected
        except (TypeError, ValueError):
            return False
    if type(expected) is float:
        try:
            number = float(token)
            return math.isfinite(number) and number == expected
        except (TypeError, ValueError):
            return False
    return token == str(expected)


def compare_table(found, expected, keys, checks, name):
    expected_index = {_csv_key(row, keys): row for row in expected}
    index = {}
    for j, row in enumerate(found):
        try:
            key = _csv_key(row, keys)
        except KeyError:
            checks.check(False, name+':ROW_KEY:'+str(j)); continue
        if not checks.check(key not in index, name+':DUPLICATE_ROW:'+str(j)):
            continue
        index[key] = row
    checks.check(set(index) == set(expected_index), name+':ROW_INVENTORY')
    for key, want in expected_index.items():
        if key not in index:
            continue
        got = index[key]
        label = name+':'+':'.join(key)
        checks.check(set(got) == set(want), label+':FIELD_INVENTORY')
        for field, value in want.items():
            checks.check(field in got and _same_token(got[field], value), label+':'+field)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _regular(path):
    return path.is_file() and not any(p.is_symlink() for p in (path, *path.parents))


def _bound_path(root, name):
    if (type(name) is not str or not name or Path(name).is_absolute()
            or '..' in Path(name).parts):
        raise ValueError('UNSAFE_RELATIVE_PATH')
    path = root/name
    if not _regular(path):
        raise ValueError('NOT_REGULAR_FILE')
    return path


def _read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError('CSV_HEADER')
        result = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in result):
            raise ValueError('CSV_RECTANGULAR')
        return result


def _json(raw):
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('JSON_DUPLICATE_KEY')
            result[key] = value
        return result
    def invalid(_):
        raise ValueError('JSON_NONFINITE')
    return json.loads(raw, object_pairs_hook=object_pairs, parse_constant=invalid)


def _file_identity(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=_sha(raw))


def _parse_thread_snapshot(raw, pid):
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if lines and lines[0].split() == ['USER','PID','TT','%CPU','STAT','PRI','STIME','UTIME','COMMAND']:
        fields = [line.split() for line in lines[1:]]
        if not fields or any(len(row) < 10 or row[1] != str(pid) or row[-1] != str(pid) for row in fields):
            raise ValueError('THREAD_SNAPSHOT')
        return len(fields)
    if not lines or any(not line.isdecimal() or int(line) != pid for line in lines):
        raise ValueError('THREAD_SNAPSHOT')
    return len(lines)


def _threads():
    pid = os.getpid()
    command = (['ps', '-M', '-p', str(pid), '-o', 'pid='] if platform.system() == 'Darwin'
               else ['ps', '-L', '-p', str(pid), '-o', 'pid='])
    raw = subprocess.run(command, capture_output=True, text=True, check=True).stdout
    return _parse_thread_snapshot(raw, pid)


def _rss():
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if platform.system() == 'Darwin' else value*1024


def _reference_index(rows):
    result = {}
    for row in rows:
        key = _csv_key(row, TABLE_KEYS)
        if key in result:
            raise ValueError('DUPLICATE_ARCHIVED_ROW')
        result[key] = row
    return result


def verify_attempt(attempt, *, root=ROOT):
    """Read all eight cells and write a new aggregate-only retained receipt."""
    start = time.monotonic()
    begun = datetime.now(timezone.utc).isoformat()
    root = Path(root).absolute(); attempt = Path(attempt).absolute()
    if ('..' in attempt.parts or root/'.scratch' not in attempt.parents or not attempt.is_dir()
            or any(p.is_symlink() for p in (attempt, *attempt.parents))
            or not (attempt/'public').is_dir() or (attempt/'public').is_symlink()):
        raise ValueError('EXISTING_SCRATCH_ATTEMPT_REQUIRED')
    receipt = attempt/'public'/'independent-readback.json'
    # Claim the destination before any numerical work; an earlier receipt is immutable.
    with receipt.open('x', encoding='utf-8') as out:
        checks = Checks(); cell_receipts = []; input_hashes = []; snapshots = []
        counts = dict(verified_cells=0, verified_issues=0, checked_issued_reports=0,
                      scalar_source_windows=0, refit_count=0)
        for name in THREAD_ENV:
            os.environ[name] = '1'
        old_handler = signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('RESOURCE_WALL')))
        signal.alarm(600)
        try:
            audit_path = _bound_path(attempt, 'public/audit.json')
            audit_raw = audit_path.read_bytes(); audit = _json(audit_raw)
            input_hashes.append(dict(path='public/audit.json', **_file_identity(audit_path)))
            checks.check(audit.get('status') == 'COMPLETE', 'AUDIT_NOT_COMPLETE')
            checks.check(audit.get('accuracy_recomputed') == ['I', 'frozen_F'], 'AUDIT_METHODS')
            checks.check(audit.get('QR_refitted') is False, 'AUDIT_QR_REFITTED')
            checks.check(audit.get('independent_data_validation') is False, 'AUDIT_INDEPENDENT_DATA')
            freeze_path = _bound_path(root, FREEZE); freeze_raw = freeze_path.read_bytes(); freeze = _json(freeze_raw)
            checks.check(_sha(freeze_raw) == audit.get('executable_freeze_sha256'), 'EXECUTABLE_FREEZE_HASH')
            bound = set()
            for entry in freeze['files']:
                name = entry['path']
                checks.check(name not in bound, 'FREEZE_DUPLICATE_PATH'); bound.add(name)
                path = _bound_path(root, name)
                identity = _file_identity(path)
                checks.check(identity['bytes'] == entry['bytes'], 'FREEZE_SIZE:'+name)
                checks.check(identity['sha256'] == entry['sha256'], 'FREEZE_HASH:'+name)
            spec_path = _bound_path(root, SPEC); spec = _json(spec_path.read_bytes())
            checks.check(SPEC in bound, 'UNBOUND_RANK_SPEC')
            checks.check(spec.get('tau') == [19, 20], 'TAU_CONTRACT')
            original_path = _bound_path(root, spec['original_spec']); original_raw = original_path.read_bytes()
            checks.check(_sha(original_raw) == spec['original_spec_sha256'], 'ORIGINAL_SPEC_HASH')
            checks.check(spec['original_spec'] in bound, 'UNBOUND_ORIGINAL_SPEC')
            checks.check(spec['original_summary'] in bound, 'UNBOUND_ARCHIVE')
            original = _json(original_raw)
            archive_path = _bound_path(root, spec['original_summary']); archived = _reference_index(_read_csv(archive_path))
            input_hashes.extend([dict(path=FREEZE, **_file_identity(freeze_path)),
                                 dict(path=SPEC, **_file_identity(spec_path)),
                                 dict(path=spec['original_spec'], **_file_identity(original_path)),
                                 dict(path=spec['original_summary'], **_file_identity(archive_path))])
            expected_cells = {(source,h,w) for source,cfg in original['sources'].items()
                              for h in original['horizons'] for w in cfg['windows']}
            checks.check(len(expected_cells) == 8, 'EIGHT_CELL_CONTRACT')
            cells = {}
            for row in audit.get('cells', []):
                key = (row['source'], row['horizon'], row['window'])
                if checks.check(key not in cells, 'DUPLICATE_AUDIT_CELL'):
                    cells[key] = row
            checks.check(set(cells) == expected_cells, 'AUDIT_CELL_INVENTORY')
            checks.check(audit.get('completed_cells') == 8, 'AUDIT_COMPLETED_COUNT')
            wanted_private = {f'{source}-h{h}-w{w}.npz' for source,h,w in expected_cells}
            checks.check({p.name for p in (attempt/'private').iterdir()} == wanted_private, 'PRIVATE_FILE_INVENTORY')
            exports = audit.get('exports', [])
            csv_names = {'summary.csv', 'annual.csv', 'nonoverlap.csv', 'contrasts.csv'}
            checks.check(len(exports) == 4 and {row['path'] for row in exports} == csv_names, 'EXPORT_INVENTORY')
            checks.check({p.name for p in (attempt/'public').glob('*.csv')} == csv_names, 'PUBLIC_CSV_INVENTORY')
            for entry in exports:
                path = _bound_path(attempt/'public', entry['path']); identity = _file_identity(path)
                checks.check(identity['bytes'] == entry['bytes'], 'EXPORT_SIZE:'+entry['path'])
                checks.check(identity['sha256'] == entry['sha256'], 'EXPORT_HASH:'+entry['path'])
                input_hashes.append(dict(path='public/'+entry['path'], **identity))
            from conditional_sources import load_source
            summary_rows = []; annual_rows = []; sparse_rows = []; contrast_rows = []
            for source, cfg in original['sources'].items():
                source_path = _bound_path(root, cfg['input_relative_path'])
                series = load_source(source_path, source, expected_sha256=cfg['sha256'], expected_bytes=cfg['bytes'])
                checks.check(len(series.position) == cfg['record_count'], 'SOURCE_RECORD_COUNT:'+source)
                input_hashes.append(dict(source=source, bytes=series.bytes, sha256=series.sha256))
                position = series.position.tolist()
                ids = list(range(cfg['evaluation_origin_first'], cfg['evaluation_origin_last']+1))
                years = [str(series.dates[t])[:4] for t in ids]
                for horizon in original['horizons']:
                    for window in cfg['windows']:
                        key = (source,horizon,window); label = f'{source}-h{horizon}-w{window}'
                        before = len(checks.errors)
                        try:
                            rows = reconstruct_cell(position, ids, horizon, window, cfg['refit_step'])
                            counts['verified_cells'] += 1; counts['verified_issues'] += len(ids)
                            counts['checked_issued_reports'] += 2*len(ids)
                            counts['scalar_source_windows'] += rows['source_window_headroom_count']+len(ids)
                            counts['refit_count'] += rows['refit_count']
                            meta = dict(source=source, native_unit=cfg['native_unit'], horizon=horizon,
                                        window=window, refit_step=cfg['refit_step'])
                            audit_cell = cells.get(key, {})
                            low, high = exact_ranks(window)
                            for field,value in dict(**meta,origin_count=len(ids),rank_I=low,rank_F=high,
                                    both_empirical_minimizer_endpoints=(19*window)%20 == 0,
                                    changed_capacity_count=sum(a != b for a,b in zip(rows['I'],rows['F'])),
                                    reference_F_metrics_exact=True,private_file='private/'+label+'.npz').items():
                                checks.check(audit_cell.get(field) == value, label+':AUDIT:'+field)
                            private_path = _bound_path(attempt, 'private/'+label+'.npz')
                            identity = _file_identity(private_path)
                            checks.check(identity['sha256'] == audit_cell.get('private_sha256'), label+':PRIVATE_HASH')
                            input_hashes.append(dict(path='private/'+label+'.npz', **identity))
                            saved = read_private_npz(private_path); compare_private(saved, rows, checks, label)
                            for j,t in enumerate(ids):
                                checks.check(rows['latest_label_ends'][j] <= rows['refit_indices'][j] <= t,
                                             label+':MATURITY['+str(j)+']')
                                checks.check(rows['I'][j] <= rows['F'][j], label+':CAPACITY_MONOTONICITY['+str(j)+']')
                                checks.check(rows['I_overrun'][j] >= rows['F_overrun'][j], label+':OVERRUN_MONOTONICITY['+str(j)+']')
                                checks.check(rows['I_unused'][j] <= rows['F_unused'][j], label+':UNUSED_MONOTONICITY['+str(j)+']')
                                checks.check(not rows['F_strict_breach'][j] or rows['I_strict_breach'][j], label+':BREACH_MONOTONICITY['+str(j)+']')
                            metrics = {method:summarize(rows, method, range(len(ids))) for method in ('I','F')}
                            reference = archived[(source,str(horizon),str(window),'frozen_F')]
                            for field,value in metrics['F'].items():
                                checks.check(field in reference and _same_token(reference[field], value), label+':ARCHIVED_F:'+field)
                            qr = archived[(source,str(horizon),str(window),'QR')]
                            checks.check(audit_cell.get('imported_QR_summary') == qr, label+':IMPORTED_QR_ROW')
                            qmean = float(qr['mean_pinball'])
                            if not math.isfinite(qmean) or qmean < 0:
                                raise ValueError('INVALID_ARCHIVED_QR_MEAN')
                            for method in ('I','F'):
                                summary_rows.append(dict(**meta, method=method, **metrics[method]))
                                for year in sorted(set(years)):
                                    selected = [j for j,y in enumerate(years) if y == year]
                                    annual_rows.append(dict(**meta, method=method, issue_year=year,
                                                            **summarize(rows,method,selected)))
                                selected = list(range(0,len(ids),horizon+1))
                                sparse_rows.append(dict(**meta,method=method,**summarize(rows,method,selected)))
                            for name,left,right in [('QR-minus-I',qmean,metrics['I']['mean_pinball']),
                                                    ('I-minus-frozen_F',metrics['I']['mean_pinball'],metrics['F']['mean_pinball']),
                                                    ('QR-minus-frozen_F',qmean,metrics['F']['mean_pinball'])]:
                                direct = math.fsum(a-b for a,b in zip(rows['I_pinball'],rows['F_pinball']))/len(ids) if name=='I-minus-frozen_F' else None
                                contrast_rows.append(dict(**meta,contrast=name,origin_count=len(ids),mean_loss_left=left,
                                                          mean_loss_right=right,difference_of_means=left-right,
                                                          relative_mean_loss_difference_percent=100*((left-right)/right) if right else None,
                                                          undefined_reason=None if right else 'ZERO_REFERENCE_MEAN_LOSS',
                                                          direct_paired_difference=direct))
                            snapshots.append(_threads())
                            checks.check(snapshots[-1] <= 2, 'VERIFIER_OBSERVED_THREADS:'+label)
                            checks.check(_rss() <= 2147483648, 'VERIFIER_RSS:'+label)
                        except Exception as error:
                            checks.check(False, label+':'+type(error).__name__+':'+str(error)[:80])
                        cell_receipts.append(dict(source=source,horizon=horizon,window=window,
                                                  exact_agreement=len(checks.errors)==before))
            for name,rows,keys in [('summary.csv',summary_rows,TABLE_KEYS),('annual.csv',annual_rows,TABLE_KEYS+('issue_year',)),
                                   ('nonoverlap.csv',sparse_rows,TABLE_KEYS),('contrasts.csv',contrast_rows,('source','horizon','window','contrast'))]:
                found = _read_csv(_bound_path(attempt/'public',name))
                compare_table(found, rows, keys, checks, name)
                field = {'summary.csv':'summary_rows','annual.csv':'annual_rows','nonoverlap.csv':'nonoverlap_rows','contrasts.csv':'contrast_rows'}[name]
                checks.check(audit.get(field) == len(rows), 'AUDIT_'+field.upper())
            checks.check(counts['verified_cells'] == 8, 'FULL_CELL_RECONSTRUCTION')
            checks.check(audit.get('requested_numerical_threads') == 1, 'RUNNER_REQUESTED_THREADS')
            checks.check(type(audit.get('maximum_observed_os_threads')) is int and 1 <= audit['maximum_observed_os_threads'] <= 2, 'RUNNER_OBSERVED_THREADS')
            checks.check(type(audit.get('peak_rss_bytes')) is int and 0 < audit['peak_rss_bytes'] <= 2147483648, 'RUNNER_RSS')
            checks.check(type(audit.get('elapsed_seconds')) in (int,float) and 0 < audit['elapsed_seconds'] < 600, 'RUNNER_ELAPSED')
            checks.check(audit.get('thread_snapshot_count') == 9, 'RUNNER_THREAD_SNAPSHOT_COUNT')
            checks.check(audit.get('resources_are_snapshot_observations') is True, 'RUNNER_RESOURCE_SCOPE')
            # Re-read exact bound dependencies and source bytes after reconstruction.
            for entry in freeze['files']:
                identity = _file_identity(_bound_path(root,entry['path']))
                checks.check(identity == dict(bytes=entry['bytes'],sha256=entry['sha256']), 'POST_FREEZE_IDENTITY:'+entry['path'])
            for source,cfg in original['sources'].items():
                checks.check(_file_identity(_bound_path(root,cfg['input_relative_path'])) == dict(bytes=cfg['bytes'],sha256=cfg['sha256']), 'POST_SOURCE_IDENTITY:'+source)
            checks.check(audit_path.read_bytes() == audit_raw, 'AUDIT_CHANGED_DURING_READBACK')
        except Exception as error:
            checks.check(False, 'READBACK:'+type(error).__name__+':'+str(error)[:80])
        finally:
            signal.alarm(0); signal.signal(signal.SIGALRM,old_handler)
        try:
            snapshots.append(_threads())
        except Exception as error:
            checks.check(False, 'FINAL_THREAD_SNAPSHOT:'+type(error).__name__)
        elapsed = time.monotonic()-start; rss = _rss()
        checks.check(elapsed < 600, 'VERIFIER_WALL_LIMIT')
        checks.check(rss <= 2147483648, 'VERIFIER_RSS_LIMIT')
        checks.check(bool(snapshots) and max(snapshots) <= 2, 'VERIFIER_THREAD_LIMIT')
        result = dict(status='VERIFIED' if not checks.errors else 'FAILED', started_utc=begun,
                      finished_utc=datetime.now(timezone.utc).isoformat(), **counts,
                      full_check_count=checks.count, mismatch_count=len(checks.errors), errors=checks.errors,
                      cells=cell_receipts, input_hashes=input_hashes,
                      validation_scope='independent scalar arithmetic on unchanged accepted source bytes',
                      independent_financial_validation=False, QR_refitted=False, QR_originwise_traces_verified=False,
                      QR_summary_scope='unchanged archived aggregate rows and stored unrounded means only',
                      elapsed_seconds=elapsed, peak_rss_bytes=rss, requested_numerical_threads=1,
                      maximum_observed_os_threads=max(snapshots) if snapshots else None,
                      thread_snapshot_count=len(snapshots), resources_are_snapshot_observations=True)
        json.dump(result,out,indent=2,allow_nan=False); out.write('\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attempt', required=True)
    args = parser.parse_args()
    result = verify_attempt(args.attempt)
    print(json.dumps({key:result[key] for key in ('status','verified_cells','verified_issues','full_check_count',
                                                'mismatch_count','elapsed_seconds','peak_rss_bytes','maximum_observed_os_threads')}))
    return 0 if result['status'] == 'VERIFIED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
