"""Restyle the three saved v7 figures; never calculate a forecast or score.

Only unit conversion, plotting coordinates/ticks and drawing styles change.
Every plotted value comes from an unchanged saved v7 point or score grid.
"""
import csv
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[2] / ".scratch/revision-v8/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "submission-jof/figures"
NOTES = ROOT / "notes/revision-v8"
plt.rcParams.update({"font.family": "serif", "font.size": 10.5,
                     "axes.labelsize": 11, "xtick.labelsize": 10,
                     "ytick.labelsize": 10, "legend.fontsize": 10,
                     "pdf.fonttype": 42, "ps.fonttype": 42,
                     "axes.spines.top": False, "axes.spines.right": False})


def save(fig, ax, stem, xdigits, ydigits):
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, pos: format(v, "." + str(xdigits) + "f")))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: format(v, "." + str(ydigits) + "f")))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.grid(axis="y", color="0.88", linewidth=.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout(pad=.8)
    path = OUT / (stem + ".pdf")
    fig.savefig(path, metadata={"Title": stem, "Creator": "Matplotlib; saved-source styling only"})
    preview = ROOT / ".scratch/revision-v8/wp2/figures" / (stem + ".png")
    preview.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(preview, dpi=170)
    tick_labels = [t.get_text() for t in ax.get_xticklabels() + ax.get_yticklabels()]
    assert not any("e+" in t.lower() or "e-" in t.lower() for t in tick_labels)
    plt.close(fig)
    return dict(path=str(path.relative_to(ROOT)), preview=str(preview.relative_to(ROOT)),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(), tick_labels=tick_labels,
                scientific_notation=False, grayscale_styles=["black solid", "gray dashed"])


def main():
    results = []
    src = ROOT / "notes/v7/example-selection.json"
    example = json.loads(src.read_text())["selection"]
    fig, ax = plt.subplots(figsize=(6.5, 3.35))
    xs = list(range(len(example["absolute_positions"])))
    ax.plot(xs, [v / 1000 for v in example["absolute_positions"]], color="black", linewidth=1.55,
            marker="o", markersize=3.5, label="Observed absolute position")
    ax.plot(xs, [example["report"] / 1000] * len(xs), color="0.4", linestyle="--", linewidth=1.6,
            label="Historical headroom limit")
    ax.set(xlabel="Economic date (2021)", ylabel="Absolute position (USD billions)")
    ax.set_xticks(xs)
    item = save(fig, ax, "v7-endpoint-peak-example", 0, 0)
    # Dates are labels rather than newly inferred time-series observations.
    # Redraw with the unchanged source date strings after numeric tick testing.
    fig, ax = plt.subplots(figsize=(6.5, 3.35))
    ax.plot(xs, [v / 1000 for v in example["absolute_positions"]], color="black", linewidth=1.55,
            marker="o", markersize=3.5, label="Observed absolute position")
    ax.plot(xs, [example["report"] / 1000] * len(xs), color="0.4", linestyle="--", linewidth=1.6,
            label="Historical headroom limit")
    ax.set(xlabel="Economic date (2021)", ylabel="Absolute position (USD billions)")
    ax.set_xticks(xs, [d[5:] for d in example["dates"]])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: format(v, ".0f")))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.grid(axis="y", color="0.88", linewidth=.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="best");fig.tight_layout(pad=.8)
    path = OUT / "v7-endpoint-peak-example.pdf";fig.savefig(path, metadata={"Title": "Endpoint and peak example; unchanged saved path"})
    preview = ROOT / item["preview"];fig.savefig(preview, dpi=170)
    item.update(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                tick_labels=[t.get_text() for t in ax.get_xticklabels() + ax.get_yticklabels()],
                source=str(src.relative_to(ROOT)), source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                points=len(xs), unit_scale_from_saved_millions=.001)
    plt.close(fig);results.append(item)
    for source, scale, unit in (("fx_hourly", 1., "USD millions"), ("nyfed_weekly", .001, "USD billions")):
        relative = "results/supervisor-20261023/inference/inherited-exact/murphy-" + source + "-display.csv"
        raw = (ROOT / relative).read_bytes()
        rows = list(csv.DictReader(raw.decode().splitlines()))
        fig, ax = plt.subplots(figsize=(6.5, 3.35))
        xs = [float(row["theta_USD_millions"]) * scale for row in rows]
        ax.plot(xs, [float(row["left_elementary"]) for row in rows], color="black", linewidth=1.5, label="Quantile regression")
        ax.plot(xs, [float(row["right_elementary"]) for row in rows], color="0.4", linestyle="--", linewidth=1.5, label="Historical headroom")
        ax.set(xlabel="Score threshold (" + unit + ")", ylabel="Mean elementary score")
        item = save(fig, ax, "v7-murphy-" + source, 0, 3 if source == "fx_hourly" else 2)
        item.update(source=relative, source_sha256=hashlib.sha256(raw).hexdigest(), points=len(rows), unit_scale=scale)
        results.append(item)
    report = dict(operation="Saved-source figure styling only", figures=results, new_forecasts=0,
                  new_scores=0, source_values_changed=0)
    (NOTES / "wp2-figure-styling.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
