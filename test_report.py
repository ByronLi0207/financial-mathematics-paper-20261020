"""Wholly artificial public-boundary tests; never load source observations."""

import copy
import csv
import hashlib
import importlib
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "protocol/output-schema.json").read_text())
SPEC = json.loads((ROOT / "protocol/study-spec.json").read_text())
CELLS = ["main", "h12", "h24", "n480", "n1440", "tau90", "tau99"]
METHODS = ["F", "S", "R", "L", "P0"]
LENGTHS = [120, 240, 720, 1440]
METRICS = SCHEMA["tables"]["results/diagnostics.csv"]["method_metrics"]
PATHS = list(SCHEMA["tables"]) + SCHEMA["figures"]["exact_public_paths"]


def task_temporary_directory():
    """Keep test artifacts in task-owned scratch, avoiding system path aliases."""
    scratch = ROOT / ".scratch"
    scratch.mkdir(mode=0o700, exist_ok=True)
    return tempfile.TemporaryDirectory(prefix="report-test-", dir=scratch)


def artificial_rows():
    """60 invented origins, three months including an intentional empty month."""
    summary, paired, stability, diagnostics = [], [], [], []
    for cell in SPEC["cells"]:
        meta = {
            "cell_id": cell["cell_id"], "horizon": cell["horizon"],
            "window": cell["window"], "tau_numerator": cell["tau_numerator"],
            "tau_denominator": cell["tau_denominator"],
            "rank": cell["expected_rank"], "origin_count": 60,
        }
        for index, method in enumerate(METHODS):
            # Hand-specified public scalars, not computed forecasts or data.
            loss = [1e-12, 2e-12, 3e-12, 4e-12, 1.9e-11][index]
            row = dict(meta, method_id=method, mean_pinball=loss,
                       mean_capacity=[4e-11, 6e-11, 8e-11, 1e-10, 0.0][index],
                       mean_extra_allowance=[4e-11, 6e-11, 8e-11, 1e-10, 0.0][index],
                       strict_breach_count=60 if method == "P0" else 0,
                       strict_breach_rate=1.0 if method == "P0" else 0.0,
                       mean_positive_overrun=2e-11 if method == "P0" else 0.0,
                       conditional_mean_overrun=2e-11 if method == "P0" else None,
                       conditional_overrun_denominator=60 if method == "P0" else 0,
                       mean_unused_allowance=[2e-11, 4e-11, 6e-11, 8e-11, 0.0][index],
                       aux_breach_count=60 if method == "P0" else 0,
                       strict_aux_disagreement_count=0, near_event_boundary_count=0,
                       conditional_overrun_undefined_reason=None if method == "P0" else "NO_STRICT_BREACHES")
            summary.append(row)
        paired.append(dict(meta, mean_pinball_difference=-1e-12,
                           relative_difference_to_S=-0.5,
                           relative_difference_undefined_reason=None,
                           f_lower_count=60, equal_capacity_count=0, f_higher_count=0,
                           f_lower_fraction=1.0, equal_capacity_fraction=0.0,
                           f_higher_fraction=0.0, near_fs_capacity_count=0,
                           near_fs_capacity_fraction=0.0, paired_scores_equal_count=0,
                           scores_changed_allowances_equal_count=0,
                           allowances_changed_capacities_equal_count=0,
                           capacities_different_count=60))
    for ell in LENGTHS:
        stability.append(dict(paired[0] | {}, ell=ell))
        stability[-1] = {key: paired[0][key] for key in SCHEMA["csv"]["metadata_prefix"]}
        stability[-1].update(
            ell=ell, ell_over_origin_count=ell / 60, replicates=999,
            expected_used_blocks=1 + 59 / ell, observed_mean_d=-1e-12,
            resampled_mean_average=1e-12 if ell == 120 else 1.5e-12,
            resampled_mean_sd_ddof1=0.0 if ell == 120 else 0.5e-12,
            resampled_mean_order25=1e-12,
            resampled_mean_order975=1e-12 if ell == 120 else 2e-12,
            lower_rank=25, upper_rank=975, generator="PCG64", seed_base=20261020,
            seed_length=ell, constant_input=False, constant_shortcut_used=False)
    groups = [
        ("current_sign", "negative", 30), ("current_sign", "zero", 0),
        ("current_sign", "positive", 30),
        ("development_magnitude_tercile", "low", 30),
        ("development_magnitude_tercile", "middle", 0),
        ("development_magnitude_tercile", "high", 30),
        *[("source_index_modulo_6", str(i), 10) for i in range(6)],
        ("naive_origin_month", "2016-01", 30),
        ("naive_origin_month", "2016-02", 0),
        ("naive_origin_month", "2016-03", 30),
        ("retrospective_gap_free_path", "gap_free", 60),
        ("retrospective_gap_free_path", "has_gap", 0),
    ]
    for panel, group, count in groups:
        status = "DISPLAYED" if count >= 30 else "BELOW_DISPLAY_MIN" if count else "NO_ORIGINS"
        for method in METHODS + ["F_MINUS_S"]:
            for metric in METRICS if method != "F_MINUS_S" else ["mean_pinball_difference"]:
                if count < 30:
                    value = None
                    reason = "GROUP_BELOW_DISPLAY_MIN" if count else "NO_ORIGINS"
                elif method == "F_MINUS_S":
                    value, reason = -1e-12, None
                else:
                    method_row = summary[METHODS.index(method)]
                    value = method_row[metric]
                    if metric in {"strict_breach_count", "conditional_overrun_denominator", "aux_breach_count"}:
                        value = count if method == "P0" else 0
                    reason = "NO_STRICT_BREACHES" if metric == "conditional_mean_overrun" and method != "P0" else None
                diagnostics.append(dict(cell_id="main", panel=panel, group=group,
                                        method_or_comparison=method, metric=metric,
                                        origin_count=count, display_status=status,
                                        value=value, undefined_reason=reason))
    return summary, paired, stability, diagnostics


