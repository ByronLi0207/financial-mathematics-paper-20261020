# C4 Supplement 布局与保留核对

**C4 中间稿；C7 仍须对最终投稿包重新编译及逐页复检。**

本子任务只编辑 `submission-jof/supplement.tex`，并新增本记录。表格字面值、native bindings 和 legacy 导入由 numbers 代理负责。未修改主文、原五个 generated/v8 文件、研究代码或旧目录；未运行金融拟合、预测、诊断或模拟，未提交。

## 1. 交付与固定快照

- source：`submission-jof/supplement.tex`，96,698 bytes，SHA256 `65b8ca7cb427c225a33d9ca2f52dcfecc62fcf22e5958065000455705ee14c22`。
- 编译产物：`.scratch/v9/c4-supp-build/supplement.pdf`，**28 页**，211,757 bytes，SHA256 `68224f16a88934c1ab084c8f6ed2316c64a8420b79db8a01035f66b3e9a043f3`。
- 最终渲染：`.scratch/v9/c4-supp-render-final/`，28 张 125 dpi PNG；每页路径和完整 SHA256 见 `.scratch/v9/c4-supp-build/visual-manifest.json`（SHA256 `41a6cbde0f060cf0ad2d3b04d625f6857cc499032fa0ea9df7059a960adcdf36`）。
- 编译命令：`/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic -X compile submission-jof/supplement.tex --outdir .scratch/v9/c4-supp-build --keep-logs`。终编成功，无 overfull hbox、无未定义引用。仍有长方法标签、表注等的 underfull hbox 警告，已目视核对。

## 2. 原内容保留 check

- 初始 P5 源 90,602 bytes，SHA256 `2fb0b5fee233265cfdd968282beba43143b1a8fa92cbf62a81e090c941d5a3db`；原 PDF 30 页。源和初始清单保存在 `.scratch/v9/c4-supp-baseline/`。
- 原 28 个 section label 全部按原顺序保留。两个证明 section 从地板标题至原增量模拟标题前逐字节一致。
- 原源码 370 条含数字表行（含两条数字表头）逐字、按原顺序一致。负号、FAILED、NA 和原数值未改变。
- 原五个 generated/v8 表 SHA256 全部一致，完整两个 72 行 MC grid、daily、三窗口和 full-prefix 所有行均保留。只在输入处把两张 72 行 MC 表的字号恢复至 9pt，不改生成文件。
- 原 endpoint、AR replay、ranks、exact preference frontiers、weekly panel、保守选参/失败、ACI/SAV、组合/Murphy、状态、target-level NA、coherence/late hit 和实现说明均保留。P5 三扩展的 MISMATCH、daily 例外、backcast 重叠/后选惩罚/长 H 反例均保留。
- 唯一撤去的原展示是四特征 MC 热图 `fig:v8-mc-four`。两个完整 72 行数表未删，原全部六个 heatmap 与归档指向仍保留；正文加句明确数表完整。

|原 generated/v8 文件|保持的 SHA256|
|---|---|
|`v8-mc-full-table.tex`|`7a80f05d7d423c623fe39b185590c6535edbc57558366668f26103e453cafd2b`|
|`v8-mc-four-table.tex`|`9409a1d8061d5c05fc529c220ecaa5121c33f6bbf0818c50ef0ea05dd9597a10`|
|`v8-daily-results-table.tex`|`0da2b37ccb530e5d66e126a14f491a684d9046e882241e51ac85f0244d8ef8f3`|
|`v8-three-window-table.tex`|`fd6c41975331b318ebe54ccd836680fcda6d2aef07e54f6820ccca673c4d42b8`|
|`v8-backcast-complete-table.tex`|`67e2f15a25fa08a6d22afc49acab0d028664a8ed38beb5ae25121cf5490e4d83`|

## 3. 新增完整 grid 和方法边界

- `sup:v9-legacy-mc` 独立成节，输入 `v9-legacy-simulation-table.tex`：24 个计划格，含 QR median/IQR/win、I 和 oracle 相对分数、F/I/QR/oracle hits、infinity 选择频率；同文件另有 7 条 D1 失败的 rep/stage/lambda/reason。D0 采用指定准确名称。原 17 complete/7 failed 保留，不以 partial repetitions 填统计量。
- `sup:v9-stability` 独立成节：15 条 diagnostics；W52/W260 各 26 行，每行同时列两种 QR，合计 104 个 conditional cells；另有 52 行 F benchmark。五个生成文件共 150 个 native row bindings（24+7+15+26+26+52），由 numbers 代理逐行回读；本子任务只 input 和目视。
- 旧 MC 新表全部指向 v9 导入的 `results/v9/legacy-calibrated/`，未用旧 24 格替换 P5 网格。技术参数、hour shapes 和完整流程链接导入协议/公开 archive，不把数万回执逐份展开到 PDF。
- 方法保留：999-path plug-in bootstrap 与 p 公式、finite4 gate 的精确资格、无 exact finite-sample size 保证；描述性最多两 cut、最短 segment 约束和 penalty；wholeSD 不 demean、first target lag 连续、一次约束拟合且无 retry；switch 状态连续、last-to-first 人工 wrap、各 arm 自己的 t 变换、k0 同路径。
- 区分旧校准 median/IQR、P5 ratio of across-repetition means/MCSE、C2 source median 后 equal-weight source median，不拼分母。daily NONREGULAR_NULL、hourly GARCH_OPTIMIZATION_FAILED、W260 两条 FAIL 31/32 和未归档 hourly break dates 均明确。N1 只为原 screen 支持，N2/N4 不可评估、N3 不支持；未把 instability 写成必要原因。

