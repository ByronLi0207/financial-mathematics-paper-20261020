"""Verify the bounded WP8 writing correction against its retained checkpoint.

This checks saved identities and declared evidence fields, not financial validity.
The prior local commit must exist; this does not manufacture public provenance.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '5f9a5cbe6ec8fe7229a0bed2a58b61ffe21e7e11'
ADDITION = ' The weekly comparisons retain both selection losses and a remaining gap within the tested menu, so hindsight selection alone need not recover historical performance.'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def audit():
    old = git('show', BASE + ':submission-final/manuscript.tex').decode()
    new = (ROOT/'submission-final/manuscript.tex').read_text()
    assert new == old.replace('while all planned comparisons remain plotted.}', 'while all planned comparisons remain plotted.' + ADDITION + '}')
    assert re.findall(r'\d+(?:\.\d+)?', new) == re.findall(r'\d+(?:\.\d+)?', old)
    assert re.findall(r'\\(?:label|ref|cite|href)\{[^}]+\}', new) == re.findall(r'\\(?:label|ref|cite|href)\{[^}]+\}', old)
    checked = 0
    for raw in git('ls-tree', '-r', '-z', BASE, '--', 'results', 'protocol').split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        assert kind == 'blob'
        data = (ROOT/name.decode()).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid, name.decode()
        checked += 1
    ledger = json.loads((ROOT/'notes/final-merge/evidence-bindings.json').read_text())
    for item in ledger:
        value = json.loads((ROOT/item['source']).read_text())
        for token in item['pointer'].split('/')[1:]:
            token = token.replace('~1','/').replace('~0','~')
            value = value[int(token)] if isinstance(value,list) else value[token]
        assert value == item['expected'] and type(value) is type(item['expected']), item['id']
    original = git('show', BASE + ':notes/final-merge/thesis.md')
    thesis = (ROOT/'notes/final-merge/thesis.md').read_bytes()
    assert thesis.endswith(original)
    clauses = json.loads((ROOT/'notes/final-merge/thesis-clauses.json').read_text())['clauses']
    for clause in clauses:
        assert clause['text'] in thesis.decode() and '['+','.join(clause['evidence'])+']' in thesis.decode()
    for i in range(60,75):
        assert f'E{i:03d}' in thesis.decode()
    legends = (ROOT/'submission-final/figure-legends.tex').read_text()
    assert ADDITION.strip() in legends
    return {'status':'PASS', 'actual_utc':datetime.now(timezone.utc).isoformat(),
            'comparison_commit':BASE, 'main_delta':'One evidence-bound conclusion sentence in Figure2caption only',
            'all_original_main_numeric_tokens_exact':True,
            'all_original_main_label_reference_citation_link_tokens_exact':True,
            'current_evidence_fields_checked':len(ledger), 'evidence_mismatch_count':0,
            'historical_result_protocol_paths_exact':checked,
            'historical_wp1_thesis_exact_suffix_retained':True,
            'historical_wp1_clauses_checked':len(clauses), 'new_current_C9_evidence_ids_checked':15,
            'separate_figure_legend_synced':True, 'new_result_or_protocol_computations':0,
            'scope':'Exact saved-source and bounded current-document checks. Earlier scientific/reference/rights results retain their own evidence and limitations; original local commit availability is an explicit requirement, not fresh-public-clone provenance proof.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
