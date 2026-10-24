# Current v7 Journal of Forecasting revision

The current deliverables are `manuscript.pdf` / `manuscript.tex`, `supplement.pdf` / `supplement.tex`, `title-page.pdf` / `title-page.tex`, `references.bib`, the three `figures/v7-*.pdf` inputs, `cover-letter.md` and `AUTHOR-TODO.md`. All three document PDFs are native LaTeX/XeTeX output from the existing Tectonic compiler. The main manuscript has 17 pages including references and author placeholders; the compact Online Supplement has 20 pages.

`main.tex` is the default main entry point. Compile it with XeLaTeX or Tectonic; compile `supplement.tex` and `title-page.tex` separately. The sources contain their verified native author-year bibliography, with matching structured BibTeX metadata also supplied. No separate style download is needed for the delivered source route. The Overleaf package is self-contained and includes all current figure inputs.

For compatibility, the older filenames `manuscript-preview.pdf`, `supplement-preview.pdf` and `title-page-preview.pdf` now contain the identical current native PDF bytes; they are aliases, not a separate ReportLab rendering. The `*-content.json` files are current v7 LaTeX/source snapshots. The complete original v6 JSON schemas, source files, PDFs and package remain under `manuscript/revision-v6-preserved/`; the older version-specific builders still describe those recorded pipelines.

The v7 authoring templates, source-field bindings, evidence table, metadata checks, compiler logs and per-page visual review are in `notes/v7/`. Rebuild current text using `python3 notes/v7/build_main_v7.py` and the compact Supplement using `python3 notes/v7/build_supplement_v7.py`, then compile its generated source. These are document/readback operations, not financial replay. Full results and earlier documents are indexed by `EXTENDED_RESULTS.md`; no adverse or failed output is removed.

The manuscript is a retrospective forecast-comparison and model-validation study. It does not provide independent dealer validation, original-release public-information replication, a new estimator or a general fitted-coverage theorem. Complete the author checklist before any journal submission.
