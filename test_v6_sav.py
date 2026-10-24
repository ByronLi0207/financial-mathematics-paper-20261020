"""Synthetic contract tests; these fixtures never open the financial archive."""
import importlib
import importlib.util
from types import SimpleNamespace

import numpy as np
import pytest


def _sav():
    # Keep RED an assertion about the absent API, rather than a collection error.
    assert importlib.util.find_spec('v6_sav') is not None, 'headroom SAV API is not implemented'
    return importlib.import_module('v6_sav')


def _periodic():
    return np.tile([1., 9.], 20), np.full(40, 10.)


def test_recurrence_matches_independently_hand_calculated_values():
    # Catches a misplaced intercept, recurrence state or shock coefficient.
    sav = _sav()
    np.testing.assert_allclose(sav.sav_path([.5, .5, .25], [2., 4., 6.], 1.),
                               [1.5, 2.25, 3.125], rtol=0., atol=1e-14)


def test_constant_training_response_has_analytic_zero_loss_without_numeric_claim():
    # Catches fictitious optimizer convergence and omitted original normalization.
    sav = _sav()
    cfg = sav.SAVConfig(horizon=2, window=3, refit_step=4, segment_start=9)
    fit = sav.fit_sav_refit(np.full(20, 3.), np.full(20, 10.), 9, cfg)
    assert fit.status == 'ANALYTIC_CONSTANT'
    assert fit.objective == 0.
    assert fit.scale == 3.
    assert fit.selected_start is None
    assert fit.starts == ()
    np.testing.assert_array_equal(fit.coefficients, [1., 0., 0.])
    np.testing.assert_array_equal(fit.path_origins, [5, 6, 7, 8, 9])
    np.testing.assert_array_equal(fit.normalized_path, np.ones(5))


def test_training_pool_initialization_and_shocks_all_obey_h_maturity():
    # Catches G_(i-1) training leakage and q_init consuming a label ending later.
    sav = _sav()
    cfg = sav.SAVConfig(horizon=3, window=4, refit_step=3, segment_start=15)
    fit = sav.fit_sav_refit(np.full(30, 2.), np.ones(30), 15, cfg)
    np.testing.assert_array_equal(fit.training_origins, [9, 10, 11, 12])
    np.testing.assert_array_equal(fit.training_shock_origins, [6, 7, 8, 9])
    np.testing.assert_array_equal(fit.initialization_origins, [2, 3, 4, 5])
    assert int(fit.training_origins[-1]) + 3 == 15
    assert int(fit.initialization_origins[-1]) + 3 == 8


def test_initialization_uses_uncorrected_inverse_empirical_cdf_quantile():
    # Catches corrected-rank +inf/NA at initialization when a finite empirical q exists.
    sav = _sav()
    headroom = np.full(30, 3.)
    headroom[:3] = [1., 2., 8.]
    fit = sav.fit_sav_refit(headroom, np.ones(30), 9,
                            sav.SAVConfig(2, 3, 4, 9))
    assert fit.initial_quantile == 8. / 3.
    np.testing.assert_array_equal(fit.initialization_origins, [0, 1, 2])


def test_no_pretraining_mature_labels_is_terminal_na_even_for_constant_response():
    # Catches a zero/constant substitute used to bypass absent causal initialization.
    sav = _sav()
    with pytest.raises(sav.SAVFitError) as error:
        sav.fit_sav_refit(np.ones(20), np.ones(20), 9, sav.SAVConfig(3, 4, 3, 9))
    assert error.value.code == 'NO_INITIAL_MATURE_LABELS'
    assert error.value.refit_index == 9


def test_query_uses_newly_mature_h_lag_and_future_labels_cannot_change_earlier_issue():
    # Catches G_(t-1) query leakage and failure to advance recursion through actual t.
    sav = _sav()
    headroom, position = _periodic()
    cfg = sav.SAVConfig(2, 10, 10, 20)
    original = sav.forecast_sav(headroom, position, [20, 21], cfg)
    changed = headroom.copy()
    changed[19] = 100.
    changed[20:] = np.nan
    perturbed = sav.forecast_sav(changed, position, [20, 21], cfg)
    assert original.capacities[0] == perturbed.capacities[0]
    assert perturbed.capacities[1] > original.capacities[1]
    assert perturbed.capacities[1] - original.capacities[1] == pytest.approx(
        91. * original.refits[0].coefficients[2])
    np.testing.assert_array_equal(original.diagnostics['issue_shock_origins'], [18, 19])
    fit = original.refits[0]
    b0, b1, b2 = fit.coefficients
    previous = fit.normalized_path[-1]
    expected_next = b0 + b1 * previous + b2 * (9. / fit.scale)
    assert original.headroom_quantiles[1] == pytest.approx(fit.scale * expected_next)


