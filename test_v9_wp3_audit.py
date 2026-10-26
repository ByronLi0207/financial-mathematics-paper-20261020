"""Constructed inputs for the independent WP3 readback; no financial source I/O.

Prepared while the formal run may be active. Running this file is a separate
authorized step after that run terminates. Expected values never call the
production learning-curve or HAC helpers.
"""
import importlib.util
import math
from pathlib import Path
import numpy as np
import pytest


@pytest.fixture
def api():
    path = Path(__file__).parent / "notes/revision-v9/audit_wp3.py"
    spec = importlib.util.spec_from_file_location("independent_wp3_oracle", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_gate_rejects_a_float_change_that_readback_tolerance_accepts(api):
    old = np.array([1., 2.], dtype="<f8")
    new = old.copy()
    new[0] = np.nextafter(new[0], math.inf)
    api.compare(float(new[0]), float(old[0]))
    assert api.exact_array_differences({"values": new}, {"values": old}, "constructed")
    assert api.exact_array_differences({"values": old.copy()}, {"values": old}, "constructed") == []


@pytest.mark.parametrize("variant", ["shape", "dtype", "nonfinite"])
def test_exact_gate_checks_shape_dtype_and_finite_values(api, variant):
    old = np.array([1., 2.], dtype="<f8")
    if variant == "shape":
        new = old.reshape(1, 2)
    elif variant == "dtype":
        new = old.astype("<f4")
    else:
        new = old.copy()
        new[1] = math.nan
    assert api.exact_array_differences({"values": new}, {"values": old}, "constructed")


def test_tolerant_comparison_rejects_material_difference_and_nan(api):
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.compare(1.0001, 1., "constructed")
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.compare(math.nan, 1., "constructed")


def menus():
    return {"QR33": [.001, .01, .1], "QR4": [.001, .01, .1, 1., 10.]}


def candidates(method):
    result = []
    for value in menus()[method]:
        if method == "QR33":
            result.append(dict(parameter=value, status="COMPLETE", origin_count=4,
                               mean_pinball=1., failure=None))
        else:
            result.append(dict(penalty=value, status="COMPLETE", mean_pinball=1.))
    return result


def test_candidate_exact_ties_use_distinct_frozen_procedures(api):
    assert api.select_candidate(candidates("QR33"), "QR33", menus(), 4) == .1
    assert api.select_candidate(candidates("QR4"), "QR4", menus(), 4) == .001


def test_qr33_candidate_failure_cannot_be_dropped(api):
    rows = candidates("QR33")
    rows[0].update(status="FAILED", origin_count=0, mean_pinball=None,
                   failure={"reason": "CONSTRUCTED_FAILURE"})
    assert api.select_candidate(rows, "QR33", menus(), 4) is None


def test_qr4_uses_first_completed_minimizer_and_retains_missing_candidates(api):
    rows = candidates("QR4")
    rows[0].update(status="FAILED", mean_pinball=None, reason="CONSTRUCTED_FAILURE")
    assert api.select_candidate(rows, "QR4", menus(), 4) == .01
    for row in rows:
        row.update(status="FAILED", mean_pinball=None)
    assert api.select_candidate(rows, "QR4", menus(), 4) is None


def test_candidate_menu_and_full_count_are_not_silently_repaired(api):
    rows = candidates("QR33")
    rows[0]["origin_count"] = 3
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.select_candidate(rows, "QR33", menus(), 4)
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.select_candidate(candidates("QR4")[:-1], "QR4", menus(), 4)


def _manual_bartlett(values, horizon):
    values = list(map(float, values))
    n = len(values)
    lag = min(n - 1, max(horizon, math.floor(4 * (n / 100) ** (2 / 9))))
    mean = math.fsum(values) / n
    centered = [value - mean for value in values]
    variance = math.fsum(value * value for value in centered) / n
    for k in range(1, lag + 1):
        covariance = math.fsum(centered[i] * centered[i-k] for i in range(k, n)) / n
        variance += 2 * (1 - k / (lag + 1)) * covariance
    statistic = mean / math.sqrt(variance / n)
    return n, lag, mean, variance, statistic, math.erfc(abs(statistic) / math.sqrt(2))


def test_hac_matches_manual_centered_bartlett_with_n_denominators(api):
    values = [0., 1., 2., -1., 4., 0., 3., -2., 5., 2.]
    n, lag, mean, variance, statistic, probability = _manual_bartlett(values, 1)
    actual = api.hac_oracle(np.array(values), 1)
    assert actual["status"] == "OK"
    assert actual["n"] == n and actual["bandwidth"] == lag
    assert actual["direction"] == "QR_minus_matched_F"
    assert actual["mean_difference"] == pytest.approx(mean, abs=1e-10, rel=1e-12)
    assert actual["lrv"] == pytest.approx(variance, abs=1e-10, rel=1e-12)
    assert actual["dm_t"] == pytest.approx(statistic, abs=1e-10, rel=1e-12)
    assert actual["dm_p"] == pytest.approx(probability, abs=1e-10, rel=1e-12)
    assert actual["nominal_post_result"] is True


def test_hac_sign_is_qr_minus_f_and_two_sided_probability(api):
    values = np.array([0., 1., 2., -1., 4., 0., 3., -2., 5., 2.])
    positive = api.hac_oracle(values, 1)
    negative = api.hac_oracle(-values, 1)
    assert negative["mean_difference"] == pytest.approx(-positive["mean_difference"])
    assert negative["dm_t"] == pytest.approx(-positive["dm_t"])
    assert negative["dm_p"] == pytest.approx(positive["dm_p"])


@pytest.mark.parametrize("constant,status", [(0., "IDENTICAL_LOSSES"), (2., "ZERO_LONG_RUN_VARIANCE")])
def test_hac_degenerate_cases_keep_reason_without_fabricated_probability(api, constant, status):
    actual = api.hac_oracle(np.full(10, constant), 1)
    assert actual["status"] == status and actual["lrv"] == 0.
    assert actual["dm_t"] is None and actual["dm_p"] is None


def test_hac_rejects_nonfinite_or_incomplete_vector(api):
    for values, horizon in ((np.array([1., math.nan, 2.]), 1), (np.array([1., 2.]), 2)):
        with pytest.raises((api.AuditMismatch, ValueError)):
            api.hac_oracle(values, horizon)


@pytest.mark.parametrize("lower,upper,expected", [
    (195.264769574666, 774.9704967161092, "FIRST_CUTPOINT_CONSISTENT"),
    (92.90675766563821, 749.7655536169423, "FIRST_CUTPOINT_CONSISTENT"),
    (697.3741770523785, 2767.7517739861046, "FIRST_CUTPOINT_INCONSISTENT"),
    (331.8098488058507, 2677.7341200605083, "FIRST_CUTPOINT_CONSISTENT"),
])
def test_four_frozen_ranges_classify_one_constructed_raw_w_crossing(api, lower, upper, expected):
    actual = api.classify([360, 720, 1440, 2880, 5760], [1., -1., -2., -3., -4.], lower, upper)
    assert actual["first_crossing"] == 540.
    assert actual["prediction_status"] == expected
    assert actual["first_right_endpoint_strictly_negative"] is True


def test_curve_keeps_multiple_downward_crossings_but_uses_first(api):
    actual = api.classify([100, 200, 300, 400], [1., -1., 1., -1.], 140., 160.)
    assert actual["conditional_crossings"] == [150., 350.]
    assert actual["first_crossing"] == 150. and actual["multiple_crossings"] is True
    assert actual["prediction_status"] == "FIRST_CUTPOINT_CONSISTENT"


def test_curve_zero_touch_is_a_cutpoint_without_claiming_strict_winning(api):
    actual = api.classify([100, 200, 300], [2., 0., 2.], 190., 210.)
    assert actual["first_crossing"] == 200.
    assert actual["first_right_endpoint_strictly_negative"] is False
    assert actual["conditional_crossings"] == [200.]


def test_na_prefix_cannot_be_bridged_or_replaced_by_later_root(api):
    actual = api.classify([100, 200, 300, 400], [1., None, 2., -2.], 340., 360.)
    assert actual["conditional_crossings"] == [350.]
    assert actual["first_crossing"] is None
    assert actual["prediction_status"] == "NOT_TESTABLE_NA_PREFIX"
    actual = api.classify([100, 200, 300], [None, -1., -2.], 90., 110.)
    assert actual["prediction_status"] == "NOT_TESTABLE_NA_PREFIX"


def test_na_after_identified_first_crossing_does_not_erase_it(api):
    actual = api.classify([100, 200, 300], [1., -1., None], 140., 160.)
    assert actual["first_crossing"] == 150.
    assert actual["prediction_status"] == "FIRST_CUTPOINT_CONSISTENT"


def test_left_censoring_is_not_a_fabricated_point_estimate(api):
    actual = api.classify([100, 200, 300], [-1., 1., -1.], 110., 200.)
    assert actual["first_crossing"] is None and actual["observed_left_censoring"] is True
    assert actual["prediction_status"] == "INCONSISTENT_LEFT_CENSORED"
    actual = api.classify([100, 200, 300], [0., -1., -2.], 90., 110.)
    assert actual["prediction_status"] == "NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED"


def test_no_crossing_rejects_only_inside_uninterrupted_coverage(api):
    actual = api.classify([100, 200, 300, 400], [4., 3., 2., 1.], 110., 350.)
    assert actual["prediction_status"] == "INCONSISTENT_NO_CROSSING"
    actual = api.classify([100, 200, 300, 400], [4., 3., 2., 1.], 110., 450.)
    assert actual["prediction_status"] == "NOT_TESTABLE_NO_CROSSING"
    actual = api.classify([100, 200, 300, 400], [4., 3., None, 1.], 110., 350.)
    assert actual["prediction_status"] == "NOT_TESTABLE_NO_CROSSING"


@pytest.mark.parametrize("lower,upper", [(0., 200.), (None, 200.), (100., None), (100., math.inf)])
def test_non_discriminating_interval_cannot_be_replaced(api, lower, upper):
    actual = api.classify([100, 200], [1., -1.], lower, upper)
    assert actual["prediction_status"] == "NOT_TESTABLE_NONDISCRIMINATING_INTERVAL"
    assert actual["first_crossing"] is None


def vector_fixture():
    position = np.arange(250, dtype=float) % 7 - 3
    origins = np.arange(200, 228, dtype=np.int64)
    peak = np.array([max(abs(float(value)) for value in position[t:t+3]) for t in origins])
    floor = np.abs(position[origins])
    capacity = floor + .75
    residual = peak - capacity
    arrays = dict(origins=origins, capacity=capacity, peak=peak, floor=floor,
                  refit_indices=np.where(origins < 224, 200, 224).astype(np.int64),
                  pinball=.95*np.maximum(residual, 0)+.05*np.maximum(-residual, 0))
    clock = dict(validation_origin_first=200, validation_origin_last=227,
                 evaluation_origin_first=200, evaluation_origin_last=227,
                 refit_step=24, short_scale=24, long_scale=168, nominal_gap_seconds=3600)
    return position, arrays, clock


def test_vector_score_checks_actual_path_and_original_score_math(api):
    position, arrays, clock = vector_fixture()
    actual = api.score_vectors(position, arrays, 2, 20, "evaluation", clock, "QR33")
    residual = arrays["peak"] - arrays["capacity"]
    hits = int(np.count_nonzero(residual > 0))
    assert actual["origin_count"] == 28 and actual["strict_breach_count"] == hits
    assert actual["strict_breach_rate"] == hits / 28
    assert actual["mean_pinball"] == pytest.approx(math.fsum(map(float, arrays["pinball"])) / 28)
    assert actual["mean_capacity"] == pytest.approx(math.fsum(map(float, arrays["capacity"])) / 28)


@pytest.mark.parametrize("field", ["origins", "peak", "floor", "refit_indices", "pinball"])
def test_vector_corrupted_origin_label_floor_clock_or_loss_is_rejected(api, field):
    position, arrays, clock = vector_fixture()
    arrays[field] = arrays[field].copy()
    arrays[field][0] += 1
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.score_vectors(position, arrays, 2, 20, "evaluation", clock, "QR33")


def test_vector_trace_requires_whole_fixed_segment_and_mature_history(api):
    position, arrays, clock = vector_fixture()
    shortened = {key: value[:-1] for key, value in arrays.items()}
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.score_vectors(position, shortened, 2, 20, "evaluation", clock, "QR33")
    with pytest.raises((api.AuditMismatch, ValueError)):
        api.score_vectors(position, arrays, 2, 360, "evaluation", clock, "QR33")


def test_persisted_validation_diagnostics_use_original_qr33_and_qr4_field_names(api):
    _, _, clock = vector_fixture()
    rows = [dict(refit_index=r, training_first_origin=r-2-20+1,
                 training_last_origin=r-2, training_count=20, latest_label_end=r)
            for r in (200, 224)]
    api.fit_clock(rows, 2, 20, "validation", clock, "QR33")
    four = [dict(refit_index=r, training_first=r-2-20+1,
                 training_last=r-2, latest_label_end=r) for r in (200, 224)]
    api.fit_clock(four, 2, 20, "validation", clock, "QR4")
    api.fit_clock(rows[:1], 2, 20, "validation", clock, "QR33", partial=True)
    with pytest.raises(api.AuditMismatch):
        api.fit_clock(rows[:1], 2, 20, "validation", clock, "QR33")
    broken = [dict(r) for r in rows]
    broken[0]["latest_label_end"] += 1
    with pytest.raises(api.AuditMismatch):
        api.fit_clock(broken, 2, 20, "validation", clock, "QR33")


def test_full_old_validation_science_keeps_exact_scalar_gate_separate(api):
    old = dict(candidate_rows=[dict(parameter=.01, mean_pinball=1.)],
               fit_diagnostics=[dict(refit_index=200, latest_label_end=200)],
               selection=dict(status="SELECTED", parameter=.01))
    same = dict(candidate_rows=[dict(parameter=.01, mean_pinball=1.)],
                fit_diagnostics=[dict(refit_index=200, latest_label_end=200)],
                selection=dict(status="SELECTED", parameter=.01))
    assert api.exact_scalar_differences(same, old) == []
    same["candidate_rows"][0]["mean_pinball"] = float(np.nextafter(1., math.inf))
    api.compare(same, old)
    found = api.exact_scalar_differences(same, old)
    assert found and found[0]["location"].endswith("candidate_rows[0].mean_pinball")
