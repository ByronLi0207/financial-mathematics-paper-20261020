"""Synthetic-only location/source tests for the additive v9 number guard."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r'[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?')
WORDS = re.compile(r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|hundred|thousand)\b', re.I)


def checker():
    spec = importlib.util.spec_from_file_location('v9_number_guard', ROOT / 'notes/revision-v9/check_main_numbers.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_report(text):
    inventory, words, failures = [], [], []
    for m in TOKEN.finditer(text):
        item = dict(file='main', line=text.count('\n', 0, m.start()) + 1,
                    column=m.start() - text.rfind('\n', 0, m.start()), token=m.group(),
                    category='unclassified', context=text[max(0, m.start()-100):m.end()+120])
        inventory.append(item)
        failures.append(dict(category='UNBOUND_NUMERIC_OCCURRENCE', **{k:v for k,v in item.items() if k != 'category'}))
    for m in WORDS.finditer(text):
        item = dict(file='main', line=text.count('\n', 0, m.start()) + 1, word=m.group(),
                    context=text[max(0, m.start()-70):m.end()+120])
        words.append(item)
        failures.append(dict(category='UNBOUND_NUMBER_WORD', **item))
    return dict(status='FAIL', inventory=inventory, number_words=words, failures=failures,
                unclassified_numeric_occurrences=len(inventory), unbound_number_word_occurrences=len(words),
                figure_paths=[], figure_values_verified_here=False, full_artifact_numeric_acceptance=False)


def source(tmp_path, value):
    path = tmp_path / 'source.json'
    path.write_text(json.dumps(value))
    return dict(source='source.json', source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def binding(tmp_path, context, literal, raw, operation, *, kind='digit', offset=None):
    fields = source(tmp_path, {'value':raw})
    return dict(schema='v9-main-context-bindings-1', contexts=[dict(id='claim', file='main', text=context,
        bindings=[dict(kind=kind, offset=context.index(literal) if offset is None else offset,
                       literal=literal, pointer='/value', raw_value=raw,
                       display_operation=operation, **fields)])], figures=[])


def resolve(tmp_path, text, spec, report=None):
    return checker().resolve_additions(report or synthetic_report(text), {'main':text, 'cover_letter':''}, spec, root=tmp_path)


def categories(report):
    return {r['category'] for r in report['failures']}


def test_exact_source_and_unique_context_resolve_only_named_location(tmp_path):
    context = 'The diagnostic cutpoint is 106.5.'
    text = context + '\nAn unrelated value is 106.5.'
    spec = binding(tmp_path, context, '106.5', 106.49618468616566, {'type':'format', 'spec':'.4g'})
    report = resolve(tmp_path, text, spec)
    assert report['unclassified_numeric_occurrences'] == 1
    assert report['failures'][0]['line'] == 2
    assert report['inventory'][0]['category'] == 'v9_located_source_binding'
    assert report['inventory'][1]['category'] == 'unclassified'


@pytest.mark.parametrize('failure', ['MISSING_CONTEXT', 'PRESERVED_MATH_MISMATCH',
    'PRESERVED_TABLE_NUMERIC_VECTOR_MISMATCH', 'ORIGINAL_SOURCE_HASH_MISMATCH',
    'PERCENTAGE_DISPLAY_MISMATCH', 'NEW_CONTEXT_VALUE_MISMATCH'])
def test_legacy_non_unbound_failures_survive(tmp_path, failure):
    text = 'The diagnostic cutpoint is 106.5.'
    spec = binding(tmp_path, text, '106.5', 106.49618468616566, {'type':'format', 'spec':'.4g'})
    old = synthetic_report(text)
    old['failures'].append(dict(category=failure, marker='must survive'))
    report = resolve(tmp_path, text, spec, old)
    assert any(r.get('marker') == 'must survive' for r in report['failures'])
    assert report['status'] == 'FAIL'


def test_source_hash_and_native_value_are_both_required(tmp_path):
    text = 'The count is 47 observations.'
    spec = binding(tmp_path, text, '47', 47, {'type':'exact'})
    (tmp_path / 'source.json').write_text('{"value":48}')
    report = resolve(tmp_path, text, spec)
    assert 'V9_SOURCE_HASH_MISMATCH' in categories(report)
    assert report['unclassified_numeric_occurrences'] == 1


def test_wrong_native_value_fails_with_matching_hash(tmp_path):
    text = 'The count is 47 observations.'
    spec = binding(tmp_path, text, '47', 47, {'type':'exact'})
    spec['contexts'][0]['bindings'][0]['raw_value'] = 48
    assert 'V9_SOURCE_VALUE_MISMATCH' in categories(resolve(tmp_path, text, spec))


@pytest.mark.parametrize('text', ['The count is 48 observations.', 'The count is 47 observations. The count is 47 observations.'])
def test_missing_or_duplicate_context_never_resolves(tmp_path, text):
    spec = binding(tmp_path, 'The count is 47 observations.', '47', 47, {'type':'exact'})
    report = resolve(tmp_path, text, spec)
    assert 'V9_CONTEXT_NOT_UNIQUE' in categories(report)
    assert report['unclassified_numeric_occurrences'] >= 1


def test_unlisted_digit_in_verified_context_still_fails(tmp_path):
    text = 'The count is 47 and probability 0.123.'
    spec = binding(tmp_path, text, '47', 47, {'type':'exact'})
    report = resolve(tmp_path, text, spec)
    assert report['unclassified_numeric_occurrences'] == 1
    assert any(r.get('token') == '0.123' for r in report['failures'])


def test_incorrect_offset_is_not_repaired_by_value_search(tmp_path):
    text = 'The count is 47 observations.'
    spec = binding(tmp_path, text, '47', 47, {'type':'exact'}, offset=0)
    report = resolve(tmp_path, text, spec)
    assert 'V9_LITERAL_OFFSET_MISMATCH' in categories(report)
    assert report['unclassified_numeric_occurrences'] == 1


def test_source_bound_number_word_and_fraction(tmp_path):
    text = 'Exactly three predictions agree.'
    spec = binding(tmp_path, text, 'three', ['consistent','left','consistent','consistent'],
                   {'type':'count_eq','equals':'consistent','as':'word'}, kind='word')
    report = resolve(tmp_path, text, spec)
    assert report['status'] == 'PASS'
    assert report['unbound_number_word_occurrences'] == 0
    assert report['number_words'][0]['column'] == 9
    text = 'The count is 47/48 cases.'
    spec = binding(tmp_path, text, '47/48', [47,48], {'type':'fraction'}, kind='numeric_fragment')
    report = resolve(tmp_path, text, spec)
    assert report['status'] == 'PASS'
    assert report['v9_resolved_numeric_occurrences'] == 2


def test_word_resolution_does_not_cover_same_word_elsewhere(tmp_path):
    context = 'Exactly three predictions agree.'
    text = context + '\nExactly three observations remain.'
    spec = binding(tmp_path, context, 'three', 3, {'type':'exact','as':'word'}, kind='word')
    report = resolve(tmp_path, text, spec)
    assert report['unbound_number_word_occurrences'] == 1
    assert report['failures'][0]['line'] == 2


def test_source_text_definition_requires_exact_whole_fragment(tmp_path):
    text = r'The diagnostic is $c=W/(H+1)$.'
    spec = binding(tmp_path, text, 'W/(H+1)', 'W/(H+1)', {'type':'exact'}, kind='numeric_fragment')
    report = resolve(tmp_path, text, spec)
    assert report['status'] == 'PASS'
    spec['contexts'][0]['bindings'][0]['literal'] = '1'
    spec['contexts'][0]['bindings'][0]['offset'] = text.index('1')
    assert 'V9_DISPLAY_MISMATCH' in categories(resolve(tmp_path, text, spec))


def test_no_claim_that_external_gates_passed(tmp_path):
    text = 'The count is 47 observations.'
    spec = binding(tmp_path, text, '47', 47, {'type':'exact'})
    report = resolve(tmp_path, text, spec)
    assert report['status'] == 'PASS'
    assert report['figure_values_verified_here'] is False
    assert report['full_artifact_numeric_acceptance'] is False


def test_path_traversal_is_refused(tmp_path):
    text = 'The count is 47 observations.'
    spec = binding(tmp_path, text, '47', 47, {'type':'exact'})
    spec['contexts'][0]['bindings'][0]['source'] = '../source.json'
    assert 'V9_BINDING_INVALID' in categories(resolve(tmp_path, text, spec))


def figure_fixture(tmp_path):
    src = tmp_path / 'results/render-v5/picture.pdf'
    dst = tmp_path / 'submission-jof/figures/picture.pdf'
    src.parent.mkdir(parents=True)
    dst.parent.mkdir(parents=True)
    src.write_bytes(b'%PDF-synthetic')
    dst.write_bytes(src.read_bytes())
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    records = {
        'placement': {'assets':[{'source':'results/render-v5/picture.pdf','target':'submission-jof/figures/picture.pdf','sha256':digest}]},
        'point_audit': {'status':'PASS','difference_count':0,'mismatch_count':0,'render_directory':'results/render-v5','output_sha256':{'picture.pdf':digest}},
        'visual_receipt': {'status':'PASS_FINAL_PDF_RENDER_AND_PNG','chosen_directory':'results/render-v5','actual_raster_observed':True,'render_returncode':0},
    }
    figure = dict(path='submission-jof/figures/picture.pdf', source='results/render-v5/picture.pdf', sha256=digest)
    for key, data in records.items():
        path = tmp_path / (key + '.json')
        path.write_text(json.dumps(data))
        figure[key] = dict(source=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return figure


def test_new_figure_needs_identity_machine_audit_and_visual_receipt(tmp_path):
    figure = figure_fixture(tmp_path)
    old = synthetic_report('')
    old['failures'].append({'category':'UNBOUND_OR_CHANGED_FIGURE_SOURCE','path':figure['path']})
    old['figure_paths'].append({'path':figure['path'],'current_sha256':figure['sha256'],'expected_receipt_sha256':None,'copy_identity_verified':False,'values_verified_here':False})
    spec = dict(schema='v9-main-context-bindings-1',contexts=[],figures=[figure])
    report = resolve(tmp_path, '', spec, old)
    assert report['status'] == 'PASS'
    assert report['figure_paths'][0]['copy_identity_verified'] is True
    assert report['figure_values_verified_here'] is False
    assert report['figure_paths'][0]['values_verified_here'] is False


def test_changed_figure_receipt_does_not_resolve(tmp_path):
    figure = figure_fixture(tmp_path)
    (tmp_path / 'visual_receipt.json').write_text('{}')
    old = synthetic_report('')
    old['failures'].append({'category':'UNBOUND_OR_CHANGED_FIGURE_SOURCE','path':figure['path']})
    report = resolve(tmp_path, '', dict(schema='v9-main-context-bindings-1',contexts=[],figures=[figure]), old)
    assert 'UNBOUND_OR_CHANGED_FIGURE_SOURCE' in categories(report)
    assert 'V9_FIGURE_BINDING_INVALID' in categories(report)


def test_missing_figure_failure_never_resolves(tmp_path):
    figure = figure_fixture(tmp_path)
    old = synthetic_report('')
    old['failures'].append({'category':'MISSING_CURRENT_FIGURE','path':figure['path']})
    report = resolve(tmp_path, '', dict(schema='v9-main-context-bindings-1',contexts=[],figures=[figure]), old)
    assert 'MISSING_CURRENT_FIGURE' in categories(report)
