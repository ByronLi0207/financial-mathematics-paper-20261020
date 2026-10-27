# ASMBI 投稿定稿与本地清理（导师 Claude → GPT）· 建议开目标模式 8 小时

目标期刊：**Applied Stochastic Models in Business and Industry（ASMBI，Wiley）**。
底稿：`/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/` 下的 `submission-final` 分支，以及 `submission-package/ASMBI/`。

本轮要做三件事：①按下面的 R1–R9 改完稿件；②**删掉所有 AI 声明及其占位**（作者最后自己加）；③在 GitHub 确认保存好终版之后，本地只留一个投稿终版文件夹，其余属于本论文的工作副本**移到废纸篓**，腾出磁盘空间。

---

## 〇、执行守则

- **开启目标模式，时长 8 小时，每 10 分钟自检，连续工作。** 全程不停下来问，需要用户决定的事记入"待用户决定"。按顺序执行 R0 → R9 → C1 → C3，每一步都在 `ASMBI_FINAL_CHANGELOG.md` 里写明 PASS / BLOCKED，并附上命令和输出原文。
- **只有本对话一个执行者。** 只在 `submission-final` 分支上工作。如果发现远端有其他会话的新提交，先 fetch 并 merge，再继续。
- **硬禁令：**
  - 不新跑任何分析或模型，不改已有数字，不删不利结果；
  - 不合并 main，不关闭 PR，不删除远端分支；
  - 不安装软件，不投稿，不注册账号，不编造个人信息；
  - **不写任何 AI 声明**。
- **清理规则（C 部分）：**
  - 只能**移到废纸篓**，**禁止永久删除**，禁止清空废纸篓。用户自己清空废纸篓，空间才会真正释放。
  - 只能动第三部分"清理白名单"里列出的路径。**其他项目一律不碰。**
  - 必须先通过 C1 的"GitHub 已完整保存"核查，才能开始清理。

---

## 一、稿件修改（约 4.5 小时）

### R0 查期刊要求（20 分钟）

- 重新核对 ASMBI 当前的作者须知，包括：摘要字数上限、关键词数量、参考文献格式（AMA / APA）、模板、补充材料要求、单盲还是双盲。
- 把核对结果写进 `submission-package/ASMBI/journal-checklist.md`，注明查阅时间。后面所有格式问题都以这份清单为准。

### R1 重写摘要（40 分钟）

- 不超过 200 词（如果期刊上限更低，按期刊上限），**最多 5 个数字**。固定写成 5 句：
  ① 问题：限额关心的是期间峰值，不只是期末值；
  ② 数据：一家 FX 做市商的头寸，加上 NY Fed 和 CFTC 两类交易商周度数据；
  ③ 发现一：历史规则很难被打败；长历史下的 FX 回归有改进，但这个改进依赖于拿来比较的参照规则；
  ④ 发现二：训练历史或验证窗口太短时，条件模型会稳定地输；加长验证窗口能缩小差距，但个别任务上仍有大额损失；
  ⑤ 发现三和启示：评分更低不等于限额成本更低，验证模型时要把评分、破线次数和成本一起报告。
- **删掉这些说法：** "benchmark-default gate"、"the better realized historical score wins 29 of 34"、"arm-median"。如果确实需要相应概念，换成普通读者能看懂的表述。
- **验收：** 改写前后对照；字数；数字个数。

### R2 删除所有 AI 声明（20 分钟）

- 在稿件、标题页、cover letter、README、各类清单、模板、AUTHOR-TODO 里，删掉所有 AI 使用声明或它的占位，例如 "[AI-use disclosure …]"、"AI statement"、"Artificial intelligence" 小节。
- 在 AUTHOR-TODO 里留一行："AI 使用声明由作者投稿前自行添加（Wiley 要求披露）"。
- **验收：** 对投稿包里的全部文本文件做 grep，搜 "AI-use|AI use|artificial intelligence|generative|language model|AI disclosure"，计数为 0（AUTHOR-TODO 里那一行除外），贴出 grep 的输出。

### R3 局限与结论（60 分钟）

- **Limitations：** 把现在的 8 条项目符号改写成 **2–3 段**，分别讲：
  (a) 数据范围：只有一家做市商，周度数据都是加总数据；
  (b) 研究设计：是回溯性研究，FX 评估期此前已经被看过；
  (c) 成本是设定的，不是观察到的。

  删掉 "finite-penalty hindsight bound"、"survivor universe"、"Supplement Section S36/S40" 这类内部说法。保留实质内容，换成读者能读懂的语言。
