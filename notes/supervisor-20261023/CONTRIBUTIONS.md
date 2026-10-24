# 本文的三项贡献：发现、证据与边界

定位：这是采用成熟方法的实证比较与模型验证论文。主线是：**预测交易商净头寸的采样峰值时，简单历史规则很难打败；FX 的收益取决于参照和时期，周度回归的损失经收缩后仍未稳定消除，较低分数也可能伴随更多破线。** 文献差别依据 Table 1 的逐格原文核对和既有结果，不声称完成文献穷尽检索。

## 1. 简单历史规则是峰值预测的强基准，FX 收益取决于参照和时期

**中文一句话：** 预测双侧绝对持仓峰值时，FX 回归在原期和更早期分别比匹配历史规则降损 14.8% 和 16.6%，但更早期比短历史滚动规则增损 3.2%，原来相对该滚动规则的收益没有复现。

**English:** Historical rules are a hard benchmark for sampled position peaks: FX regression lowers matched loss by 14.8% in the original period and 16.6% in the earlier period, but its earlier loss rises 3.2% against the short-history rolling rule, reversing the original comparison's gain.

**证据与文献增量：** 目标是 \(P_{t,H}=\max_{0\le h\le H}|N_{t+h}|\)，包含当前持仓；比较匹配已完成标签、历史长度和更新安排。FX 的 H6/W2880 回归相对冻结的历史 headroom 规则降损 **14.767%**，对应正文的 **14.8%**（§3–4、Figure 1、Table 3；[原配对表][paired]）。更早的 **2015 年 FX** 比较中，同一原三点菜单回归相对 frozen F/W2880/d24 降损 **16.6%**，相对主比较的 rolling F/W720/d1 则增损 **3.2%**：原主比较的收益方向没有复现（Table 10；[原结构表][r6primary]、[固定报告与两项 HAC 比较][r6hac]）。两项比较使用相同的回归报告，不是保守 one-standard-error 规则的报告。

[Wisniewski et al. (2020)][wisniewski] 已研究同一 FX 数据家族的下一小时有符号端点区间；本研究增加多记录峰值目标及同目标、同历史、同更新比较。MaxVaR 已研究期内组合价值最大损失；van den Hoogen (2017) 已有单侧累计支付缺口峰值；Petrunia et al. (2019) 先取参与者间每日结算借方余额最大值。本文的差别是双侧绝对持仓峰值及其具体预测证据，不是“首次研究金融峰值”（§2、Table 1；[原文核对记录][literature]）。

**比较口径：** 上述 **14.767%** 属于 matched frozen F2880 比较；预先声明的主比较参照 rolling F720，原期降损 **12.7%**。这里的滚动规则是指定参照，不能写成评估后从所有简单模型中选出的“最优规则”。峰值只覆盖采样网格，条件方法本身不是新算法；程序比较也不识别单个预测变量的因果作用。

## 2. 周度回归主比较输给历史 headroom，扩大菜单和保守选参仍留下大额损失

**中文一句话：** 周度 Treasury 主比较增损 50.8%，扩大岭惩罚菜单虽减小损失，12 条附加序列仍有 34/48 格败给历史 headroom，而另一个涵盖 13 条周度序列、26 格的更早期测试中，保守选参仍留下大额损失。

**English:** Weekly regression loses 50.8% in the Treasury main comparison, and wider penalties leave 34 of 48 cells across 12 further series behind historical headroom, while conservative selection still permits large losses in the separate earlier test of 26 cells across 13 weekly series.

**证据与文献增量：** 原 Treasury H6/W260 回归相对匹配历史规则增损 **50.786%**，对应正文的 **50.8%**；扩大菜单后为 **3.4%**。**12 条追加序列、48 格**的中位超额由 **92.6% 降至 9.2%**，仍有 **34/48 格**败给 F。三条冻结预测的判定全部保留：**第一条 30/45<40，失败；第二条 24/48<36，失败；第三条 33/48≥25，成立**（§6.3、Table 6、Figures 2–3；[菜单比较表][e3]、[附加面板全表][e5]、[冻结预测判定][predictions]）。相对于 Wisniewski et al. (2020) 的 FX 端点区间预测，增量是在周度峰值任务中量化菜单敏感性及未获支持的预测，不是新正则化理论。

