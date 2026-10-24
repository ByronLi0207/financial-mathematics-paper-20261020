# Future-only amendment: an immutable first-actually-captured measurement path

Drafted 23 October 2026, before any prospective report issuance. This is a local protocol amendment for review and a new binding; it is not a public preregistration, a forecast service, an issued forecast or a prospective result.

This amendment clarifies the measurement-vintage rule left open by `prospective-public-release-protocol.md`. Preserve that original file and its recorded hash unchanged. Preserve the original historical inputs, selections, two primaries and retrospective results unchanged. A new adoption record must identify this amendment, the prior protocol, the retained parameter binding and the relevant acquisition manifests before the first prospective forecast. The methods, parameters, target horizon, 13-record refit schedule and 52-origin assessment plan remain as previously specified.

## 1. Measurement definition and explicit join

For each of the original Treasury-bill series and the twelve accepted panel series, maintain one immutable weekly path, denoted here by \(\widetilde N_t\). This is an **as-captured measurement path**, not a claim to reconstruct the publisher's first-release truth or a single-vintage history.

- The accepted historical prefix through economic 7 October 2026 stays exactly as used in the retained source-specific study. Bind its source receipt, date grid and values to the existing fingerprints; do not replace it with revised history from a new API response.
- Economic 14 October 2026 is an explicit bridge. It was already public before this amendment and is not an unseen prospective origin. Bind the first actually retained official-response receipt used to supply this bridge before any prospective issuance. If no such receipt exists for a series, acquire and record it before that series can issue its first prospective report; do not invent a previously observed capture. The bridge is not eligible for a retrospectively generated prospective forecast.
- For every subsequent economic week, append its value once from the first official response that is actually captured and retained for that series. Freeze the exact observation and its capture manifest. Subsequent responses must not overwrite it, even if the publisher revises that date.

The prefix, bridge and future records therefore form a declared join across acquisition vintages. That join is intentional and auditable; it is not evidence of economic measurement invariance, an original-release vintage or the contents of an individual dealer book. An alternative revised-history analysis, if later desired, must have a separate design and output label and cannot replace the main path or its scores.

For each appended record retain the series key, economic date, original value token, official URL, entire response bytes and SHA-256, actual acquisition start/end UTC times, available HTTP timing/version metadata, and the manifest/code identities. Distinguish a locally recorded acquisition timestamp, an HTTP server timestamp and a verified publication timestamp. Missing publication/version metadata remains unknown. A capture hash proves file identity, not that no earlier publisher version existed.

## 2. Fixed calendar, capture deadline and missed issues

The first planned new prospective economic origin is 21 October 2026, ordinarily released on 29 October. The 52 assessment origins are the 52 consecutive weekly economic dates beginning at that origin. They are not the next 52 successful forecasts or captures. Missing and late weeks consume their original calendar positions and are never replaced or used to extend the plan.

The administrative capture deadline for an economic origin is 24 hours after the official scheduled release carrying that observation. Record the schedule evidence and timezone. The ordinary illustration uses Thursday approximately 16:15 in `America/New_York`; an official announced holiday or release rescheduling supersedes that illustration and must be recorded. If no authoritative rescheduled time is available, retain the previously documented deadline and flag the uncertainty; do not move a deadline retrospectively because a later capture would produce a desired forecast. Actual acquisition and publication evidence always remain separately recorded.

An eligible on-time issue requires both a retained capture and a timestamped forecast artifact before that deadline, with the forecast created after the capture and before a subsequent observation is captured or known to have been released. This tighter boundary prevents a delayed forecast from using an intervening observation. If the issue is late, missing, cannot establish this information boundary, or cannot complete its specified method, retain its status as NA. Do not issue a hindsight report for that origin, substitute an old forecast or silently classify it as on time.

A late observation can subsequently be appended to the immutable path when first actually captured, with its true late acquisition time. It may then become available for later issues or complete the target of an earlier forecast. It cannot resurrect its own missed forecast or make that forecast retrospectively on time. If a response first supplies several previously missing economic weeks, record each at that actual capture time; do not backdate their availability.

## 3. Information admissibility and scheduled refits

