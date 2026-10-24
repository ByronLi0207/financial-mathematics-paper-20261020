"""Check the delivered TeX/PDF, prose counts and preservation of baseline files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import re
import subprocess
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
DOC = ROOT / "manuscript/supervisor-revision"
OUT = ROOT / "results/supervisor-20261023/document-verification.json"
BASE = "65feeee801b6b228a608ca3200e0678bb5f62b1c"


def prose(text):
    text = re.sub(r"\\begin\{(equation|align|figure|center)\}.*?\\end\{\1\}", " ", text, flags=re.S)
    text = re.sub(r"\\(?:subsection|section)\{[^}]*\}[^\n]*\n", "\n", text)
    text = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:citep|citet|ref|label|eqref|input)\{[^}]*\}", " ", text)
    text = re.sub(r"\$.*?\$", " ", text)
    text = text.replace(r"\%", "%")
    text = re.sub(r"\\[A-Za-z]+\*?", " ", text).replace("{", "").replace("}", "").replace("~", " ")
    return re.sub(r"\s+", " ", text).strip()


def negative_counts(text, protect_decimal_points=False):
    if protect_decimal_points:
        text = re.sub(r"(?<=\d)\.(?=\d)|(?<=et al)\.|(?<=e\.g)\.", "\u241f", text)
    pieces = [s.strip() for s in text.split(".") if s.strip()]
    core = [s for s in pieces if re.search(r"\b(?:not|no|neither|nor|cannot)\b", s, re.I)]
    expanded = [s for s in pieces if re.search(r"\b(?:not|no|neither|nor|cannot|without)\b|\brather\s+than\b", s, re.I)]
    return dict(period_segments=len(pieces), core_negative_segments=len(core),
                core_percent=100*len(core)/len(pieces), expanded_negative_segments=len(expanded),
                expanded_percent=100*len(expanded)/len(pieces))


def main():
    baseline = json.loads((ROOT / "manuscript/working-paper/paper-content.json").read_text())
    before = " ".join(html.unescape(re.sub("<[^>]+>", " ", b["html"]))
                      for section in baseline["sections"] if not section["title"].startswith("Appendix")
                      for b in section["blocks"] if b["type"] == "p")
    sections = (DOC / "sections.tex").read_text()
    expanded = sections.replace(r"\input{generated/e3-summary.tex}", (DOC / "generated/e3-summary.tex").read_text())
    after = prose(expanded)
    counts = {"literal_period": {"before": negative_counts(before), "after": negative_counts(after)},
              "decimal_abbreviation_protected": {"before": negative_counts(before, True), "after": negative_counts(after, True)}}
    abstract = prose((DOC / "abstract.tex").read_text())
    conclusion = prose(sections.split(r"\section{Conclusion}", 1)[1])
    reader = PdfReader(DOC / "main.pdf")
    page_text = [p.extract_text() for p in reader.pages]
    first_appendix = next(i for i, t in enumerate(page_text) if re.search(r"^A\s+Finite geometry and parameterization", t))
    c_pages = [i+1 for i, t in enumerate(page_text) if "C Reproducibility and technical supplement" in t]
    assert len(c_pages) == 1
    assert first_appendix <= 14 and len(reader.pages)-first_appendix <= 6
    assert len(abstract.split()) <= 180 and len(conclusion.split()) <= 200
    assert counts["literal_period"]["after"]["core_percent"] < 12
    assert counts["decimal_abbreviation_protected"]["after"]["core_percent"] < 12
    forbidden = r"commit hash|SHA-256|\bRSS\b|\bthreads?\b|\b\d+(?:\.\d+)?\s+seconds?\b|byte-identical|\breceipt\b|\bphase\b|accepted snapshot|Consulted body"
    assert not re.search(forbidden, after, re.I)
    assert reader.metadata.get("/Author") == "Byron"
    assert "xdvipdfmx" in reader.metadata.get("/Producer", "")
    assert sum(r"\section{" in line for line in sections.splitlines()) == 9
    refs = (DOC / "references.tex").read_text()
    citations = set(k.strip() for group in re.findall(r"\\cite[pt]\{([^}]*)\}", sections+(DOC/"appendices.tex").read_text()) for k in group.split(","))
    bibkeys = set(re.findall(r"\\bibitem\[[^]]*\]\{([^}]*)\}", refs))
    assert citations == bibkeys, (citations-bibkeys, bibkeys-citations)
    changed = set(subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines())
    old = set(subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT, text=True).splitlines())
    protected_changes = sorted((changed & old)-{"README.md"})
    assert not protected_changes, protected_changes
    e3 = json.loads((ROOT/"results/supervisor-20261023/e3/verification.json").read_text())
    inference = json.loads((ROOT/"results/supervisor-20261023/inference/audit-receipt.json").read_text())
    assert e3["status"] == "PASS" and e3["complete_cells"] == 8 and e3["declared_candidate_count"] == 40
    assert inference["matched_holm_family_size"] == 72 and inference["dm_contrasts"] == 74
    pdf = DOC/"main.pdf"
    result = dict(status="PASS", checked_utc=datetime.now(timezone.utc).isoformat(), baseline=BASE,
                  page_count=len(reader.pages), main_including_references_pages=first_appendix,
                  appendix_pages=len(reader.pages)-first_appendix, appendix_C_physical_pages=c_pages,
                  abstract_words=len(abstract.split()), conclusion_words=len(conclusion.split()),
                  word_count_rule="Whitespace tokens after removing TeX commands; hyphenated compounds count once.",
                  negative_sentence_counts=counts,
                  negative_count_scope="Narrative paragraphs only: old sections1-11 versus new sections1-9; includes generated E3 prose. Excludes abstract, math, tables, captions, headings, references and appendices.",
                  period_rule="Literal '.' split as requested. A second reported rule protects decimal points and et al./e.g. abbreviations before the same split. Case-insensitive whole-word negative terms.",
                  used_reference_count=len(bibkeys), main_forbidden_terms_found=False,
                  baseline_tracked_file_count=len(old), protected_baseline_changes=protected_changes,
                  pdf_producer=reader.metadata.get("/Producer"), pdf_author=reader.metadata.get("/Author"),
                  pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), pdf_bytes=pdf.stat().st_size,
                  inference_status=inference["status"], e3_status=e3["status"],
                  independent_visual_review="All17 pages inspected; Figure1 issue annotation corrected and changed page rechecked. See document-qa.md.")
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
