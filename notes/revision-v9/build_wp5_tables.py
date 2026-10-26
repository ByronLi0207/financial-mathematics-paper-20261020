"""Generate literal-number TeX evidence from immutable accepted JSON sources.

No model, estimator, test statistic or forecast is run. Every displayed numeric
token has a file hash and JSON pointer binding. Main-text namedfacts are literal
strings, never TeX macros concealing numerical content from readability checks.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
import sys
from pathlib import Path

PATHS={
    "wp1":"results/revision-v9/wp1/breakeven.json",
    "wp2":"results/revision-v9/wp2/support.json",
    "wp2_summary":"results/revision-v9/wp2/summary.json",
    "curves":"results/revision-v9/wp3/curve-predictions.json",
    "contrasts":"results/revision-v9/wp3/contrasts.json",
}
MODEL={"QR33":"Original regression","QR4":"Four-predictor regression"}
DGP={"student_t5":"Student innovations","regime_3to1":"Regime switching","compound_poisson":"Poisson jumps"}
STATUS={"SUPPORT":"Met","NOT_SUPPORT":"Not met","INCONCLUSIVE":"Inconclusive"}
CURVE_STATUS={
    "FIRST_CUTPOINT_CONSISTENT":"Consistent",
    "FIRST_CUTPOINT_INCONSISTENT":"Inconsistent",
    "NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED":"Compatible, left-censored",
    "INCONSISTENT_LEFT_CENSORED":"Inconsistent, left-censored",
    "NOT_TESTABLE_NA_PREFIX":"Untestable, missing prefix",
    "INCONSISTENT_NO_CROSSING":"Inconsistent, no crossing",
    "NOT_TESTABLE_NO_CROSSING":"Untestable, no crossing",
    "NOT_TESTABLE_NONDISCRIMINATING_INTERVAL":"Untestable interval",
}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def resolve(document,pointer):
    value=document
    if pointer:
        for part in pointer.lstrip("/").split("/"):
            key=part.replace("~1","/").replace("~0","~")
            value=value[int(key)] if isinstance(value,list) else value[key]
    return value

def escape(value):
    return str(value).replace("\\",r"\textbackslash{}").replace("&",r"\&").replace("%",r"\%").replace("_",r"\_").replace("#",r"\#")

def math_token(value):
    if "e" in value.lower():
        mantissa,exponent=value.lower().split("e")
        value=mantissa+r"\times10^{"+str(int(exponent))+"}"
    return "$"+value+"$"

def formatted(style,values):
    """Display choices fixed before output: percentages1dp, others3--4sigfig."""
    first=values[0] if values else None
    if style=="integer":
        assert type(first) is int
        plain=str(first);return plain,math_token(plain)
    if style=="fraction":
        assert all(type(x) is int for x in values)
        plain=str(values[0])+"/"+str(values[1]);return plain,math_token(plain)
    if style=="percent":
        plain="NA" if first is None else format(100*first,".1f")
        return plain,escape(plain) if first is None else math_token(plain)
    if style=="loss":
        plain="NA" if first is None else format(first,"+.1f")
        return plain,escape(plain) if first is None else math_token(plain)
    if style in ("sig3","sig4"):
        plain="NA" if first is None else format(first,".3g" if style=="sig3" else ".4g")
        return plain,escape(plain) if first is None else math_token(plain)
    if style=="interval4":
        lo,hi=values
        plain="["+("0" if lo==0 else format(lo,".4g"))+", "+("unbounded" if hi is None else format(hi,".4g"))+"]"
        token="$["+("0" if lo==0 else format(lo,".4g"))+", "+(r"\infty" if hi is None else format(hi,".4g"))+"]$"
        return plain,token
    if style=="pvalue":
        if first is None:return "NA","NA"
        if first==0:return "0 (floating-point)",r"$0^{u}$"
        plain=format(first,".2e") if first<.001 else format(first,".3g")
        return plain,math_token(plain)
    if style=="status":
        plain=STATUS[first];return plain,plain
    if style=="curve_status":
        plain=CURVE_STATUS[first]
        return plain,r"\shortstack[l]{"+escape(plain).replace(", ",r",\\")+"}"
    if style=="root":
        if first is not None:
            plain=format(first,".4g");return plain,math_token(plain)
        plain="Left-censored" if len(values)>1 and values[1] else "Unidentified"
        return plain,plain
    if style=="false_count":
        plain=str(sum(x["outcome"] is False for x in first));return plain,math_token(plain)
    if style=="identified_count":
        plain=str(sum(x["first_crossing"] is not None for x in first));return plain,math_token(plain)
    if style=="consistent_count":
        plain=str(sum(x["prediction_status"]=="FIRST_CUTPOINT_CONSISTENT" for x in first));return plain,math_token(plain)
    if style=="string":
        plain=str(first);return plain,escape(plain)
    raise ValueError("unregistered display policy "+style)

def build(root):
    docs={key:json.loads((root/path).read_text()) for key,path in PATHS.items()}
    seals={key:dict(path=path,bytes=(root/path).stat().st_size,sha256=sha(root/path)) for key,path in PATHS.items()}
    wp1,wp2,summary,curves,contrasts=(docs[k] for k in ("wp1","wp2","wp2_summary","curves","contrasts"))
    assert wp1["selected_metric"]=="c"
    assert len(summary)==144 and len(curves)==4 and len(contrasts)==20
    assert len({(r["horizon"],r["window"],r["method"]) for r in contrasts})==20
    bindings=[];namedfacts={};namedfact_sources={};rows=[];tex=[]
    def bind(source,pointers,style,name=None):
        if isinstance(pointers,str):pointers=[pointers]
        values=[resolve(docs[source],p) for p in pointers]
        display,token=formatted(style,values)
        record=dict(id="V9N"+str(len(bindings)+1).zfill(4),source_path=PATHS[source],
            source_sha256=seals[source]["sha256"],JSON_pointers=pointers,raw_values=values,
            format_style=style,display=display,tex_token=token,table_location=None)
        bindings.append(record)
        if name is not None:
            namedfacts[name]=display;namedfact_sources[name]=record["id"]
        return record
    def composite_fact(name,parts,display):
        namedfacts[name]=display;namedfact_sources[name]=[p["id"] for p in parts]
    def row(table_id,row_id,cells):
        tokens=[]
        for column,value in enumerate(cells):
            if isinstance(value,dict):
                tokens.append(value["tex_token"])
                value["table_location"]=dict(row_tag=table_id+":"+str(row_id),column=column)
            else:tokens.append(value)
        line=" & ".join(tokens)+r" \\ % v9-row:"+table_id+":"+str(row_id)
        tex.append(line);rows.append(dict(row_tag=table_id+":"+str(row_id),tokens=tokens))
    def table_start(label,title,spec,header):
        tex.extend([r"\par\medskip\refstepcounter{table}\label{tab:"+label+"}",
            r"\noindent\textbf{Table \thetable. "+title+r"}\par",
            r"\begin{center}\begin{tabular}{"+spec+"}",r"\toprule",header+r" \\",r"\midrule"])
    def table_end():
        tex.extend([r"\bottomrule",r"\end{tabular}\end{center}"])
    def note(value):
        tex.extend([r"\noindent\begin{minipage}{0.98\linewidth}\scriptsize "+value+r"\end{minipage}\par\smallskip"])
    tex.extend(["% Generated only from accepted v9 JSON. Numerical literals are source-bound.",
        "% Display policy: loss/accuracy percentages1dp; cutpoints/intervals4sig; correlations/p3sig; exact counts.",
        r"\clearpage\begingroup\footnotesize",
        r"\setlength{\tabcolsep}{3.5pt}\renewcommand{\arraystretch}{1.08}",
        r"\subsection*{Post hoc discovery and simulation confirmation}"])
    table_start("v9-discovery-scores","Post hoc candidate-index comparison.","lrrrrr",
        r"Index & Correct/total & Accuracy (\%) & $\rho$, pooled & $\rho$, original & $\rho$, four predictors")
    metric_tex={"a":r"$W/p$","b":r"$W/((H+1)p)$","c":r"$W/(H+1)$"}
    for candidate in ("a","b","c"):
        p="/candidate_scores/"+candidate
        count=bind("wp1",[p+"/correct",p+"/total"],"fraction","wp1_"+candidate+"_correct")
        accuracy=bind("wp1",p+"/accuracy","percent","wp1_"+candidate+"_accuracy_pct")
        row("discovery_scores",candidate,[metric_tex[candidate],count,accuracy,
            bind("wp1",p+"/spearman/pooled","sig3"),bind("wp1",p+"/spearman/QR33","sig3"),bind("wp1",p+"/spearman/QR4","sig3")])
    table_end()
    namedfacts["wp1_selected_metric"]=r"$c=W/(H+1)$"
    namedfact_sources["wp1_selected_metric"]=dict(source_path=PATHS["wp1"],source_sha256=seals["wp1"]["sha256"],JSON_pointer="/selected_metric",raw_value=wp1["selected_metric"])
    note(r"Correct classifications are in-sample descriptive counts, not held-out prediction accuracy. The tie rule selects the simpler index $c$, which contains no parameter count.")
    table_start("v9-discovery-cutpoints","First discovery cutpoints and all-draw envelopes.","p{33mm}rrr",
        r"Regression & First $r^\star$ & All-draw envelope & Multiple-root draws/total")
    for method in ("QR33","QR4"):
        p="/methods/"+method
        root_fact=bind("wp1",p+"/point/r_star","sig4","wp1_"+method+"_rstar")
        interval=bind("wp1",[p+"/intervals/all_draw_envelope/lower",p+"/intervals/all_draw_envelope/upper"],"interval4","wp1_"+method+"_envelope")
        multiple=bind("wp1",[p+"/multiple_crossing_draws",p+"/intervals/draw_count"],"fraction","wp1_"+method+"_multiple_draws")
        row("discovery_cutpoints",method,[MODEL[method],root_fact,interval,multiple])
    table_end()
    note(r"These post hoc envelopes condition on the chosen index and fixed discovery grid. The four-predictor discovery curve has more than one downward crossing; a first cutpoint does not imply sustained gains at every longer history.")
    table_start("v9-confirmation-pooled","Pre-run simulation criteria, with every fixed denominator.","lrrrrl",
        r"Criterion & Successes/total & Observed (\%) & Required (\%) & Missing & Result")
    for criterion in ("P1","P2","P3"):
        p="/"+criterion
        count=bind("wp2",[p+"/successes",p+"/denominator"],"fraction","wp2_"+criterion+"_count")
        observed=bind("wp2",p+"/observed_fraction","percent","wp2_"+criterion+"_observed_pct")
        required=bind("wp2",p+"/minimum_fraction","percent","wp2_"+criterion+"_required_pct")
        missing=bind("wp2",p+"/missing","integer","wp2_"+criterion+"_missing")
        status=bind("wp2",p+"/status","status","wp2_"+criterion+"_result")
        row("confirmation_pooled",criterion,[criterion,count,observed,required,missing,status])
    table_end()
    note(r"P1 checks strict losses below each method's low cutpoint region; P2 checks strict wins above its high region. P3 requires the four-predictor loss change to be no larger in every same-$c$ paired cell. P1 and P2 meet their pooled criteria; P3 does not meet its universal criterion.")
    table_start("v9-confirmation-subgroups","Method and data-generating-process breakdowns.","p{38mm}rlrl",
        r"Group & P1 successes/total & P1 & P2 successes/total & P2")
    groups=[("by_method","QR33",MODEL["QR33"]),("by_method","QR4",MODEL["QR4"])]
    groups.extend(("by_DGP",key,DGP[key]) for key in ("student_t5","regime_3to1","compound_poisson"))
    for number,(kind,key,label) in enumerate(groups):
        p="/"+kind+"/"+key
        row("confirmation_subgroups",number,[label,
            bind("wp2",[p+"/P1/successes",p+"/P1/denominator"],"fraction","wp2_"+key+"_P1_count"),
            bind("wp2",p+"/P1/status","status"),
            bind("wp2",[p+"/P2/successes",p+"/P2/denominator"],"fraction","wp2_"+key+"_P2_count"),
            bind("wp2",p+"/P2/status","status")])
    table_end()
    tex.extend([r"\clearpage",r"\subsection*{Adverse inequalities and retrospective financial cutpoints}"])
    failure_count=bind("wp2","/P3/pairs","false_count","wp2_P3_failed_pairs")
    note("The universal P3 prediction fails in "+failure_count["tex_token"]+r" paired cells. Every failed inequality is shown below; successes and ties remain in the complete fixed denominator.")
    failure_count["table_location"]=dict(note_token=failure_count["tex_token"],section="P3 adverse cases")
    table_start("v9-confirmation-failures","All failed simplification inequalities.","p{30mm}rrr rr",
        r"Process & $\phi$ & $W$ & $H$ & Original $\Delta$ (\%) & Four-predictor $\Delta$ (\%)")
    failed_ids=[i for i,pair in enumerate(wp2["P3"]["pairs"]) if pair["outcome"] is False]
    for i in failed_ids:
        pair=wp2["P3"]["pairs"][i];p="/P3/pairs/"+str(i)
        match=next(j for j,x in enumerate(summary) if all(x[k]==pair[k] for k in ("dgp","phi_index","window","horizon")) and x["method"]=="QR33")
        row("confirmation_failures",i,[DGP[pair["dgp"]],bind("wp2_summary","/"+str(match)+"/phi","sig3"),
            bind("wp2",p+"/window","integer"),bind("wp2",p+"/horizon","integer"),
            bind("wp2",p+"/QR33_delta","loss"),bind("wp2",p+"/QR4_delta","loss")])
    table_end()
    table_start("v9-financial-cutpoints","All fixed financial cutpoint predictions.","rp{32mm}p{29mm}p{23mm}p{27mm}",
        r"$H$ & Regression & Predicted $W$ interval & Identified first $W$ & Result")
    for i,curve in enumerate(curves):
        p="/"+str(i);method=curve["method"];h=curve["horizon"]
        row("financial_cutpoints",i,[bind("curves",p+"/horizon","integer"),MODEL[method],
            bind("curves",[p+"/prediction_range/0",p+"/prediction_range/1"],"interval4","wp3_"+method+"_H"+str(h)+"_predicted_interval"),
            bind("curves",[p+"/first_crossing",p+"/observed_left_censoring"],"root","wp3_"+method+"_H"+str(h)+"_first_cutpoint"),
            bind("curves",p+"/prediction_status","curve_status","wp3_"+method+"_H"+str(h)+"_prediction_result")])
    table_end()
    left_index=next(i for i,x in enumerate(curves) if x["method"]=="QR4" and x["horizon"]==6)
    first_w=bind("curves","/"+str(left_index)+"/windows/0","integer","wp3_QR4_H6_left_censoring_W")
    later=bind("curves","/"+str(left_index)+"/conditional_crossings/0","sig4","wp3_QR4_H6_later_conditional_crossing")
    note("For the shorter-horizon four-predictor curve, the first observed history "+first_w["tex_token"]+
        " already has a nonpositive loss change. Its later conditional crossing "+later["tex_token"]+
        r" does not identify the first cutpoint. Compatibility under left censoring is not confirmation. Thus the all-four financial prediction is not confirmed.")
    first_w["table_location"]=dict(note_token=first_w["tex_token"],section="financial left censoring")
    later["table_location"]=dict(note_token=later["tex_token"],section="financial left censoring")
    for name,style in (("wp3_identified_first_cutpoints","identified_count"),("wp3_consistent_identified_cutpoints","consistent_count")):
        bind("curves","",style,name)
    namedfacts["wp3_all_four_prediction_result"]="not confirmed"
    namedfact_sources["wp3_all_four_prediction_result"]=dict(source_path=PATHS["curves"],source_sha256=seals["curves"]["sha256"],JSON_pointer="",rule="all four statuses must be FIRST_CUTPOINT_CONSISTENT",raw_statuses=[x["prediction_status"] for x in curves])
    tex.extend([r"\clearpage",r"\subsection*{Complete retrospective FX learning-curve contrasts}"])
    common_n=bind("contrasts","/0/n","integer","wp3_common_evaluation_n")
    assert all(x["n"]==contrasts[0]["n"] for x in contrasts)
    note("Each complete contrast uses the same "+common_n["tex_token"]+
        r" evaluation issues and a matched historical rule at the same $W$ and update schedule. The period was previously inspected. The fixed HAC bandwidth and normal-reference DM diagnostic remain post-result and nominal.")
    common_n["table_location"]=dict(note_token=common_n["tex_token"],section="financial evaluation count")
    table_start("v9-financial-full","Every prescribed financial history, horizon and method.","rrp{33mm}rrrr",
        r"$H$ & $W$ & Regression & Loss change (\%) & Model breaches & F breaches & \shortstack{Nominal\\DM $p$}")
    ordered=sorted(enumerate(contrasts),key=lambda item:(item[1]["horizon"],item[1]["window"],0 if item[1]["method"]=="QR33" else 1))
    for i,item in ordered:
        p="/"+str(i);method=item["method"];h=item["horizon"];w=item["window"]
        loss=bind("contrasts",p+"/relative_loss_percent","loss","wp3_"+method+"_H"+str(h)+"_W"+str(w)+"_loss_pct")
        row("financial_full",i,[bind("contrasts",p+"/horizon","integer"),bind("contrasts",p+"/window","integer"),MODEL[method],loss,
            bind("contrasts",p+"/model_breaches","integer"),bind("contrasts",p+"/reference_breaches","integer"),
            bind("contrasts",p+"/dm/dm_p","pvalue")])
    table_end()
    note(r"Loss change is $100(\overline L_{\mathrm{model}}-\overline L_F)/\overline L_F$ and is displayed to one decimal place; no source value is rounded before analysis. Positive changes and every longer-history reversal remain visible. DM uses the fixed Bartlett HAC convention and a two-sided normal reference. A displayed $0^{u}$, if present, is a floating-point zero, not an exact probability.")
    tex.extend([r"\endgroup",""])
    # Main-text aliases remain literal TeX-ready strings, linked to source IDs.
    for key,value in list(namedfacts.items()):
        if key.endswith("_pct"):
            composite_fact(key+"_tex",[next(x for x in bindings if x["id"]==namedfact_sources[key])],value+r"\%")
    namedfacts["overall_mechanism_assessment"]="partly supported"
    namedfact_sources["overall_mechanism_assessment"]=dict(source_paths=[PATHS["wp2"],PATHS["curves"]],
        rule="P1/P2 pooled criterion met; universal P3 not met; one financial first-cutpoint prediction left-censored")
    assert wp2["primary_status"]=="SUPPORT" and wp2["P3"]["status"]=="NOT_SUPPORT"
    assert sum(x["prediction_status"]=="FIRST_CUTPOINT_CONSISTENT" for x in curves)==3
    for record in seals.values():assert sha(root/record["path"])==record["sha256"]
    document="\n".join(tex)
    payload=dict(schema="v9-wp5-literal-number-bindings-1",sources=seals,
        format_policy=dict(percentages="one decimal place",cutpoints_and_intervals="four significant digits",
            correlations_and_p_values="three significant digits",counts="exact integers",
            p_zero="display source floating-point zero explicitly; no invented probability bound"),
        generated_tex="submission-jof/generated/v9-evidence-tables.tex",
        generated_tex_sha256=hashlib.sha256(document.encode()).hexdigest(),tables_intended_pages=3,
        table_rows=rows,bindings=bindings,namedfacts=namedfacts,namedfact_sources=namedfact_sources,
        negative_result_preservation=dict(all_P3_failed_pairs=len(failed_ids),P3_status=wp2["P3"]["status"],
            all_four_financial_prediction="not confirmed",all20_financial_rows=len(contrasts),
            source_loss_signs_unmodified=True,raw_source_values_unrounded=True),
        scope=dict(new_models=0,new_forecasts=0,new_statistical_tests=0,only_existing_accepted_JSON=True))
    return document,payload

def main():
    if sys.flags.optimize:
        raise RuntimeError("saved-field checks require non-optimized Python; unset PYTHONOPTIMIZE and omit -O")
    parser=argparse.ArgumentParser();parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument("--check",action="store_true");args=parser.parse_args();root=args.root.resolve()
    text,bindings=build(root);tex=root/"submission-jof/generated/v9-evidence-tables.tex";numbers=root/"notes/revision-v9/wp6-new-number-bindings.json"
    if args.check:
        if tex.read_text()!=text:raise ValueError("saved evidence TeX MISMATCH")
        if json.loads(numbers.read_text())!=bindings:raise ValueError("saved evidence bindings MISMATCH")
    else:
        if tex.exists() or numbers.exists():raise FileExistsError("refuse to overwrite generated evidence; use --check")
        with tex.open("x") as f:f.write(text)
        with numbers.open("x") as f:json.dump(bindings,f,indent=2,allow_nan=False);f.write("\n")
    print(json.dumps(dict(status="PASS",mode="readback" if args.check else "generated",bindings=len(bindings["bindings"]),
        namedfacts=len(bindings["namedfacts"]),tex_bytes=tex.stat().st_size,tex_sha256=sha(tex),
        bindings_bytes=numbers.stat().st_size,bindings_sha256=sha(numbers),
        table_row_counts=dict(Counter(x["row_tag"].split(":")[0] for x in bindings["table_rows"])),
        main_or_supplement_modified=False,new_statistics_run=0),sort_keys=True))

if __name__=="__main__":main()
