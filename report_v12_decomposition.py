"""Display-only F1 signed decomposition with source-bound plot primitives.

No observations, forecasts, fitting, losses, selection or inference are created.
Run explicitly after F1; input is its public scalar rows.json, not private traces.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import hashlib
import json
import math
from numbers import Real
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
DEFAULT_ROWS = ROOT / "results/v12/decomposition/rows.json"
DEFAULT_PROTOCOL = ROOT / "protocol/v12/loss-decomposition-design.md"
METHODS = ("QR33", "QR4")
FAMILIES = ("cftc", "panel", "bill", "fx")
FAMILY_LABELS = dict(cftc="CFTC", panel="Panel", bill="Bill", fx="FX")
FIELDS = dict(S="selection_component_pct", G="signal_gap_pct", E="actual_excess_pct")
COLORS = dict(S="#0072B2", G="#D55E00", E="#000000", unavailable="#777777")
OUTPUT_NAMES = ("decomposition.pdf", "decomposition.png", "plot-data.csv", "figure-bindings.json")


def _json(raw):
    def reject(token):
        raise ValueError("NONFINITE_JSON_TOKEN:" + token)
    return json.loads(raw, parse_constant=reject)


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _finite(value):
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)


def planned_cells(protocol=DEFAULT_PROTOCOL):
    """Derive the frozen 90 slots from protocol metadata, without source I/O.

    Family order is fixed. Within a family use H, W, then the fixed source list
    in the frozen protocol. Neither input row order nor observed outcomes sorts
    the figure. Panel source IDs are the protocol's twelve pinned panel paths.
    """
    raw = Path(protocol).read_bytes()
    blocks = re.findall(r"```json\s*\n(.*?)\n```", raw.decode(), re.S)
    if len(blocks) != 1:
        raise ValueError("F1_PROTOCOL_JSON_REQUIRED")
    design = _json(blocks[0])
    if design.get("experiment") != "F1" or design.get("planned_source_cells") != 90:
        raise ValueError("F1_90_CELL_PROTOCOL_REQUIRED")
    provenance = design["input_provenance"]
    source_keys = dict(
        cftc=[row["code"] for row in provenance["cftc_sources"]],
        panel=[Path(row["path"]).stem for row in provenance["raw_sources"]
               if Path(row["path"]).parent.name == "panel"],
        bill=["PDPOSGS-B"], fx=["fx_hourly"])
    geometries = {("fx" if g["family"] == "fx_original" else g["family"]): g
                  for g in design["geometries"]}
    result = []
    for family in FAMILIES:
        geometry = geometries[family]
        keys = source_keys[family]
        if len(keys) != geometry["sources"] or len(set(keys)) != len(keys):
            raise ValueError("F1_SOURCE_INVENTORY_MISMATCH:" + family)
        for horizon in sorted(geometry["H"]):
            for window in sorted(geometry["W"]):
                for key in keys:
                    result.append(dict(family=family, source_key=key, period="original",
                                       horizon=horizon, window=window, tau=design["tau"]))
    if len(result) != 90:
        raise ValueError("F1_PLOT_PLAN_COUNT_MISMATCH")
    return result


def _key(row):
    return tuple(row.get(name) for name in
                 ("family", "source_key", "period", "horizon", "window", "method"))


def prepare_plot_rows(rows, plan):
    """Bind each of 180 planned method slots to input rows, preserving status.

    A missing, duplicate, failed, or invalid COMPLETE row is unavailable. Its
    components remain absent; the renderer uses an x marker, never zero bars.
    """
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("ROWS_JSON_LIST_OF_RECORDS_REQUIRED")
    expected = {_key(dict(cell, method=method)) for cell in plan for method in METHODS}
    grouped = defaultdict(list)
    for index, row in enumerate(rows):
        if _key(row) not in expected:
            raise ValueError("UNEXPECTED_F1_PLOT_ROW:" + str(index))
        if row.get("experiment", "F1") != "F1" or row.get("tau", .95) != .95:
            raise ValueError("NON_F1_EXPERIMENT_OR_TAU:" + str(index))
        grouped[_key(row)].append((index, row))
    prepared = []
    for method in METHODS:
        for index, cell in enumerate(plan):
            matches = grouped[_key(dict(cell, method=method))]
            row = matches[0][1] if len(matches) == 1 else None
            valid = (row is not None and row.get("status") == "COMPLETE" and
                     all(_finite(row.get(field)) for field in FIELDS.values()))
            display_status = ("MISSING_ROW" if not matches else "DUPLICATE_INPUT" if len(matches) > 1
                              else "INVALID_COMPLETE_ROW" if row.get("status") == "COMPLETE" and not valid
                              else row.get("status", "MISSING_STATUS"))
            row_index = matches[0][0] if len(matches) == 1 else None
            item = dict(cell, method=method, plan_index=index + 1,
                        cell_id=(row.get("cell_id") if row else None),
                        status=(row.get("status") if row else display_status),
                        display_status=display_status, plotted=valid,
                        input_row_indices=[i for i, _ in matches],
                        reported_statuses=[r.get("status") for _, r in matches],
                        source_row_pointer=(f"/{row_index}" if row_index is not None else None),
                        source_status_pointer=(f"/{row_index}/status" if row_index is not None else None))
            for symbol, field in FIELDS.items():
                item[field] = row.get(field) if row is not None else None
                item[symbol + "_pointer"] = f"/{row_index}/{field}" if row_index is not None else None
            prepared.append(item)
    return prepared


def _positions(plan):
    positions, blocks = [], []
    x = 0
    for family in FAMILIES:
        count = sum(cell["family"] == family for cell in plan)
        start = len(positions)
        positions.extend(range(x, x + count))
        blocks.append(dict(family=family, first_index=start + 1,
                           last_index=start + count, first_x=x, last_x=x + count - 1))
        x += count + 2
    return positions, blocks


def _render(prepared, plan, pdf_path, png_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    positions, blocks = _positions(plan)
    options = {"font.family": "DejaVu Sans", "font.size": 8,
               "axes.labelsize": 8, "axes.titlesize": 9,
               "xtick.labelsize": 8, "ytick.labelsize": 8,
               "legend.fontsize": 8, "pdf.fonttype": 42,
               "hatch.linewidth": .35, "axes.linewidth": .5}
    extents = [0.]
    with plt.rc_context(options):
        figure, axes = plt.subplots(2, 1, figsize=(6.4, 3.8), sharex=True, sharey=True)
        figure.subplots_adjust(left=.105, right=.985, bottom=.15, top=.805, hspace=.68)
        for facet, (axis, method) in enumerate(zip(axes, METHODS)):
            owned = [row for row in prepared if row["method"] == method]
            for item, x in zip(owned, positions):
                item["plot_x"] = x
                if not item["plotted"]:
                    axis.plot(x, 0, marker="x", markersize=3.2, markeredgewidth=.7,
                              color=COLORS["unavailable"], linestyle="none", zorder=6)
                    continue
                positive = negative = 0.
                for symbol, hatch in (("S", "////"), ("G", "....")):
                    value = item[FIELDS[symbol]]
                    bottom = positive if value >= 0 else negative
                    axis.bar(x, value, bottom=bottom, width=.83, color=COLORS[symbol],
                             edgecolor="#222222", linewidth=.15, hatch=hatch, zorder=3)
                    if value >= 0:
                        positive += value
                    else:
                        negative += value
                extents.extend((positive, negative, item[FIELDS["E"]]))
                axis.plot(x, item[FIELDS["E"]], marker="o", markersize=2.1,
                          color=COLORS["E"], linestyle="none", zorder=7)
            label = "Full regression" if method == "QR33" else "Four-feature regression"
            axis.set_title(f"{'ab'[facet]}  {label}", loc="left", pad=16, fontweight="bold")
            axis.axhline(0, color="#222222", linewidth=.55, zorder=2)
            axis.yaxis.grid(True, color="#dddddd", linewidth=.35, zorder=0)
            axis.spines[["top", "right"]].set_visible(False)
            axis.tick_params(axis="both", width=.5, length=2.5)
            for block in blocks:
                center = (block["first_x"] + block["last_x"]) / 2
                axis.text(center, 1.015, FAMILY_LABELS[block["family"]], ha="center", va="bottom",
                          transform=axis.get_xaxis_transform(), fontsize=8)
                if block["first_x"]:
                    axis.axvline(block["first_x"] - 1.5, color="#bbbbbb", linewidth=.45)
            axis.set_xlim(positions[0] - 1.2, positions[-1] + 1.2)
        low, high = min(extents), max(extents)
        span = high - low if high != low else 2.
        axes[0].set_ylim(low - .09 * span, high + .12 * span)
        # Sparse numeric positions, never 180 tiny source labels. Full mapping is CSV.
        ticks = (1, 18, 35, 47, 59, 71, 83, 90)
        axes[-1].set_xticks([positions[i - 1] for i in ticks], [str(i) for i in ticks])
        axes[-1].set_xlabel("Planned comparison index", labelpad=4)
        figure.text(.014, .47, "Excess loss relative to history (%)", rotation=90,
                    va="center", ha="left", fontsize=8)
        handles = [Patch(facecolor=COLORS["S"], edgecolor="#222222", linewidth=.3, hatch="////", label="Selection component"),
                   Patch(facecolor=COLORS["G"], edgecolor="#222222", linewidth=.3, hatch="....", label="Finite-menu gap"),
                   Line2D([], [], marker="o", color="black", linestyle="none", markersize=3, label="Actual excess"),
                   Line2D([], [], marker="x", color=COLORS["unavailable"], linestyle="none", markersize=4, label="Unavailable")]
        figure.legend(handles=handles, ncol=4, loc="upper center", bbox_to_anchor=(.51, .997),
                      frameon=False, handlelength=1.2, columnspacing=1.15)
        figure.savefig(pdf_path, metadata={"Title": "F1 signed fixed-menu loss decomposition",
                                          "Subject": "Display of source-bound scalar results; no new inference"})
        figure.savefig(png_path, dpi=300)
        plt.close(figure)
    return blocks


def build_figure(rows_path=DEFAULT_ROWS, output_dir=None, protocol=DEFAULT_PROTOCOL):
    """Read scalar JSON and write PDF/PNG/CSV/bindings on explicit invocation."""
    rows_path = Path(rows_path).resolve()
    output_dir = Path(output_dir).resolve() if output_dir is not None else rows_path.parent
    protocol = Path(protocol).resolve()
    rows_raw = rows_path.read_bytes()
    rows = _json(rows_raw)
    plan = planned_cells(protocol)
    prepared = prepare_plot_rows(rows, plan)
    destinations = {name: output_dir / name for name in OUTPUT_NAMES}
    if any(path.exists() for path in destinations.values()):
        raise FileExistsError("FIGURE_OUTPUT_ALREADY_EXISTS")
    output_dir.mkdir(parents=True, exist_ok=True)
    blocks = _render(prepared, plan, destinations["decomposition.pdf"], destinations["decomposition.png"])
    columns = list(prepared[0])
    with destinations["plot-data.csv"].open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in prepared:
            writer.writerow({key: json.dumps(value, allow_nan=False) if isinstance(value, list) else value
                             for key, value in row.items()})
    row_sha = _digest(rows_raw)
    bindings = []
    for row in prepared:
        for symbol, field in FIELDS.items():
            bindings.append(dict(binding_id=f"{row['method']}:{row['plan_index']:03d}:{symbol}",
                symbol=symbol, field=field, method=row["method"], plan_index=row["plan_index"],
                plot_x=row["plot_x"], cell_id=row["cell_id"], status=row["status"],
                display_status=row["display_status"], rendered=row["plotted"],
                value=row[field], rows_sha256=row_sha, json_pointer=row[symbol + "_pointer"],
                source_status_pointer=row["source_status_pointer"],
                input_row_indices=row["input_row_indices"],
                reported_statuses=row["reported_statuses"]))
    record = dict(schema_version=1, experiment="F1", planned_source_cells=90,
        planned_method_cells=180, input_rows=dict(path=str(rows_path), bytes=len(rows_raw),
            sha256=row_sha, row_count=len(rows)),
        protocol=dict(path=str(protocol), sha256=_digest(protocol.read_bytes())),
        display=dict(width_inches=6.4, height_inches=3.8, minimum_font_points=8,
            units="Percent of matched reference F mean loss", colors=COLORS,
            facet_methods=list(METHODS), family_blocks=blocks,
            sorting="fixed family, horizon, window, pinned protocol source order",
            stacking="Separate positive and negative display baselines; signed S/G preserved.",
            total_marker="E is copied from actual_excess_pct, never recalculated.",
            unavailable="Gray x at zero is an unavailable marker, never a zero-valued loss."),
        artifacts=[dict(path=str(path), bytes=path.stat().st_size,
                        sha256=_digest(path.read_bytes()))
                   for name, path in destinations.items() if name != "figure-bindings.json"],
        bindings=bindings)
    with destinations["figure-bindings.json"].open("x") as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write("\n")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    args = parser.parse_args()
    result = build_figure(args.rows, args.output_dir, args.protocol)
    print(json.dumps(dict(planned_method_cells=result["planned_method_cells"],
                         input_rows_sha256=result["input_rows"]["sha256"],
                         artifacts=result["artifacts"]), indent=2))
