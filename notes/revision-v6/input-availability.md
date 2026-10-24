# WP1 输入可用性与指纹只读盘点

盘点日期：2026-10-23。范围是原 8 个 source/H/W 格与额外 12 条 Treasury 序列的 48 格。仅检查路径、文件字节摘要、公开 manifest 绑定、NPZ 键名/shape 与 origin 起止；没有读取逐期金融数值、计算损失、组合、状态或运行预测。所有路径相对仓库根目录。

## 可用性结论

| 输入范围 | F | QR | KNN | 验证状态 |
|---|---|---|---|---|
| 原 8 格评估轨迹 | 8/8 可用，`frozen_F_capacity` | 8/8 可用，`QR_capacity` | 8/8 可用，`KNN_capacity` | 24/24 NPZ 对应 companion manifest 的大小与 SHA-256 均匹配；companion manifests 与 `numerical-audit/public` 对应 receipts 字节一致。 |
| 原 8 格 QR/KNN 验证段候选轨迹 | F 验证段未在 reference bundle 中留存 | 8/8 可用 | 8/8 可用 | 16/16 验证段 NPZ 对 companion manifest 的大小与 SHA-256 均匹配；候选编号映射仍须按已冻结 selection 文件读取。 |
| 附加 12 条 Treasury × 4 格评估轨迹 | 48/48 可用，`frozen_F` | 48/48 可用，`QR33` | 0/48，缺失 | 48/48 公共 cell 的 source/selection 绑定匹配；现有公共 cell 未保存 NPZ 摘要，因此不能宣称私有面板 NPZ 已被旧公开摘要逐文件验证。 |

原 8 格的 F/QR/KNN 评估轨迹具有一致的长度和起止索引元数据。附加面板 48 个 NPZ 均保留同一评估段的 `origins`、`peak`、`floor`、`frozen_F`、`Levy_L`、`QR33` 和 `C2_QR4`。逐期金融向量未在本记录公开；完整键名、shape、origin 起止和本次指纹仅写入 `.scratch/revision-v6/input-inventory.json`。

## 原 8 格路径与状态

根路径：`.scratch/revision-20261022/replication-revision-v3-b5-full/`。每格的 F 在 `references-{source}-h{H}-w{W}/private/numeric-traces.npz`；QR/KNN 分别在 `evaluation-{source}-h{H}-w{W}-{QR,KNN}/private/numeric-traces.npz`。同目录 `public/manifest.json` 为伴随指纹。

| source | H | W | 评估 F/QR/KNN | 对公开摘要验证 |
|---|---|---|---|---|
| fx_hourly | 6 | 720 | 全部可用 | PASS |
| fx_hourly | 6 | 2880 | 全部可用 | PASS |
| fx_hourly | 24 | 720 | 全部可用 | PASS |
| fx_hourly | 24 | 2880 | 全部可用 | PASS |
| nyfed_weekly | 6 | 52 | 全部可用 | PASS |
| nyfed_weekly | 6 | 260 | 全部可用 | PASS |
| nyfed_weekly | 24 | 52 | 全部可用 | PASS |
| nyfed_weekly | 24 | 260 | 全部可用 | PASS |

候选验证轨迹的相对目录形式为 `validation-{source}-h{H}-w{W}-{QR,KNN}/private/numeric-traces.npz`。`references-...` bundle 只有评估 origins，不能把它当作已保存的 F 验证轨迹。原始输入 `.scratch/data/1hourNetPositionsKaggle.csv` 与 `.scratch/revision-20261022/nyfed-PDPOSGS-B.csv` 均存在，大小和摘要匹配 `protocol/revision-20261022/executable-freeze.json`；公开 Treasury 副本 `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv` 也匹配该冻结摘要。

## 附加面板路径与状态

公共入口：`protocol/revision-20261023/round2-D3-panel.json`、`results/revision-20261023/round2/panel/selection-manifest.json`。私有轨迹路径形式为 `.scratch/round2/panel-models/{series_key}-h{6,24}-w{52,260}/numeric-traces.npz`；公共 cell 形式为 `results/revision-20261023/round2/panel/cells/{series_key}-h{H}-w{W}.json`。

