# v9 三条经验发现与贡献定位

依据：C2 完成提交 `153d307` 后的 `notes/v9/thesis.md`、既有原始归档和 C3/C4、C5 已落实的正文与补充材料。本说明只读取已保存结果、定义证据和解释边界；没有新增预测、诊断、拟合、模拟或数值统计。当前正文 Table 3 为 `tab:fx`、Table 4 为 `tab:weekly`、Table 5 为 `tab:diagnostics`、Table 6 为 `tab:map`；周度表未改名为 `tab:panel`。下文同时保留实际 LaTeX label 和归档字段定位。

三条贡献均放在同一 sampled absolute-position peak 任务下的比较发现。目标定义、成熟标签、地板投影、经典界和既有估计/检验工具是背景，不计为第四条贡献。所有“新增”均指本稿提供的具体比较证据，不是未经检索证明的文献优先权。

## First：小时级 FX 的匹配优势重复出现，参照规则仍改变跨期排名

**中文一句发现：** 小时级 FX 回归的同历史优势跨两个时期出现并经校准保留，但相对短历史滚动规则的排名随时期改变。

**English finding:** Matched hourly FX gains recur across periods and survive calibration, while rolling-reference rankings change.

**精确证据与定位：** 正文 `sec:results` 的 §7.1、Table 3（`tab:fx`）；校准完整结果 `sup:wp2`、`sup:wp2-pairs`；评分与破线分开解释已在 §7.3 和 Table 5（`tab:diagnostics`），不另立贡献。

| 比较 | 未舍入原值 | 正文显示 | 原档与精确字段 |
|---|---:|---|---|
| 后期 H6/W2880 QR 对同历史 F | -14.766762552613885% | 损失降低14.8% | `results/revision-20261022/paired-comparisons.csv`；`contrast_id=fx_hourly-h6-QR2880-minus-frozen_F2880`，`relative_mean_loss_difference_percent` |
| 早期 H6/W2880 原三罚项 QR/R0 对同历史 F | -16.62356533682211% | 损失降低16.6% | `results/supervisor-20261023/r6-writing-hac-20261023/results.json`；`/comparisons/0/ratio_change_percent` |
| 后期双方都经延迟校准的匹配比较 | -14.99691078803782% | 损失降低15.0% | `results/revision-20261023/v6/wp2-findings.json`；`/wrapped_pairs/1/qr_minus_f_loss_percent` |
| 同一校准比较的严格破线数 | QR=329；F=328 | 329对328 | 同上；`/wrapped_pairs/1/qr_hits`、`/wrapped_pairs/1/f_hits` |
| 后期 QR 对原 W720 rolling F | -12.660126412969763% | 损失降低12.7% | `paired-comparisons.csv`；`contrast_id=fx_hourly-h6-QR2880-minus-rolling_F720`，同一损失字段 |
| 早期 QR 对原 W720 rolling F | +3.1681985293173343% | 损失增加3.2% | `r6-writing-hac-20261023/results.json`；`/comparisons/1/ratio_change_percent` |

**最接近的已核文献：** `tab:literature` 中 Wisniewski et al. (2020)，以及正文已述的同源研究，已经预测单一做市商的 signed endpoint intervals，并联合报告 scores 与 hit tests。本稿沿用成熟的分位数预测和联合评价思路，增加的是 sampled peak 任务下的同历史匹配、滚动参照分离、两时期方向比较，以及双方校准后的损失/破线结果。Ehm et al. (2016) 的 elementary-score 工具可解释评价维度的分歧；工具本身不是本稿发明。

**边界：** 两个时期来自同一条熟悉的 FX 记录，不是两个独立交易商；与 Wisniewski 等已确认的是 source family 联系，没有核实输入字节相同。早期匹配数值属于原三罚项 QR/R0，不是 one-SE 的 R2；匹配 F 与短历史 rolling F 也不能互换。原 FX 评估期已被看过，早期回溯及扩展前缀不是前瞻性检验。15.0% 来自有限、投影、延迟的具体校准实现，不能移植成覆盖保证。未校准 matched 比较的破线数为376对360；因此较低平均 pinball loss 本身不表示较少破线，更不表示资金或交易收益。

