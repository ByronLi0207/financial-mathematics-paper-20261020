"""Generate a short paper display from saved public F1/F2/F3 scalar JSON.

No private data, fitting, scoring, reaggregation or scientific decisions occur.
Failed full-group tau summaries display NA even when a subset median is saved.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCES = {
    "short": "results/v12/decomposition/short-weekly-summary.json",
    "decomposition": "results/v12/decomposition/predictions.json",
    "validation": "results/v12/validation-length/predictions.json",
    "tau": "results/v12/tau/predictions.json",
    "menu": "results/v12/decomposition/candidates.json",
}
TEX_PATH = "submission-v10/generated/v12-low-frequency.tex"
BINDINGS_PATH = "notes/v12/new-paper-number-bindings.json"


def _at(document, pointer):
    result = document
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        result = result[int(token)] if isinstance(result, list) else result[token]
    return result


class SavedFacts:
    def __init__(self, root):
        self.sources, self.documents, self.bindings = {}, {}, []
        for key, name in SOURCES.items():
            raw = (root / name).read_bytes()
            self.documents[key] = json.loads(raw)
            self.sources[key] = dict(path=name, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))

    def bind(self, name, source, pointer, formatter=str, *, context="body"):
        value = _at(self.documents[source], pointer)
        display = formatter(value)
        self.bindings.append(dict(id=name, source=self.sources[source]["path"],
            sha256=self.sources[source]["sha256"], json_pointer=pointer,
            value=value, display=display, context=context, operation="Copy saved scalar; display formatting only"))
        return display

    def group(self, source, **selector):
        matches = [(i, group) for i, group in enumerate(self.documents[source]["descriptive_groups"])
                   if all(group.get(key) == value for key, value in selector.items())]
        if len(matches) != 1:
            raise ValueError("SAVED_GROUP_NOT_UNIQUE:" + str(selector))
        return matches[0]


def _backup(path):
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        destination = path.with_name(path.name + "." + stamp + ".bak")
        if destination.exists():
            raise FileExistsError(str(destination))
        path.rename(destination)
        return str(destination)
    return None


def _style(paragraphs):
    visible = " ".join(paragraphs)
    visible = re.sub(r"Figure~\\ref\{[^}]+\}", "Figure reference", visible)
    visible = re.sub(r"Table~\\ref\{[^}]+\}", "Table reference", visible)
    words = lambda text: re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|[+-]?\d+(?:\.\d+)?%?", text)
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", visible)
    lengths = [len(words(sentence)) for sentence in sentences]
    return dict(body_word_count=len(words(visible)), sentence_count=len(lengths),
                mean_sentence_words=sum(lengths) / len(lengths),
                maximum_sentence_words=max(lengths),
                sentences_over_40_words=sum(length > 40 for length in lengths))


def build_report(root=ROOT):
    root = Path(root)
    facts = SavedFacts(root)
    b = facts.bind
    pct = lambda value: f"{value:.2f}%"
    primary = facts.documents["decomposition"]
    if primary["D1"]["status"] != "SUPPORTED" or primary["D2"]["status"] != "SUPPORTED":
        raise ValueError("THIS_REPORT_REQUIRES_THE_SAVED_SUPPORTED_F1_SCREENS")
    if any(facts.documents["tau"][name]["status"] != "UNDETERMINED" for name in ("Q1", "Q2")):
        raise ValueError("THIS_REPORT_REQUIRES_THE_SAVED_UNDETERMINED_TAU_SCREENS")
    n = b("short_weekly_planned", "decomposition", "/D1/planned_n")
    d1 = b("gap_positive_count", "decomposition", "/D1/support_n")
    d2 = b("selection_majority_count", "decomposition", "/D2/support_n")
    if b("selection_screen_planned", "decomposition", "/D2/planned_n") != n:
        raise ValueError("DIFFERENT_PRIMARY_DENOMINATORS")
    actual = b("short_actual_median", "short", "/methods/QR33/median_actual_excess_pct", pct)
    selection = b("short_selection_median", "short", "/methods/QR33/median_selection_component_pct", pct)
    gap = b("short_gap_median", "short", "/methods/QR33/median_signal_gap_pct", pct)
    both_fx = b("long_fx_horizon_count", "decomposition", "/D3/planned_n", lambda value: {2: "Both"}[value])
    for horizon in ("6", "24"):
        pointer = "/D3/horizons/" + horizon + "/signal_gap_pct"
        if _at(primary, pointer) >= 0:
            raise ValueError("SAVED_LONG_FX_GAP_IS_NOT_NEGATIVE")
        b("long_fx_gap_H" + horizon, "decomposition", pointer,
          lambda value: "negative", context="body sign statement; raw percent not displayed")
    short_index, _ = facts.group("validation", family="cftc", window=52, validation_n=52, method="QR33")
    long_index, _ = facts.group("validation", family="cftc", window=52, validation_n=156, method="QR33")
    validation_short = b("validation_short_length", "validation", f"/descriptive_groups/{short_index}/validation_n")
    validation_long = b("validation_long_length", "validation", f"/descriptive_groups/{long_index}/validation_n")
    histories, medians, counts = {}, {}, {}
    for window in (52, 260):
        prefix = f"/methods/QR33/by_window/{window}"
        histories[window] = b(f"training_history_{window}", "validation", prefix + "/window")
        medians[window] = [b(f"median_W{window}_V{length}", "validation",
                             prefix + f"/median_relative_loss_by_validation/{length}", pct)
                           for length in (52, 156)]
        counts[window] = [b(f"infinite_W{window}_V{length}", "validation",
                            prefix + f"/known_infinity_count_by_validation/{length}")
                          for length in (52, 156)]
    eligible = b("validation_eligible_contracts", "validation", "/eligible_contract_count")
    tau_groups = facts.documents["tau"]["descriptive_groups"]
    tau_indices = {tau: next(i for i, row in enumerate(tau_groups) if row["tau"] == tau)
                   for tau in (.90, .99)}
    levels = {tau: b(f"tau_{tau}", "tau", f"/descriptive_groups/{tau_indices[tau]}/tau",
                     lambda value: f"{value:.0%}", context="body and table header") for tau in (.90, .99)}
    period_count = b("tau_fx_periods", "tau", "/Q2/denominator", lambda value: {2: "Both"}[value])
    wins = b("tau_cftc_known_wins", "tau", "/Q1/support_count")
    planned = b("tau_cftc_planned_comparisons", "tau", "/Q1/denominator")
    failed = b("tau_cftc_unresolved_comparison", "tau", "/Q1/unknown_count", lambda value: {1: "one"}[value])
    threshold = b("tau_cftc_required_wins", "tau", "/Q1/minimum_support")
    first = next(row for row in facts.documents["menu"] if row["segment"] == "validation" and row["method"] == "QR33")
    declared_menu = [(i, row) for i, row in enumerate(facts.documents["menu"])
                     if (row["cell_id"], row["segment"], row["method"]) ==
                     (first["cell_id"], "validation", "QR33")]
    if [row["penalty"] for _, row in declared_menu] != [.001, .01, .1, 1., 10., "inf"]:
        raise ValueError("SAVED_DECLARED_MENU_CHANGED")
    finite = [(i, row["penalty"]) for i, row in declared_menu if row["penalty"] != "inf"]
    facts.bindings.append(dict(id="finite_menu_cardinality", source=facts.sources["menu"]["path"],
        sha256=facts.sources["menu"]["sha256"], value=len(finite), display="five", context="method definition",
        operands=[dict(json_pointer=f"/{i}/penalty", value=value) for i, value in finite],
        operation="Count fixed declared finite penalty identities only; no losses or outcomes used"))
    paragraphs = [
        "Figure~\\ref{fig:v12-decomposition} splits full regression's actual excess into the selected report's gap from the best finite candidate and that candidate's gap from historical headroom. "
        "The best candidate uses evaluation hindsight over five finite penalties; the ordinary empirical option is excluded. "
        f"For full regression, the finite-menu gap is positive in {d1} of {n} short-history weekly cells; selection exceeds half of positive actual excess in {d2}. "
        "Both criteria hold, so benchmark advantages and selection losses coexist within this menu. "
        f"Separate component medians need not add: actual excess is {actual}, selection {selection}, and the diagnostic gap {gap}.",

        "This retrospective finite oracle is diagnostic, cannot guide deployment, and cannot rule out information in other conditional models. "
        "When validation selects the ordinary empirical limit, it can beat every finite candidate and make the selection component negative. "
        f"{both_fx} long-history FX horizons have a negative finite-menu gap. "
        "Expanded menus also bring the calibrated simulation medians close to their historical reference, leaving the empirical frequency mechanism unidentified.",

        f"Extending validation from {validation_short} to {validation_long} weeks keeps the CFTC evaluation period, training histories, and refitting clock fixed. "
        f"Median excess falls from {medians[52][0]} to {medians[52][1]} with {histories[52]}-week training histories, "
        f"and from {medians[260][0]} to {medians[260][1]} with {histories[260]}-week histories. "
        f"Infinite-penalty selections rise from {counts[52][0]} to {counts[52][1]} of {eligible} contracts, "
        f"and from {counts[260][0]} to {counts[260][1]} of {eligible}, respectively. "
        "These differences between across-contract medians need not match typical paired improvements and do not identify a causal effect. "
        "Four-feature failures remain unavailable in the complete inventory (Supplement Section S36).",

        f"Tail-level sensitivity remains incomplete, as Table~\\ref{{tab:v12-tau}} shows for {levels[.9]} and {levels[.99]} quantiles under matched histories. "
        f"At {levels[.99]}, historical headroom wins {wins} of {planned} CFTC comparisons; {failed} failure leaves the {threshold}-win threshold unresolved. "
        f"{period_count} FX periods remain unavailable at {levels[.99]}, leaving the combined improvement criterion undetermined. "
        "Unavailable planned comparisons are retained, and successful subsets never replace a missing full-group median."
    ]
    style = _style(paragraphs)
    if not 250 <= style["body_word_count"] <= 330 or style["sentences_over_40_words"]:
        raise ValueError("BODY_LENGTH_OR_SENTENCE_LIMIT:" + str(style))
    if not 15 <= style["mean_sentence_words"] <= 20:
        raise ValueError("MEAN_SENTENCE_LENGTH:" + str(style))
    table_rows = []
    selectors = [("CFTC", dict(family="cftc", period="original", window=52)),
                 ("CFTC", dict(family="cftc", period="original", window=260)),
                 ("FX, original period", dict(family="fx", period="original", window=2880)),
                 ("FX, earlier period", dict(family="fx", period="early2015", window=2880)),
                 ("Treasury bills", dict(family="bill", period="original", window=260))]
    for label, selector in selectors:
        values = []
        geometry_index, _ = facts.group("tau", tau=.90, method="QR33", **selector)
        if selector["family"] == "cftc":
            history = b(f"table_history_{geometry_index}", "tau", f"/descriptive_groups/{geometry_index}/window", context="tau table label")
            label += f", {history} weeks"
        for tau in (.90, .99):
            index, group = facts.group("tau", tau=tau, method="QR33", **selector)
            prefix = f"/descriptive_groups/{index}"
            if group["counts"]["usable"] != group["counts"]["planned"]:
                facts.bindings.append(dict(id=f"tau_{index}_unavailable_group", source=facts.sources["tau"]["path"],
                    sha256=facts.sources["tau"]["sha256"], json_pointer=prefix + "/counts",
                    value=group["counts"], display="NA", context="tau table",
                    operation="NA when saved usable count differs from planned count; no successful-subset median displayed"))
                values.append(r"\textsc{NA}")
            else:
                values.append(b(f"tau_{index}_full_group_median", "tau",
                    prefix + "/descriptive_complete_row_median_relative_loss_pct",
                    lambda value: f"{value:+.2f}", context="tau table"))
        table_rows.append(label + " & " + " & ".join(values) + r" \\")
    fx_index, _ = facts.group("tau", tau=.90, method="QR33", family="fx", period="original", window=2880)
    bill_index, _ = facts.group("tau", tau=.90, method="QR33", family="bill", period="original", window=260)
    fx_history = b("table_fx_training_history", "tau", f"/descriptive_groups/{fx_index}/window", lambda value: f"{value:,}", context="tau table note")
    bill_history = b("table_bill_training_history", "tau", f"/descriptive_groups/{bill_index}/window", context="tau table note")
    def tex(text):
        return text.replace("%", r"\%")
    content = [
        "% Display-only generated file; exact saved-number bindings are in notes/v12/new-paper-number-bindings.json.",
        r"\subsection{Why does regression lose at low frequency?}\label{sec:v12-low-frequency}",
        tex(paragraphs[0]), "", tex(paragraphs[1]), "",
        r"\begin{figure}[htbp]\centering",
        r"\includegraphics[width=.98\linewidth,height=2.75in,keepaspectratio]{figures/v12-decomposition.pdf}",
        r"\caption{Signed decomposition of regression excess loss against matched historical headroom, with selection in blue, the finite-menu diagnostic gap in orange, and actual excess as black dots. Crosses retain unavailable comparisons; the text focuses on short-history weekly cells while all planned comparisons remain plotted.}\label{fig:v12-decomposition}",
        r"\end{figure}", "", tex(paragraphs[2]), "", tex(paragraphs[3]), "",
        r"\begin{table}[htbp]\centering\small",
        r"\caption{Full-regression relative excess loss (\%) at alternative quantile levels. Positive values favor matched historical headroom; NA retains any failed required comparison.}\label{tab:v12-tau}",
        r"\begin{tabular}{lrr}\toprule",
        "Source / training history & " + tex(levels[.9]) + " & " + tex(levels[.99]) + r" \\\midrule",
        *table_rows, r"\bottomrule\end{tabular}",
        r"\par\vspace{2pt}\begin{minipage}{.95\linewidth}\footnotesize",
        f"Contract rows report full-group medians. FX uses {fx_history}-hour training histories; Treasury uses {bill_history} weeks. Successful subsets never replace a required full group.",
        r"\end{minipage}\end{table}", ""
    ]
    text = "\n".join(content)
    if re.search(r"\b(?:QR33|QR4)\b", text):
        raise ValueError("INTERNAL_MODEL_NAME_IN_PAPER")
    for criterion in ("Q1", "Q2"):
        facts.bindings.append(dict(id=criterion + "_unassessable", source=facts.sources["tau"]["path"],
            sha256=facts.sources["tau"]["sha256"], json_pointer="/" + criterion + "/status",
            value=facts.documents["tau"][criterion]["status"], display="undetermined", context="body"))
    for criterion in ("D1", "D2"):
        facts.bindings.append(dict(id=criterion + "_supported", source=facts.sources["decomposition"]["path"],
            sha256=facts.sources["decomposition"]["sha256"], json_pointer="/" + criterion + "/status",
            value=primary[criterion]["status"], display="Both criteria hold", context="body"))
    facts.bindings.append(dict(id="four_feature_failure_inventory", source=facts.sources["validation"]["path"],
        sha256=facts.sources["validation"]["sha256"], json_pointer="/counts/failed",
        value=facts.documents["validation"]["counts"]["failed"],
        display="Four-feature failures remain unavailable", context="body; count not numerically displayed"))
    output, bindings_path = root / TEX_PATH, root / BINDINGS_PATH
    backups = [backup for path in (output, bindings_path) if (backup := _backup(path))]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text)
    record = dict(schema_version=1, created_utc=datetime.now(timezone.utc).isoformat(),
        purpose="Display of saved public scalar facts only; no statistical recomputation or private data",
        sources=facts.sources, bindings=facts.bindings, style=style,
        layout=dict(body_paragraphs=4, tau_rows=5, figure_height_inches=2.75,
                    target_section_pages=1.5, pagination="Parent verifies in the assembled manuscript"),
        editorial_literals=[dict(display="Supplement Section S36", authority="Explicit parent instruction"),
                           dict(display="Short/long history", authority="Methods already defined in the paper")],
        output=dict(path=TEX_PATH, sha256=hashlib.sha256(text.encode()).hexdigest()),
        backups=backups)
    bindings_path.parent.mkdir(parents=True, exist_ok=True)
    bindings_path.write_text(json.dumps(record, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    result = build_report(parser.parse_args().root)
    print(json.dumps(dict(output=result["output"], style=result["style"],
                         bindings=len(result["bindings"]), backups=result["backups"]), indent=2))
