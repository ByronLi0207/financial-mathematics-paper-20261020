"""Deterministic prose-only edits to the v10 submission copy; no study imports."""
from pathlib import Path
p=Path('submission-v10/manuscript.tex');s=p.read_text()
a=s.index(r'\begin{abstract}');b=s.index(r'\end{abstract}',a)
abstract="""Dealers monitor the largest position reached before a review horizon ends. We compare conditional quantile models with historical rules using hourly FX positions, weekly New York Fed positions and dealer aggregates in 17 CFTC futures markets. Histories and update schedules are matched. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8\\% and 16.6\\% across two periods, but its ranking against a shorter rolling rule changes. Second, historical rules beat regression in 34 of 48 New York Fed comparisons and 29 of 34 CFTC comparisons. They usually remain in the model confidence set alongside alternatives. In calibrated simulations, expanding the penalty menu cuts the constant-parameter median excess loss from 116.2\\% to near zero; the registered switching increment is unsupported. Third, in CFTC, lower scores need not mean lower limit costs: higher reserve charges and lower breach charges generally favor regression. The evidence is retrospective, and the original FX evaluation period had been inspected beforehand."""
s=s[:a]+r'\begin{abstract}'+abstract+s[b:]
a=s.index('The paper makes three empirical findings.');b=s.index('\nSection~',a)
s=s[:a]+r'''The paper makes three empirical findings.

\textit{First, matched FX gains recur, but rankings against a shorter rolling rule change.} The period comparisons separate conditioning gains from the reference procedure (Table~\ref{tab:fx}). Delayed calibration preserves the later matched gain while changing breach behavior.

\textit{Second, historical rules remain competitive in weekly data, and penalty menus explain large losses in the calibrated simulations.} The panel and independent CFTC reporting system favor historical controls in most comparisons (Tables~\ref{tab:weekly} and~\ref{tab:v10-cftc-contracts}). Historical procedures usually remain in model confidence sets alongside alternatives (Table~\ref{tab:v10-mcs-main}). Expanding the simulation menu brings short-history full regression close to its historical reference; the registered switching increment is unsupported.

\textit{Third, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC.} The direction has local exceptions (Figure~\ref{fig:v10-cost}). Lower scores therefore need not mean lower limit costs, and validation should report reserve amounts, breach counts and exceedance amounts together.
''' +s[b:]
old='The empirical contribution concerns matched ranking stability across responses, reporting systems and cost preferences. Established forecast tests support this comparison \\citep{dm1995,gw2006,mcs2011}. Inventory-sensitive quoting motivates exposure monitoring \\citep{avellaneda2008}; the present exercise scores passive reports on observed paths.'
new=r'''The comparison yields three findings: matched FX gains depend on the reference, weekly historical controls remain competitive, and cost rankings depend on reserve and breach preferences. The weekly finding includes the calibrated menu experiment, whose registered switching increment is unsupported. Established forecast tests support the comparisons \citep{dm1995,gw2006,mcs2011}. Inventory-sensitive quoting motivates exposure monitoring \citep{avellaneda2008}; here, the forecasts are scored on observed paths.'''
assert old in s;s=s.replace(old,new)
replacements={
r'Long-history FX regression beats matched historical headroom in both periods. Loss falls by 14.8\% later and 16.6\% earlier. Table~\ref{tab:fx} separates these matched controls from the shorter rolling reference.':r'Long-history FX regression beats matched historical headroom in both periods. Table~\ref{tab:fx} separates these matched controls from the shorter rolling reference, whose earlier-period ranking reverses.',
r'Delayed calibration retains the later matched FX gain. Wrapped regression lowers loss by 15.0\%. Its 329 breaches compare with 328 for wrapped historical headroom on common origins (Table~\ref{tab:fx}).':r'Delayed calibration retains the later matched FX gain. Its breach count remains slightly higher than wrapped historical headroom on common origins (Table~\ref{tab:fx}).',
r'The earlier FX ranking reverses when the reference changes. Against shorter-history rolling headroom, later loss falls by 12.7\%, but earlier loss rises by 3.2\%. Matched gains and rolling-reference gains therefore have different period stability (Table~\ref{tab:fx}).':r'The reference-sensitive hourly results motivate comparisons with other measurement clocks and reporting systems. These comparisons retain their own matched histories and completed peak labels.',
r'Treasury-bill regression loses on both accuracy and breaches. Mean loss rises by 50.8\%, with 54 regression breaches. Historical headroom records 28 breaches; the earlier short-window version also loses (Table~\ref{tab:weekly}).':r'The weekly Treasury-bill comparison also favors historical headroom on accuracy and breaches. The earlier short-window version has a different history and retains its separate adverse result (Table~\ref{tab:weekly}).',
r'Stronger regularization narrows weekly panel losses but leaves historical rules ahead. Median excess loss falls from 92.6\% to 9.2\% after menu expansion. Regression still loses 34 of 48 matched comparisons. Conservative selection chooses I in 17 of 26 earlier weekly cells but still leaves a worst-cell increase of 181.4\%. This is the Treasury-bill short-window, 24-step comparison (Table~\ref{tab:weekly}).':r'Stronger regularization narrows weekly panel losses but leaves historical rules ahead (Table~\ref{tab:weekly}). Conservative selection chooses the intercept-only report in 17 of 26 earlier weekly cells. Its worst loss remains the Treasury-bill short-window, 24-step comparison, despite the conservative selection rule.',
r'Regression\'s median excess losses are 19.3\% and 10.3\% at histories 52 and 260. Both exceed the registered ten-percent tolerance. Four-predictor regression improves from 10.3\% to 0.2\%.':r'Both full-regression medians exceed the registered ten-percent tolerance. Four-predictor regression moves closer to historical headroom with the longer history.',
r'Lower FX loss coexists with more breaches before calibration. Regression breaches 376 times against 360 for matched historical headroom. Pinball loss measures error amounts, while a strict-hit indicator records event occurrence. Monitoring reports should show both.':r'The matched FX gain coexists with more breaches before calibration (Table~\ref{tab:fx}). Pinball loss measures error amounts, while a strict-hit indicator records event occurrence. Monitoring reports should show both.',
r'Their original history-52 medians are 116.2\% and 121.4\%.':r'Their original short-history losses motivate the paired menu comparison below.',
r'At history 52, the expanded full-regression medians are 0.2\% under constant parameters and -0.2\% under switching. Both arms improve in all thirteen sources.':r'The expanded full-regression medians move close to historical headroom in both arms (Table~\ref{tab:v10-menu-main}). Both arms improve in every source.',
r'The unwrapped matched FX gain records 376 versus 360 breaches; the daily regression exception also has more breaches.':r'The unwrapped matched FX gain and the daily regression exception both have more breaches than their historical references.',
r'The limit costs are illustrative, not observed real operating costs. ':r''
}
# A transparent record of expected matches prevents silent partial rewriting.
records=[]
for old,new in replacements.items():
 hit=old in s;records.append((hit,old));
 if hit:s=s.replace(old,new)
