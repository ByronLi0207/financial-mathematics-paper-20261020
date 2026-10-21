# Research design: historical anchoring for sampled inventory peaks

Status: frozen before computing this study's labels, forecasts or losses, at 2026-10-21T05:46:37Z. The recorded active literature requirement is21600seconds and active design requirement7200seconds, excluding waiting and parallel overlap. CandidateA is selected. Operative specification SHA-256: `0b8eda7bfd858c038bae22a96a7caa5ff21838317de58bc56eef98ca696c54ff`; output-schema SHA-256: `3bef13d68c65160b9642d715344e10a4e40ddb52c6439d09a9b5573b54e6b752`. This is a local specification freeze, not external preregistration, a manuscript or an empirical result.

## Financial question and candidate decision

The research question is whether pooling completed historical peak headrooms at their own inventory states improves the declared forecasting loss relative to revaluing completed historical increment envelopes at the current inventory state. Both constructions are mature empirical-quantile/historical-scenario methods. Their comparison concerns a passive measurement of a recorded inventory process, with simple level and current-state comparators retained.

Three applications were compared before outcomes were scored:

| Candidate | Observable and mature transfer | Reason for the current ranking |
| --- | --- | --- |
| A: sampled net-position peak | Order statistics of completed headrooms versus current-anchor historical scenarios for a maximum of recorded absolute net positions. | A small, exact versioned source is accessible; the target and anchoring difference can be stated explicitly. This supports a limited empirical application, not a new calibration algorithm. |
| B: prospective maximum drawdown | Direct functional quantiles versus historical future paths for a precisely reset investment interval. | Existing direct/indirect drawdown and maximum-drawdown work is closer. A separate data vintage, wealth convention and initial high-water definition would add unresolved scope. |
| C: operating-cash deterioration | Historical quantiles of a public cash-balance response with a verified release lag. | Current schema/access/revision evidence remains incomplete. Observed financed balance changes cannot simply be called unfinanced cash need. |

Candidate A is selected on source feasibility, target clarity and the particular empirical comparison. It is not preferred because of measured forecast performance; none has been computed. The prior candidate/rejection notes retain the broader literature and access evidence. Neither B nor C will become a post-result escape route from an adverse result in A.

The question changes both historical representation and anchor treatment. Consequently F versus S identifies the difference between two complete deterministic constructions, not a separately identified compression benefit or causal effect of current inventory. F itself uses current absolute inventory through its known floor. No learned conditional-state model is fitted.

## Closest work and claim boundary

Wisniewski, Lindsay and Lindsay (2020) already study hourly net-position interval forecasting, rolling updates and pinball. Their experiment uses a scalar hourly net-position response; its benchmark section explicitly predicts the next time epoch. The introduction's phrase about the next hour alone is not the basis for asserting a path-maximum distinction. The present response is explicitly a maximum of absolute recorded positions across several subsequent records. Different targets and procedures prevent direct comparison with their published scores.

Financial peak quantiles also precede this study: van den Hoogen's 2017 thesis concerns a maximum cumulative payment-cash deficit; Liao and Theodosopoulos (2005) model maximum collateral-adjusted contingent exposure and intervention timing. This is not a first financial peak-buffer, inventory-prediction, conformal or historical-simulation claim. The potential contribution is a bounded, reproducible empirical comparison and its observed limits. A changed response alone does not establish methodological novelty or a remaining exhaustive literature gap.

Historical-scenario generation and current-state revaluation also have established financial precedents, including Barone-Adesi, Giannopoulos and Vosper (1999; March working-paper edition read). Their filtered recursive return/valuation construction is not implemented here: S instead reanchors complete observed increment paths, without a fitted filter, innovation draws or derivative pricing. The transfer is the scenario-revaluation principle, not its original probability premises.

Gneiting's point-forecast framework supplies the standard quantile scoring interpretation. Politis and Romano supply the geometric-block resampling mechanism. The beyond-exchangeability and recent financial-calibration papers provide context; their assumptions and results are not imported as guarantees for this sequence.

## Source, measurement and information convention

Use version 2 of `davidlindsay1979/net-position-time-series-dataset`, requested single member `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv`. Accepted CSV identity is 1,286,391 bytes and SHA-256 `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`. The 274 MB complete collection is unnecessary and outside the raw-data budget. Only `datetime` and `NetPosUsd` are used; the other three fields are not candidate predictors or profit evidence.

Outcome-free feasibility checks established 18,576 ordered rows, exact field names, used-field finiteness and valid naive timestamps. The file runs from 2014-02-05T01:00:00 to 2017-01-24T00:00:00. Its 18,575 adjacent intervals include 18,420 one-hour and 155 forty-nine-hour gaps. Those structural checks do not compute this study's peak labels, capacities or losses. Broad raw-level patterns in the predecessor paper were read; the historical source context cannot be called completely unseen.

