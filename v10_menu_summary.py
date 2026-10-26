"""Pure E1 scalar reducer; importing/calling it opens no files or archives.

Every planned repetition and source is required. Failed grids retain inventory
and counts but never produce successful-subset medians. Quartiles use the
existing report convention: linear interpolation at (n-1)*p.
"""
from collections import defaultdict
import math
from numbers import Integral, Real
from statistics import median


def _number(value):
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)


def _integer(value):
    return isinstance(value, Integral) and not isinstance(value, bool)


def _relative(qr, reference):
    if not (_number(qr) and _number(reference) and qr >= 0 and reference > 0):
        return None
    # Preserve the frozen v9 arithmetic exactly. Do not rearrange this formula
    # or clip threshold operands to hide its IEEE rounding at +/-5 percent.
    value = 100. * (float(qr) / float(reference) - 1.)
    return float(value) if math.isfinite(value) else None


def _quantile(values, probability):
    ordered = sorted(float(x) for x in values)
    position = (len(ordered)-1)*probability
    lo = int(math.floor(position))
    fraction = position-lo
    return float(ordered[lo] + (ordered[min(lo+1, len(ordered)-1)]-ordered[lo])*fraction)


def _statistics(values):
    if values is None:
        return dict(median=None, q25=None, q75=None)
    return dict(median=float(median(values)), q25=_quantile(values, .25), q75=_quantile(values, .75))


def _new_record(row, count, menu):
    reasons = []
    if row.get('status') != 'COMPLETE':
        reasons.append('RECORD_NOT_COMPLETE')
    if not _integer(row.get('n')) or row['n'] != count:
        reasons.append('EVALUATION_COUNT_MISMATCH')
    value = _relative(row.get('qr_mean_loss'), row.get('f_mean_loss'))
    if value is None:
        reasons.append('INVALID_LOSS_OR_NONPOSITIVE_F')
    for name in ('qr_breaches', 'f_breaches'):
        if not _integer(row.get(name)) or not 0 <= row[name] <= count:
            reasons.append('INVALID_'+name.upper())
    if row.get('selected_penalty') not in menu:
        reasons.append('INVALID_SELECTED_PENALTY')
    return value, reasons


def _cell(rows, identity, repetitions, count, menu):
    by_rep = defaultdict(list)
    invalid_rep_ids = []
    for row in rows:
        rep = row.get('rep')
        if not _integer(rep):
            invalid_rep_ids.append(str(rep))
        else:
            by_rep[int(rep)].append(row)
    expected = range(repetitions)
    duplicates = sorted(rep for rep, entries in by_rep.items() if len(entries) > 1)
    unexpected = sorted(rep for rep in by_rep if rep not in expected)
    grid_complete = not (duplicates or unexpected or invalid_rep_ids)
    new_values, old_values, completed, old_completed = [], [], [], []
    qr_breaches, f_breaches, failures = [], [], []
    inf_count = 0
    for rep in expected:
        entries = by_rep.get(rep, [])
        if len(entries) != 1:
            failures.append(dict(rep=rep, reasons=['MISSING_REPETITION' if not entries else 'DUPLICATE_REPETITION'],
                                 qr_reason=None, f_reason=None))
            continue
        row = entries[0]
        value, reasons = _new_record(row, count, menu)
        if reasons:
            failures.append(dict(rep=rep, reasons=reasons,
                                 qr_reason=None if row.get('qr_reason') is None else str(row['qr_reason']),
                                 f_reason=None if row.get('f_reason') is None else str(row['f_reason'])))
        else:
            completed.append(rep)
            new_values.append(value)
            qr_breaches.append(float(row['qr_breaches'])/count)
            f_breaches.append(float(row['f_breaches'])/count)
            inf_count += row['selected_penalty'] == 'inf'
        old = _relative(row.get('original_qr_mean_loss'), row.get('original_f_mean_loss'))
        if row.get('original_status') == 'COMPLETE' and old is not None:
            old_completed.append(rep)
            old_values.append(old)
    full = grid_complete and len(completed) == repetitions
    old_full = grid_complete and len(old_completed) == repetitions
    new = _statistics(new_values if full else None)
    old = _statistics(old_values if old_full else None)
    return dict(identity, status='COMPLETE' if full else 'FAILED',
                required_repetitions=int(repetitions), completed_repetitions=len(completed),
                failed_repetitions=[rep for rep in expected if rep not in completed],
                duplicate_repetitions=duplicates, unexpected_repetitions=unexpected,
                invalid_repetition_ids=invalid_rep_ids, failures=failures,
                relative_median_pct=new['median'], q25=new['q25'], q75=new['q75'],
                q25_pct=new['q25'], q75_pct=new['q75'],
                selected_inf_count=int(inf_count),
                qr_breach_median=_quantile(qr_breaches, .5) if full else None,
                f_breach_median=_quantile(f_breaches, .5) if full else None,
                original_status='COMPLETE' if old_full else 'FAILED',
                original_completed_repetitions=len(old_completed),
                original_failed_repetitions=[rep for rep in expected if rep not in old_completed],
                original_relative_median_pct=old['median'],
                original_q25=old['q25'], original_q75=old['q75'])


