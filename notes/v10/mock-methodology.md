# v10 方法学模拟审阅：同模型内部意见

身份与范围：本备忘录明确是 **SAME-MODEL INTERNAL method review**，按 Journal of Forecasting 的方法学读者视角提出意见；不是该刊真实审稿、编辑决定、独立复制或跨模型审查。Claude/Cloud 未启用。只读当前 NEW 稿件、E1–E4 冻结设计、已保存汇总报告及主数字来源审计；没有读取金融向量、重算数值、运行模型/实验或改动稿件与代码。本文恰好提出以下五项主要意见。

审阅快照：`submission-v10/manuscript.tex` SHA256 为 `39fc54af093c0367f7877aa96b3b8f8c742f16ca076ec8ab31cfd9d7ea2ec672`；`submission-v10/supplement.tex` 为 `78be8bd270aeb5061d57f6796d8906019573ba765a37b3edf7711f40e2a92e0b`。下述行号以此快照为准。E5 的来源审计 PASS 解决数值绑定问题，不替代以下解释与推断问题。

## V10-M1 — 将 MCS 的未淘汰、精确样本损失相同和统计等价分开，并把名义推断的条件放在结果旁边

**当前定位。** 主稿 `sec:evaluation` 的 multiple-method 小节第 183–185 行给出 MCS 配置；`sec:results` 第 266 行写 “leaving many alternatives statistically indistinguishable”。补充材料 `sup:v10-mcs` 第 1531–1533 行区分程序标签、精确损失类和条件方法 slots；主稿 `sec:limitations` 第 334 行才集中说明 dependence 和研究阶段选择限制。冻结来源为 `protocol/v10/mcs-design.md` 第 7–17 行及第 165–199 行；汇总来源是 `results/v10/mcs/report-note-zh.md`。

**为何是主要问题。** 该 MCS 的方法池是冻结 registry 中已经完整执行的选择程序，包括选择规则与组合，并不是所有研究阶段曾考虑过的规格。它在这个池内处理多方法比较，不能倒推覆盖此前规格开发/研究搜索的全部不确定性。精确相同的完整样本 loss 列允许稳定地执行并展开 library 结果，但不证明总体预测风险相等；不同容量也可能碰巧给出相同样本损失。反之，未被 MCS 淘汰并非等价检验通过。“statistically indistinguishable” 容易把未拒绝提升为等价证据。固定 block heuristic 至少覆盖标签 horizon，仍不能仅凭此确认滚动估计、共同冲击及潜在制度变化下的 loss dependence 足以支持名义 90% 解读。不同 cell 的程序池大小和成员结构又不同，因此 197/683 是完整条件程序 slots 的描述性淘汰比例，不是独立模型/市场的共同拒绝率。当前稿已有相应限制，但主要结论处的词义仍强于设计支持。

**可执行写作修正。** 将第 266 行替换为类似：

> Under the prespecified stationary-bootstrap implementation, many saved procedures are not eliminated from the candidate set; this is not evidence of equivalent predictive risk. The 90/98 and 197/683 figures describe related comparison grids and procedure slots, respectively.

在第 183–185 行紧邻配置再说明该 90% 是依赖于适用 loss-process 条件的名义程序水平，块长是未由结果挑选的 overlap-bounded heuristic；MCS 不调整研究开发时已发生的规格选择。主文紧凑表应保留程序数与唯一损失类的区别，并将精确样本等值称为 “exact observed-loss equality”，不能简称总体 equivalence。

**未解决科学边界。** 当前材料没有证明这些金融 loss 过程满足足以保证该 bootstrap 近似精度的条件，也未给出块长稳健性或等价/非劣效分析。可保守解释现有结果；不能靠改写补出这些证据，本轮也不应为审阅追加计算。

## V10-M2 — 配对实验识别的是包含 I 的候选菜单变化，不是条件信息价值或一般频率机制

**当前定位。** 摘要第 17 行称 “Paired simulations isolate the penalty menu”；主稿 `sec:extensions` 第 274–281 行及 `fig:mechanism` 将菜单改变与损失消失相连；第 144 行限定 full regression 的菜单改变。补充材料 `sup:v10-menu` 第 1508–1510 行披露 QR4 tie、I、继承的 hourly feature clock 和 W260 失败。冻结设计 `protocol/v10/menu-isolation-design.md` 第 3–20 行、第 141–149 行与第 181–190 行；保存报告 `results/v10/menu/report-note-zh.md` 记录 exact ties=0、changed QR4 tie selections=0。

