# C0：两个 v8 的写法与产物对照清单

核读日期：2026-10-24。范围仅为 C0：识别差异、指定来源、提出后续处置；本文件中的“搬入”“放补充材料”“不用”是后续执行决策，不表示已完成 C1–C7。未运行模型、断点诊断、模拟、真实数据预测、编译或新统计检验，未提交或推送。

## 1. 固定底稿、来源及判断依据

|标记|精确目录 / 固定 Git 身份|用途与写入边界|
|---|---|---|
|V8|`/Users/bingyouli/Research/论文/金融数学论文-v8-20261024`；`revision-v8`；HEAD `f151b830489917ab7abc5137f2ec6b4135f55d6e`|只读；提取直接、简短的写法和该版独有产物。|
|P5|`/Users/bingyouli/Research/论文/金融数学论文-v9-20261024` 在 base `0f1f066843e0c49cf3e24bce7d72032dc189603d` 的文件；来自 PR #5 / `revision-v8-goal`|v9 证据底稿；当前分支 `revision-v9`。所有 `P5:路径` 都指这个固定 base 的 Git 对象，不指未来被改写的文件。|
|v9|`/Users/bingyouli/Research/论文/金融数学论文-v9-20261024`|本 C0 子任务唯一新文件为本清单。核读前本文件不存在，故无需覆盖备份；`notes/v9/` 已存在。|

下文 `V8:相对路径` 与 `P5:相对路径` 分别以表中绝对目录和固定提交为锚，完整标识精确来源。两版 `submission-jof/main.tex` 都是两行编译入口，实际正文源是 `submission-jof/manuscript.tex`。

依据为用户本轮任务单 [导师v9合并任务-20261024.md](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/导师v9合并任务-20261024.md)，以及其指定的 [导师写法修改指导-20261023.md](/Users/bingyouli/.codex/plugin-data/claude-review-assistant/workspaces/01a16028-f1df-7f31-b3ba-87f7289e5fe0/batch-oh4_2klg/导师写法修改指导-20261023.md)。采用两份任务单共同要求的成熟报告方式：先给发现，随后给具名比较和证据；把测量、回顾性和推断边界集中写明；不把基本数学性质算作方法创新；保留全部负面与失败结果。旧指导中的推送目标、页数或“此前未评估”措辞不覆盖本轮 v9 的新指令与 P5 已核实的回溯暴露事实。

**合并原则：P5 的证据作底，V8 的直接写法作模板。** 不能整份替换正文/补充材料，也不能用 V8 的 24 格模拟替换 P5 的 72 格。P5 的日频对照与完整回溯结果均保留；C2 不平稳性解释在运行前仍是假说。

## 2. 逐项写法与独有产物的处置

