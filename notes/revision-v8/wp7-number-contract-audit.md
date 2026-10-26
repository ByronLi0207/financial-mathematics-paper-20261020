# WP7 → WP8 numeric-coverage contract audit

Scope: read-only inspection of public source/binding/checker code and saved aggregates, plus the existing default read-only S2 field check. This note is the sole file written by this task. No raw FX observations, private per-issue arrays, forecasts, loss calculations, new statistical tests, models, data, tuning or document generation were performed. The audit is before final WP7 integration/compilation and **does not grant a current full-number PASS**.

## Finding that controls the implementation

The old v7 result is useful source evidence, not a current-document certificate. **Do not run `notes/v7/check_numbers_v7.py` in place to certify v8.** Its main entry point writes the old `notes/v7/s9-number-check.json` and `s9-number-token-inventory.json`. It also hardcodes the v7 document identity, paragraph templates and line locations. Its useful field-reading/whole-row binding ideas should be reused in a separate v8 checker with new output files and current source identities; the old records must remain unchanged.

An empty field-mismatch list is only one layer. It must not be reported as proof that every visible number has been located and checked. Current source occurrence coverage, generated-input coverage, charts, mathematical/design constants, metadata and rendered-document identity all need their own explicit treatment.

## What the existing mechanisms actually cover

| Mechanism | Established scope / useful reuse | Current-v8 gap or risk |
|---|---|---|
| `notes/v7/check_evidence.py` default invocation | Exact saved JSON-pointer / uniquely selected CSV-field / exact-text lookup; preserves native type and value. Default invocation is read-only. | It verifies the S2 evidence records, not their occurrence in the current manuscript. `--write` or `--append-table` would mutate old S2 artifacts and must not be used here. Some exact old scope passages are historical records, not proof of a still-current claim about untouched data. |
| `notes/v7/evidence-parts/*.json`, `evidence-table.md`, `evidence-source-fingerprints.json` | Original ID → claim, exact native value, file and field/selector; immutable source hashes. The old number checker separately extends the original fingerprint set for the later motivating-window source against its S1 commit. | Reuse all existing IDs and sources without changing them. New WP3–WP5 claims need a distinct v8 layer rather than edits to old values. A new display-format record may refer to the same raw ID. |
| `notes/v7/main-v7-numeric-bindings.json` | 117 main bindings associate an ID, native value, format and named section/table/abstract. | Current coarser prose percentages, rewritten sentences and new content are not all represented. Presence inside a named region is weaker than a located cell/sentence proof. |
| `notes/v7/s5-supplement-bindings.json` | 2,125 typed saved-field/display bindings and their source hashes, including failures/NA. | Precise format specifiers are not saved for every field. Old checker permits a fixed set of formatting possibilities; that must not become permission to alter a result. WP2 changed `\\frac` to `\\dfrac` and display padding without changing values. New `\\input` tables must be scanned, not just the parent TeX. |
| `notes/v7/check_numbers_v7.py` numeric-token census | It deliberately refuses equal-value global membership as a located binding, resolves supplement rows using ordered full-row sequences and task identity, retains ambiguity and explicitly records classification limits. These principles are sound. | Hardcoded 117/2125 counts, original paragraph templates, line-specific cases (e.g. main272–276 and many supplementary rows), preference-table line ranges, old compilation receipt/hash and old figure-source inventory make direct reuse stale. Do not simply redirect its output and interpret failures as changed science. |
| `notes/revision-v8/check_wp1_rounding.py` and WP1/WP2 rounding receipts | Seventeen old prose percentage displays are computed from the original saved fields, not from rounded table values. This prevents the documented 10.15→10.2 double-rounding error. | It requires exactly twelve old sentence anchors and compares the entire ordered percentage-sentence list. WP7 introduces new percentage sentences and may rewrite anchors, so the checker needs an additive v8 mapping/new output, not silent removal of cases. It only covers percentages, not every number. |
| `notes/revision-v8/writing_metrics.py` | Quantitative main-prose gates, fixed v7 baseline; flags overprecise percentages and “changes … by”. | It is not a scientific-number checker. Its scope excludes tables, display maths, references/declarations and the transparency subsection. It reads the main TeX text without recursively expanding inputs; any future main prose in `\\input` would require expansion or an explicit scope correction. Supplementary/letter numbers are not covered by its prose gates. |
| `notes/revision-v8/wp2-table-header-changes.json`, typography records | Records preservation of 368 original numeric result rows and the intended typography-only changes. | These are intermediate historical receipts. Recheck the current original rows against the accepted WP2/earlier source rows, allowing only explicitly documented equivalent math macro/padding transforms. They do not certify new table rows. |
| `results/revision-v8/wp3/readout-bindings.json` and summary/support/design | Hash-bound source summary, full scientific-screen object, candidate status totals and failed candidate identity. `summary.json` has216 F/QR33/QR4 cells; the complete regression central-metric table requires144 distinct QR cells. | The readout receipt is not a cell-by-cell TeX token binding. New tables must record exact `(method,phi,p,W,H)` identity, field and display rule. Do not swap model/reference breach rates or ratio-of-means with within-repetition ratios. Retain separate procedure/candidate statuses. |
| `results/revision-v8/wp4/readout-bindings.json` | Hash-bound12 method rows,8 contrasts, resampling metadata, actual930/501 counts, dates, candidate totals and classifications. | Existing row order cannot be inferred from an equal loss number. Bind `(W,H,method)` rows and the proper contrast, source-clock counts/date fields and unchanged source-table copy bytes. A map row must retain the daily QR4 exception, not only7/8 wins. |
| `results/revision-v8/wp5/three-window-bindings.json`, `three-window-summary.json` and full summary | Generator hash; exact old-row selectors, original raw copied rows/hashes; new summary/audit hashes;6 focus-window rows with new `source_contrast_index`; all8 new method/8 contrast slots retained in the full summary. | New and old DM families/fields cannot be interchanged. Old missing rolling breach/DM/QR4/H24 fields remain NA. The original-inspected relative display is explicitly derived from pinned existing mean fields in this new table; its full floating representation can differ by a few ULP from another archived ratio field. Verify the declared source/derivation, never silently replace an old native field or excuse a different statistic with a loose tolerance. |

