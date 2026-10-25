# v10 中文交付说明

**当前状态：E0–E6科学工作及E7本地验收完成；26批473个文件已发布，3925个tracked文件的全部路径、模式和blob与冻结研究树一致。首次整树核验为2026-10-25T00:56:24.875679UTC，远端f104c03d4137fa7a1fa1166422bab91bb44f53e2，tree1f51a3448c83d77a1c9be667d88b2d5390670848。最终交付元数据随后单独发布，并再次核验。**

保护核对有一项实质限定：旧v3本地目录相对E0出现8个tracked文件及HEAD/tree漂移，来源未确定，整体raw snapshot不变量为 **FAIL**；本轮未写入、恢复或回滚该目录。14个受保护旧远端refs与E0一致，NEW继承研究文件及1036项科学封存指纹通过。不能声称所有旧目录始终未变。完整证据见 [final-protection.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-protection.md>) 和 [PENDING.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/PENDING.md>)。

## 1. E1–E4：设计提交、正式运行与耗时

下表均为UTC。正式wall秒数直接取已保存回执，不含设计、实现、人工测试、准备及报告时间；stage总用时另列于第7项。所有设计均先单独提交，再开始正式计算；E2也在原设计提交后才发出首个数据请求。

|阶段／设计|设计commit|设计提交UTC|正式开始UTC|正式wall秒数|
|---|---|---|---|---:|
|E1：[menu-isolation-design.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/v10/menu-isolation-design.md>)|`3c5f167632a1a21ded29731a773a85ab307d3a96`|2026-10-24 22:18:54|2026-10-24 22:31:44.606969|367.847078|
|E2：[cftc-design.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/v10/cftc-design.md>)|`acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf`|2026-10-24 22:45:31|2026-10-24 23:08:56.022441|12.258634|
|E3：[mcs-design.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/v10/mcs-design.md>)|`78ea93493379ab3a93459d28e1bab84200f01539`|2026-10-24 23:23:01|2026-10-24 23:43:04.324505|64.372534|
|E4：[cost-design.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/protocol/v10/cost-design.md>)|`a112e458500b5dd34e0536074dff77091ab39ed1`|2026-10-24 23:45:53|2026-10-24 23:52:38.945580|1.674982|

E2首次官方数据请求为 `2026-10-24T22:46:47.043Z`。两次限定读取澄清在获取后、任何forecast/model-loss前单独提交：午夜日期suffix `4d46550c23a54662112979acc891ba4f903dc39c`（22:58:31 UTC），整数零小数写法 `818b942b1bc7d9cbb29329c9c1d8884376242769`（23:03:41 UTC）。原技术失败及零合格技术回执保留；它们没有改变数学整数定义、阈值、筛选或方法设置。

## 2. M1–M3、T1–T3与主结果

|预测|状态|冻结口径下的结果|
|---|---|---|
|M1|支持|constant、QR33、W52跨13来源中位数+0.20694%，在预定±5%内。|
|M2|不支持|switching−constant为−0.43472个百分点，未达到至少+5个百分点；未过门槛不证明等价。|
|M3|支持|两臂整体均改善，严格同时改善的来源交集为13，达到至少12／13。|
|T1|支持|F或I在29／34格损失严格低于QR33，超过预定60%。|
|T2|不支持|QR33相对F的中位数为W52 +19.33472%、W260 +10.34828%，均超过+10%上限。|
|T3|支持|QR4相对F的中位数由W52 +10.28068%降至W260 +0.21749%。|

E1八组旧／扩展菜单跨来源中位数如下。每个完整来源保留32个配对重复，再对全部13来源等权汇总；没有成功子集替代。

|参数臂|W|方法|旧菜单|扩展菜单|完整性|
|---|---:|---|---:|---:|---|
|constant|52|QR33|+116.24%|+0.21%|COMPLETE|
|constant|52|QR4|−0.02%|+0.44%|COMPLETE|
|constant|260|QR33|NA|NA|UNASSESSABLE|
|constant|260|QR4|−1.21%|−1.13%|COMPLETE|
|switching|52|QR33|+121.40%|−0.23%|COMPLETE|
|switching|52|QR4|−0.03%|+0.38%|COMPLETE|
|switching|260|QR33|NA|NA|UNASSESSABLE|
|switching|260|QR4|−0.27%|−0.28%|COMPLETE|

W260的QR33在两臂各保留一个规定来源的失败，整体均UNASSESSABLE，没有重试或以12来源补汇总。QR4的exact-tie规则变化已披露；保存exact ties为0、实际改变的tie选择为0。结果支持菜单解释，但未识别经验数据的频率机制。

