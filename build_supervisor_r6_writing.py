"""Render the writing-stage R6 clarification from existing aggregate outputs only.

No experiments, model fits, forecast generation, or statistical recalculation.
Run after build_supervisor_r6_document.py to update the expanded Table 10.
"""
from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from build_supervisor_r6_document import write_new_or_tracked

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'results/supervisor-20261023/r6'
HAC = ROOT / 'results/supervisor-20261023/r6-writing-hac-20261023'
GENERATED = ROOT / 'manuscript/supervisor-revision/generated'


def read_csv(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def build():
    summary = read_csv(ARCHIVE / 'summary.csv')
    selections = read_csv(ARCHIVE / 'selection.csv')
    primaries = read_csv(ARCHIVE / 'primary-replication.csv')
    comparisons = read_csv(HAC / 'comparisons.csv')
    assert len(comparisons) == 2 and all(r['status'] == 'OK' for r in comparisons)
    matched, original = comparisons
    assert matched['comparison'] == 'matched_frozen_F2880_d24'
    assert original['comparison'] == 'original_primary_rolling_F720_d1'
    weekly = [r for r in summary if r['phase'] == 'retro' and r['source'] == 'nyfed_weekly']
    r2 = [r for r in weekly if r['report'] == 'R2']
    selected = [r for r in selections if r['phase'] == 'retro'
                and r['source'] == 'nyfed_weekly' and r['rule'] == 'R2']
    counts = {int(r['origin_count']) for r in weekly}
    assert len(counts) == 1 and len(selected) == len(r2)
    worst = max(r2, key=lambda r: float(r['percent_vs_F']))
    assert worst['series_key'] == 'PDPOSGS-B' and int(worst['horizon']) == 24
    treasury = next(r for r in primaries if r['source'] == 'nyfed_weekly')
    design_path = ROOT / 'protocol/supervisor-20261023/r6-design.md'
    design_text = design_path.read_text()
    date_match = re.search(r'8999–10438; (\S+) 至 (\S+) \|', design_text)
    first, last = [datetime.fromisoformat(v[:10].replace('.', '-') + v[10:])
                   for v in date_match.groups()]
    weeks = round((last - first).total_seconds() / (7 * 86400))
    facts = {
        'RWritingMatchedGain': f"{-float(matched['ratio_change_percent']):.1f}",
        'RWritingOriginalExcess': f"{float(original['ratio_change_percent']):.1f}",
        'RWritingTreasuryExcess': f"{float(treasury['percent_vs_reference']):.1f}",
        'RWritingISelected': str(sum(r['selected_id'] == 'I' for r in selected)),
        'RWritingWeeklyCells': str(len(r2)),
        'RWritingWeeklyN': str(next(iter(counts))),
        'RWritingFXN': f"{int(matched['n']):,}",
        'RWritingFXWeeks': str(weeks),
        'RWritingHACL': matched['L'],
        'RWritingMatchedP': format(float(matched['two_sided_normal_HAC_p']), '.2e')
            .replace('e-05', r'\times10^{-5}'),
        'RWritingOriginalP': f"{float(original['two_sided_normal_HAC_p']):.3f}",
    }
    write_new_or_tracked(GENERATED / 'r6-writing-facts.tex',
        '% Generated from archived aggregates; see r6-writing-provenance.json.\n' +
        ''.join('\\newcommand{\\' + k + '}{' + v + '}\n' for k, v in facts.items()))
    lines = [r'\begin{table}[htbp]', r'\centering\small',
        r'\begin{tabular}{p{.25\linewidth}p{.27\linewidth}rrr}', r'\toprule',
        r'Earlier six-step structure & Historical reference & Origins & $\Delta$ (\%) & HAC $p$ \\',
        r'\midrule',
        'Treasury QR, $W=52$ analogue & Frozen $F_{52}$, $d=13$ & ' +
        facts['RWritingWeeklyN'] + ' & ' + f"{float(treasury['percent_vs_reference']):+.1f}" + r' & --- \\',
        'FX QR, $W=2880$ & Frozen $F_{2880}$, $d=24$ & ' + facts['RWritingFXN'] +
        ' & ' + f"{float(matched['ratio_change_percent']):+.1f}" + ' & $' +
        facts['RWritingMatchedP'] + r'$ \\',
        'FX QR, $W=2880$ & Rolling $F_{720}$, $d=1$ & ' + facts['RWritingFXN'] +
        ' & ' + f"{float(original['ratio_change_percent']):+.1f}" + ' & ' +
        facts['RWritingOriginalP'] + r' \\',
        r'\bottomrule', r'\end{tabular}',
        r'\caption{Earlier-period QR comparisons. $\Delta$ is mean pinball relative to the stated '
        r'reference; positive is worse. Weekly cells each have \RWritingWeeklyN{} evaluation origins; '
        r'the common FX block has \RWritingFXN{} origins (about \RWritingFXWeeks{} calendar weeks). '
        r'The original three-penalty menu selects $\lambda=\RTreasuryPrimarySelected{}$ for Treasury '
        r'and $\lambda=\RFXPrimarySelected{}$ for FX; both FX rows use the same QR reports, not R2. '
        r'Two-sided normal HAC $p$ values are later descriptive readbacks, with $L=\RWritingHACL{}$ '
        r'under Section~5\textquotesingle s rule, without multiplicity adjustment or control for '
        r'the whole selection/inspection process. Treasury is a $W=52$ structural analogue, '
        r'not exact replication of the original $W=260$ primary.}\label{tab:r6-primary}',
        r'\end{table}', '']
    # Avoid relying on an additional text-companion symbol package.
    table = '\n'.join(lines).replace(r'Section~5\textquotesingle s rule', r'the Section~5 rule')
    write_new_or_tracked(GENERATED / 'r6-primary-table.tex', table)
    inputs = [ARCHIVE / n for n in ['summary.csv', 'selection.csv', 'primary-replication.csv']]
    inputs += [HAC / 'comparisons.csv', HAC / 'results.json', design_path]
    provenance = {
        'scope': 'Document reader only; no new experiment or recomputation of results.',
        'inputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        'facts': facts, 'FX_calendar_first': first.isoformat(), 'FX_calendar_last': last.isoformat(),
        'worst_R2_weekly_cell': worst,
        'pointers': {
            'gain_and_p': 'r6-writing-hac-20261023/comparisons.csv:two fixed QR comparisons',
            'I_selected': 'r6/selection.csv:retro/nyfed_weekly/R2/selected_id=I',
            'weekly_n_and_worst': 'r6/summary.csv:retro/nyfed_weekly',
            'Treasury': 'r6/primary-replication.csv:Treasury-W52-structural-analogue',
            'calendar_weeks': 'r6-design.md:fixed FX evaluation dates; rounded elapsed calendar weeks',
        },
    }
    write_new_or_tracked(ROOT / 'notes/supervisor-20261023/r6-writing-provenance.json',
                        json.dumps(provenance, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(facts, ensure_ascii=False))


if __name__ == '__main__':
    build()
