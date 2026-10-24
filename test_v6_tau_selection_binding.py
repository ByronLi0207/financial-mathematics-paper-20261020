import copy,importlib
import pytest

def api():
    helper=getattr(importlib.import_module('v6_tau_worker'),'validate_selection_binding',None)
    assert callable(helper),'selection binding helper missing'
    return helper

def fixture():
    cell={'status':'COMPLETE','reason':None,'selected_parameter':.01}
    validation={'status':'COMPLETE','reason':None,'selection':{'status':'SELECTED','parameter':.01}}
    evaluation={'status':'COMPLETE','selected_parameter':.01}
    return cell,validation,evaluation

def test_exact_binding_accepts_and_resource_evaluation_na_does_not_invent_parameter():
    c,v,e=fixture();assert api()(c,v,e) is None
    assert api()(c,v,{'status':'NA','reason':'RESOURCE_RSS'}) is None

@pytest.mark.parametrize('where,field,value',[
    ('cell','status','NA'),('cell','reason','bad'),('cell','selected_parameter',.1),
    ('evaluation','selected_parameter',.1)])
def test_changed_selected_status_reason_or_parameter_stops(where,field,value):
    c,v,e=fixture();(c if where=='cell' else e)[field]=value
    with pytest.raises(ValueError):api()(c,v,e)

def test_ineligible_validation_never_admits_complete_evaluation():
    c={'status':'NA','reason':'FAILED','selected_parameter':None}
    v={'status':'NA','reason':'FAILED','selection':{'status':'INELIGIBLE','parameter':None}}
    with pytest.raises(ValueError):api()(c,v,{'status':'COMPLETE','selected_parameter':None})
