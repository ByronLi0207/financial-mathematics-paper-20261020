> **Final protocol supersedes preliminary suggestions below:** all six validation candidates are required for both regression methods; D3 is the conjunction of both original FX W2880 horizons H6 and H24. See protocol/v12/loss-decomposition-design.md at9679e15. Earlier audit proposals are retained as chronology, not execution settings.

# v12 model/API audit (read-only, before experiment execution)

Scope: v10 working directory on `revision-v12`; no numerical evaluation, fit, download, old-v3 access, protocol/source/result edit or Git-ref mutation was performed for this audit. Only this note is added. Frozen code is treated as the reusable baseline, rather than a refactoring target. Line references below refer to the current source files.

## Reuse the existing fixed-penalty forecast API

The most direct F1/F2 entry point at tau=0.95 is:

```python
v10_menu.forecast_report(position, times, features, cache, origins,
                        horizon, window, refit_step, method,
                        penalty=None, checkpoint=None)
```

`method` is `F`, `QR33` or `QR4`; finite QR penalties are positive real numbers. `penalty='inf'` is the exact ordinary empirical I report for QR33 and QR4. A numeric infinity is not an accepted finite solver penalty. The return value has `origins`, `capacity`, `refit_indices`, and a list of scalar `fit_diagnostics`. The wrapper delegates every finite case unchanged to `v8_mechanism_mc.forecast_report` (line 95), so it preserves both the QR33 arithmetic and the specific copied QR4 reduction/layout arithmetic. Build the reusable `features` with `conditional_features.build_features` and the reusable `cache` with `study_core.build_label_cache` once per source/horizon. Do not launch the original study drivers.

`v10_menu.select_candidate(records, method, expected_origins, menus)` (line 66) supports the exact menu `(.001, .01, .1, 1., 10., 'inf')`. Records must appear in that order and have `penalty`, `status`, `origin_count`, and `mean_loss`. Exact equal means prefer the stronger penalty, with `inf` last/strongest; there is no tolerance tie. QR33 requires all six complete validation candidates; QR4 selects among complete validation candidates, with no complete candidate making the cell ineligible. This differs from the earlier original-menu QR4 weak-penalty tie and must not silently revert to it. A v12 decomposition cell needs all five finite evaluation losses even where inherited QR4 validation selection remains eligible after another candidate failed; a missing required evaluation operand must not become a successful shortened decomposition.

`v10_menu.evaluate_method(...)` (line 124) performs validation and only the selected evaluation. Its write-once receipts, candidate inventory and exception handling are useful examples, but calling it alone does not produce the five finite evaluation losses F1 requires. A minimal new caller should run/cache fixed report segments, seal selection before evaluating the full menu, and form the decomposition from those full evaluation arrays. Cache identity must include method, penalty, horizon, window, refit step, tau, segment first and last origin, and source fingerprint. A cached failure is an attempted segment and must not be retried through another alias. Share the exact I arrays across QR33/QR4 rather than repeating empirical work. Reuse a previously completed artifact only after checking its bytes/hash, origins, definition and forecast clock; archived means alone do not demonstrate per-origin equivalence.

`supervisor_r6.CoreReports.segment(candidate_id, origins, *, window=None, refit_step=None)` (line 171) is an existing once-attempted, success-and-failure cache pattern. It issues QR33 only and has side effects that write into its supplied folder, so reuse its pattern rather than its R6 execution contract. `supervisor_e5_panel_run.segment(...)` (line 45) also implements QR33 only, fixed at H/W supplied, d=13, short=6, long=26 and gap=604800. Do not call that module's `prepare`, `contract_check`, `archived`, or execution entry point: these retain old-v3 lineage paths. The v10 QR adapter supports both QR33 and QR4 without that dependency.

## Exact model, scale, clock and score conventions

Let `B_t=abs(N_t)`, `Y_t=max(abs(N_t),...,abs(N_(t+H)))` and `Z_t=Y_t-B_t`. `study_core.build_label_cache` (line 229) constructs those labels, including the issue anchor, and sets label end to t+H.

