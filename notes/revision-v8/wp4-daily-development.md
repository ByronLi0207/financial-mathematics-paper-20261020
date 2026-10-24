# WP4 daily primitive development

Only constructed dates/scalars are used; no raw FX file, DGP, source aggregation or model is read/run.

## RED before implementation

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest python -B -m pytest -p no:cacheprovider test_v8_daily_fx.py -q --tb=short
WARN `--no-project` was provided, but no project was found
Installed 6 packages in 33ms
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF                                [100%]
=================================== FAILURES ===================================
_____ test_last_observation_is_reported_at_completed_day_end_without_fill ______
test_v8_daily_fx.py:31: in test_last_observation_is_reported_at_completed_day_end_without_fill
    x,t=fixture(); d=api().resample_closed_days(x,t)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
________ test_selected_arrays_are_readonly_copies_and_inputs_unchanged _________
test_v8_daily_fx.py:46: in test_selected_arrays_are_readonly_copies_and_inputs_unchanged
    d=api().resample_closed_days(x,t)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_____ test_fingerprints_use_canonical_little_endian_vectors_and_nul_prefix _____
test_v8_daily_fx.py:61: in test_fingerprints_use_canonical_little_endian_vectors_and_nul_prefix
    d=api().resample_closed_days(x,t)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_________ test_metadata_contains_aggregate_fields_without_raw_vectors __________
test_v8_daily_fx.py:71: in test_metadata_contains_aggregate_fields_without_raw_vectors
    x,t=fixture();m=api().resample_closed_days(x,t).metadata
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
________ test_appending_later_days_cannot_change_completed_day_proxies _________
test_v8_daily_fx.py:81: in test_appending_later_days_cannot_change_completed_day_proxies
    x,t=fixture();before=api().resample_closed_days(x[:4],t[:4])
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
________ test_partial_first_and_last_days_are_retained_under_same_rule _________
test_v8_daily_fx.py:88: in test_partial_first_and_last_days_are_retained_under_same_rule
    d=api().resample_closed_days(np.array([11.]),np.array(['2020-01-04T12:01'],dtype='datetime64[m]'))
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[empty] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[nonfinite] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[shape] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[nat] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[duplicate] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[decreasing] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[not_datetime] _
test_v8_daily_fx.py:104: in test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute
    with pytest.raises(ValueError):api().resample_closed_days(x,t)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:5: in resample_closed_days
    raise NotImplementedError