- **Conclusion：** 第一段直接给出可以带走的结论："historical rules are hard to beat; short training or validation histories reliably favor them; a long history is necessary but not sufficient; cost structure decides the preferred rule"。第二段写对实务的建议。**免责语只留在 Limitations 一节，结论里不再重复。**
- **验收：** 改写前后对照；这两节里禁用术语计数为 0。

### R4 全文去行话（60 分钟）

- 下面这些说法，第一次出现时用一句话定义，之后统一使用简短的名称；能直接删的就删：
  - "matched histories and update schedules"（定义一次，之后写作 "matched"）
  - "completed-label pool and refitting clock"
  - "arm-median"
  - "benchmark-default gate / protocol"（用一句话讲清楚它在做什么）
  - "source-specific scales"
  - "issue origin"
  - "survivor universe"
  - "finite-penalty hindsight"
- 小标题尽量写成结论句。
- **验收：** 禁用词清单计数为 0（定义句除外）；平均句长 16–24 词；没有超过 40 词的句子。

### R5 补充材料压到 30 页以内（60 分钟）

- 现在是 54 页。按下面的顺序把内容移到仓库里的 `EXTENDED_RESULTS.md`：
  ① 逐格的大表；
  ② 重复的稳健性结果；
  ③ 审计和过程细节；
  ④ 已经被拒绝的修复方案的技术细节（补充材料里只留一段说明）。
- 补充材料里**保留**：命题的证明、方法细节、各数据源的汇总表、事前登记检验的结论和反例汇总。
- 补充材料的节数合并到 12 节以内，正文里所有引用补充材料节号的地方同步更新。
- **验收：** 补充材料页数 ≤ 30；正文中的交叉引用都能对上。

### R6 数据与代码可得性（20 分钟）

- 改写成 3 段短文，分别对应 FX（Kaggle）、NY Fed、CFTC。每段写清楚：数据来源链接、获取方式、使用条款。**每段不超过 3 句。**
- 代码可得性写一句，给出 GitHub 链接，再留一个 "[Zenodo DOI to be added by the author]" 占位。
- **验收：** 改写前后对照。

### R7 标题页和 cover letter（20 分钟）

- **标题页：** 作者、单位、ORCID、通讯作者、基金、利益冲突、CRediT 贡献声明，全部写成 `[TO BE COMPLETED BY AUTHOR]`；按期刊要求加 running title。
- **cover letter（ASMBI 专用，一页以内）：** 写明论文和期刊的契合点、三条发现、预印本已在 GitHub 公开、没有一稿多投、数据和代码在哪里可以获取。**不写 AI 声明。**

### R8 终检（40 分钟）

- 数字自动核对：正文、补充材料、cover letter 里的数字逐一比对，不匹配数为 0。
- 交叉引用检查；参考文献按期刊格式逐条核对元数据。
- 编译：Tectonic 编译无 error，未定义引用为 0。
- 逐页渲染检查，跑 pytest。
- 重新生成 `main-document-source.zip` 和 `supplement-document-source.zip`。**压缩包里不能有 .bak、.aux、.scratch 文件，也不能有 AI 声明。** 解压到一个全新的临时目录后，要能一键编译通过。

### R9 发布到 GitHub（30 分钟）

- 推送前确认：`git ls-files` 里没有 `.scratch`、原始数据或凭据。
- 用之前成功过的途径把 `submission-final` 发布到远端。如果已经有对应的 PR，就更新它；没有就新开一个，标题写 "ASMBI submission-ready manuscript"。PR 描述里写明它取代 #3–#6，由作者决定关闭哪些旧 PR。**不合并，也不关闭任何 PR。**
- **验收：** 远端和本地的树逐文件一致（贴出比对输出）；PR 链接。

---

## 二、本地终版文件夹与清理（约 1.5 小时）

### C1 GitHub 完整性核查（必须 PASS，才能进入 C2/C3）

