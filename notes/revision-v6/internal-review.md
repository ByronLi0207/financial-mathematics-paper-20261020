# Independent internal self-review for revision v6

These are three role-separated internal self-reviews generated in independent same-model contexts. They are not real external referees, a journal decision, or a Claude/Cloud review. Each role inspected the current source before sharing findings. Original individual files and their evidence locators remain available.

---

# Role A

Source: `review-A.md`

# v6 内部自查 A：预测方法与统计评估

这是一份内部自我审查，不是真实的外部期刊审稿意见，也未调用 Claude 或任何跨模型复审。独立阅读当前投稿正文、补充材料、原始冻结设计、推断代码与 v5 分析设计后形成；未读取其他内部审查员的意见。审查快照为 `revision-v4-jof`、HEAD `00c9618469c291bdca186b69e3655e12174c1452`。未把平行 PR #3 的工作视为当前分支成果。未运行测试或金融实验。

任务理解：按照已授权 v6 计划的 WP1，识别 8–12 条 major/minor 问题，给出精确依据、证据等级与处理去向；保留两个原始 primary，新增分析一律为 post-result / exploratory。本文件列出 10 条，其中既有需要保留的统计限制，也有 WP2–WP5 执行前必须补齐的定义。已在现稿明确披露的问题不再冒充新发现的错误。

## 两个 primary 的身份锚点

| 身份 | 固定比较 | 原始结果定位 |
|---|---|---|
| FX primary | H6 QR W2880 − rolling F W720 | [paired-comparisons.csv:50](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261022/paired-comparisons.csv:50)：均值分别为 385844.8854897607、441774.03703851684 USD，损失变化 −12.660126412969763%，严格破线 376/332。 |
| Treasury primary | H6 QR W260 − frozen F W260 | [paired-comparisons.csv:64](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261022/paired-comparisons.csv:64)：均值分别为 4159.673194735081、2758.665342960289 USD millions，损失变化 +50.78571256749063%，严格破线 54/28。 |

上述数字直接抄自现有归档行，未重新计算。FX 的 −14.766762552613885% 属于不同的 matched 比较：QR W2880 − frozen F W2880，见 [paired-comparisons.csv:14](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261022/paired-comparisons.csv:14)。两者不得相互替换。

## A01 — major：贡献段的统计措辞应与工作参考检验的证据等级一致

**依据。** [正文:104](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript-content.json:104) 把 matched FX 比较称为 “statistically favorable”，并紧接 DM 与 Holm 数字；[正文:1035](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript-content.json:1035) 则明确说这些检验不是 selection-adjusted confirmation。[补充材料:4003](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement-content.json:4003) 已承认有效分量 p 值、长期协方差和样本检查后的选择都未获保证。[holm.csv:11](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261023/inference/holm.csv:11) 的具体数值与正文相符：DM −5.865679844214457，Holm 2.8626953049690645e-07；本条不质疑抄数正确性。

**判断。** 这是摘要式贡献表达与详细限制之间的证据等级落差，不是已证明的数值错误。小 p 值说明该工作参考计算在其假设下不利于等均值零假设，不能消除历史检查、后续模型选择或假设未验证的问题。

**处理：本轮修改。** 建议贡献段写为 “lower observed mean loss, with a favorable DM working-reference diagnostic”，保留数字并近接一句“retrospective, not selection-adjusted confirmation”。无需改变损失方向或原始结论，也无需为本条新增实验。

## A02 — major：重叠标签与共享估计产生的长期依赖没有被短带宽或 HLN 修正验证

**依据。** [inference_tests.py:65](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/inference_tests.py:65) 定义 `L=max(H,floor(4(n/100)^(2/9)))`；[inference_tests.py:76](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/inference_tests.py:76) 用正态 DM 和 Student HLN 参考分布。[原始设计:25](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/conditional-baseline-design.md:25) 与 [原始设计:33](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/conditional-baseline-design.md:33) 指定长滚动历史与分块 refit；训练重叠不因相邻目标窗口移除而消失。现有 [推断设计:5](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261023/inference-design.md:5) 及补充材料已正确披露这些前提未验证。

**判断。** 尚未证明 HAC 估计错误，也不能仅凭训练窗口长就断言应把带宽机械设置为 W。问题是有限带宽敏感性没有建立充分的长期协方差校准，HLN 原本的 MSPE 修正也没有为这里的 pinball 检验带来新的精确有限样本依据。固定有限训练窗口对 GW 式程序比较有帮助，但本身不是依赖与矩条件的实证验证。

**处理：显式限制，沿用到 WP2–WP5。** 保留既有设定与双带宽结果，新增表明确使用相同的探索性参考约定，不声称 n 个独立观测、有效样本量等于 origin 数、或“修正后显著性已经可靠”。本轮范围外不临时追加一个事后选块长的 bootstrap。若 WP4 新增 HAC，必须记录自己的有效 n、带宽、协方差秩及失败原因。

## A03 — major：稀疏覆盖诊断和 CC 变体不能作为“通过校准”的证书

**依据。** [run_v3_inference.py:59](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/run_v3_inference.py:59) 固定采用首 origin 加 `j(H+1)` 的网格。[coverage.csv:14](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261023/inference/coverage.csv:14) 起的 Treasury H6 只有 40 个网格点，[coverage.csv:20](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261023/inference/coverage.csv:20) 起的 H24 只有 12 个，且若干行有零转移计数。[inference_tests.py:93](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/inference_tests.py:93) 将全网格 POF 与按首观测条件化的转移独立性 LR 相加。[补充材料:4003](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement-content.json:4003) 已明确它不等于 Christoffersen 原文统一条件化初始化的有限样本 LR，并解释原子、边界和共享训练限制。

**判断。** 上述限制是已知且披露的；“代码算出了 p 值”不等于参考卡方在这些格子中得到校准。低破线率拒绝精确 5% 也不同于低覆盖；非拒绝更不等于条件覆盖成立。已知 floor 不必然产生分位点原子，但存在原子时严格破线概率可以合法低于名义水平。

**处理：WP2 + 本轮表述修订。** ACI 新表保留严格破线数、全部 origin 分母、稀疏网格分母、转移边界/NA 状态；将继承统计量明确标作 `CC-style diagnostic` 或完整写明构造。使用“未拒绝该工作零假设”，避免“passed calibration / calibrated at 95%”。不要按更有利的余数类重新选网格，也不要只展示一个 p 值来宣称覆盖率已被校正成功。

## A04 — major：v6 新比较必须有自己的完整检验清单与多重性边界

**依据。** [run_v3_inference.py:66](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/run_v3_inference.py:66) 只对既定 72 个 common-history contrast 做 Holm；原始 FX primary/legacy 在该 family 外。另一个 [补充表 S34:7300](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement-content.json:7300) 使用独立 48-slot family。[补充材料:8134](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement-content.json:8134) 已明确这并非全文范围的选择控制。v6 计划现在还加入 ACI、SAV、两种组合、面板扩展、状态分组/GW 与新 τ，不能继承旧的 72-family 标签。

**判断。** 当前 72-family 实现本身未发现漏项；风险在于新结果继续以未限定 family 的“Holm significant”进入正文或决策表。验证段选择 γ/λ 和研究者在同一已见评估记录上选择分析方向，也不是一次 Holm 就能全部处理。

