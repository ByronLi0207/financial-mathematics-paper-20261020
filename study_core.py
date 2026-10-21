"""Frozen, source-independent sampled-inventory calculation core.

The pure issuer accepts only an independently supplied current state and an
exact completed-label window. Future peaks enter the separate evaluator.
All public aggregate rows contain only the permitted built-in scalar types.
"""

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Callable, Iterable, Mapping

import numpy as np


METHODS = ("F", "S", "R", "L", "P0")
MECHANISMS = (
    "paired_scores_equal",
    "scores_changed_allowances_equal",
    "allowances_changed_capacities_equal",
    "capacities_different",
)
METHOD_METRICS = (
    "mean_pinball", "mean_capacity", "mean_extra_allowance",
    "strict_breach_count", "strict_breach_rate", "mean_positive_overrun",
    "conditional_mean_overrun", "conditional_overrun_denominator",
    "mean_unused_allowance", "aux_breach_count",
    "strict_aux_disagreement_count", "near_event_boundary_count",
)
EPS = float(np.finfo(np.float64).eps)
Progress = Callable[..., None]


def _integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError("invalid " + name)
    value = int(value)
    if value < minimum:
        raise ValueError("invalid " + name)
    return value


def _vector(values, name, *, nonempty=True):
    out = np.asarray(values, dtype=np.float64)
    if out.ndim != 1 or (nonempty and out.size == 0) or not np.isfinite(out).all():
        raise ValueError("invalid " + name)
    return out


def _indices(values, name, *, nonempty=True):
    out = np.asarray(values)
    if out.ndim != 1 or out.dtype.kind not in "iu" or (nonempty and out.size == 0):
        raise ValueError("invalid " + name)
    if out.size and (np.any(out < 0) or np.any(out[1:] <= out[:-1])):
        raise ValueError("invalid " + name)
    return out


def _readonly(values, dtype=None, *, copy=True):
    out = np.array(values, dtype=dtype, copy=True) if copy else np.asarray(values, dtype=dtype).view()
    out.flags.writeable = False
    return out


def _finite(values, name):
    if not np.isfinite(values).all():
        raise ValueError("nonfinite " + name)


def exact_rank(n, numerator, denominator):
    """The generic exact corrected rank, which may legitimately exceed n."""
    n = _integer(n, "sample size", 1)
    numerator = _integer(numerator, "tau numerator", 1)
    denominator = _integer(denominator, "tau denominator", 2)
    if numerator >= denominator:
        raise ValueError("invalid tau")
    return ((n + 1) * numerator + denominator - 1) // denominator


def order_statistic(values, rank):
    """One-based, noninterpolated selection; unavailable generic rank is +inf."""
    values = _vector(values, "order statistic input")
    rank = _integer(rank, "rank", 1)
    if rank > len(values):
        return math.inf
    return float(np.partition(values, rank - 1)[rank - 1])


@dataclass(frozen=True)
class CellSpec:
    cell_id: str
    horizon: int
    window: int
    tau_numerator: int
    tau_denominator: int
    expected_rank: int

    def __post_init__(self):
        if type(self.cell_id) is not str or not self.cell_id:
            raise ValueError("invalid cell id")
        for name in ("horizon", "window", "tau_numerator", "tau_denominator", "expected_rank"):
            object.__setattr__(self, name, _integer(getattr(self, name), name, 1))
        rank = exact_rank(self.window, self.tau_numerator, self.tau_denominator)
        if rank != self.expected_rank or rank > self.window:
            raise ValueError("configured rank unavailable or inconsistent")

    @classmethod
    def from_dict(cls, value):
        return cls(**{key: value[key] for key in (
            "cell_id", "horizon", "window", "tau_numerator", "tau_denominator", "expected_rank"
        )})

    @property
    def tau(self):
        return Fraction(self.tau_numerator, self.tau_denominator)

    @property
    def rank(self):
        return self.expected_rank


@dataclass(frozen=True)
class LabelCache:
    horizon: int
    origins: np.ndarray
    peak: np.ndarray
    headroom: np.ndarray
    lower_increment: np.ndarray
    upper_increment: np.ndarray
    radius: np.ndarray
    label_end: np.ndarray


@dataclass(frozen=True)
class MatureLabelWindow:
    horizon: int
    window: int
    origins: np.ndarray
    peak: np.ndarray
    headroom: np.ndarray
    lower_increment: np.ndarray
    upper_increment: np.ndarray
    radius: np.ndarray
    label_end: np.ndarray


@dataclass(frozen=True)
class IssuedForecast:
    capacities: np.ndarray
    issued_extras: np.ndarray
    selected_fs: np.ndarray
    mechanism: str
    near_fs_capacity: bool
    current_floor: float


