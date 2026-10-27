# Verification loop 18 — three further exact-source metadata checks

Checked 2026-10-23T21:47:13.765374+00:00; current main JSON SHA-256 `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2`. Seed2026102318 selected three main-bibliography entries before lookup, excluding previously checked IDs. This round checks metadata, not full-text methods, guarantees or novelty, and performs no financial experiment or document edit.

| ID | Original source and actual read scope | Assessment |
| --- | --- | --- |
| liao2005 | [Exact arXiv v1 record](https://arxiv.org/abs/math/0506077v1), title/authors/submission-history fields | Authors Jiali Liao and Ted Theodosopoulos; exact title matches; v1 submitted4June2005,01:36:33UTC. Current citation uses that version and date, not a later journal publication claim. Metadata PASS. No new full-paper reading or proof verification. |
| dataset | [Kaggle official record](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset) text rendering was empty; bounded unauthenticated [official metadata API search](https://www.kaggle.com/api/v1/datasets/list?search=net-position-time-series-dataset), exact ref entry only | David Lindsay, matching title/ref, currentVersionNumber2, lastUpdated2020-07-20. This supports the cited source/year/version, not the publisher's first-upload date or raw-member accuracy. Source license metadata reserves original authors' rights; no redistribution permission is inferred. No data ZIP, CSV, credentials or account interaction used. Metadata PASS. |
| xu2023 | [Official PMLR article record](https://proceedings.mlr.press/v202/xu23r.html), author/title/volume/pages/year and BibTeX metadata | Chen Xu and Yao Xie; exact title matches; ICML2023/PMLR202/38707–38727. Current metadata agrees. Only the abstract/metadata page was available/read in this round; no new full-paper reading or transfer of a conditional-coverage guarantee. |

## Actual metadata-only request

The Python urllib request to the public Kaggle metadata API used no credentials/cookies, a15-second timeout and at most1,000,001 response bytes. It returned HTTP200, application/json,58603bytes; selected exactly `ref == davidlindsay1979/net-position-time-series-dataset`. The selected record fields were creatorName/ownerName DavidLindsay, currentVersionNumber2, isPrivate false, and lastUpdated2020-07-20T12:21:30.54Z. The source licenseName was `Data files © Original Authors`. A public listing does not establish dataset redistribution rights, and this metadata response does not bind the accepted CSV member; the historical source-byte fingerprint remains a separate gate. No fetched values were used for financial calculations.

An accompanying broad text search returned unrelated datasets; none supported this verdict. The empty Kaggle HTML was not reported as a successful full-page or download check. The primary API response supplies the matching fields instead.

All three entries match within the explicit scopes above. No reference, numeric result, primary, manuscript or conclusion was changed. Existing SPCI nonexecution and finite ACI adaptation limits remain unchanged. No installs, tests, models, financial workers, raw downloads, cleanup, Claude/Cloud or external review occurred. Only this note and its preselected-ID JSON were written for this round.
