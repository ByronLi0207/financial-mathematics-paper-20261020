# WP7 main and title-page visual QA

Date:23 October2026. Scope:actual image review of **all18 current main-preview pages and the separate one-page title preview**, at the supplied110dpi. The reviewer used `view_image` with original detail on each of the19 individual PNGs, in page order; no page was credited from text extraction, thumbnail inventory or successful rendering alone. The PNGs were already rendered by root. No PDF, document, source, figure, financial input or result was modified; no financial task, install, deletion or UI action was performed. This note is the only newly written artifact.

**Layout disposition:PASS, with one nonblocking P3 editorial duplication.** No clipping, overlapping text, missing-glyph boxes, visibly lost mathematical symbols, detached table headers, unreadable legend, truncated caption, or page-number collision was found in the inspected images. Body text, tables, plots and reference text are readable at the actual supplied resolution. This is a visual check of the separate ReportLab previews, not a visual certification of an independently compiled TeX PDF or a journal-submission readiness claim.

## Exact reviewed PDFs

| File | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| `submission-jof/manuscript-preview.pdf` |18|406221|`2b3f5f425cd60c6b04354a454f40cd1bc7f7cad08376a1e72e03d27da3a7ef91`|
| `submission-jof/title-page-preview.pdf` |1|82874|`2717efc6348f45a8433eeb417a74c60114caa980b8c80fb71520083d2c7ef661`|

The main hash exactly matches root's nominated current PDF. `pdfinfo` independently reports18 and1 pages, A4 `595.276 x841.89pt`, no encryption, no form and no JavaScript. Its subject explicitly says “ReportLab preview; not native compiler PDF export”. All19 viewed PNGs have dimensions **910×1287**. The footer's separate-preview wording is legible and consistent with that scope.

## Per-page actual-view evidence

| Page/image | Distinct visible evidence inspected | Visual disposition |
|---|---|---|
| Main1 | Two-line title; abstract with12.660%,14.77%,360→376; keywords and Introduction; measured-source motivation and Treasury illustration text. | Title and paragraphs fit within margins; no broken glyphs or text/footer collision. |
| Main2 | Figure1 line plot, three legend styles, peak/endpoint/floor annotations, economic-date axis and complete caption; contribution paragraphs below. | Plot labels/legend and caption readable; no annotation/caption overlap. The final contribution paragraph continues normally on page3. |
| Main3 | Contribution continuation; Related literature heading; seven-column Table1 with all8 study rows; endpoint and path-literature paragraphs. | Caption/header/rows fit; fine table text remains readable; no missing cells or clipped right column. |
| Main4 | Literature continuation; Data section; source dates/gaps, Treasury maturity dates and release-vintage limits; source attribution and new budget paragraph. | Dense body text remains aligned and readable; the full budget paragraph is visible above the footer. |
| Main5 | Target/method heading; Table2 including the3 added finite-ACI/SAV/combination rows; target, refit-pool, construction and feature equations; response-scale line at bottom. | Table text wraps within its three columns; formulas/subscripts and final response-scale equation are visible, with no clipping or footer collision. |
| Main6 | QR objective/report equations, scaled-KNN equation and ranks; Proposition1 and Proposition2 statements, inequalities and proof. | Compact math is legible; Greek letters, inequalities and sub/superscripts appear; no overwritten lines or missing-glyph boxes. |
| Main7 | Proposition2 continuation; Proposition3 bounds/proof; known-floor and horizon discussion; Section5 design text and original-primary definitions. | Content fits; one duplicated design heading is visible and recorded below as P3. No clipping or overlap. |
| Main8 | Paired pinball/DM/HAC formulas; separate legacy/new coverage convention; Section6; Table3's4 paired-comparison rows; original FX loss paragraph. | Table3 headers and all figures fit and are readable; no split header or numeric-column overlap. |
| Main9 | Renumbered Table4 additive bridge with3 rows; original FX, year/sparse-grid and Treasury adverse-result paragraphs. | Correct bridge label; text and wrapped row labels are complete; no cutoff in native losses/percentages. Paragraph continuation to page10 is normal. |
| Main10 | Treasury continuation; Figure2's FX and Treasury panels, all24 comparison entries, panel labels and caption; KNN/QR inference paragraph. | Panel columns/positive and negative percentages readable; caption fits below graphic; adequate separation from surrounding text. |
| Main11 | Section7; renumbered Table5 coverage diagnostics with7 rows; scoring/calibration, Murphy and preference-envelope discussion. | Correct coverage-table label; headers/counts/p values readable; body text and page footer separated. |
| Main12 | Figure3 FX QR/rolling-F and Figure4 Treasury QR/frozen-F Murphy curves; plot titles, legends, axes, captions; full added15.00% evidence paragraph. | Both plots and captions fit; original-primary labels and line styles readable; new paragraph remains entirely on page without colliding with footer. |
| Main13 | Section8 transport/robustness; baseline/panel adverse directions; Section9 validation implications and bound qualifications. | Headings and paragraphs have readable hierarchy; no isolated heading at bottom or missing lines. |
| Main14 | Table6 decision map with all6 rows, including state and target-level cautions; Section10 limitations begins. | Long cell text wraps within columns; full table and bottom rule visible; state/target-level scope text is readable. Body continuation on page15 is normal. |
| Main15 | Remaining limitations/prospective-vintage discussion; Section11 conclusion with RQ1/RQ2/RQ3 bold labels and final next-steps paragraph. | Complete paragraphs and visible RQ hierarchy; no clipped conclusion or footer overlap. |
| Main16 | Declarations; explicit author-completion fields; first reference page, including Gibbs/Candès and accented names. | Reference typography is small but readable; no broken DOI/glyph rendering or bottom-row collision. Author placeholders are intentional completion items, not a layout defect. |
| Main17 | Remaining references, including Sussman, Sözen, van den Hoogen, Wisniewski, Xu and Zhou. | Lines wrap inside margins; accented names and reference numbers readable; no clipped ending. Blank remainder follows the completed references. |
| Main18 | Separate Figure captions section; all4 main captions, including economic-date and original-primary qualifications. | Captions are complete and correctly numbered1–4; no duplicate automatic caption prefix or truncation. Remaining whitespace is the separate caption-page layout. |
| Title1 | Two-line title; “author completion required”; author/affiliation/contact/ORCID/funding/conflict fields; running title and repository line. | Complete, readable, nonoverlapping page. Explicit unfilled author fields mean it remains a preparation title page, as labelled. |

