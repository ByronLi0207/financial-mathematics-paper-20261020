# Final candidate supplement — actual page-by-page visual review

Review UTC: 2026-10-25T05:35:24.958811+00:00

**Result: PASS WITH MINOR ISSUES.** All34 page PNGs were actually opened. No blocking clipping, overlap, missing content, missing table header or unreadable section was observed. Four minor English-spacing issues appear on pages8,13 and21; they are listed precisely below and were not edited by this reviewer.

PDF: `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/.scratch/v11/publication-candidate/supplement/supplement.pdf`. SHA-256 `bfdf53344e3843bc5d14588d1901b7ae31967d1b133a3e37ea69b46d191fe7bb`; 291,433 bytes; **34 pages**. Every per-page record repeats this PDF identity. The PDF and all34 image hashes were rechecked unchanged at the end.

The parent inspected pages1–17 directly; a same-model delegated agent inspected pages18–34 directly and additionally viewed pages1,16,17. PDF extraction was used only to cross-check locations and saved text, never as a substitute for viewing images. No Claude/cross-model review was invoked.

## Minor issues

| ID | Page | Observed → suggested | Frozen source location |
|---|---|---|
| V001 | 8 | `minimum-validation- loss rule` → `minimum-validation-loss rule` | `source/supplement.tex:677` |
| V002 | 13 | `conditional- moment rejection` → `conditional-moment rejection` | `source/supplement.tex:1070` |
| V003 | 13 | `target- level procedure` → `target-level procedure` | `source/supplement.tex:1076` |
| V004 | 21 | `then equal- weight medians` → `then equal-weight medians` | `source/supplement.tex:1483` |

All four arise from an intentional literal hyphen immediately followed by a source newline, which TeX turns into a following space. They affect spacing only, not digits, signs, methods, criteria or scientific conclusions. The source locations above are relative to the frozen publication-candidate directory, not a request to change that snapshot.

## Critical content and navigation

- **Contents:** all35 section destinations were checked against actual PDF section starts and agree. S35 points to34. No `??` or clipped contents row was observed.
- **S26, pages16–17:** the migrated original paragraph is visible in full, retaining12.2%,416 versus282 breaches and p=.055. The surrounding later-selected/pseudo-out-of-sample, overlap/MISMATCH, no independent third validation period, no pooled tests, lag rule, no epsilon repair, missing NA and no multiplicity/full-selection-adjustment qualifications remain complete. Both reviewers actually viewed these pages.
- **S35 and Table S47, page34:** complete introduction, table caption, three rows and all note lines are visible. The rows show47/48,21/24,42/48, zero missing, requirements80%/60%/100%, and two Supported plus one Not supported. All thresholds/menu/confounding, counterexample/failure, local-design/public-upload, both-horizon/all-window, long-history reversal, left-censoring/non-testability and no-new-dealer/fresh-holdout qualifications remain intact.
- **S33/Table S46:** page32. **Murphy Figures S1–S2:** page33. These are the locations in this34-page candidate and supersede page locations recorded for earlier33-page PDFs.

## Every page — actual image observation

