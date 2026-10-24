# 论文修改方案（Claude 审稿 → GPT 执行）· 2026-10-23

修改对象：GitHub `ByronLi0207/financial-mathematics-paper-20261020` 的 **main 当前版**（commit `cbce398`，25 页，preference-robustness revision）。
注意：本地 `/Users/bingyouli/Research/论文/金融数学论文_终版_20261022/` 里是**旧的 23 页版**，不要以它为底稿，也不要改动这个目录。

## 总评

数据处理、负结果保留、可复现性做得很扎实。主要问题有三个：
1. 写法不像论文，更像审计日志。约 24% 的句子带 not/neither/no 之类的免责语；commit hash、SHA-256、内存字节数、秒数也写进了正文；研究一层层往上追加（原始研究 → 检索 → 条件模型 → AR → 事后诊断 → e-value → 秩消融 → 偏好前沿），每层各带一套警告。
2. 缺少本领域的标准推断：没有 Diebold–Mariano/HAC 检验，也没有 Kupiec/Christoffersen 回测，审稿人一定会要。
3. Treasury 结果失败，最可能的原因是**特征设计照搬了小时级 FX**，论文里却没有正面分析这一点。

## 工作规则（必须遵守）

- R1：在新目录 `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/` 里重新克隆仓库，新建分支 `revision-v3-readability`。不改 main，不改 FINAL.md，**不 push**（等用户确认后再推）。
- R2：不删除任何文件。覆盖非 git 跟踪的已有文件前，先在同目录备份为 `.bak`。
- R3：**不许手填或改动任何已有数字**。正文中的每个数字，要么来自仓库里已归档的 CSV/JSON，要么来自本次新增脚本的实际输出（脚本、输出、测试一起提交）。
- R4：所有负结果都保留，措辞不许弱化，包括：Treasury primary 恶化、短历史 QR 恶化、稀疏网格反转、破线次数增加。
- R5：新做的分析一律标注 "post-result / exploratory"，不能替换两个已声明的 primary。
- R6：完成后渲染 PDF，逐页看一遍，再汇报。
- R7：新建 `REVISION_V3_CHANGELOG.md`，按 A1…C2 逐条写清楚：做了什么、改在哪里（文件/章节）、没做的原因。
- 执行顺序：A1–A9 → B5 → B1 → B3 → B2 → B4 → C1 → C2。时间不够就按这个顺序截断，并在 changelog 里写明哪些没做。

## P0 写作与结构（必须做）

- **A1 摘要重写，≤180 词。** 依次写清：研究问题；为什么重要（做市商/交易商的库存风险限额）；数据；方法；3 个核心发现；一句局限。3 个核心发现是：① FX H6 在匹配历史下 −14.77%，但破线从 360 增到 376；② Treasury primary 恶化 +50.79%，破线从 28 增到 54；③ pinball 改进常伴随破线增加。AR、前沿、稀疏网格的细节数字不写进摘要。
- **A2 引言重写。** 第一段讲经济动机：做市商/一级交易商的净头寸峰值决定库存限额、保证金和资产负债表占用。引用库存文献：Ho & Stoll (1981, JFE)、Lyons (1995, JFE)、Hansch, Naik & Viswanathan (1998, JF)；Treasury 部分接 Duffie et al. (2023) 的交易商资产负债表容量。之后按"研究问题 → 方法 → 主要发现 → 贡献（列 3 条）→ 文章结构"展开。引言里不放免责句。
- **A3 全文去掉免责口吻。** 同一个限制只说一次，集中放在 Discussion 的 Limitations 小节，例如"FX 区间此前已被查看"、"不构成条件覆盖保证"、"不代表融资节省"。目标：正文中含否定词的句子从约 24% 降到 10% 以下。统计口径：按句号分句，匹配 `\b(not|neither|nor|no|cannot)\b`。修改前后的比例都写进 changelog。
- **A4 审计信息移出正文。** commit hash、SHA-256、字节数、RSS 内存、秒数、线程数等，全部移到新附录 "Reproducibility and pre-specification"（≤1 页）或仓库 README。参考文献条目后面那类 "Consulted body… final-body equivalence is unverified" 的说明也移走。正文只保留一句：设计在执行前公开冻结（附链接），FX 评估区间此前已被查看过。
- **A5 结构重排如下：**
  1. Introduction
  2. Related literature
  3. Data
  4. Target and forecasting methods
  5. Evaluation design
  6. Results: FX
  7. Results: Treasury
  8. Robustness：把 AR replay、rank ablation、preference frontier、horizon coherence 合并成一节，每项 1 段，配 1 张汇总表，细节放附录
  9. Discussion and limitations
  10. Conclusion：≤200 词，删掉结尾挂着的 rank 补充句

  正文控制在 15 页以内，附录另计。
- **A6 统一记号和术语，并加一张 notation table。**
  - 需要改的冲突：`r` 同时表示 refit 时点和半径 r(abs)/r(signed)；`W` 同时表示窗口长度和 A.4 的平移路径 W_{i,h}；`P` 同时表示峰值、P0 报告和原问题目标 Pλ。
  - K 不再叫 "original L"。
  - Treasury、TB、NY 统一叫 Treasury；S-KNN、Scaled KNN、SCALED_KNN 统一成一个名字，图中标签也要改。
