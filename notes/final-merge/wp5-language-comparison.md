# WP5 language before/after

Same frozen extraction and counting code SHA-256: `47f7bd1b61d08eac0ef7fd6ccc82aced9bb6e5a7cd74818937b3af246d975794`. All scientific outputs and the WP2 preregistration remain unchanged.

## Abstract before (exact WP4 wording)

```tex
Dealers monitor the largest absolute position reached before a review horizon ends. We compare conditional quantile models with historical rules using hourly FX positions, weekly New York Fed positions and dealer aggregates in 17 CFTC futures markets. Histories and update schedules are matched. Historical rules are hard to beat. First, FX regression lowers matched loss by 14.8\% and 16.6\% across two periods, but its ranking against a shorter rolling rule changes. Second, historical rules beat regression in 34 of 48 New York Fed comparisons and 29 of 34 CFTC comparisons; finite-penalty hindsight still favors history in most short weekly comparisons. They usually remain in the model confidence set alongside alternatives. In calibrated simulations, expanding the penalty menu cuts the constant-parameter median excess loss from 116.2\% to near zero; switching adds no observed median loss in this short-history comparison. Third, in CFTC, lower scores need not mean lower limit costs: higher reserve charges and lower fixed breach charges generally favor expanded regression. The evidence is retrospective, and the original FX evaluation period had been inspected beforehand.
```

## Abstract after (exact current wording)

```tex
Position limits concern the largest sampled absolute net position during a review period, which an endpoint forecast can miss. We compare historical and conditional quantile forecasts using one FX market maker's positions and aggregate dealer records from the New York Fed and CFTC. Historical rules are difficult to beat across these records, while longer-history FX gains coexist with adverse weekly outcomes and important exceptions. Simulations, learning curves and the partly supported CFTC check are consistent with estimation costs varying with history and shrinkage, while causal attribution remains unresolved. Practical validation should compare scores, breaches and stated limit costs against matched historical benchmarks, since different charges can favor different procedures.
```

| Gate | Before | After | Requirement |
|---|---:|---:|---|
| Abstract words | 175 | 109 | ≤170 |
| Abstract sentences | 10 | 5 | exactly5 |
| Mean sentence words, frozen rule | 15.515244 | 19.015528 |18–24|
| Maximum numerical values per sentence |13|2|≤2|
| Explicit grammatical negatives |47/328 (14.329268%)|2/322 (0.621118%)|≤8%|
| Banned phrase matches |6|0|0|

The broader adverse-or-uncertainty lexicon occurs in 37 baseline sentences and 58 revised sentences. Grammatical negation is distinct from scientific failures: PARTLY, every failed criterion, negative comparison, unavailable estimate and identification limitation remains explicit. The negative-sentence target is not a requirement to remove adverse findings.

The frozen extraction inserts FORMULA while omitting displayed identities. Removing those 9 marker words gives a lexical mean of 18.987578 words after editing (before 15.487805); the mean gate still passes. Both original censuses and the rule SHA are retained.

All46 narrative paragraphs in Introduction, Results, history and cost have a Chinese one-sentence explanation and exact paragraph SHA in `plain-summary.md` / `wp5-plain-summary-bindings.json`. Main subheadings state bounded findings; the first use of model confidence set is immediately defined.

Main source-text count excluding tables/references is5,998 under the separately recorded WP4 cap rule. Its scope differs from the readability census, which includes table notes and inline symbols. Actual main PDF22 pages; Supplement24 pages;6 main tables;4 main figures. Conservative PDF text before References including table/figure text is8,268 words.

Native main compile v3: exit0; zero overfull/undefined/multiply-defined/error diagnostics, zero underfull warnings. Four current main pages (1,12,16,18) were actually viewed with no observed clipping; this is representative QA, not the full WP8 all-page review. The unchanged Supplement retains5 inherited underfull warnings, already inspected at WP4.

First prose-rewrite command failed closed because a Python string interpreted a TeX backslash as a control character; the function had not yet written the manuscript. Raw-string correction allowed the source-exact replacement to proceed. Initial metric extraction formatting artefacts were repaired before the rule was frozen and before source edits. Both implementation failures are disclosed rather than presented as scientific failures.

Acceptance commands and exact outputs are in `wp5-command-output.txt` and are reproduced in `FINAL_MERGE_CHANGELOG.md`. No model, bootstrap, HAC or cost computation was run in this WP.
