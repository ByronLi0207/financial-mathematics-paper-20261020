# Revision v7 execution ledger

Authority: revision-plan-v7-final.md. S1–S10 must pass sequentially. No new financial models, data, tests of hypotheses, or tuning.

## S1 — IN PROGRESS

Local source revision-v4-jof: 29190137a1a0617b9d4f70cc28175ee14a57aba6. Its tree equals fetched origin/revision-v4-jof 095ba7ff52eca8aa03e5ad552478e76714b39c6e. Supervisor source: 0ebc6e54ee3682315670a641e8783fc15c3660f4.

```text
$ git fetch origin
[no output; exit 0]
$ git fetch origin +refs/heads/revision-v4-jof:refs/remotes/origin/revision-v4-jof +refs/heads/codex/supervisor-revision-20261023:refs/remotes/origin/codex/supervisor-revision-20261023
[no output; exit 0]
$ git switch -c revision-v7-final revision-v4-jof
Switched to a new branch 'revision-v7-final'
$ git merge --no-ff --no-commit origin/codex/supervisor-revision-20261023
Auto-merging README.md
Auto-merging round2_panel_run.py
CONFLICT (add/add): Merge conflict in round2_panel_run.py
Auto-merging round2_panel_sources.py
CONFLICT (add/add): Merge conflict in round2_panel_sources.py
Automatic merge failed; fix conflicts and then commit the result.
```

Resolution: the original runner remains at round2_panel_run.py; the complete supervisor E5 runner is copied byte-for-byte to supervisor_e5_panel_run.py (SHA-256 00042a159be2921a7d88be4b07ae95b75d06dc4b3713a941131b548dd9e55dfb). Both loader versions have identical align_source ASTs; the original loader preserves its additional acquisition helpers, which were not run. No parameter or result value changed. Both required manuscript trees and submission-jof remain.

The first README preservation assertion failed: Git's automatic merge omitted three old passages. A subsequent command still created merge commit 832563b before that assertion had been resolved. S1 was never marked PASS. All omitted lines have now been restored under an explicitly historical heading; all nonblank source lines from both versions are present. This correction does not alter any existing numerical result.

The 53 pre-existing .bak files are preserved with unchanged hashes. Exact entries in local .git/info/exclude keep them out of publication without deleting files.

Full merged-tree pytest, dual ancestry and clean status remain pending. S2–S10 have not begun.

### Integration gate correction before S1 acceptance

The first all-discovered suite passed (991 tests; 1,066 subtests, 87.33 s), but read-only integration review found that AST identity alone did not preserve the supervisor R6 whole-file loader gate. S1 therefore remained IN PROGRESS. The final resolution restores both supervisor files exactly at canonical paths and saves both earlier implementations unchanged under `legacy_` filenames. The earlier test imports that legacy segment; all cases and assertions are unchanged. The existing prospective binding is historical and stays unchanged, with its path/version routing documented in README. No full-file frozen hash or scientific result is edited. The duplicate supervisor E5 source copy has identical bytes to the canonical runner, so its recorded canonical execution-source identity resolves to the same bytes. A fresh full suite is required after this integration correction.

### Final full-suite execution evidence

```text
$ /Users/bingyouli/.local/bin/uv run --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B -m pytest -p no:cacheprovider -v --basetemp /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v7/s1/pytest-temp-2
ndependentFrontierTests::test_nonfinite_negative_boolean_and_fraction_tokens_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_same_byte_source_hash_and_duplicate_cell_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_wrong_crossing_wrong_domination_and_open_winner_are_rejected PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_attempt_dotdot_escape_does_not_create_outside_receipt PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_constant_decimal_mean_is_preserved_exactly PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_exact_table_matching_reports_all_changed_fields_and_duplicate_rows PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_future_values_cannot_change_pre_refit_reports_but_do_change_target PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_integer_ranks_and_minimizer_endpoint_contract PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_no_overwrite_and_scratch_boundary PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_oracle_rejects_missing_history_duplicate_origins_and_incomplete_targets PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_saved_arrays_compare_every_issue_and_count_exact_disagreements PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============= 991 passed, 1066 subtests passed in 84.82s (0:01:24) =============
```

All 2,503 merged tracked working files were copied before discovery; no test filters, exclusions or reduced module lists. Original output: notes/v7/s1-pytest-output.txt. Invocation, actual elapsed time and child RSS: notes/v7/s1-pytest-receipt.json. Offline cached environment, one numerical thread; PYTHONPATH unset. Final acceptance commit and clean status pending.

## S1: PASS

Both source histories are ancestors of the merge (notes/v7/s1-git-graph.txt and s1-invariants.json), all required directories and both README sources are preserved, and all original result/data files are unchanged. The corrected merged tree passed the full discovered suite: **991 passed, 1,066 subtests passed**, 84.82 s pytest time; actual subprocess time 85.30 s, peak child RSS 325,632,000 bytes.

```text
$ git commit -m 'Preserve versioned replay entries and verify complete v7 merge suite'
[revision-v7-final 1f1f354] Preserve versioned replay entries and verify complete v7 merge suite
$ git status --short
[no output; exit 0]
```

S1 acceptance is complete. S2 may now begin.

## S2: PASS

The evidence table contains 1,186 exact source records from 42 existing files. FX, both original primaries, matched controls, two FX periods, DM/HLN/adjustment-family versions, coverage/Murphy/preferences, all v6 robustness inventories, expanded-panel and one-SE results, formal propositions and all saved simulation cases have field-level source bindings. No model, new data, hypothesis test, percentage, median or new p-value was computed.

```text
$ python3 notes/v7/check_evidence.py --write
{
  "status": "PASS",
  "rows_checked": 1186,
  "source_files_checked": 42,
  "mismatches": 0,
  "failures": [],
  "new_models": 0,
  "new_hypothesis_tests": 0,
  "new_data": 0
}
```

The first partial run found two duplicate metadata row IDs, not numerical disagreements. These were disambiguated as PRIMARY_CONTRAST IDs without changing values or sources. The final script reads every native JSON value / exact CSV token / exact saved passage and verifies source existence, selector uniqueness and value/type equality. Source fingerprints are separately saved.

Evidence: notes/v7/evidence-table.md, evidence-source-fingerprints.json, evidence-verification.json, evidence-parts/{metadata,fx,panel,theory}.json. MISMATCH handling: notes/v7/mismatches.md and the three scoped readbacks. In particular, the universal-failure reading is rejected; the 20.6 ratio is kept on its H24 legacy pair; aggregates, different inventories and adjustment families stay distinct. S3 may now begin.

## S3: PASS

The final English thesis and Chinese interpretation are in notes/v7/thesis.md. Every clause identifies its exact S2 records; the machine-readable map is thesis-clauses.json. The proposed universal-failure wording is qualified using existing adverse and favorable cells; no outcome is discarded. Weekly sources are called position-category aggregates. Title 1 is selected; titles 2 and 3 are saved for the author.

