# Revision v8 — ten-hour sequential execution ledger

Plan: `revision-plan-v8-goal10h.md`; original v7 execution rules remain binding where compatible.
Window: 2026-10-24 07:55:15–17:55:15 UTC (00:55:15–10:55:15 America/Vancouver). This window is elapsed time, not a claim of ten hours of continuous computation or reading.

## Execution contract

WP0 → WP9 in order. A WP requires recorded actual commands/output, all acceptance gates and one completion commit before the next WP. WP3–WP5 require separate design commits before results; those explicit preregistration commits are additional to the WP completion commits. No nonwhitelisted computations, deletion, new software installation, main merge, PR3 mutation, submission, invented data or author declarations. Original numeric results and adverse findings remain intact. Prose may express verified original percentages using the explicitly requested coarser rounding; underlying table values and result files cannot change.

10-minute checks are appended using their actual time; late checks are labelled rather than backfilled. During final review loops commits are capped at one per hour. The goal cannot be called complete before the deadline.

## WP0: PASS

Baseline: local `b571f324a253480b4e39bc8a8096775ddbcc7017`, published remote `d119a1fb30c48ceab9000552057882938cfa57a4`. Their Git histories differ because v7 was published through the browser; their complete trees are identical: `168620f47712c84a22878e77f540a4d151e08fdb`. A fresh fetch and diff are recorded in `notes/revision-v8/wp0-sync-output.json` (exit 0).

Created the requested new local branch `revision-v8-goal` from the local v7 final. Existing adjacent directory `金融数学论文-v8-20261024` has its own branch/work and uncommitted files; it is outside this task and is left untouched. No results from that directory are adopted.

Three-commit treatment and fresh post-transfer full pytest acceptance passed; see the evidence below.


### WP0 command and output record (actual)
```text
$ git fetch origin
[exit 0]
```
```text
$ git rev-parse HEAD origin/revision-v7-final
b571f324a253480b4e39bc8a8096775ddbcc7017
d119a1fb30c48ceab9000552057882938cfa57a4
[exit 0]
```
```text
$ git rev-parse HEAD^{tree} origin/revision-v7-final^{tree}
168620f47712c84a22878e77f540a4d151e08fdb
168620f47712c84a22878e77f540a4d151e08fdb
[exit 0]
```
```text
$ git diff --exit-code HEAD origin/revision-v7-final
[exit 0]
```
```text
$ git ls-remote origin refs/heads/main refs/heads/revision-v7-final refs/heads/revision-v8-goal refs/heads/codex/supervisor-revision-20261023
2328994c44ec02bd731ad556f41fe9821f6de6df	refs/heads/codex/supervisor-revision-20261023
65feeee801b6b228a608ca3200e0678bb5f62b1c	refs/heads/main
d119a1fb30c48ceab9000552057882938cfa57a4	refs/heads/revision-v7-final
[exit 0]
```
```text
$ git status --short
[exit 0]
```
Three-commit treatment: `notes/revision-v8/wp0-three-commit-treatment.md`. Original substantive patches: `notes/revision-v8/wp0-pr3-commit-diffs.txt`. Date/parent/ancestry commands: `notes/revision-v8/wp0-commit-chronology.json`. PR3 and PR4 status tool arguments and outputs: `notes/revision-v8/wp0-pr-status.json`.
```json
{
  "command": "python3 (exact descriptive-label substitutions with ordered numeric result-row equality assertion)",
  "source_commit": "d760b6b66188af6f7903a929568ebf12e69a7e47",
  "target": "submission-jof/supplement.tex",
  "header_occurrences_replaced": 4,
  "numeric_result_rows_checked": 368,
  "numeric_result_rows_identical": true,
  "header_before": "Series & H/W & F loss/hits & QR33 \\%/hits & QR4 \\%/hits & QR33+ \\%/hits & I \\%/hits \\\\",
  "header_after": "Series & H/W & F loss/hits & \\shortstack{Original\\\\regression\\\\\\% / hits} & \\shortstack{Four-predictor\\\\regression\\\\\\% / hits} & \\shortstack{Expanded-menu\\\\regression\\\\\\% / hits} & I \\%/hits \\\\",
  "paragraph_before": "Original QR33, QR4 and expanded QR33 are distinct fitted procedures.",
  "paragraph_after": "Original full regression, four-predictor regression and expanded-menu full regression are distinct fitted procedures (result codes QR33, QR4 and QR33+, respectively).",
  "rendering_pending": "WP2; source label transplant only"
}
```
```json
{
  "command": "python3 (SHA-256 comparison of all original tracked files; explicit changed-path and immutable result/data/protocol/code assertions)",
  "checked_utc": "2026-10-24T08:01:01.467419+00:00",
  "v7_files_checked": 2653,
  "missing": [],
  "changed_existing_files": [
    "submission-jof/supplement.tex"
  ],
  "original_result_data_protocol_code_files_checked": 1645,
  "protected_file_mismatches": 0,
  "allowed_change": "Descriptive Supplement labels only; 368 ordered numeric rows previously verified identical"
}
```
### Three-commit treatment table

| Commit | Treatment | Reason |
|---|---|---|
| d760b6b | 已移植（描述性标签）；其余已覆盖或不采纳 | Main labels already covered; remaining four Supplement headers and explanatory passage manually transferred, all numeric result rows unchanged. Old 71-family note is incompatible with the current displayed 72-family values. |
| 91dccbf | 已覆盖；不整体替换 | V7 already leads with historical benchmarks and preserves matched/rolling and score/breach distinctions; replacing it with the older structure would lose existing evidence. |
| 2328994 | 贡献内容已覆盖；旧核对包不作当前验收 | Old writing/PDF checks bind the supervisor source and 19-page document; keep them as history rather than claim current validation. |
### WP0 MISMATCH and clarified facts

`MISMATCH-WP0-01`: old 71-comparison reporting scope versus the original 72-comparison family shown in v7; the matching v7 note is kept. `MISMATCH-WP0-02`: old 19-page acceptance object versus the current documents; only fresh v8 checks count. These are scope boundaries, not changed financial values. The three commits really follow the 22:21 PDT research-line merge, so the temporary chronology concern was resolved rather than marked MISMATCH.

Timing ruling: approximate WP allocations sum to 10.75 hours. The ten-hour binding window and sequential acceptance gates take priority over the approximate individual durations; no gate is relaxed.

## MISMATCH register

WP0 scope boundaries are documented above and in the three-commit treatment note. No financial-result contradiction was found in this step.

## Pending author decisions

None identified at initialization.

### WP0 final pytest acceptance

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp0-after-transplant
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 991 passed, 1066 subtests passed in 131.68s (0:02:11) =============
[exit 0]
```

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
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp0-after-transplant/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp0-after-transplant/full-suite-copy",
  "scope": "Full default discovery; every tracked file copied; no test filtering or skips added",
  "tracked_files_copied": 2653,
  "started_utc": "2026-10-24T08:00:36.803728+00:00",
  "ended_utc": "2026-10-24T08:02:49.235264+00:00",
  "elapsed_seconds": 132.431622167,
  "returncode": 0,
  "child_peak_rss_bytes": 234700800,
  "output_sha256": "6218500d552813baac72906d4385b7e8c3a4ca1a9b581e7bc8b7d38b1b0b1c97",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
```

Full unfiltered output is `notes/revision-v8/wp0-after-transplant-pytest-output.txt`. Every original tracked file was copied into an isolated task scratch directory so synthetic fixture writes cannot alter the research archives. All required WP0 gates have passed. No financial analysis was run.

## WP1: PASS

Completed the researcher-voice pass. Original/revised passages are in `notes/revision-v8/wp1-before-after.md`; paragraph-by-paragraph findings and decisions are in `notes/revision-v8/wp1-readthrough.md`. The fixed baseline is the published v7 scientific text at local `b571f32`, not a previous v6 or supervisor document.

| Writing measure | Before | After | Limit |
|---|---:|---:|---|
| Abstract words | 139 | 143 | ≤180 |
| Abstract numeric items | 4 | 4 | ≤5 |
| Mean sentence words | 19.832558139534882 | 19.694835680751172 | 18–24 |
| Sentences over 35 words (%) | 0.0 | 0.0 | ≤8 |
| Sentences with negations (%) | 2.3255813953488373 | 2.816901408450704 | ≤8 |
| Maximum numbers per sentence | 2 | 2 | ≤2 |
| Percentages beyond one decimal | 15 | 0 | 0 |
| Changes … by sentences | 5 | 0 | 0 |
| Forbidden terms | 0 | 0 | 0 |
| Paragraphs over six sentences | 0 | 0 | 0 |

