# v8 mechanism interpretation before formal results

Prepared while the formal run is still in progress, using only `protocol/v8/mc-design.md` and the archived `results/v8/mc/calibration.json`. No formal outcome, pilot loss, fresh fit or additional simulation was consulted. Numerical quantities below are algebraic functions of the archived parameters. This note guides B1 analysis; it does not supply manuscript conclusions or alter the frozen design.

## What the comparisons can establish

Within a DGP and repetition, all W/p cells use the same generated path, validation dates, evaluation dates and oracle reports. Changing W therefore compares the sensitivity of the declared procedures to available completed history under one fixed mechanism. The AR/GARCH parameters, frequency, validation length, refit interval, horizon, features and penalty menu remain fixed. However, both the conditional estimator and historical F change their training pools when W changes; F's order-statistic correction also changes. A QR/F curve is consequently a comparison of complete procedures as history changes, rather than an isolated causal effect of estimation sample size on QR alone. Native or standardized mean losses, already required by the run, can help distinguish movement in QR from movement in its F denominator.

Comparing p4 with p33 at the same DGP/W holds the path, origin geometry, penalty menu and validation length fixed. The four predictors are magnitude, signed current level and two past RMS measures. The larger feature set adds lagged levels and calendar/gap terms. This identifies how these two feature-and-selection procedures perform under the specified DGP. It does not establish that each extra predictor contains signal, nor does it estimate a universal causal value of increasing dimension: lambda is selected separately for each feature set. In weekly cells the five calendar/gap columns remain constant and standardize to zero, so the declared count of 33 is not 33 independently varying predictors.

The infinity candidate is I, the ordinary empirical headroom quantile. Report its selection frequency alongside QR/F results. A gain when infinity is selected can arise from the F-versus-I rank difference and is not evidence that fitted slopes extracted conditional information. Conversely, selection of a finite lambda is not by itself proof that its slopes generalize. The required I/F diagnostic and oracle/F comparison distinguish these possibilities descriptively.

## D0 is a constant-variance control, not a no-information null

D0 has c=0.5896851, phi=0.6655338 and Gaussian innovation SD=0.7391361 in standardized source units. Its stationary mean is c/(1-phi)=1.7630635. Constant innovation variance does not make the future peak or headroom state invariant:

`E[N_(t+h) | N_t=x] = c/(1-phi) + phi^h * (x-c/(1-phi))`.

Mean reversion changes the chance of exceeding the current absolute floor. The absolute-value peak and subtraction of the current floor make headroom particularly state dependent. Thus P1 is a falsifiable prediction about this calibrated control; it is not guaranteed by the D0 definition. A rejection would not prove a programming error or justify changing D0 parameters.

The separate high-positive-level Gaussian random-walk oracle/F fixture has phi=1 and zero drift. Away from zero, its maximum future increment is nearly independent of the anchor. That explicitly nonstationary unit fixture checks oracle/target agreement; it does not validate a no-signal interpretation of calibrated D0.

## Frequency and validation length remain bundled

D1 combines FX-calibrated coefficients, a trading-hour clock, Student-t GARCH, a diurnal shape, V=1440 and refit interval 24. D0/D2 use Treasury calibration, weekly clocks, V=52 and interval 13; D0 also changes the innovation/volatility law. Cross-DGP differences therefore cannot be attributed separately to frequency, validation length, calendar information, persistence or volatility signal. H=6 also means six recorded hours in D1 and six weeks in D0/D2. The excluded secondary grids are not an executed frequency/validation factorial experiment. Any claim about these separate causes requires new controlled cells outside this run.

D0 and D2 share the Treasury AR calibration, clock, V and refit interval. Their contrast is more targeted, but still changes both Gaussian versus Student-t innovations and constant versus GARCH variance; it does not identify either change alone.

## How to interpret the oracle

The oracle uses known calibrated parameters, the current generated N_t/v_t/u_t and the known future calendar. Its target is the .95 quantile of `max(|N_t|,...,|N_(t+6)|)`, including the current floor. It approximates that quantile using 2000 independent future paths per origin; it is not the exact population conditional quantile. A population conditional quantile minimizes expected conditional pinball loss, whereas a finite simulation estimate evaluated on one realized 500-origin path need not beat F in every repetition. An observed positive oracle/F loss change therefore is not intrinsically contradictory.

Share oracle reports across all eight W/p cells, as frozen. The oracle capacity itself does not depend on W or p; its percentage loss change can vary with W because the matched F denominator changes. The dashed curve should not be described as a feature-dependent attainable QR result or a deterministic samplewise upper bound on gains. It benchmarks available conditional information under the assumed DGP, without estimation uncertainty in its calibrated parameters.

## Moment conditions and descriptive uncertainty

Both fitted GARCH laws satisfy alpha+beta<1 and nu>2, so their latent unconditional innovation variances are finite: omega/(1-alpha-beta)=0.1735553 for D1 and 0.5586832 for D2. Their AR coefficients have absolute value below one, and the D1 hour multiplier is bounded. These conditions support finite variance of the level process; they do not establish adequate finite-run precision for every loss statistic.

For standardized Student-t z with nu>4, `kappa=E[z^4]=3*(nu-2)/(nu-4)`. A GARCH(1,1) fourth moment requires `alpha^2*kappa + 2*alpha*beta + beta^2 < 1`:

|DGP|nu|alpha+beta|Fourth-moment coefficient|Implication|
|---|---:|---:|---:|---|
|D1|4.0416713|0.9800000|6.7997537|Latent GARCH fourth moment does not exist, although the standardized t innovation's own fourth moment is finite.|
|D2|14.6408291|0.9779682|0.9603241|The latent GARCH fourth-moment condition holds.|

The frozen medians, IQRs, repetition win frequencies and breach rates are descriptive summaries under these fixed parameter values. IQRs describe repetition dispersion; they are not confidence intervals for the median or intervals for real-data performance. Do not add normal/CLT intervals or finite-fourth-moment claims. The repetitions do not propagate uncertainty in the original-prefix calibration, structural breaks or model misspecification.

## Post-run decision discipline

Use exactly the frozen P1-P4 inequalities and complete-cell rules. Report unsupported predictions without changing thresholds, features, DGPs or menus. A required numerical failure makes its entire factorial cell failed; completed partial repetitions remain diagnostic and cannot supply a complete-cell median. Any affected prediction is UNASSESSABLE. All 24 cells must appear, including failures or deadline-incomplete cells. Simulation evidence concerns these three parameterized mechanisms, not independent confirmation of either financial archive or a universal explanation of why historical rules win.
