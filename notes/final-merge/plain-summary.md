# 引言与结果的逐段外行概括

由同一执行者逐段阅读并写成；不是新增审稿人或跨模型复核。

范围包含引言、结果、历史机制与成本四节的全部叙述段；表格、图注和公式另作数字与图形检查。每条绑定实际段落 SHA-256，覆盖情况由脚本核对。

## I01 — sec:intro

限额要防的是两次检查之间的最高持仓，所以期末回落并不能说明期间没有超限。

Source paragraph SHA-256: `65fe858c349d27273ee62e59f989223689aaef67c69d221ccd724a686199b60e`.

> Position limits must cover exposure between reviews, since a position that finishes inside a limit can still breach it earlier. An endpoint forecast therefore answers a different question from a peak forecast, motivating comparisons on the largest sampled absolute net position.

## I02 — sec:intro

复杂模型估计更多关系也会消耗有限历史，因此实务上应检验它能否胜过明确的历史基准。

Source paragraph SHA-256: `a866b2e2eab53a039e417e249e5aea2bd41acbdcf6a1e48a2e3ce926b03e31cf`.

> Conditional models use recent position states and calendar information to adapt a limit, but their estimated relationships consume a finite history. A historical rule estimates fewer relationships and can remain competitive, making improvement over an explicit historical benchmark the relevant practical question.

## I03 — sec:intro

研究比较一家外汇做市商和两套官方交易商汇总数据，各自保留单位与信息日期，不能把汇总类别当成独立交易商。

Source paragraph SHA-256: `63ea616dad36a03644409d1d49ce09aa476269a14239788685a124af561c1ce0`.

> We examine one market maker's FX record alongside two official reporting systems that describe different segments of aggregate dealer activity. New York Fed reports cover government securities, while CFTC categories cover futures markets, requiring distinct targets, scales and historical references. Both weekly systems report dealer aggregates rather than independent individual dealers, and their economic units and information dates remain distinct.

## I04 — sec:intro

历史长度、惩罚候选集合和假设成本能整理这些结果，但历史规则仍很强，普适门槛和因果解释尚未识别。

Source paragraph SHA-256: `61a44cbec3e82e039444ac293fcf8746884d0829679d4484a1fde7e3838b771c`.

> History, the tested penalty menu and stated limit costs organize the comparisons, while a universal history requirement and causal explanation remain unidentified. Matched FX gains coexist with adverse weekly comparisons and reversals at the longest tested histories, keeping historical rules a demanding benchmark.

## I05 — sec:intro

新增期货检验只部分符合模拟与外汇的历史模式，尤其长期胜率和严格改善要求未通过。

Source paragraph SHA-256: `4fc1d55d42520d3529d9d79245a87bf4777ba5a9834795ffb841a701dc6fe0e3`.

> The first contribution connects simulation and FX history patterns with an additional reporting system, extending their comparison while retaining their limits. Earlier simulations support the registered short-history and long-history loss-sign predictions, while their universal simplification claim fails and FX curves retain reversals. The new CFTC extension agrees with the short-history counts but misses the registered long-history win target and strict-improvement target. Its combined verdict is partial agreement, leaving the broader history pattern qualified and a universally sufficient history threshold still unestablished.

## I06 — sec:intro

扩大候选集合既可能减轻估计损失也可能直接选中历史分位数，因此应分开看候选表现、选择损失与额外预测变量的价值。

Source paragraph SHA-256: `4ba224404cf42ba22e4b1a331aa6415096865d658f5522155f5a18b27eaf588f`.

> The second contribution distinguishes the amount of history from the available procedures, separating candidate performance from the effects of their selection. An expanded penalty menu removes much of a short-history simulation loss, while financial diagnostics retain selection errors and losses within the finite menu. The expanded menu includes an ordinary historical quantile, leaving the value of extra predictors unidentified by near-parity performance alone. Related forecast comparisons leave historical methods alongside many uneliminated alternatives, showing why a single reported winner gives an incomplete account.

## I07 — sec:intro

准备额度、超限次数和超限幅度的假设权重会改变成本排名，但尚未测得真实融资收益或交易干预效果。

Source paragraph SHA-256: `1cf2696577ea940c58117f30fa7cc1dd2d7c719537b463cf78b55f87bc2692be`.

