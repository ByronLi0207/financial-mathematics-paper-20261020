"""One bounded entry point for the frozen sampled-inventory study."""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SPEC_SHA256 = "0b8eda7bfd858c038bae22a96a7caa5ff21838317de58bc56eef98ca696c54ff"
SCHEMA_SHA256 = "3bef13d68c65160b9642d715344e10a4e40ddb52c6439d09a9b5573b54e6b752"
THREAD_NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
                "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
CODE_FILES = ("study_data.py", "study_core.py", "study_report.py", "run_study.py",
              "test_data.py", "test_core.py", "test_report.py", "test_runner.py")
CELL_ORDER = ("main", "h12", "h24", "n480", "n1440", "tau90", "tau99")
METHODS = ("F", "S", "R", "L", "P0")
CHECK_NAMES = ("source_identity", "schema", "chronology", "common_origins",
               "label_maturity", "finite_results", "floors_and_geometry",
               "cross_cell_invariants", "mechanism_partitions",
               "aggregate_reconciliation", "same_block_equivalence",
               "resources", "public_serialization")


class StudyStop(Exception):
    """Sanitized failure; never carries input paths or underlying exception text."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_thread_snapshot(text, pid):
    if type(text) is not str or type(pid) is not int or pid <= 0:
        raise StudyStop("RESOURCE_UNVERIFIED")
    raw_rows = [line for line in text.splitlines() if line.strip()]
    rows = [line.strip() for line in raw_rows]
    native_header = ["USER", "PID", "TT", "%CPU", "STAT", "PRI", "STIME", "UTIME", "COMMAND"]
    if rows and rows[0].split() == native_header:
        right = raw_rows[0].index("TT", raw_rows[0].index("PID") + 3)
        fields = raw_rows[1:]
        if not fields or any(not row[:right].split() or row[:right].split()[-1] != str(pid) or row.split()[-1] != str(pid) for row in fields):
            raise StudyStop("RESOURCE_UNVERIFIED")
        return len(fields)
    if rows and rows[0] == "PID":
        rows = rows[1:]
    if not rows or any(not row.isdecimal() or int(row) != pid for row in rows):
        raise StudyStop("RESOURCE_UNVERIFIED")
    return len(rows)


def check_resource_limits(elapsed, rss, threads):
    if (type(elapsed) not in (float, int) or not math.isfinite(elapsed) or elapsed < 0
            or type(rss) is not int or rss <= 0
            or type(threads) is not int or threads < 1):
        raise StudyStop("RESOURCE_UNVERIFIED")
    if elapsed >= 540:
        raise StudyStop("RESOURCE_WALL")
    if rss >= 1610612736:
        raise StudyStop("RESOURCE_RSS")
    if threads > 2:
        raise StudyStop("RESOURCE_THREADS")


def arm_hard_deadline(seconds=600.0):
    if type(seconds) not in (float, int) or not math.isfinite(seconds) or seconds <= 0:
        raise StudyStop("RESOURCE_UNVERIFIED")
    try:
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.setitimer(signal.ITIMER_REAL, float(seconds))
    except (AttributeError, OSError, ValueError):
        raise StudyStop("RESOURCE_UNVERIFIED") from None


def create_attempt(path):
    path = Path(path)
    try:
        if any(parent.is_symlink() for parent in (path, *path.parents)):
            raise StudyStop("OUTPUT_INTEGRITY")
        path.mkdir(mode=0o700, parents=False, exist_ok=False)
        public, private = path / "public", path / "private"
        public.mkdir(mode=0o700)
        private.mkdir(mode=0o700)
        return public, private
    except OSError:
        raise StudyStop("OUTPUT_INTEGRITY") from None


def private_json(path, value):
    # All callers supply explicit scalar metadata, never source arrays/objects.
    data = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)


def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def origin_identity(origins):
    values = [int(value) for value in origins]
    if not values or values[0] < 0 or any(b != a + 1 for a, b in zip(values, values[1:])):
        raise StudyStop("STRUCTURAL_OR_NUMERIC")
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.to_bytes(8, "little", signed=False))
    return dict(origin_count=len(values), first_source_index=values[0], last_source_index=values[-1]), digest.hexdigest()


def collect_profiles(core, d, cell, guard, private):
    rows, means = [], {}
    for ell in (120, 240, 720, 1440):
        def progress(**kwargs):
            if kwargs.get("completed_replicates") != 999:
                guard(**kwargs)
        part = core.stationary_mean_profile(d, [ell], 999, 20261020, checkpoint=progress, cell=cell)
        private_json(private / ("completed-profile-" + str(ell) + ".json"), part.rows[0])
        guard.resources["completed_stability_lengths"].append(ell)
        rows.extend(part.rows)
        means.update(part.replicate_means)
        guard(stage="stability", length=ell, completed_replicates=999)
    return core.StabilityResult(rows, means, part.observed_mean_d, part.constant_input, part.constant_shortcut_used)


def prepare_fetch_destination(path):
    canonical = ROOT / ".scratch/data/1hourNetPositionsKaggle.csv"
    if path.absolute() != canonical.absolute() or any(p.is_symlink() for p in (path, *path.parents)):
        raise StudyStop("SOURCE_FETCH_OR_ARCHIVE")
    try:
        canonical.parent.mkdir(mode=0o700, exist_ok=True)
    except OSError:
        raise StudyStop("SOURCE_FETCH_OR_ARCHIVE") from None


def load_protocol():
    try:
        spec_bytes = (ROOT / "protocol/study-spec.json").read_bytes()
        schema_bytes = (ROOT / "protocol/output-schema.json").read_bytes()
        if hashlib.sha256(spec_bytes).hexdigest() != SPEC_SHA256:
            raise StudyStop("SPECIFICATION")
        if hashlib.sha256(schema_bytes).hexdigest() != SCHEMA_SHA256:
            raise StudyStop("SPECIFICATION")
        spec, schema = json.loads(spec_bytes), json.loads(schema_bytes)
        if (spec["outputs"]["output_schema_sha256"] != SCHEMA_SHA256
                or tuple(c["cell_id"] for c in spec["cells"]) != CELL_ORDER
                or tuple(spec["methods"]["order"]) != METHODS):
            raise StudyStop("SPECIFICATION")
        return spec, schema
    except (OSError, ValueError, KeyError, TypeError):
        raise StudyStop("SPECIFICATION") from None


class RunGuard:
    def __init__(self, start, started_utc, attempt, public, private):
        self.start = start
        self.attempt, self.public, self.private = attempt, public, private
        self.peak_array_bytes = 0
        self.warning_seen = False
        self.resources = {
            "started_utc": started_utc, "checkpoint_utc": None,
            "measurement_point": "final_checkpoint_before_manifest",
            "requested_numerical_threads": 1, "elapsed_seconds": None,
            "peak_rss_bytes": None, "maximum_observed_os_threads": None,
            "thread_probe_status": "UNVERIFIED", "thread_snapshot_count": 0,
            "completed_stability_lengths": [], "current_stage": "initialization",
            "current_cell_id": None, "current_length": None,
            "completed_origins_current_cell": 0,
            "completed_replicates_current_length": 0,
            "new_output_bytes_at_checkpoint": 0,
            "private_numeric_output_bytes_at_checkpoint": 0,
            "public_analysis_output_bytes_at_checkpoint": 0,
        }

    def remaining_seconds(self):
        remaining = 540.0 - (time.monotonic() - self.start)
        if remaining <= 0:
            raise StudyStop("RESOURCE_WALL")
        return remaining

    @staticmethod
    def tree_bytes(path):
        total = 0
        for entry in path.rglob("*"):
            if entry.is_symlink():
                raise StudyStop("OUTPUT_INTEGRITY")
            if entry.is_file():
                total += entry.stat().st_size
        return total

    def arrays(self, *objects):
        seen = set()
        def count(obj):
            if id(obj) in seen:
                return 0
            seen.add(id(obj))
            if hasattr(obj, "nbytes") and hasattr(obj, "shape"):
                size = int(obj.nbytes)
                if size > 67108864:
                    raise StudyStop("RESOURCE_RSS")
                return size
            if is_dataclass(obj):
                return sum(count(getattr(obj, field.name)) for field in fields(obj))
            if type(obj) is dict:
                return sum(count(value) for value in obj.values())
            if type(obj) in (list, tuple):
                return sum(count(value) for value in obj)
            return 0
        size = sum(count(obj) for obj in objects)
        self.peak_array_bytes = max(size, self.peak_array_bytes)
        if size > 134217728:
            raise StudyStop("RESOURCE_RSS")

    def __call__(self, *, stage=None, cell_id=None, length=None,
                 completed_origins=None, completed_replicates=None, **unknown):
        if unknown:
            raise StudyStop("STRUCTURAL_OR_NUMERIC")
        if platform.system() != "Darwin":
            raise StudyStop("RESOURCE_UNVERIFIED")
        try:
            elapsed = float(time.monotonic() - self.start)
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if type(rss) is not int:
                raise StudyStop("RESOURCE_UNVERIFIED")
            probe = subprocess.run(["/bin/ps", "-M", "-p", str(os.getpid()), "-o", "pid="],
                                   capture_output=True, text=True, check=True,
                                   timeout=min(5.0, max(0.01, self.remaining_seconds())))
            threads = parse_thread_snapshot(probe.stdout, os.getpid())
        except (OSError, subprocess.SubprocessError):
            raise StudyStop("RESOURCE_UNVERIFIED") from None
        self.resources.update(
            checkpoint_utc=utc_now(), elapsed_seconds=elapsed,
            peak_rss_bytes=int(rss), thread_probe_status="PASS",
            thread_snapshot_count=self.resources["thread_snapshot_count"] + 1,
            maximum_observed_os_threads=max(threads, self.resources["maximum_observed_os_threads"] or 0))
        if stage is not None:
            self.resources["current_stage"] = str(stage)
        self.resources["current_cell_id"] = cell_id
        self.resources["current_length"] = length
        if completed_origins is not None:
            self.resources["completed_origins_current_cell"] = int(completed_origins)
        if completed_replicates is not None:
            self.resources["completed_replicates_current_length"] = int(completed_replicates)
        if elapsed >= 480:
            self.warning_seen = True
        check_resource_limits(elapsed, int(rss), threads)
        public_bytes, private_bytes = self.tree_bytes(self.public), self.tree_bytes(self.private)
        self.resources.update(new_output_bytes_at_checkpoint=public_bytes + private_bytes,
                              private_numeric_output_bytes_at_checkpoint=private_bytes,
                              public_analysis_output_bytes_at_checkpoint=public_bytes)
        if public_bytes > 10485760 or private_bytes > 67108864 or public_bytes + private_bytes > 83886080:
            raise StudyStop("RESOURCE_STORAGE")


def initial_manifest(spec, attempt_id, started_utc, code_hashes):
    source_keys = ("dataset", "version", "public_url", "requested_member", "expected_csv_bytes",
                   "expected_csv_sha256", "timestamp_timezone", "observed_rights_label",
                   "raw_redistribution_verified")
    source = {key: spec["source"][key] for key in source_keys}
    source.update(accepted_csv_bytes=None, accepted_csv_sha256=None, source_verified=False,
                  acquisition_mode=None, request_performed_this_attempt=False,
                  historical_access_utc=None, local_validation_utc=None, download=None)
    cells = [{key: c[key] for key in ("cell_id", "horizon", "window", "tau_numerator",
                                      "tau_denominator", "expected_rank")} for c in spec["cells"]]
    return {
        "manifest_schema_version": 1, "declared_scope": spec["scope"],
        "study_id": spec["study_id"], "attempt_id": attempt_id,
        "run_status": "INCOMPLETE", "stop_code": "NONE", "planned_cell_ids": list(CELL_ORDER),
        "completed_cell_ids": [], "method_ids": list(METHODS), "source": source,
        "specification": {"relative_path": "protocol/study-spec.json", "sha256": SPEC_SHA256,
                          "schema_version": 1, "primary_cell_id": "main", "amends_sha256": None,
                          "common_origin_reference_sha256": None, "cells": cells,
                          "evaluation_bounds": {"origin_count": None, "first_source_index": None,
                                                "last_source_index": None}},
        "code": {"revision": None, "files": [{"relative_path": n, "sha256": code_hashes[n]} for n in CODE_FILES]},
        "environment": {"python_implementation": platform.python_implementation(),
                        "python_version": platform.python_version(), "os_family": platform.system(),
                        "os_version": platform.release(), "architecture": platform.machine(),
                        "numpy_version": None, "reportlab_version": None,
                        "thread_requests": {key: os.environ.get(key) for key in THREAD_NAMES}},
        "resources": {}, "checks": {key: "NOT_RUN" for key in CHECK_NAMES},
        "outputs": {"artifacts": []},
        "undefined_conventions": {"csv_empty_is_null": True, "json_nonfinite_allowed": False,
                                  "zero_breach_reason": "NO_STRICT_BREACHES",
                                  "zero_s_loss_reason": "ZERO_MEAN_LOSS_S", "display_min_origins": 30,
                                  "below_display_reason": "GROUP_BELOW_DISPLAY_MIN",
                                  "empty_group_reason": "NO_ORIGINS"},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / ".scratch/data/1hourNetPositionsKaggle.csv")
    parser.add_argument("--fetch", action="store_true", help="Explicit missing-source-only bounded acquisition")
    parser.add_argument("--attempt-dir", type=Path, help="New output directory under this project's .scratch")
    args = parser.parse_args(argv)
    if args.fetch and args.input.absolute() != (ROOT / ".scratch/data/1hourNetPositionsKaggle.csv").absolute():
        raise StudyStop("SOURCE_FETCH_OR_ARCHIVE")
    start, started_utc = time.monotonic(), utc_now()
    for name in THREAD_NAMES:
        os.environ[name] = "1"
    sys.dont_write_bytecode = True
    spec, schema = load_protocol()
    attempt_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    scratch = ROOT / ".scratch"
    try:
        scratch.mkdir(exist_ok=True)
    except OSError:
        raise StudyStop("OUTPUT_INTEGRITY") from None
    if args.fetch:
        prepare_fetch_destination(args.input)
    attempt = args.attempt_dir or scratch / ("analysis-" + attempt_id)
    try:
        attempt.absolute().relative_to(scratch.absolute())
        if ".." in attempt.parts:
            raise ValueError
    except ValueError:
        raise StudyStop("OUTPUT_INTEGRITY") from None
    public, private = create_attempt(attempt)
    try:
        hashes = {name: sha_file(ROOT / name) for name in CODE_FILES}
    except OSError:
        raise StudyStop("OUTPUT_INTEGRITY") from None
    manifest = initial_manifest(spec, attempt_id, started_utc, hashes)
    guard = RunGuard(start, started_utc, attempt, public, private)
    report = None
    try:
        arm_hard_deadline(600.0 - (time.monotonic() - start))
        import study_report as report
        try:
            import numpy as np
            import reportlab
            import study_data as data
            import study_core as core
        except ImportError:
            raise StudyStop("RUNTIME_UNAVAILABLE") from None
        manifest["environment"]["numpy_version"] = str(np.__version__)
        manifest["environment"]["reportlab_version"] = str(reportlab.Version)
        if np.__version__ != "2.3.5" or reportlab.Version != "4.4.9":
            raise StudyStop("RUNTIME_UNAVAILABLE")
        guard(stage="after_imports")
        cells = [core.CellSpec.from_dict(c) for c in spec["cells"]]
        source = data.load_source(args.input, spec["source"], fetch=args.fetch,
                                  remaining_seconds=guard.remaining_seconds, checkpoint=guard)
        for key in ("accepted_csv_bytes", "accepted_csv_sha256", "source_verified", "acquisition_mode",
                    "request_performed_this_attempt", "local_validation_utc", "download"):
            manifest["source"][key] = source.identity[key]
        manifest["source"]["historical_access_utc"] = "2026-10-21T02:42:07Z"
        manifest["checks"].update(source_identity="PASS", schema="PASS", chronology="PASS")
        guard.arrays(source)
        guard(stage="after_source")
        origins = core.common_origins(source.times, cells, spec["evaluation"]["cutoff_naive"])
        if not len(origins):
            raise StudyStop("STRUCTURAL_OR_NUMERIC")
        bounds, origins_sha256 = origin_identity(origins)
        manifest["specification"]["evaluation_bounds"] = bounds
        manifest["specification"]["common_origin_reference_sha256"] = origins_sha256
        manifest["checks"]["common_origins"] = "PASS"
        # Independent exact artificial arithmetic checks, never source-dependent.
        if core.explicit_block_mean(np.array([2., -1., 4., 0.]), [(3, 3), (0, 4)]) != 0.75:
            raise StudyStop("STRUCTURAL_OR_NUMERIC")
        b = float(2 ** 53)
        if core.explicit_block_mean(np.array([b, 1., -b, 1.]), [(1, 1)] * 4) != 1.0:
            raise StudyStop("STRUCTURAL_OR_NUMERIC")
        core.check_explicit_block_equivalence(np.array([2., -1., 4., 0.]), [(3, 3), (0, 4)])
        manifest["checks"]["same_block_equivalence"] = "PASS"
        caches = {}
        for h in (6, 12, 24):
            caches[h] = core.build_label_cache(source.position, h)
            guard.arrays(source, origins, caches)
            guard(stage="after_cache")
        summary, paired, results = [], [], {}
        for cell in cells:
            cache = caches[cell.horizon]
            batch = core.forecast_cell(source.position, cache, origins, cell, checkpoint=guard)
            evaluation = core.evaluate_caps(cache.peak[origins], batch, cell.tau)
            rows, contrast = core.summarize_cell(cell, batch, evaluation)
            summary.extend(rows)
            paired.append(contrast)
            results[cell.cell_id] = (cell, batch, evaluation, cache)
            manifest["completed_cell_ids"].append(cell.cell_id)
            private_json(private / ("completed-cell-" + cell.cell_id + ".json"), {"summary": rows, "paired": contrast})
            guard.arrays(source, origins, caches, results)
            guard(stage="after_cell", cell_id=cell.cell_id, completed_origins=int(len(origins)))
        core.validate_cross_cells(results)
        for key in ("label_maturity", "finite_results", "floors_and_geometry", "cross_cell_invariants",
                    "mechanism_partitions", "aggregate_reconciliation"):
            manifest["checks"][key] = "PASS"
        main_cell, main_batch, main_eval, _ = results["main"]
        diagnostics = core.diagnostics_main(source.times, source.position, origins, main_cell,
                                            main_batch, main_eval, spec["evaluation"]["cutoff_naive"])
        d = main_eval.pinball[:, 0] - main_eval.pinball[:, 1]
        profile = collect_profiles(core, d, main_cell, guard, private)
        guard.arrays(source, origins, caches, results, d, profile)
        bundle = report.AggregateBundle(summary, paired, profile.rows, diagnostics)
        guard(stage="before_output_writes")
        artifacts = report.write_aggregate_outputs(bundle, public, schema)
        manifest["outputs"]["artifacts"] = artifacts
        guard(stage="after_output_writes")
        if hashes != {name: sha_file(ROOT / name) for name in CODE_FILES}:
            raise StudyStop("SPECIFICATION")
        load_protocol()
        manifest["checks"]["public_serialization"] = "PASS"
        private_json(private / "final-verification.json", {
            "maximum_named_live_array_bytes_observed": guard.peak_array_bytes,
            "code_identity_unchanged": True, "spec_identity_unchanged": True,
            "external_manifest_hash_verification_required": True})
        guard(stage="final_manifest_checkpoint")
        manifest["checks"]["resources"] = "PASS"
        manifest.update(run_status="COMPLETE", stop_code="NONE", resources=dict(guard.resources))
        report.write_run_manifest(manifest, public, schema)
        print(json.dumps({"run_status": "COMPLETE", "attempt_id": attempt_id,
                          "elapsed_seconds_at_checkpoint": guard.resources["elapsed_seconds"],
                          "peak_rss_bytes": guard.resources["peak_rss_bytes"],
                          "maximum_observed_os_threads": guard.resources["maximum_observed_os_threads"]}))
        return 0
    except Exception as error:
        code = error.code if getattr(error, "code", None) in schema["run_manifest"]["stop_code"] else (
            "STRUCTURAL_OR_NUMERIC" if isinstance(error, (ValueError, ArithmeticError)) else "INTERNAL")
        manifest.update(run_status="INCOMPLETE", stop_code=code, resources=dict(guard.resources))
        try:
            private_json(private / "stop.json", {"stop_code": code, "stage": guard.resources["current_stage"],
                                                 "completed_cell_ids": manifest["completed_cell_ids"]})
        except OSError:
            pass  # A failed storage device cannot prevent sanitized stdout.
        if report is not None and not (public / "results/run-manifest.json").exists():
            try:
                report.write_run_manifest(manifest, public, schema)
            except Exception:
                pass  # Sanitized stop.json remains; never substitute fabricated provenance.
        print(json.dumps({"run_status": "INCOMPLETE", "stop_code": code, "attempt_id": attempt_id}))
        return 1
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except StudyStop as error:
        print(json.dumps({"run_status": "INCOMPLETE", "stop_code": error.code}))
        sys.exit(1)
