"""Pure WP4 state/conditional-moment diagnostics under the frozen v6 contract.

The caller admits original report identities, original short-increment RMS, the
complete issue axis and the first QR fit's exact mature training pool/scale.
This module reads no files, changes no environment and launches no workers.
Joint GW moments include an intercept: rejection does not imply state dependence.
"""
from __future__ import annotations

import math
import numpy as np
import inference_tests as _original

_CONDITION_LIMIT = 1e12
_GROUPS = ('low', 'middle', 'high')
_RESTRICTIONS = np.array([[1., -1., 0.], [1., 0., -1.]])


def _positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError('INVALID_' + name)
    return int(value)


def _axis(value, name):
    raw = np.asarray(value)
    if (raw.ndim != 1 or not raw.size or raw.dtype.kind not in 'iu'
            or np.any(raw > np.iinfo(np.int64).max)):
        raise ValueError('INVALID_' + name)
    ids = raw.astype(np.int64, copy=False)
    if np.any(ids < 0) or np.any(np.diff(ids) != 1):
        raise ValueError('NONCONTIGUOUS_' + name)
    return ids


def _readonly(value):
    result = np.array(value, copy=True)
    result.flags.writeable = False
    return result


def past_increment_rms(position, window):
    """Past-only synthetic helper; finance callers retain original feature RMS.

    RMS_t=sqrt(mean((N_j-N_(j-1))**2, j=t-window+1,...,t)).
    The first window entries remain NaN, including when history is too short.
    """
    window = _positive_integer(window, 'RMS_WINDOW')
    x = np.asarray(position, dtype=float)
    if x.ndim != 1 or not x.size or not np.isfinite(x).all():
        raise ValueError('FINITE_POSITION_REQUIRED')
    out = np.full(len(x), np.nan)
    if len(x) > window:
        try:
            with np.errstate(over='raise', invalid='raise'):
                changes = np.diff(x)
                out[window:] = np.sqrt(np.convolve(changes * changes,
                                                   np.ones(window) / window, mode='valid'))
        except FloatingPointError as error:
            raise ValueError('NONFINITE_PAST_RMS') from error
    return _readonly(out)


def _reference(mean, covariance, *, n, df, bandwidth):
    """Wald with a fully retained finite positive well-conditioned covariance."""
    out = dict(status='NONFINITE_COVARIANCE', n=int(n), df=df, bandwidth=bandwidth,
               covariance_rank=None, covariance_condition=None,
               eigen_min=None, eigen_max=None, stat=None, p=None)
    if covariance.shape != (df, df) or not np.isfinite(covariance).all():
        return out
    try:
        rank = int(np.linalg.matrix_rank(covariance))
        eigen = np.linalg.eigvalsh(covariance)
        condition = float(np.linalg.cond(covariance))
    except np.linalg.LinAlgError:
        out['status'] = 'COVARIANCE_DECOMPOSITION_FAILURE'
        return out
    out.update(covariance_rank=rank,
               covariance_condition=condition if math.isfinite(condition) else None,
               eigen_min=float(eigen[0]) if math.isfinite(float(eigen[0])) else None,
               eigen_max=float(eigen[-1]) if math.isfinite(float(eigen[-1])) else None)
    if not np.isfinite(eigen).all():
        out['status'] = 'NONFINITE_EIGENVALUES'
    elif rank != df:
        out['status'] = 'RANK_DEFICIENT_COVARIANCE'
    elif eigen[0] <= 0:
        out['status'] = 'NONPOSITIVE_COVARIANCE'
    elif not math.isfinite(condition) or condition > _CONDITION_LIMIT:
        out['status'] = 'ILL_CONDITIONED_COVARIANCE'
    elif not np.isfinite(mean).all():
        out['status'] = 'NONFINITE_MOMENT_MEAN'
    else:
        try:
            with np.errstate(over='ignore', invalid='ignore'):
                stat = float(n * mean @ np.linalg.solve(covariance, mean))
            if not math.isfinite(stat) or stat < 0:
                out['status'] = 'NONFINITE_OR_NEGATIVE_WALD'
            else:
                p = float(_original.chi_tail(stat, df))
                if math.isfinite(p) and 0 <= p <= 1:
                    out.update(status='OK', stat=stat, p=p)
                else:
                    out['status'] = 'NONFINITE_REFERENCE_P'
        except (ArithmeticError, np.linalg.LinAlgError):
            out['status'] = 'WALD_REFERENCE_FAILURE'
    return out


