# revision-v10b 中文交付记录

记录UTC：2026-10-25T04:18:27.716388+00:00。科学基线：`23fd9fa8c8659efd038a91c3b23d634fa15b0ce0`；工作分支：`revision-v10b`。本轮是投稿写作与显示打磨：没有新模型、新数据、新预测、重新评分、bootstrap、调参或实验。科学归档的2,077个受保护文件无变化；主稿两张内联结果表的数据行逐字节相同，六图的全部实际绘图数组及生成表的数值显示均保留。

当前本地投稿材料与30文件原生源包已完成编译、现有全套测试和53页逐页视觉验收。**发布尚未执行**；远端HEAD、远端/本地tree一致性、发布回执与全程用时在本文末尾保留 `PENDING_ROOT_FILL`。这份记录不表示已正式投稿，也不代填作者声明。

## 文件与版本

- 主稿：`submission-v10/manuscript.pdf`，19页（本轮上限20页）。
- 补充材料：`submission-v10/supplement.pdf`，32页（原33页；本轮上限33页）。
- 标题页：`submission-v10/title-page.pdf`，1页。
- Cover letter：`submission-v10/cover-letter.pdf`，1页。
- 原生LaTeX源包：`submission-v10/overleaf-package.zip`，30个成员，包含引用依赖及figure legends；ZIP SHA-256：`2185437b6d9ec280d51f47904be6f020fe5c30c98d0b4df0da4a218054a847e8`。
- 最终主稿源SHA-256：`52efe9156b504e9142b511fcace861d6c89e3b30235c564cb06ef08027735112`。各PDF的当前SHA与编译时间以 `final-native-build.json` 为准；该最终回执覆盖早期开发版或显示报告中的旧PDF SHA。

## 摘要 before / after

使用同一个冻结的写法计数器；before仅把原TeX转义去掉，没有改词。after直接抽取当前 `submission-v10/manuscript.tex`，并与 `abstract-after.txt` 一致。所谓数字数是原计数器的numeric occurrences，不是独立科学结果数；结构数量17也计入after的8个词元。

|指标|Before|After|
|---|---:|---:|
|摘要词数|164|161|
|数字词元数|18|8|
|本轮要求|至多180词|通过|
|数字要求|至多8个|通过|

### Before全文（164词，18个数字词元）

Dealer peak-position forecasts improve with conditioning only in some samples and under specific benchmarks. Matched FX regression lowers loss by 14.8% and 16.6% across two retrospective periods. Against the original shorter rolling reference, earlier loss rises by 3.2%; the earlier Treasury short-history comparison rises by 144.3%. We compare matched forecasts, independent reporting systems and limit-cost rankings. Historical rules beat expanded regression in 34 of 48 additional weekly comparisons. In 17 related CFTC dealer-category futures series, F or I beats regression in 29 of 34 comparisons. Regression's median excess losses are 19.3% and 10.3% across the two histories. The 90% model confidence set retains matched historical rules in 90 of 98 comparisons, usually alongside alternatives. On fixed calibrated paths, allowing stronger penalties and I reduces short-history median losses from 116.2% and 121.4% to 0.2% and -0.2%. Parameter switching misses the registered additional-loss threshold. Limit-cost rankings change with reserve, breach-frequency and exceedance charges. Peak-limit validation therefore needs matched references, complete tuning procedures and separate error-cost components.

### After全文（161词，8个数字词元）

Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules using hourly FX positions, weekly New York Fed positions and dealer aggregates in 17 CFTC futures markets. Histories and update schedules are matched. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8% and 16.6% across two periods, but its ranking against a shorter rolling rule changes. Second, historical rules beat regression in 34 of 48 New York Fed comparisons and 29 of 34 CFTC comparisons. They usually remain in the model confidence set alongside alternatives. In calibrated simulations, expanding the penalty menu cuts the constant-parameter median excess loss from 116.2% to near zero; the registered switching increment is unsupported. Third, in CFTC, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor expanded regression. The evidence is retrospective, and the original FX evaluation period had been inspected beforehand.

摘要保留三个发现，按FX匹配与参考敏感性、周度历史控制/菜单解释、成本偏好方向的顺序；最后一句明确回溯证据及原FX时段曾被查看。把参考说法“parameter switching adds no material loss”收紧为“the registered switching increment is unsupported”，因为M2未过门槛不能证明无效应或等价。

## 成本方向与三个已归档点

固定 `c=1`、比较 `CFTC::QR33` 与匹配历史F。读取已有 `cheaper=True` 标记，不重算成本、损失或金额。每个点的分母都是17个合约×两个历史窗口（52、260）=34个相关合约/历史比较。

