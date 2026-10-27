# C0 两个 v8 真实数据数字对照

核对时间：2026-10-24T18:11:27.129917+00:00。结论：**PASS。共同 results/data 文件 1,349 个逐文件字节数与 SHA-256 完全相同，归档字节差异 0；571 个共享真实数据证据字段逐项原生类型和值相同；另核对 2,125 个继承补充材料字段，无不一致。**

源一：`/Users/bingyouli/Research/论文/金融数学论文-v8-20261024`，HEAD `f151b830489917ab7abc5137f2ec6b4135f55d6e`。
源二：`/Users/bingyouli/Research/论文/金融数学论文-v9-20261024`，以 PR #5 的 `0f1f066843e0c49cf3e24bce7d72032dc189603d` 为底。

只读取既有输出与稿件；没有重新预测、诊断、拟合、模拟或检验。旧目录保持只读。本页与同名 JSON 是本子任务仅有的写入。

## 核心原值与显示

下表原值来自直接打开的 JSON 指针或唯一 CSV 行选择器。两个 v8 原值完全相同。表格显示列体现 PR5 常用两位小数与本地 v8 的一位小数排版；正文的降幅用正的幅度表述，带符号的原值仍完整保留。完整来源哈希在 JSON 的 shared_results_data_inventory 及 empirical_native_fields。

| 证据 ID / 位置 | 两边共同原值 | revision-v8 显示 | PR5 表格/继承显示 | 源文件与字段 |
|---|---|---|---|---|
| FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / table:fx | "-12.660126412969763" | -12.7 | -12.66 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=relative_mean_loss_difference_percent |
| FX_LATE_PRIMARY_H6_ORIGIN_COUNT / table:fx | "6625" | 6625 | 6625 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=origin_count |
| FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_LEFT / table:fx | "376" | 376 | 376 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=strict_breach_count_left |
| FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_RIGHT / table:fx | "332" | 332 | 332 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=strict_breach_count_right |
| FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / table:fx | "-14.766762552613885" | -14.8 | -14.77 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent |
| FX_LATE_MATCHED_H6_ORIGIN_COUNT / table:fx | "6625" | 6625 | 6625 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=origin_count |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT / table:fx | "376" | 376 | 376 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_left |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT / table:fx | "360" | 360 | 360 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_right |
| FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT / table:fx | 3.1681985293173343 | +3.2 | +3.17 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/ratio_change_percent |
| FX_EARLY_PRIMARY_H6_N / table:fx | 1440 | 1440 | 1440 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/n |
| FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT / table:fx | -16.62356533682211 | -16.6 | -16.62 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/ratio_change_percent |
| FX_EARLY_MATCHED_H6_N / table:fx | 1440 | 1440 | 1440 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/n |
| FX_EARLY_MATCHED_R0_STRICT_BREACH_COUNT / table:fx | "20" | 20 | 20 | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"R0"}; field=strict_breach_count |
| FX_EARLY_MATCHED_F_STRICT_BREACH_COUNT / table:fx | "16" | 16 | 16 | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"F"}; field=strict_breach_count |
| FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT / table:fx | -14.99691078803782 | -15.0 | -15.00 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_minus_f_loss_percent |
| FX_ACI_H6_W2880_N / table:fx | 6625 | 6625 | 6625 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/n |
| FX_ACI_H6_W2880_QR_HITS / table:fx | 329 | 329 | 329 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_hits |
| FX_ACI_H6_W2880_F_HITS / table:fx | 328 | 328 | 328 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/f_hits |
| PANEL_BILL_QR_H6_W260_LOSS_PERCENT / table:weekly | "50.78571256749063" | +50.8 | +50.79 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=relative_mean_loss_difference_percent |
| PANEL_R6_BILL_W52_ANALOGUE_LOSS_PERCENT / table:weekly | "144.296201250835" | +144.3 | +144.30 | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=percent_vs_reference |
| PANEL_E5_QR33_MEDIAN / table:weekly | 92.62799824594052 | +92.6 | +92.63 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/median_percent_vs_F |
| PANEL_E5_QR33_LOSSES / table:weekly | 45 | 45 | 45 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/losing_to_F |
| PANEL_E5_PLANNED / table:weekly | 48 | 48 | 48 | results/supervisor-20261023/e5/descriptive-summary.json /planned_cells |
| PANEL_E5_QR4_MEDIAN / table:weekly | 9.90727239745182 | +9.9 | +9.91 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/median_percent_vs_F |
| PANEL_E5_QR4_LOSSES / table:weekly | 37 | 37 | 37 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/losing_to_F |
| PANEL_E5_QR33_EXPANDED_MEDIAN / table:weekly | 9.220703399904492 | +9.2 | +9.22 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/median_percent_vs_F |
| PANEL_E5_QR33_EXPANDED_LOSSES / table:weekly | 34 | 34 | 34 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/losing_to_F |
| PANEL_E5_ORDINARY_I_MEDIAN / table:weekly | 0.5006801691981209 | +0.5 | +0.50 | results/supervisor-20261023/e5/descriptive-summary.json /I/median_percent_vs_F |
| PANEL_E5_ORDINARY_I_LOSSES / table:weekly | 30 | 30 | 30 | results/supervisor-20261023/e5/descriptive-summary.json /I/losing_to_F |
| PANEL_R6_R0_RETRO_MEDIAN / table:weekly | 4.1510024714803695 | +4.2 | +4.15 | results/supervisor-20261023/r6/assessment.json /S3/R0_median_percent_vs_F |
| PANEL_R6_R0_RETRO_COMPLETE / table:weekly | 26 | 26 | 26 | results/supervisor-20261023/r6/assessment.json /S3/R0_complete_count |
| PANEL_R6_R2_RETRO_MEDIAN / table:weekly | 5.374072481175762 | +5.4 | +5.37 | results/supervisor-20261023/r6/assessment.json /S1/median_percent_vs_F |
| PANEL_R6_S1_COMPLETE / table:weekly | 26 | 26 | 26 | results/supervisor-20261023/r6/assessment.json /S1/complete_count |
| PANEL_BILL_QR_H6_W260_QR_HITS / table:weekly | "54" | 54 | 54 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=strict_breach_count_left |
| PANEL_BILL_QR_H6_W260_F_HITS / table:weekly | "28" | 28 | 28 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=strict_breach_count_right |
| PANEL_BILL_QR_H6_W260_N / table:weekly | "277" | 277 | 277 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=origin_count |
| PANEL_R6_R2_RETRO_WORST / table:weekly | 181.39452368014167 | 181.4 | 181.39 | results/supervisor-20261023/r6/assessment.json /S1/worst_percent_vs_F |
| FX_DM_PRIMARY_H6_DM_P / table:diagnostics | "2.1950725127844084e-07" | 2.2e-07 | 2.2e-07 | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=dm_p |
| FX_DM_PRIMARY_H6_HLN_P / table:diagnostics | "2.312477658474048e-07" | 2.31e-07 | 2.31e-07 | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=hln_p |
| FX_DM_PRIMARY_H6_PRIMARY_BONFERRONI_P / table:diagnostics | "4.390145025568817e-07" | 4.39e-07 | 4.39e-07 | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=primary_bonferroni_p |
| FX_DM_MATCHED_H6_DM_P / table:diagnostics | "4.472961414014163e-09" | 4.47e-09 | 4.47e-09 | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=dm_p |
| FX_DM_MATCHED_H6_HLN_P / table:diagnostics | "4.82747017649871e-09" | 4.83e-09 | 4.83e-09 | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=hln_p |
| FX_DM_MATCHED_H6_ARCHIVED72_HOLM_P / table:diagnostics | "2.8626953049690645e-07" | 2.86e-07 | 2.86e-07 | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=archived72_holm_p |
| PANEL_BILL_PRIMARY_DM_P / table:diagnostics | "0.007611369596467356" | 0.00761 | 0.00761 | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=dm_p |
| PANEL_BILL_PRIMARY_HLN_P / table:diagnostics | "0.009390617005130322" | 0.00939 | 0.00939 | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=hln_p |
| PANEL_BILL_PRIMARY_HOLM_P / table:diagnostics | "0.31967752305162894" | 0.32 | 0.32 | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=holm_p |
| PANEL_BILL_PRIMARY_FAMILY_N / table:diagnostics | "72" | 72 | 72 | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=holm_family_size |
| FX_COVERAGE_QR_HITS / table:diagnostics | "50" | 50 | 50 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=hits |
| FX_COVERAGE_QR_N / table:diagnostics | "947" | 947 | 947 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=n |
| FX_COVERAGE_QR_POF_P / table:diagnostics | "0.6952768918173253" | 0.695 | 0.695 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=pof_p |
| FX_COVERAGE_QR_CC_P / table:diagnostics | "0.6361520236127319" | 0.636 | 0.636 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=cc_p |
| FX_COVERAGE_PRIMARY_F_HITS / table:diagnostics | "49" | 49 | 49 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=hits |
| FX_COVERAGE_PRIMARY_F_N / table:diagnostics | "947" | 947 | 947 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=n |
| FX_COVERAGE_PRIMARY_F_POF_P / table:diagnostics | "0.8067032386212847" | 0.807 | 0.807 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=pof_p |
| FX_COVERAGE_PRIMARY_F_CC_P / table:diagnostics | "0.9050821379899511" | 0.905 | 0.905 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=cc_p |
| FX_COVERAGE_MATCHED_F_HITS / table:diagnostics | "49" | 49 | 49 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=hits |
| FX_COVERAGE_MATCHED_F_N / table:diagnostics | "947" | 947 | 947 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=n |
| FX_COVERAGE_MATCHED_F_POF_P / table:diagnostics | "0.8067032386212847" | 0.807 | 0.807 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=pof_p |
| FX_COVERAGE_MATCHED_F_CC_P / table:diagnostics | "0.645851306104558" | 0.646 | 0.646 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=cc_p |
| COVERAGE_BILL_QR_HITS / table:diagnostics | "7" | 7 | 7 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=hits |
| COVERAGE_BILL_QR_N / table:diagnostics | "40" | 40 | 40 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=n |
| COVERAGE_BILL_QR_POF_P / table:diagnostics | "0.004126046248434382" | 0.00413 | 0.00413 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=pof_p |
| COVERAGE_BILL_QR_CC_P / table:diagnostics | "0.013592800225591856" | 0.0136 | 0.0136 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=cc_p |
| COVERAGE_BILL_FROZEN_F_HITS / table:diagnostics | "4" | 4 | 4 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=hits |
| COVERAGE_BILL_FROZEN_F_N / table:diagnostics | "40" | 40 | 40 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=n |
| COVERAGE_BILL_FROZEN_F_POF_P / table:diagnostics | "0.1986410814587244" | 0.199 | 0.199 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=pof_p |
| COVERAGE_BILL_FROZEN_F_CC_P / table:diagnostics | "0.26189986860444203" | 0.262 | 0.262 | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=cc_p |
| FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / abstract | "-14.766762552613885" | -14.8 | -14.77 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent |
| FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT / abstract | -16.62356533682211 | -16.6 | -16.62 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/ratio_change_percent |
| PANEL_E5_QR33_EXPANDED_LOSSES / abstract | 34 | 34 | 34 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/losing_to_F |
| PANEL_E5_PLANNED / abstract | 48 | 48 | 48 | results/supervisor-20261023/e5/descriptive-summary.json /planned_cells |
| FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / sec:intro:3 | "-14.766762552613885" | -14.8 | -14.77 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent |
| FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT / sec:intro:3 | -16.62356533682211 | -16.6 | -16.62 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/ratio_change_percent |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT / sec:intro:4 | "376" | 376 | 376 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_left |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT / sec:intro:4 | "360" | 360 | 360 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_right |
| FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / sec:results:0 | "-14.766762552613885" | -14.8 | -14.77 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent |
| FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT / sec:results:0 | -16.62356533682211 | -16.6 | -16.62 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/ratio_change_percent |
| FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT / sec:results:1 | -14.99691078803782 | -15.0 | -15.00 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_minus_f_loss_percent |
| FX_ACI_H6_W2880_QR_HITS / sec:results:1 | 329 | 329 | 329 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_hits |
| FX_ACI_H6_W2880_F_HITS / sec:results:1 | 328 | 328 | 328 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/f_hits |
| FX_TAU90_MATCHED_MEAN_LOSS_CHANGE_PERCENT / sec:results:2 | -10.145914078498173 | -10.15 | -10.15 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/mean_loss_change_percent |
| FX_TAU90_PRIMARY_MEAN_LOSS_CHANGE_PERCENT / sec:results:2 | -9.204288754403045 | -9.20 | -9.20 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/mean_loss_change_percent |
| FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / sec:results:3 | "-12.660126412969763" | -12.7 | -12.66 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=relative_mean_loss_difference_percent |
| FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT / sec:results:3 | 3.1681985293173343 | +3.2 | 3.17 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/ratio_change_percent |
| FX_LATE_SHORT_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT / sec:results:4 | "31.503964246480916" | 31.50 | 31.50 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=relative_mean_loss_difference_percent |
| FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_LEFT / sec:results:4 | "924" | 924 | 924 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=strict_breach_count_left |
| FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_RIGHT / sec:results:4 | "427" | 427 | 427 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=strict_breach_count_right |
| PANEL_BILL_QR_H6_W260_LOSS_PERCENT / sec:results:5 | "50.78571256749063" | +50.8 | 50.79 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=relative_mean_loss_difference_percent |
| PANEL_BILL_QR_H6_W260_QR_HITS / sec:results:5 | "54" | 54 | 54 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=strict_breach_count_left |
| PANEL_BILL_QR_H6_W260_F_HITS / sec:results:5 | "28" | 28 | 28 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=strict_breach_count_right |
| PANEL_E5_QR33_MEDIAN / sec:results:6 | 92.62799824594052 | +92.6 | 92.6 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/median_percent_vs_F |
| PANEL_E5_QR33_EXPANDED_MEDIAN / sec:results:6 | 9.220703399904492 | +9.2 | 9.2 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/median_percent_vs_F |
| PANEL_E5_QR33_EXPANDED_LOSSES / sec:results:6 | 34 | 34 | 34 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/losing_to_F |
| PANEL_E5_PLANNED / sec:results:6 | 48 | 48 | 48 | results/supervisor-20261023/e5/descriptive-summary.json /planned_cells |
| PANEL_WP3_BILL_PRIMARY_MEDIAN_VS_F / sec:results:7 | -3.9812983393045176 | -3.98 | -3.98 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/3/percent_vs_F |
| PANEL_WP3_BILL_PRIMARY_MEAN_VS_F / sec:results:7 | 2.7730553886759823 | 2.77 | 2.77 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/2/percent_vs_F |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT / sec:results:8 | "376" | 376 | 376 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_left |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT / sec:results:8 | "360" | 360 | 360 | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_right |
| FX_PREFERENCE_H24_REVERSAL_RATIO / sec:results:9 | "20.6308977263" | 20.6 | 20.6 | results/revision-20261022/preference-robustness/README.md where={}; field= |

