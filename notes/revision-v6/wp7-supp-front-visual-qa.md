# WP7 supplement front-half visual QA

- Review date: 2026-10-23; completed at approximately 13:18 PDT.
- Branch observed: `revision-v4-jof`.
- PDF: `submission-jof/supplement-preview.pdf`.
- PDF SHA-256, checked before and after visual inspection: `00f8535991b10092bee2628fe5853f3319acc2299545f4f0a185deec81119a67`.
- Scope: physical PDF pages **1-47 of 94**, inclusive. Pages 48-94 are outside this agent's assignment.
- Evidence: every assigned page was opened and visually inspected through `view_image` with `detail="original"`, using the already-rendered 110 dpi PNGs `.scratch/revision-v6/pdf-qa/supp-01.png` through `supp-47.png`. Page 18 was also reopened individually. These are actual image inspections, not a claim based merely on successful rendering or extracted text.
- Work was read-only except for creating this new note. No manuscript/PDF/source/data changes, model runs, installs, deletion, or Claude/cross-model review were performed.

## Result and limits

All 47 assigned pages were visually inspected. **No blocking clipping, overlapping text, missing-glyph boxes, missing figures, cropped captions, broken table rows, or content/footer collisions were observed** at this rendering resolution. The visible formulas, headings, table captions, repeated continuation headers, graph axes, legends, and page numbers are present and readable. This checks the supplied ReportLab preview; it does not certify a separately compiled TeX PDF or the scientific/numerical correctness of formulas/results.

The following **nonblocking readability observations** remain. They do not indicate dropped data or a broken page, but should be considered before calling the typography completely polished:

