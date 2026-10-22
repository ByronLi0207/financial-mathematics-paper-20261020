#!/usr/bin/env python3
"""Render three pinned, aggregate-only conditional-study vector figures.

Document-only entry point:
    python -B build_conditional_figures.py --output .scratch/conditional-figure-<new-name>

The accepted evaluation-audit-02.json and exactly three public aggregate CSVs
are read. No observations, private arrays, forecasts, model fitting or inference
are read or run. Display arithmetic forms relative aggregate changes only;
source-native USD and USD millions are never pooled or added across sources.
The output directory must be a new direct .scratch/conditional-figure-* child.
The fixed basenames are staged for figures/ in the manuscript package.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parent
PUBLIC_RESULTS = PROJECT_ROOT / "results" / "revision-20261022"
AUDIT_NAME = "evaluation-audit-02.json"
AUDIT_BYTES = 19755
AUDIT_SHA256 = "0f44825f200e364bd0df3cecc9dc9175a45755fe17fd048e6ad9d238bd31288b"
INPUT_IDENTITIES = {
    "evaluation-summary.csv": {"bytes": 17416, "rows": 90,
        "sha256": "2988f6239b02c0c5d4637df8ef0881de78a3d52a845c38b3c8e3726871d8be15"},
    "paired-comparisons.csv": {"bytes": 26918, "rows": 98,
        "sha256": "a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9"},
    "paired-annual.csv": {"bytes": 102217, "rows": 388,
        "sha256": "5b0727af566cbfa935fba95c25cf2a7918dc073baa2daf8558d84984161bce40"},
}
SUMMARY_COLUMNS = (
    "source", "native_unit", "horizon", "window", "method", "parameter", "refit_step",
    "plain_knn_full_pool_fallback", "origin_count", "mean_pinball", "mean_capacity",
    "mean_extra_allowance", "strict_breach_count", "strict_breach_rate", "mean_positive_overrun",
    "conditional_mean_overrun", "conditional_overrun_denominator",
    "conditional_overrun_undefined_reason", "mean_unused_allowance",
)
PAIR_COLUMNS = (
    "contrast_id", "source", "native_unit", "horizon", "left_window", "left_method",
    "right_window", "right_method", "contrast_category", "declared_source_primary",
    "h24_legacy_contrast", "origin_count", "first_source_index", "last_source_index",
    "mean_pinball_left", "mean_pinball_right", "mean_pinball_difference",
    "relative_mean_loss_difference_percent", "relative_difference_undefined_reason",
    "mean_capacity_difference", "mean_positive_overrun_difference", "mean_unused_allowance_difference",
    "strict_breach_count_left", "strict_breach_count_right",
)
ANNUAL_COLUMNS = PAIR_COLUMNS[:11] + ("calendar_year",) + PAIR_COLUMNS[11:]
CONDITIONAL_METHODS = ("QR", "KNN", "SCALED_KNN")
SOURCES = ("fx_hourly", "nyfed_weekly")
SOURCE_META = {
    "fx_hourly": {"unit": "USD", "windows": (720, 2880), "refit": 24, "n": 6625,
                  "first": 11927, "last": 18551,
                  "years": ((2016, 6262, 11927, 18188), (2017, 363, 18189, 18551))},
    "nyfed_weekly": {"unit": "USD millions", "windows": (52, 260), "refit": 13, "n": 277,
                     "first": 405, "last": 681,
                     "years": ((2021, 52, 405, 456), (2022, 52, 457, 508),
                               (2023, 52, 509, 560), (2024, 52, 561, 612),
                               (2025, 53, 613, 665), (2026, 16, 666, 681))},
}
# Fixed validated parameter choices, not a new tuning menu or ranking.
SELECTED_PARAMETERS = {
    ("fx_hourly", 6, 720): ("0.01", "180", "360"),
    ("fx_hourly", 6, 2880): ("0.01", "180", "180"),
    ("fx_hourly", 24, 720): ("0.01", "180", "180"),
    ("fx_hourly", 24, 2880): ("0.001", "180", "180"),
    ("nyfed_weekly", 6, 52): ("0.1", "52", "52"),
    ("nyfed_weekly", 6, 260): ("0.001", "80", "80"),
    ("nyfed_weekly", 24, 52): ("0.001", "52", "40"),
    ("nyfed_weekly", 24, 260): ("0.1", "160", "160"),
}
PRIMARY_IDS = (
    "fx_hourly-h6-QR2880-minus-rolling_F720",
    "fx_hourly-h24-QR2880-minus-rolling_S720",
    "nyfed_weekly-h6-QR260-minus-frozen_F260",
)
FIGURE_NAMES = (
    "conditional-common-history.pdf", "conditional-primary-tradeoffs.pdf",
    "conditional-annual-primary.pdf",
)
PAGE_WIDTH = 841.8897637795277
PAGE_HEIGHT = 595.2755905511812
INK = "#203345"
MUTED = "#526372"
GRID = "#D7DEE3"
SOURCE_COLORS = {"fx_hourly": "#187A8B", "nyfed_weekly": "#7350A2"}
METHOD_LABELS = {"QR": "QR", "KNN": "KNN", "SCALED_KNN": "S-KNN"}
SHORT_CONTRAST_LABELS = ("FX H6 primary", "FX H24 legacy", "NY H6 primary")


@dataclass(frozen=True)
class CommonHistoryPoint:
    source: str
    native_unit: str
    horizon: int
    window: int
    method: str
    parameter: str
    origin_count: int
    loss_percent: float
    full_pool: bool


@dataclass(frozen=True)
class TradeoffPoint:
    contrast_id: str
    source: str
    native_unit: str
    origin_count: int
    loss_percent: float
    breach_pp: float
    overrun_percent: float
    unused_percent: float


@dataclass(frozen=True)
class AnnualPoint:
    contrast_id: str
    source: str
    native_unit: str
    year: int
    origin_count: int
    loss_percent: float
    partial: bool


@dataclass(frozen=True)
class DisplayData:
    common_history: tuple[CommonHistoryPoint, ...]
    tradeoffs: tuple[TradeoffPoint, ...]
    annual: tuple[AnnualPoint, ...]


def relative_change(left: float, right: float):
    """100*(left-right)/right for nonnegative aggregates; zero reference is undefined."""
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool)
               and math.isfinite(x) and x >= 0 for x in (left, right)):
        raise ValueError("relative changes require finite nonnegative aggregates")
    if right == 0:
        return None
    value = ((left - right) / right) * 100.0
    if not math.isfinite(value):
        raise ValueError("relative aggregate change is unrepresentable")
    return value


def breach_rate_change(left: int, right: int, origin_count: int) -> float:
    """Difference of paired breach proportions, displayed in percentage points."""
    if (any(type(x) is not int for x in (left, right, origin_count)) or origin_count <= 0
            or not 0 <= left <= origin_count or not 0 <= right <= origin_count):
        raise ValueError("valid paired breach counts and a positive common N are required")
    return ((left - right) / origin_count) * 100.0


def _finite(row, key, nonnegative=False):
    try:
        value = float(row[key])
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError(f"invalid aggregate number: {key}") from exc
    if not math.isfinite(value) or (nonnegative and value < 0):
        raise ValueError(f"nonfinite or invalid aggregate number: {key}")
    return value


def _integer(row, key):
    value = row.get(key)
    if not isinstance(value, str) or not re.fullmatch(r"0|[1-9][0-9]*", value):
        raise ValueError(f"invalid unsigned aggregate integer: {key}")
    return int(value)


def _close(actual, expected, label):
    if not math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-7):
        raise ValueError(f"inconsistent aggregate arithmetic: {label}")


def _columns(row, columns):
    if set(row) != set(columns) or any(not isinstance(value, str) for value in row.values()):
        raise ValueError("aggregate columns or cell types differ")


def _summary_key(row):
    return (row["source"], _integer(row, "horizon"), _integer(row, "window"), row["method"])


def _summary_expectations():
    expected = {}
    for source in SOURCES:
        for horizon in (6, 24):
            for window in SOURCE_META[source]["windows"]:
                for method, parameter in zip(CONDITIONAL_METHODS, SELECTED_PARAMETERS[source, horizon, window]):
                    expected[source, horizon, window, method] = parameter
                for method in ("rolling_F", "rolling_S", "rolling_K", "frozen_F", "frozen_S", "frozen_K"):
                    expected[source, horizon, window, method] = ""
                if source == "nyfed_weekly" or window == 720:
                    count = 360 if source == "fx_hourly" else (40 if window == 52 else 80)
                    for method in ("one_state_F", "one_state_S", "one_state_K"):
                        expected[source, horizon, window, method] = str(count)
    return expected


def _index_summary(rows):
    expected = _summary_expectations()
    if len(rows) != 90:
        raise ValueError("summary must retain all 90 accepted rows")
    indexed = {}
    for row in rows:
        _columns(row, SUMMARY_COLUMNS)
        key = _summary_key(row)
        if key not in expected or key in indexed:
            raise ValueError("missing, duplicated or unknown summary identity")
        source, _, window, method = key
        meta = SOURCE_META[source]
        full_pool = source == "nyfed_weekly" and window == 52 and method == "KNN"
        if (row["native_unit"] != meta["unit"] or row["parameter"] != expected[key]
                or row["plain_knn_full_pool_fallback"] != str(full_pool)
                or _integer(row, "origin_count") != meta["n"]
                or _integer(row, "refit_step") != (1 if method.startswith(("rolling_", "one_state_")) else meta["refit"])):
            raise ValueError("summary source unit, menu, fallback, N or refit label differs")
        for name in ("mean_pinball", "mean_capacity", "mean_extra_allowance", "strict_breach_rate",
                     "mean_positive_overrun", "mean_unused_allowance"):
            _finite(row, name, nonnegative=True)
        count = _integer(row, "strict_breach_count")
        if count > meta["n"] or _integer(row, "conditional_overrun_denominator") != count:
            raise ValueError("summary breach or conditional-overrun denominator differs")
        _close(_finite(row, "strict_breach_rate"), count / meta["n"], "breach rate")
        if count:
            if row["conditional_overrun_undefined_reason"] != "":
                raise ValueError("positive breach denominator cannot be undefined")
            conditional = _finite(row, "conditional_mean_overrun", nonnegative=True)
            _close(conditional * (count / meta["n"]), _finite(row, "mean_positive_overrun"),
                   "conditional versus unconditional overrun")
        elif row["conditional_mean_overrun"] != "" or not row["conditional_overrun_undefined_reason"]:
            raise ValueError("zero breach denominator must be explicitly undefined")
        _close(_finite(row, "mean_pinball"),
               .95 * _finite(row, "mean_positive_overrun") + .05 * _finite(row, "mean_unused_allowance"),
               "pinball versus overrun/unused decomposition")
        indexed[key] = row
    if set(indexed) != set(expected):
        raise ValueError("summary identity inventory differs")
    return indexed


def _pair_identity(source, horizon, left_window, left_method, right_window, right_method, category):
    contrast_id = f"{source}-h{horizon}-{left_method}{left_window}-minus-{right_method}{right_window}"
    return {"contrast_id": contrast_id, "source": source, "native_unit": SOURCE_META[source]["unit"],
            "horizon": str(horizon), "left_window": str(left_window), "left_method": left_method,
            "right_window": str(right_window), "right_method": right_method, "contrast_category": category,
            "declared_source_primary": str(contrast_id in (PRIMARY_IDS[0], PRIMARY_IDS[2])),
            "h24_legacy_contrast": str(contrast_id == PRIMARY_IDS[1])}


def _pair_expectations():
    expected = {}
    for source in SOURCES:
        for horizon in (6, 24):
            for window in SOURCE_META[source]["windows"]:
                for method in CONDITIONAL_METHODS:
                    for reference in ("frozen_F", "frozen_S", "frozen_K"):
                        row = _pair_identity(source, horizon, window, method, window, reference, "common_history")
                        expected[row["contrast_id"]] = row
                for method in ("F", "S", "K"):
                    row = _pair_identity(source, horizon, window, "rolling_" + method, window,
                                         "frozen_" + method, "update_frequency")
                    expected[row["contrast_id"]] = row
    for horizon, reference, category in ((6, "rolling_F", "primary_contrast"),
                                          (24, "rolling_S", "h24_legacy_contrast")):
        row = _pair_identity("fx_hourly", horizon, 2880, "QR", 720, reference, category)
        expected[row["contrast_id"]] = row
    return expected


def _validate_pair(row, expected, annual=False):
    _columns(row, ANNUAL_COLUMNS if annual else PAIR_COLUMNS)
    if any(row[key] != value for key, value in expected.items()):
        raise ValueError("paired contrast identity, unit or designation differs")
    meta = SOURCE_META[row["source"]]
    if annual:
        years = {year: (count, first, last) for year, count, first, last in meta["years"]}
        year = _integer(row, "calendar_year")
        if year not in years:
            raise ValueError("annual year differs from accepted source years")
        count, first, last = years[year]
    else:
        count, first, last = meta["n"], meta["first"], meta["last"]
    if tuple(_integer(row, key) for key in ("origin_count", "first_source_index", "last_source_index")) != (count, first, last):
        raise ValueError("paired origin count or boundaries differ")
    left = _finite(row, "mean_pinball_left", True)
    right = _finite(row, "mean_pinball_right", True)
    _close(_finite(row, "mean_pinball_difference"), left - right, "paired loss difference")
    percentage = relative_change(left, right)
    if percentage is None:
        if row["relative_mean_loss_difference_percent"] != "" or not row["relative_difference_undefined_reason"]:
            raise ValueError("zero-reference relative loss must be explicitly undefined")
    else:
        if row["relative_difference_undefined_reason"]:
            raise ValueError("positive-reference relative loss cannot be undefined")
        _close(_finite(row, "relative_mean_loss_difference_percent"), percentage, "relative loss")
    for key in ("mean_capacity_difference", "mean_positive_overrun_difference", "mean_unused_allowance_difference"):
        _finite(row, key)
    if any(_integer(row, key) > count for key in ("strict_breach_count_left", "strict_breach_count_right")):
        raise ValueError("paired breach count exceeds common N")


def _index_pairs(rows, summary):
    expected = _pair_expectations()
    if len(rows) != 98:
        raise ValueError("paired table must retain all 98 accepted contrasts")
    indexed = {}
    for row in rows:
        contrast_id = row.get("contrast_id")
        if contrast_id not in expected or contrast_id in indexed:
            raise ValueError("missing, duplicated or unknown paired contrast")
        _validate_pair(row, expected[contrast_id])
        keys = [(row["source"], _integer(row, "horizon"), _integer(row, side + "_window"), row[side + "_method"])
                for side in ("left", "right")]
        left, right = (summary[key] for key in keys)
        for side, reference in (("left", left), ("right", right)):
            _close(_finite(row, "mean_pinball_" + side), _finite(reference, "mean_pinball"), "paired/summary loss")
            if row["strict_breach_count_" + side] != reference["strict_breach_count"]:
                raise ValueError("paired/summary breach counts differ")
        for pair_column, summary_column in (("mean_capacity_difference", "mean_capacity"),
                                            ("mean_positive_overrun_difference", "mean_positive_overrun"),
                                            ("mean_unused_allowance_difference", "mean_unused_allowance")):
            _close(_finite(row, pair_column), _finite(left, summary_column) - _finite(right, summary_column),
                   "paired/summary " + summary_column)
        indexed[contrast_id] = row
    if set(indexed) != set(expected):
        raise ValueError("paired identity inventory differs")
    return indexed


def _index_annual(rows, paired):
    expected = _pair_expectations()
    inventory = {(contrast_id, year) for contrast_id, identity in expected.items()
                 for year, _, _, _ in SOURCE_META[identity["source"]]["years"]}
    if len(rows) != 388:
        raise ValueError("annual table must retain all 388 accepted rows")
    indexed = {}
    for row in rows:
        key = (row.get("contrast_id"), _integer(row, "calendar_year"))
        if key not in inventory or key in indexed:
            raise ValueError("missing, duplicated or unknown annual identity")
        _validate_pair(row, expected[key[0]], annual=True)
        indexed[key] = row
    if set(indexed) != inventory:
        raise ValueError("annual identity inventory differs")
    # Reconcile within each source/contrast only. Annual percentages are never averaged.
    for contrast_id, overall in paired.items():
        parts = [indexed[contrast_id, year] for year, _, _, _ in SOURCE_META[overall["source"]]["years"]]
        total = sum(_integer(row, "origin_count") for row in parts)
        if total != _integer(overall, "origin_count"):
            raise ValueError("annual N does not reconcile to the paired total")
        for key in ("mean_pinball_left", "mean_pinball_right", "mean_pinball_difference",
                    "mean_capacity_difference", "mean_positive_overrun_difference", "mean_unused_allowance_difference"):
            mean = math.fsum(_finite(row, key) * (_integer(row, "origin_count") / total) for row in parts)
            _close(mean, _finite(overall, key), "annual count-weighted " + key)
        for key in ("strict_breach_count_left", "strict_breach_count_right"):
            if sum(_integer(row, key) for row in parts) != _integer(overall, key):
                raise ValueError("annual breach counts do not reconcile")
    return indexed


def display_data(summary_rows, pair_rows, annual_rows) -> DisplayData:
    """Validate the full accepted inventories, then extract the fixed 24/3/10 display objects."""
    summary = _index_summary(summary_rows)
    paired = _index_pairs(pair_rows, summary)
    annual = _index_annual(annual_rows, paired)
    common = []
    for source in SOURCES:
        for horizon in (6, 24):
            for window in SOURCE_META[source]["windows"]:
                for method in CONDITIONAL_METHODS:
                    selected = summary[source, horizon, window, method]
                    contrast_id = f"{source}-h{horizon}-{method}{window}-minus-frozen_F{window}"
                    value = _finite(paired[contrast_id], "relative_mean_loss_difference_percent")
                    full_pool = selected["plain_knn_full_pool_fallback"] == "True"
                    if full_pool and value != 0.0:
                        raise ValueError("declared full-pool identity is not exactly zero")
                    common.append(CommonHistoryPoint(source, SOURCE_META[source]["unit"], horizon, window,
                        method, selected["parameter"], SOURCE_META[source]["n"], value, full_pool))
    tradeoffs = []
    annual_points = []
    for contrast_id in PRIMARY_IDS:
        row = paired[contrast_id]
        source = row["source"]
        horizon = _integer(row, "horizon")
        left, right = [summary[source, horizon, _integer(row, side + "_window"), row[side + "_method"]]
                       for side in ("left", "right")]
        ratios = [relative_change(_finite(left, key), _finite(right, key))
                  for key in ("mean_positive_overrun", "mean_unused_allowance")]
        if any(value is None for value in ratios):
            raise ValueError("a fixed tradeoff reference unexpectedly has a zero denominator")
        tradeoffs.append(TradeoffPoint(contrast_id, source, row["native_unit"], _integer(row, "origin_count"),
            _finite(row, "relative_mean_loss_difference_percent"),
            breach_rate_change(_integer(row, "strict_breach_count_left"),
                               _integer(row, "strict_breach_count_right"), _integer(row, "origin_count")),
            ratios[0], ratios[1]))
        for year, _, _, _ in SOURCE_META[source]["years"]:
            part = annual[contrast_id, year]
            annual_points.append(AnnualPoint(contrast_id, source, row["native_unit"], year,
                _integer(part, "origin_count"), _finite(part, "relative_mean_loss_difference_percent"),
                (source, year) in (("fx_hourly", 2017), ("nyfed_weekly", 2026))))
    if (len(common), len(tradeoffs), len(annual_points)) != (24, 3, 10):
        raise ValueError("display inventory differs from the fixed 24/3/10 objects")
    return DisplayData(tuple(common), tuple(tradeoffs), tuple(annual_points))


def _read_regular(path, expected_bytes):
    if path.is_symlink() or not path.is_file() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError("public input must be a regular file without symlink ancestors")
    if path.stat().st_size != expected_bytes:
        raise ValueError("accepted public input byte count differs")
    return path.read_bytes()


def load_verified_results(directory=PUBLIC_RESULTS):
    """Pin the audit, its export declarations, CSV bytes/hashes, schemas and scientific identities."""
    directory = Path(directory).absolute()
    raw = _read_regular(directory / AUDIT_NAME, AUDIT_BYTES)
    if hashlib.sha256(raw).hexdigest() != AUDIT_SHA256:
        raise ValueError("accepted evaluation-audit-02 hash differs")
    audit = json.loads(raw)
    if (audit["status"] != "VERIFIED" or audit["evaluation_cell_count"] != 24
            or audit["reference_cell_count"] != 8 or audit["summary_rows"] != 90
            or audit["paired_rows"] != 98 or audit["paired_annual_rows"] != 388
            or audit["full_pool_identity_checks"] != 2):
        raise ValueError("evaluation audit is not the accepted complete inventory")
    parsed = {}
    for name, expected in INPUT_IDENTITIES.items():
        entries = [row for row in audit["exports"] if row["path"] == name]
        if (len(entries) != 1 or entries[0]["bytes"] != expected["bytes"]
                or entries[0]["sha256"] != expected["sha256"]):
            raise ValueError("accepted audit export identity differs")
        raw = _read_regular(directory / name, expected["bytes"])
        if hashlib.sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError("accepted aggregate CSV hash differs")
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
        columns = {"evaluation-summary.csv": SUMMARY_COLUMNS, "paired-comparisons.csv": PAIR_COLUMNS,
                   "paired-annual.csv": ANNUAL_COLUMNS}[name]
        if tuple(reader.fieldnames or ()) != columns:
            raise ValueError("aggregate CSV header differs")
        rows = list(reader)
        if len(rows) != expected["rows"]:
            raise ValueError("aggregate CSV row count differs")
        parsed[name] = rows
    identity = {"accepted_audit": {"path": AUDIT_NAME, "bytes": AUDIT_BYTES, "sha256": AUDIT_SHA256},
                "inputs": {name: dict(value) for name, value in INPUT_IDENTITIES.items()}}
    return display_data(parsed["evaluation-summary.csv"], parsed["paired-comparisons.csv"],
                        parsed["paired-annual.csv"]), identity


@dataclass(frozen=True)
class DisplayScale:
    lower: float
    upper: float
    left: float
    right: float

    def position(self, value):
        if not math.isfinite(value) or not self.lower <= value <= self.upper:
            raise ValueError("display value outside finite axis")
        return self.left + ((value - self.lower) / (self.upper - self.lower)) * (self.right - self.left)


def _scale(values, left, right):
    values = tuple(values)
    if not values or not all(math.isfinite(value) for value in values) or right - left < 80:
        raise ValueError("finite nonempty values and an adequate plot width are required")
    lower, upper = min(0.0, *values), max(0.0, *values)
    span = upper - lower
    padding = span * .14 if span else 1.0
    lower, upper = lower - padding, upper + padding
    if not all(math.isfinite(value) for value in (lower, upper, upper - lower)):
        raise ValueError("display axis is unrepresentable")
    return DisplayScale(lower, upper, left, right)


def _layout(kind, filename, title):
    return {"kind": kind, "file_name": filename, "public_path": "figures/" + filename,
            "title": title, "texts": [], "lines": [], "points": [], "axes": [],
            "scope": "Descriptive aggregates of overlapping issue windows; no confidence intervals or inference",
            "unit_policy": "Within-source ratios and paired percentage points only; native units are not pooled"}


def _text(layout, x, y, value, size=10, color=INK, bold=False, align="left", max_width=None):
    layout["texts"].append({"x": x, "y": y, "value": value, "size": size, "color": color,
                            "bold": bold, "align": align, "max_width": max_width})


def _line(layout, x1, y1, x2, y2, color=GRID, width=.6):
    layout["lines"].append({"x1": x1, "y1": y1, "x2": x2, "y2": y2,
                            "color": color, "width": width})


def _axis(layout, scale, bottom, top):
    layout["axes"].append({**asdict(scale), "bottom": bottom, "top": top})
    zero = scale.position(0.0)
    # Preserve exact endpoints: arithmetic interpolation of i=4 can round past upper.
    ticks = [scale.lower] + [scale.lower + (scale.upper - scale.lower) * i / 4
                             for i in range(1, 4)] + [scale.upper]
    ticks = [value for value in ticks if abs(scale.position(value) - zero) >= 33]
    for value in sorted(ticks + [0.0]):
        x = scale.position(value)
        _line(layout, x, bottom, x, top, MUTED if value == 0 else GRID, 1 if value == 0 else .5)
        _line(layout, x, bottom, x, bottom - 3, MUTED)
        _text(layout, x, bottom - 15, "0" if value == 0 else f"{value:+.1f}",
              7.3, MUTED, align="center")
    _line(layout, scale.left, bottom, scale.right, bottom, MUTED)


def _point(layout, scale, y, value, source, color=None, shape="circle", **metadata):
    axis = layout["axes"][-1]
    layout["points"].append({**metadata, "source": source, "value": value, "x": scale.position(value),
        "y": y, "zero_x": scale.position(0.0), "radius": 3.5,
        "color": color or SOURCE_COLORS[source], "shape": shape,
        "plot_bounds": [scale.left, axis["bottom"], scale.right, axis["top"]],
        "axis_limits": [scale.lower, scale.upper]})


def _header(layout, subtitle):
    _text(layout, 42, 551, layout["title"], 18, bold=True, max_width=760)
    _text(layout, 42, 529, subtitle, 10.5, MUTED, max_width=760)
    _line(layout, 42, 513, 802, 513, INK, 1)


def _common_layout(data):
    layout = _layout("common_history", FIGURE_NAMES[0], "Conditional forecasts against matched historical headrooms")
    _header(layout, "Mean loss change (%) relative to own W/H frozen F | negative is lower loss")
    for source, offset, title in (("fx_hourly", 0, "FX client-flow archive"),
                                   ("nyfed_weekly", 400, "Treasury-bill dealer aggregate")):
        points = [point for point in data.common_history if point.source == source]
        if len(points) != 12:
            raise ValueError("each source panel requires all 12 conditional configurations")
        _text(layout, 43 + offset, 485, title, 12, bold=True, max_width=359)
        _text(layout, 43 + offset, 467,
              f"Native: {SOURCE_META[source]['unit']} | N={SOURCE_META[source]['n']} | 12 configurations",
              8.4, MUTED, max_width=359)
        _text(layout, 43 + offset, 449, "H / W / method", 8.2, MUTED)
        _text(layout, 402 + offset, 449, "Loss change (%)", 8.2, MUTED, align="right")
        scale = _scale([point.loss_percent for point in points], 147 + offset, 326 + offset)
        _axis(layout, scale, 168, 443)
        for index, point in enumerate(points):
            y = 432 - index * 22.5
            method = METHOD_LABELS[point.method] + ("*" if point.full_pool else "")
            _text(layout, 43 + offset, y - 3, f"{point.horizon} / {point.window} / {method}",
                  8.8, max_width=100)
            _point(layout, scale, y, point.loss_percent, source,
                   shape={"QR": "square", "KNN": "circle", "SCALED_KNN": "diamond"}[point.method],
                   horizon=point.horizon, window=point.window, method=point.method, full_pool=point.full_pool,
                   origin_count=point.origin_count, native_unit=point.native_unit)
            _text(layout, 402 + offset, y - 3, f"{point.loss_percent:+.2f}", 9,
                  SOURCE_COLORS[source], align="right", max_width=66)
            if index in (2, 5, 8):
                _line(layout, 43 + offset, y - 11, 402 + offset, y - 11, "#E8ECEF", .4)
        _text(layout, 236 + offset, 130, "Relative mean pinball loss (%)", 8.8, MUTED, align="center")
    _line(layout, 422, 132, 422, 496, GRID)
    _text(layout, 42, 108, "QR: ridge quantile regression | KNN: local headrooms | S-KNN: scale-adjusted local headrooms", 9, MUTED)
    _text(layout, 42, 91, "* KNN uses the full pool: exact 0.00% at NY W=52 for both H; these rows show no feature-membership gain.", 9, MUTED)
    _text(layout, 42, 74, "H counts records. Each panel has its own axis range; no native monetary totals are combined.", 9, MUTED)
    _text(layout, 42, 57, "Descriptive, overlapping response windows. No confidence intervals; the FX interval was previously inspected.", 9, MUTED)
    _text(layout, 42, 36, "Source: accepted evaluation-audit-02 exports | all selected conditional configurations retained", 8, MUTED)
    return layout


def _tradeoff_layout(data):
    layout = _layout("primary_tradeoffs", FIGURE_NAMES[1], "Three fixed comparisons: loss and breach tradeoffs")
    _header(layout, "Each point is QR minus its stated reference | aggregate-relative changes; no native-dollar pooling")
    metrics = (("loss_percent", "Mean pinball loss change (%)", 0, 0),
               ("breach_pp", "Strict breach rate (percentage points)", 400, 0),
               ("overrun_percent", "Mean positive overrun change (%)", 0, -172),
               ("unused_percent", "Mean unused allowance change (%)", 400, -172))
    for metric, title, offset_x, offset_y in metrics:
        _text(layout, 43 + offset_x, 485 + offset_y, title, 11.5, bold=True, max_width=359)
        scale = _scale([getattr(point, metric) for point in data.tradeoffs], 190 + offset_x, 326 + offset_x)
        _axis(layout, scale, 365 + offset_y, 460 + offset_y)
        for index, point in enumerate(data.tradeoffs):
            y = 446 - index * 30 + offset_y
            value = getattr(point, metric)
            _text(layout, 43 + offset_x, y - 3, SHORT_CONTRAST_LABELS[index], 9.5, max_width=140)
            # Color identifies source only. Unused allowance always uses neutral grey.
            color = MUTED if metric == "unused_percent" else SOURCE_COLORS[point.source]
            _point(layout, scale, y, value, point.source, color=color, metric=metric,
                   contrast_id=point.contrast_id, origin_count=point.origin_count,
                   native_unit=point.native_unit)
            _text(layout, 402 + offset_x, y - 3, f"{value:+.2f}", 9.5, color, align="right", max_width=64)
    _line(layout, 422, 178, 422, 495, GRID)
    _text(layout, 42, 145, "FX H6 primary: QR W=2880 vs rolling F W=720 | N=6625", 9, SOURCE_COLORS["fx_hourly"])
    _text(layout, 42, 129, "FX H24 legacy: QR W=2880 vs rolling S W=720 | N=6625", 9, SOURCE_COLORS["fx_hourly"])
    _text(layout, 42, 113, "NY H6 primary: QR W=260 vs frozen F W=260 | N=277", 9, SOURCE_COLORS["nyfed_weekly"])
    _text(layout, 42, 88, "Relative (%) = 100*(QR-reference)/reference; breach change uses the same paired N in percentage points.", 9, MUTED)
    _text(layout, 42, 72, "Mean overrun averages max(P-C,0) across all origins. Unused sign is descriptive; no preference coloring.", 9, MUTED)
    _text(layout, 42, 56, "Descriptive, overlapping windows. No confidence intervals; a lower score is not an operational saving.", 9, MUTED)
    _text(layout, 42, 35, "Source: accepted paired-comparisons.csv plus matching evaluation-summary.csv aggregates", 8, MUTED)
    return layout


def _annual_layout(data):
    layout = _layout("annual_primary", FIGURE_NAMES[2], "Annual loss contrasts for the same three comparisons")
    _header(layout, "Relative mean loss (%) | negative is lower loss | annual origin counts shown; partial years retained")
    scale = _scale([point.loss_percent for point in data.annual], 235, 676)
    settings = (
        (PRIMARY_IDS[0], "FX H6 PRIMARY | QR W=2880 vs rolling F W=720", 489, (462, 438), 423, 473),
        (PRIMARY_IDS[1], "FX H24 LEGACY | QR W=2880 vs rolling S W=720", 383, (356, 332), 317, 367),
        (PRIMARY_IDS[2], "NY H6 PRIMARY | QR W=260 vs frozen F W=260", 277,
         (250, 226, 202, 178, 154, 130), 115, 261),
    )
    for contrast_id, title, title_y, ys, bottom, top in settings:
        points = [point for point in data.annual if point.contrast_id == contrast_id]
        if len(points) != len(ys):
            raise ValueError("annual panel inventory differs")
        _text(layout, 43, title_y, title, 11, bold=True, max_width=759)
        _axis(layout, scale, bottom, top)
        for point, y in zip(points, ys):
            label = f"{point.year}" + (" partial" if point.partial else "") + f"  N={point.origin_count}"
            _text(layout, 43, y - 3, label, 10, max_width=183)
            _point(layout, scale, y, point.loss_percent, point.source,
                   shape="diamond" if point.partial else "circle", contrast_id=point.contrast_id,
                   year=point.year, origin_count=point.origin_count, partial=point.partial,
                   native_unit=point.native_unit)
            _text(layout, 802, y - 3, f"{point.loss_percent:+.2f}%", 10,
                  SOURCE_COLORS[point.source], align="right", max_width=95)
    _text(layout, 42, 72, "Shared percent axis; source-native units differ. Annual ratios are computed within each stated contrast.", 9, MUTED)
    _text(layout, 42, 56, "N counts overlapping origins, not independent replicates. No confidence intervals or error bars.", 9, MUTED)
    _text(layout, 42, 35, "Source: accepted paired-annual.csv | diamonds mark 2017 / 2026 partial years; no years are omitted", 8, MUTED)
    return layout


def figure_layouts(data: DisplayData):
    """Pure display geometry; no PDF file or Canvas is created."""
    return [_common_layout(data), _tradeoff_layout(data), _annual_layout(data)]


def validate_layout(layout):
    """Check real font widths and all display geometry without constructing a PDF."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    for item in layout["texts"]:
        text, size = item["value"], item["size"]
        if not isinstance(text, str) or not text.isascii() or size <= 0:
            raise ValueError("figure labels require positive-size ASCII text")
        width = stringWidth(text, "Helvetica-Bold" if item["bold"] else "Helvetica", size)
        left = item["x"] - (width if item["align"] == "right" else width / 2 if item["align"] == "center" else 0)
        if (item["max_width"] is not None and width > item["max_width"]
                or not 0 <= left <= left + width <= PAGE_WIDTH
                or not size <= item["y"] <= PAGE_HEIGHT - size):
            raise ValueError(f"figure text exceeds page or column: {text}")
    for point in layout["points"]:
        left, bottom, right, top = point["plot_bounds"]
        radius = point["radius"]
        if not (left + radius < point["x"] < right - radius
                and bottom + radius < point["y"] < top - radius
                and (point["x"] < point["zero_x"]) == (point["value"] < 0)
                and (point["x"] > point["zero_x"]) == (point["value"] > 0)):
            raise ValueError("figure marker clips the plot or changes sign")
    for item in layout["lines"]:
        if not (0 <= min(item["x1"], item["x2"]) <= max(item["x1"], item["x2"]) <= PAGE_WIDTH
                and 0 <= min(item["y1"], item["y2"]) <= max(item["y1"], item["y2"]) <= PAGE_HEIGHT):
            raise ValueError("figure line exceeds the page")
    return layout


