# REVISION V9 CHANGELOG

研究窗口：UTC 2026-10-24T19:10:12Z 至 2026-10-25T05:10:12Z（温哥华10月24日12:10:12至22:10:12）。不重启窗口；锁屏等待不计有效研究，原时间记录保留。

## WP0: PASS — 同步底稿与 PR 整理

执行顺序：先完成 v8 冻结笔记原生浏览器发布；核对完整底稿与保护引用；核对 PR #3/#4/#5 元数据与 #5 正文实际保存；最后才创建本轮 v9 跟踪文件。下面的整树证据仅绑定新 v9 文件创建前的基线。

实际命令：

```text
python3 -B notes/revision-v8/verify_wp9_remote_tree.py --source-commit 0d3cd138359a72cc8df5f2260483c919cce2f620 --output .scratch/revision-v9/wp0-final-base-proof.json
```

返回码：0。输出原文（完整副本亦见 notes/revision-v9/wp0-sync-command-output.txt）：

```json
{
  "utc": "2026-10-24T21:52:03.883017+00:00",
  "status": "PASS",
  "source_commit": "0d3cd138359a72cc8df5f2260483c919cce2f620",
  "remote_commit": "d3c2061b208fe11e0a4aa7c5cdc48a399cd48f34",
  "source_tree": "e36ecb7144ae38ed5a2b660eca24c07fd2cfa0e4",
  "remote_tree": "e36ecb7144ae38ed5a2b660eca24c07fd2cfa0e4",
  "source_files": 3320,
  "remote_files": 3320,
  "files_checked": 3320,
  "bytes_checked": 150957975,
  "missing": [],
  "extra": [],
  "changed_or_mode_mismatches": [],
  "git_diff_returncode": 0,
  "per_file_sha256_csv": ".scratch/revision-v9/wp0-final-base-proof-files.csv",
  "per_file_csv_sha256": "043528ddae5e6170addbfd5f575789f4d126016e1aa8dc8aff8e2a559cf502a8",
  "protected_remote_refs": {
    "main": "65feeee801b6b228a608ca3200e0678bb5f62b1c",
    "codex/supervisor-revision-20261023": "2328994c44ec02bd731ad556f41fe9821f6de6df",
    "revision-v7-final": "d119a1fb30c48ceab9000552057882938cfa57a4"
  },
  "protected_ref_differences": {},
  "elapsed_seconds": 0.931718375,
  "blob_stream_buffer_max_bytes": 65536,
  "no_remote_mutations": true,
  "no_Git_identity_objects_published": true,
  "scope": "Complete file-tree and streamed content identity; remote/local commit histories differ. Financial replay and journal acceptance are not certified."
}
```

实际 GitHub 元数据工具调用：`github_get_pr_info`，repository_full_name=`ByronLi0207/financial-mathematics-paper-20261020`，pr_number 分别为 3、4、5。返回的实际范围字段：

```json
[
  {
    "number": 3,
    "url": "https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/3",
    "title": "Refocus the peak-position paper and verify the ridge-menu comparison",
    "state": "open",
    "merged": false,
    "head": "codex/supervisor-revision-20261023",
    "head_sha": "2328994c44ec02bd731ad556f41fe9821f6de6df",
    "base": "main",
    "base_sha": "65feeee801b6b228a608ca3200e0678bb5f62b1c",
    "updated_at": "2026-10-24T06:30:02Z",
    "source_tool": "github_get_pr_info"
  },
  {
    "number": 4,
    "url": "https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/4",
    "title": "Publish verified v7 peak-position manuscript and complete evidence",
    "state": "open",
    "merged": false,
    "head": "revision-v7-final",
    "head_sha": "d119a1fb30c48ceab9000552057882938cfa57a4",
    "base": "main",
    "base_sha": "65feeee801b6b228a608ca3200e0678bb5f62b1c",
    "updated_at": "2026-10-24T07:52:13Z",
    "source_tool": "github_get_pr_info"
  },
  {
    "number": 5,
    "url": "https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/5",
    "title": "Evaluate peak-position forecast regimes with complete v8 evidence",
    "state": "open",
    "merged": false,
    "head": "revision-v8-goal",
    "head_sha": "d3c2061b208fe11e0a4aa7c5cdc48a399cd48f34",
    "base": "main",
    "base_sha": "65feeee801b6b228a608ca3200e0678bb5f62b1c",
    "updated_at": "2026-10-24T21:49:44Z",
    "source_tool": "github_get_pr_info"
  }
]
```

整理说明：notes/revision-v9/pr-consolidation.md，建议以 #5 为唯一投稿准备线；是否关闭 #3/#4 由用户决定，本任务未关闭、合并或修改其分支。

PR #5 说明的原始字节核对先报告不一致，原因是 GitHub 将 17 个 LF 换成 CRLF；仅做 CRLF→LF 后与预备正文完全相等，未用任意空白压缩掩盖内容差异。原失败与归一核对均保留在本任务忽略的交付记录，科学文件不受影响。

执行边界：没有安装、删除、投稿或新金融计算；原有两个 primary、归档数字、负结果、私有原始数据的发布限制均保留。尚未实施 WP1。WP0 本地结束提交在这些验收产物之后创建，其实际 SHA 由下一阶段记录绑定。

### 规则与状态说明

- v8 的最后发布是已结束研究窗口的交付收尾；等待不是新增研究时间。v8 时间间隔与提交节奏的 MISMATCH 未被改写。
- v9 当前为 WP0→WP7 顺序执行阶段，依计划在每项结束及 WP2/WP3 设计冻结处提交；全部 WP 之后的复核循环才适用每小时最多一次的合并 local/browser 提交时钟。不得把复核阶段的时钟拆成两轨。
- 原生 Goal 仍使用旧项标签；不为创建新标签而虚报旧任务的时间合规。当前用户 v9 授权与本窗口 ledger 决定实际任务范围，原生条目状态和窗口分别如实记录。
- 所有自检实际时间、迟到和间隔问题保留在本任务 .scratch/revision-v9/selfchecks.jsonl；不得把调度、锁屏或出版等待包装为十小时有效阅读/计算。

## WP1: IN PROGRESS — pre-calculation rule freeze

Before calculating any candidate rank correlation, logistic score or breakeven threshold, wrote protocol/revision-v9/wp1-posthoc-design.md and .json. Input hashes cover five sealed simulation/design sources and four empirical-overlay tables; real data cannot select the metric or threshold. Three nominal indices, exact score tie order, fixed cached logistic specification, zero-crossing/NA rules and all 1999 cluster-bootstrap statuses are specified in advance. The common-rep bootstrap preserves paired innovation streams. Finite-only intervals are conditional; the all-draw endpoint envelope is reserved for later prediction, with unbounded outcomes marked non-discriminating. No mechanism is assumed supported.

Read-only source verification found actual nominal p34/p5, with constant Treasury/calendar columns and different penalty/failure rules retained as limitations. P3 has no common exact index support for a/b and will remain NOT_TESTABLE rather than be redefined. Source schema was inspected without fitting candidate effects. Cached runtime metadata: Python3.12.14, NumPy2.3.5, SciPy1.18.1, sklearn1.9.1; L2 uses l1_ratio=0 because the penalty argument is deprecated. Official method documentation is linked in the frozen JSON.

## WP1: PASS — 事后分界、完整重采样与原始经验对照

规则先提交：`7f0fee8f1cfdeed584098bbc27570e88eafaea43`，设计 SHA256 `fddbd6ffd1c08dbd44a6dd2bbbfe3ce1dfb8de3329c515d30a5754eb6db14b48`。运行后的规则未改。仅对已有 v8 结果计算；无新金融 forecast/DGP/raw-FX读取。新增 v9_posthoc.py、test_v9_posthoc.py、notes/revision-v9/wp1-* 与 results/revision-v9/wp1/，原科学归档与两个 primary 均未改。

实际数值命令及资源：`python3 -B .scratch/revision-v9/run_wp1_bounded.py`（原封不动 runner 已保存为 notes/revision-v9/run_wp1_bounded.py）。原始命令在数值保存后绘图阶段因缺 matplotlib 返回1，原 traceback 完整保留在 wp1-analysis-console.txt；没有将它写成成功运行。

```json
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--no-project",
    "--no-env-file",
    "--python",
    "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "--with",
    "pytest",
    "--with",
    "arch",
    "--with",
    "scikit-learn",
    "python",
    "-B",
    "v9_posthoc.py",
    "--output",
    "results/revision-v9/wp1"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023",
  "started_utc": "2026-10-24T22:09:05.269251+00:00",
  "ended_utc": "2026-10-24T22:09:08.326210+00:00",
  "elapsed_seconds": 3.056826707907021,
  "returncode": 1,
  "child_peak_rss_bytes": 246185984,
  "sampled_process_tree_peak_rss_bytes": 313606144,
  "maximum_observed_numeric_os_threads": 2,
  "resource_samples": 11,
  "stop_reason": null,
  "numerical_workers": 1,
  "numerical_threads_configured": 1,
  "UV_OFFLINE": true,
  "output_sha256": "d42ec6ce7c3bbea4e46f7360a0996985c642dad148686d2cc058cda9dbe4c6d6"
}
```

仅绘图恢复：已缓存临时环境 `uv run --no-project --no-env-file --with matplotlib python -B -`，stdin 从保存 JSON 调用 v9_posthoc.plot_initial；不重新拟合、不再 bootstrap，无安装。图 PNG 已直接查看，PDF/PNG hash及实际视检记录见 wp1-visual-inspection.json。

```json
{
  "started_utc": "2026-10-24T22:09:33.334603+00:00",
  "ended_utc": "2026-10-24T22:09:43.390830+00:00",
  "elapsed_seconds": 10.056268458953127,
  "peak_rss_bytes": 132120576,
  "returncode": 0,
  "numerical_results_recomputed": false,
  "matplotlib": "3.11.2",
  "offline_cached_temporary_dependency": true
}
```

Synthetic TDD：最初13项因模块尚未实现报错；实现后13通过；对照3项先因缺函数失败再通过；非有限数据回归用例先失败再修复。所有原始失败及成功输出保留。最后命令 `uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B -m pytest -p no:cacheprovider -q test_v9_posthoc.py --basetemp .scratch/revision-v9/wp1-green-pytest-4`，输出原文：

```text
WARN `--no-project` was provided, but no project was found
........................                                                 [100%]
24 passed in 1.99s
```

独立核对实际 launcher：`env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 UV_OFFLINE=1 /usr/bin/time -l uv run --offline --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B -`。实际完整 stdin 原封不动保存在 notes/revision-v9/audit_wp1.py，没有导入生产 analyzer，也没改原输出。原始完整输出：

```text
WARN `--no-project` was provided, but no project was found
SOURCE reports=6912 selected_cells=144 replicas_per_cell=32 n=72 fingerprint_mismatches=0 paired_loss_mismatches=0 max_archived_delta_abs_difference=8.526512829121202e-14
METRICS correct_out_of_144={"a": 117, "b": 119, "c": 119} selected=c label_wins=45 score_mismatches=0 spearman_mismatches=0 max_spearman_abs_difference=1.1102230246251565e-16
BOOTSTRAP method=QR33 draws=1999 point=106.49618468616566 finite=1999 statuses={"IDENTIFIED": 1999} envelope={"coverage_guarantee": false, "lower": 27.894967082095143, "upper": 110.71007095944418, "upper_unbounded": false} mismatches=0 max_curve_y_abs_difference=0.0
BOOTSTRAP method=QR4 draws=1999 point=27.324522025270575 finite=1999 statuses={"IDENTIFIED": 1999} envelope={"coverage_guarantee": false, "lower": 13.27239395223403, "upper": 107.10936480242033, "upper_unbounded": false} mismatches=0 max_curve_y_abs_difference=0.0
OVERLAY census=120 sources=8/8/8/96 unique_locators=120 source_pair_mismatches=0 metric_mismatches=0 status_COMPLETE=120
RESOURCE {"elapsed_seconds": 1.1900085001252592, "maximum_observed_process_os_threads": 1, "numeric_workers": 1, "numerical_threads_configured": 1, "process_peak_rss_bytes": 258113536, "versions": {"numpy": "2.3.5", "python": "3.12.14", "scikit_learn": "1.9.1", "scipy": "1.18.1"}}
PASS independent_wp1_readback imported_v9_posthoc=False original_results_written=False original_outputs_unchanged=True
        3.41 real         2.89 user         0.25 sys
           258113536  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               55199  page reclaims
                1959  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   1  messages sent
                   1  messages received
                   1  signals received
                1352  voluntary context switches
                2049  involuntary context switches
           226896786  instructions retired
           105947053  cycles elapsed
            44712536  peak memory footprint
```

完整默认发现测试：`python3 -B notes/revision-v9/run_full_pytest.py wp1-full-gate`。无筛选/无新增skip；完整 stdout 在 notes/revision-v9/wp1-full-gate-pytest-output.txt。返回的实际 receipt 和原始末行：

```json
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--no-project",
    "--no-env-file",
    "--python",
    "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "--with",
    "pytest",
    "--with",
    "arch",
    "--with",
    "scikit-learn",
    "python",
    "-B",
    "-m",
    "pytest",
    "-p",
    "no:cacheprovider",
    "-v",
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp1-full-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp1-full-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked/indexed file copied; no test filter or skips added",
  "tracked_files_copied": 3353,
  "started_utc": "2026-10-24T22:12:10.450776+00:00",
  "ended_utc": "2026-10-24T22:14:04.437096+00:00",
  "elapsed_seconds": 113.98660800000653,
  "returncode": 0,
  "child_peak_rss_bytes": 346128384,
  "sampled_process_tree_peak_rss_bytes": 419856384,
  "stop_reason": null,
  "output_sha256": "438322ac9862ead06939a34a44c279fa9369b0f2fef20b2cc3000295a8707a3d",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
```

```text
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1359 passed, 1068 subtests passed in 113.19s (0:01:53) ============
```

验收含144格、6912份报告、每模型1999完整抽样、120原始经验格(8/8/8/96)、0 NA_MISMATCH和独立容差内0差异；不是bitwise全等，浮点最大差在原始输出明确保留。

实质结果：候选得分 a117/144，b119/144，c119/144；按预写平局规则选 c=W/(H+1)。这不含p，不能单独确认每参数机制。QR33首切点106.49618468616566；QR4首切点27.324522025270575，并有第二个向下交点。全部交点、宽区间、所有bootstrap状态和25个经验不一致格保留。经验 CONSISTENT/INCONSISTENT 明确定义为 first-cutpoint hypothesis diagnostic，不是完整非单调曲线一致性或普遍阈值规律。详见 wp1-readout.md、wp1-breakeven.json。WP1仍只是post hoc，WP2/WP3未运行。

MISMATCH/失败：原 combined 命令缺少绘图库并返回1，单独读取保存结果补图后恢复；原始日志不覆盖。未改变已冻结统计定义，也未为改善结果换指标/种子/区间。WP1结束提交在全部验收文件之后创建；后续状态将记录实际SHA。

## WP2: IN PROGRESS — 运行前确认设计冻结

WP1结束提交9784372d523e93a50f21212e9a10adb55485768c已通过，工作区曾实际核实干净。新写 protocol/revision-v9/wp2-confirmatory.md/.json；新DGP、种子、精确P1/P2范围和48/24分母、48个P3配对、完整/缺失/打平判据以及预算缩减顺序均在运行前写定。不得运行后改。主screen明确为pooled，分方法/DGP矛盾必须保留；c不含参数个数。尚未生成WP2 DGP、抽取正式种子或拟合。