@dataclass(frozen=True)
class ForecastBatch:
    cell_id: str
    origins: np.ndarray
    floors: np.ndarray
    capacities: np.ndarray
    issued_extras: np.ndarray
    selected_fs: np.ndarray
    mechanism: np.ndarray
    near_fs_capacity: np.ndarray


@dataclass(frozen=True)
class EvaluationBatch:
    origins: np.ndarray
    peak: np.ndarray
    errors: np.ndarray
    pinball: np.ndarray
    overrun: np.ndarray
    unused: np.ndarray
    strict_breach: np.ndarray
    aux_breach: np.ndarray
    near_event_boundary: np.ndarray


@dataclass(frozen=True)
class StabilityResult:
    rows: list
    replicate_means: dict
    observed_mean_d: float
    constant_input: bool
    constant_shortcut_used: bool


MAIN_CELL = CellSpec("main", 6, 720, 19, 20, 685)


def _times(values):
    times = np.asarray(values)
    if times.ndim != 1 or times.size == 0 or times.dtype.kind != "M":
        raise ValueError("invalid timestamps")
    times = times.astype("datetime64[us]", copy=False)
    if np.isnat(times).any() or np.any(times[1:] <= times[:-1]):
        raise ValueError("invalid timestamp chronology")
    return times


def common_origins(times, cells, cutoff):
    times = _times(times)
    cells = list(cells)
    if not cells or not all(isinstance(cell, CellSpec) for cell in cells):
        raise ValueError("invalid cell menu")
    cutoff = np.datetime64(cutoff, "us")
    if np.isnat(cutoff):
        raise ValueError("invalid cutoff")
    first = max(int(np.searchsorted(times, cutoff, side="left")), max(c.horizon + c.window - 1 for c in cells))
    last = len(times) - 1 - max(c.horizon for c in cells)
    if first > last:
        raise ValueError("empty common evaluation sample")
    return _readonly(np.arange(first, last + 1, dtype=np.int64))


def _label_geometry(peak, headroom, lower, upper, radius):
    for value in (peak, headroom, lower, upper, radius):
        _finite(value, "label")
    if np.any(peak < 0) or np.any(headroom < 0) or np.any(lower > 0) or np.any(upper < 0) or np.any(radius < 0):
        raise ValueError("exact label sign violation")
    scale = np.maximum(1., np.maximum(headroom, radius))
    if np.any(headroom - radius > 32 * EPS * scale):
        raise ValueError("material historical upper geometry violation")


def build_label_cache(position, H):
    position = _vector(position, "position")
    H = _integer(H, "horizon", 1)
    if len(position) <= H:
        raise ValueError("no complete labels")
    size = len(position) - H
    anchor = position[:size]
    peak = np.abs(anchor).copy()
    lower = np.zeros(size, dtype=np.float64)
    upper = np.zeros(size, dtype=np.float64)
    with np.errstate(over="raise", invalid="raise"):
        for h in range(1, H + 1):
            future = position[h:h + size]
            np.maximum(peak, np.abs(future), out=peak)
            increment = future - anchor
            np.minimum(lower, increment, out=lower)
            np.maximum(upper, increment, out=upper)
        headroom = peak - np.abs(anchor)
        radius = np.maximum(upper, -lower)
    _label_geometry(peak, headroom, lower, upper, radius)
    origins = np.arange(size, dtype=np.int64)
    return LabelCache(H, _readonly(origins), _readonly(peak), _readonly(headroom),
                      _readonly(lower), _readonly(upper), _readonly(radius), _readonly(origins + H))


def mature_window(cache, t, cell):
    t = _integer(t, "actual issue index")
    if cache.horizon != cell.horizon or t < cell.horizon + cell.window - 1:
        raise ValueError("invalid completed-label window")
    first = t - cell.horizon - cell.window + 1
    stop = t - cell.horizon + 1
    if stop > len(cache.origins):
        raise ValueError("completed-label window outside cache")
    names = ("origins", "peak", "headroom", "lower_increment", "upper_increment", "radius", "label_end")
    parts = [_readonly(getattr(cache, name)[first:stop], copy=False) for name in names]
    labels = MatureLabelWindow(cell.horizon, cell.window, *parts)
    _validate_window(t, labels, labels.origins, cell)
    return labels