> The third contribution connects forecast comparisons to stated limit costs, with reserve amounts, breach frequency and exceedance magnitude entering separately. Their weights can change which tested report is cheaper, although local exceptions persist within the evaluated grid of hypothetical preferences. The cost comparison illustrates this dependence on preferences, leaving realized funding gains and the effects of trading interventions outside its scope.

## I08 — sec:intro

匹配已完成标签的历史与重估时点使基准更明确，却没有统一所有特征和验证信息，因果与失败边界仍须保留。

Source paragraph SHA-256: `927dc8385df154969946a493f6faa16de34b1b8efe57f54bff67c591e31b4d12`.

> Matching training-label histories and refit schedules makes the benchmark explicit, while feature construction and validation can still use different information. Causal feature effects therefore remain unidentified, and all observed failures, unavailable comparisons and inspected-period qualifications remain part of the evidence.

## I09 — sec:intro

文章先定义目标并报告预测比较，再把跨数据的历史证据与假设成本联系起来。

Source paragraph SHA-256: `389866a64424f19e6254116dce73fb2a7c3ee1bf7a00dfd3340a845f071b4801`.

> Section defines the response and Section reports the forecasting comparisons, separating matched conditional gains from changes in the reference procedure. Section connects the history evidence across simulations, FX and CFTC, before Section relates these forecast comparisons to stated cost preferences.

## R01 — sec:results

较长历史下外汇回归在两个时期都胜过匹配基准，但换成较短滚动基准后早期排名反转。

Source paragraph SHA-256: `11cf629011b4654a7ec05dcb9ade746d42ec362665d9cd7dfbe24ba8757274f5`.

> Long-history FX regression beats matched historical headroom in both periods, yet its ranking against the shorter rolling reference reverses in the earlier period (Table ). The reference procedure is therefore part of the substantive finding, with a matched conditioning gain leaving the ranking against other historical rules unresolved.

## R02 — sec:results

短历史和较长预测期的外汇回归损失与超限次数都更差，说明长历史案例的优势只能作条件化解释。

Source paragraph SHA-256: `fd92fcb176846269bbdf75e8d4da922d21294994231ef5177b24fcdbb8050f20`.

> Beyond the matched long-history case, short-history FX regression performs poorly at the longer horizon. Loss rises by 31.5% against matched historical headroom. Regression records 924 breaches against 427 for the reference; the full horizon map retains the other adverse comparisons. This adverse case confines the interpretation of the matched long-history gain to its evaluated horizon and training-window setting, retaining the broader failures.

## R03 — sec:results

延迟校准保留了相对外汇得分优势，却仍有略多超限，而且每个校准方法相对自己的未校准版本都付出了绝对得分成本。

Source paragraph SHA-256: `dcd40619b3e8a68be42d870d170659f77f072e6b7f215476373d25a8ffb7d5c7`.

> Delayed calibration retains the later matched FX gain, although its breach count remains slightly higher than wrapped historical headroom on common origins (Table ). Calibration therefore changes breach frequency, while the distinct score and hit rankings persist on the common comparison grid. Each wrapper has a higher saved mean score than its own unwrapped base, so the retained relative ranking coexists with an absolute score cost. The headroom-SAV recursion refits on its evaluation training pools, whereas the selected ACI wrapper carries its delayed calibration state.

## R04 — sec:results

状态、目标分位数和重叠回溯比较的完整结果仍保留在原补充材料的对应位置。

Source paragraph SHA-256: `498d2e579b000748621cdb45de191ca195993ffc35e6115d323f57f5f526bd94`.

> The original full Supplement: Sections SID--SID and SID report the state, target-level and overlapping full-prefix comparisons ( the original full Supplement: Tables SID--SID and SID--SID ).

## R05 — sec:results

外汇回归在历史网格内先改善后回吐优势，完整曲线需要连同各自匹配基准一起看。

Source paragraph SHA-256: `730cdb3cd116e44fa29a1e91f802f91f4e9b24038d2cf0e40892c6d6a7aaeb78`.

> History sensitivity within the original FX record reverses across the tested grid, as full regression gives back gains at the longest history. Section combines both horizon curves with the simulation and CFTC evidence, retaining every tested window and its own matched historical reference.

