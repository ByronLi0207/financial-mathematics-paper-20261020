"""Typeset supplied paper text and append one approved three-figure inventory.

This is a document builder only. It never opens source observations, scientific
result tables, or any PDF other than its own text body and the original or
revision canonical figure inventory selected by validated content. Each approved
inventory has exactly three figures in a fixed order. The caller runs and
visually verifies the final output.

Text typesetting requires the four existing macOS Supplemental Times New Roman
TTF files listed in MACOS_TIMES_FONTS. They are read in place, never copied or
distributed. Missing or unreadable fonts stop the build without font fallback.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from dataclasses import dataclass
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PAPER_ROOT = ROOT / "manuscript/working-paper"
FIGURE_PATHS = (
    "figures/within-cell-paired-means.pdf",
    "figures/primary-monthly-paired-means.pdf",
    "figures/primary-resampling-ranges.pdf",
)
REVISION_FIGURE_PATHS = (
    "figures/within-cell-paired-means.pdf",
    "figures/revision-retrieval-contrasts.pdf",
    "figures/revision-retrieval-monthly.pdf",
)
APPROVED_FIGURE_INVENTORIES = (FIGURE_PATHS, REVISION_FIGURE_PATHS)
MACOS_TIMES_FONTS = {
    "PaperTimes": Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
    "PaperTimes-Bold": Path("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"),
    "PaperTimes-Italic": Path("/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"),
    "PaperTimes-BoldItalic": Path("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"),
}


class PaperBuildError(ValueError):
    """A concise fixed diagnostic, without arbitrary content coercion."""


def fail(code):
    raise PaperBuildError(code) from None


def mapping(value, keys, optional=()):
    if type(value) is not dict or not set(keys).issubset(value) or set(value) - set(keys) - set(optional):
        fail("INVALID_FIELDS")


def text(value, *, allow_empty=False):
    if type(value) is not str or (not allow_empty and not value.strip()):
        fail("INVALID_TEXT")
    return value


class MarkupValidator(HTMLParser):
    def __init__(self, links=False):
        super().__init__(convert_charrefs=False)
        self.allowed = {"b", "i", "sub", "super"} | ({"a"} if links else set())
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.allowed:
            fail("UNSUPPORTED_MARKUP")
        if tag == "a":
            if len(attrs) != 1 or attrs[0][0] != "href" or type(attrs[0][1]) is not str:
                fail("INVALID_REFERENCE_LINK")
            try:
                link = urlsplit(attrs[0][1])
                if link.scheme not in ("https", "http") or not link.hostname or link.username is not None or link.password is not None:
                    fail("INVALID_REFERENCE_LINK")
            except ValueError:
                fail("INVALID_REFERENCE_LINK")
        elif attrs:
            fail("UNSUPPORTED_MARKUP")
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            fail("UNBALANCED_MARKUP")

    def handle_startendtag(self, tag, attrs):
        fail("UNSUPPORTED_MARKUP")

    def handle_comment(self, data):
        fail("UNSUPPORTED_MARKUP")

    def handle_decl(self, decl):
        fail("UNSUPPORTED_MARKUP")

    def handle_pi(self, data):
        fail("UNSUPPORTED_MARKUP")


def markup(value, *, links=False):
    value = text(value)
    validator = MarkupValidator(links=links)
    validator.feed(value)
    validator.close()
    if validator.stack:
        fail("UNBALANCED_MARKUP")
    return value


def load_content(path):
    """Validate paper text and one complete, ordered canonical figure inventory."""
    with open(path, "r", encoding="utf-8") as source:
        content = json.load(source)
    mapping(content, ("title", "subtitle", "date", "abstract", "sections", "references", "figures"))
    text(content["title"])
    text(content["subtitle"], allow_empty=True)
    text(content["date"], allow_empty=True)
    markup(content["abstract"])
    if type(content["sections"]) is not list or not content["sections"]:
        fail("INVALID_SECTIONS")
    for section in content["sections"]:
        mapping(section, ("title", "blocks"))
        text(section["title"])
        if type(section["blocks"]) is not list:
            fail("INVALID_BLOCKS")
        for block in section["blocks"]:
            if type(block) is not dict or type(block.get("type")) is not str:
                fail("INVALID_BLOCK")
            kind = block["type"]
            if kind in ("p", "equation"):
                mapping(block, ("type", "html"), ("latex",) if kind == "equation" else ())
                markup(block["html"])
                if "latex" in block:
                    text(block["latex"])
            elif kind == "subheading":
                mapping(block, ("type", "text"))
                text(block["text"])
            elif kind == "table":
                mapping(block, ("type", "caption", "headers", "rows"))
                text(block["caption"])
                headers, rows = block["headers"], block["rows"]
                if type(headers) is not list or not headers or type(rows) is not list:
                    fail("INVALID_TABLE")
                for header in headers:
                    text(header)
                for row in rows:
                    if type(row) is not list or len(row) != len(headers):
                        fail("INVALID_TABLE")
                    for cell in row:
                        text(cell, allow_empty=True)
            else:
                fail("UNSUPPORTED_BLOCK_TYPE")
    if type(content["references"]) is not list:
        fail("INVALID_REFERENCES")
    reference_ids = set()
    for reference in content["references"]:
        mapping(reference, ("id", "html"))
        identifier = reference["id"]
        if type(identifier) not in (str, int) or (type(identifier) is str and not identifier.strip()):
            fail("INVALID_REFERENCE_ID")
        if identifier in reference_ids:
            fail("DUPLICATE_REFERENCE_ID")
        reference_ids.add(identifier)
        markup(reference["html"], links=True)
    if type(content["figures"]) is not list or len(content["figures"]) != 3:
        fail("INVALID_FIGURES")
    for figure in content["figures"]:
        mapping(figure, ("path", "caption"))
    if tuple(figure["path"] for figure in content["figures"]) not in APPROVED_FIGURE_INVENTORIES:
        fail("NONCANONICAL_FIGURE")
    for figure in content["figures"]:
        text(figure["caption"])
    return content


@dataclass(frozen=True)
class Layout:
    width: float
    height: float
    margin: float = 50.0

    @property
    def text_width(self):
        return self.width - 2 * self.margin


def make_styles():
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.styles import ParagraphStyle

    base = dict(fontName="PaperTimes", fontSize=10.5, leading=14, spaceAfter=6,
                splitLongWords=1, allowWidows=0, allowOrphans=0)
    body = ParagraphStyle("PaperBody", alignment=TA_JUSTIFY, **base)
    return {
        "body": body,
        "title": ParagraphStyle("PaperTitle", parent=body, fontName="PaperTimes-Bold", fontSize=17,
                                leading=21, alignment=TA_CENTER, spaceAfter=8),
        "subtitle": ParagraphStyle("PaperSubtitle", parent=body, fontName="PaperTimes-Italic", fontSize=11,
                                   leading=14, alignment=TA_CENTER, spaceAfter=6),
        "date": ParagraphStyle("PaperDate", parent=body, fontSize=9.5, leading=12,
                               alignment=TA_CENTER, spaceAfter=14),
        "section": ParagraphStyle("PaperSection", parent=body, fontName="PaperTimes-Bold", fontSize=12,
                                  leading=16, alignment=TA_LEFT, spaceBefore=12,
                                  spaceAfter=6, keepWithNext=True),
        "subheading": ParagraphStyle("PaperSubheading", parent=body, fontName="PaperTimes-Bold",
                                     alignment=TA_LEFT, spaceBefore=8, spaceAfter=4, keepWithNext=True),
        "equation": ParagraphStyle("PaperEquation", parent=body, fontSize=10, leading=14,
                                   alignment=TA_CENTER, spaceBefore=4, spaceAfter=8),
        "caption": ParagraphStyle("PaperCaption", parent=body, fontName="PaperTimes-Italic", fontSize=9.5,
                                  leading=12, alignment=TA_LEFT, spaceBefore=6, spaceAfter=5),
        "table_caption": ParagraphStyle("PaperTableCaption", parent=body, fontName="PaperTimes-Italic",
                                        fontSize=9.5, leading=12, alignment=TA_LEFT,
                                        spaceBefore=6, spaceAfter=5, keepWithNext=True),
        "table": ParagraphStyle("PaperTableCell", parent=body, fontSize=8.5, leading=11,
                                alignment=TA_LEFT, spaceAfter=0, allowWidows=1, allowOrphans=1),
        "table_header": ParagraphStyle("PaperTableHeader", parent=body, fontName="PaperTimes-Bold",
                                       fontSize=8.5, leading=11, alignment=TA_LEFT, spaceAfter=0,
                                       allowWidows=1, allowOrphans=1),
        "reference": ParagraphStyle("PaperReference", parent=body, fontSize=9.5, leading=12.5,
                                    alignment=TA_LEFT, spaceAfter=6),
    }


def make_table(block, styles, available_width):
    from reportlab.lib import colors
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.platypus import Paragraph, Table, TableStyle

    raw_rows = [block["headers"], *block["rows"]]
    natural_widths = []
    for index in range(len(block["headers"])):
        longest = max(stringWidth(row[index], "PaperTimes", 8.5) for row in raw_rows)
        natural_widths.append(min(180.0, max(38.0, longest + 10.0)))
    total = math.fsum(natural_widths)
    widths = [available_width * width / total for width in natural_widths]
    rows = [[Paragraph(escape(cell), styles["table_header" if j == 0 else "table"])
             for cell in row] for j, row in enumerate(raw_rows)]
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.95, 0.95, 0.95)),
    ]))
    return table


def make_story(content, styles, layout):
    from reportlab.platypus import Paragraph, Spacer

    story = [Paragraph(escape(content["title"]), styles["title"])]
    if content["subtitle"]:
        story.append(Paragraph(escape(content["subtitle"]), styles["subtitle"]))
    if content["date"]:
        story.append(Paragraph(escape(content["date"]), styles["date"]))
    story.extend([Paragraph("Abstract", styles["subheading"]),
                  Paragraph(content["abstract"], styles["body"]), Spacer(1, 6)])
    for section in content["sections"]:
        story.append(Paragraph(escape(section["title"]), styles["section"]))
        for block in section["blocks"]:
            kind = block["type"]
            if kind == "p":
                story.append(Paragraph(block["html"], styles["body"]))
            elif kind == "equation":
                story.append(Paragraph(block["html"], styles["equation"]))
            elif kind == "subheading":
                story.append(Paragraph(escape(block["text"]), styles["subheading"]))
            elif kind == "table":
                story.extend([Paragraph(escape(block["caption"]), styles["table_caption"]),
                              make_table(block, styles, layout.text_width), Spacer(1, 6)])
            else:
                fail("UNSUPPORTED_BLOCK_TYPE")
    story.append(Paragraph("References", styles["section"]))
    for reference in content["references"]:
        story.append(Paragraph(reference["html"], styles["reference"]))
    story.append(Paragraph("Figure captions", styles["section"]))
    for number, figure in enumerate(content["figures"], start=1):
        story.append(Paragraph(escape(figure["caption"]), styles["caption"]))
    return story


def check_output(path):
    """Require a new output distinct from every approved canonical figure input."""
    if path.exists() or path.is_symlink():
        fail("OUTPUT_ALREADY_EXISTS")
    if not path.parent.is_dir() or any(parent.is_symlink() for parent in path.parents):
        fail("INVALID_OUTPUT_DIRECTORY")
    if Path(os.path.abspath(path)) in {Path(os.path.abspath(PAPER_ROOT / figure))
                           for inventory in APPROVED_FIGURE_INVENTORIES for figure in inventory}:
        fail("OUTPUT_IS_SOURCE_FIGURE")


def register_paper_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for name, path in MACOS_TIMES_FONTS.items():
        if not path.is_file():
            fail("MISSING_REQUIRED_MACOS_FONT:" + path.name)
        try:
            pdfmetrics.registerFont(TTFont(name, str(path)))
        except Exception:
            fail("UNREADABLE_REQUIRED_MACOS_FONT:" + path.name)
    pdfmetrics.registerFontFamily("PaperTimes", normal="PaperTimes", bold="PaperTimes-Bold",
                                  italic="PaperTimes-Italic", boldItalic="PaperTimes-BoldItalic")


def build_paper(content_path, output_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    from pypdf import PdfReader, PdfWriter

    content = load_content(content_path)
    check_output(output_path)
    figure_files = [PAPER_ROOT / figure["path"] for figure in content["figures"]]
    for figure in figure_files:
        if not figure.is_file() or figure.is_symlink():
            fail("MISSING_CANONICAL_FIGURE")
    register_paper_fonts()
    scratch = ROOT / ".scratch"
    if any(parent.is_symlink() for parent in (scratch, *scratch.parents)):
        fail("INVALID_SCRATCH_DIRECTORY")
    scratch.mkdir(mode=0o700, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="paper-build-", dir=scratch))
    os.chmod(temporary, 0o700)
    body_path = temporary / "text-body.pdf"
    layout = Layout(*A4)
    styles = make_styles()

    def page_number(canvas, document):
        canvas.saveState()
        canvas.setAuthor("")
        canvas.setTitle(content["title"])
        canvas.setFont("Times-Roman", 8)
        canvas.drawCentredString(layout.width / 2, 25, str(document.page))
        canvas.restoreState()

    fd = os.open(body_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as target:
        document = BaseDocTemplate(target, pagesize=A4,
                                   rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50,
                                   title=content["title"], author="", subject=content["subtitle"],
                                   creator="", pageCompression=1)
        frame = Frame(50, 50, layout.text_width, layout.height - 100,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                      id="paper-body")
        document.addPageTemplates([PageTemplate(id="paper", frames=[frame], onPage=page_number)])
        document.build(make_story(content, styles, layout))
    with ExitStack() as opened:
        readers = [PdfReader(opened.enter_context(open(path, "rb")), strict=True)
                   for path in (body_path, *figure_files)]
        if readers[0].is_encrypted or not len(readers[0].pages):
            fail("INVALID_BODY_PDF")
        for reader in readers[1:]:
            if reader.is_encrypted or len(reader.pages) != 1:
                fail("INVALID_FIGURE_PDF")
        writer = PdfWriter()
        for reader in readers:
            for page in reader.pages:
                writer.add_page(page)
        writer.add_metadata({"/Title": content["title"], "/Author": "",
                             "/Subject": content["subtitle"], "/Creator": ""})
        # Exclusive creation never replaces an existing final paper or figure.
        fd = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as target:
            writer.write(target)
        body_pages = len(readers[0].pages)
        writer.close()
    return {"body_pages": body_pages, "figure_pages": 3, "total_pages": body_pages + 3,
            "body_pdf": str(body_path), "output_pdf": str(output_path)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=PAPER_ROOT / "paper-content.json")
    parser.add_argument("--output", type=Path, default=PAPER_ROOT / "paper.pdf")
    args = parser.parse_args(argv)
    try:
        result = build_paper(args.content, args.output)
    except PaperBuildError as error:
        print("PAPER_BUILD_ERROR:" + str(error), file=sys.stderr)
        return 1
    except Exception as error:
        print("PAPER_BUILD_ERROR:" + type(error).__name__, file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
