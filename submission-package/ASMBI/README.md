# ASMBI submission package

Final external acceptance: PASS — see `notes/submission/final-visual-coverage.json` and `h8-visual-asmbi-final.json`.

Builder-stage status (recorded before external visual review): COMPILED_PENDING_VISUAL_QA

Rebuild from current canonical sources with `python3 notes/submission/build_asmbi_package.py`.
Actual PDF route: ASMBI_OFFICIAL_FREE_FORMAT_INITIAL_SUBMISSION.

The official Wiley NJDv5 class and bibliography style files are unmodified; `WileyNJD-AMA.bst` is a case-portable byte-identical alias. Uncompiled original/compatible NJD sources and failure logs are audit records in `.scratch/submission/asmbi/`; they are excluded from the actual upload ZIP. NJDv5 could not compile with offline dependencies, so actual PDFs must not be described as unmodified NJD typesetting.

Standalone compile targets: `manuscript.tex`, `supplement.tex`, `title-page.tex`, `cover-letter.tex`; use `tectonic -X compile -C <target>` in this directory.

- The builder certifies source closure and compilation only. External final visual acceptance covers all 82 current ASMBI PDF pages and is bound to the exact hashes in the final reports.
- Author, affiliation, contact, ORCID, funding, competing interests, CRediT and permissions remain author-verification placeholders.
- Independent vector PDFs and 1000-dpi TIFF exports are present in figures-upload/. The font and grayscale preflight is recorded in notes/submission/figure-preflight.json; final page checks retain the actual full displays.
- Supplement long tables retain native S-section positions; main-article tables alone are moved after references.
- Actual PDFs use the journal-permitted Free Format initial-submission route with official Wiley AMA BST. NJDv5 original/compatible sources are retained; NJDv5 PDF did not compile because required packages are not cached.

- manuscript.pdf: 26 pages; COMPILED
- supplement.pdf: 54 pages; COMPILED
- title-page.pdf: 1 pages; COMPILED
- cover-letter.pdf: 1 pages; COMPILED
