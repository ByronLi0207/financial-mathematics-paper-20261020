"""Resolve S3 thesis references to the checked S2 evidence rows."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
clauses = json.loads((here / "thesis-clauses.json").read_text())
rows = {row["id"] for file in (here / "evidence-parts").glob("*.json")
        for row in json.loads(file.read_text())}
missing = [key for clause in clauses for key in clause["evidence"] if key not in rows]
unbound = sum(not clause["evidence"] for clause in clauses)
report = {"status": "PASS" if not missing and not unbound else "FAIL",
          "clauses_checked": len(clauses), "clauses_without_evidence": unbound,
          "missing_evidence_ids": missing, "all_referenced_rows_exist": not missing}
print(json.dumps(report, indent=2))
raise SystemExit(bool(missing or unbound))
