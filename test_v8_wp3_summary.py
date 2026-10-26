"""Hand-built WP3 summary fixtures; no DGP, model fit, or study-output reads.

The independent oracle uses only Fraction and stdlib statistics. Its unit of
uncertainty is a completed repetition, even though a study repetition contains
72 overlapping evaluation origins.
"""

from fractions import Fraction
import math
from statistics import mean, stdev

import pytest

from v8_mechanism_mc import summary_from_repetitions


ESTIMATE_FIELDS = (
    "relative_loss_percent",
    "relative_loss_mcse",
    "model_breach_rate",
    "model_breach_mcse",
    "reference_breach_rate",
    "reference_breach_mcse",
    "win_fraction",
    "win_mcse",
    "win_mcse_worst_bound",
)


def _complete(rep, reference_loss, model_loss, reference_rate, model_rate):
    return {
        "rep": rep,
        "status": "COMPLETE",
        "reference_loss": reference_loss,
        "model_loss": model_loss,
        "reference_breach_rate": reference_rate,
        "model_breach_rate": model_rate,
    }


def _unequal_loss_fixture():
    # A/B are deliberately unequal: the ratio of means is 9/16, whereas
    # the mean of the four individual ratios is 133/144.
    return [
        _complete(0, 1.0, 2.0, 0.0, 0.0),
        _complete(1, 4.0, 1.0, 0.5, 0.25),
        _complete(2, 2.0, 2.0, 0.25, 0.5),
        _complete(3, 9.0, 4.0, 0.25, 1.0),
    ]


def _stdlib_oracle(complete_rows):
    """Compute the stated estimands without any production-code helpers."""
    a = [Fraction(str(row["model_loss"])) for row in complete_rows]
    b = [Fraction(str(row["reference_loss"])) for row in complete_rows]
    model_rates = [Fraction(str(row["model_breach_rate"])) for row in complete_rows]
    reference_rates = [
        Fraction(str(row["reference_breach_rate"])) for row in complete_rows
    ]
    repetitions = len(a)
    ratio = mean(a) / mean(b) if mean(b) else None
    p = Fraction(sum(model < reference for model, reference in zip(a, b)), repetitions)
    return {
        "relative_loss_percent": None if ratio is None else float(100 * (ratio - 1)),
        "relative_loss_mcse": (
            None
            if ratio is None or repetitions < 2
            else 100
            * stdev(model - ratio * reference for model, reference in zip(a, b))
            / (math.sqrt(repetitions) * float(mean(b)))
        ),
        "model_breach_rate": float(mean(model_rates)),
        "model_breach_mcse": (
            stdev(model_rates) / math.sqrt(repetitions) if repetitions > 1 else None
        ),
        "reference_breach_rate": float(mean(reference_rates)),
        "reference_breach_mcse": (
            stdev(reference_rates) / math.sqrt(repetitions) if repetitions > 1 else None
        ),
        "win_fraction": float(p),
        "win_mcse": (
            math.sqrt(float(p * (1 - p)) / repetitions) if repetitions > 1 else None
        ),
        "win_mcse_worst_bound": 0.5 / math.sqrt(repetitions),
    }


def _assert_estimates(actual, expected):
    for field in ESTIMATE_FIELDS:
        if expected[field] is None:
            assert actual[field] is None, field
        else:
            assert actual[field] == pytest.approx(expected[field]), field


def test_complete_summary_uses_ratio_of_means_and_paired_delta_mcse():
    rows = _unequal_loss_fixture()
    result = summary_from_repetitions(rows, planned_repetitions=4)

    assert result["planned_repetitions"] == 4
    assert result["complete_repetitions"] == 4
    assert result["failed_repetitions"] == 0
    assert result["unattempted_repetitions"] == 0
    assert result["conditional_on_completion"] is False
    assert result["full_procedure_status"] == "COMPLETE"
    assert result["relative_loss_percent"] == pytest.approx(-43.75)
    _assert_estimates(result, _stdlib_oracle(rows))
    assert result["full_procedure_relative_loss_percent"] == pytest.approx(-43.75)

    wrong_mean_of_ratios = 100 * (
        mean(row["model_loss"] / row["reference_loss"] for row in rows) - 1
    )
    assert result["relative_loss_percent"] != pytest.approx(wrong_mean_of_ratios)