```text
$ python3 -B notes/revision-v8/writing_metrics.py --output notes/revision-v8/wp1-after-metrics.json --require-pass
{
  "before": {
    "abstract_words": 139,
    "abstract_numbers": 4,
    "main_sentences": 215,
    "mean_sentence_words": 19.832558139534882,
    "over35_percent": 0.0,
    "negation_percent": 2.3255813953488373,
    "max_numbers_per_sentence": 2,
    "overprecise_percentage_count": 15,
    "changes_by_count": 5,
    "all_v8_writing_gates_pass": false
  },
  "after": {
    "abstract_words": 143,
    "abstract_numbers": 4,
    "main_sentences": 213,
    "mean_sentence_words": 19.694835680751172,
    "over35_percent": 0.0,
    "negation_percent": 2.816901408450704,
    "max_numbers_per_sentence": 2,
    "overprecise_percentage_count": 0,
    "changes_by_count": 0,
    "all_v8_writing_gates_pass": true
  },
  "after_failures": {
    "numeric_violations": [],
    "paragraphs_over6": [],
    "banned_counts": {
      "retained": 0,
      "declared": 0,
      "frozen": 0,
      "receipt": 0,
      "archive(d)": 0,
      "byte": 0,
      "hash": 0,
      "post-result": 0,
      "exploratory": 0,
      "inspected": 0,
      "stipulated": 0,
      "issued": 0,
      "admissible": 0,
      "source-specific": 0,
      "no ... is claimed": 0,
      "does not establish": 0
    },
    "jargon_counts": {
      "evaluated finite delayed coverage correction": 0,
      "numerically accepted regression fits": 0,
      "explicitly identified comparison sets": 0,
      "source-native": 0,
      "completed response": 0,
      "strict-hit indicator": 0,
      "elementary-score curves": 0
    },
    "overprecise_percentages": [],
    "changes_by_sentences": []
  }
}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/check_wp1_rounding.py --output notes/revision-v8/wp1-rounding-green.json
{
  "operation": "saved-field lookup and display formatting only",
  "bound_percentages": 17,
  "mismatches": 0,
  "failures": []
}
[exit 0]
```

MISMATCH-WP1-01: direct source readback caught and corrected an intermediate double-rounding display (10.2 to source-formatted 10.1); original result remains unchanged. The first failing check and corrected field bindings are preserved, not overwritten. All 17 percentages are bound to original saved fields. All six original main table blocks, 27 mathematical blocks and 1,645 original data/result/protocol/code files remain identical.

```json
{
  "command": "python3 (exact original table/math block and original result/data/protocol/code SHA-256 comparisons)",
  "checked_utc": "2026-10-24T08:08:49.216006+00:00",
  "original_main_table_blocks": 6,
  "all_main_table_blocks_identical": true,
  "original_main_math_blocks": 27,
  "all_main_math_blocks_identical": true,
  "original_protected_files": 1645,
  "protected_mismatches": 0
}
```

### Before abstract and Introduction opening

```tex
Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. Long-history FX regression changes matched loss by -14.77\% and -16.62\% in the later and earlier periods. Its later advantage survives the evaluated finite delayed coverage correction. Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.

A position can finish inside its limit after exceeding that limit during the intervening period, as Figure~\ref{fig:example} illustrates. For a market maker, the relevant forecast therefore concerns the largest exposure before the next review, rather than the endpoint alone. The distinction changes the response variable, the observations available for training, and the interpretation of successful prediction. We study how established historical and conditional forecasts perform when every method targets this same sampled absolute-position peak.
```

### After abstract and Introduction opening

```tex
Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the later and earlier periods. Its later advantage survives a delayed adaptive coverage adjustment (ACI). Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.

A position can finish inside its limit after exceeding that limit during the intervening period, as Figure~\ref{fig:example} illustrates. For a market maker, the relevant forecast therefore concerns the largest exposure before the next review, rather than the endpoint alone. The distinction changes the response variable, the observations available for training, and the interpretation of successful prediction. We ask whether conditional forecasts can improve on historical rules for this sampled absolute-position peak.
```

## WP2: PASS

The three existing main figures now use ordinary axis numbers, matching serif fonts and black-solid/gray-dashed curves. The Treasury path and threshold axes use USD billions; conversion is display scaling of unchanged saved values. All six main tables and 25 Supplement tables use booktabs. Numerical outcome cells keep their original values: percentages use the original per-column display, counts remain integers, p-values retain consistent significant-figure formatting, and rational boundaries remain exact. Two p-value displays received zero-padding only, with exact Decimal equality checked. Internal method/rule labels in column headings were expanded.

The first compile exposed four 8.82703pt overfull alignments caused by longer descriptive preference-table headers. Splitting the header words corrected all four. Actual pixel review then identified missing continuation identifiers, small exact fractions and stretched reference word spacing; these were corrected through standard longtable continued captions, display-size fractions and ragged-right reference paragraphs. Original failure/first-pass records are retained. The Supplement is now 21 pages.

### Commands and actual outputs

