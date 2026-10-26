"""Numerical contracts for the frozen v9 post-hoc analysis; no financial DGP."""
import importlib
import math
from fractions import Fraction
import numpy as np
import pytest

@pytest.fixture
def api():
    try:
        return importlib.import_module("v9_posthoc")
    except ModuleNotFoundError as error:
        if error.name != "v9_posthoc":
            raise
        pytest.fail("WP1 saved-result analysis is not implemented", pytrace=False)

def test_metric_denominators_use_nominal_coefficients_and_overlap(api):
    assert api.metric_value(260, 6, "QR33", "a") == Fraction(130,17)
    assert api.metric_value(260, 6, "QR4", "b") == Fraction(52,7)
    assert api.metric_value(260, 24, "QR4", "c") == Fraction(52,5)

def test_relative_change_is_ratio_of_means_not_mean_of_ratios(api):
    assert api.relative_change([1.,9.],[1.,3.]) == pytest.approx(150.)

def test_zero_reference_is_reported_not_divided_or_imputed(api):
    with pytest.raises(ValueError,match="reference"):
        api.relative_change([1.,2.],[0.,0.])

def test_candidate_selection_uses_integer_accuracy_then_predeclared_simplicity(api):
    assert api.select_candidate({"a":110,"b":110,"c":110},144)=="c"
    assert api.select_candidate({"a":120,"b":121,"c":110},144)=="b"
    with pytest.raises(ValueError):
        api.select_candidate({"a":120,"b":121},144)

def test_crossing_interpolates_in_raw_not_log_metric(api):
    out=api.describe_crossings([1.,5.],[2.,-2.])
    assert out["status"]=="IDENTIFIED"
    assert out["r_star"]==pytest.approx(3.)

def test_multiple_crossings_retain_all_and_choose_first(api):
    out=api.describe_crossings([1.,2.,3.,4.],[2.,-2.,2.,-2.])
    assert out["crossings"]==pytest.approx([1.5,3.5])
    assert out["r_star"]==pytest.approx(1.5)

def test_exact_zero_endpoint_is_not_lost(api):
    out=api.describe_crossings([1.,2.,3.],[2.,0.,-2.])
    assert out["r_star"]==pytest.approx(2.)

def test_left_censoring_and_missing_crossing_do_not_extrapolate(api):
    out=api.describe_crossings([1.,2.,3.],[-1.,2.,-2.])
    assert out["status"]=="UNIDENTIFIED_LEFT_CENSORED" and out["r_star"] is None
    assert out["crossings"]==pytest.approx([2.5])
    out=api.describe_crossings([1.,2.],[2.,1.])
    assert out["status"]=="UNIDENTIFIED_NO_CROSSING" and out["r_star"] is None

def test_same_metric_groups_equal_weight_cell_percentages(api):
    r,y=api.group_curve([Fraction(1),Fraction(1),Fraction(2)],[100.,-20.,-10.])
    assert r==[1.,2.] and y==pytest.approx([40.,-10.])

def test_cluster_resampling_preserves_paired_ratio_in_every_draw(api):
    reference=np.array([[1.,3.,10.],[2.,6.,20.]])
    model=reference*np.array([[1.2],[.8]])
    indices=np.random.default_rng(345).integers(0,3,size=(30,3))
    draws=api.bootstrap_roots([Fraction(1),Fraction(3)],model,reference,indices)
    assert len(draws)==30
    assert all(x["r_star"]==pytest.approx(2.) for x in draws)

def test_missing_bootstrap_roots_remain_in_full_draw_envelope(api):
    roots=[float(i) for i in range(1,19)]+[None,None]
    result=api.percentile_intervals(roots)
    assert result["finite_count"]==18 and result["missing_count"]==2
    assert result["finite_only"]["lower"]==1. and result["finite_only"]["upper"]==18.
    assert result["all_draw_envelope"]["lower"]==0.
    assert result["all_draw_envelope"]["upper"] is None
    assert result["all_draw_envelope"]["upper_unbounded"] is True

def test_final_evaluation_field_is_used_instead_of_validation_candidate(api):
    report={"status":"COMPLETE","evaluation":{"mean_loss":7.,"n":72,"strict_breach_count":3,"strict_breach_rate":3/72},"candidates":[{"mean_loss":999.}]}
    out=api.read_evaluation(report)
    assert out["mean_loss"]==7. and out["n"]==72
    with pytest.raises(ValueError):
        api.read_evaluation({"status":"COMPLETE","candidates":[{"mean_loss":999.}]})

def test_missing_source_fingerprint_fails_closed(api,tmp_path):
    source=tmp_path/"sealed.csv";source.write_text("old bytes")
    with pytest.raises(ValueError,match="fingerprint"):
        api.assert_fingerprint(source,"0"*64)

