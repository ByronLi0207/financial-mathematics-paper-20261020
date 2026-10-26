# G1 table and wording edits

Completed editorial checks: 2026-10-26T03:12:31.470144+00:00.

## Table 2

- Before: `.scratch/v13/editorial-before/table2-05.png`; after: `.scratch/v13/editorial-after/table2-05.png`. Both 1,800-pixel page renders were actually viewed.
- Panel A: one source per line; original period dates shown YYYY-MM. Earlier FX dates and complete peak counts retained in the note. Every cell is a single line.
- Panel B: units on every source row, three significant digits, comma grouping and no scientific notation. All 45 displayed values were converted from the old displayed numeric token and compared by exact Decimal equality; there is no recomputation.
- Main and supplement native Tectonic compilation both pass, with no overfull boxes, undefined references or duplicate labels. These are interim G1 PDFs, not final publication.

## Wording and display edits

- Removed 85 visible targeted term occurrences, leaving one permitted QR4 code in the main methods table. Nonprinting source comments, URL argument bytes and T1 font encoding remain intact.
- Separately changed one figure title from "full registered grid" to "full pre-specified grid". The saved cost arrays and all 115 numerical PDF text tokens are unchanged; all other PDF text is identical after the specified title substitution.
- The supplementary MCS method-key table now uses explanatory procedure/source labels instead of internal paths. Short IDs and every numerical membership result are unchanged; the exact before/after display mapping is in `G1-method-labels.json`.
- Full line-by-line before/after edits are in `G1-formatting-check.json`; title and array comparison is `G1-cost-title-check.json`.
- Kept the meaning of fixed simulation designs and unavailable cells. "unverified assumptions" becomes "unestablished assumptions", not a stronger assumption claim.

## Files

- `submission-v10/figures/v10-cost-regions.pdf`
- `submission-v10/generated/v10-mcs-compact.tex`
- `submission-v10/generated/v10-menu-main.tex`
- `submission-v10/generated/v12-data-table.tex`
- `submission-v10/generated/v8-three-window-table.tex`
- `submission-v10/generated/v9-legacy-simulation-table.tex`
- `submission-v10/generated/v9-stability-W260-table.tex`
- `submission-v10/generated/v9-stability-W52-table.tex`
- `submission-v10/generated/v9-stability-diagnostics-table.tex`
- `submission-v10/manuscript.tex`
- `submission-v10/supplement.tex`
