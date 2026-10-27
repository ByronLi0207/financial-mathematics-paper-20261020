# ASMBI 定稿与清理：R8 阻塞状态报告

截至 2026-10-27T10:48:14.286080+00:00。这是本地检查点报告，任务未完成，不代表已达到“作者补完信息就能投 ASMBI”。目标约八小时；本轮实际尚未用满，不能把目标时长写成完成工时。

## 1. 一句话结论

写法和排版已完成，数字来源、编译与逐页检查已通过；全套 pytest 因本机缺少既有依赖未能启动，且任务禁止安装软件，因此 R8 未通过，GitHub 发布和本地清理未开始。

## 2. 合规与实际用时

所有执行命令、原始 stdout/stderr 与退出码均在根目录 ASMBI_FINAL_CHANGELOG.md 及本目录 commands/。

| 项目 | 状态 | 实际时间 | 证据 |
|---|---|---|---|
| R0 作者须知核查 | PASS | 2.7 分钟 | notes/asmbi-final-20261027/R0-verification.json |
| R1 五句摘要 | PASS | 3.5 分钟 | notes/asmbi-final-20261027/R1-verification.json |
| R2 删除声明及占位 | PASS | 4.5 分钟 | notes/asmbi-final-20261027/R2-verification.json |
| R3 局限与结论 | PASS | 4.0 分钟 | notes/asmbi-final-20261027/R3-verification.json |
| R4 全文去行话 | PASS | 9.3 分钟 | notes/asmbi-final-20261027/R4-verification.json |
| R5 补充材料压缩 | PASS | 21.9 分钟 | notes/asmbi-final-20261027/R5-verification.json |
| R6 数据和代码可得性 | PASS | 8.9 分钟 | notes/asmbi-final-20261027/R6-verification.json |
| R7 标题页与投稿信 | PASS | 1.7 分钟 | notes/asmbi-final-20261027/R7-verification.json |
| R8 终检 | BLOCKED | 截至本报告 79.2 分钟 | notes/asmbi-final-20261027/R8-verification.json |
| R9 GitHub 发布 | BLOCKED | 0 分钟 | 未执行：R8 前置验收未通过 |
| C1 GitHub 完整性及历史核查 | BLOCKED | 0 分钟 | 未执行：R8 前置验收未通过 |
| C2 唯一终版文件夹 | BLOCKED | 0 分钟 | 未执行：R8 前置验收未通过 |
| C3 白名单移到废纸篓 | BLOCKED | 0 分钟 | 未执行：R8 前置验收未通过 |

R8 失败原文：`Because arch was not found in the cache and you require arch==8.0.0`。程序在测试收集前退出，退出码 1；本轮实际运行测试数为 0。现有 Python 同时缺少 pytest、scikit-learn、cvxpy、clarabel。没有补装、联网下载或以旧记录代替新通过。`R8-pytest.json`、`R8-pytest-console.txt`、`R8-dependency-inventory-final.json` 保存证据。

其余终检：数字不匹配 0；2527 个冻结科学文件逐字节不变；参考文献元数据不匹配 0；12 份 PDF 共 101 页全部直接看过，最终重建页面仅在 PNG 字节完全相同时继承检查。四个独立源码包均在全新目录解压、使用已有缓存一键编译，逐页提取文本与活动 PDF 一致；包内 .bak、.aux、.scratch 和声明匹配数均为 0。投稿包及当前稿源仅保留任务单要求的 AUTHOR-TODO 一行提醒，实际声明及占位匹配数为 0。

正式文档采用期刊允许的 12pt Free Format 和未改动的官方 AMA BST；原 NJDv5 模板的本地依赖不足，未伪称模板直接编译成功。单盲或双盲未在本次作者须知中查实，保留待作者决定。

## 3. 摘要前后对照

### 改前：175 词、8 个数字、9 句

Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules on hourly foreign exchange (FX) positions, weekly New York Fed positions and Commodity Futures Trading Commission (CFTC) dealer positions, matching histories and update schedules. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8% and 16.6% in two periods, but its ranking against a shorter rolling rule changes. Second, in the initial weekly comparisons, historical headroom beats full regression in 34 of 48 New York Fed cases; the better realized historical score wins 29 of 34 CFTC cases. Longer validation improves full regression medians in both reporting systems; CFTC short-history excess falls from 19.3% to 4.0%. A benchmark-default gate retains FX gains and improves weekly median performance, but leaves large individual losses. Third, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor regression in CFTC. Costs are illustrative, and the evidence is retrospective; the original FX evaluation period had been inspected beforehand.

### 改后：122 词、0 个数字、固定 5 句