## Second：低频比较中历史规则通常占优，强收缩与保守选择未稳定守住基准

**中文一句发现：** 在所检验周度汇总头寸和同记录日频 FX 中，历史规则通常占优，强收缩与保守选参没有稳定守住基准。

**English finding:** Historical rules usually prevail in weekly and daily comparisons, despite stronger regularization and conservative selection.

**精确证据与定位：** 正文 `sec:results` 的 §7.2、Table 4（`tab:weekly`）、Table 6（`tab:map`）；完整周度面板为 Supplement S12/S13（`sup:panel`、`sup:panel-second`）；保守选择为 S15/S16（`sup:selection`、`sup:selection-failures`）；日频对照为 S26（`sup:v8-daily`）及 Table S28（`tab:daily-fx`）。

| 证据 | 未舍入原值/完整计数 | 说明与原档 |
|---|---|---|
| 强正则化后的附加周度面板 | 34/48格 QR33-plus 损失高于匹配 F | `results/supervisor-20261023/e5/descriptive-summary.json`；`/QR33_plus/losing_to_F=34`，`/planned_cells=48` |
| 面板原菜单与扩展菜单的中位数 | +92.62799824594052% → +9.220703399904492% | 同上；`/original_QR33/median_percent_vs_F`、`/QR33_plus/median_percent_vs_F`；正文92.6%→9.2% |
| 同一做市商日频版本 | F赢7/8；QR33四格全败；QR4赢1/4 | `results/revision-v8/wp4/summary.json`；`/classifications/QR33`：historical_wins=4、conditional_wins=0；`/classifications/QR4`：historical_wins=3、conditional_wins=1 |
| 日频唯一 QR 胜格 | QR4、W260/H6，-2.9739933765508653% | 同上；`/contrasts/5/relative_loss_percent`；保留这一例外，不能写历史规则8格全胜 |
| 早期 one-SE 最差格 | +181.39452368014167% | `results/supervisor-20261023/r6/assessment.json`；`/S1/worst_percent_vs_F`；实际格为 PDPOSGS-B、H24、W52、R2，正文181.4% |
| 早期 one-SE 选择普通 I 的次数 | 17/26 | `r6/retro-summary.csv`；限制 `source=nyfed_weekly, report=R2` 的26行，`selected_id=I` 共17行；已存逐行核对见 `notes/v9/real-number-reconciliation.json` 的 `one_se_17_of_26_census` |
| 普通 I 自己的最差格 | +36.50893744342638% | `r6/summary.csv`；`phase=retro, source=nyfed_weekly, series_key=PDPOSGSC-L2, horizon=24, window=52, report=I`，`percent_vs_F`；正文36.5% |

181.4% 和36.5% 来自不同 series/方法格；17/26 是选中候选 I 的次数，不是失败格数、独立样本量或胜率。普通 I 与 corrected-rank F 的有限样本规则不同，不能把选择“简单候选”本身等同于守住 F。上述 R6 数字保留其熟悉历史、后结果探索性选择的证据角色，不升级为新的确认性结果。

**最接近的已核文献：** `tab:literature` 的 Wisniewski et al. (2020) 提供单一做市商预测的直接前例；Duffie et al. (2023) 讨论 dealer capacity、Treasury-market functioning 及不同目标的 PnL quantile 比较；Engle and Manganelli (2004) 提供成熟的条件分位数递推。本稿增加的是同一 sampled peak 与匹配 F 下的具体周度面板、同记录日频对照，以及扩大收缩/保守选择后仍存在的失败分布。它没有把这些前例的 endpoint/PnL/return 目标混为当前峰值目标，也没有发明新的正则化或选择法。

