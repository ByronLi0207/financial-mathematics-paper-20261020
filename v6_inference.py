"""Aggregate-only diagnostics for the frozen exploratory v6 procedures.

The original DM/HAC/HLN convention, scalar likelihood and probability helpers,
and Holm arithmetic are reused from immutable ``inference_tests``. Its legacy
``coverage_tests`` is deliberately not called: v6 transition-conditional CC
compares the saturated Markov likelihood with the fixed-alpha likelihood on
the SAME n-1 pairs, conditioning on the first hit.

All p-values are working-reference diagnostics, with unverified dependence,
moment, finite-sample and boundary assumptions. A reference failure is NA.
Holm bookkeeping values do not turn an NA component into a valid test.

Callers must supply the complete authoritative origin vector, including its
original evaluation anchor. Interior grid gaps are detected here; an already
truncated vector cannot establish whether an earlier original anchor existed.
No finance files are read and no per-origin arrays enter aggregate reports.
"""
from collections.abc import Mapping
from fractions import Fraction
import math

import numpy as np

import inference_tests as _original


def _tau_weights(tau):
    # Interpret the declared decimal level, matching the frozen 19/20 and 1/20
    # source weights without introducing binary subtraction in the complement.
    level = Fraction(str(tau))
    return float(level), float(1 - level)


def _tau_value(tau):
    tau = float(tau)
    if not math.isfinite(tau) or not 0 < tau < 1 or not 0 < _tau_weights(tau)[1] < 1:
        raise ValueError("tau and its computed hit null must be finite and strictly interior")
    return tau


def _horizon_value(horizon):
    if isinstance(horizon, (bool, np.bool_)) or not isinstance(horizon, (int, np.integer)) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    return int(horizon)


def _aligned_vectors(left, right):
    left, right = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    if left.ndim != 1 or right.ndim != 1 or len(left) != len(right):
        raise ValueError("aligned one-dimensional vectors required")
    return left, right


def _origin_vector(origins, n):
    raw = np.asarray(origins)
    if raw.ndim != 1 or len(raw) != n:
        raise ValueError("origins must align with the complete observation vector")
    try:
        result = [int(value) for value in raw]
        if any(not math.isfinite(float(value)) or value != integer
               for value, integer in zip(raw, result)):
            raise ValueError("finite integer origins required")
    except (TypeError, OverflowError, ValueError) as exc:
        raise ValueError("finite integer origins required") from exc
    if any(right <= left for left, right in zip(result[:-1], result[1:])):
        raise ValueError("origins must be unique and strictly increasing")
    return result


def pinball_losses(actual, forecast, *, tau):
    """Return private per-origin pinball losses using the supplied tau."""
    tau = _tau_value(tau)
    upper, lower = _tau_weights(tau)
    actual, forecast = _aligned_vectors(actual, forecast)
    if not len(actual) or not np.isfinite(actual).all() or not np.isfinite(forecast).all():
        raise ValueError("finite nonempty score vectors required")
    with np.errstate(over="ignore", invalid="ignore"):
        errors = actual - forecast
        losses = upper * np.maximum(errors, 0) + lower * np.maximum(-errors, 0)
    if not np.isfinite(losses).all():
        raise ValueError("pinball losses are nonfinite")
    return losses


def _unconditional_coverage(hits, alpha):
    n, k = len(hits), int(sum(hits))
    boundary = bool(n and k in (0, n))
    out = dict(n=n, hits=k, rate=k / n if n else None, uc_lr=None, uc_p=None,
               uc_status="EMPTY_SAMPLE", boundary=boundary)
    if n:
        lr = max(0., 2 * (_original.log_bernoulli(k, n, k / n)
                          - _original.log_bernoulli(k, n, alpha)))
        out.update(uc_lr=lr, uc_p=_original.chi_tail(lr, 1),
                   uc_status="BOUNDARY_REFERENCE" if boundary else "OK")
    return out