def validate_output_directory(output):
    """Validate an exclusive staging destination without creating it or importing Canvas."""
    path = Path(output)
    if ".." in path.parts:
        raise ValueError("output traversal is not allowed")
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    scratch = PROJECT_ROOT / ".scratch"
    if path.parent != scratch or not re.fullmatch(r"conditional-figure-[A-Za-z0-9][A-Za-z0-9-]*", path.name):
        raise ValueError("output must be a new direct .scratch/conditional-figure-* directory")
    if not scratch.is_dir() or scratch.is_symlink() or any(parent.is_symlink() for parent in scratch.parents):
        raise ValueError("output parent must be the regular task scratch directory")
    if os.path.lexists(path):
        raise FileExistsError("output already exists; overwrite is not allowed")
    return path


def _render(canvas, layout):
    from reportlab.lib.colors import HexColor
    for item in layout["lines"]:
        canvas.setStrokeColor(HexColor(item["color"]))
        canvas.setLineWidth(item["width"])
        canvas.line(item["x1"], item["y1"], item["x2"], item["y2"])
    for point in layout["points"]:
        x, y, radius = point["x"], point["y"], point["radius"]
        canvas.setFillColor(HexColor(point["color"]))
        if point["shape"] == "square":
            canvas.rect(x - radius, y - radius, radius * 2, radius * 2, stroke=0, fill=1)
        elif point["shape"] == "diamond":
            path = canvas.beginPath()
            path.moveTo(x, y + radius)
            path.lineTo(x + radius, y)
            path.lineTo(x, y - radius)
            path.lineTo(x - radius, y)
            path.close()
            canvas.drawPath(path, stroke=0, fill=1)
        else:
            canvas.circle(x, y, radius, stroke=0, fill=1)
    for item in layout["texts"]:
        canvas.setFont("Helvetica-Bold" if item["bold"] else "Helvetica", item["size"])
        canvas.setFillColor(HexColor(item["color"]))
        method = {"left": canvas.drawString, "right": canvas.drawRightString,
                  "center": canvas.drawCentredString}[item["align"]]
        method(item["x"], item["y"], item["value"])


