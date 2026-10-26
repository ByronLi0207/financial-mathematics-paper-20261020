"""Deliberately corrupted saved-figure receipts; no new financial analysis."""
import copy,importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('figure_number_check',ROOT/'notes/revision-v8/check_wp8_figures.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def fixture():
    read=lambda p:json.loads((ROOT/p).read_text())
    return read('results/revision-v8/wp3/summary.json'),read('protocol/revision-v8/wp3-mechanism-design.json'),read('results/revision-v8/wp3/figures/display-receipt.json')

def codes(errors):return {r['code'] for r in errors}

def test_complete_keyed_figures_have_all432_cells():
    errors,proof=m.audit_mc(*fixture())
    assert errors==[] and len(proof)==432


def test_annotation_copied_from_another_real_cell_is_rejected():
    s,d,r=fixture();cells=r['figures'][0]['panels'][0]['cells'][0]
    cells[0]['annotation']=cells[1]['annotation']
    assert 'FIGURE_ANNOTATION' in codes(m.audit_mc(s,d,r)[0])


def test_swapped_complete_cells_are_not_global_membership_pass():
    s,d,r=fixture();cells=r['figures'][0]['panels'][0]['cells'][0];cells[0],cells[1]=cells[1],cells[0]
    assert 'CELL_POSITION' in codes(m.audit_mc(s,d,r)[0])


def test_wrong_MCSE_is_rejected_even_if_annotation_unchanged():
    s,d,r=fixture();r['figures'][0]['panels'][0]['cells'][0][0]['mcse']*=100
    assert 'CELL_VALUE_OR_ELIGIBILITY' in codes(m.audit_mc(s,d,r)[0])


def test_changed_completion_count_cannot_relabel_complete():
    s,d,r=fixture();r['figures'][0]['panels'][0]['cells'][0][0]['complete_repetitions']-=1
    assert 'CELL_VALUE_OR_ELIGIBILITY' in codes(m.audit_mc(s,d,r)[0])


def test_dropped_chart_does_not_silently_reduce_inventory():
    s,d,r=fixture();r['figures'].pop()
    assert 'FIGURE_SET' in codes(m.audit_mc(s,d,r)[0])
