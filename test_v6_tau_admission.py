"""Independent synthetic receipt/full-axis admission tests; no financial I/O."""
import copy
import importlib

import numpy as np
import pytest


EXECUTION='c'*64
SELECTION='d'*64
CONTROLS={'fx_hourly':'a'*64,'nyfed_weekly':'b'*64}


def helper(name):
    module=importlib.import_module('v6_tau_worker')
    function=getattr(module,name,None)
    assert callable(function), name+' is not implemented'
    return function


def control_fixture(source='fx_hourly'):
    cfg={'validation_origin_first':10,'validation_origin_last':14,
         'evaluation_origin_first':20,'evaluation_origin_last':27,
         'primary_window':2880 if source=='fx_hourly' else 260}
    def check(method,phase,n,window=None):
        row={'method':method,'phase':phase,'n':n,'status':'EXACT_IDENTITY',
             'capacity_sha256':'a'*64,'original_trace_sha256':'b'*64}
        if window is not None:row['window']=window
        return row
    checks=[check('QR','validation',5),check('QR','evaluation',8),
            check('frozen_F','evaluation',8,cfg['primary_window'])]
    if source=='fx_hourly':checks.append(check('rolling_F','evaluation',8,720))
    receipt={'status':'COMPLETE_EXACT_IDENTITY','source':source,'tau':.95,
             'executable_freeze_sha256':EXECUTION,'checks':checks}
    return receipt,cfg


@pytest.mark.parametrize('source',['fx_hourly','nyfed_weekly'])
def test_control_admits_only_both_complete_qr_segments_and_named_full_f_controls(source):
    # Catches rejecting the real control schema or imposing a QR window field
    # absent from the writer's original exact-identity receipt entries.
    receipt,cfg=control_fixture(source)
    assert helper('validate_control_receipt')(receipt,source,cfg,EXECUTION) is None


@pytest.mark.parametrize('field,bad',[
    ('source','wrong-source'),('tau',.9),('status','COMPLETE'),
    ('executable_freeze_sha256','e'*64)])
def test_control_wrong_header_cannot_admit_new_tau_finance(field,bad):
    # Catches trusting a status while source, level or execution provenance differs.
    receipt,cfg=control_fixture();receipt[field]=bad
    with pytest.raises(ValueError):helper('validate_control_receipt')(receipt,'fx_hourly',cfg,EXECUTION)


@pytest.mark.parametrize('mutation',[
    'empty','missing_validation','duplicate','wrong_window','wrong_phase',
    'wrong_count','short_validation','not_exact','bad_capacity_hash','bad_original_hash'])
def test_control_requires_exact_nondeduplicated_full_segment_inventory(mutation):
    # Catches shortened evidence, silent set-deduplication, altered named F
    # histories, and missing/invalid cryptographic evidence.
    receipt,cfg=control_fixture()
    if mutation=='empty':receipt['checks']=[]
    elif mutation=='missing_validation':receipt['checks'].pop(0)
    elif mutation=='duplicate':receipt['checks'].append(copy.deepcopy(receipt['checks'][0]))
    elif mutation=='wrong_window':receipt['checks'][2]['window']=720
    elif mutation=='wrong_phase':receipt['checks'][0]['phase']='evaluation'
    elif mutation=='wrong_count':receipt['checks'][1]['n']=7
    elif mutation=='short_validation':receipt['checks'][0]['n']=4
    elif mutation=='not_exact':receipt['checks'][0]['status']='FAILED'
    elif mutation=='bad_capacity_hash':receipt['checks'][0]['capacity_sha256']='g'*64
    elif mutation=='bad_original_hash':receipt['checks'][0]['original_trace_sha256']=''
    with pytest.raises(ValueError):helper('validate_control_receipt')(receipt,'fx_hourly',cfg,EXECUTION)


def test_treasury_control_cannot_add_a_second_independent_primary_matched_history():
    # Catches adding a fourth named F control to the declared Treasury three checks.
    receipt,cfg=control_fixture('nyfed_weekly')
    receipt['checks'].append({'method':'rolling_F','window':720,'phase':'evaluation','n':8,
        'status':'EXACT_IDENTITY','capacity_sha256':'a'*64,'original_trace_sha256':'b'*64})
    with pytest.raises(ValueError):helper('validate_control_receipt')(receipt,'nyfed_weekly',cfg,EXECUTION)


def phase_fixture(phase='validation',status='COMPLETE'):
    receipt={'source':'fx_hourly','level':'90','tau':.9,'phase':phase,'status':status,
             'point95_controls':copy.deepcopy(CONTROLS),'executable_freeze_sha256':EXECUTION}
    if phase=='evaluation':receipt['selection_freeze_sha256']=SELECTION
    return receipt


