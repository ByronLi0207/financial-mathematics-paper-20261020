"""Bounded runner for the frozen exploratory selected-history comparison.

Import and --help are source independent. Only main loads the existing source,
with acquisition disabled. Calculation helpers accept synthetic arrays directly.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import time

THREAD_NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
for _thread_name in THREAD_NAMES:
    os.environ[_thread_name] = "1"
sys.dont_write_bytecode = True

# Preserve the real CLI clock before numerical imports. Explicit argv calls
# are an import-safe library/testing entry and get their own invocation clock.
PROCESS_STARTED_MONOTONIC = time.monotonic()
PROCESS_STARTED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

import numpy as np
import study_core as core
from revision_selection import METHODS, issue_selected
from run_study import RunGuard, StudyStop, arm_hard_deadline, create_attempt, utc_now, sha_file

ROOT = Path(__file__).resolve().parent
SPEC_SHA256 = "fe836dfd17390031b8721ec8f7860919e596bbc2682ee34d6b2f4ab4b462b8c8"
PROTOCOL_SHA256 = "55e2359666068b799f64bca6c0b23edc32f891fbd47b2430b22786dd8a363e36"
ORIGINAL_SPEC_SHA256 = "0b8eda7bfd858c038bae22a96a7caa5ff21838317de58bc56eef98ca696c54ff"
PUBLIC_COMMIT = "69d5bb67c6ca1e3c1509e29c14400462ce2a1130"


@dataclass(frozen=True)
class Scores:
    origins: np.ndarray
    capacities: np.ndarray
    floors: np.ndarray
    errors: np.ndarray
    pinball: np.ndarray
    overrun: np.ndarray
    unused: np.ndarray
    strict_breach: np.ndarray


def score_arrays(peak, capacities, floors, origins):
    """Score stored P-C using independently converted 19/20 and 1/20."""
    peak = core._vector(peak, "peak")
    floors = core._vector(floors, "floors")
    origins = core._indices(origins, "evaluation origins")
    capacities = np.asarray(capacities, dtype=np.float64)
    if (capacities.shape != (len(peak), 3) or floors.shape != peak.shape or origins.shape != peak.shape
            or not np.isfinite(capacities).all() or np.any(peak < floors) or np.any(floors < 0)
            or np.any(capacities < floors[:, None])):
        raise ValueError("invalid scoring alignment or floor")
    with np.errstate(over="raise", invalid="raise"):
        errors = peak[:, None] - capacities
        overrun = np.maximum(errors, 0.)
        unused = np.maximum(-errors, 0.)
        pinball = float(Fraction(19, 20)) * overrun + float(Fraction(1, 20)) * unused
    for values in (errors, overrun, unused, pinball):
        core._finite(values, "score")
    return Scores(*(core._readonly(values) for values in
                    (origins, capacities, floors, errors, pinball, overrun, unused, errors > 0)))


def method_metrics(scores, j):
    if type(j) is not int or not 0 <= j < 3:
        raise ValueError("invalid method")
    count = len(scores.origins)
    breaches = int(np.count_nonzero(scores.strict_breach[:, j]))
    mean_overrun = core.stable_mean(scores.overrun[:, j])
    conditional = float(math.fsum(float(v) for v in scores.overrun[:, j]) / breaches) if breaches else None
    metrics = dict(mean_pinball=core.stable_mean(scores.pinball[:, j]),
                   mean_capacity=core.stable_mean(scores.capacities[:, j]),
                   mean_extra_allowance=core.stable_mean(scores.capacities[:, j] - scores.floors),
                   strict_breach_count=breaches, strict_breach_rate=float(breaches / count),
                   mean_positive_overrun=mean_overrun, conditional_mean_overrun=conditional,
                   conditional_overrun_denominator=breaches,
                   mean_unused_allowance=core.stable_mean(scores.unused[:, j]),
                   conditional_overrun_undefined_reason=None if breaches else "NO_STRICT_BREACHES")
    core._assert_mean_equal(metrics["mean_pinball"], float(Fraction(19, 20))*mean_overrun +
                            float(Fraction(1, 20))*metrics["mean_unused_allowance"], count,
                            max(1., metrics["mean_pinball"]))
    if conditional is not None:
        core._assert_mean_equal(mean_overrun, metrics["strict_breach_rate"]*conditional, count,
                                max(1., mean_overrun, conditional))
    return metrics


def _public_tree(value, depth=0):
    if depth > 20:
        raise ValueError("invalid public nesting")
    if value is None or type(value) in (bool, int):
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("nonfinite public value")
        return
    if type(value) is str:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ._:+-]{0,199}", value):
            raise ValueError("unsafe public text")
        return
    if type(value) is list:
        for child in value:
            _public_tree(child, depth+1)
        return
    if type(value) is dict:
        for key, child in value.items():
            if type(key) is not str or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,99}", key) or any(
                    fragment in key.lower() for fragment in ("account", "path", "username", "email", "credential", "token")):
                raise ValueError("unsafe public key")
            _public_tree(child, depth+1)
        return
    raise ValueError("nonbuiltin public object")


def public_json_bytes(value):
    _public_tree(value)
    return (json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8")


def csv_bytes(rows, columns):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        if set(row) != set(columns):
            raise ValueError("CSV column mismatch")
        _public_tree(row)
        writer.writerow({key: "" if value is None else value for key, value in row.items()})
    return buffer.getvalue().encode("utf-8")

SETS = (("full720", "full", 720, 685), ("recent360", "recent", 360, 343),
        ("nearest360", "nearest", 360, 343), ("recent180", "recent", 180, 172),
        ("nearest180", "nearest", 180, 172))
METRICS = ("mean_pinball", "mean_capacity", "mean_extra_allowance", "strict_breach_count", "strict_breach_rate",
           "mean_positive_overrun", "conditional_mean_overrun", "conditional_overrun_denominator", "mean_unused_allowance")
META = ("horizon", "eligible_count", "set_id", "selection", "selected_count", "tau_numerator", "tau_denominator", "rank", "origin_count")
SUMMARY_COLUMNS = META + ("method_id",) + METRICS + ("conditional_overrun_undefined_reason",)
GEOMETRY_COLUMNS = META + ("mean_absolute_f_minus_s", "equal_capacity_count", "mean_absolute_anchor_radius",
                           "mean_signed_anchor_radius", "mean_selected_origin_age_records", "maximum_geometry_excess", "maximum_arithmetic_tolerance")
COMPARISON_COLUMNS = ("horizon", "contrast_id", "left_set", "right_set", "left_method", "right_method", "origin_count", "mean_pinball_difference")
MONTHLY_COLUMNS = ("horizon", "month", "origin_count", "status", "mean_pinball_nearest360_K", "mean_pinball_recent360_K",
                   "mean_pinball_difference", "undefined_reason")
TABLE_COLUMNS = {"summary": SUMMARY_COLUMNS, "geometry": GEOMETRY_COLUMNS, "comparisons": COMPARISON_COLUMNS, "monthly": MONTHLY_COLUMNS}
CODE_FILES = ("revision_selection.py", "run_revision_selection.py", "test_revision_selection.py", "test_revision_runner.py",
              "study_core.py", "study_data.py", "run_study.py")
CHECK_NAMES = ("frozen_protocol", "source_identity", "origin_identity", "complete_pool_eligibility", "finite_scores",
               "geometry", "aggregate_identities", "original_global_reference", "public_serialization", "code_identity", "resources")
STOP_CODES = ("NONE", "SPECIFICATION", "SOURCE_IDENTITY_OR_SCHEMA", "SOURCE_FETCH_OR_ARCHIVE", "OUTPUT_INTEGRITY",
              "RESOURCE_UNVERIFIED", "RESOURCE_WALL", "RESOURCE_RSS", "RESOURCE_THREADS", "RESOURCE_STORAGE",
              "STRUCTURAL_OR_NUMERIC", "RUNTIME_UNAVAILABLE", "INTERNAL")


def validate_spec(spec):
    expected = dict(horizons=[6, 24], eligible_count=720, tau_numerator=19, tau_denominator=20,
                    first_origin=11927, last_origin=18551, expected_origin_count=6625, expected_source_rows=18576,
                    representations=["F", "S", "K"], fetch_new_data=False, monthly_display_min_origins=30,
                    calendar_months_inclusive=["2016-01", "2017-01"],
                    public_tables=dict(summary_rows=30, geometry_rows=10, comparison_rows=22, monthly_primary_rows=26))
    if type(spec) is not dict or any(type(spec.get(k)) is not type(v) or spec.get(k) != v for k, v in expected.items()):
        raise ValueError("fixed specification mismatch")
    if spec.get("sets") != [dict(set_id=s, selection=q, count=n, rank=k) for s, q, n, k in SETS]:
        raise ValueError("fixed menu mismatch")
    if tuple(METHODS) != ("F", "S", "K"):
        raise ValueError("method interface mismatch")


def load_protocol(root=ROOT):
    """Check local frozen bytes and existing public-freeze receipt, without data."""
    try:
        paths = ("protocol/revision-20261021-exploratory-spec.json", "protocol/revision-20261021-exploratory-protocol.md", "protocol/study-spec.json")
        for relative, digest in zip(paths, (SPEC_SHA256, PROTOCOL_SHA256, ORIGINAL_SPEC_SHA256)):
            if sha_file(root / relative) != digest:
                raise ValueError("pinned bytes changed")
        spec = json.loads((root / paths[0]).read_text())
        old = json.loads((root / paths[2]).read_text())
        validate_spec(spec)
        if (spec["protocol_sha256"] != PROTOCOL_SHA256 or spec["original_spec_sha256"] != ORIGINAL_SPEC_SHA256
                or spec["source_csv_sha256"] != old["source"]["expected_csv_sha256"]
                or spec["source_csv_bytes"] != old["source"]["expected_csv_bytes"]
                or spec["expected_source_rows"] != old["source"]["expected_rows"]):
            raise ValueError("source specification mismatch")
        receipt = json.loads((root / "state/revision-20261021-protocol-publication.json").read_text())
        expected = {paths[0]: SPEC_SHA256, paths[1]: PROTOCOL_SHA256}
        if (receipt["status"] != "VERIFIED" or receipt["commit"] != PUBLIC_COMMIT or
                {row["path"]: row["sha256"] for row in receipt["files"]} != expected):
            raise ValueError("public freeze receipt mismatch")
        return spec, old
    except (OSError, ValueError, KeyError, TypeError):
        raise StudyStop("SPECIFICATION") from None


def monthly_rows(times, left, right, horizon):
    times = np.asarray(times)
    left, right = core._vector(left, "monthly left"), core._vector(right, "monthly right")
    if times.ndim != 1 or times.dtype.kind != "M" or np.isnat(times).any() or left.shape != times.shape or right.shape != times.shape or horizon not in (6, 24):
        raise ValueError("monthly alignment mismatch")
    months = times.astype("datetime64[M]")
    allowed = np.arange(np.datetime64("2016-01", "M"), np.datetime64("2017-02", "M"))
    if not np.isin(months, allowed).all():
        raise ValueError("monthly origin outside fixed calendar")
    rows = []
    for month in allowed:
        mask = months == month
        n = int(np.count_nonzero(mask))
        shown = n >= 30
        rows.append(dict(horizon=int(horizon), month=str(month), origin_count=n,
                         status="DISPLAYED" if shown else "SUPPRESSED",
                         mean_pinball_nearest360_K=core.stable_mean(left[mask]) if shown else None,
                         mean_pinball_recent360_K=core.stable_mean(right[mask]) if shown else None,
                         mean_pinball_difference=core.stable_mean(left[mask]-right[mask]) if shown else None,
                         undefined_reason=None if shown else ("NO_ORIGINS" if not n else "GROUP_BELOW_DISPLAY_MIN")))
    return rows


def _metadata(horizon, item, count):
    set_id, selection, m, rank = item
    return dict(horizon=int(horizon), eligible_count=720, set_id=set_id, selection=selection, selected_count=m,
                tau_numerator=19, tau_denominator=20, rank=rank, origin_count=int(count))


def compose(position, times, origins, spec, checkpoint=None):
    """Calculate the fixed menu from supplied arrays; no source I/O or inference."""
    validate_spec(spec)
    position = core._vector(position, "composition position")
    times = core._times(times)
    origins = core._indices(origins, "composition origins")
    if len(position) != 18576 or len(times) != len(position) or not np.array_equal(origins, np.arange(11927, 18552)):
        raise ValueError("source or common origin identity mismatch")
    # Origins must remain the original full-menu cutoff/last-origin rule.
    summary, geometry, comparisons, monthly, digests = [], [], [], [], []
    count = len(origins)
    floors = np.abs(position[origins])
    for horizon in (6, 24):
        cell = core.CellSpec("h"+str(horizon), horizon, 720, 19, 20, 685)
        cache = core.build_label_cache(position, horizon)
        results = {}
        for item in SETS:
            set_id, selection, m, rank = item
            caps = np.empty((count, 3), dtype=np.float64)
            diagnostics = np.empty((count, 6), dtype=np.float64)
            digest = hashlib.sha256()
            for j, origin in enumerate(origins):
                t = int(origin)
                labels = core.mature_window(cache, t, cell)
                issued = issue_selected(t, float(position[t]), labels, position[labels.origins], cell, selection, m)
                if issued.rank != rank or len(issued.origins) != m:
                    raise ValueError("selected interface identity mismatch")
                caps[j] = issued.capacities
                diagnostics[j] = (issued.absolute_radius, issued.signed_radius, issued.mean_age_records,
                                  issued.geometry_excess, issued.arithmetic_tolerance, issued.refined_bound)
                digest.update(t.to_bytes(8, "little"))
                digest.update(np.asarray(issued.origins, dtype="<i8").tobytes())
                if checkpoint is not None and (j+1) % 100 == 0:
                    checkpoint(stage="revision_forecast", cell_id="h"+str(horizon)+"_"+set_id, completed_origins=j+1)
            if checkpoint is not None and count % 100:
                checkpoint(stage="revision_forecast", cell_id="h"+str(horizon)+"_"+set_id, completed_origins=count)
            scores = score_arrays(cache.peak[origins], caps, floors, origins)
            results[set_id] = scores
            meta = _metadata(horizon, item, count)
            summary.extend(dict(meta, method_id=method, **method_metrics(scores, j)) for j, method in enumerate(METHODS))
            geometry.append(dict(meta, mean_absolute_f_minus_s=core.stable_mean(np.abs(caps[:, 0]-caps[:, 1])),
                                 equal_capacity_count=int(np.count_nonzero(caps[:, 0] == caps[:, 1])),
                                 mean_absolute_anchor_radius=core.stable_mean(diagnostics[:, 0]),
                                 mean_signed_anchor_radius=core.stable_mean(diagnostics[:, 1]),
                                 mean_selected_origin_age_records=core.stable_mean(diagnostics[:, 2]),
                                 maximum_geometry_excess=float(np.max(diagnostics[:, 3])),
                                 maximum_arithmetic_tolerance=float(np.max(diagnostics[:, 4]))))
            digests.append(dict(horizon=horizon, set_id=set_id, sha256=digest.hexdigest()))
            if checkpoint is not None and hasattr(checkpoint, "arrays"):
                checkpoint.arrays(position, times, origins, floors, cache, results, caps, diagnostics)
        for m in (360, 180):
            for j, method in enumerate(METHODS):
                comparisons.append(dict(horizon=horizon, contrast_id="nearest_minus_recent", left_set="nearest"+str(m),
                                        right_set="recent"+str(m), left_method=method, right_method=method, origin_count=count,
                                        mean_pinball_difference=core.stable_mean(results["nearest"+str(m)].pinball[:, j]-results["recent"+str(m)].pinball[:, j])))
        for set_id, _, _, _ in SETS:
            comparisons.append(dict(horizon=horizon, contrast_id="F_minus_S", left_set=set_id, right_set=set_id,
                                    left_method="F", right_method="S", origin_count=count,
                                    mean_pinball_difference=core.stable_mean(results[set_id].pinball[:, 0]-results[set_id].pinball[:, 1])))
        monthly.extend(monthly_rows(times[origins], results["nearest360"].pinball[:, 2], results["recent360"].pinball[:, 2], horizon))
    bundle = dict(summary=summary, geometry=geometry, comparisons=comparisons, monthly=monthly,
                  private=dict(selection_digests=digests, origin_count=count, first_source_index=int(origins[0]), last_source_index=int(origins[-1])))
    validate_tables(bundle, spec)
    return bundle


def _number(value, *, nonnegative=False):
    if type(value) not in (int, float) or not math.isfinite(value) or (nonnegative and value < 0):
        raise ValueError("invalid public number")


def _count(value, maximum=6625):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError("invalid public count")


def _close(left, right, count=6625, scale=None):
    core._assert_mean_equal(left, right, count, max(1., abs(left), abs(right), scale or 0.))


def validate_tables(bundle, spec):
    validate_spec(spec)
    for name, n in (("summary", 30), ("geometry", 10), ("comparisons", 22), ("monthly", 26)):
        rows = bundle[name]
        if type(rows) is not list or len(rows) != n:
            raise ValueError("aggregate row count mismatch")
        for row in rows:
            if type(row) is not dict or set(row) != set(TABLE_COLUMNS[name]):
                raise ValueError("aggregate schema mismatch")
            _public_tree(row)
    expected_meta = [_metadata(h, item, 6625) for h in (6, 24) for item in SETS]
    index = {}
    for i, row in enumerate(bundle["summary"]):
        meta = expected_meta[i//3]
        if any(type(row[k]) is not type(v) or row[k] != v for k, v in meta.items()) or row["method_id"] != METHODS[i%3]:
            raise ValueError("summary identity mismatch")
        for metric in METRICS:
            if metric != "conditional_mean_overrun":
                _number(row[metric], nonnegative=True)
        for key in ("strict_breach_count", "conditional_overrun_denominator"):
            _count(row[key])
        b = row["strict_breach_count"]
        if b != row["conditional_overrun_denominator"] or row["strict_breach_rate"] != b/6625:
            raise ValueError("breach denominator mismatch")
        if not b:
            if row["conditional_mean_overrun"] is not None or row["conditional_overrun_undefined_reason"] != "NO_STRICT_BREACHES" or row["mean_positive_overrun"] != 0.:
                raise ValueError("undefined conditional severity mismatch")
        else:
            _number(row["conditional_mean_overrun"], nonnegative=True)
            if row["conditional_mean_overrun"] <= 0 or row["conditional_overrun_undefined_reason"] is not None:
                raise ValueError("conditional severity reason mismatch")
            _close(row["mean_positive_overrun"], row["strict_breach_rate"]*row["conditional_mean_overrun"])
        _close(row["mean_pinball"], .95*row["mean_positive_overrun"]+.05*row["mean_unused_allowance"])
        if row["mean_extra_allowance"] > row["mean_capacity"]:
            raise ValueError("extra exceeds capacity")
        index[row["horizon"], row["set_id"], row["method_id"]] = row
    for row, meta in zip(bundle["geometry"], expected_meta):
        if any(type(row[k]) is not type(v) or row[k] != v for k, v in meta.items()):
            raise ValueError("geometry identity mismatch")
        _count(row["equal_capacity_count"])
        for key in GEOMETRY_COLUMNS[len(META):]:
            _number(row[key], nonnegative=True)
        if row["maximum_geometry_excess"] > row["maximum_arithmetic_tolerance"]:
            raise ValueError("geometry check failed")
    identities = []
    for h in (6, 24):
        identities.extend((h, "nearest_minus_recent", "nearest"+str(m), "recent"+str(m), method, method) for m in (360, 180) for method in METHODS)
        identities.extend((h, "F_minus_S", set_id, set_id, "F", "S") for set_id, _, _, _ in SETS)
    for row, identity in zip(bundle["comparisons"], identities):
        if tuple(row[k] for k in COMPARISON_COLUMNS[:6]) != identity or type(row["origin_count"]) is not int or row["origin_count"] != 6625:
            raise ValueError("comparison identity mismatch")
        _number(row["mean_pinball_difference"])
        h, _, left, right, lm, rm = identity
        _close(row["mean_pinball_difference"], index[h, left, lm]["mean_pinball"]-index[h, right, rm]["mean_pinball"],
               scale=max(index[h, left, lm]["mean_pinball"], index[h, right, rm]["mean_pinball"]))
    for i, row in enumerate(bundle["monthly"]):
        month = str(np.datetime64("2016-01", "M") + i%13)
        if row["horizon"] != (6 if i < 13 else 24) or row["month"] != month:
            raise ValueError("monthly identity mismatch")
        _count(row["origin_count"])
        n = row["origin_count"]
        if n < 30:
            if row["status"] != "SUPPRESSED" or row["undefined_reason"] != ("NO_ORIGINS" if not n else "GROUP_BELOW_DISPLAY_MIN") or any(row[k] is not None for k in MONTHLY_COLUMNS[4:7]):
                raise ValueError("monthly suppression mismatch")
        else:
            if row["status"] != "DISPLAYED" or row["undefined_reason"] is not None:
                raise ValueError("monthly display status mismatch")
            for key in MONTHLY_COLUMNS[4:7]:
                _number(row[key], nonnegative=key != "mean_pinball_difference")
            _close(row["mean_pinball_difference"], row["mean_pinball_nearest360_K"]-row["mean_pinball_recent360_K"], n,
                   scale=max(row["mean_pinball_nearest360_K"], row["mean_pinball_recent360_K"]))
    for h in (6, 24):
        if sum(r["origin_count"] for r in bundle["monthly"] if r["horizon"] == h) != 6625:
            raise ValueError("monthly count reconciliation failed")


def table_bytes(bundle, spec):
    validate_tables(bundle, spec)
    return {name+".csv": csv_bytes(bundle[name], columns) for name, columns in TABLE_COLUMNS.items()}


def validate_original_reference(summary, reference):
    """Reconcile six shared full720 aggregates; K alone maps to original L."""
    selected = [row for row in reference if row.get("cell_id") in ("main", "h24") and row.get("method_id") in ("F", "S", "L")]
    if len(selected) != 6 or len({(r["cell_id"], r["method_id"]) for r in selected}) != 6:
        raise ValueError("original reference identity missing")
    original = {(r["cell_id"], r["method_id"]): r for r in selected}
    shared = [r for r in summary if r["set_id"] == "full720"]
    if len(shared) != 6:
        raise ValueError("full720 reference count mismatch")
    for row in shared:
        old = original[("main" if row["horizon"] == 6 else "h24", "L" if row["method_id"] == "K" else row["method_id"])]
        for key in ("horizon", "tau_numerator", "tau_denominator", "rank", "origin_count"):
            if int(old[key]) != row[key]:
                raise ValueError("original reference metadata mismatch")
        if int(old["window"]) != 720:
            raise ValueError("original reference window mismatch")
        for key in METRICS:
            value = old[key]
            if key == "conditional_mean_overrun" and value in ("", None):
                if row[key] is not None:
                    raise ValueError("original null mismatch")
            elif key in ("strict_breach_count", "conditional_overrun_denominator"):
                if int(value) != row[key]:
                    raise ValueError("original breach count mismatch")
            else:
                _close(float(value), row[key])
        if (old["conditional_overrun_undefined_reason"] or None) != row["conditional_overrun_undefined_reason"]:
            raise ValueError("original null reason mismatch")


def validate_source_identity(identity):
    expected = dict(accepted_csv_bytes=1286391, accepted_csv_sha256="b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
                    source_verified=True, acquisition_mode="local_reuse", request_performed_this_attempt=False, download=None)
    if type(identity) is not dict or any(type(identity.get(k)) is not type(v) or identity.get(k) != v for k, v in expected.items()):
        raise ValueError("source reuse identity mismatch")
    if type(identity.get("local_validation_utc")) is not str or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", identity["local_validation_utc"]):
        raise ValueError("source validation time missing")


def validate_measured_resources(resources):
    from run_study import check_resource_limits
    try:
        check_resource_limits(resources["elapsed_seconds"], resources["peak_rss_bytes"], resources["maximum_observed_os_threads"])
        if resources["thread_probe_status"] != "PASS" or type(resources["thread_snapshot_count"]) is not int or resources["thread_snapshot_count"] <= 0:
            raise ValueError("unverified snapshots")
        if type(resources["checkpoint_utc"]) is not str or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", resources["checkpoint_utc"]):
            raise ValueError("unverified measurement timestamp")
    except (KeyError, StudyStop) as exc:
        raise ValueError("unverified or exceeded resources") from exc


def new_attempt(output, root=ROOT):
    output, scratch = Path(output).absolute(), (root/".scratch").absolute()
    try:
        relative = output.relative_to(scratch)
        if not relative.parts or ".." in output.parts or any(p.is_symlink() for p in (output, *output.parents)):
            raise ValueError
        return create_attempt(output)
    except (ValueError, OSError):
        raise StudyStop("OUTPUT_INTEGRITY") from None


def exclusive_write(target, content):
    target = Path(target)
    if type(content) is not bytes or any(p.is_symlink() for p in (target, *target.parents)):
        raise StudyStop("OUTPUT_INTEGRITY")
    try:
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
    except OSError:
        raise StudyStop("OUTPUT_INTEGRITY") from None


def initial_manifest(started_utc, code_hashes):
    return dict(manifest_schema_version=1, revision_id="exploratory-state-selection-20261021",
                run_status="INCOMPLETE", stop_code="NONE", started_utc=started_utc,
                specification=dict(spec_sha256=SPEC_SHA256, protocol_sha256=PROTOCOL_SHA256,
                                   original_spec_sha256=ORIGINAL_SPEC_SHA256, public_freeze_commit=PUBLIC_COMMIT),
                source=dict(expected_csv_bytes=1286391, expected_csv_sha256="b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
                            expected_rows=18576, accepted_csv_bytes=None, accepted_csv_sha256=None, source_verified=False,
                            acquisition_mode=None, request_performed_this_attempt=False, local_validation_utc=None, download=None),
                evaluation=dict(origin_count=None, first_source_index=None, last_source_index=None),
                original_reference=dict(summary_sha256=None, h6_original_cell="main", h24_original_cell="h24", K_original_method="L"),
                code=[dict(file_name=name, sha256=digest) for name, digest in code_hashes.items()],
                environment=dict(python_version=sys.version.split()[0], numpy_version=str(np.__version__),
                                 thread_requests={name: os.environ.get(name) for name in THREAD_NAMES}),
                resources={}, checks={name: "NOT_RUN" for name in CHECK_NAMES}, artifacts=[],
                undefined_conventions=dict(csv_empty_is_null=True, no_strict_breaches="NO_STRICT_BREACHES",
                                           below_display_min="GROUP_BELOW_DISPLAY_MIN", no_origins="NO_ORIGINS"))


def mark_failure(manifest, guard, error):
    code = getattr(error, "code", None)
    if code not in STOP_CODES or code == "NONE":
        code = "STRUCTURAL_OR_NUMERIC" if isinstance(error, (ValueError, ArithmeticError)) else "INTERNAL"
    manifest.update(run_status="INCOMPLETE", stop_code=code, resources=dict(guard.resources))


def validate_manifest(manifest):
    expected_keys = {"manifest_schema_version", "revision_id", "run_status", "stop_code", "started_utc", "specification", "source",
                     "evaluation", "original_reference", "code", "environment", "resources", "checks", "artifacts", "undefined_conventions"}
    if type(manifest) is not dict or set(manifest) != expected_keys:
        raise ValueError("manifest schema mismatch")
    _public_tree(manifest)
    if (manifest["manifest_schema_version"] != 1 or manifest["revision_id"] != "exploratory-state-selection-20261021"
            or manifest["run_status"] not in ("COMPLETE", "INCOMPLETE") or manifest["stop_code"] not in STOP_CODES):
        raise ValueError("manifest status mismatch")
    expected_spec = initial_manifest(manifest["started_utc"], {})["specification"]
    if manifest["specification"] != expected_spec or set(manifest["checks"]) != set(CHECK_NAMES) or any(v not in ("PASS", "NOT_RUN", "FAIL") for v in manifest["checks"].values()):
        raise ValueError("manifest identity mismatch")
    template = initial_manifest(manifest["started_utc"], {})
    for area in ("source", "evaluation", "original_reference", "environment", "undefined_conventions"):
        if type(manifest[area]) is not dict or set(manifest[area]) != set(template[area]):
            raise ValueError("unknown nested manifest field")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", manifest["started_utc"]):
        raise ValueError("invalid start timestamp")
    for key in ("expected_csv_bytes", "expected_csv_sha256", "expected_rows"):
        if type(manifest["source"][key]) is not type(template["source"][key]) or manifest["source"][key] != template["source"][key]:
            raise ValueError("source expected identity mismatch")
    if type(manifest["source"]["source_verified"]) is not bool:
        raise ValueError("source verification flag mismatch")
    if manifest["source"]["source_verified"]:
        validate_source_identity(manifest["source"])
    elif any(manifest["source"][k] is not None for k in ("accepted_csv_bytes", "accepted_csv_sha256", "acquisition_mode", "local_validation_utc", "download")) or manifest["source"]["request_performed_this_attempt"] is not False:
        raise ValueError("unverified source provenance")
    if manifest["evaluation"] not in (template["evaluation"], dict(origin_count=6625, first_source_index=11927, last_source_index=18551)):
        raise ValueError("evaluation identity mismatch")
    reference = manifest["original_reference"]
    if any(reference[k] != template["original_reference"][k] for k in ("h6_original_cell", "h24_original_cell", "K_original_method")) or (reference["summary_sha256"] is not None and not re.fullmatch(r"[0-9a-f]{64}", reference["summary_sha256"])):
        raise ValueError("original reference identity mismatch")
    if manifest["undefined_conventions"] != template["undefined_conventions"]:
        raise ValueError("undefined convention mismatch")
    for key in ("python_version", "numpy_version"):
        if type(manifest["environment"][key]) is not str or not re.fullmatch(r"\d+\.\d+\.\d+", manifest["environment"][key]):
            raise ValueError("environment version mismatch")
    resource_keys = {"started_utc", "checkpoint_utc", "measurement_point", "requested_numerical_threads", "elapsed_seconds", "peak_rss_bytes", "maximum_observed_os_threads", "thread_probe_status", "thread_snapshot_count", "completed_stability_lengths", "current_stage", "current_cell_id", "current_length", "completed_origins_current_cell", "completed_replicates_current_length", "new_output_bytes_at_checkpoint", "private_numeric_output_bytes_at_checkpoint", "public_analysis_output_bytes_at_checkpoint"}
    resources = manifest["resources"]
    if type(resources) is not dict or (resources and set(resources) != resource_keys):
        raise ValueError("unknown resource field")
    if resources:
        if (resources["started_utc"] != manifest["started_utc"] or resources["measurement_point"] != "final_checkpoint_before_manifest" or resources["requested_numerical_threads"] != 1 or resources["completed_stability_lengths"] != [] or resources["current_length"] is not None or resources["completed_replicates_current_length"] != 0):
            raise ValueError("resource provenance mismatch")
        for key in ("elapsed_seconds", "peak_rss_bytes", "maximum_observed_os_threads"):
            if resources[key] is not None:
                _number(resources[key], nonnegative=True)
                if key != "elapsed_seconds" and (type(resources[key]) is not int or resources[key] <= 0):
                    raise ValueError("invalid measured resource")
        for key in ("thread_snapshot_count", "completed_origins_current_cell", "new_output_bytes_at_checkpoint", "private_numeric_output_bytes_at_checkpoint", "public_analysis_output_bytes_at_checkpoint"):
            if type(resources[key]) is not int or resources[key] < 0:
                raise ValueError("invalid resource counter")
        if resources["thread_probe_status"] not in ("PASS", "UNVERIFIED") or resources["current_stage"] not in ("initialization", "after_imports", "source_snapshot", "after_source", "revision_forecast", "before_output_writes", "final_manifest_checkpoint"):
            raise ValueError("invalid resource stage")
        if resources["current_cell_id"] not in (None, *("h"+str(h)+"_"+item[0] for h in (6, 24) for item in SETS)):
            raise ValueError("invalid resource cell")
        if resources["checkpoint_utc"] is not None and not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", resources["checkpoint_utc"]):
            raise ValueError("invalid resource timestamp")
    if manifest["environment"]["thread_requests"] != {name: "1" for name in THREAD_NAMES}:
        raise ValueError("thread request mismatch")
    if type(manifest["code"]) is not list:
        raise ValueError("manifest code mismatch")
    names = []
    for row in manifest["code"]:
        if set(row) != {"file_name", "sha256"} or row["file_name"] not in CODE_FILES or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError("manifest code hash mismatch")
        names.append(row["file_name"])
    if len(names) != len(set(names)):
        raise ValueError("duplicate code identity")
    artifact_names = []
    for row in manifest["artifacts"]:
        if (set(row) != {"file_name", "bytes", "sha256", "rows"} or row["file_name"] not in {n+".csv" for n in TABLE_COLUMNS}
                or type(row["bytes"]) is not int or row["bytes"] <= 0 or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])):
            raise ValueError("artifact identity mismatch")
        expected_rows = {"summary.csv": 30, "geometry.csv": 10, "comparisons.csv": 22, "monthly.csv": 26}
        if type(row["rows"]) is not int or row["rows"] != expected_rows[row["file_name"]]:
            raise ValueError("artifact rows mismatch")
        artifact_names.append(row["file_name"])
    if len(artifact_names) != len(set(artifact_names)):
        raise ValueError("duplicate artifact")
    if manifest["run_status"] == "COMPLETE":
        if (manifest["stop_code"] != "NONE" or any(v != "PASS" for v in manifest["checks"].values()) or set(names) != set(CODE_FILES)
                or set(artifact_names) != {n+".csv" for n in TABLE_COLUMNS}
                or manifest["evaluation"] != dict(origin_count=6625, first_source_index=11927, last_source_index=18551)
                or reference["summary_sha256"] is None or manifest["environment"]["numpy_version"] != "2.3.5"):
            raise ValueError("incomplete verification")
        validate_source_identity(manifest["source"])
        validate_measured_resources(manifest["resources"])


def write_manifest(manifest, public):
    validate_manifest(manifest)
    exclusive_write(public/"manifest.json", public_json_bytes(manifest))


def write_tables(bundle, public, spec):
    outputs = table_bytes(bundle, spec)
    if any((public/name).exists() or (public/name).is_symlink() for name in outputs):
        raise StudyStop("OUTPUT_INTEGRITY")
    artifacts = []
    for name, content in outputs.items():
        exclusive_write(public/name, content)
        if (public/name).read_bytes() != content:
            raise StudyStop("OUTPUT_INTEGRITY")
        artifacts.append(dict(file_name=name, bytes=len(content), sha256=hashlib.sha256(content).hexdigest(), rows=len(bundle[name[:-4]])))
    return artifacts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New attempt beneath this project's .scratch")
    args = parser.parse_args(argv)
    start, started_utc = ((PROCESS_STARTED_MONOTONIC, PROCESS_STARTED_UTC) if argv is None
                          else (time.monotonic(), utc_now()))
    public, private = new_attempt(args.output, ROOT)
    guard = RunGuard(start, started_utc, args.output, public, private)
    manifest = initial_manifest(started_utc, {})
    armed = False
    try:
        spec, old_spec = load_protocol(ROOT)
        manifest["checks"]["frozen_protocol"] = "PASS"
        hashes = {name: sha_file(ROOT/name) for name in CODE_FILES}
        manifest["code"] = [dict(file_name=name, sha256=digest) for name, digest in hashes.items()]
        arm_hard_deadline(600.-(time.monotonic()-start))
        armed = True
        if np.__version__ != "2.3.5":
            raise StudyStop("RUNTIME_UNAVAILABLE")
        guard(stage="after_imports")
        import study_data as data
        source = data.load_source(ROOT/".scratch/data/1hourNetPositionsKaggle.csv", old_spec["source"], fetch=False,
                                  remaining_seconds=guard.remaining_seconds, checkpoint=guard)
        validate_source_identity(source.identity)
        for key in ("accepted_csv_bytes", "accepted_csv_sha256", "source_verified", "acquisition_mode",
                    "request_performed_this_attempt", "local_validation_utc", "download"):
            manifest["source"][key] = source.identity[key]
        manifest["checks"]["source_identity"] = "PASS"
        guard.arrays(source)
        guard(stage="after_source")
        original_cells = [core.CellSpec.from_dict(c) for c in old_spec["cells"]]
        origins = core.common_origins(source.times, original_cells, old_spec["evaluation"]["cutoff_naive"])
        if not np.array_equal(origins, np.arange(11927, 18552)):
            raise ValueError("original common origin mismatch")
        manifest["evaluation"] = dict(origin_count=len(origins), first_source_index=int(origins[0]), last_source_index=int(origins[-1]))
        manifest["checks"]["origin_identity"] = "PASS"
        original_reference_sha256 = sha_file(ROOT/"results/summary.csv")
        manifest["original_reference"]["summary_sha256"] = original_reference_sha256
        with (ROOT/"results/summary.csv").open(newline="") as stream:
            original_reference = list(csv.DictReader(stream))
        bundle = compose(source.position, source.times, origins, spec, checkpoint=guard)
        for name in ("complete_pool_eligibility", "finite_scores", "geometry", "aggregate_identities"):
            manifest["checks"][name] = "PASS"
        validate_original_reference(bundle["summary"], original_reference)
        if sha_file(ROOT/"results/summary.csv") != original_reference_sha256:
            raise StudyStop("SPECIFICATION")
        manifest["checks"]["original_global_reference"] = "PASS"
        # Digests and source indices remain private; no origin-level public object.
        exclusive_write(private/"selection-evidence.json", public_json_bytes(bundle["private"]))
        guard.arrays(source, origins)
        guard(stage="before_output_writes")
        manifest["artifacts"] = write_tables(bundle, public, spec)
        manifest["checks"]["public_serialization"] = "PASS"
        load_protocol(ROOT)
        if hashes != {name: sha_file(ROOT/name) for name in CODE_FILES}:
            raise StudyStop("SPECIFICATION")
        manifest["checks"]["code_identity"] = "PASS"
        guard(stage="final_manifest_checkpoint")
        validate_measured_resources(guard.resources)
        manifest["checks"]["resources"] = "PASS"
        manifest.update(run_status="COMPLETE", stop_code="NONE", resources=dict(guard.resources))
        write_manifest(manifest, public)
        print(json.dumps(dict(run_status="COMPLETE", stop_code="NONE", elapsed_seconds=guard.resources["elapsed_seconds"],
                              peak_rss_bytes=guard.resources["peak_rss_bytes"], maximum_observed_os_threads=guard.resources["maximum_observed_os_threads"]), allow_nan=False))
        return 0
    except Exception as error:
        mark_failure(manifest, guard, error)
        try:
            write_manifest(manifest, public)
        except Exception:
            # If the output device/schema itself fails, retain an explicit safe
            # private stop record when possible and always emit sanitized stdout.
            try:
                exclusive_write(private/"stop.json", public_json_bytes(dict(run_status="INCOMPLETE", stop_code=manifest["stop_code"])))
            except Exception:
                pass
        print(json.dumps(dict(run_status="INCOMPLETE", stop_code=manifest["stop_code"])))
        return 1
    finally:
        if armed:
            signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except StudyStop as error:
        print(json.dumps(dict(run_status="INCOMPLETE", stop_code=error.code)))
        sys.exit(1)
