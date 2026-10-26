# WP2 v11 import audit

Pinned source: `60e03b8ae7a950c96ace3987f0625b3e434e6887`.

**Decision: UNVERIFIED; import_allowed=false.** Do not import a WP2 table or numerical claim into v11 under the required provenance gate. The original design commit and WP2 completion commit are absent from this repository.

## Provenance

- Missing original design object: `f2ce438ccb2fcf671c849a83032ac700ac6007c6`. Its UTC and changed-path list are unavailable; the assertion that it was a separate pre-run design commit is unverified.
- Missing original completion object: `1a535efe289254ced5b163361fefee357d13d583`. Missing WP1 completion object: `9784372d523e93a50f21212e9a10adb55485768c`.
- Verified public design upload: `3b8b994990da774c8abd0e1c28cbcacae3e9d0be`, author/committer **2026-10-25 04:00:56 UTC**; seven protocol files changed. This is later than the recorded formal start **2026-10-24 22:25:19.696709 UTC**.
- Verified public results upload: `81e9ac550fc27f7412dd2d0df0c3293bd45f2b4a`, author/committer **2026-10-25 04:03:02 UTC**. This proves publication of bytes, not original completion-time provenance.
- Saved design/run/end/receipt metadata are internally ordered. They cannot establish missing commit objects or their original UTC. No external directory was consulted.

## Byte integrity

- Archive SHA-256: `aa794fc6b83c0e4e74f98b11aa4768a90f6f03dfe052fda9d679cd9e88972e7a`; matches its own package receipt.
- Member-index SHA-256: `9e942726a6c5bec102ad7c25fb2e4a5b000df59694fce87831517ce85fb9a3ba`; matches its own package receipt.
- All **30,536** tar members checked against the full own index; **0** byte/size/hash mismatches, **0** missing/unexpected members; **83,094,855** uncompressed bytes.
- Published manifest, summary.json, summary.csv, support.json, study-termination.json and budget-decision.json equal their indexed tar members byte for byte.
- All 13 source/code/protocol seals match the pinned Git blobs. This verifies byte identity, not pre-run existence.

## Saved outcomes retained without recomputation

| Prediction | Saved successes / fixed denominator | Missing | Required fraction | Saved screen |
|---|---:|---:|---:|---|
| P1 | 47/48 | 0 | 0.8 | SUPPORT |
| P2 | 21/24 | 0 | 0.6 | SUPPORT |
| P3 | 42/48 | 0 | 1.0 | NOT_SUPPORT |

This table is a source-bound **future template only**, blocked from import now. Every numeric cell is bound to an exact source path, SHA-256 and JSON pointer in `wp2-import-audit.json`. All method and DGP P1/P2 backing rows are recorded there without selection.

Static records contain 144 summary cells, all COMPLETE, with 32 completed repetitions per cell and zero failed/unattempted repetitions. The archive selected-report inventory contains 4,608 COMPLETE entries. Candidate status counts: `{'COMPLETE': 12286, 'FAILED': 2}`. Worker status counts: `{'COMPLETE': 192}`. No budget removal is recorded. These are saved-status inventories, not a numerical replay.

The two saved candidate failures are both QR4 penalty `0.001`, status `FAILED`, reason `NONCONVERGENCE`: `units/rep-010_dgp-0_phi-1/W52_H24_QR4.json#/candidates/0` and `units/rep-014_dgp-0_phi-0/W52_H6_QR4.json#/candidates/0`. Their full original failure diagnostics, exact member SHA and archive SHA remain in the JSON. The frozen QR4 rule allows selection among completed candidates while retaining failed candidates.

All ten declared counterexample rows are retained, including one P1, three P2 and all six failed P3 inequalities:

| Prediction | DGP | phi | W | H | Method | Saved adverse value(s) |
|---|---|---:|---:|---:|---|---|
| P1 | student_t5 | 0.7 | 720 | 24 | QR33 | -1.346460491424284 |
| P2 | student_t5 | 0.7 | 720 | 6 | QR4 | 7.312975832354329 |
| P2 | student_t5 | 0.9 | 720 | 6 | QR4 | 0.8986970904158786 |
| P2 | student_t5 | 0.9 | 2880 | 6 | QR33 | 0.03462371888021121 |
| P3 | student_t5 | 0.7 | 720 | 6 | QR4_vs_QR33 | QR4=7.312975832354329; QR33=4.830690418857531 |
| P3 | student_t5 | 0.7 | 720 | 24 | QR4_vs_QR33 | QR4=16.02356520538195; QR33=-1.346460491424284 |
| P3 | student_t5 | 0.9 | 720 | 24 | QR4_vs_QR33 | QR4=2.63174423575232; QR33=1.5806851456921622 |
| P3 | student_t5 | 0.9 | 2880 | 24 | QR4_vs_QR33 | QR4=-6.545515431604143; QR33=-10.918683141764108 |
| P3 | regime_3to1 | 0.7 | 2880 | 6 | QR4_vs_QR33 | QR4=-10.774924657612761; QR33=-11.039777078608381 |
| P3 | regime_3to1 | 0.9 | 720 | 24 | QR4_vs_QR33 | QR4=14.634735498897422; QR33=12.44685994746002 |

No failed criterion is recast as a majority claim. P3 remains NOT_SUPPORT. The screen is finite-grid and pooled; c excludes parameter count, menus differ and no oracle separates approximation, regularization and estimation-cost effects.

## Boundary and retained evidence

Only pinned Git blobs and existing current-repository Git objects were read. Copies of 34 original Git blobs are in `.scratch/v11/wp2-audit/`; their paths, blob IDs and SHA-256 values are indexed in the JSON. No results/data/protocol path was modified. No checkout/cherry-pick, experiment, original summary program, fit, score, bootstrap or driver was run. No Claude/cross-model review was used.

The historical independent-audit PASS and full-test receipt remain source assertions, not fresh reproduction claims. Validation selection was historically checked against saved scalar validation losses because issue-level validation forecasts were not saved. The full-test output still matches its own recorded SHA.

Only the original commit-object provenance can resolve the import gate; public post-run upload timestamps and metadata true flags are insufficient.
