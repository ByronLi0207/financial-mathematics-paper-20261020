# E7 最终原生 PDF 视觉检查：Supplement B／标题页／投稿信

结果：**PASS，负责范围内无阻断性视觉问题**。时间：2026-10-25T00:18:22.410332+00:00。

逐张通过 `view_image(detail="original")` 打开补充材料18–33页和标题页、投稿信各1页，共18张1500px渲染图；不是只读文字或拼图抽查。每张PNG的SHA-256均与原生编译记录相符。只写本记录和JSON，没有改稿、重编PDF或读取金融数组。

源ZIP：`bea59ba142898dc83a763419bc13cf50471bcf3a903e79013b7add73508af501`，29 members。仅负责的三个最终原生PDF如下；本轮root另改主稿结构并重编，主稿最终SHA与视觉检查由root单独记录。

|PDF|页数|最终原生PDF SHA-256|
|---|---:|---|
|submission-v10/supplement.pdf|33|`8d67122b814b2b01410fceb0499c6c3aee92def0ccbd38603f68f2d21997cf0a`|
|submission-v10/title-page.pdf|1|`aef9bf4f87aa65eb7e10694a0c0342c4c56ae723db578cb997e77489ae606a0a`|
|submission-v10/cover-letter.pdf|1|`77da3a58886383bcb3c9c43fa40dced454b182943279a9bbabba2c34871a3755`|

原生输出、投稿目录PDF与编译回执三者指纹一致。

