"""Independent WP2 readback: no production science imports or model fitting.

Execute only after the owned numerical workers have terminated. Validation
candidate losses are recorded scalars: their selection is independently audited,
but absent validation forecast traces are not represented as re-scored data.
"""
from __future__ import annotations
import argparse
import copy
import csv
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import signal
import statistics
import subprocess
import time
from collections import Counter
from fractions import Fraction
import numpy as np

FROZEN_COMMIT = "f2ce438ccb2fcf671c849a83032ac700ac6007c6"
ATOL, RTOL = 1e-10, 1e-12
METHODS = ("F", "QR33", "QR4")
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
           "NUMBA_NUM_THREADS")

class AuditMismatch(AssertionError):
    pass

def require(condition, message):
    if not condition:
        raise AuditMismatch(message)

def compare(actual, expected, location="value"):
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and set(actual) == set(expected), location+": keys")
        for key in expected:
            compare(actual[key], expected[key], location+"."+str(key))
    elif isinstance(expected, (tuple, list)):
        require(isinstance(actual, (tuple, list)) and len(actual) == len(expected), location+": length")
        for i, (a, b) in enumerate(zip(actual, expected)):
            compare(a, b, location+"["+str(i)+"]")
    elif expected is None or isinstance(expected, (str, bool)):
        require(actual == expected, location+": scalar")
    elif isinstance(expected, int):
        require(type(actual) is int and actual == expected, location+": integer")
    else:
        require(type(actual) in (int, float) and math.isfinite(actual)
                and math.isclose(float(actual), float(expected), abs_tol=ATOL, rel_tol=RTOL),
                location+": number")

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def stable_mean(values):
    values = list(map(float, values))
    require(bool(values) and all(map(math.isfinite, values)), "invalid finite mean")
    return values[0] if all(v == values[0] for v in values) else math.fsum(values)/len(values)

def regenerate(rep, di, phi, design):
    """Regenerate only the frozen input experiment, never a fitted forecast."""
    count = design["burn_in"] + design["retained_observations"]
    generators = [np.random.Generator(np.random.PCG64(np.random.SeedSequence(
        design["master_entropy"], spawn_key=(rep, di, stream)))) for stream in range(3)]
    before = [copy.deepcopy(g.bit_generator.state) for g in generators]
    if di == 0:
        innovation = generators[0].standard_t(5, size=count)*math.sqrt(3/5)
    elif di == 1:
        normal = generators[0].standard_normal(count)
        uniforms = generators[1].random(count+1)
        state = int(uniforms[0] >= .5)
        states = np.empty(count, dtype=np.int64)
        for i in range(count):
            states[i] = state
            if uniforms[i+1] < .02:
                state = 1-state
        innovation = normal*np.where(states == 0, 1., 3.)/math.sqrt(5)
    elif di == 2:
        normal = generators[0].standard_normal(count)
        multiplicity = generators[1].poisson(.01, size=count)
        positive = generators[2].binomial(multiplicity, .5)
        innovation = (normal+5*(2*positive-multiplicity))/math.sqrt(1.25)
    else:
        raise AuditMismatch("unregistered DGP")
    level = np.empty(count)
    previous = float(design["initial_level"])
    for i in range(count):
        previous = phi*previous+innovation[i]
        level[i] = previous
    retained = level[design["burn_in"]:].copy()
    metadata = dict(stream_key=[rep, di], master_entropy=design["master_entropy"],
        initial_states=before, final_states=[copy.deepcopy(g.bit_generator.state) for g in generators],
        innovation_sha256=hashlib.sha256(innovation.astype("<f8").tobytes()).hexdigest(),
        position_sha256=hashlib.sha256(retained.astype("<f8").tobytes()).hexdigest(),
        innovation_count=count)
    return retained, metadata

def direct_peak(position, origins, horizon):
    return np.array([max(abs(float(v)) for v in position[int(t):int(t)+horizon+1]) for t in origins])