|项目|V8 精确来源与内容|P5 实际差异|处置|v9 目标用途与必要改动|
|---|---|---|---|---|
|摘要|`V8:submission-jof/manuscript.tex:17`；最终绑定 `V8:notes/v8/abstract-final.json`。发现先行：历史规则难打败；14.8% / 16.6% 匹配收益；后期校准 15.0%、329/328；周度 34/48；未校准 376/360；平稳模拟未重现周度损失、七格小时模拟不可用。|`P5:submission-jof/manuscript.tex:17` 仍将 “We formalize the known-floor target and apply a classical endpoint-to-peak bound” 放入摘要；已有 P5 的受控模拟、日频与回溯概述。|**搬入**|采用 V8 的动机→发现→具名证据顺序和短句。去掉数学创新口吻；加入 P5 日频 F 赢 7/8、完整 72 格的正确结论及 C2 实际结论。七格失败只能明确归属“另一个校准模拟”，不能使读者误以为 P5 72 格失败。不能声称两个时期都做了校准，15.0% / 329/328 仅属后期单独包装比较。|
|引言贡献段|`V8:submission-jof/manuscript.tex:42–50`；核读支持 `V8:notes/v8/CONTRIBUTIONS.md`、`contribution-review.md`、`contribution-bindings.json`。用 First/Second/Third，三点均为经验发现。|`P5:submission-jof/manuscript.tex:40–44` 以 C1/C2/C3 展开，C1 仍突出已知地板与经典 Lévy 界，句长和文献对照较重。|**搬入**|采用 First/Second/Third 形式与“结论＋数字＋表图”的写法。按本轮指令重组为：小时 FX 匹配收益与后期校准；周度及同一 FX 日频历史规则优势；平稳模拟及 C2 的机制边界。V8 原 Third 的分数/破线分歧保留为第一点和实务解释的组成部分，不保留为额外第四条贡献。|
|基本数学性质降级|`V8:submission-jof/manuscript.tex:50` 已写 “Section … defines the target and records two elementary properties used later.”；`:85–117` 保留目标、地板和经典界。|P5 的摘要和 C1 仍占用贡献位置；基本性质和出处本身不是需要删掉的证据。|**搬入**|采用任务单指定的 Section 3 一句式定位；保留公式、假设、证明、原有 crossing 诊断和经典出处，避免“新理论贡献”。本清单不修改这些对象。|
|相关文献结尾与术语|`V8:submission-jof/manuscript.tex:54–81`；短的领域定位、unverified passage 用破折号；结尾三点与贡献一致。|P5 同节较长，并以 `n.r.` 表述部分未核实维度。|**搬入**|采用短句与读者可懂的模型名；文献支持与尚未核实的维度按 P5 原证据保留。不把“所读段落未核实”写成文献不存在，也不把 V8 重复三点整段照搬而增加篇幅。|
|§7.4 校准模拟解释|`V8:submission-jof/manuscript.tex:296–303`；开头直接说不能重现持续周度损失，并将数值失败与准确性分开。|P5 `:293–303` 是 “Controlled and within-record extensions”，包含 72 格的 MISMATCH、日频及回溯；没有 V8 的 D0/D2 校准网格。|**搬入**|只搬“先说研究问题和结果”的写法与 D0/D2 结果指向。按本轮改标题为 “Does sample size explain the low-frequency losses?”，合并两个平稳模拟、日频和 C2；完整原网格在补充材料。不能把 P5 的 72 格 MISMATCH 结果移除或改成机制被证实。|
|§8 实务含义|`V8:submission-jof/manuscript.tex:306–318`：三条粗体建议分别为匹配历史基准、短周度样本使用修正秩 F、共同报告分数和破线；有 36.5% 和 376/360 证据。|`P5:submission-jof/manuscript.tex:307–315` 为三个长段；P5 表注明确历史规则赢分数不保证覆盖率，日频 F 自身有破线。|**搬入**|采用三个短建议＋一句对应证据的格式。将“default to”落在验证基准/比较程序上，并保留 P5 对 F 自身破线和未测量运营收益的边界；不能据优于 QR 自动授权部署 F。36.5% 原范围必须保留，不能称普遍上界。|
|Table 6 决策图|`V8:submission-jof/manuscript.tex:321–328` 将 financial / simulation / action 并列，小时机制明确 unresolved，周度损失未重现。|P5 `:318–328` 已有同一做市商日频、较长 H 的回溯反例及非部署政策说明，但没有 C2 一栏。|**搬入**|采用 V8 的“证据→对应模拟→验证动作”紧凑结构；以 P5 全部行与日频例外为底，并按 C4 加日频/C2 两列。不能恢复 V8 的“小时长历史才有益”普遍边界；P5 长 H 和日频 QR4 例外须可见。|
|Limitations 文字|`V8:submission-jof/manuscript.tex:332–342` 将限制集中为四段；包括单做市商、先见原评估期、2015 回顾性、共用报告体系、Treasury 下载版本回放、非因果、无覆盖保证、无交易/资金收益及七格模拟失败。|P5 `:334–343` 更详述重叠回溯、后选惩罚、原始 p 值、没有真实成本；日频 last-record 口径也在 Data 中。|**搬入**|使用 V8 紧凑分组，逐条保留本轮八项必留限制，并补 P5 扩展回溯与 2015 均非前瞻、嵌套且既往评分覆盖、后选惩罚；保留同一 FX 日频的非时区/市场收盘/盘中峰值边界。V8 的“future separate experiment”不能用来掩盖本轮实际 C2；是否解决仅按 C2 输出。|
|结论文字|`V8:submission-jof/manuscript.tex:347–351` 两个短段，首句就是历史规则难打败，具名重述匹配收益、校准、周度负面及破线分歧。|P5 `:347–355` 三个长段，重述边界与未来工作较多，已有较长 H/日频例外、72 格 MISMATCH 和回溯。|**搬入**|采用短而直接的首句和三条主线，补日频、P5 全模拟和 C2 的实际结论。不能照搬到只剩原两个时期，也不能写成独立三次验证。未来工作集中 Limitations / AUTHOR-TODO，结论不新增因果或运营收益。|
|Figure 1 千分位|`V8:notes/v8/figure-sources/endpoint-peak.tex:10–18`；`V8:submission-jof/figures/v8-endpoint-peak-example.pdf`；凭据 `V8:notes/v8/figure1-format-check.json`。五个标签为 40,600 / 49,500 / 58,500 / 67,400 / 76,300。|P5 正文仍包含 `figures/v7-endpoint-peak-example.pdf`，源为 `P5:notes/v7/figure-sources/v7-endpoint-peak-example.tex`，五标签仍是科学记数法。|**搬入**|只搬格式。C0 再次只读比较：两份图源替换右对齐纵轴标签字符串后完全一致；不换观察窗、不改坐标/曲线/数据。原冻结选择 `notes/v7/example-selection.json` 不改。后续重新编译并看图，不直接以旧 PDF 的 QA 代替 v9 QA。|
|Cover letter 写法|`V8:submission-jof/cover-letter.md`；一页源/产物 `cover-letter.tex` / `cover-letter.pdf`；首段用一句话写 14.8% / 16.6% 与周度结果，第二段说明 Journal of Forecasting 的比较预测评估定位。|`P5:submission-jof/cover-letter.md` 先请求审稿，随后约五段；明确受控模拟未支持、同源日频非纯频率识别、重叠回溯。|**搬入**|采用 V8 的两段开头与简明经验定位，补 P5 的三个扩展及 C2 后的真实结果。保留单独校准与失败格说明、作者占位符；不得整封复制而丢 P5 边界。C6 再做一页编排。|
|旧 Cover letter 二进制与旧链接|V8 的 `cover-letter.pdf`、`manuscript-preview.pdf` 及 `revision-v8` 可用性链接。|P5/v9 的证据与分支对象不同。|**不用**|旧 PDF 只作排版参考，不充当 v9 投稿成品。正文、README、letter、源包和代码链接由 C6/C7 指向 `revision-v9` 并重新检查。|
|三角色 15 条模拟审稿与逐条回应|`V8:notes/v8/mock-methodology.md`、`mock-finance.md`、`mock-editor.md`；合并正文 `mock-referees.md`；结构化 15 条 `mock-responses.json`。均为同模型内部角色模拟，不是 Claude、外部审稿或期刊意见。|P5 有另一组三角色各 9 条、共 27 条；精确来源 `P5:notes/revision-v8/review-A-editor.md`、`review-B-econometrics.md`、`review-C-risk-manager.md`，回应 `internal-review-2.md`。两组不能用“已有审过”互相覆盖。|**搬入**|在 C5 的 `notes/v9/referee-check.md` 与 P5 27 条合表，保留来源 ID 和每条实际定位。下节逐项列 V8 的 15 条不可漏项；C0 不创建该 C5 文件，也不启动新审稿。|
|D0/D2 完整校准模拟与设计|`V8:protocol/v8/mc-design.md`；`results/v8/mc/{calibration.json,experiment-settings.json,summary.csv,summary.json,predictions.json,analysis-facts.json}`；现成文稿 `notes/v8/mc-supplement.tex` 及数字绑定 `mc-supplement-bindings.json`。|上述 V8 特有路径在 P5 不存在；P5 72 格使用不同 DGP/网格、32 重复和不同失败合同。|**放补充材料**|按 C4 独立一节呈现这次校准设计的全部 24 格与 D1 失败，不与 P5 的 72 格拼成同一种设计；主文仅用合并图/简短比较引用。原始设计/输出保持冻结；具体迁入路径由后续实施确定。|
|D1 数值失败记录|`V8:notes/v8/numerical-failures.md`、`results/v8/mc/analysis-facts.json`、`formal/replicates.json`、`formal/worker-logs.zip` 与 manifest；见第 4 节。|P5 72 格的 selected method tasks 完成，仍有 1 个 QR4 candidate FAILED；这与 V8 的七个整格 FAILED 不是同一状态。|**放补充材料**|保留失败格、失败阶段、lambda、停止条件和诊断缺失；不补跑、不换解算器、不把部分重复汇成成功格。不能将 failure 叙述照搬到 P5 整个网格。|
|D0“无条件信号”解释及模拟成功因果说法|即使原任务曾提出 no-signal 假设，V8 已在 `protocol/v8/mc-design.md:24,74` 与 `notes/v8/mc-analysis.md` 指出常方差不代表没有水平状态信息；oracle 明显优于 F。|P5 的同方差过程也不能被用来声称“条件信息不应有用”。|**不用**|统一写 **“constant-variance AR(1) levels, where the peak depends on the current position”**。不用“no signal / no conditional information”描述 D0；不把平稳模拟未重现损失写成已证明真实损失由不平稳导致。|
|V8 的整本生成材料、旧统计与发布凭据|`V8:notes/v8/final-prose.md`、`writing-*.json`、旧 compilation/package/remote receipts。|它们绑定 V8 的源、15/25 页产物及旧分支，不绑定 v9。|**不用**|用于定位/参考，不整份搬入作为 v9 已通过的证据。后续写法、编译、逐页 QA、测试和远端一致性必须针对 v9 自己重新产生。|

