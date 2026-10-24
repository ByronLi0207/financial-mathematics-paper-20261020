"""Strict admission for the 48 pre-existing additional Treasury panel cells.

No files are read at import, no models are fitted, and no fallback is supplied.
The caller invokes load_panel_cell with the frozen inventory entry and root.
Private current fingerprints are checked together with original public scalar
summaries; they do not establish a pre-existing public NPZ hash binding.
"""
import hashlib
import json
from pathlib import Path
from zipfile import BadZipFile

import numpy as np

from conditional_study import score_predictions, summarize_scores, select_parameter


class DataIdentityError(ValueError):
    """Stop the affected analysis; an identity mismatch is not method NA."""
    def __init__(self, code):
        self.code = str(code)
        super().__init__(self.code)


def _require(condition, code):
    if not condition:
        raise DataIdentityError(code)


def _path(root, relative):
    value = Path(relative)
    _require(not value.is_absolute(), "ABSOLUTE_INPUT_PATH")
    path = (root / value).resolve()
    _require(path.is_relative_to(root), "INPUT_OUTSIDE_ROOT")
    return path


def _json(path):
    return json.loads(path.read_text())


def _pin(path, expected_hash, expected_bytes=None):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    _require(expected_bytes is None or len(data) == expected_bytes, "BYTE_IDENTITY")
    _require(digest == expected_hash, "HASH_IDENTITY")
    return digest


def _one(rows, predicate, code):
    matches = [row for row in rows if predicate(row)]
    _require(len(matches) == 1, code)
    return matches[0]


def _same_fields(left, right, keys, code):
    for key in keys:
        _require(key in left and key in right and left[key] == right[key], code + ":" + key)


def _readonly(array):
    result = np.array(array, copy=True)
    result.flags.writeable = False
    return result


