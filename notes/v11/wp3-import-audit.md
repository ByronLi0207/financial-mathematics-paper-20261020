# WP3 read-only import audit

**Decision: FAIL — do not import WP3 into v11.** The mandatory exact anchors fail, and the claimed separate pre-run design commit is unavailable in the current repository. No experiment, scoring, summary rebuilding, refit, checkout or commit was performed.

Pinned PR5 source: `60e03b8ae7a950c96ace3987f0625b3e434e6887`. Existing v10b owning-source base: `de1a1cf22a005179f0d9a7c288855591292ddb49`.

## Exact anchor gate

| H/W/method/reference | v10b archived full precision | PR5 contrasts full precision | display, both | exact |
|---|---:|---:|---:|---|
| H6/W720/QR33/matched F | -2.1167271486370858 | -2.1167271486370893 | -2.12% | FAIL |
| H6/W2880/QR33/matched F | -14.766762552613885 | -14.766762552613883 | -14.77% | FAIL |

Original source: `results/revision-20261022/paired-comparisons.csv`, SHA-256 `a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9`. W720 physical line 2 (`contrast_id=fx_hourly-h6-QR720-minus-frozen_F720`), W2880 physical line 14 (`contrast_id=fx_hourly-h6-QR2880-minus-frozen_F2880`), field `relative_mean_loss_difference_percent`. v10b explicitly binds these in `notes/v10/main-number-audit.json#/old_archive_locator_checks/217` and `/0`, SHA-256 `a014dff6641fa8daeaa0c10fa390fb4f798a671ce57c48d218485bfaef377708`.

New source: `results/revision-v9/wp3/contrasts.json`, SHA-256 `576e9070644e211d417f84efba6a8b77b295be8e1f5870a5ec42aed7d7362ce4`, W720 `/8/relative_loss_percent`, W2880 `/0/relative_loss_percent`. CSV SHA-256 `f3a9cbc35cb310a6eb2371e06619638feac4d2add13ba78f68bf8042115bdd86`, physical lines 10 and 2 respectively. Decimal differences new minus old are `-3.5E-15` and `2E-15` percentage points. Neither numeric nor string equality holds. The two means and breach counts are retained in the inventory; displayed rounding does not establish strict equality. No tolerance was applied. Other existing e3 percentages happen to match new values, but they are not substituted for the v10b owning anchors.

## Time and Git provenance

- Claimed design commit `b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a`: `git cat-file` / `git show` return missing object. Its object timestamp, content and ancestry are **UNVERIFIED**.
- Receipt timestamps: design created `2026-10-24T23:10:52.678962+00:00`; pre-result check `2026-10-24T23:13:50.989187+00:00`; pre-run code binding `2026-10-24T23:24:35.895093+00:00`; formal start `2026-10-24T23:24:51.666335+00:00`; formal end `2026-10-24T23:35:21.429167+00:00`; package `2026-10-24T23:36:47.665646+00:00`; acceptance `2026-10-24T23:39:21.096007+00:00`.
- These internal timestamps are ordered as claimed, and protocol/code hashes bind consistently to the source Git blobs. They do not replace the absent pre-run commit object.
- Available protocol public import commit `3b8b994990da774c8abd0e1c28cbcacae3e9d0be` is 2026-10-25T04:00:56+00:00; receipt import `9aec7d2ecddb542e7a8e08841a1e585591daa2a1` is 2026-10-25T03:55:28+00:00; result import `131157623e2749654d0d35ed5033e23d4e107d18` is 2026-10-25T04:04:21+00:00. All are after the recorded formal run. The local run/result commit is not independently established.
- The pinned source README itself states that public browser-upload history lacks the local pre-run design object. This audit does not bypass that limitation.

## Own receipt and package integrity

**PASS for byte integrity only.** Archive SHA-256 `1ee2f4d848e209b882329f98f5ab0cbe21fe7251b4c9ba9854ac54e7d11b9fa0` and index SHA-256 `d501493ce9fb8d95b1211c813079eb46e08b8be0e76462c560cf92e85c2ec2b0` match the WP3 package receipt. All 206 members match their own indexed sizes and SHA-256 values; no member differences. The five target files below match their own index receipts and identical archive members.

| Target | SHA-256 | own index physical line |
|---|---|---:|
| `results/revision-v9/wp3/contrasts.csv` | `f3a9cbc35cb310a6eb2371e06619638feac4d2add13ba78f68bf8042115bdd86` | 2 |
| `results/revision-v9/wp3/contrasts.json` | `576e9070644e211d417f84efba6a8b77b295be8e1f5870a5ec42aed7d7362ce4` | 3 |
| `results/revision-v9/wp3/curve-predictions.json` | `1568fbe4d43b4f93192d554e99bdf489c130f37dc7e89773d4a063b2f477ffca` | 4 |
| `results/revision-v9/wp3/manifest.json` | `429d866d105469b2c2904adfdb991e9b6c4ff5fc128be3d6980b90d1d59fc61c` | 5 |
| `results/revision-v9/wp3/study-termination.json` | `adad6870f70c14eb4e5ecd965a24bf9e0ef58a18a668ac90173a96270dfbf47c` | 7 |

