# H4 当前主文主张—证据映射

UTC：2026-10-27T04:46:38.181675+00:00；主文 SHA-256：`ffa32c810cb296ea7e21240f75e235e7366374781c96ff177ba33c66fb9b75f6`。

本档案以58个实质主张组覆盖当前摘要、引言三条 findings、方法、结果、实务、局限、结论及数据/代码可用性。同一主张在多处出现时共享证据，但保留每个位置。

只读已有文本和来源，只新建这两份claim-map；没有修改canonical、结果、协议、研究代码或投稿包，没有运行拟合/评分/金融统计、调用Claude或外部模型、提交Git或另派代理。

数值可读回不等于解释自动成立。方法、命题和文献陈述不强配经验预测行，而指原命题、原引用或执行协议。本轮不是独立金融复算、全文文献复核、外部审稿或PDF/远端验收。

## H4 当场已解决的三项准确性问题

- **H4-R1 / 原P1 / 已解决**：benchmark-protected标题过强。当前标题改benchmark-default；G3.R2失败结果保留。 当前定位：[manuscript:353](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:353>)。
- **H4-R2 / 原P1 / 已解决**：WP2 precommitted/registered可能误读公开预注册。当前正文明确local before/public afterward，并用prewritten screens；非外部预注册。 当前定位：[manuscript:246](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:246>)。
- **H4-R3 / 原P1 / 已解决**：Both FX periods fail混淆数值和经济失败。当前明确required numerical fits，G1保真6/10与未运行三格及undetermined判断保留。 当前定位：[manuscript:308](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:308>)。

以上只记录当前H4文本已解决；历史H5草案仍保留其原快照，没有修改。

## 当前仍需限定的措辞风险

P1：0项；P2：6项。P2表示证据范围/解释需限定，不表示绑定数值错误。

- **P2 / C19**：Each new analysis states thresholds before computation 总括需保留逐组来源精度；不能暗示每个原Git对象均可复核或外部预注册。 [当前锚点](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:200>)。
- **P2 / C25**：link conditional gains to history/strong shrinkage 只支持 tested configurations，后文 sufficient history 不宜读作充分条件。 [当前锚点](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:238>)。
- **P2 / C27**：正文partial support未直述QR33 P2 planned0；S39保留但只读正文者可能高估高history测试覆盖。 [当前锚点](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:246>)。
- **P2 / C33**：摘要29/34未就近说明事后取corrected/ordinary较好者；不能当作单一实时可执行F的胜率。 [当前锚点](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)。
- **P2 / C35**：Why does regression lose 和 indicates limited incremental information 可能被读成因果/信息不存在；证据只提供菜单内诊断。 [当前锚点](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:293>)。
- **P2 / C38**：摘要/intro泛称regression medians宜点明full版本；QR4 H6 median screen未达预定5pp。 [当前锚点](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)。

## 全文逐组映射

### C01｜采样绝对净头寸峰值与 endpoint 漏掉中间 breach

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[24](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:24>)；[29](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:29>)；[82](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:82>)；[86](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:86>)；[89](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:89>)。