def _transition_conditional_cc(hits, alpha):
    counts = [[0, 0], [0, 0]]
    for previous, current in zip(hits[:-1], hits[1:]):
        counts[previous][current] += 1
    row_n = [sum(row) for row in counts]
    n_pairs = max(0, len(hits) - 1)
    zeros = sum(cell == 0 for row in counts for cell in row)
    absent = sum(n == 0 for n in row_n)
    out = dict(definition="TRANSITION_CONDITIONAL", conditioning="FIRST_HIT",
               transition_n=n_pairs, n00=counts[0][0], n01=counts[0][1],
               n10=counts[1][0], n11=counts[1][1],
               boundary=bool(zeros), boundary_cell_count=zeros,
               absent_row_count=absent, reference_df=2, lr=None, p=None,
               saturated_log_likelihood=None, fixed_alpha_log_likelihood=None,
               status="TOO_SHORT" if not n_pairs else "UNIDENTIFIED_TRANSITION_ROW")
    if not n_pairs or absent:
        return out
    saturated = math.fsum(
        _original.log_bernoulli(row[1], n, row[1] / n)
        for row, n in zip(counts, row_n))
    successors = counts[0][1] + counts[1][1]
    fixed = _original.log_bernoulli(successors, n_pairs, alpha)
    lr = max(0., 2 * (saturated - fixed))
    out.update(lr=lr, p=_original.chi_tail(lr, 2),
               saturated_log_likelihood=saturated, fixed_alpha_log_likelihood=fixed,
               status="BOUNDARY_REFERENCE" if zeros else "OK")
    return out


def coverage_diagnostics(hits, *, tau, origins, horizon):
    """Full-origin UC plus exact first+j(H+1) grid UC and conditional CC.

    The grid's UC uses all its hits. CC uses only its n-1 consecutive pairs.
    A missing required grid origin suppresses grid tests rather than joining
    the surviving hits across the gap. Reports contain counts and metadata.
    """
    tau, horizon = _tau_value(tau), _horizon_value(horizon)
    raw = np.asarray(hits, dtype=float)
    if raw.ndim != 1 or not np.isfinite(raw).all() or not np.isin(raw, [0, 1]).all():
        raise ValueError("finite binary one-dimensional hits required")
    origin_values = _origin_vector(origins, len(raw))
    hit_values = [int(hit) for hit in raw]
    alpha = _tau_weights(tau)[1]
    full = _unconditional_coverage(hit_values, alpha)
    step = horizon + 1
    start = origin_values[0] if origin_values else None
    expected_n = (origin_values[-1] - start) // step + 1 if origin_values else 0
    grid_hits = [hit for origin, hit in zip(origin_values, hit_values)
                 if (origin - start) % step == 0]
    grid = _unconditional_coverage(grid_hits, alpha)
    grid.update(origins=dict(start=start, step=step, expected_count=expected_n,
                             observed_count=len(grid_hits)),
                missing_origin_count=expected_n - len(grid_hits))
    cc = _transition_conditional_cc(grid_hits, alpha)
    if grid["missing_origin_count"]:
        grid.update(uc_lr=None, uc_p=None, uc_status="MISSING_GRID_ORIGINS")
        # Counts over surviving rows cannot be called consecutive transitions.
        cc.update(lr=None, p=None, status="MISSING_GRID_ORIGINS",
                  transition_n=None, n00=None, n01=None, n10=None, n11=None,
                  boundary=None, boundary_cell_count=None, absent_row_count=None,
                  saturated_log_likelihood=None, fixed_alpha_log_likelihood=None)
    grid["transition_cc"] = cc
    na_count = sum(p is None for p in (full["uc_p"], grid["uc_p"], cc["p"]))
    boundary_count = sum(bool(value) for value in (full["boundary"], grid["boundary"], cc["boundary"]))
    return dict(status="OK" if not na_count else "PARTIAL_REFERENCE_NA", tau=tau,
                null_probability=alpha, horizon=horizon, full=full,
                fixed_grid=grid, boundary_count=boundary_count, na_count=na_count)


