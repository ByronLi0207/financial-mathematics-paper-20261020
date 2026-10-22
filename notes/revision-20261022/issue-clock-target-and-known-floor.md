# Issue clock, revisions and the known-floor target

22 October2026. This is a design and identification note, not a new forecast experiment or a change to the accepted study. It follows the [official vintage feasibility audit](official-release-vintage-feasibility-agent.md). The actual paper remains an economic-date replay of a fixed downloaded vintage. No original prediction, score, source hash or executable freeze changes here.

## The missing object is an information history

The current [NYFed owning page](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics) describes Thursday-afternoon publication of prior-week statistics; the [2004 announcement](https://www.newyorkfed.org/newsevents/news/markets/2004/an040115.html) establishes the historical move to a one-week lag. [ALFRED Help](https://alfred.stlouisfed.org/help) distinguishes original-source release, provider release and first FRED availability, while [FRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html) separate economic dates from information intervals. These sources establish why issue information must be defined. They do not supply this study's complete original-vintage archive. The exact NYFed-series mapping to ALFRED remains unverified.

Write s for an economic observation date, a for the public availability timestamp of a specific version, and N_s^[a] for that version's value. At a public forecast issue u, a value is admissible only when a<=u; a present-day HTTP retrieval timestamp is not the original availability timestamp. If a provider stores only dates, a same-day ordering convention must be fixed conservatively before analysis. Publication at a normal afternoon time does not establish each historical intraday timestamp.

A reproducible information table would need at least the economic date, source-series definition, value, first-publication/version identifier, availability interval, source evidence, and precision of the timestamp. An unchanged release occasion is still an issue occasion even if a change-only vintage-date endpoint omits it. Missing releases, revisions, schema periods and holiday delays need explicit handling; inferring all of them from a weekday offset is not verified vintage reconstruction.

## Why adding a feature lag is insufficient

The paper's sampled target is P_(t,H)=max_(h=0,...,H)|N_(t+h)|. Its headroom is G=P-|N_t|, with known floor B=|N_t|. Within the accepted economic-date fixed-vintage construction, this floor is an algebraic consequence of including h0 and is used consistently in every method. For a public forecaster at economic date t, however, N_t is generally not yet released. Using lagged regressors but retaining this unreleased B leaves future information in the report.

Moving the issue to a later release also changes the question. Some economic observations after the latest published date can already have occurred by issue u while still being unknown publicly. Forecasting their subsequent publication is a valid information problem, but it includes nowcasting an already elapsed economic interval. It must not be described as a purely future-inventory risk forecast from u.

Revisions create a second, distinct floor issue. An issue-time reported anchor and a later-vintage realization need not share the same h0 value. An invented example demonstrates the point: the last publicly reported anchor is10 at issue; a subsequent revision makes it4; all future selected economic observations have magnitudes at most3. A final-vintage peak that includes the revised anchor is4, below the purported issue-time floor10. Thus nonnegative headroom relative to the old report does not follow for that different target. This is elementary target arithmetic, not a claim that such a revision occurred in the acquired data. The example supplies neither a new theorem nor a measured revision effect.

## Three coherent future contracts answer different questions

| Contract | Target and known anchor | What it can establish if the necessary archive exists |
|---|---|---|
| Fixed-vintage economic-date analysis, current paper | Future recorded peak and h0 from one accepted snapshot; issue information is idealized at the economic date | A bounded historical method comparison on the declared sampled response; no verified public-information replay |
| Release-native report forecast | Freeze the last available anchor at issue; take a maximum with explicitly selected subsequent first-publication reports | Forecasts of later publicly reported magnitudes, possibly describing economic dates already elapsed at issue; preserves a floor by its declared definition, not by identifying current true exposure |
| Future economic-path forecast at a public issue | Select economic dates strictly after the issue according to an explicit calendar, and a fixed realization-vintage rule | A future economic response under the chosen observation convention; the last publicly reported position is a lagged covariate and need not be a lower bound on that future path |

For the release-native contract, revisions to old dates must not silently count as new future economic observations. If the target instead follows every change in the displayed latest report, it is a different publication-process target and must be named accordingly. Combining an issue-frozen anchor with later first-release values also creates a mixed-vintage constructed response; it is not a continuously observed common-vintage inventory path.

For the future economic-path contract, adding the old public anchor to the maximum can force a known floor, but changes the estimand. It becomes the maximum of a stale reported magnitude and a future selected path. It cannot be sold as an unchanged estimate of the actual future peak. A genuinely internal dealer study could know its contemporaneous position, but public aggregate NYFed data do not establish that access or reproduce the dealer's information set.

## Training and testing must use the same availability rule

A complete economic-date label i+H<=r is not automatically a label available by a public refit u. Each needed realization version must have become available under the declared rule. If final revised values are used to fit a model at an earlier historical issue, label completion in economic time does not prevent revision leakage. Conversely, labels may be evaluated later using a prespecified realization rule without having been admissible for training at the earlier issue.

The design must therefore bind predictor versions, anchor versions, complete-label eligibility, refit dates, validation choices, forecast origins, and the evaluation-realization rule to one contract. It must specify whether a frozen historical label is restated when revised, and which version a saved forecast will be scored against. The model cannot be compared across methods with different availability conventions under a claim of matched information.

Overlapping outcome windows and release delays must also enter any dependence or coverage argument. The current fixed-terminal phase proof uses maturity spacing for its explicitly fixed sampled response. An actual public-release study would need its own verified label-resolution times; copying H+1economic-record spacing does not by itself establish that the previous hit is known at the next phase issue.

## Decision for this revision

Keep the current paper's explicit economic-date downloaded-vintage boundary. Do not relabel it as a live backtest, replace only selected regressors, borrow a generic ALFRED capability as proof of this series' membership, or infer absence of an archive from a failed search. A future availability study can begin only after the necessary series/vintage mapping and timing evidence are established and a complete new target/information contract is frozen. No financial fit is justified by this memo alone.