Position limits must cover the largest absolute position reached during a review period, since an acceptable endpoint can conceal an earlier breach. We retrospectively compare historical and conditional quantile forecasts using hourly positions from one foreign exchange (FX) market maker and weekly dealer aggregates from the New York Fed and the Commodity Futures Trading Commission. Historical rules are hard to beat: regression improves FX peak forecasts with long training histories, but the measured gain depends on the historical reference. In the weekly comparisons, short training or validation histories favor historical rules; longer validation narrows median loss gaps, while large individual losses remain. Lower forecast scores need not imply lower limit costs, so model validation should report scores, breach counts and costs together.

## 4. 篇幅与写法

ASMBI 正文含参考文献和八张文末表共 25 页；叙述正文 4142 词（固定口径，排除摘要、引用、声明、图表及图表题、显示公式）。补充材料由 54 页压缩为 21 页、12 节，完整旧四十节逐字保存在 EXTENDED_RESULTS.md 和 evidence/asmbi-final-20261027/。原有两个完整证明、全部三十六条预写判断和反例仍保留。平均句长 16.568 词，超过 40 词的句子为 0，保守措辞比例 6.4%。备用 QF 主稿 22 页，补充 15 页；标题页和各投稿信均一页。

## 5. GitHub

工作分支：submission-final。本轮尚未推送；尚未进入 R9，因此没有本轮 PR 或新的远端终版 commit，不能声称远端与这些本地修改一致。原封存提交为 3dba6d906fc181be116c0b630ea97fd1a79fee7c；旧标签 submission-2026-10 未移动。本地 WIP 检查点已保存为 `99e0c16929dabcba8104bc71e89b3a1be391cafa`；它不等于远端发布完成，R8 仍为 BLOCKED。

## 6. 本地终版文件夹

计划路径：/Users/bingyouli/Research/论文/金融数学论文-ASMBI投稿终版/ 。C1 未通过前没有创建或验收这个文件夹，不能提供虚构的树形清单。现有文件仍在 v10 目录中的 submission-package/ASMBI/、QF/ 和 SHARED/，各文件用途见 MANIFEST.md。

## 7. 废纸篓与空间

本轮移入废纸篓：无；永久删除：无；清空废纸篓：无。实际释放空间为 0，未估算尚未核查副本的可释放空间。所有白名单旧目录仍保留，其他项目未作清理。只有完成 C1、C2 和 C3 验收之后，作者才能自行确认是否清空废纸篓；本次没有可清空的新移动项目。

## 8. AUTHOR-TODO.md 全文

# 作者投稿前待办

当前目标期刊为 Applied Stochastic Models in Business and Industry（ASMBI）；QF 文件包仅作为备用，不能同时投稿。本文仍是回溯性研究；保留所有不利、失败及无法判定结果。

1. AI 使用声明由作者投稿前自行添加（Wiley 要求披露）。
2. 补作者姓名和顺序、单位、通讯方式、ORCID；所有个人信息占位均需作者核实。
3. 补真实的基金、利益冲突、CRediT 贡献声明及适用的权限信息，不默认填写“无”。
4. 确认论文标题，以及 GitHub 预印本、其他公开版本和全体作者同意；亲自确认没有一稿多投。
5. 决定是否在 Zenodo 存档代码并获取 DOI，选择软件许可证；检查 FX 使用权、共享例外和复算所需原输入。
6. 决定是否关闭旧 PR #3–#6 或归档旧分支；本轮不代为关闭或合并。
7. 决定是否安排额外英文润色；不因此改动数字、结论或失败判定。
8. 核对费用、投稿方式、审稿人关系及期刊表单，补完材料后由作者本人在 Wiley 系统提交。
9. 只有 GitHub 完整性核查和本地终版核查通过、确认旧副本可以恢复后，才自行清空废纸篓释放空间。

## 待用户决定

- 是否使用已核实可接受的 Free Format 初次投稿格式，或另行准备完整的 NJDv5 排版环境；当前 PDF 不宣称由原 NJDv5 类直接排成。
- 作者须确认独家投稿、全体作者同意及数据权限，投稿信保留明确待确认文字。
- 当前 R8 全套测试因本机缺少既定测试依赖而未启动；本轮禁止安装软件，未擅自补装。后续需要可用的既有测试环境，或另行授权临时依赖环境。
- 单盲或双盲方式未在已查阅的当前作者须知中确认，不作推断。

## 目标模式最终状态

2026-10-27T10:55:32.251452+00:00：同一测试依赖阻塞已连续三轮核实，目标模式正式标记为 blocked，未标记 complete。十分钟自检进程已请求正常停止；没有发布或清理操作。后续只能在既有完整测试环境可用或约束被明确改变后，从 R8 继续。