## Recorded issue and completion boundary

**P3, main page7:**the numbered heading “5. Research design and transparency” is immediately followed by an identical unnumbered bold “Research design and transparency” subheading. It is a redundant editorial line, not a mathematical, table, figure, data or rendering failure. It corresponds to the section title plus its first subheading block in current JSON (`/sections/4/title` and `/sections/4/blocks/0`). Root was notified during review. No edit was made. Removing it later would change pagination; the changed rendering must then receive an appropriate new visual readback rather than inheriting these PNG hashes automatically.

Main page16 and title page1 retain clearly labelled `[TO BE COMPLETED BY AUTHOR]` fields. These do not prevent visual layout acceptance but do prevent describing this preparation package as author-complete or already submitted. The reviewer did not fill or infer author information.

Tables1–6, Figures1–4 and their visible internal routes were examined. The bridge is now Table4 (page9) and coverage Table5 (page11); the contribution text's Tables3/5 and Figure3/4 references match those visible objects. Supplementary cross-reference strings are legible, but this task did not visually inspect the94-page supplement; its QA is assigned elsewhere. The earlier source/aggregate review supplies scientific/citation checks, not a substitute for these actual page views.

## Viewed-image fingerprints

Each path is under `.scratch/revision-v6/pdf-qa/`. These are hashes of the individual original-detail images actually viewed, not a contact sheet:

```text
de8b08d3118f929e58abe271283d90131dfbee7e27e09faf93de822f4cd98ac7 main-01.png
8fce18c954175f5580b3a68f55ed9535d12d5815e3bfd4d8f28b4a393e612cb4 main-02.png
af4dc0b99e37514c211dac549ede3c8248a03bd920062067cd3688ebe55c9490 main-03.png
de0b0125d447e2c7aa4f225f14fdaea0037f91882bf2f7e720e7939b54502e97 main-04.png
ab6df49f0f6fde20b4116742b9f94467e4364bd33f9ff6afe6e4c9e61f06d579 main-05.png
a6b12eaf13e5deeaf2258f3526569b465c2773b59156e863289478c7ca41d018 main-06.png
8dfc92fcc9cbeb7474676555e982cf2d8860a0c181422cd5e0ef4a98e02678c8 main-07.png
1a78f273677a433cf6d36301ae26c7ebc5520af869fb0ccf2060bea7446cc483 main-08.png
36a2c87cef083340366cdbb00a88be06a970bdc9d590eae47a9f1e31f705d266 main-09.png
1e431bb5cbee95e800b8aae45216f882418767d5e1f295a3cf1b6ee2eb9093e8 main-10.png
2c67b21394233583765ee7e4aed10a28e00d7272c92db47cd770b207059af737 main-11.png
6566a4854d9ea55cc99eb67008279416517b7983d7b3d3c6a6692e3aace27402 main-12.png
be7cf5993d2acd1a1e9069c046e0dc6140ee7ceaea74577c8e7e10927bb417c0 main-13.png
ae276db61a553c4794ce1111191389eaca69159c4c28ecea54ccbbacf1e58362 main-14.png
df8c0bfa8925d93d4dbb27b169e2875ba15ea80869c4539077f3062b214797a7 main-15.png
b85e61a55c9d34140cb4f47556c002bbed7f8176c198850fda1063f71b980813 main-16.png
45c174d47fb37fe93473458d1a5603fdd8390c8cafdbfa24f8a3ee04b81f2d0d main-17.png
d6a52d2b070fb8e2829eea8bcc71cafc5540f64ad13985bb05afd25218da563d main-18.png
28914a1de5e6862913c3469a6b34d95fc39eef17168b1c05e3adfd9b8f9c39b8 title-1.png
```

The actual PDFs and images were fingerprinted after all page views. Their page count and filenames are supplementary integrity evidence; the visual verdict above comes from the19 actual image inspections.
