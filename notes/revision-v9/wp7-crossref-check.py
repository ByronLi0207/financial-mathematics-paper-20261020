#!/usr/bin/env python3
"""Static document citation/label/input check; no TeX or scientific code runs."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(text):
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def locations(pattern, text, path):
    return [{"key": match.group(1), "file": str(path),
             "line": text.count("\n", 0, match.start()) + 1}
            for match in re.finditer(pattern, text)]


def inspect(repo):
    folder = repo / "submission-jof"
    documents = ["manuscript.tex", "supplement.tex", "extended-v9-technical.tex"]
    hashes, reports, all_label_roots = {}, [], defaultdict(list)
    bibfile = folder / "references.bib"
    bibtext = clean(bibfile.read_text())
    bibkeys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bibtext)
    hashes[str(bibfile.relative_to(repo))] = sha(bibfile)
    for document in documents:
        visited, inputs, missing, labels, refs, citations, bibitems, assets = set(), [], [], [], [], [], [], []

        def walk(path, ancestors=()):
            rel = path.relative_to(repo)
            if path in ancestors:
                missing.append({"kind": "recursive_input_cycle", "file": str(rel)})
                return
            if not path.is_file():
                missing.append({"kind": "missing_input", "file": str(rel)})
                return
            # Each expansion is inspected: repeated inclusion can duplicate labels.
            visited.add(str(rel))
            hashes[str(rel)] = sha(path)
            text = clean(path.read_text())
            labels.extend(locations(r"\\label\s*\{([^{}]+)\}", text, rel))
            refs.extend(locations(r"\\(?:ref|eqref|pageref|autoref|cref|Cref)\*?\s*\{([^{}]+)\}", text, rel))
            bibitems.extend(locations(r"\\bibitem\s*(?:\[[^\]]*\])?\s*\{([^{}]+)\}", text, rel))
            for item in locations(r"\\cite(?:p|t|alp|alt|author|year|yearpar)?\*?\s*(?:\[[^\]]*\]\s*)*\{([^{}]+)\}", text, rel):
                for key in item["key"].split(","):
                    citations.append(dict(item, key=key.strip()))
            for item in locations(r"\\(?:input|include)\s*\{([^{}]+)\}", text, rel):
                target = path.parent / item["key"]
                if not target.suffix:
                    target = target.with_suffix(".tex")
                # TeX lookup in this project uses the entry-document directory.
                if not target.exists():
                    target = folder / item["key"]
                    if not target.suffix:
                        target = target.with_suffix(".tex")
                item["resolved_path"] = str(target.relative_to(repo))
                inputs.append(item)
                walk(target, ancestors + (path,))
            for item in locations(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^{}]+)\}", text, rel):
                target = folder / item["key"]
                alternatives = [target] if target.suffix else [target.with_suffix(x) for x in (".pdf", ".png", ".jpg", ".jpeg")]
                found = next((x for x in alternatives if x.is_file()), None)
                item["resolved_path"] = str(found.relative_to(repo)) if found else None
                assets.append(item)
                if found is None:
                    missing.append(dict(item, kind="missing_graphic"))
                else:
                    hashes[str(found.relative_to(repo))] = sha(found)

        walk(folder / document)
        labelcounts, bibcounts = Counter(x["key"] for x in labels), Counter(x["key"] for x in bibitems)
        for label in labelcounts:
            all_label_roots[label].append(document)
        undefined_refs = [x for x in refs if x["key"] not in labelcounts]
        # Main uses its explicit thebibliography, not references.bib; no global
        # citation inheritance is assumed for the two standalone supplements.
        undefined_cites = [x for x in citations if x["key"] not in bibcounts]
        duplicate_labels = sorted(k for k, n in labelcounts.items() if n > 1)
        duplicate_bibitems = sorted(k for k, n in bibcounts.items() if n > 1)
        reports.append({"document": document, "files": sorted(visited),
                        "inputs": inputs, "graphics": assets,
                        "label_count": len(labels), "reference_count": len(refs),
                        "citation_occurrences": len(citations),
                        "unique_citation_keys": sorted({x["key"] for x in citations}),
                        "bibitem_keys": sorted(bibcounts),
                        "undefined_refs": undefined_refs, "undefined_citations": undefined_cites,
                        "duplicate_labels": duplicate_labels, "duplicate_bibitems": duplicate_bibitems,
                        "missing_files": missing})
    errors = sum(len(x[k]) for x in reports for k in ("undefined_refs", "undefined_citations", "duplicate_labels", "duplicate_bibitems", "missing_files"))
    mains = reports[0]
    bib_missing = sorted(set(mains["bibitem_keys"]) - set(bibkeys))
    duplicate_bibkeys = sorted(k for k, n in Counter(bibkeys).items() if n > 1)
    errors += len(bib_missing) + len(duplicate_bibkeys)
    return {"status": "PASS" if errors == 0 else "FAIL", "error_count": errors,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "Static regex inspection of entry documents and recursive TeX inputs; independent of compiler and PDF checks. No model, statistical calculation, tests, or compile runs.",
            "documents": reports, "references_bib_key_count": len(bibkeys),
            "main_bibitems_absent_from_reference_bib": bib_missing,
            "duplicate_references_bib_keys": duplicate_bibkeys,
            "labels_repeated_across_standalone_documents": {k:v for k,v in sorted(all_label_roots.items()) if len(v) > 1},
            "cross_document_note": "Each document is standalone and has no externaldocument directive. Shared sup:frontier-0, sup:frontier-8 and sup:implementation labels mark intentional relocation/index sections in the compact Supplement and full sections in the technical appendix; they do not create automatic cross-document references. Cross-document access uses explicit hyperlinks. All actual ref/eqref/citation commands must resolve in the document that emits them.",
            "source_sha256": dict(sorted(hashes.items()))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = inspect(args.repo)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k:output[k] for k in ("status", "error_count", "references_bib_key_count", "main_bibitems_absent_from_reference_bib", "duplicate_references_bib_keys", "labels_repeated_across_standalone_documents")}, indent=2))
    for document in output["documents"]:
        print(json.dumps({key: document[key] for key in ("document", "label_count", "reference_count", "citation_occurrences", "undefined_refs", "undefined_citations", "duplicate_labels", "duplicate_bibitems", "missing_files")}))
    raise SystemExit(0 if output["status"] == "PASS" else 1)
