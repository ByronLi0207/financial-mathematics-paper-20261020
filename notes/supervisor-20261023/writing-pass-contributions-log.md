# 贡献说明写作修订记录（2026-10-23）

范围：只改 `notes/supervisor-20261023/CONTRIBUTIONS.md`；论文正文、代码、结果、图和 Git 均未由此任务修改。依据为本轮已保存的摘要、引言贡献段和原结果；未新增拟合、计算或分析。

| 段落 | 原首句 | 新首句 | 删减或移动 |
|---|---|---|---|
| 定位 | 这是采用成熟方法的实证比较与模型验证论文。 | 这是采用成熟方法的实证比较与模型验证论文。 | 随后直接写“历史规则很难打败”的三点主线；保留文献核对范围。 |
| 第一项中文一句话 | 将预测对象统一为包含当前持仓的双侧绝对采样峰值，并匹配完成标签、历史长度和更新安排后，条件模型的增益随数据与设定而异，不能由端点预测的成功直接推出。 | 预测双侧绝对持仓峰值时，FX 回归在原期和更早期分别比匹配历史规则降损 14.8% 和 16.6%，但更早期比短历史滚动规则增损 3.2%，原来相对该滚动规则的收益没有复现。 | 将原第二项的更早期 FX 证据移到第一项；明确 matched 与 rolling 两个固定参照。 |
| 第一项英文一句话 | On a common sampled absolute-position-peak target, comparisons with matched completed-label histories and refit schedules show that conditional gains depend on the data and specification. | Historical rules are a hard benchmark for sampled position peaks: FX regression lowers matched loss by 14.8% in the original period and 16.6% in the earlier period, but its earlier loss rises 3.2% against the short-history rolling rule, reversing the original comparison's gain. | 先给发现，再给数字；保留原峰值目标、文献证据和非因果范围。 |
| 第一项证据 | 目标是 \(P_{t,H}=\max_{0\le h\le H}\|N_{t+h}\|\)，不是 \(N_{t+H}\) 的区间；FX 的 H6/W2880 匹配历史比较相对 frozen F 降损 **14.767%**，原 Treasury H6/W260 则增损 **50.786%**。 | 目标是 \(P_{t,H}=\max_{0\le h\le H}\|N_{t+h}\|\)，包含当前持仓；比较匹配已完成标签、历史长度和更新安排。 | 原 Treasury 50.786% 移到第二项；保留 FX 14.767% 与正文 14.8% 的显示对应，保留所有文献和链接。 |
| 第二项中文一句话 | 扩大岭惩罚菜单缓解周度恶化，但在这次短周度验证和评估中，包括 one-SE 在内的选择规则仍未稳定守住历史基准。 | 周度 Treasury 主比较增损 50.8%，扩大岭惩罚菜单虽减小损失，12 条附加序列仍有 34/48 格败给历史 headroom，而另一个涵盖 13 条周度序列、26 格的更早期测试中，保守选参仍留下大额损失。 | 把 12-series/48-cell panel 与 13-series/26-cell selection test 分开。 |
| 第二项英文一句话 | Expanding the ridge menu mitigates weekly deterioration, but selection on the short weekly validation samples, including a paired-loss one-SE rule, does not reliably preserve the historical benchmark in the subsequent evaluation. | Weekly regression loses 50.8% in the Treasury main comparison, and wider penalties leave 34 of 48 cells across 12 further series behind historical headroom, while conservative selection still permits large losses in the separate earlier test of 26 cells across 13 weekly series. | 避免把原主比较损失扩大为所有 conditional methods 都输。 |
| 第二项证据与实务范围 | 原 Treasury primary 的超额损失由 50.8% 降至 3.4%。 | 原 Treasury H6/W260 回归相对匹配历史规则增损 50.786%，对应正文的 50.8%；扩大菜单后为 3.4%。 | 保留原所有 panel 负预测、保守规则的三项失败标准和全部数值；用描述性名称代替逐数字附带的内部代号。保留 I/rank、重叠标签、无独立复制及无切换阈值说明，并指出部分 expanded regression 和 AR 有收益。 |
| 更早期 Treasury | 更早的 2015 年 FX 比较还说明参照不能混用。 | 更早期 Treasury H6/W52 短窗口版本增损 144.3%，延续原比较的恶化方向。 | FX 证据已移第一项；W52 不能替代 W260 的范围及原结构结果链接仍保留。 |
| 第三项中文一句话 | 在这些归档预测中，较低的 0.95 pinball 损失可以伴随更多破线，且分数偏好的改变会改写排序，因此模型结论须同时报告误差金额、破线次数和评分敏感性。 | 较低的 0.95 pinball 损失可以伴随更多破线，FX 主比较为 376 对 332、匹配比较为 376 对 360，模型评估因此须同时报告误差金额、破线次数和评分敏感性。 | 直接并列两组 breach 的参照口径；保留 1.83%、20.6、Murphy 曲线交叉及原链接。 |
| 第三项英文一句话 | In these archived forecasts, lower 0.95 pinball loss can coexist with more breaches and score-dependent rankings, so forecast assessment must jointly report error amounts, breach occasions and scoring sensitivity. | Lower 0.95 pinball loss can accompany more breaches, with 376 versus 332 in the FX main comparison and 376 versus 360 in the matched comparison, so forecast assessment should report error amounts, breach counts and scoring sensitivity together. | 移除不影响结果的过程修饰，保留 fixed-report weights 与 fixed-quantile Murphy 的区别。 |
| 审稿质疑与“不是创新” | 增量是目标、比较控制和上述三项带数字的发现。 | 增量是目标、比较控制和上述三项带数字的发现。 | 保留四项质疑、既有方法归属、原 FX inspection、2015 的本项目核对范围、两条失败预测和经济价值边界；缩短数字后反复附带的过程文字。 |
| 待用户决定 | 仅提供标题备选，正式标题未改。 | 标题备选，待用户决定；正式标题未改。 | 用两个体现“历史基准难打败”的候选替代旧候选；补记图内旧标签冲突及原图字节保留、正文描述性名称、Appendix C 表映射的处理。 |

旧标题备选（仅作修改历史，不再列为当前待选）：*Forecasting Sampled Position Peaks: Stronger Shrinkage and Persistent Benchmark Gaps*；*Conditional Position-Peak Forecasts: Shrinkage, Historical Rules and Breach Risk*。

检查：原 14 个链接定义全部保留；三条中文与三条英文一句话均在；原全部 panel 负预测、保守选参失败、+144.3% 短窗口结果和 +3.2% FX 反转仍在。此记录只说明该贡献文件的改写，不代表论文最终稿已经完成全稿核查。
