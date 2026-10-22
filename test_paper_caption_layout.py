"""Exercise caption pagination at the real PDF boundary using synthetic text."""

from io import BytesIO
import unittest

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

import build_paper


CAPTION_MARKERS = ("CAPTIONALPHA", "CAPTIONBETA", "CAPTIONGAMMA")


def caption_fixture(reference_count):
    return {
        "title": "Synthetic caption boundary",
        "subtitle": "",
        "date": "",
        "abstract": "Synthetic abstract.",
        "sections": [{"title": "Scope", "blocks": []}],
        "references": [
            {"id": number, "html": f"Reference {number}. A short synthetic reference."}
            for number in range(1, reference_count + 1)
        ],
        "figures": [
            {
                "path": path,
                "caption": (
                    f"Figure {number}. "
                    "Synthetic caption text explains the displayed comparison without source observations. "
                    "Synthetic caption text explains the displayed comparison without source observations. "
                    "Synthetic caption text explains the displayed comparison without source observations. "
                    + marker
                ),
            }
            for number, (path, marker) in enumerate(zip((
                "figures/within-cell-paired-means.pdf",
                "figures/primary-monthly-paired-means.pdf",
                "figures/primary-resampling-ranges.pdf",
            ), CAPTION_MARKERS), start=1)
        ],
    }


def rendered_pages(reference_count):
    """Run the production story through real typesetting and strict PDF parsing."""
    layout = build_paper.Layout(*A4)
    styles = build_paper.make_styles()
    # Keep production dimensions/spacing; portable built-in fonts avoid macOS files.
    fonts = {
        "PaperTimes": "Times-Roman",
        "PaperTimes-Bold": "Times-Bold",
        "PaperTimes-Italic": "Times-Italic",
        "PaperTimes-BoldItalic": "Times-BoldItalic",
    }
    for style in styles.values():
        style.fontName = fonts[style.fontName]
    target = BytesIO()
    document = BaseDocTemplate(target, pagesize=A4, leftMargin=50, rightMargin=50,
                               topMargin=50, bottomMargin=50)
    frame = Frame(50, 50, layout.text_width, layout.height - 100,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  id="synthetic-body")
    document.addPageTemplates([PageTemplate(id="synthetic", frames=[frame])])
    document.build(build_paper.make_story(caption_fixture(reference_count), styles, layout))
    reader = PdfReader(BytesIO(target.getvalue()), strict=True)
    return [page.extract_text() for page in reader.pages]


class PaperCaptionLayoutTests(unittest.TestCase):
    def assert_caption_block_on_page(self, pages, page_number):
        for marker in ("Figure captions", *CAPTION_MARKERS):
            with self.subTest(marker=marker):
                self.assertEqual(sum(page.count(marker) for page in pages), 1)
                self.assertEqual(
                    [number for number, page in enumerate(pages, start=1) if marker in page],
                    [page_number],
                    f"{marker} was separated from the caption block",
                )

    def test_caption_block_moves_together_when_final_caption_would_be_orphaned(self):
        # Catches independent caption flowables: 25 references leave room for only
        # the heading and first two captions, although the whole block fits page 2.
        pages = rendered_pages(reference_count=25)
        self.assertEqual(len(pages), 2)
        self.assertIn("Reference 25.", pages[0])
        self.assert_caption_block_on_page(pages, page_number=2)

    def test_caption_block_stays_on_current_page_when_it_fits(self):
        # Catches an unconditional page break that would waste the available room.
        pages = rendered_pages(reference_count=0)
        self.assertEqual(len(pages), 1)
        self.assert_caption_block_on_page(pages, page_number=1)


if __name__ == "__main__":
    unittest.main()
