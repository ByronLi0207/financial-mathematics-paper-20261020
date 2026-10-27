"""Pure v12 aggregate screens with protocol-fixed slots and missingness bounds.

The functions read only the saved scientific contracts and caller-owned scalar
rows. They never read observations/traces, fit, predict, score, acquire, or write.
Missing/duplicate/invalid rows are visible planned slots, never favorable picks.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
import json
import math
from numbers import Real
from pathlib import Path
import re
from statistics import median


ROOT = Path(__file__).resolve().parent
PROTOCOLS = {'F2':'validation-length-design.md','F3':'tau-design.md'}
IDENTITY = ('family','source_key','period','horizon','window','validation_n','tau','method')


def _protocol(experiment):
    text = (ROOT/'protocol/v12'/PROTOCOLS[experiment]).read_text()
    blocks = re.findall(r'```json\s*\n(.*?)\n```',text,re.S)
    if len(blocks)!=1:
        raise ValueError('PROTOCOL_JSON_REQUIRED')
    value = json.loads(blocks[0])
    if value.get('experiment')!=experiment:
        raise ValueError('PROTOCOL_EXPERIMENT_MISMATCH')
    return value


def _finite(value):
    return isinstance(value,Real) and not isinstance(value,bool) and math.isfinite(value)


def _safe(value):
    if isinstance(value,dict):
        return {key:_safe(item) for key,item in value.items()}
    if isinstance(value,(list,tuple)):
        return [_safe(item) for item in value]
    if isinstance(value,Real) and not isinstance(value,bool):
        return value if math.isfinite(value) else None
    return value


def _key(row):
    return tuple(row.get(field) for field in IDENTITY)


def _identity(family,key,period,horizon,window,validation_n,tau,method):
    return dict(zip(IDENTITY,(family,key,period,horizon,window,validation_n,tau,method)))


def _penalty_valid(value,menu):
    return value=='inf' if isinstance(value,str) else (
        _finite(value) and value in [p for p in menu if not isinstance(p,str)])


def _usable(row,menu):
    return (row.get('status')=='COMPLETE'
        and _finite(row.get('relative_loss_pct'))
        and _finite(row.get('reference_loss')) and row['reference_loss']>0
        and _finite(row.get('actual_loss')) and row['actual_loss']>=0
        and _penalty_valid(row.get('selected_penalty'),menu))


def _slots(expected,rows,menu):
    by_identity = defaultdict(list)
    for row in rows:
        by_identity[_key(row)].append(row)
    slots = []
    expected_keys = {_key(item) for item in expected}
    for identity in expected:
        matches = by_identity[_key(identity)]
        slot = dict(identity,usable=False,relative_loss_pct=None,selected_penalty=None,
                    cell_ids=[row.get('cell_id') for row in matches],
                    received_row_count=len(matches),reported_statuses=[row.get('status') for row in matches])
        if not matches:
            slot.update(status='MISSING_ROW',reason='PLANNED_SLOT_NOT_RECEIVED')
        elif len(matches)>1:
            slot.update(status='DUPLICATE_INPUT',reason='NO_ROW_SELECTED_FROM_DUPLICATES')
        else:
            row = matches[0]
            valid = _usable(row,menu)
            slot.update(status=row.get('status','MISSING_STATUS'),usable=valid,
                        row=_safe(deepcopy(row)),reason=row.get('reason'))
            if valid:
                slot.update(relative_loss_pct=float(row['relative_loss_pct']),
                            selected_penalty=row['selected_penalty'])
            elif row.get('status')=='COMPLETE':
                slot.update(status='INVALID_COMPLETE_ROW',
                            reason='FINITE_RELATIVE_LOSS_POSITIVE_REFERENCE_AND_DECLARED_SELECTION_REQUIRED')
        slots.append(slot)
    unexpected = [_safe(deepcopy(row)) for row in rows if _key(row) not in expected_keys]
    return slots,unexpected


def _counts(slots):
    counts = Counter(slot['status'] for slot in slots)
    return dict(planned=len(slots),received=sum(s['received_row_count'] for s in slots),
        complete=sum(s['status']=='COMPLETE' for s in slots),usable=sum(s['usable'] for s in slots),
        failed=sum(s['status'].startswith('FAILED') or s['status']=='INVALID_COMPLETE_ROW' for s in slots),
        resource=sum('RESOURCE' in s['status'] or 'TIME_LIMIT' in s['status'] for s in slots),
        not_run=sum(s['status'].startswith('NOT_RUN') for s in slots),
        missing=counts['MISSING_ROW'],duplicate_slots=counts['DUPLICATE_INPUT'],
        invalid_complete=counts['INVALID_COMPLETE_ROW'],unknown=sum(not s['usable'] for s in slots),
        status_counts=dict(sorted(counts.items())))


def _median(values):
    return None if not values else float(median(values))


def _descriptive_groups(slots):
    dimensions = ('family','period','horizon','window','validation_n','tau','method')
    grouped = {}
    for slot in slots:
        key = tuple(slot[d] for d in dimensions)
        grouped.setdefault(key,[]).append(slot)
    result = []
    for key,owned in grouped.items():
        valid = [s['relative_loss_pct'] for s in owned if s['usable']]
        result.append(dict(zip(dimensions,key),counts=_counts(owned),
            descriptive_complete_row_median_relative_loss_pct=_median(valid),
            F_strictly_better_count=sum(value>0 for value in valid),
            regression_strictly_better_count=sum(value<0 for value in valid),
            tie_count=sum(value==0 for value in valid),
            estimand='Equal-cell descriptive relative-loss summary; incomplete subsets explicitly counted; no native-unit pooling or independence test.'))
    return result


def _conjunction(statuses):
    if any(status=='NOT_SUPPORTED' for status in statuses):
        return 'NOT_SUPPORTED'
    if statuses and all(status=='SUPPORTED' for status in statuses):
        return 'SUPPORTED'
    return 'UNDETERMINED'


def _eligibility(eligibility,canonical):
    declarations = []
    for item in eligibility:
        declarations.append(dict(source_key=item,eligible=True) if isinstance(item,str) else deepcopy(item))
    seen = set()
    for item in declarations:
        key = item.get('source_key',item.get('key'))
        if key not in canonical or key in seen or type(item.get('eligible')) is not bool:
            raise ValueError('INVALID_OR_DUPLICATE_ELIGIBILITY_DECLARATION')
        item['source_key']=key
        seen.add(key)
    eligible = [key for key in canonical if any(r['source_key']==key and r['eligible'] for r in declarations)]
    excluded = [r for r in declarations if not r['eligible']]
    excluded.extend(dict(source_key=key,eligible=False,reason='NOT_IN_ELIGIBLE_LIST')
                    for key in canonical if key not in seen)
    return eligible,excluded


def summarize_validation(rows,eligibility):
    """F2: difference of fixed-denominator medians, and strict infinity increase.

    ``eligibility`` is either the pre-gate list of eligible literal CFTC codes
    or all dictionaries returned by v12_inputs.f2_eligibility_inventory().
    Solver/resource completion can never change that eligible denominator.
    """
    design = _protocol('F2')
    canonical = [r['code'] for r in design['input_provenance']['cftc_sources']]
    eligible,excluded = _eligibility(eligibility,canonical)
    windows = design['windows']
    lengths = design['validation_lengths']
    if lengths!=[52,156]:
        raise ValueError('UNSUPPORTED_VALIDATION_LENGTH_CONTRACT')
    match = re.search(r'<=(-?\d+(?:\.\d+)?) percentage points',design['predictions']['V1'])
    if match is None:
        raise ValueError('V1_THRESHOLD_NOT_FOUND_IN_PROTOCOL')
    threshold = float(match.group(1))
    expected = [_identity('cftc',key,'original',design['H'],w,v,design['tau'],method)
                for method in design['methods'] for w in windows for key in eligible for v in lengths]
    rows = list(rows)
    slots,unexpected = _slots(expected,rows,design['menu'])
    methods = {}
    n = len(eligible)
    for method in design['methods']:
        by_window = {}
        for w in windows:
            owned = [s for s in slots if s['method']==method and s['window']==w]
            arms = {str(v):[s for s in owned if s['validation_n']==v] for v in lengths}
            paired = []
            for key in eligible:
                pair = [next(s for s in arms[str(v)] if s['source_key']==key) for v in lengths]
                if all(s['usable'] for s in pair):
                    paired.append(pair)
            all_complete = bool(n) and len(paired)==n
            pair_medians = {str(v):_median([pair[j]['relative_loss_pct'] for pair in paired])
                            for j,v in enumerate(lengths)}
            pair_difference = (pair_medians['156']-pair_medians['52']) if paired else None
            medians = pair_medians.copy() if all_complete else {'52':None,'156':None}
            difference = pair_difference if all_complete else None
            inf_counts = {str(v):sum(s['usable'] and s['selected_penalty']=='inf' for s in arms[str(v)]) for v in lengths}
            fractions = {str(v):(inf_counts[str(v)]/n if n and all(s['usable'] for s in arms[str(v)]) else None) for v in lengths}
            bounds = {str(v):([inf_counts[str(v)]/n,
                              (inf_counts[str(v)]+sum(not s['usable'] for s in arms[str(v)]))/n] if n else [None,None]) for v in lengths}
            v1 = ('SUPPORTED' if difference<=threshold else 'NOT_SUPPORTED') if all_complete else 'UNDETERMINED'
            v2 = ('SUPPORTED' if inf_counts['156']>inf_counts['52'] else 'NOT_SUPPORTED') if all_complete else 'UNDETERMINED'
            by_window[str(w)] = dict(window=w,eligible_contracts=n,complete_pair_count=len(paired),
                missing_pair_count=n-len(paired),complete_pair_source_keys=[p[0]['source_key'] for p in paired],
                median_relative_loss_by_validation=medians,median_difference_pct_points=difference,
                known_infinity_count_by_validation=inf_counts,infinity_fraction_by_validation=fractions,
                infinity_fraction_bounds_by_validation=bounds,
                arm_counts={str(v):_counts(arms[str(v)]) for v in lengths},
                descriptive_complete_pairs=dict(n=len(paired),source_keys=[p[0]['source_key'] for p in paired],
                    median_relative_loss_by_validation=pair_medians,
                    median_difference_pct_points=pair_difference,
                    median_paired_change_pct_points=_median([p[1]['relative_loss_pct']-p[0]['relative_loss_pct'] for p in paired]),
                    infinity_count_by_validation={str(v):sum(p[j]['selected_penalty']=='inf' for p in paired) for j,v in enumerate(lengths)},
                    interpretation='Complete-pair subset is descriptive only; it does not replace the eligible denominator.'),
                V1=v1,V2=v2)
        v1_states = {w:d['V1'] for w,d in by_window.items()}
        v2_states = {w:d['V2'] for w,d in by_window.items()}
        methods[method] = dict(by_window=by_window,
            V1=dict(status=_conjunction(list(v1_states.values())),by_window=v1_states,
                    threshold_pct_points=threshold,rule='median156 minus median52 <= threshold in both windows'),
            V2=dict(status=_conjunction(list(v2_states.values())),by_window=v2_states,
                    rule='infinity156 count strictly exceeds infinity52 count in both windows'))
    primary = 'QR33'
    return dict(experiment='F2',primary_method=primary,eligible_contract_count=n,
        eligible_contracts=eligible,excluded_contracts=_safe(excluded),methods=methods,
        V1=deepcopy(methods[primary]['V1']),V2=deepcopy(methods[primary]['V2']),
        predictions={name:deepcopy(methods[primary][name]) for name in ('V1','V2')},
        counts=_counts(slots),received_input_rows=len(rows),unexpected_row_count=len(unexpected),
        unexpected_rows=unexpected,slot_inventory=slots,descriptive_groups=_descriptive_groups(slots),
        interpretation=design['predictions']['missing'])


def _explicit_geometry(text):
    match = re.fullmatch(r'H(\d+)/W(\d+),validation(\d+)\.\.(\d+)/evaluation(\d+)\.\.(\d+)/d(\d+)',text)
    if match is None:
        raise ValueError('UNSUPPORTED_TAU_GEOMETRY')
    h,w,a,b,_,_,_ = map(int,match.groups())
    return h,w,b-a+1


def summarize_tau(rows):
    """F3: fixed 34-cell .99 F-win bound and both-period matched FX screen."""
    design = _protocol('F3')
    codes = [r['code'] for r in design['input_provenance']['cftc_sources']]
    geometry = re.fullmatch(r'(\d+)xW(\d+)/(\d+),H(\d+),unchangedV(\d+)/eval(\d+)/d(\d+)',design['geometries']['cftc'])
    threshold = re.search(r'at least\s*(\d+) of\s*(\d+)',design['predictions']['Q1'])
    if geometry is None or threshold is None:
        raise ValueError('TAU_CONTRACT_NOT_UNDERSTOOD')
    count,w1,w2,h,vn,_,_ = map(int,geometry.groups())
    minimum,denominator = map(int,threshold.groups())
    if count!=len(codes) or count*2!=denominator:
        raise ValueError('TAU_FIXED_DENOMINATOR_MISMATCH')
    expected = []
    for tau in sorted(design['tau_values'],reverse=True):
        expected.extend(_identity('cftc',key,'original',h,w,vn,tau,'QR33') for key in codes for w in (w1,w2))
        for period,key in [('original','fx_original'),('early2015','fx_early2015')]:
            hh,ww,v = _explicit_geometry(design['geometries'][key])
            expected.append(_identity('fx','fx_hourly',period,hh,ww,v,tau,'QR33'))
        hh,ww,v = _explicit_geometry(design['geometries']['bill'])
        expected.append(_identity('bill','PDPOSGS-B','original',hh,ww,v,tau,'QR33'))
    if len(expected)!=design['planned_cells_per_tau']*len(design['tau_values']):
        raise ValueError('TAU_PLANNED_COUNT_MISMATCH')
    rows = list(rows)
    slots,unexpected = _slots(expected,rows,design['menu'])
    cftc = [s for s in slots if s['family']=='cftc' and s['tau']==.99]
    support = sum(s['usable'] and s['relative_loss_pct']>0 for s in cftc)
    unknown = sum(not s['usable'] for s in cftc)
    q1_status = ('SUPPORTED' if support>=minimum else
                 'NOT_SUPPORTED' if support+unknown<minimum else 'UNDETERMINED')
    q1 = dict(status=q1_status,tau=.99,denominator=denominator,minimum_support=minimum,
        support_count=support,complete_nonsupport_count=denominator-support-unknown,
        unknown_count=unknown,tie_count=sum(s['usable'] and s['relative_loss_pct']==0 for s in cftc),
        support_fraction_bounds=[support/denominator,(support+unknown)/denominator],
        rule='F strictly better means relative QR33 excess loss > 0; exact zero is not a win.')
    fx = [s for s in slots if s['family']=='fx' and s['tau']==.99]
    fx_support = sum(s['usable'] and s['relative_loss_pct']<0 for s in fx)
    fx_failure = sum(s['usable'] and s['relative_loss_pct']>=0 for s in fx)
    fx_unknown = sum(not s['usable'] for s in fx)
    q2_status = 'NOT_SUPPORTED' if fx_failure else ('SUPPORTED' if fx_support==2 else 'UNDETERMINED')
    q2 = dict(status=q2_status,tau=.99,denominator=2,support_count=fx_support,
        complete_nonsupport_count=fx_failure,unknown_count=fx_unknown,
        support_fraction_bounds=[fx_support/2,(fx_support+fx_unknown)/2],
        by_period={s['period']:dict(status=('SUPPORTED' if s['relative_loss_pct']<0 else 'NOT_SUPPORTED')
                    if s['usable'] else 'UNDETERMINED',input_status=s['status'],
                    relative_loss_pct=s['relative_loss_pct']) for s in fx},
        rule='QR33 relative excess loss < 0 in both original and early2015 matched FX periods.')
    return dict(experiment='F3',Q1=q1,Q2=q2,predictions=dict(Q1=deepcopy(q1),Q2=deepcopy(q2)),
        counts=_counts(slots),received_input_rows=len(rows),unexpected_row_count=len(unexpected),
        unexpected_rows=unexpected,slot_inventory=slots,descriptive_groups=_descriptive_groups(slots),
        tau90_descriptive_only=True,interpretation=design['interpretation'])
