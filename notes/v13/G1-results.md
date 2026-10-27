# G1: τ = 0.99 post-failure repair result

The predeclared consistency gate failed: **6/10** fitted examples meet the pointwise relative-forecast error threshold **1e-6**. The other four maxima range from **1.6645049920077414e-5** to **1.0376561296174956e-4**. Every repaired fit passed all three original residual/gap conditions, but that does not satisfy the independent forecast-preservation gate. No setting, threshold, or example was changed; no second repair was attempted.

|Example|History W|λ|Maximum pointwise relative error|Outcome|
|---:|---:|---:|---:|---|
|1|52|0.001|4.06986951323e-05|FAIL_PREDICTION_DIFFERENCE|
|2|52|0.01|3.17244027887e-07|PASS|
|3|52|0.1|0|PASS|
|4|52|1.0|0|PASS|
|5|52|10.0|1.66450499201e-05|FAIL_PREDICTION_DIFFERENCE|
|6|260|0.001|7.87266935802e-05|FAIL_PREDICTION_DIFFERENCE|
|7|260|0.01|0|PASS|
|8|260|0.1|0|PASS|
|9|260|1.0|0|PASS|
|10|260|10.0|0.000103765612962|FAIL_PREDICTION_DIFFERENCE|

These ten cases were fixed before fitting: first two saved CFTC contract-history candidates, all five finite penalties, with each first-refit block covering13 predictions. No examples were replaced. This is a numerical-compatibility test, not evidence that financial forecast gains vanish.

Per the binding gate, the three original failed cells are **NOT_RUN_CONSISTENCY_GATE**; all their validation and evaluation outputs remain unavailable. No candidate from a failed cell was newly fitted, no old archive was overwritten, and no partial success was promoted. The old Q1 and Q2 remain **UNDETERMINED**. The separately labelled post-failure assessments also remain **UNDETERMINED**: F is known to win28/34 CFTC cells with one unknown (four ties and one regression win), and both FX periods remain unresolved.

Formal run started 2026-10-26T03:11:01.592871+00:00, ended 2026-10-26T03:11:01.768033+00:00, elapsed 0.17517212545499206 seconds. This includes the binding ten-fit gate and terminal records; it must not be described as three failed-cell reruns. Designbad6722d preceded all fitting; code16e95536 was sealed first.

The repair is therefore **not adopted** in the manuscript or in G2/G3. Future numerical work would need a separately authorized design; this revision retains the failure and states its limit. CVXPY/Clarabel were exercised only by toy unit tests, because adaptive ADMM completed all ten gate fits and the gate then rejected adoption.

Sources: results/v13/tau-repair/consistency.json; summary.json; runtime.json; code-seal.json. SHA bindings are in output-manifest.json.
