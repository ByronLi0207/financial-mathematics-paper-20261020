"""Consolidate the v12 article's argument and reuse its unchanged numeric rows."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'submission-final'
TITLE='When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits'
URL='https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/EXTENDED_RESULTS.md'


def main():
    p=DEST/'manuscript.tex';text=p.read_text();original=text
    assert 'sec:history-mechanism' not in text
    old_title='Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits'
    text=text.replace(old_title,TITLE)
    figures=re.findall(r'\\begin\{figure\}.*?\\end\{figure\}',text,re.S)
    assert len(figures)==5
    endpoint=next(f for f in figures if r'\label{fig:example}' in f)
    for f in figures:
        if any(label in f for label in ('fig:v11-history','fig:v10-cftc')):text=text.replace(f,'')
    # Relocate exact table source; no scientific numeric field is changed.
    tables=re.findall(r'\\begin\{table\}.*?\\end\{table\}',text,re.S)
    literature=next(t for t in tables if r'\label{tab:literature}' in t)
    tau=next(t for t in tables if r'\label{tab:v12-tau}' in t)
    text=text.replace(literature,'').replace(tau,'')
    contract=(DEST/'generated/v10-cftc-contracts.tex').read_text()
    text=text.replace(r'\input{generated/v10-cftc-contracts.tex}','')
    moved=[('literature-matrix',literature),('tail-sensitivity-table',tau),('individual-CFTC-table',contract)]
    folder=ROOT/'notes/final-merge/wp4-relocation';records=[]
    with (ROOT/'EXTENDED_RESULTS.md').open('a') as stream:
        stream.write('\n\n# Exact tables relocated from the v12 main article\n\n')
        for name,raw in moved:
            q=folder/(name+'.tex');q.write_text(raw)
            digest=hashlib.sha256(raw.encode()).hexdigest();records.append(dict(name=name,path=str(q.relative_to(ROOT)),sha256=digest,bytes=len(raw.encode())))
            stream.write('## '+name+'\n\nSHA-256 `'+digest+'`. The original source is retained without changing its numerical rows.\n\n```latex\n'+raw+'\n```\n\n')
    intro=r'''
\section{Introduction}\label{sec:intro}

Position limits must cover exposure between reviews. A position that finishes
inside a limit can still breach it earlier, so an endpoint forecast answers a
different question from a forecast of the intervening peak. We study the largest
sampled absolute net position and compare all procedures on that same response.

'''+endpoint+r'''

Conditional models can use recent position states and calendar information to
adapt a limit. Estimating those relationships also uses a finite history, while
a historical rule can be competitive without estimating many slopes. The
practical question is when the extra conditioning improves on an explicit
historical benchmark, rather than whether a complex model fits the past well.

We examine one market maker's FX record and two official dealer reporting
systems. New York Fed reports describe government-securities positions, while
CFTC categories describe aggregate dealer positions in futures markets. Their
economic units and information dates differ, so comparisons keep their own
targets, scales and historical references. Neither weekly system provides a
collection of independent individual dealers.

The central finding is conditional: history, the tested penalty menu and stated
limit costs organize the comparisons, but they do not establish a universally
sufficient history or a uniquely causal explanation. Matched FX gains coexist
with adverse weekly comparisons and with reversals at the longest tested
histories. Historical rules remain a demanding benchmark across these records.

The first contribution is to connect the history-length evidence with an
additional reporting system. Earlier simulations support the registered
short-history and long-history loss-sign predictions, while their universal
simplification claim fails. FX learning curves give a similarly qualified
pattern. The new CFTC extension agrees with the short-history counts but misses
the registered long-history win target and the strict-improvement target.
The combined CFTC verdict is partial agreement, not validation of a universal
history threshold.

The second contribution is to distinguish history from the available procedures.
An expanded penalty menu removes much of a short-history simulation loss, while
financial diagnostics retain both selection errors and losses within the finite
menu. Access to an ordinary historical quantile is part of that expanded menu,
so near-parity performance alone does not establish the value of extra
predictors. Related forecast comparisons leave historical methods alongside
many uneliminated alternatives.

The third contribution is to connect forecast comparisons to stated limit
costs. Reserve amounts, breach frequency and exceedance magnitude enter
separately. Their weights can change which tested report is cheaper, and local
exceptions remain. These are hypothetical preferences rather than measured
funding gains or an evaluated trading intervention.

Matching training-label histories and refit schedules makes the benchmark
explicit. It does not equalize every feature's raw history or every validation
calculation, and it does not isolate a causal feature effect. All observed
failures, unavailable comparisons and inspected-period qualifications remain
part of the evidence.

Section~\ref{sec:target} defines the response, and Section~\ref{sec:results}
reports the forecasting comparisons. Section~\ref{sec:history-mechanism}
connects history, simulation and the CFTC extension. Section~\ref{sec:cost}
adds the stated cost preferences before the validation implications.

\FloatBarrier

'''
    left=text.index(r'\section{Introduction}');right=text.index(r'\section{Related literature}')
    text=text[:left]+intro+text[right:]
    text=text.replace(r'Table~\ref{tab:literature} locates the present peak response, completed labels and matched historical controls.',
        r'The extended literature matrix contrasts the present peak response, completed labels and matched historical controls.')
    start=text.index(r'\subsection{How much history does FX regression need?}')
    end=text.index(r'\subsection{RQ2:',start)
    text=text[:start]+r'''\subsection{History gains depend on the tested range}\label{sec:fx-history}

History sensitivity within the original FX record is not monotone. The full
regression improves over part of the grid and gives back some gain at the
longest history. Section~\ref{sec:history-mechanism} combines both horizon curves
with the simulation and CFTC evidence, retaining every tested window and its
own matched historical reference.

\FloatBarrier

'''+text[end:]
    text=text.replace(r'Table~\ref{tab:v12-tau} shows',r'the retained supplementary tail-sensitivity table shows')
    mechanism=r'''
\section{Why history length matters}\label{sec:history-mechanism}

\subsection{A descriptive coordinate organizes the simulation evidence}

Let the training history contain $W$ completed targets and let the horizon span
$H$ subsequent observations. The earlier discovery study selected the ratio
\[
c=\frac{W}{H+1}
\]
as a descriptive coordinate on its fixed simulation grid. This ratio excludes
the number of coefficients. It is neither a dependence-adjusted effective
sample size nor an identified normalization by model complexity. Estimating a
separate threshold for each method also makes a later constant rescaling within
that method observationally equivalent for the history-region checks.

The discovery first crossing is approximately $106.5$ for full regression.
For four-predictor regression it is approximately $27.3$. The full-regression
fixed-grid interval runs from $27.89$ to $110.71$. The sparse-regression interval
runs from $13.27$ to $107.11$. These ranges condition on the selected coordinate
and simulation grid, omitting uncertainty from choosing that coordinate.
The sparse curve crosses downward more than once, so its first crossing cannot
be a permanently sufficient history bound.

The subsequent registered simulation checks meet the short-history prediction
in $47$ of $48$ cells. The long-history prediction holds in $21$ of $24$ cells.
Those are finite-grid descriptive successes under the declared laws and menus,
rather than independent-cell significance tests. The simpler procedure satisfies
the universal-ordering inequality in $42$ of $48$ cells. All six counterexamples
remain, so the universal simplification claim is not supported.

\subsection{FX curves retain left censoring and long-history reversals}

Figure~\ref{fig:history} retains both regression variants and both FX horizons,
alongside the earlier simulation and financial comparisons. Three identified
financial first crossings fall within the broad transported ranges. Another
curve already favors regression at its shortest tested history, leaving its
first crossing left-censored. A pooled simulation crossing and a crossing at
one fixed financial horizon are different objects. Their agreement does not
identify a horizon-invariant financial threshold.

Both longer-horizon FX curves lose their advantage again at the largest
history. The shorter-horizon full-regression gain also weakens after its best
tested history. These are the previously studied FX observations, including
overlap with earlier comparisons. They establish neither another dealer
replication nor an untouched financial holdout.

\begin{figure}[p]\centering
\includegraphics[width=.98\linewidth,height=.78\textheight,keepaspectratio]{figures/final-unified-history.pdf}
\caption{All earlier conditional-model records and all CFTC comparisons are retained against their own matched historical benchmark. Negative changes favor regression. The upper panels preserve the complete range; the lower panels repeat the same records in a labelled detail range. Eight FX records reuse an earlier period. CFTC is an independent reporting source of aggregate, potentially dependent markets; its shorter-history outcomes were already inspected. Shading summarizes the original simulation crossings conditional on the chosen grid and coordinate, without accounting for coordinate selection. History alone does not guarantee a gain.}\label{fig:history}
\end{figure}

\subsection{CFTC meets the short-history count but misses the long-history target}

The CFTC extension fixes the earlier thresholds before adding a training
history of $520$ weeks. Both shorter-history predictions reuse their unchanged
saved reports. The universe, validation period, evaluation dates, candidate
menus and refit schedule remain the inherited design. Completed training labels
end no later than each refit, and every validation label finishes before the
evaluation begins. Downloaded economic-date vintages remain distinct from
historically available first releases.

For the full procedure, the low-history region contains $34$ planned
market-history comparisons. It loses to matched historical headroom in $29$.
The sparse procedure loses in $15$ of $17$ low-history comparisons. Both meet
their registered eighty-percent targets. The sparse procedure wins in $10$ of
$17$ long-history markets. That fraction misses its registered sixty-percent
target. Only $6$ of $17$ sparse-regression curves improve strictly at both steps
of the history grid, missing the secondary seventy-percent target.

\begin{table}[htbp]\centering\small
\caption{Registered CFTC history-region predictions. The primary verdict is partial agreement because both short-history screens pass and the sparse long-history screen fails.}\label{tab:cftc-mechanism}
\begin{tabular}{lllll}\toprule
Prediction & Procedure & Region / ordering & Successes & Verdict\\\midrule
P1 & Full regression & $c<r^*/2$ & $29/34$ & Supported\\
P1 & Four predictors & $c<r^*/2$ & $15/17$ & Supported\\
P2 & Four predictors & $c>2r^*$ & $10/17$ & Not supported\\
P2 & Full regression & No eligible high-region cell & NA & Not testable\\
P3 & Four predictors & Strict fall at both history steps & $6/17$ & Not supported\\
\bottomrule\end{tabular}
\par\smallskip\begin{minipage}{.98\linewidth}\footnotesize
Both P1 screens must pass; the primary verdict then combines P1 and sparse P2.
P3 is secondary and cannot upgrade that verdict. Ties count as neither wins nor
losses. Unknowns retain planned denominators; none occurs in this run.
All comparisons use matched corrected-rank F, rather than selecting the better
of F and I after evaluation. Both model procedures can select ordinary I.
\end{minipage}\end{table}

Seven markets remain adverse for the sparse procedure at the long history.
The complete market-level scores, strict breaches, HAC diagnostics and
counterexamples remain in the supplementary result inventory and linked source
tables. No market, failed criterion or unfavorable curve was removed to obtain
the primary verdict. The shorter CFTC outcomes were known before this
registration, so the extension is prospective only for its new computations.
It gives partial agreement with a transported pattern, rather than a complete
independent confirmation or causal identification of estimation cost.

\FloatBarrier

'''
    position=text.index(r'\section{RQ3: limit-cost regions}')
    text=text[:position]+mechanism+text[position:]
    # Replace the old cost heatmap slot, retaining that complete figure in its
    # original package and extended index rather than exceeding four main slots.
    costfig=next(f for f in re.findall(r'\\begin\{figure\}.*?\\end\{figure\}',text,re.S) if 'fig:v10-cost' in f)
    decision=r'''\begin{figure}[htbp]\centering
\includegraphics[width=.98\linewidth]{figures/final-decision-map.pdf}
\caption{History, the tested penalty menu and stated cost preferences guide a matched comparison. The simulation median is full regression at the shorter history in the constant-parameter experiment. The CFTC cost fraction refers only to full regression at the original histories, varying reserve and breach-event charges with the exceedance-magnitude charge fixed. All charges are hypothetical. History, shrinkage and stated costs must be assessed together in the intended application.}\label{fig:decision}
\end{figure}'''
    text=text.replace(costfig,decision).replace(r'\ref{fig:v10-cost}',r'\ref{fig:decision}')
    # Keep every original illustrative cost number; add the method/fee scope.
    text=text.replace('For CFTC, higher reserve coefficients and lower fixed-breach coefficients generally favor expanded-menu regression over matched historical headroom, although the grid is not monotone',
        'For CFTC full regression, higher reserve coefficients and lower fixed-breach coefficients generally favor the expanded-menu procedure over matched historical headroom, although the grid is not monotone')
    evaluation='We form a 90\\% model confidence set separately'
    text=text.replace(evaluation,'A model confidence set contains the procedures a joint loss comparison does not eliminate under its stated statistical approximation. We form a 90\\% model confidence set separately')
    text=text.replace('Matching histories and update schedules isolates the forecast gain associated with the added conditioning within each comparison.',
        'Matching completed training histories and update schedules names an explicit benchmark, while extra features and validation remain parts of each procedure.')
    # Conclusions are rewritten from the fixed evidence, including adverse/NA.
    a=text.index(r'\section{Conclusion}');b=text.index(r'\section*{Data and code availability}',a)
    text=text[:a]+r'''\section{Conclusion}\label{sec:conclusion}

Historical rules are hard to beat in these position records. Matched FX gains
coexist with adverse daily and weekly comparisons, changing reference rankings
and nonmonotone history curves. The original evaluation period was inspected,
and related reporting categories do not provide independent dealer replications.

The history evidence supports a bounded interpretation. Registered simulations
meet the short-history and long-history loss-sign criteria, while their
universal simplification claim fails. The CFTC extension gives partial
agreement: short-history disadvantage counts pass, whereas the long-history
win target and strict-improvement target fail. Longer history therefore cannot
serve as an automatic deployment rule.

The menu and selection evidence complements that result. A broader simulated
menu reduces a large short-history disadvantage, but the available financial
menu and its selection procedure still leave losses. Access to a historical
candidate helps explain why menu expansion alone does not identify predictor
value. The high-quantile failures remain unavailable and prevent a general
extension of the original gains to the higher target level.

Reserve amounts, breach frequency and exceedance magnitude also affect the
preferred tested report under stated charges. The fixed cost grids have local
exceptions and express hypothetical preferences, rather than realized trading
or funding benefits. Validation should retain a matched historical benchmark,
display the complete history sensitivity and report all three cost components
alongside scores and failures. Figure~\ref{fig:decision} summarizes this bounded
evaluation guidance.

\FloatBarrier

'''+text[b:]
    text=text.replace('/tree/revision-v12','/tree/final-jof')
    # Explicitly distinguish the extension from the old two-window CFTC record.
    phrase='Refits occur every thirteen records with histories of 52 and 260, using downloaded economic dates; first-release vintages remain unobserved.'
    assert phrase in text
    text=text.replace(phrase,phrase+' The registered mechanism extension adds a 520-week history on the same evaluation dates, while retaining the two older histories unchanged.')
    p.write_text(text)
    # Tail sensitivity stays in the compact Supplement even though its main
    # table was relocated; adverse and NA prose remains in the main article.
    supp=DEST/'supplement.tex';s=supp.read_text();s=s.replace(r'\end{document}',
        '\n\\section{Retained tail-level comparison table}\\label{sup:final-tail}\n'+tau+'\n'+r'\end{document}')
    supp.write_text(s)
    # Preserve title-page placeholders, changing the title only.
    title=DEST/'title-page.tex'
    if title.exists():title.write_text(title.read_text().replace(old_title,TITLE))
    report=dict(status='MAIN_ARGUMENT_DRAFTED_NOT_ACCEPTED',title=TITLE,
        baseline_main_sha256=hashlib.sha256(original.encode()).hexdigest(),
        draft_main_sha256=hashlib.sha256(text.encode()).hexdigest(),relocated_main_tables=records,
        inline_main_tables=len(re.findall(r'\\begin\{table\}',text)),
        main_table_inputs=re.findall(r'\\input\{([^}]+)\}',text),
        main_figures=len(re.findall(r'\\begin\{figure\}',text)),
        pending=['Current cross-references and supplemental CFTC mechanism details','Compilation, actual words/pages and six-table/four-figure limits','WP5 abstract and quantitative readability'],
        old_scientific_outputs_changed=0,new_model_fits=0)
    (ROOT/'notes/final-merge/wp4-main-rewrite.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