| Page | PNG SHA-256 | Visible object and observation | Status |
|---|---|---|---|
| 1 | `a1bc8b092aad394c8c9eaeb8f9fda758186c1a822c7a392cac8c7a7cfab2c962` | **Title, v11 introduction and complete contents.** All introductory paragraphs, S1–S35 contents rows, dot leaders and page numbers are readable. S35 points to page34. No row is clipped and the printed footer is1. | PASS |
| 2 | `7a9c091f39069159c7f85d1ed62d3b508eedf3ff7206cae16fb956c33cf4b2b5` | **S1 floor projection and S2 classical endpoint bound.** Propositions, proof paragraphs and displayed inequalities fit within the page. Paragraph labels are distinct and no formula intersects text or margins; continuation into page3 is natural. | PASS |
| 3 | `fd64b5799a29814d6f36be85a46d4b0b0d6475a1423f55b72a8f695c2974ced7` | **S3/Table S1 and S4/Table S2.** Both numerical tables, multi-line headers and all final rows are visible. Dense process/seed columns remain distinguishable; S4 adverse-result language and footer3 are not clipped. | PASS |
| 4 | `80214e56be21c9a216147d1456d3e25eb009464d734c6b032c831b4fe793e3e8` | **S4 conclusion; S5/Table S3; S6/Table S4.** Complete secondary-sensitivity table and all original endpoint rows are visible. Fixed-start/conditional distinction and zero-count limitation remain readable; no table or footer overlap. | PASS |
| 5 | `f64615754eb8898e247b3cc3bd483c1cd7435bf1413d7c225773a6aed64361c7` | **Table S5; S7/Table S6; S8 opening.** Scientific-notation p-values and replay rows are readable under intact headers. Algebraic identity and post-result limitation fit; S8 opening is not truncated. | PASS |
| 6 | `05ab1408e9c59cb910deddf6cf4085cbfc3599c33b0c45da4338a6e436c04fc3` | **Table S7; S9/Table S8; S10.** Rational boundary fractions remain inside their final column; closely spaced monetary columns are distinguishable. S9 now says linked complete frontiers; S10 archive directions and footer6 are complete. | PASS |
| 7 | `bc506260165ae11bc9a99b2c478dc374398fb2fbd1741438327047a2115ef33f` | **S11/Table S9; S12/Table S10 opening.** All first-panel rows and the initial second-panel rows fit. Wrapped series IDs have sufficient row height; first-page headers and the S12 heading/prose do not overlap. | PASS |
| 8 | `09d0397dc5b4b682e56a7760e8f3cef8ad5cbde95fc06f315dc353e799f4466f` | **Table S10 continuation; S13/Table S11; S14 opening.** Repeated continuation header and every final panel row are visible. Endpoint comparison header/rows fit. A small extra space after a literal hyphen appears in minimum-validation- loss; otherwise no clipping/overlap. | MINOR_ISSUE |
| 9 | `3827d1b94df02cb13ec7bcd9c91c42709d2be92d70bfa1ce57174af71ebb9598` | **S14/Table S12; S15/Table S13 opening.** Long selection table headers and rows are readable. All NOT_MET wording and failure context remain visible. Table S13 begins with one row here and clearly continues on page10; no row is cut. | PASS |
| 10 | `c57297ff16fe96f13896f3348eb20807bc8d69503ec9c73e28303037896d71df` | **Table S13 continuation; S16/Table S14; S17 opening.** Repeated failure-table header and all remaining FAILED rows are present. Delayed-wrapper table retains both NA cells and its failure reason. The revised adapts to wording is visible; no missing footer. | PASS |
| 11 | `fa2b7b56a76d7a59e4e6ce560da96c6eed2ef4d585c4f96428ab2ae125550167` | **Table S15; S18/Tables S16–S17.** Comparison columns and all combination rows are legible. Score-below-that-of and outperform edits are visible. Table S17 continues with a repeated header on page12; no content is cropped. | PASS |
| 12 | `685daa7cb707fb7ebddf8268e2504af464395d67647e6f13a6a678ecff49c324` | **Table S17 continuation; S19/Table S18; S20/Tables S19–S20.** Missing-median explanation, long method IDs and state-group table are readable. Negative regression-minus-reference wording is clear; diagnostic continuation onto page13 is explicit. | PASS |
| 13 | `b9a8f78cc18f90784d78a86319c8d40cd70d585523dbc944e0417a67046e6558` | **Table S20 continuation; S21/Table S21; S22/Table S22.** Continuation header, all NA upper-target rows, horizon-coherence counts and conditional-hit limitations are complete. Two literal hyphens retain unwanted following spaces: conditional- moment and target- level. No clipping or overlap. | MINOR_ISSUE |
| 14 | `63becb84016118d157b540f0fc70d256586576a0dedf7951327e9fa11c79ae93` | **Table S23 and S23 numerical/inference conventions.** Saved diagnostic values, all bold paragraph headings and both common-pool inequalities are visible. Primal–dual objective-gap wording is clear. Long formulas and final archive sentence fit above the footer. | PASS |
| 15 | `c7672548f2a7ee39306c4c4b0a1cd126d26d870ce55f92690bf937df0d37aa39` | **S24 controlled design and S25 opening.** All design equations, uncertainty formula, MISMATCH outcome, failed candidate details and source path are legible. Mean losses and fraction of at least edits are visible. S25 continues normally onto page16. | PASS |
| 16 | `3bded6e7a33bd249cedc25274b8e3e490de67687fd940fee3d687c7757033443` | **Table S24; S26 migrated paragraphs; Table S25.** Daily results and all matched/rolling backcast rows are legible. The migrated paragraph visibly retains12.2%,416 versus282 and p=.055, alongside pseudo-out-of-sample, later-selected, overlap/MISMATCH and non-independent-validation limits. No table or text overlap. | PASS |
| 17 | `9c3eea105f6089919dd1f3ebd70af0f8795a34273b7c4b34adccce4bbd61526d` | **Table S26; S26 inference limits; S27/Table S27 opening.** All eight backcast rows and the lag formula are complete. No-epsilon, missing-NA, no multiplicity/full-selection-adjustment and no independent-confirmation qualifications remain visible. S27 starts normally; vertical headers fit and clearly continue to page18. | PASS |
| 18 | `b1d0b1418a6746ea6a1e539916ea56e3eac499b72ecbbc991cb53f234dcfe504` | **Table S27 continuation; Table S28; S28 opening.** Continuation headers, failure strings, entire failure inventory and two qualification paragraphs are visible. No right-edge overflow or footer collision. | PASS |
| 19 | `d7d5863ce736bfdb66b1ba5682f1241feec4d932b073abbab7876a47bd0f911d` | **Table S29; S28 explanation; Table S30 opening.** Rotated headers are separate from the data. Diagnostic footnotes and the Continued on next page marker are intact; no clipped table edge. | PASS |
| 20 | `a6f5e013e51f6caef22fae358f6ec5f6f68b0f5df94ea2202f3895d435903f45` | **Table S30 continuation; Tables S31–S32.** FAIL31/32 and NA cells, conditions and table separators remain visible. Rotated headers and final continuation marker fit above footer20. | PASS |
| 21 | `5aa0284869da2f8c0f23c0b80fa84f81532142d032ddf894a81ef129bae331bd` | **Table S32 continuation; loss-summary limits; S29 opening.** Table header, F benchmark rows and note are complete. The explanatory paragraph shows then equal- weight medians with an unwanted space after the literal hyphen. No other visual defect or overlap. | MINOR_ISSUE |
| 22 | `c041e7f8a8fdb6eb2eb43a6eb6105f1054879c0692f4748814a6eb7d1409a9ad` | **S29 continuation; Table S33.** Very dense source/arm/history/method table, but column headers and NA,31/32,FAILED,COMPLETE values are distinguishable at the supplied resolution. No adjacent-column collisions or missing footer. | PASS |
| 23 | `50c46bcb73e0530edf586bfd33f6c52f9052c5a3384ecba34e49519cccb4919f` | **Table S33 continuation and closing note.** Repeated header, last data row, bottom rule and Constant=C/switching=S note are intact. Large remaining whitespace follows the table end; it does not indicate clipped content. | PASS |
| 24 | `de880013adaf590431b14f4ba1c251bc50183e41c1dae2ad636b14afbdb68b06` | **S30 CFTC definitions, eligibility and contract list.** All source/date restrictions,17-code list, release-time wording, units and two format clarifications are visible. Long contract names wrap without colliding with numerical columns. | PASS |
| 25 | `d44072197402315bd5f4392c51f52f0c4de374833cc8af0512e178c7ec214051` | **S31 MCS explanation; Tables S35–S37.** All explanation, rotated labels, bold memberships and M superscripts are readable. Three original-FX blocks are separated and none is clipped. | PASS |
| 26 | `086bb4f7c7da2f8a177315a5b9d1f9a88617be287f7733ca2dd01fd2d9f72f65` | **Early2015 FX; Table S38.** Four rows, NA/dash values, rotated header and superscripts are complete. Display label now has a space in early2015. Large remaining whitespace is a group-page design, not a missing continuation. | PASS |
| 27 | `8abf427efe48c10bd5f89abc30f9cb4447587713d31ddad6a3d67c7e245ca4ea` | **Treasury bills; Tables S39–S41.** All three blocks and their superscripts fit, with clear separation. No collision with the bottom footer. | PASS |
| 28 | `34c16e7b4284304165fc0a9c9511acc48c25111d5dc6e36e37bef7d2b14757c4` | **Other NYFed panels; Table S42.** Dense full-height table remains in bounds. Rightmost median-combination NA values, rotated headers and table rules are legible; no truncated row. | PASS |
| 29 | `6464cef1629af3747cd5f825818ae477e9fe86d681bf5f4c9c84553adeccc059` | **Same-record daily FX; Table S43.** Natural-language heading has the daily FX space. All four rows and bottom rule are complete; whitespace reflects separate grouping. | PASS |
| 30 | `24fe0b8b07439ba382923274811680968b6dcfb8646d046aafa4a34b58188544` | **CFTC; Table S44.** All34 contract/history rows fit; codes are not split, and bold p-values and M08/M09 superscripts are distinguishable. Rightmost four-feature column and footer30 are intact. | PASS |
| 31 | `6ce0ecd1716fdcbc6ac8b2e8b219988f50a427014aec674ac37738be583de572` | **Complete method legend; S32 cost definitions.** M01–M41 mapping and class column are readable even for long labels. Cost formula, units and fixed coefficient menus fit without overlap. | PASS |
| 32 | `a4d69eacba7bf836b8f6d2ba7331efde8ef8cd4cedd23c610a5886d5f663cced` | **S32 ending; S33/Table S46; S34 availability.** Both diagnostic panels and all adjustment/coverage notes are complete. Reproduction, compatible-input, restricted-data, first-release and unmet-validation qualifications remain on-page. | PASS |
| 33 | `bfaa03928400ea8c2d39585555dd5596742d84f6ef797c1f08913694788efcfa` | **Murphy Figures S1–S2.** Both figures retain legends, axis labels, units, curves and full captions. Captions do not collide with axes; the lower figure remains well above footer33. | PASS |
| 34 | `ae48a6e6897c15336df5c3c85b604ea54721dd84f76f5373b650ad21d2436bf2` | **S35 full text and Table S47.** All three criteria and47/48,21/24,42/48;0 missing;80%/60%/100%;two Supported and one Not supported are legible. All three note lines, source/design paragraph and final FX/holdout paragraph are complete, with no cropping or overlap. | PASS |

