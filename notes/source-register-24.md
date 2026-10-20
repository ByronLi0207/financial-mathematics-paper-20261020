# Source register24 — financial density calibration and volatility-adjusted scenarios

**Selected primary-source reading, 20 October 2026.** This register consolidates completed selected primary-source reading. It reports no project empirical result or selected research design. Administrative curation adds no original-body reading credit.

## 1. Multivariate forecast evaluation and historical PIT calibration

**Francis X. Diebold, Jinyong Hahn and Anthony S. Tay (1999), “Multivariate Density Forecast Evaluation and Calibration in Financial Risk Management: High-Frequency Returns on Foreign Exchange.” Review of Economics and Statistics81(4),661–673, November1999.** [Formal DOI](https://doi.org/10.1162/003465399558526).

Actual primary edition: [NYU FIN-98-079 author draft](https://archive.nyu.edu/bitstream/2451/27077/2/wpa98079.pdf), **26 August 1998**, titled **“Real-Time Multivariate Density Forecast Evaluation and Calibration: Monitoring the Risk of High-Frequency Returns on Foreign Exchange.”** The42-page image-only file was read visually. Its title/date are not substituted for the formal1999 reference, whose body was not read or compared.

**Source synthesis — 148 words.**

<!-- SYNTHESIS_1_START -->
Diebold, Hahn and Tay use ordered conditional transforms to evaluate joint forecasts. Under correct conditional densities and regularity, the transformed components have the specified independent uniform law; marginal diagnostics alone omit dependence structure. Historical recalibration instead needs stable iid PITs with a potentially nonuniform distribution. Correct location-scale dynamics with iid innovations provide one sufficient example, while estimating the correction need not improve finite-sample forecasts. The draft applies these ideas to half-hour indicative currency quotes. Decay selection and calibration precede evaluation, although full preprocessing availability remains unverified for live use. Different variable orders are diagnostic views of shared observations, not independent replications. Recursive monitoring is a future direction without a specified alarm guarantee. Selected 1998 visual body passages were read; the formal edition, full figures, external estimation proofs, original observations and current permissions remain unverified. The empirical exercise concerns spot-quote forecasts rather than pricing-measure calibration or executable trading profits.
<!-- SYNTHESIS_1_END -->

## 2. Preference-based adjustment of option-implied densities

**Robert R. Bliss and Nikolaos Panigirtzoglou (2004), “Option-Implied Risk Aversion Estimates.” The Journal of Finance59(1),407–446, February2004.** [Formal DOI](https://doi.org/10.1111/j.1540-6261.2004.00637.x). A later digital-publication metadata field is not used as the print issue year.

Actual primary edition: [Chicago WP2001-15r3 in the official FRASER archive](https://fraser.stlouisfed.org/files/docs/historical/frbchi/workingpapers/frbchi_workingpaper_2001-15r3.pdf). Cover: **Revised March2003**. Inner title: **26 February2003**; first draft **2 November2001**. The earlier title was *Recovering Risk Aversion from Options*. This61-page revision is not certified equivalent to the unread2004 typesetting.

**Source synthesis — 142 words.**

<!-- SYNTHESIS_2_START -->
Bliss and Panigirtzoglou adjust option-implied risk-neutral densities using stationary parametric utility and representative-agent restrictions. The physical distribution is not identified by option prices alone. Their risk-aversion parameter maximizes an in-sample Berkowitz diagnostic p-value; Monte Carlo calibration repeats that fitting operation because selection changes its reference distribution. Pair bootstrap and leave-one-out exercises assess variability and influence rather than chronological holdout forecasting. Contract settlement, option filtering, smile smoothing and extrapolation are substantive inputs. The application uses S&P500 futures options and FTSE100 options across several horizons, with shared expiries and overlap affecting dependence. Gaussian likelihood diagnostics examine selected restrictions, and nonrejection does not certify full conditional correctness or economic superiority. Selected 2003 working-paper methods, application and test descriptions were read. The final journal edition, external equilibrium/extraction arguments, executable implementation and current option/rate-data rights remain unverified. Reported simulations do not establish distribution-free finite-sample or anytime validity.
<!-- SYNTHESIS_2_END -->

## 3. Volatility updating of historical scenarios

**John Hull and Alan White (1998), “Incorporating volatility updating into the historical simulation method for value-at-risk.” Journal of Risk1(1),5–19, Fall1998.** [Formal DOI](https://doi.org/10.21314/jor.1998.001); [publisher record](https://www.risk.net/journal-of-risk/2161156/incorporating-volatility-updating-into-the-historical-simulation-method-for-value-at-risk). DOI metadata records September1998.

Actual primary body: the [public author-uploaded full-text page](https://www.researchgate.net/publication/2645882_Incorporating_volatility_updating_into_the_historical_simulation_method_for_VaR), marked as uploaded by John Hull on **28 March2014**. The manuscript says **first draftMarch1998; this versionOctober1998**. Platform/upload dates are not manuscript revisions or substitutes for the formal citation. No source PDF was obtained; retained reader excerpts are identified separately below.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_3_START -->
Hull and White standardize historical changes by previously forecast volatility and rescale them using the current forecast. Their premise is stationarity of standardized changes, not a proof of iid shocks or distribution-free conditional coverage. The demonstration uses a 500-day history and EWMA volatility, distinguishing rescaled observations from age-weighted historical sampling and separate mean adjustment. Twelve currencies and five equity indices supply tail-frequency, clustering and capital comparisons. The multi-day exercise scales daily VaR and evaluates subsequent losses; it does not recursively generate an entire future volatility path. Reported capital findings are stronger for currencies, with mixed longer-horizon equity results. Overlapping-window diagnostics have stated inferential limits. Selected October 1998 author-body passages were read through a public reader view. Retained fingerprints concern excerpt snapshots, not a source PDF or complete HTML. Full results, external theory, initialization, executable reproduction, original observations and current data/article reuse rights remain unverified.
<!-- SYNTHESIS_3_END -->

## Actual editions and root selected reading

Selected ranges do not certify every line, numerical cell, figure or outside proof. Auxiliary reading does not enlarge root scope or time.

| Source | Actual retained evidence | Root selected scope | Remaining boundary |
|---|---|---|---|
| Diebold–Hahn–Tay |42-page image-only NYU draft; titlePDF5; main printed page = PDF page − 5 after title/blanks |Direct visual selected readingPDF5,7–27,28(first reference page), using existing rendered pages |Full graph/table pages29–42, final1999 body, other editions and external proofs unread; rendering itself is not counted as reading |
| Bliss–Panigirtzoglou |61-page Chicago revision; main printed page = PDF page − 2 throughPDF35 |Text-layer selected readingPDF1–29,33–35,39–43,48;9–10 and26 revisited; visual checks5,9–10,17–20,22–23,48 |Mapping snippets30–32/36–38 are not body reading; AppendixB44–46 and full remaining tables/plots unreviewed; external proofs not independently verified |
| Hull–White |Author-body reader view with manuscript-page markers; no original PDF or complete HTML retained |Reader lines50–916, manuscriptpp2–10 plus version evidence;84–210 and701–916 explicitly revisited after truncation |References, full tables/figures and external theory unaudited; no source-PDF page count, original-PDF visual check or typeset equivalence claimed |

The Hull–White evidence is selected actual author-body text, not abstract-only reading. Its snapshot fingerprints preserve the accessible excerpts without representing them as original-file hashes.

## Original crosswalk of objects and timing

| Distinction | Boundary retained |
|---|---|
| Economic adjustment versus statistical calibration | Utility restrictions linking pricing densities to subjective forecasts differ from estimating a stable PIT correction distribution. Neither bridge follows from an option price or diagnostic nonrejection alone. |
| Forecast issuance versus outcome transformation | A joint forecast is issued before outcomes; within-date conditional PITs can use realized earlier components only when settling that forecast. |
| Earlier calibration versus complete live availability | Prior fitting/evaluation segments do not automatically settle availability of interpolation, seasonal preprocessing or every constructed input. |
| Retrospective fitting versus chronological holdout | Repeating parameter fitting inside null simulation addresses that stated selection operation; leave-one-out influence checks do not create a forward evaluation period. |
| Scenario distribution versus future path law | Rescaling historical daily shocks and scaling a daily percentile differ from recursively simulating future states and path functionals. |
| Diagnostic evidence versus guarantee | Marginal/serial checks, simulated reference distributions and economic capital comparisons answer different questions; none automatically gives full conditional or arbitrary-stopping validity. |

The recorded financial applications and extensions are existing source work. No new method, financial series, experiment or empirical finding is selected here.

## Data, materials and rights

Diebold–Hahn–Tay uses1996Olsen indicative DM/dollar and yen/dollar quotes. The draft describes an estimation segment ending30June1996,21:00GMT and evaluation beginning21:30GMT. Article educational/research reproduction conditions do not license the quote observations. Current data access, vintage and replication materials remain unverified.

Bliss–Panigirtzoglou's options, contract-specific settlements and BBA/Bloomberg rate inputs are historical study materials. Present access, processed versions, executable programs and redistribution rights were not verified. Article hosting does not supply those rights.

Hull–White's market-variable histories cover currencies during1988–1997 and equity indices during1988–1998. Original provider/vintage, complete input specifications, programs and present reuse rights remain unverified. The author-upload page does not establish an open article/data licence. Historical capital conventions are attributed to this source, not asserted as current regulation.

No original article, observations, source program or substantial third-party passage is delivered. Existing failed access routes were not retried during administrative preparation.

## De-duplication and retained fingerprints

Registers01–23 were checked by author/title terms and identifiers; none of these three sources was already a principal entry. The update uses completed root94–96 records only, without a new paper search or body reading.

All four retained files below were rehashed and matched their recorded fingerprints. Two are original PDFs and two are derived reader snapshots. A snapshot identifies captured text, not an unavailable original PDF or complete page response. Fingerprints do not certify unread version equivalence or replication.

| Evidence type and edition | Bytes | SHA-256 |
|---|---:|---|
| Original PDF: Diebold–Hahn–Tay, NYU1998 draft |1165172|`1bf974c62504cec9f0288d80ffb29ba0dc6ddb92d5ed3d4d2a01dc3c44396780`|
| Original PDF: Bliss–Panigirtzoglou, Chicago2003 revision |488331|`478a76b090c033c74eb7438eee9dc7c96e871aabd621df0039d33e84a9f55d94`|
| Derived Hull–White reader snapshot: author-body excerpt |29143|`e4aa21439a8ec0cbf484e20b76f2cff3130601228f7bfa44da533cbc08be8722`|
| Derived Hull–White reader snapshot: capital excerpt |20987|`da066d0eee65b63de230a262974acbfe7c7b676f2036c2205947ec05fe34f3f4`|