## 任务点名的额外核对

| 项目 | revision-v8 原值 | PR5 原值 | 来源 |
|---|---|---|---|
| ORDINARY_I_RETRO_WORST | 36.50893744342638 | 36.50893744342638 | results/supervisor-20261023/r6/summary.csv where={"phase":"retro","source":"nyfed_weekly","series_key":"PDPOSGSC-L2","horizon":"24","window":"52","report":"I"}; field=percent_vs_F |
| ONE_SE_RETRO_BILL_H24_W52_WORST | 181.39452368014167 | 181.39452368014167 | results/supervisor-20261023/r6/retro-summary.csv where={"source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R2"}; field=percent_vs_F |
| One-standard-error 选普通 I | 17 / 26 | 17 / 26 | `r6/retro-summary.csv`：source=nyfed_weekly, report=R2；按 selected_id=I 逐行计数，26 行完整记录见 JSON |

其中 181.39452368014167 是 PDPOSGS-B、H=24、W=52、R2 的最差损失增加；36.50893744342638 是另一格 PDPOSGSC-L2、H=24、W=52、I 的最差增加，不能混成同一格。原始 Treasury +50.78571256749063 对应 W=260 的原评估；早期 +144.296201250835 对应 W=52 结构类比。

## HAC p 值与比较族

主要原始/匹配检验的整行在 JSON 中保留，包括双带宽与 HLN 项；本表选原始 DM、HLN 和明确命名的调整。

| 归档 / 对比 | DM p | HLN p | 家族与调整原值 |
|---|---|---|---|
| results/supervisor-20261023/inference/dm-verified.csv fx_hourly-h6-QR2880-minus-frozen_F2880 | 4.472961414014163e-09 | 4.82747017649871e-09 | {"holm_family_size": "72", "holm_p": "2.8626953049690645e-07"} |
| results/supervisor-20261023/inference/dm-verified.csv fx_hourly-h6-QR2880-minus-rolling_F720 | 2.1950725127844084e-07 | 2.312477658474048e-07 | {"holm_family_size": "", "holm_p": ""} |
| results/supervisor-20261023/inference/dm-verified.csv nyfed_weekly-h6-QR260-minus-frozen_F260 | 0.007611369596467356 | 0.009390617005130322 | {"holm_family_size": "72", "holm_p": "0.31967752305162894"} |
| results/supervisor-20261023/w3/dm-family.csv fx_hourly-h6-QR2880-minus-frozen_F2880 | 4.472961414014163e-09 | 4.82747017649871e-09 | {"family": "remaining_matched_71", "holm_family_size": "71", "holm_p": "2.817965690828923e-07", "archived72_holm_family_size": "72", "archived72_holm_p": "2.8626953049690645e-07", "primary_bonferroni_family_size": "", "primary_bonferroni_p": ""} |
| results/supervisor-20261023/w3/dm-family.csv fx_hourly-h6-QR2880-minus-rolling_F720 | 2.1950725127844084e-07 | 2.312477658474048e-07 | {"family": "source_primaries_2", "holm_family_size": "", "holm_p": "", "archived72_holm_family_size": "", "archived72_holm_p": "", "primary_bonferroni_family_size": "2", "primary_bonferroni_p": "4.390145025568817e-07"} |
| results/supervisor-20261023/w3/dm-family.csv nyfed_weekly-h6-QR260-minus-frozen_F260 | 0.007611369596467356 | 0.009390617005130322 | {"family": "source_primaries_2", "holm_family_size": "", "holm_p": "", "archived72_holm_family_size": "72", "archived72_holm_p": "0.31967752305162894", "primary_bonferroni_family_size": "2", "primary_bonferroni_p": "0.015222739192934712"} |
| Earlier FX matched_frozen_F2880_d24 | 2.937322779608827e-05 | 未出 HLN | 描述性 normal HAC；L=7；无多重校正；QR/R0 原三罚项，并非 R2 |
| Earlier FX original_primary_rolling_F720_d1 | 0.5735832734537913 | 未出 HLN | 描述性 normal HAC；L=7；无多重校正；QR/R0 原三罚项，并非 R2 |

原始 matched Holm 使用 72 项。后来的重分组是事后划分：两项 source primaries 用 Bonferroni，其余 matched 71 项用 Holm。原始 72 项的调整和后分组调整不能互换。Treasury 原格 DM p=0.007611…、HLN p=0.009390…；在原始 72 家族 Holm 约 0.320，而在两项 Bonferroni 家族约 0.0152；不同家族数字相异不属于两个 v8 的结果冲突。

## 显示差别与归档差别分开

归档差别：**0**。本地 v8 表 3/4 的主要百分比用一位小数，PR5 仍多用两位小数，例如 -14.8 / -14.77、+144.3 / +144.30、181.4 / 181.39；科学计数法 2.2e-07 / 2.20e-07 和 0.32 / 0.320 也只有显示差别。JSON 的 actual_document_table_rows 同时保留两稿实际表格行，避免仅据旧排版回执判断。

## PR5 独有真实证据（不是共享数字）

### WP4 同做市商日频 FX

`results/revision-v8/wp4/summary.json`；SHA-256 `bac2c595a4d06419e4e38606360cf59989ccecb674c32797be61b58171884b12`。四个几何格、两种 QR，共 8 对比全部 COMPLETE；F 胜 7 格，QR33 四格全败。唯一 QR 胜格为 QR4、W260/H6，-2.9739933765508653%。

| W | H | QR | 相对 F 原值 (%) | N |
|---|---|---|---|---|
| 52 | 6 | QR33 | 93.58585225605731 | 501 |
| 52 | 6 | QR4 | 88.1280685610611 | 501 |
| 52 | 24 | QR33 | 122.58857446533482 | 501 |
| 52 | 24 | QR4 | 103.71907462675436 | 501 |
| 260 | 6 | QR33 | 21.872717170090738 | 501 |
| 260 | 6 | QR4 | -2.9739933765508653 | 501 |
| 260 | 24 | QR33 | 40.33518872078312 | 501 |
| 260 | 24 | QR4 | 15.626613176471604 | 501 |

### WP5 扩展已检视回溯

`results/revision-v8/wp5/summary.json`；SHA-256 `7b349dcd341f42b1b5f23b65f0f47673d56a90fcb50380ae4f8d5d012c544629`。这套更长前缀与早期回溯重叠，既有观测和目标路径事先看过；结果为描述性、探索性。共有三窗口汇总见 `results/revision-v8/wp5/three-window-summary.json`，哈希和原字段同存 JSON。

| H | QR | 参考 | 相对损失原值 (%) | breaches QR / F | N | normal DM p |
|---|---|---|---|---|---|---|
| 6 | QR33 | F_matched | -12.166526643171782 | 416 / 282 | 7368 | 0.00043544197837010185 |
| 6 | QR33 | F_rolling720 | -5.29573502748879 | 416 / 387 | 7368 | 0.05505865409429612 |
| 6 | QR4 | F_matched | -7.619791687121458 | 290 / 282 | 7368 | 0.01248062106004164 |
| 6 | QR4 | F_rolling720 | -0.39333078932036747 | 290 / 387 | 7368 | 0.8593873528410942 |
| 24 | QR33 | F_matched | -17.53791852263443 | 470 / 275 | 7368 | 0.04587411834032745 |
| 24 | QR33 | F_rolling720 | 2.729637545911623 | 470 / 477 | 7368 | 0.7524145458262981 |
| 24 | QR4 | F_matched | -21.0273891000744 | 355 / 275 | 7368 | 0.0054706997930857384 |
| 24 | QR4 | F_rolling720 | -1.6174761968566265 | 355 / 477 | 7368 | 0.819577070706853 |

WP3 72 格模拟和本地 v8 的 D0/D2/D1 缺失模拟是不同设计，均不计入共享真实数据数字。旧目录 results/data 独有文件全部位于 `results/v8/mc/`；新目录的新增真实结果位于 wp4 与 wp5。

## 完整共享真实证据原字段清单

以下逐行显示同一源字段在两边的实际原值；来源路径相对各自根目录。SHA-256、CSV 精确选择器、JSON 指针及 typed equality 见对应 JSON。