## 3. 15 条模拟审稿的具体保留项

以下 ID 来自 `V8:notes/v8/mock-referees.md` 的回应表及 `mock-responses.json`。处置均为“搬入 C5 核对表”，不是认定问题已经解决。P5 的相关项只是合并线索，最终 C5 须保留原 27 条逐项记录，不能仅留这些主题。

|V8 ID / 角色|具体问题与原回应|v9 所需实际核对 / 目标位置|与 P5 衔接|
|---|---|---|---|
|M1 方法|14.8% 匹配与 12.7% rolling 比较不同；校准须双方都包装。|摘要/贡献/Table 3 每一收益都命名 F 历史和更新时间；15.0%、329/328 只属于后期已包装比较。|P5 的 R1/R6 与新回溯具名参考保留。|
|M2 方法|Treasury 原 DM p=0.00761 与原 72-contrast Holm p=0.32，另有两主比较族，不能混用。|Evaluation 与表注保留各自 family；P5 回溯的 raw normal-HAC 不继承旧调整。|P5 B5/B9、R5；不是新增检验请求。|
|M3 方法|2015 规则设计于原结果被查看之后；“再出现”只表示记录内稳定性。|Limitations、结果和回溯表注写明后见设计、重叠与后选惩罚，不授予独立/前瞻复制地位。|P5 A3/B1/B6/C7、R4。|
|M4 方法|52 个重叠 validation origins、34 回归系数、六候选；181.4% 最差损失不能隐藏。|方法/周度表完整保留短验证与配对 HAC 一标准误规则；更长验证列 AUTHOR-TODO。|P5 R2/R7；保留各程序不同失败合同。|
|M5 方法|七个小时校准模拟格失败；frequency/validation/volatility 联动。|§7.4 和补充材料区分“未完成数值接受”与“预测差”；D0/D2 只支持完成格范围内结论。|P5 A1/B2/B3/C9；C2 另按冻结设计，不能倒写原模拟。|
|F1 金融|被动观测路径上的报告评估不等于库存干预政策。|§8/Table 6 与 Limitations 不许声称最优限额、干预收益或生产 fallback。|P5 A8/C1/C4/C8、R6。|
|F2 金融|单 market-maker client flow 与相关公共类别不是独立做市商样本。|Data/Limitations 保留测量单位、同源类别和单做市商；日频固定源不增加做市商数。|P5 R3/R4 的同源和嵌套边界。|
|F3 金融|weekly fair-value、long-minus-short 总量会受估值/净额/报告组成影响。|Data 和补充元数据保留定义；不将类别峰值当个体 gross exposure 或识别交易调整。|P5 Data、C6/R6 的测量界限。|
|F4 金融|H 是 source records，FX 缺口、周度和日频带来不同物理期限；漏掉观测间峰值。|方法在 H 定义旁交代记录钟；日频是完成日 last-record proxy，非 verified close/intraday maximum。|P5 C5/C6、R3。|
|F5 金融|loss、breach frequency/severity、unused allowance 不能直接变成资金/干预效用。|§8 联合报告，Limitations 保留无交易/资金收益；19:1 是评价权重，非实际成本。|P5 C2/C3/C4、R6。|
|E1 编辑|峰值实证应用是贡献；标准预测法、地板和经典界不构成新方法。|First/Second/Third 及 letter 用经验发现，保留既有标题为当前选择，标题变更记作者事项。|P5 A4/A5/A6、R1。|
|E2 编辑|13 类不等于 13 位独立交易商；外推需要独立做市商/前瞻数据。|Limitations/作者事项保留；本轮不新增数据补强。|P5 单源、相关聚合和外部验证缺口。|
|E3 编辑|V8 17 complete / 7 failed，P1/P3 未支持，P2/P4 不可评估，不解释实证机制。|完整补充 24 格及预登记状态；主文只以完成格支持“样本短本身未重现大损失”；机制句等 C2。|P5 A1/B2/C9 的 72 格 MISMATCH 同样保留。|
|E4 编辑|引言与文献结尾重复贡献；旧 132-word 摘要数字密集；图 tick 可读性。|C3/C4 减重复、短句、单图、千分位；旧评论的 132 words 是评论当时快照，V8 最终摘要凭据为 147 words，不能当当前计数。|P5 正文篇幅与 C4 18/30 页上限，最终再测。|
|E5 编辑|README、availability、AUTHOR-TODO 与 v8 路线须一致；文档复现和受限数据重跑分开。|C6/C7 全部指 `revision-v9`，保留作者/ORCID/funding/conflict/AI 占位符；不推定许可或真实投稿已完成。|P5 A9、R8；旧包 PASS 不自动继承。|

