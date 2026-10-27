# H0：CFTC 历史长度 WP2 只读来源审计

结论：**可导入已封存结果，但必须显式补齐依赖闭包。** 共同核心数字无漂移；原始数据已在 v13。不能声称全部 148 个运行依赖已在 v13：141 个原路径逐字节相同，7 个原路径缺失，其中两项是既有阈值分析文件和 HAC 辅助代码。此次只写本审计 JSON/Markdown；未运行模型、评分、摘要驱动器或实验。

固定来源 `6192ec370d131c60d05e9fb103150e0e9db6aa23`；固定 v13 底稿 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`。所有来源文件均从 `git show` 读取，提交时间与祖先链从 `git log` 读取。

## 1. 设计先于正式运行的可检查证据

- 原设计提交 `effa537bd6d9b89855002aa79f95f62f9ff3761c`：作者和提交者 UTC 均为 **2026-10-26 03:32:15**。
- 正式开始 `start.json:/utc`：**2026-10-26T03:32:28.372451+00:00**，晚于设计提交 **13.372451 秒**。该提交中的结果目录不存在。
- 原结果提交 `3396aed2b88e99c66bcb8c602911e65698d0d1ba`：**2026-10-26 03:36:31 UTC**；其直接父提交为上述设计提交。
- 协议 SHA256：`9036b0f599dd8dbef6ae9232a5f0389c5f61cde535e33f37188e1a65de59d9cb`。
- 输入封条 SHA256：`94b03ca0c36767d08c4b12ddac79a8556c1cabb56d26cdfa70141959a72cfbe7`。
- 两个 SHA 均与 `start.json` 的对应回执相同；148/148 封条条目与原设计对象及 final-jof 当前来源的字节/长度完全匹配。
- 公开上传协议提交是 `475788a5f0387164297579005e09582eedee549d`，公开结果上传是 `98d6dc03a2e691156caa6abdd2460bd52b7e8d3c`，发生在运行后。这里只证实本地 Git 预先提交及封存，不能改写为外部公开预注册。

## 2. SHA、回执和数据依赖

- 结果目录共 **739 个文件**，全部与原结果提交逐字节一致。
- `summary.json:/cells` 的 **153 条** evaluation trace SHA256 全部与实际 Git blob 一致。
- `independent-verification.json` 记录 315,512 检查、153 完整 evaluation traces、204 完整 validation reports、1,836 maturity records，0 mismatch；这里只核验其来源与封存状态，没有重跑这些数值检查。
- 全部 **17 个 CFTC source arrays** 在 v13 的原路径均存在，与 `sources.json` 回执及 final-jof 完全相同；旧 W52/260 traces、`formal/units.zip` 和继承求解代码也均相同。
- 下列 7 个封条路径在 v13 不存在：

  - `final_merge_wp2.py`
  - `notes/revision-v9/wp1-breakeven.json`
  - `protocol/final-merge/wp2-cftc-mechanism.md`
  - `run_final_merge_wp2.py`
  - `test_final_merge_wp2.py`
  - `v9_learning_curve.py`
  - `verify_final_merge_wp2.py`

其中 `notes/revision-v9/wp1-breakeven.json` 与 `v9_learning_curve.py` 是非原始数据的继承依赖，另 5 个是 WP2 新代码/协议。原始数据全部已在 v13；完整运行路径闭包尚未全部在 v13。两句话必须同时保留。

## 3. 共同核心数字逐项比较

final-jof 的已保存数字清单含 **1,186 个 legacy 字段/行定位项 + 50 个 v12 字段/操作定位项**。它们涉及的 **47 个源文件全部在 v13 逐字节相同**。此外，evidence-bindings 中共同源项逐一读取 JSON Pointer；共同项无数值/类型/字节不一致。完整逐项记录、源 SHA、v13 SHA、JSON Pointer 或 CSV 行选择器和两侧值均见同名 JSON 的 `shared_core.rows`。A 的阈值 JSON 在 v13 中缺失，列作待导入依赖；新 WP2 本身也不冒充两分支共同结果。

下表各值在 v13 与 final-jof 一致。CSV 数字直接读取保存行；没有重算金融统计。

| 项目 | 两侧保存值 | 文件 | JSON Pointer / CSV 位置 |
|---|---:|---|---|
| FX H6 relative mean loss % | -12.660126412969763 | `results/revision-20261022/paired-comparisons.csv` | `{"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"} / relative_mean_loss_difference_percent` |
| Treasury bill H6 relative mean loss % | 50.78571256749063 | `results/revision-20261022/paired-comparisons.csv` | `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"} / relative_mean_loss_difference_percent` |
| Treasury bill H6 Holm p | 0.31967752305162894 | `results/supervisor-20261023/inference/dm-verified.csv` | `{"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"} / holm_p` |
| E023 | 29 | `results/v10/cftc/summary.json` | `/predictions/T1/simple_better_cells` |
| E026 | 19.334715757564624 | `results/v10/cftc/summary.json` | `/predictions/T2/median_pct_by_window/52` |
| E027 | 10.34828178946443 | `results/v10/cftc/summary.json` | `/predictions/T2/median_pct_by_window/260` |
| E028 | 10.280676300222424 | `results/v10/cftc/summary.json` | `/predictions/T3/W52_median_pct` |
| E029 | 0.2174917571722501 | `results/v10/cftc/summary.json` | `/predictions/T3/W260_median_pct` |
| E031 | 90 | `results/v10/mcs/summary.json` | `/overall/metrics/matched_FI_membership/count_successful` |
| E032 | 197 | `results/v10/mcs/summary.json` | `/overall/conditional_exclusion/excluded_slots` |
| E033 | 683 | `results/v10/mcs/summary.json` | `/overall/conditional_exclusion/successful_complete_slots` |
| E034 | 0.2069371499562489 | `results/v10/menu/summary.json` | `/predictions/M1/constant_median_pct` |
| E035 | -0.22777914491914353 | `results/v10/menu/summary.json` | `/predictions/M2/switching_median_pct` |
| E037 | 13 | `results/v10/menu/summary.json` | `/predictions/M3/joint_improved_sources` |
| E038 | 98 | `results/v10/cost/summary.json` | `/comparisons` |
| E039 | 98 | `results/v10/cost/summary.json` | `/complete` |
| E040 | 189 | `results/v10/cost/summary.json` | `/grid_points` |
| E041 | 29 | `results/v12/decomposition/predictions.json` | `/D1/support_n` |
| E043 | 27 | `results/v12/decomposition/predictions.json` | `/D2/support_n` |
| E045 | -14.917351765503492 | `results/v12/decomposition/predictions.json` | `/D3/horizons/6/signal_gap_pct` |
| E046 | -3.7577697957958254 | `results/v12/decomposition/predictions.json` | `/D3/horizons/24/signal_gap_pct` |
| E051 | UNDETERMINED | `results/v12/tau/predictions.json` | `/Q1/status` |
| E052 | 1 | `results/v12/tau/predictions.json` | `/Q1/unknown_count` |
| E053 | UNDETERMINED | `results/v12/tau/predictions.json` | `/Q2/status` |
| E054 | 2 | `results/v12/tau/predictions.json` | `/Q2/unknown_count` |

