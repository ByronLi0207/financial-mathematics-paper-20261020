"""Pure E4 fixed-grid costs for already-issued, matched capacity reports.

No input loading, model selection, estimation, floor recovery or persistence is
performed here.  The input adapter owns exact origin/target/floor matching.
"""
from itertools import product
import math

import numpy as np


def _vector(value, label, n=None):
    raw = np.asarray(value)
    if raw.ndim != 1 or raw.size == 0 or np.iscomplexobj(raw):
        raise ValueError(f"INVALID_VECTOR:{label}")
    a = np.asarray(raw, dtype=float)
    if not np.all(np.isfinite(a)) or (n is not None and len(a) != n):
        raise ValueError(f"NONFINITE_OR_UNMATCHED_VECTOR:{label}")
    return a


def _coefficients(grid):
    values = []
    for name in ("kappa", "beta", "c"):
        a = _vector(grid[name], name)
        if np.any(a < 0):
            raise ValueError(f"NEGATIVE_COEFFICIENT:{name}")
        values.append([float(x) for x in a])
    return values


def evaluate_costs(capacities, target, floor, reference_id, grid,
                   primary_method_id):
    """Return all method/grid costs, or whole-comparison UNAVAILABLE.

    Cost = kappa*mean(C-B)/mF + beta*mean(Y>C)
           + c*mean(max(Y-C,0))/mF, where mF=mean(C_F-B)>0.
    All comparisons and cost ties use exact floating comparisons.  Missing
    primary methods are recorded without replacing the fixed comparator.
    """
    primary_available = primary_method_id in capacities
    unavailable = {
        "status": "UNAVAILABLE", "reason": None, "mean_F_headroom": None,
        "methods": {}, "rows": [], "primary_method_id": primary_method_id,
        "primary_available": bool(primary_available),
    }
    try:
        if not capacities or reference_id not in capacities:
            raise ValueError("ABSENT_REFERENCE")
        if any(not isinstance(k, str) for k in capacities):
            raise ValueError("INVALID_METHOD_ID")
        coefficients = _coefficients(grid)
        y = _vector(target, "target")
        b = _vector(floor, "floor", len(y))
        cs = {k: _vector(capacities[k], k, len(y)) for k in sorted(capacities)}
        if np.any(y < b):
            raise ValueError("TARGET_BELOW_FLOOR")
        if any(np.any(c < b) for c in cs.values()):
            raise ValueError("CAPACITY_BELOW_FLOOR")
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            mf = float(np.mean(cs[reference_id] - b))
            if not math.isfinite(mf) or mf <= 0:
                raise ValueError("NONPOSITIVE_REFERENCE_HEADROOM")
            methods = {}
            for method, c in cs.items():
                reserve = float(np.mean(c - b))
                count = int(np.count_nonzero(y > c))
                excess = float(np.mean(np.maximum(y - c, 0.)))
                stats = {
                    "n": int(len(y)), "mean_headroom": reserve,
                    "normalized_mean_headroom": reserve / mf,
                    "strict_breach_count": count,
                    "strict_breach_rate": count / len(y),
                    "mean_excess": excess, "normalized_mean_excess": excess / mf,
                }
                if any(not math.isfinite(v) for v in stats.values()):
                    raise ValueError("NONFINITE_PRIMITIVE")
                methods[method] = stats
            rows = []
            for kappa, beta, c in product(*coefficients):
                costs = {
                    method: kappa * s["normalized_mean_headroom"]
                    + beta * s["strict_breach_rate"] + c * s["normalized_mean_excess"]
                    for method, s in methods.items()
                }
                ref = costs[reference_id]
                for method, cost in costs.items():
                    difference = cost - ref
                    if not all(math.isfinite(x) for x in (cost, ref, difference)):
                        raise ValueError("NONFINITE_COST")
                    rows.append({
                        "method_id": method, "kappa": kappa, "beta": beta, "c": c,
                        "method_mean": float(cost), "reference_mean": float(ref),
                        "difference": float(difference), "cheaper": difference < 0,
                        "equal": difference == 0,
                    })
    except (ValueError, TypeError, KeyError, OverflowError, FloatingPointError) as exc:
        unavailable["reason"] = str(exc) or type(exc).__name__
        return unavailable
    return {
        "status": "COMPLETE", "reason": None, "mean_F_headroom": mf,
        "methods": methods, "rows": rows, "primary_method_id": primary_method_id,
        "primary_available": bool(primary_available),
    }
