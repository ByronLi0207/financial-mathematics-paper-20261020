"""Verify a complete browser-published file tree without publishing Git identities.

Uses Git's read-only transport and a streaming cat-file process. It neither
pushes nor changes research bytes, account settings, or source histories.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
TARGET = "refs/remotes/origin/revision-v8-goal"
PROTECTED = {
    "main": "65feeee801b6b228a608ca3200e0678bb5f62b1c",
    "codex/supervisor-revision-20261023": "2328994c44ec02bd731ad556f41fe9821f6de6df",
    "revision-v7-final": "d119a1fb30c48ceab9000552057882938cfa57a4",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def tree(commit):
    result = {}
    for entry in git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if entry:
            meta, name = entry.split(b"\t", 1)
            result[name.decode()] = tuple(meta.decode().split())
    return result


def check(source, output):
    start = time.monotonic()
    refs = ["revision-v8-goal", *PROTECTED]
    cmd = ["git", "-c", "pack.threads=1", "-c", "pack.windowMemory=64m",
           "fetch", "origin", *[f"refs/heads/{r}:refs/remotes/origin/{r}" for r in refs]]
    subprocess.run(cmd, cwd=ROOT, check=True, timeout=60,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    source = git("rev-parse", source+"^{commit}").decode().strip()
    remote = git("rev-parse", TARGET).decode().strip()
    left, right = tree(source), tree(remote)
    missing = sorted(set(left)-set(right)); extra = sorted(set(right)-set(left))
    changed = [name for name in sorted(set(left)&set(right)) if left[name] != right[name]]
    rows = []; byte_count = 0; cache = {}
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for name in sorted(set(left)&set(right)):
            if left[name] != right[name]:
                continue
            mode, kind, oid = right[name]
            if kind != "blob":
                raise ValueError("Unexpected non-file object: "+name)
            if oid not in cache:
                process.stdin.write((oid+"\n").encode()); process.stdin.flush()
                header = process.stdout.readline().decode().split()
                assert len(header)==3 and header[:2]==[oid,"blob"], header
                size = remaining = int(header[2]); h = hashlib.sha256()
                while remaining:
                    block = process.stdout.read(min(65536,remaining))
                    assert block, (name,remaining)
                    h.update(block); remaining -= len(block)
                assert process.stdout.read(1)==b"\n"
                cache[oid] = (size,h.hexdigest())
            size,digest = cache[oid]; byte_count += size
            rows.append(dict(path=name,mode=mode,git_blob=oid,bytes=size,sha256=digest))
    finally:
        process.stdin.close(); process.wait(timeout=10)
    assert process.returncode==0
    output = Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    csv_path = output.with_name(output.stem+"-files.csv")
    with csv_path.open("x",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=["path","mode","git_blob","bytes","sha256"])
        writer.writeheader(); writer.writerows(rows)
    protected={r:git("rev-parse","refs/remotes/origin/"+r).decode().strip() for r in PROTECTED}
    protected_differences={r:dict(expected=PROTECTED[r],actual=actual)
                           for r,actual in protected.items() if actual!=PROTECTED[r]}
    source_tree=git("rev-parse",source+"^{tree}").decode().strip()
    remote_tree=git("rev-parse",remote+"^{tree}").decode().strip()
    diff=subprocess.run(["git","diff","--quiet",source,remote,"--"],cwd=ROOT).returncode
    record=dict(utc=datetime.now(timezone.utc).isoformat(),
        status="PASS" if not missing and not extra and not changed and diff==0 else "FAIL",
        source_commit=source,remote_commit=remote,source_tree=source_tree,remote_tree=remote_tree,
        source_files=len(left),remote_files=len(right),files_checked=len(rows),bytes_checked=byte_count,
        missing=missing,extra=extra,changed_or_mode_mismatches=changed,git_diff_returncode=diff,
        per_file_sha256_csv=str(csv_path),
        per_file_csv_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        protected_remote_refs=protected,protected_ref_differences=protected_differences,
        elapsed_seconds=time.monotonic()-start,blob_stream_buffer_max_bytes=65536,
        no_remote_mutations=True,no_Git_identity_objects_published=True,
        scope="Complete file-tree and streamed content identity; remote/local commit histories differ. Financial replay and journal acceptance are not certified.")
    with output.open("x") as stream:stream.write(json.dumps(record,indent=2)+"\n")
    return record


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit",required=True)
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    result=check(args.source_commit,args.output)
    print(json.dumps(result,indent=2))
    raise SystemExit(result["status"]!="PASS")
