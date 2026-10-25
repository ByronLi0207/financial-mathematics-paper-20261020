"""Display existing prediction exceptions and complete saved HAC fields.

No fitting, forecast generation, test-statistic calculation or selection occurs.
Every displayed number is copied from an accepted JSON field with its hash and
pointer. This separate builder leaves the original evidence table untouched.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "support": "results/revision-v9/wp2/support.json",
    "summary": "results/revision-v9/wp2/summary.json",
    "contrasts": "results/revision-v9/wp3/contrasts.json",
}
TEX = "submission-jof/generated/v9-complete-diagnostic-fields.tex"
BINDINGS = "notes/revision-v9/continuation-number-bindings.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(root):
    docs = {key: json.loads((root / path).read_text()) for key, path in SOURCES.items()}
    seals = {key: {"path": path, "sha256": digest(root / path)} for key, path in SOURCES.items()}
    bindings, exceptions, contrast_rows = [], [], []

    def number(source, pointer, value, style="six", tag=""):
        current = docs[source]
        for part in pointer.strip("/").split("/"):
            current = current[int(part)] if isinstance(current, list) else current[part]
        assert current == value
        if style == "integer":
            assert type(value) is int
            shown = str(value)
        elif style == "signed":
            shown = format(value, "+.6g")
        else:
            shown = format(value, ".6g")
        if "e" in shown.lower():
            mantissa, exponent = shown.lower().split("e")
            token = mantissa + r"\times10^{" + str(int(exponent)) + "}"
        else:
            token = shown
        if value == 0 and pointer.endswith("dm_p"):
            token += r"^{u}"
        bindings.append(dict(source=source, source_path=SOURCES[source],
                             source_sha256=seals[source]["sha256"], JSON_pointer=pointer,
                             value=value, display=shown, tex_token="$" + token + "$", tag=tag))
        return "$" + token + "$"

    tex = [r"% Generated from existing saved fields only; six significant figures preserve small signs.",
           r"\section{Complete primary-screen exceptions and saved paired-loss diagnostics}\label{sup:v9-complete-fields}",
           "These displays add no analysis. They expose existing exceptions and diagnostic fields that were summarized in the compact Supplement. Original source values, decisions and archives remain unchanged.",
           r"\subsection*{Every exception to the two primary simulation screens}",
           r"\begingroup\small\setlength{\tabcolsep}{4pt}",
           r"\refstepcounter{table}\label{tab:v9-primary-exceptions}",
           r"\noindent\textbf{Table \thetable. Complete saved primary-screen exceptions.}\par",
           r"\begin{center}\begin{tabular}{lrrrlrr}\toprule",
           r"Criterion & $\phi$ & $W$ & $H$ & Model & $\Delta$ (\%) & MCSE \\\midrule"]
    support, summary = docs["support"], docs["summary"]
    for criterion in ("P1", "P2"):
        record = support[criterion]
        assert len(record["cells"]) == len(record["outcomes"]) == record["denominator"]
        assert sum(x is True for x in record["outcomes"]) == record["successes"]
        for cell_index, (cell, outcome) in enumerate(zip(record["cells"], record["outcomes"])):
            if outcome is not False:
                continue
            matches = [(i, row) for i, row in enumerate(summary)
                       if [row[k] for k in ("dgp", "phi_index", "window", "horizon", "method")] == cell]
            assert len(matches) == 1
            index, row = matches[0]
            assert row["dgp"] == "student_t5" and row["full_procedure_status"] == "COMPLETE"
            assert (row["relative_loss_percent"] <= 0 if criterion == "P1" else row["relative_loss_percent"] >= 0)
            base, tag = "/" + str(index), criterion + ":" + str(cell_index)
            values = [criterion, number("summary", base + "/phi", row["phi"], tag=tag),
                      number("summary", base + "/window", row["window"], "integer", tag),
                      number("summary", base + "/horizon", row["horizon"], "integer", tag), row["method"],
                      number("summary", base + "/relative_loss_percent", row["relative_loss_percent"], "signed", tag),
                      number("summary", base + "/relative_loss_mcse", row["relative_loss_mcse"], tag=tag)]
            tex.append(" & ".join(values) + r" \\ % continuation-row:" + tag)
            exceptions.append(dict(criterion=criterion, support_cell_pointer="/"+criterion+"/cells/"+str(cell_index),
                                   support_outcome_pointer="/"+criterion+"/outcomes/"+str(cell_index),
                                   summary_index=index, cell=cell, saved_outcome=False))
    tex.extend([r"\bottomrule\end{tabular}\end{center}\endgroup",
                "All listed cases use Student innovations. A nonpositive loss change contradicts the short-history strict-loss prediction; a nonnegative change contradicts the long-history strict-win prediction. The small positive long-history exception remains a strict-win failure, not a rounded tie. MCSE is the saved repetition-cluster uncertainty summary, not a new significance test. Pooled screen decisions remain unchanged.",
                r"The compact Supplement separately retains every failed universal-simplification inequality. Complete candidate and repetition records remain in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v8-goal/results/revision-v9/wp2}{public simulation archive} with its member index.",
                r"\clearpage\subsection*{Every saved financial paired-loss diagnostic}",
                r"\begingroup\footnotesize\setlength{\tabcolsep}{3pt}",
                r"\refstepcounter{table}\label{tab:v9-complete-hac}",
                r"\noindent\textbf{Table \thetable. Full saved HAC fields for the financial learning curve.}\par",
                r"\begin{center}\begin{tabular}{rrlrrrrr}\toprule",
                r"$H$ & $W$ & Model & $L$ & Mean difference & LRV & DM $t$ & Nominal $p$ \\\midrule"])
    contrasts = docs["contrasts"]
    assert all(row["status"] == "COMPLETE" and row["dm"]["status"] == "OK" for row in contrasts)
    for index, row in sorted(enumerate(contrasts), key=lambda item: (item[1]["horizon"], item[1]["window"], item[1]["method"])):
        base, tag = "/" + str(index), "HAC:" + str(index)
        values = [number("contrasts", base + "/horizon", row["horizon"], "integer", tag),
                  number("contrasts", base + "/window", row["window"], "integer", tag), row["method"],
                  number("contrasts", base + "/dm/bandwidth", row["dm"]["bandwidth"], "integer", tag)]
        values.extend(number("contrasts", base + "/dm/" + field, row["dm"][field], tag=tag)
                      for field in ("mean_difference", "lrv", "dm_t", "dm_p"))
        tex.append(" & ".join(values) + r" \\ % continuation-row:" + tag)
        contrast_rows.append(dict(contrast_index=index, horizon=row["horizon"], window=row["window"], method=row["method"]))
    common_n = contrasts[0]["n"]
    assert all(row["n"] == row["dm"]["n"] == common_n for row in contrasts)
    n_token = number("contrasts", "/0/n", common_n, "integer", "common_n")
    tex.extend([r"\bottomrule\end{tabular}\end{center}\endgroup",
                "Every row uses " + n_token + r" common evaluation issues. The difference is regression minus matched historical headroom, in native FX loss units; $L$ is the saved Bartlett bandwidth and LRV its saved long-run variance. Fields are copied, not recomputed. The tests use a two-sided normal reference, remain post-result and nominal, and carry no family or full-selection adjustment. $0^{u}$, if present, denotes a saved floating-point zero rather than an exact probability.",
                r"Machine-readable \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v8-goal/results/revision-v9/wp3/contrasts.csv}{complete contrasts} preserve additional scores, breaches and exact saved precision.", ""])
    text = "\n".join(tex)
    assert len(exceptions) == sum(support[k]["denominator"] - support[k]["successes"] - support[k]["missing"] for k in ("P1", "P2"))
    assert len(contrast_rows) == len(contrasts)
    assert all(digest(root / value["path"]) == value["sha256"] for value in seals.values())
    receipt = dict(schema="continuation-saved-field-display-1", sources=seals,
                   display_policy="six significant figures; explicit loss sign; exact integer counts; no new statistic",
                   generated_tex=TEX, generated_tex_sha256=hashlib.sha256(text.encode()).hexdigest(),
                   primary_screen_exceptions=exceptions, paired_loss_rows=contrast_rows, bindings=bindings,
                   new_models=0, new_forecasts=0, new_statistical_tests=0, result_archives_changed=False)
    return text, receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text, receipt = build(ROOT)
    tex, bindings = ROOT / TEX, ROOT / BINDINGS
    if args.check:
        assert tex.read_text() == text and json.loads(bindings.read_text()) == receipt
    else:
        assert not tex.exists() and not bindings.exists()
        tex.write_text(text)
        bindings.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    print(json.dumps(dict(status="PASS", mode="check" if args.check else "generated",
                          exceptions=len(receipt["primary_screen_exceptions"]),
                          diagnostics=len(receipt["paired_loss_rows"]), bindings=len(receipt["bindings"]),
                          source_values_modified=False, new_statistics=0)))


if __name__ == "__main__":
    main()
