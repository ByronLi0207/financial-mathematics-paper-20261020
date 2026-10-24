# 全文写法修改日志（2026-10-23）

本轮以《导师写法修改指导-20261023.md》替代旧“30分钟精简摘要”任务，按第1–10步执行。只改文字、标签、图表说明和排版；没有实验或新的结果计算。基线提交：`0ebc6e54ee3682315670a641e8783fc15c3660f4`。

## 主线与术语（步骤1–2）

在这两类数据上，简单历史规则是难以打败的峰值预测基准；FX优势依参照和时期而变，周度回归经强收缩与保守选参后仍留损失，低分数可伴随更多破线。标题保持原样。内部代码的对应关系仅放附录C表格；方法名称、预先指定比较和早期时期均采用读者可理解的描述。

## 摘要（步骤3）

**原首句：** Three findings qualify conditional forecasts of two-sided absolute holding-period position peaks: FX gains depend on the historical reference and period.

**新首句：** Dealers monitor the largest absolute net position reached during a holding period.

**处理：** 动机→问题/两类数据→回答→三个发现→监测收束→唯一局限句。153词、10个数字；24步收益/交叉点、短窗口Treasury +144.3%与one-SE细节留结果节，去掉跟随数字的核验过程说明。main的332→376与matched的360→376没有混用。

## 引言、限制、建议与结论（步骤4–7）

引言和第二节总结统一为基准选择、周度损失与评分/破线分离。五项指定限制分别集中在摘要尾句/第5和9节、早期检验第7节、Table10表注、第9节及结论尾句。第8节每条给出建议及证据；结论121词，首句给主线、末句给唯一范围句。下文逐段列出具体改动。

## 结果写法与全文复核（步骤8–9）

第6–7节发现段先结论、再数值、再解释或图表定位；方法段直接交代设定。正文所有超过40词的句子已拆分。数学定义和陈列公式的前后引导与显示公式视为一个逻辑方法段；第8节按指导的“建议＋证据”结构写。第2–4、5、6、7、9节和附录A–C全部过完，没有因为时间原因跳过任何节。

## 正文逐段核对（第1节至结论）

以下按修订前段落编号；含公式的段落按原文本断点列出，公式另由指纹核对。每段均已先分类再阅读全文，列出的新首句来自实际修订稿。

### P01 · Introduction · 方法

**原首句：** Dealer inventories connect customer order imbalances to risk limits and balance-sheet capacity.

**新首句：** Dealer inventories connect customer order imbalances to risk limits and balance-sheet capacity.

**删减、移动与核对：** 保留库存经济动机及峰值与端点的区别；核对两处经济文献引用。

### P02 · Introduction · 方法

**原首句：** We ask when conditional quantile methods forecast a sampled absolute position peak better than simple historical rules.

**新首句：** We ask when conditional quantile methods forecast a sampled absolute position peak better than simple historical rules.

**删减、移动与核对：** 合并数据来源与问题，直接回答历史规则难以打败；保留上分位数的监测含义。

### P03 · Introduction · 方法

**原首句：** The comparison uses an hourly client-flow net-position record from one FX market maker and a weekly Treasury-bill net-position aggregate.

**新首句：** We ask when conditional quantile methods forecast a sampled absolute position peak better than simple historical rules. / Historical headroom and translated-path rules compete with ridge quantile regression and nearest-neighbour quantiles.

**删减、移动与核对：** 来源描述并入问题段；匹配设计与两项事先指定比较各用直接句定义。

### P04 · Introduction · 过程

**原首句：** The source-specific rankings motivate an exploratory sequence that separates update schedules, history lengths, predictor sets and penalty menus; the original comparisons remain the reference points.

**新首句：** Penalty expansion accounts for most of the Treasury score improvement in the ordered comparison.

**删减、移动与核对：** 删去引言里的过程预告；顺序比较改为第6节发现，具体步骤在Table7及附录C阶段表。

### P05 · Introduction · 发现

**原首句：** Three empirical findings define the contribution.

**新首句：** The paper makes three empirical points. / Second, weekly regression struggles against historical headroom. / Third, lower pinball loss need not mean fewer breaches.

**删减、移动与核对：** 拆为三项结论，各带原数值和图表定位；精确区分FX两个参照及周度面板与保守选参测试。

### P06 · Introduction · 限制/过程

**原首句：** The comparison is retrospective, and Section describes its information, statistical and decision limits.

**新首句：** The paper develops the target and methods before comparing forecast performance.

**删减、移动与核对：** 引言只留阅读路线；回溯与FX检视限制按指定位置集中于摘要、第5和9节。

### P07 · Related literature · 方法

**原首句：** Inventory research provides the economic motivation for position monitoring.

**新首句：** Inventory research provides the economic motivation for position monitoring.

**删减、移动与核对：** 保留三篇库存与中介背景；删去无新增信息的被动报告自我限定句。

### P08 · Related literature · 方法

**原首句：** Financial path extrema and liquidity buffers provide the closest target precedents.

**新首句：** Financial path extrema and liquidity buffers provide the closest target precedents.

**删减、移动与核对：** 逐项保留已有峰值/支付文献和目标差异；未加文献或优先权主张。

### P09 · Related literature · 方法

**原首句：** Conditional quantile forecasting and its evaluation use mature tools.

**新首句：** Conditional quantile forecasting combines regression with consistent scoring rules.

**删减、移动与核对：** 保留标准条件分位数与评分文献；用直接的方法与评分联系代替成熟性反复表态。

### P10 · Related literature · 发现

**原首句：** Relative to these studies, three findings concern a common two-sided absolute sampled peak rather than a signed endpoint, directional payment deficit or portfolio-value loss.

**新首句：** The comparison adds three empirical findings for a common sampled position peak.

**删减、移动与核对：** 统一为同样三点发现，删除末尾再次退回“只是应用”的限定；旧数值在正文结果段保留。

### P11 · Data and target · 方法/限制

**原首句：** The FX record contains hourly client-flow net positions for one market maker across five liquid currency pairs, as described by .

**新首句：** The FX record contains hourly client-flow net positions for one market maker across five liquid currency pairs, as described by .

**删减、移动与核对：** 保留来源、采样、单位和观察数；输入文件等同性未核实移至附录C来源段。

### P12 · Data and target · 方法

**原首句：** The Treasury input is New York Fed Primary Dealer Statistics series PDPOSGS-B, the aggregate Treasury-bill long position less the short position .

**新首句：** The Treasury input is New York Fed Primary Dealer Statistics series PDPOSGS-B, the aggregate Treasury-bill long position less the short position .