## Observed read-only checks in this audit

Actual command:

```text
$ python3 -B notes/v7/check_evidence.py
{
  "status": "PASS",
  "rows_checked": 1205,
  "source_files_checked": 43,
  "mismatches": 0,
  "failures": [],
  "new_models": 0,
  "new_hypothesis_tests": 0,
  "new_data": 0
}
[exit0]
```

The default invocation above does not write the old evidence files. It establishes current equality of those1,205 saved S2 fields/passages only.

A standard-library SHA-256 comparison against `notes/v7/s9-number-check.json:documents` returned:

```text
{"document":"submission-jof/manuscript.pdf","historical_pages":17,"current_pdf_same_as_historical_s9":false}
{"document":"submission-jof/supplement.pdf","historical_pages":20,"current_pdf_same_as_historical_s9":false}
```

Thus the historical s9 PASS cannot certify even the current intermediate PDF bytes, let alone the forthcoming v8 final. The old receipt has0 mismatches and0 unclassified/ambiguous locations **for its own frozen files**, with status `CLASSIFIED_WITH_LIMITS`, not an unrestricted universal claim.

## Required v8 implementation sequence

1. **Fix the current artifact identity before checking it.** Record final main/Supplement/cover-letter source hashes, recursive generated-input hashes, exact included-figure hashes, actual compilation source/PDF hashes and paths. If sources change after this, rerun the affected checks and do not reuse an earlier hash as current proof.
2. **Read immutable old evidence and verify source hashes/types.** Reuse the original S2 records and supplement raw-field bindings without writing to v7. Keep a new v8 report. Verify the original protected result/data/protocol/Python files independently of document formatting. This is result preservation, not proof of current printed coverage.
3. **Recursively expand current TeX inputs with provenance.** Resolve every current `\\input`/`\\include` path, reject missing/ambiguous/out-of-scope paths, and keep origin filename, line and offset mapping. Census generated table files, captions, notes and main prose; do not let inserted `generated/v8-*` files bypass the inventory. Compare full expected rows with printed rows using task/column order. Missing, duplicate or unaligned rows are failures/unresolved items, not successful membership checks.
4. **Make an additive v8 field/display ledger.** Each measured or design numeric occurrence needs `(artifact, section/table/figure identity, exact unique sentence/row/cell, source file+hash, JSON pointer or unique CSV selector+field, native value/type, explicit display operation, printed token)`. Source formatting may multiply a saved rate by100 or divide native USD by1e6, or apply the explicitly authorized coarser precision. Those are declared unit/display operations, not new financial estimates. For prose using “lowers” or “raises”, verify the source sign as well as an absolute magnitude. Never derive prose from an already rounded table.
5. **Apply current sentence and cell anchors.** The old fixed paragraph templates and line numbers must not be treated as current. Preserve old IDs for unchanged meanings and add new occurrence records. Required new content includes MC2/12 and6/60, required-screen threshold and MC uncertainty/design counts; daily930/501,7/8, exception change/breaches and its correct W/H; WP5 ranges,7368/1440 overlap, later penalty identities, losses/breaches and the eight raw DM values. Keep paired-reference identity explicit.
6. **Separate result bindings from classifications.** Enumerate all digit occurrences, Unicode signed/range forms and meaningful number words. Check `one/two/three`, spelled-out parameter/count descriptions and ratio words manually where they carry a quantitative claim; a digit-only census cannot claim to cover them. Unbound `\\(p=0.055\\)` is still a result, not automatically a mathematical/structural constant. Likewise QR33/H6/W260 contain actual model/parameter meaning and need metadata identity even when their digit strings are classified as labels. Bibliographic years/volumes/pages and DOI/URL digits go to a separately verified reference/source-identifier inventory; layout dimensions and auto counters are explicitly classified rather than asserted to be financial fields.
7. **Verify mathematical and design constants in context.** Preserve exact numerator/denominator strings when normalizing `\\frac`/`\\dfrac`; do not turn an exact ratio into a fresh numerical statistic. Bind newly printed phi/p/W/H grids, GARCH constants, burn/retained lengths, seed/RNG, repetitions, sample indices, validation/evaluation counts, maturity clocks, penalty menus and failure totals to the frozen JSON/manifest—not to a handfilled expected-number dictionary. Mathematical identities/normalization constants and theorem/proposition numbering require a reviewed role, not a default escape hatch for all numbers in maths.
8. **Check the actual current figures, not the old source list.** Discover `\\includegraphics` from current TeX. For retained WP2 PDFs, verify exact bytes against `wp2-figure-styling.json` and their source hashes; validate the disclosed unit scale, recorded ticks and source-point preservation rather than calling ticks observations. The old `notes/v7/figure-sources/*.tex` are no longer sufficient current-artifact evidence. For WP3, `figures/display-receipt.json` contains every panel/cell/annotation and output hash. Independently reconstruct each saved-summary annotation from exact `(method,metric,H,phi,W,p)` and its field/MCSE, compare all stored annotations and figure-copy hashes, and retain the source-summary hash. This checks data-to-display traceability without refitting. Final per-page visual QA is still required for clipping, row/column placement, legibility and glyphs; scalar existence anywhere in a PDF does not prove position.
9. **Check the cover letter separately.** It was expressly outside the old delegated numeric checker. Scan its final current text even if it avoids digit results; meaningful counts/number words and any performance claim still need context. Author placeholders are not scientific outcomes. Confirm the letter's causal/mechanism/independence language agrees with the accepted negative evidence; that is a semantic review beyond number matching.
10. **Report separate gates with truthful scope.** Suggested fields: `raw_source_mismatches`, `located_display_mismatches`, `unclassified_occurrences`, `ambiguous_row_or_sentence_locations`, `meaningful_number_words_pending`, `figure_annotation_mismatches`, `reference_metadata_pending`, `current_source_pdf_hash_matches`, and `unreviewed_rendered_pages`. A global current numeric PASS requires all required classes reviewed/resolved, not just `raw_source_mismatches==0`. Keep limitations explicit: a binding/format check is not independent forecasting replication, causal identification, selection-adjusted inference or economic validation.