## 4. D0/D2 的具体内容，以及 D1 的失败说明

V8 这次设计为 `D0,D1,D2 × W={52,260,720,2880} × p={4,33}`，共 24 格；H=6，tau=0.95，每个完整格 100 次重复、每次 500 origins，有限 oracle 每个 origin 使用 2,000 条未来路径。D0/D2 的 AR 水平过程来自 Treasury 原 pre-validation prefix；D1 来自 FX prefix 并含 hour shape。其源是 `V8:protocol/v8/mc-design.md`、`results/v8/mc/experiment-settings.json` 与现成补充源 `notes/v8/mc-supplement.tex`。这与 P5 的 72 格受控 factorial grid 不同，不能合并分母、MCSE、IQR 或成功率。

下表直接抄取 `V8:results/v8/mc/summary.csv` 的 `qr_median_pct` / `oracle_median_pct`，仅显示一位小数；负数表示相对 F 的平均 pinball loss 降低。每行两格均 COMPLETE，完整 IQR、win frequency、breach、I 和 oracle 结果仍须整体进入补充材料。

|DGP|W|p=4 QR/F 中位变化 %|p=33 QR/F 中位变化 %|Oracle/F 中位变化 %|
|---|---:|---:|---:|---:|
|D0 常方差 AR(1) 水平|52|-0.2|+1.1|-30.0|
|D0 常方差 AR(1) 水平|260|-15.0|-2.2|-24.6|
|D0 常方差 AR(1) 水平|720|-18.8|-14.6|-23.3|
|D0 常方差 AR(1) 水平|2880|-21.8|-19.8|-23.6|
|D2 周度校准 AR-GARCH|52|+1.2|+0.4|-29.5|
|D2 周度校准 AR-GARCH|260|-13.9|-0.8|-25.6|
|D2 周度校准 AR-GARCH|720|-18.6|-12.4|-24.8|
|D2 周度校准 AR-GARCH|2880|-20.1|-20.6|-24.1|

D0 必须表述为 **“constant-variance AR(1) levels, where the peak depends on the current position”**。oracle 在 D0 比 F 低约 23%–30% 正是条件水平信息有用的归档结果；不能把它视为无信号 null 被预测方法“意外打败”。D2 W52/QR33 为 +0.3528682097196367%，未达到预登记的 >5% 损失，W2880 为 -20.562859332263795%。这些平稳过程没有重现真实周度的大损失；它们并未识别真实机制。

七个 D1 整格失败均保存 `QuantileFitError:NONCONVERGENCE`，最小声明惩罚 lambda=0.001：

|D1 W|p|首次失败 repetition（0-based）|阶段|处置|
|---|---:|---:|---|---|
|2880|4|1|evaluation|FAILED 整格保留|
|720|4|3|validation|FAILED 整格保留|
|260|4|4|validation|FAILED 整格保留|
|52|4|10|validation|FAILED 整格保留|
|720|33|17|validation|FAILED 整格保留|
|2880|33|32|validation|FAILED 整格保留|
|260|33|56|validation|FAILED 整格保留|

来源为 `V8:notes/v8/numerical-failures.md`、`results/v8/mc/analysis-facts.json`，原日志归档为 `results/v8/mc/formal/worker-logs.zip`。唯一完整 D1 格是 W52/p33，中位变化 +0.20004059890593728%。原解算器在 10,000 次迭代内未同时取得 ADMM residual 与 feasible-dual Fenchel-gap 接受条件；这既不证明优化问题无解，也不证明预测准确性差。归档未保存 exception diagnostics，四个 p4 失败亦无精确 refit context，不能编造最终 residual/gap，不能未经授权重跑补回。整格中位数/IQR/胜率/破线字段继续为空，不用先完成的部分重复代替。

`V8:results/v8/mc/predictions.json` 的原判定全部保留：P1/P3 = `NOT_SUPPORTED`，P2/P4 = `UNASSESSABLE`。P2/P4 是需要的小时格未完成，不是统计拒绝。原模拟没有被本次 C0 重算或修复。

## 5. P5 底稿必须原样保留的新增证据

