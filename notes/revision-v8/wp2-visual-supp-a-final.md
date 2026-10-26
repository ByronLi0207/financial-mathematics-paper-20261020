# v8 WP2 Supplement 最终逐页视觉检查 A（第 1–10 页）

- 检查对象：`submission-jof/supplement.pdf`；本次任务说明为 21 页，本记录仅覆盖实际查看的第 1–10 页。
- PDF SHA256（本次检查读取）：`77d950417642f466ca6e9f779d552ba825a8fc4a2111e9050173a44df06328ca`。
- 方法：实际逐页使用 `view_image` 查看最终 PNG；未以文本提取代替视觉检查，未新增计算，未修改 PDF、源文件、结果或旧检查记录。
- 截图目录：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/`。
- 本记录的 PASS 指本范围内的版面和像素检查通过，不表示重新核对了数值或分子分母。

| PDF 页 | 结论 | 实际视觉所见 | 截图路径 |
|---|---|---|---|
| 1 | PASS | 标题、S1、命题、公式、证明与页末正文均清楚，无缺失字形、覆盖、裁切或越界。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-01.png` |
| 2 | PASS | S1 Takeaway、S2 命题与证明均正常；公式、上下标和页末续接正文可读，无重叠或缺字。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-02.png` |
| 3 | PASS，附分页观察 | Table S1 caption、描述性列头、数据和表后解释段可读。Table S2 仍在页底显示 caption、列头和第一行，余行续至第 4 页；无行裁切，续页已补表号（见下一页）。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-03.png` |
| 4 | PASS；原续表标识问题已解决 | 顶部明确显示 “Table S2: Continued.”，下方重复完整列头。数据与横线完整，未发生 caption/表头/表体重叠。S5 和 Table S3 可读；表后解释段整体移至下一页，无裁切。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-04.png` |
| 5 | PASS | 页首正常承接 Table S3 解释段。Table S4 与 S5 的 caption、两行描述性列头和全部数据均可读；科学计数 p 值无覆盖或越界，底部解释段完整。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-05.png` |
| 6 | PASS | Table S6 的 Mean fitted phi、Replay vs translated (%)、Replay vs regression (%)、Breaches replay/translated 拆行表头仍可读，无相撞或溢出。S8、Table S7 caption、列头与前三行清楚，余行续至第 7 页且无裁切。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-06.png` |
| 7 | PASS；续表标识与分数字号问题已解决 | 页首明确显示 “Table S7: Continued.” 并重复完整列头。Table S8 的两处长精确分数字号明显增大，与相邻表内数字接近；分数线和分子/分母可辨，无跨单元格覆盖、越界或裁切。描述性表头和表后说明段可读。S10 标题现移至下一页，未留下孤立标题。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-07.png` |
| 8 | PASS；长分数可读性已改善 | S10 标题、引言、Table S9 caption 与 5 列列头完整。长精确分数已明显放大；分子、分母和分数线可辨，行高随之增加，未见字符覆盖或越界。Table S9 本页未完，续至第 9 页；页底行无裁切。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-08.png` |
| 9 | PASS，附分页观察 | 顶部明确显示 “Table S9: Continued.” 和完整列头，剩余表体及底线完整。续页开头的 Task 单元格为空，是上一页 Bills full H6/W260 组的延续；表号和列头可保持识别。下半页 S11、Table S10 caption、列头及数据可读，长分数放大后无重叠。页底仅放 FX sparse H24/W720 组首行，其余续至第 10 页，属于较碎的组内分页，但无丢表题、断行或截断。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-09.png` |
| 10 | PASS；原续表标识问题已解决 | 顶部明确显示 “Table S10: Continued.” 和完整列头。页首正常承接 FX sparse H24/W720，后续各组分数、标签、Minimizers 换行和表底线完整。长分数可辨，无重叠、缺字、裁切或越界。FX sparse H24/W2880、Bills sparse H24/W260 的长 Task 标签仍拆为两行，字间距较大但可辨。 | `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-10.png` |

## 最终结论（仅第 1–10 页）

- 旧检查指出的缺少续表表号问题已解决：本范围续页均出现正确的 “Table Sx: Continued.”，并保留列头。
- 长精确分数字号问题已改善：Table S8–S10 中长分子分母明显放大，未发现放大引入的重叠、裁切或越界。
- 第 6 页目标描述性表头继续通过。
- 新分页使 Table S9 跨第 8–9 页、Table S10 跨第 9–10 页；续表表号和列头完整，未发现新增阻断性分页问题。Table S2 在第 3 页仅有首行、Table S10 的 FX sparse H24/W720 组在第 9 页仅有首行，作为非阻断性分页观察保留。
- 本次只写本记录；旧记录保留。
