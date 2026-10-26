"""Source-bound daily-result tables and interpretation; no forecasting."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/revision-v8/wp4'
NAMES = {'F': 'Historical headroom', 'QR33': '33-feature regression',
         'QR4': 'Four-feature regression'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, text):
    with (BASE / name).open('x') as stream:
        stream.write(text)


def main():
    audit = json.loads((ROOT / 'notes/revision-v8/wp4-independent-audit.json').read_text())
    assert audit['status'] == 'PASS' and audit['difference_count'] == 0
    assert all(sha(BASE / p) == h for p, h in audit['input_hashes'].items())
    summary = json.loads((BASE / 'summary.json').read_text())
    manifest = json.loads((BASE / 'manifest.json').read_text())
    termination = json.loads((BASE / 'study-termination.json').read_text())
    rows = summary['cells']; contrasts = summary['contrasts']
    metadata = summary['source_consistency']['daily_metadata']
    source_cell = next(iter((BASE / 'cells').iterdir()))
    source = json.loads((source_cell / 'worker-source.json').read_text())
    mapping = Path(manifest['private_directory']) / source_cell.name / 'daily-series.npz'
    mapping.resolve().relative_to((ROOT / '.scratch').resolve())
    assert sha(mapping) == source['daily_mapping_sha256']
    with np.load(mapping, allow_pickle=False) as arrays:
        times = arrays['times'].copy()
    design = manifest['design']; sample = design['sample']
    first = sample['evaluation_first']; last = len(times) - 1 - max(design['clock_and_target']['horizons'])
    stamp = lambda i: str(np.datetime_as_string(times[i], unit='us'))
    periods = dict(validation_first=stamp(sample['validation_first']),
        validation_last=stamp(sample['validation_last']),
        validation_last_target_max_horizon=stamp(sample['validation_last'] + max(design['clock_and_target']['horizons'])),
        evaluation_first=stamp(first), evaluation_last=stamp(last),
        evaluation_last_target_max_horizon=stamp(len(times)-1),
        evaluation_count=last-first+1)
    lookup = {(r['window'], r['horizon'], r['method']): r for r in contrasts}
    candidates = Counter(c['status'] for r in rows for c in r['candidates'])
    classes = summary['classifications']
    examples = [r for c in classes.values() for r in c['literal_hourly_counterexamples']]
    bindings = dict(generated_utc=datetime.now(timezone.utc).isoformat(),
        source_hashes=audit['input_hashes'], daily_metadata=metadata,
        periods=periods, candidate_status_counts=dict(candidates),
        classifications=classes, counterexamples=examples,
        original_raw_and_private_mapping_redistributed=False)
    save('readout-bindings.json', json.dumps(bindings, indent=2) + '\n')
    md = ['# Complete same-dealer daily FX results', '',
        'All numbers are generated from the unchanged saved summaries. Loss is in '
        'source-reported USD; CSV/JSON retain full precision. This is a post-result '
        'within-dealer aggregation contrast, with no new significance test.', '',
        '| History | Horizon | Procedure | Selected penalty | Evaluation issues | Mean loss (USD) | Strict breaches | Breach % | Loss change vs matched F % |',
        '|---:|---:|---|---:|---:|---:|---:|---:|---:|']
    tex = [r'\begingroup\small\setlength{\tabcolsep}{3pt}',
        r'\begin{longtable}{rrlrrrr}',
        r'\caption{Same-dealer daily sampled-position results. History and horizon count recorded nonempty calendar days. All methods share the declared evaluation grid; loss is scaled to USD millions for display only. The isolated parsimonious score gain has more breaches than its historical reference.}\label{tab:daily-fx}\\',
        r'\toprule',
        r'History & Horizon & Procedure & Penalty & \shortstack{Mean loss\\(USD m)} & \shortstack{Loss change\\vs historical (\%)} & \shortstack{Breaches\\count / rate (\%)}\\\midrule',
        r'\endfirsthead',
        r'\caption[]{Continued.}\\\toprule',
        r'History & Horizon & Procedure & Penalty & \shortstack{Mean loss\\(USD m)} & \shortstack{Loss change\\vs historical (\%)} & \shortstack{Breaches\\count / rate (\%)}\\\midrule',
        r'\endhead', r'\bottomrule\endfoot']
    for r in rows:
        e = r['evaluation']; c = lookup.get((r['window'], r['horizon'], r['method']))
        penalty = '--' if r['selected_penalty'] is None else f"{r['selected_penalty']:g}"
        change = '--' if c is None or c['relative_loss_percent'] is None else f"{c['relative_loss_percent']:.3f}"
        md.append('| ' + ' | '.join([str(r['window']), str(r['horizon']), NAMES[r['method']],
            penalty, str(e['n']), repr(e['mean_loss']), str(e['strict_breach_count']),
            f"{100*e['strict_breach_rate']:.3f}", change]) + ' |')
        tex.append(f"{r['window']} & {r['horizon']} & {NAMES[r['method']]} & {penalty} & "
            f"{e['mean_loss']/1_000_000:.3f} & {change} & {e['strict_breach_count']} / "
            f"{100*e['strict_breach_rate']:.3f}" + r'\\')
    tex += [r'\end{longtable}', r'\endgroup', '']
    save('COMPLETE_RESULTS.md', '\n'.join(md) + '\n')
    save('daily-results-table.tex', '\n'.join(tex))
    historical = sum(c['historical_wins'] for c in classes.values())
    complete = sum(c['complete_comparisons'] for c in classes.values())
    example_text = []
    for ex in examples:
        c = lookup[(ex['window'], ex['horizon'], ex['method'])]
        e = next(r['evaluation'] for r in rows if
            (r['window'], r['horizon'], r['method']) == (ex['window'], ex['horizon'], ex['method']))
        ref = next(r['evaluation'] for r in rows if
            (r['window'], r['horizon'], r['method']) == (ex['window'], ex['horizon'], 'F'))
        example_text.append(f"- {NAMES[ex['method']]}, W{ex['window']}/H{ex['horizon']}: "
            f"loss change {c['relative_loss_percent']:.6f}%; strict breaches "
            f"{e['strict_breach_count']} versus {ref['strict_breach_count']} for matched F.")
    readme = f'''# WP4: same-dealer daily aggregation

The frozen finite-record classifications are **{classes['QR33']['status']}**
for the original regression and **{classes['QR4']['status']}** for the
four-feature regression. Historical headroom wins {historical} of {complete}
complete named comparisons. Original regression historical wins:
{classes['QR33']['historical_wins']} / {classes['QR33']['planned_comparisons']};
four-feature historical wins: {classes['QR4']['historical_wins']} /
{classes['QR4']['planned_comparisons']}. The complete table retains the exception:

{chr(10).join(example_text)}

## Observation and interpretation boundaries

The exact accepted {metadata['n_original']}-row file produces
**{metadata['n_daily']} nonempty source-naive calendar days**, rather than the
instruction's rough780-day expectation (**MISMATCH-WP4-02**). Every nonempty
day, including partial boundary days, remains under the frozen last-record
rule. No weekday filter or deletion was introduced to reach an expected count.
The report clock is the completed day's23:59:59.999999; this is a last-record
proxy, not a reconstruction of an actual financial market close or intraday peak.
The original timestamp timezone and historical release vintage remain unknown.

Validation: {periods['validation_first']} through {periods['validation_last']}.
Evaluation: {periods['evaluation_first']} through {periods['evaluation_last']},
{periods['evaluation_count']} common issues. The original Treasury absolute2021
dates cannot be shared with this record; the predeclared adaptation carries
over its observation-index geometry (**MISMATCH-WP4-01**).

The same recorded dealer now yields a largely historical-rule-favoring pattern,
so source identity alone cannot describe all the rankings. Physical horizons,
physical histories, update cadence, calendar predictors and sampled targets
change jointly. This does not identify a pure frequency effect or prove a
source-only explanation; it supplies no independent-dealer or prospective
validation. The daily parsimonious gain also contradicts a literal hourly-only
description of conditional gains (**MISMATCH-WP4-03**), while its higher breach
count prevents equating a lower score with a safer limit.

## Decision-map consequence

Add a same-dealer daily row: historical score wins predominate at the executed
histories/horizons, retain the named parsimonious exception and assess its
breaches jointly. Short-history historical F itself also has substantial
breach frequencies; historical score superiority is not a nominal-coverage
guarantee. Keep the hourly/weekly evidence and every adverse daily cell.

## Verification and full record

- Design commit: `{manifest['design_commit']}`.
- Unique actual run: {termination['elapsed_seconds']:.6f}s;
  {termination['completed_workers']} / {termination['planned_workers']} workers;
  {len(rows)} method slots; {sum(candidates.values())} declared validation candidates.
- Candidate statuses: `{json.dumps(dict(candidates), sort_keys=True)}`.
- Independent readback: {audit['status']}, {audit['difference_count']} differences;
  {audit['complete_trace_scores_checked']} complete score traces and
  {audit['fit_maturity_records_checked']} mature-refit records checked.
- Actual maximum worker RSS: {audit['resources']['maximum_observed_rss_bytes']}B;
  maximum observed OS threads: {audit['resources']['maximum_observed_os_threads']}.

`summary.json/csv`, `contrasts.csv`, `classification.json`, all four cell
receipts and `readout-bindings.json` preserve the complete aggregation and
comparison record. `daily-results-table.tex` is generated from those source
fields for later manuscript integration. No model or inferential test is added
by this readout. Raw/daily observations and per-issue NPZ arrays stay in task
scratch; their hashes support local audit without redistribution.
'''
    save('README.md', readme)
    assert all(sha(BASE / p) == h for p, h in audit['input_hashes'].items())
    print(json.dumps(dict(method_rows=len(rows), contrasts=len(contrasts),
        daily_rows=metadata['n_daily'], evaluation_issues=periods['evaluation_count'],
        historical_wins=historical, complete_comparisons=complete,
        source_input_changes=0)))


if __name__ == '__main__':
    main()
