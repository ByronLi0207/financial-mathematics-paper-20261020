# R6：基准保护选参规则与回溯检验设计（评估前冻结）

**状态：待本文件单独提交并核对提交身份后执行；截至写入时没有新回溯拟合、峰值评分或评估结果。** 本设计一次冻结回溯与 inspected 两个阶段，不根据任一阶段结果换主规则、阈值、时期、候选或失败政策。文献依据见同目录上两层的 notes/supervisor-20261023/r6-literature.md；实际版本和访问边界在该记录中。

## 1. 问题、定位和识别边界

问题是：在已经选定的采样双侧绝对头寸峰值任务中，偏向截距参照的保守选参是否减少周度大幅失利，同时保留 FX 的条件分数收益。只组合成熟做法：显式简单候选、one-SE 简约偏好、按时间推进的验证。本任务的配对差 HAC 容忍带是适配，不是 ESL 原公式、显著性检验或非劣性保证；选择 I 不等于 forecast averaging。

**主要规则事先指定 R2；R3 为敏感性比较。** 选择依据是需要冻结的设计自由度和已知小验证样本，未使用新时期结果。

当前仓库 409 个 JSON、17 个角色 CSV 及生产入口审计未发现旧 validation 起点前的金融 evaluation origin。该结论仅限这次可见仓库角色审计；未证明历史上任何人、其他对话、已删除文件或外部论文从未评估。原始文件和早期记录已用于读取、特征及训练。故称“此前未被本仓库审计发现用作 evaluation 的回溯期”，不称未见原始数据、前瞻盲测或独立外部验证。若执行前发现相反的角色证据，保守停止“未曾评估”声明并记录，不能迁移到一个看结果后更好的时期。

## 2. 固定来源、时期与标签时钟

所有索引从零开始，区间端点均包含；日期仅从现有原始文件的时间戳映射，没有计算新标签或损失来选时期。只用现有 FX 和同一 NY Fed 日期网格上的 Treasury-bill 加 12 条已冻结 panel 序列，不重新下载、补值、换序列或增加模型族。

令共同缓冲 H*=24。旧 validation 首索引为 v0；新验证长度 V 为 weekly52、FX1440；回溯评估长度 E=V。固定：
\[
e_{\rm last}=v_0-25,\quad e_{\rm first}=e_{\rm last}-E+1,\quad
v_{\rm last}=e_{\rm first}-25,\quad v_{\rm first}=v_{\rm last}-V+1.
\]
H6/H24 使用同一来源的同一评估 origin 网格。所有回溯目标的末记录 t+H 均小于 v0：weekly 最晚328（2019-07-17），FX最晚10462（2015-10-07 23:00）；因此在旧 validation 起点之前全部完成。外层验证目标也在新评估首 origin 之前完成。

| 来源、阶段和 W | 外层验证索引及日期 | 评估索引及日期 | R3总折数 / 评分origins |
|---|---|---|---|
| nyfed_weekly; retro_pre_original_validation; W=52 | 177–228; 2016-08-24 至 2017-08-16 | 253–304; 2018-02-07 至 2019-01-30 | 3 / 78 |
| nyfed_weekly; inspected_original_evaluation; W=52 | 329–380; 2019-07-24 至 2020-07-15 | 405–681; 2021-01-06 至 2026-04-22 | 7 / 130 |
| nyfed_weekly; inspected_original_evaluation; W=260 | 329–380; 2019-07-24 至 2020-07-15 | 405–681; 2021-01-06 至 2026-04-22 | 1 / 52 |
| fx_hourly; retro_pre_original_validation; W=720 | 7535–8974; 2015.04.21T00:00:00.000 至 2015.07.13T23:00:00.000 | 8999–10438; 2015.07.15T00:00:00.000 至 2015.10.06T23:00:00.000 | 139 / 4752 |
| fx_hourly; retro_pre_original_validation; W=2880 | 7535–8974; 2015.04.21T00:00:00.000 至 2015.07.13T23:00:00.000 | 8999–10438; 2015.07.15T00:00:00.000 至 2015.10.06T23:00:00.000 | 94 / 3672 |
| fx_hourly; inspected_original_evaluation; W=720 | 10463–11902; 2015.10.08T00:00:00.000 至 2015.12.30T23:00:00.000 | 11927–18551; 2016.01.01T00:00:00.000 至 2017.01.23T00:00:00.000 | 200 / 6216 |
| fx_hourly; inspected_original_evaluation; W=2880 | 10463–11902; 2015.10.08T00:00:00.000 至 2015.12.30T23:00:00.000 | 11927–18551; 2016.01.01T00:00:00.000 至 2017.01.23T00:00:00.000 | 155 / 5136 |

