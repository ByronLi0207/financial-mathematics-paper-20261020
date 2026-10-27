# H5 内部模拟审读草案

生成时间（UTC）：2026-10-27T04:20:27.430382+00:00

**内部模拟编辑初审/方法学/领域审读；不是期刊编辑、外部审稿人、人类专家或 Claude 的评价。未启动跨模型复审。**

H4 尚未正式开始；本档案是并行阅读准备。正式验收仍按 H0–H8 顺序，不能据此宣称 H5 完成。

意见来自文本与已保存证据的一致性审读；未独立验证全部底层数值、推导、程序或公开远端状态。行号与 SHA 绑定当前快照，后续 H4/H5 改稿后需刷新定位。

阅读与写入范围：只读当前主文、补充、三篇已核实本刊文献及现有审计档案；只新建本草案的 Markdown/JSON。没有修改 canonical、投稿包或科学结果，没有研究重跑、外部联系、额外代理或 Git 提交。

每条的“高/较高”是内部风险排序，不是拒稿概率。以下按每角色约一页的内容密度组织；没有生成或宣称完成 PDF 分页。

## 编辑初审（内部模拟）

优先判断贡献是否足以送审、主张是否可信，以及数据与审查入口是否清楚。以下是可能触发退修或拒稿的具体风险，不是对期刊编辑决定的预测。

### E1｜高：“受基准保护”标题与失败的尾部标准冲突

**锚点：**[manuscript.tex:353](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:353>)（sec:v13-rp：小节标题）；[manuscript.tex:354](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:354>)（8/60 与最坏 80.98%）；[prediction-register.md:40](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.md:40>)（G3.R2.RP = NOT_SUPPORTED）；[v13-supplement.tex:41](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:41>)（中位数通过、尾部失败）。

**具体意见：**小节标题把 benchmark-protected 当作已实现的性质，而正文与登记表明确显示尾部标准失败：预定允许至多 3/60 个大于 10% 的损失，实际为 8/60。读者先见标题，容易把零中位数误读为保护有效；摘要只说仍有大损失，也没有给失败判定。

**写作修复：**将标题改为中性的“基准默认验证规则的回顾性检验”，并在摘要或首个结论句直接说尾部保护标准未满足；保留 32/60 回退历史规则、0.00% 中位数及 8/60 的完整关系。不要把 G3.R2 与 RQ2 混为一个检验。

**保留边界：**写作不能消除 8/60 和 +80.98% 的实际结果，不能把规则重新命名后称为满足原保护目标。

### E2｜高：WP2 留档时序须与“预先承诺/注册”用语同时呈现

**锚点：**[manuscript.tex:245](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:245>)（par:wp2-history）；[manuscript.tex:246](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:246>)（precommitted / registered）；[submission-wp2.tex:3](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:3>)（本地先行、公开后行、非外部注册）；[wp2-import-audit.md:9](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/wp2-import-audit.md:9>)（原设计提交时间）；[wp2-import-audit.md:10](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/wp2-import-audit.md:10>)（提前 13.372451 秒）；[wp2-import-audit.md:15](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/wp2-import-audit.md:15>)（公开上传发生在运行后）。

**具体意见：**主文使用 precommitted 和 registered，而关键时序限定埋在 S39。可核实的本地设计提交仅早于正式运行 13.372451 秒，公开上传在计算之后；且 W52/W260 已知。这些事实支持本地运行前封存，不能支持外部公开预注册或全新金融确认。

**写作修复：**正文首次出现 WP2 时写清“本地运行前封存、公开运行后上传；仅 W520 新算”；统一用 fixed/prewritten/local design 等准确措辞。保留原提交、UTC 时刻和来源分支审计入口，明确短历史结果此前已查看。

**保留边界：**已经发生的公开 after-run 和研究阶段检视不能通过语言变成外部预注册、独立预先确认或未见测试集。

### E3｜较高：贡献需要和本刊近期分布预测应用形成准确关系

