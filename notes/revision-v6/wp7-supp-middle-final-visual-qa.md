# WP7 final visual QA — Supplement pages 48–71

**Visual result: PASS on all 24 assigned original v2 page images. No actionable overlap, clipping, truncated-digit, NA-retention or footer defect was found.**

Every actual PNG from `.scratch/revision-v6/pdf-qa-v2/supp-48.png` through `supp-71.png` was individually viewed using `view_image(detail="original")`. No contact sheet, text-only substitution or unviewed-page extrapolation was used. Only this new note was written; no rendering, financial execution, installation, deletion, source edit or Claude review occurred.

## Source identity and scope

The root supplied a 94-page `submission-jof/supplement-preview.pdf`. Its SHA-256 was independently recomputed at the start of this visual pass and matched the requested source:

`3a20a0dc17652cf0a7243822608134d91c13b40bb5ca7cd1304fbcfbed347888`

A final identity check found that the PDF had been replaced after the v2 PNGs were rendered. The replacement hash at note creation is:

`4887efcb02124612df5b5782f1dbdfb214102e3df108739fdcccc1f17ab9e495`

The root was notified immediately. The replacement is now bound to this visual pass by `notes/revision-v6/wp7-final-raster-identity.json` (SHA-256 `7962c225bf381428e93e45b2b446c8666fb69f919a63bff184bc8f6b26ec836f`). That full-render receipt records only page 23 as changed after a caption-spacing correction. I independently rehashed both v2 and v3 PNG files for **every page 48–71** and checked each against the receipt: all 24 pairs are byte-for-byte identical. The currently hashed replacement PDF therefore has exactly the same assigned-page images that were actually viewed, and the PASS conclusion also applies to its pages 48–71. No changed page was certified without inspection; page 23 is outside this assignment. The per-page hashes below identify the exact viewed images and their identical v3 counterparts.

## Per-page evidence

Each page has readable continuation headers where applicable and the matching bottom-right physical page number. Typography is compact but legible at supplied original resolution. Procedure names and long reasons sometimes wrap; all their text remains present. Normal white space follows table endings on pages 54 and 58.