| 序列 | F/QR 四格 | KNN 四格 | source/provenance 与 selection 绑定 |
|---|---|---|---|
| PDPOSMBS-TOT | 全部可用 | 全部缺失 | PASS |
| PDPOSCS-TOT | 全部可用 | 全部缺失 | PASS |
| PDPOSFGS-TOT | 全部可用 | 全部缺失 | PASS |
| PDPOSTIPS-L2 | 全部可用 | 全部缺失 | PASS |
| PDPOSTIPS-G11 | 全部可用 | 全部缺失 | PASS |
| PDPOSTIPS-G2 | 全部可用 | 全部缺失 | PASS |
| PDPOSTIPS-G6L11 | 全部可用 | 全部缺失 | PASS |
| PDPOSGSC-L2 | 全部可用 | 全部缺失 | PASS |
| PDPOSGSC-G2L3 | 全部可用 | 全部缺失 | PASS |
| PDPOSGSC-G3L6 | 全部可用 | 全部缺失 | PASS |
| PDPOSGSC-G6L7 | 全部可用 | 全部缺失 | PASS |
| PDPOSGSC-G7L11 | 全部可用 | 全部缺失 | PASS |

12 份面板 raw CSV 位于 `.scratch/round2/panel-data/{series_key}.csv`；其当前字节摘要均匹配 `results/revision-20261023/round2/panel/sources/{series_key}/provenance.json`，并与对应公共 cell 的 source 摘要一致。现有公开 cell schema 绑定的是 source 和 selection，不含私有 NPZ 摘要。本次私有清单记录的是当前 NPZ 指纹，不能追溯创造一个先前不存在的公开绑定。

两个原先因缺失经济日期跳过的候选 `PDPOSGSC-G11L21`、`PDPOSGSC-G21` 继续是跳过状态；本次未补齐、拼接或重跑。

## 六份原 CSV 的字节一致性

逐文件将 `.scratch/revision-20261022/replication-revision-v3-b5-full/numerical-audit/public/` 与 `results/revision-20261022/` 的同名文件直接比较，并核对前者 `reproduction-comparison.json` 的 export 摘要。没有解析或重新计算 CSV 中的金融结果。

| 文件 | 两处均存在 | 当前字节一致 | 两处摘要均匹配已存 export 摘要 |
|---|---|---|---|
| `evaluation-summary.csv` | PASS | PASS | PASS |
| `evaluation-annual.csv` | PASS | PASS | PASS |
| `evaluation-nonoverlap.csv` | PASS | PASS | PASS |
| `paired-comparisons.csv` | PASS | PASS | PASS |
| `paired-annual.csv` | PASS | PASS | PASS |
| `paired-nonoverlap.csv` | PASS | PASS | PASS |

## 对后续 WP 的输入边界

- 原 8 格已经具有 F/QR/KNN 的评估输入，可在设计冻结后进入规定的计算；本盘点不构成组合或评分结果。
- 附加面板已有 F 与 QR 的等权组合输入。F/QR/KNN 三报告中位数缺 KNN；不能以 C2 或 L 静默替代。按 WP3“可用的格子”处理时应明示该缺失；如要新增面板 KNN，需要在运行前另行冻结其设计，不能把现存面板当成已有 KNN。
- ACI 验证段可能需要额外生成 F 验证预测；当前 references NPZ 的评估轨迹不能冒充验证轨迹。是否及如何生成应由事先冻结的 WP2 设计处理。
- 面板 NPZ 的旧公开摘要绑定缺口仍在；当前 metadata/来源绑定通过不等于逐期金融输出已独立重现。若后续工作依赖更强的复现要求，应由主流程决定是否按已授权设计重现并核验归档。
- 本次没有恢复废纸篓、复制原数据、安装依赖、修改原文件、运行任何实验、提交或推送。
