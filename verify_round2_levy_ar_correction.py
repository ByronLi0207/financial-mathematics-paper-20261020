"""Read-only scalar audit of retained D2 AR-correction outputs.

Uses only the standard library. Never imports the simulator, draws random
numbers, fits a model, writes a result, or changes the retained evidence.
"""
from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "results/revision-20261023/round2/levy-ar-correction"
PROTOCOL = "protocol/revision-20261023/D2-AR-correction-20261023.md"
BINDING = ROOT / "protocol/revision-20261023/D2-AR-correction-binding.json"
STATE = RESULT / "prior-scientific-identities.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    def invalid(token):
        raise ValueError("nonfinite JSON token: " + token)
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=invalid)


def aware_time(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "timestamp lacks timezone")
    return result


def covariance_variance(coefficients, phi):
    """Contract a stationary unit-variance AR covariance matrix directly."""
    return math.fsum(
        a * b * phi ** abs(i - j)
        for i, a in enumerate(coefficients)
        for j, b in enumerate(coefficients)
        if a and b
    )


def normal_cdf(value, mean=0.0, variance=1.0):
    require(variance > 0, "positive Gaussian variance required")
    return 0.5 * math.erfc(-(value - mean) / math.sqrt(2 * variance))


def expected_cells():
    cells = {}
    for horizon in (6, 24):
        for family, model, phis in (
            (1, "level", (.68, .85, .98)),
            (2, "increment", (-.3, -.6)),
        ):
            for index, phi in enumerate(phis):
                anchors = ("stationary", "absolute95", "signed95") if model == "level" else ("zero",)
                for anchor_index, anchor in enumerate(anchors):
                    seed = 20261023 + 300000 + 1000 * horizon + 100 * family + 10 * index + anchor_index
                    informations = (
                        ("stationary_increment_endpoint",) if model == "increment"
                        else ("stationary_marginal_endpoint",) if anchor == "stationary"
                        else ("stationary_marginal_endpoint", "conditional_endpoint_oracle")
                    )
                    cells[model, horizon, phi, anchor] = (seed, informations)
    return cells