def test_original_segment_grid_applies_when_first_requested_issue_is_between_refits():
    # Catches anchoring refits at origins[0] or using the refit anchor as the floor.
    sav = _sav()
    position = np.arange(30, dtype=float) - 18.
    result = sav.forecast_sav(np.zeros(30), position, [16, 17, 18],
                              sav.SAVConfig(2, 3, 3, 14))
    assert [fit.refit_index for fit in result.refits] == [14, 17]
    np.testing.assert_array_equal(result.diagnostics['issue_refit_origins'], [14, 17, 17])
    np.testing.assert_array_equal(result.capacities, [2., 1., 0.])
    assert result.diagnostics['floor_count'] == 3


def test_nonconstant_fit_retains_six_success_or_failure_receipts_and_bounded_coefficients():
    # Catches hidden starts and accepting an unbounded or nonfinite numerical fit.
    sav = _sav()
    headroom, position = _periodic()
    fit = sav.fit_sav_refit(headroom, position, 20, sav.SAVConfig(2, 10, 10, 20))
    assert fit.status == 'CONVERGED'
    assert len(fit.starts) == 6
    assert fit.starts[fit.selected_start].eligible
    assert np.isfinite(fit.objective)
    # A constant .95 quantile of 1.8 has normalized loss .04 here.
    # No global optimum or near-zero objective is promised by bounded Powell.
    assert fit.objective < .04
    assert 0. <= fit.coefficients[0] <= 100.
    assert 0. <= fit.coefficients[1] <= .995
    assert 0. <= fit.coefficients[2] <= 100.
    assert all(start.nfev > 0 and start.nit > 0 for start in fit.starts)
    assert all(start.bound_solutions is not None for start in fit.starts)


def test_all_start_nonconvergence_is_explicit_and_never_substitutes_a_forecast(monkeypatch):
    # The optimizer is the external numerical boundary: forcing its documented failure
    # exercises real selection/error handling, and asserts no mock-owned result.
    sav = _sav()
    import scipy.optimize
    def fail(_objective, x0, **_kwargs):
        return SimpleNamespace(success=False, x=np.array(x0), fun=1., nfev=3,
                               nit=1, message='synthetic iteration limit', status=1)
    monkeypatch.setattr(scipy.optimize, 'minimize', fail)
    headroom, position = _periodic()
    with pytest.raises(sav.SAVFitError) as error:
        sav.forecast_sav(headroom, position, [20, 21], sav.SAVConfig(2, 10, 10, 20))
    assert error.value.code == 'NO_CONVERGED_START'
    assert len(error.value.diagnostics['starts']) == 6
    assert not any(start.eligible for start in error.value.diagnostics['starts'])
    assert not hasattr(error.value, 'capacities')
    initial = [start.initial_coefficients for start in error.value.diagnostics['starts']]
    np.testing.assert_allclose(initial,
        [[1.43, .2, .01], [1.34, .2, .1], [.71, .6, .01],
         [.62, .6, .1], [.17, .9, .01], [.08, .9, .1]], rtol=0., atol=1e-14)


def test_later_refit_failure_returns_no_partial_cell_metrics(monkeypatch):
    # Catches silently returning the successful prefix after a later fit fails.
    sav = _sav()
    import scipy.optimize
    def fail(_objective, x0, **_kwargs):
        return SimpleNamespace(success=False, x=np.array(x0), fun=1., nfev=1,
                               nit=1, message='synthetic failure', status=1)
    monkeypatch.setattr(scipy.optimize, 'minimize', fail)
    headroom = np.zeros(30)
    headroom[10] = 1.
    with pytest.raises(sav.SAVFitError) as error:
        sav.forecast_sav(headroom, np.ones(30), np.arange(10, 15),
                         sav.SAVConfig(2, 3, 3, 10))
    assert error.value.refit_index == 13
    assert error.value.code == 'NO_CONVERGED_START'
    assert not hasattr(error.value, 'capacities')


