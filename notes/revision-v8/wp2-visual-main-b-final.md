# v8 WP2 最终主稿逐页视觉复检 B：仅第 9–17 页

- 检查日期：2026-10-24。
- 检查范围：最终主稿第 9–17 页，共 9 页。每一页均再次实际调用 `view_image` 查看 `.scratch/revision-v8/wp2/render-final/manuscript/` 下的页面像素；未以旧截图或文本提取代替。
- 被检 PDF：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript.pdf`。
- 当前 PDF SHA256：`41b7dde4bc7ee5de58c7ee7cd78f9c6173063d929035080461f7ec5b7d6774f1`。
- 哈希与 `notes/revision-v8/wp2-rendering-final.json` 中主稿渲染记录一致；该记录为 17 页、110 dpi。
- 本次只记录视觉结果；未改 source、代码或图表，未覆盖旧记录 `notes/revision-v8/wp2-visual-main-b.md`，未调用 Claude/Cloud，未做数值或引用事实分析。

## 逐页记录

### 第 9 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-09.png`
- 正文、Table 3、表下注释及页码均完整，未见溢出、断表、缺字或重叠。
- 五个列名完整可读，多行数据单元格没有跨列相压；表题末句 “Matched gains recur while the rolling-reference direction changes.” 完整。

### 第 10 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-10.png`
- 更新后的 Table 4 caption 完整显示，首句为 “Weekly evidence across the original primary, added panel and earlier-period comparisons.”，末句为 “Stronger regularization narrows losses while leaving substantial failures.”。
- 表体、四列列名及表下注释清楚，未见改 caption 后产生挤压、断表、裁切或正文重叠。

### 第 11 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-11.png`
- Table 5 的 Panel A / B、列名及两处表下注释均完整可读，无断表或跨列相压。
- Panel A 中显示的补零 p 值（如 `2.20e-07`、`4.39e-07`、`0.320`）完整留在相应单元格内；此处仅记录视觉呈现，不判断数学值保持性。
- Panel B 第一列的 `reference` 仍以正常断词换行显示，无缺字。表题末句与末条注释均完整。

### 第 12 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-12.png`
- Figure 2 / 3 的绘图区、坐标、轴名、图例及图注完整，字号清楚，未见裁切、重叠。
- Figure 2 横轴 `0–60`、纵轴 `0.000–0.015`；Figure 3 横轴 `25–200`、纵轴 `0.00–0.08`，均使用普通数字，没有科学记数乘数或偏移量。
- 黑色实线 Quantile regression 与灰色虚线 Historical headroom 可区分。
- Figure 2 最后 takeaway 完整：“Average pinball superiority does not imply dominance across elementary scores.”
- Figure 3 最后 takeaway 完整：“A single average-score ordering leaves other consistent-score preferences unresolved.”

### 第 13 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-13.png`
- Table 6 四列列名与所有行完整，列间未相压，表底线清楚；caption 最后 takeaway 完整。
- 第 8、9 节标题及正文正常。页末 `ex-` 与下一页 `ternal` 连续，未见页脚相压或内容裁切。

### 第 14 页 — PASS

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-14.png`
- 正文、Conclusion 与 Data and code availability 标题完整，页边和页脚正常，无溢出、缺字或重叠。
- 页末 `observa-` 与下一页 `tions` 衔接正常；本页无图表或参考文献。

### 第 15 页 — 排版 PASS；作者信息待填状态仍可见

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-15.png`
- 数据/代码链接、作者信息区与 References 标题完整，无横向溢出。
- 参考文献左对齐后字距自然，长 URL / DOI 完整留在版心内，条目没有裁切或重叠。
- Author information、ORCID、Funding、Competing interests、AI statement 五项仍各有一处 `[TO BE COMPLETED BY AUTHOR]`，完整可见；仅保留该内容状态记录。

### 第 16 页 — PASS；旧词距问题已消失

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-16.png`
- Gibbs & Candès (2021) 条目的作者、标题、刊名及 URL 字距自然；旧记录所指出的拉大词距已在当前像素中消失。
- 所有可见参考文献保持左对齐与悬挂缩进；长链接在版心内换行，无溢出、裁切、重叠或可见缺字。
- 页底 McNeil & Frey (2000) 条目完整；Meinshausen (2006) 现完整移至第 17 页，未出现条目跨页截断。

### 第 17 页 — PASS；旧词距问题已消失

- 截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/manuscript/page-17.png`
- Wisniewski (2024) 条目的标题与机构行字距自然，旧记录所指出的拉大词距已消失；URL 在版心内换行，尾部完整。
- 页首 Meinshausen (2006) 及其余六条参考文献均完整，悬挂缩进一致，无可见缺字、裁切、重叠或横向溢出；页码完整。

## 范围内结果

最终主稿第 9–17 页共 9 页视觉 PASS。第 16 / 17 页两处旧参考文献词距问题已解决；第 9–14 页表图布局未见新问题。第 15 页五项作者信息占位符仍可见，其状态与排版验收分开记录。

本记录仅覆盖上述 9 页视觉排版，不代表第 1–8 页、Supplement、引用事实、数值保持性、链接有效性或整体投稿包验收。