def audit():
    document = load_json(RESULT / "simulation.json")
    rows = document["results"]
    with (RESULT / "simulation.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        header = reader.fieldnames
        csv_rows = list(reader)
    require(len(rows) == len(csv_rows) == 34, "expected all34 threshold rows")
    require(header == list(rows[0]), "CSV column order differs from JSON row schema")

    binding = load_json(BINDING)
    state = load_json(STATE)
    require(sha256(BINDING) == document["binding_sha256"], "result binding hash mismatch")
    require(binding["sha256"][PROTOCOL] == document["protocol_sha256"] == state["protocol_sha256"],
            "protocol/result/state binding mismatch")
    binding_mismatches = [name for name, digest in binding["sha256"].items()
                          if sha256(ROOT / name) != digest]
    require(not binding_mismatches, "changed bound files: " + repr(binding_mismatches))
    require(aware_time(binding["bound_before_new_outcomes_utc"])
            < aware_time(document["resources"]["started_utc"]), "binding does not precede execution")

    old = state["prior_result_hashes"]
    require(len(old) == 109, "expected109 protected prior-result identities")
    old_mismatches = [name for name, digest in old.items() if sha256(ROOT / name) != digest]
    require(not old_mismatches, "protected prior results changed: " + repr(old_mismatches))

    cells = expected_cells()
    expected_keys = {(m, h, p, a, information)
                     for (m, h, p, a), (_, infos) in cells.items() for information in infos}
    actual_keys = set()
    seed_rows = {}
    primary_count = 0
    max_errors = {name: 0.0 for name in (
        "endpoint_mean", "endpoint_variance", "quantile_CDF", "anchor_CDF",
        "rate", "endpoint_rate", "delta_probability", "delta_percentage_points",
        "MCSE", "peak_minus_twice_endpoint", "stationary_reference_correlation")}
    zero_counts = []
    above_five = []
    ranges = {}

    for number, (row, csv_row) in enumerate(zip(rows, csv_rows)):
        require(list(row) == header and set(csv_row) == set(header), "row schema differs")
        for name, value in row.items():
            if isinstance(value, (float, int)) and not isinstance(value, bool):
                require(math.isfinite(value) and float(csv_row[name]) == value,
                        f"JSON/CSV scalar mismatch at row{number}/{name}")
            else:
                require(csv_row[name] == ("" if value is None else str(value)),
                        f"JSON/CSV field mismatch at row{number}/{name}")

        model, horizon, phi, anchor, information = (row[name] for name in
            ("model", "horizon", "phi", "anchor", "q_information"))
        key = model, horizon, phi, anchor, information
        require(key in expected_keys and key not in actual_keys, "unexpected/duplicate threshold row: " + repr(key))
        actual_keys.add(key)
        seed, infos = cells[model, horizon, phi, anchor]
        require(type(row["seed"]) is int and row["seed"] == seed, "wrong fixed seed")
        seed_rows.setdefault(seed, []).append(row)
        primary = information != "conditional_endpoint_oracle" and anchor != "signed95"
        require(type(row["primary_design"]) is bool and row["primary_design"] == primary,
                "primary/secondary label mismatch")
        primary_count += int(primary)
        require(row["post_result"] is True and row["exploratory"] is True
                and row["independence_premise"] is False, "missing scope/assumption boundary")

        n, hits, endpoint_hits = (row[name] for name in ("paths", "max_exceedances", "endpoint_exceedances"))
        require(all(type(value) is int for value in (n, hits, endpoint_hits))
                and n == 100000 and 0 <= hits <= n and 0 <= endpoint_hits <= n,
                "invalid path/count integers")
        x = row["initial_abs_value"]
        anchor_error = 0.0
        if model == "increment":
            require(x == 0.0, "increment mechanism must start at zero")
            mean = 0.0
            variance = covariance_variance([1.0] * horizon, phi)
            reference_correlation = phi
        else:
            coefficients = [-1.0] + [0.0] * (horizon - 1) + [1.0]
            if anchor == "stationary":
                require(x is None, "stationary random start must not carry a fixedx")
            else:
                require(isinstance(x, (float, int)) and math.isfinite(x) and x > 0,
                        "fixed positive anchor required")
                probability = (normal_cdf(x) - normal_cdf(-x)) if anchor == "absolute95" else normal_cdf(x)
                anchor_error = abs(probability - .95)
            if information == "conditional_endpoint_oracle":
                mean = (phi ** horizon - 1) * x
                weights = [math.sqrt(1 - phi * phi) * phi ** j for j in range(horizon)]
                variance = math.fsum(weight * weight for weight in weights)
            else:
                mean = 0.0
                variance = covariance_variance(coefficients, phi)
            # Independent direct covariance contraction, stationary reference only.
            covariance12 = math.fsum(a * b * phi ** abs(i - j)
                for i, a in enumerate((-1.0, 1.0, 0.0))
                for j, b in enumerate((0.0, -1.0, 1.0)))
            reference_correlation = covariance12 / covariance_variance([-1.0, 1.0], phi)

        q = row["oracle_abs_endpoint_quantile"]
        require(math.isfinite(q) and q > 0, "invalid positive endpoint quantile")
        rate, endpoint_rate = hits / n, endpoint_hits / n
        mcse = math.sqrt(rate * (1 - rate) / n)
        expected = {
            "rate": (row["max_exceedance_rate"], rate),
            "endpoint_rate": (row["endpoint_exceedance_rate"], endpoint_rate),
            "delta_probability": (row["rate_minus_point05"], rate - .05),
            "delta_percentage_points": (row["rate_minus_five_percentage_points"], 100 * (rate - .05)),
            "MCSE": (row["monte_carlo_standard_error"], mcse),
            "peak_minus_twice_endpoint": (row["max_rate_minus_two_endpoint_rate"], rate - 2 * endpoint_rate),
        }
        for name, (actual, wanted) in expected.items():
            error = abs(actual - wanted)
            max_errors[name] = max(max_errors[name], error)
            require(actual == wanted, "integer-derived arithmetic mismatch: " + name + repr(key))
        independent_errors = {
            "endpoint_mean": abs(row["population_endpoint_mean"] - mean),
            "endpoint_variance": abs(row["population_endpoint_variance"] - variance),
            "quantile_CDF": abs(normal_cdf(q, mean, variance) - normal_cdf(-q, mean, variance) - .975),
            "anchor_CDF": anchor_error,
            "stationary_reference_correlation": abs(row["stationary_reference_increment_lag1_correlation"] - reference_correlation),
        }
        for name, error in independent_errors.items():
            max_errors[name] = max(max_errors[name], error)
            require(error <= 2e-13, "independent Gaussian/covariance mismatch: " + name + repr(key))

        if hits == 0:
            upper = -math.expm1(math.log(.05) / n)
            zero_counts.append(dict(row_key=list(key), paths=n, zero_observed=True,
                single_row_one_sided_95_percent_binomial_upper_probability=upper,
                upper_rate_percent=100 * upper))
        if rate > .05:
            above_five.append(dict(row_key=list(key), primary_design=primary,
                rate=rate, excess_percentage_points=100 * (rate - .05), MCSE=mcse,
                excess_in_MCSE_units=(rate - .05) / mcse))
        group = model + "/" + anchor + "/" + information
        ranges.setdefault(group, []).append(rate)

    require(actual_keys == expected_keys and primary_count == 16, "incomplete fixed design")
    require(len(seed_rows) == len(cells) == 22, "wrong distinct seed/path-cell count")
    monotonic_pairs = 0
    for seed, partners in seed_rows.items():
        first = partners[0]
        cell_key = tuple(first[name] for name in ("model", "horizon", "phi", "anchor"))
        require(len(partners) == len(cells[cell_key][1]), "wrong threshold multiplicity")
        require({tuple(row[name] for name in ("model", "horizon", "phi", "anchor")) for row in partners}
                == {cell_key}, "seed reused across different path cells")
        ordered = sorted(partners, key=lambda row: row["oracle_abs_endpoint_quantile"])
        for small, large in zip(ordered, ordered[1:]):
            require(small["max_exceedances"] >= large["max_exceedances"]
                    and small["endpoint_exceedances"] >= large["endpoint_exceedances"],
                    "same-path threshold counts violate monotonicity")
            monotonic_pairs += 1
    require(monotonic_pairs == 12, "expected12 shared-path threshold pairs")

    resource = document["resources"]
    require(0 < resource["peak_rss_bytes"] <= 2 * 1024 ** 3
            and 0 <= resource["elapsed_seconds"] < 590
            and resource["requested_numerical_threads"] == 1
            and resource["maximum_observed_os_threads"] == 1
            and resource["thread_probe_status"] == "PASS", "resource receipt outside declared scope")
    return dict(status="VERIFIED_READ_ONLY_SAVED_OUTPUTS", threshold_rows=34,
        primary_rows=16, secondary_rows=18, unique_initialized_path_cells=22,
        unique_seeds=22, shared_path_monotonicity_pairs=monotonic_pairs,
        JSON_CSV_all_fields_match=True, independent_max_absolute_errors=max_errors,
        bound_files_checked=len(binding["sha256"]), binding_precedes_actual_start=True,
        protected_prior_result_hashes_checked=len(old), protected_prior_result_mismatches=[],
        simulation_sha256=sha256(RESULT / "simulation.json"),
        CSV_sha256=sha256(RESULT / "simulation.csv"), resources=resource,
        state_status=state.get("status"), state_current=state.get("current"),
        rate_ranges={name: dict(rows=len(values), minimum=min(values), maximum=max(values))
                     for name, values in sorted(ranges.items())},
        zero_count_single_row_bounds=zero_counts,
        above_five_percent_point_estimates=above_five,
        interpretation=[
            "The qCDF check uses the information set explicitly named in each row. A stationary-marginalq at a fixed start is not a conditional endpoint oracle.",
            "Stationary-reference increment correlation is not the actual nonstationary fixed-start conditional increment correlation.",
            "Threshold partners share a seed and have monotone counts. Aggregate files alone cannot reconstruct or independently prove the realized shared paths; the before-run bound implementation specifies that sharing.",
            "Zero observed exceedances do not establish zero population risk. Listed upper bounds are exact one-sided95% binomial bounds for each single predetermined row under independent Monte Carlo paths; they are not simultaneous bounds across rows.",
            "A point estimate above5% does not by itself establish population violation or a general counterexample; no new path draw, stopping, model fit or outcome-based threshold choice is performed.",
            "All main checks use retained JSON/CSV and immutable hashes only. No result files or state are written."
        ])


def main():
    try:
        summary = audit()
    except Exception as exc:
        print(json.dumps(dict(status="FAILED_READ_ONLY_AUDIT", error_type=type(exc).__name__,
                              error=str(exc)), ensure_ascii=False, allow_nan=False, indent=2))
        return 1
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
