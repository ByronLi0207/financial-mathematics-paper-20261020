"""Frozen WP1 saved-result analysis. No financial DGP is generated here."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import tarfile
import warnings
from fractions import Fraction
import numpy as np

P = {"QR33": 34, "QR4": 5}
DESIGN_SHA = "fddbd6ffd1c08dbd44a6dd2bbbfe3ce1dfb8de3329c515d30a5754eb6db14b48"
DESIGN_COMMIT = "7f0fee8f1cfdeed584098bbc27570e88eafaea43"
FINAL_RE = re.compile(r"^units/rep-(\d{3})_phi-(\d)_p-(\d)/W(\d+)_H(\d+)_(F|QR33|QR4)\.json$")

def assert_fingerprint(path, expected):
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != expected:
        raise ValueError(f"source fingerprint mismatch: {path}: {digest}")
    return digest

def metric_value(window, horizon, method, candidate):
    if candidate not in ("a", "b", "c"):
        raise ValueError("unknown candidate")
    denominator = P[method] if candidate == "a" else (horizon+1)*(P[method] if candidate == "b" else 1)
    return Fraction(int(window), int(denominator))

def relative_change(model, reference):
    model, reference = np.asarray(model, float), np.asarray(reference, float)
    if model.shape != reference.shape or model.size == 0 or not np.isfinite(model).all() or not np.isfinite(reference).all():
        raise ValueError("invalid paired final losses")
    denominator = reference.mean()
    if denominator <= 0:
        raise ValueError("nonpositive reference loss")
    value = float(100*(model.mean()/denominator-1))
    if not math.isfinite(value):
        raise ValueError("nonfinite relative loss")
    return value

def select_candidate(correct, total):
    if set(correct) != {"a", "b", "c"} or total <= 0 or any(type(v) is not int or not 0 <= v <= total for v in correct.values()):
        raise ValueError("incomplete or invalid candidate scores")
    maximum = max(correct.values())
    return next(k for k in ("c", "a", "b") if correct[k] == maximum)

def group_curve(metrics, percentages):
    if len(metrics) != len(percentages) or not metrics:
        raise ValueError("empty/mismatched curve")
    groups = {}
    for r, y in zip(metrics, percentages):
        key = Fraction(r)
        if key <= 0 or not math.isfinite(float(y)):
            raise ValueError("nonfinite or nonpositive curve input")
        groups.setdefault(key, []).append(float(y))
    keys = sorted(groups)
    return [float(x) for x in keys], [math.fsum(groups[x])/len(groups[x]) for x in keys]

def describe_crossings(abscissae, ordinates):
    x, y = list(abscissae), list(ordinates)
    if len(x) != len(y) or not x or any(not math.isfinite(v) for v in x+y) or any(v <= 0 for v in x) or any(a >= b for a,b in zip(x,x[1:])):
        raise ValueError("invalid ordered curve")
    roots = [float(a+(b-a)*u/(u-v)) for a,b,u,v in zip(x,x[1:],y,y[1:]) if u > 0 and v <= 0]
    status = "UNIDENTIFIED_LEFT_CENSORED" if y[0] <= 0 else ("IDENTIFIED" if roots else "UNIDENTIFIED_NO_CROSSING")
    return {"status":status, "r_star":roots[0] if status == "IDENTIFIED" else None,
            "crossings":roots, "multiple_crossings":len(roots)>1, "x":x, "y":y}

def bootstrap_roots(metrics, model, reference, indices):
    model, reference = np.asarray(model, float), np.asarray(reference, float)
    indices = np.asarray(indices)
    if model.shape != reference.shape or model.ndim != 2 or len(metrics) != model.shape[0] or indices.ndim != 2 or not np.issubdtype(indices.dtype, np.integer) or indices.min() < 0 or indices.max() >= model.shape[1]:
        raise ValueError("invalid clustered bootstrap shapes/indices")
    if not np.isfinite(model).all() or not np.isfinite(reference).all():
        raise ValueError("nonfinite bootstrap losses")
    draws = []
    for ids in indices:
        fm = reference[:,ids].mean(axis=1)
        if np.any(fm <= 0):
            raise ValueError("nonpositive resampled reference loss")
        delta = 100*(model[:,ids].mean(axis=1)/fm-1)
        draws.append(describe_crossings(*group_curve(metrics, delta)))
    return draws

def _order_stat(values, q):
    values = sorted(values)
    return float(values[max(0, math.ceil(q*len(values))-1)])

def percentile_intervals(roots):
    if not roots or any(v is not None and (not math.isfinite(v) or v <= 0) for v in roots):
        raise ValueError("invalid bootstrap roots")
    finite = [v for v in roots if v is not None]
    lower = _order_stat([0. if v is None else v for v in roots], .05)
    upper = _order_stat([math.inf if v is None else v for v in roots], .95)
    return {"draw_count":len(roots), "finite_count":len(finite), "missing_count":len(roots)-len(finite),
            "finite_only":{"lower":_order_stat(finite,.05) if finite else None, "upper":_order_stat(finite,.95) if finite else None, "conditional_on_finite_crossing":True},
            "all_draw_envelope":{"lower":lower,"upper":upper if math.isfinite(upper) else None,"upper_unbounded":not math.isfinite(upper), "coverage_guarantee":False},
            "conditions":"post-hoc chosen metric and fixed DGP grid; metric-selection uncertainty excluded"}

def read_evaluation(report):
    evaluation = report.get("evaluation")
    if report.get("status") != "COMPLETE" or not isinstance(evaluation, dict):
        raise ValueError("missing complete final evaluation")
    if not isinstance(evaluation.get("n"), int) or evaluation["n"] <= 0 or not math.isfinite(evaluation.get("mean_loss", math.nan)):
        raise ValueError("invalid final evaluation")
    return evaluation

def read_csv(path):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))

def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refuse to overwrite: {path}")
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")

def load_saved_reports(root, design):
    for source in design["inputs"]:
        path = root/source["path"]
        assert_fingerprint(path, source["sha256"])
        if path.stat().st_size != source["bytes"]:
            raise ValueError("source size mismatch")
    index = {row["path"]:row for row in read_csv(root/"results/revision-v8/wp3/wp3-driver-output-members.csv")}
    reports = {}
    members = []
    with tarfile.open(root/"results/revision-v8/wp3/wp3-driver-output.tar.gz", "r|gz") as archive:
        for member in archive:
            match = FINAL_RE.fullmatch(member.name)
            if match is None:
                continue
            content = archive.extractfile(member).read()
            seal = index[member.name]
            if len(content) != int(seal["size"]) or hashlib.sha256(content).hexdigest() != seal["sha256"]:
                raise ValueError("archive member fingerprint mismatch")
            rep, phi, volatility, window, horizon = map(int, match.groups()[:5])
            key = (rep, phi, volatility, window, horizon, match.group(6))
            if key in reports:
                raise ValueError("duplicate final report")
            reports[key] = read_evaluation(json.loads(content))
            members.append({"path":member.name,"sha256":seal["sha256"],"bytes":len(content)})
    expected = {(r,p,v,w,h,m) for r in range(32) for p in range(3) for v in range(3) for w in (52,260,720,2880) for h in (6,24) for m in ("F","QR33","QR4")}
    if set(reports) != expected:
        raise ValueError("incomplete selected-report pairing")
    rows = [x for x in read_csv(root/"results/revision-v8/wp3/summary.csv") if x["method"] in P]
    cells, mismatches = [], []
    for row in rows:
        phi, volatility, window, horizon = (int(row[k]) for k in ("phi_index","p_index","window","horizon"))
        method = row["method"]
        model = [reports[(r,phi,volatility,window,horizon,method)]["mean_loss"] for r in range(32)]
        reference = [reports[(r,phi,volatility,window,horizon,"F")]["mean_loss"] for r in range(32)]
        if any(reports[(r,phi,volatility,window,horizon,method)]["n"] != reports[(r,phi,volatility,window,horizon,"F")]["n"] for r in range(32)):
            raise ValueError("unequal paired issue counts")
        delta = relative_change(model, reference)
        for key, derived in (("relative_loss_percent",delta),("mean_model_loss",np.mean(model)),("mean_reference_loss",np.mean(reference))):
            if not math.isclose(derived,float(row[key]),rel_tol=1e-12,abs_tol=1e-10):
                mismatches.append({"cell":[phi,volatility,window,horizon,method],"field":key,"derived":float(derived),"archived":float(row[key])})
        cells.append({"phi_index":phi,"volatility_index":volatility,"phi":float(row["phi"]),"variance_persistence":float(row["variance_persistence"]),"window":window,"horizon":horizon,"method":method,"relative_loss_percent":delta,"model_losses":model,"reference_losses":reference})
    if len(cells) != 144 or mismatches:
        raise ValueError(f"source-summary numerical MISMATCH: {mismatches}")
    return cells, members

def candidate_scores(cells):
    from scipy.stats import rankdata
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.exceptions import ConvergenceWarning
    y = np.asarray([int(c["relative_loss_percent"] < 0) for c in cells])
    delta = np.asarray([c["relative_loss_percent"] for c in cells])
    if not np.isfinite(delta).all():
        raise ValueError("nonfinite cell loss delta")
    if len(cells) != 144 or len(np.unique(y)) != 2:
        raise ValueError("invalid classification population")
    scores = {}
    for candidate in ("a","b","c"):
        r = np.asarray([float(metric_value(c["window"],c["horizon"],c["method"],candidate)) for c in cells])
        if not np.isfinite(r).all() or np.any(r <= 0):
            raise ValueError("nonfinite/nonpositive candidate metric")
        z = StandardScaler().fit_transform(np.log(r).reshape(-1,1))
        model = LogisticRegression(C=1., l1_ratio=0., solver="lbfgs",max_iter=10000,tol=1e-10,fit_intercept=True,class_weight=None,warm_start=False)
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            model.fit(z,y)
        if model.n_iter_.max() >= 10000:
            raise ValueError("logistic max iteration reached")
        correct = int(np.sum((model.decision_function(z)>0).astype(int)==y))
        correlations = {}
        for group in ("pooled","QR33","QR4"):
            mask = np.ones(len(cells),bool) if group == "pooled" else np.array([c["method"]==group for c in cells])
            ranks_x, ranks_y = rankdata(r[mask],method="average"), rankdata(delta[mask],method="average")
            correlations[group] = float(np.corrcoef(ranks_x,ranks_y)[0,1])
        scores[candidate] = {"correct":correct,"total":len(cells),"accuracy":correct/len(cells),"spearman":correlations,"standardized_log_coefficient":float(model.coef_[0,0]),"intercept":float(model.intercept_[0]),"iterations":int(model.n_iter_[0]),"target_wins":int(y.sum()),"classification":"in-sample descriptive; not predictive validation"}
    return scores, select_candidate({k:v["correct"] for k,v in scores.items()},len(cells))

def overlay_pair(row, reference, source, window, horizon, method, source_file, source_row):
    result = {"source":source,"window":window,"horizon":horizon,"method":method,
              "nominal_coefficients":P[method],"source_file":source_file,"source_row":source_row,
              "source_status":row.get("status","COMPLETE"),"status":"COMPLETE", "reason":None,
              "relative_loss_percent":None,"model_loss":None,"reference_loss":None,"n":None}
    if result["source_status"] != "COMPLETE":
        result.update(status="NA_SOURCE_FAILED",reason="original selected procedure not complete")
        return result
    if reference is None or reference.get("status","COMPLETE") != "COMPLETE":
        result.update(status="NA_MISMATCH",reason="missing/ambiguous/incomplete matched F")
        return result
    try:
        n, nf = int(row["origin_count"]), int(reference["origin_count"])
        model_loss, reference_loss = float(row["mean_pinball"]), float(reference["mean_pinball"])
        if n != nf or n <= 0 or not math.isfinite(model_loss) or not math.isfinite(reference_loss) or reference_loss <= 0:
            raise ValueError("unequal issue count or invalid losses")
        result.update(model_loss=model_loss,reference_loss=reference_loss,n=n,
                      relative_loss_percent=100*(model_loss/reference_loss-1))
    except (KeyError,TypeError,ValueError) as error:
        result.update(status="NA_MISMATCH",reason=str(error))
    return result

def empirical_overlay(root, selected, curves):
    output = []
    original_path = "results/revision-20261022/evaluation-summary.csv"
    original = read_csv(root/original_path)
    def unique(rows):
        return rows[0] if len(rows)==1 else None
    for line, row in enumerate(original,2):
        if row["method"] != "QR":
            continue
        reference = unique([r for r in original if r["method"]=="frozen_F" and all(r[k]==row[k] for k in ("source","horizon","window","refit_step"))])
        item = overlay_pair(row,reference,row["source"],int(row["window"]),int(row["horizon"]),"QR33",original_path,line)
        item["refit_step"] = int(row["refit_step"])
        output.append(item)
    path = "results/revision-20261023/parsimonious/summary.csv"
    for line,row in enumerate(read_csv(root/path),2):
        cadence = 24 if row["source"]=="fx_hourly" else 13
        reference = unique([r for r in original if r["method"]=="frozen_F" and all(r[k]==row[k] for k in ("source","horizon","window")) and int(r["refit_step"])==cadence])
        item = overlay_pair(row,reference,row["source"],int(row["window"]),int(row["horizon"]),"QR4",path,line)
        item["refit_step"] = cadence
        if item["status"]=="COMPLETE" and not math.isclose(item["relative_loss_percent"],float(row["percent_vs_frozen_F"]),rel_tol=1e-12,abs_tol=1e-10):
            item.update(status="NA_MISMATCH",reason="archived percent_vs_frozen_F differs",relative_loss_percent=None)
        output.append(item)
    path = "results/revision-v8/wp4/contrasts.csv"
    for line,row in enumerate(read_csv(root/path),2):
        model = {"status":row["status"],"origin_count":row["n"],"mean_pinball":row["model_loss"]}
        reference = {"status":"COMPLETE","origin_count":row["n"],"mean_pinball":row["reference_loss"]} if row["reference_method"]=="F" else None
        item = overlay_pair(model,reference,"fx_daily",int(row["window"]),int(row["horizon"]),row["method"],path,line)
        if item["status"]=="COMPLETE" and not math.isclose(item["relative_loss_percent"],float(row["relative_loss_percent"]),rel_tol=1e-12,abs_tol=1e-10):
            item.update(status="NA_MISMATCH",reason="archived daily contrast differs",relative_loss_percent=None)
        output.append(item)
    path = "results/revision-20261023/round2/panel/summary.csv"
    panel = read_csv(root/path)
    for line,row in enumerate(panel,2):
        if row["method"] not in ("QR33","C2_QR4"):
            continue
        reference = unique([r for r in panel if r["method"]=="frozen_F" and all(r[k]==row[k] for k in ("series_key","horizon","window"))])
        item = overlay_pair(row,reference,"panel:"+row["series_key"],int(row["window"]),int(row["horizon"]),"QR4" if row["method"]=="C2_QR4" else "QR33",path,line)
        if item["status"]=="COMPLETE" and not math.isclose(item["relative_loss_percent"],float(row["percent_vs_frozen_F"]),rel_tol=1e-12,abs_tol=1e-10):
            item.update(status="NA_MISMATCH",reason="archived panel contrast differs",relative_loss_percent=None)
        output.append(item)
    for item in output:
        item["metric"] = float(metric_value(item["window"],item["horizon"],item["method"],selected))
        threshold = curves[item["method"]]["point"]["r_star"]
        item["threshold"] = threshold
        if threshold is None or item["status"] != "COMPLETE":
            item["threshold_consistency"] = "NOT_TESTABLE"
        elif item["metric"] == threshold or item["relative_loss_percent"] == 0:
            item["threshold_consistency"] = "BOUNDARY"
        else:
            item["threshold_consistency"] = "CONSISTENT" if ((item["metric"]>threshold)==(item["relative_loss_percent"]<0)) else "INCONSISTENT"
    return output

def plot_initial(cells, overlay, curves, selected, destination):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1,2,figsize=(11,4.5),sharey=True)
    symbols = {"fx_hourly":"o","fx_daily":"s","nyfed_weekly":"^","panel":"D"}
    for ax, method in zip(axes,("QR33","QR4")):
        for c in cells:
            if c["method"]==method:
                ax.scatter(float(metric_value(c["window"],c["horizon"],method,selected)),c["relative_loss_percent"],color="0.7",s=18,alpha=.6)
        curve = curves[method]
        ax.plot(curve["point"]["x"],curve["point"]["y"],color="#496778",lw=1,label="Post-hoc v8 cell mean")
        interval = curve["intervals"]["all_draw_envelope"]
        if interval["lower"]>0 and interval["upper"] is not None:
            ax.axvspan(interval["lower"],interval["upper"],color="#496778",alpha=.15,label="90% bootstrap envelope")
        for source,symbol in symbols.items():
            group = [x for x in overlay if x["method"]==method and x["status"]=="COMPLETE" and (x["source"].startswith("panel:") if source=="panel" else x["source"]==source)]
            if group:
                ax.scatter([x["metric"] for x in group],[x["relative_loss_percent"] for x in group],marker=symbol,s=30,facecolors="none",edgecolors="#112d40",label=source)
        ax.axhline(0,color="black",lw=.7); ax.set_xscale("log")
        ax.set_title(method+"; nominal p="+str(P[method])); ax.set_xlabel({"a":"W / p","b":"W / ((H+1) p)","c":"W / (H+1)"}[selected])
    axes[0].set_ylabel("Loss change versus matched F (%)")
    axes[1].legend(fontsize=7,loc="best")
    fig.suptitle("Post-hoc description: frozen v8 simulation and original empirical cells")
    fig.tight_layout()
    for extension in ("png","pdf"):
        target=Path(str(destination)+"."+extension)
        if target.exists(): raise FileExistsError(target)
        fig.savefig(target,dpi=160,bbox_inches="tight")
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=Path.cwd())
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(); root=args.root.resolve(); out=args.output
    if out.exists(): raise FileExistsError(out)
    design_path=root/"protocol/revision-v9/wp1-posthoc-design.json"
    assert_fingerprint(design_path,DESIGN_SHA)
    design=json.loads(design_path.read_text())
    import platform, scipy, sklearn, subprocess
    actual_versions={"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"scikit_learn":sklearn.__version__}
    if actual_versions != design["runtime_versions"]:
        raise ValueError(f"runtime MISMATCH: {actual_versions}")
    if subprocess.run(["git","merge-base","--is-ancestor",DESIGN_COMMIT,"HEAD"],cwd=root).returncode:
        raise ValueError("precalculation design not committed in ancestry")
    cells,members=load_saved_reports(root,design)
    scores,selected=candidate_scores(cells)
    indices=np.random.Generator(np.random.PCG64(np.random.SeedSequence(2026102491))).integers(0,32,size=(1999,32))
    draw_hashes=[hashlib.sha256(np.asarray(row,dtype="<i8").tobytes()).hexdigest() for row in indices]
    curves={}
    for method in ("QR33","QR4"):
        subset=[c for c in cells if c["method"]==method]
        metrics=[metric_value(c["window"],c["horizon"],method,selected) for c in subset]
        point=describe_crossings(*group_curve(metrics,[c["relative_loss_percent"] for c in subset]))
        draws=bootstrap_roots(metrics,[c["model_losses"] for c in subset],[c["reference_losses"] for c in subset],indices)
        curves[method]={"point":point,"intervals":percentile_intervals([d["r_star"] for d in draws]),"multiple_crossing_draws":sum(d["multiple_crossings"] for d in draws),"status_counts":{status:sum(d["status"]==status for d in draws) for status in sorted({d["status"] for d in draws})},"draws":draws}
    overlay=empirical_overlay(root,selected,curves)
    out.mkdir(parents=True)
    for c in cells:
        c["metrics"]={candidate:str(metric_value(c["window"],c["horizon"],c["method"],candidate)) for candidate in ("a","b","c")}
    write_json(out/"simulation-cells.json",cells)
    write_json(out/"empirical-overlay.json",overlay)
    write_json(out/"archive-member-bindings.json",members)
    write_json(out/"bootstrap.json",{"seed_entropy":2026102491,"draw_indices":indices.tolist(),"draw_index_sha256":draw_hashes,"methods":curves})
    result={"stage":"WP1_POST_HOC","post_hoc":True,"design_commit":DESIGN_COMMIT,"design_sha256":DESIGN_SHA,"selected_metric":selected,"definition":design["candidate_metrics"][selected],"candidate_scores":scores,"methods":{m:{k:v for k,v in curve.items() if k!="draws"} for m,curve in curves.items()},"simulation_cells":len(cells),"final_reports":len(members),"source_summary_mismatches":0,"source_summary_tolerance":{"absolute":1e-10,"relative":1e-12},"empirical_overlay_cells":len(overlay),"empirical_overlay_status_counts":{s:sum(x["status"]==s for x in overlay) for s in sorted({x["status"] for x in overlay})},"empirical_consistency_counts":{s:sum(x["threshold_consistency"]==s for x in overlay) for s in sorted({x["threshold_consistency"] for x in overlay})},"versions":actual_versions,"inputs":design["inputs"],"caveats":["Post-hoc metric selection: resubstitution accuracy is descriptive, not out-of-sample validation.","Nominal p is not effective degrees of freedom; method menus and failure policies differ.","Intervals condition on fixed chosen metric and fixed simulation grid; no metric-selection uncertainty or universal coverage guarantee.","The empirical overlay is consistency checking only, not independent metric selection.","If c is selected, it has no p and cannot alone identify a per-parameter mechanism.","Multiple crossings cannot justify a claim of universal improvement above the first crossing."]}
    write_json(out/"breakeven.json",result)
    plot_initial(cells,overlay,curves,selected,out/"initial-scatter")
    print(json.dumps({"selected_metric":selected,"scores":scores,"methods":result["methods"],"overlay":result["empirical_overlay_status_counts"],"output":str(out)},indent=2,allow_nan=False))

if __name__=="__main__":
    main()
