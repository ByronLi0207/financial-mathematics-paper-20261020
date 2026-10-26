# v10 E1 六菜单接口与旧 v9 路径证据核对

本备忘录只记录对公开 v9 源码、已保存参数和存档结构的只读核对。它不是 E1 preregistration、实施文件或 run-plan，不授权也不记录任何新真实序列统计、校准、拟合、bootstrap、模拟、预测或评估。E1 design 必须先独立提交，随后才能启动新数值工作。Claude／Cloud 与跨模型复审保持关闭。

核对基线为公开 `revision-v9` 提交 `0d2526cc69092c5158437a0509613bac5e86d47f`。旧目录 `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024` 仅用于只读源和存档结构检查；本备忘录仅写入新目录 `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024`。

## 1. 最小适配接口与继承边界

旧 `v8_mechanism_mc.select_candidate`（70–92 行）硬编码两种不同的失败和平局合同：

| 项目 | v9 QR33 | v9 QR4 | v10 E1 目标 |
|---|---|---|---|
| 菜单 | `.001, .01, .1` | `.001, .01, .1, 1, 10` | 两者均 `.001, .01, .1, 1, 10, inf` |
| 候选失败 | 全部必需候选完整才可选择 | 从完整候选中选择；失败候选保留 | 原失败政策各自保留 |
| 完全相同 validation loss 的 tie | 更大 lambda | 更小 lambda | 两者均更大 lambda，`inf` 最强 |

“其余选择规则不变”包括：QR33 的 required-all 和 QR4 的 successful-subset 不得被合并为相同失败政策。旧 `protocol/v9/nonstationarity-design.md` 第 7 节也明确保存了这一差别。

旧 `v8_mechanism_mc.forecast_report`（95–172 行）支持 F、QR33、QR4；108–111 行要求 conditional penalty 为有限正数。因此不能把 IEEE infinity 直接交给该函数或 quantile solver。公开 JSON 写入使用 `allow_nan=False`；菜单中的 infinity 需要一个明确的可序列化标识，例如字符串 `"inf"`，与数值无穷分开。

最小适配边界应使有限 lambda 原样进入旧 forecast 函数；infinity 对应现有 `empirical_headroom.predict` 的 `I` 输出。有限部分的特征变换、训练池、refit 频率、响应尺度、求解器初始化、容差、最大迭代数以及 issue floor 均沿用旧接口，不因六菜单改动而改变。旧 v9／WP3 模块应保持原字节。

旧 `run_v8_wp3.evaluate_method`（376–443 行）具有需要继承的行为：每个菜单候选至多尝试一次，候选成功或失败均独立留档；先写 selection receipt，再运行一次 selected evaluation；selected evaluation 失败后不选择另一 lambda；资源中断先保存失败候选和 method 状态，再向外传播。该函数在内部导入旧 selector，故只修改调用处的菜单并不足以替换 QR4 的 tie 规则。

## 2. infinity 等于 I 的已有接口

`empirical_headroom.py` 的普通经验分位数 `I` 使用精确一基 rank `ceil(19*W/20)`，corrected `F` 使用 `ceil(19*(W+1)/20)`：

| W | I rank | F rank |
|---|---:|---:|
| 52 | 50 | 51 |
| 260 | 247 | 248 |

`predict(positions, origins, horizon, window, refit_step)` 直接返回 `I`、`F`、`origins`、`floors`、`refit_indices`、`training_first_origins`、`training_last_origins` 和 `latest_label_ends`。每次 refit 的历史 origin 为 `r-H-W+1 .. r-H`，只使用在 r 已完成的标签；在 block 内冻结经验分位数，但 current issue 的 `abs(position)` floor 继续更新。重复 headroom 保留，取 lower ordinary empirical minimizer，不插值。

这些 maturity 数组足够组成原 forecast receipt 的 refit diagnostics，不需要拟合 infinity 模型。I 分支须使用 E1 的 H6、W52／260 和 refit24。已有 `supervisor_r6.CoreReports.segment`（171–240 行）展示了 I／F 共同经验入口、历史成熟度核对、失败缓存和诊断转录；`supervisor_r6_rules.CANDIDATE_IDS` 为 `('0.001','0.01','0.1','1','10','I')`。R6 的 exact-tie 强惩罚优先可参考，但 R6 的所有候选必需政策不能替换 QR4 原政策。E5 具有五个有限候选和单独 I 评估，不能称为已实现 infinity 菜单候选。

## 3. 精确 calibration、种子与原几何

v9 C2 preregistration 的独立提交为 `5decccb0a13ef1969629cfec695dd3459c412c4e`。原 timing-only run-plan 独立提交为 `3411a1fee705ef83b070cfd12e110c5d3d9f357f`，选择正式 R32，F、QR33 与 QR4。

已保存 calibration 的来源是 `results/v9/nonstationarity/diagnostics.json` 和 `results/v9/nonstationarity/diagnostics/units.zip` 中每个 `sXX/result.json`，不是重新读取真实序列后再次拟合。13 条 weekly 的 M 均为 404，whole／segment calibration 均为 COMPLETE。源顺序必须保留：

