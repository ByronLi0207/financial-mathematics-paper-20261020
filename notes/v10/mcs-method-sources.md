# E3 MCS 方法来源核对

核对日期：2026-10-24 UTC。核对发生在 E3 设计独立提交及任何 MCS／缺失逐点损失派生之前。只使用论文作者所属机构、出版者条目和软件作者官方文档／源码；没有新增金融数据。

- Hansen, P. R., Lunde, A., & Nason, J. M. (2011). *The Model Confidence Set*. **Econometrica**,79(2),453–497. DOI:10.3982/ECTA5771。作者机构 [Aarhus University 条目](https://pure.au.dk/portal/en/publications/the-model-confidence-set/) 核实作者、年份、卷期、页码、DOI；[出版者 DOI 条目](https://doi.org/10.3982/ECTA5771) 的索引亦一致。直接抓取出版页遇超时／重定向限制，没有把它说成完整全文已阅读。MCS 将多方法比较表达为一个不能排除的集合；数据不足以区分时可保留多种方法。本文采用这个成熟工具，不提出新检验。
- [arch8.0.0 官方 API 文档](https://bashtage.github.io/arch/multiple-comparison/generated/arch.bootstrap.MCS.html) 核实 losses 为T×k矩阵，支持R／max统计量、stationary／circular／moving-block bootstrap、明确block_size、replications和seed；本轮固定R、stationary、1000次、size.10和自定预置block规则。库默认的sqrt(T)块长没有被误称成本轮的cube-root规则。
- [arch8.0.0 官方实现源码](https://bashtage.github.io/arch/_modules/arch/bootstrap/multiple_comparison.html) 核实输入至少两列、按消去顺序产生单调p值，以及 included 采用Pvalue>size、excluded采用<=size。完全重复损失列需先合为等价类，再将结果展开到所有不同程序；只剩一个唯一损失列时，明确作为精确相同损失的解析情形处理。没有把多份等价标签当成独立证据。

`arch.readthedocs.io/en/latest/...` 在查询时显示7.2.0；实际临时运行环境固定arch8.0.0，因此采用其对应的作者官方GitHub Pages文档及源码。直接核对版本优先于“latest”字样。

预置块长max(H,ceil(n^(1/3)))是透明的固定经验规则，不声称最优。Stationary bootstrap 的依赖近似不能自动消除非平稳、既往查看、相关合约或重复窗口问题。输出保留这些解释边界、失败格和完整分母；不把MCS成员身份当作未来覆盖或真实经济价值保证。协议为 `protocol/v10/mcs-design.md`，设计提交 `78ea93493379ab3a93459d28e1bab84200f01539`。
