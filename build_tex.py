"""Reproduce the paper's TeX source from its canonical content JSON.

The conversion and formatting reproduce the existing compiled main.tex bytes.
Supported HTML markup is b/i/sub/super/a (the latter with href); equation blocks
use their explicit latex field. This tool only writes TeX source. It never runs
TeX, uses the network, or reads raw observations, result tables, or figure PDFs.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "manuscript/working-paper/paper-content.json"


def esc(value):
    special = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "<": r"\( < \)", ">": r"\( > \)", "τ": r"\(\tau\)", "ρ": r"\(\rho\)",
        "ε": r"\(\epsilon\)", "ℓ": r"\(\ell\)", "≤": r"\(\le\)", "≥": r"\(\ge\)",
        "−": r"\(-\)", "…": r"\ldots{}", "©": r"\copyright{}", "\u00a0": " ",
    }
    result = "".join(special.get(char, char) for char in value)
    return re.sub(
        r"\b([0-9a-f]{40}|[0-9a-f]{64})\b",
        lambda match: r"\texttt{" + r"}\allowbreak\texttt{".join(
            match[0][index:index + 16] for index in range(0, len(match[0]), 16)
        ) + "}",
        result,
    )


class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ("b", "i"):
            self.out.append(r"\textbf{" if tag == "b" else r"\emph{")
        elif tag in ("sub", "super"):
            self.out.append(r"\textsubscript{" if tag == "sub" else r"\textsuperscript{")
        elif tag == "a":
            attributes = dict(attrs)
            if set(attributes) != {"href"} or type(attributes["href"]) is not str:
                raise ValueError("INVALID_REFERENCE_LINK")
            self.out.append(r"\href{" + attributes["href"].replace("%", r"\%").replace("#", r"\#") + "}{")
        else:
            raise ValueError("UNSUPPORTED_MARKUP")
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            raise ValueError("UNBALANCED_MARKUP")
        self.out.append("}")

    def handle_data(self, data):
        self.out.append(esc(data))

    def handle_startendtag(self, tag, attrs):
        raise ValueError("UNSUPPORTED_MARKUP")

    def handle_comment(self, data):
        raise ValueError("UNSUPPORTED_MARKUP")

    def handle_decl(self, decl):
        raise ValueError("UNSUPPORTED_MARKUP")


def conv(value):
    parser = Markup()
    parser.feed(value)
    parser.close()
    if parser.stack:
        raise ValueError("UNBALANCED_MARKUP")
    return "".join(parser.out)


def build_source(content):
    parts = [r'''\documentclass[10pt,a4paper]{article}
\usepackage[margin=50pt]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,graphicx,booktabs,array}
\usepackage[unicode,breaklinks=true,colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{2em}
\setlength{\tabcolsep}{3pt}
\hypersetup{pdftitle={Historical Headrooms versus Current-State Scenarios for Sampled Inventory Peaks},pdfauthor={}}
\begin{document}
\fontsize{10.5}{14}\selectfont
\begin{center}
{\LARGE\bfseries ''' + esc(content["title"]) + r'''}\par\vspace{8pt}
{\large ''' + esc(content["subtitle"]) + r'''}\par\vspace{6pt}
''' + esc(content["date"]) + r'''
\end{center}
\begin{abstract}
''' + conv(content["abstract"]) + r'''
\end{abstract}
''']
    for section in content["sections"]:
        parts.append(r"\section*{" + esc(section["title"]) + "}\n")
        for block in section["blocks"]:
            kind = block["type"]
            if kind == "p":
                parts.append(conv(block["html"]) + "\n\n")
            elif kind == "equation":
                if type(block.get("latex")) is not str or not block["latex"].strip():
                    raise ValueError("EQUATION_REQUIRES_LATEX")
                parts.append("\\[\n" + block["latex"] + "\n\\]\n")
            elif kind == "subheading":
                parts.append(r"\subsection*{" + esc(block["text"]) + "}\n")
            elif kind == "table":
                columns = len(block["headers"])
                parts.append("\\begin{center}\n\\begin{minipage}{\\linewidth}\n\\small\\textbf{"
                             + esc(block["caption"]) + "}\\par\\medskip\n\\centering\\fontsize{8}{10}\\selectfont\n\\begin{tabular}{"
                             + ("l" + "r" * (columns - 1)) + "}\n\\toprule\n")
                parts.append(" & ".join(esc(str(value)) for value in block["headers"]) + r" \\" + "\n\\midrule\n")
                for row in block["rows"]:
                    parts.append(" & ".join(esc(str(value)) for value in row) + r" \\" + "\n")
                parts.append("\\bottomrule\n\\end{tabular}\n\\end{minipage}\n\\end{center}\n")
            else:
                raise ValueError("UNSUPPORTED_BLOCK_TYPE")
    parts.append("\\section*{References}\n")
    for reference in content["references"]:
        parts.append(conv(reference["html"]) + "\n\n")
    parts.append("\\clearpage\n")
    for figure in content["figures"]:
        parts.append("\\begin{figure}[p]\n\\centering\n\\includegraphics[width=\\linewidth]{"
                     + figure["path"] + "}\n\\par\\smallskip\n\\small " + esc(figure["caption"])
                     + "\n\\end{figure}\n\\clearpage\n")
    parts.append("\\end{document}\n")
    return "".join(parts)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".scratch/main-reproduced.tex",
                        help="Exclusive output TeX path; an existing file is never replaced")
    args = parser.parse_args(argv)
    try:
        scratch = ROOT / ".scratch"
        if any(path.is_symlink() for path in (scratch, *scratch.parents)):
            raise ValueError("INVALID_SCRATCH_DIRECTORY")
        scratch.mkdir(mode=0o700, exist_ok=True)
        output = args.output
        if output.exists() or output.is_symlink():
            raise ValueError("OUTPUT_ALREADY_EXISTS")
        if not output.parent.is_dir() or any(path.is_symlink() for path in output.parents):
            raise ValueError("INVALID_OUTPUT_DIRECTORY")
        content = json.loads(CONTENT.read_text(encoding="utf-8"))
        encoded = build_source(content).encode("utf-8")
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as target:
            target.write(encoded)
    except (OSError, ValueError, KeyError, TypeError) as error:
        # Fixed control errors are safe to show; OS diagnostics may contain paths.
        reason = str(error) if type(error) is ValueError and re.fullmatch(r"[A-Z_]+", str(error)) else type(error).__name__
        print("TEX_BUILD_ERROR:" + reason, file=sys.stderr)
        return 1
    print(json.dumps({"status": "TEX_SOURCE_WRITTEN", "bytes": len(encoded), "output": str(output)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
