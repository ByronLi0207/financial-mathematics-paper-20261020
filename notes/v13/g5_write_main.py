"""Apply the requested v13 main-text structure using saved numeric outputs only."""
from pathlib import Path
import json,hashlib,re,subprocess
R=Path(__file__).resolve().parents[2];D=R/'submission-v10';N=R/'notes/v13'
p=D/'manuscript.tex';s=p.read_text();before=s
load=lambda name:json.loads((R/name).read_text())
f1=load('results/v12/decomposition/predictions.json')
f2=load('results/v12/validation-length/predictions.json')['methods']['QR33']['by_window']
g2=load('results/v13/nyfed-validation/summary.json')['methods']['QR33']['by_horizon']
g1=load('results/v13/tau-repair/consistency.json')
g3=load('results/v13/recommended-protocol/summary.json');w=g3['weekly']
# Retain four already verified original rows; all omitted precedents remain cited in the text.
start=s.index(r'\begin{table}[htbp]',s.index(r'\section{Related literature}'))
end=s.index(r'\end{table}',start)+len(r'\end{table}')
old_table=s[start:end]
rows=old_table.splitlines();drop=('\\shortstack[l]{Duffie','\\shortstack[l]{Engle','\\shortstack[l]{Ehm','\\shortstack[l]{Meinshausen')
new_rows=[line for line in rows if not line.startswith(drop)]
new_table='\n'.join(new_rows);assert sum(line.endswith(r'\\') for line in new_rows)==4
s=s[:start]+new_table+s[end:]
# Move the MCS paragraph and table to the supplement; its own identifiers remain unchanged there.
start=s.index(r'\subsubsection{Model confidence sets}')
end=s.index('% Display-only generated file',start)
old_mcs=s[start:end]
replacement=r'''\subsubsection{Model confidence sets}

Matched historical methods remain in most confidence sets, usually alongside alternatives (Supplement Table~\vthirteenMCSTable{}). Non-elimination establishes neither equal predictive risk nor a uniquely preferred method, supporting the retention of historical controls as comparators.

'''
s=s[:start]+replacement+s[end:]
s=s.replace(r'\newcounter{proposition}',r'\newcounter{proposition}'+'\n'+r'\newcommand{\vthirteenMCSTable}{S49}')
s=s.replace(r'Tables~\ref{tab:weekly}--\ref{tab:v10-mcs-main}',r'Table~\ref{tab:weekly} and Supplement Table~\vthirteenMCSTable{}')
# New common validation table, with all values read from the preserved arm summaries.
table=r'''\begin{table}[htbp]\centering\small
\caption{Full-regression excess loss versus matched historical headroom under longer validation. Entries are source medians in percent; the final column counts selections of the intercept-only limit.}\label{tab:v13-validation}
\begin{tabular}{lrrrrrr}\toprule
Reporting system & Horizon & History & Series & Validation 52 & Validation 156 & Limit selections\\\midrule
'''
for label,h,history,n,arms,counts in [
 ('CFTC',6,52,17,f2['52']['median_relative_loss_by_validation'],f2['52']['known_infinity_count_by_validation']),
 ('CFTC',6,260,17,f2['260']['median_relative_loss_by_validation'],f2['260']['known_infinity_count_by_validation']),
 ('New York Fed',6,52,13,g2['6']['median_relative_loss_by_validation'],g2['6']['infinity_count_by_validation']),
 ('New York Fed',24,52,13,g2['24']['median_relative_loss_by_validation'],g2['24']['infinity_count_by_validation'])]:
 table+=f"{label} & {h} & {history} & {n} & {arms['52']:+.2f} & {arms['156']:+.2f} & {counts['52']} to {counts['156']} "+r'\\'+'\n'
