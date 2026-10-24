# v8内部模拟审稿与回应

三份意见由同一模型的独立角色生成；每份五条、少于300英文词，相当于一页以内的审稿文本。它们是内部压力测试，不代表外部审稿、期刊意见或录用预测。

# Simulated forecasting-methodology referee

Internal same-model simulated review.

1. **Benchmark fairness (Table 3; Evaluation design).** The 14.8% matched gain and 12.7% rolling-reference gain use different controls. Is every headline tied to the correct history and update schedule, including the separately wrapped comparison? Request explicit control labels wherever gains are summarized. **New data/experiment: no; clarify existing comparisons.**

2. **Inference and multiplicity (Table 5).** Treasury's DM p=0.00761 accompanies Holm p=0.32 over 72 contrasts; another family adjusts two main comparisons. Which family supports each claim? Request consistent working-reference language, with dependence and post-selection scope explicit. Multiplicity adjustment alone does not validate pinball HAC inference. **New data/experiment: no.**

3. **Data snooping and replication (Limitations; Table 3).** The earlier 2015 gain uses rules designed after original FX results were viewed. Does “recurring” mean within-record stability or independent confirmation? Request the former interpretation throughout. Stronger confirmation needs an additional dealer or prospective observations; the current chronology can be stated directly. **New data: required only for stronger confirmation.**

4. **Short validation (Table 4; Supplement “Earlier-period fixed selection rules”).** Weekly selection uses 52 validation origins, overlapping labels, 34 regression coefficients and a six-candidate menu. Why should one-standard-error selection be stable here? Its 181.4% worst-cell excess warrants a procedure-specific interpretation. Request clear validation size, paired-band definition and retention of all failures. **New experiment: unnecessary for that clarification; longer-validation evidence remains future work.**

5. **Mechanism identification (calibrated-simulation subsection; Supplement “Interpretation and limits”).** Seven hourly cells fail numerically, and frequency is bundled with validation length and volatility laws. Which proposed mechanism is actually identified? Request conclusions limited to completed stationary weekly comparisons; numerical failure is not poor forecast accuracy. **New experiment: required to separate bundled effects or resolve unavailable hourly performance, outside this revision.**


---

# Finance and market-microstructure referee

Internal same-model review; no external referee.

1. **Forecast report versus inventory policy — Introduction; Implications; Table 6.** Who sets the limit, and what action follows a breach? The backtest scores passive reports on an observed position path; intervention could change that path. State this distinction. **Clarification now; policy benefits require future intervention/cost data or a separate experiment.**

2. **Representativeness — Data; Limitations.** Why should one market-maker client-flow record and related public category aggregates support a dealer-level recommendation? Preserve their different economic units and avoid reading panel breadth as independent dealer replication. Bound conclusions to the observed records. **Clarification now; generalization requires future independent dealers and prospective observations.**

3. **Weekly measurement — Data; FR 2004 references; source metadata.** The metadata describes an aggregate market-value replay, while the main says position totals. Explain how valuation, netting and reporting composition can move measured peaks without identifying trading or inventory adjustment. Distinguish this target from gross dealer exposure. **Existing definitions support clarification; separating these channels needs future valuation/gross-position data.**

4. **Economic horizon and clock — Forecasting methods; Table 2; Limitations.** What review decision corresponds to a horizon measured in source records? FX calendar gaps and weekly sampling produce different elapsed exposure periods; sampled peaks miss intervening excursions. State the clock interpretation beside the horizon definition. **Clarification now; operational peak validation requires future finer-frequency exposure data.**

5. **Scores, breaches and decision value — Tables 3 and 5; Implications.** How should a manager trade off forecast loss, breach frequency, breach severity and unused allowance? The pinball asymmetry is not an estimated funding or intervention cost. Keep the recommendation a joint-validation checklist rather than an optimal-limit claim. **Clarification now; monetary utility requires future decision-cost data and separately designed evaluation.**


---

# Simulated JoF editorial screening

Internal, same-model exercise; no journal contact or acceptance forecast.

1. **Contribution and title scope — writing.** The title, Abstract and Introduction promise a broad benchmark lesson from bounded records. The three empirical findings fit comparative forecasting evaluation, but standard tools alone supply no methodological novelty. State the exact retrospective peak-forecast setting beside the headline finding and explain its forecasting lesson in the cover letter.