```text
$ python3 notes/v7/check_thesis.py
{
  "status": "PASS",
  "clauses_checked": 7,
  "clauses_without_evidence": 0,
  "missing_evidence_ids": [],
  "all_referenced_rows_exist": true
}
```

The saved check reads the S2 records, resolves each mapped ID, asserts every clause has bindings and reports missing IDs. Evidence/narrative MISMATCH handling is explicitly described in the thesis. S4 may now begin.

## S4: PASS

Three fixed-template five-sentence passages are inserted in the current main TeX and saved in notes/v7/contributions.{json,md}. Each begins with We formalize / We find / We show, describes the executed approach, supplies a key saved numerical result, distinguishes specific nearest work and names a main evidence location. The current transport section now explicitly carries the existing expanded-menu and earlier-period results so these contribution locations are real. S5 will reorganize, rather than invent, their target locations.

```text
$ python3 notes/v7/check_contributions.py
{
  "status": "PASS",
  "sentence_counts": {
    "C1": 5,
    "C2": 5,
    "C3": 5
  },
  "main_passages_present": {
    "C1": true,
    "C2": true,
    "C3": true
  },
  "evidence_locations": {
    "C1": "Section 4; Supplement S11 and Table S15",
    "C2": "Section 8, integration paragraph; Table 6",
    "C3": "Sections 6\u20139; Figure 3 and Table 6; preference discussion Section 7"
  },
  "missing_evidence_ids": [],
  "forbidden_phrase_counts_current_main": {
    "merely": 0,
    "only an application": 0,
    "using mature methods": 0
  },
  "priority_claims_added": 0
}
```

Current evidence locations: C1 Section 4 plus Supplement S11/Table S15; C2 Section 8 and Table 6; C3 Sections 6–9, Figure 3, Table 6 and the Section 7 preference discussion. Figures, proof qualifications and all pre-existing adverse result files remain. No first/novel priority claim was introduced, and no new priority search was needed. The closest works already contain endpoint methods, financial path extrema and joint score/coverage evaluation.

**MISMATCH M7:** Duffie2023 is not capacity-only: existing Section 6 / Appendix E evidence includes out-of-sample PnL quantiles. The contribution now contrasts its target explicitly. See notes/v7/s4-source-comparison.md and mismatches.md. MaxVaR metadata has an older-record conflict reserved for S7 verification. S5 may now begin.

## S5: PASS

The manuscript now follows the ten required sections, with exactly three related-literature prose paragraphs and a seven-paper/six-dimension positioning table plus this study. Main methods use descriptive names; the method table maps existing codes. Propositions retain their mathematics and correct numbered cross-references; proofs and detailed diagnostics are in the compact Supplement. Every main and Supplement table/figure caption ends with its interpretation.

All 23 original v6 submission files were copied byte-for-byte to manuscript/revision-v6-preserved/ from source commit 2919013 before rewriting. The original 94-page supplement and every adverse result remain accessible through EXTENDED_RESULTS.md; no source/result file was removed or overwritten. The compact Supplement itself carries complete simulation, panel and relevant unsuccessful-cell tables.

### Deterministic real-window rule and actual output

The script comments, written before execution, fix the earliest eligible original Treasury H6/W260 issue with endpoint <= **saved** fixed-window historical headroom report < sampled peak. It reads the existing saved capacities and source observations; it does not compute a forecast or choose a favorable gap.

```text
$ /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B notes/v7/select_example.py
{
  "status": "PASS",
  "saved_trace_sha256": "aea48830e43da898c389a9f36da9848953fa62b191f9b3a0c6e7e174ebc15dfa",
  "source_sha256": "9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb",
  "existing_illustration_identical": true,
  "forecasts_computed": 0,
  "models_fitted": 0,
  "new_data": 0
}
{
  "origin": 408,
  "horizon": 6,
  "report": 73139.0,
  "peak": 74397.0,
  "endpoint_absolute": 48144.0
}
```

Only existing saved score-display grids are used for the two Murphy figures. The three figures are now native LaTeX vector outputs with descriptive legends, compiled with the existing Tectonic executable and cached components. No plotting software was installed.

### Existing-field additions required by this presentation

Nineteen missing original source fields (Treasury sparse-grid coverage and the existing selected example) were appended to the S2 table before use. Every original S2 row and source fingerprint remained unchanged. The combined check now reads 1,205 records in 43 files with zero mismatches. This is extra saved-field readback, not a new test, forecast or sample.

```text
$ python3 notes/v7/check_evidence.py --append-table
{ "status": "PASS", "rows_checked": 1205, "source_files_checked": 43, "mismatches": 0, "failures": [], "new_models": 0, "new_hypothesis_tests": 0, "new_data": 0 }
{ "existing_rows_changed": 0, "existing_source_changes": 0, "new_saved_fields_appended": 19 }
```

### Pagination and word-budget acceptance

Actual final S5 pagination commands used the existing compiler:

```text
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached supplement.tex --outdir .scratch/revision-v7/s5/attempt3-supplement --keep-logs --keep-intermediates
[exit 0; original full output: notes/v7/s5-compilation/supplement-compile-output.txt]
$ /Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile --only-cached manuscript.tex --outdir .scratch/revision-v7/s5/attempt3-manuscript --keep-logs --keep-intermediates
[exit 0; original full output: notes/v7/s5-compilation/main-compile-output.txt]
$ /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B notes/v7/check_s5_budget.py
{
  "section_counts": [
    {
      "section": "Introduction",
      "words": 808,
      "limit": 1300,
      "pass_limit": true
    },
    {
      "section": "Related literature",
      "words": 292,
      "limit": 900,
      "pass_limit": true
    },
    {
      "section": "The forecast target",
      "words": 518,
      "limit": 1000,
      "pass_limit": true
    },
    {
      "section": "Data",
      "words": 246,
      "limit": 600,
      "pass_limit": true
    },
    {
      "section": "Forecasting methods",
      "words": 339,
      "limit": 800,
      "pass_limit": true
    },
    {
      "section": "Evaluation design",
      "words": 401,
      "limit": 800,
      "pass_limit": true
    },
    {
      "section": "Results",
      "words": 1021,
      "limit": 2000,
      "pass_limit": true
    },
    {
      "section": "Implications for model validation",
      "words": 254,
      "limit": 500,
      "pass_limit": true
    },
    {
      "section": "Limitations",
      "words": 252,
      "limit": 500,
      "pass_limit": true
    },
    {
      "section": "Conclusion",
      "words": 263,
      "limit": 350,
      "pass_limit": true
    }
  ],
  "total_words": 4394,
  "total_limit": 8800,
  "captioned_main_tables": 6,
  "main_figures": 3,
  "main_pages": 16,
  "supplement_pages": 20,
  "supplement_page_limit": 30,
  "main_pdf_producer": "xdvipdfmx (0.1)",
  "supplement_pdf_producer": "xdvipdfmx (0.1)",
  "status": "PASS"
}
```

The saved budget script conservatively includes non-table source text and figure captions, excluding references and captioned tables. All ten section limits, total words, six main tables, three figures and twenty-page Supplement pass. Main pagination is sixteen pages at this checkpoint.

