# E5 关键文献一手来源核对

访问日期：2026-10-24 UTC。范围为现稿书目／引用句与作者、出版社或机构原文记录的只读对照；不是全书目逐条审计。没有改稿、下载金融数据、读取真实 NPZ、拟合／重算预测，亦未调用 Claude 或跨模型复审。一项独立的同模型研究子任务协助核对以下一手来源；本记录区分元数据核对、摘要可读与全文核对，不把 DOI 可解析等同于全文已读。

## 核对清单

| 文献 | 核准的出版元数据 | 现稿状态与需处理项 | 本轮证据范围 |
|---|---|---|---|
| Diebold–Mariano 1995 | Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, **13**(3), 253–263. DOI `10.1080/07350015.1995.10524599`。 | 投稿主稿及 `.bib` 的作者、年、题名、卷期页和 DOI 正确，无需据线上日期改年。 | Taylor & Francis 官方搜索索引的出版元数据和摘要；直接全文／DOI入口返回403，未逐段核全文。 |
| Giacomini–White 2006 | Giacomini, R., & White, H. (2006). Tests of conditional predictive ability. *Econometrica*, **74**(6), 1545–1578. DOI `10.1111/j.1468-0262.2006.00718.x`。 | 现稿及 `.bib` 元数据正确。主文应保留有限工具条件预测能力诊断的限定，不能声称本实现的全部渐近条件已由该引用验证。 | Wiley 官方原文页的元数据、摘要可核；首次出版2006-11-01。未完成全文算法／假设的逐项复核。 |
| Hansen–Lunde–Nason 2011 | Hansen, P. R., Lunde, A., & Nason, J. M. (2011). The model confidence set. *Econometrica*, **79**(2), 453–497. DOI `10.3982/ECTA5771`。 | 当前投稿 `manuscript.tex`、`supplement.tex`、`references.bib` 未检出该条目／MCS 引用。v10 如报告实际 MCS，须新增正文引用与完整书目。不能把现有 DM+Holm 直接改称 MCS。 | Wiley 原文元数据与作者所属 Aarhus University 文献记录交叉一致；出版社首次线上出版2011-02-14。本轮不声称已核原文全部算法细节。 |
| Duffie et al. 2023 | Duffie, D., Fleming, M. J., Keane, F. M., Nelson, C., Shachar, O., & Van Tassel, P. (2023). *Dealer capacity and U.S. Treasury market functionality*. Federal Reserve Bank of New York Staff Report **No. 1070**. August 2023, revised October 2023. DOI `10.59576/sr.1070`。 | 现稿作者顺序／题名与报告身份准确。建议补月份、修订月份，`.bib` 报告编号明确为1070；不是期刊论文，卷期页不适用。 | NY Fed 官方报告页及官方 PDF；Appendix E（PDF第59页，正文页码58）直接核对每日 PnL 预测分位数回归和 expanding-window 样本外描述。 |
| Avellaneda–Stoikov 2008 | Avellaneda, M., & Stoikov, S. (2008). High-frequency trading in a limit order book. *Quantitative Finance*, **8**(3), 217–224. DOI `10.1080/14697680701381228`。全名 Marco Avellaneda、Sasha Stoikov。 | 旧 `manuscript/working-paper` 有此条目且字段正确；当前投稿主稿／`.bib` 未列。若恢复引用，应说明其库存风险和主动报价目标与本文 peak forecasting 不同。 | Taylor & Francis 出版社页与 NYU 作者主页的期刊版 PDF；作者 PDF 首页的卷期页及 DOI 可直接核对。 |

## 一手直接来源与当前文件定位

