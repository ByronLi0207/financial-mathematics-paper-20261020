"""Synthetic-only contracts for the exploratory composition runner."""
import csv
from fractions import Fraction
import io
import json
import math
import os
from pathlib import Path
import unittest

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"
import numpy as np

try:
    import run_revision_selection as runner
except ImportError:
    runner = None


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runner, "synthetic scoring/serialization implementation is missing")

    def test_literal_positive_negative_zero_errors_and_dollar_losses(self):
        scores = runner.score_arrays([10., 10., 10.], np.array([[8.]*3, [12.]*3, [10.]*3]), [2.]*3, [7, 8, 9])
        np.testing.assert_array_equal(scores.errors[:, 0], [2., -2., 0.])
        np.testing.assert_array_equal(scores.pinball[:, 0], [1.9, .1, 0.])
        metrics = runner.method_metrics(scores, 0)
        for key, expected in {"mean_pinball": 2/3, "mean_capacity": 10., "mean_extra_allowance": 8., "strict_breach_count": 1,
                              "strict_breach_rate": 1/3, "mean_positive_overrun": 2/3, "conditional_mean_overrun": 2.,
                              "conditional_overrun_denominator": 1, "mean_unused_allowance": 2/3}.items():
            self.assertEqual(metrics[key], expected, key)
        self.assertIsNone(metrics["conditional_overrun_undefined_reason"])

    def test_complement_is_converted_independently(self):
        scores = runner.score_arrays([0.], [[1., 1., 1.]], [0.], [0])
        self.assertEqual(scores.pinball[0, 0], .05)
        self.assertNotEqual(scores.pinball[0, 0], 1. - .95)

    def test_stored_peak_minus_capacity_controls_strict_breach(self):
        peak = float(2**53)
        caps = np.array([[np.nextafter(peak, 0.), peak, np.nextafter(peak, math.inf)]])
        scores = runner.score_arrays([peak], caps, [peak-4], [12])
        np.testing.assert_array_equal(scores.errors, [[1., 0., -2.]])
        np.testing.assert_array_equal(scores.strict_breach, [[True, False, False]])
        np.testing.assert_array_equal(scores.pinball, [[.95, 0., .1]])

    def test_zero_breach_is_null_with_reason_in_json_and_csv(self):
        scores = runner.score_arrays([2., 2.], [[2.]*3, [3.]*3], [2., 2.], [0, 1])
        metrics = runner.method_metrics(scores, 0)
        self.assertIsNone(metrics["conditional_mean_overrun"])
        self.assertEqual(metrics["conditional_overrun_denominator"], 0)
        self.assertEqual(metrics["conditional_overrun_undefined_reason"], "NO_STRICT_BREACHES")
        self.assertIsNone(json.loads(runner.public_json_bytes(metrics))["conditional_mean_overrun"])
        decoded = list(csv.DictReader(io.StringIO(runner.csv_bytes([metrics], tuple(metrics)).decode())))
        self.assertEqual(decoded[0]["conditional_mean_overrun"], "")
        self.assertEqual(decoded[0]["conditional_overrun_undefined_reason"], "NO_STRICT_BREACHES")

    def test_public_json_rejects_nonfinite_numpy_paths_accounts_and_unknown_objects(self):
        for value in [math.inf, math.nan, np.float64(1), np.array([1]), Path("/private/example"), "/Users/example", "person@example.org", {"account": "secret"}, {"path": "secret"}, object()]:
            with self.subTest(kind=type(value).__name__), self.assertRaises(ValueError):
                runner.public_json_bytes({"value": value})

    def test_malformed_nonfinite_shapes_origins_and_floor_are_rejected(self):
        cases = [([2.], [[2.]*3], [3.], [0]), ([math.nan], [[2.]*3], [0.], [0]),
                 ([2.], [[math.inf]*3], [0.], [0]), ([2.], [[2.]*2], [0.], [0]),
                 ([2., 2.], [[2.]*3]*2, [0., 0.], [1, 1]), ([2.], [[2.]*3], [0.], [True])]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                runner.score_arrays(*args)




