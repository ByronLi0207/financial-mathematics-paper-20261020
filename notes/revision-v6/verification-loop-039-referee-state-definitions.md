# Verification loop 039 — State definitions and working-reference meanings

- Reviewer: one same-model internal textual/static check; not external validation or two independent referee reviews.
- Assignment: read the single S16 “Issue-known position-change states” subsection through, but not including, target-level refits; compare the non-table definitions with current `v6_states.py` and its frozen current protocol only.
- First version/hash readback: **2026-10-23T22:31:26Z**.
- Last readback/note timestamp: **2026-10-23T22:32:38Z**.
- Branch: `revision-v4-jof`.
- Initial HEAD: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`; HEAD at note write: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`.
- The root goal remains active through 2026-10-24T00:31:50Z; this note does not mark that goal complete.

## Verdict

No new scientific or conclusion-changing definition issue was found within the bounded text-to-static-contract check. The current paragraph distinguishes training-frozen position-increment RMS states, full-axis group-HAC inference, equal-group-mean heterogeneity and a separate H-burn-in finite-instrument GW-style joint null. It does not interpret joint rejection as a state effect or switching-policy gain. The stated maturity, scaling and failure boundaries agree with the current static module and protocol, subject to the explicit caller-provenance limits below.

This is an internal consistency finding, not fresh covariance/test reproduction, financial-statistic validation, proof of conditional predictive ability or authentication of private input vectors.

## Exact read scope

- Current `submission-jof/supplement-content.json`, Section index 15 (`S16. Additional benchmarks and robustness`), bounded interval **blocks[26:31]**.
- The interval has exactly **one non-table paragraph**, block 26, “Issue-known position-change states”. Read its full prose and every inline-math mapping.
- Blocks 27–30 are Tables S58–S61. Their captions were read to establish scope and the declared reference meanings; no numerical table cells were reviewed or recalculated.
- Stop boundary: block 31, “Refitted target-level sensitivity”. Its heading located the endpoint; its following method content was not audited here.
- Read the corresponding current Supplement TeX paragraph in full at **line 2524**; target-level subsection begins at line 2582.
- Read `v6_states.py` **lines 1–230** (the entire current static module) and `protocol/revision-v6/wp4-state-gw.md` **lines 1–13** (the entire current protocol). No imported covariance/probability implementation or caller execution was opened or run as part of this check.
- Main JSON/article TeX/PDF and Supplement PDF were fingerprinted only; no PDF page rendering, compiler run or visual-layout verification is claimed.
- No earlier loop verdict or earlier numerical result served as proof.

## Definition checks