table+=r'''\bottomrule\end{tabular}
\par\vspace{2pt}\begin{minipage}{.98\linewidth}\footnotesize
Training history and validation length count weekly records; evaluation dates remain unchanged within each reporting system.
New York Fed horizon six also advances the validation endpoint by eighteen weeks and changes the refit phase; across-arm medians do not measure typical paired changes.
Supplement Section S38 retains individual series, four-feature results and the complete source comparison figure.
\end{minipage}\end{table}
'''
tp=D/'generated/v13-validation-main.tex';assert not tp.exists();tp.write_text(table)
start=s.index(r'\subsection{Why does regression lose at low frequency?}')
end=s.index(r'\subsection{Scores and breach behavior',start)
old_low=s[start:end]
low=r'''\subsection{Why does regression lose at low frequency?}\label{sec:v12-low-frequency}
Penalty selection dominates positive excess loss in @D2@ of @N@ short-history weekly comparisons (Figure~\ref{fig:v12-decomposition}). Extending validation lowers CFTC median excess loss from @C52A@\% to @C52B@\% with short histories, and from @C260A@\% to @C260B@\% with longer histories. The New York Fed medians fall from @N6A@\% to @N6B@\% at horizon six and from @N24A@\% to @N24B@\% at horizon twenty-four (Table~\ref{tab:v13-validation}). Yet the best finite penalty selected with evaluation hindsight still loses to historical headroom in @D1@ of @N@ comparisons. This residual gap indicates limited incremental information within the tested feature set and finite menu.

The decomposition separates the selected report's gap from the best finite candidate and that candidate's gap from historical headroom. The retrospective finite candidate uses five penalties and excludes the ordinary empirical limit, supplying a diagnostic rather than a deployable selection rule. Separate component medians need not add: actual excess is 19.44\%, selection 18.32\%, and the diagnostic gap 4.37\%. An empirical-limit selection can beat every finite candidate, making its selection component negative; both long-history FX horizons have negative finite-menu gaps.

\begin{figure}[htbp]\centering
\includegraphics[width=.98\linewidth]{figures/v12-decomposition.pdf}
\caption{Signed decomposition of regression excess loss against matched historical headroom, with selection in blue, the finite-menu diagnostic gap in orange, and actual excess as black dots. Crosses retain unavailable comparisons; the text focuses on short-history weekly cells while all planned comparisons remain plotted.}\label{fig:v12-decomposition}
\end{figure}

\input{generated/v13-validation-main.tex}

Longer validation selects the intercept-only limit more often in both reporting systems, consistent with less aggressive conditional fitting (Table~\ref{tab:v13-validation}). The New York Fed horizon-six endpoint also advances eighteen weeks and changes the refit phase, leaving a causal length-only effect unidentified. Its median paired change is zero despite the lower long-validation arm median, so differences between arm medians need not represent typical improvements. Four-feature results and original CFTC failures remain available in Supplement Sections S36 and S38. The simulation menu comparison also brings short-history regression closer to history, linking useful conditional reports to sufficient history, validation evidence and adequate shrinkage.

Tail-level sensitivity remains incomplete, as Table~\ref{tab:v12-tau} shows under matched histories. At 99\%, historical headroom wins 28 of 34 CFTC comparisons; one failure leaves the 29-win threshold unresolved. Both FX periods remain unavailable at that level, leaving their joint improvement criterion undetermined. After a solver repair designed after the failure, only @PASS@ of @GATEN@ compatibility fits met the pre-specified forecast-preservation criterion. The repair was therefore rejected before the three failed cells were re-estimated; their original unavailable results and judgments remain intact.

\begin{table}[htbp]\centering\small
\caption{Full-regression relative excess loss (\%) at alternative quantile levels. Positive values favor matched historical headroom; NA retains any failed required comparison.}\label{tab:v12-tau}
\begin{tabular}{lrr}\toprule
Source / training history & 90\% & 99\% \\\midrule
CFTC, 52 weeks & +3.45 & +15.05 \\
CFTC, 260 weeks & +1.58 & \textsc{NA} \\
FX, original period & -10.15 & \textsc{NA} \\
FX, earlier period & -17.85 & \textsc{NA} \\
Treasury bills & +0.67 & +44.22 \\
\bottomrule\end{tabular}
\par\vspace{2pt}\begin{minipage}{.95\linewidth}\footnotesize
Contract rows report full-group medians; FX uses 2,880-hour histories and Treasury uses 260 weeks.
After a solver repair designed after the failure, six of ten numerical fits preserved forecasts within the required relative tolerance; the rejected repair leaves all original NA entries unchanged.
Supplement Section S38 reports every compatibility case, with successful subsets excluded from full-group medians.
\end{minipage}\end{table}


'''
values={'D2':f1['D2']['support_n'],'D1':f1['D1']['support_n'],'N':f1['D1']['planned_n'],
 'C52A':f"{f2['52']['median_relative_loss_by_validation']['52']:.2f}",'C52B':f"{f2['52']['median_relative_loss_by_validation']['156']:.2f}",
 'C260A':f"{f2['260']['median_relative_loss_by_validation']['52']:.2f}",'C260B':f"{f2['260']['median_relative_loss_by_validation']['156']:.2f}",
 'N6A':f"{g2['6']['median_relative_loss_by_validation']['52']:.2f}",'N6B':f"{g2['6']['median_relative_loss_by_validation']['156']:.2f}",
 'N24A':f"{g2['24']['median_relative_loss_by_validation']['52']:.2f}",'N24B':f"{g2['24']['median_relative_loss_by_validation']['156']:.2f}",
 'PASS':g1['passed'],'GATEN':g1['n']}