**锚点：**[manuscript.tex:54](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:54>)（sec:literature）；[manuscript.tex:59](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:59>)（路径风险先例）；[manuscript.tex:62](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:62>)（分位模型与评价文献）；[manuscript.tex:76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)（三个经验发现）；[wiley-risk-policies.md:9](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/wiley-risk-policies.md:9>)（ASMBI 官方范围档案）。

**具体意见：**稿件使用成熟预测工具，两个命题也是已知性质；若只靠目标更换和大批对照表，编辑可能难以识别对应用随机建模读者的新经验知识。现有综述尚未联系已核实的三篇近期本刊论文，但这不是要求为凑本刊引用而全部加入。

**写作修复：**用一段说明“已观察路径峰值、严格匹配历史基准、验证失败边界、评分与成本分离”共同补充什么现有证据。Lee–Kim 可接时序稳定性，Pagnottoni 可接分布/分位差异，Muddana 等可接递归评价与基准；按真正相关点择用，并承认响应与模型不同。

**保留边界：**这轮证据不建立新模型族、普遍优越性或新覆盖理论；三篇来源只核对了官网元数据和摘要，不能据此声称全面方法比较或已读全文。

### E4｜高：“跨频率/独立系统”必须限定为相关的聚合任务

**锚点：**[manuscript.tex:32](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:32>)（数据系统概述）；[manuscript.tex:38](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:38>)（RQ2）；[manuscript.tex:126](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:126>)（CFTC survivor universe）；[manuscript.tex:276](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:276>)（independent reporting-system evidence）；[manuscript.tex:375](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:375>)（一个市场商）；[manuscript.tex:377](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:377>)（相关聚合任务）。

**具体意见：**一个市场商 FX、同一 FX 日度聚合、13 个纽约联储类别与 17 个 CFTC 合约并不是独立机构样本。跨频率还同时改变响应、物理跨度与时钟，CFTC 则是回顾性连续存续样本。宽泛“financial forecasting”或“independent evidence”易被看成超出观测对象。

**写作修复：**在 RQ2 首次说明独立的是报告系统；把一般结论限定于所选的采样净头寸、固定菜单和聚合任务。将频率变化描述为同源再聚合比较，避免由任务数暗示样本外机构复制。

**保留边界：**无新增独立 dealer 数据或真实首发时点样本，就不能消除单一机构、相关类别、幸存者选择及纯频率效应未识别的局限。

### E5｜高：数据权限和复现层级需能让编辑迅速核验

**锚点：**[manuscript.tex:398](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:398>)（FX 版权与排除范围）；[manuscript.tex:400](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:400>)（NY Fed 源条款）；[manuscript.tex:404](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:404>)（code availability）；[supplement.tex:1590](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1590>)（文档再生不等于预测复算）；[supplement.tex:1595](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1595>)（完整 replay 输入条件）；[supplement.tex:1608](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1608>)（尚无独立/前瞻验证）。

**具体意见：**公开代码和已保存结果并不等于任何审稿人可独立复算全部 FX 预测。FX 元数据仅指向原作者版权，原始数据与逐期私有预测未再分发；纽约联储数据另受源条款约束。若摘要/投稿信只写可复现，编辑会高估公开材料的闭包。

**写作修复：**保持现有权限说明，在复现入口用简短表或段落区分：保存结果/文档再生、持合法匹配输入的全量 replay、真正独立复现。明确需要匹配版本和 fingerprint，并给可访问的公开 CFTC 路径；权限核实仍交作者完成。

**保留边界：**不得把 Kaggle 可下载等同于再分发许可，也不能由代码许可替代数据条款；未取得授权输入者的完整 FX 独立复算仍有实际边界。

## 方法学审稿人（内部模拟）

重点审查比较对象、选择过程和不确定性解释。可建议重写和补充已保存证据的说明；本草案不要求重跑实验或改变任何冻结阈值。

### M1｜高：同一验证段选候选再设一标准误门槛，不产生保护概率

**锚点：**[manuscript.tex:354](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:354>)（候选选择与 HAC 门槛）；[v13-supplement.tex:39](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:39>)（selection and gate share validation data）；[v13-supplement.tex:58](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:58>)（评估期已查看）；[manuscript.tex:366](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:366>)（保护不足）。