| Topic | Current static/protocol anchor | Finding and practical limit |
|---|---|---|
| Fixed original comparison identity | Protocol line 3; module lines 1–6 and 109–129 | The protocol specifies exactly FX H6 QR W2880 minus original rolling F W720 and Treasury H6 QR W260 minus original frozen F W260. The prose says new-minus-original-reference and does not substitute a favorable matched reference. The generic module receives an already admitted difference vector; it cannot independently authenticate report identities. No actual loss or forecast vector was reopened here. |
| State information and interpretation | Protocol line 5; module lines 42–61, 125–140 | State is past-only short **position-increment RMS**, not price/yield volatility. The protocol uses the original feature's 24-record FX / 6-record Treasury lookback. The module's optional synthetic helper is explicitly past-only, and its finance caller contract retains original RMS. This static read does not prove actual supplied feature provenance or economic public-release availability. |
| Exact initial mature training pool | Module lines 118–124; protocol lines 5 and 9 | Input origin and training axes must be contiguous. The final training origin must be first evaluation issue minus H, so that final training label completes at the initial evaluation issue. The module rejects a mismatched terminal boundary. The caller supplies the QR pool's earlier boundary and actual response scale; the generic module does not reconstruct or independently authenticate those values. |
| Training-only linear terciles | Module lines 132–140; protocol line 5 | Both empirical cut points come from training RMS only using the declared linear 1/3 and 2/3 quantiles. Evaluation groups apply the same frozen cut points: low <= cut1, middle <= cut2 after excluding low, otherwise high. No evaluation refitting of thresholds or threshold movement to fill empty groups occurs in this module. |
| Ties and empty groups | Module lines 140–158, 176–177; protocol lines 5 and 7 | Equal/collapsed cut points can leave a group empty. Empty group rows preserve count zero with no mean or SE, and the heterogeneity reference becomes NA/EMPTY_GROUP. No regrouping or threshold rescue is performed. This matches the prose's tie qualification. |
| Full-axis group influence | Module lines 141–161; protocol line 7 | The influence matrix is allocated over all n original evaluation rows and starts at zero. Within group g its column is (d_t - mu_g)/(n_g/n); other dates stay zero. HAC receives that full matrix, with the full-n bandwidth. Nonconsecutive group dates are not compressed or joined as adjacent dates. |
| Group SE sample size | Module lines 159–171; protocol line 7 | The reported group SE uses the corresponding full-axis HAC diagonal divided by **full n**, matching the displayed formula. Descriptive group means use their own members. A zero diagonal can retain SE=0 with explicit `ZERO_LONG_RUN_VARIANCE`; that descriptive status does not create an eligible positive-covariance Wald reference. No SE was recomputed in this loop. |
| Group heterogeneity null | Module lines 14–16, 172–177; protocol lines 7 and 11 | The two fixed restrictions compare low-minus-middle and low-minus-high group means. The reference uses their projected full-axis covariance and df=2. It tests equality of group means; it is not the same as zero joint finite-instrument moments. Empty/singular/failed references remain NA. |
| Issue-known delayed instrument | Module lines 185–198; protocol line 9 | The three fixed instruments are intercept, d_(t-H)/a0 and current issue-known RMS_t/v0. With a contiguous source-record issue axis, d_(t-H)'s H-step target finishes at t. The module aligns d[:-H] with current suffix d[H:] and RMS[H:], rather than using an unfinished recent loss or wrapping pre-evaluation lags. Equality at maturity follows the recorded issue-clock convention, not reconstructed publication vintages. |
| H-row burn-in and scope | Module lines 185–198, 213–229; protocol line 9 | GW alone uses the suffix after H evaluation rows, reporting full_n, suffix n and requested/actual burn-in. Too-short suffixes retain NA. Group means, group influence and heterogeneity were built earlier on the full original axis. The text and S61 caption correctly keep these sample scopes distinct. |
| Frozen normalizers | Module lines 122–124, 132–139, 196–198; protocol line 9 | a0 is required positive and finite and is contractually the initial mature QR response scale. v0 is the training-only short-RMS mean floored at 1e-12; evaluation RMS does not fit that normalizer. Both lagged and current d use the same a0. The module's validation of a0's positivity is not independent proof of its training-only provenance. |
| GW moment and intercept meaning | Module lines 191–212, 221; protocol lines 9–11 | Moments are the fixed three-vector instrument multiplied by current d_t/a0 on the H-burn-in suffix. The intercept permits joint rejection from an unconditional mean difference alone. The prose expressly says rejection need not establish a state effect or switching policy; it does not claim a full conditional-null theorem. |
| Failure and no rescue | Module lines 64–106, 199–212; protocol lines 9–11 | The fixed reference requires finite moments/covariance, full required covariance rank, positive eigenvalues, condition <=1e12, finite nonnegative Wald value and valid reference probability. The GW instrument matrix must retain rank 3. Failed decompositions, singular/ill-conditioned/nonpositive references, deficient instruments and too-short samples retain missing statistics/p-values with explicit status. No instrument is dropped and no pseudoinverse rescues a failed reference. |
| Working assumptions / limits | Protocol lines 3, 9–13; module line 221; current paragraph and S60 caption | The current protocol and module explicitly retain exploratory working-reference status and unvalidated limited-memory, moment, mixing and long-run covariance assumptions. The bounded subsection distinguishes nulls and effects; its caption calls the four slots working-reference tests. No causal state effect, extra state-conditioned fit, switching backtest, independent validation or success claim follows from this reading. |

## Necessary issues and optional wording

- Necessary scientific/conclusion issue: **none found in this bounded static reading**. No scientific author-pending correction is created.
- Optional phrase only: “the separate finite-instrument GW-style test” could say “the separate finite-instrument GW-style working-reference diagnostic” so the paragraph carries that qualification locally as well as the current protocol, module note and table caption. This would not change the stated null or any result. No edit was made.
- No missing/failed test was converted to an observed p-value, and no actual group covariance, heterogeneity statistic, GW statistic, financial mean or source data was calculated.

## Explicit provenance and access limits

`v6_states.py` is a pure input-accepting module. Its documented caller admits the original report identities, original past-only RMS, full original issue vector, exact first QR mature pool and its response scale. The static checks enforce many shapes, boundary and finite-value conditions, but this loop did not inspect private arrays or trace the caller's actual admitted financial inputs. Accordingly the verdict concerns the text and declared algorithm/contract, not a fresh empirical certification of original-vs-matched identity or no-lookahead provenance.

No covariance/test/proof/statistical execution or new analysis, raw/private vector access, models, test suite, network/external source lookup, UI, Claude/Cloud/cross-model review, nested delegation, source/manuscript/result/protocol/state/ledger edit, commit, push, deletion or installation occurred. Only this authorized note path was written.

## Current byte fingerprints

| File | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `submission-jof/supplement.tex` | `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8` |
| `submission-jof/supplement-preview.pdf` | `7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991` |
| `v6_states.py` | `1c50807a3bd85906d9fcef971c9efa6e3784a712008635971e7b6ce1f9252d64` |
| `protocol/revision-v6/wp4-state-gw.md` | `e8a832e4a6c5cb17ac79d931d83a19836e597dcef713b4e5d26bc7cacb9b9259` |
