# H2 QF corrected-cut full-page visual review

Reviewed 2026-10-27T04:01:30.570069+00:00

**PASS for layout, with one nonblocking P3 punctuation observation. All 22 new main pages were directly opened individually using view_image with original detail. No body/equation/figure/page-number collision, clipping, or left/right overflow observed.**

Current main SHA-256: `766a22842b2588cce25b3b22becf418f5095f10efa146dd72296290abac4e807`. Both start/end checks agree with the corrected render manifest. All 22 PNG hashes match. Supplement SHA remains `f6ac52d32d69c75ddfdf48cec6c7af53a3893473ea4ae1a346a8a5ced8f7868c`; its 40-page prior direct coverage is retained by exact PDF and PNG identity. Current coverage is 22 new plus 40 carried pages = 62 pages. Supplement was not newly re-viewed in this follow-up.

## Resolved old findings

- Former equation/page-number collision: resolved. Equation now fully on page 4, with a clear footer gap.
- Footer clearance: all 22 new pages directly checked; text, formulas and captions separated from page numbers.
- Page 19 Data availability. and page 20 Code availability.: each has one full stop.
- Page 22 Wisniewski2020: one Proceedings of the prefix, with bibliographic year/volume/pages/editors retained.

## Remaining nonblocking observation

QF-C-01 - P3_NONBLOCKING: p10, Italic-bold paragraph label A fixed CFTC history-length extension... Doubled full stop remains in this separate label. It is outside the two exact Data/Code label conversions and does not affect content or readability. Recorded only; no source change requested or made by reviewer.

## Geometry, template and precise conversion rules

Geometry receipt: US Letter; left/right 22 mm, top/bottom 24 mm, include header/footer, header height 14 pt, header separation 15 pt, footer skip 20 pt, offsets zero. Actual text height 609.39677 pt; the previous class setting was 676 pt with a 4 pt footer skip. All new rendered pages were checked after that correction.

Only the exact Data availability. and Code availability. paragraph source labels omit their final source full stops because the unchanged class supplies them. No general punctuation normalization is claimed. The scientific-body equivalence receipt permits these two label changes and citation-group ordering. Derived Wisniewski2020 booktitle removes only the literal existing Proceedings of the prefix supplied automatically by the unchanged official bibliography style.

Publisher class and BST were again compared byte for byte to the official cached ZIP: unchanged. Class SHA `5ceee7d7f54fcf10f5f992bb21c9018b562ca85e13d375a2ee7cd1ea1bd57f9c`; BST SHA `924f0b2386491926dd630f2b8cbae18926190f1c34eb8c06ea2262210d559fcd`. Cached-font substitutions remain logged, with no visible missing-glyph square in the new pages.

## Numeric, negative-result and structure checks

- Old/new PDF numeric token multisets are equal: 1,158 tokens each, after removing each page final folio and joining a digit-dot-newline-digit DOI line break. This is content-presence support, not numerical recomputation or an ordering certificate.
- Old/new scientific body source signed-numeric token multisets are equal: 388 each, after excluding document preambles.
- Main retains 8 captioned tables and 6 figures; no literal unresolved ?? found.
- Partial support/WP2 PARTLY, upper-tail NA, rejected solver repair, unmet conditions, large losses and retrospective limits remain. Supplement bytes and its failure/counterexample inventories are unchanged.

## New main: individual original-size direct views

