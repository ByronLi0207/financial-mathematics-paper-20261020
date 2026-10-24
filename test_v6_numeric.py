from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import patch
import sys
import v4_numeric as numeric

def test_v6_root_regeneration_accepts_exact_claim_and_rejects_context_swapped_number():
    expected={'type':'p','html':'A bound result is 15.00%.'}
    b={**expected,'_generator':'v6:fixture','_bindings':[]}
    with patch('v6_submission.generated',return_value=expected):
        assert numeric.validate_block(b)==[]
        bad=deepcopy(b);bad['html']='A bound result is 14.77%.'
        assert numeric.validate_block(bad)

def test_v6_supplement_dispatch_checks_regeneration_and_original_input_fingerprints():
    expected={'type':'table','caption':'Table S38. Complete inventory.','headers':['Score'],'rows':[['2.50']]}
    b={**deepcopy(expected),'_generator':'v6supp:fixture','_bindings':[]}
    with patch.dict(sys.modules,{'v6_supplement':SimpleNamespace(generated=lambda _:expected)}):
        assert numeric.validate_block(b)==[]
        b['rows'][0][0]='3.50';assert numeric.validate_block(b)

def test_new_reference_matches_verified_entry_and_existing_metadata_dispositions():
    assert hasattr(numeric,'expected_reference_html'),'reference extension missing'
    text=numeric.expected_reference_html('gibbs2021')
    assert '1660–1672' in text and 'Gibbs' in text
    assert numeric.expected_reference_html('gw2006') is not None
    assert numeric.expected_reference_html('UNVERIFIED_NEW_ID') is None

def test_new_math_mapping_is_context_checked_even_if_visible_html_numbers_match():
    expected={'type':'p','html':'The report is q.','inline_math':[{'html':'q','latex':r'a_\kappa q_t'}]}
    b={**deepcopy(expected),'_generator':'v6:fixture','_bindings':[]}
    with patch('v6_submission.generated',return_value=expected):
        assert numeric.validate_block(b)==[]
        b['inline_math'][0]['latex']=r'q_t'
        assert numeric.validate_block(b),'LaTeX-only scale removal must not evade contextual audit'
