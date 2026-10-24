"""Document-only report routing checks in preserved isolated fixture trees.

The packager is copied into each fresh fixture so its ordinary __file__ root
resolution applies. No production root, validation guard, or report is patched.
Fixtures are retained; the tests never delete files or run financial software.
"""
import importlib.util
import inspect
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("seal_wp8_delivery.py")
DEFAULT_MAIN = "notes/revision-v8/wp8-main-number-check-root.json"
DEFAULT_SUPP = "notes/revision-v8/wp8-supp-number-check-final-layout.json"
NEW_MAIN = "notes/revision-v8/review-main.json"
NEW_SUPP = "notes/revision-v8/wp8-supp-review-number-check.json"


class PackageReportRoutingTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="v8-package-report-test-"))
        self.script = self.root / "notes/revision-v8/seal_wp8_delivery.py"
        self.script.parent.mkdir(parents=True)
        shutil.copy2(SCRIPT, self.script)
        spec = importlib.util.spec_from_file_location("isolated_sealer", self.script)
        self.sealer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.sealer)
        self.delivery = self.root / "submission-jof"
        self.delivery.mkdir()
        (self.delivery / "main.tex").write_text(r"\input{manuscript}")
        inputs = []
        for index in range(5):
            figure = self.delivery / f"figures/f{index}.pdf"
            figure.parent.mkdir(exist_ok=True)
            figure.write_bytes(b"fake-figure")
            generated = self.delivery / f"generated/g{index}.tex"
            generated.parent.mkdir(exist_ok=True)
            generated.write_text("fixture table")
            inputs += [rf"\includegraphics{{figures/f{index}.pdf}}",
                       rf"\input{{generated/g{index}}}"]
        (self.delivery / "manuscript.tex").write_text("\n".join(inputs))
        (self.delivery / "supplement.tex").write_text("fixture supplement")
        (self.delivery / "title-page.tex").write_text("fixture title")
        for name in ("references.bib", "README.md", "AUTHOR-TODO.md", "cover-letter.md"):
            (self.delivery / name).write_text("fixture document")
        self.pdfs = []
        for stem in ("manuscript", "supplement", "title-page"):
            path = self.root / (stem + "-compiled.pdf")
            path.write_bytes(("fake compiled " + stem).encode())
            self.pdfs.append(path)
        self.main_report = {
            "status": "PASS",
            "current_main_sha256": self.sealer.sha(self.delivery / "manuscript.tex"),
        }
        self.supp_report = {
            "status": "PASS_WITH_SCOPE_LIMITS",
            "files": {"submission-jof/supplement.tex": {
                "sha256": self.sealer.sha(self.delivery / "supplement.tex")}},
        }
        self.write_report(DEFAULT_MAIN, self.main_report)
        self.write_report(DEFAULT_SUPP, self.supp_report)

    def write_report(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))

    def require_options(self):
        parameters = inspect.signature(self.sealer.package).parameters
        self.assertIn("main_numeric_report", parameters)
        self.assertIn("supp_numeric_report", parameters)

    def snapshot(self, stem):
        return json.loads((self.delivery / (stem + "-content.json")).read_text())

    def assert_no_delivery_side_effects(self):
        self.assertFalse((self.delivery / "overleaf-package.zip").exists())
        for stem in ("manuscript", "supplement", "title-page"):
            self.assertFalse((self.delivery / (stem + ".pdf")).exists())
            self.assertFalse((self.delivery / (stem + "-preview.pdf")).exists())
            self.assertFalse((self.delivery / (stem + "-content.json")).exists())

    def test_defaults_preserve_existing_report_paths(self):
        result = self.sealer.package(*self.pdfs)
        self.assertTrue(result["all_members_match_current_sources"])
        self.assertEqual(self.snapshot("manuscript")["source_bindings"], "../" + DEFAULT_MAIN)
        self.assertEqual(self.snapshot("supplement")["source_bindings"], "../" + DEFAULT_SUPP)

    def test_explicit_reports_are_checked_and_recorded(self):
        self.require_options()
        self.write_report(NEW_MAIN, self.main_report)
        self.write_report(NEW_SUPP, self.supp_report)
        self.write_report(DEFAULT_MAIN, {"status": "FAIL"})
        self.write_report(DEFAULT_SUPP, {"status": "FAIL"})
        self.sealer.package(*self.pdfs, main_numeric_report=NEW_MAIN,
                            supp_numeric_report=NEW_SUPP)
        self.assertEqual(self.snapshot("manuscript")["source_bindings"], "../" + NEW_MAIN)
        self.assertEqual(self.snapshot("supplement")["source_bindings"], "../" + NEW_SUPP)

    def test_supplement_override_keeps_main_default(self):
        self.require_options()
        self.write_report(NEW_SUPP, self.supp_report)
        self.write_report(DEFAULT_SUPP, {"status": "FAIL"})
        self.sealer.package(*self.pdfs, supp_numeric_report=Path(NEW_SUPP))
        self.assertEqual(self.snapshot("manuscript")["source_bindings"], "../" + DEFAULT_MAIN)
        self.assertEqual(self.snapshot("supplement")["source_bindings"], "../" + NEW_SUPP)

    def test_wrong_supplement_hash_fails_before_copy(self):
        self.require_options()
        bad = json.loads(json.dumps(self.supp_report))
        bad["files"]["submission-jof/supplement.tex"]["sha256"] = "0" * 64
        self.write_report(NEW_SUPP, bad)
        with self.assertRaises(AssertionError):
            self.sealer.package(*self.pdfs, supp_numeric_report=NEW_SUPP)
        self.assert_no_delivery_side_effects()

    def test_wrong_main_hash_fails_before_copy(self):
        self.require_options()
        bad = dict(self.main_report, current_main_sha256="0" * 64)
        self.write_report(NEW_MAIN, bad)
        with self.assertRaises(AssertionError):
            self.sealer.package(*self.pdfs, main_numeric_report=NEW_MAIN)
        self.assert_no_delivery_side_effects()

    def test_wrong_statuses_fail_before_copy(self):
        self.require_options()
        for stem, path, report, wrong_status in (
                ("main", NEW_MAIN, self.main_report, "PASS_WITH_SCOPE_LIMITS"),
                ("supp", NEW_SUPP, self.supp_report, "PASS")):
            with self.subTest(stem=stem):
                self.write_report(path, dict(report, status=wrong_status))
                options = {"main_numeric_report" if stem == "main" else "supp_numeric_report": path}
                with self.assertRaises(AssertionError):
                    self.sealer.package(*self.pdfs, **options)
                self.assert_no_delivery_side_effects()

    def test_cli_routes_only_the_supplement_override(self):
        self.write_report(NEW_SUPP, self.supp_report)
        self.write_report(DEFAULT_SUPP, {"status": "FAIL"})
        output = self.root / "fixture-package-receipt.json"
        command = [sys.executable, "-B", str(self.script),
                   "--main-pdf", str(self.pdfs[0]),
                   "--supplement-pdf", str(self.pdfs[1]),
                   "--title-pdf", str(self.pdfs[2]),
                   "--supp-numeric-report", NEW_SUPP,
                   "--output", str(output)]
        result = subprocess.run(command, cwd=self.root, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(json.loads(output.read_text())["all_members_match_current_sources"])
        self.assertEqual(self.snapshot("manuscript")["source_bindings"], "../" + DEFAULT_MAIN)
        self.assertEqual(self.snapshot("supplement")["source_bindings"], "../" + NEW_SUPP)


if __name__ == "__main__":
    unittest.main(verbosity=2)
