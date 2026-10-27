# H8预备视觉QA：ASMBI H5正文与标题页

UTC：2026-10-27T05:09:23.036226+00:00。**结论：需修复第3页叙述引用作者标签，当前cut不判PASS。**

实际逐页打开原图：正文26页＋标题页1页，共27页；全部`view_image(detail=original)`直接查看，H2继承0页。只写本Markdown/JSON，没有改源、PDF或其他报告，没有编译/commit/另派代理；cover按要求留待H6。

## 阻断项

**ASMBI-PREVIS-001 / 正文第3页**：三篇新增ASMBI叙述引用均显示粗体`(author?)`，后接上标13/14/15，未显示作者名。受影响key为`LeeKim2024ASMBI`, `Pagnottoni2026ASMBI`, `MuddanaEtAl2025ASMBI`。原图：[第3页实际原图](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/.scratch/submission/h5-manuscripts/ASMBI/manuscript/page-03.png>)。

根代理已确认这是AMA BBL作者标签与natbib叙述引用的包装兼容问题。三条参考文献本身完整存在。后续按授权仅在ASMBI派生包装转换这三个确定key为显式作者名＋数字上标，canonical不动；本轮没有修复。重编后须以PNG精确SHA比较，只继承真正不变页并直接看全部变更页。

## 本次PDF与图片身份

- [submission-package/ASMBI/manuscript.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/manuscript.pdf>)：26页；SHA-256 `d36157f653a553cdfd3e7d5f59d5f58c681341ae3dd724e941857380507549a8`。
- [submission-package/ASMBI/title-page.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/title-page.pdf>)：1页；SHA-256 `45e49feb9a1287aff8e28da4c9f0561305f2a8b5cec2e08288ee741ee916e9cf`。

渲染目录：[notes/submission/renders-h5-manuscripts.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/renders-h5-manuscripts.json>)；manifest SHA-256 `bbb183f830d8d177b7617a195dbe8fd26f31b7e4e3b827ee15010a73ef932ef5`。逐页PNG SHA见下面及JSON。

## 实际逐页记录

