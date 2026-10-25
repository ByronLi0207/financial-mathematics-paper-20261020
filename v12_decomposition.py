"""Pure arithmetic for the frozen F1 fixed-menu diagnostic.

Scientific authority: protocol/v12/loss-decomposition-design.md.  This module
does no fitting, file access, acquisition, statistical testing, or loss pooling.
The finite-menu evaluation oracle is retrospective and optimistic; its gap is
not a conclusion about every possible conditional signal.
"""

from collections import Counter, defaultdict
from collections.abc import Mapping
from math import fsum, isfinite
from numbers import Integral, Real
from statistics import median


MENU = (0.001, 0.01, 0.1, 1.0, 10.0, "inf")
METHODS = ("QR33", "QR4")
CFTC_SOURCE_KEYS = (
    "044601", "043602", "042601", "045601", "020601", "099741", "1170E1",
    "097741", "096742", "095741", "090741", "232741", "33874A", "240743",
    "092741", "098662", "112741",
)
PANEL_SOURCE_KEYS = (
    "PDPOSCS-TOT", "PDPOSFGS-TOT", "PDPOSGSC-G2L3", "PDPOSGSC-G3L6",
    "PDPOSGSC-G6L7", "PDPOSGSC-G7L11", "PDPOSGSC-L2", "PDPOSMBS-TOT",
    "PDPOSTIPS-G11", "PDPOSTIPS-G2", "PDPOSTIPS-G6L11", "PDPOSTIPS-L2",
)
COMPONENTS = ("actual_excess_pct", "selection_component_pct", "signal_gap_pct")
_GEOMETRIES = (
    ("cftc", (6,), (52, 260), 17),
    ("panel", (6, 24), (52, 260), 12),
    ("bill", (6, 24), (52, 260), 1),
    ("fx", (6, 24), (720, 2880), 1),
)


def _finite_number(value):
    return isinstance(value, Real) and not isinstance(value, bool) and isfinite(value)


def _positive_integer(value):
    return isinstance(value, Integral) and not isinstance(value, bool) and value > 0


def _penalty_index(value):
    if not ((isinstance(value, Real) and not isinstance(value, bool)) or
            (isinstance(value, str) and value == "inf")):
        return None
    for index, penalty in enumerate(MENU):
        if value == penalty:
            return index
    return None


def _validate_candidates(candidates, expected_n=None):
    if not isinstance(candidates, (list, tuple)) or len(candidates) != len(MENU):
        return "Exactly six ordered menu candidates are required."
    if expected_n is not None and not _positive_integer(expected_n):
        return "expected_n must be a positive integer."
    required_n = expected_n
    for index, record in enumerate(candidates):
        if not isinstance(record, Mapping):
            return f"Candidate {index} is not a record."
        if _penalty_index(record.get("penalty")) != index:
            return f"Candidate {index} does not match the fixed ordered menu."
        if record.get("status") != "COMPLETE":
            return f"Required candidate {MENU[index]} is not COMPLETE."
        loss = record.get("mean_loss")
        if not _finite_number(loss) or loss < 0:
            return f"Candidate {MENU[index]} has an invalid mean loss."
        n = record.get("n")
        if not _positive_integer(n):
            return f"Candidate {MENU[index]} has an invalid origin count."
        if required_n is None:
            required_n = n
        if n != required_n:
            return f"Candidate {MENU[index]} does not cover all declared origins."
    return None


def select_candidate(candidates, expected_n=None):
    """Select the exact validation minimum after all six candidates complete.

    The supplied list follows MENU order. Equal means favor the later (stronger)
    penalty, including infinity. ``expected_n`` enforces a declared origin count
    when available; otherwise all positive candidate counts must agree.
    """
    reason = _validate_candidates(candidates, expected_n)
    if reason:
        return dict(status="FAILED", penalty=None, reason=reason, exact_tie=False,
                    mean_loss=None, n=None, tied_penalties=[])
    minimum = min(record["mean_loss"] for record in candidates)
    tied = [index for index, record in enumerate(candidates)
            if record["mean_loss"] == minimum]
    return dict(status="SELECTED", penalty=MENU[tied[-1]], reason=None,
                exact_tie=len(tied) > 1, mean_loss=minimum,
                n=int(candidates[0]["n"]),
                tied_penalties=[MENU[index] for index in tied])


