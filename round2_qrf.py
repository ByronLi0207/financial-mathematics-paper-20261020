"""Fixed post-result QRF baseline with all-original-row leaf distributions.

This implements the weighted conditional empirical CDF of Meinshausen (2006),
equations 4--6. Bootstrap samples construct tree partitions; the CDF then uses
every original mature training row in a matching leaf, without multiplicities.
No time-series consistency or conditional coverage guarantee is asserted.
"""
import hashlib
import json
import math

import numpy as np

from conditional_features import (
    build_features, completed_training_indices, fit_feature_transform,
    refit_origin, response_scale, transform_features,
)
from conditional_study import StudyConfig
from study_core import _readonly, _vector, build_label_cache


FOREST_PARAMETERS = {
    'n_estimators': 100,
    'criterion': 'squared_error',
    'bootstrap': True,
    'max_samples': None,
    'max_features': 11,
    'min_samples_leaf': 5,
    'min_samples_split': 10,
    'max_depth': 10,
    'n_jobs': 1,
    'random_state': 20261023,
    'oob_score': False,
    'warm_start': False,
}


def weights_from_leaves(training_leaves, query_leaves):
    """Average uniform mass on each tree's matching original training rows."""
    leaves = np.asarray(training_leaves)
    query = np.asarray(query_leaves)
    if (leaves.ndim != 2 or not all(leaves.shape)
            or leaves.dtype.kind not in 'iu' or np.any(leaves < 0)
            or query.shape != (leaves.shape[1],)
            or query.dtype.kind not in 'iu' or np.any(query < 0)):
        raise ValueError('invalid original-row leaf membership arrays')
    weights = np.zeros(leaves.shape[0], dtype=np.float64)
    for tree in range(leaves.shape[1]):
        member = leaves[:, tree] == query[tree]
        size = int(np.count_nonzero(member))
        if not size:
            raise ValueError('query leaf has no original training member')
        weights[member] += 1. / (leaves.shape[1] * size)
    total = math.fsum(map(float, weights))
    if (not np.isfinite(weights).all() or np.any(weights < 0)
            or not math.isclose(total, 1., rel_tol=0, abs_tol=1e-12)):
        raise ValueError('invalid leaf distribution mass')
    return _readonly(weights)


def weighted_quantile(values, weights, tau=.95):
    """Noninterpolated left inverse of a finite weighted empirical CDF."""
    y = np.asarray(values, dtype=np.float64)
    w = np.asarray(weights, dtype=np.float64)
    if (y.ndim != 1 or not y.size or w.shape != y.shape
            or not np.isfinite(y).all() or not np.isfinite(w).all()
            or np.any(w < 0) or isinstance(tau, (bool, np.bool_))
            or np.asarray(tau).ndim):
        raise ValueError('invalid weighted quantile input')
    try:
        tau = float(tau)
        total = math.fsum(map(float, w))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('invalid weighted quantile mass or level') from exc
    if not math.isfinite(tau) or not 0 < tau <= 1 or not math.isfinite(total) or total <= 0:
        raise ValueError('invalid weighted quantile mass or level')
    positive = w > 0
    y, w = y[positive], w[positive]
    order = np.argsort(y, kind='stable')
    cdf = np.cumsum(w[order] / total)
    cdf[-1] = 1.  # Exact total mass; avoid an unavailable q_1 from roundoff.
    index = int(np.searchsorted(cdf, tau, side='left'))
    return float(y[order[index]])


def _fingerprint(*arrays):
    digest = hashlib.sha256()
    for value in arrays:
        a = np.asarray(value)
        if a.dtype.kind in 'iu':
            a = a.astype('<i8', copy=False)
        else:
            a = a.astype('<f8', copy=False)
        digest.update(json.dumps(list(a.shape)).encode('ascii'))
        digest.update(a.dtype.str.encode('ascii'))
        digest.update(a.tobytes(order='C'))
    return digest.hexdigest()


