# v8 WP2 主稿逐页视觉检查 A：第 1–8 页

检查日期：2026-10-24。检查范围严格限于主稿第 1–8 页；未检查第 9–17 页及 Supplement。本记录是同模型像素视觉检查，不是数学、统计或实证结果复核。未调用 Claude/Cloud，未修改主稿、图表、代码或其他文件。

## 对应文件与检查方法

- 实际主稿 PDF：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/manuscript.pdf`
- 本次直接读取上述 PDF 字节得到的 SHA256：`eec2e59fdb1134f5a502f2548cb3496d9f3a5e73d29051d9a32a77db65d812ac`
- 检查图为现有 110 dpi 渲染结果；逐张实际调用 `view_image` 查看第 01–08 页像素，未以文字提取替代视觉检查。
- 辅助阅读 `submission-jof/manuscript.tex` 的表题、图注和列名，以确认实际可见标题；没有改写或重排源文件。

## 逐页结果

### 第 1 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-01.png`

标题的两行排版、Abstract 标题与正文、Introduction 节标题、正文和页码均完整可见。字体、粗体层级与数学/百分比字符清楚；无可见缺字、黑方块、横向溢出、裁切或重叠。正文自然接到下一页。此页无表格或图。

### 第 2 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-02.png`

Figure 1 完整。纵轴刻度 48、56、64、72 为普通数字，无科学计数法偏移标记；横轴日期、Economic date (2021)、Absolute position (USD billions) 均可读。Observed absolute position 使用黑色实线和圆点，Historical headroom limit 使用灰色虚线，两者在灰度下可辨；图例不遮盖关键折线路径。图注完整，结尾明确给出 takeaway：“Endpoint containment can conceal a peak breach.” C1–C3 的粗体标签与正文清楚，页内无可见溢出、缺字或裁切。此页无表格。

### 第 3 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-03.png`

Related literature 标题、引文、正文和页码均清楚。正文行距、段距与左右边界一致；未见缺字、重叠或溢出。末段完整结束，Table 1 引用可读。此页无图表；下部留白不影响阅读。

### 第 4 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-04.png`

Table 1 在单页内完整显示，上下横线、全部文献行和底部说明均未裁切或跨页断开。列名 Study、Response、Data unit、Peak floor、Label timing、Evaluation、Source scope 均完整可读，未见列间文字覆盖。窄列存在正常断词，文字较密，但在本次渲染中仍可辨；无可见缺字。表题包括比较范围、n.r. 的解释与共同 peak-position target / validation design 的 takeaway。该页为整页浮动表，上部留白较多，未发现需要阻断交付的视觉问题。

### 第 5 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-05.png`

The forecast target 标题、两条 Proposition 标题、正文和页码清楚。展示公式中的下标、上下限、绝对值、希腊字母、条件竖线、不等号均可辨；最宽的概率不等式仍位于正文边界内。公式与段落无碰撞，未见缺字、黑方块、裁切或横向溢出。此页无图表。

### 第 6 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-06.png`

Data 与 Forecasting methods 两节标题、正文、引文、行内数学和页码完整。字形、粗细与段落间距一致；未见溢出、裁切、缺字或文字重叠。此页无图表。

### 第 7 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-07.png`

Table 2 在页内完整显示，全部九类方法行、表底线和脚注均可见，未跨页断开。列名 Method / code、Forecast definition、Executed menu / setting 完整；代码 F、S、K、QR、KNN、QR4、L 可辨。三列内换行正常，没有跨列覆盖、裁切或缺字。表题的 takeaway 为匹配历史与更新日程使参照明确；表题与脚注均可读。正文、表格与页码之间保留足够间距。表格较密，但本次渲染未见阻断性可读问题。此页无图。

### 第 8 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/manuscript/page-08.png`

Evaluation design、Research design and transparency、Results、Where conditional models improve 的标题层级清楚。行内数学、引文、正文与页码完整；未见缺字、溢出或重叠。Results 与 7.1 标题后均有正文，页底段落正常续到下一页；没有孤立标题。此页无图表。

## 范围内结论

第 1–8 页全部完成实际像素视觉查看，结论为 8 页 PASS；本范围内未发现需修复的裁切、文字重叠、缺字、断表、图轴数字或灰度辨识问题。图注 takeaway 与两张表的列名均已按可见像素检查。未据此对主稿其余页或 Supplement 作出通过结论。
