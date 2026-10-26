# Verification loop 093 — five current Table 3 numeric cells

Internal same-model field/display trace, prior-exposed; not external review. First clock 2026-10-23 23:42:14 UTC; written 2026-10-23T23:44:32.031513+00:00. Branch revision-v4-jof; initial HEAD `8906bee6e1f7f93090964cb45ea50be4fea0eeb5`; freeze HEAD `b7065ade6ba60c7b13397076f1600b5feda855af`. Goal stays active through 2026-10-24 00:31:50 UTC. This note does not certify compilation, tests, publication or the whole loop092 language candidate.

Current main JSON SHA-256 is `b9197f80173b8dccbb74cb2086cea202a4f2d1c1659768f7f62835a1a9a1510b`, different from089's `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`. Freshly extracted actual Table3 at `$.sections[5].blocks[0]`; no full-hash equivalence or inherited-frame assumption. Old Git main at089 freeze ref61d60e8 was read solely for Table3; its hash matched089's binding. Complete Table3 blocks including bindings compare equal as sorted-key compact UTF-8 JSON bytes, SHA-256 `ad74f194cf60e93992db169e75ae64e42f964de19daab314b09bd4a4ec785af7`. This is canonical table-byte equality, not whole-source or whitespace-byte equality. The freshly enumerated22 numeric cells also equal089's stored frame.

Predeclared repeat: exclude ONLY089's five identities, leaving17 eligible. Complete22 current frame, two nonnumeric “Outside family” exclusions and exact ordered eligible17 are in JSON. Each L/R display is one cell. No unused/unseen or cumulative-chain remaining count is claimed; cells/files/scalars have prior exposure. Old verdicts do not establish matches. Table5 is exhausted.

Seed2026102393/frame/draw frozen 2026-10-23T23:42:41.447455+00:00. `random.Random(2026102393).sample(range(17),5)` drew positions [15,11,8,7,2], full-frame indices [17,13,10,9,3]. Frozen JSON SHA-256 `1747ba097fcea1b00057044c5328e4a27a0937c2d8fb47297171202102edcd48`. Owning lookup began 23:43:08.679091 UTC; first scalar read ended23:43:08.680963 UTC, after freeze. Evidence append preserved frame/exclusions/seed/draw, without replacement.

| Order / actual cell | Exact saved field(s) | Display / verdict |
|---|---|---|
| 1 FX legacy loss Δ% | fx_hourly-h24-QR2880-minus-rolling_S720: relative_mean_loss_difference_percent−1.8290714567022697 | signed .2f → −1.83; match |
| 2 Treasury HLN p | nyfed_weekly-h6-QR260-minus-frozen_F260: hln_p0.009390617005130322; n277/bandwidth6/statusOK | .3g → 0.00939; match |
| 3 FX matched Kupiec p L/R | H6 QR2880/frozen_F2880: pof_p0.6952768918173253 / 0.8067032386212847 | .3g each → 0.695 / 0.807; match |
| 4 FX matched breach % L/R | fx_hourly-h6-QR2880-minus-frozen_F2880: saved counts376/360, origin_count6625 | line44 display → 5.675 / 5.434; match |
| 5 FX original breach % L/R | fx_hourly-h6-QR2880-minus-rolling_F720: saved counts376/332, origin_count6625 | line44 display → 5.675 / 5.011; match |

Loss percentage is read directly, not rebuilt from means. Line44's existing `100*saved_count/saved_origin_count` .3f conversion alone was reproduced; no raw-event recount/new rate estimate. FX paired unit is USD, Treasury USD millions; p-values are dimensionless, loss/breach displays percentages. Matched frozen_F2880 differs from original rolling_F720; legacy H24 rolling_S720 differs from H6. Full paired n6625 differs from matched sparse Kupiec n947/stride7/hits50,49 and saved DQ n6615. Both selected coverage rows retain ind_statusOK/boundaryFalse; no NA/family/boundary substitution. OK does not validate a reference distribution.

Fresh scalar reads: `results/revision-20261022/paired-comparisons.csv`; `results/revision-20261023/inference/dm.csv` and `coverage.csv`. JSON stores exact selectors/strings/hashes. Numeric formatter `v4_submission.py` lines11–17,34–48 and current route `v6_submission.py` lines7–12,16–49,158–190 plus targeted matches were read as text only. The latter copies/remaps table labels/retags blocks; full table equality was separately checked. Formatter/route hashes and filename-only script-location inventory scope are in JSON. No script import/run, build or test occurred.

Verdict: five matches, zero failures/substitutions; no necessary conclusion problem within this trace and no conclusion edit. All six current main/supplement JSON/TeX/PDF hashes remain unchanged at 2026-10-23T23:44:32.031513+00:00; full hashes are in JSON. Only loop093 JSON/MD writes. No source/results/state/ledger edit or commit, new statistic/event count/model/proof/test, raw/private vector, network/UI, Claude or nested agent. Complete final readback/hashes follow; no edits after final delivery. Field/format verification only.

Metadata readback correction 2026-10-23T23:45:00.869625+00:00: initial and freeze HEAD are now separately recorded; frozen JSON, draw and numeric evidence were already correct and unchanged.
