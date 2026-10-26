"""Artificial-input checks only: no financial inputs, fitting or study runs."""
import copy
import hashlib
import importlib
import importlib.util

import numpy as np
import pytest
from scipy.stats import t


def api():
    # A missing implementation fails as the intended RED assertion, not import noise.
    assert importlib.util.find_spec('v9_switching') is not None, 'v9_switching API not implemented'
    return importlib.import_module('v9_switching')


def params(**changes):
    p = dict(intercept=.4, phi=.2, omega=.3, alpha=.1, beta=.6, nu=6.)
    p.update(changes)
    return p


def design(burn=0, retained=12):
    return dict(master_entropy=2026102408, burn_in=burn, retained_observations=retained)


def pair(*, segments=None, lengths=None, rep=0, repetitions=4, tag=2,
         source=0, d=None, checkpoint=None):
    p = params()
    return api().generate_pair(p, [p] if segments is None else segments,
        [7] if lengths is None else lengths, source, rep, repetitions,
        tag, design() if d is None else d, checkpoint=checkpoint)


def test_four_public_apis_exist():
    m = api()
    for name in ('standardized_t_shocks', 'regime_schedule',
                 'simulate_constant_paths', 'generate_pair'):
        assert callable(getattr(m, name))


def test_standardized_t_inverse_cdf_preserves_quantiles_and_unit_scale():
    u = np.array([.1, .5, .9])
    got = api().standardized_t_shocks(u, 6.)
    np.testing.assert_allclose(got, t.ppf(u, 6.) * np.sqrt(2/3), rtol=0, atol=0)
    assert got.dtype == np.float64


def test_standardized_t_fixed_artificial_sample_has_unit_variance():
    # Catches omitted/wrong t variance normalization; never a study repetition.
    u = np.random.Generator(np.random.PCG64(87123)).random(300000)
    z = api().standardized_t_shocks(u, 8.)
    assert abs(float(z.mean())) < .015
    assert abs(float(z.var()) - 1.) < .025


@pytest.mark.parametrize('u', [[0.], [1.], [np.nan], [np.inf], [-.2]])
def test_closed_nonfinite_or_outside_uniform_is_rejected(u):
    with pytest.raises(ValueError):
        api().standardized_t_shocks(u, 6.)


@pytest.mark.parametrize('nu', [2., 1.9, np.inf, np.nan, True])
def test_infinite_variance_or_invalid_t_df_is_rejected(nu):
    with pytest.raises(ValueError):
        api().standardized_t_shocks([.5], nu)


def test_schedule_accounts_for_burn_phase_and_repeated_wrap():
    got = api().regime_schedule([2, 3], phase=4, burn_in=2, retained=7)
    np.testing.assert_array_equal(got, [1, 1, 1, 0, 0, 1, 1, 1, 0])
    assert got.dtype.kind in 'iu'


@pytest.mark.parametrize('lengths', [[], [0, 3], [-1, 3], [1.5, 3], [True, 3]])
def test_nonpositive_or_noninteger_dwell_lengths_are_rejected(lengths):
    with pytest.raises(ValueError):
        api().regime_schedule(lengths, 0, 0, 3)


class FixedTDraws:
    """Explicit RNG protocol fixture: predetermined independent column shocks."""
    def __init__(self, standardized, nu=6.):
        self.raw = np.asarray(standardized) / np.sqrt((nu-2)/nu)
        self.index = 0

    def standard_t(self, nu, size):
        row = self.raw[self.index]
        self.index += 1
        assert row.shape == (size,)
        return row.copy()


def test_null_batch_first_variance_and_garch_recursion_do_not_cross_paths():
    # With c=phi=0, output equals innovation, making each conditional variance observable.
    rng = FixedTDraws([[1., 2.], [-1., 1.], [1., -1.]])
    p = params(intercept=0., phi=0., omega=.2, alpha=.1, beta=.6)
    got = api().simulate_constant_paths(p, 3, 2, rng, burn_in=0)
    expected = np.array([[1., -np.sqrt(.9), np.sqrt(.83)],
                         [2., np.sqrt(1.2), -np.sqrt(1.04)]])
    np.testing.assert_allclose(got, expected, rtol=2e-15, atol=2e-15)
    assert got.shape == (2, 3) and got.dtype == np.float64


def test_null_batch_does_not_reset_level_at_retained_boundary():
    rng = FixedTDraws([[0.], [0.], [0.], [0.]])
    p = params(intercept=1., phi=.5, omega=1., alpha=0., beta=0.)
    got = api().simulate_constant_paths(p, 2, 1, rng, burn_in=2)
    np.testing.assert_array_equal(got, [[1.75, 1.875]])


def test_null_batch_draws_are_reproducible_and_distinct_by_path():
    p = params()
    a = api().simulate_constant_paths(p, 9, 4, np.random.default_rng(38), burn_in=10)
    b = api().simulate_constant_paths(p, 9, 4, np.random.default_rng(38), burn_in=10)
    np.testing.assert_array_equal(a, b)
    assert all(not np.array_equal(a[0], row) for row in a[1:])


def test_k_zero_reuses_identical_paths_and_has_no_artificial_transition():
    got = pair(d=design(burn=7, retained=21))
    for key in ('position', 'variance', 'innovations'):
        assert got['constant'][key].tobytes() == got['switching'][key].tobytes()
    for arm in ('constant', 'switching'):
        np.testing.assert_array_equal(got[arm]['regime_ids'], np.zeros(21, dtype=int))
        assert len(got[arm]['transition_indices']) == len(got[arm]['wrap_indices']) == 0


