"""Exact preference sensitivity for a finite set of fixed reported actions.

For components U = mean positive overrun and V = mean unused allowance,
the loss is L_alpha = alpha U + (1-alpha) V. This module reweights supplied
components. It fits no new quantiles, and says nothing about dominance over
all quantile-consistent scoring functions. Results are exact for the supplied
decimal tokens, which may themselves be rounded reports of original data.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import re
from typing import Mapping


_DECIMAL = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def parse_nonnegative_decimal(token: object) -> Fraction:
    """Parse a finite decimal string, integer, or exact Fraction.

    Binary floats, booleans, nonfinite values, rational strings and negative
    values are rejected. Scientific decimal notation and surrounding spaces
    are accepted; no float conversion or decimal rounding is performed.
    """
    if isinstance(token, bool):
        raise TypeError("A boolean is not a loss component")
    if isinstance(token, (int, Fraction)):
        value = Fraction(token)
    elif isinstance(token, str):
        clean = token.strip()
        if not _DECIMAL.fullmatch(clean):
            raise ValueError("Expected a finite decimal token")
        value = Fraction(clean)
    else:
        raise TypeError("Expected a decimal string, integer, or Fraction")
    if value < 0:
        raise ValueError("Loss components must be nonnegative")
    return value


@dataclass(frozen=True)
class LossComponents:
    mean_positive_overrun: Fraction
    mean_unused_allowance: Fraction

    def __post_init__(self):
        for name in ("mean_positive_overrun", "mean_unused_allowance"):
            object.__setattr__(self, name, parse_nonnegative_decimal(getattr(self, name)))

    @classmethod
    def from_tokens(cls, overrun: object, unused: object) -> "LossComponents":
        return cls(overrun, unused)


@dataclass(frozen=True)
class Comparison:
    """Weak component dominance or crossing within [0,1].

    A dominance relation is strict for at least one component; it can still
    tie at one endpoint. equality_alpha is that unique equality in [0,1],
    including endpoints, or None for no equality or identical entire lines.
    """
    relation: str
    equality_alpha: Fraction | None


@dataclass(frozen=True)
class Region:
    """Methods minimizing loss on the open interval (left, right)."""
    left: Fraction
    right: Fraction
    methods: tuple[str, ...]


@dataclass(frozen=True)
class Point:
    """All minimizers at one endpoint or frontier change point."""
    alpha: Fraction
    methods: tuple[str, ...]


@dataclass(frozen=True)
class Frontier:
    regions: tuple[Region, ...]
    points: tuple[Point, ...]


def mean_loss(record: LossComponents, alpha: Fraction | int) -> Fraction:
    """Evaluate a fixed record at an exact alpha in the closed unit interval."""
    if isinstance(alpha, bool) or not isinstance(alpha, (int, Fraction)):
        raise TypeError("alpha must be an exact Fraction or integer")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0,1]")
    return alpha * record.mean_positive_overrun + (1 - alpha) * record.mean_unused_allowance


def compare_records(left: LossComponents, right: LossComponents) -> Comparison:
    """Compare fixed mean-loss lines, retaining any unique endpoint equality."""
    delta_u = left.mean_positive_overrun - right.mean_positive_overrun
    delta_v = left.mean_unused_allowance - right.mean_unused_allowance
    if delta_u == delta_v == 0:
        return Comparison("identical", None)
    slope = delta_u - delta_v
    equality = -delta_v / slope if slope else None
    if equality is not None and not 0 <= equality <= 1:
        equality = None
    if delta_u <= 0 and delta_v <= 0:
        relation = "left_dominates"
    elif delta_u >= 0 and delta_v >= 0:
        relation = "right_dominates"
    else:
        relation = "crosses"
    return Comparison(relation, equality)


def lower_envelope(records: Mapping[str, LossComponents]) -> Frontier:
    """Return the exact lower envelope for a nonempty finite method set.

    All pairwise interior crossings partition [0,1]. On each open cell,
    affine ordering is constant, so its exact midpoint identifies all
    minimizers. Nonfrontier crossings are then merged away. The separate
    point results preserve every tie at frontier changes and both endpoints,
    including methods optimal only at a point. Method names are sorted.
    """
    if not records:
        raise ValueError("At least one method is required")
    if any(not isinstance(name, str) or not name for name in records):
        raise ValueError("Method names must be nonempty strings")
    if any(not isinstance(record, LossComponents) for record in records.values()):
        raise TypeError("Every method must supply LossComponents")
    names = tuple(sorted(records))

    def winners(alpha):
        losses = {name: mean_loss(records[name], alpha) for name in names}
        minimum = min(losses.values())
        return tuple(name for name in names if losses[name] == minimum)

    breaks = {Fraction(0), Fraction(1)}
    for left, right in combinations(names, 2):
        equality = compare_records(records[left], records[right]).equality_alpha
        if equality is not None:
            breaks.add(equality)
    boundaries = sorted(breaks)
    regions = []
    for left, right in zip(boundaries, boundaries[1:]):
        methods = winners((left + right) / 2)
        if regions and regions[-1].methods == methods and winners(left) == methods:
            regions[-1] = Region(regions[-1].left, right, methods)
        else:
            regions.append(Region(left, right, methods))
    retained = [regions[0].left] + [region.right for region in regions]
    points = tuple(Point(alpha, winners(alpha)) for alpha in retained)
    return Frontier(tuple(regions), points)
