# Final v8 prose

Source SHA256: 1522c06446e76df48f175aa9f82fb7631a7c58989451f2c7058028d1084ab6aa

## Abstract

Dealers set limits on the largest position reached before a review horizon ends. Using hourly FX and weekly dealer positions, we compare conditional quantile forecasts with historical rules at matched history lengths and update schedules. Historical rules are demanding benchmarks. Long-history FX regression lowers matched loss by 14.8\% and 16.6\% in two periods. A calibration adjustment that updates after outcomes are observed retains the later gain (15.0\%), with 329 versus 328 breaches. Ranking against a shorter-history rolling rule changes across periods. On weekly aggregates, expanded regularization still leaves regression behind in 34 of 48 panel comparisons. Conservative short-sample validation also leaves large weekly losses. Lower scores accompany more breaches before calibration: 376 versus 360 in the matched FX comparison. These findings support selecting peak limits from accuracy, breaches and ranking stability together.

## Introduction contributions

The paper makes three empirical points.

\textit{First, matched FX gains recur across periods, and the later gain survives delayed calibration.} Regression lowers matched loss by 14.8\% and 16.6\% in the later and earlier periods (Table~\ref{tab:fx}). Calibration retains a 15.0\% gain with 329 versus 328 breaches. The shorter-history rolling reference reverses the earlier-period ranking.

\textit{Second, historical rules prevail across the weekly aggregate comparisons.} The Treasury-bill regression raises loss by 50.8\%, and expanded-menu regression still loses 34 of 48 additional-panel comparisons (Table~\ref{tab:weekly}). Conservative one-standard-error selection also leaves a worst-cell loss increase of 181.4\% in the earlier weekly period. More regularization and conservative validation therefore leave substantial observed gaps.

\textit{Third, lower quantile loss can coincide with more limit breaches.} The unwrapped matched FX gain comes with 376 versus 360 breaches (Table~\ref{tab:fx}). Elementary-score curves cross for both original main comparisons (Figures~\ref{fig:murphyfx} and~\ref{fig:murphybill}). Scores, error amounts and breach counts therefore provide complementary evidence for selecting a peak limit.

## Conclusion

\label{sec:conclusion}

Simple historical rules are hard to beat for peak net positions in these records. FX regression lowers matched loss by 14.8\% and 16.6\% across periods. Calibration retains the later gain with 329 versus 328 breaches. The shorter rolling reference changes the earlier ranking.

Expanded regularization leaves weekly regression behind in 34 of 48 panel comparisons, and conservative validation leaves large losses. Lower FX pinball loss coexists with 376 versus 360 breaches before calibration. Peak-limit selection should assess accuracy, error amounts, breaches and reference stability together.

\FloatBarrier