@pytest.mark.parametrize('phase',['validation','evaluation'])
@pytest.mark.parametrize('status',['COMPLETE','NA'])
def test_phase_headers_and_immutable_control_hashes_are_checked_for_complete_and_na(phase,status):
    # Catches requiring numerical arrays for declared NA, or skipping its provenance.
    receipt=phase_fixture(phase,status)
    selection=SELECTION if phase=='evaluation' else None
    assert helper('validate_phase_receipt')(receipt,'fx_hourly','90',phase,CONTROLS,
                                           EXECUTION,selection_freeze=selection) is None


@pytest.mark.parametrize('field,bad',[
    ('source','nyfed_weekly'),('level','99'),('tau',.99),('phase','validation'),
    ('executable_freeze_sha256','e'*64),('selection_freeze_sha256','e'*64)])
@pytest.mark.parametrize('status',['COMPLETE','NA'])
def test_phase_wrong_identity_stops_even_when_scores_are_unavailable(field,bad,status):
    # Catches accepting a receipt for a different source/tau/phase/freeze.
    receipt=phase_fixture('evaluation',status);receipt[field]=bad
    with pytest.raises(ValueError):
        helper('validate_phase_receipt')(receipt,'fx_hourly','90','evaluation',CONTROLS,
                                         EXECUTION,selection_freeze=SELECTION)


@pytest.mark.parametrize('mutation',['missing','changed','extra'])
def test_phase_control_digest_inventory_is_exact_and_cannot_drift(mutation):
    # Catches a point95 control overwritten or swapped after validation was issued.
    receipt=phase_fixture()
    if mutation=='missing':receipt['point95_controls'].pop('nyfed_weekly')
    elif mutation=='changed':receipt['point95_controls']['fx_hourly']='f'*64
    else:receipt['point95_controls']['other_source']='f'*64
    with pytest.raises(ValueError):
        helper('validate_phase_receipt')(receipt,'fx_hourly','90','validation',CONTROLS,EXECUTION)


def arrays_fixture():
    arrays={'origins':np.arange(20,24),'peak':np.array([5.,6.,7.,8.]),
            'floor':np.array([1.,2.,3.,4.]),'QR':np.array([6.,5.,8.,9.]),
            'matched_F':np.array([5.,7.,6.,10.]),'primary_F':np.array([6.,6.,7.,8.])}
    return arrays,arrays['origins'].copy(),arrays['peak'].copy(),arrays['floor'].copy()


def test_evaluation_arrays_admit_exact_axis_target_and_feasible_named_reports():
    # Catches interpreting primary_F and matched_F as required-identical FX controls.
    arrays,ids,peak,floor=arrays_fixture()
    assert helper('validate_evaluation_arrays')(arrays,ids,peak,floor) is None


@pytest.mark.parametrize('mutation',[
    'shortened','shifted','gapped','target','floor','nonfinite_peak','negative_floor','peak_below_floor',
    'missing_report','qr_below_floor','matched_below_floor','primary_below_floor','nonfinite_report','wrong_shape'])
def test_evaluation_identity_or_geometry_failure_stops_without_row_deletion(mutation):
    # Catches favorable shortened origins, self-consistent wrong targets, altered
    # floors, a missing constituent, and reports that violate the feasible bound.
    arrays,ids,peak,floor=arrays_fixture()
    if mutation=='shortened':
        for key in arrays:arrays[key]=arrays[key][1:]
    elif mutation=='shifted':arrays['origins']+=1
    elif mutation=='gapped':arrays['origins'][2]+=10
    elif mutation=='target':arrays['peak'][0]+=1.
    elif mutation=='floor':arrays['floor'][0]+=.5
    elif mutation=='nonfinite_peak':arrays['peak'][0]=np.nan
    elif mutation=='negative_floor':arrays['floor'][0]=-1.;floor[0]=-1.
    elif mutation=='peak_below_floor':arrays['peak'][0]=0.;peak[0]=0.
    elif mutation=='missing_report':arrays.pop('matched_F')
    elif mutation=='qr_below_floor':arrays['QR'][0]=.5
    elif mutation=='matched_below_floor':arrays['matched_F'][0]=.5
    elif mutation=='primary_below_floor':arrays['primary_F'][0]=.5
    elif mutation=='nonfinite_report':arrays['primary_F'][0]=np.inf
    elif mutation=='wrong_shape':arrays['QR']=np.array([[6.,5.,8.,9.]])
    with pytest.raises(ValueError):helper('validate_evaluation_arrays')(arrays,ids,peak,floor)