2. **Breadth — new data if claims expand.** Section 4 and Table 4 combine one FX record with related weekly dealer aggregates. Thirteen categories do not represent thirteen independent dealer replications, and frequency is entangled with measurement. Keep that distinction explicit. Independent dealers or prospective issuance would require new data; retain those as author tasks.

3. **What simulation adds — new experiment to resolve, writing now.** Section 7.4/Figure 4 has seventeen complete cells, seven failed hourly cells, unsupported P1/P3 and unassessable P2/P4. It does not explain the empirical pattern. Present it as a failed or incomplete mechanism test, keep all failures visible, and avoid implying the subsection establishes why historical rules win.

4. **Editorial economy — writing.** The fifteen-page main text is manageable, but the Introduction and Section 2 repeat the numbered findings; the 132-word Abstract packs nine numbers. Reduce duplicated signposting and leave detailed inventories in the twenty-five-page Supplement, with precise table references and readable figure ticks.

5. **Availability and submission readiness — package/author action.** The Data and code availability section, README and AUTHOR-TODO need mutually consistent v8 reproduction routes and actual data-access restrictions. README still describes v7 pages and builders. Refresh it; distinguish document reproduction from restricted-input financial replay. Preserve every author, ORCID, funding, conflict and AI placeholder for personal completion. Verify permissions and declarations before submission.


---

## 逐条回应

|编号|质疑|处理|对应改动或证据|后续边界|
|---|---|---|---|---|
|M1|比较基准与包装公平性|已改|Table 3表注明确双方均校准；摘要/贡献使用14.8%匹配对照，滚动对照分列。|无需新数据。|
|M2|推断与多重比较|已改|Section 6保留探索性推断定位；Table 5表注明确调整p只属于所命名比较族，原值全部保留。|无需重算或新检验。|
|M3|2015回顾性与复制含义|已改并限定|Introduction定义原执行协议固定的比较；Section 9明确已见历史与2015事后设计。|T1：独立交易商/前瞻观察。|
|M4|短验证与重叠标签|已改并保留负面|Sections 5--6明示52个重叠验证起点及候选配对HAC标准误带；Table 4另列52评估点和181.4%最差单元。|T2：更长验证设计，本轮不补跑。|
|M5|模拟机制与数值失败|已改|Section 7.4首句直接说明未重现周度损失；Supplement S26.4区分数值不可用与预测准确性。|T3：解耦设计/数值可执行性。|
|F1|预测报告与库存政策|已改|Section 6明确在观测路径上评分被动报告；Section 8建议仍为模型验证。|T4：干预及成本数据。|
|F2|代表性与外推|已改并限定|Section 4保留不同测量单位；Section 9集中单FX、同报告体系与回顾性范围。|T1：扩大外推前取得独立证据。|
|F3|周度测量口径|已改|Section 4补明fair-value与long-minus-short；FR2004 Section III.A公允价值规则已核对。|T4：估值/总敞口渠道需新数据。|
|F4|记录数与经济期限|已改|Section 5在H定义旁说明FX缺口延长日历跨度、周度步长不同；Section 9保留采样遗漏。|T4：更高频实际敞口。|
|F5|分数与经济价值|保留明确边界|Section 8联合报告损失、U/V和破线；Section 9明确未测量交易/资金收益与实际决策成本。|T4：货币效用另行设计。|
|E1|贡献、标题与JoF定位|已改定位；标题保留|三条经验发现覆盖五处，初等理论降级；cover letter定位于比较预测评价。|T5：标题改选由作者决定。|
|E2|经验广度|不扩大主张|Section 9与T1保留单记录/相关聚合限制；不把13类当13位独立交易商。|需要新数据，超出本轮。|
|E3|模拟增加何种证据|已改|Section 7.4/图4/Table 6明示失败或未支持；第三条贡献采用分数与破线分歧。|T3：后续机制实验。|
|E4|重复与摘要密度|已缩短Section 2|保留任务要求的三条同口径定位；摘要9个数字对应三组必要比较，仍低于10个上限。|不删必要对照或负面数字。|
|E5|投稿包与可用性|已改并核对|B6已统一v8编译路线、清单、关键词和声明；145项包检查通过，作者占位符保留，B7另做最终导出/视觉核对。|最终发布与逐页QA由B7完成。|

新数据与新实验需求集中写入Section 9及AUTHOR-TODO的T1--T6。本轮没有启动这些扩展。