**删减、移动与核对：** 保留净额构造、观察数、周三日期、单位和FR2004计量口径；核对无数字修改。

### P13 · Data and target · 方法

**原首句：** The target includes the known issue position.

**新首句：** The target is the largest absolute position over the sampled holding interval.

**删减、移动与核对：** 先给目标定义再列原公式；包含当前头寸、记录时长和headroom定义均保留。

### P14 · Data and target · 发现

**原首句：** Figure illustrates why endpoint information can miss an intervening peak.

**新首句：** Endpoint marginals permit different peak distributions.

**删减、移动与核对：** 把有限例子的结论放前面，保留相同边际、不同依赖与不同峰值分布例子。

### P15 · Data and target · 方法

**原首句：** The information set enforces label completion before fitting.

**新首句：** The information set enforces label completion before fitting.

**删减、移动与核对：** 逐句核对完成标签训练时钟与重估索引，原陈列公式保持。

### P16 · Data and target · 方法

**原首句：** Every training response ends by (t) .

**新首句：** Every training response ends by (t) .

**删减、移动与核对：** 保留转换与系数冻结、当前query更新和标签成熟后可进入训练的时序。

### P17 · Forecasting methods · 方法

**原首句：** The historical rules differ in how they anchor completed episodes to the current issue.

**新首句：** The historical rules differ in how they anchor completed episodes to the current issue.

**删减、移动与核对：** 保留三种报告及秩定义，补齐F/S/K读者名称，公式不改。

### P18 · Forecasting methods · 方法

**原首句：** Rolling controls use the most recent completed episodes at every issue.

**新首句：** Rolling controls use the most recent completed episodes at every issue.

**删减、移动与核对：** 保留rolling/frozen集合及query锚点的区别；把段落与上一数学定义清楚分开。

### P19 · Forecasting methods · 方法

**原首句：** The original specification contains 33 predictors: the current signed level and preceding lagged levels, current magnitude, two past increment RMS measures, recorded hour and weekday sine/cosine pairs, and a gap indicator.

**新首句：** The original specification contains 33 predictors.

**删减、移动与核对：** 拆开长变量清单，定义RMS，保留33预测变量和lag范围；四变量说明从第6节移到此处。

### P20 · Forecasting methods · 方法

**原首句：** The spans are daily and weekly record counts in FX, and six and 26 records in Treasury.

**新首句：** The spans are daily and weekly record counts in FX, and six and 26 records in Treasury.

**删减、移动与核对：** 保留两个来源的RMS跨度、训练均值/尺度及标准化公式。

### P21 · Forecasting methods · 方法

**原首句：** An exactly constant predictor is centered at its repeated value and assigned scale one.

**新首句：** An exactly constant predictor is centered at its repeated value and assigned scale one.

**删减、移动与核对：** 保留常数特征处理与过去信息回看，用正面方法句表述lookback。

### P22 · Forecasting methods · 方法

**原首句：** Ridge quantile regression fits normalized headroom with an unpenalized intercept.

**新首句：** Ridge quantile regression (QR) fits normalized headroom with an unpenalized intercept.

**删减、移动与核对：** 首次定义QR缩写；保留目标、无惩罚截距、归一化和原优化公式。

### P23 · Forecasting methods · 方法

**原首句：** and issues C t QR =B t+ \ 0,s ( 0+z t, T )\ .

**新首句：** and issues C t QR =B t+ \ 0,s ( 0+z t, T )\ .

**删减、移动与核对：** 保留投影与原惩罚菜单；补充扩展菜单名称所指的既有强惩罚值，未改变候选集合。

### P24 · Forecasting methods · 方法

**原首句：** As , penalized slopes vanish and the unpenalized intercept approaches the set of empirical headroom-quantile minimizers.

**新首句：** As , penalized slopes vanish and the unpenalized intercept approaches the set of empirical headroom-quantile minimizers.

**删减、移动与核对：** 保留极限截距、分位数最优区间和两种秩；末句改成正面说明报告差异。

### P25 · Forecasting methods · 方法

**原首句：** Nearest-neighbour quantiles select standardized predictor rows by a group-balanced Euclidean distance and resolve equal distances by recency.

**新首句：** Nearest-neighbour quantiles (KNN) select standardized predictor rows by a group-balanced Euclidean distance and resolve equal distances by recency. / Plain KNN applies the corrected order statistic to selected headrooms.

**删减、移动与核对：** 拆成距离构造和报告构造两段，首次定义KNN；固定菜单的文件去向并入附录C。

### P26 · Forecasting methods · 方法/过程

**原首句：** Validation selects the lowest native-unit mean pinball loss and resolves an exact parameter tie toward the larger candidate.

**新首句：** Standard validation selects the lowest native-unit mean pinball loss.

**删减、移动与核对：** 保留最低损失、平局规则和候选完成条件；数值核验与完整执行清单集中附录C。

### P27 · Evaluation design · 方法/限制

**原首句：** The two source-specific main comparisons were declared before their conditional evaluation runs.

**新首句：** The two pre-specified comparisons use six-record horizons.

**删减、移动与核对：** 明确主比较参照和时点；保留FX先看过这一指定限制；执行冻结历史移附录C。

### P28 · Evaluation design · 方法

**原首句：** Mean score and breach frequency answer complementary questions.

**新首句：** Mean pinball loss measures forecast accuracy, while breach frequency records limit exceedances.

**删减、移动与核对：** 直接定义分数和两个误差金额，原分解公式不改。

### P29 · Evaluation design · 方法

**原首句：** A strict breach is P t,H >C t ; equality is a nonbreach.

**新首句：** A strict breach occurs when P t,H >C t ; equality counts as a nonbreach.

**删减、移动与核对：** 保留严格破线、等号非破线、单位和各自分母；把逐issue headroom与平均金额分清。

### P30 · Evaluation design · 方法/限制

**原首句：** Paired loss differentials support descriptive unconditional predictive-ability comparisons.

**新首句：** Paired loss differences compare unconditional predictive accuracy.

**删减、移动与核对：** 保留HAC统计量、带宽公式与原样本敏感性；HLN适用与长程方差假设集中附录C。

### P31 · Evaluation design · 过程/限制

**原首句：** We report the two previously declared source-specific primaries with unadjusted HAC p-values and a Bonferroni sensitivity across those two comparisons.

**新首句：** Apart from the two pre-specified comparisons, all p-values are exploratory and unadjusted unless stated.

**删减、移动与核对：** 按指导文件在第5节集中说明p值地位；Holm 71项置表注，旧72项来历置附录C。

### P32 · Evaluation design · 方法/限制

