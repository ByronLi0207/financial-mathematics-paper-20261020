"""v10b document-only supplement edit; never imports financial code."""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / 'submission-v10/supplement.tex'
original = p.read_text()
s = original
removed = []

def move(title, old, new, reason):
    global s
    assert s.count(old) == 1, (title, s.count(old))
    removed.append(dict(title=title, original_tex=old, replacement_tex=new, reason=reason))
    s = s.replace(old, new)

s = s.replace(r'\renewcommand{\thetable}{S\arabic{table}}', r'\renewcommand{\thetable}{S\arabic{table}}' + '\n' + r'\renewcommand{\thefigure}{S\arabic{figure}}')
move('Opening: document binding and builder',
'''Different source-reported monetary units are not pooled. NA and failed rows
remain distinct from complete results. The exact binding file and document
builder permit source-field readback without re-running any financial model.''',
'''Different source-reported monetary units are not pooled. NA and failed rows
remain distinct from complete results.''',
'Keep units and missing-result semantics; move document-generation verification metadata.')
move('S2: source-consultation audit',
'''maximal inequality. The existing source audit identifies Sussman (2023),
Proposition 3.4, and records the actual consulted source range.''',
'''maximal inequality; see Sussman (2023), Proposition 3.4.''',
'Keep attribution in the proof; move the administrative description of consulted-source records.')
move('S7: numerical readback receipt',
'''These are post-result / exploratory same-data calculations, not independent
validation. Numerical readback checked the represented-input recursion and
saved summaries without validating the financial innovation law.''',
'''These are post-result / exploratory same-data calculations, not independent
validation.''',
'Retain post-result status and validation boundary; move the performed readback receipt.')
move('S12: independent arithmetic check entry point',
'''The independent saved-array arithmetic checks and selection-before-
evaluation records are linked from \\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/supervisor-20261023/e5/README.md}{the E5 archive}. The original panel's entire candidate/status inventory remains in''',
'''The expanded-menu selection precedes its evaluation, as documented in \\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/supervisor-20261023/e5/README.md}{the E5 archive}. The original panel's entire candidate/status inventory remains in''',
'Retain the selection-before-evaluation chronology and archive link; move the arithmetic-check receipt.')
move('S21: selection and evaluation receipts',
'''The existing selection freezes and chronological evaluation receipts remain
linked in \\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp5-tau-summary.json}{the target-level inventory}.''',
'''The fixed target-specific selections precede their evaluation; full settings
and results remain in \\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp5-tau-summary.json}{the target-level inventory}.''',
'Keep chronology and technical inventory link; move the description of administrative receipts.')
move('S23: document implementation evidence',
'''\\paragraph{Complete implementation evidence.}
Exact menus, numerical tolerances, failures and diagnostic tables remain in
\\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/EXTENDED_RESULTS.md}{EXTENDED RESULTS} and the dated source archives.
The separate study receipts identify the executed additions. This document
builder imports no forecasting code and only formats unchanged public results.
''',
'''Exact menus, numerical tolerances, failures and diagnostic tables remain in
\\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/EXTENDED_RESULTS.md}{EXTENDED RESULTS} and the dated source archives.
''',
'Retain technical specifications and failures; move study-receipt and document-builder assertions.')
move('S24: archived receipt and duplicate heatmap routing',
'''precision in \\path{results/revision-v8/wp3/summary.json}; all six loss, breach and
win heatmaps and the complete receipt archive remain alongside them.

The duplicate four-feature loss heatmap is available with the six complete
archived heatmaps. Both complete numerical grids above retain every cell.''',
'''precision in \\path{results/revision-v8/wp3/summary.json}; all six loss, breach and
win heatmaps remain alongside them. Both complete numerical grids retain every cell.''',
'Retain all simulation/failure quantities and scientific grid access; move duplicate-display routing and receipt-archive metadata.')
move('S25: raw-data fingerprint and private mapping routing',
'''2015-05-24 to 2016-12-27 on 501 common issues. The exact accepted raw fingerprint and
private resampling mapping are recorded separately; raw or resampled positions
and per-issue trajectories are not redistributed.''',
'''2015-05-24 to 2016-12-27 on 501 common issues. Raw or resampled positions
and per-issue trajectories are not redistributed.''',
'Keep dates, sample count and availability boundary; move private mapping/fingerprint record location.')
move('S30: acquisition transport provenance',
'''The source is the CFTC TFF futures-only historical backcast for 2006--2016 plus annual 2017--2026 files. The retained observations begin in 2010. Each of eleven archives has its exact official URL, request and completion UTC, byte length and SHA-256 in \\texttt{data/cftc-tff/provenance.json}. No other new financial data were acquired. The original archive bytes remain public. The browser API did not expose HTTP status or redirect-chain metadata; those fields are explicitly unobserved.''',
'''The source is the CFTC TFF futures-only historical backcast for 2006--2016 plus annual 2017--2026 files. The retained observations begin in 2010. All eleven original source archives remain public; no other new financial data were acquired.''',
'Keep source family, years, scope and public availability; move request timestamps, bytes, hashes and browser transport limitations. Economic-date and first-release limitations remain below.')
move('S34: public artifact binding details',
'''\\paragraph{What is public.}
Editable sources, aggregate results, original designs, code and verification
records accompany the paper. Favourable, adverse and failed outputs remain
unchanged, with longer tables linked rather than removed. Source-field
bindings identify every printed aggregate.''',
'''Editable sources, aggregate results, original designs and code accompany the
paper; favourable, adverse and failed outputs remain accessible.''',
'Retain availability and adverse-result access; move audit-record and source-field-binding descriptions.')
move('S34: public-check receipt interpretation',
'''\\paragraph{What public checking proves.}
Archive checking and document regeneration verify saved aggregates without raw
observations. They establish artifact consistency, not recomputed forecast
accuracy, a new sample, independent replication or journal acceptance.''',
'''Document regeneration checks saved aggregates without raw observations; it
does not establish recomputed forecast accuracy or independent replication.''',
'Retain the distinction between artifact checking and scientific validation; move redundant administrative qualification.')
start = s.index('\\paragraph{Version-specific entry points.}')
end = s.index('\\paragraph{Routes to complete evidence.}', start)
move('S34: version-specific entry points and resources', s[start:end], '',
     'Move historical path/identity gates, prospective parameter-binding maintenance, local assembly, worker time/memory/threads and test isolation records; no forecasting design or result is removed.')

