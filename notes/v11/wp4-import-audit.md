# WP4 import audit — fixed PR5 source

**Overall: UNVERIFIED. Import decision: DO NOT IMPORT under the strict design-before-formal-run gate. Eligible imports: none.**

The selected WP4 figure is a display of already saved results, not a new scientific experiment. Artifact identity and readback checks PASS. An exemption from the user’s timing gate is not presumed: accessible Git objects do not establish a WP4 pre-render design commit/UTC together with formal-start and completion commits/UTC.

Fixed source: `60e03b8ae7a950c96ace3987f0625b3e434e6887`. Current branch inspected: `revision-v11`. Fresh audit completed: `2026-10-25T05:06:09.524876+00:00`.

## Verdicts

| Item | Status | Evidence/boundary |
|---|---|---|
| Selected artifact identity | PASS | FINAL-RENDER selects render-v5; all five output hashes match its render receipt and saved independent audit |
| Source identity and point readback | PASS | 380 unique records; exact saved y; rational c=W/(H+1); 190 per method; all source paths and hashes verified |
| Stored artists and range preservation | PASS | 760 exact offsets in four panels; each complete panel retains all 190 method records; labelled detail panels repeat records |
| Existing-result display scope | PASS | Contract, static plotter readback and receipt show zero new model fits/predictions; no new experimental design is invented |
| Design-before-formal-render chronology | UNVERIFIED | Original pre-render design/start/end commits are unavailable; public upload chronology follows actual rendering |
| Strict-gate import permission | UNVERIFIED | No files admitted; candidate artifacts remain only in scratch copies |
| Original/private financial replication | UNVERIFIED | Byte checks do not supply private inputs or independent financial replication; nine private WP3 seal records deliberately not read |

## Timing evidence

| Event | Recorded content UTC | Accessible commit and UTC |
|---|---|---|
| Display contract `protocol/revision-v9/wp4-display.md` | No embedded creation time | `3b8b994990da774c8abd0e1c28cbcacae3e9d0be`; `2026-10-25T04:00:56+00:00` |
| Source inventory | `2026-10-24T23:42:03.492040+00:00` | `ed00d1597b1ca02da4c8d33dc4537f033b5e0f95`; `2026-10-25T03:57:37+00:00` |
| First saved render completion | `2026-10-24T23:42:24.685879+00:00` | Original completion commit unavailable |
| Selected render-v5 completion | `2026-10-24T23:46:39.218742+00:00` | First public upload `0ee0ac928134137d97beb046511a027320bb4384`; `2026-10-25T04:07:59+00:00` |
| Selected render-v5 start | Exact separately timestamped start unavailable; approximate `2026-10-24T23:46:38.475850+00:00` | Formal-start commit unavailable |

The approximate render-v5 start subtracts the receipt’s `0.7428919579833746` seconds from its recorded completion. It is not an independent formal-start receipt. The public display-contract commit is after both saved renders. Its earlier position than the public render upload proves upload order only.

`notes/revision-v9/REPRODUCING.md` explicitly states that browser uploads created a different public history and did not export original local design objects. The current repository cannot read the following referenced commit objects:

- `bfd0493f4237b6b99ca4370a2e6cf2195f653b28` — unavailable; UNVERIFIED.
- `7f0fee8f1cfdeed584098bbc27570e88eafaea43` — unavailable; UNVERIFIED.
- `f2ce438ccb2fcf671c849a83032ac700ac6007c6` — unavailable; UNVERIFIED.
- `b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a` — unavailable; UNVERIFIED.

No forbidden old directory was read, no missing history was fabricated, and no alternative design commit or ancestry bypass was substituted. WP4 has a saved-result display contract, but no new-experiment-design object; calling this display “preregistered experimentation” would be unsupported.

## Byte and numerical readback

- The render receipt’s four source bindings and all six inventory source fingerprints match fixed-source Git blobs.
- All five delivered output fingerprints match both the render receipt and saved independent audit. The band source hash and its envelopes match the independent WP1 note.
- Every plotted y has a `source_path`, full SHA-256, source row JSON pointer and exact value in `point_numeric_bindings`. Both x operands and the exact rational c are bound there as well. No loss was recalculated.
- `band_and_cutpoint_numeric_bindings` binds every envelope endpoint and first cutpoint to the WP1 result path/SHA/JSON pointer. The source code reads the stored first cutpoint for its dashed line; the receipt does not separately store that line’s artist coordinate, and no fresh PDF coordinate replay is claimed.
- Fixed ticks and detail limits are identified as display constants. They have source-code or receipt locations and are not estimated scientific numbers.
- All 380 JSON/CSV point fields match. Render-v2/v3/v4 points JSON and CSV are byte-identical to render-v5.
- Family counts: 144 v8 simulation, 96 v9 conditional simulation, 120 original empirical, 20 learning-curve records. Exactly 48 F self-comparison rows are separately documented and excluded. They are not discarded conditional failures.
- There are 103 negative points, zero zero-valued points, and zero nonfinite/missing plotted points. Every point remains in a full-range panel; no same-x pooling, jitter, rounding or outcome trimming was observed.
- The 120 old empirical rows match their original saved CSV line, source, method, W, H, model loss and issue count. The existing `C2_QR4`→`QR4` and `QR`→`QR33` label mappings were verified from the source; the audit’s initial omitted alias is retained transparently in `audit_development_record`.
- All nine WP1 original input fingerprints also match the current branch’s inherited baseline bytes.