```text
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached manuscript.tex --outdir /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/manuscript --keep-logs --keep-intermediates
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
note: Rerunning TeX because "manuscript.aux" changed ...
note: Rerunning TeX because "manuscript.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/manuscript/manuscript.log` (13.052734375 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/manuscript/manuscript.out` (2.1611328125 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/manuscript/manuscript.aux` (10.619140625 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/manuscript/manuscript.pdf` (156.8876953125 KiB)

[exit 0]
```
```text
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached supplement.tex --outdir /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/supplement --keep-logs --keep-intermediates
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
note: Rerunning TeX because "supplement.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/supplement/supplement.pdf` (134.333984375 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/supplement/supplement.log` (14.4775390625 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/supplement/supplement.aux` (19.0390625 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/compile-review/supplement/supplement.out` (6.779296875 KiB)
warning: supplement.tex:529: Underfull \hbox (badness 10000) in paragraph at lines 528--529
warning: supplement.tex:530: Underfull \hbox (badness 10000) in paragraph at lines 529--530
warning: supplement.tex:542: Underfull \hbox (badness 10000) in paragraph at lines 541--542
warning: supplement.tex:547: Underfull \hbox (badness 10000) in paragraph at lines 546--547
warning: supplement.tex:561: Underfull \hbox (badness 10000) in paragraph at lines 560--561
warning: supplement.tex:562: Underfull \hbox (badness 10000) in paragraph at lines 561--562
warning: supplement.tex:596: Underfull \hbox (badness 10000) in paragraph at lines 595--596
warning: supplement.tex:609: Underfull \hbox (badness 10000) in paragraph at lines 608--609
warning: supplement.tex:610: Underfull \hbox (badness 10000) in paragraph at lines 609--610
warning: supplement.tex:611: Underfull \hbox (badness 10000) in paragraph at lines 611--611
warning: supplement.tex:622: Underfull \hbox (badness 10000) in paragraph at lines 621--622
warning: supplement.tex:627: Underfull \hbox (badness 10000) in paragraph at lines 626--627
warning: supplement.tex:632: Underfull \hbox (badness 10000) in paragraph at lines 631--632
warning: supplement.tex:635: Underfull \hbox (badness 10000) in paragraph at lines 634--635
warning: supplement.tex:636: Underfull \hbox (badness 10000) in paragraph at lines 635--636
warning: supplement.tex:636: Underfull \hbox (badness 10000) in paragraph at lines 635--636
warning: supplement.tex:637: Underfull \hbox (badness 10000) in paragraph at lines 636--637
warning: supplement.tex:637: Underfull \hbox (badness 10000) in paragraph at lines 637--637
warning: supplement.tex:641: Underfull \hbox (badness 10000) in paragraph at lines 640--641
warning: supplement.tex:734: Underfull \hbox (badness 10000) in paragraph at lines 734--734
warning: supplement.tex:735: Underfull \hbox (badness 10000) in paragraph at lines 735--735
warning: supplement.tex:736: Underfull \hbox (badness 10000) in paragraph at lines 736--736
warning: supplement.tex:737: Underfull \hbox (badness 10000) in paragraph at lines 737--737
warning: supplement.tex:754: Underfull \hbox (badness 10000) in paragraph at lines 754--754
warning: supplement.tex:755: Underfull \hbox (badness 10000) in paragraph at lines 755--755
warning: supplement.tex:756: Underfull \hbox (badness 10000) in paragraph at lines 756--756
warning: supplement.tex:757: Underfull \hbox (badness 10000) in paragraph at lines 757--757
warning: supplement.tex:1364: Underfull \hbox (badness 1681) in paragraph at lines 1356--1364
warning: supplement.tex:529: Underfull \hbox (badness 10000) in paragraph at lines 528--529
warning: supplement.tex:530: Underfull \hbox (badness 10000) in paragraph at lines 529--530
warning: supplement.tex:542: Underfull \hbox (badness 10000) in paragraph at lines 541--542
warning: supplement.tex:547: Underfull \hbox (badness 10000) in paragraph at lines 546--547
warning: supplement.tex:561: Underfull \hbox (badness 10000) in paragraph at lines 560--561
warning: supplement.tex:562: Underfull \hbox (badness 10000) in paragraph at lines 561--562
warning: supplement.tex:596: Underfull \hbox (badness 10000) in paragraph at lines 595--596
warning: supplement.tex:609: Underfull \hbox (badness 10000) in paragraph at lines 608--609
warning: supplement.tex:610: Underfull \hbox (badness 10000) in paragraph at lines 609--610
warning: supplement.tex:611: Underfull \hbox (badness 10000) in paragraph at lines 611--611
warning: supplement.tex:622: Underfull \hbox (badness 10000) in paragraph at lines 621--622
warning: supplement.tex:627: Underfull \hbox (badness 10000) in paragraph at lines 626--627
warning: supplement.tex:632: Underfull \hbox (badness 10000) in paragraph at lines 631--632
warning: supplement.tex:635: Underfull \hbox (badness 10000) in paragraph at lines 634--635
warning: supplement.tex:636: Underfull \hbox (badness 10000) in paragraph at lines 635--636
warning: supplement.tex:636: Underfull \hbox (badness 10000) in paragraph at lines 635--636
warning: supplement.tex:637: Underfull \hbox (badness 10000) in paragraph at lines 636--637
warning: supplement.tex:637: Underfull \hbox (badness 10000) in paragraph at lines 637--637
warning: supplement.tex:641: Underfull \hbox (badness 10000) in paragraph at lines 640--641
warning: supplement.tex:734: Underfull \hbox (badness 10000) in paragraph at lines 734--734
warning: supplement.tex:735: Underfull \hbox (badness 10000) in paragraph at lines 735--735
warning: supplement.tex:736: Underfull \hbox (badness 10000) in paragraph at lines 736--736
warning: supplement.tex:737: Underfull \hbox (badness 10000) in paragraph at lines 737--737
warning: supplement.tex:754: Underfull \hbox (badness 10000) in paragraph at lines 754--754
warning: supplement.tex:755: Underfull \hbox (badness 10000) in paragraph at lines 755--755
warning: supplement.tex:756: Underfull \hbox (badness 10000) in paragraph at lines 756--756
warning: supplement.tex:757: Underfull \hbox (badness 10000) in paragraph at lines 757--757
warning: supplement.tex:1364: Underfull \hbox (badness 1681) in paragraph at lines 1356--1364
warning: warnings were issued by the TeX engine; use --print and/or --keep-logs for details.

[exit 0]
```
```json
{
  "operation": "Typography and descriptive headings only",
  "continued_caption_tables": 25,
  "exact_fractions_set_in_display_size": 86,
  "original_result_rows_unchanged_after_fraction-command_normalization": 368,
  "remaining_parameter_and_rule_headers_expanded": 4,
  "p_value_zero_padding": [
    {
      "before": " & 2.2e-07 & ",
      "after": " & 2.20e-07 & "
    },
    {
      "before": "Original matched Holm family: 0.32\\\\",
      "after": "Original matched Holm family: 0.320\\\\"
    }
  ],
  "numeric_values_changed": 0,
  "bibliography": "ragged-right within the bibliography to remove stretched URL lines"
}
```
```json
{
  "main_pages": 17,
  "supplement_pages": 21,
  "main_1_to_8": "wp2-visual-main-a.md plus exact current rendered-byte identity in wp2-main-pages1-8-current-binding.json",
  "main_9_to_17": "wp2-visual-main-b-final.md",
  "supplement_1_to_10": "wp2-visual-supp-a-final.md",
  "supplement_11_to_16": "wp2-visual-supp-b-final.md",
  "supplement_17_to_21": "wp2-visual-supp-c-final.json",
  "final_main_sha256": "41b7dde4bc7ee5de58c7ee7cd78f9c6173063d929035080461f7ec5b7d6774f1",
  "final_supplement_sha256": "77d950417642f466ca6e9f779d552ba825a8fc4a2111e9050173a44df06328ca",
  "unreviewed_pages": 0,
  "blocking_findings": 0
}
```
```json
{
  "checked_utc": "2026-10-24T08:23:18.783190+00:00",
  "status": "PASS",
  "main_tables": 6,
  "supplement_tables": 25,
  "current_figures": 3,
  "main_pages": 17,
  "supplement_pages": 21,
  "original_protected_file_count": 1645,
  "protected_mismatches": 0,
  "new_financial_computations": 0,
  "unreviewed_pages": 0,
  "overfull_undefined_missing_glyphs": 0,
  "all_current_sources_hash_bound": true,
  "nonblocking_layout_observations": [
    "Some longtable groups break across pages, with automatic continued table number and repeated headers."
  ]
}
```

Figure source hashes, point counts and style/tick checks: `notes/revision-v8/wp2-figure-styling.json`; original numeric table rows remain unchanged apart from the fraction-sizing command and two value-identical zero-padding changes. Table-by-table checklists: `wp2-manuscript-table-checklist.json` and `wp2-supplement-table-checklist.json`. Every current page screenshot path and the actual pdftoppm commands are in `wp2-rendering-final.json`; all 38 pages have pixel-review coverage. Main pages1–8 are byte-identical to the actual first visual review; final pages9–17 and all 21 Supplement pages have the final review records. Nonblocking longtable group splits keep captions and repeated headings.

The standalone plotting dependencies were used only through an offline cached temporary `uv run --with` environment, as authorized. No system software or new TeX package was installed. Financial sources, saved scores and original research code remain unchanged. All WP2 gates passed; the next step is to freeze WP3 before any simulation.

## WP3: IN_PROGRESS — design frozen before study computation

The fixed design is `protocol/revision-v8/wp3-mechanism-design.md` and its JSON. It uses the required72-cell level-AR/GARCH grid,32 predetermined repetitions, original QR33/QR4 menus and selector differences, mature training labels, matched fixed-window F, independent-repetition Monte Carlo errors, explicit failure/NA handling and a hard one-hour global deadline that also interrupts in-flight work. Main conclusions cannot be chosen after results.

Method and primary-source reading evidence: `notes/revision-v8/wp3-method-source-audit.md`; six exact historical resource objects are in `wp3-original-runtime-fields.json`, not represented as new timing measurements. The one pre-freeze budget loophole found by the same-model read was corrected before this commit.

```text
$ python3 (protocol index bounds, unchanged original module hashes, and absence of formal outputs)
{
  "checked_utc": "2026-10-24T08:37:00.471883+00:00",
  "design_paths": [
    "protocol/revision-v8/wp3-mechanism-design.json",
    "protocol/revision-v8/wp3-mechanism-design.md"
  ],
  "design_sha256": "ed2bedb5a086615957ea8423d61632edbb9de34549c886b4e2f6a04bb3567d70",
  "design_text_sha256": "ef708ee8aea26fe4a87affa445ef14fa0e43ec0f1ba0dd3db4c4b10a8f08d6a6",
  "grid_cells": 72,
  "repetitions": 32,
  "new_study_outputs_exist": false,
  "original_module_hashes_match": true,
  "global_deadline_stops_inflight": true,
  "status": "PRE_RESULT_DESIGN_ACCEPTED"
}
[exit 0]
```

This is the explicit mandatory design commit, additional to the single WP3 completion commit required after results. WP3 has not passed and no subsequent WP may begin.

### WP3 development evidence — before formal study

The62 deterministic tests are separate fixtures, not the32 Monte Carlo repetitions. The first60 contract tests were observed to fail solely on implementation stubs, then pass after implementation. Two further tests check exact QR4 agreement and forbid silently converting a nonfinite query into a floor report.

```json
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--offline",
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
    "test_v8_wp3_core.py",
    "test_v8_wp3_summary.py",
    "-q"
  ],
  "returncode": 1,
  "tail": [
    "FAILED test_v8_wp3_summary.py::test_row_without_a_repetition_id_is_rejected",
    "60 failed in 0.28s",
    "WARN `--no-project` was provided, but no project was found"
  ]
}
```

The new exact-QR4 fixture then failed before its fix:

```text
$ ... python -B -m pytest -p no:cacheprovider test_v8_wp3_core.py test_v8_wp3_summary.py -q
FAILED test_v8_wp3_core.py::test_qr4_matches_original_fixed_parameter_arithmetic
Mismatched elements: 2 / 6 (33.3%)
Max absolute difference among violations: 2.22044605e-16
1 failed, 61 passed in 0.25s
[exit 1]
```

```json
{
  "hypothesis": "QR4 column selection produced a Fortran-order intermediate; original features4 copies to C order. Different reduction/matrix layouts changed two reports by one ULP. Preserve the original layout, not a looser comparison tolerance.",
  "new_C_contiguous": false,
  "new_F_contiguous": true,
  "original_C_contiguous": true,
  "selected_values_equal": true,
  "training_mean_exact_equal_before_copy": false,
  "training_mean_exact_equal_after_copy": true
}
```

The cause was a Fortran-contiguous selected-column intermediate versus the original C-order copy. Matching the original layout corrected the arithmetic; comparison tolerances were not widened. No original code, scientific parameter or study design changed. No formal study observations existed during this correction.

```text
$ /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B -m pytest -p no:cacheprovider test_v8_wp3_core.py test_v8_wp3_summary.py -q
..............................................................           [100%]
62 passed in 0.21s
WARN `--no-project` was provided, but no project was found
[exit 0]
```

### WP3 pre-run independent review and preliminary full suite

A fresh read-only same-model review found a classification implementation stricter than the frozen protocol: missing target cells were always inconclusive, even when six known target gains and all outside cells were available. This is being corrected against the original rule before any study draw. The protocol, grid, menus, repetition count and seeds remain unchanged.

The first complete suite below tested the code copy before this pending classification correction; it is preliminary, not the final launch gate.

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp3-pre-run
1072 passed, 1066 subtests passed in 82.86s (0:01:22)
exit 0
```

Actual elapsed 83.273359s; measured child peak RSS 315834368 B; numerical threads 1. Full output and receipt: `notes/revision-v8/wp3-pre-run-pytest-output.txt`, `wp3-pre-run-pytest-receipt.json`.

### WP3 final pre-run gate — PASS (WP3 itself still pending)

The independent readback confirmed the support-rule correction follows the unchanged pre-result protocol. Exact command and full output are preserved.

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp3-final-gate
1080 passed, 1066 subtests passed in 83.75s (0:01:23)
exit 0
```

Measured full-suite elapsed 84.141837s; child peak RSS 312229888 B; one numerical thread. Receipt `notes/revision-v8/wp3-final-gate-pytest-receipt.json`. No study output directory existed at this gate. The only formal launch now uses the unchanged design commit `039f6f1b49d46610697bed5300cab687b37951df`; final run manifest seals all scientific source and test hashes before RNG initialization.

### WP3 independent display and readback fixtures

The display helper and independent stdlib auditor were developed without reading the formal run or calling its DGP/model functions. Their development notes preserve observed RED/GREEN stages. Root reran both final constructed-scalar suites during the sealed run:

```text
$ ... uv run --offline --no-project --no-env-file --python BUNDLED --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_plots.py -q
WARN `--no-project` was provided, but no project was found
...............                                                          [100%]
15 passed in 0.07s
exit 0

$ ... uv run --offline --no-project --no-env-file --python BUNDLED --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_audit.py -q
WARN `--no-project` was provided, but no project was found
.....................                                                    [100%]
21 passed in 0.31s
exit 0
```

`BUNDLED` is `/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`; the three environment variables are `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`. These checks do not add study repetitions, forecasts or model fits. Formal figure and audit acceptance remains pending termination.

### WP3 scientific result and complete delivery (acceptance pending final suite)

The predeclared narrow-region mechanism is **MISMATCH**, for both regressions: 2 clear target gains and 6 clear outside gains each. All72 procedure cells per regression have32 complete paired repetitions. The support rule, seed, menu and design were not revised. Full scientific counterexamples are in `support.json`; `notes/revision-v8/wp3-scientific-mismatch.json` records the required narrative correction. The draft result paragraph is source-bound to those counts, with integration reserved for WP7.

```text
$ ... python -B run_v8_wp3.py --run
WARN `--no-project` was provided, but no project was found
{"event": "study_terminated", "status": "COMPLETE", "reason": null}
exit 0

$ ... python -B run_v8_wp3.py --summarize
{"event": "summary_written", "status": "COMPLETE", "cells": 216}
exit 0

$ python3 -B notes/revision-v8/audit_wp3.py --output notes/revision-v8/wp3-independent-audit.json
{"status": "PASS", "difference_count": 0, "actual_inventory_count": 6912, "summary_cell_count": 216, "method_status_counts": {"COMPLETE": 6912}}
exit 0

$ python3 -B notes/revision-v8/build_wp3_readout.py
{"method_tasks": 6912, "summary_rows": 216, "candidate_status_counts": {"COMPLETE": 18431, "FAILED": 1}, "scientific_screen": "MISMATCH", "figures": 6, "input_changes": 0}
exit 0
```

The single failed QR4 validation candidate is retained: repetition23, phi0.9, homoskedastic, W52/H24, penalty0.1, NONCONVERGENCE at10000 iterations. The original eligible-candidate rule selected0.01; evaluation was not replaced. The complete candidate diagnostics remain in the public archive and readout bindings.

Execution2059.646685s; actual maxRSS63258624B, maxOSthreads1, maxworkerwall10.024692s. All288 workers measured. All six actual PNGs were viewed, each vector PDF has one page, and no clipping/overlap was found; uncapped loss annotations above100% remain visible. See `wp3-actual-figure-visual.json`.

To retain all results while avoiding a55MB loose JSON and38599 tiny public files, the exact original driver bytes were archived without deleting any loose file. Only the loose `units/` and `inventory.json` paths are Git-ignored; their complete contents are included in the indexed archive. This changes delivery format, not a calculation or a failure rule.

```text
$ python3 -B notes/revision-v8/package_wp3.py --audit notes/revision-v8/wp3-independent-audit.json
{"status": "PASS", "archive_name": "wp3-driver-output.tar.gz", "member_count": 38599, "archive_bytes": 14883171, "archive_sha256": "519f442094420053d8160ae07e5612f55ac8fe53d07fa8c689b674cdff7ecdb5", "source_hashes_unchanged": "PASS"}
exit 0
```

Every archived member was re-read and hashed; source file collection and hashes remained unchanged. No `.scratch` trace, raw FX file, original result or unrelated file was deleted or packaged.

### WP3 unabridged executed commands and output

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp3.py --run > notes/revision-v8/wp3-study-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "study_terminated", "status": "COMPLETE", "reason": null}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp3.py --summarize > notes/revision-v8/wp3-summary-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "summary_written", "status": "COMPLETE", "cells": 216}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/audit_wp3.py --output notes/revision-v8/wp3-independent-audit.json > notes/revision-v8/wp3-audit-console.txt 2>&1
{"status": "PASS", "difference_count": 0, "actual_inventory_count": 6912, "summary_cell_count": 216, "method_status_counts": {"COMPLETE": 6912}}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with matplotlib --with pypdf --with pillow python -B notes/revision-v8/plot_wp3.py --summary results/revision-v8/wp3/summary.json --outdir .scratch/revision-v8/wp3-formal-figures > notes/revision-v8/wp3-figure-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
Matplotlib is building the font cache; this may take a moment.
{"figures": 6, "source_sha256": "3de27c0f50a5b1882d4c8aba80d3fc8d2487972f22674d7e6e1423e62da663d0", "output_directory": ".scratch/revision-v8/wp3-formal-figures"}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/build_wp3_readout.py > notes/revision-v8/wp3-readout-console.txt 2>&1
{"method_tasks": 6912, "summary_rows": 216, "candidate_status_counts": {"COMPLETE": 18431, "FAILED": 1}, "scientific_screen": "MISMATCH", "figures": 6, "input_changes": 0}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/package_wp3.py --audit notes/revision-v8/wp3-independent-audit.json > notes/revision-v8/wp3-package-console.txt 2>&1
{"status": "PASS", "archive_name": "wp3-driver-output.tar.gz", "member_count": 38599, "archive_bytes": 14883171, "archive_sha256": "519f442094420053d8160ae07e5612f55ac8fe53d07fa8c689b674cdff7ecdb5", "source_hashes_unchanged": "PASS"}
[exit 0]
```


## WP3: PASS — verified experiment; scientific restriction MISMATCH

All specified WP3 delivery gates pass. This is procedural acceptance of the complete experiment, not support for its hypothesis. Both procedures contradict the predeclared narrow-region restriction, which must be changed in the later integrated narrative. Evidence: `notes/revision-v8/wp3-acceptance.json`.

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp3-complete-gate
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1132 passed, 1066 subtests passed in 88.06s (0:01:28) =============
[exit 0]
```

Full command/environment, scope and measured resources:

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
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp3-complete-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp3-complete-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked file copied; no test filtering or skips added",
  "tracked_files_copied": 2793,
  "started_utc": "2026-10-24T09:40:46.294164+00:00",
  "ended_utc": "2026-10-24T09:42:14.911234+00:00",
  "elapsed_seconds": 88.616216666,
  "returncode": 0,
  "child_peak_rss_bytes": 328171520,
  "output_sha256": "b817c9ac8174bd341146ee1b19dbed8e83d2f42bd09120654cfaf179a14716d7",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
```

Full original pytest output: `notes/revision-v8/wp3-complete-gate-pytest-output.txt`. No filters or skips were introduced. The final preservation check confirms all1645 original result/data/protocol/Python paths and all13 run-sealed paths unchanged; source-comparison output is in `wp3-original-preservation-final.json`. Main-paper integration is reserved for WP7. No WP4 computation or source recovery has started at this gate.

## WP4 pre-analysis design freeze (WP4 results pending)

WP3 completion commit is `9d8c731fff3ffa1bfa70ecdf50da1791fa5bc19d`. The whole-evidence `git diff --check` printed trailing whitespace from preserved raw pytest output and an extra caption EOF blank; it was not a WP3 acceptance gate and is not reported as passing. Verbatim output was retained. A follow-up source-only `git diff --check HEAD^ HEAD -- '*.py' .gitignore 'protocol/**'` returned0 with empty output. No raw console bytes were trimmed to manufacture a green check.

The original accepted raw CSV already exists inside this task scratch. Byte/hash verification returned:

```text
source=.scratch/data/1hourNetPositionsKaggle.csv
bytes=1286391
sha256=b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa
status=PASS
raw_rows_parsed=false
resampling_started=false
```

No Trash access or download is needed. Original-rule audit and source line references: `notes/revision-v8/wp4-original-rule-audit.md`. **MISMATCH-WP4-01:** the original Treasury cutoff uses2021 absolute dates, which cannot evaluate the accepted earlier FX record. The predeclared adaptation preserves its observation-index geometry (validation329–380; evaluation405 through n_daily−25; refit13; RMS6/26), with an explicit same-calendar/proportional-split exclusion. The daily report occurs after each source-naive day ends, because its last observation is not identifiable earlier. Empty days stay absent.

The frozen contract specifies all methods/menus, mature-label clock, NA and failure rules, per-regression support/non-support classifications and actual resource limits. The complete four-cell table, not favorable cases alone, will determine the decision-map update. Even historical dominance will not be presented as causal identification of frequency or independent-dealer validation. `wp4-pre-result-design-check.json` records the source hash and confirms zero daily rows/forecasts constructed at this point.

This is the mandatory design commit before any new WP4 aggregation or model evaluation, not a completed WP4 result. No original result or WP3-sealed source file was modified.

### WP4 final pre-run gate — PASS (WP4 result pending)

The preliminary full suite passed1187+1066 before the legitimate INELIGIBLE-interruption correction. The corrected driver test then observed2 failures before its fix and18 passes after it. All scientific choices remain at design commit `1427dc0b943ee77a82ee03a67ec9281c20e2cdf5`.

```text
$ python3 -B notes/revision-v8/run_full_pytest.py wp4-final-gate
1209 passed, 1066 subtests passed in 83.00s (0:01:22)
[exit 0]
```

Full original output is in `notes/revision-v8/wp4-final-gate-pytest-output.txt`; exact nested command/environment/resources:

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
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp4-final-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v8/wp4-final-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked file copied; no test filtering or skips added",
  "tracked_files_copied": 2809,
  "started_utc": "2026-10-24T10:16:21.592553+00:00",
  "ended_utc": "2026-10-24T10:17:45.128677+00:00",
  "elapsed_seconds": 83.53603233300001,
  "returncode": 0,
  "child_peak_rss_bytes": 323633152,
  "output_sha256": "f57e89bd6c7be7902b1c119f4f5d7f82a3224be26e3cb730a78462f704456af6",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
```

The formal WP4 directory did not exist at this gate, the raw CSV had not been aggregated for WP4, and all9 original/WP3 source hashes match the pre-result protocol. Source review is `wp4-pre-run-source-review.json`; this is followed by the one sealed actual run, without numerical retuning or additional methods.

## WP4: PASS — complete same-dealer daily contrast; scope limits and exception retained

Design `1427dc0b943ee77a82ee03a67ec9281c20e2cdf5` preceded actual parsing/aggregation. Unique actual study completed4workers/12methods/32candidates; all44 score traces and596 refit records independently checked,0differences. The pre-run default suite passed1209tests and1066subtests; all scientific/audit sources remain identical, so it was not needlessly repeated after table-only generation.

The actual series has930 nonempty source-naive days and501 evaluation issues, not the rough780-day estimate. F wins7/8 comparisons: QR33 loses4/4; QR4 loses3/4. The remaining QR4 W260/H6 comparison lowers mean loss2.973993%, but strict breaches are37 versus30 for F. This exception and every adverse result remain. Both frozen majority classifications are TREASURY_LIKE. Same source identity alone cannot explain all rankings; physical horizon/history and sampled target also change, so a pure frequency cause has not been isolated. No compatible independent dealer validation is claimed.

Actual runtime9.748697s; max observed workerRSS58359808B/one OSthread/maxworker4.081998s. Main original primaries/results and all1645 protected source paths are unchanged, as are every run-sealed source/protocol hash. Complete result table, source bindings, all cell receipts, periods, classification and decision-map consequence: `results/revision-v8/wp4/`. Acceptance: `notes/revision-v8/wp4-acceptance.json`; mismatches: `wp4-mismatches.json`.

The complete12row LaTeX table was compiled with existing cached Tectonic, rendered and actually viewed: one page, no error/overfull/undefined/missing glyph; the local absolute-input warning is retained in the original console. This preview is not final manuscript-page verification.

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp4.py --run > notes/revision-v8/wp4-study-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "study_terminated", "status": "COMPLETE", "reason": null}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp4.py --summarize > notes/revision-v8/wp4-summary-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "summary_written", "status": "COMPLETE", "method_slots": 12, "contrasts": 8}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 python -B notes/revision-v8/audit_wp4.py --output notes/revision-v8/wp4-independent-audit.json > notes/revision-v8/wp4-audit-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"status": "PASS", "difference_count": 0, "actual_method_slots": 12, "actual_candidate_slots": 32, "complete_trace_scores_checked": 44}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 python -B notes/revision-v8/build_wp4_readout.py > notes/revision-v8/wp4-readout-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"method_rows": 12, "contrasts": 8, "daily_rows": 930, "evaluation_issues": 501, "historical_wins": 7, "complete_comparisons": 8, "source_input_changes": 0}
[exit 0]
```

```text
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached .scratch/revision-v8/wp4-table-preview/preview.tex --outdir .scratch/revision-v8/wp4-table-preview/compiled --keep-logs --keep-intermediates > notes/revision-v8/wp4-table-compile-console.txt 2>&1
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
warning: accessing absolute path `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-v8/wp4/daily-results-table.tex`; build may not be reproducible in other environments
note: Rerunning TeX because "preview.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `.scratch/revision-v8/wp4-table-preview/compiled/preview.log` (6.36328125 KiB)
note: Writing `.scratch/revision-v8/wp4-table-preview/compiled/preview.pdf` (7.9794921875 KiB)
note: Writing `.scratch/revision-v8/wp4-table-preview/compiled/preview.aux` (663 B)
[exit 0]
```

No WP5 backcast model, period selection or computation has begun at this acceptance gate. Integration of the queued daily results and decision-map row remains WP7.


## WP5: PASS

Procedural PASS means the exact original fixed-prefix backcast, complete result inventory and honest overlapping-window summary were executed and verified. It does **not** mean a previously unscored third independent period was obtained: that claim is **FAIL/MISMATCH-WP5-01**. Design467a995 precedes the unique135.720915s run. All8methods and8specifiednormal-HACcomparisons complete; independent readback0differences checks8scoretraces and16578maturefitrecords. MaxworkerRSS72318976B,OSthreads1,maxworker43.130888s.

H6QR33screen is SUPPORT_WITH_LIMITS: all three inspected-window matched mean changes favorQR, while rolling-reference direction varies. The newfullprefix includes all1440 earlierretroorigins; oldR3targetexposure covers itsH24paths. NewH24matchedgains also defeat literalshort-horizon-only phrasing (MISMATCH-WP5-02). Scores, breaches, rawpvalues, unfavorableH24rollingcomparison andmissingoldbreach/DMfields remain visible. No retrospective design can create a new independentdealer/prospective validation.

FirstauditfailedonCSVdefault131072fieldlimit; the exactfailedconsole andcommandreceiptremain. Repairchanged onlyauditorCSVreader plus3regressiontests. Subsequent fullsuite1302tests+1066subtestsPASS;71scientificstudy/initialsummaryfilehashes identical; all1645baselineprotectedpathsunchanged. No studywasrerun and noforecastingparameters/sourcechanged.

Acceptance: `notes/revision-v8/wp5-acceptance.json`; source/gateadjudicationandprior-exposureproof retain both audit judgments, the inherited rule4 rationale and MISMATCH. Complete results: `results/revision-v8/wp5/summary.json`, `FULL_BACKCAST_RESULTS.md`, `THREE_WINDOWS.md`, and exactoldfieldbindings. Both tablepreviewpagesrenderedandactuallyviewed; noerror/overfull/undefined/missingglyph.

Actual commands and original outputs, including failedreadback and both fullsuite receipts, follow in `notes/revision-v8/wp5-commands-and-output.md` and their unabridged logs.

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



## WP6: PASS

Threefreshinternalroles each delivered9findings: editor6major/3minor;econometrician7major/2minor;riskmanager7major/2minor. All27individualdispositions are in `notes/revision-v8/internal-review-2.md`, including explicit reasons for scientificlimits that cannot be solved withinthisdesign. This is an internal review and disposition gate, not actualjournalreview, cross-modelreview, scientificconfirmation or aclaimthatWP7integrationhasalreadyoccurred. All20majoritems have a concrete response or reason; no major was silently labelledscientificallysolved.

No newfinancialcomputation, model, data, test or tuning occurred. Main/Supplement/coverletter remainunchanged inWP6; accepted responses are routed toWP7. The originalcompleteinternalreviews are retained in `review-A-editor.md`, `review-B-econometrics.md`, `review-C-risk-manager.md`.

```text
$ python3 -B notes/revision-v8/check_wp6_reviews.py
{
  "checked_utc": "2026-10-24T11:16:07.709346+00:00",
  "status": "PASS",
  "wp": "WP6",
  "review_roles": {
    "A": {
      "path": "notes/revision-v8/review-A-editor.md",
      "sha256": "ccddcb21c75ad7c6ba2340fcea5a1717cfa3f390a5f692a45038a53730bfe5bd",
      "count": 9,
      "major": 6,
      "minor": 3
    },
    "B": {
      "path": "notes/revision-v8/review-B-econometrics.md",
      "sha256": "ded2bf701fcf03d11dbc19d4d3a0c3eddc6b8ba8aac0f2dc12cc26a8d52a6418",
      "count": 9,
      "major": 7,
      "minor": 2
    },
    "C": {
      "path": "notes/revision-v8/review-C-risk-manager.md",
      "sha256": "7480f5e9124732711ed03e13d2aacc7d49635df97e2bb9e3b45239029a51cd23",
      "count": 9,
      "major": 7,
      "minor": 2
    }
  },
  "total_findings": 27,
  "major_findings": 20,
  "minor_findings": 7,
  "dispositions": 27,
  "major_without_response_or_reason": 0,
  "new_financial_computations": 0,
  "new_models_data_tests_or_tuning": false,
  "unresolved_scientific_gaps_explicitly_retained": true,
  "manuscript_integration_not_yet_claimed": "WP7 next; currentTeXunchanged inWP6",
  "premature_submission_file_edits": [],
  "external_or_cross_model_review": false,
  "response_sha256": "bd1a57f39f83f8c43c853d50363c19a04dbbf8b2b68f8c4fd5652f61c770941c"
}
[exit0]
```


## WP7: PASS

Integrated the acceptedWP3–5resultsandall27reviewresponses into main/Supplement/map/abstract/conclusion/coverletter, withscientificlimitsretained. Main20pages,4figures/6tables; Supplement29pages<=30. Body4996words; conservativebudgetincluding164wordabstract5160<=9000, retainingtransparencyandfigurecaptions inbudget. All6oldmainresult-tablenumericvectors andallolddisplaymathblocks unchanged; all368oldSupresultrows+2numericheaders unchanged.

The mainuses oneMCparagraph+oneoriginalsaved-summarylossfigure; completedSupgrids contain72+72QRrows,12dailyrows,6overlappingwindowrows and8backcastcomparisons. Main20percentagefields lookupPASS0differences; currentwritinggatesPASS. NewSup2080fieldbindingscheck0mismatches. These areintegrationchecks; all-number/ref/finalallpage/testgatesremainWP8.

MISMATCH-WP7-LETTER-01/02 narrowtherequestedmechanism/frequencyclaims toactualevidence. MISMATCH-WP7-SEED-DISPLAY corrects defaultg-rounding oftheintegerseed; originalincorrectdraftsource/PDF/PNG/hashesretained,design andstudyseedunchanged. Independentreviewfollowthroughrequired andverifiedexplicitoldprefixrange andnoevaluatedproductionfallbackpolicy.

OpenlayoutnotesroutedtoWP8: acontinuedH,fragmentatSup28top andsparsefinalroutesparagraphon29; underfullwarningsarepreserved, nooverfull/error/undefined/missingglyph. No claimofwhole-goalcompletion orpublication.

Acceptance: `notes/revision-v8/wp7-acceptance.json`; exactfirst-passagebefore/after: `wp7-before-after.md`; sourcefieldreceiptsandactualcommandsfollow.

# WP7 actual command/output evidence

No financial model or new statistical test runs in this package. Source-bound formatting and compilation only. Full implementation/field ledgers and all draft failures remain in separate unchanged files.

```text
$ python3 -B notes/revision-v8/integrate_wp7_main.py
{
  "operation": "Existing saved fields and prose integration only; no new financial calculation",
  "main_figures": 4,
  "main_tables": 6,
  "abstract_added_sentences": 1,
  "main_MC_result_paragraphs": 1,
  "all6_original_table_numeric_vectors_unchanged": true,
  "all_original_display_math_blocks_byte_identical": true,
  "scientific_results_modified": false
}
[exit0]
```

```text
$ python3 -B notes/revision-v8/writing_metrics.py --output notes/revision-v8/wp7-writing-initial.json --require-pass
{
  "before": {
    "abstract_words": 139,
    "abstract_numbers": 4,
    "main_sentences": 215,
    "mean_sentence_words": 19.832558139534882,
    "over35_percent": 0.0,
    "negation_percent": 2.3255813953488373,
    "max_numbers_per_sentence": 2,
    "overprecise_percentage_count": 15,
    "changes_by_count": 5,
    "all_v8_writing_gates_pass": false
  },
  "after": {
    "abstract_words": 164,
    "abstract_numbers": 4,
    "main_sentences": 244,
    "mean_sentence_words": 19.03688524590164,
    "over35_percent": 0.0,
    "negation_percent": 4.508196721311475,
    "max_numbers_per_sentence": 2,
    "overprecise_percentage_count": 0,
    "changes_by_count": 0,
    "all_v8_writing_gates_pass": false
  },
  "after_failures": {
    "numeric_violations": [],
    "paragraphs_over6": [],
    "banned_counts": {
      "retained": 1,
      "declared": 1,
      "frozen": 0,
      "receipt": 0,
      "archive(d)": 0,
      "byte": 0,
      "hash": 0,
      "post-result": 0,
      "exploratory": 0,
      "inspected": 4,
      "stipulated": 0,
      "issued": 1,
      "admissible": 0,
      "source-specific": 0,
      "no ... is claimed": 0,
      "does not establish": 0
    },
    "jargon_counts": {
      "evaluated finite delayed coverage correction": 0,
      "numerically accepted regression fits": 0,
      "explicitly identified comparison sets": 0,
      "source-native": 0,
      "completed response": 0,
      "strict-hit indicator": 0,
      "elementary-score curves": 0
    },
    "overprecise_percentages": [],
    "changes_by_sentences": []
  }
}
[exit1; draft prose-word exclusions subsequently corrected]
```

```text
$ python3 -B notes/revision-v8/check_wp7_rounding.py --output notes/revision-v8/wp7-rounding-check.json
{
  "status": "PASS",
  "operation": "exactsavedfieldlookup andone-decimalprosedisplayonly",
  "original_bound_percentage_fields": 17,
  "new_bound_percentage_fields": 3,
  "total_bound_percentage_fields": 20,
  "current_percentage_sentences": 14,
  "unbound_percentage_sentences": 0,
  "mismatches": 0
}
[exit0]
```

```text
$ python3 -B notes/revision-v8/writing_metrics.py --output notes/revision-v8/wp7-writing-final.json --require-pass
{
  "before": {
    "abstract_words": 139,
    "abstract_numbers": 4,
    "main_sentences": 215,
    "mean_sentence_words": 19.832558139534882,
    "over35_percent": 0.0,
    "negation_percent": 2.3255813953488373,
    "max_numbers_per_sentence": 2,
    "overprecise_percentage_count": 15,
    "changes_by_count": 5,
    "all_v8_writing_gates_pass": false
  },
  "after": {
    "abstract_words": 164,
    "abstract_numbers": 4,
    "main_sentences": 244,
    "mean_sentence_words": 19.049180327868854,
    "over35_percent": 0.0,
    "negation_percent": 4.508196721311475,
    "max_numbers_per_sentence": 2,
    "overprecise_percentage_count": 0,
    "changes_by_count": 0,
    "all_v8_writing_gates_pass": true
  },
  "after_failures": {
    "numeric_violations": [],
    "paragraphs_over6": [],
    "banned_counts": {
      "retained": 0,
      "declared": 0,
      "frozen": 0,
      "receipt": 0,
      "archive(d)": 0,
      "byte": 0,
      "hash": 0,
      "post-result": 0,
      "exploratory": 0,
      "inspected": 0,
      "stipulated": 0,
      "issued": 0,
      "admissible": 0,
      "source-specific": 0,
      "no ... is claimed": 0,
      "does not establish": 0
    },
    "jargon_counts": {
      "evaluated finite delayed coverage correction": 0,
      "numerically accepted regression fits": 0,
      "explicitly identified comparison sets": 0,
      "source-native": 0,
      "completed response": 0,
      "strict-hit indicator": 0,
      "elementary-score curves": 0
    },
    "overprecise_percentages": [],
    "changes_by_sentences": []
  }
}
[exit0]
```

```text
$ python3 -B notes/revision-v8/check_wp7_budget.py --output notes/revision-v8/wp7-budget.json
{
  "checked_utc": "2026-10-24T11:36:58.308086+00:00",
  "status": "PASS",
  "operation": "Word/layout/source checks only",
  "word_count_method": "Regexalphanumeric tokens including numeric/math tokens, figure captions and full Research design/transparency; excludes all table environments/references/author-provided placeholder block. Abstract added separately. No favorable exclusion of transparency from this budget.",
  "section_words_excluding_table_environments": {
    "Introduction": 782,
    "Related literature": 327,
    "The forecast target": 540,
    "Data": 314,
    "Forecasting methods": 433,
    "Evaluation design": 451,
    "Results": 1171,
    "Implications for model validation": 251,
    "Limitations": 287,
    "Conclusion": 274,
    "Data and code availability": 166
  },
  "main_body_words": 4996,
  "abstract_words": 164,
  "budget_words_including_abstract": 5160,
  "word_limit": 9000,
  "main_figures": 4,
  "main_tables": 6,
  "main_pages": 20,
  "supplement_pages": 29,
  "supplement_page_limit": 30,
  "main_source_sha256": "3769d9ea4e342ebc2fb8dd2ff0239cbc3ab508dbc1ce9925d5808406e7135814",
  "main_pdf_path": ".scratch/revision-v8/wp7-main-final-layout/manuscript.pdf",
  "main_pdf_sha256": "a8881e6c71f5325e2e798084e8ca2d4b873927e45932b766c91f98538cc63814",
  "supplement_source_sha256": "e9472bb4f2238c4ac941ab4c206bd880a546bc1f2fd7351b94e92c6fd0ac8b28",
  "supplement_pdf_path": ".scratch/revision-v8/wp7-supplement-preview/compiled-postreview/supplement.pdf",
  "supplement_pdf_sha256": "e1ef75d6b3a3479513e0e3449df2cdd181ffcb065f0bea24545a19daf4b49f28",
  "final_all_page_QA_not_yet_claimed": "WP8 required"
}
[exit0]
```

```text
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached manuscript.tex --outdir ../.scratch/revision-v8/wp7-main-final-layout --keep-logs --keep-intermediates
[cwd submission-jof]
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
note: Rerunning TeX because "manuscript.out" changed ...
note: Running xdvipdfmx ...
note: Writing `../.scratch/revision-v8/wp7-main-final-layout/manuscript.log` (13.16015625 KiB)
note: Writing `../.scratch/revision-v8/wp7-main-final-layout/manuscript.aux` (11.9453125 KiB)
note: Writing `../.scratch/revision-v8/wp7-main-final-layout/manuscript.pdf` (183.431640625 KiB)
note: Writing `../.scratch/revision-v8/wp7-main-final-layout/manuscript.out` (2.4169921875 KiB)
[exit0]
```

Actual final Supplement compile receipt:
```json
{
  "started_utc": "2026-10-24T11:32:39.179065+00:00",
  "ended_utc": "2026-10-24T11:32:39.794862+00:00",
  "command": [
    "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
    "-X",
    "compile",
    "--only-cached",
    "submission-jof/supplement.tex",
    "--outdir",
    ".scratch/revision-v8/wp7-supplement-preview/compiled-postreview",
    "--keep-logs",
    "--keep-intermediates"
  ],
  "returncode": 0,
  "elapsed_seconds": 0.61580925,
  "pages": 29,
  "source_sha256": "e9472bb4f2238c4ac941ab4c206bd880a546bc1f2fd7351b94e92c6fd0ac8b28",
  "pdf_path": ".scratch/revision-v8/wp7-supplement-preview/compiled-postreview/supplement.pdf",
  "pdf_sha256": "e1ef75d6b3a3479513e0e3449df2cdd181ffcb065f0bea24545a19daf4b49f28",
  "log_sha256": "f6db6e96bbc299544ec071456e458de0271335c0af4083def2e5da99cd438f9a",
  "error_overfull_undefined_missing_glyph_lines": [],
  "underfull_warning_count": 28,
  "scope": "post-reviewtwo-gapwritingfix integrationpreview; parentWP8fullfinalPDFQA remainsrequired",
  "prior_receipt_snapshot": "notes/revision-v8/wp7-supplement-compile-receipt-pre-followthrough.json"
}
```

Full Supplement build/verification/seed-display failure and repair evidence are preserved in the wp7-supplement-* logs and JSON, including versioned pre-followthrough receipts. Initial integer seed shorthand was not exact; the complete seed is now checked from its frozen integer field.

Independent27itemfollowthrough: `wp7-review-followthrough.md`; all source sentences and existing table inputs actually checked. No current full-number/PDF/pytest/publication PASS is claimed by this package.



## WP8: PASS

Accepted 2026-10-24T12:10:05.008381+00:00. Scope is the current document/source verification and delivered package, rather than independent financial replication. No new financial experiment, model, sample, hypothesis test or tuning was run in WP8.

Current native documents: main20pages including references/author placeholders; Supplement30pages; unfilled titlepage1page. Main body4996words, abstract164, budget5160;4mainfigures and6maintables. The source snapshots, native preview aliases, references, cover letter, author checklist and19memberOverleafpackage now all describe v8. Historical guides are explicitly labelled; `FINAL.md` and original archives are unchanged.

### Numeric, figure, reference and cross-reference gates

Actual commands executed:

```text
python3 -B notes/revision-v8/check_wp8_main_numbers.py --output notes/revision-v8/wp8-main-number-check-root.json
python3 -B notes/revision-v8/check_wp8_supp_numbers.py --output notes/revision-v8/wp8-supp-number-check-final-layout.json
python3 -B notes/revision-v8/check_wp8_figures.py
python3 -B notes/revision-v8/writing_metrics.py --output notes/revision-v8/wp8-writing-metrics.json --require-pass
```

Verbatim successful Supplement stdout:

```text
$ python3 -B notes/revision-v8/check_wp8_supp_numbers.py
{
  "status": "PASS_WITH_SCOPE_LIMITS",
  "counts": {
    "old_typed_fields": 2125,
    "old_numeric_rows": 370,
    "old_result_rows": 368,
    "new_typed_fields": 2080,
    "mc_rows": 144,
    "daily_rows": 12,
    "three_window_rows": 6,
    "complete_backcast_rows": 8
  },
  "numeric_occurrences": 4983,
  "number_word_occurrences": 109,
  "failures": 0,
  "unresolved": 0,
  "ambiguous": 0,
  "output": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/notes/revision-v8/wp8-supp-number-check.json"
}

