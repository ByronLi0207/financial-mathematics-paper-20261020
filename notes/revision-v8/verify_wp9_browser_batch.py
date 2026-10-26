"""Read-only remote batch verification against the frozen browser upload copy."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / ".scratch/revision-v8/wp9-browser-source"
manifest = json.loads((SNAPSHOT / "upload-manifest.json").read_text())
index = int(sys.argv[1])
batch = manifest["batches"][index]
fetch = subprocess.run(["git", "fetch", "origin",
    "refs/heads/revision-v8-goal:refs/remotes/origin/revision-v8-goal"],
    cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60)
if fetch.returncode:
    print(fetch.stdout)
    raise SystemExit(fetch.returncode)
remote = subprocess.check_output(["git", "rev-parse", "origin/revision-v8-goal"], cwd=ROOT, text=True).strip()
tree = {}
for entry in subprocess.check_output(["git", "ls-tree", "-r", "-z", remote], cwd=ROOT).split(b"\0"):
    if not entry:
        continue
    meta, name = entry.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    tree[name.decode()] = (mode, kind, oid)
differences = []
for name in batch["files"]:
    data = (SNAPSHOT / name).read_bytes()
    expected = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if tree.get(name) != ("100644", "blob", expected):
        differences.append(name)
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), batch=index,
    directory=batch["directory"], source_commit=manifest["source_commit"],
    remote_commit=remote, file_count=len(batch["files"]), differences=differences,
    status="PASS" if not differences else "PENDING_OR_DIFFERENT",
    method="Fetched Git tree/blob identity and mode against frozen exact local upload bytes; no remote mutation")
(SNAPSHOT / f"batch-{index:02}-remote-receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps(receipt, indent=2))
raise SystemExit(bool(differences))
