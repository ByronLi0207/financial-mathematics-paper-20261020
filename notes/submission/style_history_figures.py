"""Display-only history-title clarification from pinned, tracked materials.

Loads only the original pure cftc/menu plotting definitions through an AST
allowlist. No model, runner, reducer, summary or legacy BEFORE-cache import.
All numeric artist arrays are checked against the tracked v10b style receipt.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
BASE = "8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6"
SOURCE = "notes/v10b/style_saved_displays.py"
SAVED_RECEIPT = "notes/v10b/visual-style-report.json"
HERE = ROOT / "notes/submission"
QA = ROOT / ".scratch/submission/figures-preflight/history-labels"
QA.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(QA / "matplotlib-cache")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.text import Text
import numpy as np
from pypdf import PdfReader
from PIL import Image


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def tracked_blob(path):
    data = git_blob(path)
    assert (ROOT / path).read_bytes() == data, "TRACKED_INPUT_DRIFT:" + path
    return data


def clean(value):
    if isinstance(value, np.ndarray):
        return clean(value.tolist())
    if isinstance(value, (list, tuple)):
        return [clean(x) for x in value]
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return repr(value)
    return value


def line_state(line):
    return clean(dict(
        x=np.asarray(line.get_xdata()), y=np.asarray(line.get_ydata()),
        color=line.get_color(), linestyle=line.get_linestyle(),
        linewidth=line.get_linewidth(), marker=line.get_marker(),
        markersize=line.get_markersize(), markerfacecolor=line.get_markerfacecolor(),
        markeredgecolor=line.get_markeredgecolor(),
        markeredgewidth=line.get_markeredgewidth(), markevery=line.get_markevery(),
        alpha=line.get_alpha(), zorder=line.get_zorder(),
        transform=line.get_transform().get_matrix(),
    ))


def collection_state(col):
    result = dict(
        type=type(col).__name__, facecolors=col.get_facecolors(),
        edgecolors=col.get_edgecolors(), linewidths=col.get_linewidths(),
        linestyles=col.get_linestyles(), alpha=col.get_alpha(),
        zorder=col.get_zorder(), transform=col.get_transform().get_matrix(),
        offset_transform=col.get_offset_transform().get_matrix(),
    )
    if hasattr(col, "get_offsets"):
        result["offsets"] = np.asarray(col.get_offsets())
    if hasattr(col, "get_sizes"):
        result["sizes"] = col.get_sizes()
    if hasattr(col, "get_segments"):
        result["segments"] = col.get_segments()
    if hasattr(col, "get_paths"):
        result["paths"] = [dict(vertices=p.vertices, codes=p.codes) for p in col.get_paths()]
    return clean(result)


def text_state(t):
    return clean(dict(
        text=t.get_text(), position=t.get_position(), fontsize=t.get_fontsize(),
        family=t.get_fontfamily(), style=t.get_fontstyle(), weight=t.get_fontweight(),
        rotation=t.get_rotation(), color=t.get_color(),
        horizontalalignment=t.get_ha(), verticalalignment=t.get_va(),
        transform=t.get_transform().get_matrix(), visible=t.get_visible(),
    ))


def protected_state(fig):
    """Everything displayed except the approved six title strings."""
    fig.canvas.draw()
    axes = []
    for ax in fig.axes:
        axes.append(clean(dict(
            position=ax.get_position().bounds, xlim=ax.get_xlim(), ylim=ax.get_ylim(),
            xscale=ax.get_xscale(), yscale=ax.get_yscale(),
            xticks=ax.get_xticks(), yticks=ax.get_yticks(),
            xticklabels=[text_state(t) for t in ax.get_xticklabels()],
            yticklabels=[text_state(t) for t in ax.get_yticklabels()],
            xlabel=text_state(ax.xaxis.label), ylabel=text_state(ax.yaxis.label),
            lines=[line_state(x) for x in ax.lines],
            collections=[collection_state(x) for x in ax.collections],
            xgrid=[line_state(x) for x in ax.get_xgridlines()],
            ygrid=[line_state(x) for x in ax.get_ygridlines()],
            other_text=[text_state(t) for t in ax.texts],
            facecolor=ax.get_facecolor(),
            title_style={k: v for k, v in text_state(ax.title).items() if k != "text"},
        )))
    return clean(dict(
        size_inches=fig.get_size_inches(), dpi=fig.dpi, axes=axes,
        figure_text=[text_state(t) for t in fig.texts],
        legends=[dict(texts=[text_state(t) for t in leg.get_texts()],
                      lines=[line_state(x) for x in leg.get_lines()],
                      bbox=leg.get_bbox_to_anchor().bounds) for leg in fig.legends],
    ))


class ApprovedTitleChange(ast.NodeTransformer):
    def __init__(self, name):
        self.name = name
        self.changes = 0

    def visit_Call(self, node):
        node = self.generic_visit(node)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "set_title":
            literal = ("f'{window}-week training history'" if self.name == "cftc"
                       else "f'{arm.capitalize()} | {window} training labels'")
            node.args[0] = ast.parse(literal, mode="eval").body
            self.changes += 1
        return node


def load_pure_plotters(source, reports, changed):
    parsed = ast.parse(source)
    names = {"arr", "figure_geometry", "setup", "base", "cftc", "menu"}
    definitions = []
    modifications = []
    for item in parsed.body:
        if not isinstance(item, ast.FunctionDef) or item.name not in names:
            continue
        item = copy.deepcopy(item)
        if item.name in {"cftc", "menu"}:
            body = []
            for statement in item.body:
                if isinstance(statement, ast.Assert) and any(
                    isinstance(n, ast.Name) and n.id == "BEFORE" for n in ast.walk(statement)
                ):
                    continue
                if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Call):
                    fn = statement.value.func
                    if isinstance(fn, ast.Name) and fn.id == "original_fig":
                        statement.value = ast.Constant(None)
                body.append(statement)
            item.body = body
            if changed:
                transformer = ApprovedTitleChange(item.name)
                item = transformer.visit(item)
                assert transformer.changes == 1, item.name
                modifications.append(item.name + ":set_title text only")
        definitions.append(item)
    assert len(definitions) == len(names)
    tree = ast.fix_missing_locations(ast.Module(body=definitions, type_ignores=[]))
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))
    forbidden = {"original_fig", "module", "forecast_report", "evaluate_method"}
    assert not any(isinstance(n, ast.Name) and n.id in forbidden for n in ast.walk(tree))
    namespace = dict(
        np=np, plt=plt, Line2D=Line2D, FuncFormatter=FuncFormatter,
        MaxNLocator=MaxNLocator, BLUE="#0072B2", PURPLE="#CC79A7", INK="#222222",
        METHOD={"QR33": "Full regression", "QR4": "Four-feature"},
        STEMS=["v9-endpoint-peak-example", "v10-cftc-contract-changes", "v10-menu-isolation"],
        js=lambda path: copy.deepcopy(reports[path]),
        save=lambda fig, stem, before, binding: (fig, stem, binding),
    )
    exec(compile(tree, SOURCE + (":approved-titles" if changed else ":baseline"), "exec"), namespace)
    return namespace, modifications


def pdf_bytes(fig):
    result = io.BytesIO()
    fig.savefig(result, format="pdf", dpi=220,
                metadata={"CreationDate": None, "ModDate": None})
    return result.getvalue()


def numeric_tokens(pdf):
    text = PdfReader(io.BytesIO(pdf)).pages[0].extract_text()
    return re.findall(r"[−-]?(?:\d+(?:\.\d+)?|\.\d+)", text)


def non_title_pdf_text(pdf, titles):
    records = []
    def visitor(text, cm, tm, font, size):
        normalized = " ".join(text.split())
        if normalized and normalized not in titles:
            records.append(dict(text=normalized, cm=cm, tm=tm, font_size=size))
    PdfReader(io.BytesIO(pdf)).pages[0].extract_text(visitor_text=visitor)
    return records


def check_no_clipping(fig):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = fig.bbox
    inactive = set()
    for ax in fig.axes:
        for axis, limits in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            for tick in axis.get_major_ticks():
                if not min(limits) <= tick.get_loc() <= max(limits):
                    inactive.update((id(tick.label1), id(tick.label2)))
    clipped = []
    for t in fig.findobj(Text):
        if id(t) in inactive or not t.get_visible() or not t.get_text():
            continue
        b = t.get_window_extent(renderer)
        if b.x0 < -1 or b.y0 < -1 or b.x1 > bbox.width + 1 or b.y1 > bbox.height + 1:
            clipped.append(t.get_text())
    assert not clipped, clipped
    return clipped


def min_pdf_font(pdf):
    values = []
    def visitor(text, cm, tm, font, size):
        if text.strip():
            values.append(size * math.hypot(tm[2]*cm[0]+tm[3]*cm[2],
                                             tm[2]*cm[1]+tm[3]*cm[3]))
    PdfReader(io.BytesIO(pdf)).pages[0].extract_text(visitor_text=visitor)
    return min(values)


def main():
    if "--execute" not in sys.argv:
        raise SystemExit("Use --execute for the two authorized display-only PDF updates.")
    output_json = HERE / "history-figure-style-check.json"
    output_md = HERE / "history-figure-style-check.md"
    assert not output_json.exists() and not output_md.exists(), "Refusing receipt overwrite"
    source = tracked_blob(SOURCE)
    saved_bytes = tracked_blob(SAVED_RECEIPT)
    saved = json.loads(saved_bytes)
    paths = ["results/v10/cftc/report-values.json", "results/v10/menu/report-values.json"]
    raw = {path: tracked_blob(path) for path in paths}
    reports = {path: json.loads(data) for path, data in raw.items()}
    assert all(digest(raw[path]) == saved["sources_sha256"][path] for path in paths)
    original, _ = load_pure_plotters(source, reports, False)
    updated, changes = load_pure_plotters(source, reports, True)
    entries = []
    pending = []
    original_others = {p.name: digest(p.read_bytes()) for p in (ROOT/"submission-final/figures").glob("*.pdf")
                       if p.stem not in {"v10-cftc-contract-changes", "v10-menu-isolation"}}
    for name, scale in (("cftc", .97*160*72/25.4/450), ("menu", .98*170*72/25.4/450)):
        oldfig, stem, old_binding = original[name]()
        newfig, _, new_binding = updated[name]()
        old_state, new_state = protected_state(oldfig), protected_state(newfig)
        assert old_state == new_state, "PROTECTED_DISPLAY_STATE_DRIFT:" + stem
        arrays = original["figure_geometry"](oldfig)
        new_arrays = updated["figure_geometry"](newfig)
        inherited = next(x for x in saved["figures"] if x["figure"] == stem)
        assert arrays == new_arrays == inherited["after_artist_arrays"], "SAVED_ARTIST_ARRAY_DRIFT:" + stem
        assert old_binding == new_binding
        old_titles = [ax.get_title() for ax in oldfig.axes]
        new_titles = [ax.get_title() for ax in newfig.axes]
        before = ROOT / "submission-final/figures" / (stem + ".pdf")
        current_bytes = before.read_bytes()
        original_path = "submission-v10/figures/" + stem + ".pdf"
        v13_bytes = git_blob(original_path)
        assert current_bytes == v13_bytes, "PRE_EDIT_CANONICAL_NOT_V13:" + stem
        assert digest(v13_bytes) == inherited["after_pdf_sha256"]
        check_no_clipping(newfig)
        old_recreated = pdf_bytes(oldfig)
        after = pdf_bytes(newfig)
        assert numeric_tokens(v13_bytes) == numeric_tokens(after), "NUMERIC_TEXT_DRIFT:" + stem
        assert non_title_pdf_text(v13_bytes, old_titles) == non_title_pdf_text(after, new_titles), "OTHER_PDF_TEXT_OR_POSITION_DRIFT:" + stem
        font = min_pdf_font(after)
        assert font*scale >= 7
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(before.relative_to(ROOT))],
                                 cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
        backup = None
        if not tracked:
            backup = before.with_suffix(before.suffix + ".bak")
            assert not backup.exists(), "Refusing .bak overwrite"
            shutil.copy2(before, backup)
        entry = dict(
            figure=stem, canonical_path=str(before.relative_to(ROOT)),
            pre_edit_tracked=tracked, non_git_backup=str(backup) if backup else None,
            original_v13_pdf_path=original_path, original_v13_sha256=digest(v13_bytes),
            pre_edit_canonical_sha256=digest(current_bytes), after_sha256=digest(after),
            recreated_original_pdf_sha256=digest(old_recreated),
            recreated_original_pdf_byte_identical=(old_recreated == v13_bytes),
            title_map=[dict(before=a, after=b) for a,b in zip(old_titles,new_titles)],
            numeric_text_tokens=numeric_tokens(after), numeric_text_equal=True,
            non_title_pdf_text_and_positions_equal=True,
            saved_artist_arrays=arrays, output_artist_arrays=new_arrays,
            saved_artist_arrays_equal=True,
            artist_array_sha256=digest(json.dumps(arrays,sort_keys=True).encode()),
            protected_artist_style_and_geometry=old_state,
            protected_artist_style_and_geometry_equal=True,
            protected_style_sha256=digest(json.dumps(old_state,sort_keys=True).encode()),
            report_values_path=paths[0 if name=="cftc" else 1],
            source_binding=new_binding, clipped_text=[],
            source_minimum_font_bp=font, current_include_scale=scale,
            printed_minimum_font_bp=font*scale, font_gate_7bp="PASS",
            color_directly_viewed=False, grayscale_directly_viewed=False,
        )
        entries.append(entry)
        pending.append((before, after, stem))
        plt.close(oldfig); plt.close(newfig)
    # All numerical, style, geometry, text and font checks finish before either replacement.
    for path, after, stem in pending:
        path.write_bytes(after)
        for mode, extra in (("color", []), ("gray", ["-gray"])):
            prefix = QA / (stem + "-" + mode)
            assert not prefix.with_suffix(".png").exists()
            subprocess.run(["pdftoppm","-f","1","-singlefile","-r","150","-png",*extra,
                            str(path),str(prefix)], check=True, capture_output=True)
        a=Image.open(QA/(stem+"-color.png")).convert("RGB")
        b=Image.open(QA/(stem+"-gray.png")).convert("RGB")
        pair=Image.new("RGB",(a.width+b.width+20,max(a.height,b.height)),"white")
        pair.paste(a,(0,0));pair.paste(b,(a.width+20,0));pair.save(QA/(stem+"-comparison.png"))
    assert original_others == {p.name:digest(p.read_bytes()) for p in (ROOT/"submission-final/figures").glob("*.pdf")
                               if p.stem not in {"v10-cftc-contract-changes", "v10-menu-isolation"}}
    assert all((ROOT/p).read_bytes() == raw[p] for p in paths)
    assert (ROOT/SOURCE).read_bytes() == source and (ROOT/SAVED_RECEIPT).read_bytes() == saved_bytes
    receipt=dict(
        schema="submission-history-title-style-v1", status="STRUCTURAL_PASS_AWAITING_DIRECT_RENDER_REVIEW",
        created_utc=datetime.now(timezone.utc).isoformat(), source_commit=BASE,
        code_path=str(Path(__file__).relative_to(ROOT)), code_sha256=digest(Path(__file__).read_bytes()),
        source_materials=[dict(path=SOURCE,sha256=digest(source)),dict(path=SAVED_RECEIPT,sha256=digest(saved_bytes))]
                        +[dict(path=p,sha256=digest(raw[p])) for p in paths],
        pure_ast_definitions=["arr","figure_geometry","setup","base","cftc","menu"],
        display_ast_changes=changes,
        original_untracked_BEFORE_cache_accessed=False, model_or_runner_imported=False,
        financial_statistic_recomputed=False, raw_financial_inputs_read=False,
        figures=entries, unrelated_eight_figures_unchanged=True,
        source_code_and_results_unchanged=True, canonical_PDFs_changed=2,
        matplotlib_version=matplotlib.__version__, numpy_version=np.__version__,
        python_executable=sys.executable, render_directory=str(QA.relative_to(ROOT)),
    )
    output_json.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    lines=["# Two history-title clarifications", "", "Structural checks pass; direct color/grayscale render review pending.",
           "", "Only the two authorized canonical PDF titles changed. No caption, result, data, original plotting source, model or runner was changed or executed.", ""]
    for e in entries:
        lines += ["## "+e["figure"],"", "- v13/pre-edit SHA256: `"+e["original_v13_sha256"]+"`",
                  "- New SHA256: `"+e["after_sha256"]+"`",
                  "- Numeric text, tracked saved artist arrays, all non-title PDF text/positions, colors, markers, error bars, axis limits and protected geometry: exact equality.",
                  "- Printed minimum font: "+format(e["printed_minimum_font_bp"],".6f")+"bp; PASS at current include width."]
        lines += ["- `"+t["before"]+"` -> `"+t["after"]+"`" for t in e["title_map"]]
        lines += [""]
    lines += ["All materials came from pinned tracked files, including notes/v10b/visual-style-report.json. The legacy BEFORE cache and dynamic original_fig importer were excluded from the executed AST.", ""]
    output_md.write_text("\n".join(lines))
    print(json.dumps(dict(status=receipt["status"], figures=[dict(figure=e["figure"],
                         original_recreated_exact=e["recreated_original_pdf_byte_identical"],
                         old=e["pre_edit_canonical_sha256"],new=e["after_sha256"],
                         font=e["printed_minimum_font_bp"]) for e in entries])))


if __name__ == "__main__":
    main()