The source describes hourly USD net positions accumulated from market-maker client flow in five liquid currency pairs. A single netted scalar does not identify gross multicurrency exposure, mark-to-market P&L, margin or settlement cash. Timezone, intrarecord extrema and field-release/vintage conventions are unverified. Record index t is assumed available immediately before issuing the indexed forecast, after observing record t; this is an explicit retrospective information convention, not proof of live executability.

The visible rights label attributes data files to original authors. Anonymous access does not establish raw redistribution permission. Raw CSV/ZIP, source PDFs and reconstructive origin traces stay local. Public provenance gives the exact source, version, member, retrieval procedure and hash. A present mismatched file stops without replacement; absent-source fetching is explicit, bounded and confined to the verified one-file endpoint. The two-request route disables automatic redirects and implicit proxies, closes redirect/error bodies without reading them, and validates the single allowed storage redirect before a bounded ZIP read.

## Target and completed historical information

Let N_t denote signed source-reported USD inventory and B_t=|N_t|. For H subsequent recorded observations, including the known origin state in the maximum, define

    P[t,H] = max(|N[t+h]| : h=0,...,H),
    G[t,H] = P[t,H] - B[t],
    a[i,H] = min(N[i+h]-N[i] : h=0,...,H),
    b[i,H] = max(N[i+h]-N[i] : h=0,...,H),
    D[i,H] = max(b[i,H], -a[i,H]).

Because P includes the current observation, a forecast below B is pointwise dominated by B under the declared pinball loss. This motivates the known floor; it does not make B an adequate risk limit.

H counts recorded steps, not clock hours or continuous-time protection. No sorting, dropping, imputation or interpolation repairs the path. The target includes B_t, so P>=B and G>=0. A between-endpoint spike belongs to this target even when the endpoint returns to its starting value.

At actual issue t, the common calibration origins for a cell are exactly t-H-n+1,...,t-H. Every historical label ends at i+H<=t. A partial label is never mixed with completed labels. The latest completed label may end at t: that record is already observed under the convention. The issuer receives a restricted completed-window view plus independently supplied t, current inventory and CellSpec. Inferring t from the supplied label ends would be a tautological maturity check and is forbidden.

## Fixed menu and constructions

| Cell | H | n | tau | Exact prediction rank |
| --- | ---: | ---: | ---: | ---: |
| main | 6 | 720 | 19/20 | 685 |
| h12 | 12 | 720 | 19/20 | 685 |
| h24 | 24 | 720 | 19/20 | 685 |
| n480 | 6 | 480 | 19/20 | 457 |
| n1440 | 6 | 1440 | 19/20 | 1369 |
| tau90 | 6 | 720 | 9/10 | 649 |
| tau99 | 6 | 720 | 99/100 | 714 |

This is seven one-factor-at-a-time cells, not a Cartesian search. For n finite candidates, Q denotes their ceil((n+1)*tau)-th smallest value. Keep duplicates; do not interpolate, jitter or add decimal rounding. A generic unavailable rank returns positive infinity; a configured unavailable rank is a structural stop. Recompute the exact integer rank and assert the expected value rather than overriding it.

For the same completed pool and issue origin, in fixed method order:

    F: selected cF = Q(G_i);                         CF = B + cF.
    S: s_i = max(N_t+b_i, -N_t-a_i) - B;
       selected cS = Q(s_i);                        CS = B + cS.
    R:                                               CR = B + Q(D_i).
    L:                                               CL = max(B,Q(P_i)).
    P0:                                              CP0 = B.

S uses the two directional extrema of a completed increment path; these are sufficient for the maximum absolute value at any fixed anchor. They are not merely the first and last observations of that path. The canonical stored S computation selects headroom first and then adds the common B, matching F's operation sequence. Private selected allowances and public issued extra C-B remain distinct when floating addition collapses a difference.

Exact-arithmetic geometry gives F<=R and S<=R, but no universal F/S ordering. These mechanical bounds are not the main empirical hypothesis. Simple L and P0 may outperform the specialized constructions and must remain visible. No source observation is assumed to be a future support bound.

## Chronology, contrast and falsifiability

Construct one ordered common evaluation-origin vector for all seven cells: naive timestamp at least 2016-01-01, t at least the full-menu maximum warmup 1445, and t no later than T-1-24. For the pinned row count the last admissible source index is 18551. The actual common count and first eligible index are obtained only during the frozen run. Every origin has equal weight. Later forecasts may use earlier evaluation labels once they have fully matured.

