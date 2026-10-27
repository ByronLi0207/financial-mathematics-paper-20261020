# C2 方法独立审查：预注册前建议，不是正式设计

审查时间：2026-10-24T18:23:54.370792+00:00。本审查只阅读既存 WP3 设计、生成器源码和公开原始论文/官方文档；未读取真实序列数值，未运行真实诊断、AR/GARCH 拟合、自助模拟或预测。仅写本文件。以下都是在结果出现前的建议，不是对 N1–N4 的预判。

## 审查结论

建议主检验采用 **Hansen (1992) 的 OLS 联合 score-instability 统计量，以固定参数 AR(1)-GARCH(1,1)-标准化 t 过程做参数自助校准**。理由是只看残差本身的 CUSUM 对 AR 斜率变化可能弱，而该联合分数同时包括截距、斜率和残差平方通道；有现成、可直接核查的官方实现，不需要在本轮发明新的检验。它仍是模型条件的校准检验，并不无条件保证 5% 尺寸。[Hansen 作者页](https://users.ssc.wisc.edu/~behansen/papers/jpm_92.html)、[官方实现与源码](https://www.statsmodels.org/stable/_modules/statsmodels/stats/diagnostic.html#breaks_hansen)。

Root 提议的 BDE recursive CUSUM + CUSUMsq 也可实施，但应选一个统计量家族为主，不能分别运行后挑更容易拒绝的结果。若坚持两通道 max 统计量，组合方式、标准化和整套搜索必须在自助样本里原样重做，使用联合零分布；两个各 5% 的检验取 OR 不是 5% 联合检验。

正式设计提交前最需要解决的四点：

1. 明确检验无效、null 拟合不收敛、单位根边界和无限四阶矩时的失败规则。
2. N1 的 raw 5% 拒绝数与 Holm13 的确认性主张分开；不能写 raw N1 达到 7 就获得家族层面确认。
3. 不把数据选择后的子节点 p 值加个 alpha 预算就称为修正了断点搜索。
4. 冻结模拟排程，并明确伸展排程几乎消除评估邻域内变化、循环排程则增加人工 last→first 转移。不能看 N2 后改变排程。

## 三种成熟路线的取舍

| 路线 | 成熟来源与优点 | 本任务的弱点 | 建议角色 |
|---|---|---|---|
| Hansen 联合 score-instability + AR-GARCH-t 参数自助 | 原论文的例子包括 AR(1)；官方实现含系数分数与残差平方；每自助样本只须重估 OLS 即可构造同一统计量 | 并非检验所有 GARCH 参数的全能检验；t/持久性导致无条件四阶矩不存在时理论边界严重；全样本 null 校准仍有模型错设风险 | **推荐唯一主检验** |
| BDE recursive CUSUM / CUSUMsq 联合 max + 同一参数自助 | 经典回归稳定性方法，图形直观；定位可从累积过程观察 | 经典临界线不适用于直接套用 GARCH/t；递归残差不在该 null 下自动独立同方差；只累积 e 的通道可能遗漏斜率变化；初始化消耗短样本 | 可替代主方法，勿与第一种择优 |
| Andrews sup-Wald / Bai–Perron 有界分段定位，方差用 modified ICSS | 断点搜索、最小分段与多断点理论成熟；modified ICSS 显式处理金融序列条件异方差和峰度 | AR-GARCH-t 的联合参数变化需额外推导/自助；纯 OLS 分段 SSR 难以定位只有方差的变化；两种检验又增加多重性；本轮预算有限 | 留作后续稳健性，不作为临时救援 |

BDE 原论文：[Brown, Durbin & Evans (1975), JRSS B 37(2), 149–163](https://academic.oup.com/jrsssb/article/37/2/149/7027284)，DOI https://doi.org/10.1111/j.2517-6161.1975.tb01532.x 。该来源核对到出版信息和摘要；没有声称其经典临界值在 AR-GARCH-t 下已被证明有效。

Andrews：[作者托管原论文](https://users.ssc.wisc.edu/~behansen/718/Andrews1993.pdf)，DOI https://doi.org/10.2307/2951764 。未知断点本身就是搜索的 nuisance；不能把选中日期当作事先已知日期再用普通 Chow 临界值。

Bai–Perron：[作者托管 1998 原论文](https://www.columbia.edu/~jb3064/papers/1998_Estimating_and_testing_linear_models_with_multiple_structural_changes.pdf)，DOI https://doi.org/10.2307/2998540 。该文的线性分段理论不能被本轮自定义 GARCH-t 分段生成器直接冒用为已验证的完整定理。

modified ICSS：[Sansó, Aragó & Carrion-i-Silvestre 原文，Revista de Economía Financiera，2004，4，32–53](https://aefin.es/wp-content/uploads/2019/02/A4-2_443809.pdf)。原文明确指出原始 ICSS 在厚尾及条件异方差下会产生严重尺寸偏差，并提出考虑四阶矩和条件异方差的修正；不能直接用原始 ICSS 的 iid Gaussian 阈值。

## 可直接落地的主统计量与 bootstrap

令 M 为用于 AR 回归的转移数。405 个 level 观测通常只产生 M=404 个 `(y[t-1], y[t])` 对；必须明确所有 minsegment、日期和密度分母到底用 level 还是回归对，不能差一位。固定模型含截距：`y[t] = c + phi*y[t-1] + e[t]`。全段 OLS 残差记 e[t]。

推荐直接复用官方 Hansen 统计量。取 `x[t]=(1,y[t-1])`、`f[t]=(x[t]*e[t], e[t]^2-mean(e^2))`，累积分数为 `S[k]=sum(t<=k) f[t]`。官方实现计算 `H=trace((M*sum(f[t]f[t]'))^-1 * sum(S[k]S[k]'))`。为数值稳定，level 可以按本段固定仿射变换预缩放；须对原样本和全部自助样本采用相同规则。病态/奇异矩阵不得静默加 ridge 后沿用原检验名；预先定容忍阈值并记录失败。[统计量说明](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.breaks_hansen.html)。

不要用该函数返回的表格临界值作为 GARCH/t 的主 p 值。按 null 拟合一次 constant AR-GARCH-t，再用其参数生成 B=999 条相同长度、相同初始化规则的合成 level 序列。每条必须重新构造其自己的滞后列、重新估计 OLS、重新计算 H。采用 `p=(1 + #{H_boot >= H_observed})/(B+1)`，并保存超过次数和 B。它是 plug-in 参数自助 p 值，不是已知 nuisance 参数下的精确随机化 p 值。

**不必每条 bootstrap 再拟合 GARCH**，前提是检验统计量只依赖 OLS score：GARCH 的估计在这里只确定 null 生成参数。若设计改成以重新估计的条件方差标准化残差、GARCH score 或 likelihood-ratio 为统计量，就必须在每条自助样本重做对应拟合，不能一面换统计量一面沿用省时论证。

AR lagged dependent variable 的处理不能省略：保留原始 X 固定不动、只随机置换/重抽残差，破坏了 `x[t]=(1,y[t-1])` 的生成关系。BDE 路线也一样，bootstrap 中必须递归生成 y、重建 X、按原初始化长度递归估计参数。经典递归残差的特殊独立同方差性质不自动延伸到条件异方差的 AR 样本。[官方 recursive_olsresiduals 文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.recursive_olsresiduals.html)。

## null、厚尾及拟合失败的边界

null 应明确为“在拟合的 constant AR(1)-GARCH(1,1)-t 模型族内，AR 均值关系及无条件尺度保持稳定”。检验拒绝可以来自真实参数变化、非线性/均值错设、离群值、近单位根、日历结构等；不能一律译成结构断点，更不能译成制度变化的因果证据。反过来，不拒绝不证明稳定。

建议保守有效性闸门：`abs(phi)<1`、`omega>0`、`alpha>=0`、`beta>=0`、`alpha+beta<1`、`nu>4`，且无条件四阶矩条件 `alpha^2*kappa + 2*alpha*beta + beta^2 < 1`，其中标准化 t 的 `kappa=3*(nu-2)/(nu-4)`。有限二阶矩和有限四阶矩是不同要求；只有 `nu>4` 仍不够保证 GARCH 无条件四阶矩有限。[He & Teräsvirta 研究记录](https://swopec.hhs.se/hastef/abs/hastef0168.htm)、[作者工作论文](https://swopec.hhs.se/hastef/papers/hastef0168.pdf)。上述 GARCH(1,1) 条件也可直接从 `h[t]=omega+(alpha*z[t-1]^2+beta)h[t-1]` 平方取期望推得。

官方 arch 的 Student-t 估计默认下界仅为 2.05，**并不保证四阶矩**；其创新是标准化到单位方差的 t，不是未缩放的 `standard_t(nu)`。必须用 `z=t_nu*sqrt((nu-2)/nu)`。[官方 Student-t 分布及源码](https://bashtage.github.io/arch/_modules/arch/univariate/distribution.html#StudentsT)。

若上述闸门不满足，建议标 `CALIBRATION_INADMISSIBLE`，不给确认性稳定/不稳定结论；不能在看到结果后把 nu 或持久性裁剪到合格。若决定从一开始做约束估计，须事先写出边界与优化规则，并称为约束模型近似；它不会证明真实序列本身拥有该矩。拟合不收敛、bootstrap 任一必需条失败、非有限路径和严重矩阵病态的处理也须冻结，不能悄悄重抽或减少分母直到 p 变好。

B=999 在 0.05 附近的 Monte Carlo 标准误约 0.0069；Holm 首阈值 0.05/13≈0.00385 的精度更粗。设计可坚持 B=999，但应保存离散超过次数、报告 Monte Carlo 精度，并禁止只对临界附近结果加抽到想要的方向。定种子之前需分离 diagnostic bootstrap、pilot、formal simulation 的流。

## 检验与定位分离：不要把子节点 alpha 预算当成充分修正

建议每条序列只做一次全段主检验，13 条周度序列构成固定家族。**定位用于合成过程校准，是描述性估计；不再给每个选中断点一个未经选择修正的“5% 显著”标签。**

若采用 binary segmentation，可把 `maxbreaks=2`、`minsegment=max(104,ceil(0.2*M))`、搜索网格、平手取最早、节点优先级和停止准则全定死；但子节点区间由父节点极大值选出，该节点的普通未选择条件 p 值不再自动有效。alpha spending 只能在每个被分配 p 值本身有效的前提下控制多重性。可以完整 bootstrap 重放整套搜索并校准其最大值/最大改进量，或者仅作描述性定位。后者最适合本轮预算。

一个可实现的描述性定位方式是按三通道 score 的二次范数在允许 k 上取最大，随后按同一规则继续分割，最多两处；也可以预先固定高斯准似然分段 cost `n_j*log(SSE_j/n_j)`，对 0、1、2 个分段模型用固定 BIC 处罚择分区。**这只是定位准则，不应冒称完整 Bai–Perron GARCH-t 检验。** 若用 score 定位，还需冻结是否除以 `r*(1-r)`，不准在看到位置后改权重。后续分段拟合从同一段截取 AR 对，避免把前一 regime 的首个跨界转移误归入段内估计。

null 未拒绝的序列是否强制零断点、用于 DGP 的拒绝门槛用 raw 还是 Holm，都必须先定。建议 DGP 用 Holm13 通过的周度系列分段，其余零断点；同时保留全部未经 Holm 的 pointwise 结果。若 raw 通过就分段，也可作为事先规定的敏感性设计，但不得在跑完后换成这个门槛以凑 N2。

## N1、N4 以及共同报告体系

建议把用户给出的 N1 原始目标保留为明确的描述性门槛：`N1_raw: #{p_raw<=0.05}>=7 of 13`；另设 `N1_Holm: #{p_Holm<=0.05}>=7 of 13` 作为更强确认性陈述。最终主文以 Holm 结果决定能声称哪些具体序列不稳定，同时如实回答 N1_raw。只满足 raw 时不得写“至少七条经过家族校正后不稳定”。13 条并不独立，不能另加独立二项分布的拒绝数 p 值。[官方 Holm 实现入口](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)。

缺失/不合格序列不可从家族中删除后缩小 m。Holm 保留 m=13，可用 p=1 占位计算但标记该行 `UNEVALUABLE`；占位不是“已证明稳定”。N1_raw 若有未知，报告已知拒绝数下界和加上未知后的上界；下界已达 7 才可判 MET，上界不足 7 判 NOT_MET，其他为 INCONCLUSIVE。

**N4 的“每 100 个观测”比较有机械的频率效应。** 相同日历期、相同一个真实断点，daily 的 1/405 与 hourly 的 1/8000 已会产生更高 daily 观测密度；并不能说明低频实际有更多制度变化。maxbreaks=2 的共同上限还会使 hourly 的每观测密度受到更强机械压缩。建议同时固定并主报每日历年的断点数、每序列的上限是否触发、实际 minsegment 对应的日历长度；每100观测可按用户要求保留，但只能称 observation-density 描述。

daily 与 hourly 必须用同一真实日历截止时间，均严格在各自评估开始之前。若日历重叠不完整，不能补观测或扩大区间；记录实际范围并降级比较。检验功效随 n、最短段长度、厚尾、聚合目标不同而变；daily 拒绝且 hourly 不拒绝也不直接证明二者“稳定性不同”。N4 如继续原门槛，应保留这一解释限制；更可解释的替代是事先改用同日历断点率，但这属于正式设计需要明确选择的变化。

## 模拟断点位置：两种映射没有中性的等价关系

本轮已核对 WP3 设计原值：burn=20000、retained=3264、validation=3072..3143、evaluation=3168..3239、H=6（本轮固定）、W=52/260。原 WP3 创新为 normal，C2 按用户要求改为 fitted t；必须在两条 C2 处理臂同时改成同一族，不能说 C2 与 WP3 的 DGP 除断点外完全相同。

**相对长度伸展**：把前缀断点 k 映射为 `round(3264*k/M)`。优点是保留一次历史顺序、各段占比，无人工回到早期 regime。缺点在本设置特别严重：末段至少104/404，故最后断点最迟大约2424，离3168评估起点已有约744点。W260 的训练、validation、evaluation 及168点长RMS几乎均落同一个末段；这个设计主要测试“末段参数不同于全样本参数”，很难测试训练/评估邻域的变化冲击。其 N2 不成立不能排除真正发生在该邻域的不稳定机制。**绝对不能看到 N2 不成立后把断点挪到评估段。**

**保留原 dwell lengths 的循环 regime stress schedule**：依原分段长度组成长度约404的 regime 环；每个 repetition 在生成创新前抽取固定相位，W、模型、断点/constant 两臂用同一个 repetition 编号和随机流约定。整个20000 burn与3264 retained均按事先固定规则推进；不在断点重置 y、h 或前一残差。优点是评估窗口不被故意放在某个断点之后，平均覆盖不同暴露位置；W260 看到相邻 regime 的可能性保留。缺点是 last→first 是**人为新增的反向/回归转移**，历史中并未观测；多轮重复相同 regime 也不是历史复现。

若研究目的在本轮有限 WP3 位置下测试“换 regime 是否足以造出损失”，推荐循环 stress 方案为主、预先冻结并明确人工 wrap；若坚持忠于一次历史顺序，则选伸展，并接受其评估暴露弱的结论。二者不能根据结果择优。

再一个术语边界：均匀随机相位的周期 regime 过程，在将相位边际化且适当初始化后可能具有严格平稳分布，尽管每条路径的条件参数不断切换。因此主文应称“带 regime 变化的 stress DGP / conditional parameter switching”，不要仅因为画了分段参数就宣称数学意义上整体非平稳。固定相位产生的时变模型与随机相位混合过程是不同对象。

循环排程应记录每次 replicate 的完整 regime-id、真实拟合断点转移位置、人工 wrap 转移位置，以及落入 training/validation/evaluation 的次数。不要按这些暴露次数删除或重加权 repetitions。未拒绝且零断点的序列，stress 臂应退化为 constant 臂；用共同随机数时应能对到相同生成路径。这是合成代码正确性的测试，不是新真实数据实验。

GARCH 拼接要保留状态连续：`h[t]=omega_j+alpha_j*e[t-1]^2+beta_j*h[t-1]`；AR 截距 c 与均衡均值 mu 的参数化不得混淆。不同段/对照的 nu 可以不同，使用共同 Uniform U 经各自 t 逆CDF转换能保留 common random numbers；不能假称不同 nu 下共用同一标准化 t 向量。不要在每个段边界重新 burn/reset；那会添加另一种变化处理。

## N2/N3 的固定计算口径与失败传播

对 source s、rep r、W、arm 计算 `d[s,r,W,arm]=100*(mean_pinball_QR33 / mean_pinball_F - 1)`，mean 只在同一对比的完整共同72个 evaluation origins 上。F 分母为零或任何必需报告缺失时该格 NA，不能截断到共同完成的部分。

每条 source 内先取32次 d 的中位数，再对13条 source 中位数取等权中位数。N2 为 stress 臂在 W52 与 W260 均严格大于+5%；N3 为 constant 臂 W52 位于[-3,+3]。严格/非严格边界应在设计中写清。预先允许的16次或只QR33降级按正式冻结的资源规则触发，不能从32次结果里挑16次。

这与 WP3 的 `100*(mean(loss_QR)/mean(loss_F)-1)` 是不同统计量；应分别列名，不把两个定义并排后声称数值可精确比较。source 与其重复不是13*32个独立真实样本，不做跨source独立合并检验或伪标准误。

任一 N2 必需 source×rep×W×arm 的 QR33/F 完整性失败，N2 不可评估；N3 在其必需 constant W52 网格有失败则不可评估。若 root 选择更严格“任一正式必需格失败则 N2/N3 全部不可评估”，必须原样冻结。QR4 的失败是否同时使 QR33 主要命题不可评估，也要写明；不能事后按有利性决定。完整网格全部报告，允许额外给“仅完成格的条件摘要”，但该摘要不能用于判 N2/N3 成立。

即使 N1/N2/N3 都成立，也只能写“这种经前缀校准、带人工排程的参数切换能够复现模拟中的损失”，不能证明它就是真实低频失利的机制。真实数据没有新的预测实验；整个研究仍位于已观察到原失利之后的探索性机制研究。

## 冻结前最低检查点

- 一个主统计量及其完整公式/软件版本；是否保留辅助检验且怎样命名。
- 405 level 与404 AR对的精确定义、前缀截止日期、缺失观测规则。
- null 参数化、厚尾/平稳矩边界、数值病态阈值、失败规则与 B=999 的离散 p 规则。
- Holm13、raw N1 与缺失行保留家族的做法；不以家族外的 daily/hourly 稀释或扩大13项家族。
- 定位与检验分离；max2、minsegment、分段准则、重复搜索的选择效应边界。
- DGP 排程、wrap、随机相位和共同随机数、GARCH状态连续性、无断点退化检查。
- N2/N3 原始 ratio 定义、两层中位数、失败传播与资源降级顺序。
- N4 同日历范围、观测密度与日历密度并列、maxbreak上限与不同功效的限制。

本文件没有批准任何尚未提交的设计；实施者应在正式 protocol 中明确采纳/不采纳及理由，然后单独提交设计，最后才运行。