运行前只读旧metadata估时命令：`python3 -B -`读取旧archive的study-termination.json及WP1readout；输出原文：

```json
{
  "actual_utc": "2026-10-24T22:16:40.507601+00:00",
  "wp1_end_commit": "9784372d523e93a50f21212e9a10adb55485768c",
  "source_old_metadata": "results/revision-v8/wp3/wp3-driver-output.tar.gz:study-termination.json",
  "original_study_elapsed_seconds": 2059.6466849998105,
  "original_worker_count": 288,
  "new_planned_worker_count": 192,
  "linear_wall_estimate_seconds": 1373.0977899998738,
  "safety_factor": 2.0,
  "safety_wall_estimate_seconds": 2746.1955799997477,
  "global_budget_seconds": 5400,
  "old_maximum_worker_seconds": 10.024692,
  "new_dgp_not_generated": true,
  "all32_initially_planned": true,
  "threshold_regions": {
    "QR33": {
      "r_star": 106.49618468616566,
      "low_boundary": 53.24809234308283,
      "high_boundary": 212.99236937233132,
      "low_WH": [
        [
          52,
          6
        ],
        [
          52,
          24
        ],
        [
          260,
          6
        ],
        [
          260,
          24
        ],
        [
          720,
          24
        ]
      ],
      "high_WH": [
        [
          2880,
          6
        ]
      ]
    },
    "QR4": {
      "r_star": 27.324522025270575,
      "low_boundary": 13.662261012635287,
      "high_boundary": 54.64904405054115,
      "low_WH": [
        [
          52,
          6
        ],
        [
          52,
          24
        ],
        [
          260,
          24
        ]
      ],
      "high_WH": [
        [
          720,
          6
        ],
        [
          2880,
          6
        ],
        [
          2880,
          24
        ]
      ]
    }
  },
  "expected_P1_cell_count": 48,
  "expected_P2_cell_count": 24,
  "expected_P3_pair_count": 48
}
```

三种创新项单位方差、3:1 regime标准差、每Poisson事件独立正负5倍GaussianSD均明确。第一次预算检查固定在rep0–15全部完成后，只有耗时参与；先减少W52余下16rep，再260、720、2880。保留全部NA/失败，禁止结果导向缩减。设计审查未发现阻断提交的科学合同矛盾。新种子2026102492与v8及WP1不同。正式设计提交将早于run manifest/RNG/results。

WP1附带工具记录：`git diff HEAD^ HEAD --check`对未改写的原始pytest stdout末尾空格返回2；完整警告见 wp1-raw-log-whitespace-check.txt。对v9代码/设计/结果及结构化记录的同项检查返回0。原始stdout按原字节保留，没有修剪以伪造无差异；此非科学数值MISMATCH。

## WP2: PASS — 新DGP确认与全部反例保留

设计冻结提交 `f2ce438ccb2fcf671c849a83032ac700ac6007c6` 早于正式run manifest/RNG。MD/JSON与该提交逐字一致；正式代码hash在运行前封存并在192个worker前后核对。没有改动原始模块、旧科学数字或归档。

TDD先见10个缺模块错误，再实现生成过程/固定判据；独立审查发现失败优先级问题，构造用例先失败后修复；之后原driver/core加新契约测试60项通过。预算移除保留完整BUDGET_REDUCED库存，正式运行无需触发。小测试只用entropy19，未提前抽取正式seed2026102492。实际末次运行前命令 `uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B -m pytest -p no:cacheprovider -q test_v9_confirmation.py test_v8_wp3_driver.py test_v8_wp3_core.py --basetemp .scratch/revision-v9/wp2-green-pytest-4`，原始输出：

```text
WARN `--no-project` was provided, but no project was found
............................................................             [100%]
60 passed in 0.58s
```

唯一正式运行实际命令（线程变量均在启动前设1，UV_OFFLINE=1）：`uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B run_v9_confirmation.py --run`，工具返回码0；完整stdout原文：

```text
WARN `--no-project` was provided, but no project was found
{"status": "COMPLETE", "reason": null, "attempted": 192, "completed": 192, "removed_windows": []}
```

终止记录：

```json
{
  "status": "COMPLETE",
  "reason": null,
  "ended_utc": "2026-10-24T22:50:26.787681+00:00",
  "elapsed_seconds": 1507.0915186251514,
  "attempted_workers": 192,
  "completed_workers": 192,
  "removed_windows": [],
  "code_seal": "PASS",
  "all_workers_terminated": true
}
```

预定rep0–15后的无结果预算检查，实际原文：

```json
{
  "actual_utc": "2026-10-24T22:38:20.531656+00:00",
  "after_reps": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15
  ],
  "uses_losses": false,
  "removed_windows": [],
  "projected_seconds_before": 773.1567138005048,
  "projected_seconds_after": 773.1567138005048,
  "remaining_seconds": 4619.166298374999,
  "allowance_seconds": 4157.2496685375,
  "can_continue": true
}
```

192个正式worker全部结束后才运行汇总：`uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B run_v9_confirmation.py --summarize`，返回0。完整输出原文单独保留于 notes/revision-v9/wp2-summary-console.txt；完整144-cell JSON/CSV与全部P1/P2/P3逐格判定见 results/revision-v9/wp2。

核对/包装构造测试实际命令：`uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B -m pytest -p no:cacheprovider -q test_v9_confirmation.py test_v9_confirmation_audit.py test_v9_confirmation_package.py --basetemp .scratch/revision-v9/wp2-post-run-pytest-1`，原始输出：

```text
WARN `--no-project` was provided, but no project was found
...............................                                          [100%]
31 passed in 0.20s
```

独立实际命令：全部7数值线程变量=1、UV_OFFLINE=1，`uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn python -B notes/revision-v9/audit_wp2.py --output notes/revision-v9/wp2-independent-audit.json`，返回0；它不导入新生产core/aggregation、不重新拟合。原始完整console在 wp2-independent-audit-console.txt；实际receipt原文：

```json
{
  "status": "PASS",
  "mismatch_count": 0,
  "differences": [],
  "difference_count": 0,
  "initial_inventory_records": 4608,
  "summary_cells": 144,
  "synthetic_inputs_regenerated": 192,
  "evaluation_traces_verified": 4608,
  "candidate_receipts_checked": 12288,
  "worker_resource_receipts": 192,
  "worker_maximum_rss_bytes": 63930368,
  "worker_maximum_os_threads": 1,
  "worker_maximum_wall_seconds": 11.445564874913543,
  "inventory_status_counts": {
    "COMPLETE": 4608
  },
  "removed_windows": [],
  "P1": {
    "status": "SUPPORT",
    "successes": 47,
    "missing": 0,
    "denominator": 48,
    "lower_bound": 0.9791666666666666,
    "upper_bound": 0.9791666666666666,
    "observed_fraction": 0.9791666666666666,
    "minimum_fraction": 0.8,
    "cells": [
      [
        "student_t5",
        0,
        52,
        6,
        "QR33"
      ],
      [
        "student_t5",
        0,
        52,
        6,
        "QR4"
      ],
      [
        "student_t5",
        0,
        52,
        24,
        "QR33"
      ],
      [
        "student_t5",
        0,
        52,
        24,
        "QR4"
      ],
      [
        "student_t5",
        0,
        260,
        6,
        "QR33"
      ],
      [
        "student_t5",
        0,
        260,
        24,
        "QR33"
      ],
      [
        "student_t5",
        0,
        260,
        24,
        "QR4"
      ],
      [
        "student_t5",
        0,
        720,
        24,
        "QR33"
      ],
      [
        "student_t5",
        1,
        52,
        6,
        "QR33"
      ],
      [
        "student_t5",
        1,
        52,
        6,
        "QR4"
      ],
      [
        "student_t5",
        1,
        52,
        24,
        "QR33"
      ],
      [
        "student_t5",
        1,
        52,
        24,
        "QR4"
      ],
      [
        "student_t5",
        1,
        260,
        6,
        "QR33"
      ],
      [
        "student_t5",
        1,
        260,
        24,
        "QR33"
      ],
      [
        "student_t5",
        1,
        260,
        24,
        "QR4"
      ],
      [
        "student_t5",
        1,
        720,
        24,
        "QR33"
      ],
      [
        "regime_3to1",
        0,
        52,
        6,
        "QR33"
      ],
      [
        "regime_3to1",
        0,
        52,
        6,
        "QR4"
      ],
      [
        "regime_3to1",
        0,
        52,
        24,
        "QR33"
      ],
      [
        "regime_3to1",
        0,
        52,
        24,
        "QR4"
      ],
      [
        "regime_3to1",
        0,
        260,
        6,
        "QR33"
      ],
      [
        "regime_3to1",
        0,
        260,
        24,
        "QR33"
      ],
      [
        "regime_3to1",
        0,
        260,
        24,
        "QR4"
      ],
      [
        "regime_3to1",
        0,
        720,
        24,
        "QR33"
      ],
      [
        "regime_3to1",
        1,
        52,
        6,
        "QR33"
      ],
      [
        "regime_3to1",
        1,
        52,
        6,
        "QR4"
      ],
      [
        "regime_3to1",
        1,
        52,
        24,
        "QR33"
      ],
      [
        "regime_3to1",
        1,
        52,
        24,
        "QR4"
      ],
      [
        "regime_3to1",
        1,
        260,
        6,
        "QR33"
      ],
      [
        "regime_3to1",
        1,
        260,
        24,
        "QR33"
      ],
      [
        "regime_3to1",
        1,
        260,
        24,
        "QR4"
      ],
      [
        "regime_3to1",
        1,
        720,
        24,
        "QR33"
      ],
      [
        "compound_poisson",
        0,
        52,
        6,
        "QR33"
      ],
      [
        "compound_poisson",
        0,
        52,
        6,
        "QR4"
      ],
      [
        "compound_poisson",
        0,
        52,
        24,
        "QR33"
      ],
      [
        "compound_poisson",
        0,
        52,
        24,
        "QR4"
      ],
      [
        "compound_poisson",
        0,
        260,
        6,
        "QR33"
      ],
      [
        "compound_poisson",
        0,
        260,
        24,
        "QR33"
      ],
      [
        "compound_poisson",
        0,
        260,
        24,
        "QR4"
      ],
      [
        "compound_poisson",
        0,
        720,
        24,
        "QR33"
      ],
      [
        "compound_poisson",
        1,
        52,
        6,
        "QR33"
      ],
      [
        "compound_poisson",
        1,
        52,
        6,
        "QR4"
      ],
      [
        "compound_poisson",
        1,
        52,
        24,
        "QR33"
      ],
      [
        "compound_poisson",
        1,
        52,
        24,
        "QR4"
      ],
      [
        "compound_poisson",
        1,
        260,
        6,
        "QR33"
      ],
      [
        "compound_poisson",
        1,
        260,
        24,
        "QR33"
      ],
      [
        "compound_poisson",
        1,
        260,
        24,
        "QR4"
      ],
      [
        "compound_poisson",
        1,
        720,
        24,
        "QR33"
      ]
    ],
    "outcomes": [
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      false,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true
    ]
  },
  "P2": {
    "status": "SUPPORT",
    "successes": 21,
    "missing": 0,
    "denominator": 24,
    "lower_bound": 0.875,
    "upper_bound": 0.875,
    "observed_fraction": 0.875,
    "minimum_fraction": 0.6,
    "cells": [
      [
        "student_t5",
        0,
        720,
        6,
        "QR4"
      ],
      [
        "student_t5",
        0,
        2880,
        6,
        "QR33"
      ],
      [
        "student_t5",
        0,
        2880,
        6,
        "QR4"
      ],
      [
        "student_t5",
        0,
        2880,
        24,
        "QR4"
      ],
      [
        "student_t5",
        1,
        720,
        6,
        "QR4"
      ],
      [
        "student_t5",
        1,
        2880,
        6,
        "QR33"
      ],
      [
        "student_t5",
        1,
        2880,
        6,
        "QR4"
      ],
      [
        "student_t5",
        1,
        2880,
        24,
        "QR4"
      ],
      [
        "regime_3to1",
        0,
        720,
        6,
        "QR4"
      ],
      [
        "regime_3to1",
        0,
        2880,
        6,
        "QR33"
      ],
      [
        "regime_3to1",
        0,
        2880,
        6,
        "QR4"
      ],
      [
        "regime_3to1",
        0,
        2880,
        24,
        "QR4"
      ],
      [
        "regime_3to1",
        1,
        720,
        6,
        "QR4"
      ],
      [
        "regime_3to1",
        1,
        2880,
        6,
        "QR33"
      ],
      [
        "regime_3to1",
        1,
        2880,
        6,
        "QR4"
      ],
      [
        "regime_3to1",
        1,
        2880,
        24,
        "QR4"
      ],
      [
        "compound_poisson",
        0,
        720,
        6,
        "QR4"
      ],
      [
        "compound_poisson",
        0,
        2880,
        6,
        "QR33"
      ],
      [
        "compound_poisson",
        0,
        2880,
        6,
        "QR4"
      ],
      [
        "compound_poisson",
        0,
        2880,
        24,
        "QR4"
      ],
      [
        "compound_poisson",
        1,
        720,
        6,
        "QR4"
      ],
      [
        "compound_poisson",
        1,
        2880,
        6,
        "QR33"
      ],
      [
        "compound_poisson",
        1,
        2880,
        6,
        "QR4"
      ],
      [
        "compound_poisson",
        1,
        2880,
        24,
        "QR4"
      ]
    ],
    "outcomes": [
      false,
      true,
      true,
      true,
      false,
      false,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true,
      true
    ]
  },
  "P3": {
    "status": "NOT_SUPPORT",
    "successes": 42,
    "missing": 0,
    "denominator": 48,
    "lower_bound": 0.875,
    "upper_bound": 0.875,
    "observed_fraction": 0.875,
    "minimum_fraction": 1.0,
    "secondary": true
  },
  "primary_status": "SUPPORT",
  "by_method": {
    "QR33": "SUPPORT",
    "QR4": "SUPPORT"
  },
  "by_DGP": {
    "student_t5": "SUPPORT",
    "regime_3to1": "SUPPORT",
    "compound_poisson": "SUPPORT"
  },
  "audit_elapsed_seconds": 132.50022458308376,
  "audit_peak_rss_bytes": 135397376,
  "audit_maximum_observed_os_threads": 1,
  "audit_numerical_threads_configured": 1,
  "production_core_imported": false,
  "production_aggregation_imported": false,
  "model_fits_run": 0,
  "validation_boundary": "selection from retained scalar validation losses; validation forecast traces were not saved",
  "original_files_written": 0
}
```

独立逐issue math/input/selection/maturity与汇总0差异，容差abs1e-10/rel1e-12，不声称bitwise普遍等同。validation没有保存forecast NPZ，所以只核对保存的scalar validation loss所决定的λ，未声称逐issue重算validation或重新估计QR系数。

实际打包命令：`/usr/bin/time -l python3 -B notes/revision-v9/package_wp2.py`，返回0。所有合成原记录保持原始内容，tar owner/time等元数据正规化；原文件未删除。完整输出原文：

