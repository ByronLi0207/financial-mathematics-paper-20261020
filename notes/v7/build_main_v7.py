"""Typeset the v7 main text from authored prose and saved evidence fields.

Formatting and document assembly only: no forecast, statistical test or data
acquisition. Every substituted result token is linked to its exact S2 row.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ROWS = {row["id"]: row for file in (HERE / "evidence-parts").glob("*.json")
        for row in json.loads(file.read_text())}
BINDINGS = []


def substitute(text, location):
    def value(match):
        key, form = match.group(1), match.group(2) or ""
        row = ROWS[key]
        raw = row["value"]
        if form == "set":
            rendered = r"\{" + ",".join(format(float(v), "g") for v in raw) + r"\}"
        elif form:
            rendered = format(float(raw), form)
        else:
            rendered = str(raw)
        BINDINGS.append(dict(location=location, id=key, source=row["source"],
                             raw_value=raw, format=form, rendered=rendered))
        return rendered
    return re.sub(r"@@([A-Z0-9_]+)(?:\|([^@]*))?@@", value, text)


def table(caption, label, widths, headers, rows, note=""):
    col = "".join(r">{\raggedright\arraybackslash}p{" + str(w) + "cm}" for w in widths)
    return (r"\begin{table}[htbp]\centering\small" + "\n" +
            r"\caption{" + caption + r"}\label{" + label + "}\n" +
            r"\begin{tabular}{" + col + r"}\toprule" + "\n" +
            " & ".join(headers) + r"\\\midrule" + "\n" +
            "\n".join(" & ".join(row) + r"\\" for row in rows) + "\n" +
            r"\bottomrule\end{tabular}" + "\n" +
            (r"\par\smallskip\begin{minipage}{.98\linewidth}\footnotesize " + note + r"\end{minipage}" if note else "") +
            "\n" + r"\end{table}" + "\n")


def tables():
    lit = table(
        "Closest literature and the present forecasting task. n.r. marks a dimension unreported in the consulted task or passage. The distinction is a common peak-position target and its validation design.",
        "tab:literature", [2.4,2.1,1.5,1.6,1.6,1.7,1.7],
        ["Study", "Response", "Data unit", "Peak floor", "Label timing", "Evaluation", "Source scope"], [
            [r"\citealp{wisniewski2020}", "Signed endpoint interval", "One FX market maker", "n.r.", "Ordered train/calibrate/test", "Scores and hit tests", "One source family"],
            [r"\citealp{boudoukh2004}", "Worst portfolio return", "Stylized fixed portfolio", "Different initial-value anchor", "Analytic diffusion", "Tail ratios and monitoring", "Parameter cases"],
            [r"\citealp{hoogen2017}", "Cumulative payment-deficit peak", "Confidential bank payments", "Absolute-position floor n.r.", "Path simulation", "EVT methodology; results partly confidential", "Bank payment task"],
            [r"\citealp{duffie2023}", "Capacity, illiquidity, PnL quantiles", "Dealer/market sources", "n.r.", "Expanding PnL fits", "Capacity and PnL forecasts", "Several sources"],
            [r"\citealp{engle2004}", "Return quantile", "Asset returns", "n.r.", "Lagged predictors", "Quantile scores and DQ", "Several returns"],
            [r"\citealp{ehm2016}", "Quantile/expectile comparison", "Multiple forecast examples", "n.r.", "Original example designs", "Elementary-score curves", "Multiple tasks"],
            [r"\citealp{meinshausen2006}", "Conditional response quantile", "Regression examples", "n.r.", "Original regression splits", "Conditional distributions", "Several datasets"],
            ["This study", "Sampled absolute-position peak", "One FX record; weekly totals", "Observed current magnitude", "Completed forward labels", "Scores, breaches, coherence", "Related aggregate tasks"],
        ], "The institutional payment-thesis reading is partial; n.r. is not evidence of absence. The earlier FX work and this paper share a source family, without verified input-byte identity.")
    for key,study in (("wisniewski2020",r"Wisniewski\\et al. (2020)"),
                      ("boudoukh2004",r"Boudoukh\\et al. (2004)"),
                      ("hoogen2017",r"van den\\Hoogen (2017)"),
                      ("duffie2023",r"Duffie\\et al. (2023)"),
                      ("engle2004",r"Engle and\\Manganelli\\(2004)"),
                      ("ehm2016",r"Ehm et al.\\(2016)"),
                      ("meinshausen2006",r"Meinshausen\\(2006)")):
        lit=lit.replace(r"\citealp{"+key+"}",r"\shortstack[l]{"+study+"}")
    lit=lit.replace(r"\centering\small",r"\centering\footnotesize\uchyph=1\hyphenation{con-fi-den-tial con-di-tion-al re-gres-sion com-plet-ed el-e-men-ta-ry ex-pand-ing}")
    lit=lit.replace("/",r"/\allowbreak ")
    lit=lit.replace("Confidential",r"Con\-fi\-den\-tial").replace("Elementary-score",r"El\-e\-men\-tary-score")
    methods = table(
        "Forecast definitions and executed menus. Codes occur here to connect with the result files. Matched histories and update schedules make the reference explicit.",
        "tab:methods", [2.9,6.0,5.3], ["Method / code", "Forecast definition", "Executed menu / setting"], [
            ["Historical headroom (F)", r"Current floor plus a quantile of completed peak headrooms", r"FX histories @@META_FX_HOURLY_WINDOWS|set@@; weekly @@META_NYFED_WEEKLY_WINDOWS|set@@"],
            ["Translated path (S)", "Translate completed signed paths to the current position before taking their peaks", "Same completed-label pools; fixed-window and rolling-window controls"],
            ["Historical peak (K)", "Historical absolute-peak quantile projected to the current floor", "Same histories and update controls"],
            ["Quantile regression (QR)", "Training-scaled headroom regression with ridge slopes and an unpenalized intercept", r"Original penalties $@@META_QR_PENALTIES|set@@$; expanded menu in Supplement"],
            ["Local quantiles (KNN)", "Neighbor headroom quantile, with a separate increment-scale variant", "Training-only transforms and fixed neighbor menus; Supplement"],
            ["Parsimonious regression (QR4)", "Current signed/magnitude positions and short/long increment RMS", "Separate five-point penalty menu; common-menu comparison in Supplement"],
            ["Endpoint plug-in (L)", "Floor plus a high absolute-displacement endpoint quantile", r"Proposition~\ref{prop:levy}; empirical plug-in evaluated separately"],
            ["Further benchmarks", "Autoregressive replay; filtered paths; peak-tail fit; quantile forest", "Existing bounded specifications, complete failures included in Supplement"],
            ["Coverage and combinations", "Delayed projected ACI-style wrappers; headroom SAV; fixed forecast combinations", "Original-source wrapper/SAV inventory and broader combination inventory are separate"],
        ], r"Training histories count completed labels. Fixed-window models refit every @@META_FX_HOURLY_REFIT_STEP@@ FX records or @@META_NYFED_WEEKLY_REFIT_STEP@@ weekly records. Quantile and normalization conventions are detailed in the Supplement; this table does not expand any executed menu.")
    fx = table(
        "Long-history short-horizon FX regression under two references and periods. Negative percentages favor regression. Matched gains recur while the rolling-reference direction changes.",
        "tab:fx", [2.6,4.4,2.5,1.5,3.2], ["Period / procedure", "Reference", "Loss change (\\%)", "Issues", "Strict breaches (regression / reference)"], [
            ["Later / original primary", "Shorter-history rolling headroom", "@@FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|.2f@@", "@@FX_LATE_PRIMARY_H6_ORIGIN_COUNT@@", "@@FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_LEFT@@ / @@FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_RIGHT@@"],
            ["Later / matched", "Same-history fixed-window headroom", "@@FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT|.2f@@", "@@FX_LATE_MATCHED_H6_ORIGIN_COUNT@@", "@@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT@@ / @@FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT@@"],
            ["Earlier / original structure", "Shorter-history rolling headroom", "@@FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT|+.2f@@", "@@FX_EARLY_PRIMARY_H6_N@@", "See complete earlier-period tables"],
            ["Earlier / matched", "Same-history fixed-window headroom", "@@FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT|.2f@@", "@@FX_EARLY_MATCHED_H6_N@@", "@@FX_EARLY_MATCHED_R0_STRICT_BREACH_COUNT@@ / @@FX_EARLY_MATCHED_F_STRICT_BREACH_COUNT@@"],
            ["Later / coverage-wrapped", "Same-history wrapped headroom", "@@FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT|.2f@@", "@@FX_ACI_H6_W2880_N@@", "@@FX_ACI_H6_W2880_QR_HITS@@ / @@FX_ACI_H6_W2880_F_HITS@@"],
        ], r"Regression uses history @@META_FX_HOURLY_PRIMARY_CONTRAST_WINDOW@@ and horizon @@META_FX_HOURLY_PRIMARY_CONTRAST_HORIZON@@; the original rolling reference uses @@META_FX_HOURLY_PRIMARY_CONTRAST_REFERENCE_WINDOW@@. The earlier matched comparison is the original three-penalty regression, not the later one-standard-error selection rule. The wrapper comparison is a separate finite projected delayed ACI-style exercise.")
    weekly = table(
        "Weekly evidence across distinct, explicitly identified comparison sets. Counts refer to related tasks rather than independent dealers. Stronger regularization narrows losses while leaving substantial failures.",
        "tab:weekly", [4.3,4.7,2.7,2.5], ["Comparison set", "Procedure", "Loss change / median (\\%)", "Higher-loss cells"], [
            ["Original Treasury-bill primary", "Original regression, long history", "@@PANEL_BILL_QR_H6_W260_LOSS_PERCENT|+.2f@@", "Original primary"],
            ["Earlier Treasury-bill analogue", "Short-history structural analogue", "@@PANEL_R6_BILL_W52_ANALOGUE_LOSS_PERCENT|+.2f@@", "Different history"],
            ["Additional panel", "Original full regression", "@@PANEL_E5_QR33_MEDIAN|+.2f@@", "@@PANEL_E5_QR33_LOSSES@@ / @@PANEL_E5_PLANNED@@"],
            ["Additional panel", "Four-predictor regression", "@@PANEL_E5_QR4_MEDIAN|+.2f@@", "@@PANEL_E5_QR4_LOSSES@@ / @@PANEL_E5_PLANNED@@"],
            ["Additional panel", "Full regression, expanded penalties", "@@PANEL_E5_QR33_EXPANDED_MEDIAN|+.2f@@", "@@PANEL_E5_QR33_EXPANDED_LOSSES@@ / @@PANEL_E5_PLANNED@@"],
            ["Additional panel", "Ordinary empirical headroom quantile", "@@PANEL_E5_ORDINARY_I_MEDIAN|+.2f@@", "@@PANEL_E5_ORDINARY_I_LOSSES@@ / @@PANEL_E5_PLANNED@@"],
            ["Earlier weekly groups", "Validation-minimum expanded rule", "@@PANEL_R6_R0_RETRO_MEDIAN|+.2f@@", "@@PANEL_R6_R0_RETRO_COMPLETE@@ groups"],
            ["Earlier weekly groups", "One-standard-error rule", "@@PANEL_R6_R2_RETRO_MEDIAN|+.2f@@", "@@PANEL_R6_S1_COMPLETE@@ groups"],
        ], r"The original bill primary has @@PANEL_BILL_QR_H6_W260_QR_HITS@@ versus @@PANEL_BILL_QR_H6_W260_F_HITS@@ strict breaches among @@PANEL_BILL_QR_H6_W260_N@@ issues. Earlier short-history bill results are a structural analogue, not an exact replay of that primary. The one-standard-error worst excess is +@@PANEL_R6_R2_RETRO_WORST|.2f@@\%; all its prewritten success criteria remain unmet. Full panel and selection tables are linked from the Supplement and EXTENDED\_RESULTS.md.")
    inference = table(
        "Accuracy and hit diagnostics for explicitly named reports. Panel A reports paired working-reference tests; Panel B uses the fixed nonoverlap grid for hit tests. A better average score does not imply fewer breaches.",
        "tab:diagnostics", [4.3,2.1,2.1,5.7], ["Panel A: paired contrast", "DM p", "HLN p", "Named adjustment / p"], [
            ["FX original primary", "@@FX_DM_PRIMARY_H6_DM_P|.3g@@", "@@FX_DM_PRIMARY_H6_HLN_P|.3g@@", "Two-primary Bonferroni: @@FX_DM_PRIMARY_H6_PRIMARY_BONFERRONI_P|.3g@@"],
            ["FX matched history", "@@FX_DM_MATCHED_H6_DM_P|.3g@@", "@@FX_DM_MATCHED_H6_HLN_P|.3g@@", "Original matched Holm family: @@FX_DM_MATCHED_H6_ARCHIVED72_HOLM_P|.3g@@"],
            ["Treasury original primary", "@@PANEL_BILL_PRIMARY_DM_P|.3g@@", "@@PANEL_BILL_PRIMARY_HLN_P|.3g@@", "Original matched Holm family: @@PANEL_BILL_PRIMARY_HOLM_P|.3g@@"],
        ], r"Original matched Holm uses @@PANEL_BILL_PRIMARY_FAMILY_N@@ contrasts. The later regrouped matched family is separate; earlier-period writing-stage HAC comparisons have neither a new HLN field nor a new family adjustment.")
    inference=inference.replace(r"\end{table}","")
    inference += r"\par\medskip\begin{center}\small" + "\n" + r"\begin{tabular}{p{4.0cm}rrrr}\toprule" + "\n" + r"Panel B: report & Grid hits & Grid issues & Kupiec p & Christoffersen CC p\\\midrule" + "\n"
    for label, prefix in [("FX regression", "FX_COVERAGE_QR"), ("FX original rolling reference", "FX_COVERAGE_PRIMARY_F"), ("FX matched fixed reference", "FX_COVERAGE_MATCHED_F")]:
        inference += label + " & @@"+prefix+"_HITS@@ & @@"+prefix+"_N@@ & @@"+prefix+"_POF_P|.3g@@ & @@"+prefix+"_CC_P|.3g@@"+r"\\"+"\n"
    for label, prefix in [("Treasury regression", "COVERAGE_BILL_QR"), ("Treasury historical reference", "COVERAGE_BILL_FROZEN_F")]:
        inference += label + " & @@"+prefix+"_HITS@@ & @@"+prefix+"_N@@ & @@"+prefix+"_POF_P|.3g@@ & @@"+prefix+"_CC_P|.3g@@"+r"\\"+"\n"
    inference += r"\bottomrule\end{tabular}\end{center}"+"\n"+r"{\footnotesize Hit tests use the full fixed nonoverlap grid; the conditional-coverage likelihood conditions on its initial hit. Equality to the nominal tail rate is the stated diagnostic null, distinct from the population upper-quantile inequality. The grid does not create independence.}"+"\n"+r"\end{table}"+"\n"
    decision = table(
        "Frequency, history and horizon as a validation decision map. Each entry describes executed comparisons rather than a causal frequency effect. Keep the historical rule until the named advantage survives joint validation.",
        "tab:map", [3.3,3.7,4.0,3.2], ["Frequency / history", "Horizon", "Evidence", "Validation action"], [
            ["Hourly / longer history", "Short", "Repeated matched score gains; separate wrapper check", "Compare named control and breaches"],
            ["Hourly / shorter history", "Short", "Small score gain with more breaches", "Require stable joint performance"],
            ["Hourly / either history", "Longer", "Losses or weaker gains; coherence and preference sensitivity", "Check horizon order and loss preferences"],
            ["Weekly / short or long history", "Short or longer", "Frequent regression losses despite expanded penalties", "Keep historical and parsimonious controls"],
            ["Any source / endpoint bound", "Specified horizon", "Population premises and plug-in behavior differ", "Check absolute displacement and dependence"],
        ])
    return {key: substitute(text, "table:"+key) for key, text in
            (("literature",lit),("methods",methods),("fx",fx),("weekly",weekly),("diagnostics",inference),("map",decision))}


def figure(filename, label, caption, width=".94"):
    return (r"\begin{figure}[htbp]\centering\includegraphics[width="+width+r"\linewidth]{figures/"+filename+"}\n"+
            r"\caption{"+caption+r"}\label{"+label+"}\n"+r"\end{figure}"+"\n")


def provisional_references(keys):
    """Keep existing reference text for pagination; S7 verifies final metadata.

    The earlier supervisor manuscript already uses native thebibliography.
    This avoids requiring an uncached BibTeX style or downloading software.
    """
    verified=HERE/"references-v7.tex"
    if verified.exists():
        text=verified.read_text()
        actual=set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}",text))
        if actual!=keys:raise ValueError("verified reference set differs from current citations")
        return text
    source = (ROOT/"submission-jof/references.bib").read_text()
    chunks = re.split(r"(?=^@)",source,flags=re.M)
    entries = {}
    for chunk in chunks:
        match = re.match(r"@\w+\{([^,]+),",chunk)
        if not match:continue
        fields = {}
        for found in re.finditer(r"^\s*(\w+)\s*=\s*\{",chunk,flags=re.M):
            start=found.end();level=1;end=start
            while end<len(chunk) and level:
                if chunk[end]=="{" and (end==0 or chunk[end-1]!="\\"):level+=1
                elif chunk[end]=="}" and (end==0 or chunk[end-1]!="\\"):level-=1
                end+=1
            fields[found.group(1)]=chunk[start:end-1]
        entries[match.group(1)]=fields
    old=(ROOT/"manuscript/supervisor-revision/references.tex").read_text()
    labels={key:label for label,key in re.findall(r"\\bibitem\[([^\]]+)\]\{([^}]+)\}",old)}
    items=[]
    for key in sorted(keys):
        fields=entries[key];body=fields.get("note")
        if body is None:
            body=fields.get("author","")+" ("+fields.get("year","")+"). "+fields.get("title","")+". "+fields.get("booktitle","")+"."
        year=fields.get("year")
        if not year:
            found=re.search(r"\((\d{4})\)",body);year=found.group(1) if found else "n.d."
        if key in labels and key!="dataset":label=labels[key]
        else:
            author=fields.get("author",body.split("(",1)[0]).strip().split(",",1)[0]
            label=author+"("+year+")"
        for a,b in (("’","'"),("–","--"),("—","---")):body=body.replace(a,b);label=label.replace(a,b)
        items.append(r"\bibitem["+label+r"]{"+key+"} "+body+"\n")
    return r"\begin{thebibliography}{99}"+"\n"+"\n".join(items)+r"\end{thebibliography}"+"\n"


def main():
    data = json.loads((HERE / "main-v7-sections.json").read_text())
    tab = tables()
    contributions = json.loads((HERE / "contributions.json").read_text())
    # Existing S4 passages change evidence-location text only to the final S5 order.
    contribution_text = []
    for item in contributions:
        sentences = list(item["sentences"])
        if item["id"] == "C1":
            sentences[-1] = r"Section~\ref{sec:target} provides the definitions, propositions and crossing diagnostic, with proofs and simulation qualifications in the Supplement."
        elif item["id"] == "C2":
            sentences[-1] = r"Section~\ref{sec:results} reports the gains and failures, and Table~\ref{tab:map} organizes the frequency--history--horizon decision map."
        else:
            sentences[-1] = r"Sections~\ref{sec:evaluation}--\ref{sec:implications} support a four-part checklist: use matured labels, separate history and model changes, report scores with breaches, and check stability across periods and related series."
        contribution_text.append(r"\textbf{"+item["id"]+".} "+" ".join(sentences))
    example = figure("v7-endpoint-peak-example.pdf", "fig:example", "A selected Treasury-bill path whose endpoint returns within the historical report after an intervening breach. The rule chooses the earliest eligible original evaluation window. Endpoint containment can conceal a peak breach.")
    murphyfx = figure("v7-murphy-fx_hourly.pdf", "fig:murphyfx", "Elementary quantile-score curves for the original short-horizon FX primary. The full-breakpoint calculation finds crossings; the graph is a display of saved scores. Average pinball superiority does not imply dominance across elementary scores.")
    murphybill = figure("v7-murphy-nyfed_weekly.pdf", "fig:murphybill", "Elementary quantile-score curves for the original Treasury-bill primary. The saved full-breakpoint comparison also crosses. A single average-score ordering leaves other consistent-score preferences unresolved.")
    parts = [r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{iftex}
\ifPDFTeX\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\fi
\usepackage{amsmath,amssymb,graphicx,booktabs,array}
\usepackage[authoryear,round]{natbib}
\usepackage{caption,placeins}
\usepackage[unicode,breaklinks=true,hidelinks]{hyperref}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}\setlength{\tabcolsep}{3pt}
\clubpenalty=10000\widowpenalty=10000
\captionsetup{font=small,labelfont=bf}
\newcounter{proposition}
\begin{document}
\begin{center}\Large\bfseries """+data["title"]+r"\end{center}"+"\n",
             r"\begin{abstract}"+substitute(data["abstract"],"abstract")+r"\end{abstract}"+"\n"]
    words = {}
    for number, section in enumerate(data["sections"],1):
        label=section["label"]
        parts.append(r"\section{"+section["title"]+r"}\label{"+label+"}\n")
        prose=[]; paragraph_number=0; result_stage=0
        for block in section["blocks"]:
            kind=block["kind"]
            if kind=="p":
                text=substitute(block["tex"],label+":"+str(paragraph_number))
                text=re.sub(r"\\paragraph\{Proposition [12] \(([^}]+)\)\.\}",
                            lambda m:r"\refstepcounter{proposition}\noindent\textbf{Proposition~\theproposition ("+m.group(1)+").}",text)
                parts.append(text+"\n\n");prose.append(text);paragraph_number+=1
                if number==1 and paragraph_number==2:parts.append(example)
            elif kind=="eq":parts.append("\\[\n"+substitute(block["tex"],label+":equation")+"\n\\]\n")
            elif kind=="subsection":
                if number==7 and result_stage==1:parts.append(tab["fx"])
                if number==7 and result_stage==2:parts.append(tab["weekly"])
                parts.append(r"\subsection{"+block["tex"]+"}\n")
                if number==7:result_stage+=1
            elif kind=="insert" and block["key"]=="contributions":
                parts.append("\n\n".join(contribution_text)+"\n\n");prose.extend(contribution_text)
            else:raise ValueError("unknown main block: "+str(block))
        if number==2:parts.append(tab["literature"])
        if number==5:parts.append(tab["methods"])
        if number==7:parts.extend([tab["diagnostics"],murphyfx,murphybill])
        if number==8:parts.append(tab["map"])
        words[section["title"]]=prose
        parts.append(r"\FloatBarrier"+"\n")
    availability=HERE/"availability-v7.tex"
    parts.append(availability.read_text() if availability.exists() else r"""\section*{Data and code availability}
Data and code access conditions are described in the Online Supplement and repository. Author information, ORCID, funding, competing interests and AI statement: [TO BE COMPLETED BY AUTHOR].
""")
    keys={key.strip() for match in re.findall(r"\\cite(?:p|t|alp)?\{([^}]+)\}","\n".join(parts)) for key in match.split(",")}
    parts.append(provisional_references(keys))
    parts.append(r"\end{document}"+"\n")
    text="\n".join(parts)
    for a,b in (("’","'"),("–","--"),("—","---")):text=text.replace(a,b)
    if "@@" in text:raise ValueError("unresolved evidence token")
    (ROOT/"submission-jof/manuscript.tex").write_text(text)
    (HERE/"main-v7-numeric-bindings.json").write_text(json.dumps(BINDINGS,indent=2,ensure_ascii=False)+"\n")
    (HERE/"main-v7-prose-for-counts.json").write_text(json.dumps(words,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"sections":len(data["sections"]),"main_tables":6,"main_figures":3,"evidence_substitutions":len(BINDINGS),"new_models":0,"new_tests":0},indent=2))


if __name__=="__main__":
    main()