Earlier compilation attempts exposed a glued table-ending command, an uncached decorative proof symbol, an unused main longtable/caption dependency and an uncached bibliography style. These were repaired within the existing LaTeX path: group delimiters, text QED, removal of the unused package, and the supervisor line's native thebibliography convention. No scientific values changed. References remain existing provisional text until S7; remaining table-width warnings are reserved for S8 layout repair. S5 is a structure/budget gate, not final compilation or visual acceptance. Actual compile receipts peak at 244,760,576 child RSS bytes; no new software or data were acquired. S6 may now begin.

## S6: PASS

The same scope/tokenizer compares the exact preserved v6 text with the current main source. Citation years count as numbers. Decimals and scientific values are not split at their internal periods. Headings are excluded as headings in both versions; this removes a false extra sentence at each contribution label. All required thresholds pass.

```text
$ python3 notes/v7/writing_metrics.py --output notes/v7/s6-final-metrics.json --summary --require-pass
{
  "before": {
    "abstract_words": 215,
    "abstract_numbers": 9,
    "main_sentences": 400,
    "main_words": 6713,
    "mean_sentence_words": 16.7825,
    "sentences_over35": 8,
    "over35_percent": 2.0,
    "negation_sentences": 80,
    "negation_percent": 20.0,
    "max_numbers_per_sentence": 10,
    "pass_quantitative": false,
    "paragraphs_over6": 11,
    "banned_total": 71
  },
  "after": {
    "abstract_words": 139,
    "abstract_numbers": 4,
    "main_sentences": 215,
    "main_words": 4243,
    "mean_sentence_words": 19.73488372093023,
    "sentences_over35": 0,
    "over35_percent": 0.0,
    "negation_sentences": 5,
    "negation_percent": 2.3255813953488373,
    "max_numbers_per_sentence": 2,
    "pass_quantitative": true,
    "paragraphs_over6": 0,
    "banned_total": 0
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
    }
  }
}
```

| Metric | Before | After |
|---|---:|---:|
| Abstract words | 215 | 139 |
| Abstract numbers | 9 | 4 |
| Mean sentence words | 16.7825 | 19.73488372093023 |
| Sentences over 35 words (%) | 2.0 | 0.0 |
| Sentences with negation (%) | 20.0 | 2.3255813953488373 |
| Maximum numbers per sentence | 10 | 2 |
| Paragraphs exceeding six sentences | 11 | 0 |
| Banned terms / phrases | 71 | 0 |

The full audit and excluded headings are in notes/v7/s6-final-metrics.json; the qualitative checks are in s6-writing-audit.md. Citation-dense sentences were split without changing their sources. C1 has six sentences; C2 and C3 have five. All numerical outcomes and adverse cases remain unchanged.

### Abstract before

> Endpoint forecasts do not determine the maximum position reached along a financial path. We study the upper quantile of a sampled absolute net-position peak with a known current-position floor, explicitly matured training labels and matched-history controls. We state a pointwise floor projection, a classical absolute-displacement endpoint-to-peak bound and common-pool construction distances; none creates a new distribution-free coverage guarantee for fitted reports. Three findings delimit the empirical value. The original FX primary lowers mean loss by 12.660% on the previously inspected record. Its separately identified matched-history short-horizon regression lowers mean pinball loss by 14.77% but increases breaches from 360 to 376. Elementary-score curves for the distinct original FX primary cross, ruling out dominance for that pair. Horizon-specific short-history FX regression reports cross on 640/6625 origins despite ordered realized targets. The separately fitted Treasury regression primary raises loss by 50.79%, and the additional aggregate panel yields only 3/48 lower-loss original-regression cells. Exact gain decomposition, label-timing controls and additional mature benchmarks are post-result / exploratory, with mixed directions, failed fits and incomplete upper-target evidence retained. The Treasury exercise replays a downloaded vintage by economic date; compatible unseen-dealer and prospective public-release validation remain outstanding. The evidence supports joint validation of accuracy, calibration, report coherence and measurement compatibility, rather than a universal forecasting or funding advantage.

### Abstract after

> Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. Long-history FX regression changes matched loss by -14.77% and -16.62% in the later and earlier periods. Its later advantage survives the evaluated finite delayed coverage correction. Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.

### Introduction opening before

> Dealers absorb customer order imbalances while managing inventory risk and scarce balance-sheet capacity. Inventory affects optimal dealer pricing (Ho and Stoll, 1981), FX dealing (Lyons, 1995), and observed inventory adjustment in dealership markets (Hansch, Naik and Viswanathan, 1998). Treasury intermediation likewise depends on dealer capacity (Duffie et al., 2023). A forecast of the maximum recorded position magnitude over a future horizon may support monitoring of the measured position: an endpoint can return toward its starting value after an intervening large position. Translating that monitoring signal into a particular margin or financing decision requires the corresponding contractual and balance-sheet inputs. The inventory literature motivates monitoring; this passive forecast comparison identifies no change in optimal quotes, hedges or realized funding requirements.

### Introduction opening after

> A position can finish inside its limit after exceeding that limit during the intervening period, as Figure illustrates. For a market maker, the relevant forecast therefore concerns the largest exposure before the next review, rather than the endpoint alone. The distinction changes the response variable, the observations available for training, and the interpretation of successful prediction. We study how established historical and conditional forecasts perform when every method targets this same sampled absolute-position peak.

### Substantive definition correction

A draft had confused the filtered-path benchmark with ordered-residual mean replay. Inspection of the archived executed source restores the GARCH-standardized iid empirical-innovation definition.

```text
$ shasum -a 256 round2_filtered.py
c01b675d5a284ffc92890b78d043362edcc329f5d1ef824e81db43cef3f0aad7  round2_filtered.py
```

This exactly matches results/revision-20261023/round2/baselines/nyfed_weekly-h6-w260-FHS.json /code_sha256/round2_filtered.py. No forecasting, simulation, hypothesis test or data change was made. S7 may now begin.

## S7: PASS

Each cited work was checked against current primary publisher/DOI/institution records, with page-endpoint/cover checks where metadata were shortened. The raw per-group records include access limits; whole-paper identity is verified for every retained reference, while unsupported DOI fields are omitted. FR 2004’s two actual dated documents are separate APA entries. The changing NYFed data tool has n.d. plus retrieval date; its experiment’s snapshot/economic dates are unchanged. No unused current bibliography entry remains; the complete old bibliography stays preserved.

### Per-reference verification table

# S7 reference verification

Metadata are verified against the linked owning/publisher records; empty optional DOI fields are deliberately omitted. This is not a full-text-method replication claim.

