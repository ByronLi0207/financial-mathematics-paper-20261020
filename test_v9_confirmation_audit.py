"""Constructed-input contracts for an independent, read-only WP2 oracle."""
import importlib.util
from pathlib import Path
import math
import numpy as np
import pytest

@pytest.fixture
def api():
    path=Path(__file__).parent/"notes/revision-v9/audit_wp2.py"
    spec=importlib.util.spec_from_file_location("independent_wp2_oracle",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def selection_design():
    return dict(menus={"QR33":[.001,.01,.1],"QR4":[.001,.01,.1,1.,10.]},validation_first=10,validation_last=13)

def candidates(method,statuses=None):
    menu=selection_design()["menus"][method]
    return [dict(penalty=p,status=(statuses or ["COMPLETE"]*len(menu))[i],origin_count=4,mean_loss=1.) for i,p in enumerate(menu)]

def test_selection_strict_menu_failure_vs_eligible_menu(api):
    qr33=candidates("QR33",["COMPLETE","FAILED","COMPLETE"])
    assert api.select_from_records(qr33,"QR33",selection_design())==dict(status="INELIGIBLE",penalty=None)
    qr4=candidates("QR4",["FAILED","COMPLETE","COMPLETE","COMPLETE","COMPLETE"])
    assert api.select_from_records(qr4,"QR4",selection_design())["penalty"]==.01

def test_selection_exact_tie_rules_and_menu_identity(api):
    assert api.select_from_records(candidates("QR33"),"QR33",selection_design())["penalty"]==.1
    assert api.select_from_records(candidates("QR4"),"QR4",selection_design())["penalty"]==.001
    with pytest.raises(api.AuditMismatch):api.select_from_records(candidates("QR4")[:-1],"QR4",selection_design())

def test_complete_candidate_requires_full_validation_and_finite_loss(api):
    rows=candidates("QR33");rows[0]["origin_count"]=3
    with pytest.raises(api.AuditMismatch):api.select_from_records(rows,"QR33",selection_design())
    rows=candidates("QR33");rows[0]["mean_loss"]=math.nan
    with pytest.raises(api.AuditMismatch):api.select_from_records(rows,"QR33",selection_design())

def record(rep,loss,status="COMPLETE"):
    return dict(rep=rep,status=status,evaluation=dict(mean_loss=loss,strict_breach_rate=.1) if status=="COMPLETE" else None)

def test_summary_ratio_of_means_and_full_missing_flag(api):
    a={0:record(0,1),1:record(1,9)};b={0:record(0,1),1:record(1,3)}
    result=api.independent_summary(a,b,2)
    assert result["full_procedure_relative_loss_percent"]==150.
    a[1]=record(1,0,"FAILED");result=api.independent_summary(a,b,2)
    assert result["failed_repetitions"]==1 and result["full_procedure_relative_loss_percent"] is None
    assert result["conditional_on_completion"] is True

def test_summary_failure_precedence_and_inventory(api):
    a={0:record(0,1,"NOT_ATTEMPTED")};b={0:record(0,1,"FAILED")}
    result=api.independent_summary(a,b,1)
    assert result["failed_repetitions"]==1 and result["unattempted_repetitions"]==0
    with pytest.raises(api.AuditMismatch):api.independent_summary({},b,1)

def test_fixed_denominator_missing_never_promotes_support(api):
    result=api.fixed_screen([True]*8+[None]*2,.8)
    assert result["status"]=="INCONCLUSIVE" and result["lower_bound"]==.8
    result=api.fixed_screen([False]*5+[None]*5,.8)
    assert result["status"]=="NOT_SUPPORT" and result["upper_bound"]==.5
    assert api.fixed_screen([True]*8+[False]*2,.8)["status"]=="SUPPORT"

def test_peak_target_includes_anchor_and_entire_future_path(api):
    assert np.array_equal(api.direct_peak(np.array([8.,-2.,3.,-10.]),np.array([0,1]),2),[8.,10.])

def trace_fixture(api):
    position=np.arange(40,dtype=float)%7-3
    design=dict(evaluation_first=28,evaluation_last=31,refit_step=2)
    origins=np.arange(28,32);peak=api.direct_peak(position,origins,2);floor=np.abs(position[origins]);cap=api.direct_f(position,origins,2,20,2)
    residual=peak-cap
    trace=dict(origins=origins,peak=peak,floor=floor,capacity=cap,refit_indices=np.array([28,28,30,30]),pinball=.95*np.maximum(residual,0)+.05*np.maximum(-residual,0),strict_breach=residual>0)
    return position,trace,design

def test_trace_recomputes_f_peak_floor_pinball_and_breaches(api):
    x,t,d=trace_fixture(api);score=api.check_trace(x,t,2,20,"F",d)
    assert score["n"]==4 and score["mean_loss"]>=0
    t["pinball"]=t["pinball"].copy();t["pinball"][0]+=1
    with pytest.raises(api.AuditMismatch):api.check_trace(x,t,2,20,"F",d)

@pytest.mark.parametrize("field",["peak","floor","refit_indices","strict_breach"])
def test_trace_corrupt_labels_clocks_and_strict_flags_are_rejected(api,field):
    x,t,d=trace_fixture(api);t[field]=t[field].copy();t[field][0]=not t[field][0] if field=="strict_breach" else t[field][0]+1
    with pytest.raises(api.AuditMismatch):api.check_trace(x,t,2,20,"F",d)

def test_maturity_rejects_future_label_and_incomplete_fit_grid(api):
    design=dict(evaluation_first=28,evaluation_last=31,refit_step=2,feature_valid_from=0,solver={"max_iter":10000})
    rows=[dict(refit_index=r,training_first_origin=r-2-20+1,training_last_origin=r-2,training_count=20,latest_label_end=r) for r in (28,30)]
    summary=dict(refit_count=2,training_first_origin_min=7,training_last_origin_max=28,latest_label_end_max=30,maximum_label_end_minus_refit=0)
    api.check_maturity(rows,summary,20,2,"evaluation",design,"F")
    rows[0]["latest_label_end"]=29
    with pytest.raises(api.AuditMismatch):api.check_maturity(rows,summary,20,2,"evaluation",design,"F")

def test_rng_regeneration_retains_same_innovations_across_phi(api):
    design=dict(burn_in=10,retained_observations=12,master_entropy=2026102492,initial_level=0.)
    a,sa=api.regenerate(0,2,.7,design);b,sb=api.regenerate(0,2,.9,design)
    assert sa["innovation_sha256"]==sb["innovation_sha256"] and sa["final_states"]==sb["final_states"]
    assert not np.array_equal(a,b) and a.shape==(12,)

def screen_fixture():
    design=dict(dgp=["student_t5","regime_3to1","compound_poisson"],phi=[.7,.9],windows=[52,260,720,2880],horizons=[6,24],
        thresholds={"QR33":{"r_star":106.49618468616566},"QR4":{"r_star":27.324522025270575}})
    rows=[]
    for dgp in design["dgp"]:
        for pi in range(2):
            for w in design["windows"]:
                for h in design["horizons"]:
                    for method in ("F","QR33","QR4"):
                        delta=0.
                        if method!="F":
                            r=w/(h+1);threshold=design["thresholds"][method]["r_star"]
                            if r<threshold/2:delta=10. if method=="QR33" else 1.
                            elif r>2*threshold:delta=-1. if method=="QR33" else -10.
                        rows.append(dict(dgp=dgp,phi_index=pi,window=w,horizon=h,method=method,full_procedure_relative_loss_percent=delta))
    return rows,design

def test_confirmation_full_population_subgroups_and_secondary_pairing(api):
    rows,design=screen_fixture();out=api.independent_screen(rows,design)
    assert out["primary_status"]=="SUPPORT" and out["P1"]["denominator"]==48 and out["P2"]["denominator"]==24
    assert out["P3"]["denominator"]==48 and out["P3"]["status"]=="SUPPORT"
    assert all(x["primary_status"]=="SUPPORT" for x in out["by_method"].values())
    assert all(x["primary_status"]=="SUPPORT" for x in out["by_DGP"].values())

def test_confirmation_primary_missing_is_inconclusive_and_zero_is_not_a_win(api):
    rows,design=screen_fixture()
    target=next(x for x in rows if x["method"]=="QR33" and x["window"]==52 and x["horizon"]==6)
    target["full_procedure_relative_loss_percent"]=None
    out=api.independent_screen(rows,design)
    assert out["primary_status"]=="INCONCLUSIVE" and out["P1"]["missing"]==1
    for item in rows:item["full_procedure_relative_loss_percent"]=0.
    out=api.independent_screen(rows,design)
    assert out["P1"]["successes"]==out["P2"]["successes"]==0 and out["primary_status"]=="NOT_SUPPORT"
    assert out["P3"]["status"]=="SUPPORT"