def synthetic_reference():
    rows = []
    for cell_id, h in (("main", 6), ("h24", 24)):
        for method in ("F", "S", "L"):
            rows.append(dict(cell_id=cell_id, horizon=h, window=720, tau_numerator=19, tau_denominator=20,
                             rank=685, origin_count=6625, method_id=method, mean_pinball=0., mean_capacity=2.,
                             mean_extra_allowance=0., strict_breach_count=0, strict_breach_rate=0.,
                             mean_positive_overrun=0., conditional_mean_overrun=None,
                             conditional_overrun_denominator=0, mean_unused_allowance=0.,
                             conditional_overrun_undefined_reason="NO_STRICT_BREACHES"))
    return rows


class CompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = None
        if runner is not None and hasattr(runner, "compose"):
            cls.spec, cls.old_spec = runner.load_protocol()
            cls.position = np.full(18576, 2.)
            cls.origins = np.arange(11927, 18552)
            cls.times = np.datetime64("2016-01-01T00:00") + (np.arange(18576)-11927)*np.timedelta64(80, "m")
            cls.bundle = runner.compose(cls.position, cls.times, cls.origins, cls.spec)

    def setUp(self):
        self.assertIsNotNone(self.bundle, "full-menu composition implementation is missing")

    def test_constant_full_menu_has_literal_counts_and_method_metrics(self):
        self.assertEqual([len(self.bundle[name]) for name in ("summary", "geometry", "comparisons", "monthly")], [30, 10, 22, 26])
        self.assertEqual([(r["horizon"], r["set_id"], r["method_id"]) for r in self.bundle["summary"][:6]],
                         [(6, "full720", "F"), (6, "full720", "S"), (6, "full720", "K"),
                          (6, "recent360", "F"), (6, "recent360", "S"), (6, "recent360", "K")])
        for row in self.bundle["summary"]:
            self.assertEqual(row["origin_count"], 6625)
            self.assertEqual(row["mean_capacity"], 2.)
            self.assertEqual(row["mean_pinball"], 0.)
            self.assertEqual(row["strict_breach_count"], 0)
            self.assertIsNone(row["conditional_mean_overrun"])
            self.assertEqual(row["rank"], {720: 685, 360: 343, 180: 172}[row["selected_count"]])
        runner.validate_tables(self.bundle, self.spec)

    def test_selected_age_geometry_and_exact_equality_are_preserved(self):
        for row in self.bundle["geometry"]:
            self.assertEqual(row["equal_capacity_count"], 6625)
            self.assertEqual(row["mean_absolute_f_minus_s"], 0.)
            self.assertEqual(row["mean_absolute_anchor_radius"], 0.)
            self.assertEqual(row["mean_signed_anchor_radius"], 0.)
            m = {"full720": 720, "recent360": 360, "nearest360": 360, "recent180": 180, "nearest180": 180}[row["set_id"]]
            self.assertEqual(row["mean_selected_origin_age_records"], row["horizon"]+(m-1)/2)
        self.assertEqual(len(self.bundle["private"]["selection_digests"]), 10)

    def test_paired_comparisons_keep_all_fixed_directions(self):
        rows = self.bundle["comparisons"]
        self.assertEqual(sum(r["contrast_id"] == "nearest_minus_recent" for r in rows), 12)
        self.assertEqual(sum(r["contrast_id"] == "F_minus_S" for r in rows), 10)
        self.assertTrue(all(r["mean_pinball_difference"] == 0. for r in rows))
        self.assertTrue(all(r["origin_count"] == 6625 for r in rows))

    def test_original_global_reference_maps_only_K_to_L_and_rejects_change(self):
        runner.validate_original_reference(self.bundle["summary"], synthetic_reference())
        changed = synthetic_reference()
        changed[-1]["mean_pinball"] = 1.
        with self.assertRaises(ValueError):
            runner.validate_original_reference(self.bundle["summary"], changed)
        with self.assertRaises(ValueError):
            runner.validate_original_reference(self.bundle["summary"], synthetic_reference()[:-1])

    def test_public_tables_keep_nulls_and_exclude_private_predictions(self):
        outputs = runner.table_bytes(self.bundle, self.spec)
        self.assertEqual(set(outputs), {"summary.csv", "geometry.csv", "comparisons.csv", "monthly.csv"})
        rows = list(csv.DictReader(io.StringIO(outputs["summary.csv"].decode())))
        self.assertEqual(rows[0]["conditional_mean_overrun"], "")
        for name, value in outputs.items():
            self.assertNotIn(b"selection_digest", value, name)
            self.assertNotIn(b"capacities", value, name)

    def test_real_output_writer_and_guard_snapshot_accept_synthetic_bundle(self):
        import tempfile
        import time
        from run_study import RunGuard
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root/".scratch").mkdir()
            output = root/".scratch"/"synthetic"
            public, private = runner.new_attempt(output, root)
            started = runner.utc_now()
            guard = RunGuard(time.monotonic(), started, output, public, private)
            manifest = runner.initial_manifest(started, {name: runner.sha_file(runner.ROOT/name) for name in runner.CODE_FILES})
            manifest["source"].update(accepted_csv_bytes=1286391, accepted_csv_sha256="b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa", source_verified=True,
                                      acquisition_mode="local_reuse", request_performed_this_attempt=False, local_validation_utc=started, download=None)
            manifest["evaluation"] = dict(origin_count=6625, first_source_index=11927, last_source_index=18551)
            manifest["original_reference"]["summary_sha256"] = "0"*64  # Explicit synthetic reference fixture.
            manifest["artifacts"] = runner.write_tables(self.bundle, public, self.spec)
            guard(stage="final_manifest_checkpoint")
            manifest.update(run_status="COMPLETE", stop_code="NONE", resources=dict(guard.resources))
            manifest["checks"] = {name: "PASS" for name in runner.CHECK_NAMES}  # Synthetic validator fixture.
            runner.write_manifest(manifest, public)
            self.assertEqual(set(p.name for p in public.iterdir()), {"summary.csv", "geometry.csv", "comparisons.csv", "monthly.csv", "manifest.json"})
            for row in manifest["artifacts"]:
                content = (public/row["file_name"]).read_bytes()
                self.assertEqual(len(list(csv.DictReader(io.StringIO(content.decode())))), row["rows"])
                self.assertEqual(runner.sha_file(public/row["file_name"]), row["sha256"])
            self.assertGreater(manifest["resources"]["peak_rss_bytes"], 0)
            self.assertGreater(manifest["resources"]["thread_snapshot_count"], 0)
            with self.assertRaises(StudyStopForTest()):
                runner.write_tables(self.bundle, public, self.spec)

    def test_bad_row_identity_count_nonfinite_null_and_reason_are_rejected(self):
        import copy
        for mutate in (
            lambda b: b["summary"].pop(),
            lambda b: b["summary"][0].update(method_id="L"),
            lambda b: b["summary"][0].update(origin_count=6624),
            lambda b: b["summary"][0].update(mean_pinball=math.nan),
            lambda b: b["summary"][0].update(mean_pinball=None),
            lambda b: b["summary"][0].update(conditional_mean_overrun=0.),
            lambda b: b["summary"][0].update(conditional_overrun_undefined_reason=None),
            lambda b: b["comparisons"][0].update(left_set="recent360"),
            lambda b: b["monthly"][0].update(month="2015-12")):
            bundle = copy.deepcopy(self.bundle)
            mutate(bundle)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                runner.table_bytes(bundle, self.spec)

    def test_paired_monthly_reconciliation_uses_loss_scale_after_cancellation(self):
        import copy
        bundle = copy.deepcopy(self.bundle)
        # Two huge compensated means can round equally while the paired mean is 1.
        row = bundle["monthly"][0]
        row.update(mean_pinball_nearest360_K=float(2**53), mean_pinball_recent360_K=float(2**53), mean_pinball_difference=1.)
        runner.validate_tables(bundle, self.spec)

    def test_origin_continuity_full_eligibility_and_nonfinite_source_are_rejected(self):
        for origins in [self.origins[1:], np.r_[self.origins[:-1], 18552], np.r_[0, self.origins[1:]]]:
            with self.subTest(origin_count=len(origins)), self.assertRaises(ValueError):
                runner.compose(self.position, self.times, origins, self.spec)
        position = self.position.copy()
        position[1] = math.inf
        with self.assertRaises(ValueError):
            runner.compose(position, self.times, self.origins, self.spec)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(runner is not None and hasattr(runner, "monthly_rows"), "runner boundary implementation is missing")

    def test_months_include_empty_and_suppress_every_metric_below_30(self):
        times = np.array(["2016-01-01", "2016-01-02"] + ["2016-02-01"]*30, dtype="datetime64[D]")
        rows = runner.monthly_rows(times, np.full(32, 3.), np.full(32, 1.), 6)
        self.assertEqual(len(rows), 13)
        self.assertEqual([r["month"] for r in rows], [f"2016-{m:02d}" for m in range(1, 13)]+["2017-01"])
        self.assertEqual(rows[0]["origin_count"], 2)
        self.assertEqual(rows[0]["status"], "SUPPRESSED")
        self.assertEqual(rows[0]["undefined_reason"], "GROUP_BELOW_DISPLAY_MIN")
        self.assertTrue(all(rows[0][k] is None for k in ("mean_pinball_nearest360_K", "mean_pinball_recent360_K", "mean_pinball_difference")))
        self.assertEqual(rows[1]["origin_count"], 30)
        self.assertEqual(rows[1]["status"], "DISPLAYED")
        self.assertEqual(rows[1]["mean_pinball_difference"], 2.)
        self.assertEqual(rows[-1]["origin_count"], 0)
        self.assertEqual(rows[-1]["undefined_reason"], "NO_ORIGINS")

    def test_monthly_signed_paired_means_retain_favorable_and_adverse_values(self):
        times = np.full(30, np.datetime64("2016-01-01"))
        for left, right, expected in ((3., 1., 2.), (1., 3., -2.), (2., 2., 0.)):
            rows = runner.monthly_rows(times, np.full(30, left), np.full(30, right), 24)
            self.assertEqual(rows[0]["mean_pinball_difference"], expected)
            decoded = list(csv.DictReader(io.StringIO(runner.csv_bytes(rows, runner.MONTHLY_COLUMNS).decode())))
            self.assertEqual(float(decoded[0]["mean_pinball_difference"]), expected)

    def test_pinned_protocol_and_publication_receipt_are_verified_without_source(self):
        spec, old = runner.load_protocol()
        self.assertEqual(spec["expected_origin_count"], 6625)
        self.assertEqual(old["source"]["expected_csv_sha256"], "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa")
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(StudyStopForTest()):
                runner.load_protocol(Path(folder))

    def test_source_identity_rejects_missing_false_and_mismatched_evidence(self):
        good = dict(accepted_csv_bytes=1286391, accepted_csv_sha256="b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
                    source_verified=True, acquisition_mode="local_reuse", request_performed_this_attempt=False,
                    local_validation_utc="2026-10-21T00:00:00Z", download=None)
        runner.validate_source_identity(good)
        for update in ({"accepted_csv_bytes": 1}, {"source_verified": False}, {"request_performed_this_attempt": True},
                       {"download": {}}, {"local_validation_utc": None}, {"accepted_csv_sha256": "0"*64}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                runner.validate_source_identity(dict(good, **update))

    def test_measured_resources_reject_unknown_or_fabricated_zero_snapshots(self):
        good = dict(elapsed_seconds=.5, peak_rss_bytes=1000000, maximum_observed_os_threads=1,
                    thread_probe_status="PASS", thread_snapshot_count=2, checkpoint_utc="2026-10-21T00:00:00Z")
        runner.validate_measured_resources(good)
        for update in ({"peak_rss_bytes": None}, {"peak_rss_bytes": 0}, {"maximum_observed_os_threads": 0},
                       {"thread_snapshot_count": 0}, {"elapsed_seconds": None}, {"maximum_observed_os_threads": 3},
                       {"elapsed_seconds": 540.}, {"peak_rss_bytes": 1610612736}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                runner.validate_measured_resources(dict(good, **update))


def StudyStopForTest():
    from run_study import StudyStop
    return StudyStop


class ExecutionBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(runner is not None and hasattr(runner, "new_attempt"), "bounded CLI implementation is missing")

    def test_new_attempt_requires_new_nonsymlink_scratch_descendant(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            scratch = root/".scratch"
            scratch.mkdir()
            public, private = runner.new_attempt(scratch/"fresh", root)
            self.assertTrue(public.is_dir())
            self.assertTrue(private.is_dir())
            for path in (scratch/"fresh", root/"outside", scratch):
                with self.subTest(path=path), self.assertRaises(StudyStopForTest()):
                    runner.new_attempt(path, root)
            (scratch/"link").symlink_to(root, target_is_directory=True)
            with self.assertRaises(StudyStopForTest()):
                runner.new_attempt(scratch/"link"/"escape", root)

    def test_exclusive_write_rejects_symlinks_and_never_overwrites(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder).resolve()/"artifact.csv"
            runner.exclusive_write(target, b"first")
            with self.assertRaises((ValueError, OSError, StudyStopForTest())):
                runner.exclusive_write(target, b"second")
            self.assertEqual(target.read_bytes(), b"first")
            link = Path(folder).resolve()/"link.csv"
            link.symlink_to(target)
            with self.assertRaises((ValueError, OSError, StudyStopForTest())):
                runner.exclusive_write(link, b"third")
            self.assertEqual(target.read_bytes(), b"first")

    def test_failure_manifest_preserves_unmeasured_nulls_and_safe_code(self):
        from run_study import RunGuard
        manifest = runner.initial_manifest("2026-10-21T00:00:00Z", {})
        guard = RunGuard(0., "2026-10-21T00:00:00Z", Path("unused"), Path("unused"), Path("unused"))
        runner.mark_failure(manifest, guard, StudyStopForTest()("SOURCE_IDENTITY_OR_SCHEMA"))
        self.assertEqual(manifest["run_status"], "INCOMPLETE")
        self.assertEqual(manifest["stop_code"], "SOURCE_IDENTITY_OR_SCHEMA")
        self.assertIsNone(manifest["resources"]["elapsed_seconds"])
        self.assertIsNone(manifest["resources"]["peak_rss_bytes"])
        self.assertIsNone(manifest["resources"]["maximum_observed_os_threads"])
        runner.validate_manifest(manifest)
        runner.mark_failure(manifest, guard, RuntimeError("/Users/private/account@example.org"))
        value = runner.public_json_bytes(manifest)
        self.assertNotIn(b"/Users/private", value)
        self.assertNotIn(b"example.org", value)
        self.assertEqual(manifest["stop_code"], "INTERNAL")

    def test_manifest_rejects_unknown_nested_account_metadata(self):
        import copy
        manifest = runner.initial_manifest("2026-10-21T00:00:00Z", {})
        for area in ("source", "evaluation", "environment", "resources", "undefined_conventions"):
            bad = copy.deepcopy(manifest)
            bad[area]["unapproved_owner"] = "PrivateOwner123"
            with self.subTest(area=area), self.assertRaises(ValueError):
                runner.validate_manifest(bad)

    def test_source_error_keeps_safe_source_code_without_its_reason(self):
        from study_data import SourceError
        from run_study import RunGuard
        manifest = runner.initial_manifest("2026-10-21T00:00:00Z", {})
        guard = RunGuard(0., "2026-10-21T00:00:00Z", Path("unused"), Path("unused"), Path("unused"))
        runner.mark_failure(manifest, guard, SourceError("SOURCE_IDENTITY_OR_SCHEMA", "/Users/private/secret"))
        self.assertEqual(manifest["stop_code"], "SOURCE_IDENTITY_OR_SCHEMA")
        self.assertNotIn(b"secret", runner.public_json_bytes(manifest))

    def test_guard_failure_happens_before_source_access_and_is_retained(self):
        import contextlib
        import tempfile
        from unittest.mock import patch
        actual_root = runner.ROOT
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root/".scratch").mkdir()
            # Leave the real source path unreachable: the failed first guard
            # must terminate before importing/calling any source loader.
            with patch.object(runner, "ROOT", root), patch.object(runner, "load_protocol", return_value=runner.load_protocol(actual_root)), patch.object(runner, "sha_file", return_value="0"*64), patch.object(runner.RunGuard, "__call__", side_effect=StudyStopForTest()("RESOURCE_UNVERIFIED")), contextlib.redirect_stdout(io.StringIO()):
                code = runner.main(["--output", str(root/".scratch"/"guard-failed")])
            manifest = json.loads((root/".scratch"/"guard-failed"/"public"/"manifest.json").read_text())
            self.assertEqual(code, 1)
            self.assertEqual(manifest["stop_code"], "RESOURCE_UNVERIFIED")
            self.assertFalse(manifest["source"]["source_verified"])
            self.assertIsNone(manifest["resources"]["maximum_observed_os_threads"])

    def test_complete_manifest_cannot_accept_unrun_checks_or_fake_resources(self):
        manifest = runner.initial_manifest("2026-10-21T00:00:00Z", {})
        manifest["run_status"] = "COMPLETE"
        with self.assertRaises(ValueError):
            runner.validate_manifest(manifest)

    def test_help_is_source_independent_and_rejects_other_entry_options(self):
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()) as out:
            with self.assertRaises(SystemExit) as exit_code:
                runner.main(["--help"])
        self.assertEqual(exit_code.exception.code, 0)
        self.assertIn("--output", out.getvalue())
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as bad:
                runner.main(["--fetch"])
        self.assertEqual(bad.exception.code, 2)

    def test_cli_start_clock_includes_pre_numpy_import_time(self):
        import contextlib
        import tempfile
        import time
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root/".scratch").mkdir()
            output = root/".scratch"/"clock-failed"
            # No source or calculation runs: missing pinned protocol stops first.
            with patch.object(runner, "ROOT", root), patch.object(runner, "PROCESS_STARTED_UTC", "2000-01-01T00:00:00Z", create=True), patch.object(runner, "PROCESS_STARTED_MONOTONIC", time.monotonic()-1., create=True), patch("sys.argv", ["run_revision_selection.py", "--output", str(output)]), contextlib.redirect_stdout(io.StringIO()):
                code = runner.main()
            self.assertEqual(code, 1)
            manifest = json.loads((output/"public"/"manifest.json").read_text())
            self.assertEqual(manifest["started_utc"], "2000-01-01T00:00:00Z")
            self.assertEqual(manifest["resources"]["started_utc"], "2000-01-01T00:00:00Z")

    def test_protocol_failure_retains_sanitized_incomplete_attempt(self):
        import contextlib
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root/".scratch").mkdir()
            with patch.object(runner, "ROOT", root), contextlib.redirect_stdout(io.StringIO()) as out:
                code = runner.main(["--output", str(root/".scratch"/"failed")])
            self.assertEqual(code, 1)
            manifest = json.loads((root/".scratch"/"failed"/"public"/"manifest.json").read_text())
            self.assertEqual(manifest["run_status"], "INCOMPLETE")
            self.assertEqual(manifest["stop_code"], "SPECIFICATION")
            self.assertIsNone(manifest["resources"]["peak_rss_bytes"])
            self.assertNotIn(folder, out.getvalue())


if __name__ == "__main__":
    unittest.main()
