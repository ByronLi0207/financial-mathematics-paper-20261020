"""Toy arithmetic only: tests for the frozen F1 loss decomposition contract."""

from copy import deepcopy
from importlib import import_module
import math

import pytest


PENALTIES = (0.001, 0.01, 0.1, 1.0, 10.0, "inf")
CFTC_KEYS = ("044601", "043602", "042601", "045601", "020601", "099741",
             "1170E1", "097741", "096742", "095741", "090741", "232741",
             "33874A", "240743", "092741", "098662", "112741")
PANEL_KEYS = ("PDPOSCS-TOT", "PDPOSFGS-TOT", "PDPOSGSC-G2L3", "PDPOSGSC-G3L6",
              "PDPOSGSC-G6L7", "PDPOSGSC-G7L11", "PDPOSGSC-L2", "PDPOSMBS-TOT",
              "PDPOSTIPS-G11", "PDPOSTIPS-G2", "PDPOSTIPS-G6L11", "PDPOSTIPS-L2")


def api():
    return import_module("v12_decomposition")


def candidates(losses=(15, 14, 13, 12, 11, 9), n=8):
    return [dict(penalty=p, status="COMPLETE", mean_loss=l, n=n)
            for p, l in zip(PENALTIES, losses)]


def row(source="044601", family="cftc", horizon=6, window=52,
        method="QR33", status="COMPLETE", e=10, s=6, g=4,
        period="original"):
    return dict(cell_id=f"{family}/{source}/H{horizon}/W{window}/{method}",
                family=family, source_key=source, period=period,
                horizon=horizon, window=window, method=method, status=status,
                actual_excess_pct=e, selection_component_pct=s, signal_gap_pct=g)


def primary_rows(support=41, nonsupport=0, method="QR33"):
    rows = [row(key, method=method) for key in CFTC_KEYS]
    rows += [row(key, family="panel", horizon=h, method=method)
             for h in (6, 24) for key in PANEL_KEYS]
    for index, item in enumerate(rows):
        if index < support:
            continue
        if index < support + nonsupport:
            item.update(actual_excess_pct=-2, selection_component_pct=0,
                        signal_gap_pct=-2)
        else:
            item.update(status="FAILED", actual_excess_pct=None,
                        selection_component_pct=None, signal_gap_pct=None)
    return rows


def fx(horizon, g=-1, method="QR33", status="COMPLETE"):
    return row("fx", family="fx", horizon=horizon, window=2880,
               method=method, status=status, e=g + 2, s=2, g=g)


def test_selection_exact_ties_choose_strongest_including_infinity():
    chosen = api().select_candidate(candidates((1, 1, 1, 1, 1, 1)), expected_n=8)
    assert chosen["status"] == "SELECTED"
    assert chosen["penalty"] == "inf"
    assert chosen["exact_tie"] is True


def test_selection_near_ties_are_not_tolerance_ties():
    chosen = api().select_candidate(candidates((1, 2, 3, 4, 5, 1 + 1e-12)))
    assert chosen["penalty"] == 0.001
    assert chosen["exact_tie"] is False


@pytest.mark.parametrize("bad_index", range(6))
@pytest.mark.parametrize("method", ("QR33", "QR4"))
def test_any_candidate_failure_fails_whole_method_cell(bad_index, method):
    records = candidates()
    records[bad_index].update(status="FAILED", method=method)
    result = api().select_candidate(records)
    assert result["status"] == "FAILED"
    assert result["penalty"] is None
    assert result["reason"]
    assert api().decompose(records, "inf", 10)["status"] == "FAILED"


@pytest.mark.parametrize("change", ("missing", "reordered", "duplicate", "short_n",
                                   "n_zero", "nan", "negative", "infinite"))
def test_selection_requires_full_structurally_valid_six_menu(change):
    records = candidates()
    if change == "missing":
        records.pop()
    elif change == "reordered":
        records[0], records[1] = records[1], records[0]
    elif change == "duplicate":
        records[-1]["penalty"] = 10
    elif change == "short_n":
        records[3]["n"] = 7
    elif change == "n_zero":
        records[3]["n"] = 0
    elif change == "nan":
        records[3]["mean_loss"] = math.nan
    elif change == "negative":
        records[3]["mean_loss"] = -1
    else:
        records[3]["mean_loss"] = math.inf
    assert api().select_candidate(records, expected_n=8)["status"] == "FAILED"


