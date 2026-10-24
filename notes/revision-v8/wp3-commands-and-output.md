# Actual WP3 commands and original console output

Commands below are the actual executed invocations. Output is copied verbatim from each preserved console file; shell redirection explains why it was not printed by the launching cell. All six invocations returned exit0.

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp3.py --run > notes/revision-v8/wp3-study-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "study_terminated", "status": "COMPLETE", "reason": null}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with arch --with scikit-learn python -B run_v8_wp3.py --summarize > notes/revision-v8/wp3-summary-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
{"event": "summary_written", "status": "COMPLETE", "cells": 216}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/audit_wp3.py --output notes/revision-v8/wp3-independent-audit.json > notes/revision-v8/wp3-audit-console.txt 2>&1
{"status": "PASS", "difference_count": 0, "actual_inventory_count": 6912, "summary_cell_count": 216, "method_status_counts": {"COMPLETE": 6912}}
[exit 0]
```

```text
$ OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with matplotlib --with pypdf --with pillow python -B notes/revision-v8/plot_wp3.py --summary results/revision-v8/wp3/summary.json --outdir .scratch/revision-v8/wp3-formal-figures > notes/revision-v8/wp3-figure-console.txt 2>&1
WARN `--no-project` was provided, but no project was found
Matplotlib is building the font cache; this may take a moment.
{"figures": 6, "source_sha256": "3de27c0f50a5b1882d4c8aba80d3fc8d2487972f22674d7e6e1423e62da663d0", "output_directory": ".scratch/revision-v8/wp3-formal-figures"}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/build_wp3_readout.py > notes/revision-v8/wp3-readout-console.txt 2>&1
{"method_tasks": 6912, "summary_rows": 216, "candidate_status_counts": {"COMPLETE": 18431, "FAILED": 1}, "scientific_screen": "MISMATCH", "figures": 6, "input_changes": 0}
[exit 0]
```

```text
$ python3 -B notes/revision-v8/package_wp3.py --audit notes/revision-v8/wp3-independent-audit.json > notes/revision-v8/wp3-package-console.txt 2>&1
{"status": "PASS", "archive_name": "wp3-driver-output.tar.gz", "member_count": 38599, "archive_bytes": 14883171, "archive_sha256": "519f442094420053d8160ae07e5612f55ac8fe53d07fa8c689b674cdff7ecdb5", "source_hashes_unchanged": "PASS"}
[exit 0]
```
