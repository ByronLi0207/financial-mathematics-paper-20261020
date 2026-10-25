# v10b 三发现与成本措辞一致性只读核对

核对时间：2026-10-25 04:03 UTC。范围仅为当前 `submission-v10/manuscript.tex`、`submission-v10/cover-letter.tex`，以及主稿实际引用的三张生成表；以既有 `notes/v10b/cost-reading.json` 为成本读出依据。没有新分析、没有更改正文、生成表或任何科学归档。

读取快照 SHA-256：

|文件|SHA-256|
|---|---|
|`submission-v10/manuscript.tex`|`419e0011bb9f2c702c9e5bbd7bf7c2cd8a8cda456c0681059fc5cf2fa6e66344`|
|`submission-v10/cover-letter.tex`|`070ee95c23440eef9d8dc6122fe2181d1cdb57380090e81fc79a8d7b07673843`|
|`notes/v10b/cost-reading.json`|`e21af04506bb34d9ebe6c5de294d943bc7415d9adf4d6ae48f903dec389add7b`|

结论：没有发现需要立即纠正的结果数字错误、方向反写、M2 等价推论或 MCS 最优性推论。五处核心三发现次序一致；成本正文解释恰为三句。两处小幅用词精确化建议列在后面。

## 五处三发现顺序

固定核对次序是：①匹配 FX 收益重现，但与较短滚动参考的排名会变；②历史规则在周度/独立报告系统中仍有竞争力，校准模拟中的大损失对惩罚菜单敏感且 M2 未获支持；③CFTC 回归成本优势较常出现在较高预留系数、较低固定破线系数一侧，存在局部例外。

|具体位置|已符合内容|判断|
|---|---|---|
|`manuscript.tex:17` 摘要|明确 First / Second / Third；FX 收益及参考变化 → NYFed/CFTC 历史优势、MCS 共存和菜单模拟/M2 → 成本方向。结尾保留回溯性质及原始 FX 时段预先查看的限制。|符合。成本方向用 generally，没有写成严格单调。|
|`manuscript.tex:43–47` Introduction 三贡献|三个斜体首句依次覆盖同一三发现；第二项的模拟解释限定在 calibrated simulations，第三项明写 local exceptions。|符合。|
|`manuscript.tex:80` §2 结尾|FX reference → weekly historical controls / expanded simulation menus / unsupported switching increment → CFTC higher reserve / lower fixed breach / local exceptions。|符合。文献定位后的研究落点保持原顺序。|
|`manuscript.tex:335–339` Conclusion|RQ1、RQ2、RQ3 按相同顺序逐个回答；RQ2 保留 empirical low-frequency mechanism remains unidentified；RQ3 保留 local exceptions。|符合。没有另塞第四个发现，也没有新增结果数字。|
|`cover-letter.tex:10–12`|首句以三个并列分句依次给出 FX、周度历史控制、CFTC 成本方向；下一段补充模拟/M2 与期刊定位。|符合。后段补充第二发现是解释性展开，不是重排三发现。|

## M2、MCS 和成本方向边界

|具体位置|原文判断与既有证据|判断|
|---|---|---|
|`manuscript.tex:17,45,80,337`；`cover-letter.tex:12`|都写 registered switching increment is unsupported，未写 no switching effect。既有 `cost-reading.json#/abstract_checks/menu_and_M2` 绑定的 M2 为 −0.43471629487539243 个百分点，相对注册 +5 点门槛未获支持。|符合。|
|`manuscript.tex:272,274,282,325`|说明菜单与 exact-tie rule 的完整程序改变；有限惩罚和 I 的贡献不单独识别；near-parity 不证明特征增值；无五点增量不证明等价；经验因果机制仍未解决。|符合，因果和等价边界完整。|
|`manuscript.tex:17,45,254,337`|MCS 采用 usually / most，并保留 alongside alternatives；254 行明确 Non-elimination does not establish equal predictive risk。|符合。既有读出是 90/98，而非 sole historical winner。|
|`manuscript.tex:183–185,329`；`generated/v10-mcs-main.tex:16–18`|保留 bootstrap 假设、研究阶段选择限制、相关任务非独立、无 future coverage / simultaneous best-model 认证。表区分 sole literal method 与 sole loss class。|符合。|
|`manuscript.tex:17,47,80,295,339`；`cover-letter.tex:10`|全部是较高 reserve、较低 fixed breach 一侧较有利，使用 generally；摘要以外的各处明写 local exceptions / not monotone。|符合只读网格方向，无反写。摘要 generally 足以避免声称无条件单调。|
|`manuscript.tex:297,323,329`|成本是 illustrative 而非 observed；不推 funding return、optimal intervention 或 trading profit，归一化 ex ante 应用仍未检验。|符合。|