**原首句：** Coverage diagnostics use the single grid t 0+j(H+1) , anchored once at evaluation start.

**新首句：** Coverage diagnostics use the fixed grid t 0+j(H+1) , starting at evaluation onset.

**删减、移动与核对：** 保留非重叠grid与条件化的likelihood定义；小样本和floor-atom零假设细节移附录C。

### P33 · Results · 发现

**原首句：** Long-history regression improves the six-step FX score.

**新首句：** Long-history regression beats both six-step FX headroom references.

**删减、移动与核对：** 先报两个参照均赢，再给12.7%与14.8%；-5.2/-5.9统计量移附录C数值表。

### P34 · Results · 发现

**原首句：** Short-history regression has a much weaker six-step result.

**新首句：** Short-history regression offers little six-step improvement. / The short-history 24-step regression loses, even under the expanded penalty menu.

**删减、移动与核对：** 拆为弱六步收益与24步失败；保留2.12%、p=.54、+31.5%及同一惩罚参数。

### P35 · Results · 发现

**原首句：** The longer-horizon legacy gain is small and statistically imprecise.

**新首句：** The 24-step FX comparison gives a small, imprecise gain.

**删减、移动与核对：** 保留1.83%、p=.84、2017尾部集中和六步各年同向；去legacy内部叫法。

### P36 · Results · 发现

**原首句：** The original Treasury regression is less accurate than matched historical headroom.

**新首句：** Original Treasury regression loses to matched historical headroom. / The Treasury loss increase accompanies more breaches.

**删减、移动与核对：** 分开分数失利与破线增加；保留+50.8%、p=.008、28→54，.015敏感性移附录C。

### P37 · Results · 发现

**原首句：** Plain KNN at the short Treasury history reproduces F .

**新首句：** The plain nearest-neighbour forecast reproduces historical headroom at the short Treasury history.

**删减、移动与核对：** 保留全池恒等及12点grid反转、双方两次破线，使用完整方法名称。

### P38 · Results · 发现

**原首句：** Coverage diagnostics reinforce the original Treasury regression's adverse breach record.

**新首句：** Coverage diagnostics reinforce Treasury regression's adverse breach record.

**删减、移动与核对：** 把结论放前面，保留40/12点范围与Table5；小样本统计前提集中附录C。

### P39 · Results · 方法/过程

**原首句：** The exploratory sequence asks which procedural changes accompany the score differences.

**新首句：** The four-predictor specification uses current signed position, current magnitude and the two past RMS measures. / Penalty expansion accounts for most of the Treasury score improvement in the ordered comparison.

**删减、移动与核对：** 四变量定义移到方法节；顺序步骤由Table7/Figure2给出，正文直接写比较发现。

### P40 · Results · 过程

**原首句：** The original sequence combines two changes at its last step.

**新首句：** Penalty expansion accounts for most of the Treasury score improvement in the ordered comparison.

**删减、移动与核对：** 固定切分、菜单和候选核验去附录C；原与扩展菜单的差别保留在方法、Table6/7。

### P41 · Results · 发现

**原首句：** A wider penalty menu largely removes the original Treasury deterioration.

**新首句：** Penalty expansion accounts for most of the Treasury score improvement in the ordered comparison. / The two predictor sets give similar Treasury scores under the common menu.

**删减、移动与核对：** 保留50.8→3.43和1.24%、p=.685，删去等价性收回句；惩罚.001→1移附录C。

### P42 · Results · 发现

**原首句：** The FX gain persists under the wider menu: every selection and issued report agrees with the original full specification.

**新首句：** The FX gain survives the wider penalty menu.

**删减、移动与核对：** 保留10.9%及原调整p<.001；不再逐结果重复单变量非因果限定，统一放第9节。

### P43 · Results · 发现

**原首句：** The intercept-only reference helps locate the remaining Treasury differences.

**新首句：** Stronger Treasury shrinkage leaves the breach count above historical headroom.

**删减、移动与核对：** 保留主设定32vs28破线；普通截距四格及3/4菜单端点诊断移附录C，Table6全部原值不改。

### P44 · Results · 发现/过程

**原首句：** An additional panel reuses 12 previously archived New York Fed position series on the same economic-date grid, with all 48 horizon—history cells retained (Figure ).

**新首句：** Expanded-menu regression still loses in most additional weekly cells. / Menu expansion nevertheless reduces the typical weekly deterioration substantially. / Two of the three pre-set panel predictions fail.

**删减、移动与核对：** 拆成残留失利、改善幅度和预测未达三段；三项阈值与通过/失败数移附录C表。

### P45 · Robustness and score interpretation · 发现/方法

**原首句：** AR residual-block replay shows that family choice matters.

**新首句：** Residual replay adds a fitted conditional mean to historical path construction. / Residual replay improves some scores while increasing breaches. / Residual replay improves the main Treasury score against both historical references. / Residual replay also beats most Treasury regression reports.

**删减、移动与核对：** OLS/唯一转移/有序残差方法移第4节；保留所有AR收益和破线增加，分为三个结果段。

### P46 · Robustness and score interpretation · 发现/方法

**原首句：** Rank sensitivity changes the finite-sample convention.

**新首句：** The historical quantile rank changes both reports and rankings.

**删减、移动与核对：** 保留秩公式、短Treasury差异、相同全池下恒等和已有反转解释。

### P47 · Robustness and score interpretation · 发现

**原首句：** Loss reweighting distinguishes a robust linear gain from a narrow tradeoff.

**新首句：** The main FX gain improves both mean error amounts while increasing breaches. / The 24-step FX gain trades greater underprediction for less overprediction. / Both main comparisons change ranking across consistent quantile scores.

**删减、移动与核对：** 拆为金额与破线、24步权重反转、Murphy交叉；固定报告权重定义与20.6均保留。

### P48 · Robustness and score interpretation · 发现

**原首句：** Horizon diagnostics show that realized peaks and fitted reports have different ordering properties.

**新首句：** Fitted quantile reports can cross across horizons even though realized peaks increase.

**删减、移动与核对：** 保留29%交叉与抬高报告可增损的有限例子；去逐段归档说明。

### P49 · Robustness and score interpretation · 发现/方法/过程

**原首句：** Conservative selection on an earlier period.

**新首句：** The earlier-period exercise keeps the forecast target and uses shorter weekly histories. / The conservative one-standard-error rule favours stronger shrinkage when validation losses are close. / All three pre-set success criteria fail for this conservative rule. / Both the protection and median-improvement requirements fail. / Frequent selection of the intercept-only option coexists with large weekly losses. / The conservative rule also gives up more than half the eligible FX gain. / Rolling cross-validation produces two failed FX cells.

