# Evidence-directed writing comparison

Writing branch: **partly supported**. The simulation primary P1/P2 screen passes; universal simplification fails; the FX grid gives three identified consistent cutpoints and a compatible-left-censored NOT_TESTABLE case, with longest-history reversals. The selected c omits p, and the design does not isolate estimation cost. Every original main-table numeric vector and display equation is unchanged.

| Measure | Before v8 | Current draft |
|---|---:|---:|
| abstract_words | 164 | 149 |
| abstract_numbers | 4 | 2 |
| main_words | 4646 | 5377 |
| main_sentences | 244 | 275 |
| mean_sentence_words | 19.040983606557376 | 19.55272727272727 |
| over35_percent | 0.0 | 0.0 |
| negation_percent | 4.508196721311475 | 4.363636363636363 |
| max_numbers_per_sentence | 2 | 2 |
| pass_quantitative | True | True |
| all_v8_writing_gates_pass | True | True |

Original and current abstracts, Introduction opening, C2 and conclusion are printed verbatim below. These are prose revisions around unchanged older numerical results plus source-bound new outcomes.

## title

Before:

Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits

After:

When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits

## intro-central-claim

Before:

We examine these competing effects through matched histories, alternative reference rules, and repeated chronological comparisons.

After:

We examine these competing effects through matched histories, alternative reference rules, and repeated chronological comparisons.

Training-history length provides an organizing question for the comparisons, with the proposed explanation tested rather than imposed on every favorable and adverse result. A post hoc coordinate comparison motivates predictions for a new simulation grid and fixed-period FX learning curves under unchanged validation and evaluation clocks. The resulting support is partial: the broad simulated loss pattern survives, while universal simplification fails and the financial curves show censoring and reversals. This evidence guides history-sensitivity validation without identifying a unique estimation-cost channel or a permanent sample-size threshold.

## abstract

Before:

Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the previously reported later and earlier windows. Its later advantage survives a delayed adaptive coverage adjustment (ACI). Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series. A controlled simulation rejects a universal narrow-regime explanation, while aggregation and the overlapping backcast further qualify the empirical pattern.

After:

Peak-position limits concern the largest absolute inventory reached before a review ends, making completed path labels and the observed current position central to forecasting. We compare historical and conditional quantile reports for an FX market maker and weekly primary-dealer position aggregates, using matched histories and update schedules. Simple historical rules remain demanding benchmarks across frequencies, position categories and reference choices. At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the previously reported later and earlier windows. A post hoc history-to-horizon coordinate organizes simulation gains, and a new simulation passes its short-history and long-history prediction screens. Real-record learning curves partly support the predicted first cutpoints, while left censoring, large-history reversals and failures of universal simplification qualify that pattern. For limit managers, these findings motivate matching historical information before assessing conditional forecasts jointly on score, breaches and stability, with history length guiding evaluation.

## intro-first

Before:

A dealer's recorded net position can finish inside its limit after exceeding it earlier in the monitoring period, as Figure~\ref{fig:example} illustrates. The forecasting question concerns the largest sampled exposure before the next review, rather than the endpoint alone. This changes the response and when its training label becomes available. We ask whether additional conditioning improves that peak forecast once historical information is matched, and whether the gain survives alternative references and breach assessment.

After:

An inventory limit can look adequate at the horizon endpoint even when a dealer's position has crossed it earlier in the review period. Figure~\ref{fig:example} shows why the relevant forecast is a sampled path maximum rather than an endpoint interval. The challenge is to learn that peak from completed historical labels while preserving the information available when the position is observed. We ask when additional conditioning improves on historical headroom forecasts that use the same training history, and how longer histories alter that comparison.

## C2

Before:

\textbf{C2.} We find that historical rules win most weekly comparisons, while the original long-history FX gain depends on the chosen reference. We compare the same peak target for one FX record and thirteen weekly position-category aggregates with matched histories and update schedules. Even after extending the regression penalty menu, historical rules win in 34 of 48 additional-panel comparisons. Where Duffie et al. (2023) examine capacity, illiquidity and PnL quantiles, and Wisniewski et al. (2020) forecast one market maker's endpoints, we compare these peak-position tasks. Section~\ref{sec:results} reports the gains and failures, and Table~\ref{tab:map} organizes the observed settings and validation questions. The controlled study rejects the proposed regime restriction, while aggregation supplies a same-dealer contrast without isolating frequency.

