# Exploratory extension: selecting historical responses for sampled net-position peaks

This protocol is recorded after the original evaluation interval and results have been inspected, and before calculating the extension's forecasts or losses. It constrains further choices; it does not create an unseen holdout or external preregistration. The original specification, source fingerprint,35 summary rows and adverse results remain available in the repository history and original results files.

## Question and scope

For the same sampled absolute client-flow net-position peak, does selecting historical starting positions near the current signed position improve a finite empirical-quantile forecast relative to selecting the same number of most recent completed responses? Within each selected set, how do native headrooms, reanchored increment envelopes and floored native peaks differ?

This is a transfer of mature nearest-neighbor empirical quantiles to a particular financial response, not a new NN algorithm. A single signed state is not established as sufficient for the full conditional law. The comparison does not implement the richer lag/calendar regressions in Wisniewski et al.(2020)/Wisniewski's later thesis, or conditional mean/volatility filters. Neither a small report gap nor an observed loss advantage proves coverage, cash adequacy, capital savings or policy profits.

## Unchanged source, response and issue convention

- Source: version2 of `davidlindsay1979/net-position-time-series-dataset`, accepted one-hour CSV;18576 records,1286391 bytes,SHA-256 `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`.
- Only the existing timestamp and signed `NetPosUsd` fields enter. Source timezone and historical release/vintage availability remain unverified. No raw data or origin traces are to be redistributed.
- At issue index t, the record N_t is observed. Set B_t=|N_t| and P_(t,H)=max_(0<=h<=H)|N_(t+h)|. Headroom is G=P−B. This is a maximum over records, not a continuous-time maximum, gross exposure, P&L or settlement cash.
- Use exactly H=6 and H=24, tau=19/20, eligible pool size n=720. H6 is the primary extension; H24 retains the original adverse-horizon context. H counts subsequent recorded observations, including gaps; no imputation or gap exclusion.
- Use the existing6625 common origins, zero-based11927 through18551 inclusive. These correspond to the original timestamp cutoff and full-menu last-origin rule. No new favorable subset is selected.
- At t, eligible origins are I_t={t−H−719,...,t−H}; every response ends at i+H<=t. A completed label may include the already observed N_t. Completion does not imply independence.

## Selected historical rows

For each t,H compare the following five sets, in this fixed order:

| Set | Size m | Selection within I_t | Corrected rank k=ceil((m+1)*19/20) |
|---|---:|---|---:|
| full720 |720|All eligible rows|685|
| recent360 |360|Largest origin indices|343|
| nearest360 |360|Smallest absolute signed-position difference; equal distances prefer the most recent origin|343|
| recent180 |180|Largest origin indices|172|
| nearest180 |180|Same signed-distance and recency-tie rule|172|

The nearest distance is abs(N_i−N_t). After membership is selected, carry the paired rows in chronological order. Selection uses only origin-known signed positions and issue-known eligibility; never future query outcomes or candidate responses as tie breakers. No interpolation, jitter, distance threshold, feature standardization, volatility coordinate, coefficient fitting, adaptive m or search is added. The two counts are fixed half/quarter-pool challenges, not asserted optimal choices. Matched counts do not match sample age, volatility or dependence.

## Three representations on every selected set J

For each historical origin retain P_i,G_i and a_i=min_h(N_(i+h)−N_i), b_i=max_h(N_(i+h)−N_i), with h=0,...,H. With a common selected J and rank k, issue:

- F_J=B_t+Q_k(G_i:i in J).
- S_J=B_t+Q_k(max(N_t+b_i,−N_t−a_i)−B_t:i in J).
- K_J=max(B_t,Q_k(P_i:i in J)). K is the original rule L under another explanatory symbol, not an added algorithm.

The original S subtract-then-rank-then-add operation order is retained in float64. Real-arithmetic equivalence to ranking peaks directly is not permission to change strict breaches or stored equalities. There are15 rules per H,30 configuration cells total, with shared full720 references counted once per H. Full720 F/S/K in H6/H24 repeat original reference cells, not independent new findings. Original R/P0 and the remaining original sensitivity results remain available; the extension does not silently extend all five original representations to every selected pool.

## Evaluation and failure criteria

Use direct stored error e=P−C and pinball rho_tau(e)=tau*max(e,0)+(1−tau)*max(−e,0). Convert19/20 and1/20 separately; preserve float64, duplicate order statistics and strict breach e>0. Aggregate with the original compensated mean and explicit scalar/null conventions.

The primary extension contrast is equal-origin mean loss(nearest360,K) minus loss(recent360,K) at H6. A value>=0 fails the finite-record improvement criterion. H24 reports the identical contrast as an adverse-context check; m180 is the fixed sensitivity. No population test, p-value, confidence interval, inference from independent6625 observations, winning-parameter selection or new bootstrap is added. Every configured outcome, including adverse/null ones, is retained.

