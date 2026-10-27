# Final v13 reusable prose

Native source SHA-256: `2a86025e0231fe76d008cff972c99289578bbb8bd9716846bc1c5de957aa233e`. Reference numbers resolved from the final owning main aux.

## Abstract

Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules on hourly FX positions, weekly New York Fed positions and CFTC dealer positions, matching histories and update schedules. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8% and 16.6% in two periods, but its ranking against a shorter rolling rule changes. Second, in the initial weekly comparisons, historical rules beat regression in 34 of 48 New York Fed and 29 of 34 CFTC cases. Longer validation improves regression medians in both reporting systems; CFTC short-history excess falls from 19.3% to 4.0%. A benchmark-default gate retains FX gains and improves weekly median performance, but leaves large individual losses. Third, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor regression in CFTC. Costs are illustrative, and the evidence is retrospective; the original FX evaluation period had been inspected beforehand.

## Section 7.4 — opening paragraph

Loss from penalty selection exceeds half of positive actual excess loss in 27 of 41 short-history weekly comparisons (Figure 4). Extending validation lowers CFTC median excess loss from 19.33% to 4.03% with short histories, and from 10.35% to 0.53% with longer histories. The New York Fed medians fall from 6.68% to -1.13% at horizon six and from 40.47% to 5.02% at horizon twenty-four (Table 7). Yet the best finite penalty selected with evaluation hindsight still loses to historical headroom in 29 of 41 comparisons. This residual gap indicates limited incremental information within the tested feature set and finite menu.

## Section 9.1 — complete protocol subsection

The protocol combines the six-point menu in Table 3, longer validation and a corrected-rank historical default. It selects the lowest mean validation loss over 156 weekly observations or 5,760 FX records. The selected candidate replaces historical headroom only when its paired validation improvement strictly exceeds one HAC standard error (Newey & West, 1987). Across 60 weekly comparisons, the protocol retains historical headroom in 32 and has 0.00% median excess, compared with 14.63% for ordinary regression. This zero median reflects the majority of decisions retaining historical headroom. However, 8 cases lose by over ten percent, exceeding the prewritten five-percent ceiling for such cases; the worst excess is 80.98% (Figure 6). Both FX periods retain the ordinary regression gains, meeting the criterion for retaining gains. The rule was designed after earlier findings and uses inspected evaluation periods, so this check is retrospective.

## Contribution 1

First, matched FX gains recur across periods but remain reference-dependent. Long-history regression lowers matched loss by 14.8% and 16.6%, while its ranking against the shorter rolling rule changes (Section 7.1). The original-period learning curve improves with more history before surrendering part of the gain at the longest history (Figure 2). Matching peak responses, completed labels and refit schedules makes these comparisons interpretable without isolating causal feature effects.

## Contribution 2

Second, longer validation improves weekly regression medians while leaving large losses on individual tasks. Historical controls remain competitive in both weekly reporting systems, while extended validation reduces regression medians (Section 7.4). The CFTC short-history median excess falls from 19.3% to 4.0%, and New York Fed medians also improve. A benchmark-default protocol retains FX gains and has zero weekly median excess, but 8 of 60 cases still lose by over ten percent (Section 9.1). These are retrospective arm-median comparisons; the horizon-six New York Fed extension also moves the validation boundary.

## Contribution 3

Third, lower scores leave limit-cost rankings sensitive to prices. Expanded regression is cheaper in 5/34 CFTC cases at the grid center, and in 32/34 or 1/34 at opposite corners (Section 8). Higher reserve charges and lower fixed breach charges generally favor regression, with local exceptions. These illustrative preferences motivate joint reporting of reserves, breaches and exceedance amounts, while institutional costs remain unmeasured.

## Conclusion

Historical rules are hard to beat. For RQ1, matched FX regression gains recur across periods, but a shorter rolling reference changes the ranking (Table 4). The learning curve also gives back part of its gain at the longest history, linking conditional performance to available history rather than universal model advantage (Figure 2).

For RQ2, longer validation reduces full-regression medians in both weekly reporting systems, but across-arm differences need not describe typical paired improvements (Table 7). These dealer aggregates remain related tasks, and the horizon-six New York Fed extension also moves the validation endpoint. The benchmark-default protocol cuts weekly median excess to 0.00% and preserves FX gains, yet 8 of 60 cases still lose by over ten percent, with a worst excess of 80.98% (Section 9.1). This failed tail criterion limits the protocol's risk-management recommendation, and the rejected high-quantile repair leaves its original judgments unresolved.

For RQ3, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC, with local exceptions (Figure 5). Lower pinball scores can therefore coexist with more breaches and different cost rankings, requiring joint reporting of reserve amounts, breach counts and exceedance amounts. The costs are stipulated preferences rather than observed institutional costs, and the financial evidence remains retrospective.