def _validate_window(t, labels, origins, cell):
    t = _integer(t, "actual issue index")
    if labels.horizon != cell.horizon or labels.window != cell.window or t < cell.horizon + cell.window - 1:
        raise ValueError("completed-label configuration mismatch")
    origins = _indices(origins, "calibration origins")
    label_origins = _indices(labels.origins, "label origins")
    ends = _indices(labels.label_end, "label ends")
    expected = np.arange(t - cell.horizon - cell.window + 1, t - cell.horizon + 1, dtype=np.int64)
    if not np.array_equal(origins, expected) or not np.array_equal(label_origins, expected):
        raise ValueError("exact calibration pool violation")
    if not np.array_equal(ends, expected + cell.horizon) or np.any(ends > t):
        raise ValueError("exact label maturity violation")
    fields = [_vector(getattr(labels, name), "label field") for name in (
        "peak", "headroom", "lower_increment", "upper_increment", "radius"
    )]
    if any(field.shape != (cell.window,) for field in fields):
        raise ValueError("completed-label shape mismatch")
    _label_geometry(*fields)


def _capacity_geometry(capacities, floor):
    _finite(capacities, "capacities")
    if np.any(capacities < floor):
        raise ValueError("exact current-floor violation")
    scale = max(1., float(np.max(capacities)))
    if capacities[0] - capacities[2] > 32 * EPS * scale or capacities[1] - capacities[2] > 32 * EPS * scale:
        raise ValueError("material issued upper geometry violation")


def issue_capacities(t, current, labels, origins, cell):
    """Issue from exactly n completed historical rows; no future/raw array input."""
    _validate_window(t, labels, origins, cell)
    current = float(current)
    if not math.isfinite(current):
        raise ValueError("nonfinite current state")
    B = abs(current)
    with np.errstate(over="raise", invalid="raise"):
        scores_s = np.maximum(current + labels.upper_increment, -current - labels.lower_increment) - B
        _finite(scores_s, "reanchored headrooms")
        if np.any(scores_s < 0):
            raise ValueError("negative reanchored headroom")
        c_f = order_statistic(labels.headroom, cell.rank)
        c_s = order_statistic(scores_s, cell.rank)
        capacities = np.array((B + c_f, B + c_s, B + order_statistic(labels.radius, cell.rank),
                               max(B, order_statistic(labels.peak, cell.rank)), B), dtype=np.float64)
        extras = capacities - B
    _capacity_geometry(capacities, B)
    if np.array_equal(labels.headroom, scores_s):
        if c_f != c_s or capacities[0] != capacities[1]:
            raise ValueError("canonical score equality implication violation")
        mechanism = MECHANISMS[0]
    elif c_f == c_s:
        if capacities[0] != capacities[1]:
            raise ValueError("canonical allowance equality implication violation")
        mechanism = MECHANISMS[1]
    elif capacities[0] == capacities[1]:
        mechanism = MECHANISMS[2]
    else:
        mechanism = MECHANISMS[3]
    near = bool(abs(float(capacities[0]) - float(capacities[1])) <= 32 * EPS * max(1., float(capacities[0]), float(capacities[1])))
    return IssuedForecast(_readonly(capacities), _readonly(extras), _readonly([c_f, c_s]), mechanism, near, float(B))


def forecast_cell(position, cache, origins, cell, checkpoint=None):
    position = _vector(position, "position")
    origins = _indices(origins, "issue origins")
    if cache.horizon != cell.horizon or len(cache.peak) + cell.horizon != len(position) or int(origins[-1]) >= len(position):
        raise ValueError("forecast source/cache alignment violation")
    M = len(origins)
    capacities = np.empty((M, 5), dtype=np.float64)
    extras = np.empty((M, 5), dtype=np.float64)
    selected = np.empty((M, 2), dtype=np.float64)
    mechanisms = np.empty(M, dtype="U40")
    near = np.empty(M, dtype=bool)
    floors = np.abs(position[origins])
    for j, origin in enumerate(origins):
        t = int(origin)
        labels = mature_window(cache, t, cell)
        issued = issue_capacities(t, float(position[t]), labels, labels.origins, cell)
        capacities[j], extras[j], selected[j] = issued.capacities, issued.issued_extras, issued.selected_fs
        mechanisms[j], near[j] = issued.mechanism, issued.near_fs_capacity
        if checkpoint is not None and (j + 1) % 100 == 0:
            checkpoint(stage="forecast", cell_id=cell.cell_id, completed_origins=int(j + 1))
    if checkpoint is not None and M % 100:
        checkpoint(stage="forecast", cell_id=cell.cell_id, completed_origins=int(M))
    return ForecastBatch(cell.cell_id, _readonly(origins), _readonly(floors), _readonly(capacities),
                         _readonly(extras), _readonly(selected), _readonly(mechanisms), _readonly(near))


def _tau_fraction(tau):
    if isinstance(tau, CellSpec):
        tau = tau.tau
    if isinstance(tau, tuple) and len(tau) == 2:
        tau = Fraction(*tau)
    if not isinstance(tau, Fraction) or not 0 < tau < 1:
        raise ValueError("evaluation requires an exact rational tau")
    return tau


