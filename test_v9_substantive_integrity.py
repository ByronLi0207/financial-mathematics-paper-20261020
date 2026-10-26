"""Constructed software-contract checks only: no raw data, fitting or TeX engine.

Each fixture is retained by the explicitly selected pytest --basetemp. External
compilation and saved-number construction are replaced at their I/O boundaries;
the command entry points and their acceptance/failure decisions remain real.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parent


def module(name):
    path = ROOT / "notes/revision-v9" / (name + ".py")
    spec = importlib.util.spec_from_file_location("integrity_" + name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def frozen_design():
    return {
        "schema": 1,
        "created_utc": "CONSTRUCTED-NOT-A-RESEARCH-RECEIPT",
        "raw": {"path": "DO-NOT-OPEN-RAW"},
        "clock": {"refit_step": 24},
        "menus": {"QR33": [.001, .01, .1], "QR4": [.001, .01, .1, 1., 10.]},
        "horizons": [6, 24],
        "windows": [360, 720, 1440, 2880, 5760],
        "run_order": [[6, 2880], [24, 2880], [6, 360], [24, 360],
                      [6, 720], [24, 720], [6, 1440], [24, 1440],
                      [6, 5760], [24, 5760]],
        "prediction_ranges": [
            {"horizon": 6, "method": "QR33", "lower": 1., "upper": 2.},
            {"horizon": 6, "method": "QR4", "lower": 1., "upper": 2.},
            {"horizon": 24, "method": "QR33", "lower": 1., "upper": 2.},
            {"horizon": 24, "method": "QR4", "lower": 1., "upper": 2.},
        ],
    }


@pytest.mark.parametrize("changed", ["metadata", "range", "menus", "clock", "raw", "type"])
def test_wp3_rejects_entire_manifest_design_drift_before_source_io(changed):
    api = module("audit_wp3")
    frozen = frozen_design()
    altered = copy.deepcopy(frozen)
    if changed == "metadata":
        altered["created_utc"] = "DRIFT"
    elif changed == "range":
        altered["prediction_ranges"][0]["upper"] = 99.
    elif changed == "menus":
        altered["menus"]["QR33"] = [.01]
    elif changed == "clock":
        altered["clock"]["refit_step"] = 1
    elif changed == "raw":
        altered["raw"]["path"] = "ANOTHER-UNOPENED-PATH"
    else:
        altered["schema"] = True
    with pytest.raises(api.AuditMismatch):
        api.validate_manifest_design({"design": altered}, frozen)


@pytest.mark.parametrize("malformed", ["empty_ranges", "duplicate_ranges", "missing_unit", "duplicate_unit"])
def test_wp3_rejects_incomplete_or_duplicate_frozen_plan(malformed):
    api = module("audit_wp3")
    frozen = frozen_design()
    if malformed == "empty_ranges":
        frozen["prediction_ranges"] = []
    elif malformed == "duplicate_ranges":
        frozen["prediction_ranges"][3] = copy.deepcopy(frozen["prediction_ranges"][0])
    elif malformed == "missing_unit":
        frozen["run_order"].pop()
    else:
        frozen["run_order"][-1] = frozen["run_order"][0]
    with pytest.raises(api.AuditMismatch):
        api.validate_manifest_design({"design": copy.deepcopy(frozen)}, frozen)


def test_wp3_accepts_exact_complete_frozen_plan_without_opening_raw():
    api = module("audit_wp3")
    frozen = frozen_design()
    actual = api.validate_manifest_design({"design": copy.deepcopy(frozen)}, frozen)
    assert actual == frozen


def output_fixture():
    design = frozen_design()
    units = copy.deepcopy(design["run_order"])
    rows = [{"horizon": h, "window": w, "method": method}
            for h, w in units for method in ("QR33", "QR4")]
    curves = [{"horizon": h, "method": method}
              for h in (6, 24) for method in ("QR33", "QR4")]
    return design, units, rows, curves


@pytest.mark.parametrize("missing", ["unit", "row", "curve", "duplicate_row", "duplicate_curve"])
def test_wp3_complete_cannot_accept_missing_or_duplicate_verified_objects(missing):
    api = module("audit_wp3")
    design, units, rows, curves = output_fixture()
    if missing == "unit":
        units.pop()
    elif missing == "row":
        rows.pop()
    elif missing == "curve":
        curves.clear()
    elif missing == "duplicate_row":
        rows[-1] = rows[0]
    else:
        curves[-1] = curves[0]
    with pytest.raises(api.AuditMismatch):
        api.validate_output_census(design, "COMPLETE", units, rows, curves, curves)


def test_wp3_verified_curve_count_comes_from_actual_saved_objects():
    api = module("audit_wp3")
    design, units, rows, curves = output_fixture()
    actual = api.validate_output_census(design, "COMPLETE", units, rows, curves, copy.deepcopy(curves))
    assert actual == {"planned_units": 10, "planned_conditional_rows": 20,
                      "verified_units": 10, "verified_conditional_inventory_rows": 20,
                      "curve_classifications": 4, "saved_curve_classifications_verified": 4}
    without_saved = api.validate_output_census(design, "BLOCKED", [], rows, curves, None)
    assert without_saved["saved_curve_classifications_verified"] == 0
    with pytest.raises(api.AuditMismatch):
        api.validate_output_census(design, "COMPLETE", units, rows, curves, [])


def test_wp3_blocked_not_attempted_rows_are_inventory_not_completed_results():
    api = module("audit_wp3")
    design, _, rows, curves = output_fixture()
    for row in rows:
        row["status"] = "NOT_ATTEMPTED"
    actual = api.validate_output_census(design, "BLOCKED", [], rows, curves, None)
    assert actual["verified_units"] == 0
    assert actual["verified_conditional_inventory_rows"] == 20
    assert "verified_conditional_rows" not in actual
    assert actual["saved_curve_classifications_verified"] == 0
    assert all(row["status"] == "NOT_ATTEMPTED" for row in rows)


def contrast_scalar_fixture(status):
    reference = {"mean_pinball": 2., "strict_breach_count": 1, "origin_count": 4}
    report = {"method": "QR33", "status": status,
              "selected_penalty": None if status == "INELIGIBLE" else .01,
              "evaluation": None}
    row = {"horizon": 6, "window": 720, "method": "QR33", "status": status,
           "relative_loss_percent": None, "mean_model_loss": None,
           "mean_reference_loss": 2., "model_breaches": None,
           "reference_breaches": 1, "n": 0, "dm": None}
    if status == "COMPLETE":
        report["evaluation"] = {"mean_pinball": 3., "strict_breach_count": 2, "origin_count": 4}
        row.update(relative_loss_percent=50., mean_model_loss=3., model_breaches=2,
                   n=4, dm={"status": "CONSTRUCTED-SCALAR-NO-HAC-CALCULATED"})
    return row, report, reference


def test_wp3_complete_method_report_cannot_be_relabelled_na_to_skip_pair_audit():
    api = module("audit_wp3")
    row, _, reference = contrast_scalar_fixture("EVALUATION_FAILED")
    _, report, _ = contrast_scalar_fixture("COMPLETE")
    with pytest.raises(api.AuditMismatch):
        api.validate_contrast_status_and_na(row, report, reference, 6, 720)


def test_wp3_incomplete_method_report_cannot_be_relabelled_complete():
    api = module("audit_wp3")
    row, _, reference = contrast_scalar_fixture("COMPLETE")
    _, report, _ = contrast_scalar_fixture("INELIGIBLE")
    with pytest.raises(api.AuditMismatch):
        api.validate_contrast_status_and_na(row, report, reference, 6, 720)


@pytest.mark.parametrize("status", ["INELIGIBLE", "EVALUATION_FAILED", "FAILED"])
def test_wp3_genuine_failure_contrast_preserves_na_and_verified_reference_scalars(status):
    api = module("audit_wp3")
    row, report, reference = contrast_scalar_fixture(status)
    before = copy.deepcopy((row, report, reference))
    api.validate_contrast_status_and_na(row, report, reference, 6, 720)
    assert (row, report, reference) == before


@pytest.mark.parametrize("field,value", [
    ("horizon", 24), ("window", 360), ("method", "QR4"),
    ("relative_loss_percent", 0.), ("mean_model_loss", 0.), ("model_breaches", 0),
    ("mean_reference_loss", None), ("mean_reference_loss", 99.),
    ("reference_breaches", None), ("reference_breaches", 99),
    ("reference_breaches", True), ("n", 1), ("n", False), ("dm", {}),
])
def test_wp3_na_contrast_rejects_fabricated_or_missing_scalar_meaning(field, value):
    api = module("audit_wp3")
    row, report, reference = contrast_scalar_fixture("EVALUATION_FAILED")
    row[field] = value
    with pytest.raises(api.AuditMismatch):
        api.validate_contrast_status_and_na(row, report, reference, 6, 720)


@pytest.mark.parametrize("sabotage", ["extra", "missing", "unattempted", "unknown", "evaluation_present"])
def test_wp3_saved_na_contrast_requires_legal_method_status_and_exact_schema(sabotage):
    api = module("audit_wp3")
    row, report, reference = contrast_scalar_fixture("EVALUATION_FAILED")
    if sabotage == "extra":
        row["unbound_extra"] = 0
    elif sabotage == "missing":
        row.pop("mean_reference_loss")
    elif sabotage == "unattempted":
        row["status"] = report["status"] = "NOT_ATTEMPTED"
    elif sabotage == "unknown":
        row["status"] = report["status"] = "UNKNOWN"
    else:
        report["evaluation"] = {"mean_pinball": 3.}
    with pytest.raises(api.AuditMismatch):
        api.validate_contrast_status_and_na(row, report, reference, 6, 720)


def test_wp3_complete_status_admission_does_not_calculate_hac_or_require_significance():
    api = module("audit_wp3")
    row, report, reference = contrast_scalar_fixture("COMPLETE")
    api.validate_contrast_status_and_na(row, report, reference, 6, 720)
    assert row["dm"] == {"status": "CONSTRUCTED-SCALAR-NO-HAC-CALCULATED"}


def test_wp3_true_na_retains_a_zero_reference_score_without_dividing():
    api = module("audit_wp3")
    row, report, reference = contrast_scalar_fixture("INELIGIBLE")
    row["mean_reference_loss"] = reference["mean_pinball"] = 0.
    api.validate_contrast_status_and_na(row, report, reference, 6, 720)
    assert row["relative_loss_percent"] is None and row["dm"] is None


BUILDERS = ("build_wp5_tables", "build_continuation_tables")
TARGETS = {
    "build_wp5_tables": ("submission-jof/generated/v9-evidence-tables.tex",
                         "notes/revision-v9/wp6-new-number-bindings.json"),
    "build_continuation_tables": ("submission-jof/generated/v9-complete-diagnostic-fields.tex",
                                 "notes/revision-v9/continuation-number-bindings.json"),
}
CONSTRUCTED_RECEIPT = {"bindings": [], "namedfacts": {}, "table_rows": [],
                       "primary_screen_exceptions": [], "paired_loss_rows": []}


def builder_case(tmp_path, name, state):
    for relative in TARGETS[name]:
        (tmp_path / relative).parent.mkdir(parents=True, exist_ok=True)
    if state != "missing":
        (tmp_path / TARGETS[name][0]).write_text("literal fixture\n" if state == "matching" else "MISMATCH\n")
        (tmp_path / TARGETS[name][1]).write_text(json.dumps(CONSTRUCTED_RECEIPT if state == "matching" else {}))


def run_builder(tmp_path, name, optimize, check=True):
    # Replace only saved-number construction, so no archived numeric inputs are
    # loaded. The real main() still decides acceptance, exit status and writes.
    code = "\n".join([
        "import importlib.util,json,sys",
        "from pathlib import Path",
        f"spec=importlib.util.spec_from_file_location('constructed_builder',{str(ROOT / 'notes/revision-v9' / (name+'.py'))!r})",
        "api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)",
        f"api.ROOT=Path({str(tmp_path)!r})",
        f"api.build=lambda root: ('literal fixture\\n',json.loads({json.dumps(CONSTRUCTED_RECEIPT)!r}))",
        f"sys.argv={[name+'.py', *(['--root', str(tmp_path)] if name=='build_wp5_tables' else []), *(['--check'] if check else [])]!r}",
        "api.main()",
    ])
    env = dict(os.environ, PYTHONOPTIMIZE=str(optimize), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, "-B", "-c", code], cwd=tmp_path, env=env,
                          capture_output=True, text=True, timeout=15)


@pytest.mark.parametrize("name", BUILDERS)
@pytest.mark.parametrize("state", ["missing", "mismatch"])
@pytest.mark.parametrize("optimize", [0, 1])
def test_documented_builders_never_report_pass_for_missing_or_mismatched_targets(tmp_path, name, state, optimize):
    builder_case(tmp_path, name, state)
    result = run_builder(tmp_path, name, optimize)
    assert result.returncode != 0, result.stdout
    assert '"status": "PASS"' not in result.stdout


@pytest.mark.parametrize("name", BUILDERS)
@pytest.mark.parametrize("optimize", [0, 1])
def test_builder_generation_refuses_to_overwrite_existing_evidence(tmp_path, name, optimize):
    builder_case(tmp_path, name, "mismatch")
    before = [(tmp_path / target).read_bytes() for target in TARGETS[name]]
    result = run_builder(tmp_path, name, optimize, check=False)
    assert result.returncode != 0, result.stdout
    assert [(tmp_path / target).read_bytes() for target in TARGETS[name]] == before


@pytest.mark.parametrize("name", BUILDERS)
def test_builder_normal_check_accepts_matching_constructed_evidence_without_writes(tmp_path, name):
    builder_case(tmp_path, name, "matching")
    before = [(tmp_path / target).read_bytes() for target in TARGETS[name]]
    result = run_builder(tmp_path, name, 0)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "PASS"
    assert [(tmp_path / target).read_bytes() for target in TARGETS[name]] == before


@pytest.mark.parametrize("bad_log", [
    "LaTeX Warning: Reference `missing' on page 1 undefined",
    "Missing character: There is no Ω in font",
    "Overfull \\hbox (8.0pt too wide)",
])
def test_compile_zero_exit_with_serious_diagnostics_fails_and_records_reason(tmp_path, monkeypatch, bad_log):
    api, receipt = compile_fixture(tmp_path, monkeypatch, bad_log)
    with pytest.raises(SystemExit) as stopped:
        api.main()
    assert stopped.value.code == 1
    result = json.loads(receipt.read_text())
    assert result["status"] == "FAIL" and result["diagnostics_clean"] is False
    assert result["error_undefined_missing_glyph_overfull_lines"] == [bad_log]
    assert result["failure_reasons"] == ["SERIOUS_TEX_DIAGNOSTICS"]


def compile_fixture(tmp_path, monkeypatch, log):
    api = module("compile_documents")
    (tmp_path / "submission-jof").mkdir()
    (tmp_path / "notes/revision-v9").mkdir(parents=True)
    (tmp_path / "submission-jof/manuscript.tex").write_text("CONSTRUCTED SOURCE; NOT COMPILED\n")
    monkeypatch.setattr(api, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["compile_documents.py", "--stage", "constructed", "--targets", "manuscript"])

    def compiler_double(command, *, cwd, env, stdout, stderr, timeout):
        # Preserve the compiler's file side effects in the isolated fixture,
        # without invoking a process, parsing TeX or accessing a real PDF.
        destination = Path(cwd) / command[command.index("--outdir") + 1]
        (destination / "manuscript.log").write_text(log)
        (destination / "manuscript.pdf").write_bytes(b"%PDF-CONSTRUCTED-NOT-A-COMPILED-DOCUMENT\n")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(api.subprocess, "run", compiler_double)
    return api, tmp_path / "notes/revision-v9/constructed-manuscript-compile-receipt.json"


def test_compile_clean_zero_exit_has_explicit_pass_receipt(tmp_path, monkeypatch):
    api, receipt = compile_fixture(tmp_path, monkeypatch, "Constructed clean compiler log\n")
    api.main()
    result = json.loads(receipt.read_text())
    assert result["status"] == "PASS" and result["diagnostics_clean"] is True
    assert result["failure_reasons"] == []