def test_breach_mcse_uses_sample_sd_across_repetitions_not_origin_iid():
    rows = _unequal_loss_fixture()
    result = summary_from_repetitions(rows, planned_repetitions=4)

    # Squared deviations sum to 35/64 for model rates, 1/8 for reference
    # rates; divide by R-1 before dividing the sample SD by sqrt(R).
    assert result["model_breach_rate"] == pytest.approx(7 / 16)
    assert result["model_breach_mcse"] == pytest.approx(math.sqrt(35 / 192) / 2)
    assert result["reference_breach_rate"] == pytest.approx(1 / 4)
    assert result["reference_breach_mcse"] == pytest.approx(math.sqrt(1 / 24) / 2)
    wrong_origin_iid = math.sqrt((7 / 16) * (9 / 16) / (4 * 72))
    assert result["model_breach_mcse"] != pytest.approx(wrong_origin_iid)


def test_strict_win_fraction_excludes_ties_and_has_plugin_mcse():
    result = summary_from_repetitions(_unequal_loss_fixture(), planned_repetitions=4)

    # Two strict wins, one tie and one strict loss.
    assert result["win_fraction"] == pytest.approx(0.5)
    assert result["win_mcse"] == pytest.approx(0.25)
    assert result["win_mcse_worst_bound"] == pytest.approx(0.25)


def test_proportional_paired_losses_have_zero_relative_delta_mcse():
    rows = [
        _complete(0, 1.0, 0.5, 0.25, 0.0),
        _complete(1, 2.0, 1.0, 0.5, 0.25),
        _complete(2, 8.0, 4.0, 0.0, 0.5),
    ]
    result = summary_from_repetitions(rows, planned_repetitions=3)

    # The losses vary greatly, but each paired delta A-rB is exactly zero.
    assert result["relative_loss_percent"] == pytest.approx(-50.0)
    assert result["relative_loss_mcse"] == pytest.approx(0.0, abs=1e-14)
    assert result["win_fraction"] == pytest.approx(1.0)
    assert result["win_mcse"] == pytest.approx(0.0)
    assert result["win_mcse_worst_bound"] == pytest.approx(0.5 / math.sqrt(3))


def test_missing_reports_keep_planned_counts_and_mark_available_pairs_conditional():
    completed = [
        _complete(0, 2.0, 1.0, 0.5, 0.25),
        _complete(2, 6.0, 9.0, 1.0, 0.75),
    ]
    rows = [
        completed[0],
        {"rep": 1, "status": "FAILED"},
        completed[1],
        {"rep": 3, "status": "NOT_ATTEMPTED"},
        {"rep": 4, "status": "FAILED"},
    ]
    result = summary_from_repetitions(rows, planned_repetitions=5)

    assert result["planned_repetitions"] == 5
    assert result["complete_repetitions"] == 2
    assert result["failed_repetitions"] == 2
    assert result["unattempted_repetitions"] == 1
    assert result["conditional_on_completion"] is True
    assert result["full_procedure_status"] == "NA"
    assert result["full_procedure_relative_loss_percent"] is None
    _assert_estimates(result, _stdlib_oracle(completed))
    assert result["relative_loss_percent"] == pytest.approx(25.0)
    assert result["model_breach_rate"] == pytest.approx(0.5)
    assert result["win_fraction"] == pytest.approx(0.5)


@pytest.mark.parametrize(
    "statuses,failed,unattempted",
    [
        (["FAILED", "FAILED", "FAILED"], 3, 0),
        (["NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED"], 0, 3),
        (["FAILED", "NOT_ATTEMPTED", "FAILED"], 2, 1),
    ],
    ids=["all-failed", "all-unattempted", "mixed-missing"],
)
def test_no_completed_pairs_has_counts_and_no_invented_estimates(
    statuses, failed, unattempted
):
    rows = [{"rep": rep, "status": status} for rep, status in enumerate(statuses)]
    result = summary_from_repetitions(rows, planned_repetitions=3)

    assert result["planned_repetitions"] == 3
    assert result["complete_repetitions"] == 0
    assert result["failed_repetitions"] == failed
    assert result["unattempted_repetitions"] == unattempted
    assert result["conditional_on_completion"] is True
    assert result["full_procedure_status"] == "NA"
    assert result["full_procedure_relative_loss_percent"] is None
    for field in ESTIMATE_FIELDS:
        assert result[field] is None, field