**删减、移动与核对：** 将长段拆成范围、规则、三项未达、截距选择和数值失败；52/1440、17/26、+5.4/+181.4、阈值、R0中位与两失败均保留。规则后设计的限制只留第7节。

### P50 · Robustness and score interpretation · 发现/过程

**原首句：** Retuning the original three-penalty QR structure on the earlier validation segment also qualifies replication (Table ).

**新首句：** The earlier FX period repeats the matched gain but reverses the rolling-reference comparison. / The earlier rolling-reference difference is statistically imprecise. / The earlier Treasury comparison retains the adverse regression direction.

**删减、移动与核对：** 先报匹配收益复现但rolling方向不复现，保留两个精确p和+144.3%；带宽与短窗口非260限制只在Table10注。

### P51 · Implications for position monitoring · 发现/建议

**原首句：** Keep a historical benchmark.

**新首句：** Benchmark against historical headroom.

**删减、移动与核对：** 改为明确匹配历史基准建议，证据限定为Treasury-bill全格与追加面板多数格，保留部分方法胜出的事实。

### P52 · Implications for position monitoring · 发现/建议

**原首句：** Default to conservative historical reports in short samples.

**新首句：** Default to corrected-rank headroom in short weekly samples.

**删减、移动与核对：** 保留短周度默认修正秩建议和+36.5%证据；删除阈值撤回句及重复保护保证限定。

### P53 · Implications for position monitoring · 发现/建议

**原首句：** Report error amounts and breach occasions together.

**新首句：** Report breaches with the score.

**删减、移动与核对：** 建议显示三项误差/破线信息；经济价值限制集中第9节。

### P54 · Discussion and limitations · 限制

**原首句：** Inspection and inference.

**新首句：** The comparisons describe forecasting performance within these records.

**删减、移动与核对：** 保留指定FX检视事实；HAC/重叠有效样本假设移附录C，停止逐结果重复。

### P55 · Discussion and limitations · 限制

**原首句：** Measurement and information timing.

**新首句：** The two data sources describe different dealer-position records.

**删减、移动与核对：** 保留单做市商客户流、交易商聚合、经济日期下载vintage和采样间运动的范围。

### P56 · Discussion and limitations · 限制/发现

**原首句：** Coverage and specification.

**新首句：** The comparisons describe forecasting performance within these records. / Forecast scores and breach counts answer different monitoring questions.

**删减、移动与核对：** 非因果与单预测变量作用只放第9节；coverage/economic范围同处集中，实际负结果在第6–7节保留。

### P56b · 第9节原经济价值段 · 限制

**原首句：** Decision value.

**新首句：** Forecast scores and breach counts answer different monitoring questions.

**删减、移动与核对：** 原段关于没有观察交易、对冲、抵押和融资决策，集中为第9节末句“未测经济收益”；结论最后一句保留同一范围。删除重复的“低分不能说明低融资成本”与政策反应扩展，未删除实测负结果。

### P57 · Discussion and limitations · 限制

**原首句：** The empirical object is a measured position magnitude; its connection to a particular inventory policy requires the corresponding decision setting.

**新首句：** 删除，无独立新段。

**删减、移动与核对：** 删除无新增信息的泛政策句；目标的计量性质在第3节定义，经济范围在第9节。

### P58 · Conclusion · 发现

**原首句：** Three findings qualify conditional forecasts of two-sided absolute holding-period peaks.

**新首句：** Simple historical rules are hard to beat when forecasting peaks of dealer net positions. / On weekly positions, stronger regularization narrows regression's gap, but 34 of 48 panel cells still lose.

**删减、移动与核对：** 第一句直接给主线；两FX参照、残留周度损失和评分/破线分离压为同样三点。

### P59 · Conclusion · 限制/过程

**原首句：** These retrospective comparisons apply established estimators to a sampled peak.

**新首句：** On weekly positions, stronger regularization narrows regression's gap, but 34 of 48 panel cells still lose.

**删减、移动与核对：** 成熟方法定位留引言，结论只保留最后一句两来源回溯、无coverage保证和未测经济收益。


## 正文四幅图的说明

### 正文 Figure 1 图注

**原首句：** An artificial sampled path distinguishes the issue magnitude, the holding-interval peak and the endpoint magnitude.

**新首句：** A sampled path separates the issue magnitude, holding-interval peak and endpoint magnitude.

**处理：** 图注改为显示对象与口径，最多三句；图文件及图内所有数据/文字保持原字节。原归档、内部任务标记或因果限定的重复句转附录C或第9节。

### 正文 Figure 2 图注

**原首句：** Ordered loss changes for the six-step comparisons.

**新首句：** Successive procedure changes in the six-step comparisons.

**处理：** 图注改为显示对象与口径，最多三句；图文件及图内所有数据/文字保持原字节。原归档、内部任务标记或因果限定的重复句转附录C或第9节。

### 正文 Figure 3 图注

**原首句：** All archived panel cells, each comparing original and expanded full regression against its own F .

**新首句：** Original and expanded-menu regression compared with matched historical headroom in every additional weekly panel cell.

**处理：** 图注改为显示对象与口径，最多三句；图文件及图内所有数据/文字保持原字节。原归档、内部任务标记或因果限定的重复句转附录C或第9节。

### 正文 Figure 4 图注

**原首句：** Mean underprediction ( U ), mean overprediction ( V ) and strict-breach changes for the named original comparisons.

**新首句：** Changes in underprediction amounts, overprediction amounts and strict breaches for the original comparisons.

**处理：** 图注改为显示对象与口径，最多三句；图文件及图内所有数据/文字保持原字节。原归档、内部任务标记或因果限定的重复句转附录C或第9节。

## 表格与附录逐段记录

# 表注与附录逐段写法日志（2026-10-23）

范围：只编辑 `manuscript/supervisor-revision/generated/*-table.tex` 共11份及 `appendices.tex`；summary/facts、图资产、实验代码和结果文件不动。冻结基线：`.scratch/writing-pass-20261023/before/manuscript/supervisor-revision/`。

## 原有附录段落逐项记录

### 基线 appendices.tex:2
- 原首句：`These elementary arguments concern a common nonempty historical set $J$, an available rank $1\le j\le |J|$ and real arithmetic.`
- 新首句：`The finite-array arguments use a common nonempty historical set $J$, an available rank $1\le j\le |J|$ and real arithmetic.`
- 处理/去向：方法条件直接设定；全部符号与假设保留。

