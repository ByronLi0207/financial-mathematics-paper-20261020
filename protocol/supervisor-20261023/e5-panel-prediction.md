# E5 pre-run prediction freeze

This document is committed alone before the first new E5 model fit. It fixes predictions for a later exploratory diagnostic after the original panel QR33 and QR4+ outcomes have already been inspected. It is not an original study preregistration or an independent replication.

## Fixed inputs and lineage

Reuse exactly the twelve eligible series and their order from the earlier frozen panel manifest. No download, series substitution, addition, removal, splice, interpolation or missing-date fill is permitted. Raw observations and per-origin financial arrays remain private; public provenance, source hashes, aggregate results and receipts are archived under `results/supervisor-20261023/e5/`.

The eligible list consists of three asset totals, four TIPS series and five coupon maturity buckets. Two calendar-ineligible earlier downloads remain skipped. All twelve are aligned to the unchanged 706-date original PDPOSGS-B grid, 2013-04-03 through 2026-10-07. Shared dealer reporting, overlapping economic positions and same-key definition changes limit interpretation; the twelve series are not twelve independent dealer samples.

| Series key | Raw bytes | SHA-256 |
|---|---:|---|
| PDPOSMBS-TOT | 25680 | `2e493d17890870eff6eca247c62b9175fcf7564a70d87e63ee520561bb71efcb` |
| PDPOSCS-TOT | 24713 | `169fdb5201f6a34152936f0aa2b444d9ea0f8814d39750bfd4a4bc942a41fade` |
| PDPOSFGS-TOT | 25495 | `00f321abeebf1aaee1af68dc7ab41bb403eafe770c915f4229fc80e18e3586de` |
| PDPOSTIPS-L2 | 24883 | `dc3dd1ef3f9a364c25789523a5b2f0d46860681808005620055db4a47c996995` |
| PDPOSTIPS-G11 | 25017 | `810355b1cf4c93282dcc76fa6fdc41bbccc1ec7d3675024a2400e2c27c695d5d` |
| PDPOSTIPS-G2 | 24761 | `8e54675071813501a240c1ea3a2ca4fda0f2e2aa88b1ea1bb2852fe6a9f6c894` |
| PDPOSTIPS-G6L11 | 26797 | `1e3ee3a336be321f47a3f7481591b15650607baa3fb46be7da99968ccbea7845` |
| PDPOSGSC-L2 | 24714 | `7ab08e2b39534ca67f43006949a7504334d90b63034b9ed3cd5248e59c9126bf` |
| PDPOSGSC-G2L3 | 25930 | `10c35a9516154011c0821d12eb86052f7d4df01a4c7b0cddee4878b72868678c` |
| PDPOSGSC-G3L6 | 26090 | `453f1a2458a2c9c7049d9128ccc9d1945b5a61e469ab1c8112577b3ad7539fa5` |
| PDPOSGSC-G6L7 | 25967 | `429d542e2cda305d8d5c458592b57b4042c9f479ce4135e3ab3610951ae6b35d` |
| PDPOSGSC-G7L11 | 26639 | `0b102760c5e4cc181d438d9c8618f8990d047ac8ecb9bd85bac63851742199d0` |

Frozen manifest SHA-256: `c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858`.
Original panel summary SHA-256: `34134445a00354dcce3dc43de4c2adada7f2ea5403212558f90ef3480ee810f9`.
Original economic-grid CSV SHA-256: `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb`.

## Fixed procedure

Use the existing `round2_panel_sources.py` alignment and the QR33 segment of `round2_panel_run.py`, minimally ported to the present checkout and E5 output paths. Keep the existing forecasting core, optimizer, numerical tolerances, past-only feature construction, training standardization and response scaling unchanged. No new fitting family or tool-edge-case work.

For each series use H in {6,24}, W in {52,260}, and `StudyConfig(H,W,13,6,26,604800)`. Validation origins are 329–380 inclusive (52 issues; 2019-07-24 through 2020-07-15). Evaluation origins are 405–681 inclusive (277 issues; 2021-01-06 through 2026-04-22). Refit every 13 records on completed labels. Preserve the original segment restarts.

Fit all 33 predictors with an unpenalized intercept. Extend only the ridge menu from {0.001,0.01,0.1} to {0.001,0.01,0.1,1,10}. Every candidate must complete every validation issue; an incomplete/failed candidate makes the entire cell ineligible. Select by lowest native-unit validation mean pinball loss; exact ties choose the larger penalty. Save the selected parameter and complete menu before evaluation begins. Never select by the evaluation curve.

Reuse and independently rescore the archived F, original QR33 and QR4+ arrays without refitting them. Recompute ordinary empirical frozen headroom I using `ceil(.95 W)`, with the existing implementation and refit schedule. F retains `ceil(.95(W+1))`. Strict breach means peak > capacity, equality is a nonbreach. The main comparison uses the same .95 pinball loss and source-native USD millions.

## Predictions fixed before the new run

- **P1:** Among the **45 fixed cells** whose archived original QR33 loss exceeds F, at least **40** will have new QR33+ mean loss strictly below original QR33.
- **P2:** At least **36 of all 48 cells** will have `100*(QR33+ loss - F loss)/F loss` in the **inclusive interval [-10%,+10%]**.
- **P3:** More than half of all 48 cells, meaning at least **25**, will select **lambda >= 1**.

Report each prediction as supported or unsupported by its exact count and threshold. No threshold, menu, tie rule or membership change is allowed after outcomes. P1's subset is fixed by the original archive before the run, never by the new results. Missing or failed cells do not count toward any success count and are never removed from the fixed denominators (45 for P1; 48 for P2/P3). No pooled significance calculation treats the twelve series as independent.

## Execution limits and complete reporting

Run in manifest order, then H6/W52, H6/W260, H24/W52, H24/W260. One worker and one numerical thread; keep the existing 2 GiB RSS limit and at most 590 seconds per cell. The total E5 calculation hard stop is **10,800 seconds (three hours)** from its first run start, including time spent in failed cells. Stop rather than extend or retry. Use exclusive new attempt directories; no automatic retry suffix, overwritten attempt or failed-fit replacement.

Report all 48 planned rows, including COMPLETE, VALIDATION_INELIGIBLE, EVALUATION_FAILED, TIME_LIMIT or NOT_RUN_TIME_LIMIT as applicable. Preserve partial candidate diagnostics and terminal reasons. A failed cell does not contribute a shortened score. The public table must contain series, H, W, status, F, original QR33, QR4+, QR33+, I, selected penalty and strict breaches for the compared reports. The final summary must show the fixed P1–P3 decisions even if they fail.

A receipt will record this file's committed Git SHA, Git commit timestamp, file hash, run-start timestamp, all source identities and the actual run completion/stop time. The commit must precede the first model fit. The E5 item has a 3.5-hour total budget, and an unfinished item stops after its 150% ceiling under the user's global rule; this never extends the three-hour calculation stop.

## Interpretation fixed in advance

If stronger shrinkage helps, describe how much deterioration it removes and what remains. Failure of P2 supports the narrower statement that expansion mitigates rather than eliminates the observed weakness. No result establishes that predictors contain no usable information, equivalence of methods, future evaluation noninferiority or independent external validation.
