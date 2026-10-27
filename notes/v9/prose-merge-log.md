# C3 主文写法合并日志（候选稿，未替换投稿源）

本子任务只新建 `notes/v9/manuscript-c3-draft.tex` 和本日志。没有改动 `submission-jof/`、两个旧目录、归档结果、模型或实验。没有编译、提交或推送。文本依据为本轮任务、指定导师写法指南、C2后的 `notes/v9/thesis.md`、`c2-results.md` 与 `results/v9/nonstationarity/prior-stationary-reconciliation.json`；后者不存在同名 notes Markdown，已使用实际 JSON。

## 迁移方式与证据保护

- 结构采用旧 V8 的短句骨架和各段“发现先行”；PR5 六张表、四张图和全部原参考文献保留。表内仅把 primary/analogue 等改成读者名称，六表的全部数字字符串逐项断言相同，未把 PR5 的两位小数换成 V8 一位小数。
- 所有图仍指向 PR5 既有文件。C4 root 将替换千分位 Figure1 并生成合并模拟图；当前没有新增图表。`fig:mechanism` 位置保留，相关正文提前按 C4 合并图写，交付时不能把目前仍是旧图的文件误当已完成新图。
- 原标题、声明占位符和原参考文献全文保留；仅增加已核实 Hansen1992 书目，正文引用联合 OLS score 方法。可用性分支改为 revision-v9。

## 段落级合并记录

|位置|PR5 原首句 / 问题|候选稿首句与处理|证据去向|
|---|---|---|---|
|摘要|Risk limits on dealer positions concern…；数学性质占贡献位置，机制过度概括|Dealers set limits on the largest position reached…；三条经验主线，明确 stationary loss 及 switching 未识别；删数学贡献口吻|原真实锚点、C2 W52 116.2/121.4，后续由同口径计数核验|
|引言开头|A dealer's recorded net position can finish…；长解释段|Dealer position limits concern…；目标→历史基准→匹配问题，采用V8短句|Figure1、Table3及方法|
|引言贡献|C1/C2/C3，C1突出地板和经典界|First/Second/Third三条：FX；weekly/daily；stationary反证；原score/breach第三条融入FX和实践|不出现第四条贡献|
|引言路线|The remaining sections define…|Section3 defines the target and records two elementary properties used later.|目标/地板/Lévy作为背景，公式原样保留|
|相关文献三段|Net-position forecasting already has…等长句|采用V8 Wisniewski / path-risk / quantile三段；仅声明已建立方法与经验比较|原Table1数字全保留；n.r.改dash，仅指未核实维度|
|相关文献结尾|重复三点经验贡献|The empirical contribution concerns matched peak forecasts…|删重复数字，不删结果|
|目标|The forecast target is the largest sampled…|采用V8简短目标与四个原显示公式；保留命题假设和640 crossings|未改基础数学；没有把真实程序写成覆盖保证|
|Data|The FX application uses the hourly member…|采用V8短句并保留18576、706；新增原P5日频930/501和last-record定义|单做市商、vintage、未知timezone等限制集中Limits|
|Forecast methods|The primary forecasts target…及四个长段|Forecasts target…；条件方法、历史规则、local/filtered、calibration/combination短段|原菜单、refit、feature数和方法Table2不改数字|
|Evaluation|The forecasting clock admits…|At refit r, training labels are eligible…；保留标签成熟、52 validation、配对/HAC/family定义|后见历史与回溯暴露放Limits；表注保持命名family|
|Transparency|The original source-specific primaries…长过程段|The original protocol fixes the two main comparisons…|设计/失败记录一处交代；新增C2 frozen-before-calculation说明|
|7.1 FX|Long-history FX regression provides…|Long-history FX regression beats matched historical headroom…；沿用V8三短段|14.8/16.6、15.0、329/328、lower-target10.1/9.2完整保留|
|7.1 回溯|原在7.4 An expanded fixed-parameter backcast…|The full-prefix backcast also preserves reference-sensitive gains.|12.2/5.3、416/282、rawp.055和long-H收益保留；overlap/future penalties只Limits|
|7.2 负面结果|五个长段|采用V8 reference reversal / long-H / Treasury / regularization / combinations五短段|12.7/+3.2、31.5、924/427、50.8、54/28、92.6→9.2、34/48、181.4、-4.0/+2.8全部保留|
|7.2 日频|原在7.4 Same-dealer daily aggregation…|Historical headroom wins seven of eight same-record daily comparisons.|QR4 W260/H6 -3.0%、37/30保留；纯frequency识别边界Limits|
|7.3 分数/破线|Lower FX loss coexists…等长段|采用V8三短段|376/360；original Murphy pair分别；24-step20.6:1仅其reference；原Table5不改数|
|7.4 样本量解释|Controlled and within-record extensions；未讨论旧校准及新C2|Does sample size explain the low-frequency losses?；六段比较三设计|旧D0/D2、七小时失败；P5 stationary W52和W260；N1raw/Holm；C2constant/switch；缺W260；daily/hourly unavailable|
|7.4 原前提纠正|任务曾称两次平稳W52皆近持平|开头Short histories can produce large regression losses even under stationary laws.|PR5 QR33/H6/W52九格113.5–135.5%，W26021.3–36.3%；不是补跑|
|§8|Peak-limit validation should begin…等三个长段|V8三条粗体建议：matched benchmark、short-weekly corrected-rank comparator、scores+breaches|不是F自动部署政策；自身breach评估继续保留|
|Table6|原观察场景验证图|原六行保留；仅命名规范化|C4 root负责增加daily/C2列和版面，不在此稿重建|
|Limits|三大长段，重复边界散见多处|集中四段：FX chronology；weekly/measurement；causal/coverage/economic；simulation/bootstrap|指定八项限制各一次；backcast overlap、source-clock、moment/phase/boundary等保留|
|Conclusion|三大段、未来工作和机制限制重述|Simple historical rules are hard to beat for peak net positions.|三条同口径，不重复八限制；stationary反证与W260不可用明确|
|Availability/author|generic repository link，旧v8 extensions话术|revision-v9分支和各类结果说明；作者字段原样|不增加个人声明，不称已投稿|

