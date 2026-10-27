# C2 文献补充：Hansen 联合得分与描述性 BIC 分段

核对日期：2026-10-24。本文件仅补核对来源，不改已提交设计、既有 literature、实现或结果；没有运行任何估计、诊断或模拟。正式算法以独立提交的设计为准，不由这份文献笔记重新选择。

## Hansen1992 的实际覆盖

Hansen, B. E. (1992). **Testing for parameter instability in linear models**. *Journal of Policy Modeling*, **14(4), 517–533**. DOI [10.1016/0161-8938(92)90019-9](https://doi.org/10.1016/0161-8938(92)90019-9)。题名/卷期页码由[出版社页面](https://www.sciencedirect.com/science/article/pii/0161893892900199)核实；直接核读[作者保存原文](https://users.ssc.wisc.edu/~behansen/papers/jpm_92.pdf)的 pp.520–523 和 Table 1。

原文检验联合回归系数及误差方差的稳定性，包含静态与动态回归；明确排除 unit-root / deterministic-trend regressors 的常规分布套用，并明确该稳定性检验**不负责定位断点**。其局部替代允许一般参数漂移。原文 p.522 说明 score 外积矩阵提供 White 型异方差处理；残差串行相关需进一步修改协方差估计，不能把普通外积矩阵称为已做 HAC。[原文 pp.520–523](https://users.ssc.wisc.edu/~behansen/papers/jpm_92.pdf)

对含截距的 AR(1)，令回归行 `x_t=(1,N_{t-1})`、OLS 残差为 `e_t`、回归有效行数为 `M`、`s²=M⁻¹Σe_t²`。三项 first-order-condition 向量是

\[
f_t=(e_t,\;N_{t-1}e_t,\;e_t^2-s^2)^\top,\qquad
S_t=\sum_{i=1}^t f_i,\qquad V=\sum_{t=1}^{M}f_tf_t^\top.
\]

联合统计量可写为

\[
L_c=\frac1M\sum_{t=1}^{M}S_t^\top V^{-1}S_t
=\operatorname{tr}\!\left[(MV)^{-1}\sum_{t=1}^{M}S_tS_t^\top\right].
\]

这里 `M` 指实际用于 OLS 的行数，不是未经滞后处理的原始序列长度。公式与[官方 `breaks_hansen` 源码](https://www.statsmodels.org/stable/_modules/statsmodels/stats/diagnostic.html#breaks_hansen)核对一致：源码将 `x*resid` 与 `resid²−mean(resid²)` 拼接，取累积和，再以 `M*Σf_tf_t'` 计算 trace。它返回统计量及稀疏 `crit95` 表，**不返回 p 值，也没有 HAC、GARCH-t 拟合或参数自助校准**。常规源码使用矩阵逆；任何 singular-score 处理应遵守已冻结设计，不能从此引用推定自动可用。

本 C2 使用的是 **Hansen-type joint OLS score statistic with fitted-null AR–GARCH–t parametric-bootstrap calibration**：保留成熟统计量，另用固定的稳定模型和 999 次 bootstrap 得到一个全局 p 值。其参考分布不是 Hansen 已发表临界值；须在 bootstrap 样本重走与观测样本一致的 OLS / score / 统计量链。此校准依赖拟合零假设，不是 finite-sample exact 5%，也不直接检验 GARCH 每一参数的所有变动方向。t/GARCH 高阶矩不足、模型错设和近单位根边界继续保留；拒绝解释为拟合稳定零假设下的筛查证据。

## Yao 与 Bai–Perron 能支持到哪里

Yao, Y.-C. (1988). **Estimating the number of change-points via Schwarz' criterion**. *Statistics & Probability Letters*, **6(3), 181–189**. DOI [10.1016/0167-7152(88)90118-6](https://doi.org/10.1016/0167-7152(88)90118-6)。[出版社原文页面/摘要](https://www.sciencedirect.com/science/article/pii/0167715288901186)核实其对象是 **independent normal sequence**，结论是该 Schwarz 型断点数估计的 weak consistency。本轮 DOI/正文直接访问有 403，但可核实出版社索引的摘要；没有声称通读证明，更不能将该一致性结论直接套到本任务的 AR–GARCH–t 数据与分段方差 QML。

Bai, J., & Perron, P. (2003). **Computation and analysis of multiple structural change models**. *Journal of Applied Econometrics*, **18(1), 1–22**，DOI [10.1002/jae.659](https://onlinelibrary.wiley.com/doi/10.1002/jae.659)。其 §3 支持利用可加分段 cost、最短段约束和动态规划搜索多断点的成熟计算思想；其特定 SSR、协方差处理和推断理论不自动证明所有 Gaussian-QML / BIC 变体。本文前一份 `literature.md` 已记录其 trimming 与串行相关警戒。

本设计的独立段 AR(1) 均值加独立段方差，若有 `k` 个断点，每段计截距、斜率、方差三个参数，共 `3(k+1)`，再按本设计计 `k` 个断点位置，得到 **`(3+4k) log M`** 惩罚。这个计数是本任务冻结的 **descriptive BIC-style penalty**，不是宣称它就是 Yao 或 Bai–Perron 原定理的完整准则。全局 raw 5% screen 未拒绝则设 k=0；拒绝后在 k≤2、固定最短段约束中作 Gaussian-QML+BIC 动态规划定位，所得日期是条件性的描述性估计，不能标成独立显著的断点或附会 95% 日期保证。

## 核对边界

本文件来源仅为 Hansen 作者原文、期刊原元数据/摘要、官方 statsmodels 源码和此前已核读的 Bai–Perron 出版社全文。没有新增实证发现；没有据此次补核改动已经冻结的任何方法规则或阈值。
