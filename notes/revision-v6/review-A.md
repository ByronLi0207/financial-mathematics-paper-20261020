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
