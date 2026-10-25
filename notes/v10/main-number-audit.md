# E5 主稿数字与来源绑定审计

结论：**PASS，未发现尚未解决的事实数字错误**。初读时发现一处菜单范围句子过宽，root 已在审计期间改为只指 full regression；数值和保存结果没有差异。这是源对照审计，不是独立金融重算，也不是 E6 模拟审稿。

本轮读取从 `2026-10-25T00:00:39.088047+00:00` 开始。主稿初始 SHA-256 为 `988787596bc14554d31237345de263af6f7645d3f834771517761608fa9bb19f`；当前审计快照为 `39fc54af093c0367f7877aa96b3b8f8c742f16ca076ec8ab31cfd9d7ea2ec672`。root 在此期间作排版和上述措辞修订。旧 `submission-jof/manuscript.tex` 当前 SHA-256 为 `83c611692ecba07dd155d9792aa71870f9f9040f88cc9143c7ea639dd9278993`。审计只写本 Markdown 与 companion JSON，没有改主稿、表、图或继承代码。

## 重点事实数字

|主稿事实|本轮直接核对的保存来源与精确字段|结果|
|---|---|---|
|较晚／较早匹配 FX 降低14.8%／16.6%|`results/revision-20261022/paired-comparisons.csv`，唯一 `contrast_id=fx_hourly-h6-QR2880-minus-frozen_F2880`，`relative_mean_loss_difference_percent=-14.766762552613885`；`results/supervisor-20261023/r6-writing-hac-20261023/results.json#/comparisons/0/ratio_change_percent=-16.62356533682211`|PASS|
|校准后降低15.0%，329对328 breaches|`results/revision-20261023/v6/wp2-findings.json#/wrapped_pairs/1/qr_minus_f_loss_percent=-14.99691078803782`；同一对象 `qr_hits=329,f_hits=328`|PASS|
|较早 weekly 的 I 选择17/26|`results/supervisor-20261023/r6/retro-summary.csv`，筛 `source=nyfed_weekly,report=R2`；26行的 `selected_id` 为 I:17、1:3、10:5、0.1:1|PASS；仅清点已保存选择|
|最差 one-SE 增幅181.4%（表181.39%）|同一 `retro-summary.csv`，唯一 `source=nyfed_weekly,series_key=PDPOSGS-B,horizon=24,window=52,report=R2`，`percent_vs_F=181.39452368014167`|PASS；明确是24步、W52|
|较早短历史 bill +144.3%（表144.30%）|`results/supervisor-20261023/r6/primary-replication.csv`，唯一 `id=Treasury-W52-structural-analogue`，`percent_vs_reference=144.296201250835`|PASS；保留与原主比较不同 history 的限定|
|expanded weekly 34/48 higher-loss|`results/supervisor-20261023/e5/descriptive-summary.json#/QR33_plus/losing_to_F=34`，`#/planned_cells=48`|PASS|
|CFTC877周、17个合格代码／141个总代码|`results/v10/cftc/eligibility.json#/N=877`；`len(/selected)=17,len(/contracts)=141,len(/calendar)=877`；周历端点2010-01-04／2026-10-19|PASS；Monday model clock 与实际 position date 区别保留|
|CFTC evaluation日期、52／260、H6|`results/v10/cftc/splits.json#/indices` 为 validation553..604、evaluation611..870，52／260、gap6；`#/actual_dates/evaluation` 为2021-09-21、2026-09-08、末标签2026-10-20；`#/model_clock`为相应Monday|PASS|
|CFTC29/34与60%门槛|`results/v10/cftc/summary.json#/predictions/T1`，`simple_better_cells=29,required_cells=34,minimum_inclusive_fraction=.6,status=SUPPORTED`|PASS|
|CFTC QR33 +19.3%／+10.3%|同一 summary `#/predictions/T2/median_pct_by_window/52=19.334715757564624`、`/260=10.34828178946443`；`status=NOT_SUPPORTED`|PASS；两者均超过10%容忍上限|
|QR4从10.3%到0.2%|同一 summary `#/predictions/T3/W52_median_pct=10.280676300222424`、`W260_median_pct=.2174917571722501`|PASS；这是QR4跨history的中位数变化|
|E1旧116.2%／121.4%，新+0.2%／−0.2%|`results/v10/menu/summary.json#/across_sources`，筛 `method=QR33,window=52,arm=constant/switching`；`original_median_pct=116.24327967680179/121.40097999787356`，`median_pct=.2069371499562489/−.22777914491914353`|PASS；来源内32重复、全部13来源中位数|
|E1 M1/M3支持，switch增量不足+5pp|同一 summary `#/predictions/M1/status=SUPPORTED`、`M3/status=SUPPORTED,joint_improved_sources=13`；`M2/status=NOT_SUPPORTED,switching_minus_constant_pct_points=−.43471629487539243`|PASS；未把门槛未过写成等价|
|W260两臂 QR33 whole summary unavailable|同一 `#/across_sources` 的 QR33/W260 `status=UNASSESSABLE,missing_sources=[PDPOSTIPS-G11]`；report receipts明确failed repetition24|PASS；未用成功来源子集补中位数|
|MCS90/98、197/683、sole literal2|`results/v10/mcs/summary.json#/overall/metrics/matched_FI_membership/count_successful=90`，`planned_comparisons=98`；`conditional_exclusion/excluded_slots=197,successful_complete_slots=683`；`metrics/literal_sole_FI/count_successful=2`|PASS；sole loss class另外是4，未混用|
|CFTC成本1–32/34|`results/v10/cost/group-regions.json`筛 `group_label=CFTC,c=1`；保存的 `wins`最小1、最大32，`complete=planned=34`。精确行指针见JSON的 `COST_CFTC_MIN/MAX`|PASS；仅读保存win-count，不重算金融成本|