## C2数字绑定与措辞边界

- `results/v9/nonstationarity/postrun/predictions.json`：N1 raw7/13、Holm2/13；N2 UNASSESSABLE；N3 NOT_SUPPORTED；N4 UNASSESSABLE；W52 constant116.24327967680179%，switching121.40097999787356%。显示一位小数，不以未完成W260来源补聚合。
- `results/v9/nonstationarity/prior-stationary-reconciliation.json`：P5 33-feature/H6的W52九设定113.45974253719095–135.5188592993867%，W26021.307826749419533–36.270776649491744%；这些是ratio-of-means，和C2 source-medians-of-repetition-medians不同，正文已说明。
- 旧V8 `results/v8/mc/summary.csv`：D0/D2在W52 QR33分别+1.1/+0.4，W2880 -19.8/-20.6；100重复、500origins、含intercept-only菜单、weeklyclock。不能把旧近持平结果用于覆盖P5已有大额平稳损失。
- D0完整英文口径已用：constant-variance AR(1) levels, where the peak depends on the current position。未使用no-signal标签。
- `fig:mechanism`当前仍指PR5旧figure，root C4必须完成合并图后再编译/交付；此稿未声称图已更新。

## 本轮结构自检

六个既有table环境、四个既有figure环境保留；六表数字token序列逐表与PR5完全相同；作者占位符数量相同。未编译，未运行研究。正式写法计数、数字回审、分页和逐页视觉QA由后续root检查，不能以此结构检查替代。

## Paragraph-level coverage: Sections 2-9

Paragraph IDs count prose blocks after removing tables, figures, display equations and subsection headings. Proposition titles are removed before extracting first sentences. All 50 candidate paragraphs and all 43 original PR5 paragraphs are covered. New C2 text is marked new; pending C4 material is not described as already transferred.

