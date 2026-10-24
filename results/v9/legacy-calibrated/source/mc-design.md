# Frozen v8 calibrated Monte Carlo design

Status: PRESPECIFIED. This file is committed alone before calibration, simulation, pilot or Monte Carlo evaluation. Authority: the user-supplied B1 task. The approved real-data archives are read-only. The simulation investigates a mechanism under three specified DGPs; it neither validates the DGPs as true nor creates an independent real-data test.

## 1. Estimation inputs and mature components

Only the original pre-validation prefix estimates parameters. Load each pinned local snapshot with `conditional_sources.load_source`, verify its size/hash, and slice before any estimation:

|Source|Allowed zero-based rows|Last allowed date|Original validation starts|SHA256|
|---|---|---|---|---|
|FX hourly|0:10463 (10463 observations)|2015-10-07 23:00|2015-10-08 00:00|b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa|
|Treasury PDPOSGS-B weekly|0:329 (329 observations)|2019-07-17|2019-07-24|9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb|

Estimate an intercept AR(1) by least squares, constrained a priori to phi in [-0.995,0.995]; if the unconstrained coefficient exceeds the interval, use its nearest endpoint and re-estimate the intercept as mean(y-phi*x). Record both estimates and whether the constraint binds. This is a fixed stationarity restriction, not an outcome-dependent fit change. Residual variance uses mean squared residuals. Work in standardized source units for numerical conditioning; archive the scale and all transformations.

Use `arch` (via uv, never system installation) for zero-mean GARCH(1,1) with Student-t innovations on the AR residuals. Use package defaults, one fit, no restarts, no alternate distribution. Record convergence flag, parameters and package version. Nonconvergence, nonfinite parameters, nonpositive omega, negative alpha/beta, alpha+beta >=1, or nu<=2 means DGP calibration FAILED. There is no repair after seeing outcomes.

