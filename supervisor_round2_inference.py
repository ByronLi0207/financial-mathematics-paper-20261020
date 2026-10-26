"""W3 post-result family reorganization using immutable verified p-values only.

No source data, forecasting model, HAC fit or original archive is changed.
Previously declared source primaries receive raw exploratory p-values and
Bonferroni across two. The other 71 original matched contrasts receive Holm.
"""
from __future__ import annotations

import os
import sys
sys.dont_write_bytecode = True
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
from inference_tests import holm

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT/'results/supervisor-20261023/inference'
INPUT_DM = ARCHIVE/'dm-verified.csv'
INPUT_TABLE = ARCHIVE/'tables3-4-ready.csv'
OUTPUT = ROOT/'results/supervisor-20261023/w3'
PRIMARY_IDS = frozenset(('fx_hourly-h6-QR2880-minus-rolling_F720',
                         'nyfed_weekly-h6-QR260-minus-frozen_F260'))
P_FIELDS = ('dm_p', 'double_dm_p', 'hln_p', 'double_hln_p')
HOLM_FIELDS = ('holm_p', 'double_holm_p', 'hln_holm_p', 'double_hln_holm_p')
BONF_FIELDS = ('primary_bonferroni_p', 'primary_double_bonferroni_p',
               'primary_hln_bonferroni_p', 'primary_double_hln_bonferroni_p')
