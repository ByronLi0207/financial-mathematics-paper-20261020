"""Pure aggregate/geometry checks; this test file never renders PDF artifacts."""

from __future__ import annotations

import copy
import csv
from dataclasses import replace
import importlib
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "results" / "revision-20261022"
try:
    figures = importlib.import_module("build_conditional_figures")
except ModuleNotFoundError as exc:
    if exc.name != "build_conditional_figures":
        raise
    figures = None


def aggregate_rows():
    result = []
    for name in ("evaluation-summary.csv", "paired-comparisons.csv", "paired-annual.csv"):
        with (PUBLIC / name).open(newline="", encoding="utf-8") as stream:
            result.append(list(csv.DictReader(stream)))
    return result


class ConditionalFigureDataTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(figures, "aggregate-only conditional figure builder is missing")
        return figures

    def test_known_ratio_and_rate_arithmetic_keep_distinct_denominators(self):
        # Catches percent sign inversion, dividing by the left value, and mixing pp with percent.
        module = self.module()
        self.assertEqual(module.relative_change(80.0, 100.0), -20.0)
        self.assertEqual(module.relative_change(150.0, 100.0), 50.0)
        self.assertEqual(module.relative_change(0.0, 100.0), -100.0)
        self.assertIsNone(module.relative_change(0.0, 0.0))
        self.assertIsNone(module.relative_change(2.0, 0.0))
        self.assertEqual(module.relative_change(1e308, 1e308), 0.0)
        self.assertEqual(module.relative_change(0.0, 1e308), -100.0)
        self.assertEqual(module.breach_rate_change(5, 2, 10), 30.0)
        self.assertEqual(module.breach_rate_change(0, 5, 10), -50.0)
        for left, right in ((float("nan"), 1), (1, float("inf")), (-1, 2), (1e308, 1e-308)):
            with self.subTest(left=left, right=right), self.assertRaises(ValueError):
                module.relative_change(left, right)
        for values in ((2, 1, 0), (11, 1, 10), (-1, 1, 10), (2.0, 1, 10)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                module.breach_rate_change(*values)

    def test_full_inventory_keeps_adverse_rows_and_full_pool_equalities(self):
        # Catches cherry-picking favorable configurations or disguising the two k=W degeneracies.
        module = self.module()
        data, identity = module.load_verified_results(PUBLIC)
        self.assertEqual(len(data.common_history), 24)
        self.assertEqual(len(data.tradeoffs), 3)
        self.assertEqual(len(data.annual), 10)
        self.assertEqual([p.contrast_id for p in data.tradeoffs], [
            "fx_hourly-h6-QR2880-minus-rolling_F720",
            "fx_hourly-h24-QR2880-minus-rolling_S720",
            "nyfed_weekly-h6-QR260-minus-frozen_F260",
        ])
        self.assertEqual([sum(p.source == source for p in data.common_history)
                          for source in ("fx_hourly", "nyfed_weekly")], [12, 12])
        full = [p for p in data.common_history if p.full_pool]
        self.assertEqual([(p.source, p.horizon, p.window, p.method, p.loss_percent) for p in full], [
            ("nyfed_weekly", 6, 52, "KNN", 0.0),
            ("nyfed_weekly", 24, 52, "KNN", 0.0),
        ])
        self.assertAlmostEqual(data.tradeoffs[0].loss_percent, -12.660126412969763, places=10)
        self.assertAlmostEqual(data.tradeoffs[1].loss_percent, -1.8290714567022697, places=10)
        self.assertAlmostEqual(data.tradeoffs[2].loss_percent, 50.78571256749063, places=10)
        self.assertAlmostEqual(data.tradeoffs[0].breach_pp, 0.6641509433962264, places=10)
        self.assertAlmostEqual(data.tradeoffs[1].breach_pp, 3.683018867924528, places=10)
        self.assertAlmostEqual(data.tradeoffs[2].breach_pp, 9.386281588447653, places=10)
        self.assertTrue(data.tradeoffs[1].overrun_percent > 100)
        self.assertTrue(data.tradeoffs[2].overrun_percent > 100)
        self.assertTrue(all(p.unused_percent < 0 for p in data.tradeoffs))
        self.assertEqual([(p.year, p.origin_count) for p in data.annual if p.partial],
                         [(2017, 363), (2017, 363), (2026, 16)])
        ny_annual = [p for p in data.annual if p.source == "nyfed_weekly"]
        self.assertEqual([p.origin_count for p in ny_annual], [52, 52, 52, 52, 53, 16])
        self.assertTrue(all(p.loss_percent > 0 for p in ny_annual[:-1]))
        self.assertEqual(set(identity["inputs"]),
                         {"evaluation-summary.csv", "paired-comparisons.csv", "paired-annual.csv"})

    def test_missing_duplicate_or_mislabeled_rows_cannot_silently_change_the_menu(self):
        # Catches index-by-dict overwrite, wrong units, omitted negative results and wrong identity joins.
        module = self.module()
        original = aggregate_rows()
        mutations = []
        for file_index in range(3):
            missing = copy.deepcopy(original)
            missing[file_index].pop()
            mutations.append((f"missing-{file_index}", missing))
            duplicated = copy.deepcopy(original)
            duplicated[file_index][-1] = dict(duplicated[file_index][0])
            mutations.append((f"duplicated-{file_index}", duplicated))
        wrong_unit = copy.deepcopy(original)
        wrong_unit[0][0]["native_unit"] = "USD millions"
        mutations.append(("wrong-source-unit", wrong_unit))
        wrong_method = copy.deepcopy(original)
        wrong_method[1][0]["left_method"] = "KNN"
        mutations.append(("mislabeled-contrast", wrong_method))
        wrong_year = copy.deepcopy(original)
        wrong_year[2][0]["calendar_year"] = "2020"
        mutations.append(("mislabeled-year", wrong_year))
        wrong_flag = copy.deepcopy(original)
        wrong_flag[1][0]["declared_source_primary"] = "True"
        mutations.append(("mislabeled-primary", wrong_flag))
        wrong_fallback = copy.deepcopy(original)
        target = next(r for r in wrong_fallback[0] if r["plain_knn_full_pool_fallback"] == "True")
        target["plain_knn_full_pool_fallback"] = "False"
        mutations.append(("removed-fullpool-label", wrong_fallback))
        for label, changed in mutations:
            with self.subTest(label=label), self.assertRaises(ValueError):
                module.display_data(*changed)

    def test_numeric_inconsistency_cannot_pass_pure_input_validation(self):
        # Catches independent loss/overrun identities and a misleading percent or annual N.
        module = self.module()
        for file_index, key, new in (
            (0, "strict_breach_rate", "0.0"),
            (0, "mean_pinball", "1.0"),
            (1, "relative_mean_loss_difference_percent", "123.0"),
            (1, "mean_positive_overrun_difference", "nan"),
            (2, "origin_count", "52"),
            (2, "mean_pinball_difference", "0.0"),
        ):
            changed = aggregate_rows()
            changed[file_index][0][key] = new
            with self.subTest(file_index=file_index, key=key), self.assertRaises(ValueError):
                module.display_data(*changed)

    def test_accepted_audit_and_csv_bytes_are_pinned_before_any_display(self):
        # Catches hash drift, trusting a modified audit, and symlink-based source substitution.
        module = self.module()
        names = ("evaluation-audit-02.json", "evaluation-summary.csv",
                 "paired-comparisons.csv", "paired-annual.csv")
        with tempfile.TemporaryDirectory(prefix="conditional-figure-test-", dir=ROOT / ".scratch") as raw:
            directory = Path(raw)
            for target in names:
                for path in directory.iterdir():
                    path.unlink()
                for name in names:
                    (directory / name).write_bytes((PUBLIC / name).read_bytes())
                with (directory / target).open("ab") as stream:
                    stream.write(b" ")
                with self.subTest(target=target), self.assertRaises(ValueError):
                    module.load_verified_results(directory)
            for target in names:
                for path in directory.iterdir():
                    path.unlink()
                for name in names:
                    (directory / name).write_bytes((PUBLIC / name).read_bytes())
                # A same-length numeric byte change defeats a byte-count-only gate.
                original = (directory / target).read_bytes()
                index = original.rfind(b"0")
                self.assertGreaterEqual(index, 0)
                mutated = original[:index] + b"1" + original[index + 1:]
                self.assertEqual(len(mutated), len(original))
                (directory / target).write_bytes(mutated)
                with self.subTest(same_length_target=target), self.assertRaises(ValueError):
                    module.load_verified_results(directory)
            for path in directory.iterdir():
                path.unlink()
            for name in names:
                (directory / name).write_bytes((PUBLIC / name).read_bytes())
            (directory / "paired-annual.csv").unlink()
            (directory / "paired-annual.csv").symlink_to(PUBLIC / "paired-annual.csv")
            with self.assertRaises(ValueError):
                module.load_verified_results(directory)


class ConditionalFigureGeometryTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(figures, "aggregate-only conditional figure builder is missing")
        return figures

    def test_layout_contains_all_points_and_labels_inside_the_page_without_inference(self):
        # Catches clipped long captions, lost annual points, pooled units or a lost full-pool annotation.
        module = self.module()
        data, _ = module.load_verified_results(PUBLIC)
        layouts = module.figure_layouts(data)
        self.assertEqual([len(layout["points"]) for layout in layouts], [24, 12, 10])
        self.assertEqual([layout["public_path"] for layout in layouts], [
            "figures/conditional-common-history.pdf",
            "figures/conditional-primary-tradeoffs.pdf",
            "figures/conditional-annual-primary.pdf",
        ])
        for layout in layouts:
            module.validate_layout(layout)
            for point in layout["points"]:
                left, bottom, right, top = point["plot_bounds"]
                self.assertTrue(left + point["radius"] < point["x"] < right - point["radius"])
                self.assertTrue(bottom + point["radius"] < point["y"] < top - point["radius"])
                self.assertEqual(point["x"] < point["zero_x"], point["value"] < 0)
                self.assertEqual(point["x"] > point["zero_x"], point["value"] > 0)
            texts = " ".join(t["value"] for t in layout["texts"])
            self.assertIn("No confidence intervals", texts)
            self.assertIn("overlapping", texts)
        common_text = " ".join(t["value"] for t in layouts[0]["texts"])
        self.assertIn("full pool", common_text)
        self.assertIn("12 configurations", common_text)
        self.assertIn("USD millions", common_text)
        tradeoff_text = " ".join(t["value"] for t in layouts[1]["texts"])
        self.assertIn("percentage points", tradeoff_text)
        self.assertIn("Unused sign is descriptive", tradeoff_text)
        annual_text = " ".join(t["value"] for t in layouts[2]["texts"])
        self.assertIn("2017 partial", annual_text)
        self.assertIn("2026 partial", annual_text)
        self.assertIn("N=363", annual_text)
        self.assertIn("N=16", annual_text)

    def test_zero_only_positive_and_negative_layouts_have_nonzero_signed_scales(self):
        # Catches division by zero, excluding zero, and fixed-axis clipping when display data are all one sign.
        module = self.module()
        data, _ = module.load_verified_results(PUBLIC)
        for value in (0.0, 2.0, -2.0):
            synthetic = replace(data,
                common_history=tuple(replace(p, loss_percent=value) for p in data.common_history),
                tradeoffs=tuple(replace(p, loss_percent=value, breach_pp=value,
                                        overrun_percent=value, unused_percent=value) for p in data.tradeoffs),
                annual=tuple(replace(p, loss_percent=value) for p in data.annual))
            for layout in module.figure_layouts(synthetic):
                module.validate_layout(layout)
                for point in layout["points"]:
                    self.assertEqual(point["x"] < point["zero_x"], value < 0)
                    self.assertEqual(point["x"] > point["zero_x"], value > 0)

    def test_output_guard_rejects_existing_outside_and_symlink_paths_without_rendering(self):
        # Catches accidental overwrite or writing outside the task-owned staging area before Canvas is imported.
        module = self.module()
        with tempfile.TemporaryDirectory(prefix="conditional-figure-test-", dir=ROOT / ".scratch") as raw:
            directory = Path(raw)
            sentinel = directory / "keep"
            sentinel.write_text("keep")
            for bad in (directory, ROOT / "conditional-figure-outside",
                        directory / "conditional-figure-nested", ROOT / ".scratch" / "other-prefix"):
                with self.subTest(path=str(bad)), self.assertRaises((ValueError, FileExistsError)):
                    module.validate_output_directory(bad)
            self.assertEqual(sentinel.read_text(), "keep")
            link = directory / "conditional-figure-link"
            link.symlink_to(directory, target_is_directory=True)
            with self.assertRaises((ValueError, FileExistsError)):
                module.validate_output_directory(link)
            self.assertEqual(sorted(p.name for p in directory.iterdir()), ["conditional-figure-link", "keep"])


if __name__ == "__main__":
    unittest.main()