## R06 — sec:results

小时结果对基准敏感，所以还要比较其他记录频率与报告系统，同时保持各比较内部的历史和标签一致。

Source paragraph SHA-256: `c6c097e784bbf5a6cffc17eb8adbf9b1df7283ead8a38f777a7c4476fd4676d3`.

> The reference-sensitive hourly results motivate comparisons with other measurement clocks and reporting systems, each retaining matched histories and completed peak labels.

## R07 — sec:results

国库券周频比较在得分与超限上都偏向历史规则，较早短窗口的不利结果也因历史不同而单独保留。

Source paragraph SHA-256: `569cd1418273402c4e302803cc8fdd410c30763ac558f7cc5abfafcd755cb536`.

> At weekly frequency, the Treasury-bill comparison favors historical headroom on both accuracy and breaches, extending the adverse ranking beyond the hourly examples. The earlier short-window version retains its separate adverse result because it uses a different history (Table ).

## R08 — sec:results

更强正则化缩小了周频损失，却没有消除历史基准优势，保守选择的最差国库券案例仍然失败。

Source paragraph SHA-256: `e7930ee3a43f41e1bfc24e688330fab2770366022fd229dba9c08a9ea37ae5f0`.

> Stronger regularization narrows weekly panel losses but leaves historical rules ahead, with conservative selection choosing the intercept-only report in 17 of 26 earlier cells (Table ). Its largest relative loss increase occurs in the Treasury-bill short-history, 24-step comparison, despite conservative selection.

## R09 — sec:results

简化条件模型和固定组合仍有周频失败，完整损失与失败表支持继续保留历史基准。

Source paragraph SHA-256: `9e188b997ced64f42542fa7772f61602d091db6455ac639bcc6a863395b7b1cf`.

> Simpler conditioning and fixed combinations retain adverse weekly comparisons, reinforcing the importance of an explicit historical benchmark for each forecast setting. The original full Supplement: Sections SID--SID retain their complete losses and failures, including the headroom-recursion results ( the original full Supplement: Tables SID--SID ).

## R10 — sec:results

改成日频后历史规则赢了大多数比较，唯一回归得分优势仍伴随更多超限。

Source paragraph SHA-256: `048ce5f2cb306f1a371516be3d0b40a23867dc4855e07cb8f929b5af651860b6`.

> Returning to the same FX record, historical headroom wins seven of eight daily comparisons, retaining a demanding reference after changing the measurement clock. The exception uses four predictors, with its complete specification and matched historical comparison retained alongside the adverse cases in the Supplement. Its training history is 260 and its horizon is 6, maintaining common completed targets and forecast dates across the matched procedures. The regression loss falls by 3.0%, although this accuracy gain accompanies a worse breach count than the matched historical report. Regression records 37 breaches versus 30 for headroom, preserving the score--breach disagreement while aggregation changes the leading method in most comparisons.

## R11 — sec:results

原期货比较大体重复历史规则难以击败的模式，但其事后较优历史参考不能当作可执行选择规则。

Source paragraph SHA-256: `70983618290c176bb6049c8fa04f6acae9c968b8b2fe9342104bc13a736798e8`.

> The independent reporting system gives a similar overall ranking: a historical headroom rule has lower loss in 29 of 34 contract/history comparisons. This meets the pre-specified 60% threshold, using the better realized score of corrected and ordinary empirical historical reports rather than an executable selector. Corrected historical headroom remains the fixed matched reference, with the ordinary empirical version reported separately. Both full-regression medians exceed the pre-specified ten-percent tolerance, whereas four-feature regression moves closer to history with the longer window. These comparisons extend the benchmark pattern to a separate reporting system while retaining substantial contract-level variation. This older reference comparison differs from Section , whose new history predictions use fixed corrected-rank headroom and separately registered thresholds.

## R12 — sec:results

联合方法比较通常把历史规则和多种替代方法一起留下，这表示尚未统计区分，而不是已经证明预测风险相同。

Source paragraph SHA-256: `fe144b52b71b597d7b18ee1484962646be34b90183971c1fd0fd841d63b76b97`.