| 文件/页 | 方法 | 视觉状态 | 观察 | PNG SHA-256 |
|---|---|---|---|---|
| 正文 1 | 直接原图；继承否 | PASS | Title, abstract, declared author placeholder, 5 keywords and opening RQ1/RQ2 readable; 14.8/16.6,34/48,29/34,19.3→4.0 retained; no clipping or overlap. | `6a2aad8ad57d8bb2d107f9ef8cc24e44d752b8d29d221098f2e550b289c8760d` |
| 正文 2 | 直接原图；继承否 | PASS | Figure1 complete with USD millions/economic dates/legend and caption; three findings and RQ3 readable; 8/60,5/34,32/34,1/34 visible. | `3b5fe2579fb60481d5d2cb6434bec4c00539af54925e5d1b42bc9ff3b4760c6e` |
| 正文 3 | 直接原图；继承否 | FAIL_CITET_AUTHOR_LABEL | New ASMBI literature paragraph has three bold '(author?)' labels before superscripts13,14,15 instead of author names. Other text and target/loss equations readable. | `de55549fc3f477d0a6e57606b93793f7d51993e0b959e665ca69f263a0e447a9` |
| 正文 4 | 直接原图；继承否 | PASS | Both propositions and symbols/max/conditional probability clear; data definitions and18576/706/930/501/877 counts and publication-clock limits readable. | `ba58f84556b50b06f70bd7f7959219785648b535c6cfce3e5b0812fce0f0ae0c` |
| 正文 5 | 直接原图；继承否 | PASS | Historical-rank and ridge equations including lambda menu/infinity readable; tau19/20 and training-only scaling clear. Method acronyms expanded. Bottom paragraph continues to p6 without clipping. | `1a8253aeb6817e4802c2e4a3547988009e6aee1ddc4e7389428b7c51f5beb93b` |
| 正文 6 | 直接原图；继承否 | PASS | Evaluation formula, HAC bandwidth, round-specific timing, S40 reference, MCS90%/1000/bootstrap and dependence boundaries readable; page flow intact. | `bbead846ac0016d1d2462a2257494ee8a91aabc17f7b85bede52ea730eae3ae0` |
| 正文 7 | 直接原图；继承否 | PASS | RQ1 adverse31.5%/924vs427 clear; Figure2 fully visible with both curves, W360..5760, axes/legend/caption. WP2 heading has opening text before continuation. | `935a1361cd5020713d017d3e2ac34f9e12908031521bf866653cf16e0f196eb1` |
| 正文 8 | 直接原图；继承否 | PASS | WP2 continuation keeps15/17,29/34,10/17(58.8%),60%,6/17,untestable and partial verdict; daily37vs30 and CFTC baseline distinction readable. S49 reference resolved. | `b719dc776228f14fb607610fd901c0325afb693dd50ce8f07f15ed5ef7064cb6` |
| 正文 9 | 直接原图；继承否 | PASS | Figure3 full-page CFTC two-history plot: all17 codes, axes, signs, zero lines and source-unit/dependence notes readable; no cut labels. | `467f072f431f6c4c3a1fc9220bdd466814e6e0bede686a81b53325d54c6b1bc8` |
| 正文 10 | 直接原图；继承否 | PASS | Finite-menu title/27of41/29of41 and19.33→4.03 etc readable. Figure4 complete with both method panels, hatching/legend/actual dots/unavailable crosses; caption and QR4 failure text clear. | `3f1dda05af97bec34a6d793713492aab425af6c41442e565855a150b01560d5c` |
| 正文 11 | 直接原图；继承否 | PASS | Required numerical fits,6of10 compatibility,3failed retained and undetermined wording visible. Score/breach distinction and20.6:1 reference clear; cost formula and5/34,32/34,1/34 grid points readable; whitespace intentional. | `afb02564bc4ff38d0e8454bba7933a77143ffe0ae585c5564c42bf57385f5ff0` |
| 正文 12 | 直接原图；继承否 | PASS | Figure5 six heatmaps/complete counts/axis ticks/colorbar and full caption legible; reserve/breach coefficients and34/34CFTC,48/48panel labels intact. | `fc00b9ba4df9a5555d6bfe2ac86f82afed12031ded72e86d52a54d47c9d5581c` |
| 正文 13 | 直接原图；继承否 | PASS | Benchmark-default heading,156/5760,32fallback,0.00/14.63median,8adverse and80.98worst visible. Figure6 three panels and separate scales complete; practical bullets readable. | `045a71eaab55af0252dd355c7c0a59cf07f12c711677c35d3eb7a8e4abd873f2` |
| 正文 14 | 直接原图；继承否 | PASS | All8 limitation bullets visible including gross/hedging/capital and6of10 repair. S40 and conclusion intact; availability begins cleanly and continues p15. | `39a32df054f06b8f7c766bc58689970a1f3ae1a69a3ecb89821bbafa3e7a43e1` |
| 正文 15 | 直接原图；继承否 | PASS_EXPECTED_AUTHOR_PLACEHOLDERS | Availability URL wraps and author/license/DOI placeholders legible; references[1]-[3] begin. Editor list punctuation clean, no duplicated kern punctuation; no clipping. | `7f4305f32635f1b1963f25f3b78705722e13522d526614054f5622e8812f025a` |
| 正文 16 | 直接原图；继承否 | PASS | References[4]-[18] complete, URLs/DOIs legible. van den Hoogen2017 thesis institution punctuation clean. New refs[13]-[15] show correct two/four/single author metadata,2024/2026/2025,volumes/issues/eIDs/DOIs; no entry split or overflow. | `ec8fb5c0b8f6aa67a5d358e4d441aa54ebc131273a4e478394308fe5874e25f9` |
| 正文 17 | 直接原图；继承否 | PASS | References[19]-[32] complete; institutional author periods clean; CFTC[24] hasn.d.,retrievaldate and full URL. Complex DOI[26] angle/semicolon characters readable. No oldemptyaddress/doublepunctuation defects seen. | `794144dd1966429b6fbab78f4a3a313023a254f90a322ce0cc14c76470ff6e6e` |
| 正文 18 | 直接原图；继承否 | PASS | References[33]-[34] complete with author/year/journal/DOI. Sparse remainder intentional before separately paginated tables; no split entry. | `6480e80cdfd03e49b29c926bba126f92e67cdbd321775f2272c0ae34f5949561` |
| 正文 19 | 直接原图；继承否 | PASS | Table1 alone after references; all4study rows and4columns complete, booktabs and wrapped response/data/evaluation text readable. | `b4c50eae72e2a331273bbef4dc29ad6a783ac2714c957dbd2c93b0269500011f` |
| 正文 20 | 直接原图；继承否 | PASS | Table2 alone: PanelA5sources and PanelB5rows with nine numeric summaries complete; units/dates/SD/95th/headroom symbols clear. Notes18,570/924/700/871 andH6 not clipped. | `c299f57bbd75df127923e58451122c737bc890fd5e068f2ab424fbe0581c15bb` |
| 正文 21 | 直接原图；继承否 | PASS | Table3 alone and complete9method rows; infinity/six-point menu,history sets,ACI/SAV expansions and24FX/13weekly footnote legible. | `5956fb3b4dcea5a81968100dd28234dfc775a7f5854ab7500719473b0a571f09` |
| 正文 22 | 直接原图；继承否 | PASS | Table4 complete5FX rows; signs -12.66,-14.77,+3.17,-16.62,-15.00,issue counts andbreach pairs clearly aligned. Footnote retains2880/720 and3penalty distinction. | `42a80806eead1d0492a872b627675a21bb748fc87d3f16937b198eb7a8c86ad8` |
| 正文 23 | 直接原图；继承否 | PASS | Table5 complete8rows; +50.79,+144.30,+92.63,+9.91,+9.22,+.50,+4.15,+5.37 and45/48,37/48,34/48,30/48 readable;181.39% and unmet criteria note complete. | `19999a14fcb5dd3dbd28dd4fa96d1c6a4da858e3089190d68c12c639d4b5d8e1` |
| 正文 24 | 直接原图；继承否 | PASS | Table6 complete17contract rows and2histories×5method columns,negative signs andcode33874A readable; no clipped numbers or header overlap;60%/34/10% conditions andfullprecision note complete. | `cf7c36d72d73d5ed2c50654ecb16091816c1ebdec6d3df9f71389e73ef6ffb59` |
| 正文 25 | 直接原图；继承否 | PASS | Table7 complete4source/horizon/history rows with validation52/156 medians andlimit-selection counts; NewYorkFedH6-1.13 minus sign clear; endpoint/refit andpaired-median footnote intact. | `37bdeccf97a94dde64b3c08a7cac7dd3e338eed3abe7c9b8fb315684db6f76f2` |
| 正文 26 | 直接原图；继承否 | PASS | Table8 complete5rows at90/99%,+/-signs clear; NA visible forCFTC260 andbothFX99%; originalNA/rejectedrepair footnote complete, no split table. | `197162f98ea26a82a9018b0e73264ec60198d60ff5e7bc7027a07199a9057d2f` |
| 标题页 1 | 直接原图；继承否 | PASS_EXPECTED_AUTHOR_PLACEHOLDERS | One-page title: all author/affiliation/contact/ORCID/funding/conflict/CRediT/permission placeholders legible; runningtitle;4,121 narrativewords and exclusion scope;exactly5keywords;data/code statement all fit without clipping. | `2b786cf4a747db00da857283536df944dccfae7261acb4f5bd7d3062709ea43f` |

