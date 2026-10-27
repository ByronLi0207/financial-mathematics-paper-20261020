# 候选审稿人核验记录

核验日期：2026-10-26（America/Vancouver；网页读取日期相同）。本记录只供投稿准备，不属于论文正文或 Online Supplement。

## 范围与判定规则

候选来源为只读 Git 对象 `6192ec370d131c60d05e9fb103150e0e9db6aa23`（`origin/final-jof`）的 `notes/final-merge/suggested-reviewers.md`，共 5 人。问答来源为同一对象的 `notes/final-merge/anticipated-questions.md`，共 10 条。来源分支的科学叙述不直接移入当前稿件。

当前科学基线为 `8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6` 的 v13。根 README 指定 `submission-v10/` 为当前稿件；保留的 `submission-jof/` 是旧稿。学术相关性以当前 `submission-v10/manuscript.tex`、`supplement.tex` 及其 `generated/v13-supplement.tex` 为准。

核验只采用成功读取的官方机构网页、机构出版物目录或官方出版社网页；不把搜索引擎摘要、私人社交页面或姓名相似作为通过依据。下文短引是网页原文；“与本文相关”是根据已核实研究领域和当前稿件作出的学术匹配判断，不是机构的推荐意见。未下载论文或其他文件，未联系候选人，未注册或操作投稿账户，也未进行 GitHub 操作。