def direct_f(position, origins, horizon, window, step):
    first = int(origins[0]); answer = []
    rank = math.ceil(Fraction(19*(window+1), 20))
    require(rank <= window, "corrected rank unavailable")
    for t in origins:
        refit = first+step*((int(t)-first)//step)
        pool = range(refit-horizon-window+1, refit-horizon+1)
        headrooms = [max(abs(float(x)) for x in position[i:i+horizon+1])-abs(float(position[i])) for i in pool]
        answer.append(abs(float(position[t]))+sorted(headrooms)[rank-1])
    return np.array(answer)

def check_trace(position, trace, horizon, window, method, design):
    expected_ids = np.arange(design["evaluation_first"], design["evaluation_last"]+1, dtype=np.int64)
    require(set(trace) == {"origins", "capacity", "peak", "floor", "refit_indices", "pinball", "strict_breach"}, "trace schema")
    require(np.array_equal(trace["origins"], expected_ids), "evaluation origins")
    refit = expected_ids[0]+design["refit_step"]*((expected_ids-expected_ids[0])//design["refit_step"])
    require(np.array_equal(trace["refit_indices"], refit), "issue/refit clock")
    peak = direct_peak(position, expected_ids, horizon)
    floor = np.abs(position[expected_ids])
    require(np.array_equal(trace["peak"], peak), "actual path peak labels")
    require(np.array_equal(trace["floor"], floor), "actual path anchor floors")
    capacity = trace["capacity"]
    require(capacity.shape == peak.shape and np.isfinite(capacity).all() and np.all(capacity >= floor), "capacity geometry")
    if method == "F":
        require(np.allclose(capacity, direct_f(position, expected_ids, horizon, window, design["refit_step"]), atol=ATOL, rtol=RTOL), "independent F capacity")
    residual = peak-capacity
    loss = .95*np.maximum(residual, 0)+.05*np.maximum(-residual, 0)
    hit = residual > 0
    require(np.allclose(trace["pinball"], loss, atol=ATOL, rtol=RTOL), "per-issue pinball math")
    require(np.array_equal(trace["strict_breach"], hit), "per-issue strict breach math")
    return dict(mean_loss=stable_mean(loss), n=len(expected_ids),
                strict_breach_count=int(hit.sum()), strict_breach_rate=float(hit.sum()/len(hit)))

def check_maturity(diagnostics, maturity, window, horizon, segment, design, method):
    refs = list(range(design[segment+"_first"], design[segment+"_last"]+1, design["refit_step"]))
    require(len(diagnostics) == len(refs), "full fit/refit diagnostics")
    for item, r in zip(diagnostics, refs):
        for key, expected in dict(refit_index=r, training_first_origin=r-horizon-window+1,
                training_last_origin=r-horizon, training_count=window, latest_label_end=r).items():
            require(item[key] == expected, "mature training clock "+key)
        require(item["training_first_origin"] >= (0 if method == "F" else design["feature_valid_from"]), "feature maturity")
        require(all(value is None or isinstance(value, (str, bool)) or math.isfinite(value)
                    for value in item.values()), "finite diagnostics")
        if method != "F":
            require(0 < item["iterations"] <= design["solver"]["max_iter"], "solver iteration cap")
            for left, right in (("duality_gap", "gap_tolerance"), ("primal_residual", "primal_tolerance"), ("dual_residual", "dual_tolerance")):
                require(item[left] <= item[right], "solver accepted diagnostic "+left)
    expected = dict(refit_count=len(refs), training_first_origin_min=min(refs)-horizon-window+1,
        training_last_origin_max=max(refs)-horizon, latest_label_end_max=max(refs), maximum_label_end_minus_refit=0)
    compare(maturity, expected, "maturity summary")

def select_from_records(records, method, design):
    menu = design["menus"][method]
    require([x.get("penalty") for x in records] == menu, "registered candidate menu")
    completed = []
    for item in records:
        require(item["status"] in ("COMPLETE", "FAILED", "INCOMPLETE"), "candidate terminal status")
        if item["status"] == "COMPLETE":
            require(item["origin_count"] == design["validation_last"]-design["validation_first"]+1,
                    "full validation count")
            require(math.isfinite(item["mean_loss"]) and item["mean_loss"] >= 0, "finite validation loss")
            completed.append(item)
    if not completed or (method == "QR33" and len(completed) != len(menu)):
        return dict(status="INELIGIBLE", penalty=None)
    selected = sorted(completed, key=lambda item:(item["mean_loss"], -item["penalty"] if method == "QR33" else menu.index(item["penalty"])))[0]
    return dict(status="SELECTED", penalty=selected["penalty"], mean_validation_loss=selected["mean_loss"])

def independent_summary(models, references, planned):
    require(set(models) == set(references) == set(range(planned)), "complete effective repetition inventory")
    complete = []; failed = pending = 0
    for rep in range(planned):
        a, b = models[rep], references[rep]
        if a["status"] == b["status"] == "COMPLETE":
            complete.append((a["evaluation"], b["evaluation"]))
        elif a["status"] == "FAILED" or b["status"] == "FAILED":
            failed += 1
        elif a["status"] == "NOT_ATTEMPTED" or b["status"] == "NOT_ATTEMPTED":
            pending += 1
        else:
            failed += 1
    n = len(complete)
    out = dict(planned_repetitions=planned, complete_repetitions=n, failed_repetitions=failed,
        unattempted_repetitions=pending, conditional_on_completion=n != planned,
        full_procedure_status="COMPLETE" if n == planned else "NA", full_procedure_relative_loss_percent=None)
    for key in ("relative_loss_percent", "relative_loss_mcse", "model_breach_rate", "model_breach_mcse",
                "reference_breach_rate", "reference_breach_mcse", "win_fraction", "win_mcse", "win_mcse_worst_bound"):
        out[key] = None
    if n:
        a = [x[0]["mean_loss"] for x in complete]; b = [x[1]["mean_loss"] for x in complete]
        ma, mb = statistics.mean(a), statistics.mean(b)
        out.update(mean_model_loss=ma, mean_reference_loss=mb)
        if mb:
            ratio = ma/mb; out["relative_loss_percent"] = 100*(ratio-1)
            if n > 1:
                out["relative_loss_mcse"] = 100*statistics.stdev([x-ratio*y for x,y in zip(a,b)])/(math.sqrt(n)*mb)
        for name, side in (("model",0), ("reference",1)):
            rates = [x[side]["strict_breach_rate"] for x in complete]
            out[name+"_breach_rate"] = statistics.mean(rates)
            if n > 1:out[name+"_breach_mcse"] = statistics.stdev(rates)/math.sqrt(n)
        p = sum(x < y for x,y in zip(a,b))/n
        out["win_fraction"] = p; out["win_mcse_worst_bound"] = .5/math.sqrt(n)
        if n > 1:out["win_mcse"] = math.sqrt(p*(1-p)/n)
        if n == planned:out["full_procedure_relative_loss_percent"] = out["relative_loss_percent"]
    return out

def fixed_screen(outcomes, minimum):
    require(bool(outcomes) and all(x is None or type(x) is bool for x in outcomes), "fixed-denominator outcomes")
    n = len(outcomes); yes = sum(x is True for x in outcomes); missing = sum(x is None for x in outcomes)
    threshold = Fraction(str(minimum))
    if Fraction(yes+missing,n) < threshold:status = "NOT_SUPPORT"
    elif missing:status = "INCONCLUSIVE"
    elif Fraction(yes,n) >= threshold:status = "SUPPORT"
    else:status = "NOT_SUPPORT"
    return dict(status=status, successes=yes, missing=missing, denominator=n, lower_bound=yes/n,
        upper_bound=(yes+missing)/n, observed_fraction=yes/n if not missing else None, minimum_fraction=minimum)

def independent_screen(rows, design):
    conditional = [x for x in rows if x["method"] != "F"]
    def one(subset):
        out = {}
        for name, small, required in (("P1", True, .8), ("P2", False, .6)):
            values = []; keys = []
            for item in subset:
                metric = item["window"]/(item["horizon"]+1); threshold = design["thresholds"][item["method"]]["r_star"]
                if not (metric < threshold/2 if small else metric > 2*threshold):continue
                delta = item["full_procedure_relative_loss_percent"]
                values.append(None if delta is None else bool(delta > 0 if small else delta < 0))
                keys.append([item[k] for k in ("dgp", "phi_index", "window", "horizon", "method")])
            out[name] = dict(fixed_screen(values, required), cells=keys, outcomes=values)
        statuses = [out[k]["status"] for k in ("P1","P2")]
        out["primary_status"] = "NOT_SUPPORT" if "NOT_SUPPORT" in statuses else ("INCONCLUSIVE" if "INCONCLUSIVE" in statuses else "SUPPORT")
        return out
    out = one(conditional)
    require(out["P1"]["denominator"] == 48 and out["P2"]["denominator"] == 24, "fixed P1/P2 population")
    out["by_method"] = {m:one([x for x in conditional if x["method"] == m]) for m in ("QR33","QR4")}
    out["by_DGP"] = {d:one([x for x in conditional if x["dgp"] == d]) for d in design["dgp"]}
    index = {(x["dgp"],x["phi_index"],x["window"],x["horizon"],x["method"]):x for x in conditional}
    values = []; pairs = []
    for dgp in design["dgp"]:
        for pi in range(len(design["phi"])):
            for w in design["windows"]:
                for h in design["horizons"]:
                    a = index[(dgp,pi,w,h,"QR4")]["full_procedure_relative_loss_percent"]
                    b = index[(dgp,pi,w,h,"QR33")]["full_procedure_relative_loss_percent"]
                    value = None if a is None or b is None else bool(a <= b)
                    values.append(value); pairs.append(dict(dgp=dgp, phi_index=pi, window=w, horizon=h, QR4_delta=a, QR33_delta=b, outcome=value))
    require(len(pairs) == 48, "fixed P3 population")
    out["P3"] = dict(fixed_screen(values, 1.), pairs=pairs, secondary=True)
    out["interpretation"] = "pooled primary only; contrary method/DGP/P3 outcomes retained; metric excludes p"
    return out

def check_budget(formal, term, design):
    removed = term["removed_windows"]
    path = formal/"budget-decision.json"
    if not path.exists():
        require(not removed, "missing reduction decision")
        return
    decision = read(path); receipts = [read(formal/"units"/f"rep-{r:03d}_dgp-{di}_phi-{pi}"/"worker-receipt.json") for r in range(16) for di in range(3) for pi in range(2)]
    require(all(x["status"] == "COMPLETE" for x in receipts) and decision["uses_losses"] is False,
            "budget review first16 completion/outcome blindness")
    windows = {w:math.fsum(x["window_seconds"].get(str(w),0.) for x in receipts) for w in design["windows"]}
    overhead = max(0.,math.fsum(x["elapsed_seconds"] for x in receipts)-math.fsum(windows.values()))
    projected = math.fsum(windows.values())+overhead; remaining = decision["remaining_seconds"]
    expected = []; after = projected
    for w in (52,260,720,2880):
        if after <= .9*remaining:break
        expected.append(w);after -= windows[w]
    require(expected == removed == decision["removed_windows"], "predeclared reduction order")
    for key, value in dict(projected_seconds_before=projected, projected_seconds_after=after,
            allowance_seconds=.9*remaining, can_continue=after <= .9*remaining).items():
        compare(decision[key], value, "budget "+key)

def main():
    parser = argparse.ArgumentParser();parser.add_argument("--root",type=Path,default=Path.cwd())
    parser.add_argument("--formal",type=Path,default=Path(".scratch/revision-v9/wp2-run"))
    parser.add_argument("--output",type=Path);args=parser.parse_args()
    root = args.root.resolve(); formal = args.formal if args.formal.is_absolute() else root/args.formal
    began = time.monotonic();signal.signal(signal.SIGALRM, lambda *_:(_ for _ in ()).throw(TimeoutError("WP2 audit 600s limit")));signal.alarm(590)
    require(all(os.environ.get(k) == "1" for k in THREADS), "audit numerical thread environment")
    require(np.__version__ == "2.3.5", "frozen RNG runtime")
    audit_max_threads=0
    def probe_audit():
        nonlocal audit_max_threads
        observed=subprocess.check_output(["ps","-M","-p",str(os.getpid())],text=True)
        audit_max_threads=max(audit_max_threads,len(observed.strip().splitlines())-1)
        require(audit_max_threads <= 2 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= 2147483648,
                "actual audit thread/RSS samples")
    probe_audit()
    manifest = read(formal/"manifest.json"); term = read(formal/"study-termination.json"); design = manifest["design"]
    require(term["all_workers_terminated"] is True, "workers must terminate before audit")
    require(manifest["design_commit"] == FROZEN_COMMIT and manifest["initial_planned_workers"] == 192
        and manifest["initial_planned_selected_reports"] == 4608, "frozen initial census")
    for name in ("protocol/revision-v9/wp2-confirmatory.md", "protocol/revision-v9/wp2-confirmatory.json"):
        require(subprocess.check_output(["git","show",FROZEN_COMMIT+":"+name],cwd=root) == (root/name).read_bytes(), "committed protocol bytes")
    for name, sha in manifest["sealed_files"].items():require(digest(root/name) == sha, "sealed file "+name)
    require(read(root/"protocol/revision-v9/wp2-confirmatory.json") == design, "manifest design")
    check_budget(formal,term,design)
    snapshots = {str(p):digest(p) for p in formal.rglob("*") if p.is_file()}
    inventory = read(formal/"inventory.json"); saved_summaries = read(formal/"summary.json"); saved_screen = read(formal/"support.json")
    require(len(inventory) == 4608, "initial inventory length")
    inv_index = {(x["rep"],x["dgp"],x["phi_index"],x["window"],x["horizon"],x["method"]):x for x in inventory}
    expected_keys = {(r,d,pi,w,h,m) for r in range(32) for d in design["dgp"] for pi in range(2) for w in design["windows"] for h in design["horizons"] for m in METHODS}
    require(set(inv_index) == expected_keys and len(inv_index) == 4608, "exact initial inventory keys")
    scores = {}; synthetic_count = trace_count = candidate_count = resource_count = 0; maximum_rss = maximum_threads = 0; maximum_worker_wall = 0.
    started_clocks = []; ended_clocks = []
    for rep in range(32):
        for di,dgp in enumerate(design["dgp"]):
            for pi,phi in enumerate(design["phi"]):
                probe_audit()
                unit = formal/"units"/f"rep-{rep:03d}_dgp-{di}_phi-{pi}"
                position = None
                if (unit/"synthetic-input.npz").exists():
                    position, rng = regenerate(rep,di,phi,design)
                    compare(read(unit/"rng-receipt.json"),rng,"RNG receipt")
                    with np.load(unit/"synthetic-input.npz",allow_pickle=False) as source:
                        require(set(source.files) == {"position","times"} and np.array_equal(source["position"],position), "synthetic retained position")
                        expected_times = np.datetime64(design["retained_clock_first"])+np.arange(len(position))*np.timedelta64(design["gap_seconds"],"s")
                        require(np.array_equal(source["times"],expected_times), "synthetic observation clock")
                    synthetic_count += 1
                if (unit/"worker-receipt.json").exists():
                    receipt = read(unit/"worker-receipt.json"); measured = receipt["resources"]
                    require(measured is not None, "worker actual resource receipt")
                    rss, threads, wall = measured["peak_rss_bytes"], measured["maximum_observed_os_threads"],receipt["elapsed_seconds"]
                    require(rss is not None and rss <= 2147483648 and threads is not None and threads <= 2 and wall <= 600,
                            "worker absolute actual resource limits")
                    require(measured["requested_numerical_threads"] == 1 and measured["thread_snapshot_count"] > 0,
                            "worker actual resource samples")
                    maximum_rss=max(maximum_rss,rss);maximum_threads=max(maximum_threads,threads);maximum_worker_wall=max(maximum_worker_wall,wall);resource_count+=1
                    started_clocks.append(dt.datetime.fromisoformat(receipt["started_utc"]));ended_clocks.append(dt.datetime.fromisoformat(receipt["ended_utc"]))
                if (unit/"unit-start.json").exists():
                    initial=read(unit/"unit-start.json"); expected_windows=[w for w in design["windows"] if rep < 16 or w not in term["removed_windows"]]
                    require(initial["windows"] == expected_windows, "unit frozen window admission")
                for w in design["windows"]:
                    for h in design["horizons"]:
                        for method in METHODS:
                            key=(rep,dgp,pi,w,h,method); listed=inv_index[key]; path=unit/f"W{w}_H{h}_{method}.json"
                            reduced=rep >= 16 and w in term["removed_windows"]
                            if reduced:
                                require(listed["status"] == "BUDGET_REDUCED" and listed["reason"] == "PREDECLARED_REMAINING_HALF_REMOVED" and not path.exists(), "budget-reduced initial record")
                                continue
                            if path.exists():row=read(path)
                            elif path.with_name(path.stem+".started.json").exists():row=dict(status="FAILED",reason="INTERRUPTED_METHOD",evaluation=None)
                            else:row=dict(status="NOT_ATTEMPTED",reason="METHOD_NOT_REACHED",evaluation=None)
                            require(row["status"] == listed["status"] and row.get("reason") == listed["reason"], "inventory terminal record")
                            require(listed["source"] == str(path.relative_to(root)) and listed.get("selected_penalty") == row.get("selected_penalty"), "inventory source/penalty binding")
                            scores[key]=row
                            if path.exists() and method != "F":
                                records=[]
                                for i,penalty in enumerate(design["menus"][method]):
                                    candidate_path=unit/f"W{w}_H{h}_{method}_validation-{i}.json"
                                    if not candidate_path.exists():continue
                                    candidate=read(candidate_path);require(candidate["penalty"] == penalty,"candidate identity");records.append(candidate);candidate_count+=1
                                    if candidate["status"] == "COMPLETE":check_maturity(candidate["fit_diagnostics"],candidate["maturity"],w,h,"validation",design,method)
                                selection_path=unit/f"W{w}_H{h}_{method}.selection.json"
                                if selection_path.exists():
                                    selection=select_from_records(records,method,design)
                                    compare(read(selection_path),selection,"independent lambda selection")
                                    require(row.get("selected_penalty") == selection["penalty"], "selected evaluation lambda")
                                    if selection["status"] == "INELIGIBLE":require(row["status"] == "FAILED" and row.get("reason") == "VALIDATION_INELIGIBLE", "mandatory menu failure policy")
                                else:
                                    require(row["status"] != "COMPLETE" and row.get("selected_penalty") is None,
                                            "missing selection cannot yield a completed selected procedure")
                                require(row.get("candidates",[]) == records or row["status"] != "COMPLETE", "all selected-procedure candidate records retained")
                            trace_path=unit/f"W{w}_H{h}_{method}_evaluation.npz"
                            if trace_path.exists():
                                require(position is not None,"complete forecast must have retained input")
                                with np.load(trace_path,allow_pickle=False) as z:trace={k:z[k] for k in z.files}
                                score=check_trace(position,trace,h,w,method,design);trace_count+=1
                            if row["status"] == "COMPLETE":
                                require(trace_path.exists(),"complete procedure requires evaluation trace")
                                compare(row["evaluation"],score,"independent final evaluation")
                                check_maturity(row["fit_diagnostics"],row["maturity"],w,h,"evaluation",design,method)
                            else:require(row.get("evaluation") is None,"failed procedure cannot carry full evaluation")
    require(all(b <= a for b,a in zip(ended_clocks,started_clocks[1:])),"single numerical worker, no overlapping worker clocks")
    summaries=[]
    for di,dgp in enumerate(design["dgp"]):
        for pi,phi in enumerate(design["phi"]):
            for w in design["windows"]:
                planned=16 if w in term["removed_windows"] else 32
                for h in design["horizons"]:
                    for method in METHODS:
                        a={rep:scores[(rep,dgp,pi,w,h,method)] for rep in range(planned)};b={rep:scores[(rep,dgp,pi,w,h,"F")] for rep in range(planned)}
                        summaries.append(dict(dgp=dgp,dgp_index=di,phi=phi,phi_index=pi,window=w,horizon=h,method=method,
                            initial_planned_repetitions=32,budget_reduced=w in term["removed_windows"],**independent_summary(a,b,planned)))
    require(len(summaries) == len(saved_summaries) == 144,"all summary cells")
    compare(saved_summaries,summaries,"independent complete/conditional summary")
    with (formal/"summary.csv").open(newline="") as f:csv_rows=list(csv.DictReader(f))
    require(len(csv_rows)==144,"CSV summary census")
    for actual,expected in zip(csv_rows,summaries):
        for k,v in expected.items():require(actual[k] == ("" if v is None else str(v)),"CSV/JSON summary "+k)
    screen=independent_screen(summaries,design);compare(saved_screen,screen,"independent confirmation screen")
    require(all(digest(Path(p)) == sha for p,sha in snapshots.items()),"formal results unchanged by audit")
    probe_audit();elapsed=time.monotonic()-began;rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed <= 600 and rss <= 2147483648,"audit actual resource bounds")
    result=dict(status="PASS",mismatch_count=0,differences=[],difference_count=0,initial_inventory_records=4608,summary_cells=144,
        synthetic_inputs_regenerated=synthetic_count,evaluation_traces_verified=trace_count,candidate_receipts_checked=candidate_count,
        worker_resource_receipts=resource_count,worker_maximum_rss_bytes=maximum_rss,worker_maximum_os_threads=maximum_threads,
        worker_maximum_wall_seconds=maximum_worker_wall,inventory_status_counts=dict(Counter(x["status"] for x in inventory)),
        removed_windows=term["removed_windows"],P1=screen["P1"],P2=screen["P2"],P3={k:v for k,v in screen["P3"].items() if k != "pairs"},
        primary_status=screen["primary_status"],by_method={k:v["primary_status"] for k,v in screen["by_method"].items()},
        by_DGP={k:v["primary_status"] for k,v in screen["by_DGP"].items()},audit_elapsed_seconds=elapsed,audit_peak_rss_bytes=rss,
        audit_maximum_observed_os_threads=audit_max_threads,audit_numerical_threads_configured=1,
        production_core_imported=False,production_aggregation_imported=False,model_fits_run=0,
        validation_boundary="selection from retained scalar validation losses; validation forecast traces were not saved",
        original_files_written=0)
    if args.output is not None:
        target=args.output if args.output.is_absolute() else root/args.output
        with target.open("x") as stream:stream.write(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__ == "__main__":
    main()