This is a retrospective specification holdout with prequential completed-label feedback. It is not external preregistration, a permanently unseen test set or a live trial. Broad source-paper knowledge and the source selection are acknowledged. Choices are frozen before computing these study-specific losses, not claimed independent of all prior knowledge of the record.

Use stored e=P-C and direct pinball

    rho = float(tau)*max(e,0) + float(1-tau)*max(-e,0),

with both weights converted separately from exact fractions. The primary within-cell series is d=loss_F-loss_S, retaining every zero. Its equal-origin mean is the primary contrast; negative favors F. An assertion that F improves on S on the primary record requires a negative mean; a nonnegative mean fails that finite-record claim. This is not a formal population hypothesis test.

Report all five mean losses, capacities, issued extras, raw strict breach counts/rates, unconditional positive overruns, conditional mean overruns with their breach denominator, and unused allowance. No-breach conditional severity is undefined with a reason, not zero. Relative paired difference is mean(d)/mean(loss_S) only when the denominator is positive. Do not subtract rounded displayed losses to create the primary contrast.

Pinball is a standard quantile-consistent objective, with primary underprediction weight nineteen times the overprediction weight. Those weights are not observed dealer costs. Conditional expected-loss optimality characterizes a conditional quantile under its moment conditions; it does not prove F/S optimal for the current state. Nor is ceil((n+1)*tau) generically the unique empirical-risk minimizer: at n720/tau99 it selects rank714 while an ordinary lower empirical quantile has rank713. The rank convention is described as an upper prediction rank.

## Dependence and descriptive stability

Overlapping targets, calibration windows and persistent inventory states make the record dependent. A six-phase split does not make the derived comparisons independent. No actual augmented-score exchangeability, stationarity, mixing rate or inferential-bootstrap premise is established. Claims of finite-sample, current-state-conditional, simultaneous or anytime coverage are excluded.

For the primary ordered d vector, retain circular stationary-bootstrap-style mean profiles at ell=120,240,720,1440, with 999 replicates per length. Use one PCG64 SeedSequence([20261020,ell]) stream for all replicates at that length. Draw a uniform start then a positive-support geometric block length with p=1/ell; continue circularly and truncate only the last block to exactly M consumed positions. Do not refit forecasts, center on a null, reject long blocks or select a favorable length.

Report the observed mean separately from the replicate average; SD has divisor998 and is centered on the replicate average. Endpoints are ordinary one-based order statistics25 and975. Report ell/M and expected used blocks1+(M-1)/ell; the latter is not effective sample size. All four rows and actual endpoints remain visible. They are descriptive resampled-mean ranges, not confidence intervals, standard errors or superiority probabilities.

A finite exactly constant vector returns its stored constant directly for the mean. Constant d produces999 analytically equal means per length, equal endpoints and SD0, with explicit constant/shortcut flags. It does not require actual block draws. Mean zero alone does not trigger that branch, and a degenerate output does not by itself prove a deterministic population effect.

## Diagnostics, arithmetic and interpretation

Primary-only panels use exact current sign, development-only absolute-position terciles, original source-index t modulo6, every naive origin calendar month and a retrospective future-gap-free flag. Development ranks are ordinary ceil(m/3) and ceil(2m/3); coincident thresholds keep empty groups. Future gap flags are evaluation descriptions, never predictors or eligibility filters. No interactions, fitted associations, smoothing or favorable subgroup selection are added.

Groups with fewer than30 origins retain count/status but uniformly withhold metric values; zero-origin groups remain intentional rows. No extra minimum-breach rule is imposed. Every observation remains in global evaluation, calibration and resampling. The public table has61 rows per intentional group, including small/empty groups.

Raw error signs, equality and breaches are never overwritten by tolerance. Separately record the fixed32eps common-scale auxiliary events and numerical near coincidence. Maturity/pool errors and finite issued capacity below B stop exactly. Only upper geometry permits the declared tiny arithmetic discrepancies without clipping. A realized future peak above any forecast is a scientific failure event, not a structural reason to stop.

Cross-cell checks include shared origins, same-H target identity, increasing-H target and L ordering, increasing-tau capacity ordering, and P0 identities. F/S/R have no universal horizon order. Conditional severity and auxiliary flags do not inherit every raw-event monotonicity. The four computed mechanism categories distinguish equal candidate scores, changed scores with equal selected allowance, changed allowance with equal stored capacity, and different stored capacities.

