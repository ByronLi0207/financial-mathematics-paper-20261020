# v8 submission-package inventory and B7 check route

This is a read-only B6 inventory and acceptance checklist. It does not certify refreshed PDFs or the ZIP before root's final compilation. At the initial inventory the checker had only been syntax-parsed. Corrected B6 execution results are recorded below; they certify the current exported bytes, while root's B7 per-page review and publication checks remain separate.

|Role|Required current package files|Check|
|---|---|---|
|Default main entry|main.tex → manuscript.tex|The wrapper includes the current manuscript; all ZIP inputs resolve inside the ZIP.|
|Main, Supplement, title sources|manuscript.tex; supplement.tex; title-page.tex|Native labels/citations resolve; Abstract matches supplied B3 prose; Keywords synchronized; author placeholders preserved.|
|Main figure inputs|figures/v8-endpoint-peak-example.pdf; figures/v7-murphy-fx_hourly.pdf; figures/v7-murphy-nyfed_weekly.pdf; figures/v8-calibrated-mc.pdf|Exactly these four appear in the main and source ZIP; MC figure equals saved results/v8/mc/mc-main.pdf. Figure1 tick formatting changes no source data.|
|Publication metadata|references.bib; README.md; AUTHOR-TODO.md; cover-letter.md|Current v8 route and source restrictions; the three finding footprints remain present in five locations; declarations remain placeholders.|
|Delivered PDFs|manuscript.pdf; supplement.pdf; title-page.pdf|Current source/PDF fingerprints agree with compile receipts; native LaTeX producer; main<=18 pages; title=1 page.|
|Compatibility previews|manuscript-preview.pdf; supplement-preview.pdf; title-page-preview.pdf|Byte-for-byte aliases of current native PDFs.|
|Source snapshots|manuscript-content.json; supplement-content.json|schema v8-latex-snapshot; canonical_source basename; source_sha256; exact current latex; source_bindings array of existing ledger paths relative to the JSON directory; historical_v6_schema retained.|
|Portable sources|overleaf-package.zip|All required source/text/bibliography files and four figures; every ZIP member matches its current file; recursive local inputs/graphics present.|
|Optional cover proof|cover-letter.tex and cover-letter.pdf|If either exists, both are required; PDF one page, native producer and current source/receipt binding. Add files to ZIP if used as portable review input.|

At the first B6 inventory, content JSONs still described v7 and the old source ZIP had11 members without the MC figure. This is an expected pre-refresh state. Root owns replacing these derived deliverables after current metadata and Figure1 are ready; those old observations are not final acceptance results.

Metadata contract: the exact six Keywords are Peak net positions; Quantile forecasting; Historical benchmarks; Forecast comparison; Calibration; Dealer positions. The title-page running title remains Historical Rules and Peak Limits (32 characters). Keywords may be a single plain or textbf line separated by semicolons/commas; main/title order and text must match.

B0 author-placeholder contract, observed directly during the initial v7 readback: main has five exact fields (Author information, ORCID, Funding, Competing interests, AI statement); title has six (Authors and affiliations, Corresponding author and contact, ORCID, Funding, Conflict of interest, AI statement); cover has one final signature; Supplement has zero. Every value remains [TO BE COMPLETED BY AUTHOR]. No identity, funding or declaration is inferred.

Supplement cross-reference contract: section label sup:v8-calibrated is S26; table label tab:v8-mc-loss is TableS29; tab:v8-mc-predictions is TableS32. The checker counts actual numbered source sections/captioned tables and also inspects the compiled Supplement text in full mode. Main's plain Supplement TableS32 reference points to the frozen-predictions table, not the loss table, and must match that label. All ordinary local labels/references and native citation keys must resolve.

For Abstract checking, the default provided source is notes/v8/b3-prose.json, field abstract. Current B3/B4/B5 Abstract remains that text. If root intentionally changes the authorized abstract source, pass --abstract-source to its replacement JSON; do not edit the checker to silently accept drift. Budget is<=170 words and<=10 numeric occurrences, using the PR3 word/number token regexes.

The package check proves the three numeric finding groups appear in Abstract, Introduction, Section2, Conclusion and cover letter. The independent contribution review owns their semantic distinction: matched versus rolling reference, later-period wrapper only, and original-comparison Murphy crossings. Token presence alone is not semantic proof.

## Commands after root requests the checks

Source-only mode while derived files are still being refreshed:

```text
python3 -B notes/v8/check_package_v8.py --source-only --output notes/v8/package-source-check.json
```

Full B7 mode after final compilation, aliases, snapshots and ZIP refresh:

```text
python3 -B notes/v8/check_package_v8.py --compile-receipt notes/v8/package-compilation.json --output notes/v8/package-final-check.json
```

Both output paths are explicit and exclusive-create. The checker does not overwrite an earlier result, compile anything, extract the ZIP, run research code, read raw inputs, access Git or publish a package. Full mode requires pypdf from the existing runtime.

The root's compile receipt format is documents keyed by manuscript, supplement, title-page, plus optional cover-letter. Each item has source_sha256, pdf_sha256, producer and pages. Extra command/log provenance may be kept. Native PDF metadata alone is not evidence of current-source compilation, so full mode requires both the receipt fingerprints and actual file metadata. Root's final per-page visual review remains separate.

## Corrected B6 source-check assumptions

The retained notes/v8/package-source-check.json failed on two checker assumptions, not document defects: it incorrectly expected the loss table to beS32, and expected the preserved v7 Figure1 filename. The checker now independently requires the loss label to resolve toS29 and predictions label toS32, with the calibrated section stillS26. The current Figure1 input is figures/v8-endpoint-peak-example.pdf, as planned. Existing checker and inventory drafts were preserved in .bak files before these corrections. The failed check JSON remains unchanged.

Root has refreshed the native four-document exports, aliases, v8 source snapshots and17-member source ZIP. Its compile receipt records16/25/1/1 pages for manuscript/Supplement/title/cover. These are receipt observations; the corrected source and full checks are run to new output paths and their results are appended below. README's wording still distinguishes the latest pre-B7 checkpoint from final B7 acceptance; no earlier15-page checkpoint is treated as the delivered16-page proof.

## Current B6 execution results

- `notes/v8/package-source-corrected.json`: **PASS**,73 assertions,0 failures. The earlier `package-source-check.json` remains an unchanged historical FAIL from the two incorrect checker assumptions described above.
- `notes/v8/package-b6-check.json`: retained historical FAIL, six ledger-path assertions only. The content snapshots correctly use `../notes/...` relative to their own `submission-jof/` directory; the first checker incorrectly resolved them against the repository root. The corrected checker resolves paths relative to the snapshot directory and additionally requires every resolved ledger to remain inside this repository and exist.
- `notes/v8/package-b6-corrected.json`: **PASS**,145 assertions,0 failures. Native PDF current-source fingerprints and producers,16/25/1/1 pages, three preview aliases, both exact v8 content snapshots, all source ledger paths,17-member ZIP byte identity and all package TeX/figure inputs passed. S26, loss TableS29, and frozen-prediction TableS32 were checked separately.

No remaining package inconsistency was found by the corrected checks. These readbacks do not replace root's final source/figure semantic audit, per-page visual review, full test run, final README/manifest update or authorized branch push. No previous FAIL receipt was edited or removed. Checker and inventory versions preceding each correction remain in `.bak` files.
