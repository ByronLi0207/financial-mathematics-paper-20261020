# v8 三条经验发现（B3 定位稿）

这篇论文的贡献放在同一峰值目标下的比较发现；目标定义、成熟标签、地板投影和经典 Lévy 界作为必要背景。

**First：FX 的同历史优势跨两个时期出现，但对照选择仍改变排名。** 长历史、六步 QR 相对同历史固定 headroom 规则，后期和早期损失分别降低 **14.8%**、**16.6%**；延迟校准后，后期优势仍为 **15.0%**，破线数 **329 对 328**（Table 3）。相对原短历史滚动对照，后期降低 12.7%，早期却增加 **3.2%**。因此可报告匹配优势的时期稳定性，不能报告对所有历史规则的稳定优势；两个时期仍来自同一条熟悉的 FX 记录。

First, long-history regression lowers matched FX loss by 14.8% and 16.6% across periods; calibration retains the later-period 15.0% gain with 329 versus 328 breaches (Table 3).

**Second：周度汇总头寸中，扩大正则化和保守选参没有守住历史基准。** 原 Treasury-bill 对比中 QR 损失增加 **50.8%**；扩展 ridge 菜单后的附加面板仍有 **34/48** 格输给匹配历史规则；一标准误规则在早期周度格的最差超额损失达 **181.4%**（Table 4；Supplement selection tables）。这些结果支持把历史规则作为这组短周度样本的严格基准，不是“条件模型永远无用”的结论，也不是独立交易商复制。

Second, historical rules beat expanded-menu regression in 34 of 48 weekly comparisons; conservative selection still permits a 181.4% worst excess (Table 4).

**Third：较低平均分数与较少破线、跨评分偏好的优势可以分开。** 未校准的匹配 FX 比较中，QR 虽降低平均损失，破线仍为 **376 对 360**（Table 3）。另行指定的原 FX 和 Treasury 对比，其 elementary-score 曲线都交叉（Figures 2–3；Table 5）。这是本任务中具体的评价分歧；联合报告分数与覆盖以及 Murphy 方法本身已有成熟文献。

Third, matched FX regression lowers loss but breaches 376 versus 360 times, while the original comparisons have crossing elementary-score curves (Table 3; Figures 2–3).

**最近文献与边界。** Wisniewski et al. (2020) 及 Wisniewski (2024), Chapter 6 已研究同源市场做市商的 signed endpoint intervals 并联合报告分数与覆盖；MaxVaR 和 van den Hoogen 的既有阅读记录提供不同路径风险目标的前例；Ehm et al. (2016) 提供一致评分及 elementary-score 工具。本稿保留这些前例，不声称上述工具、路径风险或联合评价的首创。van den Hoogen 未核实的具体维度以“—”处理。

**模拟的地位。** v8 校准模拟作机制探索和失败证据：P1/P3 不支持，P2/P4 因必要格失败无法评估，七个失败格完整保留；不把它列作第三条贡献或宣称确认真实数据机制。

Section 3 defines the target and records two elementary properties used later.
