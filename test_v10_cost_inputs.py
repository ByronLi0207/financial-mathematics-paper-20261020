"""Artificial temporary NPZ fixtures only; no real vectors or costs."""
from copy import deepcopy
import hashlib
import importlib
from pathlib import Path

import numpy as np
import pytest


def pin(path):
    raw=path.read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def fixture(root, method='QR4::QR4', provided=False):
    arrays=dict(origins=np.arange(3,dtype=np.int64),peak=np.array([4.,3.,5.]),
        capacities_matrix=np.array([[3.,4.],[4.,3.],[5.,5.]]),loss_matrix=np.zeros((3,2)),floor_000=np.ones(3))
    if provided:arrays['floor_001']=np.ones(3)
    old_reference='/old/reference.npz'
    row=dict(period='original_evaluation',normalized_source='fx_hourly',source='fx_hourly',horizon=6,window=720,
        family=method.split('::')[0],method=method.split('::')[1],trace_path='/old/candidate.npz',floor_key=None,
        scope_classification='requested_core_saved_method',
        floor_recovery=dict(trace_path=old_reference,key='frozen_F_floor',origin_axis_sha256_match=True))
    path=root/'group.npz';ref=root/'copied-reference.npz'
    np.savez(ref,frozen_F_origins=arrays['origins'],frozen_F_peak=arrays['peak'],frozen_F_floor=arrays['floor_000'])
    group=dict(identity={k:row[k] for k in ['period','normalized_source','horizon','window']},status='READY',
        private_path='group.npz',n=3,first_origin=0,last_origin=2,methods=[
            dict(method_id='F',method_class='matched_historical',column_index=0,floor_key='floor_000',provenance={}),
            dict(method_id=method,method_class='conditional',column_index=1,floor_key='floor_001' if provided else None,
                 provenance=dict(source_rows=[deepcopy(row)],original_trace_path=row['trace_path']))])
    inventory=dict(methods=[row],minimum_core_private_copy_manifest=[dict(path=old_reference,
        proposed_scratch_relative='copied-reference.npz',**pin(ref))])
    save_group(root,group,arrays)
    return group,inventory,arrays


def save_group(root,group,arrays):
    path=root/group['private_path'];np.savez(path,**arrays);group.update(pin(path))
    group['arrays']={k:dict(shape=list(v.shape),dtype=v.dtype.str,sha256=hashlib.sha256(v.tobytes()).hexdigest()) for k,v in arrays.items()}


def api():
    assert Path(__file__).with_name('v10_cost_inputs.py').is_file(),'E4 input adapter is absent'
    return importlib.import_module('v10_cost_inputs')


@pytest.mark.parametrize('method',['QR4::QR4','Levy::Levy_L'])
def test_allowlisted_missing_floor_is_exactly_recovered_from_pinned_new_copy(tmp_path,method):
    g,i,a=fixture(tmp_path,method);before=deepcopy((g,i))
    result=api().load_cost_group(g,i,tmp_path)
    assert set(result)=={'origins','target','floor','capacities','recovery_receipts'}
    assert np.array_equal(result['floor'],np.ones(3))
    assert np.array_equal(result['target'],a['peak'])
    assert np.array_equal(result['capacities'][method],a['capacities_matrix'][:,1])
    assert result['recovery_receipts'][0]['method_id']==method
    assert result['recovery_receipts'][0]['reference_id']=='F'
    assert (g,i)==before
    assert not result['floor'].flags.writeable


def test_provided_floors_need_no_recovery_or_old_file(tmp_path):
    g,i,a=fixture(tmp_path,provided=True);(tmp_path/'copied-reference.npz').unlink()
    result=api().load_cost_group(g,{},tmp_path)
    assert result['recovery_receipts']==[]
    assert set(result['capacities'])=={'F','QR4::QR4'}


@pytest.mark.parametrize('corruption',['file','array_pin','extra_key','origin','target_shape','columns'])
def test_frozen_group_integrity_errors_fail_whole_input(tmp_path,corruption):
    g,i,a=fixture(tmp_path)
    if corruption=='file':(tmp_path/'group.npz').write_bytes(b'changed')
    elif corruption=='array_pin':g['arrays']['peak']['sha256']='0'*64
    elif corruption=='extra_key':a['extra']=np.ones(3);np.savez(tmp_path/'group.npz',**a);g.update(pin(tmp_path/'group.npz'))
    elif corruption=='origin':a['origins']=np.array([0,1,3]);save_group(tmp_path,g,a)
    elif corruption=='target_shape':a['peak']=np.ones(2);save_group(tmp_path,g,a)
    else:g['methods'][1]['column_index']=0
    with pytest.raises(api().CostInputError):api().load_cost_group(g,i,tmp_path)


@pytest.mark.parametrize('corruption',['missing_F','missing_F_floor','different_provided_B','C_below_B','Y_below_B','unknown_missing'])
def test_no_reference_fallback_floor_repair_or_unknown_missing_floor(tmp_path,corruption):
    g,i,a=fixture(tmp_path,provided=corruption=='different_provided_B')
    if corruption=='missing_F':g['methods'][0]['method_id']='qualified::F'
    elif corruption=='missing_F_floor':g['methods'][0]['floor_key']=None
    elif corruption=='different_provided_B':a['floor_001'][0]=2.;save_group(tmp_path,g,a)
    elif corruption=='C_below_B':a['capacities_matrix'][0,1]=.5;save_group(tmp_path,g,a)
    elif corruption=='Y_below_B':a['peak'][0]=.5;save_group(tmp_path,g,a)
    else:g['methods'][1]['method_id']='conditional::unknown'
    with pytest.raises(api().CostInputError):api().load_cost_group(g,i,tmp_path)


@pytest.mark.parametrize('corruption',['wrong_identity','undeclared_recovery','copy_hash','copy_origin','copy_target','copy_floor','path_escape'])
def test_recovery_binds_full_identity_copy_hash_and_entire_origin_target_floor(tmp_path,corruption):
    g,i,a=fixture(tmp_path)
    if corruption=='wrong_identity':i['methods'][0]['window']=2880
    elif corruption=='undeclared_recovery':del i['methods'][0]['floor_recovery']
    elif corruption=='copy_hash':i['minimum_core_private_copy_manifest'][0]['sha256']='0'*64
    elif corruption=='path_escape':i['minimum_core_private_copy_manifest'][0]['proposed_scratch_relative']='../escape.npz'
    else:
        origins=a['origins'].copy();target=a['peak'].copy();floor=a['floor_000'].copy()
        if corruption=='copy_origin':origins[-1]=9
        elif corruption=='copy_target':target[-1]=6.
        else:floor[-1]=2.
        path=tmp_path/'copied-reference.npz';np.savez(path,frozen_F_origins=origins,frozen_F_peak=target,frozen_F_floor=floor)
        i['minimum_core_private_copy_manifest'][0].update(pin(path))
    with pytest.raises(api().CostInputError):api().load_cost_group(g,i,tmp_path)
