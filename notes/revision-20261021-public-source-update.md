# Research source update: path extrema and the measurement of dealer exposure

This update clarifies the closest financial precedents and what the available exposure series measures. It records literature findings and reading limits; it introduces no new empirical result, selected model, or revised evaluation protocol. Two points narrow the prospective contribution: financial path-extreme quantiles have a direct established precedent, and client-flow exposure should be distinguished from a dealer's observed book after active hedging.

For reference, the response under discussion is

$$
P_{t,H}=\max_{0\le h\le H}|N_{t+h}|,
\qquad B_t=|N_t|,
\qquad G_{t,H}=P_{t,H}-B_t.
$$

The window includes the current record. These are sampled exposure levels and headroom, rather than price losses, collateral requirements, or settlement cash.

## 1. MaxVaR is a direct path-extreme quantile precedent

**Jacob Boudoukh, Matthew Richardson, Richard Stanton and Robert F. Whitelaw (2004), “MaxVaR: Long-Horizon Value at Risk in a Mark-to-Market Environment,” Journal of Investment Management 2(3):14–19.** The [journal's issue directory](https://joim.com/year/2004/) and [author publication list](https://pages.stern.nyu.edu/~rwhitela/research.html) identify the publication. The consulted [nine-page author version](https://pages.stern.nyu.edu/~rwhitela/papers/maxvar.pdf) has no explicit manuscript date and is not asserted to be identical to the six-page published layout. No DOI was verified.

**Reading scope:** all nine pages of author-version text, with the central formulas and monitoring discussion visually checked; no calculation or simulation was reproduced.

MaxVaR takes the worst cumulative portfolio loss relative to initial value over a horizon and studies its tail threshold. Fixed holdings and a constant-parameter lognormal diffusion underpin the calculation. Thus both “take a path extreme, then its quantile” and the motivation that endpoint risk misses interim risk are established financial ideas. The present response differs economically and mathematically: it is a two-sided absolute exposure level, with a known current floor, rather than a one-sided loss relative to initial wealth.

The source also distinguishes discrete from continuous monitoring. Its illustrative ratios depend on the process, drift, volatility, horizon, loss definition and monitoring convention. They supply no universal inventory-capacity multiplier. Under zero log-return drift, the crossing probability doubles at the same threshold; this does not double the quantile. Without an identified intrarecord process, a recorded peak cannot establish coverage of unobserved continuous-time excursions.

## 2. W20 already contains substantive conditional forecasting

**Wojciech Wisniewski, David Lindsay and Siân Lindsay (2020), “Application of Conformal Prediction Interval Estimations to Market Makers' Net Positions,” PMLR 128:285–301.** [Official record](https://proceedings.mlr.press/v128/wisniewski20a.html); [proceedings PDF](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf).

**Reading scope used for this update:** data and methods in §§2–3.4, especially physical PDF pp.2–8, and §4.1's discussion. This is a passage-specific account; figures were consulted through text and captions.

The target is the next-hour signed position, with two-sided prediction intervals. Position lags, calendar/session features, fitted regression engines, normalized conformal prediction and quantile variants precede the present comparison. A simple reanchoring rule therefore cannot represent the entire class of conditional exposure forecasters. Published endpoint scores cannot be inserted into a peak-forecast comparison: the response, forecast windows and scoring problem differ.

Crucially, §3.1 describes a sample of client flow, with market-maker-side changes equal and opposite to client fills. This supports a client-flow exposure proxy. It does not establish observation of external hedge execution, all desks and accounts, or the complete actively controlled dealer book. Reusing that source does not create independent validation.

## 3. The thesis chapter is now available and strengthens the direct lineage

**Wojciech Jakub Wisniewski, “Net Position and Retail Trader Behaviour: Implications for Market Makers' Risk Management Strategies,” Royal Holloway doctoral thesis.** The [institutional record](https://pure.royalholloway.ac.uk/en/publications/net-position-and-retail-trader-behaviour-implications-for-market-/) gives 2024 and an award date of 1 October 2024; the cover of the [official PDF](https://pure.royalholloway.ac.uk/ws/portalfiles/portal/63018039/2024WisniewskiWJWphd.pdf) says 2023. These are different bibliographic roles. No DOI was verified.

**Reading scope:** cover, abstract and contents; all Chapter 6 text, physical pp.107–125 / printed pp.106–124; selected §2.4 data descriptions, physical pp.29–35. This is not a complete 139-page thesis read. The official PDF resolves the earlier source list's limited-access status for these passages.

Chapter 6 retains the signed next-hour endpoint. It develops normalized conformal prediction using a fitted error scale with additive regularization, a mature conditional-scale precedent. Its tables differ from W20 and are not independent replications. Table 6.2 reports proportions of tests passed across nominal levels, not empirical coverage percentages; most conditional-coverage tests reject. Its preliminary CQR finding concerns that endpoint study and supplies no result for the present peak response.

The data chapter describes the January 2014–January 2017, five-currency-pair hourly USD client-flow sample. It does not supply the missing external hedge records. Applying an established conditional method to the peak label would be a method transfer, with target-specific performance still to establish.

## 4. WAA separates client exposure, generated hedges and the resulting position

**Najim Al-Baghdadi, Yuri Kalnishkan, David Lindsay and Siân Lindsay (2022), “Online Portfolio Hedging with the Weak Aggregating Algorithm,” PMLR 179:149–168.** [Official record](https://proceedings.mlr.press/v179/al-baghdadi22a.html); [original PDF](https://proceedings.mlr.press/v179/al-baghdadi22a/al-baghdadi22a.pdf).

**Reading scope:** all twenty pages of text, including loss definitions and arguments; graphs and calculations were not reconstructed. The PDF's internal pp.1–20 differ from its proceedings pagination.

The paper explicitly distinguishes client position, an offsetting hedge generated by the strategy, and the resulting overall position. Its empirical comparison includes an unhedged client benchmark. The inputs cover three currency-specific client-exposure/price/PnL series from February 2014 to June 2017; overlapping authors and dates establish neither identical files nor an independent second broker.

Its cylinder experts and aggregation choose hedge fractions and are evaluated through PnL, drawdown and related criteria. These are control decisions, not calibrated passive peak quantiles. Expert-combination guarantees require their stated convexity and loss-spread assumptions and do not establish peak coverage. The linked [author repository](https://github.com/Najim-Al/PhD_AA) was inspected only at metadata and top-level documentation; no explicit licence was verified and serialized financial inputs were not inspected. A public link alone does not establish redistribution permission or replication completeness.

## 5. Actual dealer records sharpen the measurement distinction

**Geir Høidal Bjønnes and Dagfinn Rime (2005), “Dealer behavior and trading systems in foreign exchange markets,” Journal of Financial Economics 75(3):571–605, [DOI](https://doi.org/10.1016/j.jfineco.2004.08.001).** The consulted body is the [Norges Bank Working Paper 10/2003](https://www.norges-bank.no/globalassets/upload/import/publikasjoner/arbeidsnotater/pdf/arb-2003-10.pdf?v=09032017122305), whose title page dates it 27 November 2003; final-journal equivalence is unverified.

**Reading scope:** §§1–2 and the §3 opening with selected inventory definitions and half-life discussion on physical pp.1–12; selected quote-shading passages and Tables 9–10 on pp.21–22; and §5.1 through Table 12 and the opening of §5.2 on pp.22–24. Not all derivations, tables or appendices were read.

The data comprise complete transaction records for four dealers at one bank, including customer and multiple interdealer channels. This is closer to observed controlled inventory than a client-flow scalar. Inventory adjustment need not operate through the dealer's own quotes: active trades provide other channels. The findings do not identify which mechanism generated the proxy's increments or supply a passive peak-quantile guarantee.

## 6. Mature comparisons remain informative without becoming new methods

**Jeremy Berkowitz and James O'Brien (2002), “How Accurate Are Value-at-Risk Models at Commercial Banks?” Journal of Finance 57(3):1093–1111, [DOI](https://doi.org/10.1111/1540-6261.00455).** Consulted: [FEDS 2001-31](https://www.federalreserve.gov/pubs/feds/2001/200131/200131pap.pdf), physical pp.1–15 and selected tables/references through p.20, rather than the entire working paper or final article. Its simple conditional comparator and discussion of PnL measurement mismatches motivate a fair, response-matched reference; they provide no inventory data or transferable performance result.

**Jacob Boudoukh, Matthew Richardson and Robert F. Whitelaw (1998), “The Best of Both Worlds: A Hybrid Approach to Calculating Value at Risk,” Risk 11(5):64–67.** Consulted: all thirteen text pages of the [longer author manuscript](https://pages.stern.nyu.edu/~rwhitela/papers/hybrid%20risk98.pdf), not asserted identical to the published layout. Recency-weighted historical tails are mature. Its probability weighting and interpolation differ from conditional scale filtering and a step-CDF quantile; any transfer must specify those choices rather than rename them as innovation.

For the existing constructions—F pooling native historical headrooms and S reanchoring historical increment paths to the current position—shared-side dominance can make the candidates identical; zero anchors and tied positive/negative peaks need explicit treatment. Even wholly positive native windows allow synthetic opposite-side excursions after reanchoring; in that setting, with a nonnegative current anchor, a common pool and rank imply only the capacity ordering $S\ge F$. These are deterministic geometric facts, not a validated conditional law, a market mechanism, or a ranking of forecast losses.

The remaining research question concerns a precisely measured sampled exposure and the behavior of specified historical representations under an appropriate comparison. These sources strengthen the case for an established conditional reference while narrowing the claims that the comparison could support. They establish neither a new path-risk functional nor capital savings, deployed hedge benefits, or external replication.
