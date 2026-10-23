"""Build aggregate-only tables/figures for the separately compiled TeX revision.

The manuscript PDF is produced by Tectonic, never by this figure renderer.
Frozen originals are read only. All generated outputs are revision-specific.
"""
from pathlib import Path
import csv
import json
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, black, white

ROOT = Path(__file__).resolve().parent
DOC = ROOT / "manuscript/supervisor-revision"
GEN = DOC / "generated"
FIG = DOC / "figures"
NEW = ROOT / "results/supervisor-20261023"
OLD = ROOT / "results/revision-20261022"
BLUE = HexColor("#236A91")
RED = HexColor("#B24C42")
GREY = HexColor("#66727D")
LIGHT = HexColor("#D9E0E5")


def rows(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def tex(s):
    s = str(s).replace("–", "--").replace("—", "---").replace("’", "'")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#")]:
        s = s.replace(a, b)
    return s


def pval(x):
    if x in (None, ""):
        return "--"
    x = float(x)
    return "$<.001$" if x < .001 else f"{x:.3f}"


def table(name, caption, label, columns, data, align=None, note="", fontsize="small"):
    align = align or "l" + "r" * (len(columns) - 1)
    align = align.replace("p{", r">{\raggedright\arraybackslash}p{")
    out = [r"\begin{table}[!htbp]", "\\centering\\" + fontsize,
           "\\caption{" + caption + "}\\label{" + label + "}",
           r"\begin{tabular}{" + align + "}", r"\toprule",
           " & ".join(columns) + r" \\", r"\midrule"]
    out += [" & ".join(map(str, r)) + r" \\" for r in data]
    out += [r"\bottomrule", r"\end{tabular}"]
    if note:
        out += [r"\par\smallskip\begin{minipage}{\linewidth}\footnotesize " + note + r"\end{minipage}"]
    out += [r"\end{table}", ""]
    (GEN / name).write_text("\n".join(out))


def build_tables():
    # Short display cells retain exactly the scope of the full audited JSON.
    literature = [
        ["Boudoukh et al. (2004)", "Worst intermediate portfolio-value loss", "Modeled portfolio paths", "First-passage formula; discrete simulation", "MaxVaR/VaR ratios and parameter illustrations"],
        ["Petrunia et al. (2019)", "Largest daily endpoint debit across ACSS participants", "ACSS settlement balances", "GEV blocks; GPD exceedances", "Quantile diagnostics; monthly collateral shortfalls"],
        ["van den Hoogen (2017)", "Maximum cumulative negative payment balance", "Confidential bank transactions", "Modeled transaction paths; EVT", "UC and independence procedures; outcomes confidential"],
        ["Wisniewski et al. (2020)", "Next-hour signed-position interval", "Same FX source family", "Quantile/conformal intervals; KNN and other regressions", "Two endpoint pinball scores; interval and coverage diagnostics"],
        ["This paper", "Two-sided absolute sampled peak quantile", "FX record; Treasury aggregate", "Historical rules; QR/KNN on matched histories", "Pinball, paired DM, U/V, breaches and coverage diagnostics"],
    ]
    audit = json.loads((NEW / "literature-table.json").read_text())
    assert len(audit["rows"]) == len(literature) == 5
    table("literature-table.tex", "Closest studies and the present comparison.", "tab:literature",
          ["Study", "Target", "Data", "Method", "Evaluation"], literature,
          align="p{.14\\linewidth}p{.20\\linewidth}p{.14\\linewidth}p{.20\\linewidth}p{.20\\linewidth}",
          note="The FX relationship concerns the source family. The public thesis specifies backtests but withholds its application outcomes.", fontsize="footnotesize")
    table("data-table.tex", "Source-specific chronological budgets. Dates are issue dates; all horizons share the same evaluation issues.", "tab:data",
          ["Source", "Full record", "Validation", "Evaluation", "$W$ / $d$"],
          [["FX", "2014-02-05 to 2017-01-24", "2015-10-08 to 2015-12-30", "2016-01-01 to 2017-01-23", "720 or 2880 / 24"],
           ["Treasury", "2013-04-03 to 2026-10-07", "2019-07-24 to 2020-07-15", "2021-01-06 to 2026-04-22", "52 or 260 / 13"]],
          align="lp{.20\\linewidth}p{.20\\linewidth}p{.20\\linewidth}p{.17\\linewidth}",
          note="FX has 1,440 validation and 6,625 evaluation issues; Treasury has 52 and 277. The longest validation response completes before evaluation starts. $H$ counts records, preserving recorded FX gaps.", fontsize="footnotesize")
    ready = rows(NEW / "inference/tables3-4-ready.csv")
    assert len(ready) == 48
    names = {"frozen_F": "$F$", "frozen_S": "$S$", "frozen_K": "$K$", "QR": "QR", "KNN": "KNN", "SCALED_KNN": "Scaled KNN"}
    for source, name, label, title in [("fx_hourly", "fx", "tab:fx", "FX"), ("nyfed_weekly", "treasury", "tab:treasury", "Treasury")]:
        subset = [r for r in ready if r["source"] == source]
        assert len(subset) == 24
        data = [[r["horizon"], r["window"], names[r["method"]], r["loss_display"], r["relative_display"], r["breach_rate_display"], r["holm_display"].replace("<", "$<").replace(".001", ".001$") if r["holm_display"].startswith("<") else r["holm_display"]] for r in subset]
        table(name + "-table.tex", title + " original reports, matched by horizon and history. Loss is in source-reported USD millions.", label,
              ["$H$", "$W$", "Report", "Mean loss", "$\\Delta_F$ (\\%)", "Breach (\\%)", "$p_{\\rm Holm}$"], data,
              align="rrlrrrr", note="Every relative change uses its own frozen $F$. Holm adjustment covers the original 72 matched conditional-versus-$F/S/K$ contrasts. Dashes mark self-references, historical contrasts outside that family, or the exact full-pool KNN identity. Identical-loss cells receive input one solely for conservative family bookkeeping. Percentages and loss are computed before display rounding.")
    cov = rows(NEW / "inference/coverage-verified.csv")
    covkeys = [("fx_hourly", "6", "2880", "QR"), ("nyfed_weekly", "6", "260", "QR"), ("nyfed_weekly", "6", "260", "frozen_F")]
    data = []
    for key in covkeys:
        r = next(r for r in cov if tuple(r[k] for k in ["source", "horizon", "window", "method"]) == key)
        data.append([("FX" if key[0] == "fx_hourly" else "Treasury") + " " + names[key[3]], r["n"], r["hits"], f"{100*float(r['rate']):.3f}", pval(r["pof_p"]), pval(r["ind_p"]), pval(r["cc_p"])])
    table("coverage-table.tex", "Six-step coverage diagnostics on the fixed nonoverlap grid.", "tab:coverage",
          ["Report", "$n$", "Breaches", "Rate (\\%)", "$p_{\\rm POF}$", "$p_{\\rm IND}$", "$p_{\\rm CC}$"], data,
          align="lrrrrrr", note="POF uses every retained hit. IND and CC condition on the first hit; their likelihoods therefore use the subsequent transitions consistently. Values are asymptotic reference p-values for equality/independence nulls. Complete grids and the preserved earlier initialization convention are in the inference supplement.")
    e3 = rows(NEW / "e3/summary.csv")
    pairs = rows(NEW / "e3/paired-dm.csv")
    e6 = rows(NEW / "e6/table6.csv")
    data = []
    for r in sorted(e6, key=lambda r: (r["source"] != "fx_hourly", int(r["horizon"]), int(r["window"]))):
        data.append(["FX" if r["source"] == "fx_hourly" else "Treasury", r["horizon"], r["window"], f"{float(r['extended33_selected_penalty']):g}", *[f"{float(r[k]):+.2f}" for k in ["original33_percent_vs_frozen_F", "four_percent_vs_frozen_F", "extended33_percent_vs_frozen_F", "I_percent_vs_frozen_F"]], r["extended33_breaches"]])
    table("e3-table.tex", "Penalty-menu expansion and the intercept-only reference. Loss changes relative to frozen $F$ (percent); the final column counts strict breaches.", "tab:e3",
          ["Source", "$H$", "$W$", "$\\lambda$ (33+)", "Original 33", "Four+", "33+", "$I$", "Breaches (33+)"], data,
          align="lrrrrrrrr", fontsize="footnotesize", note="Plus denotes the common menu $\\{.001,.01,.1,1,10\\}$. Original 33 retains its smaller menu. $I$ uses the ordinary empirical headroom quantile at $\\lceil .95W\\rceil$; it is a $\\lambda\\to\\infty$ reference, with a minimizer interval when $.95W$ is integral. $F$ instead uses $\\lceil .95(W+1)\\rceil$. Each predictor set selects its own penalty by the same validation rule. All eight cells and all 40 candidates completed. Common-menu paired tests, the separate 28-comparison E3 adjustment, HLN and doubled-bandwidth results remain in the supplement.")
    treasury = [r for r in e6 if r["source"] == "nyfed_weekly"]
    primary = next(r for r in treasury if r["horizon"] == "6" and r["window"] == "260")
    endpoint_count = sum(r["selected_at_extended_menu_upper_endpoint"] == "True" for r in treasury)
    i_changes = ", ".join(f"${float(r['I_percent_vs_frozen_F']):+.1f}$\\%" for r in treasury)
    (GEN / "e6-summary.tex").write_text(
        f"The intercept-only reference helps locate the remaining Treasury differences. In the displayed Treasury order, $I$ changes loss by {i_changes} relative to $F$. The expanded full regression selects the menu's upper endpoint in {endpoint_count} of {len(treasury)} Treasury cells. At the main Treasury setting, expanded QR has {primary['extended33_breaches']} strict breaches, compared with {primary['frozen_F_breaches']} for $F$ and {primary['original33_breaches']} for original QR. Stronger shrinkage therefore narrows the score deterioration without restoring the historical breach count.\\n".replace("\\n", "\n"))
    decomp = rows(NEW / "e3/primary-decomposition.csv")
    round2 = NEW / "round2"
    round2.mkdir(exist_ok=True)
    (round2 / "document-inputs.json").write_text(json.dumps({"table3_4_rows": len(ready), "e3_cells": len(e3), "e6_cells": len(e6), "decomposition_rows": len(decomp), "original_archives_read_only": True}, indent=2) + "\n")
    # Direct columns are intentionally selected by schema, never reconstructed from rounded paper values.
    method_names = {"rolling_F": "Rolling $F_{720}$", "frozen_F": "Frozen $F$", "four_predictor_extended_menu": "Four+", "33_predictor_extended_menu": "33+", "33_predictor_original_menu": "Original 33"}
    data = []
    for r in decomp:
        source = "FX" if r["source"] == "fx_hourly" else "Treasury"
        old = method_names[r["old_method"]]
        new = method_names[r["new_method"]]
        if r["old_method"] == r["new_method"] == "frozen_F":
            old, new = "Frozen $F_{720}$", "Frozen $F_{2880}$"
        data.append([source, old + "$\\to$" + new, f"{float(r['relative_percent']):+.3f}", f"{float(r['percentage_points_of_initial_loss']):+.3f}", pval(r.get("dm_p")), pval(r.get("hln_p"))])
    table("decomposition-table.tex", "Ordered six-step changes ending at the original main comparisons.", "tab:decomp",
          ["Source", "Change", "Step (\\%)", "Initial (pp)", "$p_{\\rm DM}$", "$p_{\\rm HLN}$"], data,
          align="llrrrr", fontsize="footnotesize", note="Step percentages use the preceding row's loss and compound. Initial percentage points use the chain's common starting loss and sum to the original total. The last Treasury step restricts the ridge menu again, separating that change from the common-menu predictor comparison. Dashes denote identical losses. Tests are exploratory and unadjusted here; the declared E3 family and twice-bandwidth checks are in the supplement.")
    (GEN / "e3-summary.tex").write_text("""A wider penalty menu largely removes the original Treasury deterioration. At the main Treasury setting, the full regression's excess loss relative to $F$ falls from 50.8\\% to 3.43\\%. Its penalty changes from 0.001 to one. Under the common menu, the full predictor set increases loss by 1.24\\% relative to the parsimonious regression, with a descriptive p-value of 0.685. The small difference leaves substantial uncertainty; it is not an equivalence result. Across the Treasury cells, the full model's matched-$F$ changes now range from a modest improvement to a modest deterioration.

The FX gain persists under the wider menu. Every FX selection and issued report agrees with the original full specification. At the long history, changing from the parsimonious to the full predictor set reduces loss by 10.9\\%, with an E3-adjusted HAC p-value below 0.001. Changing from frozen $F$ to the parsimonious model yields a smaller reduction; that step has an unadjusted p-value of 0.010 and an E3-adjusted value of 0.251. Table~\\ref{tab:decomp} retains every step, including the update and history changes.

The revised interpretation concerns regularization and specification jointly. Stronger shrinkage is useful for the weekly Treasury histories, while the long-history FX specification retains its gain. The shared-menu comparison permits each feature set to select its own penalty. Its order-dependent differences support a conditional comparison of procedures, rather than a causal attribution to a particular predictor or a universal dimension rule.
""")
    # Named U/V comparisons from the immutable original paired table.
    pairsold = rows(OLD / "paired-comparisons.csv")
    ids = ["fx_hourly-h6-QR2880-minus-rolling_F720", "fx_hourly-h6-QR2880-minus-frozen_F2880", "fx_hourly-h24-QR2880-minus-rolling_S720", "nyfed_weekly-h6-QR260-minus-frozen_F260"]
    uvdata = []
    for cid, label in zip(ids, ["FX six-step primary", "FX six-step matched", "FX longer-horizon legacy", "Treasury primary"]):
        r = next(r for r in pairsold if r["contrast_id"] == cid)
        scale = 1e6 if r["source"] == "fx_hourly" else 1
        u, v = [float(r[k]) / scale for k in ["mean_positive_overrun_difference", "mean_unused_allowance_difference"]]
        crossing = "--" if u*v >= 0 else f"{-v/u:.3f}"
        uvdata.append([label, f"{u:+.3f}", f"{v:+.3f}", crossing, r["strict_breach_count_left"] + "/" + r["strict_breach_count_right"]])
    table("uv-table.tex", "Error components and strict breaches for the original named comparisons.", "tab:uv", ["Comparison", "$\\Delta U$", "$\\Delta V$", "Crossing $\\omega$", "Breaches A/B"], uvdata,
          align="lrrrr", note="A is regression and B its named reference. Amounts are in source-reported USD millions, with distinct source measurement processes. Negative component differences favor A. A missing crossing means both components have the same sign. The weights describe hypothetical fixed-report preferences.")
    table("robustness-table.tex", "Compact robustness summary; the complete original outputs are retained.", "tab:robustness", ["Check", "Finding", "Interpretation"],
          [["AR residual replay", "Lower loss than translated paths in five cells; more breaches in every cell", "Conditional-family rankings differ"],
           ["Rank convention", "Ordinary versus corrected rank changes some finite reports; full-pool identities persist", "Report construction matters"],
           ["Fixed linear weights", "FX short-horizon components both fall; longer-horizon crossing near the original weight", "Mean score and breach count differ"],
           ["Horizon order", "Targets are ordered; fitted reports can cross", "Separate fits need an explicit reconciliation criterion"]],
          align="p{.19\\linewidth}p{.47\\linewidth}p{.23\\linewidth}", fontsize="footnotesize")
    # Only original Table B1 stays printed. Its cells are copied directly, rounding for display.
    content = json.loads((DOC.parent / "working-paper/paper-content.json").read_text())
    sec = next(s for s in content["sections"] if s["title"].startswith("Appendix B"))
    original = next(b for b in sec["blocks"] if b["type"] == "table")
    # Actual baseline schema is inspected rather than assuming HTML table contents.
    data = [[tex(r[0])] + [f"{float(v):.3f}" for v in r[1:-1]] + [f"{float(r[-1]):+.3f}"] for r in original["rows"]]
    table("earlier-table.tex", "Original historical construction grid; mean FX losses in USD millions.", "tab:old", ["Setting", "$F$", "$S$", "$R$", "$K$", "$C^{\\rm floor}$", "$F-S$"], data,
          align="lrrrrrr", note="Each sensitivity changes one factor from the original six-step setting. All rows retain the same evaluation issues; different score preferences are separate tasks. The displayed +0.000 in the tau90 row is positive before rounding.")


def start_pdf(name, width, height):
    c = canvas.Canvas(str(FIG / name), pagesize=(width, height), pageCompression=1)
    c.setTitle(name.removesuffix(".pdf").replace("-", " "))
    c.setAuthor("")
    c.setFont("Helvetica", 9)
    return c


def label(c, x, y, text, size=9, color=black, align="left"):
    c.setFont("Helvetica", max(9, size*1.15))
    c.setFillColor(color)
    {"left": c.drawString, "right": c.drawRightString, "center": c.drawCentredString}[align](x, y, text)


def path_figure():
    c = start_pdf("path-target.pdf", 470, 200)
    x0, x1, y0, y1 = 45, 430, 32, 175
    px = lambda i: x0 + (x1-x0)*i/5
    py = lambda v: y0 + (v+7)/11*(y1-y0)
    c.setStrokeColor(LIGHT)
    for v in [-6, 0, 2]:
        c.line(x0, py(v), x1, py(v)); label(c, x0-9, py(v)-3, str(v), 8, GREY, "right")
    vals = [2, 3, -1, -6, -2, 1.2]
    c.setStrokeColor(BLUE); c.setLineWidth(1.8)
    for i in range(5): c.line(px(i), py(vals[i]), px(i+1), py(vals[i+1]))
    for i, v in enumerate(vals): c.setFillColor(BLUE); c.circle(px(i), py(v), 2.8, fill=1, stroke=0)
    label(c, 48, 181, "Signed sampled position", 10)
    label(c, px(0)+6, py(2)-18, "Issue magnitude B", 9)
    label(c, px(3)-15, py(-6)-15, "Peak magnitude P", 9, RED, "center")
    label(c, px(5), py(1.2)+10, "Endpoint magnitude", 9, BLUE, "right")
    label(c, x0, 12, "Issue", 8, GREY, "center"); label(c, x1, 12, "Horizon", 8, GREY, "center")
    c.save()


def waterfall():
    c = start_pdf("decomposition.pdf", 600, 245)
    e3 = rows(NEW / "e3/primary-decomposition.csv")
    for panel, source in enumerate(["fx_hourly", "nyfed_weekly"]):
        rr = [r for r in e3 if r["source"] == source]
        x0, width, y0, h = 43+panel*298, 245, 70, 137
        y = lambda v: y0 + (v-80)/80*h
        c.setStrokeColor(LIGHT)
        for tick in [80,100,120,140,160]:
            c.line(x0,y(tick),x0+width,y(tick)); label(c,x0-6,y(tick)-3,str(tick),7,GREY,"right")
        title = "FX: six-step, original rolling reference" if panel == 0 else "Treasury: six-step, W=260"
        label(c,x0,225,title,9)
        initial = float(rr[0]["old_mean_pinball"])
        values = [100]+[100*float(r["new_mean_pinball"])/initial for r in rr]
        labs = (["Rolling F", "Frozen F", "Long F", "Four+", "33+", "Orig. 33"] if panel == 0 else ["Frozen F", "Four+", "33+", "Orig. 33"])
        spacing=width/len(values);bw=min(27,spacing*.65)
        for i, val in enumerate(values):
            x=x0+(i+.5)*spacing
            old=80 if i==0 else values[i-1]
            c.setFillColor(GREY if i==0 else (BLUE if val<=old else RED)); c.setStrokeColor(GREY)
            if abs(val-old)<1e-9: c.line(x-bw/2,y(val),x+bw/2,y(val))
            else: c.rect(x-bw/2,y(min(old,val)),bw,abs(y(val)-y(old)),fill=1,stroke=0)
            if i: c.setStrokeColor(GREY);c.setLineWidth(.5);c.line(x-spacing+bw/2,y(old),x-bw/2,y(old))
            label(c,x,y(val)+5,f"{val:.1f}",8,black,"center")
            for j, bit in enumerate(labs[i].split(" ")): label(c,x,49-j*10,bit,7,black,"center")
        label(c,x0,17,"Common starting loss = 100; blue lowers mean loss",8,GREY)
    c.save()


def error_figure():
    c=start_pdf("error-components.pdf",600,193)
    paired=rows(OLD/"paired-comparisons.csv")
    ids=["fx_hourly-h6-QR2880-minus-rolling_F720","fx_hourly-h24-QR2880-minus-rolling_S720","nyfed_weekly-h6-QR260-minus-frozen_F260"]
    labels=["FX six-step","FX longer horizon","Treasury six-step"]
    # Recover exact component references from score, paired difference and summaries.
    cells=rows(OLD/"evaluation-summary.csv")
    for pi,(field,title) in enumerate([("U","Mean underprediction (U)"),("V","Mean overprediction (V)"),("B","Strict breaches (pp)")]):
        x0=147+pi*148; span=116
        values=[]
        for cid in ids:
            r=next(r for r in paired if r["contrast_id"]==cid)
            if field=="B": val=100*(int(r["strict_breach_count_left"])-int(r["strict_breach_count_right"]))/int(r["origin_count"])
            else:
                metric="mean_positive_overrun" if field=="U" else "mean_unused_allowance"
                left=next(q for q in cells if q["source"]==r["source"] and q["horizon"]==r["horizon"] and q["window"]==r["left_window"] and q["method"]==r["left_method"])
                diff=float(r[metric+"_difference"]);ref=float(left[metric])-diff;val=100*diff/ref
            values.append(val)
        bound=max(1,max(abs(v) for v in values))*1.18
        zero=x0+span*.5
        c.setStrokeColor(LIGHT);c.line(zero,35,zero,150)
        label(c,x0+span/2,174,title,8,black,"center")
        for ri,(v,lab) in enumerate(zip(values,labels)):
            y=135-ri*42; end=zero+v/bound*span*.47
            c.setFillColor(BLUE if v<0 else RED);c.rect(min(zero,end),y-5,max(.4,abs(end-zero)),10,fill=1,stroke=0)
            label(c,zero,y+9,f"{v:+.1f}"+("%" if field!="B" else ""),8,black,"center")
            if pi==0:label(c,8,y-3,lab,9)
        label(c,x0+span/2,17,"Change / own reference" if field!="B" else "Percentage-point change",7,GREY,"center")
    c.save()


def murphy():
    c=start_pdf("murphy.pdf",600,178)
    directory=NEW/"inference/inherited-exact"
    for pi,source in enumerate(["fx_hourly","nyfed_weekly"]):
        paths=list(directory.rglob("murphy-"+source+"-display.csv"))
        assert len(paths)==1,paths
        rr=rows(paths[0]);xkey=next(k for k in rr[0] if k.startswith("theta"))
        xs=[float(r[xkey]) for r in rr];ys=[float(r["left_elementary"])-float(r["right_elementary"]) for r in rr]
        x0,x1,y0,y1=43+pi*299,282+pi*299,39,140
        xmin,xmax=min(xs),max(xs);bound=max(map(abs,ys))*1.15
        px=lambda v:x0+(v-xmin)/(xmax-xmin)*(x1-x0)
        py=lambda v:(y0+y1)/2+v/bound*(y1-y0)/2
        c.setStrokeColor(LIGHT);c.line(x0,py(0),x1,py(0))
        c.setStrokeColor(BLUE);c.setLineWidth(1)
        for i in range(len(xs)-1):c.line(px(xs[i]),py(ys[i]),px(xs[i+1]),py(ys[i+1]))
        label(c,x0,158,"FX" if pi==0 else "Treasury",10)
        label(c,x0,y0-13,f"{xmin:.1f}",8,GREY);label(c,x1,y0-13,f"{xmax:.1f}",8,GREY,"right")
        label(c,(x0+x1)/2,8,"Threshold in source-reported USD millions",8,GREY,"center")
        label(c,x0-4,py(0)-3,"0",8,GREY,"right")
        label(c,x0-4,y1-3,f"{bound:.3f}",7,GREY,"right")
        label(c,x0-4,y0-3,f"{-bound:.3f}",7,GREY,"right")
    c.save()


def lambda_path():
    path = rows(NEW / "e6/lambda-path.csv")
    refs = rows(NEW / "e6/lambda-path-I.csv")
    c = start_pdf("lambda-path.pdf", 600, 235)
    for panel, source in enumerate(["fx_hourly", "nyfed_weekly"]):
        subset = [r for r in path if r["source"] == source]
        baseline = [r for r in refs if r["source"] == source]
        scale = 1e6 if source == "fx_hourly" else 1
        values = [float(r["mean_pinball"])/scale for r in subset + baseline if r["status"] == "COMPLETE"]
        lower, upper = min(values), max(values)
        pad = (upper-lower)*.12
        x0, x1, y0, y1 = 49+panel*300, 282+panel*300, 48, 187
        px = lambda v: x0+(math.log10(v)+3)/5*(x1-x0)
        py = lambda v: y0+(v-lower+pad)/(upper-lower+2*pad)*(y1-y0)
        label(c, x0, 216, "FX: original six-step long history" if panel == 0 else "Treasury: original six-step long history", 9)
        for j in range(4):
            val = lower-pad+(upper-lower+2*pad)*j/3
            c.setStrokeColor(LIGHT); c.line(x0,py(val),x1,py(val))
            label(c,x0-5,py(val)-3,f"{val:.2f}" if scale == 1e6 else f"{val:.0f}",8,GREY,"right")
        for phase, color in [("validation", BLUE), ("evaluation", RED)]:
            rr = sorted([r for r in subset if r["phase"] == phase and r["status"] == "COMPLETE"], key=lambda r:float(r["parameter"]))
            c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(1.2)
            for a,b in zip(rr,rr[1:]):
                c.line(px(float(a["parameter"])),py(float(a["mean_pinball"])/scale),px(float(b["parameter"])),py(float(b["mean_pinball"])/scale))
            for r in rr: c.circle(px(float(r["parameter"])),py(float(r["mean_pinball"])/scale),2.2,fill=1,stroke=0)
            ref = next(r for r in baseline if r["phase"] == phase)
            c.setDash(4,3); c.line(x0,py(float(ref["mean_pinball"])/scale),x1,py(float(ref["mean_pinball"])/scale)); c.setDash()
        for val in sorted({float(r["parameter"]) for r in subset}): label(c,px(val),y0-15,f"{val:g}",8,GREY,"center")
        label(c,x0,199,"Mean pinball loss (USD millions)",8,GREY)
        label(c,(x0+x1)/2,15,"Ridge penalty (log scale)",8,GREY,"center")
    label(c,300,3,"Blue: validation; red: evaluation; dashed: phase-specific intercept-only I",8,GREY,"center")
    c.save()


def main():
    GEN.mkdir(parents=True,exist_ok=True);FIG.mkdir(parents=True,exist_ok=True)
    build_tables();path_figure();waterfall();error_figure();murphy();lambda_path()
    print("Built revision-specific aggregate tables and vector figures; manuscript PDF requires Tectonic.")


if __name__=="__main__":main()
