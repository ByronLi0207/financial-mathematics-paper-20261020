#!/usr/bin/env python3
"""Package existing code, protocols and aggregate evidence without running science.

The default is a read-only selection report. Pass --build only after the release
instructions have been finalized. All payload bytes are copied unchanged;
mixed aggregate/trace summaries are excluded as whole files, never rewritten.
Uses only the Python standard library and local Git objects; no network access.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import zipfile


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'submission-package/RELEASE'
WP2_COMMIT = '6192ec370d131c60d05e9fb103150e0e9db6aa23'
WP2_BASE = 'evidence/submission/final-jof/'
WP2_RESULTS = WP2_BASE + 'results/final-merge/wp2-cftc-mechanism/'
SUMMARY_NAMES = {'summary.json', 'summary.csv', 'contract-summary.csv',
                 'short-weekly-summary.json'}
# Inspected originals that mix aggregate rows with unit/fit details. Exclude
# the complete file, including Python-repr diagnostics embedded in old CSVs.
MIXED_DETAIL_FILES = {
    'results/revision-v8/wp4/summary.csv',
    'results/revision-v8/wp4/summary.json',
    'results/revision-v8/wp5/summary.csv',
    'results/revision-v8/wp5/summary.json',
    'results/v9/nonstationarity/audit/summary.json',
    'results/v13/tau-repair/consistency.json',
}
FORBIDDEN_PARTS = {'data', 'raw', 'raw-data', 'private', '.private', '.git',
                   '.scratch', 'scratch', '__pycache__', 'units', 'unit',
                   'traces', 'trace', 'inputs'}
ALLOWED_SUFFIXES = {'.py', '.txt', '.md', '.json', '.jsonl', '.csv', '.cff'}
TRACE_KEYS = {'fit_diagnostics', 'traces', 'trace', 'units', 'unit_records',
              'prediction_vectors', 'pointwise', 'pointwise_losses',
              'per_issue', 'per_origin', 'per_point'}
POINT_ARRAY_KEYS = {'y', 'y_true', 'y_pred', 'yhat', 'q', 'qhat', 'target',
                    'targets', 'forecast', 'forecasts', 'prediction',
                    'loss', 'losses', 'residuals', 'observations',
                    'positions', 'net_positions', 'timestamps',
                    'evaluation_origins', 'validation_origins'}
POINT_CSV_COLUMNS = {'origin_index', 'issue_index', 'observation_index',
                     'y', 'y_true', 'y_pred', 'yhat', 'qhat', 'prediction',
                     'forecast', 'loss', 'pointwise_loss', 'residual'}
DOCUMENTS = (
    'README.md', 'REPRODUCING.md', 'CITATION.cff',
    'notes/submission/historical-reproducing-v13.md',
    'notes/submission/zenodo-steps.md', 'notes/submission/PENDING.md',
    'notes/submission/prediction-register.json',
    'notes/submission/prediction-register.md',
    'notes/submission/import-audit.md',
    'notes/submission/wp2-import-audit.md',
    'notes/submission/baseline-single-thread.json',
    'notes/v13/independent-reproduction.md',
    'notes/v12/design-publication.jsonl',
    'notes/v13/design-publication.jsonl',
)
JUDGMENTS = (
    'results/supervisor-20261023/e5/prediction-assessment.json',
    'results/supervisor-20261023/r6/assessment.json',
    'results/supervisor-20261023/r6/verification.json',
    'results/v12/decomposition/predictions.json',
    'results/v12/tau/predictions.json',
    'results/v12/validation-length/predictions.json',
    'results/v13/tau-repair/consistency.json',
    'results/v9/legacy-calibrated/predictions.json',
    'results/v9/nonstationarity/postrun/predictions.json',
)
WP2_FILES = (
    'protocol/final-merge/wp2-cftc-mechanism.md',
    'protocol/final-merge/wp2-input-seal.json',
    'results/final-merge/wp2-cftc-mechanism/summary.json',
    'results/final-merge/wp2-cftc-mechanism/acceptance.json',
    'results/final-merge/wp2-cftc-mechanism/independent-verification.json',
    'results/final-merge/wp2-cftc-mechanism/verification-roundoff-detail.json',
    'results/final-merge/wp2-cftc-mechanism/completion.json',
    'results/final-merge/wp2-cftc-mechanism/start.json',
)
LIMITS = {
    'purpose': 'Existing scientific source, written protocols, aggregate inspection and saved judgments only.',
    'standalone_full_financial_reproduction': False,
    'standalone_full_historical_test_suite': False,
    'additional_requirements': [
        'Exact restricted FX observations and the original panel CSV, obtained separately under their source terms.',
        'Other original financial inputs and preserved historical Git objects required by the relevant replay/provenance gates.',
        'The omitted unit/fit traces and other historical fixtures required by some full-repository tests.',
    ],
    'project_software_license': 'NONE_SELECTED: no project LICENSE; no reuse permission or license is invented by this package.',
    'new_zenodo_doi': 'NONE_CREATED_OR_ASSIGNED',
    'third_party_rights': 'Source-data and publisher-template rights remain separate. Neither raw data nor publisher templates are included.',
    'no_financial_recalculation': True,
    'no_network_or_download': True,
    'pointwise_array_scope': 'Recursively inspect structured evidence, including JSON serialized inside CSV fields. Python source/test literals and written protocol grids are code/design metadata, not released observations or forecast vectors.',
    'wp2': 'Audited original summary, protocol and acceptance/verification metadata only. No unit files or 153 forecast traces are included. Trace-path/hash strings in the unchanged summary identify omitted provenance, not embedded trace payloads.',
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.run(['git', *args], cwd=ROOT, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def path_problem(name: str) -> str | None:
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        return 'Unsafe archive path'
    if set(p.parts) & FORBIDDEN_PARTS:
        return 'Raw/private/input/unit/trace/scratch subtree is excluded'
    if '.bak' in p.name.lower() or p.name.startswith('.'):
        return 'Backup or hidden file is excluded'
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        return 'Binary/archive/template/raw-array format is excluded'
    if p.name.lower().startswith(('license', 'copying')):
        return 'No project license may be selected by this builder'
    return None


def inspect_structured(name: str, raw: bytes, role: str) -> dict:
    """Reject evidence traces; retain scalar judgments/finite aggregate grids."""
    p = PurePosixPath(name)
    text = raw.decode('utf-8')
    problems, numeric_arrays = [], []
    containers = 0
    evidence = role in {'aggregate', 'judgment', 'wp2'} or name.endswith('prediction-register.json')

    def visit(value, pointer=''):
        nonlocal containers
        if isinstance(value, dict):
            containers += 1
            for key, item in value.items():
                loc = pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')
                lowered = str(key).lower()
                if evidence and lowered in TRACE_KEYS and isinstance(item, (list, dict)) and item:
                    problems.append({'pointer': loc, 'reason': 'Mixed unit/fit/pointwise trace container'})
                if evidence and lowered in POINT_ARRAY_KEYS and isinstance(item, list) and item:
                    problems.append({'pointer': loc, 'reason': 'Per-observation/forecast/loss array key'})
                visit(item, loc)
        elif isinstance(value, list):
            containers += 1
            if value and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value):
                numeric_arrays.append({'pointer': pointer, 'length': len(value)})
                if len(value) > 64:
                    problems.append({'pointer': pointer, 'reason': 'Long numeric vector requires separate author review', 'length': len(value)})
            for item in value:
                visit(item, pointer + '/*')
        elif isinstance(value, str) and value[:1] in ('{', '['):
            # Older summaries put nested diagnostics into CSV JSON strings.
            try:
                nested = json.loads(value)
            except (ValueError, TypeError):
                try:
                    nested = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    return
            visit(nested, pointer + '<embedded-json>')

    rows = None
    if p.suffix == '.json':
        visit(json.loads(text))
    elif p.suffix == '.jsonl':
        for number, line in enumerate(text.splitlines(), 1):
            if line.strip():
                visit(json.loads(line), f'/line-{number}')
    elif p.suffix == '.csv':
        csv.field_size_limit(32 * 1024 * 1024)
        reader = csv.DictReader(io.StringIO(text))
        columns = set(reader.fieldnames or [])
        if columns & POINT_CSV_COLUMNS:
            problems.append({'pointer': '/csv-columns', 'reason': 'Per-point CSV column',
                             'columns': sorted(columns & POINT_CSV_COLUMNS)})
        rows = list(reader)
        visit(rows)
    return {'status': 'EXCLUDE_MIXED_OR_POINTWISE' if problems else 'PASS',
            'recursive_containers_checked': containers, 'csv_rows': len(rows) if rows is not None else None,
            'numeric_arrays': numeric_arrays, 'problems': problems}


def select() -> tuple[dict, list, dict, dict]:
    if any(p.is_file() for pattern in ('LICENSE*', 'LICENCE*', 'COPYING*')
           for p in ROOT.glob(pattern)):
        raise ValueError('Project license state changed; author must reconcile the release instructions')
    tracked = {x.decode() for x in git('ls-files', '-z').split(b'\0') if x}
    candidates, excluded = {}, []

    def add(name: str, role: str):
        p = ROOT / name
        if not p.is_file() or p.is_symlink():
            raise ValueError(f'Required regular source file missing: {name}')
        if name in candidates:
            return
        candidates[name] = role

    for name in sorted(tracked):
        if '/' not in name and name.endswith('.py'):
            add(name, 'scientific_code_and_tests')
    for name in ('requirements.txt', 'requirements-paper.txt'):
        add(name, 'requirements')
    for p in sorted((ROOT / 'protocol').rglob('*')):
        if p.is_file():
            add(p.relative_to(ROOT).as_posix(), 'protocol')
    for name in DOCUMENTS:
        add(name, 'reproduction_and_register')
    for name in JUDGMENTS:
        add(name, 'judgment')
    for p in sorted((ROOT / 'results').rglob('*')):
        if p.is_file() and p.name in SUMMARY_NAMES:
            add(p.relative_to(ROOT).as_posix(), 'aggregate')
    for p in sorted((ROOT / 'results').rglob('README.md')):
        add(p.relative_to(ROOT).as_posix(), 'reproduction_notes')

    audit_path = ROOT / 'notes/submission/wp2-import-audit.json'
    audit = json.loads(audit_path.read_text())
    if not audit.get('import_allowed') or audit.get('source_commit') != WP2_COMMIT:
        raise ValueError('The local WP2 import audit does not authorize this source')
    wp2_checks = {}
    for original in WP2_FILES:
        name = WP2_BASE + original
        add(name, 'wp2')
        raw = (ROOT / name).read_bytes()
        original_raw = git('show', WP2_COMMIT + ':' + original)
        if raw != original_raw:
            raise ValueError(f'WP2 original-byte mismatch: {name}')
        wp2_checks[name] = sha(raw)

    selected, checks = {}, {}
    for name, role in sorted(candidates.items()):
        problem = path_problem(name)
        raw = (ROOT / name).read_bytes()
        if problem:
            excluded.append({'path': name, 'reason': problem, 'source_sha256': sha(raw)})
            continue
        if name in MIXED_DETAIL_FILES:
            excluded.append({'path': name,
                'reason': 'Inspected mixed aggregate and unit/fit detail file; whole original omitted, no scientific fields changed.',
                'source_sha256': sha(raw)})
            continue
        check = inspect_structured(name, raw, role)
        if check['status'] != 'PASS':
            excluded.append({'path': name, 'reason': 'Contains mixed trace or per-point evidence; whole original file omitted, no fields changed.',
                             'source_sha256': sha(raw), 'content_findings': check['problems']})
            continue
        selected[name] = {'raw': raw, 'role': role}
        checks[name] = check
    for name in (WP2_BASE + x for x in WP2_FILES):
        if name not in selected:
            raise ValueError(f'An explicitly required WP2 file failed inspection: {name}')
    # A saved judgment may itself bundle fit details (e.g. the solver examples).
    # Omit that original file whole; the unchanged aggregate summary and current
    # prediction register still retain its gate verdict and counts.
    for name in DOCUMENTS:
        if name not in selected:
            raise ValueError(f'A required instruction/judgment failed inspection: {name}')
    return selected, excluded, checks, {'audit_sha256': sha(audit_path.read_bytes()),
                                      'source_commit': WP2_COMMIT, 'original_bytes_verified': wp2_checks}


def put(path: Path, raw: bytes, stamp: str, backups: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == raw:
            return
        saved = path.with_name(path.name + '.bak.' + stamp)
        if saved.exists():
            raise FileExistsError(saved)
        saved.write_bytes(path.read_bytes())
        backups.append(saved.relative_to(ROOT).as_posix())
    path.write_bytes(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Write release only after explicit root authorization')
    args = parser.parse_args()
    selected, excluded, checks, wp2 = select()
    groups = Counter(item['role'] for item in selected.values())
    report = {'mode': 'BUILD' if args.build else 'READ_ONLY_SELECTION',
              'selected_files': len(selected), 'source_bytes': sum(len(x['raw']) for x in selected.values()),
              'categories': dict(sorted(groups.items())), 'excluded_candidates': excluded,
              'selected_paths': sorted(selected), 'limits': LIMITS}
    if not args.build:
        print(json.dumps(report, indent=2))
        return

    created = datetime.now(timezone.utc)
    stamp = created.strftime('%Y%m%dT%H%M%S%fZ')
    readme = ('''# Code, protocols and aggregate evidence release

This bounded archive copies existing scientific Python modules/tests, requirements,
written protocols, inspected aggregate summaries, saved judgments and reproduction
instructions. Original scientific payload bytes are unchanged. Read REPRODUCING.md
and notes/submission/prediction-register.md for evidence and interpretation limits.

This archive cannot independently run every financial comparison or the complete
historical test suite. Exact restricted FX observations, the original panel CSV,
other required financial inputs, historical Git objects and omitted unit/fit traces
must be obtained or retained separately under their original rights and provenance
conditions. No financial estimation, new test or source download is performed here.

Raw data, private pointwise predictions/losses, NumPy arrays, unit/fit traces,
original result ZIPs, backups, scratch files and publisher templates are omitted.
Some historical files named summary mix aggregate results with fit traces; these
are omitted whole, without changing scientific fields. release-manifest.json lists
the selected bytes, explicit exclusions and recursive structured-content checks.
WP2 contains only its audited protocol, aggregate summary and necessary judgments;
its trace-path/hash strings refer to omitted files, not embedded forecast vectors.

No project software LICENSE has been selected. This archive does not grant a new
license or choose one for the author. No new Zenodo DOI has been assigned or
created. Third-party source rights remain separate. CITATION.cff and the Zenodo
instructions retain author-only decisions. This is a local package, not a deposit,
publication or proof of independent financial reproduction.
''').encode()
    selected['RELEASE-README.md'] = {'raw': readme, 'role': 'generated_release_scope'}
    checks['RELEASE-README.md'] = inspect_structured('RELEASE-README.md', readme, 'generated_release_scope')
    files = {name: {'bytes': len(item['raw']), 'sha256': sha(item['raw']), 'role': item['role']}
             for name, item in sorted(selected.items())}
    manifest = {'schema': 'submission-code-aggregate-release-v1',
        'generated_utc': created.isoformat(), 'repository_head': git('rev-parse', 'HEAD').decode().strip(),
        'archive': 'code-and-aggregate-results.zip', 'payload_file_count': len(files),
        'archive_member_count_including_this_manifest': len(files) + 1,
        'manifest_self_hash_excluded': True, 'categories': dict(sorted(Counter(x['role'] for x in selected.values()).items())),
        'limits': LIMITS, 'source_files_unchanged': True, 'files': files,
        'selected_aggregate_files': [n for n, item in sorted(selected.items())
                                     if item['role'] == 'aggregate' or n == WP2_RESULTS + 'summary.json'],
        'selected_wp2_files': [n for n, item in sorted(selected.items()) if item['role'] == 'wp2'],
        'selected_judgment_files': [n for n, item in sorted(selected.items())
                                    if item['role'] == 'judgment'],
        'excluded_candidates': excluded, 'content_checks': checks,
        'wp2_import_validation': wp2,
        'global_exclusions': ['all raw/source data directories', '*.npz/*.npy and other binary arrays',
            'all original result ZIPs and unit/trace/input subtrees', 'private per-point losses/prediction vectors',
            'backups, scratch, private files and Git objects', 'publisher templates',
            'historical-readme-v13.md (not required for this release)']}
    manifest_raw = (json.dumps(manifest, indent=2) + '\n').encode()
    payload = {name: item['raw'] for name, item in selected.items()}
    payload['release-manifest.json'] = manifest_raw
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    archive_raw = memory.getvalue()
    # Read back every compressed member; inspect nested JSON/CSV once more.
    with zipfile.ZipFile(io.BytesIO(archive_raw)) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(payload):
            raise ValueError('Archive member/CRC mismatch')
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('Duplicate archive member')
        for name in archive.namelist():
            if path_problem(name) or archive.read(name) != payload[name]:
                raise ValueError(f'Archive byte/path mismatch: {name}')
            role = selected[name]['role'] if name in selected else 'manifest'
            if inspect_structured(name, archive.read(name), role)['status'] != 'PASS':
                raise ValueError(f'Archive recursive readback rejected: {name}')
    for name, item in selected.items():
        if item['role'] != 'generated_release_scope' and (ROOT / name).read_bytes() != item['raw']:
            raise ValueError(f'Source changed during build: {name}')
    backups = []
    put(OUT / 'code-and-aggregate-results.zip', archive_raw, stamp, backups)
    put(OUT / 'release-manifest.json', manifest_raw, stamp, backups)
    put(OUT / 'README.md', readme, stamp, backups)
    # Verify filesystem bytes after writing as well as the in-memory ZIP.
    if ((OUT / 'code-and-aggregate-results.zip').read_bytes() != archive_raw
            or (OUT / 'release-manifest.json').read_bytes() != manifest_raw):
        raise ValueError('Written release differs from verified memory bytes')
    receipt = {'schema': 'submission-code-release-readback-v1', 'status': 'PASS_CODE_PROTOCOL_AGGREGATE_ONLY',
        'generated_utc': datetime.now(timezone.utc).isoformat(), 'command': ['python3', '-B', 'notes/submission/build_code_release.py', '--build'],
        'builder_sha256': sha(Path(__file__).read_bytes()),
        'archive_path': str((OUT / 'code-and-aggregate-results.zip').relative_to(ROOT)),
        'archive_sha256': sha(archive_raw), 'archive_bytes': len(archive_raw),
        'manifest_path': str((OUT / 'release-manifest.json').relative_to(ROOT)), 'manifest_sha256': sha(manifest_raw),
        'archive_members': len(payload), 'payload_files': len(files),
        'all_member_bytes_crc_and_paths_verified': True,
        'all_structured_members_recursively_rechecked_after_zip_readback': True,
        'csv_embedded_json_checked': True, 'per_point_array_or_trace_findings_in_selected_payload': [],
        'excluded_candidate_count': len(excluded), 'excluded_candidates': excluded,
        'source_files_unchanged_during_build': True, 'wp2_original_bytes_verified': True,
        'backup_files_created': backups, 'limits': LIMITS,
        'operations_not_performed': ['financial calculation', 'scientific field modification', 'network/download',
            'test execution', 'license selection', 'DOI reservation/deposit', 'commit or publication']}
    put(OUT / 'release-check-receipt.json', (json.dumps(receipt, indent=2) + '\n').encode(), stamp, backups)
    print(json.dumps({key: receipt[key] for key in ('status', 'archive_path', 'archive_sha256',
        'archive_bytes', 'manifest_path', 'manifest_sha256', 'archive_members', 'payload_files',
        'excluded_candidate_count')}, indent=2))


if __name__ == '__main__':
    main()
