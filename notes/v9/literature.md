# C2：稳定性诊断、断点定位与参数自助校准的原始文献核对

核对日期：2026-10-24。核对者仅做文献与方法适用性检查；未读取真实序列进行估计，未运行诊断、模拟、预测或新的数值检验，未修改设计或实现。此记录不预设 N1–N4 会成立。方法及计算规则以随后独立提交的 `protocol/v9/nonstationarity-design.md` 为准。

## 1. 设计可采用的定位

对 AR(1) 残差的带符号累积和及中心化平方累积和，用拟合的稳定 AR–GARCH–t 零假设产生有限样本参考分布，是本任务可以预先明确的**模型依赖联合筛查**。其累积和形式有下列经典来源；它不是直接运行 BDE 的递归残差检验或原始 ICSS 后读取其通用 5% 临界值。若使用 OLS 残差，应称 OLS-residual CUSUM；若用两项最大值、特殊标准化、参数自助校准和受限分段，应完整给出本任务自己的统计量与算法，不能暗示该完整组合已由经典论文证明为精确 5% 检验。

均值/平方残差筛查的拒绝只说明指定零假设在该筛查下不合适，不能自动定位为 AR 斜率改变、无条件方差改变或某一经济制度变化；不拒绝也不证明所有 AR/GARCH 参数稳定。参数自助法改善与拟合零假设不匹配的参考分布问题，但依赖该模型、参数估计、矩条件和样本长度；它不自动修复错误的动态模型，也不把事后分段变成真实机制识别。

## 2. 核实的论文与出版信息