| source_index | source_id | 已保存 selected k |
|---:|---|---:|
| 0 | PDPOSGS-B | 2 |
| 1 | PDPOSMBS-TOT | 2 |
| 2 | PDPOSCS-TOT | 0 |
| 3 | PDPOSFGS-TOT | 1 |
| 4 | PDPOSTIPS-L2 | 1 |
| 5 | PDPOSTIPS-G11 | 0 |
| 6 | PDPOSTIPS-G2 | 0 |
| 7 | PDPOSTIPS-G6L11 | 1 |
| 8 | PDPOSGSC-L2 | 1 |
| 9 | PDPOSGSC-G2L3 | 2 |
| 10 | PDPOSGSC-G3L6 | 2 |
| 11 | PDPOSGSC-G6L7 | 0 |
| 12 | PDPOSGSC-G7L11 | 1 |

每日 FX 已保存为 NONREGULAR_NULL，小时 FX 为 GARCH_OPTIMIZATION_FAILED；二者都不是 E1 的 synthetic forecast source，不需要重拟合。

随机性原合同由 `v9_switching.generate_pair`（148–232 行）和原 design 固定：

- `master_entropy=2026102408`，PCG64，`SeedSequence` namespace 9。
- diagnostic spawn key 为 `(9,0,source_index)`；pilot 为 `(9,1,source_index,rep)`；formal 为 `(9,2,source_index,rep)`。
- open uniforms 为 `integers(1,2**53,dtype=int64) / 2**53`，再用相应 Student-t inverse CDF 与方差标准化。
- burn 20000，retained 3264，初始 level 0、variance 1；切换保留前一 level、variance、innovation。
- phase 为 `floor(rep*M/R)`；完整 burn 与 retained schedule 使用 `(phase+i-burn_in) mod M`。
- validation origins 为 `3072..3143`，evaluation 为 `3168..3239`，均 72 点；H6、W52／260、refit24、RMS24／168、feature valid168、nominal gap3600。
- 人工小时钟从 `2000-01-03T00:00:00` 开始；同 source／rep 的 W、method、arm 共用原生成路径。k0 来源两臂应精确相同。

## 4. pilot 与 formal 的 samepath 对应

两个阶段分别与各自旧 v9 阶段配对，不能把 pilot 改用 formal 路径：

| 阶段 | seed tag | phase 分母 | 对应旧存档 |
|---|---:|---:|---|
| pilot | 1 | 2 | 原 v9 pilot 的 rep0、rep1 |
| formal R32 | 2 | 32 | 原 v9 formal 的 rep0..31 |
| formal fallback R16 | 2 | 32 | 原 v9 formal 的 rep0..15 |

`v9_switching.py:180` 直接计算 `phase=rep*sum(lengths)//repetitions`。因此 R16 fallback 不能把 16 当作生成器的 phase 分母；否则 switching 从 rep1 起 phase 改变，只有 uniform seed 相同，路径已经不同。R16 只减少预先声明的 formal rep 库存，不改变这 16 条旧 formal 路径。原 v9 的 R16／QR33-only 第三级 timing ladder 不适用于用户本次要求的两方法完整格合同。

## 5. 已有 samepath 证据与边界

旧 ZIP 的每个 source／rep 保存 `geometry.json` 与 `geometry-{arm}.json`，包括 `phase`、`uniform_sha256`、`rng_initial`、`rng_final`、regime IDs、forward transition、last-to-first wrap 和 exposure。旧存档没有保存 position／variance／innovations 原始向量或这些 path 的 SHA。

每个 arm／W 的 F method receipt 及 `W52-F-evaluation-points.json`、`W260-F-evaluation-points.json` 存在；points JSON 保存完整 72 个 `losses`、`breaches` 和 `capacities`。所有这些成员均由 `units-manifest.json` 逐文件封存 SHA。原 formal ZIP 有 39518 成员，pilot ZIP 有 2470 成员。

可复核的旧路径证据组合是：原 calibration 指纹、原 generator 源指纹、相同 uniform／RNG／phase／geometry，加上 F scalar report 和 72 点逐值完全相等。新 v10 可以另存 path SHA 作为今后基线，但不能宣称已经与不存在的旧 path SHA 比较。

本次只读实际计算了文件指纹，并核对 pilot／formal ZIP SHA 与原 manifest 的 `archive_sha256` 一致：

