"""Independent synthetic clocks/HAC/null fixtures for frozen WP4 diagnostics."""
from fractions import Fraction
import importlib
import importlib.util
import json
import math

import numpy as np
import pytest


def api():
    assert importlib.util.find_spec('v6_states') is not None, 'WP4 state API is not implemented'
    return importlib.import_module('v6_states')


def scalar_hac(values, bandwidth):
    # Independent scalar Fraction oracle: no production covariance helper.
    x = list(map(lambda value: Fraction(str(value)), values))
    n = len(x)
    mean = sum(x) / n
    u = [value - mean for value in x]
    result = sum(value * value for value in u) / n
    for lag in range(1, bandwidth + 1):
        gamma = sum(u[t] * u[t-lag] for t in range(lag, n)) / n
        result += 2 * Fraction(bandwidth+1-lag, bandwidth+1) * gamma
    return float(result)


def fixture():
    rms = np.full(50, np.nan)
    rms[16:20] = [0., 1., 2., 3.]
    rms[20:26] = [0., 2., 3., 0., 2., 3.]
    return rms, np.array([1., 10., 100., 3., 14., 106.]), np.arange(20, 26), np.arange(16, 20)


def test_group_influence_hac_retains_the_complete_nonconsecutive_clock():
    # Catches compressing group dates, wrong p_g scaling, uncentered HAC or wrong n.
    public, private = api().analyze_states(*fixture(), horizon=1, response_scale=2., return_private=True)
    assert public['full_n'] == 6
    assert public['group_bandwidth'] == 2
    assert [g['n'] for g in public['groups']] == [2, 2, 2]
    assert [g['mean_difference'] for g in public['groups']] == [2., 12., 103.]
    np.testing.assert_array_equal(private['group_influence'],
        [[-3., 0., 0.], [0., -6., 0.], [0., 0., -9.],
         [3., 0., 0.], [0., 6., 0.], [0., 0., 9.]])
    # Low-group influence has zeros at intervening origins, variance=3 and L=2
    # autocovariances=0. Compressed [1,3] would incorrectly give SE=.5.
    assert public['groups'][0]['hac_se'] == pytest.approx(math.sqrt(.5))
    assert private['group_hac'][0, 0] == 3.
    assert public['groups'][0]['hac_se'] != pytest.approx(.5)
    for j in range(3):
        assert private['group_hac'][j,j] == pytest.approx(
            scalar_hac(private['group_influence'][:,j],2))


def test_two_restriction_heterogeneity_uses_full_influence_covariance():
    # Catches replacing equal group means by the intercept-only equal-accuracy null.
    public, private = api().analyze_states(*fixture(), horizon=1, response_scale=2., return_private=True)
    assert public['heterogeneity']['df'] == 2
    assert public['heterogeneity']['status'] == 'OK'
    # Independently assemble covariance of low-mid and low-high influences.
    contrasts = [[-3.,6.,0.,3.,-6.,0.],[-3.,0.,9.,3.,0.,-9.]]
    v00 = scalar_hac(contrasts[0],2)
    v11 = scalar_hac(contrasts[1],2)
    summed = [a+b for a,b in zip(*contrasts)]
    v01 = (scalar_hac(summed,2)-v00-v11)/2
    np.testing.assert_allclose(private['heterogeneity_hac'],[[v00,v01],[v01,v11]],rtol=1e-14)
    # Closed-form inverse of the independent2x2 covariance.
    u,v=-10.,-101.
    expected = 6*(v11*u*u-2*v01*u*v+v00*v*v)/(v00*v11-v01*v01)
    assert public['heterogeneity']['stat'] == pytest.approx(expected)
    assert public['heterogeneity']['p'] == pytest.approx(math.exp(-expected/2))


def test_gw_lag_is_t_minus_h_after_explicit_burn_in_with_frozen_normalizers():
    # Catches d_(t-1), suffix row shifting, evaluation-fitted scales or centered instruments.
    rms=np.full(40,np.nan);rms[14:19]=[1.,2.,3.,4.,5.]
    rms[20:28]=[1.,3.,5.,1.,3.,5.,1.,3.]
    losses=[1.,3.,-1.,2.,0.,5.,-2.,4.]
    public, private=api().analyze_states(rms,losses,np.arange(20,28),np.arange(14,19),
                                        horizon=2,response_scale=2.,return_private=True)
    assert public['a0']==2. and public['v0']==3.
    assert public['gw']['full_n']==8 and public['gw']['n']==6 and public['gw']['burn_in']==2
    assert public['gw']['bandwidth']==2
    np.testing.assert_array_equal(private['gw_origins'],[22,23,24,25,26,27])
    np.testing.assert_array_equal(private['gw_lag_origins'],[20,21,22,23,24,25])
    np.testing.assert_allclose(private['gw_instruments'][0],[1.,.5,5/3])
    np.testing.assert_allclose(private['gw_moments'][0],[-.5,-.25,-5/6])
    np.testing.assert_allclose(private['gw_instruments'][-1],[1.,2.5,1.])
    np.testing.assert_allclose(private['gw_moments'][-1],[2.,5.,2.])
    assert private['gw_hac'][0,0]==pytest.approx(scalar_hac([-.5,1.,0.,2.5,-1.,2.],2))


