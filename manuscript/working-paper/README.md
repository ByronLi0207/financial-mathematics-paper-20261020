# Working paper and source

**Historical Response Selection for Sampled FX Net-Position Peaks** is a 16-page English working paper: 13 pages of text, nine tables, elementary derivations, references and captions, followed by three vector figure pages. The revision distinguishes the original fixed comparison from an exploratory signed-state retrieval extension on the already inspected interval. It retains adverse score, breach, severity, horizon and calendar evidence.

- [paper.pdf](paper.pdf): reviewed standalone paper.
- [main.tex](main.tex): complete LaTeX text, tables and references, with relative figure paths.
- [paper-content.json](paper-content.json): shared manuscript content and explicit equation representations.
- [rendering-verification.json](rendering-verification.json): actual content/source/PDF identities and verification scope.
- [figures/](figures/): all three original figures and two added aggregate-only figures. The revised paper uses original within-cell paired means and the two new retrieval figures.

The source passed the desktop editor's built-in LaTeX compiler. That interface supplies diagnostics without a standalone export. The delivered PDF is independently typeset from the same structured content using ReportLab 4.4.9, with approved vector pages appended through pypdf 6.10.0. It is **not an export of the TeX compiler**. Compiling the source elsewhere can give different pagination and fonts; the scientific content and referenced figure assets are shared.

All 16 PDF pages were rasterized and inspected. The audit found no unsupported body-font characters, replacement/box/NUL glyphs or characters outside the page bounds. It reconciled 606 source text, table and caption blocks to the actual PDF text, excluding only the 13 observed page-number footers. Each appended figure stream matches its approved standalone source. Source regeneration is byte-identical to the successfully compiled `main.tex`. These checks concern document fidelity; scientific output identities are recorded in their separate run manifests.

From the repository root, in the documented existing environment:

```
python3 -B build_tex.py --output .scratch/main-rebuilt.tex
python3 -B build_paper.py --output .scratch/paper-rebuilt.pdf
python3 -B build_revision_figures.py --output .scratch/revision-figure-rebuild-01
```

Each output must be new. The PDF builder accepts exactly the original or revised ordered three-figure inventory and protects the union of their input paths, including equivalent output path spellings. Text rendering requires the four existing macOS Times New Roman files in `/System/Library/Fonts/Supplemental/`; missing fonts stop it. Font files are not redistributed. The new standalone figures use built-in Helvetica. The builders do not open raw financial observations or execute new forecasts. `requirements-paper.txt` records the document dependencies.

The combined code/test suite passed 160 tests before the final figure-footer wording edit; the 12 targeted figure tests passed again after that edit. This includes synthetic scientific validation, artifact checks and meaningful original/revised inventory selection tests; it does not establish population superiority, external validity or publication readiness.

The original 12-page manuscript is preserved in [repository history at the pre-revision baseline](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/f6dca510c137c0634845885c4d70828e37b99aea/manuscript/working-paper). Original scientific outputs and code remain unchanged. Data access, mature method lineage and interpretation are documented in the [root README](../../README.md), [extension results README](../../results/revision-20261021/README.md) and [source evidence map](../../notes/revision-20261021/paper-evidence-map.md). Raw source data and third-party papers are excluded.
