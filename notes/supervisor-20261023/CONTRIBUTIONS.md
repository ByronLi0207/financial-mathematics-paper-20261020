# 本文的三项贡献：发现、证据与边界

定位：这是采用成熟方法的实证比较与模型验证论文。下面把“比较了什么”和“发现了什么”分开；文献差别依据本轮 Table 1 的逐格原文核对和既有归档数字，不声称完成文献穷尽检索。

## 1. 在同一持有期峰值目标上识别条件预测的增益

**中文一句话：** 将预测对象统一为包含当前持仓的双侧绝对采样峰值，并匹配完成标签、历史长度和更新安排后，条件模型的增益随数据与设定而异，不能由端点预测的成功直接推出。

**English:** On a common sampled absolute-position-peak target, comparisons with matched completed-label histories and refit schedules show that conditional gains depend on the data and specification.

**证据与文献增量：** 目标是 \(P_{t,H}=\max_{0\le h\le H}|N_{t+h}|\)，不是 \(N_{t+H}\) 的区间；FX 的 H6/W2880 匹配历史比较相对 frozen F 降损 **14.767%**，原 Treasury H6/W260 则增损 **50.786%**（§3–4、Figure 1、Tables 3–4；[原配对表][paired]）。[Wisniewski et al. (2020)][wisniewski] 已研究同一 FX 数据家族的下一小时有符号端点区间；本研究增加多记录峰值目标及同目标、同历史、同更新比较。MaxVaR 已研究期内组合价值最大损失；van den Hoogen (2017) 已有单侧累计支付缺口峰值；Petrunia et al. (2019) 先取参与者间每日结算借方余额最大值。本文的差别是双侧绝对持仓峰值及其具体预测比较，不是“首次研究金融峰值”（§2、Table 1；[原文核对记录][literature]）。

**边界：** 峰值只覆盖采样网格，不是连续路径极值；条件方法本身不是新算法。上述 **14.767%** 是匹配 frozen F2880 的比较，须与另一个、预先声明但参照为 rolling F720 的 **12.7% primary** 区分；也不能据此声称某一个预测变量具有因果效果。

## 2. 识别收缩菜单与短样本选参的保护边界

**中文一句话：** 扩大岭惩罚菜单缓解周度恶化，但在这次短周度验证和评估中，包括 one-SE 在内的选择规则仍未稳定守住历史基准。

**English:** Expanding the ridge menu mitigates weekly deterioration, but selection on the short weekly validation samples, including a paired-loss one-SE rule, does not reliably preserve the historical benchmark in the subsequent evaluation.

**证据与文献增量：** 原 Treasury primary 的超额损失由 **50.8% 降至 3.4%**；E5 的 **12 条追加序列、48 格**中，中位超额由 **92.6% 降至 9.2%**，仍有 **34/48 格**败给 F。冻结预测为 **P1：30/45<40，失败；P2：24/48<36，失败；P3：33/48≥25，成立**（§6.3、Table 6、Figures 2–3；[E3 表][e3]、[E5 全表][e5]、[冻结预测判定][predictions]）。“13 条周度序列”只指**原 Treasury-bill 序列 + 12 条追加序列**；E5 面板自身只有 12 条。相对于 Wisniewski et al. (2020) 的 FX 端点区间预测，本文进一步在周度峰值任务中量化同一条件程序的菜单敏感性，并保留冻结阈值下未获支持的预测；增量是这项可追溯的经验诊断及失败边界，不是新正则化理论。

在另行冻结的更早期比较中，每个周度格只有 **52 个验证 origins 和 52 个评估 origins**。主规则 R2 在 **17/26 格**选择普通经验分位数 I，最差损失仍为 **+181.4%**，出现在 **Treasury-bill H24/W52**；I 单独作为参照的最差值也为 **+36.5%**。S1 的最差统计量由该 T-bill 格达到，但不能说 S1 仅由一格导致失败：R2 中位数 **+5.374%** 也超过 **+5%** 门槛，且 **5/26 格**超过 **+25%**。S1、S2、S3 均未达到；one-SE 是成熟简约选择思想的配对差 HAC 适配，不是本文提出的新理论，也不提供对 corrected-rank F 的非劣性保证（§7、[R6 冻结设计][r6design]、[完整结果][r6summary]、[固定判定][r6assessment]）。

更早的 **2015 年 FX** 比较还说明参照不能混用：同一原三点菜单 QR 报告相对自身 frozen F/W2880/d24 降损 **16.6%**，相对原 primary 的 rolling F/W720/d1 则增损 **3.2%**，原 primary 的收益方向没有复现。Treasury H6/W52 结构类比增损 **144.3%**，保留了周度恶化方向；它不是原 W260 primary 的精确复现，也不替换原 primary（Table 10；[原结构表][r6primary]）。两项 FX HAC 读取核算仅是结果后的描述性比较，针对这条 QR 报告而非 R2；[固定轨迹与两项核算][r6hac]保留来源与检视边界。