def evaluate_caps(peak, caps, tau, *, origins=None):
    """Evaluate stored peak minus stored capacity, preserving explicit origins.

    Production callers pass a ForecastBatch. Array-only unit callers can pass
    explicit origins; absent those, the synthetic row positions are used.
    """
    if isinstance(caps, ForecastBatch):
        if origins is not None and not np.array_equal(origins, caps.origins):
            raise ValueError("evaluation origin override mismatch")
        origins = caps.origins
        caps = caps.capacities
    peak = _vector(peak, "evaluation peak")
    caps = np.asarray(caps, dtype=np.float64)
    if caps.shape != (len(peak), 5) or not np.isfinite(caps).all() or np.any(caps < 0) or np.any(peak < 0):
        raise ValueError("invalid evaluation capacities")
    origins = np.arange(len(peak), dtype=np.int64) if origins is None else _indices(origins, "evaluation origins")
    if origins.shape != peak.shape:
        raise ValueError("evaluation origin shape mismatch")
    tau = _tau_fraction(tau)
    with np.errstate(over="raise", invalid="raise"):
        errors = peak[:, None] - caps
        overrun = np.maximum(errors, 0.)
        unused = np.maximum(-errors, 0.)
        pinball = float(tau) * overrun + float(1 - tau) * unused
    for values in (errors, overrun, unused, pinball):
        _finite(values, "evaluation result")
    scale = np.maximum(1., np.maximum(peak, np.max(caps, axis=1)))
    tol = 32 * EPS * scale[:, None]
    strict = errors > 0
    aux = errors > tol
    near = np.abs(errors) <= tol
    return EvaluationBatch(_readonly(origins), _readonly(peak), _readonly(errors), _readonly(pinball),
                           _readonly(overrun), _readonly(unused), _readonly(strict), _readonly(aux), _readonly(near))


def stable_mean(values):
    """Preserve a stored exact constant; otherwise use the specified fsum/M."""
    values = _vector(values, "required mean input")
    if np.all(values == values[0]):
        return float(values[0])
    value = math.fsum(float(x) for x in values) / len(values)
    if not math.isfinite(value):
        raise ValueError("nonfinite aggregate mean")
    return float(value)


def _arithmetic_tolerance(M, scale):
    q_eps = (2 * int(M) + 2) * EPS
    if q_eps >= 1 or not math.isfinite(float(scale)):
        raise ValueError("arithmetic tolerance unavailable")
    return 8 * q_eps / (1 - q_eps) * max(1., float(scale))


def _assert_mean_equal(left, right, M, scale):
    if not math.isfinite(left) or not math.isfinite(right) or abs(left - right) > _arithmetic_tolerance(M, scale):
        raise ValueError("aggregate arithmetic reconciliation failure")


def _prefix(cell, M):
    return dict(cell_id=cell.cell_id, horizon=int(cell.horizon), window=int(cell.window),
                tau_numerator=int(cell.tau_numerator), tau_denominator=int(cell.tau_denominator),
                rank=int(cell.rank), origin_count=int(M))


def _validate_aligned(cell, batch, evaluation):
    origins = _indices(batch.origins, "batch origins")
    M = len(origins)
    if batch.cell_id != cell.cell_id or not np.array_equal(evaluation.origins, origins):
        raise ValueError("cell/evaluation alignment violation")
    if batch.floors.shape != (M,) or batch.capacities.shape != (M, 5) or batch.issued_extras.shape != (M, 5) or batch.selected_fs.shape != (M, 2):
        raise ValueError("forecast batch shape violation")
    if batch.mechanism.shape != (M,) or batch.near_fs_capacity.shape != (M,) or evaluation.peak.shape != (M,):
        raise ValueError("batch metadata shape violation")
    for name in ("errors", "pinball", "overrun", "unused", "strict_breach", "aux_breach", "near_event_boundary"):
        values = getattr(evaluation, name)
        if values.shape != (M, 5):
            raise ValueError("evaluation batch shape violation")
        _finite(values, "evaluation batch")
    for values in (batch.floors, batch.capacities, batch.issued_extras, batch.selected_fs, evaluation.peak):
        _finite(values, "aligned batch")
    if np.any(batch.capacities < batch.floors[:, None]) or np.any(batch.floors < 0):
        raise ValueError("exact batch floor violation")
    if not np.array_equal(batch.issued_extras, batch.capacities - batch.floors[:, None]):
        raise ValueError("issued extras do not match stored capacities")
    if not np.isin(batch.mechanism, MECHANISMS).all():
        raise ValueError("unknown mechanism category")
    cap_equal = batch.capacities[:, 0] == batch.capacities[:, 1]
    if not np.array_equal(cap_equal, batch.mechanism != MECHANISMS[3]):
        raise ValueError("mechanism capacity partition violation")
    if np.any(evaluation.aux_breach & ~evaluation.strict_breach):
        raise ValueError("auxiliary breach subset violation")
    return M


