# Revision v4 — Journal of Forecasting

Plan: revision-plan-v4-jof.md (user supplied). Local branch revision-v4-jof; based on v3 HEAD8ec42dc and required merge of origin/main65feeee. No system installation, journal submission, account registration or signed author disclosure is authorized. Existing scientific values, two primaries and adverse/NA results stay fixed.

## Step0 — main synchronization and scientific corrections (in progress)

Actual command:
```sh
git fetch origin
```
Tool combined output: empty; returncode0.

Actual subsequent commands:
```sh
git log -4 --format='%h %s' origin/main
git switch -c revision-v4-jof revision-v3-readability
git merge --no-edit origin/main
```
Actual combined tool output:
```text
65feeee Merge pull request #2 from ByronLi0207/codex/critical-review-20261023
ec29c06 Verify the existing annual aggregate decomposition
1611d5c Correct the scientific scope in the verified paper
c1563ab Clarify the retrospective benchmark and document critical corrections
Switched to a new branch 'revision-v4-jof'
Merge made by the 'ort' strategy.
 README.md                                          | 167 ++---
 REVIEW_20261023.md                                 |  72 +++
 manuscript/working-paper/README.md                 |  55 +-
 manuscript/working-paper/main.tex                  | 162 +++--
 manuscript/working-paper/paper-content.json        | 180 +++---
 manuscript/working-paper/paper.pdf                 | Bin 226059 -> 220510 bytes
 manuscript/working-paper/references.bib            |  18 +-
 .../working-paper/rendering-verification.json      | 120 ++--
 notes/revision-20261023/annual-decomposition.json  | 685 +++++++++++++++++++++
 notes/revision-20261023/annual-decomposition.py    | 166 +++++
 10 files changed, 1223 insertions(+), 402 deletions(-)
 create mode 100644 REVIEW_20261023.md
 create mode 100644 notes/revision-20261023/annual-decomposition.json
 create mode 100644 notes/revision-20261023/annual-decomposition.py
```

Merge result is f8016faac7a04945d3f03c6cc0700acea20646a9 with parents8ec42dc and65feeee. No conflict; working-paper tree follows origin/main. The pre-merge v3 root guide is retained in notes/revision-v4-jof/readme-v3-before-merge.md and will be linked alongside the main guide.

Ruling: user explicitly requires this checkout and new branch, so no additional worktree or setup installation is created. The user has supplied the detailed plan; it is the task authority. Unclear author decisions are deferred rather than asked. The merge, eventual named-branch push/PR and recoverable Trash moves are explicitly authorized by this new plan and supersede the previous v3 no-push/no-cleanup scope. No filesystem deletion is used.

Ruling: PDF creation will use the existing ReportLab route and native desktop LaTeX compiler without installing any engine. PR2 expressly records native compiler diagnostics with a separately typeset PDF, so successful diagnostics will not be mislabeled as an exported compiled PDF. Final v4 source cannot be compiled before its SectionIII authoring; actual compilation follows in SectionIV.


## Step0 scientific adoption — completed

| Correction | Disposition and exact destination |
|---|---|
| FR2004A trade-date/fair-value, eligible forward/when-issued and buyback exception | Adopted in manuscript Data; generic framework reference replaced with the consulted2013/2024 versions; no data values changed. |
| Economic date versus historical release | v3 already covered the central limitation; moved precise public clock into Data and retained it in the abstract. The downloaded vintage is not called an as-released backtest. |
| Finite eight-report menu / floor-only | Adopted in RQ2 and Supplement S6; endpoint winners apply only within the menu. No new report or numerical frontier was estimated. |
| Mean errors / headroom | Adopted once in Evaluation; U/V average all origins and reported headroom is distinct; legacy result field names remain unchanged. |
| Linear preferences / FOSD / consistent-score class | v3 Murphy crossings already covered the score-class boundary; adopted zero-point empirical-FOSD argument and weak/strict constant-linear-weight qualification. Artificial REVIEW score example is inapplicable as new financial evidence and was not inserted. |
| Arbitrary residual algebra | Adopted in Supplement S2/S7, preserving v3 symbols and formulas; no assumed true AR law or martingale-difference property. |
| Numerical acceptance | Adopted unconstrained affine prediction, frozen initialization and objective-gap limits in Methods/S4. Binary-quantile qualification retained; no optimizer change or refit. |
| Annual decomposition | Adopted H6/H24 contrast and replayed the exact archived decimal-token helper. Output JSON is identical to the merged receipt; rational arithmetic does not recover infinite-precision individual losses. |
| Liao deletion | Inapplicable: v3 actually cites it. The citation is retained, with official author metadata correction. |
| Main guide conflict | No merge conflict; the main guide and exact pre-merge v3 guide are both retained and linked. |