|点的选择|kappa|beta|严格较便宜|等价|完整/计划|
|---|---:|---:|---:|---:|---:|
|已归档两轴按排序位置取中心|0.1|0.25|5/34|0|34/34|
|较高预留费、较低固定破线费角点|1|0|32/34|0|34/34|
|相反角点|0.01|5|1/34|0|34/34|

方向是较高kappa、较低beta时，扩展回归更常较便宜，**并非单调**。唯一产生个体逆向边的单元是`cftc:090741, W260`；提高kappa有9条True→False相邻边，提高beta有2条False→True相邻边，聚合计数也有3处逆向。因而五处统一保留generally和local exceptions / not monotone，不写成普遍比较静态、真实经营节约或最优政策。

`primary-regions.csv`与ZIP member在该切片的2,142条记录逐字段一致；63个点各有34个完整比较，无未知或等价。完整字段及两表行号在`cost-reading.json#/two_file_match/row_bindings`，三点在`#/examples`，例外在`#/monotonicity`。读取前后所有源SHA相同：

- `results/v10/cost/primary-regions.csv`：`7ff19bb457ed3b1f839ffdb596452742f03f20fd0ae90f00aaadb3d2444df651`。
- `results/v10/cost/cost-grid.csv.zip`：`b453c12cb8e8c4332a3ab180bbdfe899156a5a426d8a94a98dcf21967b265fa1`。

### 当前成本小节全文

公式的ASCII转写：`J_m(kappa,beta,c) = kappa*mean(C_m-B)/m_F + beta*mean(1{Y>C_m}) + c*mean((Y-C_m)_+)/m_F`，其中`m_F=mean(C_F-B)>0`、`beta=b/m_F`。以下解释恰三句，Figure 4对应正文成本区域图：

For CFTC, higher reserve coefficients and lower fixed-breach coefficients generally favor expanded-menu regression over matched historical headroom, although the grid is not monotone (Figure 4).
At c=1, regression is strictly cheaper in 5/34 comparisons at the sorted-grid centre (kappa,beta)=(.1,.25), 32/34 at (1,0), and 1/34 at the opposite corner (.01,5).
These are illustrative costs, not observed operating costs; Supplement Section S32 gives the normalization, fixed grid and complete-method results.

### 当前Introduction贡献3全文

Third, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC. The direction has local exceptions (Figure 4). Lower scores therefore need not mean lower limit costs, and validation should report reserve amounts, breach counts and exceedance amounts together.

### 当前Conclusion的RQ3全文

For RQ3, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC, with local exceptions. Lower forecast scores therefore need not imply lower limit costs. Validation should report reserve amounts, breach counts and exceedance amounts together, using the cost regions in Figure 4.

五处一致性覆盖摘要、Introduction三贡献、§2结尾、Conclusion及letter。MCS写成通常与其他方法共同保留，没有写成独占最优；其90/98保留与2/98 sole literal historical method在既有结果中分开。M2为−0.43471629487539243个百分点，未达到注册+5点额外损失门槛；全文保留经验低频机制未识别与非等价边界。

## 写法计数前后与实际取舍

计数器SHA未改：`1d02af83b5715e857490559a9b7c4e829dfc5bcef38ac96a55fe45343c0e6657`。相同范围为Introduction至Conclusion，排除浮动表图、展示公式、参考文献与声明；摘要/图注另报。未靠修改分句规则、禁词表或分母消除警报。

|冻结字段|Before|After|要求/解释|
|---|---:|---:|---|
|正文句数|318|287|删除重复结果复述，合并部分过渡|
|正文词数|3670|3513|相同计数范围|
|flagged句数|10|10|未减少也未隐藏|
|flagged比例|3.145%|3.484%|均不超过8%；分母减小导致比例略升|
|平均句长|11.541|12.240|均不超过20词|
|超过40词句数|0|0|均为0|
|primary正文出现|1|1|至多3次|
|主图caption禁词|0|0|保持0|
|旧额外FORBIDDEN原始计数|0|5|after均是正确的Supplement S1/S2/S3定位，原JSON仍保留false|

三项本轮写法门槛通过：flagged≤8%、平均≤20、没有>40词句。旧额外`no_forbidden_body`不能笼统写成PASS：新增的5个命中来自`Supplement Sections S1–S2`、`Figures S1–S2`和`Sections S3–S5`的精确交叉引用，而非已禁的成功标准代号；见`checker-interpretation.md`和`writing-final.json#/forbidden_detail`。

正文五个关键位置按同一顺序写三发现；结果重复按同一结果身份核对，含不同精度14.8/14.77等，不把窗口、日期、模型维度、坐标刻度、结构分母或巧合同数误删。主结果数字通常只留结果表和摘要/结论之一；成本三点只在成本正文一次完整列出。过渡围绕“参考变化→其他报告系统→菜单诊断→成本解释”，未新增科学发现。