成熟出版实践要求把研究能力与利益冲突分别核查。Wiley 当前[研究诚信与出版伦理指南](https://authors.wiley.com/ethics-guidelines/index.html)的 Conflicts of interest 原文为："should disclose interests that might appear to affect their ability to present or review work objectively"；Peer review 部分明确以专业能力和潜在冲突为选择依据（读取 2026-10-26）。这支持保留可追溯专业证据，同时把未掌握的作者关系留待作者确认；本记录不据此推定目标期刊要求恰好提交 5 人。

## 逐人核验

### 1. Tilmann Gneiting — 事实核验通过，提名资格待作者确认

- **官方身份与领域：** Heidelberg Institute for Theoretical Studies（HITS）Computational Statistics 组负责人；Karlsruhe Institute of Technology（KIT）Institute of Statistics 的 Computational Statistics 教授。官方个人页同时列明预测、统计概率及经济金融应用。
- **直接证据：** [HITS 官方个人页](https://www.h-its.org/people/prof-dr-tilmann-gneiting/)，读取 2026-10-26。短引："Group Leader Computational Statistics"；"Professor of Computational Statistics"；"Theory and Practice of Forecasting"。页面履历将 KIT 的 Institute of Statistics 标为自 2025 年起的机构名称。
- **本文匹配判断：** 一致分位数评分、预测比较、Murphy 图以及评分与破线频率、固定成本偏好之间的区别，分别对应主文 §5、§7.5、§8 和补充 S9、S33。本文已引用其预测评分研究。
- **状态边界：** 通过的是官方身份与专业匹配核验；未核实本人可用性、是否愿意审稿或与作者的私人关系。

### 2. Raffaella Giacomini — 事实核验通过，提名资格待作者确认

- **官方身份与领域：** University College London（UCL），Department of Economics，Professor of Economics；研究领域为 Econometrics and Applied Macroeconomics。
- **直接证据：** [UCL 当前学术人员目录](https://www.ucl.ac.uk/social-historical-sciences/economics/our-staff/academic-and-teaching-staff)，读取 2026-10-26，列名并标为 "Professor"。[UCL 2026 年官方讲座页](https://www.ucl.ac.uk/engineering/events/2026/mar/perceived-shocks-and-impulse-responses)，读取 2026-10-26，短引："Professor of Economics in the Economics Department at UCL"；"Econometrics and Applied Macroeconomics"。
- **相关研究记录：** [UCL Economics Research 官方目录](https://github-pages.ucl.ac.uk/UCL-Economics-Research/people/raffaella-giacomini/)，读取 2026-10-26，列有条件预测能力、条件分位数评价及不稳定环境中的预测比较。该目录若干年份为记录年份，未用它替换当前稿件已核对的文献出版年份。
- **本文匹配判断：** 训练与验证窗口、配对损失比较、条件预测能力、回溯选择及验证边界变化，主要对应主文 §6、§7.4 和 §9.1。删除来源草案推荐理由中的旧 WP2 定位。

### 3. Roger Koenker — 事实核验通过，提名资格待作者确认

- **官方身份：** UCL，Department of Economics，Honorary Professor；另有 University of Illinois Urbana-Champaign，Department of Economics，Professor Emeritus 身份。两个身份分别记录，不将荣誉或荣休头衔改写为普通在职教职。
- **直接证据：** [UCL 荣誉人员目录](https://www.ucl.ac.uk/social-historical-sciences/economics/our-staff/honorary-staff)，读取 2026-10-26，短引："Roger Koenker"、"Honorary Professor"。[Illinois 官方个人页](https://economics.illinois.edu/profile/rkoenker)，读取 2026-10-26，短引："Professor Emeritus"。
- **研究领域证据：** [Cambridge University Press 的 Quantile Regression 页面](https://www.cambridge.org/core/books/quantile-regression/C18AE7BCF3EC43C16937390D44A328B1)，读取 2026-10-26，作者列 Roger Koenker；书籍说明短引："estimating models of conditional quantile functions"。此处以出版社说明核实分位数回归专长，不以 2005 年书籍中的单位作当前任职证据。
- **本文匹配判断：** 惩罚分位数回归、无限惩罚的截距极限、普通经验分位数与 corrected-rank 历史规则的区别，以及 99% 分位数修复的一致性门槛，分别对应主文 §5、§7.4、§9.1 和补充 S38。可用性仍待作者核实。

### 4. Fabian Krüger — 事实核验通过，提名资格待作者确认

- **官方身份与领域：** KIT，Applied Econometrics，Professor of Economics；研究涉及概率预测和预测评价。
- **直接证据：** [KIT 学院当前教授目录](https://www.wiwi.kit.edu/english/professors.php)，读取 2026-10-26，列其姓名、Applied Econometrics 与 STAT。[KIT 官方个人页](https://ewifo.stat.kit.edu/english/21_57.php)，读取 2026-10-26，短引："Professor of Economics, Karlsruhe Institute of Technology"。个人页页脚最后更新为 2022-12-05，因此与当前学院目录交叉核实身份。
- **研究领域证据：** [KIT Applied Econometrics 官方研究页](https://ewifo.stat.kit.edu/english/26.php)，读取 2026-10-26（页脚更新 2026-05-20）。短引："Probabilistic forecasting"；"Theory and methods for forecast evaluation"。该页列有 Ehm、Gneiting、Jordan、Krüger（2016）的共同评分论文。
- **本文匹配判断：** 预测排序、评分偏好、概率预测评价和保留负面比较，主要对应主文 §7.5、§8 及补充 S9、S32–S33。

### 5. Robert F. Engle — 事实核验通过，提名资格待作者确认

- **官方身份与领域：** New York University Stern School of Business，Professor Emeritus of Finance；Volatility and Risk Institute 共同负责人；专业涉及时间序列、金融市场和动态风险模型。
- **直接证据：** [NYU Stern 官方高管教育页面](https://execed.stern.nyu.edu/pages/robert-engle)，读取 2026-10-26，短引："Professor Emeritus of Finance"；"Co-Director, The Volatility and Risk Institute"。[NYU 官方个人简介](https://web-static.stern.nyu.edu/rengle/about/)，读取 2026-10-26，短引："expert in time series analysis"；页面明确列出 CAViaR 等研究方法，并将 NYU 荣休身份列为 2021–Present。
- **本文匹配判断：** CAViaR 对照、时间序列风险监测、校准与实际风险政策之间的解释边界，主要对应主文 §5、§7.5、§10 和补充中保留的 headroom SAV/校准结果。匹配不意味着已获本人同意或可用性确认。

## 冲突与名单使用边界

5/5 候选通过机构、身份与专业相关性事实核验；原 5 人中因事实无法核验而排除者为 0。**5/5 的利益冲突与提名资格均为“待作者确认”，已确认无冲突者为 0。** 作者姓名、全部单位、合作史尚未提供，不能从网页上没有出现作者名字推导无冲突。

作者正式提名前，需按目标期刊当时的要求逐人确认近期合作、师生关系、同机构关系、私人或经济关系、相关编辑角色及可用性。名单内已有两组重合：Giacomini 与 Koenker 均列 UCL；Gneiting 与 Krüger 均有 KIT 身份且有合著记录。这些是候选之间的已知关系，不能替代对每位候选与全体作者的冲突检查，也不支持将这 5 人称为相互独立的外审。

邮箱统一保持 `[author to verify]`。成功读取的机构页面虽有联系资料，本任务未导入或使用。来源旁注另提 Meinshausen，但其不在原 5 人名单；本轮未增加第六位候选。个别首次请求超时或 403（包括 NYU 标准 faculty bio 路径），均使用成功读取的官方机构页面解决，没有绕过访问控制。

## 问答迁移检查

新 `author-qa.md` 保留 10 条问答的主题连续性，但将所有定位更新为 v13：旧 WP2 运行顺序及 PARTLY/P1–P3 问答分别改为 v13 的设计边界、拒绝采用的高分位数修复，以及基准默认流程的通过/失败条件。旧稿 W520、10/17、6/17 和七个 WP2 反例代码不作为 v13 结果导入。成本、复现、验证长度及高分位数答案均以当前稿件和保存记录为依据，不新增科学分析或改动结果。