Stable aggregation and explicit independent artificial oracles check arithmetic without turning an error bound into an inferential result. Constant means, source-index phases, future-mutation positive controls, between-endpoint spikes, coherent F/S reversals, rounding collapse and identical explicit block traces are in the small validation matrix. No check has passed merely because its expected value is written down.

If F improves on S but L/P0 is better, report only the limited pairwise result. Mixed sensitivities, unstable monthly comparisons, large overruns, exact ties and degenerate profiles remain. Smaller allowances are not cash savings; a changed live limit or hedge could change the path, whose intervention counterfactual is not observed here.

## Computation and deliverables

Use existing Python/NumPy/ReportLab only: no installation, GPU, trained model, long search or persistent service. One fresh analysis process requests one numerical thread before imports, stops if observed own-process OS threads exceed2, and measures elapsed time plus Darwin-byte peak RSS. Budget limits are600 wall seconds per run,2GiB RSS,100MiB raw and25MiB per download; warning/early-stop margins and output/buffer limits are in the frozen machine specification. Unavailable required measurements are unverified failures, not zero. Snapshot thread maxima are not continuous peaks.

The original scope is all seven cells, five methods and four primary profiles. If unchanged computations remain oversized after routine implementation fixes, a separately versioned primary-only amendment may omit all six sensitivities together while retaining the original common origins, all five methods and all four profiles. This is a resource fallback, not result-based selection; incomplete original attempts and produced partial outputs remain recorded.

The public output map is four exact CSVs, an explicit sanitized manifest, and three original aggregate vector figures with one canonical set inside the eventual manuscript project. It excludes raw/ZIP/source PDFs, per-origin traces, thresholds, full d, full replicates, local paths and credentials. The output schema is frozen first; its SHA-256 is embedded in the frozen study spec, avoiding a hash cycle. Code/source/spec identities precede financial evaluation.

After verified outputs exist, write the English working paper, compile the saved TeX source, obtain a real standalone PDF and inspect every rendered page. Compiler diagnostics do not export a PDF; a separate formatting fallback cannot prove uncompiled TeX compilable. Publish only the explicit artifact set to the existing GitHub repository, then verify actual fixed-commit paths and bytes. At the24-hour checkpoint audit the true active time and any missing artifacts, continuing essential work if incomplete. Routine implementation and publication are already authorized.

## Primary source pointers

- Wisniewski, W., D. Lindsay and S. Lindsay (2020), *Application of Conformal Prediction Interval Estimations to Market Makers’ Net Positions*, PMLR128:285–301: https://proceedings.mlr.press/v128/wisniewski20a.html . Selected original passages and methods were read; figures were not reused.
- van den Hoogen, S. (2017), *Intraday liquidity risk estimation using transaction data: an extreme value theory approach*, Delft MSc thesis: https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1 . Selected sections, not the entire160-page thesis.
- Liao, J. and T. Theodosopoulos (2005), *Study on optimal timing of mark-to-market for contingent credit risk control*, arXiv:math/0506077v1: https://arxiv.org/abs/math/0506077v1 . Selected model/objective passages.
- Barone-Adesi, G., K. Giannopoulos and L. Vosper (1999), *VaR without correlations for portfolios of derivative securities*, actual body USI Quaderno99-04 revised March1999: https://folia.unifr.ch/documents/318043/files/wp9904.pdf . Formal publication Journal of Futures Markets19(5):583–602, DOI10.1002/(SICI)1096-9934(199908)19:5<583::AID-FUT5>3.0.CO;2-S; final-body equivalence unverified. Selected original methods/application, not a reproduced filtered simulation.
- Gneiting, T. (2011), *Making and Evaluating Point Forecasts*, DOI10.1198/jasa.2011.r10138: https://doi.org/10.1198/jasa.2011.r10138 . Selected quantile-score foundations.
- Politis, D. N. and J. P. Romano (1994), *The Stationary Bootstrap*, DOI10.1080/01621459.1994.10476870: https://doi.org/10.1080/01621459.1994.10476870 . Selected original mechanism/assumption passages.
- Barber, R. F., E. J. Candès, A. Ramdas and R. J. Tibshirani (2023), *Conformal Prediction Beyond Exchangeability*, read arXiv2202.13415v5: https://arxiv.org/abs/2202.13415v5 . Selected sections, not an adopted coverage guarantee.
- Schmitt, M. (2026), *Taming Tail Risk in Financial Markets: Conformal Calibration for Nonstationary Portfolio VaR*, arXiv2602.03903v3: https://arxiv.org/abs/2602.03903v3 . Recent relevant context, not verified popularity or the present inventory target.

Exact source versions, fingerprints and reading depths remain in the literature records. This design does not turn selected passages into claims of full-paper reading or an exhaustive novelty certification.