**为何是主要问题。** 保持原校准、种子、路径和时钟的配对控制是强项，足以比较这两个已经定义的程序。但 full QR33 同时增加较强的有限惩罚及精确的无斜率 I 候选；接近历史规则的结果可能来自允许退回非条件基准，并不表明 33 个条件变量开始提供预测价值，也没有把有限正则化与加入 I 的贡献分开。I 又不是 corrected-rank F，不能将接近 F 写成精确回到同一 benchmark。QR4 另外有 tie 约定变化，虽保存结果证明它没有改变本次实际 tie 选择，也不能把设计层面的变化删除。旧长历史 mandatory failure 在新菜单中保留，所以新结果仍不是对所有 histories 的完整机制解释。稿件已承认非字面周历及经验机制未识别，但摘要和图题最容易被单独引用，需在此层面锁住范围。

**可执行写作修正。** 在第 274–276 行紧接配对结果加一句：

> The expanded procedure can shrink all the way to the ordinary empirical rule I. The paired contrast identifies the effect of this candidate-set change on the fixed calibrated paths, without separating finite-penalty regularization from access to I or establishing additional predictive content in the conditional features.

摘要可用 “On fixed calibrated paths, allowing stronger penalties and I removes the large short-history loss” 替代孤立的 “isolate the penalty menu”。保留 QR4 的 stronger-tie 改变和零实际影响说明；M1–M3 只对应 QR33，不能让 QR4 或缺失的 W260 结果借用该判定。图题应明确 “short-history full-regression” 的作用域。

**未解决科学边界。** 在既存设计下，有限惩罚与 I 候选的独立因果贡献、真实金融中的频率机制以及 W260 的全来源结论均未被识别。若稿件不声称这些，当前固定路径证据可以保留；不应在修订中悄悄补一个有利分解或成功子集。

## V10-M3 — 短重叠验证只能支持特定选择程序的表现，不能把 F/I 家族事后胜出直接转成 F 的普适部署建议

**当前定位。** 主稿第 171 行写 weekly selection 使用 52 个重叠 validation origins；第 148 行压缩介绍 finite delayed ACI；`sec:results` 第 222 行、256 行及 `sec:implications` 第 314 行连接短样本选择、F/I 胜出与 corrected-rank F 的 default benchmark 建议。补充材料 `sup:selection` 第 678–691 行说明 one-SE 不覆盖整个选择不确定性；`sup:v10-cftc` 第 1520、1525 行给出 maturity gap 和 ACI 简介；第 1438–1448、1495–1504、1510 行保留旧失败/负面结论。E2 协议第 15–19 行、第 220、234–237 行给出 F/I ranks、gamma、warmup 和跨 gap state。

**为何是主要问题。** 稿件当前把训练窗口 W、外层 validation 长度、H-delay label maturity、refit 时钟以及 ACI 的 warmup/state 都分散在不同位置。对尾分位数而言，52 个带重叠标签的 origin 不能视作 52 个独立校准误差；33 维条件程序与多个 penalty/gamma 的选择更不等于得到稳定最优程序。延迟与 gap 的正确处理避免了直接使用未成熟评价标签，但不会自动使短 CV 稳定，也不会创造覆盖保证。此外 CFTC 的 29/34 是预先定义的 `min(F,I)` 家族描述：其中任一事后平均损失较小即计胜，不是已经验证的、可在 issue time 选择 F 或 I 的实际规则。MCS 的 F/I membership 同样不能专门证明 corrected-rank F 优于 I。现有 ordinary-rank 消融本身也保留混合 loss 方向，旧负面实验不能被新菜单的近零短历史结果覆盖。

**可执行写作修正。** 将第 314 行的建议明确为“mandatory matched benchmark”，不是经确认的最优部署规则，并在第 256 行附近注明：

> The 29/34 count is a descriptive comparison with the better realized score among the two prespecified historical reports, not the performance of an implementable selector between them. F remains the fixed matched reference; I is reported separately.

在方法或补充材料增加一个紧凑的现有设置说明：分别列 W、validation/evaluation origin 数、H、refit step、validation-label maturity gap；ACI 另列 gamma 按 coverage-first 选择、最少 mature warm scores、validation→evaluation state 的延续且 gap 中无虚构 issue。只转录冻结协议，不改选择或重新 CV。结果讨论应把“较长外层验证未检验”和旧失败/负面结论放在推荐句附近。

**未解决科学边界。** 更长外层验证下的稳定性、F 相对 I 的一般优势以及可执行历史家族 selector 的表现均未检验。保存 mature-label 时序是程序合法性的证据，不是这些科学命题的证据。

## V10-M4 — F 归一化网格是相对偏好图；同一 beta 跨 cell 不代表相同实际 breach charge，且固定比较不是可达成本前沿

