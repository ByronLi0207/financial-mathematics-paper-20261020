"""Registered v9 synthetic AR(1)-GARCH-t path primitives; no source I/O.

Parameters are plain six-key dictionaries in normalized level units. The
caller owns calibration, moment qualification, resource limits and output.
This module neither fits parameters nor reads financial inputs.
"""
import copy
import hashlib
import math
import numbers

import numpy as np
from scipy.stats import t as student_t


_KEYS = frozenset(('intercept', 'phi', 'omega', 'alpha', 'beta', 'nu'))


def _integer(value, minimum=0):
    if (isinstance(value, (bool, np.bool_))
            or not isinstance(value, (int, np.integer)) or value < minimum):
        raise ValueError('invalid integer configuration')
    return int(value)


def _real(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise ValueError('finite real parameter required')
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('finite real parameter required')
    return result


def _parameters(params):
    if type(params) is not dict or set(params) != _KEYS:
        raise ValueError('exact six-key parameter dictionary required')
    p = {key: _real(value) for key, value in params.items()}
    if (abs(p['phi']) >= 1 or p['omega'] <= 0 or p['alpha'] < 0
            or p['beta'] < 0 or p['alpha'] + p['beta'] >= 1 or p['nu'] <= 2):
        raise ValueError('inadmissible finite-second-moment generator')
    return p


def _lengths(lengths):
    try:
        values = [_integer(value, 1) for value in lengths]
    except TypeError as exc:
        raise ValueError('nonempty integer dwell lengths required') from exc
    if not values:
        raise ValueError('nonempty integer dwell lengths required')
    return values


def _checkpoint(checkpoint, stage, step, total):
    if checkpoint is not None:
        checkpoint(stage=stage, step=step, total=total)


def standardized_t_shocks(uniforms, nu):
    """Transform open uniforms using a finite-variance standardized t law."""
    nu = _real(nu)
    if nu <= 2:
        raise ValueError('Student degrees of freedom must exceed two')
    raw = np.asarray(uniforms)
    if raw.dtype.kind not in 'iuf':
        raise ValueError('open finite real uniforms required')
    u = np.asarray(raw, dtype=np.float64)
    if not np.isfinite(u).all() or np.any(u <= 0) or np.any(u >= 1):
        raise ValueError('open finite real uniforms required')
    z = np.asarray(student_t.ppf(u, nu) * math.sqrt((nu - 2) / nu), dtype=np.float64)
    if not np.isfinite(z).all():
        raise ValueError('nonfinite standardized Student innovation')
    return z


def regime_schedule(lengths, phase, burn_in, retained):
    """Return full burn+retained regime IDs; retained index zero has `phase`."""
    lengths = _lengths(lengths)
    phase = _integer(phase)
    burn_in = _integer(burn_in)
    retained = _integer(retained, 1)
    period = sum(lengths)
    if phase >= period:
        raise ValueError('phase outside regime period')
    positions = (phase + np.arange(burn_in + retained, dtype=np.int64) - burn_in) % period
    boundaries = np.cumsum(lengths, dtype=np.int64)
    return np.asarray(np.searchsorted(boundaries, positions, side='right'), dtype=np.int64)


def simulate_constant_paths(params, n, bootstrap_repetitions, rng,
                            burn_in=20000, checkpoint=None):
    """Return independent path rows [B,n], retaining no burn trajectory.

    Draw one B-vector per time step from the caller's standard_t RNG. Each
    path has its own level, variance and innovation state throughout burn
    and retention. Initialization is previous level zero and first variance
    one; the registered fit restrictions are checked, never clipped here.
    """
    p = _parameters(params)
    n = _integer(n, 1)
    batch = _integer(bootstrap_repetitions, 1)
    burn_in = _integer(burn_in)
    if not callable(getattr(rng, 'standard_t', None)):
        raise ValueError('caller standard_t random generator required')
    if checkpoint is not None and not callable(checkpoint):
        raise ValueError('callable checkpoint required')
    output = np.empty((batch, n), dtype=np.float64)
    previous_level = np.zeros(batch, dtype=np.float64)
    previous_variance = np.ones(batch, dtype=np.float64)
    previous_innovation = np.zeros(batch, dtype=np.float64)
    standardization = math.sqrt((p['nu'] - 2) / p['nu'])
    total = burn_in + n
    for i in range(total):
        if i % 256 == 0:
            _checkpoint(checkpoint, 'constant_paths', i, total)
        draws = np.asarray(rng.standard_t(p['nu'], size=batch), dtype=np.float64)
        if draws.shape != (batch,) or not np.isfinite(draws).all():
            raise ValueError('invalid independent-path Student draw')
        try:
            with np.errstate(over='raise', invalid='raise', divide='raise'):
                variance = (np.ones(batch, dtype=np.float64) if i == 0 else
                    p['omega'] + p['alpha'] * previous_innovation ** 2
                    + p['beta'] * previous_variance)
                innovation = np.sqrt(variance) * (draws * standardization)
                level = p['intercept'] + p['phi'] * previous_level + innovation
        except FloatingPointError as exc:
            raise ValueError('nonfinite synthetic path recursion') from exc
        if (not np.isfinite(variance).all() or np.any(variance <= 0)
                or not np.isfinite(innovation).all() or not np.isfinite(level).all()):
            raise ValueError('nonfinite synthetic path recursion')
        if i >= burn_in:
            output[:, i - burn_in] = level
        previous_level, previous_variance, previous_innovation = level, variance, innovation
    _checkpoint(checkpoint, 'constant_paths', total, total)
    return output


def _retained_transitions(full_ids, burn_in):
    """Actual ID changes only; a single-regime clock has no transition."""
    changes = np.flatnonzero(full_ids[1:] != full_ids[:-1]) + 1
    changes = changes[changes >= burn_in]
    forward = changes[full_ids[changes] != 0] - burn_in
    wraps = changes[full_ids[changes] == 0] - burn_in
    return forward.astype(np.int64), wraps.astype(np.int64)


def generate_pair(constant_params, segment_params, lengths, source_index, rep,
                  repetitions, stream_tag, design, checkpoint=None):
    """Generate one registered constant/switching pair under common uniforms.

    The six retained vectors are accompanied by actual retained regime
    transitions and the complete uniform-stream identity. Parameters change
    at scheduled boundaries; all previous stochastic states carry across.
    No fitting, scoring, input reading, output writing or retry occurs.
    """
    constant = _parameters(constant_params)
    try:
        segments = [_parameters(p) for p in segment_params]
    except TypeError as exc:
        raise ValueError('segment parameter inventory required') from exc
    lengths = _lengths(lengths)
    if len(segments) != len(lengths):
        raise ValueError('segment and dwell inventories differ')
    source_index = _integer(source_index)
    rep = _integer(rep)
    repetitions = _integer(repetitions, 1)
    stream_tag = _integer(stream_tag)
    if rep >= repetitions:
        raise ValueError('repetition outside registered inventory')
    if type(design) is not dict:
        raise ValueError('design dictionary required')
    entropy = _integer(design['master_entropy'])
    burn_in = _integer(design['burn_in'])
    retained = _integer(design['retained_observations'], 1)
    if _integer(design.get('rng_namespace', 9)) != 9:
        raise ValueError('registered RNG namespace must be nine')
    if checkpoint is not None and not callable(checkpoint):
        raise ValueError('callable checkpoint required')
    phase = rep * sum(lengths) // repetitions
    full_ids = regime_schedule(lengths, phase, burn_in, retained)
    total = burn_in + retained
    _checkpoint(checkpoint, 'pair_paths', 0, total)
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(
        entropy, spawn_key=(9, stream_tag, source_index, rep))))
    initial = copy.deepcopy(rng.bit_generator.state)
    uniforms = rng.integers(1, 2**53, size=total, dtype=np.int64).astype(np.float64) / 2**53
    final = copy.deepcopy(rng.bit_generator.state)
    uniform_hash = hashlib.sha256(np.ascontiguousarray(uniforms, dtype='<f8').tobytes()).hexdigest()
    shocks = np.empty((2, total), dtype=np.float64)
    shocks[0] = standardized_t_shocks(uniforms, constant['nu'])
    for regime, p in enumerate(segments):
        mask = full_ids == regime
        shocks[1, mask] = standardized_t_shocks(uniforms[mask], p['nu'])
    arrays = {name: np.empty((2, retained), dtype=np.float64)
              for name in ('position', 'variance', 'innovations')}
    previous_level = [0., 0.]
    previous_variance = [1., 1.]
    previous_innovation = [0., 0.]
    for i in range(total):
        if i and i % 256 == 0:
            _checkpoint(checkpoint, 'pair_paths', i, total)
        for arm, p in enumerate((constant, segments[full_ids[i]])):
            try:
                variance = (1. if i == 0 else p['omega']
                    + p['alpha'] * previous_innovation[arm] ** 2
                    + p['beta'] * previous_variance[arm])
                innovation = math.sqrt(variance) * float(shocks[arm, i])
                level = p['intercept'] + p['phi'] * previous_level[arm] + innovation
            except (OverflowError, ValueError) as exc:
                raise ValueError('nonfinite synthetic path recursion') from exc
            if variance <= 0 or not all(math.isfinite(v) for v in (variance, innovation, level)):
                raise ValueError('nonfinite synthetic path recursion')
            if i >= burn_in:
                j = i - burn_in
                arrays['position'][arm, j] = level
                arrays['variance'][arm, j] = variance
                arrays['innovations'][arm, j] = innovation
            previous_level[arm] = level
            previous_variance[arm] = variance
            previous_innovation[arm] = innovation
    _checkpoint(checkpoint, 'pair_paths', total, total)
    forward, wraps = _retained_transitions(full_ids, burn_in)
    arms = {}
    for arm, name in enumerate(('constant', 'switching')):
        arms[name] = {field: values[arm].copy() for field, values in arrays.items()}
        arms[name].update(
            regime_ids=np.zeros(retained, dtype=np.int64) if arm == 0 else full_ids[burn_in:].copy(),
            transition_indices=np.empty(0, dtype=np.int64) if arm == 0 else forward,
            wrap_indices=np.empty(0, dtype=np.int64) if arm == 0 else wraps)
    return dict(**arms, phase=phase, uniform_sha256=uniform_hash,
                rng_initial=initial, rng_final=final)
