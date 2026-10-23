# Journal of Forecasting preparation package — revision v6

This is a research and submission-preparation package, not a journal submission or acceptance claim. Both original source-specific primaries and all archived adverse results are retained. All additional analyses are post-result / exploratory on previously inspected records.

- manuscript.tex / manuscript-preview.pdf: 18 independently typeset preview pages; 7096 prose words excluding abstract, references, tables and captions; 6 tables and 4 figures.
- supplement.tex / supplement-preview.pdf: 94 preview pages. Section S16 reports all finite delayed ACI-style, headroom SAV, fixed-combination, state and target-level inventories, including raw NA and adverse outcomes.
- title-page.tex / title-page-preview.pdf: author-completion sheet, 1 page.
- main.tex is the default article target. Select supplement.tex and title-page.tex separately.
- references.bib retains the existing union metadata and adds the verified official ACI proceedings entry; displayed references are document-specific and alphabetized.
- figures/ contains relative vector assets; no machine-specific font path is needed by the standard-article TeX.
- cover-letter.md and AUTHOR-TODO.md are drafts for author review. No signed declarations, account registration or journal submission occurred.

The PDFs are ReportLab previews. The desktop built-in compiler checks saved TeX and returns diagnostics rather than an exported PDF. Compile, export and inspect formal TeX-generated PDFs before submission. A preview does not prove identical layout in another compiler. No system software was installed.

Build the v6 documents with v6_submission.py, render the separate previews with v6_typeset.py, run the extended v4_numeric.py consistency audit and package with v6_package.py. v6_supplement.py regenerates every new table from public aggregate outputs. New financial engines and workers are separate v6 modules; v6_tau_worker_v2.py is the canonical target-level transport wrapper, while its failed v1 technical attempt remains archived. Detailed protocol freezes, complete command outputs, resource receipts and audits are in protocol/revision-v6/ and notes/revision-v6/.

Exact code/aggregate consistency is not independent financial replication. FX acquisition and source fingerprints are documented in the repository; raw FX and private origin-level traces remain unshared. Treasury tasks are related aggregates, and their downloaded economic-date vintage is not an as-released public-information backtest. New short tail failures and all historical limitations remain explicit.