更早期的保守选参测试包含**原 Treasury-bill 序列 + 12 条追加序列，共 13 条周度序列、26 格**；每格有 **52 个验证 origins 和 52 个评估 origins**。保守 one-standard-error 规则在 **17/26 格**选择普通经验分位数 I，最差损失仍为 **+181.4%**，出现在 **Treasury-bill H24/W52**；I 自身的最差超额也为 **+36.5%**。保护标准并非只被最差一格打破：保守规则的中位数 **+5.374%** 也超过 **+5%** 门槛，且 **5/26 格**超过 **+25%**。**三项预设成功标准均未达到**；该规则是成熟 one-standard-error 思想对配对预测损失的 HAC 适配（§7、[保守选参设计][r6design]、[完整结果][r6summary]、[固定判定][r6assessment]）。

更早期 Treasury H6/W52 短窗口版本增损 **144.3%**，延续原比较的恶化方向。它不是原 W260 主比较的精确复现，也不替换原主比较（Table 10；[原结构表][r6primary]）。更早期 FX 的两种参照比较集中列在第一项贡献中。

**实务含义与范围：** 这类短周度样本应先采用 corrected-rank 历史 headroom，并用它检验回归和选参程序。这里的发现不是“所有条件方法都输”：部分 expanded-menu 回归格胜出，AR residual replay 也在部分 Treasury 比较中降损；损失、破线与稳定保护是不同判断。I 是截距分位数参照，有限大 λ 或 I 都未必等于 corrected-rank F；本研究不提供非劣性保证，也未建立从历史规则切换到条件模型的充分阈值（§4、§6.3、§7–8）。失败不能推出“特征没有信息”，也不能唯一归因于 52 点验证噪声。H24 标签重叠，52 个 origins 和 26 个周度格都不能当成独立观测或复制；菜单在看过旧结果后扩展，追加面板共享报告体系及交易商，不能合并作独立样本检验。

## 3. 较低 pinball 损失不等于较少破线

**中文一句话：** 较低的 0.95 pinball 损失可以伴随更多破线，FX 主比较为 376 对 332、匹配比较为 376 对 360，模型评估因此须同时报告误差金额、破线次数和评分敏感性。

**English:** Lower 0.95 pinball loss can accompany more breaches, with 376 versus 332 in the FX main comparison and 376 versus 360 in the matched comparison, so forecast assessment should report error amounts, breach counts and scoring sensitivity together.

**证据与文献增量：** FX H6 主比较降损 **12.7%**，破线却由 **332 增至 376**；匹配历史规则的 **14.8%** 降损对应破线由 **360 增至 376**。24-step 比较的 **1.83%** 降损在固定报告的欠预测/过预测权重比超过 **20.6** 后反转；两个主比较的固定 \(\tau=.95\) Murphy 曲线均交叉（§7、Table 8、Figure 4、Appendix A.6/Figure 5；[配对表][paired]、[固定报告偏好结果][preference]、[Murphy 核对表][murphy]）。Gneiting (2011) 与 Ehm et al. (2016) 已给出一致评分和 Murphy 表示；本文把这些成熟工具与峰值预测的破线证据连接，发现分数优势和破线优势在本案中分离。

**口径：** 改变 \(\omega\) 的 \(J_\omega=\omega U+V\) 衡量固定报告的偏好敏感性，通常也改变 check-loss 对应的分位数；它与固定 \(\tau\) 的 Murphy 分析须区分。经验曲线交叉只排除本样本中的全一致评分优势，不构成总体支配检验；破线也不是已观测的保证金、融资损失或经济收益。

