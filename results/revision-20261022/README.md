# Fixed-selection conditional and historical comparisons

This checkpoint adds completed same-target conditional benchmarks and a separately defined official aggregate-position application. The manuscript revision is in progress. All frozen candidates, selected evaluations, historical references and adverse outcomes are retained; these are descriptive retrospective results, without a claimed new estimator or conditional-coverage guarantee.

## Main declared contrasts

Negative paired loss differences favor the left procedure. Values below are means in each source's native unit; FX USD and Treasury USD millions must not be pooled. Percentages use unrounded paired differences.

| Source / target | Left / reference | Left loss | Reference loss | Paired loss change | Breaches left / ref |
|---|---|---:|---:|---:|---:|
| FX, H6 records (primary) | QR W2880 / rolling_F W720 | 385,844.885 | 441,774.037 | -12.660% | 376 / 332 |
| FX, H24 records (legacy sensitivity) | QR W2880 / rolling_S W720 | 734,695.069 | 748,383.538 | -1.829% | 531 / 287 |
| Treasury bills, H6 weeks (primary) | QR W260 / frozen_F W260 | 4,159.673 | 2,758.665 | +50.786% | 54 / 28 |

The FX H6 primary improvement is 12.660%, accompanied by 376 rather than 332 strict breaches (5.675% versus 5.011%); mean positive overrun falls, so frequency and severity move differently. Against the same W2880 frozen-F history and refit schedule, QR also lowers loss by 14.767%. Matching the eligible pool does not isolate a causal effect of conditioning: functional form, local response count, regularization and validation selection still differ.

The FX H24 improvement is only 1.829% against the historical reference selected in the earlier study. It accompanies 531 versus 287 breaches and USD 167,864.232 greater mean positive overrun. The 2016 paired difference is -0.555%; the 363-origin partial 2017 is -33.007%. It is not a uniform calendar-period improvement.

The Treasury primary comparison is adverse: QR loss is 50.786% higher than matched frozen F and has 54 rather than 28 breaches. It loses in all five complete calendar years 2021--2025; the favorable 2026 group has only 16 origins. All four Treasury QR specifications lose to their matched-history F control. This contradicts a universal cross-source improvement claim.

## Complete selected conditional menu against matched frozen F

All 24 selected cells appear below. The reference uses the same eligible historical window and refit schedule. The public CSVs additionally retain all F/S/K controls, rolling/frozen update contrasts and one-state references. The two declared primaries above are not replaced by ex-post winners.

| Source | H | W | Family | Selected parameter | Mean loss | Paired vs frozen F | Breach % |
|---|---:|---:|---|---:|---:|---:|---:|
| fx_hourly | 6 | 720 | QR | 0.01 | 433,246.308 | -2.117% | 8.015 |
| fx_hourly | 6 | 720 | KNN | 180 | 436,444.693 | -1.394% | 4.815 |
| fx_hourly | 6 | 720 | SCALED_KNN | 360 | 466,292.291 | +5.349% | 4.060 |
| fx_hourly | 6 | 2880 | QR | 0.01 | 385,844.885 | -14.767% | 5.675 |
| fx_hourly | 6 | 2880 | KNN | 180 | 410,582.619 | -9.302% | 4.815 |
| fx_hourly | 6 | 2880 | SCALED_KNN | 180 | 426,458.421 | -5.795% | 4.121 |
| fx_hourly | 24 | 720 | QR | 0.01 | 1,035,482.755 | +31.504% | 13.947 |
| fx_hourly | 24 | 720 | KNN | 180 | 836,209.918 | +6.197% | 7.592 |
| fx_hourly | 24 | 720 | SCALED_KNN | 180 | 896,752.699 | +13.886% | 6.642 |
| fx_hourly | 24 | 2880 | QR | 0.001 | 734,695.069 | -3.758% | 8.015 |
| fx_hourly | 24 | 2880 | KNN | 180 | 769,767.987 | +0.837% | 6.883 |
| fx_hourly | 24 | 2880 | SCALED_KNN | 180 | 848,004.200 | +11.085% | 5.962 |
| nyfed_weekly | 6 | 52 | QR | 0.1 | 5,095.519 | +83.354% | 30.325 |
| nyfed_weekly | 6 | 52 | KNN | 52 | 2,779.054 | +0.000% | 3.971 |
| nyfed_weekly | 6 | 52 | SCALED_KNN | 52 | 4,208.293 | +51.429% | 3.249 |
| nyfed_weekly | 6 | 260 | QR | 0.001 | 4,159.673 | +50.786% | 19.495 |
| nyfed_weekly | 6 | 260 | KNN | 80 | 2,663.561 | -3.447% | 10.108 |
| nyfed_weekly | 6 | 260 | SCALED_KNN | 80 | 3,127.173 | +13.358% | 8.303 |
| nyfed_weekly | 24 | 52 | QR | 0.001 | 12,165.574 | +227.411% | 47.653 |
| nyfed_weekly | 24 | 52 | KNN | 52 | 3,715.693 | +0.000% | 11.913 |
| nyfed_weekly | 24 | 52 | SCALED_KNN | 40 | 5,625.667 | +51.403% | 11.552 |
| nyfed_weekly | 24 | 260 | QR | 0.1 | 5,204.760 | +109.843% | 30.325 |
| nyfed_weekly | 24 | 260 | KNN | 160 | 2,257.963 | -8.964% | 4.693 |
| nyfed_weekly | 24 | 260 | SCALED_KNN | 160 | 4,137.264 | +66.805% | 2.888 |