### 基线 appendices.tex:5
- 原首句：`Define $A_i=B+P_i-B_i$, $T_i=\max_h|x+d_{i,h}|$ and the floor projection $\Pi_B(v)=\max(B,v)$.`
- 新首句：`Define $A_i=B+P_i-B_i$, $T_i=\max_h|x+d_{i,h}|$ and the floor projection $\Pi_B(v)=\max(B,v)$.`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:10
- 原首句：`The second bound follows by applying the reverse triangle inequality to every path point, then taking the maximum and applying the floor projection.`
- 新首句：`The second bound follows by applying the reverse triangle inequality to every path point, then taking the maximum and applying the floor projection.`
- 处理/去向：拆开阶统计非扩张性的长句；证明步骤保留。

### 基线 appendices.tex:15
- 原首句：`where $R_{\rm abs}=\max_{i\in J}|B-B_i|$ and $R_{\rm signed}=\max_{i\in J}|x-N_i|$.`
- 新首句：`where $R_{\rm abs}=\max_{i\in J}|B-B_i|$ and $R_{\rm signed}=\max_{i\in J}|x-N_i|$.`
- 处理/去向：删除重复范围提醒，保留共同样本/秩条件及两种得分排序均可能的结论。

### 基线 appendices.tex:18
- 原首句：`Put $v_i=-\ell_i\ge0$.`
- 新首句：`Put $v_i=-\ell_i\ge0$.`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:23
- 原首句：`The branches agree at zero.`
- 新首句：`The branches agree at zero.`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:27
- 原首句：`Symmetric envelopes, $u_i=v_i$, suffice for equality of $F_J$ and $S_J$.`
- 新首句：`Symmetric envelopes, $u_i=v_i$, give $F_J=S_J$.`
- 处理/去向：充分条件直接写为等式成立条件；数学 analogue 换明确描述；不等式不动。

### 基线 appendices.tex:29
- 原首句：`Equal absolute anchors can still leave a translated-path gap.`
- 新首句：`Equal absolute anchors can still leave a translated-path gap.`
- 处理/去向：保留全部符号、数值与反例。

### 基线 appendices.tex:32
- 原首句：`Fix $d>0$ and an available corrected rank for a pool of size $n$.`
- 新首句：`Fix $d>0$ and an available corrected rank for a pool of size $n$.`
- 处理/去向：保留相同历史产生相反得分排序的完整例子。

### 基线 appendices.tex:34
- 原首句：`Report order can also differ across constructions.`
- 新首句：`Report order can also differ across constructions.`
- 处理/去向：保留全部数值、辅助分位数和构造排序。

### 基线 appendices.tex:37
- 原首句：`Fix arbitrary $c,\phi$ and define residuals $\epsilon_s=N_{s+1}-c-\phi N_s$.`
- 新首句：`Fix arbitrary $c,\phi$ and define residuals $\epsilon_s=N_{s+1}-c-\phi N_s$.`
- 处理/去向：establishes 改 gives；递推与恒等式保留。

### 基线 appendices.tex:42
- 原首句：`Taking absolute maxima and using the reverse triangle inequality gives`
- 新首句：`Taking absolute maxima and using the reverse triangle inequality gives`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:47
- 原首句：`For $0\le\phi\le1$, the coefficient is $1-\phi^H$; at $\phi=1$ the paths coincide.`
- 新首句：`For $0\le\phi\le1$, the coefficient is $1-\phi^H$; at $\phi=1$ the paths coincide.`
- 处理/去向：代数关系直接表述；情景代表性与时序信息条件保留。

### 基线 appendices.tex:49
- 原首句：`Horizon order alone leaves score effects unresolved.`
- 新首句：`Horizon order alone leaves score effects unresolved.`
- 处理/去向：保留跨期限强制排序恶化得分的反例和0.45。

### 基线 appendices.tex:52
- 原首句：`The current-magnitude predictor satisfies $B_i=\mu_{\kappa B}+\sigma_{\kappa B}z_{i,\kappa B}$ under the stated transform.`
- 新首句：`The current-magnitude predictor satisfies $B_i=\mu_{\kappa B}+\sigma_{\kappa B}z_{i,\kappa B}$ under the stated transform.`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:57
- 原首句：`Positive homogeneity of pinball loss implies that multiplying the objective in \eqref{eq:qr} by $s_\kappa$ gives`
- 新首句：`Positive homogeneity of pinball loss implies that multiplying the objective in \eqref{eq:qr} by $s_\kappa$ gives`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:63
- 原首句：`The issued report is $\max\{B_t,\alpha+z_{t,\kappa}^{\mathsf T}\theta\}$.`
- 新首句：`The issued report is $\max\{B_t,\alpha+z_{t,\kappa}^{\mathsf T}\theta\}$.`
- 处理/去向：保留参数化、投影降损及平移分位数；删末尾泛化/校准提醒；总体限制由主文第9节集中表述。

### 基线 appendices.tex:66
- 原首句：`For a threshold $\eta$, the elementary score for forecast $c$ and outcome $p$ is`
- 新首句：`For a threshold $\eta$, the elementary score for forecast $c$ and outcome $p$ is`
- 处理/去向：方法段全部保留。

### 基线 appendices.tex:70
- 原首句：`\citet{ehm2016} represents quantile-consistent scores as nonnegative mixtures of these elementary scores under the appropriate regularity conditions.`
- 新首句：`\citet{ehm2016} represents quantile-consistent scores as nonnegative mixtures of elementary scores under the stated regularity conditions.`
- 处理/去向：描述性名称替换 primary/audit；全断点、正负号和经验上非一致占优保留。

### 基线 appendices.tex:78
- 原首句：`Figure~\ref{fig:lambda} extends the penalty grid for the two original six-step long-history settings.`
- 新首句：`The penalty paths show that greater shrinkage can raise or lower evaluation loss.`
- 处理/去向：先说收缩可提高也可降低评估损失；保留固定验证选择和截距区间；执行去向集中C首段。

### 基线 appendices.tex:86
- 原首句：`Table~\ref{tab:old} retains the original historical-rule grid. $R$ is the symmetric-increment-envelope rule and $C^{\rm floor}=B$ is the issue-floor report.`
- 新首句：`Nearest-state retrieval improves its native-peak reference but still loses to the stronger historical headroom and translated-path rules.`
- 处理/去向：先说最近状态检索仍败给强历史规则；保留构造和符号；菜单/月度/区块输出去向集中C首段。