## Rejected curve inventory — H6 first

The following are verbatim saved values for audit/review, **not recommended import data**. Every row is `COMPLETE`, `n=6625`, but import status is `REJECTED` because the mandatory WP3 gates did not pass. All number locators below use the contrasts JSON hash above; each pointer names its own complete row. The JSON audit additionally binds all 30 F/QR33/QR4 absolute-loss records to archive/member SHA-256 and own receipt rows.

| H | W | QR33 relative loss % | pointer | QR4 relative loss % | pointer | matched F mean loss |
|---:|---:|---:|---|---:|---|---:|
| 6 | 360 | 3.0438186779438983 | `/4` | -0.8754052083818208 | `/5` | 456440.72347869794 |
| 6 | 720 | -2.1167271486370893 | `/8` | 1.4764717411070867 | `/9` | 442615.265176624 |
| 6 | 1440 | -6.5076708350722905 | `/12` | -3.2812108413789005 | `/13` | 444513.0040586647 |
| 6 | 2880 | -14.766762552613883 | `/0` | -4.2893706508927965 | `/1` | 452692.9834478481 |
| 6 | 5760 | -6.440694459797079 | `/16` | -4.891469312713009 | `/17` | 449277.89637071005 |
| 24 | 360 | 24.346452155465645 | `/6` | 16.590207827669552 | `/7` | 814394.7299876912 |
| 24 | 720 | 31.503964246480937 | `/10` | 16.513128710925677 | `/11` | 787415.6197911236 |
| 24 | 1440 | 9.238708964820484 | `/14` | -2.6227375691876738 | `/15` | 753862.8826360594 |
| 24 | 2880 | -3.757769795795826 | `/2` | -2.8936718065277542 | `/3` | 763381.1758251915 |
| 24 | 5760 | 1.8577089031029423 | `/18` | 0.15840259366901976 | `/19` | 758822.4055862104 |

Saved curve statuses preserve H6/QR4 `NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED`; H24 at W5760 reverses to positive relative loss for both QR33 and QR4. Candidate inventory records 80 COMPLETE candidates and no failed candidates. These are source claims supported by saved scalar records; private traces were not reopened or rescored. Package integrity and the earlier independent-audit PASS do not override this audit’s exact-anchor failure.

The experiment remains explicitly post-result and exploratory, with the same 6,625 evaluation origins and no fresh financial holdout. No one-figure/one-paragraph learning-curve import is recommended. Retain the existing v10b findings and record the rejected integration transparently.

Full source/ref/hash/pointer inventory, status distinctions and execution boundaries are in `notes/v11/wp3-import-audit.json`.


## Provenance reconciliation and precision layers (appended)

This addition preserves the initial strict FAIL above. Additional root-supplied read-only Git evidence changes the provenance assessment; it does not change either saved archive or make unequal stored percentages equal.

Proof source: `notes/v11/original-commit-proofs.json`, SHA-256 `eafbb501cc4870e19ef87bc6e108f794e64fd3ceaa3f3040b60f2ddc43ad6152`. This agent independently reconstructed Git commit SHA-1 values from the supplied raw commit bytes: both match their stated identities. Design `b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a` is **2026-10-24T23:13:51+00:00**, before formal start **2026-10-24T23:24:51.666335+00:00**. Result/end commit `bfd0493f4237b6b99ca4370a2e6cf2195f653b28` is **2026-10-24T23:39:27+00:00**, after formal end **2026-10-24T23:35:21.429167+00:00**, and directly names the design commit as parent. The root’s original repository HEAD is unchanged. Time and separate design/result commit existence therefore pass on this supplied evidence. Exact original protocol/result blob content binding remains pending; raw commit times and changed-path lists alone do not establish those file bytes.

The user supplied anchors to two decimal places. At that precision, both comparisons are **exactly identical**: W720 is `-2.12%` and W2880 is `-14.77%`. The full stored percentages remain **binary64 unequal**. The stored means and breach counts are exactly equal, and the old `mean_pinball_difference` field equals the new `dm.mean_difference` at both anchors. These three statements are compatible and are recorded separately.

Static source diagnosis (all code read from pinned `60e03b8`, no code executed):

