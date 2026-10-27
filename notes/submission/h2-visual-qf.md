# H2 QF direct-page visual review

Reviewed: 2026-10-27T03:45:27.672481+00:00

**60/60 individual page PNGs directly viewed: main 20/20, supplement 40/40. Review complete; the reviewed old main cut FAILS because its final equation on page 3 collides with page number 3.**

Only two report files written. Reviewer changed no PDF/source/science/results, performed no rebuild/commit and delegated no agents.

At review start both live PDFs matched H2. At report write root had replaced main.pdf. All sixty reviewed PNGs still match old H2 manifest; old main PDF retained in scratch and hash checked. This report does NOT approve replacement PDF. Supplement unchanged.

## Hash-bound reviewed cut

| PDF | Pages | Reviewed PDF SHA-256 |
|---|---:|---|
| `submission-package/QF/main.pdf` | 20 | `4e0526c04d5d22c0987e28da0c20b80621002ef632c2fe9a2f764be364dabbfc` |
| `submission-package/QF/supplement.pdf` | 40 | `f6ac52d32d69c75ddfdf48cec6c7af53a3893473ea4ae1a346a8a5ced8f7868c` |

All sixty image SHA values match the H2 manifest. The reviewed main remains available at `.scratch/submission/qf/20261027T032648026540Z/main/main.pdf`. Current root replacement main hash at report write: `f6d9ad0ba27fbadeb807c89ac8c1dd79eaf9b2d0107c7f5be5cca77f35a63d50`; it is outside this approval.

## Findings

### QF-M-01 - P1

`submission-package/QF/main.pdf`, pages 3. Bottom centered pinball/indicator display; original PNG approximately x560-574/y1426-1446.

Equation punctuation/symbol area physically collides with page number 3.

Repair author-side geometry/footer clearance, rebuild and directly inspect regenerated pages.

### QF-M-02 - P2

`submission-package/QF/main.pdf`, pages 2, 4, 5, 7, 9, 10, 12, 13, 18, 19. Last full-width body/reference line and centered footer. Body baseline approx 35.4pt, footer baseline approx 28.1pt, gap approx 7.3pt.

Insufficient vertical safety gap for 10.96pt text. Several lines approach/share footer glyph area. Pages 1/17 also have low baselines but short lines avoid physical intersection.

Repair with QF-M-01 and recheck all new pages.

### QF-S-01 - P2_OBSERVATION

`submission-package/QF/supplement.pdf`, pages 23, 24, 26, 27, 28, 29, 30, 31, 32. S34 and MCS/legend, especially S43 p29.

MCS source specifies 7.1pt/8.5pt, math superscripts request 3.55pt with logged substitutions. Dense rows remain distinguishable but need zoom. No clipping or physical collision observed.

Transparent readability note. Any enlargement/splitting must retain complete methods/NA/failures/denominators. No journal minimum-font rule independently verified here.

### QF-S-02 - P3_OBSERVATION

`submission-package/QF/supplement.pdf`, pages 25, 32. Seventeen-contract universe p25; M01-M41 legend p32.

Uncaptioned longtables consume S35/S46. Fifty-one visible captioned tables span counter range S1-S53; plus two uncaptioned table objects gives fifty-three. Data still present.

Distinguish caption count from object count; preserve all existing science and reference relationships.

### QF-M-03 - P3

`submission-package/QF/main.pdf`, pages 20. Wisniewski et al. (2020) reference, lower half.

Visible duplicate Proceedings of the Proceedings.

Packaging-only bibliography mapping may remove duplicate wrapper without changing facts.

### QF-M-04 - P3

`submission-package/QF/main.pdf`, pages 18, 19. Data availability.. and Code availability.. labels.

Both labels have doubled full stops.

Packaging punctuation only; preserve full rights statements.

## Template and compatibility transparency

