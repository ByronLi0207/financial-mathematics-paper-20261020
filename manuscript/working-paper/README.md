# Working paper and source

**Historical and Conditional Forecasts of Sampled Net-Position Peaks** compares historical response constructions with ridge quantile regression, multivariate local quantiles, a scale-adjusted local variant and later exploratory AR residual replay on the same sampled-peak response. The 22 October revision retains the favorable FX primary and adverse Treasury QR primary together; the later eight-cell AR comparison qualifies any generalization across conditional families. [Complete AR evidence](../../results/revision-20261022/ar1-replay/README.md) includes all twenty-four contrasts and the independent readback. It is an application and model-validation study using mature estimators; it establishes no new estimator, conditional-coverage theorem or operational saving.

The current document has **20 pages: 17 text/reference/caption pages and three vector figure pages**, with ten tables, elementary derivations, 23 references and the complete conditional loss menus. Source-specific native units, chronological selection, the previously inspected FX interval, weekly aggregate measurement, downloaded-vintage replay and post-result diagnostics are explicit.

- [paper.pdf](paper.pdf): standalone supplied PDF.
- [main.tex](main.tex): complete LaTeX source, tables, references and relative figure paths.
- [paper-content.json](paper-content.json): shared structured content, including separate readable and LaTeX equation representations.
- [references.bib](references.bib): companion catalog for the same 23 reference IDs and consulted editions, in the same order.
- [rendering-verification.json](rendering-verification.json): content/source/PDF/figure identities and actual document verification scope.
- [figures/](figures/): three current conditional-study figures and the preserved earlier figures.
- [current source evidence map](../../notes/revision-20261022/paper-evidence-map.md): consulted editions, actual selected reading ranges, closest work and unexecuted alternatives.
- [accepted conditional results](../../results/revision-20261022/README.md): complete favorable/adverse results, resources and source limitations.

The source successfully compiled with the desktop editor's built-in LaTeX compiler. That interface returns diagnostics without exporting a standalone PDF. The supplied PDF is independently typeset from the same structured content with ReportLab 4.4.9 and pypdf 6.10.0; it is **not an export of the TeX compiler**. Another TeX environment can produce different fonts and pagination.

Document checks reconcile all 642 source text, table-cell, generated-heading and caption units to the supplied PDF text, excluding only its 17 observed page-number footers. The current revision adds the separate eight-floor/four-horizon AR diagnosis and a verified prospective payment-liquidity precedent. Treasury AR horizon crossings and adverse binding-floor events are explicit; every original numerical table, equation and figure is unchanged. All sixteen changed body pages2–17 have 90dpi full-page visual checks, split between the root reader and a separate reader. Page1 and the three appended figure streams are byte-identical to their previously checked versions. All20 page boxes and font maps/programs match. No unsupported body-font codepoints or replacement/box/NUL characters were detected. Generated TeX bytes equal the successfully compiled source, and the BibTeX keys match all23 structured references in order. These document checks establish fidelity, not scientific novelty or population forecasting superiority.

The [separate AR diagnostic supplement](../../results/revision-20261022/ar1-diagnostics/README.md) retains all new counts, input/code identities, independent scalar verification, actual resources and the limitation of its manifest-bound retained-attempt audit command. The [payment-ratio/timing note](../../notes/revision-20261022/remaining-payment-ratio-and-path-timing.md) distinguishes a remaining-day resource ratio from a timing-sensitive funding peak and this paper's sampled position target.

From the repository root in the documented existing environment:

```bash
mkdir -p .scratch
python3 -B build_conditional_figures.py --output .scratch/conditional-figure-rebuild-01
python3 -B build_tex.py --output .scratch/main-rebuilt.tex
python3 -B build_paper.py --output .scratch/paper-rebuilt.pdf
```

Each output must be new. Create the regular task-owned `.scratch/` directory first: it is ignored by version control and is absent in a clean checkout. The figure builder validates accepted aggregate hashes and the full 90/98/388-row inventories before displaying 24 matched-history configurations, three fixed tradeoff comparisons and ten annual points. It writes staged figures and an identity/layout/resource receipt; it does not replace the canonical assets automatically. No source observations or model fitting are involved. The supplied paper builder uses the already approved canonical figure files and accepts exactly one of four ordered inventories: original, earlier revision, restyled earlier revision, or current conditional-study figures. Their source paths are protected against output overwrite.

The scratch TeX output is a regenerated source for byte comparison. It still uses relative `figures/conditional-*.pdf` paths and is not a self-contained compilation folder. For source compilation, open or compile `main.tex` from this `manuscript/working-paper/` directory with the supplied `figures/` alongside it; alternatively copy the complete folder to a new build directory. The desktop compilation already reported above used this complete document layout. No terminal TeX installation was performed or assumed by the three Python commands.

Text rendering requires the four existing macOS Times New Roman files in `/System/Library/Fonts/Supplemental/`; missing fonts stop the build. Font files are not redistributed. The current figures use built-in Helvetica. `requirements-paper.txt` pins the two document dependencies. The first AR-integrated text/PDF build, before subsequent text-only refinements, used 57,688,064 bytes peak process RSS and 0.167 seconds in this environment; one OS thread was observed in both before/after snapshots. The three-figure build used about 36.16 MB RSS and 0.08 seconds, with one thread in its five snapshots. These measured document processes are separate from financial-worker resources and research hours.

The prior 18-page conditional manuscript is preserved at [7588c619](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/7588c619037db0b730bf81bb1e8fc7d7caa15cbe/manuscript/working-paper). The preceding 17-page manuscript is preserved in [repository history at its pre-revision baseline](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/4e8b714f6c603b81158a03e5ef6ed6dae9c4c1f0/manuscript/working-paper). Its original and earlier retrieval results remain in their existing result folders and Appendix B. Raw observations and third-party paper PDFs are excluded from public delivery.
