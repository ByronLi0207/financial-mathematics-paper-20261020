#!/usr/bin/env python3
"""Restyle all seven accepted original paired means without rerunning forecasts.

Reads only results/run-manifest.json and results/paired-comparison.csv, whose
exact accepted identities are pinned below. The sole numerical transformation
is USD to USD million for display. The original figure files stay unchanged.
Output must be a new direct .scratch/revision-figure-* directory.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import io
import json
from pathlib import Path

from build_revision_figures import (
    INK, MUTED, PAGE_HEIGHT, PAGE_WIDTH, MoneyScale, _RenderBudget,
    _axis, _columns, _finite, _line, _marker, _new_output_directory,
    _read_regular, _text, money_scale,
)

PROJECT_ROOT = Path(__file__).resolve().parent
PUBLIC_RESULTS = PROJECT_ROOT / "results"
MANIFEST_SHA256 = "dc8f031892fb3794e5b6476d6bfcfe7e4f7745fbc16ca56c0697101db1dd14bc"
TABLE_IDENTITY = {"bytes": 1657, "rows": 7,
                  "sha256": "f41325d5090b81c0251ed7dfe290bca42dc5e2bc690ff753b3673b72c7cd9adf"}
FIGURE_NAME = "revision-original-contrasts.pdf"
COLUMNS = (
    "cell_id", "horizon", "window", "tau_numerator", "tau_denominator", "rank",
    "origin_count", "mean_pinball_difference", "relative_difference_to_S",
    "relative_difference_undefined_reason", "f_lower_count", "equal_capacity_count",
    "f_higher_count", "f_lower_fraction", "equal_capacity_fraction", "f_higher_fraction",
    "near_fs_capacity_count", "near_fs_capacity_fraction", "paired_scores_equal_count",
    "scores_changed_allowances_equal_count", "allowances_changed_capacities_equal_count",
    "capacities_different_count",
)
MENU = (
    ("main", 6, 720, 19, 20, 685),
    ("h12", 12, 720, 19, 20, 685),
    ("h24", 24, 720, 19, 20, 685),
    ("n480", 6, 480, 19, 20, 457),
    ("n1440", 6, 1440, 19, 20, 1369),
    ("tau90", 6, 720, 9, 10, 649),
    ("tau99", 6, 720, 99, 100, 714),
)
POINT_COLOR = "#187A8B"


@dataclass(frozen=True)
class OriginalPoint:
    cell_id: str
    horizon: int
    window: int
    tau_numerator: int
    tau_denominator: int
    origin_count: int
    value_millions: float


def display_data(rows) -> tuple[OriginalPoint, ...]:
    """Keep the fixed setting order and the stored direct paired means."""
    if len(rows) != len(MENU):
        raise ValueError("original paired row count differs")
    points = []
    for row, setting in zip(rows, MENU):
        _columns(row, COLUMNS)
        identity = tuple(row[key] for key in COLUMNS[:7])
        if identity != tuple(str(value) for value in (*setting, 6625)):
            raise ValueError("original paired setting, rank, count or order differs")
        cell, horizon, window, numerator, denominator, _ = setting
        difference = _finite(row, "mean_pinball_difference")
        points.append(OriginalPoint(cell, horizon, window, numerator, denominator,
                                    6625, difference * 1e-6))
    return tuple(points)


def load_verified_results(directory: Path = PUBLIC_RESULTS):
    """Check accepted manifest, table bytes/header and fixed row identities."""
    directory = Path(directory).absolute()
    manifest_raw = _read_regular(directory / "run-manifest.json")
    if hashlib.sha256(manifest_raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError("accepted original manifest hash differs")
    manifest = json.loads(manifest_raw)
    if (manifest["run_status"] != "COMPLETE"
            or any(status != "PASS" for status in manifest["checks"].values())
            or manifest["completed_cell_ids"] != [row[0] for row in MENU]):
        raise ValueError("original run was not accepted")
    matches = [entry for entry in manifest["outputs"]["artifacts"]
               if entry["relative_path"] == "results/paired-comparison.csv"]
    expected = TABLE_IDENTITY
    if (len(matches) != 1 or matches[0]["bytes"] != expected["bytes"]
            or matches[0]["row_count"] != expected["rows"]
            or matches[0]["sha256"] != expected["sha256"]):
        raise ValueError("paired table declaration differs")
    raw = _read_regular(directory / "paired-comparison.csv")
    if len(raw) != expected["bytes"] or hashlib.sha256(raw).hexdigest() != expected["sha256"]:
        raise ValueError("accepted original paired bytes or hash differs")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
    if tuple(reader.fieldnames or ()) != COLUMNS:
        raise ValueError("original paired header differs")
    points = display_data(list(reader))
    return points, {"manifest_sha256": MANIFEST_SHA256,
                    "inputs": {"paired-comparison.csv": dict(expected)}}


def figure_layout(points):
    """Map signed existing differences to an unjittered common zero axis."""
    if len(points) != 7:
        raise ValueError("exactly seven original display points required")
    scale = money_scale([point.value_millions for point in points], 390.0, 672.0)
    return {"kind": "original_contrasts", "axis_limits": [scale.lower, scale.upper],
            "points": [{**asdict(point), "x": scale.position(point.value_millions),
                        "y": 429.0 - index * 43.0, "zero_x": scale.position(0.0),
                        "label_x": 802.0, "label_y": 425.8 - index * 43.0,
                        "label_text": f"{point.value_millions:+.6f}"}
                       for index, point in enumerate(points)]}


def _render(canvas, layout):
    _text(canvas, 42, 551, "Original comparison: all seven fixed settings", 19, bold=True)
    _text(canvas, 42, 529, "Mean pinball loss difference | F minus S | negative favors F within the setting", 11, MUTED)
    _line(canvas, 42, 513, 802, 513, INK, 1.0)
    _text(canvas, 42, 490, "6,625 common issue origins in every row; source-reported USD million units", 10, MUTED)
    for x, label in ((42, "Setting"), (204, "H"), (267, "n"), (331, "tau")):
        _text(canvas, x, 462, label, 9, bold=True)
    _text(canvas, 802, 462, "F minus S (USD million)", 9, MUTED, align="right")
    scale = MoneyScale(*layout["axis_limits"], 390.0, 672.0)
    _axis(canvas, scale, 141, 445)
    labels = {"main": "main (primary)", "h12": "h12", "h24": "h24", "n480": "n480",
              "n1440": "n1440", "tau90": "tau90", "tau99": "tau99"}
    for point in layout["points"]:
        y = point["y"]
        _text(canvas, 42, y - 3.2, labels[point["cell_id"]], 10)
        _text(canvas, 204, y - 3.2, str(point["horizon"]), 10)
        _text(canvas, 267, y - 3.2, str(point["window"]), 10)
        _text(canvas, 331, y - 3.2, f"{point['tau_numerator'] / point['tau_denominator']:.2f}", 10)
        _marker(canvas, point["x"], y, 3.7, POINT_COLOR, "circle")
        _text(canvas, point["label_x"], point["label_y"], point["label_text"],
              10, POINT_COLOR, align="right", max_width=100)
    _text(canvas, 531, 104, "Mean pinball loss difference (USD million)", 9, MUTED, align="center")
    _text(canvas, 42, 83, "F pools historical headrooms; S reanchors raw increment paths at the current signed state.", 9, MUTED)
    _text(canvas, 42, 67, "H counts subsequent records; n counts completed historical episodes; tau is the score's quantile preference.", 9, MUTED)
    _text(canvas, 42, 51, "Preferences are not pooled into an overall winner. Weighted score differences are not cash savings.", 9, MUTED)
    _text(canvas, 42, 35, "Source: accepted original paired-comparison.csv | zero denotes equal recorded mean loss; no uncertainty intervals", 8, MUTED)


def build_figure(output):
    """Write one new vector PDF and a source/display/resource identity receipt."""
    budget = _RenderBudget()
    budget.sample()
    points, identity = load_verified_results()
    layout = figure_layout(points)
    directory = _new_output_directory(output)
    from reportlab.pdfgen.canvas import Canvas
    with (directory / FIGURE_NAME).open("xb") as stream:
        canvas = Canvas(stream, pagesize=(PAGE_WIDTH, PAGE_HEIGHT), invariant=1, pageCompression=1)
        canvas.setTitle("All seven fixed original paired pinball-loss comparisons")
        canvas.setAuthor("")
        canvas.setSubject("Accepted original aggregate display; USD million units")
        _render(canvas, layout)
        canvas.showPage()
        canvas.save()
    raw = (directory / FIGURE_NAME).read_bytes()
    report = {"artifact_schema_version": 1, "purpose": "aggregate-only original comparison restyling",
              **identity, "artifacts": {FIGURE_NAME: {
                  "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "pages": 1,
                  "vector_only": True, "displayed_aggregate_count": 7}},
              "display_layout": layout, "resources": budget.sample()}
    with (directory / "artifact-identity.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", required=True, help="new direct .scratch/revision-figure-* directory")
    arguments = parser.parse_args(argv)
    try:
        report = build_figure(arguments.output)
    except (ValueError, FileExistsError, RuntimeError, OSError) as exc:
        parser.exit(2, f"original figure build rejected: {exc}\n")
    print(json.dumps({"artifacts": report["artifacts"], "resources": report["resources"]}, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