周度回溯只有 W52、H6/H24，共13×2=26格；FX回溯W720/2880、H6/H24，共4格。原 inspected 阶段周度两W共52格，FX4格。回溯30个来源/H/W组、inspected56组，各组 F/I/R0–R3 六项均列入完整清单。绝不将13条周度序列当独立样本作合并检验。

## 3. 四条固定选参规则

共同有限菜单为 λ∈{.001,.01,.1,1,10}；I 是普通经验分位数的明确独立候选 ID，不向原 QR 求解器传入数值 Infinity。I 和 corrected-rank F 分别计算、分别报告；有限大 λ 或 I 不声称精确嵌套 F。模型特征、标准化、训练响应尺度、求解器、数值容差、完成标签和投影均复用原实现。

- **R0：**在五个有限候选中选外层验证平均 pinball 最低者，完全并列选 λ 较大者。
- **R1：**加入 I，按外层验证均值最低选择；完全并列偏好 I，其次 λ 从大到小。
- **R2（主规则）：**在 R1 候选中先找最低均值候选 b（同一并列规则）。对每个候选 c，令 d_t(c)=loss_t(c)−loss_t(b)。带宽 L=max{H,floor[4(n/100)^(2/9)]}，要求 n>L。以 Bartlett/Newey–West 估计配对差均值标准误 SE_c=sqrt(max(Ω_c,0)/n)。凡 mean(d_c)≤SE_c 的候选均合格，选最强收缩者；含等号，不添加事后容忍常数。负 raw LRV 原值保留并注明数值截为零，非有限值使该规则格失败。
- **R3：**使用下节事先算出的额外滚动评分折和完整外层验证段，按每个评分 origin 等权，再用与 R2 相同的规则。选择一次后固定整个评估期的 λ；仅模型参数按原 d 频率更新。

HAC 的均值为 math.fsum(d)/n；γ_l 的分母为 n。对每个真实来源记录索引差为 l 的观测对累加中心化乘积：
\[
\widehat\Omega=\gamma_0+2\sum_{l=1}^L(1-l/(L+1))\gamma_l.
\]
R2 连续验证段与正文 NW 定义相同。R3 使用真实索引差，不能把 fold 间被删除记录两侧伪装成相邻观测。SE 不处理同段选出 b 的全部选择后不确定性，也不提供同时检验或覆盖保证。

## 4. R3 的训练历史、滚动折与清除边界

“训练历史”在此固定解释为评估前可用的历史前缀，而不是仅末端 W 个训练标签。每次拟合仍使用原固定 W 个已完成标签，允许取早于评分块的 prehistory；不会缩短 inner W 或改模型。

特征可用首索引 m 为 weekly26、FX168。统一使用 H*=24 得到最早评分 origin q=m+W+24−1；折长 B=d（weekly13、FX24）。在外层验证前，从 b_k=v_first−25−k(B+24)、a_k=b_k−B+1 向后生成完整折，保留 a_k≥q，按时间排序；最后追加完整外层验证段。相邻折之间正好遗漏24个 origin，故上一折最后目标在下一折首 origin 前完成。原 core 允许训练标签末记录等于当前 issue（已知 anchor）；不把这一点声称为训练与评分窗口严格无共享记录或统计独立。