## Exact existing files to reuse read-only

Old source identity/value layer:

- `notes/v7/evidence-parts/{fx,panel,theory,metadata,s5-required-existing-fields}.json`
- `notes/v7/evidence-table.md`
- `notes/v7/evidence-source-fingerprints.json`
- `notes/v7/main-v7-numeric-bindings.json`
- `notes/v7/s5-supplement-bindings.json`
- `notes/v7/s9-number-token-inventory.json` (historical locator/classification examples only)
- `notes/v7/references-verified.json` and `reference-verification-table.md` (historic reference baseline, not current live verification)
- `notes/revision-v8/wp1-rounding-green.json`, `wp2-rounding-check.json`, `wp2-table-header-changes.json`, `wp2-final-typography-changes.json`

New source/result/design layer:

- `protocol/revision-v8/wp3-mechanism-design.json`, `wp4-daily-fx-design.json`, `wp5-fixed-prefix-design.json`
- `results/revision-v8/wp3/{manifest,summary,support,readout-bindings,study-termination}.json`
- `results/revision-v8/wp3/figures/display-receipt.json` and actual included PDF bytes
- `results/revision-v8/wp4/{manifest,summary,classification,readout-bindings,study-termination}.json`, `daily-results-table.tex`
- `results/revision-v8/wp5/{manifest,summary,three-window-summary,three-window-bindings,study-termination}.json`, both table TeX inputs
- `notes/revision-v8/wp3-independent-audit.json`, `wp4-independent-audit.json`, `wp5-independent-audit.json`
- `notes/revision-v8/wp5-prior-exposure-proof.json` and `wp5-mismatches.json` for exposure/interpretation counts; no private arrays are needed for document checking
- Current WP7 generator/field-binding receipts and generated inputs once completed; these must be verified as current, not presumed from a planned filename

## Disposition

**READY_TO_IMPLEMENT, NOT CURRENT_FULL_NUMERIC_PASS.** The existing typed locators, ordered-row checks, exact display formatting and source/PDF fingerprints are a sound foundation. The essential additions are current occurrence-level mapping, recursive input discovery, explicit figure/design/metadata handling and a residual inventory that cannot silently disappear. None of this requires a new financial experiment or editing the original result archive. This audit stops here.
