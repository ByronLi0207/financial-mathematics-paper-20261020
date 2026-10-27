# H8预备视觉检查：ASMBI补充材料

结论：**PREVISUAL_PASS_WITH_ONE_NONBLOCKING_EDITORIAL_NOTE**。当前PDF共54页：**本agent直接查看10页，另外44页以严格PNG哈希相同继承同团队真实直接查看覆盖，未覆盖0页**。没有把继承页写成本agent直接查看。

PDF：`submission-package/ASMBI/supplement.pdf`；SHA256：`dc0064cef0188be564d84e885f07d8682fc0d62f13b28f60366e026bbdb92bce`。

直接查看页：2, 45, 47, 48, 49, 50, 51, 52, 53, 54。H2比较中不匹配的9页全部直接查看；第48页额外复看。45页原本可按exact PNG继承，其中第48页此次也直接查看，最终继承计数为44。

继承链逐页核实：当前PNG → H2 corrected PNG → H2原始真实direct PNG，三份实际文件SHA256相同；原始报告明确记录每页 `tools.view_image`、`directly_viewed=true`。H2 corrected报告的存在本身没有被当作直接查看证明。

## 重点结果

- S39在p47–48：partial support、仅W520新增、先本地设计后计算但公开上传在后、QR33高区不可检验均可见。Table S53全部25反例保留，分组2+7+5+11，未见截行或遮挡。
- S40/Table S54在p49–51：36个行ID全部在PDF提取文本中各出现一次；逐页完整显示10/16/10行，Panel A为29条主/次预测，Panel B为7条独立QR4敏感性；不支持与未定状态保留，续表列头与长数值换行清楚。
- G1在p45：四句话完整保留99%失败范围、1e-6下6/10兼容、拒绝修复和阻止三次更改重跑、原不可用值及两项未定。
- 既有两处captionless longtable位于p31、p39；这些页与原来实际看过的PNG完全相同。保留S35/S46原有隐含计数位置，邻近显示编号仍为S34→S36、S45→S47；未补caption或重排旧编号。
- References[1]–[36]在p51–54。p53的CFTC条目含完整URL；p54是三条完整新增文献与DOI，不是URL孤立页。没有可见裁切、页脚碰撞或缺字。

## 非阻断编辑项

**ASMBI-SUPP-PREVISUAL-E01，p51。** Table S54后仍印有：`Main Table numbers use the recorded H2 aux cut and require a final H8 check; supplement references are local.` 建议root最终核对表号后删除这句制作说明，再对受影响页做最终H8检查。本检查未改源或PDF。

## 逐页证据