Official [QF template ZIP](https://files.taylorandfrancis.com/rqufLatex.zip), local SHA `c3da9ab0b3f20e7d8fcb0be9d9e91aee234930262bf06e814253ea5fb24d4ee4`. The downloaded archive and receipt were inspected locally; raw bytes of packaged class/bst equal the official ZIP members.

- `rQUF2e.cls`: `5ceee7d7f54fcf10f5f992bb21c9018b562ca85e13d375a2ee7cd1ea1bd57f9c`
- `rQUF.bst`: `924f0b2386491926dd630f2b8cbae18926190f1c34eb8c06ea2262210d559fcd`
- Reviewed compatibility macro: `542fce083d321cd474528dd44a0a3149253f29bd48a5b41a27b5ea1ac5a5fa98`
- Reviewed font setup: `797b195a65b2fee9c481cc411b917505ff24c08b9253993dffd6bb9bb289f4a4`

Unused extended enumerate interface marked provided; standard lists retained. Availability assertions are from then-current README/receipt; macro directly read.

Cached Latin Modern OpenType regular/italic/bold/mono; small caps substitute regular; bold italic synthetically emboldens italic. Conventional Computer Modern math with logged fallbacks. No font download/install by reviewer.

TU/cmr, OML/cmr, OMS/cmr, OMX/cmr undefined shapes; 5.5/7.5/3.75pt size substitutions/defaults substituted. No missing-glyph square seen.

3.55pt OT1/cmr, OML/cmm, OMS/cmsy and bold size substitutions; underfull boxes.

Official class/bst unchanged bytes do not certify modern-output compatibility; actual footer collision remains blocker for reviewed old cut.

## Counts, continuations and preserved science

Main: 8 captioned tables (1-8), 6 figures (1-6). Supplement: 51 captioned tables across S1-S53, plus two uncaptioned longtables consuming S35/S46, total 53 table objects; 4 figures (S1-S4). No literal `??` found by auxiliary text inspection. This does not certify all hyperlink destinations.

Continuation headers checked: S10 p7-8, S15 p10-11, S24 p15-16, S29 p18-19, S32 p20-21, S34 p23-24. Repeated headers present, no clipped row observed.

FAIL/FAILED/NA/NOT_MET/MISMATCH/unavailable methods/rejected repair/full counterexamples retained.

Main p10 and supplement p39 partial support retained; S52 Not supported/Not testable; p40 full counterexamples. WP2 PARTLY is not upgraded.

No numerical experiment/scientific certification/external review/submission claim.

## Individual page register

Every row is an actual individual page view; no contact sheet or extraction was substituted. Full image paths and findings are in JSON.

### submission-package/QF/main.pdf

| Page | Image SHA-256 | Direct view | Observation |
|---:|---|---|---|
| 1 | `4c64836adda07874494a0205ec6865e1ec778738472f4c1939b80a8f02af9cd2` | Yes | Title, abstract, six keywords and explicit author/affiliation/JEL placeholders clear; header intact. Short final RQ2 line near footer, no physical collision. |
| 2 | `fe17ce2b554eabb5aa17343bc078ff2e780ab7619ad201435bfc6fcac0faf301` | Yes | Figure 1 axes/legend/units/caption clear; final related-literature line too close to page number 2. |
| 3 | `7424cc663657567bbdec8a56b3848d8160d825138fa2900ff27cf607b7d38007` | Yes | Table 1 four rows complete; peak definitions clear. Final pinball/indicator equation physically collides with centered page number 3. |
| 4 | `8479e47d88371f6f4df4d2473ba7473f1139a1190ccbb471620668b18813c9ae` | Yes | Both propositions and wide displays fit; Data final line too close to page number 4. |
| 5 | `852d442c21e4420d665dde14f4faff40c37f9631d8f5b392801f815db19906dd` | Yes | Table 2 both panels, units/counts/notes intact; quantile display clear. Final Standardization line too close to page number 5. |
| 6 | `a781c3fb415ae7fcceba2699765a2ec6431fab5066100a73b8b32d57ff2e1c50` | Yes | Penalized objective and six penalties clear; calibration/combination/failure boundaries retained. Large lower whitespace; footer separated. |
| 7 | `d2bdb24cac87060bc5aae1d42cfea4a28a93fae65a427c55cc8eb5cdd6375ecd` | Yes | Table 3 all methods/menus/notes intact. Evaluation display clear. Final Newey-West line too close to page number 7. |
| 8 | `a2a5453d572d6abafa0da9578b9acb933a4c14bb265d47dbf45f238da4a143a2` | Yes | Sections 6.1/6.2/7/7.1 hierarchy clear; MCS and incomplete-method boundaries readable. Footer separated. |
| 9 | `9055d47eb542aaaf1014528c9edddb4180e31909996e46da8226630c6023f57a` | Yes | Table 4 five rows intact. Figure 2 six history points, axes and caption intact. Last WP2-extension line too close to page number 9. |
| 10 | `fa6a43f7e9433b2ea4f499338e40661a7bb846eb08889b1643aa5924570b0459` | Yes | Partial support retained. Table 5 eight rows/NOT_MET note clear. Final Corrected historical headroom line too close to page number 10. |
| 11 | `e27e69d680fb946b27d496f1b683117cf129c705ddfcf835e8fab0c4e598c620` | Yes | Table 6 all seventeen contract codes at both histories clear; signs/failure notes retained. Section 7.3.2/footer separated. |
| 12 | `34303eeed0a36569f91e7bd1b4cb4115b3cd2624980c004121d976e2979565cf` | Yes | Figure 3 both histories/all seventeen codes intact. Selection/information gap text intact. Last line too close to page number 12. |
| 13 | `64c6be194b3c68b80e64c4ef0bf80508cf8b9ebd399c4ad59ba2ee15cc6f42cb` | Yes | Figure 4 both panels/Unavailable crosses/full planned index retained; Table 7 four rows clear. Rejected repair/NA retained. Last line too close to page number 13. |
| 14 | `da12d1d25001e74ce9566bda3c9385192ec8e75d6d0fdbf24402a0c73eec2c44` | Yes | Table 8 both quantile columns/three NA entries/rejected-repair note intact. Large lower whitespace; no clipping/collision. |
| 15 | `8d2bd1641574f1ea5c8e09f5835f4c4eb9d6bbff7045fbc872fe45597671b6ae` | Yes | Cost equation/mean/beta definition and three CFTC grid counts clear. Large lower whitespace; no collision. |
| 16 | `a25d279419746cffb9c6eb02ab09986080e494082b88d67895719f6e559346ac` | Yes | Figure 5 six panels/common color bar/completion denominators readable; caption and footer separated. |
| 17 | `d1663e06083f451636a566f2447e17d00f70e51f6aaa9ce57999fc69b4479e59` | Yes | Figure 6 three separately scaled groups/planned counts intact. Practical-reporting text clear. Short final limitation line close to footer but no physical intersection. |
| 18 | `44c4f097b77bf87e3e9cc015e4e03203cd937ff0ea393226b7cd362c8ffca41a` | Yes | Limitations/conclusion/rights text intact. Data availability label has doubled full stops. Final license/source-conditions line too close to page number 18. |
| 19 | `93a7dc6054503427c2dae1ae3af93e71667cd81f4d03a24105f171513d68bb4f` | Yes | Code availability label has doubled full stops. Author/ORCID/funding/interests placeholders retained. Reference URLs wrap within margins. Last NYFed URL too close to page number 19. |
| 20 | `f45702fee59994ff1aad33cb20cda6af06f7dce86eb2c86a1bd420ab673ff870` | Yes | Reference continuation/long URLs intact. Wisniewski et al. (2020) visibly repeats Proceedings of the Proceedings. Footer separated. |

### submission-package/QF/supplement.pdf

| Page | Image SHA-256 | Direct view | Observation |
|---:|---|---|---|
| 1 | `6322ad955bf4a3f62824bb29179545fa60b972116d0fbbcc83d91fd5aa492645` | Yes | Title/preservation statement/contents S1-S37 intact; NA and failure preservation visible; footer clear. |
| 2 | `65e07737858ddff72864a35986efdbab9640db1d3d6e6d73cc628927d9b9f8b5` | Yes | Contents S38-S39 then S1-S2; propositions/proofs/wide equations/QED/conditional limits intact. |
| 3 | `f583a22847f62a68740daa2ff99c7bddb11732a56577eff3e8e38bb455110061` | Yes | S3-S4: Table S1 eight rows, Table S2 sixteen rows; probability/MCSE and negative-increment sensitivity intact. |
| 4 | `28dfd7300416b2e1f5ade3383d60cc7c2f4b53acad50201cfca004fb4bcf1936` | Yes | S5-S6: Table S3 eighteen rows, Table S4 eight rows; zero-count/Monte Carlo limits intact. |
| 5 | `df77ff003e39456ddbaf9ff5df57ce5b620a6f475a9dda3c6fdfa306772e8a58` | Yes | Table S5 sixteen rows; AR identity and Table S6 eight rows intact; adverse breaches retained. |
| 6 | `740044098d57478233f7d2b191891e488ec5c2c168290bd4ca5ff4c765582d35` | Yes | Table S7 eight rows and S8 four rows intact. Exact rational fractions have dense long integers; no neighbor collision. |
| 7 | `53310eed9bc8074007c97a915f93b4f497d57c034ff70fd3ae1111235b2ae22b` | Yes | Table S9 twenty-four rows intact. S10 starts eleven rows through G2L3/24/52; clear header. |
| 8 | `f8055d207426584e33faa00b3cc85073def6f53da9b2c1dc02e660e0b50c5a08` | Yes | S10 Continued/repeated header joins thirteen rows; Table S11 twelve rows and S14 explanation intact. |
| 9 | `7f95d3f0d2878dcc55e48a230e4ecb1c8710d3e5636d70552a686524172b87b8` | Yes | Table S12 thirty rows/three NOT_MET criteria; S13 four FAILED rows and saved reason intact. |
| 10 | `62da5f2b884753bdb831590905832cdb8b41361768dcb214d63f40e1d8d7022b` | Yes | Table S14 twenty-four rows includes two NA/VALIDATION_INELIGIBLE. S15 starts three rows; no collision. |
| 11 | `a55531e5425160f4350936d16e2a078ce8023049ec5455f6e8b8f9310e7134ed` | Yes | S15 Continued joins five rows including NA; S16 sixteen rows and S17 counts clear; missing median inputs retained. |
| 12 | `0e6df4761f0fe32cf232e86ce2b49bf8f00d9981dc435c521a660f01ca17046a` | Yes | S18 eight rows, S19 six rows, S20 four rows intact; unavailable p-values/noncausal limit retained. |
| 13 | `028bfd038786e6833fc872158c91084d6216e6e498bbcdeb1f7e4abd047e5b28` | Yes | S21 six rows includes three upper-target NA; S22/S23 four rows each intact; target/forecast crossings distinguished. |
| 14 | `69907d285b536956d5cbbf3451fb89bbe3a87808eb7c9de0a3776fa4f241b814` | Yes | S23 conventions/common-pool displays/S24 settings intact; wide formulas fit; footer clear. |
| 15 | `414313cc26f53c796fc966fc171cb178fd0af7564403951045db711220b2c101` | Yes | Ratio/MCSE display/MISMATCH/failed-candidate boundaries retained. S24 starts eight rows. |
| 16 | `075e71af6a4ff010d3414279032b021d7ec6b42979bef2a0c16fe75d0c945828` | Yes | S24 Continued joins four rows; S25 six rows and S26 eight rows intact; retrospective/MISMATCH/NA retained. |
| 17 | `8804052af67bfa5632b1081f83ba3658b4277ba3e1c52ff14544817daefb9f1a` | Yes | S27 twenty-four planned cells includes seven FAIL rows; rotated headers dense, no clipping/collision. |
| 18 | `f78d8660e8637a257c232fb9ae7eb9473826f5783bbc9c0420173fc67a453f29` | Yes | S28 seven failure rows; S29 starts fourteen source rows, continued-next-page note/header intact. |
| 19 | `36fc53f56bae6ebd73ba754aca0175bfb2c82575035e28c1411d5aef689c62ce` | Yes | S29 last FX-hourly row and OF/NR notes intact; S30 twenty-six rows/whole-cell failure policy retained. |
| 20 | `a4749d4c2a9f4578d26c822e22c8fe4c43af157e84da197dd1702b6821d751eb` | Yes | S31 twenty-six rows includes two FAIL 31/32; S32 starts twenty-seven rows with continued-next-page note. |
| 21 | `b6f246f407dbb4c07f8be9be56f38b5923a6f14795b79f17659cf15ed2537848` | Yes | S32 repeated header joins twenty-five rows, total fifty-two; S29/menu-isolation text intact. |
| 22 | `17f5af48585f2e08ab72c16aad3a3335c10d3e90183207bc6d6460146666af8b` | Yes | Figure S1 four panels/all-source denominators/IQR/both NA(12/13) labels and failure limits intact. |
| 23 | `c0eab9aaf03c625b2d077b2f1deae4ba5e4e4c5ee52f3a3e23bc8c5fe4fd74c9` | Yes | S33 eight rows/all-source NA intact. S34 starts thirty-four rows; small dense type, no physical collision. |
| 24 | `2632dd4837708d906615fd5923b4fc6579cb78dd05b0931cc8ea49fadd3acfdb` | Yes | S34 repeated header joins seventy rows, total 104. Both TIPS-G11 FAILED/31/32 rows retained. |
| 25 | `9cacdede0b7aa201b4a269fe973f772b1e4006557817553d67b00986c12a2169` | Yes | S30 release-time limits and all seventeen contracts intact. Uncaptioned contract table consumes S35. |
| 26 | `ed43fde1c628e4de9e16c07346205f40359168343acd9dbb3c4456f57c31a7bc` | Yes | S31 counts and Tables S36-S38 MCS intact; bold/NA/short-ID superscripts discernible. 7.1pt type needs zoom. |
| 27 | `6f5b837a329d0ab1b338b4e24ee38e97972890e7c7209fe254e3fdf2f8b4e663` | Yes | S39 four earlier-FX rows intact with NA/superscripts. 7.1pt type; large lower whitespace. |
| 28 | `3ecdf339a5da092d09aaece98c27d2f71e3b2836427d97e89c6af6f78e299f1a` | Yes | S40-S42 Treasury MCS blocks, four rows each, intact. 7.1pt type/superscripts without clipping. |
| 29 | `920ba74d16570a20947287adab556d836fd08161e69d2bb233ef2ba51278942a` | Yes | S43 forty-eight NYFed rows and eighteen columns including Source/H/W visible. 7.1pt dense type/superscripts need zoom. |
| 30 | `f0f8461ca63e7e2938dc995773575d95d3fc93b1e5615e04df1d863a3c870239` | Yes | S44 four daily-FX rows intact. 7.1pt type; very large lower whitespace, no clipping. |
| 31 | `34383118afe81fc06b6a4b1dff17e04966c657a61ec4f8fb6c9a7543323dd22b` | Yes | S45 thirty-four CFTC rows/two histories/classes/bold values intact. 7.1pt type needs zoom, margins clear. |
| 32 | `c1f3a78efbe0ad042dc308a8fe1e4cee3228c7df22dcd6a0e11dc98c45a0e2ac` | Yes | Method legend M01-M41/Class intact. Uncaptioned legend consumes S46. S32 cost formula/counts intact. |
| 33 | `ee07e23e976be43baa6cdd4e32c9c9fa01b0d1fe8c7c49a7e3547099bc68790a` | Yes | S47 Panel A three rows/Panel B five rows, adjustments/hit-grid/reproduction limits clear. |
| 34 | `6bf1017b548cc90049bc226f50cd1701fdf861cd9445917c458e13a875472dd0` | Yes | Figures S2/S3 curves/legends/units/crossing limits intact; captions/footer clear. |
| 35 | `91aabf9b8e79afde1d48e486005de03e1abd36bed8617eb30c04665c052b6930` | Yes | S48 three criteria includes Not supported/counterexamples. S35-S36 retained-scope limits clear. |
| 36 | `954a725e7712bc1376ccd2e49dd1df2d29dab2e10387b3358f42729ccdbd64d0` | Yes | S36 whole-cell/upper-tail limits retained. S49 six groups plus total/98/98/sixty unavailable procedures clear. |
| 37 | `b0e67480cdbacbb6a083c4470d5c4ea243f2996234377fdf26162a77c672a3d5` | Yes | S38 rejected repair/6 of 10 agreement/three failed 99% cells retained. S50 four rows includes Four-feature H6 Fail. |
| 38 | `83b0a5bc6b84eeb11fcc6df77737d5359b41bed293568c448f8a970c8a30e626` | Yes | Figure S4 four panels/13 and 17 labels/two validation markers/timing limit intact; separate y-scales clear. |
| 39 | `6791a05f75fb0418dbe5c042442e958e6498295b40f0cea83bec963817f5d538` | Yes | Fallback protocol/8 of 60 adverse losses and S51 eight rows intact. S52 five screens includes Not supported/Not testable; partial support retained. |
| 40 | `e445952e4f24baf816216f3797d248348993aaca7840b1cd8419785a85b07819` | Yes | S53 twenty-five counterexamples/signs/three-history sequences intact. Provenance distinguishes local design/public upload/audited status. |

## Handoff

Repair old main footer problem and directly inspect new PDF pages. Old page review cannot automatically approve any regenerated page.