```text
{
  "status": "PASS",
  "actual_utc": "2026-10-24T22:54:17.600042+00:00",
  "elapsed_seconds": 6.927943999879062,
  "formal_source": ".scratch/revision-v9/wp2-run",
  "members": 30536,
  "uncompressed_bytes": 83094855,
  "archive_bytes": 20739514,
  "archive_sha256": "aa794fc6b83c0e4e74f98b11aa4768a90f6f03dfe052fda9d679cd9e88972e7a",
  "index_sha256": "9e942726a6c5bec102ad7c25fb2e4a5b000df59694fce87831517ce85fb9a3ba",
  "mismatches": 0,
  "source_files_deleted": 0,
  "metadata_sanitized": "tar mode644; uid/gid0, empty owner names, mtime0; content bytes unchanged"
}
        6.95 real         3.92 user         1.46 sys
           143605760  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                9105  page reclaims
                   0  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
               25768  voluntary context switches
                 122  involuntary context switches
         70300838926  instructions retired
         20699007381  cycles elapsed
           133104216  peak memory footprint
```

默认全套测试实际命令：`python3 -B notes/revision-v9/run_full_pytest.py wp2-full-gate`。无筛选/新增skip；完整 stdout 保存在 wp2-full-gate-pytest-output.txt，返回receipt与末行原文：

```json
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--no-project",
    "--no-env-file",
    "--python",
    "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "--with",
    "pytest",
    "--with",
    "arch",
    "--with",
    "scikit-learn",
    "python",
    "-B",
    "-m",
    "pytest",
    "-p",
    "no:cacheprovider",
    "-v",
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp2-full-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp2-full-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked/indexed file copied; no test filter or skips added",
  "tracked_files_copied": 3397,
  "started_utc": "2026-10-24T22:55:48.600721+00:00",
  "ended_utc": "2026-10-24T22:57:35.206860+00:00",
  "elapsed_seconds": 106.60622875019908,
  "returncode": 0,
  "child_peak_rss_bytes": 335413248,
  "sampled_process_tree_peak_rss_bytes": 401162240,
  "stop_reason": null,
  "output_sha256": "a29ee2485b67a9c26e18d04af6ec01a8afe2a7f6de4cb7ac4ed6c438e74149d3",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
```

```text
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1390 passed, 1068 subtests passed in 105.96s (0:01:45) ============
```

科学结论严格区分验收：P1 47/48、P2 21/24均通过，pooled primary为SUPPORT；P3 42/48，全格均不差的次要预测NOT_SUPPORT。六个P3反例、P1/P2未满足格及全部不利cells保留在 wp2-all-prediction-counterexamples.csv 与完整summary。不能把87.5%写成全格成功，不能以P1/P2通过推出参数数目机制；c仍不含p。WP3真实学习曲线尚未开始。

附带MISMATCH：新的方法书目核对发现NBER对Turner等期刊版年份字段与出版社不同，采用出版社1989，阅读层级与原始链接见 wp2-method-source-reading.md。22:50自检的通用running_scope文字仍说无终止，实际status及完整study_termination已正确记录终止；原记录保留，并在本地runtime增加文字erratum，不影响时间戳或科学结果。

## WP3: IN PROGRESS — 原期间学习曲线运行前冻结

WP2已结束提交 `1a535efe289254ced5b163361fefee357d13d583`。只读核对canonical raw的hash/bytes/记录数，与既有16个公开/私人归档hash/NPZ headers；未读出任何金融行，未新forecast/HAC。Raw只复制到本任务新private目录，原始文件未动；复制回执在 wp3-private-input-copy-receipt.json，来源/缺失历史字段明细见 wp3-source-preflight.json。

写定新的 protocol/revision-v9/wp3-learning-curve.md/.json，数值预测从WP1 all-draw envelope原样乘(H+1)，不取整或为命中网格扩区间。NA不可跨接，0/∞范围不可测试，左右删失/零触及/多根不伪造确认。首先运行H6/W2880、H24/W2880 exact gate，任何旧可比向量/标量/λ不符立即BLOCKED，不重试或另选归档。QR4历史没有保存的字段明确不可核对，不声称旧公开hash已绑定。原validation10463..11902与eval11927..18551保持；W5760的成熟历史可满足，不改变期间。

这还是旧已研究FX期间的回顾性检验，不能叫新的金融holdout；新λ菜单、额外HLN/coverage/带宽搜索或新模型均未获本轮计算授权。DM仅固定原Bartlett NW带宽及双侧normal诊断；不按p选择曲线。来源函数复用原QR33/QR4及F-only分支，避免顺带计算S/K。设计核对命令 `python3 -B -` 读取指定frozen archives/protocol hashes并断言一致；输出原文：

```json
{
  "actual_utc": "2026-10-24T23:13:50.989187+00:00",
  "status": "PASS_PRECALCULATION_DESIGN",
  "wp2_end_commit": "1a535efe289254ced5b163361fefee357d13d583",
  "new_FX_forecasts": 0,
  "new_HAC": 0,
  "protocol_hashes": {
    "protocol/revision-v9/wp3-learning-curve.json": "0490302463c17096b612fa7241cae97fed082052cefd29f176f0eba3926aedae",
    "protocol/revision-v9/wp3-learning-curve.md": "58855b74a875dd0632e571074f7fd1e3bb507bb12e61d2c32d8188c79f1d02e6"
  },
  "source_copy_sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
  "legacy_archive_metadata_mismatches": 0,
  "peer_review": "No blocking contract contradiction; 16 existing archive files metadata verified read-only; no arrays valued/fitted",
  "prediction_ranges": [
    {
      "horizon": 6,
      "method": "QR33",
      "lower": 195.264769574666,
      "upper": 774.9704967161092,
      "upper_unbounded": false,
      "source_envelope": {
        "lower": 27.894967082095143,
        "upper": 110.71007095944418,
        "upper_unbounded": false,
        "coverage_guarantee": false
      },
      "numeric_testable": true
    },
    {
      "horizon": 6,
      "method": "QR4",
      "lower": 92.90675766563821,
      "upper": 749.7655536169423,
      "upper_unbounded": false,
      "source_envelope": {
        "lower": 13.27239395223403,
        "upper": 107.10936480242033,
        "upper_unbounded": false,
        "coverage_guarantee": false
      },
      "numeric_testable": true
    },
    {
      "horizon": 24,
      "method": "QR33",
      "lower": 697.3741770523785,
      "upper": 2767.7517739861046,
      "upper_unbounded": false,
      "source_envelope": {
        "lower": 27.894967082095143,
        "upper": 110.71007095944418,
        "upper_unbounded": false,
        "coverage_guarantee": false
      },
      "numeric_testable": true
    },
    {
      "horizon": 24,
      "method": "QR4",
      "lower": 331.8098488058507,
      "upper": 2677.7341200605083,
      "upper_unbounded": false,
      "source_envelope": {
        "lower": 13.27239395223403,
        "upper": 107.10936480242033,
        "upper_unbounded": false,
        "coverage_guarantee": false
      },
      "numeric_testable": true
    }
  ],
  "runtime_estimate": {
    "old_W2880_measured_seconds": {
      "6": 82.36570449988358,
      "24": 72.21311250003055
    },
    "window_scaling_sum": 3.875,
    "safety_factor": 2.0,
    "safety_total_estimated_seconds": 1197.9858317493345
  },
  "bandwidth_by_horizon": {
    "6": 10,
    "24": 24
  }
}
```

本设计将在任何新curve forecast/HAC之前提交。窗口与资源预算不重置，逐点结果/失败/NA及所有交点保留。

### WP3 pre-run implementation and sole run start

设计已先提交`b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a`。随后TDD实现exact gate、固定curve分类与HAC；代码未改变冻结协议。静态审查发现中断前候选/selection落盘过晚，正式运行前用独立exclusive候选JSON/NPZ、先行selection、pre-gate evaluation保存修正。新构造测试先RED后GREEN。

验算命令（所有7个数值线程变量=1，UV_OFFLINE=1，既有bundled Python通过cached uv运行，未安装）：

```sh
uv run --offline --python <existing bundled Python> --with pytest --with arch --with scikit-learn python -B -m pytest test_v9_learning_curve.py test_conditional_study.py test_conditional_features.py test_v8_wp3_core.py test_parsimonious_v3.py -q
```

Raw output wp3-red-persistence-output.txt (middle command had nonexistent test filename, corrected before run):

```text
..............F                                                          [100%]
=================================== FAILURES ===================================
______ test_candidate_and_selection_evidence_survives_later_gate_failure _______

tmp_path = PosixPath('/private/var/folders/4g/4pc4x_0x10dcd_t1wwhqss980000gn/T/pytest-of-bingyouli/pytest-123/test_candidate_and_selection_e0')

    def test_candidate_and_selection_evidence_survives_later_gate_failure(tmp_path):
     import run_v9_learning_curve as driver,json
     public=tmp_path/'public'
     candidate=dict(parameter=.01,status='FAILED',failure={'code':'SOLVER'},mean_pinball=None)
>    driver.record_candidate(public,'QR33',0,candidate,[{'refit_index':10,'status':'FAILED'}])
     ^^^^^^^^^^^^^^^^^^^^^^^
E    AttributeError: module 'run_v9_learning_curve' has no attribute 'record_candidate'

test_v9_learning_curve.py:96: AttributeError
=========================== short test summary info ============================
FAILED test_v9_learning_curve.py::test_candidate_and_selection_evidence_survives_later_gate_failure
1 failed, 14 passed in 0.15s
```

Raw output wp3-green-persistence-output.txt (middle command had nonexistent test filename, corrected before run):

```text
ERROR: file or directory not found: test_v8_mc_core.py


no tests ran in 0.00s
```

Raw output wp3-green-persistence-output-2.txt (middle command had nonexistent test filename, corrected before run):

```text
.....................................................................    [100%]
69 passed in 0.35s
```

运行前metadata verifier命令`uv ... python -B -`直接调用`verify_design()`，核Git已提交协议、全部旧代码/input hash，再封存代码：

```json
{
  "actual_utc": "2026-10-24T23:24:35.895093+00:00",
  "status": "PASS_PRE_RUN",
  "design_commit": "b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a",
  "design_bytes_match_commit": true,
  "formal_forecasts_started": false,
  "targeted_tests": "69 passed in0.35s",
  "code_hashes": {
    "run_v9_learning_curve.py": "9952026f3b95e7f6239b876417c0ff7e74df7146962384edac833ad611352ed4",
    "v9_learning_curve.py": "f219d43e00859239eb21d05c5ea458fe5817984faada315a87265f811b9e4ec8",
    "run_conditional_study.py": "14881dc6611feef3cd642558ecdff0571f16dde1af1081349c2d99bd36dbf2e0",
    "v3_revision.py": "1d0b0ceb92ae6c09cff6d34f0be07d01309fb23d07d484d76a6284bbd19e4eb8",
    "run_v8_wp3.py": "1b5489fc9875137fc1217f2bfe412046f1a353287d234a201f9ac29da3e7352f",
    "run_study.py": "8d8c305357e888f7665beed67dcc8f8a3619070a33a30d935c9582512db18f1f",
    "conditional_sources.py": "a56cb374cff93b5d18889d2b69a993ad1a3b871ee20bb8349fad04b2fc839709",
    "conditional_study.py": "aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740",
    "conditional_features.py": "4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5",
    "conditional_quantile.py": "2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7",
    "study_core.py": "1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf",
    "parsimonious_v3.py": "d330cf53c34b8cb8c9b6b182bf0c8ae21b40b92548e71644abfbf4ceb7e259e8",
    "v8_mechanism_mc.py": "71134570e1b4d63f98dcd2bb4eb7c1bc596a516b3ca8243b77ad913670a7d7c4",
    "inference_tests.py": "2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c"
  },
  "protocol_hashes": {
    "protocol/revision-v9/wp3-learning-curve.md": "58855b74a875dd0632e571074f7fd1e3bb507bb12e61d2c32d8188c79f1d02e6",
    "protocol/revision-v9/wp3-learning-curve.json": "0490302463c17096b612fa7241cae97fed082052cefd29f176f0eba3926aedae"
  },
  "input_seals": {
    ".scratch/revision-v9/wp3-input/1hourNetPositionsKaggle.csv": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
    "notes/revision-v9/wp1-breakeven.json": "84d983fffcc79b19d9a1618cf44a7d3c11a2b40f8d51eb23cb0068c13b069184",
    "notes/revision-v9/wp3-source-preflight.json": "8ebe30e98e27f732a3115a79f78c866682a8be4dd98b7dc3190f92b8e91b40b5",
    "results/revision-20261022/validation-fx_hourly-h6-w2880-QR.json": "dbc56674ff3331d3f46fc2d0c90a9bca2bedaa277793b1b478909f0d3ac9aa68",
    "results/revision-20261022/evaluation-fx_hourly-h6-w2880-QR.json": "30f872660f7b6eabbcec884d0a8fabca0f2071f52eb861414c5750f0b053f49f",
    "results/revision-20261022/references-fx_hourly-h6-w2880.json": "020ed4ba49c58ed6186031c821e2d7cf3d3d8187731e435fddb25b0d4637c6f2",
    "results/revision-20261022/validation-fx_hourly-h24-w2880-QR.json": "a75f0f4a492509ec97e83ea5dedefe89c07e77b37fccee57b64634b631a268a2",
    "results/revision-20261022/evaluation-fx_hourly-h24-w2880-QR.json": "5e13a67a74c0e79735e47365811cce6c5044bb4e2c16b225e6eb409cef4385cf",
    "results/revision-20261022/references-fx_hourly-h24-w2880.json": "9e4b399bb8c9b371481873d9c80c49d553cc7285bb3f72fb0b816e642cf2e25f",
    ".scratch/revision-20261022/replication-revision-v3-b5-full/validation-fx_hourly-h6-w2880-QR/private/numeric-traces.npz": "f689e3aa1c80bd1038559653b3258abe910bffbf1e82263321786d3714dfd3e6",
    ".scratch/revision-20261022/replication-revision-v3-b5-full/evaluation-fx_hourly-h6-w2880-QR/private/numeric-traces.npz": "2d7b1950a8a94fb194319616179486fef0b83f14b6ca68a76ec18871d91609bf",
    ".scratch/revision-20261022/replication-revision-v3-b5-full/references-fx_hourly-h6-w2880/private/numeric-traces.npz": "12fbd3a7858dbf4397ddee4392cdd0043bfd5cd1a973d21f81968fe3440232c9",
    ".scratch/revision-20261022/replication-revision-v3-b5-full/validation-fx_hourly-h24-w2880-QR/private/numeric-traces.npz": "04813257646c434574b8dd2543e4b9a81bda9d0784611175f11c039f497fde9d",
    ".scratch/revision-20261022/replication-revision-v3-b5-full/evaluation-fx_hourly-h24-w2880-QR/private/numeric-traces.npz": "4adcd90f111303f5d83bf9a5d241ff5b0abf653fd5cf8662d07b8237dc055c67",
    ".scratch/revision-20261022/replication-revision-v3-b5-full/references-fx_hourly-h24-w2880/private/numeric-traces.npz": "b143db8e2e39002b0c0f6943ec12afa5e06d9b51c7a81be6a3f58673a8470f5e",
    "results/revision-20261023/parsimonious/fx_hourly-h6-w2880.json": "b32541cb18e3ee149e68932affbfb0c02026dd8fa79625066a198493bf567d87",
    ".scratch/v3-parsimonious/fx_hourly-h6-w2880/numeric-traces.npz": "6a1a81692b48cb302d9c20d221d542168816af1d6581dd50c3cea1da6bcd00ff",
    "results/revision-20261023/parsimonious/fx_hourly-h24-w2880.json": "6e6d18e979e1fdc2b6ba6bc1fe78bb0821ee83701c0973b0b959fcb2ae6d34b9",
    ".scratch/v3-parsimonious/fx_hourly-h24-w2880/numeric-traces.npz": "21cab12c76dc117da22fcd1c131f8b245e1fd1b23df07649d872b377774d09db"
  },
  "persistence_fix": "per-candidate metadata and private trace, selection before exact gate/evaluation, pre-gate evaluation scalars; no forecast arithmetic or frozen rules changed"
}
```