def test_switching_carries_previous_level_variance_and_innovation():
    p0 = params()
    p1 = params(intercept=-.7, phi=-.2, omega=.8, alpha=.05, beta=.3, nu=10.)
    got = pair(segments=[p0, p1], lengths=[2, 2], d=design(0, 6))
    s = got['switching']
    assert s['variance'][0] == 1.
    np.testing.assert_array_equal(s['regime_ids'], [0, 0, 1, 1, 0, 0])
    np.testing.assert_array_equal(s['transition_indices'], [2])
    np.testing.assert_array_equal(s['wrap_indices'], [4])
    assert s['variance'][2] == pytest.approx(.8 + .05*s['innovations'][1]**2 + .3*s['variance'][1])
    assert s['position'][2] == pytest.approx(-.7 - .2*s['position'][1] + s['innovations'][2])
    assert s['variance'][4] == pytest.approx(.3 + .1*s['innovations'][3]**2 + .6*s['variance'][3])
    assert s['position'][4] == pytest.approx(.4 + .2*s['position'][3] + s['innovations'][4])


def test_phase_grid_and_boundary_zero_include_burn_predecessor():
    p1 = params(intercept=-1.)
    d = design(2, 6)
    got = pair(segments=[params(), p1], lengths=[2, 3], rep=2, repetitions=5, d=d)
    assert got['phase'] == 2
    np.testing.assert_array_equal(got['switching']['regime_ids'], [1, 1, 1, 0, 0, 1])
    np.testing.assert_array_equal(got['switching']['transition_indices'], [0, 5])
    np.testing.assert_array_equal(got['switching']['wrap_indices'], [3])
    assert len(got['constant']['transition_indices']) == len(got['constant']['wrap_indices']) == 0


def test_pair_uses_registered_open_integer_uniform_stream_and_saves_rng_states():
    d = design(3, 8)
    got = pair(source=4, rep=1, repetitions=4, tag=2, d=d)
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(2026102408, spawn_key=(9, 2, 4, 1))))
    initial = copy.deepcopy(rng.bit_generator.state)
    u = rng.integers(1, 2**53, size=11, dtype=np.int64).astype(np.float64) / 2**53
    assert got['rng_initial'] == initial
    assert got['rng_final'] == rng.bit_generator.state
    assert got['uniform_sha256'] == hashlib.sha256(np.ascontiguousarray(u, dtype='<f8').tobytes()).hexdigest()
    z = t.ppf(u, 6.) * np.sqrt(2/3)
    np.testing.assert_allclose(got['constant']['innovations'] / np.sqrt(got['constant']['variance']), z[3:], rtol=2e-15, atol=2e-15)


def test_pair_reproducible_distinct_source_rep_and_pilot_streams():
    a = pair()
    b = pair()
    assert a['rng_initial'] == b['rng_initial'] and a['rng_final'] == b['rng_final']
    np.testing.assert_array_equal(a['constant']['position'], b['constant']['position'])
    hashes = {a['uniform_sha256'], pair(source=1)['uniform_sha256'],
              pair(rep=1)['uniform_sha256'], pair(tag=1)['uniform_sha256']}
    assert len(hashes) == 4


def test_pair_retains_only_requested_arrays_and_does_not_mutate_parameters():
    p = params()
    before = p.copy()
    d = design(11, 19)
    got = api().generate_pair(p, [p], [17], 0, 0, 2, 2, d)
    assert p == before
    for arm in ('constant', 'switching'):
        for key in ('position', 'variance', 'innovations', 'regime_ids'):
            assert got[arm][key].shape == (19,)
            assert np.isfinite(got[arm][key]).all()


@pytest.mark.parametrize('change', [dict(phi=1.), dict(omega=0.), dict(alpha=-.1),
    dict(alpha=.4, beta=.6), dict(nu=2.), dict(intercept=np.nan)])
def test_invalid_process_is_rejected_without_clipping(change):
    with pytest.raises(ValueError):
        api().simulate_constant_paths(params(**change), 2, 2, np.random.default_rng(3), burn_in=0)


def test_parameter_key_inventory_is_exact_and_no_fit_boundary_is_silently_changed():
    m = api()
    with pytest.raises(ValueError):
        m.simulate_constant_paths({**params(), 'extra': 1.}, 2, 1, np.random.default_rng(3), burn_in=0)
    with pytest.raises(ValueError):
        m.generate_pair(params(), [params()], [2, 3], 0, 0, 2, 2, design())
    p = params(phi=.999, alpha=.1, beta=.899)
    got = m.simulate_constant_paths(p, 2, 1, FixedTDraws([[0.], [0.]]), burn_in=0)
    np.testing.assert_allclose(got, [[.4, .7996]], rtol=0, atol=2e-16)


def test_checkpoints_cover_burn_and_retained_with_at_most_256_steps():
    marks = []
    api().simulate_constant_paths(params(), 281, 2, np.random.default_rng(5), burn_in=300,
        checkpoint=lambda **kw: marks.append(kw['step']))
    assert marks[0] == 0 and marks[-1] == 581
    assert max(np.diff(marks)) <= 256
    marks = []
    pair(d=design(300, 281), checkpoint=lambda **kw: marks.append(kw['step']))
    assert marks[0] == 0 and marks[-1] == 581
    assert max(np.diff(marks)) <= 256


def test_checkpoint_cancellation_propagates_before_another_path_step():
    class Stop(Exception):
        pass
    def stop(**kw):
        raise Stop('fixture cancellation')
    with pytest.raises(Stop):
        pair(checkpoint=stop)
    with pytest.raises(Stop):
        api().simulate_constant_paths(params(), 3, 2, np.random.default_rng(7), burn_in=0, checkpoint=stop)