def analyze_states(rms, losses_difference, origins, training_indices, *,
                   horizon, response_scale, return_private=False):
    """Analyze full-origin states and the fixed H-burn-in GW suffix.

    Default returns a JSON-safe aggregate dict. With return_private=True return
    (public, private_arrays). No origins/loss_difference/training_indices key is
    placed in private_arrays, so the caller can add its admitted input vectors.
    Only actually used training/evaluation RMS slices must be finite.
    """
    h = _positive_integer(horizon, 'HORIZON')
    ids, train = _axis(origins, 'ORIGIN_AXIS'), _axis(training_indices, 'TRAINING_POOL')
    if int(train[-1]) != int(ids[0]) - h:
        raise ValueError('TRAINING_POOL_NOT_INITIAL_EXACT_MATURE_WINDOW')
    a0 = float(response_scale)
    if isinstance(response_scale, (bool, np.bool_)) or not math.isfinite(a0) or a0 <= 0:
        raise ValueError('POSITIVE_FINITE_RESPONSE_SCALE_REQUIRED')
    state_history = np.asarray(rms, dtype=float)
    d = np.asarray(losses_difference, dtype=float)
    n = len(ids)
    if d.shape != (n,) or not np.isfinite(d).all():
        raise ValueError('FINITE_ALIGNED_LOSS_DIFFERENCE_REQUIRED')
    if state_history.ndim != 1 or max(int(ids[-1]), int(train[-1])) >= len(state_history):
        raise ValueError('RMS_HISTORY_DOES_NOT_COVER_USED_INDICES')
    training_rms, issued_rms = state_history[train], state_history[ids]
    if any(not np.isfinite(v).all() or np.any(v < 0) for v in (training_rms, issued_rms)):
        raise ValueError('FINITE_NONNEGATIVE_USED_RMS_REQUIRED')
    cut1, cut2 = map(float, np.quantile(training_rms, [1/3, 2/3], method='linear'))
    try:
        v0 = max(math.fsum(map(float, training_rms)) / len(train), 1e-12)
    except OverflowError as error:
        raise ValueError('NONFINITE_TRAINING_RMS_NORMALIZER') from error
    states = np.where(issued_rms <= cut1, 0, np.where(issued_rms <= cut2, 1, 2))
    counts = np.bincount(states, minlength=3)
    group_means = np.full(3, np.nan)
    influence = np.zeros((n, 3))
    group_rows = []
    for group, name in enumerate(_GROUPS):
        count = int(counts[group])
        row = dict(group=name, n=count, mean_difference=None, hac_se=None,
                   hac_status='EMPTY_GROUP')
        if count:
            try:
                mean = math.fsum(map(float, d[states == group])) / count
            except OverflowError as error:
                raise ValueError('NONFINITE_GROUP_MEAN') from error
            group_means[group] = mean
            with np.errstate(over='ignore', invalid='ignore'):
                influence[states == group, group] = (d[states == group] - mean) / (count / n)
            row['mean_difference'] = mean
        group_rows.append(row)
    group_bandwidth = int(_original.bandwidth(n, h))
    with np.errstate(over='ignore', invalid='ignore'):
        group_hac = _original.hac(influence, group_bandwidth)
    for group, row in enumerate(group_rows):
        if row['n']:
            variance = float(group_hac[group, group])
            if not math.isfinite(variance):
                row['hac_status'] = 'NONFINITE_COVARIANCE'
            elif variance < 0:
                row['hac_status'] = 'NONPOSITIVE_COVARIANCE'
            else:
                row.update(hac_se=math.sqrt(variance / n),
                           hac_status='OK' if variance > 0 else 'ZERO_LONG_RUN_VARIANCE')
    with np.errstate(over='ignore', invalid='ignore'):
        heterogeneity_hac = _RESTRICTIONS @ group_hac @ _RESTRICTIONS.T
    heterogeneity = _reference(_RESTRICTIONS @ group_means, heterogeneity_hac,
                               n=n, df=2, bandwidth=group_bandwidth)
    if np.any(counts == 0):
        heterogeneity.update(status='EMPTY_GROUP', stat=None, p=None)
    if np.isfinite(group_hac).all():
        try:
            heterogeneity['full_influence_covariance_rank'] = int(np.linalg.matrix_rank(group_hac))
        except np.linalg.LinAlgError:
            heterogeneity['full_influence_covariance_rank'] = None
    else:
        heterogeneity['full_influence_covariance_rank'] = None
    suffix_n = max(0, n - h)
    suffix_bandwidth = int(_original.bandwidth(suffix_n, h)) if suffix_n else None
    gw = dict(status='TOO_SHORT', n=suffix_n, full_n=n, burn_in=min(h, n),
              requested_burn_in=h, df=3, bandwidth=suffix_bandwidth,
              instrument_rank=None, covariance_rank=None, covariance_condition=None,
              eigen_min=None, eigen_max=None, stat=None, p=None)
    instruments = np.empty((0, 3))
    moments = np.empty((0, 3))
    gw_hac = np.full((3, 3), np.nan)
    if suffix_n:
        with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
            instruments = np.column_stack((np.ones(suffix_n), d[:-h] / a0,
                                           issued_rms[h:] / v0))
            moments = instruments * (d[h:] / a0)[:, None]
        if not np.isfinite(instruments).all() or not np.isfinite(moments).all():
            gw['status'] = 'NONFINITE_MOMENTS'
        else:
            try:
                instrument_rank = int(np.linalg.matrix_rank(instruments))
            except np.linalg.LinAlgError:
                instrument_rank = None
            with np.errstate(over='ignore', invalid='ignore'):
                gw_hac = _original.hac(moments, suffix_bandwidth)
            gw.update(_reference(np.mean(moments, axis=0), gw_hac,
                                 n=suffix_n, df=3, bandwidth=suffix_bandwidth))
            gw['instrument_rank'] = instrument_rank
            if instrument_rank != 3:
                gw.update(status='RANK_DEFICIENT_INSTRUMENTS', stat=None, p=None)
    public = dict(status='OK' if gw['status'] == heterogeneity['status'] == 'OK'
                  else 'PARTIAL_REFERENCE_NA', analysis_status='post-result / exploratory',
                  full_n=n, horizon=h, direction='new_minus_reference',
                  training_count=len(train), training_first=int(train[0]), training_last=int(train[-1]),
                  latest_training_label_end=int(train[-1]) + h,
                  cut1=cut1, cut2=cut2, cutpoint_method='training-only linear empirical terciles',
                  a0=a0, v0=v0, group_bandwidth=group_bandwidth,
                  groups=group_rows, heterogeneity=heterogeneity, gw=gw,
                  reference_note='Working-reference diagnostics with unverified limited-memory, moment, mixing and long-run covariance assumptions. GW includes an intercept; rejection alone does not establish position-increment RMS dependence.')
    if not return_private:
        return public
    private = dict(states=_readonly(states), group_influence=_readonly(influence),
                   group_influence_valid=_readonly(counts > 0), group_hac=_readonly(group_hac),
                   heterogeneity_hac=_readonly(heterogeneity_hac),
                   gw_origins=_readonly(ids[h:]), gw_lag_origins=_readonly(ids[:-h] if suffix_n else ids[:0]),
                   gw_instruments=_readonly(instruments), gw_moments=_readonly(moments),
                   gw_hac=_readonly(gw_hac))
    return public, private