def _os_threads():
    if sys.platform == "darwin":
        result = subprocess.run(["ps", "-M", "-p", str(os.getpid())], check=True,
                                capture_output=True, text=True, timeout=3)
        count = len([line for line in result.stdout.splitlines()[1:] if line.strip()])
    else:
        count = len(list(Path("/proc/self/task").iterdir()))
    if count < 1:
        raise RuntimeError("OS thread measurement is unavailable")
    return count


class _RenderBudget:
    def __init__(self):
        self.started = time.monotonic()
        self.maximum_threads = 0
        self.samples = 0

    def sample(self):
        self.maximum_threads = max(self.maximum_threads, _os_threads())
        self.samples += 1
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss_bytes = int(rss if sys.platform == "darwin" else rss * 1024)
        elapsed = time.monotonic() - self.started
        if elapsed >= 600 or rss_bytes >= 2 * 1024 ** 3 or self.maximum_threads > 2:
            raise RuntimeError("document-render resource budget exceeded")
        return {"elapsed_seconds": elapsed, "peak_rss_bytes": rss_bytes,
                "maximum_observed_os_threads": self.maximum_threads,
                "thread_snapshot_count": self.samples, "requested_numerical_threads": 1}


def build_figures(output):
    """Create exactly three vector PDFs plus a provenance/geometry/resource receipt."""
    budget = _RenderBudget()
    budget.sample()
    data, inputs = load_verified_results()
    layouts = [validate_layout(layout) for layout in figure_layouts(data)]
    directory = validate_output_directory(output)
    directory.mkdir(mode=0o700)
    # Keep transitive document-library imports inside the standing thread budget.
    for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
                     "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[variable] = "1"
    from reportlab.pdfgen.canvas import Canvas
    report = {"artifact_schema_version": 1, "purpose": "aggregate-only conditional-study document figures",
              **inputs, "display_inventory": {"common_history": 24, "tradeoff_comparisons": 3, "annual": 10},
              "artifacts": {}, "display_layouts": layouts}
    for layout in layouts:
        path = directory / layout["file_name"]
        with path.open("xb") as stream:
            canvas = Canvas(stream, pagesize=(PAGE_WIDTH, PAGE_HEIGHT), invariant=1, pageCompression=1)
            canvas.setTitle(layout["title"])
            canvas.setAuthor("")
            canvas.setSubject(layout["scope"] + "; " + layout["unit_policy"])
            _render(canvas, layout)
            canvas.showPage()
            canvas.save()
        raw = path.read_bytes()
        report["artifacts"][path.name] = {"public_path": layout["public_path"], "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "pages": 1, "vector_only": True,
            "displayed_point_count": len(layout["points"])}
        budget.sample()
    report["resources"] = budget.sample()
    with (directory / "artifact-identity.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", required=True, help="new direct .scratch/conditional-figure-* directory")
    arguments = parser.parse_args(argv)
    try:
        report = build_figures(arguments.output)
    except (ValueError, FileExistsError, RuntimeError, OSError) as exc:
        parser.exit(2, f"conditional figure build rejected: {exc}\n")
    print(json.dumps({"output_directory": str(Path(arguments.output).absolute()),
                      "artifacts": report["artifacts"], "resources": report["resources"]}, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
