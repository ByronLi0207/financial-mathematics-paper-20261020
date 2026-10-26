"""Align the three findings across native main-text entry points; no new results."""
from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'submission-v10';N=R/'notes/v13'
p=D/'manuscript.tex';s=p.read_text();before=s
old_abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',s,re.S).group(1)
abstract='''Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules on hourly FX positions, weekly New York Fed positions and CFTC dealer positions, matching histories and update schedules. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8\\% and 16.6\\% in two periods, but its ranking against a shorter rolling rule changes. Second, historical rules beat regression in 34 of 48 New York Fed and 29 of 34 CFTC comparisons. Longer validation improves regression medians in both reporting systems; CFTC short-history excess falls from 19.3\\% to 4.0\\%. A benchmark-default gate retains FX gains and improves weekly median performance, but leaves large individual losses. Third, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor regression in CFTC. Costs are illustrative, and the evidence is retrospective; the original FX evaluation period had been inspected beforehand.'''
s=s.replace(r'\begin{abstract}'+old_abstract+r'\end{abstract}',r'\begin{abstract}'+abstract+r'\end{abstract}')
a=s.index('The paper makes three empirical findings.');b=s.index('Section~\\ref{sec:target}',a)
old_contrib=s[a:b]
contrib=r'''The paper makes three empirical findings.

\textit{First, matched FX gains recur across periods but remain reference-dependent.} Long-history regression lowers matched loss by 14.8\% and 16.6\%, while its ranking against the shorter rolling rule changes (Table~\ref{tab:fx}). The original-period learning curve improves with more history before surrendering part of the gain at the longest history (Figure~\ref{fig:v11-fx-history}). Matching peak responses, completed labels and refit schedules makes these comparisons interpretable without isolating causal feature effects.

\textit{Second, longer validation improves weekly regression medians while leaving large individual-task losses.} Historical controls remain competitive in both weekly reporting systems, while extended validation reduces regression medians (Table~\ref{tab:v13-validation}). The CFTC short-history median excess falls from 19.3\% to 4.0\%, and New York Fed medians also improve. A benchmark-default protocol retains FX gains and has zero weekly median excess, but 8 of 60 cases still lose by over ten percent (Section~\ref{sec:v13-rp}). These are retrospective arm-median comparisons; the horizon-six New York Fed extension also moves the validation boundary.

\textit{Third, lower scores leave limit-cost rankings sensitive to prices.} Expanded regression is cheaper in 5/34 CFTC cases at the grid center, and in 32/34 or 1/34 at opposite corners (Figure~\ref{fig:v10-cost}). Higher reserve charges and lower fixed breach charges generally favor regression, with local exceptions. These illustrative preferences motivate joint reporting of reserves, breaches and exceedance amounts, while institutional costs remain unmeasured.

'''
# Use the actual retained history-figure identifier.
if r'\label{fig:v11-fx-history}' not in s:
 m=re.search(r'\\includegraphics\[[^\]]*\]\{figures/v11-fx-history.pdf\}.*?\\label\{([^}]+)\}',s,re.S);assert m;contrib=contrib.replace('fig:v11-fx-history',m.group(1))
s=s[:a]+contrib+s[b:]
a=s.index('The matched FX gain changes interpretation');b=s.index(r'\FloatBarrier',a)
old_lit_end=s[a:b]
lit_end=r'''Matched FX gains remain reference-dependent, while longer validation reduces weekly regression medians in two reporting systems. A benchmark-default gate still leaves large weekly losses, and illustrative cost rankings change as reserve and breach prices vary. These three findings use established forecast tests \citep{dm1995,gw2006,mcs2011}; inventory-sensitive quoting motivates exposure monitoring \citep{avellaneda2008}. Observed position paths identify forecast behavior, leaving the effects of limits on subsequent trading decisions unmeasured.

'''
s=s[:a]+lit_end+s[b:]
a=s.index(r'\section{Conclusion}\label{sec:conclusion}')+len(r'\section{Conclusion}\label{sec:conclusion}');b=s.index(r'\FloatBarrier',a)
old_conclusion=s[a:b]
conclusion=r'''

Historical rules are hard to beat. For RQ1, matched FX regression gains recur across periods, but a shorter rolling reference changes the ranking (Table~\ref{tab:fx}). The learning curve also gives back part of its gain at the longest history, linking conditional performance to available history rather than universal model advantage (Figure~\ref{fig:fx-history}).

For RQ2, longer validation reduces full-regression medians in both weekly reporting systems, but across-arm differences need not describe typical paired improvements (Table~\ref{tab:v13-validation}). These dealer aggregates remain related tasks, and the horizon-six New York Fed extension also moves the validation endpoint. The benchmark-default protocol cuts weekly median excess to 0.00\% and preserves FX gains, yet 8 of 60 cases still lose by over ten percent, including a worst 80.98\% (Section~\ref{sec:v13-rp}). This failed tail criterion limits the protocol's risk-management recommendation, and the rejected high-quantile repair leaves its original judgments unresolved.

For RQ3, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC, with local exceptions (Figure~\ref{fig:v10-cost}). Lower pinball scores can therefore coexist with more breaches and different cost rankings, requiring joint reporting of reserve amounts, breach counts and exceedance amounts. The costs are stipulated preferences rather than observed institutional costs, and the financial evidence remains retrospective.

'''
# Obtain the same figure label used above rather than introducing a new reference.
history_label=re.search(r'\\includegraphics\[[^\]]*\]\{figures/v11-fx-history.pdf\}.*?\\label\{([^}]+)\}',s,re.S).group(1)
conclusion=conclusion.replace('fig:fx-history',history_label)
s=s[:a]+conclusion+s[b:]
# Current practical advice must distinguish a historical default from the failed evidence-gate protection claim.
a=s.index(r'\textbf{Use historical headroom by default');b=s.index(r'\textbf{Report breaches with the score.}',a)
old_practical=s[a:b]
practical=r'''\textbf{Use historical headroom by default when validation evidence is short.} Longer validation and a paired standard-error gate improve the weekly median, but leave eight large losses in the complete comparison (Section~\ref{sec:v13-rp}). Passing this gate alone therefore fails to establish adequate benchmark protection. The ordinary empirical quantile is up to 36.5\% worse than corrected headroom in the earlier weekly grid, supporting a separately validated historical default.

'''
s=s[:a]+practical+s[b:]
p.write_text(s)
record={'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest(),'abstract_before':old_abstract,'abstract_after':abstract,'contributions_before':old_contrib,'contributions_after':contrib,'related_ending_before':old_lit_end,'related_ending_after':lit_end,'conclusion_before':old_conclusion,'conclusion_after':conclusion,'practical_before':old_practical,'practical_after':practical,'order':['Reference-dependent matched FX gains and history','Weekly validation improvement with remaining protocol losses','Price-dependent illustrative cost rankings'],'result_archives_changed':False}
(N/'G6-main-edit.json').write_text(json.dumps(record,indent=2))
print('G6_MAIN_FIVE_ENTRY_POINTS_ALIGNED')