|图像|SHA-256|视觉观察|
|---|---|---|
|supplement p18|`7fec32a09d461b2ac0c91bb8a8f62e5b5b232f7653af02a905e84e4541feea90`|S29 stability table and S30 W52 comparison start are legible. Upper inline fourth-moment condition continues fromp17 and its final inequality is entirely visible; no clipping. Table headers, dashes, NR/OF states and continuation footers are clear.|
|supplement p19|`cc5d32ebea0f0c7715554cdc42a91332935ba7402a43c68b3d5faeaf0f550f98`|S30 continuation and S31 W260 table are readable; bold FAIL31/32 and unavailable dashes distinguish failed whole cells. S32 benchmark table starts with clear header and next-page marker.|
|supplement p20|`245cce81a8c19668400f7edeb161333e46becc1d83b4e96821993a4ff7522568`|S32 benchmark continuation retains source/arm/W/R/loss/hit columns and descriptive IQRs; table bottom rule and full explanatory text visible, with comfortable margins.|
|supplement p21|`17d5c2288d40a5cc69a429aed9f5b5f9096085a0c219b7c8ec2f044ed0c3ed37`|S29 paired-menu section and S33 inventory start are dense but readable at the1500px render. Old/expanded columns,32/32 versus31/32, NA and FAILED states are distinguishable and inside margins.|
|supplement p22|`60ae04240ef021eab64864ab6c4bfa7c6129e87a31bca57c09313ce21c1f2284`|S33 continuation repeats caption/header; all columns through State remain visible, and the explanatory NA/whole-cell note follows without overlap.|
|supplement p23|`7bfc6d5b0a6c2e1c6b3eab9a114b86ac574e0f52ba829517d23d44434a52e0fe`|CFTC sources/eligibility/information-date section is legible. All17 literal codes, contract names, meanOI andWeeks columns are visible; long names wrap within cells. ACI/date/count-clarification paragraphs extend safely above footer.|
|supplement p24|`6c65e3e20f12ac17140856f330cf4408df85ee4d0530a51819516f6705df2c30`|S31 MCS explanation plus FX-original method blocks1/3,2/3,3/3 are all visible. All method headers, p-values, bold membership, exact-loss superscripts, NA and emdash entries are distinguishable; no cropped rightmost column.|
|supplement p25|`bae3636f03fd1bc9ea26711e0404386b6c0ed850917ff19eb1ae2a9379ed08a8`|FXearly2015 MCS block1/1 shows all method columns and four origin grids clearly. Large trailing white space is a deliberate group-page layout, not missing/overprinted content.|
|supplement p26|`9db028f12c55484d8dfb188660452271330051d78488b25d1f7b65b15e21bea9`|Treasury-bill MCS blocks1/3,2/3,3/3 all fit within margins. Rightmost headers and exact-loss superscripts remain legible; NA and unregistered dashes are distinct.|
|supplement p27|`2ff592019f16f13c7cff15502ffcab12d9554ae92b5b9a95303a00ea99ca26c3`|OtherNYFed panels MCS full table is dense but all48 rows and headers throughM41 are visible. Bold inclusion, superscripts and final NA column remain readable; bottom rule is above footer.|
|supplement p28|`59032e72e47abe40f8a3946aa6fc5231dbddc5a4646db5fa53be1562a0827789`|DailyFX MCS table shows its complete compact method block with source/H/W/M01/M20/M21 headers. White space follows an intact table; no missing glyphs or clipping.|
|supplement p29|`65ffdee8bf22c4d34ebfb8fe728cd4dac49867ec105634b24085e4a86076641c`|CFTC MCS table displays all34 contract/history rows and all six method columns M01/M02/M06/M07/M08/M09. Bold inclusion and superscript classes are legible; row labels preserve alphanumeric codes.|
|supplement p30|`f13bf9584a745c21228671906d5cfb18fdeab212f573ab365eb2606965bd7708`|Complete method legend M01throughM41 is legible. Long qualified IDs fit within full-ID column; class codes and explanations of NA/superscripts/exact-loss classes are complete and no rightedge is clipped.|
|supplement p31|`4c7587a387d033c3b89c58789ca788d4cfbfaa65c8818009ecefc8a5424b68c5`|Cost/reproduction sections and S46 accuracy/hit diagnostics are readable. Both table panels, numeric exponents, named adjustments, footnotes and bottom continuation text fit without collision.|
|supplement p32|`7bbc70b6eb861731e130f8280aad8edfcad8ea2c5c2428d58e9c0075940828c7`|Both Murphy diagrams have clear axes, currency-unit labels, blacksolid/graydashed legends and captions. Curves, ticklabels and negative/zero positions are not clipped; no raster artifacts obscure the plot.|
|supplement p33|`1e630f879c5c0784c45b49bfb50eaf44e66a992d7d9f76f354ca5306f4fb2459`|Reproduction paragraph continuation and closing routes-to-evidence paragraphs are readable; footer33 is visible. Sparse ending is normal; no unintended blank page or placeholder appears.|
|title-page p1|`963f9dad91f939ead60120cce6422ed22adc6d439044574f3cbed33cbefc5f90`|Title and author/declaration template fit on one page. Expected TOBE COMPLETEDBYAUTHOR fields remain visible for authors/affiliations,correspondence,ORCID,funding,conflict andAI; repository link visible. Title word Models breaks Mod-/els across lines, a cosmetic hyphenation with no information loss.|
|cover-letter p1|`96ec3d2d5efd7dfb13cfd6752307a0c143014213e3de7dcbd7ba63c828b7cda6`|Single-page letter is legible from salutation to signature. Paragraphs, percentages, method labels and deliberate author signature placeholder fit inside margins; no overflow, blackboxes or overlapping text.|

MCS各方法分块、完整legend、NA／未注册破折号、加粗成员值与exact-loss superscripts均可辨。两张Murphy图的轴、单位、线型legend和caption清楚；没有发现裁切、重叠、黑框或不可读符号。

补充材料p18顶部完整承接p17的inline fourth-moment条件；不等式尾部和后接句均在正文范围内，没有丢字或裁切。p31文字在p32浮动图页后由p33续接，属正常分页。

仅一项非阻断性观感记录：标题页标题中的Models自动断为Mod-/els，不损信息。标题页作者/机构、联系方式、ORCID、资助、利益冲突和AI声明，以及投稿信作者签名的待填字段按要求保留；没有把视觉PASS当作作者信息完成或可直接投稿的证明。

本记录只认证以上18张图像与三个PDF的已检查字节；补充材料1–17页及主稿由其他检查者负责。后续这些PDF如发生变化需按新指纹复核。完整逐页尺寸、bytes、SHA和观察见同名JSON。
