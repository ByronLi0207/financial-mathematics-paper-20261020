"""Frozen PR #5 v8 document negative controls; v9 authoring stays independent.

All original field/source guards and negative assertions remain in place.
These historical cases audit public-base document fixtures, not the v9 draft.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parent
FROZEN=ROOT/'fixtures/v9-baselines/pr5-v8'
BASE_COMMIT='0f1f066843e0c49cf3e24bce7d72032dc189603d'


def frozen_document(name):
    assert (FROZEN/'manifest.json').is_file(), 'frozen public PR #5 document fixtures missing'
    manifest=json.loads((FROZEN/'manifest.json').read_text())
    assert manifest['source_commit']==BASE_COMMIT
    raw=(FROZEN/name).read_bytes();entry=manifest['members'][name]
    assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256']
    return raw


def checker():
    spec=importlib.util.spec_from_file_location('wp8main',ROOT/'notes/revision-v8/check_wp8_main_numbers.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


@pytest.fixture
def documents(tmp_path):
    main=tmp_path/'manuscript.tex';letter=tmp_path/'cover-letter.md'
    main.write_bytes(frozen_document('submission-jof/manuscript.tex'))
    letter.write_bytes(frozen_document('submission-jof/cover-letter.md'))
    return main,letter


def run(documents):
    main,letter=documents
    return checker().audit_documents(main,letter,root=ROOT)


def replace(path,old,new):
    text=path.read_text();assert text.count(old)==1
    path.write_text(text.replace(old,new))


def test_actual_current_main_has_no_unlocated_numeric_result(documents):
    r=run(documents)
    assert r['status']=='PASS',r['failures'][:15]
    assert r['unclassified_numeric_occurrences']==0
    assert r['ambiguous_numeric_locations']==0
    assert r['cover_letter_numeric_occurrences']==0
    assert not r['full_artifact_numeric_acceptance']
    assert r['original_evidence_fields_checked']==1205


def test_wrong_paired_table_count_is_not_global_value_membership(documents):
    replace(documents[0],'-14.77 & 6625 & 376 / 360', '-14.77 & 6625 & 360 / 376')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='TABLE_NUMERIC_SEQUENCE_MISMATCH' for x in r['failures'])


def test_changed_prose_percentage_fails_saved_field_display_check(documents):
    replace(documents[0],'matched score falls about 12.2\\%', 'matched score falls about 21.2\\%')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='PERCENTAGE_DISPLAY_MISMATCH' for x in r['failures'])


def test_wrong_new_breach_count_does_not_pass_equal_value_elsewhere(documents):
    replace(documents[0],'Matched breaches are 416 for regression and 282', 'Matched breaches are 282 for regression and 416')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='NEW_CONTEXT_VALUE_MISMATCH' for x in r['failures'])


@pytest.mark.parametrize('probability',['0.123','0.055'])
def test_unbound_inline_math_probability_is_not_structural_escape(documents,probability):
    replace(documents[0],'These specified processes therefore','An added probability is '+r'\(p='+probability+r'\). These specified processes therefore')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='UNBOUND_NUMERIC_OCCURRENCE' and x.get('token')==probability for x in r['failures'])


def test_unbound_new_numeric_prose_is_reported(documents):
    replace(documents[0],'\\section{Limitations}', 'A further result has value 987.654.\n\n\\section{Limitations}')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='UNBOUND_NUMERIC_OCCURRENCE' and x.get('token')=='987.654' for x in r['failures'])


def test_modified_accepted_math_constant_is_not_blanket_classified(documents):
    replace(documents[0],r'\tau=19/20',r'\tau=19/21')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category'] in ('UNBOUND_NUMERIC_OCCURRENCE','PRESERVED_MATH_MISMATCH') for x in r['failures'])


def test_unbound_new_cover_letter_result_is_not_outside_checker(documents):
    documents[1].write_text(documents[1].read_text()+'\nA new numerical advantage is 42.7 percent.\n')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='UNBOUND_NUMERIC_OCCURRENCE' and x.get('file')=='cover_letter' for x in r['failures'])


def test_new_number_word_claim_is_not_silently_ignored(documents):
    replace(documents[0],'across three windows with previously examined outcomes','across four windows with previously examined outcomes')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='UNBOUND_NUMBER_WORD' for x in r['failures'])


def test_false_global_pass_for_external_reference_or_figure_gates_is_forbidden(documents):
    r=run(documents)
    assert r['figure_values_verified_here'] is False
    assert r['reference_metadata_verified_here'] is False
    assert r['figure_paths'] and all(x['current_sha256'] for x in r['figure_paths'])
    assert r['reference_metadata_occurrences']>0


def test_deleted_unfavorable_table_row_cannot_pass_remaining_number_checks(documents):
    row='Later / matched & Same-history fixed-window headroom & -14.77 & 6625 & 376 / 360\\\\\n'
    replace(documents[0],row,'')
    r=run(documents)
    assert r['status']=='FAIL'
    assert any(x['category']=='PRESERVED_TABLE_NUMERIC_VECTOR_MISMATCH' for x in r['failures'])
