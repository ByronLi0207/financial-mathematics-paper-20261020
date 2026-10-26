# C3 frozen writing measurement

The original PR3 pure statistic functions and the v8 unified-TeX adapter are
copied byte-for-byte into `writing_check.py`; only its CLI contract path points
to v9. The identical prefix SHA and source/contract digests are recorded in
`writing-check-provenance.json`. `measure_writing.py` adds separately labeled
primary-word counts and the current acceptance thresholds; it does not change
sentence splitting, word definitions, flagged terms or scope.

Scope is Introduction through Conclusion. Figures, tables, captions, displayed
math, declarations and references are omitted from body statistics. The abstract
and captions are measured separately. Inline math remains eligible as in PR3.
The primary counter additionally reports the literal main-source count; the
body count is displayed separately, rather than silently switching scopes.

| Snapshot, measured with this same program | Flagged sentences | Mean words | >40 words | primary body / main-source |
|---|---:|---:|---:|---:|
| PR5 exact starting manuscript | 35/246 = 14.227642% | 18.605691 | 1 | 11 / 22 |
| revision-v8 style-source manuscript | 3/185 = 1.621622% | 12.167568 | 0 | 2 / 2 |

These current source measurements do not reproduce the task's quoted
16.1%/20.4/18 and2.3%/14.6/1 snapshots. That difference is retained explicitly;
the program and source scope are not changed to force those quoted figures.
The actual before/after comparison uses `writing-before.json` and the final
v9 result from this one program. The style-source value is a reference, not
the v9 before value.

Acceptance: flagged<=8%, mean<=20words, zero sentences>40words, primary<=3,
and no forbidden internal names in body prose. All eight required limitations
remain in Limitations; a low wording count is not achieved by removing their
content. The final abstract and conclusion also retain their stated word limits.
