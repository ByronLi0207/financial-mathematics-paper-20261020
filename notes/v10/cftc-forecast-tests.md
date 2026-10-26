# E2 六方法 forecast 适配器人工验证

开发前已读独立冻结的 `protocol/v10/cftc-design.md`，设计提交为 `acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf`，实际文件 SHA-256 为 `a7aacd4180d27ab810284119b0e4d0cdef79e5d2b0d0c9e7ad2cef8037ab5d78`。

本次仅新增 `v10_cftc_forecast.py`、`test_v10_cftc_forecast.py` 和本记录。未读取真实 CFTC observations／archives，未下载，未执行真实 study，未提交，未运行全套 suite。测试仅使用 400／110 点自造常数序列与正弦趋势序列，日期为从 2000-01-03 起的人工周标签；人工 design 的 validation4／evaluation8 用于短测试。生产设计的 validation52／evaluation260、W52／260、H6 与 step13 均未修改。

## RED → GREEN 证据

- 先写测试，生产模块不存在时实际运行：exit1，`9 failed in 0.22s`，全部为预期断言 `CFTC forecast adapter is missing`；无收集错误或环境错误。
- 新增生产模块后，同命令实际 GREEN：exit0，`9 passed in 0.27s`。
- 随后增加非恒定输入的原 segment／gap feedback 核对，并加强原测试的逐方法恢复断言：exit0，`10 passed in 0.42s`。
- 三次均仅有 uv 提示 `--no-project was provided, but no project was found`，没有 pytest warning／error。没有为得到通过而修改数值接受标准或生产 design。

实际 focused 命令：

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest==9.1.1 python -B -m pytest -q -p no:cacheprovider --tb=short test_v10_cftc_forecast.py
```

## 已实现的输入、缓存与持久化边界

入口为 `forecast_cell(position,times,design,window,output,checkpoint=None)`。caller 提供数组；模块没有源获取或路径加载接口。`output` exclusive 创建。split 根据 N、H 和冻结 design 内的 validation／evaluation count 推导；validation 和 evaluation 各自以首个 issue 为 refit13 原点。特征只调用既有 `build_features(short_scale=6,long_scale=26,nominal_gap_seconds=604800)` 的 design 参数。

返回 `methods` 固定六行，顺序为 F、I、QR4、QR33、ACI_F、ACI_QR33；每行含 method／status／selected_penalty／selected_gamma／mean_loss／strict_breach_count／n／reason。返回 `traces` 只包含完整方法，固定八个 NumPy 数组键：origins、capacities、peak、floor、pinball、strict_breach、overrun、unused。

每个完整方法立即先用 exclusive 文件句柄写 `trace-METHOD.npz`，随后 exclusive 写 `result-METHOD.json`，包含相对 `trace_path`、`trace_bytes` 和 `trace_sha256`。普通失败／NA 也独立写 canonical result，没有 trace 或 partial mean。后续方法或 ACI 中断不会删除此前完整方法的数据。StudyStop 和 DriverStop 显式向 root driver 传播，由 root 为未完成 slots 留存失败库存。

QR 方法直接复用 `v10_menu.evaluate_method` 和 finite／infinity forecaster。候选与选择仍写到既有 `W{W}_H{H}_METHOD...json`，不覆盖这些回执；canonical result 使用另一文件名。QR33 required-all、QR4 completed-subset、两方法 stronger exact tie 和一次 selected evaluation 原语义均继承。

base segment 以方法、lambda、起止 issue、W 和 step 为键，成功和失败均缓存。F／I 来自同次既有 empirical 函数调用；QR33 validation candidate capacities 和 selected evaluation capacities直接给 ACI_QR33。ACI 只增加独立 warm segment，固定已选择 lambda，不为 ACI 重新拟合 validation 或 evaluation，也不增加 tau 层拟合。

ACI 直接调用既有 `initialization_grid`／`aci_stream`／`select_gamma`：F minimum feature0，QR33为26；至少19个成熟 warm scores；固定四 gamma，各尝试一次，完整 validation coverage-first 选择；选择落盘后才拼接 validation 与 evaluation，精确核对 validation capacity 前缀。原 gap 没有虚构 issue；此方法仍称 finite delayed ACI-style calibration，不导入 canonical ACI 保证。

## 十项人工行为验证

1. 真实旧数值函数处理自造常数序列，六方法均完成；动态 split 给出人工 evaluation386..393；所有逐点 trace 为完整有限八键数组，F／I 精确匹配既有 empirical 结果。
2. 六点 QR candidate 和 selection receipts完整；常数序列的 exact tie 选 infinity。四 gamma receipts完整，gamma 先按既定准则选择；validation prefix identical 为真。
3. 所有 complete canonical results 与 API row 一致；NPZ 先存在，bytes／SHA 一致，八键完整。
4. 真实 forecaster外层计数确认同一 QR 方法／lambda／segment 不重复拟合；ACI_QR33 仅增加一次独立 warm segment，复用已保存 validation／evaluation bases。
5. 强制一个 QR33 mandatory candidate 数值失败：保留六 candidate，QR33 无 partial mean／trace，ACI_QR33 unavailable；F、I、QR4、ACI_F 不受影响。
6. 强制 selected QR33 evaluation失败：selection已在调用前落盘，只尝试选中 infinity 一次；没有另一 lambda、重试或 ACI rescue。
7. 四 gamma全部失败：各失败均可见，ANC 无 trace／partial mean；四个 base 方法保持完整。
8. 强制 combined ACI stream 改动 validation 前缀：即使 gamma selection存在，方法仍整格 FAILED／VALIDATION_PREFIX_CHANGED，不对 evaluation 成功部分评分。
9. 人工短历史区分 feature0／26 的 warm准入：base QR33 完整、ACI_F 完整、ACI_QR33因不足19个成熟 warm scores为NA；没有缩短 validation或改 feature边界。
10. 非恒定正弦趋势输入下，ACI_F 精确匹配独立组装的 warm／validation／evaluation经验基模型和既有 ACI引擎；没有 gap origins380..385；共消费6个成熟 wrapped feedback（4个 validation、2个 evaluation），防止 evaluation 重置状态。分别以 StudyStop／DriverStop 中断后，F和I的完整逐点 NPZ及canonical results仍存在。

## 指纹与验证范围

逐项核对 design 的全部九个 `inherited_or_E1_code_sha256` 均 MATCH；`git diff` 对本次所用继承模块和 E1 adapter为空。

| 新文件 | bytes | SHA-256 |
|---|---:|---|
| `v10_cftc_forecast.py` | 14494 | `4638b0aa039d35fc0252267b902a1985cc8d01d83a87c0a8f1c48aeff2c8894e` |
| `test_v10_cftc_forecast.py` | 11602 | `cbeba7bf37e48478b714dbfc3dc51f9f0798b879bb81b8de13b81115b6db0791` |

本记录只证明所述人工 forecast 接线、失败与保存行为。真实数据获取／解析、source universe、真实52／260点完整性、资源运行、汇总和全套测试由 root另行验证；本次不声称任何真实 CFTC预测结果或独立实证结论。