Actual command:
```sh
python3 -B v4_scientific_port.py
```
Actual output:
```text
Scientific port saved; source manuscripts unchanged; two primary definitions and all v3 tables retained.
```

## II — official journal requirements

Completed by reading the official Wiley author, data-sharing and ethics pages. Actual source access interval and URLs are in submission-jof/journal-requirements.md. Single-blind; Free Format; up to six keywords; running title under40 characters. No published body/abstract numerical cap or JEL/highlights requirement was found. The9000-word/six-table/four-figure target is this project's choice, not a journal rule. Detailed AI guidance returned403; accessible current ethics requirements are recorded without authoring the personal disclosure. No reason to switch journal.

## III — article restructuring and complete supplementary archive

New v4 source uses three research questions; includes a method overview, a joint score/DM/HLN/Holm/breach/Kupiec table generated by unique CSV selectors, and grayscale vector figures. Original scientific files are read-only. The37 original tables occur once each across the outputs with exact headers/rows; new main tables are qualitative overview and combined archived results. The two original primaries, all adverse cells and six NA outcomes remain. All original appendices and detailed robustness tables are routed to named S-sections. Transparency is centralized, with a dagger marking later additions. Earlier material is not retrospectively labeled preregistered or post-result solely because it moved.

Reference audit:40 evidence dispositions with primary links; bibliography corrections affect metadata only. Unverified specific dates/professional degree or disputed pagination are omitted rather than invented. Main retains36 cited items; Supplement retains9; union bibliography40. Kaggle current metadata does not establish raw-redistribution permission. NYFed permitted reuse retains attribution/terms. No new raw observations were downloaded. Source-code URL stays real under verified single-blind review. Personal statements remain author placeholders.

Actual authoring/readback commands:
```sh
python3 -B v4_submission.py
python3 -B v4_figures.py
python3 -B v4_typeset.py
python3 -B v4_numeric.py
python3 -B notes/revision-20261023/annual-decomposition.py --output .scratch/v4-jof/annual-replay.json
```
Actual figures output:
```text
Five grayscale vector figures; original source bytes untouched.
```
An initial optional matplotlib import failed (ModuleNotFoundError); nothing was installed. It was replaced by the existing ReportLab vector drawing route. The initial missing-module red test of v4_numeric was intentional; context-sensitive corruption and substitution tests then passed. This is recorded as an implementation failure/recovery, not a scientific experiment.

## IV — verification

Numerical checker binds each retained block to a hashed, immutable archived JSON context and regenerates the new table directly from named CSV rows/fields. It validates the rendered TeX against that source-bound rendering, includes equations, figure captions and verified bibliography dispositions, and classifies structural/layout and bibliographic digits separately. It is an archive-consistency check, not an independent raw-data replication; it does not treat a bag of globally present numbers as evidence. The regression test substitutes another number that exists elsewhere in the archive and requires failure.

Actual latest v4_typeset output (metrics):
```json
{
  "manuscript": {
    "pages": 14,
    "prose_words_excluding_abstract_references_tables_captions": 5322,
    "abstract_words": 210,
    "main_tables": 4,
    "figures": 4
  },
  "supplement": {
    "pages": 30,
    "prose_words_excluding_abstract_references_tables_captions": 7061,
    "abstract_words": 0,
    "main_tables": 35,
    "figures": 5
  }
}
```

Actual latest numerical-check output:
```json
{
  "status": "PASS",
  "scope": "All numeric tokens in manuscript.tex and supplement.tex; exact per-block source contexts and generated CSV row/field selectors. Archived consistency only, not independent data replication.",
  "documents": {
    "manuscript": {
      "tex_numeric_token_count": 983,
      "archived_or_synthesis_tokens": 578,
      "bibliographic_tokens": 215,
      "mismatch_count": 0
    },
    "supplement": {
      "tex_numeric_token_count": 4119,
      "archived_or_synthesis_tokens": 3740,
      "bibliographic_tokens": 71,
      "mismatch_count": 0
    }
  },
  "mismatches": [],
  "matched_numeric_tokens": 5102,
  "empirical_or_archived_claim_tokens": 4318,
  "structural_template_tokens": 498,
  "bibliographic_tokens": 286
}
```

