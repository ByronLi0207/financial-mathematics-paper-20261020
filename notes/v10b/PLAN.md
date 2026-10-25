# v10b 投稿写作与版式执行计划

Goal: 3小时内，纯文档打磨，固定科学结果。Base23fd9fa；branchrevision-v10b。
Architecture: canonical投稿文件仍在submission-v10/，其git分支隔离v10b；results/data/protocol全部SHA封存不可改，图表显示稿仅在submission-v10/生成。只读成本网格脚本/输出在notes/v10b/。
Spec: 用户本轮0–8详细步骤；不等确认，保守决定记PENDING。
Approach: 保留原原生TeX工作流，用现有归档与成熟出版规范校文，三位同模型助手分工只读成本/显示样式/supp，根统一主稿、letter、作者指南和验收。不实验，不新模型，不改归档。
Review focus: M2未过阈值不能证明无效应；成本计数只读取已有点；同一结果数字最多两次（结果表一次+摘要或结论一次，结构索引/定义/日期另记）；图表显示值前后逐项比较；仅新branch发布，研究历史与网页历史区别保存。

- [x] 0 基准/新branch/科学SHA/旧refs保护；5min。
- [x] 1 核对摘要每句原文/归档，<=180words/8numeric tokens、三个发现、末局限；25min。
- [x] 2 只读归档成本方向及中心/反角3点，脚本输出+四处统一；25min。
- [x] 3 五处三发现同顺序，RQ1–3逐一回答；30min。
- [x] 4 第1–9节逐段过渡/重复数字，写法同checker前后；40min。
- [x] 5 图表显示样式/字号/单位/色盲/对齐/注<=3句，数值绑定；30min（独立助手与写作并行）。
- [x] 6 Supp目录/正确交叉引用/审计移文档/<=33页；20min（独立助手并行）。
- [x] 7 官方JoF指南/<=6keywords/<=40runningtitle/声明链接v10b/refs/letter1page/保留占位；15min。
- [x] 8 全套测试/四PDF重编译全页渲染看过/数字核对/main20supp33/仅v10b发布/最终树相等/交付；10min（实际需为测试发布预留）。

Ruling: 阶段分钟建议总和超过180min，独立显示/补充检查并行，不删任务。保留主稿数据与定义数字的必要重复，结果数值按语义定位和显示精度核查；发现无法兼容时记录明确处理而非悄悄漏报。

本地最终验收：19/32/1/1页，53页全部逐页看过；最后main4/11/12/title1重看，其余PNG逐张SHA相同。现有1715 tests+1181subtests通过；2077tracked与55520全部本地science文件均未改。仅新branch远端发布/树核对待完成。

首轮97文件/6批远端完整tree已核验，final-check各门槛PASS；最终仅元数据发布/branch对齐回执另存本地，科学与论文内容已冻结。