OLD_ADJUSTMENT_FIELDS = ('holm_family_size', 'holm_input_p', 'holm_p',
                          'double_holm_p', 'hln_holm_p')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_rows(path):
    with Path(path).open(newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    with Path(path).open('x') as target:
        target.write(stream.getvalue())


def dump(path, value):
    with Path(path).open('x') as target:
        json.dump(value, target, indent=2, allow_nan=False)
        target.write('\n')


def partition(rows):
    ids = [r['contrast_id'] for r in rows]
    if len(rows) != 74 or len(set(ids)) != 74:
        raise ValueError('EXPECTED_74_UNIQUE_ARCHIVED_CONTRASTS')
    declared = {r['contrast_id'] for r in rows if r['primary'] == 'True'}
    if declared != PRIMARY_IDS:
        raise ValueError('DECLARED_SOURCE_PRIMARIES_CHANGED')
    original = [r for r in rows if r['category'] == 'common_history']
    primaries = [r for r in rows if r['contrast_id'] in PRIMARY_IDS]
    remaining = [r for r in original if r['contrast_id'] not in PRIMARY_IDS]
    outside = [r for r in rows if r not in primaries and r not in remaining]
    if (len(original) != 72 or len(primaries) != 2 or len(remaining) != 71
            or len(outside) != 1
            or {r['source'] for r in primaries} != {'fx_hourly', 'nyfed_weekly'}
            or sum(r['contrast_id'] in PRIMARY_IDS for r in original) != 1
            or outside[0]['legacy'] != 'True'):
        raise ValueError('FAMILY_MEMBERSHIP')
    return primaries, remaining, outside


def independent_holm(pvalues):
    """Direct closed formula, separate from the reused production helper."""
    p = list(map(float, pvalues))
    if not p or any(not math.isfinite(v) or not 0 <= v <= 1 for v in p):
        raise ValueError('FINITE_PROBABILITIES_REQUIRED')
    order = sorted(range(len(p)), key=lambda j: p[j])
    out = [0.]*len(p)
    for rank, index in enumerate(order):
        out[index] = min(1., max((len(p)-k)*p[order[k]] for k in range(rank+1)))
    return out


def probability(row, field):
    if row['status'] != 'OK':
        if row['status'] != 'IDENTICAL_LOSSES' or row[field] != '':
            raise ValueError('UNEXPECTED_UNAVAILABLE_TEST')
        return 1.
    value = float(row[field])
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('INVALID_ARCHIVED_PROBABILITY')
    return value


def p_display(value):
    return '<0.001' if value < .0005 else f'{value:.3f}'


def execute():
    protected = {str(p.relative_to(ROOT)): sha(p) for p in ARCHIVE.rglob('*') if p.is_file()}
    for name in ('inference_tests.py', 'supervisor_inference_audit.py'):
        protected[name] = sha(ROOT/name)
    original = read_rows(INPUT_DM)
    primaries, matched, outside = partition(original)
    transformed = {}
    for row in original:
        new = {k:v for k, v in row.items() if k not in OLD_ADJUSTMENT_FIELDS}
        new.update({'archived72_'+k:row[k] for k in OLD_ADJUSTMENT_FIELDS})
        new.update(family_reorganized_post_result=True, primary_p_exploratory=True,
                   family='', holm_family_size=None, holm_input_p=None,
                   holm_p=None, double_holm_p=None, hln_holm_p=None,
                   double_hln_holm_p=None, primary_bonferroni_p=None,
                   primary_double_bonferroni_p=None, primary_hln_bonferroni_p=None,
                   primary_double_hln_bonferroni_p=None, reported_p=None, reported_p_role='')
        transformed[row['contrast_id']] = new
    checks = []
    for field, adjusted_field in zip(P_FIELDS, HOLM_FIELDS):
        raw = [probability(r, field) for r in matched]
        adjusted = list(map(float, holm(raw)))
        oracle = independent_holm(raw)
        if any(abs(a-b) > 1e-15 for a,b in zip(adjusted, oracle)):
            raise ValueError('HOLM_INDEPENDENT_FORMULA_MISMATCH')
        order = sorted(range(len(raw)), key=lambda j:raw[j])
        if (any(adjusted[j] < raw[j] for j in order)
                or any(adjusted[a] > adjusted[b] for a,b in zip(order, order[1:]))):
            raise ValueError('HOLM_ORDER_OR_LOWER_BOUND')
        for row, value in zip(matched, adjusted):
            new = transformed[row['contrast_id']]
            new.update(family='remaining_matched_71', holm_family_size=71)
            new[adjusted_field] = value
            if field == 'dm_p':
                new.update(holm_input_p=probability(row, field), reported_p=value,
                           reported_p_role='Holm across remaining 71 matched contrasts')
        checks.append(dict(raw_field=field, adjusted_field=adjusted_field,
            family_count=71, independent_formula_max_absolute_error=max(abs(a-b) for a,b in zip(adjusted, oracle)),
            monotone_in_sorted_raw_p=True, adjusted_at_least_input=True))
    for row in primaries:
        if row['status'] != 'OK':
            raise ValueError('PRIMARY_RAW_TEST_UNAVAILABLE')
        new = transformed[row['contrast_id']]
        new.update(family='source_primaries_2', reported_p=float(row['dm_p']),
                   reported_p_role='primary, unadjusted', primary_bonferroni_family_size=2)
        for field, adjusted_field in zip(P_FIELDS, BONF_FIELDS):
            new[adjusted_field] = min(1., 2*probability(row, field))
    for row in outside:
        transformed[row['contrast_id']].update(family='legacy_outside_families',
            reported_p=float(row['dm_p']), reported_p_role='legacy, unadjusted')
    dm_rows = [transformed[r['contrast_id']] for r in original]
    for old, new in zip(original, dm_rows):
        if any(old[k] != new[k] for k in old if k not in OLD_ADJUSTMENT_FIELDS):
            raise ValueError('ARCHIVED_RAW_VALUE_CHANGED')
    table = read_rows(INPUT_TABLE)
    if len(table) != 48:
        raise ValueError('EXPECTED_48_ORIGINAL_TABLE_ROWS')
    matched_map = {(r['source'], r['horizon'], r['left_window'], r['left_method']):transformed[r['contrast_id']]
                   for r in original if r['category'] == 'common_history' and r['right_method'] == 'frozen_F'}
    for row in table:
        row['archived72_holm_p'] = row.pop('holm_p')
        row['archived72_holm_display'] = row.pop('holm_display')
        dm = matched_map.get((row['source'], row['horizon'], row['window'], row['method']))
        row.update(contrast_id=dm['contrast_id'] if dm else '',
                   family=dm['family'] if dm else 'outside_matched_families',
                   is_source_primary=dm['primary'] if dm else 'False',
                   holm_family_size=dm['holm_family_size'] if dm else None,
                   holm_p=dm['holm_p'] if dm else None,
                   holm_display=p_display(dm['holm_p']) if dm and dm['status']=='OK' and dm['holm_p'] is not None else '--',
                   reported_p=dm['reported_p'] if dm and dm['status']=='OK' else None,
                   reported_p_role=dm['reported_p_role'] if dm else 'outside matched families',
                   p_display=p_display(dm['reported_p']) if dm and dm['status']=='OK' else '--',
                   p_label='primary, unadjusted' if dm and dm['primary']=='True' else 'Holm (71)' if dm else '',
                   primary_bonferroni_p=dm['primary_bonferroni_p'] if dm else None,
                   family_reorganized_post_result=True)
    fixtures = [([.04,.002,.01,.03], [.06,.008,.03,.06]), ([.01,.01,1.], [.03,.03,1.])]
    for values, expected in fixtures:
        for actual in (independent_holm(values), list(map(float, holm(values)))):
            if any(abs(a-b)>1e-15 for a,b in zip(actual,expected)):
                raise ValueError('KNOWN_HOLM_FIXTURE')
    if any(sha(ROOT/p) != h for p,h in protected.items()):
        raise ValueError('IMMUTABLE_ARCHIVE_CHANGED')
    OUTPUT.mkdir(parents=True, exist_ok=False)
    write_csv(OUTPUT/'dm-family.csv', dm_rows)
    write_csv(OUTPUT/'tables3-4-ready.csv', table)
    dump(OUTPUT/'protected-input-identities.json', protected)
    summary = dict(status='PASS', generated_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
        family_reorganized_post_result=True,
        interpretation='Previously declared source primaries; raw p-values remain exploratory. The family reorganization is post-result and does not create a new preregistration or confirmatory error-control claim.',
        total_retained_contrasts=74, archived_matched_family_size=72,
        primary_family_size=2, remaining_matched_family_size=71, legacy_outside_family_size=1,
        primary_contrast_ids=[r['contrast_id'] for r in primaries],
        remaining_matched_contrast_ids=[r['contrast_id'] for r in matched],
        legacy_contrast_ids=[r['contrast_id'] for r in outside],
        source_primaries=[transformed[r['contrast_id']] for r in primaries],
        remaining_matched_identical_loss_cells=sum(r['status']=='IDENTICAL_LOSSES' for r in matched),
        identical_loss_policy='Preserve null raw statistics and p-values; use p=1 only for Holm bookkeeping; display dash in the report table.',
        table_rows=48, table_source_primary_rows=sum(r['is_source_primary']=='True' for r in table),
        FX_cross_window_primary_outside_matched_table=True,
        independent_checks=checks, known_holm_fixture_checks_passed=2,
        all_raw_archived_values_unchanged=True, protected_archive_files_unchanged=True,
        no_models_or_HAC_refitted=True,
        code_sha256={name:sha(ROOT/name) for name in ('supervisor_round2_inference.py','inference_tests.py','supervisor_inference_audit.py')},
        input_sha256={str(p.relative_to(ROOT)):sha(p) for p in (INPUT_DM, INPUT_TABLE)},
        output_sha256={name:sha(OUTPUT/name) for name in ('dm-family.csv','tables3-4-ready.csv','protected-input-identities.json')})
    dump(OUTPUT/'summary.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    if not args.run:
        parser.error('explicit --run is required')
    result = execute()
    print(json.dumps({k:result[k] for k in ('status','total_retained_contrasts','primary_family_size','remaining_matched_family_size','table_rows')}))
