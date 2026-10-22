"""Original seven-cell display contract; no source observations or forecast run."""

import copy
import csv
from dataclasses import replace
import hashlib
import io
import json
import math
from pathlib import Path
import shutil
import tempfile
import unittest
import uuid

import build_original_comparison_figure as figures


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "results"
MANIFEST_SHA = "dc8f031892fb3794e5b6476d6bfcfe7e4f7745fbc16ca56c0697101db1dd14bc"
PAIRED_SHA = "f41325d5090b81c0251ed7dfe290bca42dc5e2bc690ff753b3673b72c7cd9adf"
OLD_FIGURE = ROOT / "manuscript/working-paper/figures/within-cell-paired-means.pdf"
OLD_FIGURE_SHA = "4ada53d86dad20d55bb2c19fe4b62b7e019269f246327f899234a82f5b0e0eb1"
PDF_NAME = "revision-original-contrasts.pdf"

# Independently transcribed accepted paired means, expressed once in USD millions.
EXPECTED = (
    ("main", 6, 720, 19, 20, 6625, -0.009374860250076379),
    ("h12", 12, 720, 19, 20, 6625, -0.01226339239575125),
    ("h24", 24, 720, 19, 20, 6625, +0.028685304973826256),
    ("n480", 6, 480, 19, 20, 6625, -0.010973039407515613),
    ("n1440", 6, 1440, 19, 20, 6625, -0.004481653197532082),
    ("tau90", 6, 720, 9, 10, 6625, +0.0001442255223117037),
    ("tau99", 6, 720, 99, 100, 6625, -0.004006922538233692),
)
EXPECTED_LABELS = ("-0.009375", "-0.012263", "+0.028685", "-0.010973",
                   "-0.004482", "+0.000144", "-0.004007")


def public_rows():
    return list(csv.DictReader(io.StringIO((PUBLIC / "paired-comparison.csv").read_text())))


class OriginalComparisonDataTests(unittest.TestCase):
    def test_all_seven_pinned_rows_keep_menu_order_sign_and_single_unit_conversion(self):
        # Catches omitted settings, H/n/tau swaps, absolute-value/sign changes and scaling twice.
        points, identity = figures.load_verified_results(PUBLIC)
        self.assertIsInstance(points, tuple)
        self.assertEqual(len(points), 7)
        for point, expected in zip(points, EXPECTED):
            self.assertEqual((point.cell_id, point.horizon, point.window,
                              point.tau_numerator, point.tau_denominator, point.origin_count),
                             expected[:6])
            self.assertAlmostEqual(point.value_millions, expected[6], places=16)
        self.assertGreater(points[5].value_millions, 0)
        self.assertLess(points[5].value_millions, 0.000145)
        self.assertEqual(identity["manifest_sha256"], MANIFEST_SHA)
        self.assertEqual(identity["inputs"]["paired-comparison.csv"],
                         {"bytes": 1657, "rows": 7, "sha256": PAIRED_SHA})

    def test_synthetic_signed_differences_are_scaled_once_and_not_recomputed(self):
        # Catches reading the relative-difference field or discarding positive/zero differences.
        rows = public_rows()
        for row in rows:
            row["mean_pinball_difference"] = "0"
            row["relative_difference_to_S"] = "0"
        rows[0].update(mean_pinball_difference="-2000000", relative_difference_to_S="-0.2")
        rows[2].update(mean_pinball_difference="3000000", relative_difference_to_S="0.3")
        points = figures.display_data(rows)
        self.assertEqual(tuple(p.value_millions for p in points), (-2.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0))

    def test_schema_menu_order_rank_and_nonfinite_display_values_fail_closed(self):
        # Catches accepting a different scientific menu or incomplete/ambiguous aggregate rows.
        base = public_rows()
        cases = [base[:-1], base + [copy.deepcopy(base[-1])]]
        rows = copy.deepcopy(base); rows[0], rows[1] = rows[1], rows[0]; cases.append(rows)
        changes = ((0, "cell_id", "other"), (2, "horizon", "6"), (3, "window", "720"),
                   (0, "horizon", "6.0"), (0, "tau_numerator", "19.0"),
                   (5, "tau_denominator", "20"), (0, "rank", "684"),
                   (0, "origin_count", "6624"), (0, "mean_pinball_difference", "NaN"),
                   (6, "mean_pinball_difference", "inf"))
        for index, key, value in changes:
            rows = copy.deepcopy(base); rows[index][key] = value; cases.append(rows)
        rows = copy.deepcopy(base); rows[0]["unexpected"] = "1"; cases.append(rows)
        rows = copy.deepcopy(base); del rows[0]["rank"]; cases.append(rows)
        for index, rows in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(ValueError):
                figures.display_data(rows)

    def test_byte_pins_and_regular_input_paths_cannot_be_bypassed(self):
        # Catches fail-open hash checks, symlink files and symlinked input ancestors.
        with tempfile.TemporaryDirectory(prefix="original-figure-input-", dir=ROOT / ".scratch") as raw:
            source = Path(raw)
            for target in ("run-manifest.json", "paired-comparison.csv"):
                for name in ("run-manifest.json", "paired-comparison.csv"):
                    (source / name).write_bytes((PUBLIC / name).read_bytes())
                with (source / target).open("ab") as stream:
                    stream.write(b" ")
                with self.subTest(tampered=target), self.assertRaises(ValueError):
                    figures.load_verified_results(source)
            for name in ("run-manifest.json", "paired-comparison.csv"):
                (source / name).write_bytes((PUBLIC / name).read_bytes())
            (source / "paired-comparison.csv").unlink()
            (source / "paired-comparison.csv").symlink_to(PUBLIC / "paired-comparison.csv")
            with self.assertRaises(ValueError):
                figures.load_verified_results(source)
            link = source / "linked-input"
            link.symlink_to(PUBLIC, target_is_directory=True)
            with self.assertRaises(ValueError):
                figures.load_verified_results(link)