CFTC全部17合约的等权中位相对损失如下，均以各自匹配F为基准，不混合原单位的绝对损失。204个方法格全部完成，无数值重试。

|方法|W52|W260|
|---|---:|---:|
|F|0.00%|0.00%|
|I|+3.37%|+0.92%|
|QR4|+10.28%|+0.22%|
|QR33|+19.33%|+10.35%|
|ACI_F|+30.15%|+5.58%|
|ACI_QR33|+24.64%|+9.39%|

旧真实结果保持原比较身份：较晚／较早匹配FX降低14.8%／16.6%，但较早相对原短rolling reference增损3.2%；较早Treasury短历史结构类比增损144.3%，one-SE最差格仍增损181.4%。没有把不同history/reference重新包装成同一个复现。[数字来源审计](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/main-number-audit.md>)记录240个旧来源定位与62个新增绑定。

完整结果：[E1 report-values.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/menu/report-values.json>)、[E2 report-values.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/report-values.json>)、[CFTC完整方法格cells.csv](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/cells.csv>)。

## 3. CFTC的17个代码与唯一新数据来源

严格筛选得到17／141个观察代码，少于20上限，未放宽规则凑数。下表按冻结的OI展示顺序列出代码与保存metadata中的最新名称；历史name spans仍保留。

|代码|最新合约名称|
|---|---|
|`044601`|UST 5Y NOTE — CHICAGO BOARD OF TRADE|
|`043602`|UST 10Y NOTE — CHICAGO BOARD OF TRADE|
|`042601`|UST 2Y NOTE — CHICAGO BOARD OF TRADE|
|`045601`|FED FUNDS — CHICAGO BOARD OF TRADE|
|`020601`|UST BOND — CHICAGO BOARD OF TRADE|
|`099741`|EURO FX — CHICAGO MERCANTILE EXCHANGE|
|`1170E1`|VIX FUTURES — CBOE FUTURES EXCHANGE|
|`097741`|JAPANESE YEN — CHICAGO MERCANTILE EXCHANGE|
|`096742`|BRITISH POUND — CHICAGO MERCANTILE EXCHANGE|
|`095741`|MEXICAN PESO — CHICAGO MERCANTILE EXCHANGE|
|`090741`|CANADIAN DOLLAR — CHICAGO MERCANTILE EXCHANGE|
|`232741`|AUSTRALIAN DOLLAR — CHICAGO MERCANTILE EXCHANGE|
|`33874A`|E-MINI S&P 400 STOCK INDEX — CHICAGO MERCANTILE EXCHANGE|
|`240743`|NIKKEI STOCK AVERAGE YEN DENOM — CHICAGO MERCANTILE EXCHANGE|
|`092741`|SWISS FRANC — CHICAGO MERCANTILE EXCHANGE|
|`098662`|USD INDEX — ICE FUTURES U.S.|
|`112741`|NZ DOLLAR — CHICAGO MERCANTILE EXCHANGE|

对象为TFF Futures Only的Dealer/Intermediary long−short，单位是原始合约数。2010起完整周历共877周；实际evaluation position dates为2021-09-21至2026-09-08，末标签至2026-10-20。Monday仅作为模型特征日历索引，通常Tuesday持仓／Friday发布不等于Monday公开可用。类别是相关汇总，不是17位独立dealer；全历史连续性构成retrospective survivor universe，下载vintage不是first-release试验。

唯一新金融数据来自 [CFTC官方历史索引](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm)：2006–2016历史包加2017–2026 annual，共11文件。每文件URL、请求/完成UTC、bytes和SHA-256在 [provenance.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/data/cftc-tff/provenance.json>)；原始ZIP在 [data/cftc-tff/raw](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/data/cftc-tff/raw>)。

字段及官方访问核对：[cftc-source-verification.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/cftc-source-verification.md>)；完整筛选／排除理由：[eligibility.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/eligibility.json>)；切分：[splits.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/splits.json>)；逐合约汇总：[contract-summary.csv](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cftc/contract-summary.csv>)。

## 4. MCS汇总与成本区域

|MCS全计划98比较|结果|
|---|---:|
|完整比较|98／98|
|匹配F/I在90% MCS中|90／98|
|唯一literal历史方法|2／98|
|唯一loss class含F/I|4／98|
|完整conditional方法slot被排除|197／683|
|已知不可用方法slot|60，其中conditional56；不计入统计排除|

MCS使用arch8.0.0、R statistic、1000 stationary-bootstrap draws及固定block length；不是跨任务独立联合检验或未来coverage保证。正文表：[v10-mcs-main.tex](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/generated/v10-mcs-main.tex>)；完整集合、p值、loss classes与NA：[MCS保存报告](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/mcs/report-values.json>)和 [Supplement](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/supplement.pdf>)。

