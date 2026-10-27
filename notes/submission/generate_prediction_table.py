#!/usr/bin/env python3
"""Format the saved H3 register; never fit a model or recompute a judgment.

The only prose normalization inserts whitespace. Every displayed cell is bound
to its exact register fields, whole-register SHA, and individual field SHA.
Main-table numbers come from the explicitly recorded H2 compiled aux cut;
H8 must check them again against its final aux. Supplement references are local.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = Path("notes/submission/prediction-register.json")
OUTPUT = Path("submission-final/generated/submission-predictions.tex")
BINDINGS = Path("notes/submission/prediction-display-bindings.json")
MAIN_AUX = Path("submission-package/ASMBI/manuscript.aux")
SUPPLEMENT = Path("submission-final/supplement.tex")
DECISIONS = {"\u6210\u7acb": "Supported", "\u4e0d\u6210\u7acb": "Not supported", "\u65e0\u6cd5\u5224\u5b9a": "Undetermined"}

# Current local sections replacing the register's pinned historical anchors.
LOCATIONS = {
    "E5": (("sup:panel", "sup:panel-second"), ("tab:weekly",)),
    "R6": (("sup:selection", "sup:selection-failures"), ("tab:weekly",)),
    "E1": (("sup:v10-menu",), ()),
    "E2": (("sup:v10-cftc",), ("tab:v10-cftc-contracts",)),
    "F1": (("sup:v12-details",), ()),
    "F2": (("sup:v12-details", "sup:v13-checks"), ("tab:v13-validation",)),
    "F3": (("sup:v13-checks",), ("tab:v12-tau",)),
    "G2": (("sup:v13-checks",), ("tab:v13-validation",)),
    "G3": (("sup:v13-checks",), ()),
    "WP2": (("sup:submission-wp2",), ()),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def value_digest(value: object) -> str:
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


def display_spaces(value: str) -> str:
    """Insert only whitespace, preserving all characters and numeric strings."""
    text = re.sub(r"(?<=[a-z])(?=\d)", " ", value)
    text = re.sub(r"(?<=\d)(?=[a-z])", " ", text)
    text = re.sub(r"(?<=[a-z])(?=[+-]\d|\[)", " ", text)
    text = re.sub(r"(?<=tau)(?=\.)", " ", text)
    text = text.replace("Nonepp", "None pp")
    text = re.sub(r"(<=|>=|=>|[=<>])", r" \1 ", text)
    text = re.sub(r";(?=\S)", "; ", text)
    # Preserve conventional digit-grouping commas; space ordinary punctuation.
    text = re.sub(r",(?=\S)(?!\d{3}(?:\D|$))", ", ", text)
    text = re.sub(r" +", " ", text).strip()
    if re.sub(r"\s", "", text) != re.sub(r"\s", "", value):
        raise ValueError("Display formatting changed a non-whitespace character")
    return text


def tex(value: str, breaks: bool = True) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
        "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "<": r"\ensuremath{<}", ">": r"\ensuremath{>}",
    }
    out = []
    for char in value:
        out.append(replacements.get(char, char))
        if breaks and char in "_/,=":
            out.append(r"\allowbreak{}")
    return "".join(out)


def row_id_tex(value: str) -> str:
    return r"\texttt{" + r"\allowbreak{}".join(tex(p, False) for p in
              re.split(r"(?<=[._])", value)) + "}"


def local_sources(path: Path, seen: set[Path] | None = None) -> dict[str, str]:
    seen = set() if seen is None else seen
    if path in seen:
        return {}
    seen.add(path)
    result = {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8")}
    for rel in re.findall(r"\\input\{([^}]+)\}", result[str(path.relative_to(ROOT))]):
        filename = rel if rel.endswith(".tex") else rel + ".tex"
        # TeX resolves these project inputs against the master directory, even
        # when the command occurs inside an already included generated file.
        candidate = ROOT / SUPPLEMENT.parent / filename
        if not candidate.exists():
            candidate = path.parent / filename
        if candidate.exists():
            result.update(local_sources(candidate, seen))
        elif candidate.resolve() != (ROOT / OUTPUT).resolve():
            raise FileNotFoundError(candidate)
    return result


def render(main_aux: Path) -> tuple[str, dict]:
    raw = (ROOT / REGISTER).read_bytes()
    register_sha = digest(raw)
    register = json.loads(raw)
    rows = register["rows"]
    ids = [r["row_id"] for r in rows]
    order = register["latex_table_handoff"]["row_order"]
    if len(rows) != 36 or len(set(ids)) != 36 or ids != order:
        raise ValueError("Expected all 36 unique rows in the saved handoff order")
    decisions = collections.Counter(DECISIONS[r["decision_zh"]] for r in rows)
    if decisions != {"Supported": 20, "Not supported": 11, "Undetermined": 5}:
        raise ValueError("Saved decision counts changed; do not recompute them")
    sensitivities = [r for r in rows if r["role"] == "sensitivity"]
    if len(sensitivities) != 7 or any(r["method"] != "QR4" for r in sensitivities):
        raise ValueError("Expected the seven separately registered QR4 sensitivities")
    aux_bytes = main_aux.read_bytes()
    aux_labels = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]+)\}",
                                 aux_bytes.decode("utf-8")))
    sources = local_sources(ROOT / SUPPLEMENT)
    local_labels = set(re.findall(r"\\label\{([^}]+)\}", "\n".join(sources.values())))
    location_records = {}
    for group, (sections, tables) in LOCATIONS.items():
        missing = set(sections) - local_labels
        if missing or any(t not in aux_labels for t in tables):
            raise ValueError(f"Unresolved location for {group}: {missing}")
        section_refs = [r"\ref{" + label + "}" for label in sections]
        parts = [("Supplement Section~" + section_refs[0]) if len(sections) == 1
                 else (r"Supplement\par Sections\par " + ", ".join(section_refs))]
        parts += ["Main Table " + aux_labels[label] for label in tables]
        location_records[group] = {
            "latex": r";\par ".join(parts), "local_section_labels": list(sections),
            "main_table_labels": {label: aux_labels[label] for label in tables},
            "source_register_field": "manuscript_locations",
            "remapping_note": "Current local section labels replace pinned historical anchors; WP2 uses sup:submission-wp2, not historical sup:final-cftc.",
        }
    lines = [
        "% Generated by notes/submission/generate_prediction_table.py; do not hand edit.",
        "% Register SHA256: " + register_sha,
        r"\clearpage",
        r"\section{Prewritten predictions, thresholds and saved judgments}\label{sup:submission-predictions}",
        "This register prints every saved prediction without fitting models, recomputing thresholds or changing a saved judgment. Round gives the complete row identifier and its recorded role. Supported, Not supported and Undetermined translate the saved decision only; saved status strings and unavailable reasons remain explicit.",
        "Prewritten before the indicated new calculations does not imply original-study preregistration, an untouched evaluation period or external-registry preregistration. Public Git posting and local pre-run designs are distinct. E5 has only a saved receipt for its local pre-run design: the original design Git object is unavailable, and its public file upload followed the recorded run. R6, E1, E2 and WP2 have verified local pre-run designs but public file uploads after calculation. F1, F2, F3, G2 and G3 have local and public Git design commits before their new calculations; their inspected-study and retrospective limits still apply.",
        "Panel A retains the primary and secondary rows. Panel B separately retains all QR4 sensitivity rows; they cannot replace a primary QR33 judgment. This separation does not relabel the originally primary QR4 predictions in E2 or WP2. Related series and markets do not create independent dealer replications.",
        "WP2 adds only W520 forecasts; W52/W260 outcomes were already known. Its QR33 high-region row remains structurally NOT\_TESTABLE with planned=0 and NO\_REGISTERED\_REGION\_CELL. Both low-region methods support combined P1, but the saved overall primary verdict remains PARTLY; the secondary P3 cannot upgrade it.",
        r"\begingroup",
        r"\fontsize{8.5}{10.2}\selectfont",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\setlength{\LTcapwidth}{\linewidth}",
        r"\begin{longtable}{@{}>{\raggedright\arraybackslash}p{18mm}>{\raggedright\arraybackslash}p{33mm}>{\raggedright\arraybackslash}p{30mm}>{\raggedright\arraybackslash}p{43mm}>{\raggedright\arraybackslash}p{20mm}>{\raggedright\arraybackslash}p{17mm}@{}}",
        r"\caption{All saved prewritten prediction rows. Thresholds, results and judgments are copied from the bound register; numeric precision is retained.}\label{tab:submission-predictions}\\",
        r"\toprule Round & Prediction & Threshold & Saved result & Judgment & Location \\\midrule",
        r"\endfirsthead",
        r"\caption[]{Continued.}\\",
        r"\toprule Round & Prediction & Threshold & Saved result & Judgment & Location \\\midrule",
        r"\endhead",
        r"\midrule\multicolumn{6}{r}{\emph{Continued on next page}}\\",
        r"\endfoot",
        r"\bottomrule\endlastfoot",
    ]
    bindings = []
    for panel, panel_rows in [("A", [r for r in rows if r["role"] != "sensitivity"]),
                              ("B", sensitivities)]:
        title = "Primary and secondary predictions" if panel == "A" else "Separate QR4 sensitivity predictions"
        lines += [r"\multicolumn{6}{@{}l}{\textbf{Panel " + panel + ". " + title + r"}}\\*\midrule"]
        for row in panel_rows:
            index = ids.index(row["row_id"])
            fields = ["prediction", "original_threshold", "actual_output"]
            displays = {field: display_spaces(row[field]) for field in fields}
            judgment = DECISIONS[row["decision_zh"]]
            status = json.dumps(row["saved_status"], ensure_ascii=False) if isinstance(row["saved_status"], bool) else row["saved_status"]
            cells = [row_id_tex(row["row_id"]) + r"\par " + tex(row["role"]),
                     *(tex(displays[field]) for field in fields),
                     tex(judgment) + r"\par\texttt{" + tex(status) + "}",
                     location_records[row["group"]]["latex"]]
            lines += ["% row_id: " + row["row_id"], " & ".join(cells) + r" \\[3pt]"]
            source_fields = [["row_id", "role"], ["prediction"], ["original_threshold"],
                             ["actual_output"], ["decision_zh", "saved_status"], ["manuscript_locations"]]
            cell_bindings = []
            for column, latex, source_names in zip(["Round", "Prediction", "Threshold", "Saved result", "Judgment", "Location"], cells, source_fields):
                cell_bindings.append({"column": column, "display_latex": latex,
                    "sources": [{"register_pointer": f"/rows/{index}/{field}",
                                 "raw_value": row[field], "value_sha256": value_digest(row[field])}
                                for field in source_names]})
            bindings.append({"row_id": row["row_id"], "register_index": index,
                "handoff_index": index, "display_index": len(bindings), "panel": panel,
                "source_row_sha256": value_digest(row), "register_sha256": register_sha,
                "formatted_fields": displays, "judgment_translation": judgment,
                "location_resolution": location_records[row["group"]], "cells": cell_bindings,
                "original_design_bindings": row["design_bindings"],
                "original_result_bindings": row["result_bindings"]})
    lines += [r"\end{longtable}", r"\endgroup",
        "The display-bindings JSON retains raw fields, JSON Pointers and SHA256 values.", ""]
    result = "\n".join(lines)
    if len(re.findall(r"^% row_id:", result, re.M)) != 36:
        raise ValueError("Generated row loss")
    return result, {"schema": "submission-prediction-display-bindings-v1",
        "register": str(REGISTER), "register_sha256": register_sha,
        "generator": str(Path(__file__).relative_to(ROOT)),
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "generated_tex": str(OUTPUT), "generated_tex_sha256": digest(result.encode()),
        "main_aux": str(main_aux.relative_to(ROOT)), "main_aux_sha256": digest(aux_bytes),
        "main_aux_cut": "H2 actual ASMBI compile; no later main table insertion before H4. Recheck numbering against final H8 aux.",
        "current_supplement_source_sha256": {name: digest(text.encode()) for name, text in sources.items() if name != str(OUTPUT)},
        "counts": {"total": 36, "panel_A": 29, "panel_B_QR4_sensitivity": 7,
                   "judgments": dict(decisions)},
        "formatting": "Whitespace insertion only before TeX escaping; no numeric rounding, replacement or decision computation.",
        "value_sha256_encoding": "UTF-8 JSON, ensure_ascii=False, sort_keys=True, separators=(',', ':'); whole-file SHA values use the original file bytes.",
        "layout": {"columns": ["Round", "Prediction", "Threshold", "Saved result", "Judgment", "Location"],
                   "font_pt": 8.5, "leading_pt": 10.2,
                   "column_widths_mm": [18, 33, 30, 43, 20, 17],
                   "alignment": "ragged right", "repeated_longtable_headers": True},
        "scope_note_register_pointers": ["/global_limits", "/timing_by_group", "/latex_table_handoff/required_footnotes", "/wp2_group_verdict", "/rows/34/original_threshold", "/rows/34/actual_output", "/rows/31/interpretation_limit"],
        "rows": bindings}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-aux", type=Path, default=ROOT / MAIN_AUX)
    parser.add_argument("--check", action="store_true", help="Require exact existing generated bytes; write nothing")
    args = parser.parse_args()
    text, bindings = render(args.main_aux.resolve())
    payload = json.dumps(bindings, ensure_ascii=False, indent=2) + "\n"
    for path, value in [(ROOT / OUTPUT, text), (ROOT / BINDINGS, payload)]:
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != value:
                raise SystemExit(f"Stale or missing generated output: {path.relative_to(ROOT)}")
        else:
            path.write_text(value, encoding="utf-8")
    print(json.dumps({"status": "PASS_CHECK" if args.check else "GENERATED",
                      "rows": bindings["counts"], "register_sha256": bindings["register_sha256"],
                      "tex_sha256": bindings["generated_tex_sha256"]}))


if __name__ == "__main__":
    main()