[exit 0]
```

This earlier stdout has the same counts as the final-layout rerun; the final source hash is owned by `wp8-supp-number-check-final-layout.json`. Main located535digit occurrences and32numberwords; Supplement located4983digits and109numberwords. Unbound, ambiguous and mismatch counts are0;20mainpercentagedisplays,3330oldtypedfields,2080newSupplementfieldbindings,6oldmainnumeric-tablevectors and370oldSupplementnumericrows are checked. These are exhaustive occurrence/role inventories, not global equal-number searches.

Main12, Supplement8 and figure6softwarecorruptioncontrols passed. They reject swapped counts/rows, changed percentages/seed, added inline probabilities even with an already-existing equal value, missing generated input and omitted original table rows. The main deleted-row control first exposed a one-way-check defect, then passed only after full ordered-vector preservation was added. Full current source/report hashes and actual development outputs remain in the owning receipts.

Figure stdout:

```text
{
  "checked_utc": "2026-10-24T11:49:13.218577+00:00",
  "status": "PASS",
  "scope": "Source/byte identity and independently keyed saved-data-to-annotation traceability; actual final-page visual QA is separate.",
  "current_included_figures": [
    [
      "manuscript.tex",
      "figures/v7-endpoint-peak-example.pdf"
    ],
    [
      "manuscript.tex",
      "figures/v7-murphy-fx_hourly.pdf"
    ],
    [
      "manuscript.tex",
      "figures/v7-murphy-nyfed_weekly.pdf"
    ],
    [
      "manuscript.tex",
      "figures/v8-wp3-qr33-loss.pdf"
    ],
    [
      "supplement.tex",
      "figures/v8-wp3-qr4-loss.pdf"
    ]
  ],
  "old_figures_checked": 3,
  "all_MC_figures_checked": 6,
  "MC_cells_independently_checked": 432,
  "MC_numeric_annotations_checked": 864,
  "source_summary_sha256": "3de27c0f50a5b1882d4c8aba80d3fc8d2487972f22674d7e6e1423e62da663d0",
  "difference_count": 0,
  "differences": [],
  "forecasts_computed": 0,
  "new_scores_computed": 0,
  "new_simulations": 0,
  "global_numeric_presence_used_as_location_proof": false
}
```

The29reference entries and103supplied year/volume/issue/page/DOIfields were checked against owning primary metadata. All29citedkeys are used; missing/duplicate/uncitedkeys0. Hoogen indexed passages, unavailable fulltext and other reading limits remain explicit. Main23labels/23references andSupplement34labels/1reference have no unresolved or duplicate labels. See `wp8-reference-audit.{json,md}`, `wp8-reference-primary-snapshots.json` and `wp8-crossrefs-sealed-preservation.json`.

### Compile, visual failure correction and isolated package rebuild

Actual cached compiler route:

```text
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached submission-jof/manuscript.tex --outdir .scratch/revision-v8/wp8-main-final --keep-logs --keep-intermediates
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached submission-jof/supplement.tex --outdir .scratch/revision-v8/wp8-fraction-layout-250 --keep-logs --keep-intermediates
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached submission-jof/title-page.tex --outdir .scratch/revision-v8/wp8-title-final --keep-logs --keep-intermediates
```

**MISMATCH-WP8-LAYOUT, resolved before acceptance:** Actual28pageinitialSupplementpixels revealed overlapping exact fractions inS8–S10(p7–10). The originalFAILvisualrecord remains. Three arraystretcharguments alone were enlarged; no numeric result, fraction numerator/denominator, equation or table row was changed. The1.90preview remained tight;2.50produced a30pagecandidate. All30pages and all continuations were actually viewed, with detailviews; no material visual defect remains observed. Small table/paragraph widow and headinghyphenation notes remain. First guarded captionmatch failed before source write; no paper source changed in that attempt.

All20currentmainpages,30currentSupplementpages and1titlepage were actually viewed. `wp8-main-visual.json` and `wp8-supplement-visual-final.{json,md}` contain everypagepath/hash; originalfailedcandidate and bothintermediatepreviews remain. The current compiledmain/Supplement sources are `d8a20c6f...`/`7b78ee55...`. Logs have0error,0overfull,0undefinedreference,0missingglyph; underfullwarnings are counted, not concealed.

Actual independent document-pack check command:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 UV_OFFLINE=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pypdf python -B notes/revision-v8/check_wp8_package.py
```

