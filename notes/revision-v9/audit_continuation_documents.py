"""Read-only document delta and saved-field audit against a public source cut.

No ancestry/deadline guard of a scientific driver is changed or invoked.
The baseline is an actually published commit, not a private design identity.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASELINE = '60e03b8ae7a950c96ace3987f0625b3e434e6887'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = ROOT / args.output
    assert not output.exists()

    def old(path):
        return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT, text=True)

    rows = []
    pattern = r'\\\[.*?\\\]|\\begin\{(?:equation|align)\*?\}.*?\\end\{(?:equation|align)\*?\}'
    for path in ('submission-jof/manuscript.tex', 'submission-jof/supplement.tex'):
        before, after = old(path), (ROOT / path).read_text()
        equations = re.findall(pattern, before, re.S)
        assert equations == re.findall(pattern, after, re.S)
        assert re.findall(r'\\begin\{table\}.*?\\end\{table\}', before, re.S) == re.findall(
            r'\\begin\{table\}.*?\\end\{table\}', after, re.S)
        rows.append(dict(path=path, old_display_equations=len(equations),
                         equations_unchanged=True, original_inline_tables_unchanged=True))
    path = 'submission-jof/extended-v9-technical.tex'
    assert old(path).encode() == (ROOT / path).read_bytes()
    assert old('submission-jof/supplement.tex').encode() == (ROOT / 'submission-jof/supplement.tex').read_bytes()
    for prefix in ('results/', 'protocol/'):
        assert not subprocess.check_output(['git', 'diff', '--name-only', BASELINE, '--', prefix], cwd=ROOT, text=True)
    path = 'submission-jof/generated/v9-evidence-tables.tex'
    assert old(path).encode() == (ROOT / path).read_bytes()

    binding_path = ROOT / 'notes/revision-v9/continuation-number-bindings.json'
    bindings = json.loads(binding_path.read_text())
    generated = (ROOT / bindings['generated_tex']).read_text()
    for item in bindings['bindings']:
        raw = (ROOT / item['source_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item['source_sha256']
        value = json.loads(raw)
        for part in item['JSON_pointer'].strip('/').split('/'):
            value = value[int(part)] if isinstance(value, list) else value[part]
        assert value == item['value'] and item['tex_token'] in generated

    spec = importlib.util.spec_from_file_location('prose_measure', ROOT / 'notes/revision-v8/writing_metrics.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    metrics = module.measure(ROOT / 'submission-jof/manuscript.tex')
    report = dict(actual_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  baseline_public_commit=BASELINE,
                  status='PASS' if metrics['all_v8_writing_gates_pass'] else 'WRITING_REPAIR_REQUIRED',
                  scope='Prose/display preservation and saved numeric-field readback; no statistical recomputation',
                  preservation=rows, original_extended_sections_byte_identical=True,
                  entire_protected_supplement_and_technical_source_identical=True,
                  result_and_protocol_diffs=[], original_generated_tables_identical=True,
                  new_numeric_bindings_checked=len(bindings['bindings']), new_models=0, new_statistical_tests=0,
                  new_binding_file='notes/revision-v9/continuation-number-bindings.json',
                  historical_audits=['notes/revision-v9/wp7-main-number-audit.json',
                                     'notes/revision-v9/wp7-supp-number-audit-after-fixture.json'], writing=metrics)
    with output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('writing', 'historical_audits')}, indent=2))
    print(json.dumps({key: metrics.get(key) for key in (
        'main_words', 'main_sentences', 'mean_sentence_words', 'negation_percent',
        'over35_percent', 'max_numbers_per_sentence', 'all_v8_writing_gates_pass')}))


if __name__ == '__main__':
    main()
