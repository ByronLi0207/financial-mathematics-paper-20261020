"""Run default full discovery in a fresh copy; preserve original research files.

Verification only. No test module filtering, test deletion or financial study.
Uses an already-cached temporary uv environment, never system installation.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
stage = sys.argv[1]
if not stage.replace("-", "").isalnum():
    raise ValueError("A simple stage identifier is required")
scratch = ROOT / ".scratch" / "revision-v8" / stage
copy = scratch / "full-suite-copy"
copy.mkdir(parents=True, exist_ok=False)
paths = [p.decode() for p in subprocess.check_output(
    ["git", "ls-files", "-z"], cwd=ROOT).split(b"\0") if p]
for name in paths:
    target = copy / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, target)
env = dict(os.environ)
env.pop("PYTHONPATH", None)
env.update(UV_OFFLINE="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
           MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1",
           VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
cmd = ["/Users/bingyouli/.local/bin/uv", "run", "--no-project",
       "--no-env-file", "--python",
       "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
       "--with", "pytest", "--with", "arch", "--with", "scikit-learn",
       "python", "-B", "-m", "pytest", "-p", "no:cacheprovider", "-v",
       "--basetemp", str(scratch / "pytest-temp")]
start = dt.datetime.now(dt.timezone.utc).isoformat()
clock = time.monotonic()
log = ROOT / "notes" / "revision-v8" / (stage + "-pytest-output.txt")
with log.open("w") as stream:
    try:
        result = subprocess.run(cmd, cwd=copy, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=600)
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = 124
receipt = dict(command=cmd, cwd=str(copy), scope="Full default discovery; every tracked file copied; no test filtering or skips added",
               tracked_files_copied=len(paths), started_utc=start,
               ended_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
               elapsed_seconds=time.monotonic() - clock, returncode=code,
               child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               output_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
               numerical_threads=1, UV_OFFLINE=True)
(log.parent / (stage + "-pytest-receipt.json")).write_text(
    json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
print("\n".join(log.read_text().splitlines()[-8:]))
raise SystemExit(code)
