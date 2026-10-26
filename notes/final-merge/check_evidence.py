"""Verify declared legacy facts without recomputing scientific outcomes."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def pointer(document, path):
    for part in path.split('/')[1:]:
        key = part.replace('~1', '/').replace('~0', '~')
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def audit(bindings, root=ROOT):
    failures = []
    checked = []
    for row in bindings:
        path = root / row['source']
        raw = path.read_bytes()
        observed = pointer(json.loads(raw), row['pointer'])
        if observed != row['expected']:
            failures.append({'id': row['id'], 'expected': row['expected'], 'observed': observed})
        checked.append({'id': row['id'], 'observed': observed, 'source': row['source'],
                        'pointer': row['pointer'], 'sha256': hashlib.sha256(raw).hexdigest()})
    return {'status': 'PASS' if not failures else 'MISMATCH', 'checked': len(checked),
            'mismatches': len(failures), 'failures': failures, 'rows': checked,
            'scope': 'Exact legacy field bindings; no new fit, statistic or causal identification.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bindings', type=Path, default=ROOT/'notes/final-merge/evidence-bindings.json')
    parser.add_argument('--output', type=Path, default=ROOT/'notes/final-merge/wp0-evidence-check.json')
    args = parser.parse_args()
    result = audit(json.loads(args.bindings.read_text()))
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in ('status', 'checked', 'mismatches', 'failures')}))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