Native compiler tool results (current sources; diagnostic success does not export a PDF):
```json
{
  "manuscript": {
    "content": [
      {
        "type": "text",
        "text": "{\"path\":\"/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript.tex\",\"mainDocument\":\"/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript.tex\",\"kind\":\"success\",\"message\":\"The current source compiled successfully with the desktop editor's compiler.\"}"
      }
    ],
    "isError": false
  },
  "supplement": {
    "content": [
      {
        "type": "text",
        "text": "{\"path\":\"/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement.tex\",\"mainDocument\":\"/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement.tex\",\"kind\":\"success\",\"message\":\"The current source compiled successfully with the desktop editor's compiler.\"}"
      }
    ],
    "isError": false
  },
  "title_page": {
    "content": [
      {
        "type": "text",
        "text": "{\"path\":\"/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/title-page.tex\",\"mainDocument\":\"/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/title-page.tex\",\"kind\":\"success\",\"message\":\"The current source compiled successfully with the desktop editor's compiler.\"}"
      }
    ],
    "isError": false
  }
}
```

Actual selected-suite invocation and resource measurement:
```json
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--no-project",
    "--no-env-file",
    "--python",
    "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "--with",
    "pytest",
    "--with",
    "arch",
    "--with",
    "scikit-learn",
    "python",
    "-B",
    "-m",
    "pytest",
    "-p",
    "no:cacheprovider",
    "-v",
    "test_inference_tests.py",
    "test_parsimonious_v3.py",
    "test_v3_math_format.py",
    "test_v3_inference_presentation.py",
    "test_v3_student_reference.py",
    "test_v3_write_policy.py",
    "test_round2_shrinkage.py",
    "test_round2_levy.py",
    "test_round2_panel.py",
    "test_v3_round2_consistency.py",
    "test_round2_qrf.py",
    "test_round2_filtered.py",
    "test_round2_baseline_worker.py",
    "test_round2_baseline_readback.py",
    "test_round2_levy_ar_correction.py",
    "test_reproducibility_guide.py",
    "test_v4_numeric.py"
  ],
  "exit_code": 0,
  "elapsed_seconds": 4.34162712097168,
  "child_maxrss_bytes": 229343232,
  "scope": "17 explicitly selected modules; no claim of all historical tests. Old cleanup/deletion fixtures excluded."
}
```

