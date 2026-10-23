# 第二轮最终改动清单（2026-10-23）

修改依据为《第二轮修改意见（导师版）》，继续使用 PR #3 的 `codex/supervisor-revision-20261023` 分支。执行顺序为 **E6 → E5 → W1 → W2 → W3 → W4 → W5 → C1**。本节记录第二轮的当前交付事实；下方第一轮记录完整保留，仅作为历史记录，不能用其中旧页数、旧词数或旧推断口径代表本轮。

## 1. 最终稿、范围与当前状态

- [最终论文 PDF](manuscript/supervisor-revision/main.pdf)：**正文连参考文献 14 页，附录 5 页，共 19 页**；附录从物理第 15 页开始，满足本轮 14/5 页上限。
- 摘要 **158 词**，结论 **185 词**。统计规则为展开数值宏后按空格分词，连字符词计一个；记录见 [第二轮文档核对](results/supervisor-20261023/round2/document-verification.json)。
- **E6、E5、W1–W5、C1 全部完成。** 编译、逐页检查和完整测试已形成记录；最终论文、结果与原始执行历史包均已发布到同一 PR 分支并核对。最后仅发布本次计时/回执并对齐本地引用。
- 保留两个原 primary、所有原始正负结果和原 72 项 Holm 归档；新增结果明确标为 post-result exploratory。没有增加 E5 指定 panel 之外的新数据、新模型或新命题，也没有启动 Claude/Cloud 或跨模型复审。

## 2. E6 与 E5：实际做了什么

**E6：λ→∞ 参照和菜单端点。** [Table 6 的 8 行数值表](results/supervisor-20261023/e6/table6.csv)加入普通经验分位数 I 和 QR33+ 严格破线次数；[正式排版表源](manuscript/supervisor-revision/generated/e3-table.tex)使用明确列名。Treasury 四格的 I 相对 F 损失依次为 −1.99%、+3.24%、+6.21%、+2.35%；QR33+ 为 −3.24%、+3.43%、+4.34%、−0.19%。主格 QR33+、F、原 QR 的破线次数为 32、28、54。正文写明 Treasury 四格中三格选到扩展菜单上端点 λ=10。

第 4 节说明未惩罚截距的 λ→∞ 极限和两种秩的区别：I 使用 `ceil(.95W)`，F 使用 `ceil(.95(W+1))`；当 `.95W` 为整数时，截距最优解可能是以 I/F 为端点的区间。选做的 λ 路径图也已完成，放在附录 A.7；[路径 CSV](results/supervisor-20261023/e6/lambda-path.csv)与[分阶段 I 参照](results/supervisor-20261023/e6/lambda-path-I.csv)保留验证和评估两条曲线，评估曲线不用于重新选参。[E6 数值读回记录](results/supervisor-20261023/e6/numeric-readback.json)说明了核对范围。

**E5：先提交预测，再跑全部 48 格。** 使用 v3 已下载并冻结的 12 条合格序列，移植既有读取/运行入口，沿用原来源记录、哈希、对齐、切分、平局规则和核心模型。没有重新下载或替换序列。扩展 QR33 菜单为 `{.001,.01,.1,1,10}`，另算 I；原 F、QR33、QR4+ 只读取和核对，不重拟合。

- [预测文件](protocol/supervisor-20261023/e5-panel-prediction.md)的独立提交为 `8baa2f5b44327b3ba295927bd3db954f3475d35d`，提交时间 **2026-10-23 18:27:50 UTC（温哥华 11:27:50）**。
- E5 运行开始于 **18:30:55.671193 UTC**，首个新拟合开始于 **18:30:55.774398 UTC**；预测提交在前。运行于 **18:31:33.256996 UTC** 完成，实际计算耗时 **37.586 秒**。[运行回执](results/supervisor-20261023/e5/run-receipt.json)保留精确时间、文件身份和资源记录。
- **48/48 格均首次完成**，没有失败后重试、删格或更换菜单；[完整 48 行汇总表](results/supervisor-20261023/e5/summary.csv)包含 F、原 QR33、QR4+、QR33+、I、选中 λ 和破线次数。

| 冻结预测 | 实际成功数 | 事先阈值 | 结论 |
|---|---:|---:|---|
| P1：原来输给 F 的 45 格中，QR33+ 优于原 QR33 | **30/45** | 至少 40 格 | **不成立** |
| P2：QR33+ 相对 F 落在含端点的 ±10% 内 | **24/48** | 至少 36 格 | **不成立** |
| P3：选择 λ≥1 | **33/48** | 至少 25 格 | **成立** |