| Page | PNG SHA-256 | Direct original view | Observation |
|---:|---|---|---|
| 1 | `83f605a38e831d66bc619ce8b3888c08cfb4e9950d6ffccd8fa2084f9e1cdb38` | Yes | Title, abstract, six keywords and explicit author/affiliation/JEL placeholders intact. Header and footer have whitespace. Final short RQ2 line separated from page number 1; no cropping. |
| 2 | `a55fe5c86b4c37858fa4ca204dcb3f5ef11bc9a1ab50266bf109bb08e25b9bd4` | Yes | Figure 1 full axes, labels, units, legend and caption intact. All three empirical findings and counts visible. Last line clearly separated from page number 2; both side margins clear. |
| 3 | `353c3d8d191d5dfcedcc3ce36d6c916460bdd9388ba8dd2cf3f2f3ccdf0650de` | Yes | Related literature, four-row Table 1 and Section 3 opening complete. No cropped table cell or line. Page number 3 now has clear separation from text; the formerly colliding equation has moved to page 4. |
| 4 | `446175bad17916519581f70863a787d8fd46f094f5274a0c57f81902db486892` | Yes | Peak/floor/headroom identity, pinball/indicator identity and both proposition displays complete. Former p3 collision resolved: equation punctuation and page number 4 do not touch. Wide inequality fits both side boundaries. |
| 5 | `139e1c186d2366e782c8e4934b398cf64b42baf1cc09110b572ae9d989ecc69a` | Yes | Daily/CFTC data counts and timing limitations retained. Table 2 both panels, five source rows, units/peak counts/notes complete. Section 5 opening fits; footer clearly separated. |
| 6 | `6d6143ae84c7a3914e95b562f1b718891e87191f0c23902e5ec6f1b6ed2f1573` | Yes | Historical-quantile equation and full penalized objective with all six penalties complete. Text and wide display fit left/right margins. Calibration/combination/failure limitations retained; footer separated. |
| 7 | `ad48fa720f9cb1e3adf56d095425694e37aeee4cf4478ee56c8477d4a97ec3e6` | Yes | Table 3 complete methods, menus and notes visible. Evaluation-design text fits both margins and ends above clear footer gap. No cell/row cropping. |
| 8 | `f2fa0b2400cc5ce31d82cd42096098818bb0da28f7489f56e18a2556c7e96b3b` | Yes | DM/HAC display, Section 6.1/6.2 and 7.1 clear. Quantiles, bootstrap settings and adverse counts retained. Display/paragraphs and page number 8 separated. |
| 9 | `a4fe27d0d70ec1872cbfcecc00a8c040752f063fc35a8179b399fa90a211d4ba` | Yes | Table 4 all five rows with references, issues, signs and strict-breach counts intact. History discussion legible; footer separated. Large lower whitespace is pagination, not missing content. |
| 10 | `6325b4e1307da7652c21e939483d9327093abf483fc6b4fc31d1e1c7c064e812` | Yes | Figure 2 all history points, two series, axes and caption intact. WP2 extension retains partial support, failed high-history screen, 10/17, 6/17 and counterexample boundary. One minor doubled full stop remains in the italic-bold extension label. All body/footer margins clear. |
| 11 | `ff3625c9c3100182d64dcade2598ba6ff695db51eb2f0ff77deb368ec3bb6159` | Yes | Table 5 all eight rows, adverse results and unmet-criterion note intact. CFTC and MCS subsection text clear and inside boundaries. Footer separated. |
| 12 | `310b2d213bf0839b29569967e99278eb0402ee4571b552a3b28b094fb2c9aa04` | Yes | Table 6 all seventeen literal contract codes and both histories complete. Positive/negative entries and missing/failure interpretation note intact. No clipped row/column or footer collision. |
| 13 | `6f26be63f7a3f1689ecef3bdc404c6800e68f1dd9c8f3cf3b1f132af8bf4ade0` | Yes | Figure 3 both histories and all seventeen contract labels/points intact. NA and dependence limitations retained. Caption inside boundaries with clear footer space. |
| 14 | `2b58c1a952da141290cfd33ed825082f0be14c647653886a13b7cf60d141739b` | Yes | Section 7.4 decomposition text and Figure 4 both panels intact. Unavailable crosses and full planned index remain. Caption, following text and footer separated; no side clipping. |
| 15 | `61771eb06c51e6a5e5005bcd42a68861bb8f07095bed32d84b6b74c01a87a393` | Yes | Table 7 four source/horizon rows and all selection counts intact. Footnote and continuation text complete. Large lower whitespace but no clipping or collision. |
| 16 | `c6d173211e59cdaaf5bb2e12b3a00d9d514e01eefb7c383d72702b8e865deba2` | Yes | Table 8 all five source rows, three upper-tail NA and rejected-repair narrative retained. Scores-versus-breaches discussion and wide cost equation fit both margins. Footer separated. |
| 17 | `4fb4308598c1f0583236242d615f28685f1aee0f509290b6750be93b0d955e20` | Yes | Figure 5 all six panels, completion denominators, axes, common color bar and caption intact. Plot labels/caption clear of margins and footer. |
| 18 | `6bf89adcc822f8c9d2c24e737e78881bc21e67058f418c8716406eef01f9ed4f` | Yes | Figure 6 all three source groups with separate y-scales and complete planned counts intact. Benchmark protocol retains 8/60 adverse cases and 80.98% worst loss. Practical reporting ends above a clear footer gap. |
| 19 | `64574eb40ebde69235da88eaea6035c78d74a02e4702249668c46b01e6556b90` | Yes | Limitations and conclusion intact, including retrospective/whole-cell/failure boundaries. Data availability label has a single full stop. First data paragraph ends above page number 19 without collision. |
| 20 | `2c4a8b3da29be0177f29221c882c9142c7bb556434b77a61d3360596ce65c373` | Yes | Data-rights continuation and long URLs wrap within side boundaries. Code availability label has a single full stop. Author/ORCID/funding/interests placeholders remain. References start normally and final CFTC URL stays above footer. |
| 21 | `8f25bd9915a521e098f672f505168c8fc714e61023f022a7e323dd10fb7338c2` | Yes | Reference continuation, years, volumes, page spans and DOI/URL strings intact. Long links wrap without side cropping. Final thesis entry and page number 21 are separated. |
| 22 | `858ece834e08f396d4e65e38695419cc038e300f018da9726d04edae76801ce2` | Yes | Wisniewski2020 shows one Proceedings of the prefix, with editors, volume 128, pages 285-301, year and PMLR retained. Wisniewski2024 and its URL/year intact. No clipping/collision; footer separated. |

