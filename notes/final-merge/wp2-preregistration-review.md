# WP2 pre-execution design and code review

This record precedes the W=520 forecasts. It is not an experiment result or a
WP2 completion receipt. The sole executor performed this review; there was no
Claude call, second model or subagent.

## Input and timing checks

The read-only preflight checked all 17 exact source-array hashes and lengths,
their weekly clocks and the W=520 split geometry. It sealed 148 input/code
files. No new output directory existed, no model was fitted and no inherited
result was written. The runtime estimate comes from B's existing formal receipt
(12.25863366597332 seconds), with an explicit conservative allowance; it is not
an unregistered pilot. Only existing cached dependencies are used offline.

## Chronological derivation

With N=877 and H=6, first evaluation is N-H-260=611. Last validation is
611-6-1=604, first validation is 553 and its last label ends at 610. The first
W=520 training origin at validation is 553-6-520+1=28. The last completed
training origin is 547, so its label ends at the refit 553. The first pool
contains exactly 520 observations and starts after feature valid-from 26.
Validation and evaluation start their own original 13-observation refit grids.
The independent verifier checks these exact identities, not just an inequality
that would admit a silently shortened training pool.

## Rules checked against the mentor plan

The low-region P1 counts are 34 QR33 cells and 17 QR4 cells; both method-specific
screens must pass for combined P1. P2 uses 17 QR4 W=520 cells; there is no QR33
high-region cell. P3 requires both successive QR4 relative-loss decreases in
each market. Exact ties do not meet a strict win, loss or decrease condition.
Unknowns retain their planned denominators and produce conservative bounds.
H=24 is absent before execution, as the mentor's first budget priority; W=52
uses unchanged archived traces rather than consuming new-model budget.

## Implementation review

The new adapter calls the inherited fixed-feature/solver/menu procedures. It
does not edit their code. Each source is launched once, with fixed source order,
one numerical thread and explicit time limits. Candidate inventories and their
validation traces are retained; selection is persisted before the single
selected evaluation. Exceptions are not replaced with a better-performing
method. Old W=52/260 trace identities are checked against their original result
receipts, and all new writes use an exclusive-create WP2 output directory.

Separate scalar loops reconstruct target peaks, floors, pinball losses, breach
counts and centered Bartlett HAC from the source and saved predictions. They
also reconstruct empirical capacities for F and exact-empirical selected
models, and independently count every primary and secondary outcome. They do
not independently solve the finite-penalty quantile problem a second time.
Recorded solver tolerances, training bounds and candidate selection are audited.
Algorithmic independence does not establish independent authorship, a new data
replication, first-release observability or a uniquely identified mechanism.

## Constructed tests

The first test execution failed in all 11 cases because the adapter was absent.
The implementation then passed all 11 constructed tests. Tests cover exact
split bounds, insufficient-history rejection, fixed missing-data denominators,
threshold inclusivity, the combined primary rule, strict monotonicity, a known
HAC answer and its undefined cases, target/floor/strict-breach arithmetic and
exact label maturity. The HAC known-answer fixture was corrected from a draft
hand-calculation to the archived convention before implementation verification:
for [1,2,3,4], H=2, L=2 and LRV=17/12. No financial outcome was used to set it.

Full merged pytest is required before the registration commit. The numerical
experiment, independent comparison, result verdict and counterexample list
remain pending at this stage.
