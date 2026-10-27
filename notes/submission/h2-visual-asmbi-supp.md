# H2 visual inspection — ASMBI supplement

结论：**PASS_WITH_NONBLOCKING_EDITORIAL_NOTE**。全部 **50/50 页**均已通过 `tools.view_image` 逐张直接查看（每批最多四张完整页面 PNG），没有用缩略图拼接或文本提取替代视觉检查。未发现排版阻断问题；保留一项参考文献编辑问题。

- PDF：`submission-package/ASMBI/supplement.pdf`
- PDF SHA-256：`345173ce781ae55546f3e62f5aed16d905d3a52998ef03b4bc4556dbc0e0dfca`，当前文件与 H2 清单一致。
- `pdfinfo`：50 页，A4。50 张页面图像的当前 SHA-256 全部与清单一致。
- 清单：`notes/submission/renders-h2-all-pages.json`；SHA-256 `e27698b15c2b85a8a9460bb895d9f6ed68462920a35dedaa148291be8df0b301`。
- 本次仅写本报告及同名 JSON；未修改源文件、结果或 PDF，未重新渲染、提交或另派代理。

按任务上下文，此 ASMBI PDF 使用期刊允许的 Free Format 与官方 AMA；原 NJD 模板离线依赖不可用。本轮检查的是实际生成的 PDF，不声称原样 NJD 模板，也未独立复核官网政策。

## 重点核对

- 长表续页、重复列头、数值列、公式、字体、图例、页码与页边界：未见截断、溢出、缺字或影响阅读的重叠。表 S34 与完整 MCS 表字体较小，但在逐张页面图像中可辨。
- 目录 S1–S39 起始页逐项与实际页相符；S39 在第 47 页，独立参考文献在第 49–50 页。
- NA、FAILED、FAIL、NOT_MET、不可用检验及未测试结果仍在；没有用完成子集替代缺失整格的可见表述。
- G1：第 45 页明确保留 6/10 再现比例、容差及未通过门禁的 99% 重跑。
- G2：第 45 页表 S50 保留四特征短期 Median screen = Fail；第 46 页四面板保留分来源证据。
- G3：第 47 页保留 8/60 尾部不利格、最坏 +80.98%、历史默认 32 格/回归 28 格，以及尾部条件失败和回顾性限制。
- 导入 WP2 = S39：第 47 页明确为 partial support（PARTLY 的自然语言呈现）；第 48 页 Full/P2 为 Not testable，P2/P3 四特征为 Not supported，25 条反例（2+7+5+11）完整可见。
- 参考文献：[1]–[33] 在两页独立清单中；本轮不替代文献正确性核验。

## 具体发现

**ASMBI-SUPP-H2-01 — 非阻断编辑问题。** 第 50 页底部 References [33] 可见 `Historical compressed. ; . Retrieved October 24, 2026.`，存在空字段标点且未显示 URL。条目未被裁切，文献清单本身完整，但从 PDF 独立定位该网页来源较弱。由主任务核对其元数据并决定修正；本检查未改动。

## 逐页直接查看记录

每行“已直接查看”均指直接打开对应完整 PNG，而非仅查看文本、目录或缩略图。