def test_rms_and_state_thresholds_are_prefix_only_with_no_future_refitting():
    # Catches forward-looking RMS or estimating terciles/normalizers on evaluation.
    module=api()
    positions=np.array([0.,1.,3.,6.,10.,15.,21.])
    original=module.past_increment_rms(positions,3)
    changed=positions.copy();changed[4:]+=1000.
    perturbed=module.past_increment_rms(changed,3)
    assert np.isnan(original[:3]).all()
    assert original[3]==pytest.approx(math.sqrt(14/3))
    np.testing.assert_array_equal(original[:4],perturbed[:4])
    rms,losses,origins,training=fixture()
    before, private=module.analyze_states(rms,losses,origins,training,horizon=1,response_scale=2.,return_private=True)
    altered=rms.copy();altered[23:26]=1e8
    after, changed_private=module.analyze_states(altered,losses,origins,training,horizon=1,response_scale=2.,return_private=True)
    assert (before['cut1'],before['cut2'],before['v0'])==(1.,2.,1.5)
    assert (after['cut1'],after['cut2'],after['v0'])==(1.,2.,1.5)
    np.testing.assert_array_equal(private['states'][:3],changed_private['states'][:3])


def test_state_ties_are_low_then_middle_and_collapsed_groups_are_not_repaired():
    # Catches changing <= boundaries or moving cutpoints to force nonempty groups.
    rms,losses,origins,training=fixture()
    rms[20:26]=[1.,2.,2.5,1.,2.,2.5]
    public,private=api().analyze_states(rms,losses,origins,training,horizon=1,response_scale=2.,return_private=True)
    np.testing.assert_array_equal(private['states'],[0,1,2,0,1,2])
    rms[training]=1.
    public=api().analyze_states(rms,losses,origins,training,horizon=1,response_scale=2.)
    assert public['cut1']==public['cut2']==1.
    assert public['groups'][1]['n']==0
    assert public['groups'][1]['mean_difference'] is None
    assert public['heterogeneity']['status']=='EMPTY_GROUP'
    assert public['heterogeneity']['p'] is None


def test_gw_can_reject_mean_advantage_while_equal_state_means_have_no_heterogeneity():
    # Catches interpreting a joint GW rejection as volatility dependence.
    rms=np.full(180,np.nan);rms[14:19]=[0.,.75,1.5,2.25,3.]
    rms[20:140]=np.tile([.25,1.5,2.75],40)
    noise=np.tile([-.4,.4,-.3,.3,-.2,.2,-.1,.1],5)
    losses=np.repeat(-3.+noise,3)
    public=api().analyze_states(rms,losses,np.arange(20,140),np.arange(14,19),horizon=2,response_scale=1.)
    assert [g['mean_difference'] for g in public['groups']]==[-3.,-3.,-3.]
    assert public['heterogeneity']['status']=='OK'
    assert public['heterogeneity']['stat']==0.
    assert public['heterogeneity']['p']==1.
    assert public['gw']['status']=='OK'
    assert public['gw']['p']<.001
    assert public['gw']['df']==3 and public['gw']['instrument_rank']==3
    assert public['gw']['covariance_condition']<=1e12


def test_constant_loss_and_constant_rms_preserve_singular_na_without_dropping_instruments():
    # Catches reducing to an intercept test or manufacturing p=1 after rank failure.
    rms=np.ones(40)
    public=api().analyze_states(rms,np.full(12,-2.),np.arange(20,32),np.arange(14,19),horizon=2,response_scale=1.)
    assert public['gw']['status']=='RANK_DEFICIENT_INSTRUMENTS'
    assert public['gw']['df']==3
    assert public['gw']['instrument_rank']==1
    assert public['gw']['p'] is None
    assert public['heterogeneity']['status']=='EMPTY_GROUP'
    assert public['full_n']==12 and sum(g['n'] for g in public['groups'])==12


def test_zero_within_group_variance_is_explicit_singular_covariance_na():
    # Catches displaying a valid equal-means p after zero long-run covariance.
    rms,losses,origins,training=fixture()
    public=api().analyze_states(rms,np.ones(6),origins,training,horizon=1,response_scale=1.)
    assert public['heterogeneity']['status']=='RANK_DEFICIENT_COVARIANCE'
    assert public['heterogeneity']['p'] is None
    assert all(g['hac_status']=='ZERO_LONG_RUN_VARIANCE' for g in public['groups'])