> Joint comparison leaves matched historical methods alongside alternatives in most sets, with a single historical method surviving in only a small minority. These results support retaining historical controls while leaving many alternatives uneliminated under the fixed bootstrap approximation. Surviving procedures remain statistically unseparated under the specified comparison, while equality of their predictive risks remains a stronger, unestablished proposition. Table reports surviving methods, and Supplement Section SID retains every set, method p-value, identical-loss class and prior unavailable method.

## R13 — sec:results

周频损失同时来自选择错误和有限候选集合内的表现差距，各分量中位数也不能直接相加。

Source paragraph SHA-256: `e76b87538223cc6c97aa6c1c4d3d8426f2203e2cb6da10e2e4ec8a5bd2f17e68`.

> Short weekly samples leave both tuning errors and a performance gap within the finite penalty menu. Figure splits full regression's actual excess into the selected report's gap from the best finite candidate and that candidate's gap from historical headroom. The best candidate uses evaluation hindsight over five finite penalties; the ordinary empirical option is excluded. For full regression, the finite-menu gap is positive in 29 of 41 short-history weekly cells, retaining a disadvantage even after retrospective selection. Selection exceeds half of positive actual excess in 27 cells, so benchmark advantages and selection losses coexist within this finite menu. The median actual excess is 19.44%, while the median selection component is 18.32%, with each statistic summarizing its own component distribution. The median diagnostic gap is 4.37%; separate component medians generally differ from the median of their sum across the same comparisons.

## R14 — sec:results

事后挑选最好候选只能用于诊断，历史选项还可能让选择分量为负，因此部署表现和其他条件信息的价值仍未确定。

Source paragraph SHA-256: `26007d20c26e4ce99ea8c8407d3c808247ce3371615c903e5fab61663001506f`.

> Choosing the best candidate after evaluation makes this a retrospective diagnostic, leaving deployment performance and information in other conditional models unresolved. When validation selects the ordinary empirical limit, it can beat every finite candidate and make the selection component negative. Both long-history FX horizons have a negative finite-menu gap. Expanded menus also bring the calibrated simulation medians close to their historical reference, leaving the empirical frequency mechanism unidentified.

## R15 — sec:results

延长验证期后短训练历史的期货中位损失缩小，但仍按原来的目标、基准和预测日期比较。

Source paragraph SHA-256: `36941eca6e5648f24713b5520da2891c5b390254d8c0a691b229fe0b296aefe3`.

> Extending validation from 52 to 156 weeks keeps the CFTC evaluation period, training histories and refitting clock fixed in the saved sensitivity exercise. Consider first the 52-week training history, which retains its own historical reference and forecast dates when the validation period is extended. Its median excess falls from 19.33% to 4.03%, showing a narrower loss disadvantage under the longer validation period in this comparison.

## R16 — sec:results

较长训练历史也出现中位损失缩小，同时完整结果保留不同合约之间的差异。

Source paragraph SHA-256: `d411462d294581df2f27c3884da78fc5d14338e7eb0da6e50ca59e853a5fef71`.

> For the 260-week training history, the same exercise again holds the evaluated targets, historical benchmark and refitting schedule fixed. Its median excess falls from 10.35% to 0.53%, while the complete results retain the variation among contracts around these separate medians.

## R17 — sec:results

延长验证期更常选中普通经验分位数，但这些跨合约中位数和选择次数既不证明典型配对改善也不识别因果效应。

Source paragraph SHA-256: `3a99b60bed19ecba9f77c3777bacab0ab877bb048df2ba2c5ef46ed430f1e09b`.

> Infinite-penalty selections rise from 4 to 10 contracts under the shorter training history, favoring the ordinary empirical quantile more often. Under the longer training history, these selections rise from 4 to 5 contracts, again retaining the full market universe in the denominator. Each comparison covers 17 contracts; differences between their separate medians leave typical paired improvements and a causal interpretation unresolved. Four-feature failures remain unavailable in the complete inventory, preserving the distinction between a successful subset and its planned comparison (Supplement Section SID).

## R18 — sec:results

极端分位数检验仍有数值失败，期货门槛和外汇综合判据都保持无法判定，不能用成功子集替代完整分组。

Source paragraph SHA-256: `38dd364ce88cdd3e48202763ddfb21d6b6e79346c23980e59de4ac521dcb41f0`.

