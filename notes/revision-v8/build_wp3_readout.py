"""Write a source-bound WP3 readout; no draws, forecasts or new tests."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/revision-v8/wp3'


def read(name):
    return json.loads((BASE / name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, text):
    with path.open('x') as stream:
        stream.write(text)


def main():
    inputs = ['manifest.json', 'inventory.json', 'summary.json', 'support.json',
              'study-termination.json']
    hashes = {name: sha(BASE / name) for name in inputs}
    manifest, inventory, summary, support, termination = [read(name) for name in inputs]
    audit_path = ROOT / 'notes/revision-v8/wp3-independent-audit.json'
    audit = json.loads(audit_path.read_text())
    assert audit['status'] == 'PASS' and audit['input_hashes'] == hashes
    assert termination['all_workers_terminated']
    cells = summary['cells']
    candidates = Counter(c['status'] for r in inventory for c in r['candidates'])
    failed = [dict(identity={k: r[k] for k in
        ('rep', 'phi', 'variance_persistence', 'window', 'horizon', 'method')},
        candidate=c, procedure_status=r['status'],
        selected_penalty=r['selected_penalty'])
        for r in inventory for c in r['candidates'] if c['status'] != 'COMPLETE']
    output = dict(generated_utc=datetime.now(timezone.utc).isoformat(),
        source_hashes=hashes, candidate_status_counts=dict(candidates),
        failed_candidates=failed, scientific_screen=support,
        resources=audit['resources'], study_elapsed_seconds=termination['elapsed_seconds'],
        method_status_counts=termination['method_status_counts'])
    save(BASE / 'readout-bindings.json', json.dumps(output, indent=2) + '\n')
    names = dict(F='Historical headroom', QR33='33-feature quantile regression',
                 QR4='Four-feature quantile regression')
    lines = ['# Complete WP3 simulation summaries', '',
        'Generated from the unchanged saved summaries. Full precision, missingness '
        'fields and denominator details remain in `summary.csv` and `summary.json`. '
        'All candidate and method receipts, including failures, are retained in '
        '`wp3-driver-output.tar.gz`; see its complete member index. This table '
        'rounds for display only. Loss uses simulated position units. Relative loss '
        'is the ratio of repetition-mean losses against same-cell F, not a mean '
        'of within-repetition percentage ratios.', '']
    for method, name in names.items():
        lines += ['## ' + name, '',
            '| Level persistence | Variance persistence | History | Horizon | Complete / planned | Mean loss | Relative loss % (MCSE) | Breach % (MCSE) | Strict win % (MCSE) |',
            '|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        def pair(row, value, se, scale=1):
            if row[value] is None or row[se] is None:
                return 'NA'
            return f'{scale*row[value]:.3f} ({scale*row[se]:.3f})'
        for r in cells:
            if r['method'] != method:
                continue
            values = [f"{r['phi']:g}", f"{r['variance_persistence']:g}",
                str(r['window']), str(r['horizon']),
                f"{r['complete_repetitions']} / {r['planned_repetitions']}",
                f"{r['mean_model_loss']:.6f}" if 'mean_model_loss' in r else 'NA',
                pair(r, 'relative_loss_percent', 'relative_loss_mcse'),
                pair(r, 'model_breach_rate', 'model_breach_mcse', 100),
                pair(r, 'win_fraction', 'win_mcse', 100)]
            lines.append('| ' + ' | '.join(values) + ' |')
        lines.append('')
    lines += ['F is paired with itself: its zero relative loss and zero strict-win '
        'fraction are bookkeeping reference values. Win MCSE is plug-in binomial; '
        'a zero at an observed boundary is not certainty. The saved summaries '
        'also give the worst-case bound.', '']
    save(BASE / 'COMPLETE_RESULTS.md', '\n'.join(lines))
    screen_rows = []
    for method, r in support['procedures'].items():
        screen_rows.append(f"| {names[method]} | {r['target_clear_gain_count']} / "
            f"{r['target_cell_count']} | {r['outside_clear_gain_count']} / "
            f"{r['outside_cell_count']} | **{r['status']}** |")
    text = f'''# WP3: frozen level-AR/GARCH mechanism study

**Scientific conclusion: {support['broad_conditional_models_restriction']}.**
The predeclared restriction to short-horizon, long-history, strongly clustered
conditions is contradicted by clear gains outside that region. The historical
empirical pattern cannot be presented as a universal mechanism boundary.
The support rule was not changed after seeing this result.

| Procedure | Clear gains inside target | Clear gains outside target | Frozen classification |
|---|---:|---:|---|
{chr(10).join(screen_rows)}

A clear gain requires all planned paired repetitions, a relative mean-loss
change plus twice its Monte Carlo standard error below zero, and a strict-win
fraction at least the frozen threshold. These are descriptive screens, without
a family-wide significance guarantee. Outside gains include homoskedastic
processes and the longer horizon. Small-history regression losses and excess
breaches remain visible in the full grids. The two regression procedures retain
their different original penalty menus and validation-failure rules; their
comparison is not a pure feature-count intervention.

## Provenance and measured execution

- Design commit: `{manifest['design_commit']}`; protocol bytes are checked
  against that commit before any study draw.
- Study: `{termination['started_utc']}` to `{termination['ended_utc']}`;
  elapsed {termination['elapsed_seconds']:.6f} seconds.
- Worker tasks: {termination['completed_workers']} / {termination['planned_workers']}.
- Complete method tasks: {termination['method_status_counts'].get('COMPLETE', 0)}.
- Candidate statuses: `{json.dumps(dict(candidates), sort_keys=True)}`.
  Candidate failures are retained in `readout-bindings.json` and the full archive.
  A failed eligible-menu candidate does not imply the original QR4 procedure
  failed; no selected evaluation was replaced by another penalty.
- Actual observed peak worker RSS: {audit['resources']['maximum_observed_rss_bytes']} bytes;
  maximum observed OS threads: {audit['resources']['maximum_observed_os_threads']}.
- Independent scalar/provenance audit: `{audit['status']}`,
  {audit['difference_count']} differences. This is arithmetic verification,
  not independent study replication.

## Complete delivery

`summary.csv` / `summary.json` retain every cell and full-precision metric;
`COMPLETE_RESULTS.md` is the complete readable grid. `support.json` records
every target and outside counterexample. `figures/` holds all six saved-summary
heatmaps with Monte Carlo uncertainty, using fixed shading limits and uncapped
numeric annotations. The QR33 loss figure is designated for the main paper;
the other grids and results remain available for the Supplement.

`wp3-driver-output.tar.gz` preserves the original driver manifest, inventory,
status logs, termination, summaries, support screen and every public per-unit
receipt. `wp3-driver-output-members.csv` enumerates every archived byte count
and SHA-256; `wp3-package-receipt.json` records the full archive readback.
The loose unit directory and large inventory remain locally intact and are
excluded from Git only to avoid publishing tens of thousands of tiny files and
an oversized loose JSON. Nothing is dropped from the complete archive.

The archive excludes `.scratch` traces and raw FX observations. For independent
readback, extract its contents into a separate empty directory and point
`notes/revision-v8/audit_wp3.py --formal` there. Re-executing the study requires
a fresh output location and the frozen design commit; version-specific public
reproduction instructions are finalized with the release.
'''
    save(BASE / 'README.md', text)
    source = ROOT / '.scratch/revision-v8/wp3-formal-figures'
    receipt = json.loads((source / 'display-receipt.json').read_text())
    assert receipt['source_sha256'] == hashes['summary.json']
    target = BASE / 'figures'
    target.mkdir(exist_ok=False)
    for row in receipt['figures']:
        for key in ('pdf', 'preview'):
            shutil.copy2(source / row[key], target / row[key])
    for name in ('display-receipt.json', 'captions.md'):
        shutil.copy2(source / name, target / name)
    assert hashes == {name: sha(BASE / name) for name in inputs}
    print(json.dumps(dict(method_tasks=len(inventory), summary_rows=len(cells),
        candidate_status_counts=dict(candidates), scientific_screen=support['broad_conditional_models_restriction'],
        figures=len(receipt['figures']), input_changes=0)))


if __name__ == '__main__':
    main()