|Candidate paragraph|Original paragraph and first sentence|New first sentence|Actual deletion, compression or destination|
|---|---|---|---|
|2.1|PR5 2.1: Net-position forecasting already has a close empirical lineage in the market-making literature, where Wisniewski and colleagues predict signed next-hour endpoint intervals.|Wisniewski and colleagues forecast signed next-hour position intervals using historical states, calendar information and local prediction methods .|Shorten endpoint lineage and retain its citations and label distinction.|
|2.2|PR5 2.2: Financial path-risk studies establish that a within-period extreme can matter more than the value observed at the end of the period.|Path-risk forecasts address within-period extremes.|Shorten path-risk background; preserve partial-reading scope in Table 1 note.|
|2.3|PR5 2.3: Quantile estimation and evaluation supply established tools for comparing conditional peak forecasts against historical rules on a shared response.|Regression quantiles target asymmetric forecast errors directly .|Retain established quantile/scoring methods and citations; remove repeated positioning.|
|2.4|PR5 2.3: Quantile estimation and evaluation supply established tools for comparing conditional peak forecasts against historical rules on a shared response.|The empirical contribution concerns matched peak forecasts and the stability of their rankings.|Add concise empirical positioning; remove repeated contribution numbers.|
|3.1|PR5 3.1: The forecast target is the largest sampled absolute position between the issue time and the end of the stated forecast horizon.|The target is the largest sampled absolute position from issue time through the stated horizon.|Shorten target introduction; all original display equations stay identical.|
|3.2|PR5 3.2: The inclusion of the issue position matters because a feasible peak limit must already cover the exposure observed at the forecast origin.|A feasible limit covers the current observed exposure.|Retain floor and breach definitions; passive reporting is retained in 6.3 and cash/policy scope in 9.2/9.4.|
|3.3|PR5 3.3: Suppose \(Y B\) almost surely and the issue information contains \(B\).|Suppose \(Y B\) almost surely and the issue information contains \(B\).|Keep proposition assumptions, statement and equation.|
|3.4|PR5 3.4: Let future increments be independent and individually symmetric about zero, with partial sums \(S h\).|Let future increments be independent and individually symmetric about zero, with partial sums \(S h\).|Keep classical-bound assumptions, statement and equation; remove contribution status.|
|3.5|PR5 3.5: The Supplement gives both proofs and distinguishes the population endpoint quantile from the empirical endpoint estimate used by the corresponding benchmark.|The Supplement proves both statements and compares population quantiles with their empirical plug-ins.|Shorten proof/plugin distinction; refer to existing Supplement proofs, without claiming a new transfer.|
|3.6|PR5 3.6: Forecasts for longer horizons should also respect the nesting of the underlying path maxima, which makes the true horizon quantiles ordered.|Separately fitted horizon forecasts can violate the ordering of true peak quantiles.|Shorten coherence explanation; retain the 640 crossings.|
|4.1|PR5 4.1: The FX application uses the hourly member of the publicly described Net Position Time Series Dataset, representing a market maker's net client-flow position .|The FX application uses the hourly Net Position Time Series Dataset, reporting market-maker client-flow positions .|Shorten FX description; retain 18576 and the distinct issue grids.|
|4.2|PR5 4.2: The weekly application uses Primary Dealer Statistics published by the Federal Reserve Bank of New York .|The weekly data are New York Fed Primary Dealer Statistics .|Retain 706, USD millions, fair-value/long-minus-short and sources; reporting/vintage limits are in 9.2.|
|4.3|PR5 4.4: Daily aggregation of the same dealer produces 930 nonempty source-naive calendar days and 501 common evaluation issues.|Daily aggregation takes the last recorded position on each nonempty source-naive calendar day.|Move daily target definition into Data; retain 930/501/last-record rule; clock caveats go to 9.2/9.3.|
|4.4|PR5 4.3: The FX record describes one market maker, while the weekly series combine signed positions across primary dealers.|Every method within a comparison uses identical peak labels, current floors and issue origins.|Shorten alignment and units; single-maker/related-category restrictions are concentrated in 9.1/9.2.|
|5.1|PR5 5.1: The primary forecasts target the conditional quantile at \( =19/20\), with its upper tail defining the strict-breach event.|Forecasts target the conditional quantile at \( =19/20\).|Shorten tau, horizon and record-clock definition; actual-cost restriction is in 9.4.|
|5.2|PR5 5.2: Historical rules serve as substantive competitors because they can already adapt their limits to the position observed at the forecast origin.|Historical headroom uses the corrected empirical rank of completed headrooms and adds its report to the current magnitude.|Retain corrected rank, current floor and translated/peak/endpoint definitions.|
|5.3|PR5 5.3: Conditional quantile regression links completed peak headroom to issue-known position histories and calendar information, using training-based transformations and ridge regularization.|Ridge quantile regression links mature headroom to issue-known position states and calendar variables.|Retain 33 plus intercept and four features; causal predictor interpretation is addressed in 9.4.|
|5.4|PR5 5.4: Local quantile methods condition on neighboring historical states, with a scale-adjusted variant using training information to normalize the comparison.|Local quantiles use neighboring historical states, with an increment-scaled variant.|Shorten method descriptions; complete prior failures remain in the existing Supplement.|
|5.5|PR5 5.5: The further robustness comparisons address calibration, forecast combination, and conservative selection while keeping the peak response and chronological information restrictions explicit.|Further comparisons apply delayed calibration, fixed combinations and conservative selection to the same peak response.|Retain mature calibration, fixed combinations and paired-HAC one-SE definition.|
|6.1|PR5 6.1: The forecasting clock admits a training label only after the entire response horizon has ended, preventing an unfinished peak from entering estimation.|At refit \(r\), training labels are eligible only when \(i+H r\).|Shorten label/validation process; future-selected prefix penalties are stated in 9.1.|
|6.2|PR5 6.2: Matched comparisons hold the completed-response history and refit schedule fixed when evaluating the regression against the historical headroom rule.|Matched comparisons fix completed-response history and refit schedule for regression and historical headroom.|Replace internal primary labels; distinguish matched and shorter rolling references.|
|6.3|PR5 6.3: We evaluate forecast accuracy with mean pinball loss and report strict breaches separately, including their frequency and the associated overrun amounts.|Accuracy uses mean pinball loss; breaches are strict peak exceedances.|Shorten loss/HAC/hit explanation; retain passive reports, adjustment families and fixed grid.|
|6.4|PR5 6.4: The original source-specific primaries retain their original roles, outcomes, and reference procedures throughout this paper. / PR5 6.5: The Supplement provides the complete prior and later comparison inventories, the exact evaluation clocks, numerical checks, and all incomplete or unsuccessful procedures.|The original protocol fixes the two main comparisons and their reference procedures.|Merge two process paragraphs; existing inventories remain cited, while new C2 records currently remain in results/notes.|
|7.1|PR5 7.1: Long-history FX regression provides the clearest repeated improvement against a historical headroom rule using the same completed history and update schedule.|Long-history FX regression beats matched historical headroom in both periods.|Use finding/numbers/table sequence; retain 14.8/16.6.|
|7.2|PR5 7.2: The delayed ACI adjustment preserves the matched FX score advantage while bringing the two observed breach frequencies close together.|Delayed calibration retains the later matched FX gain.|Retain later-period, both-wrapped scope and 15.0/329/328.|
|7.3|PR5 7.3: The long-history FX gain also persists across the evaluated position-increment states and at the lower target quantile.|The long-history FX gain persists across training-defined increment-RMS states and at the lower target quantile.|Retain state/lower-target 10.1/9.2 and upper-quantile failures.|
|7.4|PR5 7.14: An expanded fixed-parameter backcast preserves the reference-sensitive pattern but supplies no fresh independent validation.|The full-prefix backcast also preserves reference-sensitive gains.|Move backcast from old 7.4 to new 7.1; retain 12.2/5.3/416/282/.055 and long-H gains; exposure is in 9.1.|
|7.5|PR5 7.4: The advantage changes when the reference changes, even for the same long-history FX regression report at the shorter horizon.|The earlier FX ranking reverses when the reference changes.|Shorten reference reversal; retain 12.7/+3.2.|
|7.6|PR5 7.5: Short histories and longer horizons produce additional adverse outcomes that prevent a broad ranking of regression above historical forecasting rules.|Short-history FX regression performs poorly at the longer horizon.|Shorten adverse longer-horizon result; retain 31.5 and 924/427.|
|7.7|PR5 7.6: The original Treasury-bill primary loses on both score and breach count.|Treasury-bill regression loses on both accuracy and breaches.|Shorten Treasury result; retain 50.8 and 54/28.|
|7.8|PR5 7.7: Heavier regularization improves the additional weekly panel substantially but leaves historical rules ahead in most of its evaluated cells.|Stronger regularization narrows weekly panel losses but leaves historical rules ahead.|Retain 92.6 to 9.2, 34/48 and the named 181.4 worst cell.|
|7.9|PR5 7.8: Simpler conditional descriptions and forecast combinations also produce mixed outcomes rather than a uniform solution to the weekly regression losses.|Simpler conditional reports and fixed combinations also give mixed weekly results.|Retain combination -4.0/+2.8 and worse recursion.|
|7.10|PR5 7.13: Same-dealer daily aggregation produces predominantly historical-rule score wins.|Historical headroom wins seven of eight same-record daily comparisons.|Move daily result from old 7.4 to new 7.2; retain 7/8, QR4 W260/H6 -3.0 and 37/30; frequency scope is in 9.3.|
|7.11|PR5 7.9: The matched FX gain comes with more breaches before calibration, showing why pinball accuracy and exceedance frequency deserve separate reporting.|Lower FX loss coexists with more breaches before calibration.|Retain matched 376/360 and the score/hit distinction.|
|7.12|PR5 7.10: Murphy diagrams reveal that forecast rankings can depend on the scoring rule even when the quantile level and reports stay fixed.|Elementary-score rankings cross for both original main comparisons (Figures and ).|Retain both original Murphy pairs and the separate 24-step 20.6:1 reference.|
|7.13|PR5 7.11: Table places the working-reference loss tests alongside the fixed-grid coverage results, preserving their distinct null hypotheses and comparison families.|Loss and hit diagnostics answer different questions (Table ).|Shorten diagnostics; Table 5 numbers, nulls and family notes stay.|
|7.14|PR5 7.12: The controlled mean-reverting level study with GARCH innovations rejects the proposed narrow-regime explanation .|Short histories can produce large regression losses even under stationary laws.|Add a corrected three-design question; this is writing from frozen outputs, not a new run.|
|7.15|No PR5 paragraph. V8 original 7.4: The calibrated simulation does not reproduce the persistent weekly losses in the financial record.|The earlier weekly-calibrated design uses a six-candidate menu including an intercept-only limit.|Add saved V8 calibrated evidence; its full grid is not yet moved into v9 Supplement and remains C4 work.|
|7.16|PR5 7.12: The controlled mean-reverting level study with GARCH innovations rejects the proposed narrow-regime explanation .|The controlled stationary grid uses narrower original menus and an hourly feature clock .|Retain 72-cell MISMATCH and 2/12 versus 6/60; add source-checked stationary-loss ranges from old tables.|
|7.17|New C2 paragraph; no corresponding PR5 prose paragraph.|The new experiment calibrates constant and segmented AR—GARCH—t processes to pre-evaluation prefixes of thirteen weekly series.|New C2 method/diagnostic paragraph from the registered protocol and postrun results.|
|7.18|New C2 paragraph; no corresponding PR5 prose paragraph.|At history 52, the across-source median loss increase is 116.2% for the constant arm and 121.4% for switching.|New C2 W52 medians and missing W260 statement; no incomplete-source substitution.|
|7.19|New C2 paragraph; no corresponding PR5 prose paragraph.|The daily fitted null fails the fourth-moment qualification, and the matched-calendar hourly null fails optimization.|New C2 daily/hourly unavailable states and unresolved interpretation.|
|8.1|PR5 8.1: Peak-limit validation should begin with the information set and the comparison rule before examining a candidate model's favorable performance statistic.|Benchmark against historical headroom.|Turn process into a named matched-benchmark recommendation.|
|8.2|PR5 8.3: For a limit manager, the key decision is whether extra conditioning improves the chosen monitoring objective reliably enough to justify the additional estimation.|In short weekly samples, retain the corrected-rank rule as a demanding benchmark.|Retain 36.5 and assessment of F breaches; do not authorize deployment by score superiority.|
|8.3|PR5 8.2: A practical validation record should also keep scores, breaches, and stability together rather than replacing one assessment with another after seeing the results.|Report breaches with the score.|Turn joint-evaluation paragraph into score/breach recommendation; fold old third contribution into this advice and FX evidence.|
|9.1|PR5 9.1: The FX evidence comes from a single market maker's client-flow record, limiting conclusions about other dealers, currencies, and market-making arrangements. / PR5 6.4: The original source-specific primaries retain their original roles, outcomes, and reference procedures throughout this paper. / PR5 7.14: An expanded fixed-parameter backcast preserves the reference-sensitive pattern but supplies no fresh independent validation.|The FX evidence describes a single market maker's client-flow record.|Concentrate single maker and chronology; explicitly retain issue-date-later penalties, nesting and earlier target-path scoring.|
|9.2|PR5 9.2: The weekly data are signed position-category aggregates, so offsetting exposures across dealers can reduce the aggregate while individual gross exposures remain large. / PR5 3.2: The inclusion of the issue position matters because a feasible peak limit must already cover the exposure observed at the forecast origin.|The weekly categories share a reporting system and economic components; they are related aggregate tasks, not independent dealer replications.|Concentrate reporting/vintage/gross/cash/sampled-target and unknown daily clock limits.|
|9.3|PR5 4.4: Daily aggregation of the same dealer produces 930 nonempty source-naive calendar days and 501 common evaluation issues. / PR5 7.13: Same-dealer daily aggregation produces predominantly historical-rule score wins. / PR5 9.2: The weekly data are signed position-category aggregates, so offsetting exposures across dealers can reduce the aggregate while individual gross exposures remain large.|Daily aggregation jointly changes physical histories, horizons, update cadence, calendar predictors, evaluation span and sampled targets.|Retain joint changes in daily history/horizon/cadence/predictors/span/target; no pure frequency claim.|
|9.4|PR5 9.3: The later analyses and working-reference tests describe the observed records after earlier results had informed the research process and additional comparisons. / PR5 5.1: The primary forecasts target the conditional quantile at \( =19/20\), with its upper tail defining the strict-breach event.|The design gives no causal interpretation or individual-predictor effects.|Concentrate causal/coverage/trading-funding/cost limits; author declarations stay untouched.|
|9.5|PR5 9.3: The later analyses and working-reference tests describe the observed records after earlier results had informed the research process and additional comparisons. / PR5 7.12: The controlled mean-reverting level study with GARCH innovations rejects the proposed narrow-regime explanation .|The simulation designs use different menus, clocks, calibration laws and summary statistics.|Add C2 model/bootstrap/phase/boundary/failure scope; no claim that C4 Supplement integration has occurred.|

