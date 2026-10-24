#!/usr/bin/env python3
"""Focused read-only v8 submission-package check; explicit new JSON output.

No compilation, model import, experiment, Git operation or package mutation.
--source-only skips PDFs, snapshots and ZIP while those are being refreshed.
Full mode requires pypdf and a saved compile receipt binding current sources
to the delivered native PDFs. Existing output files are never overwritten.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "submission-jof"
PLACEHOLDER = "[TO BE COMPLETED BY AUTHOR]"
KEYWORDS = ("Peak net positions", "Quantile forecasting", "Historical benchmarks",
            "Forecast comparison", "Calibration", "Dealer positions")
RUNNING_TITLE = "Historical Rules and Peak Limits"
FIGURES = {
    "figures/v8-endpoint-peak-example.pdf", "figures/v7-murphy-fx_hourly.pdf",
    "figures/v7-murphy-nyfed_weekly.pdf", "figures/v8-calibrated-mc.pdf",
}
REQUIRED_SOURCES = {"main.tex", "manuscript.tex", "supplement.tex", "title-page.tex",
                    "references.bib", "README.md", "AUTHOR-TODO.md", "cover-letter.md"} | FIGURES
WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?(?:[-‐‑][A-Za-z0-9]+)*|(?<![A-Za-z])\d+(?:,\d{3})*(?:\.\d+)?(?:[-‐‑][A-Za-z]+)*")
NUM = re.compile(r"(?<![A-Za-z0-9])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?|(?<![A-Za-z0-9])[-+−]?\.\d+")
PLACEHOLDER_FIELDS = {
    "manuscript.tex": ("Author information", "ORCID", "Funding", "Competing interests", "AI statement"),
    "title-page.tex": ("Authors and affiliations", "Corresponding author and contact", "ORCID", "Funding", "Conflict of interest", "AI statement"),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def plain(text):
    text = text.replace(r"\%", "%").replace(r"\&", "&").replace("~", " ")
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", text)
    return re.sub(r"\s+", " ", re.sub(r"[{}$\\]", " ", text)).strip()


def compact(text):
    return re.sub(r"\s+", "", text).replace("−", "-").replace("–", "-")


class Audit:
    def __init__(self):
        self.assertions = 0
        self.failures = []
        self.hashes = {}

    def check(self, condition, category, detail):
        self.assertions += 1
        if not condition:
            self.failures.append({"category": category, "detail": detail})

    def read(self, name):
        raw = (PACKAGE / name).read_bytes()
        self.hashes[name] = sha(raw)
        return raw.decode("utf-8")


def region(text, start, end):
    begin = text.index(start) + len(start)
    return text[begin:text.index(end, begin)]


def keyword_list(text):
    matches = [plain(line) for line in text.splitlines() if re.search(r"\bKeywords\b", line, re.I)]
    if len(matches) != 1:
        return []
    value = re.split(r"\bKeywords\b\s*[:.]?\s*", matches[0], maxsplit=1, flags=re.I)[-1]
    return [item.strip().rstrip(".") for item in re.split(r"[;,]", value) if item.strip()]


def refs_and_cites(audit, name, tex):
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    refs = re.findall(r"\\(?:ref|eqref|pageref)\{([^}]+)\}", tex)
    bib = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    cites = [key.strip() for group in re.findall(r"\\cite(?:p|t|alp|author|year)?(?:\[[^\]]*\]){0,2}\{([^}]+)\}", tex)
             for key in group.split(",")]
    audit.check(not [key for key, count in Counter(labels).items() if count > 1], "unique_labels", name)
    audit.check(set(refs) <= set(labels), "all_local_refs_resolve", {"file": name, "missing": sorted(set(refs) - set(labels))})
    audit.check(set(cites) <= set(bib), "all_native_citations_resolve", {"file": name, "missing": sorted(set(cites) - set(bib))})
    return {"labels": len(labels), "references": len(refs), "citations": len(cites), "bibitems": len(bib)}


def source_checks(audit, abstract_source):
    texts = {name: audit.read(name) for name in ("main.tex", "manuscript.tex", "supplement.tex", "title-page.tex", "cover-letter.md", "README.md", "AUTHOR-TODO.md")}
    main, supp, title = texts["manuscript.tex"], texts["supplement.tex"], texts["title-page.tex"]
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", main, re.S).group(1)
    supplied = json.loads((ROOT / abstract_source).read_text())["abstract"]
    audit.check(re.sub(r"\s+", " ", abstract).strip() == re.sub(r"\s+", " ", supplied).strip(), "abstract_matches_provided_source", abstract_source)
    abstract_words, abstract_numbers = len(WORD.findall(plain(abstract))), len(NUM.findall(plain(abstract)))
    audit.check(abstract_words <= 170, "abstract_word_budget", abstract_words)
    audit.check(abstract_numbers <= 10, "abstract_numeric_budget", abstract_numbers)
    intro = region(main, r"\section{Introduction}\label{sec:intro}", r"\section{Related literature}")
    related = region(main, r"\section{Related literature}\label{sec:literature}", r"\section{The forecast target}")
    conclusion = region(main, r"\section{Conclusion}\label{sec:conclusion}", r"\section*{Data and code availability}")
    for ordinal in ("First", "Second", "Third"):
        audit.check(len(re.findall(r"\\textit\{" + ordinal + r",", intro)) == 1, "exact_three_intro_findings", ordinal)
    body = main.split(r"\begin{thebibliography}", 1)[0]
    audit.check(not re.search(r"\bC[123]\b", body), "no_C_contribution_tags", "main body")
    footprints = {}
    for name, passage in (("abstract", abstract), ("introduction", intro), ("section2", related), ("conclusion", conclusion), ("cover_letter", texts["cover-letter.md"])):
        values = set(NUM.findall(plain(passage)))
        facts = {"FX_two_period_gains": {"14.8", "16.6"} <= values,
                 "weekly_34_of_48": {"34", "48"} <= values,
                 "matched_unwrapped_376_vs_360": {"376", "360"} <= values}
        for finding, present in facts.items():
            audit.check(present, "five_location_numeric_footprint", {"location": name, "finding": finding})
        footprints[name] = facts
    keywords = {name: keyword_list(texts[name]) for name in ("manuscript.tex", "title-page.tex")}
    for name, values in keywords.items():
        audit.check(0 < len(values) <= 6, "keyword_limit", {"file": name, "keywords": values})
        audit.check(tuple(values) == KEYWORDS, "requested_keywords", {"file": name, "keywords": values})
    audit.check(keywords["manuscript.tex"] == keywords["title-page.tex"], "keyword_synchronization", keywords)
    running = [plain(line).split("Running title:", 1)[-1].strip() for line in title.splitlines() if "Running title:" in line]
    audit.check(len(running) == 1 and running[0] == RUNNING_TITLE and len(running[0]) <= 40, "running_title", running)
    placeholder_counts = {}
    for name, fields in PLACEHOLDER_FIELDS.items():
        tex = texts[name]
        placeholder_counts[name] = tex.count(PLACEHOLDER)
        audit.check(tex.count(PLACEHOLDER) == len(fields), "B0_placeholder_count_preserved", {"file": name, "expected": len(fields), "actual": tex.count(PLACEHOLDER)})
        for field in fields:
            audit.check(tex.count(field + ": " + PLACEHOLDER + ".") == 1, "B0_placeholder_field_text_preserved", {"file": name, "field": field})
    placeholder_counts["cover-letter.md"] = texts["cover-letter.md"].count(PLACEHOLDER)
    audit.check(placeholder_counts["cover-letter.md"] == 1 and texts["cover-letter.md"].rstrip().endswith(PLACEHOLDER), "cover_author_placeholder_preserved", placeholder_counts["cover-letter.md"])
    audit.check(supp.count(PLACEHOLDER) == 0, "B0_supplement_placeholder_count", supp.count(PLACEHOLDER))
    audit.check(PLACEHOLDER in texts["AUTHOR-TODO.md"], "author_completion_reminder_retained", "AUTHOR-TODO.md")
    links = {name: refs_and_cites(audit, name, texts[name]) for name in ("manuscript.tex", "supplement.tex", "title-page.tex")}
    sections = list(re.finditer(r"\\section\{[^{}]*\}", supp))
    section_number = None
    for number, match in enumerate(sections, 1):
        stop = sections[number].start() if number < len(sections) else len(supp)
        if r"\label{sup:v8-calibrated}" in supp[match.end():stop]:
            section_number = number
    # Iterate full blocks, not captured environment names, to bind the caption order.
    table_numbers = {}
    captioned_tables = [match.group() for match in re.finditer(r"\\begin\{(table\*?|longtable)\}.*?\\end\{\1\}", supp, re.S) if r"\caption" in match.group()]
    for number, block in enumerate(captioned_tables, 1):
        for label in ("tab:v8-mc-loss", "tab:v8-mc-predictions"):
            if r"\label{" + label + "}" in block:
                table_numbers[label] = number
    audit.check(section_number == 26, "supplement_calibrated_section_S26", section_number)
    audit.check(table_numbers.get("tab:v8-mc-loss") == 29, "supplement_main_grid_loss_table_S29", table_numbers.get("tab:v8-mc-loss"))
    audit.check(table_numbers.get("tab:v8-mc-predictions") == 32, "supplement_prediction_table_S32", table_numbers.get("tab:v8-mc-predictions"))
    audit.check("Supplement Table~S32" in main or "Supplement Table S32" in main, "main_names_actual_MC_table", "S32")
    figure_names = set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", main))
    audit.check(figure_names == FIGURES, "four_current_main_figures", sorted(figure_names))
    for name in REQUIRED_SOURCES:
        audit.check((PACKAGE / name).is_file(), "required_source_file", name)
    mc_original = ROOT / "results/v8/mc/mc-main.pdf"
    audit.check(mc_original.is_file() and (PACKAGE / "figures/v8-calibrated-mc.pdf").read_bytes() == mc_original.read_bytes(), "MC_figure_matches_saved_result", "v8-calibrated-mc.pdf")
    audit.check(r"\input{manuscript.tex}" in texts["main.tex"], "default_main_entry", "main.tex")
    audit.check("v8" in texts["README.md"].lower() and not texts["README.md"].startswith("# Current v7"), "README_current_version", "README.md")
    return texts, {"abstract_words": abstract_words, "abstract_numbers": abstract_numbers,
                   "five_location_footprints": footprints, "keywords": keywords,
                   "running_title": running, "placeholder_counts": placeholder_counts,
                   "references_and_citations": links, "supplement_section": section_number,
                   "supplement_MC_tables": table_numbers, "main_figures": sorted(figure_names)}


def full_checks(audit, texts, compile_receipt):
    from pypdf import PdfReader
    receipt = json.loads((ROOT / compile_receipt).read_text())
    documents = receipt["documents"]
    pdfs = {}
    names = ["manuscript", "supplement", "title-page"]
    if (PACKAGE / "cover-letter.tex").exists() or (PACKAGE / "cover-letter.pdf").exists():
        names.append("cover-letter")
    for name in names:
        tex_name, pdf_name = name + ".tex", name + ".pdf"
        source_raw = (PACKAGE / tex_name).read_bytes()
        pdf_raw = (PACKAGE / pdf_name).read_bytes()
        reader = PdfReader(PACKAGE / pdf_name)
        producer = str((reader.metadata or {}).get("/Producer", ""))
        pages = len(reader.pages)
        proof = documents[name]
        audit.check(proof["source_sha256"] == sha(source_raw), "compiled_current_source", tex_name)
        audit.check(proof["pdf_sha256"] == sha(pdf_raw), "compiled_delivered_PDF", pdf_name)
        audit.check(proof["pages"] == pages and proof["producer"] == producer, "compile_receipt_PDF_metadata", pdf_name)
        audit.check(bool(re.search(r"xdvipdfmx|pdftex|xetex|luatex|luahbtex", producer, re.I)), "native_LaTeX_PDF_producer", {"file": pdf_name, "producer": producer})
        if name == "manuscript":
            audit.check(0 < pages <= 18, "main_page_budget", pages)
        elif name in ("title-page", "cover-letter"):
            audit.check(pages == 1, "one_page_document", {"name": name, "pages": pages})
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        audit.check("??" not in text, "no_unresolved_PDF_refs", pdf_name)
        if name == "supplement":
            audit.check("S26Calibratedsimulation" in compact(text), "compiled_S26_heading", pdf_name)
            audit.check("TableS29" in compact(text), "compiled_S29_loss_table", pdf_name)
            audit.check("TableS32" in compact(text), "compiled_S32_table", pdf_name)
        if name != "cover-letter":
            alias = name + "-preview.pdf"
            audit.check((PACKAGE / alias).read_bytes() == pdf_raw, "PDF_preview_alias_identity", alias)
        pdfs[name] = {"pages": pages, "producer": producer, "pdf_sha256": sha(pdf_raw), "source_sha256": sha(source_raw)}
    snapshots = {}
    for name in ("manuscript", "supplement"):
        filename = name + "-content.json"
        raw = (PACKAGE / filename).read_bytes()
        data = json.loads(raw)
        source = texts[name + ".tex"]
        checks = {"schema": data.get("schema") == "v8-latex-snapshot",
                  "canonical_source": data.get("canonical_source") == name + ".tex",
                  "source_sha256": data.get("source_sha256") == sha(source.encode()),
                  "latex": data.get("latex") == source,
                  "source_bindings_array": isinstance(data.get("source_bindings"), list),
                  "historical_v6_schema_retained": "historical_v6_schema" in data}
        for item, passed in checks.items():
            audit.check(passed, "current_content_JSON", {"file": filename, "field": item})
        for relative in data.get("source_bindings", []) if isinstance(data.get("source_bindings"), list) else []:
            # Snapshot paths are relative to the JSON's package directory,
            # like canonical_source; ../notes/ points back into this repo.
            ledger = (PACKAGE / relative).resolve() if isinstance(relative, str) else None
            audit.check(ledger is not None and ledger.is_relative_to(ROOT.resolve()) and ledger.is_file(),
                        "snapshot_binding_ledger_exists", {"snapshot": filename, "ledger": relative})
        snapshots[filename] = {"sha256": sha(raw), "checks": checks}
    zip_result = {}
    with zipfile.ZipFile(PACKAGE / "overleaf-package.zip") as archive:
        members = archive.namelist()
        audit.check(len(members) == len(set(members)), "ZIP_unique_members", members)
        audit.check(REQUIRED_SOURCES <= set(members), "ZIP_all_required_sources", sorted(REQUIRED_SOURCES - set(members)))
        archive_figures = {name for name in members if name.startswith("figures/") and not name.endswith("/")}
        audit.check(archive_figures == FIGURES, "ZIP_only_four_current_figures", sorted(archive_figures))
        for member in members:
            if member.endswith("/"):
                continue
            path = PACKAGE / member
            audit.check(path.is_file() and archive.read(member) == path.read_bytes(), "ZIP_member_matches_current_package", member)
            if member.endswith(".tex"):
                tex = archive.read(member).decode()
                for target in re.findall(r"\\(?:input|include)\{([^}]+)\}", tex):
                    name = str(Path(member).parent / target)
                    if not name.endswith(".tex"):
                        name += ".tex"
                    audit.check(name in members, "ZIP_self_contained_TeX_input", {"file": member, "input": name})
                for target in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex):
                    name = str(Path(member).parent / target)
                    audit.check(name in members or name + ".pdf" in members, "ZIP_self_contained_figure_input", {"file": member, "input": name})
        zip_result = {"members": members, "sha256": sha((PACKAGE / "overleaf-package.zip").read_bytes())}
    return {"compiled_documents": pdfs, "content_snapshots": snapshots, "overleaf_package": zip_result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-only", action="store_true")
    parser.add_argument("--abstract-source", default="notes/v8/b3-prose.json")
    parser.add_argument("--compile-receipt", default="notes/v8/package-compilation.json")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.exists():
        raise SystemExit("Output exists; refusing overwrite: " + str(output))
    audit = Audit()
    result = {"mode": "source-only" if args.source_only else "full"}
    try:
        texts, source = source_checks(audit, args.abstract_source)
        result["source_checks"] = source
        if not args.source_only:
            result.update(full_checks(audit, texts, args.compile_receipt))
    except Exception as exc:
        audit.check(False, "readback_exception", {"type": type(exc).__name__, "message": str(exc)})
    result.update(status="PASS" if not audit.failures else "FAIL", assertions=audit.assertions,
                  failure_count=len(audit.failures), failures=audit.failures, source_sha256=audit.hashes,
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  limitations=["Numeric footprints check presence of the three finding groups; the separate contribution review owns claim/reference semantics.",
                               "B0 author placeholder preservation uses the observed original five main fields, six title fields, one cover signature and zero supplement placeholders.",
                               "Source-only mode intentionally skips PDF provenance, aliases, refreshed content snapshots and ZIP acceptance.",
                               "This checker compiles nothing; full mode requires the root's current-source compile receipt and actual PDF metadata.",
                               "No Git state, raw data, forecast, scientific result or submission is changed."])
    with output.open("x") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({name: result[name] for name in ("status", "mode", "assertions", "failure_count", "failures")}, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