def decompose(candidate_losses, selected_penalty, reference_loss):
    """Compute signed E/S/G from six complete evaluation means and matched F.

    Infinity may be the actual selected candidate, but is never a finite oracle
    candidate. Invalid/nonpositive F leaves the raw actual and oracle means
    available and makes the entire relative decomposition FAILED.
    """
    result = dict(status="FAILED", reason=None, actual_loss=None,
                  finite_oracle_loss=None, finite_oracle_penalty=None,
                  reference_loss=reference_loss,
                  actual_excess_pct=None, selection_component_pct=None,
                  signal_gap_pct=None, identity_residual=None)
    reason = _validate_candidates(candidate_losses)
    if reason:
        result["reason"] = reason
        return result
    selected_index = _penalty_index(selected_penalty)
    if selected_index is None:
        result["reason"] = "Selected penalty is outside the fixed menu."
        return result
    oracle_index = min(range(5), key=lambda i: (candidate_losses[i]["mean_loss"], -i))
    actual = candidate_losses[selected_index]["mean_loss"]
    oracle = candidate_losses[oracle_index]["mean_loss"]
    result.update(actual_loss=actual, finite_oracle_loss=oracle,
                  finite_oracle_penalty=MENU[oracle_index])
    if not _finite_number(reference_loss) or reference_loss <= 0:
        result["reason"] = "A finite strictly positive matched reference loss is required."
        return result
    e = 100 * ((actual - reference_loss) / reference_loss)
    s = 100 * ((actual - oracle) / reference_loss)
    g = 100 * ((oracle - reference_loss) / reference_loss)
    residual = e - (s + g)
    if not all(isfinite(value) for value in (e, s, g, residual)):
        result["reason"] = "Relative decomposition produced a nonfinite operand."
        return result
    result.update(status="COMPLETE", actual_excess_pct=e,
                  selection_component_pct=s, signal_gap_pct=g,
                  identity_residual=residual)
    return result


def _complete(row):
    return (row.get("status") == "COMPLETE" and
            all(_finite_number(row.get(component)) for component in COMPONENTS))


def _unique_slot(records):
    return records[0] if len(records) == 1 else None


def _majority(slots, condition):
    complete = [item for item in slots if item is not None and _complete(item)]
    support = sum(bool(condition(item)) for item in complete)
    planned = len(slots)
    unavailable = planned - len(complete)
    status = ("SUPPORTED" if support * 2 > planned else
              "NOT_SUPPORTED" if (support + unavailable) * 2 <= planned else
              "UNDETERMINED")
    return dict(status=status, planned_n=planned, complete_n=len(complete),
                support_n=support, nonsupport_n=len(complete) - support,
                unavailable_n=unavailable, lower_bound=support / planned,
                upper_bound=(support + unavailable) / planned)


def _d3(rows, method):
    records = [row for row in rows if row.get("method") == method and
               row.get("family") == "fx" and row.get("period") == "original" and
               row.get("window") == 2880 and row.get("horizon") in (6, 24)]
    slots = [_unique_slot([row for row in records if row.get("horizon") == horizon])
             for horizon in (6, 24)]
    complete = [row for row in slots if row is not None and _complete(row)]
    support = sum(row["signal_gap_pct"] < 0 for row in complete)
    omitted = any(row.get("status") == "NOT_RUN_RESOURCE_LIMIT" for row in records)
    status = ("NOT_EVALUATED" if omitted else
              "NOT_SUPPORTED" if any(row["signal_gap_pct"] >= 0 for row in complete)
              else "SUPPORTED" if support == 2 else "UNDETERMINED")
    return dict(status=status, planned_n=2, complete_n=len(complete),
                support_n=support, unavailable_n=2 - len(complete),
                resource_omitted_n=sum(row.get("status") == "NOT_RUN_RESOURCE_LIMIT"
                                       for row in slots if row is not None),
                horizons={str(h): dict(status=(row.get("status") if row else "MISSING_OR_DUPLICATE"),
                                       signal_gap_pct=(row.get("signal_gap_pct") if row and _complete(row) else None))
                          for h, row in zip((6, 24), slots)})