For Treasury W52, plain KNN selects k=52 at both horizons and is exactly frozen F at every origin. Its zero difference is a full-pool fallback, not evidence of useful rich-feature membership. Scaled KNN with k=W still changes response scaling; its neighbor distances do not affect membership. Long-window menus do not contain k=W. Corrected ranks and QR empirical loss minimization also differ in finite samples: for k=52, ceil((k+1)*.95)=51, whereas the ordinary .95 empirical quantile has rank50.

Treasury KNN W260/H24 improves on frozen F by 8.964% on all 277 origins, but the fixed H+1 grid reverses the difference to +10.842% on just 12 origins. This adverse sensitivity is retained. No selected conditional Treasury model is descriptively below every retained reference at its horizon; that whole-menu observation does not create a new primary selection.

## Files and acceptance evidence

- [Validation summary](validation-summary.csv): all72 candidates, including selected and full-pool flags.
- [Evaluation summary](evaluation-summary.csv): all90 conditional/reference method rows.
- [Annual method summaries](evaluation-annual.csv):372 rows.
- [Global H+1 method summaries](evaluation-nonoverlap.csv):90 rows, not independent observations.
- [All declared paired comparisons](paired-comparisons.csv):98 rows =72 matched-history +24 update-frequency +2 FX primary/legacy. The Treasury primary is already one matched-history row, not duplicated.
- [Annual paired means](paired-annual.csv):388 rows, computed within common origins, not by subtracting rounded tables.
- [Global H+1 paired means](paired-nonoverlap.csv):98 rows; grids start at the global evaluation beginning and never reset by calendar year.
- [Validation audit](validation-audit.json), [first evaluation audit](evaluation-audit.json), and [tightened evaluation audit](evaluation-audit-02.json).
- `validation-*.json`, `evaluation-*.json`, `references-*.json`: all56 accepted public-designated phase receipts, including source identity, origin fingerprint, numerical acceptance and measured resources.
- [External source and timing](EXTERNAL_DATA.md): exact downloaded version, units, issue and last-label dates, release lag, aggregation and reuse limits.

The first evaluation audit reconciled accepted private traces with independently computed direct maxima and all public summaries. A code review then tightened metadata lower-bound, finite-value, selected-parameter and terminal checks, and bound parsing to the already-hashed byte snapshot. The second audit verified all38 existing exported tables/receipts byte-for-byte unchanged. The [first audit builder](audit-builder-v01.py) is retained at its recorded source hash; the current [builder](../../build_conditional_results.py) and [adversarial tests](../../test_build_conditional_results.py) implement the tightened checks. Neither audit refits forecasts. Public diagnostic hashes identify coefficient/dual vectors; those vectors are not exposed here, so public-only metadata review is not an independent reconstruction of every hidden fit.

Financial validation workers used at most69,746,688 bytes peak RSS and evaluation/reference workers at most67,584,000 bytes. The maximum single evaluation/reference phase took15.827 seconds. The observed worker-thread maximum was1 at recorded snapshots; this is not a continuous OS thread bound or a hard memory sandbox. Audit-process resources are reported separately. The worker times are compute measurements, not authorial research hours.

## Frozen design and reproduction boundary

The [design](../../protocol/revision-20261022/conditional-baseline-design.md), [machine specification](../../protocol/revision-20261022/study-spec.json) and [executable freeze](../../protocol/revision-20261022/executable-freeze.json) were publicly present at commit `1bd5b692fd9cb240763c032fb4e1c203871fad55` before first validation. The [complete selection freeze](../../protocol/revision-20261022/selection-freeze.json) was publicly present at `8ce6e398a17e4c12cb36a9a76785e78fd21a1da0` before selected evaluation. The original FX evaluation archive had already been inspected in the preceding study; freezing this extension does not make those observations fresh prospective data.

Use Python with NumPy and the repository runners. Source files are not redistributed: obtain the original FX version and accepted Treasury snapshot through their source routes, then require the exact byte counts and SHA-256 fingerprints in the specification before parsing. The Treasury endpoint may revise or expand; a changed download supports a separately versioned rerun, not exact reproduction of the accepted snapshot. Do not silently truncate, splice aliases, overwrite accepted bytes or relabel current data as the historical version.

Archived-selection verification requires restoring the exact public `validation-*.json` bytes to the task-relative `validation_receipts[].path` entries in the selection freeze; refuse an existing different file. A newly executed validation receipt contains new timestamps/resources and is not expected to have the archived receipt hash even if its numerical results agree. The runner checks the archived selection against the archived receipts; new replication validation should be retained separately and compared without replacing the original evidence. A consolidated replication launcher and revised manuscript are still being prepared at this checkpoint.

The Treasury application is a downloaded-vintage, economic-as-of-index replay of an aggregate market-value series, not a second individual dealer, independent labels or a live public-information backtest. H6 and H24 mean six and24 weekly records there; their last labels are2026-06-03 and2026-10-07 respectively, with the same last issue date2026-04-22. No cross-source monetary mean, confidence interval, p-value, conditional-coverage guarantee or operational profit/capital/funding saving is inferred.

© 2026 Federal Reserve Bank of New York. Content from the New York Fed subject to the Terms of Use at newyorkfed.org.