**当前表/图/命题/补充：**[fig:example](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:29>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `json:notes/v7/example-selection.json#/selection`：[notes/v7/example-selection.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v7/example-selection.json>)，`#/selection`。

**证据支持：**定义和保存例图路径一致：origin408，endpoint48144 < report73139 < peak74397，单位USD millions。

**必须保留的边界：**仅采样净头寸，不能直接代表gross exposure、PnL或连续时间极值。

### C02｜pinball、strict breach与floor/headroom恒等式

**主文位置：**[86](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:86>)；[93](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:93>)；[189](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:189>)。

**当前表/图/命题/补充：**[prop:floor](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:96>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#the tail qualification requires the true conditional quantile`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:67>)。

**原文献/规范：**[koenker1978](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:466>)（https://doi.org/10.2307/1913643）；[gneiting2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:449>)（https://doi.org/10.1198/jasa.2011.r10138）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**正文公式明确响应、损失、strict exceedance；S1区分投影和真实条件分位。

**必须保留的边界：**loss降低不等于breach次数降低。

### C03｜已知floor投影逐点不增loss、真实条件分位的strict coverage

**主文位置：**[96](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:96>)；[100](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:100>)。

**当前表/图/命题/补充：**[prop:floor](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:96>)；[sup:floor](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:55>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#Proposition 1: floor projection`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:63>)。

**证据支持：**S1提供逐点恒等式及真实lower inverse quantile覆盖论证。

**必须保留的边界：**覆盖陈述属于真实条件分位，拟合报告不自动继承。

### C04｜独立对称增量下经典endpoint-to-peak界

**主文位置：**[103](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:103>)；[107](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:107>)。

**当前表/图/命题/补充：**[prop:levy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:103>)；[sup:levy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:102>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#section{Classical endpoint-to-peak`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:102>)。

**证据支持：**命题与S2列独立、逐个对称、population endpoint quantile及条件应用要求。

**必须保留的边界：**经验plug-in不是覆盖保证，金融依赖未满足该定理前提。

### C05｜horizon可能crossing；mean-reverting levels与serial increments需区分

**主文位置：**[110](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:110>)；[113](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:113>)。

**当前表/图/命题/补充：**[sup:simulation-original](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:148>)；[sup:simulation-primary](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:193>)；[sup:simulation-secondary](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:247>)；[sup:coherence](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1120>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `old:75`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/75`；唯一CSV筛选 `{"source": "fx_hourly", "window": "720", "method": "QR"}`，字段 `strict_crossing_count`；保存值 `640`。

**证据支持：**640个short-history FX crossing有原字段；S3–S5保留不同过程说明。

**必须保留的边界：**例示过程不证明实际金融序列独立/对称。

### C06｜匹配目标/完成标签/历史/refit；rolling reference另列

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[26](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:26>)；[44](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:44>)；[165](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[187](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:187>)；[250](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:250>)；[364](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:364>)。

**当前表/图/命题/补充：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)；[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)；[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#paragraph{Completed labels`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1191>)。

**证据支持：**S23给出成熟标签索引与held transforms，方法表和原protocol分开rolling reference。

**必须保留的边界：**匹配比较不隔离feature因果效果。

### C07｜FX一个market maker、18576记录及不同chronological grids

**主文位置：**[120](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:120>)；[375](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:375>)。

**当前表/图/命题/补充：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:76`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/76` → `protocol/revision-20261022/study-spec.json#/sources/fx_hourly/record_count`；保存值 `18576`。
- `text:submission-final/supplement.tex#The FX evidence describes`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1627>)。

**原文献/规范：**[dataset](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:470>)（https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset）；[wisniewski2020](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:482>)（https://proceedings.mlr.press/v128/wisniewski20a.html）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**record_count来自原study-spec；单一市场商与original period inspected由数据/原scope支持。

**必须保留的边界：**单一dealer，无未见prospective金融确认。

### C08｜NY Fed Treasury706记录、聚合long-minus-short与额外类别

**主文位置：**[122](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:122>)。

**当前表/图/命题/补充：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)；[sup:panel](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:512>)；[sup:panel-second](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:577>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:77`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/77` → `protocol/revision-20261022/study-spec.json#/sources/nyfed_weekly/record_count`；保存值 `706`。

**原文献/规范：**[nyfeddata](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:443>)（https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics）；[fr2004_2013](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:423>)（https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=f555fe11-e149-479b-8088-4ed4e9ae1206）；[fr2004_2024](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:425>)（https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=950ab256-b485-4586-99b0-b27eb205fdfa）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**record_count绑定study-spec；官方数据/FR2004引用对应定义。

**必须保留的边界：**下载economic-date vintage；aggregated net不是individual gross risk。

### C09｜FX日度930天/501issues与same-source聚合边界

**主文位置：**[124](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:124>)；[130](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:130>)。

**当前表/图/命题/补充：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)；[sup:v8-daily](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1328>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:96`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/96` → `results/revision-v8/wp4/summary.json#/source_consistency/daily_metadata/n_daily`；保存值 `930`。
- `old:97`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/97` → `results/revision-v8/wp4/summary.json#/cells/0/evaluation/n`；保存值 `501`。
- `text:submission-final/supplement.tex#Daily aggregation jointly changes`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1631>)。

**证据支持：**summary保存n_daily和evaluation n；每日最后记录与partial boundary days按原规则。

**必须保留的边界：**同时改变跨度/时钟/响应等，纯频率效应未识别。

### C10｜CFTC survivor universe、17合格代码及full-sample OI排序

**主文位置：**[32](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:32>)；[126](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:126>)；[377](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:377>)。

**当前表/图/命题/补充：**[tab:v10-cftc-contracts](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-cftc-contracts.tex:4>)；[sup:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1528>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `new:1`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/1`；保存值 `17`。
- `new:2`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/2`；保存值 `141`。
- `json:results/v10/cftc/eligibility.json#/selected`：[results/v10/cftc/eligibility.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/eligibility.json>)，`#/selected`。
- `text:submission-final/supplement.tex#Full-period mean open interest`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1531>)。

**原文献/规范：**[cftcTFF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:433>)（https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**eligibility保存全部候选/排除/选中17代码；20上限没截断，OI排序只排列survivors。

**必须保留的边界：**独立reporting system不等于独立dealer复制。

### C11｜CFTC877周、52/260分段、H6、13步refit与经济/发布时钟

**主文位置：**[128](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:128>)；[378](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:378>)。

**当前表/图/命题/补充：**[sup:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1528>)；[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `new:0`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/0` → `results/v10/cftc/eligibility.json#/N`；保存值 `877`。
- `new:4`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/4` → `results/v10/cftc/splits.json#/indices/validation_n`；保存值 `52`。
- `new:5`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/5` → `results/v10/cftc/splits.json#/indices/evaluation_n`；保存值 `260`。
- `new:6`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/6` → `results/v10/cftc/splits.json#/indices/unissued_gap_n`；保存值 `6`。
- `new:9`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/9` → `results/v10/cftc/splits.json#/actual_dates/evaluation/first`；保存值 `2021-09-21`。
- `new:10`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/10` → `results/v10/cftc/splits.json#/actual_dates/evaluation/last`；保存值 `2026-09-08`。
- `new:11`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/11` → `results/v10/cftc/splits.json#/actual_dates/evaluation/last_label_end`；保存值 `2026-10-20`。
- `new:58`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/58` → `results/v10/cftc/manifest.json#/design/horizon`；保存值 `6`。
- `new:59`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/59` → `results/v10/cftc/manifest.json#/design/windows`。
- `new:60`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/60` → `results/v10/cftc/manifest.json#/design/refit_step`；保存值 `13`。
- `text:submission-final/supplement.tex#Actual positions are normally measured`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1534>)。

**证据支持：**splits/manifest支持所有日期/长度/refit；S30保留周二测量周五发布及delay说明。

**必须保留的边界：**首次发布vintage未重建，不能称实时public-information-clock策略。

### C12｜描述表全部字段与九个within-series统计分别跨源取median

**主文位置：**[130](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:130>)；[132](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:132>)。

**当前表/图/命题/补充：**[tab:v12-data](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v12-data-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `descriptives:numeric_bindings`：[results/v12/descriptives/number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v12/descriptives/number-bindings.json>)，`#/numeric_bindings`。
- `descriptives:table_bindings`：[results/v12/descriptives/number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v12/descriptives/number-bindings.json>)，`#/table_bindings`。
- `json:results/v12/descriptives/metadata.json#/definitions`：[results/v12/descriptives/metadata.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v12/descriptives/metadata.json>)，`#/definitions`。

**证据支持：**现有1324 numeric与100 table binding逐指针/源SHA读回；metadata date display规则保留。

**必须保留的边界：**未重算统计；不同单位不池化为common-dollar风险。

### C13｜corrected rank历史headroom、sample-max cap、重锚/peak floor、tau和horizon

**主文位置：**[138](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:138>)；[140](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:140>)；[142](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:142>)；[143](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:143>)；[145](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:145>)；[146](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:146>)；[147](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:147>)；[168](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:168>)；[169](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:169>)；[170](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:170>)；[174](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:174>)。

**当前表/图/命题/补充：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[sup:rank](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)；[prop:levy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:103>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `json:protocol/revision-20261022/study-spec.json#/tau_numerator`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/tau_numerator`；保存值 `19`。
- `json:protocol/revision-20261022/study-spec.json#/tau_denominator`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/tau_denominator`；保存值 `20`。
- `text:submission-final/supplement.tex#section{Ordinary quantile ranks`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)。

**证据支持：**tau19/20与H按后续源记录计数；S8给rank和minimizer convention。

**必须保留的边界：**依赖下无finite-sample coverage；同H不同源不代表相同物理时长。

### C14｜QR33/QR4特征、ridge、训练缩放、projection与finite/infinite菜单

**主文位置：**[149](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:149>)；[151](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:151>)；[152](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:152>)；[153](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:153>)；[154](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:154>)；[156](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:156>)；[157](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:157>)；[158](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:158>)；[171](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:171>)；[173](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:173>)；[178](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:178>)。

**当前表/图/命题/补充：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)；[sup:rank](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `json:protocol/revision-20261022/study-spec.json#/feature_count_without_intercept`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/feature_count_without_intercept`；保存值 `33`。
- `json:protocol/revision-20261022/study-spec.json#/features`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/features`。
- `v12:30`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/30`；保存值 `5`。
- `text:submission-final/supplement.tex#paragraph{Regression and local quantiles`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1200>)。

**原文献/规范：**[koenker1978](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:466>)（https://doi.org/10.2307/1913643）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**原特征/目标式、五finite与六点版本有保存定义；projection发行/评分，非training objective内。

**必须保留的边界：**infinite为lower ordinary quantile，不同corrected F；菜单改变即程序改变。

### C15｜local/filtered/forest/tail等已执行有限规格及失败库存

**主文位置：**[160](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:160>)；[172](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:172>)；[175](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:175>)。

**当前表/图/命题/补充：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[sup:ar](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:375>)；[sup:levy-empirical](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:297>)；[sup:reproduction](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1583>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `json:protocol/revision-20261022/study-spec.json#/knn_rank`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/knn_rank`；保存值 `ceil((k+1)*19/20); unavailable rank fails`。
- `text:submission-final/supplement.tex#Local methods use training-only`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1204>)。

**原文献/规范：**[hull1998](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:464>)（https://doi.org/10.21314/jor.1998.001）；[barone1999](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:421>)（https://doi.org/10.1002/(SICI)1096-9934(199908)19:5<583::AID-FUT5>3.0.CO;2-S）；[meinshausen2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:474>)（https://www.jmlr.org/papers/v7/meinshausen06a.html）；[mcneilfrey2000](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:472>)（https://doi.org/10.1016/s0927-5398(00)00012-8）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**原引用对应算法类别；S7/S11–18/S34给完整执行库存与失败，不新跑算法。

**必须保留的边界：**不能代表所有现代distributional模型。

### C16｜delayed calibration/SAV、固定组合、earlier one-SE与later gate分离

**主文位置：**[162](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:162>)；[176](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:176>)。

**当前表/图/命题/补充：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[sup:wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:793>)；[sup:wp2-pairs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:855>)；[sup:wp3](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:899>)；[sup:selection](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:674>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#Updates wait for the full`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1541>)。
- `text:submission-final/supplement.tex#section{Finite delayed calibration`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:793>)。

**原文献/规范：**[engle2004](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:441>)（https://doi.org/10.1198/073500104000000370）；[gibbs2021](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:447>)（https://proceedings.neurips.cc/paper_files/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html）；[hastie2009](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:460>)（https://doi.org/10.1007/978-0-387-84858-7）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**原方法引用与补充执行设置；成熟反馈后更新，固定组合成员，one-SE倾向强shrinkage。

**必须保留的边界：**延迟反馈不构成覆盖保证；1SE不是显著性水平。

### C17｜训练标签必须成熟、训练变换固定；原validation与fixed backcast penalty分开

**主文位置：**[185](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:185>)。

**当前表/图/命题/补充：**[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)；[sup:v8-backcast](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1356>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `json:protocol/revision-20261022/study-spec.json#/sources`：[protocol/revision-20261022/study-spec.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/revision-20261022/study-spec.json>)，`#/sources`。
- `text:submission-final/supplement.tex#paragraph{Completed labels`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1191>)。

**证据支持：**r-H-W+1..r-H训练区间与原protocol/S23一致。

**必须保留的边界：**成熟label不补齐真实发布时间，backcast固定penalty仍是事后研究。

### C18｜HAC/DM、HLN/Holm、多family与sparse hit likelihood

**主文位置：**[189](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:189>)；[190](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:190>)；[192](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:192>)；[193](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:193>)；[195](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:195>)。

**当前表/图/命题/补充：**[sup:implementation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1189>)；[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)；[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)；[sup:v10-diagnostics](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1579>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `old:45`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/45`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `dm_p`；保存值 `2.1950725127844084e-07`。
- `old:46`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/46`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `hln_p`；保存值 `2.312477658474048e-07`。
- `old:47`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/47`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `primary_bonferroni_p`；保存值 `4.390145025568817e-07`。
- `old:48`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/48`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `dm_p`；保存值 `4.472961414014163e-09`。
- `old:49`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/49`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `hln_p`；保存值 `4.82747017649871e-09`。
- `old:50`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/50`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `archived72_holm_p`；保存值 `2.8626953049690645e-07`。
- `old:51`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/51`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `dm_p`；保存值 `0.007611369596467356`。
- `old:52`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/52`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `hln_p`；保存值 `0.009390617005130322`。
- `old:53`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/53`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `holm_p`；保存值 `0.31967752305162894`。
- `text:submission-final/supplement.tex#paragraph{Working-reference inference`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1221>)。

**原文献/规范：**[dm1995](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:435>)（https://doi.org/10.1080/07350015.1995.10524599）；[nw1987](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:476>)（https://doi.org/10.2307/1913610）；[hln1997](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:458>)（https://doi.org/10.1016/s0169-2070(96)00719-4）；[holm1979](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:462>)（https://www.jstor.org/stable/4615733）；[kupiec1995](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:468>)（https://doi.org/10.3905/jod.1995.407942）；[christ1998](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:431>)（https://doi.org/10.2307/2527341）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**保存推断字段有不同family和HLN/带宽标签；S23明示初始hit条件化。

**必须保留的边界：**working-reference p值不包括research-stage选择；nonrejection不证明coverage。

### C19｜透明度：原FX已查看、逐组设计/运行时序、回顾性与相关任务

**主文位置：**[200](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:200>)；[376](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:376>)。

**当前表/图/命题/补充：**[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)；[sup:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:1>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `json:notes/submission/prediction-register.json#/timing_by_group`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/timing_by_group`。
- `text:submission-final/supplement.tex#Its original evaluation period was viewed`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1627>)。

**证据支持：**登记区分local/public/run：WP2公开after-run；F2/G2/G3新算前公开。

**必须保留的边界：**Git留档不等于外部注册；E5原design对象不可读，只能按保存回执精度表述。

**P2风险：**Each new analysis states thresholds before computation 总括需保留逐组来源精度；不能暗示每个原Git对象均可复核或外部预注册。

### C20｜MCS逐格90%、R/1000stationary bootstrap、block规则与duplicate处理

**主文位置：**[204](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:204>)；[206](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:206>)。

**当前表/图/命题/补充：**[sup:v10-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1546>)；[sup:v13-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:1>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `new:52`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/52` → `results/v10/mcs/manifest.json#/design/package`；保存值 `arch==8.0.0`。
- `new:53`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/53` → `results/v10/mcs/manifest.json#/design/confidence`；保存值 `0.9`。
- `new:54`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/54` → `results/v10/mcs/manifest.json#/design/statistic`；保存值 `R`。
- `new:55`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/55` → `results/v10/mcs/manifest.json#/design/bootstrap`；保存值 `stationary`。
- `new:56`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/56` → `results/v10/mcs/manifest.json#/design/bootstrap_repetitions`；保存值 `1000`。
- `new:57`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/57` → `results/v10/mcs/manifest.json#/design/block_size`；保存值 `max(H,ceil(n**(1/3)))`。
- `text:submission-final/generated/v13-supplement.tex#Joint comparison leaves`：[submission-final/generated/v13-supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:3>)。

**原文献/规范：**[mcs2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:453>)（https://doi.org/10.3982/ECTA5771）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**manifest保存arch版本、nominal参数；相同loss column合并后恢复label。

**必须保留的边界：**依赖假设、样本与research-stage选择限制名义解释，不做跨市场独立pooled test。

### C21｜大多数MCS保留历史与替代方法，未建立等风险/唯一优胜

**主文位置：**[288](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:288>)。

**当前表/图/命题/补充：**[tab:v10-mcs-main](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-mcs-main.tex:3>)；[sup:v10-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1546>)；[sup:v13-mcs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:1>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `new:41`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/41` → `results/v10/mcs/summary.json#/overall/planned_comparisons`；保存值 `98`。
- `new:42`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/42` → `results/v10/mcs/summary.json#/overall/metrics/matched_FI_membership/count_successful`；保存值 `90`。
- `new:43`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/43` → `results/v10/mcs/summary.json#/overall/metrics/literal_sole_FI/count_successful`；保存值 `2`。
- `new:44`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/44` → `results/v10/mcs/summary.json#/overall/metrics/sole_loss_class_FI/count_successful`；保存值 `4`。
- `new:47`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/47` → `results/v10/mcs/summary.json#/overall/unavailable_method_slots`；保存值 `60`。

**证据支持：**90/98格有matched历史；literal sole2、sole loss class4；未完成方法slot保留。

**必须保留的边界：**不淘汰不等价风险，不保证future coverage或simultaneous best。

### C22｜FX两期matched14.77/16.62% gain，rolling -12.66/+3.17及issues/breaches

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[44](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:44>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)；[214](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:214>)；[223](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)；[226](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:226>)；[227](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:227>)；[228](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:228>)；[229](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:229>)；[390](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:390>)。

**当前表/图/命题/补充：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:0`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/0`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `relative_mean_loss_difference_percent`；保存值 `-14.766762552613885`。
- `old:1`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/1` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/0/ratio_change_percent`；保存值 `-16.62356533682211`。
- `old:7`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/7`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `strict_breach_count_left`；保存值 `376`。
- `old:8`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/8`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `strict_breach_count_right`；保存值 `360`。
- `old:12`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/12`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `relative_mean_loss_difference_percent`；保存值 `-12.660126412969763`。
- `old:13`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/13`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `origin_count`；保存值 `6625`。
- `old:14`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/14`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `strict_breach_count_left`；保存值 `376`。
- `old:15`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/15`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}`，字段 `strict_breach_count_right`；保存值 `332`。
- `old:16`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/16`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}`，字段 `origin_count`；保存值 `6625`。
- `old:17`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/17` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/1/ratio_change_percent`；保存值 `3.1681985293173343`。
- `old:18`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/18` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/1/n`；保存值 `1440`。
- `old:19`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/19` → `results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/0/n`；保存值 `1440`。
- `old:20`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/20`；唯一CSV筛选 `{"phase": "retro", "source": "fx_hourly", "series_key": "fx_hourly", "horizon": "6", "window": "2880", "report": "R0"}`，字段 `strict_breach_count`；保存值 `20`。
- `old:21`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/21`；唯一CSV筛选 `{"phase": "retro", "source": "fx_hourly", "series_key": "fx_hourly", "horizon": "6", "window": "2880", "report": "F"}`，字段 `strict_breach_count`；保存值 `16`。

**证据支持：**paired CSV和earlier HAC results逐字段支持全部FX表行；四舍五入支持abstract14.8/16.6。

**必须保留的边界：**matched conditioning gain不决定短rolling排序，且不是prospective确认。

### C23｜FX短history H24 +31.5% loss、924/427 breaches

**主文位置：**[216](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:216>)。

**当前表/图/命题/补充：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)；[sup:coherence](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1120>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:23`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/23`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h24-QR720-minus-frozen_F720"}`，字段 `relative_mean_loss_difference_percent`；保存值 `31.503964246480916`。
- `old:24`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/24`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h24-QR720-minus-frozen_F720"}`，字段 `strict_breach_count_left`；保存值 `924`。
- `old:25`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/25`；唯一CSV筛选 `{"contrast_id": "fx_hourly-h24-QR720-minus-frozen_F720"}`，字段 `strict_breach_count_right`；保存值 `427`。

**证据支持：**同一contrast的loss/breaches字段可读回。

**必须保留的边界：**特定H/history adverse case不能概括所有QR经济失败。

### C24｜wrapper保留later FX gain -15.00%，329/328 breaches

**主文位置：**[218](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:218>)；[230](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:230>)。

**当前表/图/命题/补充：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)；[sup:wp2-pairs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:855>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:2`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/2` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/qr_minus_f_loss_percent`；保存值 `-14.99691078803782`。
- `old:3`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/3` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/qr_hits`；保存值 `329`。
- `old:4`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/4` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/f_hits`；保存值 `328`。
- `old:22`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/22` → `results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/n`；保存值 `6625`。

**证据支持：**wrapped_pairs/1共同origin、loss与hits原字段完整。

**必须保留的边界：**是finite delayed ACI exercise，不是新RP gate；score/breach不一致仍在。

### C25｜FX history learning curve非单调、QR4改符号、各自matched F

**主文位置：**[44](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:44>)；[238](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:238>)；[241](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:241>)；[304](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:304>)；[390](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:390>)。

**当前表/图/命题/补充：**[fig:v11-history](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:241>)；[sup:v11-history](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1612>)；[sup:v10-menu](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1498>)。

**预测登记：**`E1.M1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/6`）；`E1.M2.QR33` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/7`）；`E1.M3.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/8`）。

**已有数值/来源定位：**

- `v11:0`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/0` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/window`；保存值 `360`。
- `v11:1`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/1` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/horizon`；保存值 `6`。
- `v11:2`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/2` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/relative_loss_percent`；保存值 `3.0438186779438983`。
- `v11:3`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/3` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/n`；保存值 `6625`。
- `v11:4`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/4` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/window`；保存值 `720`。
- `v11:5`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/5` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/horizon`；保存值 `6`。
- `v11:6`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/6` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/relative_loss_percent`；保存值 `-2.1167271486370893`。
- `v11:7`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/7` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/n`；保存值 `6625`。
- `v11:8`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/8` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/window`；保存值 `1440`。
- `v11:9`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/9` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/horizon`；保存值 `6`。
- `v11:10`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/10` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/relative_loss_percent`；保存值 `-6.5076708350722905`。
- `v11:11`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/11` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/n`；保存值 `6625`。
- `v11:12`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/12` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/window`；保存值 `2880`。
- `v11:13`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/13` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/horizon`；保存值 `6`。
- `v11:14`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/14` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/relative_loss_percent`；保存值 `-14.766762552613883`。
- `v11:15`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/15` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/n`；保存值 `6625`。
- `v11:16`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/16` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/window`；保存值 `5760`。
- `v11:17`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/17` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/horizon`；保存值 `6`。
- `v11:18`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/18` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/relative_loss_percent`；保存值 `-6.440694459797079`。
- `v11:19`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/19` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/n`；保存值 `6625`。
- `v11:20`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/20` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/window`；保存值 `360`。
- `v11:21`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/21` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/horizon`；保存值 `6`。
- `v11:22`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/22` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/relative_loss_percent`；保存值 `-0.8754052083818208`。
- `v11:23`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/23` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/5/n`；保存值 `6625`。
- `v11:24`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/24` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/window`；保存值 `720`。
- `v11:25`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/25` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/horizon`；保存值 `6`。
- `v11:26`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/26` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/relative_loss_percent`；保存值 `1.4764717411070867`。
- `v11:27`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/27` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/9/n`；保存值 `6625`。
- `v11:28`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/28` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/window`；保存值 `1440`。
- `v11:29`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/29` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/horizon`；保存值 `6`。
- `v11:30`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/30` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/relative_loss_percent`；保存值 `-3.2812108413789005`。
- `v11:31`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/31` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/13/n`；保存值 `6625`。
- `v11:32`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/32` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/window`；保存值 `2880`。
- `v11:33`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/33` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/horizon`；保存值 `6`。
- `v11:34`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/34` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/relative_loss_percent`；保存值 `-4.2893706508927965`。
- `v11:35`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/35` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/1/n`；保存值 `6625`。
- `v11:36`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/36` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/window`；保存值 `5760`。
- `v11:37`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/37` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/horizon`；保存值 `6`。
- `v11:38`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/38` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/relative_loss_percent`；保存值 `-4.891469312713009`。
- `v11:39`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/39` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/17/n`；保存值 `6625`。
- `v11:40`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/40` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/successes`；保存值 `47`。
- `v11:41`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/41` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/denominator`；保存值 `48`。
- `v11:42`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/42` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/missing`；保存值 `0`。
- `v11:43`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/43` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/minimum_fraction`；保存值 `0.8`。
- `v11:44`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/44` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P1/status`；保存值 `SUPPORT`。
- `v11:45`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/45` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/successes`；保存值 `21`。
- `v11:46`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/46` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/denominator`；保存值 `24`。
- `v11:47`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/47` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/missing`；保存值 `0`。
- `v11:48`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/48` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/minimum_fraction`；保存值 `0.6`。
- `v11:49`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/49` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P2/status`；保存值 `SUPPORT`。
- `v11:50`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/50` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/successes`；保存值 `42`。
- `v11:51`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/51` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/denominator`；保存值 `48`。
- `v11:52`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/52` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/missing`；保存值 `0`。
- `v11:53`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/53` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/minimum_fraction`；保存值 `1.0`。
- `v11:54`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/54` → `evidence/v11/pr5-v9/results/revision-v9/wp2/support.json#/P3/status`；保存值 `NOT_SUPPORT`。
- `v11:55`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/55` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/window`；保存值 `2880`。
- `v11:56`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/56` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/horizon`；保存值 `6`。
- `v11:57`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/57` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/0/relative_loss_percent`；保存值 `-14.766762552613883`。
- `v11:58`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/58` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/window`；保存值 `360`。
- `v11:59`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/59` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/horizon`；保存值 `6`。
- `v11:60`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/60` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/4/relative_loss_percent`；保存值 `3.0438186779438983`。
- `v11:61`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/61` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/window`；保存值 `720`。
- `v11:62`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/62` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/horizon`；保存值 `6`。
- `v11:63`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/63` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/8/relative_loss_percent`；保存值 `-2.1167271486370893`。
- `v11:64`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/64` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/window`；保存值 `1440`。
- `v11:65`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/65` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/horizon`；保存值 `6`。
- `v11:66`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/66` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/12/relative_loss_percent`；保存值 `-6.5076708350722905`。
- `v11:67`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/67` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/window`；保存值 `5760`。
- `v11:68`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/68` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/horizon`；保存值 `6`。
- `v11:69`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/69` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/16/relative_loss_percent`；保存值 `-6.440694459797079`。
- `v11:70`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/70` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/18/window`；保存值 `5760`。
- `v11:71`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/71` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/18/horizon`；保存值 `24`。
- `v11:72`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/72` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/18/relative_loss_percent`；保存值 `1.8577089031029423`。
- `v11:73`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/73` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/19/window`；保存值 `5760`。
- `v11:74`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/74` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/19/horizon`；保存值 `24`。
- `v11:75`：[notes/v11/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v11/imported-number-bindings.json>)，`#/bindings/75` → `evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json#/19/relative_loss_percent`；保存值 `0.15840259366901976`。
- `new:20`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/20` → `results/v10/menu/summary.json#/across_sources/0/median_pct`；保存值 `0.2069371499562489`。
- `new:21`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/21` → `results/v10/menu/summary.json#/across_sources/0/original_median_pct`；保存值 `116.24327967680179`。
- `new:26`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/26` → `results/v10/menu/summary.json#/across_sources/2/status`；保存值 `UNASSESSABLE`。
- `new:28`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/28` → `results/v10/menu/summary.json#/across_sources/4/median_pct`；保存值 `-0.22777914491914353`。
- `new:29`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/29` → `results/v10/menu/summary.json#/across_sources/4/original_median_pct`；保存值 `121.40097999787356`。
- `new:34`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/34` → `results/v10/menu/summary.json#/across_sources/6/status`；保存值 `UNASSESSABLE`。
- `new:36`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/36` → `results/v10/menu/summary.json#/predictions/M1/status`；保存值 `SUPPORTED`。
- `new:37`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/37` → `results/v10/menu/summary.json#/predictions/M2/status`；保存值 `NOT_SUPPORTED`。
- `new:38`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/38` → `results/v10/menu/summary.json#/predictions/M3/status`；保存值 `SUPPORTED`。
- `new:40`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/40` → `results/v10/menu/summary.json#/predictions/M3/joint_improved_sources`；保存值 `13`。

**证据支持：**76个v11导入字段保存全部history/method contrast与synthetic support；源SHA/原字段读回。 主文validation段末的simulation menu句另指S29/E1：W52 constant116.24→.21、switching121.40→-.23；M1/M3成立，M2不成立，W260旧菜单失败whole summary不可用。

**必须保留的边界：**原FX期和不同菜单；未确定一般最优/充分history，模拟不是新金融确认。

**P2风险：**link conditional gains to history/strong shrinkage 只支持 tested configurations，后文 sufficient history 不宜读作充分条件。

### C26｜WP2低区间15/17与29/34，W52/W260已知，仅W520新算；local/public时序

**主文位置：**[246](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:246>)。

**当前表/图/命题/补充：**[par:wp2-history](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:245>)；[tab:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:9>)；[sup:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:1>)。

**预测登记：**`WP2.P1_QR4.QR4` → `SUPPORT`（`notes/submission/prediction-register.json#/rows/31`）；`WP2.P1_QR33.QR33` → `SUPPORT`（`notes/submission/prediction-register.json#/rows/32`）。

**已有数值/来源定位：**

- `wp2:0`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/0` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/status`；保存值 `SUPPORT`。
- `wp2:1`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/1` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/planned`；保存值 `17`。
- `wp2:2`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/2` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/successes`；保存值 `15`。
- `wp2:3`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/3` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/threshold`；保存值 `0.8`。
- `wp2:4`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/4` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/status`；保存值 `SUPPORT`。
- `wp2:5`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/5` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/planned`；保存值 `34`。
- `wp2:6`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/6` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/successes`；保存值 `29`。
- `wp2:7`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/7` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/threshold`；保存值 `0.8`。
- `json:notes/submission/prediction-register.json#/timing_by_group/WP2`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/timing_by_group/WP2`。

**证据支持：**保存计数/阈值/判定一致；local设计早13.372451秒，public after-run；H4已在正文就近披露。

**必须保留的边界：**不是external preregistration、prospective确认或全部新金融样本。

### C27｜WP2 P2QR4 10/17、P3 6/17失败，QR33 P2 planned0不可测，总体partial

**主文位置：**[246](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:246>)。

**当前表/图/命题/补充：**[tab:submission-wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:9>)；[tab:submission-wp2-counterexamples](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/submission-wp2.tex:33>)。

**预测登记：**`WP2.P2_QR4.QR4` → `NOT_SUPPORT`（`notes/submission/prediction-register.json#/rows/33`）；`WP2.P2_QR33.QR33` → `NOT_TESTABLE`（`notes/submission/prediction-register.json#/rows/34`）；`WP2.P3_QR4.QR4` → `NOT_SUPPORT`（`notes/submission/prediction-register.json#/rows/35`）。

**已有数值/来源定位：**

- `wp2:0`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/0` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/status`；保存值 `SUPPORT`。
- `wp2:1`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/1` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/planned`；保存值 `17`。
- `wp2:2`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/2` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/successes`；保存值 `15`。
- `wp2:3`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/3` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR4/threshold`；保存值 `0.8`。
- `wp2:4`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/4` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/status`；保存值 `SUPPORT`。
- `wp2:5`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/5` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/planned`；保存值 `34`。
- `wp2:6`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/6` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/successes`；保存值 `29`。
- `wp2:7`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/7` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P1_QR33/threshold`；保存值 `0.8`。
- `wp2:8`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/8` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/status`；保存值 `NOT_SUPPORT`。
- `wp2:9`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/9` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/planned`；保存值 `17`。
- `wp2:10`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/10` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/successes`；保存值 `10`。
- `wp2:11`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/11` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR4/threshold`；保存值 `0.6`。
- `wp2:12`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/12` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR33/status`；保存值 `NOT_TESTABLE`。
- `wp2:13`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/13` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P2_QR33/planned`；保存值 `0`。
- `wp2:14`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/14` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/status`；保存值 `NOT_SUPPORT`。
- `wp2:15`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/15` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/planned`；保存值 `17`。
- `wp2:16`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/16` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/successes`；保存值 `6`。
- `wp2:17`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/17` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/tests/P3_QR4/threshold`；保存值 `0.7`。
- `wp2:18`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/18` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/screen`；保存值 `P1_QR4`。
- `wp2:19`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/19` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/code`；保存值 `240743`。
- `wp2:20`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/20` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/relative_loss_percent`；保存值 `-7.324391440817724`。
- `wp2:21`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/21` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/0/window`；保存值 `52`。
- `wp2:22`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/22` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/screen`；保存值 `P1_QR4`。
- `wp2:23`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/23` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/code`；保存值 `098662`。
- `wp2:24`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/24` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/relative_loss_percent`；保存值 `-0.43743237154514336`。
- `wp2:25`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/25` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/1/window`；保存值 `52`。
- `wp2:26`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/26` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/screen`；保存值 `P2_QR4`。
- `wp2:27`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/27` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/code`；保存值 `044601`。
- `wp2:28`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/28` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/relative_loss_percent`；保存值 `0.8114450417117558`。
- `wp2:29`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/29` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/2/window`；保存值 `520`。
- `wp2:30`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/30` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/screen`；保存值 `P2_QR4`。
- `wp2:31`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/31` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/code`；保存值 `043602`。
- `wp2:32`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/32` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/relative_loss_percent`；保存值 `8.026474775159897`。
- `wp2:33`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/33` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/3/window`；保存值 `520`。
- `wp2:34`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/34` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/screen`；保存值 `P2_QR4`。
- `wp2:35`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/35` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/code`；保存值 `042601`。
- `wp2:36`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/36` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/relative_loss_percent`；保存值 `1.1375177833979677`。
- `wp2:37`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/37` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/4/window`；保存值 `520`。
- `wp2:38`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/38` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/screen`；保存值 `P2_QR4`。
- `wp2:39`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/39` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/code`；保存值 `045601`。
- `wp2:40`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/40` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/relative_loss_percent`；保存值 `1.5209378297702525`。
- `wp2:41`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/41` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/5/window`；保存值 `520`。
- `wp2:42`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/42` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/screen`；保存值 `P2_QR4`。
- `wp2:43`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/43` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/code`；保存值 `099741`。
- `wp2:44`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/44` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/relative_loss_percent`；保存值 `0.6181027154300134`。
- `wp2:45`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/45` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/6/window`；保存值 `520`。
- `wp2:46`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/46` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/screen`；保存值 `P2_QR4`。
- `wp2:47`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/47` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/code`；保存值 `095741`。
- `wp2:48`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/48` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/relative_loss_percent`；保存值 `3.8759253581046593`。
- `wp2:49`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/49` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/7/window`；保存值 `520`。
- `wp2:50`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/50` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/screen`；保存值 `P2_QR4`。
- `wp2:51`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/51` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/code`；保存值 `232741`。
- `wp2:52`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/52` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/relative_loss_percent`；保存值 `0.5759009077565658`。
- `wp2:53`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/53` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/8/window`；保存值 `520`。
- `wp2:54`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/54` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/screen`；保存值 `P1_QR33`。
- `wp2:55`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/55` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/code`；保存值 `045601`。
- `wp2:56`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/56` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/relative_loss_percent`；保存值 `-2.041453509696134`。
- `wp2:57`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/57` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/9/window`；保存值 `52`。
- `wp2:58`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/58` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/screen`；保存值 `P1_QR33`。
- `wp2:59`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/59` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/code`；保存值 `1170E1`。
- `wp2:60`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/60` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/relative_loss_percent`；保存值 `-16.215516778622597`。
- `wp2:61`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/61` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/10/window`；保存值 `260`。
- `wp2:62`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/62` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/screen`；保存值 `P1_QR33`。
- `wp2:63`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/63` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/code`；保存值 `090741`。
- `wp2:64`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/64` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/relative_loss_percent`；保存值 `-3.599484240650086`。
- `wp2:65`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/65` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/11/window`；保存值 `260`。
- `wp2:66`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/66` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/screen`；保存值 `P1_QR33`。
- `wp2:67`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/67` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/code`；保存值 `33874A`。
- `wp2:68`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/68` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/relative_loss_percent`；保存值 `-4.775475893615089`。
- `wp2:69`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/69` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/12/window`；保存值 `260`。
- `wp2:70`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/70` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/screen`；保存值 `P1_QR33`。
- `wp2:71`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/71` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/code`；保存值 `240743`。
- `wp2:72`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/72` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/relative_loss_percent`；保存值 `-2.28338015082018`。
- `wp2:73`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/73` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/13/window`；保存值 `260`。
- `wp2:74`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/74` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/screen`；保存值 `P3_QR4`。
- `wp2:75`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/75` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/code`；保存值 `042601`。
- `wp2:76`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/76` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/relative_losses`。
- `wp2:77`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/77` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/14/windows`。
- `wp2:78`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/78` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/screen`；保存值 `P3_QR4`。
- `wp2:79`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/79` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/code`；保存值 `045601`。
- `wp2:80`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/80` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/relative_losses`。
- `wp2:81`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/81` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/15/windows`。
- `wp2:82`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/82` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/screen`；保存值 `P3_QR4`。
- `wp2:83`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/83` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/code`；保存值 `099741`。
- `wp2:84`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/84` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/relative_losses`。
- `wp2:85`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/85` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/16/windows`。
- `wp2:86`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/86` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/screen`；保存值 `P3_QR4`。
- `wp2:87`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/87` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/code`；保存值 `1170E1`。
- `wp2:88`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/88` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/relative_losses`。
- `wp2:89`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/89` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/17/windows`。
- `wp2:90`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/90` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/screen`；保存值 `P3_QR4`。
- `wp2:91`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/91` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/code`；保存值 `097741`。
- `wp2:92`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/92` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/relative_losses`。
- `wp2:93`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/93` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/18/windows`。
- `wp2:94`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/94` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/screen`；保存值 `P3_QR4`。
- `wp2:95`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/95` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/code`；保存值 `096742`。
- `wp2:96`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/96` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/relative_losses`。
- `wp2:97`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/97` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/19/windows`。
- `wp2:98`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/98` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/screen`；保存值 `P3_QR4`。
- `wp2:99`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/99` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/code`；保存值 `095741`。
- `wp2:100`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/100` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/relative_losses`。
- `wp2:101`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/101` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/20/windows`。
- `wp2:102`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/102` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/screen`；保存值 `P3_QR4`。
- `wp2:103`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/103` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/code`；保存值 `090741`。
- `wp2:104`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/104` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/relative_losses`。
- `wp2:105`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/105` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/21/windows`。
- `wp2:106`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/106` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/screen`；保存值 `P3_QR4`。
- `wp2:107`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/107` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/code`；保存值 `232741`。
- `wp2:108`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/108` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/relative_losses`。
- `wp2:109`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/109` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/22/windows`。
- `wp2:110`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/110` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/screen`；保存值 `P3_QR4`。
- `wp2:111`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/111` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/code`；保存值 `240743`。
- `wp2:112`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/112` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/relative_losses`。
- `wp2:113`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/113` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/23/windows`。
- `wp2:114`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/114` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/screen`；保存值 `P3_QR4`。
- `wp2:115`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/115` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/code`；保存值 `098662`。
- `wp2:116`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/116` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/relative_losses`。
- `wp2:117`：[notes/submission/imported-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/imported-number-bindings.json>)，`#/bindings/117` → `evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json#/counterexamples/24/windows`。
- `json:notes/submission/prediction-register.json#/wp2_group_verdict`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/wp2_group_verdict`。

**证据支持：**118显示字段含固定分母、原判定及25条反例；summary主判断partial。

**必须保留的边界：**QR33高区间0计划不可检验；无法建立一般sufficient history、估计成本因果机制或dealer复制。

**P2风险：**正文partial support未直述QR33 P2 planned0；S39保留但只读正文者可能高估高history测试覆盖。

### C28｜Treasury main +50.79、54vs28/277；earlier short-window +144.30

**主文位置：**[252](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:252>)；[264](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:264>)；[265](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:265>)；[273](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:273>)。

**当前表/图/命题/补充：**[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:26`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/26`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `relative_mean_loss_difference_percent`；保存值 `50.78571256749063`。
- `old:27`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/27`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `strict_breach_count_left`；保存值 `54`。
- `old:28`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/28`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `strict_breach_count_right`；保存值 `28`。
- `old:33`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/33`；唯一CSV筛选 `{"id": "Treasury-W52-structural-analogue"}`，字段 `percent_vs_reference`；保存值 `144.296201250835`。
- `old:43`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/43`；唯一CSV筛选 `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}`，字段 `origin_count`；保存值 `277`。

**证据支持：**paired CSV与earlier primary-replication保持不同history。

**必须保留的边界：**不同history的adverse result不是同一程序复现。

### C29｜weekly panel由92.63缩至9.22但34/48仍输，QR4与ordinary完整行

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[254](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:254>)；[261](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)；[266](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:266>)；[267](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:267>)；[268](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:268>)；[269](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:269>)。

**当前表/图/命题/补充：**[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)。

**预测登记：**`E5.P1.QR33+` → `False`（`notes/submission/prediction-register.json#/rows/0`）；`E5.P2.QR33+` → `False`（`notes/submission/prediction-register.json#/rows/1`）；`E5.P3.QR33+` → `True`（`notes/submission/prediction-register.json#/rows/2`）。

**已有数值/来源定位：**

- `old:5`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/5` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR33_plus/losing_to_F`；保存值 `34`。
- `old:6`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/6` → `results/supervisor-20261023/e5/descriptive-summary.json#/planned_cells`；保存值 `48`。
- `old:29`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/29` → `results/supervisor-20261023/e5/descriptive-summary.json#/original_QR33/median_percent_vs_F`；保存值 `92.62799824594052`。
- `old:30`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/30` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR33_plus/median_percent_vs_F`；保存值 `9.220703399904492`。
- `old:34`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/34` → `results/supervisor-20261023/e5/descriptive-summary.json#/original_QR33/losing_to_F`；保存值 `45`。
- `old:35`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/35` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR4_plus/median_percent_vs_F`；保存值 `9.90727239745182`。
- `old:36`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/36` → `results/supervisor-20261023/e5/descriptive-summary.json#/QR4_plus/losing_to_F`；保存值 `37`。
- `old:37`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/37` → `results/supervisor-20261023/e5/descriptive-summary.json#/I/median_percent_vs_F`；保存值 `0.5006801691981209`。
- `old:38`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/38` → `results/supervisor-20261023/e5/descriptive-summary.json#/I/losing_to_F`；保存值 `30`。

**证据支持：**原summary支持4个panel行及48分母；E5P1/P2失败而P3成立。

**必须保留的边界：**相关聚合任务，不是独立dealer replication；更窄loss不等于全部标准通过。

### C30｜earlier one-SE选I17/26、median5.37vs4.15、worst181.39且R6全失败

**主文位置：**[254](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:254>)；[261](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)；[270](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:270>)；[271](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:271>)；[273](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:273>)。

**当前表/图/命题/补充：**[tab:weekly](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:261>)；[sup:selection](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:674>)；[sup:selection-failures](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:756>)。

**预测登记：**`R6.S1.R2` → `NOT_MET`（`notes/submission/prediction-register.json#/rows/3`）；`R6.S2.R2` → `NOT_MET`（`notes/submission/prediction-register.json#/rows/4`）；`R6.S3.R2` → `NOT_MET`（`notes/submission/prediction-register.json#/rows/5`）。

**已有数值/来源定位：**

- `old:9`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/9`；唯一CSV筛选 `{"source": "nyfed_weekly", "series_key": "PDPOSGS-B", "horizon": "24", "window": "52", "report": "R2"}`，字段 `percent_vs_F`；保存值 `181.39452368014167`。
- `old:39`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/39` → `results/supervisor-20261023/r6/assessment.json#/S3/R0_median_percent_vs_F`；保存值 `4.1510024714803695`。
- `old:40`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/40` → `results/supervisor-20261023/r6/assessment.json#/S1/median_percent_vs_F`；保存值 `5.374072481175762`。
- `old:41`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/41` → `results/supervisor-20261023/r6/assessment.json#/S3/R0_complete_count`；保存值 `26`。
- `old:42`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/42` → `results/supervisor-20261023/r6/assessment.json#/S3/R2_complete_count`；保存值 `26`。
- `new:51`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/51`。

**证据支持：**原CSV计数记录17次I；26格完整，三原success屏NOT_MET保持。

**必须保留的边界：**earlier R2 selector不同later RP；ordinary I不等于corrected F。

### C31｜简化conditioning、SAV/固定组合未达uniform weekly improvement

**主文位置：**[256](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:256>)。

**当前表/图/命题/补充：**[sup:wp2](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:793>)；[sup:wp2-pairs](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:855>)；[sup:wp3](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:899>)；[sup:wp3-murphy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:971>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:31`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/31` → `results/revision-20261023/v6/wp3-findings.json#/primary_context_rows/3/percent_vs_F`；保存值 `-3.9812983393045176`。
- `old:32`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/32` → `results/revision-20261023/v6/wp3-findings.json#/primary_context_rows/2/percent_vs_F`；保存值 `2.7730553886759823`。
- `text:submission-final/supplement.tex#section{Untuned forecast combinations}`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:899>)。

**证据支持：**补充完整loss/失败；保存wp3 findings正负例足以否定已测组合uniform改善。

**必须保留的边界：**不概括所有组合或所有conditional models无效。

### C32｜日度历史赢7/8；QR4 W260 H6 -2.97但37/30breaches

**主文位置：**[258](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:258>)。

**当前表/图/命题/补充：**[sup:v8-daily](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1328>)；[tab:daily-fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v8-daily-results-table.tex:3>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:98`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/98` → `results/revision-v8/wp4/summary.json#/classifications/QR33`。
- `old:99`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/99` → `results/revision-v8/wp4/summary.json#/classifications/QR4`。
- `old:100`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/100` → `results/revision-v8/wp4/summary.json#/contrasts/5/relative_loss_percent`；保存值 `-2.9739933765508653`。
- `old:101`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/101` → `results/revision-v8/wp4/summary.json#/cells/8/evaluation/strict_breach_count`；保存值 `37`。
- `old:102`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/102` → `results/revision-v8/wp4/summary.json#/cells/6/evaluation/strict_breach_count`；保存值 `30`。
- `old:103`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/103` → `results/revision-v8/wp4/summary.json#/contrasts/5/window`；保存值 `260`。
- `old:104`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/104` → `results/revision-v8/wp4/summary.json#/contrasts/5/horizon`；保存值 `6`。
- `old:105`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/105` → `results/revision-v8/wp4/summary.json#/contrasts/5/method`；保存值 `QR4`。
- `old:106`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/106` → `results/revision-v8/wp4/summary.json#/contrasts/5/reference_method`；保存值 `F`。

**证据支持：**两classification各4/4、3/4历史胜，exception方法/history/H/loss/hits完整。

**必须保留的边界：**同FX聚合非外部复制，评分改善伴更多breach。

### C33｜CFTC29/34达60%：两历史report事后较好者，corrected F固定另报

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[278](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:278>)；[280](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:280>)。

**当前表/图/命题/补充：**[tab:v10-cftc-contracts](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-cftc-contracts.tex:4>)；[fig:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:283>)。

**预测登记：**`E2.T1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/9`）。

**已有数值/来源定位：**

- `new:12`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/12` → `results/v10/cftc/summary.json#/predictions/T1/simple_better_cells`；保存值 `29`。
- `new:13`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/13` → `results/v10/cftc/summary.json#/predictions/T1/required_cells`；保存值 `34`。
- `new:14`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/14` → `results/v10/cftc/summary.json#/predictions/T1/minimum_inclusive_fraction`；保存值 `0.6`。
- `json:results/v10/cftc/summary.json#/contracts`：[results/v10/cftc/summary.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/summary.json>)，`#/contracts`。

**证据支持：**T1原判断支持29/34；完整contracts节点覆盖主表17代码×2histories×5方法的relative_loss_pct。

**必须保留的边界：**better realized history score不是可执行selector，主参考仍corrected F。

**P2风险：**摘要29/34未就近说明事后取corrected/ordinary较好者；不能当作单一实时可执行F的胜率。

### C34｜CFTC full两history median未达10%容忍，QR4长history更近历史

**主文位置：**[278](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:278>)；[283](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:283>)。

**当前表/图/命题/补充：**[tab:v10-cftc-contracts](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v10-cftc-contracts.tex:4>)；[fig:v10-cftc](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:283>)。

**预测登记：**`E2.T2.QR33` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/10`）；`E2.T3.QR4` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/11`）。

**已有数值/来源定位：**

- `new:15`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/15` → `results/v10/cftc/summary.json#/predictions/T2/median_pct_by_window/52`；保存值 `19.334715757564624`。
- `new:16`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/16` → `results/v10/cftc/summary.json#/predictions/T2/median_pct_by_window/260`；保存值 `10.34828178946443`。
- `new:17`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/17` → `results/v10/cftc/summary.json#/predictions/T2/status`；保存值 `NOT_SUPPORTED`。
- `new:18`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/18` → `results/v10/cftc/summary.json#/predictions/T3/W52_median_pct`；保存值 `10.280676300222424`。
- `new:19`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/19` → `results/v10/cftc/summary.json#/predictions/T3/W260_median_pct`；保存值 `0.2174917571722501`。
- `json:results/v10/cftc/summary.json#/contracts`：[results/v10/cftc/summary.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/summary.json>)，`#/contracts`。

**证据支持：**full19.3347/10.3483→T2不成立；QR4 10.2807/.21749→T3成立。

**必须保留的边界：**normalized percentages不恢复common-dollar portfolio风险，也非全部history单调收益。

### C35｜41短history weekly中27格selection过半、29格finite hindsight gap正

**主文位置：**[293](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:293>)；[298](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:298>)。

**当前表/图/命题/补充：**[fig:v12-decomposition](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:299>)。

**预测登记：**`F1.D1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/12`）；`F1.D2.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/13`）。

**已有数值/来源定位：**

- `v13:238`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/238` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/status`；保存值 `SUPPORTED`。
- `v13:239`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/239` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/planned_n`；保存值 `41`。
- `v13:240`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/240` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/complete_n`；保存值 `41`。
- `v13:241`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/241` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/support_n`；保存值 `29`。
- `v13:242`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/242` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/nonsupport_n`；保存值 `12`。
- `v13:243`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/243` → `results/v12/decomposition/predictions.json#/methods/QR33/D1/unavailable_n`；保存值 `0`。
- `v13:244`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/244` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/status`；保存值 `SUPPORTED`。
- `v13:245`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/245` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/planned_n`；保存值 `41`。
- `v13:246`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/246` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/complete_n`；保存值 `41`。
- `v13:247`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/247` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/support_n`；保存值 `27`。
- `v13:248`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/248` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/nonsupport_n`；保存值 `14`。
- `v13:249`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/249` → `results/v12/decomposition/predictions.json#/methods/QR33/D2/unavailable_n`；保存值 `0`。

**证据支持：**D1 29/41、D2 27/41且41完整；保存判定支持。

**必须保留的边界：**tested features/finite menu内的事后诊断。

**P2风险：**Why does regression lose 和 indicates limited incremental information 可能被读成因果/信息不存在；证据只提供菜单内诊断。

### C36｜decomposition5有限候选排除infinite，中位数不可加，2FXgap负

**主文位置：**[295](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:295>)；[299](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:299>)。

**当前表/图/命题/补充：**[fig:v12-decomposition](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:299>)；[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)。

**预测登记：**`F1.D3.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/14`）。

**已有数值/来源定位：**

- `v12:4`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/4` → `results/v12/decomposition/short-weekly-summary.json#/methods/QR33/median_actual_excess_pct`；保存值 `19.435259328148383`。
- `v12:5`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/5` → `results/v12/decomposition/short-weekly-summary.json#/methods/QR33/median_selection_component_pct`；保存值 `18.317455287977513`。
- `v12:6`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/6` → `results/v12/decomposition/short-weekly-summary.json#/methods/QR33/median_signal_gap_pct`；保存值 `4.370845028558574`。
- `v12:8`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/8` → `results/v12/decomposition/predictions.json#/D3/horizons/6/signal_gap_pct`；保存值 `-14.917351765503492`。
- `v12:9`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/9` → `results/v12/decomposition/predictions.json#/D3/horizons/24/signal_gap_pct`；保存值 `-3.7577697957958254`。
- `v12:30`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/30`；保存值 `5`。

**证据支持：**19.4353/18.3175/4.37085及2FXnegative gap字段可读；图保留unavailable cross。

**必须保留的边界：**非deployable selector/全模型下界/因果mechanism；component median不加总。

### C37｜CFTC长validation median19.33→4.03、10.35→.53，infinite增加

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)；[293](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:293>)；[304](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:304>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/补充：**[tab:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-validation-main.tex:2>)；[fig:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:34>)。

**预测登记：**`F2.V1.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/18`）；`F2.V2.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/19`）；`F2.V1.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/20`）；`F2.V2.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/21`）。

**已有数值/来源定位：**

- `v13:218`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/218` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/eligible_contracts`；保存值 `17`。
- `v13:219`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/219` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/complete_pair_count`；保存值 `17`。
- `v13:220`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/220` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/median_difference_pct_points`；保存值 `-15.304032374564795`。
- `v13:221`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/221` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/V1`；保存值 `SUPPORTED`。
- `v13:222`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/222` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/V2`；保存值 `SUPPORTED`。
- `v13:223`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/223` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/median_relative_loss_by_validation/52`；保存值 `19.33471575756462`。
- `v13:224`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/224` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/known_infinity_count_by_validation/52`；保存值 `4`。
- `v13:225`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/225` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/median_relative_loss_by_validation/156`；保存值 `4.030683382999826`。
- `v13:226`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/226` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/known_infinity_count_by_validation/156`；保存值 `10`。
- `v13:227`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/227` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/52/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `-1.3632221880984783`。
- `v13:228`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/228` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/eligible_contracts`；保存值 `17`。
- `v13:229`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/229` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/complete_pair_count`；保存值 `17`。
- `v13:230`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/230` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/median_difference_pct_points`；保存值 `-9.82319311344436`。
- `v13:231`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/231` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/V1`；保存值 `SUPPORTED`。
- `v13:232`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/232` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/V2`；保存值 `SUPPORTED`。
- `v13:233`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/233` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/median_relative_loss_by_validation/52`；保存值 `10.348281789464425`。
- `v13:234`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/234` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/known_infinity_count_by_validation/52`；保存值 `4`。
- `v13:235`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/235` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/median_relative_loss_by_validation/156`；保存值 `0.5250886760200655`。
- `v13:236`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/236` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/known_infinity_count_by_validation/156`；保存值 `5`。
- `v13:237`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/237` → `results/v12/validation-length/predictions.json#/methods/QR33/by_window/260/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `-4.328369835284372`。

**证据支持：**full W两臂threshold通过；QR4原4失败使2判定undetermined，保留。

**必须保留的边界：**arm median差不等于paired median；仍post-result。

### C38｜NY full长validation median6.68→-1.13、40.47→5.02，infinite增加

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)；[293](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:293>)；[302](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:302>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/补充：**[tab:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-validation-main.tex:2>)；[fig:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:34>)。

**预测登记：**`G2.V3.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/24`）；`G2.V4.QR33` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/25`）。

**已有数值/来源定位：**

- `v13:174`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/174` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/planned_sources`；保存值 `13`。
- `v13:175`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/175` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/complete_pair_count`；保存值 `13`。
- `v13:176`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/176` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/median_difference_pct_points`；保存值 `-7.812971755453957`。
- `v13:177`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/177` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/V3`；保存值 `SUPPORTED`。
- `v13:178`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/178` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/V4`；保存值 `SUPPORTED`。
- `v13:179`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/179` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/median_relative_loss_by_validation/52`；保存值 `6.684852366728319`。
- `v13:180`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/180` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/infinity_count_by_validation/52`；保存值 `6`。
- `v13:181`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/181` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/median_relative_loss_by_validation/156`；保存值 `-1.128119388725638`。
- `v13:182`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/182` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/infinity_count_by_validation/156`；保存值 `9`。
- `v13:183`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/183` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `0.0`。
- `v13:184`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/184` → `results/v13/nyfed-validation/summary.json#/methods/QR33/V3`；保存值 `SUPPORTED`。
- `v13:185`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/185` → `results/v13/nyfed-validation/summary.json#/methods/QR33/V4`；保存值 `SUPPORTED`。
- `v13:186`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/186` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/planned_sources`；保存值 `13`。
- `v13:187`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/187` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/complete_pair_count`；保存值 `13`。
- `v13:188`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/188` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/median_difference_pct_points`；保存值 `-35.45092255436495`。
- `v13:189`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/189` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/V3`；保存值 `SUPPORTED`。
- `v13:190`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/190` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/V4`；保存值 `SUPPORTED`。
- `v13:191`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/191` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/median_relative_loss_by_validation/52`；保存值 `40.470336525635894`。
- `v13:192`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/192` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/infinity_count_by_validation/52`；保存值 `3`。
- `v13:193`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/193` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/median_relative_loss_by_validation/156`；保存值 `5.019413971270939`。
- `v13:194`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/194` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/infinity_count_by_validation/156`；保存值 `9`。
- `v13:195`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/195` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/24/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `-44.09888415118933`。

**证据支持：**summary13sources/horizon完整，full G2 V3/V4 supported。

**必须保留的边界：**H6终点/refit phase也变，不是纯长度效应。

**P2风险：**摘要/intro泛称regression medians宜点明full版本；QR4 H6 median screen未达预定5pp。

### C39｜NYH6端点混杂/paired median0、QR4一屏失败及CFTC QR4缺失

**主文位置：**[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[304](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:304>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/补充：**[tab:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-validation-main.tex:2>)；[fig:v13-validation](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:34>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`G2.V3.QR4` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/26`）；`G2.V4.QR4` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/27`）；`F2.V1.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/20`）；`F2.V2.QR4` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/21`）。

**已有数值/来源定位：**

- `v13:183`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/183` → `results/v13/nyfed-validation/summary.json#/methods/QR33/by_horizon/6/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `0.0`。
- `v13:196`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/196` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/planned_sources`；保存值 `13`。
- `v13:197`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/197` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/complete_pair_count`；保存值 `13`。
- `v13:198`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/198` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/median_difference_pct_points`；保存值 `-4.2150390061995235`。
- `v13:199`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/199` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/V3`；保存值 `NOT_SUPPORTED`。
- `v13:200`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/200` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/V4`；保存值 `SUPPORTED`。
- `v13:201`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/201` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/median_relative_loss_by_validation/52`；保存值 `3.261142455403745`。
- `v13:202`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/202` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/infinity_count_by_validation/52`；保存值 `5`。
- `v13:203`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/203` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/median_relative_loss_by_validation/156`；保存值 `-0.9538965507957784`。
- `v13:204`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/204` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/infinity_count_by_validation/156`；保存值 `7`。
- `v13:205`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/205` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/6/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `0.0`。
- `v13:206`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/206` → `results/v13/nyfed-validation/summary.json#/methods/QR4/V3`；保存值 `NOT_SUPPORTED`。
- `v13:207`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/207` → `results/v13/nyfed-validation/summary.json#/methods/QR4/V4`；保存值 `SUPPORTED`。
- `v13:208`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/208` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/planned_sources`；保存值 `13`。
- `v13:209`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/209` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/complete_pair_count`；保存值 `13`。
- `v13:210`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/210` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/median_difference_pct_points`；保存值 `-18.670087236167987`。
- `v13:211`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/211` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/V3`；保存值 `SUPPORTED`。
- `v13:212`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/212` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/V4`；保存值 `SUPPORTED`。
- `v13:213`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/213` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/median_relative_loss_by_validation/52`；保存值 `24.88331399320492`。
- `v13:214`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/214` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/infinity_count_by_validation/52`；保存值 `4`。
- `v13:215`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/215` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/median_relative_loss_by_validation/156`；保存值 `6.213226757036931`。
- `v13:216`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/216` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/infinity_count_by_validation/156`；保存值 `9`。
- `v13:217`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/217` → `results/v13/nyfed-validation/summary.json#/methods/QR4/by_horizon/24/descriptive_complete_pairs/median_paired_change_pct_points`；保存值 `0.0`。
- `text:submission-final/generated/v13-supplement.tex#The original validation origins`：[submission-final/generated/v13-supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:30>)。

**证据支持：**paired median0；QR4H6 -4.21504pp未达-5；S38明确前移18周。

**必须保留的边界：**lower arm median非典型paired改善；length-only机制未识别。

### C40｜tau表所有完整值/NA，CFTC28胜1未知、两FX原比较无法判定

**主文位置：**[308](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:308>)；[311](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:311>)；[314](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:314>)；[315](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:315>)；[316](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:316>)；[317](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:317>)；[318](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:318>)；[321](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:321>)。

**当前表/图/命题/补充：**[tab:v12-tau](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:311>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`F3.Q1.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/22`）；`F3.Q2.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/23`）。

**已有数值/来源定位：**

- `v12:25`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/25` → `results/v12/tau/predictions.json#/Q2/denominator`；保存值 `2`。
- `v12:26`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/26` → `results/v12/tau/predictions.json#/Q1/support_count`；保存值 `28`。
- `v12:27`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/27` → `results/v12/tau/predictions.json#/Q1/denominator`；保存值 `34`。
- `v12:28`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/28` → `results/v12/tau/predictions.json#/Q1/unknown_count`；保存值 `1`。
- `v12:29`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/29` → `results/v12/tau/predictions.json#/Q1/minimum_support`；保存值 `29`。
- `v12:32`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/32` → `results/v12/tau/predictions.json#/descriptive_groups/5/descriptive_complete_row_median_relative_loss_pct`；保存值 `3.4457514725248743`。
- `v12:33`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/33` → `results/v12/tau/predictions.json#/descriptive_groups/0/descriptive_complete_row_median_relative_loss_pct`；保存值 `15.051220141144864`。
- `v12:35`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/35` → `results/v12/tau/predictions.json#/descriptive_groups/6/descriptive_complete_row_median_relative_loss_pct`；保存值 `1.5760649244213407`。
- `v12:36`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/36` → `results/v12/tau/predictions.json#/descriptive_groups/1/counts`。
- `v12:37`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/37` → `results/v12/tau/predictions.json#/descriptive_groups/7/descriptive_complete_row_median_relative_loss_pct`；保存值 `-10.145914078498187`。
- `v12:38`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/38` → `results/v12/tau/predictions.json#/descriptive_groups/2/counts`。
- `v12:39`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/39` → `results/v12/tau/predictions.json#/descriptive_groups/8/descriptive_complete_row_median_relative_loss_pct`；保存值 `-17.84939757113194`。
- `v12:40`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/40` → `results/v12/tau/predictions.json#/descriptive_groups/3/counts`。
- `v12:41`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/41` → `results/v12/tau/predictions.json#/descriptive_groups/9/descriptive_complete_row_median_relative_loss_pct`；保存值 `0.668087719819157`。
- `v12:42`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/42` → `results/v12/tau/predictions.json#/descriptive_groups/4/descriptive_complete_row_median_relative_loss_pct`；保存值 `44.22222331425766`。
- `v12:45`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/45` → `results/v12/tau/predictions.json#/Q1/status`；保存值 `UNDETERMINED`。
- `v12:46`：[notes/v12/new-paper-number-bindings.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v12/new-paper-number-bindings.json>)，`#/bindings/46` → `results/v12/tau/predictions.json#/Q2/status`；保存值 `UNDETERMINED`。

**证据支持：**完整组median或counts→NA；无successful-subset补值。H4已明确required numerical fits。

**必须保留的边界：**数值程序失败不等于观察经济损失/模型经济失败。

### C41｜G1保真6/10 gate失败，三原失败不替换、Q1/Q2仍未决

**主文位置：**[308](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:308>)；[322](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:322>)；[382](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:382>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/补充：**[tab:v12-tau](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:311>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`F3.Q1.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/22`）；`F3.Q2.QR33` → `UNDETERMINED`（`notes/submission/prediction-register.json#/rows/23`）。

**已有数值/来源定位：**

- `v13:0`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/0` → `results/v13/tau-repair/consistency.json#/status`；保存值 `FAIL`。
- `v13:1`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/1` → `results/v13/tau-repair/consistency.json#/n`；保存值 `10`。
- `v13:2`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/2` → `results/v13/tau-repair/consistency.json#/passed`；保存值 `6`。
- `v13:53`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/53` → `results/v13/tau-repair/summary.json#/consistency_gate`；保存值 `FAIL`。
- `v13:54`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/54` → `results/v13/tau-repair/summary.json#/original_Q1`；保存值 `UNDETERMINED`。
- `v13:55`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/55` → `results/v13/tau-repair/summary.json#/original_Q2`；保存值 `UNDETERMINED`。
- `v13:60`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/60` → `results/v13/tau-repair/summary.json#/repairs/0/cell_id`；保存值 `F3-cftc-33874A-original-H6-W260-V52-tau0.99`。
- `v13:61`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/61` → `results/v13/tau-repair/summary.json#/repairs/0/status`；保存值 `NOT_RUN_CONSISTENCY_GATE`。
- `v13:62`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/62` → `results/v13/tau-repair/summary.json#/repairs/0/reason`；保存值 `REPAIR_NOT_ADOPTABLE`。
- `v13:63`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/63` → `results/v13/tau-repair/summary.json#/repairs/1/cell_id`；保存值 `F3-fx-fx_hourly-original-H6-W2880-V1440-tau0.99`。
- `v13:64`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/64` → `results/v13/tau-repair/summary.json#/repairs/1/status`；保存值 `NOT_RUN_CONSISTENCY_GATE`。
- `v13:65`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/65` → `results/v13/tau-repair/summary.json#/repairs/1/reason`；保存值 `REPAIR_NOT_ADOPTABLE`。
- `v13:66`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/66` → `results/v13/tau-repair/summary.json#/repairs/2/cell_id`；保存值 `F3-fx-fx_hourly-early2015-H6-W2880-V1440-tau0.99`。
- `v13:67`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/67` → `results/v13/tau-repair/summary.json#/repairs/2/status`；保存值 `NOT_RUN_CONSISTENCY_GATE`。
- `v13:68`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/68` → `results/v13/tau-repair/summary.json#/repairs/2/reason`；保存值 `REPAIR_NOT_ADOPTABLE`。
- `v13:586`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/586` → `protocol/v13/tau-solver-repair-design.md#/consistency_max_pointwise_relative_error`；保存值 `1e-06`。

**证据支持：**G1 gate FAIL使3failed格NOT_RUN_CONSISTENCY_GATE，非3次新复估。

**必须保留的边界：**6/10是兼容保真检查，不是经济成功率；原NA保留。

### C42｜score≠breach；elementary curves crossing与H24约20.6:1 reversal

**主文位置：**[328](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:328>)；[368](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:368>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/补充：**[tab:fx](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:223>)；[sup:preference](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:465>)；[sup:wp3-murphy](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:971>)；[sup:v10-diagnostics](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1579>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:212`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/212` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/2/equality_alpha`；保存值 `86579744869851975/90776350660766843`。
- `old:213`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/213` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/2/horizon`；保存值 `24`。
- `old:214`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/214` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/2/right_method`；保存值 `rolling_S`。
- `old:215`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/215` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/0/relation`；保存值 `left_dominates`。
- `old:216`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/216` → `results/revision-20261022/preference-robustness/results.json#/headline_comparisons/1/relation`；保存值 `left_dominates`。
- `json:results/revision-20261022/preference-robustness/results.json#/headline_comparisons`：[results/revision-20261022/preference-robustness/results.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/revision-20261022/preference-robustness/results.json>)，`#/headline_comparisons`。

**原文献/规范：**[gw2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:445>)（https://doi.org/10.1111/j.1468-0262.2006.00718.x）；[ehm2016](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:439>)（https://doi.org/10.1111/rssb.12154）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**原精确fraction及horizon24字段可读，两个H6 left_dominates支持两个误差项降低。

**必须保留的边界：**20.6:1属于独立H24 reference，不属于H6 matched gain。

### C43｜成本J的reserve/breach/exceedance与mF归一化；illustrative非实测

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[48](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:48>)；[335](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:335>)；[336](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:336>)；[337](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:337>)；[338](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:338>)；[343](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:343>)；[380](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:380>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/补充：**[fig:v10-cost](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:346>)；[sup:v10-cost](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1554>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `new:61`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/new_and_added_bindings/61` → `results/v10/cost/manifest.json#/design/grid`。
- `text:submission-final/supplement.tex#The normalization uses evaluation-sample F headroom`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1641>)。

**证据支持：**正文式和S32/S36明示固定偏好与evaluation-sample归一化。

**必须保留的边界：**非事前institutional charges、真实profit或限额干预反事实。

### C44｜CFTC c1网格center5/34、两指定角32/34和1/34，趋势非处处单调

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[48](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:48>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)；[341](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:341>)；[342](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:342>)；[346](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:346>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/补充：**[fig:v10-cost](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:346>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `json:results/v10/cost/group-regions.json#/1016`：[results/v10/cost/group-regions.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/group-regions.json>)，`#/1016`。
- `json:results/v10/cost/group-regions.json#/1039`：[results/v10/cost/group-regions.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/group-regions.json>)，`#/1039`。
- `json:results/v10/cost/group-regions.json#/1062`：[results/v10/cost/group-regions.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/group-regions.json>)，`#/1062`。
- `json:results/v10/cost/summary.json#/unavailable`：[results/v10/cost/summary.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/summary.json>)，`#/unavailable`；保存值 `0`。

**证据支持：**精确rows1016(.01,5)wins1，1039(.1,.25)wins5，1062(1,0)wins32；planned34且lower=upper。

**必须保留的边界：**描述性related-task比例而非独立成功率；固定c网格，有局部非单调。

### C45｜RP六点菜单、156周/5760FX验证、pairedHAC1SE和corrected F默认

**主文位置：**[354](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:354>)。

**当前表/图/命题/补充：**[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)；[fig:v13-rp](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:358>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/generated/v13-supplement.tex#Selection and the gate share`：[submission-final/generated/v13-supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:39>)。
- `v13:588`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/588` → `protocol/v13/recommended-protocol-design.md#/predictions/R1/support_median_rp_relative_excess_pct_lte`；保存值 `1.0`。
- `v13:589`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/589` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/adverse_if_rp_relative_excess_pct_gt`；保存值 `10.0`。
- `v13:590`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/590` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/support_fraction_lte`；保存值 `0.05`。
- `v13:591`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/591` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/integer_threshold_if60`；保存值 `3`。

**原文献/规范：**[nw1987](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:476>)（https://doi.org/10.2307/1913610）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**S38给validation长度、候选选取与gate共用数据、decision评估段固定；G5保留design阈值。

**必须保留的边界：**1SE启发式，非名义显著性或benchmark保护概率。

### C46｜RP完整60weekly+2FX、median0vs14.63、fallback32、8不利/80.98最坏、FX保留

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[46](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:46>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)；[354](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:354>)；[357](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:357>)；[358](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:358>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/补充：**[fig:v13-rp](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:358>)；[tab:v13-routing](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:44>)。

**预测登记：**`G3.R1.RP` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/28`）；`G3.R2.RP` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/29`）；`G3.R3.RP` → `SUPPORTED`（`notes/submission/prediction-register.json#/rows/30`）。

**已有数值/来源定位：**

- `v13:255`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/255` → `results/v13/recommended-protocol/summary.json#/R1`；保存值 `SUPPORTED`。
- `v13:256`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/256` → `results/v13/recommended-protocol/summary.json#/R2`；保存值 `NOT_SUPPORTED`。
- `v13:257`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/257` → `results/v13/recommended-protocol/summary.json#/R3`；保存值 `SUPPORTED`。
- `v13:258`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/258` → `results/v13/recommended-protocol/summary.json#/planned_geometry_cells`；保存值 `62`。
- `v13:259`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/259` → `results/v13/recommended-protocol/summary.json#/received_rows`；保存值 `62`。
- `v13:260`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/260` → `results/v13/recommended-protocol/summary.json#/weekly/planned`；保存值 `60`。
- `v13:261`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/261` → `results/v13/recommended-protocol/summary.json#/weekly/eligible`；保存值 `60`。
- `v13:262`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/262` → `results/v13/recommended-protocol/summary.json#/weekly/excluded`；保存值 `0`。
- `v13:263`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/263` → `results/v13/recommended-protocol/summary.json#/weekly/complete`；保存值 `60`。
- `v13:264`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/264` → `results/v13/recommended-protocol/summary.json#/weekly/unavailable`；保存值 `0`。
- `v13:265`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/265` → `results/v13/recommended-protocol/summary.json#/weekly/median_relative_loss_pct`；保存值 `0.0`。
- `v13:266`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/266` → `results/v13/recommended-protocol/summary.json#/weekly/descriptive_complete_median_relative_loss_pct`；保存值 `0.0`。
- `v13:267`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/267` → `results/v13/recommended-protocol/summary.json#/weekly/worst_relative_loss_pct`；保存值 `80.98396986931891`。
- `v13:268`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/268` → `results/v13/recommended-protocol/summary.json#/weekly/ordinary_complete`；保存值 `60`。
- `v13:269`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/269` → `results/v13/recommended-protocol/summary.json#/weekly/ordinary_median_relative_loss_pct`；保存值 `14.627467605779144`。
- `v13:270`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/270` → `results/v13/recommended-protocol/summary.json#/weekly/ordinary_descriptive_complete_median_relative_loss_pct`；保存值 `14.627467605779144`。
- `v13:271`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/271` → `results/v13/recommended-protocol/summary.json#/weekly/adverse_gt10_count`；保存值 `8`。
- `v13:272`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/272` → `results/v13/recommended-protocol/summary.json#/weekly/fallback_count`；保存值 `32`。
- `v13:273`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/273` → `results/v13/recommended-protocol/summary.json#/weekly/regression_count`；保存值 `28`。
- `v13:274`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/274` → `results/v13/recommended-protocol/summary.json#/weekly/unknown_route_count`；保存值 `0`。
- `v13:275`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/275` → `results/v13/recommended-protocol/summary.json#/weekly/fallback_fraction_of_planned`；保存值 `0.5333333333333333`。
- `v13:276`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/276` → `results/v13/recommended-protocol/summary.json#/weekly/fallback_fraction_of_complete`；保存值 `0.5333333333333333`。
- `v13:588`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/588` → `protocol/v13/recommended-protocol-design.md#/predictions/R1/support_median_rp_relative_excess_pct_lte`；保存值 `1.0`。
- `v13:589`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/589` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/adverse_if_rp_relative_excess_pct_gt`；保存值 `10.0`。
- `v13:590`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/590` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/support_fraction_lte`；保存值 `0.05`。
- `v13:591`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/591` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/integer_threshold_if60`；保存值 `3`。

**证据支持：**60complete、32fallback、0median、14.6275ordinary、8adverse和80.98397worst；R1/R3通过，R2失败。

**必须保留的边界：**零median反映多数保留F，不是tail protection。

### C47｜benchmark-default中性标题；实务历史默认建议保留保护失败

**主文位置：**[353](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:353>)；[366](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:366>)；[392](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:392>)。

**当前表/图/命题/补充：**[fig:v13-rp](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:358>)；[sup:v13-checks](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/generated/v13-supplement.tex:10>)。

**预测登记：**`G3.R2.RP` → `NOT_SUPPORTED`（`notes/submission/prediction-register.json#/rows/29`）。

**已有数值/来源定位：**

- `v13:256`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/256` → `results/v13/recommended-protocol/summary.json#/R2`；保存值 `NOT_SUPPORTED`。
- `v13:267`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/267` → `results/v13/recommended-protocol/summary.json#/weekly/worst_relative_loss_pct`；保存值 `80.98396986931891`。
- `v13:271`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/271` → `results/v13/recommended-protocol/summary.json#/weekly/adverse_gt10_count`；保存值 `8`。
- `v13:589`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/589` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/adverse_if_rp_relative_excess_pct_gt`；保存值 `10.0`。
- `v13:590`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/590` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/support_fraction_lte`；保存值 `0.05`。
- `v13:591`：[notes/v13/G5-number-catalog.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v13/G5-number-catalog.json>)，`#/scalar_entries/591` → `protocol/v13/recommended-protocol-design.md#/predictions/R2/integer_threshold_if60`；保存值 `3`。

**证据支持：**H4已将protected标题改default；正文保护不足及结论tail失败一致。

**必须保留的边界：**不因改名消除8/60和worst80.98；不能宣称达到原tail目标。

### C48｜earlier weekly ordinary quantile最差比corrected F高36.5%

**主文位置：**[366](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:366>)。

**当前表/图/命题/补充：**[sup:rank](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:423>)；[sup:selection](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:674>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `old:44`：[notes/v10/main-number-audit.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.json>)，`#/old_archive_locator_checks/44`；唯一CSV筛选 `{"phase": "retro", "source": "nyfed_weekly", "series_key": "PDPOSGSC-L2", "horizon": "24", "window": "52", "report": "I"}`，字段 `percent_vs_F`；保存值 `36.50893744342638`。

**证据支持：**唯一CSV source/series/H/window/reportI字段36.508937。

**必须保留的边界：**特定earlier grid最差，不概括所有ordinary quantile都不可靠。

### C49｜观测被动路径，无causal/feature效果、prospective/individual-dealer复制或实测收益

**主文位置：**[18](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:18>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)；[376](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:376>)；[379](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:379>)；[380](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:380>)；[381](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:381>)；[394](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:394>)。

**当前表/图/命题/补充：**[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)；[sup:reproduction](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1583>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#The design gives no causal interpretation`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1633>)。
- `text:submission-final/supplement.tex#Individual-dealer external validation`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1608>)。

**证据支持：**设计范围、retrospective/vintage与未测成本支持这些未建立的边界。

**必须保留的边界：**不是成功预测行；同执行者Git replay不替代独立外部验证。

### C50｜原FX研究signed next-hour interval与本稿完整未来path peak响应不同

**主文位置：**[56](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:56>)；[66](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:66>)；[69](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:69>)。

**当前表/图/命题/补充：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:66>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**


**原文献/规范：**[wisniewski2020](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:482>)（https://proceedings.mlr.press/v128/wisniewski20a.html）；[wisniewski2024](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:484>)（https://pure.royalholloway.ac.uk/en/publications/net-position-and-retail-trader-behaviour-implications-for-market-/）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**以当前PMLR论文/博士论文原引用定位；响应差异是当前定义。

**必须保留的边界：**本轮未重新读全文；原文献不证明本稿性能更好。

### C51｜MaxVaR、payment deficit、settlement与dealer capacity/PnL文献定位

**主文位置：**[59](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:59>)；[70](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:70>)；[71](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:71>)。

**当前表/图/命题/补充：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:66>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**


**原文献/规范：**[boudoukh2004](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:429>)（https://pages.stern.nyu.edu/~rwhitela/papers/maxvar%20joim04.pdf）；[hoogen2017](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:480>)（https://resolver.tudelft.nl/uuid:1c0c4545-bb07-4916-aa37-1d4bea3b7872）；[petrunia2019](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:478>)（https://www.payments.ca/sites/default/files/tail_risk_in_the_automated_clearing_settlement_system_acss.pdf）；[arjani2020](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:417>)（https://www.payments.ca/sites/default/files/discussion_paper_monitoring_intraday_liquidity_risks_in_a_real_time_gross_settlement_system.pdf）；[duffie2023](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:437>)（https://doi.org/10.59576/sr.1070）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**每类目标/数据/评价指向对应原引用和当前literature表。

**必须保留的边界：**仅建立引用—主张路由，不伪称本轮阅读全文或完整方法等同。

### C52｜quantile/CAViaR/forest与proper/elementary scores是既有方法

**主文位置：**[50](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:50>)；[62](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:62>)。

**当前表/图/命题/补充：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:66>)；[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**


**原文献/规范：**[koenker1978](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:466>)（https://doi.org/10.2307/1913643）；[engle2004](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:441>)（https://doi.org/10.1198/073500104000000370）；[meinshausen2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:474>)（https://www.jmlr.org/papers/v7/meinshausen06a.html）；[gneiting2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:449>)（https://doi.org/10.1198/jasa.2011.r10138）；[ehm2016](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:439>)（https://doi.org/10.1111/rssb.12154）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**方法/评价概念以原引用与正文式为依据，无新经验预测。

**必须保留的边界：**不宣称新模型族或评价量发明。

### C53｜standard forecast tests、inventory-sensitive quoting动机与RQ框架

**主文位置：**[34](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:34>)；[36](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:36>)；[38](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:38>)；[40](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:40>)；[42](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:42>)；[50](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:50>)；[72](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:72>)；[76](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:76>)。

**当前表/图/命题/补充：**[tab:literature](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:66>)；[tab:methods](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:165>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**


**原文献/规范：**[dm1995](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:435>)（https://doi.org/10.1080/07350015.1995.10524599）；[gw2006](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:445>)（https://doi.org/10.1111/j.1468-0262.2006.00718.x）；[mcs2011](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:453>)（https://doi.org/10.3982/ECTA5771）；[avellaneda2008](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:419>)（https://doi.org/10.1080/14697680701381228）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**RQ是待回答问题；三finding实证由C22–C48分别映射，库存报价引用只作动机。

**必须保留的边界：**报价文献不证明本稿限额干预提高trading profit。

### C54｜FX源版权/获取/fingerprint，raw和private per-origin不分发

**主文位置：**[399](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:399>)。

**当前表/图/命题/补充：**定义/可用性陈述没有独立经验图表，直接指下面来源。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `text:notes/submission/availability-audit.md#- FX：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:5>)。
- `text:REPRODUCING.md#FX`：[REPRODUCING.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/REPRODUCING.md:35>)。

**原文献/规范：**[dataset](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:470>)（https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**H3档案区分可下载与再分发许可；保留rights holders条件和排除范围。

**必须保留的边界：**权限待作者确认；公开代码不意味着无授权输入者能完整独立复算。

### C55｜NY Fed源条款/Treasury snapshot，original panel不分发/新vintage不保原字节

**主文位置：**[401](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:401>)。

**当前表/图/命题/补充：**定义/可用性陈述没有独立经验图表，直接指下面来源。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `text:notes/submission/availability-audit.md#- New York Fed：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:6>)。

**原文献/规范：**[nyfeddata](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:443>)（https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**H3明确当前保存/缺失输入与source conditions，不沿用旧文暗示项目已有code license。

**必须保留的边界：**软件可用性不替代源数据条款。

### C56｜CFTC TFF已有公开原文件与URL/time/bytes/SHA回执

**主文位置：**[403](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:403>)。

**当前表/图/命题/补充：**定义/可用性陈述没有独立经验图表，直接指下面来源。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `json:data/cftc-tff/provenance.json#`：[data/cftc-tff/provenance.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/data/cftc-tff/provenance.json>)，`#`。
- `text:notes/submission/availability-audit.md#- CFTC：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:7>)。

**原文献/规范：**[cftcTFF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:433>)（https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm）。这里只定位当前原引用，不声称本轮重新读过全部全文。

**证据支持：**直接读现存provenance节点，未新下载或验证远端。

**必须保留的边界：**可检查原记录与独立重估全论文是不同状态。

### C57｜代码/协议/汇总与复现说明入口；fullreplay需原inputs和Git objects

**主文位置：**[405](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:405>)。

**当前表/图/命题/补充：**[sup:reproduction](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1583>)。

**预测登记：**不适用。36行登记没有这项旧结果/描述性或可用性陈述；不补造预测行，直接指保存结果/档案。

**已有数值/来源定位：**

- `text:notes/submission/availability-audit.md#- 代码：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:8>)。
- `text:notes/submission/availability-audit.md#- LICENSE：`：[notes/submission/availability-audit.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/availability-audit.md:10>)。
- `text:submission-final/supplement.tex#Full financial replay requires compatible inputs`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1595>)。

**证据支持：**H3区分公开可检查与有输入者replay；DOI/license仍占位。

**必须保留的边界：**未核对当前远端字节；同执行者新clone不等于外部独立dealer/researcher replication。

### C58｜state/target/backcast/S36/S40完整判定及失败入口

**主文位置：**[113](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:113>)；[220](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:220>)；[384](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/manuscript.tex:384>)。

**当前表/图/命题/补充：**[sup:wp4](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1017>)；[sup:wp5](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1078>)；[sup:v8-backcast](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1356>)；[sup:v12-details](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1622>)。

**预测登记：**不适用。定义/命题/方法/文献无对应经验预测阈值，依据所列命题、原引用或执行协议。

**已有数值/来源定位：**

- `text:submission-final/supplement.tex#The full-prefix backcast uses penalties`：[submission-final/supplement.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-final/supplement.tex:1627>)。
- `json:notes/submission/prediction-register.json#/adverse_context_records`：[notes/submission/prediction-register.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/submission/prediction-register.json>)，`#/adverse_context_records`。

**证据支持：**保存state/target/overlapping backcast完整入口；S40 consolidated register接全部36行及7个额外敏感性。

**必须保留的边界：**登记/链接不是额外实验或全部主张supported；S40最终表号另按编译aux核对。

## 覆盖与验证范围

- 58个主张组；157个主文源行显式映射；501个选用来源节点。当前叙述段落遗漏候选为0，所有主张有当前表/图/命题或具体来源定位。
- FX/weekly/tau表覆盖各行；CFTC主表完整contracts节点覆盖17代码、2history、5种相对F的方法字段；描述表另读回已有1324个numeric及100个table binding。只读保存字段与hash，不重算金融统计。
- 图表和公式延续行归属相应定义/命题组；结构标题、无事实过渡、作者/DOI/许可占位不当作已证实事实。
- 文献只建立原引用—主张路由，没有伪称本轮阅读全文；如原文不能支持更强解释，仍须回原文精读，不能以当前绑定记录代替。
- 不把related aggregate markets当独立dealer复制；全部NA/NOT_SUPPORTED/UNDETERMINED/NOT_TESTABLE与rights/input缺失边界保留。
- JSON包含全部来源SHA、当前段落SHA、真实JSON Pointer/唯一CSV筛选、原登记阈值和保存判定、覆盖索引。后续改稿必须刷新SHA和行号。
- S40是新增consolidated register入口，其最终节号/表号仍由根代理按编译辅助文件核对；本映射不冒称已有最终PDF验收。
