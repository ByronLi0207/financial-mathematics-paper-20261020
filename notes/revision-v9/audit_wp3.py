"""Independent saved-trace WP3 oracle; never fits or issues new QR forecasts.

Run only after the sole formal process ends. Raw positions, forecast vectors and
per-observation values remain private; console/receipt contain only aggregate
verification counts, identifiers and predeclared curve classifications.
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import signal
import subprocess
import time
from collections import Counter
from fractions import Fraction
import numpy as np

DESIGN_COMMIT="b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a"
DESIGN_SHA="0490302463c17096b612fa7241cae97fed082052cefd29f176f0eba3926aedae"
ATOL,RTOL=1e-10,1e-12
THREADS=("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS","NUMBA_NUM_THREADS")

class AuditMismatch(AssertionError):pass

def require(condition,label):
    if not condition:raise AuditMismatch(label)

def validate_manifest_design(manifest,frozen_design):
    """Bind the entire adopted design before any raw/trace fingerprint or read."""
    design=manifest["design"]
    require(isinstance(design,dict) and isinstance(frozen_design,dict),"manifest design object")
    require(json.dumps(design,sort_keys=True,allow_nan=False)==json.dumps(frozen_design,sort_keys=True,allow_nan=False),"manifest design differs from frozen JSON")
    require(design["horizons"]==[6,24] and design["windows"]==[360,720,1440,2880,5760],"fixed H/W plan")
    expected_units={(h,w) for h in (6,24) for w in (360,720,1440,2880,5760)}
    units=[tuple(unit) for unit in design["run_order"]]
    require(len(units)==10 and set(units)==expected_units,"ten unique planned H/W units")
    ranges=design["prediction_ranges"]
    require(len(ranges)==4 and {(row["horizon"],row["method"]) for row in ranges}=={(h,m) for h in (6,24) for m in ("QR33","QR4")},"four unique frozen prediction ranges")
    return design

def validate_output_census(design,status,completed,rows,curves,saved_curves):
    """Verify actual object populations; never infer four checks from existence."""
    planned=[tuple(unit) for unit in design["run_order"]]
    expected_rows={(h,w,m) for h,w in planned for m in ("QR33","QR4")}
    row_keys=[(row["horizon"],row["window"],row["method"]) for row in rows]
    require(len(rows)==20 and len(row_keys)==len(set(row_keys)) and set(row_keys)==expected_rows,"twenty unique conditional rows")
    expected_curves={(h,m) for h in (6,24) for m in ("QR33","QR4")}
    curve_keys=[(row["horizon"],row["method"]) for row in curves]
    require(len(curves)==4 and len(curve_keys)==len(set(curve_keys)) and set(curve_keys)==expected_curves,"four actual curve classifications")
    if status=="COMPLETE":
        require(len(completed)==10 and [tuple(unit) for unit in completed]==planned,"COMPLETE requires all ten planned units")
    if saved_curves is not None:compare(saved_curves,curves,"four frozen curve classifications")
    return dict(planned_units=len(planned),planned_conditional_rows=len(expected_rows),
        verified_units=len(completed),verified_conditional_inventory_rows=len(rows),curve_classifications=len(curves),
        saved_curve_classifications_verified=len(saved_curves) if saved_curves is not None else 0)

def validate_contrast_status_and_na(row,report,reference_summary,h,w):
    """Bind saved contrast status before it can choose a paired-audit branch."""
    fields={"horizon","window","method","status","relative_loss_percent","mean_model_loss","mean_reference_loss","model_breaches","reference_breaches","n","dm"}
    require(isinstance(row,dict) and set(row)==fields,"saved contrast exact schema")
    method=row["method"];status=row["status"]
    require(method in ("QR33","QR4") and isinstance(report,dict) and report.get("method")==method,"saved contrast method report")
    require(status==report.get("status") and status in ("COMPLETE","INELIGIBLE","EVALUATION_FAILED","FAILED"),"contrast status must match legal method-report status")
    compare([row["horizon"],row["window"]],[h,w],"saved contrast H/W")
    if status=="COMPLETE":
        require(isinstance(report.get("evaluation"),dict),"complete contrast requires complete method evaluation")
        return
    require(report.get("evaluation") is None,"failed method has no complete evaluation")
    expected=dict(horizon=h,window=w,method=method,status=status,relative_loss_percent=None,
        mean_model_loss=None,mean_reference_loss=reference_summary["mean_pinball"],model_breaches=None,
        reference_breaches=reference_summary["strict_breach_count"],n=0,dm=None)
    compare(row,expected,"failed contrast retains NA and verified F scalars")

def compare(actual,expected,location="value"):
    if isinstance(expected,dict):
        require(isinstance(actual,dict) and set(actual)==set(expected),location+":keys")
        for k in expected:compare(actual[k],expected[k],location+"."+str(k))
    elif isinstance(expected,(list,tuple)):
        require(isinstance(actual,(list,tuple)) and len(actual)==len(expected),location+":length")
        for i,(a,b) in enumerate(zip(actual,expected)):compare(a,b,location+"["+str(i)+"]")
    elif expected is None or isinstance(expected,(str,bool)):
        require(actual==expected,location+":scalar")
    elif isinstance(expected,int):require(type(actual) is int and actual==expected,location+":integer")
    else:require(type(actual) in (int,float) and math.isfinite(actual) and math.isclose(actual,expected,abs_tol=ATOL,rel_tol=RTOL),location+":number")

def exact_scalar_differences(actual,old,label="science"):
    """Exact old gate; disclose field identifiers, never private observations."""
    out=[]
    if isinstance(old,dict):
        if not isinstance(actual,dict):return [dict(location=label,kind="type")]
        for k,v in old.items():
            if k not in actual:out.append(dict(location=label+"."+str(k),kind="missing"))
            else:out.extend(exact_scalar_differences(actual[k],v,label+"."+str(k)))
    elif isinstance(old,(list,tuple)):
        if not isinstance(actual,(list,tuple)) or len(actual)!=len(old):return [dict(location=label,kind="length")]
        for i,(a,b) in enumerate(zip(actual,old)):out.extend(exact_scalar_differences(a,b,label+"["+str(i)+"]"))
    elif actual!=old or (type(old) in (int,float) and (type(actual) not in (int,float) or not math.isfinite(actual))):
        out.append(dict(location=label,kind="exact_scalar"))
    return out

def exact_array_differences(actual,old,label="array"):
    out=[]
    for k,value in old.items():
        if k not in actual:out.append(dict(location=label+"."+k,kind="missing"));continue
        a,b=np.asarray(actual[k]),np.asarray(value)
        if a.shape!=b.shape or a.dtype!=b.dtype:out.append(dict(location=label+"."+k,kind="shape_or_dtype"))
        elif a.dtype.kind not in "bifu" or not np.isfinite(a).all() or not np.isfinite(b).all() or a.tobytes(order="C")!=b.tobytes(order="C"):
            out.append(dict(location=label+"."+k,kind="exact_array_bytes"))
    return out

def stable(values):
    values=list(map(float,values));require(bool(values) and all(map(math.isfinite,values)),"finite mean")
    return values[0] if all(x==values[0] for x in values) else math.fsum(values)/len(values)

def select_candidate(candidates,method,menus,expected_count):
    key="parameter" if method=="QR33" else "penalty"
    require([r.get(key) for r in candidates]==menus[method],"full original candidate menu")
    complete=[]
    for r in candidates:
        require(r["status"] in ("COMPLETE","FAILED","INCOMPLETE"),"candidate status")
        if r["status"]=="COMPLETE":
            require(math.isfinite(r["mean_pinball"]) and r["mean_pinball"]>=0,"candidate mean")
            if method=="QR33":require(r["origin_count"]==expected_count,"complete validation count")
            complete.append(r)
    if not complete or method=="QR33" and len(complete)!=len(candidates):return None
    choice=sorted(complete,key=lambda r:(r["mean_pinball"],-r[key] if method=="QR33" else menus[method].index(r[key])))[0]
    return choice[key]

def summary_from_arrays(peak,capacity,floor):
    residual=peak-capacity;overrun=np.maximum(residual,0);unused=np.maximum(-residual,0)
    loss=.95*overrun+.05*unused;hit=residual>0;n=len(loss);hits=int(hit.sum())
    return dict(origin_count=n,mean_pinball=stable(loss),mean_capacity=stable(capacity),
        mean_extra_allowance=stable(capacity-floor),strict_breach_count=hits,strict_breach_rate=hits/n,
        mean_positive_overrun=stable(overrun),conditional_mean_overrun=stable(overrun[hit]) if hits else None,
        conditional_overrun_denominator=hits,conditional_overrun_undefined_reason=None if hits else "NO_STRICT_BREACHES",
        mean_unused_allowance=stable(unused))

def score_vectors(position,arrays,horizon,window,segment,clock,method,partial=False):
    require(set(arrays)=={"origins","capacity","peak","floor","refit_indices","pinball"},"six original trace arrays")
    first,last=clock[segment+"_origin_first"],clock[segment+"_origin_last"]
    origins=np.asarray(arrays["origins"]);n=len(origins)
    require(n>0 and n<=last-first+1,"trace issue count")
    require(np.array_equal(origins,np.arange(first,first+n,dtype=np.int64)),"fixed issue prefix")
    if not partial:require(n==last-first+1,"unshortened complete issue grid")
    require(int(origins[-1])+horizon<len(position),"complete realized labels")
    floor=np.abs(position[origins]);peak=np.array([np.max(np.abs(position[int(t):int(t)+horizon+1])) for t in origins])
    refits=first+clock["refit_step"]*((origins-first)//clock["refit_step"])
    require(np.array_equal(arrays["floor"],floor) and np.array_equal(arrays["peak"],peak),"raw-rule floor/peak")
    require(np.array_equal(arrays["refit_indices"],refits),"fixed segment refit clock")
    require(int(refits[0])-horizon-window+1 >= (0 if method=="F" else max(24,clock["short_scale"],clock["long_scale"])),"full mature feature history")
    capacity=np.asarray(arrays["capacity"])
    require(capacity.shape==peak.shape and np.isfinite(capacity).all() and np.all(capacity>=floor),"capacity geometry")
    if method=="F":
        rank=math.ceil(Fraction(19*(window+1),20));require(rank<=window,"corrected rank available")
        headroom=np.array([np.max(np.abs(position[i:i+horizon+1]))-abs(position[i]) for i in range(len(position)-horizon)])
        expected=np.empty(n);by_refit={}
        for r in np.unique(refits):by_refit[int(r)]=np.sort(headroom[int(r)-horizon-window+1:int(r)-horizon+1])[rank-1]
        for i,r in enumerate(refits):expected[i]=floor[i]+by_refit[int(r)]
        require(np.allclose(capacity,expected,atol=ATOL,rtol=RTOL),"independent matched-F own-anchor rule")
    residual=peak-capacity;loss=.95*np.maximum(residual,0)+.05*np.maximum(-residual,0)
    require(np.allclose(arrays["pinball"],loss,atol=ATOL,rtol=RTOL),"individual loss arithmetic")
    return summary_from_arrays(peak,capacity,floor)

def hac_oracle(differences,horizon):
    d=np.asarray(differences,dtype=float);require(d.ndim==1 and len(d)>horizon and np.isfinite(d).all(),"complete paired HAC differences")
    n=len(d);lag=min(n-1,max(horizon,math.floor(4*(n/100)**(2/9))));mean=math.fsum(map(float,d))/n
    out=dict(n=n,horizon=horizon,bandwidth=lag,direction="QR_minus_matched_F",mean_difference=mean,lrv=None,dm_t=None,dm_p=None,status="OK",nominal_post_result=True)
    if np.all(d==d[0]):out.update(lrv=0.,status="IDENTICAL_LOSSES" if d[0]==0 else "ZERO_LONG_RUN_VARIANCE");return out
    centered=d-d.mean();variance=float(np.dot(centered,centered)/n)
    for k in range(1,lag+1):variance+=(1-k/(lag+1))*2*float(np.dot(centered[k:],centered[:-k])/n)
    out["lrv"]=variance
    if not math.isfinite(variance) or variance<=0:out["status"]="NONPOSITIVE_LONG_RUN_VARIANCE";return out
    statistic=mean/math.sqrt(variance/n)
    if not math.isfinite(statistic):out["status"]="NONFINITE_STATISTIC";return out
    out.update(dm_t=statistic,dm_p=math.erfc(abs(statistic)/math.sqrt(2)))
    return out

def classify(windows,deltas,lower,upper):
    w,y=list(windows),list(deltas);require(len(w)==len(y)>0 and all(x>0 for x in w) and all(a<b for a,b in zip(w,w[1:])) and all(x is None or math.isfinite(x) for x in y),"fixed curve grid")
    crossings=[];rights=[]
    for j in range(1,len(w)):
        if y[j-1] is not None and y[j] is not None and y[j-1]>0 and y[j]<=0:
            crossings.append(w[j-1]+(w[j]-w[j-1])*y[j-1]/(y[j-1]-y[j]));rights.append(j)
    out=dict(windows=w,relative_losses=y,first_crossing=None,conditional_crossings=crossings,multiple_crossings=len(crossings)>1,first_right_endpoint_strictly_negative=None,observed_left_censoring=False,prediction_range=[lower,upper])
    if lower is None or lower<=0 or upper is None or not math.isfinite(upper) or upper<lower:status="NOT_TESTABLE_NONDISCRIMINATING_INTERVAL"
    elif y[0] is None:status="NOT_TESTABLE_NA_PREFIX"
    elif y[0]<=0:
        out["observed_left_censoring"]=True;status="INCONSISTENT_LEFT_CENSORED" if lower>w[0] else "NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED"
    elif crossings:
        right=rights[0]
        if any(v is None for v in y[:right+1]):status="NOT_TESTABLE_NA_PREFIX"
        else:
            root=crossings[0];out.update(first_crossing=root,first_right_endpoint_strictly_negative=y[right]<0)
            status="FIRST_CUTPOINT_CONSISTENT" if lower<=root<=upper else "FIRST_CUTPOINT_INCONSISTENT"
    else:
        stop=next((i for i,v in enumerate(y) if v is None),len(y))
        status="INCONSISTENT_NO_CROSSING" if stop and all(v>0 for v in y[:stop]) and lower>=w[0] and upper<=w[stop-1] else "NOT_TESTABLE_NO_CROSSING"
    out["prediction_status"]=status;return out

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def load_npz(path):
    with np.load(path,allow_pickle=False) as data:return {k:data[k] for k in data.files}
def block_arrays(data,prefix):return {k[len(prefix)+1:]:v for k,v in data.items() if k.startswith(prefix+"_")}

def fit_clock(diagnostics,h,w,segment,clock,method,partial=False):
    first,last=clock[segment+"_origin_first"],clock[segment+"_origin_last"]
    refs=list(range(first,last+1,clock["refit_step"]))
    require(len(diagnostics)<=len(refs) if partial else len(diagnostics)==len(refs),"complete refit diagnostic count")
    for record,r in zip(diagnostics,refs):
        expected=dict(refit_index=r,training_first_origin=r-h-w+1,training_last_origin=r-h,training_count=w,latest_label_end=r)
        if method=="QR4":expected={k.replace("training_first_origin","training_first").replace("training_last_origin","training_last"):v for k,v in expected.items()};expected.pop("training_count")
        for k,v in expected.items():require(record[k]==v,"diagnostic mature-label clock "+k)

def origin_identity(origins):
    ids=np.asarray(origins,dtype="<i8")
    return dict(count=len(ids),first=int(ids[0]),last=int(ids[-1]),sha256=hashlib.sha256(ids.tobytes()).hexdigest())

def science_block(arrays,dates,method,penalty,segment,h,fit_diagnostics=None):
    ids=arrays["origins"];metadata=dict(method=method,parameter=penalty)
    out=dict(summary_rows=[dict(metadata,**summary_from_arrays(arrays["peak"],arrays["capacity"],arrays["floor"]))],year_rows=[],nonoverlap_rows=[],fit_diagnostics=fit_diagnostics or [],origin_identity=origin_identity(ids))
    if segment=="evaluation":
        years=dates[ids].astype("datetime64[Y]").astype(int)+1970
        for year in np.unique(years):
            mask=years==year;out["year_rows"].append(dict(metadata,year=int(year),**summary_from_arrays(arrays["peak"][mask],arrays["capacity"][mask],arrays["floor"][mask])))
        mask=(ids-ids[0])%(h+1)==0
        out["nonoverlap_rows"].append(dict(metadata,**summary_from_arrays(arrays["peak"][mask],arrays["capacity"][mask],arrays["floor"][mask])))
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--root",type=Path,default=Path.cwd());parser.add_argument("--formal",type=Path,default=Path(".scratch/revision-v9/wp3-run"));parser.add_argument("--private",type=Path,default=Path(".scratch/revision-v9/wp3-private"));parser.add_argument("--output",type=Path);args=parser.parse_args()
    root=args.root.resolve();formal=args.formal if args.formal.is_absolute() else root/args.formal;private=args.private if args.private.is_absolute() else root/args.private
    began=time.monotonic();signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError("WP3 independent audit budget")));signal.alarm(590)
    require(all(os.environ.get(k)=="1" for k in THREADS),"audit numerical threads1")
    maximum_threads=0
    def probe():
        nonlocal maximum_threads
        maximum_threads=max(maximum_threads,len(subprocess.check_output(["ps","-M","-p",str(os.getpid())],text=True).strip().splitlines())-1)
        require(maximum_threads<=2 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<=2147483648,"actual audit resource samples")
    probe();term=read(formal/"study-termination.json");require(term["all_workers_terminated"] is True,"formal worker must end before audit")
    manifest=read(formal/"manifest.json")
    require(manifest["design_commit"]==DESIGN_COMMIT and digest(root/"protocol/revision-v9/wp3-learning-curve.json")==DESIGN_SHA,"frozen design identity")
    for name in ("protocol/revision-v9/wp3-learning-curve.md","protocol/revision-v9/wp3-learning-curve.json"):
        require(subprocess.check_output(["git","show",DESIGN_COMMIT+":"+name],cwd=root)==(root/name).read_bytes(),"committed protocol bytes")
    d=validate_manifest_design(manifest,read(root/"protocol/revision-v9/wp3-learning-curve.json"));cfg=d["clock"]
    for name,sha in manifest["sealed_files"].items():require(digest(root/name)==sha,"sealed source/input identity")
    snapshot={str(p):digest(p) for folder in (formal,private) for p in folder.rglob("*") if p.is_file()}
    raw=root/d["raw"]["path"];require(raw.stat().st_size==d["raw"]["bytes"] and digest(raw)==d["raw"]["sha256"],"canonical private FX source")
    with raw.open(newline="") as stream:
        reader=csv.DictReader(stream);require(reader.fieldnames==["datetime","NetPosUsd","NetUsdPnL","AbsVolume","Mid"],"source schema")
        records=list(reader)
    position=np.array([float(r["NetPosUsd"]) for r in records]);dates=np.array([datetime.strptime(r["datetime"],"%Y.%m.%dT%H:%M:%S.%f") for r in records],dtype="datetime64[us]")
    require(len(position)==d["raw"]["record_count"] and np.isfinite(position).all() and np.all(dates[1:]>dates[:-1]),"source count/chronology")
    trace_count=values_count=reports_count=dm_count=worker_count=0
    candidate_reports_count=selection_reports_count=before_gate_reports_count=0
    legacy_differences=[];legacy_unavailable=[];gates=[];expected_rows=[];completed=[];start_clocks=[];end_clocks=[];resource_max=dict(rss_bytes=0,os_threads=0,wall_seconds=0.)
    for h,w in d["run_order"]:
        probe();unit=formal/"units"/f"W{w}_H{h}";pv=private/f"W{w}_H{h}"
        receipt=read(unit/"worker-receipt.json") if (unit/"worker-receipt.json").exists() else None
        if receipt:
            worker_count+=1;res=receipt["resources"];require(res is not None,"worker actual resource receipt")
            require(res["peak_rss_bytes"]<=2147483648 and res["maximum_observed_os_threads"]<=2 and receipt["elapsed_seconds"]<=600,"formal actual resource bounds")
            require(res["requested_numerical_threads"]==1 and res["thread_snapshot_count"]>0,"formal resource measurement")
            resource_max["rss_bytes"]=max(resource_max["rss_bytes"],res["peak_rss_bytes"]);resource_max["os_threads"]=max(resource_max["os_threads"],res["maximum_observed_os_threads"]);resource_max["wall_seconds"]=max(resource_max["wall_seconds"],receipt["elapsed_seconds"])
            start_clocks.append(datetime.fromisoformat(receipt["started_utc"]));end_clocks.append(datetime.fromisoformat(receipt["ended_utc"]))
            if receipt["status"]=="COMPLETE":completed.append([h,w])
            gates.append(dict(horizon=h,window=w,worker_status=receipt["status"],reason=receipt.get("reason"),completed_baseline_checks=receipt.get("baseline_checks",[])))
        current={};validation={};partial_count=0
        if pv.exists():
            for path in sorted(pv.glob("*.npz")):
                arrays=load_npz(path);method=path.name.split("-")[0];segment="validation" if "validation" in path.name else "evaluation";prefixes=[k[:-len("_origins")] for k in arrays if k.endswith("_origins")]
                for prefix in prefixes:
                    block=block_arrays(arrays,prefix);partial="partial" in prefix or "partial" in path.name
                    stats=score_vectors(position,block,h,w,segment,cfg,method,partial=partial);trace_count+=1;values_count+=sum(v.size for v in block.values())
                    if partial:partial_count+=1;continue
                    if segment=="validation":
                        if (method,prefix) in validation:
                            require(not exact_array_differences(block,validation[(method,prefix)][0],"candidate/combined validation duplicate"),"per-candidate and combined private vectors identical")
                        validation[(method,prefix)]=(block,stats)
                    else:current[method]=(block,stats,path)
        persisted_candidates={};persisted_diagnostics={};persisted_selections={}
        for method in ("QR33","QR4"):
            records=[];diagnostics=[]
            for i,penalty in enumerate(d["menus"][method]):
                path=unit/f"{method}-candidate-{i}.json"
                if not path.exists():continue
                bundle=read(path);candidate=bundle["candidate"];candidate_reports_count+=1
                require(candidate.get("parameter" if method=="QR33" else "penalty")==penalty,"persisted candidate identity")
                rows=bundle["fit_diagnostics"];records.append(candidate);diagnostics.append(rows)
                vector_path=pv/f"{method}-validation-candidate-{i}.npz"
                require(vector_path.exists(),"every persisted candidate has private vector container")
                if candidate["status"]=="COMPLETE":
                    require((method,"candidate_"+str(i)) in validation,"completed persisted candidate trace")
                    compare(candidate["mean_pinball"],validation[(method,"candidate_"+str(i))][1]["mean_pinball"],"persisted candidate score")
                    fit_clock(rows,h,w,"validation",cfg,method)
                elif rows and all(isinstance(r,dict) and "refit_index" in r for r in rows):
                    fit_clock(rows,h,w,"validation",cfg,method,partial=True)
                elif rows:
                    legacy_unavailable.append(dict(horizon=h,window=w,method=method,candidate_index=i,scope="failed-candidate raw diagnostic container is preserved but is not a sequence of completed refit diagnostics"))
            persisted_candidates[method]=records;persisted_diagnostics[method]=diagnostics
            path=unit/(method+"-selection.json")
            if path.exists():
                selection_reports_count+=1;bundle=read(path);selected=select_candidate(records,method,d["menus"],cfg["validation_origin_last"]-cfg["validation_origin_first"]+1)
                require(bundle["selected_penalty"]==selected,"persisted selected penalty")
                require(bundle["selection"]["status"]==("SELECTED" if selected is not None else "INELIGIBLE"),"persisted selection status")
                if method=="QR33" and selected is not None:
                    compare(bundle["selection"],dict(status="SELECTED",parameter=selected,mean_validation_pinball=next(x["mean_pinball"] for x in records if x["parameter"]==selected)),"persisted QR33 selection")
                elif method=="QR4":require(bundle["selection"]["eligible_count"]==sum(x["status"]=="COMPLETE" for x in records),"eligible QR4 candidate census")
                persisted_selections[method]=bundle
        report_by_method={}
        for method in ("F","QR33","QR4"):
            path=unit/(method+".json")
            before=unit/(method+"-evaluation-before-gate.json")
            incomplete=unit/(method+"-incomplete-before-gate.json")
            if before.exists():before_gate_reports_count+=1
            if not path.exists():
                path=before if before.exists() else incomplete
            if not path.exists():continue
            report=read(path);report_by_method[method]=report;reports_count+=1
            if before.exists():require(report==read(before),"before-gate evaluation record retained unchanged")
            if method!="F":
                require(report["candidates"]==persisted_candidates[method],"selected report retains every persisted candidate")
                require(method in persisted_selections and report["selected_penalty"]==persisted_selections[method]["selected_penalty"],"selected report bound to prior selection receipt")
                selected=select_candidate(report["candidates"],method,d["menus"],cfg["validation_origin_last"]-cfg["validation_origin_first"]+1)
                require(report["selected_penalty"]==selected,"selected original lambda")
                for i,candidate in enumerate(report["candidates"]):
                    if candidate["status"]=="COMPLETE":
                        require((method,"candidate_"+str(i)) in validation,"completed validation trace retained")
                        stats=validation[(method,"candidate_"+str(i))][1]
                        compare(candidate["mean_pinball"],stats["mean_pinball"],"candidate score")
            else:require(report["selected_penalty"] is None,"F has no lambda")
            if report["status"]=="COMPLETE":
                require(method in current,"completed evaluation trace retained");block,stats,path=current[method]
                require(digest(path)==report["trace_sha256"],"saved private trace hash")
                compare(report["evaluation"],stats,"saved evaluation score");fit_clock(report["fit_diagnostics"],h,w,"evaluation",cfg,method)
            else:require(report.get("evaluation") is None,"failed selected procedure has no complete score")
        if w==2880:
            for method,phase,prefix in (("F","references","frozen_F"),("QR33","validation",None),("QR33","evaluation","QR")):
                info=next(x for x in d["legacy_private"] if x["horizon"]==h and x["phase"]==phase)
                public=next(x for x in d["legacy_public"] if x["horizon"]==h and x["phase"]==phase)
                if method=="QR33" and phase=="validation":
                    if not (pv/"QR33-validation.npz").exists():continue
                    actual={"candidate_"+str(i)+"_"+k:v for i in range(3) if ("QR33","candidate_"+str(i)) in validation for k,v in validation[("QR33","candidate_"+str(i))][0].items()}
                elif method in current:actual={prefix+"_"+k:v for k,v in current[method][0].items()}
                else:continue
                oldarrays=load_npz(root/info["path"])
                if method=="F":oldarrays={k:v for k,v in oldarrays.items() if k.startswith("frozen_F_")}
                legacy_differences.extend(exact_array_differences(actual,oldarrays,f"W2880_H{h}_{method}_{phase}"))
                old=read(root/public["path"])["result"]
                if method=="QR33" and phase=="validation":
                    combined=dict(summary_rows=[],year_rows=[],nonoverlap_rows=[],fit_diagnostics=[],origin_identity={})
                    for i,penalty in enumerate(d["menus"][method]):
                        if (method,"candidate_"+str(i)) not in validation:continue
                        diag=persisted_diagnostics[method][i] if i<len(persisted_diagnostics[method]) else []
                        wrapped=[dict(method="QR",parameter=penalty,**r) for r in diag]
                        block=science_block(validation[(method,"candidate_"+str(i))][0],dates,"QR",penalty,"validation",h,wrapped)
                        combined["origin_identity"]=block["origin_identity"]
                        for key in ("summary_rows","year_rows","nonoverlap_rows","fit_diagnostics"):combined[key].extend(block[key])
                    combined["candidate_rows"]=persisted_candidates[method]
                    combined["selection"]={k:v for k,v in persisted_selections.get(method,{}).get("selection",{}).items() if k!="failed_candidates"}
                    expected={k:old[k] for k in ("summary_rows","year_rows","nonoverlap_rows","fit_diagnostics","origin_identity","candidate_rows","selection")}
                    legacy_differences.extend(exact_scalar_differences(combined,expected,f"H{h}.QR33.validation.full_persisted_science"))
                elif method in current:
                    penalty=report_by_method.get(method,{}).get("selected_penalty",old.get("selection",{}).get("parameter") if old.get("selection") else None)
                    diagnostics=[dict(method="QR",parameter=penalty,**x) for x in report_by_method[method]["fit_diagnostics"]] if method=="QR33" and method in report_by_method else []
                    fresh=science_block(current[method][0],dates,"frozen_F" if method=="F" else "QR",penalty,"evaluation",h,diagnostics)
                    for key in ("summary_rows","year_rows","nonoverlap_rows"):
                        expected=[x for x in old[key] if x["method"]=="frozen_F"] if method=="F" else old[key]
                        legacy_differences.extend(exact_scalar_differences(fresh[key],expected,f"H{h}.{method}.{key}"))
                    if method=="QR33" and method in report_by_method:legacy_differences.extend(exact_scalar_differences(fresh["fit_diagnostics"],old["fit_diagnostics"],f"H{h}.QR33.evaluation.fit_diagnostics"))
            if "QR4" in current:
                info=next(x for x in d["legacy_QR4"] if x["horizon"]==h);oldarrays=load_npz(root/info["private"]["path"]);old=read(root/info["public"]["path"])
                legacy_differences.extend(exact_array_differences(current["QR4"][0],oldarrays,f"H{h}.QR4.evaluation"))
                for i,candidate in enumerate(old["candidates"]):
                    if ("QR4","candidate_"+str(i)) in validation:
                        legacy_differences.extend(exact_scalar_differences(validation[("QR4","candidate_"+str(i))][1]["mean_pinball"],candidate["mean_pinball"],f"H{h}.QR4.validation.candidate_{i}.mean_pinball"))
                if "QR4" in report_by_method:
                    report=report_by_method["QR4"]
                    for key in ("status","selected_penalty","candidates","evaluation","fit_diagnostics"):legacy_differences.extend(exact_scalar_differences(report[key],old[key],f"H{h}.QR4.{key}"))
                legacy_unavailable.append(dict(horizon=h,method="QR4",scope="old validation/floor/refit vectors absent; no archived comparison claim"))
        path=unit/"contrasts.json"
        if receipt and receipt["status"]=="COMPLETE":
            require(path.exists() and set(report_by_method)=={"F","QR33","QR4"},"complete worker preserves reports and contrasts")
        if path.exists():
            contrasts=read(path);require(len(contrasts)==2,"two conditional contrasts")
            for row in contrasts:
                method=row["method"]
                require(method in report_by_method and "F" in current,"saved contrast requires method report and verified F trace")
                validate_contrast_status_and_na(row,report_by_method[method],current["F"][1],h,w)
                if row["status"]=="COMPLETE":
                    require(method in current and "F" in current,"same-target paired traces")
                    a,b=current[method][1],current["F"][1];delta=100*(a["mean_pinball"]-b["mean_pinball"])/b["mean_pinball"] if b["mean_pinball"]>0 else None
                    difference=current[method][0]["pinball"]-current["F"][0]["pinball"];dm=hac_oracle(difference,h)
                    expected=dict(horizon=h,window=w,method=method,status="COMPLETE",relative_loss_percent=delta,mean_model_loss=a["mean_pinball"],mean_reference_loss=b["mean_pinball"],model_breaches=a["strict_breach_count"],reference_breaches=b["strict_breach_count"],n=a["origin_count"],dm=dm)
                    compare(row,expected,"paired contrast/HAC");dm_count+=1
                else:require(row["relative_loss_percent"] is None and row["dm"] is None,"incomplete pair remains NA")
            expected_rows.extend(contrasts)
        else:
            for method in ("QR33","QR4"):expected_rows.append(dict(horizon=h,window=w,method=method,status="NOT_ATTEMPTED",relative_loss_percent=None,mean_model_loss=None,mean_reference_loss=None,model_breaches=None,reference_breaches=None,n=0,dm=None))
    require(all(b<=a for b,a in zip(end_clocks,start_clocks[1:])),"no overlapping financial numerical workers")
    require(completed==term["completed_units"],"actual complete unit inventory")
    if term["status"]!="COMPLETE":
        attempted=[(g["horizon"],g["window"]) for g in gates]
        require(attempted==[tuple(x) for x in d["run_order"][:len(attempted)]],"hard-stop run order")
        require(not any(g["worker_status"]=="COMPLETE" for g in gates[next((i for i,g in enumerate(gates) if g["worker_status"]!="COMPLETE"),len(gates))+1:]),"no work after hard stop")
    require(not legacy_differences or term["status"]=="BLOCKED","exact legacy mismatch must block")
    require(not any(g["worker_status"]=="COMPLETE" and g["window"]==2880 for g in gates) or all(c["status"]=="PASS" for g in gates if g["window"]==2880 and g["worker_status"]=="COMPLETE" for c in g["completed_baseline_checks"]),"completed legacy gate receipts")
    if (formal/"contrasts.json").exists():compare(read(formal/"contrasts.json"),expected_rows,"complete displayed contrast inventory")
    curves=[]
    for band in d["prediction_ranges"]:
        rows=sorted((r for r in expected_rows if r["horizon"]==band["horizon"] and r["method"]==band["method"]),key=lambda r:r["window"])
        curves.append(dict(horizon=band["horizon"],method=band["method"],**classify([r["window"] for r in rows],[r["relative_loss_percent"] for r in rows],band["lower"],band["upper"])))
    saved_curves=read(formal/"curve-predictions.json") if (formal/"curve-predictions.json").exists() else None
    census=validate_output_census(d,term["status"],completed,expected_rows,curves,saved_curves)
    require(all(digest(Path(path))==sha for path,sha in snapshot.items()),"formal/private traces unchanged")
    probe();elapsed=time.monotonic()-began;rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;require(elapsed<=600 and rss<=2147483648,"audit resource cap")
    aggregate_outputs_present=all((formal/name).exists() for name in ("contrasts.json","curve-predictions.json","contrasts.csv"))
    result=dict(status="PASS",audit_status="PASS",differences=[],difference_count=0,mismatch_count=0,
        formal_study_status=term["status"],formal_study_reason=term.get("reason"),scientific_WP3_complete=term["status"]=="COMPLETE" and not legacy_differences and aggregate_outputs_present,
        saved_aggregate_outputs_present=aggregate_outputs_present,saved_curve_classifications_verified=census["saved_curve_classifications_verified"],
        legacy_hard_gate_status="BLOCKED" if term["status"]=="BLOCKED" and any(g["window"]==2880 and g["worker_status"]=="BLOCKED" for g in gates) else ("PASS" if sum(g["window"]==2880 and g["worker_status"]=="COMPLETE" for g in gates)==2 and not legacy_differences else "INCOMPLETE"),
        independent_legacy_exact_difference_count=len(legacy_differences),independent_legacy_exact_differences=legacy_differences,
        legacy_verification_boundaries=legacy_unavailable,worker_gates=gates,complete_units=completed,planned_units=census["planned_units"],planned_conditional_rows=census["planned_conditional_rows"],
        verified_complete_units=census["verified_units"],verified_conditional_inventory_rows=census["verified_conditional_inventory_rows"],actual_curve_classifications=census["curve_classifications"],
        actual_resource_worker_receipts=worker_count,formal_resource_maximum=resource_max,scored_trace_blocks=trace_count,checked_numeric_values=values_count,
        retained_method_reports=reports_count,persisted_candidate_reports_verified=candidate_reports_count,
        persisted_selection_reports_verified=selection_reports_count,before_gate_evaluation_reports_verified=before_gate_reports_count,
        HAC_pairs_recomputed=dm_count,curve_classifications=[dict(horizon=x["horizon"],method=x["method"],prediction_status=x["prediction_status"]) for x in curves],
        conditional_row_status_counts=dict(Counter(x["status"] for x in expected_rows)),audit_elapsed_seconds=elapsed,audit_peak_rss_bytes=rss,
        audit_maximum_observed_os_threads=maximum_threads,audit_numerical_threads_configured=1,new_model_fits=0,new_forecasts_issued=0,
        production_aggregation_imported=False,private_observations_disclosed=False)
    if args.output:
        target=args.output if args.output.is_absolute() else root/args.output
        with target.open("x") as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write("\n")
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=="__main__":main()
