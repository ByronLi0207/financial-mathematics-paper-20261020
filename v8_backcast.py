"""WP5 fixed-prefix arithmetic helpers; no source I/O or model fitting.

Only the declared standard-normal HAC comparison is implemented. There is no
HLN, extra sensitivity, coverage test, multiplicity adjustment or old-window fit.
The caller supplies complete declared traces and retains unavailable slots.
"""
from fractions import Fraction
import math
import numbers

import numpy as np

from study_core import stable_mean


def _integer(value, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError('integer outside declared range')
    return int(value)


def _finite(value, minimum=None):
    if (isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real)
            or not math.isfinite(value) or minimum is not None and value < minimum):
        raise ValueError('finite real scalar required')
    return float(value)


def _vector(values, *, nonnegative=False):
    array = np.asarray(values, dtype=np.float64)
    if (array.ndim != 1 or not array.size or not np.isfinite(array).all()
            or nonnegative and np.any(array < 0)):
        raise ValueError('finite complete vector required')
    return array


def _origins(values):
    array = np.asarray(values)
    if (array.ndim != 1 or not array.size or array.dtype.kind not in 'iu'
            or np.any(array < 0) or np.any(array > np.iinfo(np.int64).max)
            or np.any(np.diff(array.astype(np.int64)) != 1)):
        raise ValueError('contiguous nonnegative signed issue indices required')
    return array.astype(np.int64, copy=False)


def backcast_geometry(n, design):
    """Return the entire declared grid, even when its source is unavailable."""
    n = _integer(n, 1)
    sample = design['sample']
    valid = _integer(sample['feature_valid_from'])
    window = _integer(sample['longest_window'], 1)
    max_h = max(_integer(h, 1) for h in design['clock_and_target']['horizons'])
    first = valid + window + max_h - 1
    validation = _integer(sample['original_validation_first'], 1)
    last = validation - max_h - 1
    count = last - first + 1
    if (first != sample['evaluation_first'] or last != sample['evaluation_last']
            or count != sample['evaluation_count'] or max_h != sample['max_horizon']
            or count <= 0):
        raise ValueError('declared geometry identity mismatch')
    old_first, old_last = map(_integer, design['known_exposure']['R6_retro_evaluation'])
    overlap = max(0, min(last, old_last) - max(first, old_first) + 1)
    if overlap != design['known_exposure']['overlap_with_retro_evaluation_origins']:
        raise ValueError('declared old-window overlap mismatch')
    result = dict(status='READY', reason=None, evaluation_first=first,
        evaluation_last=last, evaluation_count=count, last_target_index=last+max_h,
        original_validation_first=validation,
        earliest_H24_W2880_training_origin=first-max_h-window+1,
        previous_retro_overlap_count=overlap, previously_unscored=False)
    if last + max_h >= n:
        result.update(status='NA_SAMPLE_SIZE', reason='INCOMPLETE_DECLARED_TARGET_GRID')
    return result


def normal_dm(d, h):
    """Declared normal DM only, matching the original Bartlett/divisor-n rule."""
    d = _vector(d); h = _integer(h, 1); n = len(d)
    if n <= h:
        raise ValueError('more complete observations than horizon required')
    lag_count = min(n-1, max(h, int(4*(n/100)**(2/9))))
    mean = math.fsum(map(float, d)) / n
    # Keep the original single-column matrix arithmetic. This intentionally
    # avoids calling dm_test, which also evaluates an unrequested HLN statistic.
    column = d[:, None]
    u = column - column.mean(axis=0)
    covariance = u.T @ u / n
    for lag in range(1, lag_count+1):
        gamma = u[lag:].T @ u[:-lag] / n
        covariance += (1-lag/(lag_count+1)) * (gamma+gamma.T)
    lrv = float(covariance[0, 0])
    if not math.isfinite(lrv) or not math.isfinite(mean):
        raise ValueError('nonfinite HAC comparison')
    result = dict(n=n, horizon=h, bandwidth=lag_count, mean_difference=mean,
                  lrv=lrv, dm_t=None, dm_p=None)
    if lrv <= 0 or np.all(d == d[0]):
        result['status'] = 'IDENTICAL_LOSSES' if np.all(d == 0) else 'ZERO_LONG_RUN_VARIANCE'
    else:
        statistic = mean / math.sqrt(lrv/n)
        if not math.isfinite(statistic):
            raise ValueError('nonfinite DM statistic')
        result.update(status='OK', dm_t=statistic,
                      dm_p=math.erfc(abs(statistic)/math.sqrt(2)))
    return result


