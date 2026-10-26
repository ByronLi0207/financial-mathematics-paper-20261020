# C2 登记前：已有输入路由与时间边界

本记录是时间戳和输入完整性元数据，不是断点诊断或模型结果。2026-10-24 18:18–18:21 UTC 期间只读旧目录、校验 bytes/SHA、复制既有输入到新 clone 忽略区，并读取旧日频 NPZ 的 `times.npy`。没有读取 `position.npy`，没有把 CSV 的头寸字段转换成数值，没有重新聚合、拟合、校准、模拟、预测或统计检验。

机器可读清单：`notes/v9/input-boundaries.json`。它只包含输入身份、路由、请求的首尾边界，不含原始 CSV、数组、完整时间序列或私有逐期头寸/预测。

## 输入路由

- FX：`.scratch/v9/inputs/1hourNetPositionsKaggle.csv`，1286391 bytes，SHA-256 `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`。
- 12 条 panel：`.scratch/v9/inputs/panel/<KEY>.csv`。KEY、bytes、SHA 和原路径均列在 JSON 的 `input_routes`，依据 `results/revision-20261023/round2/panel/selection-manifest.json` 的12条 ELIGIBLE，未加入2条 SKIPPED。
- Treasury：直接读取新 clone 已有 `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv`，23315 bytes，SHA-256 `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb`，没有多造一份。
- 原始输入只来自旧目录 `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/` 的既有文件；13 个复制目标原来均不存在，使用 exclusive create，权限0600。`git check-ignore` 逐项确认目标被忽略。源/目标散列不符数为0。
- Panel date check 只查看经济日期与series key：每条raw707个互异日期，包含全部706条 Treasury 固定日期网格；没有将头寸值带入对齐运算或检验。新诊断应在登记后用原 `round2_panel_sources.align_source` 依固定网格对齐后再取 prefix。

## 已有合同的边界

所有索引均为0-based。FX时钟是 source-naive，无时区转换或UTC断言。

| 对象 | 只允许的原评估前prefix | 首个允许观测 | 最后允许观测 | 首个原评估观测 |
|---|---|---|---|---|
| Treasury + 12 panel，各自 | 0..404，共405 | 2013-04-03 | 2020-12-30 | index405，2021-01-06 |
| 已存daily FX | 0..404，共405 | 2014-02-05T23:59:59.999999 | 2015-05-22T23:59:59.999999 | index405，2015-05-24T23:59:59.999999 |
| hourly FX，原合同前缀 | 0..11926，共11927 | 2014-02-05T01:00:00.000000 | 2015-12-31T23:00:00.000000 | index11927，2016-01-01T00:00:00.000000 |

周度边界依据 `protocol/revision-20261022/study-spec.json` 和 panel D3 合同，日期来自 Treasury 原已归档CSV。Daily边界来自原WP4 manifest的private directory下 `W52_H6/daily-series.npz`；读取的唯一数组成员是 `times.npy`，总长930，NPZ SHA与公开 `worker-source.json.daily_mapping_sha256` 一致：`421547a72242e2af62cf3b5621542de33706b905ec89a4ef18deda7afaf54afd`。`times.npy` 的canonical payload SHA也与公开`issue_times_sha256`一致：`923e3a8676a7f5f5cbb5965f73d663f37282209dbda16bcf1d7ef5dbd87ee004`。

## 给 root 决定的 N4 共同日历前缀候选

这不是已选择的设计或诊断结果，只回答所询问的timestamp search：

- 日历区间为 **[2014-02-05T00:00:00.000000，2015-05-24T00:00:00.000000)**。
- Daily保留原index0..404的405条；首评估日index405从2015-05-24开始，其issue到该日日末才发出。
- Hourly要求timestamp严格早于该评估日开始，并仍在原hourly评估index11927之前：得到 **0..8108，共8109条**。首条2014-02-05T01:00，末条2015-05-22T21:00。
- 第一个排除的hourly observation是index8109，2015-05-24T22:00；没有填充2015-05-23或其他空白日。
- 采用的是 `bisect_left` 对timestamp的边界定位，没有按头寸值、断点结果或模型性能选择cutoff。Daily405个观测和hourly8109个观测覆盖同一source-naive日历前缀，但不是相同数量或相同采样目标。

## 登记后、仅合成序列的最小 WP3 调用样例（未执行）