All PNGs are1061×1500. Page status concerns actual readability, visible English and layout, not independent verification of every numerical cell. Natural source IDs, failure codes, NA values and superscripts were preserved. Long tables carry visible repeated headers/continuation marks; whitespace on separately grouped pages is not treated as missing content.

## Contents destination cross-check

| Section | Contents page | Actual page | Status |
|---|---|---|---|
| S1 | 2 | 2 | PASS |
| S2 | 2 | 2 | PASS |
| S3 | 3 | 3 | PASS |
| S4 | 3 | 3 | PASS |
| S5 | 4 | 4 | PASS |
| S6 | 4 | 4 | PASS |
| S7 | 5 | 5 | PASS |
| S8 | 5 | 5 | PASS |
| S9 | 6 | 6 | PASS |
| S10 | 6 | 6 | PASS |
| S11 | 7 | 7 | PASS |
| S12 | 7 | 7 | PASS |
| S13 | 8 | 8 | PASS |
| S14 | 8 | 8 | PASS |
| S15 | 9 | 9 | PASS |
| S16 | 10 | 10 | PASS |
| S17 | 10 | 10 | PASS |
| S18 | 11 | 11 | PASS |
| S19 | 12 | 12 | PASS |
| S20 | 12 | 12 | PASS |
| S21 | 13 | 13 | PASS |
| S22 | 13 | 13 | PASS |
| S23 | 14 | 14 | PASS |
| S24 | 15 | 15 | PASS |
| S25 | 15 | 15 | PASS |
| S26 | 16 | 16 | PASS |
| S27 | 17 | 17 | PASS |
| S28 | 18 | 18 | PASS |
| S29 | 21 | 21 | PASS |
| S30 | 24 | 24 | PASS |
| S31 | 25 | 25 | PASS |
| S32 | 31 | 31 | PASS |
| S33 | 32 | 32 | PASS |
| S34 | 32 | 32 | PASS |
| S35 | 34 | 34 | PASS |

