# v12最终正文摘录

## Abstract

Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules using hourly FX positions, weekly New York Fed positions and dealer aggregates in 17 CFTC futures markets. Histories and update schedules are matched. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8% and 16.6% across two periods, but its ranking against a shorter rolling rule changes. Second, historical rules beat regression in 34 of 48 New York Fed comparisons and 29 of 34 CFTC comparisons; finite-penalty hindsight still favors history in most short weekly comparisons. They usually remain in the model confidence set alongside alternatives. In calibrated simulations, expanding the penalty menu cuts the constant-parameter median excess loss from 116.2% to near zero; switching adds no observed median loss in this short-history comparison. Third, in CFTC, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor expanded regression. The evidence is retrospective, and the original FX evaluation period had been inspected beforehand.

## Contributions

First, matched FX gains recur, but rankings against a shorter rolling rule change. The period comparisons separate conditioning gains from the reference procedure (Table 4). Delayed calibration preserves the later matched gain while changing breach behavior. Within the original FX period, the full-regression learning curve improves at intermediate histories but gives back part of the gain at the longest history (Figure 2).

Second, historical rules remain competitive in weekly data, where both penalty selection and the finite menu leave losses. The panel and independent CFTC reporting system favor historical controls in most comparisons, and historical methods usually survive joint forecast comparison (Tables 5–7). Even the best finite penalty chosen with evaluation hindsight loses in 29 of 41 short-history weekly comparisons (Section 7.4). Longer validation narrows CFTC losses and selects the intercept-only limit more often, linking tuning instability to the available validation history. Expanded simulation menus also bring short-history regression near its historical reference, with no additional observed median loss from parameter switching. These retrospective diagnostics distinguish a finite-menu gap from selection errors, without ruling out other conditional signals.

Third, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC. The direction has local exceptions (Figure 5). Lower scores therefore need not mean lower limit costs, and validation should report reserve amounts, breach counts and exceedance amounts together.

## Why does regression lose at low frequency?

Short weekly samples leave both tuning errors and a performance gap within the finite penalty menu. Figure 4 splits full regression's actual excess into the selected report's gap from the best finite candidate and that candidate's gap from historical headroom. The best candidate uses evaluation hindsight over five finite penalties; the ordinary empirical option is excluded. For full regression, the finite-menu gap is positive in 29 of 41 short-history weekly cells; selection exceeds half of positive actual excess in 27. Both criteria hold, so benchmark advantages and selection losses coexist within this menu. Separate component medians need not add: actual excess is 19.44%, selection 18.32%, and the diagnostic gap 4.37%.

This retrospective finite oracle is diagnostic, cannot guide deployment, and cannot rule out information in other conditional models. When validation selects the ordinary empirical limit, it can beat every finite candidate and make the selection component negative. Both long-history FX horizons have a negative finite-menu gap. Expanded menus also bring the calibrated simulation medians close to their historical reference, leaving the empirical frequency mechanism unidentified.



Extending validation from 52 to 156 weeks keeps the CFTC evaluation period, training histories, and refitting clock fixed. Median excess falls from 19.33% to 4.03% with 52-week training histories, and from 10.35% to 0.53% with 260-week histories. Infinite-penalty selections rise from 4 to 10 of 17 contracts, and from 4 to 5 of 17, respectively. These differences between across-contract medians need not match typical paired improvements and do not identify a causal effect. Four-feature failures remain unavailable in the complete inventory (Supplement Section S36).

Tail-level sensitivity remains incomplete, as Table 8 shows for 90% and 99% quantiles under matched histories. At 99%, historical headroom wins 28 of 34 CFTC comparisons; one failure leaves the 29-win threshold unresolved. Both FX periods remain unavailable at 99%, leaving the combined improvement criterion undetermined. Unavailable planned comparisons are retained, and successful subsets never replace a missing full-group median.

## Conclusion

Historical rules are hard to beat. For RQ1, matched FX regression gains recur across periods, but the shorter rolling reference changes the ranking and history gains are not monotone. Delayed calibration preserves the later matched gain with a small breach-count difference, reinforcing the need to interpret conditioning gains under explicit histories and update schedules.

For RQ2, historical controls remain competitive across related weekly aggregates and same-record daily FX, usually surviving joint comparison alongside alternatives. The finite-penalty hindsight diagnostic leaves losses in most short weekly comparisons, while longer validation improves CFTC selection toward historical reports. Both menu limits and selection errors therefore matter within the tested procedures; neither result rules out every possible conditional signal. Expanded simulation menus bring short-history regression near its historical reference, with switching adding no further observed median loss in that comparison. Numerical failures prevent a complete assessment at the higher quantile level, leaving the original gains without a demonstrated extension there.

For RQ3, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC, with local exceptions. Lower forecast scores therefore need not imply lower limit costs. Validation should report reserve amounts, breach counts and exceedance amounts together, using the cost regions in Figure 5.