def _method_metrics(batch, evaluation, j, mask):
    count = int(np.count_nonzero(mask))
    if count == 0:
        raise ValueError("empty required method aggregate")
    raw = evaluation.strict_breach[mask, j]
    overrun = evaluation.overrun[mask, j]
    breaches = int(np.count_nonzero(raw))
    conditional = float(math.fsum(float(x) for x in overrun) / breaches) if breaches else None
    if conditional is not None and not math.isfinite(conditional):
        raise ValueError("nonfinite conditional severity")
    return dict(
        mean_pinball=stable_mean(evaluation.pinball[mask, j]),
        mean_capacity=stable_mean(batch.capacities[mask, j]),
        mean_extra_allowance=stable_mean(batch.issued_extras[mask, j]),
        strict_breach_count=breaches,
        strict_breach_rate=float(breaches / count),
        mean_positive_overrun=stable_mean(overrun),
        conditional_mean_overrun=conditional,
        conditional_overrun_denominator=breaches,
        mean_unused_allowance=stable_mean(evaluation.unused[mask, j]),
        aux_breach_count=int(np.count_nonzero(evaluation.aux_breach[mask, j])),
        strict_aux_disagreement_count=int(np.count_nonzero(raw != evaluation.aux_breach[mask, j])),
        near_event_boundary_count=int(np.count_nonzero(evaluation.near_event_boundary[mask, j])),
    )


def summarize_cell(cell, batch, evaluation):
    M = _validate_aligned(cell, batch, evaluation)
    mask = np.ones(M, dtype=bool)
    rows = []
    for j, method in enumerate(METHODS):
        metrics = _method_metrics(batch, evaluation, j, mask)
        row = _prefix(cell, M)
        row.update(method_id=method, **metrics)
        row["conditional_overrun_undefined_reason"] = "NO_STRICT_BREACHES" if metrics["strict_breach_count"] == 0 else None
        rows.append(row)
    with np.errstate(over="raise", invalid="raise"):
        d = evaluation.pinball[:, 0] - evaluation.pinball[:, 1]
    mean_d = stable_mean(d)
    _assert_mean_equal(mean_d, rows[0]["mean_pinball"] - rows[1]["mean_pinball"], M,
                       float(np.max(np.abs(evaluation.pinball[:, :2]))))
    loss_s = rows[1]["mean_pinball"]
    relative = float(mean_d / loss_s) if loss_s > 0 else None
    if relative is not None and not math.isfinite(relative):
        raise ValueError("nonfinite relative difference")
    lower = int(np.count_nonzero(batch.capacities[:, 0] < batch.capacities[:, 1]))
    equal = int(np.count_nonzero(batch.capacities[:, 0] == batch.capacities[:, 1]))
    higher = int(np.count_nonzero(batch.capacities[:, 0] > batch.capacities[:, 1]))
    counts = [int(np.count_nonzero(batch.mechanism == name)) for name in MECHANISMS]
    if lower + equal + higher != M or sum(counts) != M or equal != sum(counts[:3]) or counts[3] != lower + higher:
        raise ValueError("mechanism partition reconciliation failure")
    near = int(np.count_nonzero(batch.near_fs_capacity))
    paired = _prefix(cell, M)
    paired.update(
        mean_pinball_difference=mean_d, relative_difference_to_S=relative,
        relative_difference_undefined_reason="ZERO_MEAN_LOSS_S" if loss_s == 0 else None,
        f_lower_count=lower, equal_capacity_count=equal, f_higher_count=higher,
        f_lower_fraction=float(lower / M), equal_capacity_fraction=float(equal / M), f_higher_fraction=float(higher / M),
        near_fs_capacity_count=near, near_fs_capacity_fraction=float(near / M),
    )
    paired.update({name + "_count": count for name, count in zip(MECHANISMS, counts)})
    return rows, paired