## Carried supplement: byte-identical prior direct views

These pages were actually viewed in the prior H2 review. The current PDF and all these PNG hashes were rechecked unchanged. Existing small-type and uncaptioned-table notes remain; no new direct view is claimed here.

| Page | PNG SHA-256 | Prior direct view retained |
|---:|---|---|
| 1 | `6322ad955bf4a3f62824bb29179545fa60b972116d0fbbcc83d91fd5aa492645` | Yes, by identical PDF/PNG SHA |
| 2 | `65e07737858ddff72864a35986efdbab9640db1d3d6e6d73cc628927d9b9f8b5` | Yes, by identical PDF/PNG SHA |
| 3 | `f583a22847f62a68740daa2ff99c7bddb11732a56577eff3e8e38bb455110061` | Yes, by identical PDF/PNG SHA |
| 4 | `28dfd7300416b2e1f5ade3383d60cc7c2f4b53acad50201cfca004fb4bcf1936` | Yes, by identical PDF/PNG SHA |
| 5 | `df77ff003e39456ddbaf9ff5df57ce5b620a6f475a9dda3c6fdfa306772e8a58` | Yes, by identical PDF/PNG SHA |
| 6 | `740044098d57478233f7d2b191891e488ec5c2c168290bd4ca5ff4c765582d35` | Yes, by identical PDF/PNG SHA |
| 7 | `53310eed9bc8074007c97a915f93b4f497d57c034ff70fd3ae1111235b2ae22b` | Yes, by identical PDF/PNG SHA |
| 8 | `f8055d207426584e33faa00b3cc85073def6f53da9b2c1dc02e660e0b50c5a08` | Yes, by identical PDF/PNG SHA |
| 9 | `7f95d3f0d2878dcc55e48a230e4ecb1c8710d3e5636d70552a686524172b87b8` | Yes, by identical PDF/PNG SHA |
| 10 | `62da5f2b884753bdb831590905832cdb8b41361768dcb214d63f40e1d8d7022b` | Yes, by identical PDF/PNG SHA |
| 11 | `a55531e5425160f4350936d16e2a078ce8023049ec5455f6e8b8f9310e7134ed` | Yes, by identical PDF/PNG SHA |
| 12 | `0e6df4761f0fe32cf232e86ce2b49bf8f00d9981dc435c521a660f01ca17046a` | Yes, by identical PDF/PNG SHA |
| 13 | `028bfd038786e6833fc872158c91084d6216e6e498bbcdeb1f7e4abd047e5b28` | Yes, by identical PDF/PNG SHA |
| 14 | `69907d285b536956d5cbbf3451fb89bbe3a87808eb7c9de0a3776fa4f241b814` | Yes, by identical PDF/PNG SHA |
| 15 | `414313cc26f53c796fc966fc171cb178fd0af7564403951045db711220b2c101` | Yes, by identical PDF/PNG SHA |
| 16 | `075e71af6a4ff010d3414279032b021d7ec6b42979bef2a0c16fe75d0c945828` | Yes, by identical PDF/PNG SHA |
| 17 | `8804052af67bfa5632b1081f83ba3658b4277ba3e1c52ff14544817daefb9f1a` | Yes, by identical PDF/PNG SHA |
| 18 | `f78d8660e8637a257c232fb9ae7eb9473826f5783bbc9c0420173fc67a453f29` | Yes, by identical PDF/PNG SHA |
| 19 | `36fc53f56bae6ebd73ba754aca0175bfb2c82575035e28c1411d5aef689c62ce` | Yes, by identical PDF/PNG SHA |
| 20 | `a4749d4c2a9f4578d26c822e22c8fe4c43af157e84da197dd1702b6821d751eb` | Yes, by identical PDF/PNG SHA |
| 21 | `b6f246f407dbb4c07f8be9be56f38b5923a6f14795b79f17659cf15ed2537848` | Yes, by identical PDF/PNG SHA |
| 22 | `17f5af48585f2e08ab72c16aad3a3335c10d3e90183207bc6d6460146666af8b` | Yes, by identical PDF/PNG SHA |
| 23 | `c0eab9aaf03c625b2d077b2f1deae4ba5e4e4c5ee52f3a3e23bc8c5fe4fd74c9` | Yes, by identical PDF/PNG SHA |
| 24 | `2632dd4837708d906615fd5923b4fc6579cb78dd05b0931cc8ea49fadd3acfdb` | Yes, by identical PDF/PNG SHA |
| 25 | `9cacdede0b7aa201b4a269fe973f772b1e4006557817553d67b00986c12a2169` | Yes, by identical PDF/PNG SHA |
| 26 | `ed43fde1c628e4de9e16c07346205f40359168343acd9dbb3c4456f57c31a7bc` | Yes, by identical PDF/PNG SHA |
| 27 | `6f5b837a329d0ab1b338b4e24ee38e97972890e7c7209fe254e3fdf2f8b4e663` | Yes, by identical PDF/PNG SHA |
| 28 | `3ecdf339a5da092d09aaece98c27d2f71e3b2836427d97e89c6af6f78e299f1a` | Yes, by identical PDF/PNG SHA |
| 29 | `920ba74d16570a20947287adab556d836fd08161e69d2bb233ef2ba51278942a` | Yes, by identical PDF/PNG SHA |
| 30 | `f0f8461ca63e7e2938dc995773575d95d3fc93b1e5615e04df1d863a3c870239` | Yes, by identical PDF/PNG SHA |
| 31 | `34383118afe81fc06b6a4b1dff17e04966c657a61ec4f8fb6c9a7543323dd22b` | Yes, by identical PDF/PNG SHA |
| 32 | `c1f3a78efbe0ad042dc308a8fe1e4cee3228c7df22dcd6a0e11dc98c45a0e2ac` | Yes, by identical PDF/PNG SHA |
| 33 | `ee07e23e976be43baa6cdd4e32c9c9fa01b0d1fe8c7c49a7e3547099bc68790a` | Yes, by identical PDF/PNG SHA |
| 34 | `6bf1017b548cc90049bc226f50cd1701fdf861cd9445917c458e13a875472dd0` | Yes, by identical PDF/PNG SHA |
| 35 | `91aabf9b8e79afde1d48e486005de03e1abd36bed8617eb30c04665c052b6930` | Yes, by identical PDF/PNG SHA |
| 36 | `954a725e7712bc1376ccd2e49dd1df2d29dab2e10387b3358f42729ccdbd64d0` | Yes, by identical PDF/PNG SHA |
| 37 | `b0e67480cdbacbb6a083c4470d5c4ea243f2996234377fdf26162a77c672a3d5` | Yes, by identical PDF/PNG SHA |
| 38 | `83b0a5bc6b84eeb11fcc6df77737d5359b41bed293568c448f8a970c8a30e626` | Yes, by identical PDF/PNG SHA |
| 39 | `6791a05f75fb0418dbe5c042442e958e6498295b40f0cea83bec963817f5d538` | Yes, by identical PDF/PNG SHA |
| 40 | `e445952e4f24baf816216f3797d248348993aaca7840b1cd8419785a85b07819` | Yes, by identical PDF/PNG SHA |

## Preservation and scope

Only these two new report files written. No PDF/source/result edits, rebuild, commit, deletion, or child-agent delegation by reviewer. This is visual/layout and content-presence verification, not numerical recomputation or independent scientific validation. Author placeholders remain explicit.

Prior failed JSON SHA `b347ff67de8cf8684ad754dacfc6f4086080e7ca350202adfe818ac8fc11a759` and Markdown SHA `b9ca75ae6d807af346ee24eb4d498a983a102f38ad85745f3fb92fcf10f3843e` verified unchanged. They remain the historical failure record for the old cut.