# Native TOC keeps all scientific section numbers and does not list table continuations.
anchor = '\\section{Known-floor projection and strict quantile coverage}'
toc = r'''\begingroup
\small
\setlength{\parskip}{0pt}
\setcounter{tocdepth}{1}
\makeatletter
\renewcommand*\l@section[2]{\@dottedtocline{1}{0em}{2.5em}{#1}{#2}}
\makeatother
\tableofcontents
\endgroup
\medskip
'''
assert s.count(anchor) == 1
s = s.replace(anchor, toc + anchor)

# Move the technical cost definition into the supplement as well as its main-text summary.
cost_anchor = '\\section{Fixed limit costs and full parameter regions}\\label{sup:v10-cost}\n'
cost = r'''For each comparison, let $B$ be the issue-known floor, $Y$ the realized sampled peak,
$C_m$ a saved method report, and $m_F=\overline{C_F-B}>0$ the matched F report's
mean reserved headroom. All four quantities use the same source-native position
units (currency or contract counts). The normalized per-issue cost is
\[
J_m(\kappa,\beta,c)=\kappa\frac{\overline{C_m-B}}{m_F}
+\beta\,\overline{\mathbf 1\{Y>C_m\}}
+c\frac{\overline{(Y-C_m)_+}}{m_F},\qquad b=\beta m_F.
\]
Reserve, strict breach frequency and excess enter separately. The fixed breach
charge $b$ is in those same position-value units; each $\beta$ scales it to that
comparison's evaluation-sample F headroom. Charges therefore differ across
comparisons. Costs apply per issued report; overlapping horizons are not
added as separate cash flows.
The fixed grid is $\kappa\in\{.01,.025,.05,.1,.2,.5,1\}$,
$\beta\in\{0,.01,.05,.1,.25,.5,1,2,5\}$ and $c\in\{.5,1,2\}$.
At $\kappa=.05,\beta=0,c=1$, the cost difference from F is the pinball-loss
difference divided by $m_F$. Other weights need not preserve that ranking.
The panels compare fixed reports and do not estimate a cost-optimal policy.

'''
assert s.count(cost_anchor) == 1
s = s.replace(cost_anchor, cost_anchor + cost)
s = s.replace('\\clearpage\n' + cost_anchor, cost_anchor)
s = s.replace('\\clearpage\n\\section{Paired menu isolation:', '\\section{Paired menu isolation:')
s = s.replace("The main formula uses each matched F's mean reserved headroom. All 98 comparisons", "All 98 comparisons")
s = s.replace('F/I,2/98', 'F/I, 2/98').replace('and4/98', 'and 4/98')
repro_anchor = '\\section{Reproduction, availability and retained extended results}\\label{sup:reproduction}\n'
s = s.replace(repro_anchor, repro_anchor + '\n' + r'Audit and run records are retained verbatim in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v10b/notes/v10b/supplement-audit-records.md}{v10b audit archive}.' + '\n')
eligibility_anchor = 'Seventeen of 141 observed codes qualify; the top-twenty cap never changes that count.\n'
s = s.replace(eligibility_anchor, eligibility_anchor + r'The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v10b/results/v10/cftc/eligibility.json}{complete code-level eligibility and exclusions} preserve every screening decision.' + '\n')

assert s.count('\\section{') == original.count('\\section{') == 35  # includes preamble definition
assert re.findall(r'\\input\{[^}]+\}', s) == re.findall(r'\\input\{[^}]+\}', original)
assert re.findall(r'\\author\{[^}]*\}', s) == re.findall(r'\\author\{[^}]*\}', original)
p.write_text(s)

audit = ROOT/'notes/v10b/supplement-audit-records.md'
header = '''# Supplement audit and run records retained for revision-v10b

This document-only archive preserves verbatim the original TeX passages whose audit/run metadata was moved or shortened in the supplement. Its replacements retain scientific design, results, failure semantics, selection/evaluation chronology, source information dates, and data-availability limits. It is an evidence-navigation record, not new scientific validation.

Branch: [`revision-v10b`](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v10b). Scientific base: `23fd9fa`.

Original supplement source SHA-256: `''' + hashlib.sha256(original.encode()).hexdigest() + '''`.

## Verbatim moved passages
'''
for i, item in enumerate(removed, 1):
    header += f"\n### A{i}. {item['title']}\n\nReason: {item['reason']}\n\n```tex\n{item['original_tex']}\n```\n\nReplacement retained in supplement:\n\n```tex\n{item['replacement_tex'] or '(Moved in full; scientific context remains in the neighboring paragraphs.)'}\n```\n"
audit.write_text(header)
(ROOT/'notes/v10b/supplement-moved-passages.json').write_text(json.dumps(dict(original_source_sha256=hashlib.sha256(original.encode()).hexdigest(), final_source_sha256=hashlib.sha256(s.encode()).hexdigest(), passages=removed), indent=2)+'\n')
print(f'Edited supplement: 34 scientific sections retained; {len(removed)} passage records archived.')
