# WP3 frozen Monte Carlo mechanism design

Status: **design fixed before any WP3 study simulation or model fit**.
This prospective execution contract belongs to an otherwise post-result,
exploratory manuscript revision. It does not replace either original primary.
The companion JSON is the machine-readable contract. No outcome-dependent
change to this design, repetition count, menu, seed or failure rule is allowed.

## Aim and target

Ask whether the observed difficulty of beating historical headroom can arise
from estimation, persistence and volatility clustering in a controlled process.
Every method predicts the same sampled absolute-position peak, including the
current observation, at target quantile 19/20. Headroom is that peak minus the
current absolute position. Horizons and histories count observations.

## DGP and fixed factorial grid

Retained observations follow `N_t = phi*N_(t-1) + epsilon_t`, with
`epsilon_t = sqrt(v_t)*z_t`, independent standard-normal `z_t`, and
`v_t = omega + a*epsilon_(t-1)^2 + b*v_(t-1)`.

- Position persistence: phi = 0.7, 0.9, 0.98.
- Variance persistence p = a+b = 0, 0.9, 0.98. At p=0 use a=b=0,
  omega=1. At positive p use a=0.05, b=p-0.05 and omega=1-p.
  Thus innovation unconditional variance is one, with p<1 in all cases.
  The machine-readable constants are used directly (omega0.1/0.02 and
  beta0.85/0.93), avoiding a different binary rounding from recomputing the
  decimal differences. Changing p here is a specified GARCH-persistence intervention, not an
  exhaustive comparison of every alpha/beta pair with the same sum.
- Histories W = 52, 260, 720, 2880; horizons H = 6, 24: 72 cells.
- Initialize the pre-burn path at previous level 0, first variance 1; draw
  its first innovation before subsequent GARCH recursion. Discard 20,000
  observations, then retain 3,264. This is a long-burn approximation to
  stationarity, not an exact stationary draw for GARCH-driven levels.
- The retained-index calendar begins at 2000-01-03T00:00, increasing exactly
  one hour per record, identically for every condition and repetition.

The design deliberately contains mean-reverting **levels**, not positively
autocorrelated increments. It does not estimate DGP parameters from the FX or
weekly observations and is not a fitted simulator of either source.

## Methods and fixed information clock

Only three reports are calculated: matched fixed-window historical headroom F,
original 33-predictor QR, and the four-predictor parsimonious QR. No additional
forecast, conditional-quantile oracle, fitted GARCH model or hypothesis test is
introduced.

- At refit r, use precisely the W origins r-H-W+1 through r-H, so every
  training label satisfies i+H<=r. Refit every 24 records, separately anchored
  at the validation/evaluation start. Freeze the pool, transformations,
  response scale and coefficients between refits; query features and floor
  use the actual current issue t. Mature earlier evaluation labels may enter
  later refits, exactly as in the original online procedure.
- F uses the corrected empirical rank ceil(19*(W+1)/20) of mature headroom,
  added to the current floor. Calculate F alone, not unlisted S/K/I reports.
- QR33 retains the original 33 features: signed levels at lags0–24, current
  absolute level, increment RMS over24/168 records, hour and weekday sine/cosine,
  and observed-gap indicator. The gap indicator is identically zero on this
  calendar; calendar features are retained even though the DGP has no calendar
  effect. Feature validity begins at retained index168 for both regressions.
- QR4 selects columns [25,0,26,27]: absolute level, signed level, and the same
  two RMS features. It does not receive an earlier feature-validity privilege.
- Standardize on the mature training pool, population SD, with exact constant
  columns centered at their repeated value and scale1. Normalize the response
  by max(mean training headroom,1e-6*mean absolute training level,1e-12).
  Fit the unchanged ridge quantile objective with an unpenalized intercept;
  project only the final predicted headroom at zero, then add the issue floor.
- Preserve original solver: max_iter10000, atol1e-6, rtol1e-5, gap_rtol1e-6;
  both ADMM residual criteria and the feasible-dual Fenchel gap must pass.
  Nonfinite inputs, coefficients or forecast headroom are failures, never a
  silently substituted floor.

### Original menu and selector differences are preserved

QR33 uses penalties [0.001,0.01,0.1], requires every validation candidate to
complete, and breaks exact validation-loss ties toward the larger penalty.
QR4 uses [0.001,0.01,0.1,1,10], selects among completed candidates, and breaks
exact ties toward the first candidate in that increasing menu. Failed QR4
candidates remain in the inventory. If its selected evaluation procedure
fails, there is no replacement parameter. This reproduces the historical
procedure difference rather than describing the comparison as a pure effect
of predictor count. Methods are matched within each repetition; no original
outcome is imported as a simulated observation.

## Validation, gap and evaluation

All W/H cells share the same retained-index segments:

- Validation origins3072–3143 inclusive: 72 issues, three refit blocks.
- Evaluation origins3168–3239 inclusive: 72 issues, three refit blocks.
- All validation targets, including H24, finish by3167, before evaluation.
- The earliest training origin is169 for W2880/H24, exceeding feature index168.
- Evaluation includes overlapping targets; observations inside a repetition
  are not treated as independent Monte Carlo repetitions. The short segments
  are a budget-limited mechanism probe, not a reconstruction of the original
  long empirical validation/evaluation periods.

## Repetitions, RNG and budget