# Conclusion contains one answer per question in the same three-finding order.
a=s.index(r'\section{Conclusion}');b=s.index(r'\FloatBarrier',a)
s=s[:a]+r'''\section{Conclusion}\label{sec:conclusion}

Historical rules are hard to beat. For RQ1, matched FX regression gains recur across periods, but rankings against the shorter rolling reference change. Delayed calibration preserves the later matched gain with a small breach-count difference. Matching history and update schedules is therefore central to interpreting conditional forecast gains.

For RQ2, historical controls remain competitive in related weekly categories, same-record daily aggregates and the independent CFTC reporting system. They usually remain in model confidence sets alongside alternatives. Short-sample validation still fails to protect the historical benchmark consistently. The calibrated paired experiment brings full regression near its historical reference by expanding the penalty menu. The registered switching increment is unsupported, while the empirical low-frequency mechanism remains unidentified.

For RQ3, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC, with local exceptions. Lower forecast scores therefore need not imply lower limit costs. Validation should report reserve amounts, breach counts and exceedance amounts together, using the cost regions in Figure~\ref{fig:v10-cost}.

''' +s[b:]
s=s.replace('/tree/revision-v10}', '/tree/revision-v10b}')
p.write_text(s)
Path('notes/v10b/prose-replacement-log.txt').write_text('\n'.join(str(hit)+' '+old for hit,old in records)+'\n')
Path('notes/v10b/abstract-after.txt').write_text(abstract.replace('\\%','%')+'\n')
print('Replaced',sum(x[0] for x in records),'of',len(records),'expected exact passages; inspect misses.')
