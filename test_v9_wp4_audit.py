"""Constructed figure-evidence sabotage tests; no production plotter import.

This file does not load any financial source or formal result. Execute only in
the separate verification phase authorized by the main task.
"""
import copy
import importlib.util
from pathlib import Path
import pytest

def test_same_period_key_marks_repeated_cells_not_all_new_window_cells(api):
    base=dict(source="fx_hourly",horizon=6,method="QR33")
    assert api.expected_period_key(dict(base,family="empirical",window=720))=="fx_hourly:6:720:QR33"
    assert api.expected_period_key(dict(base,family="curve",window=2880))=="fx_hourly:6:2880:QR33"
    assert api.expected_period_key(dict(base,family="curve",window=360)) is None
    assert api.expected_period_key(dict(base,family="curve",window=1440)) is None
    assert api.expected_period_key(dict(base,family="curve",window=5760)) is None


@pytest.fixture
def api():
    path = Path(__file__).parent / "notes/revision-v9/audit_wp4.py"
    spec = importlib.util.spec_from_file_location("independent_wp4_oracle", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evidence_fixture():
    def point(identifier, family, source, window, horizon, loss):
        return dict(point_id=identifier, method="QR33", family=family, source=source,
                    window=window, horizon=horizon, c=window/(horizon+1),
                    relative_loss_percent=loss)

    points = [
        point("v8-a", "v8_sim", "synthetic", 70, 6, 100.),
        point("v8-b", "v8_sim", "synthetic", 70, 6, 120.),
        point("v9-a", "v9_sim", "synthetic", 140, 6, 30.),
        point("hourly-a", "empirical", "fx_hourly", 350, 6, -10.),
        point("daily-a", "empirical", "fx_daily", 280, 6, 10.),
        point("treasury-a", "empirical", "nyfed_weekly", 210, 6, 20.),
        point("panel-a", "empirical", "panel:CONSTRUCTED", 560, 6, 5.),
        point("curve6-a", "curve", "fx_hourly", 70, 6, 20.),
        point("curve6-b", "curve", "fx_hourly", 140, 6, -5.),
        point("curve24-a", "curve", "fx_hourly", 250, 24, 10.),
        point("curve24-b", "curve", "fx_hourly", 500, 24, -10.),
    ]
    index = {p["point_id"]: p for p in points}

    def artist(kind, marker, identifiers):
        return dict(kind=kind, marker=marker, point_ids=list(identifiers),
                    actual_offsets=[[index[i]["c"], index[i]["relative_loss_percent"]]
                                    for i in identifiers])

    artists = [
        artist("scatter", "x", ["v8-a", "v8-b"]),
        artist("scatter", "+", ["v9-a"]),
        artist("scatter", "o", ["hourly-a"]),
        artist("scatter", "^", ["daily-a"]),
        artist("scatter", "s", ["treasury-a"]),
        artist("scatter", "D", ["panel-a"]),
        artist("line", "o", ["curve6-a", "curve6-b"]),
        artist("line", "v", ["curve24-a", "curve24-b"]),
    ]
    panel = dict(panel="constructed_full", point_ids=list(index),
                 visible_point_ids=list(index), xlim=[1., 100.], ylim=[-50., 150.],
                 full_range=True, artists=artists)
    bands = {"QR33": dict(lower=3., upper=20., upper_unbounded=False)}
    return panel, index, bands


def test_complete_constructed_panel_passes_without_name_or_artist_label_contract(api):
    panel, index, bands = evidence_fixture()
    panel["panel"] = "arbitrary descriptive label"
    for i, artist in enumerate(panel["artists"]):
        artist["category"] = "arbitrary visible legend " + str(i)
    assert isinstance(api.audit_panel(panel, index, bands), dict)


def test_actual_artist_y_offsets_are_verified_against_each_point(api):
    panel, index, bands = evidence_fixture()
    panel["artists"][0]["actual_offsets"][0][1] += 1.
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_actual_artist_x_offsets_are_verified_before_display_claims(api):
    panel, index, bands = evidence_fixture()
    panel["artists"][0]["actual_offsets"][0][0] += 1.
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_missing_logical_group_artist_does_not_pass_point_census(api):
    panel, index, bands = evidence_fixture()
    panel["artists"].pop(2)
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


@pytest.mark.parametrize("artist_index,wrong_marker", [(0, "o"), (1, "x"), (3, "s"), (7, "o")])
def test_marker_mapping_is_derived_from_scientific_group(api, artist_index, wrong_marker):
    panel, index, bands = evidence_fixture()
    panel["artists"][artist_index]["marker"] = wrong_marker
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_scatter_cannot_be_presented_as_curve_and_curve_cannot_be_scatter(api):
    panel, index, bands = evidence_fixture()
    panel["artists"][0]["kind"] = "line"
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)
    panel, index, bands = evidence_fixture()
    panel["artists"][6]["kind"] = "scatter"
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_falsely_claimed_full_range_crop_is_rejected(api):
    panel, index, bands = evidence_fixture()
    panel["ylim"] = [-50., 110.]
    panel["visible_point_ids"] = [i for i in panel["point_ids"] if i != "v8-b"]
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_band_interval_must_be_contained_in_panel_x_limits(api):
    panel, index, bands = evidence_fixture()
    bands["QR33"]["upper"] = 101.
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_omitted_coincident_x_point_is_not_hidden_by_another_point(api):
    panel, index, bands = evidence_fixture()
    assert index["v8-a"]["c"] == index["v8-b"]["c"]
    panel["artists"][0]["point_ids"].pop()
    panel["artists"][0]["actual_offsets"].pop()
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_duplicate_point_in_artist_is_not_an_extra_visual_copy(api):
    panel, index, bands = evidence_fixture()
    panel["artists"][0]["point_ids"].append("v8-a")
    panel["artists"][0]["actual_offsets"].append([10., 100.])
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_curve_artist_order_must_strictly_increase_training_window(api):
    panel, index, bands = evidence_fixture()
    panel["artists"][6]["point_ids"].reverse()
    panel["artists"][6]["actual_offsets"].reverse()
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_one_artist_cannot_mix_derived_categories(api):
    panel, index, bands = evidence_fixture()
    other = panel["artists"].pop(1)
    panel["artists"][0]["point_ids"].extend(other["point_ids"])
    panel["artists"][0]["actual_offsets"].extend(other["actual_offsets"])
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_each_derived_category_has_one_artist_not_split_groups(api):
    panel, index, bands = evidence_fixture()
    panel["artists"].append(dict(kind="scatter", marker="x", point_ids=["v8-b"],
                                 actual_offsets=[[10., 120.]]))
    panel["artists"][0]["point_ids"] = ["v8-a"]
    panel["artists"][0]["actual_offsets"] = [[10., 100.]]
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_detail_crop_lists_exactly_the_centers_in_view(api):
    panel, index, bands = evidence_fixture()
    panel["panel"] = "constructed_detail"
    panel["full_range"] = False
    panel["ylim"] = [-20., 60.]
    panel["visible_point_ids"] = [i for i,p in index.items()
                                  if 1. <= p["c"] <= 100. and -20. <= p["relative_loss_percent"] <= 60.]
    assert isinstance(api.audit_panel(panel, index, bands), dict)
    panel["visible_point_ids"].remove("hourly-a")
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_detail_crop_cannot_claim_an_out_of_view_center(api):
    panel, index, bands = evidence_fixture()
    panel["full_range"] = False
    panel["ylim"] = [-20., 60.]
    panel["visible_point_ids"] = [i for i in index if i not in ("v8-a", "v8-b")]
    panel["visible_point_ids"].append("v8-a")
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)


def test_method_population_cannot_be_reduced_in_panel_and_artists_together(api):
    panel, index, bands = evidence_fixture()
    panel["point_ids"].remove("v8-b")
    panel["visible_point_ids"].remove("v8-b")
    panel["artists"][0]["point_ids"].remove("v8-b")
    panel["artists"][0]["actual_offsets"].pop()
    with pytest.raises(api.AuditMismatch):
        api.audit_panel(panel, index, bands)
