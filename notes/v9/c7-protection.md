# C7 保护与归档完整性验收

总体：**PASS（文件与来源完整性；不改变任何科学判断）**。核查 2026-10-24T20:36:59.388268+00:00 至 2026-10-24T20:37:10.620101+00:00，耗时 11.232 秒。

仅新增本 JSON/Markdown；没有拟合、诊断、预测、模拟、研究模块导入、重跑/补救，未提交。两旧目录只读；全部 Git 调用设置 `GIT_OPTIONAL_LOCKS=0` 和 `GIT_TERMINAL_PROMPT=0`。私有基线仅导出指纹、计数与公开 Git 身份，不输出原数据字段、私有文件名或内容。

|保护范围|结果|实际检查|
|---|---|---|
|protected-v7|PASS|tracked 3320；不变 3320；改变 0；缺失 0；tracked 增/减 0/0；HEAD/tree/branch 均匹配=True。|
|protected-v8|PASS|tracked 2780；不变 2780；改变 0；缺失 0；tracked 增/减 0/0；HEAD/tree/branch 均匹配=True。|
|远端受保护 heads / PR heads|PASS|7 个 C0 指定 refs；匹配 7/7。|
|PR5 继承 data/results|PASS|1590 文件，改变 0、缺失 0；新 v9 文件不混入分母。|
|C2 sealed 科学代码/协议|PASS|manifest 的 14 个代码 SHA、协议 SHA、输入边界元数据 SHA、9 个 forecast source SHA 与 run-plan seal。|
|正式 ZIP / parts / index / loose|PASS|2 个 parts；39518 个 index 条目，ZIP 与 loose 均逐项核字节/SHA；改变/缺失均为 0/0/0。|
|原报告错误与独立序列化|PASS|7 个 source receipts、5 个 postrun outputs 的 SHA 符合 provenance；原坏写 159-byte predictions 与独立保留副本一致。|

## 远端身份

|Ref|C0 / 本轮实际 SHA（匹配时）|状态|
|---|---|---|
|`refs/heads/main`|`65feeee801b6b228a608ca3200e0678bb5f62b1c`|MATCH|
|`refs/heads/revision-v7-final`|`d119a1fb30c48ceab9000552057882938cfa57a4`|MATCH|
|`refs/heads/revision-v8`|`f151b830489917ab7abc5137f2ec6b4135f55d6e`|MATCH|
|`refs/heads/revision-v8-goal`|`0f1f066843e0c49cf3e24bce7d72032dc189603d`|MATCH|
|`refs/pull/3/head`|`2328994c44ec02bd731ad556f41fe9821f6de6df`|MATCH|
|`refs/pull/4/head`|`d119a1fb30c48ceab9000552057882938cfa57a4`|MATCH|
|`refs/pull/5/head`|`0f1f066843e0c49cf3e24bce7d72032dc189603d`|MATCH|

本次只核 C0 原有 main、v7、v8、v8-goal 和 PR3/4/5 heads；新 v9 发布后的 remote tree/content 验收仍由主任务随后进行，本报告不先行声称完成。

## 无损分片与完整日志

拼接 40,508,197 bytes 的流式 SHA256=`7ecc25fe719c5624e8e9774b38eb3a54aa6ed14d6d8756d3cbefbbffe214c1b8`，与 `archive-parts.json`、原 `units.zip` 和 `units-manifest.json` 的 whole hash 完全一致。每片 ≤20 MiB，原完整 ZIP 和全部 loose files 均保留；本次未写复原文件。

index 39,518 条，unique 39,518；ZIP 39,518 条、172,735,704 uncompressed bytes；loose 39,518 条、172,735,704 bytes。无重复/额外/缺失 ZIP member，无哈希或字节差异。

## 科学失败与报告层错误继续保留

正式 416 个 worker 的已有回执、4990 COMPLETE / 2 FAILED 方法、13303 COMPLETE / 9 FAILED candidates、102 COMPLETE / 2 FAILED 条件格和 52 COMPLETE F 格均按保存的审计计数报告；没有重算统计量或把失败格改成成功。N1=SUPPORTED、N2=UNASSESSABLE、N3=NOT_SUPPORTED、N4=UNASSESSABLE 保留。daily NONREGULAR_NULL、hourly 优化失败与两个 W260 QR33 31/32 失败格继续成立；完整性 PASS 不提供额外科学支持。

冻结 runner 的原 NumPy 标量 JSON 写入错误及坏写 predictions 原件仍在，独立 postrun 只作同值标量序列化；7 个来源及 5 个输出均符合既存 provenance SHA。报告器/metadata 文件没有被拿来替换研究原件。

原错误文本：2480 bytes，SHA256=`6ce1afe17f68bda5863b25aacf723f30ec038f85efaf6940616c53eadd69dd26`；其 SHA 是否在 C2 说明已记载：True。原始坏写 JSON 仍不可解析，且与 `postrun/original-predictions-write.txt` 逐字节相同。

所有逐项布尔值、SHA、计数与检查边界见相邻 `c7-protection.json`；私有基线的全文件清单未被复制到公开报告。