## 成本小节恰三句及三点绑定

`manuscript.tex:286–301` 的公式后、图之前，解释正文就是以下三句（295、296、297 行）；公式和图注不算解释正文句数。

1. 295 行给方向，含 generally 与 grid is not monotone。
2. 296 行固定 `c=1`，给三个实际归档点及计数。
3. 297 行说明 illustrative / not observed operating costs，并引向补充材料 S32。

|主稿296行点|主稿结果|既有读出字段|判断|
|---|---:|---|---|
|`(.1,.25)`|`5/34`|`cost-reading.json#/examples/0`，selection=`sorted_position_center`，kappa=`0.1`，beta=`0.25`，strict_cheaper_count=5，complete_denominator=34|一致。|
|`(1,0)`|`32/34`|`#/examples/1`，selection=`higher_reserve_lower_breach_corner`，strict_cheaper_count=32，complete_denominator=34|一致。|
|`(.01,5)`|`1/34`|`#/examples/2`，selection=`lower_reserve_higher_breach_corner`，strict_cheaper_count=1，complete_denominator=34|一致。|

三个点在 `cost-reading.json` 均保留 primary CSV 与 ZIP member 的34条行号，逐条字段相同；计数来自 archived `cheaper=True`。分母为17个合约 × 两个历史长度，等价记录为零。主稿没有把这些相关任务解释为独立样本概率。

## 需精确化的两处小修

这两项是可直接采纳的编辑建议，不是结果错误，也不应引入新分析或增加成本解释句数。

|位置|建议|理由|
|---|---|---|
|`manuscript.tex:296`|在现有第二句内，把 `regression is cheaper in ... at ...` 改成 `regression is strictly cheaper in ... at the sorted-grid centre ...`，并可把 `across the 17 contracts and two histories` 放进同一句。|目前数字完全正确，但正文没有把 `.1,.25` 明确标成按排序位置选的中心，也没有在此处说明34的构成。用一个短语补足与只读选点规则的直接对应；保持整节恰三句。|
|`manuscript.tex:17`|Second 的 `historical rules beat regression` 可改成 `historical rules beat expanded regression`。|34/48 的 NYFed 数字来自 expanded-penalty full regression（正文表234行），CFTC 也使用扩展菜单。补充 expanded 可避免读者误认为同一计数属于原始窄菜单；不改变数值或摘要数值词元数量。|

## 同一实证结果数字的重复

按结果身份和精度核对，而非机械地把每个相同数字当成重复。没有发现同一实证结果在当前主稿和所含表中出现三次以上、必须删减的情况；Introduction、§2、Conclusion、letter 的结果性叙述已基本改为定性。

|同一结果|实际位置与重复次数|判断|
|---|---|---|
|匹配 FX 后期损失降低14.8% / 14.77%|摘要17行；FX表204行|两次，分别摘要与结果表，符合。|
|匹配 FX 前期损失降低16.6% / 16.62%|摘要17行；FX表206行|两次，符合。|
|NYFed 扩展全回归高损失34/48|摘要17行；周度表234行|两次，符合。|
|CFTC 历史规则低损失29/34|摘要17行；244行|两次。合约表展示逐合约损失，没有再次印29/34；表注30行的34只是同一设计分母，不构成第三次29/34结果。|
|模拟恒定组原菜单116.2% / 116.24%|摘要17行；`generated/v10-menu-main.tex:8`|两次，符合；near zero 是定性压缩，不应误计为第三个数值呈现。|
|MCS 90/98、sole method 2/98、conditional excluded197/683|`generated/v10-mcs-main.tex:13`|主要数值只在结果表；正文及摘要使用定性叙述，符合。|
|成本5/34、32/34、1/34及其三个点|296行|每个结果一次。成本图展示相同固定网格是图形证据，不是多处重复抄写同一结果数字。|
|FX未包裹回归376次 breaches|表203、204行|同一个回归预测对两个不同历史参考，分别376/332与376/360；重复376是行自足所需，不应删除一行或合并为无参照含义的数。|

以下相同数字应保留并区分：17是合约数量或独立的“17 of 26选择截距”结果，34可为CFTC分母或NYFed胜负分子，260可为历史长度或评价起点数量，52可为历史或验证长度，6/24是结构性horizon，32在模拟为重复次数、在成本为严格较便宜计数；这些不是同一实证结果的冗余复述。阈值5个百分点、成本c=1、菜单中的惩罚系数、交叉引用、日期及bibliography页码同样不适用结果数字删重。

审查交付仅为此文件。没有修改主稿、letter或科学文件；没有跨模型复审。
