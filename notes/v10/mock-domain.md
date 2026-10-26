# E6 同模型内部领域审阅：Journal of Forecasting 视角

身份与范围：**same-model internal domain reviewer**。这不是 Journal of Forecasting 编辑或外部审稿人的意见，也不是跨模型、Claude/Cloud 或独立数据复现。仅依据当前主稿、补充材料、AUTHOR-TODO、已有官方期刊定位记录及保存的 CFTC/成本汇总，提出以下恰好五项主要关切。没有读取金融数组、下载数据、计算新结果或修改论文。E5 的数字绑定通过不等于以下外推和经济解释问题已经得到实证解决。

审阅时间：2026-10-25 UTC；E6 委派开始 00:07:12 UTC，文件读取核对 00:08:30 UTC。对应 E5 提交 `11cda8a` 后快照：`submission-v10/manuscript.tex` SHA-256 `39fc54af093c0367f7877aa96b3b8f8c742f16ca076ec8ab31cfd9d7ea2ec672`；`supplement.tex` SHA-256 `78be8bd270aeb5061d57f6796d8906019573ba765a37b3edf7711f40e2a92e0b`；`AUTHOR-TODO.md` SHA-256 `284ec2fcc6a4092b0a5f17dd2e0f030f55178f5fd8ca3c144c4f2bb730e12529`。下列行号以这些字节为准。

## V10-D1 — 跨报告系统扩展不能承担个体 dealer 外部有效性的证明

**理由与重要性。** CFTC 是另一个官方报告体系，因而扩大了测量与来源范围；其 Dealer/Intermediary long-minus-short 仍是报告类别的合约净额。NY Fed 类别之间、两个体系之间可能共享经济风险和共同市场驱动，不能把来源不同转换为独立 dealer 样本。17 个代码、34 个 history cells 或 98 个 MCS tasks 都不是独立机构的重复实验。文章以 dealer limits 为动机，读者容易把“independent reporting systems”及跨体系重复的历史规则表现读成个体机构风险管理的外部验证，而这一层尚未建立。

**精确定位。** 主稿 `submission-v10/manuscript.tex:17` 摘要、`:23` 开篇 dealer-limit 动机、`:31` 两套 aggregate 系统、`:37` RQ2、`:80` 经验贡献、`:130` CFTC 定义及 `:332` 限制；标签 `sec:intro`、`sec:data`、`sec:limitations`。补充材料 `submission-v10/supplement.tex:1522`，标签 `sup:v10-cftc`；`:1533`，标签 `sup:v10-mcs`；`:1588`。AUTHOR-TODO `:18–23`（T2）及 `:81`（T10）。

**稿件已经缓解的部分。** 主稿31、324、332和补充材料1533、1588已明确 aggregate/related tasks 与未完成 individual-dealer validation；本关切不是指控遗漏或数字错误。MCS 90/98 的正文也保留了通常与其他方法共同入选的限定。

**写作修复。** 在摘要或首次引入 CFTC 的结果句就把证据层级写成“a separate official reporting system of related category aggregates”，并把可支持的结论限定为这些 aggregate forecasting tasks 的 benchmark pattern。保持“来源独立／另一个报告体系”与“统计独立／个体 dealer 外部验证”的术语区别；不要把90/98解释成90次独立成功或普遍最佳规则。

**仍未解决的科学问题。** 个体 dealer 的 gross inventory、机构特有约束和独立持出记录未观察。只能将此作为明确保留的外推缺口；现有披露不能变成“已满足”的结论，也不应在本轮通过新的子集或 pooled test 来补救。

## V10-D2 — CFTC 结果是历史 survivor-universe 的 economic-date replay，而非可部署的首次发布预测试验

**理由与重要性。** 合格性要求从2010至2026全程连续、literal exchange/units稳定，因此在2021 evaluation 开始时无法知道哪些代码最终满足完整筛选。规则在本次计算前冻结，能防止结果导向重筛，但不能使历史 evaluation 时点具有未来可知的 universe。全期OI排名也使用后续信息；不过本次仅17个合格代码、小于20上限，**OI排名实际没有排除额外代码，只决定顺序**，不能把它误报成这次入选偏差的主要数值来源。另一个独立问题是 Monday model clock 与 Tuesday positions/Friday releases，及修订、节假日、停摆、ION延迟：完成标签的时间控制并不自动恢复原始 first-release information set。

