# Working paper and source

**Historical Response Selection for Sampled FX Net-Position Peaks** is a 17-page English working paper: 14 pages of text, ten tables, elementary derivations, references and captions, followed by three vector figure pages. The revision distinguishes the original fixed comparison from an exploratory signed-state retrieval extension on the already inspected interval. It retains adverse score, breach, severity, horizon and calendar evidence.

- [paper.pdf](paper.pdf): reviewed standalone paper.
- [main.tex](main.tex): complete LaTeX text, tables and references, with relative figure paths.
- [paper-content.json](paper-content.json): shared manuscript content and explicit equation representations.
- [references.bib](references.bib): reusable BibTeX records for the same 14 cited sources, with matching reference keys and notes on consulted editions.
- [rendering-verification.json](rendering-verification.json): actual content/source/PDF identities and verification scope.
- [figures/](figures/): all three original figures and three added aggregate-only figures. The current paper uses a restyled display of all seven original paired means and the two retrieval figures; the original figure files remain unchanged. The current monthly display explicitly distinguishes H=6 primary from H=24 sensitivity; its source values and plotted data region are unchanged.

The delivered paper takes its reference text from `paper-content.json`; `references.bib` is a companion catalog rather than a build dependency. Keep the catalog consistent when revising the structured references. Publication years and consulted manuscript dates are kept distinct. Actual reading scopes remain in the [source evidence map](../../notes/revision-20261021/paper-evidence-map.md).

The source passed the desktop editor's built-in LaTeX compiler. That interface supplies diagnostics without a standalone export. The delivered PDF is independently typeset from the same structured content using ReportLab 4.4.9, with approved vector pages appended through pypdf 6.10.0. It is **not an export of the TeX compiler**. Compiling the source elsewhere can give different pagination and fonts; the scientific content and referenced figure assets are shared.

All 17 PDF pages were rasterized and inspected. The audit found no unsupported body-font characters, replacement/box/NUL glyphs or characters outside the page bounds. It reconciled 635 source text, table and caption blocks to the actual PDF text, excluding only the 14 observed page-number footers. Each appended figure stream matches its approved standalone source. Source regeneration is byte-identical to the successfully compiled `main.tex`. These checks concern document fidelity; scientific output identities are recorded in their separate run manifests.

From the repository root, in the documented existing environment:

```
python3 -B build_tex.py --output .scratch/main-rebuilt.tex
python3 -B build_paper.py --output .scratch/paper-rebuilt.pdf
python3 -B build_revision_figures.py --output .scratch/revision-figure-rebuild-01
python3 -B build_original_comparison_figure.py --output .scratch/revision-figure-original-rebuild-01
```

Each output must be new. The PDF builder accepts exactly the original, earlier revision or restyled revision ordered three-figure inventory and protects the union of their input paths, including equivalent output path spellings. Text rendering requires the four existing macOS Times New Roman files in `/System/Library/Fonts/Supplemental/`; missing fonts stop it. Font files are not redistributed. The figure-caption heading and its three captions stay together when they fit a page. All three current standalone figures use built-in Helvetica. The original-comparison renderer pins the original manifest and seven-row paired table; its sole numerical transformation is USD to USD million for display. The builders do not open raw financial observations or execute new forecasts. `requirements-paper.txt` records the document dependencies.

After the original comparison was restyled, caption pagination corrected and monthly horizon labels clarified, the combined code/test suite passed 173 tests in 7.940 seconds by unittest's clock. This includes synthetic scientific validation, aggregate artifact checks, preservation of the original figures, selection/protection checks for all three approved inventories and two physical-PDF caption pagination cases. It does not establish population superiority, external validity or publication readiness.

The figure tests subsequently replaced a machine-specific interpreter path with the active Python interpreter. Their 12 existing tests, including the CLI subprocess, passed after that correction; the 173-test result is the earlier full run.

The original 12-page manuscript is preserved in [repository history at the pre-revision baseline](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/f6dca510c137c0634845885c4d70828e37b99aea/manuscript/working-paper). Original scientific outputs and code remain unchanged. Data access, mature method lineage and interpretation are documented in the [root README](../../README.md), [extension results README](../../results/revision-20261021/README.md) and [source evidence map](../../notes/revision-20261021/paper-evidence-map.md). Raw source data and third-party papers are excluded.
