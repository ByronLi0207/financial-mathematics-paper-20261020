# V5 exploratory analysis design

Frozen before either financial-data experiment is run. All analyses are **post-result / exploratory**. The two original primary comparisons, old archives, old source files and old manuscript numbers are unchanged.

## 1. Arithmetic decomposition

Read the immutable `results/revision-20261022/paired-comparisons.csv` bytes (SHA-256 `a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9`). Match the FX H6 QR W2880 versus rolling F W720 and versus frozen F W2880 contrasts. Require their QR loss, origin count, first origin and last origin to match exactly as decimal tokens. Let R, F and Q be those archived mean losses. Compute F−R, Q−F and Q−R in native USD; express all three as percentages of R so they add. Separately show (Q−F)/F, the existing matched comparison. This is a descriptive bridge across combined history and update changes; it does not causally identify a pure history or update effect. Repeating percentages with different denominators cannot provide an additive decomposition.

## 2. Deliberate label-maturity violation

Only two existing H6 long-window source cells are used: FX W2880 and original Treasury-bill W260. Keep original frozen QR and KNN selections (`selection-freeze.json`), original 33 causal features, projection, inverted-CDF order ranks, solver acceptance, normalization and update schedules. F denotes the frozen-refit historical-headroom report. No new tuning or method-selection step is allowed.

Before reading forecast outcomes, select the first, middle (floor middle index), and last **complete** original refit block from each original evaluation interval. FX has 276 complete blocks of 24 issues: starts 11927, 15215 and 18527, totaling 72 issues. Treasury has 21 complete blocks of 13 issues: starts 405, 535 and 665, totaling 39 issues. The terminal incomplete block is excluded by the clock rule rather than its performance. The samples are descriptive slices, not the complete evaluation archive, not independent observations, and not a new primary.

At each selected original refit r compare the W origins ending at r−H (**clean**) with W origins ending at r (**oracle-leakage, intentionally invalid**). In the latter pool exactly H labels end after refit, with the most recent ending at r+H; these future values are read only for this negative-control demonstration. The artificial leak is anchored at the actual refit r even for later queries in its block. Some leaked labels will mature later during the block, but none were available when its coefficients or historical pool were fixed. Features are separately scaled on each method's designated training pool, matching the corresponding naive procedure. All three methods and both pools are scored on exactly the same issues.

Record clean and illegal mean pinball loss, strict breaches, U and V; the illegal-minus-clean native and percent loss difference, not a predetermined “inflation.” Improvement, no change and deterioration are all publishable outcomes. If any selected fit fails, retain its error code; do not shorten its block or replace a parameter. A failed method/source has no complete three-block score. Each source experiment has its own 540-second internal deadline, 600-second maximum, one numeric thread and RSS bound of 2 GiB; actual wall time and high-water RSS are recorded. No full-sample extension or outcome-dependent resampling is planned.

## 3. Reproducible motivating window

Prefer the public NYFed original bill series. Using clean H6 frozen F W260, inspect the original evaluation origins in ascending order and select the first with `abs(N[t+H]) <= C_F[t] < max(abs(N[t:t+H+1]))`. Retain the actual signed path and dates for the selected NYFed window, its known floor, constant issued report, endpoint and sampled peak. This is a deterministic illustration, not an extra holdout or a claim about typicality. It demonstrates that an endpoint can remain inside an issued limit while a sampled path peak exceeds it. It does not demonstrate an intrarecord peak.

## Inputs, tests and resources

Raw snapshots must match the original spec byte count and SHA-256 before parsing. FX raw data and per-origin FX forecasts will not be published; outputs contain aggregate source summaries only. NYFed illustration has source provenance and is subject to the package's source-rights check. Financial-data scripts open outputs exclusively and never overwrite old results. Unit tests are written first; RED collection fails with `ModuleNotFoundError: No module named 'v5_analysis'` (seven tests not yet executed). Full RED and subsequent GREEN receipts are saved in the new result directory. No software is installed into a system environment; pytest is used through the already authorized temporary uv environment.
