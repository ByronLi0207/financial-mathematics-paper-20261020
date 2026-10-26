"""Independent provenance/Matplotlib-receipt readback; no plotter import.

This checks stored plotted coordinates and parameters, not pixel appearance.
Full-range panels must show all finite points; explicitly labelled detail panels
can crop their view only when complete full-range evidence remains alongside.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import signal
import struct
import subprocess
import time

class AuditMismatch(AssertionError):pass

def require(condition,label):
    if not condition:raise AuditMismatch(label)

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())

def logical_group(point):
    family=point["family"]
    if family in ("v8_sim","v9_sim"):return family
    if family=="curve":return "curve_H"+str(point["horizon"])
    require(family=="empirical","known point family")
    return "empirical_panel" if point["source"].startswith("panel:") else "empirical_"+point["source"]

MARKERS={"v8_sim":"x","v9_sim":"+","empirical_fx_hourly":"o","empirical_fx_daily":"^",
    "empirical_nyfed_weekly":"s","empirical_panel":"D","curve_H6":"o","curve_H24":"v"}

def expected_period_key(point):
    repeated=point["source"]=="fx_hourly" and (point["family"]=="empirical" or
        point["family"]=="curve" and point["window"] in (720,2880))
    return f"fx_hourly:{point['horizon']}:{point['window']}:{point['method']}" if repeated else None

def audit_panel(panel,point_index,bands):
    ids=panel["point_ids"];require(bool(ids) and len(ids)==len(set(ids)),"panel unique point census")
    require(all(x in point_index for x in ids),"panel point provenance")
    methods={point_index[x]["method"] for x in ids};require(len(methods)==1,"one method per panel")
    method=next(iter(methods));expected={x for x,p in point_index.items() if p["method"]==method}
    require(set(ids)==expected,"panel includes every method point without same-x pooling")
    xl,yl=panel["xlim"],panel["ylim"]
    require(len(xl)==len(yl)==2 and all(math.isfinite(x) for x in xl+yl) and 0<xl[0]<xl[1] and yl[0]<yl[1],"finite log-x panel limits")
    visible={x for x in ids if xl[0]<=point_index[x]["c"]<=xl[1] and yl[0]<=point_index[x]["relative_loss_percent"]<=yl[1]}
    require(len(panel["visible_point_ids"])==len(set(panel["visible_point_ids"])) and set(panel["visible_point_ids"])==visible,"actual visible-ID envelope")
    if panel["full_range"]:require(visible==expected,"full-range panel cannot crop an outlier")
    band=bands[method]
    require(band["lower"]>0 and band["upper"] is not None and not band["upper_unbounded"] and xl[0]<=band["lower"]<=band["upper"]<=xl[1],"all-draw band inside log-x view")
    offsets=0;seen=Counter();groups={};line_count=scatter_count=0
    for artist in panel["artists"]:
        selected=artist["point_ids"];xy=artist["actual_offsets"]
        require(bool(selected) and len(selected)==len(xy) and len(selected)==len(set(selected)),"artist point/offset count")
        require(all(x in expected for x in selected),"artist method/source membership")
        labels={logical_group(point_index[x]) for x in selected};require(len(labels)==1,"one source group per artist")
        group=next(iter(labels));require(group not in groups,"source group cannot be split/duplicated silently");groups[group]=set(selected)
        require(artist["marker"]==MARKERS[group],"source/generation/horizon marker identity")
        require(artist["kind"]==("line" if group.startswith("curve_H") else "scatter"),"learning-curve line versus source scatter")
        if artist["kind"]=="line":
            windows=[point_index[x]["window"] for x in selected]
            require(all(a<b for a,b in zip(windows,windows[1:])),"learning-curve order by true W")
            line_count+=1
        else:scatter_count+=1
        for point_id,actual in zip(selected,xy):
            p=point_index[point_id]
            require(len(actual)==2 and all(math.isfinite(v) for v in actual),"finite artist offset")
            require(actual[0]==p["c"] and actual[1]==p["relative_loss_percent"],"artist exact coordinates, no jitter/rounding")
            seen[point_id]+=1;offsets+=1
    require(seen==Counter({x:1 for x in expected}),"each point occurs exactly once per panel")
    expected_groups={logical_group(point_index[x]) for x in expected}
    require(set(groups)==expected_groups,"every source group represented")
    for group in groups:require(groups[group]=={x for x in expected if logical_group(point_index[x])==group},"no dropped coincident-x point")
    return dict(panel=panel["panel"],method=method,full_range=panel["full_range"],point_count=len(ids),visible_point_count=len(visible),
        detail_outside_view_count=len(ids)-len(visible),artist_count=len(panel["artists"]),scatter_artists=scatter_count,line_artists=line_count,artist_offsets_verified=offsets)

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--root",type=Path,default=Path.cwd())
    parser.add_argument("--render",type=Path,required=True);parser.add_argument("--output",type=Path,required=True);args=parser.parse_args()
    root=args.root.resolve();render=args.render if args.render.is_absolute() else root/args.render
    begin=time.monotonic();signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError("WP4 QA600s")));signal.alarm(590)
    initial={str(p):digest(p) for p in render.iterdir() if p.is_file()}
    inventory=read(root/"notes/revision-v9/wp4-source-inventory.json");receipt=read(render/"render-receipt.json");points=read(render/"points.json")
    for record in inventory["source_hashes"].values():
        p=root/record["path"];require(p.stat().st_size==record["bytes"] and digest(p)==record["sha256"],"independently inventoried source fingerprint")
    expected={(p["source_path"],p["source_json_index"]):p for p in inventory["point_records"]}
    require(len(points)==len(expected)==380,"380 conditional records, not428")
    point_index={p["point_id"]:p for p in points};require(len(point_index)==380,"unique plot point IDs")
    actual={(p["source_file"],p["source_index"]):p for p in points};require(len(actual)==380 and set(actual)==set(expected),"complete source-row mapping")
    source_cache={};family_map={"simulation_v8":"v8_sim","simulation_v9":"v9_sim","empirical_old":"empirical","empirical_learning_curve":"curve"}
    family_counts=Counter();source_counts=Counter();method_counts=Counter();overlap=[]
    for key,source in expected.items():
        p=actual[key];family=family_map[source["category"]];family_counts[family]+=1;source_counts[p["source"]]+=1;method_counts[p["method"]]+=1
        require(p["family"]==family and p["method"]==source["method"] and p["window"]==source["window"] and p["horizon"]==source["horizon"],"point family/method/W/H")
        require(p["source_sha256"]==source["source_sha256"] and p["source_y_field"]==source["y_field"],"exact y-field and source fingerprint binding")
        if key[0] not in source_cache:source_cache[key[0]]=read(root/key[0])
        row=source_cache[key[0]][key[1]];value=row[source["y_field"]]
        require(p["relative_loss_percent"]==value==source["y"] and math.isfinite(value),"source ordinate unchanged")
        exact=Fraction(row["window"],row["horizon"]+1)
        require(Fraction(p["c_fraction"])==exact and p["c"]==float(exact)==source["x"],"exact c coordinate, no p substitution")
        require(p["status"]=="COMPLETE" and p["nominal_coefficients"]=={"QR33":34,"QR4":5}[p["method"]],"status/nominal coefficient label")
        if family=="v8_sim":
            require(p["source"]=="v8_AR_GARCH" and p["phi"]==row["phi"] and p["variance_persistence"]==row["variance_persistence"],"v8 DGP metadata")
        elif family=="v9_sim":require(p["source"]==row["dgp"] and p["dgp"]==row["dgp"] and p["phi"]==row["phi"],"new DGP metadata")
        elif family=="empirical":
            require(p["source"]==row["source"] and p["underlying_source_file"]==row["source_file"] and p["underlying_source_row"]==row["source_row"],"old empirical CSV locator")
        else:require(p["source"]=="fx_hourly","fixed-source learning curve")
        is_overlap=family=="curve" and p["window"] in (720,2880)
        require(p["overlapping_old_FX_cell"]==is_overlap,"same-period repeated-cell flag")
        require(p["same_period_key"]==expected_period_key(p),"same-period repeated-cell lineage key")
        if is_overlap:overlap.append(p)
    require(family_counts=={"v8_sim":144,"v9_sim":96,"empirical":120,"curve":20} and method_counts=={"QR33":190,"QR4":190},"conditional point census")
    require(len(overlap)==8,"eight retained repeated old/new FX tasks")
    old_by_key={p["same_period_key"]:p for p in points if p["family"]=="empirical" and p["source"]=="fx_hourly"}
    for point in overlap:
        old=old_by_key[point["same_period_key"]]
        require(old["point_id"]!=point["point_id"] and old["c"]==point["c"] and math.isclose(old["relative_loss_percent"],point["relative_loss_percent"],abs_tol=1e-10,rel_tol=1e-12),"preserved repeated provenance with frozen arithmetic")
    excluded=read(render/"excluded-reference-rows.json");excluded_keys={(r["source_file"],r["source_index"]) for r in excluded}
    expected_excluded={(r["source_path"],r["source_json_index"]) for r in inventory["excluded_F_self_reference_rows"]}
    require(len(excluded)==len(excluded_keys)==48 and excluded_keys==expected_excluded and all(x["method"]=="F" for x in excluded),"exclude exactly48 reference self-comparisons")
    for record in excluded:require(source_cache[record["source_file"]][record["source_index"]]["method"]=="F","excluded row actual method")
    with (render/"points.csv").open(newline="") as stream:csv_points=list(csv.DictReader(stream))
    require(len(csv_points)==380,"CSV point census")
    for a,b in zip(csv_points,points):
        require(set(a)==set(b) and all(a[k]==("" if v is None else str(v)) for k,v in b.items()),"CSV/JSON field identity")
    require(receipt["metric"]=="c=W/(H+1)" and receipt["x_scale"]=="log" and receipt["parameter_count_in_metric"] is False,"displayed metric metadata")
    require(receipt["point_count"]==380 and receipt["family_counts"]==dict(family_counts) and receipt["method_counts"]==dict(method_counts) and receipt["source_counts"]==dict(source_counts),"actual render census")
    require(receipt["excluded_F_reference_self_rows"]==48 and receipt["overlapping_old_FX_curve_records"]==8 and receipt["deduplicated_records"]==receipt["jittered_records"]==receipt["rounded_ordinates"]==0,"no hidden trimming or transformation")
    expected_bindings={p["source_file"] for p in points};require({x["path"] for x in receipt["source_bindings"]}==expected_bindings,"four source bindings")
    for binding in receipt["source_bindings"]:
        path=root/binding["path"];require(digest(path)==binding["sha256"] and path.stat().st_size==binding["bytes"] and len(read(path))==binding["source_rows"],"source row/hash receipt")
    bands_source=root/receipt["band_source"];require(digest(bands_source)==receipt["band_source_sha256"],"all-draw band source hash")
    bands_data=read(bands_source);bands={method:bands_data["methods"][method]["intervals"]["all_draw_envelope"] for method in ("QR33","QR4")}
    require(receipt["bands"]==bands,"band uses entire-draw envelope, not finite-only interval")
    named=read(root/inventory["source_hashes"]["wp1"]["path"])
    require(all(bands[m]==named["methods"][m]["intervals"]["all_draw_envelope"] for m in bands),"WP1 independent envelope binding")
    panel_results=[audit_panel(panel,point_index,bands) for panel in receipt["panels"]]
    require(len(panel_results)==4,"two full-range plus two detail panels")
    for method in ("QR33","QR4"):
        pp=[x for x in panel_results if x["method"]==method];require(len(pp)==2 and sum(x["full_range"] for x in pp)==1,"one complete full-range panel per method")
    for name,sha in receipt["output_sha256"].items():require(digest(render/name)==sha,"delivered artifact hash "+name)
    png=(render/"unified-history.png").read_bytes();pdf=(render/"unified-history.pdf").read_bytes()
    require(png[:8]==b'\x89PNG\r\n\x1a\n' and pdf.startswith(b'%PDF-'),"PNG/PDF file identity")
    width,height=struct.unpack('>II',png[16:24]);require(width>0 and height>0,"nonempty raster extent")
    generation_copies={}
    for version in ("render-v2","render-v3","render-v4"):
        other=render.parent/version
        if other.exists():
            require((other/"points.json").read_bytes()==(render/"points.json").read_bytes() and (other/"points.csv").read_bytes()==(render/"points.csv").read_bytes(),"layout-only prior render point identity "+version)
            generation_copies[version]="points JSON/CSV byte-identical; originals retained"
    require(receipt["new_model_fits"]==receipt["new_predictions"]==0 and receipt["maximum_observed_os_threads"]<=2 and receipt["peak_rss_bytes"]<=2147483648 and receipt["requested_numerical_threads"]==1,"plotting actual resource/no-model scope")
    require(all(digest(Path(path))==sha for path,sha in initial.items()),"final render files unchanged by audit")
    observed_threads=len(subprocess.check_output(["ps","-M","-p",str(os.getpid())],text=True).strip().splitlines())-1
    elapsed=time.monotonic()-begin;rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed<=600 and rss<=2147483648 and observed_threads<=2,"actual audit resources")
    result=dict(status="PASS",differences=[],difference_count=0,mismatch_count=0,render_directory=str(render.relative_to(root)),
        point_count=380,family_counts=dict(family_counts),method_counts=dict(method_counts),excluded_F_self_reference_rows=48,retained_same_period_overlap_pairs=8,
        panels=panel_results,actual_artist_count=sum(x["artist_count"] for x in panel_results),actual_artist_offsets_verified=sum(x["artist_offsets_verified"] for x in panel_results),
        all_unique_points_visible_in_full_range=True,no_outlier_dropped=True,detail_views_explicit=True,all_draw_band_parameters_verified=True,
        source_row_mapping_verified=380,CSV_JSON_fields_verified=380,prior_render_metadata_identity=generation_copies,
        PNG_dimensions=[width,height],output_sha256=receipt["output_sha256"],audit_elapsed_seconds=elapsed,audit_peak_rss_bytes=rss,
        audit_observed_os_threads=observed_threads,model_fits_run=0,new_statistics_fit=0,production_plotter_imported=False,
        verification_boundary="stored Matplotlib offsets/markers/axis limits and band parameters verified; pixel appearance and legend readability are separate visual QA")
    target=args.output if args.output.is_absolute() else root/args.output
    with target.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=="__main__":main()