def test_matched_overlay_refuses_different_issue_count(api):
    row={"origin_count":"10","mean_pinball":"2","status":"COMPLETE"}
    reference={"origin_count":"11","mean_pinball":"1"}
    result=api.overlay_pair(row,reference,"fx_hourly",720,24,"QR33","sealed.csv",2)
    assert result["status"]=="NA_MISMATCH" and result["relative_loss_percent"] is None

def test_overlay_retains_original_failure_instead_of_using_apparent_loss(api):
    row={"origin_count":"10","mean_pinball":"2","status":"FAILED"}
    reference={"origin_count":"10","mean_pinball":"1"}
    result=api.overlay_pair(row,reference,"fx_hourly",720,24,"QR33","sealed.csv",2)
    assert result["status"]=="NA_SOURCE_FAILED" and result["relative_loss_percent"] is None

def test_overlay_uses_matched_loss_with_original_row_locator(api):
    row={"origin_count":"10","mean_pinball":"2","status":"COMPLETE"}
    reference={"origin_count":"10","mean_pinball":"1"}
    result=api.overlay_pair(row,reference,"fx_hourly",720,24,"QR33","sealed.csv",2)
    assert result["relative_loss_percent"]==100.
    assert result["source_row"]==2 and result["source_file"]=="sealed.csv"

def test_cluster_draw_indices_change_root_with_exact_shared_rep_pairing(api):
    reference=np.ones((2,2)); model=np.array([[3.,2.],[.5,0.]])
    draws=api.bootstrap_roots([Fraction(1),Fraction(3)],model,reference,np.array([[0,0],[1,1],[0,1]]))
    assert [d["r_star"] for d in draws]==pytest.approx([2.6,2.,7/3])

def test_one_missing_draw_need_not_make_envelope_unbounded(api):
    out=api.percentile_intervals([float(i) for i in range(1,100)]+[None])
    assert out["all_draw_envelope"]=={"lower":4.,"upper":95.,"upper_unbounded":False,"coverage_guarantee":False}

def classification_cells():
    return [{"window":(52,260,720,2880)[i%4],"horizon":(6,24)[i%2],"method":("QR33","QR4")[i%2],"relative_loss_percent":-1. if i%3==0 else 0.} for i in range(144)]

def test_logistic_decision_zero_is_no_win(api,monkeypatch):
    import sklearn.linear_model
    class ZeroDecision:
        def __init__(self,**kwargs): pass
        def fit(self,x,y):
            self.coef_=np.array([[0.]]);self.intercept_=np.array([0.]);self.n_iter_=np.array([1]);return self
        def decision_function(self,x): return np.zeros(len(x))
    monkeypatch.setattr(sklearn.linear_model,"LogisticRegression",ZeroDecision)
    scores,chosen=api.candidate_scores(classification_cells())
    assert all(row["correct"]==96 for row in scores.values()) and chosen=="c"

def test_logistic_convergence_warning_blocks_selection(api,monkeypatch):
    import sklearn.linear_model
    from sklearn.exceptions import ConvergenceWarning
    import warnings
    class FailedFit:
        def __init__(self,**kwargs): pass
        def fit(self,x,y): warnings.warn("synthetic nonconvergence",ConvergenceWarning)
    monkeypatch.setattr(sklearn.linear_model,"LogisticRegression",FailedFit)
    with pytest.raises(ConvergenceWarning): api.candidate_scores(classification_cells())

def test_logistic_maximum_iterations_blocks_selection(api,monkeypatch):
    import sklearn.linear_model
    class MaxIteration:
        def __init__(self,**kwargs): pass
        def fit(self,x,y): self.n_iter_=np.array([10000]);return self
    monkeypatch.setattr(sklearn.linear_model,"LogisticRegression",MaxIteration)
    with pytest.raises(ValueError,match="iteration"): api.candidate_scores(classification_cells())

def test_nonfinite_delta_blocks_classifier_before_turning_nan_into_no_win(api):
    cells=classification_cells();cells[0]["relative_loss_percent"]=float("nan")
    with pytest.raises(ValueError,match="nonfinite"): api.candidate_scores(cells)

def test_touching_zero_is_retained_without_claiming_strict_win(api):
    out=api.describe_crossings([1.,2.,3.],[2.,0.,2.])
    assert out["r_star"]==2. and out["y"][-1]>0
    assert api.describe_crossings([1.,2.],[0.,-1.])["status"]=="UNIDENTIFIED_LEFT_CENSORED"

def test_bootstrap_combines_ratio_of_means_then_equal_cell_groups(api):
    reference=np.array([[1.,3.],[2.,6.],[1.,2.]])
    model=reference*np.array([[2.],[1.4],[.5]])
    draws=api.bootstrap_roots([Fraction(1),Fraction(1),Fraction(3)],model,reference,np.array([[0,1]]))
    assert draws[0]["r_star"]==pytest.approx(1+2*70/120)
