"""Check inherited result/protocol blob preservation for the two fixed inputs."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
INPUTS = {'A': '60130eec7af2ebb38719b195dbe0e09fcb5796e7',
          'B': '80608070e4a6f4207483dc95770e6e5926172b19'}


def audit(root=ROOT):
    rows = []
    for label, ref in INPUTS.items():
        entries = subprocess.check_output(
            ['git', 'ls-tree', '-r', '-z', ref, 'results', 'protocol'], cwd=root)
        for entry in entries.split(b'\0'):
            if not entry:
                continue
            meta, name = entry.split(b'\t', 1)
            mode, kind, blob = meta.decode().split()
            if kind != 'blob':
                continue
            name = name.decode()
            path = root / name
            raw = path.read_bytes() if path.is_file() else None
            actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() if raw is not None else None
            rows.append({'line': label, 'ref': ref, 'path': name,
                         'expected_blob': blob, 'actual_blob': actual,
                         'byte_identical': actual == blob})
    failures = [row for row in rows if not row['byte_identical']]
    return {'status': 'MISMATCH' if failures else 'PASS',
            'original_result_protocol_files_checked': len(rows),
            'unique_paths': len({row['path'] for row in rows}),
            'mismatches': len(failures), 'failures': failures, 'rows': rows,
            'scope': 'Every inherited tracked result/protocol blob from each fixed line; no fit/statistic rerun.'}


if __name__ == '__main__':
    result = audit()
    (ROOT/'notes/final-merge/wp0-frozen-science-preservation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
