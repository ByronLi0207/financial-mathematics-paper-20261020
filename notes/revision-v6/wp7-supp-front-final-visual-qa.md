# WP7 updated supplement front-half visual QA

- Date: 2026-10-23; full assigned-page image review completed at approximately 13:28 PDT.
- Branch: `revision-v4-jof`.
- PDF reviewed at the start of this pass: `submission-jof/supplement-preview.pdf`.
- Start-of-pass PDF SHA-256: `3a20a0dc17652cf0a7243822608134d91c13b40bb5ca7cd1304fbcfbed347888`.
- Actual visual evidence: `.scratch/revision-v6/pdf-qa-v2/supp-01.png` through `supp-47.png`, rendered at 110 dpi. Every assigned image was opened through `view_image` with `detail="original"`; pages 18, 35, and 38 received additional focused image rechecks.
- Scope: physical PDF pages **1-47 of 94**, inclusive. No claim is made here for pages 48-94.
- Prior note `wp7-supp-front-visual-qa.md` was preserved unchanged. This pass created only this new note; no manuscript/source/PDF/data edits, financial runs, installations, deletion, or Claude/cross-model review were performed by this agent.

## Version boundary

The full-page inspection below is bound to the **v2 images and the start-of-pass PDF hash `3a20a0dc...`**. Before this note was written, the root agent had begun the separately announced caption-only correction `on277` to `on 277`; the current PDF hash had advanced to `4887efcb02124612df5b5782f1dbdfb214102e3df108739fdcccc1f17ab9e495`. This note therefore does **not** assert that the subsequently replaced PDF received another full visual pass. The root agent will compare all 94 newly rendered PNG hashes against v2; if only p23 differs, the new p23 requires actual image review and a version-binding addendum. The actual inspections recorded here remain valid evidence for pixel-identical pages.

## Result

All **47/47 assigned updated pages** were actually visually inspected. No blocking clipping, text overlap, missing-glyph boxes, broken/split table rows, missing/cropped figures, cropped captions, or content/footer collisions were observed at 110 dpi. Continuation tables retain their headers and complete visible rows. Formula glyphs, captions, graph labels and page numbers are readable. This is a visual check of the supplied ReportLab preview, not a scientific recalculation, exhaustive numeric equality audit, or certification of a separate TeX compilation.

Focused outcomes:

- **New ACI update on p33:** the text visibly initializes `alpha=.05`, defines newly matured strict-hit feedback, and displays the sequential projected update `alpha <- min(1,max(1/(m_t+1),alpha+gamma(.05-err_i)))`. The current completed-score pool size and immediate-before-next-report projection are explained. All math and prose fit inside the page without overlap or missing glyphs.
- **pp36-37 Table S41 numerical wrapping improved:** slash-separated grid quantities now have separator whitespace. Long rates move as complete numerical tokens to the next line. For example, the first p36 row shows `947 / 42 /` and the whole `0.04435058` below, instead of placing the final digit on a separate line. Repeated table headers and row heights remain intact.
- **p47 Table S50 bookkeeping probabilities improved:** status cells show `OK; book=` and the whole decimal or scientific-notation probability on the next line. For example `0.002448895` and `3.325628e-10` are each intact. No digit tail or exponent is separated from its number.
- **H/W-to-procedure separation improved:** the fields on pp34-35 and p38 are distinguishable, including long H/W entries. Focused rechecks on pp35/38 found no overlap.
- **Numerical displays remain readable:** the original results/tables retain complete visible numeric strings at inspected locations. No values were recomputed; full source-data/value invariance remains the root agent's integrity-check responsibility.

Remaining nonblocking observations in this exact v2 rendering:

1. p3 Table S4 and pp17-18 Table S25 still split `IDENTICAL_LOSSES` across lines inside the status token. The complete strings are retained in their cells without collision. This is a readability item, not a lost-data or broken-layout issue.
2. p23 Table S32 caption visibly says `on277` without a space. This was reported to the root agent, who announced the separate caption-only fix described in the version boundary above.

## Per-page actual-image record

All filenames below are relative to `.scratch/revision-v6/pdf-qa-v2/`. “Clear” means no blocking visual defect observed in that actual full-page image.

