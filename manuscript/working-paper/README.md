# Working paper and source

**Historical and Conditional Forecasts of Sampled Net-Position Peaks** is a retrospective benchmark of established forecasting methods on an individual-market-maker FX record and separately fitted Treasury position aggregates. The 23 October critical review clarifies the estimand, information clock, comparison scope and loss interpretation. The [review and corrections](../../REVIEW_20261023.md) identify the actual issues and the evidence gaps that remain.

The current supplied paper has **24 pages: 21 text, reference and caption pages followed by three vector figure pages**. It retains all **15 numerical tables and 21 equation blocks** from the preceding 25-page revision. The current bibliography contains **25 used reference entries**, with matching BibTeX IDs and order; the unused Liao–Theodosopoulos entry remains in historical source records. The declared primaries, complete adverse/favorable financial results and three vector figure inputs are unchanged. No financial model was refitted for this revision.

- [paper.pdf](paper.pdf): current standalone reading copy.
- [main.tex](main.tex): complete current LaTeX source, tables, references and relative figure paths.
- [paper-content.json](paper-content.json): canonical structured text, with readable and LaTeX equation representations.
- [references.bib](references.bib): matching companion reference catalog; the build embeds the canonical reference text.
- [rendering-verification.json](rendering-verification.json): current file identities, inventory and actual verification scope.
- [figures](figures/): the three current vector figures and preserved earlier figures.

The current source compiled successfully with the desktop editor's built-in LaTeX compiler. That interface returns diagnostics without exporting a standalone PDF. The supplied PDF is separately typeset from the same structured content using ReportLab 4.4.9 and pypdf 6.10.0. It is **not an export of the TeX compiler**; another TeX environment may produce different fonts and pagination.

## Current checks

Every complete canonical text, equation, heading, table-cell, reference and caption unit is reconciled against extracted PDF text. The receipt states the normalization and matched-unit counts. All fifteen table objects and twenty-one equation objects are compared directly with baseline commit cbce398; all three figure inputs and their appended PDF streams match exactly. Removal of the one unused reference and the revised prose are intentional content changes.

The review renders every body page and checks the full layout, then inspects dense target, preference, numerical and frontier pages at higher resolution. Preserved vector figure pages are also checked in the supplied document. Visual inspection, successful source compilation and text reconciliation establish different aspects of document fidelity; none constitutes new financial validation.

Relevant existing document tests and the read-only sixty-nine-file core archive check are recorded separately from historical whole-repository suites. The [new annual-decomposition helper](../../notes/revision-20261023/annual-decomposition.py) reads only three hash-bound public CSVs. It reproduces the added 8.64%, 6.87% and 70.83% contribution descriptions, rejects changed inputs and refuses to overwrite an output. A relocated minimal checkout reproduced its JSON bytes with Python 3.12.14 and system Python 3.9.6.

## Rebuild the document

Use an existing compatible environment with `requirements-paper.txt` dependencies. The actual document checks used Python 3.12.14. The PDF route also reads the macOS Times New Roman fonts listed in `build_paper.py`; they are not redistributed. No raw financial source is needed for document generation.

From the repository root, choose new output paths:

```bash
mkdir -p .scratch
python3 -B build_tex.py --output .scratch/critical-main-NEW_ID.tex
python3 -B build_paper.py --output .scratch/critical-paper-NEW_ID.pdf
```

The scratch TeX file is suitable for byte comparison, not isolated compilation without its figure folder. Compile the supplied `main.tex` from this directory with adjacent `figures`, or copy the entire document directory to a new build location. Each builder refuses an existing output.

To reproduce the small aggregate decomposition without source observations or model fitting:

```bash
python3 -B notes/revision-20261023/annual-decomposition.py --output .scratch/annual-decomposition-NEW_ID.json
```

The [main repository guide](../../README.md) separates the standard-library archive route, Python 3.10+ preference-envelope route and Python 3.11+ pinned NumPy financial replay. Choose an explicit interpreter if the system `python3` is older than the route requires. Financial replay is optional and requires the exact accepted inputs; it is separate from rebuilding this document or checking the new aggregate decomposition.

## Evidence and earlier revisions

The [source evidence map](../../notes/revision-20261022/paper-evidence-map.md) records actual consulted editions and reading scopes. The [conditional results](../../results/revision-20261022/README.md), [AR replay](../../results/revision-20261022/ar1-replay/README.md), [rank control](../../results/revision-20261022/rank-ablation/README.md), [coverage diagnostic](../../results/revision-20261022/coverage-evalues/README.md) and [fixed-report loss weights](../../results/revision-20261022/preference-robustness/README.md) preserve complete menus and execution records. Their dated page counts and rendering checkpoints describe those earlier manuscript versions.

The accepted [Treasury snapshot](../../data/nyfed-pdposgs-b-20261022/README.md) remains archived under its continuing source terms. FX acquisition and redistribution remain separate. Economic-date downloaded-vintage replay is not historical first-release forecasting. Compatible untouched dealer validation, an observed decision mechanism and established statistical coverage assumptions remain absent.