|P5 证据与精确来源|本次核读到的范围|不得被 V8 替换的内容|
|---|---|---|
|`P5:results/revision-v8/wp3/README.md`、`summary.csv`、`support.json`；`protocol/revision-v8/wp3-mechanism-design.*`；补充 `submission-jof/supplement.tex:1396` 起|72 格受控设计；每个 regression 的 clear gains 为目标区 2/12、区外 6/60；32 repetition streams / 72 issues per repetition；6912 selected method tasks 完成，18431 COMPLETE 与 1 FAILED candidate。|完整网格与 MISMATCH；QR33 mandatory candidates 和 QR4 eligible-completed selector 的失败合同不同，1 个 QR4 候选失败不能说成 selected method task 失败；也不能用 V8 整格失败政策重新改判。|
|`P5:results/revision-v8/wp4/README.md`；补充 `submission-jof/supplement.tex:1482` 起；主文 `:129,301`|930 nonempty source-naive days、501 issues；F 赢 7/8，QR33 输 4/4；例外 QR4 W260/H6 -2.973993%，37/30 breaches。|完整八格、例外及 F 自身破线；last-record/partial-day/unknown timezone-vintage 口径；不是纯频率因果识别，也不是日内最大值。|
|`P5:results/revision-v8/wp5/README.md`、`THREE_WINDOWS.md`；`protocol/revision-v8/wp5-fixed-prefix-design.*`；补充 `submission-jof/supplement.tex:1512` 起；主文 `:303`|7368 origins 的 full-prefix 包含旧 1440-origin 回溯；H6 QR33 matched -12.166527%，416/282；rolling -5.295735%，416/387；raw rolling p=0.05505865409429612。|三段重叠/已查看窗口的全部范围、长 H 结果与未有字段的 NA；后选惩罚；无新增独立复制 credit，不能因 V8 简短措辞删除暴露事实。|
|`P5:notes/revision-v8/internal-review-2.md` 与三份 review；`wp6-acceptance.json`|三角色各 9 条，共 27 条；20 MAJOR / 7 MINOR，27 条均有回应或保留理由。|不得只保留 V8 15 条；旧回应 accepted 不是科学缺口已经解决，C5 要逐项查 v9 真实落点。|

## 6. 真实数据数字门槛与写法快照差异

本子任务只核对写法用到的核心锚点，完整“全部真实数据核心数字对照表”由 C0 的数字核对任务另行完成，不能以这里的简表替代。以下五个归档文件已对 V8 与 P5 进行只读逐字节比较，均完全相同：

|两版相同的精确相对路径|写法锚点 / 不能混用的口径|
|---|---|
|`results/revision-20261022/paired-comparisons.csv`|后期 matched -14.766762552613885%、376/360；后期 rolling -12.660126412969763%；Treasury +50.78571256749063%。|
|`results/supervisor-20261023/r6-writing-hac-20261023/results.json`|earlier matched -16.62356533682211%；earlier rolling +3.1681985293173343%；不是扩展 full-prefix。|
|`results/revision-20261023/v6/wp2-findings.json`|后期双方 delayed calibration -14.99691078803782%、329/328；不是未经包装的 matched pair，也没有早期包装结果。|
|`results/supervisor-20261023/e5/descriptive-summary.json`|additional 12-series panel，expanded QR33 输 34/48；不是所有真实数据格子的总分母。|
|`results/supervisor-20261023/r6/assessment.json`|181.39452368014167% 属 earlier weekly conservative selector 最差格，不是 median 或普遍最大风险。|

本次未发现上述真实归档源的数字冲突；这不宣称完成了所有真实数据逐项核对。若完整 C0 对照发现任何真实数字不一致，须停在 C0 查明原因，不能以显示四舍五入或写法偏好跳过。

任务单开头 2.3% / 14.6 词属于给定写法快照；V8 绑定当前正文 SHA256 `2f34250947a157ca81b65d7e06352a1e1b397ce45093a3757379f7261e7094aa` 的 `notes/v8/writing-abstract-final.json` 实际保存 185 句、2251 词、3 句标记、1.6216216216%、平均 12.1675675676 词、>40 词为 0、摘要 147 词/9 数字。不能把旧 132-word 摘要评论或任务单近似快照当作当前复算结果。`notes/v8/writing-metric-contract.md` 明确 Introduction–Conclusion、去表图/图注/展示公式/声明/参考文献、同一 full-stop splitter；其口径不同于旧 v7 的 negation / >35-word checker。C3 应在 P5/v9 同口径重测 before/after，并另测 `primary` ≤3，不能用两份不同统计法的 JSON 直接相减。本 C0 未运行统计器。

## 7. 待作者决定与执行交接

无需等待答复：按当前标题继续；保留作者、ORCID、资金、利益冲突、AI 声明所有占位符；保留独立做市商、真正前瞻数据、更长验证、gross exposure/估值/成本与干预验证等未解决问题；PR #3/#4/#5 后续处置留作者决定。没有外发消息、Claude/跨模型审查或期刊接触。

C1–C7 后续执行者应以本清单的“处置”列作迁移导航，并以 P5 全数字核对、C2 冻结设计和实际结果为硬约束。本清单没有把任何后续写作、C2 结论、图表生成、模拟迁入、审稿合表或投稿包宣称已完成。

## 8. 本子任务实际核读的文件清单

以下记录实际打开的文本/JSON/CSV；列出整个文件不表示逐行重新验证全部内部记录。`rg --files` 目录发现不等于核读内容；旧 PDF 仅核实路径存在，C0 未渲染。