**具体意见：**在六点菜单中先取验证均值最小者，再用同一段数据判断其胜过历史基准一个 HAC 标准误，门槛会受到候选选择和验证噪声影响。一标准误是规则参数，不是显著性水平；此处又使用已查看的评估期。零中位数与 FX 留益不能解释为事前非劣或风险保证。

**写作修复：**把它明确称为固定的启发式决策规则，说明候选选择与 gate 共用数据、决策在评估段固定；删去任何暗示名义保护概率的词。联合报告中位数、尾部失败与回退比例，避免只展示选中回归的子集。

**保留边界：**没有未查看的前瞻数据或独立校准设计，不能把这次回顾性规则检验升级为确认性保护；一标准误阈值也不能事后解释为某个检验大小。

### M2｜高：验证长度对比混入端点变化，组中位数不等于典型配对改善

**锚点：**[manuscript.tex:293](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:293>)（两系统中位数改善）；[manuscript.tex:304](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:304>)（端点与配对中位数限定）；[v13-supplement.tex:24](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:24>)（QR4 H6 median screen Fail）；[v13-supplement.tex:30](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:30>)（验证索引与 +0.00 配对中位数）；[prediction-register.md:37](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.md:37>)（G2.V3.QR4 不成立）。

**具体意见：**纽约联储 H6 延长验证还把终点前移 18 周并改变 refit phase，因此不能只归因于样本长度。全回归 H6 两臂中位数下降 7.81pp，配对变化中位数却为 0；QR4 H6 的 -4.22pp 未达预定 -5pp。泛称“longer validation improves regression”会遮蔽这些差别。

**写作修复：**每个总述都限定为 full-regression across-series arm medians，并就近指向端点变化和 QR4 失败；区分“中位数之差”和“配对变化的中位数”。沿用原阈值，不用改变成功定义来保住方向性叙述。

**保留边界：**当前已保存对照无法识别纯长度因果效应；未达 QR4 阈值的结果仍是不成立，不能用另一方法或另一 horizon 的成功替代。

### M3｜较高：事后有限菜单分解不证明特征缺乏信息的机制

**锚点：**[manuscript.tex:292](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:292>)（Why does regression lose 标题）；[manuscript.tex:293](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:293>)（27/41 与 29/41）；[manuscript.tex:295](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:295>)（有限五惩罚且排除 infinite）；[supplement.tex:1648](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1648>)（diagnostic 与 negative component）。

**具体意见：**分解的“最佳有限惩罚”用评估结果事后选取，并排除普通经验分位候选；它是测试菜单内的乐观诊断。余差仍为正，只说明这一特征/惩罚菜单未超过基准，不能区分真实信息不足、模型错设、估计误差或遗漏非线性结构。

**写作修复：**将“why”与“indicates limited incremental information”限定为菜单内诊断或与某解释一致；给出分解定义和负选择项的原因。保留 component medians 不可相加、finite 候选不含 infinite 的说明，不把该对象称为所有可行方法的下界。

**保留边界：**不增加新的识别设计或模型族，不能获得因果估计成本机制、单个特征作用或条件信息不存在的结论。

### M4｜高：99% 的数值失败不能被读成经济预测失败

**锚点：**[manuscript.tex:308](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:308>)（Both FX periods fail）；[manuscript.tex:315](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:315>)（CFTC W260 NA）；[manuscript.tex:316](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:316>)（两 FX NA）；[v13-supplement.tex:13](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:13>)（G1 仅 6/10 兼容检查通过）；[prediction-register.md:34](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.md:34>)（F3.Q2 UNDETERMINED）。

**具体意见：**正文“Both FX periods fail”缺少失败类型。这里是所需 99% 数值拟合/完整程序单元未完成，预测损失为空；G1 修复在 10 个既收敛拟合中仅 6 个满足保真标准，因而未采用。它既不是 QR 已被证明在 FX 经济上输掉，也不是修复后 60% 的经济成功率。

**写作修复：**明确写“required numerical fits/procedure cells failed, leaving comparative performance undetermined”，将原始求解失败与后续兼容 gate 失败分开。CFTC 保留 28/34 已知胜、1 个未知及 29 胜阈值未决；不要对成功子集求完整组结论。

