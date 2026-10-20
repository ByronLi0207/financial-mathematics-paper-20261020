# Source register23 — density diagnostics and parametric quantile estimation risk

**Selected primary-source reading, 20 October 2026.** This register consolidates completed selected primary-source reading. It reports no project empirical result or selected research design. Administrative curation adds no original-body reading credit.

## 1. Normal-transform diagnostics for issued density forecasts

**Jeremy Berkowitz (2001), “Testing Density Forecasts, With Applications to Risk Management.” Journal of Business & Economic Statistics19(4),465–474, October2001.** [Formal DOI](https://doi.org/10.1198/07350010152596718).

Actual primary edition: [university-hosted author manuscript](https://mx.nthu.edu.tw/~jtyang/Teaching/Risk_management/Papers/Testing/Testing%20Density%20Forecasts%2C%20with%20Applications%20to%20Risk%20Management.pdf), dated **27 December 2000**,36 physical pages. The formal2001 body was not read or version-compared. No separate first-online date is asserted.

**Source synthesis — 145 words.**

<!-- SYNTHESIS_1_START -->
Berkowitz evaluates issued forecast distributions by mapping PITs into normal scores. An iid uniform PIT premise gives iid standard normal transformed values; that implication does not make finite diagnostics a certificate of complete conditional correctness. A Gaussian autoregressive likelihood targets location, scale and specified persistence, with acknowledged limitations concerning other departures. A censored likelihood addresses the retained tail distribution, requiring more information than a scalar shortfall report. Forecasts are primitives; discussion of parameter uncertainty supplies no universal fixed, rolling or recursive estimation adjustment. The financial demonstration simulates option profit and loss under Black–Scholes and stochastic volatility. Numerical density approximation affects reported rejection behavior, and size-adjusted power comparisons are simulation evidence rather than exact finite-sample control. Selected December 2000 author-manuscript methods and application were read; the final journal edition, outside regularity arguments, executable implementation and current material permissions remain unverified. No observed market dataset was reproduced.
<!-- SYNTHESIS_1_END -->

## 2. Conditional-density correctness and practical PIT evaluation

**Francis X. Diebold, Todd A. Gunther and Anthony S. Tay (1998), “Evaluating Density Forecasts with Applications to Financial Risk Management.” International Economic Review39(4),863–883, November1998.** [Formal DOI](https://doi.org/10.2307/2527342); [NYU institutional record](https://archive.nyu.edu/handle/2451/14779).

Actual primary edition: [NYU archive file](https://archive.nyu.edu/bitstream/2451/14779/1/SOR-98-6.pdf), a formal journal scan with one archive transmission cover and21 article pages,22 physical pages total. Its catalogue/file label SOR-98-6 does not turn this actual scan into a separate working-paper edition. Scanning timestamps are not scholarly revision dates.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_2_START -->
Diebold, Gunther and Tay derive iid uniform PITs from correct one-step conditional densities under regular invertible transformations. The triangular-Jacobian proof is a forward implication; finite histograms and selected autocorrelations do not certify its premise against every conditioning variable. Their decision discussion separates the value of correct densities from rankings of two misspecified forecasts, which can depend on the user's loss. Forecasts are evaluated as primitives, leaving general parameter-estimation adjustments outside the main method. Existing extensions discuss recalibration, multivariate conditional transforms, overlapping horizons and recursive monitoring, without a specific anytime alarm guarantee. The financial exercise separates earlier estimation from later S&P500 evaluation. Recalibration itself carries an explicit finite-sample improvement caveat. Selected formal-scan proof, diagnostic, application and extension passages were read. Full figures, outside estimator theory, source observations and present data/code permissions remain unverified. Simulation performance and individual graphical intervals are not exact simultaneous finite-sample inference.
<!-- SYNTHESIS_2_END -->

## 3. Parametric VaR backtests with estimation effects

**J. Carlos Escanciano and Jose Olmo (2010), “Backtesting Parametric Value-at-Risk With Estimation Risk.” Journal of Business & Economic Statistics28(1),36–51, January2010.** [Formal DOI](https://doi.org/10.1198/jbes.2009.07063).

Actual primary edition: [Indiana University CAEPR deposit](https://hdl.handle.net/2022/3190), with an explicitly linked [institutional manuscript](https://scholarworks.iu.edu/iuswrrest/api/core/bitstreams/dd4a4258-a913-42c2-8ce9-75d51bba2800/content). Cover: **CAEPR2007-005_updated**, original **19 March 2007**, updated **4 September 2008**. Body title: **draft21 February 2008**. These distinct labels are preserved; the cover update does not certify revision of every body passage. The retained39-page file is not the final2010 typesetting, which was not obtained on the stopped publisher route.

**Source synthesis — 143 words.**

<!-- SYNTHESIS_3_START -->
Escanciano and Olmo separate ideal hit variation, parameter estimation and model misspecification in plug-in conditional-quantile backtests. The main corrected inference imposes true-parameter quantile correctness, not ideal finite-history issued forecasts. Fixed, rolling and recursive schemes have different asymptotic variance corrections as training and evaluation lengths grow with a finite ratio. Fixed means frozen parameter updates, not bounded asymptotic training length. Stationarity, smooth densities and quantile derivatives, and martingale influence expansions remain substantive premises. Covariance terms mean estimation effects need not always inflate variance. Fixed-lag dependence diagnostics require additional expansions; selected hit moments do not establish full-information conditional correctness. The S&P500 illustration compares corrected and uncorrected decisions, while acknowledging weak rare-tail approximations. Selected institutional working-paper methods and supplied proof routes were read; deferred external arguments, final-edition identity, executable materials and current reuse permissions remain unverified. Bootstrap mentions do not supply a general validated resampling procedure.
<!-- SYNTHESIS_3_END -->

## Actual editions and recorded root scope

These ranges concern selected passages, not every line, figure or numerical cell on each page. Auxiliary records do not enlarge root scope or hours.

| Source | Retained edition and page mapping | Root selected reading | Remaining boundary |
|---|---|---|---|
| Berkowitz |36-page author manuscript dated27December2000; physical numbering used; main1–26, references27–28, tables29–30, figure material31–36 |Main prose1–26 and selected displays; references27–28 screened; table/figure-caption context29–36; visual checks10–12,15,17,21,29 |Full numerical tables and plotted curves not audited; final journal body and external LR/pricing/estimation proofs unreviewed |
| Diebold–Gunther–Tay |22-page formal journal scan; PDF1 is the archive cover; printed page = PDF page + 861 forPDF2–22 |Primary prosePDF2–9,12,18–20; references21–22 screened; captions10–11,13–17 extracted; visual checks4–7,12,18–20 |Plots not visually audited or reproduced; outside GARCH, estimation-risk and monitoring implementations unreviewed |
| Escanciano–Olmo |39-page IU working-paper deposit; institutional cover1, numbered manuscript1–38; printed page = PDF page − 1 |PDF1–19,23–32, including supplied AppendixA proof routes; visual checks8–10,13,24–25,28,30 |Simulation tables/figures20–22,33–39 not comprehensively audited; deferred empirical-process/variance/ULLN arguments and final journal body unreviewed |

The Escanciano–Olmo cover, body and repository labels identify the actual accessed edition; none is silently substituted for the formal publication. Original-file identity does not establish equation-level equivalence with another edition.

## Original crosswalk of targets and guarantees

| Distinction | Boundary retained |
|---|---|
| Issued forecast versus estimated parametric null | Treating forecasts as primitive objects differs from testing existence of a true model parameter while accounting for its estimation. A diagnostic model fitted to PITs does not automatically adjust uncertainty in the upstream forecast model. |
| Density correctness versus quantile correctness | A full predictive density and a conditional quantile family impose different population restrictions; neither is identified by every finite practical diagnostic battery. |
| Transformation law versus test calibration | An exact PIT transformation under ideal forecasts does not make a chosen likelihood or portmanteau statistic exactly calibrated at finite sample size. |
| Selected history versus full conditioning | Hit/PIT history and a finite collection of lagged instruments do not automatically include every forecast-time predictor. |
| Fixed forecast scheme versus fixed window size | Freezing parameter updates differs from holding training length bounded while evaluation grows. The asymptotic regime remains part of the theorem. |
| Simulation versus statistical guarantee | Reported size, adjusted power and numerical approximation exercises are source evidence under specified scenarios, not universal finite-sample or arbitrary-stopping guarantees. |
| Graphical diagnostics versus simultaneous inference | Separate bins, lags, moments and monitoring dates need an explicit joint error target; presenting them together does not supply one. |

The applications and extensions are historical source work. This register selects no new method, financial series, experiment or empirical comparison.

## Financial materials, access and permissions

Berkowitz's option-risk examples are simulated. No program, financial observations or current redistribution licence was verified. The public university copy is evidence of reading access, not an open reuse declaration.

Diebold–Gunther–Tay's empirical series is dividend-inclusive daily S&P500 returns over1962–1995 with distinct estimation/evaluation periods. The original provider, fixed vintage and raw reuse rights were not established. The NYU scan's article/transmission notices do not license its underlying financial observations.

Escanciano–Olmo attributes its S&P500 log returns to Freelunch.com, February2000–February2006, and illustrates five chronological fixed-estimate exercises. Present source access, exact vintage, executable replication and data/code permissions remain unverified. The manuscript cover reserves copyright; no open article licence is inferred.

No original article, raw observations, source program or substantial third-party passage is delivered. Current data/code access is not inferred from a source's historical citation or implementation mention. Existing protected routes were not retried during curation.

## De-duplication and retained fingerprints

Registers01–22 were checked by author combinations, titles and identifiers. None of these three sources had an earlier principal entry; incidental density-evaluation references are not counted as such. Abstract-only access records outside this assigned group are not used to add entries or reading depth.

The three existing source files were rehashed during preparation and matched the recorded byte counts and SHA-256. No original body was reopened or newly read. Fingerprints identify retained editions, not unread proof correctness or final-version equivalence.

| Retained evidence | Bytes | SHA-256 |
|---|---:|---|
| Berkowitz, author27December2000 |134806|`821204f733e4fc5659299447f37a2bf86220833a1a88c96e79d23a961a75f8d1`|
| Diebold–Gunther–Tay, formal1998 NYU scan |517244|`331eab590c36981a7ea42d10a43ac56707ac1522a3fb37dc0fa959ac5414aab4`|
| Escanciano–Olmo, IU updated working-paper deposit |478785|`dd7d1c11e9a1801945799b90c2dae4a47e8ca6ffb145636f2e979a97ac79c939`|
