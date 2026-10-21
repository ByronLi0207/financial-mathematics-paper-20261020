"""Aggregate-only figure checks; fixtures never load source observations."""

import copy
import csv
import hashlib
import importlib
import io
import json
import math
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "results" / "revision-20261021"
PYTHON = "/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"

try:
    figures = importlib.import_module("build_revision_figures")
except ModuleNotFoundError as exc:
    if exc.name != "build_revision_figures":
        raise
    figures = None


def public_rows(name):
    return list(csv.DictReader(io.StringIO((PUBLIC / name).read_text(encoding="utf-8"))))


class RevisionFigureDataTests(unittest.TestCase):
    def builder(self):
        self.assertIsNotNone(figures, "aggregate-only figure builder is missing")
        return figures

    def test_all_twelve_contrasts_are_extracted_in_frozen_order_with_usd_million_units(self):
        # Catches wrong subset, F-minus-S leakage, method/H/m swaps, or 1e6 error.
        data = self.builder().display_data(public_rows("comparisons.csv"), public_rows("monthly.csv"))
        expected = [
            (6, 360, "F", -0.005424719981816602),
            (6, 360, "S", -0.018947342324827627),
            (6, 360, "K", -0.2777044657473585),
            (6, 180, "F", -0.017733389718916966),
            (6, 180, "S", -0.01934777781268045),
            (6, 180, "K", -0.26040704476271698),
            (24, 360, "F", -0.016304833238710946),
            (24, 360, "S", -0.053693152344350805),
            (24, 360, "K", -0.2859339678602264),
            (24, 180, "F", -0.010480277164669433),
            (24, 180, "S", -0.06841309302911171),
            (24, 180, "K", -0.32016101687894337),
        ]
        self.assertEqual(len(data.contrasts), 12)
        for point, (horizon, count, method, value) in zip(data.contrasts, expected):
            self.assertEqual((point.horizon, point.count, point.method, point.origin_count),
                             (horizon, count, method, 6625))
            self.assertAlmostEqual(point.value_millions, value, places=14)
        self.assertEqual([(p.horizon, p.count, p.method) for p in data.contrasts if p.primary],
                         [(6, 360, "K")])

    def test_all_monthly_values_and_counts_include_both_positive_january_values(self):
        # Catches favorable-month filtering, horizon swaps, month/count drift or wrong units.
        data = self.builder().display_data(public_rows("comparisons.csv"), public_rows("monthly.csv"))
        expected = [
            (6, "2016-01", 504, 0.003379202671130899),
            (6, "2016-02", 504, -0.3669779044940477),
            (6, "2016-03", 552, -0.21149891870561618),
            (6, "2016-04", 502, -0.5228371073446215),
            (6, "2016-05", 530, -0.4325947091320754),
            (6, "2016-06", 528, -0.236362239282197),
            (6, "2016-07", 504, -0.21317523093948414),
            (6, "2016-08", 552, -0.49449830939855083),
            (6, "2016-09", 526, -0.23685027831654),
            (6, "2016-10", 506, -0.23055153645355738),
            (6, "2016-11", 528, -0.22004531861931813),
            (6, "2016-12", 526, -0.32357084552376426),
            (6, "2017-01", 363, -0.04194035996143251),
            (24, "2016-01", 504, 0.52044745803670626),
            (24, "2016-02", 504, -0.4068034682628969),
            (24, "2016-03", 552, -0.08623247632608683),
            (24, "2016-04", 502, -0.5899708175846615),
            (24, "2016-05", 530, -0.3527344066481131),
            (24, "2016-06", 528, -0.10578481239962115),
            (24, "2016-07", 504, -0.4949428393948412),
            (24, "2016-08", 552, -0.6856965832644927),
            (24, "2016-09", 526, -0.338211527026616),
            (24, "2016-10", 506, -0.13551585372727268),
            (24, "2016-11", 528, -0.3107681063929925),
            (24, "2016-12", 526, -0.4229384731017111),
            (24, "2017-01", 363, -0.2866188067327824),
        ]
        self.assertEqual(len(data.monthly), 26)
        for point, (horizon, month, count, value) in zip(data.monthly, expected):
            self.assertEqual((point.horizon, point.month, point.origin_count), (horizon, month, count))
            self.assertAlmostEqual(point.value_millions, value, places=14)

    def test_zero_positive_and_negative_values_have_signed_unclipped_positions(self):
        # Catches plots assuming all values are negative or reversing the money axis.
        module = self.builder()
        for values in ((-2.0, 0.0, 4.0), (0.0, 0.0), (2.0, 4.0), (-4.0, -2.0)):
            with self.subTest(values=values):
                scale = module.money_scale(values, 100.0, 400.0)
                self.assertLess(scale.lower, min(0.0, *values))
                self.assertGreater(scale.upper, max(0.0, *values))
                zero = scale.position(0.0)
                self.assertGreater(zero, 103.0)
                self.assertLess(zero, 397.0)
                for value in values:
                    point = scale.position(value)
                    self.assertTrue(103.0 < point < 397.0)
                    self.assertEqual(point < zero, value < 0)
                    self.assertEqual(point > zero, value > 0)
        with self.assertRaises(ValueError):
            module.money_scale((math.nan,), 100, 400)

    def test_small_synthetic_fixture_keeps_signed_literal_values(self):
        # Catches accidental absolute value or scaling twice, without observed values.
        # Synthetic 22/26-row menu: no accepted numeric values enter this fixture.
        comparison = []
        monthly = []
        months_and_counts = [("2016-01", 504), ("2016-02", 504), ("2016-03", 552),
                             ("2016-04", 502), ("2016-05", 530), ("2016-06", 528),
                             ("2016-07", 504), ("2016-08", 552), ("2016-09", 526),
                             ("2016-10", 506), ("2016-11", 528), ("2016-12", 526),
                             ("2017-01", 363)]
        for horizon in ("6", "24"):
            for count in ("360", "180"):
                for method in ("F", "S", "K"):
                    comparison.append(dict(horizon=horizon, contrast_id="nearest_minus_recent",
                                           left_set="nearest" + count, right_set="recent" + count,
                                           left_method=method, right_method=method,
                                           origin_count="6625", mean_pinball_difference="0"))
            for selected in ("full720", "recent360", "nearest360", "recent180", "nearest180"):
                comparison.append(dict(horizon=horizon, contrast_id="F_minus_S", left_set=selected,
                                       right_set=selected, left_method="F", right_method="S",
                                       origin_count="6625", mean_pinball_difference="0"))
            for month, count in months_and_counts:
                monthly.append(dict(horizon=horizon, month=month, origin_count=str(count),
                                    status="DISPLAYED", mean_pinball_nearest360_K="7",
                                    mean_pinball_recent360_K="7", mean_pinball_difference="0",
                                    undefined_reason=""))
        comparison[0]["mean_pinball_difference"] = "-2000000"
        comparison[1]["mean_pinball_difference"] = "3000000"
        for row in monthly:
            row.update(mean_pinball_nearest360_K="7", mean_pinball_recent360_K="7",
                       mean_pinball_difference="0")
        monthly[0].update(mean_pinball_nearest360_K="1", mean_pinball_recent360_K="2000001",
                          mean_pinball_difference="-2000000")
        monthly[13].update(mean_pinball_nearest360_K="3000007", mean_pinball_recent360_K="7",
                           mean_pinball_difference="3000000")
        data = self.builder().display_data(comparison, monthly)
        self.assertEqual([p.value_millions for p in data.contrasts[:3]], [-2.0, 3.0, 0.0])
        self.assertEqual((data.monthly[0].value_millions, data.monthly[13].value_millions), (-2.0, 3.0))

    def test_identity_order_row_counts_columns_and_nonfinite_values_are_rejected(self):
        # Catches fail-open parsing even if caller has in-memory rows.
        module = self.builder()
        base_c = public_rows("comparisons.csv")
        base_m = public_rows("monthly.csv")
        cases = []
        cases.append((base_c[:-1], base_m))
        cases.append((base_c, base_m[:-1]))
        c = copy.deepcopy(base_c); c[0], c[1] = c[1], c[0]; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[0]["left_set"] = "nearest180"; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[0]["right_method"] = "K"; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[0]["origin_count"] = "6624"; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[0]["mean_pinball_difference"] = "NaN"; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[6]["mean_pinball_difference"] = "inf"; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[0]["extra"] = "1"; cases.append((c, base_m))
        c = copy.deepcopy(base_c); c[0]["horizon"] = "6.0"; cases.append((c, base_m))
        m = copy.deepcopy(base_m); m[0]["month"] = "2016-02"; cases.append((base_c, m))
        m = copy.deepcopy(base_m); m[0]["origin_count"] = "503"; cases.append((base_c, m))
        m = copy.deepcopy(base_m); m[0]["status"] = "SUPPRESSED"; cases.append((base_c, m))
        m = copy.deepcopy(base_m); m[0]["undefined_reason"] = "x"; cases.append((base_c, m))
        m = copy.deepcopy(base_m); m[0]["mean_pinball_recent360_K"] = "-inf"; cases.append((base_c, m))
        m = copy.deepcopy(base_m); del m[0]["mean_pinball_difference"]; cases.append((base_c, m))
        for i, (comparison, monthly) in enumerate(cases):
            with self.subTest(case=i), self.assertRaises(ValueError):
                module.display_data(comparison, monthly)

    def test_exact_accepted_public_hashes_bytes_and_counts_are_verified(self):
        # Independent public identity literals catch accepting a re-export or edited manifest.
        module = self.builder()
        data, identity = module.load_verified_results(PUBLIC)
        self.assertEqual(len(data.contrasts), 12)
        self.assertEqual(identity["manifest_sha256"], "396cbdc35288cc4a60ac371b3f0561ffc76bee4b50cda910a29be9e8dc89eb9b")
        expected = {
            "comparisons.csv": (1580, 22, "2d2df9c730b41b24dad9ed1047dcc983326cb4c8413ab0677d249c4b99986393"),
            "monthly.csv": (2229, 26, "14665edd9e0b584f3f88bb054ead5cc2e39c017547d4e0c99f3114ea25f11eb9"),
        }
        for name, (size, rows, digest) in expected.items():
            self.assertEqual(identity["inputs"][name], {"bytes": size, "rows": rows, "sha256": digest})

    def test_hash_drift_and_source_symlinks_are_rejected_before_display(self):
        module = self.builder()
        with tempfile.TemporaryDirectory(prefix="revision-figure-test-", dir=ROOT / ".scratch") as raw:
            source = Path(raw)
            for target in ("manifest.json", "comparisons.csv", "monthly.csv"):
                for path in source.iterdir():
                    path.unlink()
                for name in ("manifest.json", "comparisons.csv", "monthly.csv"):
                    (source / name).write_bytes((PUBLIC / name).read_bytes())
                with (source / target).open("ab") as stream:
                    stream.write(b" ")
                with self.subTest(target=target), self.assertRaises(ValueError):
                    module.load_verified_results(source)
            (source / "manifest.json").write_bytes((PUBLIC / "manifest.json").read_bytes())
            (source / "monthly.csv").unlink()
            (source / "monthly.csv").symlink_to(PUBLIC / "monthly.csv")
            with self.assertRaises(ValueError):
                module.load_verified_results(source)