| 文件（相对 `results/v9/nonstationarity/`） | bytes（如本次记录） | SHA-256 |
|---|---:|---|
| `diagnostics.json` | 455113 | `9d3be1de5cffdb82b0209cff98a6b360a5036bffedff2ab5363f31a283d0f621` |
| `manifest.json` | 7488 | `23677c45d23acccf0bf110adebd3a8c60c489ece5998484c7d8028e810fbc2d7` |
| `diagnostics/units.zip` | 163750 | `4d9f1c474fc71eda1a3f91ec434e1eec2f0ae9b03fadd296011bae8729925810` |
| `diagnostics/units-manifest.json` | 2403 | `4654f2d81b72acbed0566cd2ff62727cde709c8ba77148fd152b4a6b9aef7ba3` |
| `pilot/units.zip` | — | `156b31cf3cc9ffebabc442618e6f17894bd12fd780df64d9d9d34fbc3e6e9c01` |
| `pilot/units-manifest.json` | 438344 | `ff9c4948fe535815b469c029559d5c59098a90da431585cc32e8bfe1e3fb8d92` |
| `formal/units.zip` | — | `7ecc25fe719c5624e8e9774b38eb3a54aa6ed14d6d8756d3cbefbbffe214c1b8` |
| `formal/units-manifest.json` | 7011022 | `16d929a0cebbfade7aee54f64b44c64ee8e4a11a48ffde46e891cdbba9483589` |
| `run-plan.json` | 2287 | `93746ce60ba0fe37e2236acc7cd7ae85a06b10562feaccbf4925de956998b643` |

原 manifest 封存的 `v9_switching.py` SHA 为 `70309cfe6a055af8503fcb81e07d8a0240d115211f185740a68a1eec3d196731`；`v8_mechanism_mc.py` 为 `71134570e1b4d63f98dcd2bb4eb7c1bc596a516b3ca8243b77ad913670a7d7c4`；`run_v8_wp3.py` 为 `1b5489fc9875137fc1217f2bfe412046f1a353287d234a201f9ac29da3e7352f`。

## 6. 已保存失败与扩大菜单的限制

这是旧回执事实，不能提前写作新 v10 结果。旧 formal 中 `s05-r024/{constant,switching}/W260_H6_QR33.json` 均为 VALIDATION_INELIGIBLE，原菜单 `.001` candidate 的原因均为 NONCONVERGENCE；`.01` 与 `.1` 完整。s05 为 PDPOSTIPS-G11，k0，两臂相同。

若正式 R32 严格保留旧路径、旧有限候选算术与求解器，原 `.001` 必需候选的失败具有可重现风险；增加 1、10、infinity 不能按原 QR33 required-all 合同救格。实际 v10 仍须如实记录尝试，不能把该风险当作已经产生的新结果。若 timing-only 规则预先降至 rep0..15，则 rep24 不在本次 planned inventory，不能事后用此事实选择缩减。

旧审计 `results/v9/nonstationarity/audit/summary.json` 保存 9 个 failed candidates，均 `.001`／NONCONVERGENCE：

| source index / rep | arm | W | method |
|---|---|---:|---|
| s01 / r003 | switching | 52 | QR4 |
| s00 / r005 | constant | 52 | QR4 |
| s03 / r006 | constant | 260 | QR4 |
| s05 / r024 | constant | 260 | QR33 |
| s05 / r024 | constant | 260 | QR4 |
| s05 / r024 | switching | 260 | QR33 |
| s05 / r024 | switching | 260 | QR4 |
| s01 / r025 | constant | 52 | QR4 |
| s10 / r030 | switching | 260 | QR4 |

原审计保存 104 个条件格中的 102 COMPLETE、2 FAILED；52 个 F 格全部 COMPLETE；4992 个 method receipts 中 4990 COMPLETE、2 FAILED。这些是读取旧存档的历史事实。新增候选可能出现新的失败；所有 planned 格、失败、未到达候选与中断必须留存，不允许重试或成功前缀中位数。

## 7. 必要的行为验证清单

以下是后续开发应覆盖的行为，不表示本次已经运行测试：

1. 两方法严格六候选库存及 `"inf"` JSON round-trip；完全同损失时选择 `"inf"`，有限候选平局时选择更大 lambda。
2. QR33 任一必需候选失败即 ineligible；QR4 可从其余成功候选中选择；两者均保留所有 candidate receipts。
3. infinity 每个 capacity、refit 和训练边界均等于现有 I；不调用 quantile solver；W52／260 的 I／F ranks 可由独立普通次序统计量核对。
4. 有限分支与旧 `forecast_report` 的容量和诊断逐值相等；特征、尺度、初始化、容差和接受标准没有侧面变化。
5. selection receipt 先于 evaluation；selected evaluation 失败后不尝试第二候选；资源中断保留已完成候选及未触及候选状态。
6. pilot tag1／phase2 仅对照旧 pilot；formal tag2／phase32 对照旧 formal；R16 保留 rep0..15 的 R32 phase；k0 两臂完全相同。
7. 原 calibration／generator／uniform／RNG／geometry 和 F 72 点核对；旧 path SHA 缺失的证据边界保持明确。
8. 未独立提交、stale 或被修改的 E1 design／正式 run-plan 在任何新数值计算前拒绝；已有输出目录拒绝覆盖和重跑。
9. reducer 保留失败、重复、缺失 rep 的完整格语义，不输出 successful-prefix median；所有 planned 来源／arm／W／method 格留存。
10. 报告层将 NumPy scalar 转为同值原生标量，避免重演 v9 已保存的 `predictions.json` 序列化故障；不得为报告层错误重跑 numerical work。

可参考已有测试 `test_v9_nonstationarity_driver.py`、`test_v9_switching.py`、`test_v8_wp3_driver.py`、`test_empirical_headroom.py`。本次没有执行测试或任何新数值 run。