## Source receipts and dependency identity

| Dependency | Fresh verification | Status |
|---|---|---|
| WP2 package | Receipt archive/index hashes; all 30,536 member sizes and SHA-256 values; public summary, manifest and termination bytes equal archived members | PASS |
| WP3 package | Receipt archive/index hashes; all 206 member sizes and SHA-256 values; public contrasts, manifest and termination bytes equal archived members | PASS |
| WP1 original simulation reports | All 6,912 saved member-binding records match the original v8 archive members | PASS |
| WP1 input evidence | Nine path/size/SHA fingerprints match fixed source and inherited HEAD result identity | PASS |
| WP2 runtime code/design seals | All 13 public sealed paths match their own runtime manifest | PASS |
| WP3 runtime code/design seals | All 26 public sealed paths match their own runtime manifest | PASS |
| WP3 private runtime seals | Nine private/scratch files intentionally unavailable in authorized Git-only scope | UNVERIFIED |

These checks establish saved artifact identity. They do not repair unavailable original design-commit ancestry, prove independent financial replication, or turn the WP3 repeated period into a new financial holdout. WP2/WP3 admission remains subject to their separate v11 audits.

## Repeated observations and adverse evidence

Eight old-FX/WP3 pairs represent the same W/H/procedure tasks on the same inspected period. Their original stored ordinates are retained, including final-bit differences from the two frozen arithmetic expressions. Exact numeric equality is not asserted and no new tolerance is registered. The eight pairs are not independent validation observations. WP2’s P3 failure, long-W reversals, post hoc fixed-grid envelope limits, and failed rendering attempts must remain in the evidence and narrative.

The stored final PNG was freshly opened and inspected: complete/detail labels, extreme and negative points, legend, footer overlap warning, and source marks are visible. No fresh PDF raster was generated; the PDF’s exact SHA and the archived PDF visual-QA record were checked. This fresh visual claim therefore applies to the stored PNG only.

## Minimal artifact list

**Currently eligible under the strict gate: empty.** The following is the smallest conditional candidate set, not authorization to import:

| Candidate path at fixed source | SHA-256 | Bytes |
|---|---|---|
| `results/revision-v9/wp4/render-v5/unified-history.pdf` | `694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3` | 40098 |
| `results/revision-v9/wp4/render-v5/points.json` | `c04932d44d0485008c5f8c3b314c6ea1e77f7e52f5b0cf8b026deb80180ac1ed` | 301512 |
| `results/revision-v9/wp4/render-v5/render-receipt.json` | `3bd8b199e5f6bd75c24efd69826714e43699846a25da5806606a3c6bc26a09a0` | 128800 |

If separately admitted later, retain FINAL-RENDER, excluded-reference rows, source inventory, independent audit, visual-QA record and display contract alongside the candidate. The full machine audit preserves their fingerprints. No failed or missing evidence is deleted.

## Caption suggestion

Unified display of 380 previously saved conditional-model records against c=W/(H+1): 144 discovery-simulation cells, 96 confirmation-simulation cells, 120 original empirical cells and 20 same-period FX learning-curve cells (190 per procedure). Forty-eight F self-comparisons are separately documented and excluded. Complete-range panels retain every point; labelled detail panels repeat the same records. Eight FX tasks overlap the original inspected period and provide no independent validation. Shading reproduces the post hoc, fixed-grid all-draw first-cutpoint endpoint envelopes; c omits parameter count and is not an estimated effective sample size. Connected FX segments are descriptive and permit long-history reversals. The figure does not establish a universal threshold, a pure estimation-cost channel, or a fresh financial holdout; retain the failed universal simplification prediction. Original pre-render chronology is unverified in the public Git history.

## Action boundary

Only this audit Markdown/JSON and exact Git blob copies beneath `.scratch/v11/wp4-audit/` were written. No checkout, branch creation/change, commit, experiment, scoring, summary driver, model fit, prediction, bootstrap, or research result/protocol/data edit occurred. No Claude or cross-model review was invoked.

## Provenance reconciliation — appended 2026-10-25T05:08:00.915831+00:00

This addition preserves the initial **UNVERIFIED / no import** assessment and every original numerical binding. It records new original-repository evidence supplied after that assessment. The root audit will make the final conservative applicability/admission decision; this addition grants no exemption.