class RevisionFigureArtifactTests(unittest.TestCase):
    def feature(self):
        self.assertIsNotNone(figures, "aggregate-only figure builder is missing")
        self.assertTrue(callable(getattr(figures, "build_figures", None)),
                        "exclusive vector PDF build entry point is missing")
        return figures

    def new_output(self):
        import uuid
        import shutil
        path = ROOT / ".scratch" / ("revision-figure-test-" + uuid.uuid4().hex)
        self.addCleanup(lambda: shutil.rmtree(path) if path.exists() and not path.is_symlink() else None)
        return path

    def test_two_exclusive_deterministic_vector_pages_have_every_display_label(self):
        # Catches wrong filenames, pagination, raster fallback, missing labels or nondeterminism.
        from pypdf import PdfReader
        module = self.feature()
        first, second = self.new_output(), self.new_output()
        report = module.build_figures(first)
        module.build_figures(second)
        self.assertEqual(set(p.name for p in first.iterdir()),
                         {"revision-retrieval-contrasts.pdf", "revision-retrieval-monthly.pdf", "artifact-identity.json"})
        data, _ = module.load_verified_results(PUBLIC)
        for name in ("revision-retrieval-contrasts.pdf", "revision-retrieval-monthly.pdf"):
            raw = (first / name).read_bytes()
            self.assertEqual(raw, (second / name).read_bytes())
            artifact = report["artifacts"][name]
            self.assertEqual(artifact["bytes"], len(raw))
            self.assertEqual(artifact["sha256"], hashlib.sha256(raw).hexdigest())
            reader = PdfReader(first / name)
            self.assertEqual(len(reader.pages), 1)
            page = reader.pages[0]
            self.assertAlmostEqual(float(page.mediabox.width), 841.8898, places=3)
            self.assertAlmostEqual(float(page.mediabox.height), 595.2756, places=3)
            for obj in page["/Resources"].get("/XObject", {}).values():
                self.assertNotEqual(obj.get_object().get("/Subtype"), "/Image")
            text = page.extract_text()
            self.assertIn("negative favors nearest", text)
            self.assertIn("Exploratory", text)
            points = data.contrasts if "contrasts" in name else data.monthly
            for point in points:
                self.assertIn(f"{point.value_millions:+.6f}", text)
            if "monthly" in name:
                for month in ("2016-01", "2016-12", "2017-01"):
                    self.assertIn(month, text)
                self.assertIn("+0.003379", text)
                self.assertIn("+0.520447", text)
                for count in ("504", "552", "502", "530", "528", "526", "506", "363"):
                    self.assertIn(count, text)
            else:
                self.assertIn("PRIMARY", text)
        saved = json.loads((first / "artifact-identity.json").read_text())
        self.assertEqual(saved, report)
        self.assertLess(report["resources"]["peak_rss_bytes"], 2 * 1024 ** 3)
        self.assertLess(report["resources"]["elapsed_seconds"], 600)
        self.assertLessEqual(report["resources"]["maximum_observed_os_threads"], 2)

    def test_layout_places_all_markers_and_labels_inside_page_and_retains_sign(self):
        # Catches clipped markers, inconsistent axes, or omission from rendered geometry.
        module = self.feature()
        data, _ = module.load_verified_results(PUBLIC)
        layouts = module.figure_layouts(data)
        self.assertEqual([len(layout["points"]) for layout in layouts], [12, 26])
        for layout in layouts:
            for point in layout["points"]:
                left, bottom, right, top = point["plot_bounds"]
                self.assertTrue(left + point["radius"] < point["x"] < right - point["radius"])
                self.assertTrue(bottom + point["radius"] < point["y"] < top - point["radius"])
                self.assertEqual(point["x"] < point["zero_x"], point["value_millions"] < 0)
                self.assertEqual(point["x"] > point["zero_x"], point["value_millions"] > 0)
                self.assertTrue(0 < point["label_x"] < 842)
                self.assertTrue(0 < point["label_y"] < 596)
            self.assertEqual(len({tuple(p["axis_limits"]) for p in layout["points"]}), 1)
        january = [p for p in layouts[1]["points"] if p["month"] == "2016-01"]
        self.assertEqual(len(january), 2)
        self.assertTrue(all(p["x"] > p["zero_x"] for p in january))

    def test_all_zero_and_all_positive_synthetic_layouts_remain_unclipped(self):
        # Catches all-zero division, positive-axis exclusion and x clipping in actual layouts.
        module = self.feature()
        data, _ = module.load_verified_results(PUBLIC)
        from dataclasses import replace
        for values in ((0.0, 0.0), (2.0, 3.0), (-2.0, 3.0)):
            synthetic = replace(data,
                                contrasts=tuple(replace(p, value_millions=values[i % 2])
                                                for i, p in enumerate(data.contrasts)),
                                monthly=tuple(replace(p, value_millions=values[i % 2])
                                              for i, p in enumerate(data.monthly)))
            for layout in module.figure_layouts(synthetic):
                for point in layout["points"]:
                    self.assertTrue(point["plot_bounds"][0] + 4 < point["x"] < point["plot_bounds"][2] - 4)
                    self.assertEqual(point["x"] < point["zero_x"], point["value_millions"] < 0)
                    self.assertEqual(point["x"] > point["zero_x"], point["value_millions"] > 0)

    def test_existing_nested_outside_and_symlink_outputs_are_rejected_without_writes(self):
        # Catches destructive overwrite, path traversal or a symlink escaping task scope.
        module = self.feature()
        existing = self.new_output()
        existing.mkdir()
        (existing / "sentinel").write_text("keep")
        bad = [existing, existing / "revision-figure-nested", ROOT / "revision-figure-outside",
               ROOT / ".scratch" / "other-prefix", existing / ".." / "revision-figure-traversal"]
        link = self.new_output()
        link.symlink_to(existing, target_is_directory=True)
        self.addCleanup(link.unlink)
        bad.append(link)
        for path in bad:
            with self.subTest(path=str(path)), self.assertRaises((ValueError, FileExistsError)):
                module.build_figures(path)
        self.assertEqual((existing / "sentinel").read_text(), "keep")
        self.assertEqual(sorted(p.name for p in existing.iterdir()), ["sentinel"])
        self.assertFalse((ROOT / "revision-figure-outside").exists())
        self.assertFalse((ROOT / ".scratch" / "other-prefix").exists())

    def test_cli_creates_only_pinned_public_figures_in_new_task_directory(self):
        # Catches a broken documented CLI; the real process needs no source-data access.
        import os
        import subprocess
        module = self.feature()
        output = self.new_output()
        env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                   VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
        result = subprocess.run([PYTHON, "-B", str(ROOT / "build_revision_figures.py"),
                                 "--output", str(output)], cwd=ROOT, env=env,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)
        self.assertEqual(message["output_directory"], str(output))
        self.assertEqual(message["pdf_count"], 2)
        self.assertEqual(len(list(output.glob("*.pdf"))), 2)


if __name__ == "__main__":
    unittest.main()