**精确定位。** 主稿 `submission-v10/manuscript.tex:130–132` 及 `:332`，标签 `sec:data`、`sec:limitations`；补充材料 `submission-v10/supplement.tex:1518–1520`（完整周历、17/141、rank、模型日期与实际发布日期）、`:1527`（两个获取后读取澄清），标签 `sup:v10-cftc`。AUTHOR-TODO `:81`（T10）。保存结果 `results/v10/cftc/report-values.json` 的 `contract_count=17,N=877` 与 `splits` 确认这里讨论的是该固定历史样本。

**稿件已经缓解的部分。** retrospective survivor universe、经济日期重放、Monday不代表公开可用、延迟和两个 ingestion clarifications 均已披露。因此问题属于尚未识别的 prospective estimand，而非发现模型使用未来 target 作训练、代码错误或事后修改统计阈值。

**写作修复。** 在主稿 CFTC 数据/结果首次出现时直接标明“retrospective survivor-universe, economic-date replay”，并在复述计数时区分141个观察代码、17个合格代码与未触发的top20 cap。将Monday定位为继承特征时钟的索引，不是交易员周一可发出的公开数据预测。避免用“pre-registered sample”暗示当年的可执行 universe，或用“no leakage”覆盖尚未重建的发布 vintage。

**仍未解决的科学问题。** 真正的 prospective, first-release evaluation 需要当时可知的入选规则和逐次发布 vintage。literal units/exchange稳定也不能证明长期经济合约范围及报告人组成恒定。当前证据可以保留，不应改筛选、重排年份或另补历史vintage后仍称为同一冻结试验。

## V10-D3 — 被动路径上的归一化成本区域不是机构经营成本或限额干预价值

**理由与重要性。** 当前 J 将 reserved headroom、strict breach frequency 和 exceedance 以预设偏好组合，是有用的 forecast-use sensitivity analysis。它没有观测实际资本/资金费用、违约/监管罚金或机构处理规则；一旦触线后交易、对冲或缩仓改变未来头寸，固定观察路径上的反事实“成本”也不再等于执行政策价值。尤其 `beta=b/m_F` 使同一归一化beta对应不同任务的不同原单位b；CFTC原单位是异质合约数，NY Fed/FX又是不同货币量口径。1–32/34表示所列相关任务在不同偏好下的排名范围，不是同一美元费用向量下的跨市场利润或节约比例。

**精确定位。** 主稿 `submission-v10/manuscript.tex:39` RQ3、`:47` 摘要式结果、`:80` passive scoring、`:290–305` 公式/系数/图注（标签 `sec:cost`、`fig:v10-cost`）、`:328`、`:334` 限制及 `:344` 结论；补充材料 `submission-v10/supplement.tex:1538–1541`，标签 `sup:v10-cost`；AUTHOR-TODO `:42–51`（T5）和 `:81`（T10）。保存汇总 `results/v10/cost/report-values.json#/groups` 的CFTC项固定 `primary=CFTC::QR33,c=1,planned=complete=34`，最小/最大便宜比例约为.02941/.94118。

**稿件已经缓解的部分。** 主稿296已说明按issued report且不把重叠视为独立现金流；334和T5明确是illustrative、非实测经营成本，也不主张盈利或最优干预。这里没有公式或数值不一致。

**写作修复。** 在成本公式前或图注就命名为“illustrative normalized per-report disutility on unchanged observed paths”，明确共同系数是共同归一化偏好而非共同货币收费。成本结论保持“ranking changes under stated preferences”，不要把“cheaper”提升为资金占用改善、operating savings、safe limits或交易策略价值。保留完整系数区域与固定模型，不能以各格最便宜模型作oracle结论。

**仍未解决的科学问题。** 经营成本校准和会改变路径的限额行动，需要新决策数据及行动模型。现有被动比较不能识别这些量；将这项缺口归入未完成经济验证比追加形式上的“cost PASS”更准确。

## V10-D4 — FX 匹配增益、原始 reference 反向和144.3%负面结果要求任务级结论，不能上升为普遍模型选择规则

**理由与重要性。** 同一记录上的14.8%/16.6% matched gains与较早rolling-reference +3.2%可以同时成立，说明回答依赖reference的history/update contract。144.3%是另一早期Treasury短历史结构类比，不是原来长历史主比较的相同程序复现。再加上daily聚合共同改变了物理history、horizon和时钟，新的paired菜单试验又把短history QR33损失降到近零，现有证据支持“完整forecasting procedure及benchmark定义至关重要”，不能识别“conditioning通常无效”“周频天然需要历史法”或低频机制。主稿的default benchmark建议应保持验证对照的意义，避免变成production选择建议。

