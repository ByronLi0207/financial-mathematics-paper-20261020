# E3 MCS wrapper 人工验证记录

开发前已读 `protocol/v10/mcs-design.md`，其独立提交为 `78ea93493379ab3a93459d28e1bab84200f01539`，实际 SHA-256 为 `2985d6484f9ca0fbb61281e082cf3a6a9496ee0667a042b7eb32aff39f353654`。本地依赖 introspection 确认为 arch8.0.0；其 MCS.included 使用 `Pvalue > size`，excluded 使用 `Pvalue <= size`。

本工作只新增 `v10_mcs.py`、`test_v10_mcs.py` 和本记录。没有读取真实金融 loss、capacity、target 或任何真实 comparison matrix；没有运行实际 E3 MCS，没有修改已冻结 E2 数值代码，没有提交或运行全套 suite。所有数值测试仅使用人工 PCG64 随机数和自造数组。

## RED → GREEN

- 先写19项测试，模块尚不存在时实际运行：exit1，`19 failed in 0.87s`；全部为预期断言 `MCS wrapper is missing`，没有收集／环境错误。
- 新增包装器后同命令实际 GREEN：exit0，`19 passed in 2.09s`。
- 补充真实 arch 的人工零方差差异警告与 zero-method unavailable 回归：exit0，`21 passed in 2.02s`。

实际命令：

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with arch==8.0.0 --with numpy==2.3.5 --with pytest==9.1.1 python -B -m pytest -q -p no:cacheprovider --tb=short test_v10_mcs.py
```

仅有 uv 的 `--no-project was provided, but no project was found` 环境提示；pytest没有未处理warning／error。人工 fixtures 使用99、49、17或11 bootstrap replications；生产仍从已冻结 design 读取1000，没有修改 protocol 或实际 run 配置。

## 包装器合同

入口为 `compute_mcs(losses,identity,design,checkpoint=None)`，只接 caller-owned method-ID→loss-vector mapping。方法列始终 lexicographic 排序；不作 semantic alias 或方法类别决策。

每个输入必须为非空一维、有限、非负、相同长度的完整 loss；任何不符合均 FAILED_INPUT，library_attempts0，不删方法、不交集、不缩短。零个方法为 UNAVAILABLE。

仅按完整 `np.array_equal` loss 分组，`unique_loss_groups` 固定为 `[{representative:lexfirst,members:[...]}]`。一个完整方法为 COMPLETE_SINGLE_METHOD；多个方法但一个 exact-loss class 为 COMPLETE_IDENTICAL_LOSSES；这两种解析情况全部 p1、全部 included、library_attempts0，不构造 arch MCS 对象。方法总数与 unique class 数明确保存。

其余情况只调用一次 arch8.0.0 `MCS(size=.10,method='R',bootstrap='stationary',reps=design.bootstrap_repetitions,block_size=max(H,ceil(n**(1/3))),seed=...)`。seed 为冻结 identity JSON 与 prefix 的 SHA256 前四字节 big-endian；不依赖 dict 插入顺序或 loss 排名。

library 的 included／excluded／pvalues 原样读取，检查全代表集合的完整不重叠 partition、合法 index、有限且位于[0,1]的 p-value、`>size`／`<=size` 一致性。随后展开到每个 distinct procedure ID。任何 RuntimeWarning、其他 library exception 或无效结果整格 MCS_FAILED，included／excluded／pvalues 清空，保留诊断和一个 attempt；没有 retry、alternate statistic／block／bootstrap 或 subset。

StudyStop／DriverStop 显式不吞；before／after checkpoint 的资源中断继续交给 root worker 记录。包装器无文件 I/O、forecast、loss derivation 或实际研究调度。

## 人工行为证据

1. 真实 arch8 对两列256点人工正随机 loss计算：明显较差列还含独立随机变化，被排除；较好列保留。该例没有利用恒定差异造成零方差。
2. 精确复制较好 loss 但保留另一个 procedure ID：library 矩阵只有两个代表列、代表按 lexical 排序；展开后两个等价标签同时 included，p-value相同，较差标签 excluded。
3. all-identical 与 singleton 分别验证解析 status／explicit counts，禁止构造任何 library对象。
4. 同 seed、同数据、反转输入 dict顺序，真实 library 的完整返回row精确相同。含 Unicode 的人工 source identity核对固定 seed4102530119；n256/H6核对 block7，H24核对 horizon下界24。
5. 人工 library 在 compute 中发 RuntimeWarning 或抛 exception，均只构造一次／compute一次，reps不变，没有第二配置。
6. literal p=.10 被 excluded；非有限／超范围 p-value、缺失／重叠 partition、与 p-value边界矛盾的 membership均整格失败。
7. NaN、长度不匹配、负 loss、二维 matrix输入均 FAILED_INPUT，零 libraryattempt。
8. 真实 arch 对人工 `a=x,b=x+2` 的零方差差异确实产生 RuntimeWarning；wrapper保留两个不相等 loss class，并以 MCS_FAILED／1attempt结束，没有将常数差异也合并为 exact equality。
9. 空 mapping为 UNAVAILABLE／0attempt；两种 root资源异常都向外传播，未启动 library或重试。

## 文件指纹与边界

| 文件 | bytes | SHA-256 |
|---|---:|---|
| `v10_mcs.py` | 7246 | `2c8d3b759240134557ebced420a0c15210409586a2e23d329c2905f190905a35` |
| `test_v10_mcs.py` | 8022 | `b2e98a2965f6aabf5d973c8b2db51c31ce4884a7c09a8b139b5f9f2223979685` |

这21项测试只验证包装、固定配置、解析等价类、library展开和失败语义；真实 source／period／origin／target admission、完整98格库存、semantic aliases、正式1000次bootstrap、资源归档与汇总由 root另行执行验证。本记录不含真实金融 MCS 结果。
