# WP7 cover-letter integration response

Only `submission-jof/cover-letter.md` and this response note were edited. No manuscript, numerical result, source data, code, private trajectory, author declaration or other file was changed. This is a local letter draft for the paper package; no communication or journal submission occurred.

## Evidence-priority MISMATCH

The WP7 instruction asks the letter to say that the simulation has explained the mechanism and separated the frequency effect. The accepted evidence does not support that wording. Under the inherited evidence-priority rule, the letter reports what was actually obtained:

- **MISMATCH-WP7-LETTER-01 — mechanism confirmation.** `results/revision-v8/wp3/README.md` and `support.json` retain the failed frozen narrow-region criterion for both regressions. The letter says the controlled simulation tests the restriction and the criterion is not supported. It does not rescue the restriction through a new region or favorable subset.
- **MISMATCH-WP7-LETTER-02 — pure frequency separation.** `results/revision-v8/wp4/README.md`, especially its observation/interpretation boundaries, states that dealer identity is fixed while physical histories, horizons, update cadence, predictors and sampled targets change jointly. The letter calls this same-dealer daily aggregation, retains the conditional exception with more breaches, and expressly says it does not identify a pure frequency effect.
- **MISMATCH-WP5-01 retained — fresh third period.** `results/revision-v8/wp5/README.md` and `THREE_WINDOWS.md` disclose overlapping windows, prior scoring exposure and later-selected penalties. The letter describes an additional within-record comparison and those limits. “Observations covered by earlier scoring” deliberately avoids implying that every new issue origin had an identical previously scored forecast; the provenance proof concerns prior target-interval coverage and the nested earlier evaluation window.

## Framing and evidence boundaries

The opening now asks one forecasting question: what conditioning adds after history is matched, and whether the answer survives a changed reference and breach assessment. The contribution paragraph foregrounds the comparative application, named historical controls and score–breach disagreement. It labels the floor argument elementary and the bound classical, without claiming a new estimator, external review, independent validation, journal readiness, acceptance or demonstrated operating value. The original primary comparisons and adverse/failed outcomes remain part of the stated paper.

No numerical results were added to the letter. All empirical statements draw only on the accepted WP3–WP5 readouts. The author-completion placeholder and the requirement for personal authorship/permissions confirmation remain unchanged; no personal information, funding, conflict or AI declaration was supplied.

## Local checks

The following is the actual local structural-check output from the write/check operation (not a scientific result):

```json
{
  "baseline_commit": "642d6af",
  "checked_utc": "2026-10-24T11:19:02.881649+00:00",
  "before_sha256": "4d46c5748e44729d1acacfdfe6401476e75d9b6580aeeded6ad3333248339625",
  "after_sha256": "3c7c88356d3bf4feaf8854eaddbacdcbe22951bd80008075cc1509f7f2b05b7f",
  "before_words": 194,
  "after_words": 309,
  "reader_visible_numeric_tokens_added": [],
  "author_placeholder_preserved": true,
  "new_financial_computations": 0,
  "scope": "Letter writing from accepted WP3\u2013WP5 results; no result/source changes."
}
```

The original/revised source diff follows. Full paper coherence, compiled package verification and remote publication are later parent-task gates; this letter edit does not claim they have occurred.

```diff
--- cover-letter.md at642d6af
+++ cover-letter.md WP7
@@ -2,10 +2,12 @@
 
 Please consider “Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits” for Journal of Forecasting.
 
-The paper evaluates historical and conditional quantile forecasts of sampled peak net positions for a market-maker FX record and related weekly dealer-position aggregates. Historical rules provide a demanding benchmark. The clearest repeated regression gains use long FX histories and a short horizon against a same-history historical control. The later gain survives the evaluated coverage wrapper, while unwrapped regression breaches more often. Rankings against a shorter-history rolling rule change across periods, and the weekly comparisons remain largely adverse despite stronger regularization.
+This paper asks whether conditioning improves forecasts of sampled absolute-position peaks once historical information is matched, and whether observed gains survive a changed reference and a separate breach assessment. We compare a market-maker FX record with related weekly dealer-position aggregates. Historical rules are demanding competitors: regression gains occur in named FX comparisons, rankings change with the historical reference, and lower loss can accompany more breaches. The weekly comparisons remain largely unfavorable to regression despite stronger regularization.
 
-The contribution combines a precise known-floor peak target, a qualified application of the classical endpoint-to-peak bound, and evidence on reference sensitivity, score–breach disagreement and stability across related tasks. The manuscript separates distinct retrospective periods from independent or prospective validation, preserves numerical failures and adverse results, and provides complete source-linked result files and reproducible document sources.
+A controlled simulation with mean-reverting position levels and GARCH innovations tests a proposed restriction of conditional gains to a narrow history, horizon and volatility regime. The frozen criterion is not supported. Daily aggregation of the same recorded dealer produces predominantly historical-rule-favoring results, including a conditional exception with more breaches. Dealer identity is fixed, but physical histories, horizons, predictors and sampled targets change jointly; this contrast does not identify a pure frequency effect. A broader fixed-parameter backcast adds a within-record comparison, but overlaps the earlier backcast and reuses observations covered by earlier scoring; its penalties were selected later.
 
-The submission materials include the main manuscript, Online Supplement, title-page template and public code/result repository. The author must complete and personally confirm authorship, permissions and all journal-required declarations before any submission.
+The contribution is a comparative forecasting application for a precisely defined path-dependent position target, with mature-label implementation, matched historical controls and evidence on reference sensitivity and score–breach disagreement. The known-floor argument is elementary, and the endpoint-to-peak result applies a classical bound under explicit assumptions. These support the target formulation rather than a new estimation method. The original primary comparisons and all adverse or failed results remain intact. The manuscript distinguishes its retrospective diagnostics from independent-dealer or prospective validation.
+
+The materials include the main manuscript, Online Supplement, title-page template and public code/result repository. The author must complete and personally confirm authorship, permissions and all journal-required declarations before any submission.
 
 [TO BE COMPLETED BY AUTHOR]
```