def test_single_completion_reports_means_but_sample_mcse_is_undefined():
    rows = [_complete(0, 4.0, 1.0, 0.5, 0.25)]
    result = summary_from_repetitions(rows, planned_repetitions=1)

    assert result["planned_repetitions"] == result["complete_repetitions"] == 1
    assert result["failed_repetitions"] == result["unattempted_repetitions"] == 0
    assert result["conditional_on_completion"] is False
    assert result["full_procedure_status"] == "COMPLETE"
    assert result["relative_loss_percent"] == pytest.approx(-75.0)
    assert result["full_procedure_relative_loss_percent"] == pytest.approx(-75.0)
    assert result["model_breach_rate"] == pytest.approx(0.25)
    assert result["reference_breach_rate"] == pytest.approx(0.5)
    assert result["win_fraction"] == pytest.approx(1.0)
    assert result["win_mcse"] is None
    assert result["win_mcse_worst_bound"] == pytest.approx(0.5)
    for field in ("relative_loss_mcse", "model_breach_mcse", "reference_breach_mcse"):
        assert result[field] is None, field


def test_zero_reference_loss_disables_only_relative_loss_estimates():
    rows = [
        _complete(0, 0.0, 1.0, 0.0, 0.5),
        _complete(1, 0.0, 0.0, 0.25, 0.0),
        _complete(2, 0.0, 3.0, 0.5, 1.0),
    ]
    result = summary_from_repetitions(rows, planned_repetitions=3)

    assert result["full_procedure_status"] == "COMPLETE"
    assert result["conditional_on_completion"] is False
    assert result["full_procedure_relative_loss_percent"] is None
    _assert_estimates(result, _stdlib_oracle(rows))
    assert result["relative_loss_percent"] is None
    assert result["relative_loss_mcse"] is None
    assert result["win_fraction"] == pytest.approx(0.0)
    assert result["model_breach_rate"] == pytest.approx(0.5)
    assert result["reference_breach_rate"] == pytest.approx(0.25)


def test_summary_accepts_any_row_order_with_the_exact_planned_rep_set():
    rows = _unequal_loss_fixture()
    result = summary_from_repetitions([rows[2], rows[0], rows[3], rows[1]], 4)

    _assert_estimates(result, _stdlib_oracle(rows))
    assert result["complete_repetitions"] == 4
    assert result["full_procedure_status"] == "COMPLETE"


@pytest.mark.parametrize(
    "reps",
    [[0, 1], [0, 0, 2], [0, 1, 3], [-1, 1, 2], [0, 1, 2, 3]],
    ids=["missing", "duplicate", "out-of-range", "negative", "extra"],
)
def test_repetition_inventory_must_be_exactly_the_planned_set(reps):
    rows = [_complete(rep, 1.0, 0.5, 0.0, 0.0) for rep in reps]
    with pytest.raises(ValueError):
        summary_from_repetitions(rows, planned_repetitions=3)


@pytest.mark.parametrize("status", ["complete", "BROKEN", ""], ids=["case", "unknown", "empty"])
def test_unrecognized_status_is_rejected(status):
    rows = [_complete(0, 1.0, 0.5, 0.0, 0.0)]
    rows[0]["status"] = status
    with pytest.raises(ValueError):
        summary_from_repetitions(rows, planned_repetitions=1)


@pytest.mark.parametrize("field", ["reference_loss", "model_loss"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), -0.1], ids=["nan", "infinity", "negative-infinity", "negative"])
def test_completed_losses_must_be_finite_and_nonnegative(field, value):
    rows = [_complete(0, 1.0, 0.5, 0.0, 0.0)]
    rows[0][field] = value
    with pytest.raises(ValueError):
        summary_from_repetitions(rows, planned_repetitions=1)


@pytest.mark.parametrize("field", ["reference_breach_rate", "model_breach_rate"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), -0.01, 1.01], ids=["nan", "infinity", "negative-infinity", "below-zero", "above-one"])
def test_completed_breach_rates_must_be_finite_probabilities(field, value):
    rows = [_complete(0, 1.0, 0.5, 0.0, 0.0)]
    rows[0][field] = value
    with pytest.raises(ValueError):
        summary_from_repetitions(rows, planned_repetitions=1)


@pytest.mark.parametrize(
    "field",
    ["reference_loss", "model_loss", "reference_breach_rate", "model_breach_rate"],
)
def test_complete_status_cannot_hide_a_missing_numeric_report(field):
    rows = [_complete(0, 1.0, 0.5, 0.0, 0.0)]
    del rows[0][field]
    with pytest.raises(ValueError):
        summary_from_repetitions(rows, planned_repetitions=1)


def test_row_without_a_repetition_id_is_rejected():
    rows = [_complete(0, 1.0, 0.5, 0.0, 0.0)]
    del rows[0]["rep"]
    with pytest.raises(ValueError):
        summary_from_repetitions(rows, planned_repetitions=1)
