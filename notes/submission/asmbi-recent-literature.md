# ASMBI 近年相关文献：H5 准备

只从 Wiley 官方论文页核实元数据和摘要；筛选范围为正式期刊年份 2021–2026，选入三篇直接相关论文。UTC 访问窗口：2026-10-27 00:59:21–00:59:44。没有下载 PDF，没有修改稿件，没有提交或调用外部模型。

以下正文语境句是待采用的写作建议，证据只覆盖摘要。不得据此声称已审读未访问的全文、复核定理或重现论文数值。

| 引用键 | 作者与正式年 | 卷期、页码或文章号 | 直接相关主题 |
|---|---|---|---|
| LeeKim2024ASMBI | Sangyeol Lee; Chang Kyeom Kim (2024) | 40(4), 1012–1038 | 条件分位数顺序监测、VaR/ES、金融日收益 |
| Pagnottoni2026ASMBI | Paolo Pagnottoni (2026) | 42(1), e70067 | 金融分布预测、预测误差的时间与分位依赖 |
| MuddanaEtAl2025ASMBI | Thanoj K. Muddana; Komal S. R. Bhimireddy; Anandamayee Majumdar; Rangan Gupta (2025) | 41(5), e70042 | 分位回归、尾风险、递归样本外波动预测 |

两点元数据容易误写：Lee 论文有 **Lee 和 Kim 两位作者**；Pagnottoni 论文首发为 **2025-12-30**，但正式卷期和官方 How to cite 是 **2026**，故 BibTeX 用 2026。

## Sequential monitoring for conditional quantiles of general conditional heteroscedastic time series models

官方来源：[Sequential monitoring for conditional quantiles of general conditional heteroscedastic time series models](https://onlinelibrary.wiley.com/doi/abs/10.1002/asmb.2865)；DOI：[10.1002/asmb.2865](https://doi.org/10.1002/asmb.2865)。
正式期刊年：2024；首发：2024-05-13；卷 40、期 4；页码 1012–1038。

摘要支持的相关点：在线顺序监测位置–尺度异方差时序的条件分位数变点，摘要明确联系 VaR/ES 风险管理；用 KOSPI 与 EuroStoxx 50 日收益实证。
短引：`sequentially detect change points in the conditional quantiles`（8 词）。
建议用途：用于说明金融条件分位数和时序稳定性已是本刊相关议题。
证据边界：这是变点监测研究；摘要不能支持本稿模型优于其方法，或本稿静态评价量具有新颖性的结论。
访问范围：Official metadata, abstract and How to cite read. Main article full text was not accessed or reviewed; no PDF downloaded.

可放正文的简洁语境句：

\citet{LeeKim2024ASMBI} develop sequential monitoring procedures for changes in conditional quantiles of heteroscedastic time series, with applications to financial return data.

BibTeX 字段：

```bibtex
@article{LeeKim2024ASMBI,
  author = {Lee, Sangyeol and Kim, Chang Kyeom},
  title = {Sequential monitoring for conditional quantiles of general conditional heteroscedastic time series models},
  journal = {Applied Stochastic Models in Business and Industry},
  year = {2024},
  volume = {40},
  number = {4},
  pages = {1012--1038},
  doi = {10.1002/asmb.2865},
  url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/asmb.2865}
}
```

## Optimal Transport Autoregression to Forecast High-Frequency Financial Data Distributions

官方来源：[Optimal Transport Autoregression to Forecast High-Frequency Financial Data Distributions](https://onlinelibrary.wiley.com/doi/10.1002/asmb.70067)；DOI：[10.1002/asmb.70067](https://doi.org/10.1002/asmb.70067)。
正式期刊年：2026；首发：2025-12-30；卷 42、期 1；文章号 e70067。

摘要支持的相关点：用最优传输自回归预测 Bitcoin 高频收益与波动分布；摘要报告误差依赖时间与分位数，极端分位附近误差上升且不单调。
短引：`forecast errors are highly time- and quantile-dependent`（7 词）。
建议用途：用于说明应在多个分位和时间位置检查金融分布预测表现。
证据边界：摘要针对其最优传输模型和 Bitcoin 数据；不能外推为所有金融模型的普遍定理，也不能据此声称本稿已解决极端分位问题。
访问范围：Official HTML contains full text, but this record uses only abstract, author and bibliographic metadata; no full-text review or PDF reading is claimed.

可放正文的简洁语境句：

\citet{Pagnottoni2026ASMBI} study distributional forecasts of high-frequency Bitcoin returns and volatility, reporting forecast errors that vary across time and quantile levels.

BibTeX 字段：

```bibtex
@article{Pagnottoni2026ASMBI,
  author = {Pagnottoni, Paolo},
  title = {Optimal Transport Autoregression to Forecast High-Frequency Financial Data Distributions},
  journal = {Applied Stochastic Models in Business and Industry},
  year = {2026},
  volume = {42},
  number = {1},
  pages = {e70067},
  doi = {10.1002/asmb.70067},
  url = {https://onlinelibrary.wiley.com/doi/10.1002/asmb.70067}
}
```

## Forecasting Gold Returns Volatility Over 1258–2023: The Role of Moments

官方来源：[Forecasting Gold Returns Volatility Over 1258–2023: The Role of Moments](https://onlinelibrary.wiley.com/doi/10.1002/asmb.70042)；DOI：[10.1002/asmb.70042](https://doi.org/10.1002/asmb.70042)。
正式期刊年：2025；首发：2025-09-15；卷 41、期 5；文章号 e70042。

摘要支持的相关点：先用 Bayesian 时变参数分位回归构建波动、尾风险和矩指标，再作递归样本外线性预测并比较自回归基准。
短引：`recursively estimated linear predictive regressions over the out-of-sample periods`（9 词）。
建议用途：用于说明时间顺序的样本外验证和明确基准比较在本刊金融预测应用中的位置。
证据边界：研究目标是波动预测，不能将其等同于本稿的分位损失目标或宣称摘要证明某种分位评价标准有效。
访问范围：Official metadata, abstract and How to cite read. Main article full text was not accessed or reviewed; no PDF downloaded.

可放正文的简洁语境句：

\citet{MuddanaEtAl2025ASMBI} use quantile-regression-derived measures of tail risk and higher moments in recursive out-of-sample forecasts of gold-return volatility.

BibTeX 字段：

```bibtex
@article{MuddanaEtAl2025ASMBI,
  author = {Muddana, Thanoj K. and Bhimireddy, Komal S. R. and Majumdar, Anandamayee and Gupta, Rangan},
  title = {Forecasting Gold Returns Volatility Over 1258--2023: The Role of Moments},
  journal = {Applied Stochastic Models in Business and Industry},
  year = {2025},
  volume = {41},
  number = {5},
  pages = {e70042},
  doi = {10.1002/asmb.70042},
  url = {https://onlinelibrary.wiley.com/doi/10.1002/asmb.70042}
}
```

只新增本文件与 JSON；没有把这些引用插入论文。
