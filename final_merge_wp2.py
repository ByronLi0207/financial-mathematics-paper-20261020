"""Scalar audit and predeclared decisions for the final CFTC extension.

No financial input, model fitting, source acquisition or file writes on import.
The scalar scoring/HAC functions are independent of the inherited NumPy path.
"""
import math


def split_geometry(n, h, w):
    if any(type(x) is not int or x < 1 for x in (n, h, w)):
        raise ValueError('positive integer geometry required')
    ef = n-h-260
    vl = ef-h-1
    vf = vl-51
    first = vf-h-w+1
    if first < 26:
        raise ValueError('INSUFFICIENT_FEATURE_HISTORY')
    return dict(validation_first=vf, validation_last=vl, evaluation_first=ef,
        evaluation_last=n-h-1, first_training_origin=first,
        latest_validation_label_end=vl+h, last_evaluation_label_end=n-1)


def screen(outcomes, threshold):
    values = list(outcomes)
    if (not values or type(threshold) not in (int, float) or not 0 < threshold <= 1
            or any(x is not None and type(x) is not bool for x in values)):
        raise ValueError('boolean-or-missing fixed cells and interior threshold required')
    n = len(values)
    successes = sum(x is True for x in values)
    unknown = sum(x is None for x in values)
    low, high = successes/n, (successes+unknown)/n
    status = 'SUPPORT' if low >= threshold else 'NOT_SUPPORT' if high < threshold else 'NOT_TESTABLE'
    return dict(status=status, planned=n, complete=n-unknown, successes=successes,
        unknown=unknown, complete_fraction=successes/(n-unknown) if n > unknown else None,
        lower=low, upper=high, threshold=threshold)


def primary_status(p1_qr33, p1_qr4, p2_qr4):
    values = (p1_qr33, p1_qr4, p2_qr4)
    if any(x not in ('SUPPORT', 'NOT_SUPPORT', 'NOT_TESTABLE') for x in values):
        raise ValueError('unknown primary decision status')
    p1 = ('NOT_SUPPORT' if 'NOT_SUPPORT' in values[:2] else
          'SUPPORT' if values[:2] == ('SUPPORT', 'SUPPORT') else 'NOT_TESTABLE')
    if 'NOT_TESTABLE' in (p1, p2_qr4):
        return 'NOT_TESTABLE'
    return ('SUPPORT' if p1 == p2_qr4 == 'SUPPORT' else
            'PARTLY' if 'SUPPORT' in (p1, p2_qr4) else 'NOT_SUPPORT')


def strict_decrease(values):
    values = list(values)
    if len(values) != 3:
        raise ValueError('three declared windows required')
    if any(x is None for x in values):
        return None
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in values):
        raise ValueError('finite relative losses required')
    return values[0] > values[1] > values[2]


def scalar_hac(differences, horizon):
    d = [float(x) for x in differences]
    n = len(d)
    if type(horizon) is not int or horizon < 1 or n <= horizon or not all(map(math.isfinite, d)):
        raise ValueError('complete finite paired differences required')
    lag = min(n-1, max(horizon, int(4*(n/100)**(2/9))))
    mean = math.fsum(d)/n
    out = dict(n=n, horizon=horizon, bandwidth=lag, mean_difference=mean,
        lrv=None, dm_t=None, dm_p=None, status='OK')
    if all(x == d[0] for x in d):
        out.update(lrv=0., status='IDENTICAL_LOSSES' if d[0] == 0 else 'ZERO_LONG_RUN_VARIANCE')
        return out
    # Match the archived centering convention's arithmetic mean; independently
    # sum covariance products rather than calling the NumPy matrix routine.
    center = sum(d)/n
    u = [x-center for x in d]
    lrv = math.fsum(x*x for x in u)/n
    lrv += math.fsum(2*(1-k/(lag+1))*math.fsum(u[t]*u[t-k] for t in range(k, n))/n
                     for k in range(1, lag+1))
    out['lrv'] = lrv
    if not math.isfinite(lrv) or lrv <= 0:
        out['status'] = 'NONPOSITIVE_LONG_RUN_VARIANCE'
        return out
    t = mean/math.sqrt(lrv/n)
    out.update(dm_t=t, dm_p=math.erfc(abs(t)/math.sqrt(2)))
    return out


def scalar_trace(position, origins, capacities, horizon):
    x, ids, caps = list(position), list(origins), list(capacities)
    if len(ids) != len(caps) or not ids or any(type(i) is not int or i < 0 or i+horizon >= len(x) for i in ids):
        raise ValueError('complete trace geometry required')
    if any(not math.isfinite(v) for v in x+caps):
        raise ValueError('finite trace required')
    floor = [abs(float(x[i])) for i in ids]
    if any(c < f for c, f in zip(caps, floor)):
        raise ValueError('CAPACITY_BELOW_CURRENT_FLOOR')
    peak = [max(abs(float(v)) for v in x[i:i+horizon+1]) for i in ids]
    errors = [p-c for p, c in zip(peak, caps)]
    loss = [(19/20)*e if e >= 0 else (1/20)*(-e) for e in errors]
    return dict(peak=peak, floor=floor, pinball=loss,
        strict_breach=[p > c for p, c in zip(peak, caps)],
        overrun=[max(0., e) for e in errors], unused=[max(0., -e) for e in errors])


def check_maturity(diagnostics, window, horizon, conditional):
    count = 0
    for row in diagnostics:
        r = row['refit_index']
        first, last = r-horizon-window+1, r-horizon
        if (row['training_first_origin'] != first or row['training_last_origin'] != last
                or row['training_count'] != window or row['latest_label_end'] != r
                or first < (26 if conditional else 0)):
            raise ValueError('MATURITY_OR_EXACT_POOL_MISMATCH')
        count += 1
    if not count:
        raise ValueError('MATURITY_DIAGNOSTICS_ABSENT')
    return count
