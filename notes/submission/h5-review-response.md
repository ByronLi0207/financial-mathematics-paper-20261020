# H5 内部模拟审读逐条回应

UTC：2026-10-27T05:00:10.078723+00:00；当前主文 SHA-256：`6f9f196f4bc9637674e253b5194bc0717a0c8b4436ca61047a96dc8736519cc8`。

**这是内部模拟审读的写作回应，不是外部编辑/审稿人或Claude评价。** 三角色各5条、共15条全部回应。H4已解决项明确标H4；其余按H5写作收紧或保留现有实质限制记录。

写作主张已纠正或现有边界已明确保留；不表示数据、首发时点、前瞻、独立复制、风险映射、真实成本或因果识别限制被消除。

## 编辑初审（内部模拟）

### E1｜“受基准保护”标题与失败的尾部标准冲突

**处理阶段：**H4；状态 `H4_WRITING_CORRECTION_WITH_TAIL_FAILURE_RETAINED`。

**原意见：**小节标题把 benchmark-protected 当作已实现的性质，而正文与登记表明确显示尾部标准失败：预定允许至多 3/60 个大于 10% 的损失，实际为 8/60。读者先见标题，容易把零中位数误读为保护有效；摘要只说仍有大损失，也没有给失败判定。

**当前处理：**H4 已将小节标题改为 benchmark-default，避免把保护当作已达成性质。当前摘要仍说 gate 留下大损失，结果和结论继续明确原尾部标准失败。