[固定预测判定 JSON](results/supervisor-20261023/e5/prediction-assessment.json)原样保留失败阈值。原 QR33 的相对 F 损失中位数为 +92.6%，QR33+ 为 +9.2%；扩展后仍有 **34/48** 格输给 F。正文第 6.3 节和新 panel 图据此写成“收缩缓解但没有消除劣势”，没有写成 13 条序列一致，也没有把失败结果推成预测变量完全没有信息。正文同时说明设计发生在看过原 QR33/QR4+ 之后，序列共享报告体系及重叠交易商头寸，不能当作独立复制或做独立样本合并检验。[E5 完整说明](results/supervisor-20261023/e5/README.md)列出来源与复现边界。

## 3. W1–W5：逐项落实位置

| 编号 | 本轮改动与位置 | 未做事项及原因 |
|---|---|---|
| W1 | 重写摘要、引言贡献段、第 2 节结尾和结论，围绕 Treasury 过窄菜单、FX 同菜单增益与 E5 剩余损失展开；将库存政策限定句移到第 9 节。完整三段见[改写全文](manuscript/supervisor-revision/round2-rewritten-passages.md)。 | 没有采用“13 条周度序列结论一致”的候选措辞，因为 E5 的 P1/P2 不成立。 |
| W2 | 新增第 8 节 Implications for position monitoring，写历史基准、显式收缩/基准候选、U/V 与破线次数联合报告三条。明确 I 和有限大 λ 未必等于 F，建议显式加入 I 和精确 F；验证损失保护不构成评估期保证。 | 无删减。 |
| W3 | 第 5 节、6.2 和 Tables 3/4 统一两个原 primary 的原始 HAC p 值；Treasury 显示 0.008，两个 primary 的 Bonferroni 敏感性为 0.015；剩余 71 个 matched 对比使用 Holm。明确该报告口径重排发生在结果之后，旧 72 项调整原样保留。来源见 [W3 汇总](results/supervisor-20261023/w3/summary.json)。 | 没有把重新分组宣称为新的预注册或全研究过程的确认性错误控制。 |
| W4 | 第 7 节 AR 段和 Table 9 改以 F/S 为主，并加上 AR 对 QR33+ 的 3/4 Treasury 格及主格 −23.0% 对比；6.2 加前向引用；第 9 节 Coverage and specification 同步 E3/E5；6.1 写明 FX H24/W720 的 λ=0.01 和 +31.5% 仍不变。来源见 [AR 对比汇总](results/supervisor-20261023/w4/ar-comparison.json)。 | 无新增拟合；只核对已有聚合结果。 |
| W5 | 删除或改写指定审计腔句子；数据文件同一性边界移到数据节；直接写 H6 年度方向一致和 H24 改进集中于 2017 年尾段；p 值解释集中在第 5 节。记号表移至附录 C.1；Figure 1/2 标签分开；Figure 2 图注明确 Table 7；Table 6 列名加入 λ、I 和破线；Table 1 前三行按原来源再核对。核对记录见 [round2-literature-recheck.md](notes/supervisor-20261023/round2-literature-recheck.md)。 | van den Hoogen 直接 PDF 请求超时，核对范围明确限于机构索引中的正文段落与目录，没有声称新读完整学位论文。 |
| C1 | 最终 TeX 已编译成 19 页 PDF；19 页均逐页渲染检查；完整 574 项测试及 69 个原归档结果文件核对通过。更新本清单与交付链接。 | 无科学任务删减；执行历史 bundle 已验证并发布。网站上传产生额外分目录提交，详见末尾。 |

## 4. 实际分项用时

以下为 [round2/timing.json](results/supervisor-20261023/round2/timing.json)记录的分项墙钟时间，包含该项读写、执行和核对；不等同于模型纯计算时间。顺序和起止记录保留在原 JSON。

| 项目 | 预算 | 实际用时（秒，显示至毫秒） | 约合 | 状态 |
|---|---:|---:|---:|---|
| E6 | 90 分钟 | 693.349 | 11 分 33.349 秒 | COMPLETE |
| E5 | 210 分钟 | 469.323 | 7 分 49.323 秒 | COMPLETE |
| W1 | 90 分钟 | 186.348 | 3 分 6.348 秒 | COMPLETE |
| W2 | 30 分钟 | 27.807 | 27.807 秒 | COMPLETE |
| W3 | 30 分钟 | 245.558 | 4 分 5.558 秒 | COMPLETE |
| W4 | 30 分钟 | 156.033 | 2 分 36.033 秒 | COMPLETE |
| W5 | 60 分钟 | 364.797 | 6 分 4.797 秒 | COMPLETE |
| C1 | 60 分钟 | 2232.124 | 37 分 12.124 秒 | COMPLETE |

