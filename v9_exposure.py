"""Descriptive synthetic regime exposure under the frozen WP3 issue geometry."""
from collections import Counter
import numpy as np


def _counts(values):
    return {str(k): int(v) for k,v in sorted(Counter(map(int,values)).items())}


def describe_geometry(arm,design):
    """Count fixed path exposures; no outcome, fitting or selection is used.

    A boundary at b changes the law generating level b. A label issued at t
    crosses it precisely when t < b <= t+H. Issue-boundary counts include
    boundaries exactly at the first issue. Training-label unions count each
    index once; future-label regime counts include overlap multiplicity.
    """
    ids=np.asarray(arm['regime_ids'],dtype=np.int64)
    forward=np.asarray(arm['transition_indices'],dtype=np.int64)
    wraps=np.asarray(arm['wrap_indices'],dtype=np.int64)
    h=int(design['horizon'])
    def n_between(boundaries,first,last):
        return int(np.count_nonzero((boundaries>=first)&(boundaries<=last)))
    def cross(boundaries,origins):
        return sum(bool(np.any((boundaries>t)&(boundaries<=t+h))) for t in origins)
    def origin_exposure(origins):
        return dict(first_origin=int(origins[0]),last_origin=int(origins[-1]),
            issue_regime_counts=_counts(ids[origins]),
            future_label_regime_counts=_counts(np.concatenate([ids[t+1:t+h+1] for t in origins])),
            labels_crossing_forward_boundary=cross(forward,origins),
            labels_crossing_wrap_boundary=cross(wraps,origins),
            forward_boundaries_in_label_union=n_between(forward,int(origins[0])+1,int(origins[-1])+h),
            wrap_boundaries_in_label_union=n_between(wraps,int(origins[0])+1,int(origins[-1])+h))
    result=dict(retained_regime_counts=_counts(ids),
                boundary_definition='law generating retained level b changes at b; label t crosses iff t < b <= t+H')
    for segment in ('validation','evaluation'):
        first,last=int(design[segment+'_first']),int(design[segment+'_last'])
        origins=np.arange(first,last+1,dtype=np.int64)
        row=origin_exposure(origins)
        row.update(issue_forward_boundaries=n_between(forward,first,last),
                   issue_wrap_boundaries=n_between(wraps,first,last),training_refits=[])
        for w in design['windows']:
            for r in range(first,last+1,int(design['refit_step'])):
                pool=np.arange(r-h-int(w)+1,r-h+1,dtype=np.int64)
                training=origin_exposure(pool)
                training.update(refit_index=r,window=int(w),latest_label_end=r,
                    unique_level_span_regime_counts=_counts(ids[pool[0]:r+1]))
                row['training_refits'].append(training)
        result[segment]=row
    return result