**边界：** 附加面板12条序列与原 Treasury-bill 共用一个周度报告体系，不是13个独立交易商。日频 FX 沿用同一做市商，频率、物理 horizon、物理 history、日历特征及 sampled target 一起改变；7/8不是纯频率效应或新交易商验证。扩展 lambda 菜单是见到结果后的探索；9.2% 的改善保留，但34/48的劣势也保留。结论限于这些程序、菜单、来源及评估期，不外推为所有条件模型都无用，也不产生部署或盈利建议。

## Third：平稳设计的结果并不一致，新控制过程也亏损，所提不稳定性机制未被识别

**中文一句发现：** 不同平稳设计给出的短历史结果不同，而新拟合恒定控制本身已有大幅亏损，所提不稳定性机制没有被识别。

**English finding:** Different stationary designs yield different losses, and fitted controls leave the proposed instability mechanism unidentified.

**精确证据与定位：** 正文 §7.4（`sec:extensions`）的实际标题为 “Does sample size explain the low-frequency losses?”，Figure 4（`fig:mechanism`）并列受控平稳设计与新校准比较。P5 受控网格的完整表在 Supplement S25（`sup:v8-mc`）及 Tables S26/S27（`tab:v8-mc-full`、`tab:v8-mc-four`）。旧 D0/D1/D2 全 24 格和七失败已在 S28（`sup:v9-legacy-mc`）及 Tables S31/S32（`tab:v9-legacy-mc`、`tab:v9-legacy-failures`）；C2 已在 S29（`sup:v9-stability`）及 Tables S33–S36（`tab:v9-stability-diagnostics`、`tab:v9-stability-w52`、`tab:v9-stability-w260`、`tab:v9-stability-f`）。以下继续绑定原始字段与 `prior-stationary-reconciliation.json`。

| 设计与比较 | 既存精确结果 | 统计口径与证据边界 |
|---|---|---|
| 旧 v8 校准 D0，QR33/H6/W52 | +1.0883496892148292% | 每重复相对损失变化的中位数；100次重复、500个评估 origin；宽菜单含截距极限 `inf`，weekly clock/特征/更新 |
| 旧 v8 校准 D2，QR33/H6/W52 | +0.3528682097196367% | 同一旧批次口径；接近持平是该设计的具体结果 |
| PR5 WP3，QR33/H6/W52，9个参数设定 | +113.45974253719095% 至 +135.5188592993867% | 各设定为跨重复的 mean-loss ratio；QR33仅三罚项，人工 hourly clock/特征/更新；这批平稳过程已经有大幅亏损 |
| PR5 WP3，QR33/H6/W260，9个参数设定 | +21.307826749419533% 至 +36.270776649491744% | 同一 WP3 mean-loss ratio；也不能写成“W≥260一律优于F” |
| C2 新拟合 constant control，QR33/H6/W52 | +116.24327967680179% | source内32个相对损失变化取中位数，再对全部13个source中位数等权取中位数；跨source IQR为92.89995539118937%至124.3385564851092% |
| C2 parameter-switching stress，QR33/H6/W52 | +121.40097999787356% | 同一两层中位数；跨source IQR为101.91853468487092%至131.2574640787476% |
| C2 两臂 QR33/H6/W260 | 全13来源的预设汇总不可评估 | PDPOSTIPS-G11 的 rep24、lambda=.001 验证不收敛，使 constant 与 switching 各一格仅31/32；不重试、不以31次或12来源补预设汇总 |

前三批结果的定位如下，不新增计算：

- 旧 D0/D2：本版原字节导入文件 `results/v9/legacy-calibrated/summary.json`，按 `dgp=D0/D2, window=52, features=33` 读取 `qr_median_pct`；原只读来源为 `/Users/bingyouli/Research/论文/金融数学论文-v8-20261024/results/v8/mc/summary.json`。导入身份见 `results/v9/legacy-calibrated/manifest.json`；逐行快照及原文件 SHA 继续保留于 `results/v9/nonstationarity/prior-stationary-reconciliation.json` 的 `legacy_W52_QR33` 与 `source_sha256`。
- PR5 WP3：`results/revision-v8/wp3/summary.json` 的 `cells`，限定 `method=QR33, horizon=6, window=52/260`，读取 `relative_loss_percent`；9行与既存范围位于 `prior-stationary-reconciliation.json` 的 `pr5_groups`。范围不是从挑选的有利行产生。
- C2：`results/v9/nonstationarity/postrun/analysis/qr33-across-sources.csv`，以 `arm`、`window` 选择 `median_pct`、`q25_pct`、`q75_pct`；命题状态来自 `postrun/predictions.json`；失败原回执和完整计数位于 `audit/failures.json`。postrun 只对已保存结果作精确 NumPy 标量转原生类型的报告，原 serialization error/partial 文件保留，没有科学重跑。

