"""V8 prose-only statistics with a fixed v7 baseline and inherited v7 scope.

This measures documents, not financial outcomes. Tables/notes, display maths,
declarations/references and Research design and transparency retain v7's
explicit exclusions. Abstract and figure captions remain in scope.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("v7_prose_metrics", ROOT / "notes/v7/writing_metrics.py")
v7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v7)
BASELINE = "b571f324a253480b4e39bc8a8096775ddbcc7017"


def prose(tex):
    labels = {key: label for label, key in re.findall(r"\\bibitem\[([^\]]+)\]\{([^}]+)\}", tex)}
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
    body = tex[re.search(r"\\section\{Introduction\}", tex).start():]
    body = re.split(r"\\section\*?\{(?:Declarations and availability|Data and code availability|References)\}", body)[0]
    for env in ("table", "longtable", "tabular", "samepage"):
        body = re.sub(r"\\begin\{" + env + r"\}.*?\\end\{" + env + r"\}", "\n\n", body, flags=re.S)
    body = re.sub(r"\{\\footnotesize Hit tests.*?\}\s*", "\n\n", body, flags=re.S)
    body = re.sub(r"\\\[.*?\\\]", "\n\n", body, flags=re.S)
    body = re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}", "", body)
    body = re.sub(r"\\(section|subsection)\*?\{([^}]*Research design and transparency[^}]*)\}.*?(?=\\(?:section|subsection)\*?\{|\Z)", "\n\n", body, flags=re.S)
    body = re.sub(r"\\(?:section|subsection|paragraph)\*?\{[^}]*\}", "\n\n", body)
    body = re.sub(r"\\textbf\{(?:C[123]\.|Contribution on[^}]+|Proposition[^}]+)\}", "", body)
    body = re.sub(r"\\(?:begin|end)\{(?:figure|center|minipage)\}(?:\[[^\]]*\])?", "", body)
    body = body.replace(r"\FloatBarrier", "").replace(r"\centering", "")
    paragraphs = [v7.plain(part, labels) for part in re.split(r"\n\s*\n", body)]
    paragraphs = [p for p in paragraphs if re.search(r"[A-Za-z]", p)]
    return v7.plain(abstract, labels), paragraphs


def measure(path):
    report = v7.metrics(path)
    abstract, paragraphs = prose(path.read_text())
    full = abstract + " " + " ".join(paragraphs)
    report["overprecise_percentages"] = re.findall(r"(?<![\w.])[+-]?\d+\.\d{2,}\s*%", full)
    report["changes_by_sentences"] = [s for s in v7.sentences(full)
                                      if re.search(r"\bchanges?\b[^.!?]*\bby\b", s, re.I)]
    report["jargon_counts"] = {term: len(re.findall(re.escape(term), full, re.I)) for term in (
        "evaluated finite delayed coverage correction", "numerically accepted regression fits",
        "explicitly identified comparison sets", "source-native", "completed response",
        "strict-hit indicator", "elementary-score curves")}
    report["overprecise_percentage_count"] = len(report["overprecise_percentages"])
    report["changes_by_count"] = len(report["changes_by_sentences"])
    report["all_v8_writing_gates_pass"] = (report["pass_quantitative"] and
        not report["overprecise_percentages"] and not report["changes_by_sentences"] and
        not any(report["jargon_counts"].values()))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    baseline = ROOT / ".scratch/revision-v8/wp1-baseline/manuscript.tex"
    baseline.parent.mkdir(parents=True, exist_ok=True)
    original = subprocess.check_output(["git", "show", BASELINE + ":submission-jof/manuscript.tex"], cwd=ROOT)
    if baseline.exists() and baseline.read_bytes() != original:
        raise ValueError("The fixed v7 baseline copy changed")
    if not baseline.exists():
        baseline.write_bytes(original)
    report = dict(baseline_commit=BASELINE, scope="Inherited v7 prose exclusions; percentages/changes-by include abstract",
                  before=measure(baseline), after=measure(ROOT / "submission-jof/manuscript.tex"))
    (ROOT / args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    keys = ("abstract_words", "abstract_numbers", "main_sentences", "mean_sentence_words", "over35_percent",
            "negation_percent", "max_numbers_per_sentence", "overprecise_percentage_count", "changes_by_count",
            "all_v8_writing_gates_pass")
    summary = {phase: {k: report[phase][k] for k in keys} for phase in ("before", "after")}
    summary["after_failures"] = {k: report["after"][k] for k in ("numeric_violations", "paragraphs_over6", "banned_counts", "jargon_counts", "overprecise_percentages", "changes_by_sentences")}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.require_pass:
        raise SystemExit(not report["after"]["all_v8_writing_gates_pass"])


if __name__ == "__main__":
    main()
