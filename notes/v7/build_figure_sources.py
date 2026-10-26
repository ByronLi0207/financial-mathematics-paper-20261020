"""Draw the selected window and saved score grids using standard LaTeX.

Only affine page coordinates and tick labels are computed. Source paths,
capacities, elementary scores and scientific conclusions are unchanged.
No plotting package, software installation, forecast or test is needed.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "figure-sources"
BLUE = "0.08,0.28,0.52"
ORANGE = "0.72,0.25,0.06"


def text(x, y, content, align="c"):
    return rf"\put({x:.2f},{y:.2f}){{\makebox(0,0)[{align}]{{{content}}}}}"


def line(points, colour):
    commands = [r"{\color[rgb]{" + colour + r"}\linethickness{.8pt}"]
    for (x, y), (a, b) in zip(points, points[1:]):
        commands.append(rf"\qbezier({x:.2f},{y:.2f})({(x+a)/2:.2f},{(y+b)/2:.2f})({a:.2f},{b:.2f})")
    commands.append("}")
    return "\n".join(commands)


def source(name, xs, series, xlabel, ylabel, ticks=None):
    left, right, bottom, top = 66., 451., 48., 214.
    xmin, xmax = min(xs), max(xs)
    all_y = [v for _, ys, _ in series for v in ys]
    ymin, ymax = min(all_y), max(all_y)
    pad = max((ymax-ymin)*.06, 1e-10)
    ymin, ymax = ymin-pad, ymax+pad
    X = lambda x: left + (x-xmin)/(xmax-xmin)*(right-left)
    Y = lambda y: bottom + (y-ymin)/(ymax-ymin)*(top-bottom)
    commands = [r"\put(66,48){\line(1,0){385}}", r"\put(66,48){\line(0,1){166}}"]
    for j in range(5):
        value = ymin+(ymax-ymin)*j/4
        commands.extend([rf"\put(62,{Y(value):.2f}){{\line(1,0){{4}}}}", text(58,Y(value),format(value,".3g"),"r")])
    if ticks is None:
        ticks=[(xmin+(xmax-xmin)*j/4,format(xmin+(xmax-xmin)*j/4,".3g")) for j in range(5)]
    for value, label in ticks:
        commands.extend([rf"\put({X(value):.2f},44){{\line(0,1){{4}}}}", text(X(value),34,label)])
    commands.extend([text((left+right)/2,14,xlabel),text(left,230,ylabel,"l")])
    for j,(label,ys,colour) in enumerate(series):
        commands.append(line([(X(x),Y(y)) for x,y in zip(xs,ys)],colour))
        commands.append(text(245,263-j*13,r"{\color[rgb]{"+colour+"}"+label+"}"))
    doc=(r"""\documentclass[11pt]{article}
\usepackage[paperwidth=500pt,paperheight=290pt,margin=10pt]{geometry}
\usepackage[T1]{fontenc}\usepackage{color}
\setlength{\parindent}{0pt}\setlength{\topskip}{0pt}
\begin{document}\thispagestyle{empty}\noindent
\setlength{\unitlength}{1pt}\begin{picture}(480,270)
"""+"\n".join(commands)+"\n"+r"\end{picture}\end{document}"+"\n")
    (OUT/(name+".tex")).write_text(doc)


def main():
    OUT.mkdir(exist_ok=True)
    record=json.loads((HERE/"example-selection.json").read_text());e=record["selection"]
    ticks=[(j,date[5:] if len(date)>=10 else date) for j,date in enumerate(e["dates"])]
    source("v7-endpoint-peak-example",list(range(len(e["absolute_positions"]))),
           [("Observed absolute position",e["absolute_positions"],BLUE),
            ("Historical headroom limit",[e["report"]]*len(e["absolute_positions"]),ORANGE)],
           "Economic date", "USD millions",ticks)
    bindings=[dict(figure="v7-endpoint-peak-example",source="notes/v7/example-selection.json",
                   raw_series=e["absolute_positions"],capacity=e["report"],point_count=len(e["dates"]))]
    for name in ("fx_hourly","nyfed_weekly"):
        relative=Path("results/supervisor-20261023/inference/inherited-exact")/("murphy-"+name+"-display.csv")
        raw=(ROOT/relative).read_bytes();rows=list(csv.DictReader(raw.decode().splitlines()))
        source("v7-murphy-"+name,[float(row["theta_USD_millions"]) for row in rows],
               [("Conditional regression",[float(row["left_elementary"]) for row in rows],BLUE),
                ("Historical headroom reference",[float(row["right_elementary"]) for row in rows],ORANGE)],
               "Score threshold (USD millions)","Mean elementary score")
        bindings.append(dict(figure="v7-murphy-"+name,source=str(relative),
                             sha256=hashlib.sha256(raw).hexdigest(),columns=list(rows[0]),point_count=len(rows),
                             new_score_calculation=False,display_only=True))
    (HERE/"s5-figure-bindings.json").write_text(json.dumps(bindings,indent=2)+"\n")
    print(json.dumps({"figure_sources":3,"new_forecasts":0,"new_scores":0,"saved_values_unchanged":True},indent=2))


if __name__=="__main__":
    main()
