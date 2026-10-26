"""Toy-only acceptance tests for the predeclared v13 numerical repair."""
import numpy as np
import pytest


def test_repair_module_exposes_same_objective_solver():
    from v13_tau_repair import fit_adaptive_admm
    X=np.column_stack((np.ones(8),np.zeros(8)))
    y=np.arange(8,dtype=float)
    fit=fit_adaptive_admm(X,y,tau=.99,penalty=.01)
    assert abs(fit.coefficients[0]-7)<2e-4
    assert fit.coefficients[1]==0
    assert fit.primal_residual<=fit.primal_tolerance
    assert fit.dual_residual<=fit.dual_tolerance
    assert fit.duality_gap<=fit.gap_tolerance
    assert fit.dual_integer_sum==0
    assert not fit.coefficients.flags.writeable


def test_clarabel_requires_original_external_certificate():
    from v13_tau_repair import fit_clarabel
    rng=np.random.default_rng(340)
    X=np.column_stack((np.ones(60),rng.normal(size=(60,3))))
    y=1+X[:,1]*.8+rng.normal(size=60)
    fit=fit_clarabel(X,y,tau=.99,penalty=.1)
    assert fit.primal_residual<=fit.primal_tolerance
    assert fit.dual_residual<=fit.dual_tolerance
    assert fit.duality_gap<=fit.gap_tolerance
    assert fit.dual_integer_sum==0
    assert abs(np.mean(fit.dual_weights))<1e-15
    assert np.max(fit.dual_weights)<=.99
    assert np.min(fit.dual_weights)>=-.01


def test_adaptive_and_convex_solver_objectives_agree_on_toy():
    from v13_tau_repair import fit_adaptive_admm,fit_clarabel
    rng=np.random.default_rng(341)
    X=np.column_stack((np.ones(52),rng.normal(size=(52,4))))
    y=np.maximum(0,2+X[:,1]*.7+rng.normal(size=52))
    before=X.copy(); response=y.copy()
    a=fit_adaptive_admm(X,y,tau=.99,penalty=.01)
    b=fit_clarabel(X,y,tau=.99,penalty=.01)
    assert abs(a.primal_objective-b.primal_objective)<2e-6
    np.testing.assert_array_equal(X,before)
    np.testing.assert_array_equal(y,response)


def test_bad_input_is_rejected_without_solver_fallback():
    from v13_tau_repair import fit_repaired
    from conditional_quantile import QuantileFitError
    with pytest.raises(QuantileFitError,match='INTERCEPT_COLUMN_REQUIRED'):
        fit_repaired(np.zeros((4,2)),np.arange(4.),tau=.99,penalty=.01)
