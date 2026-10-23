# Supplement visual review

Review completed (UTC): 2026-10-23T17:24:23.994358+00:00

## Result

**PASS for the supplied final rendered pages.** Initial caption/number-wrap defects and the later orphan S14 heading were visually rechecked after repair. No remaining clipped content, page-edge overflow, table-row truncation, overlapping objects, black replacement boxes or visibly missing mathematical glyphs were observed in the reviewed images.

## PDF identity

- PDF: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement-preview.pdf`
- SHA-256 at final review and immediately before writing: `18b2b6d947500e3c241e835ab59c559d97db4d858eae3c0233b458fc7b1bca8e`
- Bytes: 463007
- Raw `/Type /Page` object count: 30; page inventory: 30 PNGs.
- Supplied final page bitmaps: 703 x 994 pixels.

## Actual visual inspection and version boundary

- Initial review: all eight `.scratch/v4-jof/render/supp-contact-1.jpg` through `supp-contact-8.jpg`, plus every original `supp-01.png` through `supp-30.png`, were directly opened using `view_image`.
- Initial reviewed PDF: `efa4d1e648e153c7ba2430b538b6c1a384c36109dcf6b24bef32cd294fdc6c9e`.
- After caption/range repairs: all eight `.scratch/v4-jof/render-final/supp-contact-1.jpg` through `supp-contact-8.jpg` were directly opened, covering all 30 pages. Original PNGs 16, 18, 19, 20, 21, 27, 28, 29 and 30 were directly opened for detailed checking. This stage bound to PDF `c0906a5b978306d12d45f9960349bac0b592711b0478d373a8ed0e1721aff30e`.
- The last isolated repair inserted an explicit page break before S14. The coordinator reported only this layout repair and refreshed PNGs 27-30. All four refreshed original PNGs were directly reopened; the final PDF hash is recorded above.
- **Final contacts 7 and 8 were not regenerated after the last repair. Their page-27-30 panels are stale and are not evidence for final page-27-30 appearance.** Final page-27-30 acceptance uses the refreshed individual PNGs. The page-25-26 panels of contact 7 remain part of the preceding review.
- Pages 1-26 use the preceding full render. Their unchanged-prefix relationship to the final PDF relies on the coordinator's stated isolated page-break edit. This reviewer did not run a renderer or independently perform a fresh full-PDF pixel comparison.

## Issues and closure

| Initial issue | Final check | Result |
|---|---|---|
| S25 caption orphaned on old p14 | Final p16 original PNG | Caption, header and first rows together. |
| S26 range tail digits isolated on old p17-18 | Final p19 original PNG | All four ranges readable on one line. |
| S29 caption split over old p18-19 | Final p20 original PNG | Complete caption and table on same page. |
| S30 caption split over old p19-20 | Final p21 original PNG | Complete caption and table on same page. |
| S14 heading orphaned on repaired p27 | Refreshed final p27-28 original PNGs | Heading starts p28 with Figure S1. |

## Page-by-page record

| Page | Result and observation |
|---:|---|
| 1 | PASS - Title, notation S1 and validation S2 intact; no clipping. |
| 2 | PASS - Full FX S3 table stays under its caption; dense but within margins. |
| 3 | PASS - Treasury S4 table and robustness prose intact. |
| 4 | PASS - Tables S5-S8 and continuation prose readable; no lost rows. |
| 5 | PASS - Tables S9-S10, limitations and S2 opening intact. |
| 6 | PASS - Finite-geometry mathematics stays within text width; no missing-glyph boxes observed. |
| 7 | PASS - Artificial tables S11-S12 and AR replay formulas intact. |
| 8 | PASS - Original tables S13-S14 and beginning of numerical conventions intact. |
| 9 | PASS - Objective/gap and shifted-penalty mathematics intact; S5 opens with body text. |
| 10 | PASS - Horizon-coherence S15 table and e-value formulas/prose intact. |
| 11 | PASS - E-value S16 table and ordinary-rank explanation intact. |
| 12 | PASS - Rank S17 table and preference formulas intact. |
| 13 | PASS - Preference tables S18-S19 and complete menus S20-S21 fit within margins. |
| 14 | PASS - Tables S22-S23 and AR definition/bound prose intact. |
| 15 | PASS - Reproduction/inference prose and S24 intact; no orphan S25 caption. |
| 16 | PASS - S25 caption, header and first rows share page; no clipped cells. |
| 17 | PASS - S25 continuation repeats headers; wrapped status codes remain inside their cells. |
| 18 | PASS - S25 continuation ends normally; S10 heading has its paragraph. Dense numeric columns remain distinguishable. |
| 19 | PASS - All four S26 norm ranges now stay on one line; S27 and classical-bound proof intact. |
| 20 | PASS - S28 and complete S29 caption/table share page; no split caption; formulas intact. |
| 21 | PASS - Complete S30 caption and table share page; prose below is not clipped. |
| 22 | PASS - Complete S31 and analytic-boundary formulas intact; S12 has opening body text. |
| 23 | PASS - Dense S32 panel table within margins; continuation repeats header. |
| 24 | PASS - S32 continuation and prospective/FHS method prose intact. |
| 25 | PASS - POT/QRF method mathematics and complete S33 within margins. |
| 26 | PASS - S34 caption with table start; rows continue without clipping. |
| 27 | PASS - After final repair: S34 continuation and S35 intact; orphan S14 heading removed from page end. |
| 28 | PASS - After final repair: S14 heading begins page with Figure S1; S2 and both captions fit. |
| 29 | PASS - Figure S3 annual display and S4 Murphy diagram, labels and captions intact. |
| 30 | PASS - Figure S5, nine reference entries and figure captions fit; final text remains inside page. |

## Final image fingerprints

All listed PNGs were represented in the full contact review. `direct original` marks those also opened individually after the caption/range repair; for pages 27-30 it means the last refreshed files.

| Page PNG | SHA-256 | Dimensions | Inspection |
|---|---|---|---|
| `.scratch/v4-jof/render-final/supp-01.png` | `af5e8dfd91fda198dea4d8171c50e1317cb3b038d4a007890ee847c9e7f00e04` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-02.png` | `04a1848a18212813b149763c643f8c77eeb157525609b8bfbeeecacdfe97a8b3` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-03.png` | `d318f2905b24e19d1eb0f0e75bafc21e2ba59cb9640c6d2c0edacc1fefba764a` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-04.png` | `c9858e9b395ad16e4463ef67a08898a0948314861c334993d36bc9c84c80ccbf` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-05.png` | `e0d0e999647127c59159ec504e6a251da7b866c4805106748e17ff1847604a5c` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-06.png` | `65991445441084420be16a00c27663087d47533271eb5638535e02fa347b603f` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-07.png` | `2fb0e9cde2f07ccee171fb9b89b07a525ede2e80582c3de51d2ccec703041633` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-08.png` | `bdc5938e7f8faea220bf4d558265fd7010c9991bb9366aaaf1a2f96eed730850` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-09.png` | `f5ed8867044f6d8646ff8f7d8bf6b22f86763c5ea1bc8b849a95ee44f213d1d2` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-10.png` | `5e7d3735ca68c04f8249b584ae90400c75a1bedb34bd289fe764f68c601c9da9` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-11.png` | `7da6cdac392249759e78f9f513527bdf6ef6430fa8ccd205cd11dd4fc00dd622` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-12.png` | `9aa81f49a6379b8bbc487724d867907eb4d73f1097a2b9fef4c03c1eb4151035` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-13.png` | `4b3d95300714074d79f549324652af87d5bda533063645f40435c76963f97aff` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-14.png` | `25550a00d650f03296069439151d9d81dcaa64fbf0712a695747c833d94efa29` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-15.png` | `ffe0658921682026c145a08980bf1a7077414a78c6615ccf0b07a3e18d5f730d` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-16.png` | `5acb3eb2176b7a849f4a8a232f7343c2e613f4a0c1995fa82af65417059da8d1` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-17.png` | `dde4329b93d073dc800cc6d47d275a351281ae26318fa50421b934a253ba6de0` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-18.png` | `f9b741b345bcb7a44513e2da0b22ea5e6c9524676dd4132137d11a0cc8c705d2` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-19.png` | `2ec5cf687c8936c35e986c254c092ff4dc977276953e0b3e70d8380338c15ded` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-20.png` | `fe29ed661b901d340e2b0a90bdf2670d108da78de0a34b9b56c192457481b665` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-21.png` | `802ab96ecff16d41c9b5c977116792b0753cf0e85e0da5923a033e3e1d93d187` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-22.png` | `378b3e29d4c3bf71ff606678f0c7cc89fc26c1f027c102908301109780f17b2b` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-23.png` | `a61cc95414346ab06bb1b074cb14e958e9b0da9d2c9178a19a42321811a09801` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-24.png` | `eb6afcf18f14aa668557bed0a656b26e3893ccd84414b33c4ca686d8c6c3f478` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-25.png` | `fe43a792fb09e5ac7213ba42da11796acb74f328f58bb62c882bbcb2bda4e5dd` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-26.png` | `f86945ca41a7c13e24514899c6d9ff450e6fb46e2e3bf41ddbd4b97576d7e0ce` | 703 x 994 | contact |
| `.scratch/v4-jof/render-final/supp-27.png` | `649ddbc1c819e5e48fa21a74f23ab4efe851b0a13c7832a336d00ae17fffef88` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-28.png` | `ac68de21d94d498370c4a0e2fffd38131a913b7db4543e28f71392a85e9984b7` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-29.png` | `739e733e54b72b12904f234936fb42323c0039fbcd43589ba6bfc5db45f472a0` | 703 x 994 | contact + direct original |
| `.scratch/v4-jof/render-final/supp-30.png` | `420b6a2562a094ed1c20b38716c87e43d25af53a11dc72e8d70fbd07e064f509` | 703 x 994 | contact + direct original |

