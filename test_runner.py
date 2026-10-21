"""Artificial orchestration/resource checks; no scientific source is loaded."""
import importlib
import math
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent

class RunnerTests(unittest.TestCase):
    def setUp(self):
        try:
            self.runner = importlib.import_module("run_study")
        except ModuleNotFoundError as error:
            if error.name == "run_study":
                self.fail("The bounded study runner has not yet been implemented")
            raise

    def test_known_header_and_each_own_pid_row_count_as_observed_threads(self):
        self.assertEqual(self.runner.parse_thread_snapshot("  PID\n  421\n421\n", 421), 2)
        self.assertEqual(self.runner.parse_thread_snapshot("421\n", 421), 1)
        native = "USER PID TT %CPU STAT PRI STIME UTIME COMMAND\nname 421 ?? 0.0 S 31T 0:00.01 0:00.02 /Python 421\nname 421 ?? 0.0 S 31T 0:00.00 0:00.00 /Python 421\n"
        self.assertEqual(self.runner.parse_thread_snapshot(native, 421), 2)
        native_sparse = "USER        PID   TT   %CPU STAT PRI     STIME     UTIME COMMAND      \nname        421   ??    0.0 S    31T   0:00.01   0:00.02 /Python 421\n            421         0.0 S    31T   0:00.00   0:00.00         421\n"
        self.assertEqual(self.runner.parse_thread_snapshot(native_sparse, 421), 2)
        native_right_aligned = "USER        PID   TT   %CPU STAT PRI     STIME     UTIME COMMAND      \nexamplexx 30281   ??    0.0 S    31T   0:00.02   0:00.06 /Python 30281\n"
        self.assertEqual(self.runner.parse_thread_snapshot(native_right_aligned, 30281), 1)

    def test_missing_or_foreign_or_malformed_thread_observation_is_not_zero(self):
        for value in ["", "PID\n", "PID LWP\n421 1\n", "PID\n421\n422\n", "nonsense"]:
            with self.subTest(value=value):
                with self.assertRaises(self.runner.StudyStop) as caught:
                    self.runner.parse_thread_snapshot(value, 421)
                self.assertEqual(caught.exception.code, "RESOURCE_UNVERIFIED")

    def test_actual_resource_limits_stop_without_silently_disabling_measurement(self):
        self.runner.check_resource_limits(1.25, 123456, 2)
        cases = [(540.0, 123456, 1, "RESOURCE_WALL"),
                 (1.0, 1610612736, 1, "RESOURCE_RSS"),
                 (1.0, 123456, 3, "RESOURCE_THREADS"),
                 (math.nan, 123456, 1, "RESOURCE_UNVERIFIED"),
                 (-1.0, 123456, 1, "RESOURCE_UNVERIFIED"),
                 (1.0, None, 1, "RESOURCE_UNVERIFIED"),
                 (1.0, 0, 1, "RESOURCE_UNVERIFIED"),
                 (1.0, 123456, 0, "RESOURCE_UNVERIFIED")]
        for elapsed, rss, threads, code in cases:
            with self.subTest(code=code, elapsed=elapsed, rss=rss, threads=threads):
                with self.assertRaises(self.runner.StudyStop) as caught:
                    self.runner.check_resource_limits(elapsed, rss, threads)
                self.assertEqual(caught.exception.code, code)

    def test_exclusive_attempt_paths_and_private_modes(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as folder:
            attempt = Path(folder) / "attempt"
            public, private = self.runner.create_attempt(attempt)
            self.assertEqual(public, attempt / "public")
            self.assertEqual(private, attempt / "private")
            self.assertTrue(public.is_dir() and private.is_dir())
            self.assertEqual(attempt.stat().st_mode & 0o777, 0o700)
            marker = private / "completed-stage.txt"
            marker.write_text("preserve")
            with self.assertRaises(self.runner.StudyStop):
                self.runner.create_attempt(attempt)
            self.assertEqual(marker.read_text(), "preserve")

    def test_short_os_alarm_terminates_even_without_a_checkpoint(self):
        code = "import run_study,time;run_study.arm_hard_deadline(0.05);time.sleep(2)"
        process = subprocess.run([sys.executable, "-B", "-c", code], cwd=ROOT,
                                 capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, -signal.SIGALRM)

    def test_help_is_available_without_a_scientific_run(self):
        process = subprocess.run([sys.executable, "-B", str(ROOT / "run_study.py"), "--help"],
                                 capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 0)
        self.assertIn("--fetch", process.stdout)
        self.assertIn("--attempt-dir", process.stdout)

    def test_initial_manifest_uses_frozen_scope_and_is_report_compatible(self):
        import study_report
        spec, schema = self.runner.load_protocol()
        manifest = self.runner.initial_manifest(spec, "artificial-runner", "2026-10-21T06:00:00Z", {name: "a" * 64 for name in self.runner.CODE_FILES})
        self.assertEqual(manifest["declared_scope"], spec["scope"])
        manifest["stop_code"] = "RESOURCE_UNVERIFIED"
        guard = self.runner.RunGuard(0., "2026-10-21T06:00:00Z", ROOT, ROOT, ROOT)
        manifest["resources"] = guard.resources
        study_report.validate_run_manifest(manifest, schema)

    def test_common_origin_identity_is_explicit_little_endian_indices(self):
        import hashlib
        self.assertTrue(hasattr(self.runner, "origin_identity"), "Common origin fingerprint is not implemented")
        bounds, digest = self.runner.origin_identity([2, 3])
        self.assertEqual(bounds, dict(origin_count=2, first_source_index=2, last_source_index=3))
        self.assertEqual(digest, hashlib.sha256(bytes([2]) + bytes(7) + bytes([3]) + bytes(7)).hexdigest())
        for values in [[], [2, 4], [-1, 0]]:
            with self.assertRaises(self.runner.StudyStop):
                self.runner.origin_identity(values)

    def test_setup_filesystem_failure_is_sanitized(self):
        from unittest.mock import patch
        with patch.object(Path, "mkdir", side_effect=OSError("private path")):
            with self.assertRaises(self.runner.StudyStop) as caught:
                self.runner.main([])
        self.assertEqual(caught.exception.code, "OUTPUT_INTEGRITY")

    def test_completed_profile_is_preserved_before_a_later_failure(self):
        from types import SimpleNamespace
        def profile(d, lengths, *args, **kwargs):
            if lengths == [240]:
                raise self.runner.StudyStop("RESOURCE_WALL")
            return SimpleNamespace(rows=[dict(ell=120, observed_mean_d=1.)], replicate_means={120: [1.]})
        core = SimpleNamespace(stationary_mean_profile=profile)
        class Guard:
            resources = {"completed_stability_lengths": []}
            def __call__(self, **kwargs):
                pass
        guard = Guard()
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as folder:
            private = Path(folder)
            with self.assertRaises(self.runner.StudyStop):
                self.runner.collect_profiles(core, [1.], None, guard, private)
            self.assertTrue((private / "completed-profile-120.json").is_file())
            self.assertEqual(guard.resources["completed_stability_lengths"], [120])

    def test_fetch_prepares_only_the_fixed_task_cache_and_rejects_symlinks(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as folder:
            root = Path(folder)
            (root / ".scratch").mkdir()
            canonical = root / ".scratch/data/1hourNetPositionsKaggle.csv"
            with patch.object(self.runner, "ROOT", root):
                self.runner.prepare_fetch_destination(canonical)
                self.assertTrue(canonical.parent.is_dir())
                with self.assertRaises(self.runner.StudyStop):
                    self.runner.prepare_fetch_destination(root / "outside.csv")
                canonical.parent.rmdir()
                canonical.parent.symlink_to(root, target_is_directory=True)
                with self.assertRaises(self.runner.StudyStop):
                    self.runner.prepare_fetch_destination(canonical)

if __name__ == "__main__":
    unittest.main()