E   NotImplementedError
_ test_original_ordinal_geometry_has_common_tail_and_mature_training[6-52-272] _
test_v8_daily_fx.py:109: in test_original_ordinal_geometry_has_common_tail_and_mature_training
    g=api().daily_issue_geometry(780,h,w,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_ test_original_ordinal_geometry_has_common_tail_and_mature_training[24-52-254] _
test_v8_daily_fx.py:109: in test_original_ordinal_geometry_has_common_tail_and_mature_training
    g=api().daily_issue_geometry(780,h,w,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_ test_original_ordinal_geometry_has_common_tail_and_mature_training[6-260-64] _
test_v8_daily_fx.py:109: in test_original_ordinal_geometry_has_common_tail_and_mature_training
    g=api().daily_issue_geometry(780,h,w,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_ test_original_ordinal_geometry_has_common_tail_and_mature_training[24-260-46] _
test_v8_daily_fx.py:109: in test_original_ordinal_geometry_has_common_tail_and_mature_training
    g=api().daily_issue_geometry(780,h,w,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
__ test_one_complete_evaluation_origin_is_admitted_without_fabricated_padding __
test_v8_daily_fx.py:117: in test_one_complete_evaluation_origin_is_admitted_without_fabricated_padding
    g=api().daily_issue_geometry(430,24,260,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
___________ test_empty_common_evaluation_is_na_without_moving_cutoff ___________
test_v8_daily_fx.py:123: in test_empty_common_evaluation_is_na_without_moving_cutoff
    g=api().daily_issue_geometry(429,6,52,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_____ test_unavailable_validation_labels_are_na_before_any_score_can_exist _____
test_v8_daily_fx.py:129: in test_unavailable_validation_labels_are_na_before_any_score_can_exist
    g=api().daily_issue_geometry(404,24,260,design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_______ test_inadequate_feature_history_is_na_without_shortening_window ________
test_v8_daily_fx.py:136: in test_inadequate_feature_history_is_na_without_shortening_window
    g=api().daily_issue_geometry(780,24,260,s)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
____________ test_invalid_geometry_options_are_rejected[True-6-52] _____________
test_v8_daily_fx.py:143: in test_invalid_geometry_options_are_rejected
    with pytest.raises(ValueError):api().daily_issue_geometry(n,h,w,design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_____________ test_invalid_geometry_options_are_rejected[-1-6-52] ______________
test_v8_daily_fx.py:143: in test_invalid_geometry_options_are_rejected
    with pytest.raises(ValueError):api().daily_issue_geometry(n,h,w,design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_____________ test_invalid_geometry_options_are_rejected[780-5-52] _____________
test_v8_daily_fx.py:143: in test_invalid_geometry_options_are_rejected
    with pytest.raises(ValueError):api().daily_issue_geometry(n,h,w,design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_____________ test_invalid_geometry_options_are_rejected[780-6-53] _____________
test_v8_daily_fx.py:143: in test_invalid_geometry_options_are_rejected
    with pytest.raises(ValueError):api().daily_issue_geometry(n,h,w,design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:9: in daily_issue_geometry
    raise NotImplementedError
E   NotImplementedError
_ test_historical_majority_and_literal_daily_counterexample_both_remain_visible _
test_v8_daily_fx.py:156: in test_historical_majority_and_literal_daily_counterexample_both_remain_visible
    r=api().classify_against_f(rows(),'QR33',design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
___________ test_three_conditional_wins_classifies_persistent_gains ____________
test_v8_daily_fx.py:166: in test_three_conditional_wins_classifies_persistent_gains
    r=api().classify_against_f(rows((.5,.5,.5,2.),'QR4'),'QR4',design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
____ test_ties_are_neither_win_and_mixed_grid_is_not_forced_into_dominance _____
test_v8_daily_fx.py:171: in test_ties_are_neither_win_and_mixed_grid_is_not_forced_into_dominance
    r=api().classify_against_f(rows((.5,2.,1.,1.)),'QR33',design())
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
________ test_another_regressions_failure_does_not_contaminate_this_one ________
test_v8_daily_fx.py:180: in test_another_regressions_failure_does_not_contaminate_this_one
    assert api().classify_against_f(data,'QR33',design())['status']=='TREASURY_LIKE'
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[row] _
test_v8_daily_fx.py:191: in test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive
    result=api().classify_against_f(data,'QR33',design())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[reference] _
test_v8_daily_fx.py:191: in test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive
    result=api().classify_against_f(data,'QR33',design())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[failed] _
test_v8_daily_fx.py:191: in test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive
    result=api().classify_against_f(data,'QR33',design())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[sample_na] _
test_v8_daily_fx.py:191: in test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive
    result=api().classify_against_f(data,'QR33',design())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_____ test_zero_reference_loss_preserves_absolute_comparison_and_exact_tie _____
test_v8_daily_fx.py:203: in test_zero_reference_loss_preserves_absolute_comparison_and_exact_tie
    result=api().classify_against_f(data,'QR33',design())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[duplicate] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[unknown_method] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[unexpected_window] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[negative_loss] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[nan] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[mismatched_n] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
_ test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[bad_breach] _
test_v8_daily_fx.py:217: in test_malformed_identity_or_complete_score_is_rejected_instead_of_classified
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
v8_daily_fx.py:13: in classify_against_f
    raise NotImplementedError
E   NotImplementedError
=========================== short test summary info ============================
FAILED test_v8_daily_fx.py::test_last_observation_is_reported_at_completed_day_end_without_fill
FAILED test_v8_daily_fx.py::test_selected_arrays_are_readonly_copies_and_inputs_unchanged
FAILED test_v8_daily_fx.py::test_fingerprints_use_canonical_little_endian_vectors_and_nul_prefix
FAILED test_v8_daily_fx.py::test_metadata_contains_aggregate_fields_without_raw_vectors
FAILED test_v8_daily_fx.py::test_appending_later_days_cannot_change_completed_day_proxies
FAILED test_v8_daily_fx.py::test_partial_first_and_last_days_are_retained_under_same_rule
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[empty]
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[nonfinite]
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[shape]
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[nat]
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[duplicate]
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[decreasing]
FAILED test_v8_daily_fx.py::test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute[not_datetime]
FAILED test_v8_daily_fx.py::test_original_ordinal_geometry_has_common_tail_and_mature_training[6-52-272]
FAILED test_v8_daily_fx.py::test_original_ordinal_geometry_has_common_tail_and_mature_training[24-52-254]
FAILED test_v8_daily_fx.py::test_original_ordinal_geometry_has_common_tail_and_mature_training[6-260-64]
FAILED test_v8_daily_fx.py::test_original_ordinal_geometry_has_common_tail_and_mature_training[24-260-46]
FAILED test_v8_daily_fx.py::test_one_complete_evaluation_origin_is_admitted_without_fabricated_padding
FAILED test_v8_daily_fx.py::test_empty_common_evaluation_is_na_without_moving_cutoff
FAILED test_v8_daily_fx.py::test_unavailable_validation_labels_are_na_before_any_score_can_exist
FAILED test_v8_daily_fx.py::test_inadequate_feature_history_is_na_without_shortening_window
FAILED test_v8_daily_fx.py::test_invalid_geometry_options_are_rejected[True-6-52]
FAILED test_v8_daily_fx.py::test_invalid_geometry_options_are_rejected[-1-6-52]
FAILED test_v8_daily_fx.py::test_invalid_geometry_options_are_rejected[780-5-52]
FAILED test_v8_daily_fx.py::test_invalid_geometry_options_are_rejected[780-6-53]
FAILED test_v8_daily_fx.py::test_historical_majority_and_literal_daily_counterexample_both_remain_visible
FAILED test_v8_daily_fx.py::test_three_conditional_wins_classifies_persistent_gains
FAILED test_v8_daily_fx.py::test_ties_are_neither_win_and_mixed_grid_is_not_forced_into_dominance
FAILED test_v8_daily_fx.py::test_another_regressions_failure_does_not_contaminate_this_one
FAILED test_v8_daily_fx.py::test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[row]
FAILED test_v8_daily_fx.py::test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[reference]
FAILED test_v8_daily_fx.py::test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[failed]
FAILED test_v8_daily_fx.py::test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive[sample_na]
FAILED test_v8_daily_fx.py::test_zero_reference_loss_preserves_absolute_comparison_and_exact_tie
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[duplicate]
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[unknown_method]
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[unexpected_window]
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[negative_loss]
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[nan]
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[mismatched_n]
FAILED test_v8_daily_fx.py::test_malformed_identity_or_complete_score_is_rejected_instead_of_classified[bad_breach]
41 failed in 0.37s

[exit 1]
```

## GREEN attempt after minimal implementation

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest python -B -m pytest -p no:cacheprovider test_v8_daily_fx.py -q --tb=short
WARN `--no-project` was provided, but no project was found
.........................................                                [100%]
41 passed in 0.11s

[exit 0]
```

## Final fixture verification

Strengthened existing assertions to check source inputs before intentional caller mutation and make the mismatched-count fixture retain a valid hit-rate fraction, so it specifically exercises paired sample alignment rather than a malformed breach fraction. No production behavior or frozen design changed.

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest python -B -m pytest -p no:cacheprovider test_v8_daily_fx.py -q --tb=short
WARN `--no-project` was provided, but no project was found
.........................................                                [100%]
41 passed in 0.11s

[exit 0]
```

The complete project suite and formal source run are integration gates owned by the parent; this local verification uses the one constructed-date/scalar test module only. No raw source was accessed and no financial model was fitted.

Final owned source SHA-256:

```json
{
  "v8_daily_fx.py": "cb9e86602ed01a6aefc37772df1245c7e060d5d719a803239deee08b79010b36",
  "test_v8_daily_fx.py": "53ffc6162208c1335e0490f150749e037456b6bd0412a969f0893a74e82cf9bc"
}
```
