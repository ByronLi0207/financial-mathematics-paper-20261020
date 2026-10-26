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
