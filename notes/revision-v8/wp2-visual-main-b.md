# v8 WP2 主稿逐页视觉检查 B：仅第 9–17 页

- 检查日期：2026-10-24。
- 检查范围：主稿第 9–17 页，共 9 页；每一页均实际使用 `view_image` 查看所列 PNG 的页面像素。未检查第 1–8 页或 Supplement；未以文本提取替代视觉检查。
- 被检 PDF：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript.pdf`。
- 当前 PDF SHA256：`eec2e59fdb1134f5a502f2548cb3496d9f3a5e73d29051d9a32a77db65d812ac`。
- 该哈希与 `notes/revision-v8/wp2-rendering.json` 的主稿渲染记录一致；主稿为 17 页，现有截图以 110 dpi 渲染。
- 本次仅执行同模型视觉检查并记录问题；未做额外研究或数值分析，未调用 Claude/Cloud，未修改主稿、图表或代码。

## 逐页记录

### 第 9 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-09.png`
- 正文与页码均在版心内，未见溢出、重叠、缺字或黑色替代字符。
- Table 3 的表题、列名和五条数据行完整显示；`Period / procedure`、`Reference`、`Loss change (%)`、`Issues` 与 `Strict breaches (regression / reference)` 可读。多行单元格留在各自行内，表体与表下注释未跨页断裂。
- 表题末句 “Matched gains recur while the rolling-reference direction changes.” 完整可读。
- 本页无图或参考文献。

### 第 10 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-10.png`
- 正文衔接正常，未见溢出、断字缺失或重叠。
- Table 4 完整留在一页，四列标题 `Comparison set`、`Procedure`、`Loss change / median (%)`、`Higher-loss cells` 清晰。行内换行与表下注释均未被裁切，底线与注释相邻但不相压。
- 表题末句 “Stronger regularization narrows losses while leaving substantial failures.” 完整可读。
- 本页无图或参考文献。

### 第 11 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-11.png`
- Table 5 的 Panel A 与 Panel B 均完整显示，未发生断表、裁切或重叠。Panel A 的 `DM p`、`HLN p`、`Named adjustment / p` 可读；Panel B 的 `Grid hits`、`Grid issues`、`Kupiec p`、`Christoffersen CC p` 可读。
- Panel B 第一列较窄，`reference` 在部分行中分为 `refer-` / `ence`，属于完整可读的行内换行，未见文字丢失。
- 两块表下注释完整，末句 “The grid does not create independence.” 可读；表题末句 “A better average score does not imply fewer breaches.” 完整。
- 下部留白较大，但未造成内容溢出或页码冲突。本页无图或参考文献。

### 第 12 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-12.png`
- Figure 2 与 Figure 3 的绘图区、轴名、图例及图注均完整留在页面内，无裁切或相互重叠。
- Figure 2 横轴为 `0, 10, 20, 30, 40, 50, 60`，单位 `USD millions`；纵轴为 `0.000, 0.005, 0.010, 0.015`。Figure 3 横轴为 `25, 50, 75, 100, 125, 150, 175, 200`，单位 `USD billions`；纵轴为 `0.00, 0.02, 0.04, 0.06, 0.08`。两图均为普通数字，无科学记数乘数或偏移标记。
- `Quantile regression` 为黑色实线，`Historical headroom` 为灰色虚线；灰度和线型可区分，图例与坐标字号可读。
- Figure 2 图注最后 takeaway 完整：“Average pinball superiority does not imply dominance across elementary scores.”
- Figure 3 图注最后 takeaway 完整：“A single average-score ordering leaves other consistent-score preferences unresolved.”
- 本页无表或参考文献。

### 第 13 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-13.png`
- Table 6 的四列标题 `Frequency / history`、`Horizon`、`Evidence`、`Validation action` 清楚，所有数据行与底线完整；多行文字未跨列或互相压住。
- 表题末句 “Keep the historical rule until the named advantage survives joint validation.” 完整。
- 第 8、9 节标题与正文均正常。页末正文的 `ex-` 延续到下一页的 `ternal`；两页接续可见，未见缺字、裁切或页码相压。
- 本页无图或参考文献。

### 第 14 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-14.png`
- 上接第 13 页的 `external`，正文与 Conclusion、Data and code availability 标题层级清楚，未见溢出、缺字或重叠。
- 页末 `FX observa-` 与第 15 页首行 `tions` 衔接，分页未裁切文字。
- 本页无图、表或参考文献。

### 第 15 页 — 排版 PASS；可见内容状态记录

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-15.png`
- 页首承接上一页正文，数据和代码链接均在版心内换行，未见链接文字溢出。
- Author-provided information 区的 Author information、ORCID、Funding、Competing interests、AI statement 仍各有一处 `[TO BE COMPLETED BY AUTHOR]`，共五处。它们完整显示；这是页面可见的内容待填状态，不是本次修复项。
- References 标题与首批条目完整。长 URL、DOI 在行间断开但留在版心内；各条目没有跨页拆成孤立末行，未见缺字、黑框或裁切。
- 本页无图或表。

### 第 16 页 — 问题（轻微参考文献字距）；无阻断性排版缺陷

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-16.png`
- 参考文献条目及长链接均留在版心内，无横向溢出、文字重叠或可见缺字；页底 Meinshausen (2006) 条目完整显示。
- **轻微问题：** Gibbs & Candès (2021) 条目部分正文行的词间距明显拉大，特别是作者与标题首行、标题和刊名续行，以及 `1660–1672.` 与后续 URL 之间的间距。该条目仍可读，无裁切；建议排版修订者检查其两端对齐与 URL 断行组合。
- DOI / URL 有在 `https:` 后或域名内部换行的情况，均可见上下行连续，不构成溢出。这里仅检查视觉完整性，未核验链接访问。
- 本页无图或表。

### 第 17 页 — 问题（轻微参考文献字距）；无阻断性排版缺陷

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-17.png`
- 最后六条参考文献和页码完整，页面底部留白正常；无溢出、重叠、黑色替代字符或可见缺字。
- **轻微问题：** Wisniewski (2024) 条目的前两行词间距明显拉大，标题出现 `Implica-` / `tions` 的正常断词；下方论文机构信息和 URL 完整可读。建议排版修订者检查该条目的两端对齐与长链接断行。
- 其他条目的 URL 均留在版心内，未见参考文献条目被裁切。
- 本页无图或表。

## 范围内结论

- 已实际逐页检查主稿第 9–17 页，共 9 页。
- 未见溢出、断表、文字重叠、缺字或图轴记数法问题；Table 3–6 列名均可读，Figure 2–3 灰度线型与字号可读，图注末句完整。
- 记录两处轻微的参考文献词间距问题（第 16 页 Gibbs & Candès 2021、第 17 页 Wisniewski 2024），以及第 15 页五处作者信息占位符的可见状态。未自行修复。
- 此结论仅覆盖视觉排版，不代表对内容、数值、引用事实、链接有效性、独立验证或整个投稿包的验收。
