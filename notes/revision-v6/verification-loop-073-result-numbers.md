# Verification loop 073 — five actual Table 3 cells

Internal same-model display trace; prior-exposed repeat, not external peer review or independent statistical validation. First clock 2026-10-23 23:17:50 UTC; written 2026-10-23T23:19:16.857456+00:00. Branch revision-v4-jof; freeze HEAD `598a293bf706d1fa7601af2138fd327bf06482d3`. Parent goal stays active through 2026-10-24 00:31:50 UTC.

Table 5's 35 cells are exhausted. The complete 22 actual numeric Table 3 cells are reused from loop069's selection, whose bound main JSON hash equals the current `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`. Main/supplement/PDF content was not reopened. The complete frame, two nonnumeric “Outside family” exclusions and loop069's five excluded cell identities are retained in the companion JSON. Removing those five leaves 17 eligible cells; “remaining” does not mean unseen. Each L/R display is one actual table cell. Existing verdicts were not used to establish matches.

Seed 2026102373 and the ordered frame were frozen at 2026-10-23T23:18:03.927493+00:00, before owning-output lookup. `random.Random(2026102373).sample(range(17),5)` selected remaining-frame positions [14,12,13,7,3], corresponding to complete-frame indices [17,15,16,9,3]. Frozen JSON SHA-256 `d6831f7c8a09b8926ca3228b3b624da1cc4c9dddc59e5565811a1de687d6cdc5`. Lookup began 23:18:08.895797 UTC; scalar rows were first read at 23:18:17.464639 UTC. Displays, source files and scalar fields were already exposed in prior work; this is not blinded or new independent evidence.

| Order / cell | Exact saved scalar(s) | Static display / verdict |
|---|---|---|
| 1 FX legacy loss Δ% | paired: fx_hourly-h24-QR2880-minus-rolling_S720; relative_mean_loss_difference_percent = −1.8290714567022697 | signed .2f → −1.83; match |
| 2 Treasury breach % L/R | paired: nyfed_weekly-h6-QR260-minus-frozen_F260; strict_breach_count_left/right = 54/28; origin_count = 277 | existing line44 display rule → 19.495 / 10.108; match |
| 3 Treasury Kupiec p L/R | coverage: nyfed_weekly, H6, W260, QR/frozen_F; pof_p = 0.004126046248434382 / 0.1986410814587244 | .3g each → 0.00413 / 0.199; match |
| 4 FX matched breach % L/R | paired: fx_hourly-h6-QR2880-minus-frozen_F2880; saved counts 376/360; origin_count = 6625 | existing line44 display rule → 5.675 / 5.434; match |
| 5 FX original breach % L/R | paired: fx_hourly-h6-QR2880-minus-rolling_F720; saved counts 376/332; origin_count = 6625 | existing line44 display rule → 5.675 / 5.011; match |

Line44 is precisely `100*saved_count/saved_origin_count` formatted .3f on each side. Only this pre-existing display arithmetic was reproduced; no event counts or statistics were re-estimated from vectors. The legacy loss percentage was read directly, not reconstructed from mean losses. FX source unit is USD; Treasury is USD millions; the selected loss change and breach displays are percentages. Matched frozen_F2880 and original rolling_F720 remain distinct references despite the shared left count/display. H24 legacy remains distinct from H6.

Treasury full-origin breach denominator277 differs from sparse Kupiec n40, stride7, hits7/4 and DQ n267. These saved fields were read, not recalculated. Coverage left has ind_status=OK, boundary=False; right has ind_status=BOUNDARY_REFERENCE, boundary=True. The selected value is pof_p; no independence/CC reference validity is inferred from it. No NA or boundary status was suppressed/replaced. The two excluded “Outside family” cells receive no p-value.

Fresh owning reads: `results/revision-20261022/paired-comparisons.csv` and `results/revision-20261023/inference/coverage.csv`; exact selectors, strings and SHA-256 hashes are in JSON. Actual `v4_submission.py` lines11–17,34–48 was read as text, not imported/run; SHA-256 `11725bfe7c8922fb08ad8c6acb579bf53f890ab82967c52368c5f1f589022852`. Only selected static display expressions were reproduced.

Verdict: all five match, zero failures or substitutions; no necessary conclusion problem identified in this bounded trace and no conclusion edit. All six main/supplement JSON/TeX/PDF hashes remain unchanged at 2026-10-23T23:19:16.857456+00:00; exact hashes are in JSON. Only the two authorized loop073 files are written. No source/results/state/ledger change, commit, new statistic/count/model/proof/test, raw/private vector, network/UI, Claude or nested agent. Complete final readback and final hashes follow; no further edits after final delivery.