For every contiguous segment starting at t0, refit origin is `r=t0+d*floor((t-t0)/d)`. A new validation/evaluation segment resets that anchor. The W training origins are `[r-H-W+1, r-H]`, inclusive, and their latest label ends exactly at r. Queries use the current issue t even when the pool and coefficients remain frozen at r. It is correct for the newest completed training label and current known anchor to share record r; this is not independent training/test observations. The primitive clock functions are `conditional_features.completed_training_indices` (line 94) and `refit_origin` (line 102).

The 33 causal predictors are N_t through N_(t-24), abs(N_t), short and long trailing RMS of changes, sin/cos hour, sin/cos weekday, and the indicator that the previous timestamp gap exceeds the nominal gap. QR4 uses exactly columns `[25,0,26,27]`, in that order: abs(N_t), N_t, short RMS, long RMS. Feature availability is `max(24,long_scale,short_scale)`. A frozen fit standardizes each selected predictor using only its W mature rows, population standard deviation (ddof=0), and constant-column scale 1. QR33 calls `fit_feature_transform` and `transform_features`; QR4 computes means/standard deviations on its copied four-column array to match the original arithmetic. No normalization uses the whole source or query block.

`response_scale(headroom, anchors)` (line 108) gives `s=max(mean(Z_pool),1e-6*mean(abs(N_pool)),1e-12)`. With standardized feature z, the solver fits:

\[
\min_{a,b}\; W^{-1}\sum_{i\in pool}\rho_\tau(Z_i/s-a-z_i^\top b)
             +(\lambda/2)\|b\|_2^2.
\]

The intercept a is unpenalized. This is a penalty on the coefficients of the standardized, response-scaled problem; it should not be described as the same lambda on raw native-unit slopes. Issue capacity is `B_t+max(0,s*(a+z_t'b))`. The mature ADMM/Fenchel-gap implementation is `conditional_quantile.fit_quantile_ridge` (line 166); its own docstring gives the optimization references. Defaults remain max_iter=10000, atol=1e-6, rtol=1e-5 and gap_rtol=1e-6. Acceptance requires both primal/dual residual conditions and the feasible-dual gap threshold. Numerical failure raises `QuantileFitError`; no fallback output is returned.

`empirical_headroom.predict(positions, origins, horizon, window, refit_step)` (line 36) issues both I and F using the same frozen mature pool, preserving duplicates, and reanchors each issue at B_t. At tau=19/20, I uses `ceil(19W/20)` and F uses `ceil(19(W+1)/20)`. I is the lower empirical pinball minimizer when the minimizer is an interval. `v10_menu.forecast_report(...,'inf')` returns I exactly; it is not corrected-rank F and is not an approximate finite-penalty fit. Both empirical and model reports project to the issue floor B_t.

`conditional_study.score_predictions(peak,capacities,floors,origins)` (line 205) scores aligned complete vectors with `rho_.95(Y-C)=.95*max(Y-C,0)+.05*max(C-Y,0)`. A breach is strictly Y>C. There is no tolerance in the strict breach count. `summarize_scores` (line 217) and `study_core.stable_mean` use the preserved constant or math.fsum/n convention. Means and percentages must remain per-source-cell; do not pool native-unit losses across contracts or weekly series. The positive overrun and overprediction components are nonnegative, but the new differences between model mean losses need not be.

## Tau sensitivity requires a small new shell

The accepted solver supports any finite `0<tau<1`. The upper APIs `v8_mechanism_mc.forecast_report`, `conditional_study.conditional_forecast`, `conditional_study.score_predictions`, `StudyConfig`'s rank validation, and `empirical_headroom.ranks/predict` are fixed at .95. Passing tau to the solver alone would leave the empirical baseline/scoring inconsistent. Avoid monkeypatching and changing these frozen modules.

The minimal v12 tau shell should preserve the same feature/scale/clock/projection steps, call the unchanged solver with the declared tau, and compute F/I on the same mature headrooms with exact integer rank arithmetic. `study_core.exact_rank(n,numerator,denominator)` (line 70) already supplies `ceil((n+1)*numerator/denominator)`; I uses the corresponding `ceil(n*numerator/denominator)`.

