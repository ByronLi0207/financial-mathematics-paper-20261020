"""Artificial-only checks for the frozen E4 per-issued-report cost formula."""
import importlib
import json

import numpy as np
import pytest


def evaluate(*args, **kwargs):
    return importlib.import_module("v10_cost").evaluate_costs(*args, **kwargs)


def fixture():
    return (
        {"Q": np.array([11., 13., 15., 17.]), "F": np.full(4, 12.),
         "F_copy": np.full(4, 12.)},
        np.array([10., 12., 15., 18.]), np.full(4, 10.),
    )


def test_handworked_reserve_breach_excess_and_fixed_reference_costs():
    capacities, target, floor = fixture()
    r = evaluate(capacities, target, floor, "F",
                 {"kappa": [.5], "beta": [2.], "c": [3.]}, "Q")
    assert r["status"] == "COMPLETE"
    assert r["mean_F_headroom"] == 2.
    assert r["methods"]["F"] == {
        "n": 4, "mean_headroom": 2., "normalized_mean_headroom": 1.,
        "strict_breach_count": 2, "strict_breach_rate": .5,
        "mean_excess": 2.25, "normalized_mean_excess": 1.125,
    }
    assert r["methods"]["Q"] == {
        "n": 4, "mean_headroom": 4., "normalized_mean_headroom": 2.,
        "strict_breach_count": 1, "strict_breach_rate": .25,
        "mean_excess": .25, "normalized_mean_excess": .125,
    }
    q = next(x for x in r["rows"] if x["method_id"] == "Q")
    assert q == {"method_id": "Q", "kappa": .5, "beta": 2., "c": 3.,
                 "method_mean": 1.875, "reference_mean": 4.875,
                 "difference": -3., "cheaper": True, "equal": False}
    assert {x["method_id"] for x in r["rows"]} == set(capacities)
    for x in r["rows"]:
        if x["method_id"] != "Q":
            assert x["equal"] is True and x["cheaper"] is False
    json.dumps(r, allow_nan=False)


def test_positive_common_scale_preserves_normalized_costs_and_decisions():
    capacities, target, floor = fixture()
    grid = {"kappa": [.05, 1.], "beta": [0., 2.], "c": [.5, 1.]}
    a = evaluate(capacities, target, floor, "F", grid, "Q")
    b = evaluate({k: v * 8. for k, v in capacities.items()}, target * 8.,
                 floor * 8., "F", grid, "Q")
    assert a["rows"] == b["rows"]
    assert b["mean_F_headroom"] == 16.
    assert b["methods"]["Q"]["mean_excess"] == 2.


def test_zero_coefficients_keep_every_method_with_exact_zero_costs():
    capacities, target, floor = fixture()
    r = evaluate(capacities, target, floor, "F",
                 {"kappa": [0.], "beta": [0.], "c": [0.]}, "absent")
    assert r["status"] == "COMPLETE"
    assert r["primary_available"] is False
    assert len(r["rows"]) == 3
    assert all(x["method_mean"] == x["reference_mean"] == x["difference"] == 0.
               and x["equal"] and not x["cheaper"] for x in r["rows"])


def test_breach_is_strict_without_tolerance_and_equality_is_not_cheaper():
    c = np.array([1., np.nextafter(1., 0.), np.nextafter(1., 2.)])
    r = evaluate({"F": np.ones(3), "Q": c}, np.ones(3), np.zeros(3), "F",
                 {"kappa": [0.], "beta": [1.], "c": [0.]}, "Q")
    assert r["methods"]["F"]["strict_breach_count"] == 0
    assert r["methods"]["Q"]["strict_breach_count"] == 1
    q = next(x for x in r["rows"] if x["method_id"] == "Q")
    assert q["difference"] == 1 / 3 and not q["equal"] and not q["cheaper"]


def test_next_float_cost_difference_is_never_rounded_into_a_tie():
    r = evaluate({"F": np.array([1.]), "Q": np.array([np.nextafter(1., 0.)])},
                 np.array([0.]), np.array([0.]), "F",
                 {"kappa": [1.], "beta": [0.], "c": [0.]}, "Q")
    q = next(x for x in r["rows"] if x["method_id"] == "Q")
    assert q["difference"] < 0 and q["cheaper"] and not q["equal"]


@pytest.mark.parametrize("change", ["missing_F", "zero_headroom", "capacity_below_floor",
    "target_below_floor", "tiny_floor_violation", "nan", "infinite", "length", "matrix", "empty"])
def test_any_invalid_method_or_axis_makes_whole_comparison_unavailable(change):
    capacities, target, floor = fixture()
    if change == "missing_F": del capacities["F"]
    elif change == "zero_headroom": capacities["F"] = floor.copy()
    elif change == "capacity_below_floor": capacities["Q"][0] = 9.
    elif change == "target_below_floor": target[0] = 9.
    elif change == "tiny_floor_violation": capacities["Q"][0] = np.nextafter(10., 0.)
    elif change == "nan": capacities["Q"][0] = np.nan
    elif change == "infinite": floor[0] = np.inf
    elif change == "length": capacities["Q"] = capacities["Q"][:-1]
    elif change == "matrix": target = target.reshape(2, 2)
    elif change == "empty":
        capacities = {"F": np.array([])}; target = floor = np.array([])
    r = evaluate(capacities, target, floor, "F",
                 {"kappa": [.05], "beta": [0.], "c": [1.]}, "Q")
    assert r["status"] == "UNAVAILABLE" and r["reason"]
    assert r["rows"] == [] and r["methods"] == {}
    json.dumps(r, allow_nan=False)


@pytest.mark.parametrize("bad", [-.01, np.nan, np.inf])
def test_invalid_coefficient_does_not_produce_any_partial_grid(bad):
    capacities, target, floor = fixture()
    r = evaluate(capacities, target, floor, "F",
                 {"kappa": [.05], "beta": [0., bad], "c": [1.]}, "Q")
    assert r["status"] == "UNAVAILABLE" and r["rows"] == []


def test_tau_point_ninety_five_cost_difference_equals_pinball_difference():
    capacities, target, floor = fixture()
    r = evaluate(capacities, target, floor, "F",
                 {"kappa": [.05], "beta": [0.], "c": [1.]}, "Q")
    # Independent pinball definition at tau=.95, with equality contributing zero.
    losses = {k: np.mean(np.where(target > c, .95 * (target - c), .05 * (c - target)))
              for k, c in capacities.items()}
    for row in r["rows"]:
        assert row["difference"] == pytest.approx(
            (losses[row["method_id"]] - losses["F"]) / 2., abs=1e-15)


def test_all_cartesian_grid_points_and_methods_survive_without_model_selection():
    capacities, target, floor = fixture()
    r = evaluate(capacities, target, floor, "F",
                 {"kappa": [.01, .05], "beta": [0., 1., 5.], "c": [.5, 1.]}, "Q")
    assert len(r["rows"]) == 36
    assert len({(x["method_id"], x["kappa"], x["beta"], x["c"]) for x in r["rows"]}) == 36
    assert r["primary_available"] is True
