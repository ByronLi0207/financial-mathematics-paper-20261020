# 已公开版本与预印本政策

核查范围：H0所保存的15个公开分支头及其可达PDF修改历史；每份列出固定commit、Git blob、SHA-256和URL。未下载PDF，仅读已经存在的Git对象与公开GitHub元数据；不声称掌握作者在仓库外的其他版本。这里只做同一研究版本清单，不提供未实际运行的相似度百分比。

## 公开分支头

| Branch | Pinned head | Document PDFs | Link |
|---|---|---:|---|
| `codex/critical-review-20261023` | `ec29c060d8a9` | 1 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/codex/critical-review-20261023) |
| `codex/preference-robustness-20261022` | `895162023445` | 1 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/codex/preference-robustness-20261022) |
| `codex/supervisor-revision-20261023` | `2328994c44ec` | 2 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/codex/supervisor-revision-20261023) |
| `final-jof` | `6192ec370d13` | 34 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/final-jof) |
| `main` | `65feeee801b6` | 1 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/main) |
| `revision-v10` | `23fd9fa8c865` | 17 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v10) |
| `revision-v10b` | `de1a1cf22a00` | 17 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v10b) |
| `revision-v11` | `452064866c2b` | 17 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v11) |
| `revision-v12` | `80608070e4a6` | 17 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v12) |
| `revision-v13` | `8c4b2b1572ee` | 17 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v13) |
| `revision-v4-jof` | `095ba7ff52ec` | 5 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v4-jof) |
| `revision-v7-final` | `d119a1fb30c4` | 12 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v7-final) |
| `revision-v8` | `f151b8304899` | 13 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v8) |
| `revision-v8-goal` | `60130eec7af2` | 12 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v8-goal) |
| `revision-v9` | `0d2526cc6909` | 13 | [文件树](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v9) |

分支头共有 179 个文稿/补充/标题页/附信PDF路径出现；可达历史去重后共有 162 个 path/blob 版本。完整逐文件清单与 SHA 在 [public-versions.json](public-versions.json)。同一PDF在多个分支出现不当成多项独立研究。新的 submission-final 文件以最终 MANIFEST 为入口，发布后由H8远端回执确认。

## PR #3–#6（只读）

| PR | Title | Head | State |
|---|---|---|
| [#3](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/3) | Refocus the peak-position paper and verify the ridge-menu comparison | `codex/supervisor-revision-20261023` / `2328994c44ec` | open; merged=False; draft=False |
| [#4](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/4) | Publish verified v7 peak-position manuscript and complete evidence | `revision-v7-final` / `d119a1fb30c4` | open; merged=False; draft=False |
| [#5](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/5) | Assess partial history-length support for peak-position forecasts (v9) | `revision-v8-goal` / `60130eec7af2` | open; merged=False; draft=False |
| [#6](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/pull/6) | Final consolidated JoF submission | `final-jof` / `6192ec370d13` | open; merged=False; draft=True |

## ASMBI 官方预印本政策

[作者指南](https://onlinelibrary.wiley.com/page/journal/15264025/homepage/forauthors.html)，本轮H6再次直接读取，Preprint Policy原文短引：

> will consider for review articles previously available as preprints

该政策允许考虑已有预印本，也允许作者随时把投稿版本放在预印本服务器，并要求出版后更新最终出版链接。指南同时要求避免已正式发表和同时投他刊；预印本例外不能替作者证明全部原创性、版权或独家投稿条件。

附信第三段披露GitHub工作版本、分支与PR，以及公开代码和汇总；供编辑在其政策下考虑，不断言任何GitHub形式都会自动被接受。受限原始输入的权利与共享例外另由作者确认。作者仍须确认仓库以外版本、所有作者同意和当前独家投稿状态。本轮没有联系期刊、改变公开范围或操作PR。

## 待用户决定

确认仓库外是否还有版本；确认本次只向一家期刊提交及全部作者批准；出版后补最终文章链接；是否调整仓库可见性或处理旧PR留待作者决定。
