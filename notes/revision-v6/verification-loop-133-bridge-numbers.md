# Verification loop133 — five actual Table4 bridge cells

Internal same-model saved-field/display trace, prior-exposed. First clock `2026-10-24T00:23:28.955799+00:00`; evidence appended `2026-10-24T00:24:28.340255+00:00`. Branchrevision-v4-jof; freezeHEAD `f60873c5ff85187762e3b5a855c16c174bf544f8`. Parent goal active through2026-10-24T00:31:50Z, no overall completion claim. Fixed96 excludes later133.

Fresh current Table4 is `submission-jof/manuscript-content.json`, `$.sections[5].blocks[2]`. Main SHA256 `b9197f80173b8dccbb74cb2086cea202a4f2d1c1659768f7f62835a1a9a1510b`. Canonical tableSHA256 `61a2be66173d91f0efcf5b6b99f262dee1f38db87697fda5c13d3df449abde74` (sorted-key compact UTF-8 JSON, not whitespace-byte equality). Six main/supplement artifact hashes unchanged; full values in JSON. Other artifact contents hash-only.

Complete6 actual displayed result cells, no exclusions, frozen with seed2026102433 at `2026-10-24T00:23:28.959498+00:00`. `random.Random(2026102433).sample(range(6),5)` drew[2,1,5,0,3]. Full frame/IDs/displays retained in JSON; labels/settings do not count. Prior exposure is explicit; no unused/unseen/blinded/independent claim. FrozenJSON SHA256 `680c2c961783547ec6287326d94489af95e3dcb500f49d243b10e8f2d8f7d3bc`. Lookup began00:23:42.606703UTC and first selected scalar read ended00:23:42.607329UTC, after freeze. No resampling/substitution.

Owning saved output `results/revision-20261023/v5-novelty/gain-decomposition.json`, SHA256 `9cc9192a969b51b910b18dc46e6b5d2ab1beea05633a6f05e76f026dc041d6b8`. All5 selected owning fields exist; no derivation fallback.

| Order / actual Table4 cell | Exact saved field / raw string | Original display / verdict |
|---|---|---|
| 1 Frozen F W2880→QR W2880 / USD | estimator_difference_native = -66848.0979580874 | −66,848.09796; match |
| 2 Rolling F W720→frozen F W2880 / % original | length_update_difference_percent_original_reference = 2.47161342538997433466739110552915911527618872501184464823793 | +2.4716; match |
| 3 Original primary total / % original | total_difference_percent_original_reference = -12.6601264129697733607913887312172123117816985431877568719227 | −12.6601; match |
| 4 Rolling F W720→frozen F W2880 / USD | length_update_difference_native = 10918.94640933126 | +10,918.94641; match |
| 5 Frozen F W2880→QR W2880 / % original | estimator_difference_percent_original_reference = -15.1317398383597476954587798367463714270578872681996015201607 | −15.1317; match |

Fresh text-only `v5_submission.py`11–36:22–23 formats Decimal(str(saved)) with explicit sign/comma grouping and replaces minus by U+2212;34 binds these saved fields, USD5dp and original-reference percentage4dp. Only that existing display conversion reproduced. No subtraction, division, summation, additivity check, inference or script execution. `v6_submission.py`23–32,44–49,167–189 reread for current Table5→Table4 remap/copy/retag route, not run. Full static hashes in JSON; old005 verdict was not used.

Saved context is post-result/exploratory descriptive bridge, nativeUSD, origins6625, first/last source indices11927/18551. Exact primary `fx_hourly-h6-QR2880-minus-rolling_F720` and matched `fx_hourly-h6-QR2880-minus-frozen_F2880` identities reread in bound `paired-comparisons.csv`; actual SHA matches saved source_sha256. Original primaryTrue/cross-window and matched common_history/primaryFalse remain separate. All percentage-point cells use original rolling_F720 mean pinball denominator (saved441774.03703851684), not matched-reference denominator. No ratio was recalculated. First contrast jointly changes history/update; middle contrast changes the full conditional procedure and is not an isolated estimator or causal effect. These are changes in a pinball score, not measured financing costs/capital savings. Stored COMPLETE is process metadata, not validity proof.

Verdict5matches,0failures/substitutions, no scope gap/necessary conclusion problem; no conclusion edit. This bridge contains no sampled coverage-grid/DQ/NA statistic. No independent statistical/financial/causal validation or compile/test/publication certification. Only133MD/JSON written; no source/results/state/ledger edit or commit; no new monetary analysis/statistic/rate/event count/model/proof/test/vector/network/UI/Claude/nesting. Final complete readback/hashes follow; FINAL then immutable.
