# Independent mathematical review of the coverage diagnostic

22 October 2026. Scope: read-only review of `coverage_evalues.py`, `test_coverage_evalues.py`, and `protocol/revision-20261022/coverage-evalue-design.md`. No financial arrays, new statistics, source acquisition, or scientific computation were used. The 15 synthetic test functions were read, not rerun. This review does not certify the financial runner, its inputs, or a future output receipt.

## Finding

No blocking mathematical or count-level implementation defect was found in the three reviewed files. No new numerical concern justifies repeating the existing synthetic tests. The principal limitation is inferential rather than an arithmetic bug: the mathematical fixed-procedure e-value/FWER theorem must remain distinct from the post-result status of this archive. The design already makes that distinction in its purpose and threshold sections; scientific integration must preserve it.

## Exact calculation

The normalized uniform mixture is

\[
E_{n,k}=\frac1{1-\alpha}\int_\alpha^1
 (u/\alpha)^k\{(1-u)/(1-\alpha)\}^{n-k}\,du
=\int_0^1(1+rv)^k(1-v)^{n-k}\,dv,
\quad r=(1-\alpha)/\alpha.
\]

Its positive expansion terms are

\[
a_j={k\choose j}r^j B(j+1,n-k+1),
\quad a_0=\frac1{n-k+1},
\quad \frac{a_{j+1}}{a_j}=\frac{(k-j)r}{n-k+j+2}.
\]

This matches `mixture_evalue` lines 35–41 and the design recurrence exactly, including zero breaches, all breaches, and the empty product. At alpha 1/20, the stated positive integer formula

\[
E_{n,k}=\frac{\sum_{j=0}^k{n+1\choose j}19^{k-j}}
{(n+1){n\choose k}}
\]

is equivalent. The test file contains distinct signed-polynomial and integer-formula checks, as well as null-expectation fixtures; reading those tests is not a fresh execution result. Display rounding is correctly separated from exact comparisons.

## Delay and fixed-terminal validity

Under the stated full issue-information null, the conditional expectation of a single factor is

\[
1+\frac{(u-\alpha)(q_t-\alpha)}{\alpha(1-\alpha)}\le1.
\]

Actual-index residues modulo H+1 ensure that earlier factors within a phase have matured before the next issue. The production kernel uses actual origin indices, rejects non-increasing origins, retains every phase, and averages phase values rather than multiplying them. The kernel deliberately does not certify label maturity or completeness; those are caller obligations expressly retained by the design.

Iterated conditional expectation, nonnegative mixing, and fixed-weight averaging therefore establish expectation at most one at the declared fixed terminal. No stationarity or independence follows or is needed. The code and design appropriately withhold full-filtration supermartingale and arbitrary-stopping claims. Strict breaches also preserve the intended treatment of equality atoms.

## Selection and what an empirical flag can mean

For a genuinely fixed collection of M causal report procedures and fixed diagnostic rules, each true-null statistic has expectation at most one. Markov's inequality and a union bound then control erroneous flags at threshold M/delta without independence, including when other cells' nulls are false. Thus 56/delta = 1120 is the correct *formal* threshold for that stipulated fixed family and delta 1/20.

That implication is not a retrospective error-control certificate for the present archive. The design explicitly records that forecasts, scores and breach summaries were inspected before this diagnostic was chosen, and that the 56-cell matched family excludes other reports in the archive. Freezing these choices before computing the new statistic prevents subsequent drift; it does not make earlier method-family, terminal or diagnostic selection independent of the observations. A larger correction over the 98 current reports alone would not automatically account for those other searches either.

Accordingly, later output may report the exact evidence values and crossings of the declared formal threshold as a **late exploratory diagnostic**. It must not describe those crossings as empirically established 5% family-wise-error-controlled discoveries, call the new freeze prospective preregistration of this archive, or turn non-crossings into coverage certification. This is the substantive interpretation gate, not a request for additional boilerplate or an alteration of the correctly specified recurrence.

No edits to the reviewed source files are requested on the basis of this audit. Preserve the design's existing selection qualifications in any result table and manuscript interpretation.