**边界与实务含义：** 证据只说明当前数据、切分、特征和选择规则下没有稳定的基准保护，不能推出“特征没有信息”，也不能把失败唯一归因于 52 点验证噪声。H24 标签重叠，52 个 origins 不是 52 个独立观测；26 个周度格同样不是独立复制。I 是截距分位数参照，有限大 λ 或 I 都未必等于 corrected-rank F。对这类短样本，默认采用历史报告，仅在验证证据足够充分时才切换为条件模型；本研究没有建立何为充分的切换阈值。短窗口优先采用 corrected-rank F：早期 I 自身仍有最高 +36.5% 的超额损失；截距选项和较大惩罚本身不能保证评估保护（§4、§6.3、§8）。菜单在看过旧结果后扩展，12 条序列共享报告体系及交易商，不能当作独立复制或合并独立样本做检验。

## 3. 显示本案中“分数更低”与“风险更少”会分离

**中文一句话：** 在这些归档预测中，较低的 0.95 pinball 损失可以伴随更多破线，且分数偏好的改变会改写排序，因此模型结论须同时报告误差金额、破线次数和评分敏感性。

**English:** In these archived forecasts, lower 0.95 pinball loss can coexist with more breaches and score-dependent rankings, so forecast assessment must jointly report error amounts, breach occasions and scoring sensitivity.

**证据与文献增量：** FX H6 primary 降损 **12.7%**，破线却由 **332 增至 376**；H24 legacy 的 **1.83%** 降损在固定报告的欠预测/过预测权重比超过 **20.6** 后反转；两个 primary 的固定 \(\tau=.95\) Murphy 曲线均交叉（§7、Table 8、Figure 4、Appendix A.6/Figure 5；[配对表][paired]、[固定报告偏好归档][preference]、[Murphy 核对表][murphy]）。Gneiting (2011) 与 Ehm et al. (2016) 已给出一致评分和 Murphy 表示；本文的增量是将它们与本案破线证据连接，限定具体金融预测结论，而非提出新评分法。

**边界：** 改变 \(\omega\) 的 \(J_\omega=\omega U+V\) 是固定报告偏好敏感性，通常也改变 check-loss 所对应的分位数；它**不是**固定 \(\tau\) 的 Murphy 分析。经验曲线交叉只排除本样本中的全一致评分优势，不构成总体支配检验；破线也不是已观测的保证金、融资损失或经济收益。

## 审稿人可能的质疑与回答

1. **“QR、KNN 和评分都是旧方法，创新在哪里？”** 增量是目标、比较控制和上述三项带数字的发现；算法、优化器和评分理论均明确归于既有文献。定位：§2/Table 1、§4、§6.3、§7；不以“新算法”答辩。
2. **“两个数据来源能证明外部有效吗？”** 不能。一个来源是单个 FX 做市商的客户流记录，另一个是 Treasury 交易商聚合；追加面板仍属同一 NY Fed 报告体系。定位：§3/Table 2、§6.3/Figure 3、§9 “Measurement and information timing”。
3. **“FX 评估期是否此前看过？”** 原评估期此前看过，后来的执行冻结不能把它变成干净的未知留出集。更早的 2015 年 R6 origins 在有界仓库审计中未发现既往 evaluation 角色，且所有目标在原验证期前完成；但原始历史已经被读取和训练使用，新规则也受先前已检视结果影响，无法排除仓库外使用，因此不称完全未见、前瞻或外部验证。该更早期 QR 报告相对 matched frozen F 降损，不能掩盖它相对原 rolling F 的 +3.2%：原 FX primary 的收益方向未复现；相应两项 HAC p 值仍属结果后描述性读取核算。保留原 primary 与不利结果不消除检视限制。定位：§5、§7/Table 10、§9 “Inspection and inference”；[R6 设计][r6design]、[两项核算及边界][r6hac]。
4. **“看到失败才扩菜单，E5 算原始预注册吗？”** 不算。E3 是结果后探索；E5 是看过旧 QR33/QR4+ 后设计、仅在新 QR33+ 运行前提交预测的局部冻结，且 P1/P2 失败照报。定位：§6.3、§9、Appendix C 及[预测文件][protocol]（提交 `8baa2f5`）。

## 不是创新的部分

QR/KNN、岭惩罚与 ADMM、pinball/HAC/DM/Murphy 方法不是新发明；金融峰值风险对象和条件 FX 持仓预测已有明确前例；本文没有建立新的条件覆盖保证，也没有验证经济价值、实际库存政策收益或融资成本节约。最稳妥的贡献表述是：**在明确目标和比较条件下，发现收缩能缓解却不能普遍消除周度损失，并展示评分改善与破线风险的分离。**

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

仅提供标题备选，正式标题未改：

1. *Forecasting Sampled Position Peaks: Stronger Shrinkage and Persistent Benchmark Gaps*
2. *Conditional Position-Peak Forecasts: Shrinkage, Historical Rules and Breach Risk*
