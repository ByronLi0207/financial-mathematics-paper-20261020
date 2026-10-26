"""WP4 deterministic daily primitives; no source I/O or model fitting.

The caller supplies a pinned source snapshot. Only completed source-naive
day-end proxies are returned; raw vectors and mappings are private artifacts.
"""
from collections import Counter
from dataclasses import dataclass
import hashlib
import math

import numpy as np


@dataclass(frozen=True)
class DailySeries:
    position: np.ndarray
    times: np.ndarray
    selected_indices: np.ndarray
    selected_raw_times: np.ndarray
    metadata: dict


def _readonly(a):
    out=np.array(a,copy=True)
    out.flags.writeable=False
    return out


def _integer(value,minimum=0):
    if isinstance(value,(bool,np.bool_)) or not isinstance(value,(int,np.integer)) or value<minimum:
        raise ValueError('finite nonnegative integer required')
    return int(value)


def _stamp(value):
    return str(np.datetime_as_string(value,unit='us'))


def resample_closed_days(position,times):
    """Select last rows, with an issue clock after their source day ends.

    No source sort, row dropping, timezone conversion or missing-day filling is
    performed. The first/last partial observed days follow the same proxy rule.
    """
    raw=np.asarray(position);t=np.asarray(times)
    if (raw.ndim!=1 or not raw.size or raw.dtype.kind not in 'iuf'
            or t.ndim!=1 or t.shape!=raw.shape or t.dtype.kind!='M'
            or np.isnat(t).any()):
        raise ValueError('invalid source vectors')
    x=np.array(raw,dtype=np.float64,copy=True)
    t=np.array(t,dtype='datetime64[us]',copy=True)
    if not np.isfinite(x).all() or np.any(t[1:]<=t[:-1]):
        raise ValueError('nonfinite position or nonincreasing source time')
    days=t.astype('datetime64[D]')
    indices=np.concatenate((np.flatnonzero(days[1:]!=days[:-1]),
                            np.array([len(days)-1],dtype=np.int64))).astype(np.int64)
    selected_times=t[indices]
    issue=days[indices].astype('datetime64[us]')+np.timedelta64(1,'D')-np.timedelta64(1,'us')
    selected=x[indices]
    # Canonical byte order is a public fingerprint contract, independent of
    # caller array byte order or memory layout.
    vectors=(np.ascontiguousarray(indices,dtype='<i8').tobytes(),
        np.ascontiguousarray(selected_times.astype('datetime64[us]').view('i8'),dtype='<i8').tobytes(),
        np.ascontiguousarray(issue.astype('datetime64[us]').view('i8'),dtype='<i8').tobytes(),
        np.ascontiguousarray(selected,dtype='<f8').tobytes())
    names=('selected_indices_sha256','selected_raw_times_sha256',
           'issue_times_sha256','position_sha256')
    fingerprints={name:hashlib.sha256(v).hexdigest() for name,v in zip(names,vectors)}
    fingerprints['combined_sha256']=hashlib.sha256(b'v8-daily-v1\x00'+b''.join(vectors)).hexdigest()
    gap_seconds=(np.diff(issue).astype('timedelta64[us]').astype(np.int64)//1_000_000)
    histogram=Counter(int(v) for v in gap_seconds)
    metadata=dict(schema='wp4-daily-resampling-v1',n_original=len(x),n_daily=len(selected),
        n_discarded_original=len(x)-len(selected),
        source_first_timestamp=_stamp(t[0]),source_last_timestamp=_stamp(t[-1]),
        first_issue_time=_stamp(issue[0]),last_issue_time=_stamp(issue[-1]),
        daily_gap_seconds_histogram={str(k):histogram[k] for k in sorted(histogram)},
        fingerprints=fingerprints)
    return DailySeries(_readonly(selected),_readonly(issue),_readonly(indices),
                       _readonly(selected_times),metadata)


def daily_issue_geometry(n,h,w,design):
    """Declared indices/counts; NA never moves a cutoff or shortens history.

    validation_count is the fixed declared grid size, not a claim that any
    validation report has been computed. Only READY permits scoring that grid.
    """
    n,h,w=map(_integer,(n,h,w))
    horizons=design['clock_and_target']['horizons']
    if h not in horizons or w not in design['windows']:
        raise ValueError('cell outside frozen design')
    sample=design['sample'];first=int(sample['validation_first']);last=int(sample['validation_last'])
    evaluation_first=int(sample['evaluation_first'])
    evaluation_last=n-1-max(horizons)
    earliest=first-h-w+1;valid=int(design['features']['valid_from'])
    result=dict(status='READY',reason=None,validation_first=first,validation_last=last,
        validation_count=last-first+1,evaluation_first=evaluation_first,
        evaluation_last=evaluation_last,evaluation_count=max(0,evaluation_last-evaluation_first+1),
        earliest_training_origin=earliest,feature_valid_from=valid)
    if last+max(horizons)>=n:
        result.update(status='NA_SAMPLE_SIZE',reason='VALIDATION_NOT_FULLY_OBSERVED')
    elif evaluation_last<evaluation_first:
        result.update(status='NA_SAMPLE_SIZE',reason='EMPTY_EVALUATION_GRID')
    elif earliest<valid:
        result.update(status='NA_SAMPLE_SIZE',reason='INSUFFICIENT_FEATURE_HISTORY')
    return result


def _score(row):
    e=row.get('evaluation')
    if not isinstance(e,dict):
        raise ValueError('complete method missing evaluation')
    loss=e.get('mean_loss');n=e.get('n');hits=e.get('strict_breach_count');rate=e.get('strict_breach_rate')
    if (type(loss) not in (int,float) or not math.isfinite(loss) or loss<0
            or type(n) is not int or n<=0 or type(hits) is not int or not 0<=hits<=n
            or type(rate) not in (int,float) or not math.isfinite(rate) or rate!=hits/n):
        raise ValueError('invalid complete method score')
    return loss,n


def classify_against_f(rows,method,design):
    """Apply the frozen four-comparison descriptive rule separately by QR.

    There is no significance test or precision threshold. Absolute mean losses
    define wins even when a percentage ratio against zero F loss is unavailable.
    """
    if method not in ('QR33','QR4'):
        raise ValueError('unsupported regression')
    grid=[(w,h) for w in design['windows'] for h in design['clock_and_target']['horizons']]
    methods=set(design['methods']);expected={(w,h,m) for w,h in grid for m in methods}
    index={}
    statuses={'COMPLETE','FAILED','NOT_ATTEMPTED','NA_SAMPLE_SIZE','INELIGIBLE'}
    for row in rows:
        try:key=tuple(row[k] for k in ('window','horizon','method'))
        except (KeyError,TypeError) as exc:raise ValueError('invalid method identity') from exc
        if key not in expected or key in index:
            raise ValueError('unexpected or duplicate method identity')
        if row.get('status') not in statuses:
            raise ValueError('invalid method status')
        if row['status']=='COMPLETE':_score(row)
        index[key]=row
    counts=Counter();comparisons=[];counterexamples=[]
    for w,h in grid:
        model=index.get((w,h,method));reference=index.get((w,h,'F'))
        case=dict(window=w,horizon=h,method=method,outcome='UNAVAILABLE',
            model_status=None if model is None else model['status'],
            reference_status=None if reference is None else reference['status'],
            mean_model_loss=None,mean_F_loss=None,reason=None)
        if model is None or reference is None:
            case['reason']='MISSING_METHOD_ROW' if model is None else 'MISSING_REFERENCE_ROW'
        elif model['status']!='COMPLETE' or reference['status']!='COMPLETE':
            case['reason']='METHOD_OR_REFERENCE_UNAVAILABLE'
        else:
            a,na=_score(model);b,nb=_score(reference)
            if na!=nb:raise ValueError('paired evaluation counts differ')
            outcome='CONDITIONAL_WIN' if a<b else ('HISTORICAL_WIN' if b<a else 'TIE')
            case.update(outcome=outcome,mean_model_loss=a,mean_F_loss=b)
        counts[case['outcome']]+=1;comparisons.append(case)
        if case['outcome']=='CONDITIONAL_WIN':counterexamples.append(dict(case))
    missing=counts['UNAVAILABLE']
    if missing:status='INCONCLUSIVE'
    elif counts['HISTORICAL_WIN']>=3:status='TREASURY_LIKE'
    elif counts['CONDITIONAL_WIN']>=3:status='CONDITIONAL_GAINS_PERSIST'
    else:status='MIXED'
    return dict(method=method,status=status,planned_comparisons=len(grid),
        complete_comparisons=len(grid)-missing,historical_wins=counts['HISTORICAL_WIN'],
        conditional_wins=counts['CONDITIONAL_WIN'],ties=counts['TIE'],
        missing_comparisons=missing,comparisons=comparisons,
        literal_hourly_counterexamples=counterexamples,descriptive_only=True)
