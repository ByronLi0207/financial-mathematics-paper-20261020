# v8 WP2 Supplement 逐页视觉检查 A（第 1–10 页）

- 检查对象：`submission-jof/supplement.pdf`，共 20 页；本记录只覆盖第 1–10 页。
- PDF SHA256（本次检查读取）：`1ac58b5c47581367beb58356f88c6dae91d08b3d1b97553aa674376991053bfd`。
- 方法：实际逐页使用 `view_image` 查看现有 PNG；未用文本提取代替视觉检查；未重新计算、未改源文件或结果。
- 截图目录：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/`。

| PDF 页 | 结论 | 实际视觉所见 | 截图路径 |
|---|---|---|---|
| 1 | PASS | 标题、S1 标题、命题、公式和证明均可读；未见字形缺失、重叠、越界。正文在页末正常续接。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-01.png` |
| 2 | PASS | S1 Takeaway、S2 命题及证明版面正常；公式、上下标、概率符号可见，无裁切。正文页末续接。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-02.png` |
| 3 | 问题：续表分页标识（见第 4 页） | S3、Table S1 新描述性列头均可读，概率保留 5 位小数，表后解释段可读。Table S2 的 caption、列头和仅第一行放在本页底部，其余在第 4 页；首行无裁切。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-03.png` |
| 4 | 问题：缺少续表表号/标题 | 顶部 Table S2 续表重复了完整列头，数据与横线完整，但未重复 “Table S2” 或 “continued” 标识，单独看本页无法由标题确认所属表。S5、Table S3 caption、描述性列头、数据与表后正文均可读。概率精度一致，未见重叠或越界。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-04.png` |
| 5 | PASS | Table S4 的两行描述性列头（Endpoint vs historical/regression、Breaches endpoint/historical）可读，列间未相撞。Table S5 的 DM/HLN/Holm 列和科学计数 p 值可读；两表 caption 与后续解释段完整，无裁切、缺字或跨页表体。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-05.png` |
| 6 | 问题：Table S7 跨页标识（见第 7 页）；Table S6 表头 PASS | Table S6 的 Mean fitted phi、Replay vs translated (%)、Replay vs regression (%)、Breaches replay/translated 均成功拆行，可读且不重叠；全部 8 行、表下注释/解释段完整。S8、Table S7 caption 和列头可读，但本页仅放前三行，余行续至第 7 页。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-06.png` |
| 7 | 问题：续表表号缺失；精确分数偏小 | 顶部 Table S7 续表列头完整、表体无裁切，但未重复 Table S7/continued 标识。Table S8 的新多行描述性列头可读、未重叠；Equal-loss weight ratio 列的精确分数比相邻数值明显小且密集，需要放大阅读，未见越出单元格。Table S8 caption 和表后 takeaway/说明段可读。S10 标题及引言完整。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-07.png` |
| 8 | 问题：精确分数可读性 | Table S9 完整置于一页，caption、5 列表头、首尾横线均完整。Left/point a 与 Right a 列的精确有理数分子/分母字号明显小于普通正文和邻列，行间密集，整页视图难以直接读出长整数，需放大；未见明显字符互相覆盖、越界、缺失或截断。Minimizers 多方法项正常换行。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-08.png` |
| 9 | 问题：精确分数可读性；续表分页标识（见第 10 页） | S11、Table S10 caption 和列头可读。精确分数与第 8 页一样明显偏小、密集，需要放大；未见裁切或重叠。较长 Task 标签（FX sparse H24/W2880）拆成两行且第一行字间距大，仍可辨。Table S10 在本页未完，续至第 10 页。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-09.png` |
| 10 | 问题：缺少续表表号/标题；其他 PASS | 顶部 Table S10 续表重复列头但无 Table S10/continued 标识；最前两行的 Task 单元格为空，是上一页同一组的延续，单页识别较弱。精确分数小但无越界或覆盖。S12、Table S11 caption、描述性表头和本页全部行可读；数值/百分比/次数斜线分隔清楚，表格未裁断，未见缺字。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render/supplement/page-10.png` |

## 汇总

- 第 6 页目标长列名拆行在像素上通过：无重叠、溢出或裁切。
- 第 1–10 页未发现缺失字形、表头覆盖数据或越出页边界。
- 待主代理判断的视觉问题：Table S2、S7、S10 跨页后缺少表号/continued 标识；Table S8–S10 精确有理数显示明显小于邻列，需要放大阅读。此处只记录现象，未修改。
