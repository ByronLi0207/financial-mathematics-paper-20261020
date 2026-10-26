"""Pure E2 reducer over caller-supplied saved scalar method receipts.

No I/O, acquisition, calibration, forecast, scoring, or pooled test occurs here.
Literal contract codes and every planned method slot remain in the inventory.
"""
from collections import defaultdict
import math
from numbers import Integral, Real
from statistics import median


def _number(value):
    if not isinstance(value, Real) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, ValueError):
        return False


def _integer(value):
    return isinstance(value, Integral) and not isinstance(value, bool)


def _parameter(value):
    if isinstance(value, str) and value == 'inf':
        return 'inf'
    return float(value) if _number(value) else None


def _in_menu(value, menu):
    normalized = _parameter(value)
    return normalized is not None and normalized in menu


def _relative(loss, reference):
    if not (_number(loss) and _number(reference) and loss >= 0 and reference > 0):
        return None
    # Frozen arithmetic: do not rearrange, epsilon-clip, or round thresholds.
    value = 100. * (float(loss)/float(reference)-1.)
    return float(value) if math.isfinite(value) else None


def _quantile(values, probability):
    values = sorted(float(v) for v in values)
    position = (len(values)-1)*probability
    lo = int(math.floor(position))
    return float(values[lo] + (values[min(lo+1, len(values)-1)]-values[lo])*(position-lo))


def _method_cell(entries, code, window, method, design):
    count = int(design['split_formulas']['evaluation_n'])
    reasons = []
    row = entries[0] if len(entries) == 1 else {}
    if not entries:
        reasons.append('MISSING_METHOD_RECORD')
    elif len(entries) > 1:
        reasons.append('DUPLICATE_METHOD_RECORD')
    else:
        if row.get('status') != 'COMPLETE':
            reasons.append('RECORD_NOT_COMPLETE')
        if not _integer(row.get('n')) or row['n'] != count:
            reasons.append('FULL_EVALUATION_COUNT_MISMATCH')
        if not _number(row.get('mean_loss')) or row['mean_loss'] < 0:
            reasons.append('INVALID_MEAN_LOSS')
        hits = row.get('strict_breach_count')
        if not _integer(hits) or not 0 <= hits <= count:
            reasons.append('INVALID_STRICT_BREACH_COUNT')
        if method in ('QR4', 'QR33') and not _in_menu(row.get('selected_penalty'), design['menus'][method]):
            reasons.append('INVALID_SELECTED_PENALTY')
        if method in ('ACI_F', 'ACI_QR33') and not _in_menu(row.get('selected_gamma'), design['ancillary']['gammas']):
            reasons.append('INVALID_SELECTED_GAMMA')
    complete = not reasons
    saved_reason = row.get('reason')
    if not complete and saved_reason is not None:
        reasons.append(str(saved_reason))
    return dict(code=code, window=int(window), method=method,
                status='COMPLETE' if complete else 'FAILED', record_count=len(entries),
                reported_status=None if not row else str(row.get('status')),
                reported_n=int(row['n']) if _integer(row.get('n')) else None,
                n=count if complete else None,
                mean_loss=float(row['mean_loss']) if complete else None,
                strict_breach_count=int(row['strict_breach_count']) if complete else None,
                strict_breach_rate=float(row['strict_breach_count'])/count if complete else None,
                selected_penalty=_parameter(row.get('selected_penalty')),
                selected_gamma=_parameter(row.get('selected_gamma')),
                reason='; '.join(reasons) if reasons else None,
                relative_loss_pct=None, relative_reason=None)


def _across(cells, codes, windows, methods):
    index = {(c['code'], c['window'], c['method']): c for c in cells}
    result = []
    for window in windows:
        for method in methods:
            rows = [index[code, window, method] for code in codes]
            available = [r for r in rows if r['relative_loss_pct'] is not None]
            full = bool(codes) and len(available) == len(codes)
            values = [r['relative_loss_pct'] for r in available]
            result.append(dict(window=int(window), method=method,
                status='UNAVAILABLE' if not codes else 'COMPLETE' if full else 'UNASSESSABLE',
                required_contracts=len(codes), complete_method_contracts=sum(r['status'] == 'COMPLETE' for r in rows),
                complete_relative_pairs=len(available),
                missing_contracts=[r['code'] for r in rows if r['relative_loss_pct'] is None],
                missing_reasons={r['code']: r['relative_reason'] for r in rows if r['relative_loss_pct'] is None},
                median_pct=float(median(values)) if full else None,
                q25_pct=_quantile(values, .25) if full else None,
                q75_pct=_quantile(values, .75) if full else None,
                estimand='equal-weight median across ALL selected contracts of within-contract100*(method/F-1); descriptive only'))
    return result


def _status(available, supported, codes):
    return 'UNAVAILABLE' if not codes else 'UNASSESSABLE' if not available else 'SUPPORTED' if supported else 'NOT_SUPPORTED'