There is a real convention conflict in the task: at W52/tau=.99, `ceil(53*.99)=53`, so the original corrected rank is unavailable, and `empirical_headroom.predict` explicitly rejects it. Calling the sample maximum requires the explicit new convention `j=min(W,ceil((W+1)*tau))`. The coordinator has chosen this v12-only cap in response to the task's explicit historical-maximum requirement, with a disclosure that it supplies no coverage guarantee. At W52/.99 both capped F and I are the sample maximum. Test tau=.95 equivalence of the new shell to the unchanged adapter on constructed inputs after the design commit.

The existing general scorer `v6_inference.pinball_losses(actual,forecast,*,tau)` (line 70) is reusable for F3. It constructs both decimal weights using `Fraction(str(tau))`; at .95 they match the frozen 19/20 and 1/20 arithmetic. This avoids unnecessarily replacing .05 with the different float result of `1-.95`. Retain the usual floor/alignment validations around it and use `stable_mean` for means.

## Existing sources and trace locations

| Source | Existing input and immutable provenance | Inherited geometry |
|---|---|---|
| CFTC17 | `results/v10/cftc/sources.json` pins the 17 `sources/s00.npz` through `s16.npz`; keys are position, actual_dates and model_dates. Use model_dates for the inherited feature clock; use actual_dates for dates shown to readers. | N877, H6, W52/260, d13, RMS6/26, nominal gap604800. Validation553..604 (52); evaluation611..870 (260), six unissued origins. |
| Treasury bill | `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv`; SHA 9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb, 23315 bytes. Loader: `conditional_sources.load_source(path,'nyfed_weekly',expected_sha256=...,expected_bytes=...)` (line155). | N706, H6/24, W52/260, d13, RMS6/26, gap604800. Validation329..380; evaluation405..681 (277). Primary bill is H6/W260. |
| NY Fed panel12 | Eligible keys and per-source hashes in `results/supervisor-20261023/e5/inputs/panel/selection-manifest.json`. `round2_panel_sources.align_source(raw,key,grid)` (line11) strictly aligns to the bill's immutable706 dates; no fill or splice. | Same H/W/clock/splits as bill. Longer raw files have707 rows; only the fixed706-date grid is used. |
| FX hourly | SHA b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa,1286391 bytes. Loader `conditional_sources.load_source(...,'fx_hourly',...)`. | N18576, H6/24, W720/2880, d24, RMS24/168, gap3600. Original validation10463..11902 (1440), evaluation11927..18551 (6625). R6 retro validation7535..8974, evaluation8999..10438 (1440). |

The old R6/E5/E3 private roots named in their original manifests do not exist at the original relative paths in this v10 checkout. Their copied evaluation traces do exist under `.scratch/v10/loss-inputs/`, with explicit copied-path mappings in `notes/v10/loss-input-inventory.json` and `.scratch/v10/copied-private-inputs.json`. All407 entries in `minimum_core_private_copy_manifest` were found present by existence check;195 identify R6 traces and48 identify E5 evaluation traces. This check did not independently rehash those407 artifacts.

Examples of usable local copies are:

* `.scratch/v10/loss-inputs/supervisor/r6-20261023/run/inspected/inspected-PDPOSCS-TOT-h24-w260/10-405-681-w260-d13.npz`
* `.scratch/v10/loss-inputs/supervisor/supervisor-round2-20261023/e5/cells/PDPOSCS-TOT-h24-w260/numeric-traces.npz`
* CFTC public traces: `results/v10/cftc/complete-traces/s00-W52-QR33.npz`, and complete per-method receipt/trace pairs under `results/v10/cftc/formal/units/s00/W52/`.

Original R6 archive metadata: `results/supervisor-20261023/r6/private-archive-manifest.json`; R6 validation candidates/selected IDs and public evaluation summaries: `inspected-cells.json` and `retro-cells.json`. Original E5 per-cell selection-before-evaluation and candidate metadata: `results/supervisor-20261023/e5/cells/{key}-h{H}-w{W}/`. The minimum private copy inventory includes selected evaluation traces rather than every unselected finite evaluation report; F1 cannot be obtained solely by rescoring that set of saved selected forecasts.

The source inventory also identifies already-downloaded raw source copies in the separate **v9** directory (all14 listed files currently exist):

