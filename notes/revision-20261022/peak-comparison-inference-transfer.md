# What conditional-predictive-ability inference would require for this peak task

22 October 2026. Existing literature revisited after the QR and exploratory AR additions. This note designs no new test and calculates no current financial loss, covariance, confidence interval or p-value. It changes no original hypothesis, forecast, comparison or result. The current manuscript remains descriptive.

## Primary reading and scope

Raffaella Giacomini and Halbert White, *Tests of Conditional Predictive Ability*, Econometrica 74(6):1545–1578 (November 2006), [DOI:10.1111/j.1468-0262.2006.00718.x](https://doi.org/10.1111/j.1468-0262.2006.00718.x). The retained [UC3M institutional journal-typeset copy](https://economia.uc3m.es/jgonzalo/teaching/PhdTimeSeries/GiacominiWhite.pdf) is 34 pages / 344,647 bytes, SHA-256 `cc6e86b69e2cc70f484b45367528bd47f58e17f35102a87179ed3ce9060a0642`. The original named cache had been removed; a bounded ordinary retrieval restored the identical bytes in a new task-private directory. No access boundary was bypassed and no new edition or distinct paper was discovered.

Root actually reread selected original physical pp.4–14 and 28–31, including the bounded-memory environment, conditional/unconditional nulls, Theorems 1–4 and their displayed proof routes. Earlier selected reading and the new [separate applicability review](conditional-predictive-ability-feasibility-agent.md) are distinct evidence. External mixing/CLT/HAC references were not independently certified; the source's simulations and empirical tables were not reproduced. The source permits heterogeneous distributions subject to its conditions; it does not require strict stationarity in every result. It does assume short-memory regularity and supplies asymptotic, not exact finite-sample, conclusions. General loss comparison does not automatically require a continuous positive target density.

## A legitimate indexing route

For fixed record horizon H, define the resolved backward-window target

\[
Y_s^{(H)}=\max_{s-H\le j\le s}|N_j|.
\]

The current issue-t forecast concerns `Y_(t+H)^(H)=P_(t,H)`. Under the stated economic-date replay, the report is issue-information measurable and its loss resolves at t+H. This maps the peak into fixed-horizon forecasting notation without replacing it with a signed endpoint. A known-floor atom and overlapping outcomes do not themselves invalidate such a representation. Nothing in this indexing establishes a mixing rate, moment bound, appropriate public-release information set or valid variance estimate.

Let

\[
D_{t,H}=\rho_{.95}(P_{t,H}-C^A_{t,H})
       -\rho_{.95}(P_{t,H}-C^B_{t,H}).
\]

Mean loss comparison concerns an unconditional expectation or a separately defined expected-average estimand. A full-information conditional null instead states `E[D_(t,H)|F_t]=0`. These are different questions. Rejection of conditional equality need not mean that one method has a uniformly lower average loss; nonrejection using finitely many instruments is not proof of conditional equality or calibrated forecasts. The heterogeneity and centering of any proposed expected-average confidence interval must be addressed explicitly rather than inferred from a fixed-pair test's name.

## Label delay also governs diagnostic instruments

An issue-s difference `D_(s,H)` generally needs its full target, which resolves by s+H. Without a separately justified early-resolution rule, the guaranteed completed-comparison indices at issue t satisfy `s<=t-H` under the current observation convention. For H>1, the previous issue's `D_(t-1,H)` generally contains future observations and is not an issue-known predictor of relative performance. The most recently guaranteed completed difference is `D_(t-H,H)`, not automatically the preceding row of an evaluation CSV. Some differences can be known earlier, such as exactly identical reports or the constant-target example below; the maturity statement is a safe general rule, not a universal impossibility of early knowledge. A data release lag would require an additional availability check.

The same timing explains the conditional-null covariance cutoff. For an issue-known instrument `h_t`, put `Z_t=h_t D_(t,H)`. If j>=H, the old `Z_(t-j)` has resolved by t and is F_t-measurable. Provided the products are integrable, the full conditional null gives

\[
E[Z_tZ_{t-j}' ]
=E\{h_tZ_{t-j}'E[D_{t,H}\mid F_t]\}=0.
\]

This is an elementary tower-property check, not a new theorem. It remains true even when the two target windows share a now-known issue observation. Conversely, mechanically spacing origins H+1 apart does not create the full conditional null or remove all dependence. Under unconditional equal expected loss, the source calls for a general long-run variance rather than a covariance cutoff justified solely by H.

### A bounded artificial example of the distinction

Take an abstract constant path `N_t=0`, so every sampled peak and known floor is zero. Let issue-known `X_t` be a stationary symmetric two-state Markov chain on `{-1,+1}`, with probability of staying in its current state `(1+r)/2` and r=9/10. Consider the artificial reports `C_A=2+X_t` and `C_B=2-X_t`; both obey the known floor. These are constructed reports, not fitted QR/AR outputs or financial observations.

Since both reports exceed the zero target, pinball loss gives

\[
D_t=2(1-\tau)X_t,
\qquad E[D_t]=0,
\qquad \gamma_j=[2(1-\tau)]^2r^{|j|}.
\]

At tau=19/20, `gamma_j=(1/100)*(9/10)^|j|`, which is nonzero at every finite lag. Its long-run variance is

\[
\gamma_0+2\sum_{j=1}^{\infty}\gamma_j
=\gamma_0\frac{1+r}{1-r}=\frac{19}{100}.
\]

The two methods have equal unconditional expected loss, but the horizon alone does not truncate their covariance sequence. In fact D_t is already known at issue, so `E[D_t|F_t]=D_t`, not zero. Thus this example does not contradict the full conditional-null result and does not obey the generic need to wait H records for its loss. It is an elementary counterexample to deriving a covariance cutoff from unconditional equality and the horizon alone. It establishes neither the actual archive's dependence nor the superiority of any variance estimator.

## Actual finite memory is longer than the training-row count

Conditional on fixed tuning choices, the oldest rich training feature at refit r reads `N_(r-H-W+1-L)`, where L is the longest raw-position lag and `0<=t-r<=d-1`. Thus an inclusive upper bound on raw-position memory through issue t is

\[
M_N=W+H+L+d-1.
\]

For the mean-only AR replay, L=0. For the rich QR/local feature procedures, L=168 FX records or 26 Treasury records. Deterministic refit/calendar phase need not itself violate the source's allowance for heterogeneous finite-block transformations. The table is computational bookkeeping from the unchanged specification, not a fitted statistical result, effective sample size or degrees-of-freedom calculation.

| Source | H | W | Refit d | Rich-feature raw-memory bound | AR raw-memory bound |
|---|---:|---:|---:|---:|---:|
| FX | 6 | 720 | 24 | 917 | 749 |
| FX | 24 | 720 | 24 | 935 | 767 |
| FX | 6 | 2,880 | 24 | 3,077 | 2,909 |
| FX | 24 | 2,880 | 24 | 3,095 | 2,927 |
| Treasury | 6 | 52 | 13 | 96 | 70 |
| Treasury | 24 | 52 | 13 | 114 | 88 |
| Treasury | 6 | 260 | 13 | 304 | 278 |
| Treasury | 24 | 260 | 13 | 322 | 296 |

One-time validation selection is additional retained state. The chosen lambda/k can be treated as a fixed method definition or analyzed with an explicit conditioning/selection argument, but the last W fitted rows alone do not supply that argument. The source also discusses fixed-initial-sample estimation, so permanently retained selection should not be described as an automatic prohibition. Its stochastic treatment still has to be specified.

## What remains before a defensible implementation

The selected theorem's mixing and sufficiently high loss-product moment conditions, covariance nondegeneracy, null-specific weights/bandwidth and growing-evaluation framework remain substantive assumptions. Finite saved forecasts do not prove those conditions. The source's conditional retained-lag weights must approach one; a fixed conventional Bartlett weight `1-j/H` is not by itself that sequence. This is an implementation translation check, not an allegation that a source theorem is false.

Population regularity cannot be certified from any single finite archive. A later applied study may state and defend explicit working assumptions and report transparent sensitivity under them. The decision not to append inference in this batch rests on the absence of a fixed inferential estimand, selection treatment and variance protocol, rather than a demand that every population assumption be empirically proved or a claim that financial inference is categorically impossible.

The exact full-pool Treasury KNN/F identity has zero loss difference and cannot be fed into an invertible-variance Wald statistic solely because it has two method labels. At H24, 277 weekly origins and 12 fixed sparse starts also do not come with a theorem-supplied acceptance or rejection threshold for sample size. Small-sample size, power and covariance behavior need investigation; neither arbitrary rejection of 277 nor treating 12 starts as independent is justified.

A new inferential protocol would first state the estimand/null, fixed pairs, issue-known instruments, treatment of the retained validation selection, variance formula and bandwidth sequence, multiplicity and evaluation/stop rule. The inspected FX interval and later AR additions remain exploratory. Selecting a favorable instrument or bandwidth after reading p-values would be another selection step, not an application of an unchanged test.

The direction decision is therefore to preserve descriptive results now while keeping this mature inferential route open for a properly specified later study. No present claim that all time-series inference is impossible is warranted. Equally, merely citing this source does not justify appending inferential certainty, restore unseen records or establish live dealer decision value.