- **A7 数学排版。** 正文里的 ASCII 公式全部改成正式数学记号，例如 `alpha=mu(B)+a beta(0)`、`phi(r)^h`、`ceil((m+1)19/20)`、`sum_i in T`。
  - 现在的 PDF 是 ReportLab 排的，不是 LaTeX 编译的。优先用真 LaTeX 编译 main.tex。
  - 本机没有 TeX 引擎时，先问用户是否允许安装（例如 `brew install tectonic`），**不要擅自安装**。用户同意之前，至少让 ReportLab 版的公式用上正确的 Unicode 符号和上下标。
- **A8 图表。**
  - Figure 1–3 目前正文一次都没引用。要在结果节中引用，并把图放到对应位置。
  - Table 3/4 增加三列：breach rate、相对匹配 frozen F 的 % 变化、B1 的检验结果。
- **A9 参考文献。**
  - Liao & Theodosopoulos (2005) 正文没有引用，要么删掉，要么在正文中引用。
  - 作者 "davidlindsay1979" 改为规范的数据集引用格式，年份以 Kaggle 页面为准，查不到就写 n.d.。
  - 新增文献逐条核对 DOI。核对不了的不要写 DOI。

## P1 标准统计推断（必须做）

- **B5 先恢复逐点数据。** 逐点预测轨迹原本是私有文件，本地已经删除。
  - 用仓库的 `reproduce_conditional.py replicate` 重新生成。
  - FX 原始数据按仓库 README 第 82–94 行的说明从 Kaggle 重新下载，并校验 SHA-256 `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`。
  - 重算得到的 summary 必须与归档 CSV 完全一致。不一致就**停下来报告**，不要继续往下做。
  - Kaggle 下载失败时：先完成 Treasury 的 B1–B4，FX 部分标注 "blocked: raw input unavailable"，**不许编数**。
- **B1 预测精度检验。**
  - 检验范围：两个 primary、FX H24 legacy、Table 3/4 中每个条件方法相对匹配 frozen F 的对比。
  - 方法：Diebold–Mariano (1995)，方差用 Newey–West HAC（带宽 ≥ H，因为 H 步窗口重叠），同时报告 Harvey, Leybourne & Newbold (1997) 的小样本修正。
  - 由于是固定窗口滚动估计，正文要说明 Giacomini & White (2006) 无条件 CPA 检验的适用理由。
  - 表中报告 t 统计量和 p 值。
- **B2 多重比较。** 对 72 个匹配对比报告 Holm 调整后的 p 值；或者对每个 source/H/W 格子做 Hansen, Lunde & Nason (2011) 的 Model Confidence Set（90%）。
- **B3 覆盖率回测。**
  - 在已有的不重叠 H+1 网格上（样本数 947/265/40/12），做 Kupiec (1995) POF 检验和 Christoffersen (1998) 独立性/条件覆盖检验。
  - 全样本另做 Engle & Manganelli (2004) 的 DQ 检验。
  - 正文的覆盖率讨论用这些标准检验；Appendix D 的 e-value 降级为附录补充。
- **B4 Murphy 图。** 用 Ehm, Gneiting, Jordan & Krüger (2016, JRSS-B) 的 elementary quantile scores，给两个 primary 画 τ=0.95 的 Murphy diagram。这正好回答论文自己写的"无法回答"的问题：QR 是否在所有 0.95 分位一致评分函数下都占优。现有的 preference frontier 保留，但要写明它和 Murphy 图的区别（前者在固定报告下变动分位水平，后者固定 τ、变动阈值 θ）。表述框架引用 Gneiting, Balabdaoui & Raftery (2007) 的 "sharpness subject to calibration"。
- **B6 代码和输出位置。**
  - 新脚本 `inference_tests.py`，配套 `test_inference_tests.py`：DM、Kupiec、Christoffersen 都要用已知答案的小例子测试。
  - 输出放到 `results/revision-20261023/inference/`。

## P2 解释 Treasury 失败（P0、P1 完成后再做）

- **C1 在 Discussion 中正面分析最可能的机制。** Treasury 直接沿用了为小时级 FX 设计的 33 维特征，导致：
  - 25 个滞后水平放在周数据上，等于用了 24 周的水平值；
  - hour-of-day 的正余弦在周三收盘数据上是常数；
  - W=52 时，34 个参数只配 52 个重叠样本，明显过参数化；
  - Treasury 四个格子的 λ 全部落在菜单端点。
- **C2 简约 QR（探索性，明确标注 post-result）。**
  - 特征只用 B_t、N_t、短期 RMS、长期 RMS 共 4 个；λ 网格扩展为 {0.001, 0.01, 0.1, 1, 10}。
  - 验证/评估切分不变，报告 Treasury 4 格和 FX 4 格的结果。
  - 不替换 primary，只用来判断失败到底是"条件方法本身不行"，还是"特征设计不适配"。

## 不要做

- 除 C2 外，不再追加新一层"补充分析"：不加新的 e-value、前沿或消融。
- 不改任何已归档的结果文件；不 push；不动其他项目。
- 不因为检验结果不好看就改措辞或挑结果。

## 交付后在对话里贴出

- 新 PDF 的路径和页数；
- 否定句比例的修改前/后数值；
- B1 与 B3 的主结果表；
- `pytest` 的完整输出；
- REVISION_V3_CHANGELOG.md 的路径。
