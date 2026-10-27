# Common manuscript sources for submission-final

This directory preserves the v13 scientific manuscript as the common source for the final submission packages, with only the audited saved CFTC history-length extension imported from final-jof. It is not a separate scientific revision or an additional journal submission.

Use the primary [ASMBI submission package](../submission-package/ASMBI/README.md) and the shared [upload manifest](../submission-package/MANIFEST.md). [Quantitative Finance](../submission-package/QF/README.md) is the first alternative format of the same study. The canonical title and three findings remain those of v13; the alternative final-jof title and abstract are not adopted.

- `manuscript.tex`, `supplement.tex`, `references.bib`, `figures/` and `generated/` supply the common scientific text and displays.
- Publisher-specific cover letters, title pages, reference styles and compiled PDFs are in `submission-package/`. Those files identify the actual upload columns in the manifest.
- `notes/submission/import-audit.md` binds every imported result to the fixed source commit, file SHA and saved JSON/CSV location.
- `notes/submission/journal-shortlist.md` records the official MJL SCIE checks and current publisher requirements. Quartiles remain for the author to verify through the university.
- `notes/submission/prediction-register.json` records all prewritten screens, including unsupported and untestable outcomes. It does not relabel locally committed designs as externally registered studies.
- `REPRODUCING.md` at the repository root separates document rebuilding, aggregate inspection and raw-input financial replay.

No new experiment or financial fit is performed in this submission round. Original archived results and failures remain unchanged. Author identity, affiliations, ORCID, funding, interests, CRediT roles and source permissions require author completion. No journal submission, account registration, reviewer contact, PR change or repository-visibility change is performed.