**处理：WP2–WP5。** 每个冻结设计列出预期 contrast ID、比较方向、source/H/W/τ、组件方法、状态检验及 family 边界，事前决定是一个完整 v6 family 还是清楚限定的工作包 family。组件统计 NA 保持 NA；若为调整记账预留 p=1，必须与真实 p 值分列。不要因失败、重复或不利结果缩小 family。旧 72 与 48-family 的输出和标签保留；新调整不宣称修复历史选择或无效参考分布。

## A05 — major：延迟 ACI 需要完整的单侧校准与反馈定义，不能直接继承即时反馈保证

**依据。** [v6 计划:33](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/revision-plan-v6-goal6h.md:33) 至 38 只给出 α 更新、成熟误差、γ 菜单与待回答问题，尚未定义 conformity score、校准库、热身、状态初始化/延续、越界规则与 γ 选择目标。现有 [conditional_study.py:103](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_study.py:103) 至 137 的 base model 则固定 refit 池与 .95 参数。

**成熟做法依据。** Gibbs–Candès (2021) 的 [正式论文 §1.1、§2、§4.1](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf) 定义 score、其校准分位函数、即时误差更新及边界约定；长期频率结论依赖所给算法。将标签推迟 H 期消费是这里的适配，不能直接声称得到逐期条件覆盖或原定理原样适用。

**判断。** 这是尚待冻结的实现定义，不是当前分支已出现 ACI 泄漏的证据。需要防止误把历史目标与当前 report 比较，或反复消费同一破线，或为变动 α 每期重拟合 QR 而改变原 refit 时点。

**处理：WP2。** 冻结至少以下内容：单侧 score（例如真正 issue 时 base report 的 `P_i−C_i`，须明说选择）、按成熟期入库的样本及窗口、只用当时可得信息产生的历史 residual、热身与校准/训练重用边界、验证和评估之间 gap 内的反馈处理、α 初值与 carry/reset、精确更新/issue 顺序、原实际 wrapped report 的严格破线如何只消费一次、α/分位 rank 越界及非有限报告的失败规则、γ 的验证损失目标与并列规则。若采用裁剪或有限端点替代原文边界，则明确是受限适配，不援引原分布无关保证。保留 base 与 wrapped 两套全段结果；只有实际破线率/动态诊断改善后才能描述为“观察到覆盖改善”，不可把 wrapper 的名字当作覆盖已校正。

## A06 — major：headroom SAV 是需要重新定义时钟的 CAViaR 适配

