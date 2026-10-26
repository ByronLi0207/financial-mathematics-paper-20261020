"""S2/S9 read-only field checking, within v7 whitelist (a) and (b).

This script reads saved fields and exact text, never fits or tests a model.
Evidence records preserve the original source value, selector and source bytes.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def pointer(value, path):
    if path == "":
        return value
    if not path.startswith("/"):
        raise ValueError("JSON pointer must start with /")
    for piece in path[1:].split("/"):
        key = piece.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def read(record):
    source = ROOT / record["source"]
    if not source.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("source outside repository")
    raw = source.read_bytes()
    kind = record["format"]
    if kind == "json":
        got = pointer(json.loads(raw), record["pointer"])
    elif kind == "csv":
        rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
        matches = [row for row in rows if all(row[k] == str(v) for k, v in record["where"].items())]
        if len(matches) != 1:
            raise ValueError(f"CSV selector found {len(matches)} rows")
        got = matches[0][record["field"]]
    elif kind == "text":
        text = raw.decode("utf-8")
        if record["value"] not in text:
            raise ValueError("exact text absent")
        got = record["value"]
    else:
        raise ValueError(f"unsupported evidence format: {kind}")
    if got != record["value"] or type(got) is not type(record["value"]):
        raise ValueError(f"field mismatch: {got!r} versus {record['value']!r}")
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write new S2 table/verification files")
    parser.add_argument("--append-table", action="store_true", help="append newly required saved fields without changing an existing S2 row")
    args = parser.parse_args()
    records = []
    for part in sorted((HERE / "evidence-parts").glob("*.json")):
        payload = json.loads(part.read_text())
        if not isinstance(payload, list):
            raise ValueError(f"expected a list: {part}")
        records.extend(payload)
    if not records:
        raise ValueError("no evidence records")
    ids, failures, sources = set(), [], {}
    for record in records:
        try:
            if record["id"] in ids:
                raise ValueError("duplicate row ID")
            ids.add(record["id"])
            sources[record["source"]] = read(record)
        except Exception as exc:
            failures.append({"id": record.get("id"), "error": str(exc)})
    report = {"status": "PASS" if not failures else "FAIL", "rows_checked": len(records),
              "source_files_checked": len(sources), "mismatches": len(failures), "failures": failures,
              "new_models": 0, "new_hypothesis_tests": 0, "new_data": 0}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.append_table:
        if failures:
            raise SystemExit(1)
        prior_sources = json.loads((HERE / "evidence-source-fingerprints.json").read_text())
        if any(sources.get(name) != digest for name, digest in prior_sources.items()):
            raise ValueError("an original S2 source changed")
        table = HERE / "evidence-table.md"
        original = table.read_text()
        existing = {line.split("|")[1].strip() for line in original.splitlines() if line.startswith("| ")}
        added = [record for record in records if record["id"] not in existing]
        clean = lambda value: str(value).replace("|", "&#124;").replace("\n", "<br>")
        extra = []
        for record in added:
            selector = record.get("pointer", json.dumps(record.get("where", {})) + " / " + record.get("field", "exact passage"))
            extra.append("| " + " | ".join(clean(v) for v in (record["id"], record["claim"], json.dumps(record["value"], ensure_ascii=False), record["source"], selector)) + " |")
        table.write_text(original + "\n".join(extra) + ("\n" if extra else ""))
        assert table.read_text().startswith(original)
        print(json.dumps({"existing_rows_changed": 0, "existing_source_changes": 0, "new_saved_fields_appended": len(added)}, indent=2))
    if args.write:
        if failures:
            raise SystemExit(1)
        rows = ["# v7 evidence table", "", "Every value below is an exact saved field or exact source passage; it is checked by `python3 notes/v7/check_evidence.py`. Original reports keep their original definitions and comparison families.", "", "| ID | Conclusion / scope | Exact saved value | Source | Field / selector |", "|---|---|---|---|---|"]
        clean = lambda value: str(value).replace("|", "&#124;").replace("\n", "<br>")
        for record in records:
            selector = record.get("pointer", json.dumps(record.get("where", {}), ensure_ascii=False) + " / " + record.get("field", "exact passage"))
            rows.append("| " + " | ".join(clean(v) for v in (record["id"], record["claim"], json.dumps(record["value"], ensure_ascii=False), record["source"], selector)) + " |")
        for name, content in (("evidence-table.md", "\n".join(rows) + "\n"),
                              ("evidence-verification.json", json.dumps(report, indent=2) + "\n"),
                              ("evidence-source-fingerprints.json", json.dumps(sources, indent=2) + "\n")):
            with (HERE / name).open("x") as handle:
                handle.write(content)
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
