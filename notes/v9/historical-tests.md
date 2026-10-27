# C3: version routing for historical document tests

Only two test files required routing. The eight document/table snapshots were extracted from public PR #5 base `0f1f066843e0c49cf3e24bce7d72032dc189603d` using read-only `git show`, with `GIT_OPTIONAL_LOCKS=0`. No source was taken from a private historical commit object, and no Git objects or bundles were exported.

Snapshot directory: `fixtures/v9-baselines/pr5-v8/`. Its manifest SHA-256 at creation is `992be30307880a795f8c521a9aba46b96c0b7c532710ac55597998999d41b741`; eight members total173985bytes. Each has the original public Git blob ID, byte count and SHA-256. The test adapters verify the fixed public source commit and member fingerprints before copying into their existing mutable temporary fixtures.

## Changed routing

| Test file | Old document input | New document input | Preserved behavior |
|---|---|---|---|
| `test_v8_main_numbers.py` | Live `submission-jof/manuscript.tex` and `cover-letter.md` | Exact public-base snapshots of those two files, copied into the same per-test temporary files | All11 original test functions/12 parameterized cases, original checker, ROOT evidence lookup, old Git/source/figure guards and every original assertion remain. |
| `notes/revision-v8/test_v8_supp_numbers.py` | Live Supplement and five generated v8 table files | Exact public-base snapshots of those six files, copied into the same temporary document tree | All8 original cases, `checker.audit(ROOT,self.docs)`, original source/evidence/Git guards and every assertion remain. |

The scientific checkers themselves were not modified. The changes are test docstrings, a fingerprint-checked snapshot path helper, and the two old fixture-copy routes. None of the cases was skipped, marked xfail, deleted or relaxed. A static AST comparison against the public-base test files confirmed that all19 original `test_*` function bodies remain identical; the only extra test count is the already-existing two-value probability parameterization, for20 historical cases total.

## Every retained main-document case

These names are intentionally retained for test-history continuity. In this historical test module, “current” means the frozen PR #5 v8 document copied into the test's temporary tree, not the v9 draft.

| Case | Unchanged check |
|---|---|
| `test_actual_current_main_has_no_unlocated_numeric_result` | The frozen main/letter pass the old located-value audit with zero unclassified/ambiguous occurrences and the original1205 evidence fields. |
| `test_wrong_paired_table_count_is_not_global_value_membership` | Swapping376/360 is rejected by the original row-sequence check. |
| `test_changed_prose_percentage_fails_saved_field_display_check` | Replacing12.2% with21.2% fails the original saved-field display check. |
| `test_wrong_new_breach_count_does_not_pass_equal_value_elsewhere` | Swapping416/282 fails the original context binding. |
| `test_unbound_inline_math_probability_is_not_structural_escape` | Both existing0.123 and0.055 parameterized additions remain rejected as unbound results. |
| `test_unbound_new_numeric_prose_is_reported` | The added987.654 result remains unbound. |
| `test_modified_accepted_math_constant_is_not_blanket_classified` | Changing19/20 to19/21 is still rejected. |
| `test_unbound_new_cover_letter_result_is_not_outside_checker` | A newly added42.7-percent cover-letter claim is still rejected. |
| `test_new_number_word_claim_is_not_silently_ignored` | Changing three examined windows to four remains an unbound word claim. |
| `test_false_global_pass_for_external_reference_or_figure_gates_is_forbidden` | The old checker still explicitly declines full figure/reference/artifact acceptance. |
| `test_deleted_unfavorable_table_row_cannot_pass_remaining_number_checks` | Deleting the adverse matched-comparison row still fails the preserved-table check. |

## Every retained Supplement case

