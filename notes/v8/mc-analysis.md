# B1 calibrated simulation analysis

Design: b7e548df at 2026-10-24T00:37:44-07:00. Run plan: c66fc9d at 00:46:17 PDT. Formal start: 2026-10-24T07:46:22.956722+00:00; numerical elapsed: 1209.614 seconds.

Fixed size: 100 repetitions x 500 evaluation origins. Pilot projection: 4598.7 seconds. Main grid not reduced; optional secondary grids were excluded in the prespecified plan.

All24 cells have terminal status: 17 complete and 7 failed. Independent verification: 51,606 assertions passed.

|DGP|p|W52 median change%|W2880 median change%|
|---|---:|---:|---:|
|D0|4|-0.2|-21.8|
|D0|33|+1.1|-19.8|
|D1|4|FAILED|FAILED|
|D1|33|+0.2|FAILED|
|D2|4|+1.2|-20.1|
|D2|33|+0.4|-20.6|

Full24-cell IQRs, win rates, all-method breach rates, I and oracle comparisons: summary.csv. Figure: mc-main.pdf/png.

## Frozen predictions

- P1: NOT_SUPPORTED.
- P2: UNASSESSABLE.
- P3: NOT_SUPPORTED.
- P4: UNASSESSABLE.

P1 is not supported: the calibrated constant-variance AR(1) retains state information, and longer histories improve QR substantially. Constant variance is not a no-information null. P3 is not supported: the complete short-weekly33-predictor cell misses the prespecified adverse threshold. P2 and P4 are unassessable because required hourly cells failed, not statistically rejected.

## Interpretation

The stationary weekly DGPs favor conditional models as W grows. This does not reproduce the persistent large weekly losses in the financial record. Changing W alters both QR estimation and F. Cross-DGP contrasts also bundle frequency, parameters, validation length, calendar and physical horizon. They cannot isolate their separate effects.

Seven hourly cells fail the unchanged solver acceptance test at the smallest declared penalty. The entire cells remain failed: no retry, altered tolerance, alternate penalty or partial-success median. The one complete hourly cell cannot establish the long-history FX mechanism. Events/stages/penalties/context are retained in analysis-facts.json; four-variable exceptions lack exact refit context, which cannot be reconstructed without a prohibited rerun.

The finite2000-path oracle approximates conditional quantiles; IQRs measure repetition dispersion, not confidence intervals. Calibration uncertainty is excluded. The hourly GARCH has no finite fourth moment under its archived parameters; no normal-CLT claim is made.

B3 therefore uses the task-authorized fallback third contribution: score/breach divergence. The simulation is reported as a bounded and partly unsuccessful mechanism check, not packaged as a supported explanation of the financial results.

## Technical completion

Numerical computation ran once and saved all outputs. Optional matplotlib was missing only at the subsequent plotting import. A separate uv environment ran the frozen plot code with presentation-only common-axis/marker/failure-label/print-size adjustments; no simulation, model or random draw was rerun. Original console: formal-console.log; plotting-receipt.json binds summary and frozen source.

All300 worker logs are retained locally and byte-for-byte in formal/worker-logs.zip plus its SHA manifest. Formal/replicates.json retains every repetition status, saved loss and candidate diagnostic. Initial figure versions were preserved as .bak before readability changes.

## Pending author decisions

Future work on hourly numerical feasibility requires a separate design retaining these seven failures. A frequency/validation factorial study, parameter uncertainty or new financial evidence also requires a later task. No such extension is made here.