成本图固定 **c=1** 时，CFTC expanded QR33在显示的系数网格上更便宜的格数为 **1–32／34**。这是按各比较F平均headroom归一化的固定路径偏好分析，非观测经营费用、盈利、最优干预或共同美元风险。全部98比较、976完整方法、189系数点及184,464成本行保留，没有按结果选有利模型。

成本正文图：[v10-cost-regions.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/figures/v10-cost-regions.pdf>)；原结果图：[cost-regions.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/cost-regions.pdf>)；完整区域：[primary-regions.csv](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/primary-regions.csv>)；完整方法成本表：[cost-grid.csv.zip](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/cost-grid.csv.zip>)；汇总：[cost report-values.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/results/v10/cost/report-values.json>)。

其他新图：[CFTC合约变化图](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/figures/v10-cftc-contract-changes.pdf>)、[菜单隔离图](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/figures/v10-menu-isolation.pdf>)。

## 5. 目标期刊候选与第一目标

官方查询日期为2026-10-24 UTC。**三刊当前JCR及中科院分区全部未核实**，不能称为已认证的三区名单。第一目标为Journal of Forecasting，依据官方范围契合，非分区猜测或录用预测。

|候选与官方来源|范围／格式核对|当前JCR／CAS|
|---|---|---|
|[Journal of Forecasting](https://onlinelibrary.wiley.com/journal/1099131x)；[官方指南](https://onlinelibrary.wiley.com/page/journal/1099131x/homepage/forauthors.html)|第一目标；跨学科预测理论、应用与计算。Free Format；初投可LaTeX及PDF/依赖，≤6关键词、running title<40字符、要求ORCID。可读官方指南未见硬性总页数／字数上限；本轮20页来自任务约束。|均未核实|
|[International Journal of Forecasting](https://shop.elsevier.com/journals/international-journal-of-forecasting/0169-2070)；[IIF官方页](https://forecasters.org/ijf/)|预测方法与经验评价；官方说明double-blind及数据/代码补充。完整作者指南返回403，具体字数／模板细则未核实。|均未核实|
|[Journal of Risk Model Validation](https://www.risk.net/journal-of-risk-model-validation)；[官方指南](https://www.risk.net/static/risk-journals-submission-guidelines)|风险模型实施、验证与回测。匿名主PDF另title page，摘要150–200词、4–6关键词、3–4条key messages；research paper10000词是指导值而非硬限。|均未核实|

分区入口：[Clarivate JCR](https://jcr.clarivate.com/)、[中科院分区表](https://www.fenqubiao.com/)。认证详情不足，未以MJL、影响因子、Scopus/SJR或第三方站替代。完整范围、格式和访问精度记录：[target-journals.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/target-journals.md>)；关键文献一手核对：[reference-verification.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/reference-verification.md>)。

## 6. 完整改写文本与稿件

改写后的**摘要、三个研究问题、最多三条贡献及结论全文**集中在 [final-prose.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-prose.md>)。该文件按最终主稿去TeX转义并展开核对编号；此处链接全文，不再复制出易漂移的第二版本。

最终稿件：[正文PDF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/manuscript.pdf>)、[Supplement PDF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/supplement.pdf>)、[标题页PDF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/title-page.pdf>)、[cover letter PDF](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/cover-letter.pdf>)。源文件、29-member原生源ZIP和回放入口见 [REPRODUCING.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/REPRODUCING.md>)。原始FX与私有逐origin向量不公开；金融回放与公开aggregate／文档再生是不同验收。

E6为两份**同模型内部**模拟意见，各5项，与v9继承42项合并为52项逐条处理；不是期刊外审、跨模型或Claude复核。[review-reconciliation.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/review-reconciliation.md>)及 [AUTHOR-TODO](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/AUTHOR-TODO.md>)保留不能由写法解决的科学缺口。

## 7. 写法、页数、测试、阶段用时、待决定项与compare

|相同checker的写法指标|改前|改后|任务门槛|
|---|---:|---:|---:|
|保守措辞句比例|1.5686%|3.14465%|≤8%|
|平均句长（词）|11.392|11.54088|≤20|
|超过40词的句子|0|0|0|

来源：[writing-comparison.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/writing-comparison.json>)、[writing-final-frozen.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/writing-final-frozen.json>)。这是固定词表／句子规则下的写法计数，不是科学质量评分。

最终原生PDF为 **20／33／1／1页**（正文／Supplement／标题页／信），**全部55页内容均已逐页查看**。最后改动页面重开检查，其他最终页面与已看图像字节一致；没有overfull box或未解析引用。PDF与PNG指纹：[final-native-build.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-native-build.json>)；逐页视觉记录：[main](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-visual-main.md>)、[Supplement1–17](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-visual-supp-a.md>)、[Supplement18–33/title/letter](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-visual-supp-b.md>)。

全套固定测试 **1715 passed, 1181 subtests passed**，exit0；pytest报告110.99秒，实际wall111.619131秒。精确命令、环境、输出及指纹在 [final-tests.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/final-tests.json>)。此后仅文档文字／显示变化，数值代码与测试不变。保存命令如下，不在本交付阶段重跑：

```sh
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1 --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow python -B -m pytest -q -p no:cacheprovider
```

线程环境的 `OMP_NUM_THREADS`、`OPENBLAS_NUM_THREADS`、`VECLIB_MAXIMUM_THREADS`、`MKL_NUM_THREADS`、`NUMEXPR_NUM_THREADS`、`BLIS_NUM_THREADS`、`NUMBA_NUM_THREADS` 均为1；另 `PYTHONDONTWRITEBYTECODE=1`、`GIT_OPTIONAL_LOCKS=0`。输出末行：`1715 passed, 1181 subtests passed in 110.99s (0:01:50)`。

|阶段|实际UTC起止（账本）|账本stage wall秒数|
|---|---|---:|
|E0|2026-10-24 21:58:30 → 22:16:20.619289|账本仅列起止，未单列elapsed|
|E1|2026-10-24 22:16:21 → 22:39:31.421447|1390.421447|
|E2|2026-10-24 22:39:36 → 23:15:37.729595|2161.729595|
|E3|2026-10-24 23:15:38 → 23:44:39.388643|1741.388643|
|E4|2026-10-24 23:44:50 → 23:53:41.266201|531.266201|
|E5|2026-10-24 23:54:30 → 2026-10-25 00:06:46.681067|736.681067|
|E6|2026-10-25 00:07:12 → 00:14:49.970327|457.970327|
|E7|2026-10-25 00:14:51 → 首次整树核验00:56:24.875679|2493.875679（最终元数据发布后本地收据另列）|

E5账本中的文档／写作完成为00:06:46.681067 UTC；提交 `11cda8a` 的Git时间戳为00:07:09 UTC，root记录提交动作完成为 **00:07:10 UTC**。两者分别是阶段工作结束及提交完成，不混成同一计时。完整账本：[timing.jsonl](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/timing.jsonl>)。

待用户决定事项集中在 [PENDING.md](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/notes/v10/PENDING.md>) 和AUTHOR-TODO：

- 如何协调并行旧分支／旧v3目录漂移；本轮不恢复、回滚或改旧工作。
- 作者、机构、联系方式、ORCID、funding、conflicts、AI声明及源数据权利条件由作者本人完成，全部占位保持。
- 17合约的外推界限、个体dealer和prospective first-release证据仍未完成；不用放宽筛选或新模型凑数。
- 三刊官方认证分区、最终期刊及真实投稿由作者决定；JoF仅按scope列为第一目标。
- 原始本地设计对象／受限输入的安全回放路线待决定。浏览器文件树发布不转移原研究Git历史；原提交／私有bundle不公开。
- 仅发布 `revision-v10`，不开PR、不合并、不关闭旧PR。Git CLI没有可用非交互凭证，GitHub connector写分支返回403；因此使用现有、已授权的Chrome owner会话，在GitHub官方页面直接分批提交到 `revision-v10`。浏览器发布提交与原本地研究提交身份分别披露。

已确认的发布核验路径：26批473文件通过官方浏览器发布，每批用Git只读fetch核验路径、模式和blob。随后3925个tracked文件的整树核验PASS，见publication-first-tree.json；受保护旧refs最终再次核对14/14PASS，见publication-protected-refs.json。原始研究提交c587d5d与网页提交不同，内容树完全相同；原研究历史保存在本地专用ref与bundle，不把私有历史推送到远端。试运行归档首次网络提交未生效，确认远端仍为前一提交后重新提交同一文件；这不是科学计算重试。

E7已经超过原30分钟预算，首次整树验收在45分钟硬上限前完成。最终元数据发布、branch对齐和总用时存本地 .scratch/v10/final-remote-tree.json（该最终记录不自包含自身提交）。不追加分析。此前8个旧目录文件的外部漂移仍是未消除限定。

Compare入口：[fixedv9base...revision-v10](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/compare/0d2526cc69092c5158437a0509613bac5e86d47f...revision-v10)。