Evidence: `notes/v11/original-commit-proofs.json`, SHA-256 at read `eafbb501cc4870e19ef87bc6e108f794e64fd3ceaa3f3040b60f2ddc43ad6152`. The root used read-only original Git-object queries and recorded identical source HEAD before/after: `689d4928f55bb73cac5b73e6cfc34aee1209e57a`. This subagent read the supplied proof and independently recomputed the Git commit SHA-1 from each raw commit body; all four identities match.

| Source dependency | Original design commit UTC | Saved formal numerical run start UTC | Original completion commit UTC | Timing-only verdict |
|---|---|---|---|---|
| WP2 | `f2ce438ccb2fcf671c849a83032ac700ac6007c6` — `2026-10-24T22:19:50+00:00` | `2026-10-24T22:25:19.696709+00:00` | `1a535efe289254ced5b163361fefee357d13d583` — `2026-10-24T22:59:15+00:00` | PASS; end parent is design and design predates start |
| WP3 | `b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a` — `2026-10-24T23:13:51+00:00` | `2026-10-24T23:24:51.666335+00:00` | `bfd0493f4237b6b99ca4370a2e6cf2195f653b28` — `2026-10-24T23:39:27+00:00` | PASS; end parent is design and design predates start |

These timing facts do not resolve separate scientific/strict-anchor requirements. WP1’s existing post hoc design object is not included in this supplied proof snapshot and receives no new timing verdict here.

The original source history identifies WP4 completion and first committed source inventory / FINAL-RENDER as `32ee58688bac260de322c31cb8945adbf3b53154`, UTC `2026-10-24T23:49:08Z`. This follows the first saved render (`23:42:24.685879Z`) and selected render-v5 (`23:46:39.218742Z`). The inventory’s earlier embedded creation text is not proof that the inventory or display contract had been committed before plotting. The raw WP4 commit body and original display-contract path history are not present in this proof snapshot.

| Gate interpretation | Status | Meaning |
|---|---|---|
| New experimental design must precede a new formal numerical experiment | **N/A for WP4** | WP4 has no new formal numerical experiment. The contract, static plotter and receipt establish only rendering of saved outcomes, with zero new model fits, predictions or inferential statistics. WP1/WP2/WP3 keep their original designs and limitations. |
| The display/plotting contract itself must be committed before rendering | **UNVERIFIED — NOT PASSED** | No pre-render contract commit is established by this snapshot. The original inventory/FINAL-RENDER completion commit and public contract upload both postdate rendering. The stricter interpretation is not waived. |

“No formal numerical experiment” does not mean that no program ran: a display render ran and copied the existing numerical outcomes. It does mean no new WP4 experimental result, fit, forecast, score or inferential test was produced. The initial report’s object-availability limitation was accurate for the published/current repository; the new original-object proof adds earlier WP2/WP3 provenance without changing a saved result.

All scientific values, source paths, SHA-256 values, 380 point bindings, 103 negative points, eight repeated-period pairs, excluded F rows, P3 failure and long-W reversals remain unchanged. `eligible_imports` remains empty until the root’s explicit aggregate adjudication.

## Definitive provenance reconciliation — appended 2026-10-25T05:09:54.555023+00:00

**Latest strict display-contract gate: NOT_PASSED. Root adjudication: DO NOT IMPORT WP4; no pure-display exemption.** The initial UNVERIFIED report and preceding reconciliation remain preserved as the historical evidence sequence.

New primary object evidence: `notes/v11/original-blob-proofs.json`, SHA-256 `126ddc187c93beb656c5c93e8187ed24a98492a16491630dac8c5569c1fa1c33`. The original raw WP4 commit body independently hashes to `32ee58688bac260de322c31cb8945adbf3b53154`. Its committer UTC is `2026-10-24T23:49:08+00:00`, its parent is the original WP3 completion `bfd0493...`, and its changed-path record adds `protocol/revision-v9/wp4-display.md`. The original path history confirms this is that contract’s first commit.

The contract commit is therefore later than the first render completion (`2026-10-24T23:42:24.685879Z`) and render-v5 completion (`2026-10-24T23:46:39.218742Z`). The stricter requirement now has definite contrary evidence: it is **NOT_PASSED**, not only unverified.

All six WP4 original/public mappings were independently checked against the pinned `60e03b8...` blobs: contract, source inventory, FINAL-RENDER, selected points, selected render receipt and PDF. Their Git blob IDs, SHA-256 values and byte lengths match; the original source HEAD is recorded unchanged.

WP4’s new-experiment gate remains N/A because it only displays existing saved results. That applicability fact grants no exemption from the user’s stricter precommitted-display-contract rule. The root has explicitly chosen the conservative strict interpretation and rejected the WP4 import. `eligible_imports` remains empty. Every original numerical binding and adverse result remains unchanged.