* FX: `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/1hourNetPositionsKaggle.csv`.
* Panel: `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/{key}.csv`.
* Bill: that v9 directory's `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv`, with the existing v10 copy preferred.

Use inventory-pinned hashes/byte counts when creating any caller-owned v12 input snapshot. No old-v3 read or new download is necessary. This audit checked existence, not source-byte hash equality, for the14 v9 source files.

CFTC uses Monday00:00 model labels for features, but economic dates are normally Tuesday; model dates are not public availability times. `results/v10/cftc/splits.json` records both. Its actual validation dates are2020-08-11..2021-08-03; actual evaluation origins2021-09-21..2026-09-08, with the last H6 target ending2026-10-20. This is downloaded-vintage economic-position-date replay, rather than a first-release tradable backtest.

The two FX periods are already fixed in R6. Its original-primary replication additionally compares QR/W2880/d24 against rolling F/W720/d1, which differs from the matched F/W2880/d24 comparison. Freeze this distinction explicitly for F3 and keep matched-reference and original-primary contrasts separately named. The task's bill main comparison is the inspected H6/W260 comparison; retro W52 is only a structural analogue, not an exact W260 primary replay.

## Resource and interpretation risks before running

F1 declares90 source/H/W groups (34 CFTC+48 panel+4 bill+4 FX),180 method cells, and five finite evaluation reports per method cell, plus validation selection and empirical I/F. With no reuse, finite QR segment fits total1800 across validation/evaluation; many refits occur within each segment. FX dominates because its original evaluation has6625 origins and W2880, while weekly segments have260/277 origins. Reuse features/labels and exact cached fixed reports, keep the sole-attempt discipline, and retain the predeclared FX-first/panel-W260-second truncation order. The one-contract timing pilot must cover both W and both QR methods to be a meaningful projection; any source-count projection still needs a conservative separate FX allowance.

Historical elapsed receipts give context only: CFTC's old complete formal run reported12.26 seconds with its existing worker arrangement; E5 reported37.59 seconds; R6 reported635.36 seconds and included many additional rolling folds. These are different workloads and cannot establish that the new full-menu evaluation or tau99 run will meet its cap. No timing or fit was performed by this audit. Tau.99 and weak penalties can stress solver convergence; preserve the10000-iteration cap and failure, with no retune or retry. Thread environment variables must be set before NumPy imports by the new worker. Existing guards use one numerical thread and observed-thread/RSS/time caps, not only a requested thread count.

The F1 identity is algebraically exact: `actual-F=(actual-finite_oracle)+(finite_oracle-F)`. Because actual may select I while the oracle excludes I, `actual-finite_oracle` may be negative; it is not universally nonnegative regret. Do not clip signed components, force a positive-only stacked bar, or describe a negative value as an error penalty. Finite-oracle advantage is an optimistic in-sample diagnostic, not deployable predictive selection and not proof of structural signal absence. Failure of a finite model menu is narrower than absence of every possible conditional signal.

The coordinator has specified the conservative threshold interpretation before execution: D1/D2 primary uses QR33 on41 W52 source/H cells (17 CFTC H6+24 panel H6/H24); QR4 is a separately labelled sensitivity. D1 is strict positive signal gap and D2 strict selection share>1/2; actual excess<=0 counts as nonsupport for D2, with signed error retained. D3 primary is FX H6/W2880, with H24 separately exploratory. Any unavailable required operand remains unavailable and cannot be removed to improve a completion-conditioned percentage. All threshold definitions, failure denominator handling, reference clocks and caps belong in the independently committed designs before execution.

F2's validation156 run should retain the original H6 unissued gap rather than append validation origins until evaluation: with evaluation starting611, validation ends604 and starts449. At its earliest validation refit, the W260 mature pool begins184, exceeding the feature prefix26; the same 17 current N877 contracts have sufficient conditional history under this geometry. Declare the general whole-contract exclusion formula `validation_first-H-max(W)+1 >= feature_prefix` before checking sources; do not replace a failing contract. Both evaluation origin sets and their t0=611/d13 clock remain unchanged across validation lengths. V1 medians must compare paired, same-contract QR33 relative losses; V2 needs a fixed denominator and strict higher infinity-selection fraction.