每折调用原 forecast 入口，并以该折首 origin 重置原 refit 日程。每个 refit r 的训练 origins 是 [r−H−W+1,r−H]，标签末记录≤r；所有拟合与评分只用当时可得信息。没有完整前缀折的 inspected weekly W260 预先声明 NO_EXTRA_FOLDS：R3 与 R2 完全相同，仅52个外层验证 origins；这是固定设计恒等式，不是数值失败后的 fallback。

原 inspected R3 的前缀会使用部分本次回溯 evaluation origins。因此必须先完成并封存全部回溯结果，再开始 inspected 计算；后者不得反过来修改本设计、回溯规则或论文发表门槛。回溯阶段构建特征、标签和预测时将实际位置数组截断在 v0 前，避免先构建旧评估期的目标。

## 5. 成功标准、原 primary 结构与论文门槛

对每个完成格定义 Δ=100(mean_pinball_rule/mean_pinball_F−1)，F 为同 W、同 d 的冻结 corrected-rank 历史规则。F 均值为零则百分比未定义、该成功判定不可成立，不删除该格。周度汇总是26个相关格的描述性统计，不是合并检验。

- **S1 保护：**主规则 R2 的26个回溯周度格必须全部完成；最差 Δ≤+25%，中位数 Δ≤+5%。
- **S2 保留：**在回溯 FX 的两个 H6/W720、H6/W2880 格中，凡 R0 的 Δ<0，要求 R2 的 Δ≤0.5Δ_R0。至少存在一个这样的 R0 获益格才可判 PASS；没有则 NOT_ASSESSABLE，不能声称保留收益。任一所需格失败不能判 PASS。
- **S3 改善：**R0、R2各26个周度回溯格全部完成，且 R2 的 Δ 中位数严格低于 R0。用相对同格 F 的变化消除系列规模差别；不把不同量级的原币损失直接取跨系列中位数。所有界值提前固定，不根据结果调整。

除四条新规则，复现两个指定原结构作为单独诊断，不改原 primary：
1. FX：H6/W2880，用原三点菜单{.001,.01,.1}在新验证段选参，与 rolling corrected F/W720/d1 比较。原方向是 QR 降损；回溯平均损失仍更低才记方向复现。
2. Treasury-bill：H6/W52，同样原三点菜单，对 frozen corrected F/W52/d13。原方向是 QR 增损；回溯仍更高才记该短窗口结构方向复现。原 W260 primary 历史不足，**没有精确复现**；表中必须标“W52结构类比”，不能用它替换 W260 原 primary。

论文分支：只有 S1 与 S2 都 PASS，才加≤1.5页方法/检验小节并同步摘要、贡献段、结论及 CONTRIBUTIONS；无论 S3 是否 PASS 都照报。否则仅在稳健性加入一段，摘要不提 R6。无论成功与否，两条原结构结果均以正文小表及一段报告；正文含参考文献≤15页。

## 6. 完整性、执行次序、失败和资源

顺序固定为：文献与本设计单独提交并核对 → 人造单元测试 → 全部回溯规则格与原结构 → 回溯结果封存 → inspected原区间 → 独立数值核对 → 备忘录/论文。不得在封存回溯前先计算 inspected R3 的历史折。

“规则格”固定为阶段/来源/序列/H/W/规则。一个规则所需的任一候选或选中评估预测数值失败，整个规则格标 FAILED，没有完整均值；不改候选、不尝试别的 λ、不 fallback、不重试、不删行。共享候选失败影响所有依赖它的规则；其他预先定义、所需候选均完成的规则仍独立列示。每个已选报告在同一组最多拟合一次，完全相同的报告只共享已完成数组，不重复拟合。F/I 作为独立参照行始终列出；其失败也保留。未运行格也须列状态和原因。