| ID | revision-v8 原值 | PR5 原值 | 来源 / 字段 |
|---|---|---|---|
| FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT | "-12.660126412969763" | "-12.660126412969763" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=relative_mean_loss_difference_percent |
| FX_LATE_PRIMARY_H6_MEAN_PINBALL_LEFT | "385844.8854897607" | "385844.8854897607" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=mean_pinball_left |
| FX_LATE_PRIMARY_H6_MEAN_PINBALL_RIGHT | "441774.03703851684" | "441774.03703851684" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=mean_pinball_right |
| FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_LEFT | "376" | "376" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=strict_breach_count_left |
| FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_RIGHT | "332" | "332" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=strict_breach_count_right |
| FX_LATE_PRIMARY_H6_ORIGIN_COUNT | "6625" | "6625" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=origin_count |
| FX_LATE_PRIMARY_H6_MEAN_POSITIVE_OVERRUN_DIFFERENCE | "-10408.03273273336" | "-10408.03273273336" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=mean_positive_overrun_difference |
| FX_LATE_PRIMARY_H6_MEAN_UNUSED_ALLOWANCE_DIFFERENCE | "-920830.4090531879" | "-920830.4090531879" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=mean_unused_allowance_difference |
| FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT | "-14.766762552613885" | "-14.766762552613885" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent |
| FX_LATE_MATCHED_H6_MEAN_PINBALL_LEFT | "385844.8854897607" | "385844.8854897607" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=mean_pinball_left |
| FX_LATE_MATCHED_H6_MEAN_PINBALL_RIGHT | "452692.9834478481" | "452692.9834478481" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=mean_pinball_right |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT | "376" | "376" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_left |
| FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT | "360" | "360" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_right |
| FX_LATE_MATCHED_H6_ORIGIN_COUNT | "6625" | "6625" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=origin_count |
| FX_LATE_MATCHED_H6_MEAN_POSITIVE_OVERRUN_DIFFERENCE | "-29549.203192461686" | "-29549.203192461686" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=mean_positive_overrun_difference |
| FX_LATE_MATCHED_H6_MEAN_UNUSED_ALLOWANCE_DIFFERENCE | "-775527.0985049764" | "-775527.0985049764" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=mean_unused_allowance_difference |
| FX_LATE_SHORT_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT | "-2.1167271486370858" | "-2.1167271486370858" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=relative_mean_loss_difference_percent |
| FX_LATE_SHORT_H6_MEAN_PINBALL_LEFT | "433246.30769461836" | "433246.30769461836" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=mean_pinball_left |
| FX_LATE_SHORT_H6_MEAN_PINBALL_RIGHT | "442615.265176624" | "442615.265176624" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=mean_pinball_right |
| FX_LATE_SHORT_H6_STRICT_BREACH_COUNT_LEFT | "531" | "531" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=strict_breach_count_left |
| FX_LATE_SHORT_H6_STRICT_BREACH_COUNT_RIGHT | "332" | "332" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=strict_breach_count_right |
| FX_LATE_SHORT_H6_ORIGIN_COUNT | "6625" | "6625" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=origin_count |
| FX_LATE_SHORT_H6_MEAN_POSITIVE_OVERRUN_DIFFERENCE | "36457.94386399208" | "36457.94386399208" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=mean_positive_overrun_difference |
| FX_LATE_SHORT_H6_MEAN_UNUSED_ALLOWANCE_DIFFERENCE | "-880080.083055962" | "-880080.083055962" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=mean_unused_allowance_difference |
| FX_LATE_SHORT_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT | "31.503964246480916" | "31.503964246480916" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=relative_mean_loss_difference_percent |
| FX_LATE_SHORT_H24_MEAN_PINBALL_LEFT | "1035482.7551213254" | "1035482.7551213254" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=mean_pinball_left |
| FX_LATE_SHORT_H24_MEAN_PINBALL_RIGHT | "787415.6197911236" | "787415.6197911236" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=mean_pinball_right |
| FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_LEFT | "924" | "924" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=strict_breach_count_left |
| FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_RIGHT | "427" | "427" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=strict_breach_count_right |
| FX_LATE_SHORT_H24_ORIGIN_COUNT | "6625" | "6625" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=origin_count |
| FX_LATE_SHORT_H24_MEAN_POSITIVE_OVERRUN_DIFFERENCE | "393138.10588744807" | "393138.10588744807" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=mean_positive_overrun_difference |
| FX_LATE_SHORT_H24_MEAN_UNUSED_ALLOWANCE_DIFFERENCE | "-2508281.3052574797" | "-2508281.3052574797" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=mean_unused_allowance_difference |
| FX_LATE_LONG_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT | "-3.7577697957958187" | "-3.7577697957958187" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent |
| FX_LATE_LONG_H24_MEAN_PINBALL_LEFT | "734695.0685732415" | "734695.0685732415" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=mean_pinball_left |
| FX_LATE_LONG_H24_MEAN_PINBALL_RIGHT | "763381.1758251915" | "763381.1758251915" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=mean_pinball_right |
| FX_LATE_LONG_H24_STRICT_BREACH_COUNT_LEFT | "531" | "531" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=strict_breach_count_left |
| FX_LATE_LONG_H24_STRICT_BREACH_COUNT_RIGHT | "357" | "357" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=strict_breach_count_right |
| FX_LATE_LONG_H24_ORIGIN_COUNT | "6625" | "6625" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=origin_count |
| FX_LATE_LONG_H24_MEAN_POSITIVE_OVERRUN_DIFFERENCE | "74765.69586074568" | "74765.69586074568" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=mean_positive_overrun_difference |
| FX_LATE_LONG_H24_MEAN_UNUSED_ALLOWANCE_DIFFERENCE | "-1994270.366393168" | "-1994270.366393168" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=mean_unused_allowance_difference |
| FX_LATE_LEGACY_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT | "-1.8290714567022697" | "-1.8290714567022697" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=relative_mean_loss_difference_percent |
| FX_LATE_LEGACY_H24_MEAN_PINBALL_LEFT | "734695.0685732415" | "734695.0685732415" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=mean_pinball_left |
| FX_LATE_LEGACY_H24_MEAN_PINBALL_RIGHT | "748383.5382581805" | "748383.5382581805" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=mean_pinball_right |
| FX_LATE_LEGACY_H24_STRICT_BREACH_COUNT_LEFT | "531" | "531" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=strict_breach_count_left |
| FX_LATE_LEGACY_H24_STRICT_BREACH_COUNT_RIGHT | "287" | "287" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=strict_breach_count_right |
| FX_LATE_LEGACY_H24_ORIGIN_COUNT | "6625" | "6625" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=origin_count |
| FX_LATE_LEGACY_H24_MEAN_POSITIVE_OVERRUN_DIFFERENCE | "167864.23163659475" | "167864.23163659475" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=mean_positive_overrun_difference |
| FX_LATE_LEGACY_H24_MEAN_UNUSED_ALLOWANCE_DIFFERENCE | "-3463189.794794077" | "-3463189.794794077" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-rolling_S720"}; field=mean_unused_allowance_difference |
| FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT | -16.62356533682211 | -16.62356533682211 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/ratio_change_percent |
| FX_EARLY_MATCHED_H6_QR_MEAN_LOSS | 286562.4725431636 | 286562.4725431636 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/QR_mean_loss |
| FX_EARLY_MATCHED_H6_F_MEAN_LOSS | 343697.20137447916 | 343697.20137447916 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/F_mean_loss |
| FX_EARLY_MATCHED_H6_MEAN_LOSS_DIFFERENCE_QR_MINUS_F | -57134.728831315566 | -57134.728831315566 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/mean_loss_difference_QR_minus_F |
| FX_EARLY_MATCHED_H6_N | 1440 | 1440 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/n |
| FX_EARLY_MATCHED_H6_ORIGIN_FIRST | 8999 | 8999 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/origin_first |
| FX_EARLY_MATCHED_H6_ORIGIN_LAST | 10438 | 10438 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/origin_last |
| FX_EARLY_MATCHED_H6_SELECTED_LAMBDA | "0.01" | "0.01" | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/selected_lambda |
| FX_EARLY_MATCHED_H6_QR_WINDOW | 2880 | 2880 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/QR_window |
| FX_EARLY_MATCHED_H6_QR_REFIT_STEP | 24 | 24 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/QR_refit_step |
| FX_EARLY_MATCHED_H6_F_WINDOW | 2880 | 2880 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/F_window |
| FX_EARLY_MATCHED_H6_F_REFIT_STEP | 24 | 24 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/F_refit_step |
| FX_EARLY_MATCHED_H6_L | 7 | 7 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/L |
| FX_EARLY_MATCHED_H6_HAC_STATISTIC | -4.178271978163359 | -4.178271978163359 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/HAC_statistic |
| FX_EARLY_MATCHED_H6_TWO_SIDED_NORMAL_HAC_P | 2.937322779608827e-05 | 2.937322779608827e-05 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/two_sided_normal_HAC_p |
| FX_EARLY_MATCHED_H6_MULTIPLICITY_ADJUSTMENT | "none_descriptive_only" | "none_descriptive_only" | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/0/multiplicity_adjustment |
| FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT | 3.1681985293173343 | 3.1681985293173343 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/ratio_change_percent |
| FX_EARLY_PRIMARY_H6_QR_MEAN_LOSS | 286562.4725431636 | 286562.4725431636 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/QR_mean_loss |
| FX_EARLY_PRIMARY_H6_F_MEAN_LOSS | 277762.40801736113 | 277762.40801736113 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/F_mean_loss |
| FX_EARLY_PRIMARY_H6_MEAN_LOSS_DIFFERENCE_QR_MINUS_F | 8800.064525802492 | 8800.064525802492 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/mean_loss_difference_QR_minus_F |
| FX_EARLY_PRIMARY_H6_N | 1440 | 1440 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/n |
| FX_EARLY_PRIMARY_H6_ORIGIN_FIRST | 8999 | 8999 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/origin_first |
| FX_EARLY_PRIMARY_H6_ORIGIN_LAST | 10438 | 10438 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/origin_last |
| FX_EARLY_PRIMARY_H6_SELECTED_LAMBDA | "0.01" | "0.01" | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/selected_lambda |
| FX_EARLY_PRIMARY_H6_QR_WINDOW | 2880 | 2880 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/QR_window |
| FX_EARLY_PRIMARY_H6_QR_REFIT_STEP | 24 | 24 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/QR_refit_step |
| FX_EARLY_PRIMARY_H6_F_WINDOW | 720 | 720 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/F_window |
| FX_EARLY_PRIMARY_H6_F_REFIT_STEP | 1 | 1 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/F_refit_step |
| FX_EARLY_PRIMARY_H6_L | 7 | 7 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/L |
| FX_EARLY_PRIMARY_H6_HAC_STATISTIC | 0.5627820958725974 | 0.5627820958725974 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/HAC_statistic |
| FX_EARLY_PRIMARY_H6_TWO_SIDED_NORMAL_HAC_P | 0.5735832734537913 | 0.5735832734537913 | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/two_sided_normal_HAC_p |
| FX_EARLY_PRIMARY_H6_MULTIPLICITY_ADJUSTMENT | "none_descriptive_only" | "none_descriptive_only" | results/supervisor-20261023/r6-writing-hac-20261023/results.json /comparisons/1/multiplicity_adjustment |
| FX_EARLY_SCOPE_SCOPE | "Post-result descriptive, nonconfirmatory paired unconditional HAC comparisons of two fixed references for the same retrospective conditional QR report. The original-three-menu validation selected lambda 0.01, also selected by R0 in this group. These are QR-versus-F comparisons, not R2 results. The R6 rules followed earlier inspected results; the bounded repository audit found no prior evaluation role for these earlier origins, but the raw history was familiar. These p-values are a later writing-stage readback and do not account for the whole selection and inspection process or supply confirmatory error control, prospective validation, or external replication." | "Post-result descriptive, nonconfirmatory paired unconditional HAC comparisons of two fixed references for the same retrospective conditional QR report. The original-three-menu validation selected lambda 0.01, also selected by R0 in this group. These are QR-versus-F comparisons, not R2 results. The R6 rules followed earlier inspected results; the bounded repository audit found no prior evaluation role for these earlier origins, but the raw history was familiar. These p-values are a later writing-stage readback and do not account for the whole selection and inspection process or supply confirmatory error control, prospective validation, or external replication." | results/supervisor-20261023/r6-writing-hac-20261023/results.json /scope |
| FX_EARLY_SCOPE_EXPERIMENT_OR_REFIT | false | false | results/supervisor-20261023/r6-writing-hac-20261023/results.json /experiment_or_refit |
| FX_EARLY_SCOPE_CANDIDATE_RESELECTION | false | false | results/supervisor-20261023/r6-writing-hac-20261023/results.json /candidate_reselection |
| FX_EARLY_MATCHED_R0_STRICT_BREACH_COUNT | "20" | "20" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"R0"}; field=strict_breach_count |
| FX_EARLY_MATCHED_R0_STRICT_BREACH_RATE | "0.013888888888888888" | "0.013888888888888888" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"R0"}; field=strict_breach_rate |
| FX_EARLY_MATCHED_R0_ORIGIN_COUNT | "1440" | "1440" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"R0"}; field=origin_count |
| FX_EARLY_MATCHED_R0_PERCENT_VS_F | "-16.62356533682211" | "-16.62356533682211" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"R0"}; field=percent_vs_F |
| FX_EARLY_MATCHED_F_STRICT_BREACH_COUNT | "16" | "16" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"F"}; field=strict_breach_count |
| FX_EARLY_MATCHED_F_STRICT_BREACH_RATE | "0.011111111111111112" | "0.011111111111111112" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"F"}; field=strict_breach_rate |
| FX_EARLY_MATCHED_F_ORIGIN_COUNT | "1440" | "1440" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"F"}; field=origin_count |
| FX_EARLY_MATCHED_F_PERCENT_VS_F | "0.0" | "0.0" | results/supervisor-20261023/r6/retro-summary.csv where={"phase":"retro","source":"fx_hourly","series_key":"fx_hourly","horizon":"6","window":"2880","report":"F"}; field=percent_vs_F |
| FX_DM_PRIMARY_H6_DM_T | "-5.182010163255102" | "-5.182010163255102" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=dm_t |
| FX_DM_PRIMARY_H6_DM_P | "2.1950725127844084e-07" | "2.1950725127844084e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=dm_p |
| FX_DM_PRIMARY_H6_HLN_T | "-5.177708102311265" | "-5.177708102311265" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=hln_t |
| FX_DM_PRIMARY_H6_HLN_P | "2.312477658474048e-07" | "2.312477658474048e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=hln_p |
| FX_DM_PRIMARY_H6_BANDWIDTH | "10" | "10" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=bandwidth |
| FX_DM_PRIMARY_H6_DOUBLE_BANDWIDTH | "20" | "20" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=double_bandwidth |
| FX_DM_PRIMARY_H6_DOUBLE_DM_P | "3.474598871721835e-07" | "3.474598871721835e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=double_dm_p |
| FX_DM_PRIMARY_H6_FAMILY | "source_primaries_2" | "source_primaries_2" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=family |
| FX_DM_PRIMARY_H6_HOLM_FAMILY_SIZE | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=holm_family_size |
| FX_DM_PRIMARY_H6_HOLM_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=holm_p |
| FX_DM_PRIMARY_H6_HLN_HOLM_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=hln_holm_p |
| FX_DM_PRIMARY_H6_ARCHIVED72_HOLM_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=archived72_holm_p |
| FX_DM_PRIMARY_H6_PRIMARY_BONFERRONI_P | "4.390145025568817e-07" | "4.390145025568817e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=primary_bonferroni_p |
| FX_DM_MATCHED_H6_DM_T | "-5.865679844214457" | "-5.865679844214457" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=dm_t |
| FX_DM_MATCHED_H6_DM_P | "4.472961414014163e-09" | "4.472961414014163e-09" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=dm_p |
| FX_DM_MATCHED_H6_HLN_T | "-5.860810206492443" | "-5.860810206492443" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=hln_t |
| FX_DM_MATCHED_H6_HLN_P | "4.82747017649871e-09" | "4.82747017649871e-09" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=hln_p |
| FX_DM_MATCHED_H6_BANDWIDTH | "10" | "10" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=bandwidth |
| FX_DM_MATCHED_H6_DOUBLE_BANDWIDTH | "20" | "20" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=double_bandwidth |
| FX_DM_MATCHED_H6_DOUBLE_DM_P | "4.454841587785831e-09" | "4.454841587785831e-09" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=double_dm_p |
| FX_DM_MATCHED_H6_FAMILY | "remaining_matched_71" | "remaining_matched_71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=family |
| FX_DM_MATCHED_H6_HOLM_FAMILY_SIZE | "71" | "71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=holm_family_size |
| FX_DM_MATCHED_H6_HOLM_P | "2.817965690828923e-07" | "2.817965690828923e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=holm_p |
| FX_DM_MATCHED_H6_HLN_HOLM_P | "3.0413062111941877e-07" | "3.0413062111941877e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=hln_holm_p |
| FX_DM_MATCHED_H6_ARCHIVED72_HOLM_P | "2.8626953049690645e-07" | "2.8626953049690645e-07" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=archived72_holm_p |
| FX_DM_MATCHED_H6_PRIMARY_BONFERRONI_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=primary_bonferroni_p |
| FX_DM_SHORT_H6_DM_T | "-0.6158931794865111" | "-0.6158931794865111" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=dm_t |
| FX_DM_SHORT_H6_DM_P | "0.5379650233773263" | "0.5379650233773263" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=dm_p |
| FX_DM_SHORT_H6_HLN_T | "-0.6153818701857628" | "-0.6153818701857628" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=hln_t |
| FX_DM_SHORT_H6_HLN_P | "0.5383237026862189" | "0.5383237026862189" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=hln_p |
| FX_DM_SHORT_H6_BANDWIDTH | "10" | "10" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=bandwidth |
| FX_DM_SHORT_H6_DOUBLE_BANDWIDTH | "20" | "20" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=double_bandwidth |
| FX_DM_SHORT_H6_DOUBLE_DM_P | "0.545619455482008" | "0.545619455482008" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=double_dm_p |
| FX_DM_SHORT_H6_FAMILY | "remaining_matched_71" | "remaining_matched_71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=family |
| FX_DM_SHORT_H6_HOLM_FAMILY_SIZE | "71" | "71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=holm_family_size |
| FX_DM_SHORT_H6_HOLM_P | "1.0" | "1.0" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=holm_p |
| FX_DM_SHORT_H6_HLN_HOLM_P | "1.0" | "1.0" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=hln_holm_p |
| FX_DM_SHORT_H6_ARCHIVED72_HOLM_P | "1.0" | "1.0" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=archived72_holm_p |
| FX_DM_SHORT_H6_PRIMARY_BONFERRONI_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h6-QR720-minus-frozen_F720"}; field=primary_bonferroni_p |
| FX_DM_SHORT_H24_DM_T | "3.2227581052382384" | "3.2227581052382384" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=dm_t |
| FX_DM_SHORT_H24_DM_P | "0.0012696272270405155" | "0.0012696272270405155" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=dm_p |
| FX_DM_SHORT_H24_HLN_T | "3.2113264257670964" | "3.2113264257670964" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=hln_t |
| FX_DM_SHORT_H24_HLN_P | "0.0013275508421535195" | "0.0013275508421535195" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=hln_p |
| FX_DM_SHORT_H24_BANDWIDTH | "24" | "24" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=bandwidth |
| FX_DM_SHORT_H24_DOUBLE_BANDWIDTH | "48" | "48" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=double_bandwidth |
| FX_DM_SHORT_H24_DOUBLE_DM_P | "0.004607895774245358" | "0.004607895774245358" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=double_dm_p |
| FX_DM_SHORT_H24_FAMILY | "remaining_matched_71" | "remaining_matched_71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=family |
| FX_DM_SHORT_H24_HOLM_FAMILY_SIZE | "71" | "71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=holm_family_size |
| FX_DM_SHORT_H24_HOLM_P | "0.0660206158061068" | "0.0660206158061068" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=holm_p |
| FX_DM_SHORT_H24_HLN_HOLM_P | "0.06903264379198301" | "0.06903264379198301" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=hln_holm_p |
| FX_DM_SHORT_H24_ARCHIVED72_HOLM_P | "0.06729024303314732" | "0.06729024303314732" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=archived72_holm_p |
| FX_DM_SHORT_H24_PRIMARY_BONFERRONI_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR720-minus-frozen_F720"}; field=primary_bonferroni_p |
| FX_DM_LONG_H24_DM_T | "-0.5040894639524137" | "-0.5040894639524137" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=dm_t |
| FX_DM_LONG_H24_DM_P | "0.6141985104549805" | "0.6141985104549805" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=dm_p |
| FX_DM_LONG_H24_HLN_T | "-0.5023013715829252" | "-0.5023013715829252" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=hln_t |
| FX_DM_LONG_H24_HLN_P | "0.6154722415137552" | "0.6154722415137552" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=hln_p |
| FX_DM_LONG_H24_BANDWIDTH | "24" | "24" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=bandwidth |
| FX_DM_LONG_H24_DOUBLE_BANDWIDTH | "48" | "48" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=double_bandwidth |
| FX_DM_LONG_H24_DOUBLE_DM_P | "0.6570411249016875" | "0.6570411249016875" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=double_dm_p |
| FX_DM_LONG_H24_FAMILY | "remaining_matched_71" | "remaining_matched_71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=family |
| FX_DM_LONG_H24_HOLM_FAMILY_SIZE | "71" | "71" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=holm_family_size |
| FX_DM_LONG_H24_HOLM_P | "1.0" | "1.0" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=holm_p |
| FX_DM_LONG_H24_HLN_HOLM_P | "1.0" | "1.0" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=hln_holm_p |
| FX_DM_LONG_H24_ARCHIVED72_HOLM_P | "1.0" | "1.0" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=archived72_holm_p |
| FX_DM_LONG_H24_PRIMARY_BONFERRONI_P | "" | "" | results/supervisor-20261023/w3/dm-family.csv where={"contrast_id":"fx_hourly-h24-QR2880-minus-frozen_F2880"}; field=primary_bonferroni_p |
| FX_COVERAGE_QR_N | "947" | "947" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=n |
| FX_COVERAGE_QR_HITS | "50" | "50" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=hits |
| FX_COVERAGE_QR_RATE | "0.05279831045406547" | "0.05279831045406547" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=rate |
| FX_COVERAGE_QR_POF_P | "0.6952768918173253" | "0.6952768918173253" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=pof_p |
| FX_COVERAGE_QR_CC_P | "0.6361520236127319" | "0.6361520236127319" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=cc_p |
| FX_COVERAGE_QR_CC_INITIALIZATION | "condition_on_first_hit_n_minus_1" | "condition_on_first_hit_n_minus_1" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=cc_initialization |
| FX_COVERAGE_QR_GRID_STRIDE | "7" | "7" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"QR"}; field=grid_stride |
| FX_COVERAGE_PRIMARY_F_N | "947" | "947" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=n |
| FX_COVERAGE_PRIMARY_F_HITS | "49" | "49" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=hits |
| FX_COVERAGE_PRIMARY_F_RATE | "0.05174234424498416" | "0.05174234424498416" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=rate |
| FX_COVERAGE_PRIMARY_F_POF_P | "0.8067032386212847" | "0.8067032386212847" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=pof_p |
| FX_COVERAGE_PRIMARY_F_CC_P | "0.9050821379899511" | "0.9050821379899511" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=cc_p |
| FX_COVERAGE_PRIMARY_F_CC_INITIALIZATION | "condition_on_first_hit_n_minus_1" | "condition_on_first_hit_n_minus_1" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=cc_initialization |
| FX_COVERAGE_PRIMARY_F_GRID_STRIDE | "7" | "7" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"720","method":"rolling_F"}; field=grid_stride |
| FX_COVERAGE_MATCHED_F_N | "947" | "947" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=n |
| FX_COVERAGE_MATCHED_F_HITS | "49" | "49" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=hits |
| FX_COVERAGE_MATCHED_F_RATE | "0.05174234424498416" | "0.05174234424498416" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=rate |
| FX_COVERAGE_MATCHED_F_POF_P | "0.8067032386212847" | "0.8067032386212847" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=pof_p |
| FX_COVERAGE_MATCHED_F_CC_P | "0.645851306104558" | "0.645851306104558" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=cc_p |
| FX_COVERAGE_MATCHED_F_CC_INITIALIZATION | "condition_on_first_hit_n_minus_1" | "condition_on_first_hit_n_minus_1" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=cc_initialization |
| FX_COVERAGE_MATCHED_F_GRID_STRIDE | "7" | "7" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"fx_hourly","horizon":"6","window":"2880","method":"frozen_F"}; field=grid_stride |
| FX_MURPHY_H6_RANKING | "CROSSING" | "CROSSING" | results/supervisor-20261023/inference/murphy-verified.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=ranking |
| FX_MURPHY_H6_SIGN_CROSSING_COUNT | "11" | "11" | results/supervisor-20261023/inference/murphy-verified.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=sign_crossing_count |
| FX_MURPHY_H6_MIN_ELEMENTARY_DIFFERENCE | "-0.004430188679245283" | "-0.004430188679245283" | results/supervisor-20261023/inference/murphy-verified.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=min_elementary_difference |
| FX_MURPHY_H6_MAX_ELEMENTARY_DIFFERENCE | "0.0011622641509433963" | "0.0011622641509433963" | results/supervisor-20261023/inference/murphy-verified.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=max_elementary_difference |
| FX_MURPHY_H6_ALL_REAL_THRESHOLDS_COVERED | "True" | "True" | results/supervisor-20261023/inference/murphy-verified.csv where={"contrast_id":"fx_hourly-h6-QR2880-minus-rolling_F720"}; field=all_real_thresholds_covered |
| FX_PREFERENCE_H6_PRIMARY_RELATION | "left_dominates" | "left_dominates" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/0/relation |
| FX_PREFERENCE_H6_PRIMARY_EQUALITY_ALPHA | null | null | results/revision-20261022/preference-robustness/results.json /headline_comparisons/0/equality_alpha |
| FX_PREFERENCE_H6_PRIMARY_HORIZON | 6 | 6 | results/revision-20261022/preference-robustness/results.json /headline_comparisons/0/horizon |
| FX_PREFERENCE_H6_PRIMARY_LEFT_METHOD | "QR" | "QR" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/0/left_method |
| FX_PREFERENCE_H6_PRIMARY_RIGHT_METHOD | "rolling_F" | "rolling_F" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/0/right_method |
| FX_PREFERENCE_H6_MATCHED_RELATION | "left_dominates" | "left_dominates" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/1/relation |
| FX_PREFERENCE_H6_MATCHED_EQUALITY_ALPHA | null | null | results/revision-20261022/preference-robustness/results.json /headline_comparisons/1/equality_alpha |
| FX_PREFERENCE_H6_MATCHED_HORIZON | 6 | 6 | results/revision-20261022/preference-robustness/results.json /headline_comparisons/1/horizon |
| FX_PREFERENCE_H6_MATCHED_LEFT_METHOD | "QR" | "QR" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/1/left_method |
| FX_PREFERENCE_H6_MATCHED_RIGHT_METHOD | "frozen_F" | "frozen_F" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/1/right_method |
| FX_PREFERENCE_H24_LEGACY_RELATION | "crosses" | "crosses" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/2/relation |
| FX_PREFERENCE_H24_LEGACY_EQUALITY_ALPHA | "86579744869851975/90776350660766843" | "86579744869851975/90776350660766843" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/2/equality_alpha |
| FX_PREFERENCE_H24_LEGACY_HORIZON | 24 | 24 | results/revision-20261022/preference-robustness/results.json /headline_comparisons/2/horizon |
| FX_PREFERENCE_H24_LEGACY_LEFT_METHOD | "QR" | "QR" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/2/left_method |
| FX_PREFERENCE_H24_LEGACY_RIGHT_METHOD | "rolling_S" | "rolling_S" | results/revision-20261022/preference-robustness/results.json /headline_comparisons/2/right_method |
| FX_PREFERENCE_H24_REVERSAL_RATIO | "20.6308977263" | "20.6308977263" | results/revision-20261022/preference-robustness/README.md where={}; field= |
| FX_ACI_H6_W720_STATUS | "COMPLETE" | "COMPLETE" | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/status |
| FX_ACI_H6_W720_QR_MINUS_F_LOSS_PERCENT | -6.982528592685567 | -6.982528592685567 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/qr_minus_f_loss_percent |
| FX_ACI_H6_W720_QR_MEAN_LOSS | 439672.91206129093 | 439672.91206129093 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/qr_mean_loss |
| FX_ACI_H6_W720_F_MEAN_LOSS | 472677.77269068744 | 472677.77269068744 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/f_mean_loss |
| FX_ACI_H6_W720_QR_HITS | 352 | 352 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/qr_hits |
| FX_ACI_H6_W720_F_HITS | 331 | 331 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/f_hits |
| FX_ACI_H6_W720_N | 6625 | 6625 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/n |
| FX_ACI_H6_W720_QR_RATE | 0.05313207547169811 | 0.05313207547169811 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/qr_rate |
| FX_ACI_H6_W720_F_RATE | 0.049962264150943396 | 0.049962264150943396 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/f_rate |
| FX_ACI_H6_W720_QR_COVERAGE_DISTANCE | 0.003132075471698109 | 0.003132075471698109 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/qr_coverage_distance |
| FX_ACI_H6_W720_F_COVERAGE_DISTANCE | 3.773584905660682e-05 | 3.773584905660682e-05 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/0/f_coverage_distance |
| FX_ACI_H6_W2880_STATUS | "COMPLETE" | "COMPLETE" | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/status |
| FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT | -14.99691078803782 | -14.99691078803782 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_minus_f_loss_percent |
| FX_ACI_H6_W2880_QR_MEAN_LOSS | 393795.05776986334 | 393795.05776986334 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_mean_loss |
| FX_ACI_H6_W2880_F_MEAN_LOSS | 463271.4662733057 | 463271.4662733057 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/f_mean_loss |
| FX_ACI_H6_W2880_QR_HITS | 329 | 329 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_hits |
| FX_ACI_H6_W2880_F_HITS | 328 | 328 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/f_hits |
| FX_ACI_H6_W2880_N | 6625 | 6625 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/n |
| FX_ACI_H6_W2880_QR_RATE | 0.04966037735849057 | 0.04966037735849057 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_rate |
| FX_ACI_H6_W2880_F_RATE | 0.04950943396226415 | 0.04950943396226415 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/f_rate |
| FX_ACI_H6_W2880_QR_COVERAGE_DISTANCE | 0.0003396226415094336 | 0.0003396226415094336 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/qr_coverage_distance |
| FX_ACI_H6_W2880_F_COVERAGE_DISTANCE | 0.0004905660377358539 | 0.0004905660377358539 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1/f_coverage_distance |
| FX_ACI_H24_W720_STATUS | "COMPLETE" | "COMPLETE" | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/status |
| FX_ACI_H24_W720_QR_MINUS_F_LOSS_PERCENT | 10.72474300913029 | 10.72474300913029 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/qr_minus_f_loss_percent |
| FX_ACI_H24_W720_QR_MEAN_LOSS | 1020220.0873449822 | 1020220.0873449822 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/qr_mean_loss |
| FX_ACI_H24_W720_F_MEAN_LOSS | 921402.0819726406 | 921402.0819726406 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/f_mean_loss |
| FX_ACI_H24_W720_QR_HITS | 393 | 393 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/qr_hits |
| FX_ACI_H24_W720_F_HITS | 322 | 322 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/f_hits |
| FX_ACI_H24_W720_N | 6625 | 6625 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/n |
| FX_ACI_H24_W720_QR_RATE | 0.05932075471698113 | 0.05932075471698113 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/qr_rate |
| FX_ACI_H24_W720_F_RATE | 0.04860377358490566 | 0.04860377358490566 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/f_rate |
| FX_ACI_H24_W720_QR_COVERAGE_DISTANCE | 0.009320754716981128 | 0.009320754716981128 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/qr_coverage_distance |
| FX_ACI_H24_W720_F_COVERAGE_DISTANCE | 0.0013962264150943413 | 0.0013962264150943413 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/2/f_coverage_distance |
| FX_ACI_H24_W2880_STATUS | "COMPLETE" | "COMPLETE" | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/status |
| FX_ACI_H24_W2880_QR_MINUS_F_LOSS_PERCENT | -4.480242144763569 | -4.480242144763569 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/qr_minus_f_loss_percent |
| FX_ACI_H24_W2880_QR_MEAN_LOSS | 755982.7014517846 | 755982.7014517846 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/qr_mean_loss |
| FX_ACI_H24_W2880_F_MEAN_LOSS | 791441.1828781047 | 791441.1828781047 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/f_mean_loss |
| FX_ACI_H24_W2880_QR_HITS | 294 | 294 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/qr_hits |
| FX_ACI_H24_W2880_F_HITS | 323 | 323 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/f_hits |
| FX_ACI_H24_W2880_N | 6625 | 6625 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/n |
| FX_ACI_H24_W2880_QR_RATE | 0.04437735849056604 | 0.04437735849056604 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/qr_rate |
| FX_ACI_H24_W2880_F_RATE | 0.048754716981132075 | 0.048754716981132075 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/f_rate |
| FX_ACI_H24_W2880_QR_COVERAGE_DISTANCE | 0.005622641509433965 | 0.005622641509433965 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/qr_coverage_distance |
| FX_ACI_H24_W2880_F_COVERAGE_DISTANCE | 0.0012452830188679279 | 0.0012452830188679279 | results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/3/f_coverage_distance |
| FX_ACI_H6_LONG_DM_MEAN_DIFFERENCE | -69476.40850344242 | -69476.40850344242 | results/revision-20261023/v6/wp2-comparisons.json /rows/49/mean_difference |
| FX_ACI_H6_LONG_DM_DM_P | 3.457942781347373e-07 | 3.457942781347373e-07 | results/revision-20261023/v6/wp2-comparisons.json /rows/49/dm_p |
| FX_ACI_H6_LONG_DM_HLN_P | 3.6336772003486773e-07 | 3.6336772003486773e-07 | results/revision-20261023/v6/wp2-comparisons.json /rows/49/hln_p |
| FX_ACI_H6_LONG_DM_HOLM_P | 1.8327096741141078e-05 | 1.8327096741141078e-05 | results/revision-20261023/v6/wp2-comparisons.json /rows/49/holm_p |
| FX_ACI_H6_LONG_DM_N | 6625 | 6625 | results/revision-20261023/v6/wp2-comparisons.json /rows/49/n |
| FX_ACI_H6_LONG_DM_STATUS | "OK" | "OK" | results/revision-20261023/v6/wp2-comparisons.json /rows/49/status |
| FX_STATE_LOW_N | 1593 | 1593 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/0/n |
| FX_STATE_LOW_MEAN_DIFFERENCE | -58761.26651484724 | -58761.26651484724 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/0/mean_difference |
| FX_STATE_LOW_HAC_SE | 16492.94369217626 | 16492.94369217626 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/0/hac_se |
| FX_STATE_MIDDLE_N | 1816 | 1816 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/1/n |
| FX_STATE_MIDDLE_MEAN_DIFFERENCE | -27839.43372761798 | -27839.43372761798 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/1/mean_difference |
| FX_STATE_MIDDLE_HAC_SE | 16257.69788113348 | 16257.69788113348 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/1/hac_se |
| FX_STATE_HIGH_N | 3216 | 3216 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/2/n |
| FX_STATE_HIGH_MEAN_DIFFERENCE | -70387.91038650597 | -70387.91038650597 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/2/mean_difference |
| FX_STATE_HIGH_HAC_SE | 17895.89187185643 | 17895.89187185643 | results/revision-20261023/v6/wp4-states.json /rows/0/groups/2/hac_se |
| FX_STATE_STATE_DEFINITION | "Issue-known position-increment RMS, not price or yield volatility" | "Issue-known position-increment RMS, not price or yield volatility" | results/revision-20261023/v6/wp4-states.json /rows/0/state_definition |
| FX_STATE_FULL_N | 6625 | 6625 | results/revision-20261023/v6/wp4-states.json /rows/0/full_n |
| FX_STATE_CUT1 | 947476.4010013953 | 947476.4010013953 | results/revision-20261023/v6/wp4-states.json /rows/0/cut1 |
| FX_STATE_CUT2 | 1401103.2792395097 | 1401103.2792395097 | results/revision-20261023/v6/wp4-states.json /rows/0/cut2 |
| FX_STATE_TEST_0_TEST | "joint_GW" | "joint_GW" | results/revision-20261023/v6/wp4-states.json /ranking/0/test |
| FX_STATE_TEST_0_RAW_P | 1.4629751215136517e-06 | 1.4629751215136517e-06 | results/revision-20261023/v6/wp4-states.json /ranking/0/raw_p |
| FX_STATE_TEST_0_HOLM_P | 5.851900486054607e-06 | 5.851900486054607e-06 | results/revision-20261023/v6/wp4-states.json /ranking/0/holm_p |
| FX_STATE_TEST_0_STATUS | "OK" | "OK" | results/revision-20261023/v6/wp4-states.json /ranking/0/status |
| FX_STATE_TEST_1_TEST | "group_heterogeneity" | "group_heterogeneity" | results/revision-20261023/v6/wp4-states.json /ranking/1/test |
| FX_STATE_TEST_1_RAW_P | 0.15938333671965318 | 0.15938333671965318 | results/revision-20261023/v6/wp4-states.json /ranking/1/raw_p |
| FX_STATE_TEST_1_HOLM_P | 0.15938333671965318 | 0.15938333671965318 | results/revision-20261023/v6/wp4-states.json /ranking/1/holm_p |
| FX_STATE_TEST_1_STATUS | "OK" | "OK" | results/revision-20261023/v6/wp4-states.json /ranking/1/status |
| FX_TAU90_PRIMARY_TAU | 0.9 | 0.9 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/tau |
| FX_TAU90_PRIMARY_STATUS | "OK" | "OK" | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/status |
| FX_TAU90_PRIMARY_REASON | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/reason |
| FX_TAU90_PRIMARY_SELECTED_PARAMETER | 0.1 | 0.1 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/selected_parameter |
| FX_TAU90_PRIMARY_DIRECTION_REVERSAL | false | false | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/direction_reversal |
| FX_TAU90_PRIMARY_MEAN_DIFFERENCE | -60715.44469989856 | -60715.44469989856 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/mean_difference |
| FX_TAU90_PRIMARY_HOLM_P | 1.3655876903219617e-12 | 1.3655876903219617e-12 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/holm_p |
| FX_TAU90_PRIMARY_MEAN_LOSS_CHANGE_PERCENT | -9.204288754403045 | -9.204288754403045 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/mean_loss_change_percent |
| FX_TAU90_PRIMARY_DM_P | 2.7311753806439233e-13 | 2.7311753806439233e-13 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/dm_p |
| FX_TAU90_PRIMARY_HLN_P | 3.1914659442393274e-13 | 3.1914659442393274e-13 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/hln_p |
| FX_TAU90_PRIMARY_N | 6625 | 6625 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/n |
| FX_TAU90_PRIMARY_QR_SCORES_MEAN_LOSS | 598927.5360883147 | 598927.5360883147 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/qr_scores/mean_loss |
| FX_TAU90_PRIMARY_QR_SCORES_FULL_HITS | 686 | 686 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/qr_scores/full_hits |
| FX_TAU90_PRIMARY_QR_SCORES_FULL_RATE | 0.10354716981132076 | 0.10354716981132076 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/qr_scores/full_rate |
| FX_TAU90_PRIMARY_REFERENCE_SCORES_MEAN_LOSS | 659642.9807882133 | 659642.9807882133 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/reference_scores/mean_loss |
| FX_TAU90_PRIMARY_REFERENCE_SCORES_FULL_HITS | 620 | 620 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/reference_scores/full_hits |
| FX_TAU90_PRIMARY_REFERENCE_SCORES_FULL_RATE | 0.09358490566037736 | 0.09358490566037736 | results/revision-20261023/v6/wp5-tau-summary.json /rows/0/reference_scores/full_rate |
| FX_TAU90_MATCHED_TAU | 0.9 | 0.9 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/tau |
| FX_TAU90_MATCHED_STATUS | "OK" | "OK" | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/status |
| FX_TAU90_MATCHED_REASON | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/reason |
| FX_TAU90_MATCHED_SELECTED_PARAMETER | 0.1 | 0.1 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/selected_parameter |
| FX_TAU90_MATCHED_DIRECTION_REVERSAL | false | false | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/direction_reversal |
| FX_TAU90_MATCHED_MEAN_DIFFERENCE | -67628.1691375431 | -67628.1691375431 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/mean_difference |
| FX_TAU90_MATCHED_HOLM_P | 6.916985591464706e-21 | 6.916985591464706e-21 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/holm_p |
| FX_TAU90_MATCHED_MEAN_LOSS_CHANGE_PERCENT | -10.145914078498173 | -10.145914078498173 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/mean_loss_change_percent |
| FX_TAU90_MATCHED_DM_P | 1.1528309319107842e-21 | 1.1528309319107842e-21 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/dm_p |
| FX_TAU90_MATCHED_HLN_P | 1.711467007218909e-21 | 1.711467007218909e-21 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/hln_p |
| FX_TAU90_MATCHED_N | 6625 | 6625 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/n |
| FX_TAU90_MATCHED_QR_SCORES_MEAN_LOSS | 598927.5360883147 | 598927.5360883147 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/qr_scores/mean_loss |
| FX_TAU90_MATCHED_QR_SCORES_FULL_HITS | 686 | 686 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/qr_scores/full_hits |
| FX_TAU90_MATCHED_QR_SCORES_FULL_RATE | 0.10354716981132076 | 0.10354716981132076 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/qr_scores/full_rate |
| FX_TAU90_MATCHED_REFERENCE_SCORES_MEAN_LOSS | 666555.7052258579 | 666555.7052258579 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/reference_scores/mean_loss |
| FX_TAU90_MATCHED_REFERENCE_SCORES_FULL_HITS | 667 | 667 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/reference_scores/full_hits |
| FX_TAU90_MATCHED_REFERENCE_SCORES_FULL_RATE | 0.10067924528301887 | 0.10067924528301887 | results/revision-20261023/v6/wp5-tau-summary.json /rows/1/reference_scores/full_rate |
| FX_TAU99_PRIMARY_TAU | 0.99 | 0.99 | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/tau |
| FX_TAU99_PRIMARY_STATUS | "NA" | "NA" | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/status |
| FX_TAU99_PRIMARY_REASON | "VALIDATION_INELIGIBLE" | "VALIDATION_INELIGIBLE" | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/reason |
| FX_TAU99_PRIMARY_SELECTED_PARAMETER | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/selected_parameter |
| FX_TAU99_PRIMARY_DIRECTION_REVERSAL | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/direction_reversal |
| FX_TAU99_PRIMARY_MEAN_DIFFERENCE | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/mean_difference |
| FX_TAU99_PRIMARY_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp5-tau-summary.json /rows/3/holm_p |
| FX_TAU99_MATCHED_TAU | 0.99 | 0.99 | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/tau |
| FX_TAU99_MATCHED_STATUS | "NA" | "NA" | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/status |
| FX_TAU99_MATCHED_REASON | "VALIDATION_INELIGIBLE" | "VALIDATION_INELIGIBLE" | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/reason |
| FX_TAU99_MATCHED_SELECTED_PARAMETER | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/selected_parameter |
| FX_TAU99_MATCHED_DIRECTION_REVERSAL | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/direction_reversal |
| FX_TAU99_MATCHED_MEAN_DIFFERENCE | null | null | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/mean_difference |
| FX_TAU99_MATCHED_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp5-tau-summary.json /rows/4/holm_p |
| PANEL_BILL_QR_H6_W52_LOSS_PERCENT | "83.35448336982303" | "83.35448336982303" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR52-minus-frozen_F52"}; field=relative_mean_loss_difference_percent |
| PANEL_BILL_QR_H6_W52_QR_HITS | "84" | "84" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR52-minus-frozen_F52"}; field=strict_breach_count_left |
| PANEL_BILL_QR_H6_W52_F_HITS | "11" | "11" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR52-minus-frozen_F52"}; field=strict_breach_count_right |
| PANEL_BILL_QR_H6_W52_N | "277" | "277" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR52-minus-frozen_F52"}; field=origin_count |
| PANEL_BILL_QR_H6_W52_QR_LOSS | "5095.519389384495" | "5095.519389384495" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR52-minus-frozen_F52"}; field=mean_pinball_left |
| PANEL_BILL_QR_H6_W52_F_LOSS | "2779.053610108303" | "2779.053610108303" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR52-minus-frozen_F52"}; field=mean_pinball_right |
| PANEL_BILL_QR_H6_W260_LOSS_PERCENT | "50.78571256749063" | "50.78571256749063" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=relative_mean_loss_difference_percent |
| PANEL_BILL_QR_H6_W260_QR_HITS | "54" | "54" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=strict_breach_count_left |
| PANEL_BILL_QR_H6_W260_F_HITS | "28" | "28" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=strict_breach_count_right |
| PANEL_BILL_QR_H6_W260_N | "277" | "277" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=origin_count |
| PANEL_BILL_QR_H6_W260_QR_LOSS | "4159.673194735081" | "4159.673194735081" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=mean_pinball_left |
| PANEL_BILL_QR_H6_W260_F_LOSS | "2758.665342960289" | "2758.665342960289" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=mean_pinball_right |
| PANEL_BILL_QR_H24_W52_LOSS_PERCENT | "227.41062414680638" | "227.41062414680638" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR52-minus-frozen_F52"}; field=relative_mean_loss_difference_percent |
| PANEL_BILL_QR_H24_W52_QR_HITS | "132" | "132" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR52-minus-frozen_F52"}; field=strict_breach_count_left |
| PANEL_BILL_QR_H24_W52_F_HITS | "33" | "33" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR52-minus-frozen_F52"}; field=strict_breach_count_right |
| PANEL_BILL_QR_H24_W52_N | "277" | "277" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR52-minus-frozen_F52"}; field=origin_count |
| PANEL_BILL_QR_H24_W52_QR_LOSS | "12165.57410365444" | "12165.57410365444" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR52-minus-frozen_F52"}; field=mean_pinball_left |
| PANEL_BILL_QR_H24_W52_F_LOSS | "3715.693140794224" | "3715.693140794224" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR52-minus-frozen_F52"}; field=mean_pinball_right |
| PANEL_BILL_QR_H24_W260_LOSS_PERCENT | "109.84342115850872" | "109.84342115850872" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR260-minus-frozen_F260"}; field=relative_mean_loss_difference_percent |
| PANEL_BILL_QR_H24_W260_QR_HITS | "84" | "84" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR260-minus-frozen_F260"}; field=strict_breach_count_left |
| PANEL_BILL_QR_H24_W260_F_HITS | "12" | "12" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR260-minus-frozen_F260"}; field=strict_breach_count_right |
| PANEL_BILL_QR_H24_W260_N | "277" | "277" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR260-minus-frozen_F260"}; field=origin_count |
| PANEL_BILL_QR_H24_W260_QR_LOSS | "5204.759632250341" | "5204.759632250341" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR260-minus-frozen_F260"}; field=mean_pinball_left |
| PANEL_BILL_QR_H24_W260_F_LOSS | "2480.3063176895307" | "2480.3063176895307" | results/revision-20261022/paired-comparisons.csv where={"contrast_id":"nyfed_weekly-h24-QR260-minus-frozen_F260"}; field=mean_pinball_right |
| PANEL_BILL_PRIMARY_DM_P | "0.007611369596467356" | "0.007611369596467356" | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=dm_p |
| PANEL_BILL_PRIMARY_HLN_P | "0.009390617005130322" | "0.009390617005130322" | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=hln_p |
| PANEL_BILL_PRIMARY_HOLM_P | "0.31967752305162894" | "0.31967752305162894" | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=holm_p |
| PANEL_BILL_PRIMARY_FAMILY_N | "72" | "72" | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=holm_family_size |
| PANEL_BILL_PRIMARY_STATUS | "OK" | "OK" | results/supervisor-20261023/inference/dm-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=status |
| PANEL_BILL_PRIMARY_MURPHY | "CROSSING" | "CROSSING" | results/supervisor-20261023/inference/murphy-verified.csv where={"contrast_id":"nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=ranking |
| PANEL_R6_BILL_W52_ANALOGUE_LOSS_PERCENT | "144.296201250835" | "144.296201250835" | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=percent_vs_reference |
| PANEL_R6_BILL_W52_ANALOGUE_QR_LOSS | "3058.2172973547076" | "3058.2172973547076" | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=QR_mean_pinball |
| PANEL_R6_BILL_W52_ANALOGUE_F_LOSS | "1251.8480769230769" | "1251.8480769230769" | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=F_mean_pinball |
| PANEL_R6_BILL_W52_ANALOGUE_WINDOW | "52" | "52" | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=window |
| PANEL_R6_BILL_W52_ANALOGUE_REFERENCE | "frozen corrected F W52 d13" | "frozen corrected F W52 d13" | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=reference |
| PANEL_R6_BILL_W52_ANALOGUE_LIMITATION | "W52 structural analogue; original W260 primary not exactly replicated" | "W52 structural analogue; original W260 primary not exactly replicated" | results/supervisor-20261023/r6/primary-replication.csv where={"id":"Treasury-W52-structural-analogue"}; field=limitation |
| PANEL_ORIGINAL_SERIES_COUNT | 12 | 12 | results/revision-20261023/round2/panel/descriptive-counts.json /series_count |
| PANEL_ORIGINAL_SKIPPED_COUNT | 2 | 2 | results/revision-20261023/round2/panel/descriptive-counts.json /skipped_count |
| PANEL_ORIGINAL_CELL_COUNT | 48 | 48 | results/revision-20261023/round2/panel/descriptive-counts.json /QR33/total_cells |
| PANEL_ORIGINAL_QR33_WINS | 3 | 3 | results/revision-20261023/round2/panel/descriptive-counts.json /QR33/lower_loss_than_F |
| PANEL_ORIGINAL_QR33_LOSSES | 45 | 45 | results/revision-20261023/round2/panel/descriptive-counts.json /QR33/higher_loss_than_F |
| PANEL_ORIGINAL_QR4_WINS | 11 | 11 | results/revision-20261023/round2/panel/descriptive-counts.json /C2_QR4/lower_loss_than_F |
| PANEL_ORIGINAL_QR4_LOSSES | 37 | 37 | results/revision-20261023/round2/panel/descriptive-counts.json /C2_QR4/higher_loss_than_F |
| PANEL_ORIGINAL_LEVY_WINS | 19 | 19 | results/revision-20261023/round2/panel/descriptive-counts.json /Levy_L/lower_loss_than_F |
| PANEL_ORIGINAL_LEVY_LOSSES | 29 | 29 | results/revision-20261023/round2/panel/descriptive-counts.json /Levy_L/higher_loss_than_F |
| PANEL_ORIGINAL_LEVY_TOTAL | 48 | 48 | results/revision-20261023/round2/panel/descriptive-counts.json /Levy_L/total_cells |
| PANEL_E5_QR33_MEDIAN | 92.62799824594052 | 92.62799824594052 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/median_percent_vs_F |
| PANEL_E5_QR33_LOSSES | 45 | 45 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/losing_to_F |
| PANEL_E5_QR33_WINS | 3 | 3 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/winning_over_F |
| PANEL_E5_QR33_MIN | -26.42400809091829 | -26.42400809091829 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/minimum_percent_vs_F |
| PANEL_E5_QR33_MAX | 544.3372584055676 | 544.3372584055676 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/maximum_percent_vs_F |
| PANEL_E5_QR33_WITHIN10 | 6 | 6 | results/supervisor-20261023/e5/descriptive-summary.json /original_QR33/within_inclusive_ten_percent |
| PANEL_E5_QR4_MEDIAN | 9.90727239745182 | 9.90727239745182 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/median_percent_vs_F |
| PANEL_E5_QR4_LOSSES | 37 | 37 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/losing_to_F |
| PANEL_E5_QR4_WINS | 11 | 11 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/winning_over_F |
| PANEL_E5_QR4_MIN | -5.787028224177445 | -5.787028224177445 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/minimum_percent_vs_F |
| PANEL_E5_QR4_MAX | 299.11570737413126 | 299.11570737413126 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/maximum_percent_vs_F |
| PANEL_E5_QR4_WITHIN10 | 24 | 24 | results/supervisor-20261023/e5/descriptive-summary.json /QR4_plus/within_inclusive_ten_percent |
| PANEL_E5_QR33_EXPANDED_MEDIAN | 9.220703399904492 | 9.220703399904492 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/median_percent_vs_F |
| PANEL_E5_QR33_EXPANDED_LOSSES | 34 | 34 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/losing_to_F |
| PANEL_E5_QR33_EXPANDED_WINS | 14 | 14 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/winning_over_F |
| PANEL_E5_QR33_EXPANDED_MIN | -6.039089778580286 | -6.039089778580286 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/minimum_percent_vs_F |
| PANEL_E5_QR33_EXPANDED_MAX | 264.79764256040943 | 264.79764256040943 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/maximum_percent_vs_F |
| PANEL_E5_QR33_EXPANDED_WITHIN10 | 24 | 24 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus/within_inclusive_ten_percent |
| PANEL_E5_ORDINARY_I_MEDIAN | 0.5006801691981209 | 0.5006801691981209 | results/supervisor-20261023/e5/descriptive-summary.json /I/median_percent_vs_F |
| PANEL_E5_ORDINARY_I_LOSSES | 30 | 30 | results/supervisor-20261023/e5/descriptive-summary.json /I/losing_to_F |
| PANEL_E5_ORDINARY_I_WINS | 18 | 18 | results/supervisor-20261023/e5/descriptive-summary.json /I/winning_over_F |
| PANEL_E5_ORDINARY_I_MIN | -6.277870770160739 | -6.277870770160739 | results/supervisor-20261023/e5/descriptive-summary.json /I/minimum_percent_vs_F |
| PANEL_E5_ORDINARY_I_MAX | 14.853366598672611 | 14.853366598672611 | results/supervisor-20261023/e5/descriptive-summary.json /I/maximum_percent_vs_F |
| PANEL_E5_ORDINARY_I_WITHIN10 | 46 | 46 | results/supervisor-20261023/e5/descriptive-summary.json /I/within_inclusive_ten_percent |
| PANEL_E5_PLANNED | 48 | 48 | results/supervisor-20261023/e5/descriptive-summary.json /planned_cells |
| PANEL_E5_COMPLETE | 48 | 48 | results/supervisor-20261023/e5/descriptive-summary.json /complete_cells |
| PANEL_E5_EXPANDED_LOWER_THAN_OLD | 31 | 31 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus_relative_to_original_QR33/strictly_lower_cells |
| PANEL_E5_EXPANDED_EQUAL_TO_OLD | 15 | 15 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus_relative_to_original_QR33/exactly_equal_cells |
| PANEL_E5_EXPANDED_HIGHER_THAN_OLD | 2 | 2 | results/supervisor-20261023/e5/descriptive-summary.json /QR33_plus_relative_to_original_QR33/higher_cells |
| PANEL_E5_OLD_MENU_READBACK_ERROR | 0 | 0 | results/supervisor-20261023/e5/descriptive-summary.json /original_menu_validation_readback/maximum_absolute_loss_difference |
| PANEL_E5_NO_INDEPENDENCE | true | true | results/supervisor-20261023/e5/descriptive-summary.json /no_independent_sample_or_pooled_inference |
| PANEL_E5_P1_SUCCESSES | 30 | 30 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P1/success_count |
| PANEL_E5_P1_DENOMINATOR | 45 | 45 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P1/fixed_denominator |
| PANEL_E5_P1_THRESHOLD | 40 | 40 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P1/threshold |
| PANEL_E5_P1_SUPPORTED | false | false | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P1/supported |
| PANEL_E5_P2_SUCCESSES | 24 | 24 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P2/success_count |
| PANEL_E5_P2_DENOMINATOR | 48 | 48 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P2/fixed_denominator |
| PANEL_E5_P2_THRESHOLD | 36 | 36 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P2/threshold |
| PANEL_E5_P2_SUPPORTED | false | false | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P2/supported |
| PANEL_E5_P3_SUCCESSES | 33 | 33 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P3/success_count |
| PANEL_E5_P3_DENOMINATOR | 48 | 48 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P3/fixed_denominator |
| PANEL_E5_P3_THRESHOLD | 25 | 25 | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P3/threshold |
| PANEL_E5_P3_SUPPORTED | true | true | results/supervisor-20261023/e5/prediction-assessment.json /predictions/P3/supported |
| PANEL_R6_S1_STATUS | "NOT_MET" | "NOT_MET" | results/supervisor-20261023/r6/assessment.json /S1/status |
| PANEL_R6_S1_REQUIRED | 26 | 26 | results/supervisor-20261023/r6/assessment.json /S1/complete_required |
| PANEL_R6_S1_COMPLETE | 26 | 26 | results/supervisor-20261023/r6/assessment.json /S1/complete_count |
| PANEL_R6_R2_RETRO_WORST | 181.39452368014167 | 181.39452368014167 | results/supervisor-20261023/r6/assessment.json /S1/worst_percent_vs_F |
| PANEL_R6_R2_RETRO_MEDIAN | 5.374072481175762 | 5.374072481175762 | results/supervisor-20261023/r6/assessment.json /S1/median_percent_vs_F |
| PANEL_R6_S3_STATUS | "NOT_MET" | "NOT_MET" | results/supervisor-20261023/r6/assessment.json /S3/status |
| PANEL_R6_R0_RETRO_COMPLETE | 26 | 26 | results/supervisor-20261023/r6/assessment.json /S3/R0_complete_count |
| PANEL_R6_R2_RETRO_COMPLETE | 26 | 26 | results/supervisor-20261023/r6/assessment.json /S3/R2_complete_count |
| PANEL_R6_R0_RETRO_MEDIAN | 4.1510024714803695 | 4.1510024714803695 | results/supervisor-20261023/r6/assessment.json /S3/R0_median_percent_vs_F |
| PANEL_R6_PUBLICATION_GATE | "ROBUSTNESS_PARAGRAPH" | "ROBUSTNESS_PARAGRAPH" | results/supervisor-20261023/r6/assessment.json /publication_gate/status |
| PANEL_R6_ABSTRACT_MENTION | false | false | results/supervisor-20261023/r6/assessment.json /publication_gate/abstract_mention |
| PANEL_R6_DESCRIPTIVE_ONLY | true | true | results/supervisor-20261023/r6/assessment.json /descriptive_only |
| PANEL_R6_POOLED_TESTS | false | false | results/supervisor-20261023/r6/assessment.json /pooled_tests_performed |
| PANEL_R6_INSPECTED_BILL_H6_W52_R0_LOSS_PERCENT | "-3.2437361473403814" | "-3.2437361473403814" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"52","report":"R0"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H6_W52_R0_HITS | "14" | "14" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"52","report":"R0"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H6_W52_R0_SELECTED | "10" | "10" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"52","report":"R0"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H6_W52_R2_LOSS_PERCENT | "-1.9946015697497543" | "-1.9946015697497543" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"52","report":"R2"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H6_W52_R2_HITS | "14" | "14" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"52","report":"R2"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H6_W52_R2_SELECTED | "I" | "I" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"52","report":"R2"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H6_W260_R0_LOSS_PERCENT | "3.434171780248918" | "3.434171780248918" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"260","report":"R0"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H6_W260_R0_HITS | "32" | "32" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"260","report":"R0"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H6_W260_R0_SELECTED | "1" | "1" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"260","report":"R0"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H6_W260_R2_LOSS_PERCENT | "2.1358341667261804" | "2.1358341667261804" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"260","report":"R2"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H6_W260_R2_HITS | "32" | "32" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"260","report":"R2"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H6_W260_R2_SELECTED | "10" | "10" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"6","window":"260","report":"R2"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H24_W52_R0_LOSS_PERCENT | "4.339873488858559" | "4.339873488858559" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R0"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H24_W52_R0_HITS | "39" | "39" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R0"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H24_W52_R0_SELECTED | "10" | "10" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R0"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H24_W52_R2_LOSS_PERCENT | "6.213226757036927" | "6.213226757036927" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R2"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H24_W52_R2_HITS | "37" | "37" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R2"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H24_W52_R2_SELECTED | "I" | "I" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"52","report":"R2"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H24_W260_R0_LOSS_PERCENT | "-0.19348933268801272" | "-0.19348933268801272" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"260","report":"R0"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H24_W260_R0_HITS | "17" | "17" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"260","report":"R0"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H24_W260_R0_SELECTED | "10" | "10" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"260","report":"R0"}; field=selected_id |
| PANEL_R6_INSPECTED_BILL_H24_W260_R2_LOSS_PERCENT | "2.3528740518177216" | "2.3528740518177216" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"260","report":"R2"}; field=percent_vs_F |
| PANEL_R6_INSPECTED_BILL_H24_W260_R2_HITS | "15" | "15" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"260","report":"R2"}; field=strict_breach_count |
| PANEL_R6_INSPECTED_BILL_H24_W260_R2_SELECTED | "I" | "I" | results/supervisor-20261023/r6/summary.csv where={"phase":"inspected","source":"nyfed_weekly","series_key":"PDPOSGS-B","horizon":"24","window":"260","report":"R2"}; field=selected_id |
| PANEL_LEVY_BILL_H6_W52_LOSS | 2872.719494584838 | 2872.719494584838 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w52.json /evaluation/mean_pinball |
| PANEL_LEVY_BILL_H6_W52_HITS | 10 | 10 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w52.json /evaluation/strict_breach_count |
| PANEL_LEVY_BILL_H6_W52_N | 277 | 277 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w52.json /evaluation/origin_count |
| PANEL_LEVY_BILL_H6_W52_VS_F | 3.370423806717569 | 3.370423806717569 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w52.json /comparisons/0/relative_loss_percent |
| PANEL_LEVY_BILL_H6_W52_VS_QR | -43.62263637796023 | -43.62263637796023 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w52.json /comparisons/1/relative_loss_percent |
| PANEL_LEVY_BILL_H6_W260_LOSS | 2433.895306859206 | 2433.895306859206 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w260.json /evaluation/mean_pinball |
| PANEL_LEVY_BILL_H6_W260_HITS | 15 | 15 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w260.json /evaluation/strict_breach_count |
| PANEL_LEVY_BILL_H6_W260_N | 277 | 277 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w260.json /evaluation/origin_count |
| PANEL_LEVY_BILL_H6_W260_VS_F | -11.772723245675618 | -11.772723245675618 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w260.json /comparisons/0/relative_loss_percent |
| PANEL_LEVY_BILL_H6_W260_VS_QR | -41.48830465961125 | -41.48830465961125 | results/revision-20261023/round2/levy/nyfed_weekly-h6-w260.json /comparisons/1/relative_loss_percent |
| PANEL_LEVY_BILL_H24_W52_LOSS | 4693.837184115523 | 4693.837184115523 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w52.json /evaluation/mean_pinball |
| PANEL_LEVY_BILL_H24_W52_HITS | 42 | 42 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w52.json /evaluation/strict_breach_count |
| PANEL_LEVY_BILL_H24_W52_N | 277 | 277 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w52.json /evaluation/origin_count |
| PANEL_LEVY_BILL_H24_W52_VS_F | 26.324672308979274 | 26.324672308979274 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w52.json /comparisons/0/relative_loss_percent |
| PANEL_LEVY_BILL_H24_W52_VS_QR | -61.41705155775976 | -61.41705155775976 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w52.json /comparisons/1/relative_loss_percent |
| PANEL_LEVY_BILL_H24_W260_LOSS | 2725.0732851985563 | 2725.0732851985563 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w260.json /evaluation/mean_pinball |
| PANEL_LEVY_BILL_H24_W260_HITS | 22 | 22 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w260.json /evaluation/strict_breach_count |
| PANEL_LEVY_BILL_H24_W260_N | 277 | 277 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w260.json /evaluation/origin_count |
| PANEL_LEVY_BILL_H24_W260_VS_F | 9.868416887194494 | 9.868416887194494 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w260.json /comparisons/0/relative_loss_percent |
| PANEL_LEVY_BILL_H24_W260_VS_QR | -47.6426679089436 | -47.6426679089436 | results/revision-20261023/round2/levy/nyfed_weekly-h24-w260.json /comparisons/1/relative_loss_percent |
| PANEL_LEVY_PRIMARY_VS_FROZEN_F_DM_P | "0.1784812492533747" | "0.1784812492533747" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-frozen_F"}; field=dm_p |
| PANEL_LEVY_PRIMARY_VS_FROZEN_F_HLN_P | "0.18835285356083853" | "0.18835285356083853" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-frozen_F"}; field=hln_p |
| PANEL_LEVY_PRIMARY_VS_FROZEN_F_HOLM_P | "0.7002176763451322" | "0.7002176763451322" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-frozen_F"}; field=holm_p |
| PANEL_LEVY_PRIMARY_VS_FROZEN_F_FAMILY_N | "16" | "16" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-frozen_F"}; field=separate_family_size |
| PANEL_LEVY_PRIMARY_VS_QR_DM_P | "0.0024408620726638656" | "0.0024408620726638656" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-QR"}; field=dm_p |
| PANEL_LEVY_PRIMARY_VS_QR_HLN_P | "0.0032358101353604264" | "0.0032358101353604264" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-QR"}; field=hln_p |
| PANEL_LEVY_PRIMARY_VS_QR_HOLM_P | "0.029290344871966387" | "0.029290344871966387" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-QR"}; field=holm_p |
| PANEL_LEVY_PRIMARY_VS_QR_FAMILY_N | "16" | "16" | results/revision-20261023/round2/levy/paired-tests.csv where={"contrast_id":"nyfed_weekly-h6-w260-Levy_L-minus-QR"}; field=separate_family_size |
| PANEL_WP3_MEAN_TOTAL | 56 | 56 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/total |
| PANEL_WP3_MEAN_COMPLETE | 56 | 56 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/complete |
| PANEL_WP3_MEAN_NA | 0 | 0 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/na |
| PANEL_WP3_MEAN_LOWER_THAN_BOTH | 14 | 14 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/lower_than_both |
| PANEL_WP3_MEAN_LOWER_THAN_F | 16 | 16 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/lower_than_F |
| PANEL_WP3_MEAN_LOWER_THAN_QR | 54 | 54 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/lower_than_QR |
| PANEL_WP3_MEAN_EXACTLY_F | 0 | 0 | results/revision-20261023/v6/wp3-findings.json /counts/MEAN_F_QR/exactly_F |
| PANEL_WP3_MEDIAN_TOTAL | 56 | 56 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/total |
| PANEL_WP3_MEDIAN_COMPLETE | 8 | 8 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/complete |
| PANEL_WP3_MEDIAN_NA | 48 | 48 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/na |
| PANEL_WP3_MEDIAN_LOWER_THAN_BOTH | 3 | 3 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/lower_than_both |
| PANEL_WP3_MEDIAN_LOWER_THAN_F | 5 | 5 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/lower_than_F |
| PANEL_WP3_MEDIAN_LOWER_THAN_QR | 6 | 6 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/lower_than_QR |
| PANEL_WP3_MEDIAN_EXACTLY_F | 2 | 2 | results/revision-20261023/v6/wp3-findings.json /counts/MEDIAN_F_QR_KNN/exactly_F |
| PANEL_WP3_BILL_PRIMARY_MEAN_VS_F | 2.7730553886759823 | 2.7730553886759823 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/2/percent_vs_F |
| PANEL_WP3_BILL_PRIMARY_MEAN_VS_QR | -31.84164889450287 | -31.84164889450287 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/2/percent_vs_QR |
| PANEL_WP3_BILL_PRIMARY_MEAN_LOSS | 2835.1646609087857 | 2835.1646609087857 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/2/scores/mean_loss |
| PANEL_WP3_BILL_PRIMARY_MEAN_HITS | 40 | 40 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/2/scores/full_hits |
| PANEL_WP3_BILL_PRIMARY_MEAN_N | 277 | 277 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/2/scores/n |
| PANEL_WP3_BILL_PRIMARY_MEDIAN_VS_F | -3.9812983393045176 | -3.9812983393045176 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/3/percent_vs_F |
| PANEL_WP3_BILL_PRIMARY_MEDIAN_VS_QR | -36.32108770403683 | -36.32108770403683 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/3/percent_vs_QR |
| PANEL_WP3_BILL_PRIMARY_MEDIAN_LOSS | 2648.8346454740417 | 2648.8346454740417 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/3/scores/mean_loss |
| PANEL_WP3_BILL_PRIMARY_MEDIAN_HITS | 28 | 28 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/3/scores/full_hits |
| PANEL_WP3_BILL_PRIMARY_MEDIAN_N | 277 | 277 | results/revision-20261023/v6/wp3-findings.json /primary_context_rows/3/scores/n |
| PANEL_WP3_BILL_MURPHY_4 | "CROSSING" | "CROSSING" | results/revision-20261023/v6/wp3-findings.json /murphy_rankings/4/ranking |
| PANEL_WP3_BILL_MURPHY_5 | "CROSSING" | "CROSSING" | results/revision-20261023/v6/wp3-findings.json /murphy_rankings/5/ranking |
| PANEL_WP3_BILL_MURPHY_6 | "CROSSING" | "CROSSING" | results/revision-20261023/v6/wp3-findings.json /murphy_rankings/6/ranking |
| PANEL_WP3_BILL_MURPHY_7 | "CROSSING" | "CROSSING" | results/revision-20261023/v6/wp3-findings.json /murphy_rankings/7/ranking |
| PANEL_SAV_ORIGINAL_EIGHT_COMPLETE | 8 | 8 | results/revision-20261023/v6/wp2-findings.json /method_inventory/SAV/complete |
| PANEL_SAV_ORIGINAL_EIGHT_NA | 0 | 0 | results/revision-20261023/v6/wp2-findings.json /method_inventory/SAV/na |
| PANEL_SAV_BILL_H6_W52_LOSS | 2974.3236023506083 | 2974.3236023506083 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w52-SAV.json /scores/mean_loss |
| PANEL_SAV_BILL_H6_W52_HITS | 16 | 16 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w52-SAV.json /scores/full_hits |
| PANEL_SAV_BILL_H6_W52_N | 277 | 277 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w52-SAV.json /scores/n |
| PANEL_SAV_BILL_H6_W52_RATE | 0.05776173285198556 | 0.05776173285198556 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w52-SAV.json /scores/full_rate |
| PANEL_SAV_BILL_H6_W260_LOSS | 2892.2308802158063 | 2892.2308802158063 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w260-SAV.json /scores/mean_loss |
| PANEL_SAV_BILL_H6_W260_HITS | 29 | 29 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w260-SAV.json /scores/full_hits |
| PANEL_SAV_BILL_H6_W260_N | 277 | 277 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w260-SAV.json /scores/n |
| PANEL_SAV_BILL_H6_W260_RATE | 0.10469314079422383 | 0.10469314079422383 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h6-w260-SAV.json /scores/full_rate |
| PANEL_SAV_BILL_H24_W52_LOSS | 4182.397565906022 | 4182.397565906022 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w52-SAV.json /scores/mean_loss |
| PANEL_SAV_BILL_H24_W52_HITS | 35 | 35 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w52-SAV.json /scores/full_hits |
| PANEL_SAV_BILL_H24_W52_N | 277 | 277 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w52-SAV.json /scores/n |
| PANEL_SAV_BILL_H24_W52_RATE | 0.1263537906137184 | 0.1263537906137184 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w52-SAV.json /scores/full_rate |
| PANEL_SAV_BILL_H24_W260_LOSS | 3100.9667732237945 | 3100.9667732237945 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w260-SAV.json /scores/mean_loss |
| PANEL_SAV_BILL_H24_W260_HITS | 25 | 25 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w260-SAV.json /scores/full_hits |
| PANEL_SAV_BILL_H24_W260_N | 277 | 277 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w260-SAV.json /scores/n |
| PANEL_SAV_BILL_H24_W260_RATE | 0.09025270758122744 | 0.09025270758122744 | results/revision-20261023/v6/wp2/evaluation-nyfed_weekly-h24-w260-SAV.json /scores/full_rate |
| PANEL_SAV_BILL_H6_W52_VS_FROZEN_F_MEAN_DIFFERENCE | 195.26999224230465 | 195.26999224230465 | results/revision-20261023/v6/wp2-comparisons.json /rows/28/mean_difference |
| PANEL_SAV_BILL_H6_W52_VS_FROZEN_F_DM_P | 0.253500249800881 | 0.253500249800881 | results/revision-20261023/v6/wp2-comparisons.json /rows/28/raw_p |
| PANEL_SAV_BILL_H6_W52_VS_FROZEN_F_HLN_P | 0.2640219354967316 | 0.2640219354967316 | results/revision-20261023/v6/wp2-comparisons.json /rows/28/hln_p |
| PANEL_SAV_BILL_H6_W52_VS_FROZEN_F_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp2-comparisons.json /rows/28/holm_p |
| PANEL_SAV_BILL_H6_W52_VS_QR_MEAN_DIFFERENCE | -2121.195787033887 | -2121.195787033887 | results/revision-20261023/v6/wp2-comparisons.json /rows/29/mean_difference |
| PANEL_SAV_BILL_H6_W52_VS_QR_DM_P | 0.001574870019929032 | 0.001574870019929032 | results/revision-20261023/v6/wp2-comparisons.json /rows/29/raw_p |
| PANEL_SAV_BILL_H6_W52_VS_QR_HLN_P | 0.0021509407042462564 | 0.0021509407042462564 | results/revision-20261023/v6/wp2-comparisons.json /rows/29/hln_p |
| PANEL_SAV_BILL_H6_W52_VS_QR_HOLM_P | 0.07716863097652257 | 0.07716863097652257 | results/revision-20261023/v6/wp2-comparisons.json /rows/29/holm_p |
| PANEL_SAV_BILL_H6_W260_VS_FROZEN_F_MEAN_DIFFERENCE | 133.56553725551774 | 133.56553725551774 | results/revision-20261023/v6/wp2-comparisons.json /rows/34/mean_difference |
| PANEL_SAV_BILL_H6_W260_VS_FROZEN_F_DM_P | 0.16270607236696893 | 0.16270607236696893 | results/revision-20261023/v6/wp2-comparisons.json /rows/34/raw_p |
| PANEL_SAV_BILL_H6_W260_VS_FROZEN_F_HLN_P | 0.17232892868800043 | 0.17232892868800043 | results/revision-20261023/v6/wp2-comparisons.json /rows/34/hln_p |
| PANEL_SAV_BILL_H6_W260_VS_FROZEN_F_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp2-comparisons.json /rows/34/holm_p |
| PANEL_SAV_BILL_H6_W260_VS_QR_MEAN_DIFFERENCE | -1267.4423145192739 | -1267.4423145192739 | results/revision-20261023/v6/wp2-comparisons.json /rows/35/mean_difference |
| PANEL_SAV_BILL_H6_W260_VS_QR_DM_P | 0.017469717616953692 | 0.017469717616953692 | results/revision-20261023/v6/wp2-comparisons.json /rows/35/raw_p |
| PANEL_SAV_BILL_H6_W260_VS_QR_HLN_P | 0.020555504742543213 | 0.020555504742543213 | results/revision-20261023/v6/wp2-comparisons.json /rows/35/hln_p |
| PANEL_SAV_BILL_H6_W260_VS_QR_HOLM_P | 0.7511978575290088 | 0.7511978575290088 | results/revision-20261023/v6/wp2-comparisons.json /rows/35/holm_p |
| PANEL_SAV_BILL_H24_W52_VS_FROZEN_F_MEAN_DIFFERENCE | 466.7044251117983 | 466.7044251117983 | results/revision-20261023/v6/wp2-comparisons.json /rows/40/mean_difference |
| PANEL_SAV_BILL_H24_W52_VS_FROZEN_F_DM_P | 0.05354541146725355 | 0.05354541146725355 | results/revision-20261023/v6/wp2-comparisons.json /rows/40/raw_p |
| PANEL_SAV_BILL_H24_W52_VS_FROZEN_F_HLN_P | 0.07838137994156787 | 0.07838137994156787 | results/revision-20261023/v6/wp2-comparisons.json /rows/40/hln_p |
| PANEL_SAV_BILL_H24_W52_VS_FROZEN_F_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp2-comparisons.json /rows/40/holm_p |
| PANEL_SAV_BILL_H24_W52_VS_QR_MEAN_DIFFERENCE | -7983.176537748418 | -7983.176537748418 | results/revision-20261023/v6/wp2-comparisons.json /rows/41/mean_difference |
| PANEL_SAV_BILL_H24_W52_VS_QR_DM_P | 0.02651328231171469 | 0.02651328231171469 | results/revision-20261023/v6/wp2-comparisons.json /rows/41/raw_p |
| PANEL_SAV_BILL_H24_W52_VS_QR_HLN_P | 0.043276216488319655 | 0.043276216488319655 | results/revision-20261023/v6/wp2-comparisons.json /rows/41/hln_p |
| PANEL_SAV_BILL_H24_W52_VS_QR_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp2-comparisons.json /rows/41/holm_p |
| PANEL_SAV_BILL_H24_W260_VS_FROZEN_F_MEAN_DIFFERENCE | 620.6604555342641 | 620.6604555342641 | results/revision-20261023/v6/wp2-comparisons.json /rows/46/mean_difference |
| PANEL_SAV_BILL_H24_W260_VS_FROZEN_F_DM_P | 0.22812068503816374 | 0.22812068503816374 | results/revision-20261023/v6/wp2-comparisons.json /rows/46/raw_p |
| PANEL_SAV_BILL_H24_W260_VS_FROZEN_F_HLN_P | 0.27100336666668523 | 0.27100336666668523 | results/revision-20261023/v6/wp2-comparisons.json /rows/46/hln_p |
| PANEL_SAV_BILL_H24_W260_VS_FROZEN_F_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp2-comparisons.json /rows/46/holm_p |
| PANEL_SAV_BILL_H24_W260_VS_QR_MEAN_DIFFERENCE | -2103.7928590265465 | -2103.7928590265465 | results/revision-20261023/v6/wp2-comparisons.json /rows/47/mean_difference |
| PANEL_SAV_BILL_H24_W260_VS_QR_DM_P | 0.20360005842334972 | 0.20360005842334972 | results/revision-20261023/v6/wp2-comparisons.json /rows/47/raw_p |
| PANEL_SAV_BILL_H24_W260_VS_QR_HLN_P | 0.2456315404631253 | 0.2456315404631253 | results/revision-20261023/v6/wp2-comparisons.json /rows/47/hln_p |
| PANEL_SAV_BILL_H24_W260_VS_QR_HOLM_P | 1.0 | 1.0 | results/revision-20261023/v6/wp2-comparisons.json /rows/47/holm_p |
| PANEL_SCOPE_BILL_PLUS_TWELVE | "The original bill plus 12 archived panel series share the 706-date grid; no new data were downloaded." | "The original bill plus 12 archived panel series share the 706-date grid; no new data were downloaded." | results/supervisor-20261023/r6/README.md where={}; field= |
| PANEL_SCOPE_NOT_INDEPENDENT_DEALERS | "The series share a dealer reporting system and overlapping economic positions; they are not independent dealer replications." | "The series share a dealer reporting system and overlapping economic positions; they are not independent dealer replications." | results/supervisor-20261023/e5/README.md where={}; field= |
| PANEL_SCOPE_WP3_LIMITS | "Untuned combinations, no conditional quantile or coverage guarantee; normal-DM Holm family224, HLN unadjusted, overlapping/dependent inspected records." | "Untuned combinations, no conditional quantile or coverage guarantee; normal-DM Holm family224, HLN unadjusted, overlapping/dependent inspected records." | results/revision-20261023/v6/wp3-combinations.json where={}; field= |
| COVERAGE_BILL_QR_N | "40" | "40" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=n |
| COVERAGE_BILL_QR_HITS | "7" | "7" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=hits |
| COVERAGE_BILL_QR_RATE | "0.175" | "0.175" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=rate |
| COVERAGE_BILL_QR_POF_P | "0.004126046248434382" | "0.004126046248434382" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=pof_p |
| COVERAGE_BILL_QR_CC_P | "0.013592800225591856" | "0.013592800225591856" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=cc_p |
| COVERAGE_BILL_QR_CC_INITIALIZATION | "condition_on_first_hit_n_minus_1" | "condition_on_first_hit_n_minus_1" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"QR"}; field=cc_initialization |
| COVERAGE_BILL_FROZEN_F_N | "40" | "40" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=n |
| COVERAGE_BILL_FROZEN_F_HITS | "4" | "4" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=hits |
| COVERAGE_BILL_FROZEN_F_RATE | "0.1" | "0.1" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=rate |
| COVERAGE_BILL_FROZEN_F_POF_P | "0.1986410814587244" | "0.1986410814587244" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=pof_p |
| COVERAGE_BILL_FROZEN_F_CC_P | "0.26189986860444203" | "0.26189986860444203" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=cc_p |
| COVERAGE_BILL_FROZEN_F_CC_INITIALIZATION | "condition_on_first_hit_n_minus_1" | "condition_on_first_hit_n_minus_1" | results/supervisor-20261023/inference/coverage-verified.csv where={"source":"nyfed_weekly","horizon":"6","window":"260","method":"frozen_F"}; field=cc_initialization |
| EXAMPLE_ORIGIN | 408 | 408 | results/revision-20261023/v5-novelty/motivating-window-final.json /example/origin |
| EXAMPLE_HORIZON | 6 | 6 | results/revision-20261023/v5-novelty/motivating-window-final.json /example/horizon |
| EXAMPLE_REPORT | 73139.0 | 73139.0 | results/revision-20261023/v5-novelty/motivating-window-final.json /example/report |
| EXAMPLE_FLOOR | 42513.0 | 42513.0 | results/revision-20261023/v5-novelty/motivating-window-final.json /example/floor |
| EXAMPLE_PEAK | 74397.0 | 74397.0 | results/revision-20261023/v5-novelty/motivating-window-final.json /example/peak |
| EXAMPLE_ENDPOINT_ABSOLUTE | 48144.0 | 48144.0 | results/revision-20261023/v5-novelty/motivating-window-final.json /example/endpoint_absolute |
| EXAMPLE_DATES | ["2021-01-27T00:00:00.000000", "2021-02-03T00:00:00.000000", "2021-02-10T00:00:00.000000", "2021-02-17T00:00:00.000000", "2021-02-24T00:00:00.000000", "2021-03-03T00:00:00.000000", "2021-03-10T00:00:00.000000"] | ["2021-01-27T00:00:00.000000", "2021-02-03T00:00:00.000000", "2021-02-10T00:00:00.000000", "2021-02-17T00:00:00.000000", "2021-02-24T00:00:00.000000", "2021-03-03T00:00:00.000000", "2021-03-10T00:00:00.000000"] | results/revision-20261023/v5-novelty/motivating-window-final.json /example/dates |

## 验证范围与重做方式

核对程序只用 Python 标准库：按相对路径枚举两个根目录 results/ 与 data/，分别取文件字节数及 SHA-256；打开共同 numerical registry 每条 CSV where/field 或 JSON pointer，比较原生类型和值及 registry 既存值；打开完整 2,125 条 supplement binding 逐条相同验证；按明示条件点数 R2 的 26 行选择。所有预存文件都只读。完整文件清单、每条原值、实际文档表格行和源哈希保存在 `notes/v9/real-number-reconciliation.json`。本核对不代表重新执行或独立复现实证模型。
