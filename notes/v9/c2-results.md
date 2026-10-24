# C2 结果、前提纠正与报告层故障记录

设计单独提交：`5decccb0a13ef1969629cfec695dd3459c412c4e`，2026-10-24T18:38:37UTC（11:38:37PDT）。第一次实际诊断：2026-10-24T19:08:52.012080+00:00。正式预测：2026-10-24T19:10:05.397496+00:00，已存completion耗时328.849364秒。两次试跑完成后，按耗时规则单独提交`3411a1f`选择R32、QR33及QR4；没有按结果调整规模。

全部416个正式worker任务退出0。ZIP审计4990个方法完成、2个失败；13303个候选完成、9个失败；F52格均32/32完整。104个配对条件格为102完成、2失败。具体库存由`results/v9/nonstationarity/audit/summary.json`提供，失败不补跑。

| 预测 | 判断 | 直接依据 |
|---|---|---|
| N1 | SUPPORTED | raw拒绝7/13；Holm13拒绝2/13 |
| N2 | UNASSESSABLE | W52切换中位数+121.400980%；W260必须的PDPOSTIPS-G11/QR33在rep24失败 |
| N3 | NOT_SUPPORTED | W52恒定控制中位数+116.243280%，不在预设±3%内 |
| N4 | UNASSESSABLE | 日频矩资格不足；小时拟合不收敛；保留未知状态 |

## 任务前提的事实纠正

PR5 WP3已保存的QR33/H6原表，在W52及W260均已有正的损失变化；完整范围和原行在`prior-stationary-reconciliation.json`。旧v8的D0/D2近持平来自另一菜单、weekly特征/时钟、校准与汇总口径。不得沿用“两次平稳模拟都不能产生损失”或把不稳定性写成损失的必要原因。N3的新反证进一步要求修改C1主线和C3第三条发现。

## 冻结runner的报告层错误

正式forecast和原ZIP结束后，runner在写`predictions.json`时因NumPy整数无法JSON序列化退出1。`summary.json`已完整写出；原`predictions.json`不完整。原文件、错误stdout、全部ZIP和loose回执全部保留。没有重跑forecast、诊断、拟合、随机路径或候选。

`finalize_v9_archive.py`只从原ZIP收集回执，并调用原封存的纯汇总函数；NumPy标量用`.item()`转换为同值原生标量。它exclusive写独立`postrun/`，复制的manifest/diagnostics/summary与原件逐字节相同。坏文件没有覆盖。原报告错完整保存在`postrun/original-reporting-error.txt`，源stdoutSHA256为`6ce1afe17f68bda5863b25aacf723f30ec038f85efaf6940616c53eadd69dd26`。

序列化回归先RED（2失败），再GREEN（2通过，1.29秒）。封存driver未变，修复只在独立报告层。归档报告器与ZIP/F审计器互相核对，104格完成数、全部完成格中位数、52个F格、全部SHA均通过。更早完整prelaunch suite为1448passed、1068subtests；C7另跑包含归档工具的全套。

## 解释与图检查

N1是拟合稳定零假设下的原始点位拒绝数；Holm后只保留2条。描述性BIC分段不等于每条断点的显著性结论。矩资格和边界拟合不能证明真实模型正确。C2的循环排程及last→first人工转移已归档。

报告图已打开目视检查：W52两个已知点、W260两条明确不可评估标记，未用12个完成来源补13来源汇总。图没有裁切或文字重叠。C4将用同一归档生成正文双栏图，保留这些缺失。

## 待用户决定

- PR #3、#4、#5日后如何处理；本轮不关闭、不合并。
- 作者、ORCID、资金、利益冲突和AI声明等保留占位，投稿前由作者确认。
