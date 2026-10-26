"""Pure selection and fold arithmetic for the frozen R6 design.

Only caller-supplied loss vectors and integer origin metadata enter here.
There is no financial source I/O, target construction, fitting or evaluation.
The paired one-SE band is a frozen selection heuristic, not an inference test.
"""
from collections.abc import Mapping
import math
from numbers import Integral, Real


CANDIDATE_IDS = ('0.001', '0.01', '0.1', '1', '10', 'I')
FINITE_CANDIDATE_IDS = CANDIDATE_IDS[:-1]
COMMON_PURGE = 24


def _integer(value, name, minimum=1):
    if isinstance(value, bool) or not isinstance(value, Integral) or value < minimum:
        raise ValueError('INVALID_'+name)
    return int(value)


def _ids(candidate_ids):
    if isinstance(candidate_ids, (str, bytes)):
        raise ValueError('INVALID_CANDIDATE_IDS')
    ids = list(candidate_ids)
    if (not ids or any(type(c) is not str or c not in CANDIDATE_IDS for c in ids)
            or len(set(ids)) != len(ids)
            or ids != sorted(ids, key=CANDIDATE_IDS.index)):
        raise ValueError('INVALID_CANDIDATE_IDS')
    return ids


def _vector(values, *, nonnegative=False):
    if values is None or isinstance(values, (str, bytes, Mapping)):
        raise ValueError('INVALID_LOSS_VECTOR')
    try:
        result = list(values)
    except TypeError as error:
        raise ValueError('INVALID_LOSS_VECTOR') from error
    if not result or any(isinstance(v, bool) or not isinstance(v, Real) for v in result):
        raise ValueError('INVALID_LOSS_VECTOR')
    result = list(map(float, result))
    if any(not math.isfinite(v) or (nonnegative and v < 0) for v in result):
        raise ValueError('NONFINITE_OR_INVALID_LOSS')
    return result


def _fsum(values):
    try:
        result = math.fsum(values)
    except (OverflowError, ValueError) as error:
        raise ValueError('NONFINITE_ARITHMETIC') from error
    if not math.isfinite(result):
        raise ValueError('NONFINITE_ARITHMETIC')
    return result


def _origins(values, n):
    try:
        result = list(values)
    except TypeError as error:
        raise ValueError('INVALID_ORIGINS') from error
    if len(result) != n:
        raise ValueError('ORIGIN_COUNT_MISMATCH')
    result = [_integer(v, 'ORIGIN', 0) for v in result]
    if any(a >= b for a,b in zip(result, result[1:])):
        raise ValueError('ORIGINS_NOT_STRICTLY_INCREASING')
    return result


def _required(candidate_losses, candidate_ids):
    ids = _ids(candidate_ids)
    if not isinstance(candidate_losses, Mapping):
        raise ValueError('CANDIDATE_LOSS_MAPPING_REQUIRED')
    vectors, rows, n = {}, [], None
    for candidate in ids:
        row = dict(candidate_id=candidate, status='FAILED', n=None, mean_loss=None)
        try:
            if candidate not in candidate_losses:
                raise ValueError('MISSING_REQUIRED_CANDIDATE')
            if candidate_losses[candidate] is None:
                raise ValueError('INCOMPLETE_REQUIRED_CANDIDATE')
            vector = _vector(candidate_losses[candidate], nonnegative=True)
            if n is None:
                n = len(vector)
            if len(vector) != n:
                raise ValueError('ORIGIN_COUNT_MISMATCH')
            mean = _fsum(vector)/len(vector)
            vectors[candidate] = vector
            row.update(status='COMPLETE', n=len(vector), mean_loss=mean)
        except ValueError as error:
            row['reason'] = str(error)
        rows.append(row)
    return ids, vectors, rows, n


def _base(method, rows, n):
    return dict(status='FAILED', reason=None, selection_method=method,
                selected_id=None, best_id=None, n=n, bandwidth=None, candidates=rows)


def _best(rows):
    # Caller order is frozen weak-to-strong; the negative index resolves exact ties.
    return min(range(len(rows)), key=lambda j:(rows[j]['mean_loss'], -j))


def select_minimum(candidate_losses, candidate_ids):
    """Select R0/R1 (or the frozen original subset); required failures are fatal."""
    ids, _, rows, n = _required(candidate_losses, candidate_ids)
    result = _base('minimum_mean_loss', rows, n)
    if any(row['status'] != 'COMPLETE' for row in rows):
        result['reason'] = 'REQUIRED_CANDIDATE_FAILED'
        return result
    best = _best(rows)
    for row in rows:
        row['eligible'] = row['mean_loss'] == rows[best]['mean_loss']
    result.update(status='SELECTED', selected_id=ids[best], best_id=ids[best])
    return result


def lrv_standard_error(raw_lrv, n):
    """Retain the raw scalar and make the frozen numerical clipping visible."""
    n = _integer(n, 'SAMPLE_SIZE')
    if isinstance(raw_lrv, bool) or not isinstance(raw_lrv, Real) or not math.isfinite(raw_lrv):
        raise ValueError('NONFINITE_LRV')
    raw_lrv = float(raw_lrv)
    clipped = max(raw_lrv, 0.)
    return dict(status='NUMERICAL_LRV_CLIPPED_TO_ZERO' if raw_lrv < 0 else 'OK',
                raw_lrv=raw_lrv, lrv=clipped, standard_error=math.sqrt(clipped/n))