**保留边界：**原 NA、三项失败单元和无法判定状态必须保留；不允许放松容差、替换求解器后冒充原预定结果，或将未跑修复后的比较当成失败评分。

### M5｜较高：重叠损失和研究阶段选择限制名义推断与任务计数

**锚点：**[manuscript.tex:185](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:185>)（完成标签与重叠验证）；[manuscript.tex:189](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:189>)（HAC 与 multiplicity families）；[manuscript.tex:204](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:204>)（90% MCS / 1000 bootstrap）；[manuscript.tex:206](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:206>)（重复损失和相关任务）；[supplement.tex:1641](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1641>)（名义解释边界）。

**具体意见：**horizon 重叠、同源类别相关和已有研究阶段模型发展，使 DM/HAC、MCS 和跨任务胜率回答不同问题。MCS 未剔除不能读成预测风险相等；29/34、8/60 也不是独立伯努利样本。当前部分解释已经到位，但结果总述仍可能被胜率和“confidence”术语带走。

**写作修复：**在核心表/图注重申检验的逐格比较单位、原有 Holm family 和未涵盖的研究阶段选择；把 MCS 表述为固定近似下的存活集合。保持完整分母、重复列等价处理与所有 unavailable 方法，避免追加未经设计的 pooled p 值。

**保留边界：**现有固定块长、1000 次 bootstrap 和样本无法建立同时最优、未来覆盖或独立市场总体概率；不能通过重新包装名义 90% 扩张适用范围。

## 金融风险与预测领域审稿人（内部模拟）

重点审查预测响应与真实风控决策之间的距离，以及基准和跨市场解释是否具有可执行含义。现有负面结果有价值，但需要把操作性建议限制在其观测范围内。

### D1｜高：采样绝对净头寸峰值不是损失、总风险或真实资金需求

**锚点：**[manuscript.tex:82](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:82>)（Y/B/Z 响应定义）；[manuscript.tex:96](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:96>)（known-floor 命题）；[manuscript.tex:103](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:103>)（Lévy 独立对称假设）；[manuscript.tex:147](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:147>)（无经验覆盖保证）；[supplement.tex:1629](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1629>)（gross exposure / cash needs / sampled peak）。

**具体意见：**当前对象是采样时点的绝对净头寸峰值。净额抵消、遗漏区间内极值、估值与报告构成变化，使它不能直接代表 gross exposure、PnL 尾损失或结算流动性。两个命题分别是已知 floor 投影和强假设下的经典概率界，不自动为实证报告赋予监管式覆盖保证。

**写作修复：**首次解释“position limits”时明确 sampled passive-report benchmark；在金融解释中区分头寸、损益与现金需求。保持 Lévy 条件和经验 plug-in 分离，指出理论分位覆盖陈述针对真实条件分位，不是拟合预测的既得性质。

**保留边界：**缺少更细交易、总敞口、估值和资金流数据，不能把本稿评分或 breach 直接换算成资本节省、资金需求或损失风险。

### D2｜高：周报经济日期不构成当时可交易的信息集

**锚点：**[manuscript.tex:124](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:124>)（日末记录聚合）；[manuscript.tex:128](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:128>)（Tuesday positions / Friday release）；[supplement.tex:1534](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1534>)（实际发布时间与延迟）；[supplement.tex:1631](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1631>)（频率同时改变多个设计要素）；[manuscript.tex:378](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:378>)（first-release 与区间极值缺失）。

**具体意见：**按当时公开信息进行实时预测的理解会与经济日期回放发生冲突：CFTC 通常周二测量周五公布，纽约联储历史首发与修订版本未重建，日 FX“最后记录”也非已验证收盘。相同完成标签条件保证回放一致，却不能补齐当时公开信息集。

**写作修复：**将所有操作性建议表述为对 downloaded economic-date vintages 的回顾性结果；避免“实时可部署”或纯频率效果。说明同源日度聚合还改变物理跨度、时钟、训练/评估范围与响应采样。

**保留边界：**没有带真实发布时间与修订轨迹的数据，无法验证 public-information-clock 策略；仅重排文字或加发布日期滞后也不能证明历史首发可用性。