- 外部任务源：本文件第 1 节所链两份导师任务单。
- V8 正文/letter：`submission-jof/main.tex`、`submission-jof/manuscript.tex`、`submission-jof/cover-letter.md`。
- V8 贡献/写法：`notes/v8/CONTRIBUTIONS.md`、`final-prose.md`（段落定位）、`contribution-review.md`、`contribution-bindings.json`、`abstract-final.json`、`writing-final.json`、`writing-abstract-final.json`、`writing-metric-contract.md`、`b4-check.json`、`author-decisions.md`。
- V8 审稿：`notes/v8/mock-methodology.md`、`mock-finance.md`、`mock-editor.md`、`mock-referees.md`、`mock-responses.json`。
- V8 Figure 1：`notes/v8/figure1-format-check.json`、`notes/v8/figure-sources/endpoint-peak.tex`。
- V8 模拟：`protocol/v8/mc-design.md`、`results/v8/mc/main-results.md`、`summary.csv`、`predictions.json`、`experiment-settings.json`、`analysis-facts.json`（定位字段）、`notes/v8/numerical-failures.md`、`mc-analysis.md`、`mc-supplement.tex`、`mc-supplement-bindings.json`（定位字段）。
- P5 正文/letter/图源：`submission-jof/main.tex`、`submission-jof/manuscript.tex`、`submission-jof/supplement.tex`（节定位）、`submission-jof/cover-letter.md`、`notes/v7/figure-sources/v7-endpoint-peak-example.tex`。
- P5 扩展：`results/revision-v8/wp3/README.md`、`results/revision-v8/wp4/README.md`、`results/revision-v8/wp5/README.md`、`results/revision-v8/wp5/THREE_WINDOWS.md`。
- P5 审稿：`notes/revision-v8/review-A-editor.md`、`review-B-econometrics.md`、`review-C-risk-manager.md`、`internal-review-2.md`、`wp6-acceptance.json`、`check_wp6_reviews.py`（只读定位回应文件，未运行）、`wp7-cover-letter-response.md`。
- 两版共同归档：第 6 节列出的五个文件，均只读按字节核对。
- 环境辅助：全局 using-superpowers skill（该文件明确派发子任务忽略其工作流）；记忆注册表仅用于定位旧版范围，当前判断全部回到上述本地源核实。未调用 Claude skill 或任何跨模型工具。

## 9. 来源完整性快照

|V8 相对路径|本次只读 SHA256|
|---|---|
|`submission-jof/manuscript.tex`|`2f34250947a157ca81b65d7e06352a1e1b397ce45093a3757379f7261e7094aa`|
|`submission-jof/cover-letter.md`|`f314e5cde0b0dac82e7ec7a176fbcca0ed72b3f3812d309bac262d9cb01843ef`|
|`notes/v8/mc-supplement.tex`|`4d6632c358750b0dece0caeb81cb666b2b573ddf58fa9b21855de77bcc3916c4`|
|`results/v8/mc/summary.csv`|`ca6bbe25cd02a5fa7dcbee5e55498cb0b86e16394292b7cfe2b9dedfb7e02e0f`|
|`notes/v8/mock-responses.json`|`612e5c33c059c1a52d5131f759b2b69d1328ea542279c846db2acc7209ef28c1`|
|`notes/v8/figure-sources/endpoint-peak.tex`|`66b50f95179b4e30b6f45089fb69877fa060729297e7e81b51ab7890d2e01169`|


## 10. v9最终处理状态（C5）

本节是 C4 提交 `e6a3c98` 后的 C5 迁入收口快照，只追加处置状态，不改写上文 C0 的历史清单和当时预期。以下路径均以本文件第 1 节的 v9 目录为根。已完成表示当前文件中有实际落点；科学缺口、失败状态和后续阶段分别列明。未运行新的拟合、诊断、预测、模拟或统计分析。