### 基线 appendices.tex:92
- 原首句：`The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020}{repository} separates frozen original results, new exploratory results and document sources.`
- 新首句：`The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020}{repository} links the original comparisons, subsequent diagnostics and document sources to their specifications.`
- 处理/去向：与旧C末段合并；来源映射、编译及完整不利/失败输出去向只在C首段集中说明。

### 基线 appendices.tex:94
- 原首句：`Exact recomputation requires the pinned source snapshots, model specification and code.`
- 新首句：`Exact recomputation uses the pinned source snapshots, model specification and code.`
- 处理/去向：吸收原第3节FX输入文件等同性未验证；保留来源条款、公私边界与下载版本差异。

### 基线 appendices.tex:96
- 原首句：`The original ridge optimizer uses two-block ADMM \citep{boyd2011}.`
- 新首句：`The original ridge optimizer uses two-block ADMM \citep{boyd2011}.`
- 处理/去向：接受条件直接表述；吸收表6八格/40候选完成与四预测变量核对；保留ADMM及截距区间例子。

### 基线 appendices.tex:98
- 原首句：`E1--E4 form a later exploratory supplement.`
- 新首句：`The split between the two main comparisons and the remaining 71 matched contrasts was chosen after observing results.`
- 处理/去向：拆入数值接受段、五阶段表、Holm来历段和代码表；内部ID仅在附录表格可见。

### 基线 appendices.tex:100
- 原首句：`The former long coverage-evidence table, full loss-weight frontiers, machine diagnostics and execution histories remain in their original repository paths.`
- 新首句：`The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020}{repository} links the original comparisons, subsequent diagnostics and document sources to their specifications.`
- 处理/去向：并入C首段；不利格、原文件身份、长表和编译输出说明集中一次。

## 原有表注与图注逐项记录

### generated/coverage-table.tex
- 原caption首句：`Six-step coverage diagnostics on the fixed nonoverlap grid.`
- 新caption首句：`Six-step coverage diagnostics on the fixed nonoverlap grid.`
- 原表注首句：`POF uses every retained hit.`
- 新表注首句：`POF uses every retained hit; IND and CC condition on the first hit and use the subsequent transitions in both likelihoods.`
- 处理/去向：1句caption+2句表注；POF全网格、IND/CC首hit条件似然保留；旧初始化、稀疏网格与地板原子口径移C。

### generated/data-table.tex
- 原caption首句：`Source-specific chronological budgets.`
- 新caption首句：`Source records and chronological validation and evaluation periods, with issue dates and common evaluation origins across horizons.`
- 原表注首句：`FX has 1,440 validation and 6,625 evaluation issues; Treasury has 52 and 277.`
- 新表注首句：`FX has 1,440 validation and 6,625 evaluation origins; Treasury has 52 and 277.`
- 处理/去向：1句caption+2句表注；样本数、标签完成与记录间隔保留；日期和全部数据不动。

### generated/decomposition-table.tex
- 原caption首句：`Ordered six-step changes ending at the original main comparisons.`
- 新caption首句：`Ordered six-step loss changes from historical rules to original regression.`
- 原表注首句：`Step percentages use the preceding row's loss and compound.`
- 新表注首句：`Step percentages use each preceding loss and compound; initial percentage points share the chain's starting loss and add.`
- 处理/去向：1句caption+2句表注；Four+/33+/Original 33改描述名称，Change列换行；阶梯分母/共同起点、菜单回退与未调整口径保留；分组去向移C。

### generated/e3-table.tex
- 原caption首句：`Penalty-menu expansion and the intercept-only reference.`
- 新caption首句：`Regression loss changes (percent) relative to frozen $F$ under the expanded penalty menu; selected penalties and breaches describe expanded-menu regression.`
- 原表注首句：`Plus denotes the common menu $\{.001,.01,.1,1,10\}$.`
- 新表注首句：`Expanded-menu and four-predictor regressions each select from $\{.001,.01,.1,1,10\}$; original regression retains its smaller menu.`
- 处理/去向：1句caption+2句表注；模型表头展开，文字列换行。八格/40候选、复用核对和28比较分组移C；I/F秩口径保留。

### generated/earlier-table.tex
- 原caption首句：`Original historical construction grid; mean FX losses in USD millions.`
- 新caption首句：`Historical construction grid, with mean FX losses in USD millions.`
- 原表注首句：`Each sensitivity changes one factor from the original six-step setting.`
- 新表注首句：`Each row changes one factor from the original six-step setting while retaining its evaluation origins; quantile preferences define separate tasks.`
- 处理/去向：1句caption+2句表注；合并单因素/共同起点；保留tau90的+0.000舍入方向；附录表内原setting标签允许保留。

### generated/fx-table.tex
- 原caption首句：`FX original reports, matched by horizon and history.`
- 新caption首句：`FX forecasts matched by horizon and history, with mean pinball losses in source-reported USD millions.`
- 原表注首句：`Every relative change uses its own frozen $F$. $^{*}$Primary, unadjusted HAC p-value (Treasury QR at the main setting).`
- 新表注首句：`Relative changes use each report's frozen $F$; conditional p-values use Holm over the remaining 71 matched conditional-versus-$F/S/K$ contrasts.`
- 处理/去向：1句caption+2句表注；保留frozen F分母、71比较Holm、p=1恒等格与破折号；71/72分组来历移C。

### generated/literature-table.tex
- 原caption首句：`Closest studies and the present comparison.`
- 新caption首句：`Related studies: targets, data, methods and evaluation evidence.`
- 原表注首句：`Van den Hoogen (2017) specifies coverage and independence tests in Section 5.4; detailed application results in Section 5.5 are confidential, while Chapter 7 provides public out-of-sample summaries.`
- 新表注首句：`Van den Hoogen (2017) specifies coverage and independence tests in Section 5.4; detailed application results in Section 5.5 are confidential, while Chapter 7 provides public out-of-sample summaries.`
- 处理/去向：caption说明文献内容；所有文献数据格与可访问性表注保留。

### generated/r6-primary-table.tex
- 原caption首句：`Earlier-period QR comparisons. $\Delta$ is mean pinball relative to the stated reference; positive is worse.`
- 新caption首句：`Earlier-period six-step regression compared with matched and rolling historical rules.`
- 新表注首句：`Positive $\Delta$ denotes higher mean pinball loss; the weekly comparison has \RWritingWeeklyN{} origins and the common FX period has \RWritingFXN{} (about \RWritingFXWeeks{} calendar weeks).`
- 处理/去向：原长caption拆为1句caption+2句表注；起点数/周数、带宽7/未调整留此；三点菜单所选两项λ移C。短窗口与原W=260比较的区别仅留本表注；第一列增宽防W=52断行。

