# v8 WP2 最终 Supplement 像素视觉检查 B：第 11–16 页

检查日期：2026-10-24。范围严格限于最终 Supplement 第 11–16 页，共 6 页；当前 Supplement 为 21 页，本记录不覆盖其他页。逐页实际调用 `view_image` 查看指定 `render-final` PNG 像素；未使用文字提取替代视觉检查，未运行数学、统计或实证分析。仅新增本文件，未覆盖旧 QA，未修改任何源文件，未调用 Claude/Cloud。

## 文件与字节标识

- 当前实际 PDF：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/submission-jof/supplement.pdf`
- 本次直接读取该 PDF 当前字节得到的 SHA256：`77d950417642f466ca6e9f779d552ba825a8fc4a2111e9050173a44df06328ca`
- 本次只检查现有最终渲染图，不重新编译或重渲染。

## 第 11 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-11.png`

S12 标题、正文与 S13 标题完整。Table S11 的首半面板完整容于单页，表头和底线可见；Series、Horizon / history、Historical loss / breaches、Original regression % / hits、Four-predictor regression % / hits、Expanded-menu regression % / hits、Empirical % / breaches 的层级与列边界可辨。全部数据行未见覆盖或裁切。字体较小且行密，但当前像素中可辨；未见缺字、黑方块或横向溢出。表题的 takeaway 可见。

## 第 12 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-12.png`

Table S12 标题、描述性表头、后半面板全部行和底线完整。较长 Series 名分成两行，但未覆盖相邻列或行。正文与 S14 标题留有清楚间距。Table S13 在本页开始，标题、Horizon 6 / history 52、Horizon 6 / history 260、Horizon 24 / history 52、Horizon 24 / history 260 及前四个数据行可见；该长表在页底正常断页，未被裁切或压到页码。表题含“Fewer breaches do not guarantee a better score.”，可读。

## 第 13 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-13.png`

页顶续表标题实际显示为 `Table S13: Continued.`，与第 12 页起始表的 S13 号一致。重复列名完整，剩余八个 Series 行与底线清楚；无续表号跳变、漏表头或表格截断。S15 标题与正文正常。Table S14 在本页开始，描述性列名 Series、Horizon / history、Minimum-loss rule (%)、One-SE rule (%)、Breaches minimum-loss / one-SE、Historical breaches 均可辨，列间未相撞。表题与本页首段数据未见缺字或溢出。

## 第 14 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-14.png`

页顶实际显示 `Table S14: Continued.`，与第 13 页起始表号一致；表头重复完整，其余数据行与底线清楚，无列间覆盖、缺字或裁切。S16 标题、正文、Table S15 的标题与全部四行完整。Table S15 的 Phase、Series、Horizon / history、Rule、Status 列名可辨；两列紧凑但未重叠。`REQUIRED_VALIDATION_CANDIDATE_FAILED` 的正文等宽字符完整。页面正文与页码未发生碰撞。

## 第 15 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-15.png`

S17 标题和正文完整。Table S16 的 Source、Horizon / history、Method、Mean loss、Breaches、Status 列名可辨，整张表和底线均在页内。长数值与 COMPLETE / NA 状态文字未覆盖相邻列，未见缺字或裁切。表题中 two long-horizon wrapper cells remain unavailable 的 takeaway 清楚。表后说明与 S18 标题、后续段落均完整，页面边界正常。

## 第 16 页 — PASS

截图：`/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/.scratch/revision-v8/wp2/render-final/supplement/page-16.png`

Table S17 的标题、八个数据行、底线与 NA 行完整。Source、Horizon / history、Regression vs historical (%)、Breaches regression / historical、Regression adjustment、Historical adjustment 均使用描述性列名，可辨且没有交叠；小数、负号和斜线可见。表题的 takeaway 清楚。S19 标题与正文完整。Table S18 在本页开始，Source、Horizon / history、Rule、vs historical (%)、vs regression (%)、Breaches 列名完整；本页所示数据行正常排至长表断页边界，未压到页码。第 17 页续表不在本次检查范围内。

## 范围内结论

6 页均已实际查看像素，均为 PASS；本范围未发现需要修复的缺字、裁切、文字重叠、列名碰撞或续表表号问题。已实际核对 Table S13（第 12→13 页）与 Table S14（第 13→14 页）的续表号及重复表头。

本页段没有图，也没有长显示分数或可见 `dfrac` 分式；图轴/灰度与长显示分数检查在本范围记为不适用，未据此对其他页的长分数给出通过结论。表内的 Horizon / history 和 breaches 斜线是可见文字表达，并未作为长分数检查的替代。原始数字是否变化不属于本次像素 QA 的分析范围。
