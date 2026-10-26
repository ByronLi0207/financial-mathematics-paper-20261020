"""Tiny synthetic end-to-end wiring check; no real calibration or archives."""
from copy import deepcopy
import hashlib
import json
import math

import numpy as np

from run_v9_nonstationarity import simulate_unit as inherited_unit
from run_v10_menu import simulate_unit as expanded_unit
from v9_switching import generate_pair


def read(path):
    return json.loads(path.read_text())


def test_artificial_old_and_expanded_units_preserve_controls_and_attach_same_rep(tmp_path):
    whole = dict(intercept=.2, phi=.4, omega=.1, alpha=.05, beta=.5, nu=8.)
    segments = [dict(whole, intercept=.1, phi=.3, nu=6.),
                dict(whole, intercept=-.1, phi=.7, omega=.12, nu=10.)]
    calibration = dict(source_id='ARTIFICIAL_ONLY', source_index=0, n=201, M=200,
        whole_fit={'params': whole}, calibration_status='COMPLETE',
        partition={'cuts': [100], 'segment_lengths': [100, 100]},
        segment_fits=[{'params': p} for p in segments])
    old_design = dict(master_entropy=424242, rng_namespace=9, burn_in=8,
        retained_observations=500, initial_level=0., initial_variance=1.,
        validation_first=300, validation_last=301, evaluation_first=360,
        evaluation_last=361, horizon=6, windows=[52], refit_step=24,
        feature_rms_short=24, feature_rms_long=168, feature_valid_from=168,
        nominal_gap_seconds=3600,
        menus={'QR33': [.001, .01, .1], 'QR4': [.001, .01, .1, 1., 10.]})
    new_design = deepcopy(old_design)
    menu = [.001, .01, .1, 1., 10., 'inf']
    new_design['menus'] = {'QR33': list(menu), 'QR4': list(menu)}
    calibration_before, old_before = deepcopy(calibration), deepcopy(old_design)
    old_dir, new_dir = tmp_path/'artificial-old', tmp_path/'artificial-expanded'
    old = inherited_unit(calibration, 1, 2, 1, old_design, old_dir)
    def legacy(name):
        return read(old_dir/name)
    new = expanded_unit(calibration, 1, 2, 1, new_design, new_dir, legacy=legacy)
    assert old['complete'] is True and new['complete'] is True
    assert calibration == calibration_before and old_design == old_before
    assert len(new['records']) == 4
    assert {(r['arm'], r['window'], r['method']) for r in new['records']} == {
        (arm, 52, method) for arm in ('constant', 'switching') for method in ('QR33', 'QR4')}

    # The extra direct generation is artificial and supplies an independent
    # byte-level oracle for the newly archived path hashes.
    pair = generate_pair(whole, segments, [100, 100], 0, 1, 2, 1, new_design)
    for arm in ('constant', 'switching'):
        assert read(new_dir/f'geometry-{arm}.json') == read(old_dir/f'geometry-{arm}.json')
        assert read(new_dir/arm/'W52-F-evaluation-points.json') == read(old_dir/arm/'W52-F-evaluation-points.json')
        assert read(new_dir/arm/'W52_H6_F.json')['evaluation'] == read(old_dir/arm/'W52_H6_F.json')['evaluation']
        proof = read(new_dir/arm/'W52-F-control-check.json')
        assert proof == dict(status='EXACT_MATCH', geometry=True, all_point_arrays=True, all_score_scalars=True)
        hashes = read(new_dir/f'path-hashes-{arm}.json')
        assert hashes == {name: hashlib.sha256(np.ascontiguousarray(pair[arm][name], dtype='<f8').tobytes()).hexdigest()
                          for name in ('position', 'variance', 'innovations')}
        for method in ('QR33', 'QR4'):
            receipt = read(new_dir/arm/f'W52_H6_{method}.json')
            assert [r['penalty'] for r in receipt['candidates']] == menu
            assert len(list((new_dir/arm).glob(f'W52_H6_{method}_validation-*.json'))) == 6
            infinity = receipt['candidates'][-1]
            assert infinity['status'] == 'COMPLETE' and infinity['origin_count'] == 2
            assert math.isfinite(infinity['mean_loss'])
            if receipt['status'] == 'COMPLETE':
                assert receipt['selected_penalty'] in menu and receipt['evaluation']['n'] == 2
                assert read(new_dir/arm/f'W52_H6_{method}.selection.json')['penalty'] == receipt['selected_penalty']

    for row in new['records']:
        assert row['source_id'] == 'ARTIFICIAL_ONLY' and row['rep'] == 1
        original = legacy(f"comparison-{row['arm']}-W52-{row['method']}.json")
        assert row['original_status'] == original['status']
        assert row['original_qr_mean_loss'] == original['qr_mean_loss']
        assert row['original_f_mean_loss'] == original['f_mean_loss']
