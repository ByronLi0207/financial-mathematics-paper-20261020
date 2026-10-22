"""Causal fixed-pool ordinary/corrected empirical headroom-rank ablation.

I selects the lower empirical .95 pinball minimizer rank ceil(19 W / 20).
F retains ceil(19 (W+1) / 20). When 19 W / 20 is integral, both distinct
adjacent order statistics are endpoints of the empirical minimizer interval;
the corrected report is not generally a non-ERM report. At W52, ranks 50/51
differ and only rank 50 is an ordinary minimizer for distinct responses.

This module opens no files, evaluates no future target and performs no tuning.
Only labels completed by each refit enter that refit's frozen pool. The actual
query supplies the current magnitude. Providing no post-query observations is
valid; prediction does not require an evaluation outcome.
"""
import numpy as np


def _positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError('invalid ' + name)
    value = int(value)
    if value < 1:
        raise ValueError('invalid ' + name)
    return value


def ranks(window):
    """Return exact one-based lower-ordinary and add-one ranks at tau=19/20.

For a small window the add-one rank can exceed W; predict explicitly rejects
that unavailable report instead of inventing a fallback or interpolation.
"""
    window = _positive_integer(window, 'window')
    return ((19 * window + 19) // 20, (19 * (window + 1) + 19) // 20)


def predict(positions, origins, horizon, window, refit_step):
    """Issue I/F with a shared frozen completed-label pool and issue floor.

Origins must be nonempty consecutive nonnegative integer indices. For segment
start t0, r=t0+d*floor((t-t0)/d). At r, training origins run from r-H-W+1
through r-H, inclusive. Every historical response max(|N_i|,...,|N_(i+H)|)
is completed at r. Both ranks use exactly the same duplicate-preserving
headrooms. The returned per-issue arrays bind ranks to their actual pool
bounds and schedule. They are copies marked read-only.

Positions supplied through the last issue must be finite real numbers. Any
post-issue suffix is irrelevant and is not used in arithmetic or validation.
There is no partial-segment success, interpolation, fallback or clipping.
"""
    horizon = _positive_integer(horizon, 'horizon')
    window = _positive_integer(window, 'window')
    refit_step = _positive_integer(refit_step, 'refit step')
    ordinary, corrected = ranks(window)
    if corrected > window:
        raise ValueError('unavailable corrected rank')

    raw_ids = np.asarray(origins)
    if raw_ids.ndim != 1 or not raw_ids.size or raw_ids.dtype.kind not in 'iu':
        raise ValueError('invalid issue origins')
    if (np.any(raw_ids > np.iinfo(np.int64).max) or np.any(raw_ids < 0)
            or np.any(raw_ids[1:] <= raw_ids[:-1])):
        raise ValueError('invalid issue origins')
    ids = raw_ids.astype(np.int64, copy=True)
    if np.any(np.diff(ids) != 1):
        raise ValueError('nonconsecutive issue origins')
    raw_positions = np.asarray(positions)
    if (raw_positions.ndim != 1 or raw_positions.dtype.kind not in 'iuf'
            or int(ids[-1]) >= len(raw_positions)):
        raise ValueError('invalid positions or out-of-range issue')
    try:
        x = np.array(raw_positions[:int(ids[-1]) + 1], dtype=np.float64, copy=True)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError('invalid positions') from exc
    if not np.isfinite(x).all():
        raise ValueError('nonfinite positions through last issue')
    if int(ids[0]) - horizon - window + 1 < 0:
        raise ValueError('insufficient completed history')

    n = len(ids)
    result = {'origins': ids, 'I': np.empty(n), 'F': np.empty(n),
              'floors': np.empty(n), 'refit_indices': np.empty(n, dtype=np.int64),
              'training_first_origins': np.empty(n, dtype=np.int64),
              'training_last_origins': np.empty(n, dtype=np.int64),
              'latest_label_ends': np.empty(n, dtype=np.int64)}
    previous_refit = None
    first_issue = int(ids[0])
    try:
        with np.errstate(over='raise', invalid='raise'):
            for j, index in enumerate(ids):
                t = int(index)
                r = first_issue + ((t - first_issue) // refit_step) * refit_step
                first = r - horizon - window + 1
                last = r - horizon
                if r != previous_refit:
                    # This slice ends exactly at refit r: no unresolved label
                    # or later query value enters the frozen response pool.
                    magnitudes = np.abs(x[first:r + 1])
                    peaks = magnitudes[:window].copy()
                    for h in range(1, horizon + 1):
                        np.maximum(peaks, magnitudes[h:h + window], out=peaks)
                    headrooms = peaks - magnitudes[:window]
                    if not np.isfinite(headrooms).all() or np.any(headrooms < 0):
                        raise ValueError('invalid completed headrooms')
                    ordered = np.sort(headrooms)
                    lower = float(ordered[ordinary - 1])
                    upper = float(ordered[corrected - 1])
                    previous_refit = r
                floor = abs(float(x[t]))
                result['I'][j] = np.float64(floor) + lower
                result['F'][j] = np.float64(floor) + upper
                result['floors'][j] = floor
                result['refit_indices'][j] = r
                result['training_first_origins'][j] = first
                result['training_last_origins'][j] = last
                result['latest_label_ends'][j] = last + horizon
    except FloatingPointError as exc:
        raise ValueError('nonfinite headroom capacity') from exc
    if (not np.isfinite(result['I']).all() or not np.isfinite(result['F']).all()
            or np.any(result['I'] < result['floors'])
            or np.any(result['F'] < result['I'])):
        raise ValueError('invalid empirical reports')
    for values in result.values():
        values.flags.writeable = False
    return result