def _across(cells, sources, arms, windows, methods):
    index = {(r['source_id'], r['arm'], r['window'], r['method']): r for r in cells}
    output = []
    for arm in arms:
        for window in windows:
            for method in methods:
                rows = [index[s, arm, window, method] for s in sources]
                complete = [r for r in rows if r['status'] == 'COMPLETE']
                old_complete = [r for r in rows if r['original_status'] == 'COMPLETE']
                full, old_full = len(complete) == len(sources), len(old_complete) == len(sources)
                new = _statistics([r['relative_median_pct'] for r in rows] if full else None)
                old = _statistics([r['original_relative_median_pct'] for r in rows] if old_full else None)
                output.append(dict(arm=arm, window=window, method=method,
                    status='COMPLETE' if full else 'UNASSESSABLE', required_sources=len(sources),
                    complete_sources=len(complete), missing_sources=[r['source_id'] for r in rows if r['status'] != 'COMPLETE'],
                    median_pct=new['median'], q25=new['q25'], q75=new['q75'],
                    q25_pct=new['q25'], q75_pct=new['q75'],
                    original_status='COMPLETE' if old_full else 'UNASSESSABLE',
                    original_complete_sources=len(old_complete),
                    original_missing_sources=[r['source_id'] for r in rows if r['original_status'] != 'COMPLETE'],
                    original_median_pct=old['median'], original_q25=old['q25'], original_q75=old['q75']))
    return output


def _status(assessable, supported):
    return 'UNASSESSABLE' if not assessable else 'SUPPORTED' if supported else 'NOT_SUPPORTED'


def _predictions(cells, across, sources, design):
    index = {(r['arm'], r['window'], r['method']): r for r in across}
    cell_index = {(r['source_id'], r['arm'], r['window'], r['method']): r for r in cells}
    def operand(arm, settings, old=False):
        row = index.get((arm, settings['window'], settings['method']))
        return None if row is None else row['original_median_pct' if old else 'median_pct']
    m1 = design['M1']
    constant = operand(m1['arm'], m1)
    one = dict(status=_status(constant is not None, constant is not None and
               m1['lower_inclusive_pct'] <= constant <= m1['upper_inclusive_pct']),
               constant_median_pct=constant, lower_inclusive_pct=float(m1['lower_inclusive_pct']),
               upper_inclusive_pct=float(m1['upper_inclusive_pct']))
    m2 = design['M2']
    a, b = operand('constant', m2), operand('switching', m2)
    difference = None if a is None or b is None else float(b-a)
    two = dict(status=_status(difference is not None, difference is not None and
               difference >= m2['minimum_inclusive_percentage_points']),
               constant_median_pct=a, switching_median_pct=b,
               switching_minus_constant_pct_points=difference,
               minimum_inclusive_percentage_points=float(m2['minimum_inclusive_percentage_points']))
    m3 = design['M3']
    operands = {arm: dict(expanded=operand(arm, m3), original=operand(arm, m3, True))
                for arm in ('constant', 'switching')}
    group_known = all(v is not None for pair in operands.values() for v in pair.values())
    group_improved = all(pair['expanded'] < pair['original'] for pair in operands.values()) if group_known else None
    joint, unknown = [], []
    for source in sources:
        paired = [cell_index.get((source, arm, m3['window'], m3['method'])) for arm in ('constant', 'switching')]
        if any(row is None or row['status'] != 'COMPLETE' or row['original_status'] != 'COMPLETE' for row in paired):
            unknown.append(source)
        elif all(row['relative_median_pct'] < row['original_relative_median_pct'] for row in paired):
            joint.append(source)
    assessable = group_known and not unknown
    three = dict(status=_status(assessable, group_improved and len(joint) >= m3['minimum_joint_improved_sources']),
                 group_both_arms_improved=group_improved,
                 group_operands=operands, joint_improved_sources=len(joint),
                 joint_improved_source_ids=joint, unknown_source_ids=unknown,
                 minimum_joint_improved_sources=int(m3['minimum_joint_improved_sources']))
    return dict(M1=one, M2=two, M3=three)


def summarize(records, repetitions, source_ids, design):
    """Summarize caller-supplied same-stage paired scalar records only.

    Repetition IDs are exactly0..R-1. Unknown source/arm/window/method identities
    are rejected; missing, duplicate and extra repetitions fail the owning cell.
    Old operands are taken only from the attached same-repetition original row.
    The return value contains Python-native JSON-safe values and no file I/O.
    """
    if not _integer(repetitions) or repetitions <= 0:
        raise ValueError('positive integer repetitions required')
    repetitions = int(repetitions)
    sources = [str(s) for s in source_ids]
    arms = [str(a) for a in design['arms']]
    methods = [str(m) for m in design['conditional_methods']]
    windows = list(design['windows'])
    if any(not _integer(w) or w <= 0 for w in windows):
        raise ValueError('positive integer windows required')
    windows = [int(w) for w in windows]
    if any(not values or len(set(values)) != len(values) for values in [sources, arms, windows, methods]):
        raise ValueError('nonempty unique planned inventory required')
    count = int(design['evaluation_last']-design['evaluation_first']+1)
    if count != 72:
        raise ValueError('E1 requires exactly72 evaluation origins')
    grouped = defaultdict(list)
    planned = {(s, arm, w, method) for s in sources for arm in arms for w in windows for method in methods}
    for row in records:
        try:
            identity = (row.get('source_id'), row.get('arm'), row.get('window'), row.get('method'))
            admitted = identity in planned
        except (AttributeError, TypeError) as exc:
            raise ValueError('invalid comparison record identity') from exc
        if not admitted:
            raise ValueError('comparison record outside planned source/arm/window/method inventory')
        grouped[identity].append(row)
    cells = []
    for source in sources:
        for arm in arms:
            for window in windows:
                for method in methods:
                    identity = (source, arm, window, method)
                    cells.append(_cell(grouped[identity],
                        dict(source_id=source, arm=arm, window=window, method=method),
                        repetitions, count, design['menus'][method]))
    across = _across(cells, sources, arms, windows, methods)
    return dict(cells=cells, across_sources=across,
                predictions=_predictions(cells, across, sources, design))
