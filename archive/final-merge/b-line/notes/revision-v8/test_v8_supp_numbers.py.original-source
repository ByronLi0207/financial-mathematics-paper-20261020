"""Frozen PR #5 v8 negative controls; mutations use fresh scratch copies.

No financial model, data input, simulation or statistical test is executed.
All original assertions/source guards are retained; the v9 draft is not the
document-under-test for these version-specific historical cases.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN = ROOT / 'fixtures/v9-baselines/pr5-v8'
BASE_COMMIT = '0f1f066843e0c49cf3e24bce7d72032dc189603d'
spec = importlib.util.spec_from_file_location("wp8_supp_numbers", HERE / "check_wp8_supp_numbers.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def frozen_document(name):
    assert (FROZEN/'manifest.json').is_file(), 'frozen public PR #5 document fixtures missing'
    manifest=json.loads((FROZEN/'manifest.json').read_text())
    assert manifest['source_commit']==BASE_COMMIT
    source=FROZEN/name;raw=source.read_bytes();entry=manifest['members'][name]
    assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256']
    return source


class SupplementNumericControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="wp8-supp-negative-")
        self.docs = Path(self.tmp.name)
        for name in ["submission-jof/supplement.tex", *checker.EXPECTED_INPUTS]:
            target = self.docs / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(frozen_document(name), target)

    def tearDown(self):
        self.tmp.cleanup()

    def run_audit(self):
        return checker.audit(ROOT, self.docs)

    def mutate_main(self, before, after):
        path = self.docs / "submission-jof/supplement.tex"
        text = path.read_text()
        self.assertIn(before, text)
        path.write_text(text.replace(before, after, 1))

    def test_current_document_has_no_numeric_residuals(self):
        report = self.run_audit()
        self.assertEqual(report["failures"], [])
        self.assertEqual(report["unresolved"], [])
        self.assertEqual(report["ambiguous"], [])
        self.assertEqual(report["status"], "PASS_WITH_SCOPE_LIMITS")

    def test_swapped_mc_rows_fail_ordered_identity_binding(self):
        path = self.docs / checker.EXPECTED_INPUTS[0]
        lines = path.read_text().splitlines(keepends=True)
        indices = [i for i, line in enumerate(lines) if line.startswith("6 & ")]
        lines[indices[0]], lines[indices[1]] = lines[indices[1]], lines[indices[0]]
        path.write_text("".join(lines))
        report = self.run_audit()
        self.assertTrue(any(f["gate"] == "mc_ordered_rows" for f in report["failures"]))

    def test_wrong_master_entropy_is_rejected_exactly(self):
        self.mutate_main("master entropy 2026102408", "master entropy 2026102409")
        report = self.run_audit()
        self.assertTrue(any(f["gate"] == "new_exact_passage" for f in report["failures"]))

    def test_unbound_inline_p_is_not_classified_as_math(self):
        self.mutate_main("\\section{Reproduction, availability", "An additional result is \\(p=0.055\\).\n\\section{Reproduction, availability")
        report = self.run_audit()
        residual = [r for r in report["unresolved"] if r.get("token") == "0.055"]
        self.assertTrue(residual, report["status"])
        self.assertEqual(report["status"], "NEEDS_REVIEW")

    def test_unbound_result_beside_layout_command_is_not_exempt(self):
        self.mutate_main("\\includegraphics[width=.96\\linewidth]{figures/v8-wp3-qr4-loss.pdf}", "\\includegraphics[width=.96\\linewidth]{figures/v8-wp3-qr4-loss.pdf} Additional result \\(p=0.055\\).")
        report = self.run_audit()
        self.assertTrue(any(r.get('token')=='0.055' for r in report['unresolved']))

    def test_omitted_generated_table_is_rejected(self):
        self.mutate_main("\\input{generated/v8-daily-results-table.tex}", "")
        report = self.run_audit()
        self.assertTrue(any(f["gate"] == "required_generated_inputs" for f in report["failures"]))

    def test_changed_old_numeric_row_is_rejected(self):
        self.mutate_main("156123.03 & 166531.06", "156123.04 & 166531.06")
        report = self.run_audit()
        self.assertTrue(any(f["gate"] == "old_ordered_rows" for f in report["failures"]))

    def test_numeric_native_types_are_not_coerced(self):
        self.assertFalse(checker.identical(True, 1))
        self.assertFalse(checker.identical(1, 1.0))
        self.assertTrue(checker.identical({"v": [1, 0.7]}, {"v": [1, 0.7]}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