Actual complete stdout/stderr:
```text
============================= test session starts ==============================
platform darwin -- Python 3.12.14, pytest-9.1.1, pluggy-1.7.0 -- /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/uv-d1-cache/builds-v0/.tmpSJWVa7/bin/python
rootdir: /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023
collecting ... collected 130 items

test_inference_tests.py::KnownAnswers::test_bad_inputs PASSED            [  0%]
test_inference_tests.py::KnownAnswers::test_chi_square_six_known PASSED  [  1%]
test_inference_tests.py::KnownAnswers::test_christoffersen_known PASSED  [  2%]
test_inference_tests.py::KnownAnswers::test_dm_horizon_two_known PASSED  [  3%]
test_inference_tests.py::KnownAnswers::test_dm_known_bartlett_and_hln PASSED [  3%]
test_inference_tests.py::KnownAnswers::test_dm_sign_and_degenerate PASSED [  4%]
test_inference_tests.py::KnownAnswers::test_dq_unidentified_hits PASSED  [  5%]
test_inference_tests.py::KnownAnswers::test_holm_known_and_order PASSED  [  6%]
test_inference_tests.py::KnownAnswers::test_kupiec_known PASSED          [  6%]
test_inference_tests.py::KnownAnswers::test_murphy_crossing_and_integral PASSED [  7%]
test_inference_tests.py::KnownAnswers::test_student_against_closed_forms PASSED [  8%]
test_parsimonious_v3.py::CausalFourFeatures::test_current_and_rms_known PASSED [  9%]
test_parsimonious_v3.py::CausalFourFeatures::test_future_changes_do_not_change_issued_features PASSED [ 10%]
test_parsimonious_v3.py::CausalFourFeatures::test_training_transform_constant_and_causal PASSED [ 10%]
test_v3_math_format.py::MathematicalTypesetting::test_absolute_value_is_not_norm PASSED [ 11%]
test_v3_math_format.py::MathematicalTypesetting::test_adjacent_variance_word_does_not_block_the_complete_formula PASSED [ 12%]
test_v3_math_format.py::MathematicalTypesetting::test_canonical_positive_parts_and_equal_window_binding PASSED [ 13%]
test_v3_math_format.py::MathematicalTypesetting::test_catalog_does_not_bind_inside_larger_identifiers PASSED [ 13%]
test_v3_math_format.py::MathematicalTypesetting::test_current_source_preserves_input_and_idempotence PASSED [ 14%]
test_v3_math_format.py::MathematicalTypesetting::test_figure_caption_uses_whole_formula_binding PASSED [ 15%]
test_v3_math_format.py::MathematicalTypesetting::test_full_inline_formula_is_single_math_span PASSED [ 16%]
test_v3_math_format.py::MathematicalTypesetting::test_long_inline_formulas_and_caption_are_whole_math PASSED [ 16%]
test_v3_math_format.py::MathematicalTypesetting::test_membership_does_not_consume_english_phi PASSED [ 17%]
test_v3_math_format.py::MathematicalTypesetting::test_notation_cells_use_whole_tex_expressions PASSED [ 18%]
test_v3_math_format.py::MathematicalTypesetting::test_recovered_parameterization_has_real_symbols PASSED [ 19%]
test_v3_math_format.py::MathematicalTypesetting::test_round2_table_norm_and_persistence_delta_are_whole_math PASSED [ 20%]
test_v3_math_format.py::MathematicalTypesetting::test_simple_numeric_reports_are_full_math_spans PASSED [ 20%]
test_v3_inference_presentation.py::FamilyReadback::test_existing_and_doubled_reference_counts PASSED [ 21%]
test_v3_inference_presentation.py::FamilyReadback::test_identical_forecasts_are_conservative_bookkeeping PASSED [ 22%]
test_v3_inference_presentation.py::FamilyReadback::test_mismatched_archived_adjustment_fails PASSED [ 23%]
test_v3_inference_presentation.py::FamilyReadback::test_rejection_counts_preserve_adverse_directions PASSED [ 23%]
test_v3_student_reference.py::IndependentStudentReference::test_closed_cauchy_and_t2_answers PASSED [ 24%]
test_v3_student_reference.py::IndependentStudentReference::test_domain_is_bounded_to_audit_scope PASSED [ 25%]
test_v3_student_reference.py::IndependentStudentReference::test_scalar_rows_and_mismatch PASSED [ 26%]
test_v3_write_policy.py::WriteOwnership::test_backup_policy PASSED       [ 26%]
test_v3_write_policy.py::WriteOwnership::test_new_owned_file_rewrites_without_backup PASSED [ 27%]
test_round2_shrinkage.py::ShrinkageDiagnostics::test_overlap_counts_not_ordinary_accuracy PASSED [ 28%]
test_round2_shrinkage.py::ShrinkageDiagnostics::test_projection_is_not_unprojected_contribution PASSED [ 29%]
test_round2_shrinkage.py::ShrinkageDiagnostics::test_zero_slope_and_constant_correlation PASSED [ 30%]
test_round2_shrinkage.py::ManuscriptCells::test_round2_table_cells_are_formal_converter_strings PASSED [ 30%]
test_round2_levy.py::LevyBaseline::test_discrete_population_quantile_triangle_corollary PASSED [ 31%]
test_round2_levy.py::LevyBaseline::test_exact_independent_symmetric_maximal_inequality PASSED [ 32%]
test_round2_levy.py::LevyBaseline::test_exact_mature_endpoint_pool PASSED [ 33%]
test_round2_levy.py::LevyBaseline::test_future_perturbation_and_truncation PASSED [ 33%]
test_round2_levy.py::LevyBaseline::test_rank_and_gaussian_variance PASSED [ 34%]
test_round2_levy.py::IndependenceBoundary::test_symmetric_but_dependent_counterexample PASSED [ 35%]
test_round2_panel.py::PanelAlignment::test_duplicate_wrong_key_and_nonfinite_rejected PASSED [ 36%]
test_round2_panel.py::PanelAlignment::test_exact_grid_truncates_only_extra_dates PASSED [ 36%]
test_round2_panel.py::PanelAlignment::test_no_imputation_of_missing_date PASSED [ 37%]
test_round2_panel.py::PanelFitting::test_common_strict_menu_rejects_failure PASSED [ 38%]
test_round2_panel.py::PanelFitting::test_future_perturbation_preserves_both_issued_fits PASSED [ 39%]
test_v3_round2_consistency.py::Round2ContentAudit::test_D2_new_formulas_are_whole_TeX_math_spans PASSED [ 40%]
test_v3_round2_consistency.py::Round2ContentAudit::test_conclusion_count_includes_every_paragraph PASSED [ 40%]
test_v3_round2_consistency.py::Round2ContentAudit::test_original_primaries_and_all_holm_rows_retained PASSED [ 41%]
test_round2_qrf.py::test_all_original_leaf_weights_are_not_quantiles_of_tree_means PASSED [ 42%]
test_round2_qrf.py::test_leaf_distribution_does_not_replace_original_rows_by_bootstrap_counts PASSED [ 43%]
test_round2_qrf.py::test_duplicate_responses_and_zero_mass_use_cdf_left_inverse_without_interpolation PASSED [ 43%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values0-weights0-0.95] PASSED [ 44%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values1-weights1-0.95] PASSED [ 45%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values2-weights2-0.95] PASSED [ 46%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values3-weights3-0.95] PASSED [ 46%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values4-weights4-0.95] PASSED [ 47%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values5-weights5-0.95] PASSED [ 48%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values6-weights6-0.0] PASSED [ 49%]
test_round2_qrf.py::test_invalid_weighted_distribution_fails_without_inventing_a_quantile[values7-weights7-True] PASSED [ 50%]
test_round2_qrf.py::test_invalid_or_unoccupied_query_leaf_is_rejected PASSED [ 50%]
test_round2_qrf.py::test_constant_headroom_returns_current_floor_and_retains_mature_fit_receipt[0.0] PASSED [ 51%]
test_round2_qrf.py::test_constant_headroom_returns_current_floor_and_retains_mature_fit_receipt[-12.5] PASSED [ 52%]
test_round2_qrf.py::test_known_linear_path_has_exact_nonnegative_headroom_six PASSED [ 53%]
test_round2_qrf.py::test_full_future_perturbation_cannot_change_reports_or_fit_fingerprints PASSED [ 53%]
test_round2_qrf.py::test_fixed_forest_seed_gives_identical_reports_and_fit_receipts PASSED [ 54%]
test_round2_qrf.py::test_checkpoint_failure_retains_only_issued_prefix_and_no_fallback PASSED [ 55%]
test_round2_qrf.py::test_noncontiguous_origins_and_unavailable_training_features_fail_with_context PASSED [ 56%]
test_round2_qrf.py::test_failed_forest_fit_retains_attempted_mature_pool_instead_of_a_fake_report PASSED [ 56%]
test_round2_filtered.py::test_manual_variance_recursion PASSED           [ 57%]
test_round2_filtered.py::test_simulated_peak_is_path_maximum_at_signed_anchor_and_includes_h0 PASSED [ 58%]
test_round2_filtered.py::test_corrected_quantile_rank_and_unavailable_rank PASSED [ 59%]
test_round2_filtered.py::test_strict_pot_threshold_ties_and_structural_small_window PASSED [ 60%]
test_round2_filtered.py::test_gpd_exponential_limit_and_support_gate PASSED [ 60%]
test_round2_filtered.py::test_one_pot_fit_retains_optimizer_and_finite_tail PASSED [ 61%]
test_round2_filtered.py::test_real_garch_future_perturbation_and_frozen_issue_state PASSED [ 62%]
test_round2_filtered.py::test_nonfinite_source_fails_and_w52_is_rejected_before_filter_fit PASSED [ 63%]
test_round2_filtered.py::test_peak_pot_full_future_perturbation PASSED   [ 63%]
test_round2_filtered.py::test_failed_garch_retains_training_bounds_without_shortening_cell PASSED [ 64%]
test_round2_filtered.py::test_future_change_inside_refit_block_preserves_earlier_issues[FHS] PASSED [ 65%]
test_round2_filtered.py::test_future_change_inside_refit_block_preserves_earlier_issues[PEAK_POT] PASSED [ 66%]
test_round2_filtered.py::test_unobserved_nan_nat_and_absent_outcomes_cannot_affect_reports[FHS] PASSED [ 66%]
test_round2_filtered.py::test_unobserved_nan_nat_and_absent_outcomes_cannot_affect_reports[PEAK_POT] PASSED [ 67%]
test_round2_filtered.py::test_interrupted_filter_preserves_attempted_mature_pool_without_retry[TimeoutError] PASSED [ 68%]
test_round2_filtered.py::test_interrupted_filter_preserves_attempted_mature_pool_without_retry[MemoryError] PASSED [ 69%]
test_round2_filtered.py::test_interrupted_arch_fit_keeps_actual_warning_and_original_exception_code[TimeoutError] PASSED [ 70%]
test_round2_filtered.py::test_interrupted_arch_fit_keeps_actual_warning_and_original_exception_code[MemoryError] PASSED [ 70%]
test_round2_baseline_worker.py::test_comparison_retains_dm_status_once_and_identical_losses_are_not_failed_cells PASSED [ 71%]
test_round2_baseline_worker.py::test_comparison_loss_direction_and_reference_hits_match_inputs PASSED [ 72%]
test_round2_baseline_worker.py::test_qrf_checkpoint_adapter_calls_strict_guard_without_diagnostic_keywords PASSED [ 73%]
test_round2_baseline_worker.py::test_successful_worker_saves_complete_cell_and_both_comparisons PASSED [ 73%]
test_round2_baseline_worker.py::test_resource_failure_keeps_visible_reason_and_no_scored_cell PASSED [ 74%]
test_round2_baseline_worker.py::test_setup_failure_yields_retained_NA_receipt_without_partial_average PASSED [ 75%]
test_round2_baseline_worker.py::test_nonfinite_failed_optimizer_diagnostics_are_explicit_nulls_not_numbers PASSED [ 76%]
test_round2_baseline_readback.py::test_scalar_bartlett_known_alternating_loss_difference PASSED [ 76%]
test_round2_baseline_readback.py::test_successful_optimizer_rejected_only_by_frozen_persistence_gate_is_not_nonconvergence PASSED [ 77%]
test_round2_baseline_readback.py::test_structural_POT_NA_and_complete_record_are_separate PASSED [ 78%]
test_round2_levy_ar_correction.py::test_level_difference_covariance_by_independent_matrix_construction PASSED [ 79%]
test_round2_levy_ar_correction.py::test_endpoint_variances_and_nonzero_conditional_mean PASSED [ 80%]
test_round2_levy_ar_correction.py::test_folded_normal_quantiles_and_degenerate_distribution PASSED [ 80%]
test_round2_levy_ar_correction.py::test_level_recursion_includes_initial_position_and_sign_mirror PASSED [ 81%]
test_round2_levy_ar_correction.py::test_negative_increment_ar_is_not_level_mean_reversion PASSED [ 82%]
test_round2_levy_ar_correction.py::test_strict_breach_endpoint_difference_and_h0_floor PASSED [ 83%]
test_round2_levy_ar_correction.py::test_fixed_seed_is_batch_invariant_for_random_levels_and_negative_increments PASSED [ 83%]
test_round2_levy_ar_correction.py::test_fixed_start_oracles_share_paths_and_have_distinct_information_labels PASSED [ 84%]
test_round2_levy_ar_correction.py::test_invalid_level_parameters_fail[args0] PASSED [ 85%]
test_round2_levy_ar_correction.py::test_invalid_level_parameters_fail[args1] PASSED [ 86%]
test_round2_levy_ar_correction.py::test_invalid_level_parameters_fail[args2] PASSED [ 86%]
test_round2_levy_ar_correction.py::test_invalid_level_parameters_fail[args3] PASSED [ 87%]
test_round2_levy_ar_correction.py::test_invalid_quantile_parameters_fail[0.0-0.0-1.0] PASSED [ 88%]
test_round2_levy_ar_correction.py::test_invalid_quantile_parameters_fail[1.0-0.0-1.0] PASSED [ 89%]
test_round2_levy_ar_correction.py::test_invalid_quantile_parameters_fail[0.975-nan-1.0] PASSED [ 90%]
test_round2_levy_ar_correction.py::test_invalid_quantile_parameters_fail[0.975-0.0--1.0] PASSED [ 90%]
test_reproducibility_guide.py::RebuildGuideTests::test_empty_migration_and_same_content_rebuild_are_idempotent PASSED [ 91%]
test_reproducibility_guide.py::RebuildGuideTests::test_existing_region_update_preserves_both_manual_sides PASSED [ 92%]
test_reproducibility_guide.py::RebuildGuideTests::test_file_input_preserves_crlf_outside_the_generated_region PASSED [ 93%]
test_reproducibility_guide.py::RebuildGuideTests::test_legacy_migration_preserves_indented_manual_headings 
test_reproducibility_guide.py::RebuildGuideTests::test_legacy_migration_preserves_indented_manual_headings PASSED [ 93%]
test_reproducibility_guide.py::RebuildGuideTests::test_legacy_migration_preserves_unknown_sections_verbatim PASSED [ 94%]
test_reproducibility_guide.py::RebuildGuideTests::test_malformed_or_duplicate_reserved_markers_fail_closed 
test_reproducibility_guide.py::RebuildGuideTests::test_malformed_or_duplicate_reserved_markers_fail_closed PASSED [ 95%]
test_reproducibility_guide.py::RebuildGuideTests::test_unknown_nonempty_legacy_header_fails_closed 
test_reproducibility_guide.py::RebuildGuideTests::test_unknown_nonempty_legacy_header_fails_closed PASSED [ 96%]
test_v4_numeric.py::test_archive_block_accepts_unchanged_science PASSED  [ 96%]
test_v4_numeric.py::test_wrong_context_value_fails_even_when_it_exists_elsewhere PASSED [ 97%]
test_v4_numeric.py::test_joint_table_regenerates_all_contextual_cells PASSED [ 98%]
test_v4_numeric.py::test_missing_provenance_is_not_silently_accepted PASSED [ 99%]
test_v4_numeric.py::test_definition_cannot_hide_empirical_numbers PASSED [100%]

=================== 130 passed, 15 subtests passed in 3.79s ====================
WARN `--no-project` was provided, but no project was found
```

