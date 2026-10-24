"""Frozen v8 pre-validation-prefix calibration; no fitting occurs on import.

The only source entry point is calibrate_all(root). File identity is checked
by conditional_sources before a fixed explicit prefix is passed to estimation.
The module neither downloads data nor writes calibration outputs.
"""
from __future__ import annotations

from datetime import datetime, timezone
import importlib.metadata
import math
from pathlib import Path
import platform
import sys

import numpy as np

from conditional_sources import SourceError, load_source


SOURCE_PINS = {
    "fx_hourly": {
        "path": ".scratch/data/1hourNetPositionsKaggle.csv", "bytes": 1286391,
        "sha256": "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa",
        "record_count": 18576, "prefix_stop": 10463,
        "last_prefix_date": "2015-10-07T23:00:00.000000",
        "validation_first_date": "2015-10-08T00:00:00.000000",
    },
    "nyfed_weekly": {
        "path": ".scratch/revision-20261022/nyfed-PDPOSGS-B.csv", "bytes": 23315,
        "sha256": "9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb",
        "record_count": 706, "prefix_stop": 329,
        "last_prefix_date": "2019-07-17T00:00:00.000000",
        "validation_first_date": "2019-07-24T00:00:00.000000",
    },
}


class CalibrationError(ValueError):
    """Terminal calibration reason and JSON-safe diagnostics, never raw data."""

    def __init__(self, reason, details=None):
        self.reason = reason
        self.details = details or {}
        super().__init__(reason)


def fit_ar1(values):
    """OLS intercept AR(1), fixed slope projection, and refitted intercept."""
    values = np.asarray(values, dtype=float)
    if (values.ndim != 1 or len(values) < 3 or not np.isfinite(values).all()
            or not float(np.std(values[:-1])) > 0.):
        raise CalibrationError("AR_INPUT_INVALID")
    x, y = values[:-1], values[1:]
    coefficients = np.linalg.lstsq(np.column_stack((np.ones(len(x)), x)), y, rcond=None)[0]
    unconstrained_c, unconstrained_phi = map(float, coefficients)
    if not all(map(math.isfinite, (unconstrained_c, unconstrained_phi))):
        raise CalibrationError("AR_NONFINITE")
    phi = float(np.clip(unconstrained_phi, -.995, .995))
    binds = phi != unconstrained_phi
    c = float(np.mean(y - phi * x)) if binds else unconstrained_c
    residuals = y - c - phi * x
    residual_variance = float(np.mean(residuals**2))
    if not math.isfinite(residual_variance):
        raise CalibrationError("AR_NONFINITE")
    return {"c": c, "phi": phi, "unconstrained_c": unconstrained_c,
            "unconstrained_phi": unconstrained_phi, "constraint_binds": binds,
            "residual_variance": residual_variance, "residual_count": len(residuals),
            "residuals": residuals}


def diurnal_shape(residuals, hours):
    """Hour RMS normalized by its prefix observation-weighted mean square."""
    residuals, hours = np.asarray(residuals, float), np.asarray(hours)
    if (residuals.ndim != 1 or hours.shape != residuals.shape
            or not np.isfinite(residuals).all() or not np.isin(hours, np.arange(24)).all()):
        raise CalibrationError("HOUR_SHAPE_INPUT_INVALID")
    counts = np.bincount(hours.astype(int), minlength=24)
    if np.any(counts == 0):
        raise CalibrationError("HOUR_MISSING")
    sum_squares = np.bincount(hours.astype(int), weights=residuals**2, minlength=24)
    rms = np.sqrt(sum_squares / counts)
    if not np.isfinite(rms).all() or np.any(rms <= 0.):
        raise CalibrationError("HOUR_RMS_NONPOSITIVE")
    normalizer = float(np.sqrt(np.average(rms**2, weights=counts)))
    return rms / normalizer, counts