## 表、图、状态与参考文献

- **8表**全部在参考文献之后，p19–26各一张，表头、全部行、注释完整；Table6为17合约×两history×5方法，Table8保留3个99% NA。
- **6图**位于p2/7/9/10/12/13；轴、单位、legend、source/task counts和完整caption均可读，未见裁切/重叠。此为原图视觉可读性检查，不冒称新测量字号。
- **负面状态**：p11的required numerical fits、6of10 compatibility、3failedcells和undetermined；p13的32fallback、8adverse及80.98worst；p14新增gross/hedging/capital限制和6of10；p26的原NA说明均显示清楚。
- **参考文献34条**连续[1]–[34]，aux有34个不同被引key，p15–18直接查看。新[13]–[15]作者/年份/卷期/页码或eID/DOI完整；van den Hoogen/Delft机构、机构作者句点、CFTC n.d./retrievaldate/URL、编辑名单标点未见旧问题复发。长URL和复杂DOI字符没有视觉裁切。
- 参考文献检查是当前排版/连续性核对，不是新一次官方元数据、全文或逐条AMA规范合规审计。p3叙述作者标签问题与文末条目完整性分别记录。

## 标题页

- 一页直接查看，实际显示`Main-text narrative word count: 4,121`和排除abstract/citations/references/declarations/tables/figures/captions/displayed equations的统计范围。这里只核对显示值匹配要求，没有重新计算word count。
- 恰好5关键词：Peak net positions; Quantile forecasting; Historical benchmarks; Forecast comparison; Calibration。runningtitle、data/code、作者/affiliation/contact/ORCID/funding/conflict/CRediT/permission占位均完整可读。
- 个人信息、DOI/软件许可和权限占位仍待作者提供，未被当作已完成信息。

## 验收边界

本cut为`NEEDS_PACKAGING_FIX_P3_CITET_AUTHOR_LABELS`。正文其余25页及标题页未见新增视觉缺陷；p3修复前不能称正文全部视觉通过。该报告绑定本次PDF/PNG，不代表H8最终投稿包、supplement、cover或远端发布验收。