The arch documentation specifies standardized Student-t innovations (unit variance); NumPy draws are therefore t_nu*sqrt((nu-2)/nu). References checked before execution: [arch introduction](https://arch.readthedocs.io/en/latest/univariate/introduction.html), [StudentsT](https://arch.readthedocs.io/en/latest/univariate/generated/arch.univariate.StudentsT.html), [forecasting](https://arch.readthedocs.io/en/latest/univariate/forecasting.html). QR, response scaling, feature transforms, pinball score and frozen historical ranks are the existing implementations, without solver changes.

## 2. DGPs

Let N_t=c+phi*N_(t-1)+s_t*u_t, u_t=sqrt(v_t)*z_t, and v_t=omega+alpha*u_(t-1)^2+beta*v_(t-1).

- D0: Treasury-prefix AR(1), constant residual variance, Gaussian z, s=1. This is a constant-variance control. AR(1) levels can still contain conditional peak information: the label 'no signal' is not imposed as a mathematical fact.
- D1: FX-prefix AR(1), Student-t GARCH(1,1), known deterministic hour shape. Estimate hour-specific RMS of AR residuals, then normalize the shape so its observation-weighted mean square equals one. Fit GARCH to residual/shape. A missing hour or nonpositive hour RMS fails calibration. The fitted latent residual is multiplied by the hour shape in simulation.
- D2: Treasury-prefix AR(1), Student-t GARCH(1,1), s=1, no calendar effect in the DGP.

Initialize N at c/(1-phi), v at omega/(1-alpha-beta) (constant variance for D0), and u=0. Burn in max(10000,ceil(10/(1-abs(phi))),ceil(10/(1-alpha-beta))) steps, omitting the GARCH term for D0. A required burn-in above 1000000 fails calibration. No estimated parameter is altered to make a prediction succeed.

The hourly synthetic clock starts Monday 2000-01-03 00:00, has 120 hourly records then a 48-hour weekend gap; integer index i maps to anchor+i hours+48*floor(i/120) hours, also during burn-in. Weekly clocks start Wednesday 2000-01-05 and advance seven days. Clock is deterministic and known to the oracle. This trading-clock idealization does not reproduce every observed holiday.

## 3. Main grid and comparable origins

Main grid: D0,D1,D2 x W={52,260,720,2880} x p={4,33}:24 cells. H=6 and tau=0.95. p counts exclude the intercept. Four features are the existing magnitude, signed level, short RMS, long RMS;33 features are exactly the existing level-lag, magnitude, RMS, calendar and gap construction. Keep constant weekly calendar features in p=33; do not remove them.

Frequency settings: D0/D2 weekly (short6,long26,nominal gap604800sec,validation V52,refit d13);D1 hourly (short24,long168,gap3600sec,V1440,d24). All eight cells within one DGP/repetition use the same simulated path and validation/evaluation origins. With feature valid_from L (26 weekly,168 hourly), validation first a=L+2880+H-1, validation origins a,...,a+V-1; evaluation first b=a+V+H; evaluation origins b,...,b+M-1. Generate through b+M-1+H. Every validation label ends before evaluation starts; each fit uses exactly W labels with origins r-H-W+1,...,r-H. Future labels can be stored but never enter fitting before completion.

Default R100 independent repetitions, M500 evaluation origins each. Common random numbers across W and p improve within-DGP comparisons. Four worker processes; numerical library threads fixed at one. Secondary grids (H24, double validation, old menu) are optional and excluded from this core plan because the full main grid and oracle take priority.

## 4. Forecasts, selection, failures and oracle

- F: corrected empirical headroom rank ceil(19*(W+1)/20), frozen on the frequency-specific refit schedule and reanchored at each current absolute position.
- I: ordinary empirical rank ceil(19*W/20), same pool and schedule. It is the limiting intercept-only QR candidate.
- QR: lambda in {0.001,0.01,0.1,1,10,infinity}. Score every finite candidate and I on all V validation points. Choose minimum mean projected peak pinball, exact ties going to the largest lambda (infinity strongest). Freeze lambda for the evaluation segment; estimates continue to refit using completed observations. Reuse `conditional_study.conditional_forecast` for33 features and `parsimonious_v3.forecast` for4, and `empirical_headroom.predict` for F/I. The infinity candidate bypasses the finite-lambda solver. Do not reuse the older cell wrapper's incomplete-menu behavior.
- Oracle: at every evaluation origin, simulate2000 independent future paths of length H from the *known current* N_t, latent v_t,u_t and known future calendar. First update v_(t+1)=omega+alpha*u_t^2+beta*v_t, then generate the next innovation. Report the inverted-empirical-CDF0.95 quantile of max(|N_t|,...,|N_(t+H)|). It includes the current floor and differs from an endpoint quantile. Share the same oracle reports across the eight W/p cells of a DGP/repetition. Batch vectorization may change only memory use, not scientific settings. A2000-path estimate approximates the population conditional quantile; finite-sample oracle loss need not beat F in every repetition.

Numerical policy: no retry, alternate lambda, weakened solver tolerances, dropped origin, or replacement draw. Any required candidate/refit/oracle failure in any required repetition makes the *entire factorial cell* FAILED. Retain failed details and completed partial repetitions as diagnostic records, but no complete-cell median, IQR or win rate. Other factorial cells continue. Mark later work for a terminal failed cell NOT_RUN_CELL_FAILED. DGP calibration failure makes all its cells FAILED. Global deadline makes incomplete cells INCOMPLETE_DEADLINE. All24 rows appear in summary.

## 5. Seeds and execution freeze

Base entropy20261024, NumPy SeedSequence keys: phase1=pilot,2=formal,9=unit fixtures; DGP codes0,1,2; repetition zero-based;stream0=simulated path,stream1=oracle. Construct SeedSequence([20261024,phase,dgp,rep,stream]); never seed from worker order or a Python hash. Pilot paths and oracle draws are excluded from formal summaries.

Pilot: two repetitions of the full24-cell main grid with M500 and2000 oracle paths, same algorithms. Pilot may stop cells at their first numerical failure, which is recorded. Its sole design role is timing. Estimate each DGP/rep work time by the larger of its two observed total worker times (simulation+oracle+eight-cell work). Missing pilot work is conservatively imputed using the largest completed same-frequency cell time or, absent that, the largest cell time overall. The projection for R,M is 1.25*(sum of projected per-repetition work across DGPs * R /4 + largest projected per-DGP/rep work). For M300, scale only the evaluation/oracle component by300/500; leave calibration/validation costs fixed. If timing components are unavailable, conservatively do not scale work at all.

Select the first option whose projection is <=5400sec: (R100,M500), then(R50,M500), then(R50,M300). Optional secondary grids have already been omitted before the final M reduction. If none fits, select(R50,M300), retain the5400sec hard stop, and report the resulting incomplete cells. Commit/archive an immutable run-plan with pilot receipts, selected R/M and projection before formal execution. Do not change the rule based on pilot loss values.

Formal wall clock is one continuous maximum5400sec from start, including output checkpoints. Each worker checks the shared deadline during fits and between origins; the parent cancels unfinished tasks at the deadline. Schedule independent DGP/repetition tasks interleaved by repetition, with cells in W ascending then p4,p33. A failed cell remains failed; no later task can restore it. A runtime interruption is reported rather than rerun. No change after formal start.

## 6. Reports and prespecified predictions

For every complete cell report across R repetitions: QR vs F mean-pinball percent change100*(L_QR/L_F-1), median and25/75percentiles; frequency QR<F; median breach rate for F,I,QR,oracle; oracle vs F median percent change; selected-infinity frequency. Report I vs F additionally as a rank diagnostic. Zero F loss makes the relative metric unavailable and the cell fails relative-score reporting; retain raw losses. No pooled independence claim across cells or repetition-level significance fishing.

- P1: all eight D0 cells have median QR/F change >=-2% (gain at most2%).
- P2: both p4 and p33 D1,W2880 cells have median change <-5%.
- P3: D2,W52,p33 median change >+5%.
- P4: for each p in both D1 and D2, median changes are nonincreasing through W52,260,720,2880. Exact equality qualifies. All four sequences must satisfy the condition.

Missing/failed cells make the affected prediction UNASSESSABLE, not a partial pass. Report support/failure honestly. Plot W against median change with IQR, three DGP panels,4/33 feature lines and oracle dashed. Oracle is feature-invariant; display one dashed W curve. Write outputs only to results/v8/mc and notes/v8; preserve all old archives.

## 7. Tests before pilot

Write failing tests first. Verify fixed-seed reproducibility, standardized t variance, stationary AR and GARCH moments using fixed synthetic fixtures, and recovery of a specified diurnal RMS pattern. Verify oracle's use of current latent state, floor inclusion, and invariance to changes in the realized future. Verify infinity selection/tie rule, complete-menu eligibility and whole-cell failure aggregation. Verify exact origin geometry.

For the requested D0 oracle/F agreement test, use a separate zero-drift Gaussian random-walk fixture at a large positive level with a long historical window; its headroom law is nearly state invariant. Compare the oracle headroom to corrected empirical F within a fixed12% tolerance. This fixture is explicitly nonstationary and is not the calibrated D0; a stationary AR(1) is not asserted to have no conditional information. No fixture threshold is adjusted after a failed test without a documented implementation diagnosis.

## 8. Scope and pending author decisions

The main grid does not separately identify frequency and validation-length effects because both are tied to DGP. The fitted parameter uncertainty, structural breaks, alternative innovation families and other dealers are outside scope. Simulation supports only these DGP settings. Whether to obtain additional independent data or extend the factorial design is an author decision; no extra real-data experiment is authorized here.