Saved output summary:

```text
status: PASS
manuscript 20 all text/pixels identical True
supplement 30 all text/pixels identical True
title-page 1 all text/pixels identical True
child_peak_rss_bytes:249020416
financial_models_run:0
raw_financial_inputs_read:0
network_downloads:0
```

`wp8-isolated-package-check.json` binds all51rebuiltpagepixels to actuallyviewed originals andevery ZIPmember tocurrentbytes. The three previewaliases are exactnativePDFbytecopies. MainPDFSHA256`fc2b58f3a75fcc62da0631a6072e5a0a11eadff65d4c3e3dd0fe2f2bb1e51d3c`; Supplement`cdee84121670396eef1b1a99134209384b8e5409c52068c2776d9ebde797bb97`; sourceZIP`f9e72867dcede089469e0a4104f0374a43522acd4891659b1a452844791a7cb9`.

### Complete software suite and preservation

Actual command:

```text
python3 -B notes/revision-v8/run_full_pytest.py wp8-final
```

Verbatim complete-suite ending:

```text
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1328 passed, 1066 subtests passed in 100.65s (0:01:40) ============
```

Full unfiltered output: `wp8-final-pytest-output.txt`; invocation/environment/resource receipt: `wp8-final-pytest-receipt.json`.3205trackedfileswerecopied intoa freshisolateddirectory; no testselection/filter/skipwasadded. Actualelapsed101.056983834s; childpeakRSS333365248B; numericalthreads1; exit0. This local verification still has its owning localGitobjects, not an independently reproduced publicclone.