Historical cleanup/deletion fixtures were excluded under the no-delete rule; no claim that the entire historical repository test suite ran. Domain tests and five new numerical-source tests were included. Models were not refitted. Subprocess resource measurement applies to this test run, not the native compiler.

Every main/Supplement page was rendered. Actual image inspection found and fixed separated table captions, a split range cell and orphan supplementary heading. Current PNG/hash receipts and the independent same-model visual report record the observed resolution and boundaries. No Claude/Cloud call was used. Main preview14 pages including references/captions, Supplement30; title page1. Formal source diagnostics succeeded; delivered PDFs are separately typeset ReportLab previews.

Readability lexical counts (not a quality or scientific-validity metric; no adverse result was softened to optimize this statistic):
```json
{
  "definition": "Lexical English no/not/never/neither/without/cannot contractions; paragraph prose only; not a scientific-quality metric",
  "counts": {
    "v3": {
      "sentences": 308,
      "negative_sentences": 30,
      "ratio": 0.09740259740259741
    },
    "v4_main": {
      "sentences": 347,
      "negative_sentences": 44,
      "ratio": 0.12680115273775217
    }
  }
}
```

## V — preparation package

Actual command:
```sh
python3 -B v4_package.py
```
Actual output:
```text
Author placeholders, cover letter, union bibliography, complete relative-asset ZIP and title preview created.
```
The ZIP integrity/relative-asset readback passed:11 files, three targets, no missing graphic assets or absolute local font requirement. No highlights file is generated because it was not required by the retrieved guidelines. This is a preparation package; author completion, formal PDF export/inspection and actual submission remain personal tasks.

