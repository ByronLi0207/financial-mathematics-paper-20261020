# WP5 actual command/output evidence

The scientific study ran once. The first independent readback hit the CSV parser limit; its failed output remains below and in its original file. Only verification code was repaired, with three regression tests and a new full suite; all71study/initial-summary file hashes remained identical.

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp5.py --run > notes/revision-v8/wp5-study-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "study_terminated", "status": "COMPLETE", "reason": null}
[exit0]
```

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 python -B run_v8_wp5.py --summarize
WARN `--no-project` was provided, but no project was found
{"event": "summary_written", "status": "COMPLETE", "method_slots": 8, "contrasts": 8}
[exit0]
```

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 python -B notes/revision-v8/audit_wp5.py --output notes/revision-v8/wp5-independent-audit.json
WARN `--no-project` was provided, but no project was found
Traceback (most recent call last):
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/audit_wp5.py", line 516, in <module>
    if __name__=='__main__':raise SystemExit(main())
                                             ^^^^^^
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/audit_wp5.py", line 510, in main
    result=audit_bundle(root,formal);output.parent.mkdir(parents=True,exist_ok=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/audit_wp5.py", line 458, in audit_bundle
    errors+=csv_errors(formal/'summary.csv',inventory);errors+=csv_errors(formal/'contrasts.csv',summary.get('contrasts',[]))
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/audit_wp5.py", line 64, in csv_errors
    reader=csv.DictReader(stream);actual=list(reader)
                                         ^^^^^^^^^^^^
  File "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/csv.py", line 116, in __next__
    row = next(self.reader)
          ^^^^^^^^^^^^^^^^^
_csv.Error: field larger than field limit (131072)
[exit1]
```

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 python -B notes/revision-v8/audit_wp5.py --output notes/revision-v8/wp5-independent-audit.json
WARN `--no-project` was provided, but no project was found
{
  "schema": "independent-wp5-audit-1",
  "status": "PASS",
  "audited_utc": "2026-10-24T11:03:29.915327+00:00",
  "difference_count": 0,
  "differences": [],
  "input_hashes": {
    "manifest.json": "ed01c556bcb73973d6ae50d96c4bf4e4fc8bccd9d1cc2cd200b4ac7665065e46",
    "inventory.json": "bb4567a873db31afd2a93e6a90b631d2a95ec0de7b33185d1216159646271916",
    "summary.json": "7b349dcd341f42b1b5f23b65f0f47673d56a90fcb50380ae4f8d5d012c544629",
    "study-termination.json": "5da8e8a4fdd795a151728ff5f47ea143c3a50717a211a81d87edeadd849cad0f",
    "summary.csv": "ce9fd997fd4eb96c08fb97a505475fdfd812d0777100d55413a8650bfeef1861",
    "contrasts.csv": "cd7c4c9d4ad72757c6192080419325b9eb2444b8beb3b83bc6c7967fb466a75b"
  },
  "scope": "Pinned source, fixed-grid target/loss/F/maturity/parameter and normal-HAC readback only; no QR refits or new tests.",
  "source_sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
  "original_rows_checked": 18576,
  "source_metadata": {
    "n": 18576,
    "source_first_timestamp": "2014-02-05T01:00:00.000000",
    "source_last_timestamp": "2017-01-24T00:00:00.000000",
    "origin_first": 3071,
    "origin_last": 10438,
    "origin_count": 7368,
    "first_issue_time": "2014-08-04T00:00:00.000000",
    "last_issue_time": "2015-10-06T23:00:00.000000",
    "target_end_by_horizon": {
      "6": "2015-10-07T05:00:00.000000",
      "24": "2015-10-07T23:00:00.000000"
    },
    "position_sha256": "f21a4ab7d35ac59d83eef1956dafdcce16d2dc6db1e31c5834cb46a7969d1e01",
    "times_sha256": "b2b0457013dcfc41ab03a65f5303ef3df0d2719de454afedafb67bc79be04f18"
  },
  "complete_trace_scores_checked": 8,
  "fit_maturity_records_checked": 16578,
  "planned_method_slots": 8,
  "actual_method_slots": 8,
  "normal_DM_comparisons_checked": 8,
  "known_exposure": {
    "extra_full_prefix": [
      3071,
      10438
    ],
    "previous_retro": [
      8999,
      10438
    ],
    "original_inspected": [
      11927,
      18551
    ],
    "overlap_origins": 1440,
    "previous_retro_fully_nested": true,
    "fresh_independent_third_period": false,
    "scientific_status": "MISMATCH",
    "mismatch": "MISMATCH-WP5-01",
    "later_parameter_choice_disclosed": true
  },
  "resources": {
    "status": "PASS",
    "attempted_worker_count": 8,
    "unverified_units": [],
    "observations": [
      {
        "unit_id": "H24_F_matched",
        "elapsed_seconds": 0.330701,
        "peak_rss_bytes": 62554112,
        "maximum_observed_os_threads": 1,
        "probe_count": 4,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H24_F_rolling720",
        "elapsed_seconds": 0.330858,
        "peak_rss_bytes": 65077248,
        "maximum_observed_os_threads": 1,
        "probe_count": 4,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H24_QR33",
        "elapsed_seconds": 43.130888,
        "peak_rss_bytes": 72318976,
        "maximum_observed_os_threads": 1,
        "probe_count": 171,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H24_QR4",
        "elapsed_seconds": 29.972485,
        "peak_rss_bytes": 63193088,
        "maximum_observed_os_threads": 1,
        "probe_count": 121,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H6_F_matched",
        "elapsed_seconds": 0.27039,
        "peak_rss_bytes": 62521344,
        "maximum_observed_os_threads": 1,
        "probe_count": 4,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H6_F_rolling720",
        "elapsed_seconds": 0.330685,
        "peak_rss_bytes": 65110016,
        "maximum_observed_os_threads": 1,
        "probe_count": 4,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H6_QR33",
        "elapsed_seconds": 27.767295,
        "peak_rss_bytes": 67321856,
        "maximum_observed_os_threads": 1,
        "probe_count": 111,
        "resource_source": "worker-receipt"
      },
      {
        "unit_id": "H6_QR4",
        "elapsed_seconds": 33.446266,
        "peak_rss_bytes": 64667648,
        "maximum_observed_os_threads": 1,
        "probe_count": 135,
        "resource_source": "worker-receipt"
      }
    ],
    "differences": [],
    "maximum_observed_rss_bytes": 72318976,
    "maximum_observed_os_threads": 1,
    "maximum_observed_worker_seconds": 43.130888,
    "termination_tolerance_seconds": 5.0
  },
  "study_elapsed_seconds": 135.72091462486424,
  "design_commit": "467a995b16a1c6446b5927992faec26b7f5f6276",
  "design_commit_time": "2026-10-24T03:48:52-07:00",
  "study_started_utc": "2026-10-24T10:57:23.306163Z",
  "private_npz_hashes": {
    "H6_F_matched/evaluation.npz": "63f35a58f03681db2145e1bb6cc2e9353ba192975f1736b9668bf0907b935870",
    "H6_F_rolling720/evaluation.npz": "f39bc1cc2fd587ad22b48359ef067e21ee648b97a6508dc43fdb7621fb9adca6",
    "H6_QR33/evaluation.npz": "b6aab4a654c1923c44f4c4b8f6231f820df62a92d25376dee59593223cd9e641",
    "H6_QR4/evaluation.npz": "247ec69e96e116ce96374ae39e80daf2a9c8ce85c8484ffd71ddb0d2477b84cf",
    "H24_F_matched/evaluation.npz": "379d31613a4bb373d5fdd84d7d01b79105ad1433c0c7473433ad22a4f1a233b8",
    "H24_F_rolling720/evaluation.npz": "7fc6f579372a8f53e359fa50807af92a118a24a95503b227e2d8dda9fce602f5",
    "H24_QR33/evaluation.npz": "a27df0474ccac5df7623fbdaca82989a66e4d1b8e40e37598152306beff69b13",
    "H24_QR4/evaluation.npz": "c950af3973407101306459e31545a17bfb0bdea664ec50fff46a77ea91ab438d"
  },
  "data_privacy": "Only aggregates and hashes are emitted; private vectors remain private.",
  "original_primary_comparisons_modified_by_auditor": false,
  "new_statistical_tests": false,
  "qr_refits_performed_by_auditor": 0,
  "auditor_sha256": "bb039d5728abe9048bd5336bbd9ec203c8641b8e3189432dac9819a7f07a45bb",
  "process_completion_is_not_method_success": true
}
[exit0]
```

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 python -B notes/revision-v8/build_wp5_readout.py
WARN `--no-project` was provided, but no project was found
Old archived comparison rows bound: 4
{"three_window_rows": 6, "old_source_rows": 9, "screen": {"status": "SUPPORT_WITH_LIMITS", "method": "QR33", "horizon": 6, "planned_comparisons": 6, "missing_comparisons": 0, "matched_wins": 3, "rolling_signs": [-1, 1], "comparisons": [{"window_name": "extra_full_prefix", "reference": "F_matched", "status": "COMPLETE", "relative_change_percent": -12.166526643171782, "available": true}, {"window_name": "extra_full_prefix", "reference": "F_rolling720", "status": "COMPLETE", "relative_change_percent": -5.29573502748879, "available": true}, {"window_name": "previous_retro", "reference": "F_matched", "status": "COMPLETE", "relative_change_percent": -16.62356533682211, "available": true}, {"window_name": "previous_retro", "reference": "F_rolling720", "status": "COMPLETE", "relative_change_percent": 3.1681985293173343, "available": true}, {"window_name": "original_inspected", "reference": "F_matched", "status": "COMPLETE", "relative_change_percent": -14.766762552613887, "available": true}, {"window_name": "original_inspected", "reference": "F_rolling720", "status": "COMPLETE", "relative_change_percent": -12.660126412969763, "available": true}], "missing": [], "fresh_independent_third_period": false, "independence_claim_status": "FAIL_MISMATCH", "previous_retro_overlap_count": 1440}, "old_missing_inference_recomputed": false}
[exit0]
```

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp5-final-gate
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
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp5-final-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp5-final-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked file copied; no test filtering or skips added",
  "tracked_files_copied": 2992,
  "started_utc": "2026-10-24T10:55:37.284463+00:00",
  "ended_utc": "2026-10-24T10:57:04.443650+00:00",
  "elapsed_seconds": 87.159153875,
  "returncode": 0,
  "child_peak_rss_bytes": 318455808,
  "output_sha256": "041f0d6ddbd44f98301ecfb33dccd04f7ce4b87dce86081b6bc39ae4ad2ffbb9",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1299 passed, 1066 subtests passed in 86.57s (0:01:26) =============
[exit0]
```
Full unabridged default-discovery output: `wp5-final-gate-pytest-output.txt`.

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp5-audit-repair-gate
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
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp5-audit-repair-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp5-audit-repair-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked file copied; no test filtering or skips added",
  "tracked_files_copied": 2992,
  "started_utc": "2026-10-24T11:01:17.076838+00:00",
  "ended_utc": "2026-10-24T11:02:43.276768+00:00",
  "elapsed_seconds": 86.19996579100001,
  "returncode": 0,
  "child_peak_rss_bytes": 323944448,
  "output_sha256": "614b72eede22bbb878d44a0af8c73f562aed2dce7dd2d2ccc1e74b531bf44985",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1302 passed, 1066 subtests passed in 85.77s (0:01:25) =============
[exit0]
```
Full unabridged default-discovery output: `wp5-audit-repair-gate-pytest-output.txt`.

```text
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached .scratch/revision-v8/wp5-table-preview/preview.tex --outdir .scratch/revision-v8/wp5-table-preview/compiled --keep-logs --keep-intermediates
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
warning: accessing absolute path `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-v8/wp5/three-window-table.tex`; build may not be reproducible in other environments
warning: accessing absolute path `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-v8/wp5/backcast-complete-table.tex`; build may not be reproducible in other environments
note: Rerunning TeX because "preview.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `.scratch/revision-v8/wp5-table-preview/compiled/preview.pdf` (11.3369140625 KiB)
note: Writing `.scratch/revision-v8/wp5-table-preview/compiled/preview.aux` (1.275390625 KiB)
note: Writing `.scratch/revision-v8/wp5-table-preview/compiled/preview.log` (6.4912109375 KiB)
[exit0]
```
Bothactualrenderedpagesviewed; source/PDF/PNGhashbinding: `wp5-table-visual.json`.

Metadata-only source-index proof command: `python3 -B notes/revision-v8/check_wp5_exposure.py`; actual output:
```json
{
  "status": "PASS",
  "scope": "Public metadata and source-index arithmetic, not new financial analysis",
  "source": "results/supervisor-20261023/r6/retro-cells.json",
  "source_sha256": "360734e167597656f234365e1d259b67d2c2c445d9871972b706b93d133f6e60",
  "R3_selection_status": "SELECTED",
  "R3_complete_candidate_count": 6,
  "R3_candidate_scored_issue_count": 3672,
  "old_H24_target_coverage_merged": [
    [
      3071,
      10462
    ]
  ],
  "new_full_prefix_issue_bounds": [
    3071,
    10438
  ],
  "new_H24_target_bounds": [
    3071,
    10462
  ],
  "nested_old_retro_issue_count": 1440,
  "fresh_unscored_third_period": false,
  "mismatch": "MISMATCH-WP5-01"
}
```

NoWP6review orpaperintegration began before thisWP5gate/completioncommit.