def garch_burnin(phi, parameters):
    """Validate fitted GARCH parameters before computing the frozen burn-in."""
    try:
        omega, alpha, beta, nu = (float(parameters[name]) for name in ("omega", "alpha", "beta", "nu"))
    except (KeyError, TypeError, ValueError):
        raise CalibrationError("GARCH_PARAMETER_INVALID") from None
    if not all(map(math.isfinite, (omega, alpha, beta, nu, float(phi)))):
        raise CalibrationError("GARCH_NONFINITE")
    if omega <= 0. or alpha < 0. or beta < 0. or nu <= 2.:
        raise CalibrationError("GARCH_PARAMETER_INVALID")
    if alpha + beta >= 1. or abs(phi) >= 1.:
        raise CalibrationError("GARCH_NONSTATIONARY")
    burnin = max(10000, math.ceil(10. / (1. - abs(phi))), math.ceil(10. / (1. - alpha - beta)))
    if burnin > 1000000:
        raise CalibrationError("BURNIN_LIMIT_EXCEEDED")
    return burnin


def fit_garch(residuals):
    """Exactly one package-default zero-mean GARCH(1,1)/Student-t fit."""
    from arch import arch_model

    residuals = np.asarray(residuals, dtype=float)
    if residuals.ndim != 1 or len(residuals) < 3 or not np.isfinite(residuals).all():
        raise CalibrationError("GARCH_INPUT_INVALID")
    try:
        model = arch_model(residuals, mean="Zero", vol="GARCH", p=1, o=0, q=1,
                           dist="StudentsT", rescale=False)
        fitted = model.fit(disp="off", show_warning=False)
        parameters = {"omega": float(fitted.params["omega"]),
                      "alpha": float(fitted.params["alpha[1]"]),
                      "beta": float(fitted.params["beta[1]"]),
                      "nu": float(fitted.params["nu"]),
                      "convergence_flag": int(fitted.convergence_flag),
                      "optimizer_message": str(fitted.optimization_result.message),
                      "arch_version": importlib.metadata.version("arch"),
                      "rescale": False, "fit_attempts": 1}
    except CalibrationError:
        raise
    except Exception as exc:
        raise CalibrationError("GARCH_FIT_EXCEPTION", {"exception_type": type(exc).__name__, "fit_attempts": 1}) from None
    if parameters["convergence_flag"] != 0:
        raise CalibrationError("GARCH_NONCONVERGENCE", parameters)
    try:
        # A zero slope here isolates parameter validation; actual AR slope is
        # included in the final burn-in below. No parameter is repaired.
        garch_burnin(0., parameters)
    except CalibrationError as exc:
        raise CalibrationError(exc.reason, parameters) from None
    return parameters


def calibrate_source(source, *, dgp, prefix_stop):
    """Estimate one DGP using only source.position[:prefix_stop].

    This lower-level function is also the synthetic-fixture boundary. The real
    data entry point verifies fixed file and cutoff identities before calling it.
    """
    record = {"dgp": dgp, "source_id": source.source_id}
    try:
        if dgp not in ("D0", "D1", "D2"):
            raise CalibrationError("DGP_CONFIGURATION")
        if type(prefix_stop) is not int or not 3 <= prefix_stop <= len(source.position):
            raise CalibrationError("PREFIX_BOUNDARY_INVALID")
        # The explicit slice precedes every transform, scale or estimation.
        prefix = np.asarray(source.position[:prefix_stop], dtype=float).copy()
        dates = np.asarray(source.dates[:prefix_stop], dtype="datetime64[us]").copy()
        if len(dates) != len(prefix) or np.isnat(dates).any() or not np.isfinite(prefix).all():
            raise CalibrationError("PREFIX_INVALID")
        record.update(prefix_count=prefix_stop, first_prefix_date=str(dates[0]),
                      last_prefix_date=str(dates[-1]))
        source_scale = float(np.std(prefix, ddof=0))
        if not math.isfinite(source_scale) or source_scale <= 0.:
            raise CalibrationError("NONPOSITIVE_SOURCE_SCALE")
        record["source_scale"] = source_scale
        record["scale_transformation"] = "position / prefix.std(ddof=0); no centering"
        ar = fit_ar1(prefix / source_scale)
        residuals = ar.pop("residuals")
        record["ar"] = ar
        sigma = float(np.sqrt(ar["residual_variance"]))
        if not math.isfinite(sigma) or sigma <= 0.:
            raise CalibrationError("NONPOSITIVE_RESIDUAL_VARIANCE")
        shape = np.ones(24)
        if dgp == "D1":
            hours = dates[1:].astype("datetime64[h]").astype(np.int64) % 24
            shape, counts = diurnal_shape(residuals, hours)
            residuals = residuals / shape[hours]
            record["hour_counts"] = counts.tolist()
            record["hour_shape_weighted_mean_square"] = float(np.average(shape**2, weights=counts))
        if dgp == "D0":
            garch = None
            burnin = max(10000, math.ceil(10. / (1. - abs(ar["phi"]))))
            omega, alpha, beta, nu = 0., 0., 0., None
        else:
            garch = fit_garch(residuals)
            record["garch"] = garch
            burnin = garch_burnin(ar["phi"], garch)
            omega, alpha, beta, nu = (garch[k] for k in ("omega", "alpha", "beta", "nu"))
        if burnin > 1000000:
            raise CalibrationError("BURNIN_LIMIT_EXCEEDED")
        parameters = {"dgp": dgp, "c": ar["c"], "phi": ar["phi"],
                      "omega": omega, "alpha": alpha, "beta": beta, "nu": nu,
                      "shape": tuple(float(x) for x in shape), "sigma": sigma,
                      "burnin": burnin}
        record.update(status="COMPLETE", parameters=parameters,
                      initialization={"N": ar["c"] / (1. - ar["phi"]),
                                      "v": sigma**2 if dgp == "D0" else omega / (1. - alpha - beta), "u": 0.})
    except CalibrationError as exc:
        record.update(status="FAILED", reason=exc.reason)
        if exc.details:
            # Retain a failed fit's fields while making nonfinite estimates
            # explicit nulls, so strict JSON output remains possible.
            record["failure_details"] = {
                key: None if isinstance(value, float) and not math.isfinite(value) else value
                for key, value in exc.details.items()
            }
    except (ValueError, TypeError, np.linalg.LinAlgError, FloatingPointError) as exc:
        record.update(status="FAILED", reason="CALIBRATION_EXCEPTION", exception_type=type(exc).__name__)
    return record