## Verification boundary and follow-up

Visual/readability and English-spacing audit only. It does not recalculate any cell, score, p-value, statistical conclusion or source archive identity. No scientific result, source, generated table, Git state or original directory was modified. Only the two requested final visual-review notes were written.

If the minor spacing items are corrected and the PDF is regenerated, compare every page hash and actually re-view all changed pages, including contents when pagination changes. Retain this frozen candidate audit as its own evidence.

## Corrected continuous-history snapshot — appended 2026-10-25T05:36:38.813097+00:00

**Latest status: PASS.** This is a new snapshot record. The earlier candidate’s PASS_WITH_MINOR_ISSUES record and its four observed spacing issues remain preserved above; they are resolved in this corrected snapshot.

New PDF: `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/.scratch/v11/continuous-history/supplement/supplement.pdf`. SHA-256 `df302a3d1d6eae343ce12aadc140d850f5d178f0b93c5fdbadde4cc3408b0e95`; 291,176 bytes; **34 pages**. The canonical `submission-v10/supplement.pdf` has the same hash.

All34 new PNG hashes were compared with the previously inspected candidate. Exactly five changed: **8,11,12,13,21**. Each was actually reopened with view_image; the remaining29 are byte-identical to images already actually viewed and retain those visual observations.

| Page | New PNG SHA-256 | Fresh observation |
|---|---|---|
| 8 | `f2e5a3540cccd3328da020afe1772f1a9d23562b1ceaaa930255cae0a9dbf2e1` | Fresh image view: minimum-validation-loss has no extra space. Continuation header, Table S11, S13/S14 paragraphs, wrapped codes and footer8 remain complete; no new clipping/overlap. |
| 11 | `2628335b41557c694b9a7d2fccbf8f43012755384b0c86de1903d2d4e68d934e` | Fresh image view: the relocated median/mean-combination sentence is complete immediately below S18, retaining4.0% and2.8%. All of Table S16 fits; the longer introductory paragraph has no collision or clipping. |
| 12 | `7a77be6a4d9a214f2949ee1ad82aabf5a1f2d6155534285f9d0b24e8b2f7e998` | Fresh image view: Table S17 now has both Mean and Median rows together at the top, with intact header. Tables S18–S19 and beginning of S20 remain readable; continuation is explicit. |
| 13 | `5bd702c6c9ab929e1f5fdd00a7d17f97a110633cf9f1405014765efcec4e1be1` | Fresh image view: Table S20 continuation now contains the remaining three rows under an intact repeated header. Conditional-moment and target-level spacing is corrected. S21/S22 tables and all limitations fit without clipping/overlap. |
| 21 | `c0b7a069702fb21b18995931754c13ecbf31b598a4a2a8b9c1583edae54fbf6f` | Fresh image view: then equal-weight medians is correctly joined. Table S32 continuation, complete note, summary paragraph and S29 opening remain readable with no new clipping/overlap. |