| Case | Unchanged check |
|---|---|
| `test_current_document_has_no_numeric_residuals` | Frozen Supplement and five table inputs retain the original PASS_WITH_SCOPE_LIMITS, with no failures/unresolved/ambiguous occurrences. |
| `test_swapped_mc_rows_fail_ordered_identity_binding` | Swapped source-identified Monte Carlo rows are still rejected. |
| `test_wrong_master_entropy_is_rejected_exactly` | Changing2026102408 to2026102409 still fails exact passage binding. |
| `test_unbound_inline_p_is_not_classified_as_math` | An added p=0.055 remains unresolved/NEEDS_REVIEW. |
| `test_unbound_result_beside_layout_command_is_not_exempt` | A numeric result adjoining an includegraphics command remains unresolved. |
| `test_omitted_generated_table_is_rejected` | Removing the daily-results table still fails the required-input gate. |
| `test_changed_old_numeric_row_is_rejected` | Changing156123.03 to156123.04 still fails old ordered-row preservation. |
| `test_numeric_native_types_are_not_coerced` | Boolean/integer and integer/float distinctions remain exact. |

## Reviewed files that did not need changes

- `notes/revision-v8/test_review_package_reports.py` already creates an entirely invented temporary submission tree, copies the unchanged packager there, and checks its real routing/hash/status behavior. It never requires the live v9 paper to retain v8 prose. All seven cases were left unchanged.
- `test_v8_wp3_package.py` already creates small artificial archive inputs and tests the public packaging/integrity boundaries. It does not read the live manuscript/Supplement. All15 cases were left unchanged.
- `test_v6_submission.py` composes retained v5/v6 document snapshots and only fingerprints the live content aliases to prove its read-only operation. It does not assert that the live v9 prose equals v6 prose; no routing change was needed.
- `test_v8_figure_numbers.py` audits the original archived WP3 summary/design/display receipts. Those scientific inputs remain frozen, so no routing change was needed.
- Earlier figure/inventory/composition tests already target their named historical inputs or constructed fixtures. No general test tool, source guard, scientific code, protocol, result, figure or actual submission document was changed by this task.

## Private historical-object dependency remains explicit

The original local acceptance environment retains five exact historical commits:

- WP3 design `039f6f1b49d46610697bed5300cab687b37951df`;
- WP4 design `1427dc0b943ee77a82ee03a67ec9281c20e2cdf5`;
- WP5 design `467a995b16a1c6446b5927992faec26b7f5f6276`;
- numeric-proof baseline `b571f324a253480b4e39bc8a8096775ddbcc7017`;
- pre-integration baseline `642d6af9eaccdd27896fd7a2e265cddd6f7a91e5`.

The two historical numeric checkers directly use the last two objects; the three sealed financial drivers retain the first three design guards. This routing task neither changes nor removes any of those dependencies. The browser-created public Git history does not supply those objects, and the new public text fixtures are not a substitute for them. They contain private machine-local identity metadata in the original commit objects; this task does not publish those objects, invent ancestry, supply a bundle or weaken an identity check. C6/C7 must not claim that the original entire validation environment is dependency-free or fully reproduced by a fresh public clone.

The main historical checker continues checking protected old `submission-jof/figures/` paths. Root agreed that new v9 figures will use new filenames and that the existing v7/v8 assets/bindings will remain unchanged. This preserves those source guards rather than making them accept altered figure bytes.

## Verification and v9 acceptance boundary

Before the snapshot payloads were created, the newly routed historical cases failed at the explicit missing-fixture boundary:8 failed and12 fixture-setup errors in0.08s. The complete output is retained in `.scratch/v9/historical-doc-routing-red.txt`. This is an expected pre-fixture dependency failure, not a scientific failure.

After extraction, the two routed modules and the two unchanged packaging modules were run together: **42 passed,2 subtests passed in16.64s**, exit0. The owning output is `.scratch/v9/historical-doc-routing-green.txt`. The test set was `test_v8_main_numbers.py notes/revision-v8/test_v8_supp_numbers.py notes/revision-v8/test_review_package_reports.py test_v8_wp3_package.py`, with the existing cached uv environment, numerical threads1, `python -B -m pytest -q -p no:cacheprovider --tb=short`. The only wrapper warning was uv's no-project message.

These are historical software/negative-control checks. Passing them does not certify new v9 manuscript numbers, prose, figures, layout or submission package. Root will add separate v9 current-document checks after promoting the approved draft. No old result is silently reclassified as v9 acceptance.
