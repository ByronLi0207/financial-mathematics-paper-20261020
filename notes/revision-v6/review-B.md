# Internal self-review B — financial economics

**Status:** Author-side internal self-review prepared for WP1 on 23 October 2026. This is not an external referee report, a journal decision, an independent financial replication, or a Claude/Cloud review.

**Task understood:** Review the current `revision-v4-jof` submission package for economic meaning, dealer-inventory positioning, data representativeness and practical value, then assign each concern to a text edit, authorized WP2–WP5 work, or an explicit limitation. I read the current manuscript and supplement independently; I did not read the other internal reviewer reports. No forecasts or new analyses were run for this review. Numerical statements below are readbacks of the existing submission content, not independently reproduced results.

**Overall diagnosis:** The paper has become much more defensible as a retrospective benchmark of a precisely measured peak functional. Its main economic vulnerability is the distance between that scalar functional and a dealer's actual inventory risk, balance-sheet utilization or funding decision. The existing caveats often address this distance correctly; they should be preserved during v6 rather than replaced by stronger application language after adding benchmarks. Mature practice in the inspected primary literature is to define the economic exposure and unit of observation before interpreting forecast performance, and to evaluate calibration alongside the relevant predictive score. The authorized v6 analyses can strengthen the forecast comparison. They cannot supply missing dealer books, an intervention counterfactual, decision costs, first-release history or a fresh external dealer sample.

Evidence locators use zero-based JSON pointers into `submission-jof/manuscript-content.json` (M) and `submission-jof/supplement-content.json` (S). Primary links were reopened during this review. A severity of major denotes a material interpretation or scope issue, including issues that are already adequately bounded and should remain limitations.

## B1 — Major: The stipulated score does not identify economic value

