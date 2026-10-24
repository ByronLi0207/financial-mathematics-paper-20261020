"""S9 read-only saved-field and document-token checks.

No research code is imported. No score, model, simulation, statistical test,
financial ratio, median, cell-win count or new data is calculated here.
Only source-field lookup, exact type/value checks, display formatting, file
hashing and document text presence are used. The sole writable output is the
assigned notes/v7/s9-number-check.json.
"""
from __future__ import annotations

import csv
import ast
from collections import Counter, defaultdict
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "notes/v7"
OUTPUT = HERE / "s9-number-check.json"
TOKEN_OUTPUT = HERE / "s9-number-token-inventory.json"
CACHE = {}
FAILURES = []
NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
FRACTION = re.compile(r"^\\\(\\frac\{(-?\d+)\}\{(-?\d+)\}\\\)$")
SUPPLEMENT_NUMERIC_FORMATS = (".0f", ".1f", ".2f", ".3f", ".4g", ".5f", ".6g")
S1_FROZEN_COMMIT = "3d964af91679a03088f811d7f01f89495a3adf20"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError("source outside repository")
    return path


def read(relative, kind):
    key = (relative, kind)
    if key not in CACHE:
        raw = safe_path(relative).read_bytes()
        if kind == "json":
            result = json.loads(raw)
        elif kind == "csv":
            result = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
        elif kind == "text":
            result = raw.decode("utf-8")
        else:
            raise ValueError("unsupported source format")
        CACHE[key] = result
    return CACHE[key]