> Tail-level sensitivity remains incomplete, as the retained supplementary tail-sensitivity table shows for 90% and 99% quantiles under matched histories. Consider the 99% target separately, retaining the originally planned comparisons and the numerical failure recorded under that quantile sensitivity design. Historical headroom wins 28 of 34 CFTC comparisons, while the remaining numerical failure prevents classification of the complete planned group. The registered threshold requires 29 wins, leaving its verdict unresolved until the failed comparison can be determined under an authorized analysis. Both FX periods remain unavailable at 99%, leaving the combined improvement criterion undetermined and their failed planned comparisons explicitly retained. Successful subsets remain distinct from a missing full-group median, preserving the original uncertainty instead of replacing it with a favorable partial summary.

## R19 — sec:results

平均预测损失与是否超限衡量不同错误，所以得分改善时仍须同时报告超限。

Source paragraph SHA-256: `82518988f39b72a7d2f780ae13687e1fd627d2640fccffa739fabccd96fb3da3`.

> Accuracy rankings leave breach behavior unresolved: the matched FX gain coexists with more breaches before calibration (Table ). Pinball loss measures error amounts while a strict-hit indicator records event occurrence, so monitoring reports should show both forms of error.

## R20 — sec:results

误差权重改变会使特定长预测期的外汇比较反转，而较短预测期的两种误差都下降，不能把反转推广到全部比较。

Source paragraph SHA-256: `cc7026ef2f22b08754d8a369cccd8233759b77efaabf447674ee1e580a33a111`.

> Elementary-score rankings cross for both original main comparisons ( the original full Supplement: Figures SID--SID , the original full Supplement: Section SID ). A separate 24-step FX comparison against rolling translated paths changes ranking as the relative penalty on underprediction rises across the evaluated preferences. Its reversal occurs near 20.6:1, reflecting the weighting of underprediction against overprediction in that particular comparison of the saved reports. Both six-step FX comparisons reduce mean underprediction and mean overprediction, confining this weight reversal to the longer-horizon translated-path reference.

## R21 — sec:results

平均损失检验、超限事件检验和状态分组诊断回答不同问题，完整解释必须保持这种区分。

Source paragraph SHA-256: `00b214c54eb8497ab23d840115ff7364f40802d623c8566c9bf0f040db119dcb`.

> Loss and hit diagnostics answer different questions ( the original full Supplement: Table SID , the original full Supplement: Section SID ). HAC tests compare average loss and strict-hit tests examine event frequency and serial behavior, while RMS-state diagnostics compare conditional predictive ability across training-defined groups .

## H01 — sec:history-mechanism

模拟选中的历史与预测期比值只是整理固定网格的描述坐标。

Source paragraph SHA-256: `2020d56a9fa294f6daeaa9d3f7de573d79df03ed1deaee109c6b03249d4e73bf`.

> Let the training history contain W completed targets and let the horizon span H subsequent observations. The earlier discovery study selected the following ratio as a descriptive coordinate on its fixed simulation grid, leaving model complexity outside its definition:

## H02 — sec:history-mechanism

该比值没有模型参数数目，按方法分别估门槛还使常数缩放等价，因此它不能识别复杂度归一化或有效样本量。

Source paragraph SHA-256: `1dcda8ae1dfab28cb4575efd13e764590985c2b08a2982d9921b5eea6d006e26`.

> It excludes the number of coefficients, so an interpretation as dependence-adjusted information or an identified complexity normalization remains unsupported by this design. Estimating a separate threshold for each method also makes a later constant rescaling within that method observationally equivalent for the history-region checks.

## H03 — sec:history-mechanism

首次交点及宽区间只反映给定坐标与网格内的不确定性，多次交叉和坐标选择的不确定性排除了永久充分历史的解释。

Source paragraph SHA-256: `786def33aade0805ad4df250d5f2edaf9747017145a0708c5e8c670ac2c9dec6`.

> The discovery first crossing is approximately 106.5 for full regression, locating the initial change in sign on the selected simulation coordinate. For the sparse regression it is approximately 27.3 , with the underlying curve retaining further changes in direction across the tested grid. The full-regression fixed-grid interval runs from 27.89 to 110.71 , summarizing the original resampling uncertainty conditional on the selected coordinate. The sparse-regression interval runs from 13.27 to 107.11 , under the same restriction to the selected coordinate and simulation grid. Uncertainty from choosing that coordinate remains outside these ranges, and repeated downward crossings invalidate a permanently sufficient history interpretation.

