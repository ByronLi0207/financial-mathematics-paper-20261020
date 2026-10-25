#!/usr/bin/env python3
"""Compare four manually verified primary-record metadata sets with current TeX/BibTeX."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "submission-jof/references.bib"
MAIN = ROOT / "submission-jof/manuscript.tex"
RECORDS = [
    {"key": "merton1976", "author": "Merton, Robert C.", "main_author": "Merton, R. C.",
     "title": "Option pricing when underlying stock returns are discontinuous",
     "year": "1976", "journal": "Journal of Financial Economics", "volume": "3", "number": "1--2", "pages": "125--144",
     "doi": "10.1016/0304-405X(76)90022-2", "issue_date": "January–March 1976",
     "sources": ["https://www.sciencedirect.com/science/article/pii/0304405X76900222"],
     "actual_reading_scope": "Primary-publisher indexed article preview: title, author, journal/issue/pages/DOI, abstract. Direct DOI and publisher opens returned 403. No original body or full-text review in this check.",
     "citation_use": "Historical precedent for continuous-plus-jump financial models only, not a claim that the study's discrete mean-reverting jump DGP reproduces Merton's option-pricing model."},
    {"key": "turner1989", "author": "Turner, Christopher M. and Startz, Richard and Nelson, Charles R.",
     "main_author": "Turner, C. M., Startz, R., \\& Nelson, C. R.",
     "title": "A Markov model of heteroskedasticity, risk, and learning in the stock market",
     "year": "1989", "journal": "Journal of Financial Economics", "volume": "25", "number": "1", "pages": "3--22",
     "doi": "10.1016/0304-405X(89)90094-9", "issue_date": "November 1989",
     "sources": ["https://www.sciencedirect.com/science/article/pii/0304405X89900949", "https://www.sciencedirect.com/author/6602724008/richard-startz", "https://faculty.washington.edu/cnelson/CV.htm"],
     "actual_reading_scope": "Publisher indexed article preview and author listing: metadata/abstract. Author's university CV: corresponding publication entry and author names. Direct publisher opens returned 403. No original article body read in this check.",
     "citation_use": "Historical precedent for Markov-state conditional variance; no claim that its estimated excess-return/risk-learning model is the study's specified discrete level process."},
    {"key": "viering2023", "author": "Viering, Tom and Loog, Marco", "main_author": "Viering, T., \\& Loog, M.",
     "title": "The Shape of Learning Curves: A Review", "year": "2023",
     "journal": "IEEE Transactions on Pattern Analysis and Machine Intelligence", "volume": "45", "number": "6", "pages": "7799--7819",
     "doi": "10.1109/TPAMI.2022.3220744", "issue_date": "June 2023", "online_publication_date": "2022-11-09",
     "eprint": "2103.10948", "arxiv_version": "v2", "arxiv_v2_revision_date": "2022-11-05",
     "sources": ["https://ieeexplore.ieee.org/document/9944190/", "https://research.tudelft.nl/en/publications/the-shape-of-learning-curves-a-review/", "https://arxiv.org/abs/2103.10948v2"],
     "actual_reading_scope": "IEEE indexed metadata/abstract; author's institutional publication record metadata/abstract; arXiv version-specific abstract and submission history. Direct IEEE open presented robot verification. No full original body review in this check.",
     "citation_use": "Diverse and nonmonotone learning curves as background; not evidence that the paper's fixed-period relative-loss curve has an independent-sample expected-risk interpretation."},
    {"key": "bollerslev1986", "author": "Bollerslev, Tim", "main_author": "Bollerslev, T.",
     "title": "Generalized autoregressive conditional heteroskedasticity", "year": "1986",
     "journal": "Journal of Econometrics", "volume": "31", "number": "3", "pages": "307--327",
     "doi": "10.1016/0304-4076(86)90063-1", "issue_date": "April 1986",
     "sources": ["https://www.sciencedirect.com/science/article/pii/0304407686900631", "https://scholars.duke.edu/publication/651658", "https://public.econ.duke.edu/~boller/research.html"],
     "actual_reading_scope": "Primary publisher indexed article metadata/abstract plus direct author's university metadata/abstract record and author publication-list entry. Direct publisher open returned 403. No original article body review in this check.",
     "citation_use": "Origin of the conditional-variance model family; not proof of the current simulation's outcomes or an explanation of the failed narrow regime."},
]


def normalize(value):
    return re.sub(r"\s+", " ", value).strip().casefold()


def bib_entry(text, key):
    match = re.search(r"@\w+\s*\{\s*" + re.escape(key) + r"\s*,", text)
    if match is None:
        return None
    depth, cursor = 1, match.end()
    start = cursor
    while cursor < len(text) and depth:
        depth += (text[cursor] == "{") - (text[cursor] == "}")
        cursor += 1
    return text[start:cursor - 1]


def run():
    bibtext, maintext = BIB.read_text(), MAIN.read_text()
    differences = []
    for record in RECORDS:
        key = record["key"]
        entry = bib_entry(bibtext, key)
        mainline = next((x for x in maintext.splitlines() if re.search(r"\\bibitem(?:\[[^\]]*\])?\{" + re.escape(key) + r"\}", x)), None)
        record["reference_bib_fields"] = {}
        record["main_bibitem"] = mainline
        for field in ("author", "title", "year", "journal", "volume", "number", "pages", "doi"):
            match = re.search(r"\b" + field + r"\s*=\s*\{([^{}]*)\}", entry or "", re.I)
            actual = match.group(1) if match else None
            record["reference_bib_fields"][field] = actual
            if actual is None or normalize(actual) != normalize(record[field]):
                differences.append({"key": key, "surface": "references.bib", "field": field, "actual": actual, "expected": record[field]})
        tokens = [record["main_author"], record["title"], "(" + record["year"] + ")", record["journal"], "\\emph{" + record["volume"] + "}(" + record["number"] + ")", record["pages"], record["doi"]]
        for token in tokens:
            if mainline is None or normalize(token) not in normalize(mainline):
                differences.append({"key": key, "surface": "manuscript.tex bibitem", "missing_token": token})
        if key == "viering2023":
            for token in ("2103.10948", "v2", "2022-11-05"):
                if token not in (entry or ""):
                    differences.append({"key": key, "surface": "references.bib preprint", "missing_token": token})
        record["status"] = "PASS" if not any(x["key"] == key for x in differences) else "FAIL"
    output = {"created_utc": datetime.now(timezone.utc).isoformat(),
              "status": "PASS" if not differences else "FAIL", "paper_metadata_mismatch_count": len(differences),
              "differences": differences, "records": RECORDS,
              "scope": "Four references rechecked from owning publisher or author/institutional primary records; metadata and abstract only. No full-text reading, experiment, statistical analysis, compile, or pytest claim.",
              "source_discrepancies": [
                  {"status": "MISMATCH", "key": "turner1989", "field": "pages", "author_cv_value": "3–25", "publisher_value": "3–22", "resolution": "Publisher issue pagination controls; both current paper surfaces already correctly use 3--22. No edit required."},
                  {"status": "MISMATCH", "key": "bollerslev1986", "field": "publication_month_day", "duke_repository_value": "January 1, 1986", "publisher_issue_value": "April 1986", "resolution": "Use publisher issue date for issue month, retain only the verified year 1986 in existing bibliographies. Do not infer an exact publication day from generic repository metadata."}],
              "version_note": "Viering/Loog journal issue year 2023, online-publication year 2022, and arXiv v2 revised 2022-11-05 describe different version events; these are not conflicting bibliographic years.",
              "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in (MAIN, BIB)}}
    destination = ROOT / "notes/revision-v9/wp7-reference-check.json"
    destination.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": output["status"], "paper_metadata_mismatch_count": len(differences), "references": [{"key": x["key"], "status": x["status"], "reading_scope": "metadata_and_abstract_only"} for x in RECORDS], "external_primary_record_discrepancies": output["source_discrepancies"]}, indent=2, ensure_ascii=False))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(run())