| PDF page | Image actually viewed | Material and checks | Finding |
|---:|---|---|---|
| 1 | `supp-01.png` | Title; added QR33/C2 abbreviation explanation; Tables S1/S2; last paragraph and footer clearance. | Clear; added lines fit. |
| 2 | `supp-02.png` | FX Table S3; rightmost DM/HLN entries, captions, rules and page number. | Clear. |
| 3 | `supp-03.png` | Treasury Table S4 and robustness prose; lower paragraph continuation. | Clear; nonblocking status-token wrap remains. |
| 4 | `supp-04.png` | Robustness continuation; Tables S5-S8; caption/table spacing and all columns. | Clear. |
| 5 | `supp-05.png` | Tables S9/S10, discussion, S2 opening and inline geometry formulas. | Clear. |
| 6 | `supp-06.png` | S2.1/S2.2 proof text; displayed bounds, subscripts/superscripts and bottom paragraph. | Clear. |
| 7 | `supp-07.png` | Tables S11/S12; S2.4 recursion formulas; S3 transition. | Clear. |
| 8 | `supp-08.png` | Tables S13/S14; expanded RMS wording; S4 beginning and page-bottom continuation. | Clear. |
| 9 | `supp-09.png` | Numerical conventions; objective/dual and peak-parameter formulas; revised S5 heading. | Clear. |
| 10 | `supp-10.png` | Table S15; report-order discussion and evidence formulas/integral; last paragraph. | Clear. |
| 11 | `supp-11.png` | Table S16; empirical-rank ablation text and two-report equation. | Clear. |
| 12 | `supp-12.png` | Table S17; S6 preference objective and interval explanation. | Clear. |
| 13 | `supp-13.png` | Tables S18/S19 frontier rows and S20/S21 loss menus; bottom table/footer gap. | Clear. |
| 14 | `supp-14.png` | Tables S22/S23; capitalized AR headings, replay formulas and annual/grid sensitivity. | Clear. |
| 15 | `supp-15.png` | S8 reproduction and S9 inference text; URL wrapping; Table S24. | Clear. |
| 16 | `supp-16.png` | Table S25 first page; multiline last header, rows, and bottom clearance. | Clear. |
| 17 | `supp-17.png` | Table S25 continuation; repeated headers; source transition and status cells. | Clear; nonblocking status-token wrap remains. |
| 18 | `supp-18.png` | Table S25 last page, repeated headers, bottom rule and revised S10 heading; focused recheck also performed. | Clear; nonblocking status-token wrap remains. |
| 19 | `supp-19.png` | Tables S26/S27; S11 proof and simulation text; math glyphs. | Clear. |
| 20 | `supp-20.png` | Tables S28/S29; corrected-process section; several displayed formulas and lower continuation. | Clear. |
| 21 | `supp-21.png` | Simulation continuation; marginal-threshold formula; Table S30 and explanatory paragraphs. | Clear. |
| 22 | `supp-22.png` | Table S31; revised random-stream wording; horizon-limit formula; S12 opening. | Clear. |
| 23 | `supp-23.png` | Table S32 beginning; long compact table, complete bottom row and caption. | Clear layout; `on277` caption copy-spacing item reported. |
| 24 | `supp-24.png` | Table S32 final rows and header; prospective text; revised S13 title; FHS formulas. | Clear. |
| 25 | `supp-25.png` | POT/QRF text and formulas; Table S33; last row and bottom rule. | Clear. |
| 26 | `supp-26.png` | Table S34 first page; full-width table, scientific notation and bottom rows. | Clear; intentional continuation. |
| 27 | `supp-27.png` | S34 continuation; retained-failure text; tolerance formula and Table S35. | Clear. |
| 28 | `supp-28.png` | Figures S1/S2; titles, labels, values, source-unit notes and captions. | Clear. |
| 29 | `supp-29.png` | Figure S3 annual panels and Figure S4 FX graph; legend, ticks, axes, lines and captions. | Clear. |
| 30 | `supp-30.png` | Figure S5 Treasury graph; S15, Tables S36/S37 and lower prose. | Clear. |
| 31 | `supp-31.png` | Revised capitalization; gain bridge, math illustrations and dense positioning locators. | Clear. |
| 32 | `supp-32.png` | Positioning continuation and S16 with expanded ACI/SAV definitions; lower prose. | Clear; added text fits above footer. |
| 33 | `supp-33.png` | Table S38; new ACI initialization, strict-hit feedback and projected update; SAV text/formulas. | Clear; new update readable in full. |
| 34 | `supp-34.png` | Table S39; H/W and procedure columns, NA reasons, final row. | Clear; field separation readable. |
| 35 | `supp-35.png` | Table S40 and coverage explanation; H/W/procedure gutter; focused recheck performed. | Clear; no overlap. |
| 36 | `supp-36.png` | Table S41 beginning; new separator whitespace; whole rate tokens and NA cell wrapping. | Clear; prior numerical-tail wrap improved. |
| 37 | `supp-37.png` | Table S41 continuation; repeated header, whole rate tokens and closing rule. | Clear; prior numerical-tail wrap improved. |
| 38 | `supp-38.png` | Table S42; long H/W fields, NA reasons and last row; focused recheck performed. | Clear; no overlap. |
| 39 | `supp-39.png` | Table S43 beginning; header and many multiline context rows, lower row. | Clear; intentional continuation. |
| 40 | `supp-40.png` | Table S43 second page; repeated headers, Treasury contexts and values. | Clear; intentional continuation. |
| 41 | `supp-41.png` | Table S43 final page; complete not-run/initial-calibration reasons and closing rule. | Clear. |
| 42 | `supp-42.png` | Table S44; alpha ranges, rank bounds, context wrapping and NA rows. | Clear. |
| 43 | `supp-43.png` | Table S45; feedback headings, quantities and retained NA reasons. | Clear. |
| 44 | `supp-44.png` | Table S46; signed decimal differences and distinct neighboring headers. | Clear. |
| 45 | `supp-45.png` | Tables S47/S48; contrast headings, multiline NA reason and intertable separation. | Clear. |
| 46 | `supp-46.png` | Table S49; scientific-notation quantities, conditional counts and row spacing. | Clear; numerical strings are contained. |
| 47 | `supp-47.png` | Table S50 beginning; contrast labels, status/bookkeeping probability column, last row. | Clear; whole probability tokens now remain intact. Continuation beyond this page is outside this agent's scope. |