## 继承数值与新表图

旧 v9 审计只作为定位路由。本轮重新读取其 **240个 owning source locators**，分别检查文件 SHA-256、JSON pointer、唯一 CSV 条件行或原文片段，240项全部通过；逐项原值、精确键和当前指纹保留在 `main-number-audit.json#/old_archive_locator_checks`。这涵盖主稿保留的640 crossing、18,576 FX records、706 weekly records、930 daily days／501 issues、FX损失/strict breaches、daily比较、20.6:1与旧simulation等数字。旧审计记录的早期主稿指纹不等于最终v9文件，所以没有借它替代本轮源字段复核。

新 menu 表8行（含 IQR、NA与缺来源数）和 CFTC 表17行／170个显示值逐项匹配 `results/v10/*/report-values.json` 的完整精度值，按2位小数显示；新 MCS紧凑表7行各自的分母、计数与百分比匹配保存group对象。合计32行检查通过。MCS表在本轮由root压缩排版，已非字节复制，但数字和限定保持一致，机器审计中单列为 `PASS_COMPACT_REFORMAT_VALUES_CHECKED`。

menu与CFTC两份表、三张v10 PDF图均与结果目录对应artifact字节一致；继承的 `v9-endpoint-peak-example.pdf`也与v9字节一致。7对artifact中6对字节一致，另1对为上述已检查的MCS紧凑改排。只核来源绑定与文件身份，没有把这声称为图像像素、排版或编译验收。

## 新设定、引用与限制

MCS的90% confidence、`arch==8.0.0`、R statistic、stationary bootstrap、1000 repetitions、`max(H,ceil(n**(1/3)))` 均核 `results/v10/mcs/manifest.json#/design`。CFTC的H6、W52/260、refit13核对应manifest。成本的kappa七点、beta九点、c三点与 `results/v10/cost/manifest.json#/design/grid`逐值一致。详细键及值列入JSON。

DM1995、GW2006、HLN2011、Duffie2023及Avellaneda–Stoikov2008五条书目与本轮已保存的一手核对记录 `notes/v10/reference-verification.md`一致；HLN条目现在已加入，Duffie月份/编号已明确，A–S保持库存报价动机的用途。这里只沿用该记录实际访问精度，没有把摘要/索引的元数据核对升级为全文算法证明，也未声称全书目核对。官方DOI分别为：`10.1080/07350015.1995.10524599`、`10.1111/j.1468-0262.2006.00718.x`、`10.3982/ECTA5771`、`10.59576/sr.1070`、`10.1080/14697680701381228`。

Limitations保留了：原FX和早期／backcast的事后研究时点；CFTC经济日期重放而非原始first-release vintage；类别aggregate而非独立dealer；net可抵消gross和rawcontracts不可换成共同美元风险；continuity与OI排名形成retrospective survivor universe；两个ingestion澄清发生在获取后、任何forecast/model-loss前；旧simulation菜单/时钟/校准law/summary不等价；paired QR4 tie规则变化；illustrative成本系数与MCS依赖假设。没有发现限制条款被新结论覆盖。

## 已处理的唯一问题与边界

初始句 `Expanded-menu regression changes only the penalty grid.` 对QR4过宽。root已改成 `Expanded-menu full regression changes only the penalty grid.`，与后文及表脚的QR4 stronger exact-tie说明相容；保存exactties0、changedQR4tie selections0，因此该项不是数值错误。

本审计结论仅适用于记录的主稿末次SHA和当前表图；后续科学内容改动需增量复核。没有读取真实NPZ、下载金融数据、导入预测模型或重算金融统计，没有改稿、提交、Claude/Cloud或跨模型审查。完整机器证据见同目录JSON。