| C2 预登记命题 | 实际状态 | 可作的陈述 |
|---|---|---|
| N1：至少7/13周度 raw 5%拒绝 | SUPPORTED：7/13；Holm13仅2/13 | 部分固定 AR-GARCH-t 模型的稳定性被拒绝；原始计数与家族修正分开，不能声称7条均经家族修正确认 |
| N2：switching在W52及W260均超过+5% | UNASSESSABLE | W52已完整，但W260必要格失败；不能称N2已成立或被否定 |
| N3：constant的W52变化在±3%内 | NOT_SUPPORTED | +116.24327967680179% 明确偏离；平稳恒定参数控制自己可以产生大幅亏损 |
| N4：日频拒绝且观测密度更高 | UNASSESSABLE | daily为NONREGULAR_NULL，有限四阶矩资格不足；matched-calendar hourly为GARCH_OPTIMIZATION_FAILED；未知不等于稳定或不稳定 |

**最接近的已核文献：** `tab:literature` 的 Engle and Manganelli (2004)、Meinshausen (2006) 提供成熟的条件分位数结构，Ehm et al. (2016) 提供成熟的比较评价工具；它们不是为本稿的三套菜单、记录钟与校准机制提供现成解释。本稿增加的是这些已执行程序在明确设置下的受控/校准比较，以及对原先机制叙述的可核查反证和未决结果。Hansen 检验、AR-GARCH-t 拟合、BIC 定位与参数自助均为现有工具，出处已在本轮 `notes/v9/literature.md` 和正式 protocol 核过，不声称方法创新。

**边界：** 旧批次与 WP3 同时改变菜单、是否含 `inf`、时钟、特征、更新、验证/评估长度、校准和汇总量；差别不能单独归因于其中一项。C2 两臂在本轮按同一规则配对，但使用拟合模型与人工循环 regime 排程，last→first 是人为转移。研究问题来自已观察到的真实失利，前缀诊断/拟合不使用评估后观测也不使研究变成前瞻性或独立确认。控制过程本身亏损，说明不稳定性不是这些合成设置产生亏损的必要条件；没有识别真实低频损失机制，也不能反过来说样本长度就是唯一原因。

**必须删除的旧叙述：** “两次平稳模拟都在W52近持平且W≥260更好”“样本短本身造不出损失”“低频失利因此归因于不稳定”。可保留的叙述是：不同平稳设计有不同结果，新的恒定参数控制也有大幅亏损，低频失利的机制仍未识别。

## 不是创新的部分

1. **目标定义、成熟标签和已知地板。** 峰值目标与严格信息时序使研究问题明确；地板投影的逐点 pinball 非劣性质是基础性质。正文沿用：`Section 3 defines the target and records two elementary properties used later.` 不把它们放入摘要贡献句，也不称新估计方法。
2. **经典 Lévy 界与 endpoint-to-peak 讨论。** 经典概率工具在明确独立/对称假设下使用；经验 plug-in 或非违例模拟不把它变成真实头寸的覆盖保证。MaxVaR 与支付流动性文献提供不同路径目标的前例；van den Hoogen (2017) 的阅读缺口和 `n.r.` 保留，不把未报告当作没有。
3. **分位数回归、ridge、CAViaR式递推、分位数森林、有限ACI式校准、one-SE与组合。** 都是成熟程序或明确限定的实现。贡献来自共同目标和匹配基准下的实际结果，失败程序与不利比较仍保留。
4. **联合报告分数/破线、Murphy图、HAC与稳定性检验。** 既有文献已有这些工具；本稿贡献是当前任务上的具体分歧、失败和机制边界。不得把运行现成检验本身包装为理论或因果创新。
5. **D0没有条件信号的旧命名。** 必须改成 `constant-variance AR(1) levels, where the peak depends on the current position`。常方差不消除当前位置对峰值的条件信息，不能再称 D0 为“没有条件信号”或“不可预测”的设计。