## 4. 应保留的 WP2 结论

| Screen | successes / planned | threshold | status |
|---|---:|---:|---|
| P1_QR4 | 15 / 17 | 0.8 | SUPPORT |
| P2_QR4 | 10 / 17 | 0.6 | NOT_SUPPORT |
| P1_QR33 | 29 / 34 | 0.8 | SUPPORT |
| P2_QR33 | NA / 0 | NA | NOT_TESTABLE |
| P3_QR4 | 6 / 17 | 0.7 | NOT_SUPPORT |

主判决 **PARTLY**。10/17 = 58.82352941176471%，不能向上取整变为达到 60%；6/17 不达到 70%。QR33 高区不存在设计单元，保持 `NOT_TESTABLE`。153 cells、102 comparisons 均完整，25 个 counterexample entries，unknowns=0。W52/260 在注册前已经看过；只有 W520 是新预测扩展。

`summary.json:/independent_verification` 的 `PENDING` 是执行阶段保存标记，必须保留；后续 `independent-verification.json:/status=PASS` 与 `acceptance.json:/status=PASS` 是完成核验回执。算法审计由同一执行者完成，不是另一人/模型、另一批数据或第二次有限惩罚求解。

## 5. 最小导入范围

闭包导入共 **747 个文件**：完整 `results/final-merge/wp2-cftc-mechanism/` 的 **739 个文件**，以及以下 **8 个**代码/协议/非数据继承依赖。所有路径、字节和 SHA256 在 JSON 的 `minimum_import.manifest` 中逐项列出。

