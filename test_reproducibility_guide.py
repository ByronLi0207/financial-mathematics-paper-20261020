"""Guide-preservation regressions; temporary owned fixtures are retained."""

import unittest
from pathlib import Path
import tempfile


TITLE = "# Reproducibility, pre-specification and consulted editions"
BEGIN = "<!-- BEGIN REPRODUCIBILITY_V3 GENERATED -->"
END = "<!-- END REPRODUCIBILITY_V3 GENERATED -->"


class RebuildGuideTests(unittest.TestCase):
    def rebuild(self, previous, generated):
        try:
            from reproducibility_guide import rebuild_guide
        except ModuleNotFoundError as exc:
            if exc.name == "reproducibility_guide":
                self.fail("The guide-region helper has not been implemented")
            raise
        return rebuild_guide(previous, generated)

    def test_empty_migration_and_same_content_rebuild_are_idempotent(self):
        generated = TITLE + "\n\nGenerated information.\n"
        expected = BEGIN + "\n" + generated + END + "\n"
        migrated = self.rebuild("", generated)
        self.assertEqual(migrated, expected)
        self.assertEqual(self.rebuild(migrated, generated), expected)

    def test_legacy_migration_preserves_unknown_sections_verbatim(self):
        first = (
            "## Post-correction information\r\n\r\nKeep α exactly.\r\n"
            "```markdown\r\n## Original reference-edition notes retained verbatim\r\n"
            "This is a manual example, not a generated section.\r\n```\r\n\r\n"
        )
        second = "## New manual limitation\n\nKeep another paragraph.\n\n"
        last = "## Final hand note\n\nKeep the missing final newline."
        legacy = (
            TITLE + "\n\nOld generated preface.\n\n" + first
            + "## Original reference-edition notes retained verbatim\n\nOld references.\n\n"
            + second + "## Additional appendix execution records\n\nOld execution.\n\n"
            + last
        )
        generated = TITLE + "\n\nFresh generated content.\n"
        expected = BEGIN + "\n" + generated + END + "\n\n" + first + second + last
        migrated = self.rebuild(legacy, generated)
        self.assertEqual(migrated, expected)
        self.assertEqual(self.rebuild(migrated, generated), expected)

    def test_existing_region_update_preserves_both_manual_sides(self):
        prefix = "Manual preface α.\r\n\r\n"
        suffix = "\r\n\r\n## Post-correction information\n\nKeep this exactly.\r\n"
        previous = prefix + BEGIN + "\nOld generated material.\n" + END + suffix
        expected = prefix + BEGIN + "\nNew generated material.\n" + END + suffix
        self.assertEqual(self.rebuild(previous, "New generated material."), expected)

    def test_legacy_migration_preserves_indented_manual_headings(self):
        for spaces in range(4):
            with self.subTest(spaces=spaces):
                manual = " " * spaces + "## Manual\n\nRetain this paragraph exactly.\n"
                migrated = self.rebuild(TITLE + "\n\nOld generated preface.\n" + manual, "Fresh generated material.\n")
                self.assertTrue(migrated.endswith("\n\n" + manual))

    def test_file_input_preserves_crlf_outside_the_generated_region(self):
        import reproducibility_guide
        reader = getattr(reproducibility_guide, "read_guide_text", None)
        self.assertTrue(callable(reader), "The actual guide reader must preserve newline bytes")
        parent = Path(__file__).resolve().parent / ".scratch" / "guide-tests"
        parent.mkdir(parents=True, exist_ok=True)
        folder = Path(tempfile.mkdtemp(prefix="retained-", dir=parent))
        source = folder / "guide.md"
        before = "Manual prefix.\r\n" + BEGIN + "\r\nOld generated.\r\n" + END + "\r\nManual suffix.\r\n"
        source.write_bytes(before.encode("utf-8"))
        loaded = reader(source)
        self.assertEqual(loaded.encode("utf-8"), source.read_bytes())
        result = self.rebuild(loaded, "Fresh generated.\n")
        self.assertTrue(result.startswith("Manual prefix.\r\n"))
        self.assertTrue(result.endswith("\r\nManual suffix.\r\n"))
        self.assertEqual(reader(folder / "absent.md"), "")

    def test_malformed_or_duplicate_reserved_markers_fail_closed(self):
        malformed = [
            TITLE + "\n" + BEGIN,
            TITLE + "\n" + END,
            END + "\nold\n" + BEGIN,
            BEGIN + "\n" + BEGIN + "\nold\n" + END,
            BEGIN + "\nold\n" + END + "\n" + END,
            TITLE + "\ninline " + BEGIN + "\nold\n" + END,
        ]
        for previous in malformed:
            with self.subTest(previous=previous), self.assertRaises(ValueError):
                self.rebuild(previous, "Fresh content.")
        for generated in ["prefix " + BEGIN, END]:
            with self.subTest(generated=generated), self.assertRaises(ValueError):
                self.rebuild("", generated)

    def test_unknown_nonempty_legacy_header_fails_closed(self):
        for previous in [
            "# Unrelated document\n\n## Manual notes\nKeep me.\n",
            TITLE + " appended text\n\nDo not guess ownership.\n",
            " \n\t",
        ]:
            with self.subTest(previous=previous), self.assertRaises(ValueError):
                self.rebuild(previous, "Fresh content.")


if __name__ == "__main__":
    unittest.main()