唯一正式命令，stdout原文保存`notes/revision-v9/wp3-formal-run-console.txt`，manifest先于新forecast：

```sh
UV_OFFLINE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 /Users/bingyouli/.local/bin/uv run --offline --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v9_learning_curve.py --run
```

两个W2880 exact gate均已实际PASS，原协议与seal未变，后续固定W继续；这只是数值正确性gate，不是机制确认。证据输出原文：

```json
{
  "actual_utc": "2026-10-24T23:27:37.460807+00:00",
  "status": "PASS_BOTH_EXACT_W2880_GATES",
  "design_commit": "b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a",
  "gate_receipts": [
    {
      "horizon": 6,
      "baseline_checks": [
        {
          "status": "PASS",
          "phase": "references",
          "method": "F",
          "horizon": 6,
          "legacy_public": "results/revision-20261022/references-fx_hourly-h6-w2880.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/references-fx_hourly-h6-w2880/private/numeric-traces.npz",
          "science_scalars_checked": 45,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "validation",
          "method": "QR33",
          "horizon": 6,
          "legacy_public": "results/revision-20261022/validation-fx_hourly-h6-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/validation-fx_hourly-h6-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 3647,
          "arrays_checked": 18,
          "values_checked": 25920,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "evaluation",
          "method": "QR33",
          "horizon": 6,
          "legacy_public": "results/revision-20261022/evaluation-fx_hourly-h6-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/evaluation-fx_hourly-h6-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 5590,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "method": "QR4",
          "horizon": 6,
          "science_scalars_checked": 1960,
          "arrays_checked": 4,
          "values_checked": 26500,
          "mismatches": 0,
          "scope": "old four evaluation vectors and public scalars; absent old validation/floor/refit vectors not claimed"
        }
      ],
      "elapsed_seconds": 73.70251520792954,
      "resources": {
        "started_utc": "2026-10-24T23:24:51.727512+00:00",
        "checkpoint_utc": "2026-10-24T23:26:05Z",
        "measurement_point": "final_checkpoint_before_manifest",
        "requested_numerical_threads": 1,
        "elapsed_seconds": 73.68805254204199,
        "peak_rss_bytes": 91324416,
        "maximum_observed_os_threads": 1,
        "thread_probe_status": "PASS",
        "thread_snapshot_count": 289,
        "completed_stability_lengths": [],
        "current_stage": "finalization",
        "current_cell_id": null,
        "current_length": null,
        "completed_origins_current_cell": 0,
        "completed_replicates_current_length": 0,
        "new_output_bytes_at_checkpoint": 3126993,
        "private_numeric_output_bytes_at_checkpoint": 2145890,
        "public_analysis_output_bytes_at_checkpoint": 981103
      }
    },
    {
      "horizon": 24,
      "baseline_checks": [
        {
          "status": "PASS",
          "phase": "references",
          "method": "F",
          "horizon": 24,
          "legacy_public": "results/revision-20261022/references-fx_hourly-h24-w2880.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/references-fx_hourly-h24-w2880/private/numeric-traces.npz",
          "science_scalars_checked": 45,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "validation",
          "method": "QR33",
          "horizon": 24,
          "legacy_public": "results/revision-20261022/validation-fx_hourly-h24-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/validation-fx_hourly-h24-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 3647,
          "arrays_checked": 18,
          "values_checked": 25920,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "evaluation",
          "method": "QR33",
          "horizon": 24,
          "legacy_public": "results/revision-20261022/evaluation-fx_hourly-h24-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/evaluation-fx_hourly-h24-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 5590,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "method": "QR4",
          "horizon": 24,
          "science_scalars_checked": 1960,
          "arrays_checked": 4,
          "values_checked": 26500,
          "mismatches": 0,
          "scope": "old four evaluation vectors and public scalars; absent old validation/floor/refit vectors not claimed"
        }
      ],
      "elapsed_seconds": 64.08799737505615,
      "resources": {
        "started_utc": "2026-10-24T23:26:05.521468+00:00",
        "checkpoint_utc": "2026-10-24T23:27:09Z",
        "measurement_point": "final_checkpoint_before_manifest",
        "requested_numerical_threads": 1,
        "elapsed_seconds": 64.07695791590959,
        "peak_rss_bytes": 90324992,
        "maximum_observed_os_threads": 1,
        "thread_probe_status": "PASS",
        "thread_snapshot_count": 250,
        "completed_stability_lengths": [],
        "current_stage": "finalization",
        "current_cell_id": null,
        "current_length": null,
        "completed_origins_current_cell": 0,
        "completed_replicates_current_length": 0,
        "new_output_bytes_at_checkpoint": 3119122,
        "private_numeric_output_bytes_at_checkpoint": 2138479,
        "public_analysis_output_bytes_at_checkpoint": 980643
      }
    }
  ],
  "archive_scope": "all enumerated available old fields; old QR4 validation/floor/refit vectors absent and not claimed",
  "later_windows_may_start": true
}
```

运行开始后另见auxiliary失败diagnostic容器边界，未改sealed code/重跑。原`_failure`仍保存数值diagnostics/context；如无partial_forecast，单独fit_diagnostics可能只是key列表，不冒称完整fitclock。待结束audit核实际发生次数。见wp3-failure-diagnostics-scope.json。

### WP3 PASS — 全曲线完成，三条已识别相容、一条删失不可检验

唯一正式run已经正常退出，全部10单位、80validation候选、20选定QR评估与10matchedF完整，未重试/改规格。总study超过10分钟但单naturalunit最大低于600s，不能混淆两个预算口径。汇总命令`uv ... python -B run_v9_learning_curve.py --summarize`在全部worker结束后运行一次；完整原输出在wp3-summary-console.txt，完整20行DM表与全部四分类见wp3-readout.md/公开contrasts.csv。

正式运行stdout原文：

```text
{"status": "COMPLETE", "reason": null, "completed_units": 10}
```

独立audit命令：

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 UV_OFFLINE=1 /usr/bin/time -l /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B notes/revision-v9/audit_wp3.py --output notes/revision-v9/wp3-independent-audit.json
```

其独立原始stdout/stderr（含实际time/RSS）：

```text
WARN `--no-project` was provided, but no project was found
{
  "status": "PASS",
  "audit_status": "PASS",
  "differences": [],
  "difference_count": 0,
  "mismatch_count": 0,
  "formal_study_status": "COMPLETE",
  "formal_study_reason": null,
  "scientific_WP3_complete": true,
  "saved_aggregate_outputs_present": true,
  "saved_curve_classifications_verified": 4,
  "legacy_hard_gate_status": "PASS",
  "independent_legacy_exact_difference_count": 0,
  "independent_legacy_exact_differences": [],
  "legacy_verification_boundaries": [
    {
      "horizon": 6,
      "method": "QR4",
      "scope": "old validation/floor/refit vectors absent; no archived comparison claim"
    },
    {
      "horizon": 24,
      "method": "QR4",
      "scope": "old validation/floor/refit vectors absent; no archived comparison claim"
    }
  ],
  "worker_gates": [
    {
      "horizon": 6,
      "window": 2880,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": [
        {
          "status": "PASS",
          "phase": "references",
          "method": "F",
          "horizon": 6,
          "legacy_public": "results/revision-20261022/references-fx_hourly-h6-w2880.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/references-fx_hourly-h6-w2880/private/numeric-traces.npz",
          "science_scalars_checked": 45,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "validation",
          "method": "QR33",
          "horizon": 6,
          "legacy_public": "results/revision-20261022/validation-fx_hourly-h6-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/validation-fx_hourly-h6-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 3647,
          "arrays_checked": 18,
          "values_checked": 25920,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "evaluation",
          "method": "QR33",
          "horizon": 6,
          "legacy_public": "results/revision-20261022/evaluation-fx_hourly-h6-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/evaluation-fx_hourly-h6-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 5590,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "method": "QR4",
          "horizon": 6,
          "science_scalars_checked": 1960,
          "arrays_checked": 4,
          "values_checked": 26500,
          "mismatches": 0,
          "scope": "old four evaluation vectors and public scalars; absent old validation/floor/refit vectors not claimed"
        }
      ]
    },
    {
      "horizon": 24,
      "window": 2880,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": [
        {
          "status": "PASS",
          "phase": "references",
          "method": "F",
          "horizon": 24,
          "legacy_public": "results/revision-20261022/references-fx_hourly-h24-w2880.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/references-fx_hourly-h24-w2880/private/numeric-traces.npz",
          "science_scalars_checked": 45,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "validation",
          "method": "QR33",
          "horizon": 24,
          "legacy_public": "results/revision-20261022/validation-fx_hourly-h24-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/validation-fx_hourly-h24-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 3647,
          "arrays_checked": 18,
          "values_checked": 25920,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "phase": "evaluation",
          "method": "QR33",
          "horizon": 24,
          "legacy_public": "results/revision-20261022/evaluation-fx_hourly-h24-w2880-QR.json",
          "legacy_private": ".scratch/revision-20261022/replication-revision-v3-b5-full/evaluation-fx_hourly-h24-w2880-QR/private/numeric-traces.npz",
          "science_scalars_checked": 5590,
          "arrays_checked": 6,
          "values_checked": 39750,
          "mismatches": 0
        },
        {
          "status": "PASS",
          "method": "QR4",
          "horizon": 24,
          "science_scalars_checked": 1960,
          "arrays_checked": 4,
          "values_checked": 26500,
          "mismatches": 0,
          "scope": "old four evaluation vectors and public scalars; absent old validation/floor/refit vectors not claimed"
        }
      ]
    },
    {
      "horizon": 6,
      "window": 360,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 24,
      "window": 360,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 6,
      "window": 720,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 24,
      "window": 720,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 6,
      "window": 1440,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 24,
      "window": 1440,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 6,
      "window": 5760,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    },
    {
      "horizon": 24,
      "window": 5760,
      "worker_status": "COMPLETE",
      "reason": null,
      "completed_baseline_checks": []
    }
  ],
  "complete_units": [
    [
      6,
      2880
    ],
    [
      24,
      2880
    ],
    [
      6,
      360
    ],
    [
      24,
      360
    ],
    [
      6,
      720
    ],
    [
      24,
      720
    ],
    [
      6,
      1440
    ],
    [
      24,
      1440
    ],
    [
      6,
      5760
    ],
    [
      24,
      5760
    ]
  ],
  "planned_units": 10,
  "planned_conditional_rows": 20,
  "actual_resource_worker_receipts": 10,
  "formal_resource_maximum": {
    "rss_bytes": 94420992,
    "os_threads": 1,
    "wall_seconds": 206.27386266598478
  },
  "scored_trace_blocks": 190,
  "checked_numeric_values": 2574900,
  "retained_method_reports": 30,
  "persisted_candidate_reports_verified": 80,
  "persisted_selection_reports_verified": 20,
  "before_gate_evaluation_reports_verified": 20,
  "HAC_pairs_recomputed": 20,
  "curve_classifications": [
    {
      "horizon": 6,
      "method": "QR33",
      "prediction_status": "FIRST_CUTPOINT_CONSISTENT"
    },
    {
      "horizon": 6,
      "method": "QR4",
      "prediction_status": "NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED"
    },
    {
      "horizon": 24,
      "method": "QR33",
      "prediction_status": "FIRST_CUTPOINT_CONSISTENT"
    },
    {
      "horizon": 24,
      "method": "QR4",
      "prediction_status": "FIRST_CUTPOINT_CONSISTENT"
    }
  ],
  "conditional_row_status_counts": {
    "COMPLETE": 20
  },
  "audit_elapsed_seconds": 1.2175136250443757,
  "audit_peak_rss_bytes": 64258048,
  "audit_maximum_observed_os_threads": 1,
  "audit_numerical_threads_configured": 1,
  "new_model_fits": 0,
  "new_forecasts_issued": 0,
  "production_aggregation_imported": false,
  "private_observations_disclosed": false
}
        1.41 real         1.15 user         0.11 sys
            64258048  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               26522  page reclaims
                 558  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   1  messages sent
                   1  messages received
                   1  signals received
                 707  voluntary context switches
                1137  involuntary context switches
           218592012  instructions retired
           100352244  cycles elapsed
            44237376  peak memory footprint
```

打包命令`python3 -B notes/revision-v9/package_wp3.py`只复制本轮scalar JSON/CSV/log与原始bytes，不含private NPZ或raw；tar206成员全部逐hash/内容核对，原文件未删除。原输出：

```json
{
  "actual_utc": "2026-10-24T23:36:47.665646+00:00",
  "status": "PASS",
  "source_members": 206,
  "uncompressed_bytes": 9903332,
  "archive_bytes": 1862483,
  "archive_sha256": "1ee2f4d848e209b882329f98f5ab0cbe21fe7251b4c9ba9854ac54e7d11b9fa0",
  "index_sha256": "d501493ce9fb8d95b1211c813079eb46e08b8be0e76462c560cf92e85c2ec2b0",
  "byte_mismatches": 0,
  "raw_financial_files_included": 0,
  "private_forecast_vectors_included": 0,
  "original_files_deleted": 0,
  "scope": "scalar formal output preservation and byte identity, not independent financial replication",
  "elapsed_seconds": 0.246355875,
  "peak_rss_bytes": 16056320
}
```

全套命令`python3 -B notes/revision-v9/run_full_pytest.py wp3-full-gate`默认完整discovery、不filter；所有indexed文件复制到新独立临时目录。全部原文保存在wp3-full-gate-pytest-output.txt，wrapper receipt与末尾原文如下：

```json
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--no-project",
    "--no-env-file",
    "--python",
    "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "--with",
    "pytest",
    "--with",
    "arch",
    "--with",
    "scikit-learn",
    "python",
    "-B",
    "-m",
    "pytest",
    "-p",
    "no:cacheprovider",
    "-v",
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp3-full-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp3-full-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked/indexed file copied; no test filter or skips added",
  "tracked_files_copied": 3434,
  "started_utc": "2026-10-24T23:36:53.823043+00:00",
  "ended_utc": "2026-10-24T23:38:44.875557+00:00",
  "elapsed_seconds": 111.052542083,
  "returncode": 0,
  "child_peak_rss_bytes": 355008512,
  "sampled_process_tree_peak_rss_bytes": 409878528,
  "stop_reason": null,
  "output_sha256": "f5e8986b9354b5c791360570a9e6d31fcb8d14bcb4540a9480d0622e0798fa7f",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
