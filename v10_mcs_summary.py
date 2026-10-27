"""Pure E3 membership/inventory reducer; no loss data or MCS library is used."""
from collections import Counter, defaultdict
import math
from numbers import Integral, Real


IDENTITY = ('period', 'normalized_source', 'horizon', 'window')
CLASSES = {'matched_historical', 'other_historical', 'conditional', 'other_benchmark'}
SUCCESS = {'COMPLETE', 'COMPLETE_IDENTICAL_LOSSES', 'COMPLETE_SINGLE_METHOD'}
METRICS = ('matched_FI_membership', 'literal_sole_FI', 'sole_loss_class_FI',
           'historical_only', 'rolling_F_membership', 'broad_FI_or_rolling_F_membership')


def _native(value):
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        return str(value)
    if isinstance(value, Integral):
        return int(value)
    if isinstance(value, Real):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError('nonfinite scalar metadata')
        return number
    if isinstance(value, dict):
        return {str(k): _native(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_native(v) for v in value]
    raise ValueError('metadata must contain scalar JSON values, not loss vectors')


def _identity(row):
    raw = row.get('identity', row)
    result = {name: _native(raw[name]) for name in IDENTITY}
    if (not all(isinstance(result[name], str) and result[name] for name in IDENTITY[:2])
            or not all(type(result[name]) is int and result[name] > 0 for name in IDENTITY[2:])):
        raise ValueError('invalid comparison identity')
    return tuple(result[name] for name in IDENTITY), result


def _registry(group, labels):
    key, identity = _identity(group)
    label = str(group['group_label'])
    if label not in labels:
        raise ValueError('unplanned comparison group label')
    methods, classes = [], {}
    for entry in group['methods']:
        method = entry.get('method_id')
        kind = entry.get('method_class')
        if not isinstance(method, str) or not method or method in classes or kind not in CLASSES:
            raise ValueError('method IDs must be unique and explicitly classified')
        methods.append(_native(entry)); classes[str(method)] = str(kind)
    unavailable, na_ids = [], set()
    for entry in group.get('unavailable_methods', []):
        item = dict(method_id=entry, method_class=None) if isinstance(entry, str) else _native(entry)
        method = item.get('method_id')
        if not isinstance(method, str) or not method or method in na_ids or method in classes:
            raise ValueError('unavailable method identity overlaps or is duplicated')
        kind = item.get('method_class')
        if kind is not None and kind not in CLASSES:
            raise ValueError('invalid unavailable method class')
        unavailable.append(item); na_ids.add(method)
    return key, dict(identity=identity, group_label=label, registry_status=str(group.get('status', 'UNSPECIFIED')),
                     method_metadata=methods, method_classes=classes, method_ids=sorted(classes),
                     unavailable_methods=unavailable)


def _validated_success(row, method_ids, size):
    """Validate only saved membership metadata; never recompute a p-value."""
    ids = row.get('method_ids')
    if not isinstance(ids, list) or len(ids) != len(set(ids)) or set(ids) != set(method_ids):
        raise ValueError('COMPLETE_METHOD_INVENTORY_MISMATCH')
    n = row.get('n')
    if not isinstance(n, Integral) or isinstance(n, bool) or n <= 0:
        raise ValueError('INVALID_COMPLETE_ORIGIN_COUNT')
    included, excluded = row.get('included'), row.get('excluded')
    if not isinstance(included, list) or not isinstance(excluded, list):
        raise ValueError('INVALID_MEMBERSHIP_LISTS')
    if (not included or len(included) != len(set(included)) or len(excluded) != len(set(excluded))
            or set(included) & set(excluded) or set(included) | set(excluded) != set(method_ids)):
        raise ValueError('INCOMPLETE_OR_OVERLAPPING_MEMBERSHIP_PARTITION')
    raw_pvalues = row.get('pvalues')
    if not isinstance(raw_pvalues, dict) or set(raw_pvalues) != set(method_ids):
        raise ValueError('INCOMPLETE_PVALUE_INVENTORY')
    pvalues = {}
    for method, raw in raw_pvalues.items():
        if not isinstance(raw, Real) or isinstance(raw, bool) or not math.isfinite(raw) or not 0 <= raw <= 1:
            raise ValueError('INVALID_PVALUE')
        value = float(raw)
        if (method in included) != (value > size):
            raise ValueError('MEMBERSHIP_DISAGREES_WITH_LITERAL_ARCH_BOUNDARY')
        pvalues[str(method)] = value
    groups, seen = [], set()
    for entry in row.get('unique_loss_groups', []):
        members = entry.get('members', entry.get('methods'))
        representative = entry.get('representative')
        if (not isinstance(members, list) or not members or len(members) != len(set(members))
                or not set(members) <= set(method_ids) or seen & set(members)
                or representative != min(members)):
            raise ValueError('INVALID_EXACT_LOSS_CLASS_PARTITION')
        if not (set(members) <= set(included) or set(members) <= set(excluded)):
            raise ValueError('EXACT_LOSS_CLASS_PARTLY_INCLUDED')
        if any(pvalues[m] != pvalues[representative] for m in members):
            raise ValueError('EXACT_LOSS_CLASS_PVALUES_DIFFER')
        seen.update(members)
        groups.append(dict(representative=str(representative), members=sorted(str(m) for m in members)))
    if seen != set(method_ids):
        raise ValueError('MISSING_EXACT_LOSS_CLASS_MEMBERS')
    if row['status'] == 'COMPLETE_IDENTICAL_LOSSES' and (len(groups) != 1 or excluded or any(p != 1. for p in pvalues.values())):
        raise ValueError('INVALID_IDENTICAL_LOSS_ANALYTIC_RECEIPT')
    if row['status'] == 'COMPLETE_SINGLE_METHOD' and (len(method_ids) != 1 or excluded or any(p != 1. for p in pvalues.values())):
        raise ValueError('INVALID_SINGLE_METHOD_ANALYTIC_RECEIPT')
    return dict(n=int(n), included=sorted(str(m) for m in included), excluded=sorted(str(m) for m in excluded),
                pvalues=pvalues, unique_loss_groups=groups)


def _cell(plan, rows, size):
    cell = dict(plan)
    cell.update(record_count=len(rows), status='MISSING_RESULT' if not rows else 'DUPLICATE_RESULT' if len(rows) > 1 else str(rows[0].get('status', 'MISSING_STATUS')),
                reported_status=None if len(rows) != 1 else str(rows[0].get('status', 'MISSING_STATUS')),
                n=None, included=[], excluded=[], pvalues={}, unique_loss_groups=[],
                summary_failure=None, reason=None, successful=False,
                metrics={m: None for m in METRICS}, conditional_included=[], conditional_excluded=[],
                surviving_loss_classes=[], single_method_analytic=False)
    if len(rows) != 1:
        return cell
    row = rows[0]
    if cell['status'] not in SUCCESS:
        cell['reason'] = None if row.get('reason') is None else str(row['reason'])
        return cell
    try:
        if cell['registry_status'].startswith('FAILED') or cell['registry_status'] == 'UNAVAILABLE':
            raise ValueError('SUCCESS_CONTRADICTS_FAILED_REGISTRY_INPUT')
        cell.update(_validated_success(row, cell['method_ids'], size))
    except (ValueError, TypeError, KeyError) as exc:
        cell.update(status='FAILED_INPUT', summary_failure=str(exc))
        return cell
    matched = {m for m, c in cell['method_classes'].items() if c == 'matched_historical'}
    rolling = {m for m, c in cell['method_classes'].items() if c == 'other_historical'}
    conditional = {m for m, c in cell['method_classes'].items() if c == 'conditional'}
    included = set(cell['included'])
    surviving = [g for g in cell['unique_loss_groups'] if set(g['members']) <= included]
    cell.update(successful=True, single_method_analytic=cell['status'] == 'COMPLETE_SINGLE_METHOD',
                surviving_loss_classes=surviving, conditional_included=sorted(included & conditional),
                conditional_excluded=sorted(set(cell['excluded']) & conditional),
                metrics=dict(matched_FI_membership=bool(included & matched),
                    literal_sole_FI=len(included) == 1 and bool(included & matched),
                    sole_loss_class_FI=len(surviving) == 1 and bool(set(surviving[0]['members']) & matched),
                    historical_only=bool(included) and included <= matched,
                    rolling_F_membership=bool(included & rolling),
                    broad_FI_or_rolling_F_membership=bool(included & (matched | rolling))))
    return cell


def _fraction(numerator, denominator):
    return float(numerator/denominator) if denominator else None


def _aggregate(cells, label):
    planned = len(cells)
    good = [c for c in cells if c['successful']]
    failed = planned-len(good)
    metrics = {}
    for name in METRICS:
        count = sum(c['metrics'][name] for c in good)
        metrics[name] = dict(count_successful=int(count), denominator_successful=len(good),
            fraction_successful=_fraction(count, len(good)), denominator_all_planned=planned,
            lower_count_all_planned=int(count), upper_count_all_planned=int(count+failed),
            fraction_all_planned_lower=_fraction(count, planned), fraction_all_planned_upper=_fraction(count+failed, planned))
    successful_cond = sum(sum(k == 'conditional' for k in c['method_classes'].values()) for c in good)
    failed_cond = sum(sum(k == 'conditional' for k in c['method_classes'].values()) for c in cells if not c['successful'])
    na = [m for c in cells for m in c['unavailable_methods']]
    excluded = sum(len(c['conditional_excluded']) for c in good)
    conditional = dict(excluded_slots=excluded, successful_complete_slots=successful_cond,
        failed_complete_slots=failed_cond, planned_complete_slots=successful_cond+failed_cond,
        known_na_slots=sum(m.get('method_class') == 'conditional' for m in na),
        fraction_successful=_fraction(excluded, successful_cond),
        fraction_all_planned_lower=_fraction(excluded, successful_cond+failed_cond),
        fraction_all_planned_upper=_fraction(excluded+failed_cond, successful_cond+failed_cond),
        all_planned_lower_excluded_slots=excluded, all_planned_upper_excluded_slots=excluded+failed_cond,
        denominator_note='Known unavailable methods are counted separately and enter neither statistical exclusion numerator nor complete-slot denominator.')
    return dict(group_label=label, planned_comparisons=planned, successful_comparisons=len(good), failed_comparisons=failed,
        unavailable_comparisons=sum(c['status'] == 'UNAVAILABLE' for c in cells),
        single_method_comparisons=sum(c['single_method_analytic'] for c in good),
        identical_loss_comparisons=sum(c['status'] == 'COMPLETE_IDENTICAL_LOSSES' for c in good),
        status_counts=dict(Counter(c['status'] for c in cells)),
        failed_cells=[dict(identity=c['identity'], status=c['status'], reason=c['reason'], summary_failure=c['summary_failure']) for c in cells if not c['successful']],
        unavailable_method_slots=len(na), unavailable_unclassified_slots=sum(m.get('method_class') is None for m in na),
        metrics=metrics, conditional_exclusion=conditional)


def summarize(records, registry_groups, design):
    """Count literal unfolded saved memberships with both registered denominators.

    Registry classes alone determine procedure categories. Failed comparisons
    contribute unknown planned-grid outcomes/complete conditional slots, never
    favourable exclusions. Known NA procedures remain separate from both.
    """
    labels = [str(x) for x in design['report']['groups'] if x != 'All comparisons']
    if len(labels) != len(set(labels)):
        raise ValueError('duplicate report group label')
    size = float(design['size'])
    if not math.isfinite(size) or not 0 < size < 1:
        raise ValueError('invalid registered MCS size')
    plans, order = {}, []
    for group in registry_groups:
        key, value = _registry(group, labels)
        if key in plans:
            raise ValueError('duplicate registry comparison identity')
        plans[key] = value; order.append(key)
    indexed = defaultdict(list)
    for row in records:
        key, _ = _identity(row)
        if key not in plans:
            raise ValueError('result outside planned registry inventory')
        indexed[key].append(row)
    cells = [_cell(plans[key], indexed[key], size) for key in order]
    return dict(groups_summary=[_aggregate([c for c in cells if c['group_label'] == label], label) for label in labels],
                overall=_aggregate(cells, 'All comparisons'), cells=cells)
