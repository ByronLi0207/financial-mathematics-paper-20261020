"""Source-independent selected-row forecasts for the exploratory extension."""

from dataclasses import dataclass
import math

import numpy as np

import study_core as core


METHODS = ("F", "S", "K")


@dataclass(frozen=True)
class SelectedForecast:
    capacities: np.ndarray
    origins: np.ndarray
    rank: int
    absolute_radius: float
    signed_radius: float
    mean_age_records: float
    refined_bound: float
    arithmetic_tolerance: float
    geometry_excess: float


def issue_selected(t, current, labels, anchor_positions, cell, selection, count):
    """Issue F/S/K after validating the entire independently timed pool.

    Anchors are the signed positions paired with every row in ``labels``,
    rather than a raw history. Membership depends only on those anchors,
    origins and the current state. All selected rows retain chronological
    order. ``geometry_excess`` is the largest positive, pre-tolerance
    excess over any of the four declared finite-sample geometry bounds.
    """
    if not isinstance(cell, core.CellSpec) or not isinstance(labels, core.MatureLabelWindow):
        raise ValueError("invalid selected pool or cell")
    core._validate_window(t, labels, labels.origins, cell)
    label_origins = np.asarray(labels.origins, dtype=np.int64)
    t = int(t)
    if np.asarray(current).ndim != 0:
        raise ValueError("invalid current state")
    try:
        current = float(current)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("invalid current state") from exc
    if not math.isfinite(current):
        raise ValueError("nonfinite current state")
    anchors = core._vector(anchor_positions, "anchor positions")
    if anchors.shape != (cell.window,):
        raise ValueError("anchor positions shape mismatch")
    if not np.array_equal(labels.peak - np.abs(anchors), labels.headroom):
        raise ValueError("exact anchor/headroom alignment violation")
    if type(selection) is not str or selection not in ("full", "recent", "nearest"):
        raise ValueError("invalid selection")
    count = core._integer(count, "selected count", 1)
    if count > cell.window or (selection == "full" and count != cell.window):
        raise ValueError("selected count inconsistent with eligible pool")
    rank = core.exact_rank(count, cell.tau_numerator, cell.tau_denominator)
    if rank > count:
        raise ValueError("selected corrected rank unavailable")
    B = abs(current)
    try:
        with np.errstate(over="raise", invalid="raise"):
            if selection == "full":
                rows = np.arange(cell.window)
            elif selection == "recent":
                rows = np.arange(cell.window-count, cell.window)
            else:
                distances = np.abs(anchors-current)
                # Last lexsort key is primary: distance, then descending origin.
                rows = np.sort(np.lexsort((-label_origins, distances))[:count])
            anchors = anchors[rows]
            origins = label_origins[rows]
            peak = labels.peak[rows]
            headroom = labels.headroom[rows]
            lower = labels.lower_increment[rows]
            upper = labels.upper_increment[rows]
            # Keep subtract -> order statistic -> add, as in the original S.
            scores_s = np.maximum(current + upper, -current - lower) - B
            core._finite(scores_s, "selected reanchored headrooms")
            if np.any(scores_s < 0):
                raise ValueError("negative selected reanchored headroom")
            capacities = np.array((
                B + core.order_statistic(headroom, rank),
                B + core.order_statistic(scores_s, rank),
                max(B, core.order_statistic(peak, rank)),
            ), dtype=np.float64)
            core._finite(capacities, "selected capacities")
            if np.any(capacities < B):
                raise ValueError("exact selected current-floor violation")
            absolute_radius = float(np.max(np.abs(np.abs(anchors)-B)))
            signed_distances = np.abs(anchors-current)
            signed_radius = float(np.max(signed_distances))
            refined_bound = float(np.max(np.minimum(2*signed_distances, np.abs(upper+lower))))
    except FloatingPointError as exc:
        raise ValueError("nonfinite selected arithmetic") from exc
    tolerance = 64 * core.EPS * max(1., B, float(np.max(np.abs(anchors))),
                                  float(np.max(peak)), float(np.max(capacities)),
                                  absolute_radius, signed_radius)
    F, S, K = map(float, capacities)
    excess = max(0., abs(F - K) - absolute_radius,
                 abs(S - K) - signed_radius,
                 abs(F - S) - absolute_radius - signed_radius,
                 abs(F - S) - refined_bound)
    if excess > tolerance:
        raise ValueError("material selected geometry violation")
    return SelectedForecast(core._readonly(capacities), core._readonly(origins, dtype=np.int64),
                            rank, absolute_radius, signed_radius,
                            core.stable_mean(t - origins), refined_bound, float(tolerance), float(excess))