Contacts actually opened, with current fingerprints. Contacts 7-8 have the stale-panel limitation above.

| Contact file | SHA-256 |
|---|---|
| `.scratch/v4-jof/render-final/supp-contact-1.jpg` | `85476929982a4fc8695d641f02e7ef38c5e3a24a0240520d4eaeae67546ebf7e` |
| `.scratch/v4-jof/render-final/supp-contact-2.jpg` | `6843496787782884e5d0118a7bab58e65f13d6f939a2909838352690d0086996` |
| `.scratch/v4-jof/render-final/supp-contact-3.jpg` | `6174e0c3a9a789ab470550e79883a1f211f32cd8956a75da51184c8d04db48ba` |
| `.scratch/v4-jof/render-final/supp-contact-4.jpg` | `22988431bd9bd740116284f5a6c8b2d105c183dcea8fbabcd90fb9fc5d9a12e6` |
| `.scratch/v4-jof/render-final/supp-contact-5.jpg` | `d4d6986cdb38d0de30ed803cab8caa10a6798cf184b3e44b53f381a242744e86` |
| `.scratch/v4-jof/render-final/supp-contact-6.jpg` | `606a066b709ec9a42a60a4b818f41e0e92925386995f88d62d81ccdd4b197d17` |
| `.scratch/v4-jof/render-final/supp-contact-7.jpg` | `bf4107527fa2e8c1c24c24333ededdb6126a3dccdfb5fe1717bb1b5b4a885f72` |
| `.scratch/v4-jof/render-final/supp-contact-8.jpg` | `d4f06d4a7db5a80c262b536cc5045bb29383aca0e725385d89257d4d3b0119ab` |

## Limits

- This was actual image inspection, not a text-extraction substitute. No PDF rendering, PDF/source editing, model execution or tests were performed by this reviewer.
- The reviewed document is the supplied ReportLab preview. Its footer identifies a separate preview and supplied standard-article TeX. This review does not establish that formal TeX has compiled or that another PDF has the same layout.
- Page bitmaps are 703 x 994 pixels. Acceptance is bounded by that resolution; no higher-resolution print proof, accessibility audit or independent glyph-by-glyph comparison was performed.
- Continuation across pages is accepted where headers repeat and rows stay intact. Sparse whitespace and status-code wrapping inside a cell are not treated as missing content.
- This visual review does not revalidate all numerical results, citations or scientific claims; those are separate audits.
- A later layout/content change or PDF with a different hash requires renewed review of affected pages or a verified pixel-equivalence bridge before reusing this result.