def _reconcile_groups(groups, global_metrics, global_d, batch, evaluation):
    M = len(global_d)
    if sum(count for _, _, count, _, _ in groups) != M:
        raise ValueError("diagnostic panel count mismatch")
    memberships = np.zeros(M, dtype=np.int8)
    for _, mask, _, _, _ in groups:
        memberships += mask
    if np.any(memberships != 1):
        raise ValueError("diagnostic groups do not partition origins")
    weighted_d = math.fsum(count * paired for _, _, count, _, paired in groups if count) / M
    _assert_mean_equal(weighted_d, stable_mean(global_d), M, float(np.max(np.abs(global_d))))
    mean_inputs = {
        "mean_pinball": evaluation.pinball,
        "mean_capacity": batch.capacities,
        "mean_extra_allowance": batch.issued_extras,
        "strict_breach_rate": evaluation.strict_breach,
        "mean_positive_overrun": evaluation.overrun,
        "mean_unused_allowance": evaluation.unused,
    }
    count_keys = ("strict_breach_count", "conditional_overrun_denominator", "aux_breach_count",
                  "strict_aux_disagreement_count", "near_event_boundary_count")
    for j in range(5):
        for key, inputs in mean_inputs.items():
            weighted = math.fsum(count * metrics[j][key] for _, _, count, metrics, _ in groups if count) / M
            _assert_mean_equal(weighted, global_metrics[j][key], M, float(np.max(np.abs(inputs[:, j]))))
        for key in count_keys:
            if sum(metrics[j][key] for _, _, count, metrics, _ in groups if count) != global_metrics[j][key]:
                raise ValueError("diagnostic event count reconciliation failure")
        breaches = global_metrics[j]["strict_breach_count"]
        if breaches:
            weighted = math.fsum(metrics[j]["strict_breach_count"] * metrics[j]["conditional_mean_overrun"]
                                 for _, _, count, metrics, _ in groups if count and metrics[j]["strict_breach_count"]) / breaches
            _assert_mean_equal(weighted, global_metrics[j]["conditional_mean_overrun"], M,
                               float(np.max(np.abs(evaluation.overrun[:, j]))))