## 4. 布局迭代与未采用方案

- 采用标准 10pt A4、20mm 边距；原 scriptsize 在 10pt 文档内改 footnotesize，使原 8pt 表保持可见字号。新表 9pt，两张 P5 72 行表单独 9pt。
- 缩小段落/标题和 longtable 前后留白，caption 使用全栏宽。保留自然换行，不按结果删行。
- 原三处 arraystretch 2.50 试压至 1.10 的 v1/v3 使 display fractions 相撞，这些版本未采用且全部保留。最终三表恢复 2.50，完整精确分子/分母和显示字号不变。
- v1 至 v7 均在 `.scratch/v9/c4-supp-build-v1` 至 `-v7` 独立保存。v5 原证据紧排 24 页；全表首编 v6 为 28 页；20mm 版 v7 为 27 页；恢复 P5 MC 9pt 后终编 28 页。
- 终编最初有复现说明五行落在第 28 页。在 S30 前加标准 clearpage，使完整 S30 独立在第 28 页，页数仍 28。原终编目录覆盖前完整复制至 `.scratch/v9/retained-backups/c4-supp-build-before-tail-pagebreak.bak/`。
- 最后一改后重新渲染全部 28 页：1–26 页 PNG 与前版逐字节相同（前版已逐页打开），27/28 页再次打开。因此以下每页都有实际图像检查依据。

## 5. 逐页视觉 manifest

全部页未见裁切、相撞、黑块缺字或不可读数表；续表保留表头。小表续页如 S8/S17 仍采用正常 continued 格式，没有空白页或孤立正文标题。最后一页为完整 S30，而非五行孤尾。逐页 PNG 完整哈希在上述 JSON。

|页|本轮目视观察|
|---:|---|
|1|标题、导言和地板证明；完整在页内。|
|2|经典界证明与原增量模拟；公式、首表可读。|
|3|修正主模拟与次级敏感性；两完整长表无相撞。|
|4|次级模拟尾段、全部 endpoint 对照与 AR 方法；无裁切。|
|5|AR 结果、rank ablation 和偏好表起始；续页标识清楚。|
|6|偏好表续页与完整 frontier 起始；精确分式可区分。|
|7|full frontier 续页；分子分母、方法标签可读。|
|8|full frontier 尾与 sparse frontier 起始；无数据裁切。|
|9|sparse frontier 续页；分式和并列 minimizers 可读。|
|10|sparse frontier 尾和 weekly panel 定义；正文正常续页。|
|11|weekly panel 两半；全部正负值可读。|
|12|weekly panel 尾、endpoint panel、选参方法；无叠字。|
|13|保守选参全表与 FAILED 库存；失败字样完整。|
|14|ACI/SAV 全表、NA 和 wrapper 比较起始；无缺字。|
|15|wrapper NA 续行、组合比较及统计；NA 未隐藏。|
|16|Murphy 组合、状态组与诊断；密表可读。|
|17|target-level NA、coherence、late hits 和实现方法；公式完整。|
|18|数值实现和受控 MC 方法；底部展示公式未裁切。|
|19|P5 全回归 72 行网格起始；9pt，表头与数值可读。|
|20|P5 全回归网格尾与四特征 72 行网格起始；9pt，无挤压。|
|21|P5 四特征网格尾、候选失败说明和日频定义；无重叠。|
|22|同记录日频完整表、重叠 backcast 与三窗口表；不利行保留。|
|23|完整 backcast 表、旧校准设计和 24 格表起始；13 列 9pt 可读。|
|24|旧 24 格续页、七失败表、C2 方法和诊断起始；reason 全词不越界。|
|25|诊断续页和 W52 全部来源/两 arm/两 QR；daily/hourly 不可用状态可见。|
|26|W260 全部条件格和 F 表起始；两个 QR33 FAIL 31/32 明示。|
|27|F52 格续页与解释；尾段完整，独立 S30 前留白正常。|
|28|S30 完整复现与可用性说明；不再只有上版五行孤尾。|

## 6. 核读依据与交接

- 当前 Supplement 源、五个 generated/v8 完整字节与五个 generated/v9 完整字节；`v9-table-bindings.json` 结构和 numbers 完备性通知；`results/v9/legacy-calibrated/README.md`。
- `protocol/v9/nonstationarity-design.md`、`notes/v9/c2-results.md`、`notes/v9/thesis.md`、`notes/v9/two-v8-inventory.md`。
- 只读旧 v8 的 `notes/v8/mc-supplement.tex`、`protocol/v8/mc-design.md`、`notes/v8/numerical-failures.md`，核旧设计和失败含义。原字节导入与新表字段归 numbers 代理。
- 原 v8 Supplement builder 开头与末次 console 的原行保留口径；现版本全部保留结论以本轮直接比较为准。
- C7 须基于最终主文/补充材料重新构建、检查链接/数字绑定、逐页视觉复检。本记录不是最终投稿包验收。