## 审稿人可能的质疑与回答

1. **“QR、KNN 和评分都是旧方法，创新在哪里？”** 增量是目标、比较控制和上述三项带数字的发现；算法、优化器和评分理论均明确归于既有文献。定位：§2/Table 1、§4、§6.3、§7；不以“新算法”答辩。
2. **“两个数据来源能证明外部有效吗？”** 不能。一个来源是单个 FX 做市商的客户流记录，另一个是 Treasury 交易商聚合；追加面板仍属同一 NY Fed 报告体系。定位：§3/Table 2、§6.3/Figure 3、§9。
3. **“FX 评估期是否此前看过？”** 原评估期在条件方法设计前已经看过。更早的 2015 年 origins 在本项目的有界仓库核对中未发现既往 evaluation 角色，且所有目标在原验证期前完成；原始历史已经被读取和训练使用，规则也在原结果之后设计，因此不是完全未见、前瞻或外部验证，仓库外的使用无法由该核对排除。更早期回归对 matched frozen F 降损，却对原 rolling F 增损 **+3.2%**；原主比较的收益方向没有复现。相应两项 HAC p 值是结果后的探索性比较。定位：§5、§7/Table 10、§9；[保守选参设计][r6design]、[两项比较及范围][r6hac]。
4. **“看到失败才扩菜单，附加面板算原始预注册吗？”** 不算。菜单扩展是结果后探索；附加面板是在看过原回归和 four-predictor regression 后设计、仅在 expanded-menu regression 运行前提交预测的局部冻结，前两项预测失败照报。定位：§6.3、§9、Appendix C 及[预测文件][protocol]（提交 `8baa2f5`）。

## 不是创新的部分

QR/KNN、岭惩罚与 ADMM、pinball/HAC/DM/Murphy 方法不是新发明；金融峰值风险对象和条件 FX 持仓预测已有明确前例。本文没有建立新的条件覆盖保证，也没有验证经济价值、实际库存政策收益或融资成本节约。贡献是三项已有证据支持的发现：**历史规则很难打败，回归相对历史规则的收益随来源、参照和时期变化；更强收缩减轻但未稳定消除周度损失；较低分数与较少破线会分离。**

[paired]: ../../results/revision-20261022/paired-comparisons.csv
[wisniewski]: https://proceedings.mlr.press/v128/wisniewski20a.html
[literature]: contributions-table1-audit.md
[e3]: ../../results/supervisor-20261023/e3/summary.csv
[e5]: ../../results/supervisor-20261023/e5/summary.csv
[predictions]: ../../results/supervisor-20261023/e5/prediction-assessment.json
[preference]: ../../results/revision-20261022/preference-robustness/results.json
[murphy]: ../../results/supervisor-20261023/inference/murphy-verified.csv
[protocol]: ../../protocol/supervisor-20261023/e5-panel-prediction.md
[r6design]: ../../protocol/supervisor-20261023/r6-design.md
[r6summary]: ../../results/supervisor-20261023/r6/summary.csv
[r6assessment]: ../../results/supervisor-20261023/r6/assessment.json
[r6primary]: ../../results/supervisor-20261023/r6/primary-replication.csv
[r6hac]: ../../results/supervisor-20261023/r6-writing-hac-20261023/results.json

## 待用户决定

1. **标题备选，待用户决定；正式标题未改。**

   - *Forecasting Dealer Position Peaks: Historical Rules as a Hard Benchmark*
   - *Historical Benchmarks for Dealer Position Peaks: Conditional Gains and Breach Tradeoffs*

2. **图内旧标签与本轮“只改写法、不改图”的冲突，待用户决定。** 原图含 `33+`、`Four+` 等内部标签；本轮保留图的原字节，正文、表头和图注采用 descriptive names，Appendix C 表格给出旧标签映射。图内文字的统一须留待用户另行授权改图。