```

```text
test_verify_rank_ablation.py::IndependentReadbackTests::test_oracle_rejects_missing_history_duplicate_origins_and_incomplete_targets PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_saved_arrays_compare_every_issue_and_count_exact_disagreements PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1442 passed, 1068 subtests passed in 110.27s (0:01:50) ============
```

最终验收（命令`python3 -B -`断言设计bytes/10units/20contrasts/audit0diff/tar0diff/tests0及原归档无改）：

```json
{
  "wp": "WP3",
  "procedural_acceptance": "PASS",
  "actual_gate_utc": "2026-10-24T23:39:21.096007+00:00",
  "design_commit": "b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a",
  "design_before_new_forecasts": true,
  "formal_status": "COMPLETE",
  "completed_units": 10,
  "complete_conditional_contrasts": 20,
  "exact_W2880_both_horizons": "PASS",
  "ordinary_independent_difference_count": 0,
  "old_gate_exact_difference_count": 0,
  "prediction_classifications": [
    {
      "horizon": 6,
      "method": "QR33",
      "prediction_status": "FIRST_CUTPOINT_CONSISTENT",
      "first_crossing": 572.3369815680499,
      "prediction_range": [
        195.264769574666,
        774.9704967161092
      ]
    },
    {
      "horizon": 6,
      "method": "QR4",
      "prediction_status": "NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED",
      "first_crossing": null,
      "prediction_range": [
        92.90675766563821,
        749.7655536169423
      ]
    },
    {
      "horizon": 24,
      "method": "QR33",
      "prediction_status": "FIRST_CUTPOINT_CONSISTENT",
      "first_crossing": 2463.6419536695043,
      "prediction_range": [
        697.3741770523785,
        2767.7517739861046
      ]
    },
    {
      "horizon": 24,
      "method": "QR4",
      "prediction_status": "FIRST_CUTPOINT_CONSISTENT",
      "first_crossing": 1341.317712918093,
      "prediction_range": [
        331.8098488058507,
        2677.7341200605083
      ]
    }
  ],
  "all_four_numerical_confirmation": false,
  "formal_resources": {
    "rss_bytes": 94420992,
    "os_threads": 1,
    "wall_seconds": 206.27386266598478
  },
  "formal_total_wall_seconds": 629.7637939588167,
  "full_pytest": {
    "command": [
      "/Users/bingyouli/.local/bin/uv",
      "run",
      "--no-project",
      "--no-env-file",
      "--python",
      "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
      "--with",
      "pytest",
      "--with",
      "arch",
      "--with",
      "scikit-learn",
      "python",
      "-B",
      "-m",
      "pytest",
      "-p",
      "no:cacheprovider",
      "-v",
      "--basetemp",
      "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp3-full-gate/pytest-temp"
    ],
    "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp3-full-gate/full-suite-copy",
    "scope": "Full default discovery; every tracked/indexed file copied; no test filter or skips added",
    "tracked_files_copied": 3434,
    "started_utc": "2026-10-24T23:36:53.823043+00:00",
    "ended_utc": "2026-10-24T23:38:44.875557+00:00",
    "elapsed_seconds": 111.052542083,
    "returncode": 0,
    "child_peak_rss_bytes": 355008512,
    "sampled_process_tree_peak_rss_bytes": 409878528,
    "stop_reason": null,
    "output_sha256": "f5e8986b9354b5c791360570a9e6d31fcb8d14bcb4540a9480d0622e0798fa7f",
    "numerical_threads": 1,
    "UV_OFFLINE": true
  },
  "full_pytest_summary": "============ 1442 passed, 1068 subtests passed in 110.27s (0:01:50) ============",
  "targeted_output": "....................................................                     [100%]\n52 passed in 0.27s\n",
  "package": {
    "actual_utc": "2026-10-24T23:36:47.665646+00:00",
    "status": "PASS",
    "source_members": 206,
    "uncompressed_bytes": 9903332,
    "archive_bytes": 1862483,
    "archive_sha256": "1ee2f4d848e209b882329f98f5ab0cbe21fe7251b4c9ba9854ac54e7d11b9fa0",
    "index_sha256": "d501493ce9fb8d95b1211c813079eb46e08b8be0e76462c560cf92e85c2ec2b0",
    "byte_mismatches": 0,
    "raw_financial_files_included": 0,
    "private_forecast_vectors_included": 0,
    "original_files_deleted": 0,
    "scope": "scalar formal output preservation and byte identity, not independent financial replication",
    "elapsed_seconds": 0.246355875,
    "peak_rss_bytes": 16056320
  },
  "failure_container_inventory": {
    "actual_utc": "2026-10-24T23:36:14.050398+00:00",
    "candidate_status_counts": {
      "COMPLETE": 80
    },
    "failed_candidates": [],
    "auxiliary_key_list_occurrences": [],
    "sealed_driver_unchanged": true,
    "scope": "QA of retained failure records; no model/selection change or new experiment"
  },
  "old_scientific_archive_or_code_changes": "",
  "no_raw_financial_data_published": true,
  "no_other_WP_started": true,
  "scope": "Procedural PASS does not mean all predictions SUPPORT; c excludes p, long-W reversals/left censoring preserved; no independent dealer/new holdout/oracle/cost identification"
}
```

这一步的PASS是执行验收：四条全确认条件未满足。QR4/H6 left-censored是NOT_TESTABLE，不换成后来的conditional root；H24两方法在最长W都回正，不能说越长越好。c不含p，WP2 P3仍NOT_SUPPORT，没有oracle且菜单不同，未识别纯估计成本机制。旧QR4缺失的历史向量边界、普通DM名义/事后/共享训练依赖、当前旧期间重复研究均保留。aux失败容器静态缺陷本次发生0次，sealed code从未运行中改写。WP4只有本步commit实际产生后才能进入。

## WP4 PASS — 全来源统一图与逐点追溯

前项实际结束提交bfd0493f4237b6b99ca4370a2e6cf2195f653b28后才开始。先写display contract，图只读取既有四个保存结果JSON；selected c不含p，原纵值不重算、不平均、不舍入、不jitter/合并同x。将原v8 QR33主热图完整移入Supplement并保留原PDF文件字节；主图仍4张。新主图已改准引用和图注，不再谎称scatter含MCSE annotations。Supplement最终页数仍待后续正式编译验收。

来源census校正MISMATCH：WP2 summary144行含48 F自比，所以conditional点只有96；实际总380，非428。8对旧FX与curve同期间重叠仍分别显示，不能冒称新增独立样本；原两种等价损失算术的末位差不手改。每点sourcehash/JSONindex、图上实际760offset(重复detail显示，不是760独立点)均独立核对。

最终绘图命令（既有cached matplotlib，无安装，7线程环境1，UV_OFFLINE1）：

```sh
/usr/bin/time -l /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with matplotlib python -B plot_v9_unified.py --output results/revision-v9/wp4/render-v5
```

完整原stdout/stderr：

```text
WARN `--no-project` was provided, but no project was found
{
  "status": "GENERATED_PENDING_INDEPENDENT_READBACK_VISUAL_QA",
  "actual_utc": "2026-10-24T23:46:39.218742+00:00",
  "metric": "c=W/(H+1)",
  "x_scale": "log",
  "parameter_count_in_metric": false,
  "source_bindings": [
    {
      "path": "results/revision-v9/wp1/simulation-cells.json",
      "sha256": "1186c50c4033332a58718f680ad00a5d7a47fb67c4c5c3e1bb9210be8a4de5a3",
      "bytes": 296855,
      "source_rows": 144
    },
    {
      "path": "results/revision-v9/wp2/summary.json",
      "sha256": "ab77dade64a67751f8e93b1bb18bc9a491c22a6efb2b5292840748e8a6b636bc",
      "bytes": 137693,
      "source_rows": 144
    },
    {
      "path": "results/revision-v9/wp1/empirical-overlay.json",
      "sha256": "c3c94df846cd8888c4d6fe8c0863dd1e5787894901d9aa3bc1b87064b6edf647",
      "bytes": 66901,
      "source_rows": 120
    },
    {
      "path": "results/revision-v9/wp3/contrasts.json",
      "sha256": "576e9070644e211d417f84efba6a8b77b295be8e1f5870a5ec42aed7d7362ce4",
      "bytes": 12569,
      "source_rows": 20
    }
  ],
  "point_count": 380,
  "family_counts": {
    "v8_sim": 144,
    "v9_sim": 96,
    "empirical": 120,
    "curve": 20
  },
  "method_counts": {
    "QR33": 190,
    "QR4": 190
  },
  "source_counts": {
    "v8_AR_GARCH": 144,
    "student_t5": 32,
    "regime_3to1": 32,
    "compound_poisson": 32,
    "fx_hourly": 28,
    "nyfed_weekly": 8,
    "fx_daily": 8,
    "panel:PDPOSMBS-TOT": 8,
    "panel:PDPOSCS-TOT": 8,
    "panel:PDPOSFGS-TOT": 8,
    "panel:PDPOSTIPS-L2": 8,
    "panel:PDPOSTIPS-G11": 8,
    "panel:PDPOSTIPS-G2": 8,
    "panel:PDPOSTIPS-G6L11": 8,
    "panel:PDPOSGSC-L2": 8,
    "panel:PDPOSGSC-G2L3": 8,
    "panel:PDPOSGSC-G3L6": 8,
    "panel:PDPOSGSC-G6L7": 8,
    "panel:PDPOSGSC-G7L11": 8
  },
  "excluded_F_reference_self_rows": 48,
  "overlapping_old_FX_curve_records": 8,
  "deduplicated_records": 0,
  "jittered_records": 0,
  "rounded_ordinates": 0,
  "band_source": "results/revision-v9/wp1/breakeven.json",
  "band_source_sha256": "bda0e60a195c364ee39738ccadbb20c227990a1d9711230d77969528abae0b98",
  "bands": {
    "QR33": {
      "lower": 27.894967082095143,
      "upper": 110.71007095944418,
      "upper_unbounded": false,
      "coverage_guarantee": false
    },
    "QR4": {
      "lower": 13.27239395223403,
      "upper": 107.10936480242033,
      "upper_unbounded": false,
      "coverage_guarantee": false
    }
  },
  "elapsed_seconds": 0.7428919579833746,
  "peak_rss_bytes": 115867648,
  "new_model_fits": 0,
  "new_predictions": 0,
  "observed_os_thread_samples": [
    1,
    1
  ],
  "maximum_observed_os_threads": 1,
  "requested_numerical_threads": 1
}
        0.82 real         0.76 user         0.06 sys
           115867648  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               16682  page reclaims
                   2  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   1  messages sent
                   1  messages received
                   1  signals received
                   6  voluntary context switches
                 217  involuntary context switches
           181815895  instructions retired
            82932715  cycles elapsed
            38519336  peak memory footprint
```

初次独立QA失败原输出保留（validator误解same_period_key的范围；修validator metadata规则加回归测试，未改图/值/科学规则）：

```text
WARN `--no-project` was provided, but no project was found
Traceback (most recent call last):
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v9/audit_wp4.py", line 172, in <module>
    if __name__=="__main__":main()
                            ^^^^^^
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v9/audit_wp4.py", line 114, in main
    require(p["same_period_key"]==expected_period_key,"same-period financial lineage key")
  File "/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v9/audit_wp4.py", line 26, in require
    if not condition:raise AuditMismatch(label)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
AuditMismatch: same-period financial lineage key
        0.06 real         0.04 user         0.02 sys
            61964288  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                6059  page reclaims
                   0  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   1  messages sent
                   1  messages received
                   1  signals received
                   3  voluntary context switches
                 224  involuntary context switches
           199782424  instructions retired
            91111627  cycles elapsed
            43074136  peak memory footprint
```

最终独立核对命令（同一线程/offline env）：

```sh
/usr/bin/time -l uv run --offline --no-project --no-env-file --python <existing bundled Python> --with pytest --with arch --with scikit-learn python -B notes/revision-v9/audit_wp4.py --render results/revision-v9/wp4/render-v5 --output notes/revision-v9/wp4-independent-audit.json
```

最终原输出：

```text
WARN `--no-project` was provided, but no project was found
{
  "status": "PASS",
  "differences": [],
  "difference_count": 0,
  "mismatch_count": 0,
  "render_directory": "results/revision-v9/wp4/render-v5",
  "point_count": 380,
  "family_counts": {
    "v8_sim": 144,
    "v9_sim": 96,
    "empirical": 120,
    "curve": 20
  },
  "method_counts": {
    "QR33": 190,
    "QR4": 190
  },
  "excluded_F_self_reference_rows": 48,
  "retained_same_period_overlap_pairs": 8,
  "panels": [
    {
      "panel": "QR33_all",
      "method": "QR33",
      "full_range": true,
      "point_count": 190,
      "visible_point_count": 190,
      "detail_outside_view_count": 0,
      "artist_count": 8,
      "scatter_artists": 6,
      "line_artists": 2,
      "artist_offsets_verified": 190
    },
    {
      "panel": "QR33_detail",
      "method": "QR33",
      "full_range": false,
      "point_count": 190,
      "visible_point_count": 112,
      "detail_outside_view_count": 78,
      "artist_count": 8,
      "scatter_artists": 6,
      "line_artists": 2,
      "artist_offsets_verified": 190
    },
    {
      "panel": "QR4_all",
      "method": "QR4",
      "full_range": true,
      "point_count": 190,
      "visible_point_count": 190,
      "detail_outside_view_count": 0,
      "artist_count": 8,
      "scatter_artists": 6,
      "line_artists": 2,
      "artist_offsets_verified": 190
    },
    {
      "panel": "QR4_detail",
      "method": "QR4",
      "full_range": false,
      "point_count": 190,
      "visible_point_count": 169,
      "detail_outside_view_count": 21,
      "artist_count": 8,
      "scatter_artists": 6,
      "line_artists": 2,
      "artist_offsets_verified": 190
    }
  ],
  "actual_artist_count": 32,
  "actual_artist_offsets_verified": 760,
  "all_unique_points_visible_in_full_range": true,
  "no_outlier_dropped": true,
  "detail_views_explicit": true,
  "all_draw_band_parameters_verified": true,
  "source_row_mapping_verified": 380,
  "CSV_JSON_fields_verified": 380,
  "prior_render_metadata_identity": {
    "render-v2": "points JSON/CSV byte-identical; originals retained",
    "render-v3": "points JSON/CSV byte-identical; originals retained",
    "render-v4": "points JSON/CSV byte-identical; originals retained"
  },
  "PNG_dimensions": [
    1584,
    1536
  ],
  "output_sha256": {
    "points.json": "c04932d44d0485008c5f8c3b314c6ea1e77f7e52f5b0cf8b026deb80180ac1ed",
    "points.csv": "8126745c395622513b69888b4b8587ba9b22855b9e52c91f41aff736ce16140a",
    "excluded-reference-rows.json": "f58ce0d7b38ddbc09059fe9f09647a000e61528a0c6b6ad8ff8821361fa95afb",
    "unified-history.pdf": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
    "unified-history.png": "44e6d208c9f1335521a2aac0cdd5fe6ffb6a0b1aafa3a7015f5a78fe3f78603f"
  },
  "audit_elapsed_seconds": 0.01822120905853808,
  "audit_peak_rss_bytes": 29458432,
  "audit_observed_os_threads": 1,
  "model_fits_run": 0,
  "new_statistics_fit": 0,
  "production_plotter_imported": false,
  "verification_boundary": "stored Matplotlib offsets/markers/axis limits and band parameters verified; pixel appearance and legend readability are separate visual QA"
}
        0.07 real         0.04 user         0.02 sys
            67239936  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                7632  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   1  messages sent
                   1  messages received
                   1  signals received
                   3  voluntary context switches
                 233  involuntary context switches
           202674201  instructions retired
            91362336  cycles elapsed
            48284248  peak memory footprint
```

构造破坏测试实际命令和原文：

```text
Actual command (previously executed; not rerun for this record):
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 UV_OFFLINE=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B -m pytest -q -p no:cacheprovider test_v9_wp4_audit.py