| Key | Status | Author/year/venue/volume/issue/pages | DOI | Evidence |
|---|---|---|---|---|
| arjani2020 | verified | Arjani, N.; Li, F.; Sabetti, L.; 2020; Payments Canada; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.payments.ca/sites/default/files/discussion_paper_monitoring_intraday_liquidity_risks_in_a_real_time_gross_settlement_system.pdf) |
| barone1999 | verified | Barone-Adesi, G.; Giannopoulos, K.; Vosper, L.; 1999; Journal of Futures Markets; 19; 5; 583–602 | 10.1002/(SICI)1096-9934(199908)19:5<583::AID-FUT5>3.0.CO;2-S | [source](https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291096-9934%28199908%2919%3A5%3C583%3A%3AAID-FUT5%3E3.0.CO%3B2-S), [source](https://api.crossref.org/works/10.1002%2F%28SICI%291096-9934%28199908%2919%3A5%3C583%3A%3AAID-FUT5%3E3.0.CO%3B2-S) |
| fr2004_2013 | corrected | Board of Governors of the Federal Reserve System; 2013; Board of Governors of the Federal Reserve System; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.federalreserve.gov/apps/reportingforms/Report/Index/FR_2004), [source](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=f555fe11-e149-479b-8088-4ed4e9ae1206), [source](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=950ab256-b485-4586-99b0-b27eb205fdfa) |
| fr2004_2024 | corrected | Board of Governors of the Federal Reserve System; 2024; Board of Governors of the Federal Reserve System; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.federalreserve.gov/apps/reportingforms/Report/Index/FR_2004), [source](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=f555fe11-e149-479b-8088-4ed4e9ae1206), [source](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=950ab256-b485-4586-99b0-b27eb205fdfa) |
| boudoukh2004 | corrected | Boudoukh, J.; Richardson, M.; Stanton, R.; Whitelaw, R. F.; 2004; Journal of Investment Management; 2; 3; 1–6 | omitted: unverified / none supplied | [source](https://pages.stern.nyu.edu/~rwhitela/papers/maxvar%20joim04.pdf), [source](https://joim.com/year/2004/) |
| christ1998 | corrected | Christoffersen, P. F.; 1998; International Economic Review; 39; 4; 841–862 | 10.2307/2527341 | [source](https://doi.org/10.2307/2527341), [source](https://api.crossref.org/works/10.2307%2F2527341), [source](https://users.ssc.wisc.edu/~behansen/718/Christoffersen1998.pdf) |
| dm1995 | corrected | Diebold, F. X.; Mariano, R. S.; 1995; Journal of Business & Economic Statistics; 13; 3; 253–263 | 10.1080/07350015.1995.10524599 | [source](https://doi.org/10.1080/07350015.1995.10524599), [source](https://api.crossref.org/works/10.1080%2F07350015.1995.10524599) |
| duffie2023 | corrected | Duffie, D.; Fleming, M. J.; Keane, F. M.; Nelson, C.; Shachar, O.; Van Tassel, P.; 2023; Federal Reserve Bank of New York Staff Reports; n.a.; n.a.; n.a. | 10.59576/sr.1070 | [source](https://www.newyorkfed.org/research/staff_reports/sr1070), [source](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf) |
| ehm2016 | verified | Ehm, W.; Gneiting, T.; Jordan, A.; Krüger, F.; 2016; Journal of the Royal Statistical Society Series B: Statistical Methodology; 78; 3; 505–562 | 10.1111/rssb.12154 | [source](https://academic.oup.com/jrsssb/article-abstract/78/3/505/7040984), [source](https://academic.oup.com/jrsssb/issue/78/3), [source](https://api.crossref.org/works/10.1111%2Frssb.12154) |
| engle2004 | verified | Engle, R. F.; Manganelli, S.; 2004; Journal of Business & Economic Statistics; 22; 4; 367–381 | 10.1198/073500104000000370 | [source](https://www.tandfonline.com/doi/abs/10.1198/073500104000000370), [source](https://www.tandfonline.com/toc/ubes20/22/4), [source](https://api.crossref.org/works/10.1198%2F073500104000000370) |
| nyfeddata | corrected | Federal Reserve Bank of New York; n.d.; Federal Reserve Bank of New York; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics), [source](https://www.newyorkfed.org/privacy/termsofuse.html) |
| gw2006 | verified | Giacomini, R.; White, H.; 2006; Econometrica; 74; 6; 1545–1578 | 10.1111/j.1468-0262.2006.00718.x | [source](https://api.crossref.org/works/10.1111/j.1468-0262.2006.00718.x), [source](https://doi.org/10.1111/ecta.2006.74.issue-6) |
| gibbs2021 | corrected | Gibbs, I.; Candès, E. J.; 2021; Advances in Neural Information Processing Systems; 34; n.a.; 1660–1672 | omitted: unverified / none supplied | [source](https://proceedings.neurips.cc/paper_files/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html), [source](https://proceedings.neurips.cc/paper_files/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Bibtex.bib), [source](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf) |
| gneiting2011 | verified | Gneiting, T.; 2011; Journal of the American Statistical Association; 106; 494; 746–762 | 10.1198/jasa.2011.r10138 | [source](https://api.crossref.org/works/10.1198/jasa.2011.r10138) |
| hln1997 | verified | Harvey, D.; Leybourne, S.; Newbold, P.; 1997; International Journal of Forecasting; 13; 2; 281–291 | 10.1016/s0169-2070(96)00719-4 | [source](https://api.crossref.org/works/10.1016/S0169-2070(96)00719-4) |
| holm1979 | verified | Holm, S.; 1979; Scandinavian Journal of Statistics; 6; 2; 65–70 | omitted: unverified / none supplied | [source](https://www.jstor.org/stable/i412579), [source](https://www.jstor.org/stable/4615733) |
| hull1998 | corrected | Hull, J.; White, A.; 1998; The Journal of Risk; 1; 1; 5–19 | 10.21314/jor.1998.001 | [source](https://api.crossref.org/works/10.21314/JOR.1998.001), [source](https://www.risk.net/journal-of-risk/volume-1-number-1-fall-1998), [source](https://www.risk.net/ja/node/2161156) |
| koenker1978 | verified | Koenker, R.; Bassett, G., Jr.; 1978; Econometrica; 46; 1; 33–50 | 10.2307/1913643 | [source](https://api.crossref.org/works/10.2307/1913643), [source](https://www.jstor.org/stable/1913643), [source](https://people.eecs.berkeley.edu/~jordan/sail/readings/koenker-bassett.pdf) |
| kupiec1995 | verified | Kupiec, P. H.; 1995; The Journal of Derivatives; 3; 2; 73–84 | 10.3905/jod.1995.407942 | [source](https://api.crossref.org/works/10.3905/jod.1995.407942) |
| dataset | verified | Lindsay, D.; 2020; Kaggle; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.kaggle.com/api/v1/datasets/view/davidlindsay1979/net-position-time-series-dataset), [source](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset) |
| mcneilfrey2000 | verified | McNeil, A. J.; Frey, R.; 2000; Journal of Empirical Finance; 7; 3–4; 271–300 | 10.1016/s0927-5398(00)00012-8 | [source](https://api.crossref.org/works/10.1016/S0927-5398(00)00012-8) |
| meinshausen2006 | corrected | Meinshausen, N.; 2006; Journal of Machine Learning Research; 7; 35; 983–999 | omitted: unverified / none supplied | [source](https://www.jmlr.org/papers/v7/meinshausen06a.html), [source](https://jmlr.org/beta/papers/v7/meinshausen06a.html), [source](https://jmlr.org/papers/v7/meinshausen06a.bib) |
| nw1987 | verified | Newey, W. K.; West, K. D.; 1987; Econometrica; 55; 3; 703–708 | 10.2307/1913610 | [source](https://www.jstor.org/stable/i332769), [source](https://www.jstor.org/stable/1913610), [source](https://users.ssc.wisc.edu/~behansen/718/NeweyWest1987.pdf) |
| petrunia2019 | corrected | Petrunia, R.; Sabetti, L.; Voia, M.; 2019; Payments Canada; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.payments.ca/sites/default/files/tail_risk_in_the_automated_clearing_settlement_system_acss.pdf) |
| sussman2023 | corrected | Sussman, E.; 2023; Annals of Functional Analysis; 14; 1; Article 22 | 10.1007/s43034-022-00225-1 | [source](https://link.springer.com/article/10.1007/s43034-022-00225-1), [source](https://dspace.mit.edu/entities/publication/c7fe2a31-9850-43f0-853f-8a0dc66cea2d) |
| hoogen2017 | corrected | van den Hoogen, S.; 2017; Delft University of Technology; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://www.tudelft.nl/ewi/over-de-faculteit/afdelingen/applied-mathematics/statistics/alumni), [source](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1), [source](https://resolver.tudelft.nl/uuid:1c0c4545-bb07-4916-aa37-1d4bea3b7872) |
| wisniewski2020 | verified | Wisniewski, W.; Lindsay, D.; Lindsay, S.; 2020; Proceedings of the Ninth Symposium on Conformal and Probabilistic Prediction and Applications; 128; n.a.; 285–301 | omitted: unverified / none supplied | [source](https://proceedings.mlr.press/v128/wisniewski20a.html), [source](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf) |
| wisniewski2024 | corrected | Wisniewski, W. J.; 2024; Royal Holloway, University of London; n.a.; n.a.; n.a. | omitted: unverified / none supplied | [source](https://pure.royalholloway.ac.uk/en/publications/net-position-and-retail-trader-behaviour-implications-for-market-/), [source](https://pure.royalholloway.ac.uk/files/63018039/2024WisniewskiWJWphd.pdf) |

### Actual citation/list and declaration check

```text
$ python3 notes/v7/build_references_v7.py
{
  "status": "PASS",
  "cited_keys": 28,
  "reference_entries": 28,
  "missing_references": [],
  "unused_entries": [],
  "verified": 14,
  "corrected": 14,
  "unverified": 0,
  "dois_printed": 15,
  "doi_omitted": 13,
  "author_fields_filled": 0
}
$ python3 notes/v7/check_references.py
{
  "status": "PASS",
  "cited": 28,
  "bib_entries": 28,
  "printed_entries": 28,
  "missing": [],
  "unused": [],
  "print_mismatches": [],
  "metadata_entries_with_primary_evidence": 28,
  "author_placeholders": {
    "Author information": true,
    "ORCID": true,
    "Funding": true,
    "Competing interests": true,
    "AI statement": true
  },
  "author_declarations_completed": 0
}
```

The final reference text uses APA author-initials, author-year labels, sentence-case titles and verified publication fields. It follows the supervisor’s existing native thebibliography compilation path, with a standard structured references.bib alongside it; no style download or software installation. Data Availability reports Kaggle’s actual “Data files © Original Authors” label, excludes FX observations/private forecast vectors, and describes continuing NYFed source conditions. Code Availability gives the authorized GitHub repository. All five author-provided fields remain literal placeholders; the title page also keeps its author/contact fields unfilled.

Kaggle metadata: HTTP 200, 4,552-byte public JSON; no raw observations downloaded. Official NYFed data and terms pages were read. See data-availability-verification.md and kaggle-metadata-verification.json. The inherited aggregate README already supplies the required attribution and was not changed.

**MISMATCH M8:** older MaxVaR pages 14–19 are superseded by the owning final-layout article’s 1–6. Other metadata corrections and version distinctions are documented per source, not silently guessed. Fifteen DOI fields are verified; thirteen entries omit DOI. No whole work remains unverified. S6 quantitative requirements were rechecked after author-year labels changed and still pass. S8 may now begin.

## S8: PASS

The main manuscript, compact Supplement and title page are actual LaTeX/XeTeX outputs from the existing app-bundled Tectonic executable. All compilations use --only-cached; no software, class, style or font download/install occurred. Final native producer is xdvipdfmx (0.1), not ReportLab. The generated vector figures also use native LaTeX.

Compilation commands and exact outputs are in notes/v7/s8-compilation/*-receipt.json and *-output.txt; complete final native logs are *-log.txt. Their final checks and file identities are:

```text
{
  "status": "PASS",
  "documents": {
    "manuscript": {
      "pages": 17,
      "producer": "xdvipdfmx (0.1)",
      "sha256": "34ab3ce8465ab66e706d226f8b643f1f54672799d6e6418fde4bf89b9304308d",
      "source_sha256": "e900bc34a25b9f11e03b4ae8ca34bc7d2af76eb8cff3f4f4f43a2357ecc27728",
      "overfull": 0,
      "undefined_references": 0,
      "missing_characters": 0,
      "returncode": 0
    },
    "supplement": {
      "pages": 20,
      "producer": "xdvipdfmx (0.1)",
      "sha256": "8b2be84f711b1873c6911bcbde75dbc97b7afba59af34060c7908bf57e803afb",
      "source_sha256": "fa3051bf6e39424beca41ed881b0e26026e1da6c430902e3ac88bed953e46a58",
      "overfull": 0,
      "undefined_references": 0,
      "missing_characters": 0,
      "returncode": 0
    },
    "title-page": {
      "pages": 1,
      "producer": "xdvipdfmx (0.1)",
      "sha256": "715df8004aefe1d85e0580a1a4ed8ed8f445320af25ff96eabd95a26c1a74280",
      "source_sha256": "0d4102c4126f15c662cbd3d8178e09bdfda3cb5d5daf6b1c5d2f1f43005bdc53",
      "overfull": 0,
      "undefined_references": 0,
      "missing_characters": 0,
      "returncode": 0
    }
  },
  "pages_rendered_and_visually_reviewed": 38,
  "review_files": [
    "s8-main-visual-review.json",
    "s8-supp-pages01-10-visual.json",
    "s8-supp-pages11-20-visual.json",
    "s8-root-visual.json"
  ],
  "software_installed": 0,
  "compiler_path": "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
  "only_cached": true,
  "fallback_used": false,
  "nonblocking_style_notes": "Tight proposition-heading space and expanded justified reference spacing; dense exact rational frontier columns remain legible."
}
```

The final native log has zero errors, undefined references, overfull boxes and missing-character warnings in each document. Underfull reference/table whitespace notices are preserved in the logs and were checked visually; they do not hide clipping. Main proof labels resolve to Propositions 1 and 2.

### Exact compilation-output tails

```text
manuscript
rfull \hbox (badness 1237) in paragraph at lines 378--379
warning: manuscript.tex:383: Underfull \hbox (badness 10000) in paragraph at lines 382--383
warning: manuscript.tex:383: Underfull \hbox (badness 10000) in paragraph at lines 382--383
warning: manuscript.tex:383: Underfull \hbox (badness 10000) in paragraph at lines 382--383
warning: manuscript.tex:413: Underfull \hbox (badness 7540) in paragraph at lines 412--413
warning: manuscript.tex:413: Underfull \hbox (badness 2326) in paragraph at lines 412--413
warning: manuscript.tex:413: Underfull \hbox (badness 1490) in paragraph at lines 412--413
warning: warnings were issued by the TeX engine; use --print and/or --keep-logs for details.

```

```text
supplement
\hbox (badness 10000) in paragraph at lines 722--722
warning: supplement.tex:723: Underfull \hbox (badness 10000) in paragraph at lines 723--723
warning: supplement.tex:740: Underfull \hbox (badness 10000) in paragraph at lines 740--740
warning: supplement.tex:741: Underfull \hbox (badness 10000) in paragraph at lines 741--741
warning: supplement.tex:742: Underfull \hbox (badness 10000) in paragraph at lines 742--742
warning: supplement.tex:743: Underfull \hbox (badness 10000) in paragraph at lines 743--743
warning: supplement.tex:1337: Underfull \hbox (badness 1681) in paragraph at lines 1329--1337
warning: warnings were issued by the TeX engine; use --print and/or --keep-logs for details.

```

```text
title-page
note: "version 2" Tectonic command-line interface activated
note: using only cached resource files
note: Running TeX ...
note: Rerunning TeX because "title-page.aux" changed ...
note: Running xdvipdfmx ...
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v7/s8/compile-4-title-page/title-page.aux` (652 B)
note: Not writing `title-page.out`: it would be empty.
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v7/s8/compile-4-title-page/title-page.pdf` (10.013671875 KiB)
note: Writing `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v7/s8/compile-4-title-page/title-page.log` (8.7265625 KiB)

```

### Rendering and visual acceptance

```text
$ pdftoppm -png -r 120 .scratch/revision-v7/s8/compile-5-manuscript/manuscript.pdf .scratch/revision-v7/s8/main-page
[exit 0; 17 page PNGs]
$ pdftoppm -png -r 120 .scratch/revision-v7/s8/compile-4-supplement/supplement.pdf .scratch/revision-v7/s8/supp-page
[exit 0; 20 page PNGs]
$ pdftoppm -png -r 120 .scratch/revision-v7/s8/compile-4-title-page/title-page.pdf .scratch/revision-v7/s8/title-page
[exit 0; 1 page PNG]
```

Each of the 38 actual page images was individually viewed. Main 17 pages and Supplement 20 pages have per-page observations, with title-page review by the root. Table 5’s two panels and both notes remain together on main page 11. Main page 4’s complete positioning matrix fits. Supplement continuation tables repeat headings and split only after whole rows; unsuccessful and NA entries remain visible. No blocking overflow, broken table row, equation or glyph defect was observed. Nonblocking density/spacing observations are recorded, rather than claiming a warning-free aesthetic. Final PDFs were copied byte-for-byte to submission-jof/. S9 may now begin.

## S9: PASS — full final acceptance

Accepted 2026-10-24T06:30:36.769948+00:00. All S9 gates below have passed before entering S10. No publication action had begun at this acceptance.

### s9-budget-check.json

```text
$ python3 -B notes/v7/check_s5_budget.py --current
```

```json
{
  "section_counts": [
    {
      "section": "Introduction",
      "words": 809,
      "limit": 1300,
      "pass_limit": true
    },
    {
      "section": "Related literature",
      "words": 316,
      "limit": 900,
      "pass_limit": true
    },
    {
      "section": "The forecast target",
      "words": 519,
      "limit": 1000,
      "pass_limit": true
    },
    {
      "section": "Data",
      "words": 252,
      "limit": 600,
      "pass_limit": true
    },
    {
      "section": "Forecasting methods",
      "words": 411,
      "limit": 800,
      "pass_limit": true
    },
    {
      "section": "Evaluation design",
      "words": 401,
      "limit": 800,
      "pass_limit": true
    },
    {
      "section": "Results",
      "words": 917,
      "limit": 2000,
      "pass_limit": true
    },
    {
      "section": "Implications for model validation",
      "words": 254,
      "limit": 500,
      "pass_limit": true
    },
    {
      "section": "Limitations",
      "words": 272,
      "limit": 500,
      "pass_limit": true
    },
    {
      "section": "Conclusion",
      "words": 263,
      "limit": 350,
      "pass_limit": true
    }
  ],
  "total_words": 4414,
  "total_limit": 8800,
  "captioned_main_tables": 6,
  "main_figures": 3,
  "main_pages": 17,
  "supplement_pages": 20,
  "supplement_page_limit": 30,
  "main_pdf_producer": "xdvipdfmx (0.1)",
  "supplement_pdf_producer": "xdvipdfmx (0.1)",
  "main_pdf": "submission-jof/manuscript.pdf",
  "supplement_pdf": "submission-jof/supplement.pdf",
  "status": "PASS"
}
```

### s9-delivery-check.json

```text
$ read-only source/PDF/ZIP verification and native cover pagination
```

```json
{
  "status": "PASS",
  "cover_words": 192,
  "cover_pages": 1,
  "cover_producer": "xdvipdfmx (0.1)",
  "cover_numbers": [],
  "aliases_identical": true,
  "snapshots_match_source": true,
  "zip_members_match_source": true,
  "canonical_scientific_numeric_changes_after_S8": 0,
  "compiler_returncode": 0,
  "first_compile_attempt": "fontspec name unavailable; retried using existing main document font route; no install/download",
  "controller_note": "Receipt serialization initially shadowed subprocess object with a Path; files verified read-only after correcting receipt code"
}
```

### s9-package-compile-check.json

```text
$ compile each extracted current-package entry point with existing Tectonic --only-cached
```

```json
{
  "status": "PASS",
  "extracted_members": 11,
  "compiled_from_package_alone": true,
  "only_cached_existing_compiler": true,
  "documents": [
    {
      "command": [
        "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
        "-X",
        "compile",
        "--only-cached",
        "main.tex",
        "--outdir",
        "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v7/s9/package-compile/main-output",
        "--keep-logs",
        "--keep-intermediates"
      ],
      "returncode": 0,
      "pages": 17,
      "producer": "xdvipdfmx (0.1)",
      "seconds": 0.4520337078720331,
      "overfull": 0,
      "undefined": 0,
      "missing_characters": 0
    },
    {
      "command": [
        "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
        "-X",
        "compile",
        "--only-cached",
        "supplement.tex",
        "--outdir",
        "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v7/s9/package-compile/supplement-output",
        "--keep-logs",
        "--keep-intermediates"
      ],
      "returncode": 0,
      "pages": 20,
      "producer": "xdvipdfmx (0.1)",
      "seconds": 0.3810056250076741,
      "overfull": 0,
      "undefined": 0,
      "missing_characters": 0
    },
    {
      "command": [
        "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
        "-X",
        "compile",
        "--only-cached",
        "title-page.tex",
        "--outdir",
        "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v7/s9/package-compile/title-page-output",
        "--keep-logs",
        "--keep-intermediates"
      ],
      "returncode": 0,
      "pages": 1,
      "producer": "xdvipdfmx (0.1)",
      "seconds": 0.2410389999859035,
      "overfull": 0,
      "undefined": 0,
      "missing_characters": 0
    }
  ],
  "new_financial_calculations": 0
}
```

### s9-current-document-check.json

```text
$ compare old/new aux label mappings, numeric tokens and rendered page files
```

```json
{
  "status": "PASS",
  "scope": "S9 reference-only correction and fresh compiled output",
  "original_S8_evidence_remains_historical": true,
  "only_main_source_edit": "coVaRiance -> covariance",
  "ordered_numeric_tokens_identical": true,
  "compiled_label_number_page_mapping_identical": true,
  "rendered_pages_identical_to_individually_reviewed_S8": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16
  ],
  "changed_page_visually_reviewed": [
    17
  ],
  "visual_observation": "Page 17 corrected covariance spelling; complete references and glyphs readable, no clipping or broken lines; other 16 pixel files byte-identical",
  "page17_png_sha256": "a9abc8e775a1cf7c78590350b7889a01b2a62c7ea3da365a82606bd84666270c",
  "scientific_results_changed": 0
}
```

### Full final pytest

```text
$ /Users/bingyouli/.local/bin/uv run --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B -m pytest -p no:cacheprovider -v --basetemp /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v7/s9/final-pytest-temp
test_verify_preference_frontier.py::IndependentFrontierTests::test_inequality_intersection_retains_point_only_winner PASSED [ 97%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_json_duplicate_keys_are_rejected PASSED [ 97%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_missing_boundary_tie_is_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_missing_headline_fields_and_invalid_record_shapes_are_rejected 
test_verify_preference_frontier.py::IndependentFrontierTests::test_missing_headline_fields_and_invalid_record_shapes_are_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_missing_pair_and_duplicate_pair_are_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_nonfinite_negative_boolean_and_fraction_tokens_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_same_byte_source_hash_and_duplicate_cell_rejected PASSED [ 98%]
test_verify_preference_frontier.py::IndependentFrontierTests::test_wrong_crossing_wrong_domination_and_open_winner_are_rejected PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_attempt_dotdot_escape_does_not_create_outside_receipt PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_constant_decimal_mean_is_preserved_exactly PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_exact_table_matching_reports_all_changed_fields_and_duplicate_rows PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_future_values_cannot_change_pre_refit_reports_but_do_change_target PASSED [ 98%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_integer_ranks_and_minimizer_endpoint_contract PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_no_overwrite_and_scratch_boundary PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_oracle_rejects_missing_history_duplicate_origins_and_incomplete_targets PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_saved_arrays_compare_every_issue_and_count_exact_disagreements PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============= 991 passed, 1066 subtests passed in 83.62s (0:01:23) =============
```

Full output: notes/v7/s9-final-pytest-output.txt. No tests filtered, skipped or removed. Offline cached uv environment, isolated full tracked-file copy; original result trees unchanged.

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
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v7/s9/final-pytest-temp"
  ],
  "scope": "default full discovery after S9 one-word APA correction; all current tracked files copied; no filtering/skipping",
  "tracked_file_count": 2633,
  "UV_OFFLINE": true,
  "PYTHONPATH": null,
  "started_utc": "2026-10-24T06:24:08.384996+00:00",
  "ended_utc": "2026-10-24T06:25:32.480678+00:00",
  "returncode": 0,
  "seconds": 84.09579029097222,
  "child_peak_rss_bytes": 335331328
}
```

### Exact final numerical / crossreference / metadata outputs

```text
$ /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B notes/v7/check_numbers_v7.py
{
  "status": "PASS",
  "main_binding_count": 117,
  "supplement_binding_count": 2125,
  "s2_records_checked": 1205,
  "s2_source_files_checked": 43,
  "supplement_original_source_files_checked": 27,
  "distinct_original_source_hashes_checked": 52,
  "rendered_pdf_checks": {
    "main": {
      "set": 4,
      "scalar": 113
    },
    "supplement": {
      "not_a_simple_numeric_token": 47,
      "scalar": 1925,
      "fraction_components": 153
    }
  },
  "unclassified_digit_token_occurrences": 0,
  "unresolved_token_row_alignments": 0,
  "mismatches": 0,
  "failures": [],
  "token_inventory_status": "CLASSIFIED_WITH_LIMITS"
}
```

```text
$ /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B notes/v7/check_final_crossrefs.py
{
  "status": "PASS",
  "documents": {
    "manuscript": {
      "labels": 21,
      "reference_occurrences": 22,
      "unresolved": [],
      "duplicate_labels": []
    },
    "supplement": {
      "labels": 25,
      "reference_occurrences": 1,
      "unresolved": [],
      "duplicate_labels": []
    }
  },
  "preservation": {
    "v6": {
      "source_commit": "29190137a1a0617b9d4f70cc28175ee14a57aba6",
      "original_paths": 2095,
      "missing_original_paths": [],
      "protected_files": 1079,
      "changed_protected_files": []
    },
    "supervisor": {
      "source_commit": "0ebc6e54ee3682315670a641e8783fc15c3660f4",
      "original_paths": 850,
      "missing_original_paths": [],
      "protected_files": 537,
      "changed_protected_files": []
    }
  },
  "issues": []
}
```

```text
$ /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B notes/v7/check_references.py
{
  "status": "PASS",
  "cited": 28,
  "bib_entries": 28,
  "printed_entries": 28,
  "missing": [],
  "unused": [],
  "print_mismatches": [],
  "metadata_entries_with_primary_evidence": 28,
  "author_placeholders": {
    "Author information": true,
    "ORCID": true,
    "Funding": true,
    "Competing interests": true,
    "AI statement": true
  },
  "author_declarations_completed": 0
}
```

### Writing metrics retained at final source

```text
$ python3 -B notes/v7/writing_metrics.py --output notes/v7/s9-writing-metrics.json --summary --require-pass
```

Full actual output is in s9-final-check-output.json; final-source counts are unchanged by the bibliography-only spelling repair.
```json
[
  {
    "before": {
      "abstract_words": 215,
      "abstract_numbers": 9,
      "main_sentences": 400,
      "mean_sentence_words": 16.7825,
      "over35_percent": 2.0,
      "negation_percent": 20.0,
      "max_numbers_per_sentence": 10,
      "pass_quantitative": false
    }
  },
  {
    "after": {
      "abstract_words": 139,
      "abstract_numbers": 4,
      "main_sentences": 215,
      "mean_sentence_words": 19.832558139534882,
      "over35_percent": 0.0,
      "negation_percent": 2.3255813953488373,
      "max_numbers_per_sentence": 2,
      "pass_quantitative": true
    }
  }
]
```

### Scope and issues actually resolved

- The source inventory classifies all 8,500 numeric token occurrences; unclassified tokens and unresolved row alignments are zero. This role classification does not claim independent validation of scientific results or PDF coordinates. Scalar bindings and saved fractions are checked separately; the three LaTeX figure sources were regenerated in an isolated directory from saved values and are byte-identical (s9-figure-source-check.json), with no score/model calculation.
- Existing mathematical constants and source identifiers were read against their definitions and recorded sources. Spelled counts in the thesis, contributions, cover and scope descriptions were read against their S2 statements; the cover has no numeric digit tokens.
- Corrected covariance spelling after the APA acronym formatter matched VaR inside a longer word. Final source changes exactly that word since S8; the numeric sequence and aux number/page maps are identical. The recompiled first sixteen page PNGs are byte-identical to S8; the changed last reference page was individually viewed and is readable. Sources, aliases, content snapshots and ZIP are synchronized.
- Native cover pagination initially failed on an unavailable named font. Retrying the already working main-document font route succeeded in one page without installation. A receipt-only Python variable-shadowing error was repaired; completed files were independently read back before acceptance. These failed attempts remain recorded.
- Full pytest was run again after the one-word reference fix. Default discovery, all tracked source files, no filtered or removed cases; 991 tests and 1,066 subtests passed. Peak child RSS 335331328 bytes. A new copied workspace isolates synthetic fixture writes from all original results.
- Preserved: both source lines, every original tracked path, all 69 original frozen result files, 16 frozen core-code files, 23 exact v6 deliverables and 53 pre-existing backups. No new financial model/data/test/parameter fit and no file deletion.
- Full references, per-field evidence, token inventory, compiled logs, package checks and pytest transcripts are linked in notes/v7/. Cover remains an unsigned author-completion draft. S10 may now begin.

### S9 optional whitespace check clarification

`git diff --cached --check` reported trailing whitespace in literal pytest/compiler transcripts and their quoted ledger output. These are preserved original command outputs required by the plan; no scientific text or source error was reported. This optional whitespace command was nonzero and is not represented as PASS. All actual S9 acceptance gates above passed.

## S10: IN PROGRESS — prepush checks

`git ls-files -z` identifies no tracked .scratch path, raw Kaggle FX dataset, private numeric-array/trace file or credential-shaped path. Standard token/private-key content patterns have zero matches. The broader ZIP path heuristic first flagged the already existing 41-member replay-metadata.zip: manual review confirms only public JSON manifests/input fingerprints, all matching the frozen original manifest and original Git blob. Its historical member names are not newly copied scratch/private files. Initial candidates are retained in s10-prepush-initial-candidates.json; final review is s10-prepush-check.json. No file is removed or repackaged.

Read-only remote observation: main remains 65feeee; PR #3 remains open/unmerged but another conversation advanced its head from the S1 merged snapshot 0ebc6e54 to 2328994c. S1 used the then-current fetched supervisor snapshot; S10 does not repeat S1 or alter PR #3. The later external writing changes are an author integration decision, recorded in author-decisions.md.

## S10: BLOCKED — Git HTTPS authentication unavailable

The actual push was attempted once after S9 PASS and a clean tracked-file/public-content check. It failed before upload:

```text
$ git push -u origin revision-v7-final
fatal: could not read Username for 'https://github.com': terminal prompts disabled
[exit 128]
```

The complete command/timestamps/local HEAD are in notes/v7/s10-first-push-receipt.json. No credential, billing or permission was changed. The plan has a PR-creation fallback, but no push-authentication fallback; under Part I.2 execution stops at S10, without a browser/API upload, another push, or a PR against a missing head.

Read-only confirmation after failure:

```text
$ git ls-remote origin refs/heads/main refs/heads/codex/supervisor-revision-20261023 refs/heads/revision-v7-final
2328994c44ec02bd731ad556f41fe9821f6de6df	refs/heads/codex/supervisor-revision-20261023
65feeee801b6b228a608ca3200e0678bb5f62b1c	refs/heads/main
[exit 0]
```

No revision-v7-final remote head exists, so a remote-tree equality check and usable PR/compare URL cannot be supplied. Main remains 65feeee; PR #3 was not changed by this task. All S1–S9 deliverables remain committed locally. Final publication is BLOCKED rather than represented as completed. See notes/v7/s10-blocked.json.

## S10: PASS — author-authorized browser publication

Accepted 2026-10-24T07:51:03.629521+00:00. The user explicitly authorized switching from the unavailable command-line Git authentication to the existing logged-in GitHub browser, while prohibiting main merges and changes to PR #3. This supersedes the earlier S10 transport blocker; its original failure record remains above.

Browser actions: create revision-v7-final from the existing v4 publication branch; upload the exact local delta by directory; commit each batch only to revision-v7-final; open a new PR with base main and head revision-v7-final. No credential or permission was changed. Browser commits have their own history; exact file-tree identity is verified rather than claiming identical commit IDs.

Actual terminal readback after the complete upload:

```text
$ git fetch origin refs/heads/revision-v7-final:refs/remotes/origin/revision-v7-final
From https://github.com/ByronLi0207/financial-mathematics-paper-20261020
   1fcab92..7056570  revision-v7-final -> origin/revision-v7-final
$ git diff --exit-code 5e35dba21ea5ced708dad47cbee29fe12e4c6936 7056570757a6721da873ec1032a62e7111bdda07
[no output; exit 0]
```

Every remote blob was then read from git cat-file --batch and compared byte-for-byte to its local file, with SHA-256 and file mode checks:

```json
{
  "status": "PASS",
  "checked_utc": "2026-10-24T07:48:23.688382+00:00",
  "local_source_commit": "5e35dba21ea5ced708dad47cbee29fe12e4c6936",
  "remote_commit": "7056570757a6721da873ec1032a62e7111bdda07",
  "local_tree": "ad439a1c12b16b3f198d43e398248f1fe5f85ff0",
  "remote_tree": "ad439a1c12b16b3f198d43e398248f1fe5f85ff0",
  "files_checked": 2652,
  "bytes_checked": 74909563,
  "mismatches": 0,
  "missing": 0,
  "extra": 0,
  "mode_mismatches": 0,
  "git_diff_returncode": 0
}
```

The native browser result visibly showed:

```text
URL: https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/4
Publish verified v7 peak-position manuscript and complete evidence — #4
Open
base: main
head: revision-v7-final
```

The GitHub connector independently confirmed PR #4 open/unmerged with head 7056570 and base 65feeee; PR #3 remained open/unmerged at 2328994c with the same main base. The new PR is attached to this task. Native 17/20/1-page PDFs match the final S9 hashes. Existing scientific code, data, results, negative findings and author placeholders are unchanged. No merge, submission, deletion or new financial calculation occurred.

Publication evidence is notes/v7/s10-browser-publication.json. This final evidence record and ledger appendix add metadata only; after uploading them, the updated branch is subjected to another complete tree and file-content comparison before handoff.
