# F4.5 — Table 1 original-source check

Checked 25 October 2026. Scope: the eight rows of Table 1 in `submission-v10/manuscript.tex`, including the existing seven external studies. This note supplies the manuscript owner with replacement wording; it does not edit the manuscript, bibliography, numerical results or Git state.

## Decision and exact replacement

Retain four columns: **Study, Response, Data unit, Evaluation**. Delete **Peak floor, Label timing, Source scope** in their entirety. The floor column currently contains five unexplained dashes plus a partly empty payment-thesis cell. The timing column mixes analytic calculations, predictor timing and label availability; it is not a uniform comparison of the same property. The scope column adds little information beyond Data unit and encourages unsupported transfer interpretations. Do not replace their gaps with “No”, “N/A”, or a claim of absence.

Use the following complete matrix. All 32 cells, including study identities, have the support recorded below. The evaluation column describes reported evaluation approaches; it does not imply that every paper conducts an identical forecasting experiment.

| Study | Response | Data unit | Evaluation |
|---|---|---|---|
| Wisniewski et al. (2020) | Next-hour signed-position interval | One market maker's hourly FX positions | Pinball and interval scores; coverage tests |
| Boudoukh et al. (2004) | Worst cumulative portfolio-return quantile | Fixed portfolio under a lognormal diffusion | MaxVaR/VaR ratios; discrete-monitoring simulation |
| van den Hoogen (2017) | Conditional quantile of cumulative payment-deficit peak | ABN AMRO transaction accounts | Coverage and independence backtests |
| Duffie et al. (2023) | Capacity, Treasury illiquidity and PnL tail quantiles | Dealer positions, transactions and PnL | Illiquidity regressions; out-of-sample PnL pseudo-R² |
| Engle and Manganelli (2004) | Conditional return quantile | GM, IBM and S&P 500 daily returns | Quantile objective, exception rates and DQ tests |
| Ehm et al. (2016) | Quantile and expectile forecast comparison | Economic and wind-speed forecasts | Elementary-score curves and score differences |
| Meinshausen (2006) | Conditional response quantile | Regression datasets | Cross-validated quantile loss |
| This study | Sampled absolute-position peak | FX positions; weekly position aggregates | Pinball loss, breaches, model confidence sets and costs |

Caption:

> Related studies: reported targets, data units and evaluation approaches.

Delete the existing table footnote in full. In particular, remove both the statement that the payment-thesis reading is partial and the input-byte-identity disclaimer. This replacement makes no input-byte-equality claim, and it makes no claim about unpublished payment results. The access and version details belong in this source note.

## Original passages actually read in this pass

Page numbers below are one based. “Physical” denotes the PDF page position. Body passages were read in extracted primary text; the Delft passages were returned from the institution's indexed original PDF. Previously written audit notes were used only to find sources and page locators. They are not substituted for a current original-source read.

### W20 — Wisniewski, Lindsay and Lindsay (2020)

Primary: [PMLR original PDF](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf). Seventeen physical pages; cover directly confirms authors, title and year.

| Retained cell | Passage actually read and support |
|---|---|
| Response | Introduction, physical/local p.2: prediction of the market maker's net position in the next hour; §2 interval construction is visible on p.4. |
| Data unit | §3.1, physical/local p.4: a sample of one market maker's client flow, five liquid currency pairs, hourly positions in USD. |
| Evaluation | §3.5, physical/local pp.9–10: coverage, width and Winkler score; averaged lower/upper pinball losses; UC, CC and independence tests. |

No claim of identical files between W20 and this study is needed or retained.

### MAX — Boudoukh, Richardson, Stanton and Whitelaw (2004)

