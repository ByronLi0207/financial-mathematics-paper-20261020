"""Pinned local-source contracts, using invented CSV bytes only.

No real source is opened and no network is requested.  Each fixture is written
to a fresh temporary directory; expected values are hand-specified.
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import importlib
from pathlib import Path
import tempfile
import unittest

import numpy as np


try:
    SOURCES = importlib.import_module("conditional_sources")
except ModuleNotFoundError as exc:
    if exc.name != "conditional_sources":
        raise
    SOURCES = None


FX_HEADER = b"datetime,NetPosUsd,NetUsdPnL,AbsVolume,Mid\n"
FX = (FX_HEADER
      + b"2020.01.03T22:00:00.000000,-4,unused,unused,unused\n"
      + b"2020.01.03T23:00:00.000001,0,unused,unused,unused\n"
      + b"2020.01.06T00:00:00.000001,7.5,unused,unused,unused\n")
NY_HEADER = b'"As Of Date","Time Series","Value (millions)"\n'
NY = (NY_HEADER
      + b'"2020-01-01","PDPOSGS-B","-3"\n'
      + b'"2020-01-08","PDPOSGS-B","0"\n'
      + b'"2020-01-22","PDPOSGS-B","2.25"\n')


class SourceFixture(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SOURCES, "conditional_sources implementation is missing")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "invented.csv"

    def load(self, raw, source_id, **overrides):
        self.path.write_bytes(raw)
        identity = {"expected_sha256": hashlib.sha256(raw).hexdigest(),
                    "expected_bytes": len(raw)}
        identity.update(overrides)
        return SOURCES.load_source(self.path, source_id, **identity)

    def reject(self, raw, source_id, **overrides):
        try:
            self.load(raw, source_id, **overrides)
        except Exception as exc:
            self.assertIsInstance(exc, ValueError)
            self.assertRegex(str(exc), r"^SOURCE_[A-Z_]+$")
            self.assertNotIn(str(self.path), str(exc))
            return exc
        self.fail("invalid invented source was accepted")


class TestPinnedSources(SourceFixture):
    def test_fx_preserves_signed_values_microseconds_and_row_order(self):
        source = self.load(FX, "fx_hourly")
        self.assertEqual(source.source_id, "fx_hourly")
        np.testing.assert_array_equal(source.position, [-4.0, 0.0, 7.5])
        np.testing.assert_array_equal(source.dates, np.array([
            "2020-01-03T22:00:00.000000", "2020-01-03T23:00:00.000001",
            "2020-01-06T00:00:00.000001"], dtype="datetime64[us]"))
        self.assertEqual(source.position.dtype, np.dtype("float64"))
        self.assertEqual(source.dates.dtype, np.dtype("datetime64[us]"))
        self.assertEqual(source.sha256, hashlib.sha256(FX).hexdigest())
        self.assertEqual(source.bytes, len(FX))
        self.assertEqual(source.metadata["units"], "USD")

    def test_nyfed_preserves_native_millions_and_economic_date_gaps(self):
        source = self.load(NY, "nyfed_weekly")
        self.assertEqual(source.source_id, "nyfed_weekly")
        np.testing.assert_array_equal(source.position, [-3.0, 0.0, 2.25])
        np.testing.assert_array_equal(source.dates, np.array([
            "2020-01-01", "2020-01-08", "2020-01-22"], dtype="datetime64[us]"))
        self.assertEqual(source.metadata["units"], "USD millions")
        self.assertEqual(source.metadata["observation_count"], 3)
        self.assertEqual(source.metadata["nominal_interval_seconds"], 604800)
        self.assertEqual(source.metadata["gap_seconds_unique"], [604800.0, 1209600.0])
        self.assertEqual(source.metadata["gap_counts"], [1, 1])
        self.assertEqual(source.metadata["irregular_gap_count"], 1)

    def test_returned_arrays_cannot_be_modified_or_made_writable(self):
        source = self.load(NY, "nyfed_weekly")
        for array in [source.dates, source.position]:
            with self.subTest(dtype=str(array.dtype)):
                self.assertFalse(array.flags.writeable)
                with self.assertRaises(ValueError):
                    array[0] = array[-1]
                with self.assertRaises(ValueError):
                    array.setflags(write=True)

    def test_source_identity_fields_are_frozen_and_repr_omits_values(self):
        source = self.load(NY, "nyfed_weekly")
        with self.assertRaises(FrozenInstanceError):
            source.source_id = "fx_hourly"
        self.assertNotIn("2.25", repr(source))
        self.assertNotIn(str(self.path), repr(source))

    def test_metadata_contains_only_json_safe_nonfinancial_scalars_and_lists(self):
        source = self.load(FX, "fx_hourly")
        for value in source.metadata.values():
            items = value if isinstance(value, list) else [value]
            for item in items:
                self.assertIn(type(item), [str, int, float, bool, type(None)])
        self.assertEqual(source.metadata["observation_count"], 3)
        self.assertNotIn("position", source.metadata)
        self.assertNotIn("values", source.metadata)
        self.assertNotIn(str(self.path), str(source.metadata))

    def test_pinned_hash_rejects_same_size_source_modification(self):
        changed = NY.replace(b'"-3"', b'"-4"')
        self.assertEqual(len(changed), len(NY))
        self.reject(changed, "nyfed_weekly", expected_sha256=hashlib.sha256(NY).hexdigest())

    def test_pinned_byte_count_rejects_source_size_change(self):
        self.reject(NY, "nyfed_weekly", expected_bytes=len(NY) + 1)

    def test_identity_is_verified_before_decoding_financial_tokens(self):
        invalid_utf8 = NY.replace(b'"-3"', b'"\xff"')
        exc = self.reject(invalid_utf8, "nyfed_weekly", expected_sha256="0" * 64)
        self.assertEqual(getattr(exc, "reason", None), "SOURCE_HASH")

    def test_bad_digest_configuration_is_rejected(self):
        for digest in [None, 42, "", "a" * 63, "a" * 65, "Z" * 64, "A" * 64]:
            with self.subTest(digest=digest):
                self.reject(NY, "nyfed_weekly", expected_sha256=digest)

    def test_bad_size_configuration_is_rejected_before_reading(self):
        for size in [None, True, 1.5, "100", 0, -1, 100 * 1024 * 1024 + 1]:
            with self.subTest(size=size):
                self.reject(NY, "nyfed_weekly", expected_bytes=size)

    def test_unknown_source_is_rejected_before_opening_path(self):
        for source_id in ["fx", "NYFED", "", None, ["nyfed_weekly"]]:
            with self.subTest(source_id=source_id):
                try:
                    SOURCES.load_source(self.path, source_id,
                                        expected_sha256=hashlib.sha256(NY).hexdigest(),
                                        expected_bytes=len(NY))
                except Exception as exc:
                    self.assertIsInstance(exc, ValueError)
                    self.assertEqual(getattr(exc, "reason", None), "SOURCE_CONFIGURATION")
                else:
                    self.fail("unknown source was accepted")

    def test_exact_schema_rejects_reordered_extra_missing_or_bom_headers(self):
        invalid = [
            (FX.replace(FX_HEADER, b"NetPosUsd,datetime,NetUsdPnL,AbsVolume,Mid\n"), "fx_hourly"),
            (FX.replace(b"NetPosUsd", b"other"), "fx_hourly"),
            (NY.replace(b"Value (millions)", b"Value"), "nyfed_weekly"),
            (NY.replace(b"Time Series", b"Time Series "), "nyfed_weekly"),
            (b"\xef\xbb\xbf" + NY, "nyfed_weekly"),
            (NY_HEADER.replace(b"\n", b',"extra"\n') + NY[len(NY_HEADER):], "nyfed_weekly"),
        ]
        for raw, source_id in invalid:
            with self.subTest(source_id=source_id, header=raw.splitlines()[0]):
                self.reject(raw, source_id)

    def test_nyfed_requires_exact_series_key_on_every_record(self):
        for wrong in [b"PDPOSGS-X", b"pdposgs-b", b"", b"PDPOSGS-B "]:
            with self.subTest(key=wrong):
                raw = NY.replace(b"PDPOSGS-B", wrong, 1)
                self.reject(raw, "nyfed_weekly")

    def test_duplicate_dates_are_not_dropped(self):
        self.reject(NY.replace(b"2020-01-08", b"2020-01-01"), "nyfed_weekly")
        self.reject(FX.replace(b"2020.01.03T23:00:00.000001", b"2020.01.03T22:00:00.000000"), "fx_hourly")

    def test_out_of_order_dates_are_not_sorted(self):
        self.reject(NY.replace(b"2020-01-08", b"2019-12-31"), "nyfed_weekly")
        self.reject(FX.replace(b"2020.01.03T23:00:00.000001", b"2020.01.02T23:00:00.000001"), "fx_hourly")

    def test_nyfed_dates_must_be_unambiguous_iso_dates(self):
        for token in [b"2020-1-01", b"20200101", b"2020-02-30", b"2020-01-01T00:00:00",
                      b" 2020-01-01", b"2020-01-01Z", b"", b"NaT"]:
            with self.subTest(token=token):
                self.reject(NY.replace(b"2020-01-01", token, 1), "nyfed_weekly")

    def test_fx_preserves_accepted_strptime_format_and_rejects_timezone_or_bad_dates(self):
        for token in [b"2020-01-03T22:00:00.000000", b"2020.02.30T22:00:00.000000",
                      b"2020.01.03T22:00:00.000000Z", b"2020.01.03T22:00:00",
                      b"2020.01.03T22:00:00.0000001", b"NaT"]:
            with self.subTest(token=token):
                self.reject(FX.replace(b"2020.01.03T22:00:00.000000", token, 1), "fx_hourly")

    def test_missing_suppressed_malformed_and_nonfinite_values_are_rejected(self):
        for token in [b"", b" ", b"NA", b"N/A", b"null", b"--", b".", b"NaN", b"nan",
                      b"inf", b"+Infinity", b"-inf", b"1e999", b"-1e999", b"1,200",
                      b"1_000", "１２".encode()]:
            for raw, source_id in [
                (NY.replace(b'"-3"', b'"' + token + b'"', 1), "nyfed_weekly"),
                (FX.replace(b",-4,", b"," + token + b",", 1), "fx_hourly"),
            ]:
                with self.subTest(token=token, source_id=source_id):
                    self.reject(raw, source_id)

    def test_finite_scientific_notation_is_preserved_without_unit_conversion(self):
        source = self.load(NY.replace(b'"-3"', b'"-3e2"', 1), "nyfed_weekly")
        np.testing.assert_array_equal(source.position, [-300.0, 0.0, 2.25])

    def test_bad_row_width_or_blank_observations_are_not_deleted(self):
        for raw, source_id in [
            (NY.replace(b',"-3"', b"", 1), "nyfed_weekly"),
            (NY.replace(b',"-3"', b',"-3","extra"', 1), "nyfed_weekly"),
            (FX.replace(b",unused,unused,unused", b",unused,unused", 1), "fx_hourly"),
            (FX.replace(b",unused,unused,unused", b",unused,unused,unused,extra", 1), "fx_hourly"),
            (NY + b"\n", "nyfed_weekly"),
            (FX + b"\n", "fx_hourly"),
        ]:
            with self.subTest(source_id=source_id, row_width=len(raw)):
                self.reject(raw, source_id)

    def test_header_only_empty_invalid_utf8_and_malformed_csv_are_safe_failures(self):
        for raw, source_id in [(b"", "fx_hourly"), (FX_HEADER, "fx_hourly"),
                               (NY_HEADER, "nyfed_weekly"), (NY + b"\xff", "nyfed_weekly"),
                               (NY_HEADER + b'"2020-01-01,PDPOSGS-B,3\n', "nyfed_weekly")]:
            with self.subTest(source_id=source_id, byte_count=len(raw)):
                self.reject(raw, source_id)

    def test_single_observation_has_empty_gap_metadata(self):
        source = self.load(NY_HEADER + b'"2020-01-01","PDPOSGS-B","-3"\n', "nyfed_weekly")
        self.assertEqual(source.metadata["gap_seconds_unique"], [])
        self.assertEqual(source.metadata["gap_counts"], [])
        self.assertEqual(source.metadata["irregular_gap_count"], 0)

    def test_missing_or_nonregular_input_is_a_safe_failure(self):
        for path in [self.path, self.path.parent]:
            with self.subTest(kind="missing" if path == self.path else "directory"):
                try:
                    SOURCES.load_source(path, "nyfed_weekly", expected_sha256="0" * 64, expected_bytes=100)
                except Exception as exc:
                    self.assertIsInstance(exc, ValueError)
                    self.assertRegex(str(exc), r"^SOURCE_[A-Z_]+$")
                    self.assertNotIn(str(path), str(exc))
                else:
                    self.fail("invalid local file was accepted")


if __name__ == "__main__":
    unittest.main()
