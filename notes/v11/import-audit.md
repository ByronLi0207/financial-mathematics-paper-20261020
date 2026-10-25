# v11 导入前来源核查与裁定

固定来源为PR5 / revision-v8-goal `60e03b8ae7a950c96ace3987f0625b3e434e6887`；基础稿为revision-v10b `de1a1cf`。只读Git源，不运行实验、评分或结果汇总。

|项|设计提交UTC|正式开始UTC|结果完成提交UTC|自己的SHA回执|裁定|
|---|---|---|---|---|---|
|WP2|f2ce438，2026-10-24 22:19:50|22:25:19.696709|1a535ef，22:59:15|30,536 members及summary/support等全部一致|导入保存的确认汇总表|
|WP3|b26628f，23:13:51|23:24:51.666335|bfd0493，23:39:27|206 members及五项输出全部一致|按用户给定两位锚点精度导入；完整精度末位差异明确保留|
|WP4|wp4-display合同原首次32ee586，23:49:08|首次render完成23:42:24.685879；v5完成23:46:39.218742|32ee586，23:49:08|图及380点/映射/来源均一致|不导入：合同commit晚于render，不豁免用户时序门槛|

## 原提交证据与网页上传区别

公开网页上传均晚于研究计算，不能充当运行前设计提交。初次仅看公开源时三份分项审计给UNVERIFIED/FAIL，该初稿完整保留。随后以GIT_OPTIONAL_LOCKS=0仅查询旧原Git对象的cat-file/show/log/diff-tree/rev-parse/merge-base；没有status/checkout/fetch/索引/配置/工作树/分支写入。旧HEAD查询前后均689d492。raw commit bytes可独立还原原Git SHA-1，设计与结果protocol/result blobs共21项与固定公开源逐字相同。证据在original-commit-proofs.json及original-blob-proofs.json；WP2补核为wp2-provenance-reconciliation.json。此项验证本地研究时间链，不声称当时已公开预注册。

## FX两个锚点的两层核对

|W|v10b owning paired-comparisons原保存值|WP3 contrasts原保存值|用户给定两位显示|
|---|---:|---:|---|
|720|-2.1167271486370858|-2.1167271486370893|-2.12%，完全相同|
|2880|-14.766762552613885|-14.766762552613883|-14.77%，完全相同|

原owning文件`results/revision-20261022/paired-comparisons.csv` SHA a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9，行2/14；新`results/revision-v9/wp3/contrasts.json` SHA576e9070644e211d417f84efba6a8b77b295be8e1f5870a5ec42aed7d7362ce4，/8和/0的relative_loss_percent。

底层保存的模型损失均值、历史参照均值、破线数和paired mean difference逐位相同。旧代码先求逐点差均值，再除参照均值；新保存百分比用两个已存均值相减再除参照均值。两式实数代数等价，binary64聚合次序不同。这里不重算score、ratio或summary，也不改任何原值。

裁定明确：用户给出的核验锚点为两位小数，本轮按该指定展示精度通过，并以底层量严格一致作额外核对；原计划额外要求的存储百分比bitwise检查仍标FAIL，不删除初始严审、不换用碰巧相等的其他旧文件、不加容差、不声称完整精度百分比逐位一致。图以原WP3保存值绘制。此解释与差异列入待用户决定，若作者要求存储百分比也逐位一致，应撤下曲线，而非修补数据。

## 导入与不导入

正文只用WP3原FX H6学习曲线全部五历史点、两方法；保留长历史收益回落，补充引用保留H24反转，不能写越长越好。补充导入WP2三条预测的全部分母/缺失/阈值/状态，P3 NOT_SUPPORT和反例不弱化。WP4统一历史图不进稿，也不另绘替代版本绕过门槛。PR5标题/摘要/主线不导入；标题仅列备选。

每一导入数字的固定来源path/SHA/JSONpointer和导入目的地由imported-number-bindings.json给出；导入副本逐字保持源，详见import-manifest.json。分项严审与补核全过程均保留在notes/v11/，无新增实验。