Actual stdout:
WARN `--no-project` was provided, but no project was found
....................                                                     [100%]
20 passed in 0.05s
```

实际PDF raster命令`pdftoppm -f 1 -singlefile -r 160 -png results/revision-v9/wp4/render-v5/unified-history.pdf .scratch/revision-v9/wp4-pdf-render/unified-history-v5`退出0，无stdout/stderr；主线程直接看PNG及该PDF raster，最终无标题/图例/轴/footer重叠。此前失败布局render均保留，所有render数值坐标相同。验收输出：

```json
{
  "wp": "WP4",
  "procedural_acceptance": "PASS",
  "actual_gate_utc": "2026-10-24T23:49:08.598505+00:00",
  "prior_WP_end_commit": "bfd0493f4237b6b99ca4370a2e6cf2195f653b28",
  "selected_render": "results/revision-v9/wp4/render-v5",
  "points": 380,
  "family_counts": {
    "v8_sim": 144,
    "v9_sim": 96,
    "empirical": 120,
    "curve": 20
  },
  "same_period_overlap_pairs": 8,
  "excluded_reference_self_rows": 48,
  "source_mapping_count": 380,
  "actual_artists": 32,
  "actual_offsets": 760,
  "offsets_not_independent_observations": true,
  "independent_mismatch_count": 0,
  "full_range_all_points_visible": true,
  "all_draw_bands_verified": true,
  "main_figures": 4,
  "old_heatmap_preserved_in_supplement": true,
  "visual_QA": "notes/revision-v9/wp4-visual-QA.json",
  "construct_tests_raw_output": "Actual command (previously executed; not rerun for this record):\nenv OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 UV_OFFLINE=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B -m pytest -q -p no:cacheprovider test_v9_wp4_audit.py\n\nActual stdout:\nWARN `--no-project` was provided, but no project was found\n....................                                                     [100%]\n20 passed in 0.05s\n",
  "old_scientific_archive_or_code_changes": "",
  "supplement_final_page_budget": "pending WP5/WP7 compilation; no page PASS claimed here",
  "semantic_limit": "partial nonmonotone history-to-horizon pattern; c excludes p; no universal threshold, parameter-cost identification or new financial holdout",
  "model_fits_added": 0,
  "new_inferential_statistics": 0,
  "known_QA_failures_preserved": [
    "initial rendering legend collision",
    "v3 title collision",
    "first independent validator misread overlap-only key; regression test corrected; no science changed"
  ]
}
```

WP5必须在本步实际commit后才开始；不能把图的形状写成阈值定理，也不能将左删失、长期反转或P3失败写掉。

## WP5 PASS — partly supported主线与原有科学数值保护

WP4实际结束提交32ee58688bac260de322c31cb8945adbf3b53154后才进入。以数据选择partly-supported写法，不使用估计成本已识别、effective sample per parameter或永久阈值。采用问句标题When Is History Long Enough?；成本副标题未采用。完整前后对照在wp5-argument-before-after.md，后续两项引用归属/原坐标插值和P3不软化改写另有逐字记录。

运行 `python3 -B notes/revision-v9/build_wp5_main.py` 后，脚本保留6主表原数字vector、4旧display math与所有作者占位字段，新增数字从原JSON直接格式化。旧1205source/locators审核不改，在其外加精确source+SHA+JSONpointer+全文唯一位置绑定，绝非裸数字全局membership。原test_v8_main_numbers.py只改checker入口到additive wrapper，所有原negative mutation与assertions保持；旧guard及原proof文件字节未改。

完整旧+新负控制和compiler解析负控制命令：

```sh
UV_OFFLINE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --offline --no-project --no-env-file --python <existing bundled Python> --with pytest --with arch --with scikit-learn python -B -m pytest -q -p no:cacheprovider test_v8_main_numbers.py test_v9_main_numbers.py test_v9_compile_diagnostics.py
```

原始输出：

```text
WARN `--no-project` was provided, but no project was found
...................................                                      [100%]
35 passed in 3.55s
```

制表命令 `python3 -B notes/revision-v9/build_wp5_tables.py --check`，43表行/228数值绑定，包含20完整financial格和全部6个P3失败不等式，原输出：

```text
{"bindings": 228, "bindings_bytes": 153150, "bindings_sha256": "d44d50546e6c1d649ba5ad98dfd7938534a059d6c4c0db26639ae280c5efdc94", "main_or_supplement_modified": false, "mode": "readback", "namedfacts": 107, "new_statistics_run": 0, "status": "PASS", "table_row_counts": {"confirmation_failures": 6, "confirmation_pooled": 3, "confirmation_subgroups": 5, "discovery_cutpoints": 2, "discovery_scores": 3, "financial_cutpoints": 4, "financial_full": 20}, "tex_bytes": 9600, "tex_sha256": "cebcfac6e48f6eaaffdc67c1f2eedce46baf9ca0606a1a3292ddea2eea68f0b6"}
```

为守30页上限，将两份完整preferencefrontier与数值conventions原文逐字符复制至extended-v9-technical.tex/PDF，Supplement及EXTENDED_RESULTS显式链接。所有相关原结果/数字/失败均保留，精确移位hash证明在wp5-supplement-relocation.json。既有Tectonic --only-cached编译3文档均退出0；首次diagnostic regex将infwarerr包metadata的error一词误当错误，原receipt保留，实际log扫描0错误/undefined/overfull。修parser并用正/负控制，不靠删日志；PDF当次未因此重算。新增编译实际原输出见wp5-compile-summary-console.txt及wp5-gate-compile-summary.txt，最终主文原输出如下：

```text
{
  "command": [
    "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
    "-X",
    "compile",
    "--only-cached",
    "submission-jof/manuscript.tex",
    "--outdir",
    ".scratch/revision-v9/wp5-gate/manuscript",
    "--keep-logs",
    "--keep-intermediates"
  ],
  "started_utc": "2026-10-25T00:20:08.931319+00:00",
  "ended_utc": "2026-10-25T00:20:09.493026+00:00",
  "elapsed_seconds": 0.560684792,
  "returncode": 0,
  "source": "submission-jof/manuscript.tex",
  "source_sha256": "998e530b2960b463ec47def4dc2170057c30cd9137b825ee1991f5ba00d72ca5",
  "source_unchanged": true,
  "pdf_path": ".scratch/revision-v9/wp5-gate/manuscript/manuscript.pdf",
  "pdf_sha256": "5a66e5aa1b5053b42e075f6082091399ec247b3cd6ba29119ef46e32f8dfd80c",
  "error_undefined_missing_glyph_overfull_lines": [],
  "child_peak_rss_bytes": 249626624,
  "resource_scope": "cumulative maximum child RSS of this sequential compiler wrapper",
  "only_cached": true,
  "numerical_thread_environment": 1,
  "packages_installed": 0
}
```

当前正文完整数值核对命令 `python3 -B notes/revision-v9/check_main_numbers.py --output notes/revision-v9/wp5-main-number-audit-gate.json`，原输出(完整inventory另在JSON)：

```text
{
  "schema": "v9-additive-current-main-number-audit-1",
  "status": "PASS",
  "checked_utc": "2026-10-25T00:20:09.885699+00:00",
  "scope": "Current main and cover-letter located numeric occurrence/word audit; source lookup/display preservation only. Figure values, reference metadata and PDF positioning have separate owning gates.",
  "current_main_sha256": "998e530b2960b463ec47def4dc2170057c30cd9137b825ee1991f5ba00d72ca5",
  "current_cover_letter_sha256": "3c7c88356d3bf4feaf8854eaddbacdcbe22951bd80008075cc1509f7f2b05b7f",
  "original_evidence_fields_checked": 1205,
  "original_main_saved_bindings_checked": 117,
  "original_table_preservation_commit": "642d6af",
  "original_table_vectors_checked": 6,
  "original_table_vector_mismatches": [],
  "labelled_table_rows_checked": 31,
  "labelled_table_numeric_tokens_checked": 80,
  "original_display_math_blocks_checked": 4,
  "accepted_exact_math_fragments_checked": 26,
  "total_numeric_occurrences": 582,
  "main_numeric_occurrences": 582,
  "cover_letter_numeric_occurrences": 0,
  "category_counts": {
    "figure_axis_or_layout": 53,
    "current_located_source_binding": 34,
    "existing_binding": 106,
    "source_file_or_model_label": 2,
    "mathematical_definition_or_structure": 20,
    "contribution_counter": 2,
    "reference_or_source_identifier": 29,
    "reference_or_crossref_identifier": 9,
    "reference_metadata": 314,
    "v9_located_source_binding": 11,
    "figure_path_or_display_parameter": 2
  },
  "unclassified_numeric_occurrences": 0,
  "ambiguous_numeric_locations": 0,
  "meaningful_number_word_occurrences": 32,
  "unbound_number_word_occurrences": 0,
  "old_and_new_percentage_fields_checked": 20,
  "failures": [],
  "mismatches": 0,
  "figure_paths": [
    {
      "path": "submission-jof/figures/v7-endpoint-peak-example.pdf",
      "current_sha256": "8a64f721028b931b5cd5a9031ad28a197ea5fc3b3338d3dd6bf13216e5e33d1f",
      "expected_receipt_sha256": "8a64f721028b931b5cd5a9031ad28a197ea5fc3b3338d3dd6bf13216e5e33d1f",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v7-murphy-fx_hourly.pdf",
      "current_sha256": "43e0c421140d91120eefac427f243b5775ebd43bfec579392b6d0e61ce199aa1",
      "expected_receipt_sha256": "43e0c421140d91120eefac427f243b5775ebd43bfec579392b6d0e61ce199aa1",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v7-murphy-nyfed_weekly.pdf",
      "current_sha256": "3bdb6d07d8f516ea8930c1f40a1c4396114369770bb66e74351260d236e8cd48",
      "expected_receipt_sha256": "3bdb6d07d8f516ea8930c1f40a1c4396114369770bb66e74351260d236e8cd48",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v9-unified-history.pdf",
      "current_sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "expected_receipt_sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "copy_identity_verified": true,
      "values_verified_here": false,
      "v9_identity_evidence": {
        "path": "submission-jof/figures/v9-unified-history.pdf",
        "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
        "receipt_paths": {
          "placement": "notes/revision-v9/wp4-final-placement-v5.json",
          "point_audit": "notes/revision-v9/wp4-independent-audit.json",
          "visual_receipt": "notes/revision-v9/wp4-visual-QA.json"
        },
        "values_verified_here": false,
        "visual_review_performed_here": false
      }
    }
  ],
  "figure_values_verified_here": false,
  "reference_metadata_verified_here": false,
  "reference_metadata_occurrences": 352,
  "full_artifact_numeric_acceptance": false,
  "required_separate_gates": [
    "Actual included figure value/annotation audit",
    "Current reference metadata audit",
    "Current source-to-PDF identity and every-page visual QA",
    "Supplement numeric audit"
  ],
  "new_financial_computations": 0,
  "models_refitted": 0,
  "new_hypothesis_tests": 0,
  "private_arrays_read": false,
  "legacy_status": "FAIL",
  "v9_resolved_numeric_occurrences": 11,
  "v9_resolved_number_words": 1,
  "v9_verified_figure_identities": [
    {
      "path": "submission-jof/figures/v9-unified-history.pdf",
      "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "receipt_paths": {
        "placement": "notes/revision-v9/wp4-final-placement-v5.json",
        "point_audit": "notes/revision-v9/wp4-independent-audit.json",
        "visual_receipt": "notes/revision-v9/wp4-visual-QA.json"
      },
      "values_verified_here": false,
      "visual_review_performed_here": false
    }
  ],
  "legacy_checker_path": "notes/revision-v8/check_wp8_main_numbers.py",
  "legacy_checker_sha256": "a2fa6f10a085dfda25fd73faf8eec814b77f290fd167e863f16e5a2b437688c1",
  "v9_bindings_sha256": "6231ab33464c0b8ccd4b0f360d2d07e6c9ed1d4ed4af8ace4d42cf4380621f46"
}
```

S6实际before/after（同一scope，未藏数字于macro；table与transparency仅按v7原授权排除，figurecaption/inlineMath/citationyear仍计数）：

| Measure | Before v8 | Current |
|---|---:|---:|
| abstract_words | 164 | 149 |
| abstract_numbers | 4 | 2 |
| main_words | 4646 | 5408 |
| main_sentences | 244 | 276 |
| mean_sentence_words | 19.040983606557376 | 19.594202898550726 |
| over35_percent | 0.0 | 0.0 |
| negation_percent | 4.508196721311475 | 4.3478260869565215 |
| max_numbers_per_sentence | 2 | 2 |
| all_v8_writing_gates_pass | True | True |

全部banned counts0、paragraph>6为0；作者占位不填。摘要与引言首段原文按要求如下：

### Before abstract

Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the previously reported later and earlier windows. Its later advantage survives a delayed adaptive coverage adjustment (ACI). Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series. A controlled simulation rejects a universal narrow-regime explanation, while aggregation and the overlapping backcast further qualify the empirical pattern.

### After abstract

Peak-position limits concern the largest absolute inventory reached before a review ends, making completed path labels and the observed current position central to forecasting. We compare historical and conditional quantile reports for an FX market maker and weekly primary-dealer position aggregates, using matched histories and update schedules. Simple historical rules remain demanding benchmarks across frequencies, position categories and reference choices. At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the previously reported later and earlier windows. A post hoc history-to-horizon coordinate organizes simulation gains, and a new simulation passes its short-history and long-history prediction screens. Real-record learning curves partly support the predicted first cutpoints, while left censoring, large-history reversals and failures of universal simplification qualify that pattern. For limit managers, these findings motivate matching historical information before assessing conditional forecasts jointly on score, breaches and stability, with history length guiding evaluation.

### Before Introduction opening

A dealer's recorded net position can finish inside its limit after exceeding it earlier in the monitoring period, as Figure~\ref{fig:example} illustrates. The forecasting question concerns the largest sampled exposure before the next review, rather than the endpoint alone. This changes the response and when its training label becomes available. We ask whether additional conditioning improves that peak forecast once historical information is matched, and whether the gain survives alternative references and breach assessment.

### After Introduction opening

An inventory limit can look adequate at the horizon endpoint even when a dealer's position has crossed it earlier in the review period. Figure~\ref{fig:example} shows why the relevant forecast is a sampled path maximum rather than an endpoint interval. The challenge is to learn that peak from completed historical labels while preserving the information available when the position is observed. We ask when additional conditioning improves on historical headroom forecasts that use the same training history, and how longer histories alter that comparison.

实际分节字数与PDF页数及本步验收输出（全页视觉/最终package/发布不在此冒称）：

```json
{
  "sections": [
    {
      "section": "Introduction",
      "words": 893,
      "cap": 1300,
      "PASS": true
    },
    {
      "section": "Related literature",
      "words": 329,
      "cap": 900,
      "PASS": true
    },
    {
      "section": "The forecast target",
      "words": 539,
      "cap": 1000,
      "PASS": true
    },
    {
      "section": "Data",
      "words": 307,
      "cap": 600,
      "PASS": true
    },
    {
      "section": "Forecasting methods",
      "words": 425,
      "cap": 800,
      "PASS": true
    },
    {
      "section": "Evaluation design",
      "words": 641,
      "cap": 800,
      "PASS": true
    },
    {
      "section": "Results",
      "words": 1657,
      "cap": 2000,
      "PASS": true
    },
    {
      "section": "Implications for model validation",
      "words": 317,
      "cap": 500,
      "PASS": true
    },
    {
      "section": "Limitations",
      "words": 387,
      "cap": 500,
      "PASS": true
    },
    {
      "section": "Conclusion",
      "words": 284,
      "cap": 350,
      "PASS": true
    }
  ],
  "budget_words": 5928,
  "acceptance": {
    "wp": "WP5",
    "procedural_acceptance": "PASS",
    "actual_gate_utc": "2026-10-25T00:22:03.269578+00:00",
    "prior_WP_end_commit": "32ee58688bac260de322c31cb8945adbf3b53154",
    "writing_branch": "partly supported",
    "new_title": "When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits",
    "all_four_financial_confirmation": false,
    "pure_estimation_cost_identified": false,
    "parameter_count_in_selected_coordinate": false,
    "before_after_and_abstract_intro_source": "notes/revision-v9/wp5-argument-before-after.md",
    "followthrough": [
      "notes/revision-v9/wp5-citation-interpolation-followthrough.json",
      "notes/revision-v9/wp5-negative-wording-followthrough.json",
      "notes/revision-v9/wp5-results-takeaway.json"
    ],
    "metrics_source": "notes/revision-v9/wp5-gate-writing-before-after.json",
    "style_PASS": true,
    "section_budgets_PASS": true,
    "main_figures": 4,
    "main_tables": 6,
    "PDFs": {
      "manuscript": {
        "pages": 21,
        "sha256": "5a66e5aa1b5053b42e075f6082091399ec247b3cd6ba29119ef46e32f8dfd80c"
      },
      "supplement": {
        "pages": 30,
        "sha256": "8d2023aa9f31fad66823f679cff39f8e4996e001c0ddb1e0d9fa2fedb18d111a"
      },
      "extended-v9-technical": {
        "pages": 6,
        "sha256": "7f6655dc74aa8d80104908e164fc64116a003e1701a9f22b90625759835da646"
      }
    },
    "numeric_audit_status": "PASS",
    "numeric_occurrences": 582,
    "unclassified_digits": 0,
    "unbound_number_words": 0,
    "original_source_fields_checked": 1205,
    "original_table_vectors_checked": 6,
    "new_table_numeric_bindings": 228,
    "old_scientific_values_changed": 0,
    "original_author_placeholders_changed": false,
    "actual_compiler_diagnostics": [],
    "negative_controls_output": "WARN `--no-project` was provided, but no project was found\n...................................                                      [100%]\n35 passed in 3.55s\n",
    "selected_page_QA": "PASS(main15,supp27\u201329); final allpage QA remains WP7",
    "old_full_frontiers_and_numerics": "verbatim linked extended technical PDF with relocation proof, not omitted outcomes",
    "scientific_new_analysis_since_WP3": 0,
    "pending_later_WPs": [
      "WP6 role review",
      "WP7 full tests, allpage QA, all deliverable aliases/package, remote publication"
    ],
    "illustrative_plan_MISMATCH": "13weeklycells already above smaller-model pointcutpoint; all-weekly-below claim is false and not used"
  }
}
```

另有MISMATCH：指令示例的所有weekly都低于pointcutpoint与既有WP1记录不符，13个weekly格超过小模型point值，正文如实写周频迁移局限。新学习曲线综述背景只支持非单调性已有文献，不提供本案估计成本识别或新颖性证明。资料阅读scope/DOI/版本见wp5-claim-and-learning-source.md。WP6仅在本步实际commit后进入。


## WP6 PASS — two internal mechanism reviewers and bounded responses

Actual acceptance: 2026-10-25T00:32:44.798646+00:00. Prior actual end commit `d44364c6aa5ca5a9a043f33b9173f0864b771159`. Same-model reviewers, seven issues each; no Claude, no new model/statistic/data. Review opinions and 14 responses: `notes/revision-v9/wp6-{econometric-review,risk-manager-review,response-matrix}.md`. Missing channel identification, independent dealers, selection-adjusted inference and operating/live policy remain gaps, not newly certified outcomes.

Commands and raw output:

```text
python3 -B notes/revision-v9/build_wp5_tables.py --check
{"bindings": 228, "bindings_bytes": 153150, "bindings_sha256": "c1cbe64a3b4da7c20d08f187f1918205f955ef89651b2d0fc2044ac874a75870", "main_or_supplement_modified": false, "mode": "readback", "namedfacts": 107, "new_statistics_run": 0, "status": "PASS", "table_row_counts": {"confirmation_failures": 6, "confirmation_pooled": 3, "confirmation_subgroups": 5, "discovery_cutpoints": 2, "discovery_scores": 3, "financial_cutpoints": 4, "financial_full": 20}, "tex_bytes": 9618, "tex_sha256": "23142a3fd01175b62cf4f0999a2a76c158f4ae7ec8f78a85df874f4ddf4d4927"}