**精确定位。** 主稿 `submission-v10/manuscript.tex:17`、`:43`、`:199`、`:202–211`（标签 `tab:fx`）、`:216–240`（标签 `tab:weekly`，+144.30明确different history）、`:274–282`（菜单隔离）、`:312–314`（default benchmark）、`:322`、`:326`、`:330`及`:340–342`。AUTHOR-TODO `:25–40`（T3/T4）、`:48–51`（T5）。

**稿件已经缓解的部分。** 摘要、FX表和结论都诚实报告+3.2%与+144.3%；正文还保留+31.5%和breach恶化。历史“matched gain”没有被包装为原始rolling-reference重现。本关切不是要求隐藏任一不利数字，也不是建议把不同history重新配成有利比较。

**写作修复。** 在结论/validation implication明确把F称作这些任务中应保留的matched control，而不是由本研究认证的生产fallback；以一条统一句连接“reference-dependent FX gains、不同短历史bill adverse result、menu-sensitive simulations”。保留144.3%的短历史/结构类比身份，近零simulation中位数与经验频率机制未识别的限定。各项数值不需重写或重算。

**仍未解决的科学问题。** 单个FX记录、重叠backcasts与相关weekly tasks没有提供广泛transportability或prospective selection performance。更长outer validation或可保护benchmark的选择规则仍是T3中的未来研究，不是本次菜单结果已经解决的科学问题。

## V10-D5 — JoF 的可迁移预测评价贡献需与领域用途区分；期刊分区和投稿就绪不能靠内部验收确认

**理由与重要性。** JoF范围包含预测理论、应用与计算，现稿可以作为比较完整预测程序的应用证据。但正文自己正确说明forecast tests、forecast methods与cost accounting均为既有方法；其贡献主要是特定peak response、matched-reference程序比较、菜单隔离及相关aggregate任务上的实证组合。编辑仍可能追问：这些材料给一般forecast-evaluation读者提供什么可迁移认识，而不只是金融数据表的累积？“limits”域名本身不能把位置峰值等同于经验证的监管VaR、资金流动性或操作政策。另当前官方JCR/CAS分区尚未取得认证详情，不能用“Q3达标”代替编辑适配或投稿准备。

**精确定位。** 主稿 `submission-v10/manuscript.tex:15` 标题、`:49` established methods、`:55–80` 文献及贡献、`:310–316` implications、`:357–362` 未完成作者信息；标签 `sec:literature`、`sec:implications`。AUTHOR-TODO `:8–16`（T1）、`:64–68`（T7）、`:83`（T11）。已有官方核对 `notes/v10/target-journals.md:5–15,23–30`：JoF是scope-based first target，三刊JCR/CAS全部未核实；官方Wiley范围/格式来源为 https://onlinelibrary.wiley.com/journal/1099131x 与 https://onlinelibrary.wiley.com/page/journal/1099131x/homepage/forauthors.html 。本次未重新浏览或扩大官方访问范围。

**稿件已经缓解的部分。** established-method定位、不同金融风险response、passive scoring和AUTHOR-TODO中的作者/权利/分区待办均正确。没有发现稿件声称已被JoF认可、已确认Q3或可以直接提交；内部mock意见也必须继续与真实期刊审稿分开。

**写作修复。** 让JoF定位句明确归纳一个可迁移的forecast-validation经验：比较完整调参程序时，必须同时固定mature-label timing、history/update reference，并把loss、hits和偏好区域分开解释。以此约束摘要/cover letter的贡献边界，保留established-method声明，勿夸称新预测理论、通用控制策略或监管风险有效性。作者信息、权利和分类记录应保持实际状态；不能以本内部review把T1/T7/T11自动标为完成。

**仍未解决的科学／外部事项。** 对更一般预测问题的可迁移性仍主要是论证与有限实证；期刊适配和接受是编辑决定，JCR/CAS须合法认证源按年度/类别另核，作者声明须作者本人完成。它们不是本轮新增计算或文字润色能够认证的结果。

上述五项是供root逐项协调的内部主要关切。可用更精确的claim scope处理文字部分；已经明示但尚未完成的个体dealer、first-release、经营行动及prospective证据应保持未完成状态。未提出第六项问题，也不据此要求改动冻结设计、补跑金融结果或启动外部审查。