class OriginalComparisonArtifactTests(unittest.TestCase):
    def new_output(self):
        path = ROOT / ".scratch" / ("revision-figure-original-test-" + uuid.uuid4().hex)
        self.addCleanup(lambda: shutil.rmtree(path) if path.exists() and not path.is_symlink() else None)
        return path

    def test_layout_keeps_exact_cells_labels_and_true_signed_axis_positions(self):
        # Catches a label/point mismatch, reversed axis, zeroed tau90 or clipped markers.
        points, _ = figures.load_verified_results()
        layout = figures.figure_layout(points)
        self.assertEqual(len(layout["points"]), 7)
        self.assertLess(layout["axis_limits"][0], -0.01226339239575125)
        self.assertGreater(layout["axis_limits"][1], 0.028685304973826256)
        for item, expected, label in zip(layout["points"], EXPECTED, EXPECTED_LABELS):
            self.assertEqual(item["cell_id"], expected[0])
            self.assertAlmostEqual(item["value_millions"], expected[6], places=16)
            self.assertEqual(item["label_text"], label)
            self.assertEqual(item["x"] < item["zero_x"], expected[6] < 0)
            self.assertEqual(item["x"] > item["zero_x"], expected[6] > 0)
            for key, bound in (("x", 841.8898), ("zero_x", 841.8898),
                               ("label_x", 841.8898), ("y", 595.2756), ("label_y", 595.2756)):
                self.assertTrue(0 < item[key] < bound, (expected[0], key))
        for left in layout["points"]:
            for right in layout["points"]:
                if left["value_millions"] < right["value_millions"]:
                    self.assertLess(left["x"], right["x"])

    def test_zero_positive_and_mixed_synthetic_layouts_are_finite_and_unclipped(self):
        # Catches positive-only axes, zero-span division and accidental absolute-value plotting.
        points, _ = figures.load_verified_results()
        for values in ((0.0,), (2.0, 3.0), (-2.0, 0.0, 3.0)):
            synthetic = tuple(replace(p, value_millions=values[i % len(values)])
                              for i, p in enumerate(points))
            layout = figures.figure_layout(synthetic)
            lower, upper = layout["axis_limits"]
            self.assertLess(lower, min(0.0, *values))
            self.assertGreater(upper, max(0.0, *values))
            for item in layout["points"]:
                self.assertTrue(math.isfinite(item["x"]))
                self.assertTrue(0 < item["x"] < 841.8898)
                self.assertEqual(item["x"] < item["zero_x"], item["value_millions"] < 0)
                self.assertEqual(item["x"] > item["zero_x"], item["value_millions"] > 0)
        invalid = tuple(replace(p, value_millions=math.nan if i == 0 else p.value_millions)
                        for i, p in enumerate(points))
        with self.assertRaises(ValueError):
            figures.figure_layout(invalid)

    def test_real_renderer_is_deterministic_vector_and_contains_every_signed_value(self):
        # Catches wrong PDF inventory, missing/rounded-away labels, raster fallback or overflow.
        from pypdf import PdfReader
        import pdfplumber
        first, second = self.new_output(), self.new_output()
        report = figures.build_figure(first)
        figures.build_figure(second)
        self.assertEqual(set(p.name for p in first.iterdir()), {PDF_NAME, "artifact-identity.json"})
        raw = (first / PDF_NAME).read_bytes()
        self.assertEqual(raw, (second / PDF_NAME).read_bytes())
        entry = report["artifacts"][PDF_NAME]
        self.assertEqual((entry["bytes"], entry["sha256"]), (len(raw), hashlib.sha256(raw).hexdigest()))
        saved = json.loads((first / "artifact-identity.json").read_text())
        self.assertEqual(saved, report)
        reader = PdfReader(first / PDF_NAME, strict=True)
        self.assertEqual(len(reader.pages), 1)
        page = reader.pages[0]
        self.assertAlmostEqual(float(page.mediabox.width), 841.8898, places=3)
        self.assertAlmostEqual(float(page.mediabox.height), 595.2756, places=3)
        self.assertEqual(len(page.images), 0)
        text = page.extract_text()
        for label in EXPECTED_LABELS:
            self.assertIn(label, text)
        self.assertIn("pinball", text.lower())
        self.assertIn("USD million", text)
        self.assertIn("F minus S", text)
        with pdfplumber.open(first / PDF_NAME) as doc:
            for char in doc.pages[0].chars:
                self.assertTrue(-0.01 <= char["x0"] <= char["x1"] <= doc.pages[0].width + 0.01)
                self.assertTrue(-0.01 <= char["top"] <= char["bottom"] <= doc.pages[0].height + 0.01)
        self.assertLess(report["resources"]["peak_rss_bytes"], 2 * 1024 ** 3)
        self.assertLess(report["resources"]["elapsed_seconds"], 600)
        self.assertLessEqual(report["resources"]["maximum_observed_os_threads"], 2)

    def test_existing_nested_traversal_symlink_and_canonical_outputs_are_rejected(self):
        # Catches overwrites or writes outside a new, direct task-owned scratch directory.
        existing = self.new_output(); existing.mkdir()
        (existing / "sentinel").write_text("keep")
        link = self.new_output(); link.symlink_to(existing, target_is_directory=True)
        self.addCleanup(link.unlink)
        outside = ROOT / ("revision-figure-outside-" + uuid.uuid4().hex)
        wrong_prefix = ROOT / ".scratch" / ("wrong-prefix-" + uuid.uuid4().hex)
        traversal = existing / ".." / ("revision-figure-traversal-" + uuid.uuid4().hex)
        protected = (PUBLIC / "run-manifest.json", PUBLIC / "paired-comparison.csv", OLD_FIGURE)
        before = {p: p.read_bytes() for p in protected}
        for path in (existing, existing / "revision-figure-nested", link,
                     outside, wrong_prefix, traversal, *protected):
            with self.subTest(path=str(path)), self.assertRaises((ValueError, FileExistsError)):
                figures.build_figure(path)
        self.assertEqual((existing / "sentinel").read_text(), "keep")
        self.assertEqual(sorted(p.name for p in existing.iterdir()), ["sentinel"])
        self.assertFalse(outside.exists())
        self.assertFalse(wrong_prefix.exists())
        self.assertFalse(Path(str(traversal)).absolute().exists())
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_build_preserves_the_original_figure_and_pinned_source_aggregates(self):
        # Catches replacing the historical figure or mutating the accepted original evidence.
        before = {p: p.read_bytes() for p in (OLD_FIGURE, PUBLIC / "run-manifest.json",
                                              PUBLIC / "paired-comparison.csv")}
        figures.build_figure(self.new_output())
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)
        self.assertEqual(hashlib.sha256(OLD_FIGURE.read_bytes()).hexdigest(), OLD_FIGURE_SHA)
        self.assertEqual(hashlib.sha256((PUBLIC / "run-manifest.json").read_bytes()).hexdigest(), MANIFEST_SHA)
        self.assertEqual(hashlib.sha256((PUBLIC / "paired-comparison.csv").read_bytes()).hexdigest(), PAIRED_SHA)


if __name__ == "__main__":
    unittest.main()
