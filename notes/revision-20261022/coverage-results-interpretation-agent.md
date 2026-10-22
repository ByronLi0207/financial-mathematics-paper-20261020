# Interpretation review of the completed fixed-terminal coverage diagnostic

22 October 2026. Reviewed only the completed attempt's public `coverage-evalue-summary.csv`, `coverage-evalue-phases.csv`, `coverage-evalue-manifest.json`, and `state/revision-20261022/coverage-independent-readback-01.json`. No raw source, NPZ payload, new statistic, model, test, or alternative diagnostic was accessed or computed. Numerical values below are copied from those aggregate exports.

The attempt is `coverage-evalues-fixed-terminal-20261022-01` under the already specified replica root. The manifest reports `COVERAGE_EVALUE_COMPUTATION_VERIFIED`; the separate receipt reports `COVERAGE_INDEPENDENT_READBACK_PASS`, with all 56 summary rows and 896 phase rows checked using the distinct integer formula. That receipt is evidence of computational verification, not coverage validation. Both records explicitly retain post-result exploratory status and withhold retrospective empirical 5% family-wise error control.

## Recommendation

A concise Appendix D and one body pointer are useful. They add a dependence-conscious, fixed-terminal diagnostic of a narrowly stated conditional strict-breach upper-bound null, without using stationarity to justify its expectation argument. They also expose an important limit of interpreting non-crossings. This should remain a bounded supplementary audit, rather than a new-method claim, a new winner-selection rule, or a replacement for the original pinball and breach summaries.

Keep all 56 cells and all phases available. A compact complete-family table or the linked complete CSV is preferable to showing only favorable or crossing cases. The main text needs only the four-crossing finding and the explicit warning that the other 52 cells are not certified as covered. This does not warrant a new central contribution or an abstract-level assertion of validated conditional coverage.

## What the four crossings add

The reference threshold is 1120 for every cell. The four recorded crossings are:

| Source | H | W | Report | Breaches / origins | Displayed terminal e-value |
|---|---:|---:|---|---|---:|
| FX hourly | 24 | 720 | QR | 924 / 6625 | 8.499112682788e7 |
| Treasury weekly | 6 | 52 | QR | 84 / 277 | 1.310958812771e8 |
| Treasury weekly | 6 | 260 | QR | 54 / 277 | 2.204375927802e3 |
| Treasury weekly | 24 | 52 | QR | 132 / 277 | 3.814063640027e4 |

These are four QR configurations, not a finding that every QR configuration fails, and not four independent replications. Configurations share sources and overlapping targets; the family also retains structural aliases as distinct labels. The result supports a specific additional exploratory warning about the listed issued-report configurations under the declared null. It does not identify a causal failure mechanism or particular failure date.

The correct wording is that four cells **cross the declared fixed-procedure reference threshold in this late exploratory calculation**. Calling them four empirically established family-wise-error-controlled discoveries would remove the very selection qualification recorded in the manifest. Public freezing before this calculation prevents later drift, but does not erase the prior inspection of forecasts, scores and breach summaries or selection of the method family and diagnostic.

## The 52 non-crossings are not a coverage PASS

Treasury H24/W260 `AR1_REPLAY` is the clearest cautionary example: the summary records **59 breaches among 277 origins** and terminal value **11.02843045843**, below 1120. It would be misleading to mark this report calibrated, adequate or safe merely because it does not cross the reference threshold. The value is not a posterior probability or a model-quality score. Its non-crossing also does not rebut the adverse observed breach count or establish the conditional null.

The phase export shows why limited accumulation is a serious consideration here: the H24 construction averages 25 phases containing only 11 or 12 origins each. The AR phase values range from small values for zero-breach phases to larger values for four-breach phases; all retain their fixed averaging weights. This illustrates the information cost of the delayed construction and the demanding reference threshold. It is not a measured power study, and no numerical power claim follows from these counts alone. Do not repair the non-crossing by pooling dependent phases multiplicatively, selecting a phase, shortening the delay, or lowering the threshold after seeing it.

Small e-values likewise do not establish that a report is close to the optimal quantile. An overly conservative report can have few strict breaches and a small one-sided evidence value while paying a substantial pinball or capacity cost. The original score preference and adverse cases remain essential.

## Equal total breaches can yield very different evidence values

Two Treasury QR summaries both record **84 / 277**:

- H6/W52: seven phases, terminal value **1.310958812771e8**, crossing the reference threshold.
- H24/W260: 25 phases, terminal value **59.42352425352**, not crossing it.

The phase tables are materially different. H6/W52 has 39 or 40 origins per phase; its displayed phase values include 9.168243462732e8 for the phase with 16/40 breaches. H24/W260 has 11 or 12 origins per phase; the displayed phase with 5/11 breaches has value 8.265263347763e2, and the remaining phases have different breach counts and values.

The final statistic averages nonlinear whole-product mixtures computed separately within phases. It is therefore not a function of the full-cell pair (277,84) alone. Different phase lengths and allocations of breaches change the amount and pattern of evidence accumulated. Moreover, these are different horizon/window report tasks, not the same forecast sequence repartitioned in an otherwise controlled experiment. The aggregates do not identify a single causal explanation for the entire numerical difference.

This contrast is worth one explanatory sentence in Appendix D. It rules out ranking calibration quality across horizons by terminal e-value magnitude, treating a lower e-value as better forecasting, or interpreting non-crossing as vindication of the longer-horizon QR report. Do not tune the phase rule or select an alternative aggregation after observing this contrast.

## Suggested scientific emphasis

The added result is a narrow negative/diagnostic check: selected QR configurations produce large terminal evidence values under a procedure whose fixed-design expectation argument accommodates dependence. The non-crossing AR and equal-count QR examples should accompany it so readers see what the statistic does and does not resolve. Preserve the exact rational outputs and complete family in the supplement; use rounded values only for presentation.

One body pointer can state that the supplementary late fixed-terminal audit has four reference crossings, all QR, while non-crossings do not establish coverage. Appendix D can give the null, fixed-delay mixture construction, complete-result location, the four-row reference table, and the two cautionary comparisons above. No anytime claim, retrospective FWER certificate, cross-model e-value ranking, inferred financial benefit, or new holdout claim is supported. The added appendix improves the paper's reliability assessment; it does not fill its independent dealer-data, decision-cost or originality gaps.
