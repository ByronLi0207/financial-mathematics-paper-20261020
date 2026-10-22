# Flow direction, position endpoints and sampled peaks

A mature prediction method can address different financial questions. A fair transfer requires specifying which response is forecast, what is known when the forecast is issued, and how it is evaluated. Similar inventory terminology does not make published performance measures interchangeable.

## A nearby financial application

Challet, Chicheportiche, Lallouache and Kassibrakis, *Statistically validated lead-lag networks and inventory prediction in the foreign exchange market*, is consulted in its [fixed arXiv:1609.04640v3 author version](https://arxiv.org/pdf/1609.04640v3), uploaded 26 July 2018, with an internal date of 27 July 2018. The related formal 2018 article has DOI [10.1142/S0219525918500194](https://doi.org/10.1142/S0219525918500194); final-layout equivalence was not checked.

Its implemented responses are signs of next-hour net client flow and VWAP-change directions. Trader-group states and their lags feed random forests. The private data include a retail-oriented broker and a large dealing bank, with different predictive findings. Currency-weighted sign-performance displays use subsequently observed flow magnitudes; they are not issued amount forecasts or measured funding savings. These source-specific facts concern Sections 2–4 and Figures 8–11, rather than an implemented peak-quantile model.

## Three different comparison objects

| Application | Forecast response | Why its published score is not a score for another row |
|---|---|---|
| Trader-resolved direction study above | Sign of next-period net flow, or direction of a VWAP change | Classification does not supply the amount path or its upper peak quantile. The present analysis has no trader-ID/state panel on which to refit those classifiers. |
| [Wisniewski et al. (2020) and thesis Chapter 6](paper-evidence-map.md) | Next-record signed-position interval | Its reported interval pinball averages two endpoint losses. The present response includes multiple records, an absolute value, a known current floor and one upper-quantile preference. |
| [Current working paper](../../manuscript/working-paper/main.tex) | Maximum absolute source-reported net position at issue and over the next H records | An endpoint value, a directional success rate and a peak forecast answer different questions even when a model family or broad data source is shared. |

A nominal percentage also needs its response and tail convention. Wisniewski et al.'s interval score averages losses at α/2 and 1−α/2 for a central 1−α interval. At 95% interval coverage, its upper endpoint therefore uses .975, whereas this study specifies one .95 upper peak quantile. An identical percentage label would not make the tail preferences, response or score identical. This is a comparison of definitions, not a conversion of the published results. [Original Section 3.5](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf).

The present scalar N_t is a position level. It is not an hourly flow-sign label, a trader-state panel, a complete hedged book or a funding balance. Moving to the peak response changes both the outcome and the completion time of its historical labels. Even correct marginal endpoint forecasts do not uniquely determine the maximum's law without the relevant dependence information. A published direction model cannot fill that gap merely by changing the name of its output.

An analytical illustration uses N_t=1 and H=6. At every future record, the position is 2 with probability .01 and otherwise 1. In law A, all six future positions equal 2 on the same event of probability .01; otherwise all equal 1. Law B assigns probability .01 to each of the six paths with one future position equal to 2 and the other five equal to 1; the path with all six equal to 1 has probability .94. All six future marginal distributions agree between the laws. The peak nevertheless equals 2 with probability .01 under A and .06 under B, so its unique .95 quantile is 1 under A and 2 under B. Marginal information can still support conservative bounds; this example shows that it does not identify the exact peak quantile. The specified toy laws are not source observations, a fitted mechanism or a new experiment.

## Path-extreme precedents and measurement

Financial risk measured before a terminal date is an established problem. The following works are already cited in the manuscript; they are not new fitted peak benchmarks.

| Consulted source | Financial response and mature construction | Transfer boundary |
|---|---|---|
| [Boudoukh et al., MaxVaR, author manuscript](https://pages.stern.nyu.edu/~rwhitela/papers/maxvar.pdf), Sections 2–3 | A quantile of the worst loss relative to initial portfolio value, with a first-passage calculation under a lognormal diffusion and a separate discrete-monitoring illustration | This is not running-high drawdown or absolute signed inventory. Its model-based adjustment cannot be copied to a scalar position that can cross zero, or used to infer unobserved excursions in this record. |
| [van den Hoogen, 2017 thesis](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1), selected Chapter 5 | A maximum negative cumulative payment balance and a conditional-quantile liquidity buffer, using modeled payment times and amounts | A payment-cash deficit is a different measured object. The source's transaction and redaction boundaries remain; its cash-buffer results are not validated funding requirements for the present position scalar. |
| [Liao and Theodosopoulos, fixed 2005 version](https://arxiv.org/pdf/math/0506077v1), Sections 2–3 | Policy-dependent collateral-adjusted maximum contract exposure; Brownian/bridge calculations inform choices of marking time | Collateral updates change the response itself. The timing decision and its conditional information require a stated contract/collateral model; passive peak forecasting does not establish what a different margin or hedge policy would do. |

The generic reusable idea is to define the financial path functional before choosing its conditional model and upper-quantile report. The source-specific diffusion laws, transaction models, collateral rules and numerical findings do not transfer with that idea. A changed path functional is a substantive task change, but neither financial usefulness nor methodological novelty follows from it alone.

Monitoring also defines the target. If a finer path is assumed to exist and agrees with every recorded position, its supremum of absolute position over the same time interval is at least the recorded maximum. Without further restrictions between observations, compatible finer paths can have arbitrarily high excursions. The observations therefore determine no finite upper bound that applies to every compatible finer path. This deterministic observation neither measures missed risk nor assumes that the dataset provides a latent continuous path. The study forecasts its stated sampled target, including the source's long record gaps.

The MaxVaR author manuscript was reread across all nine text pages; this does not certify the cited external probability proof or reproduce its simulations. Liao–Theodosopoulos was revisited at selected physical pages 3–6 and 13–16 for setup, policy and information timing, without certifying its formulas or numerical optimization. The thesis row relies on previously recorded selected reading, including physical pages 75–94; its institutional link timed out on this revisit, so no fresh thesis body reading is claimed. Exact editions and cumulative scopes remain in the [source evidence map](paper-evidence-map.md).

## What can be borrowed

The useful practice is to keep information, comparator and failure cases attached to the same stated task. A direct peak or headroom regression comparator would have to be fitted to completed labels, with compatible features available at issue and the same evaluation origins and preference. A model of the future conditional envelope or path can supply a different comparator, with its own estimation and information requirements. A richer model's existence does not make its unavailable inputs observable in this aggregate record. Its theoretical or published performance also does not become an executed benchmark here.

For the current paper, mature quantile and retrieval operations remain the method components. The application contribution is their bounded comparison on the specified peak response, including adverse score, breach and severity consequences. The added nearest-state rule improves equal-count recent references but does not beat the better original full-window rule at each horizon. This note supplies no new forecast, independent dealer evaluation, population inference or stronger novelty claim. It therefore leaves the paper's limited application-comparison positioning intact.

## Reading and version boundary

The fixed Challet et al. version 3 author PDF has 33 pages and is 3,055,776 bytes, SHA-256 `29f74353084c31c3712ee93398937c673c76168605c19253f98022e067cf3ea1`. This directed rereading covers selected body in physical pages 4–17 and 20; reference routing on 18–19; selected captions on 25–28 and 30; and full-size visual checks on 13, 25, 27 and 28. It is not an all-page visual audit, code audit, reproduction or a new distinct work each time it is revisited. The PDF and source images remain private reading material; no observations or third-party graphics are redistributed. Earlier detailed research notes retain their own reading scopes.