def _environment():
    return {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__,
            "arch": importlib.metadata.version("arch"),
            "created_at_utc": datetime.now(timezone.utc).isoformat()}


def calibrate_all(root):
    """Return JSON-safe parameters, pinned identities, cutoffs and diagnostics.

    No files are written. A failed source/DGP is recorded without retry and
    leaves its key absent from parameters; other DGPs continue.
    """
    root = Path(root)
    sources, identities = {}, {}
    for source_id, pin in SOURCE_PINS.items():
        identity = dict(pin)
        try:
            source = load_source(root / pin["path"], source_id,
                                 expected_sha256=pin["sha256"], expected_bytes=pin["bytes"])
            if len(source.position) != pin["record_count"]:
                raise CalibrationError("SOURCE_RECORD_COUNT")
            stop = pin["prefix_stop"]
            if str(source.dates[stop - 1]) != pin["last_prefix_date"]:
                raise CalibrationError("PREFIX_LAST_DATE")
            if str(source.dates[stop]) != pin["validation_first_date"]:
                raise CalibrationError("VALIDATION_FIRST_DATE")
            sources[source_id] = source
            identity.update(status="VERIFIED", observed_sha256=source.sha256,
                            observed_bytes=source.bytes, first_prefix_date=str(source.dates[0]),
                            last_prefix_date=str(source.dates[stop - 1]),
                            validation_first_date=str(source.dates[stop]),
                            units=source.metadata["units"])
        except (SourceError, CalibrationError) as exc:
            identity.update(status="FAILED", reason=exc.reason)
        identities[source_id] = identity
    calibrations, parameters = {}, {}
    for dgp, source_id in (("D0", "nyfed_weekly"), ("D1", "fx_hourly"), ("D2", "nyfed_weekly")):
        if source_id not in sources:
            result = {"dgp": dgp, "source_id": source_id, "status": "FAILED",
                      "reason": "SOURCE_IDENTITY_FAILED", "source_reason": identities[source_id]["reason"]}
        else:
            result = calibrate_source(sources[source_id], dgp=dgp, prefix_stop=SOURCE_PINS[source_id]["prefix_stop"])
        calibrations[dgp] = result
        if result["status"] == "COMPLETE":
            parameters[dgp] = result["parameters"]
    return {"status": "COMPLETE" if len(parameters) == 3 else "PARTIAL_FAILURE",
            "parameters": parameters, "calibrations": calibrations,
            "sources": identities, "environment": _environment(),
            "design": "protocol/v8/mc-design.md", "parameter_units": "dimensionless standardized source units"}
