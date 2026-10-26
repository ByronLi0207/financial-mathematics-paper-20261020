# R6：收缩选择与时间序列验证的原文依据

日期：2026-10-23。本文献记录在 R6 新评估前形成，供单独冻结的 `r6-design` 使用。仅核对指定的成熟方法、定义本任务的适配边界，并给出事前的 R2/R3 主要规则建议；未运行实验，未读取 R6 新评估结果，未下载新的金融原始数据，未修改任何既有结果或原 primary。

**建议预先固定 R2 为主要规则，R3 为敏感性比较。** 依据是本任务周度验证段只有 52 个连续 issue、较长目标为 H=24，清除边界会消耗部分历史记录，较早评分位置也可能来自不同状态；R2 在原验证段上完成一个固定、可解释的保守选择。此建议不是 R2 优于 R3 的经验发现，也不是有限样本保证。R2/R3 身份应在新评估前冻结，不能看结果后交换。

## 1. 原始来源、实际版本与阅读范围

### 1.1 Hastie、Tibshirani、Friedman：ESL 的 one-standard-error 规则

**书目：** Hastie, T., R. Tibshirani and J. Friedman (2009), *The Elements of Statistical Learning*, second edition. 本次实际读取作者网站提供的 **corrected 12th printing, January 2017**，不是只读书目或转引。

