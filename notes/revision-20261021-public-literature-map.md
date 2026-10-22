# Literature map: forecasting a sampled market-maker inventory peak

**Historical research snapshot.** The thesis-access limitation recorded below describes an early retrieval attempt on 21 October 2026. The official PDF was subsequently obtained and Chapter 6 was read; see the [source update, Section 3](revision-20261021-public-source-update.md#3-the-thesis-chapter-is-now-available-and-strengthens-the-direct-lineage). Use the [current paper evidence map](revision-20261021/paper-evidence-map.md) for the manuscript's consulted editions and cumulative reading scopes. The earlier account is retained to preserve the research chronology.

Research note, 21 October 2026. This is a source comparison for ongoing research, rather than a final research design or an exhaustive novelty claim. Reading scope describes the text consulted; it does not certify independent proof verification, numerical reproduction or implementation equivalence between editions.

The financial target under discussion is the future sampled absolute peak of a passive net-position record,

$$
P_{t,H}=\max_{0\le h\le H}|N_{t+h}|,
\qquad B_t=|N_t|,
\qquad G_{t,H}=P_{t,H}-B_t\ge0.
$$

Here the window includes the observed current position. A forecast of its upper quantile concerns recorded net inventory, with the sampling frequency and aggregation of that record. It does not automatically quantify settlement cash, collateral, gross currency exposure or an actively enforced inventory limit.

1. **Wisniewski, Wojciech; David Lindsay; Siân Lindsay (2020). “Application of Conformal Prediction Interval Estimations to Market Makers’ Net Positions.”** PMLR 128:285–301. [Official record](https://proceedings.mlr.press/v128/wisniewski20a.html); [consulted proceedings PDF](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf).

   **Read:** complete main text, equations, tables and discussion, physical pp.1–17 including references and appendix captions; figures through extracted labels/captions.

   **Comparison:** the closest inventory and data-source application already compares fitted conformal, normalized conformal and quantile-regression forecasts. Its response is the next-hour signed position and its intervals have two endpoints. The present response is a multi-record absolute maximum with a known floor. Published losses therefore cannot be compared directly. The source acknowledges broken exchangeability and reports conditional-coverage rejections; it supplies no inherited coverage guarantee for dependent, overlapping peaks. Reusing its inventory series is not independent data validation.

2. **Madhavan, Ananth; Seymour Smidt (1992 draft / 1993 article).** Consulted: **“An Analysis of Daily Changes in Specialist Inventories and Quotations,”** Wharton working paper 22-92, current October 1992, originally September 1991. [Institutional draft](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9222.pdf). Formal: **“An Analysis of Changes in Specialist Inventories and Quotations,”** *Journal of Finance* 48(5):1595–1628 (1993), [DOI](https://doi.org/10.1111/j.1540-6261.1993.tb05122.x). Final-body equivalence is unverified.

   **Read:** all 47 scanned draft pages, including the 30-page numbered body, appendix, tables and figures; final article abstract/metadata only.

   **Comparison:** inventory adjustment can depend on starting inventory and changing desired holdings. Individual-security findings do not establish zero-centered reversion in an aggregate dollar series; the draft’s aggregate-dollar regression does not reject a unit root. This motivates state conditioning, rather than supplying an inventory-peak algorithm, a transferable adjustment speed or an empirical mechanism already identified in another record.

3. **Avellaneda, Marco; Sasha Stoikov (2008). “High-frequency trading in a limit order book.”** *Quantitative Finance* 8(3):217–224. [DOI](https://doi.org/10.1080/14697680701381228); [consulted NYU author-hosted journal-layout PDF](https://math.nyu.edu/inmemoriam/avellaneda/HighFrequencyTrading.pdf). This eight-page copy is distinct from the coauthor’s October 2006 draft; publisher-byte equivalence was not newly established.

   **Read:** full eight-page text, including simulations and appendix.

   **Comparison:** utility-based quotes respond to signed share inventory, and quotes affect Poisson fill intensities. The familiar reservation-price formula and approximate active quotes are established inventory-control constructions. The objective is terminal marked wealth, rather than a passive path-maximum quantile. Brownian reference prices do not imply Brownian inventory. A passive forecast inherits neither control optimality nor a causal profit or risk-reduction claim; hourly net-dollar records do not identify the fill, quoting and utility parameters required by this framework.

4. **Guéant, Olivier; Charles-Albert Lehalle; Joaquin Fernandez-Tapia (2012 preprint / 2013 article). “Dealing with the inventory risk: a solution to the market making problem.”** Consulted [arXiv:1105.3115v5](https://arxiv.org/abs/1105.3115v5), uploaded 3 August 2012, title-page draft July 2012; [exact PDF](https://arxiv.org/pdf/1105.3115v5). Formal: *Mathematics and Financial Economics* 7:477–507 (2013), [DOI](https://doi.org/10.1007/s11579-012-0087-0); final-body equivalence is unverified.

   **Read:** full 36-page v5 text and proof appendix; other figures mainly through captions/text.

   **Comparison:** fixed-size fills, exponential intensities, CARA utility and hard inventory boundaries yield a finite linear system and verified optimal controls. The spectral quote approximation is separate. The illustrative backtest makes execution assumptions and calibrates risk aversion using that day’s inventory range. An enforced share boundary differs from a forecast level that can be exceeded. Neither the optimal-control theorem nor this illustration establishes passive peak-quantile coverage or out-of-sample superiority.

5. **Engle, Robert F.; Simone Manganelli (2004). “CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles.”** *Journal of Business & Economic Statistics* 22(4):367–381. [DOI](https://doi.org/10.1198/073500104000000370); [consulted author-hosted published PDF](https://www.simonemanganelli.org/Simone/Research_files/caviarPublished.pdf).

   **Read:** pp.367–375: main specifications, estimation, dynamic-quantile testing and application; all Appendix A assumptions and opening Appendix B proof arguments. Remaining proof pages were not fully read.

   **Comparison:** direct recursive conditional-quantile estimation by pinball loss is mature. The source predicts lower-tail returns, not inventory peaks. An upper-tail headroom adaptation must declare its recursion, predictors and delayed labels. Its density, identification and asymptotic assumptions are not established for overlapping headrooms with possible zero mass. The original nonlinear optimization is substantial; few coefficients do not establish cheap or reliable fitting. Passing selected dynamic-quantile moments would not prove calibration against all available information.

6. **Biau, Gérard; Benoît Patra (2010 v2 / 2011 article). “Sequential Quantile Prediction of Time Series.”** Consulted [arXiv:0908.2503v2](https://arxiv.org/abs/0908.2503v2), 31 May 2010; [exact PDF](https://arxiv.org/pdf/0908.2503v2). Formal: *IEEE Transactions on Information Theory* 57(3):1664–1674 (2011), [DOI](https://doi.org/10.1109/TIT.2011.2104610); final PDF not compared.

   **Read:** v2 pp.1–24: construction, assumptions, theorem, empirical protocol and proof arguments; references not separately read.

   **Comparison:** select similar historical lag vectors and take an empirical quantile of their following responses. The full theoretical procedure additionally truncates and aggregates infinitely many experts. Under stationarity, ergodicity, moments and other regularity conditions, its guarantee concerns long-run average pinball loss. A finite rolling inventory-state nearest-neighbour rule is an adaptation, without automatic inheritance of that theorem, finite-sample coverage or conditional coverage. Response maturity, distance ties and empirical versus corrected quantile ranks require explicit treatment.

7. **Barone-Adesi, Giovanni; Kostas Giannopoulos; Les Vosper (1999). “VaR without correlations for portfolios of derivative securities.”** *Journal of Futures Markets* 19(5):583–602, [DOI](https://doi.org/10.1002/%28SICI%291096-9934%28199908%2919%3A5%3C583%3A%3AAID-FUT5%3E3.0.CO%3B2-S). Consulted [USI Quaderno 99-04](https://folia.unifr.ch/documents/318043/files/wp9904.pdf), revised March 1999; final-journal-body equivalence is unverified.

   **Read:** selected prose, algorithm and application passages through physical p.27; bibliography screened. Damaged equation extraction and all numerical cells/graph pixels were not fully certified.

   **Comparison:** filtered historical simulation already samples standardized return innovations, recursively updates volatility and price paths, and revalues derivatives. Translating an observed inventory-increment envelope to the current position transfers only a scenario-revaluation principle. It is not full recursive filtered historical simulation. Filter adequacy, innovation assumptions and derivative-price evidence cannot be inherited as inventory-peak guarantees. More Monte Carlo draws do not add independently observed tail information.

8. **Hull, John; Alan White (1998). “Incorporating volatility updating into the historical simulation method for value-at-risk.”** *Journal of Risk* 1(1):5–19, [DOI](https://doi.org/10.21314/jor.1998.001). Consulted [John Hull’s publicly uploaded October 1998 manuscript](https://www.researchgate.net/publication/2645882_Incorporating_volatility_updating_into_the_historical_simulation_method_for_VaR); typeset-version equivalence is unverified.

   **Read:** selected manuscript pp.2–10, particularly forecast-time scaling, the comparison with recency weighting and capital utilization. A fresh complete original-PDF audit was not obtained.

   **Comparison:** historical changes are standardized by previously forecast volatility and rescaled to the current forecast. This changes scenario values; recency weighting changes probabilities. Their adequacy remains an assumption. Applying one scale ratio to an inventory envelope would be a declared simplified adaptation, not the recursive algorithm in item 7. Return percentages and daily smoothing choices do not transfer automatically to signed inventory crossing zero or irregularly spaced records. The source supplies no inventory-peak coverage guarantee.

9. **van den Hoogen, Sofie (August 2017). “Intraday liquidity risk estimation using transaction data: an extreme value theory approach.”** Delft MSc Applied Mathematics thesis, [institutional original](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1). No journal edition or DOI is asserted.

   **Read:** selected physical pp.19–24, 27–33, 75–94, 108–110, 126–128 and 148–152; not the entire 160-page thesis. A later retrieval timeout did not add reading scope.

   **Comparison:** a conditional quantile of the maximum cumulative negative payment balance determines a liquidity buffer. Duration/payment dynamics, simulated paths and extreme-value tail estimation provide a direct financial peak-to-buffer precedent. Payment cash is economically different from net inventory, and model-based/asymptotic tail assumptions do not furnish distribution-free finite-sample protection for inventory peaks. The confidential, partly redacted ABN AMRO transactions do not provide a public independent inventory benchmark.

10. **Liao, Jiali; Theodore V. Theodosopoulos (2005). “Study on optimal timing of mark-to-market for contingent credit risk control.”** Consulted [arXiv:math/0506077v1](https://arxiv.org/abs/math/0506077v1), submitted 4 June 2005. The PDF uses Theodore V.; the metadata uses Ted Theodosopoulos. No separate journal edition is asserted.

    **Read:** selected physical pp.3–5 and 11–14 for exposure definitions, assumptions and marking objectives; probability derivations and numerical results were not certified.

    **Comparison:** lifetime maximum collateral-adjusted exposure and its quantile are explicit financial risk targets. Brownian contract values, cash collateral and marking decisions distinguish this controlled continuous-path problem from passive sampled absolute inventory. Sequential marking minimizes an expected conditional potential-future-exposure objective, which is not automatically an unconditional maximum quantile. The precedent rules out a general first-financial-peak claim, while supplying neither comparable inventory scores nor statistical coverage for a new inventory record.

11. **Schmitt, Marc (2026). “Taming Tail Risk in Financial Markets: Conformal Calibration for Nonstationary Portfolio VaR.”** Consulted [arXiv:2602.03903v3](https://arxiv.org/abs/2602.03903v3), revised 3 August 2026; [versioned text](https://arxiv.org/html/2602.03903v3). Earlier v2 has a different title. No journal edition is asserted.

    **Read:** §§1–8 of v3 and selected physical pp.1–7; tables/figures on pp.4–6 visually checked. Code and numerical results were not reproduced.

    **Comparison:** age/regime-weighted financial residual calibration, feedback and effective-sample-size diagnostics are existing methods. Its response is one-step portfolio loss; the text excludes additional multi-day dependence from its framework. Regime-law smoothness and conditional independence are not established for overlapping inventory peaks. Effective sample size does not measure the unknown distributional discrepancy. Immediate score feedback cannot be copied when a peak label arrives only after its window completes. The recent date alone establishes neither popularity nor priority.

12. **Björn Löfdahl Grelsson (2026). “On the modeling assumptions of Historical Simulation for Value-at-Risk.”** Consulted [arXiv:2605.10066v1](https://arxiv.org/abs/2605.10066v1), submitted 11 May 2026; [fixed seven-page PDF](https://arxiv.org/pdf/2605.10066v1), printing 12 May 2026. An unversioned rendering displayed a later date and different equation numbering; it is not substituted for v1.

    **Read:** v1 body §§1–4 and references. No empirical implementation was reproduced.

    **Comparison:** historical shifts can be expressed through innovation extraction under state-dependent scales; absolute/relative shifts and filtered extensions have explicit assumptions. A shift-transform restatement is therefore insufficient evidence of new mathematical methodology. Signed inventory crossing zero makes price-relative scaling problematic, while a future peak requires a conditional path law beyond a one-step shift. Innovation adequacy, drift choices and the proposed estimation approach are not established for this inventory task; no transferable performance or coverage guarantee follows.

**Related thesis, access-limited:** Wojciech Wisniewski (2024), *Net Position and Retail Trader Behaviour: Implications for Market Makers’ Risk Management Strategies*, [Royal Holloway doctoral record](https://pure.royalholloway.ac.uk/en/publications/net-position-and-retail-trader-behaviour-implications-for-market-/). The official record gives an award date of 1 October 2024; the indexed PDF cover shows 2023. Official indexed passages at printed pp.16,106,110 identify contributions, a chapter with W20's title and reuse of the 2014–2017 source. The full PDF was inaccessible in the current check. These fragments are not a full-thesis read and do not exclude a closer peak treatment elsewhere in it.

The sources motivate a conditional comparison. Because the current floor is known, conditional translation gives $q_\tau(P_{t,H}\mid\mathcal F_t)=B_t+q_\tau(G_{t,H}\mid\mathcal F_t)$. Adding $B_t$ to a pooled historical headroom quantile does not itself condition that headroom distribution on the current signed state. CAViaR and Biau–Patra show that direct and local conditional quantile methods are mature alternatives; the inventory papers explain why state and policy can matter. This motivates evaluating a transparent conditional reference on the actual peak response, without choosing a final specification here. Since $|P_{t,H}-B_t|=G_{t,H}$, a floor-plus-residual-quantile construction is already a special case of mature residual calibration; renaming it does not create a new conformal algorithm. Neither a changed response nor a corrected order-statistic rank establishes the assumptions of an inherited theorem.

**Independent-data candidate: New York Fed primary-dealer statistics.** Official FR 2004A Treasury-bill net outright positions, key `PDPOSGS-B` (historical predecessor `PDPUSGTBNOP`), are aggregate long-minus-short market-value positions, in millions of dollars, at Wednesday close. Read: official forms/instructions, reporting changes, metadata, release policy and reuse terms; no observations or targets were evaluated. The changing dealer panel, netting and valuation distinguish this from one broker’s hourly inventory. The [statistics page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) gives Thursday publication; the [2004 announcement](https://www.newyorkfed.org/newsevents/news/markets/2004/an040115.html) specifies a one-week lag. Normally, the next Wednesday observation already exists when the preceding one becomes public. Naive next-week forecasting would therefore mix nowcasting and forecasting. Historical as-released vintages remain unverified. A separate weekly aggregate application may be defensible, but direct operational replication is not established. [API documentation](https://markets.newyorkfed.org/static/docs/markets-api.html); [reuse conditions](https://www.newyorkfed.org/privacy/termsofuse.html).