计时截止于交付核验点 **2026-10-23T19:28:19.338648+00:00**；此前总计 **4375.339 秒**。其后的最终元数据发布与本地引用对齐属于交付收尾，最终回复另报总墙钟时长。所有项目均低于预算，未触发 150% 停止规则。

## 5. 编译、检查与证据边界

[文档核对](results/supervisor-20261023/round2/document-verification.json)记录最终 PDF 的 14+5 页边界、158/185 词、36 个经验数值来源和保护文件范围。最终 PDF SHA-256 为 `f7369f0857b5d46cae55d25e5bb77baafff430aa415267ee153604195143a811`。[逐页检查记录](results/supervisor-20261023/round2/visual-review.json)绑定同一 PDF，记录全部物理第 1–19 页；Table 6、新 panel 图及两张标签修改图均已检查。

[完整测试记录](results/supervisor-20261023/round2/test-verification.json)为 **574 tests, OK**，用时 91.582 秒。原结果核对为 **69 个结果文件 ARCHIVE_VERIFIED**；该检查不声称重新计算原始金融准确率或产生独立金融样本。只读科学一致性检查没有发现需修改的重大科学表述问题；它与编译、测试、逐页图像检查的范围分别记录。

[远端逐项交付核对](results/supervisor-20261023/round2/delivery-verification.json)记录 E6 至 C1 每个执行快照与对应发布快照的整棵文件树完全一致。原执行链已存入 [Git 历史包](results/supervisor-20261023/round2/round2-execution-history.bundle)，可恢复真实的 E5 运行前提交；网站后续发布的提交时间不能代替该运行前证据。

## 6. 导师要求的五项交付入口

1. **新 PDF 与正文/附录页数：**[main.pdf](manuscript/supervisor-revision/main.pdf)，正文连参考文献 **14 页**、附录 **5 页**；[页数和词数核对](results/supervisor-20261023/round2/document-verification.json)。
2. **E5 提交时间、运行时间、48 格与预测判定：**[运行前预测文件](protocol/supervisor-20261023/e5-panel-prediction.md)、[提交/运行回执](results/supervisor-20261023/e5/run-receipt.json)、[48 行汇总表](results/supervisor-20261023/e5/summary.csv)、[P1–P3 判定](results/supervisor-20261023/e5/prediction-assessment.json)。
3. **新的 Table 6：**[8 行完整 CSV](results/supervisor-20261023/e6/table6.csv)和[正式排版表源](manuscript/supervisor-revision/generated/e3-table.tex)；印刷表在 PDF 物理第 9 页。
4. **改写后的摘要、贡献段和结论全文：**[round2-rewritten-passages.md](manuscript/supervisor-revision/round2-rewritten-passages.md)，已展开数值与正式交叉引用。
5. **逐项改动清单：**[本文件 REVISION_SUPERVISOR_20261023.md](REVISION_SUPERVISOR_20261023.md)。

---

# 第一轮历史记录（原文完整保留；以下不是本轮交付状态）

# 导师意见落实与改动清单

修改依据：用户提供的《论文修改意见（导师版）》，对象为公开 main `65feeee`。本轮在独立目录、独立分支完成；另一对话正在使用的 `revision-v4-jof` 目录保持只读。作者按用户最新答复填写 **Byron**，其他署名信息留空。

## 交付与篇幅

- [新论文 PDF](manuscript/supervisor-revision/main.pdf)：**正文连参考文献 13 页，附录 4 页，共 17 页**；Appendix C 独占第 17 页。
- [LaTeX 入口](manuscript/supervisor-revision/main.tex)及相邻分节源文件可编辑。该 PDF 是内置 Tectonic 0.17.0 编译的实际输出，producer 为 xdvipdfmx；没有将另行绘制的稿件冒充 TeX 输出。
- 摘要 **145 词**；结论 **104 词**。以去除 TeX 控制命令后的空格分词，连字符词计一个。
- 新版 **Table 3 / Table 4** 保留原六方法的 48 格，增加相对自身冻结 F、破线率与相应 Holm DM 列。新 **Figure 2** 是收益拆解瀑布图；**Table 6** 为 E3，**Table 7** 为每步配对检验。
- [可执行核对与统计规则](verify_supervisor_document.py)、[核对记录](results/supervisor-20261023/document-verification.json)、[排版与复现指南](manuscript/supervisor-revision/README.md)。

## 否定句统计

统计范围均为叙述段落：旧第 1–11 节与新第 1–9 节，包含新 E3 叙述；排除摘要、表格、公式、图注、标题、参考文献与附录。词项按大小写不敏感的完整单词匹配。

