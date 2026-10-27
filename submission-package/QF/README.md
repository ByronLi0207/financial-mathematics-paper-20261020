# Quantitative Finance alternative package

Generated from the current canonical `submission-final/`; the canonical sources are read-only inputs.
This is the regular Research Article alternative. QF uses single-blind review; author fields remain placeholders.

## Files

- `main.tex` / `manuscript.tex` / `main.pdf`: official rQUF2e single-column manuscript with embedded existing tables and vector figures.
- `supplement.tex` / `supplement.pdf`: unchanged canonical supplement content and its local dependencies.
- `title-page.tex` / `title-page.pdf`: canonical author-information template plus the actual frozen narrative word count, current canonical keywords, and CRediT/JEL placeholders; capped at one page.
- `cover-letter.tex` / `cover-letter.pdf`: three substantive paragraphs for QF, scope quotation and GitHub-preprint disclosure.
- `references.bib`, `rQUF.bst`, `main.bbl`: source bibliography, unchanged publisher bibliography style and the actual cited reference list.
- `rQUF2e.cls`: unchanged publisher class. The author-side preamble replaces the class's fictional publication header with a submission-draft header. Its cached `geometry` setup preserves letter paper, resets the class's inherited horizontal/vertical offsets to zero, sets left/right margins to 22 mm and top/bottom margins to 24 mm including headers/footers, and sets header height/separation to 14/15 pt and footer separation to 20 pt. This corrects the old class's 4 pt footer collision under the restored modern output routine. The resulting body width is larger than the canonical 160 mm body width; scientific figures are unchanged.
- `epsfig.sty` and `rotating.sty`: unchanged support files from the same official ZIP. `qf-compat.tex` retains the installed LaTeX kernel's document entry points, replacing the class's incompatible 2014 copies; publisher typography remains, with the explicit author-side page geometry described above. It skips the unused extended-enumeration interface, unavailable in both the ZIP and local cache; standard lists remain, and the builder rejects extended enumerate syntax.
- `qf-fonts.tex`: scalable cached Latin Modern OpenType text faces, with standard math left in Computer Modern. Small caps use the regular face and bold italic uses explicit emboldening of the italic face; this avoids unavailable cache fonts without downloading. Only font setup is added to the supplement/title-page preambles; their bodies stay unchanged.
- `source-manifest.json` and `source-package.zip`: complete transitive local source closure; backups and compiler logs are excluded.
- `BUILD-RECEIPT.json`: actual input/output hashes, commands, page counts and source-ZIP compilation checks.

## Rebuild

Use the existing environment from the repository root:

```sh
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pypdf python -B notes/submission/build_qf_package.py
```

The builder reads the current canonical files on each run and backs up changed, untracked outputs before replacement. It never changes canonical science, results or figures. It compiles with cached Tectonic only, and writes logs below `.scratch/submission/qf/`.
Changed PDF outputs and build receipts are backed up even if tracked. Rejected pre-geometry and inherited-offset trial cuts are retained below `failed-cuts/` with explicit `FAIL_VISUAL_*_SUPERSEDED` receipts; their old success claims apply only to source compilation and are explicitly superseded for visual use. No failed PDF is deleted.

## Editorial checks and remaining author actions

The abstract is unchanged (175 source words); there are 6 unchanged keywords. The title page reports the actual canonical narrative count (4122 words), read from the shared frozen `notes/submission/writing_metrics.py` definition, together with its exclusions and the canonical keywords. Main, title-page and cover-letter page caps are checked automatically. Citation groups are ordered by the inherited bibliography years without changing their membership. Only cited references are printed; historical uncited database entries remain in the database. An explicit canonical `(n.d.)` label is supplied as a packaging-only BibTeX date where the database omitted its date.
Existing institution fields are mapped to school/howpublished where the publisher style requires them, and existing URL/DOI values are repeated in notes so the old style does not silently omit access routes. No bibliographic fact is acquired or invented. Original missing publication addresses, if any, remain warnings in the receipt.
The derived Wisniewski2020 booktitle omits only its existing literal `Proceedings of the ` prefix, which the unchanged publisher bibliography style adds automatically. Only the exact `Data availability.`, `Code availability.` and `A fixed CFTC history-length extension.` paragraph labels lose their trailing source full stops, because the unchanged class adds those stops. The scientific-body equivalence check permits exactly these three label-punctuation conversions and citation-group ordering; it performs no general punctuation normalization.

Final full-page visual QA is assigned to the root task and is not asserted by this builder. Complete author names, affiliations, corresponding contact, ORCID, funding, competing interests and CRediT roles before any actual submission. The official template requests a JEL classification; its choice remains the author's decision, with a placeholder rather than an invented code. The actual narrative count and keywords update automatically on each build. The author must separately resolve applicable disclosure requirements against the policy record; this package contains no AI declaration. No claim of permission to redistribute restricted inputs, acceptance, fee payment or completed submission is made.
