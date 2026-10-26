"""Known arithmetic independent of financial fitted outcomes."""
import math
from round2_baselines_verify import scalar_dm,classification

def test_scalar_bartlett_known_alternating_loss_difference():
    # Centered sequence is[-1,1]*4: gamma0=1,gamma1=-7/8,
    # Bartlett L1 weights2*(1/2), so LRV=1/8 and DM t=8.
    r=scalar_dm([0.,2.]*4,1,1)
    assert r['mean_difference']==1.
    assert r['lrv']==.125 and r['dm_t']==8.
    assert r['hln_t']==8*math.sqrt(7/8)
    assert abs(r['dm_p']-math.erfc(8/math.sqrt(2)))<1e-28

def test_successful_optimizer_rejected_only_by_frozen_persistence_gate_is_not_nonconvergence():
    r=dict(status='NA',failure_context={'detail':{'garch_failure':{'native_parameters':{'omega':1.,'alpha':.5,'beta':.5000000002},'optimizer':{'convergence_flag':0}}}})
    q=classification(r)
    assert q['kind']=='PERSISTENCE_GATE_WITH_OPTIMIZER_SUCCESS'
    assert q['optimizer_convergence_flag']==0
    assert q['excess_over_declared_ceiling']>0
    assert 'not optimizer nonconvergence' in q['interpretation']

def test_structural_POT_NA_and_complete_record_are_separate():
    assert classification({'status':'COMPLETE'})=={'kind':'COMPLETE'}
    r={'status':'NA','window':52,'failure_reason':'POT structurally unavailable: insufficient tail','failure_context':{}}
    q=classification(r)
    assert q['kind']=='POT_STRUCTURAL_TAIL_SIZE'
    assert q['maximum_nominal_tail_count']==5 and q['required_strict_exceedances']==20