Use **32 fixed repetitions**. Master entropy is2026102408. Each repetition
uses NumPy PCG64 initialized from `SeedSequence(master,spawn_key=(rep,))`,
rep0–31. Save initial/final generator state and software versions. The same
normal innovation sequence within a repetition is deliberately reused across
phi, variance-persistence, W and H conditions (common random numbers); streams
across repetitions are distinct. No parallel financial workers are used.

Existing FX W2880 runtime receipts provide a planning reference, not a current
measurement: original QR validation/evaluation and QR4 full-cell timings are
listed in `notes/revision-v8/wp3-method-source-audit.md`. The reduced segments
and32 repetitions are chosen before outcomes to target a one-hour execution
budget. This count gives a worst-case binomial win-frequency Monte Carlo SE
of about0.0884, so fine thresholds cannot be resolved. Actual elapsed time,
memory and thread observations must be measured, not inferred from this plan.

Run in repetition-major order, then phi/p in listed order, then W ascending
and H6/H24. One worker may handle one rep/phi/p block (eight W/H cells).
Numerical threads1; observed OS threads<=2; internal RSS stop1.5GiB, public
cap2GiB. Each worker block has internal540s/hard600s limits. The **3,600s total study wall budget** also interrupts any in-flight worker;
pass the remaining global time into its checkpoint/deadline and set the
parent subprocess timeout to the smaller of600s and that remaining time.
No worker is allowed to run past the global deadline. All failures, interrupted units
and unattempted planned cells are explicitly recorded; no retries with changed
scientific or numerical settings. Fixed fixtures/unit tests run separately
and do not contribute simulated study repetitions.

## Performance and Monte Carlo uncertainty

Within each repetition/method/cell, record mean pinball loss, strict breaches
`peak>forecast`, breach frequency, selected penalty, all candidate statuses,
refit maturity extrema and complete/failed status. Preserve all32 planned
repetitions, including reasons for missing reports.

For paired complete repetitions, let A_j/B_j be QR/F mean losses. Report
100*(mean(A)/mean(B)-1). Its delta-method Monte Carlo SE is
100*sd(A-r*B)/(sqrt(R)*mean(B)), r=mean(A)/mean(B), with sample SD(ddof1).
Report mean breach frequency and its between-repetition SD/sqrt(R), and the
strict paired win fraction mean(A<B) with plug-in binomial MC SE and the
worst-case bound0.5/sqrt(R). For a single completion, MC SE is NA; for zero
reference mean loss, relative change/SE is NA. Failures are not assigned an
invented loss and are not removed from planned denominators.

If any repetition is incomplete, the full-procedure performance is NA;
available-pair summaries, if displayed, are explicitly **conditional on
completion**, with counts and reasons beside them. They cannot pass the
support criterion. Heatmaps show incomplete full-procedure cells as NA,
rather than silently coloring their successful subset.

## Predeclared support / non-support rule

For each regression separately, call a cell a *clear descriptive gain* only
when all32 planned repetitions complete, the relative loss change plus twice
its MC SE is below zero, and the strict win fraction is at least0.75.
This is a predeclared descriptive screen, not a multiple-comparison-adjusted
significance test or proof of a universal regime boundary.

The proposed narrow region is H6, W>=720, variance persistence>=0.9
(12 cells). The predicted mechanism is supported for a procedure only if at
least6 of those12 cells pass, every outside cell is fully evaluable, and no
outside cell passes. Any clear gain outside the region contradicts that
restriction and is reported as MISMATCH. Failure to obtain enough target
gains is NOT_SUPPORTED; missing/failed cells that prevent classification are
INCONCLUSIVE. The broad claim that *conditional models* gain only in that
region cannot be supported if either QR procedure supplies a clear outside
counterexample. Report the procedures separately and preserve all adverse or
uncertain evidence. Even a supported finite-grid pattern is not a theorem or
an identified empirical frequency effect.

## Output and placement

Save complete per-unit receipts and all72-cell summaries under
`results/revision-v8/wp3/`; code/tests under `notes/revision-v8/` and the normal
test discovery scope. At most one new main mechanism figure, faceted by H/phi,
with W by variance persistence; companion QR4 and complete means, breach
rates, win rates and MC SEs in Supplement or linked complete results. Main
figures remain<=4. The original scientific archives remain byte-identical.

## Verified primary sources (reading scope)

- Bollerslev (1986), *Generalized autoregressive conditional
  heteroskedasticity*, Journal of Econometrics31(3),307–327,
  DOI10.1016/0304-4076(86)90063-1. Author-hosted original, pp307–311
  (definitions, Theorem1 and GARCH(1,1)); not a whole-paper close reading:
  https://public.econ.duke.edu/~boller/Published_Papers/joe_86.pdf
- Morris, White and Crowther (2019), *Using simulation studies to evaluate
  statistical methods*, Statistics in Medicine38(11),2074–2102,
  DOI10.1002/sim.8086. Original publisher sections3–5 and Table1 consulted
  for design, matched data, failure reporting, stored RNG state and MC SE:
  https://onlinelibrary.wiley.com/doi/full/10.1002/sim.8086
- NumPy's official parallel RNG documentation, SeedSequence spawning section,
  consulted for deterministic child-stream construction; current docs version
  differs from the runtime and the actual runtime version will be recorded:
  https://numpy.org/doc/stable/reference/random/parallel.html