def qrf_forecast(position, times, origins, config, checkpoint=None):
    """Issue the frozen QRF procedure, preserving an explicit failed prefix.

    All work is source-free. Each refit sees exactly W labels completed by r;
    features and labels are built on the observed prefix only. Any failure or
    cancellation propagates without a replacement report or a shortened score.
    """
    capacities = []
    refit_indices = []
    receipts = []
    ids = np.empty(0, dtype=np.int64)
    context = {'stage': 'qrf_validate', 'fallback': False,
               'issued_origin_count': 0, 'query_issue': None, 'refit_index': None}
    try:
        if not isinstance(config, StudyConfig):
            raise ValueError('QRF requires the frozen StudyConfig interface')
        raw_x = np.asarray(position, dtype=np.float64)
        raw_times = np.asarray(times)
        raw_ids = np.asarray(origins)
        if (raw_x.ndim != 1 or raw_times.shape != raw_x.shape
                or raw_times.dtype.kind != 'M' or raw_ids.ndim != 1
                or not raw_ids.size or raw_ids.dtype.kind not in 'iu'
                or np.any(raw_ids > np.iinfo(np.int64).max)
                or np.any(raw_ids < 0)):
            raise ValueError('invalid QRF source or issue indices')
        ids = raw_ids.astype(np.int64, copy=True)
        if np.any(np.diff(ids) != 1) or ids[-1] >= len(raw_x):
            raise ValueError('noncontiguous or out-of-range QRF issue origins')
        # Future rows cannot affect global feature/label validity or a digest.
        x = _vector(raw_x[:int(ids[-1]) + 1], 'observed QRF positions')
        source_times = raw_times[:len(x)]
        features = build_features(x, source_times, short_scale=config.short_scale,
            long_scale=config.long_scale, nominal_gap_seconds=config.nominal_gap_seconds)
        cache = build_label_cache(x, config.horizon)
        from sklearn.ensemble import RandomForestRegressor

        previous_refit = None
        for j, raw_t in enumerate(ids):
            t = int(raw_t)
            r = refit_origin(t, int(ids[0]), config.refit_step)
            context = dict(stage='qrf_refit' if r != previous_refit else 'qrf_issue',
                query_issue=t, refit_index=r, issued_origin_count=j, fallback=False)
            if r != previous_refit:
                if checkpoint is not None:
                    checkpoint(stage='qrf_refit', refit_index=r, completed_origins=j)
                pool = completed_training_indices(r, config.horizon, config.window,
                    minimum_feature_index=features.valid_from)
                if np.any(cache.label_end[pool] > r):
                    raise ValueError('QRF attempted to fit unfinished labels')
                transform = fit_feature_transform(features.values[pool])
                train = transform_features(features.values[pool], transform, nearest=False)
                scale = response_scale(cache.headroom[pool], x[pool])
                train_y = cache.headroom[pool] / scale
                context.update(
                    training_first_origin=int(pool[0]),
                    training_last_origin=int(pool[-1]), training_count=len(pool),
                    latest_label_end=int(cache.label_end[pool[-1]]), response_scale=scale,
                    feature_transform_sha256=_fingerprint(transform.mean, transform.scale),
                    training_features_sha256=_fingerprint(train),
                    training_response_sha256=_fingerprint(train_y))
                forest = RandomForestRegressor(**FOREST_PARAMETERS)
                forest.fit(train, train_y)
                train_leaves = forest.apply(train)
                tree_arrays = []
                for estimator in forest.estimators_:
                    tree_arrays.extend((estimator.tree_.children_left,
                        estimator.tree_.children_right, estimator.tree_.feature,
                        estimator.tree_.threshold))
                receipt = dict(
                    refit_index=r, training_first_origin=int(pool[0]),
                    training_last_origin=int(pool[-1]), training_count=len(pool),
                    latest_label_end=int(cache.label_end[pool[-1]]), response_scale=scale,
                    feature_transform_sha256=_fingerprint(transform.mean, transform.scale),
                    training_features_sha256=_fingerprint(train),
                    training_response_sha256=_fingerprint(train_y),
                    forest_leaf_partition_sha256=_fingerprint(train_leaves),
                    forest_structure_sha256=_fingerprint(*tree_arrays),
                    forest_parameters=dict(FOREST_PARAMETERS),
                    distribution='all_original_rows_in_matching_leaf',
                    quantile='weighted_CDF_left_inverse_tau_19_over_20',
                    bootstrap_multiplicity_in_cdf=False, fallback=False,
                )
                receipts.append(receipt)
                previous_refit = r
            query = transform_features(features.values[t:t+1], transform, nearest=False)
            query_leaves = forest.apply(query)[0]
            weights = weights_from_leaves(train_leaves, query_leaves)
            headroom = scale * weighted_quantile(train_y, weights, .95)
            capacity = abs(float(x[t])) + max(0., headroom)
            if not math.isfinite(capacity):
                raise ValueError('nonfinite QRF capacity')
            capacities.append(capacity)
            refit_indices.append(r)
            if checkpoint is not None:
                checkpoint(stage='qrf_issue', refit_index=r, completed_origins=j+1)
        return dict(capacity=_readonly(capacities), refits=receipts,
                    refit_indices=_readonly(refit_indices, np.int64))
    except Exception as exc:
        # No retry, fallback, changed parameter, row omission or complete score.
        exc.failure_context = dict(context)
        exc.partial_forecast = dict(
            capacity=_readonly(capacities), refits=list(receipts),
            origins=_readonly(ids[:len(capacities)], np.int64),
            refit_indices=_readonly(refit_indices, np.int64))
        raise
