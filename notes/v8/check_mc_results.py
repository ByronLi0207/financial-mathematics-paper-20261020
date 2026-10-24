#!/usr/bin/env python3
"""Independent, post-run readback of the frozen v8 Monte Carlo aggregates.

Uses only Python's standard library and saved scalar receipts. No research
module is imported, no simulation is replayed, no financial source is read,
and no Git operation is performed. Run only after summary.json exists. The
sole output, results/v8/mc/verification.json, is created exclusively.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys


ROOT = Path(__file__).resolve().parents[2]
MC = ROOT / "results/v8/mc"
DESIGN_COMMIT = "b7e548df39bc2d5dc0108a01ec8a7c2ccfbb99d4"
DGPS = ("D0", "D1", "D2")
WINDOWS = (52, 260, 720, 2880)
FEATURES = (4, 33)
GRID = {(d, w, p) for d in DGPS for w in WINDOWS for p in FEATURES}
STATUSES = {"COMPLETE", "FAILED", "NOT_RUN_CELL_FAILED", "INCOMPLETE_DEADLINE"}
SUMMARY_METRICS = (
    "qr_median_pct", "qr_q25_pct", "qr_q75_pct", "win_rate",
    "oracle_median_pct", "i_median_pct", "f_breach_median",
    "i_breach_median", "qr_breach_median", "oracle_breach_median",
    "infinity_frequency",
)


class Audit:
    def __init__(self):
        self.assertions = 0
        self.failures = []
        self.hashes = {}

    def check(self, condition, category, detail):
        self.assertions += 1
        if not condition:
            self.failures.append({"category": category, "detail": detail})

    def equal(self, actual, expected, category, detail):
        if isinstance(expected, float):
            matches = (isinstance(actual, (int, float)) and not isinstance(actual, bool)
                       and math.isfinite(actual)
                       and math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-12))
        else:
            matches = type(actual) is type(expected) and actual == expected
        self.check(matches, category, {"location": detail, "expected": expected, "actual": actual})

    def read(self, relative):
        path = ROOT / relative
        raw = path.read_bytes()
        self.hashes[str(relative)] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw)


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return result.astimezone(timezone.utc)


def primitive_number(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value))


def key(row):
    return row["dgp"], row["window"], row["features"]


def reference_predictions(table):
    """Evaluate frozen inequalities without importing the production scorer."""
    needed = {
        "P1": [("D0", w, p) for w in WINDOWS for p in FEATURES],
        "P2": [("D1", 2880, p) for p in FEATURES],
        "P3": [("D2", 52, 33)],
        "P4": [(d, w, p) for d in ("D1", "D2") for p in FEATURES for w in WINDOWS],
    }
    out = {}
    for name, cells in needed.items():
        if any(table[c]["status"] != "COMPLETE" for c in cells):
            out[name] = {"status": "UNASSESSABLE", "reason": "REQUIRED_CELL_INCOMPLETE_OR_FAILED"}
            continue
        values = [table[c]["qr_median_pct"] for c in cells]
        if name == "P1":
            supported = min(values) >= -2.0
        elif name == "P2":
            supported = max(values) < -5.0
        elif name == "P3":
            supported = values[0] > 5.0
        else:
            supported = True
            for d in ("D1", "D2"):
                for p in FEATURES:
                    sequence = [table[d, w, p]["qr_median_pct"] for w in WINDOWS]
                    supported = supported and all(b <= a for a, b in zip(sequence, sequence[1:]))
        out[name] = {"status": "SUPPORTED" if supported else "NOT_SUPPORTED", "observed_values": values}
    return out


def verify_chronology(audit, chronology_relative, plan, calibration, pilot, formal):
    chronology = audit.read(chronology_relative)
    audit.equal(chronology["design_commit"], DESIGN_COMMIT, "design_commit", "chronology")
    for name, receipt in (("pilot", pilot), ("formal", formal)):
        audit.equal(receipt["design_commit"], DESIGN_COMMIT, "design_commit", name)
        audit.equal(receipt["calibration_sha256"], audit.hashes["results/v8/mc/calibration.json"],
                    "calibration_fingerprint", name)
    protocol_hash = hashlib.sha256((ROOT / "protocol/v8/mc-design.md").read_bytes()).hexdigest()
    audit.equal(protocol_hash, chronology["protocol_sha256"], "protocol_fingerprint", "committed evidence")
    audit.equal(protocol_hash, plan["protocol_sha256"], "protocol_fingerprint", "frozen run plan")
    audit.equal(audit.hashes["results/v8/mc/run-plan.json"], chronology["run_plan_sha256"],
                "run_plan_fingerprint", chronology["run_plan_commit"])
    audit.check(len(chronology["run_plan_commit"]) == 40, "run_plan_commit", chronology["run_plan_commit"])
    times = {
        "design_commit": timestamp(chronology["design_committed_at"]),
        "calibration_receipt": timestamp(calibration["environment"]["created_at_utc"]),
        "first_pilot": timestamp(pilot["started_utc"]),
        "plan_selected": timestamp(plan["selected_at_utc"]),
        "run_plan_commit": timestamp(chronology["run_plan_committed_at"]),
        "formal_start": timestamp(formal["started_utc"]),
    }
    for later in ("calibration_receipt", "first_pilot", "formal_start"):
        audit.check(times["design_commit"] < times[later], "design_precedes_computation", later)
    audit.check(times["calibration_receipt"] < times["first_pilot"], "calibration_precedes_pilot", times["first_pilot"].isoformat())
    audit.check(times["first_pilot"] < times["plan_selected"], "pilot_precedes_plan", times["plan_selected"].isoformat())
    audit.check(times["plan_selected"] <= times["run_plan_commit"] < times["formal_start"],
                "run_plan_committed_before_formal", {k: times[k].isoformat() for k in ("plan_selected", "run_plan_commit", "formal_start")})
    audit.equal(pilot["phase"], 1, "phase_identity", "pilot")
    audit.equal(formal["phase"], 2, "phase_identity", "formal")
    audit.equal(formal["limit_seconds"], 5400, "formal_deadline", "formal receipt")
    for field in ("repetitions", "evaluation_origins"):
        audit.equal(formal[field], plan[field], "formal_matches_frozen_plan", field)
    pilot_timing = ROOT / "results/v8/mc/pilot-timing.json"
    audit.equal(hashlib.sha256(pilot_timing.read_bytes()).hexdigest(), plan["pilot_timing_sha256"],
                "pilot_timing_fingerprint", str(pilot_timing.relative_to(ROOT)))
    for relative, expected in plan["code_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        audit.equal(actual, expected, "frozen_code_unchanged", relative)
    return {name: value.isoformat() for name, value in times.items()}


def verify_records(audit, records, repetitions, m):
    grouped = defaultdict(list)
    counts = Counter()
    oracle_by_rep = defaultdict(list)
    historical_by_rep = defaultdict(list)
    for row in records:
        cell = key(row)
        location = {"dgp": cell[0], "window": cell[1], "features": cell[2], "rep": row["rep"]}
        audit.check(cell in GRID, "declared_grid_cell", location)
        audit.check(isinstance(row["rep"], int) and not isinstance(row["rep"], bool)
                    and 0 <= row["rep"] < repetitions, "required_rep_index", location)
        audit.check(row["status"] in STATUSES, "replicate_status", location)
        grouped[cell].append(row)
        counts[row["status"]] += 1
        if row["status"] != "COMPLETE":
            audit.check(bool(row.get("reason")), "failure_reason_retained", location)
            continue
        valid = True
        for name in ("f", "i", "qr", "oracle"):
            loss = row.get(name + "_loss")
            breach = row.get(name + "_breach")
            condition = primitive_number(loss) and loss >= 0
            audit.check(condition, "finite_nonnegative_loss", {**location, "method": name})
            valid = valid and condition
            condition = primitive_number(breach) and 0 <= breach <= 1
            audit.check(condition, "breach_rate", {**location, "method": name})
            if condition:
                audit.check(math.isclose(breach * m, round(breach * m), rel_tol=0, abs_tol=1e-8),
                            "full_denominator_breach_rate", {**location, "method": name, "denominator": m})
        audit.check(primitive_number(row.get("f_loss")) and row["f_loss"] > 0,
                    "positive_F_denominator", location)
        if not valid or row["f_loss"] <= 0:
            continue
        for name in ("qr", "i", "oracle"):
            expected = 100.0 * (row[name + "_loss"] / row["f_loss"] - 1.0)
            audit.equal(row.get(name + "_change"), expected, "primitive_loss_ratio", {**location, "method": name})
        audit.equal(row.get("win"), row["qr_loss"] < row["f_loss"], "primitive_win", location)
        candidates = row.get("validation_candidates", [])
        menu = {0.001, 0.01, 0.1, 1.0, 10.0, "inf"}
        audit.check(len(candidates) == 6 and {c.get("parameter") for c in candidates} == menu,
                    "full_validation_menu", location)
        eligible = all(c.get("status") == "COMPLETE" and c.get("origin_count") == (1440 if cell[0] == "D1" else 52)
                       and primitive_number(c.get("mean_pinball")) and c["mean_pinball"] >= 0 for c in candidates)
        audit.check(eligible, "complete_validation_candidates", location)
        if len(candidates) == 6 and eligible:
            strongest = lambda c: math.inf if c["parameter"] == "inf" else float(c["parameter"])
            winner = sorted(candidates, key=lambda c: (c["mean_pinball"], -strongest(c)))[0]
            actual = math.inf if row.get("selected") == "inf" else float(row["selected"])
            audit.check(actual == strongest(winner), "validation_selection_and_tie_rule", location)
        if row.get("selected") == "inf":
            audit.equal(row["qr_loss"], row["i_loss"], "infinity_is_I", location)
            audit.equal(row["qr_breach"], row["i_breach"], "infinity_breaches_are_I", location)
        oracle_by_rep[cell[0], row["rep"]].append((location, row["oracle_loss"], row["oracle_breach"]))
        historical_by_rep[cell[0], cell[1], row["rep"]].append(row)
    for cell in GRID:
        rows = grouped[cell]
        audit.check(len(rows) == repetitions, "all_required_rep_records", {"cell": cell, "actual": len(rows), "required": repetitions})
        audit.check(Counter(r["rep"] for r in rows) == Counter(range(repetitions)),
                    "exact_required_rep_set_no_duplicates", cell)
    for locations in oracle_by_rep.values():
        _, first_loss, first_breach = locations[0]
        for location, loss, breach in locations[1:]:
            audit.equal(loss, first_loss, "oracle_shared_across_W_and_p", location)
            audit.equal(breach, first_breach, "oracle_breaches_shared_across_W_and_p", location)
    for rows in historical_by_rep.values():
        if len(rows) == 2:
            for method in ("f", "i"):
                for quantity in ("loss", "breach"):
                    field = method + "_" + quantity
                    audit.equal(rows[0][field], rows[1][field], "historical_shared_across_p", {"field": field, "dgp": rows[0]["dgp"], "window": rows[0]["window"], "rep": rows[0]["rep"]})
    return grouped, dict(counts)


def reference_summary(grouped, repetitions, m):
    expected = {}
    for cell in sorted(GRID):
        rows = grouped[cell]
        complete = [r for r in rows if r["status"] == "COMPLETE"]
        if any(r["status"] == "FAILED" for r in rows):
            status = "FAILED"
        elif len(complete) == repetitions and {r["rep"] for r in complete} == set(range(repetitions)):
            status = "COMPLETE"
        elif any(r["status"] == "INCOMPLETE_DEADLINE" for r in rows):
            status = "INCOMPLETE_DEADLINE"
        else:
            status = "INCOMPLETE"
        out = {"dgp": cell[0], "window": cell[1], "features": cell[2], "status": status,
               "required_repetitions": repetitions, "completed_repetitions": len(complete),
               "evaluation_origins": m, **{field: None for field in SUMMARY_METRICS}}
        if status == "COMPLETE":
            ratios = {name: [100.0 * (r[name + "_loss"] / r["f_loss"] - 1.0) for r in complete]
                      for name in ("qr", "i", "oracle")}
            quartiles = statistics.quantiles(ratios["qr"], n=4, method="inclusive")
            out.update(qr_median_pct=statistics.median(ratios["qr"]), qr_q25_pct=quartiles[0],
                       qr_q75_pct=quartiles[2], win_rate=sum(r["qr_loss"] < r["f_loss"] for r in complete) / repetitions,
                       oracle_median_pct=statistics.median(ratios["oracle"]), i_median_pct=statistics.median(ratios["i"]),
                       infinity_frequency=sum(r["selected"] == "inf" for r in complete) / repetitions)
            for name in ("f", "i", "qr", "oracle"):
                out[name + "_breach_median"] = statistics.median(r[name + "_breach"] for r in complete)
        expected[cell] = out
    return expected


def run(audit, chronology):
    plan = audit.read("results/v8/mc/run-plan.json")
    calibration = audit.read("results/v8/mc/calibration.json")
    pilot = audit.read("results/v8/mc/pilot/receipt.json")
    formal = audit.read("results/v8/mc/formal/receipt.json")
    completion = audit.read("results/v8/mc/formal/completion.json")
    records = audit.read("results/v8/mc/formal/replicates.json")
    summary = audit.read("results/v8/mc/summary.json")
    saved_predictions = audit.read("results/v8/mc/predictions.json")
    times = verify_chronology(audit, chronology, plan, calibration, pilot, formal)
    repetitions, m = plan["repetitions"], plan["evaluation_origins"]
    audit.check((repetitions, m) in {(100, 500), (50, 500), (50, 300)}, "declared_budget_ladder", [repetitions, m])
    audit.check(timestamp(completion["ended_utc"]) >= timestamp(formal["started_utc"]), "completion_after_start", completion["ended_utc"])
    grouped, replicate_counts = verify_records(audit, records, repetitions, m)
    expected = reference_summary(grouped, repetitions, m)
    actual = {key(r): r for r in summary}
    audit.check(len(summary) == 24 and set(actual) == GRID, "all_24_summary_rows", len(summary))
    for cell, reference in expected.items():
        if cell not in actual:
            continue
        for field, value in reference.items():
            audit.equal(actual[cell].get(field), value, "independent_summary", {"cell": cell, "field": field})
    predictions = reference_predictions(expected)
    audit.check(set(saved_predictions) == set(predictions), "four_prespecified_predictions", list(saved_predictions))
    for name, reference in predictions.items():
        saved = saved_predictions.get(name, {})
        audit.equal(saved.get("status"), reference["status"], "independent_prediction", name)
        if "observed_values" in reference:
            audit.check(len(saved.get("observed_values", [])) == len(reference["observed_values"]), "prediction_value_count", name)
            for actual_value, expected_value in zip(saved.get("observed_values", []), reference["observed_values"]):
                audit.equal(actual_value, expected_value, "prediction_values", name)
        else:
            audit.equal(saved.get("reason"), reference["reason"], "prediction_missingness", name)
    return {"required_repetitions": repetitions, "evaluation_origins": m,
            "replicate_record_count": len(records), "replicate_status_counts": replicate_counts,
            "cell_status_counts": dict(Counter(r["status"] for r in expected.values())),
            "independent_predictions": predictions, "chronology_utc": times,
            "independently_recomputed_summary": list(expected.values()),
            "formal_elapsed_seconds": completion["elapsed_seconds"],
            "unfinished_jobs": completion["unfinished_jobs"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chronology", default="notes/v8/commit-chronology.json")
    args = parser.parse_args()
    if not (MC / "summary.json").is_file():
        raise SystemExit("No summary exists; verifier has not run and writes nothing.")
    output = MC / "verification.json"
    if output.exists():
        raise SystemExit("Exclusive verification.json already exists; refusing overwrite.")
    audit = Audit()
    report = {}
    try:
        report = run(audit, args.chronology)
    except Exception as exc:
        audit.check(False, "readback_exception", {"type": type(exc).__name__, "message": str(exc)})
    report.update(status="PASS" if not audit.failures else "FAIL", created_utc=datetime.now(timezone.utc).isoformat(),
                  assertions=audit.assertions, failure_count=len(audit.failures), failures=audit.failures,
                  source_sha256=audit.hashes,
                  method="Standard-library independent scalar readback; statistics.median and inclusive quartiles; no production aggregation import.",
                  limitations=["Breach rates are verified from replicate scalar aggregates and their full M denominator; no private per-origin trace or simulated path is replayed.",
                               "Commit timestamps and committed file fingerprints come from the root's saved live Git evidence in the chronology JSON; this checker does not invoke Git.",
                               "Calibration receipt timestamp is the saved completion timestamp, not independent proof of the first optimizer instruction's wall time.",
                               "No independent real-data validation, financial experiment or DGP calibration is performed."])
    with output.open("x") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({field: report.get(field) for field in ("status", "assertions", "failure_count", "cell_status_counts", "replicate_status_counts")}, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
