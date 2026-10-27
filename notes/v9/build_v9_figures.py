"""Render v9 figures from saved public points and aggregate result fields.

No model, feature, target, forecast, score or diagnostic code is imported.
This script reads immutable archives, computes descriptive plotting summaries,
and writes only v9 figure artifacts and their exact source bindings.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/v9/figures"
FIGURES = ROOT / "submission-jof/figures"
OLD_V8 = ROOT.parent / "金融数学论文-v8-20261024"
os.environ.setdefault("MPLCONFIGDIR", str(OUT / "matplotlib-cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np


BLUE = "#17476B"
ORANGE = "#A64B16"
plt.rcParams.update({
    "font.family": "serif", "font.size": 10.5,
    "axes.labelsize": 10.5, "axes.titlesize": 11,
    "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "legend.fontsize": 9, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.unicode_minus": False, "savefig.facecolor": "white",
})


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(relative):
    return json.loads((ROOT / relative).read_text())


def base_axes(ax):
    ax.grid(axis="y", color="0.89", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=0.7)


def comma(ax, axis="y", decimals=0):
    target = ax.yaxis if axis == "y" else ax.xaxis
    target.set_major_formatter(FuncFormatter(lambda v, _: format(v, f",.{decimals}f")))


def save(fig, stem, receipt):
    pdf = FIGURES / (stem + ".pdf")
    png = FIGURES / (stem + ".png")
    fig.savefig(pdf, metadata={"Title": stem, "Creator": "Saved public archive figure rendering"})
    fig.savefig(png, dpi=220)
    receipt.update(pdf=str(pdf.relative_to(ROOT)), png=str(png.relative_to(ROOT)),
                   pdf_sha256=sha(pdf), png_sha256=sha(png),
                   page_inches=list(fig.get_size_inches()),
                   tick_labels=[[t.get_text() for t in a.get_xticklabels() + a.get_yticklabels()]
                                for a in fig.axes])
    plt.close(fig)
    return receipt


def endpoint():
    relative = "notes/v7/example-selection.json"
    source = read_json(relative)
    e = source["selection"]
    # Cross-check the actual comma-format v8 figure binding read-only.
    assert sha(ROOT / relative) == "c8166b3bb06fc2116db5f3e7143c7ff0cb38d72beb8893a20eb66f0c12e650b1"
    old_binding_path = OLD_V8 / "notes/v8/figure1-format-check.json"
    historical_check = None
    if old_binding_path.exists():
        old_binding = json.loads(old_binding_path.read_text())
        assert sha(ROOT / relative) == old_binding["frozen_data_sha256"]
        assert e["absolute_positions"] == old_binding["frozen_absolute_positions"]
        assert e["report"] == old_binding["frozen_report"]
        assert e["dates"] == old_binding["frozen_dates"]
        assert old_binding["coordinates_identical"]
        assert old_binding["qbezier_commands_identical"]
        historical_check = {
            "binding_sha256": sha(old_binding_path),
            "comma_pdf_sha256": sha(OLD_V8 / "submission-jof/figures/v8-endpoint-peak-example.pdf"),
            "same_seven_points_and_report": True,
        }
    positions = np.array(e["absolute_positions"], dtype=float)
    assert np.array_equal(positions, np.abs(e["positions"]))
    assert positions.max() == e["peak"]
    assert positions[-1] == e["endpoint_absolute"]
    assert positions[-1] <= e["report"] < positions.max()
    x = np.arange(len(positions))
    fig, ax = plt.subplots(figsize=(6.65, 3.35))
    ax.plot(x, positions, color=BLUE, marker="o", markersize=4,
            linewidth=1.65, label="Observed absolute position")
    ax.plot(x, np.full(len(x), e["report"]), color=ORANGE, linestyle="--",
            linewidth=1.65, label="Historical headroom limit")
    ax.set_xticks(x, [d[5:] for d in e["dates"]])
    ax.set(xlabel="Economic date (2021)", ylabel="Absolute position (USD millions)")
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    comma(ax)
    base_axes(ax)
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=1)
    fig.tight_layout(pad=0.7)
    record = {
        "source": relative, "source_sha256": sha(ROOT / relative),
        "pointer": "/selection", "selected_origin": e["origin"],
        "dates": e["dates"], "absolute_positions": e["absolute_positions"],
        "report": e["report"], "native_unit": "USD millions",
        "plotted_multiplier_from_saved_native_values": 1.0,
        "old_pr5_billions_multiplier": 0.001,
        "equivalent_to_old_billions_display": True,
        "equivalence_formula": "v9_millions = PR5_display_billions * 1000 = saved_native_value",
        "optional_old_v8_comma_crosscheck": historical_check,
        "old_v8_archive_required_to_render": False,
        "data_selection_changed": False,
    }
    return save(fig, "v9-endpoint-peak-example", record)


def simulation():
    relative = "results/revision-v8/wp3/summary.json"
    rows = read_json(relative)["cells"]
    windows = [52, 260, 720, 2880]
    settings = sorted({(r["phi"], r["variance_persistence"]) for r in rows
                       if r["method"] == "QR33" and r["horizon"] == 6})
    assert len(settings) == 9
    curves = []
    for phi, persistence in settings:
        points = []
        for w in windows:
            matches = [(i, r) for i, r in enumerate(rows)
                       if (r["method"], r["horizon"], r["window"], r["phi"], r["variance_persistence"])
                       == ("QR33", 6, w, phi, persistence)]
            assert len(matches) == 1
            i, r = matches[0]
            assert r["full_procedure_status"] == "COMPLETE"
            assert r["complete_repetitions"] == r["planned_repetitions"] == 32
            value = r["relative_loss_percent"]
            equivalent = 100 * (r["mean_model_loss"] / r["mean_reference_loss"] - 1)
            assert np.isclose(value, equivalent, rtol=0, atol=1e-12)
            points.append({"window": w, "value_pct": value,
                           "pointer": f"/cells/{i}/relative_loss_percent",
                           "mean_model_loss": r["mean_model_loss"],
                           "mean_reference_loss": r["mean_reference_loss"]})
        curves.append({"phi": phi, "variance_persistence": persistence, "points": points})
    matrix = np.array([[p["value_pct"] for p in c["points"]] for c in curves])
    controlled_summary = [{"window": w, "min_pct": float(matrix[:, j].min()),
                           "median_pct": float(np.median(matrix[:, j])),
                           "max_pct": float(matrix[:, j].max())}
                          for j, w in enumerate(windows)]
    c2_relative = "results/v9/nonstationarity/postrun/analysis/report.json"
    c2 = read_json(c2_relative)
    c2_rows = []
    for arm in ["constant", "switching"]:
        for w in [52, 260]:
            matches = [(i, r) for i, r in enumerate(c2["across_source"])
                       if (r["arm"], r["window"], r["method"]) == (arm, w, "QR33")]
            assert len(matches) == 1
            i, r = matches[0]
            if w == 52:
                assert r["status"] == "COMPLETE" and r["complete_sources"] == r["required_sources"] == 13
            else:
                assert r["status"] == "UNASSESSABLE" and r["complete_sources"] == 12 and r["required_sources"] == 13
                assert r["median_pct"] is None and r["q25_pct"] is None and r["q75_pct"] is None
            c2_rows.append({"arm": arm, "window": w, "method": "QR33",
                            "status": r["status"], "required_sources": r["required_sources"],
                            "complete_sources": r["complete_sources"],
                            "median_pct": r["median_pct"], "q25_pct": r["q25_pct"], "q75_pct": r["q75_pct"],
                            "missing_sources": r["missing_sources"], "pointer": f"/across_source/{i}"})

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.25), sharey=True)
    left, right = axes
    xs = np.arange(4)
    for k, values in enumerate(matrix):
        left.plot(xs, values, color="0.64", linewidth=0.8, alpha=0.7,
                  label="Nine persistence settings" if k == 0 else None)
    left.fill_between(xs, matrix.min(axis=0), matrix.max(axis=0), color="0.75", alpha=0.22,
                      label="Range across settings")
    left.plot(xs, np.median(matrix, axis=0), color=BLUE, marker="o", markersize=4,
              linewidth=1.9, label="Median across settings")
    left.set_xticks(xs, [str(w) for w in windows])
    left.set(xlabel="Training history (completed labels)", ylabel="Loss change vs matched headroom (%)",
             title="A. Controlled stationary grid")
    left.legend(frameon=False, loc="upper right", handlelength=1.6, fontsize=8.4)
    right.set_xticks([0, 1], ["52", "260"])
    right.set(xlim=(-0.5, 1.5), xlabel="Training history (completed labels)",
              title="B. Calibrated constant and switching")
    for arm, offset, color, marker, label in [
        ("constant", -0.13, BLUE, "o", "Constant parameters"),
        ("switching", 0.13, ORANGE, "s", "Parameter switching"),
    ]:
        r = next(r for r in c2_rows if r["arm"] == arm and r["window"] == 52)
        med = r["median_pct"]
        right.errorbar(offset, med, yerr=[[med-r["q25_pct"]], [r["q75_pct"]-med]],
                       fmt=marker, color=color, markersize=5, capsize=5, linewidth=1.5,
                       label=label)
        right.text(offset + (-0.08 if arm == "constant" else 0.12), 79,
                   f"{med:.1f}%", color=color, fontsize=9,
                   ha="right" if arm == "constant" else "left", va="top")
    right.text(1, 45, "Unavailable\n12/13 complete sources\nin each arm", ha="center", va="center",
               color="0.25", fontsize=9, bbox={"facecolor": "0.96", "edgecolor": "0.75", "pad": 5})
    right.legend(frameon=False, loc="upper right", fontsize=8.5)
    for ax in axes:
        base_axes(ax)
        ax.axhline(0, color="0.35", linewidth=0.8, linestyle=":")
    left.set_ylim(min(-30, float(matrix.min())-8), max(160, float(matrix.max())+15))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.27, top=0.9, wspace=0.14)
    fig.text(0.275, 0.105, "Each setting: ratio of mean losses over 32 repetitions.\nBand is a setting range, not a confidence interval.",
             ha="center", fontsize=9)
    fig.text(0.755, 0.075, "Median and IQR across 13 source medians.\nEach source requires all 32 paired repetitions.\nMarkers offset for legibility; both at history 52.",
             ha="center", fontsize=9)
    fig.text(0.53, 0.025, "33-predictor regression, six-step target. The panels summarize different estimands.",
             ha="center", fontsize=9, color="0.25")
    record = {
        "controlled_source": relative, "controlled_source_sha256": sha(ROOT / relative),
        "controlled_curves": curves, "controlled_plot_summary": controlled_summary,
        "controlled_estimand": "Each curve point is100*(mean model loss across32reps / mean matched F loss across32reps -1). The median and range across9settings are descriptive plotting summaries only.",
        "c2_source": c2_relative, "c2_source_sha256": sha(ROOT / c2_relative),
        "c2_aggregate_points": c2_rows,
        "c2_estimand": "Equal-weight median and IQR across13source-level repetition medians. Each source requires32complete paired reps. QR33,H6,W52. W260 full13source summaries unavailable.",
        "missing_values_drawn_as_numeric_points": False,
        "completed_only_12_source_substitution": False,
        "line_between_incomplete_c2_windows": False,
        "c2_horizontal_marker_offsets": "Layout only for legibility; both markers have actual training history52.",
        "new_inference_or_confidence_interval": False,
    }
    return save(fig, "v9-simulation-comparison", record)


def murphy(name):
    relative = f"results/supervisor-20261023/inference/inherited-exact/murphy-{name}-display.csv"
    rows = list(csv.DictReader((ROOT / relative).open()))
    points = [{"theta_USD_millions": float(r["theta_USD_millions"]),
               "left_elementary": float(r["left_elementary"]),
               "right_elementary": float(r["right_elementary"])} for r in rows]
    x = np.array([r["theta_USD_millions"] for r in points])
    left = np.array([r["left_elementary"] for r in points])
    right = np.array([r["right_elementary"] for r in points])
    assert len(x) == 201 and np.all(np.diff(x) > 0)
    fig, ax = plt.subplots(figsize=(6.65, 3.35))
    ax.plot(x, left, color=BLUE, linewidth=1.55, label="Quantile regression")
    ax.plot(x, right, color=ORANGE, linestyle="--", linewidth=1.55, label="Historical headroom")
    ax.set(xlabel="Score threshold (USD millions)", ylabel="Mean elementary score")
    comma(ax, "x", 0)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: format(v, ".3f")))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    base_axes(ax)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout(pad=0.7)
    record = {"source": relative, "source_sha256": sha(ROOT / relative),
              "point_count": len(points), "plotted_points": points,
              "source_fields": list(rows[0]), "plotted_x_multiplier": 1.0,
              "plotted_y_multiplier": 1.0,
              "original_pr5_x_multiplier": 1.0 if name == "fx_hourly" else 0.001,
              "reader_labels": ["Quantile regression", "Historical headroom"],
              "saved_grid_only": True, "new_elementary_scores": 0,
              "scope": "Saved display grid; full-breakpoint crossing conclusion remains in existing archive. No interpolation creates new score observations."}
    return save(fig, "v9-murphy-" + name, record)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    protected = [ROOT / "submission-jof/manuscript.tex", ROOT / "submission-jof/supplement.tex"]
    protected += list(FIGURES.glob("v7-*.pdf")) + list(FIGURES.glob("v8-*.pdf"))
    protected += [ROOT / "notes/v7/example-selection.json",
                  ROOT / "results/revision-v8/wp3/summary.json",
                  ROOT / "results/v9/nonstationarity/postrun/analysis/report.json"]
    # Add explicit sources without changing or opening any raw financial inputs.
    protected += [ROOT / f"results/supervisor-20261023/inference/inherited-exact/murphy-{n}-display.csv"
                  for n in ("fx_hourly", "nyfed_weekly")]
    before = {str(p): sha(p) for p in protected if p.exists()}
    previous = json.loads((OUT / "scalars.json").read_text()) if (OUT / "scalars.json").exists() else {}
    figures = [endpoint(), simulation()]
    for item in figures:
        item["adopted_in_main"] = True
    # These had already been rendered before scope was narrowed. Preserve them,
    # but the main retains its original, already reader-labelled Murphy PDFs.
    for item in previous.get("figures", []):
        if "v9-murphy-" in item.get("pdf", ""):
            item["adopted_in_main"] = False
            item["unused_reason"] = "Existing v7 Murphy figures already use reader names; main keeps its original paths."
            figures.append(item)
    assert all(sha(p) == value for p, value in before.items())
    payload = {"schema": "v9-saved-source-figure-scalars-v1",
               "created_utc": datetime.now(timezone.utc).isoformat(),
               "figures": figures, "protected_inputs_unchanged": before,
               "new_financial_forecasts": 0, "new_models": 0,
               "new_diagnostics": 0, "new_scores": 0,
               "scientific_code_imported": False, "visual_qa": "PENDING"}
    (OUT / "scalars.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"figures": len(figures), "scalars": str((OUT / "scalars.json").relative_to(ROOT)),
                      "new_forecasts": 0, "new_scores": 0, "protected_files_unchanged": True}))


if __name__ == "__main__":
    main()
