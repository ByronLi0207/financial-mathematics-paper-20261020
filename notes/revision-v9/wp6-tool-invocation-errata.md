# WP6 invocation errata — actual rejected attempts

These are task invocation mistakes or intended overwrite/output guards, not numerical study failures. No financial experiment ran in any of these attempts. Actual tool-output excerpts are copied below without changing their error text. Successful readbacks follow in the WP6 CHANGELOG and dedicated output files.

```text
python3 -B notes/revision-v9/build_wp5_tables.py
FileExistsError: refuse to overwrite generated evidence; use --check

python3 -B notes/revision-v9/build_wp5_tables.py --check
AssertionError
```

The first check followed a two-label generator edit before the canonical presentation label migration. Recovery explicitly proved that the entire generated payload was identical except for its TeX hash, preserved the original WP5 binding, and wrote a new WP6 presentation binding. No overwrite guard was removed; source result values and all 228 numeric bindings stayed equal.

```text
python3 -B notes/revision-v9/check_main_numbers.py --output notes/revision-v9/wp6-main-number-audit.json
ValueError: new v9 wp5-main-/wp7-main- output prefix required
```

The checker was rerun with its existing allowed `wp5-main-wp6-review-audit.json` prefix; its guard was not changed.

```text
uv run --offline --no-project --with pytest python -B -m pytest test_v9_main_numbers.py test_v8_main_numbers.py test_v9_compile_documents.py -q
ERROR: file or directory not found: test_v9_compile_documents.py

no tests ran in 0.00s
```

The correct existing filename was found with `rg --files`: `test_v9_compile_diagnostics.py`. The actual second command passed all 35 targeted controls in 3.37 seconds, saved in `wp6-targeted-tests-attempt2.txt`. The first stdout remains in `wp6-targeted-tests.txt`.

```text
measure(Path('submission-jof/manuscript.tex'))
ValueError: 'submission-jof/manuscript.tex' is not in the subpath of '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023' OR one path is relative and the other is absolute.
```

The unchanged metrics function requires an absolute path; the subsequent call used `resolve()` and passed. No scoring or style rule was modified.