|ID|核实书目与原始来源|本轮直接查到的内容及访问边界|
|---|---|---|
|L1|Brown, R. L., Durbin, J., & Evans, J. M. (1975). **Techniques for Testing the Constancy of Regression Relationships Over Time**. *Journal of the Royal Statistical Society: Series B (Methodological)*, **37(2), 149–163**. [出版社 DOI 页](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/j.2517-6161.1975.tb01532.x)，DOI `10.1111/j.2517-6161.1975.tb01532.x`。|出版社元数据与原摘要直接核实：recursive residuals、CUSUM、CUSUM of squares。使用该 DOI 页明确给出的正文页码 149–163；不把包含讨论的常见 149–192 写成正文页码。未取得可完整检索的正文，故不声称逐条核对了原文所有定理假设。|
|L2|Inclán, C., & Tiao, G. C. (1994). **Use of Cumulative Sums of Squares for Retrospective Detection of Changes of Variance**. *Journal of the American Statistical Association*, **89(427), 913–923**. [期刊 DOI 页](https://doi.org/10.1080/01621459.1994.10476824)。|期刊检索内容直接核实题名、作者、卷期页码及 independent observations / iterated cumulative sums of squares；直接 DOI 页面有 403，未声称读完原文。其 Gaussian/iid 临界值的限制另由 L3 原文核对。|
|L3|Sansó, A., Aragó, V., & Carrion-i-Silvestre, J. L. (2004). **Testing for changes in the unconditional variance of financial time series**. *Revista de Economía Financiera*, **4, 32–53**. [期刊原 PDF](https://aefin.es/wp-content/uploads/2019/02/A4-2_443809.pdf)。|原文 22 页、印刷页 32–53；直接核读 §§1–4，尤其 pp.34–37 的 κ1/κ2 与 A1。作者所属机构的[作者出版记录](https://portalinvestigacio.uib.es/documentos/5ebf1e7e2999524bdf79d76c)确认 2004/第4期；本文未查到可信 DOI，不填造 DOI。|
|L4|Bai, J., & Perron, P. (1998). **Estimating and Testing Linear Models with Multiple Structural Changes**. *Econometrica*, **66(1), 47–78**. [作者保存的期刊原 PDF](https://www.columbia.edu/~jb3064/papers/1998_Estimating_and_testing_linear_models_with_multiple_structural_changes.pdf)；DOI `10.2307/2998540`，由[期刊原目录](https://www.jstor.org/stable/i353347)核对。|作者稿的期刊版首页直接核实书目、least-squares multiple structural changes、部分参数可变与断点数检验。PDF 是扫描件，未把无法全文检索当作已通读全部证明。具体实施和串行相关处理主要由 L5 核对。|
|L5|Bai, J., & Perron, P. (2003). **Computation and analysis of multiple structural change models**. *Journal of Applied Econometrics*, **18(1), 1–22**. [出版社全文](https://onlinelibrary.wiley.com/doi/10.1002/jae.659)，DOI `10.1002/jae.659`。|出版社全文直接核读 §§2–5：SSR 全局动态规划、pure/partial structural change、HAC 和 trimming。出版在线日期为 2002-10-08，卷期正式年份为 2003，不误记为另一篇 2002 论文。|
|L6|Bai, J. (1997). **Estimating Multiple Breaks One at a Time**. *Econometric Theory*, **13(3), 315–352**. [作者保存的期刊原 PDF](https://www.columbia.edu/~jb3064/papers/1997_Estimating_multiple_breaks_one_at_a_time.pdf)。|期刊版首页与 §§1–2、A1–A3 直接核读：逐一估计断点、以 least-squares 单断点分割递归；理论有明确过程和分离条件。DOI 的解析页面本轮未成功，故当前可引用核实的作者原文链接，不要求填入未直接访问核对的 DOI。|
|L7|Davison, A. C., & Hinkley, D. V. (1997). **Bootstrap Methods and their Application**. Cambridge University Press. Ch.4, **Tests**, pp. **136–190**, DOI `10.1017/CBO9780511802843.005`；Ch.8, **Complex Dependence**, pp. **385–436**, DOI `10.1017/CBO9780511802843.009`。|直接核对出版社[第4章页面](https://www.cambridge.org/core/books/abs/bootstrap-methods-and-their-application/tests/F5B333666C386C65D57EDA2872DD26E1)与[第8章页面](https://www.cambridge.org/core/books/abs/bootstrap-methods-and-their-application/complex-dependence/20B4EBEB97AEEB73BB141A1EAF2795EC)的出版信息和公开章摘要：参数/非参数检验、简单/复合零假设、通过拟合参数模型模拟相关资料。未取得整章正文，不把本任务具体 AR–GARCH–t 统计量的有效性归为该书已证明。|
|L8|Dufour, J.-M. (2006). **Monte Carlo tests with nuisance parameters: A general approach to finite-sample inference and nonstandard asymptotics**. *Journal of Econometrics*, **133(2), 443–477**. [作者保存的期刊原 PDF](https://jeanmariedufour.research.mcgill.ca/Dufour_2006_JE_MCT.pdf)，DOI `10.1016/j.jeconom.2005.06.007`。|期刊原 PDF 首页、Introduction 与 §6 的 point-estimate Monte Carlo 说明直接核读。区分 nuisance-free 的 exact Monte Carlo、maximized Monte Carlo，以及 plug-in parametric-bootstrap 的渐近条件。本任务若只代入拟合参数，不得称在有限样本保证精确 5%。|

## 3. 方法假设、成熟实现与本任务适用范围

### 3.1 BDE 递归残差与 OLS 残差不能混名

L1 的累积和与平方累积和建立在递归残差上；摘要明确残差的零均值、不相关与常方差性质。对具有 GARCH 条件方差的 AR 残差，不能照抄常方差参考边界声称名义 5% 有效。直接对原始头寸水平做 iid CUSUM 也会把自相关混入统计量。[L1 原摘要](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/j.2517-6161.1975.tb01532.x)

官方 `statsmodels.stats.diagnostic.recursive_olsresiduals` 返回 recursive residuals、其标准化版本、`rcusum` 和 CUSUM 图边界；`alpha=0.95` 是该 API 的置信水平参数，并非传入 0.05 的显著性水平。官方返回表没有独立的 CUSUM-of-squares p-value；不能把自行平方返回残差后形成的统计量冒充这个 API 已实现的原检验。[官方 recursive_olsresiduals 文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.recursive_olsresiduals.html)

`statsmodels.stats.diagnostic.breaks_cusumolsresid(resid, ddof=...)` 用的是 OLS 残差，其 sup 统计量的默认 p 值来自 Brownian bridge 渐近分布，引用 **Ploberger, W., & Krämer, W. (1992), The CUSUM Test with OLS Residuals, Econometrica 60(2), 271–285**。该书目在官方文档核实；本轮未直接读到其原全文，因而不额外声称核查全部假设。官方还提示非截距 regressors 均值接近零时普通 CUSUM 的 power 问题。[官方 breaks_cusumolsresid 文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.breaks_cusumolsresid.html)

**对当前设计的推导警戒，不是新实证结果：** AR 斜率改变可使条件残差均值随滞后水平改变，但若该水平的均值接近零，带符号残差的边际均值仍可接近零。因此仅用 mean-CUSUM 加 square-CUSUM，不应宣称能完整检查所有 AR 参数变化。可在设计中限定这两项筛查的操作性零假设；若确实要加入含滞后水平的 score 分量，应在任何观察结果出现前连同联合校准冻结，不能看到 N1 不成立再添加。

### 3.2 原 ICSS、κ1 与 κ2 的适用区别

L2 的 ICSS 是迭代累计平方和检测无条件方差变化的经典程序。L3 §§2–3 直接说明：原 IT 统计量的 Gaussian/independence 标准化在异常峰度和条件异方差下存在尺寸偏误；厚尾和 GARCH 可造成过度拒绝、虚假方差断点。κ1 修正 iid 非正态峰度；κ2 还对平方残差序列的长期方差作修正，例如使用 Bartlett/Quadratic Spectral lag window。只做样本峰度修正不能消除平方残差自相关。[L2 期刊页](https://doi.org/10.1080/01621459.1994.10476824)，[L3 原文 pp.34–37](https://aefin.es/wp-content/uploads/2019/02/A4-2_443809.pdf)

L3 §3 A1 要求高于四阶的适当矩、有限平方过程长期方差及 mixing 条件；原文明确 iid Student-t(3) 不满足其条件。§4 又讨论 covariance-stationary GARCH 也可能不满足所需高阶矩。因而“有有限二阶矩”或“GARCH α+β<1”不足以保证平方累积和的常规 Brownian-bridge 理论。不能把 κ2 描述为对任意 t 重尾均有效的万能修正；本记录不据此裁剪真实拟合的 t 自由度。[L3 原文 pp.36–39](https://aefin.es/wp-content/uploads/2019/02/A4-2_443809.pdf)

**本任务选择：** 可以不直接采用 κ2，而用预先规定的参数自助参考分布照顾拟合 GARCH-t 下的峰度与平方依赖。此选择是模型化校准，不等于实现了 κ2，也不继承 κ2 的理论结论；矩条件不佳、近 IGARCH、尾参数不稳定时仍须保留模型依赖和有限样本局限。

### 3.3 Bai–Perron 与逐一分段的命名边界

L4/L5 的问题是线性回归系数在未知日期发生多次结构变化，包含 pure 与 partial change。L5 §3 的实际算法以受最短段长约束的 **SSR 全局最小化动态规划**估计断点；§§4–5 对异方差和串行相关提供相应协方差处理，不是普通 F 临界值无条件有效。文中程序为 GAUSS；本轮没有核实一个官方 statsmodels Bai–Perron 完整实现，不能将 `breaks_cusumolsresid` 当作它。[L4 作者原文](https://www.columbia.edu/~jb3064/papers/1998_Estimating_and_testing_linear_models_with_multiple_structural_changes.pdf)，[L5 §§3–5](https://onlinelibrary.wiley.com/doi/10.1002/jae.659)

L5 §5.1/§5.5 警告 5% trimming 在允许串行相关/异方差时可有明显尺寸失真，并给出较高 trimming 的实务建议，串行相关且 T=120 的讨论中提及 20%。因此本轮事先采用 20% 最短比例有成熟谨慎实践支持，**不代表 20% 对本数据自动保证尺寸正确**；104 观测的固定下限和最多 2 个断点是本任务的计算/拟合限制，不是该论文给出的普适数值。[L5 §5](https://onlinelibrary.wiley.com/doi/10.1002/jae.659)

L6 是 one-at-a-time 的原始理论依据，但其明确讨论的模型和估计准则不能自动覆盖任意残差/平方 CUSUM 组合。若当前实现采用贪心分割，应称 **constrained binary segmentation using the frozen bootstrap-calibrated screen**；不得声称跑了 Bai–Perron 全局动态规划。分割得到的是估计日期，受最短段长、最多断点和搜索准则影响；相反变化可能掩蔽，检测与精确定位是不同任务。[L6 §§1–2](https://www.columbia.edu/~jb3064/papers/1997_Estimating_multiple_breaks_one_at_a_time.pdf)

## 4. 参数自助校准在设计提交前需明确的事项

以下为由 L7/L8 与前述条件形成的本任务设计建议，不是声称文献已经证明此完整算法，也没有据此进行计算。

1. **冻结输入与零假设。** 只用该序列原评估期起点之前的 prefix；说明稳定 AR(1) 均值、GARCH(1,1) 条件方差、标准化 Student-t 创新、初值/burn-in、参数约束、尺度处理及拟合失败规则。模拟要保留时间顺序和 GARCH 递推；不能打乱原始残差并声称保留条件波动。L7 Ch.8 为拟合参数相关模型再模拟提供一般依据。[L7 Ch.8](https://www.cambridge.org/core/books/abs/bootstrap-methods-and-their-application/complex-dependence/20B4EBEB97AEEB73BB141A1EAF2795EC)
2. **每个 bootstrap 样本重复同一统计量计算链。** 实际统计量若从全段重新拟合 AR 得到残差，模拟样本也重新拟合 AR 后再生成残差、中心化、标准化和取最大值；实际统计量若依赖估计 GARCH 过滤/尺度，模拟样本也按相同规则重新估计相应部分。用观测样本拟合参数产生 bootstrap 路径，不等于统计量计算中可以把估计步骤省掉。该要求是保持 bootstrap 复制对象与观测统计量一致的设计原则；当前记录不把它写成某篇针对本统计量的专门定理。
3. **联合统计量与候选日期一并校准。** mean / square（或任何预先加入的 score）分量的最大值、候选 break 的 trimming、tie rule 与标准化在运行前明确。若取各分量 p<0.05 任一拒绝却仍称整体 5%，会改变联合拒绝概率。应对完整 joint statistic 在零假设模拟中同样取最大值，或事先采用有效的多重性规则；不能在看过结果后择最小 p。
4. **明确 p 值的近似地位。** 可预先用 `p_boot=(1+#{T_b>=T_obs})/(B+1)`，同时固定 B、ties、seed、失败重复处理及临界值/拒绝规则；分辨率为 `1/(B+1)`，有限 B 带来 Monte Carlo 不确定性。该 plus-one 形式不消除拟合参数 nuisance。L8 的 exact Monte Carlo 适用情况与其 §6 plug-in point-estimate 渐近近似须区分；本任务不用“finite-sample exact 5%”。[L8 §§2,6](https://jeanmariedufour.research.mcgill.ca/Dufour_2006_JE_MCT.pdf)
5. **全局 screen 与定位分开记。** 若 N1 根据 prefix 上一次全局联合筛查是否拒绝确定，后续定位应清楚标为条件于筛查的估计过程。每个递归子段再用 5% 不自动给所有断点提供 5% family-wise 保证；要么预先校准完整搜索程序，要么预先控制层级/多次比较，要么仅将定位视为受约束的探索性切分。不许把估计断点日期直接标为单独的 95% 置信断点。
6. **最短段长基准不能含混。** `h=max(104,ceil(0.20*T_prefix))` 如采用，应说明 T_prefix 是固定整段 prefix 长度；递归到子段后仍用这个绝对 h，还是重新按子段求比例，必须在设计写死。每个候选切分两侧均满足 h；若 `T<2h` 不可分，最多断点还受可行分段数约束。这是约束的定义，不是文献证明的最优值。
7. **13 条序列的计数不等于独立试验。** N1 的“至少 7 条原始 5% 拒绝”是预登记阈值；同报告体系相关类别不独立，不应给它套二项分布尾概率或据此称 family-wise 5%。同时报告全体序列和失败/不可检验状态。失败不是“不拒绝”、未拒绝也不是稳定性被证实。
8. **日频/小时断点密度是受限过程的输出。** 若最多两个断点，对长小时 prefix 与短日频 prefix 都强制相同上限，会机械影响“每100观测断点数”；20% trimming 也按各自 observation clock 改变可见尺度。N4 应解释为这一固定检测器在不同记录钟下的输出，不能直接推成经济时间尺度上的真实不稳定程度大小；原物理 horizon/聚合/clock 的区别继续保留。
9. **拒绝不识别唯一原因。** 稳定 AR–GARCH–t 零假设被拒绝可能来自均值/方差断点，也可能来自该阶数、尾分布、时钟或其他动态错设。分段拟合拼接若重现 QR 损失，只支持“在本次指定分段生成机制下”；不能倒推真实数据机制已被证明。不因结果不利更换检测器、max breaks 或 minimum length。

## 5. 对实现与论文的具体命名建议

推荐在 protocol 中明确使用一句话：

> We screen pre-evaluation prefixes for departures from a constant-parameter AR(1)–GARCH(1,1)–t model using a prespecified joint cumulative-residual statistic, calibrated by a fitted-null parametric bootstrap. Break dates are estimated by a separately specified constrained segmentation procedure.

这句话仅作为设计措辞候选，**不是已实施或已通过的描述**。若最终没有联合 AR score 分量，随后应明确 screen 针对残差均值/平方波动而非所有参数方向具有一致 power。若最终用 BDE 的递归残差则改其名称和统计量；若真的实现 Bai–Perron，则写出 SSR 目标、pure/partial-change 设定、HAC、trimming 和断点数选择，不能仅用名字替换当前算法。

原文可支持的引用关系为：BDE = 递归残差累积和的经典背景；Inclán–Tiao = 原始 ICSS；Sansó et al. = 金融序列中 ICSS 的峰度/条件异方差修正及矩限制；Bai–Perron = 回归多断点估计/检验与分段长度实践；Bai1997 = 顺序逐一估计思想；Davison–Hinkley = 参数相关模型重抽样的一般方法；Dufour = nuisance plug-in 与 exact Monte Carlo 的区别。它们都不直接证明本任务的 custom joint screen 在拟合 GARCH-t 下有限样本尺寸等于 5%。

## 6. 核对与交付边界

本次只新增本文件；未创建/覆盖 design、代码、数据、结果或模拟文件。网页依据仅采用上列期刊原文/DOI/作者保存原文/出版社书章节和官方 statsmodels 文档；作者所属机构记录仅用于 L3 的年份/期号元数据。搜索中出现的论坛、教学幻灯、百科、二手论文摘要网站没有作为方法主张证据。

明确未完成的原文访问：BDE 全部正文、Inclán–Tiao 全文、Ploberger–Krämer 原全文、Davison–Hinkley 完整章节。本记录分别标明实际只读到的摘要/官方说明，不用这些访问缺口杜撰更强定理。没有新增研究发现、C2 估计值或 N1–N4 判定。
