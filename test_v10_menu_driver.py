"""Artificial timing, stage and control fixtures; no study inputs or execution."""
from copy import deepcopy
import importlib
import importlib.util
import math

import pytest


def api():
    assert importlib.util.find_spec('run_v10_menu') is not None, 'v10 menu driver is missing'
    return importlib.import_module('run_v10_menu')


def design():
    return dict(worker_count=4, pilot_repetitions=2, projection_safety_factor=1.35,
                projection_reserve_seconds=180, formal_max_seconds=1800,
                formal_repetition_candidates=[32, 16], sources=list(range(13)))


def pilot_rows(seconds=10.):
    return [dict(complete=True, elapsed_seconds=seconds) for _ in range(26)]


@pytest.mark.parametrize('seconds,repetitions,want32,want16', [
    (10., 32, 1584., 882.),
    (20., 16, 2988., 1584.),
    (25., None, 3690., 1935.),
])
def test_timing_formula_selects_largest_predicted_fit_and_has_no_qr_only_fallback(seconds, repetitions, want32, want16):
    got = api().choose_configuration(pilot_rows(seconds), design())
    assert got['repetitions'] == repetitions
    assert [r['repetitions'] for r in got['projection_ladder']] == [32, 16]
    assert [r['predicted_seconds'] for r in got['projection_ladder']] == pytest.approx([want32, want16])
    assert [r['predicted_fits'] for r in got['projection_ladder']] == [want32 <= 1800, want16 <= 1800]


def test_timing_projection_uses_longest_unit_bound_in_addition_to_worker_divisor():
    rows = pilot_rows(.1)
    rows[0]['elapsed_seconds'] = 50.
    got = api().choose_configuration(rows, design())
    assert got['repetitions'] == 32
    assert [r['predicted_seconds'] for r in got['projection_ladder']] == pytest.approx([1260., 720.])


@pytest.mark.parametrize('count', [0, 25, 27])
def test_pilot_inventory_must_have_exactly_all_26_units(count):
    rows = [dict(complete=True, elapsed_seconds=10.) for _ in range(count)]
    got = api().choose_configuration(rows, design())
    assert got['repetitions'] is None
    assert all(r['predicted_seconds'] is None and not r['predicted_fits'] for r in got['projection_ladder'])


@pytest.mark.parametrize('change', [
    {'complete': False}, {'complete': None}, {'elapsed_seconds': None},
    {'elapsed_seconds': 0.}, {'elapsed_seconds': -1.},
    {'elapsed_seconds': float('nan')}, {'elapsed_seconds': float('inf')},
    {'elapsed_seconds': '10'}, {'elapsed_seconds': True},
])
def test_any_incomplete_or_invalid_pilot_timing_forbids_formal(change):
    rows = pilot_rows()
    rows[7].update(change)
    got = api().choose_configuration(rows, design())
    assert got['repetitions'] is None
    assert all(r['predicted_seconds'] is None and not r['predicted_fits'] for r in got['projection_ladder'])


def test_missing_pilot_elapsed_field_forbids_formal_without_assuming_zero_cost():
    rows = pilot_rows()
    del rows[8]['elapsed_seconds']
    assert api().choose_configuration(rows, design())['repetitions'] is None


def test_numerical_candidate_failure_does_not_erase_complete_unit_timing():
    rows = pilot_rows()
    rows[5]['reason'] = 'NONCONVERGENCE'
    rows[5]['records'] = [{'status': 'FAILED', 'qr_reason': 'VALIDATION_INELIGIBLE'}]
    assert api().choose_configuration(rows, design())['repetitions'] == 32


@pytest.mark.parametrize('phase,repetitions,want_r,want_tag,want_denominator', [
    ('pilot', None, 2, 1, 2),
    ('formal', 32, 32, 2, 32),
    ('formal', 16, 16, 2, 32),
])
def test_stage_plan_preserves_each_old_stage_stream_and_formal_phase_grid(phase, repetitions, want_r, want_tag, want_denominator):
    got = api().stage_plan(phase, repetitions=repetitions)
    assert got['repetitions'] == want_r
    assert got['stream_tag'] == want_tag
    assert got['path_phase_repetitions'] == want_denominator
    if phase == 'formal':
        # M404 is original weekly geometry, used here as an integer clock only.
        assert [r*404//got['path_phase_repetitions'] for r in range(want_r)] == [r*404//32 for r in range(want_r)]


def control_inputs():
    geometry = dict(phase=12, uniform_sha256='artificial-uniform',
        rng_initial={'state': 1}, rng_final={'state': 2},
        regime_ids=[0, 1, 0], transition_indices=[1], wrap_indices=[2],
        exposure={'validation': {'forward_transitions': 1, 'wraps': 1}})
    points = dict(capacities=[1.5, 2.], losses=[.01, .02], breaches=[False, True])
    score = dict(n=2, mean_loss=.015, strict_breach_count=1, strict_breach_rate=.5)
    return [deepcopy(geometry), deepcopy(geometry), deepcopy(points), deepcopy(points), deepcopy(score), deepcopy(score)]


def test_control_accepts_exact_full_receipts_without_mutating_them():
    inputs = control_inputs()
    saved = deepcopy(inputs)
    api().verify_control(*inputs)
    assert inputs == saved


@pytest.mark.parametrize('argument,path,value', [
    (0, ['phase'], 13),
    (0, ['uniform_sha256'], 'different-uniform'),
    (0, ['rng_initial', 'state'], 3),
    (0, ['rng_final', 'state'], 3),
    (0, ['regime_ids'], [0, 0, 0]),
    (0, ['transition_indices'], []),
    (0, ['wrap_indices'], []),
    (0, ['exposure', 'validation', 'wraps'], 0),
    (2, ['capacities'], [math.nextafter(1.5, math.inf), 2.]),
    (2, ['losses'], [.01, math.nextafter(.02, math.inf)]),
    (2, ['breaches'], [False, False]),
    (4, ['n'], 1),
    (4, ['mean_loss'], math.nextafter(.015, math.inf)),
    (4, ['strict_breach_count'], 0),
    (4, ['strict_breach_rate'], .0),
])
def test_any_geometry_point_or_scalar_difference_rejects_control(argument, path, value):
    inputs = control_inputs()
    target = inputs[argument]
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        api().verify_control(*inputs)