所有原来源、旧结果、E3/E5私有轨迹及原核心代码只读；新输出放入独立 r6 目录，已有目标目录不覆盖。私有原始数据和逐点轨迹不上传。单数值线程，最多2个观察到的系统线程、RSS2GiB、每组900秒、一次运行7200秒；到时未完格保留 TIME_LIMIT/NOT_RUN，不重开运行。缺包仅允许 uv 临时环境，不往系统 Python 安装。

实现先用小人造数据验证 R2 的 paired NW、含等号边界、强收缩并列优先和 I 分派；R3 验证24间隔、历史成熟、真实索引 HAC 与连续拼接不同、未来 eval 不进入选参。只添加隔离选择/切分层，不改原 solver 或工具边界情况。

## 待用户决定

无需等待用户决定即可执行。保守约定已固定：R2主要、R3敏感性；R3使用可用历史前缀且统一24条间隔；成功判定只用回溯期；Treasury W52只称结构类比；零可保留 FX 获益时 S2 不可评估。当前审计无法证明所有外部历史从未使用这些原始记录，论文只作上述有界的仓库角色声明。

## 机器可读冻结合同

下列 JSON 与本文件同次冻结；实现只读它，不在运行后改变任何科学选择。

```json
{
  "research_id": "r6-20261023",
  "baseline_commit": "67d7091b2ebf60505907039ac29f86597db3ad8b",
  "created_utc": "2026-10-23T20:17:46.911033+00:00",
  "primary_rule": "R2",
  "rules": [
    "R0",
    "R1",
    "R2",
    "R3"
  ],
  "reports": [
    "F",
    "I",
    "R0",
    "R1",
    "R2",
    "R3"
  ],
  "finite_penalties": [
    0.001,
    0.01,
    0.1,
    1.0,
    10.0
  ],
  "original_primary_penalties": [
    0.001,
    0.01,
    0.1
  ],
  "infinity_report_id": "I",
  "tau_numerator": 19,
  "tau_denominator": 20,
  "horizons": [
    6,
    24
  ],
  "common_purge": 24,
  "sources": {
    "nyfed_weekly": {
      "record_count": 706,
      "refit_step": 13,
      "short_scale": 6,
      "long_scale": 26,
      "nominal_gap_seconds": 604800,
      "native_unit": "USD millions",
      "feature_prefix": 26,
      "original_validation_start": 329,
      "validation_count": 52,
      "retro_validation": [
        177,
        228
      ],
      "retro_evaluation": [
        253,
        304
      ],
      "inspected_validation": [
        329,
        380
      ],
      "inspected_evaluation": [
        405,
        681
      ],
      "retro_windows": [
        52
      ],
      "inspected_windows": [
        52,
        260
      ]
    },
    "fx_hourly": {
      "record_count": 18576,
      "refit_step": 24,
      "short_scale": 24,
      "long_scale": 168,
      "nominal_gap_seconds": 3600,
      "native_unit": "USD",
      "feature_prefix": 168,
      "original_validation_start": 10463,
      "validation_count": 1440,
      "retro_validation": [
        7535,
        8974
      ],
      "retro_evaluation": [
        8999,
        10438
      ],
      "inspected_validation": [
        10463,
        11902
      ],
      "inspected_evaluation": [
        11927,
        18551
      ],
      "retro_windows": [
        720,
        2880
      ],
      "inspected_windows": [
        720,
        2880
      ],
      "local_path": ".scratch/supervisor-20261023/e3/sources/1hourNetPositionsKaggle.csv",
      "sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
      "bytes": 1286391
    }
  },
  "weekly_series": [
    {
      "series_key": "PDPOSGS-B",
      "local_path": "data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv",
      "raw_bytes": 23315,
      "raw_sha256": "9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb",
      "raw_observations": 706,
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07"
    },
    {
      "series_key": "PDPOSMBS-TOT",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSMBS-TOT.csv",
      "raw_bytes": 25680,
      "raw_sha256": "2e493d17890870eff6eca247c62b9175fcf7564a70d87e63ee520561bb71efcb",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSCS-TOT",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSCS-TOT.csv",
      "raw_bytes": 24713,
      "raw_sha256": "169fdb5201f6a34152936f0aa2b444d9ea0f8814d39750bfd4a4bc942a41fade",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSFGS-TOT",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSFGS-TOT.csv",
      "raw_bytes": 25495,
      "raw_sha256": "00f321abeebf1aaee1af68dc7ab41bb403eafe770c915f4229fc80e18e3586de",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSTIPS-L2",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSTIPS-L2.csv",
      "raw_bytes": 24883,
      "raw_sha256": "dc3dd1ef3f9a364c25789523a5b2f0d46860681808005620055db4a47c996995",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSTIPS-G11",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSTIPS-G11.csv",
      "raw_bytes": 25017,
      "raw_sha256": "810355b1cf4c93282dcc76fa6fdc41bbccc1ec7d3675024a2400e2c27c695d5d",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSTIPS-G2",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSTIPS-G2.csv",
      "raw_bytes": 24761,
      "raw_sha256": "8e54675071813501a240c1ea3a2ca4fda0f2e2aa88b1ea1bb2852fe6a9f6c894",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSTIPS-G6L11",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSTIPS-G6L11.csv",
      "raw_bytes": 26797,
      "raw_sha256": "1e3ee3a336be321f47a3f7481591b15650607baa3fb46be7da99968ccbea7845",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSGSC-L2",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSGSC-L2.csv",
      "raw_bytes": 24714,
      "raw_sha256": "7ab08e2b39534ca67f43006949a7504334d90b63034b9ed3cd5248e59c9126bf",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSGSC-G2L3",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSGSC-G2L3.csv",
      "raw_bytes": 25930,
      "raw_sha256": "10c35a9516154011c0821d12eb86052f7d4df01a4c7b0cddee4878b72868678c",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSGSC-G3L6",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSGSC-G3L6.csv",
      "raw_bytes": 26090,
      "raw_sha256": "453f1a2458a2c9c7049d9128ccc9d1945b5a61e469ab1c8112577b3ad7539fa5",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSGSC-G6L7",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSGSC-G6L7.csv",
      "raw_bytes": 25967,
      "raw_sha256": "429d542e2cda305d8d5c458592b57b4042c9f479ce4135e3ab3610951ae6b35d",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    },
    {
      "series_key": "PDPOSGSC-G7L11",
      "local_path": ".scratch/supervisor-round2-20261023/e5/sources/PDPOSGSC-G7L11.csv",
      "raw_bytes": 26639,
      "raw_sha256": "0b102760c5e4cc181d438d9c8618f8990d047ac8ecb9bd85bac63851742199d0",
      "raw_observations": 707,
      "raw_first_date": "2013-04-03",
      "raw_last_date": "2026-10-14",
      "aligned_observations": 706,
      "aligned_first_date": "2013-04-03",
      "aligned_last_date": "2026-10-07",
      "alignment": "Existing immutable 706-date grid; extra raw date excluded, no imputation."
    }
  ],
  "panel_manifest_sha256": "c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858",
  "core_sha256": {
    "conditional_study.py": "aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "conditional_sources.py": "a56cb374cff93b5d18889d2b69a993ad1a3b871ee20bb8349fad04b2fc839709",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf",
    "empirical_headroom.py": "db5d73facae28432bb0617d173e5b4c933d95e52b43f9363543e21194919412e",
    "inference_tests.py": "2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c",
    "round2_panel_sources.py": "e0b553d370a23f9dcc38caeb649e048bb880c6fcc9b93536d2e9a30402c4c17d"
  },
  "literature_sha256": "43b1c8f7e8366047e2418fd20eb9ac1572948f9a1d919b481b00153da81ecc7f",
  "metadata_audit_sha256": "b62c4ec88c37bb28246afc9a33eba661d779aeb51483d0d317ada918babf9163",
  "expected_groups": {
    "retro": 30,
    "inspected": 56
  },
  "expected_rule_cells": {
    "retro": 180,
    "inspected": 336
  },
  "r3_fold_formula": "B=d; earliest=m+W+24-1; b_k=validation_first-25-k*(B+24); a_k=b_k-B+1; keep a_k>=earliest, sort; append complete outer validation",
  "r3_loss_weighting": "equal weight per scored origin, no independent-fold assumption",
  "hac_bandwidth": "max(H,floor(4*(n/100)**(2/9))); require n>L",
  "hac_lag_definition": "actual source-record index difference, not concatenated adjacency",
  "hac_center": "math.fsum(d)/n; covariance pair sums divided by n",
  "one_se_eligible": "mean(candidate_loss-best_loss)<=sqrt(max(raw_Bartlett_NW_LRV,0)/n), inclusive, no extra tolerance",
  "strength_order": [
    "0.001",
    "0.01",
    "0.1",
    "1",
    "10",
    "I"
  ],
  "tie_rule": "strongest on exact mean-loss ties",
  "selection_time": "once before each evaluation phase; selected penalty held fixed for whole phase",
  "r3_no_extra_folds": "inspected weekly W260 uses outer validation alone; R3=R2 by frozen construction, not fallback",
  "phase_order": [
    "retro",
    "seal_retro_outputs",
    "inspected"
  ],
  "retro_raw_prefix_only": true,
  "no_retries": true,
  "rule_cell_failure": "any required candidate failure makes the whole source/H/W/rule cell FAILED; no partial metric, alternate parameter, fallback or row dropping; shared candidate failures affect every rule requiring that candidate",
  "shared_eval_failure": "a selected report is fitted at most once per group; a failure makes every rule selecting it FAILED",
  "resource_limits": {
    "requested_threads": 1,
    "max_observed_threads": 2,
    "max_rss_bytes": 2147483648,
    "group_wall_seconds": 900,
    "run_wall_seconds": 7200
  },
  "success": {
    "S1": {
      "weekly_R2_complete_required": 26,
      "worst_percent_vs_F_max": 25.0,
      "median_percent_vs_F_max": 5.0
    },
    "S2": {
      "FX_H6_windows": [
        720,
        2880
      ],
      "eligibility": "R0_percent_vs_F<0",
      "pass": "R2_percent_vs_F<=0.5*R0_percent_vs_F in every eligible cell",
      "require_at_least_one_eligible": true,
      "failed_required_cell": "NOT_MET",
      "zero_eligible": "NOT_ASSESSABLE"
    },
    "S3": {
      "definition": "median weekly cell percent_vs_F of R2 < median weekly cell percent_vs_F of R0",
      "complete_both_required": 26
    }
  },
  "publication_gate": "new section <=1.5 pages and abstract/contribution updates iff S1 and S2 PASS; otherwise a robustness paragraph without abstract mention; always report two original-structure retrospective comparisons in a small table plus paragraph",
  "primary_replication": [
    {
      "id": "FX-original-structure",
      "source": "fx_hourly",
      "horizon": 6,
      "window": 2880,
      "rule": "QR restricted original 3-penalty menu selected on retro validation",
      "reference": "rolling corrected F, W720, refit1",
      "direction_replicated": "QR mean pinball < reference"
    },
    {
      "id": "Treasury-W52-structural-analogue",
      "source": "nyfed_weekly",
      "series_key": "PDPOSGS-B",
      "horizon": 6,
      "window": 52,
      "rule": "QR restricted original 3-penalty menu selected on retro validation",
      "reference": "frozen corrected F, W52, refit13",
      "direction_replicated": "QR mean pinball > reference",
      "limitation": "Original W260 primary is not exactly replicated; W52 is explicitly adapted because W260 unavailable in this retrospective design"
    }
  ]
}
```