def test_selection_does_not_accept_uniformly_truncated_counts():
    assert api().select_candidate(candidates(n=7), expected_n=8)["status"] == "FAILED"


def test_decomposition_excludes_infinity_and_preserves_negative_selection():
    result = api().decompose(candidates(), "inf", 10)
    assert result["status"] == "COMPLETE"
    assert result["actual_loss"] == 9
    assert result["finite_oracle_loss"] == 11
    assert result["finite_oracle_penalty"] == 10.0
    assert result["reference_loss"] == 10
    assert result["actual_excess_pct"] == pytest.approx(-10)
    assert result["selection_component_pct"] == pytest.approx(-20)
    assert result["signal_gap_pct"] == pytest.approx(10)
    assert result["identity_residual"] == pytest.approx(0, abs=1e-12)


def test_finite_oracle_exact_tie_chooses_larger_finite_penalty():
    result = api().decompose(candidates((12, 11, 11, 11, 11, 5)), 0.001, 10)
    assert result["finite_oracle_penalty"] == 10.0
    assert result["actual_excess_pct"] == pytest.approx(20)
    assert result["selection_component_pct"] == pytest.approx(10)
    assert result["signal_gap_pct"] == pytest.approx(10)


@pytest.mark.parametrize("reference", (0, -1, math.nan, math.inf, None))
def test_nonpositive_or_nonfinite_reference_fails_relative_decomposition(reference):
    result = api().decompose(candidates(), "inf", reference)
    assert result["status"] == "FAILED"
    assert result["actual_loss"] == 9
    assert result["finite_oracle_loss"] == 11
    for field in ("actual_excess_pct", "selection_component_pct", "signal_gap_pct",
                  "identity_residual"):
        assert result[field] is None


def test_decomposition_rejects_unselected_menu_value():
    assert api().decompose(candidates(), 0.2, 10)["status"] == "FAILED"


@pytest.mark.parametrize("support,nonsupport,want", ((21, 0, "SUPPORTED"),
                                                   (20, 21, "NOT_SUPPORTED"),
                                                   (20, 20, "UNDETERMINED"),
                                                   (0, 0, "UNDETERMINED")))
def test_majority_uses_fixed_41_and_unknown_bounds(support, nonsupport, want):
    result = api().evaluate_predictions(primary_rows(support, nonsupport))
    for criterion in ("D1", "D2"):
        outcome = result[criterion]
        assert outcome["status"] == want
        assert outcome["planned_n"] == 41
        assert outcome["support_n"] == support
        assert outcome["complete_n"] == support + nonsupport
        assert outcome["unavailable_n"] == 41 - support - nonsupport
        assert outcome["lower_bound"] == pytest.approx(support / 41)
        assert outcome["upper_bound"] == pytest.approx((41 - nonsupport) / 41)


def test_missing_rows_remain_in_primary_denominator():
    result = api().evaluate_predictions(primary_rows()[:21])
    assert result["D1"]["status"] == "SUPPORTED"
    assert result["D1"]["unavailable_n"] == 20


def test_d2_nonpositive_excess_counts_complete_nonsupport():
    records = primary_rows()
    for item in records:
        item.update(actual_excess_pct=0, selection_component_pct=2,
                    signal_gap_pct=-2)
    result = api().evaluate_predictions(records)["D2"]
    assert result["status"] == "NOT_SUPPORTED"
    assert result["complete_n"] == 41
    assert result["support_n"] == 0
    assert result["unavailable_n"] == 0


def test_d1_and_d2_signs_are_strict_and_negative_selection_is_retained():
    records = primary_rows()
    for item in records:
        item.update(actual_excess_pct=10, selection_component_pct=5, signal_gap_pct=0)
    result = api().evaluate_predictions(records)
    assert result["D1"]["support_n"] == 0
    assert result["D2"]["support_n"] == 0
    records[0].update(selection_component_pct=-20, signal_gap_pct=30)
    assert api().evaluate_predictions(records)["D2"]["support_n"] == 0