1. **DM1995**：[Taylor & Francis／DOI](https://doi.org/10.1080/07350015.1995.10524599)。核对定位为 `submission-jof/manuscript.tex:163,361` 与 `submission-jof/references.bib` 的 `dm1995`。出版社所示2012-07-02是 online 日期，不能覆盖1995卷期的正式书目年。
2. **GW2006**：[Wiley 原文页](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2006.00718.x)。现稿定位 `submission-jof/manuscript.tex:232,371`，补充材料 `supplement.tex:1227–1230` 已保留矩、依赖、协方差等未验证假设及 joint rejection 可由无条件均值差驱动的边界。
3. **HLN2011**：[Wiley 原文页](https://onlinelibrary.wiley.com/doi/10.3982/ECTA5771)、[Aarhus 作者机构记录](https://pure.au.dk/portal/en/publications/the-model-confidence-set/)。这两处用于核元数据；具体 arch 版本、R statistic、bootstrap、消除规则、种子与成员边界以独立冻结的 `protocol/v10/mcs-design.md` 及软件官方实现核对为准。
4. **Duffie SR1070**：[NY Fed 官方报告页](https://www.newyorkfed.org/research/staff_reports/sr1070)、[官方 PDF](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf)。现稿定位 `submission-jof/manuscript.tex:50,63,363`；报告日期和编号补充应同步到 companion `.bib`。
5. **A–S2008**：[Taylor & Francis 出版社页](https://www.tandfonline.com/doi/abs/10.1080/14697680701381228?needAccess=true)、[NYU 作者主页期刊版 PDF](https://math.nyu.edu/inmemoriam/avellaneda/HighFrequencyTrading.pdf)。旧 working-paper 定位 `manuscript/working-paper/main.tex:295,607` 及对应 `.bib`。本轮没有把旧 working-paper 的存在误报为投稿稿已引用。

行号是本次读取时的定位，后续修订可能移动；应按 citation key／题名再次定位。此处只给修改建议，所有论文和书目文件保持不动。

## 引用用途与不能越过的边界

**DM** 可作为两个程序的配对损失比较动机，适用于非二次和非对称损失语境。引用它不自动保证本研究重叠标签、重复估计和所用 HAC／小样本修正下的检验有效；现稿 working-reference 表述应保留。它也不是模型集合选择的替代品。

**GW** 支持条件预测能力评价方向。现稿用训练期确定的 RMS 状态和损失差条件矩作为有限工具诊断，方向相容；这不是对全部条件分布或条件覆盖的检验。建议主文采用“finite-instrument conditional predictive ability diagnostics motivated by Giacomini and White (2006)”这类限定，避免把引用变成已验证所有依赖／矩条件的证明。

**HLN** 支持从预先确定的候选集合构建 model confidence set。候选程序、完整共同损失轴、bootstrap 和消除规则仍是本研究须明确的实现选择。集合成员资格不等于未来普适最优性；已有 DM p 值加 Holm 校正也不会自行产生 HLN MCS。

**Duffie et al.** 可支持 dealer capacity、Treasury market functioning 及其 PnL 分位数预测背景。官方 Appendix E 的响应是每日 PnL，而本文响应是未来窗口内最大绝对净头寸。两者不是同一个风险目标；该报告不能被写成已经直接验证本文 peak-limit 响应。

**A–S** 可支持库存风险影响报价、主动报价会改变库存过程的经济动机和被动预测边界。其核心是报价控制及终端 PnL 效用，未研究本文的未来最大绝对净头寸分位数；不能把它当作 dealer peak-limit 实际采用本文目标的直接证据，也不能据它赋予本文被动预测因果控制解释。

## 交给改稿阶段的有限清单

- 若最终纳入 E3 MCS，新增 HLN2011 正文引用、书目和相应软件引用；不要只在设计笔记中提及。
- Duffie 条目补 `Staff Report No. 1070`、August 2023／revised October 2023，主稿与 `.bib` 保持一致。
- 保留 DM／GW 的 working-reference／有限工具诊断边界；不因为经典引用存在而删除实现假设限制。
- 如恢复 A–S 引用，明确主动库存控制与本文被动 peak forecast 的目标差别。
- 本轮未逐条重核所有 FR2004、支付流动性、MaxVaR、POT 等既有参考文献；不把这份五项聚焦核查写成“全部参考文献已验证”。

## 访问精度与权限

来源访问日期为2026-10-24 UTC；网页工具没有逐请求秒级时间戳，不补造该字段。出版社搜索索引／摘要支持元数据核对的条目已说明全文未读；官方全文 PDF 的用途核对仅限上面明确标出的内容。未借用他校凭据、向作者发信或作任何外发操作。