## 图、表和补充材料变化

- 四张主图和两张Murphy图以矢量PDF重绘；保留全部实际坐标、连线、误差区间、热图矩阵、合约顺序及原曲线比例。主方法采用Okabe–Ito蓝/紫，历史规则灰黑，另加空/实心、圆/菱形、虚/实线的冗余编码。成本色阶为单调白到蓝，清楚标0–1。六图普通色彩、三类CVD及灰阶显示均经过检查。
- 主图在最终刊印宽度重画，最小普通文字约8.40–8.60pt，endpoint约8.53pt；Murphy约9.06pt。图例移出数据区域，成本全部beta刻度保留并旋转；没有靠遮挡或删刻度压缩。自然数学下标可更小，不能与普通文字混作同一字号。
- CFTC主表按小数点对齐并使用可读方法名；menu中位数/四分位数保持两位；MCS主表计数与一位小数百分比固定宽度。完整MCS保留976个原p值、全部NA和损失类上标、41个原方法身份及完整legend；密集审计矩阵仍为7.1pt并支持PDF放大，没有声称与主稿正文同字号。
- 补充材料保留S1–S34全部科学节和全部表/输入；加入可点击目录、精确主稿交叉引用、通俗化表头，正式caption/note不超过三句。完整MCS前置方法说明及完整legend的科学段落按正文处理，未把它们伪称短note。
- 12段行政审计/运行元数据逐字移入`notes/v10b/supplement-audit-records.md`；设计、随机流/种子、失败、历史信息时点、阈值、缺失与不可复现边界留在科学补充中。23段内联表数据及所有原输入身份保留。
- 菜单续页只重复表头，避免重复caption/label；原/新失败的NA、FAILED、31/32状态仍在。MCS竖排短方法名、三位小数、上标类ID与完整M01–M41 legend均在最终渲染可读。Murphy的FX横轴为USD millions、Treasury为USD billions，两张纵轴均为dimensionless，保留原Treasury显示的0.001比例。
- 最终补充32页，比原33页少1页；主稿19页、letter1页，未删除科学不利结果以满足页限。最终四文档53页逐页检查已通过；开发版或早期PDF SHA不作为最终验收依据。

## 最终验收与文件SHA

|目标|页数/上限|PDF SHA-256|最终逐页结果|
|---|---:|---|---|
|manuscript|19/20|`1cf6d4be5110d60a6e54bc5f2184bd7b0e022870eefff677aff9963479dade47`|PASS_ALL_PAGES|
|supplement|32/33|`f5ba558efb33e21477a9747e1a7bb7ac3708f00f43d17756e5bcb8a89f443d2e`|PASS_ALL_PAGES|
|title-page|1/1|`827ca5def4a96221abbd20c51112e254d9231af657a5b94caab16640089601c9`|PASS_ALL_PAGES|
|cover-letter|1/1|`c7a61d62f3f1c22818c0f484f25f742165a3f22839baebc53ae35be3236bb6d6`|PASS_ALL_PAGES|

最终原生构建无Overfull、无未解析引用、无重复label；补充材料18条Underfull提示保留为排版提示，不当成科学失败。最终源包30个成员与编译依赖一致；参考文献及bib未变。六关键词，running title为“Historical Rules and Peak Limits”，含空格32字符；作者占位和数据/代码声明保留，代码链接指向revision-v10b。

已有全套测试：**1,715 passed、1,181 subtests passed**。这是已有测试套件，不是重跑任何研究实验。`final-package-check.json`状态PASS，科学变化列表为空；`main_inline_result_rows_byte_identical`包括`tab:fx`、`tab:weekly`，六图arrays exact及generated table values preserved均为true。

## 实际时间回执（UTC，不冒充active工时）

以下只列已有文件中的实际时间戳。阶段工作窗口互相交叠；不能把并行人员的窗口相加当成总用时，也不能把一次读取/编译的时间等同整项人工工作。根任务将补`timing.json`的阶段workspan并更新这一表；没有独立起止回执的项目保留待填。