| Physical page | Exact original PNG SHA-256 | Evidence |
|---|---|---|
| 48 | `82a0cd8759f6ac7663d85cc2a6bc5e82e8d17e63e01e39f4df1f3a15606e01c5` | PASS — S50 continuation: DM/HLN/Holm columns align. Initial-calibration NA reasons and book=1 remain visible; final row stays above footer 48. |
| 49 | `30f1dc4b0b07296427600d282acb12a86e5154d0f3b08eb9e5fd9bd85deee550` | PASS — S50 final contrasts and pair NA finish cleanly. Combination definition and S51 count table start below a separate rule; wrapped decimals and footer 49 are intact. |
| 50 | `8fd946fd4526c07cd1778d08be367b9176a1860e5c59f5e2f46509b847ac7c93` | PASS — S52 starts original combinations, EXACTLY_F identities and added-panel methods. Missing-KNN NA reasons and all displayed numeric columns are complete; footer 50 is clear. |
| 51 | `1d892eac991d659b82d86274e2ac39fb3123e3de978c9928a9a88fa1debe603a` | PASS — S52 Corporate/Agency/GSE/TIPS continuation. Alternating complete means and NA medians retain complete no-substitute explanations; no overlap; footer 51 is clear. |
| 52 | `411647679ca25b416a66dbc1c9d667a8cf81e857f9c41fd3112ae8a3809d2bf9` | PASS — S52 TIPS/coupon continuation. H/W, source units, loss and rates remain readable. Unavailable medians retain all NA cells and reasons; footer 52 is clear. |
| 53 | `4626ec611bd13530679197b548542f9edbdfe4a6b4169581796d9ee406304433` | PASS — S52 coupon continuation. Multi-line contexts/reasons remain within their columns and row heights; footer 53 is unobstructed. |
| 54 | `ae6a5f2935fce8216a47043b8ed8e97d9606ff54a993fe4a7c249be95ac9f6a6` | PASS — S52 final coupon rows. Final missing-KNN explanation precedes a clean closing rule. Normal white space follows the table; footer 54 is clear. |
| 55 | `b538547eb57dcc5d00e1853f68a6a7578c1941cc7eddedeaec9a36958e4d5d09` | PASS — S53 matched F/QR controls begin. Native units, method names and seven-significant-digit values remain complete and aligned; footer 55 is clear. |
| 56 | `6b48e65fdcf68edb4d39391ffdf72c3d0342b119a10ddc7bf8a2e20fe55a29e9` | PASS — S53 Corporate/Agency/GSE/TIPS control continuation. Dense rows retain separate contexts, methods, losses, counts and rates; footer 56 is clear. |
| 57 | `aa4c2a0c6c4a8ba6be49528a909d68e55bb59594ff35ad2c241c18cce00bef40` | PASS — S53 TIPS/coupon controls continue with repeated headers and complete bottom row; no row/header/footer collision; footer 57 is clear. |
| 58 | `635f4c8864c487b8fe38407b9aeec5493a346ecdaa0eaa7b359252b12163f2a4` | PASS — S53 final coupon controls end above a clean rule. Multi-line unit labels and Complete statuses fit inside the frame; footer 58 is clear. |
| 59 | `d264185d309d3f9980f5a3a8bdb43e74080cb6afac4e182a4fe9978bd370feb7` | PASS — S54 percentage-change table begins. Minus signs, exact-zero F changes and EXACTLY_F statuses are visible; panel medians retain NA rather than zeros; footer 59 is clear. |
| 60 | `b026b81a72631b18e2c32df5bc0152ff08fc44ad0e11486127b401c919cea80d` | PASS — S54 Corporate/Agency/TIPS continuation. Decimal signs and full percentage values fit; no-substitute reasons wrap inside their status cells; footer 60 is clear. |
| 61 | `3dc4babc855474ffa945183d2fa869c9b92d1a7790c423bd0f03b10a7f595271` | PASS — S54 TIPS/coupon continuation. NA appears in loss and both percentage columns for unavailable medians, with complete explanations; footer 61 is clear. |
| 62 | `ff7358c58e0325499b0e7051c5d8bc9ad28be9b237de465e360a57a46f90331a` | PASS — S54 final coupon rows. Large positive and negative changes retain complete digits; final NA rows and closing rule are clear; footer 62 is clear. |
| 63 | `73ee735f89acb9413a360d07201361695b1e3f66191161d00eefaf53d58de5e0` | PASS — S55 coverage begins. Spaced grid n / hits / rate wraps are readable; scientific p values, boundary CC and missing-KNN NA remain separate; footer 63 is clear. |
| 64 | `ee229c567a70c3dd6e3b125b7a3130b1c5bd13c0b586d162ab3860c4dbe232fa` | PASS — S55 MBS/Corporate/Agency/GSE/TIPS continuation. Valid UC and absent-transition-row CC NA are distinguishable; boundary/NA counts remain visible; footer 64 is clear. |
| 65 | `2921b65d6bc0b1cca0503ddc9d39f36d98d5eef50910a82ef14f84a959fe043e` | PASS — S55 TIPS continuation. Repeated header, scientific exponents, grid triplets and full missing-median reasons remain readable; footer 65 is clear. |
| 66 | `c78d92b36132ed823b91b37865916a71d23fb055b447bc58120cccbf5e4fd62c` | PASS — S55 zero-hit TIPS cases and coupons. UC boundary references and absent-transition-row CC NA remain explicit, with complete counts/reasons; footer 66 is clear. |
| 67 | `0c80f26ae9b1e196cead3c3776aa238b4d386d4c24496849c98af7c54754174b` | PASS — S55 coupon continuation. Long contexts, grid counts and NA causes stay inside their cells, with no clipping at the page edge or footer 67. |
| 68 | `bcee8425393717b63ad3e092b7c705a7c9bc4258ee61953f3ce88b4ce302b414` | PASS — S55 finishes combination rows and begins matched controls. FX long p-value exponents and rate wraps keep all digits; Treasury boundary CC is readable; footer 68 is clear. |
| 69 | `3f5e7a8cc2e983474b0516c29aba5204475038d1faac8115916c1b2583f9a11d` | PASS — S55 MBS/Corporate/Agency/GSE controls. UC and CC statuses remain distinct; absent rows and boundary/NA counts such as 1/1 and 2/1 remain visible; footer 69 is clear. |
| 70 | `1a39826ea1564f1e8d0930a6efd2d7884eb24d66dd614b87f97427e576b7dc65` | PASS — S55 TIPS controls. Long scientific exponents and spaced grid triplets are complete; zero-hit UC boundary cases remain distinct from CC NA; footer 70 is clear. |
| 71 | `db79371df08990872bc5eb5af3d37f18c87f788adae9d96d44ffa34825a741b6` | PASS — S55 TIPS/coupon controls. Valid, boundary and absent-row statuses retain complete p values/counts within the frame; footer 71 is clear. |

## Requested checks

- **NA retention:** calibration failures, unavailable plain-KNN medians, absent transition rows and boundary-reference statuses remain visible where present in these pages. No unavailable test is visually presented as a computed zero.
- **Numeric wrapping:** grid n / hits / rate separators, bookkeeping values, scientific exponents, percentage signs and minus signs remain readable without truncated digits or cross-column collision.
- **Layout:** no overlapping row/header/rule, clipped right edge, missing continuation header or bottom-row/footer conflict was observed.
- **Limits:** this is visual preservation and readability review, not recalculation of financial values. Pages 1–47 and 72–94, article-TeX compilation and any subsequent PDF change beyond the verified v3 identity remain outside this assigned visual pass.
