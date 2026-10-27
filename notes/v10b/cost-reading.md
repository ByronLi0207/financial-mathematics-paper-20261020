# v10b 归档成本只读核对

状态：`PASS_READ_ONLY_ARCHIVED_FLAGS`。实际读取 UTC：`2026-10-25T03:56:52.503961+00:00` 至 `2026-10-25T03:56:53.337846+00:00`。

只读取已有 cheaper/equal、身份字段与已存汇总；没有重算损失/成本，没有模型、实验或归档写入。分母为17个 normalized_source 合约 × 两个 window（52、260）=34个相关合约/历史比较。

两份表在 c=1、group_label=CFTC、method_id=CFTC::QR33 下的2142条记录逐字段完全相同；所有点均有34条 COMPLETE，没有未知或等价记录。完整逐行证据见 JSON 的 two_file_match.row_bindings；CSV 表头算第1行，ZIP行号指解压后 member cost-grid.csv。

|原文件|SHA-256（读取前后相同）|
|---|---|
|`results/v10/cost/primary-regions.csv`|`7ff19bb457ed3b1f839ffdb596452742f03f20fd0ae90f00aaadb3d2444df651`|
|`results/v10/cost/cost-grid.csv.zip`|`b453c12cb8e8c4332a3ab180bbdfe899156a5a426d8a94a98dcf21967b265fa1`|
|`results/v10/cost/manifest.json`|`0f3605b9664f973c25458ccfb77f1588c8a5bb6e3d31849dadf075c2fd434c15`|
|`results/v10/mcs/summary.json`|`fcccd85fd9cdbbbe2343194b74d1f1279d854a1618e82c0e495be1abe340874c`|
|`results/v10/mcs/full-cells.json`|`c9cdd0f2da9168c483cda9b37d550181437e46e4152145cd525d5df459f6faab`|
|`results/v10/menu/summary.json`|`e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`|

固定参考 F、c=1 与严格 cheaper 的定义绑定 `manifest.json#/design/reference_id`、`/design/primary_c`、`/design/ties`；计算只数 `cheaper=True`，没有由 difference 重新判定。中心按已归档轴排序位置：κ第4/7项=.1，β第5/9项=.25。

|位置|κ|β|严格较便宜/分母|equal|primary行号 / ZIP member行号|
|---|---:|---:|---:|---:|---|
|sorted_position_center|0.1|0.25|5/34|0|JSON examples 对应两组34行；逐项 join 到 two_file_match.row_bindings|
|higher_reserve_lower_breach_corner|1.0|0.0|32/34|0|JSON examples 对应两组34行；逐项 join 到 two_file_match.row_bindings|
|lower_reserve_higher_breach_corner|0.01|5.0|1/34|0|JSON examples 对应两组34行；逐项 join 到 two_file_match.row_bindings|

## 方向与非单调例外

Expanded QR33 is more often cheaper than F toward higher reserve coefficients and lower fixed-breach charges, with one contract/history exception to monotonicity.

总体有利方向是更高κ、较低β，但不应写成必然单调：唯一例外单元是 cftc:090741、W260，κ升高有9条 True→False 相邻边，β升高有2条 False→True 相邻边。以下列出每条原始 cheaper 标记及两表行号；未重算任何金额。

|方向|κ前→后|β前→后|cheaper前→后|primary行前→后|ZIP行前→后|
|---|---|---|---|---|---|
|higher_kappa_true_to_false|0.05→0.1|0.0→0.0|True→False|2892→2919|17344→17506|
|higher_kappa_true_to_false|0.05→0.1|0.01→0.01|True→False|2895→2922|17362→17524|
|higher_kappa_true_to_false|0.05→0.1|0.05→0.05|True→False|2898→2925|17380→17542|
|higher_kappa_true_to_false|0.05→0.1|0.1→0.1|True→False|2901→2928|17398→17560|
|higher_kappa_true_to_false|0.05→0.1|0.25→0.25|True→False|2904→2931|17416→17578|
|higher_kappa_true_to_false|0.05→0.1|0.5→0.5|True→False|2907→2934|17434→17596|
|higher_kappa_true_to_false|0.1→0.2|1.0→1.0|True→False|2937→2964|17614→17776|
|higher_kappa_true_to_false|0.1→0.2|2.0→2.0|True→False|2940→2967|17632→17794|
|higher_kappa_true_to_false|0.2→0.5|5.0→5.0|True→False|2970→2997|17812→17974|
|higher_beta_false_to_true|0.1→0.1|0.5→1.0|False→True|2934→2937|17596→17614|
|higher_beta_false_to_true|0.2→0.2|2.0→5.0|False→True|2967→2970|17794→17812|

