# WP4 original-rule audit before daily aggregation

Scope: source code, frozen protocol and existing descriptive metadata only.
No raw FX values were read, no daily series was constructed, and no model,
forecast, score or new financial test was run for this audit. This note is not
the WP4 freeze and does not alter any original or WP3 sealed source file.

## Original Treasury split: fixed dates and indices, not percentages

`protocol/revision-20261022/study-spec.json:55–77` declares the accepted
`nyfed_weekly` input, its 706 observations and these exact settings:

```text
validation_origin_first = 329
validation_origin_last  = 380
evaluation_origin_first = 405
evaluation_origin_last  = 681
evaluation_first_date  = 2021-01-06
evaluation_last_date   = 2026-04-22
windows                = [52,260]
refit_step             = 13
short_scale / long_scale = 6 / 26
nominal_gap_seconds    = 604800
```

The corresponding design passage at
`protocol/revision-20261022/conditional-baseline-design.md:31–37` says that the
downloaded Treasury snapshot spans 2013-04-03 to 2026-10-07. Evaluation starts
at 2021-01-01 or the next observation, which is index405 / 2021-01-06, and
ends at index681 so the last common 24-record peak is observable. Validation
is the 52 origins329–380, with all validation labels complete before evaluation.
There is **no 80/20 or 60/20/20 split rule** in this contract. Describing such a
percentage split as the original Treasury procedure would be unsupported.

**Scope MISMATCH:** the Treasury absolute 2021 evaluation start is not the
FX study's calendar split. The existing FX evaluation ends at origin18551 /
2017-01-23, as recorded in `protocol/supervisor-20261023/r6-design.md:31–32`.
A daily-FX analysis may carry
over the Treasury observation-index geometry, but must state that adaptation
and must not call it the same calendar split or a proportional split.

## Parent-selected WP4 geometry to freeze

The parent has selected the following before any aggregation or outcome access:

- Use the Treasury validation origins329–380, inclusive.
- Use common evaluation origins405 through `n_daily−25`, inclusive. Equivalently,
  the last issue is `n_daily−max(H)−1`, keeping both H6 and H24 on the same grid.
- Use W52 and W260; H6 and H24; refit every13 observed daily records from the
  first issue of **each** validation/evaluation segment.
- Retain the original weekly RMS spans6/26 in observation units, with a daily
  nominal interval86400 seconds. This is a declared adaptation, not equality
  of physical memory lengths across hourly, daily and weekly records.
- Inadequate validation, complete outcomes, common evaluation grid or mature
  training history makes the affected procedure/cell NA. Do not shorten W,
  truncate a candidate's score, move the cut, or fill empty days to create a
  completed result. In particular an empty common evaluation grid is NA.

These instructions remain a pre-result recommendation/decision record until
the parent commits the actual WP4 protocol and executable freeze.

## Daily selection and issue-time availability

The parser at `conditional_sources.py:121–129` preserves FX's original
`%Y.%m.%dT%H:%M:%S.%f` timestamp convention and rejects timezone-aware or
nonincreasing observations. The source timestamps are naive; do not assert
UTC, local exchange time, or a particular trading session. The original
design explicitly calls them source-naive at
`protocol/revision-20261022/conditional-baseline-design.md:13`.

Selecting a day's *last* recorded row is known only once that source-calendar
day has ended. The parent therefore selected this causal report clock:

1. Group observations by their original source-naive calendar day.
2. For each **ended** day with at least one record, select the final recorded
   position; assign its report issue time to that day's 23:59:59.999999.
3. Keep empty days absent. Do not interpolate or fill weekend/missing days.
4. Calculate the daily gap flag from successive day-end issue times against
   the declared86400-second interval. Keep selected original row indices and
   timestamps as private provenance if needed, with public fingerprints/counts.

This is a last-record daily proxy, not a reconstructed true continuous position
at market close. The target is the sampled peak among these daily proxies,
including the current proxy; it excludes intraday excursions. Retaining a
last-observation timestamp instead would require an explicit retrospective
sampling-time qualification and should not silently be described as a live
issue-known closing rule.

## Predictor and mature-label rules

`conditional_features.py:35–65` constructs exactly33 slopes:

- columns0–24: current signed level and24 observed-record lags;
- column25: current absolute level;
- columns26–27: past-only increment RMS at the declared short/long spans;
- columns28–29: sine/cosine source-clock hour;
- columns30–31: sine/cosine Monday-zero weekday;
- column32: the just-observed adjacent-time gap exceeds the nominal interval.

The valid-from index is `max(24,long_scale,short_scale)`
(`conditional_features.py:39`), so the selected daily spans give valid-from26.
Fixed day-end issue times make the hour pair constant. The original
training-only standardizer correctly centers exact constants and assigns
scale1 (`conditional_features.py:68–79`); do not delete these columns or learn
their transform on validation/evaluation as a full series.

At refit r, the W training origins are exactly
`[r−H−W+1, …, r−H]`, all with label end at or before r.
`conditional_features.py:94–105` implements that pool and the segment-relative
refit clock. It raises on inadequate feature history. The original QR checks
`cache.label_end[pool] <= r` at `conditional_study.py:103–114`.
F may use feature-valid minimum0; QR33 and QR4 must use the feature-valid
minimum26. All methods must share the declared validation/evaluation issue
grid when their comparisons are scored.