def diagnostics_main(times, position, origins, cell, batch, evaluation, cutoff):
    M = _validate_aligned(cell, batch, evaluation)
    if cell.cell_id != "main":
        raise ValueError("diagnostics are primary only")
    times = _times(times)
    position = _vector(position, "diagnostic position")
    origins = _indices(origins, "diagnostic origins")
    if len(position) != len(times) or not np.array_equal(origins, batch.origins) or int(origins[-1]) + cell.horizon >= len(times):
        raise ValueError("diagnostic source/origin alignment violation")
    development = np.abs(position[times < np.datetime64(cutoff, "us")])
    if development.size == 0:
        raise ValueError("empty development-state set")
    q1 = order_statistic(development, (len(development) + 2) // 3)
    q2 = order_statistic(development, (2 * len(development) + 2) // 3)
    current = position[origins]
    magnitude = np.abs(current)
    panels = [
        ("current_sign", [("negative", current < 0), ("zero", current == 0), ("positive", current > 0)]),
        ("development_magnitude_tercile", [("low", magnitude <= q1), ("middle", (magnitude > q1) & (magnitude <= q2)), ("high", magnitude > q2)]),
        ("source_index_modulo_6", [(str(j), origins % 6 == j) for j in range(6)]),
    ]
    origin_month = times[origins].astype("datetime64[M]")
    month_first = int(origin_month[0].astype(np.int64))
    month_last = int(origin_month[-1].astype(np.int64))
    months = [(str(np.datetime64(j, "M")), origin_month == np.datetime64(j, "M")) for j in range(month_first, month_last + 1)]
    panels.append(("naive_origin_month", months))
    gap_free = np.ones(M, dtype=bool)
    hour = np.timedelta64(1, "h")
    for h in range(cell.horizon):
        gap_free &= times[origins + h + 1] - times[origins + h] == hour
    panels.append(("retrospective_gap_free_path", [("gap_free", gap_free), ("has_gap", ~gap_free)]))
    all_mask = np.ones(M, dtype=bool)
    global_metrics = [_method_metrics(batch, evaluation, j, all_mask) for j in range(5)]
    d = evaluation.pinball[:, 0] - evaluation.pinball[:, 1]
    rows = []
    for panel, definitions in panels:
        groups = []
        for name, mask in definitions:
            count = int(np.count_nonzero(mask))
            metrics = [_method_metrics(batch, evaluation, j, mask) for j in range(5)] if count else None
            paired = stable_mean(d[mask]) if count else None
            groups.append((name, mask, count, metrics, paired))
        # All arithmetic checks use the private unsuppressed metrics.
        _reconcile_groups(groups, global_metrics, d, batch, evaluation)
        for name, _, count, metrics, paired in groups:
            status = "DISPLAYED" if count >= 30 else "BELOW_DISPLAY_MIN" if count else "NO_ORIGINS"
            suppressed_reason = "GROUP_BELOW_DISPLAY_MIN" if count else "NO_ORIGINS"
            for j, method in enumerate(METHODS):
                for metric in METHOD_METRICS:
                    value = metrics[j][metric] if count >= 30 else None
                    reason = ("NO_STRICT_BREACHES" if metric == "conditional_mean_overrun" and value is None else None) if count >= 30 else suppressed_reason
                    rows.append(dict(cell_id=cell.cell_id, panel=panel, group=name, method_or_comparison=method,
                                     metric=metric, origin_count=count, display_status=status, value=value, undefined_reason=reason))
            rows.append(dict(cell_id=cell.cell_id, panel=panel, group=name, method_or_comparison="F_MINUS_S",
                             metric="mean_pinball_difference", origin_count=count, display_status=status,
                             value=paired if count >= 30 else None, undefined_reason=None if count >= 30 else suppressed_reason))
    return rows


def explicit_block_mean(d, blocks: Iterable[tuple], *, route="slices"):
    """Consume an explicit circular block trace, truncating only its last block.

    The production slice route uses one or two float64 slice sums per used
    block and fsum combines those segment totals. The index route is an
    independent small artificial arithmetic oracle, never a production tensor.
    """
    d = _vector(d, "block input")
    if route not in ("slices", "indices"):
        raise ValueError("unknown block arithmetic route")
    M = len(d)
    remaining = M
    parts = []
    direct = []
    for pair in blocks:
        if remaining == 0:
            break
        if len(pair) != 2:
            raise ValueError("invalid explicit block")
        start = _integer(pair[0], "block start")
        length = _integer(pair[1], "block length", 1)
        if start >= M:
            raise ValueError("block start outside vector")
        used = min(length, remaining)
        if route == "indices":
            direct.extend(float(d[(start + offset) % M]) for offset in range(used))
        else:
            first = min(used, M - start)
            with np.errstate(over="raise", invalid="raise"):
                parts.append(float(np.sum(d[start:start + first], dtype=np.float64)))
                if used > first:
                    parts.append(float(np.sum(d[:used - first], dtype=np.float64)))
        remaining -= used
        if remaining == 0:
            break
    if remaining:
        raise ValueError("explicit blocks do not fill resample")
    mean = math.fsum(direct if route == "indices" else parts) / M
    if not math.isfinite(mean):
        raise ValueError("nonfinite block mean")
    return float(mean)


def check_explicit_block_equivalence(d, blocks):
    d = _vector(d, "equivalence input")
    blocks = list(blocks)
    left = explicit_block_mean(d, blocks, route="slices")
    right = explicit_block_mean(d, blocks, route="indices")
    _assert_mean_equal(left, right, len(d), float(np.max(np.abs(d))))
    return True


def stationary_replicate(d, ell, rng):
    """Draw start then positive geometric length, continuing one RNG stream."""
    d = _vector(d, "stationary input")
    ell = _integer(ell, "block length parameter", 1)
    def blocks():
        while True:
            start = rng.integers(0, len(d))
            length = rng.geometric(1 / ell)
            yield start, length
    return explicit_block_mean(d, blocks(), route="slices")


def summarize_replicates(means, observed_mean):
    means = _vector(means, "replicate means")
    if len(means) < 2 or not math.isfinite(float(observed_mean)):
        raise ValueError("invalid replicate summary input")
    R = len(means)
    lower_rank = (R + 39) // 40
    upper_rank = (39 * R + 39) // 40
    average = stable_mean(means)
    if np.all(means == means[0]):
        sd = 0.
    else:
        variance = math.fsum((float(x) - average) ** 2 for x in means) / (R - 1)
        sd = math.sqrt(variance)
    if not math.isfinite(sd):
        raise ValueError("nonfinite replicate spread")
    return dict(observed_mean_d=float(observed_mean), resampled_mean_average=average,
                resampled_mean_sd_ddof1=float(sd), resampled_mean_order25=order_statistic(means, lower_rank),
                resampled_mean_order975=order_statistic(means, upper_rank),
                lower_rank=int(lower_rank), upper_rank=int(upper_rank))


def stationary_mean_profile(d, lengths=(120, 240, 720, 1440), reps=999, base_seed=20261020, checkpoint=None, *, cell=MAIN_CELL):
    d = _vector(d, "paired contrast")
    lengths = [_integer(ell, "block length parameter", 1) for ell in lengths]
    reps = _integer(reps, "replicate count", 2)
    base_seed = _integer(base_seed, "base seed")
    if not lengths or len(set(lengths)) != len(lengths):
        raise ValueError("invalid stability length menu")
    observed = stable_mean(d)
    constant = bool(np.all(d == d[0]))
    rows, private = [], {}
    for ell in lengths:
        if constant:
            means = np.full(reps, float(d[0]), dtype=np.float64)
            if checkpoint is not None:
                for completed in range(50, reps, 50):
                    checkpoint(stage="stability", length=int(ell), completed_replicates=int(completed))
        else:
            rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([base_seed, ell])))
            means = np.empty(reps, dtype=np.float64)
            for j in range(reps):
                means[j] = stationary_replicate(d, ell, rng)
                if checkpoint is not None and (j + 1) % 50 == 0:
                    checkpoint(stage="stability", length=int(ell), completed_replicates=int(j + 1))
        row = _prefix(cell, len(d))
        row.update(ell=int(ell), ell_over_origin_count=float(ell / len(d)), replicates=int(reps),
                   expected_used_blocks=float(1 + (len(d) - 1) / ell), **summarize_replicates(means, observed),
                   generator="PCG64", seed_base=int(base_seed), seed_length=int(ell),
                   constant_input=constant, constant_shortcut_used=constant)
        rows.append(row)
        private[ell] = _readonly(means)
        if checkpoint is not None:
            checkpoint(stage="stability", length=int(ell), completed_replicates=int(reps))
    return StabilityResult(rows, private, float(observed), constant, constant)