## H04 — sec:history-mechanism

模拟的短长期损失方向判据通过，但保留的六个反例使全称简化命题失败。

Source paragraph SHA-256: `fe4d3f27279d2a748615d6f23b8fa9b04e677c381809f2f19576661472f292d4`.

> The subsequent registered simulation checks meet the short-history prediction in 47 of 48 cells under the declared simulation laws and menus. The long-history prediction holds in 21 of 24 cells, retaining the exceptions and the original fixed denominators in its descriptive count. These are finite-grid descriptive successes rather than independent-cell significance tests, because the experiments share their designed laws and comparison structure. The simpler procedure satisfies the universal-ordering inequality in 42 of 48 cells, falling short of the all-cell requirement for that claim. All six counterexamples remain in the evidence, so the universal simplification claim fails despite its inequality holding across most tested cells.

## H05 — sec:history-mechanism

部分外汇交点落入宽范围，另一条左删失曲线仍未定位首次交点，而且混合模拟交点不能等同于固定金融预测期交点。

Source paragraph SHA-256: `3a3604ffb4553232b64dee2f0214965c3359057bd0343d29acdeb9aa6cef844a`.

> Figure retains both regression variants and both FX horizons, alongside the earlier simulation and financial comparisons. Three identified financial first crossings fall within the broad transported ranges. Another curve already favors regression at its shortest tested history, leaving its first crossing left-censored. A pooled simulation crossing and a crossing at one fixed financial horizon are different objects. Their agreement leaves a horizon-invariant financial threshold unidentified, since the transported simulation summary and the individual financial curve represent different objects.

## H06 — sec:history-mechanism

较长预测期在最大历史又失去优势，这些重用的外汇记录只支持同一记录内比较，尚不构成独立交易商或全新留出样本。

Source paragraph SHA-256: `62bf508a9e9fa0d04e7e86f1238a8261205f90addf863c8045eeb4d22d0b1233`.

> Both longer-horizon FX curves lose their advantage again at the largest history. The shorter-horizon full-regression gain also weakens after its best tested history. These are the previously studied FX observations, including overlap with earlier comparisons. Their reuse supports a within-record history comparison, leaving replication across individual dealers and validation on an untouched financial holdout unresolved.

## H07 — sec:history-mechanism

新增期货计算先固定门槛且只扩展长历史，标签按时成熟的正确性与历史首次公开信息仍是两回事。

Source paragraph SHA-256: `d10ad9a9dd3f855b076e35184e108aa72137b6f85694191f6c6ccf06309d748e`.

> The CFTC extension fixes the earlier thresholds before adding a training history of 520 weeks, while reusing the unchanged shorter-history reports. The universe, validation period, evaluation dates, candidate menus and refit schedule remain inherited, confining the new computation to the registered extension. Its protocol was locally committed before the new fits, while shorter-history outcomes were already known and external public preregistration remains unclaimed. The candidate menus differ from the simulation discovery menus, making this a transported prediction check rather than a replication with identical procedures. Training labels have completed by each refit and every validation label finishes before evaluation, under the stipulated downloaded economic-date information convention. Historical first-release information remains distinct and unreconstructed, preserving the difference between a valid completed-label schedule and actual public availability.

## H08 — sec:history-mechanism

完整和稀疏回归在短历史区域的失利比例都达到预写门槛，支持这一限定范围内的短历史模式。

Source paragraph SHA-256: `06467cff27daef4951beaf1bec0683b28243ff733ae9578cc4e91ad9a2801fca`.

> For the full procedure, the low-history region contains 34 planned market-history comparisons, all retained under the registered classification and denominator. It loses to matched historical headroom in 29 comparisons, meeting the registered disadvantage criterion within this low-history region of the grid. The sparse procedure loses in 15 of 17 low-history comparisons, retaining the same fixed historical reference in each paired comparison. Both meet their registered eighty-percent targets, supporting the short-history sign pattern under these particular menus and transported simulation thresholds.

## H09 — sec:history-mechanism

稀疏回归在长历史的胜率没有达到预写要求，因此主判定只能是部分支持。