QR4 uses precisely columns `[25,0,26,27]`, a C-order copy, and training-only
population mean/std scaling: `parsimonious_v3.py:17–26`. It retains the mature
pool, response scaling and current-position floor at
`parsimonious_v3.py:28–47`. This is the original full procedure, not a new
feature search.

## Menus, failures and matched historical comparator

Original QR33:

- penalties `[0.001,0.01,0.1]` at
  `protocol/revision-20261022/study-spec.json:9`;
- select minimum validation mean **final-capacity** pinball, not the normalized
  training objective; exact ties prefer the larger penalty;
- all declared candidates must complete the full common validation grid; any
  failed/incomplete candidate makes that QR33 cell ineligible;
- selected evaluation failure leaves the whole procedure unavailable, without
  trying a different parameter or dropping issue rows.

Evidence: protocol lines27–30 and `conditional_study.py:232–249`.

Original QR4:

- penalties `[0.001,0.01,0.1,1,10]`, evaluated in increasing order;
- select among completed candidates, minimum validation mean loss; `min` keeps
  the first increasing-menu candidate at an exact tie;
- retain every failed candidate; all candidates failed leaves the procedure
  unavailable; selected evaluation failure stays failed without replacement.

Evidence: `parsimonious_v3.py:60–78`. These inherited menus and candidate-failure
policies differ from QR33, so their comparison cannot identify a pure causal
feature-count effect.

For the same-window comparison, use **F only** with the same refit13 pool and
the current issue's absolute-position floor. The historical corrected rank is
`ceil((W+1)*19/20)`; F is not an empirically optimized rank endpoint.
The rank-objective distinction is already explicit in the original design
at `conditional-baseline-design.md:19` and should remain a qualification.

**Whitelist trap:** `conditional_study.issue_historical:165–169` computes S/K
along with F even when a caller takes only its first result;
`historical_forecasts:174–190` computes rolling/frozen F/S/K sets. Do not call
those multi-method helpers in WP4. The already sealed WP3 F-only primitive
can be called without editing its file, or a separate F-only wrapper can be
implemented and verified against the same source arithmetic.

## Solver and measured-resource boundary

Keep the original solver max10000 iterations, absolute tolerance1e-6,
relative tolerance1e-5 and `gap_rtol=1e-6` (gap tolerance is that factor times
`1 + primal_objective`); unpenalized intercept and the
existing training-only response scale. Source:
`protocol/revision-20261022/study-spec.json:10–19` and
`conditional-baseline-design.md:15`. No tolerance widening, additional
penalties or favorable shortened scores after a failure.

Use one financial worker, request one numerical thread, observe OS-thread/RSS
snapshots, and keep the original internal540-second /1.5GiB and hard600-second
/2GiB /two-observed-thread limits. The budget values are declared in
`protocol/revision-20261022/study-spec.json:90` and implemented/observed at
`run_study.py:67–87,169–194,238–267`. Limits are not measurements; save actual
elapsed time, observed threads, RSS and the failure cause. Split only by the
predeclared four H/W cells if necessary, never after seeing favorable losses.

## Interpretation and reporting boundary

Daily versus hourly FX holds the underlying recorded dealer source fixed.
It still changes the sampled response, observation count, calendar span of W/H,
calendar predictors and update cadence. Daily FX versus weekly Treasury also
changes the institution/aggregation and economic position definition. Thus
these comparisons provide a within-record aggregation sensitivity and a
source-adapted comparison; they cannot isolate a causal frequency coefficient
or establish that data source alone caused a ranking difference.

Historical wins on daily FX would be consistent with a frequency/sample-size
explanation; persistent daily FX regression gains would keep source-specific
explanations plausible. Mixed/NA results remain mixed/NA. No outcome can become
compatible independent dealer validation or prospective validation. Publish
the full fixed-cell score/breach/eligibility record and update the decision map
with this bounded interpretation. Raw hourly/daily observations and per-issue
private trajectories remain outside Git; distribute acquisition fingerprints,
code and aggregate results under the source rights boundary.

## Actual audit commands

The original code/protocol passages above were read with these command forms:

```text
nl -ba protocol/revision-20261022/study-spec.json | sed -n '1,220p'
nl -ba protocol/revision-20261022/conditional-baseline-design.md | sed -n '1,240p'
nl -ba conditional_features.py | sed -n '1,170p'
nl -ba conditional_study.py | sed -n '24,145p'
nl -ba conditional_study.py | sed -n '145,198p'
nl -ba conditional_study.py | sed -n '225,255p'
nl -ba parsimonious_v3.py | sed -n '1,110p'
nl -ba conditional_sources.py | sed -n '90,168p'
nl -ba run_study.py | sed -n '65,87p'
nl -ba run_study.py | sed -n '169,200p'
nl -ba run_study.py | sed -n '238,270p'
```

Two preliminary broad `rg` commands encountered unmatched zsh globs or an
absent `REPRODUCE.md`; the explicit existing-file reads above supplied the
actual evidence. Those failed searches did not read raw observations, change
files or create results. No computational acceptance or completed WP4 result
is claimed by this note.