def origin_aware_nw(differences, origins, horizon):
    """Bartlett NW with actual source-record index lags and denominator n."""
    differences = _vector(differences)
    n = len(differences)
    ids = _origins(origins, n)
    horizon = _integer(horizon, 'HORIZON')
    bandwidth = max(horizon, math.floor(4*(n/100)**(2/9)))
    if n <= bandwidth:
        raise ValueError('INSUFFICIENT_ORIGINS_FOR_BANDWIDTH')
    mean = _fsum(differences)/n
    centered = [d-mean for d in differences]
    if any(not math.isfinite(v) for v in centered):
        raise ValueError('NONFINITE_ARITHMETIC')
    lookup = dict(zip(ids, centered))
    terms = [_fsum(v*v for v in centered)/n]
    pair_counts = [n]
    for lag in range(1, bandwidth+1):
        products = [u*lookup[t-lag] for t,u in zip(ids, centered) if t-lag in lookup]
        covariance = _fsum(products)/n
        terms.append(2*(1-lag/(bandwidth+1))*covariance)
        pair_counts.append(len(products))
    result = lrv_standard_error(_fsum(terms), n)
    result.update(n=n, mean=mean, bandwidth=bandwidth, lag_pair_counts=pair_counts)
    return result


def select_paired_one_se(candidate_losses, origins, horizon, candidate_ids):
    """R2/R3: strongest candidate within its paired difference's one-SE band."""
    ids, vectors, rows, n = _required(candidate_losses, candidate_ids)
    result = _base('paired_difference_one_se', rows, n)
    if any(row['status'] != 'COMPLETE' for row in rows):
        result['reason'] = 'REQUIRED_CANDIDATE_FAILED'
        return result
    try:
        origin_ids = _origins(origins, n)
        horizon = _integer(horizon, 'HORIZON')
        result['bandwidth'] = max(horizon, math.floor(4*(n/100)**(2/9)))
        if n <= result['bandwidth']:
            raise ValueError('INSUFFICIENT_ORIGINS_FOR_BANDWIDTH')
    except ValueError as error:
        result['reason'] = str(error)
        return result
    best = _best(rows)
    result['best_id'] = ids[best]
    for candidate, row in zip(ids, rows):
        try:
            difference = [a-b for a,b in zip(vectors[candidate], vectors[ids[best]])]
            diagnostic = origin_aware_nw(difference, origin_ids, horizon)
            row.update(paired_mean_gap=diagnostic['mean'], raw_lrv=diagnostic['raw_lrv'],
                lrv=diagnostic['lrv'], standard_error=diagnostic['standard_error'],
                bandwidth=diagnostic['bandwidth'], nw_status=diagnostic['status'],
                lag_pair_counts=diagnostic['lag_pair_counts'],
                eligible=diagnostic['mean'] <= diagnostic['standard_error'])
        except ValueError as error:
            row.update(status='FAILED', reason=str(error), eligible=False)
    if any(row['status'] != 'COMPLETE' for row in rows):
        result['reason'] = 'REQUIRED_CANDIDATE_NUMERICAL_FAILURE'
        return result
    eligible = [j for j,row in enumerate(rows) if row['eligible']]
    # The empirical best has the exactly zero self-difference and must qualify.
    if not eligible:
        result['reason'] = 'NO_ELIGIBLE_CANDIDATE'
        return result
    result.update(status='SELECTED', selected_id=ids[eligible[-1]])
    return result


def rolling_folds(validation_first, validation_last, window, feature_prefix,
                  refit_step, purge=COMMON_PURGE):
    """Frozen common-H*=24 full prefix folds, then complete outer validation.

    Returns chronological inclusive bounds. The caller invokes the unchanged
    forecast separately for each tuple, resetting its refit anchor each time.
    A one-tuple result is the declared NO_EXTRA_FOLDS construction.
    """
    first = _integer(validation_first, 'VALIDATION_FIRST', 0)
    last = _integer(validation_last, 'VALIDATION_LAST', 0)
    window = _integer(window, 'WINDOW')
    feature_prefix = _integer(feature_prefix, 'FEATURE_PREFIX', 0)
    step = _integer(refit_step, 'REFIT_STEP')
    purge = _integer(purge, 'PURGE')
    if purge != COMMON_PURGE or last < first:
        raise ValueError('FROZEN_FOLD_CONFIGURATION')
    earliest = feature_prefix+window+COMMON_PURGE-1
    if first < earliest:
        raise ValueError('INADEQUATE_COMPLETED_FEATURE_HISTORY')
    folds = []
    end = first-COMMON_PURGE-1
    while end-step+1 >= earliest:
        folds.append((end-step+1, end))
        end -= step+COMMON_PURGE
    folds.reverse()
    folds.append((first,last))
    return folds
