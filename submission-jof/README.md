# Journal of Forecasting submission preparation

This is a preparation package, not a journal submission or acceptance claim. The official guideline check identifies single-blind review and Free Format initial submission. Personal author and disclosure fields remain placeholders.

- manuscript.tex / manuscript-preview.pdf: main article; 17 preview pages, 6721 prose words excluding abstract, references, tables and captions.
- supplement.tex / supplement-preview.pdf: 33 pages, all original tables retained across the two documents.
- title-page.tex / title-page-preview.pdf: author completion sheet.
- references.bib: union of verified metadata dispositions; each document displays only its own cited references in consistent author–date format under Free Format.
- figures/: grayscale vector assets; all archived curve-display values are preserved; the main annual display is retained in the Supplement and a deterministic endpoint-versus-peak illustration is added.
- overleaf-package.zip: select main.tex for the article; supplement.tex and title-page.tex are separate targets. Sources use standard article/packages and relative vector assets, with no local font path dependency.
- cover-letter.md: draft for author completion; no signed declarations.
- AUTHOR-TODO.md: remaining personal actions and evidential limitations.

Preview PDFs are independently typeset with ReportLab. Saved TeX source compilation is checked using the desktop editor compiler, which returns diagnostics rather than an exported PDF. Formal TeX-generated PDFs must be obtained and inspected by the author before submission.

Current v5 checks, selected-suite pytest output, original-text evidence and source/figure bindings are in notes/revision-v5-novelty/. Earlier v4 checks remain intact. The added illegal-label timing experiment is post-result / exploratory and does not replace any original result or primary. Build content with v5_submission.py, the new illustration with v5_figure.py, and previews with v4_typeset.py; check with v4_numeric.py and package with v5_package.py. Reproduce added numeric analyses with v5_analysis.py; exact mathematical checks are in v5_theory.py. The new table and figure numbers refer to the revised manuscript, while original records retain their archival numbering.
