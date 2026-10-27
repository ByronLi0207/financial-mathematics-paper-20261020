# H5 刷新后的主文主张—证据映射

UTC：2026-10-27T05:00:10.078723+00:00；当前主文 SHA-256：`6f9f196f4bc9637674e253b5194bc0717a0c8b4436ca61047a96dc8736519cc8`。

原H4的58组主张全部保留并按精确before→after记录刷新；新增三篇ASMBI文献语境，共61组。H4旧版保存在提交`b4c7eb1`。本轮不重验旧数值，不运行金融计算。

当前原文由H4源顺序应用28个主文替换精确重建，结果与[submission-final/manuscript.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex>)逐字节一致。两个cover-letter改动不属于此主文重建。

## 已解决的写作风险与仍保留的实质边界

- **H4已解决 / H4-R1**：当前标题改benchmark-default；G3.R2失败结果保留。 [当前定位](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:355>)。
- **H4已解决 / H4-R2**：当前正文明确local before/public afterward，并用prewritten screens；非外部预注册。 [当前定位](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)。
- **H4已解决 / H4-R3**：当前明确required numerical fits，G1保真6/10与未运行三格及undetermined判断保留。 [当前定位](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:310>)。
- **H5已处理 / C19 / 原P2**：Each new analysis states thresholds before computation 总括需保留逐组来源精度；不能暗示每个原Git对象均可复核或外部预注册。 对应精确编辑：`/changes/15`。
- **H5已处理 / C25 / 原P2**：link conditional gains to history/strong shrinkage 只支持 tested configurations，后文 sufficient history 不宜读作充分条件。 对应精确编辑：`/changes/16`, `/changes/21`。
- **H5已处理 / C27 / 原P2**：正文partial support未直述QR33 P2 planned0；S39保留但只读正文者可能高估高history测试覆盖。 对应精确编辑：`/changes/17`。
- **H5已处理 / C33 / 原P2**：摘要29/34未就近说明事后取corrected/ordinary较好者；不能当作单一实时可执行F的胜率。 对应精确编辑：`/changes/1`。
- **H5已处理 / C35 / 原P2**：Why does regression lose 和 indicates limited incremental information 可能被读成因果/信息不存在；证据只提供菜单内诊断。 对应精确编辑：`/changes/18`, `/changes/19`, `/changes/21`。
- **H5已处理 / C38 / 原P2**：摘要/intro泛称regression medians宜点明full版本；QR4 H6 median screen未达预定5pp。 对应精确编辑：`/changes/2`, `/changes/4`, `/changes/5`, `/changes/8`, `/changes/20`, `/changes/22`。

当前未保留活跃P1/P2写作冲突；原风险已归档。处理含义是收紧文字，不表示消除失败屏、无法判定、观察设计、权利或外部有效性限制。逐条回应见[notes/submission/h5-review-response.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/h5-review-response.md>)。

## 全文逐组映射

### C01｜采样绝对净头寸峰值与 endpoint 漏掉中间 breach

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[24](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:24>)；[29](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:29>)；[65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)；[84](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:84>)；[88](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:88>)；[91](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:91>)；[379](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:379>)。