|原 C0 迁入项 / 保留项|C5 当前状态|已完成的具体路径与定位|最终边界 / 尚待处理|
|---|---|---|---|
|摘要|已完成 C3/C4|`submission-jof/manuscript.tex`，`abstract` 环境；三点主线见 `notes/v9/thesis.md`。|采用发现先行；匹配 14.8%/16.6%、后期校准 15.0% 与 329/328 分开。已加入平稳控制出现损失及 C2 机制未识别结论，未复制旧摘要的过时模拟概括。|
|引言三点贡献|已完成 C3/C4|`submission-jof/manuscript.tex`，`sec:intro` 中 First/Second/Third；中文/英文发现、文献与边界见 `notes/v9/CONTRIBUTIONS.md`。|三点均为经验发现。第三点明确不同平稳设计给出不同结果，未将标准方法、基本数学性质或不稳定性假说写成已证新理论。|
|基本数学性质降级|已完成 C3|`submission-jof/manuscript.tex`，引言末尾指向 `sec:target`；目标与基本性质仍在 `sec:target`，证明在 `submission-jof/supplement.tex` 的 `sup:floor`、`sup:levy`。|保留公式、假设、经典出处和证明；引言使用“defines the target and records two elementary properties used later”，未列为创新。|
|相关文献结尾与术语|已完成 C3/C4|`submission-jof/manuscript.tex`，`sec:literature`、`tab:literature`；结尾直接定位 matched peak forecasts 与 ranking stability。|表中 dash 仍表示 consulted passage 未核实，不等于相关文献不存在；既有方法身份和来源边界保留。|
|§7.4 校准模拟解释|已完成 C3/C4|`submission-jof/manuscript.tex`，`sec:extensions`：“Does sample size explain the low-frequency losses?”；模拟图 `fig:mechanism`。|分别呈现旧 D0/D2、PR5 WP3 和 C2 的菜单、时钟与 estimand。完整网格均保留；旧近持平不能覆盖 PR5/C2 平稳损失。|
|§8 实务含义|已完成 C3/C4|`submission-jof/manuscript.tex`，`sec:implications`，三条粗体建议。|历史基准、正确秩和联合报告分数/破线均有具名证据。普通 I 的 36.5% 保留 earlier weekly grid 范围；不声称真实资金/交易收益或最优干预。|
|Table 6 决策图|已完成 C4|`submission-jof/manuscript.tex`，`tab:map`，新增 same-record daily 与 new stability study 列；逐值核对见 `notes/v9/main-number-audit-c4.{md,json}`。|日频 7/8、C2 +116.2%/+121.4% 和 W260 不可用均可见；没有恢复“长小时历史才可能有益”的普遍边界或部署承诺。|
|Limitations 文字|已完成 C3/C4|`submission-jof/manuscript.tex`，`sec:limitations`。|保留单做市商、已看评估期、2015 和 full-prefix 回顾性/重叠、同源周度类别、Treasury 下载 vintage、日频口径、非因果/无覆盖保证/无运营收益；新增不同模拟设计与人工 wrap、资格/优化失败及模型近似边界。|
|结论文字|已完成 C3/C4|`submission-jof/manuscript.tex`，`sec:conclusion`。|直接重述小时匹配收益、低频历史规则优势及平稳过程也可出现损失，机制仍未识别；未增加独立复制、因果或运营收益。|
|Figure 1 千分位|已完成 C4|`submission-jof/figures/v9-endpoint-peak-example.pdf`（及 PNG），正文 `fig:example`；`notes/v9/c4-figure-audit.md`、`results/v9/figures/scalars.json`。|保留 `notes/v7/example-selection.json` 的同一七点、窗口、日期和报告值，使用原生 USD millions 与普通逗号刻度；v9 自身渲染/目视凭据已生成，不继承旧 PDF 的 QA。|
|Cover letter 写法|**C6 pending**|当前 `submission-jof/cover-letter.md` 等旧文件仅为待更新对象；当前正文定位不能充当 letter 已完成。|仍须按最终三条发现、全部失败/未知状态和 v9 来源重写并做一页编排；不将计划算完成。|
|旧 Cover letter 二进制与旧链接|已执行“不采用旧成品”；**C6 pending** 链接/产物统一|旧 V8 PDF 没有被当作 v9 的核验成品；v9 当前主文/补充材料有独立 C4 凭据。|最终 letter PDF、README、availability 与投稿源包链接的统一及检查仍待 C6；最终包验收和远端发布属于 C7，未完成。|
|三角色 15 条与 P5 27 条审稿矩阵|**C5 pending：正在合表，尚未落盘**|指定目标为 `notes/v9/referee-check.md`；本追加核读时该文件尚不存在，负责代理正在逐条对照 42 条来源。|不把旧版“accepted”或当前写作计划当完成。须由实际合表保留 V8 M1–M5/F1–F5/E1–E5 和 P5 27 条的来源 ID、真实落点与未解缺口；该文件完成后由主任务补确认。|
|D0/D2 完整校准模拟与设计|已完成 C4|原字节导入 `results/v9/legacy-calibrated/`，来源/HEAD/branch/SHA/字节见其 `README.md`、`manifest.json`；`submission-jof/supplement.tex` 的 `sup:v9-legacy-mc` 输入 `generated/v9-legacy-simulation-table.tex`，`tab:v9-legacy-mc`。|全部 24 计划格均列出，17 COMPLETE / 7 FAILED；QR Δ/IQR/win、I/oracle Δ、F/I/QR/oracle hits 和 infinity 频率均保留。未替换 P5 72 格、未合并重复数或不同 estimand。|
|D1 数值失败记录|已完成 C4|`results/v9/legacy-calibrated/analysis-facts.json`、`formal/replicates.json`、`formal/worker-logs.zip` 及 manifest；补充 `sup:v9-legacy-mc`、`tab:v9-legacy-failures`。|七个 D1 全格失败及 rep/stage/lambda/reason 明示；原诊断缺失仍缺失，不补跑、不换解算器，不用部分重复填中位数。|
|D0“无条件信号”及模拟成功的因果说法|已执行“不采用”，且最终机制概括已纠正|`submission-jof/manuscript.tex` 的 `sec:extensions`；`submission-jof/supplement.tex` 的 `sup:v9-legacy-mc`；导入 `README.md`。|统一为“constant-variance AR(1) levels, where the peak depends on the current position”；不称 no signal，不将旧近持平推成不稳定性已被识别。|
|V8 整本生成材料、旧统计及发布凭据|已执行“不整份继承”|v9 自身写法凭据 `notes/v9/writing-{before,after-c3,final-c3,after-c4}.json`；版面 `c4-main-layout.json`、`c4-main-review.md`、`c4-supp-layout.md`；数字审计 `main-number-audit-c4.{md,json}`。|旧源仅作历史证据。C4 的当前版面不是 C6 源包或 C7 最终逐页/测试/远端凭据。|
|P5 WP3 完整受控网格|已保留 C4|`results/revision-v8/wp3/{summary.csv,summary.json,support.json}`；补充 `sup:v8-mc`，原 `generated/v8-mc-full-table.tex`、`v8-mc-four-table.tex` 全行保留；主文 `sec:extensions`、`fig:mechanism`。|72 个设计格及 MISMATCH 保留；6912 selected method tasks 完成与 1 个 QR4 candidate 失败的合同不混用。已明确其 QR33/H6 的 W52 大幅损失。|
|P5 WP4 同源日频八格|已保留 C4|`results/revision-v8/wp4/`；补充 `sup:v8-daily`、`generated/v8-daily-results-table.tex`；主文 `sec:data`、`sec:extensions`、`tab:map`。|F 赢 7/8、QR33 四格全败和 QR4 W260/H6 例外保留；同源聚合并非独立做市商或纯频率识别。|
|P5 WP5 全前缀及三重叠窗口|已保留 C4|`results/revision-v8/wp5/{README.md,THREE_WINDOWS.md}`；补充 `sup:v8-backcast`、`generated/v8-three-window-table.tex`、`v8-backcast-complete-table.tex`；主文 `sec:limitations`。|7368 origins 包含旧 1440 窗口；后选惩罚、既往评分暴露、长 H 反例和 NA 均保留，不授予额外独立/前瞻复制 credit。|
|C0 共同真实数字门槛|已完成 C0；C4 显示绑定另核|`notes/v9/real-number-reconciliation.{md,json}`；`notes/v9/main-number-audit-c4.{md,json}`。|共同真实数据核对与 P5 独有日频/回溯证据分列；C2 新模拟不冒充双 v8 共同数值。|
|C2 全诊断与预测/失败表|已完成 C2/C4|`results/v9/nonstationarity/postrun/{predictions.json,analysis/report.json}`、`audit/{summary.json,failures.json,f-benchmark-cells.csv}`；补充 `sup:v9-stability` 和 `tab:v9-stability-diagnostics`、`tab:v9-stability-w52`、`tab:v9-stability-w260`、`tab:v9-stability-f`。|15 条诊断、104 conditional cells 和 52 F cells 保留；daily NONREGULAR_NULL、hourly GARCH_OPTIMIZATION_FAILED 及两个 W260 QR33 整格 FAILED 31/32 不改成稳定或完整结果。|
|Data/code availability、README 与版本源包|**C6 pending**|正文现有 `Data and code availability` 段及 `submission-jof/` 现有说明是待最终联检对象。|当前 `revision-v9` 字样不等于链接、许可、源包、作者占位与最终文稿已统一通过；C6 完成前不标 package PASS，C7 发布亦未执行。|