### D3｜高：评分改善与风控改善之间仍缺实测经济价格

**锚点：**[manuscript.tex:216](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:216>)（短历史 FX 的 loss 与 breaches）；[manuscript.tex:258](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:258>)（日度 3.0% 降损但 37/30 breaches）；[manuscript.tex:328](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:328>)（score 与 breach 区分）；[manuscript.tex:334](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:334>)（归一化成本定义）；[manuscript.tex:342](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:342>)（CFTC 5/34、32/34、1/34）；[supplement.tex:1641](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1641>)（评价样本归一化）。

**具体意见：**较低 pinball 分数可以伴随更多 breach；成本角点又由固定偏好决定。以评估样本历史 headroom 作归一化提供可比较图示，但不是事前机构收费。因而“cheaper”只在给定偏好网格中成立，不能直接转成风险降低、盈利或资金效率提升。

**写作修复：**把 score、breach 次数、reserve/headroom、exceedance amount 并列解释，并保留 5/34 与两个相反角点，避免只引用有利角落。明确参数是规定偏好、归一化是描述性的，未估计实际损失/融资成本，也未识别限额改变交易行为后的效果。

**保留边界：**缺少机构价格、干预决策和反事实交易响应，无法证明真实成本节省或最优政策；无需为追求积极结论重新选择偏好网格。

### D4｜较高：“历史规则胜出”计数与可执行历史默认要分开

**锚点：**[manuscript.tex:140](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:140>)（corrected-rank 历史 headroom）；[manuscript.tex:157](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:157>)（infinite = ordinary empirical）；[manuscript.tex:278](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:278>)（29/34 用两历史规则较佳 realised score）；[manuscript.tex:366](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:366>)（ordinary 最大恶化 36.5%）。

**具体意见：**29/34 的阈值对照使用 corrected 与 ordinary 两种历史报告中事后较好者，不是实时可执行 selector；而主要曲线与推荐默认固定为 corrected F。infinite shrinkage 又只是 ordinary empirical，不能称为已经回到完全相同的历史基准。这些细节直接影响金融读者能否照做。

**写作修复：**在摘要所用 29/34 计数旁或主表注明确“better realized historical score”判定与固定 F 评分的差别；统一历史默认名称。把匹配 F、短滚动 FX reference、ordinary I 和 infinite 候选四者关系写清，保留各自菜单、历史和 refit clock。

**保留边界：**不能把事后历史赢家冒充可执行选择器，也不能由历史胜率推断所有简单规则可靠；比较只覆盖这些已执行参考程序。

### D5｜较高：历史长度扩展只支持部分运输，不能给一般“足够历史”门槛

**锚点：**[manuscript.tex:238](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:238>)（FX history learning curve）；[manuscript.tex:246](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:246>)（WP2 partial support）；[submission-wp2.tex:15](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:15>)（低历史 QR4 15/17）；[submission-wp2.tex:19](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:19>)（高历史 QR4 10/17 未达 60%）；[submission-wp2.tex:21](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:21>)（Full P2 not testable）；[submission-wp2.tex:23](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:23>)（P3 6/17 未达 70%）；[prediction-register.md:45](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.md:45>)（Full P2 planned=0）。

**具体意见：**WP2 低历史结果支持既定不利屏，但主要来自此前已知 W52/W260；唯一新 W520 在 QR4 上仅 10/17 获胜，严格递减仅 6/17，QR33 高区间计划格数为 0 而不可检验。不能由部分支持推论更多金融历史最终必胜，或证实样本/维度阈值的估计成本机制。

**写作修复：**主文在 partial support 后补一句 full-regression 高区间结构性不可检验，并保持 fixed denominator；区分低区间既有验证和长区间新增预测。将“sufficient history”改为与测试范围相称的经验条件，保留 S39 全部反例，不对成功市场再筛选。

**保留边界：**计划 0 的 QR33 P2 无法判定、QR4 的失败与非单调性仍在；现有 dependent aggregate markets 不能确定一般机构或市场的充分历史长度与因果机制。

## 三篇近期 ASMBI 文献的使用边界