**当前表/图/命题/章节：**[fig:example](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:29>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `json:notes/v7/example-selection.json#/selection`：[notes/v7/example-selection.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v7/example-selection.json>)，`#/selection`。

**证据支持：**定义和保存例图路径一致：origin408，endpoint48144 < report73139 < peak74397，单位USD millions。

**保留边界：**仅采样净头寸，不能直接代表gross exposure、PnL或连续时间极值。 当前新增限定：净头寸峰值不识别gross portfolios、hedging arrangements或economic capital requirements；没有新增这些对象的数据或模型。

### C02｜pinball、strict breach与floor/headroom恒等式

**当前主文位置：**[88](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:88>)；[95](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:95>)；[191](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:191>)。

**当前表/图/命题/章节：**[prop:floor](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:98>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#the tail qualification requires the true conditional quantile`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:67>)。

**原文献：**[koenker1978](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:468>)；[gneiting2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:451>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**正文公式明确响应、损失、strict exceedance；S1区分投影和真实条件分位。

**保留边界：**loss降低不等于breach次数降低。

### C03｜已知floor投影逐点不增loss、真实条件分位的strict coverage

**当前主文位置：**[98](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:98>)；[102](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:102>)。

**当前表/图/命题/章节：**[prop:floor](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:98>)；[sup:floor](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:55>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#Proposition 1: floor projection`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:63>)。

**证据支持：**S1提供逐点恒等式及真实lower inverse quantile覆盖论证。

**保留边界：**覆盖陈述属于真实条件分位，拟合报告不自动继承。

### C04｜独立对称增量下经典endpoint-to-peak界

**当前主文位置：**[105](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:105>)；[109](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:109>)。

**当前表/图/命题/章节：**[prop:levy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:105>)；[sup:levy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:102>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#section{Classical endpoint-to-peak`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:102>)。

**证据支持：**命题与S2列独立、逐个对称、population endpoint quantile及条件应用要求。

**保留边界：**经验plug-in不是覆盖保证，金融依赖未满足该定理前提。

### C05｜horizon可能crossing；mean-reverting levels与serial increments需区分

**当前主文位置：**[112](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:112>)；[115](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:115>)。

**当前表/图/命题/章节：**[sup:simulation-original](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:148>)；[sup:simulation-primary](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:193>)；[sup:simulation-secondary](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:247>)；[sup:coherence](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1120>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `old:75`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/75`；唯一CSV筛选 `{"source": "fx_hourly", "window": "720", "method": "QR"}`；字段 `strict_crossing_count`。

**证据支持：**640个short-history FX crossing有原字段；S3–S5保留不同过程说明。

**保留边界：**例示过程不证明实际金融序列独立/对称。

### C06｜匹配目标/完成标签/历史/refit；rolling reference另列

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[26](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:26>)；[44](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:44>)；[65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)；[167](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[189](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:189>)；[252](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:252>)；[366](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:366>)。

**当前表/图/命题/章节：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)；[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)；[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#paragraph{Completed labels`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1191>)。

**证据支持：**S23给出成熟标签索引与held transforms，方法表和原protocol分开rolling reference。

**保留边界：**匹配比较不隔离feature因果效果。

### C07｜FX一个market maker、18576记录及不同chronological grids

**当前主文位置：**[122](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:122>)；[377](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:377>)。

**当前表/图/命题/章节：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:76`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/76` → `protocol/revision-20261022/study-spec.json#/sources/fx_hourly/record_count`。
- `text:submission-final/supplement.tex#The FX evidence describes`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1627>)。

**原文献：**[dataset](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:472>)；[wisniewski2020](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:484>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**record_count来自原study-spec；单一市场商与original period inspected由数据/原scope支持。

**保留边界：**单一dealer，无未见prospective金融确认。

### C08｜NY Fed Treasury706记录、聚合long-minus-short与额外类别

**当前主文位置：**[124](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:124>)。

**当前表/图/命题/章节：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)；[sup:panel](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:512>)；[sup:panel-second](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:577>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:77`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/77` → `protocol/revision-20261022/study-spec.json#/sources/nyfed_weekly/record_count`。

**原文献：**[nyfeddata](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:445>)；[fr2004_2013](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:425>)；[fr2004_2024](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:427>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**record_count绑定study-spec；官方数据/FR2004引用对应定义。

**保留边界：**下载economic-date vintage；aggregated net不是individual gross risk。

### C09｜FX日度930天/501issues与same-source聚合边界

**当前主文位置：**[126](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:126>)；[132](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:132>)。

**当前表/图/命题/章节：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)；[sup:v8-daily](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1328>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:96`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/96` → `results/revision-v8/wp4/summary.json#/source_consistency/daily_metadata/n_daily`。
- `old:97`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/97` → `results/revision-v8/wp4/summary.json#/cells/0/evaluation/n`。
- `text:submission-final/supplement.tex#Daily aggregation jointly changes`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1631>)。

**证据支持：**summary保存n_daily和evaluation n；每日最后记录与partial boundary days按原规则。

**保留边界：**同时改变跨度/时钟/响应等，纯频率效应未识别。

### C10｜CFTC survivor universe、17合格代码及full-sample OI排序

**当前主文位置：**[32](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:32>)；[128](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:128>)；[379](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:379>)。

**当前表/图/命题/章节：**[tab:v10-cftc-contracts](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-cftc-contracts.tex:4>)；[sup:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1528>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `new:1`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/1`。
- `new:2`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/2`。
- `json:results/v10/cftc/eligibility.json#/selected`：[results/v10/cftc/eligibility.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/eligibility.json>)，`#/selected`。
- `text:submission-final/supplement.tex#Full-period mean open interest`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1531>)。

**原文献：**[cftcTFF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:435>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**eligibility保存全部候选/排除/选中17代码；20上限没截断，OI排序只排列survivors。

**保留边界：**独立reporting system不等于独立dealer复制。 当前新增限定：净头寸峰值不识别gross portfolios、hedging arrangements或economic capital requirements；没有新增这些对象的数据或模型。

### C11｜CFTC877周、52/260分段、H6、13步refit与经济/发布时钟

**当前主文位置：**[130](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:130>)；[380](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:380>)。

**当前表/图/命题/章节：**[sup:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1528>)；[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `new:0`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/0` → `results/v10/cftc/eligibility.json#/N`。
- `new:4`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/4` → `results/v10/cftc/splits.json#/indices/validation_n`。
- `new:5`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/5` → `results/v10/cftc/splits.json#/indices/evaluation_n`。
- `new:6`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/6` → `results/v10/cftc/splits.json#/indices/unissued_gap_n`。
- `new:9`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/9` → `results/v10/cftc/splits.json#/actual_dates/evaluation/first`。
- `new:10`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/10` → `results/v10/cftc/splits.json#/actual_dates/evaluation/last`。
- `new:11`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/11` → `results/v10/cftc/splits.json#/actual_dates/evaluation/last_label_end`。
- `new:58`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/58` → `results/v10/cftc/manifest.json#/design/horizon`。
- `new:59`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/59` → `results/v10/cftc/manifest.json#/design/windows`。
- `new:60`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/60` → `results/v10/cftc/manifest.json#/design/refit_step`。
- `text:submission-final/supplement.tex#Actual positions are normally measured`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1534>)。

**证据支持：**splits/manifest支持所有日期/长度/refit；S30保留周二测量周五发布及delay说明。

**保留边界：**首次发布vintage未重建，不能称实时public-information-clock策略。

### C12｜描述表全部字段与九个within-series统计分别跨源取median

**当前主文位置：**[132](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:132>)；[134](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:134>)。

**当前表/图/命题/章节：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `descriptives:numeric_bindings`：[results/v12/descriptives/number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v12/descriptives/number-bindings.json>)，`#/numeric_bindings`。
- `descriptives:table_bindings`：[results/v12/descriptives/number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v12/descriptives/number-bindings.json>)，`#/table_bindings`。
- `json:results/v12/descriptives/metadata.json#/definitions`：[results/v12/descriptives/metadata.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v12/descriptives/metadata.json>)，`#/definitions`。

**证据支持：**现有1324 numeric与100 table binding逐指针/源SHA读回；metadata date display规则保留。

**保留边界：**未重算统计；不同单位不池化为common-dollar风险。

### C13｜corrected rank历史headroom、sample-max cap、重锚/peak floor、tau和horizon

**当前主文位置：**[140](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:140>)；[142](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:142>)；[144](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:144>)；[145](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:145>)；[147](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:147>)；[148](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:148>)；[149](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:149>)；[170](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:170>)；[171](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:171>)；[172](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:172>)；[176](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:176>)。

**当前表/图/命题/章节：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[sup:rank](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)；[prop:levy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:105>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `json:protocol/revision-20261022/study-spec.json#/tau_numerator`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/tau_numerator`。
- `json:protocol/revision-20261022/study-spec.json#/tau_denominator`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/tau_denominator`。
- `text:submission-final/supplement.tex#section{Ordinary quantile ranks`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)。

**证据支持：**tau19/20与H按后续源记录计数；S8给rank和minimizer convention。

**保留边界：**依赖下无finite-sample coverage；同H不同源不代表相同物理时长。

### C14｜QR33/QR4特征、ridge、训练缩放、projection与finite/infinite菜单

**当前主文位置：**[151](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:151>)；[153](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:153>)；[154](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:154>)；[155](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:155>)；[156](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:156>)；[158](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:158>)；[159](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:159>)；[160](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:160>)；[173](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:173>)；[175](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:175>)；[180](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:180>)。

**当前表/图/命题/章节：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)；[sup:rank](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `json:protocol/revision-20261022/study-spec.json#/feature_count_without_intercept`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/feature_count_without_intercept`。
- `json:protocol/revision-20261022/study-spec.json#/features`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/features`。
- `v12:30`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/30`。
- `text:submission-final/supplement.tex#paragraph{Regression and local quantiles`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1200>)。

**原文献：**[koenker1978](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:468>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**原特征/目标式、五finite与六点版本有保存定义；projection发行/评分，非training objective内。

**保留边界：**infinite为lower ordinary quantile，不同corrected F；菜单改变即程序改变。

### C15｜local/filtered/forest/tail等已执行有限规格及失败库存

**当前主文位置：**[162](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:162>)；[174](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:174>)；[177](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:177>)。

**当前表/图/命题/章节：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[sup:ar](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:375>)；[sup:levy-empirical](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:297>)；[sup:reproduction](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1583>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `json:protocol/revision-20261022/study-spec.json#/knn_rank`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/knn_rank`。
- `text:submission-final/supplement.tex#Local methods use training-only`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1204>)。

**原文献：**[hull1998](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:466>)；[barone1999](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:423>)；[meinshausen2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:476>)；[mcneilfrey2000](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:474>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**原引用对应算法类别；S7/S11–18/S34给完整执行库存与失败，不新跑算法。

**保留边界：**不能代表所有现代distributional模型。

### C16｜delayed calibration/SAV、固定组合、earlier one-SE与later gate分离

**当前主文位置：**[164](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:164>)；[178](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:178>)。

**当前表/图/命题/章节：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[sup:wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:793>)；[sup:wp2-pairs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:855>)；[sup:wp3](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:899>)；[sup:selection](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:674>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#Updates wait for the full`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1541>)。
- `text:submission-final/supplement.tex#section{Finite delayed calibration`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:793>)。

**原文献：**[engle2004](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:443>)；[gibbs2021](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:449>)；[hastie2009](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:462>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**原方法引用与补充执行设置；成熟反馈后更新，固定组合成员，one-SE倾向强shrinkage。

**保留边界：**延迟反馈不构成覆盖保证；1SE不是显著性水平。

### C17｜训练标签必须成熟、训练变换固定；原validation与fixed backcast penalty分开

**当前主文位置：**[187](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:187>)。

**当前表/图/命题/章节：**[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)；[sup:v8-backcast](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1356>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `json:protocol/revision-20261022/study-spec.json#/sources`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/sources`。
- `text:submission-final/supplement.tex#paragraph{Completed labels`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1191>)。

**证据支持：**r-H-W+1..r-H训练区间与原protocol/S23一致。

**保留边界：**成熟label不补齐真实发布时间，backcast固定penalty仍是事后研究。

### C18｜HAC/DM、HLN/Holm、多family与sparse hit likelihood

**当前主文位置：**[191](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:191>)；[192](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:192>)；[194](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:194>)；[195](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:195>)；[197](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:197>)。

**当前表/图/命题/章节：**[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)；[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)；[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)；[sup:v10-diagnostics](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1579>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `old:45`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/45`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `dm_p`。
- `old:46`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/46`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `hln_p`。
- `old:47`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/47`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `primary_bonferroni_p`。
- `old:48`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/48`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `dm_p`。
- `old:49`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/49`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `hln_p`。
- `old:50`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/50`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `archived72_holm_p`。
- `old:51`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/51`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `dm_p`。
- `old:52`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/52`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `hln_p`。
- `old:53`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/53`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `holm_p`。
- `text:submission-final/supplement.tex#paragraph{Working-reference inference`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1221>)。

**原文献：**[dm1995](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:437>)；[nw1987](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:478>)；[hln1997](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:460>)；[holm1979](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:464>)；[kupiec1995](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:470>)；[christ1998](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:433>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**保存推断字段有不同family和HLN/带宽标签；S23明示初始hit条件化。

**保留边界：**working-reference p值不包括research-stage选择；nonrejection不证明coverage。

### C19｜透明度：原FX已查看、逐组设计/运行时序、回顾性与相关任务

**当前主文位置：**[202](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:202>)；[378](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:378>)。

**当前表/图/命题/章节：**[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)；[sup:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:1>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `json:notes/submission/prediction-register.json#/timing_by_group`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/timing_by_group`。
- `text:submission-final/supplement.tex#Its original evaluation period was viewed`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1627>)。

**证据支持：**逐轮保留现有local/public时序及原design-object可用性；不再笼统称每项新分析均可核验原对象。

**保留边界：**Git留档不是外部注册，E5原对象不可读只能按保存回执，全部金融检查仍回顾性。

**原P2处理：**写作范围已限定，实质边界保留；精确编辑 `/changes/15`。

### C20｜MCS逐格90%、R/1000stationary bootstrap、block规则与duplicate处理

**当前主文位置：**[206](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:206>)；[208](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:208>)。

**当前表/图/命题/章节：**[sup:v10-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1546>)；[sup:v13-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:1>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `new:52`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/52` → `results/v10/mcs/manifest.json#/design/package`。
- `new:53`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/53` → `results/v10/mcs/manifest.json#/design/confidence`。
- `new:54`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/54` → `results/v10/mcs/manifest.json#/design/statistic`。
- `new:55`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/55` → `results/v10/mcs/manifest.json#/design/bootstrap`。
- `new:56`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/56` → `results/v10/mcs/manifest.json#/design/bootstrap_repetitions`。
- `new:57`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/57` → `results/v10/mcs/manifest.json#/design/block_size`。
- `text:submission-final/generated/v13-supplement.tex#Joint comparison leaves`：[submission-final/generated/v13-supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:3>)。

**原文献：**[mcs2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:455>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**manifest保存arch版本、nominal参数；相同loss column合并后恢复label。

**保留边界：**依赖假设、样本与research-stage选择限制名义解释，不做跨市场独立pooled test。

### C21｜大多数MCS保留历史与替代方法，未建立等风险/唯一优胜

**当前主文位置：**[290](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:290>)。

**当前表/图/命题/章节：**[tab:v10-mcs-main](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-mcs-main.tex:3>)；[sup:v10-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1546>)；[sup:v13-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:1>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `new:41`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/41` → `results/v10/mcs/summary.json#/overall/planned_comparisons`。
- `new:42`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/42` → `results/v10/mcs/summary.json#/overall/metrics/matched_FI_membership/count_successful`。
- `new:43`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/43` → `results/v10/mcs/summary.json#/overall/metrics/literal_sole_FI/count_successful`。
- `new:44`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/44` → `results/v10/mcs/summary.json#/overall/metrics/sole_loss_class_FI/count_successful`。
- `new:47`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/47` → `results/v10/mcs/summary.json#/overall/unavailable_method_slots`。

**证据支持：**90/98格有matched历史；literal sole2、sole loss class4；未完成方法slot保留。

**保留边界：**不淘汰不等价风险，不保证future coverage或simultaneous best。

### C22｜FX两期matched14.77/16.62% gain，rolling -12.66/+3.17及issues/breaches

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[44](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:44>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)；[216](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:216>)；[225](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)；[228](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:228>)；[229](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:229>)；[230](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:230>)；[231](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:231>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/章节：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:0`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/0`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `relative_mean_loss_difference_percent`。
- `old:1`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/1` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/0/ratio_change_percent`。
- `old:7`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/7`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `strict_breach_count_left`。
- `old:8`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/8`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `strict_breach_count_right`。
- `old:12`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/12`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `relative_mean_loss_difference_percent`。
- `old:13`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/13`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `origin_count`。
- `old:14`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/14`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `strict_breach_count_left`。
- `old:15`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/15`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`；字段 `strict_breach_count_right`。
- `old:16`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/16`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`；字段 `origin_count`。
- `old:17`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/17` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/1/ratio_change_percent`。
- `old:18`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/18` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/1/n`。
- `old:19`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/19` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/0/n`。
- `old:20`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/20`；唯一CSV筛选 `{"phase": "retro", "source": "fx_hourly", "series_key": "fx_hourly", "horizon": "6", "window": "2880", "report": "R0"}`；字段 `strict_breach_count`。
- `old:21`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/21`；唯一CSV筛选 `{"phase": "retro", "source": "fx_hourly", "series_key": "fx_hourly", "horizon": "6", "window": "2880", "report": "F"}`；字段 `strict_breach_count`。

**证据支持：**paired CSV和earlier HAC results逐字段支持全部FX表行；四舍五入支持abstract14.8/16.6。

**保留边界：**matched conditioning gain不决定短rolling排序，且不是prospective确认。

### C23｜FX短history H24 +31.5% loss、924/427 breaches

**当前主文位置：**[218](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:218>)。

**当前表/图/命题/章节：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)；[sup:coherence](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1120>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:23`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/23`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h24-QR720-minus-frozen_F720"}`；字段 `relative_mean_loss_difference_percent`。
- `old:24`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/24`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h24-QR720-minus-frozen_F720"}`；字段 `strict_breach_count_left`。
- `old:25`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/25`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h24-QR720-minus-frozen_F720"}`；字段 `strict_breach_count_right`。

**证据支持：**同一contrast的loss/breaches字段可读回。

**保留边界：**特定H/history adverse case不能概括所有QR经济失败。

### C24｜wrapper保留later FX gain -15.00%，329/328 breaches

**当前主文位置：**[220](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:220>)；[232](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:232>)。

**当前表/图/命题/章节：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)；[sup:wp2-pairs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:855>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:2`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/2` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/qr_minus_f_loss_percent`。
- `old:3`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/3` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/qr_hits`。
- `old:4`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/4` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/f_hits`。
- `old:22`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/22` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/n`。

**证据支持：**wrapped_pairs/1共同origin、loss与hits原字段完整。

**保留边界：**是finite delayed ACI exercise，不是新RP gate；score/breach不一致仍在。

### C25｜FX history learning curve非单调、QR4改符号、各自matched F

**当前主文位置：**[44](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:44>)；[240](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:240>)；[243](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:243>)；[306](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:306>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/章节：**[fig:v11-history](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:243>)；[sup:v11-history](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1612>)；[sup:v10-menu](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1498>)。

**预测登记：**`E1.M1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/6`）；`E1.M2.QR33` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/7`）；`E1.M3.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/8`）。

**既有证据定位：**

- `v11:0`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/0` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/window`。
- `v11:1`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/1` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/horizon`。
- `v11:2`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/2` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/relative_loss_percent`。
- `v11:3`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/3` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/n`。
- `v11:4`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/4` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/window`。
- `v11:5`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/5` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/horizon`。
- `v11:6`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/6` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/relative_loss_percent`。
- `v11:7`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/7` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/n`。
- `v11:8`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/8` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/window`。
- `v11:9`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/9` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/horizon`。
- `v11:10`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/10` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/relative_loss_percent`。
- `v11:11`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/11` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/n`。
- `v11:12`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/12` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/window`。
- `v11:13`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/13` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/horizon`。
- `v11:14`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/14` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/relative_loss_percent`。
- `v11:15`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/15` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/n`。
- `v11:16`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/16` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/window`。
- `v11:17`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/17` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/horizon`。
- `v11:18`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/18` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/relative_loss_percent`。
- `v11:19`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/19` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/n`。
- `v11:20`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/20` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/window`。
- `v11:21`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/21` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/horizon`。
- `v11:22`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/22` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/relative_loss_percent`。
- `v11:23`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/23` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/n`。
- `v11:24`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/24` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/window`。
- `v11:25`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/25` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/horizon`。
- `v11:26`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/26` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/relative_loss_percent`。
- `v11:27`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/27` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/n`。
- `v11:28`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/28` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/window`。
- `v11:29`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/29` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/horizon`。
- `v11:30`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/30` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/relative_loss_percent`。
- `v11:31`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/31` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/n`。
- `v11:32`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/32` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/window`。
- `v11:33`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/33` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/horizon`。
- `v11:34`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/34` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/relative_loss_percent`。
- `v11:35`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/35` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/n`。
- `v11:36`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/36` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/window`。
- `v11:37`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/37` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/horizon`。
- `v11:38`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/38` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/relative_loss_percent`。
- `v11:39`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/39` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/n`。
- `v11:40`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/40` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/successes`。
- `v11:41`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/41` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/denominator`。
- `v11:42`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/42` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/missing`。
- `v11:43`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/43` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/minimum_fraction`。
- `v11:44`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/44` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/status`。
- `v11:45`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/45` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/successes`。
- `v11:46`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/46` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/denominator`。
- `v11:47`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/47` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/missing`。
- `v11:48`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/48` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/minimum_fraction`。
- `v11:49`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/49` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/status`。
- `v11:50`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/50` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/successes`。
- `v11:51`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/51` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/denominator`。
- `v11:52`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/52` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/missing`。
- `v11:53`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/53` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/minimum_fraction`。
- `v11:54`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/54` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/status`。
- `v11:55`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/55` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/window`。
- `v11:56`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/56` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/horizon`。
- `v11:57`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/57` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/relative_loss_percent`。
- `v11:58`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/58` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/window`。
- `v11:59`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/59` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/horizon`。
- `v11:60`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/60` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/relative_loss_percent`。
- `v11:61`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/61` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/window`。
- `v11:62`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/62` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/horizon`。
- `v11:63`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/63` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/relative_loss_percent`。
- `v11:64`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/64` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/window`。
- `v11:65`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/65` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/horizon`。
- `v11:66`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/66` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/relative_loss_percent`。
- `v11:67`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/67` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/window`。
- `v11:68`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/68` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/horizon`。
- `v11:69`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/69` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/relative_loss_percent`。
- `v11:70`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/70` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/18/window`。
- `v11:71`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/71` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/18/horizon`。
- `v11:72`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/72` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/18/relative_loss_percent`。
- `v11:73`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/73` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/19/window`。
- `v11:74`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/74` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/19/horizon`。
- `v11:75`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/75` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/19/relative_loss_percent`。
- `new:20`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/20` → `results/v10/menu/summary.json#/across_sources/0/median_pct`。
- `new:21`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/21` → `results/v10/menu/summary.json#/across_sources/0/original_median_pct`。
- `new:26`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/26` → `results/v10/menu/summary.json#/across_sources/2/status`。
- `new:28`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/28` → `results/v10/menu/summary.json#/across_sources/4/median_pct`。
- `new:29`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/29` → `results/v10/menu/summary.json#/across_sources/4/original_median_pct`。
- `new:34`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/34` → `results/v10/menu/summary.json#/across_sources/6/status`。
- `new:36`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/36` → `results/v10/menu/summary.json#/predictions/M1/status`。
- `new:37`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/37` → `results/v10/menu/summary.json#/predictions/M2/status`。
- `new:38`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/38` → `results/v10/menu/summary.json#/predictions/M3/status`。
- `new:40`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/40` → `results/v10/menu/summary.json#/predictions/M3/joint_improved_sources`。

**证据支持：**现有v11曲线与E1菜单结果保持原值；解释明确限于tested configurations、histories、validation windows和shrinkage menus。

**保留边界：**没有一般sufficient-history条件、全模型结论或因果机制；W260失败汇总和E1未达屏保留。

**原P2处理：**写作范围已限定，实质边界保留；精确编辑 `/changes/16`, `/changes/21`。

### C26｜WP2低区间15/17与29/34，W52/W260已知，仅W520新算；local/public时序

**当前主文位置：**[248](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)。

**当前表/图/命题/章节：**[par:wp2-history](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:247>)；[tab:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:9>)；[sup:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:1>)。

**预测登记：**`WP2.P1_QR4.QR4` → `SUPPORT`（`notes/submission/prediction-register.json#/rows/31`）；`WP2.P1_QR33.QR33` → `SUPPORT`（`notes/submission/prediction-register.json#/rows/32`）。

**既有证据定位：**

- `wp2:0`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/0` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/status`。
- `wp2:1`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/1` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/planned`。
- `wp2:2`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/2` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/successes`。
- `wp2:3`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/3` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/threshold`。
- `wp2:4`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/4` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/status`。
- `wp2:5`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/5` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/planned`。
- `wp2:6`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/6` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/successes`。
- `wp2:7`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/7` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/threshold`。
- `json:notes/submission/prediction-register.json#/timing_by_group/WP2`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/timing_by_group/WP2`。

**证据支持：**保存计数/阈值/判定一致；local设计早13.372451秒，public after-run；H4已在正文就近披露。

**保留边界：**不是external preregistration、prospective确认或全部新金融样本。

### C27｜WP2 P2QR4 10/17、P3 6/17失败，QR33 P2 planned0不可测，总体partial

**当前主文位置：**[248](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:248>)。

**当前表/图/命题/章节：**[tab:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:9>)；[tab:submission-wp2-counterexamples](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:33>)。

**预测登记：**`WP2.P2_QR4.QR4` → `NOT_SUPPORT`（`notes/submission/prediction-register.json#/rows/33`）；`WP2.P2_QR33.QR33` → `NOT_TESTABLE`（`notes/submission/prediction-register.json#/rows/34`）；`WP2.P3_QR4.QR4` → `NOT_SUPPORT`（`notes/submission/prediction-register.json#/rows/35`）。

**既有证据定位：**

- `wp2:0`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/0` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/status`。
- `wp2:1`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/1` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/planned`。
- `wp2:2`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/2` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/successes`。
- `wp2:3`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/3` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/threshold`。
- `wp2:4`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/4` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/status`。
- `wp2:5`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/5` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/planned`。
- `wp2:6`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/6` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/successes`。
- `wp2:7`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/7` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/threshold`。
- `wp2:8`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/8` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/status`。
- `wp2:9`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/9` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/planned`。
- `wp2:10`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/10` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/successes`。
- `wp2:11`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/11` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/threshold`。
- `wp2:12`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/12` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR33/status`。
- `wp2:13`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/13` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR33/planned`。
- `wp2:14`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/14` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/status`。
- `wp2:15`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/15` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/planned`。
- `wp2:16`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/16` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/successes`。
- `wp2:17`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/17` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/threshold`。
- `wp2:18`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/18` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/screen`。
- `wp2:19`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/19` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/code`。
- `wp2:20`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/20` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/relative_loss_percent`。
- `wp2:21`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/21` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/window`。
- `wp2:22`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/22` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/screen`。
- `wp2:23`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/23` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/code`。
- `wp2:24`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/24` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/relative_loss_percent`。
- `wp2:25`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/25` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/window`。
- `wp2:26`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/26` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/screen`。
- `wp2:27`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/27` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/code`。
- `wp2:28`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/28` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/relative_loss_percent`。
- `wp2:29`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/29` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/window`。
- `wp2:30`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/30` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/screen`。
- `wp2:31`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/31` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/code`。
- `wp2:32`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/32` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/relative_loss_percent`。
- `wp2:33`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/33` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/window`。
- `wp2:34`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/34` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/screen`。
- `wp2:35`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/35` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/code`。
- `wp2:36`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/36` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/relative_loss_percent`。
- `wp2:37`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/37` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/window`。
- `wp2:38`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/38` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/screen`。
- `wp2:39`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/39` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/code`。
- `wp2:40`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/40` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/relative_loss_percent`。
- `wp2:41`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/41` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/window`。
- `wp2:42`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/42` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/screen`。
- `wp2:43`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/43` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/code`。
- `wp2:44`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/44` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/relative_loss_percent`。
- `wp2:45`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/45` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/window`。
- `wp2:46`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/46` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/screen`。
- `wp2:47`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/47` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/code`。
- `wp2:48`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/48` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/relative_loss_percent`。
- `wp2:49`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/49` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/window`。
- `wp2:50`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/50` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/screen`。
- `wp2:51`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/51` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/code`。
- `wp2:52`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/52` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/relative_loss_percent`。
- `wp2:53`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/53` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/window`。
- `wp2:54`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/54` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/screen`。
- `wp2:55`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/55` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/code`。
- `wp2:56`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/56` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/relative_loss_percent`。
- `wp2:57`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/57` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/window`。
- `wp2:58`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/58` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/screen`。
- `wp2:59`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/59` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/code`。
- `wp2:60`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/60` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/relative_loss_percent`。
- `wp2:61`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/61` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/window`。
- `wp2:62`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/62` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/screen`。
- `wp2:63`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/63` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/code`。
- `wp2:64`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/64` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/relative_loss_percent`。
- `wp2:65`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/65` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/window`。
- `wp2:66`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/66` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/screen`。
- `wp2:67`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/67` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/code`。
- `wp2:68`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/68` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/relative_loss_percent`。
- `wp2:69`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/69` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/window`。
- `wp2:70`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/70` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/screen`。
- `wp2:71`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/71` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/code`。
- `wp2:72`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/72` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/relative_loss_percent`。
- `wp2:73`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/73` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/window`。
- `wp2:74`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/74` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/screen`。
- `wp2:75`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/75` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/code`。
- `wp2:76`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/76` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/relative_losses`。
- `wp2:77`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/77` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/windows`。
- `wp2:78`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/78` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/screen`。
- `wp2:79`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/79` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/code`。
- `wp2:80`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/80` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/relative_losses`。
- `wp2:81`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/81` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/windows`。
- `wp2:82`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/82` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/screen`。
- `wp2:83`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/83` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/code`。
- `wp2:84`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/84` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/relative_losses`。
- `wp2:85`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/85` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/windows`。
- `wp2:86`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/86` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/screen`。
- `wp2:87`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/87` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/code`。
- `wp2:88`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/88` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/relative_losses`。
- `wp2:89`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/89` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/windows`。
- `wp2:90`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/90` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/screen`。
- `wp2:91`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/91` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/code`。
- `wp2:92`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/92` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/relative_losses`。
- `wp2:93`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/93` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/windows`。
- `wp2:94`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/94` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/screen`。
- `wp2:95`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/95` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/code`。
- `wp2:96`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/96` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/relative_losses`。
- `wp2:97`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/97` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/windows`。
- `wp2:98`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/98` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/screen`。
- `wp2:99`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/99` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/code`。
- `wp2:100`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/100` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/relative_losses`。
- `wp2:101`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/101` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/windows`。
- `wp2:102`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/102` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/screen`。
- `wp2:103`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/103` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/code`。
- `wp2:104`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/104` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/relative_losses`。
- `wp2:105`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/105` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/windows`。
- `wp2:106`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/106` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/screen`。
- `wp2:107`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/107` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/code`。
- `wp2:108`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/108` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/relative_losses`。
- `wp2:109`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/109` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/windows`。
- `wp2:110`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/110` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/screen`。
- `wp2:111`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/111` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/code`。
- `wp2:112`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/112` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/relative_losses`。
- `wp2:113`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/113` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/windows`。
- `wp2:114`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/114` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/screen`。
- `wp2:115`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/115` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/code`。
- `wp2:116`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/116` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/relative_losses`。
- `wp2:117`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/117` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/windows`。
- `json:notes/submission/prediction-register.json#/wp2_group_verdict`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/wp2_group_verdict`。

**证据支持：**正文明确full regression没有prewritten high-region cell，高history screen untestable；原partial、固定分母与全部反例保持。

**保留边界：**QR4P2/P3不成立，QR33P2 planned0不可测；无一般充分历史或因果机制。

**原P2处理：**写作范围已限定，实质边界保留；精确编辑 `/changes/17`。

### C28｜Treasury main +50.79、54vs28/277；earlier short-window +144.30

**当前主文位置：**[254](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:254>)；[266](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:266>)；[267](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:267>)；[275](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:275>)。

**当前表/图/命题/章节：**[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:26`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/26`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `relative_mean_loss_difference_percent`。
- `old:27`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/27`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `strict_breach_count_left`。
- `old:28`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/28`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `strict_breach_count_right`。
- `old:33`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/33`；唯一CSV筛选 `{"id": "Treasury-W52-structural-analogue"}`；字段 `percent_vs_reference`。
- `old:43`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/43`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`；字段 `origin_count`。

**证据支持：**paired CSV与earlier primary-replication保持不同history。

**保留边界：**不同history的adverse result不是同一程序复现。

### C29｜weekly panel由92.63缩至9.22但34/48仍输，QR4与ordinary完整行

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[256](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:256>)；[263](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)；[268](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:268>)；[269](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:269>)；[270](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:270>)；[271](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:271>)。

**当前表/图/命题/章节：**[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)。

**预测登记：**`E5.P1.QR33+` → `False`（`notes/submission/prediction-register.json#/rows/0`）；`E5.P2.QR33+` → `False`（`notes/submission/prediction-register.json#/rows/1`）；`E5.P3.QR33+` → `True`（`notes/submission/prediction-register.json#/rows/2`）。

**既有证据定位：**

- `old:5`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/5` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR33_plus/losing_to_F`。
- `old:6`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/6` → `results/supervisor-20261023/e5/descriptive-summary.json#/planned_cells`。
- `old:29`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/29` → `results/supervisor-20261023/e5/descriptive-summary.json#/original_QR33/median_percent_vs_F`。
- `old:30`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/30` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR33_plus/median_percent_vs_F`。
- `old:34`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/34` → `results/supervisor-20261023/e5/descriptive-summary.json#/original_QR33/losing_to_F`。
- `old:35`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/35` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR4_plus/median_percent_vs_F`。
- `old:36`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/36` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR4_plus/losing_to_F`。
- `old:37`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/37` → `results/supervisor-20261023/e5/descriptive-summary.json#/I/median_percent_vs_F`。
- `old:38`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/38` → `results/supervisor-20261023/e5/descriptive-summary.json#/I/losing_to_F`。

**证据支持：**原summary支持4个panel行及48分母；E5P1/P2失败而P3成立。

**保留边界：**相关聚合任务，不是独立dealer replication；更窄loss不等于全部标准通过。

### C30｜earlier one-SE选I17/26、median5.37vs4.15、worst181.39且R6全失败

**当前主文位置：**[256](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:256>)；[263](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)；[272](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:272>)；[273](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:273>)；[275](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:275>)。

**当前表/图/命题/章节：**[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:263>)；[sup:selection](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:674>)；[sup:selection-failures](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:756>)。

**预测登记：**`R6.S1.R2` → `NOT_MET`（`notes/submission/prediction-register.json#/rows/3`）；`R6.S2.R2` → `NOT_MET`（`notes/submission/prediction-register.json#/rows/4`）；`R6.S3.R2` → `NOT_MET`（`notes/submission/prediction-register.json#/rows/5`）。

**既有证据定位：**

- `old:9`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/9`；唯一CSV筛选 `{"source": "nyfed_weekly", "series_key": "PDPOSGS-B", "horizon": "24", "window": "52", "report": "R2"}`；字段 `percent_vs_F`。
- `old:39`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/39` → `results/supervisor-20261023/r6/assessment.json#/S3/R0_median_percent_vs_F`。
- `old:40`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/40` → `results/supervisor-20261023/r6/assessment.json#/S1/median_percent_vs_F`。
- `old:41`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/41` → `results/supervisor-20261023/r6/assessment.json#/S3/R0_complete_count`。
- `old:42`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/42` → `results/supervisor-20261023/r6/assessment.json#/S3/R2_complete_count`。
- `new:51`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/51`。

**证据支持：**原CSV计数记录17次I；26格完整，三原success屏NOT_MET保持。

**保留边界：**earlier R2 selector不同later RP；ordinary I不等于corrected F。

### C31｜简化conditioning、SAV/固定组合未达uniform weekly improvement

**当前主文位置：**[258](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:258>)。

**当前表/图/命题/章节：**[sup:wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:793>)；[sup:wp2-pairs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:855>)；[sup:wp3](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:899>)；[sup:wp3-murphy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:971>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:31`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/31` → `results/revision-20261023/v6/wp3-findings.json#/primary_context_rows/3/percent_vs_F`。
- `old:32`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/32` → `results/revision-20261023/v6/wp3-findings.json#/primary_context_rows/2/percent_vs_F`。
- `text:submission-final/supplement.tex#section{Untuned forecast combinations}`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:899>)。

**证据支持：**补充完整loss/失败；保存wp3 findings正负例足以否定已测组合uniform改善。

**保留边界：**不概括所有组合或所有conditional models无效。

### C32｜日度历史赢7/8；QR4 W260 H6 -2.97但37/30breaches

**当前主文位置：**[260](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:260>)。

**当前表/图/命题/章节：**[sup:v8-daily](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1328>)；[tab:daily-fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v8-daily-results-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:98`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/98` → `results/revision-v8/wp4/summary.json#/classifications/QR33`。
- `old:99`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/99` → `results/revision-v8/wp4/summary.json#/classifications/QR4`。
- `old:100`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/100` → `results/revision-v8/wp4/summary.json#/contrasts/5/relative_loss_percent`。
- `old:101`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/101` → `results/revision-v8/wp4/summary.json#/cells/8/evaluation/strict_breach_count`。
- `old:102`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/102` → `results/revision-v8/wp4/summary.json#/cells/6/evaluation/strict_breach_count`。
- `old:103`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/103` → `results/revision-v8/wp4/summary.json#/contrasts/5/window`。
- `old:104`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/104` → `results/revision-v8/wp4/summary.json#/contrasts/5/horizon`。
- `old:105`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/105` → `results/revision-v8/wp4/summary.json#/contrasts/5/method`。
- `old:106`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/106` → `results/revision-v8/wp4/summary.json#/contrasts/5/reference_method`。

**证据支持：**两classification各4/4、3/4历史胜，exception方法/history/H/loss/hits完整。

**保留边界：**同FX聚合非外部复制，评分改善伴更多breach。

### C33｜CFTC29/34达60%：两历史report事后较好者，corrected F固定另报

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[280](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:280>)；[282](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:282>)。

**当前表/图/命题/章节：**[tab:v10-cftc-contracts](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-cftc-contracts.tex:4>)；[fig:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:285>)。

**预测登记：**`E2.T1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/9`）。

**既有证据定位：**

- `new:12`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/12` → `results/v10/cftc/summary.json#/predictions/T1/simple_better_cells`。
- `new:13`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/13` → `results/v10/cftc/summary.json#/predictions/T1/required_cells`。
- `new:14`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/14` → `results/v10/cftc/summary.json#/predictions/T1/minimum_inclusive_fraction`。
- `json:results/v10/cftc/summary.json#/contracts`：[results/v10/cftc/summary.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/summary.json>)，`#/contracts`。

**证据支持：**摘要与正文均明确better realized historical score的29/34；原E2.T1判定与固定corrected F逐表报告保持。

**保留边界：**两历史report事后较好者不是可执行selector，不能把该计数称作单一实时规则胜率。

**原P2处理：**写作范围已限定，实质边界保留；精确编辑 `/changes/1`。

### C34｜CFTC full两history median未达10%容忍，QR4长history更近历史

**当前主文位置：**[280](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:280>)；[285](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:285>)。

**当前表/图/命题/章节：**[tab:v10-cftc-contracts](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-cftc-contracts.tex:4>)；[fig:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:285>)。

**预测登记：**`E2.T2.QR33` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/10`）；`E2.T3.QR4` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/11`）。

**既有证据定位：**

- `new:15`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/15` → `results/v10/cftc/summary.json#/predictions/T2/median_pct_by_window/52`。
- `new:16`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/16` → `results/v10/cftc/summary.json#/predictions/T2/median_pct_by_window/260`。
- `new:17`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/17` → `results/v10/cftc/summary.json#/predictions/T2/status`。
- `new:18`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/18` → `results/v10/cftc/summary.json#/predictions/T3/W52_median_pct`。
- `new:19`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/19` → `results/v10/cftc/summary.json#/predictions/T3/W260_median_pct`。
- `json:results/v10/cftc/summary.json#/contracts`：[results/v10/cftc/summary.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/summary.json>)，`#/contracts`。

**证据支持：**full19.3347/10.3483→T2不成立；QR4 10.2807/.21749→T3成立。

**保留边界：**normalized percentages不恢复common-dollar portfolio风险，也非全部history单调收益。

### C35｜41短history weekly中27格selection过半、29格finite hindsight gap正

**当前主文位置：**[295](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:295>)；[300](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:300>)。

**当前表/图/命题/章节：**[fig:v12-decomposition](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:301>)。

**预测登记：**`F1.D1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/12`）；`F1.D2.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/13`）。

**既有证据定位：**

- `v13:238`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/238` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/status`。
- `v13:239`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/239` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/planned_n`。
- `v13:240`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/240` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/complete_n`。
- `v13:241`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/241` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/support_n`。
- `v13:242`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/242` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/nonsupport_n`。
- `v13:243`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/243` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/unavailable_n`。
- `v13:244`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/244` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/status`。
- `v13:245`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/245` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/planned_n`。
- `v13:246`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/246` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/complete_n`。
- `v13:247`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/247` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/support_n`。
- `v13:248`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/248` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/nonsupport_n`。
- `v13:249`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/249` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/unavailable_n`。

**证据支持：**标题改finite-menu decomposition；27/41与29/41原值保留，正文明确gap描述tested finite procedures且不证明conditional information absent。

**保留边界：**事后有限菜单诊断不识别信息不存在、特征因果作用或全模型下界。

**原P2处理：**写作范围已限定，实质边界保留；精确编辑 `/changes/18`, `/changes/19`, `/changes/21`。

### C36｜decomposition5有限候选排除infinite，中位数不可加，2FXgap负

**当前主文位置：**[297](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:297>)；[301](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:301>)。

**当前表/图/命题/章节：**[fig:v12-decomposition](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:301>)；[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)。

**预测登记：**`F1.D3.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/14`）。

**既有证据定位：**

- `v12:4`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/4` → `results/v12/decomposition/short-weekly-summary.json#/methods/QR33/median_actual_excess_pct`。
- `v12:5`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/5` → `results/v12/decomposition/short-weekly-summary.json#/methods/QR33/median_selection_component_pct`。
- `v12:6`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/6` → `results/v12/decomposition/short-weekly-summary.json#/methods/QR33/median_signal_gap_pct`。
- `v12:8`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/8` → `results/v12/decomposition/predictions.json#/D3/horizons/6/signal_gap_pct`。
- `v12:9`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/9` → `results/v12/decomposition/predictions.json#/D3/horizons/24/signal_gap_pct`。
- `v12:30`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/30`。

**证据支持：**19.4353/18.3175/4.37085及2FXnegative gap字段可读；图保留unavailable cross。

**保留边界：**非deployable selector/全模型下界/因果mechanism；component median不加总。

### C37｜CFTC长validation median19.33→4.03、10.35→.53，infinite增加

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)；[295](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:295>)；[306](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:306>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/章节：**[tab:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-validation-main.tex:2>)；[fig:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:34>)。

**预测登记：**`F2.V1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/18`）；`F2.V2.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/19`）；`F2.V1.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/20`）；`F2.V2.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/21`）。

**既有证据定位：**

- `v13:218`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/218` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/eligible_contracts`。
- `v13:219`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/219` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/complete_pair_count`。
- `v13:220`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/220` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/median_difference_pct_points`。
- `v13:221`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/221` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/V1`。
- `v13:222`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/222` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/V2`。
- `v13:223`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/223` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/median_relative_loss_by_validation/52`。
- `v13:224`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/224` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/known_infinity_count_by_validation/52`。
- `v13:225`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/225` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/median_relative_loss_by_validation/156`。
- `v13:226`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/226` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/known_infinity_count_by_validation/156`。
- `v13:227`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/227` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/descriptive_complete_pairs/median_paired_change_pct_points`。
- `v13:228`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/228` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/eligible_contracts`。
- `v13:229`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/229` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/complete_pair_count`。
- `v13:230`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/230` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/median_difference_pct_points`。
- `v13:231`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/231` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/V1`。
- `v13:232`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/232` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/V2`。
- `v13:233`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/233` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/median_relative_loss_by_validation/52`。
- `v13:234`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/234` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/known_infinity_count_by_validation/52`。
- `v13:235`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/235` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/median_relative_loss_by_validation/156`。
- `v13:236`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/236` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/known_infinity_count_by_validation/156`。
- `v13:237`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/237` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/descriptive_complete_pairs/median_paired_change_pct_points`。

**证据支持：**full W两臂threshold通过；QR4原4失败使2判定undetermined，保留。

**保留边界：**arm median差不等于paired median；仍post-result。

### C38｜NY full长validation median6.68→-1.13、40.47→5.02，infinite增加

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)；[295](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:295>)；[304](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:304>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/章节：**[tab:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-validation-main.tex:2>)；[fig:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:34>)。

**预测登记：**`G2.V3.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/24`）；`G2.V4.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/25`）。

**既有证据定位：**

- `v13:174`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/174` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/planned_sources`。
- `v13:175`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/175` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/complete_pair_count`。
- `v13:176`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/176` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/median_difference_pct_points`。
- `v13:177`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/177` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/V3`。
- `v13:178`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/178` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/V4`。
- `v13:179`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/179` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/median_relative_loss_by_validation/52`。
- `v13:180`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/180` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/infinity_count_by_validation/52`。
- `v13:181`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/181` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/median_relative_loss_by_validation/156`。
- `v13:182`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/182` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/infinity_count_by_validation/156`。
- `v13:183`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/183` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/descriptive_complete_pairs/median_paired_change_pct_points`。
- `v13:184`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/184` → `results/v13/nyfed-validation/summary.json#/methods/QR33/V3`。
- `v13:185`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/185` → `results/v13/nyfed-validation/summary.json#/methods/QR33/V4`。
- `v13:186`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/186` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/planned_sources`。
- `v13:187`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/187` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/complete_pair_count`。
- `v13:188`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/188` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/median_difference_pct_points`。
- `v13:189`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/189` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/V3`。
- `v13:190`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/190` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/V4`。
- `v13:191`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/191` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/median_relative_loss_by_validation/52`。
- `v13:192`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/192` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/infinity_count_by_validation/52`。
- `v13:193`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/193` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/median_relative_loss_by_validation/156`。
- `v13:194`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/194` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/infinity_count_by_validation/156`。
- `v13:195`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/195` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/descriptive_complete_pairs/median_paired_change_pct_points`。

**证据支持：**摘要/intro/综述/结论统一full regression，并在结果正文明确four-feature H6 median-improvement screen fails。

**保留边界：**原QR4失败和CFTC不可用状态保留；H6端点/refit混杂及arm/paired median差异未消除。

**原P2处理：**写作范围已限定，实质边界保留；精确编辑 `/changes/2`, `/changes/4`, `/changes/5`, `/changes/8`, `/changes/20`, `/changes/22`。

### C39｜NYH6端点混杂/paired median0、QR4一屏失败及CFTC QR4缺失

**当前主文位置：**[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[306](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:306>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/章节：**[tab:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-validation-main.tex:2>)；[fig:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:34>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`G2.V3.QR4` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/26`）；`G2.V4.QR4` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/27`）；`F2.V1.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/20`）；`F2.V2.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/21`）。

**既有证据定位：**

- `v13:183`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/183` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/descriptive_complete_pairs/median_paired_change_pct_points`。
- `v13:196`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/196` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/planned_sources`。
- `v13:197`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/197` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/complete_pair_count`。
- `v13:198`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/198` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/median_difference_pct_points`。
- `v13:199`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/199` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/V3`。
- `v13:200`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/200` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/V4`。
- `v13:201`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/201` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/median_relative_loss_by_validation/52`。
- `v13:202`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/202` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/infinity_count_by_validation/52`。
- `v13:203`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/203` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/median_relative_loss_by_validation/156`。
- `v13:204`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/204` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/infinity_count_by_validation/156`。
- `v13:205`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/205` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/descriptive_complete_pairs/median_paired_change_pct_points`。
- `v13:206`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/206` → `results/v13/nyfed-validation/summary.json#/methods/QR4/V3`。
- `v13:207`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/207` → `results/v13/nyfed-validation/summary.json#/methods/QR4/V4`。
- `v13:208`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/208` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/planned_sources`。
- `v13:209`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/209` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/complete_pair_count`。
- `v13:210`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/210` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/median_difference_pct_points`。
- `v13:211`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/211` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/V3`。
- `v13:212`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/212` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/V4`。
- `v13:213`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/213` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/median_relative_loss_by_validation/52`。
- `v13:214`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/214` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/infinity_count_by_validation/52`。
- `v13:215`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/215` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/median_relative_loss_by_validation/156`。
- `v13:216`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/216` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/infinity_count_by_validation/156`。
- `v13:217`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/217` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/descriptive_complete_pairs/median_paired_change_pct_points`。
- `text:submission-final/generated/v13-supplement.tex#The original validation origins`：[submission-final/generated/v13-supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:30>)。

**证据支持：**paired median0；QR4H6 -4.21504pp未达-5；S38明确前移18周。

**保留边界：**lower arm median非典型paired改善；length-only机制未识别。

### C40｜tau表所有完整值/NA，CFTC28胜1未知、两FX原比较无法判定

**当前主文位置：**[310](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:310>)；[313](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:313>)；[316](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:316>)；[317](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:317>)；[318](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:318>)；[319](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:319>)；[320](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:320>)；[323](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:323>)。

**当前表/图/命题/章节：**[tab:v12-tau](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:313>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`F3.Q1.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/22`）；`F3.Q2.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/23`）。

**既有证据定位：**

- `v12:25`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/25` → `results/v12/tau/predictions.json#/Q2/denominator`。
- `v12:26`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/26` → `results/v12/tau/predictions.json#/Q1/support_count`。
- `v12:27`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/27` → `results/v12/tau/predictions.json#/Q1/denominator`。
- `v12:28`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/28` → `results/v12/tau/predictions.json#/Q1/unknown_count`。
- `v12:29`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/29` → `results/v12/tau/predictions.json#/Q1/minimum_support`。
- `v12:32`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/32` → `results/v12/tau/predictions.json#/descriptive_groups/5/descriptive_complete_row_median_relative_loss_pct`。
- `v12:33`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/33` → `results/v12/tau/predictions.json#/descriptive_groups/0/descriptive_complete_row_median_relative_loss_pct`。
- `v12:35`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/35` → `results/v12/tau/predictions.json#/descriptive_groups/6/descriptive_complete_row_median_relative_loss_pct`。
- `v12:36`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/36` → `results/v12/tau/predictions.json#/descriptive_groups/1/counts`。
- `v12:37`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/37` → `results/v12/tau/predictions.json#/descriptive_groups/7/descriptive_complete_row_median_relative_loss_pct`。
- `v12:38`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/38` → `results/v12/tau/predictions.json#/descriptive_groups/2/counts`。
- `v12:39`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/39` → `results/v12/tau/predictions.json#/descriptive_groups/8/descriptive_complete_row_median_relative_loss_pct`。
- `v12:40`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/40` → `results/v12/tau/predictions.json#/descriptive_groups/3/counts`。
- `v12:41`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/41` → `results/v12/tau/predictions.json#/descriptive_groups/9/descriptive_complete_row_median_relative_loss_pct`。
- `v12:42`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/42` → `results/v12/tau/predictions.json#/descriptive_groups/4/descriptive_complete_row_median_relative_loss_pct`。
- `v12:45`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/45` → `results/v12/tau/predictions.json#/Q1/status`。
- `v12:46`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/46` → `results/v12/tau/predictions.json#/Q2/status`。

**证据支持：**完整组median或counts→NA；无successful-subset补值。H4已明确required numerical fits。

**保留边界：**数值程序失败不等于观察经济损失/模型经济失败。

### C41｜G1保真6/10 gate失败，三原失败不替换、Q1/Q2仍未决

**当前主文位置：**[310](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:310>)；[324](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:324>)；[384](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:384>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/章节：**[tab:v12-tau](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:313>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`F3.Q1.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/22`）；`F3.Q2.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/23`）。

**既有证据定位：**

- `v13:0`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/0` → `results/v13/tau-repair/consistency.json#/status`。
- `v13:1`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/1` → `results/v13/tau-repair/consistency.json#/n`。
- `v13:2`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/2` → `results/v13/tau-repair/consistency.json#/passed`。
- `v13:53`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/53` → `results/v13/tau-repair/summary.json#/consistency_gate`。
- `v13:54`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/54` → `results/v13/tau-repair/summary.json#/original_Q1`。
- `v13:55`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/55` → `results/v13/tau-repair/summary.json#/original_Q2`。
- `v13:60`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/60` → `results/v13/tau-repair/summary.json#/repairs/0/cell_id`。
- `v13:61`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/61` → `results/v13/tau-repair/summary.json#/repairs/0/status`。
- `v13:62`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/62` → `results/v13/tau-repair/summary.json#/repairs/0/reason`。
- `v13:63`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/63` → `results/v13/tau-repair/summary.json#/repairs/1/cell_id`。
- `v13:64`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/64` → `results/v13/tau-repair/summary.json#/repairs/1/status`。
- `v13:65`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/65` → `results/v13/tau-repair/summary.json#/repairs/1/reason`。
- `v13:66`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/66` → `results/v13/tau-repair/summary.json#/repairs/2/cell_id`。
- `v13:67`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/67` → `results/v13/tau-repair/summary.json#/repairs/2/status`。
- `v13:68`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/68` → `results/v13/tau-repair/summary.json#/repairs/2/reason`。
- `v13:586`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/586` → `protocol/v13/tau-solver-repair-design.md#/consistency_max_pointwise_relative_error`。

**证据支持：**G1 gate FAIL使3failed格NOT_RUN_CONSISTENCY_GATE，非3次新复估。

**保留边界：**6/10是兼容保真检查，不是经济成功率；原NA保留。

### C42｜score≠breach；elementary curves crossing与H24约20.6:1 reversal

**当前主文位置：**[330](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:330>)；[370](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:370>)；[396](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:396>)。

**当前表/图/命题/章节：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:225>)；[sup:preference](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:465>)；[sup:wp3-murphy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:971>)；[sup:v10-diagnostics](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1579>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:212`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/212` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/2/equality_alpha`。
- `old:213`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/213` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/2/horizon`。
- `old:214`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/214` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/2/right_method`。
- `old:215`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/215` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/0/relation`。
- `old:216`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/216` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/1/relation`。
- `json:results/revision-20261022/preference-robustness/results.json#/headline_comparisons`：[results/revision-20261022/preference-robustness/results.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/revision-20261022/preference-robustness/results.json>)，`#/headline_comparisons`。

**原文献：**[gw2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:447>)；[ehm2016](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:441>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**原精确fraction及horizon24字段可读，两个H6 left_dominates支持两个误差项降低。

**保留边界：**20.6:1属于独立H24 reference，不属于H6 matched gain。

### C43｜成本J的reserve/breach/exceedance与mF归一化；illustrative非实测

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[48](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:48>)；[337](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:337>)；[338](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:338>)；[339](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:339>)；[340](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:340>)；[345](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:345>)；[382](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:382>)；[396](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:396>)。

**当前表/图/命题/章节：**[fig:v10-cost](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:348>)；[sup:v10-cost](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1554>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `new:61`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/61` → `results/v10/cost/manifest.json#/design/grid`。
- `text:submission-final/supplement.tex#The normalization uses evaluation-sample F headroom`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1641>)。

**证据支持：**正文式和S32/S36明示固定偏好与evaluation-sample归一化。

**保留边界：**非事前institutional charges、真实profit或限额干预反事实。

### C44｜CFTC c1网格center5/34、两指定角32/34和1/34，趋势非处处单调

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[48](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:48>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)；[343](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:343>)；[344](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:344>)；[348](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:348>)；[396](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:396>)。

**当前表/图/命题/章节：**[fig:v10-cost](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:348>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `json:results/v10/cost/group-regions.json#/1016`：[results/v10/cost/group-regions.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/group-regions.json>)，`#/1016`。
- `json:results/v10/cost/group-regions.json#/1039`：[results/v10/cost/group-regions.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/group-regions.json>)，`#/1039`。
- `json:results/v10/cost/group-regions.json#/1062`：[results/v10/cost/group-regions.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/group-regions.json>)，`#/1062`。
- `json:results/v10/cost/summary.json#/unavailable`：[results/v10/cost/summary.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/summary.json>)，`#/unavailable`。

**证据支持：**精确rows1016(.01,5)wins1，1039(.1,.25)wins5，1062(1,0)wins32；planned34且lower=upper。

**保留边界：**描述性related-task比例而非独立成功率；固定c网格，有局部非单调。

### C45｜RP六点菜单、156周/5760FX验证、pairedHAC1SE和corrected F默认

**当前主文位置：**[356](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:356>)。

**当前表/图/命题/章节：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)；[fig:v13-rp](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:360>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/generated/v13-supplement.tex#Selection and the gate share`：[submission-final/generated/v13-supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:39>)。
- `v13:588`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/588` → `protocol/v13/recommended-protocol-design.md#/predictions/R1/support_median_rp_relative_excess_pct_lte`。
- `v13:589`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/589` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/adverse_if_rp_relative_excess_pct_gt`。
- `v13:590`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/590` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/support_fraction_lte`。
- `v13:591`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/591` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/integer_threshold_if60`。

**原文献：**[nw1987](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:478>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**S38给validation长度、候选选取与gate共用数据、decision评估段固定；G5保留design阈值。

**保留边界：**1SE启发式，非名义显著性或benchmark保护概率。

### C46｜RP完整60weekly+2FX、median0vs14.63、fallback32、8不利/80.98最坏、FX保留

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)；[356](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:356>)；[359](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:359>)；[360](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:360>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/章节：**[fig:v13-rp](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:360>)；[tab:v13-routing](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:44>)。

**预测登记：**`G3.R1.RP` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/28`）；`G3.R2.RP` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/29`）；`G3.R3.RP` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/30`）。

**既有证据定位：**

- `v13:255`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/255` → `results/v13/recommended-protocol/summary.json#/R1`。
- `v13:256`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/256` → `results/v13/recommended-protocol/summary.json#/R2`。
- `v13:257`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/257` → `results/v13/recommended-protocol/summary.json#/R3`。
- `v13:258`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/258` → `results/v13/recommended-protocol/summary.json#/planned_geometry_cells`。
- `v13:259`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/259` → `results/v13/recommended-protocol/summary.json#/received_rows`。
- `v13:260`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/260` → `results/v13/recommended-protocol/summary.json#/weekly/planned`。
- `v13:261`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/261` → `results/v13/recommended-protocol/summary.json#/weekly/eligible`。
- `v13:262`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/262` → `results/v13/recommended-protocol/summary.json#/weekly/excluded`。
- `v13:263`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/263` → `results/v13/recommended-protocol/summary.json#/weekly/complete`。
- `v13:264`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/264` → `results/v13/recommended-protocol/summary.json#/weekly/unavailable`。
- `v13:265`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/265` → `results/v13/recommended-protocol/summary.json#/weekly/median_relative_loss_pct`。
- `v13:266`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/266` → `results/v13/recommended-protocol/summary.json#/weekly/descriptive_complete_median_relative_loss_pct`。
- `v13:267`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/267` → `results/v13/recommended-protocol/summary.json#/weekly/worst_relative_loss_pct`。
- `v13:268`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/268` → `results/v13/recommended-protocol/summary.json#/weekly/ordinary_complete`。
- `v13:269`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/269` → `results/v13/recommended-protocol/summary.json#/weekly/ordinary_median_relative_loss_pct`。
- `v13:270`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/270` → `results/v13/recommended-protocol/summary.json#/weekly/ordinary_descriptive_complete_median_relative_loss_pct`。
- `v13:271`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/271` → `results/v13/recommended-protocol/summary.json#/weekly/adverse_gt10_count`。
- `v13:272`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/272` → `results/v13/recommended-protocol/summary.json#/weekly/fallback_count`。
- `v13:273`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/273` → `results/v13/recommended-protocol/summary.json#/weekly/regression_count`。
- `v13:274`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/274` → `results/v13/recommended-protocol/summary.json#/weekly/unknown_route_count`。
- `v13:275`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/275` → `results/v13/recommended-protocol/summary.json#/weekly/fallback_fraction_of_planned`。
- `v13:276`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/276` → `results/v13/recommended-protocol/summary.json#/weekly/fallback_fraction_of_complete`。
- `v13:588`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/588` → `protocol/v13/recommended-protocol-design.md#/predictions/R1/support_median_rp_relative_excess_pct_lte`。
- `v13:589`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/589` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/adverse_if_rp_relative_excess_pct_gt`。
- `v13:590`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/590` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/support_fraction_lte`。
- `v13:591`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/591` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/integer_threshold_if60`。

**证据支持：**60complete、32fallback、0median、14.6275ordinary、8adverse和80.98397worst；R1/R3通过，R2失败。

**保留边界：**零median反映多数保留F，不是tail protection。

### C47｜benchmark-default中性标题；实务历史默认建议保留保护失败

**当前主文位置：**[355](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:355>)；[368](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:368>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/章节：**[fig:v13-rp](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:360>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`G3.R2.RP` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/29`）。

**既有证据定位：**

- `v13:256`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/256` → `results/v13/recommended-protocol/summary.json#/R2`。
- `v13:267`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/267` → `results/v13/recommended-protocol/summary.json#/weekly/worst_relative_loss_pct`。
- `v13:271`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/271` → `results/v13/recommended-protocol/summary.json#/weekly/adverse_gt10_count`。
- `v13:589`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/589` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/adverse_if_rp_relative_excess_pct_gt`。
- `v13:590`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/590` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/support_fraction_lte`。
- `v13:591`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/591` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/integer_threshold_if60`。

**证据支持：**H4已将protected标题改default；正文保护不足及结论tail失败一致。

**保留边界：**不因改名消除8/60和worst80.98；不能宣称达到原tail目标。

### C48｜earlier weekly ordinary quantile最差比corrected F高36.5%

**当前主文位置：**[368](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:368>)。

**当前表/图/命题/章节：**[sup:rank](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)；[sup:selection](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:674>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `old:44`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/44`；唯一CSV筛选 `{"phase": "retro", "source": "nyfed_weekly", "series_key": "PDPOSGSC-L2", "horizon": "24", "window": "52", "report": "I"}`；字段 `percent_vs_F`。

**证据支持：**唯一CSV source/series/H/window/reportI字段36.508937。

**保留边界：**特定earlier grid最差，不概括所有ordinary quantile都不可靠。

### C49｜观测被动路径，无causal/feature效果、prospective/individual-dealer复制或实测收益

**当前主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)；[378](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:378>)；[379](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:379>)；[381](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:381>)；[382](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:382>)；[383](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:383>)；[396](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:396>)。

**当前表/图/命题/章节：**[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)；[sup:reproduction](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1583>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#The design gives no causal interpretation`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1633>)。
- `text:submission-final/supplement.tex#Individual-dealer external validation`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1608>)。

**证据支持：**设计范围、retrospective/vintage与未测成本支持这些未建立的边界。

**保留边界：**不是成功预测行；同执行者Git replay不替代独立外部验证。 当前新增限定：净头寸峰值不识别gross portfolios、hedging arrangements或economic capital requirements；没有新增这些对象的数据或模型。

### C50｜原FX研究signed next-hour interval与本稿完整未来path peak响应不同

**当前主文位置：**[56](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:56>)；[68](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:68>)；[71](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:71>)。

**当前表/图/命题/章节：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:68>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**


**原文献：**[wisniewski2020](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:484>)；[wisniewski2024](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:486>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**以当前PMLR论文/博士论文原引用定位；响应差异是当前定义。

**保留边界：**本轮未重新读全文；原文献不证明本稿性能更好。

### C51｜MaxVaR、payment deficit、settlement与dealer capacity/PnL文献定位

**当前主文位置：**[59](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:59>)；[72](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:72>)；[73](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:73>)。

**当前表/图/命题/章节：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:68>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**


**原文献：**[boudoukh2004](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:431>)；[hoogen2017](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:482>)；[petrunia2019](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:480>)；[arjani2020](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:419>)；[duffie2023](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:439>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**每类目标/数据/评价指向对应原引用和当前literature表。

**保留边界：**仅建立引用—主张路由，不伪称本轮阅读全文或完整方法等同。

### C52｜quantile/CAViaR/forest与proper/elementary scores是既有方法

**当前主文位置：**[50](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:50>)；[62](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:62>)。

**当前表/图/命题/章节：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:68>)；[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**


**原文献：**[koenker1978](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:468>)；[engle2004](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:443>)；[meinshausen2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:476>)；[gneiting2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:451>)；[ehm2016](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:441>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**方法/评价概念以原引用与正文式为依据，无新经验预测。

**保留边界：**不宣称新模型族或评价量发明。

### C53｜standard forecast tests、inventory-sensitive quoting动机与RQ框架

**当前主文位置：**[34](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:34>)；[36](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:36>)；[38](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:38>)；[40](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:40>)；[42](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:42>)；[50](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:50>)；[74](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:74>)；[78](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:78>)。

**当前表/图/命题/章节：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:68>)；[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:167>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**


**原文献：**[dm1995](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:437>)；[gw2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:447>)；[mcs2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:455>)；[avellaneda2008](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:421>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**RQ是待回答问题；三finding实证由C22–C48分别映射，库存报价引用只作动机。

**保留边界：**报价文献不证明本稿限额干预提高trading profit。

### C54｜FX源版权/获取/fingerprint，raw和private per-origin不分发

**当前主文位置：**[401](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:401>)。

**当前表/图/命题/章节：**定义/可用性直接指下面来源。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `text:notes/submission/availability-audit.md#- FX：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:5>)。
- `text:REPRODUCING.md#FX`：[REPRODUCING.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/REPRODUCING.md:35>)。

**原文献：**[dataset](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:472>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**H3档案区分可下载与再分发许可；保留rights holders条件和排除范围。

**保留边界：**权限待作者确认；公开代码不意味着无授权输入者能完整独立复算。

### C55｜NY Fed源条款/Treasury snapshot，original panel不分发/新vintage不保原字节

**当前主文位置：**[403](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:403>)。

**当前表/图/命题/章节：**定义/可用性直接指下面来源。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `text:notes/submission/availability-audit.md#- New York Fed：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:6>)。

**原文献：**[nyfeddata](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:445>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**H3明确当前保存/缺失输入与source conditions，不沿用旧文暗示项目已有code license。

**保留边界：**软件可用性不替代源数据条款。

### C56｜CFTC TFF已有公开原文件与URL/time/bytes/SHA回执

**当前主文位置：**[405](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:405>)。

**当前表/图/命题/章节：**定义/可用性直接指下面来源。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `json:data/cftc-tff/provenance.json#`：[data/cftc-tff/provenance.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/data/cftc-tff/provenance.json>)，`#`。
- `text:notes/submission/availability-audit.md#- CFTC：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:7>)。

**原文献：**[cftcTFF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:435>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**直接读现存provenance节点，未新下载或验证远端。

**保留边界：**可检查原记录与独立重估全论文是不同状态。

### C57｜代码/协议/汇总与复现说明入口；fullreplay需原inputs和Git objects

**当前主文位置：**[407](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:407>)。

**当前表/图/命题/章节：**[sup:reproduction](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1583>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**既有证据定位：**

- `text:notes/submission/availability-audit.md#- 代码：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:8>)。
- `text:notes/submission/availability-audit.md#- LICENSE：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:10>)。
- `text:submission-final/supplement.tex#Full financial replay requires compatible inputs`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1595>)。

**证据支持：**H3区分公开可检查与有输入者replay；DOI/license仍占位。

**保留边界：**未核对当前远端字节；同执行者新clone不等于外部独立dealer/researcher replication。

### C58｜state/target/backcast/S36/S40完整判定及失败入口

**当前主文位置：**[115](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:115>)；[222](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:222>)；[386](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:386>)。

**当前表/图/命题/章节：**[sup:wp4](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1017>)；[sup:wp5](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1078>)；[sup:v8-backcast](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1356>)；[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**既有证据定位：**

- `text:submission-final/supplement.tex#The full-prefix backcast uses penalties`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1627>)。
- `json:notes/submission/prediction-register.json#/adverse_context_records`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/adverse_context_records`。

**证据支持：**保存state/target/overlapping backcast完整入口；S40 consolidated register接全部36行及7个额外敏感性。

**保留边界：**登记/链接不是额外实验或全部主张supported；S40最终表号另按编译aux核对。

### C59｜近期ASMBI语境：Sequential monitoring for conditional quantiles of general conditional heteroscedastic time series models

**当前主文位置：**[65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)。

**当前表/图/命题/章节：**[sec:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:54>)。

**预测登记：**不适用。文献语境陈述不属于本稿经验预测登记；依据已核实的出版社元数据/摘要记录。

**新增文献语境：**\citet{LeeKim2024ASMBI} develop sequential monitoring procedures for changes in conditional quantiles of heteroscedastic time series, with applications to financial return data.

**既有证据定位：**

- `asmbi-context:LeeKim2024ASMBI`：[notes/submission/asmbi-recent-literature.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/asmbi-recent-literature.json>)，`#/records/0`；[出版社论文页](https://onlinelibrary.wiley.com/doi/abs/10.1002/asmb.2865)；DOI `10.1002/asmb.2865`。

**原文献：**[LeeKim2024ASMBI](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:487>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**在线顺序监测位置–尺度异方差时序的条件分位数变点，摘要明确联系 VaR/ES 风险管理；用 KOSPI 与 EuroStoxx 50 日收益实证。

**保留边界：**这是变点监测研究；摘要不能支持本稿模型优于其方法，或本稿静态评价量具有新颖性的结论。 只依官网摘要，不声称阅读全文、全面方法优越性或本稿极端分位问题已解决。

### C60｜近期ASMBI语境：Optimal Transport Autoregression to Forecast High-Frequency Financial Data Distributions

**当前主文位置：**[65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)。

**当前表/图/命题/章节：**[sec:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:54>)。

**预测登记：**不适用。文献语境陈述不属于本稿经验预测登记；依据已核实的出版社元数据/摘要记录。

**新增文献语境：**\citet{Pagnottoni2026ASMBI} study distributional forecasts of high-frequency Bitcoin returns and volatility, reporting forecast errors that vary across time and quantile levels.

**既有证据定位：**

- `asmbi-context:Pagnottoni2026ASMBI`：[notes/submission/asmbi-recent-literature.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/asmbi-recent-literature.json>)，`#/records/1`；[出版社论文页](https://onlinelibrary.wiley.com/doi/10.1002/asmb.70067)；DOI `10.1002/asmb.70067`。

**原文献：**[Pagnottoni2026ASMBI](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:489>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**用最优传输自回归预测 Bitcoin 高频收益与波动分布；摘要报告误差依赖时间与分位数，极端分位附近误差上升且不单调。

**保留边界：**摘要针对其最优传输模型和 Bitcoin 数据；不能外推为所有金融模型的普遍定理，也不能据此声称本稿已解决极端分位问题。 只依官网摘要，不声称阅读全文、全面方法优越性或本稿极端分位问题已解决。

### C61｜近期ASMBI语境：Forecasting Gold Returns Volatility Over 1258–2023: The Role of Moments

**当前主文位置：**[65](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:65>)。

**当前表/图/命题/章节：**[sec:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:54>)。

**预测登记：**不适用。文献语境陈述不属于本稿经验预测登记；依据已核实的出版社元数据/摘要记录。

**新增文献语境：**\citet{MuddanaEtAl2025ASMBI} use quantile-regression-derived measures of tail risk and higher moments in recursive out-of-sample forecasts of gold-return volatility.

**既有证据定位：**

- `asmbi-context:MuddanaEtAl2025ASMBI`：[notes/submission/asmbi-recent-literature.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/asmbi-recent-literature.json>)，`#/records/2`；[出版社论文页](https://onlinelibrary.wiley.com/doi/10.1002/asmb.70042)；DOI `10.1002/asmb.70042`。

**原文献：**[MuddanaEtAl2025ASMBI](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:491>)。旧引用只刷新位置；三篇新引用依据已保存官方元数据/摘要，不声称重读全文。

**证据支持：**先用 Bayesian 时变参数分位回归构建波动、尾风险和矩指标，再作递归样本外线性预测并比较自回归基准。

**保留边界：**研究目标是波动预测，不能将其等同于本稿的分位损失目标或宣称摘要证明某种分位评价标准有效。 只依官网摘要，不声称阅读全文、全面方法优越性或本稿极端分位问题已解决。

## 验证范围

- 原58组全部定位；新增3组官方摘要支持的语境；当前叙述遗漏候选0。
- 原501个H4证据节点继承，不重读/重验整套旧数值；3个新增文献记录只读本地已核实档案。
- 主文、补充和展示label按当前文本刷新；预测登记原阈值/数值/判定不修改。
- 新净头寸限制映射至C01/C10/C49：gross portfolios、hedging、economic capital未识别。
- 不把写作修正当作新增外部验证、因果识别、首发时点重建、真实成本测量或数据授权。
- H8若只格式转换，仍须单独证明格式产物与此主文内容一致并完成最终PDF验收。
