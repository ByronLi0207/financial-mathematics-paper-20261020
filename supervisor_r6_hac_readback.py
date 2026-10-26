#!/usr/bin/env python3
"""Two descriptive HAC comparisons of immutable, saved R6 FX loss arrays.

No source data, label construction, forecast, fit or selection is performed.
The conditional QR report is the original-three-menu selection (also R0 in
this group), not the main R2 procedure. Existing study archives stay read-only.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from inference_tests import bandwidth, dm_test


ROOT = Path(__file__).resolve().parent
R6 = ROOT / 'results/supervisor-20261023/r6'
OUTPUT = ROOT / 'results/supervisor-20261023/r6-writing-hac-20261023'
GROUP = '.scratch/r6-20261023/run/retro/retro-fx_hourly-h6-w2880/'
PINS = {
    'results/supervisor-20261023/r6/private-archive-manifest.json':
        '926747a8d140b78112bf00793f1c42a2c4914883e93401d1c14fb265d5af9b9e',
    'results/supervisor-20261023/r6/retro-seal.json':
        'bf20128698618ce7d843d3a8069ac776ef20ced85a5f2e9540f1865141599638',
    'results/supervisor-20261023/r6/verification.json':
        '83522d3577274486cded6449bbb36ae3475051f24bb804f85ddc7860bbef1862',
    'inference_tests.py':
        '2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c',
    GROUP + '0.01-8999-10438-w2880-d24.npz':
        'c29e6a17459cf59f0af04bba839cc5711d06c9b0b4ac31ddbdbcfc7cb8c0d831',
    GROUP + 'F-8999-10438-w2880-d24.npz':
        '1d2f318eebe1f34c1aced3016e431d10e88889fba6615231565db7e8f2e9a65c',
    GROUP + 'F-8999-10438-w720-d1.npz':
        '8070df82a33bb635432173f86b6cec02142875947836df85ec26e0e197e9c518',
}
SCOPE = (
    'Post-result descriptive, nonconfirmatory paired unconditional HAC comparisons '
    'of two fixed references for the same retrospective conditional QR report. '
    'The original-three-menu validation selected lambda 0.01, also selected by R0 '
    'in this group. These are QR-versus-F comparisons, not R2 results. The R6 '
    'rules followed earlier inspected results; the bounded repository audit found '
    'no prior evaluation role for these earlier origins, but the raw history '
    'was familiar. These p-values are a later writing-stage readback and do not '
    'account for the whole selection and inspection process or supply confirmatory '
    'error control, prospective validation, or external replication.'
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def read_csv(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(relative):
    path = ROOT / relative
    return dict(path=relative, bytes=path.stat().st_size, sha256=sha(path))


def run():
    require(not OUTPUT.exists(), 'Refusing existing output directory')
    identities = []
    for relative, expected in PINS.items():
        item = identity(relative)
        require(item['sha256'] == expected, 'Pinned input hash mismatch: ' + relative)
        identities.append(item)
    archive = read_json(R6 / 'private-archive-manifest.json')
    seal = read_json(R6 / 'retro-seal.json')
    verified = read_json(R6 / 'verification.json')
    require(verified['status'] == 'PASS' and not verified['issues'], 'R6 verification must be PASS')
    require(seal['status'] == 'SEALED', 'Retro archive must be sealed')
    archived = {r['path']: r for r in archive['files']}
    sealed = {r['path']: r for r in seal['files']}
    def bound_file(relative, *, private=True):
        item = identity(relative)
        for ledger in ((archived, sealed) if private else (sealed,)):
            require(relative in ledger and ledger[relative]['sha256'] == item['sha256']
                and ledger[relative]['bytes'] == item['bytes'], 'Archive/seal binding mismatch: ' + relative)
        return item
    for relative in PINS:
        if relative.endswith('.npz'):
            bound_file(relative)
    selection_path = GROUP + 'selection-before-evaluation.json'
    identities.append(bound_file(selection_path))
    frozen = read_json(ROOT / selection_path)
    require(frozen['primary_selection']['status'] == 'SELECTED'
        and frozen['primary_selection']['selected_id'] == '0.01'
        and frozen['rules']['R0']['status'] == 'SELECTED'
        and frozen['rules']['R0']['selected_id'] == '0.01', 'Frozen original-menu/R0 selection identity')
    require([r['candidate_id'] for r in frozen['primary_selection']['candidates']]
        == ['0.001', '0.01', '0.1'], 'Original three-penalty menu identity')
    primary_path = 'results/supervisor-20261023/r6/primary-replication.csv'
    identities.append(bound_file(primary_path, private=False))
    primary = next(r for r in read_csv(ROOT / primary_path) if r['id'] == 'FX-original-structure')
    require(primary['status'] == 'COMPLETE' and primary['selected_id'] == '0.01'
        and primary['QR_trace_sha256'] == PINS[GROUP + '0.01-8999-10438-w2880-d24.npz']
        and primary['F_trace_sha256'] == PINS[GROUP + 'F-8999-10438-w720-d1.npz'], 'Primary trace binding')
    summary = read_csv(R6 / 'summary.csv')
    summary_identity = identity('results/supervisor-20261023/r6/summary.csv')
    verified_public = {r['path']: r for r in verified['public_input_identities']}
    require(summary_identity == verified_public[summary_identity['path']], 'Prior verified summary identity')
    identities.append(summary_identity)
    rows = {r['report']: r for r in summary if r['phase'] == 'retro'
        and r['source'] == 'fx_hourly' and r['horizon'] == '6' and r['window'] == '2880'}
    require(rows['R0']['status'] == rows['F']['status'] == 'COMPLETE'
        and rows['R0']['selected_id'] == '0.01'
        and rows['R0']['trace_sha256'] == primary['QR_trace_sha256']
        and rows['F']['trace_sha256'] == PINS[GROUP + 'F-8999-10438-w2880-d24.npz'], 'Matched QR/R0/F binding')
    def saved_loss(name):
        relative = GROUP + name
        with np.load(ROOT / relative, allow_pickle=False) as data:
            origins, loss = data['origins'].copy(), data['pinball'].copy()
        require(origins.ndim == loss.ndim == 1 and len(origins) == len(loss), 'Aligned saved trace vectors')
        require(np.array_equal(origins, np.arange(8999, 10439, dtype=np.int64)), 'Exact declared saved origin grid')
        require(np.isfinite(loss).all(), 'Finite saved losses required')
        return origins, loss
    origins, qr = saved_loss('0.01-8999-10438-w2880-d24.npz')
    n, horizon = len(origins), 6
    lag = max(horizon, math.floor(4 * (n / 100) ** (2 / 9)))
    require(n == 1440 and lag == 7 and bandwidth(n, horizon) == lag and n > lag, 'Frozen bandwidth identity')
    mean_qr = math.fsum(map(float, qr)) / n
    comparisons = []
    references = (
        ('matched_frozen_F2880_d24', 'F-8999-10438-w2880-d24.npz', 2880, 24),
        ('original_primary_rolling_F720_d1', 'F-8999-10438-w720-d1.npz', 720, 1),
    )
    for name, filename, window, refit in references:
        reference_origins, reference = saved_loss(filename)
        require(np.array_equal(origins, reference_origins), 'Exact paired origin equality')
        mean_reference = math.fsum(map(float, reference)) / n
        require(mean_reference > 0, 'Positive reference mean required for ratio')
        test = dm_test(qr - reference, horizon, L=lag)
        difference = math.fsum(float(x) - float(y) for x, y in zip(qr, reference)) / n
        require(test['mean_difference'] == difference, 'Paired mean differential readback')
        if test['status'] == 'OK':
            require(test['lrv'] > 0 and math.isfinite(test['dm_t'])
                and test['dm_p'] is not None and 0 <= test['dm_p'] <= 1, 'Finite positive-variance HAC result')
        else:
            require(test['dm_t'] is None and test['dm_p'] is None, 'Undefined HAC must remain undefined')
        comparisons.append(dict(comparison=name, phase='retro', source='fx_hourly', horizon=horizon,
            conditional_report='QR_original_three_menu_also_R0_NOT_R2', selected_lambda='0.01',
            QR_window=2880, QR_refit_step=24, F_window=window, F_refit_step=refit,
            n=n, H=horizon, L=lag, origin_first=int(origins[0]), origin_last=int(origins[-1]),
            exact_shared_origins=True, QR_mean_loss=mean_qr, F_mean_loss=mean_reference,
            mean_loss_difference_QR_minus_F=difference,
            ratio_change_percent=100 * (mean_qr / mean_reference - 1),
            raw_LRV=test['lrv'], HAC_statistic=test['dm_t'], two_sided_normal_HAC_p=test['dm_p'],
            status=test['status'], reference_distribution='standard_normal_two_sided',
            covariance='Bartlett_Newey_West_divisor_n', multiplicity_adjustment='none_descriptive_only',
            QR_trace_sha256=primary['QR_trace_sha256'], F_trace_sha256=PINS[GROUP + filename]))
    require(len(comparisons) == 2, 'Exactly two comparisons')
    require(math.isclose(comparisons[0]['ratio_change_percent'], float(rows['R0']['percent_vs_F']), rel_tol=1e-13)
        and math.isclose(comparisons[1]['ratio_change_percent'], float(primary['percent_vs_reference']), rel_tol=1e-13),
        'Existing matched/primary ratio readback')
    # Check every bound input again before writing new aggregates.
    for item in identities:
        require(identity(item['path']) == item, 'Input changed during readback: ' + item['path'])
    result = dict(status='COMPLETE', created_utc=datetime.now(timezone.utc).isoformat(),
        scope=SCOPE, experiment_or_refit=False, labels_or_source_data_loaded=False,
        candidate_reselection=False, comparison_count=2, input_identities=identities,
        code_identity=identity(Path(__file__).name),
        method=dict(function='inference_tests.dm_test', bandwidth_function='inference_tests.bandwidth',
            difference='saved QR pinball loss minus saved F pinball loss',
            bandwidth='max(H,floor(4*(n/100)**(2/9)))', n=n, H=horizon, L=lag,
            reference_distribution='two-sided standard normal',
            estimator='Bartlett Newey-West, centered covariance divided by n',
            negative_or_zero_LRV='Retain raw LRV and undefined statistic/p; no fabricated zero p-value',
            additional_sensitivities_reported=False),
        comparisons=comparisons)
    OUTPUT.mkdir(exist_ok=False)
    with (OUTPUT / 'results.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    with (OUTPUT / 'comparisons.csv').open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)
    lines = [
        '# R6 writing-stage paired HAC readback', '', SCOPE, '',
        'Exactly two comparisons use the same saved QR W2880/d24, lambda 0.01 report '
        'on retrospective FX H6 origins 8999–10438 (n=1440). The references are '
        'matched frozen F/W2880/d24 and original-primary rolling F/W720/d1. '
        'The first comparison has a different reference from the original-primary comparison.', '',
        'The manuscript Section 5 definition and unchanged inference_tests.dm_test '
        'supply Bartlett Newey–West covariance (denominator n) and a two-sided normal '
        'reference. L=max(H,floor(4*(n/100)^(2/9)))=7. Negative differences favour QR. '
        'No HLN, alternative bandwidth, adjustment family, or additional comparison is reported. '
        'If the helper reports nonpositive LRV, the statistic and p-value remain undefined.', '',
        'The helper is reused unchanged. It also returns its legacy HLN fields internally; '
        'this readback discards those fields and reports only the two requested normal HAC p-values.', '',
        '| Fixed comparison | QR − F mean loss | Change vs F | HAC statistic | Normal two-sided p |',
        '|---|---:|---:|---:|---:|',
    ]
    for c in comparisons:
        stat = 'undefined' if c['HAC_statistic'] is None else format(c['HAC_statistic'], '.12g')
        p = 'undefined' if c['two_sided_normal_HAC_p'] is None else format(c['two_sided_normal_HAC_p'], '.12g')
        lines.append(f"| {c['comparison']} | {c['mean_loss_difference_QR_minus_F']:.12g} | {c['ratio_change_percent']:+.12g}% | {stat} | {p} |")
    lines.extend(['', 'results.json binds the private-archive manifest, retro seal, prior PASS verification, '
        'unchanged inference helper, exact three NPZ hashes and selection/primary identities. '
        'Per-origin arrays and source data remain private; no existing R6 file is changed.', '',
        'Command: `PYTHONDONTWRITEBYTECODE=1 /Users/bingyouli/.cache/codex-runtimes/'
        'codex-primary-runtime/dependencies/python/bin/python3 -B supervisor_r6_hac_readback.py --execute`', ''])
    with (OUTPUT / 'README.md').open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(lines))
    print(json.dumps(dict(output=str(OUTPUT), comparisons=comparisons), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', required=True)
    parser.parse_args()
    run()