def summarize_scores(actual, forecast, *, tau, origins, horizon):
    """Return JSON-safe score/hit aggregates without deleting any issue row."""
    tau, horizon = _tau_value(tau), _horizon_value(horizon)
    actual, forecast = _aligned_vectors(actual, forecast)
    _origin_vector(origins, len(actual))
    invalid = int((~(np.isfinite(actual) & np.isfinite(forecast))).sum())
    out = dict(status="NONFINITE_SCORES" if invalid else "EMPTY_SAMPLE",
               n=len(actual), tau=tau, horizon=horizon, nonfinite_count=invalid,
               mean_loss=None, full_hits=None, full_rate=None,
               coverage_distance=None, coverage=None)
    if invalid or not len(actual):
        return out
    try:
        losses = pinball_losses(actual, forecast, tau=tau)
        mean_loss = math.fsum(map(float, losses)) / len(losses)
    except (ValueError, OverflowError):
        out["status"] = "NONFINITE_LOSS"
        return out
    coverage = coverage_diagnostics(actual > forecast, tau=tau, origins=origins, horizon=horizon)
    full = coverage["full"]
    out.update(status="OK", mean_loss=mean_loss, full_hits=full["hits"],
               full_rate=full["rate"], coverage_distance=abs(full["rate"] - coverage["null_probability"]),
               coverage=coverage)
    return out


def compare_losses(new_losses, control_losses, *, horizon):
    """Original DM/HAC and HLN for new minus control; no pair deletion."""
    horizon = _horizon_value(horizon)
    new, control = _aligned_vectors(new_losses, control_losses)
    n = len(new)
    out = dict(n=n, horizon=horizon, bandwidth=_original.bandwidth(n, horizon) if n else None,
               direction="new_minus_control", mean_difference=None, lrv=None,
               dm_t=None, dm_p=None, hln_t=None, hln_p=None,
               nonfinite_count=int((~(np.isfinite(new) & np.isfinite(control))).sum()))
    if out["nonfinite_count"]:
        out["status"] = "NONFINITE_LOSSES"
        return out
    if n <= horizon:
        out["status"] = "EMPTY_SAMPLE" if not n else "TOO_SHORT"
        return out
    with np.errstate(over="ignore", invalid="ignore"):
        differences = new - control
    if not np.isfinite(differences).all():
        out["status"] = "NONFINITE_DIFFERENCE"
        return out
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            diagnostic = _original.dm_test(differences, horizon)
    except ArithmeticError:
        out["status"] = "REFERENCE_FAILURE"
        return out
    if any(isinstance(value, (float, np.floating)) and not math.isfinite(value)
           for value in diagnostic.values()):
        out["status"] = "NONFINITE_REFERENCE"
        return out
    out.update(diagnostic)
    return out


def fixed_slot_holm(slot_ids, raw_pvalues):
    """Adjust every declared slot; raw NA and bookkeeping one stay distinct.

    Supply the full frozen inventory, even if all component tests failed.
    Missing, explicit None and nonfinite p-values retain separate statuses.
    Unknown keys, duplicate slots and out-of-range finite p-values are errors.
    """
    slots = list(slot_ids)
    if not slots or any(not isinstance(slot, str) or not slot for slot in slots) or len(set(slots)) != len(slots):
        raise ValueError("a nonempty inventory of unique string slot IDs is required")
    if not isinstance(raw_pvalues, Mapping) or set(raw_pvalues) - set(slots):
        raise ValueError("raw p-values must be a mapping over the supplied inventory")
    rows = []
    for slot in slots:
        value, status = None, "MISSING_RAW_P"
        if slot in raw_pvalues:
            supplied = raw_pvalues[slot]
            if supplied is None:
                status = "RAW_P_NA"
            else:
                supplied = float(supplied)
                if not math.isfinite(supplied):
                    status = "RAW_P_NONFINITE"
                elif not 0 <= supplied <= 1:
                    raise ValueError("finite raw p-values must lie in [0,1]")
                else:
                    value, status = supplied, "OK"
        rows.append(dict(slot_id=slot, raw_p=value,
                         bookkeeping_p=1. if value is None else value, status=status))
    adjusted = _original.holm([row["bookkeeping_p"] for row in rows])
    for row, p in zip(rows, adjusted):
        row["holm_p"] = float(p)
    return dict(family_n=len(slots), raw_na_count=sum(row["raw_p"] is None for row in rows), slots=rows)
