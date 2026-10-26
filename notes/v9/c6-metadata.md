# C6 cover letter 与结构化参考文献元数据核对

任务基点：C5 提交 `310ff88`。本子任务只编辑 `submission-jof/cover-letter.md`、`submission-jof/references.bib`，exclusive 新增本记录；未提交。没有拟合、诊断、预测、模拟、新研究分析或外部元数据检索。README、snapshots、ZIP、title page、论文与归档均不由本子任务编辑；这些对象的并行 C6 交付由主任务负责。

## Cover letter

- 第一实质段为一句主要发现：匹配 FX 收益在两个时期出现，低频历史规则通常占优，平稳控制也能产生大的短历史回归损失。
- 第二实质段说明 Journal of Forecasting 适配：共同 path-dependent response、completed labels、matched controls 及 score/breach 联合比较；既有方法不被写成新估计法。
- 随后保留一个 FX 做市商、相关周度类别、同记录日频/回顾性回溯、不同模拟设计、真实机制未识别、失败/不可用结果与数据再分发边界。
- 保留唯一签名 `[TO BE COMPLETED BY AUTHOR]`；未填作者身份或代作者确认声明。
- 可见英文词数 **211**：去掉 Markdown URL target 后，按 `[A-Za-z]+(?:[-–’'][A-Za-z]+)*` 计词，连字符词计一个；数字百分比不计作英文词。
- **一页要求待 native 编排验收**：本子任务没有把词数当页数证明；主任务将实际排版并检查 ≤1 页。没有修改/生成 letter PDF 或 TeX。

## 两条新增 bibliography entries

只追加 `hansen1992` 与 `hastie2009`，原 29 条记录字节前缀保持不变。元数据以当前 `submission-jof/manuscript.tex` 已打印且此前核过的两条参考文献为直接依据；没有新增文献、改正文或作本轮独立外部核验。

|Key|匹配正文已印条目的字段|
|---|---|
|`hansen1992`|Hansen, B. E.; 1992; Testing for parameter instability in linear models; Journal of Policy Modeling 14(4), 517–533; DOI `10.1016/0161-8938(92)90019-9`。|
|`hastie2009`|Hastie, T.; Tibshirani, R.; Friedman, J.; 2009; The elements of statistical learning: Data mining, inference, and prediction; second edition; Springer; DOI `10.1007/978-0-387-84858-7`。|

实际键集合检查：**31 个 BibTeX 唯一键 = 31 个主文 citation keys = 31 个 printed bibliography keys**；没有缺项或重复键。两 DOI 与正文已经打印的 URL 字面值相同。结构化 `edition = {2}` 对应主文 “2nd ed.”。

## Keywords、running title 与个人声明占位

|对象|实际核查|处置|
|---|---|---|
|Keywords|6 个：Peak net positions; Quantile forecasting; Historical benchmarks; Forecast comparison; Calibration; Dealer positions。|保留；未修改正文。|
|Running title|`Historical Rules and Peak Limits`，32 个字符（含空格）。|保留；满足当前 dated requirements 记录的 <40 字符口径。|
|主文个人占位|5：Author information、ORCID、Funding、Competing interests、AI statement。|全部保留。|
|Title page 个人占位|6：Authors/affiliations、Corresponding author/contact、ORCID、Funding、Conflict of interest、AI statement。|全部保留；主任务只可能统一代码链接。|
|Cover letter 签名占位|1。|保留。|
|合计|**12 个源位置**（含跨文件重复声明，并非 12 个不同作者字段）。|未代作者填写或确认。|

`journal-requirements.md` 是 2026-10-23 的 dated receipt；本轮没有把该日期升级为新政策核查。文档中的要求说明/示例 placeholder 不计为新增作者填写位置。最终 C6/C7 仍需由主任务核对所有实际产物、快照和源包，不能据本 note 认定 ZIP 或公开发布通过。

## 本子任务实际验证及字节凭据

- 第一实质段一完整句检查通过；letter 签名占位仍为 1。
- 原 bibliography 10149 bytes 的前缀逐字节保留；原 SHA256=`3e02559cce9fc22c796a4f9a2a4e1b590020a451c983b8ae447728fed79250d5`。
- 写入期间只读保护检查：README、main/supplement、title page、两个 content JSON、ZIP、journal requirements、AUTHOR-TODO 均未由本次写入改变（并行主任务可随后更新其自己拥有的文件）。
- 修改前 letter SHA256=`3c7c88356d3bf4feaf8854eaddbacdcbe22951bd80008075cc1509f7f2b05b7f`。
- 当前 letter：1725 bytes，SHA256=`e84ade50ff8c030679397a01115d598d9686fc2650aa8b65029e6067041189fb`。
- 当前 bibliography：10796 bytes，SHA256=`678a090615eaefae1c29781b2a2eee6340cd0dff3c30b1fa2f64913a21546d6a`。

## Root native/package acceptance (C6)

Cover letter compiled with native TeX to exactly1page and its sole page was rendered/opened; source `submission-jof/cover-letter.tex` is derived from the checked Markdown. Its repeated signature placeholder is the same unfilled field, not an additional author declaration. Main/Supp/title native outputs are17/28/1pages with equal preview aliases. Current JSON snapshots match the saved TeX and10recursive generated inputs exactly. ZIP has23members and passes CRC plus byte comparison of every member; numeric binding is `main-number-audit-c6-final.json`. C7 will independently compile the ZIP, inspect every final page, run the full suite and verify actual publication. No journal submission.
