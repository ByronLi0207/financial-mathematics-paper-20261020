"""B3 one-time prose rewrite; every result token reads frozen v7 evidence."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EVIDENCE={r['id']:r for p in (ROOT/'notes/v7/evidence-parts').glob('*.json') for r in json.loads(p.read_text())}
BINDINGS=[]


def render(text):
    def sub(m):
        key,fmt=m.group(1),m.group(2);row=EVIDENCE[key];raw=float(row['value'])
        value=abs(raw) if fmt=='gain' else raw
        result=str(int(value)) if fmt=='count' else format(value,'.1f')
        BINDINGS.append(dict(id=key,source=row['source'],raw=row['value'],format=fmt,rendered=result))
        return result
    return re.sub(r'@@([A-Z0-9_]+)\|(gain|pct|count)@@',sub,text)


ABSTRACT=r'''Dealers set limits on the largest position reached before a review horizon ends. Using hourly FX and weekly dealer positions, we compare conditional quantile forecasts with historical rules at matched history lengths and update schedules. Historical rules are demanding benchmarks. Long-history FX regression lowers matched loss by @@FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|gain@@\% and @@FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT|gain@@\% in two periods. A calibration adjustment that updates after outcomes are observed retains the later gain (@@FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT|gain@@\%), with @@FX_ACI_H6_W2880_QR_HITS|count@@ versus @@FX_ACI_H6_W2880_F_HITS|count@@ breaches. Ranking against a shorter-history rolling rule changes across periods. On weekly aggregates, expanded regularization still leaves regression behind in @@PANEL_E5_QR33_EXPANDED_LOSSES|count@@ of @@PANEL_E5_PLANNED|count@@ panel comparisons. Conservative short-sample validation also leaves large weekly losses. Lower scores accompany more breaches before calibration: @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT|count@@ versus @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT|count@@ in the matched FX comparison. These findings support selecting peak limits from accuracy, breaches and ranking stability together.'''

CONTRIBUTIONS=r'''The paper makes three empirical points.

\textit{First, matched FX gains recur across periods, and the later gain survives delayed calibration.} Regression lowers matched loss by @@FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|gain@@\% and @@FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT|gain@@\% in the later and earlier periods (Table~\ref{tab:fx}). Calibration retains a @@FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT|gain@@\% gain with @@FX_ACI_H6_W2880_QR_HITS|count@@ versus @@FX_ACI_H6_W2880_F_HITS|count@@ breaches. The shorter-history rolling reference reverses the earlier-period ranking.

\textit{Second, historical rules prevail across the weekly aggregate comparisons.} The Treasury-bill regression raises loss by @@PANEL_BILL_QR_H6_W260_LOSS_PERCENT|pct@@\%, and expanded-menu regression still loses @@PANEL_E5_QR33_EXPANDED_LOSSES|count@@ of @@PANEL_E5_PLANNED|count@@ additional-panel comparisons (Table~\ref{tab:weekly}). Conservative one-standard-error selection also leaves a worst-cell loss increase of @@PANEL_R6_R2_RETRO_WORST|pct@@\% in the earlier weekly period. More regularization and conservative validation therefore leave substantial observed gaps.

\textit{Third, lower quantile loss can coincide with more limit breaches.} The unwrapped matched FX gain comes with @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT|count@@ versus @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT|count@@ breaches (Table~\ref{tab:fx}). Elementary-score curves cross for both original main comparisons (Figures~\ref{fig:murphyfx} and~\ref{fig:murphybill}). Scores, error amounts and breach counts therefore provide complementary evidence for selecting a peak limit.'''

RELATED=r'''Relative to the endpoint and path-risk precedents in Table~\ref{tab:literature}, the contribution is three comparative findings. First, matched FX gains of @@FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|gain@@\% and @@FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT|gain@@\% recur across periods; the later gain survives calibration, while the shorter rolling reference changes the earlier ranking (Table~\ref{tab:fx}). Second, expanded regression still loses @@PANEL_E5_QR33_EXPANDED_LOSSES|count@@ of @@PANEL_E5_PLANNED|count@@ weekly panel comparisons, while conservative validation leaves a @@PANEL_R6_R2_RETRO_WORST|pct@@\% worst-cell excess (Table~\ref{tab:weekly}). Third, the matched FX score gain accompanies @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT|count@@ versus @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT|count@@ breaches; the two original comparisons have crossing elementary-score curves (Table~\ref{tab:diagnostics}; Figures~\ref{fig:murphyfx}--\ref{fig:murphybill}). The forecasting and scoring methods are standard.'''

CONCLUSION=r'''Simple historical rules are hard to beat when forecasting peak net positions in these records. Long-history FX regression lowers matched loss by @@FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|gain@@\% and @@FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT|gain@@\% across two periods. Calibration retains the later gain with @@FX_ACI_H6_W2880_QR_HITS|count@@ versus @@FX_ACI_H6_W2880_F_HITS|count@@ breaches, while the shorter rolling reference changes the earlier ranking.

Weekly regression remains behind historical headroom: expanded regularization leaves @@PANEL_E5_QR33_EXPANDED_LOSSES|count@@ of @@PANEL_E5_PLANNED|count@@ panel comparisons worse, and conservative validation leaves large losses. Lower pinball loss also accompanies more breaches before FX calibration (@@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT|count@@ versus @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT|count@@). Peak-limit selection should therefore assess accuracy, error amounts, breaches and reference stability together. The calibrated simulation leaves the hourly mechanism unresolved and fails to reproduce the persistent weekly losses; the empirical findings remain specific to the observed records.'''

COVER=r'''Dear Editors,

Long-history FX quantile regression lowers matched peak-position forecast loss by @@FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|gain@@% and @@FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT|gain@@% across two periods, while historical rules prevail in most weekly comparisons.

Please consider "Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits" for Journal of Forecasting. The paper addresses comparative forecast evaluation, demanding simple benchmarks and the practical choice of position limits. Its peak target requires completed forward labels and matched histories and update schedules.

The three empirical findings concern reference stability, weekly benchmark strength and score-breach disagreement. A calibration adjustment retains the later FX gain with @@FX_ACI_H6_W2880_QR_HITS|count@@ versus @@FX_ACI_H6_W2880_F_HITS|count@@ breaches, but rankings against a shorter rolling reference vary by period. Expanded regression loses @@PANEL_E5_QR33_EXPANDED_LOSSES|count@@ of @@PANEL_E5_PLANNED|count@@ weekly panel comparisons; conservative validation leaves large losses. Before calibration, the matched FX score gain accompanies @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT|count@@ versus @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT|count@@ breaches. Standard methods and elementary target properties support these comparisons; they are not presented as methodological contributions.

The submission includes the manuscript, Online Supplement, title-page template and code/results. The calibrated simulation preserves every adverse and numerically failed cell. Author information and all required declarations remain marked for author completion before submission.

[TO BE COMPLETED BY AUTHOR]
'''


if __name__=='__main__':
    prose={key:render(text) for key,text in dict(abstract=ABSTRACT,contributions=CONTRIBUTIONS,related=RELATED,conclusion=CONCLUSION,cover_letter=COVER).items()}
    path=ROOT/'submission-jof/manuscript.tex';text=path.read_text()
    text,n=re.subn(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:r'\begin{abstract}'+prose['abstract']+r'\end{abstract}',text,count=1,flags=re.S);assert n==1
    start=text.index(r'\textbf{C1.}');end=text.index('\n\\FloatBarrier',start)
    roadmap=r'Section~\ref{sec:target} defines the target and records two elementary properties used later. The classical endpoint-to-peak bound supplies a separate benchmark under its stated assumptions. The subsequent sections compare matched forecasts, their stability and their implications for monitoring limits.'
    text=text[:start]+prose['contributions']+'\n\n'+roadmap+'\n'+text[end:]
    marker='\\FloatBarrier\n\n\\section{The forecast target}'
    assert text.count(marker)==1;text=text.replace(marker,prose['related']+'\n\n'+marker)
    start=text.index('\\section{Conclusion}\\label{sec:conclusion}')+len('\\section{Conclusion}\\label{sec:conclusion}')
    end=text.index('\n\\FloatBarrier',start);text=text[:start]+'\n\n'+prose['conclusion']+'\n'+text[end:]
    assert not re.search(r'\\textbf\{C[123]\.\}',text)
    path.write_text(text);(ROOT/'submission-jof/cover-letter.md').write_text(prose['cover_letter'])
    with (ROOT/'notes/v8/b3-prose.json').open('x') as f:json.dump(prose,f,indent=2);f.write('\n')
    with (ROOT/'notes/v8/contribution-bindings.json').open('x') as f:json.dump(BINDINGS,f,indent=2);f.write('\n')
    print('abstract words',len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:\.\d+)?",prose['abstract'])))