python3 -B notes/revision-v9/check_main_numbers.py --output notes/revision-v9/wp5-main-wp6-final-audit.json
{
  "schema": "v9-additive-current-main-number-audit-1",
  "status": "PASS",
  "checked_utc": "2026-10-25T00:32:18.944149+00:00",
  "scope": "Current main and cover-letter located numeric occurrence/word audit; source lookup/display preservation only. Figure values, reference metadata and PDF positioning have separate owning gates.",
  "current_main_sha256": "2cbf38039b2b0d254ca88e3ad18badd6020907838ec5f2d31fe5d08799c8763f",
  "current_cover_letter_sha256": "3c7c88356d3bf4feaf8854eaddbacdcbe22951bd80008075cc1509f7f2b05b7f",
  "original_evidence_fields_checked": 1205,
  "original_main_saved_bindings_checked": 117,
  "original_table_preservation_commit": "642d6af",
  "original_table_vectors_checked": 6,
  "original_table_vector_mismatches": [],
  "labelled_table_rows_checked": 31,
  "labelled_table_numeric_tokens_checked": 80,
  "original_display_math_blocks_checked": 4,
  "accepted_exact_math_fragments_checked": 26,
  "total_numeric_occurrences": 582,
  "main_numeric_occurrences": 582,
  "cover_letter_numeric_occurrences": 0,
  "category_counts": {
    "figure_axis_or_layout": 53,
    "current_located_source_binding": 34,
    "existing_binding": 106,
    "source_file_or_model_label": 2,
    "mathematical_definition_or_structure": 20,
    "contribution_counter": 2,
    "reference_or_source_identifier": 29,
    "reference_or_crossref_identifier": 9,
    "reference_metadata": 314,
    "v9_located_source_binding": 11,
    "figure_path_or_display_parameter": 2
  },
  "unclassified_numeric_occurrences": 0,
  "ambiguous_numeric_locations": 0,
  "meaningful_number_word_occurrences": 32,
  "unbound_number_word_occurrences": 0,
  "old_and_new_percentage_fields_checked": 20,
  "failures": [],
  "mismatches": 0,
  "figure_paths": [
    {
      "path": "submission-jof/figures/v7-endpoint-peak-example.pdf",
      "current_sha256": "8a64f721028b931b5cd5a9031ad28a197ea5fc3b3338d3dd6bf13216e5e33d1f",
      "expected_receipt_sha256": "8a64f721028b931b5cd5a9031ad28a197ea5fc3b3338d3dd6bf13216e5e33d1f",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v7-murphy-fx_hourly.pdf",
      "current_sha256": "43e0c421140d91120eefac427f243b5775ebd43bfec579392b6d0e61ce199aa1",
      "expected_receipt_sha256": "43e0c421140d91120eefac427f243b5775ebd43bfec579392b6d0e61ce199aa1",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v7-murphy-nyfed_weekly.pdf",
      "current_sha256": "3bdb6d07d8f516ea8930c1f40a1c4396114369770bb66e74351260d236e8cd48",
      "expected_receipt_sha256": "3bdb6d07d8f516ea8930c1f40a1c4396114369770bb66e74351260d236e8cd48",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v9-unified-history.pdf",
      "current_sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "expected_receipt_sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "copy_identity_verified": true,
      "values_verified_here": false,
      "v9_identity_evidence": {
        "path": "submission-jof/figures/v9-unified-history.pdf",
        "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
        "receipt_paths": {
          "placement": "notes/revision-v9/wp4-final-placement-v5.json",
          "point_audit": "notes/revision-v9/wp4-independent-audit.json",
          "visual_receipt": "notes/revision-v9/wp4-visual-QA.json"
        },
        "values_verified_here": false,
        "visual_review_performed_here": false
      }
    }
  ],
  "figure_values_verified_here": false,
  "reference_metadata_verified_here": false,
  "reference_metadata_occurrences": 352,
  "full_artifact_numeric_acceptance": false,
  "required_separate_gates": [
    "Actual included figure value/annotation audit",
    "Current reference metadata audit",
    "Current source-to-PDF identity and every-page visual QA",
    "Supplement numeric audit"
  ],
  "new_financial_computations": 0,
  "models_refitted": 0,
  "new_hypothesis_tests": 0,
  "private_arrays_read": false,
  "legacy_status": "FAIL",
  "v9_resolved_numeric_occurrences": 11,
  "v9_resolved_number_words": 1,
  "v9_verified_figure_identities": [
    {
      "path": "submission-jof/figures/v9-unified-history.pdf",
      "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "receipt_paths": {
        "placement": "notes/revision-v9/wp4-final-placement-v5.json",
        "point_audit": "notes/revision-v9/wp4-independent-audit.json",
        "visual_receipt": "notes/revision-v9/wp4-visual-QA.json"
      },
      "values_verified_here": false,
      "visual_review_performed_here": false
    }
  ],
  "legacy_checker_path": "notes/revision-v8/check_wp8_main_numbers.py",
  "legacy_checker_sha256": "a2fa6f10a085dfda25fd73faf8eec814b77f290fd167e863f16e5a2b437688c1",
  "v9_bindings_sha256": "16219b1fb805ecd6ba8a51c7e5f3fc514c0b39cb24ece8e02337b53cb9d26a00"
}

uv run --offline --no-project --with pytest python -B -m pytest test_v9_main_numbers.py test_v8_main_numbers.py test_v9_compile_diagnostics.py -q
...................................                                      [100%]
35 passed in 3.37s

python3 -B notes/revision-v9/compile_documents.py --stage wp6-final --targets manuscript
{
  "command": [
    "/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
    "-X",
    "compile",
    "--only-cached",
    "submission-jof/manuscript.tex",
    "--outdir",
    ".scratch/revision-v9/wp6-final/manuscript",
    "--keep-logs",
    "--keep-intermediates"
  ],
  "started_utc": "2026-10-25T00:32:18.979108+00:00",
  "ended_utc": "2026-10-25T00:32:19.594016+00:00",
  "elapsed_seconds": 0.613626416,
  "returncode": 0,
  "source": "submission-jof/manuscript.tex",
  "source_sha256": "2cbf38039b2b0d254ca88e3ad18badd6020907838ec5f2d31fe5d08799c8763f",
  "source_unchanged": true,
  "pdf_path": ".scratch/revision-v9/wp6-final/manuscript/manuscript.pdf",
  "pdf_sha256": "154519bd7d297541f9c9867f2a731fb64480014f0b3864c18b25046c615ee29c",
  "error_undefined_missing_glyph_overfull_lines": [],
  "child_peak_rss_bytes": 249626624,
  "resource_scope": "cumulative maximum child RSS of this sequential compiler wrapper",
  "only_cached": true,
  "numerical_thread_environment": 1,
  "packages_installed": 0
}

Acceptance readback:
{
  "wp": "WP6",
  "procedural_acceptance": "PASS",
  "actual_utc": "2026-10-25T00:32:44.798646+00:00",
  "prior_WP_end_commit": "d44364c6aa5ca5a9a043f33b9173f0864b771159",
  "roles": {
    "A": 7,
    "B": 7
  },
  "response_items": 14,
  "new_analyses": 0,
  "new_financial_runs": 0,
  "scientific_values_changed": 0,
  "remaining_substantive_gaps_not_claimed_solved": true,
  "writing_PASS": true,
  "numeric_mismatches": 0,
  "causal": {
    "before": 7,
    "after": 4,
    "affirmative_empirical_causal_claims": 0,
    "occurrences": [
      {
        "line": 46,
        "term": "established",
        "reason": "mature method adjective"
      },
      {
        "line": 62,
        "term": "established",
        "reason": "mature method adjective"
      },
      {
        "line": 92,
        "term": "establishes",
        "reason": "negative scope qualification"
      },
      {
        "line": 301,
        "term": "establish",
        "reason": "negative scope qualification"
      }
    ],
    "source_sha256": "2cbf38039b2b0d254ca88e3ad18badd6020907838ec5f2d31fe5d08799c8763f"
  },
  "PDF_pages": {
    "manuscript": 21,
    "supplement": 30,
    "extended-v9-technical": 6
  },
  "current_main_sha256": "2cbf38039b2b0d254ca88e3ad18badd6020907838ec5f2d31fe5d08799c8763f",
  "main_pdf_sha256": "154519bd7d297541f9c9867f2a731fb64480014f0b3864c18b25046c615ee29c",
  "targeted_tests": "...................................                                      [100%]\n35 passed in 3.37s",
  "full_default_suite": "Deferred to WP7",
  "all_page_visual_QA": "Deferred to WP7",
  "next_WP": "WP7 only after actual end commit"
}
```

Only writing and table-scope labels changed. Generated table numeric rows/bindings/namedfacts/sources are identical; old WP5 bindings preserved, new labels own a separate WP6 binding. Initial guarded generation correctly refused overwrite; first prefix invocation and first targeted test path were rejected before running any numerical work. Actual invocation errors are retained in the WP6 errata; no production bug or scientific failure is inferred from them. Current main/supplement compile with no error, undefined reference, missing glyph or overfull diagnostic. Full default tests, final artifact sync and allpage QA are WP7, not claimed here.


## WP7 local gates PASS; publication gate still PENDING

Actual local gate: 2026-10-25T01:00:14.541702+00:00. Prior WP6 end `2e6425881db1b25957d5d5da2f6e8168000a2caf`. This is not the WP7 final acceptance. Source/numeric gates, all58page actual visual basis, independent sourceZIP recompilation/text/pixels and default unfiltered tests passed. Remote publication is next.

Actual commands and complete owning outputs are saved as follows.

```text
python3 -B notes/revision-v9/check_main_numbers.py --output notes/revision-v9/wp7-main-number-audit.json
{
  "schema": "v9-additive-current-main-number-audit-1",
  "status": "PASS",
  "checked_utc": "2026-10-25T00:52:15.535786+00:00",
  "scope": "Current main and cover-letter located numeric occurrence/word audit; source lookup/display preservation only. Figure values, reference metadata and PDF positioning have separate owning gates.",
  "current_main_sha256": "9bff2b48461a0f042f9655cef71b4eb3ddfee30f8dd99786174118cd242006db",
  "current_cover_letter_sha256": "ee6988e523e3cfefb989c930802786d02c406cf6e63b32b40d7fd21eca4f6f87",
  "original_evidence_fields_checked": 1205,
  "original_main_saved_bindings_checked": 117,
  "original_table_preservation_commit": "642d6af",
  "original_table_vectors_checked": 6,
  "original_table_vector_mismatches": [],
  "labelled_table_rows_checked": 31,
  "labelled_table_numeric_tokens_checked": 80,
  "original_display_math_blocks_checked": 4,
  "accepted_exact_math_fragments_checked": 26,
  "total_numeric_occurrences": 582,
  "main_numeric_occurrences": 582,
  "cover_letter_numeric_occurrences": 0,
  "category_counts": {
    "figure_axis_or_layout": 53,
    "current_located_source_binding": 34,
    "existing_binding": 106,
    "source_file_or_model_label": 2,
    "mathematical_definition_or_structure": 20,
    "contribution_counter": 2,
    "reference_or_source_identifier": 29,
    "reference_or_crossref_identifier": 9,
    "reference_metadata": 314,
    "v9_located_source_binding": 11,
    "figure_path_or_display_parameter": 2
  },
  "unclassified_numeric_occurrences": 0,
  "ambiguous_numeric_locations": 0,
  "meaningful_number_word_occurrences": 32,
  "unbound_number_word_occurrences": 0,
  "old_and_new_percentage_fields_checked": 20,
  "failures": [],
  "mismatches": 0,
  "figure_paths": [
    {
      "path": "submission-jof/figures/v7-endpoint-peak-example.pdf",
      "current_sha256": "8a64f721028b931b5cd5a9031ad28a197ea5fc3b3338d3dd6bf13216e5e33d1f",
      "expected_receipt_sha256": "8a64f721028b931b5cd5a9031ad28a197ea5fc3b3338d3dd6bf13216e5e33d1f",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v7-murphy-fx_hourly.pdf",
      "current_sha256": "43e0c421140d91120eefac427f243b5775ebd43bfec579392b6d0e61ce199aa1",
      "expected_receipt_sha256": "43e0c421140d91120eefac427f243b5775ebd43bfec579392b6d0e61ce199aa1",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v7-murphy-nyfed_weekly.pdf",
      "current_sha256": "3bdb6d07d8f516ea8930c1f40a1c4396114369770bb66e74351260d236e8cd48",
      "expected_receipt_sha256": "3bdb6d07d8f516ea8930c1f40a1c4396114369770bb66e74351260d236e8cd48",
      "copy_identity_verified": true,
      "values_verified_here": false
    },
    {
      "path": "submission-jof/figures/v9-unified-history.pdf",
      "current_sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "expected_receipt_sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "copy_identity_verified": true,
      "values_verified_here": false,
      "v9_identity_evidence": {
        "path": "submission-jof/figures/v9-unified-history.pdf",
        "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
        "receipt_paths": {
          "placement": "notes/revision-v9/wp4-final-placement-v5.json",
          "point_audit": "notes/revision-v9/wp4-independent-audit.json",
          "visual_receipt": "notes/revision-v9/wp4-visual-QA.json"
        },
        "values_verified_here": false,
        "visual_review_performed_here": false
      }
    }
  ],
  "figure_values_verified_here": false,
  "reference_metadata_verified_here": false,
  "reference_metadata_occurrences": 352,
  "full_artifact_numeric_acceptance": false,
  "required_separate_gates": [
    "Actual included figure value/annotation audit",
    "Current reference metadata audit",
    "Current source-to-PDF identity and every-page visual QA",
    "Supplement numeric audit"
  ],
  "new_financial_computations": 0,
  "models_refitted": 0,
  "new_hypothesis_tests": 0,
  "private_arrays_read": false,
  "legacy_status": "FAIL",
  "v9_resolved_numeric_occurrences": 11,
  "v9_resolved_number_words": 1,
  "v9_verified_figure_identities": [
    {
      "path": "submission-jof/figures/v9-unified-history.pdf",
      "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
      "receipt_paths": {
        "placement": "notes/revision-v9/wp4-final-placement-v5.json",
        "point_audit": "notes/revision-v9/wp4-independent-audit.json",
        "visual_receipt": "notes/revision-v9/wp4-visual-QA.json"
      },
      "values_verified_here": false,
      "visual_review_performed_here": false
    }
  ],
  "legacy_checker_path": "notes/revision-v8/check_wp8_main_numbers.py",
  "legacy_checker_sha256": "a2fa6f10a085dfda25fd73faf8eec814b77f290fd167e863f16e5a2b437688c1",
  "v9_bindings_sha256": "16219b1fb805ecd6ba8a51c7e5f3fc514c0b39cb24ece8e02337b53cb9d26a00"
}