**依据。** [v6 计划:39](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/revision-plan-v6-goal6h.md:39) 至 42 的“已成熟的最新冲击”存在多种不同定义。Engle–Manganelli (2004) 的 [作者提供正式论文 §3，p.369](https://simonemanganelli.org/Simone/Research_files/caviarPublished.pdf) 将 SAV 写为前一期分位递推加前一期响应绝对值；这里的响应是 H 期峰值 headroom，`G_(i,H)` 直到 `i+H` 才可见。[原始设计:11](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/conditional-baseline-design.md:11) 与 [conditional_study.py:108](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_study.py:108) 已确立成熟池边界。

**判断。** 如果训练时使用 `G_(i−1,H)`，issue i 时它通常尚未成熟；若改用最新已实现位置增量，则是另一个外生冲击规范。两者都不能含糊称作相同的经典 SAV。多起点优化的终止条件也不等于全局最小值认证。

**处理：WP2。** 事前指定冲击到底是 `G_(t−H,H)`、位置增量还是其他量，训练每一行都采用与 issue 时相同的延迟；不得仅在评估时补延迟。冻结递推初值、可用的初值历史、refit 后状态重建及块内推进、约束/稳定性边界、尺度变换、floor 投影位置、起点菜单/种子、目标与容差、非收敛规则。与同 source/H/W 的 F 和原选 QR 比较，保留完整失败格子。正文及 cover letter 称“maturity-aware headroom SAV adaptation of CAViaR”，避免把一个适配规范的结果推广到整个 CAViaR 家族。

## A07 — major：GW 联合拒绝与“波动状态改变优势”是不同问题，分组 HAC 不能压缩时间轴

**依据。** [v6 计划:54](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/revision-plan-v6-goal6h.md:54) 至 57 要求 RMS 三分位分组与含常数的 GW 工具变量。[Giacomini–White 正式论文摘要](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2006.00718.x) 区分无条件比较与预测未来相对准确性的条件评价；这里需明确所选有限工具矩检验的零假设。短期 RMS 本身的因果构造可沿用 [conditional_features.py:46](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_features.py:46) 至 55。

**判断。** 含截距的 `E[h_t d_t]=0` 联合拒绝可能完全由平均差非零驱动，不能单凭该 p 值认定高波动状态更有利。若先筛选某组日期，再对压缩后的 d 向量计算 HAC，其 lag 1 不再代表原始相邻 issue，协方差定义发生变化。这是执行前防错意见，尚未发现已经存在该错误的 v6 代码。

**处理：WP4。** 冻结工具向量、损失差符号、最近成熟 loss lag、训练阈值来自固定初始训练集还是随 refit 更新、阈值相等时规则，以及原始比较/ matched 比较的身份。对每组均值的 HAC 使用完整 issue 时轴上的 indicator 加权影响序列，如 `1{state_t=g}(d_t−mean_g)/p_g`，保留原始间距并报告组 n。联合 GW、无条件均值及状态间差异分开解释；工具矩或协方差奇异则 NA。决策表只增加实际支持的描述性状态结果，不把这一次回看分析写成已验证的切换策略。

## A08 — minor：组合基准需固定组件身份，并标出已知的精确退化情形

**依据。** [v6 计划:46](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/revision-plan-v6-goal6h.md:46) 至 50 未完全展开 F/QR/KNN 的组件身份。[原始设计:21](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/conditional-baseline-design.md:21) 说明 plain KNN 在 k=W 时等于 frozen F；Treasury W52 的 H6 与 H24 原选 k 都是 52，见 [selection-freeze.json:190](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/selection-freeze.json:190) 和 [selection-freeze.json:274](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/selection-freeze.json:274)。两行 [dm.csv:43](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261023/inference/dm.csv:43)、[dm.csv:61](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/results/revision-20261023/inference/dm.csv:61) 已记录 `IDENTICAL_LOSSES`。

**判断。** 在这两个格子，`median(F,QR,KNN)=F` 是精确代数身份，不是组合方法获得新的独立预测信息。两个报告平均的 pinball 损失由凸性至多为组件损失平均，却不保证胜过最佳单组件；报告组合也不自动拥有分位数或覆盖保证。

**处理：WP3。** 列出每个组件的固定 selection、history、refit、τ 与源单位；F 默认应明确为 matched frozen F，KNN 明确 plain KNN 或其他既定对象。面板任何缺组件格子保留 NA 与原因，不能临时删组件。分别比较组合与 F、QR，保留精确身份并按已有 NA/记账规则处理。Murphy 排名沿用全部唯一断点判别，201 点展示网格只用于画图，参照 [run_v3_inference.py:80](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/run_v3_inference.py:80) 至 85。

## A09 — major：τ 稳健性不能只改评分权重；现有辅助函数含 .95/5% 固定常数

**依据。** [conditional_study.py:46](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_study.py:46)、[conditional_study.py:118](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_study.py:118)、[conditional_study.py:162](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_study.py:162) 固定 19/20；[inference_tests.py:93](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/inference_tests.py:93) 的 coverage 默认 p=.05，[inference_tests.py:113](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/inference_tests.py:113) 的 DQ 直接减 .05，[inference_tests.py:134](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/inference_tests.py:134) 的 Murphy 默认 τ=.95。这些常数对当前原始研究正确，但不适用于计划的其他 τ。[v6 计划:61](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/revision-plan-v6-goal6h.md:61) 要求重拟合并重新选择 λ。

**判断。** 尚未证明任何新 τ 结果出错；这是若直接复用现有函数就会产生错误目标/零假设的具体入口。高 τ 的尾部信息稀少，不能以零破线或非拒绝作为更稳定的证据，也不能看到结果后才决定“样本不足”的标准。

**处理：WP5。** 贯通参数化拟合、F 的精确 rank、native pinball 验证选择、严格破线名义 p=1−τ，以及任何输出的 DQ/Murphy。保留 .95 路径回归不变的验证；为新 τ 使用能识别错误尾概率的已知答案检查。冻结可用 rank、拟合和样本不足规则，区分“有有限预测但统计诊断弱”与“方法结构不可计算”，不得因结果不利而标 NA。只重做计划指定的两个 primary 及对应 matched 控制，不顺便扩大菜单。

## A10 — minor：新增 matched 基准不能悄悄改变 primary 或解释成纯特征收益

**依据。** [正文:1079](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript-content.json:1079) 正确区分两个原始 primary；[正文:104](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript-content.json:104) 的较强数值论点使用 matched FX 比较，而 Murphy 曲线对应不同的原始 primary。[原始设计:19](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/conditional-baseline-design.md:19) 与 21 已说明，即便同池同更新，rank、优化目标、正则、有效局部样本和特征仍然不同。v5 [analysis-design.md:7](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v5-novelty/analysis-design.md:7) 的 gain bridge 也是描述性分解。

**判断。** 当前比较身份没有发现错误；v6 的“ACI 后 QR 优势是否还在”及“何时 QR 赢”最容易在概括时跨越这些身份。对 matched F 的结论不能冒充对 rolling W720 原始 primary 的覆盖校正结论，也不能从同池胜出归因为 isolated conditioning/feature value。

**处理：WP2–WP5 + 显式限制。** 新表、Murphy 图和状态表把 source/H/W/更新方式/τ 与 contrast ID 写入输出绑定，正文新增一句准确说出是哪一对。原始 FX 和 Treasury primary 继续完整展示，新增方法不重新命名为 primary。将 remaining caveat 保留为一句：“Matched histories and update schedules compare complete procedures; they do not isolate a causal feature or estimator effect.” 无需为此添加计划外消融实验。

## 处理清单

| ID | 严重度 | 建议去向 | 本轮验收证据 |
|---|---|---|---|
| A01 | major | 本轮修改 | 贡献段与全文限制采用一致的工作参考措辞，原数值与方向保留。 |
| A02 | major | 显式限制；WP2–WP5 沿用 | 新表注明依赖/矩条件及 HAC 限制，不声称已获精确校准。 |
| A03 | major | WP2；本轮表述 | 新覆盖表含分母、边界与 NA；CC 构造和非拒绝的含义清楚。 |
| A04 | major | WP2–WP5 | 冻结完整检验清单、family 边界及 NA 记账，旧 family 不改名。 |
| A05 | major | WP2 | 完整 ACI 设计、成熟反馈与失败规则、base/wrapped 全段输出。 |
| A06 | major | WP2 | 完整 SAV 时钟/递推定义与失败记录，适配命名准确。 |
| A07 | major | WP4 | 原时轴分组 HAC；GW 与状态差异分开解释；不生成部署策略宣称。 |
| A08 | minor | WP3 | 固定组件、精确退化身份、完整两侧比较与断点 Murphy 检查。 |
| A09 | major | WP5 | τ 贯通方法/评分/检验且 .95 保持；预定 NA 规则。 |
| A10 | minor | WP2–WP5；显式限制 | 两个 primary、matched 对与每一新增结论身份完全可追溯。 |

本次阅读没有证明原始成熟池代码存在前视，也没有重新验证全部原始逐期轨迹。现有 `pool` 的 `label_end<=r` 检查是可见的代码证据；金融序列的完整独立重跑不属于本自查任务。执行方应在恢复轨迹并完成既定字节核对后开展新分析；本文件不把任何尚未运行的工作包写成已完成结果。

## A05 追加裁定：拟议的有限延迟 ACI-style 规范

独立 10 条意见写完后，执行方另行要求评估以下待冻结方案：以 `S_i=P_i−baseC_i` 为单侧 score，只收原 refit 网格更早产生、`i+H<=t` 的 prefix/out-of-sample scores，最多 W 个；每条反馈只消费一次；有效 α 投影到 `[1/(m+1),1]`，rank 为 `ceil((m+1)(1−α))`，rank 0 用 −∞ 后执行已知 floor；γ 按验证段破线率距 .05 的绝对差、pinball、小 γ 顺序选择。该方案不援引原即时、未截断 ACI 的保证。此处为具体实现裁定，不是增加第 11 条独立审稿意见。

**结论。** 该有限适配适合作为本轮需要完整有限 pinball 轨迹的探索性比较程序；它比在部分 issue 出现 ±∞ 后仍强行汇总一个有限损失的做法明确。它与 canonical ACI 是不同程序；canonical 结果按既定规则 NA 也是诚实选择。不能把选用有限适配表述成已经执行了原算法、保留原保证，或统计证据更强。应使用 `finite delayed ACI-style calibration` 的全名，并以实测结果回答覆盖是否改善。

**冻结前仍需裁定的具体点。**

1. **状态与投影顺序。** 明确投影的是递推 α 状态本身，还是仅用于报告的有效 α；m 增加时是否重新投影；同一期先消费反馈还是先 issue。三者会改变算法。原文未截断更新的求和恒等式不能直接搬到投影递推。
2. **校准网格与反馈网格。** 明确校准库只收 refit-origin，破线反馈却消费全部 issue，还是二者都只用 refit-origin。两者速度和统计对象不同，不能在结果后互换。旧 score 对应当时的 base report，反馈 hit 对应当时实际 issued wrapped report，不能用当前 report 重算。
3. **小 m 主导。** 当校准库很短时，`1/(m+1)` 可能远高于 .05，有限 rank 实际频繁停在样本最大 score。记录每期 m、有效 α 范围、投影次数/比例及 γ 的验证并列；不要把 γ 选择或取最大 score 描述成获得名义 95% 覆盖。任何最小 m 门槛必须事前冻结，不能看结果后补。
4. **精确 rank 边界。** 在数学边界 `α=1/(m+1)` 时 rank=m，但直接浮点乘法再 ceil 可能给 m+1；需冻结有明确边界行为的算术并验证。`α=1` 的 rank 0、−∞ 后 floor、m=0、以及 score 全为负时的行为同样须定义。对有限 rank 的约定不能临时用宽松 epsilon 改目标。
5. **原选 λ 与重复验证。** 原选 QR 的 λ 已利用同一历史验证段选择，现在再选择 γ 是对该历史验证信息的再次使用。可以把 λ 当作已冻结配置重建每个 prefix 因果的 base 轨迹，但应称作事后条件于该配置的反事实轨迹，不能宣称这些报告在历史时点真实已发布或是全流程 fresh holdout 验证。`out-of-sample` 在此只表达每个 score 的目标未参与该次拟合，不消除验证选择。
6. **评价目标。** coverage-first 的验证选择与原 QR 的 pinball-first 选择不同；这是有意改变调参目标的完整程序比较。冻结使用全部验证 origin 的严格破线率、分母、并列和失败候选规则，不将它解释成只剥离了“覆盖偏差”的纯因果效果。
7. **完整格子的 NA。** Treasury H24/W260 QR 在首验证 issue 前可能没有合法 prequential score 的判断可由原池边界直接审计。原 QR 需训练池首 origin 至少为 feature valid_from=26；原设计给 H=24、W=260、验证首 origin 329、refit step 13，因此合法 prior refit 316 的标签到 340 才成熟，前一个网格 refit 303 的池首 origin 为 20，达不到 26。这里的索引全由 [study-spec.json:62](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/study-spec.json:62)、[原始设计:13](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/protocol/revision-20261022/conditional-baseline-design.md:13) 与 [conditional_study.py:108](/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/conditional_study.py:108) 的定义推得，未运行金融数据。若全段规则要求首期即有合法校准，则该格整格 ACI-QR 为 NA 是诚实处理；不得造 in-sample score、前移 refit、修改切分或只评分后半段。冻结后可用不读金融值的索引检查核对这个推导。

上述裁定不要求增加 v6 范围之外的实验；验收仍是已授权的设计冻结、边界/因果测试、完整输出与准确命名。

### 执行方后续澄清：尚待冻结与实施，不是本审查已验证的完成事实

执行方在阅读风险后澄清，拟改用所有合法 issue 行的 base scores，base 模型仍按原 refit 网格拟合；初始化只含验证首期前可发出的 prefix 预测且目标已成熟的 score。拟事前固定 `m<19` 则整格 NA，不缩短验证段；γ 在原验证段选择，原冻结 λ 不变，选定候选 α 状态携带至评估首期。gap 内不虚造 issue，在下一 issue 按成熟时间消费待处理的验证反馈且各消费一次。投影作用于递推状态，每次 update/issue 随 m 投影；记录 clip 与 m 范围。α、γ 和 rank 拟使用精确 Fraction 算术。

这些澄清能够处理上述“只取 refit-origin 校准”、浮点 rank、状态延续与全段 NA 的主要歧义；它们仍是执行方拟采纳的规范，不能由本文件证明已经编码、冻结、测试或运行。`m>=19` 只保证 5% 的有限 corrected-rank 分辨/可用性，不证明样本充足、条件覆盖或延迟 ACI 保证。

该 NA 规则应覆盖所有方法，而不只预列 QR：若 prevalidation 网格严格从验证首 origin 329 向后以 13 延伸，则 Treasury H24/W260 frozen F 最早合法 refit 为 290（此前 277 的池首 origin 为 −6）；首验证时可成熟 issue 只有 290..305，共 16 条，故也不足 19。相同假设下 H6/W260 QR 最早合法 refit 为 303，首验证时成熟 issue 303..323，共 21 条。这里都是原索引公式的直接推导，没有读取金融 outcome 或运行实验；执行方应在金融执行前以独立索引 fixture 核对，保留新旧提案的差别。两个原始 primary 的未包装结果不因 wrapper NA 而改变。

---

# Role B

Source: `review-B.md`

# Internal self-review B — financial economics

**Status:** Author-side internal self-review prepared for WP1 on 23 October 2026. This is not an external referee report, a journal decision, an independent financial replication, or a Claude/Cloud review.

**Task understood:** Review the current `revision-v4-jof` submission package for economic meaning, dealer-inventory positioning, data representativeness and practical value, then assign each concern to a text edit, authorized WP2–WP5 work, or an explicit limitation. I read the current manuscript and supplement independently; I did not read the other internal reviewer reports. No forecasts or new analyses were run for this review. Numerical statements below are readbacks of the existing submission content, not independently reproduced results.

**Overall diagnosis:** The paper has become much more defensible as a retrospective benchmark of a precisely measured peak functional. Its main economic vulnerability is the distance between that scalar functional and a dealer's actual inventory risk, balance-sheet utilization or funding decision. The existing caveats often address this distance correctly; they should be preserved during v6 rather than replaced by stronger application language after adding benchmarks. Mature practice in the inspected primary literature is to define the economic exposure and unit of observation before interpreting forecast performance, and to evaluate calibration alongside the relevant predictive score. The authorized v6 analyses can strengthen the forecast comparison. They cannot supply missing dealer books, an intervention counterfactual, decision costs, first-release history or a fresh external dealer sample.

Evidence locators use zero-based JSON pointers into `submission-jof/manuscript-content.json` (M) and `submission-jof/supplement-content.json` (S). Primary links were reopened during this review. A severity of major denotes a material interpretation or scope issue, including issues that are already adequately bounded and should remain limitations.

## B1 — Major: The stipulated score does not identify economic value

**Evidence.** M `/sections/4/blocks/7` explicitly treats the pinball asymmetry as stipulated, distinguishes unconditional underprediction and overprediction amounts from report headroom, and rejects an observed-cost interpretation. M `/sections/6/blocks/3` already recognizes that a cost per breach or a nonlinear loss can change a fixed-report ranking. M `/sections/9/blocks/4` lists the missing quotes, fills, hedges, collateral and cash-flow inputs. These are substantive qualifications, not disposable disclaimers. The FR 2004 reporting framework separately records positions and financing; its instructions use different accounting conventions for FR 2004A positions and FR 2004C financing, reinforcing why a position amount alone is not a cash requirement ([official instructions, A-1 and Appendix B](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=950ab256-b485-4586-99b0-b27eb205fdfa)).

**Concern.** Lower score, smaller reported headroom, fewer breaches and lower realized funding cost are different outcomes. In particular, reduced overprediction is not evidence that excess cash was actually held or released.

**Disposition — limitation.** Retain the current explicit decision-cost boundary, and apply it to all WP2–WP5 interpretation and the cover letter. A sufficient response is: “The score evaluates a stipulated quantile objective; realized financing or inventory-policy value requires decision-linked data that are unavailable here.” No new funding simulation is requested.

## B2 — Major: Aggregate cancellation changes the exposure being forecast

**Evidence.** M `/sections/2/blocks/1` correctly describes the absolute value of a dealer-aggregate signed position. Duffie et al. distinguish within-dealer absolute imbalances from taking an absolute value after signed dealer aggregation; their footnote 17 explicitly discusses offsetting positions. Their principal capacity constructions also use risk adjustments and dealer-level scaling ([official report, printed pp. 23–24 and footnote 17 on p. 27](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf)). M `/sections/7/blocks/1` and S `/sections/11/blocks/0` correctly identify the added panel as related aggregate tasks.

**Concern.** At a given time, `|sum_d N_d| <= sum_d |N_d|`. Consequently the peak of the signed aggregate is not the peak of total dealer magnitudes or a bound on each dealer's exposure. A low aggregate can conceal large offsetting books. The additional Treasury tasks broaden measured tasks but do not resolve that missing cross section.

**Disposition — this-round edit, with retained limitation.** Add one concise sentence to the transport interpretation or Table 6 caution explicitly distinguishing the absolute aggregate peak from aggregate absolute dealer inventories. Keep “related aggregate tasks” in the panel summaries. The adverse panel results delimit the executed forecasting specifications on these measurements; they do not establish a failure to forecast industry funding needs. No disaggregation analysis is requested.

## B3 — Major: The FX source is an attributed sample of client flow, not a verified complete dealer book

**Evidence.** M `/sections/2/blocks/0` uses one scalar over 2014–2017; M `/sections/9/blocks/8` acknowledges unverified commercial completeness and measurement accuracy. The original source paper describes a sample of one market maker's client flow involving its five most liquid currency pairs, measured hourly in USD ([Wisniewski et al., Section 3.1, physical p. 4](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf)). That supports the attributed data lineage, not a claim about all dealer business or residual inventory after every hedge. I did not obtain additional raw-book evidence, and the Kaggle page's substantive documentation was not readable through the web tool.

**Concern.** “One market maker” can be read too broadly if the original source's sampling qualification disappears. Neither the record count nor the related Treasury panel identifies representativeness across dealers, markets, currencies or later business practices.

**Disposition — this-round edit plus limitation.** Restore the word “sample” in the first FX data description, for example “a source-attributed sample of one market maker's client-flow-derived positions.” Preserve the missing complete-book and unseen-dealer qualifications. WP2–WP5 remain retrospective analyses of these same observations and cannot count as independent dealer validation.

## B4 — Major: The Treasury known floor belongs to the replay information convention

**Evidence.** M `/sections/2/blocks/4` states that the current economic-date observation is treated as known by convention and that the exercise is not an as-released backtest. The current NYFed page says statistics normally update on Thursdays with the previous week's observations ([official release description](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics)). S `/sections/11/blocks/2`–`3` distinguishes capture and issue timestamps, retains a future-vintage amendment, and says the live issuance adapter has not been implemented.

**Concern.** “Issue-known floor” without the replay qualification can sound operational for a public-data user at the economic date. The mathematical floor result is conditional on observing the anchor; it does not make an unpublished aggregate publicly observable. Adding ACI, CAViaR or combinations cannot repair the historical publication-clock gap.

**Disposition — this-round edit plus limitation.** When integrating new Treasury results, attach “downloaded-vintage economic-date replay” to the first main-text comparison or its caption, rather than relying only on Section 3. Preserve the no-prospective-validation statement and do not describe the unimplemented adapter as completed. Building that adapter is outside the authorized WPs.

## B5 — Minor: Keep recorded sampling and operational monitoring horizons distinct

**Evidence.** M `/sections/2/blocks/0` retains both one-hour and forty-nine-hour FX adjacent gaps, and M `/sections/2/blocks/3` defines H in subsequent source records. Treasury observes weekly closes. The target in M `/sections/3/blocks/3` is a maximum over those recorded observations, including the issue anchor; the motivating illustration in M `/sections/0/blocks/1` already disclaims the unobserved between-record maximum.

**Concern.** “Short horizon,” “hourly peak” or “six-hour monitoring” can inadvertently imply a fixed elapsed horizon or continuous intraday coverage. The weekly task is particularly remote from the maximum cash or securities need within each week.

**Disposition — this-round edit.** Add “H counts source records; between-record peaks are unobserved” to the decision-map note or the new supplement introduction. Preserve the sampled-target wording in the abstract and captions. No interpolation, alternative horizon or new intraday experiment is requested.

## B6 — Major: Explain how the dealer-inventory literature motivates this passive forecast without identifying a control policy

**Evidence.** M `/sections/0/blocks/0` cites Ho–Stoll, Lyons and Hansch et al. as economic motivation. M `/sections/9/blocks/4` distinguishes the passive envelope from an active quoting model. The inspected Hansch et al. primary abstract links relative dealer inventories to dealer behavior and documents nonlinear inventory adjustment ([published article](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00067)). That is a behavioral mechanism involving actions and relative positions, whereas this paper forecasts a scalar under the realized historical business process. I did not newly verify the complete Ho–Stoll or Lyons articles; no claim of a complete dealer-literature audit is made here.

**Concern.** An improved envelope forecast does not show how quotes, hedges or client selection should change, and deploying such actions could change future position dynamics. These data do not identify the counterfactual law under a different inventory policy.

**Disposition — this-round edit.** Add one sentence connecting the literature to the narrower use: “Inventory-control studies motivate monitoring, but this passive forecasting exercise does not estimate the effects of changing quotes or hedges.” Keep the contribution as predictive validation, without a new inventory-control model or policy experiment.

## B7 — Major: Separate a score–breach coexistence finding from a claim about a calibrated model advantage

**Evidence.** M Table 3 (`/sections/5/blocks/0`) reports lower matched FX loss with more all-origin breaches; Table 4 uses a different, explicitly sparse diagnostic grid. The closest endpoint lineage already compares conformal methods with ordinary quantile procedures and evaluates interval calibration ([Wisniewski et al., Sections 4.1–4.3](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf)). Gibbs and Candès provide the primary ACI framework, which wraps estimated predictions or quantiles ([NeurIPS 2021 proceedings](https://proceedings.neurips.cc/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html)).

**Concern.** The current coexistence result is legitimate, but whether QR retains an advantage after adaptive coverage correction remains unanswered. Failure to reject a sparse-grid diagnostic is also not proof of calibrated conditional risk. The economic interpretation should not assume the answer favors QR.

**Disposition — route to WP2.** Compare the frozen F and selected QR wrappers using only matured feedback and the frozen selection menu, then retain all score and coverage outcomes. Describe CAViaR as the specified adaptation to peak headroom, rather than a literal replication of a return-VaR application. A delayed-feedback, overlapping-label implementation needs its stated guarantees qualified; a standard ACI citation alone does not establish conditional coverage for this adaptation. Preserve the two original primaries and distinguish full-origin breach counts from sparse-grid tests.

## B8 — Minor: Simple combinations are necessary context for practical model comparison

**Evidence.** The current decision map, M `/sections/8/blocks/3`, organizes method evidence but contains no executed forecast-combination comparator. The v6 plan fixes equal averaging of F and QR and the median of F, QR and KNN before the new results are observed.

**Concern.** A practitioner considering whether conditional complexity is useful can reasonably ask whether a simple fixed combination offers a better score–coverage balance. A combined report would be another candidate forecast; its retrospective performance would not establish a new operational switching policy. This is a reviewer judgment about comparator relevance, not a literature-priority claim.

**Disposition — route to WP3.** Report both prescribed combinations for every required complete cell, including ties, deterioration and unavailable constituents. Evaluate their loss, breaches and prescribed comparisons without tuning weights after seeing outcomes. Update the decision map only if the actual results materially change its descriptive message; do not presume combinations improve either source.

## B9 — Minor: WP4 states measure position-change volatility, not Treasury yield or FX price volatility

**Evidence.** M `/sections/3/blocks/9`–`10` defines RMS from changes in the signed position scalar. M `/sections/8/blocks/1` already disclaims a causal frequency effect. Duffie et al.'s economic setting distinguishes yield volatility from intermediation-capacity measures ([official report](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf)); the present RMS variable is not an observed yield-volatility series.

**Concern.** “QR works in high volatility” would overstate the state measurement if readers understand volatility as market price risk. The same RMS can reflect client-flow dynamics, scale, valuations or reporting changes. State-specific average score differences cannot identify the causal mechanism or a deployable regime rule.

**Disposition — route to WP4.** Name the state “issue-known position-increment RMS” or “position-change volatility,” freeze the training-only cut points and matured loss instruments as planned, and report actual directions with HAC uncertainty. Preserve the descriptive status of Table 6. No market-price variables, new regime search or policy backtest is requested.

## B10 — Major: Quantile-level robustness tests a forecast target, not observed economic preferences

**Evidence.** M `/sections/3/blocks/13` fixes the current estimation level, while M `/sections/6/blocks/4` describes a different exercise that holds archived reports fixed and changes loss weights. WP5 instead refits at its two predeclared quantile levels. These are distinct comparisons; M `/sections/4/blocks/7` correctly rejects interpreting the current score ratio as an observed financing-price ratio.

**Concern.** Fixed-report preference sensitivity cannot substitute for a newly estimated tail quantile. Conversely, stable rankings under WP5 would strengthen target-level robustness but would not validate a bank's objective, stress loss or capital requirement. At the more extreme level, limited mature observations can undermine informative comparison, particularly in the weekly tasks.

**Disposition — route to WP5.** Keep refitting, validation selection and sample-failure rules frozen before evaluation, show direction reversals and NA cells, and describe the output as quantile-level robustness. Do not characterize it as welfare, funding-price or regulatory-capital robustness. Treat the choice of an institution-specific decision objective as an explicit limitation.

## B11 — Minor: Preserve the correct boundary between a known floor, an atom and fitted coverage

**Evidence.** M Proposition 1 (`/sections/3/blocks/20`–`23`) correctly makes the floor projection a pointwise scoring result and the strict-tail inequality a population-quantile result. M `/sections/9/blocks/3` and S `/sections/14/blocks/12` explicitly show that the floor need not create an atom. M `/sections/3/blocks/34` also confirms that the historical controls already use current information.

**Concern.** The known floor is an informative feasibility restriction, but it neither proves that fitted reports meet a desired breach rate nor supplies a separate economic benefit relative to controls using that same restriction. Equality-based coverage tests require their stated null, especially with discrete or rounded measurements. This part is already handled well and should not be simplified incorrectly during English editing.

**Disposition — limitation; preserve existing text.** Keep the population-versus-fitted distinction and do not attribute excess conservatism automatically to a floor atom. Apply the same floor consistently to the authorized new reports. A sufficient response is: “The common observed floor is a feasibility constraint; it supplies neither fitted conditional calibration nor identified financing value.” No new floor analysis is requested.

## Disposition register for WP1 integration

| ID | Severity | Primary disposition | Concrete closure criterion |
|---|---|---|---|
| B1 | Major | Limitation | Preserve stipulated-score versus realized-cost boundary in new results and cover letter. |
| B2 | Major | This-round edit | Explicit absolute-aggregate versus dealer-magnitude distinction; retain related-task scope. |
| B3 | Major | This-round edit + limitation | Restore original FX sampling qualification; no new independent-validation claim. |
| B4 | Major | This-round edit + limitation | Attach replay information convention to first new Treasury comparison; prospective results remain pending. |
| B5 | Minor | This-round edit | Decision-map/supplement note states recorded horizons and unobserved between-record peaks. |
| B6 | Major | This-round edit | One sentence separates passive forecasts from effects of inventory-control actions. |
| B7 | Major | WP2 | Report actual calibrated-wrapper and CAViaR results with mature timing and qualified guarantees. |
| B8 | Minor | WP3 | Report the two frozen combinations, including adverse/tied/NA results. |
| B9 | Minor | WP4 | Correct state label; actual state effects and uncertainty; no inferred switching policy. |
| B10 | Major | WP5 | Refit target-level sensitivity with reversals/NA retained; no cost-preference inference. |
| B11 | Minor | Limitation | Preserve floor/atom/population/fitted distinctions for all added reports. |

**Review boundary:** These are requested dispositions, not claims that the edits or WPs have already been completed. The economic limitations in B1–B4 and B6 remain after any statistically favorable new benchmark result. No analysis beyond WP2–WP5 is requested, and no forecast family is assumed to win.

---

# Role Editor

Source: `review-editor.md`

# WP1 — Internal editor self-review

**Status: internal self-review by the project assistant. This is not an external editor report, an external peer review, a journal decision, or independent scientific validation. No Claude/Cloud review was invoked.**

Reviewed on 23 October 2026, branch `revision-v4-jof`. Scope: current `submission-jof/` manuscript, supplement, title page, cover letter, author checklist and package README; v5 contribution/positioning source and evidence records; the authorized v6 plan. Other WP1 reviewer files were not consulted. No scientific source, code, experiment or manuscript was changed during this review. Line locators below refer to this inspected source snapshot and must be refreshed after integration.

## Editorial assessment and verified journal context

The paper has a plausible Journal of Forecasting application/evaluation fit: it studies a clearly defined forecast functional, compares mature procedures, and preserves failures and unfavorable results. Its strongest editorial story is the contrast between a favorable inspected FX score comparison and adverse separately fitted aggregate-task results, with explicit information timing and measurement boundaries. The present title, abstract and contribution paragraphs distribute attention across too many secondary findings before that story is established. These are concerns about evidence hierarchy, interpretation and reader navigation; they do not establish that any reported numerical result is wrong.

Fresh official-source checks support the following boundaries:

- The [official journal scope](https://onlinelibrary.wiley.com/page/journal/1099131x/homepage/productinformation.html) describes a broad forecasting journal and emphasizes modelling and connections to decisions. The direct page request timed out; its current official-domain search result supplied the scope text. Fit here is an editorial inference, not a promise of review or acceptance.
- The [official Author Guidelines](https://onlinelibrary.wiley.com/page/journal/1099131x/homepage/forauthors.html), retrieved successfully in this review, allow consistent initial Free Format references, require a peer-review PDF alongside LaTeX and supporting sources, and request a brief informative title, fewer than 40 characters for the running title and up to six keywords. They state single-blind review and expect data sharing. No numerical body/abstract word limit or page cap was found in the inspected guidelines. The project's 9,000-word/six-table/four-figure budget is a working constraint, not a verified journal limit.

Mature editorial practice for this task is to declare the target and primary comparisons first, separate descriptive accuracy from calibration tests and decision value, compare credible alternatives on the same information clock, give the reader usable cross-references, and distinguish frozen retrospective evidence from genuinely new validation. The manuscript already implements many of these practices; the issues below identify where presentation or the remaining menu weakens them.

## Issues and proposed disposition

### E01 — Major: the title/abstract/contribution hierarchy obscures the primary empirical question

**Passages/routes:** `submission-jof/manuscript.tex:12–16`, `:34–38`; `title-page.tex:7`; `cover-letter.md:3–5`. The abstract foregrounds three elementary construction properties, then the **matched** FX loss reduction of 14.77%, original-primary elementary-score crossing, W720 horizon crossing, Treasury +50.79%, a 3/48 panel count and an invalid-label experiment. It does not report the original FX primary's 12.66% reduction, although that primary anchors RQ1. The current title gives the classical bound and the floor the same prominence as the empirical forecasting question.

**Why it matters:** The numbers are explicitly distinguished in the text, but a new reader must reconstruct which result answers which question. A title about construction bounds can also set an expectation of a principal theoretical advance that the paper correctly disclaims.

**Disposition: NOW, with final synchronization in WP6–7.** Keep the application/model-validation contribution and both original primaries as the main contract. Lead the abstract with the target, comparison design and two original-primary outcomes; give the matched-history FX contrast as a clearly labeled control. Retain one concise qualification on retrospective inspection/vintage and one on absent prospective/unseen-dealer validation. Leave the timing oracle and detailed crossing/panel counts in the supplement unless new WP results materially change the conclusion. Consider the already recorded question-led title; author confirmation of the final title remains in `AUTHOR-TODO.md`. No priority claim or numerical outcome should be upgraded.

### E02 — Major: the benchmark menu remains incomplete at exactly the points the positioning discussion makes salient

**Passages/routes:** `manuscript.tex:63–71`, `:345`, `:360`; `supplement.tex:1111`. The closest endpoint lineage is conformal, CAViaR is named as a relevant mature alternative, and the conclusion still lists these as future work. Fixed forecast combinations are absent from the executed main menu.

**Why it matters:** An application paper can use established methods, but its conclusions about the comparative value of conditional reports are harder to interpret when a directly adjacent calibration method and simple combinations have not been evaluated. The existing text honestly limits the menu; this is a substantive evidence gap rather than a citation omission.

**Disposition: WP2–3.** Execute the predeclared ACI, SAV-CAViaR and fixed-combination comparisons on the original mature-label clock and retain failures. Update the method overview, complete supplement results, cover letter and the remaining-alternatives sentence only after actual outputs exist. ACI-CAViaR evidence must remain exploratory; it does not replace the original primaries or establish a universal winner. If a method is NA, retain that explicit limitation instead of saying it was successfully benchmarked.

### E03 — Major: matched-history score claims route to original-primary score diagrams

**Passages/routes:** `manuscript.tex:36` gives the matched-history 14.77%, 376/360 and Holm result with the route “Tables 3–4 and Figures 3–4.” However, Figure 3 (`:293`) and Figure 4 (`:298`) are explicitly **original-primary** diagrams. Table 6 (`:327`) likewise places long-history matched QR/KNN score evidence next to “crossed score curves … Figure 3.” Supplement Table S24 (`supplement.tex:618–625`) confirms that the full-breakpoint audit is for the two original primaries.

**Why it matters:** The source says “distinct original primary,” but the route still permits a reader to attach the crossing finding to the matched pair or KNN. Crossing has not been established for those other pairs by the cited diagrams. This is a comparison-attribution problem, not a demonstrated numerical error.

**Disposition: NOW.** Split the contribution paragraph into separately routed claims: matched-history score and hit counts → Tables 3–4; original-primary score-class sensitivity → Figure 3/Table S24; Treasury original-primary sensitivity → Figure 4. Qualify the Table 6 caution explicitly as the **original-primary QR comparison**. Do not silently generalize the diagrams to matched controls or KNN; a new diagram would need its own authorized analysis/binding.

### E04 — Major: increased hit frequency must remain distinct from demonstrated calibration deterioration

**Passages/routes:** title `manuscript.tex:12`, abstract `:16`, contribution `:36`, discussion `:282–288`; Table 4 (`:270–272`) shows FX H6 QR POF p=0.695 and DQ p=0.736, while rolling and matched F have DQ p=0.00798 and p=0.0407. The title's “Score–Coverage Disagreement” and repeated “more breaches” can be read more strongly than this evidence warrants.

**Why it matters:** More observed breaches is an exact descriptive statement; it does not by itself show worse conditional calibration or a conflict between a proper score and a coverage theorem. The paper already explains this correctly in Sections 4, 7 and 9. The high-visibility framing should preserve the same distinction, especially because the diagnostics do not uniformly favor F.

**Disposition: NOW + WP2.** Prefer “score and breach-frequency trade-offs” where the evidence is only descriptive; retain calibration as a separate diagnostic object. Add one clear statement near the headline example that more breaches alone do not establish calibration deterioration. WP2 should then answer the genuinely new question of whether the score ranking persists after online calibration. Keep nonrejection qualified; it is not proof of correct calibration.

### E05 — Major: the decision map lacks evidence on issue-known states and quantile-level sensitivity

**Passages/routes:** `manuscript.tex:316–330`, especially “Use frequency, history and the measurement definition to frame validation comparisons”; `:339–351`. Current Table 6 organizes findings mainly by source/history, and the main analysis fixes the .95 quantile. The text correctly avoids causal frequency and switching-policy claims.

**Why it matters:** Readers looking for guidance on when the fitted procedure helps can presently identify archive settings, but cannot infer an issue-known state rule or robustness across tail preferences. These limitations constrain the practical contribution even after the forecasting functional is clearly stated.

**Disposition: WP4–5, then explicit limitation.** Add only the predeclared known-at-issue volatility groups, conditional predictive-ability calculation and .90/.99 fits. Update the map if those outputs support a state or quantile distinction, including null results and direction reversals. Retain the sentences that the analysis does not identify a causal frequency effect, a deployable switch, independent dealers, or prospective calibration. These work packages cannot repair the absent unseen-dealer/prospective validation.

### E06 — Minor: the evaluation sample and refit budget are too remote from the core design

**Passages/routes:** `manuscript.tex:78–86`, `:112–115`, `:187–189`; `supplement.tex:1142–1149` (Table S36). Main text gives exact boundary dates and an algebraic refit rule, but the concise source-specific validation/evaluation counts, W values and cadence are relegated to the last supplement section. Several early results use 6,625 or 277 origins before that budget has been presented together.

**Why it matters:** These are the basic denominators and learning schedules needed to understand the primary comparison, not merely reproduction internals.

**Disposition: NOW.** Add one compact design sentence or source-budget panel using existing S36 values: FX validation/evaluation 1,440/6,625 and refit d=24; Treasury 52/277 and d=13, with the existing W values. Explain H as source-record transitions and keep sparse-grid counts separate. Reuse existing output values; no new calculation is needed.

### E07 — Minor: main-table numbering is out of reading order

**Passages/routes:** Table 3 at `manuscript.tex:207`, Table 5 at `:223`, Table 4 at `:264`, Table 6 at `:321`. Physical source order is 1, 2, 3, 5, 4, 6.

**Why it matters:** The bridge was integrated after numbering was settled. Hard-coded table numbers make a correct route harder to follow and increase the risk of a partial renumbering during WP6.

**Disposition: NOW / WP7 cross-reference check.** Either move the bridge after the coverage table or renumber the bridge and coverage tables in order of first appearance. Update every main, supplement, caption and decision-map reference together, including `supplement.tex:1175`. Confirm the rendered order after the rebuild; do not change archival table numbers in original result records.

### E08 — Minor: repeated qualifications and archival detail displace the main forecast narrative

**Passages/routes:** duplicate section/subsection heading at `manuscript.tex:181–182`; intercept/normalization explanation repeated at `:134` and `:142`; finite-menu floor qualification repeated at `:286` and `:288`; selected-fit shrinkage internals at `:347`. Recorded v5 metrics are 6,721 main prose words, six tables and four figures, plus 8,313 supplement prose words/37 tables; these are recorded metrics, not a new formal-TeX page measurement.

**Why it matters:** There is no verified journal cap breach. The concern is cognitive load: the main result is repeatedly interrupted by extensive historical and numerical qualifications, while the supplement also starts by replaying a substantial article-like narrative.

**Disposition: NOW / WP6–7.** Remove literal duplication, merge adjacent statements with the same meaning, and keep detailed selected-fit/numerical history in its existing supplement route. Preserve qualifications once at the relevant claim and in a focused limitations paragraph. Put WP2–5 full outputs in the planned supplement section; mention a new result in the main text only when it materially changes the conclusion. Recount the project's stated word/table/figure budget after integration without relabeling that budget a JoF rule.

### E09 — Minor: the supplement contains machine pointers and revision labels that are weak reader-facing locators

**Passages/routes:** `supplement.tex:1139` (“S15. V5 post-result analyses…”), `:1205` includes `THIS_STUDY, ['sections', 3, 'blocks', 2]` and `sections[7].blocks[5]`; `:1207` routes source IDs generally to a repository register. Compare the readable article locators elsewhere in the same subsection.

**Why it matters:** These are useful audit bindings, but a journal reader cannot reliably navigate a printed paper using JSON offsets or an unnamed repository log. Revision labels also make the supplement look like an internal project history instead of a stable research document.

**Disposition: NOW / WP7.** Replace printed JSON offsets with current article section/proposition/table locators. Give the source register a specific repository-relative path or stable link, retaining machine pointers there for audit. Rename S15 by its analytical contents, retaining the post-result label and the original evidence files. Use consistent capitalization for “AR,” “FHS,” “POT” and supplement headings.

### E10 — Minor: bibliography inclusion and citation routing are not fully consistent

**Passages/routes:** `manuscript.tex:434` lists Sussman (2023), Proposition 3.4, but no author–date invocation appears in the manuscript or supplement; the Lévy result is named at `:160–165` without a linked source invocation. `submission-jof/README.md` says each document displays only its own cited references. The main reference list also puts Lindsay (`:390`) before Diebold (`:392`), interrupting author order. `AUTHOR-TODO.md:11` explicitly retains unresolved metadata checks.

**Why it matters:** The present package does not yet fulfill its own one-to-one citation claim. This review does not certify all reference metadata and does not infer that the listed end pages or names are wrong.

**Disposition: NOW / WP7.** If Sussman is the consulted source for the classical inequality, add the appropriate author–date/proposition citation where it supports that statement; otherwise remove the uncited entry from that document while retaining the source register. Sort and format consistently, and perform a cited-work ↔ displayed-entry audit separately for the main and standalone supplement. Verify the explicitly pending fields against primary metadata before clearing the author checklist. Initial Free Format flexibility is not a reason to claim an audit that has not been completed.

### E11 — Minor: availability wording blurs access restrictions with local trace handling

**Passages/routes:** `manuscript.tex:363–365`; `supplement.tex:606–611`; `cover-letter.md:9`; `AUTHOR-TODO.md:9`. The public Kaggle acquisition route and non-assumed redistribution rights are stated, followed by “Private raw FX observations and private per-origin forecast traces are not redistributed.” The supplement says accepted forecasts are preserved but origin-level traces remain private.

**Why it matters:** A reader may interpret “private raw FX observations” as a nonpublic proprietary input rather than a locally held copy of a source with stated third-party rights. They also need to distinguish publicly archived aggregates from regenerable local forecasts and unavailable original dealer books.

**Disposition: NOW, retaining the explicit data limitation.** Describe the actual access route and redistribution boundary of raw inputs, then separately state whether origin-level traces are obtainable or must be regenerated and point to the exact reproduction instructions. Do not imply redistribution permission, independent audit, permanent anonymous access, or access to original dealer books. Preserve the actual source/vintage limitations and the author's permission check.

### E12 — Major for submission readiness: preview PDFs and personal declarations are still preparatory artifacts

**Passages/routes:** `submission-jof/README.md` states that all preview PDFs were independently typeset with ReportLab and source compilation returned diagnostics rather than an exported TeX PDF; `AUTHOR-TODO.md:8` requires formal output and page review. `title-page.tex:8–14`, `manuscript.tex:367–373` and `cover-letter.md:11–14` retain author/disclosure placeholders.

**Why it matters:** A successful diagnostic compile and a separately generated preview do not establish that the peer-review PDF is the actual output of the submitted sources. Author identity, approval and declarations cannot be inferred from the scientific package. These are explicit current boundaries, not evidence that the underlying source fails to compile or that declarations were omitted dishonestly.

**Disposition: explicit submission limitation / AUTHOR-TODO; technical artifact checks in WP7.** Bind the final sources, figures and package to the formal TeX-generated peer-review PDF and inspect it after final integration. Keep preview provenance explicit until that exists. Leave personal fields for the author, and do not make a journal submission, approval or disclosure on their behalf. An internal v6 completion report should distinguish completed preparation from submission readiness.

## Disposition ledger

| ID | Severity | Primary route | Completion evidence required |
|---|---|---|---|
| E01 | major | now; synchronize WP6–7 | abstract/title/contributions and cover letter express one comparison hierarchy |
| E02 | major | WP2–3 | complete fixed-menu outputs, failures and revised remaining-work sentence |
| E03 | major | now | each score-diagram claim names its actual pair and routes to its own caption/audit |
| E04 | major | now + WP2 | breach-frequency wording kept separate from calibration inference; actual ACI outcomes |
| E05 | major | WP4–5 + limitation | complete planned state/quantile outputs and bounded decision-map update |
| E06 | minor | now | original sample/refit budget readable beside design |
| E07 | minor | now / WP7 | sequential displayed numbering and consistent cross-document routes |
| E08 | minor | now / WP6–7 | redundancy reduced; project metrics refreshed without invented JoF cap |
| E09 | minor | now / WP7 | readable printed locators and specifically linked audit register |
| E10 | minor | now / WP7 | per-document citation audit and retained unresolved metadata boundaries |
| E11 | minor | now + limitation | source access and trace regeneration/availability stated separately |
| E12 | major | WP7 + author-controlled limitation | actual final-source PDF binding; personal declarations remain author actions |

**Count: 12 issues, 6 major and 6 minor.** These are proposed dispositions for the integrating agent; this reviewer did not execute them. The absent compatible unseen-dealer sample, unexecuted prospective protocol, source-vintage limitations and missing decision-cost mapping remain explicit scientific limitations after WP2–5.

## Inspected-source fingerprints

```text
902de0569b6e2ec9aff225f33941f02b0194c4cfbfc079bf634d04d3eb91f873  submission-jof/manuscript.tex
656e87821d822fdaec9b9ef10ead6590e83f83348afc9d1058cef50abf0e0d89  submission-jof/supplement.tex
fa0990c364597a4b22cbf6b3e6cc92b525b2743c76712731dff85b55bc34083e  submission-jof/title-page.tex
566cb41ab8405617666d000bb53bd6c76e953e7a9e251e91faa3b256232a0465  submission-jof/cover-letter.md
97fb9ac619b1e51e220f6668ec83dd470b99fd949cecec6d075640cff99b079c  submission-jof/AUTHOR-TODO.md
93067bde6be00cc1eee2b654630a6aa3df43be52fb2dbfc3dddd08cee2f5c8d9  notes/revision-v5-novelty/contributions-proposal.md
bf4033ba651c8db57c56e4c32dca4ca8130cd7331f400efd629eedcb2e883508  notes/revision-v5-novelty/positioning-source.json
```

Memory was used only for orientation and the instruction to reopen current sources, not as evidence for present scientific findings. Current findings above come from the inspected sources and fresh official guidance. No tests, experiments, compilation or independent statistical validation were performed by this editor self-review.