- `protocol/final-merge/wp2-cftc-mechanism.md`
- `protocol/final-merge/wp2-input-seal.json`
- `final_merge_wp2.py`
- `run_final_merge_wp2.py`
- `verify_final_merge_wp2.py`
- `test_final_merge_wp2.py`
- `notes/revision-v9/wp1-breakeven.json`
- `v9_learning_curve.py`

可选携带上下文：`notes/final-merge/wp2-preregistration-review.md`、`notes/final-merge/wp2-cftc-mechanism-results.md`。无需导入其他 final-jof 文稿、图、发布包装或跨模型审查记录。不要挑出有利 markets/cells 或覆盖 v13 现有结果。

## 6. 准确正文一段建议

A precommitted extension examines whether the short-history pattern transports to the 17 CFTC aggregate dealer-position markets at a six-week horizon. The 52- and 260-week results were already known and are reused unchanged; only the 520-week forecasts were new. Both registered low-history screens pass: QR4 loses to its matched rolling reference in 15 of 17 cells and QR33 in 29 of 34. The high-history QR4 screen fails, because 10 of 17 wins (58.8%) fall below the fixed 60% rule; strict improvement over all three windows holds in only 6 of 17 markets. The primary verdict is therefore partial support. These dependent aggregate-market counts describe transport of a fixed prediction; they do not establish a generally sufficient financial history, a causal estimation-cost mechanism, or dealer-level replication.

## 7. 补充材料摘要建议

The archived protocol was committed at 2026-10-26 03:32:15 UTC (effa537bd6d9b89855002aa79f95f62f9ff3761c), before the recorded execution start at 03:32:28.372451 UTC. All 17 markets, the six-candidate penalty menu, H=6, W in {52,260,520}, chronological validation/evaluation split, transported thresholds, and fixed-denominator decision rules were frozen before the new W=520 run. The archive contains 153 complete market/window/method cells, 102 matched conditional comparisons, and 25 counterexample entries with no unknown cells. QR33 has no registered high-region cell, so its high-region prediction is not testable. Separate scalar verification by the same executor reports zero mismatches across 315,512 checks, using absolute 1e-10 plus relative 1e-12 tolerance; it does not repeat the finite-penalty solver fit. The downloaded economic-date vintage does not reconstruct first-release information, and the already inspected W=52/260 outcomes are not prospective confirmations. The summary retains its execution-stage PENDING marker; the dated independent-verification and acceptance receipts carry the completed verification state.

## 8. 拒绝的表述

- “148 个封存依赖在 v13 原路径全部已经存在。”
- “W52/260 是未见结果的前瞻确认。”
- “10/17 达到 60%”或“窗口增长普遍单调改善”。
- “另一模型/作者独立复现了模型拟合”或“独立 dealer-level replication”。
- “证实一般充分历史阈值、因果估计成本机制或覆盖保证”。
