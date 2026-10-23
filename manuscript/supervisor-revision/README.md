# Supervisor revision: source and verification

Author: **Byron**. No affiliation is supplied, as the author requested.

`main.pdf` is the output of Tectonic 0.17.0 (XeTeX and xdvipdfmx), not the separate ReportLab manuscript renderer used by the preceding version. ReportLab here draws only four vector figure assets. The paper has **13 main/reference pages and four appendix pages**, including the one-page Appendix C. Its abstract has **145 whitespace-delimited words** and its conclusion **104**.

## Read and edit

- `main.tex` is the compilation entry point and controls layout and author details.
- `abstract.tex`, `sections.tex`, `appendices.tex` and `references.tex` are editable manuscript sources.
- `generated/` contains aggregate-derived display tables and the E3 results paragraph. Edit its generator, `build_supervisor_document.py`, rather than hand-changing numeric cells.
- `figures/` contains the synthetic target illustration, ordered loss waterfall, U/V-versus-breach changes and Murphy display.
- `../../results/supervisor-20261023/document-verification.json` records counts, scope, PDF identity and baseline preservation.

## Build

Use the project's compatible existing Python environment with ReportLab and pypdf. The calculation environment used Python 3.12.14 and NumPy 2.3.5. From the repository root:

```sh
python3 -B build_supervisor_document.py
tectonic --keep-logs manuscript/supervisor-revision/main.tex
python3 -B verify_supervisor_document.py
```

On the author's machine the engine was already bundled at `/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic`; no TeX distribution or application was installed. Tectonic fetched the missing font resources into its normal cache during the first compilation. Subsequent final builds used `--only-cached`. The actual successful command was:

```sh
/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic --only-cached --keep-logs manuscript/supervisor-revision/main.tex
```

The compiler output is kept as delivered; pypdf only reads it for verification. The PDF's producer is xdvipdfmx and author metadata is Byron. The compilation log had no overfull boxes after ragged-right table columns were introduced. Underfull spacing warnings are distinguished from clipping; actual page renders were inspected.

## Tables and figures

| Display | Inputs and interpretation |
|---|---|
| Table 1: closest studies | `results/supervisor-20261023/literature-table.json`; primary-source scopes in `notes/supervisor-20261023/literature-audit.md` |
| Table 2: calendar splits | Pinned source timestamps, checked during E3 source loading; no source observations are printed |
| Tables 3/4: full original method cells | `inference/tables3-4-ready.csv`; 48 rows, own-F changes and the original 72-family Holm adjustment |
| Table 5: nonoverlap coverage | `inference/coverage-verified.csv`; full-n POF and consistent first-hit-conditioned CC |
| Table 6: E3 | `e3/summary.csv` and `e3/paired-dm.csv`; shared-menu comparisons are exploratory |
| Table 7 / Figure 2: ordered comparison | `e3/primary-decomposition.csv`; common-baseline percentage points add, step-relative percentages compound |
| Table 8 / Figure 3: U/V and breaches | Original `results/revision-20261022/paired-comparisons.csv` and `evaluation-summary.csv` |
| Table 9: robustness | Complete AR/rank/horizon and fixed-report result supplements retained at their original paths |
| Figure 4: Murphy | Inherited plotting CSVs display the curves; the all-breakpoint check is independently retained in `inference/murphy-verified.csv` and `murphy-two-primary-exact.pdf` |
| Table 10: old Table B1 | The unchanged previous structured paper content, rounded for display; the tiny adverse tau90 difference stays explicitly positive |

## Statistical and reuse boundaries

The original two primaries remain unchanged. The FX cross-window primary is outside the 72 matched contrasts. The E3 family has its own 28 comparisons. Identical KNN/F loss sequences have no nondegenerate DM statistic; conservative p=1 values are used solely to retain their family slots. The CC initialization correction changes diagnostics, not any forecast, loss or breach count. All statistical additions were made after inspection.

The E1/E3 helpers read retained private numeric traces and the earlier four-predictor run. Their default locations identify this actual audit context, not a clean-clone data service. Public outputs contain hashes, aggregates, candidate selections and solver diagnostics; per-origin financial arrays remain private. A fresh public checkout can rebuild the manuscript and inspect aggregate evidence, but reproducing these added financial calculations also requires the documented pinned source snapshots and retained numeric trace context. The older `reproduce_conditional.py` route remains the documented clean-attempt route for the original study. None of these calculations creates independent financial validation.

The previous manuscript and every original result file are preserved. The Chinese change inventory maps material removed from the new printed paper to its retained repository location. Third-party full article copies and visual reading extracts remain in the ignored local scratch directory; the public source notes provide canonical links and reading scopes.
