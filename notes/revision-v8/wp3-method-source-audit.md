# WP3 method and source audit before freezing

No WP3 study simulation, data-dependent tuning or model fitting has occurred.
The method inspection below is a readback of the existing repository.

## Original procedures

`conditional_features.py:35` defines the 33 predictors and validity index;
`:68` defines mature-training mean/population-SD normalization; `:94` supplies
the exact completed-label pool; `:108` supplies the response scale.
`conditional_study.py:71` implements the QR33 fixed-parameter segment and
`:232` the strict full-menu selector. `parsimonious_v3.py:17` selects four
columns [25,0,26,27]; `:28` implements its fixed-parameter segment; `:62–72`
contains its five-penalty eligible-subset selector and first-menu tie rule.

Both procedures use the unchanged `conditional_quantile.py:166` solver, with
the unpenalized intercept, ridge slopes, ADMM residual checks and feasible-dual
Fenchel gap. Its defaults and failure states are preserved. The simulation
issuer must additionally reject nonfinite raw headroom explicitly rather than
let a Python `max` operation turn a nonfinite value into a floor forecast.
This is a validation guard, not a different fitted model.

QR33 uses the original three penalties; QR4 uses five. Their candidate-failure
and exact-tie rules differ. This is already documented by the existing
`protocol/revision-20261023/round2-D3-panel.md`. The simulation preserves those
differences and cannot identify a pure predictor-count effect.

The hourly recipe is short/long RMS24/168, refit24, nominal gap3600 seconds.
The same fixed synthetic calendar starts after burn-in, so calendar phase is
unchanged across conditions and the gap feature is zero. At every refit,
the current outcome may close the last training label, but no unfinished
label is used. The issue floor and query remain current between refits.

The minimum first refit is `m+H+W-1`, `m=max(24,short,long)=168`.
The design's common first origin3072 is valid for W2880/H24; its validation
targets finish before the evaluation start, and the last evaluation target
fits inside the retained input. These are index-boundary checks, not fitted
study results.

## Existing runtime records, not current measurements

Exact original resource objects are saved in
`wp3-original-runtime-fields.json` with their six source paths. QR33 validation
and evaluation are separate receipts; QR4 covers five validation candidates
and the selected evaluation in one receipt. Their elapsed values therefore
are not direct speed comparisons. No fit-count field is fabricated from the
training-count or completed-origin fields. These records informed the bounded
design choice; they do not prove that this new simulation will fit its budget.

## Primary sources actually consulted

- **Bollerslev (1986)**, *Generalized autoregressive conditional
  heteroskedasticity*, Journal of Econometrics31(3),307–327,
  DOI10.1016/0304-4076(86)90063-1. The author-hosted original pp307–311 were
  read, including definitions, Theorem1 and the GARCH(1,1) discussion. This
  verifies the positive variance recursion and finite-variance stationarity
  restriction used here; it supplies no guarantee for fitted peak forecasts.
  [Original author copy](https://public.econ.duke.edu/~boller/Published_Papers/joe_86.pdf).
- **Morris, White and Crowther (2019)**, *Using simulation studies to evaluate
  statistical methods*, Statistics in Medicine38(11),2074–2102,
  DOI10.1002/sim.8086. Publisher sections3–5 and Table1 were read for explicit
  design, shared datasets for comparisons, generator-state records, missing
  estimates and Monte Carlo uncertainty. Failures may depend on simulated
  conditions, so successful-only summaries cannot silently stand for the full
  procedure. [Original publisher text](https://onlinelibrary.wiley.com/doi/full/10.1002/sim.8086).
- **NumPy official RNG documentation**, SeedSequence spawning section,
  [official reference](https://numpy.org/doc/stable/reference/random/parallel.html).
  Deterministic child construction is documented; approximate independence is
  not a mathematical guarantee of nonoverlap. The consulted current manual
  is2.5; the actual runtime version must be recorded separately.

No source was described as fully close-read. No third-party paper PDF is
copied into the repository. New-study code and results must cite these reading
scopes accurately rather than inherit an earlier reading-time total.

## Pre-freeze design challenge

A same-model read-only design check identified one substantive omission:
stopping new workers at3600 seconds alone could allow the final worker to run
another600 seconds. Before freezing, both protocol files were corrected to
interrupt in-flight work at the global deadline and constrain the worker's
timeout/checkpoint to remaining global time. The index boundaries, independent
repetition MC SE unit, paired loss-ratio formula, fixed menus and missing-result
rules were also checked. This is an internal design check, not Claude review
or external validation.
