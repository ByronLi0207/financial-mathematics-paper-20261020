"""Strict local position-series loading from one caller-pinned byte snapshot.

This module has no network, source discovery, repair or experiment entry point.
Identity checks precede financial-token parsing; returned arrays have immutable
byte backing.  Errors contain fixed codes instead of paths or rejected values.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import io
import math
import os
import re
import stat

import numpy as np


_SOURCE_HEADERS = {
    "fx_hourly": ["datetime", "NetPosUsd", "NetUsdPnL", "AbsVolume", "Mid"],
    "nyfed_weekly": ["As Of Date", "Time Series", "Value (millions)"],
}
_NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_CHUNK_BYTES = 64 * 1024


class SourceError(ValueError):
    """A fixed, safe reason code; no input values or filesystem path."""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class SourceSeries:
    """Source identity plus immutable sampled positions and economic dates.

    Metadata is a flat JSON-safe dictionary of nonfinancial identity/date/gap
    summaries.  It contains no raw observations or input filesystem path.
    """

    source_id: str
    dates: np.ndarray = field(repr=False)
    position: np.ndarray = field(repr=False)
    sha256: str
    bytes: int
    metadata: dict = field(repr=False)


def _fail(reason):
    raise SourceError(reason) from None


def _check_identity_arguments(source_id, expected_sha256, expected_bytes):
    if type(source_id) is not str or source_id not in _SOURCE_HEADERS:
        _fail("SOURCE_CONFIGURATION")
    size_cap = 2 * 1024 * 1024 if source_id == "nyfed_weekly" else 100 * 1024 * 1024
    if (type(expected_sha256) is not str
            or re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None
            or type(expected_bytes) is not int
            or not 0 < expected_bytes <= size_cap):
        _fail("SOURCE_CONFIGURATION")


def _read_snapshot(path, expected_bytes):
    descriptor = None
    try:
        # A FIFO must not block this local-file-only boundary.
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            _fail("SOURCE_NOT_REGULAR")
        if before.st_size != expected_bytes:
            _fail("SOURCE_SIZE")
        pieces = []
        count = 0
        while count <= expected_bytes:
            piece = os.read(descriptor, min(_CHUNK_BYTES, expected_bytes + 1 - count))
            if not piece:
                break
            pieces.append(piece)
            count += len(piece)
        after = os.fstat(descriptor)
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            _fail("SOURCE_CHANGED")
        if count != expected_bytes:
            _fail("SOURCE_SIZE")
        return b"".join(pieces)
    except SourceError:
        raise
    except (OSError, TypeError, ValueError):
        _fail("SOURCE_IO")
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _parse_snapshot(raw, source_id):
    header = _SOURCE_HEADERS[source_id]
    try:
        reader = csv.reader(io.StringIO(raw.decode("utf-8"), newline=""), strict=True)
        if next(reader, None) != header:
            _fail("SOURCE_SCHEMA")
        dates, values = [], []
        previous = None
        for row in reader:
            if len(row) != len(header):
                _fail("SOURCE_SCHEMA")
            if source_id == "nyfed_weekly":
                if row[1] != "PDPOSGS-B":
                    _fail("SOURCE_KEY")
                if _ISO_DATE.fullmatch(row[0]) is None:
                    _fail("SOURCE_CHRONOLOGY")
                date_format, value_column = "%Y-%m-%d", 2
            else:
                # Preserve the accepted FX source's original strptime format.
                date_format, value_column = "%Y.%m.%dT%H:%M:%S.%f", 1
            try:
                timestamp = datetime.strptime(row[0], date_format)
            except (ValueError, OverflowError):
                _fail("SOURCE_CHRONOLOGY")
            if timestamp.tzinfo is not None or (previous is not None and timestamp <= previous):
                _fail("SOURCE_CHRONOLOGY")
            token = row[value_column].strip()
            if _NUMBER.fullmatch(token) is None:
                _fail("SOURCE_POSITION")
            try:
                value = float(token)
            except (ValueError, OverflowError):
                _fail("SOURCE_POSITION")
            if not math.isfinite(value):
                _fail("SOURCE_POSITION")
            dates.append(timestamp)
            values.append(value)
            previous = timestamp
        if not dates:
            _fail("SOURCE_SCHEMA")
        dates = np.frombuffer(np.asarray(dates, dtype="datetime64[us]").tobytes(), dtype="datetime64[us]")
        position = np.frombuffer(np.asarray(values, dtype=np.float64).tobytes(), dtype=np.float64)
        if np.isnat(dates).any() or not np.isfinite(position).all():
            _fail("SOURCE_SCHEMA")
        return dates, position
    except SourceError:
        raise
    except (UnicodeError, csv.Error, ValueError, OverflowError):
        _fail("SOURCE_SCHEMA")


def load_source(path, source_id, *, expected_sha256, expected_bytes):
    """Verify one pinned local snapshot, then parse without repairing any row.

    Only ``fx_hourly`` and ``nyfed_weekly`` are supported.  The caller must pin
    both a lowercase SHA-256 and a positive byte count.  Gaps remain intact;
    no sorting, dropping, alias splicing, imputation or unit conversion occurs.
    Only the FX time/position columns are used; its other fields are preserved
    structurally but not interpreted.  NYFed requires PDPOSGS-B on every row.
    """
    _check_identity_arguments(source_id, expected_sha256, expected_bytes)
    raw = _read_snapshot(path, expected_bytes)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        _fail("SOURCE_HASH")
    dates, position = _parse_snapshot(raw, source_id)
    units, nominal = ("USD", 3600) if source_id == "fx_hourly" else ("USD millions", 604800)
    gaps_us = np.diff(dates.astype(np.int64))
    unique, counts = np.unique(gaps_us, return_counts=True)
    metadata = {
        "units": units, "observation_count": len(position),
        "first_date": str(dates[0]), "last_date": str(dates[-1]),
        "nominal_interval_seconds": nominal,
        "gap_seconds_unique": (unique / 1_000_000).tolist(),
        "gap_counts": counts.tolist(),
        "irregular_gap_count": int(np.count_nonzero(gaps_us != nominal * 1_000_000)),
    }
    return SourceSeries(source_id, dates, position, digest, len(raw), metadata)
