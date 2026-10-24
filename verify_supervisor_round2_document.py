"""Verify the actual second-revision document and its frozen result contracts.

Run with the existing bundled Python/pypdf environment after the final test and
page-review receipts exist. No model, build, test or visual review is performed.
Only a new, exclusive round2/document-verification.json is written on success.
"""
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import subprocess
import unicodedata

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "manuscript/supervisor-revision"
RESULTS = ROOT / "results/supervisor-20261023"
ROUND2 = RESULTS / "round2"
OUT = ROUND2 / "document-verification.json"
BASE = "a2020e68dabab5b0e7dde5add1a3647162d03acc"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def rows(path):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def prose(text):
    text = re.sub(r"(?m)(?<!\\)%.*$", "", text)
    text = re.sub(r"\\(?:cite[pt]?|ref|eqref|label)\{[^}]*\}", " ", text)
    text = re.sub(r"\\(?:section|subsection)\{[^}]*\}", " ", text)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = text.replace(r"\%", "%").replace("~", " ")
    text = re.sub(r"\\[A-Za-z]+\*?", " ", text)
    return re.sub(r"\s+", " ", text.replace("{", "").replace("}", "")).strip()


def normalized(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    # Undo the observed TeX line-wrap hyphenation in historical/observations.
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def include_tex(path):
    """Expand the document's existing local input directives for citation checks."""
    return re.sub(r"\\input\{([^}]+)\}",
                  lambda match: include_tex(DOC / match.group(1)),
                  Path(path).read_text())


def verify_document():
    main = (DOC / "main.tex").read_text()
    sections = (DOC / "sections.tex").read_text()
    facts = read_json(ROUND2 / "numerical-facts.json")
    fact_tex = (DOC / "generated/round2-facts.tex").read_text()
    macros = dict(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}\{([^\n]*)\}", fact_tex))
    require(set(macros) == set(facts), "Generated empirical fact/macro names differ")
    fact_sources = {}
    for name, record in facts.items():
        path = ROOT / record["source"]
        digest = sha(path)
        require(digest == record["source_sha256"], "Fact source hash changed: " + name)
        require(macros[name] == record["display"], "Fact display differs: " + name)
        fact_sources[record["source"]] = digest

    def expand(text):
        for name, display in macros.items():
            text = re.sub(r"\\" + name + r"(?:\{\})?(?![A-Za-z])",
                          lambda _match, value=display: value, text)
        return text

    abstract = prose(expand((DOC / "abstract.tex").read_text()))
    conclusion = prose(expand(sections.split(r"\section{Conclusion}", 1)[1]))
    require(len(abstract.split()) <= 180, "Abstract exceeds 180 expanded prose words")
    require(150 <= len(conclusion.split()) <= 200,
            "Conclusion is outside 150-200 expanded prose words")
    require(len(re.findall(r"(?m)^\\section\{", sections)) == 10,
            "Main text must have ten sections")
    body_tex = include_tex(DOC / "abstract.tex") + include_tex(DOC / "sections.tex") + include_tex(DOC / "appendices.tex")
    used = {key.strip() for group in re.findall(
        r"\\cite[pt]?(?:\[[^]]*\]){0,2}\{([^}]*)\}", body_tex) for key in group.split(",")}
    bibkeys = set(re.findall(r"\\bibitem\[[^]]*\]\{([^}]*)\}", (DOC / "references.tex").read_text()))
    require(used == bibkeys and len(bibkeys) == 25,
            "Used citation keys must equal the 25 bibliography keys")
    require(r"\input{generated/round2-facts.tex}" in main,
            "Main document does not load its generated numerical facts")
    pdf = DOC / "main.pdf"
    reader = PdfReader(pdf)
    texts = [page.extract_text() or "" for page in reader.pages]
    appendix = [i for i, text in enumerate(texts)
                if re.search(r"(?:^|\n)A\s+Finite geometry and parameterization", text)]
    require(len(appendix) == 1, "Cannot uniquely locate the actual appendix start")
    first = appendix[0]
    require(first <= 14 and len(texts) - first <= 5,
            "Actual PDF exceeds main/reference or appendix page budget")
    require(reader.metadata.get("/Author") == "Byron", "PDF author is not Byron")
    require("xdvipdfmx" in reader.metadata.get("/Producer", ""),
            "PDF is not the compiled xdvipdfmx document")
    pdf_abstract = texts[0].split("Abstract", 1)[1].split("Keywords:", 1)[0]
    require(normalized(pdf_abstract) == normalized(abstract),
            "Actual PDF abstract differs from expanded TeX")
    full = "\n".join(texts[:first])
    pdf_conclusion = re.split(r"10\s+Conclusion", full, maxsplit=1)[1].split("References", 1)[0]
    # Physical page numbers are separate lines; they are not conclusion words.
    pdf_conclusion = re.sub(r"(?m)^\s*\d+\s*$", "", pdf_conclusion)
    require(normalized(pdf_conclusion) == normalized(conclusion),
            "Actual PDF conclusion differs from expanded TeX")
    require("??" not in full and "[?]" not in full, "Unresolved PDF cross-reference")
    return dict(page_count=len(texts), main_including_references_pages=first,
                appendix_pages=len(texts)-first, appendix_first_physical_page=first+1,
                abstract_words=len(abstract.split()), conclusion_words=len(conclusion.split()),
                word_count_rule="Whitespace tokens in prose after expanding round2-facts macros; hyphenated compounds count once.",
                main_section_count=10, used_reference_count=len(bibkeys),
                empirical_fact_count=len(facts), fact_source_sha256=fact_sources,
                pdf_author=reader.metadata.get("/Author"), pdf_producer=reader.metadata.get("/Producer"),
                pdf_sha256=sha(pdf), pdf_bytes=pdf.stat().st_size)


def verify_results():
    e6 = read_json(RESULTS / "e6/verification.json")
    e6_numeric = read_json(RESULTS / "e6/numeric-readback.json")
    require(e6["status"] == e6_numeric["status"] == "PASS", "E6 verification did not pass")
    require((e6["table_complete_rows"], e6["path_complete_rows"], e6["reference_rows"]) == (8, 24, 4),
            "E6 complete counts are not 8/24/4")
    require(e6["protected_archive_files_unchanged"] and e6["no_new_selection"] and e6["E3_menu_unchanged"],
            "E6 changed protected archives or selection")
    e6_table, e6_path = rows(RESULTS/"e6/table6.csv"), rows(RESULTS/"e6/lambda-path.csv")
    require(len(e6_table) == 8 and len(e6_path) == 24
            and len(rows(RESULTS/"e6/lambda-path-I.csv")) == 4, "E6 actual CSV row counts differ")
    require(all(row["status"] == "COMPLETE" for row in e6_table+e6_path), "E6 actual CSV contains incomplete reports")
    for filename, digest in e6_numeric["export_sha256"].items():
        require(sha(RESULTS/"e6"/filename) == digest, "E6 verified export changed: " + filename)

    e5 = read_json(RESULTS / "e5/run-receipt.json")
    e5_check = read_json(RESULTS / "e5/verification.json")
    independent = read_json(RESULTS / "e5/independent-readback.json")
    panel = rows(RESULTS / "e5/summary.csv")
    expected = {"P1": dict(success_count=30, fixed_denominator=45, threshold=40, supported=False),
                "P2": dict(success_count=24, fixed_denominator=48, threshold=36, supported=False),
                "P3": dict(success_count=33, fixed_denominator=48, threshold=25, supported=True)}
    require(e5["status"] == "COMPLETE" and e5["completed_cells"] == e5["planned_cells"] == len(panel) == 48,
            "E5 is not complete in all 48 cells")
    require(all(row["status"] == "COMPLETE" for row in panel), "E5 contains incomplete cells")
    require(e5_check["status"] == independent["status"] == "PASS" and independent["counts"]["mismatch_count"] == 0,
            "E5 readback did not pass")
    require(e5_check["evaluation_arrays_checked"] == e5_check["validation_segments_checked"] == 240
            and e5_check["new_fit_diagnostics_checked"] == 2016,
            "E5 checked-array counts differ")
    require(e5["predictions"] == independent["predictions"] == expected
            == read_json(RESULTS/"e5/prediction-assessment.json")["predictions"], "E5 P1-P3 decisions differ")
    members = [row for row in panel if row["fixed_p1_member"] == "True"]
    actual = (sum(float(row["QR33_plus_mean_pinball"]) < float(row["original_QR33_mean_pinball"]) for row in members),
              sum(-10 <= float(row["QR33_plus_percent_vs_F"]) <= 10 for row in panel),
              sum(float(row["selected_penalty"]) >= 1 for row in panel))
    require(len(members) == 45 and actual == (30, 24, 33), "E5 fixed-denominator CSV counts differ")
    require(sha(RESULTS/"e5/summary.csv") == e5["summary_sha256"], "E5 summary changed")
    commit = e5["prediction_commit"]
    filename = e5["prediction_file"]
    blob = git("show", f"{commit}:{filename}")
    require(hashlib.sha256(blob).hexdigest() == sha(ROOT/filename) == e5["prediction_file_sha256"],
            "E5 committed prediction bytes differ")
    require(git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).decode().splitlines() == [filename],
            "E5 prediction commit was not standalone")
    stamp = git("show", "-s", "--format=%cI", commit).decode().strip()
    require(stamp == e5["prediction_commit_timestamp"], "E5 Git timestamp differs")
    parse = datetime.fromisoformat
    require(parse(stamp) < parse(e5["run_started_utc"]) <= parse(e5["first_model_fit_utc"]),
            "E5 prediction did not precede first fit")
    subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT, check=True)

    w3 = read_json(RESULTS/"w3/summary.json")
    family = rows(RESULTS/"w3/dm-family.csv")
    require(w3["status"] == "PASS" and (w3["total_retained_contrasts"], w3["archived_matched_family_size"],
            w3["primary_family_size"], w3["remaining_matched_family_size"], w3["legacy_outside_family_size"]) == (74,72,2,71,1),
            "W3 statuses or family counts differ")
    require(w3["table_rows"] == len(rows(RESULTS/"w3/tables3-4-ready.csv")) == 48, "W3 actual table row count differs")
    require(len(family) == 74 and sum(row["family"] == "source_primaries_2" for row in family) == 2
            and sum(row["family"] == "remaining_matched_71" for row in family) == 71, "W3 actual family rows differ")
    require(w3["family_reorganized_post_result"] and w3["all_raw_archived_values_unchanged"]
            and w3["protected_archive_files_unchanged"] and w3["no_models_or_HAC_refitted"], "W3 scope/preservation differs")
    for filename, digest in w3["input_sha256"].items():
        require(sha(ROOT/filename) == digest, "W3 protected input changed: " + filename)
    for filename, digest in w3["output_sha256"].items():
        require(sha(RESULTS/"w3"/filename) == digest, "W3 verified output changed: " + filename)
    olddm = rows(RESULTS/"inference/dm-verified.csv")
    require(sum(row["holm_family_size"] == "72" for row in olddm) == 72, "Original 72-member archive differs")
    original = {row["contrast_id"]: row for row in olddm}
    for row in family:
        for field in ("mean_difference", "dm_t", "dm_p", "hln_t", "hln_p", "double_dm_t", "double_dm_p", "double_hln_p"):
            require(row[field] == original[row["contrast_id"]][field], "W3 changed archived raw value")
    for row in family:
        if row["family"] == "source_primaries_2":
            require(row["reported_p_role"] == "primary, unadjusted" and int(row["primary_bonferroni_family_size"]) == 2
                    and math.isclose(float(row["primary_bonferroni_p"]), min(1., 2*float(row["dm_p"]))),
                    "W3 primary reporting differs")
    w4 = read_json(RESULTS/"w4/ar-comparison.json")
    require(w4["status"] == "PASS" and len(rows(RESULTS/"w4/ar-comparison.csv")) == len(w4["rows"]) == 8,
            "W4 statuses or eight-cell counts differ")
    require(w4["checks"]["original_paired_rows_reconciled"] == 24 and w4["checks"]["no_new_fit"]
            and w4["checks"]["no_inference"], "W4 readback scope differs")
    require((w4["counts_all"]["F"]["lower_loss"], w4["counts_all"]["S"]["lower_loss"],
             w4["counts_by_source"]["nyfed_weekly"]["original_QR33"]["lower_loss"],
             w4["counts_by_source"]["nyfed_weekly"]["QR33_plus"]["lower_loss"]) == (5,5,4,3), "W4 reported counts differ")
    require(sha(RESULTS/"w4/ar-comparison.csv") == w4["output_csv_sha256"], "W4 output changed")
    for filename, digest in w4["input_sha256"].items():
        require(sha(ROOT/filename) == digest, "W4 verified input changed: " + filename)
    return dict(e6_status="PASS", e6_complete_counts=[8,24,4], e5_status="COMPLETE", e5_complete_cells=48,
                e5_predictions=expected, prediction_commit=commit, prediction_commit_timestamp=stamp,
                first_model_fit_utc=e5["first_model_fit_utc"], w3_status="PASS", original_holm_family_size=72,
                w3_primary_family_size=2, w3_remaining_matched_family_size=71, w4_status="PASS", w4_cells=8)