All1645originalresults/data/protocol/Pythonpaths matchv7baseline;0differences and`FINAL.md`unchanged. Sealedv8WP3/WP4/WP5result+driverpaths28/146/73alsohave0differences againsttheir completioncommits. Currenttrackedpathscope excludesactualscratch/rawFX/privatearrays/credentialfiles. No userfile was deleted or newsoftwareinstalled.

### Remaining non-acceptance capability and evidence mismatch

**MISMATCH-WP8-PUBLIC-HISTORY / BLOCKED financial replay in a fresh browser clone:** file-tree publication does not transferoriginal localdesigncommitobjects. FullorpartialGitobjectpublication would disclose a previouslyunpublishedmachine-localidentity, so no suchbundle/packwascreated orpublished. Sealeddrivers andhistory-dependentdocumenttests are not weakened. Current documentZIPcompilation and savedfieldinspection are separate fromcompletefinancialreplay. This limitation andpendingauthorchoice are explicitin`REPRODUCING.md`, currentguides andAUTHOR-TODO. It is not a new scientific failure or a claim that numericalresults were independently reproduced.

**MISMATCH-TIMING, retained:** the11:55:15selfcheck actuallyran12:03:27.388881Z(delay492.388881s), followedby12:05:19.247730Z(delay4.247730s). No completeadditional600sslot wasmissed inthose records, but strict punctual10mincadence mustnotbeclaimed. Selfchecksgiveactualtimes; no idleorparallelagenttime isaddedasresearch.

AllWP8requiredartifactgatesPASS; `wp8-acceptance.json` is the aggregate. WP9 remains unstarted until this completioncommit. The10hourgoal remainsactive until17:55:15Z; whole-goalcompletion isnotclaimed.

WP8 writer correction: the first ledger aggregation completed its evidence append but its state update raised `NameError: load is not defined`. All actual acceptance gates and saved acceptance JSON had already passed; no research artifact changed. The state update was corrected and the single WP8 completion commit amended before starting WP9.