以下仅是已保存的出版社官网元数据与摘要证据，不声称已阅读不可访问的全文。本草案没有插入任何文献。可优先择用与定位最直接相关的两篇，第三篇只在其具体语境确实需要时使用。

- **LeeKim2024ASMBI**：[Sequential monitoring for conditional quantiles of general conditional heteroscedastic time series models](https://onlinelibrary.wiley.com/doi/abs/10.1002/asmb.2865)，2024，DOI `10.1002/asmb.2865`。本地来源：`notes/submission/asmbi-recent-literature.json#/records/0`；官网访问日期 UTC `2026-10-27`。摘要支持：在线顺序监测位置–尺度异方差时序的条件分位数变点，摘要明确联系 VaR/ES 风险管理；用 KOSPI 与 EuroStoxx 50 日收益实证。 边界：这是变点监测研究；摘要不能支持本稿模型优于其方法，或本稿静态评价量具有新颖性的结论。
- **Pagnottoni2026ASMBI**：[Optimal Transport Autoregression to Forecast High-Frequency Financial Data Distributions](https://onlinelibrary.wiley.com/doi/10.1002/asmb.70067)，2026，DOI `10.1002/asmb.70067`。本地来源：`notes/submission/asmbi-recent-literature.json#/records/1`；官网访问日期 UTC `2026-10-27`。摘要支持：用最优传输自回归预测 Bitcoin 高频收益与波动分布；摘要报告误差依赖时间与分位数，极端分位附近误差上升且不单调。 边界：摘要针对其最优传输模型和 Bitcoin 数据；不能外推为所有金融模型的普遍定理，也不能据此声称本稿已解决极端分位问题。
- **MuddanaEtAl2025ASMBI**：[Forecasting Gold Returns Volatility Over 1258–2023: The Role of Moments](https://onlinelibrary.wiley.com/doi/10.1002/asmb.70042)，2025，DOI `10.1002/asmb.70042`。本地来源：`notes/submission/asmbi-recent-literature.json#/records/2`；官网访问日期 UTC `2026-10-27`。摘要支持：先用 Bayesian 时变参数分位回归构建波动、尾风险和矩指标，再作递归样本外线性预测并比较自回归基准。 边界：研究目标是波动预测，不能将其等同于本稿的分位损失目标或宣称摘要证明某种分位评价标准有效。

## 当前快照与后续处理

正式修改时先处理 E1、E2、M4 的准确性，再核对其余处主张是否一致。此排序不会改变 H0–H8 的验收顺序；所有科学判定、数值、原阈值和失败单元保持不变。

| 只读来源 | SHA-256 |
|---|---|
| `submission-final/manuscript.tex` | `34b05fe4df73f31ecdce76b6a58a960c7e5afd21b18340003234d3dff2fb4744` |
| `submission-final/supplement.tex` | `8084fe5365b1f904841174285d5985deba6b5aa69183b109817259771633b0b2` |
| `submission-final/generated/v13-supplement.tex` | `f2518eeb459e44c4a331731e19b99186b47b3872ec2af73e91902d3a56742621` |
| `submission-final/generated/submission-wp2.tex` | `a2f4f1372c541e78383780c94ed0f60f5ed86b501f1c947bfdf8902d61265fb2` |
| `notes/submission/asmbi-recent-literature.json` | `dec23716ffe3b1c1fbd7d4b2e12114acfa6f9eff49a0cab7714b4a3fd9851d9d` |
| `notes/submission/prediction-register.md` | `7041a7f545a30a360c19dd0f2e453340ecf7cf5d0acbf147e4ab63fe939b5b3c` |
| `notes/submission/wp2-import-audit.md` | `7cedaadeb048cb0891cac87d3df91d6441f72bcd21ba7aa2ea59782d8a193e75` |
| `notes/submission/wiley-risk-policies.md` | `33e76e6faf6b37bfdf45d2afcf997658fcf57c19304c59b7e865d7273b185dad` |

JSON 保留全部 15 条意见、机器可读锚点和三篇文献记录。后续若 canonical 改动，须按新 SHA 重定位，不能把本草案视为改稿后的验证回执。
