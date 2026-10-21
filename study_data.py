"""Pinned CSV validation and bounded anonymous single-archive acquisition.

The caller owns production configuration and the global wall budget.  This
module never inspects other source files, repairs an existing cache, or exposes
input paths, rejected digests, response bodies, or transient signed URLs.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import http.client
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import tempfile
from typing import Callable
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import zlib

import numpy as np


_MAX_RAW_BYTES = 100 * 1024 * 1024
_MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
_CHUNK_BYTES = 64 * 1024
_ENDPOINT = "https://api.kaggle.com/v1/datasets.DatasetApiService/DownloadDataset"
_IDENTITY_CODE = "SOURCE_IDENTITY_OR_SCHEMA"
_FETCH_CODE = "SOURCE_FETCH_OR_ARCHIVE"


class SourceError(ValueError):
    """Fixed safe failure fields; never contains a lower-level exception."""

    def __init__(self, code: str, reason: str):
        self.code = code
        self.reason = reason
        super().__init__(code + ":" + reason)


@dataclass(frozen=True, repr=False)
class SourceData:
    times: np.ndarray = field(repr=False)
    position: np.ndarray = field(repr=False)
    identity: dict = field(repr=False)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class _Absent(Exception):
    pass


def _fail(code, reason):
    raise SourceError(code, reason) from None


def _checkpoint(callback, stage):
    if callback is not None:
        callback(stage=stage, cell_id=None, completed_origins=0)


def _utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _config(source_spec):
    """Accept the frozen source dictionary; fixtures use this same boundary."""
    if type(source_spec) is not dict:
        _fail(_IDENTITY_CODE, "SOURCE_CONFIGURATION")
    try:
        size = source_spec["expected_csv_bytes"]
        rows = source_spec["expected_rows"]
        digest = source_spec["expected_csv_sha256"]
        header = source_spec["expected_header"]
        time_format = source_spec["timestamp_format"]
        if (type(size) is not int or not 0 < size <= _MAX_RAW_BYTES
                or type(rows) is not int or rows <= 0
                or type(digest) is not str or len(digest) != 64
                or any(c not in "0123456789abcdef" for c in digest)
                or type(header) is not list or len(header) != 5
                or any(type(s) is not str for s in header)
                or len(set(header)) != 5
                or "datetime" not in header or "NetPosUsd" not in header
                or time_format != "%Y.%m.%dT%H:%M:%S.%f"):
            _fail(_IDENTITY_CODE, "SOURCE_CONFIGURATION")
    except (KeyError, TypeError):
        _fail(_IDENTITY_CODE, "SOURCE_CONFIGURATION")
    return source_spec


def _read_local_snapshot(path, spec):
    fd = None
    try:
        # NONBLOCK permits immediate rejection of a FIFO or other special file.
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            _fail(_IDENTITY_CODE, "LOCAL_NOT_REGULAR")
        expected = spec["expected_csv_bytes"]
        if opened.st_size != expected:
            _fail(_IDENTITY_CODE, "CSV_IDENTITY")
        pieces = []
        count = 0
        while count <= expected:
            piece = os.read(fd, min(_CHUNK_BYTES, expected + 1 - count))
            if not piece:
                break
            pieces.append(piece)
            count += len(piece)
        snapshot = b"".join(pieces)
        if len(snapshot) != expected:
            _fail(_IDENTITY_CODE, "CSV_IDENTITY")
        return snapshot
    except FileNotFoundError:
        raise _Absent from None
    except SourceError:
        raise
    except OSError:
        _fail(_IDENTITY_CODE, "LOCAL_IO")
    finally:
        if fd is not None:
            os.close(fd)


def _verify_bytes(snapshot, spec, *, downloaded=False):
    if (len(snapshot) != spec["expected_csv_bytes"]
            or hashlib.sha256(snapshot).hexdigest() != spec["expected_csv_sha256"]):
        _fail(_FETCH_CODE if downloaded else _IDENTITY_CODE,
              "RAW_IDENTITY" if downloaded else "CSV_IDENTITY")


def _parse_snapshot(snapshot, spec):
    try:
        text = snapshot.decode("utf-8")
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        if next(reader, None) != spec["expected_header"]:
            _fail(_IDENTITY_CODE, "CSV_SCHEMA")
        time_column = spec["expected_header"].index("datetime")
        position_column = spec["expected_header"].index("NetPosUsd")
        times = []
        positions = []
        previous = None
        for row in reader:
            if len(row) != len(spec["expected_header"]) or len(times) >= spec["expected_rows"]:
                _fail(_IDENTITY_CODE, "CSV_SCHEMA")
            try:
                timestamp = datetime.strptime(row[time_column], spec["timestamp_format"])
            except (ValueError, OverflowError):
                _fail(_IDENTITY_CODE, "CSV_CHRONOLOGY")
            if timestamp.tzinfo is not None or (previous is not None and timestamp <= previous):
                _fail(_IDENTITY_CODE, "CSV_CHRONOLOGY")
            try:
                position = float(row[position_column])
            except (ValueError, OverflowError):
                _fail(_IDENTITY_CODE, "CSV_POSITION")
            if not math.isfinite(position):
                _fail(_IDENTITY_CODE, "CSV_POSITION")
            times.append(timestamp)
            positions.append(position)
            previous = timestamp
        if len(times) != spec["expected_rows"]:
            _fail(_IDENTITY_CODE, "CSV_SCHEMA")
        time_array = np.array(times, dtype="datetime64[us]")
        position_array = np.array(positions, dtype=np.float64)
        if np.isnat(time_array).any() or not np.isfinite(position_array).all():
            _fail(_IDENTITY_CODE, "CSV_SCHEMA")
        time_array.setflags(write=False)
        position_array.setflags(write=False)
        return time_array, position_array
    except SourceError:
        raise
    except (UnicodeError, csv.Error, ValueError, OverflowError):
        _fail(_IDENTITY_CODE, "CSV_SCHEMA")


def _budget(remaining_seconds):
    if not callable(remaining_seconds):
        _fail(_FETCH_CODE, "FETCH_BUDGET")
    try:
        remaining = remaining_seconds()
        if type(remaining) not in (int, float) or not math.isfinite(remaining) or remaining <= 0:
            _fail(_FETCH_CODE, "FETCH_BUDGET")
    except SourceError:
        raise
    except (TypeError, ValueError, OverflowError):
        _fail(_FETCH_CODE, "FETCH_BUDGET")
    return min(float(remaining), 10.0)


def _fetch_configuration(spec):
    if (spec.get("fetch_endpoint") != _ENDPOINT
            or spec.get("fetch_method") != "POST"
            or spec.get("initial_host") != "api.kaggle.com"
            or spec.get("allowed_redirect_hosts") != ["storage.googleapis.com"]
            or spec.get("allowed_https_ports") != [443]
            or spec.get("allowed_redirect_statuses") != [302]
            or spec.get("max_redirects") != 1 or spec.get("final_status") != 200
            or spec.get("accepted_final_media_types") != ["application/zip"]
            or type(spec.get("fetch_request")) is not dict):
        _fail(_FETCH_CODE, "FETCH_CONFIGURATION")
    request = spec["fetch_request"]
    if (set(request) != {"ownerSlug", "datasetSlug", "datasetVersionNumber", "fileName"}
            or any(type(request.get(key)) is not str or not request[key]
                   for key in ("ownerSlug", "datasetSlug", "fileName"))
            or type(request.get("datasetVersionNumber")) is not int
            or request["datasetVersionNumber"] <= 0
            or request["fileName"] != spec.get("requested_member")):
        _fail(_FETCH_CODE, "FETCH_CONFIGURATION")
    try:
        return json.dumps(request, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail(_FETCH_CODE, "FETCH_CONFIGURATION")


def _redirect_location(location):
    if type(location) is not str or not location or any(ord(c) <= 32 or ord(c) == 127 for c in location):
        _fail(_FETCH_CODE, "REDIRECT_URL")
    try:
        parsed = urllib.parse.urlsplit(location)
        if (parsed.scheme != "https" or parsed.hostname != "storage.googleapis.com"
                or parsed.port not in (None, 443)
                or parsed.username is not None or parsed.password is not None
                or parsed.fragment or "#" in location
                or parsed.netloc.lower() not in ("storage.googleapis.com", "storage.googleapis.com:443")
                or not parsed.path.startswith("/")):
            _fail(_FETCH_CODE, "REDIRECT_URL")
        return bool(parsed.query)
    except (ValueError, TypeError):
        _fail(_FETCH_CODE, "REDIRECT_URL")


def _open_response(request, remaining_seconds):
    timeout = _budget(remaining_seconds)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
    try:
        return opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as response:
        # HTTPError is a file-like response.  The caller must close it unread.
        return response
    except (urllib.error.URLError, http.client.HTTPException, OSError,
            ValueError, OverflowError):
        _fail(_FETCH_CODE, "HTTP_TRANSPORT")


def _response_status(response):
    try:
        return response.getcode()
    except (AttributeError, TypeError, ValueError):
        _fail(_FETCH_CODE, "HTTP_STATUS")


def _stream_archive(response, remaining_seconds, checkpoint):
    media = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    if media != "application/zip":
        _fail(_FETCH_CODE, "HTTP_MEDIA_TYPE")
    declared = response.headers.get("Content-Length")
    if declared is not None:
        if not isinstance(declared, str) or not declared.isascii() or not declared.isdecimal():
            _fail(_FETCH_CODE, "DOWNLOAD_SIZE")
        try:
            declared = int(declared)
        except ValueError:
            _fail(_FETCH_CODE, "DOWNLOAD_SIZE")
        if declared > _MAX_DOWNLOAD_BYTES:
            _fail(_FETCH_CODE, "DOWNLOAD_SIZE")
    pieces = []
    count = 0
    while True:
        _budget(remaining_seconds)
        _checkpoint(checkpoint, "source_download")
        _budget(remaining_seconds)
        try:
            piece = response.read(min(_CHUNK_BYTES, _MAX_DOWNLOAD_BYTES + 1 - count))
        except (OSError, urllib.error.URLError, http.client.HTTPException, ValueError):
            _fail(_FETCH_CODE, "HTTP_TRANSPORT")
        if type(piece) is not bytes:
            _fail(_FETCH_CODE, "HTTP_TRANSPORT")
        if not piece:
            break
        count += len(piece)
        if count > _MAX_DOWNLOAD_BYTES:
            _fail(_FETCH_CODE, "DOWNLOAD_SIZE")
        pieces.append(piece)
    if declared is not None and count != declared:
        _fail(_FETCH_CODE, "DOWNLOAD_SIZE")
    _budget(remaining_seconds)
    return b"".join(pieces)


def _download(spec, remaining_seconds, checkpoint):
    body = _fetch_configuration(spec)
    _budget(remaining_seconds)
    first = urllib.request.Request(_ENDPOINT, data=body,
                                   headers={"Content-Type": "application/json"}, method="POST")
    response = _open_response(first, remaining_seconds)
    try:
        if _response_status(response) != 302:
            _fail(_FETCH_CODE, "HTTP_STATUS")
        location = response.headers.get("Location")
        query_present = _redirect_location(location)
    finally:
        response.close()
    # The signed URL stays in these local variables; no POST material follows.
    second = urllib.request.Request(location, method="GET")
    response = _open_response(second, remaining_seconds)
    try:
        if _response_status(response) != 200:
            _fail(_FETCH_CODE, "HTTP_STATUS")
        payload = _stream_archive(response, remaining_seconds, checkpoint)
    finally:
        response.close()
    facts = {
        "endpoint": _ENDPOINT, "http_status": 200,
        "redirect_hosts": ["storage.googleapis.com"], "redirect_statuses": [302],
        "query_present": bool(query_present), "archive_bytes": int(len(payload)),
        "archive_sha256": hashlib.sha256(payload).hexdigest(),
    }
    return payload, facts


def _unpack(payload, spec, remaining_seconds, checkpoint):
    _budget(remaining_seconds)
    _checkpoint(checkpoint, "source_archive")
    allowed = spec.get("accepted_zip_members")
    expected = spec["expected_csv_bytes"]
    if (type(allowed) is not list or not allowed
            or any(type(name) is not str for name in allowed)
            or spec.get("zip_policy", {}).get("extracted_byte_cap") != expected):
        _fail(_FETCH_CODE, "FETCH_CONFIGURATION")
    try:
        with zipfile.ZipFile(io.BytesIO(payload), "r") as zf:
            members = zf.infolist()
            if len(members) != 1:
                _fail(_FETCH_CODE, "ZIP_POLICY")
            member = members[0]
            name = member.filename
            path = PurePosixPath(name)
            mode = member.external_attr >> 16
            filetype = stat.S_IFMT(mode)
            if (name not in allowed or member.is_dir() or path.is_absolute()
                    or ".." in path.parts or "\\" in name or "\x00" in name
                    or any(part in ("", ".") for part in name.split("/"))
                    or filetype not in (0, stat.S_IFREG)
                    or member.flag_bits & 1
                    or member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
                    or member.file_size != expected):
                _fail(_FETCH_CODE, "ZIP_POLICY")
            pieces = []
            count = 0
            with zf.open(member, "r") as stream:
                while count <= expected:
                    _budget(remaining_seconds)
                    _checkpoint(checkpoint, "source_archive")
                    piece = stream.read(min(_CHUNK_BYTES, expected + 1 - count))
                    if not piece:
                        break
                    count += len(piece)
                    if count > expected:
                        _fail(_FETCH_CODE, "ZIP_POLICY")
                    pieces.append(piece)
            snapshot = b"".join(pieces)
    except SourceError:
        raise
    except (zipfile.BadZipFile, zlib.error, RuntimeError, OSError, EOFError,
            ValueError, NotImplementedError):
        _fail(_FETCH_CODE, "ZIP_INTEGRITY")
    _verify_bytes(snapshot, spec, downloaded=True)
    return snapshot


def _accept_exclusively(path, snapshot):
    """A same-directory temporary inode is linked atomically without replace."""
    temporary = None
    try:
        destination = Path(path)
        fd, temporary = tempfile.mkstemp(prefix=".source-", suffix=".tmp", dir=destination.parent)
        with os.fdopen(fd, "wb") as stream:
            stream.write(snapshot)
            stream.flush()
            os.fsync(stream.fileno())
        # link is exclusive even if another writer creates a file or symlink.
        os.link(temporary, destination, follow_symlinks=False)
    except (OSError, ValueError, TypeError):
        _fail(_FETCH_CODE, "CACHE_ACCEPT")
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass


def load_source(path, source_spec, *, fetch=False,
                remaining_seconds: Callable[[], float] | None = None,
                checkpoint=None):
    """Validate one opened immutable snapshot, or explicitly fetch if absent.

    ``remaining_seconds`` is mandatory for acquisition and must represent the
    runner's remaining global budget.  Callback operands are safe progress only.
    Existing local input is always validated first and is never replaced.
    """
    spec = _config(source_spec)
    download = None
    acquisition_mode = "local_reuse"
    try:
        snapshot = _read_local_snapshot(path, spec)
    except _Absent:
        # A dangling local symlink is an existing input, never an output route.
        if not fetch or os.path.lexists(path):
            _fail(_IDENTITY_CODE, "LOCAL_ABSENT")
        payload, download = _download(spec, remaining_seconds, checkpoint)
        snapshot = _unpack(payload, spec, remaining_seconds, checkpoint)
        acquisition_mode = "explicit_fetch"
    _checkpoint(checkpoint, "source_snapshot")
    _verify_bytes(snapshot, spec)
    times, position = _parse_snapshot(snapshot, spec)
    if acquisition_mode == "explicit_fetch":
        _budget(remaining_seconds)
        _accept_exclusively(path, snapshot)
    identity = {
        "accepted_csv_bytes": int(len(snapshot)),
        "accepted_csv_sha256": spec["expected_csv_sha256"],
        "source_verified": True, "acquisition_mode": acquisition_mode,
        "request_performed_this_attempt": acquisition_mode == "explicit_fetch",
        "historical_access_utc": None, "local_validation_utc": _utc_now(),
        "download": download,
    }
    return SourceData(times=times, position=position, identity=identity)