**Evidence.** M `/sections/4/blocks/7` explicitly treats the pinball asymmetry as stipulated, distinguishes unconditional underprediction and overprediction amounts from report headroom, and rejects an observed-cost interpretation. M `/sections/6/blocks/3` already recognizes that a cost per breach or a nonlinear loss can change a fixed-report ranking. M `/sections/9/blocks/4` lists the missing quotes, fills, hedges, collateral and cash-flow inputs. These are substantive qualifications, not disposable disclaimers. The FR 2004 reporting framework separately records positions and financing; its instructions use different accounting conventions for FR 2004A positions and FR 2004C financing, reinforcing why a position amount alone is not a cash requirement ([official instructions, A-1 and Appendix B](https://www.federalreserve.gov/apps/reportingforms/Download/DownloadAttachment?guid=950ab256-b485-4586-99b0-b27eb205fdfa)).

**Concern.** Lower score, smaller reported headroom, fewer breaches and lower realized funding cost are different outcomes. In particular, reduced overprediction is not evidence that excess cash was actually held or released.

**Disposition — limitation.** Retain the current explicit decision-cost boundary, and apply it to all WP2–WP5 interpretation and the cover letter. A sufficient response is: “The score evaluates a stipulated quantile objective; realized financing or inventory-policy value requires decision-linked data that are unavailable here.” No new funding simulation is requested.

## B2 — Major: Aggregate cancellation changes the exposure being forecast

**Evidence.** M `/sections/2/blocks/1` correctly describes the absolute value of a dealer-aggregate signed position. Duffie et al. distinguish within-dealer absolute imbalances from taking an absolute value after signed dealer aggregation; their footnote 17 explicitly discusses offsetting positions. Their principal capacity constructions also use risk adjustments and dealer-level scaling ([official report, printed pp. 23–24 and footnote 17 on p. 27](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf)). M `/sections/7/blocks/1` and S `/sections/11/blocks/0` correctly identify the added panel as related aggregate tasks.

**Concern.** At a given time, `|sum_d N_d| <= sum_d |N_d|`. Consequently the peak of the signed aggregate is not the peak of total dealer magnitudes or a bound on each dealer's exposure. A low aggregate can conceal large offsetting books. The additional Treasury tasks broaden measured tasks but do not resolve that missing cross section.

**Disposition — this-round edit, with retained limitation.** Add one concise sentence to the transport interpretation or Table 6 caution explicitly distinguishing the absolute aggregate peak from aggregate absolute dealer inventories. Keep “related aggregate tasks” in the panel summaries. The adverse panel results delimit the executed forecasting specifications on these measurements; they do not establish a failure to forecast industry funding needs. No disaggregation analysis is requested.

## B3 — Major: The FX source is an attributed sample of client flow, not a verified complete dealer book

**Evidence.** M `/sections/2/blocks/0` uses one scalar over 2014–2017; M `/sections/9/blocks/8` acknowledges unverified commercial completeness and measurement accuracy. The original source paper describes a sample of one market maker's client flow involving its five most liquid currency pairs, measured hourly in USD ([Wisniewski et al., Section 3.1, physical p. 4](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf)). That supports the attributed data lineage, not a claim about all dealer business or residual inventory after every hedge. I did not obtain additional raw-book evidence, and the Kaggle page's substantive documentation was not readable through the web tool.

**Concern.** “One market maker” can be read too broadly if the original source's sampling qualification disappears. Neither the record count nor the related Treasury panel identifies representativeness across dealers, markets, currencies or later business practices.

**Disposition — this-round edit plus limitation.** Restore the word “sample” in the first FX data description, for example “a source-attributed sample of one market maker's client-flow-derived positions.” Preserve the missing complete-book and unseen-dealer qualifications. WP2–WP5 remain retrospective analyses of these same observations and cannot count as independent dealer validation.

## B4 — Major: The Treasury known floor belongs to the replay information convention

**Evidence.** M `/sections/2/blocks/4` states that the current economic-date observation is treated as known by convention and that the exercise is not an as-released backtest. The current NYFed page says statistics normally update on Thursdays with the previous week's observations ([official release description](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics)). S `/sections/11/blocks/2`–`3` distinguishes capture and issue timestamps, retains a future-vintage amendment, and says the live issuance adapter has not been implemented.

**Concern.** “Issue-known floor” without the replay qualification can sound operational for a public-data user at the economic date. The mathematical floor result is conditional on observing the anchor; it does not make an unpublished aggregate publicly observable. Adding ACI, CAViaR or combinations cannot repair the historical publication-clock gap.

**Disposition — this-round edit plus limitation.** When integrating new Treasury results, attach “downloaded-vintage economic-date replay” to the first main-text comparison or its caption, rather than relying only on Section 3. Preserve the no-prospective-validation statement and do not describe the unimplemented adapter as completed. Building that adapter is outside the authorized WPs.

## B5 — Minor: Keep recorded sampling and operational monitoring horizons distinct

**Evidence.** M `/sections/2/blocks/0` retains both one-hour and forty-nine-hour FX adjacent gaps, and M `/sections/2/blocks/3` defines H in subsequent source records. Treasury observes weekly closes. The target in M `/sections/3/blocks/3` is a maximum over those recorded observations, including the issue anchor; the motivating illustration in M `/sections/0/blocks/1` already disclaims the unobserved between-record maximum.

**Concern.** “Short horizon,” “hourly peak” or “six-hour monitoring” can inadvertently imply a fixed elapsed horizon or continuous intraday coverage. The weekly task is particularly remote from the maximum cash or securities need within each week.

**Disposition — this-round edit.** Add “H counts source records; between-record peaks are unobserved” to the decision-map note or the new supplement introduction. Preserve the sampled-target wording in the abstract and captions. No interpolation, alternative horizon or new intraday experiment is requested.

## B6 — Major: Explain how the dealer-inventory literature motivates this passive forecast without identifying a control policy

**Evidence.** M `/sections/0/blocks/0` cites Ho–Stoll, Lyons and Hansch et al. as economic motivation. M `/sections/9/blocks/4` distinguishes the passive envelope from an active quoting model. The inspected Hansch et al. primary abstract links relative dealer inventories to dealer behavior and documents nonlinear inventory adjustment ([published article](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00067)). That is a behavioral mechanism involving actions and relative positions, whereas this paper forecasts a scalar under the realized historical business process. I did not newly verify the complete Ho–Stoll or Lyons articles; no claim of a complete dealer-literature audit is made here.

**Concern.** An improved envelope forecast does not show how quotes, hedges or client selection should change, and deploying such actions could change future position dynamics. These data do not identify the counterfactual law under a different inventory policy.

**Disposition — this-round edit.** Add one sentence connecting the literature to the narrower use: “Inventory-control studies motivate monitoring, but this passive forecasting exercise does not estimate the effects of changing quotes or hedges.” Keep the contribution as predictive validation, without a new inventory-control model or policy experiment.

## B7 — Major: Separate a score–breach coexistence finding from a claim about a calibrated model advantage

**Evidence.** M Table 3 (`/sections/5/blocks/0`) reports lower matched FX loss with more all-origin breaches; Table 4 uses a different, explicitly sparse diagnostic grid. The closest endpoint lineage already compares conformal methods with ordinary quantile procedures and evaluates interval calibration ([Wisniewski et al., Sections 4.1–4.3](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf)). Gibbs and Candès provide the primary ACI framework, which wraps estimated predictions or quantiles ([NeurIPS 2021 proceedings](https://proceedings.neurips.cc/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html)).

**Concern.** The current coexistence result is legitimate, but whether QR retains an advantage after adaptive coverage correction remains unanswered. Failure to reject a sparse-grid diagnostic is also not proof of calibrated conditional risk. The economic interpretation should not assume the answer favors QR.

**Disposition — route to WP2.** Compare the frozen F and selected QR wrappers using only matured feedback and the frozen selection menu, then retain all score and coverage outcomes. Describe CAViaR as the specified adaptation to peak headroom, rather than a literal replication of a return-VaR application. A delayed-feedback, overlapping-label implementation needs its stated guarantees qualified; a standard ACI citation alone does not establish conditional coverage for this adaptation. Preserve the two original primaries and distinguish full-origin breach counts from sparse-grid tests.

## B8 — Minor: Simple combinations are necessary context for practical model comparison

**Evidence.** The current decision map, M `/sections/8/blocks/3`, organizes method evidence but contains no executed forecast-combination comparator. The v6 plan fixes equal averaging of F and QR and the median of F, QR and KNN before the new results are observed.

**Concern.** A practitioner considering whether conditional complexity is useful can reasonably ask whether a simple fixed combination offers a better score–coverage balance. A combined report would be another candidate forecast; its retrospective performance would not establish a new operational switching policy. This is a reviewer judgment about comparator relevance, not a literature-priority claim.

**Disposition — route to WP3.** Report both prescribed combinations for every required complete cell, including ties, deterioration and unavailable constituents. Evaluate their loss, breaches and prescribed comparisons without tuning weights after seeing outcomes. Update the decision map only if the actual results materially change its descriptive message; do not presume combinations improve either source.

## B9 — Minor: WP4 states measure position-change volatility, not Treasury yield or FX price volatility

**Evidence.** M `/sections/3/blocks/9`–`10` defines RMS from changes in the signed position scalar. M `/sections/8/blocks/1` already disclaims a causal frequency effect. Duffie et al.'s economic setting distinguishes yield volatility from intermediation-capacity measures ([official report](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf)); the present RMS variable is not an observed yield-volatility series.

**Concern.** “QR works in high volatility” would overstate the state measurement if readers understand volatility as market price risk. The same RMS can reflect client-flow dynamics, scale, valuations or reporting changes. State-specific average score differences cannot identify the causal mechanism or a deployable regime rule.

**Disposition — route to WP4.** Name the state “issue-known position-increment RMS” or “position-change volatility,” freeze the training-only cut points and matured loss instruments as planned, and report actual directions with HAC uncertainty. Preserve the descriptive status of Table 6. No market-price variables, new regime search or policy backtest is requested.

## B10 — Major: Quantile-level robustness tests a forecast target, not observed economic preferences

**Evidence.** M `/sections/3/blocks/13` fixes the current estimation level, while M `/sections/6/blocks/4` describes a different exercise that holds archived reports fixed and changes loss weights. WP5 instead refits at its two predeclared quantile levels. These are distinct comparisons; M `/sections/4/blocks/7` correctly rejects interpreting the current score ratio as an observed financing-price ratio.

**Concern.** Fixed-report preference sensitivity cannot substitute for a newly estimated tail quantile. Conversely, stable rankings under WP5 would strengthen target-level robustness but would not validate a bank's objective, stress loss or capital requirement. At the more extreme level, limited mature observations can undermine informative comparison, particularly in the weekly tasks.

**Disposition — route to WP5.** Keep refitting, validation selection and sample-failure rules frozen before evaluation, show direction reversals and NA cells, and describe the output as quantile-level robustness. Do not characterize it as welfare, funding-price or regulatory-capital robustness. Treat the choice of an institution-specific decision objective as an explicit limitation.

## B11 — Minor: Preserve the correct boundary between a known floor, an atom and fitted coverage

**Evidence.** M Proposition 1 (`/sections/3/blocks/20`–`23`) correctly makes the floor projection a pointwise scoring result and the strict-tail inequality a population-quantile result. M `/sections/9/blocks/3` and S `/sections/14/blocks/12` explicitly show that the floor need not create an atom. M `/sections/3/blocks/34` also confirms that the historical controls already use current information.

**Concern.** The known floor is an informative feasibility restriction, but it neither proves that fitted reports meet a desired breach rate nor supplies a separate economic benefit relative to controls using that same restriction. Equality-based coverage tests require their stated null, especially with discrete or rounded measurements. This part is already handled well and should not be simplified incorrectly during English editing.

**Disposition — limitation; preserve existing text.** Keep the population-versus-fitted distinction and do not attribute excess conservatism automatically to a floor atom. Apply the same floor consistently to the authorized new reports. A sufficient response is: “The common observed floor is a feasibility constraint; it supplies neither fitted conditional calibration nor identified financing value.” No new floor analysis is requested.

## Disposition register for WP1 integration

| ID | Severity | Primary disposition | Concrete closure criterion |
|---|---|---|---|
| B1 | Major | Limitation | Preserve stipulated-score versus realized-cost boundary in new results and cover letter. |
| B2 | Major | This-round edit | Explicit absolute-aggregate versus dealer-magnitude distinction; retain related-task scope. |
| B3 | Major | This-round edit + limitation | Restore original FX sampling qualification; no new independent-validation claim. |
| B4 | Major | This-round edit + limitation | Attach replay information convention to first new Treasury comparison; prospective results remain pending. |
| B5 | Minor | This-round edit | Decision-map/supplement note states recorded horizons and unobserved between-record peaks. |
| B6 | Major | This-round edit | One sentence separates passive forecasts from effects of inventory-control actions. |
| B7 | Major | WP2 | Report actual calibrated-wrapper and CAViaR results with mature timing and qualified guarantees. |
| B8 | Minor | WP3 | Report the two frozen combinations, including adverse/tied/NA results. |
| B9 | Minor | WP4 | Correct state label; actual state effects and uncertainty; no inferred switching policy. |
| B10 | Major | WP5 | Refit target-level sensitivity with reversals/NA retained; no cost-preference inference. |
| B11 | Minor | Limitation | Preserve floor/atom/population/fitted distinctions for all added reports. |

**Review boundary:** These are requested dispositions, not claims that the edits or WPs have already been completed. The economic limitations in B1–B4 and B6 remain after any statistically favorable new benchmark result. No analysis beyond WP2–WP5 is requested, and no forecast family is assumed to win.