聚合计数也不是处处单调：

|方向|κ前→后|β前→后|严格较便宜计数前→后（分母均34）|
|---|---|---|---|
|higher_kappa_reduces_count|0.1→0.2|2.0→2.0|2→1|
|higher_kappa_reduces_count|0.2→0.5|5.0→5.0|2→1|
|higher_beta_increases_count|0.2→0.2|2.0→5.0|1→2|

完整计数矩阵（行κ、列β；每项为 cheaper=True/34，全部原始行在 JSON）：

|κ / β|0.0|0.01|0.05|0.1|0.25|0.5|1.0|2.0|5.0|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0.01|2|1|1|1|1|1|1|1|1|
|0.025|3|2|1|1|1|1|1|1|1|
|0.05|5|5|4|3|1|1|1|1|1|
|0.1|15|15|10|8|5|2|2|2|2|
|0.2|26|25|23|21|15|10|3|1|2|
|0.5|31|31|31|31|31|29|18|9|1|
|1.0|32|32|32|32|32|31|31|20|6|

## 成本小节精确三句英文

At fixed $c=1$, expanded-menu QR33 is generally cheaper than F more often with higher reserve coefficient $\kappa$ and lower fixed-breach coefficient $\beta$, although the archived grid is not monotone.
Across the 17 contracts and two histories, it is strictly cheaper in 5/34 comparisons at the sorted-grid centre $(\kappa,\beta)=(0.1,0.25)$, versus 32/34 at $(1,0)$ and 1/34 at the opposite corner $(0.01,5)$.
These coefficients are illustrative preferences rather than observed business costs, so the rankings do not establish funding gains or a cost-optimal policy.

## 其他三处同口径建议

贡献3：Third, score gains translate into lower limit costs only in parts of the coefficient grid; CFTC expanded-regression cost advantages are more prevalent under higher reserve and lower fixed-breach charges, with exceptions to monotonicity.

RQ3结论：For RQ3, score gains imply lower limit costs only for some illustrative reserve, breach-frequency and exceedance preferences; the CFTC grid generally favors expanded regression as reserve charges rise and fixed-breach charges fall, with exceptions to monotonicity.

Letter：The third finding separates forecast-score gains from limit-cost rankings: expanded regression is generally cheaper in more CFTC comparisons under higher reserve and lower fixed-breach charges, while the illustrative coefficient grid contains exceptions to monotonicity.

The cost subsection's three sentences contain the full three-point numerical example. Use qualitative versions in contribution 3, RQ3 conclusion and letter to avoid repeating the same result numbers. Relocate the existing illustrative-cost caveat from Limitations if needed so that it appears only once in the main manuscript. Do not turn the direction into an exception-free comparative-static claim.

## 摘要顺带核对

- `results/v10/mcs/summary.json#/overall/metrics/matched_FI_membership/count_successful=90`，`denominator_successful=98`，`fraction_successful=.9183673469387755`；逐个核对 full-cells.json 已存 included 字段得到同样90/98。可写 nearly always，但更建议精确 in 90 of 98 comparisons；这不是独占胜出。`literal_sole_FI/count_successful=2`；非排除不证明风险相等。
- `results/v10/menu/summary.json#/across_sources/0` 的 `arm=constant,window=52,method=QR33,status=COMPLETE,complete_sources=13,original_median_pct=116.24327967680179,median_pct=.2069371499562489`，支持116.2%→0.2%；`/across_sources/4` 的 switching 对应121.40097999787356%→−.22777914491914353%。这是每来源重复中位数再跨13来源中位数，不是全部重复混合或观测商业损益。
- 同文件 `/predictions/M2/switching_minus_constant_pct_points=-.43471629487539243`，`minimum_inclusive_percentage_points=5.0,status=NOT_SUPPORTED`。只能写注册的额外损失阈值未获支持，不能写切换无效应或两组等价。所有数值的精确字段绑定在 JSON abstract_checks。
