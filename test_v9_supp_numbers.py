"""Current v9 source/relocation controls; no financial models or statistics."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parent


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


@pytest.fixture(scope='module')
def qa():
    return load('notes/revision-v9/wp7_supplement_numeric_audit.py','v9_supp_current_guard')


def test_current_v9_full_source_gate_has_no_unclassified_residuals(qa,tmp_path):
    result=qa.audit(ROOT,view_root=tmp_path/'replay',legacy_receipt=None)
    assert result['status']=='PASS_WITH_SCOPE_LIMITS'
    assert result['mismatch_count']==0
    assert result['relocation']['inverse_mapping_exact'] is True
    assert result['new_protocol_constants']['unclassified_scientific_numeric_paragraphs']==0
    assert result['new_tables']['native_binding_records_checked']==228
    assert result['new_tables']['complete_ordered_rows_checked']==43
    assert result['unchanged_legacy_guard']['failures']==0
    assert result['unchanged_legacy_guard']['unresolved']==0
    assert result['unchanged_legacy_guard']['ambiguous']==0
    assert result['private_arrays_read'] is False
    assert result['PDFs_read'] is False


def test_exactly_named_fixture_difference_keeps_all_old_assertions(qa):
    proof=qa.fixture_contract(ROOT)
    assert proof['status']=='PASS'
    assert proof['old_guard_unchanged'] is True
    assert len(proof['test_methods'])==8
    assert all(x['exact_source_identical'] for x in proof['test_methods'])
    proof=qa.preserve_archives(ROOT)
    assert proof['mismatch_count']==0
    assert [x['path'] for x in proof['allowed_existing_code_differences']]==['notes/revision-v8/test_v8_supp_numbers.py']
    assert proof['existing_files_checked']==proof['unchanged_files']+1


def test_changed_current_old_scientific_row_blocks_reconstruction(qa):
    original=(ROOT/qa.SUPP).read_text()
    assert '156123.03 & 166531.06' in original
    wrong=original.replace('156123.03 & 166531.06','156123.04 & 166531.06',1)
    with pytest.raises(ValueError):qa.relocation(ROOT,compact_text=wrong)


def test_omitted_current_extended_adverse_fragment_blocks_reconstruction(qa):
    original=(ROOT/qa.EXT).read_text()
    lines=original.splitlines(keepends=True)
    row=next(x for x in lines if '&' in x and any(c.isdigit() for c in x) and x.rstrip().endswith(r'\\'))
    with pytest.raises(ValueError):qa.relocation(ROOT,extended_text=original.replace(row,'',1))


@pytest.mark.parametrize('before,after',[
    ('2026102492','2026102493'),
    (r'at least 80\%',r'at least 81\%'),
    (r'\sqrt{\frac{3}{5}}',r'\sqrt{\frac{4}{5}}'),
])
def test_changed_new_protocol_value_is_rejected(qa,before,after):
    _,added,_=qa.relocation(ROOT)
    assert before in added
    with pytest.raises(ValueError):qa.protocol_constants(ROOT,added.replace(before,after,1))


def test_unbound_new_result_beside_registered_link_is_rejected(qa):
    _,added,_=qa.relocation(ROOT)
    anchor='Cutpoints interpolate the relative-loss curve'
    assert anchor in added
    changed=added.replace(anchor,'An extra result is $p=0.123$.\n\n'+anchor,1)
    with pytest.raises(ValueError):qa.protocol_constants(ROOT,changed)


def test_changed_new_table_number_or_missing_row_is_rejected(qa):
    original=(ROOT/qa.TABLE).read_text()
    wrong=original.replace('$47/48$','$48/47$',1)
    with pytest.raises(ValueError):qa.new_tables(ROOT,tex_text=wrong)
    row=next(x for x in original.splitlines(keepends=True) if 'v9-row:confirmation_failures:' in x)
    with pytest.raises(ValueError):qa.new_tables(ROOT,tex_text=original.replace(row,'',1))


def test_constructed_new_saved_source_field_mutation_is_rejected(qa):
    payload=json.loads((ROOT/'notes/revision-v9/wp6-new-number-bindings.json').read_text())
    binding=payload['bindings'][0]
    original=json.loads((ROOT/binding['source_path']).read_text())
    changed=copy.deepcopy(original)
    first=binding['JSON_pointers'][0]
    parts=first.strip('/').split('/')
    owner=changed
    for part in parts[:-1]:owner=owner[int(part)] if isinstance(owner,list) else owner[part]
    leaf=parts[-1]
    owner[int(leaf) if isinstance(owner,list) else leaf]+=1
    with pytest.raises(ValueError):qa.check_native_binding(binding,changed)


def test_constructed_old_saved_source_field_mutation_reaches_strict_guard(qa):
    legacy=load(qa.GUARD,'old_supp_guard_for_source_control')
    auditor=legacy.Audit(ROOT)
    bindings=auditor.load('notes/v7/s5-supplement-bindings.json')['bindings']
    row=next(x for x in bindings if x['format']=='json' and type(x['value']) in (int,float) and x['pointer'])
    changed=copy.deepcopy(auditor.load(row['source']))
    parts=row['pointer'].strip('/').split('/')
    owner=changed
    for part in parts[:-1]:
        part=part.replace('~1','/').replace('~0','~')
        owner=owner[int(part)] if isinstance(owner,list) else owner[part]
    leaf=parts[-1].replace('~1','/').replace('~0','~')
    owner[int(leaf) if isinstance(owner,list) else leaf]+=1
    auditor.cache[row['source']]=changed
    auditor.old_sources()
    assert any(x['gate']=='old_typed_field' for x in auditor.failures)
