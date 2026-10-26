# S6 writing audit

Before is the exact v6 source preserved before v7 rewriting. The same script and scope apply to both versions. Citation years and inline numbers are counted. Headings are not prose sentences; both versions exclude the explicitly named transparency section/subsection, tables, table notes and displayed equations. Figure-caption prose remains included.

| Metric | Before | After |
|---|---:|---:|
| Abstract words | 215 | 139 |
| Abstract numbers | 9 | 4 |
| Mean sentence words | 16.7825 | 19.73488372093023 |
| Sentences over 35 words (%) | 2.0 | 0.0 |
| Sentences with negation (%) | 20.0 | 2.3255813953488373 |
| Maximum numbers per sentence | 10 | 2 |
| Paragraphs exceeding six sentences | 11 | 0 |
| Banned terms / phrases | 71 | 0 |

## Qualitative checks

- Paragraphs open with their main point, and the final prose sentence of each section draws its implication. Introduction, Results and Conclusion explicitly address limit monitoring.
- Limits on generalization and retrospective inference are collected in Limitations and the specified transparency subsection; formal theorem premises and table notes retain their necessary definitions.
- C2 describes observed setting differences without a causal frequency claim; C3 names both histories/update schedules without a causal decomposition claim.
- Horizon crossings refer explicitly to regression reports. The main method section now states the unchanged target fraction and the two source-record horizons.
- A drafting error in the filtered-path description was corrected against archived executed code: GARCH-standardized innovations are drawn independently with replacement; historical residual-block ordering was not claimed. Source SHA matches the archived run field, and no code/result changed.

## Abstract before

> Endpoint forecasts do not determine the maximum position reached along a financial path. We study the upper quantile of a sampled absolute net-position peak with a known current-position floor, explicitly matured training labels and matched-history controls. We state a pointwise floor projection, a classical absolute-displacement endpoint-to-peak bound and common-pool construction distances; none creates a new distribution-free coverage guarantee for fitted reports. Three findings delimit the empirical value. The original FX primary lowers mean loss by 12.660% on the previously inspected record. Its separately identified matched-history short-horizon regression lowers mean pinball loss by 14.77% but increases breaches from 360 to 376. Elementary-score curves for the distinct original FX primary cross, ruling out dominance for that pair. Horizon-specific short-history FX regression reports cross on 640/6625 origins despite ordered realized targets. The separately fitted Treasury regression primary raises loss by 50.79%, and the additional aggregate panel yields only 3/48 lower-loss original-regression cells. Exact gain decomposition, label-timing controls and additional mature benchmarks are post-result / exploratory, with mixed directions, failed fits and incomplete upper-target evidence retained. The Treasury exercise replays a downloaded vintage by economic date; compatible unseen-dealer and prospective public-release validation remain outstanding. The evidence supports joint validation of accuracy, calibration, report coherence and measurement compatibility, rather than a universal forecasting or funding advantage.

## Abstract after

> Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. Long-history FX regression changes matched loss by -14.77% and -16.62% in the later and earlier periods. Its later advantage survives the evaluated finite delayed coverage correction. Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.

## Introduction opening before

> Dealers absorb customer order imbalances while managing inventory risk and scarce balance-sheet capacity. Inventory affects optimal dealer pricing (Ho and Stoll, 1981), FX dealing (Lyons, 1995), and observed inventory adjustment in dealership markets (Hansch, Naik and Viswanathan, 1998). Treasury intermediation likewise depends on dealer capacity (Duffie et al., 2023). A forecast of the maximum recorded position magnitude over a future horizon may support monitoring of the measured position: an endpoint can return toward its starting value after an intervening large position. Translating that monitoring signal into a particular margin or financing decision requires the corresponding contractual and balance-sheet inputs. The inventory literature motivates monitoring; this passive forecast comparison identifies no change in optimal quotes, hedges or realized funding requirements.

## Introduction opening after

> A position can finish inside its limit after exceeding that limit during the intervening period, as Figure illustrates. For a market maker, the relevant forecast therefore concerns the largest exposure before the next review, rather than the endpoint alone. The distinction changes the response variable, the observations available for training, and the interpretation of successful prediction. We study how established historical and conditional forecasts perform when every method targets this same sampled absolute-position peak.