def score_trace(origins, peak, capacity):
    """Summarize one declared trace with the original exact-rational loss."""
    ids = _origins(origins)
    peak = _vector(peak, nonnegative=True)
    capacity = _vector(capacity, nonnegative=True)
    if len(ids) != len(peak) or capacity.shape != peak.shape:
        raise ValueError('score trace shape mismatch')
    tau = Fraction(19, 20)
    with np.errstate(over='raise', invalid='raise'):
        error = peak-capacity
        pinball = float(tau)*np.maximum(error, 0.) + float(1-tau)*np.maximum(-error, 0.)
    count = int(np.count_nonzero(error > 0))
    return dict(n=len(ids), mean_loss=stable_mean(pinball),
                strict_breach_count=count, strict_breach_rate=count/len(ids))


def _complete_trace(trace):
    ids = _origins(trace['origins'])
    loss = _vector(trace['pinball'], nonnegative=True)
    hits = np.asarray(trace['strict_breach'])
    if (loss.shape != ids.shape or hits.shape != ids.shape
            or not np.isin(hits, [0, 1]).all()):
        raise ValueError('invalid complete loss/breach trace')
    return ids, loss, hits


def compare_traces(model, reference, h):
    """Compare complete paired grids; never silently truncate or drop issues."""
    ids, model_loss, model_hits = _complete_trace(model)
    ref_ids, ref_loss, ref_hits = _complete_trace(reference)
    if not np.array_equal(ids, ref_ids):
        raise ValueError('paired complete issue grids differ')
    n = len(ids)
    mean_model, mean_reference = stable_mean(model_loss), stable_mean(ref_loss)
    model_breaches, reference_breaches = int(np.count_nonzero(model_hits)), int(np.count_nonzero(ref_hits))
    return dict(status='COMPLETE', reason=None, n=n, exact_shared_origins=True,
        mean_model_loss=mean_model, mean_reference_loss=mean_reference,
        relative_change_percent=100*(mean_model/mean_reference-1) if mean_reference else None,
        model_breach_count=model_breaches, model_breach_rate=model_breaches/n,
        reference_breach_count=reference_breaches, reference_breach_rate=reference_breaches/n,
        dm=normal_dm(model_loss-ref_loss, h))


def classify_three_windows(rows, design):
    """Frozen H6 QR33 screen; secondary results cannot rescue a failed claim."""
    window_names = [window['name'] for window in design['three_window_summary']['windows']]
    references = ('F_matched', 'F_rolling720')
    expected = {(window, reference) for window in window_names for reference in references}
    index = {}
    for row in rows:
        if row.get('method') != 'QR33' or row.get('horizon') != 6:
            continue
        key = (row.get('window_name'), row.get('reference'))
        if key not in expected or key in index:
            raise ValueError('unexpected or duplicate primary comparison')
        index[key] = row
    missing = []; comparisons = []; matched_wins = 0; rolling_signs = set()
    for window in window_names:
        for reference in references:
            row = index.get((window, reference))
            value = None if row is None else row.get('relative_change_percent')
            case = dict(window_name=window, reference=reference,
                        status=None if row is None else row.get('status'), relative_change_percent=value)
            try:
                if row is None or row.get('status') != 'COMPLETE':
                    raise ValueError('unavailable comparison')
                value = _finite(value)
            except ValueError:
                missing.append(dict(case)); case['available'] = False
            else:
                case['available'] = True
                if reference == 'F_matched':
                    matched_wins += value < 0
                else:
                    rolling_signs.add(-1 if value < 0 else 1 if value > 0 else 0)
            comparisons.append(case)
    if missing:
        status = 'INCONCLUSIVE'
    elif matched_wins == 3 and -1 in rolling_signs and 1 in rolling_signs:
        status = 'SUPPORT_WITH_LIMITS'
    else:
        status = 'MISMATCH'
    return dict(status=status, method='QR33', horizon=6, planned_comparisons=6,
        missing_comparisons=len(missing), matched_wins=matched_wins,
        rolling_signs=sorted(rolling_signs), comparisons=comparisons,
        missing=missing, fresh_independent_third_period=False,
        independence_claim_status='FAIL_MISMATCH',
        previous_retro_overlap_count=design['known_exposure']['overlap_with_retro_evaluation_origins'])
