# Verification loop26 — three selected journal records and consulted preprint version

Checked 2026-10-23T22:13:42.843890+00:00; seed2026102326 fixed selection before lookup. Current main JSON SHA-256 `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`. This is a bibliographic metadata audit, not full-paper reading, a new analysis or a methodological/novelty certificate.

| Reference | Primary registration or version record actually read | Assessment |
| --- | --- | --- |
| Hansch/Naik/Viswanathan1998 | [Wiley-deposited DOI metadata](https://api.crossref.org/works/10.1111%2F0022-1082.00067) | Authors/title and Journal of Finance53(5),1623–1656 agree. Registered print date is October1998; a later online date17December2002 is distinct and does not change the printed-edition citation year. |
| Ehm/Gneiting/Jordan/Krüger2016 | [Journal DOI registration](https://api.crossref.org/works/10.1111%2Frssb.12154), plus [exact arXiv v2 record](https://arxiv.org/abs/1503.08195v2) | Four authors/title and journal78(3),505–562 agree;2016 journal year is distinct from the consulted author-preprint v2 of17April2015. The exact v2 record was opened and its history read. Current citation explicitly distinguishes those editions. |
| McNeil/Frey2000 | [Elsevier-deposited DOI metadata](https://api.crossref.org/works/10.1016%2FS0927-5398%2800%2900012-8) | Authors/title, Journal of Empirical Finance7(3–4),271–300,November2000 and DOI agree. DOI letter-case normalization is not a mismatch. |

The three selected registration responses were fetched without credentials/cookies with15-second per-request timeout and1,000,001-byte maximum read, using the standard library. The public companion JSON records only selected bibliographic fields, source URL and actual timestamp; it excludes abstracts, contact data, financial observations and paper-body content. Its SHA-256 is `8d0573fad78b5625e4bb9663fdee97c25c940953f5156132fc9d45541ecf601c`.

Direct DOI article pages for the first two were inaccessible through the text reader; the McNeil–Frey DOI body returned403. No body-access success is claimed or authentication bypass attempted. Registration metadata supplies the limited publication-field checks; the arXiv page independently identifies the consulted preprint version and authors. Its abstract was incidentally returned but no new paper-method verdict is drawn from it. The current publisher-registration field is not used to rewrite the original article's historical publisher or consulted edition.

Three citation metadata matches within the stated scope; no citation, manuscript, result or conclusion was edited. No full source PDF was downloaded/re-published, no model/test/financial analysis was run, and no existing file was removed. No current or inherited guarantee is inferred for the paper's finite adaptations from these metadata checks.
