"""Document identity checks independent of financial data or result tables."""

import unittest

import build_tex


class PaperMetadataTests(unittest.TestCase):
    def test_revised_mathematical_prose_has_portable_tex_symbols(self):
        self.assertEqual(
            build_tex.esc("Δ μ φ ∈"),
            r"\(\Delta\) \(\mu\) \(\phi\) \(\in\)",
        )

    def test_metadata_and_display_title_follow_the_supplied_title(self):
        content = {
            "title": "State & response: a 5% comparison",
            "subtitle": "A finite application",
            "date": "Working paper",
            "abstract": "A synthetic document identity fixture.",
            "sections": [{"title": "Scope", "blocks": []}],
            "references": [],
            "figures": [],
        }
        source = build_tex.build_source(content)
        escaped = r"State \& response: a 5\% comparison"
        self.assertIn(r"\hypersetup{pdftitle={" + escaped + r"},pdfauthor={}}", source)
        self.assertIn(r"{\LARGE\bfseries " + escaped + "}", source)
        self.assertNotIn("Historical Headrooms versus Current-State Scenarios", source)


if __name__ == "__main__":
    unittest.main()