## VI — branch publication and recoverable cleanup (in progress)

Actual fetch before publication returned origin/main65feeee801b6b228a608ca3200e0678bb5f62b1c; local main remains cbce3986276e994add53b0f5c6bdeec5191f4412. All1284 protected tracked files after the required merge remain byte-identical, except the explicitly authorized root README addition. FINAL.md and both prior manuscripts are unchanged.

### VI actual outcome — local work complete; authenticated publication pending

The separate backup-index removal commit is f3a4b80; actual git-rm output/commit stdout are in backup-index-removal.json. All12 local copies were retained. The package commit is3a6a0797d4fa5114cd09c9d54ba0842e6aa77d4f.

Actual preflight output:
```json
{
  "status": "PASS",
  "tracked_file_count": 1340,
  "staged_paths": [
    "README.md",
    "REVISION_V4_CHANGELOG.md",
    "notes/revision-v4-jof/backup-index-removal.json",
    "notes/revision-v4-jof/data-policy-audit.md",
    "notes/revision-v4-jof/document-metrics.json",
    "notes/revision-v4-jof/figure-bindings.json",
    "notes/revision-v4-jof/final-document-bindings.json",
    "notes/revision-v4-jof/main-title-visual-review.md",
    "notes/revision-v4-jof/native-compiler-results.json",
    "notes/revision-v4-jof/numeric-final-pass.txt",
    "notes/revision-v4-jof/numeric-first-pass.txt",
    "notes/revision-v4-jof/numeric-validation.json",
    "notes/revision-v4-jof/overleaf-manifest.json",
    "notes/revision-v4-jof/pdf-geometry.json",
    "notes/revision-v4-jof/pytest-final-full-output.txt",
    "notes/revision-v4-jof/pytest-final-invocation.json",
    "notes/revision-v4-jof/pytest-full-output.txt",
    "notes/revision-v4-jof/pytest-invocation.json",
    "notes/revision-v4-jof/pytest-release-full-output.txt",
    "notes/revision-v4-jof/pytest-release-invocation.json",
    "notes/revision-v4-jof/readability-counts.json",
    "notes/revision-v4-jof/readme-v3-before-merge.md",
    "notes/revision-v4-jof/reference-audit.json",
    "notes/revision-v4-jof/reference-audit.md",
    "notes/revision-v4-jof/rendered-page-hashes.json",
    "notes/revision-v4-jof/routing.json",
    "notes/revision-v4-jof/scientific-port.json",
    "notes/revision-v4-jof/state.json",
    "notes/revision-v4-jof/supplement-visual-review.md",
    "notes/revision-v4-jof/table-preservation.json",
    "submission-jof/AUTHOR-TODO.md",
    "submission-jof/README.md",
    "submission-jof/cover-letter.md",
    "submission-jof/figures/conditional-annual-primary.pdf",
    "submission-jof/figures/conditional-common-history.pdf",
    "submission-jof/figures/conditional-primary-tradeoffs.pdf",
    "submission-jof/figures/murphy-fx_hourly.pdf",
    "submission-jof/figures/murphy-nyfed_weekly.pdf",
    "submission-jof/journal-requirements.md",
    "submission-jof/main.tex",
    "submission-jof/manuscript-content.json",
    "submission-jof/manuscript-preview.pdf",
    "submission-jof/manuscript.tex",
    "submission-jof/overleaf-package.zip",
    "submission-jof/references.bib",
    "submission-jof/supplement-content.json",
    "submission-jof/supplement-preview.pdf",
    "submission-jof/supplement.tex",
    "submission-jof/title-page-preview.pdf",
    "submission-jof/title-page.tex",
    "test_v4_numeric.py",
    "v4_figures.py",
    "v4_numeric.py",
    "v4_package.py",
    "v4_scientific_port.py",
    "v4_submission.py",
    "v4_typeset.py"
  ],
  "forbidden_path_matches": [],
  "data_paths": [
    "data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv",
    "data/nyfed-pdposgs-b-20261022/README.md",
    "data/nyfed-pdposgs-b-20261022/provenance.json"
  ],
  "nyfed_permission": "Existing attribution and Terms retained; see data-policy-audit.md",
  "new_raw_downloads": 0,
  "known_credential_pattern_matches": [],
  "protected_file_changes_except_authorized_README": [],
  "raw_FX_or_private_per_origin_artifacts_included": false,
  "scope": "path/type and staged-text scan plus data inventory; no claim of universal secret detection"
}
```
The full actual `git ls-files` output is saved in git-index-before-push.txt. The only raw-source observation file is the attributed NYFed CSV; no raw FX, private per-origin arrays, scratch content or standard credential-token matches entered the index. This is a scoped scan, not a universal secret-detection claim.

