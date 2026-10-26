# WP2: fixed CFTC history-length mechanism check

Status: prospective registration for the W=520 extension, written before any
new WP2 forecast. This file and its companion design/input seal must be committed
on `final-jof` before `results/final-merge/wp2-cftc-mechanism/` is created. They
will not be revised after execution. Corrections, if needed, are separate dated
deviations and do not replace this registration.

## 1. What this can establish

This is the mentor-requested check of A's fixed history-region predictions in B's
CFTC reporting system. CFTC TFF Futures Only dealer net positions aggregate many
dealers within a market. They are not independent dealer-level replications.
The reporting system differs from the FX source and NY Fed dealer reports, but
markets can be dependent. The universe was selected retrospectively using the
original B design. The W=52 and W=260 outcomes have already been inspected in B
and in WP1; they are reused unchanged, not rebranded as untouched confirmation.
Only the W=520 conditional forecasts are uncomputed when this file is committed.
All estimates use the downloaded vintage on the economic-position calendar;
they do not reconstruct first-release information available to a real observer.

The screen is a check of a transported descriptive prediction, not a causal
identification of estimation cost, normalization by parameter count, a universal
break-even law, or a coverage guarantee. The coordinate c=W/(H+1) excludes p.
Validation selection, persistence, nonstationarity and shrinkage also change
performance. Matching W matches mature training labels and refit cadence, not
all raw feature history or validation information across methods.

## 2. Fixed inputs, geometry and estimators

Use exactly the 17 rows, their literal codes and their order in
`results/v10/cftc/sources.json`; verify all stored SHA-256 values. No acquisition,
new filtering, market substitution, imputation, universe reranking, or splice.
The source arrays have 877 weekly observations. Preserve actual economic dates
and the inherited Monday modelling clock separately.

H=6 weeks; W in [52,260,520]; tau=19/20; refit every 13 observations.
Validation is 52 observations, indices 553..604. Evaluation is 260 observations,
indices 611..870. Latest validation label ends at 610, before first evaluation
611; the last evaluation label ends at 876. The six intervening dates are not
issued reports. At refit r, training uses exactly W origins r-H-W+1..r-H,
whose labels end no later than r. The first W=520 validation pool starts at 28,
beyond the inherited conditional-feature valid-from index 26. Insufficient
history in any source is NA with a reason; never shorten W.

Methods are F, QR4 and QR33. The target is max |position| over t..t+H, including
the current floor |position_t|. F uses the inherited corrected empirical rank
ceil((W+1)*19/20). Both regressions retain B's six-candidate penalty menu
[.001,.01,.1,1,10,"inf"], its solver and feature transformations, and its
training-only response scaling. "inf" is exactly ordinary empirical I.
Exact validation-loss ties select the stronger penalty. QR33 requires all six
validation candidates complete; QR4 may select from complete candidates under
the original B policy. Each candidate is attempted once. Failed selected
evaluation remains unavailable; no fallback, retuning, retry or partial mean.
F/I/ACI variants beyond the three named procedures are not new WP2 tasks.

For W=52 and W=260, reuse every matching complete trace and scalar result from
the original `results/v10/cftc/complete-traces/` and `formal/units.zip`. Hash-bind
them before execution. No refit or overwrite of these older results. For W=520,
call the unchanged `v10_menu.forecast_report` and `evaluate_method` through the
new caller-owned adapter, with all outputs in the new WP2 directory. Fit both
regression menus afresh for the longer pool; do not borrow later selected
penalties or choose penalties using evaluation losses.

## 3. Fixed A thresholds

Read only `notes/revision-v9/wp1-breakeven.json`:

| Method | r* | recorded lower | recorded upper |
|---|---:|---:|---:|
| QR33 | 106.49618468616566 | 27.894967082095143 | 110.71007095944418 |
| QR4 | 27.324522025270575 | 13.27239395223403 | 107.10936480242033 |

Use point r* to define the requested primary regions; report the original
intervals without re-estimation or treating them as universal confidence bands.
They condition on A's post hoc coordinate choice and fixed simulation grid.
QR4 had multiple downward crossings; crossing its first r* did not imply
universal subsequent improvement. The six-candidate CFTC selector also differs
from A's original discovery menus. These are material transport limitations.

At H=6, c is 52/7, 260/7, 520/7. QR33's low region contains W=52 and W=260;
QR4's low region contains W=52. Only QR4 W=520 is in its high region. QR33
has no observed c>2r* cell and its P2 is NOT_TESTABLE by design.

## 4. Immutable predictions and classifications

Let Delta=100*(mean pinball(method)/mean pinball(matched F)-1). Positive Delta
means a loss; negative means a win. Exact Delta=0 is a tie, neither win nor loss.
If F has zero mean loss, the comparison is NA and the reason is explicit.
All arithmetic uses the same complete 260-date axis; never pair-delete dates.

* **P1-QR33:** among the 34 planned market/window cells with c<r*/2, at least
  80% have Delta>0.
