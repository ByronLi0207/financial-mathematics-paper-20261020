"""Editorial insertion of audited fixed-source evidence, with no result recalculation."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];DOC=ROOT/'submission-v10';p=DOC/'manuscript.tex';s=p.read_text();abstract=s.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
anchor=r'\subsection{RQ2: daily, weekly and independently reported positions}'
block=r'''\subsection{How much history does FX regression need?}\label{sec:fx-history}

The fixed-period learning curve shows that more history helps only over part of the tested range (Figure~\ref{fig:v11-history}). Full regression moves from higher loss at the shortest history to its largest matched gain at an intermediate history. Part of that gain reverses at the longest history, while the four-feature curve also changes sign. Both curves use the original FX period and their original penalty menus; each history changes the regression and its matched historical reference. In these comparisons, conditional gains depend on sufficient history and a penalty menu that permits strong shrinkage.

\begin{figure}[!htbp]\centering\includegraphics[width=.88\linewidth]{figures/v11-fx-history.pdf}
\caption{Saved short-horizon FX learning curves on the original evaluation period. Both methods retain their original, different penalty menus, and every tested history is shown against its own matched historical headroom. This retrospective comparison does not identify a universally optimal history.}\label{fig:v11-history}
\end{figure}
\FloatBarrier

'''
assert s.count(anchor)==1;s=s.replace(anchor,block+anchor)
old='Delayed calibration preserves the later matched gain while changing breach behavior.';new=old+' Within the original FX period, the learning curve improves over intermediate histories but gives back part of the gain at the longest history (Figure~\\ref{fig:v11-history}).';assert old in s;s=s.replace(old,new)
old='Matching history and update schedules is therefore central to interpreting conditional forecast gains.';new=old+' The original-period learning curve also shows that gains are not monotone in history length.';assert old in s;s=s.replace(old,new)
s=s.replace('/tree/revision-v10b}', '/tree/revision-v11}')
assert abstract==s.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0];p.write_text(s)
p=DOC/'supplement.tex';s=p.read_text();i=s.index(r'\end{document}')
extra=r'''\section{Additional saved evidence on history length}\label{sup:v11-history}

The earlier confirmation exercise applies its frozen pooled criteria to heavy-tailed, regime-switching and compound-Poisson innovation laws. Table~\ref{tab:v11-confirmation} reports every prewritten criterion, including the failed universal ordering prediction. Its history regions use method-specific thresholds estimated in the earlier source study; they are not an oracle rule for the financial data.

\input{generated/v11-confirmation.tex}

The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v11/evidence/v11/pr5-v9}{unchanged source records} retain the complete synthetic results, counterexamples and candidate failures. The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v11/evidence/v11/pr5-v9/protocol/revision-v9/wp2-confirmatory.md}{original confirmation design} records the fixed laws, history regions, penalty menus and decision rules. Local design commits precede the numerical runs; their later public file uploads are not public preregistration.

The complete \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v11/evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json}{FX history contrasts} retain both horizons and every tested window. Both longer-horizon methods lose their gain again at the longest history. The four-feature short-horizon first cutpoint is left-censored and not testable, so the original all-curve confirmation is not established. These are inspected-period comparisons, not additional dealers or a fresh financial holdout.

'''
s=s[:i]+extra+s[i:];p.write_text(s)
p=DOC/'cover-letter.tex';s=p.read_text().replace('/tree/revision-v10b}', '/tree/revision-v11}');old='The paper suits Journal of Forecasting through its comparison of complete forecast procedures under matched histories and update schedules.';new=old+' The original-period FX learning curve shows that intermediate histories improve the matched comparison, while the longest history gives back part of the gain.';assert old in s;s=s.replace(old,new);p.write_text(s)
p=DOC/'title-page.tex';p.write_text(p.read_text().replace('/tree/revision-v10b}', '/tree/revision-v11}'))
(ROOT/'notes/v11/abstract-preservation.json').write_text(json.dumps({'status':'UNCHANGED_FROM_V10B','abstract_sha256':hashlib.sha256(abstract.encode()).hexdigest(),'words_from_base_receipt':161,'numeric_occurrences_from_base_receipt':8,'reason':'Retain v10b abstract/title/main line; history evidence enters the existing first finding without another numeric claim in the abstract.'},indent=2)+'\n')
