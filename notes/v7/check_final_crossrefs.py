"""S9 read-only compiled-label and protected-tree checks; no research imports."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    issues = []
    documents = {}
    for name, compiled in (
        ('manuscript', '.scratch/revision-v7/s9/compile-manuscript'),
        ('supplement', '.scratch/revision-v7/s8/compile-4-supplement'),
    ):
        tex = (ROOT / 'submission-jof' / (name + '.tex')).read_text()
        aux = (ROOT / compiled / (name + '.aux')).read_text()
        labels = re.findall(r'\\label\{([^}]+)\}', tex)
        refs = re.findall(r'\\(?:ref|pageref)\{([^}]+)\}', tex)
        compiled_labels = dict((k, (number, page)) for k, number, page in
            re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{([^}]+)\}', aux))
        missing = sorted((set(refs) | set(labels)) - compiled_labels.keys())
        duplicate = sorted(k for k in set(labels) if labels.count(k) > 1)
        if missing or duplicate:
            issues.append(dict(document=name, missing=missing, duplicate=duplicate))
        documents[name] = dict(labels=len(labels), reference_occurrences=len(refs),
                               compiled_mapping=compiled_labels,
                               unresolved=missing, duplicate_labels=duplicate)
    preservation = {}
    for label, commit in (
        ('v6', '29190137a1a0617b9d4f70cc28175ee14a57aba6'),
        ('supervisor', '0ebc6e54ee3682315670a641e8783fc15c3660f4'),
    ):
        paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit], cwd=ROOT).decode().splitlines()
        protected = [p for p in paths if p.startswith(('results/', 'data/', 'protocol/'))]
        changed = []
        missing = [p for p in paths if not (ROOT / p).exists()]
        for p in protected:
            old = subprocess.check_output(['git', 'show', commit + ':' + p], cwd=ROOT)
            if not (ROOT / p).exists() or hashlib.sha256(old).digest() != hashlib.sha256((ROOT / p).read_bytes()).digest():
                changed.append(p)
        preservation[label] = dict(source_commit=commit, original_paths=len(paths),
                                   missing_original_paths=missing,
                                   protected_files=len(protected), changed_protected_files=changed)
        if missing or changed:
            issues.append(dict(source=label, missing=missing, changed=changed))
    report = dict(status='PASS' if not issues else 'FAIL', documents=documents,
                  preservation=preservation, issues=issues, new_financial_calculations=0)
    (ROOT / 'notes/v7/s9-final-crossref-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], documents={k: {f: v[f] for f in
        ('labels', 'reference_occurrences', 'unresolved', 'duplicate_labels')} for k, v in documents.items()},
        preservation=preservation, issues=issues), indent=2))
    raise SystemExit(bool(issues))


if __name__ == '__main__':
    main()