def _load_panel_cell(entry, root):
    inventory = _json(root / ".scratch/revision-v6/input-inventory.json")
    ident = (entry["series_key"], entry["horizon"], entry["window"])
    canonical = _one(inventory["panel_cells"],
                     lambda row: (row["series_key"], row["horizon"], row["window"]) == ident,
                     "CANONICAL_CELL_MISSING_OR_DUPLICATE")
    _require(entry == canonical, "SUPPLIED_ENTRY_IDENTITY")
    key, horizon, window = ident
    _require(type(horizon) is int and type(window) is int, "CELL_INTEGER_IDENTITY")
    _require(entry["exists"] is True and entry["public_cell_exists"] is True,
             "MISSING_ADMISSION_ARTIFACT")
    _require(entry["public_cell_source_matches_provenance"] is True
             and entry["public_cell_selection_binding_matches_current_selection"] is True,
             "FAILED_HISTORICAL_ADMISSION")
    _require(entry["preexisting_public_trace_digest_present"] is False,
             "UNEXPECTED_HISTORICAL_TRACE_HASH_CLAIM")
    _require(entry["required_methods"] == {"F": "frozen_F", "QR": "QR33", "KNN": "KNN"},
             "METHOD_IDENTITY")
    availability = {"F": True, "QR": True, "KNN": False}
    _require(entry["method_availability"] == availability, "METHOD_AVAILABILITY_IDENTITY")

    spec = _json(root / "protocol/revision-20261022/study-spec.json")
    cfg = spec["sources"]["nyfed_weekly"]
    _require(horizon in spec["horizons"] and window in cfg["windows"], "UNDECLARED_CELL")
    val_bounds = [cfg["validation_origin_first"], cfg["validation_origin_last"]]
    bounds = [cfg["evaluation_origin_first"], cfg["evaluation_origin_last"]]
    _require(entry["public_validation_origin_bounds"] == val_bounds
             and entry["public_evaluation_origin_bounds"] == bounds, "INVENTORY_GRID_IDENTITY")

    selection_meta = inventory["panel_selection"]
    selection_path = _path(root, selection_meta["path"])
    selection_hash = _pin(selection_path, selection_meta["sha256"])
    selection = _json(selection_path)
    _require(selection["status"] == "SELECTION_FROZEN_BEFORE_MODELS"
             and selection["eligible"] == selection_meta["eligible"]
             and selection["eligible"].count(key) == 1, "PANEL_SELECTION_IDENTITY")
    selected_source = _one(selection["series"], lambda row: row["series_key"] == key,
                           "SELECTED_SOURCE_IDENTITY")
    source_meta = _one(inventory["panel_source_inputs"], lambda row: row["series_key"] == key,
                       "SOURCE_INVENTORY_IDENTITY")
    _require(source_meta["exists"] is True and source_meta["source_fingerprint_match"] is True,
             "SOURCE_ADMISSION_FAILED")
    _require(source_meta["sha256"] == source_meta["expected_sha256"], "SOURCE_EXPECTED_HASH_IDENTITY")
    source_hash = _pin(_path(root, source_meta["path"]), source_meta["sha256"], source_meta["bytes"])
    provenance_path = _path(root, source_meta["provenance_path"])
    provenance_hash = _pin(provenance_path, source_meta["provenance_sha256"])
    provenance = _json(provenance_path)
    _same_fields(provenance, source_meta,
                 ("series_key", "sha256", "bytes", "aligned_observations",
                  "aligned_first_date", "aligned_last_date"), "SOURCE_PROVENANCE_IDENTITY")
    _same_fields(selected_source, provenance,
                 ("series_key", "status", "native_unit", "sha256", "bytes",
                  "aligned_observations", "aligned_first_date", "aligned_last_date",
                  "missing_required_dates", "spliced", "imputed"), "SELECTION_SOURCE_IDENTITY")
    _require(provenance["status"] == "ELIGIBLE" and provenance["native_unit"] == "USD millions"
             and provenance["missing_required_dates"] == 0
             and provenance["spliced"] is False and provenance["imputed"] is False,
             "INELIGIBLE_SOURCE")

    public_path = _path(root, entry["public_cell_path"])
    public_hash = _pin(public_path, entry["public_cell_sha256"])
    public = _json(public_path)
    _same_fields(public, entry, ("series_key", "horizon", "window"), "PUBLIC_CELL_IDENTITY")
    _require(public["native_unit"] == "USD millions"
             and public["post_result"] is True and public["exploratory"] is True,
             "PUBLIC_SCOPE_OR_UNIT_IDENTITY")
    _require(public["source_sha256"] == source_hash == entry["public_cell_source_sha256"],
             "PUBLIC_SOURCE_BINDING")
    _require(public["selection_manifest_sha256"] == selection_hash
             == entry["public_cell_selection_manifest_sha256"], "PUBLIC_SELECTION_BINDING")
    _require(public["validation_origins"] == val_bounds and public["evaluation_origins"] == bounds,
             "PUBLIC_GRID_IDENTITY")
    records = {name: _one(public["records"], lambda row: row["method"] == name,
                           "PUBLIC_METHOD_MISSING_OR_DUPLICATE:" + name)
               for name in ("frozen_F", "QR33")}
    _require(not any(row["method"] == "KNN" for row in public["records"]), "UNEXPECTED_PANEL_KNN")
    _require(all(row["status"] == "COMPLETE" for row in records.values()), "PUBLIC_METHOD_INCOMPLETE")
    _require(records["frozen_F"]["selected_penalty"] is None, "F_METHOD_IDENTITY")
    qr = records["QR33"]
    choice = select_parameter(qr["candidates"], spec["qr_penalties"],
                              expected_count=val_bounds[1] - val_bounds[0] + 1)
    _require(choice == qr["selection"] and choice["status"] == "SELECTED"
             and qr["selected_penalty"] == choice["parameter"], "QR_SELECTION_IDENTITY")
    expected_refits = range(bounds[0], bounds[1] + 1, cfg["refit_step"])
    diagnostics = qr["fit_diagnostics"]
    _require(len(diagnostics) == len(expected_refits), "QR_REFIT_COUNT_IDENTITY")
    for detail, refit in zip(diagnostics, expected_refits):
        expected = dict(refit_index=refit, training_first_origin=refit-horizon-window+1,
                        training_last_origin=refit-horizon, training_count=window, latest_label_end=refit)
        _same_fields(detail, expected, tuple(expected), "QR_REFIT_GRID_IDENTITY")

    trace_path = _path(root, entry["path"])
    trace_hash = _pin(trace_path, entry["sha256"], entry["bytes"])
    with np.load(trace_path, allow_pickle=False) as trace:
        _require("KNN" not in trace.files, "UNEXPECTED_PANEL_KNN")
        required = ("origins", "peak", "floor", "frozen_F", "QR33")
        _require(all(name in trace.files for name in required), "MISSING_REQUIRED_ARRAY")
        arrays = {name: np.array(trace[name], copy=True) for name in required}
    origins = arrays["origins"]
    expected_origins = np.arange(bounds[0], bounds[1] + 1, dtype=np.int64)
    _require(origins.ndim == 1 and origins.dtype.kind in "iu"
             and np.array_equal(origins, expected_origins), "COMPLETE_ORIGIN_GRID_IDENTITY")
    for name, values in arrays.items():
        _require(values.shape == expected_origins.shape and values.dtype.kind in "iuf"
                 and np.isfinite(values).all(), "ARRAY_ALIGNMENT_OR_FINITE:" + name)
    _require(np.all(arrays["floor"] >= 0) and np.all(arrays["peak"] >= arrays["floor"])
             and np.all(arrays["frozen_F"] >= arrays["floor"])
             and np.all(arrays["QR33"] >= arrays["floor"]), "PEAK_FLOOR_REPORT_GEOMETRY")
    reproduced = {}
    for name, report in (("frozen_F", arrays["frozen_F"]), ("QR33", arrays["QR33"])):
        summary = summarize_scores(score_predictions(arrays["peak"], report, arrays["floor"], origins))
        _same_fields(records[name], summary, tuple(summary), "ORIGINAL_SUMMARY_IDENTITY:" + name)
        reproduced[name] = summary
    f_loss = reproduced["frozen_F"]["mean_pinball"]
    f_hits = reproduced["frozen_F"]["strict_breach_count"]
    for name, summary in reproduced.items():
        percent = 100 * (summary["mean_pinball"] - f_loss) / f_loss if f_loss else None
        _require(records[name]["percent_vs_frozen_F"] == percent
                 and records[name]["breaches_frozen_F"] == f_hits, "PAIRED_F_SUMMARY_IDENTITY:" + name)

    proof = dict(status="CURRENT_FINGERPRINT_AND_PUBLIC_SUMMARY_IDENTITY", series_key=key,
                 horizon=horizon, window=window, native_unit="USD millions",
                 origin_count=len(origins), first_origin=int(origins[0]), last_origin=int(origins[-1]),
                 private_trace_sha256=trace_hash, private_trace_bytes=entry["bytes"],
                 public_cell_sha256=public_hash, source_sha256=source_hash,
                 provenance_sha256=provenance_hash, selection_manifest_sha256=selection_hash,
                 preexisting_public_trace_digest_present=False,
                 private_hash_scope="CURRENT_ONLY_NOT_PRIOR_PUBLIC_VALIDATION",
                 KNN_available=False, KNN_status="NOT_RUN_NO_SUBSTITUTE")
    for prefix, name in (("F", "frozen_F"), ("QR", "QR33")):
        proof.update({prefix + "_" + k: value for k, value in reproduced[name].items()})
    json.dumps(proof, allow_nan=False)
    return dict(origins=_readonly(origins), peak=_readonly(arrays["peak"]),
                floor=_readonly(arrays["floor"]), F=_readonly(arrays["frozen_F"]),
                QR=_readonly(arrays["QR33"]), KNN=None, available_methods=availability, proof=proof)


def load_panel_cell(entry, *, root):
    """Load a fully admitted cell, or raise DataIdentityError and stop analysis.

    The returned arrays are private inputs. Only ``proof`` is suitable for a
    public receipt: it has scalar fields, fingerprints, and reproduced means/
    counts, with no private paths or per-origin vectors.
    """
    try:
        return _load_panel_cell(entry, Path(root).resolve())
    except DataIdentityError:
        raise
    except (OSError, ValueError, TypeError, KeyError, IndexError, OverflowError, BadZipFile) as error:
        raise DataIdentityError("MALFORMED_OR_MISSING_PANEL_INPUT:" + type(error).__name__) from error