|项目|已有UTC回执|已证实的耗时/性质|阶段workspan|
|---|---|---|---|
|0 基准、分支与科学封存|science-seal.json：2026-10-25T03:57:24.184895+00:00|仅完成时间；无可据此推算的active分钟|PENDING_ROOT_FILL|
|1 摘要与三发现|writing-before：2026-10-25T03:55:11.885507+00:00；writing-final：2026-10-25T04:14:59.302528+00:00|两个全稿计数快照，非摘要专项起止|PENDING_ROOT_FILL|
|2 成本只读读出|2026-10-25T03:56:52.503961+00:00 → 2026-10-25T03:56:53.337846+00:00|脚本归档读取约0.834秒，非整项工作时长|PENDING_ROOT_FILL|
|3 五处同序、RQ逐项回答|当前稿及prose-consistency-review已核对|无独立起止回执，不估填分钟|PENDING_ROOT_FILL|
|4 逐段写法与数字去重|writing-final：2026-10-25T04:14:59.302528+00:00|冻结计数完成时间，非全阶段起止|PENDING_ROOT_FILL|
|5 图表显示与色盲/字号核对|visual-style-report及最终PDFscale回执|图表任务并行；没有本记录可据的独立active计时|PENDING_ROOT_FILL|
|6 Supplement目录、审计移文与页限|supplement-check及最终build|开发检查与最终32页已有记录；阶段起止待根归并|PENDING_ROOT_FILL|
|7 期刊格式、refs、letter|jof-guide-check：2026-10-25 UTC|仅核对日期，不能据此编造分钟|PENDING_ROOT_FILL|
|8 测试|2026-10-25T04:00:39.082082+00:00 → 2026-10-25T04:02:49.546315+00:00|130.464711秒，实际测试进程wall time|PENDING_ROOT_FILL|
|8 最终原生编译：manuscript|2026-10-25T04:13:19.403783+00:00 → 2026-10-25T04:13:23.647810+00:00|编译实际UTC起止；不含此前写作|见timing.json待补|
|8 最终原生编译：supplement|2026-10-25T04:13:23.651075+00:00 → 2026-10-25T04:13:30.461357+00:00|编译实际UTC起止；不含此前写作|见timing.json待补|
|8 最终原生编译：title-page|2026-10-25T04:13:30.466384+00:00 → 2026-10-25T04:13:30.801360+00:00|编译实际UTC起止；不含此前写作|见timing.json待补|
|8 最终原生编译：cover-letter|2026-10-25T04:13:30.801696+00:00 → 2026-10-25T04:13:31.145349+00:00|编译实际UTC起止；不含此前写作|见timing.json待补|
|8 全53页视觉整合|2026-10-25T04:15:23.520221+00:00|最终视觉验收完成时间|PENDING_ROOT_FILL|
|8 最终包验收|2026-10-25T04:16:41.971557+00:00|最终本地包检查完成时间|PENDING_ROOT_FILL|
|总历时/阶段重叠归并|PENDING_ROOT_FILL|不能由并行窗口求和，也不推算active分钟|PENDING_ROOT_FILL|

## Pending、发布与compare

以下保持明确待办，不把写作打磨当成投稿或商业/科学认证：

- 作者姓名、机构、联系方式、ORCID、funding、competing interests及AI声明保持原占位；真实投稿前由作者提供并完成。本轮没有登录投稿平台或提交。
- Journal of Forecasting当前官方认证分区仍为“未核实”；本轮按官方作者指南核对格式，不声称已确认分区、录用或可代作者提交。
- 原FX及私有逐点向量的权利、访问和安全回放仍由作者决定；公开包不包含受限观测或私有逐点轨迹。
- M2的边界、成本非单调、MCS非独占最优及相关任务非独立都保持；文档/图形一致性不是独立重算、因果识别、真实成本收益或外部复现。
- 旧额外禁词raw flag保留为5并逐项解释，未改冻结checker；18条Underfull与7.1pt密集MCS矩阵的显示边界如实保留。

|发布核对项|状态|
|---|---|
|仅revision-v10b提交/发布回执|PENDING_ROOT_FILL（本记录生成时尚未发布）|
|最终本地commit|PENDING_ROOT_FILL|
|远端revision-v10b HEAD|PENDING_ROOT_FILL|
|本地/远端HEAD与tree相等|PENDING_ROOT_FILL|
|受保护旧分支/refs与网页历史核对|PENDING_ROOT_FILL|
|timing.json、每项最终workspan及总历时|PENDING_ROOT_FILL|

固定compare链接：[基线23fd9fa…revision-v10b](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/compare/23fd9fa8c8659efd038a91c3b23d634fa15b0ce0...revision-v10b)。该链接当前只是固定比较入口；只有根任务完成发布并回读远端后，才可填入远端已一致的结论。

## 证据索引

摘要全文与计数：`abstract-before.txt`、`abstract-after.txt`、`writing-before.json`、`writing-final.json`。成本字段/行号/SHA：`cost-reading.json`及`cost-reading.md`。显示数值和输入SHA：`visual-style-report.json/.md`。补充移文与保留理由：`supplement-audit-records.md`、`supplement-metadata-decisions.md`。最终原生PDF/页PNG/SHA：`final-native-build.json`；全部53页最终核对：`final-visual-all-pages.json`；本地整包总验收：`final-package-check.json`；待作者决定事项：`PENDING.md`。本记录优先使用最终native-build和package回执，不用开发版替代最终版。
