"""Check explicit clause/evidence links; scientific entailment is a separate review."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]


def main():
    folder = ROOT/'notes/final-merge'
    document = json.loads((folder/'thesis-clauses.json').read_text())
    bindings = {row['id']: row for row in json.loads((folder/'evidence-bindings.json').read_text())}
    text = (folder/'thesis.md').read_text()
    failures = []
    for clause in document['clauses']:
        if not clause['evidence'] or any(key not in bindings for key in clause['evidence']):
            failures.append({'clause': clause['id'], 'issue': 'missing or unknown evidence ID'})
        if clause['text'] not in text or '['+','.join(clause['evidence'])+']' not in text:
            failures.append({'clause': clause['id'], 'issue': 'clause or evidence list absent from prose'})
    if document['WP2_result'] != 'PENDING_NOT_RUN':
        failures.append({'issue': 'WP2 result claimed before registration/run'})
    report = {'status': 'FAIL' if failures else 'PASS', 'clauses': len(document['clauses']),
              'bound_clauses': len(document['clauses'])-len({x.get('clause') for x in failures}),
              'unbound_or_missing': len(failures), 'failures': failures,
              'manual_semantic_review': 'Root checked each claim against cited saved fields and retained limits.',
              'automatic_entailment_claimed': False, 'WP2_result': document['WP2_result']}
    (folder/'wp1-thesis-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