Actual authenticated-transport attempts:
```text
$ GIT_TERMINAL_PROMPT=0 git push -u origin revision-v4-jof
fatal: could not read Username for 'https://github.com': terminal prompts disabled
exit128
$ GIT_TERMINAL_PROMPT=0 git -c credential.helper=osxkeychain push -u origin revision-v4-jof
fatal: could not read Username for 'https://github.com': terminal prompts disabled
exit128
```
The existing connector recognized the requested account; that identity check is not a Git-transport credential. No credential was extracted, created or expanded, and no repeated connector write attempts were made after prior write-permission failures. There is no remote revision-v4-jof publication or PR receipt, and no remote/local-HEAD equality is claimed. This step needs the user's existing Git authentication to be restored, so it is skipped under the explicit no-question instruction.

Cleanup is consequently deferred. Inventory lists61 untracked backup files (430419B) and .scratch (848093297B at inventory time). The plan conditions their Trash move on successful remote verification; that condition is unmet. No file was moved to Trash or permanently deleted. The actual local package, source history, preserved old manuscripts, FINAL.md and all unrelated projects remain intact. No work process or resident service is left running.

Final readback: fetch still gives origin/main65feeee; ls-remote for revision-v4-jof returns empty (no published branch). main/FINAL/old sources remain unchanged. The default main.tex Overleaf wrapper also compiled successfully; exact native result is in wrapper-compiler-results.json. Final numeric check remains5102 matched tokens, zero mismatches. No additional permission question or remote mutation was performed.