**E3 的最终纠正（覆盖其后续执行预期，不删除原评论）。** 上文 C0 第 3 节 E3 的“主文只以完成格支持‘样本短本身未重现大损失’”只反映当时对旧 D0/D2 网格的预期，不能作为合并后的共同结论；任何“平稳模拟不能损失”或“样本短本身无害”的泛化均已在最终主线中弃用。原始证据的逐行核对保存在 `results/v9/nonstationarity/prior-stationary-reconciliation.json`：旧 D0/D2 的 W52/QR33 接近持平，但 P5 WP3 的 QR33/H6/W52 九格已为 +113.45974253719095% 至 +135.5188592993867%（ratio of across-repetition mean losses）。C2 的 W52 恒定控制中位数为 +116.24327967680179%，切换为 +121.40097999787356%（先 repetition median，再十三来源 median）。因此不同设计不能合并，也不能用后者相近就识别真实不稳定机制。最终改写已实际落在 `notes/v9/thesis.md`、主文 `abstract` / `sec:intro` 第三点 / `sec:extensions` / `sec:limitations` / `sec:conclusion`，补充材料同时保留两批旧模拟和 C2 的全表。

**当前页数与判断来源。** C4 主文 **17 页**，凭据 `notes/v9/c4-main-layout.json`、`c4-main-review.md`；补充材料 **28 页**，凭据 `notes/v9/c4-supp-layout.md`，不冒称已经完成 C7 最终包逐页验收。C2 原始判断以 `results/v9/nonstationarity/postrun/predictions.json` 为准，解释见 `notes/v9/c2-results.md` 和 `thesis.md`：N1=`SUPPORTED`，raw 7/13、Holm13 2/13；N2=`UNASSESSABLE`；N3=`NOT_SUPPORTED`（预设 near-parity 预测不成立）；N4=`UNASSESSABLE`。N2 的两个 W260 QR33 必需格和 N4 两个 FX 诊断的缺失均未补跑，不用部分成功替代。

本次追加前原清单共 **28226 bytes**，SHA256=`92fa4a8f7b3e5de89129ecb917756f6ef598efd2a0968bb4968e8c8d6514bc64`；追加后再次逐字节比较确认该原始前缀不变。仅修改本文件末尾；旧目录、结果归档、研究代码和论文源均未改写，未提交。

### C5 合表落盘确认

`notes/v9/referee-check.md` 已完成并独立只读复核：15+27=42行、42个唯一ID，遗漏0、重复0；三份当前源哈希与八份意见来源均吻合。上表“尚未落盘”为此前读取时点的历史状态，由本确认收口。未解科学问题保留在Limits与T1–T9；C6/7尚待后续验收。

### C6 投稿包收口

旧cover letter仅取简洁定位，现已重写为v9的211词、一页native稿；作者签名仍占位。title-page版本链接已统一、6关键词/32字符running title通过；31个bib键匹配31正文引文/打印项。README、两源快照、10递归表输入与23成员ZIP已按现源逐字节验收，详见`c6-metadata.md`/`c6-package.json`。上表C6 pending至此由实际产物收口；C7尚未预判。

### C7实际科研内容收口

主文17/补充28/title1/letter1，47页逐页检查；1463tests与1068subtests通过。公开8d0b676a...与原本地e094bf6...整树3451文件/227358259bytes完全一致，全部文件逐字节及SHA256核对通过。见publication-first-tree.json。原本地设计历史没有由浏览器镜像传远端，私有原对象留在新clone；最终仅凭据/交付metadata同步的head和结束时刻由最终回复收口。原各项pending已按实际产物处理，科学NA/失败及作者决定继续保留。
