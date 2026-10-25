# v11 test and public-package verification

The original working checkout passes the complete existing suite: **1,715 tests and 1,181 subtests**. Its exact command, environment, times and output are in [final-tests.json](final-tests.json). No financial experiment, forecast study or restricted-input replay was executed in this revision.

The same command was also run against an independently downloaded public checkout at `b3390eed6734276ee2176e71b0b3eb40fbc49749`. The first run is deliberately retained as **FAIL: 30 failed, 1,685 passed, 1,181 subtests passed**. All failures stop at `git show` of three absent historical Git objects. These are the historical document-number controls and the original v9 design guard, rather than changed v11 forecasts or numerical results. This precondition was already documented in [the v9 reproduction guide](../v9/REPRODUCING.md).

The three original author-retained commits are:

- `642d6af9eaccdd27896fd7a2e265cddd6f7a91e5` — old supplement baseline;
- `b571f324a253480b4e39bc8a8096775ddbcc7017` — old numeric-inventory baseline;
- `5decccb0a13ef1969629cfec695dd3459c412c4e` — original v9 design.

They were copied into the isolated local verification checkout only. Their original commit bytes were checked against the author's retained repository. No test, guard, source file, result, checked-out tree, public ref or old directory was changed. Repeating the **unmodified full suite** then passed **1,715 tests and 1,181 subtests**. The public checkout remained clean. See [the prerequisite receipt](historical-test-prerequisites.json), [the original public-clone FAIL](public-clone-tests.json), and [the qualified complete PASS](public-clone-with-history-tests.json).

The command was:

```sh
uv run --offline --no-project --no-env-file \
  --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1 \
  --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow \
  python -B -m pytest -q -p no:cacheprovider
```

The saved environment fixes the native thread counts to one, sets `PYTHONDONTWRITEBYTECODE=1` and `GIT_OPTIONAL_LOCKS=0`, and uses temporary uv dependencies. No package was installed into system Python.

This does **not** turn a bare public clone into a complete historical-test or financial-replay environment. Publishing a safe historical-object route remains the earlier author action T6; the original historical bundle is not published here. Restricted FX observations are a separate input requirement. The recorded FAIL is not replaced by the later qualified PASS.

The publicly downloaded native source ZIP was independently extracted and all four targets were compiled. It has **32 members** and produces **20/34/1/1 pages** for the main article, supplement, title page and cover letter. All **56 rendered page images** and extracted page texts exactly match the already reviewed canonical pages. These document checks need no private observations or historical Git objects; see [public-source-package-check.json](public-source-package-check.json).

The writing statistics retain the original checker. The requested three gates pass; its five additional legacy flags are literal Supplement S1/S2/S3 cross-references. Their raw flags remain in the JSON, and the checker was not changed.

The final English-only closure was tested again in the unchanged original historical-object environment: **1,715 tests and 1,181 subtests passed**. Its exact final command, UTC times and output fingerprint are in [closure-tests.json](closure-tests.json). Earlier public-package checks bind their named snapshot; the final public package has its separate closing readback receipt.

The final public source ZIP readback is now [public-source-package-closure.json](public-source-package-closure.json): its 32 members produce all four targets and all 56 reviewed page images exactly. This closing receipt binds the named public commit and the final archive fingerprint.
