# Pre-launch implementation review

This is a same-model, read-only implementation review, not the disabled
Claude/cross-model review. No financial raw file was opened, and no study
calculation was run during it.

## Statistical and generation primitives

Reviewed the committed protocol SHA256
`76df3a3d2c2c5b90d4c3f4b225cc4f879b384c6f3d288b6732f488bda15a3894`,
`v9_nonstationarity.py` at SHA256
`ae73f11b508c47b9a213c524ffe9596a7ccc06c882c092427864674d84e72ddb`,
and `v9_switching.py` at SHA256
`70309cfe6a055af8503fcb81e07d8a0240d115211f185740a68a1eec3d196731`.
No hard scientific deviation was found in this scope. Checked:

- finite-fourth-moment gate and unavailable qualified p for nonregular fits;
- one fitted null, new OLS on every simulated path, no dropped bootstrap draw;
- exact integer BIC partition cost/penalty, complete-partition ties and cuts;
- shared whole-prefix SD, preserved level mean, prior observed segment lag;
- constrained AR profile and optimization-time GARCH restriction, one fit;
- preserved level/variance/innovation at regime changes, common uniforms,
  correct t standardization, and identical zero-break paths.

## Driver review and corrections

The first driver review found that a segmented-calibration failure would
cancel a valid constant arm, and that a later interruption could discard
completed earlier comparisons and generation identity. Both are failures
of implementation, not reasons to change the registered scientific policy.
They are repaired and tested before launch. The observed RED/GREEN record
is in `driver-test-log.md`; no real result was inspected to choose a repair.

Additional preflight checks retain source identifiers after worker failure,
record dates for both FX clocks, describe boundary exposure without filtering
repetitions, and enforce the separately committed timing-only run plan.