After:

\textbf{C2.} We find that horizon-adjusted training history organizes conditional peak-forecast gains, with partial support from a new simulation grid and retrospective learning curves. We compare the same peak target for one FX record and thirteen weekly position-category aggregates with matched histories and update schedules. Even after extending the regression penalty menu, historical rules win in 34 of 48 additional-panel comparisons. The new simulations satisfy their short-history and long-history criteria, while the predicted universal advantage of the smaller regression fails in the comparable cells. Where Duffie et al. (2023) examine capacity, illiquidity and PnL quantiles, and Wisniewski et al. (2020) forecast one market maker's endpoints, we compare these peak-position tasks. Section~\ref{sec:results} and Figure~\ref{fig:mechanism} connect that contrast to post hoc first cutpoints, left censoring and long-history reversals, guiding matched history-sensitivity validation.

## decision-rule

Before:



After:

A practical history screen is to examine the entire matched-loss curve around the available history and verify its breach behavior and temporal stability. The coordinate and its cutpoints can organize that investigation, but left censoring and later reversals require testing the actual reporting configuration. Treat a favorable region as a candidate for further validation rather than a permanent minimum-sample rule or an empirically measured sample-per-parameter threshold.

## map-caption

Before:

A winning score leaves breach behavior and operating suitability to be assessed.

After:

The map guides history-sensitivity checks alongside breach behavior and operating suitability.

## mechanism-limitations

Before:



After:

The history coordinate is descriptive, with parameter count absent from the selected index and dependence beyond the response horizon left unmeasured. Different penalty menus and approximation errors move together with predictor count, so the comparison does not isolate an estimation-cost channel. The new simulation's specified loss-pattern screens are met, while universal simplification fails and the financial grid supplies partial first-cutpoint consistency. Wide post hoc endpoint envelopes and left censoring limit threshold precision, while the longest-history reversals contradict a permanent operating cutoff. Weekly grids lack a dedicated broad-history learning curve, and some exceed the smaller model's point cutpoint without uniformly winning.

## conclusion-first

Before:

Simple historical rules are strong competitors for predicting the largest sampled absolute position before a monitoring horizon ends. The original long-history FX regression gains against matched headroom survive in the broader backcast on previously examined observations, although score reductions coexist with more breaches. Longer-horizon backcast gains and the daily exception prevent a literal short-horizon or hourly-only interpretation. The controlled simulation also rejects the proposed narrow-regime restriction, while the same-dealer aggregation contrast leaves frequency mixed with measurement and clock changes. The defensible result is reference-sensitive comparative accuracy in these records, rather than a universal mechanism or validated operating-limit rule.

After:

Historical rules remain demanding competitors for sampled peak-position quantiles, with conditional gains depending on the reference, training history and forecast horizon. The post hoc history-to-horizon coordinate organizes the original simulations, and the new simulation grid supports its specified short-history and long-history loss patterns. Retrospective FX curves provide partial first-cutpoint consistency, while left censoring, long-history reversals and failed universal simplification qualify a single-threshold interpretation. The controlled study's earlier narrow-regime explanation still fails, so the history pattern adds a bounded organizing description rather than replacing contrary evidence. These results motivate validation at the actual history and reference, combining score, breach frequency and stability before a limit manager adopts additional conditioning.

## Decisions and boundaries

The question-form title is adopted. The alternative subtitle The Estimation Cost of Conditioning remains unadopted and is not recommended as an identified mechanism claim. The decision map now guides full history-sensitivity validation; it supplies no automatic per-parameter deployment cutoff. The illustrative all-weekly-below-threshold claim was checked against saved coordinates and is false in13 cells, so the prose keeps weekly transfer failures visible.

Complete preference frontiers and numerical conventions are preserved verbatim in the linked extended technical source/PDF to retain the Supplement page budget. The full table output, all six simplification failures and complete twenty financial contrasts remain in the compact Supplement. The current PDF counts are main21, Supplement30 and separate technical overflow6; every-page final QA and package publication remain WP7 tasks.