* **P1-QR4:** among the 17 planned low-region cells, at least 80% have Delta>0.
  Combined P1 passes only if both method-specific screens pass. Report both
  fractions and every failure/tie independently.
* **P2-QR4:** among 17 planned W=520 cells with c>2r*, at least 60% have Delta<0.
  P2-QR33 is structurally NOT_TESTABLE and is not counted as a failed primary.
* **P3 (secondary):** Delta_QR4(52)>Delta_QR4(260)>Delta_QR4(520) strictly in
  at least 70% of the 17 markets. A tie or reversal is a counterexample.
  Do not substitute an endpoint-only decrease for both successive decreases.

Cells are equally weighted within each screen; do not average native contract
losses across markets. These percentages are descriptive counts, not binomial
tests of independent markets. Missing cells stay in the planned denominator.
For success count s, unknown count u and planned n, show complete-only s/(n-u)
and the fixed-denominator bounds [s/n,(s+u)/n]. A screen is SUPPORT when its
lower bound meets the threshold; NOT_SUPPORT when its upper bound is below it;
otherwise NOT_TESTABLE. This prevents failure-dependent deletion from creating
support. Combined P1 is NOT_SUPPORT if either component is NOT_SUPPORT;
otherwise it is SUPPORT only when both support, and NOT_TESTABLE otherwise.

If P1 and P2-QR4 are both testable: both pass => **SUPPORT**; exactly one pass
=> **PARTLY**; neither pass => **NOT_SUPPORT**. If an unresolved primary cannot
be classified by the conservative bounds, overall is **NOT_TESTABLE**, never
silently relabelled a pass or failure. P3 cannot upgrade the primary verdict.
The run reports the full counterexample/unknown inventory, including adverse
markets at every window, rather than only supporting examples.

## 5. Requested diagnostics and independent implementation

Publish each market/method/window's status, mean loss, matched F mean loss,
Delta, strict breach counts (peak>capacity), selected penalty and trace identity.
For each complete QR-minus-F pair use all 260 losses in the existing normal
HAC DM convention: centered Bartlett autocovariances divided by n, bandwidth
L=min(n-1,max(H,floor(4*(n/100)^(2/9)))). Here L=6. Report mean difference, LRV,
t=mean/sqrt(LRV/n), two-sided p=erfc(|t|/sqrt(2)). Identical/constant/nonpositive
variance cases retain undefined statistics and reasons. No HLN, new family
adjustment, significance gate, or p-value-based selection. The many dependent
raw p-values remain working-reference diagnostics, not a new confirmatory
multiple-testing claim; pre-existing selection is not repaired by registration.

The same sole executor will use a separate scalar implementation (math.fsum,
explicit target/score loops, covariance loops) to verify source targets, floor,
loss, breach count, HAC diagnostics, fixed denominators and P1-P3 decisions.
This is algorithmic independence, not a second person/model or independent data
reproduction. Compare full arrays and full-precision scalars with absolute
1e-10 plus relative 1e-12 tolerance (integer identities exact); report mismatch
count zero only when every check passes. Independently inspect recorded exact
training bounds, every latest label end, validation separation and selected
candidate inventory. No second real-model fit is needed or allowed merely to
make verification look independent. Retain all diagnostics and source hashes.

## 6. Runtime, resource and reduction policy fixed before execution

The archived original 17-market / two-window / six-method run took
12.25863366597332 seconds with four workers. A conservative 10-fold allowance
for the longer conditional pool is about 123 seconds; budget 30 minutes for
the new fit stage, 90 seconds internal and 120 seconds hard per market. This
estimate is from existing receipts, not a pilot fit. Use one worker at a time,
one numerical thread, source_index ascending, F then QR4 then QR33. A source
time-out preserves partial receipts, marks uncompleted methods NA, and advances
once; never rerun failed sources. At the global deadline, all unstarted tasks
remain NA and are listed. Existing sources/results/protocols stay byte-identical.

The inherited design contains H=6 only. H=24 is excluded before execution as
the mentor's first budget priority and because this WP's registered primary
regions use H=6. Keep W=52 through archived reuse, which requires no model
budget. If any later resource reduction is necessary, the fixed removal order
is H=24 first (already absent), then new W=52 fits (none planned); never drop
W=520, markets or adverse outcomes based on results. Budget exhaustion yields
NA, not a redesigned successful experiment. This scope decision is disclosed
instead of pretending that H=24 was run.

## 7. Audit gates

Constructed tests must pass without reading financial sources or fitting
models. The code/input seal contains source, old-trace, threshold, algorithm,
protocol and new-adapter hashes and no WP2 numerical results. Commit it and this
file, verify a clean `final-jof`, and record the actual commit before launch.
The execution start receipt binds that commit and UTC. Every generated output
is new and exclusive-create. At the end, verify the committed protocol/code
unchanged, input hashes unchanged, independent mismatch count zero, P1-P3
classification/counterexamples complete, and old science preservation. Record
commands and actual output in the WP2 changelog before proceeding to WP3.
