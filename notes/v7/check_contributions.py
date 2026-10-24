"""S4 contribution-location and forbidden-phrase checks; no financial run."""
import json
import re
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
contributions = json.loads((here / "contributions.json").read_text())
rows = {row["id"] for file in (here / "evidence-parts").glob("*.json")
        for row in json.loads(file.read_text())}
main = (root / "submission-jof/manuscript.tex").read_text()
banned = {phrase: len(re.findall(pattern, main, flags=re.I)) for phrase, pattern in (
    ("merely", r"\bmerely\b"),
    ("only an application", r"\bonly\s+an\s+application\b"),
    ("using mature methods", r"\busing\s+mature\s+methods\b"))}
missing = [key for item in contributions for key in item["evidence"] if key not in rows]
locations = {item["id"]: item["current_main_location"] for item in contributions}
normal = lambda value: value.replace("’", "'").replace("–", "--").replace("—", "---")
presence = {item["id"]: all(normal(sentence) in main for sentence in item["sentences"])
            for item in contributions}
sentence_counts = {item["id"]: len(item["sentences"]) for item in contributions}
passed = (all(4 <= count <= 6 for count in sentence_counts.values())
          and all(locations.values()) and all(presence.values())
          and not missing and not any(banned.values()))
report = {"status": "PASS" if passed else "FAIL", "sentence_counts": sentence_counts,
          "main_passages_present": presence, "evidence_locations": locations,
          "missing_evidence_ids": missing, "forbidden_phrase_counts_current_main": banned,
          "priority_claims_added": 0}
print(json.dumps(report, indent=2))
raise SystemExit(not passed)
