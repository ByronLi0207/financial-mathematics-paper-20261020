"""Package already checked native documents; never regenerate research results.

This is a document-copy/snapshot/ZIP operation, not a financial replay.
Historical authoring builders must not overwrite the current saved TeX.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DELIVERY = ROOT / "submission-jof"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def included_sources(name, seen=None):
    seen = set() if seen is None else seen
    if name in seen:
        return []
    seen.add(name)
    text = (DELIVERY / name).read_text()
    answer = [name]
    for child in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
        child += "" if Path(child).suffix else ".tex"
        answer += included_sources(child, seen)
    return answer


def package(main_pdf, supplement_pdf, title_pdf, *,
            main_numeric_report=None, supp_numeric_report=None):
    source_names = sorted(set(included_sources("main.tex") +
                              included_sources("supplement.tex") +
                              included_sources("title-page.tex")))
    figures = set()
    for name in source_names:
        for graphic in re.findall(
                r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
                (DELIVERY / name).read_text()):
            graphic += "" if Path(graphic).suffix else ".pdf"
            figures.add(graphic)
    assert len(figures) == 5, figures
    assert len([name for name in source_names if name.startswith("generated/")]) == 5
    numeric_reports = {
        "manuscript": main_numeric_report or "notes/revision-v8/wp8-main-number-check-root.json",
        "supplement": supp_numeric_report or "notes/revision-v8/wp8-supp-number-check-final-layout.json",
    }
    # Keep bindings repository-relative even when the caller supplies an
    # absolute in-repository path. Outside reports cannot become public links.
    numeric_reports = {
        stem: (ROOT / path).resolve().relative_to(ROOT.resolve()).as_posix()
        for stem, path in numeric_reports.items()
    }
    for stem in numeric_reports:
        expected = json.loads((ROOT / numeric_reports[stem]).read_text())
        if stem == "manuscript":
            assert expected["current_main_sha256"] == sha(DELIVERY / f"{stem}.tex")
            assert expected["status"] == "PASS"
        else:
            assert expected["status"] == "PASS_WITH_SCOPE_LIMITS"
            assert expected["files"]["submission-jof/supplement.tex"]["sha256"] == sha(DELIVERY / f"{stem}.tex")
    for stem, source in (("manuscript", main_pdf), ("supplement", supplement_pdf),
                         ("title-page", title_pdf)):
        assert source.is_file(), source
        shutil.copy2(source, DELIVERY / f"{stem}.pdf")
        shutil.copy2(source, DELIVERY / f"{stem}-preview.pdf")
    title = "Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits"
    for stem in ("manuscript", "supplement"):
        source = DELIVERY / f"{stem}.tex"
        dependencies = [dict(path=name, sha256=sha(DELIVERY / name),
                             latex=(DELIVERY / name).read_text())
                        for name in included_sources(source.name)[1:]]
        snapshot = dict(schema="v8-current-native-latex-snapshot", title=title,
                        canonical_source=source.name, source_sha256=sha(source),
                        latex=source.read_text(), recursive_inputs=dependencies,
                        source_bindings="../" + numeric_reports[stem],
                        historical_v6_schema=f"../manuscript/revision-v6-preserved/{stem}-content.json",
                        historical_v7_source_commit="b571f324a253480b4e39bc8a8096775ddbcc7017",
                        meaning="Current saved source and recursive TeX inputs; not a separate authoring/rendering pipeline")
        (DELIVERY / f"{stem}-content.json").write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    members = sorted(set(source_names) | figures | {
        "references.bib", "README.md", "AUTHOR-TODO.md", "cover-letter.md"})
    target = DELIVERY / "overleaf-package.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in members:
            path = DELIVERY / name
            assert path.is_file() and not path.is_symlink(), path
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 24, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert archive.namelist() == members
        for name in members:
            assert archive.read(name) == (DELIVERY / name).read_bytes()
    receipt = dict(utc=datetime.now(timezone.utc).isoformat(),
                   script="notes/revision-v8/seal_wp8_delivery.py", script_sha256=sha(Path(__file__)),
                   source_input_count=len(source_names), figure_input_count=len(figures),
                   source_members={name: dict(bytes=(DELIVERY / name).stat().st_size,
                                              sha256=sha(DELIVERY / name)) for name in members},
                   package_bytes=target.stat().st_size, package_sha256=sha(target),
                   all_members_match_current_sources=True,
                   current_pdfs={stem: dict(sha256=sha(DELIVERY / f"{stem}.pdf"),
                                                preview_alias_equal=sha(DELIVERY / f"{stem}.pdf") == sha(DELIVERY / f"{stem}-preview.pdf"))
                                 for stem in ("manuscript", "supplement", "title-page")},
                   raw_data_included=False, results_recomputed=False,
                   final_compilation_and_visual_acceptance="Separate owning WP8 receipts required")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-pdf", type=Path, required=True)
    parser.add_argument("--supplement-pdf", type=Path, required=True)
    parser.add_argument("--title-pdf", type=Path, required=True)
    parser.add_argument("--main-numeric-report", type=Path,
                        help="Checked main numeric report within the repository; defaults to the WP8 report")
    parser.add_argument("--supp-numeric-report", type=Path,
                        help="Checked Supplement numeric report within the repository; defaults to the WP8 report")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = package(args.main_pdf, args.supplement_pdf, args.title_pdf,
                      main_numeric_report=args.main_numeric_report,
                      supp_numeric_report=args.supp_numeric_report)
    with args.output.open("x") as stream:
        stream.write(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
