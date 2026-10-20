# Reading update 02 — conditions that must survive method transfer

20 October 2026. **Literature review continues.** The six-hour reading requirement is not complete. This update contains selected primary-text reading and a search queue, not an experiment or a chosen manuscript.

## Updated and additional primary sources

| Source | Actual scope in this batch | Consequence for a financial application |
|---|---|---|
| Wang, Wang and Ziegel, [E-backtesting, 2209.00991v6](https://arxiv.org/abs/2209.00991v6), revised 15 April 2026 | PDF pp.8–16; definitions, Theorems 1–2, Proposition 1 | ES validity requires the stated auxiliary VaR/spread conditions. A monitored threshold of 10 is not a generic 5% test. |
| Jiao, Wang and Zhao, [Comparative e-backtests, 2511.05840v2](https://arxiv.org/abs/2511.05840v2), revised 5 March 2026 | PDF pp.10–20, 42–44; two mathematical pages visually checked | Conditional score dominance is different from average performance. Restarts and future-loss bounds need separate checking. |
| Wang and Yu, [ES-only e-backtesting, 2610.17681v1](https://arxiv.org/abs/2610.17681v1), 13 October 2026 | PDF pp.5–13, 17–19, 32–33, 36–37 | The ideal profiled statistic and its finite parameter-grid approximation have different guarantees. |
| Choe and Ramdas, [Comparing Sequential Forecasters, 2110.00115v6](https://arxiv.org/html/2110.00115v6), 9 November 2023; Operations Research 72(4), 2024 | Selected §§4.2–4.4 | Prefix-average conditional score differences and pointwise dominance already have distinct established methods. |
| Shin, Ramdas and Rinaldo, [E-detectors](https://nejsds.nestat.org/journal/NEJSDS/article/59/text), NEJSDS 2, 229–260, 2024 | Selected §§2.1–2.4 and delay assumptions | Restart-based change detection with average-run-length control is mature; it does not automatically bound the probability of ever alarming. |
| Choe and Ramdas, [Combining Evidence Across Filtrations, 2402.09698v5](https://arxiv.org/html/2402.09698v5), 15 March 2026 | Selected §§1.2–1.3, 3.1, 6 | Coarser-filtration e-processes generally need adjustment before combining them under the full information set. |
| Arnold, Gavrilopoulos, Schulz and Ziegel, [Sequential model confidence sets, 2404.18678v4](https://arxiv.org/html/2404.18678v4), 22 January 2026 | Selected §2 and §3.1 | Selecting among many risk forecasters requires a clearly defined superior-model set and multiplicity control. |

The first row corrects the initial v5-as-latest reference: the v6 submission history and fixed PDF are now checked. For comparative e-backtesting, the v2 PDF title page is dated 6 March, while arXiv's revision is 5 March UTC; HTML's unrelated internal August date is not used as a version date. Reading scope is retained rather than retrospectively relabeling earlier screening as a full review.

## A direct new overlap alert

Jing Li and Haibin Zhu, [Sequential Confidence Sets for Coverage-Constrained Conformal Model Selection, 2609.28522v1](https://arxiv.org/abs/2609.28522v1), 22 September 2026, explicitly targets selection among adaptive pipelines under coverage constraints, with delayed multi-horizon extensions. **Only its abstract and metadata were screened here.** Its theory, empirical setup and code still need examination. It blocks an immediate claim that combining coverage constraints and sequential pipeline selection is an untouched problem.

## Questions to answer before design

- Does the decision require an adequately calibrated risk forecast, a better average score, or a useful alarm for a change? Choose the estimand before choosing the test.
- Does a proposed multi-day adaptation preserve the information available when each prediction was issued and when its outcome settles?
- Is a claimed bound for one monitoring process, all assets/models, or repeated restarted processes? Record the actual error metric.
- Does a numerical shortcut preserve the theorem's candidate set, or merely converge toward it as computation increases?

These checks refine the candidate list. They do not establish novelty, prove that an empirical result will be favorable, or replace the remaining reading.