python3 -B notes/revision-v9/check_source_zip_closure.py --sync-receipt notes/revision-v9/wp7-deliverable-sync-final.json --output notes/revision-v9/wp7-zip-closure-recovered.json
{
  "status": "PASS",
  "difference_count": 0,
  "differences": [],
  "expected_member_count": 21,
  "actual_member_count": 21,
  "package_sha256": "3691deaf6f31e89ce27ddff2ba63847cc7f42f6e9b1c3c5660a3c9c2323775d7",
  "elapsed_seconds": 0.003703874999999999,
  "peak_rss_bytes": 15695872,
  "financial_models_run": 0
}

python3 -B notes/revision-v9/check_document_package.py --suffix final (cached uv pypdf/Pillow)
WARN `--no-project` was provided, but no project was found
manuscript 21 pages: all text and pixels identical; visual review separate
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4433522320), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4433522320)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4433522320), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4433522320)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4433522320), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4433522320)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4433522320), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4433522320)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(422, 0, 4433522320), '/FirstChar': 91, '/LastChar': 91, '/BaseFont': '/GJMHKB+MSBM10', '/FontDescriptor': IndirectObject(484, 0, 4433522320)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4433522320), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4433522320)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4439803760), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4439803760)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4439803760), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4439803760)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4439803760), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4439803760)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4439803760), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4439803760)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(422, 0, 4439803760), '/FirstChar': 91, '/LastChar': 91, '/BaseFont': '/GJMHKB+MSBM10', '/FontDescriptor': IndirectObject(484, 0, 4439803760)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(411, 0, 4439803760), '/FirstChar': 16, '/LastChar': 113, '/BaseFont': '/UTACNV+CMEX10', '/FontDescriptor': IndirectObject(481, 0, 4439803760)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
supplement 30 pages: all text and pixels identical; visual review separate
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(92, 0, 4433093616), '/FirstChar': 12, '/LastChar': 12, '/BaseFont': '/PVTTLK+CMEX10', '/FontDescriptor': IndirectObject(116, 0, 4433093616)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
fontTools is required to fully parse the encoding of a CFF Type1 font in font dictionary {'/Type': '/Font', '/Subtype': '/Type1', '/Widths': IndirectObject(92, 0, 4436313296), '/FirstChar': 12, '/LastChar': 12, '/BaseFont': '/PVTTLK+CMEX10', '/FontDescriptor': IndirectObject(116, 0, 4436313296)}, but is not installed. Consider installing fontTools if you encounter encoding problems.
extended-v9-technical 6 pages: all text and pixels identical; visual review separate
title-page 1 pages: all text and pixels identical; visual review separate
{
  "actual_utc": "2026-10-25T00:47:35.541444+00:00",
  "status": "PASS",
  "package_sha256": "3691deaf6f31e89ce27ddff2ba63847cc7f42f6e9b1c3c5660a3c9c2323775d7",
  "total_pages": 58,
  "isolated_source": ".scratch/revision-v9/wp7-document-package-final/sources",
  "cumulative_child_peak_rss_bytes": 251559936,
  "root_process_peak_rss_bytes": 151715840,
  "installed_packages": 0,
  "network_downloads": 0,
  "raw_financial_inputs": 0,
  "financial_models_run": 0,
  "visual_review_performed_here": false,
  "public_financial_replay": "Separate; missing original local Git objects/rights-cleared raw input not repaired"
}

python3 -B notes/revision-v9/run_full_pytest.py wp7-release-gate
{
  "command": [
    "/Users/bingyouli/.local/bin/uv",
    "run",
    "--no-project",
    "--no-env-file",
    "--python",
    "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "--with",
    "pytest",
    "--with",
    "arch",
    "--with",
    "scikit-learn",
    "python",
    "-B",
    "-m",
    "pytest",
    "-p",
    "no:cacheprovider",
    "-v",
    "--basetemp",
    "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp7-release-gate/pytest-temp"
  ],
  "cwd": "/Users/bingyouli/Research/\u8bba\u6587/\u91d1\u878d\u6570\u5b66\u8bba\u6587-\u4fee\u8ba2v3-20261023/.scratch/revision-v9/wp7-release-gate/full-suite-copy",
  "scope": "Full default discovery; every tracked/indexed file copied; no test filter or skips added",
  "tracked_files_copied": 3699,
  "started_utc": "2026-10-25T00:56:11.432003+00:00",
  "ended_utc": "2026-10-25T00:58:01.751631+00:00",
  "elapsed_seconds": 110.319849416,
  "returncode": 0,
  "child_peak_rss_bytes": 339918848,
  "sampled_process_tree_peak_rss_bytes": 402784256,
  "stop_reason": null,
  "output_sha256": "f3b1d212b12f0a1e4caba884d74f8330641de146f03e113188bc16f1cb7b6d04",
  "numerical_threads": 1,
  "UV_OFFLINE": true
}
test_verify_rank_ablation.py::IndependentReadbackTests::test_scalar_oracle_reanchors_floor_and_freezes_until_next_refit PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_strict_npz_boundary_rejects_missing_duplicate_and_unexpected_keys PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_thread_snapshot_requires_every_pid_row PASSED [ 99%]
test_verify_rank_ablation.py::IndependentReadbackTests::test_ties_strict_breach_and_zero_breach_reason PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_changed_public_values_and_private_issue_are_all_reported PASSED [ 99%]
test_verify_rank_ablation.py::CompleteSyntheticAttemptTests::test_complete_synthetic_readback_is_arithmetic_only_and_records_actual_resources PASSED [100%]

============ 1534 passed, 1068 subtests passed in 109.49s (0:01:49) ============

```

The complete 1,534-test/1,068-subtest stdout is preserved without selection or truncation in `notes/revision-v9/wp7-release-gate-pytest-output.txt`, SHA256 `f3b1d212b12f0a1e4caba884d74f8330641de146f03e113188bc16f1cb7b6d04`. No test filter, skip or missing-history bypass was added.

The first full run failed1old-layout positive (1484pass); the second failed3fresh-copy path contexts (1531pass); both raw logs/receipts remain. The original oldguard and all8original methods/assertions are exact; only a named ordinary fixture setup now proves the current compact+extended inverse layout before applying its v8 contract. Archive census explicitly reports2232unchanged plus that1test-fixture code difference. The corrected Git census uses `--full-tree`; no absent original commit becomes acceptable. The writer receipt-shadowing defect was caught before publication, reproduced RED, minimally repaired and covered by output-contract tests. Archive-relative path checks work inside task scratch as well as at repository root. Scientific values, frozen protocols and original result archives are unchanged.

All actual current document identities:

```json
[
  {
    "document": "manuscript",
    "pages": 21,
    "pdf_sha256": "60be9859b5bd7dfde4861f558852edd0a5db6c3896867ad7f12082123dbcdd5e",
    "source_sha256": "9bff2b48461a0f042f9655cef71b4eb3ddfee30f8dd99786174118cd242006db"
  },
  {
    "document": "supplement",
    "pages": 30,
    "pdf_sha256": "5de7d8f4d9e5c7a5792399c3f195b44e73ecde750e240079a3bf6eeaa2c3e7b1",
    "source_sha256": "ae9d9cbe5d4100a6cb35abddafeaf49441181e953f176623e5d37728b41f4fb9"
  },
  {
    "document": "extended-v9-technical",
    "pages": 6,
    "pdf_sha256": "bf242d71f16cf8178e0bfabf669bdd2056532440caa991ab939ec73c4199928e",
    "source_sha256": "4af08dded87ff896143fc5e341cf966269e26ce3b16bdb5de143a284fdc6cfb4"
  },
  {
    "document": "title-page",
    "pages": 1,
    "pdf_sha256": "f72a487713b674cf9a745d57d97e9080dfb44312085622d71025056dea1f9a0b",
    "source_sha256": "43011e5debcc7334ea03af2c06aea9c642d4adb9d3243a62dba6fa5115f2a9a3"
  }
]
```

Main21pages, Supplement30, linked complete technical6, unfilled titletemplate1. Fourmainfigures and6maintables; broader bodybudget6209words. 32reference entry contents were alphabetized without changing any entry fields; only mainpage21changed and was directly re-viewed. All other final raster pages equal their individually viewed basis. The initial Supplement29column-readability concern was not reproduced by direct original-page rechecks and is retained in the visual receipt; no fabricated numeric/layout defect is asserted. 

Existing cached Tectonic only; uv uses existing offline cache in temporary environments, with no new system/TeX installation. This local suite has access to original local Git objects. Browser file-tree mirroring does not transfer them; fresh public-clone sealed financial replay/history-dependent checks remain a separate BLOCKED provenance issue, and private FX observations/vectors remain excluded.


## WP7: PASS — local release gates and frozen-payload remote identity

Actual closing record: 2026-10-25T04:11:11.884904+00:00. The 18 authorized GitHub upload commits were each fresh-fetched and checked for exact path/blob/mode scope and their expected single parent. All 404 changed files / 55,415,163 bytes were transmitted from the immutable snapshot. The full payload has 3,703 files / 205,037,784 bytes and exactly the frozen tree. The final local WP7 commit and the finite closing-metadata mirror are bound after their actual creation/readback in ignored runtime; this avoids embedding a commit hash inside its own commit. No whole-task completion before the fixed deadline is asserted.

Actual batch verification commands and saved emitted JSON receipts are retained in `notes/revision-v9/wp7-publication-command-output.txt` and `wp7-publication-batches.json`. Final payload command and original stdout:

```text
python3 -B .scratch/revision-v9/publish_snapshot.py whole
```

```json
{
  "actual_utc": "2026-10-25T04:09:46.484864+00:00",
  "status": "PASS",
  "source_index_tree": "fb2c3a741e8876056aefcdbf1784791d125f04fd",
  "remote_commit": "f866a6145a96f82f6234f87a1b50ab741b66e04e",
  "remote_tree": "fb2c3a741e8876056aefcdbf1784791d125f04fd",
  "files": 3703,
  "bytes": 205037784,
  "missing": [],
  "extra": [],
  "content_or_mode_differences": [],
  "protected_refs": {
    "main": "65feeee801b6b228a608ca3200e0678bb5f62b1c",
    "codex/supervisor-revision-20261023": "2328994c44ec02bd731ad556f41fe9821f6de6df",
    "revision-v7-final": "d119a1fb30c48ceab9000552057882938cfa57a4"
  },
  "protected_ref_differences": {},
  "git_histories_identical": false,
  "public_financial_replication_claimed": false,
  "scope": "Full Git file/blob/mode identity against frozen index tree; original local design objects and private financial input remain separate",
  "fetch_output": ""
}
```

The existing complete default suite remains 1534 passed, 1068 subtests passed in 109.49s; no numerical experiment, bootstrap, compile or test was rerun for publication. All four document/PDF/source and source-ZIP hashes were checked against the already passed local acceptance before closing. The earlier local-only receipt remains historical evidence of its then-pending remote state; `wp7-final-acceptance.json` supersedes that publication field. The two earlier full-suite failures, output-writer failure, RED/GREEN evidence, negative results, left-censoring, six P3 counterexamples and long-history reversals remain present. The native selector focus/disabled-Open interruptions were resolved using the browser's documented file-chooser control and exact frozen paths; no hidden network, credential, permission or CLI write route was used. Early readbacks during GitHub processing did not trigger duplicate uploads.

Scope remains limited: exact public file-tree equality does not transport original local design Git objects and does not establish an independent financial replication. Fresh-public-clone history-dependent financial replay remains BLOCKED pending an author-approved safe provenance route. No private FX observations/vectors or private identity bundle is exported. Main and PR #3/#4 refs remain unchanged. The fixed deadline remains 2026-10-25T05:10:12Z; after the actual final closing readback only the prescribed bounded review loop is allowed, with shared local/browser commit cadence.
