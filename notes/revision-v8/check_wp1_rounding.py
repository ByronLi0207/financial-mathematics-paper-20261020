"""Read original saved fields and verify rounded prose, without new analysis."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("v8_writing", ROOT / "notes/revision-v8/writing_metrics.py")
writing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writing)
ROWS = {r["id"]: r for p in (ROOT / "notes/v7/evidence-parts").glob("*.json")
        for r in json.loads(p.read_text())}
# Anchors bind every percentage-bearing prose sentence to its original fields.
CASES = [
    ("At the shorter horizon, long-history FX regression lowers matched loss", ["FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT", "FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT"]),
    ("Against a historical headroom rule with the same history, it lowers", ["FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT"]),
    ("The earlier-period reduction is", ["FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT"]),
    ("It lowers matched loss by", ["FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT", "FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT"]),
    ("Adjusted regression lowers mean loss", ["FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT"]),
    ("At the lower target, regression lowers loss", ["FX_TAU90_MATCHED_MEAN_LOSS_CHANGE_PERCENT", "FX_TAU90_PRIMARY_MEAN_LOSS_CHANGE_PERCENT"]),
    ("Against the original shorter-history rolling rule, it lowers", ["FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT", "FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT"]),
    ("The short-history FX regression at the longer horizon raises", ["FX_LATE_SHORT_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT"]),
    ("Its loss increase is", ["PANEL_BILL_QR_H6_W260_LOSS_PERCENT"]),
    ("The richer regression's median excess loss falls", ["PANEL_E5_QR33_MEDIAN", "PANEL_E5_QR33_EXPANDED_MEDIAN"]),
    ("The fixed median combination lowers loss", ["PANEL_WP3_BILL_PRIMARY_MEDIAN_VS_F"]),
    ("The fixed mean combination instead raises loss", ["PANEL_WP3_BILL_PRIMARY_MEAN_VS_F"]),
]


def original_value(row):
    path = ROOT / row["source"]
    if row["format"] == "csv":
        data = list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))
        selected = [r for r in data if all(r[k] == v for k, v in row["where"].items())]
        assert len(selected) == 1
        value = selected[0][row["field"]]
    elif row["format"] == "json":
        value = json.loads(path.read_text())
        for key in row["pointer"].lstrip("/").split("/") if row["pointer"] else []:
            key = key.replace("~1", "/").replace("~0", "~")
            value = value[int(key)] if isinstance(value, list) else value[key]
    else:
        raise ValueError("Unsupported financial-field source")
    assert value == row["value"], row["id"]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    abstract, paragraphs = writing.prose((ROOT / "submission-jof/manuscript.tex").read_text())
    sentences = writing.v7.sentences(abstract + " " + " ".join(paragraphs))
    records = []
    failures = []
    bound = []
    for anchor, identifiers in CASES:
        matches = [s for s in sentences if s.startswith(anchor)]
        assert len(matches) == 1, (anchor, matches)
        sentence = matches[0]
        actual = re.findall(r"(?<![\w.])([+-]?\d+(?:\.\d+)?)\s*%", sentence)
        expected = [format(abs(float(original_value(ROWS[key]))), ".1f") for key in identifiers]
        item = dict(anchor=anchor, sentence=sentence, ids=identifiers,
                    sources=[ROWS[key]["source"] for key in identifiers],
                    raw_values=[ROWS[key]["value"] for key in identifiers],
                    actual_display=actual, expected_display=expected, match=actual == expected)
        records.append(item)
        bound.append(sentence)
        if not item["match"]:
            failures.append(item)
    all_percentage_sentences = [s for s in sentences if re.search(r"\d\s*%", s)]
    assert all_percentage_sentences == bound, "Unbound or reordered prose percentage sentence"
    report = dict(operation="saved-field lookup and display formatting only", bound_percentages=sum(len(x[1]) for x in CASES),
                  records=records, mismatches=len(failures), failures=failures)
    (ROOT / args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("operation", "bound_percentages", "mismatches", "failures")}, indent=2))
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