## 审稿质疑与应答口径

| 可能质疑 | 本轮应答与证据边界 |
|---|---|
| 方法都现成，贡献究竟是什么？ | 三条明确的经验比较发现：matched hourly gains及rolling跨期反转、低频基准难以击败、平稳设计分歧及机制未识别。不给目标定义、地板投影、经典界或现成检验记方法创新。最近文献和任务维度沿用 `tab:literature`。 |
| 只有两类来源，13条周度序列是否伪装成独立复制？ | 明说单一做市商 FX 与同一报告体系的相关周度汇总。日频是同记录聚合，扩展回溯是重叠/熟悉前缀；均不新增独立交易商。不得做跨series独立合并显著性叙述。 |
| FX原评估期已看过，还能叫验证吗？ | 保留研究时序：原FX评估已先检视，后续校准、状态、选择及回溯是后结果探索。C2只在自己的运算前登记，不抹去研究动机的后验性质；早期及2015时期均非前瞻性验证。 |
| 扩大lambda菜单是见到失败后的补救，9.2%是否挑结果？ | 如实称后结果的探索性菜单扩展，同时报告92.6%→9.2%与34/48仍输、完整菜单/格子和失败。没有反复挑选有利菜单，也不把改善称为独立确认。 |
| one-SE选择更简单，为什么还不能守住F？ | 181.4%为R2的实际最差格；17/26仅为选择I的次数；普通I自己在另一格可比F差36.5%。这三个事实支持保留corrected-rank F作基准，不能把简单候选或one-SE当保证。它们都是原R6探索证据，不是新确认实验。 |
| 三个平稳设计为何相互矛盾？是否可以挑一批支持故事？ | 完整列出菜单、clock、features、校准和estimand的共同变化。旧D0/D2的近持平、WP3的短历史大亏损和C2恒定控制的大亏损全部保留；不选择一批覆盖另两批，不用统计量名称相近冒充数值可比。 |
| N1已成立，是否就证明了不稳定性机制？ | 7/13是raw计数，Holm13仅2条；global拒绝也可反映模型错设。N3已失败，N2/N4不可评估，完整解释条件未满足；结论是机制未识别。 |
| 两个W260格只差一个rep，为何不补跑或用31次？ | 正式设计规定任一必需rep失败则整格失败。PDPOSTIPS-G11、rep24、QR33的`.001`候选在两臂不收敛，两格均31/32；不补跑，不改菜单，不以12个source或31个rep替代预设13-source/32-rep汇总。 |
| 低损失是否意味着更少破线、较低资金成本或交易收益？ | 未校准 matched FX仍有376对360破线；校准329对328只说明这两个具体实现的观测频率接近。评分、覆盖与经营收益不是同一结果，本稿没有估计资金成本、收益或最优交易策略。 |

## 与摘要、引言、结论的共同约束

First/Second/Third 最多三条，均依照上述发现。摘要不保留 “We formalize…apply a classical bound”。Limitations 集中保留单一做市商、FX评估先检视、非前瞻回溯、同周度报告体系、Treasury下载版本回放、无因果机制、无覆盖保证及无交易/资金收益；各说一次即可。C2 的失败与反证进入主线，不用更乐观的旧措辞替代。上述正文表号、Figure 4 和新增 Supplement labels 已在 C3/C4 落实；C5 的 42 项处置记录位于 `notes/v9/referee-check.md`。本说明只收口已存在的落点，不把 C6/C7 的最终交付和验证预先判为通过。