## Pending user decisions

- Complete author identity/order/affiliation/contact/ORCID, funding, conflicts, author approval and applicable AI-use disclosure. No personal declaration was supplied or signed.
- Confirm the selected title: Forecasting Sampled Net-Position Peaks: Historical Rules, Conditional Quantiles and Validation. Alternatives: Accuracy and Calibration of Sampled Position-Peak Forecasts across FX and Treasury Tasks; When Conditional Quantiles Improve Position-Peak Forecasts: A Retrospective Model-Validation Study.
- Obtain and inspect the formal TeX-generated PDFs, preferably from the supplied Overleaf package; native compiler diagnostics passed, but did not export those PDFs.
- Resolve remaining bibliographic uncertainties listed in reference-audit.md (notably disputed MaxVaR pagination and incompletely registered older article end pages).
- Decide whether to merge the review PR later; this task does not merge main or enable auto-merge.
- Execute prospective public-release validation only with bound capture/issuance adapters. Compatible unseen second-dealer validation remains absent; the six NA outcomes remain visible.
- Complete the journal system steps personally; no account, submission, payment or disclosure form was performed.

Publication-specific pending action: restore existing Git authentication, push only revision-v4-jof, create the review PR against main, verify actual remote HEAD, then perform only the inventoried recoverable Trash moves. No permission question was sent.
