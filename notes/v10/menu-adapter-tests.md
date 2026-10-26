# E1 六菜单适配器人工测试记录

实施前已读取独立冻结的 `protocol/v10/menu-isolation-design.md`。其提交为 `3c5f167632a1a21ded29731a773a85ab307d3a96`，设计 SHA-256 实际核对为 `f15d9ce114bd6675a4094aa4997cab5566766792beaad3a87c505814041279c7`。

本工作只新增 `v10_menu.py`、`test_v10_menu.py` 和本记录。没有执行真实校准、统计、bootstrap、随机路径生成、研究 pilot／formal、真实序列预测或评估；没有提交，也没有运行全套 suite。人工测试使用确定性正弦／余弦／多项式构造序列和小型报告回调；不会读取金融输入或旧数值 study 数组。

## 先 RED 后 GREEN

测试先写入，生产适配器尚不存在时运行同一测试命令：

- RED：exit 1，`17 failed in 0.37s`；全部失败均为预期断言 `six-menu adapter is missing`，没有收集错误、环境错误或继承求解器错误。
- 随后新增适配器并运行原命令。
- GREEN：exit 0，`17 passed in 0.39s`。

两次运行均出现 uv 的 `--no-project was provided, but no project was found` 环境提示；pytest 无其他 warning 或 error。没有为得到 GREEN 修改测试期望或数值接受标准。

实际命令（同一次人工测试范围）：

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest==9.1.1 python -B -m pytest -q -p no:cacheprovider test_v10_menu.py
```

## 真实行为覆盖

1. 有限分支直接调用未改动的 `v8_mechanism_mc.forecast_report`。人工序列上，F／W52、QR33／QR4 在 W52 的 lambda .1 和 W260 的 lambda 10，均核对 origin、capacity、refit indices 和完整 fit diagnostics 精确相同；同时验证 `predict_report` 别名入口。
2. QR33／QR4、W52／W260 的 `"inf"` 容量精确等于现成 `empirical_headroom.predict` 的 I；独立循环重建成熟 headroom 并按 rank50／247 取次序统计量。严格递增人工响应将其与 corrected F 区分。测试同时禁止 finite solver 被 infinity 分支调用，并检查 current floor、refit500／524、训练首尾／数量／label maturity。
3. 两方法完全相同 validation loss 取最强 `"inf"`；去掉 infinity 最小值后取 10；`nextafter` 的真实非零差异按实际损失选择，未引入 tolerance tie。
4. QR33 任一 required candidate 失败则 ineligible；QR4 从其余 completed candidates 选择；无 completed candidate 则 ineligible。缺失候选、错误 origin count 和非有限完整 loss 均拒绝。
5. 候选 `.001` 的人工 NONCONVERGENCE 被写入完整六候选库存；QR33 不评估，QR4 精确选择 infinity。独立读取 selection receipt，确认它已在 selected evaluation 前落盘。
6. selected evaluation 人工失败后保留选中的 infinity 和失败原因；只调用这一项 evaluation 一次，没有 fallback、retry 或第二 lambda。
7. 资源中断保留已尝试 candidate 的 FAILED 回执、method 失败原因和其余五个 NOT_ATTEMPTED 行。
8. 报告回调实际返回 NumPy scalar 的 n／loss／breach，公开 JSON 及返回 row 转为同值原生有限标量；JSON 保存内容与返回 row 相同。进度日志只使用继承的有限状态字段，不打印预测数组。

## 接口与新增 tie 字段

`forecast_report` 与其别名 `predict_report` 沿用 v8 的完整参数签名和返回 shape。有限惩罚无重新实现的拟合路径；`"inf"` 返回 I 容量和原 shape 的训练成熟度 diagnostics。`select_candidate(records, method, expected_origins, menus)` 以及 `evaluate_method(design, public, window, horizon, method, report, checkpoint, fit_error, resource_errors)` 保持旧调用签名。

两方法六点菜单为 `.001,.01,.1,1,10,"inf"`，QR33 的 required-all 与 QR4 的 completed-subset 分别保留。旧 QR4 exact tie 取较弱 lambda；新 QR4 按用户冻结要求取较强 lambda，属已披露的次要程序差异。

selection receipt 与 method return row 增加：

- `exact_tie`：最小 validation loss 有两个或以上 completed candidates 完全相同。
- `minimum_loss_tied_candidates`：达到该最小 loss 的 completed candidate 数量；ineligible 为 0。
- `tied_penalties`：这些候选，按固定弱到强菜单排序；ineligible 为空。
- `legacy_qr4_tie_changed`：QR4 且 exact tie，表示本次选择与旧较弱 tie 规则不同。

## 冻结源与本次文件指纹

实际逐项核对 design 中九个 `v9_forecast_source_sha256` 均 MATCH；`v9_switching.py` 也与 design 的 generator SHA 相同。`git diff` 对 `v8_mechanism_mc.py`、`run_v8_wp3.py`、`empirical_headroom.py` 为空。没有改动任何继承算法源。

| 新文件 | bytes | SHA-256 |
|---|---:|---|
| `v10_menu.py` | 10540 | `e91c942d6a24cb833ceaed48c282360a578325c0ebf3c5b370b42c4b14ca5014` |
| `test_v10_menu.py` | 8637 | `cf6eb728f1def76c2eafcd479681c8d2d7b1df080cf348db76e45d16b8bdde10` |

本记录仅证明上述人工适配行为与源完整性。driver 的 phase／路径配对、正式运行资源、完整研究输出、汇总和全套测试由主任务另行验证，不能从这 17 个测试推导其已完成。
