# G7 全文通读与逐项修改记录

从主文第一页至参考文献末尾完成逐段审读；不是把自动词数检查当作通读。82个索引记录覆盖主文全部段落（部分定义/结论索引有重叠，报告明确标出，不因此删除原文）。每条记录分别判断主张、证据、含义、过渡、术语和语法。结构性引导句/定义段不强行添加不存在的实验数字。

- 前半部45记录：`G7-review-sections1-6.md/.json`。
- 后半部37记录：`G7-review-sections7-end.md/.json`，另覆盖新增补充文字、图表注、数据/代码信息、作者占位符和参考文献。
- 最终引文和首次引用编号核对：`G7-reference-census.md/.json`及后续最终aux核对报告。
- 原写法口径与最终口径均使用未改动的v9检测器。原6.7265%保守措辞、16.5874词/句、0个超过40词；G7最终7.5556%、16.7822词/句、0个超过40词。摘要161词、8个数字。旧检测器的5个forbidden命中是合法的Supplement S1–S3指向，不是T1/T2/T3内部代号；不改检测器，不删除正确引用以迎合旧计数。

## 主张与证据修正

1. 匹配历史和更新日程写成保持标签池和时钟一致，避免声称隔离出了纯条件特征的因果效果。
2. 无限收缩明确为零斜率和约定的下侧普通经验分位数；整数秩情况下不声称截距最小值唯一。
3. 既有一标准误选参法与本轮赢家对历史规则的HAC证据闸门明确区分。
4. 把分解的选择分量表述精确为27/41格超过正超额损失的一半，避免把不同分量中位数相加。
5. RP的零中位数明确与32/60次保留历史规则相关；8/60及最差损失、失败尾部标准均保留。
6. Murphy曲线交叉指Figures S2–S3；20.6:1反转另指Section S9/Table S8；日聚合结果指Section S25。
7. 主文早期图表引用改成所属节引用，恢复Tables1–8和Figures1–6的首次引用顺序；补充逐项补齐科学语境内的就近引用。
8. six-point与早期five-finite菜单区分，34/48原始比较的计数不被后来实验替换。

## 排版、版本和术语

- 两个可见跨行表头以及续表模板中遗漏的Unused allowance改为Mean overprediction；所有数值行不动。
- figure-legends同步实际六张主文图注。
- 标题页代码链接改为v13，五个作者占位符逐个保留；AUTHOR-TODO更新当前版本与失败结论，不篡改历史v12设计发布时间。
- REPRODUCING补任务所称CFTC Table5与实际Table6的映射，已验证的复现命令正文不变。
- tail段前排空浮动表格，避免Table7插在跨页半词之间；压缩重复的tail说明、表7注和7.5节文字，完整保留判断和证据，消除成本段落的孤页。
- recorded-calendar用语替代source-naive，不虚构时区或交易收盘。

## 精确逐处差异与审阅底稿

以下机器可读记录保存原文、改文和原因，是本日志的一部分（未修改任何研究结果）：
- `G7-evidence-edits.json`
- `G7-float-layout-edit.json`
- `G7-orphan-cost-edit.json`
- `G7-package-reference-edits.json`
- `G7-root-edits.json`
- `G7-score-paragraph-edit.json`
- `G7-supp-header-edit.json`
- `G7-supp-reference-edits.json`
- `G7-terminology-and-metadata-edits.json`
- `G7-validation-note-edit.json`

所有最终页的直接视觉验收单独记录在G8视觉报告，不把这次源通读冒称为最终PDF验收。