def test_qr4_and_nonprimary_geometries_cannot_substitute_for_qr33():
    records = primary_rows(0, 41) + primary_rows(method="QR4")
    records += [row(f"extra{i}", window=260) for i in range(30)]
    records += [row(f"bill{i}", family="bill") for i in range(30)]
    result = api().evaluate_predictions(records)
    assert result["D1"]["status"] == "NOT_SUPPORTED"
    assert result["methods"]["QR4"]["D1"]["status"] == "SUPPORTED"


def test_primary_duplicate_is_unavailable_instead_of_double_counted():
    records = primary_rows()
    records.append(deepcopy(records[0]))
    result = api().evaluate_predictions(records)["D1"]
    assert result["complete_n"] == 40
    assert result["unavailable_n"] == 1
    assert result["support_n"] == 40


@pytest.mark.parametrize("g6,g24,want", ((-1, -2, "SUPPORTED"),
                                         (-1, 0, "NOT_SUPPORTED"),
                                         (1, -2, "NOT_SUPPORTED")))
def test_d3_requires_both_original_fx_horizons_negative(g6, g24, want):
    outcome = api().evaluate_predictions([fx(6, g6), fx(24, g24)])["D3"]
    assert outcome["status"] == want
    assert outcome["planned_n"] == 2


def test_d3_one_negative_and_one_failed_is_undetermined():
    result = api().evaluate_predictions([fx(6), fx(24, status="FAILED")])
    assert result["D3"]["status"] == "UNDETERMINED"


def test_d3_complete_counterexample_decides_despite_other_failure():
    result = api().evaluate_predictions([fx(6, 0), fx(24, status="FAILED_RESOURCE")])
    assert result["D3"]["status"] == "NOT_SUPPORTED"


def test_d3_resource_omission_is_not_evaluated():
    result = api().evaluate_predictions([fx(6, status="NOT_RUN_RESOURCE_LIMIT"),
                                         fx(24, status="NOT_RUN_RESOURCE_LIMIT")])
    assert result["D3"]["status"] == "NOT_EVALUATED"


def test_d3_missing_and_wrong_window_do_not_count_as_negative():
    records = [fx(6), row("fx", family="fx", horizon=24, window=720, g=-1)]
    assert api().evaluate_predictions(records)["D3"]["status"] == "UNDETERMINED"


def test_d3_unknown_horizon_resource_row_cannot_change_conjunction():
    records = [fx(6), fx(24), fx(999, status="NOT_RUN_RESOURCE_LIMIT")]
    assert api().evaluate_predictions(records)["D3"]["status"] == "SUPPORTED"


def test_d3_qr4_does_not_replace_qr33_and_is_reported_separately():
    records = [fx(6, method="QR4"), fx(24, method="QR4")]
    result = api().evaluate_predictions(records)
    assert result["D3"]["status"] == "UNDETERMINED"
    assert result["methods"]["QR4"]["D3"]["status"] == "SUPPORTED"


def test_summaries_preserve_groups_failures_and_component_statistics():
    records = [row(e=100, s=90, g=10), row("043602", e=-20, s=-30, g=10),
               row("042601", status="FAILED", e=None, s=None, g=None),
               row("045601", status="NOT_RUN_RESOURCE_LIMIT", e=None, s=None, g=None),
               row("020601", e=10, s=0, g=10), row("099741", method="QR4", e=5, s=3, g=2)]
    summaries = api().summarize_rows(records)
    full = next(x for x in summaries if x["family"] == "cftc" and
                x["window"] == 52 and x["method"] == "QR33")
    assert full["planned_n"] == 17
    assert full["complete_n"] == 3
    assert full["failed_n"] == 1
    assert full["resource_omitted_n"] == 1
    assert full["unavailable_n"] == 14
    assert full["mean_actual_excess_pct"] == pytest.approx(30)
    assert full["median_actual_excess_pct"] == 10
    assert full["mean_selection_component_pct"] == pytest.approx(20)
    assert full["median_selection_component_pct"] == 0
    assert full["mean_signal_gap_pct"] == pytest.approx(10)
    assert full["median_signal_gap_pct"] == 10
    four = next(x for x in summaries if x["family"] == "cftc" and
                x["window"] == 52 and x["method"] == "QR4")
    assert four["complete_n"] == 1
    assert four["median_actual_excess_pct"] == 5


