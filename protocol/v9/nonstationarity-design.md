# C2 preregistration: parameter-instability diagnostics and paired switching simulations

**Status:** written and to be committed alone before any new real-series diagnostic, AR/GARCH fit, bootstrap or synthetic forecast calculation. Metadata-only source inspection and the unchanged baseline software suite have already run. The study is retrospective and motivated by inspected financial results; local freezing is not prospective or independent validation.

## 1. Question and mature methods

Can instability observed before each original evaluation period, calibrated into a parameter-switching process, reproduce the large QR losses against corrected-rank F? We do not assume that low-frequency losses identify instability, nor that a fitted breakpoint is a policy or institutional event.

The sole global statistic is Hansen's (1992) joint OLS score-instability statistic for an AR(1) with intercept. Its score includes the intercept, AR slope and residual-square channels. We use the statistic implemented by `statsmodels.stats.diagnostic.breaks_hansen`, not its tabulated iid critical values. Brown–Durbin–Evans CUSUM and Inclan–Tiao ICSS are reviewed but not run as alternative tests after seeing outcomes. Their usual thresholds are not automatically valid for GARCH/t data.

Primary references verified before registration:

- Hansen (1992), *Journal of Policy Modeling*14(4),517–533, DOI10.1016/0161-8938(92)90019-9, [author paper](https://users.ssc.wisc.edu/~behansen/papers/jpm_92.pdf); [official statistic/source](https://www.statsmodels.org/stable/_modules/statsmodels/stats/diagnostic.html#breaks_hansen).
- Brown, Durbin & Evans (1975), DOI10.1111/j.2517-6161.1975.tb01532.x, and Inclan & Tiao (1994), DOI10.1080/01621459.1994.10476824, for the classical alternatives and their assumptions.
- Sanso, Arago & Carrion-i-Silvestre (2004), *Revista de Economia Financiera*4,32–53, [original paper](https://aefin.es/wp-content/uploads/2019/02/A4-2_443809.pdf), for heavy-tail/conditional-heteroskedasticity warnings.
- Davison & Hinkley (1997), Chapters4/8, DOI10.1017/CBO9780511802843.005 and .009; Dufour (2006), DOI10.1016/j.jeconom.2005.06.007, for model-based bootstrap and nuisance-parameter limits.
- Bai & Perron (2003), DOI10.1002/jae.659, and Yao (1988), DOI10.1016/0167-7152(88)90118-6, motivate bounded segmentation/model selection. Our separate-variance AR quasi-likelihood locator is a descriptive recipe, not the full Bai–Perron GARCH test or an application of Yao's independent-normal consistency theorem.

The source-verification record and independent pre-design review are in `notes/v9/literature.md` and `design-method-review.md`. This study combines mature tools; it claims no new test or estimator.

## 2. Inputs, cutoff and units

Only existing pinned local inputs in `notes/v9/input-boundaries.json` are allowed. No network acquisition is permitted. Treasury and the12 accepted panel series are aligned by the unchanged `round2_panel_sources.align_source` to the same706-date grid. Each diagnostic/calibration takes raw indices0..404:2013-04-03..2020-12-30, strictly before original evaluation index405/2021-01-06. No skipped panel source is added.

Daily FX is recreated by the unchanged WP4 `resample_closed_days`: source-naive nonempty dates, last recorded position, issue at day end, no timezone conversion, filling or interpolation. The full930-day aggregation must reproduce the saved fingerprints before its prefix is used. Daily indices0..404 end2015-05-22; original evaluation begins index405 on2015-05-24. Full aggregation is data preparation, not a new financial forecast evaluation, and no evaluation value is used by diagnostics/fits.

For N4, use a common calendar interval `[2014-02-05T00:00,2015-05-24T00:00)`: daily405 observations and hourly indices0..8108 (8109 observations; last2015-05-22T21:00). This hourly prefix is also strictly before original hourly evaluation11927/2016-01-01. We deliberately do not compare the longer hourly11927-prefix with the shorter daily period. Arrays, daily mapping and raw FX remain private; public outputs contain aggregate diagnostics, parameters and fingerprints.

There are15 diagnostic rows:13 weekly,1 daily FX and1 matched-period hourly FX. No new real-data predictive evaluation is run.

## 3. Global stability screen and fitted-null qualification

For n levels, form M=n−1 pairs `(x_t=(1,N_(t−1)), y_t=N_t)`. Re-estimate unconstrained OLS for the statistic. Let e_t be its residual, f_t=(x_t e_t, e_t^2−mean(e^2)), and S_k=sum_(t<=k)f_t. The Hansen statistic is `trace((M*sum f_t f_t')^(-1)*sum S_k S_k')`. Use the official implementation after harmless sample scaling. For conditioning diagnostics, rescale score columns by their RMS; if their correlation matrix is singular or has condition number>1e12, the primary diagnostic fails. Do not silently ridge the statistic.

Fit a constant-parameter AR(1)-GARCH(1,1)-standardized-t null once on the eligible prefix, using the two-step procedure in Section5. Qualified primary calibration requires nu>4 and `q4=alpha^2*kappa+2*alpha*beta+beta^2 < 1−1e−8`, with `kappa=3*(nu−2)/(nu−4)`, in addition to finite second moments and successful optimization. A failed fourth-moment gate is `NONREGULAR_NULL`, not evidence of stability or instability. Its primary p is unavailable. It does not prevent descriptive segmentation or finite-second-moment stress simulation if the underlying fit is admissible.

For each qualified null, simulate exactly999 independent paths of the same length after burn20000, recursively generating their levels and own lag regressors. Re-estimate OLS and H on every path. The statistic does not use estimated GARCH filtering, so the null generator is fitted once, not refitted999times. Set `p=(1+count(H_boot>=H_observed))/1000`. Save exceedance count, seed/RNG state, all bootstrap H values and Monte Carlo standard error. Do not add draws near a threshold. Any required bootstrap numerical failure makes that diagnostic unavailable; do not drop/re-draw paths.

This is a plug-in model-based approximation, not an exact finite-sample5% guarantee. Qualification does not establish that the real process has the assumed moments or distribution. Rejection may reflect model misspecification, nonlinear behavior or outliers as well as parameter change. No additional diagnostic family will be selected after results.

## 4. Significance, multiple testing and descriptive break localization

Pointwise alpha=.05 is fixed. N1 is the suggested descriptive threshold: at least7 of the13 weekly rows reject with qualified raw p<=.05. Report Holm13 adjusted p alongside, preserving the family size13; unavailable rows use p=1 only inside the adjustment and retain their unavailable labels. Do not treat that placeholder as evidence of stability, pool series as independent observations, or attach a binomial p to the count. For missing diagnostics, the number of rejections has lower/upper bounds: N1 is supported only when the known lower bound>=7, unsupported when the upper bound<7, and otherwise unassessable. Daily/hourly form a separate2-row descriptive comparison, not part of Holm13.

Locate candidate regimes with one fixed descriptive algorithm, independently of whether the global screen is qualified or rejects. M=n−1 transitions are partitioned into k+1 contiguous segments, k in{0,1,2}. Each segment has at least `max(104,ceil(.20*M))` transitions. For each legal partition, fit an intercept and slope by OLS on that segment's target transitions, allowing the first target after a break to use the preceding observed level. Cost is `sum_j m_j*log(RSS_j/m_j)` and criterion adds `(3+4*k)*log(M)` (intercept, slope, variance per segment and a per-break location penalty). Exact dynamic programming/exhaustive integer search finds the minimum for each k without a dense M-by-M array. Within1e−10 ties choose fewer breaks, then lexicographically earliest cuts. Nonpositive residual variance or singular segment design is inadmissible, not repaired by a variance floor.

Report the selected k, dates and minimum segment sizes, plus whether the k=2 cap is reached. These are descriptive calibration partitions; no individual break is called5%-significant and no selected child-node p is reported. A global rejection with k=0 is possible; a descriptive partition with an unavailable global p is also possible. Neither is silently relabeled.

N4 retains the requested rule: qualified daily raw p<=.05 and daily selected k/n strictly exceeds hourly k/n. Both rows must have qualified p and a valid partition; otherwise N4 is unassessable. Also report breaks per calendar year using the common interval. Per100-observation density has a mechanical clock/sample-size effect and a max2 cap; it does not identify greater instability per unit economic time.

## 5. AR/GARCH calibration, scale and failure

Whole-prefix null calibration applies to all15 diagnostic rows. Segmented stress calibration and forecasting apply only to the13 weekly sources: fit one whole-prefix constant control and one AR-GARCH-t parameter vector per selected descriptive segment. Divide levels by their whole-prefix population SD for numerical scale but do not subtract their mean; this preserves the sign/absolute-position anchor geometry. Record that scale. The AR intercept and slope minimize squared residuals with `|phi|<=.999`: use the exact profiled constrained least-squares solution, report any boundary hit, and do not fit then silently clip. Each segment uses its designated global target transitions, including the lag observed just before its first target.

Divide fitted AR residuals by their population SD, then fit a zero-mean GARCH(1,1) with standardized Student-t innovations using arch8.0.0. Impose `alpha+beta<=.999` as an explicit optimization constraint from the outset; use the library's nu bounds[2.05,500], maxiter2000, ftol1e−9, one default-start fit only. Transform omega back to the normalized-level units by the squared residual scale. Report convergence/status, parameters, restrictions and boundary hits. The constraint is a declared stationary approximation, not proof of real stationarity; no fourth-moment constraint is forced into the fitted generator. Mark restricted-boundary estimates as BOUNDARY_FIT even when the moment gate passes: qualified means only the registered numerical/moment gate, not an interior nuisance estimate or exact bootstrap size.

Generation requires finite coefficients, positive omega, nonnegative alpha/beta, alpha+beta<1 and nu>2. A nonconverged/invalid whole fit or required segment fit is failed; no alternative starts, solver, distribution or segment count is tried. Whole-fit failure makes its qualified diagnostic and all its paired simulation cells unavailable. Segment-fit failure makes the switching cells unavailable. Do not substitute a no-break fit to rescue a switching cell. A k=0 partition reuses the exact whole parameter vector, so the two arms must generate identical paths under common uniforms.

## 6. Paired parameter-switching stress DGP

For arm j at time t, use `N_t=c_j+phi_j*N_(t−1)+e_t`, `h_t=omega_j+alpha_j*e_(t−1)^2+beta_j*h_(t−1)`, `e_t=sqrt(h_t)*z_t`. First variance is1, preceding level0. Standardize t shocks to unit variance with `sqrt((nu_j−2)/nu_j)`. At a switch, retain the previous level, variance and innovation; do not reset or reburn.

The constant arm uses the whole-prefix fit throughout. The switching arm cycles the fitted regimes using their original M=n−1 transition dwell lengths. Rep r has predetermined phase `floor(r*M/R)`, not a phase chosen after observing loss. For full generated index i, regime position is `(phase+i−burn_in) mod M`; thus both burn and retained paths follow the same schedule, and retained index0 has the registered phase. Repeat the schedule for burn20000 plus retained3264. The last-to-first wrap is an artificial transition and must be marked separately from forward fitted transitions. Report all transition/exposure counts in training/validation/evaluation; do not filter or reweight reps based on exposure.

This is a conditional parameter-switching stress process with a deterministic phase grid, not a literal replay of history or a proof of mathematical nonstationarity. The once-stretched alternative would put the evaluation near the final stable segment under the required WP3 geometry; it is not run as a second chance. Both arms use the same source, rep, open-uniform vector; transform each U through the appropriate t inverse CDF and variance normalization. Different nu does not mean the same t vector. The innovation law and estimated calibration distinguish C2 from WP3's controlled normal DGP; within C2 the two arms share the same estimation restrictions and model family. Whole-prefix and segment fits need not have equal unconditional moments.

## 7. Unchanged forecast experiment contract

Reuse WP3 forecasting, features, selection and score functions unchanged. H6; W52/260; tau19/20; retained3264; artificial hourly clock beginning2000-01-03T00:00; RMS24/168, valid168; nominal gap3600; refit24. Validation3072..3143 and evaluation3168..3239 each have72 complete origins. All labels use the issue state and future six records; no unresolved target enters training. Query features/floor are current while training transforms and coefficients stay frozen inside blocks.

Only corrected-rank F, QR33 and QR4 are computed. QR33 menu .001/.01/.1 requires all mandatory validation candidates to complete and breaks exact ties toward larger lambda. QR4 menu .001/.01/.1/1/10 selects among completed candidates and breaks ties toward the first/smaller lambda; failed candidates remain. These policies, ADMM tolerances/maxiter10000 and initialization are inherited literally from WP3. I, S, local quantiles and other forecast families are not added.

There are104 conditional source/arm/W/method cells (13*2*2*2), plus52 corresponding F cells. Each intended conditional cell has32 repetitions before the timing-only ladder. A failed mandatory candidate, selected evaluation, required F report, numeric path or resource limit propagates its source/arm/W/method cell to FAILED. No successful-prefix median is used. QR4 candidate failure is not automatically whole-procedure failure when WP3's selector still permits a complete choice; changing this policy would change the specified comparator.

## 8. Randomness, pilot and compute ceiling

Use PCG64/SeedSequence entropy2026102408 with namespace9. Diagnostics use spawn_key(9,0,source_index), vectorized independent paths and standardized t draws. Pilot and formal pairs use spawn_key(9,tag,source_index,rep), tag1/2. Draw open uniforms as integer1..2^53−1 divided by2^53 for t inverse CDF. W/method/arm share the same generated source/rep paths, with separate deterministic pilot/formal phase grids. Save seed identity and initial/final RNG states; no post-result seed changes.

The global numerical study clock starts at the first real diagnostic/fit and permits5400seconds through diagnostic calibration, pilot and formal forecasting. Formal synthetic forecasting also cannot exceed5400seconds; its effective allowance is the smaller remaining global time. Four owned worker processes, one numerical thread each; worker internal540s/hard600s and public RSS cap2GiB. Do not change numerical solver acceptance to meet time.

The2-repetition pilot covers every planned source/arm/W/method with its distinct stream, including failures; cap pilot at1200s or remaining global time. It is timing evidence, not included in formal medians and not used to change menus or interpretation. It does not retry formal reps. For each ladder configuration, estimate applicable pilot-unit cost by summing its generation, F and retained conditional-method elapsed costs. Count failed/stopped tasks at their elapsed or hard600s ceiling. The frozen projection is `1.35*(R/2)*max(sum(applicable_unit_seconds)/4,max(applicable_unit_seconds))+180`, with the four-worker divisor, longest-unit bound and180s reserve explicit. In this fixed order choose the largest predicted fit within remaining global time: R32 both QR; R16 both QR; R16 QR33 only (F always). If pilot is incomplete, use the final R16/QR33-only setting and charge each missing task the hard ceiling. If even that projection exceeds remaining time, retain the final setting but stop at the fixed global deadline and report unfinished cells, not a partial favorable conclusion. No configuration or repeat count is changed after formal launch. Seal chosen settings and tested code in a separate run-plan commit before formal launch.

## 9. Estimands and prewritten N1–N4

Per source/rep/arm/W/method compute `d=100*(mean_pinball_QR/mean_pinball_F−1)` on the full same72 evaluation origins. F loss must be positive. For a complete source/arm/W/method cell, report median/IQR over all registered reps, strict win fraction and each method's breach rate. Across sources, take the equal-weight median of all13 source medians. This is descriptive, without treating related real series or reps as independent observations. WP3's ratio-of-mean-losses and its MCSE remain separately labeled.

- N1: at least7 of13 weekly qualified raw diagnostics reject at5%, using the lower/upper unknown-count policy above. Report Holm13 separately.
- N2: switching QR33's across-source median is strictly>+5% at both W52 andW260. Every13-source QR33/F cell required for those statements must be complete; otherwise N2 is unassessable.
- N3: constant QR33's across-source median atW52 is within[-3%,+3%], inclusive. Any required cell failure makes N3 unassessable.
- N4: daily qualified raw rejection and higher descriptive breaks per100observations than matched-calendar hourly, with both rows qualified/valid; interpretation as specified in Section4.

QR4 failure alone does not make a complete QR33 primary prediction unassessable. All QR4 failures still appear in the full grid. No across-series pooled significance test, alternative threshold or conditional-on-completion aggregate is substituted for a failed primary statement.

## 10. Reporting and interpretation branches

Archive every diagnostic row, qualification/fitting failure, partition, constrained calibration, pilot task, formal cell/repetition/candidate and transition exposure under `results/v9/nonstationarity/`. Keep raw financial inputs, per-issue private vectors and full real/daily arrays outside Git. Synthetic task outputs and scalar scores may be public. The main figure has W on x, QR33 relative-loss medians on y, switching and constant curves, with missing required aggregates visibly unavailable; all source rows remain in the supplement.

If N1/N2/N3 are supported, the maximum claim is that parameter switching accounts for losses **in this registered calibrated stress simulation**, with the artificial scheduling and model qualifications named. If N1 is supported but N2 is not, state that low-frequency instability signals did not reproduce the losses in the registered simulation. If N1 is unsupported or unassessable, remove the instability explanation from the main thesis. Distinguish the two earlier v8 stationary grids from the newly fitted C2 constant controls: if N3 fails because the latter themselves produce large losses, report that contrary evidence and do not claim that every stationary process excludes such losses. The earlier grids alone cannot establish a universal sample-size explanation or its universal negation. If N1/N2 are supported but N3 is not or any needed predicate is unassessable, do not use the full explanatory claim; report each outcome separately. N4 never supplies an independent causal frequency conclusion.

No real-data forecast outcomes are recomputed. All older unfavorable results remain, including the daily exception, overlapping backcast, WP3 candidate failure and seven original hourly whole-cell failures. The final manuscript's new numbers must bind to this v9 archive.

## Machine-readable frozen settings

The JSON below and the preceding policies form one design file. Source hashes bind reused code/input metadata; new implementation hashes and the timing-only selected configuration are sealed before the formal launch. This file itself must be the sole file in its preregistration commit.

```json
{
  "schema": "v9-nonstationarity-design-v1",
  "base_pr5_commit": "0f1f066843e0c49cf3e24bce7d72032dc189603d",
  "created_utc": "2026-10-24T18:33:36.911319+00:00",
  "input_metadata": "notes/v9/input-boundaries.json",
  "input_metadata_sha256": "bdb43380b6efa22a2a5293ed3c0105b257efb4522fcb94938eb82ea50fbc5f46",
  "forecast_source_sha256": {
    "v8_mechanism_mc.py": "71134570e1b4d63f98dcd2bb4eb7c1bc596a516b3ca8243b77ad913670a7d7c4",
    "run_v8_wp3.py": "1b5489fc9875137fc1217f2bfe412046f1a353287d234a201f9ac29da3e7352f",
    "v8_daily_fx.py": "cb9e86602ed01a6aefc37772df1245c7e060d5d719a803239deee08b79010b36",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "conditional_study.py": "aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf",
    "conditional_sources.py": "a56cb374cff93b5d18889d2b69a993ad1a3b871ee20bb8349fad04b2fc839709",
    "round2_panel_sources.py": "e0b553d370a23f9dcc38caeb649e048bb880c6fcc9b93536d2e9a30402c4c17d"
  },
  "weekly_raw_stop_exclusive": 405,
  "daily_raw_stop_exclusive": 405,
  "hourly_raw_stop_exclusive": 8109,
  "hourly_original_evaluation_start": 11927,
  "fx_common_calendar_start": "2014-02-05T00:00:00",
  "fx_common_calendar_stop_exclusive": "2015-05-24T00:00:00",
  "diagnostic": "Hansen1992_OLS_joint_score",
  "bootstrap_repetitions": 999,
  "alpha": 0.05,
  "weekly_family_size": 13,
  "max_breaks": 2,
  "minimum_segment_transitions": 104,
  "minimum_segment_fraction": 0.2,
  "bic_parameter_count_formula": "3+4*k",
  "bic_tie_tolerance": 1e-10,
  "phi_bound": 0.999,
  "garch_persistence_bound": 0.999,
  "garch_maxiter": 2000,
  "garch_ftol": 1e-09,
  "student_df_min": 2.05,
  "student_df_max": 500.0,
  "fourth_moment_margin": 1e-08,
  "score_correlation_condition_max": 1000000000000.0,
  "master_entropy": 2026102408,
  "rng_namespace": 9,
  "diagnostic_stream_tag": 0,
  "pilot_stream_tag": 1,
  "formal_stream_tag": 2,
  "burn_in": 20000,
  "retained_observations": 3264,
  "initial_level": 0.0,
  "initial_variance": 1.0,
  "validation_first": 3072,
  "validation_last": 3143,
  "evaluation_first": 3168,
  "evaluation_last": 3239,
  "horizon": 6,
  "windows": [
    52,
    260
  ],
  "tau_numerator": 19,
  "tau_denominator": 20,
  "refit_step": 24,
  "feature_rms_short": 24,
  "feature_rms_long": 168,
  "feature_valid_from": 168,
  "nominal_gap_seconds": 3600,
  "menus": {
    "QR33": [
      0.001,
      0.01,
      0.1
    ],
    "QR4": [
      0.001,
      0.01,
      0.1,
      1.0,
      10.0
    ]
  },
  "methods": [
    "F",
    "QR33",
    "QR4"
  ],
  "pilot_repetitions": 2,
  "repetition_ladder": [
    32,
    16,
    16
  ],
  "conditional_method_ladder": [
    [
      "QR33",
      "QR4"
    ],
    [
      "QR33",
      "QR4"
    ],
    [
      "QR33"
    ]
  ],
  "worker_count": 4,
  "worker_internal_seconds": 540,
  "worker_hard_seconds": 600,
  "worker_rss_public_cap_bytes": 2147483648,
  "global_study_seconds": 5400,
  "pilot_max_seconds": 1200,
  "projection_safety_factor": 1.35,
  "projection_reserve_seconds": 180,
  "N1_min_rejections": 7,
  "N2_median_percent_strict_min": 5.0,
  "N3_median_percent_inclusive_bounds": [
    -3.0,
    3.0
  ],
  "phase_rule": "floor(rep * (raw_n-1) / formal_R); pilot uses its own R=2 and distinct seed tag",
  "summary_estimand": "median over repetitions within each source, then equal-weight median of all13 source medians",
  "nonregular_null_policy": "No qualified primary p; retain unknown status and all descriptive partitions/calibrations",
  "segmentation_policy": "Descriptive Gaussian AR1 separate-variance quasi-likelihood DP/BIC over k0,1,2 for every valid source; no per-break significance claims",
  "failure_policy": "No retry; any required rep/report failure makes that source/arm/W/conditional-method cell FAILED, with no partial median; all inventory rows retained",
  "projection_formula": "1.35*(R/2)*max(sum(applicable_pilot_unit_seconds)/4,max(applicable_pilot_unit_seconds))+180"
}
```
