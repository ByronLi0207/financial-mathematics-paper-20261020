"""Artificial file fixtures only; never open an archived financial NPZ."""
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, allow_nan=False))


class PanelAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("v6_panel_admission"),
                             "panel admission API is not implemented")
        self.api = importlib.import_module("v6_panel_admission")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self._fixture()

    def _fixture(self):
        self.origins = np.arange(405, 682, dtype=np.int64)
        self.arrays = dict(origins=self.origins, peak=np.full(277, 3.),
                           floor=np.ones(277), frozen_F=np.full(277, 4.),
                           QR33=np.full(277, 2.), C2_QR4=np.full(277, 99.))
        self.source_path = self.root / ".scratch/synthetic.csv"
        self.source_path.parent.mkdir(parents=True)
        self.source_path.write_bytes(b"synthetic source fingerprint only\n")
        source_hash = _digest(self.source_path)
        self.provenance = dict(series_key="SYNTHETIC", status="ELIGIBLE",
                               native_unit="USD millions", sha256=source_hash,
                               bytes=self.source_path.stat().st_size,
                               aligned_observations=706, aligned_first_date="2013-04-03",
                               aligned_last_date="2026-10-07", missing_required_dates=0,
                               imputed=False, spliced=False)
        self.provenance_path = self.root / "public/provenance.json"
        _write_json(self.provenance_path, self.provenance)
        self.selection = dict(status="SELECTION_FROZEN_BEFORE_MODELS",
                              eligible=["SYNTHETIC"], series=[deepcopy(self.provenance)])
        self.selection_path = self.root / "public/selection.json"
        _write_json(self.selection_path, self.selection)
        self.spec = dict(horizons=[6, 24], qr_penalties=[.001, .01, .1], sources={
            "nyfed_weekly": dict(windows=[52, 260], refit_step=13,
                                 validation_origin_first=329, validation_origin_last=380,
                                 evaluation_origin_first=405, evaluation_origin_last=681)})
        _write_json(self.root / "protocol/revision-20261022/study-spec.json", self.spec)
        # Literal known answers: F overreports by 1, QR underreports by 1.
        f = dict(method="frozen_F", status="COMPLETE", selected_penalty=None,
                 origin_count=277, mean_pinball=.05, mean_capacity=4., mean_extra_allowance=3.,
                 strict_breach_count=0, strict_breach_rate=0., mean_positive_overrun=0.,
                 conditional_mean_overrun=None, conditional_overrun_denominator=0,
                 conditional_overrun_undefined_reason="NO_STRICT_BREACHES", mean_unused_allowance=1.,
                 percent_vs_frozen_F=0., breaches_frozen_F=0)
        qr = dict(method="QR33", status="COMPLETE", selected_penalty=.1,
                  origin_count=277, mean_pinball=.95, mean_capacity=2., mean_extra_allowance=1.,
                  strict_breach_count=277, strict_breach_rate=1., mean_positive_overrun=1.,
                  conditional_mean_overrun=1., conditional_overrun_denominator=277,
                  conditional_overrun_undefined_reason=None, mean_unused_allowance=0.,
                  percent_vs_frozen_F=1799.9999999999995, breaches_frozen_F=0,
                  selection=dict(status="SELECTED", parameter=.1, mean_validation_pinball=.8),
                  candidates=[dict(parameter=p, status="COMPLETE", origin_count=52, mean_pinball=v)
                              for p, v in [(.001, 2.), (.01, 1.5), (.1, .8)]],
                  fit_diagnostics=[dict(refit_index=r, training_first_origin=r-6-52+1,
                                        training_last_origin=r-6, training_count=52, latest_label_end=r)
                                   for r in range(405, 682, 13)])
        self.public = dict(series_key="SYNTHETIC", horizon=6, window=52, post_result=True,
                           exploratory=True, native_unit="USD millions", source_sha256=source_hash,
                           selection_manifest_sha256=_digest(self.selection_path),
                           validation_origins=[329, 380], evaluation_origins=[405, 681],
                           records=[f, qr])
        self.public_path = self.root / "public/cell.json"
        _write_json(self.public_path, self.public)
        self.trace_path = self.root / ".scratch/synthetic.npz"
        np.savez(self.trace_path, **self.arrays)
        self.entry = dict(path=".scratch/synthetic.npz", exists=True,
                          bytes=self.trace_path.stat().st_size, sha256=_digest(self.trace_path),
                          series_key="SYNTHETIC", horizon=6, window=52,
                          public_cell_path="public/cell.json", public_cell_exists=True,
                          public_cell_sha256=_digest(self.public_path),
                          public_cell_source_sha256=source_hash,
                          public_cell_selection_manifest_sha256=_digest(self.selection_path),
                          public_cell_source_matches_provenance=True,
                          public_cell_selection_binding_matches_current_selection=True,
                          public_validation_origin_bounds=[329, 380], public_evaluation_origin_bounds=[405, 681],
                          preexisting_public_trace_digest_present=False,
                          required_methods={"F": "frozen_F", "QR": "QR33", "KNN": "KNN"},
                          method_availability={"F": True, "QR": True, "KNN": False})
        self.inventory = dict(panel_cells=[self.entry],
            panel_selection=dict(path="public/selection.json", sha256=_digest(self.selection_path),
                                 eligible=["SYNTHETIC"]),
            panel_source_inputs=[dict(series_key="SYNTHETIC", path=".scratch/synthetic.csv",
                exists=True, bytes=self.source_path.stat().st_size, sha256=source_hash,
                expected_sha256=source_hash, source_fingerprint_match=True,
                provenance_path="public/provenance.json", provenance_sha256=_digest(self.provenance_path),
                aligned_observations=706, aligned_first_date="2013-04-03", aligned_last_date="2026-10-07")])
        self._inventory()

    def _inventory(self):
        _write_json(self.root / ".scratch/revision-v6/input-inventory.json", self.inventory)

    def _repin_public(self):
        _write_json(self.public_path, self.public)
        self.entry["public_cell_sha256"] = _digest(self.public_path)
        self._inventory()

    def _repin_trace(self):
        np.savez(self.trace_path, **self.arrays)
        self.entry.update(bytes=self.trace_path.stat().st_size, sha256=_digest(self.trace_path))
        self._inventory()

    def _load(self):
        return self.api.load_panel_cell(deepcopy(self.entry), root=self.root)

    def test_valid_cell_reproduces_both_scalar_summaries_and_knn_is_absent(self):
        # Catches swapped F/QR, loss weight drift and substituting C2 for KNN.
        z = self._load()
        np.testing.assert_array_equal(z["origins"], self.origins)
        np.testing.assert_array_equal(z["F"], np.full(277, 4.))
        np.testing.assert_array_equal(z["QR"], np.full(277, 2.))
        self.assertIsNone(z["KNN"])
        self.assertEqual(z["available_methods"], {"F": True, "QR": True, "KNN": False})
        self.assertEqual(z["proof"]["F_mean_pinball"], .05)
        self.assertEqual(z["proof"]["QR_strict_breach_count"], 277)
        self.assertFalse(z["proof"]["preexisting_public_trace_digest_present"])
        self.assertTrue(all(value is None or isinstance(value, (str, bool, int, float))
                            for value in z["proof"].values()))
        self.assertNotIn(".scratch", json.dumps(z["proof"], allow_nan=False))
        self.assertNotIn("path", " ".join(z["proof"]))

    def test_every_original_mean_hit_and_count_scalar_is_exactly_checked(self):
        # Every scalar mismatch must stop admission, even after current hashes are pinned.
        keys = ["origin_count", "mean_pinball", "mean_capacity", "mean_extra_allowance",
                "strict_breach_count", "strict_breach_rate", "mean_positive_overrun",
                "conditional_mean_overrun", "conditional_overrun_denominator",
                "conditional_overrun_undefined_reason", "mean_unused_allowance",
                "percent_vs_frozen_F", "breaches_frozen_F"]
        baseline = deepcopy(self.public)
        for method in range(2):
            for key in keys:
                with self.subTest(method=method, key=key):
                    self.public = deepcopy(baseline)
                    value = self.public["records"][method][key]
                    self.public["records"][method][key] = ("WRONG" if value is None or isinstance(value, str)
                                                          else value + 1)
                    self._repin_public()
                    with self.assertRaises(self.api.DataIdentityError):
                        self._load()

    def test_trace_digest_and_size_change_are_identity_errors(self):
        # Catches loading a changed NPZ merely because its arrays still look plausible.
        self.trace_path.write_bytes(self.trace_path.read_bytes() + b"changed")
        with self.assertRaises(self.api.DataIdentityError):
            self._load()

    def test_invalid_pinned_archive_is_a_data_identity_error(self):
        # Catches leaking a raw ZIP parser failure instead of stopping admission.
        self.trace_path.write_bytes(b"PK\x03\x04not-a-valid-archive")
        self.entry.update(bytes=self.trace_path.stat().st_size, sha256=_digest(self.trace_path))
        self._inventory()
        with self.assertRaises(Exception) as caught:
            self._load()
        self.assertIsInstance(caught.exception, self.api.DataIdentityError)

    def test_public_digest_change_is_identity_error(self):
        self.public_path.write_text(self.public_path.read_text() + " ")
        with self.assertRaises(self.api.DataIdentityError):
            self._load()

    def test_source_and_provenance_and_selection_hashes_are_rechecked(self):
        # Catches trusting stale metadata flags rather than each current owning file.
        for name in ("source_path", "provenance_path", "selection_path"):
            with self.subTest(name=name):
                path = getattr(self, name)
                original = path.read_bytes()
                path.write_bytes(original + b" ")
                with self.assertRaises(self.api.DataIdentityError):
                    self._load()
                path.write_bytes(original)

    def test_rehashed_wrong_bindings_or_units_or_status_cannot_be_admitted(self):
        baseline = deepcopy(self.public)
        mutations = [("source_sha256", "0" * 64), ("selection_manifest_sha256", "0" * 64),
                     ("series_key", "ANOTHER"), ("horizon", 24), ("window", 260),
                     ("native_unit", "USD"), ("evaluation_origins", [406, 682]),
                     ("validation_origins", [330, 381]), ("post_result", False)]
        for key, value in mutations:
            with self.subTest(key=key):
                self.public = deepcopy(baseline)
                self.public[key] = value
                self._repin_public()
                with self.assertRaises(self.api.DataIdentityError):
                    self._load()

    def test_grid_interior_dtype_geometry_and_nonfinite_arrays_are_checked(self):
        baseline = {k: v.copy() for k, v in self.arrays.items()}
        for mutation in ("interior", "float_origins", "nonfinite", "negative_floor", "peak_floor", "F_floor", "QR_floor", "short", "missing_F"):
            with self.subTest(mutation=mutation):
                self.arrays = {k: v.copy() for k, v in baseline.items()}
                if mutation == "interior": self.arrays["origins"][10] += 1
                elif mutation == "float_origins": self.arrays["origins"] = self.origins.astype(float)
                elif mutation == "nonfinite": self.arrays["QR33"][3] = np.nan
                elif mutation == "negative_floor": self.arrays["floor"][3] = -1
                elif mutation == "peak_floor": self.arrays["peak"][3] = 0
                elif mutation == "F_floor": self.arrays["frozen_F"][3] = 0
                elif mutation == "QR_floor": self.arrays["QR33"][3] = 0
                elif mutation == "short": self.arrays["QR33"] = self.arrays["QR33"][:-1]
                else: del self.arrays["frozen_F"]
                self._repin_trace()
                with self.assertRaises(self.api.DataIdentityError):
                    self._load()

    def test_complete_selected_qr_and_original_refit_grid_are_required(self):
        baseline = deepcopy(self.public)
        for mutation in ("status", "selected", "candidate", "refit"):
            with self.subTest(mutation=mutation):
                self.public = deepcopy(baseline)
                qr = self.public["records"][1]
                if mutation == "status": qr["status"] = "FAILED"
                elif mutation == "selected": qr["selected_penalty"] = .01
                elif mutation == "candidate": qr["candidates"][0]["mean_pinball"] = .1
                else: qr["fit_diagnostics"][1]["refit_index"] += 1
                self._repin_public()
                with self.assertRaises(self.api.DataIdentityError):
                    self._load()

    def test_supplied_entry_and_method_inventory_cannot_be_rewritten(self):
        foreign = deepcopy(self.entry)
        foreign["sha256"] = "0" * 64
        with self.assertRaises(self.api.DataIdentityError):
            self.api.load_panel_cell(foreign, root=self.root)
        self.entry["required_methods"]["QR"] = "C2_QR4"
        self._inventory()
        with self.assertRaises(self.api.DataIdentityError):
            self._load()

    def test_false_admission_flag_and_unexpected_knn_stop_without_substitution(self):
        self.entry["public_cell_source_matches_provenance"] = False
        self._inventory()
        with self.assertRaises(self.api.DataIdentityError): self._load()
        self.entry["public_cell_source_matches_provenance"] = True
        self.arrays["KNN"] = np.ones(277)
        self._repin_trace()
        with self.assertRaises(self.api.DataIdentityError): self._load()


if __name__ == "__main__":
    unittest.main(verbosity=2)