def test_summaries_keep_all_180_planned_method_cells_even_when_empty():
    summaries = api().summarize_rows([])
    assert len(summaries) == 28
    assert sum(x["planned_n"] for x in summaries) == 180
    assert sum(x["complete_n"] for x in summaries) == 0
    assert all(x["mean_actual_excess_pct"] is None for x in summaries)


def test_summaries_preserve_original_plan_when_only_other_period_is_supplied():
    summaries = api().summarize_rows([row(period="early2015")])
    original = [item for item in summaries if item["period"] == "original"]
    assert sum(item["planned_n"] for item in original) == 180
    assert sum(item["complete_n"] for item in original) == 0


def test_summaries_do_not_mix_periods():
    summaries = api().summarize_rows([row(period="original", e=10),
                                      row(period="early2015", e=90)])
    matching = [x for x in summaries if x["family"] == "cftc" and
                x["window"] == 52 and x["method"] == "QR33"]
    assert {x["period"]: x["mean_actual_excess_pct"] for x in matching} == {
        "original": 10, "early2015": 90}


def test_component_medians_are_separate_and_need_not_obey_identity():
    records = [row(e=0, s=0, g=0), row("043602", e=10, s=0, g=10),
               row("042601", e=10, s=10, g=0)]
    summary = next(x for x in api().summarize_rows(records) if x["family"] == "cftc"
                   and x["window"] == 52 and x["method"] == "QR33")
    assert summary["median_actual_excess_pct"] == 10
    assert summary["median_selection_component_pct"] == 0
    assert summary["median_signal_gap_pct"] == 0
    assert summary["mean_actual_excess_pct"] == pytest.approx(20 / 3)


def test_failed_resource_retains_failure_and_planned_denominator():
    records = [row(status="FAILED_RESOURCE", e=None, s=None, g=None)]
    summary = next(x for x in api().summarize_rows(records) if x["family"] == "cftc"
                   and x["window"] == 52 and x["method"] == "QR33")
    assert summary["planned_n"] == 17
    assert summary["failed_n"] == 1
    assert summary["complete_n"] == 0
    assert summary["unavailable_n"] == 17
    assert summary["status_counts"] == {"FAILED_RESOURCE": 1}


def test_other_period_cannot_replace_missing_f1_cells():
    records = primary_rows()[:20]
    other = primary_rows()
    for item in other:
        item["period"] = "early2015"
    result = api().evaluate_predictions(records + other)
    assert result["D1"]["support_n"] == 20
    assert result["D1"]["unavailable_n"] == 21
    assert result["D1"]["status"] == "UNDETERMINED"
    other_fx = fx(24)
    other_fx["period"] = "early2015"
    assert api().evaluate_predictions([fx(6), other_fx])["D3"]["status"] == "UNDETERMINED"


def test_unknown_source_cannot_replace_missing_pinned_primary_slot():
    records = primary_rows()[1:]
    records.append(row("unplanned_source"))
    result = api().evaluate_predictions(records)["D1"]
    assert result["complete_n"] == 40
    assert result["unavailable_n"] == 1


@pytest.mark.parametrize("field,bad", (("penalty", []), ("mean_loss", True),
                                      ("n", True), ("mean_loss", "9")))
def test_invalid_scalar_types_fail_instead_of_silent_coercion(field, bad):
    records = candidates()
    records[0][field] = bad
    assert api().select_candidate(records)["status"] == "FAILED"


def test_pure_functions_do_not_mutate_inputs():
    records, rows = candidates(), primary_rows()
    before_records, before_rows = deepcopy(records), deepcopy(rows)
    api().select_candidate(records)
    api().decompose(records, "inf", 10)
    api().evaluate_predictions(rows)
    api().summarize_rows(rows)
    assert records == before_records
    assert rows == before_rows
