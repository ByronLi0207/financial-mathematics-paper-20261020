# WP0: manual treatment of the three PR3 writing commits

Only the new local `revision-v8-goal` branch is changed. PR3 and its source
directory are not merged or edited. Full original substantive diffs are saved
in `wp0-pr3-commit-diffs.txt`; command output for dates, parents and ancestry is
in `wp0-commit-chronology.json`.

| Commit | Decision | Actual treatment and reason |
|---|---|---|
| `d760b6b66188af6f7903a929568ebf12e69a7e47` | 已移植（部分）；其余已覆盖或不采纳 | Its descriptive labels were already used in the v7 main tables. The remaining Supplement panel paragraph and four repeated headers now say original, four-predictor and expanded-menu regression, with the old result-code mapping preserved. The old eleven-table layout is not reintroduced. All 368 numeric result-row strings remain identical in order; `wp0-label-transplant.json` records the exact substitutions and assertion. The shortened old 71-member family note is not transferred onto the v7 table showing the original 72-member family. |
| `91dccbf43efb3f293676c41cfb4e85645e462183` | 已覆盖（核心写作）；不采纳旧稿整体替换 | Its historical-benchmark-first abstract and separation of matched-reference gains, rolling-reference reversal, weekly failures and score/breach disagreement are already present in v7's abstract, introduction, Results and Conclusion. The v7 Evaluation/Limitations sections already preserve mature labels, matched histories/update schedules and retrospective scope. Its old source/PDF is not substituted for the ten-section v7 draft: that would lose existing wrapper, combination, state and quantile-level evidence. Further prose changes belong to WP1, after WP0 acceptance. |
| `2328994c44ec02bd731ad556f41fe9821f6de6df` | 贡献内容已覆盖；不采纳旧核对包作为 v8 验收 | This commit changes historical notes, not the manuscript sources. Its contribution themes agree with v7. Its 19-page PDF, abstract/conclusion metrics and protected-cell checks refer to `manuscript/supervisor-revision/`, not the current 17-page main plus 20-page Supplement. These historical checks cannot serve as current v8 acceptance. Their source files remain untouched in their original history. |

## Chronology, verified rather than inferred

The research-line merge `832563b` occurred at 2026-10-23 22:21:02 PDT.
The writing commits occurred at 23:27:54, 23:28:17 and 23:28:33 PDT, in the
parent chain `0ebc6e5 → d760b6b → 91dccbf → 2328994`. None is an ancestor of
the local v7 final; the common ancestor is `0ebc6e5`. Thus the instruction's
statement “after the v7 merge” is correct when referring to the research-line
merge. A preliminary timing suspicion was resolved and is not a MISMATCH.

## Version boundaries that must not be collapsed

- **MISMATCH-WP0-01 (statistical-family scope):** the later PR3 shortened table
  note uses 71 remaining contrasts. The v7 diagnostics table explicitly uses
  its original 72-member family and the corresponding saved values. Both
  source versions exist; they answer different reporting scopes. We preserve
  v7's matching note instead of transplanting the incompatible 71-family note.
- **MISMATCH-WP0-02 (acceptance object):** PR3's 19-page historical writing
  checks cannot validate the v8 documents. Fresh current checks are required.
  This is a scope mismatch, not a newly discovered error in an empirical value.
- The old alignment JSON records `raw_automated_checks_pass: false`, alongside
  its explanation of label/layout differences and separate cell alignment.
  It is not described as an entirely unflagged raw numeric scan.
- Coarser display of 14.8/16.6/3.2/50.8 in the old prose versus more precise
  v7 tables is rounding, not a change in the underlying financial results.

Same-model read-only commit audit was used to cross-check the coverage. No
Claude request, new study calculation or new statistical test was performed.