def pointer(node, locator):
    if locator == "":
        return node
    if not locator.startswith("/"):
        raise ValueError("invalid JSON pointer")
    for part in locator[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def identical(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all(identical(a, b) for a, b in zip(left, right))
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(identical(left[k], right[k]) for k in left)
    return left == right


def source_value(row):
    kind = row["format"]
    data = read(row["source"], kind)
    if kind == "json":
        return pointer(data, row["pointer"])
    if kind == "csv":
        if not row.get("where"):
            raise ValueError("empty CSV selector")
        if any(type(v) is not str for v in row["where"].values()):
            raise ValueError("CSV selector does not preserve native strings")
        matches = [r for r in data if all(r[k] == v for k, v in row["where"].items())]
        if len(matches) != 1:
            raise ValueError("CSV selector matched " + str(len(matches)) + " rows")
        return matches[0][row["field"]]
    if kind == "text":
        if type(row["value"]) is not str or row["value"] not in data:
            raise ValueError("exact source passage absent")
        return row["value"]
    raise ValueError("unsupported source kind")


def check(condition, category, detail):
    if not condition:
        FAILURES.append(dict(category=category, detail=detail))


def tex_escape(value):
    substitutions = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
                     "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
                     "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(substitutions.get(c, c) for c in str(value))


def main_format(value, specifier):
    if specifier == "set":
        return r"\{" + ",".join(format(float(v), "g") for v in value) + r"\}"
    return format(float(value), specifier) if specifier else str(value)


def supplement_format_options(value):
    if value is None or value == "":
        return {"NA"}
    result = {str(value), tex_escape(value)}
    try:
        result.update(format(float(value), spec) for spec in SUPPLEMENT_NUMERIC_FORMATS)
    except (TypeError, ValueError, OverflowError):
        pass
    if isinstance(value, str) and re.fullmatch(r"-?\d+/-?\d+", value):
        numerator, denominator = value.split("/")
        result.add(r"\(\frac{" + numerator + "}{" + denominator + r"}\)")
    return result


def pdf_normal(value):
    return re.sub(r"\s+", "", value.replace("−", "-").replace("–", "-").replace("—", "-"))


def document(relative):
    reader = PdfReader(safe_path(relative))
    return dict(path=relative, sha256=sha(safe_path(relative)), pages=len(reader.pages),
                text=pdf_normal("\n".join(page.extract_text() or "" for page in reader.pages)))


def source_region(tex, location):
    if location.startswith("table:"):
        label = "tab:" + location.split(":", 1)[1]
        blocks = re.findall(r"\\begin\{table\}.*?\\end\{table\}", tex, re.S)
        matches = [b for b in blocks if r"\label{" + label + "}" in b]
        if len(matches) != 1:
            raise ValueError("main table region not unique: " + location)
        return matches[0]
    if location == "abstract":
        match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
        if not match:
            raise ValueError("abstract absent")
        return match.group(1)
    section = ":".join(location.split(":")[:2])
    marker = r"\label{" + section + "}"
    if tex.count(marker) != 1:
        raise ValueError("main section region not unique: " + location)
    result = tex.split(marker, 1)[1]
    return re.split(r"\\section\*?\{", result, maxsplit=1)[0]


def pdf_display_status(display, doc):
    if NUMBER.fullmatch(display):
        return "scalar", pdf_normal(display) in doc["text"]
    match = FRACTION.fullmatch(display)
    if match:
        # Numerator and denominator are preserved separately by PDF extractors.
        return "fraction_components", all(pdf_normal(v) in doc["text"] for v in match.groups())
    if display.startswith(r"\{") and display.endswith(r"\}"):
        return "set", pdf_normal(display.replace("\\", "")) in doc["text"]
    return "not_a_simple_numeric_token", None


TOKEN = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")


def lexical_numbers(text, offset=0):
    result = []
    for match in TOKEN.finditer(text):
        a, b = match.span()
        before = text[a - 1] if a else ""
        after = text[b] if b < len(text) else ""
        if before.isalpha() or before == "_" or after.isalpha() or after == "_":
            continue
        result.append((offset + a, offset + b, match.group()))
    return result


def numeric_token_inventory(main_bindings, supplement_bindings, by_id):
    """Census source-digit occurrences; preserve uncertainty about positions."""
    source_files = ["submission-jof/manuscript.tex", "submission-jof/supplement.tex",
                    "submission-jof/cover-letter.md", "submission-jof/title-page.tex"]
    source_files.extend(str(p.relative_to(ROOT)) for p in sorted((HERE / "figure-sources").glob("*.tex")))
    texts = {name: safe_path(name).read_text() for name in source_files}
    annotations = defaultdict(list)
    exact_template_passages = []
    unresolved_rows = []

    def typography(value):
        return value.replace("’", "'").replace("–", "--").replace("—", "---")

    def annotate_template(template, location):
        template = typography(template)
        output, last, marks = "", 0, []
        for match in re.finditer(r"@@([A-Z0-9_]+)(?:\|([^@]*))?@@", template):
            output += template[last:match.start()]
            key, form = match.group(1), match.group(2) or ""
            rendered = main_format(by_id[key]["value"], form)
            marks.append((len(output), len(output) + len(rendered), key))
            output += rendered
            last = match.end()
        output += template[last:]
        if not marks:
            return
        main_text = texts["submission-jof/manuscript.tex"]
        hits = [m.start() for m in re.finditer(re.escape(output), main_text)]
        if len(hits) != 1:
            unresolved_rows.append(dict(file="submission-jof/manuscript.tex", location=location,
                                        reason="exact authored template passage not uniquely located", hits=len(hits)))
            return
        start = hits[0]
        for left, right, key in marks:
            annotations["submission-jof/manuscript.tex"].append((start + left, start + right,
                dict(method="exact_placeholder_passage", evidence_ids=[key], location=location)))
        exact_template_passages.append(location)

    authored = json.loads((HERE / "main-v7-sections.json").read_text())
    annotate_template(authored["abstract"], "abstract")
    for section in authored["sections"]:
        for index, block in enumerate(section["blocks"]):
            if block["kind"] in ("p", "eq"):
                annotate_template(block["tex"], section["label"] + ":block:" + str(index))
    # Read literal table templates from syntax only; never import/run the builder.
    tree = ast.parse((HERE / "build_main_v7.py").read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "tables")
    for call in ast.walk(function):
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "table":
            label = ast.literal_eval(call.args[1])
            rows = ast.literal_eval(call.args[4])
            for index, row in enumerate(rows):
                annotate_template(" & ".join(row) + r"\\", label + ":row:" + str(index))
            if len(call.args) > 5:
                annotate_template(ast.literal_eval(call.args[5]), label + ":note")

    # Three manually authored financial contribution literals have separate S2 checks.
    literal_cases = [
        ("cross across horizons on 640 evaluation origins.", {"640": "THEORY_CROSSING_FX_HOURLY_W720_STRICT_CROSSING_COUNT"}),
        ("historical rules win in 34 of 48 additional-panel comparisons.",
         {"34": "PANEL_E5_QR33_EXPANDED_LOSSES", "48": "PANEL_E5_PLANNED"}),
        ("the preferred report reverses at a penalty ratio of about 20.6:1.",
         {"20.6": "FX_PREFERENCE_H24_REVERSAL_RATIO"}),
    ]
    for passage, keys in literal_cases:
        text = texts["submission-jof/manuscript.tex"]
        for found in re.finditer(re.escape(passage), text):
            for left, right, token in lexical_numbers(passage, found.start()):
                if token in keys:
                    annotations["submission-jof/manuscript.tex"].append((left, right,
                        dict(method="separate_contribution_literal_readback", evidence_ids=[keys[token]])))

    # Row-position check, rather than membership in a global set of numbers:
    # every complete supplement data row must match a consecutive sequence of
    # the already field/type-verified binding displays. Ambiguities stay visible.
    flat = []
    for index, binding in enumerate(supplement_bindings):
        display = binding["display"]
        if NUMBER.fullmatch(display):
            flat.append((display, index))
        elif FRACTION.fullmatch(display):
            flat.extend((v, index) for v in FRACTION.fullmatch(display).groups())
    flat_values = [v for v, _ in flat]
    starts = defaultdict(list)
    for index, (value, _) in enumerate(flat):
        starts[value].append(index)
    supplement = texts["submission-jof/supplement.tex"]
    row_matches = []
    for table_index, table in enumerate(re.finditer(r"\\begin\{longtable\}.*?\\end\{longtable\}", supplement, re.S), 1):
        block = table.group()
        body_start = block.index(r"\endfoot") + len(r"\endfoot")
        body = block[body_start:block.rfind(r"\end{longtable}")]
        absolute = table.start() + body_start
        for row in re.finditer(r"[^\n]+", body):
            line = row.group()
            if "&" not in line or not line.rstrip().endswith(r"\\"):
                continue
            nums = lexical_numbers(line, absolute + row.start())
            if not nums:
                continue
            values = [v for _, _, v in nums]
            matches = [i for i in starts[values[0]] if flat_values[i:i + len(values)] == values]
            # Explicit series labels disambiguate repeated integer status rows.
            if len(matches) > 1:
                narrowed = []
                for candidate in matches:
                    indices = {flat[k][1] for k in range(candidate, candidate + len(values))}
                    relevant = [supplement_bindings[k].get("where", {}) for k in indices]
                    series = {where["series_key"] for where in relevant if "series_key" in where}
                    if series and all(key in line for key in series):
                        narrowed.append(candidate)
                if narrowed:
                    matches = narrowed
            lineno = supplement.count("\n", 0, absolute + row.start()) + 1
            if len(matches) != 1:
                unresolved_rows.append(dict(file="submission-jof/supplement.tex", line=lineno,
                    table=table_index, reason="whole-row consecutive-binding alignment " + ("absent" if not matches else "ambiguous"),
                    candidate_windows=len(matches), row=line.strip()))
            if matches:
                candidate = matches[0]
                for position, (left, right, _) in enumerate(nums):
                    binding_index = flat[candidate + position][1]
                    annotations["submission-jof/supplement.tex"].append((left, right,
                        dict(method="whole_row_consecutive_binding_sequence", binding_index=binding_index,
                             source=supplement_bindings[binding_index]["source"],
                             alignment_unique=len(matches) == 1, table=table_index)))
                row_matches.append(dict(table=table_index, line=lineno, numeric_tokens=len(nums),
                                        alignment_unique=len(matches) == 1))

    manual_reviews = []
    resolved_rows = set()

    def line_span(name, line_number):
        lines = texts[name].splitlines(keepends=True)
        return sum(len(line) for line in lines[:line_number - 1]), lines[line_number - 1]

    def bind_exact_line(name, line_number, indices, binding_rows, display_key):
        start, line = line_span(name, line_number)
        actual = lexical_numbers(line, start)
        expected, locators = [], []
        for index in indices:
            binding = binding_rows[index]
            display = binding[display_key]
            values = [display] if NUMBER.fullmatch(display) else list(FRACTION.fullmatch(display).groups())
            expected.extend(values)
            locators.extend([index] * len(values))
        if [v for _, _, v in actual] != expected:
            raise ValueError("manual exact-line binding changed: " + name + ":" + str(line_number))
        for (left, right, _), index in zip(actual, locators):
            annotations[name].append((left, right, dict(method="manually_reviewed_exact_row_or_prose_sequence",
                binding_index=index, source=binding_rows[index]["source"], alignment_unique=True)))
        manual_reviews.append(dict(file=name, line=line_number, method="exact line numeric sequence and explicitly selected original source locators", binding_indices=indices))
        resolved_rows.add((name, line_number))

    # The appended coverage Panel B is not part of the table(...) literal AST.
    # Its five labelled rows were individually read and matched to their four
    # existing coverage bindings (hits/n/POF-p/conditional-CC-p), in column order.
    coverage_prefixes = ["FX_COVERAGE_QR", "FX_COVERAGE_PRIMARY_F", "FX_COVERAGE_MATCHED_F",
                         "COVERAGE_BILL_QR", "COVERAGE_BILL_FROZEN_F"]
    for line_number, prefix in zip(range(272, 277), coverage_prefixes):
        indices = [next(i for i, b in enumerate(main_bindings) if b["id"] == prefix + "_" + suffix)
                   for suffix in ("HITS", "N", "POF_P", "CC_P")]
        bind_exact_line("submission-jof/manuscript.tex", line_number, indices, main_bindings, "rendered")

    # These short prose passages were independently inspected above and read
    # against the exact source locators, rather than an equal-value global set.
    prose_lines = {133:[2],218:[195],219:[196],220:[197],268:[342,343],
                   651:[1377],652:[1378,1379],869:[1737],870:[1738],
                   1007:[1924],1008:[1925],1123:[2044],1124:[2045],
                   1227:[2087],1228:[2088]}
    for line_number, indices in prose_lines.items():
        bind_exact_line("submission-jof/supplement.tex", line_number, indices, supplement_bindings, "display")
    # In the headline preference table, the fraction is registered before the
    # four monetary cells. Verify actual printed column order explicitly.
    for line_number, indices in ((462,[609,610,611,612,608]), (463,[614,615,616,617,613])):
        bind_exact_line("submission-jof/supplement.tex", line_number, indices, supplement_bindings, "display")

    # Exact preference endpoints repeat in many groups. Resolve by the printed
    # source/sample/H/W group, open/point kind, both exact rational strings and
    # complete minimizer list. No fraction is evaluated numerically.
    frontier_source = "results/revision-20261022/preference-robustness/results.json"
    groups = read(frontier_source, "json")["groups"]
    active_group = None
    for line_number in range(501, 632):
        start, line = line_span("submission-jof/supplement.tex", line_number)
        if "&" not in line or not line.rstrip().endswith(r"\\"):
            continue
        label = re.search(r"(FX|Bills) (full|sparse) H(\d+)/W(\d+)", line)
        if label:
            source = "fx_hourly" if label.group(1) == "FX" else "nyfed_weekly"
            options = [(i,g) for i,g in enumerate(groups) if g["source"] == source and
                       g["sample"] == label.group(2) and str(g["horizon"]) == label.group(3) and str(g["window"]) == label.group(4)]
            if len(options) != 1:
                raise ValueError("frontier printed task not unique")
            active_group = options[0]
        if not active_group:
            continue
        cells = line.rstrip().removesuffix(r"\\").split("&")
        if len(cells) != 5 or cells[1].strip() not in ("open", "point"):
            continue
        fractions = [a + "/" + b for a,b in re.findall(r"\\frac\{(-?\d+)\}\{(-?\d+)\}", line)]
        methods = cells[-1].strip().replace(r"\_", "_")
        group_index, group = active_group
        kind = "regions" if cells[1].strip() == "open" else "points"
        candidates = []
        for i,item in enumerate(group["frontier"][kind]):
            expected = [item["left"],item["right"]] if kind == "regions" else [item["alpha"]]
            if expected == fractions and ", ".join(item["methods"]) == methods:
                candidates.append(i)
        if len(candidates) != 1:
            raise ValueError("frontier exact task/boundary/method row mismatch at " + str(line_number))
        for left, right, _ in lexical_numbers(line, start):
            annotations["submission-jof/supplement.tex"].append((left, right,
                dict(method="manually_reviewed_task_kind_exact_fraction_and_minimizers",
                     source=frontier_source, pointer=f"/groups/{group_index}/frontier/{kind}/{candidates[0]}", alignment_unique=True)))
        resolved_rows.add(("submission-jof/supplement.tex", line_number))
        manual_reviews.append(dict(file="submission-jof/supplement.tex", line=line_number,
            method="source/sample/H/W plus kind, exact rational boundary strings and complete minimizer list", source=frontier_source,
            pointer=f"/groups/{group_index}/frontier/{kind}/{candidates[0]}"))

    # Four all-integer failure rows and six all-NA rows are identified from their
    # printed model/reference labels, not by repeated H/W or tau values alone.
    failure_source = "results/supervisor-20261023/r6/summary.csv"
    for line_number in range(897,901):
        start,line = line_span("submission-jof/supplement.tex",line_number)
        cells=[c.strip().replace(r"\_","_") for c in line.rstrip().removesuffix(r"\\").split("&")]
        phase,key,hw,report,status=cells;horizon,window=hw.split("/")
        where=dict(phase=phase,series_key=key,horizon=horizon,window=window,report=report)
        matches=[r for r in read(failure_source,"csv") if all(r[k]==v for k,v in where.items())]
        if len(matches)!=1 or matches[0]["status"]!=status:
            raise ValueError("R6 named failed-row mismatch")
        for left,right,_ in lexical_numbers(line,start):
            annotations["submission-jof/supplement.tex"].append((left,right,dict(method="explicit_named_csv_failure_row",source=failure_source,where=where,alignment_unique=True)))
        resolved_rows.add(("submission-jof/supplement.tex",line_number))
    na_sources=[(965,"results/revision-20261023/v6/wp2-summary.json","method_rows","ACI_F"),
                (966,"results/revision-20261023/v6/wp2-summary.json","method_rows","ACI_QR"),
                (1003,"results/revision-20261023/v6/wp2-findings.json","wrapped_pairs",None)]
    for line_number,source,array,method in na_sources:
        choices=[(i,r) for i,r in enumerate(read(source,"json")[array]) if r['source']=='nyfed_weekly' and r['horizon']==24 and r['window']==260 and (method is None or r['method']==method)]
        if len(choices)!=1 or choices[0][1]['status']!='NA':raise ValueError('named WP2 NA row mismatch')
        start,line=line_span('submission-jof/supplement.tex',line_number)
        for left,right,_ in lexical_numbers(line,start):annotations['submission-jof/supplement.tex'].append((left,right,dict(method='explicit_named_json_NA_row',source=source,pointer=f'/{array}/{choices[0][0]}',alignment_unique=True)))
        resolved_rows.add(('submission-jof/supplement.tex',line_number))
    for line_number,source_name,reference in [(1221,'fx_hourly','primary'),(1222,'fx_hourly','matched'),(1223,'nyfed_weekly','primary')]:
        source='results/revision-20261023/v6/wp5-tau-summary.json'
        choices=[(i,r) for i,r in enumerate(read(source,'json')['rows']) if r['source']==source_name and r['tau']==.99 and r['reference_kind']==reference]
        if len(choices)!=1 or choices[0][1]['status']!='NA':raise ValueError('named WP5 NA row mismatch')
        start,line=line_span('submission-jof/supplement.tex',line_number)
        for left,right,_ in lexical_numbers(line,start):annotations['submission-jof/supplement.tex'].append((left,right,dict(method='explicit_named_json_NA_row',source=source,pointer=f'/rows/{choices[0][0]}',alignment_unique=True)))
        resolved_rows.add(('submission-jof/supplement.tex',line_number))
    unresolved_rows=[r for r in unresolved_rows if (r.get('file'),r.get('line')) not in resolved_rows]

    inventory = []
    for name, text in texts.items():
        bib = text.find(r"\begin{thebibliography}")
        begin = text.find(r"\begin{document}")
        math_spans = [m.span() for pattern in (r"\\\(.*?\\\)", r"\\\[.*?\\\]", r"(?<!\\)\$[^$]*?\$")
                      for m in re.finditer(pattern, text, re.S)]
        reference_spans = [m.span() for pattern in (r"\\(?:cite[a-zA-Z]*|label|ref)\{[^}]*\}", r"\\(?:url|href)\{[^}]*\}")
                           for m in re.finditer(pattern, text)]
        lines = text.splitlines(keepends=True)
        line_start = 0
        in_longtable = False
        for line_number, line in enumerate(lines, 1):
            if r"\begin{longtable}" in line:
                in_longtable = True
            for match in TOKEN.finditer(line):
                a, b = match.span(); left, right = line_start + a, line_start + b
                token = match.group()
                record = dict(file=name, line=line_number, column=a + 1, token=token,
                              context=line.strip()[:500])
                category, detail = None, {}
                mapped = [extra for x, y, extra in annotations[name] if x <= left and right <= y]
                mapped.sort(key=lambda v: (not v.get('alignment_unique',True),v.get('method')=='whole_row_consecutive_binding_sequence'))
                if name.startswith("notes/v7/figure-sources/"):
                    category = "figure_axis_or_layout"
                    detail = dict(verified_scope="classification only; graph coordinates/ticks are not a new scientific calculation or per-point source verification")
                elif mapped:
                    category = "existing_binding"
                    detail = mapped[0]
                elif bib >= 0 and left >= bib:
                    category = "reference_metadata"
                elif any(x <= left < y for x, y in reference_spans):
                    category = "reference_or_source_identifier"
                elif begin >= 0 and left < begin:
                    category = "figure_axis_or_layout"
                elif re.search(r"\\(?:uchyph|setlength|renewcommand|begin\{(?:tabular|longtable|minipage)|includegraphics|vspace|hspace)", line):
                    category = "figure_axis_or_layout"
                elif any(x <= left < y for x, y in math_spans):
                    category = "mathematical_definition_or_structure"
                elif (a and (line[a - 1].isalpha() or line[a - 1] == "_")) or (b < len(line) and (line[b].isalpha() or line[b] == "_")):
                    category = "source_file_or_model_label"
                elif re.search(r"\\(?:section|paragraph|textbf)\{(?:S\d+|C\d+|Proposition\s*\d+)", line):
                    category = "mathematical_definition_or_structure"
                elif (name.endswith('manuscript.tex') and line_number==253 and token=='1') or (name.endswith('supplement.tex') and line_number==93 and token=='3.4'):
                    category = "mathematical_definition_or_structure"
                    detail = dict(manual_review='normalized ratio denominator 1 or cited proposition number, not a new measured result')
                    if name.endswith('supplement.tex'):
                        locator='results/revision-20261023/round2/levy/theorem-source.json'
                        if 'Proposition3.4' not in read(locator,'json')['actual_scope']:
                            raise ValueError('historical Proposition 3.4 locator changed')
                        detail.update(source=locator,pointer='/actual_scope',parent_readback='notes/revision-v4-jof/reference-audit.md:439-451')
                elif re.fullmatch(r"(?:19|20)\d\d", token) and (line[max(0,a-2):a].endswith("(") or re.search(r"(?:et al\.|Lindsay|Gneiting|Holm|White|Newey|Hoogen|Sussman|Wisniewski)",line)):
                    category = "reference_metadata"
                else:
                    category = "unclassified"
                    # Keep unbound prose candidates explicit; never call this a
                    # located binding merely because an equal number occurs elsewhere.
                    candidates = [i for i, r in enumerate(supplement_bindings) if name.endswith("supplement.tex") and r["display"] == token]
                    if candidates:
                        detail["equal_display_candidate_binding_indices"] = candidates
                        detail["warning"] = "Equal value only; position/source correspondence is NOT established."
                record.update(category=category, evidence=detail)
                inventory.append(record)
            if r"\end{longtable}" in line:
                in_longtable = False
            line_start += len(line)
    unclassified = [r for r in inventory if r["category"] == "unclassified"]
    payload = dict(
        status="NEEDS_MANUAL_REVIEW" if unclassified or unresolved_rows else "CLASSIFIED_WITH_LIMITS",
        files={name: dict(sha256=sha(safe_path(name)), numeric_token_occurrences=sum(r["file"] == name for r in inventory)) for name in texts},
        definition="Exhaustive occurrences of ASCII digit-bearing numeric tokens in the seven listed source files; digits inside identifiers and URLs are retained and classified, not dropped.",
        category_counts=dict(Counter(r["category"] for r in inventory)),
        main_exact_template_passages=exact_template_passages,
        supplement_whole_row_matches=row_matches,
        independently_reviewed_exact_contexts=manual_reviews,
        unresolved_row_alignment=unresolved_rows,
        unclassified=unclassified,
        tokens=inventory,
        limits=["This is an exhaustive digit-token source inventory, not a census of spelled-out number words or automatic PDF layout positions.",
                "No global set membership is represented as a located binding. Main locations use exact original placeholder passages; supplement data rows use complete numeric sequences against consecutive field-verified bindings. Nonunique row alignments remain listed.",
                "Figure-source coordinates and ticks are classified as display parameters; this inventory does not recalculate coordinates or check every plotted value against research arrays.",
                "Mathematical/structural and metadata categories classify roles; publication metadata verification is the separate S7 record.",
                "Unclassified occurrences and ambiguous row locations require the parent's explicit reading; an empty raw-value mismatch list does not resolve them."],
    )
    TOKEN_OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return {key: payload[key] for key in ("status", "category_counts", "unclassified", "unresolved_row_alignment")}


def main():
    s2 = []
    for part in sorted((HERE / "evidence-parts").glob("*.json")):
        payload = json.loads(part.read_text())
        if not isinstance(payload, list):
            raise ValueError("evidence part is not a list: " + str(part))
        s2.extend(payload)
    by_id = {}
    for row in s2:
        check(row["id"] not in by_id, "duplicate_s2_id", row["id"])
        by_id[row["id"]] = row
        try:
            check(identical(source_value(row), row["value"]), "s2_source_value_or_type", row["id"])
        except Exception as exc:
            check(False, "s2_source_read", dict(id=row["id"], error=str(exc)))

    bindings_main = json.loads((HERE / "main-v7-numeric-bindings.json").read_text())
    bindings_supp_file = json.loads((HERE / "s5-supplement-bindings.json").read_text())
    bindings_supp = bindings_supp_file["bindings"]
    check(len(bindings_main) == 117, "main_binding_count_drift", len(bindings_main))
    check(len(bindings_supp) == 2125, "supplement_binding_count_drift", len(bindings_supp))
    main_tex = (ROOT / "submission-jof/manuscript.tex").read_text()
    supp_tex = (ROOT / "submission-jof/supplement.tex").read_text()
    main_pdf = document("submission-jof/manuscript.pdf")
    supp_pdf = document("submission-jof/supplement.pdf")
    pdf_status = {"main": {}, "supplement": {}}
    supplement_non_numeric = []

    for index, binding in enumerate(bindings_main):
        try:
            row = by_id[binding["id"]]
            check(binding["source"] == row["source"], "main_source_locator", index)
            actual = source_value(row)
            check(identical(actual, binding["raw_value"]), "main_raw_value_or_type", index)
            expected_display = main_format(actual, binding["format"])
            check(expected_display == binding["rendered"], "main_display_format", index)
            check(binding["rendered"] in source_region(main_tex, binding["location"]),
                  "main_tex_named_region", dict(index=index, location=binding["location"]))
            category, present = pdf_display_status(binding["rendered"], main_pdf)
            pdf_status["main"][category] = pdf_status["main"].get(category, 0) + 1
            check(present is not False, "main_pdf_numeric_presence", index)
        except Exception as exc:
            check(False, "main_binding_read", dict(index=index, error=str(exc)))

    for index, binding in enumerate(bindings_supp):
        try:
            actual = source_value(binding)
            check(identical(actual, binding["value"]), "supplement_raw_value_or_type", index)
            check(binding["display"] in supplement_format_options(actual), "supplement_display_format", index)
            check(binding["display"] in supp_tex, "supplement_tex_display_presence", index)
            category, present = pdf_display_status(binding["display"], supp_pdf)
            pdf_status["supplement"][category] = pdf_status["supplement"].get(category, 0) + 1
            if present is None:
                supplement_non_numeric.append(dict(index=index, location=binding["location"], display=binding["display"]))
            check(present is not False, "supplement_pdf_numeric_presence", index)
        except Exception as exc:
            check(False, "supplement_binding_read", dict(index=index, error=str(exc)))

    fingerprints = json.loads((HERE / "evidence-source-fingerprints.json").read_text())
    supplement_fingerprints = bindings_supp_file["source_sha256"]
    s2_sources = {row["source"] for row in s2}
    supplement_sources = {row["source"] for row in bindings_supp}
    s1_baseline_extensions = {}
    # S2 later gained saved motivating-window fields. The original fingerprint
    # JSON did not include that public file. Preserve that baseline unchanged,
    # and compare the additional source to the immutable pre-S2 S1 PASS blob.
    for relative in sorted(s2_sources - fingerprints.keys()):
        try:
            safe_path(relative)
            frozen = subprocess.run(["git", "show", S1_FROZEN_COMMIT + ":" + relative],
                                    cwd=ROOT, check=True, capture_output=True).stdout
            digest = hashlib.sha256(frozen).hexdigest()
            s1_baseline_extensions[relative] = dict(commit=S1_FROZEN_COMMIT, sha256=digest)
            fingerprints[relative] = digest
        except Exception as exc:
            check(False, "s1_frozen_source_extension", dict(source=relative, error=str(exc)))
    check(s2_sources <= fingerprints.keys(), "s2_source_without_frozen_hash",
          sorted(s2_sources - fingerprints.keys()))
    check(supplement_sources <= supplement_fingerprints.keys(), "supplement_source_without_frozen_hash",
          sorted(supplement_sources - supplement_fingerprints.keys()))
    hashes = {}
    for baseline, expected_hashes in (("S2", fingerprints), ("supplement", supplement_fingerprints)):
        for relative, expected in expected_hashes.items():
            try:
                actual = sha(safe_path(relative))
                check(actual == expected, "original_source_hash_drift", dict(baseline=baseline, source=relative))
                if relative in hashes:
                    check(hashes[relative]["expected"] == expected, "frozen_hash_baselines_disagree", relative)
                hashes[relative] = dict(expected=expected, actual=actual)
            except Exception as exc:
                check(False, "original_source_hash_read", dict(source=relative, error=str(exc)))

    s8 = json.loads((HERE / "s8-verification.json").read_text())["documents"]
    s9_main_receipt_path = HERE / "s9-manuscript-compile-receipt.json"
    s9_main_receipt = json.loads(s9_main_receipt_path.read_text()) if s9_main_receipt_path.exists() else None
    for name, doc, tex in (("manuscript", main_pdf, main_tex), ("supplement", supp_pdf, supp_tex)):
        expected = s9_main_receipt if name == "manuscript" and s9_main_receipt else s8[name]
        expected_pdf = expected["pdf_sha256"] if "pdf_sha256" in expected else expected["sha256"]
        check(doc["sha256"] == expected_pdf, "pdf_approved_compile_identity", name)
        check(hashlib.sha256(tex.encode()).hexdigest() == expected["source_sha256"], "tex_approved_compile_identity", name)

    contribution_cases = [
        dict(id="C1", evidence=["THEORY_CROSSING_FX_HOURLY_W720_STRICT_CROSSING_COUNT"],
             values=["640"], passage="cross across horizons on 640 evaluation origins."),
        dict(id="C2", evidence=["PANEL_E5_QR33_EXPANDED_LOSSES", "PANEL_E5_PLANNED"],
             values=[34, 48], passage="historical rules win in 34 of 48 additional-panel comparisons."),
        dict(id="C3", evidence=["FX_PREFERENCE_H24_REVERSAL_RATIO"],
             values=["20.6308977263"], passage="the preferred report reverses at a penalty ratio of about 20.6:1."),
    ]
    contributions = {r["id"]: r for r in json.loads((HERE / "contributions.json").read_text())}
    for case in contribution_cases:
        for key, expected in zip(case["evidence"], case["values"]):
            check(key in contributions[case["id"]]["evidence"], "contribution_s2_link", case["id"])
            check(identical(source_value(by_id[key]), expected), "contribution_native_value", case["id"])
        if case["id"] == "C3":
            check(format(float(case["values"][0]), ".1f") == "20.6", "contribution_ratio_format", "C3")
        check(case["passage"] in main_tex, "contribution_tex_passage", case["id"])
        check(pdf_normal(case["passage"]) in main_pdf["text"], "contribution_pdf_passage", case["id"])

    token_inventory = numeric_token_inventory(bindings_main, bindings_supp, by_id)
    report = dict(
        status="PASS" if not FAILURES else "FAIL",
        command=[sys.executable, "-B", "notes/v7/check_numbers_v7.py"],
        main_binding_count=len(bindings_main), supplement_binding_count=len(bindings_supp),
        s2_records_checked=len(s2), s2_source_files_checked=len(fingerprints),
        supplement_original_source_files_checked=len(supplement_fingerprints),
        every_s2_and_supplement_source_has_frozen_hash=(
            s2_sources <= fingerprints.keys() and supplement_sources <= supplement_fingerprints.keys()),
        distinct_original_source_hashes_checked=len(hashes),
        contribution_literals_checked=["C1: 640", "C2: 34 of 48", "C3: 20.6:1"],
        rendered_pdf_checks=pdf_status,
        documents=[{k: v for k, v in doc.items() if k != "text"} for doc in (main_pdf, supp_pdf)],
        source_hashes=hashes, mismatches=len(FAILURES), failures=FAILURES,
        additional_s2_source_baselines=s1_baseline_extensions,
        current_main_compilation_baseline="notes/v7/s9-manuscript-compile-receipt.json" if s9_main_receipt else "notes/v7/s8-verification.json",
        token_inventory_summary=token_inventory,
        unclassified_digit_token_occurrences=len(token_inventory['unclassified']),
        unresolved_token_row_alignments=len(token_inventory['unresolved_row_alignment']),
        coverage_limits=[
            "Checks the 117 saved main bindings, 2125 saved supplement bindings, all current S2 records and the three separately hand-authored contribution literals.",
            "Main TeX token presence is checked in its named table/abstract/section, not at every individual PDF coordinate. Supplement full display strings are checked in actual final TeX.",
            "PDF checks confirm numeric scalar tokens and set contents anywhere in the corresponding PDF text; exact rational numerators and denominators are checked as separate components. This is not a new visual or cell-position proof.",
            "Supplement binding records omit their precise numeric-format specifier. Each display must match a fixed allowed source-scalar formatting convention (.0f/.1f/.2f/.3f/.4g/.5f/.6g), exact raw/escaped text, exact LaTeX, NA or exact rational formatting; no financial statistic is derived.",
            "Non-numeric LaTeX identities/status strings are source- and TeX-checked; PDF glyph order for those expressions is not inferred from text extraction.",
            "This does not claim an exhaustive census of every freehand numeric glyph, structural equation constant, bibliographic year, figure axis tick or linked archival document. The cover letter is outside this delegated check.",
            "No private input CSV, source-paper dataset, per-origin trace or research implementation is read or executed. No new financial result, model, score, hypothesis test or S10 action is performed.",
        ],
        non_numeric_supplement_pdf_not_inferred=supplement_non_numeric,
        new_models=0, new_financial_statistics=0, new_hypothesis_tests=0, new_research_data=0,
    )
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    summary = {k: report[k] for k in ("status", "main_binding_count", "supplement_binding_count",
               "s2_records_checked", "s2_source_files_checked", "supplement_original_source_files_checked",
               "distinct_original_source_hashes_checked", "rendered_pdf_checks", "unclassified_digit_token_occurrences",
               "unresolved_token_row_alignments", "mismatches", "failures")}
    summary['token_inventory_status']=token_inventory['status']
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return bool(FAILURES)


if __name__ == "__main__":
    raise SystemExit(main())
