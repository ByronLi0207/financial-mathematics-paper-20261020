# Remaining-payment ratios and the timing of funding needs

22 October 2026. Selected primary reading and a constructed measurement example. No financial observation, forecast, target, primary comparison or model choice is changed by this note.

Arjani, Li and Sabetti's *Monitoring Intraday Liquidity Risks in a Real Time Gross Settlement System* is a direct precedent for prospective payment-system liquidity assessment. The [official PDF](https://www.payments.ca/sites/default/files/discussion_paper_monitoring_intraday_liquidity_risks_in_a_real_time_gross_settlement_system.pdf) cover gives **23 April 2020**. Its remaining-day indicator is `LRI=RPD/(PI+CL+RPI)`: payment demand divided by net payment income, credit limits and remaining receipts. Its later probability construction concerns exceeding an LRI threshold. This is a different functional from this manuscript's sampled absolute-position maximum; it also needs different inputs.

The root reader consulted selected abstract/introduction, target, data/split and bootstrap passages, including physical pp.8–15 and 21–24, and visually checked the cover and physical pp.9–10. This is not a full 36-page reading or a replication of its models. The consulted PDF is 7,004,098 bytes, SHA-256 `cb1860bc7d46faefbbb3fa34e47f4cf49299956654377405f87021f798fef8b4`. The copyrighted PDF and page renders remain private. No public participant-level transaction dataset was verified.

The following example is our own arithmetic illustration, not a result reported in that paper. At one common current time, stipulate net payment income zero, credit capacity five, and exactly one remaining receipt and payment, each ten. Both possible instruction orders give `LRI=10/(0+5+10)=2/3`. Adopt the convention that a cumulative net-receipt path is receipts minus payments, starting from zero. Before imposing settlement constraints, the two planned paths are:

| Order of instructions | Planned cumulative net receipts | Absolute peak | Directional funding peak before credit | Uncovered amount after credit five |
|---|---|---:|---:|---:|
| Pay, then receive | `[0,-10,0]` | 10 | 10 | 5 |
| Receive, then pay | `[0,10,0]` | 10 | 0 | 0 |

Thus the same remaining totals and current ratio do not identify a timing-sensitive peak. The equal absolute peaks also do not identify a directional requirement. These are statements about the displayed functionals at this common time, not a criticism of the paper's full forecasting or probability framework. Its indicator can update as events occur. In an actual system with credit five, the first payment of ten might queue until a receipt or additional resources arrive; the first row must not be called an unconstrained path of already settled transactions.

This example does not identify either manuscript source's position measurement with settlement cash. A prospective funding study would additionally need institution-level payment instructions and timestamps, opening resources, credit/collateral availability, settlement and queuing rules, and a defensible issue-time information convention. A downloaded securities-value aggregate or source-reported client position cannot supply those quantities by relabeling its maximum.

The related primary lead by Carlos León, *Estimating financial institutions' intraday liquidity risk: a Monte Carlo simulation approach*, Banco de la República Borradores703, 15 April 2012, DOI [10.32468/be.703](https://doi.org/10.32468/be.703), already motivates confidence-level maximum daily funding needs. Selected team reading reached physical pp.2–10 and the opening of p.11; later body access failed. The root did not personally read those body passages. Its exact later peak formula, prospective test and data release remain unverified. This lead weakens a broad novelty claim; it is not evidence that the present exact response-and-data comparison has been reproduced elsewhere.

The direction decision remains a bounded forecasting application and validation benchmark. Financial peak-risk prediction is established territory. The present target, completed-label timing and same-response comparisons must stand on their own; none supplies measured collateral savings, an optimal funding decision or a new general estimator.