## Handoff

The v2 full-pass coverage is exactly **47/47 assigned pages**. The root agent should attach the announced v3 PNG-comparison result and actual p23 image check before binding these observations to the later caption-corrected PDF. This note does not certify pages 48-94 or any changed image that has not been viewed.

## Final v3 addendum: version binding completed

This addendum supersedes the pending v3 inspection/binding statements above. The final current PDF SHA-256 was verified as **`4887efcb02124612df5b5782f1dbdfb214102e3df108739fdcccc1f17ab9e495`**.

- Read the root agent's `notes/revision-v6/wp7-final-raster-identity.json`, which contains 94 page comparison records and reports `changed_pages: [23]`.
- Independently rehashed both v2/v3 PNG files for **all 47 assigned pages**, verified their hashes against that JSON, and confirmed **46 byte-identical assigned page pairs** with **only p23 changed**. This binds the actual v2 full-page inspections for pp1-22 and pp24-47 to those same final v3 pixels.
- Actually opened and inspected `.scratch/revision-v6/pdf-qa-v3/supp-23.png` with `view_image`, `detail="original"`. Its SHA-256 is `bbd8e1153bae262a275326c19b12966dfbc78eb292285c8c82598082c9542298`. The caption now visibly reads **“All methods complete on 277 evaluation origins in every cell.”** The inserted space does not add a caption line, shift the table, cut a row, or collide with the page number/footer. The table remains fully contained on this continuation page.

**Final assigned-scope result: pp1-47 are covered for the final PDF hash above by actual full-page v2 inspections plus exact final-image identity for unchanged pages, and a fresh actual-image inspection for changed p23. No blocking visual defects were observed.** The p23 copy-spacing issue is resolved. The contained `IDENTICAL_LOSSES` line wrapping on p3 and pp17-18 remains a nonblocking presentation observation. The pp36-37 and p47 whole-number wrapping improvements and readable p33 ACI update are preserved by exact PNG identity.