- [作者书站](https://hastie.su.domains/ElemStatLearn/main.html)及[官方下载页](https://hastie.su.domains/ElemStatLearn/download.html)。
- [作者指定的 PDF 下载入口](https://hastie.su.domains/ElemStatLearn/printings/ESLII_print12_toc.pdf.download.html)当前跳转至作者指定的 Google Drive 下载；实际取得的文件为 764 页，SHA-256 `8d098d65cf53925ba0fc13a52a2790d48a32433223cbd876d0a527cd1afe2e0f`。
- **直接读取位置：** printed p.61（physical p.80），§3.3.4；printed p.244（physical p.263），§7.10.1、Figure 7.9。p.244 已实际渲染查看。

原文把调参视为训练的一部分，保留测试集评估选定程序；当 CV 曲线在最低点附近平坦时，以一个标准误的容忍带偏向较简约模型。p.61 的示例标准误来自十折误差估计；p.244 同样讨论 CV 误差及其标准误。

**本任务可以引用的思想：** 估计的最低损失有噪声；在相近的估计准确率之间预先偏向简单程序，是成熟的保守选择思路。

**不能归给 ESL 的公式：** ESL 在这些段落没有规定本任务的“候选对最佳候选的配对 pinball 损失差 + Bartlett/Newey–West HAC 标准误”，也没有为重叠峰值、52 点验证段或选定后的非劣性提供保证。R2 应称为 **依赖验证损失上的 one-SE 思想适配**，不能称为 ESL 的规范实现、正式检验或新理论。

### 1.2 Bergmeir、Hyndman、Koo：普通 K 折时间序列 CV 的适用条件

**书目：** Bergmeir, C., R. J. Hyndman and B. Koo (2018), “A note on the validity of cross-validation for evaluating autoregressive time series prediction,” *Computational Statistics & Data Analysis* **120**, 70–83, DOI [10.1016/j.csda.2017.11.003](https://doi.org/10.1016/j.csda.2017.11.003)。

- [作者发布记录](https://robjhyndman.com/publications/cv-time-series/)确认正式书目信息。
- **实际读取正文：** [作者托管原稿](https://robjhyndman.com/papers/cv-wp.pdf)，封面标明 **23 July 2017, preprint submitted to Elsevier**，18 页。本记录使用该版本的本地页码，不冒称新读了 2018 年期刊排版全文。
- **关键位置：** §2、local pp.2–4 的嵌入自回归行及图 1；§3、local pp.4–7 的模型、A1–A3、Theorem 1 及假设违反的讨论。

该理论针对平稳、遍历的非线性 AR(p)，要求一致的非线性最小二乘估计；误差条件包括鞅差、固定条件方差、矩与连续性条件。独立同分布误差是充分情形之一，**不是原文唯一允许的误差结构**。相应预测误差论证使用平方损失。原文说明残差串行相关会破坏其普通 K 折论证，并展示非依赖 CV 会损失训练信息。

**对本任务的边界：** 不能把这篇文章当作非平稳数据、pinball QR 或重叠 H 步峰值标签的普通 K 折许可。本任务没有证明这些定理前提。R3 采用按时间推进和 H 边界清除，是面向信息时钟的设计选择；它不是该定理自动给出的保证，清除边界也不会使折内重叠损失独立。

### 1.3 Timmermann：简单组合与收缩的估计误差背景

**书目：** Timmermann, A. (2006), “Forecast Combinations,” *Handbook of Economic Forecasting*, volume 1, chapter 4, **135–196**, DOI [10.1016/S1574-0706(05)01004-9](https://doi.org/10.1016/S1574-0706(05)01004-9)。

- **正式版本的原文依据：** [ScienceDirect 官方章节](https://www.sciencedirect.com/science/article/abs/pii/S1574070605010049)。直接 PDF 请求返回 403；但本次重新取得了官方页面索引中的**原文正文**，包括 §3 “Estimation” 和 §5 “Shrinkage methods”，不是仅有摘要/元数据。这里以章节定位，不虚构未见的期刊版页内位置。
- **另外实际读取的作者原稿：** [UCSD 作者托管 combine.pdf](https://econweb.ucsd.edu/~atimmerm/combine.pdf)，封面实际标明 **1 November 2004**，84 页；SHA-256 `fb7fa4e13c3c5b8fc3a764d2e92987e873b390b4c7c4ab53a054126a66e3f109`。正文编码异常，本次渲染并实际查看了封面及 **§6.4、printed p.57**。该节号属于 2004 原稿，不与正式版 §5 混用。

正式版 §3 说明估计组合权重会引入误差，简单等权可胜过需要估计权重的程序；§5 解释以偏差换取更小权重估计误差的收缩动机。作者原稿 §6.4 讨论向等权收缩的经验表现，也保留收缩参数敏感性的限制。

**可用联系仅是背景：** 小样本下不应把噪声较大的经验最优复杂程序当成已知最优。**本任务只选择 I 或 QR 时，并没有平均预测或估计组合权重。** 因此它不能被描述为实施了 Timmermann 的 forecast combination；向无条件 I 的模型选择也不是向等权组合的同一数学操作。这是有限样本下偏向简单参照的类比，不是结果保证。

## 2. R0–R3 应如何承接这些文献

下表只解释交由主任务事先冻结的程序，不根据新结果修改菜单。

| 规则 | 本任务含义 | 文献支持及限制 |
|---|---|---|
| R0 | 在既定 QR 菜单 `{.001,.01,.1,1,10}` 中按验证均值选最低值。 | 成熟的验证选参；经验最低点本身有估计误差。 |
| R1 | R0 的候选中显式加入截距经验分位数 I，即无条件 headroom 参照。 | 提供简单候选；I 的普通秩不等于 corrected-rank F，因此未精确嵌套 F。 |
| R2 | 在同一验证段上按候选相对最佳候选的配对损失差与 HAC SE 定义可接受集合，再选事先声明的最强收缩候选。 | 借用 ESL 偏向简约的 one-SE 思想；配对差/HAC 是本任务适配，不是 ESL 原公式，也不是非劣性检验。 |
| R3 | 按时间推进的内层验证、清除 H 边界，再应用已声明的 R2 选择规则。 | 使验证流程符合可用信息时钟；不能借 BHK 定理声称一般有效，也不能把各折当独立重复。 |

R1 增加 I 后，候选集内的最低**验证均值**不会因增加选项而上升；R2 可有意选取均值略高的简单候选。二者都不保证新评估期表现不劣，更不保证相对 F 不劣。

## 3. R2 的精确定义必须在设计中冻结

令 `c*` 是固定候选集上验证平均损失最低的候选，令

\[
d_t(c)=\ell_t(c)-\ell_t(c^*),\qquad
\widehat{SE}_c=\sqrt{\widehat\Omega_{NW}\{d_t(c)\}/n}.
\]

若设计采用 `mean(d(c)) <= SE_c` 作为 one-SE 可接受条件，就应把它直接写出，并称为本任务的适配。该阈值使用的是**配对损失差**的估计长期方差，不能误写为最佳模型损失的普通 iid 标准误。

主任务应在新评估前同时固定：候选集；有限 λ 和 I 的收缩顺序；最佳均值的完全平局规则；HAC 的核、带宽和有限样本归一化；阈值是否含等号；完整候选失败时的整格处理；R3 的所有切点、训练长度、清除边界和合格 issue 规则。不得在看到新评估后更换任一项。

最强收缩顺序可以预先声明为 **I，然后 λ=10、1、.1、.01、.001**。这是本任务的候选优先顺序，不是对所有模型类的复杂度定理。最佳候选自身的差为零，因而在正常完成的计算中应有可接受候选；这不授权修补、重试失败格。

这里的 SE 也有局限：52 点、H=24 和高序列依赖使长期方差估计脆弱；`c*` 已由同一段数据挑选；同时比较若干候选也有选择不确定性。一个 SE 的阈值没有覆盖这些选择后问题，不能标为预定显著性水平、等价性区间或评估非劣性证书。

## 4. 为什么预先选 R2 主要、R3 敏感性

这是**设计判断**，依据为文献边界和已知样本布局，不是新实验结论。

1. **少一层历史位置选择。** R2 对同一段 52 个验证 issue 使用已冻结的候选损失。最终设计的 R3 保留完整外层验证段，并添加更早训练前缀中的滚动评分折；它不再切短这 52 行。每折仅有有限信息，统一 24 条记录的边界清除会消耗历史，较早状态也未必代表评估期。H=24 的峰值标签跨度为 25 个记录，不能将更多评分行直接等同于更多独立误差。
2. **规则更易事先界定。** R2 只增加一个固定的容忍规则与简单候选优先级，直接回答“允许保守选择是否帮助”这个有限问题。R3 还增加切点、内层窗口、清除方式和折汇总，增加了需要冻结的选择。BHK 并未证明本任务可以无代价地使用随机 K 折来恢复样本量。
3. **保留 R3 的信息价值。** 有足够早期历史、明确成熟标签和完整内层验证时，按时间推进的 R3 值得比较；但其合格 origins 数应由冻结的索引设计给出，不能先假定足够。H 清除可避免边界上的直接标签重叠，不能消除折内依赖或分布变化。

R2 自身可能过度保守而舍弃真实条件增益；R3 也可能利用多个时间位置提高选择稳定性。因此建议只固定其主要/敏感性身份，保留完整两者结果，不事先宣称谁会胜出。若任一规则数值失败或因冻结的历史/时间限制不可运行，依既定规则保留失败，不看结果后另换程序。

## 5. 可用于论文的事前定位

> We combine established ideas: an explicit unconditional candidate, a parsimonious selection preference inspired by the one-standard-error rule, and validation that respects the forecast information clock. Our paired-loss HAC tolerance is a task-specific adaptation, rather than the standard cross-validation formula or a finite-sample noninferiority guarantee. Forecast-combination research motivates caution about estimated optimal complexity, but the present selection rule does not average forecasts.

这里的可检验增量是既定峰值任务中这些成熟做法的具体实证比较；不是首个 one-SE 程序、首个时间序列 CV 方法、新收缩理论或新组合框架。任何收益结论必须等预先冻结的评估完成后写，不能从文献背景推出。

周度原 Treasury-bill 与追加 12 条序列共享报告体系；本记录不授权把它们当独立样本合并检验。它也不判定 S1–S3 是否通过，不变更原 primary，不改变用户的发表篇幅/摘要门槛。已有旧结果被看过的身份仍须保留；新 retrospective 段的时间冻结不能重新命名为独立外部验证。

## 6. 本记录的操作边界

唯一新增的正式文件是本记录。为读取原文，作者提供的 ESL 和 Timmermann 文献 PDF 及相关阅读页仅存于忽略的私有 scratch；这些是文献材料，不是新增金融数据。未拟合、评估或重跑任何模型，未修改原归档，也未调用 Claude/Cloud 或双模型审查。设计与预测阈值由主任务单独冻结并提交后，才能进入新的 R6 评估。