|页|覆盖|PNG SHA256|观察|
|---:|---|---|---|
|1|exact PNG继承团队实际direct|`57b0e6fd3bfdb94fdae8a30be6c81268e0cfe9aff28085d1c8ae139cddd1fd74`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：标题和范围说明完整；NA 与失败不混同的保留说明可读；目录 S1–S23 页码列对齐。|
|2|本agent直接查看|`27dc65cd1fa5c8f9a028fcd350261cdc6d297ec56907a0786e36ea06f7fbeae9`|直接查看完整原图：目录新增S40起始页49、S39起始页47；S1命题、条件概率、上下标和页码可读，无遮挡或裁切。|
|3|exact PNG继承团队实际direct|`714bfc8d7ef29e3d288b6d7f7674f0fb8dd92f0a3c1a56f4b3702c846bcee105`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S2 页码与目录一致；最大不等式、严格事件与原子证明及反例段落完整；S3 从本页开始。|
|4|exact PNG继承团队实际direct|`221c4b81ad5233f5c9619c8abadb5f794b1ab86f8eb2ebbe0881f17f12e64567`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S1、S2 所有数值列和多行表头清楚；负增量敏感性仍在表内，页末自然续句无截断。|
|5|exact PNG继承团队实际direct|`b03fd6d33709d63aa90c7b180589e161f5b4a9d71bb8b5f081ae0b66bfab4c6a`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：上页续句完整；表 S3 18 行及零计数完整可读；S5、S6 均与目录定位一致。|
|6|exact PNG继承团队实际direct|`65b972ac3bb20718ad6564fd4cb3806998feb25148242e733edae80f9f1a21c8`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S4、S5 完整且负百分数与检验数值可辨；S7 重播恒等式清晰，页末自然续词。|
|7|exact PNG继承团队实际direct|`27169eb5ed839919e976480e63fc51c999ed55d11d43ec55e6dc9558827aa8a6`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S6 保留全部不利 breach 比较；S8 和表 S7 普通分位秩数据列对齐，无裁切。|
|8|exact PNG继承团队实际direct|`60fbfcad24f7e4719be25744a1d479d64b388d3dc5fb00086b60ab4e96424b22`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S9 固定误差权重公式及表 S8 的长有理数分数处于各自列内；S10、S11 标题和正文清楚。|
|9|exact PNG继承团队实际direct|`919751971da1d96740f620d98e6a31ede1b44519d656978e2c1935176a828405`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S9 24 行与表 S10 起始两行可读；列标题重复层次清楚，系列名自然换行。|
|10|exact PNG继承团队实际direct|`7406cb0a77351c6e17b1b5125ebce8c013c1a2be05a8f04f8f20a6107dd4f83b`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S10 Continued 标识与列头重复完整；长系列名在首列换行，不侵入数值列；S13 正文完整。|
|11|exact PNG继承团队实际direct|`735e403ec0eb98ae69c4479b1e684e1c74704307e46402e378dc52f6486bf106`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S11 的全部 12 个系列及四组 horizon/history 可读；S14 说明及表 S12 起始五行完整。|
|12|exact PNG继承团队实际direct|`64d27d6631139ff786fb29565796211b26b3bb4fa6c095f012a082dfde0278d9`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S12 续表列头与全部余行完整；三项 NOT_MET 和表 S13 的四个 FAILED 行及失败原因文本明确保留。|
|13|exact PNG继承团队实际direct|`e47654f2a2c8d6d48fb06ea0a462bb45f9cc64fe55dd798d41e43b97d619d60a`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S16、表 S14 完整；Bills 24/260 两个包装器均为 NA，VALIDATION_INELIGIBLE 原因保留；数值与状态列无碰撞。|
|14|exact PNG继承团队实际direct|`d7ee5bc04d9624a381631409c31784582d59fee7fbb50f1585479d09cabae22a`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S15 末行 NA 及缺失 p 值解释清楚；S18 与表 S16 前六行可读，表格在页内收束。|
|15|exact PNG继承团队实际direct|`17c3503642e05a5aa2ca1ba69dace4a334557f9016d83186de92d5972d8fb47c`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S16 续页重复表头；表 S17 显示 Median 8 complete/48 unavailable；表 S18 全部 CROSSING 行可读。|
|16|exact PNG继承团队实际direct|`3ac2a4ca00b6609e898385e9236e127f791a2dd5230ddce946142bccabe2b293`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S19 续段清楚；S20 的表 S19、S20 状态与原始/调整 p 值分列；S21 明确保留上尾不可用结果。|
|17|exact PNG继承团队实际direct|`c3d66730c70b18d8fd7ed902a4b39d158411fba7a59b78ad346a0453d85f1cea`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S21 的三个 0.99 目标行均为 NA；表 S22 和 S23 全部可读；条件命中定义与公式字形完整。|
|18|exact PNG继承团队实际direct|`9ad70ec194758f5b5761bceded5b46e28195a0740955d299d500682ab291055b`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S23 实现与推断说明完整；共同样本池距离公式与上下标可辨；正文及页码无重叠。|
|19|exact PNG继承团队实际direct|`e2e89c17bba5f3e531f5a668991831e61ed864a7c8fcd864bcb265c6433ead57`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S24 模拟机制和 MCSE 公式清楚；MISMATCH、失败候选与完整程序 NA 解释保留；页末路径按行自然延续。|
|20|exact PNG继承团队实际direct|`0df154592da30d335974b225afe46fa4e927d3da6553b098ea70f1a5284f5a7d`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：上页路径续文完整；S25 表 S24 全部 12 行清楚，负向例外与 breach 增加均保留；S26 起始公式未越界。|
|21|exact PNG继承团队实际direct|`190f312213889e384898a41e6f8f542afcb6026e70c892f9da47d45a090ff24b`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S25、S26 两组 full-prefix/rolling 对照完整；旧 breach-count NA 保留；Bartlett 带宽与标准误公式清楚。|
|22|exact PNG继承团队实际direct|`e4eec0ea066deefb6816ebee62d3c6eda26faec7d3ab3a9a00906ffa21042dd3`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S27 表 S27 全部 24 个计划格可读，七个 FAIL 行、complete/required 与竖排表头完整；脚注无裁切。|
|23|exact PNG继承团队实际direct|`e82236e8d43a6e2f44e5aa01d0088991820ca97351dd895545cb5b28634c409d`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S28 全部七个失败格原因可读；S28 稳定性公式清楚；表 S29 前 13 个来源行及续页提示完整。|
|24|exact PNG继承团队实际direct|`477afe8ca7fd199494dc7250341c05c65d64d3e81ead59b60f066624484cc6f5`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S29 续页重复表头，FX daily NR 和 FX hourly OF 可读；表 S30 全部 W=52 条件比较及失败边界脚注明确。|
|25|exact PNG继承团队实际direct|`97c10bd3785d7bf140c65832451461f7ab0c4625fc4bf034a37141b6fa246c64`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S31 两条 TIPS-G11 FAIL 31/32 保留；表 S32 起始 26 行完整，列头、脚注、续页提示均在页内。|
|26|exact PNG继承团队实际direct|`6367184c768e4afb20c4cf2acc80dffd99575d20c9100a53dfdbb4b0bb165b00`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S32 剩余 26 行重复列头，所有 F 行 32/32 可读；S29 与 S29.1 起始位置和目录页码 26 一致。|
|27|exact PNG继承团队实际direct|`852844a590b29afc39938d00a4f60b587c4f67b801600cafb97281869378bf88`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S33 两条长历史 full-regression 汇总 NA 与 missing 1/1 保留；M1/M3 hold、M2 fails 和无子集替代的说明可读。|
|28|exact PNG继承团队实际direct|`99e3ed7837125063efe730d976f853aea621a8ddfbfe3985867786127b50c4ad`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：图 S1 四个面板、点型图例、坐标和图注清楚；两个长历史全回归面板明确显示 old/expanded menu NA (12/13)，无被掩盖的缺失项。|
|29|exact PNG继承团队实际direct|`eac7fe07157584776c1376be7e676f02d7415404fd97b3aeeaa4a6f7b5167c36`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S34 密集长表首段完整，所有列处于页内；两条 TIPS-G11 31/32 FAILED 与 NA 可辨；页末行和页码无重叠。|
|30|exact PNG继承团队实际direct|`169cfa3813ce985e90aa16524debacaa91f2549108e44650e9a2b9003ca42fe6`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S34 余行续页重复列头，长表终线完整；各 source/arm/history/predictor 与状态列对齐。|
|31|exact PNG继承团队实际direct|`2260deff4ad51658b21c5ff91aa91772836ec84bb5975e8bb30b8edad8976813`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S30 CFTC 来源及信息日期说明清楚；17 个合约来源的代码、名称、open interest 与 877 weeks 完整；长名称自然换行。|
|32|exact PNG继承团队实际direct|`04c12cce95138ea1ce591e06b96cd6e505f1a3af185d7ee704ed28931a8e42e7`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S30 续文包含十九个成熟分数、六期延迟及两项 schema 澄清，原失败尝试仍被说明；大段留白无丢页征象。|
|33|exact PNG继承团队实际direct|`9e7e7d44c83aaeaaf02800a8b56d33f439be12c3406dfaad1e1ad54a9a34ec43`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S31 完整 MCS 规则和 98/98、60 unavailable 说明清楚；表 S36–S38 的三块列头、粗体成员、NA 与上标类别可辨。|
|34|exact PNG继承团队实际direct|`ce9ecfa107311b8cc7e1e27584cd8bf397b8ad7a873272e22fa69450d2492711`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S39 FX early 2015 四行完整；NA、破折号及 exact-loss 类别上标清楚；页内留白属于单组表排布。|
|35|exact PNG继承团队实际direct|`6954e6061a4698ebaf646e73296b5b232267b7cd209aee305b1e6ba56b5ab741`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S40–S42 Treasury bills 三个方法块均有完整表头和四行；NA 及粗体成员可辨，无列越界。|
|36|exact PNG继承团队实际direct|`0866ca1e18541ee08d7e4ed61adaecbe16cfa8d22f02b522e869c0792e6584ff`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S43 48 个 Other NYFed panel 行完整；较小字体、竖排表头和上标在整页图像中仍可辨，末列 Median combination 的 NA 保留。|
|37|exact PNG继承团队实际direct|`4c343315bf7877fc556c1d0387c58c0fb35eb798a014e4f851993bdc9fa1a3e8`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S44 四个 same-record daily FX 行与 full-grid n=501 标签清楚；所有表线和成员粗体完整。|
|38|exact PNG继承团队实际direct|`44a917e6ad8f25239cfba3f002501fc272e781ef97b30e0f8a1ae776e485a1bc`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：表 S45 CFTC 全部 34 行（17 合约乘两历史）处于页内；上标与粗体可辨，未见数值列相撞或切边。|
|39|exact PNG继承团队实际direct|`6543804db77ff44854bf717d2a9c0783fc1c0ae6889dda9e6d2ac6a5b93f32a0`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：完整方法图例 M01–M41 及类 H/C/B/R 的列对齐；S32 固定成本公式与参数网格清楚，正文未越界。|
|40|exact PNG继承团队实际direct|`b746ce45e2ec7f0bb282b11de7c9ccdc3c8c7b100345acab194d314adaf84445`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S32 184,464 cost rows 和 18,522 primary grid rows 明确；表 S47 两个 panel 可读；S33、S34 与目录页码一致。|
|41|exact PNG继承团队实际direct|`f15cd51f05ae72a02a37f239ae09cd89ac5510119e6c339b1b54fe005d6265bb`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：图 S2、S3 各自的图例、坐标、货币单位和完整图注清楚；两条折线与交叉性质未被图注掩盖。|
|42|exact PNG继承团队实际direct|`bcc1a7f0ead9b3122bb805bb2c196f0384417cce35c508c1116b0e5e7f5c01c4`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S34 可用性边界完整；S35 表 S48 明确保留 42/48、100% required、Not supported 的通用排序反例；左删失 not testable 说明可读。|
|43|exact PNG继承团队实际direct|`1a98d52b65e2845b383d97fda73798e16b6ad66d54447085b8a4faee1ab9dacf`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S36 保留的范围限制完整，含未独立 dealer 验证、经验因果未解、失败及 unavailable 状态；正文与页脚间距正常。|
|44|exact PNG继承团队实际direct|`4d33116b5563fb3e0d8f60d7d8a60c43f05c1fdd6aee5efda739faf0793da7bb`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：S36 额外检查说明清楚；S37 表 S49 全部 98/98 比较、90/98 matched-history included、60 unavailable 仍可读；无表列错位。|
|45|本agent直接查看|`6d4152d154a18ae6391d353637bc160c05dbec96940bbeb6c9107c9fc8acc22d`|直接查看完整原图：G1的四句话完整显示99%失败格、1e-6容差仅6/10兼容、拒绝修复并阻止三个失败比较重跑、原不可用值及两项未定继续保留；Table S50四特征短horizon的Median screen=Fail清晰。|
|46|exact PNG继承团队实际direct|`087bb55fc0a8ef8d8041125efb6008a8d581f7fbee29a421069fd82869dbfb6a`|与H2 corrected及原始direct页三方哈希相同；原始direct观察：图 S4 四个面板的 52/156 validation weeks 图例、所有系列/合约标签、纵轴和图注清楚；极端反例点未越框。|
|47|本agent直接查看|`96e2099312182cea8c8dc16ad2d26b09df8ce679c0117f7a00c4a5086e1d1ad3`|直接查看完整原图：G3保留62全部完成、8/60尾部失败、最坏+80.98%、fallback32/28及回顾性限制；S39完整陈述仅W520新增、设计本地先于计算但公开上传在后、两个低历史屏通过而高历史/顺序改善失败、QR33无高区、整体partial support。|
|48|本agent直接查看|`cf3b50bcb945241d64aa8edc9df1ce47eb0e9a0294e1a5eaa370903785b77d40`|额外直接复看完整原图（本页亦与H2真直接查看PNG完全相同）：Table S52五行判断齐全；Table S53完整25行反例，分组2+7+5+11，符号与三历史序列可读；未测试与不支持未合并。|
|49|本agent直接查看|`2e86df8bdf5bf14586fdf0246d91d72e47596364986392800e88267a5b8a0eb0`|直接查看完整原图：S40解释与Table S54起始清楚；Panel A前10行完整，29主/次预测与7条独立QR4敏感性分区说明可读；长表页末Continued on next page与页码不重叠。|
|50|本agent直接查看|`e4c5ad3bb7ada57280d77182b735594feed55d68becc061e51e3211f7dfbd989`|直接查看完整原图：Table S54 Continued与6列列头重复；16行完整，F3两条UNDETERMINED、G3尾部失败、WP2两个低区支持保留；长数值和状态换行均处于各自列内。|
|51|本agent直接查看|`ef16d39c5264549614353ed61fbcd275b815b8d68f6a179378fa1a1fbfc24ca6`|直接查看完整原图：余下3条WP2主/次行及Panel B全部7条QR4敏感性行完整；NOT_TESTABLE与UNDETERMINED、F2QR4两个未定、G2QR4不支持保留；表终线清楚，随后References[1]-[3]完整。表后仍有要求final H8 check的制作说明，见编辑项E01。|
|52|本agent直接查看|`f8c387fbb3b1a49f2bd4800b7b727279397f495340aff0a4429d2f949f7490de`|直接查看完整原图：References[4]-[18]完整可读，长官方URL自然换行；[18]的DOI在本页收束，没有跨页URL孤段。|
|53|本agent直接查看|`9de21a01258727f5564ddbf31cf856be80a912e95cd9a1cfd16a0f08d7d648a9`|直接查看完整原图：References[19]-[33]完整；van den Hoogen、Wisniewski与CFTC条目及URL可读；CFTC n.d./检索日期/官方URL同条同页，不出现空字段标点或URL孤页。|
|54|本agent直接查看|`22a26c1175226557f46be53685ceb465fc848de41e95e9352b33ac4230b48a46`|直接查看完整原图：新增References[34]-[36]均为完整条目和DOI，全部在页内；尾页留白为完整三条文献之后的正常留白，不是单独URL页。|

## 边界

这是当前H5字节切片的预备视觉检查，不是之后H8新字节的自动通过，也不是金融复算、文献事实或期刊政策合规审计。使用既有ASMBI Free Format/AMA产品，不声称原NJD类编译。只写本Markdown及配套JSON，未改源码、PDF、RELEASE或任何科学结果；未提交、未另派代理。报告终写后冻结。