def test_short_gw_suffix_keeps_full_group_denominators():
    # Catches shortening state summaries to the GW suffix or indexing a future lag.
    rms=np.ones(40)
    public=api().analyze_states(rms,[1.,2.],[20,21],np.arange(13,19),horizon=2,response_scale=1.)
    assert public['full_n']==2
    assert public['gw']['n']==0 and public['gw']['status']=='TOO_SHORT'
    assert sum(g['n'] for g in public['groups'])==2


def test_unobserved_early_and_future_rms_nan_is_allowed_but_used_nan_is_not():
    # Catches scanning unused RMS history or dropping malformed actual issues.
    parts=fixture()
    public=api().analyze_states(*parts,horizon=1,response_scale=2.)
    assert public['full_n']==6
    parts[0][22]=np.nan
    with pytest.raises(ValueError,match='USED_RMS'):
        api().analyze_states(*parts,horizon=1,response_scale=2.)


@pytest.mark.parametrize('origin,training',[
    ([20,22],np.arange(14,19)),([20,21],[14,16,18]),([20,21],np.arange(15,20)),
    ([20.,21.],np.arange(14,19)),([True],np.arange(14,19))])
def test_bad_full_axis_or_nonmature_training_pool_is_rejected(origin,training):
    # Catches compressed issue dates, favorable training deletion or immature labels.
    with pytest.raises(ValueError):
        api().analyze_states(np.ones(40),np.ones(len(origin)),origin,training,horizon=2,response_scale=1.)


def test_nonfinite_moments_are_na_without_a_smaller_instrument_menu():
    # Catches normalizing overflow, deleting moments, or retaining a misleading p.
    rms,losses,origins,training=fixture()
    public=api().analyze_states(rms,losses,origins,training,horizon=1,response_scale=1e-308)
    assert public['gw']['status']=='NONFINITE_MOMENTS'
    assert public['gw']['df']==3 and public['gw']['p'] is None


def test_public_output_is_json_safe_aggregate_only_and_native_unit_rescaling_is_invariant():
    # Catches leaking influence arrays or fitting a0/v0 from evaluation data.
    parts=fixture();module=api()
    before=module.analyze_states(*parts,horizon=1,response_scale=2.)
    after=module.analyze_states(parts[0]*10,parts[1]*100,parts[2],parts[3],horizon=1,response_scale=200.)
    assert after['heterogeneity']['stat']==pytest.approx(before['heterogeneity']['stat'])
    assert after['gw']['stat']==pytest.approx(before['gw']['stat'])
    assert after['groups'][0]['hac_se']==pytest.approx(100*before['groups'][0]['hac_se'])
    json.dumps(before,allow_nan=False)
    def no_arrays(value):
        assert not isinstance(value,np.ndarray)
        if isinstance(value,dict):
            for v in value.values():no_arrays(v)
        elif isinstance(value,(list,tuple)):
            for v in value:no_arrays(v)
    no_arrays(before)


def test_nonfinite_eigendecomposition_remains_json_safe_na():
    # Catches storing inf eigen diagnostics after a finite huge covariance input.
    result=api()._reference(np.ones(3),np.full((3,3),1e308),n=6,df=3,bandwidth=2)
    assert result['status']=='NONFINITE_EIGENVALUES'
    assert result['eigen_max'] is None
    assert result['p'] is None
    json.dumps(result,allow_nan=False)


def test_positive_full_rank_covariance_must_also_pass_condition_gate():
    # Catches accepting a full-rank but unstable inverse, or centering/dropping
    # the nearly constant RMS instrument to force an eligible smaller menu.
    rng=np.random.default_rng(20261023)
    losses=.3+rng.normal(size=120)
    state_increments=rng.normal(size=120)
    results=[]
    for amplitude in (1e-5,1e-6):
        rms=np.full(160,np.nan);rms[14:19]=[1.,2.,3.,4.,5.]
        rms[20:140]=3+amplitude*state_increments
        result=api().analyze_states(rms,losses,np.arange(20,140),np.arange(14,19),
                                    horizon=2,response_scale=1.)['gw']
        assert result['instrument_rank']==result['covariance_rank']==3
        assert result['eigen_min']>0
        results.append(result)
    assert results[0]['covariance_condition']<1e12
    assert results[0]['status']=='OK' and results[0]['p'] is not None
    assert results[1]['covariance_condition']>1e12
    assert results[1]['status']=='ILL_CONDITIONED_COVARIANCE'
    assert results[1]['p'] is None and results[1]['stat'] is None