| 统一规则 | 改前 | 改后 |
|---|---:|---:|
| 严格按字面句点切分，not/no/neither/nor/cannot | 83/449 = **18.49%** | 10/249 = **4.02%** |
| 先保护小数点与 et al./e.g. 缩写，再按句点切分，同一组词 | 83/353 = **23.51%** | 10/225 = **4.44%** |
| 第二种规则，再计 without / rather than | 108/353 = **30.59%** | 12/225 = **5.33%** |

原意见中的“约 25%”与小数/缩写保护后的口径接近。这里保留两套可复核结果，没有通过混用分母来制造下降。新正文两种核心统计均低于 12%。

## 改写了什么

| 新章节 | 实际改动 |
|---|---|
| 1 Introduction | 经济动机、研究问题、数据设计、主发现、三条经验贡献和范围，依次展开；移走原执行日志式段落。 |
| 2 Related literature | 按库存/资产负债表、金融路径极值/缓冲、分位预测/评分三条线组织。新增五列近邻研究表；前三篇评价方式按原文核对，保留 van den Hoogen 数值保密事实。FX 仅称同一来源家族，未声称输入文件相同。 |
| 3 Data and target | 日期取代零起索引。定义 B/P/G 和成熟标签时钟；新增人造路径示意图与统一记号表。恢复正式数据来源引文。 |
| 4 Forecasting methods | 正式 LaTeX 排版；保留三种历史构造、训练变换、QR 与组平衡 KNN 距离。峰值参数化的 shifted ridge 推导移到 A.5；AR 移到稳健性。 |
| 5 Evaluation design | 明确两个原主比较、未见留出集的边界、后加分析身份；加入 HAC、HLN、固定 Holm 家族、非重叠网格覆盖检验及初始化约定。 |
| 6 Results | 分为 FX、Treasury、顺序拆解。保留短历史 QR 恶化、Treasury 原主比较恶化、稀疏网格反转及更多破线；同时加入 E3 解释。 |
| 7 Robustness | AR、秩、固定线性权重、预测期顺序各一段，配汇总表；U/V 图名改正，使用 Treasury 和 Scaled KNN 的统一标签。Murphy 图置附录。 |
| 8 Discussion and limitations | 集中四项：历史检查与推断、数据口径/信息时钟、覆盖和规格、实际决策价值。必要的摘要与评估身份提示保留。 |
| 9 Conclusion | 104 词，三条经验贡献与摘要、引言和文献综述保持一致。 |
| A/B/C | A 保留并压缩原有限几何证明及反例，加入被移入的 ridge 推导和已有 Murphy 诊断；B 仅原 Table B1 与一段说明；C 一页复现与补充材料指引。 |

正文采用 2–3 位有效数字，表格统一三位小数；原始 CSV 保持完整精度。原 Table B1 的微小 tau90 正差舍入成 +0.000，表注明确其原始符号，避免隐藏反向结果。符号分开使用 κ、s、ell/u、Traw、Rabs/Rsigned、omega、Cfloor 与原目标 P。

## E1、E2、E4 核查及实质更正

E1 核对 90 个原逐点报告单元、74 个检验及固定 72 项 matched 家族。主带宽下有 19 项 Holm p<.05，双倍带宽为 18 项。FX 跨窗口主比较在该家族之外，单独标明原始 p。Treasury 主比较的 **原始 p=.007611，Holm p=.319678**；没有称其为经多重调整后显著。

E2 发现旧代码把 full-n Kupiec 项与条件于首个 hit 的 n−1 独立性项相加。新条件覆盖 LR 使用同一条件似然；full-n Kupiec 仍单列，旧文件原样保留。三项条件 CC p 值分别为 FX QR **.636152**、Treasury QR **.013593**、Treasury F **.261900**。这只更正检验约定，不改任何预测、损失或破线。

E4 对所有实数阈值的有限断点核查，两个原主比较均交叉。FX 检查 16,146 个断点，Treasury 检查 640 个；积分重现原配对 pinball 差。本文图区分固定 U/V 线性权重与同一分位水平下的一致评分，不推断总体支配。

详细方法、来源、实际阅读范围、独立标量核算及文件身份见 [推断审计](notes/supervisor-20261023/inference-audit.md) 和 [文献审计](notes/supervisor-20261023/literature-audit.md)。HLN 原文正文访问受阻；元数据已核，修正公式以官方实现文档与独立 Student 积分另行核对，未冒充全文重读。Hansch 仅元数据/摘要核对成功，本次动机使用已读相关原始正文的 Ho–Stoll 与 Lyons。

## E3 新实验与贡献二

