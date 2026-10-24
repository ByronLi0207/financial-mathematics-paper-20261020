"""Known-answer tests for the explicitly corrected D2 mechanism families."""
from statistics import NormalDist
import numpy as np
import pytest
from round2_levy_ar_correction import (
    level_endpoint_parameters, level_increment_autocorrelation,
    absolute_gaussian_quantile, level_paths, increment_paths,
    exceedance_counts, simulate_cell,
)


def test_level_difference_covariance_by_independent_matrix_construction():
    for phi in (.68, .85, .98):
        c=phi**np.abs(np.arange(7)[:,None]-np.arange(7)[None,:])
        d=np.diff(np.eye(7),axis=0)
        v=d@c@d.T
        assert np.allclose(np.diag(v),2*(1-phi),rtol=1e-13,atol=1e-15)
        for k in range(1,6):
            assert v[0,k]==pytest.approx(-(1-phi)**2*phi**(k-1),abs=5e-16)
            assert level_increment_autocorrelation(phi,k)==pytest.approx(v[0,k]/v[0,0],abs=3e-14)


def test_endpoint_variances_and_nonzero_conditional_mean():
    for h in (1,6,24):
        for phi in (.68,.85,.98):
            mu,v=level_endpoint_parameters(h,phi)
            assert mu==0
            c=phi**np.abs(np.arange(h+1)[:,None]-np.arange(h+1)[None,:])
            a=np.zeros(h+1);a[0]=-1;a[-1]=1
            assert v==pytest.approx(a@c@a,abs=5e-15)
            m,w=level_endpoint_parameters(h,phi,2.)
            assert m==pytest.approx(2*(phi**h-1))
            assert w==pytest.approx((1-phi**2)*sum(phi**(2*j) for j in range(h)),abs=5e-15)
            assert m<0


def test_folded_normal_quantiles_and_degenerate_distribution():
    q=absolute_gaussian_quantile(.975,0.,4.)
    assert q==pytest.approx(2*NormalDist().inv_cdf(.9875),abs=3e-14)
    for m in (-3.,.7,3.):
        q=absolute_gaussian_quantile(.975,m,1.4)
        z=NormalDist(m,1.4**.5)
        assert z.cdf(q)-z.cdf(-q)==pytest.approx(.975,abs=5e-15)
    assert absolute_gaussian_quantile(.975,-3.,0.)==3.


def test_level_recursion_includes_initial_position_and_sign_mirror():
    z=np.array([[0.,1.,-1.],[1.,2.,3.]])
    x=np.array([2.,-3.]);phi=.5
    p=level_paths(z,x,phi)
    np.testing.assert_array_equal(p[:,0],x)
    np.testing.assert_allclose(p[:,1],phi*x+(1-phi**2)**.5*z[:,0])
    np.testing.assert_allclose(level_paths(-z,-x,phi),-p,rtol=0,atol=0)
    deterministic=level_paths(np.zeros((1,5)),np.array([2.]),phi)
    assert np.max(abs(deterministic))==2.


def test_negative_increment_ar_is_not_level_mean_reversion():
    z=np.array([[1.,0.,0.]])
    np.testing.assert_allclose(increment_paths(z,-.6),[[0.,1.,.4,.76]])
    np.testing.assert_allclose(level_paths(z,np.array([0.]),.6),[[0.,.8,.48,.288]])


def test_strict_breach_endpoint_difference_and_h0_floor():
    paths=np.array([[2.,2.,3.],[2.,-4.,2.],[-2.,-2.,-3.]])
    assert exceedance_counts(paths,np.array([3.,3.,3.]))==(1,0)
    assert exceedance_counts(paths,np.array([2.,2.,2.]))==(3,2)
    with pytest.raises(ValueError):exceedance_counts(paths,np.array([1.,3.,3.]))


def test_fixed_seed_is_batch_invariant_for_random_levels_and_negative_increments():
    for model,phi,anchor in [('level',.85,'stationary'),('increment',-.6,'zero')]:
        a=simulate_cell(model,6,phi,anchor,137,17,88)
        b=simulate_cell(model,6,phi,anchor,137,137,88)
        assert a==b


def test_fixed_start_oracles_share_paths_and_have_distinct_information_labels():
    rows=simulate_cell('level',6,.68,'absolute95',103,20,9)
    assert len(rows)==2
    assert [r['q_information'] for r in rows]==['stationary_marginal_endpoint','conditional_endpoint_oracle']
    assert rows[0]['seed']==rows[1]['seed']
    assert rows[0]['initial_abs_value']==pytest.approx(NormalDist().inv_cdf(.975))
    assert rows[0]['oracle_abs_endpoint_quantile']!=rows[1]['oracle_abs_endpoint_quantile']
    assert all(not r['independence_premise'] for r in rows)
    assert all('increment_lag1_correlation' not in r for r in rows)
    assert all(r['stationary_reference_increment_lag1_correlation']==pytest.approx(-.16) for r in rows)


@pytest.mark.parametrize('args',[(0,.68), (6,1.),(True,.68),(6,float('nan'))])
def test_invalid_level_parameters_fail(args):
    with pytest.raises(ValueError):level_endpoint_parameters(*args)


@pytest.mark.parametrize('p,m,v',[(0.,0.,1.),(1.,0.,1.),(.975,float('nan'),1.),(.975,0.,-1.)])
def test_invalid_quantile_parameters_fail(p,m,v):
    with pytest.raises(ValueError):absolute_gaussian_quantile(p,m,v)
