# Verification loop22 — publisher-deposited/official bibliographic metadata

Checked 2026-10-23T22:05:06.076276+00:00. Seed2026102322 fixed three references before lookup (selection JSON retained). Current main JSON SHA-256 `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`. No reference, manuscript, source, empirical result or conclusion was changed. This is metadata checking, not a claim of fresh full-text reading or methodological validation.

| Entry | Actually used primary metadata | Match |
| --- | --- | --- |
| Hull–White1998 | [Publisher-deposited Crossref DOI record](https://api.crossref.org/works/10.21314%2Fjor.1998.001) | John Hull/Alan White; exact title; journal1(1),5–19; registered publicationSeptember1998; DOI10.21314/jor.1998.001. Current citation matches. Direct DOI webpage inaccessible through the text tool, so no direct body access claimed. |
| Wisniewski–Lindsay–Lindsay2020 | [Official PMLR record](https://proceedings.mlr.press/v128/wisniewski20a.html), authors/title/venue/volume/pages/year and BibTeX | Wojciech Wisniewski/David Lindsay/Sian Lindsay; title and ninth symposium metadata agree; PMLR128,285–301,2020. Capitalization/typographic apostrophe differences do not change identity. No original endpoint theorem or full paper was newly read. |
| Biau–Patra2011 | [IEEE-deposited Crossref DOI record](https://api.crossref.org/works/10.1109%2FTIT.2011.2104610) | Gérard Biau/Benoît Patra; exact title; IEEE Transactions on Information Theory57(3),1664–1674; registered printMarch2011. DOI case normalization agrees. Current citation matches; direct IEEE/DOI access was blocked/inaccessible. |

For the two DOI entries a bounded unauthenticated urllib request read their official registration-service responses, then printed only title/authors/container/volume/issue/pages/date/publisher/DOI/URL. Each request had15-second timeout and1,000,001-byte maximum read. The observations above are the publisher-deposited bibliographic fields, not a snapshot of an article body or a guarantee that every other field in a live record is correct.

Primary-source filtering matters: the initial risk.net search returned other articles' bibliographies rather than the target record; broad search also showed a third-party1999 date for Hull–White and2017 date for Biau–Patra. Those were excluded from the verdict. The accepted1998/2011 dates come from the actual corresponding DOI registration records, and the PMLR metadata from its own proceedings page. No paid delivery, authentication bypass, installation, journal account, data/model run or source-PDF redistribution occurred.

Three metadata matches; direct-body access limits explicit. No new method comparison, novelty claim, ACI/SPCI guarantee or independent replication follows from these checks. Only this note and the preselected-ID JSON were written for this round.
