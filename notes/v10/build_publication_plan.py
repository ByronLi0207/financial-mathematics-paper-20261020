"""Read-only Git metadata to upload batches; run only after the final commit.

No Git/network/UI mutation. The only output is an exclusive local JSON plan.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "0d2526cc69092c5158437a0509613bac5e86d47f"
MAX_FILES = 80
MAX_BYTES = 20 * 1024 * 1024


def git(*args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    return subprocess.check_output(["git", *args], cwd=ROOT, env=env)


def eligible(path):
    parts = PurePosixPath(path).parts
    return ".scratch" not in parts and ".git" not in parts and not path.endswith(".bak")


def tracked_tree(head):
    result = {}
    for raw in git("ls-tree", "-rz", "--full-tree", head).split(b"\0"):
        if not raw:
            continue
        metadata, path = raw.split(b"\t", 1)
        mode, kind, blob = metadata.decode("ascii").split()
        result[os.fsdecode(path)] = dict(mode=mode, kind=kind, blob=blob)
    return result


def file_record(relative, tree, status=None):
    entry = tree[relative]
    if entry["kind"] != "blob" or entry["mode"] not in {"100644", "100755"}:
        raise ValueError("UNSUPPORTED_UPLOAD_MODE:" + relative)
    path = ROOT / relative
    if path.is_symlink() or not path.is_file():
        raise ValueError("MISSING_OR_SYMLINK_PAYLOAD:" + relative)
    size = path.stat().st_size
    expected_executable = entry["mode"] == "100755"
    if bool(path.stat().st_mode & 0o111) != expected_executable:
        raise ValueError("WORKTREE_MODE_DIFFERS_FROM_HEAD:" + relative)
    sha256 = hashlib.sha256()
    blob = hashlib.sha1(b"blob " + str(size).encode("ascii") + b"\0")
    actual = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha256.update(chunk)
            blob.update(chunk)
            actual += len(chunk)
    if actual != size or blob.hexdigest() != entry["blob"]:
        raise ValueError("WORKTREE_BYTES_DIFFER_FROM_HEAD:" + relative)
    return dict(status=status, relative_path=relative, absolute_path=str(path),
                directory=str(PurePosixPath(relative).parent), bytes=size,
                sha256=sha256.hexdigest(), mode=entry["mode"], git_blob=entry["blob"])


def group_batches(files):
    """Deterministic directory-local batches; no file is split or omitted."""
    grouped = defaultdict(list)
    for item in files:
        grouped[item["directory"]].append(item)
    batches = []
    for directory in sorted(grouped):
        current, size = [], 0

        def flush():
            nonlocal current, size
            if current:
                batches.append(dict(batch_id=f"b{len(batches):04d}", directory=directory,
                    absolute_directory=str(ROOT / directory), file_count=len(current),
                    bytes=size, files=current))
                current, size = [], 0

        for item in sorted(grouped[directory], key=lambda x: x["relative_path"]):
            if item["bytes"] > MAX_BYTES:
                raise ValueError("SINGLE_FILE_EXCEEDS_20MIB:" + item["relative_path"])
            # A full-size formal archive part must be its own batch, including
            # when an adjacent zero-byte file would otherwise fit.
            if item["bytes"] == MAX_BYTES:
                flush()
                current, size = [item], item["bytes"]
                flush()
                continue
            if len(current) == MAX_FILES or size + item["bytes"] > MAX_BYTES:
                flush()
            current.append(item)
            size += item["bytes"]
        flush()
    return batches


def cftc_trace_preservation(tree, changed):
    relative = "results/v10/cftc/method-inventory.json"
    inventory = file_record(relative, tree)
    rows = json.loads((ROOT / relative).read_text())
    if not isinstance(rows, list) or len(rows) != 204:
        raise ValueError("EXPECTED_204_CFTC_METHOD_ROWS")
    traces = []
    for row in rows:
        path = row["trace_path"]
        if row["status"] != "COMPLETE" or path not in tree or not eligible(path):
            raise ValueError("CFTC_COMPLETE_TRACE_NOT_TRACKED:" + path)
        record = file_record(path, tree)
        if record["bytes"] != row["trace_bytes"] or record["sha256"] != row["trace_sha256"]:
            raise ValueError("CFTC_TRACE_RECEIPT_MISMATCH:" + path)
        record["publication_disposition"] = "upload" if path in changed else "preserved_from_base"
        traces.append(record)
    if len({x["relative_path"] for x in traces}) != 204:
        raise ValueError("EXPECTED_204_DISTINCT_CFTC_TRACE_FILES")
    return dict(method_inventory=inventory, count=204, all_traces_tracked_and_verified=True,
                no_trace_arrays_loaded=True, traces=traces)


def build_plan():
    head = git("rev-parse", "HEAD").decode().strip()
    git("merge-base", "--is-ancestor", BASE, head)
    if git("rev-parse", "--show-object-format").decode().strip() != "sha1":
        raise ValueError("EXPECTED_SHA1_GIT_OBJECT_FORMAT")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("COMMIT_TRACKED_CHANGES_BEFORE_PUBLICATION_PLAN")
    tree = tracked_tree(head)
    parts = git("diff", "--no-renames", "--name-status", "-z", "--diff-filter=AM", BASE, head).split(b"\0")
    files, excluded = [], []
    for i in range(0, len(parts) - 1, 2):
        status, relative = parts[i].decode("ascii"), os.fsdecode(parts[i + 1])
        if not eligible(relative):
            excluded.append(dict(relative_path=relative, reason="bak_or_scratch_excluded"))
            continue
        files.append(file_record(relative, tree, status))
    batches = group_batches(files)
    changed = {x["relative_path"] for x in files}
    traces = cftc_trace_preservation(tree, changed)
    untracked = [os.fsdecode(p) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p]
    if git("rev-parse", "HEAD").decode().strip() != head:
        raise ValueError("HEAD_CHANGED_DURING_PLAN")
    ref = "refs/heads/archive/v10-original-" + head[:12]
    bundle = ROOT / ".scratch/v10" / ("v10-original-" + head[:12] + ".bundle")
    q = shlex.quote
    return dict(schema="v10-publication-plan-v1", status="READY_METADATA_ONLY",
        created_utc=datetime.now(timezone.utc).isoformat(), root=str(ROOT), base_commit=BASE,
        frozen_head=head, diff_filter="ADD_MODIFY_ONLY_NO_RENAMES_NO_DELETIONS",
        target_policy="Create a NEW publication branch from base_commit; never overwrite an existing remote branch. Remote absence has NOT been checked.",
        max_files_per_batch=MAX_FILES, max_bytes_per_batch=MAX_BYTES,
        file_count=len(files), bytes=sum(x["bytes"] for x in files), batch_count=len(batches),
        batches=batches, excluded_tracked=excluded, excluded_untracked=untracked,
        ignored_files_policy="Ignored files are not tracked diff inputs; .bak and .scratch are additionally excluded. Untracked E7 notes enter only after commit.",
        earlier_files_policy="No deletion is planned. All base files are preserved; only the explicit A/M inventory is uploaded.",
        cftc_complete_trace_preservation=traces,
        history_preservation_advice=dict(executed=False,
            explanation="Advice only: preserve the original new local commits before any browser upload creates a different publication history. The expected-old zero value prevents overwriting an existing archive ref. Bundle contains the new history with the base commit as prerequisite; keep a base repository as well.",
            commands=["git update-ref " + q(ref) + " " + q(head) + " " + "0" * 40,
                      "git bundle create " + q(str(bundle)) + " " + q(ref) + " " + q("^" + BASE),
                      "git bundle verify " + q(str(bundle)),
                      "git bundle list-heads " + q(str(bundle))]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".scratch/v10/publication-plan.json")
    args = parser.parse_args()
    plan = build_plan()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(plan, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(json.dumps(dict(status=plan["status"], frozen_head=plan["frozen_head"],
        files=plan["file_count"], batches=plan["batch_count"], bytes=plan["bytes"],
        excluded_untracked=len(plan["excluded_untracked"]), output=str(args.output))))


if __name__ == "__main__":
    main()