- 远端 `submission-final` 的文件树与本地完全一致，包括稿件、补充材料、代码、协议、结果、`EXTENDED_RESULTS.md`、CFTC 的数据和 provenance。
- QF 投稿包如果不在远端，就先发布到 `submission-final` 分支里，作为备用期刊的材料。
- 白名单里的每个工作副本都要检查一遍：有没有哪些文件**只在本地、不在任何远端分支上**，例如未提交的修改，或者只存在于本地的重要结果。把清单列出来。凡是对论文有用的，先发布到 `submission-final`，或者复制进终版文件夹；纯缓存、日志和 .bak 不需要保留。
- **历史备份：** 把各工作副本的本地 git 历史打包成**一个** `paper-history.bundle`（`git bundle create … --all`），放进终版文件夹。如果打出来超过 1 GB，就不做这一步，记入"待用户决定"。
- **验收：** 一致性比对的输出；"只在本地"文件的清单和处理方式；bundle 的大小，以及 `git bundle verify` 的输出。

### C2 建立本地终版文件夹

新建 `/Users/bingyouli/Research/论文/金融数学论文-ASMBI投稿终版/`，**只放投稿和存档必需的文件**：

```
金融数学论文-ASMBI投稿终版/
├── 01-投稿上传文件/          ← 投稿系统里要上传的全部文件，不含其他任何东西
│   ├── manuscript.pdf
│   ├── main-document-source.zip
│   ├── supplement.pdf
│   ├── supplement-document-source.zip
│   ├── title-page.pdf（及 .tex）
│   ├── cover-letter.pdf（及 .tex）
│   └── figures/            ← 期刊要求单独上传的图
├── 02-备用期刊QF/            ← QF 投稿包精简版（只放上传文件，可选）
├── AUTHOR-TODO.md           ← 中文：投稿前作者要做的事
├── GITHUB.md                ← 远端仓库链接、终版分支、PR 链接、终版 commit 号
└── paper-history.bundle     ← 可选，见 C1
```

**AUTHOR-TODO.md 至少包括：**
1. 补 AI 使用声明；
2. 补作者信息、单位、ORCID；
3. 补基金、利益冲突、CRediT 贡献声明；
4. 确认标题；
5. 决定是否在 Zenodo 存档代码并拿到 DOI，以及选择许可证；
6. 在 GitHub 上关闭旧的 PR #3–#6（可选）；
7. 英文润色（可选）；
8. 在 Wiley 投稿系统里提交；
9. 确认无误后**自行清空废纸篓**，释放空间。

**验收：** 文件夹的树形清单和总大小；`01-投稿上传文件/` 里没有 .bak、.aux 文件；PDF 都能打开，并逐页渲染检查过。

### C3 把其余工作副本移到废纸篓

**清理白名单：只能动下面这些路径，并且只能移到废纸篓。**

- `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/`
- `/Users/bingyouli/Research/论文/金融数学论文-v8-20261024/`
- `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/`
- `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/`（**最后才移**，必须在 C2 完成并通过验收之后）
- `/Users/bingyouli/Research/论文/金融数学论文-final-jof-20261025/`
- `/Users/bingyouli/Research/论文/金融数学论文-导师修订-20261023/`
- `/Users/bingyouli/Research/论文/金融数学论文_终版_20261022/`（旧的 23 页终版，已被新终版取代）
- `/Users/bingyouli/Desktop/codex folder/2026-10-22/financial-mathematics-improvement/`：要先确认它是本论文仓库的旧克隆，才能移；不是的话就不动。

**绝对不许碰：** `论文1-finite-extendibility-*`、`markov-*`、`few-psu-*`、`deliverables/`，以及 `/Users/bingyouli/Research/论文/` 下所有其他项目、`~/.cache` 和系统目录。

**操作要求：**
- 移动之前，先列出每个路径的大小。
- 一律用 macOS 的"移到废纸篓"（Finder 或 `osascript` 调用 Finder delete）。**不许用 `rm`，不许清空废纸篓。**
- 移动之后，确认原路径已经不存在、废纸篓里能找到。另外再确认一次：受保护的其他项目，目录列表与清理前完全相同。

**验收：** 清理前后的磁盘占用对比；移入废纸篓的清单及每项大小；受保护项目的前后对比结果。

---

## 三、最终报告（中文，简明）

1. 一句话结论：稿件是否已达到"作者补完信息就能投 ASMBI"的状态。
2. 合规表：R0–R9、C1–C3，每项写 PASS / BLOCKED，并注明证据位置。
3. 新摘要（英文原文），附改写前后对照。
4. 篇幅：正文页数和字数、补充材料页数。
5. GitHub：终版分支、PR 链接、终版 commit。
6. 本地终版文件夹的路径和树形清单。
7. 移入废纸篓的清单，以及可以释放的空间（**提醒用户自己清空废纸篓**）。
8. AUTHOR-TODO.md 全文。