### generated/robustness-table.tex
- 原caption首句：`Compact robustness summary; the complete original outputs are retained.`
- 新caption首句：`Robustness checks for residual replay, quantile ranks, loss weights and horizon ordering.`
- 处理/去向：caption说明检查内容；删除完整输出去向句并集中C；QR33+展开，所有不利计数保留。

### generated/treasury-table.tex
- 原caption首句：`Treasury original reports, matched by horizon and history.`
- 新caption首句：`Treasury forecasts matched by horizon and history, with mean pinball losses in source-reported USD millions.`
- 原表注首句：`Every relative change uses its own frozen $F$. $^{*}$Primary, unadjusted HAC p-value (Treasury QR at the main setting).`
- 新表注首句：`Relative changes use each report's frozen $F$; conditional p-values use Holm over the remaining 71 matched conditional-versus-$F/S/K$ contrasts, except the marked unadjusted Treasury main comparison.`
- 处理/去向：1句caption+2句表注；保留frozen F分母、71比较Holm、星号未调整主比较、p=1与破折号；71/72来历移C。

### generated/uv-table.tex
- 原caption首句：`Error components and strict breaches for the original named comparisons.`
- 新caption首句：`Error components and strict breaches for the original comparisons.`
- 原表注首句：`A is regression and B its named reference.`
- 新表注首句：`A denotes regression and B its stated historical reference; amounts are source-reported USD millions, and negative differences favor regression.`
- 处理/去向：1句caption+2句表注；primary/legacy改main comparison/24-step comparison；第一列换行；单位、方向、交叉与固定报告偏好保留。

### 附录图注 fig:murphy
- 原首句：`Elementary-score differences for the two original primaries, regression minus its declared reference.`
- 新首句：`Elementary-score differences for the two main comparisons, with regression minus its stated historical reference.`
- 各3句，写内容与口径；过程去向集中C；图资产不动。

### 附录图注 fig:lambda
- 原首句：`Elementary-score differences for the two original primaries, regression minus its declared reference.`
- 新首句：`Elementary-score differences for the two main comparisons, with regression minus its stated historical reference.`
- 各3句，写内容与口径；过程去向集中C；图资产不动。

### 原有记号表caption
- 原首句与新首句相同：`Notation used in the comparison and appendices.`
- 全部记号数据格原样保留。

## 迁入C的内容与新增表

- 原§3 FX输入精确等同性未验证 → C来源段。
- 原§5的71/72分组来历、HAC serial/LRV、HLN用于pinball的近似 → C分组/推断段。
- 原§5的Treasury 40/12稀疏网格、floor-atom nominal null与旧CC混合初始化 → C推断段；表5保留当前一致条件似然。
- 原§6 FX −5.2/−5.9 → C数值迁移表。
- 原§6 Treasury主比较HAC p=.008/两比较Bonferroni p=.015，以及原e3-summary中选定penalty .001→1 → C数值迁移表。
- 原e6-summary的ordinary-I Treasury −2.0%、+3.2%、+6.2%、+2.4%和上端点3/4 → C数值迁移表。
- 原e5-summary的P1=30/45/阈值40、P2=24/48/阈值36、P3=33/48/阈值25 → C代码/判定表，结果依次unsupported、unsupported、supported，定义来自原冻结预测。
- 原时期选参结果用于开发、前后各2个rolling-CV失败 → C五阶段表；四失败均保留。
- C代码表集中R0–R3、S1–S3、E3、E5、E6、R6、33+/Four+/Original 33、P1–P3，附录正文采用描述名称。
- 五阶段表记录历史构造、初始条件比较、回归/面板诊断、较早时期选参、原时期开发/写作顺序。
- B→C从强制分页改为仅FloatBarrier，保留全部数学、图、表。

## 检查与排版记录

- 11表共92行；589个未改名列单元格逐字节/顺序一致（初次500个检查未包含部分首列；后补全）。仅豁免decomposition的Change列、robustness的Interpretation列、uv与较早期表的描述性行标签。逐表证据见 `writing-pass-table-verification.json`。
- 9个显示数学块与基线完全相同；6个图SHA-256完全相同；原summary/facts逐字节相同。
- 11表caption+note合计均≤3句；附录两图注各3句。可见项目代码仅在C代码表；LaTeX交叉引用标签保持原名。
- Tectonic --only-cached预编译输出仅在`.scratch/writing-pass-20261023/caption-appendix-check/`：正文/参考文献14页+附录5页，共19页。唯一TeX警告为references.tex:82的underfull hbox；参考文献不在本代理范围。
- 已看110dpi第8、9、12、18、19页：文字表头、Change列和C新增表均未见重叠/裁切；表10第一列增宽后已再次编译/渲染检查，W=52完整保留同一行，C新增数值行也已复查。根代理负责最终全文编译及全部改页核验。

## 待用户决定

- Figure 2的原图像内仍有Four+、33+、Orig. 33等代码。用户同时要求不改图及代码仅在附录表可见，两条在此冲突；按保守原则原图不动，C代码释义表解释旧标签。未自动重绘或增加分析。

## 最后数字范围修正

- C代码表P2行将协议中明确的数字区间改写为 `within the pre-set band around F`，避免把改前论文未显示的区间数值带入本轮；24/48、阈值36及unsupported结论不变。本次仅改这一处论文措辞；未重新计算结果。
- 更新日志和核验JSON前，已分别保留同名`.bak`备份；P2/P3定义来源映射改为仅记录仍显示的P3阈值。


## 贡献说明同步

# 贡献说明写作修订记录（2026-10-23）

范围：只改 `notes/supervisor-20261023/CONTRIBUTIONS.md`；论文正文、代码、结果、图和 Git 均未由此任务修改。依据为本轮已保存的摘要、引言贡献段和原结果；未新增拟合、计算或分析。