- `conditional_study.py:274–277`, SHA-256 `aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740`: the original paired archive first obtains `difference=core.stable_mean(left.pinball[mask]-right.pinball[mask])`, then saves `relative=100*(difference/b)`.
- `run_v9_learning_curve.py:177–179`, SHA-256 `9952026f3b95e7f6239b876417c0ff7e74df7146962384edac833ad611352ed4`: v9 separately stores the paired difference for DM, but its curve percentage uses `100*(summary['mean_pinball']-fsummary['mean_pinball'])/fsummary['mean_pinball']`.
- `study_core.py:403–411`, SHA-256 `1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf`: the common `stable_mean` uses the specified `math.fsum(...)/len(values)` (with an exact-constant shortcut). `conditional_study.py:222` binds each stored mean to this function.

Thus the old percentage divides the stable mean of pointwise differences; the new percentage subtracts the separately aggregated means before dividing. These expressions are equivalent over exact real arithmetic and have different floating-point operation paths. The observed discrepancy is localized to that saved percentage path. No ratio, score, summary, HAC or fit was rerun. No tolerance or alternate owning source was used. The initial strict stored-value FAIL remains; any editorial admission under the user’s stated display precision must describe that level accurately and must not claim bitwise identity.

The archive writer confirms the linkage: `build_conditional_results.py:300,307,318–323`, SHA-256 `9f87c689dd20027e223a423f427380cba7179f78565c0cf4fc896274be1776ab`, calls `paired_comparison`, appends its `all` record, and writes it to `results/revision-20261022/paired-comparisons.csv`. The `conditional_study.py` and `study_core.py` bytes are also identical in the v10b base and pinned PR5 source.


## Final reconciliation after original blob proofs (appended)

Root supplied `notes/v11/original-blob-proofs.json`, SHA-256 `126ddc187c93beb656c5c93e8187ed24a98492a16491630dac8c5569c1fa1c33`. Its eight WP3 checks bind the original b266 design JSON/MD and bfd protocol/result files to the pinned PR5 bytes. This audit independently checked every supplied original/source Git blob ID, SHA-256 and length against its previously read pinned-source record: **8/8 PASS**. The original repository HEAD remains unchanged. Together with the raw commit checks above, **design content and pre-run chronology PASS**, and **original result content PASS**. The earlier pending provenance statement is superseded by these additional proofs.

Final layers: **saved percentage full precision/binary64 exact agreement remains FAIL**; **underlying saved mean losses and breach counts are EXACT PASS**; **the two user-provided decimal anchors -2.12% and -14.77% are EXACT PASS at two decimal places**. The initial strict FAIL and `admit_to_v11=false` snapshot remain unchanged for audit history. The root has separately decided to allow static editorial import under the actual user-specified display precision, with the floating-point arithmetic-path discrepancy disclosed. This reconciliation makes no claim of unrounded percentage bitwise identity.

The full 20 unchanged source records, H6 five-window QR33/QR4 records, nine higher-loss rows, longest-window H24 reversals, and all four saved curve classification records are bound with exact JSON pointers in `provenance_reconciliation.final_reconciliation_after_original_blob_proofs`. H6 main-figure source: `results/revision-v9/wp3/contrasts.json`, SHA-256 `576e9070644e211d417f84efba6a8b77b295be8e1f5870a5ec42aed7d7362ce4`.

| W | QR33 relative loss % | exact field pointer | QR4 relative loss % | exact field pointer |
|---:|---:|---|---:|---|
| 360 | 3.0438186779438983 | `/4/relative_loss_percent` | -0.8754052083818208 | `/5/relative_loss_percent` |
| 720 | -2.1167271486370893 | `/8/relative_loss_percent` | 1.4764717411070867 | `/9/relative_loss_percent` |
| 1440 | -6.5076708350722905 | `/12/relative_loss_percent` | -3.2812108413789005 | `/13/relative_loss_percent` |
| 2880 | -14.766762552613883 | `/0/relative_loss_percent` | -4.2893706508927965 | `/1/relative_loss_percent` |
| 5760 | -6.440694459797079 | `/16/relative_loss_percent` | -4.891469312713009 | `/17/relative_loss_percent` |

Preserve adverse results and uncertainty: H6 QR33 W360 is `+3.0438186779438983%` (`/4/relative_loss_percent`), H6 QR4 W720 is `+1.4764717411070867%` (`/9/relative_loss_percent`); H24 at W5760 reverses to `+1.8577089031029423%` (`/18/relative_loss_percent`, QR33) and `+0.15840259366901976%` (`/19/relative_loss_percent`, QR4). All are `COMPLETE`. H6 QR4 remains `NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED`, from `curve-predictions.json#/1/prediction_status` (SHA-256 `1568fbe4d43b4f93192d554e99bdf489c130f37dc7e89773d4a063b2f477ffca`), and the source acceptance `/all_four_numerical_confirmation` is `false`. These are descriptive post-result curves on the same evaluation period, without a fresh holdout or causal history/menu claim.