def validate_cross_cells(mapping: Mapping):
    """Validate {cell_id: (CellSpec, ForecastBatch, EvaluationBatch, LabelCache)}.

    The mapping must contain the seven frozen cell ids. All comparisons use
    shared original issue indices. No F/S/R horizon or window ordering and no
    conditional-severity or auxiliary-flag horizon ordering is imposed.
    """
    ids = ("main", "h12", "h24", "n480", "n1440", "tau90", "tau99")
    if set(mapping) != set(ids):
        raise ValueError("cross-cell menu mismatch")
    reference = mapping["main"][1]
    for key in ids:
        cell, batch, evaluation, cache = mapping[key]
        _validate_aligned(cell, batch, evaluation)
        if key != cell.cell_id or cache.horizon != cell.horizon or not np.array_equal(batch.origins, reference.origins) or not np.array_equal(batch.floors, reference.floors):
            raise ValueError("cross-cell original-index alignment violation")
        if int(batch.origins[-1]) >= len(cache.peak) or not np.array_equal(evaluation.peak, cache.peak[batch.origins]):
            raise ValueError("cross-cell target/cache mismatch")
        if np.any(evaluation.peak < batch.floors) or not np.array_equal(batch.capacities[:, 4], batch.floors) or np.any(batch.issued_extras[:, 4] != 0) or np.any(evaluation.unused[:, 4] != 0):
            raise ValueError("P0 floor identity violation")
        if not np.array_equal(evaluation.errors[:, 4], evaluation.peak - batch.floors) or not np.array_equal(evaluation.overrun[:, 4], evaluation.errors[:, 4]):
            raise ValueError("P0 raw error identity violation")
    for left_id, right_id in (("tau90", "main"), ("main", "tau99")):
        if np.any(mapping[left_id][1].capacities > mapping[right_id][1].capacities):
            raise ValueError("tau capacity order violation")
    for i, left_id in enumerate(ids):
        left_cell, left_batch, left, _ = mapping[left_id]
        for right_id in ids[i + 1:]:
            right_cell, right_batch, right, _ = mapping[right_id]
            if left_cell.horizon == right_cell.horizon:
                for a, b in ((left.peak, right.peak), (left.peak - left_batch.floors, right.peak - right_batch.floors),
                             (left.errors[:, 4], right.errors[:, 4]), (left.overrun[:, 4], right.overrun[:, 4]),
                             (left.strict_breach[:, 4], right.strict_breach[:, 4])):
                    if not np.array_equal(a, b):
                        raise ValueError("same-horizon target or P0 mismatch")
                if left_cell.tau == right_cell.tau and not np.array_equal(left.pinball[:, 4], right.pinball[:, 4]):
                    raise ValueError("same-horizon same-tau P0 score mismatch")
    for left_id, right_id in (("main", "h12"), ("h12", "h24")):
        _, left_batch, left, _ = mapping[left_id]
        _, right_batch, right, _ = mapping[right_id]
        if np.any(left.peak > right.peak) or np.any(left.peak - left_batch.floors > right.peak - right_batch.floors):
            raise ValueError("future target horizon order violation")
        if np.any(left_batch.capacities[:, 3] > right_batch.capacities[:, 3]):
            raise ValueError("L horizon order violation")
        for name in ("errors", "overrun", "strict_breach", "pinball"):
            if np.any(getattr(left, name)[:, 4] > getattr(right, name)[:, 4]):
                raise ValueError("P0 raw horizon order violation")
    return True
