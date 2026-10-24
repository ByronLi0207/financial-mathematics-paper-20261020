"""Constructed boundaries: exposure records describe, never select, paths."""
import importlib
import numpy as np


def test_issue_label_and_training_exposures_include_cross_boundary_labels():
    m=importlib.import_module('v9_exposure')
    ids=np.r_[np.zeros(8,dtype=int),np.ones(8,dtype=int),np.zeros(8,dtype=int)]
    arm=dict(regime_ids=ids,transition_indices=np.array([8]),wrap_indices=np.array([16]))
    d=dict(horizon=2,validation_first=8,validation_last=11,evaluation_first=16,
           evaluation_last=19,windows=[4],refit_step=2)
    r=m.describe_geometry(arm,d)
    assert r['validation']['issue_regime_counts']=={'1':4}
    assert r['evaluation']['issue_regime_counts']=={'0':4}
    assert r['validation']['issue_forward_boundaries']==1
    assert r['evaluation']['issue_wrap_boundaries']==1
    first=r['validation']['training_refits'][0]
    assert first['refit_index']==8 and first['window']==4
    assert first['first_origin']==3 and first['last_origin']==6
    assert first['latest_label_end']==8
    assert first['labels_crossing_forward_boundary']==1
    assert first['forward_boundaries_in_label_union']==1
    assert first['wrap_boundaries_in_label_union']==0


def test_zero_break_arm_records_no_boundaries_and_all_exposures():
    m=importlib.import_module('v9_exposure')
    arm=dict(regime_ids=np.zeros(30,dtype=int),transition_indices=np.array([],dtype=int),wrap_indices=np.array([],dtype=int))
    d=dict(horizon=2,validation_first=10,validation_last=13,evaluation_first=20,
           evaluation_last=23,windows=[4,6],refit_step=2)
    r=m.describe_geometry(arm,d)
    assert r['retained_regime_counts']=={'0':30}
    assert r['evaluation']['labels_crossing_forward_boundary']==0
    assert len(r['evaluation']['training_refits'])==4
    assert r['evaluation']['training_refits'][-1]['first_origin']==15