Report all30 method cells: origin count, rank, mean pinball, mean issued capacity, mean extra, strict breach count/rate, mean positive overrun, conditional overrun and its breach denominator, and mean unused allowance. With no breaches, conditional overrun is null with an explicit reason. For each H/set report mean absolute F−S report gap, exact equal-capacity count, mean signed/absolute maximum anchor radii and mean selected origin age in records. Radii describe construction, not accuracy. Same-pool finite inequalities are checked only with declared arithmetic tolerance, separate from strict breach/equality categories.

Report paired nearest-minus-recent losses for F/S/K at both counts/horizons and same-pool F-minus-S contrasts. Calendar-month paired means for the primary nearest360K/recent360K contrast at both horizons retain every original month. Groups below30 origins report counts/status and suppress metric values uniformly; this never changes global evaluation. No new state grouping, retrospective exclusion or learned regime is introduced.

For each issued set use arithmetic tolerance64*epsilon*max(1,|N_t|,max_J|N_i|,max_J P_i,max(F,S,K),r_abs,r_signed), with float64 epsilon. Check |F−K|<=r_abs+tolerance, |S−K|<=r_signed+tolerance and |F−S|<=r_abs+r_signed+tolerance. Also check the envelope refinement |F−S|<=max_J min(2|N_i−N_t|,|b_i+a_i|)+tolerance. These are arithmetic consistency checks, not future coverage tests. Exact F=S counts and strict e>0 breaches are never replaced by this tolerance.

## Verification, resource limits and stopping

Before financial execution, tests must independently cover hand-valued coherent paths, deterministic tie selection, unavailable/future-label rejection, future perturbation/prefix invariance, m=n identity with original F/S/L, positive-scale/global-sign transformations, exact fractional ranks, direct scoring and both coherent favorable/adverse continuations. Reject malformed/nonfinite inputs and floor/maturity violations. Preserve original core/data/report code and original result files.

One CPU process; numerical thread requests set to1 before NumPy import; at most2 observed numerical/process threads, RSS at most2GiB, raw data at most100MiB, each download at most25MiB, each experiment at most10minutes. Reuse the already verified source snapshot; no new download is planned for this extension. Measure elapsed time,RSS and thread snapshots; do not report budget values as observed measurements. Stop on a resource, source, eligibility, numerical or aggregate-reconciliation failure and preserve its reason. A correction may repair a documented implementation defect, but must not change the scientific menu in response to the scores.

Public outputs contain code, this protocol, source/version hashes and aggregates only. Private selected rows/origin predictions remain task-owned temporary replication evidence. The extension is completed only after exact source/global-reference reconciliation, content/number checks, an inspectable English manuscript/PDF and actual GitHub-file verification. No journal submission is authorized.

## Method and direct-lineage sources

- Biau & Patra, *Sequential Quantile Prediction of Time Series*, IEEE Transactions on Information Theory57(3):1664–1674(2011),DOI[10.1109/TIT.2011.2104610](https://doi.org/10.1109/TIT.2011.2104610); actual methods/assumptions consulted in [arXiv0908.2503v2](https://arxiv.org/pdf/0908.2503v2),31May2010. Fixed finite retrieval here does not inherit the complete expert strategy's asymptotic result.
- Wisniewski,Lindsay & Lindsay(2020),[Application of conformal prediction interval estimations to market makers' net positions](https://proceedings.mlr.press/v128/wisniewski20a.html),PMLR128:285–301. Their response is a next-hour signed endpoint with two-sided intervals; their published values are not same-peak benchmarks.
- Wisniewski,[Net Position and Retail Trader Behaviour: Implications for Market Makers' Risk Management Strategies](https://pure.royalholloway.ac.uk/en/publications/net-position-and-retail-trader-behaviour-implications-for-market-/),doctoral thesis,2024 institutional record,Chapter6. This is the same source lineage, not independent validation.
- Hull & White(1998),[Incorporating volatility updating into the historical simulation method for value-at-risk](https://doi.org/10.21314/jor.1998.001),and Pritsker,[The Hidden Dangers of Historical Simulation,FEDS2001-27](https://www.federalreserve.gov/pubs/feds/2001/200127/200127abs.html). Conditional scale/innovation filtering differs from signed-level matching and is not implemented here.
- Gneiting(2011),[Making and Evaluating Point Forecasts](https://doi.org/10.1198/jasa.2011.r10138). Quantile-consistent scoring does not certify a finite rule's conditional calibration or economic-cost interpretation.
