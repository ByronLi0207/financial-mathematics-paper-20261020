#!/usr/bin/env python3
"""Independently audit the exact source ZIP whitelist and sync receipt.

This checker does not extract, compile, render, fit or recompute any model. The
allowed membership below is explicit and independent of the archive/receipt;
parsing the current TeX verifies it still describes exactly this closure.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import stat
import sys
import time
import zipfile


REQUIRED_MODE = 0o100644
TEX_ROOTS = (
    "main.tex", "manuscript.tex", "supplement.tex",
    "extended-v9-technical.tex", "title-page.tex",
)
NON_COMPILED_REQUIRED = frozenset((
    "references.bib", "README.md", "AUTHOR-TODO.md", "cover-letter.md",
))
EXPECTED_MEMBERS = frozenset((
    *TEX_ROOTS, *NON_COMPILED_REQUIRED,
    "figures/v7-endpoint-peak-example.pdf",
    "figures/v7-murphy-fx_hourly.pdf",
    "figures/v7-murphy-nyfed_weekly.pdf",
    "figures/v8-wp3-qr33-loss.pdf",
    "figures/v8-wp3-qr4-loss.pdf",
    "figures/v9-unified-history.pdf",
    "generated/v8-backcast-complete-table.tex",
    "generated/v8-daily-results-table.tex",
    "generated/v8-mc-four-table.tex",
    "generated/v8-mc-full-table.tex",
    "generated/v8-three-window-table.tex",
    "generated/v9-evidence-tables.tex",
))
MAX_MEMBER_BYTES = 25 * 1024**2
MAX_TOTAL_BYTES = 100 * 1024**2
SHA_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_member(name):
    """Allow only canonical relative POSIX file names, without normalizing."""
    return (isinstance(name, str) and bool(name) and "\x00" not in name
            and "\\" not in name and not name.startswith("/")
            and not re.match(r"^[A-Za-z]:", name)
            and all(part not in ("", ".", "..", ".git", ".scratch")
                    for part in name.split("/"))
            and str(PurePosixPath(name)) == name)


def _no_symlinks(delivery, name):
    path = delivery
    if path.is_symlink():
        return False
    for component in PurePosixPath(name).parts:
        path = path / component
        if path.is_symlink():
            return False
    return True


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _commentless(source):
    # An unescaped percent begins a TeX comment; preserve newlines for evidence.
    return re.sub(r"(?<!\\)%[^\n]*", "", source)


def check_source_zip(delivery_dir, zip_path, sync_receipt):
    """Return a complete PASS/FAIL receipt without writing or extracting files."""
    start = time.monotonic()
    delivery, package, receipt_path = map(Path, (delivery_dir, zip_path, sync_receipt))
    delivery = delivery.absolute()
    package = package.absolute()
    receipt_path = receipt_path.absolute()
    differences, local, members, receipt = [], {}, [], None

    def issue(code, **details):
        differences.append(dict(code=code, **details))

    # Read only exact approved local files. A link never expands this authority.
    for name in sorted(EXPECTED_MEMBERS):
        path = delivery / name
        if not _no_symlinks(delivery, name):
            issue("LOCAL_SYMLINK", path=name)
            continue
        try:
            info = path.stat()
            mode = stat.S_IFMT(info.st_mode) | stat.S_IMODE(info.st_mode)
            if not stat.S_ISREG(info.st_mode):
                issue("LOCAL_NOT_REGULAR", path=name, actual_mode=oct(mode))
                continue
            if mode != REQUIRED_MODE:
                issue("LOCAL_MODE", path=name, actual_mode=oct(mode), expected_mode=oct(REQUIRED_MODE))
            if info.st_size > MAX_MEMBER_BYTES:
                issue("LOCAL_MEMBER_BUDGET", path=name, bytes=info.st_size)
                continue
            data = path.read_bytes()
            local[name] = dict(data=data, bytes=len(data), sha256=digest(data), mode=mode)
        except (OSError, ValueError) as exc:
            issue("LOCAL_MISSING_OR_UNREADABLE", path=name, error=type(exc).__name__)

    # Current source closure is checked independently, not used to widen the list.
    seen, active, closure_edges = set(), set(), []

    def visit(name):
        if name in active:
            issue("TEX_INPUT_CYCLE", path=name)
            return
        if name in seen:
            return
        if name not in local:
            return
        seen.add(name)
        if not name.endswith(".tex"):
            return
        active.add(name)
        try:
            source = _commentless(local[name]["data"].decode("utf-8"))
        except UnicodeDecodeError:
            issue("TEX_ENCODING", path=name)
            active.remove(name)
            return
        for kind, pattern, extension in (
            ("tex", r"\\(?:input|include)\s*\{([^{}]+)\}", ".tex"),
            ("graphic", r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^{}]+)\}", ".pdf"),
        ):
            for match in re.finditer(pattern, source):
                raw = match.group(1)
                target = raw if PurePosixPath(raw).suffix else raw + extension
                edge = dict(parent=name, target=target, kind=kind)
                closure_edges.append(edge)
                if not safe_member(target):
                    issue("TEX_UNSAFE_DEPENDENCY", **edge)
                    continue
                if target not in EXPECTED_MEMBERS:
                    issue("TEX_NONWHITELIST_DEPENDENCY", **edge)
                    continue
                visit(target)
        active.remove(name)

    for name in TEX_ROOTS:
        visit(name)
    derived_closure = seen | set(NON_COMPILED_REQUIRED)
    for name in sorted(EXPECTED_MEMBERS - derived_closure):
        issue("WHITELIST_MEMBER_NOT_IN_CURRENT_TEX_CLOSURE", path=name)

    package_sha, package_size, archive_names = None, None, []
    try:
        if package.is_symlink():
            raise ValueError("Archive is symlink")
        package_size = package.stat().st_size
        if not package.is_file() or package_size > MAX_TOTAL_BYTES:
            raise ValueError("Archive type/budget")
        package_sha = digest(package.read_bytes())
        with zipfile.ZipFile(package) as archive:
            infos = archive.infolist()
            archive_names = [x.filename for x in infos]
            counts = Counter(archive_names)
            for name, count in sorted(counts.items()):
                if count != 1:
                    issue("ARCHIVE_DUPLICATE", path=name, count=count)
            archive_set = set(archive_names)
            for name in sorted(EXPECTED_MEMBERS - archive_set):
                issue("ARCHIVE_MISSING", path=name)
            for name in sorted(archive_set - EXPECTED_MEMBERS):
                issue("ARCHIVE_EXTRA", path=name)
            total_uncompressed = sum(x.file_size for x in infos)
            if total_uncompressed > MAX_TOTAL_BYTES:
                issue("ARCHIVE_TOTAL_BUDGET", bytes=total_uncompressed)
            for info in infos:
                name = info.filename
                if not safe_member(name) or not safe_member(info.orig_filename):
                    issue("ARCHIVE_UNSAFE_NAME", path=name)
                if info.is_dir():
                    issue("ARCHIVE_DIRECTORY", path=name)
                mode = (info.external_attr >> 16) & 0xFFFF
                if info.create_system != 3 or mode != REQUIRED_MODE:
                    issue("ARCHIVE_MODE", path=name, create_system=info.create_system,
                          actual_mode=oct(mode), expected_mode=oct(REQUIRED_MODE))
                if info.flag_bits & 0x1:
                    issue("ARCHIVE_ENCRYPTED", path=name)
                # Never read an unapproved member, even to fingerprint it.
                if name not in EXPECTED_MEMBERS or counts[name] != 1:
                    continue
                if info.file_size > MAX_MEMBER_BYTES or total_uncompressed > MAX_TOTAL_BYTES:
                    issue("ARCHIVE_MEMBER_BUDGET", path=name, bytes=info.file_size)
                    continue
                try:
                    data = archive.read(info)
                except (RuntimeError, OSError, zipfile.BadZipFile) as exc:
                    issue("ARCHIVE_UNREADABLE_MEMBER", path=name, error=type(exc).__name__)
                    continue
                row = dict(path=name, bytes=len(data), sha256=digest(data), mode=oct(mode),
                           create_system=info.create_system)
                members.append(row)
                if name in local:
                    if data != local[name]["data"]:
                        issue("ARCHIVE_LOCAL_BYTES", path=name,
                              archive_sha256=row["sha256"], local_sha256=local[name]["sha256"])
                    if mode != local[name]["mode"]:
                        issue("ARCHIVE_LOCAL_MODE", path=name)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        issue("ARCHIVE_OPEN", error=type(exc).__name__)

    try:
        receipt = json.loads(receipt_path.read_text())
        if not isinstance(receipt, dict):
            raise ValueError("Receipt is not a mapping")
    except (OSError, ValueError, TypeError) as exc:
        issue("SYNC_RECEIPT_OPEN", error=type(exc).__name__)
        receipt = None
    if receipt is not None:
        if receipt.get("status") != "PASS":
            issue("SYNC_STATUS", actual=receipt.get("status"))
        try:
            expected_package_name = str(package.relative_to(delivery.parent))
        except ValueError:
            expected_package_name = None
            issue("PACKAGE_OUTSIDE_REPO")
        if receipt.get("package") != expected_package_name:
            issue("SYNC_PACKAGE_PATH", expected=expected_package_name, actual=receipt.get("package"))
        if not _is_integer(receipt.get("bytes")) or receipt.get("bytes") != package_size:
            issue("SYNC_PACKAGE_BYTES", expected=package_size, actual=receipt.get("bytes"))
        if not isinstance(receipt.get("sha256"), str) or not SHA_PATTERN.fullmatch(receipt["sha256"]) or receipt["sha256"] != package_sha:
            issue("SYNC_PACKAGE_SHA256", expected=package_sha, actual=receipt.get("sha256"))
        sync_rows = receipt.get("members")
        if not isinstance(sync_rows, list):
            issue("SYNC_MEMBERS_TYPE")
            sync_rows = []
        valid_rows = [x for x in sync_rows if isinstance(x, dict) and isinstance(x.get("path"), str)]
        if len(valid_rows) != len(sync_rows):
            issue("SYNC_MEMBER_ROW_TYPE")
        sync_names = [x["path"] for x in valid_rows]
        for name, count in sorted(Counter(sync_names).items()):
            if count != 1:
                issue("SYNC_DUPLICATE_MEMBER", path=name, count=count)
        for name in sorted(EXPECTED_MEMBERS - set(sync_names)):
            issue("SYNC_MISSING_MEMBER", path=name)
        for name in sorted(set(sync_names) - EXPECTED_MEMBERS):
            issue("SYNC_EXTRA_MEMBER", path=name)
        if sync_names != archive_names:
            issue("SYNC_ARCHIVE_NAME_ORDER", sync_names=sync_names, archive_names=archive_names)
        for row in valid_rows:
            name = row["path"]
            if not safe_member(name):
                issue("SYNC_UNSAFE_NAME", path=name)
            if name not in local:
                continue
            if not _is_integer(row.get("bytes")) or row.get("bytes") != local[name]["bytes"]:
                issue("SYNC_MEMBER_BYTES", path=name, expected=local[name]["bytes"], actual=row.get("bytes"))
            if not isinstance(row.get("sha256"), str) or not SHA_PATTERN.fullmatch(row["sha256"]) or row["sha256"] != local[name]["sha256"]:
                issue("SYNC_MEMBER_SHA256", path=name, expected=local[name]["sha256"], actual=row.get("sha256"))
            # Existing sync rows omit mode; ZIP and local modes are still checked
            # independently above. If a future sync row declares mode, verify it.
            if "mode" in row and row["mode"] not in (REQUIRED_MODE, oct(REQUIRED_MODE)):
                issue("SYNC_MEMBER_MODE", path=name, actual=row["mode"])

    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return dict(status="PASS" if not differences else "FAIL", difference_count=len(differences),
                differences=differences, actual_utc=datetime.now(timezone.utc).isoformat(),
                expected_members=sorted(EXPECTED_MEMBERS), expected_member_count=len(EXPECTED_MEMBERS),
                actual_member_count=len(archive_names), archive_namelist=archive_names,
                package_sha256=package_sha, package_bytes=package_size,
                sync_receipt=str(receipt_path), sync_receipt_sha256=digest(receipt_path.read_bytes()) if receipt_path.is_file() else None,
                member_records=sorted(members, key=lambda x:x["path"]),
                current_tex_closure=sorted(derived_closure), tex_dependency_edges=closure_edges,
                mode_contract="Each ZIP member is a Unix regular0644 file and matches the exact local regular0644 file; receipt mode fields are checked when present. Existing receipt rows supply path/bytes/SHA rather than a mode claim.",
                elapsed_seconds=time.monotonic()-start,
                peak_rss_bytes=rss if sys.platform == "darwin" else rss*1024,
                extracted_members=0, compiled_documents=0, financial_models_run=0,
                scope="Explicit21-file whitelist plus independently parsed current TeX closure, bidirectional namelist, byte/mode and sync-receipt identity. No install, extraction, compile, render, statistical analysis or financial replay.")


def main():
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delivery-dir", type=Path, default=root/"submission-jof")
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--sync-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = check_source_zip(args.delivery_dir,
                              args.zip_path or args.delivery_dir/"overleaf-package.zip",
                              args.sync_receipt)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({k: result[k] for k in ("status", "difference_count", "differences", "expected_member_count", "actual_member_count", "package_sha256", "elapsed_seconds", "peak_rss_bytes", "financial_models_run")}, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
