"""Render R6 manuscript facts from the completed, separately archived run.

This reader never imports an experiment, fits a model or changes a result.
All manuscript numbers have a CSV/JSON pointer in the generated provenance.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results/supervisor-20261023/r6'
GENERATED = ROOT / 'manuscript/supervisor-revision/generated'
NOTES = ROOT / 'notes/supervisor-20261023'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value):
    if value in (None, ''):
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def formatted(value, places=1, signed=False):
    value = finite(value)
    if value is None:
        return 'unavailable'
    return format(value, ('+' if signed else '') + '.' + str(places) + 'f')


def write_new_or_tracked(path, text):
    """Back up a pre-existing untracked target before a requested regeneration."""
    import subprocess
    if path.exists():
        tracked = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', str(path.relative_to(ROOT))],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        ).returncode == 0
        if not tracked:
            backup = path.with_name(path.name + '.bak')
            if backup.exists():
                raise FileExistsError(backup)
            with backup.open('xb') as stream:
                stream.write(path.read_bytes())
    path.write_text(text, encoding='utf-8')


def build():
    summary_path = RESULTS / 'summary.csv'
    assessment_path = RESULTS / 'assessment.json'
    primary_path = RESULTS / 'primary-replication.csv'
    design_path = ROOT / 'protocol/supervisor-20261023/r6-design.md'
    rows = list(csv.DictReader(summary_path.open()))
    assessment = json.loads(assessment_path.read_text())
    contract = json.loads(re.findall(r'```json\s*([\s\S]*?)```',
                                    design_path.read_text())[-1])
    loss_threshold = contract['success']['S1']['worst_percent_vs_F_max']
    retro = [row for row in rows if row['phase'] == 'retro']
    # The runner declares these exact report IDs; absence remains visible.
    reports = ['F', 'I', 'R0', 'R1', 'R2', 'R3']
    weekly = {}
    for report in reports:
        selected = [row for row in retro
                    if row['source'] == 'nyfed_weekly' and row['report'] == report]
        values = [finite(row['percent_vs_F']) for row in selected]
        complete = [v for row, v in zip(selected, values)
                    if row['status'] == 'COMPLETE' and v is not None]
        weekly[report] = dict(
            expected=len(selected), complete=len(complete),
            median=statistics.median(complete) if complete else None,
            worst=max(complete) if complete else None,
            over_25=sum(v > loss_threshold for v in complete),
            wins=sum(v < 0 for v in complete),
            scope='descriptive completed cells; failures remain in summary.csv',
        )

    facts = {}
    pointers = {}

    def fact(name, value, pointer, places=1, signed=False):
        facts[name] = formatted(value, places, signed)
        pointers[name] = pointer

    for report, values in weekly.items():
        names = dict(F='F', I='I', R0='Zero', R1='One', R2='Two', R3='Three')
        for key, suffix in [('median', 'Median'), ('worst', 'Worst'),
                            ('complete', 'Complete'), ('over_25', 'LargeLosses'),
                            ('wins', 'Wins')]:
            fact('RWeekly' + names[report] + suffix, values[key],
                 'summary.csv: retro/nyfed_weekly/' + report + '/' + key,
                 places=0 if key in ('complete', 'over_25', 'wins') else 1,
                 signed=key in ('median', 'worst'))
    for criterion in ['S1', 'S2', 'S3']:
        name = dict(S1='ROneStatus', S2='RTwoStatus', S3='RThreeStatus')[criterion]
        facts[name] = assessment[criterion]['status'].replace('_', r'\_')
        pointers[name] = 'assessment.json:/' + criterion + '/status'

    for row in retro:
        if row['source'] == 'fx_hourly' and int(row['horizon']) == 6:
            window = dict({720: 'Short', 2880: 'Long'})[int(row['window'])]
            report = dict(F='F', I='I', R0='Zero', R1='One', R2='Two', R3='Three')[row['report']]
            fact('RFX' + window + report + 'Change', row['percent_vs_F'],
                 f"summary.csv:retro/fx_hourly/H6/W{row['window']}/{row['report']}",
                 signed=True)

    primary_rows = list(csv.DictReader(primary_path.open()))
    primary_names = {'FX-original-structure': 'RFXPrimary',
                     'Treasury-W52-structural-analogue': 'RTreasuryPrimary'}
    for row in primary_rows:
        prefix = primary_names[row['id']]
        fact(prefix + 'Change', row['percent_vs_reference'],
             'primary-replication.csv:' + row['id'] + '/percent_vs_reference', signed=True)
        facts[prefix + 'Selected'] = row['selected_id'] or 'unavailable'
        pointers[prefix + 'Selected'] = 'primary-replication.csv:' + row['id'] + '/selected_id'

    facts_text = '% Generated only from archived R6 CSV/JSON; see r6-document-provenance.json.\n'
    facts_text += ''.join('\\newcommand{\\' + key + '}{' + value + '}\n'
                          for key, value in facts.items())
    write_new_or_tracked(GENERATED / 'r6-facts.tex', facts_text)

    lines = [r'\begin{table}[htbp]', r'\centering\small',
             r'\begin{tabular}{lrrrr}', r'\toprule',
             r'Rule & Complete & Median $\Delta$ (\%) & Worst $\Delta$ (\%) & $\Delta>25\%$ \\',
             r'\midrule']
    for report in reports:
        v = weekly[report]
        lines.append(f"{report} & {v['complete']}/{v['expected']} & "
                     + formatted(v['median'], signed=True) + ' & '
                     + formatted(v['worst'], signed=True) + ' & '
                     + str(v['over_25']) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}',
              r'\caption{R6 retrospective weekly comparisons with same-window, same-update frozen $F$. '
              r'$\Delta$ is the percentage change in mean pinball loss; positive values are worse. '
              r'Cell summaries are descriptive across related series and horizons, not independent replications. '
              r'All rule cells, including failures, are retained in the public R6 archive.}\label{tab:r6-selection}',
              r'\end{table}', '']
    write_new_or_tracked(GENERATED / 'r6-summary-table.tex', '\n'.join(lines))

    lines = [r'\begin{table}[htbp]', r'\centering\small',
             r'\begin{tabular}{p{.31\linewidth}p{.29\linewidth}rr}', r'\toprule',
             r'Retrospective structure & Historical reference & Selected $\lambda$ & $\Delta$ (\%) \\',
             r'\midrule']
    for row in primary_rows:
        is_fx = row['source'] == 'fx_hourly'
        name = ('FX QR, $W=' + str(row['window']) + '$') if is_fx else (
            'Treasury bill QR, $W=' + str(row['window']) + '$ analogue')
        reference = r'Rolling $F$, $W=720$, $d=1$' if is_fx else r'Frozen $F$, $W=52$, $d=13$'
        selected = row['selected_id'] or 'unavailable'
        lines.append(name + ' & ' + reference + ' & ' + selected + ' & '
                     + formatted(row['percent_vs_reference'], signed=True) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}',
              r'\caption{Original comparison structures on the R6 retrospective six-step origins, '
              r'with the original three-penalty menu retuned on the earlier validation segment. '
              r'$\Delta$ is QR mean pinball relative to the stated reference; positive is worse. '
              r'The Treasury row is a short-window structural analogue, not an exact replication '
              r'of the original $W=260$ primary. Original primaries remain unchanged.}\label{tab:r6-primary}',
              r'\end{table}', '']
    write_new_or_tracked(GENERATED / 'r6-primary-table.tex', '\n'.join(lines))

    provenance = dict(
        inputs={str(p.relative_to(ROOT)): sha(p)
                for p in [summary_path, assessment_path, primary_path, design_path]},
        facts=facts, pointers=pointers, weekly_descriptive=weekly,
        publication_gate=assessment['publication_gate'],
        note='Reader only; no fitting, forecasts, original-result edits or pooled inference.',
    )
    write_new_or_tracked(NOTES / 'r6-document-provenance.json',
                        json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(provenance, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
