#!/usr/bin/env python3
"""Render two frozen aggregate tables as standalone vector PDF pages.

Document-only entry point (run from this project):
    python -B build_revision_figures.py --output .scratch/revision-figure-<new-name>

Only the accepted public manifest, comparisons.csv and monthly.csv are read.
No observations, forecasts, inference, confidence intervals or new metrics are
computed. The only numerical transformation is USD -> USD million for display.
An output directory must be a new direct child of this project's .scratch with
an exclusive revision-figure-* name. Existing paths and symlinks are rejected.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
import hashlib
import io
import json
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PUBLIC_RESULTS = PROJECT_ROOT / "results" / "revision-20261021"
MANIFEST_SHA256 = "396cbdc35288cc4a60ac371b3f0561ffc76bee4b50cda910a29be9e8dc89eb9b"
INPUT_IDENTITIES = {
    "comparisons.csv": {"bytes": 1580, "rows": 22,
                        "sha256": "2d2df9c730b41b24dad9ed1047dcc983326cb4c8413ab0677d249c4b99986393"},
    "monthly.csv": {"bytes": 2229, "rows": 26,
                    "sha256": "14665edd9e0b584f3f88bb054ead5cc2e39c017547d4e0c99f3114ea25f11eb9"},
}
COMPARISON_COLUMNS = (
    "horizon", "contrast_id", "left_set", "right_set", "left_method",
    "right_method", "origin_count", "mean_pinball_difference",
)
MONTHLY_COLUMNS = (
    "horizon", "month", "origin_count", "status", "mean_pinball_nearest360_K",
    "mean_pinball_recent360_K", "mean_pinball_difference", "undefined_reason",
)
MONTHS = (
    "2016-01", "2016-02", "2016-03", "2016-04", "2016-05", "2016-06",
    "2016-07", "2016-08", "2016-09", "2016-10", "2016-11", "2016-12", "2017-01",
)
MONTH_COUNTS = (504, 504, 552, 502, 530, 528, 504, 552, 526, 506, 528, 526, 363)


@dataclass(frozen=True)
class ContrastPoint:
    horizon: int
    count: int
    method: str
    origin_count: int
    value_millions: float
    primary: bool


@dataclass(frozen=True)
class MonthlyPoint:
    horizon: int
    month: str
    origin_count: int
    value_millions: float


@dataclass(frozen=True)
class DisplayData:
    contrasts: tuple[ContrastPoint, ...]
    monthly: tuple[MonthlyPoint, ...]


@dataclass(frozen=True)
class MoneyScale:
    lower: float
    upper: float
    left: float
    right: float

    def position(self, value: float) -> float:
        if not math.isfinite(value) or not self.lower <= value <= self.upper:
            raise ValueError("display value outside finite axis")
        return self.left + (value - self.lower) / (self.upper - self.lower) * (self.right - self.left)


def money_scale(values, left: float, right: float) -> MoneyScale:
    """A shared signed axis that contains zero and pads every marker."""
    values = tuple(values)
    if not values or not all(math.isfinite(x) for x in values):
        raise ValueError("finite nonempty display values required")
    if not math.isfinite(left) or not math.isfinite(right) or right - left < 30:
        raise ValueError("finite plot width of at least 30 points required")
    lower, upper = min(0.0, *values), max(0.0, *values)
    span = upper - lower
    padding = span * 0.10 if span else 0.05
    lower, upper = lower - padding, upper + padding
    if not all(math.isfinite(x) for x in (lower, upper, upper - lower)):
        raise ValueError("unrepresentable display axis")
    return MoneyScale(lower, upper, left, right)


def _finite(row, key):
    try:
        value = float(row[key])
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError(f"invalid aggregate number: {key}") from exc
    if not math.isfinite(value):
        raise ValueError(f"nonfinite aggregate number: {key}")
    return value


def _columns(row, columns):
    if set(row) != set(columns) or any(not isinstance(value, str) for value in row.values()):
        raise ValueError("aggregate columns or cell types differ")


def display_data(comparisons, monthly) -> DisplayData:
    """Validate fixed public row identities and extract existing differences only."""
    if len(comparisons) != 22 or len(monthly) != 26:
        raise ValueError("aggregate row count differs from the accepted menu")
    contrasts = []
    row_index = 0
    for horizon in (6, 24):
        identities = [
            ("nearest_minus_recent", f"nearest{count}", f"recent{count}", method, method, count)
            for count in (360, 180) for method in ("F", "S", "K")
        ] + [("F_minus_S", selected, selected, "F", "S", None)
             for selected in ("full720", "recent360", "nearest360", "recent180", "nearest180")]
        for contrast, left, right, method, right_method, count in identities:
            row = comparisons[row_index]
            row_index += 1
            _columns(row, COMPARISON_COLUMNS)
            actual = tuple(row[key] for key in COMPARISON_COLUMNS[:7])
            if actual != (str(horizon), contrast, left, right, method, right_method, "6625"):
                raise ValueError("comparison identity or order differs")
            difference = _finite(row, "mean_pinball_difference")
            if contrast == "nearest_minus_recent":
                contrasts.append(ContrastPoint(horizon, count, method, 6625, difference * 1e-6,
                                                (horizon, count, method) == (6, 360, "K")))
    months = []
    row_index = 0
    for horizon in (6, 24):
        for month, count in zip(MONTHS, MONTH_COUNTS):
            row = monthly[row_index]
            row_index += 1
            _columns(row, MONTHLY_COLUMNS)
            identity = tuple(row[key] for key in MONTHLY_COLUMNS[:4])
            if identity != (str(horizon), month, str(count), "DISPLAYED") or row["undefined_reason"] != "":
                raise ValueError("monthly identity, count, status or order differs")
            for key in MONTHLY_COLUMNS[4:7]:
                _finite(row, key)
            months.append(MonthlyPoint(horizon, month, count, _finite(row, "mean_pinball_difference") * 1e-6))
    return DisplayData(tuple(contrasts), tuple(months))


def _read_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("public input must be a regular file without symlinks")
    if any(parent.is_symlink() for parent in path.parents):
        raise ValueError("public input ancestor is a symlink")
    return path.read_bytes()


def load_verified_results(directory: Path = PUBLIC_RESULTS):
    """Pin the accepted manifest, CSV bytes, hashes, columns, rows and identities."""
    directory = Path(directory).absolute()
    manifest_bytes = _read_regular(directory / "manifest.json")
    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:
        raise ValueError("accepted public manifest hash differs")
    manifest = json.loads(manifest_bytes)
    if manifest["run_status"] != "COMPLETE" or manifest["checks"]["aggregate_identities"] != "PASS":
        raise ValueError("public run was not accepted")
    parsed = {}
    identity = {"manifest_sha256": MANIFEST_SHA256, "inputs": {}}
    for name, expected in INPUT_IDENTITIES.items():
        matches = [entry for entry in manifest["artifacts"] if entry["file_name"] == name]
        if len(matches) != 1 or {key: matches[0][key] for key in expected} != expected:
            raise ValueError("CSV identity differs from accepted manifest")
        raw = _read_regular(directory / name)
        if len(raw) != expected["bytes"] or hashlib.sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError("accepted public CSV bytes or hash differs")
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
        columns = COMPARISON_COLUMNS if name == "comparisons.csv" else MONTHLY_COLUMNS
        if tuple(reader.fieldnames or ()) != columns:
            raise ValueError("CSV header differs")
        rows = list(reader)
        if len(rows) != expected["rows"]:
            raise ValueError("CSV row count differs")
        parsed[name] = rows
        identity["inputs"][name] = dict(expected)
    return display_data(parsed["comparisons.csv"], parsed["monthly.csv"]), identity

# The renderer uses no numerical library. Keep any transitive numerical import
# within the project's standing thread request before loading document packages.
import os
for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
                         "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

import argparse
from dataclasses import asdict
import re
import resource
import subprocess
import sys
import time

PAGE_WIDTH = 841.8897637795277
PAGE_HEIGHT = 595.2755905511812
FIGURE_NAMES = ("revision-retrieval-contrasts.pdf", "revision-retrieval-monthly.pdf")
METHOD_COLORS = {"F": "#187A8B", "S": "#C16C13", "K": "#7350A2"}
HORIZON_COLORS = {6: "#187A8B", 24: "#7350A2"}
INK = "#203345"
MUTED = "#526372"
GRID = "#D7DEE3"


def figure_layouts(data: DisplayData):
    """Return the exact aggregate-to-page positions used by the vector renderer."""
    contrast_scale = money_scale([p.value_millions for p in data.contrasts], 128.0, 330.0)
    contrast_points = []
    for index, point in enumerate(data.contrasts):
        offset = 0.0 if point.horizon == 6 else 400.0
        y = 433.0 - (index % 6) * 44.0
        contrast_points.append({
            **asdict(point), "x": contrast_scale.position(point.value_millions) + offset,
            "y": y, "radius": 3.7, "zero_x": contrast_scale.position(0.0) + offset,
            "plot_bounds": [128.0 + offset, 190.0, 330.0 + offset, 452.0],
            "axis_limits": [contrast_scale.lower, contrast_scale.upper],
            "label_x": 402.0 + offset, "label_y": y - 3.2,
        })
    monthly_scale = money_scale([p.value_millions for p in data.monthly], 190.0, 596.0)
    monthly_points = []
    for index, point in enumerate(data.monthly):
        y = 451.0 - (index % 13) * 24.0 + (3.0 if point.horizon == 6 else -3.0)
        monthly_points.append({
            **asdict(point), "x": monthly_scale.position(point.value_millions),
            "y": y, "radius": 3.3, "zero_x": monthly_scale.position(0.0),
            "plot_bounds": [190.0, 148.0, 596.0, 466.0],
            "axis_limits": [monthly_scale.lower, monthly_scale.upper],
            "label_x": 701.0 if point.horizon == 6 else 802.0,
            "label_y": 448.0 - (index % 13) * 24.0,
        })
    return [
        {"kind": "contrasts", "points": contrast_points,
         "axis_limits": [contrast_scale.lower, contrast_scale.upper]},
        {"kind": "monthly", "points": monthly_points,
         "axis_limits": [monthly_scale.lower, monthly_scale.upper]},
    ]


def _text(canvas, x, y, value, size=10, color=INK, bold=False, align="left", max_width=None):
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase.pdfmetrics import stringWidth
    if not value.isascii():
        raise ValueError("standalone figure labels must be ASCII")
    font = "Helvetica-Bold" if bold else "Helvetica"
    width = stringWidth(value, font, size)
    left = x - width if align == "right" else x - width / 2 if align == "center" else x
    if (max_width is not None and width > max_width) or not (0 <= left and left + width <= PAGE_WIDTH):
        raise ValueError("figure text exceeds its page or column")
    if not size <= y <= PAGE_HEIGHT - size:
        raise ValueError("figure text baseline exceeds its page")
    canvas.setFont(font, size)
    canvas.setFillColor(HexColor(color))
    if align == "right":
        canvas.drawRightString(x, y, value)
    elif align == "center":
        canvas.drawCentredString(x, y, value)
    else:
        canvas.drawString(x, y, value)


def _line(canvas, x1, y1, x2, y2, color=GRID, width=0.6):
    from reportlab.lib.colors import HexColor
    canvas.setStrokeColor(HexColor(color))
    canvas.setLineWidth(width)
    canvas.line(x1, y1, x2, y2)


def _marker(canvas, x, y, radius, color, shape):
    from reportlab.lib.colors import HexColor
    canvas.setFillColor(HexColor(color))
    canvas.setStrokeColor(HexColor(color))
    if shape == "circle":
        canvas.circle(x, y, radius, stroke=0, fill=1)
    elif shape == "square":
        canvas.rect(x - radius, y - radius, radius * 2, radius * 2, stroke=0, fill=1)
    else:
        path = canvas.beginPath()
        path.moveTo(x, y + radius)
        path.lineTo(x + radius, y)
        path.lineTo(x, y - radius)
        path.lineTo(x - radius, y)
        path.close()
        canvas.drawPath(path, stroke=0, fill=1)


def _axis(canvas, scale, bottom, top):
    # Keep the zero tick apart from nearby regular ticks, including axes with
    # only positive or only negative data. This does not discard data markers.
    zero = scale.position(0.0)
    ticks = [scale.lower + (scale.upper - scale.lower) * i / 4 for i in range(5)]
    ticks = [value for value in ticks if abs(scale.position(value) - zero) >= 30.0]
    ticks.append(0.0)
    for value in sorted(ticks):
        x = scale.position(value)
        is_zero = value == 0.0
        _line(canvas, x, bottom, x, top, MUTED if is_zero else GRID, 1.0 if is_zero else 0.5)
        _line(canvas, x, bottom, x, bottom - 4, MUTED)
        _text(canvas, x, bottom - 17, "0" if is_zero else f"{value:+.3f}",
              8.0, MUTED, align="center")
    _line(canvas, scale.left, bottom, scale.right, bottom, MUTED, 0.7)


def _render_contrasts(canvas, layout):
    _text(canvas, 42, 551, "Nearest versus recent: all frozen loss contrasts", 19, bold=True)
    _text(canvas, 42, 529, "Exploratory paired means | nearest minus recent | negative favors nearest", 11, MUTED)
    _line(canvas, 42, 513, 802, 513, INK, 1.0)
    for offset, horizon in ((0, 6), (400, 24)):
        _text(canvas, 43 + offset, 485, f"H = {horizon} records", 13, bold=True)
        _text(canvas, 43 + offset, 467, "6,625 paired origins in every row", 9, MUTED)
        _text(canvas, 43 + offset, 450, "m / method", 8, MUTED)
        _text(canvas, 402 + offset, 450, "USD million", 8, MUTED, align="right")
        scale = MoneyScale(*layout["axis_limits"], 128 + offset, 330 + offset)
        _axis(canvas, scale, 181, 443)
        _line(canvas, 43 + offset, 323, 402 + offset, 323, GRID)
        _text(canvas, 229 + offset, 143, "Mean pinball loss difference (USD million)",
              8.8, MUTED, align="center")
    _line(canvas, 422, 145, 422, 495, GRID, 0.8)
    for point in layout["points"]:
        offset = 0 if point["horizon"] == 6 else 400
        method = point["method"]
        _text(canvas, 43 + offset, point["y"] - 3.2, f"{point['count']}  {method}", 10,
              bold=point["primary"], max_width=80)
        if point["primary"]:
            _text(canvas, 43 + offset, point["y"] - 15.5, "PRIMARY", 7.5, METHOD_COLORS["K"], bold=True)
        _marker(canvas, point["x"], point["y"], point["radius"], METHOD_COLORS[method],
                {"F": "circle", "S": "square", "K": "diamond"}[method])
        _text(canvas, point["label_x"], point["label_y"], f"{point['value_millions']:+.6f}",
              9.5, METHOD_COLORS[method], bold=point["primary"], align="right", max_width=66)
    for x, method in ((49, "F"), (121, "S"), (193, "K")):
        _marker(canvas, x, 111, 3.4, METHOD_COLORS[method],
                {"F": "circle", "S": "square", "K": "diamond"}[method])
        _text(canvas, x + 10, 108, method, 9, METHOD_COLORS[method], bold=True)
    _text(canvas, 42, 80, "PRIMARY marks the prespecified H=6, m=360, K contrast; it does not imply an overall ranking.", 9, MUTED)
    _text(canvas, 42, 64, "All 12 frozen nearest-minus-recent aggregate means are shown. No uncertainty intervals are displayed.", 9, MUTED)
    _text(canvas, 42, 41, "Source: accepted public comparisons.csv | exploratory-state-selection-20261021", 8, MUTED)


def _render_monthly(canvas, layout):
    _text(canvas, 42, 551, "Monthly primary contrasts: descriptive / exploratory", 19, bold=True)
    _text(canvas, 42, 529, "Exploratory paired means | nearest360 K minus recent360 K | negative favors nearest", 10.5, MUTED)
    _line(canvas, 42, 513, 802, 513, INK, 1.0)
    for x, horizon in ((48, 6), (168, 24)):
        _marker(canvas, x, 496, 3.5, HORIZON_COLORS[horizon], "circle" if horizon == 6 else "diamond")
        _text(canvas, x + 11, 493, f"H = {horizon} records", 9.5, HORIZON_COLORS[horizon], bold=True)
    _text(canvas, 42, 476, "Month", 9, bold=True)
    _text(canvas, 165, 476, "n (each H)", 8.5, MUTED, align="right")
    _text(canvas, 701, 476, "H=6 (USD million)", 8.5, HORIZON_COLORS[6], align="right")
    _text(canvas, 802, 476, "H=24 (USD million)", 8.5, HORIZON_COLORS[24], align="right")
    scale = MoneyScale(*layout["axis_limits"], 190, 596)
    _axis(canvas, scale, 137, 465)
    for index, (month, count) in enumerate(zip(MONTHS, MONTH_COUNTS)):
        y = 451 - index * 24
        _text(canvas, 42, y - 3, month, 9.5)
        _text(canvas, 165, y - 3, str(count), 9.5, MUTED, align="right")
        if index < 12:
            _line(canvas, 42, y - 12, 802, y - 12, "#E8ECEF", 0.35)
    for point in layout["points"]:
        horizon = point["horizon"]
        color = HORIZON_COLORS[horizon]
        _marker(canvas, point["x"], point["y"], point["radius"], color,
                "circle" if horizon == 6 else "diamond")
        _text(canvas, point["label_x"], point["label_y"], f"{point['value_millions']:+.6f}",
              9.2, color, align="right", max_width=78)
    _text(canvas, 393, 100, "Monthly mean pinball loss difference (USD million)", 9, MUTED, align="center")
    _text(canvas, 42, 78, "All 13 calendar months are retained, including positive January 2016 at both horizons.", 9, MUTED)
    _text(canvas, 42, 62, "Descriptive summaries of the inspected evaluation record. Zero marks equal average pinball loss.", 9, MUTED)
    _text(canvas, 42, 41, "Source: accepted public monthly.csv | primary nearest360 K minus recent360 K", 8, MUTED)


def _new_output_directory(output):
    path = Path(output)
    if ".." in path.parts:
        raise ValueError("output path traversal is not allowed")
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    scratch = PROJECT_ROOT / ".scratch"
    if path.parent != scratch or not re.fullmatch(r"revision-figure-[A-Za-z0-9][A-Za-z0-9-]*", path.name):
        raise ValueError("output must be a new direct .scratch/revision-figure-* directory")
    if not scratch.is_dir() or scratch.is_symlink() or any(parent.is_symlink() for parent in scratch.parents):
        raise ValueError("output parent must be a regular task scratch directory")
    if os.path.lexists(path):
        raise FileExistsError("output path already exists; no overwrite is allowed")
    path.mkdir(mode=0o700)
    return path


def _os_threads():
    if sys.platform == "darwin":
        result = subprocess.run(["ps", "-M", "-p", str(os.getpid())], check=True,
                                capture_output=True, text=True, timeout=3)
        count = len([line for line in result.stdout.splitlines()[1:] if line.strip()])
    else:
        count = len(list(Path("/proc/self/task").iterdir()))
    if count < 1:
        raise RuntimeError("OS thread measurement unavailable")
    return count


class _RenderBudget:
    def __init__(self):
        self.started = time.monotonic()
        self.max_threads = 0
        self.snapshots = 0

    def sample(self):
        self.max_threads = max(self.max_threads, _os_threads())
        self.snapshots += 1
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss_bytes = int(rss if sys.platform == "darwin" else rss * 1024)
        elapsed = time.monotonic() - self.started
        if elapsed >= 600 or rss_bytes >= 2 * 1024 ** 3 or self.max_threads > 2:
            raise RuntimeError("document-render resource budget exceeded")
        return {"elapsed_seconds": elapsed, "peak_rss_bytes": rss_bytes,
                "maximum_observed_os_threads": self.max_threads,
                "thread_snapshot_count": self.snapshots, "requested_numerical_threads": 1}


def build_figures(output):
    """Create exactly two pinned standalone vector PDFs and one identity receipt."""
    budget = _RenderBudget()
    budget.sample()
    data, inputs = load_verified_results()
    layouts = figure_layouts(data)
    directory = _new_output_directory(output)
    from reportlab.pdfgen.canvas import Canvas
    report = {"artifact_schema_version": 1, "purpose": "aggregate-only document figures",
              **inputs, "artifacts": {}, "display_layouts": layouts}
    for name, layout, render in zip(FIGURE_NAMES, layouts, (_render_contrasts, _render_monthly)):
        # Exclusive byte streams avoid ReportLab's default overwrite behavior.
        with (directory / name).open("xb") as stream:
            canvas = Canvas(stream, pagesize=(PAGE_WIDTH, PAGE_HEIGHT), invariant=1, pageCompression=1)
            canvas.setTitle("Frozen exploratory retrieval contrasts" if layout["kind"] == "contrasts"
                            else "Descriptive exploratory monthly primary contrasts")
            canvas.setAuthor("")
            canvas.setSubject("Frozen public aggregate display; USD million units")
            render(canvas, layout)
            canvas.showPage()
            canvas.save()
        raw = (directory / name).read_bytes()
        report["artifacts"][name] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                                   "pages": 1, "vector_only": True,
                                   "displayed_aggregate_count": len(layout["points"])}
        budget.sample()
    report["resources"] = budget.sample()
    with (directory / "artifact-identity.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", required=True, help="new direct .scratch/revision-figure-* directory")
    arguments = parser.parse_args(argv)
    try:
        report = build_figures(arguments.output)
    except (ValueError, FileExistsError, RuntimeError, OSError) as exc:
        parser.exit(2, f"figure build rejected: {exc}\n")
    output = Path(arguments.output)
    if not output.is_absolute():
        output = PROJECT_ROOT / output
    print(json.dumps({"output_directory": str(output), "pdf_count": len(report["artifacts"]),
                      "artifacts": report["artifacts"], "resources": report["resources"]}, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
