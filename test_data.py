"""Artificial behavior checks for bounded, pinned source acquisition.

All CSV observations, archives and responses in this file are invented.  No
network is used.  Tests deliberately avoid the real source or frozen hashes.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import http.client
import importlib
import io
import json
import os
from pathlib import Path
import stat
import struct
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
import zipfile


try:
    DATA = importlib.import_module("study_data")
except ModuleNotFoundError as exc:
    if exc.name != "study_data":
        raise
    DATA = None


HEADER = "datetime,NetPosUsd,NetUsdPnL,AbsVolume,Mid\n"
CSV = (HEADER
       + "2015.12.31T23:00:00.000000,-2,unused,unused,unused\n"
       + "2016.01.01T00:00:00.000000,0,unused,unused,unused\n"
       + "2016.01.01T02:00:00.000000,3.5,unused,unused,unused\n").encode()
MEMBER = "invented/inventory.csv"
ENDPOINT = "https://api.kaggle.com/v1/datasets.DatasetApiService/DownloadDataset"
SIGNED_URL = "https://storage.googleapis.com/artificial/inventory.zip?secret=DO_NOT_LOG"


def fixture_spec(raw=CSV, **changes):
    spec = {
        "dataset": "artificial/never-requested", "version": 2,
        "public_url": "https://www.kaggle.com/datasets/artificial/never-requested",
        "requested_member": MEMBER, "accepted_zip_members": [MEMBER],
        "expected_csv_bytes": len(raw),
        "expected_csv_sha256": hashlib.sha256(raw).hexdigest(),
        "expected_rows": 3,
        "expected_header": HEADER.rstrip("\n").split(","),
        "used_fields": ["datetime", "NetPosUsd"],
        "timestamp_format": "%Y.%m.%dT%H:%M:%S.%f",
        "timestamp_timezone": "unspecified_naive",
        "observed_rights_label": "Artificial fixture",
        "raw_redistribution_verified": False,
        "fetch_endpoint": ENDPOINT, "fetch_method": "POST",
        "fetch_request": {"ownerSlug": "artificial", "datasetSlug": "never-requested",
                          "datasetVersionNumber": 2, "fileName": MEMBER},
        "initial_host": "api.kaggle.com",
        "allowed_redirect_hosts": ["storage.googleapis.com"],
        "allowed_https_ports": [443], "max_redirects": 1,
        "allowed_redirect_statuses": [302], "final_status": 200,
        "accepted_final_media_types": ["application/zip"],
        "zip_policy": {"extracted_byte_cap": len(raw)},
    }
    spec.update(changes)
    return spec


def archive(raw=CSV, names=None, *, symlink=False, encrypted=False,
            compression=zipfile.ZIP_DEFLATED):
    sink = io.BytesIO()
    with zipfile.ZipFile(sink, "w", compression=compression) as zf:
        for name in names or [MEMBER]:
            info = zipfile.ZipInfo(name)
            info.compress_type = compression
            if symlink:
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
            zf.writestr(info, raw)
    result = sink.getvalue()
    if encrypted:
        result = bytearray(result)
        local = result.index(b"PK\x03\x04")
        central = result.index(b"PK\x01\x02")
        struct.pack_into("<H", result, local + 6, 1)
        struct.pack_into("<H", result, central + 8, 1)
        result = bytes(result)
    return result


class Response:
    def __init__(self, status, body=b"", headers=None, *, unread=False,
                 virtual_length=None):
        self.status = status
        self.headers = headers or {}
        self._body = io.BytesIO(body)
        self._remaining = virtual_length
        self.unread = unread
        self.read_calls = []
        self.closed = False

    def getcode(self):
        return self.status

    def read(self, size=-1):
        self.read_calls.append(size)
        if self.unread:
            raise AssertionError("Forbidden redirect/error body was read")
        if size < 0:
            raise AssertionError("Unbounded response read")
        if self._remaining is not None:
            count = min(size, self._remaining)
            self._remaining -= count
            return b"x" * count
        return self._body.read(size)

    def close(self):
        self.closed = True


class Transport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.handlers = []

    def build(self, *handlers):
        self.handlers.append(handlers)
        return self

    def open(self, request, timeout=None):
        self.calls.append((request, timeout))
        if not self.responses:
            raise AssertionError("Unexpected extra request")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(DATA, "study_data source validation/acquisition is not implemented")
        scratch = Path(__file__).resolve().parent / ".scratch"
        scratch.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="artificial-source-", dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "fixture.csv"

    def load(self, raw=CSV, spec=None, **kwargs):
        self.path.write_bytes(raw)
        return DATA.load_source(self.path, fixture_spec(raw) if spec is None else spec, **kwargs)

    def assert_source_error(self, operation, code, reason=None):
        with self.assertRaises(DATA.SourceError) as caught:
            operation()
        self.assertEqual(caught.exception.code, code)
        if reason is not None:
            self.assertEqual(caught.exception.reason, reason)
        self.assertNotIn("DO_NOT_LOG", str(caught.exception))
        self.assertNotIn(str(self.path), str(caught.exception))
        self.assertNotIn("DO_NOT_LOG", repr(caught.exception))
        self.assertIsNone(caught.exception.__cause__)
        return caught.exception

    @contextmanager
    def transport(self, responses):
        transport = Transport(responses)
        with patch("urllib.request.build_opener", side_effect=transport.build):
            yield transport

    def acquire(self, responses, spec=None, **kwargs):
        with self.transport(responses) as transport:
            source = DATA.load_source(self.path, spec or fixture_spec(), fetch=True,
                                      remaining_seconds=lambda: 30.0, **kwargs)
        return source, transport

    def successful_responses(self, payload=None):
        payload = archive() if payload is None else payload
        return [Response(302, headers={"Location": SIGNED_URL}, unread=True),
                Response(200, payload, {"Content-Type": "application/zip",
                                        "Content-Length": str(len(payload))})]

    def test_pinned_artificial_values_and_readonly_arrays(self):
        source = self.load()
        self.assertEqual(source.position.tolist(), [-2.0, 0.0, 3.5])
        self.assertEqual(str(source.position.dtype), "float64")
        self.assertEqual(str(source.times.dtype), "datetime64[us]")
        self.assertEqual(str(source.times[2]), "2016-01-01T02:00:00.000000")
        self.assertFalse(source.position.flags.writeable)
        self.assertFalse(source.times.flags.writeable)
        self.assertEqual(source.identity["accepted_csv_bytes"], len(CSV))
        self.assertEqual(source.identity["accepted_csv_sha256"], hashlib.sha256(CSV).hexdigest())
        self.assertTrue(source.identity["source_verified"])
        self.assertEqual(source.identity["acquisition_mode"], "local_reuse")
        self.assertFalse(source.identity["request_performed_this_attempt"])
        self.assertIsNone(source.identity["download"])
        self.assertNotIn(str(self.path), json.dumps(source.identity))

    def test_matching_existing_file_never_builds_transport(self):
        with patch("urllib.request.build_opener", side_effect=AssertionError("network attempted")):
            self.load(fetch=True, remaining_seconds=lambda: 30.0)

    def test_existing_wrong_hash_never_fetches_or_replaces(self):
        self.path.write_bytes(CSV)
        with patch("urllib.request.build_opener", side_effect=AssertionError("network attempted")):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(expected_csv_sha256="0" * 64), fetch=True),
                "SOURCE_IDENTITY_OR_SCHEMA", "CSV_IDENTITY")
        self.assertEqual(self.path.read_bytes(), CSV)

    def test_hash_and_parse_use_same_opened_snapshot(self):
        self.path.write_bytes(CSV)
        seen = []
        def checkpoint(**progress):
            seen.append(progress)
            self.path.write_bytes(b"changed after immutable snapshot")
        source = DATA.load_source(self.path, fixture_spec(), checkpoint=checkpoint)
        self.assertEqual(source.position.tolist(), [-2.0, 0.0, 3.5])
        self.assertTrue(seen)

    def test_local_explicit_symlink_to_regular_file_is_accepted(self):
        target = self.path.with_name("target.csv")
        target.write_bytes(CSV)
        self.path.symlink_to(target)
        source = DATA.load_source(self.path, fixture_spec())
        self.assertEqual(source.position.tolist(), [-2.0, 0.0, 3.5])

    def test_local_nonregular_file_is_rejected(self):
        self.path.mkdir()
        self.assert_source_error(lambda: DATA.load_source(self.path, fixture_spec()),
                                 "SOURCE_IDENTITY_OR_SCHEMA", "LOCAL_NOT_REGULAR")

    def test_missing_local_requires_explicit_fetch(self):
        self.assert_source_error(lambda: DATA.load_source(self.path, fixture_spec()),
                                 "SOURCE_IDENTITY_OR_SCHEMA", "LOCAL_ABSENT")

    def test_size_mismatch_stops(self):
        self.assert_source_error(lambda: self.load(spec=fixture_spec(expected_csv_bytes=len(CSV)-1)),
                                 "SOURCE_IDENTITY_OR_SCHEMA", "CSV_IDENTITY")

    def test_header_width_and_row_count_are_exact(self):
        variants = [CSV.replace(b"NetPosUsd", b"OtherPosx"),
                    CSV.replace(b"-2,unused,unused,unused", b"-2,unused,unused"),
                    CSV + b"2016.01.01T03:00:00.000000,4,a,b,c\n"]
        for raw in variants:
            with self.subTest(raw_length=len(raw)):
                self.assert_source_error(lambda raw=raw: self.load(raw),
                                         "SOURCE_IDENTITY_OR_SCHEMA", "CSV_SCHEMA")

    def test_invalid_duplicate_and_reversed_timestamps_stop_without_sort(self):
        for text in [b"2016.99.01T00:00:00.000000", b"2015.12.31T23:00:00.000000",
                     b"2015.12.31T22:00:00.000000", b"2016-01-01T00:00:00.000000"]:
            raw = CSV.replace(b"2016.01.01T00:00:00.000000", text)
            with self.subTest(timestamp=text):
                self.assert_source_error(lambda raw=raw: self.load(raw),
                                         "SOURCE_IDENTITY_OR_SCHEMA", "CSV_CHRONOLOGY")

    def test_nonfinite_used_positions_stop_but_unused_text_is_allowed(self):
        for value in [b"nan", b"inf", b"-inf", b"1e999", b"bad"]:
            raw = CSV.replace(b",-2,", b"," + value + b",")
            with self.subTest(value=value):
                self.assert_source_error(lambda raw=raw: self.load(raw),
                                         "SOURCE_IDENTITY_OR_SCHEMA", "CSV_POSITION")

    def test_manual_redirect_fetches_exact_anonymous_post_then_clean_get(self):
        responses = self.successful_responses()
        source, transport = self.acquire(responses)
        self.assertEqual(self.path.read_bytes(), CSV)
        self.assertEqual(len(transport.calls), 2)
        first, second = [call[0] for call in transport.calls]
        self.assertEqual(first.full_url, ENDPOINT)
        self.assertEqual(first.get_method(), "POST")
        self.assertEqual(json.loads(first.data), fixture_spec()["fetch_request"])
        self.assertEqual(second.full_url, SIGNED_URL)
        self.assertEqual(second.get_method(), "GET")
        self.assertIsNone(second.data)
        self.assertEqual(second.header_items(), [])
        self.assertTrue(all(0 < call[1] <= 30 for call in transport.calls))
        self.assertEqual(len(transport.handlers), 2)
        for handlers in transport.handlers:
            proxies = [h for h in handlers if isinstance(h, urllib.request.ProxyHandler)]
            redirects = [h for h in handlers if isinstance(h, urllib.request.HTTPRedirectHandler)]
            self.assertEqual(len(proxies), 1)
            self.assertEqual(proxies[0].proxies, {})
            self.assertEqual(len(redirects), 1)
            self.assertIsNone(redirects[0].redirect_request(first, None, 302, "", {}, SIGNED_URL))
        self.assertEqual(responses[0].read_calls, [])
        self.assertTrue(all(response.closed for response in responses))
        self.assertEqual(source.identity["acquisition_mode"], "explicit_fetch")
        self.assertTrue(source.identity["request_performed_this_attempt"])
        download = source.identity["download"]
        self.assertEqual(download["redirect_hosts"], ["storage.googleapis.com"])
        self.assertEqual(download["redirect_statuses"], [302])
        self.assertTrue(download["query_present"])
        self.assertEqual(download["http_status"], 200)
        self.assertEqual(download["archive_bytes"], len(archive()))
        self.assertNotIn("DO_NOT_LOG", json.dumps(source.identity))
        self.assertNotIn("artificial/inventory.zip", json.dumps(source.identity))

    def test_first_http_error_redirect_is_closed_without_read(self):
        body = Response(302, unread=True)
        error = urllib.error.HTTPError(ENDPOINT, 302, "private DO_NOT_LOG",
                                       {"Location": SIGNED_URL}, body)
        source, transport = self.acquire([error, self.successful_responses()[1]])
        self.assertTrue(source.identity["source_verified"])
        self.assertEqual(body.read_calls, [])
        self.assertTrue(body.closed)

    def test_error_http_body_closed_unread_and_exception_sanitized(self):
        body = Response(403, unread=True)
        error = urllib.error.HTTPError(SIGNED_URL, 403, "private DO_NOT_LOG", {}, body)
        with self.transport([error]):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "HTTP_STATUS")
        self.assertEqual(body.read_calls, [])
        self.assertTrue(body.closed)
        self.assertFalse(self.path.exists())

    def test_second_redirect_stops_and_closes_body_unread(self):
        second = Response(302, headers={"Location": SIGNED_URL}, unread=True)
        with self.transport([self.successful_responses()[0], second]) as transport:
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "HTTP_STATUS")
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(second.read_calls, [])
        self.assertTrue(second.closed)

    def test_broken_http_framing_is_sanitized_without_acceptance(self):
        for phase in ("status_line", "chunked_read"):
            with self.subTest(phase=phase):
                final = Response(200, headers={"Content-Type": "application/zip"})
                def incomplete_read(size):
                    raise http.client.IncompleteRead(b"DO_NOT_LOG")
                final.read = incomplete_read
                responses = ([http.client.BadStatusLine("DO_NOT_LOG")]
                             if phase == "status_line"
                             else [self.successful_responses()[0], final])
                with self.transport(responses):
                    self.assert_source_error(lambda: DATA.load_source(
                        self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                        "SOURCE_FETCH_OR_ARCHIVE", "HTTP_TRANSPORT")
                if phase == "chunked_read":
                    self.assertTrue(final.closed)
                self.assertFalse(self.path.exists())

    def test_disallowed_redirects_stop_before_get(self):
        bad_urls = ["http://storage.googleapis.com/a", "https://evil.invalid/a",
                    "https://storage.googleapis.com.evil.invalid/a",
                    "https://storage.googleapis.com:444/a", "https://user@storage.googleapis.com/a",
                    "https://storage.googleapis.com/a#fragment", "/relative", "https://storage.googleapis.com./a"]
        for url in bad_urls:
            response = Response(302, headers={"Location": url}, unread=True)
            with self.subTest(url=url), self.transport([response]) as transport:
                self.assert_source_error(lambda: DATA.load_source(
                    self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                    "SOURCE_FETCH_OR_ARCHIVE", "REDIRECT_URL")
                self.assertEqual(len(transport.calls), 1)
                self.assertEqual(response.read_calls, [])
                self.assertTrue(response.closed)

    def test_changed_initial_endpoint_stops_before_request(self):
        spec = fixture_spec(fetch_endpoint="https://evil.invalid/DO_NOT_LOG")
        with patch("urllib.request.build_opener", side_effect=AssertionError("network attempted")):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, spec, fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "FETCH_CONFIGURATION")

    def test_nonzip_final_media_is_rejected_without_read(self):
        final = Response(200, headers={"Content-Type": "text/html"}, unread=True)
        with self.transport([self.successful_responses()[0], final]):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "HTTP_MEDIA_TYPE")
        self.assertEqual(final.read_calls, [])
        self.assertTrue(final.closed)

    def test_declared_oversize_is_rejected_without_read(self):
        final = Response(200, headers={"Content-Type": "application/zip",
                                      "Content-Length": str(25*1024*1024+1)}, unread=True)
        with self.transport([self.successful_responses()[0], final]):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "DOWNLOAD_SIZE")
        self.assertEqual(final.read_calls, [])
        self.assertTrue(final.closed)

    def test_unknown_length_stream_is_bounded(self):
        final = Response(200, headers={"Content-Type": "application/zip"},
                         virtual_length=25*1024*1024+1000)
        progress = []
        with self.transport([self.successful_responses()[0], final]):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30,
                checkpoint=lambda **kw: progress.append(kw)),
                "SOURCE_FETCH_OR_ARCHIVE", "DOWNLOAD_SIZE")
        self.assertTrue(final.closed)
        self.assertLessEqual(25*1024*1024+1000-final._remaining, 25*1024*1024+1)
        self.assertTrue(progress)
        self.assertFalse(self.path.exists())

    def test_missing_global_budget_and_exhausted_global_budget_stop(self):
        with patch("urllib.request.build_opener", side_effect=AssertionError("network attempted")):
            self.assert_source_error(lambda: DATA.load_source(self.path, fixture_spec(), fetch=True),
                                     "SOURCE_FETCH_OR_ARCHIVE", "FETCH_BUDGET")
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 0),
                "SOURCE_FETCH_OR_ARCHIVE", "FETCH_BUDGET")

    def test_deadline_rechecked_during_stream(self):
        final = Response(200, archive(), {"Content-Type": "application/zip"})
        state = {"expired": False}
        def checkpoint(**kw):
            if kw.get("stage") == "source_download":
                state["expired"] = True
        with self.transport([self.successful_responses()[0], final]):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True,
                remaining_seconds=lambda: 0 if state["expired"] else 30,
                checkpoint=checkpoint), "SOURCE_FETCH_OR_ARCHIVE", "FETCH_BUDGET")
        self.assertTrue(final.closed)
        self.assertFalse(self.path.exists())

    def test_archive_member_policy_rejects_wrong_extra_traversal_symlink_encryption(self):
        variants = [archive(names=["wrong.csv"]), archive(names=[MEMBER, "extra.csv"]),
                    archive(names=["../inventory.csv"]), archive(names=["/inventory.csv"]),
                    archive(symlink=True), archive(encrypted=True),
                    archive(compression=zipfile.ZIP_BZIP2)]
        for payload in variants:
            with self.subTest(payload_size=len(payload)), self.transport(self.successful_responses(payload)):
                self.assert_source_error(lambda: DATA.load_source(
                    self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                    "SOURCE_FETCH_OR_ARCHIVE", "ZIP_POLICY")
                self.assertFalse(self.path.exists())

    def test_archive_preinflate_size_and_raw_hash_must_match(self):
        for payload, spec in [(archive(CSV + b"x"), fixture_spec()),
                              (archive(CSV.replace(b",-2,", b",-1,")), fixture_spec())]:
            with self.subTest(payload_size=len(payload)), self.transport(self.successful_responses(payload)):
                self.assert_source_error(lambda: DATA.load_source(
                    self.path, spec, fetch=True, remaining_seconds=lambda: 30),
                    "SOURCE_FETCH_OR_ARCHIVE")
                self.assertFalse(self.path.exists())

    def test_corrupt_crc_is_rejected_before_cache_acceptance(self):
        payload = bytearray(archive(compression=zipfile.ZIP_STORED))
        local = payload.index(b"PK\x03\x04")
        name_length, extra_length = struct.unpack_from("<HH", payload, local + 26)
        payload[local + 30 + name_length + extra_length + len(HEADER)] ^= 1
        with self.transport(self.successful_responses(bytes(payload))):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "ZIP_INTEGRITY")
        self.assertFalse(self.path.exists())

    def test_malformed_deflate_is_sanitized_before_cache_acceptance(self):
        payload = bytearray(archive())
        local = payload.index(b"PK\x03\x04")
        name_length, extra_length = struct.unpack_from("<HH", payload, local + 26)
        compressed_start = local + 30 + name_length + extra_length
        # DEFLATE block type 3 is reserved, independently of the input CSV.
        payload[compressed_start] = (payload[compressed_start] & 0xF8) | 0x07
        with self.transport(self.successful_responses(bytes(payload))):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "ZIP_INTEGRITY")
        self.assertFalse(self.path.exists())

    def test_racing_existing_destination_is_preserved_without_overwrite(self):
        responses = self.successful_responses()
        original_read = responses[1].read
        def racing_read(size):
            self.path.write_bytes(b"another writer owns this file")
            return original_read(size)
        responses[1].read = racing_read
        with self.transport(responses):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_FETCH_OR_ARCHIVE", "CACHE_ACCEPT")
        self.assertEqual(self.path.read_bytes(), b"another writer owns this file")

    def test_dangling_output_symlink_is_not_populated(self):
        target = self.path.with_name("missing-target.csv")
        self.path.symlink_to(target)
        with patch("urllib.request.build_opener", side_effect=AssertionError("network attempted")):
            self.assert_source_error(lambda: DATA.load_source(
                self.path, fixture_spec(), fetch=True, remaining_seconds=lambda: 30),
                "SOURCE_IDENTITY_OR_SCHEMA", "LOCAL_ABSENT")
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
