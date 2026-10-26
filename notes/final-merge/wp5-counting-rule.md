# WP5 fixed counting rule

Established before the first WP5 manuscript edit at 2026-10-26T04:32:54.645817+00:00.

Auditor SHA-256: `47f7bd1b61d08eac0ef7fd6ccc82aced9bb6e5a7cd74818937b3af246d975794`.

Primary scope is the abstract and scholarly main text through the conclusion, including figure captions and explanatory table notes. Tabular cells, headings, displayed mathematical identities, bibliography, URLs and reference/citation identifiers are excluded; these receive separate source-field checks. Inline mathematical numerical literals and spelled numerals remain in the numeric-density count, including hyphenated number words. Author and availability material is reported separately. Sentence boundaries use terminal punctuation or actual paragraph endings, with decimal points retained. Words use the exact regular expression in the auditor. Formatting widths and TeX control values are excluded. The complete baseline sentence list is saved.

Grammatical negative sentences contain an explicit negation operator from the saved list, including not/no/neither/nor/never/cannot/without and common negative contractions. A broader adverse-or-uncertainty lexicon is reported separately; favorable wording is never substituted for an adverse scientific outcome.

Banned terms are scanned case-insensitively over all pre-bibliography TeX text, including table cells, with plural/hyphen/space forms recognized. The explicit abstract gate is exactly five sentences and no more than170 words. The other gates are mean18–24 words, at most2 numerical values per sentence, grammatical-negation sentences at most8 percent, and zero banned phrases.

Initial extraction artefacts (formatting widths, headings and interrupted display formulae) were corrected before this rule was frozen and before source edits; only the corrected baseline is used for the before/after comparison. No forecast computation is part of this audit.