**当前定位。** 主稿 `sec:cost` 第 290–305 行定义 `m_F`、`beta=b/m_F`、固定 expanded QR33 比较及图中的组级分数；第 334 行给出 illustrative-cost 限制。补充材料 `sup:v10-cost` 第 1539–1541 行说明所有完整方法、正尺度、完整区域与 floor recovery。冻结协议 `protocol/v10/cost-design.md` 第 3–7 行、第 50–66 行；保存报告 `results/v10/cost/report-note-zh.md`。

**为何是主要问题。** 用同一 cell 的正 F headroom 归一化有明确维度意义，且 pinball 对应点的恒等式有助解释。但 mF 来自整个已评估 origin grid，而每个 source/H/W 的尺度不同；固定同一 beta 就是在每个 cell 采用不同的实际 charge `b=beta*mF`。因此图是“相同相对收费偏好”的跨 cell 发生比例，不是单一美元罚金/共同经营成本下的胜率。F 还是比较与横轴尺度的共同锚，换参照会重参数化 beta；这不影响给定真实系数和给定报告下的代数比较，却影响如何读图和将其移植到经营决策。固定 QR33 的区域也不是所有可行规则的最优成本区域。主稿已禁止最小成本选模和 common-dollar 聚合，但目前图题中的 “costs less” 及后文经济解释仍容易超出这种相对、事后尺度的含义。

**可执行写作修正。** 在公式或第 298 行后加一句：

> The common beta grid holds the breach charge fixed relative to each cell's full-grid F headroom, rather than holding a common currency charge fixed across cells. The panels summarize the prespecified QR33 procedure's relative-cost regions, not an optimal policy frontier or a prospective estimate of the scale available at each issue.

图题说明 group fractions 对相关 source/H/W 任务等权计数、不是概率估计或共用金额的风险收益；继续保留 daily 原菜单比较的独立身份。不需再重复一次 “illustrative, not observed” 句子，可引用既有 Limitations。

**未解决科学边界。** 未观测真实收费、资金成本或干预后的持仓路径，也没有部署期预先固定 mF 的政策评估。当前结果能够回答固定保存报告在相对系数下如何换序，不能证明实际经营价值。

## V10-M5 — 把预计算冻结、未见新来源前设计和未见结果的确认性预注册分层呈现

**当前定位。** 主稿 `sec:evaluation` 第 177–179 行说新研究均在其 calculations 前固定设计；摘要第 17 行及结果第 256、276 行使用 registered threshold/预测判定。`sec:limitations` 第 322、330、332–334 行披露旧结果可见、schema 澄清与研究阶段选择。补充材料 `sup:v10-menu` 第 1510 行、`sup:v10-cftc` 第 1527 行及 `sup:selection` 第 668–676 行给出部分时序。E1 协议第 3–18 行明确继承已知旧损失与失败；E2 协议第 1–3 行明确设计在数据请求前；E3 协议第 1–15 行只保证在缺失 loss 派生/bootstrap 前；E4 协议第 1–9 行只保证在 cost means/regions 前。

**为何是主要问题。** 这些设计冻结的可核查性是优点，但四个锁定时点的证据强度不同。E1 是见过旧模拟大损失与已知失败后的固定路径机制追问；E2 在新来源获取前锁定有更强的结果不可见边界，但全历史连续性/OI universe 仍是回溯重放而非当时可执行宇宙；E3 使用已经预测和打分过的方法；E4 在已有预测及 MCS 后锁定相对成本网格。它们不能统称为同一种 outcome-blind preregistration。仅把“before their calculations”置于主文、把既有结果可见性分散到限制里，容易让注册阈值的支持/不支持被读成独立确认性检验，尤其是在多轮修订同一记录的背景下。数值来源审计或冻结 commit 也不消除这段研究路径。

**可执行写作修正。** 在 `Research design and transparency` 增加一张简短 chronology 表或等价段落，逐项列 E1–E4：此前已可见的来源/结果、实际冻结边界、随后唯一运行、结果应属的解释层级。使用 “pre-computation specification lock” 描述 E1/E3/E4；明确 E2 “specified before acquisition, evaluated retrospectively on downloaded economic dates”。把 M1–M3/T1–T3 称为“frozen descriptive decision rules”，除非另有未被查看的独立验证，不以“registered”一词单独暗示确认性证据。保留两个 schema clarifications 的发生时点和原失败回执，不宣称 ingestion 全程 blind。

**未解决科学边界。** 当前研究没有新的个体 dealer 或 prospective first-release holdout。完整 chronology 能诚实界定证据级别，但不能把已见样本变回未见样本，也不能使 repeated research-stage choices 获得未实施的全流程调整。