The four earlier issues V001–V004 are now resolved: minimum-validation-loss, conditional-moment, target-level and equal-weight all appear without the extra space after the hyphen. No new clipping, overlap, missing header, missing row or English defect was observed in the changed pages.

**S18 moved-sentence check:** the exact sentence below is present unchanged in the frozen earlier main source and the new supplement source, and it is fully readable on new PDF page11. No source value, result or conclusion was introduced by that move.
```text
The median combination lowers Treasury-bill loss by 4.0%, while the mean combination raises it by 2.8%.
```

Sentence-source SHA-256 (including the original LaTeX percent escapes): `a2f33026c2ffebedb0d9cca13b79b8bf35ca87d70b8e5f40fc58c2ade1b4e125`.

S26 pages16–17 and S35/Table S47 page34 are byte-identical to their previously viewed PNGs. All their migrated paragraphs, table rows and limitations therefore retain the prior successful visual inspection. All35 contents destinations still match actual section starts: S35 remains34, Table S46 remains32 and Murphy Figures S1–S2 remain33.

### All-page hash comparison for the corrected snapshot

| Page | Current PNG SHA-256 | Review basis | Status |
|---|---|---|---|
| 1 | `a1bc8b092aad394c8c9eaeb8f9fda758186c1a822c7a392cac8c7a7cfab2c962` | identical bytes; prior actual view carried forward | PASS |
| 2 | `7a9c091f39069159c7f85d1ed62d3b508eedf3ff7206cae16fb956c33cf4b2b5` | identical bytes; prior actual view carried forward | PASS |
| 3 | `fd64b5799a29814d6f36be85a46d4b0b0d6475a1423f55b72a8f695c2974ced7` | identical bytes; prior actual view carried forward | PASS |
| 4 | `80214e56be21c9a216147d1456d3e25eb009464d734c6b032c831b4fe793e3e8` | identical bytes; prior actual view carried forward | PASS |
| 5 | `f64615754eb8898e247b3cc3bd483c1cd7435bf1413d7c225773a6aed64361c7` | identical bytes; prior actual view carried forward | PASS |
| 6 | `05ab1408e9c59cb910deddf6cf4085cbfc3599c33b0c45da4338a6e436c04fc3` | identical bytes; prior actual view carried forward | PASS |
| 7 | `bc506260165ae11bc9a99b2c478dc374398fb2fbd1741438327047a2115ef33f` | identical bytes; prior actual view carried forward | PASS |
| 8 | `f2e5a3540cccd3328da020afe1772f1a9d23562b1ceaaa930255cae0a9dbf2e1` | fresh actual image view | PASS |
| 9 | `3827d1b94df02cb13ec7bcd9c91c42709d2be92d70bfa1ce57174af71ebb9598` | identical bytes; prior actual view carried forward | PASS |
| 10 | `c57297ff16fe96f13896f3348eb20807bc8d69503ec9c73e28303037896d71df` | identical bytes; prior actual view carried forward | PASS |
| 11 | `2628335b41557c694b9a7d2fccbf8f43012755384b0c86de1903d2d4e68d934e` | fresh actual image view | PASS |
| 12 | `7a77be6a4d9a214f2949ee1ad82aabf5a1f2d6155534285f9d0b24e8b2f7e998` | fresh actual image view | PASS |
| 13 | `5bd702c6c9ab929e1f5fdd00a7d17f97a110633cf9f1405014765efcec4e1be1` | fresh actual image view | PASS |
| 14 | `63becb84016118d157b540f0fc70d256586576a0dedf7951327e9fa11c79ae93` | identical bytes; prior actual view carried forward | PASS |
| 15 | `c7672548f2a7ee39306c4c4b0a1cd126d26d870ce55f92690bf937df0d37aa39` | identical bytes; prior actual view carried forward | PASS |
| 16 | `3bded6e7a33bd249cedc25274b8e3e490de67687fd940fee3d687c7757033443` | identical bytes; prior actual view carried forward | PASS |
| 17 | `9c3eea105f6089919dd1f3ebd70af0f8795a34273b7c4b34adccce4bbd61526d` | identical bytes; prior actual view carried forward | PASS |
| 18 | `b1d0b1418a6746ea6a1e539916ea56e3eac499b72ecbbc991cb53f234dcfe504` | identical bytes; prior actual view carried forward | PASS |
| 19 | `d7d5863ce736bfdb66b1ba5682f1241feec4d932b073abbab7876a47bd0f911d` | identical bytes; prior actual view carried forward | PASS |
| 20 | `a6f5e013e51f6caef22fae358f6ec5f6f68b0f5df94ea2202f3895d435903f45` | identical bytes; prior actual view carried forward | PASS |
| 21 | `c0b7a069702fb21b18995931754c13ecbf31b598a4a2a8b9c1583edae54fbf6f` | fresh actual image view | PASS |
| 22 | `c041e7f8a8fdb6eb2eb43a6eb6105f1054879c0692f4748814a6eb7d1409a9ad` | identical bytes; prior actual view carried forward | PASS |
| 23 | `50c46bcb73e0530edf586bfd33f6c52f9052c5a3384ecba34e49519cccb4919f` | identical bytes; prior actual view carried forward | PASS |
| 24 | `de880013adaf590431b14f4ba1c251bc50183e41c1dae2ad636b14afbdb68b06` | identical bytes; prior actual view carried forward | PASS |
| 25 | `d44072197402315bd5f4392c51f52f0c4de374833cc8af0512e178c7ec214051` | identical bytes; prior actual view carried forward | PASS |
| 26 | `086bb4f7c7da2f8a177315a5b9d1f9a88617be287f7733ca2dd01fd2d9f72f65` | identical bytes; prior actual view carried forward | PASS |
| 27 | `8abf427efe48c10bd5f89abc30f9cb4447587713d31ddad6a3d67c7e245ca4ea` | identical bytes; prior actual view carried forward | PASS |
| 28 | `34c16e7b4284304165fc0a9c9511acc48c25111d5dc6e36e37bef7d2b14757c4` | identical bytes; prior actual view carried forward | PASS |
| 29 | `6464cef1629af3747cd5f825818ae477e9fe86d681bf5f4c9c84553adeccc059` | identical bytes; prior actual view carried forward | PASS |
| 30 | `24fe0b8b07439ba382923274811680968b6dcfb8646d046aafa4a34b58188544` | identical bytes; prior actual view carried forward | PASS |
| 31 | `6ce0ecd1716fdcbc6ac8b2e8b219988f50a427014aec674ac37738be583de572` | identical bytes; prior actual view carried forward | PASS |
| 32 | `a4d69eacba7bf836b8f6d2ba7331efde8ef8cd4cedd23c610a5886d5f663cced` | identical bytes; prior actual view carried forward | PASS |
| 33 | `bfaa03928400ea8c2d39585555dd5596742d84f6ef797c1f08913694788efcfa` | identical bytes; prior actual view carried forward | PASS |
| 34 | `ae48a6e6897c15336df5c3c85b604ea54721dd84f76f5373b650ad21d2436bf2` | identical bytes; prior actual view carried forward | PASS |

All5 changed PNGs were actually reopened. The29 unchanged image byte identities permit carry-forward of their previous actual visual inspections. No source, scientific result, PDF or Git write by this verifier. Old snapshot observations and issues remain preserved.