Source paragraph SHA-256: `299381e7ded201ce39edba30a99d1324bab5d33dcbc69102965d6126634206c2`.

> The sparse procedure wins in 10 of 17 long-history markets, leaving a substantial set of adverse contracts in the same region. That fraction misses its registered sixty-percent target, making the primary verdict partial agreement despite the successful short-history disadvantage counts.

## H10 — sec:history-mechanism

只有部分稀疏回归曲线每一步都严格改善，次要严格改善判据失败且不能改变主判定。

Source paragraph SHA-256: `455bb13aedcab2a194ffd7d9621db6d1e73390d9ae57f5f230b08c08ce2a6764`.

> Only 6 of 17 sparse-regression curves improve strictly at both steps of the history grid, retaining every reversal or tie. This misses the secondary seventy-percent target, which remains separate from the primary verdict and preserves the failure of strict improvement.

## H11 — sec:history-mechanism

七个长期不利市场、全部失败和不利曲线都保留，而较短期货结果事先已知也限制了独立确认与因果解释。

Source paragraph SHA-256: `4ad5766561dbefe7343da40e99b27e51e31650bf38c78c1f61bd4e3b09b82ddd`.

> Seven markets remain adverse for the sparse procedure at the long history. The complete market-level scores, strict breaches, HAC diagnostics and counterexamples remain in the supplementary result inventory and linked source tables. The primary verdict retains every market, failed criterion and unfavorable curve, with the full denominators fixed by the registered design. The shorter CFTC outcomes were known before this registration, so the extension is prospective only for its new computations. It gives partial agreement with a transported pattern, rather than a complete independent confirmation or causal identification of estimation cost.

## C01 — sec:cost

期货成本比较同时考虑准备额度、超限事件和幅度，幅度系数固定而其余偏好变化，且网格仍有局部反转。

Source paragraph SHA-256: `8f440058d1c87c1e029e33b7069c0423100fa121d0d6aaa3baebf91a4a323712`.

> For CFTC full regression, higher reserve coefficients and lower fixed-breach coefficients generally favor the expanded-menu procedure, although the fixed grid retains local reversals (Figure ). The exceedance-magnitude coefficient is fixed at c=1 , separating this charge from the reserve and breach-event preferences varied across the grid.

## C02 — sec:cost

在已声明成本网格的中心，回归只在较少匹配比较中更便宜。

Source paragraph SHA-256: `9cddca81ef4594bab84fbaaabec910abc9c5b972f29df79b83a99ee4a6976eb4`.

> At the center of the sorted grid, the reserve and breach-event coefficients are ( , )=(.1,.25) under the stated normalization. Regression is strictly cheaper in 5/34 comparisons there, retaining the same matched historical report and the original histories for each contract.

## C03 — sec:cost

当直接超限事件收费为零且更重视准备额度时，回归在大多数匹配比较中更便宜。

Source paragraph SHA-256: `b36ff298db10ea0e0a2b3ff7080683c1cdf5b80792afbb4102052eec523a8ca1`.

> At the reserve-heavy corner the coefficients are (1,0) , so reserve amounts and exceedance magnitude entirely determine these illustrative costs. Regression is cheaper in 32/34 comparisons there, illustrating how a different balance of stated costs can change the preferred report.

## C04 — sec:cost

相反地更重视超限事件时，回归很少更便宜，完整网格仍保留中间结果和例外。

Source paragraph SHA-256: `47429b2ad2bb3c5ea1bbae4b6d1a094d9562504e605982d04257bb095bf283dc`.

> At the opposite corner the coefficients are (.01,5) , placing greater weight on breach events relative to the reported reserve amount. Regression is cheaper in 1/34 comparisons there, with the complete grid retaining the intervening outcomes and any local exceptions.

## C05 — sec:cost

这些排名反映假设偏好而不是实际运营开支，完整归一化和方法结果仍可追溯。

Source paragraph SHA-256: `5b7bccc834ebefc60e47efe7b561280fa8605a07ac26ee7c9df122667503b603`.

> These costs express hypothetical preferences rather than observed operating expenses, and Supplement Section SID retains their normalization and complete-method results. Each contract uses its own historical headroom scale, so these normalized comparisons leave common-dollar costs and a common exposure measure unidentified.

