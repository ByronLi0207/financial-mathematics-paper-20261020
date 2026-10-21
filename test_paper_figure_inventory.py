"""Document inventory contracts using synthetic text and non-PDF sentinels only."""

from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
from types import ModuleType
import unittest
from unittest.mock import patch

import build_paper


ROOT = Path(__file__).resolve().parent
ORIGINAL = (
    "figures/within-cell-paired-means.pdf",
    "figures/primary-monthly-paired-means.pdf",
    "figures/primary-resampling-ranges.pdf",
)
REVISION = (
    "figures/within-cell-paired-means.pdf",
    "figures/revision-retrieval-contrasts.pdf",
    "figures/revision-retrieval-monthly.pdf",
)


def content_fixture(paths=ORIGINAL):
    return {
        "title": "Synthetic inventory fixture",
        "subtitle": "Document-only test",
        "date": "",
        "abstract": "A synthetic abstract without source observations.",
        "sections": [{"title": "Scope", "blocks": []}],
        "references": [],
        "figures": [{"path": path, "caption": f"Synthetic caption {number}."}
                    for number, path in enumerate(paths, start=1)],
    }


def synthetic_document_modules():
    """Replace rendering/parsing only; real builder file selection and I/O remain."""
    pagesizes = ModuleType("reportlab.lib.pagesizes")
    pagesizes.A4 = (595.0, 842.0)
    platypus = ModuleType("reportlab.platypus")
    pypdf = ModuleType("pypdf")

    class TextDocument:
        def __init__(self, target, **kwargs):
            self.target = target

        def addPageTemplates(self, templates):
            pass

        def build(self, story):
            self.target.write(b"BODY")

    class TextReader:
        def __init__(self, source, strict):
            if strict is not True:
                raise AssertionError("strict input parsing was disabled")
            self.is_encrypted = False
            self.pages = [source.read()]

    class TextWriter:
        def __init__(self):
            self.pages = []

        def add_page(self, page):
            self.pages.append(page)

        def add_metadata(self, metadata):
            pass

        def write(self, target):
            target.write(b"\n".join(self.pages))

        def close(self):
            pass

    platypus.BaseDocTemplate = TextDocument
    platypus.Frame = lambda *args, **kwargs: object()
    platypus.PageTemplate = lambda *args, **kwargs: object()
    pypdf.PdfReader = TextReader
    pypdf.PdfWriter = TextWriter
    return {"reportlab.lib.pagesizes": pagesizes, "reportlab.platypus": platypus,
            "pypdf": pypdf}


class PaperFigureInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(
            prefix="revision-document-inventory-test-", dir=ROOT / ".scratch")
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.content_path = self.folder / "synthetic-content.json"

    def load(self, content):
        self.content_path.write_text(json.dumps(content), encoding="utf-8")
        return build_paper.load_content(self.content_path)

    def test_exact_original_inventory_is_accepted(self):
        # Catches regression that drops the original manuscript's approved inventory.
        content = content_fixture(ORIGINAL)
        self.assertEqual(self.load(content), content)

    def test_exact_revision_inventory_is_accepted(self):
        # Catches refusal of the complete approved revision inventory.
        content = content_fixture(REVISION)
        self.assertEqual(self.load(content), content)

    def test_mixed_original_and_revision_paths_are_rejected(self):
        # Catches position-wise allowlists that permit unapproved mixed inventories.
        for paths in ((ORIGINAL[0], ORIGINAL[1], REVISION[2]),
                      (ORIGINAL[0], REVISION[1], ORIGINAL[2])):
            with self.subTest(paths=paths), self.assertRaisesRegex(
                    build_paper.PaperBuildError, "^NONCANONICAL_FIGURE$"):
                self.load(content_fixture(paths))

    def test_reordered_approved_figures_are_rejected(self):
        # Catches set membership replacing the required complete ordered tuple.
        for paths in (ORIGINAL, REVISION):
            for reordered in ((paths[1], paths[0], paths[2]),
                              (paths[0], paths[2], paths[1])):
                with self.subTest(paths=reordered), self.assertRaisesRegex(
                        build_paper.PaperBuildError, "^NONCANONICAL_FIGURE$"):
                    self.load(content_fixture(reordered))

    def test_unknown_substituted_and_repeated_paths_are_rejected(self):
        # Catches accepting generic PDFs, path aliases or repeated canonical inputs.
        for path in ("figures/unapproved.pdf", "/tmp/unapproved.pdf",
                     "figures/../figures/primary-monthly-paired-means.pdf",
                     ORIGINAL[0]):
            with self.subTest(path=path), self.assertRaisesRegex(
                    build_paper.PaperBuildError, "^NONCANONICAL_FIGURE$"):
                self.load(content_fixture((ORIGINAL[0], path, ORIGINAL[2])))

    def test_missing_or_extra_figures_are_rejected(self):
        # Catches missing/extra figures being accepted through truncated zip logic.
        for paths in ((), ORIGINAL[:2], REVISION[:2], (*REVISION, ORIGINAL[1])):
            with self.subTest(paths=paths), self.assertRaisesRegex(
                    build_paper.PaperBuildError, "^INVALID_FIGURES$"):
                self.load(content_fixture(paths))

    def test_figure_container_must_be_a_list(self):
        # Catches weakening the figure-list schema.
        for value in (None, {}, "figures"):
            content = content_fixture()
            content["figures"] = value
            with self.subTest(value=value), self.assertRaisesRegex(
                    build_paper.PaperBuildError, "^INVALID_FIGURES$"):
                self.load(content)

    def test_each_figure_requires_only_path_and_caption_fields(self):
        # Catches silently accepting malformed figure records or unknown fields.
        for value in (None, [], {"path": ORIGINAL[1]},
                      {"caption": "Missing path"},
                      {"path": ORIGINAL[1], "caption": "Caption", "extra": True}):
            content = content_fixture()
            content["figures"][1] = value
            with self.subTest(value=value), self.assertRaisesRegex(
                    build_paper.PaperBuildError, "^INVALID_FIELDS$"):
                self.load(content)

    def test_invalid_captions_are_rejected_for_both_approved_inventories(self):
        # Catches bypassing existing caption validation for the added inventory.
        for paths in (ORIGINAL, REVISION):
            for value in ("", " ", None, 12, []):
                content = content_fixture(paths)
                content["figures"][1]["caption"] = value
                with self.subTest(paths=paths, value=value), self.assertRaisesRegex(
                        build_paper.PaperBuildError, "^INVALID_TEXT$"):
                    self.load(content)

    def test_nonstring_paths_raise_a_controlled_inventory_error(self):
        # Catches accidental unhashable errors or coercion into canonical paths.
        for value in (None, 0, [], {}, [ORIGINAL[1]]):
            content = content_fixture()
            content["figures"][1]["path"] = value
            with self.subTest(value=value), self.assertRaisesRegex(
                    build_paper.PaperBuildError, "^NONCANONICAL_FIGURE$"):
                self.load(content)

    def test_absent_inputs_from_both_inventories_are_protected_as_outputs(self):
        # Catches allowing creation over a missing newly approved source path.
        paper_root = self.folder / "paper"
        (paper_root / "figures").mkdir(parents=True)
        with patch.object(build_paper, "PAPER_ROOT", paper_root):
            for name in ("within-cell-paired-means.pdf", "primary-monthly-paired-means.pdf",
                         "primary-resampling-ranges.pdf", "revision-retrieval-contrasts.pdf",
                         "revision-retrieval-monthly.pdf"):
                path = paper_root / "figures" / name
                with self.subTest(path=name), self.assertRaisesRegex(
                        build_paper.PaperBuildError, "^OUTPUT_IS_SOURCE_FIGURE$"):
                    build_paper.check_output(path)
                self.assertFalse(path.exists())

    def test_absent_canonical_input_aliases_are_protected_as_outputs(self):
        # Lexical parent segments must not bypass protection of missing inputs.
        paper_root = self.folder / "paper"
        (paper_root / "figures").mkdir(parents=True)
        with patch.object(build_paper, "PAPER_ROOT", paper_root):
            for name in ("within-cell-paired-means.pdf", "primary-monthly-paired-means.pdf",
                         "primary-resampling-ranges.pdf", "revision-retrieval-contrasts.pdf",
                         "revision-retrieval-monthly.pdf"):
                alias = paper_root / "figures" / ".." / "figures" / name
                with self.subTest(path=name), self.assertRaisesRegex(
                        build_paper.PaperBuildError, "^OUTPUT_IS_SOURCE_FIGURE$"):
                    build_paper.check_output(alias)
                self.assertFalse((paper_root / "figures" / name).exists())

    def test_ordinary_new_output_is_allowed_and_existing_output_is_preserved(self):
        # Catches overbroad output blocking and loss of exclusive-output protection.
        output = self.folder / "synthetic-output.bin"
        build_paper.check_output(output)
        output.write_bytes(b"keep")
        with self.assertRaisesRegex(build_paper.PaperBuildError, "^OUTPUT_ALREADY_EXISTS$"):
            build_paper.check_output(output)
        self.assertEqual(output.read_bytes(), b"keep")

    def run_synthetic_build(self, paths):
        paper_root = self.folder / "paper"
        (paper_root / "figures").mkdir(parents=True)
        for name, sentinel in (
                ("within-cell-paired-means.pdf", b"WITHIN"),
                ("primary-monthly-paired-means.pdf", b"OLDMONTH"),
                ("primary-resampling-ranges.pdf", b"OLDRANGE"),
                ("revision-retrieval-contrasts.pdf", b"NEWCONTRAST"),
                ("revision-retrieval-monthly.pdf", b"NEWMONTH")):
            (paper_root / "figures" / name).write_bytes(sentinel)
        self.content_path.write_text(json.dumps(content_fixture(paths)), encoding="utf-8")
        output = self.folder / "synthetic-assembled-output.bin"
        with ExitStack() as patched:
            patched.enter_context(patch.dict("sys.modules", synthetic_document_modules()))
            patched.enter_context(patch.object(build_paper, "ROOT", self.folder))
            patched.enter_context(patch.object(build_paper, "PAPER_ROOT", paper_root))
            patched.enter_context(patch.object(build_paper, "register_paper_fonts", lambda: None))
            patched.enter_context(patch.object(build_paper, "make_styles", lambda: {}))
            patched.enter_context(patch.object(build_paper, "make_story", lambda *args: []))
            report = build_paper.build_paper(self.content_path, output)
        self.assertEqual(report["figure_pages"], 3)
        self.assertEqual(report["total_pages"], 4)
        return output.read_bytes()

    def test_builder_appends_the_original_inventory_in_order(self):
        # Catches altered original inventory selection even when all five files exist.
        self.assertEqual(self.run_synthetic_build(ORIGINAL), b"BODY\nWITHIN\nOLDMONTH\nOLDRANGE")

    def test_builder_appends_the_revision_inventory_in_order(self):
        # Catches retaining the old hardcoded append paths after accepting revisions.
        self.assertEqual(self.run_synthetic_build(REVISION), b"BODY\nWITHIN\nNEWCONTRAST\nNEWMONTH")


if __name__ == "__main__":
    unittest.main()