def verify_preservation():
    old = set(git("ls-tree", "-r", "--name-only", BASE).decode().splitlines())
    changed = set(git("diff", "--name-only", BASE, "--").decode().splitlines())
    allowed = {"README.md", "REVISION_SUPERVISOR_20261023.md", "build_supervisor_document.py"}
    protected = {name for name in old if name not in allowed and not name.startswith("manuscript/supervisor-revision/")}
    require(not (changed & protected), "Protected baseline files changed: " + repr(sorted(changed & protected)))
    deleted = set(git("diff", "--name-only", "--diff-filter=D", BASE, "--").decode().splitlines())
    deleted.update(git("diff", "--name-only", "--diff-filter=D", "HEAD", "--").decode().splitlines())
    require(not deleted, "Tracked files deleted: " + repr(sorted(deleted)))
    return dict(baseline=BASE, baseline_tracked_file_count=len(old), protected_baseline_file_count=len(protected),
                protected_baseline_changes=[], deleted_tracked_files=[], original_72_archive_unchanged=True)


def main():
    require(not OUT.exists(), "Refusing to overwrite the round2 document verification receipt")
    document = verify_document()
    results = verify_results()
    preservation = verify_preservation()
    tests = read_json(ROUND2/"test-verification.json")
    visual = read_json(ROUND2/"visual-review.json")
    require(tests["status"] == "PASS", "Actual final test receipt is not PASS")
    require(visual["status"] == "PASS" and visual["pdf_sha256"] == document["pdf_sha256"]
            and visual["page_count"] == document["page_count"]
            and visual["reviewed_physical_pages"] == list(range(1, document["page_count"]+1)),
            "Actual visual review does not cover every page of this PDF")
    result = dict(status="PASS", checked_utc=datetime.now(timezone.utc).isoformat(),
                  **document, results=results, preservation=preservation,
                  test_verification_sha256=sha(ROUND2/"test-verification.json"),
                  visual_review_sha256=sha(ROUND2/"visual-review.json"),
                  verifier_sha256=sha(__file__),
                  scope="Document and accepted-result contracts only; no models, tests or visual reviews executed by this verifier.")
    with OUT.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, FileNotFoundError, subprocess.CalledProcessError) as error:
        print(json.dumps(dict(status="FAIL", error=str(error)), ensure_ascii=False))
        raise SystemExit(1)
