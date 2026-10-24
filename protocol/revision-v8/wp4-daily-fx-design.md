# WP4: same-dealer daily aggregation — pre-analysis freeze

This design is written before parsing or aggregating the accepted raw FX file.
Only its exact byte count and original SHA-256 have been checked. This is a
post-result exploratory extension of the existing paper; the original two
primary comparisons and all old results remain unchanged. The companion JSON
is the executable contract. No new model, data source, statistical test or
penalty outside its declared menus is allowed.

## Question and observation clock

Does historical headroom dominate the same dealer's daily sampled peak task,
or do conditional gains remain after within-source aggregation? Retain the
last recorded position from each nonempty source-naive calendar day. Issue
after that day ends, at the next midnight minus one microsecond: identifying
a day's last record at its original timestamp would otherwise use information
about the rest of the day. Empty days have no sample/report; never fill,
interpolate or invent weekend positions. Retain partial boundary days under
the same rule. The original timestamps have no established timezone, so these
are neither asserted UTC days nor reconstructed exchange reporting vintages.

The response is the maximum absolute daily sampled position from the current
issue through the next H recorded nonempty day-end observations, H6 or24.
It excludes discarded intraday excursions. Headroom subtracts the known
current absolute position. Every training label must satisfy i+H<=refit.
The raw input, resampled values, selected source row indices and per-issue
predictions remain private task-scratch artifacts; publish only aggregate
results, metadata and fingerprints.

## Treasury rule audit and adaptation

The original Treasury specification uses validation indices329–380,
evaluation beginning405 and a common complete-H24 tail, refit13, RMS6/26.
It is not a proportional split. Its2021 absolute calendar cutoff cannot be
copied to the earlier accepted FX record. This is an explicit calendar-scope
MISMATCH, rather than a claim to have used the same absolute dates.

Transfer the **observation-index geometry**: validation329–380 inclusive,
evaluation405 through n_daily−25 inclusive. Validation's last H24 target
ends404, before evaluation. The common first training origin must be at least
the feature-valid index26; if a cell lacks the required full history or
evaluation observations, all its methods are NA_SAMPLE_SIZE with a reason.
No shorter history, moved cutoff or extra sample is substituted.

Use W52/260 and H6/24, original33 features with RMS6/26 and day-end clock,
nominal gap86400 seconds, and original four-feature columns25/0/26/27.
Daily hour features are constant and are handled by the original training-only
standardizer. The feature builder, transform, response scale and solver are
unchanged. Calendar and gap features use only the completed issue clock.

## Methods, selection and failures

Only F, original33-feature QR and original four-feature QR are calculated.
Reuse the WP3-sealed primitive without modifying it. Avoid historical helpers
that compute unlisted S/K forecasts as side effects. F uses the corrected
ceil(19(W+1)/20) mature-headroom rank plus current floor. All methods use
the original13-observation refit blocks, restarted at each segment's first
issue, and score the same complete validation/evaluation origins.

The original QR33 penalty menu is0.001/0.01/0.1; every validation candidate
must finish, with larger penalty breaking an exact loss tie. The original
QR4 menu additionally includes1/10; it selects among completed candidates,
with the first increasing penalty breaking a tie. Keep every candidate
failure and its diagnostics. An evaluation failure is a missing full method,
never a request to try a different penalty. Solver limits/tolerances stay
at their original values. No random procedure or new inferential test is used.

Save all12 method slots and32 validation candidate slots, including any NA,
the eight named regression-versus-F contrasts, selected parameters, mature
training bounds and actual execution resources. Pinball loss uses tau19/20;
strict breaches use peak>capacity. Retain full precision in stored tables.

## Support, non-support and causal limits

For each regression separately, classify all four completed comparisons as
TREASURY_LIKE if F has lower mean loss in at least three; as
CONDITIONAL_GAINS_PERSIST if regression wins at least three; otherwise MIXED.
Any missing comparison makes that procedure's overall classification
INCONCLUSIVE, with available signs and denominators still reported. Exact
ties count as neither side's win. These are finite-record descriptive rules,
not significance tests, and comparisons share data and overlapping targets.

Any complete daily regression gain is a descriptive counterexample to a
literal assertion that conditioning requires hourly observations. Persistent
daily gains weaken an hourly-only explanation. Historical dominance is
consistent with an aggregation/history-scale explanation within the same
source. Neither pattern identifies a pure sampling-frequency or source effect:
physical horizons, physical histories and the sampled response change jointly.
The same dealer is not an independent dealer replication. The decision map
must preserve these boundaries and every adverse or inconclusive cell.

## Execution and stop conditions

One numerical worker, one requested numerical thread, observed OS threads<=2,
internal RSS stop1.5GiB and public cap2GiB. One W/H cell has540s internal and
600s hard limits, with a global1800s limit interrupting an in-flight child.
Run W ascending, H6 then24, and F/QR33/QR4 in that order. Keep interrupted and
unattempted slots; do not retry with changed settings or expand the design.
All original results and WP3-sealed source/protocol files remain unchanged.
