"""Current Supplement occurrence/field audit, using public frozen aggregates only.

This module never imports forecasting software, reads private arrays, fits models,
or recomputes financial tests. Old v7 proof files are inputs, never outputs.
Run: python3 -B notes/revision-v8/check_wp8_supp_numbers.py
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MAIN = "submission-jof/supplement.tex"
EXPECTED_INPUTS = (
    "submission-jof/generated/v8-mc-full-table.tex",
    "submission-jof/generated/v8-mc-four-table.tex",
    "submission-jof/generated/v8-daily-results-table.tex",
    "submission-jof/generated/v8-three-window-table.tex",
    "submission-jof/generated/v8-backcast-complete-table.tex",
)
TOKEN = re.compile(r"[+−-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+−-]?\d+)?")
WORDS = re.compile(r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|both|half|twice|doubled|first|second|third)\b", re.I)


def identical(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(identical(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(identical(a, b) for a, b in zip(left, right))
    return left == right


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text):
    """Only documented equivalent typography, never numeric normalization."""
    text = text.replace(r"\dfrac", r"\frac")
    text = re.sub(r"\\(?:displaystyle|textstyle)\s*", "", text)
    text = re.sub(r"\\rule\{0pt\}\{[^}]+\}", "", text)
    return re.sub(r"\s+", " ", text).strip()


def pointer(data, path):
    for key in path.lstrip("/").split("/") if path else []:
        key = key.replace("~1", "/").replace("~0", "~")
        data = data[int(key)] if isinstance(data, list) else data[key]
    return data


def field(data, tokens):
    for token in tokens:
        data = data[token]
    return data


def display(value, fmt="g", scale=1):
    if value is None:
        return "NA"
    # Integer seeds/indices must never be routed through a float or g formatter.
    return str(value) if type(value) is int and fmt == "g" and scale == 1 else format(value * scale, fmt)


def old_display_rule(value, printed):
    if value is None or value == "":
        return "NA for saved missing value" if printed == "NA" else None
    if printed == str(value):
        return "native exact string/integer representation"
    if isinstance(value,str) and re.fullmatch(r"-?\d+/-?\d+",value):
        a,b=value.split("/")
        if printed==r"\(\frac{"+a+"}{"+b+r"}\)":
            return "exact rational numerator/denominator strings; no evaluation"
    if isinstance(value,str):
        escaped=value.replace("_",r"\_").replace("%",r"\%")
        if escaped==printed:return "TeX escaped native text"
    try:
        precision=len(printed.rsplit(".",1)[1]) if "." in printed and "e" not in printed.lower() else 0
        specs=[f".{precision}f",".4g",".6g"]
        for spec in specs:
            if format(float(value),spec)==printed:return "saved native numeric field formatted "+spec
    except (ValueError,TypeError,OverflowError):
        pass
    return None


def uncomment(line):
    return re.split(r"(?<!\\)%", line, maxsplit=1)[0]


def layout_spans(text):
    """Find actual command arguments, retaining nested TeX dimension braces."""
    starts=r'\\(?:documentclass|usepackage|setlength|renewcommand|vspace|hspace|begin|includegraphics|uchyph)\b\*?'
    for match in re.finditer(starts,text):
        command=match.group().lstrip('\\').rstrip('*'); pos=match.end()
        if command=='uchyph':
            scalar=re.match(r'\s*=\s*\d+',text[pos:])
            if scalar:yield match.start(),pos+scalar.end()
            continue
        if pos<len(text) and text[pos]=='[':
            end=text.find(']',pos)
            if end<0:continue
            pos=end+1
        if command=='includegraphics':
            yield match.start(),pos
            continue
        count=2 if command in ('setlength','renewcommand','begin') else 1
        valid=True
        for index in range(count):
            if pos>=len(text) or text[pos]!='{':valid=False;break
            begin=pos; depth=1; pos+=1
            while pos<len(text) and depth:
                if text[pos]=='{' and text[pos-1]!='\\':depth+=1
                if text[pos]=='}' and text[pos-1]!='\\':depth-=1
                pos+=1
            if depth:valid=False;break
            if command=='begin' and index==0 and text[begin+1:pos-1] not in ('longtable','tabular','minipage'):
                valid=False;break
        if valid:yield match.start(),pos


class Audit:
    def __init__(self, root, document_root=None):
        self.root = Path(root).resolve()
        self.document_root = Path(document_root or root).resolve()
        self.cache = {}
        self.failures, self.ambiguous = [], []
        self.lines, self.files, self.inputs = [], {}, []
        self.annotations, self.locations = [], []
        self.contract_locations = []
        self.raw_counts = Counter()

    def path(self, name, document=False):
        base = self.document_root if document else self.root
        path = (base / name).resolve()
        if not path.is_relative_to(base):
            raise ValueError("path escapes assigned root: " + name)
        return path

    def load(self, name):
        if name not in self.cache:
            self.cache[name] = json.loads(self.path(name).read_text())
        return self.cache[name]

    def check(self, condition, gate, **detail):
        if not condition:
            self.failures.append(dict(gate=gate, **detail))
        return bool(condition)

    def expand(self, name=MAIN, stack=()):
        if name in stack:
            self.check(False, "recursive_input", file=name, reason="input cycle")
            return
        path = self.path(name, document=True)
        if not path.is_file():
            self.check(False, "recursive_input", file=name, reason="missing input")
            return
        text = path.read_text()
        self.files[name] = dict(sha256=digest(path), bytes=path.stat().st_size)
        for number, raw in enumerate(text.splitlines(), 1):
            line = uncomment(raw)
            self.lines.append(dict(file=name, line=number, text=line))
            for match in re.finditer(r"\\(?:input|include)\{([^}]+)\}", line):
                target = match[1]
                if not Path(target).suffix:
                    target += ".tex"
                # TeX compiler working directory is submission-jof for this source.
                joined = str(Path(MAIN).parent / target)
                try:
                    self.path(joined, document=True)
                except ValueError as exc:
                    self.check(False, "recursive_input", file=name, line=number, reason=str(exc))
                    continue
                self.inputs.append(joined)
                self.expand(joined, (*stack, name))

    def prepare_offsets(self):
        pieces, offset = [], 0
        for line in self.lines:
            line["start"] = offset
            pieces.append(line["text"] + "\n")
            offset += len(line["text"]) + 1
        self.text = "".join(pieces)

    def annotate(self, start, end, category, **evidence):
        self.annotations.append((start, end, category, evidence))

    def passage(self, expected, role, refs=(), required=True):
        pattern = r"\s+".join(re.escape(bit) for bit in expected.split())
        found = list(re.finditer(pattern, self.text))
        if required:
            self.check(len(found) == 1, "new_exact_passage", role=role, expected=expected, matches=len(found))
        if len(found) > 1:
            self.ambiguous.append(dict(role=role, expected=expected, matches=len(found)))
        if len(found) == 1:
            match = found[0]
            self.annotate(*match.span(), "located_current_passage", role=role, source_fields=list(refs), expected_text=expected)
            self.locations.append(dict(role=role, source_fields=list(refs), start=match.start(), end=match.end()))

    def old_sources(self):
        old = self.load("notes/v7/s5-supplement-bindings.json")
        for name, expected_hash in old["source_sha256"].items():
            self.check(digest(self.path(name)) == expected_hash, "old_source_hash", source=name)
        for index, row in enumerate(old["bindings"]):
            try:
                if row["format"] == "json":
                    actual = pointer(self.load(row["source"]), row["pointer"])
                elif row["format"] == "csv":
                    rows = list(csv.DictReader(self.path(row["source"]).read_text(encoding="utf-8-sig").splitlines()))
                    matches = [r for r in rows if all(r[k] == v for k, v in row["where"].items())]
                    if len(matches) != 1:
                        raise ValueError("nonunique CSV selector")
                    actual = matches[0][row["field"]]
                else:
                    actual = row["value"] if row["value"] in self.path(row["source"]).read_text() else None
                self.check(identical(actual, row["value"]), "old_typed_field", binding_index=index, source=row["source"])
                self.check(old_display_rule(actual,row['display']) is not None,"old_display_formatter",binding_index=index,display=row['display'])
            except (KeyError, ValueError, IndexError) as exc:
                self.check(False, "old_typed_field", binding_index=index, reason=str(exc))
        self.raw_counts["old_typed_fields"] = len(old["bindings"])
        return old["bindings"]

    def old_rows_and_occurrences(self, old_bindings):
        receipt = self.load("notes/revision-v8/wp7-supplement-integration.json")
        baseline = subprocess.check_output(["git", "show", receipt["baseline_commit"] + ":" + MAIN], cwd=self.root).decode()
        self.check(hashlib.sha256(baseline.encode()).hexdigest() == receipt["baseline_supplement_sha256"], "old_baseline_identity")
        before = [line for line in baseline.splitlines() if "&" in line and re.search(r"\d", line)]
        main_text = self.path(MAIN, document=True).read_text()
        old_area = main_text.split(r"\section{Frozen controlled comparison", 1)[0]
        after = [line for line in old_area.splitlines() if "&" in line and re.search(r"\d", line)]
        self.check(before == after, "old_ordered_rows", expected=len(before), actual=len(after), first_differences=[i for i,(a,b) in enumerate(zip(before, after)) if a != b][:10])
        self.raw_counts["old_numeric_rows"] = len(before)
        self.raw_counts["old_result_rows"] = sum(not r.startswith("Series &") for r in before)

        # Historical token annotations are relocated through complete line text,
        # not v7 line numbers or equal numeric membership. Only equivalent math
        # macro/padding transforms are normalized. All fields are reread above.
        history = self.load("notes/v7/s9-number-token-inventory.json")
        groups = defaultdict(list)
        for token in history["tokens"]:
            if token["file"] == MAIN:
                groups[token["line"]].append(token)
        contexts = defaultdict(list)
        for old_line, tokens in groups.items():
            contexts[normalize(tokens[0]["context"])].append((old_line, sorted(tokens, key=lambda r:r["column"])))
        used = Counter()
        math_roles = {
            37:"pinball quantile domain endpoints",38:"complementary pinball weight",41:"local proposition ordinal",
            44:"quantile upper-tail complement",55:"quantile upper-tail complement",81:"local proposition ordinal",
            82:"first increment index",83:"zero partial-sum initial state and sum index",85:"symmetric two-tail allocation",
            86:"symmetric two-tail allocation",89:"Levy maximal factor and zero index",93:"audited external proposition identifier",
            96:"nonnegative crossing threshold",98:"symmetry half-probability at crossing",100:"negative crossing sign boundary",
            102:"Levy factor and zero threshold",103:"partial-sum zero index",116:"two-increment counterexample labels",
            117:"symmetric Rademacher support",173:"AR lag index",174:"stationary AR innovation variance",
            176:"AR increment autocorrelation identity",226:"stationary Gaussian displacement variance",
            227:"conditional Gaussian level moments",353:"transport construction at horizon zero",
            439:"complementary preference weight",1265:"indicator definition",1305:"inclusive mature-history index",
        }
        for line in self.lines:
            if line["file"] != MAIN:
                continue
            key = normalize(line["text"])
            options = contexts.get(key, [])
            if not options:
                continue
            old_line, tokens = options[min(used[key],len(options)-1)]
            used[key] += 1
            actual = list(TOKEN.finditer(line["text"]))
            if [m.group() for m in actual] != [r["token"] for r in tokens]:
                continue
            for match, token in zip(actual, tokens):
                category, evidence = token["category"], dict(token.get("evidence", {}))
                evidence.update(historical_file="notes/v7/s9-number-token-inventory.json", historical_line=old_line, relocation="complete normalized line plus ordered token sequence")
                if category == "mathematical_definition_or_structure":
                    if old_line not in math_roles:
                        continue
                    category = "reviewed_math_definition"
                    evidence["role"] = math_roles[old_line]
                elif category == "figure_axis_or_layout":
                    category = "layout_setting"
                    evidence["role"] = "explicit TeX page/table dimension or array stretch"
                elif category == "source_file_or_model_label":
                    category = "retained_named_identity"
                    evidence["role"] = "retained task/model/series identifier in unchanged full context; numeric result cells retain their individual field bindings"
                elif category.startswith("reference"):
                    category = "reference_identifier"
                    evidence["role"] = "source URL, archive version, citation year or cross-reference identifier; bibliography verification is a separate WP8 gate"
                if "binding_index" in evidence:
                    binding = old_bindings[evidence["binding_index"]]
                    evidence.update(source=binding["source"], locator={k:binding[k] for k in ("pointer","where","field") if k in binding}, native_value=binding["value"], printed_display=binding["display"])
                    evidence['display_rule']=old_display_rule(binding['value'],binding['display'])
                self.annotate(line["start"]+match.start(), line["start"]+match.end(), category, **evidence)

    def new_fields(self):
        receipt = self.load("notes/revision-v8/wp7-supplement-integration.json")
        for name, expected_hash in receipt["source_hashes"].items():
            self.check(digest(self.path(name)) == expected_hash, "new_source_hash", source=name)
        for index, row in enumerate(receipt["bindings"]):
            actual = field(self.load(row["source"]), row["field_tokens"])
            self.check(identical(actual, row["original_value"]), "new_typed_field", binding_index=index, source=row["source"], field=row["field"])
            self.check(display(actual,row["format"],row["scale"]) == row["rendered"], "new_field_formatter", binding_index=index)
        self.raw_counts["new_typed_fields"] = len(receipt["bindings"])
        self.check(len(receipt["bindings"]) == 2080, "new_binding_contract")

    def table_rows(self, name):
        return [line for line in self.lines if line["file"] == name and "&" in line["text"] and line["text"].rstrip().endswith(r"\\") and not any(s in line["text"] for s in ("shortstack", "History &", "Window &", "Horizon &"))]

    def check_rows(self, name, expected, gate, row_evidence):
        actual = self.table_rows(name)
        texts = [line["text"].strip() for line in actual]
        self.check(texts == expected, gate, file=name, expected_rows=len(expected), actual_rows=len(actual), mismatch_rows=[i for i,(a,b) in enumerate(zip(texts,expected)) if a!=b][:10])
        for index, (line, expected_text) in enumerate(zip(actual, expected)):
            if line["text"].strip() == expected_text:
                self.annotate(line["start"],line["start"]+len(line["text"]),"located_table_row", **row_evidence[index])
                if 'token_fields' in row_evidence[index]:
                    locators=row_evidence[index]['token_fields']
                    numbers=list(TOKEN.finditer(line['text']))
                    if self.check(len(numbers)==len(locators),'table_token_locator_count',file=name,row=index,actual=len(numbers),expected=len(locators)):
                        for token,locator in zip(numbers,locators):
                            self.annotate(line['start']+token.start(),line['start']+token.end(),'located_table_cell_field',source=row_evidence[index]['source'],row_pointer=row_evidence[index]['pointer'],identity=row_evidence[index]['identity'],**locator)
        return actual

    def mc_tables(self):
        source = "results/revision-v8/wp3/summary.json"
        cells = self.load(source)["cells"]
        refs = {tuple(r[k] for k in ("horizon","phi","variance_persistence","window")):r for r in cells if r["method"] == "F"}
        for name, method in zip(EXPECTED_INPUTS[:2], ("QR33","QR4")):
            selected = sorted(((i,r) for i,r in enumerate(cells) if r["method"] == method), key=lambda pair:tuple(pair[1][k] for k in ("horizon","phi","variance_persistence","window")))
            expected, evidence = [], []
            for i,row in selected:
                identity = {k:row[k] for k in ("method","horizon","phi","variance_persistence","window")}
                ref=refs[tuple(row[k] for k in ("horizon","phi","variance_persistence","window"))]
                self.check(all(identical(row[k],ref[v]) for k,v in (("reference_breach_rate","model_breach_rate"),("reference_breach_mcse","model_breach_mcse"),("mean_reference_loss","mean_model_loss"))), "mc_reference_identity", identity=identity)
                fields=[("horizon","g",1),("phi","g",1),("variance_persistence","g",1),("window","g",1),("relative_loss_percent",".2f",1),("relative_loss_mcse",".2f",1),("reference_breach_rate",".2f",100),("reference_breach_mcse",".2f",100),("model_breach_rate",".2f",100),("model_breach_mcse",".2f",100),("win_fraction",".2f",100),("win_mcse",".2f",100),("complete_repetitions","g",1),("planned_repetitions","g",1)]
                v=[display(row[k],fmt,scale) for k,fmt,scale in fields]
                parts=v[:4]+[f"{v[j]} ({v[j+1]})" for j in (4,6,8,10)]+[f"{v[12]} / {v[13]}"]
                expected.append(" & ".join(parts)+r"\\")
                evidence.append(dict(source=source, pointer=f"/cells/{i}", identity=identity, fields=[dict(field=k,format=fmt,scale=scale,native_value=row[k],printed=vv) for (k,fmt,scale),vv in zip(fields,v)]))
            actual=self.check_rows(name,expected,"mc_ordered_rows",evidence)
            for line,ev,expected_text in zip(actual,evidence,expected):
                if line["text"].strip()!=expected_text:continue
                for token,locator in zip(TOKEN.finditer(line["text"]),ev["fields"]):
                    self.annotate(line["start"]+token.start(),line["start"]+token.end(),"located_mc_cell_field",source=source,pointer=ev["pointer"]+"/"+locator["field"],identity=ev["identity"],**locator)
            self.raw_counts["mc_rows"] += len(selected)

    def copied_tables(self):
        receipt=self.load("notes/revision-v8/wp7-supplement-integration.json")
        for copy in receipt["exact_copies"]:
            if copy["target"] not in EXPECTED_INPUTS:continue
            self.check(self.path(copy["target"],document=True).read_bytes()==self.path(copy["source"]).read_bytes(),"exact_source_table_copy",source=copy["source"],target=copy["target"])
        source="results/revision-v8/wp4/summary.json"
        daily=self.load(source)
        contrasts={(r["window"],r["horizon"],r["method"]):(i,r) for i,r in enumerate(daily["contrasts"])}
        names={"F":"Historical headroom","QR33":"33-feature regression","QR4":"Four-feature regression"}
        expected,evidence=[],[]
        for i,row in enumerate(daily["cells"]):
            metrics=row["evaluation"]
            key=(row["window"],row["horizon"],row["method"])
            contrast=contrasts.get(key)
            pct="--" if contrast is None else display(contrast[1]["relative_loss_percent"],".3f")
            parts=[str(row["window"]),str(row["horizon"]),names[row["method"]],"--" if row["selected_penalty"] is None else display(row["selected_penalty"]),display(metrics["mean_loss"],".3f",1e-6),pct,f'{metrics["strict_breach_count"]} / {display(metrics["strict_breach_rate"],".3f",100)}']
            expected.append(" & ".join(parts)+r"\\")
            evidence.append(dict(source=source,pointer=f"/cells/{i}",identity=dict(zip(("W","H","method"),key)), fields=["window","horizon","selected_penalty","evaluation.mean_loss / 1e6 (.3f)","evaluation.strict_breach_count","evaluation.strict_breach_rate * 100 (.3f)"],contrast_pointer=None if contrast is None else f"/contrasts/{contrast[0]}/relative_loss_percent",formatter="penalty g; loss USD/1e6 .3f; relative change .3f; breach rate *100 .3f"))
            loc=[dict(pointer=f'/cells/{i}/window',format='exact int'),dict(pointer=f'/cells/{i}/horizon',format='exact int')]
            if row['method']=='QR33':loc.append(dict(pointer=f'/cells/{i}/method',format='QR33 procedure-label digit, not result'))
            if row['selected_penalty'] is not None:loc.append(dict(pointer=f'/cells/{i}/selected_penalty',format='g'))
            loc.append(dict(pointer=f'/cells/{i}/evaluation/mean_loss',format='.3f',scale=1e-6))
            if contrast is not None:loc.append(dict(pointer=f'/contrasts/{contrast[0]}/relative_loss_percent',format='.3f'))
            loc.extend([dict(pointer=f'/cells/{i}/evaluation/strict_breach_count',format='exact int'),dict(pointer=f'/cells/{i}/evaluation/strict_breach_rate',format='.3f',scale=100)])
            evidence[-1]['token_fields']=loc
        self.check_rows(EXPECTED_INPUTS[2],expected,"daily_ordered_rows",evidence)
        self.raw_counts["daily_rows"]=len(expected)

        # Verify each old-source copied row through its unique selector and native
        # CSV strings, before using the additive three-window presentation.
        bindings=self.load("results/revision-v8/wp5/three-window-bindings.json")
        for b in bindings["old_source_bindings"]:
            self.check(digest(self.path(b["path"]))==b["sha256"],"backcast_old_source_hash",source=b["path"])
            rows=list(csv.DictReader(self.path(b["path"]).read_text(encoding="utf-8-sig").splitlines()))
            matches=[r for r in rows if all(r[k]==v for k,v in b["selector"].items())]
            self.check(len(matches)==1 and identical(matches[0],b["copied_row"]),"backcast_old_source_selector",source=b["path"],selector=b["selector"])
        fullsource="results/revision-v8/wp5/summary.json"
        full=self.load(fullsource)["contrasts"]
        three="results/revision-v8/wp5/three-window-summary.json"
        windows=self.load(three)["rows"]
        for i,row in enumerate(windows):
            if "source_contrast_index" in row:
                src=full[row["source_contrast_index"]]
                self.check(all(identical(row[k],src[k]) for k in src),"backcast_new_source_contrast",row=i,source_contrast_index=row["source_contrast_index"])
        copies=[v['copied_row'] for v in bindings['old_source_bindings']]
        for wi,ci in [(2,2),(3,3),(4,6),(5,8)]:
            row=windows[wi]; saved=copies[ci]
            if wi<4:
                mapping={'n':'n','mean_difference':'mean_loss_difference_QR_minus_F','lrv':'raw_LRV','dm_t':'HAC_statistic','dm_p':'two_sided_normal_HAC_p','bandwidth':'L','horizon':'H'}
                self.check(all(identical(row['dm'][k],int(saved[v]) if k in ('n','horizon','bandwidth') else float(saved[v])) for k,v in mapping.items()),'backcast_old_DM_copy',window_row=wi,source_binding=ci)
                self.check(row['model_mean_loss']==float(saved['QR_mean_loss']) and row['reference_mean_loss']==float(saved['F_mean_loss']) and row['relative_change_percent']==float(saved['ratio_change_percent']),'backcast_old_loss_copy',window_row=wi,source_binding=ci)
            else:
                self.check(all(identical(row['dm'][k],int(saved[k]) if k in ('n','horizon','bandwidth') else float(saved[k])) for k in ('n','horizon','bandwidth','mean_difference','lrv','dm_t','dm_p')),'backcast_old_DM_copy',window_row=wi,source_binding=ci)
                reference_index=5 if wi==4 else 7
                expected_model=float(copies[4]['mean_pinball']); expected_ref=float(copies[reference_index]['mean_pinball'])
                # This exact display-only derivation is explicitly declared in
                # WP5; it does not replace the archived native ratio field.
                self.check(row['model_mean_loss']==expected_model and row['reference_mean_loss']==expected_ref and row['relative_change_percent']==100*(expected_model/expected_ref-1),'backcast_declared_old_ratio_display',window_row=wi)
                self.check(row['model_breaches']==int(copies[4]['strict_breach_count']) and row['reference_breaches']==int(copies[reference_index]['strict_breach_count']),'backcast_old_breach_copy',window_row=wi)
        self.check(windows[2]['model_breaches']==int(copies[0]['strict_breach_count']) and windows[2]['reference_breaches']==int(copies[1]['strict_breach_count']) and windows[3]['model_breaches']==int(copies[0]['strict_breach_count']) and windows[3]['reference_breaches'] is None,'backcast_old_missing_fields_preserved')
        refnames={"F_matched":"Matched F2880","F_rolling720":"Rolling F720"}
        window_names={"extra_full_prefix":"Full prefix","previous_retro":"Prior backcast","original_inspected":"Original"}
        def pvalue(v):return "NA" if v is None else "<0.001" if v<.001 else display(v,".3f")
        def fmt(v):return "NA" if v is None else str(v)
        for name,source,rows,kind in [(EXPECTED_INPUTS[3],three,windows,"three_window"),(EXPECTED_INPUTS[4],fullsource,full,"complete_backcast")]:
            expected,evidence=[],[]
            for i,row in enumerate(rows):
                d=row["dm"]
                if kind=="three_window":
                    parts=[window_names[row["window_name"]],refnames[row["reference"]],display(row["model_mean_loss"],".3f",1e-6)+" / "+display(row["reference_mean_loss"],".3f",1e-6),display(row["relative_change_percent"],".3f"),fmt(row["model_breaches"])+" / "+fmt(row["reference_breaches"]),display(d.get("dm_t"),".3f"),pvalue(d.get("dm_p")),str(row["n"])]
                    ptr=f"/rows/{i}"
                else:
                    parts=[str(row["horizon"]),"33-feature" if row["method"]=="QR33" else "Four-feature",refnames[row["reference"]],display(row["mean_model_loss"],".3f",1e-6)+" / "+display(row["mean_reference_loss"],".3f",1e-6),display(row["relative_change_percent"],".3f"),fmt(row["model_breach_count"])+" / "+fmt(row["reference_breach_count"]),display(d.get("dm_t"),".3f")+" ("+pvalue(d.get("dm_p"))+")"]
                    ptr=f"/contrasts/{i}"
                expected.append(" & ".join(parts)+r"\\")
                evidence.append(dict(source=source,pointer=ptr,identity={k:row[k] for k in ("method","horizon","reference")},source_contrast_index=row.get("source_contrast_index"),formatter="loss USD/1e6 .3f; relative change .3f; counts exact integers; DM .3f; raw p <0.001 iff native p<0.001 else .3f",native_row=row))
                loc=[]
                if kind!='three_window':
                    loc.append(dict(pointer=ptr+'/horizon',format='exact int'))
                    if row['method']=='QR33':loc.append(dict(pointer=ptr+'/method',format='QR33 procedure-label digit, not result'))
                loc.append(dict(pointer=ptr+'/reference',format='named reference history 2880/720; identity preserved'))
                for k in (('model_mean_loss','reference_mean_loss') if kind=='three_window' else ('mean_model_loss','mean_reference_loss')):
                    loc.append(dict(pointer=ptr+'/'+k,format='.3f',scale=1e-6))
                loc.append(dict(pointer=ptr+'/relative_change_percent',format='.3f'))
                for k in (('model_breaches','reference_breaches') if kind=='three_window' else ('model_breach_count','reference_breach_count')):
                    if row[k] is not None:loc.append(dict(pointer=ptr+'/'+k,format='exact int'))
                if d.get('dm_t') is not None:loc.append(dict(pointer=ptr+'/dm/dm_t',format='.3f'))
                if d.get('dm_p') is not None:loc.append(dict(pointer=ptr+'/dm/dm_p',format='<0.001 iff native p<0.001; otherwise .3f',native_value=d['dm_p']))
                if kind=='three_window':loc.append(dict(pointer=ptr+'/n',format='exact int'))
                evidence[-1]['token_fields']=loc
            self.check_rows(name,expected,kind+"_ordered_rows",evidence)
            self.raw_counts[kind+"_rows"]=len(expected)

    def new_prose(self):
        ds="protocol/revision-v8/wp3-mechanism-design.json"
        d=self.load(ds)
        dsref=lambda *paths:[dict(source=ds,field=p) for p in paths]
        self.passage(r'The level persistences are \(\phi\in\{'+','.join(display(v) for v in d['phi'])+r'\}\), variance persistences \(p=a+b\in\{'+','.join(display(v) for v in d['variance_persistence'])+r'\}\), histories \(W\in\{'+','.join(map(str,d['windows']))+r'\}\), and horizons \(H\in\{'+','.join(map(str,d['horizons']))+r'\}\).',"exact DGP grids",dsref("phi","variance_persistence","windows","horizons"))
        triples=', '.join(r'\('+ '('+','.join(display(v[k]) for k in ('omega','alpha','beta'))+')'+r'\)' for v in d['variance_parameters'].values())
        self.passage(r'\((\omega,a,b)\) triples are '+triples+'.',"GARCH parameter triples",dsref("variance_parameters"))
        self.passage(f"a burn-in of {d['burn_in']} observations precedes {d['retained_observations']} retained observations.","burn and retained lengths",dsref("burn_in","retained_observations"))
        self.passage(f"There are {d['repetitions']} independent repetition streams, with master entropy {d['master_entropy']} and", "exact integer repetition/entropy",dsref("repetitions","master_entropy","rng"))
        self.passage(f"uses origins {d['validation_first']}--{d['validation_last']}; evaluation uses {d['evaluation_first']}--{d['evaluation_last']}, with {d['evaluation_last']-d['evaluation_first']+1} overlapping issues and a refit every {d['refit_step']} records.","MC issue calendar",dsref("validation_first","validation_last","evaluation_first","evaluation_last","refit_step"))
        self.passage(r'\(W\) origins \(r-H-W+1,\ldots,r-H\)',"inclusive mature-label training formula",dsref("common_random_numbers"))
        self.passage(r'N_t=\phi N_{t-1}+\varepsilon_t,\qquad \varepsilon_t=\sqrt{v_t}z_t,\qquad v_t=\omega+a\varepsilon_{t-1}^{2}+bv_{t-1},\qquad z_t\stackrel{\mathrm{iid}}{\sim}\mathcal N(0,1).',"Gaussian AR/GARCH recurrence: lags, square, mean zero and unit normal variance",dsref("initial_level","initial_variance","variance_parameters","rng"))
        self.passage(r'\widehat\Delta=100\left(\dfrac{\overline A}{\overline B}-1\right),\qquad \operatorname{MCSE}(\widehat\Delta)= \dfrac{100\,s(A_j-\widehat rB_j)}{\sqrt R\,\overline B},\qquad \widehat r=\dfrac{\overline A}{\overline B}.',"declared relative-change and delta MCSE equations",dsref("mcse.relative_change","mcse.relative_mcse"))
        self.passage(r'Sample standard deviations use divisor \(R-1\).',"sample SD divisor",dsref("mcse.relative_mcse","mcse.breach_rate"))
        self.passage(r'\(\sqrt{\widehat\pi(1-\widehat\pi)/R}\). At zero or all wins that plug-in error is zero',"binomial plug-in MC error boundary",dsref("mcse.strict_wins"))
        w=self.load("results/revision-v8/wp3/summary.json")["cells"][0]["win_mcse_worst_bound"]
        self.passage(r'\(0.5/\sqrt R\), or '+display(w,".2f",100)+" percentage points here.","worst-case win MC error",[dict(source=ds,field="mcse.strict_wins"),dict(source="results/revision-v8/wp3/summary.json",field="cells[0].win_mcse_worst_bound",format=".2f",scale=100)])
        support="results/revision-v8/wp3/support.json"
        s=self.load(support)["procedures"]["QR33"]
        threshold=re.search(r'>=([0-9.]+)',d['support_screen']['clear_gain'])[1]
        multiplier=re.search(r'plus (\d+) delta',d['support_screen']['clear_gain'])[1]
        region=re.fullmatch(r'H=(\d+),W>=(\d+),p>=([0-9.]+)',d['support_screen']['target_region'])
        self.passage(f"The frozen descriptive clear-gain screen requires all {d['repetitions']} paired repetitions, "+r'\(\widehat\Delta+'+multiplier+r'\operatorname{MCSE}(\widehat\Delta)<0\), and a strict-win fraction at least \('+threshold+r'\). Its target is \(H='+region[1]+r'\), \(W\ge '+region[2]+r'\), \(p\ge '+region[3]+r'\). Support additionally requires at least '+str(s['minimum_target_clear_gains'])+' of '+str(s['target_cell_count'])+' clear-gain target cells and none among the '+str(s['outside_cell_count'])+' outside cells. Each regression has only '+str(s['target_clear_gain_count'])+' target gains and '+str(s['outside_clear_gain_count'])+' outside gains.',"complete frozen support-screen counts and design",dsref("repetitions","support_screen")+[dict(source=support,field="procedures.QR33"),dict(source=support,field="procedures.QR4")])
        self.check(all(identical(s[k],self.load(support)['procedures']['QR4'][k]) for k in ('minimum_target_clear_gains','target_cell_count','outside_cell_count','target_clear_gain_count','outside_clear_gain_count')),"both_regression_screen_counts")
        rf="results/revision-v8/wp3/readout-bindings.json"
        r=self.load(rf); f=r['failed_candidates'][0]; ident=f['identity']
        self.passage(f"The complete inventory contains {r['method_status_counts']['COMPLETE']} complete method tasks, {r['candidate_status_counts']['COMPLETE']} complete validation candidates and {r['candidate_status_counts']['FAILED']} failed candidate. The failure is the four-feature candidate at zero-based repetition {ident['rep']}, "+r'\(\phi='+display(ident['phi'])+r'\), \(p='+display(ident['variance_persistence'])+r'\), \(W='+str(ident['window'])+r'\), \(H='+str(ident['horizon'])+r'\), and penalty \('+display(f['candidate']['penalty'])+r'\). Its duality-gap criterion fails at '+str(f['candidate']['failure_diagnostics']['iterations'])+' iterations. The frozen eligible-completed-candidate rule selects penalty \\('+display(f['selected_penalty'])+r'\),',"candidate/procedure failure identity",[dict(source=rf,field="method_status_counts"),dict(source=rf,field="candidate_status_counts"),dict(source=rf,field="failed_candidates[0]")])
        daily="results/revision-v8/wp4/readout-bindings.json"; r=self.load(daily)
        self.passage(f"The pinned hourly FX snapshot produces {r['daily_metadata']['n_daily']} nonempty source-naive calendar days", "actual completed-day source count",[dict(source=daily,field="daily_metadata.n_daily")])
        p=r['periods']; dates={k:p[k].split('T')[0] for k in ('validation_first','validation_last','evaluation_first','evaluation_last')}
        self.passage(f"validation runs from {dates['validation_first']} to {dates['validation_last']} and evaluation from {dates['evaluation_first']} to {dates['evaluation_last']} on {p['evaluation_count']} common issues.","daily dates and common issue count",[dict(source=daily,field="periods",transform="date before T")])
        self.passage('Historical headroom wins seven of the eight named comparisons,',"daily seven/eight comparison count words",[dict(source="results/revision-v8/wp4/classification.json",field="QR33.historical_wins + QR4.historical_wins; planned_comparisons sum",rendered="seven of the eight")])
        cls=self.load("results/revision-v8/wp4/classification.json")
        self.check(cls['QR33']['historical_wins']+cls['QR4']['historical_wins']==7 and cls['QR33']['planned_comparisons']+cls['QR4']['planned_comparisons']==8,"daily_word_count_source")
        self.passage(r'four-feature longer-history, shorter-horizon daily exception lowers loss by about 3.0\% with 37 regression breaches versus 30 historical breaches.',"signed daily exception and breaches",[dict(source="results/revision-v8/wp4/summary.json",field="contrasts[5].relative_loss_percent",format=".1f",scale=-1),dict(source="results/revision-v8/wp4/summary.json",field="cells[8].evaluation.strict_breach_count"),dict(source="results/revision-v8/wp4/summary.json",field="cells[6].evaluation.strict_breach_count")])
        bd="protocol/revision-v8/wp5-fixed-prefix-design.json"; b=self.load(bd); sample=b['sample']
        self.passage(f"{sample['evaluation_first']}--{sample['evaluation_last']}, with {sample['evaluation_count']} common issue origins before the original later validation.","full-prefix inclusive indices and count",[dict(source=bd,field="sample")])
        m=b['methods']; penalty=lambda i,h:display(m[i]['penalty_by_horizon'][str(h)])
        self.passage(r'full regression: \(H=6,\lambda='+penalty(2,6)+r'\), \(H=24,\lambda='+penalty(2,24)+r'\); four-feature regression: \(H=6,\lambda='+penalty(3,6)+r'\), \(H=24,\lambda='+penalty(3,24)+r'\).',"later-selected original penalties by procedure and horizon",[dict(source=bd,field="methods[2:4].penalty_by_horizon")])
        exposure="notes/revision-v8/wp5-prior-exposure-proof.json"; e=self.load(exposure)
        self.passage(f"The full prefix contains all {e['nested_old_retro_issue_count']} earlier reported backcast origins, with inclusive issue indices {b['known_exposure']['R6_retro_evaluation'][0]}--{b['known_exposure']['R6_retro_evaluation'][1]}.","old nested backcast count and exact index range",[dict(source=exposure,field="nested_old_retro_issue_count"),dict(source=bd,field="known_exposure.R6_retro_evaluation")])
        span=e['old_H24_target_coverage_merged'][0]
        self.passage(f"Actual earlier rolling-validation targets at the longer horizon cover {span[0]}--{span[1]},", "actual old longer-horizon target coverage",[dict(source=exposure,field="old_H24_target_coverage_merged[0]")])
        self.passage(r'L=\min\!\left(n-1,\max\!\left\{H, \left\lfloor4(n/100)^{2/9}\right\rfloor\right\}\right).',"exact frozen Bartlett-HAC bandwidth formula",[dict(source=bd,field="inference.bandwidth",native_value=b['inference']['bandwidth'])])
        self.passage('The added eight pairwise tests use only raw standard-normal two-sided DM-type working references,',"eight raw normal working references",[dict(source="results/revision-v8/wp5/summary.json",field="contrasts",transform="length=8; each dm.dm_p is raw normal"),dict(source=bd,field="inference")])

    def reviewed_roles(self):
        """Narrow current identities and a closed list of reviewed word meanings.

        These rules annotate only the matched word span, never an entire math
        line, so a newly inserted p-value cannot inherit a structural category.
        """
        old="notes/v7/s5-supplement-bindings.json"
        rules=[
            (r'two original primary comparisons', 'two retained primary tasks: FX and Treasury',old),
            (r'both errors','two residuals in the known-floor projection proof','notes/revision-v5-novelty/theory-source.json:/blocks/3'),
            (r'symmetric about zero|zero symmetry|atom at zero','symmetry center or atom of the proof distribution; mathematical assumption','reviewed Levy proof'),
            (r'first index','first crossing stopping index definition','reviewed Levy proof'),
            (r'one half','symmetry gives probability at least 1/2 at a positive or negative crossing','reviewed Levy proof'),
            (r'Two different failure mechanisms','two explicit constructions: dependence and one-sided substitution','notes/revision-v5-novelty/theory-source.json:/one_sided_substitution'),
            (r'endpoint is zero|maximum is one','Rademacher cancellation counterexample endpoint 0 and maximum 1','reviewed X1=Z, X2=-Z proof construction'),
            (r'one-sided endpoint','one-sided versus required absolute endpoint quantile definition','notes/revision-v5-novelty/theory-source.json:/one_sided_substitution'),
            (r'I/Zero|zero position','zero-initial-position experiment identity','results/revision-20261023/round2/levy/simulation.json'),
            (r'Zero observed counts|zero population probability|zero counts','zero observed hits versus unidentified population probability; recorded simulation table','results/revision-20261023/round2/levy-ar-correction/simulation.json'),
            (r'doubled-bandwidth','twice the recorded primary HAC bandwidth; sensitivity identity, not a new test','retained inference convention and existing HAC source fields'),
            (r'add-one rank','the specified empirical-quantile inclusive +1 rank convention','retained rank-ablation design and table'),
            (r'the two\s*$','two adjacent order-statistic reports at integral probability times pool size','retained empirical rank definition'),
            (r'four fixed headline comparisons','four full rows in the fixed-headline preference table','results/revision-20261022/preference-robustness/results.json'),
            (r'both mean error amounts|these two unconditional amounts','two loss components: unused allowance and positive overrun','results/revision-20261022/preference-robustness/results.json'),
            (r'first half|second half','layout partition of the complete panel into its first/second table, not a statistical half-sample','complete retained ordered panel rows'),
            (r'Four-predictor|four-predictor|four-feature|Four-feature|original four','four declared predictor coordinates; named procedure identity','protocol/revision-v8/wp5-fixed-prefix-design.json:/features/qr4_column_indices'),
            (r'one-standard-error|One-SE|one-SE','one recorded validation standard error in the named R2 selection rule','retained R6 selection contract'),
            (r'rank-zero','boundary rank convention issues known floor at zero rank','results/revision-20261023/v6/wp2-summary.json'),
            (r'coverage-first','selection-priority adjective; no cardinal count','retained wrapper selection convention'),
            (r'Two long-horizon wrapper cells','two saved NA wrapper rows, no values imputed','results/revision-20261023/v6/wp2-summary.json:/na_method_count'),
            (r'one constituent|than both','comparison of the two constituent reports in a combination','results/revision-20261023/v6/wp3-combinations.json'),
            (r'three state groups','three training-defined state labels low/mid/high','results/revision-20261023/v6/wp4-states.json:/rows/*/groups'),
            (r'one under the stated null','unit expectation bound of the nonnegative product under its stated null','retained e-value proof'),
            (r'On one nonempty historical episode set|on one side','single common historical pool required by the deterministic same-pool argument','reviewed common-pool distance proof'),
            (r'second inequality','reverse-direction inequality in the two-sided coordinatewise quantile bound','reviewed common-pool distance proof'),
            (r'both the target count','two clauses of the frozen screen fail: target count and outside exclusion','results/revision-v8/wp3/support.json:/procedures'),
            (r'all six loss, breach and','six saved displays: two procedures times three declared metrics','results/revision-v8/wp3/figures/display-receipt.json:/figures'),
            (r'Both regressions|two regressions','the two named procedures QR33 and QR4','protocol/revision-v8/wp3-mechanism-design.json:/methods'),
            (r'Three displayed overlapping/inspected windows|three inspected windows|third validation period','three reported window identities; no independent third sample created','results/revision-v8/wp5/three-window-summary.json:/rows/*/window_name'),
            (r'five-menu|three-menu','original procedure menu cardinalities; kept distinct from expanded menu','protocol/revision-v8/wp3-mechanism-design.json:/menus'),
            (r'first-release','historical release-vintage qualifier, not a cardinal count','explicit source/vintage limitation'),
        ]
        self.check(len(self.load('results/revision-v8/wp3/figures/display-receipt.json')['figures'])==6,'six_display_word_source')
        self.check(self.load('results/revision-20261023/v6/wp2-summary.json')['na_method_count']==2,'two_wrapper_NA_word_source')
        self.check(len(self.load('protocol/revision-v8/wp5-fixed-prefix-design.json')['features']['qr4_column_indices'])==4,'four_feature_word_source')
        self.check(len({r['window_name'] for r in self.load('results/revision-v8/wp5/three-window-summary.json')['rows']})==3,'three_window_word_source')
        for line in self.lines:
            for pattern,role,source in rules:
                for match in re.finditer(pattern,line['text'],re.I):
                    for word in WORDS.finditer(match.group()):
                        self.annotate(line['start']+match.start()+word.start(),line['start']+match.start()+word.end(),'reviewed_number_word',role=role,source=source)
            # Command path/label words carry no reader-visible count claim.
            for match in re.finditer(r'\\(?:input|include|label|ref|path)\{[^}]*\}',line['text']):
                for word in WORDS.finditer(match.group()):
                    self.annotate(line['start']+match.start()+word.start(),line['start']+match.start()+word.end(),'source_identifier_word',role='file or internal label identifier')
            if line['text'].strip()=='distinct fitted procedures (result codes QR33, QR4 and QR33+, respectively).':
                self.annotate(line['start'],line['start']+len(line['text']),'retained_named_identity',role='original QR33, QR4 and expanded-menu QR33+ procedure identities',source='retained panel typed fields and ordered full rows')
            if line['text'].strip()=='validation. R0 denotes the fixed minimum-validation-':
                self.annotate(line['start'],line['start']+len(line['text']),'retained_named_identity',role='R0 minimum-validation-loss selector identifier',source='retained R6 rule contract')
            if line['text'].startswith('Series & '+r'\shortstack{Horizon 6'):
                expected=r'Series & \shortstack{Horizon 6\\history 52} & \shortstack{Horizon 6\\history 260} & \shortstack{Horizon 24\\history 52} & \shortstack{Horizon 24\\history 260} \\'
                if line['text']==expected:
                    self.annotate(line['start'],line['start']+len(line['text']),'retained_task_header',role='ordered four horizon/history task identities: (6,52),(6,260),(24,52),(24,260)',source='same unchanged old ordered rows; 2 exact header rows in WP7 baseline')
            if line['file']==EXPECTED_INPUTS[3] and line['text'].startswith(r'\caption{H6 original regression across three inspected windows.'):
                m=re.search('6',line['text'])
                self.annotate(line['start']+m.start(),line['start']+m.end(),'table_task_identity',role='short horizon H=6 of each of the six exact source-bound rows',source='results/revision-v8/wp5/three-window-summary.json:/rows/*/horizon')
            if line['text'].startswith('The v7 merge preserves canonical supervisor scripts'):
                m=re.search('7',line['text']); self.annotate(line['start']+m.start(),line['start']+m.end(),'document_version',role='historical v7 merge/archive identity')

    def locate_new_contract(self):
        """Locate every one of the 2080 bindings, including non-MC prose fields."""
        rows=self.load('notes/revision-v8/wp7-supplement-integration.json')['bindings']
        by_index=defaultdict(list)
        for a,b,category,ev in self.annotations:
            if category!='located_mc_cell_field':continue
            for i,row in enumerate(rows[:2016]):
                ptr='/'+'/'.join(str(v).replace('~','~0').replace('/','~1') for v in row['field_tokens'])
                if ev['source']==row['source'] and ev['pointer']==ptr:by_index[i].append((a,b))
        # Ordered token slots refer to uniquely matched whole sentences above.
        # None slots are separately reviewed equation/design constants.
        slots={
            'exact DGP grids':list(range(2030,2042)),
            'GARCH parameter triples':list(range(2016,2025)),
            'burn and retained lengths':[2042,2043],
            'exact integer repetition/entropy':[2044,2045],
            'MC issue calendar':[2046,2047,2048,2049,None,2050],
            'worst-case win MC error':[None,2029],
            'complete frozen support-screen counts and design':[2044,None,None,None,None,None,None,2051,2052,2053,2054,2055],
            'candidate/procedure failure identity':[2028,2056,2057,2058,2059,2060,2061,2062,2025,2027,2026],
            'actual completed-day source count':[2063],
            'daily dates and common issue count':[None]*12+[2064],
            'signed daily exception and breaches':[2065,2066,2067],
            'full-prefix inclusive indices and count':[2075,2076,2077],
            'later-selected original penalties by procedure and horizon':[None,2071,None,2072,None,2073,None,2074],
            'old nested backcast count and exact index range':[2068,2078,2079],
            'actual old longer-horizon target coverage':[2069,2070],
        }
        for role,indices in slots.items():
            passages=[p for p in self.locations if p['role']==role]
            if len(passages)!=1:continue
            passage=passages[0]
            found=list(TOKEN.finditer(self.text,passage['start'],passage['end']))
            if not self.check(len(found)==len(indices),'new_binding_slot_count',role=role,actual=len(found),expected=len(indices)):continue
            for token,index in zip(found,indices):
                if index is None:continue
                row=rows[index]
                a,b=token.span()
                # TeX's -- is a range dash, not the sign of its upper endpoint;
                # a full stop immediately after an integer ends the sentence.
                if self.text[a:a+1]=='-' and a and self.text[a-1]=='-':a+=1
                if self.text[a:b].endswith('.') and row['rendered'].isdigit():b-=1
                printed=self.text[a:b]
                if self.check(printed==row['rendered'],'new_located_display',binding_index=index,role=role,actual=printed,expected=row['rendered']):
                    by_index[index].append((a,b))
                    self.annotate(a,b,'located_new_contract_field',binding_index=index,source=row['source'],field=row['field'],field_tokens=row['field_tokens'],native_value=row['original_value'],format=row['format'],scale=row['scale'],printed=printed,lexical_token=token.group(),role=role)
        for index,row in enumerate(rows):
            self.check(bool(by_index[index]),'new_binding_occurrence_missing',binding_index=index,source=row['source'],field=row['field'])
            locations=[]
            for a,b in by_index[index]:
                origin=next(line for line in reversed(self.lines) if line['start']<=a)
                locations.append(dict(file=origin['file'],line=origin['line'],column=a-origin['start']+1,printed=self.text[a:b]))
            self.contract_locations.append(dict(binding_index=index,**row,locations=locations))

    def inventory(self):
        tokens, words = [], []
        for line in self.lines:
            for match in TOKEN.finditer(line['text']):
                start,end=line['start']+match.start(),line['start']+match.end()
                bound=[(b-a,cat,ev) for a,b,cat,ev in self.annotations if a<=start and end<=b]
                bound.sort(key=lambda x:x[0])
                category,evidence=(bound[0][1],bound[0][2]) if bound else (None,{})
                if category is None:
                    # Syntax roles are narrowed to actual commands. Math mode by
                    # itself is deliberately NEVER an escape for unbound results.
                    text=line['text']; token=match.group()
                    if any(a<=match.start()<b for a,b in layout_spans(text)):
                        category='layout_setting'; evidence={'role':'explicit TeX dimension, array stretch, font size or image-width setting'}
                    elif any(m.start()<=match.start()<m.end() for m in re.finditer(r'\\(?:input|include|label|ref|path)\{[^}]*\}|\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}|\\(?:href|url)\{[^}]*\}',text)):
                        category='source_identifier'; evidence={'role':'current input path, source archive URL, label or file identifier; input bytes independently inventoried'}
                    elif token in ('7','8') and match.start()>0 and text[match.start()-1]=='v' and (re.fullmatch(r'The v[78] merge preserves both source lines\..*',text.strip()) or 'v8 manuscript' in text):
                        category='document_version';evidence={'role':'document/archive version identifier, not an empirical count'}
                record=dict(file=line['file'],line=line['line'],column=match.start()+1,token=match.group(),context=line['text'],category=category or 'UNRESOLVED',evidence=evidence)
                tokens.append(record)
            for match in WORDS.finditer(line['text']):
                word=match.group(); start,end=line['start']+match.start(),line['start']+match.end()
                bound=[(b-a,cat,ev) for a,b,cat,ev in self.annotations if a<=start and end<=b]
                bound.sort(key=lambda x:x[0])
                ev=bound[0][2] if bound else {}
                words.append(dict(file=line['file'],line=line['line'],column=match.start()+1,word=word,context=line['text'],category=bound[0][1] if bound else 'WORD_REVIEW_PENDING',evidence=ev))
        return tokens,words

    def run(self):
        self.expand(); self.prepare_offsets()
        self.check(Counter(self.inputs)==Counter(EXPECTED_INPUTS),'required_generated_inputs',expected=list(EXPECTED_INPUTS),actual=self.inputs)
        old=self.old_sources(); self.old_rows_and_occurrences(old)
        self.new_fields(); self.mc_tables(); self.copied_tables(); self.new_prose(); self.reviewed_roles(); self.locate_new_contract()
        tokens,words=self.inventory()
        unresolved=[r for r in tokens if r['category']=='UNRESOLVED']+[r for r in words if r['category']=='WORD_REVIEW_PENDING']
        sources=set(self.cache)
        sources.update(self.load('notes/v7/s5-supplement-bindings.json')['source_sha256'])
        sources.update(self.load('notes/revision-v8/wp7-supplement-integration.json')['source_hashes'])
        sources.update(row['path'] for row in self.load('results/revision-v8/wp5/three-window-bindings.json')['old_source_bindings'])
        source_inventory={name:dict(sha256=digest(self.path(name)),bytes=self.path(name).stat().st_size) for name in sorted(sources)}
        return dict(generated_utc=datetime.now(timezone.utc).isoformat(),status='NEEDS_REVIEW' if self.failures or unresolved or self.ambiguous else 'PASS_WITH_SCOPE_LIMITS',scope='Current Supplement TeX and all five recursively included v8 tables; public saved-field/identity/display audit only',files=self.files,source_inventory=source_inventory,recursive_inputs=self.inputs,counts=dict(self.raw_counts),numeric_occurrences=len(tokens),number_word_occurrences=len(words),category_counts=dict(Counter(r['category'] for r in tokens)),word_category_counts=dict(Counter(r['category'] for r in words)),failures=self.failures,unresolved=unresolved,ambiguous=self.ambiguous,tokens=tokens,number_words=words,located_passages=self.locations,new_contract_occurrence_ledger=self.contract_locations,limits=['This is software/document validation, not a new financial experiment or independent forecasting replication.','Included figure pixels/annotations and current PDF compilation/page identity are separately verified by the parent WP8 workflow.','References/source identifiers are classified with their actual role; independent bibliographic verification remains a separate gate.','Source-level occurrence location does not prove rendered row placement, glyph visibility or legibility; final page-by-page visual QA remains required.'],new_financial_tests=0,new_models=0,raw_private_inputs_read=0)


def audit(root=ROOT, document_root=None):
    return Audit(root,document_root).run()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--document-root',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=audit(args.root,args.document_root)
    output=args.output or args.root/'notes/revision-v8/wp8-supp-number-check.json'
    if not output.name.startswith('wp8-supp-'):
        raise ValueError('output must use the assigned wp8-supp- prefix')
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('status','counts','numeric_occurrences','number_word_occurrences')}|{'failures':len(result['failures']),'unresolved':len(result['unresolved']),'ambiguous':len(result['ambiguous']),'output':str(output)},indent=2))
    return 0 if result['status']=='PASS_WITH_SCOPE_LIMITS' else 1


if __name__=='__main__':
    raise SystemExit(main())
