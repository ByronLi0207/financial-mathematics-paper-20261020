"""Exact fixed-terminal one-sided Bernoulli coverage evidence.

Mature likelihood-ratio mixtures and delayed phase averages; see the scoped
coverage-evalue design. No financial input, prediction or file is accessed.
This kernel provides no full-filtration anytime guarantee or coverage PASS.
"""
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
import math


MAX_OBSERVATIONS = 10000
MAX_HORIZON = 1000
DEFAULT_ALPHA = Fraction(1, 20)


def _integer(value, name, lower, upper):
    if type(value) is not int or not lower <= value <= upper:
        raise ValueError(f'invalid {name}')
    return value


def mixture_evalue(n, k, alpha=DEFAULT_ALPHA):
    """Uniform-[alpha,1] whole-product mixture, as an exact positive sum.

    n and k are counts, never a declaration that the observations are iid.
    The probabilistic validity requires the causal conditional upper-bound
    null and maturity in the design, not just these integers.
    """
    _integer(n, 'observation count', 0, MAX_OBSERVATIONS)
    _integer(k, 'breach count', 0, n)
    if not isinstance(alpha, Fraction) or not 0 < alpha < 1:
        raise ValueError('alpha must be a Fraction strictly between0 and1')
    ratio = (1-alpha)/alpha
    term = Fraction(1, n-k+1)
    result = term
    for j in range(k):
        term *= Fraction(k-j, n-k+j+2) * ratio
        result += term
    return result


@dataclass(frozen=True)
class PhaseValue:
    phase: int
    n: int
    k: int
    value: Fraction


@dataclass(frozen=True)
class PhaseMixture:
    horizon: int
    first_origin: int
    last_origin: int
    n: int
    k: int
    phases: tuple[PhaseValue, ...]
    value: Fraction


def phase_mixture(origins, hits, horizon):
    """Average every H+1 phase exactly, anchored to the first actual origin.

    Reject malformed order instead of sorting or dropping entries. Gaps in
    recorded indices are allowed here; a financial caller must additionally
    enforce its own complete declared origin inventory and label maturity.
    """
    _integer(horizon, 'horizon', 1, MAX_HORIZON)
    try:
        origin_values, hit_values = tuple(origins), tuple(hits)
    except TypeError as exc:
        raise ValueError('origins and hits must be finite sequences') from exc
    n = len(origin_values)
    _integer(n, 'observation count', 1, MAX_OBSERVATIONS)
    if len(hit_values) != n:
        raise ValueError('origin/hit lengths differ')
    previous = -1
    for t in origin_values:
        _integer(t, 'record origin', 0, (1 << 63)-1)
        if t <= previous:
            raise ValueError('record origins must be strictly increasing')
        previous = t
    for bit in hit_values:
        if type(bit) not in (int, bool) or bit not in (0, 1):
            raise ValueError('hits must contain only bool or integer0/1')
    spacing = horizon+1
    counts, breaches = [0]*spacing, [0]*spacing
    first = origin_values[0]
    for t, bit in zip(origin_values, hit_values):
        phase = (t-first) % spacing
        counts[phase] += 1
        breaches[phase] += int(bit)
    phases = tuple(PhaseValue(r, counts[r], breaches[r],
                              mixture_evalue(counts[r], breaches[r]))
                   for r in range(spacing))
    value = sum((p.value for p in phases), Fraction()) / spacing
    return PhaseMixture(horizon, first, origin_values[-1], n,
                        sum(breaches), phases, value)


def fraction_fields(value):
    """Exact serialized identity plus approximate display-only labels.

    Hexadecimal integers avoid Python's decimal-int conversion digit cap.
    Neither rounded display nor log label may decide an evidence threshold.
    """
    if not isinstance(value, Fraction) or value <= 0:
        raise ValueError('a positive Fraction is required')
    with localcontext() as context:
        context.prec = 17
        context.Emax = 999999999
        context.Emin = -999999999
        decimal_value = Decimal(value.numerator)/Decimal(value.denominator)
        display = format(decimal_value, '.12E')
    log10_approx = math.log10(value.numerator)-math.log10(value.denominator)
    if not math.isfinite(log10_approx):
        raise ValueError('nonfinite approximate log label')
    return {'numerator_hex': hex(value.numerator),
            'denominator_hex': hex(value.denominator),
            'log10_approx': log10_approx, 'display': display}
