# 唯一最终投稿入口

**`submission-final` 是本研究唯一的最终投稿入口。** 使用 [MANIFEST](submission-package/MANIFEST.md) 选择文件；固定发布标签为 `submission-2026-10`。首选 Applied Stochastic Models in Business and Industry，备选格式为 Quantitative Finance，第二备选为 Computational Statistics。三刊的 SCIE 依据、未核实分区及现行政策均在 [官方期刊核查](notes/submission/journal-shortlist.md)。

**当前写法与排版修订已通过 R8，发布与清理另行验收。** R0–R7 已通过；R8 的编译、逐页检查、数字来源和完整 pytest 均已通过。测试依赖使用作者明确允许的临时环境，系统 Python 未改。R9 与 C1–C3 尚待顺序执行；旧标签仅代表此前发布的版本。详见 [本轮执行日志](ASMBI_FINAL_CHANGELOG.md) 和 [R8 验收](notes/asmbi-final-20261027/R8-verification.json)。

科学基线为 `revision-v13` / `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`。从只读 `final-jof` / `6192ec370d131c60d05e9fb103150e0e9db6aa23` 仅导入审计通过的保存证据及投稿准备材料。没有采用其标题和摘要，没有新增实验，也没有改旧结果。所有数值失败、反例、部分支持和无法判定均保留。

`submission-final/` 是共同科学源；`submission-package/ASMBI/` 是首选上传稿；`QF/` 是另一期刊的切换版，不作同时投稿。个人资料、数据权利、软件许可、DOI、费用、审稿人和独家投稿确认仍由作者完成，见 [中文清单](notes/submission/投稿操作清单.md) 和 [待决定事项](notes/submission/PENDING.md)。本轮只准备与发布文件，不代作者提交。

下面仅为**投稿后由作者决定**的整理建议，本轮不执行关闭、合并、删除、归档或可见性变更。`main` 仍是其原内容；在 GitHub 阅读或下载时请明确切换到 `submission-final`，不要把默认分支当成本次稿件。

| 分支 / PR | 本轮地位 | 建议 |
|---|---|---|
| `submission-final` | 唯一投稿稿 | 保留分支和固定标签；个人信息完成后另存作者上传切片并核验 |
| `revision-v13` | 指定科学基线 | 保留，作为审计与引用基线 |
| `final-jof` / [PR #6](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/6) | 核查通过内容的只读来源 | 保留源；投稿后可把PR标为被本稿替代并决定关闭，不合并其整份旧主线 |
| `revision-v8-goal` / [PR #5](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/5) | 旧历史长度研究与版本 | 保留证据和固定引用；投稿后决定是否关闭旧PR以减少并行“终稿” |
| `revision-v7-final` / [PR #4](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/4) | 旧投稿稿 | 保留科学记录；投稿后可关闭旧PR并标历史，不删除记录 |
| `codex/supervisor-revision-20261023` / [PR #3](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/3) | E5/R6等早期修订 | 保留原协议与负结果；投稿后决定是否关闭旧PR |
| `revision-v12`、`revision-v11` | 既有设计和逐轮修订基线 | 保留，不再作为投稿入口 |
| `revision-v10`、`revision-v10b`、`revision-v9` | 历史数值与排版切片 | 保留，可在作者决定后仅标为历史；不重写档案 |
| `revision-v8` | 与goal版本不同的早期稿 | 保留身份区别，不与PR #5的分支混称；作者之后决定归档方式 |
| `revision-v4-jof` | 更早JoF版本 | 保留，SCIE目标已由本轮重新核实，旧目标不再指引本次上传 |
| `codex/critical-review-20261023`、`codex/preference-robustness-20261022` | 早期审查/稳健性记录 | 保留，不当成最终稿 |
| `main` | 原默认分支 | 本轮保持原指向；是否以后整合由作者另行决定 |

原始分支指向在 `notes/submission/remote-before.txt`，公开PDF与PR完整清单在 `notes/submission/public-versions.md/.json`。此前发布版本的编译、逐页图像、测试与数值核查由 H8 回执绑定；当前修订的证据另存于 `notes/asmbi-final-20261027/`，不能把旧测试通过记录当成本轮重新通过。推送后的分支与标签读回须另行记录，避免把提交尚未发生时的计划写成已经发布。