def evaluate_predictions(rows):
    """Evaluate fixed planned criteria with QR33 primary and QR4 separate.

    Missing, duplicate, failed, and numerically invalid cells are unavailable.
    Unknown source keys cannot replace one of the pinned 41 primary slots.
    F1 uses period="original". Other periods never replace its planned cells.
    The driver's family="fx" represents the protocol's original FX family.
    """
    rows = list(rows)
    outcomes = {}
    for method in METHODS:
        relevant = [row for row in rows if row.get("method") == method and
                    row.get("period") == "original" and
                    row.get("window") == 52]
        slots = []
        for family, keys, horizons in (("cftc", CFTC_SOURCE_KEYS, (6,)),
                                       ("panel", PANEL_SOURCE_KEYS, (6, 24))):
            for horizon in horizons:
                for key in keys:
                    slots.append(_unique_slot([row for row in relevant
                                               if row.get("family") == family and
                                               row.get("source_key") == key and
                                               row.get("horizon") == horizon]))
        outcomes[method] = dict(
            D1=_majority(slots, lambda row: row["signal_gap_pct"] > 0),
            D2=_majority(slots, lambda row: row["actual_excess_pct"] > 0 and
                         row["selection_component_pct"] > row["actual_excess_pct"] / 2),
            D3=_d3(rows, method))
    return dict(primary_method="QR33", secondary_method="QR4", methods=outcomes,
                **outcomes["QR33"],
                interpretation=("Descriptive retrospective finite-menu diagnostic. "
                                "A positive gap concerns these cells and this finite menu; "
                                "it does not establish universal absence of conditional signal."))


def _summary_slots(records, family, sources):
    """Return pinned source slots; singleton families have one unique source."""
    by_source = defaultdict(list)
    for row in records:
        by_source[row.get("source_key")].append(row)
    if family == "cftc":
        keys = CFTC_SOURCE_KEYS
    elif family == "panel":
        keys = PANEL_SOURCE_KEYS
    else:
        keys = tuple(by_source) if len(by_source) == 1 else ()
    slots = [_unique_slot(by_source.get(key, [])) for key in keys]
    return (slots + [None] * sources)[:sources]


def summarize_rows(rows):
    """Summarize percentages separately by family/period/H/W/method.

    All 180 planned method cells remain in group denominators even if rows
    are absent. Per-component medians need not satisfy a median identity.
    Means use only complete decompositions, with counts shown; no pooled
    native-unit losses or independent-series combined tests are produced.
    """
    rows = list(rows)
    periods = sorted({"original"} | {row.get("period", "original") for row in rows}, key=str)
    summaries = []
    for family, horizons, windows, sources in _GEOMETRIES:
        for period in periods:
            for horizon in horizons:
                for window in windows:
                    for method in METHODS:
                        records = [row for row in rows if
                                   (row.get("family"), row.get("period", "original"),
                                    row.get("horizon"), row.get("window"), row.get("method"))
                                   == (family, period, horizon, window, method)]
                        slots = _summary_slots(records, family, sources)
                        complete = [row for row in slots if row is not None and _complete(row)]
                        statuses = Counter(row.get("status") for row in slots if row is not None)
                        summary = dict(family=family, period=period, horizon=horizon,
                                       window=window, method=method, planned_n=sources,
                                       complete_n=len(complete), unavailable_n=sources - len(complete),
                                       failed_n=sum(count for status, count in statuses.items()
                                                    if isinstance(status, str) and status.startswith("FAILED")),
                                       resource_omitted_n=statuses["NOT_RUN_RESOURCE_LIMIT"],
                                       missing_or_duplicate_n=sum(row is None for row in slots),
                                       invalid_complete_n=sum(row is not None and row.get("status") == "COMPLETE"
                                                              and not _complete(row) for row in slots),
                                       status_counts=dict(sorted(statuses.items(), key=lambda item: str(item[0]))))
                        for component in COMPONENTS:
                            values = [row[component] for row in complete]
                            summary["mean_" + component] = (fsum(value / len(values) for value in values)
                                                          if values else None)
                            summary["median_" + component] = median(values) if values else None
                        summaries.append(summary)
    return summaries