def artificial_manifest(complete=False, artifacts=None):
    """Safe metadata only; no accepted input facts are invented for INCOMPLETE."""
    source = SPEC["source"]
    accepted = source["expected_csv_bytes"] if complete else None
    accepted_hash = source["expected_csv_sha256"] if complete else None
    utc = "2026-10-21T06:00:00Z"
    manifest = {
        "manifest_schema_version": 1, "declared_scope": SPEC["scope"],
        "study_id": SPEC["study_id"], "attempt_id": "artificial-report-test",
        "run_status": "COMPLETE" if complete else "INCOMPLETE",
        "stop_code": "NONE" if complete else "RESOURCE_UNVERIFIED",
        "planned_cell_ids": CELLS.copy(), "completed_cell_ids": CELLS.copy() if complete else [],
        "method_ids": METHODS.copy(),
        "source": {
            "dataset": source["dataset"], "version": source["version"],
            "public_url": source["public_url"], "requested_member": source["requested_member"],
            "expected_csv_bytes": source["expected_csv_bytes"],
            "expected_csv_sha256": source["expected_csv_sha256"],
            "accepted_csv_bytes": accepted, "accepted_csv_sha256": accepted_hash,
            "source_verified": complete, "acquisition_mode": "local_reuse" if complete else None,
            "request_performed_this_attempt": False, "historical_access_utc": None,
            "local_validation_utc": utc if complete else None,
            "timestamp_timezone": "unspecified_naive",
            "observed_rights_label": source["observed_rights_label"],
            "raw_redistribution_verified": False, "download": None,
        },
        "specification": {
            "relative_path": "protocol/study-spec.json",
            "sha256": "0b8eda7bfd858c038bae22a96a7caa5ff21838317de58bc56eef98ca696c54ff",
            "schema_version": 1, "primary_cell_id": "main", "amends_sha256": None,
            "common_origin_reference_sha256": "a" * 64 if complete else None,
            "cells": [{key: cell[key] for key in SCHEMA["run_manifest"]["nested_fields"]["specification.cells[]"]} for cell in SPEC["cells"]],
            "evaluation_bounds": {"origin_count": 60 if complete else None,
                                  "first_source_index": 1500 if complete else None,
                                  "last_source_index": 1559 if complete else None},
        },
        "code": {"revision": None, "files": [{"relative_path": path, "sha256": "b" * 64} for path in SCHEMA["run_manifest"]["code_file_allowlist"]]},
        "environment": {
            "python_implementation": "CPython" if complete else None,
            "python_version": "3.12.14" if complete else None,
            "os_family": "Darwin" if complete else None,
            "os_version": "25.0.0" if complete else None,
            "architecture": "arm64" if complete else None,
            "numpy_version": "2.3.5" if complete else None,
            "reportlab_version": "4.4.9" if complete else None,
            "thread_requests": {key: "1" if complete else None for key in SCHEMA["run_manifest"]["nested_fields"]["environment.thread_requests"]},
        },
        "resources": {
            "started_utc": utc, "checkpoint_utc": utc,
            "measurement_point": "final_checkpoint_before_manifest",
            "requested_numerical_threads": 1,
            "elapsed_seconds": 1.0 if complete else None,
            "peak_rss_bytes": 10000000 if complete else None,
            "maximum_observed_os_threads": 1 if complete else None,
            "thread_probe_status": "PASS" if complete else "UNVERIFIED",
            "thread_snapshot_count": 2 if complete else None,
            "completed_stability_lengths": LENGTHS.copy() if complete else [],
            "current_stage": "final", "current_cell_id": None, "current_length": None,
            "completed_origins_current_cell": None, "completed_replicates_current_length": None,
            "new_output_bytes_at_checkpoint": 1000000 if complete else None,
            "private_numeric_output_bytes_at_checkpoint": 0 if complete else None,
            "public_analysis_output_bytes_at_checkpoint": 1000000 if complete else None,
        },
        "checks": {key: "PASS" if complete else "NOT_RUN" for key in SCHEMA["run_manifest"]["nested_fields"]["checks"]},
        "outputs": {"artifacts": artifacts if artifacts is not None else []},
        "undefined_conventions": {
            "csv_empty_is_null": True, "json_nonfinite_allowed": False,
            "zero_breach_reason": "NO_STRICT_BREACHES", "zero_s_loss_reason": "ZERO_MEAN_LOSS_S",
            "display_min_origins": 30, "below_display_reason": "GROUP_BELOW_DISPLAY_MIN",
            "empty_group_reason": "NO_ORIGINS",
        },
    }
    if complete and artifacts is None:
        manifest["outputs"]["artifacts"] = [
            dict(relative_path=path, kind="table" if path.endswith(".csv") else "figure",
                 bytes=100, sha256="c" * 64,
                 row_count={PATHS[0]: 35, PATHS[1]: 7, PATHS[2]: 4, PATHS[3]: 1037}.get(path))
            for path in PATHS
        ]
    return manifest