完整设计在拟合前写入 [e3-design.md](results/supervisor-20261023/e3-design.md)。新 33 特征 QR 使用与精简模型相同的 `{.001,.01,.1,1,10}` 菜单，保留原切分、成熟标签、重估频率、较大参数优先的完全平局规则、数值容差及所有候选必须完成的资格条件。已有四特征运行的 40 个候选均完整且均值无完全平局；较宽松的旧代码规则因此没有改变实际选参。没有从失败候选中挑选有利结果。

| Treasury | 原始 33 特征相对 F | 扩展菜单 33 特征相对 F | 同菜单 33 相对四特征 | 新 λ |
|---|---:|---:|---:|---:|
| H6/W52 | +83.354% | −3.244% | −0.672% | 10 |
| H6/W260 | +50.786% | +3.434% | +1.242% | 1 |
| H24/W52 | +227.411% | +4.340% | −1.524% | 10 |
| H24/W260 | +109.843% | −0.193% | −0.303% | 10 |

**据此改写贡献二：短周度历史的原明显失败主要随过窄 ridge 菜单出现；共同菜单下的结果不支持把原损失直接归因于额外特征。** Treasury H6/W260 的同菜单差异 p=.685，这也不是等价性证明。FX 四格的选参和每个已存报告均未改变；长历史 FX 的同菜单四→33 特征损失变化为 −10.947%，其 E3 28 项 Holm p=3.436e−6。

瀑布图按“更新→历史→四特征→同菜单全特征→恢复原菜单”顺序显示，两个终点仍是原主比较。最后 Treasury 菜单步骤与增加预测变量的步骤分开；使用初始损失作共同分母的百分点可加，上一步百分比需连乘。全部步骤都保留配对 DM/HLN，E3 多重比较单列，未并入原 72 项。

8/8 单元、40/40 候选全部完成，无重试，无数值/资源失败；2476 次拟合通过原接受条件。拟合合计约 96 秒，属于实际实验时间而不是研究工时。[完整 E3 输出与限制](results/supervisor-20261023/e3/README.md) 保留所有原始和新增正负结果。

## 从新打印稿移出、仍保留在哪里

| 材料 | 原样保留位置 |
|---|---|
| 旧 56 项 e-value 大表及全部明细 | `results/revision-20261022/coverage-evalues/`；旧稿 Appendix D 亦保留 |
| 完整损失权重前沿 E1/E2 | `results/revision-20261022/preference-robustness/`；旧稿 Appendix E 保留 |
| 机器资源、ADMM 检查、执行冻结与历史经过 | 原 `protocol/`、`results/revision-20261022/`、原稿 Appendix C，以及新 E3 回执 |
| 原 24 页稿、15 张表、21 个公式块与图 | `manuscript/working-paper/` 全部未改 |
| 完整早期检索、月份、块重采样、秩和预测期诊断 | `results/`、`results/revision-20261021/` 及 `results/revision-20261022/` 对应子目录 |
| 参考文献后的 consulted-body 阅读日志 | 原 evidence-map 及本轮两份来源审计；新参考文献只保留正式书目 |

## 验证与没有做的事项

原始 443 个已跟踪文件中只修改根 README 的入口说明；其他原文件均保留，69 个核心结果的原归档校验通过。新文件采用独立版本目录。源码、聚合数值、页数、词数、引用对应和 PDF 身份可由核对脚本检查；17 页作了实际图片检查，改动图页再次检查。没有调用 Claude 或跨模型审查。

没有增加数据源、QRF/FHS/EVT 实验、Lévy 命题或第二轮扩展。没有改原主比较或旧结果，也没有把描述性 p 值当作未受选择影响的确认性推断。没有投稿、注册账户、填写作者未授权的信息或合并 main。已有脚本/私有数值上下文是新增核算的复现依赖；公开克隆可重建稿件和检查聚合证据，不能凭空获得私有逐点数组。该边界在新文档指南明确列出。

---

## 待用户决定

**目前没有需要用户作出的科学分析决定。** 需用户知悉的交付差异是提交历史：GitHub 连接器返回 403，本地 CLI 未认证，因此网站上传增加了文件或目录级提交，远端历史未满足“每项恰好一次提交”的形式。每项内容均已与对应本地执行快照核对一致；原始按序提交链及拟合前的 E5 预测提交，已完整保存在 [round2-execution-history.bundle](results/supervisor-20261023/round2/round2-execution-history.bundle) 中。C1 用时已登记至最终内容交付核验点。最保守做法是保留网站发布历史和原执行历史包；若以后要求整理提交历史，需要用户另行决定，本轮不改写远端历史或合并 main。