**当前锚点：**[manuscript.tex:355](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:355>)；[manuscript.tex:356](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:356>)；[manuscript.tex:394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**主张映射：**`C46`, `C47`。

**仍保留的实质限制：**8/60 大于10%的损失、最坏+80.98%与 G3.R2 NOT_SUPPORTED 均保留；零中位数和FX留益不能覆盖失败判定。

**编辑来源：**此项为H4已解决或既有披露保留；不虚列为新的H5文本替换。

### E2｜WP2 留档时序须与“预先承诺/注册”用语同时呈现

**处理阶段：**H4+H5；状态 `H4_TIMING_CORRECTION_PLUS_H5_ROUND_SPECIFIC_DISCLOSURE`。

**原意见：**主文使用 precommitted 和 registered，而关键时序限定埋在 S39。可核实的本地设计提交仅早于正式运行 13.372451 秒，公开上传在计算之后；且 W52/W260 已知。这些事实支持本地运行前封存，不能支持外部公开预注册或全新金融确认。

**当前处理：**H4 已在WP2开头明示本地运行前提交、公开运行后上传，并改用 prewritten；H5 把原文 each new analysis 的总括改为逐轮保留现有 local/public 时序和原设计对象可用性。

**当前锚点：**[manuscript.tex:248](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)；[manuscript.tex:202](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:202>)；[submission-wp2.tex:3](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:3>)。

**主张映射：**`C19`, `C26`, `C27`。

**仍保留的实质限制：**WP2 本地提前13.372451秒、公开after-run、W52/W260已查看及仅W520新算均不改变；不是外部公开预注册或未见金融确认，E5原对象缺失仍按回执精度。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/15`, `notes/submission/h5-edit-log.json#/changes/29`。

### E3｜贡献需要和本刊近期分布预测应用形成准确关系

**处理阶段：**H5；状态 `H5_CONTEXT_ADDED_WITH_ABSTRACT_ONLY_SOURCE_BOUNDARY`。

**原意见：**稿件使用成熟预测工具，两个命题也是已知性质；若只靠目标更换和大批对照表，编辑可能难以识别对应用随机建模读者的新经验知识。现有综述尚未联系已核实的三篇近期本刊论文，但这不是要求为凑本刊引用而全部加入。

**当前处理：**补入 Lee–Kim 条件分位变点监测、Pagnottoni 高频分布预测、Muddana等递归波动预测的有界语境，说明本稿的采样头寸峰值和匹配历史对照。新三组文献主张分别连接本地已核实官方记录。

**当前锚点：**[manuscript.tex:65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)；[manuscript.tex:65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)；[manuscript.tex:50](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:50>)。

**主张映射：**`C50`, `C51`, `C52`, `C53`, `C59`, `C60`, `C61`。

**仍保留的实质限制：**论文仍使用成熟工具和既知性质，不据这三篇摘要主张新模型族、覆盖理论、全面方法优越性或已读全文；是否足以满足期刊新颖性属于编辑判断。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/25`, `notes/submission/h5-edit-log.json#/changes/26`。

### E4｜“跨频率/独立系统”必须限定为相关的聚合任务

**处理阶段：**H5+EXISTING_SCOPE；状态 `H5_GENERALIZATION_NARROWED_WITH_EXTERNAL_VALIDITY_LIMIT_RETAINED`。

**原意见：**一个市场商 FX、同一 FX 日度聚合、13 个纽约联储类别与 17 个 CFTC 合约并不是独立机构样本。跨频率还同时改变响应、物理跨度与时钟，CFTC 则是回顾性连续存续样本。宽泛“financial forecasting”或“independent evidence”易被看成超出观测对象。

**当前处理：**将历史/菜单解释限定于 tested configurations；正文补出 full regression 高区间不可检验；新增净头寸不识别gross portfolio、hedging和economic capital。原相关聚合任务、survivor universe、单一市场商和频率混杂说明保留。

**当前锚点：**[manuscript.tex:240](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:240>)；[manuscript.tex:248](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)；[manuscript.tex:379](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:379>)。

**主张映射：**`C09`, `C10`, `C25`, `C27`, `C49`。

**仍保留的实质限制：**没有新增独立dealer或真实首发时点数据；同FX日度聚合不构成外部复制，17合约与13类别也不是独立机构样本。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/16`, `notes/submission/h5-edit-log.json#/changes/17`, `notes/submission/h5-edit-log.json#/changes/21`, `notes/submission/h5-edit-log.json#/changes/23`。

### E5｜数据权限和复现层级需能让编辑迅速核验

**处理阶段：**EXISTING_H3_DISCLOSURE_RETAINED；状态 `EXISTING_RIGHTS_AND_REPLAY_LIMITS_RETAINED_NO_NEW_PERMISSION_CLAIM`。

**原意见：**公开代码和已保存结果并不等于任何审稿人可独立复算全部 FX 预测。FX 元数据仅指向原作者版权，原始数据与逐期私有预测未再分发；纽约联储数据另受源条款约束。若摘要/投稿信只写可复现，编辑会高估公开材料的闭包。

**当前处理：**沿用H3的分层披露：公开代码/协议/汇总可检查；FX原观察和private vectors不分发，原panel输入不分发，完整replay需匹配原输入和历史Git对象。DOI、软件许可及作者权限确认保持待填。

**当前锚点：**[manuscript.tex:401](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:401>)；[manuscript.tex:403](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:403>)；[manuscript.tex:407](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:407>)。

**主张映射：**`C54`, `C55`, `C56`, `C57`。

**仍保留的实质限制：**本轮没有取得数据再分发许可、公开历史私有输入或完成外部独立预测复算；文档再生与独立金融复算不可混称。

**编辑来源：**此项为H4已解决或既有披露保留；不虚列为新的H5文本替换。

## 方法学审稿人（内部模拟）

### M1｜同一验证段选候选再设一标准误门槛，不产生保护概率

**处理阶段：**H4+EXISTING_METHOD_DISCLOSURE；状态 `HEURISTIC_RULE_DISCLOSED_PROTECTION_NOT_ESTABLISHED`。

**原意见：**在六点菜单中先取验证均值最小者，再用同一段数据判断其胜过历史基准一个 HAC 标准误，门槛会受到候选选择和验证噪声影响。一标准误是规则参数，不是显著性水平；此处又使用已查看的评估期。零中位数与 FX 留益不能解释为事前非劣或风险保证。

**当前处理：**保留同一validation段先选候选再gate、1个paired HAC标准误和评估段固定决策的原规则。H4中性标题及结果/实务说明共同避免把启发式门槛写成名义保护概率。

**当前锚点：**[manuscript.tex:356](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:356>)；[v13-supplement.tex:39](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:39>)；[v13-supplement.tex:39](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:39>)。

**主张映射：**`C45`, `C46`, `C47`。

**仍保留的实质限制：**选择噪声、共享validation和已查看评估期仍在；没有新增独立校准或前瞻测试，一标准误没有被重新解释为显著性水平。

**编辑来源：**此项为H4已解决或既有披露保留；不虚列为新的H5文本替换。

### M2｜验证长度对比混入端点变化，组中位数不等于典型配对改善

**处理阶段：**H5；状态 `H5_STATISTICAL_OBJECT_CLARIFIED_WITH_LENGTH_CONFOUNDING_RETAINED`。

**原意见：**纽约联储 H6 延长验证还把终点前移 18 周并改变 refit phase，因此不能只归因于样本长度。全回归 H6 两臂中位数下降 7.81pp，配对变化中位数却为 0；QR4 H6 的 -4.22pp 未达预定 -5pp。泛称“longer validation improves regression”会遮蔽这些差别。

**当前处理：**摘要、finding、综述和结论统一 full regression；正文明确QR4 H6 median-improvement screen失败。既有arm-median与paired-change区别、H6端点提前18周和refit phase变化均保留。

**当前锚点：**[manuscript.tex:18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[manuscript.tex:306](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:306>)；[manuscript.tex:306](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:306>)。

**主张映射：**`C37`, `C38`, `C39`。

**仍保留的实质限制：**未识别纯validation长度因果效果，paired median0不因arm median降低而变成典型系列改善；QR4失败及CFTC不可用结果未改判。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/2`, `notes/submission/h5-edit-log.json#/changes/4`, `notes/submission/h5-edit-log.json#/changes/5`, `notes/submission/h5-edit-log.json#/changes/8`, `notes/submission/h5-edit-log.json#/changes/20`, `notes/submission/h5-edit-log.json#/changes/22`。

### M3｜事后有限菜单分解不证明特征缺乏信息的机制

**处理阶段：**H5；状态 `H5_FINITE_MENU_INTERPRETATION_NARROWED_WITH_CAUSAL_LIMIT_RETAINED`。

**原意见：**分解的“最佳有限惩罚”用评估结果事后选取，并排除普通经验分位候选；它是测试菜单内的乐观诊断。余差仍为正，只说明这一特征/惩罚菜单未超过基准，不能区分真实信息不足、模型错设、估计误差或遗漏非线性结构。

**当前处理：**将“Why does regression lose”改成有限菜单分解/验证长度；移除由余差推断conditional information不足的句子，明确不证明信息不存在。simulation解释也限定tested histories/windows/menus。

**当前锚点：**[manuscript.tex:294](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:294>)；[manuscript.tex:295](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:295>)；[manuscript.tex:297](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:297>)。

**主张映射：**`C25`, `C35`, `C36`。

**仍保留的实质限制：**事后最佳有限候选仍非deployable selector、全模型下界或因果估计成本机制；排除infinite和component medians不可相加的原定义保留。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/18`, `notes/submission/h5-edit-log.json#/changes/19`, `notes/submission/h5-edit-log.json#/changes/21`。

### M4｜99% 的数值失败不能被读成经济预测失败

**处理阶段：**H4；状态 `H4_NUMERICAL_FAILURE_TYPE_CORRECTED_UNDETERMINED_RETAINED`。

**原意见：**正文“Both FX periods fail”缺少失败类型。这里是所需 99% 数值拟合/完整程序单元未完成，预测损失为空；G1 修复在 10 个既收敛拟合中仅 6 个满足保真标准，因而未采用。它既不是 QR 已被证明在 FX 经济上输掉，也不是修复后 60% 的经济成功率。

**当前处理：**H4 已在主文和补充明确required numerical fits失败，G1仅6/10保真兼容通过导致修复拒绝，三原失败单元保持未重跑/不可用。

**当前锚点：**[manuscript.tex:310](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:310>)；[v13-supplement.tex:13](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:13>)；[manuscript.tex:384](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:384>)。

**主张映射：**`C40`, `C41`。

**仍保留的实质限制：**两FX经济比较和原F3 Q1/Q2仍undetermined；6/10不是经济成功率，也没有把NA当成观察到的经济失败或放松容差补值。

**编辑来源：**此项为H4已解决或既有披露保留；不虚列为新的H5文本替换。

### M5｜重叠损失和研究阶段选择限制名义推断与任务计数

**处理阶段：**EXISTING_INFERENCE_LIMITS+H5_TRANSPARENCY；状态 `WORKING_REFERENCE_INFERENCE_SCOPE_RETAINED_NO_NEW_CONFIRMATION`。

**原意见：**horizon 重叠、同源类别相关和已有研究阶段模型发展，使 DM/HAC、MCS 和跨任务胜率回答不同问题。MCS 未剔除不能读成预测风险相等；29/34、8/60 也不是独立伯努利样本。当前部分解释已经到位，但结果总述仍可能被胜率和“confidence”术语带走。

**当前处理：**保留逐格HAC/HLN/Holm family、MCS固定bootstrap及duplicate loss处理；明确nominal level不调整研究阶段发展，non-elimination不等于同风险，相关任务不作独立pooled test。H5补充逐轮时序/对象可用性。

**当前锚点：**[manuscript.tex:206](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:206>)；[manuscript.tex:208](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:208>)；[manuscript.tex:290](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:290>)。

**主张映射：**`C18`, `C19`, `C20`, `C21`。

**仍保留的实质限制：**重叠损失、有限样本、固定bootstrap规则和研究阶段选择仍限制推断；没有新增selection-adjusted、同时最优或未来coverage结论。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/15`。

## 金融风险与预测领域审稿人（内部模拟）

### D1｜采样绝对净头寸峰值不是损失、总风险或真实资金需求

**处理阶段：**H5；状态 `H5_ECONOMIC_OBJECT_LIMIT_ADDED_WITH_RISK_MAPPING_UNIDENTIFIED`。

**原意见：**当前对象是采样时点的绝对净头寸峰值。净额抵消、遗漏区间内极值、估值与报告构成变化，使它不能直接代表 gross exposure、PnL 尾损失或结算流动性。两个命题分别是已知 floor 投影和强假设下的经典概率界，不自动为实证报告赋予监管式覆盖保证。

**当前处理：**新增净头寸峰值只概括所观测exposure、不能识别gross portfolios、hedging和economic capital的限制，配合既有采样峰值、Lévy强假设及真实分位/拟合报告区分。

**当前锚点：**[manuscript.tex:379](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:379>)；[manuscript.tex:84](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:84>)；[manuscript.tex:149](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:149>)。

**主张映射：**`C01`, `C03`, `C04`, `C10`, `C49`。

**仍保留的实质限制：**没有更细交易、gross敞口、资金流或资本模型；不能把评分或breach换算为资本节省、真实尾损失或资金需求，理论界不赋予实证覆盖。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/23`。

### D2｜周报经济日期不构成当时可交易的信息集

**处理阶段：**EXISTING_DATA_CLOCK_LIMIT_RETAINED；状态 `PUBLIC_INFORMATION_CLOCK_AND_PURE_FREQUENCY_EFFECT_UNVERIFIED`。

**原意见：**按当时公开信息进行实时预测的理解会与经济日期回放发生冲突：CFTC 通常周二测量周五公布，纽约联储历史首发与修订版本未重建，日 FX“最后记录”也非已验证收盘。相同完成标签条件保证回放一致，却不能补齐当时公开信息集。

**当前处理：**保留economic-date replay与public information clock差别、首发/修订缺失、日末最后记录及同时改变多设计要素的说明；没有写成实时部署验证或纯频率实验。

**当前锚点：**[manuscript.tex:130](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:130>)；[manuscript.tex:380](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:380>)；[supplement.tex:1631](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1631>)。

**主张映射：**`C09`, `C11`, `C49`。

**仍保留的实质限制：**没有首发发布时间/修订轨迹和已验证close，不能认证历史实时可执行性或纯频率效果。

**编辑来源：**此项为H4已解决或既有披露保留；不虚列为新的H5文本替换。

### D3｜评分改善与风控改善之间仍缺实测经济价格

**处理阶段：**EXISTING_COST_LIMIT_RETAINED；状态 `SCORE_BREACH_AND_STIPULATED_COST_SEPARATED_NO_MEASURED_PROFIT`。

**原意见：**较低 pinball 分数可以伴随更多 breach；成本角点又由固定偏好决定。以评估样本历史 headroom 作归一化提供可比较图示，但不是事前机构收费。因而“cheaper”只在给定偏好网格中成立，不能直接转成风险降低、盈利或资金效率提升。

**当前处理：**保留score与strict breaches的相反案例，固定网格center及两相反角点，reserve/breach/exceedance联合报告和评价样本归一化说明。

**当前锚点：**[manuscript.tex:330](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:330>)；[manuscript.tex:345](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:345>)；[manuscript.tex:382](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:382>)。

**主张映射：**`C24`, `C32`, `C42`, `C43`, `C44`。

**仍保留的实质限制：**价格是规定偏好，缺少机构成本与干预后的反事实交易响应；没有新增实际profit、funding或最优政策证据。

**编辑来源：**此项为H4已解决或既有披露保留；不虚列为新的H5文本替换。

### D4｜“历史规则胜出”计数与可执行历史默认要分开

**处理阶段：**H5；状态 `H5_ABSTRACT_BASELINE_SELECTION_CLARIFIED_EXECUTABLE_DEFAULT_DISTINCT`。

**原意见：**29/34 的阈值对照使用 corrected 与 ordinary 两种历史报告中事后较好者，不是实时可执行 selector；而主要曲线与推荐默认固定为 corrected F。infinite shrinkage 又只是 ordinary empirical，不能称为已经回到完全相同的历史基准。这些细节直接影响金融读者能否照做。

**当前处理：**摘要29/34明确为better realized historical score；结果继续说明两种历史报告事后较好者不是可执行selector。corrected F、ordinary I/infinite和短rolling reference的定义保持区分。

**当前锚点：**[manuscript.tex:18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[manuscript.tex:280](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:280>)；[manuscript.tex:159](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:159>)。

**主张映射：**`C13`, `C14`, `C22`, `C33`, `C48`。

**仍保留的实质限制：**没有将事后历史赢家转成部署算法，历史胜率只覆盖已执行程序，也不证明所有简单规则可靠。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/1`。

### D5｜历史长度扩展只支持部分运输，不能给一般“足够历史”门槛

**处理阶段：**H5；状态 `H5_TRANSPORT_SCOPE_CLARIFIED_PARTIAL_AND_UNTESTABLE_RETAINED`。

**原意见：**WP2 低历史结果支持既定不利屏，但主要来自此前已知 W52/W260；唯一新 W520 在 QR4 上仅 10/17 获胜，严格递减仅 6/17，QR33 高区间计划格数为 0 而不可检验。不能由部分支持推论更多金融历史最终必胜，或证实样本/维度阈值的估计成本机制。

**当前处理：**历史曲线/菜单关联限定tested configurations，移除一般sufficient-history推断；主文补出full高区间不可测，S39全反例、固定分母和partial verdict保留。

**当前锚点：**[manuscript.tex:240](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:240>)；[manuscript.tex:248](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)；[manuscript.tex:248](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)。

**主张映射：**`C25`, `C26`, `C27`。

**仍保留的实质限制：**QR4 P2 10/17未达60%、P3 6/17未达70%、QR33 planned0不可检验均未改；不能确定一般金融充分历史长度或因果机制。

**精确编辑记录：**`notes/submission/h5-edit-log.json#/changes/16`, `notes/submission/h5-edit-log.json#/changes/17`, `notes/submission/h5-edit-log.json#/changes/21`。

## 完整性与边界

- 15/15原意见均有当前锚点、处理阶段、动作和仍保留边界；原H5草案保持历史快照。
- H4三项：E1标题、E2本地/公开时序、M4数值失败类型；H5六P2：C19/C25/C27/C33/C35/C38。
- 没有新增金融计算、数据、前瞻/外部复制、权限许可、真实成本或因果证据；没有改原阈值和失败/无法判定状态。
- 三篇文献仅依已保存出版社元数据/摘要支持，未声称阅读全文。