class ExplosiveString:
    def __str__(self):
        raise AssertionError("generic string conversion must never happen")


class ReportTests(unittest.TestCase):
    def setUp(self):
        try:
            self.report = importlib.import_module("study_report")
        except ModuleNotFoundError as exc:
            if exc.name == "study_report":
                self.fail("missing report behavior: study_report has not been implemented")
            raise

    def bundle(self):
        return self.report.AggregateBundle(*artificial_rows())

    def assert_invalid(self, mutate):
        bundle = self.bundle()
        mutate(bundle)
        with self.assertRaises((ValueError, TypeError)):
            self.report.validate_aggregate_bundle(bundle, SCHEMA)

    def test_complete_artificial_bundle_keeps_all_empty_sparse_and_no_breach_rows(self):
        bundle = self.bundle()
        self.report.validate_aggregate_bundle(bundle, SCHEMA)
        self.assertEqual([len(bundle.summary), len(bundle.paired), len(bundle.stability), len(bundle.diagnostics)], [35, 7, 4, 1037])
        empty = [row for row in bundle.diagnostics if row["group"] == "2016-02"]
        self.assertEqual(len(empty), 61)
        self.assertTrue(all(row["value"] is None and row["undefined_reason"] == "NO_ORIGINS" for row in empty))

    def test_scalar_boundary_rejects_arrays_numpy_scalars_and_objects_before_stringification(self):
        import numpy as np
        for value in [np.array([1.0]), np.float64(1.0), np.int64(1), ExplosiveString(), [1], {"x": 1}, float("nan"), float("inf"), True, None]:
            with self.subTest(kind=type(value).__name__):
                self.assert_invalid(lambda b: b.summary[0].__setitem__("mean_pinball", value))
        with self.assertRaises((ValueError, TypeError)):
            self.report.write_aggregate_outputs(ExplosiveString(), ROOT / ".scratch/never-written", SCHEMA)

    def test_rejects_unknown_missing_duplicate_out_of_order_and_wrong_count_rows(self):
        changes = [
            lambda b: b.summary[0].__setitem__("raw_source", 1),
            lambda b: b.summary[0].pop("rank"),
            lambda b: b.summary.__setitem__(1, copy.deepcopy(b.summary[0])),
            lambda b: b.summary.reverse(), lambda b: b.paired.pop(),
            lambda b: b.stability.reverse(), lambda b: b.diagnostics.pop(),
            lambda b: b.diagnostics.__setitem__(1, copy.deepcopy(b.diagnostics[0])),
            lambda b: b.diagnostics.reverse(),
        ]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                self.assert_invalid(change)

    def test_rejects_metadata_partitions_rates_and_status_inconsistencies(self):
        changes = [
            lambda b: b.summary[1].__setitem__("origin_count", 61),
            lambda b: b.paired[0].__setitem__("horizon", 12),
            lambda b: b.summary[0].__setitem__("rank", True),
            lambda b: b.paired[0].__setitem__("f_lower_count", 59),
            lambda b: b.paired[0].__setitem__("f_lower_fraction", 0.0),
            lambda b: b.paired[0].__setitem__("paired_scores_equal_count", 1),
            lambda b: b.summary[0].__setitem__("strict_breach_rate", 0.5),
            lambda b: b.summary[0].__setitem__("conditional_mean_overrun", 0.0),
            lambda b: b.summary[0].__setitem__("conditional_overrun_undefined_reason", None),
            lambda b: b.summary[4].__setitem__("conditional_mean_overrun", None),
            lambda b: b.summary[4].__setitem__("conditional_overrun_denominator", 0),
            lambda b: b.stability[0].__setitem__("observed_mean_d", 1.0),
            lambda b: b.stability[0].__setitem__("ell_over_origin_count", 0.0),
            lambda b: b.stability[0].__setitem__("replicates", 998),
            lambda b: b.stability[0].__setitem__("constant_input", True),
            lambda b: b.diagnostics[0].__setitem__("origin_count", 29),
            lambda b: b.diagnostics[61].__setitem__("value", 0.0),
            lambda b: b.diagnostics[0].__setitem__("display_status", "NO_ORIGINS"),
            lambda b: b.diagnostics[0].__setitem__("undefined_reason", "NO_ORIGINS"),
        ]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                self.assert_invalid(change)

    def test_zero_s_loss_requires_null_relative_difference_and_exact_reason(self):
        bundle = self.bundle()
        bundle.summary[1]["mean_pinball"] = 0.0
        bundle.paired[0]["mean_pinball_difference"] = 1e-12
        bundle.paired[0]["relative_difference_to_S"] = None
        bundle.paired[0]["relative_difference_undefined_reason"] = "ZERO_MEAN_LOSS_S"
        for row in bundle.stability:
            row["observed_mean_d"] = 1e-12
        for row in bundle.diagnostics:
            if row["display_status"] == "DISPLAYED" and row["method_or_comparison"] == "F_MINUS_S":
                row["value"] = 1e-12
            if row["display_status"] == "DISPLAYED" and row["method_or_comparison"] == "S" and row["metric"] == "mean_pinball":
                row["value"] = 0.0
        self.report.validate_aggregate_bundle(bundle, SCHEMA)
        bundle.paired[0]["relative_difference_to_S"] = 0.0
        with self.assertRaises(ValueError):
            self.report.validate_aggregate_bundle(bundle, SCHEMA)

    def test_actual_artifacts_headers_counts_boolean_null_hashes_and_vector_annotations(self):
        with task_temporary_directory() as tmp:
            destination = Path(tmp)
            artifacts = self.report.write_aggregate_outputs(self.bundle(), destination, SCHEMA)
            self.assertEqual([a["relative_path"] for a in artifacts], PATHS)
            self.assertEqual(len(artifacts), 7)
            for artifact in artifacts:
                self.assertEqual(set(artifact), {"relative_path", "kind", "bytes", "sha256", "row_count"})
                data = (destination / artifact["relative_path"]).read_bytes()
                self.assertEqual(artifact["bytes"], len(data))
                self.assertEqual(artifact["sha256"], hashlib.sha256(data).hexdigest())
                self.assertNotIn(b"\r\n", data if artifact["kind"] == "table" else b"")
                if artifact["kind"] == "table":
                    rows = list(csv.reader(data.decode("utf-8").splitlines()))
                    self.assertEqual(rows[0], SCHEMA["tables"][artifact["relative_path"]]["columns"])
                    self.assertEqual(len(rows) - 1, artifact["row_count"])
                else:
                    self.assertIsNone(artifact["row_count"])
                    self.assertTrue(data.startswith(b"%PDF-"))
                    self.assertNotIn(b"/Subtype /Image", data)
            stability_text = (destination / PATHS[2]).read_text()
            self.assertIn(",false,false\n", stability_text)
            with (destination / PATHS[0]).open(encoding="utf-8", newline="") as stream:
                summary = list(csv.DictReader(stream))
            self.assertEqual(summary[0]["conditional_mean_overrun"], "")
            self.assertEqual(summary[0]["conditional_overrun_undefined_reason"], "NO_STRICT_BREACHES")
            within = (destination / PATHS[4]).read_bytes()
            monthly = (destination / PATHS[5]).read_bytes()
            ranges = (destination / PATHS[6]).read_bytes()
            self.assertIn(b"-1e-18", within)
            self.assertIn(b"2016-02", monthly)
            self.assertIn(b"NO_ORIGINS", monthly)
            self.assertIn(b"n=0", monthly)
            self.assertIn(b"-1e-18", ranges)
            self.assertIn(b"1e-18", ranges)
            self.assertIn(b"2e-18", ranges)
            self.assertIn(b"zero width", ranges)
            self.assertIn(b"Observed", ranges)

    def test_writes_reject_overwrite_symlinks_traversal_and_invalid_input_before_files(self):
        with task_temporary_directory() as tmp:
            root = Path(tmp)
            unsafe = self.bundle()
            unsafe.summary[0]["unknown"] = "secret"
            with self.assertRaises((ValueError, TypeError)):
                self.report.write_aggregate_outputs(unsafe, root, SCHEMA)
            self.assertEqual(list(root.iterdir()), [])
            (root / "results").symlink_to(root, target_is_directory=True)
            with self.assertRaises((ValueError, OSError)):
                self.report.write_aggregate_outputs(self.bundle(), root, SCHEMA)
            (root / "results").unlink()
            self.report.write_aggregate_outputs(self.bundle(), root, SCHEMA)
            before = (root / PATHS[0]).read_bytes()
            with self.assertRaises((ValueError, FileExistsError)):
                self.report.write_aggregate_outputs(self.bundle(), root, SCHEMA)
            self.assertEqual((root / PATHS[0]).read_bytes(), before)
            with self.assertRaises((ValueError, OSError)):
                self.report.write_aggregate_outputs(self.bundle(), root / "missing" / "..", SCHEMA)

    def test_manifest_incomplete_preserves_null_observations_and_is_exclusive(self):
        with task_temporary_directory() as tmp:
            manifest = artificial_manifest()
            self.report.validate_run_manifest(manifest, SCHEMA)
            artifact = self.report.write_run_manifest(manifest, Path(tmp), SCHEMA)
            output = Path(tmp) / "results/run-manifest.json"
            data = output.read_bytes()
            saved = json.loads(data)
            self.assertIsNone(saved["source"]["accepted_csv_sha256"])
            self.assertIsNone(saved["resources"]["peak_rss_bytes"])
            self.assertEqual(saved["outputs"]["artifacts"], [])
            self.assertEqual(artifact["sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(artifact["bytes"], len(data))
            self.assertNotIn("sha256", saved)
            with self.assertRaises((FileExistsError, ValueError)):
                self.report.write_run_manifest(manifest, Path(tmp), SCHEMA)

    def test_complete_manifest_requires_actual_artifacts_counts_passes_and_observations(self):
        self.report.validate_run_manifest(artificial_manifest(True), SCHEMA)
        changes = [
            lambda m: m["checks"].__setitem__("resources", "UNVERIFIED"),
            lambda m: m["resources"].__setitem__("peak_rss_bytes", None),
            lambda m: m["resources"].__setitem__("maximum_observed_os_threads", 3),
            lambda m: m["resources"].__setitem__("elapsed_seconds", 600.0),
            lambda m: m["resources"]["completed_stability_lengths"].pop(),
            lambda m: m["completed_cell_ids"].pop(),
            lambda m: m["outputs"]["artifacts"][0].__setitem__("row_count", 34),
            lambda m: m["outputs"]["artifacts"].pop(),
            lambda m: m["source"].__setitem__("source_verified", False),
            lambda m: m["source"].__setitem__("accepted_csv_sha256", "d" * 64),
            lambda m: m["environment"].__setitem__("reportlab_version", None),
            lambda m: m["specification"]["evaluation_bounds"].__setitem__("origin_count", True),
            lambda m: m["resources"].__setitem__("thread_snapshot_count", 0),
        ]
        for change in changes:
            manifest = artificial_manifest(True)
            change(manifest)
            with self.subTest(change=changes.index(change)), self.assertRaises((ValueError, TypeError)):
                self.report.validate_run_manifest(manifest, SCHEMA)
        with task_temporary_directory() as tmp:
            with self.assertRaises((ValueError, OSError)):
                self.report.write_run_manifest(artificial_manifest(True), Path(tmp), SCHEMA)
            artifacts = self.report.write_aggregate_outputs(self.bundle(), Path(tmp), SCHEMA)
            self.report.write_run_manifest(artificial_manifest(True, artifacts), Path(tmp), SCHEMA)
            saved = json.loads((Path(tmp) / "results/run-manifest.json").read_text())
            self.assertEqual(saved["run_status"], "COMPLETE")
            self.assertEqual(len(saved["outputs"]["artifacts"]), 7)

    def test_manifest_rejects_unknown_nested_fields_private_values_and_nonbuiltin_scalars(self):
        changes = [
            lambda m: m.__setitem__("cwd", "/private/source"),
            lambda m: m["source"].__setitem__("basename", "local-secret.csv"),
            lambda m: m["source"].__setitem__("accepted_csv_sha256", "d" * 64),
            lambda m: m["source"].__setitem__("download", {"signed_url": "https://secret"}),
            lambda m: m["environment"].__setitem__("hostname", "private-machine"),
            lambda m: m["environment"]["thread_requests"].__setitem__("HOME", "private"),
            lambda m: m["code"]["files"][0].__setitem__("relative_path", "../study_data.py"),
            lambda m: m["resources"].__setitem__("elapsed_seconds", float("nan")),
            lambda m: m["resources"].__setitem__("peak_rss_bytes", ExplosiveString()),
            lambda m: m["specification"]["cells"][0].__setitem__("raw", []),
            lambda m: m["specification"]["evaluation_bounds"].__setitem__("origin_count", 0),
            lambda m: m["checks"].__setitem__("source_identity", "true"),
            lambda m: m["outputs"]["artifacts"].append(dict(relative_path="results/run-manifest.json", kind="manifest", bytes=1, sha256="f" * 64, row_count=None)),
            lambda m: m["undefined_conventions"].__setitem__("csv_empty_is_null", 1),
        ]
        for change in changes:
            manifest = artificial_manifest()
            change(manifest)
            with self.subTest(change=changes.index(change)), self.assertRaises((ValueError, TypeError)):
                self.report.validate_run_manifest(manifest, SCHEMA)

    def test_explicit_fetch_download_has_exact_nested_allowlist(self):
        manifest = artificial_manifest()
        manifest["source"]["request_performed_this_attempt"] = True
        manifest["source"]["acquisition_mode"] = "explicit_fetch"
        manifest["source"]["download"] = dict(
            endpoint=SPEC["source"]["fetch_endpoint"], http_status=200,
            redirect_hosts=["storage.googleapis.com"], redirect_statuses=[302],
            query_present=True, archive_bytes=100, archive_sha256="e" * 64)
        self.report.validate_run_manifest(manifest, SCHEMA)
        manifest["source"]["download"]["response_body"] = "secret"
        with self.assertRaises(ValueError):
            self.report.validate_run_manifest(manifest, SCHEMA)

    def test_accepted_explicit_fetch_requires_observed_download_metadata(self):
        manifest = artificial_manifest(True)
        manifest["source"]["acquisition_mode"] = "explicit_fetch"
        manifest["source"]["request_performed_this_attempt"] = True
        # A successful accepted fetch cannot skip the actual transport observations.
        self.assertIsNone(manifest["source"]["download"])
        with self.assertRaises(ValueError):
            self.report.validate_run_manifest(manifest, SCHEMA)


if __name__ == "__main__":
    unittest.main()