## Same-checker writing measurement

The unchanged pure functions/adapter in notes/v9/writing_check.py were called with stdout output only. No checker change or extra report JSON was written. Scope: Introduction through Conclusion excluding floats, displays, references and declarations; abstract is separate and primary is counted in main source.

|Snapshot|Sentences|Flagged sentence proportion|Mean words|Over 40|Forbidden body terms|Main primary|Abstract words/numbers|
|---|---:|---:|---:|---:|---:|---:|---:|
|PR5 before|246|14.227642%|18.605691|1|2|22|162/4|
|v9 C3 draft|250|1.600000%|11.436000|0|0|3|138/9|

Source SHA256 bindings:

- PR5 before: `66287e0d3b192affe04a4c974a1d0141fe3a3be8eda4da074552be5828bead40`.
- v9 C3 draft: `cb8cc6e249ee226f6f598ff130a6a3ff7963cd885554d35607ac92d2b7b2d598`.
- Section 7.4: 458 prose words.
- Conclusion: 101 prose words.
- Six table numeric-token sequences, four display equations and every original bibliography entry are preserved. All labels are unique; all references/citations resolve. The added Hansen citation has its verified bibliography entry.
- No compilation or pagination was performed. The current fig:mechanism file awaits the C4 combined replacement; Table 6 awaits C4 expansion. Root owns the final number audit, pagination and visual checks.
- Before the final edits, both untracked candidates were retained as versioned backups in .scratch/v9/retained-backups/ with timestamp 20261024T193707482019Z.