for key,value in values.items():low=low.replace('@'+key+'@',str(value))
assert '@' not in low;s=s[:start]+low+s[end:]
# Compress the old score/breach subsection to one paragraph; full diagnostics already remain in S33.
start=s.index(r'\subsection{Scores and breach behavior')
end=s.index(r'\FloatBarrier',start)
old_score=s[start:end]
score=r'''\subsection{Scores and breach behavior answer different questions}

Lower pinball loss leaves breach behavior unresolved: matched FX gains accompany more breaches before calibration (Table~\ref{tab:fx}). Elementary-score curves cross for both original comparisons, and the separate 24-step comparison reverses near 20.6:1 (Supplement Figures S2--S3). Both six-step FX comparisons reduce mean underprediction and mean overprediction, so that weight reversal belongs to the longer-horizon reference. Average-loss tests, strict-hit diagnostics and RMS-state comparisons therefore address distinct questions about error amounts, breach dependence and conditional predictive ability (Supplement Table S47; \citealp{gw2006}).

'''
s=s[:start]+score+s[end:]
# Insert the requested protocol subsection at the start of Section9.
marker=r'\section{Implications for model validation}\label{sec:implications}'
protocol=r'''

\subsection{A benchmark-protected validation protocol}\label{sec:v13-rp}
The protocol combines a six-point penalty menu, longer validation and a corrected-rank historical default. It selects the lowest validation loss over 156 weekly observations or 5,760 FX records, switching only when paired improvement strictly exceeds one HAC standard error. Across @WEEKLY@ weekly comparisons, median excess falls from @ORD@\% to @RP@\%, but @BAD@ still lose by more than ten percent, missing the prewritten protection criterion. Both FX periods retain their ordinary-regression gains; the worst weekly excess remains @WORST@\% (Figure~\ref{fig:v13-rp}). The rule was designed after earlier findings and uses inspected evaluation periods, so this check is retrospective.

\begin{figure}[htbp]\centering
\includegraphics[width=.98\linewidth]{figures/v13-rp.pdf}
\caption{Ordinary regression and the benchmark-default protocol relative to matched historical headroom. Every planned comparison is complete: 34 CFTC, 26 New York Fed and two FX cases; points retain each outcome, including large losses. Separate vertical scales preserve each source's distribution without pooling native exposure units.}\label{fig:v13-rp}
\end{figure}

\subsection{Practical reporting}
'''
for key,value in {'WEEKLY':w['eligible'],'ORD':f"{w['ordinary_median_relative_loss_pct']:.2f}",'RP':f"{w['median_relative_loss_pct']:.2f}",'BAD':w['adverse_gt10_count'],'WORST':f"{w['worst_relative_loss_pct']:.2f}"}.items():protocol=protocol.replace('@'+key+'@',str(value))
s=s.replace(marker,marker+protocol)
# Link the updated code/reproduction entry without rewriting fixed historical evidence links.
s=s.replace('https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v12','https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v13')
p.write_text(s)
record={'stage':'G5-main','before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest(),
 'literature':{'old_table':old_table,'new_table':new_table,'retained_rows':4,'cell_text_unchanged':all(line in old_table for line in new_rows)},
 'moved_mcs':old_mcs,'compressed_score_breach_original':old_score,
 'new_validation_table':'submission-v10/generated/v13-validation-main.tex','original_tau_numeric_rows_preserved':True,
 'new_low_frequency_first_paragraph':low.split('\n\n')[0],'new_protocol_subsection':protocol,
 'source_files':{q:hashlib.sha256((R/q).read_bytes()).hexdigest() for q in ['results/v12/decomposition/predictions.json','results/v12/validation-length/predictions.json','results/v13/nyfed-validation/summary.json','results/v13/tau-repair/consistency.json','results/v13/recommended-protocol/summary.json']}}
(N/'G5-main-edit.json').write_text(json.dumps(record,indent=2))
print('G5_MAIN_WRITTEN',len(s),'characters')