1. **Status identifiers split inside words:** p3, Table S4, Treasury W52 plain-KNN rows display `IDENTICAL_LOSSES` over two lines (`IDENTICAL_LOSS` / `ES`). On pp17-18, Table S25, the identical-loss decision/status cells split it over three lines (`IDEN` / `TICAL_LOSSE` / `S`). The row heights contain all of the text without collision. A human-readable “Identical losses” or a wider status column would read more cleanly.
2. **Long numerical strings wrap inside a number:** pp36-37, Table S41, the `Grid n/hits/rate` column wraps the last digit(s) of some FX rates to the next line (for example the first p36 row's `947/42/0.04435058` displays its final `8` below). On p47, Table S50, `Status; book p` wraps the bookkeeping probability inside its decimal or exponent (the first row shows `OK; book=0.0024` then `48895`). The complete strings remain inside their cells, but the line breaks make transcription harder. Formatting these long repeated values more compactly, or changing the column widths, would improve reading.
3. **Tight H/W-to-procedure gutter:** pp34-35 and p38, Tables S39/S40/S42, the longest `H24 / W260` or `H6 / W2880` entries come close to the following procedure name. They remain distinguishable and do not visibly overlap. A little extra gutter or a deliberate two-line H/W entry would improve separation.

## Per-page actual-image inspection record

Every row below records an actual full-page image inspection; “clear” means no blocking visual defect was observed on that page. Image filenames are relative to `.scratch/revision-v6/pdf-qa/`.

| PDF page | Image inspected | Visible material and checks | Finding |
|---:|---|---|---|
| 1 | `supp-01.png` | Supplement title; S1 introduction; notation Table S1 and selected-parameter Table S2; title wrapping, table widths, footers checked. | Clear. |
| 2 | `supp-02.png` | FX results Table S3; multiline DM/HLN entries; right column and lower table rule checked. | Clear. |
| 3 | `supp-03.png` | Treasury Table S4 and robustness prose; table cells, lower paragraph and page boundary checked. | Clear; nonblocking status-token wrap described above. |
| 4 | `supp-04.png` | Continuation of robustness prose; Tables S5-S8; captions, table-to-table spacing, all columns and rules checked. | Clear. |
| 5 | `supp-05.png` | Panel summary Table S9 and mature-method Table S10; discussion; S2 opening with inline bounds. | Clear; formula line stays within margins. |
| 6 | `supp-06.png` | S2.1 projection bounds and S2.2 envelope plateaus; displayed and inline formulas, subscripts/superscripts, bottom paragraph checked. | Clear. |
| 7 | `supp-07.png` | S2.3 constructed examples Tables S11/S12; S2.4 recursion formulas; S3 opening. | Clear; formulas and table captions fit. |
| 8 | `supp-08.png` | Historical Tables S13/S14; prose; S4 opening; bottom-of-page paragraph continuation checked. | Clear. |
| 9 | `supp-09.png` | S4 numerical conventions; primal/dual objective and equivalent-peak formulas; S5 opening. | Clear; long math strings remain within text area. |
| 10 | `supp-10.png` | Horizon-coherence Table S15; floor discussion and fixed-terminal evidence formulas. | Clear; displayed integrals/subscripts readable and lower prose does not collide with footer. |
| 11 | `supp-11.png` | Table S16; ordinary-rank ablation and two-report formula. | Clear. |
| 12 | `supp-12.png` | Rank-ablation Table S17; S6 preference objective and explanatory prose. | Clear. |
| 13 | `supp-13.png` | Frontier Tables S18/S19; S7 loss-menu Tables S20/S21; wrapped interior boundaries and last table bottom checked. | Clear. |
| 14 | `supp-14.png` | AR comparison Table S22 and preference Table S23; replay formulas; annual/grid sensitivity. | Clear; no formula or lower-text clipping. |
| 15 | `supp-15.png` | S8 reproduction text, S9 inference text, Murphy Table S24; long URL and source paths checked. | Clear; long URL wraps inside text area. |
| 16 | `supp-16.png` | Table S25 beginning; multiline decision/status header and rows; last row and page number checked. | Clear. |
| 17 | `supp-17.png` | Table S25 continuation with repeated headers; transition from FX to Treasury; row containment checked. | Clear; nonblocking status-token wrap described above. |
| 18 | `supp-18.png` | Table S25 final continuation; repeated header, complete bottom rule, S10 transition and prose checked; image reopened alone. | Clear; nonblocking status-token wrap described above. |
| 19 | `supp-19.png` | Shrinkage Tables S26/S27; S11 bound proof and simulation prose; mathematical glyphs checked. | Clear. |
| 20 | `supp-20.png` | AR Table S28, L-comparison Table S29, corrected-process formulas and text continuation. | Clear; formulas fit above bottom margin. |
| 21 | `supp-21.png` | Simulation continuation and marginal threshold formula; Table S30; explanatory prose. | Clear. |
| 22 | `supp-22.png` | Sensitivity Table S31; horizon-limit formula; S12 opening. | Clear; table is contained and formula legible. |
| 23 | `supp-23.png` | Long panel Table S32 first page; all column headers, compact numerical rows, final row above footer checked. | Clear; continuation is intentional and no row is cut. |
| 24 | `supp-24.png` | Table S32 final rows with repeated header and closing rule; prospective text; S13 and FHS formulas. | Clear; final displayed formula does not touch footer. |
| 25 | `supp-25.png` | POT and QRF method text/formulas; complete method Table S33; final row/rule checked. | Clear; dense page is contained. |
| 26 | `supp-26.png` | Paired comparison Table S34 first page; caption and all 10 columns, bottom rows checked. | Clear; continuation is intentional. |
| 27 | `supp-27.png` | S34 continuation with repeated header/closing rule; failure reasons; tolerance formula and NA Table S35. | Clear. |
| 28 | `supp-28.png` | S14; Figures S1 and S2 as vector/text panels; titles, column labels, numeric values, captions and panel spacing. | Clear; panels and captions do not overlap. |
| 29 | `supp-29.png` | Annual comparison Figure S3; FX Murphy graph Figure S4; legends, ticks, axes, curves and both captions. | Clear; no cropped axis labels or captions. |
| 30 | `supp-30.png` | Treasury Murphy graph Figure S5; S15; budget Table S36, oracle Table S37 and prose. | Clear; graph/legend/caption and dense lower page all fit. |
| 31 | `supp-31.png` | Exact-gain bridge, artificial examples and beginning of positioning source locators; dense prose and bottom continuation. | Clear. |
| 32 | `supp-32.png` | Positioning evidence continuation and S16 benchmark introduction; bold source labels, citation strings and lower paragraph. | Clear. |
| 33 | `supp-33.png` | Inventory Table S38; delayed-ACI and SAV method prose/formulas. | Clear; section uses substantial whitespace without omitted visible content. |
| 34 | `supp-34.png` | WP2 evaluation Table S39; all rows, NA reason wrapping, table closure. | Clear; tight H/W/procedure gutter described above. |
| 35 | `supp-35.png` | Control Table S40; coverage-diagnostic explanation; table/body separation. | Clear; tight H/W/procedure gutter described above. |
| 36 | `supp-36.png` | Coverage Table S41 first page; eight headers, narrow long-string columns, NA text and bottom rows. | Clear; nonblocking numerical-string wraps described above. |
| 37 | `supp-37.png` | Coverage Table S41 continuation; repeated headers and closing rule; all rows remain inside cells. | Clear; nonblocking numerical-string wraps described above. |
| 38 | `supp-38.png` | Validation Table S42; initial-calibration reasons and complete last row. | Clear; tight H/W/procedure gutter described above. |
| 39 | `supp-39.png` | Gamma-inventory Table S43 first page; repeated-context row spacing, status/selection columns, lower row. | Clear; continuation is intentional. |
| 40 | `supp-40.png` | Table S43 second page; repeated headers and three-line Treasury context cells. | Clear; continuation is intentional and no split row was observed. |
| 41 | `supp-41.png` | Table S43 final page; full NA/not-run reasons in cells and closing rule. | Clear. |
| 42 | `supp-42.png` | State-range Table S44; two-line alpha ranges, numerical bounds and NA states. | Clear. |
| 43 | `supp-43.png` | Clipping/feedback Table S45; context wrapping, cumulative-feedback heading and NA reasons. | Clear. |
| 44 | `supp-44.png` | Wrapper/base difference Table S46; closely spaced long headings, signed values and NA rows. | Clear; headings remain distinct. |
| 45 | `supp-45.png` | QR contrast Table S47 and SAV inventory Table S48; caption/table spacing and multiline NA reason. | Clear. |
| 46 | `supp-46.png` | Operational-summary Table S49; scientific-notation quantities, conditional overrun counts and row spacing. | Clear; values remain inside columns. |
| 47 | `supp-47.png` | Ranking-family Table S50 first page; multiline contrasts and status/bookkeeping p column; last row above footer. | Clear; nonblocking numerical-string wraps described above. Continuation beyond scope must be checked by the pages 48-94 reviewer. |

## Handoff

- Coverage is exactly **47/47 assigned pages**; this report makes no claim about pages 48-94.
- Observed nonblocking issues are display/presentation items only. No financial runs or numerical recomputations are needed to reproduce the observations.
- If the preview is regenerated, this hash-bound inspection is no longer a signoff for the new PDF; affected pages should be visually reinspected.
