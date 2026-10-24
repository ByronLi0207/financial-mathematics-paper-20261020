"""WP3 display checks use constructed scalar summaries; no simulated process."""
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent
MODULE = ROOT / 'notes/revision-v8/plot_wp3.py'


def load_module():
    spec = importlib.util.spec_from_file_location('plot_wp3', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_summary():
    return {'cells': [dict(method=method, phi=phi, variance_persistence=p,
        window=w, horizon=h, planned_repetitions=32, complete_repetitions=32,
        full_procedure_status='COMPLETE', relative_loss_percent=-12.345,
        relative_loss_mcse=1.25, model_breach_rate=.0625, model_breach_mcse=.005,
        win_fraction=.75, win_mcse=.07)
        for method in ('F','QR33','QR4') for phi in (.7,.9,.98)
        for p in (0.,.9,.98) for w in (52,260,720,2880) for h in (6,24)]}


def test_display_module_is_standard_library_only_at_import():
    command = "import runpy,sys; runpy.run_path(%r); assert not any(x in sys.modules for x in ('numpy','matplotlib','conditional_study','v8_mechanism_mc'))" % str(MODULE)
    result = subprocess.run([sys.executable,'-c',command],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr


def test_grid_has_six_facets_and_exactly_72_unique_cells():
    module = load_module(); panels = module.prepare_grids(fixture_summary(),'QR33','loss')
    assert len(panels) == 6
    assert sum(len(row) for p in panels for row in p['cells']) == 72
    assert [(p['horizon'],p['phi']) for p in panels] == [(h,phi) for h in (6,24) for phi in (.7,.9,.98)]
    assert panels[0]['cells'][0][0]['value'] == -12.345
    assert panels[0]['cells'][0][0]['mcse'] == 1.25
    assert all(c['eligible'] for p in panels for row in p['cells'] for c in row)


def test_partial_available_pair_value_is_na_never_zero_or_colored():
    module = load_module(); summary = fixture_summary()
    row = next(r for r in summary['cells'] if r['method']=='QR33')
    row.update(complete_repetitions=31,full_procedure_status='NA',relative_loss_percent=-99.)
    cell = module.prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
    assert cell['value'] is None and cell['mcse'] is None and not cell['eligible']
    assert cell['annotation'] == 'NA\n31/32'
    assert cell['conditional_value'] == -99.
    assert row['relative_loss_percent'] == -99.


def test_complete_status_cannot_override_missing_repetitions():
    module = load_module(); summary = fixture_summary()
    summary['cells'][72].update(complete_repetitions=0,full_procedure_status='COMPLETE')
    cell = module.prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
    assert cell['value'] is None and not cell['eligible']


@pytest.mark.parametrize('metric,expected,expected_se',[('breach',6.25,.5),('win',75.,7.)])
def test_probability_display_only_converts_units(metric,expected,expected_se):
    cell = load_module().prepare_grids(fixture_summary(),'QR4',metric)[0]['cells'][0][0]
    assert cell['value'] == expected
    assert cell['mcse'] == pytest.approx(expected_se)


@pytest.mark.parametrize('mutation',['duplicate','missing','unexpected'])
def test_full_factorial_inventory_is_required(mutation):
    summary = fixture_summary()
    if mutation=='duplicate': summary['cells'].append(dict(summary['cells'][72]))
    elif mutation=='missing': summary['cells'].pop(72)
    else: summary['cells'][72]['phi']=.8
    with pytest.raises(ValueError): load_module().prepare_grids(summary,'QR33','loss')


@pytest.mark.parametrize('bad',[None,math.nan,math.inf])
def test_nonfinite_complete_value_is_na_with_explicit_reason(bad):
    summary=fixture_summary();summary['cells'][72]['relative_loss_percent']=bad
    cell=load_module().prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
    assert not cell['eligible'] and cell['annotation']=='NA\n32/32'
    assert cell['reason']=='MISSING_OR_NONFINITE_ESTIMATE'


def test_fixed_color_limits_do_not_depend_on_results_and_annotations_retain_outliers():
    module=load_module();summary=fixture_summary();summary['cells'][72]['relative_loss_percent']=1750.5
    cell=module.prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
    assert cell['value']==1750.5 and '1750.5' in cell['annotation']
    assert module.METRICS['loss']['limits']==(-100.,100.)
    assert module.METRICS['breach']['limits']==(0.,100.)
    assert module.METRICS['win']['limits']==(0.,100.)


def test_zero_is_a_valid_complete_estimate():
    summary=fixture_summary();summary['cells'][72].update(relative_loss_percent=0.,relative_loss_mcse=0.)
    cell=load_module().prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
    assert cell['eligible'] and cell['value']==0. and cell['mcse']==0.


def test_unknown_method_or_metric_is_rejected():
    module=load_module()
    with pytest.raises(ValueError):module.prepare_grids(fixture_summary(),'QRF','loss')
    with pytest.raises(ValueError):module.prepare_grids(fixture_summary(),'QR33','pvalue')


def test_win_caption_distinguishes_zero_plugin_se_from_finite_repetition_certainty():
    module=load_module();text=module.caption('QR4','win')
    assert 'plug-in binomial Monte Carlo SE' in text
    assert 'zero for all wins or no wins' in text
    assert 'does not imply certainty from 32 repetitions' in text
    assert 'saved summary also reports the worst-case SE bound 0.5/√32' in text
    assert 'plug-in binomial Monte Carlo SE' not in module.caption('QR4','loss')