def test_guard_checkpoint_abort_propagates_without_a_fallback():
    # Catches swallowing the root worker's hard resource failure as a failed start.
    sav = _sav()
    class WorkerLimit(RuntimeError):
        pass
    def checkpoint(*, stage):
        raise WorkerLimit(stage)
    with pytest.raises(WorkerLimit, match='sav_'):
        sav.forecast_sav(np.ones(30), np.ones(30), [14, 15],
                         sav.SAVConfig(2, 3, 3, 14), checkpoint=checkpoint)


def test_normalization_preserves_forecasts_under_a_change_of_source_units():
    # Catches fitting original-unit responses with normalized coefficients/bounds.
    sav = _sav()
    headroom, position = _periodic()
    cfg = sav.SAVConfig(2, 10, 10, 20)
    small = sav.forecast_sav(headroom, position, [20, 21], cfg)
    large = sav.forecast_sav(headroom * 100., position * 100., [20, 21], cfg)
    np.testing.assert_allclose(large.capacities, small.capacities * 100., rtol=1e-10)
    np.testing.assert_allclose(large.refits[0].coefficients, small.refits[0].coefficients, rtol=1e-10)


@pytest.mark.parametrize('origins', [[], [13, 14], [14, 16], [14., 15.], [15, 14], [True]])
def test_invalid_or_incomplete_issue_vectors_are_rejected(origins):
    # Catches favorable row deletion, silent origin rounding or pre-segment queries.
    sav = _sav()
    with pytest.raises(ValueError):
        sav.forecast_sav(np.ones(30), np.ones(30), origins, sav.SAVConfig(2, 3, 3, 14))


def test_only_mature_read_slices_must_be_finite_and_nonnegative():
    # Catches full-future validation leakage while retaining malformed mature-data rejection.
    sav = _sav()
    headroom = np.ones(30)
    headroom[13:] = np.nan
    result = sav.forecast_sav(headroom, np.ones(30), [14], sav.SAVConfig(2, 3, 3, 14))
    np.testing.assert_array_equal(result.capacities, [2.])
    headroom[12] = np.nan
    with pytest.raises(sav.SAVFitError) as error:
        sav.forecast_sav(headroom, np.ones(30), [14], sav.SAVConfig(2, 3, 3, 14))
    assert error.value.code == 'INVALID_MATURE_HEADROOM'


def test_selection_ignores_failed_starts_and_uses_first_exact_objective_tie(monkeypatch):
    # Catches accepting a lower objective with success=False, choosing the last
    # exact tie, or ranking solver.fun instead of the actual returned q path.
    sav = _sav()
    import scipy.optimize
    candidates = iter([
        (False, 1.8, .001), (True, 2., .05), (True, 1.8, .04),
        (True, 1.8, .04), (True, .1, .855), (True, 1.7, .085)])
    def controlled(_objective, _x0, **_kwargs):
        success, intercept, reported = next(candidates)
        return SimpleNamespace(success=success, x=np.array([intercept, 0., 0.]),
                               fun=reported, nfev=1, nit=1,
                               message='controlled numerical boundary', status=0 if success else 1)
    monkeypatch.setattr(scipy.optimize, 'minimize', controlled)
    headroom, position = _periodic()
    fit = sav.fit_sav_refit(headroom, position, 20, sav.SAVConfig(2, 10, 10, 20))
    assert fit.selected_start == 2
    assert fit.objective == pytest.approx(.04)
    assert fit.starts[0].success is False
    assert fit.starts[0].eligible is False
    assert fit.starts[2].bound_solutions == ('beta1_lower', 'beta2_lower')


def test_success_flag_cannot_admit_a_nonfinite_solver_result(monkeypatch):
    # Catches turning a reported numerical failure into a finite forecast merely
    # because the returned coefficients happen to be finite.
    sav = _sav()
    import scipy.optimize
    def nonfinite(_objective, x0, **_kwargs):
        return SimpleNamespace(success=True, x=np.array(x0), fun=np.nan,
                               nfev=1, nit=1, message='nonfinite', status=0)
    monkeypatch.setattr(scipy.optimize, 'minimize', nonfinite)
    headroom, position = _periodic()
    with pytest.raises(sav.SAVFitError) as error:
        sav.forecast_sav(headroom, position, [20], sav.SAVConfig(2, 10, 10, 20))
    assert error.value.code == 'NO_CONVERGED_START'
    assert all(start.status == 'NONFINITE_OBJECTIVE' for start in error.value.diagnostics['starts'])