Primary: [author-hosted final journal-layout PDF](https://pages.stern.nyu.edu/~rwhitela/papers/maxvar%20joim04.pdf). Cover confirms *Journal of Investment Management*, 2(3), 1–6, 2004 and all four authors. Physical and printed pp.1–6 coincide. Body pp.2–5 were directly read.

| Retained cell | Passage actually read and support |
|---|---|
| Response | §2, pp.2–3: the minimum path value and minimum cumulative return over the horizon; a probability threshold defines MaxVaR. |
| Data unit | pp.2–3: portfolio composition is fixed and portfolio value follows a lognormal diffusion with specified drift and volatility. |
| Evaluation | §3, pp.3–5, Tables 1–2 on p.4: MaxVaR/VaR ratios across parameter cases; discrete monitoring is evaluated by simulation. |

“Quantile” describes the risk threshold, while “diffusion” makes clear that this row is model based.

### H17 — van den Hoogen (2017)

Primary: [TU Delft original PDF](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f), also [its preview route](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1). Direct open/download attempts timed out. Fresh searches of these exact institution-hosted originals returned the cover and the body passages below, including their printed page labels. This is an indexed-original reading, not a newly obtained full thesis. Cover: Sofie van den Hoogen, August 2017.

| Retained cell | Passage actually read and support |
|---|---|
| Response | §5.2, printed p.59, Eq.(5.2): maximum cumulative negative transaction position within the interval; p.60, Definition 5.1 / Eq.(5.3): its conditional quantile is the intraday risk measure. |
| Data unit | Chapter 4, printed p.32, around Eq.(4.7): transaction process for two specific accounts at ABN AMRO Bank. |
| Evaluation | §5.4, printed p.68, Definitions 5.3–5.4 / Eqs.(5.32)–(5.33): unconditional coverage and independence hypotheses for forecast violations. |

Also read §5.3, p.60: ACD timing, UHF-GARCH net-position generation and Monte Carlo estimation. The original “EVT methodology” evaluation cell mixes method and evaluation and is replaced. The proposed cell does not assert numerical backtest outcomes or access to confidential results.

### D23 — Duffie et al. (2023, revised October)

Primary: [New York Fed Staff Report 1070](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf). Seventy physical pages. Cover/title pages confirm six authors, August 2023 and October 2023 revision.

| Retained cell | Passage actually read and support |
|---|---|
| Response | Introduction, printed pp.1–3 (physical pp.3–5): dealer capacity and Treasury illiquidity; Appendix E, printed pp.58–59 (physical pp.60–61): daily PnL quantiles used for VaR. |
| Data unit | Introduction, printed pp.2–3: BrokerTec and TRACE transactions, dealer-level FR 2004 positions, and BHC/desk PnL/VaR. |
| Evaluation | §7, printed pp.24–27 (physical pp.26–29), Figure 7 and Table 1: illiquidity quantile regressions and pseudo-R²; Appendix E, printed pp.58–59, footnote 27 and Table E.12: in-sample and daily expanding-window out-of-sample PnL pseudo-R². |

The row preserves the report's distinct tasks; it does not treat dealer PnL as the present position-peak target.

### EM04 — Engle and Manganelli (2004)

Primary: [author-hosted published CAViaR PDF](https://simonemanganelli.org/Simone/Research_files/caviarPublished.pdf). Fifteen physical pages, printed pp.367–381. Cover confirms title and authors. The cover/introduction, selected model/evaluation passages and Table 1 were read; this is the published article, not the earlier working paper.

| Retained cell | Passage actually read and support |
|---|---|
| Response | p.367, abstract and introduction: time-varying conditional return quantile / VaR. |
| Data unit | §6, p.371 (physical p.5): GM, IBM and S&P 500 daily return series constructed from Datastream prices. |
| Evaluation | p.371, DQ test discussion; Table 1, p.372 (physical p.6): regression-quantile objective, in/out-of-sample exception proportions and DQ p-values. |

“DQ” is the original paper's dynamic quantile test. Its assumptions are not being transferred to the present application by the table.

### EGJK16 — Ehm, Gneiting, Jordan and Krüger (2016)

Primary metadata: [publisher record](https://rss.onlinelibrary.wiley.com/doi/10.1111/rssb.12154) and [KIT record](https://publikationen.bibliothek.kit.edu/1000055110), directly checked: 2016, 78(3), 505–562, DOI 10.1111/rssb.12154. The current body read is the authors' [arXiv v2](https://arxiv.org/pdf/1503.08195v2), title date 20 April 2015, revision 17 April 2015. The page numbers below are its physical/printed preprint pages, not journal pages.

| Retained cell | Passage actually read and support |
|---|---|
| Response | Abstract p.1 and discussion p.26: consistent quantile/expectile score comparisons and mixture representations. |
| Data unit | §4.1, p.22; §4.3, p.25; Figure 5, p.23: economic forecasts and hourly wind-speed quantiles. |
| Evaluation | p.22 and Figure 6, p.24; pp.25–26: Murphy diagrams of empirical elementary scores and their differences. |

The publisher's abstract independently confirms the elementary-score/Murphy-diagram interpretation. Full journal-body access was not obtained; no journal-page locator is invented.

### M06 — Meinshausen (2006)

Primary: [JMLR original PDF](https://jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf). Seventeen physical pages, printed pp.983–999. Cover directly confirms title, author and year.

| Retained cell | Passage actually read and support |
|---|---|
| Response | p.983, abstract/introduction, and p.984, Eq.(1): conditional distribution and conditional response quantiles. |
| Data unit | §5, pp.992–993 (physical pp.10–11): multiple regression datasets, with examples including housing, ozone and fuel. |
| Evaluation | §5, p.993 (physical p.11), Evaluation paragraph: quantile weighted absolute loss with five-fold cross-validation and bootstrap comparisons. |

The old “Conditional distributions” evaluation cell describes an estimand rather than an evaluation measure; replace it with cross-validated quantile loss.

### Current study — owning manuscript

Read `submission-v10/manuscript.tex`: title and abstract; target equations and propositions; data section; comparison design; model-confidence-set subsection; cost section. This directly supports the sampled absolute peak, FX/weekly aggregate units and named evaluation components. The row reports the manuscript's design and metrics; no numerical value was recalculated and no new result is asserted. The v12 manuscript owner should retain the same row after the new analyses are integrated, because none changes these broad descriptors.

## Application checklist

1. Replace the seven-column table with the four-column matrix above, preserving all eight rows and their narrative citations.
2. Use the short caption; remove the current table footnote entirely.
3. Do not add a source-equality, global-priority or external-validation claim while removing that footnote.
4. Confirm the compiled table has four header cells and four entries in every row, and that no dash, “unverified”, “partial”, or input-byte disclaimer remains in Table 1.

Only this source note and the separate Lévy-reference note are authored by this literature subtask. No financial data were downloaded and no forecasting/statistical experiment was run. A structural readback confirmed eight rows, four columns, and no placeholder/disclaimer in the proposed matrix. No Claude or cross-model review was used.