def _predictions(cells, across, codes, design):
    index = {(c['code'], c['window'], c['method']): c for c in cells}
    wins, complete, unknown = 0, 0, []
    for code in codes:
        for window in design['windows']:
            rows = [index[code, window, m] for m in ('F', 'I', 'QR33')]
            if any(r['status'] != 'COMPLETE' for r in rows):
                unknown.append(dict(code=code, window=int(window),
                                    missing_methods=[r['method'] for r in rows if r['status'] != 'COMPLETE']))
                continue
            complete += 1
            wins += min(rows[0]['mean_loss'], rows[1]['mean_loss']) < rows[2]['mean_loss']
    required = len(codes)*len(design['windows'])
    fraction = float(wins/required) if required and not unknown else None
    t1 = dict(status=_status(fraction is not None, fraction is not None and fraction >= design['T1']['minimum_inclusive_fraction'], codes),
              required_cells=required, complete_operand_cells=complete, simple_better_cells=int(wins),
              fraction=fraction, minimum_inclusive_fraction=float(design['T1']['minimum_inclusive_fraction']),
              unknown_cells=unknown)
    groups = {(r['window'], r['method']): r for r in across}
    def operand(window, method):
        row = groups[window, method]
        return row['median_pct'] if row['status'] == 'COMPLETE' else None
    q33 = {str(w): operand(w, 'QR33') for w in design['windows']}
    full_q33 = bool(codes) and all(v is not None for v in q33.values())
    t2 = dict(status=_status(full_q33, full_q33 and all(design['T2']['lower_inclusive_pct'] <= v <= design['T2']['upper_inclusive_pct'] for v in q33.values()), codes),
              median_pct_by_window=q33, lower_inclusive_pct=float(design['T2']['lower_inclusive_pct']),
              upper_inclusive_pct=float(design['T2']['upper_inclusive_pct']))
    short, long = operand(52, 'QR4'), operand(260, 'QR4')
    full_q4 = bool(codes) and short is not None and long is not None
    t3 = dict(status=_status(full_q4, full_q4 and long < short, codes),
              W52_median_pct=short, W260_median_pct=long,
              W260_minus_W52_pct_points=float(long-short) if full_q4 else None)
    return dict(T1=t1, T2=t2, T3=t3)


def summarize(records, contract_codes, design):
    """Retain allK selected contracts, bothW and six full-method receipt slots.

    A full method has exactly one COMPLETE record with all260 evaluation scores.
    Missing/duplicate/failed records emit FAILED slots with no partial metrics.
    Across-contract comparisons normalize each contract by its own positive F;
    no raw-contract-loss or dollar aggregation and no pooled test is produced.
    """
    codes = list(contract_codes)
    if any(not isinstance(c, str) or not c or c != c.strip() for c in codes):
        raise ValueError('contract codes must be literal nonblank stripped strings')
    codes = [str(c) for c in codes]
    if len(set(codes)) != len(codes) or len(codes) > design['top_contracts']:
        raise ValueError('selected contract universe must be unique and within frozen cap')
    windows = list(design['windows']); methods = list(design['methods'])
    if (set(windows) != {52, 260} or len(windows) != 2
            or set(methods) != {'F', 'I', 'QR4', 'QR33', 'ACI_F', 'ACI_QR33'} or len(methods) != 6
            or design['split_formulas']['evaluation_n'] != 260):
        raise ValueError('frozen E2 requires two declared windows, six methods and260 evaluations')
    windows = [int(w) for w in windows]; methods = [str(m) for m in methods]
    grouped = defaultdict(list)
    planned = {(code, window, method) for code in codes for window in windows for method in methods}
    for row in records:
        try:
            key = (row.get('code'), row.get('window'), row.get('method'))
            admitted = key in planned
        except (AttributeError, TypeError) as exc:
            raise ValueError('invalid method receipt identity') from exc
        if not admitted:
            raise ValueError('receipt outside selected literal code/window/method inventory')
        grouped[key].append(row)
    cells = [_method_cell(grouped[code, window, method], code, window, method, design)
             for code in codes for window in windows for method in methods]
    index = {(c['code'], c['window'], c['method']): c for c in cells}
    for cell in cells:
        reference = index[cell['code'], cell['window'], 'F']
        if cell['status'] != 'COMPLETE':
            cell['relative_reason'] = 'METHOD_INCOMPLETE'
        elif reference['status'] != 'COMPLETE':
            cell['relative_reason'] = 'REFERENCE_F_INCOMPLETE'
        else:
            cell['relative_loss_pct'] = _relative(cell['mean_loss'], reference['mean_loss'])
            if cell['relative_loss_pct'] is None:
                cell['relative_reason'] = 'NONPOSITIVE_F_OR_NONFINITE_RELATIVE_LOSS'
    contracts = []
    for code in codes:
        rows = [c for c in cells if c['code'] == code]
        complete = sum(c['status'] == 'COMPLETE' for c in rows)
        windows_out = {}
        for window in windows:
            selected = [c for c in rows if c['window'] == window]
            windows_out[str(window)] = dict(status='COMPLETE' if all(c['status'] == 'COMPLETE' for c in selected) else 'FAILED',
                                            methods={c['method']: dict(c) for c in selected})
        contracts.append(dict(code=code, status='COMPLETE' if complete == len(rows) else 'FAILED',
            complete_method_slots=complete, required_method_slots=len(windows)*len(methods), windows=windows_out,
            failed_method_slots=[dict(window=c['window'], method=c['method'], reason=c['reason']) for c in rows if c['status'] != 'COMPLETE']))
    across = _across(cells, codes, windows, methods)
    return dict(cells=cells, contracts=contracts, across_contracts=across,
                predictions=_predictions(cells, across, codes, design))
