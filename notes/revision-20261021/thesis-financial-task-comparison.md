# Financial tasks within the closest thesis

This comparison extends the source reading behind the working paper. It concerns one doctoral thesis, not several independent papers or dealer records. Its purpose is to distinguish existing financial applications precisely, rather than establish priority by failing to find a matching phrase.

The inspected source is Wojciech Jakub Wisniewski's *Net Position and Retail Trader Behaviour: Implications for Market Makers' Risk Management Strategies*, [institutional PDF](https://pure.royalholloway.ac.uk/ws/portalfiles/portal/63018039/2024WisniewskiWJWphd.pdf). The institutional award year is 2024; the cover is dated 2023. The retained 139-page file has SHA-256 `54856d5cc7353786c05bf411eca02529b9f70734a7dba4a3af1ebc81873943ca`. In the ranges below, physical page numbers are one-based and exceed the printed page by one.

## Cases, tasks and data identities

| Inspected material | What the source studies | Relevance and boundary for this paper |
|---|---|---|
| Section 2.4, physical 29–35; Chapter 3 narrative physical 36–51 | Staging irregular agent activity into regular samples, including a January 2017 FX case with 684 clients and 30 currency symbols | Explains why data aggregation matters. This inspection does not establish that this case or its construction is the exact pipeline behind the accepted version 2 hourly CSV. |
| Chapter 5, physical 71–106 | Trader communities and expert-advice investment strategies; the chapter describes roughly 20,000 traders during 2015–2017 | A close example of mature methods applied to FX risk management. Trader-level clusters and advice are richer inputs than the single aggregate series used here. Different case labels do not establish different dealers. |
| Chapter 6, physical 107–125 | Next-step signed net-position intervals on the public aggregate-series source | The direct response/data-source lineage, including normalized and regularized forecasts. Reusing this source does not add an independent dealer record. |
| Current working paper | A single upper empirical forecast for the maximum absolute position over the issue record and the next H records | Changes the response, known floor and label-completion time. It does not introduce nearest neighbors to this source or establish a new quantile estimator. |

Chapter 5's investment construction makes traders or trader clusters into experts. Its hierarchical-clustering route uses correlations of trader net positions, while another route uses trading synchronicity. The learner chooses an investment, and the resulting wealth path is evaluated by return, Sharpe ratio, maximum drawdown and Calmar ratio. The author reports improved variants and warns that sufficiently large scaling can cause bankruptcy or cessation of investment. Those outcomes were read, not reproduced here.

The two meanings of a path extreme must remain separate. Chapter 5's maximum drawdown evaluates a portfolio's realised wealth path. Here the maximum absolute aggregate net position is the forecast response. An investment decision is also not automatically an implemented dealer hedge. No mapping from those strategies to the source dealer's actual hedge transactions or costs was established in this reading.

Section 2.4 and the bibliography identify separate trade-level and net-position-series records. A source-file hash authenticates the exact file analysed here; it does not verify its upstream trade aggregation, the historical version used in another study, timezone or live availability. This limits provenance claims without invalidating analysis of the documented public record.

## Reading scope and contribution boundary

The cumulative reading includes Chapter 3's extracted narrative through physical 51, selected later captions, Chapter 5's extracted text/captions through physical 103 and caption/image inspection of physical 104–106. Selected original pages containing the data construction, investment game, clustering inputs and drawdown definition were visually checked. Earlier reading covered Chapter 6's complete extracted text and Chapters 4/7, as recorded in the [evidence map](paper-evidence-map.md). Not every figure, external proof or bibliography item was audited, and the whole thesis is not claimed as fully verified.

In these inspected task definitions, the Chapter 5 decision study and Chapter 6 endpoint study differ from the current peak response. This is a bounded task comparison, not proof of absence elsewhere. The current contribution remains a finite-record application comparison of mature episode selection and response representations. The thesis already supplies close financial applications and path-risk evaluation; a different response alone does not demonstrate important innovation, external validity or economic benefit.