| 段落 | 原首句 | 新首句 | 删减或移动 |
|---|---|---|---|
| 定位 | 这是采用成熟方法的实证比较与模型验证论文。 | 这是采用成熟方法的实证比较与模型验证论文。 | 随后直接写“历史规则很难打败”的三点主线；保留文献核对范围。 |
| 第一项中文一句话 | 将预测对象统一为包含当前持仓的双侧绝对采样峰值，并匹配完成标签、历史长度和更新安排后，条件模型的增益随数据与设定而异，不能由端点预测的成功直接推出。 | 预测双侧绝对持仓峰值时，FX 回归在原期和更早期分别比匹配历史规则降损 14.8% 和 16.6%，但更早期比短历史滚动规则增损 3.2%，原来相对该滚动规则的收益没有复现。 | 将原第二项的更早期 FX 证据移到第一项；明确 matched 与 rolling 两个固定参照。 |
| 第一项英文一句话 | On a common sampled absolute-position-peak target, comparisons with matched completed-label histories and refit schedules show that conditional gains depend on the data and specification. | Historical rules are a hard benchmark for sampled position peaks: FX regression lowers matched loss by 14.8% in the original period and 16.6% in the earlier period, but its earlier loss rises 3.2% against the short-history rolling rule, reversing the original comparison's gain. | 先给发现，再给数字；保留原峰值目标、文献证据和非因果范围。 |
| 第一项证据 | 目标是 \(P_{t,H}=\max_{0\le h\le H}\|N_{t+h}\|\)，不是 \(N_{t+H}\) 的区间；FX 的 H6/W2880 匹配历史比较相对 frozen F 降损 **14.767%**，原 Treasury H6/W260 则增损 **50.786%**。 | 目标是 \(P_{t,H}=\max_{0\le h\le H}\|N_{t+h}\|\)，包含当前持仓；比较匹配已完成标签、历史长度和更新安排。 | 原 Treasury 50.786% 移到第二项；保留 FX 14.767% 与正文 14.8% 的显示对应，保留所有文献和链接。 |
| 第二项中文一句话 | 扩大岭惩罚菜单缓解周度恶化，但在这次短周度验证和评估中，包括 one-SE 在内的选择规则仍未稳定守住历史基准。 | 周度 Treasury 主比较增损 50.8%，扩大岭惩罚菜单虽减小损失，12 条附加序列仍有 34/48 格败给历史 headroom，而另一个涵盖 13 条周度序列、26 格的更早期测试中，保守选参仍留下大额损失。 | 把 12-series/48-cell panel 与 13-series/26-cell selection test 分开。 |
| 第二项英文一句话 | Expanding the ridge menu mitigates weekly deterioration, but selection on the short weekly validation samples, including a paired-loss one-SE rule, does not reliably preserve the historical benchmark in the subsequent evaluation. | Weekly regression loses 50.8% in the Treasury main comparison, and wider penalties leave 34 of 48 cells across 12 further series behind historical headroom, while conservative selection still permits large losses in the separate earlier test of 26 cells across 13 weekly series. | 避免把原主比较损失扩大为所有 conditional methods 都输。 |
| 第二项证据与实务范围 | 原 Treasury primary 的超额损失由 50.8% 降至 3.4%。 | 原 Treasury H6/W260 回归相对匹配历史规则增损 50.786%，对应正文的 50.8%；扩大菜单后为 3.4%。 | 保留原所有 panel 负预测、保守规则的三项失败标准和全部数值；用描述性名称代替逐数字附带的内部代号。保留 I/rank、重叠标签、无独立复制及无切换阈值说明，并指出部分 expanded regression 和 AR 有收益。 |
| 更早期 Treasury | 更早的 2015 年 FX 比较还说明参照不能混用。 | 更早期 Treasury H6/W52 短窗口版本增损 144.3%，延续原比较的恶化方向。 | FX 证据已移第一项；W52 不能替代 W260 的范围及原结构结果链接仍保留。 |
| 第三项中文一句话 | 在这些归档预测中，较低的 0.95 pinball 损失可以伴随更多破线，且分数偏好的改变会改写排序，因此模型结论须同时报告误差金额、破线次数和评分敏感性。 | 较低的 0.95 pinball 损失可以伴随更多破线，FX 主比较为 376 对 332、匹配比较为 376 对 360，模型评估因此须同时报告误差金额、破线次数和评分敏感性。 | 直接并列两组 breach 的参照口径；保留 1.83%、20.6、Murphy 曲线交叉及原链接。 |
| 第三项英文一句话 | In these archived forecasts, lower 0.95 pinball loss can coexist with more breaches and score-dependent rankings, so forecast assessment must jointly report error amounts, breach occasions and scoring sensitivity. | Lower 0.95 pinball loss can accompany more breaches, with 376 versus 332 in the FX main comparison and 376 versus 360 in the matched comparison, so forecast assessment should report error amounts, breach counts and scoring sensitivity together. | 移除不影响结果的过程修饰，保留 fixed-report weights 与 fixed-quantile Murphy 的区别。 |
| 审稿质疑与“不是创新” | 增量是目标、比较控制和上述三项带数字的发现。 | 增量是目标、比较控制和上述三项带数字的发现。 | 保留四项质疑、既有方法归属、原 FX inspection、2015 的本项目核对范围、两条失败预测和经济价值边界；缩短数字后反复附带的过程文字。 |
| 待用户决定 | 仅提供标题备选，正式标题未改。 | 标题备选，待用户决定；正式标题未改。 | 用两个体现“历史基准难打败”的候选替代旧候选；补记图内旧标签冲突及原图字节保留、正文描述性名称、Appendix C 表映射的处理。 |

旧标题备选（仅作修改历史，不再列为当前待选）：*Forecasting Sampled Position Peaks: Stronger Shrinkage and Persistent Benchmark Gaps*；*Conditional Position-Peak Forecasts: Shrinkage, Historical Rules and Breach Risk*。

检查：原 14 个链接定义全部保留；三条中文与三条英文一句话均在；原全部 panel 负预测、保守选参失败、+144.3% 短窗口结果和 +3.2% FX 反转仍在。此记录只说明该贡献文件的改写，不代表论文最终稿已经完成全稿核查。


## 自查与交付（步骤10）

写法统计见 `writing-pass-before.json` / `writing-pass-after.json`；数字清单见 `writing-pass-numbers-before.json` / `writing-pass-numbers-after.json`，原始对比和独立逐表对齐说明分别保存。数字出现次数可因删除重复句、描述性标签和内容移动而减少；每个保留数值均需对应修订前证据，原表数值逐格检查。

最终PDF正文含参考文献14页、附录5页；19页均已渲染逐页目检。没有未通过的交叉引用或图表溢出。具体输入哈希、数值检查、视觉检查与Git交付见 `writing-pass-verification.json`。

## 待用户决定

1. 正式标题未改，备选：*Forecasting Dealer Position Peaks: Historical Rules as a Hard Benchmark*；*Historical Benchmarks for Dealer Position Peaks: Conditional Gains and Breach Tradeoffs*。
2. Figure 2、Figure 3 的图内仍有旧模型缩写。按“不改图”的明确要求，本轮保留全部图资产原字节；正文、表头、图注使用描述性名称，附录C表格解释旧标签。将来若要连图内标签也统一，需要另行允许改图；这项例外没有隐瞒为图内零代码。