| PDF 页 | 图像 SHA-256 | 直接查看 | 观察 |
|---:|---|:---:|---|
| 1 | `57b0e6fd3bfdb94fdae8a30be6c81268e0cfe9aff28085d1c8ae139cddd1fd74` | 是 | 标题和范围说明完整；NA 与失败不混同的保留说明可读；目录 S1–S23 页码列对齐。 |
| 2 | `5cf7cfdcfadf1dd1fd2d0d4bfd561e7e480af6e7f2bd3a47dbaf8011960669d9` | 是 | 目录续列 S24–S39 可读；S1 从本页开始，与目录页码 2 一致；命题、条件概率公式及证明未越界。 |
| 3 | `714bfc8d7ef29e3d288b6d7f7674f0fb8dd92f0a3c1a56f4b3702c846bcee105` | 是 | S2 页码与目录一致；最大不等式、严格事件与原子证明及反例段落完整；S3 从本页开始。 |
| 4 | `221c4b81ad5233f5c9619c8abadb5f794b1ab86f8eb2ebbe0881f17f12e64567` | 是 | 表 S1、S2 所有数值列和多行表头清楚；负增量敏感性仍在表内，页末自然续句无截断。 |
| 5 | `b03fd6d33709d63aa90c7b180589e161f5b4a9d71bb8b5f081ae0b66bfab4c6a` | 是 | 上页续句完整；表 S3 18 行及零计数完整可读；S5、S6 均与目录定位一致。 |
| 6 | `65b972ac3bb20718ad6564fd4cb3806998feb25148242e733edae80f9f1a21c8` | 是 | 表 S4、S5 完整且负百分数与检验数值可辨；S7 重播恒等式清晰，页末自然续词。 |
| 7 | `27169eb5ed839919e976480e63fc51c999ed55d11d43ec55e6dc9558827aa8a6` | 是 | 表 S6 保留全部不利 breach 比较；S8 和表 S7 普通分位秩数据列对齐，无裁切。 |
| 8 | `60fbfcad24f7e4719be25744a1d479d64b388d3dc5fb00086b60ab4e96424b22` | 是 | S9 固定误差权重公式及表 S8 的长有理数分数处于各自列内；S10、S11 标题和正文清楚。 |
| 9 | `919751971da1d96740f620d98e6a31ede1b44519d656978e2c1935176a828405` | 是 | 表 S9 24 行与表 S10 起始两行可读；列标题重复层次清楚，系列名自然换行。 |
| 10 | `7406cb0a77351c6e17b1b5125ebce8c013c1a2be05a8f04f8f20a6107dd4f83b` | 是 | 表 S10 Continued 标识与列头重复完整；长系列名在首列换行，不侵入数值列；S13 正文完整。 |
| 11 | `735e403ec0eb98ae69c4479b1e684e1c74704307e46402e378dc52f6486bf106` | 是 | 表 S11 的全部 12 个系列及四组 horizon/history 可读；S14 说明及表 S12 起始五行完整。 |
| 12 | `64d27d6631139ff786fb29565796211b26b3bb4fa6c095f012a082dfde0278d9` | 是 | 表 S12 续表列头与全部余行完整；三项 NOT_MET 和表 S13 的四个 FAILED 行及失败原因文本明确保留。 |
| 13 | `e47654f2a2c8d6d48fb06ea0a462bb45f9cc64fe55dd798d41e43b97d619d60a` | 是 | S16、表 S14 完整；Bills 24/260 两个包装器均为 NA，VALIDATION_INELIGIBLE 原因保留；数值与状态列无碰撞。 |
| 14 | `d7ee5bc04d9624a381631409c31784582d59fee7fbb50f1585479d09cabae22a` | 是 | 表 S15 末行 NA 及缺失 p 值解释清楚；S18 与表 S16 前六行可读，表格在页内收束。 |
| 15 | `17c3503642e05a5aa2ca1ba69dace4a334557f9016d83186de92d5972d8fb47c` | 是 | 表 S16 续页重复表头；表 S17 显示 Median 8 complete/48 unavailable；表 S18 全部 CROSSING 行可读。 |
| 16 | `3ac2a4ca00b6609e898385e9236e127f791a2dd5230ddce946142bccabe2b293` | 是 | S19 续段清楚；S20 的表 S19、S20 状态与原始/调整 p 值分列；S21 明确保留上尾不可用结果。 |
| 17 | `c3d66730c70b18d8fd7ed902a4b39d158411fba7a59b78ad346a0453d85f1cea` | 是 | 表 S21 的三个 0.99 目标行均为 NA；表 S22 和 S23 全部可读；条件命中定义与公式字形完整。 |
| 18 | `9ad70ec194758f5b5761bceded5b46e28195a0740955d299d500682ab291055b` | 是 | S23 实现与推断说明完整；共同样本池距离公式与上下标可辨；正文及页码无重叠。 |
| 19 | `e2e89c17bba5f3e531f5a668991831e61ed864a7c8fcd864bcb265c6433ead57` | 是 | S24 模拟机制和 MCSE 公式清楚；MISMATCH、失败候选与完整程序 NA 解释保留；页末路径按行自然延续。 |
| 20 | `0df154592da30d335974b225afe46fa4e927d3da6553b098ea70f1a5284f5a7d` | 是 | 上页路径续文完整；S25 表 S24 全部 12 行清楚，负向例外与 breach 增加均保留；S26 起始公式未越界。 |
| 21 | `190f312213889e384898a41e6f8f542afcb6026e70c892f9da47d45a090ff24b` | 是 | 表 S25、S26 两组 full-prefix/rolling 对照完整；旧 breach-count NA 保留；Bartlett 带宽与标准误公式清楚。 |
| 22 | `e4eec0ea066deefb6816ebee62d3c6eda26faec7d3ab3a9a00906ffa21042dd3` | 是 | S27 表 S27 全部 24 个计划格可读，七个 FAIL 行、complete/required 与竖排表头完整；脚注无裁切。 |
| 23 | `e82236e8d43a6e2f44e5aa01d0088991820ca97351dd895545cb5b28634c409d` | 是 | 表 S28 全部七个失败格原因可读；S28 稳定性公式清楚；表 S29 前 13 个来源行及续页提示完整。 |
| 24 | `477afe8ca7fd199494dc7250341c05c65d64d3e81ead59b60f066624484cc6f5` | 是 | 表 S29 续页重复表头，FX daily NR 和 FX hourly OF 可读；表 S30 全部 W=52 条件比较及失败边界脚注明确。 |
| 25 | `97c10bd3785d7bf140c65832451461f7ab0c4625fc4bf034a37141b6fa246c64` | 是 | 表 S31 两条 TIPS-G11 FAIL 31/32 保留；表 S32 起始 26 行完整，列头、脚注、续页提示均在页内。 |
| 26 | `6367184c768e4afb20c4cf2acc80dffd99575d20c9100a53dfdbb4b0bb165b00` | 是 | 表 S32 剩余 26 行重复列头，所有 F 行 32/32 可读；S29 与 S29.1 起始位置和目录页码 26 一致。 |
| 27 | `852844a590b29afc39938d00a4f60b587c4f67b801600cafb97281869378bf88` | 是 | 表 S33 两条长历史 full-regression 汇总 NA 与 missing 1/1 保留；M1/M3 hold、M2 fails 和无子集替代的说明可读。 |
| 28 | `99e3ed7837125063efe730d976f853aea621a8ddfbfe3985867786127b50c4ad` | 是 | 图 S1 四个面板、点型图例、坐标和图注清楚；两个长历史全回归面板明确显示 old/expanded menu NA (12/13)，无被掩盖的缺失项。 |
| 29 | `eac7fe07157584776c1376be7e676f02d7415404fd97b3aeeaa4a6f7b5167c36` | 是 | 表 S34 密集长表首段完整，所有列处于页内；两条 TIPS-G11 31/32 FAILED 与 NA 可辨；页末行和页码无重叠。 |
| 30 | `169cfa3813ce985e90aa16524debacaa91f2549108e44650e9a2b9003ca42fe6` | 是 | 表 S34 余行续页重复列头，长表终线完整；各 source/arm/history/predictor 与状态列对齐。 |
| 31 | `2260deff4ad51658b21c5ff91aa91772836ec84bb5975e8bb30b8edad8976813` | 是 | S30 CFTC 来源及信息日期说明清楚；17 个合约来源的代码、名称、open interest 与 877 weeks 完整；长名称自然换行。 |
| 32 | `04c12cce95138ea1ce591e06b96cd6e505f1a3af185d7ee704ed28931a8e42e7` | 是 | S30 续文包含十九个成熟分数、六期延迟及两项 schema 澄清，原失败尝试仍被说明；大段留白无丢页征象。 |
| 33 | `9e7e7d44c83aaeaaf02800a8b56d33f439be12c3406dfaad1e1ad54a9a34ec43` | 是 | S31 完整 MCS 规则和 98/98、60 unavailable 说明清楚；表 S36–S38 的三块列头、粗体成员、NA 与上标类别可辨。 |
| 34 | `ce9ecfa107311b8cc7e1e27584cd8bf397b8ad7a873272e22fa69450d2492711` | 是 | 表 S39 FX early 2015 四行完整；NA、破折号及 exact-loss 类别上标清楚；页内留白属于单组表排布。 |
| 35 | `6954e6061a4698ebaf646e73296b5b232267b7cd209aee305b1e6ba56b5ab741` | 是 | 表 S40–S42 Treasury bills 三个方法块均有完整表头和四行；NA 及粗体成员可辨，无列越界。 |
| 36 | `0866ca1e18541ee08d7e4ed61adaecbe16cfa8d22f02b522e869c0792e6584ff` | 是 | 表 S43 48 个 Other NYFed panel 行完整；较小字体、竖排表头和上标在整页图像中仍可辨，末列 Median combination 的 NA 保留。 |
| 37 | `4c343315bf7877fc556c1d0387c58c0fb35eb798a014e4f851993bdc9fa1a3e8` | 是 | 表 S44 四个 same-record daily FX 行与 full-grid n=501 标签清楚；所有表线和成员粗体完整。 |
| 38 | `44a917e6ad8f25239cfba3f002501fc272e781ef97b30e0f8a1ae776e485a1bc` | 是 | 表 S45 CFTC 全部 34 行（17 合约乘两历史）处于页内；上标与粗体可辨，未见数值列相撞或切边。 |
| 39 | `6543804db77ff44854bf717d2a9c0783fc1c0ae6889dda9e6d2ac6a5b93f32a0` | 是 | 完整方法图例 M01–M41 及类 H/C/B/R 的列对齐；S32 固定成本公式与参数网格清楚，正文未越界。 |
| 40 | `b746ce45e2ec7f0bb282b11de7c9ccdc3c8c7b100345acab194d314adaf84445` | 是 | S32 184,464 cost rows 和 18,522 primary grid rows 明确；表 S47 两个 panel 可读；S33、S34 与目录页码一致。 |
| 41 | `f15cd51f05ae72a02a37f239ae09cd89ac5510119e6c339b1b54fe005d6265bb` | 是 | 图 S2、S3 各自的图例、坐标、货币单位和完整图注清楚；两条折线与交叉性质未被图注掩盖。 |
| 42 | `bcc1a7f0ead9b3122bb805bb2c196f0384417cce35c508c1116b0e5e7f5c01c4` | 是 | S34 可用性边界完整；S35 表 S48 明确保留 42/48、100% required、Not supported 的通用排序反例；左删失 not testable 说明可读。 |
| 43 | `1a98d52b65e2845b383d97fda73798e16b6ad66d54447085b8a4faee1ab9dacf` | 是 | S36 保留的范围限制完整，含未独立 dealer 验证、经验因果未解、失败及 unavailable 状态；正文与页脚间距正常。 |
| 44 | `4d33116b5563fb3e0d8f60d7d8a60c43f05c1fdd6aee5efda739faf0793da7bb` | 是 | S36 额外检查说明清楚；S37 表 S49 全部 98/98 比较、90/98 matched-history included、60 unavailable 仍可读；无表列错位。 |
| 45 | `2b843faa66a66561e4499d1dd57d0e4c74b9f0940a86402fa2cbee731f582405` | 是 | S38 G1 的 Only 6 of 10、10^-6 再现门禁和原不可用值明确保留；G2 表 S50 Four-feature H=6 Median screen=Fail 与其余负结果可读。 |
| 46 | `087bb55fc0a8ef8d8041125efb6008a8d581f7fbee29a421069fd82869dbfb6a` | 是 | 图 S4 四个面板的 52/156 validation weeks 图例、所有系列/合约标签、纵轴和图注清楚；极端反例点未越框。 |
| 47 | `26cecbc440db48bceac50e76e25566fcfa65524721be4a12a79e9c794e0b7f34` | 是 | G3 协议段保留 8/60 adverse、worst +80.98%、historical fallback 32/regression 28 和 tail condition fails；表 S51 全部八行清楚；S39 说明 partial support 及无 registered full high-region cell。 |
| 48 | `cf3b50bcb945241d64aa8edc9df1ce47eb0e9a0294e1a5eaa370903785b77d40` | 是 | 表 S52 显示 P2 Full=Not testable、P2/P3 Four-feature=Not supported；表 S53 25 条反例（2+7+5+11）完整，三历史长数值行未截断；来源与执行校验边界清楚。 |
| 49 | `837ce3709d6a9ce76a141a4308d334379bb789c17477f2195eb970bf6a7e0920` | 是 | 独立 References 部分 [1]–[16] 完整可读；长 DOI 和题名自然换行，未见字体缺失或裁切。 |
| 50 | `1f2082edf35c2c878b393a6b575d22b772a31cb2f5fdf38e1eef67c8a2905537` | 是 | References [17]–[33] 全部可读且末条位于页内；[33] 可见 “Historical compressed. ; . Retrieved October 24, 2026.” 的空字段标点且未显示 URL，列为非阻断编辑问题。 |

本报告的通过范围仅覆盖实际 PDF 的视觉排版和可见边界保留；不代表新数值复现、独立金融验证或原 NJD 模板认证。