All four methods use the same source-specific immutable path, calendar indices, captured issue anchor and availability records. No method receives a revised value, earlier version or additional observation unavailable to the others at that issue. A value is admissible only after its actual retained capture, regardless of its earlier economic date.

Keep horizon and refit indices on the original weekly calendar. A missing capture does not shorten a horizon, remove a week, reset the refit phase or change the first prospective origin. At a scheduled refit \(\kappa\), the completed-origin pool remains exactly \(\kappa-H-W+1,\ldots,\kappa-H\). Every component of every required label and every required causal feature must have been captured by the actual fit/issue information cutoff. Economic-date maturity alone is insufficient if a necessary capture is missing.

If that prescribed pool or feature history is unavailable at a scheduled refit, the proposed prospective continuation rule is to retain a failed refit and NA reports for the affected method's refit block. Do not use a shorter pool, revised historical prefix, fallback model, off-schedule retry or delayed fit within the block. At the next originally scheduled refit the method may use information actually available then, retaining the earlier NA history. This is a future protocol rule that preserves the fixed schedule, not a description of behavior already executed or implemented in the current batch routines.

### Implementation boundary: protocol only

The current frozen routines are complete-data batch functions: they reject nonfinite input prefixes and abort failed cells under their recorded retrospective policies. No operational release-capture, missing-week handling or refit-continuation adapter is implemented or validated in this revision. The rule above does not change that code, its existing NA behavior or any historical result.

Before the first prospective issuance, a separately identified adapter would have to preserve the frozen procedures' complete-data forecasts, pass causal future-perturbation and explicit missing/late-capture/refit-failure fixtures, and receive its own timestamped implementation/test binding. It must enforce capture availability and the fixed calendar without quietly modifying current batch code. If the required data or refit cannot support an issue, the report remains NA; no filled forecast, substituted score or complete-procedure average may be claimed. This amendment alone does not establish that such an adapter exists or that those checks passed.

## 4. Target, issue floor and outcome maturity

The prospective target and floor are

\[
\widetilde P_{t,H}=\max_{0\le h\le H}|\widetilde N_{t+h}|,
\qquad \widetilde B_t=|\widetilde N_t|.
\]

The target includes the captured issue anchor and exactly the next \(H\) economic weeks, for \(H+1\) recorded components. It is not a maximum over the next \(H\) successful captures. The captured path defines the main target for all methods, so its known-floor identity is preserved. Publication lag still makes this a prediction of unpublished measurements with a nowcast/forecast mixture; it is not a wholly future physical inventory-path guarantee.

A target becomes scoreable only after all its exact calendar components have been retained. Record the actual last required capture time, relevant publication evidence and the identities of every component receipt. Later revisions cannot change the target, floor, loss or hit already defined by this path. If a component is missing, the target remains pending or unavailable with an explicit reason; do not interpolate it or replace it with another date.

The previously listed dates remain conditional calendar illustrations. For the planned 21 October origin, \(H=6\) ends economically 2 December and ordinarily becomes publicly available 10 December; actual complete capture may be later. The corresponding \(H=24\) illustration is 7 April 2027 economically and 15 April ordinarily publicly available. These dates are not evidence that reports were issued or outcomes captured. No service or forecast starts by writing this amendment.

## 5. Revision log, reporting and unchanged evidence

Retain a separate revision log for every later response that disagrees with an already frozen component: old/new tokens, economic date, capture time and response hashes. Preserve both response files; do not rewrite the frozen as-captured main path. Apparent corrections, source-key definition changes or schema failures require an explicit recorded status and cannot justify a silent join or replacement.

Report the original 52-origin denominator together with on-time issued, missed/late, method-failed, target-pending, target-complete and commonly scoreable counts for every source/horizon/window. Any descriptive mean calculated on a commonly scoreable subset must identify that subset and its denominator; it is not a completed 52-origin procedure result. Keep the originally planned inference timing and qualifications, and never extend or stop the sequence based on significance or favorable loss. Retain all adverse scores and every NA.

This is a future measurement and availability clarification before first issuance. It neither repairs nor changes the historical downloaded-vintage replay, the local round2 results, their negative findings, the original two primaries or the still missing compatible independent-dealer evidence.