下例中的 `position`、`times` 只能是新v9生成器已产生的**合成序列**；不能将上方真实输入路由传入此预测段。此处只是接口示例，不生成数据、不安装包、不选择新设计。

```python
# Conceptual caller supplied by the registered v9 controller:
# position, times = <synthetic arrays with retained length 3264>
# checkpoint = <v9-owned resource/deadline callable>
# public = <fresh exclusive per-source/state/rep/W/H output directory>

import numpy as np
import v8_mechanism_mc as mc
import run_v8_wp3 as sealed
from conditional_features import build_features
from conditional_quantile import QuantileFitError
from conditional_study import score_predictions
from study_core import build_label_cache, stable_mean
from run_study import StudyStop

features = build_features(
    position, times,
    short_scale=24, long_scale=168, nominal_gap_seconds=3600)
assert features.valid_from == 168
H = 6
cache = build_label_cache(position, H)
validation = np.arange(3072, 3144, dtype=np.int64)  # 72 issues
evaluation = np.arange(3168, 3240, dtype=np.int64)  # 72 issues

selection_design = {
    "validation_first": 3072,
    "validation_last": 3143,
    "menus": {
        "QR33": [0.001, 0.01, 0.1],
        "QR4": [0.001, 0.01, 0.1, 1.0, 10.0],
    },
}

def report(segment, h, w, method, penalty):
    origins = validation if segment == "validation" else evaluation
    result = mc.forecast_report(
        position, times, features, cache, origins,
        h, w, 24, method, penalty, checkpoint=checkpoint)
    scored = score_predictions(
        cache.peak[origins], result["capacity"],
        np.abs(position[origins]), origins)
    n = len(origins)
    hits = int(np.count_nonzero(scored.strict_breach))
    scalar_score = {
        "mean_loss": stable_mean(scored.pinball),
        "strict_breach_count": hits,
        "strict_breach_rate": hits / n,
        "n": n,
    }
    return scalar_score, sealed.scalar_diagnostics(result["fit_diagnostics"])

# The new v9 controller supplies one fresh `public` directory per W/H.
# Each call below is one method, not a whole-grid runner:
row = sealed.evaluate_method(
    selection_design, public, W, H, method,
    report, checkpoint, QuantileFitError,
    (sealed.DriverStop, StudyStop))
```

在此接口中，W由新控制器取52或260，method按F、QR33、QR4顺序；`public`的路径必须能区分全部source/state/rep/W/H，不能只用旧WP3的文件名当全局身份。`evaluate_method` 会写候选、selection、started和method receipts，不能复用已有文件；遇到旧目录或重复目标会拒绝写入。

若v9控制器的resource exception使用新的类型，必须把该实际异常类型也放进 `resource_errors`；上例沿用旧checkpoint接口，仅说明已有类型。不要吞掉预算异常再继续计完整分数。

固定拟合政策与返回语义：

1. `forecast_report` 调用原 `fit_quantile_ridge` 默认max_iter10000、atol1e-6、rtol1e-5、gap_rtol1e-6，tau19/20、无截距惩罚；没有warm-start或新optimizer选项。beta初始化全0，截距初始化为训练响应inverted-CDF tau分位，scaled_dual0。
2. refit r的训练origin固定为 `r-H-W+1..r-H`；每24个issue更新，验证/评估分别anchor。池、变换、响应scale和系数块内冻结，当前query/floor不断更新。F修正秩为ceil(19(W+1)/20)，不计算I。
3. QR33三个候选全部完成才能选，按完整72个validation issue的mean pinball最小，精确tie取较大lambda。QR4按完成候选中最小mean pinball，精确tie取递增菜单第一项，失败候选仍保留。所有候选只跑一次。
4. 只对所选参数跑一次完整72 issue评估。失败不换参数、不缩短score、不把非有限值投影成floor；评估异常在row里记FAILED。资源异常会先写失败receipt再重抛。
5. **返回FAILED row不必然抛异常**；v9控制器必须显式检查row.status，并按其事先登记的whole-cell/whole-repetition规则传播缺失。完整计划库存不能因早停而缩小。旧helper自身不会替新设计定义跨source/state/rep的“整格”。
6. `summary_from_repetitions` 是ratio of mean losses，不能直接用作用户N2/N3的median判据。median层级/公式由新设计登记。per-issue arrays只能留private或内存；此样例只公开标量score与有限fit/maturity诊断。
