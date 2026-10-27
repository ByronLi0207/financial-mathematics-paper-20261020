"""Pure geometry, paired evidence gate and fixed-universe v13 RP summaries.

A retrospective heuristic combines existing rules, not a new model or formal
risk guarantee. No source access, fitting, forecasts or scoring occurs here.
"""
from collections import Counter
import math
from statistics import median
import numpy as np
from inference_tests import bandwidth,hac
from v12_decomposition import CFTC_SOURCE_KEYS,PANEL_SOURCE_KEYS

NYFED_KEYS=('PDPOSGS-B',*PANEL_SOURCE_KEYS)


def decision_from_evidence(mean,se):
    return 'QR' if mean<0 and -mean>se else 'F'


def paired_gate(qr_losses,f_losses,horizon):
    qr=np.asarray(qr_losses,dtype=float);f=np.asarray(f_losses,dtype=float)
    base=dict(status='UNAVAILABLE',route='F',reason=None,n=len(qr),bandwidth=None,
        mean_difference=None,lrv=None,standard_error=None)
    if qr.ndim!=1 or f.shape!=qr.shape or len(qr)<=horizon:
        return dict(base,reason='FULL_ALIGNED_PAIRED_LOSSES_REQUIRED')
    if not np.isfinite(qr).all() or not np.isfinite(f).all():
        return dict(base,reason='NONFINITE_PAIRED_LOSSES')
    with np.errstate(over='ignore',invalid='ignore'):d=qr-f
    if not np.isfinite(d).all():return dict(base,reason='NONFINITE_PAIRED_DIFFERENCE')
    mean=math.fsum(map(float,d))/len(d);k=bandwidth(len(d),horizon)
    with np.errstate(over='ignore',invalid='ignore'):omega=float(hac(d,k)[0,0])
    base.update(mean_difference=mean,bandwidth=k)
    if not math.isfinite(omega) or omega<0:
        return dict(base,reason='NEGATIVE_OR_NONFINITE_HAC_VARIANCE')
    se=math.sqrt(omega/len(d))
    return dict(base,status='AVAILABLE',route=decision_from_evidence(mean,se),reason=None,
        lrv=omega,standard_error=se,strict_mean_improvement=mean<0,strict_one_se_improvement=-mean>se)


def expected_slots():
    rows=[]
    for h in (6,24):
        for key in NYFED_KEYS:rows.append(dict(family='bill' if key=='PDPOSGS-B' else 'panel',source_key=key,period='original',horizon=h,window=52))
    for w in (52,260):
        for key in CFTC_SOURCE_KEYS:rows.append(dict(family='cftc',source_key=key,period='original',horizon=6,window=w))
    for period in ('original','early2015'):rows.append(dict(family='fx',source_key='fx_hourly',period=period,horizon=6,window=2880))
    return rows


def _slot(row):return tuple(row[k] for k in ('family','source_key','period','horizon','window'))


def rp_cells(sources):
    indexed={(s['family'],s['key']):s for s in sources};cells=[]
    for slot in expected_slots():
        family,key,period,h,w=_slot(slot)
        if (family,key) not in indexed:raise ValueError('FIXED_SOURCE_MISSING:'+key)
        source=indexed[(family,key)]
        if family=='cftc':va,vb,ea,eb,ba,bb,d=449,604,611,870,553,604,13
        elif family in ('bill','panel'):va,vb,ea,eb,ba,bb,d=405-h-156,405-h-1,405,681,329,380,13
        elif period=='original':va,vb,ea,eb,ba,bb,d=6143,11902,11927,18551,10463,11902,24
        else:va,vb,ea,eb,ba,bb,d=3215,8974,8999,10438,7535,8974,24
        first=va-h-w+1;valid=max(24,source['short_scale'],source['long_scale'])
        eligible=first>=valid and eb+h<source['N'] and vb+h<ea and bb+h<ea
        cells.append(dict(slot,experiment='G3',cell_id=f'G3-{family}-{key}-{period}-H{h}-W{w}-tau0.95',
            tau=.95,refit_step=d,validation_first=va,validation_last=vb,validation_n=vb-va+1,
            baseline_validation_first=ba,baseline_validation_last=bb,baseline_validation_n=bb-ba+1,
            evaluation_first=ea,evaluation_last=eb,evaluation_n=eb-ea+1,
            short_scale=source['short_scale'],long_scale=source['long_scale'],nominal_gap_seconds=source['nominal_gap_seconds'],
            eligible=bool(eligible),earliest_training_origin=first,feature_valid_from=valid,
            exclusion_reason=None if eligible else 'INSUFFICIENT_COMPLETE_FEATURE_OR_LABEL_HISTORY',source=source))
    return cells


def _usable(row,method='rp'):
    return bool(row and row.get(method+'_status')=='COMPLETE' and row.get('F_status')=='COMPLETE'
        and isinstance(row.get(method+'_relative_loss_pct'),(int,float)) and math.isfinite(row[method+'_relative_loss_pct'])
        and isinstance(row.get('reference_loss'),(int,float)) and math.isfinite(row['reference_loss']) and row['reference_loss']>0
        and isinstance(row.get(method+'_loss'),(int,float)) and math.isfinite(row[method+'_loss']) and row[method+'_loss']>=0)


def _group(slots):
    eligible=[r for r in slots if not(r and r.get('eligible') is False)]
    good=[r for r in eligible if _usable(r)]
    vals=[r['rp_relative_loss_pct'] for r in good]
    routes=Counter(r.get('route') for r in good)
    ordinary=[r['ordinary_relative_loss_pct'] for r in eligible if _usable(r,'ordinary')]
    n=len(eligible)
    return dict(planned=len(slots),eligible=n,excluded=len(slots)-n,complete=len(good),unavailable=n-len(good),
        median_relative_loss_pct=median(vals) if vals and len(good)==n else None,
        descriptive_complete_median_relative_loss_pct=median(vals) if vals else None,
        worst_relative_loss_pct=max(vals) if vals else None,
        ordinary_complete=len(ordinary),ordinary_median_relative_loss_pct=median(ordinary) if ordinary and len(ordinary)==n else None,
        ordinary_descriptive_complete_median_relative_loss_pct=median(ordinary) if ordinary else None,
        adverse_gt10_count=sum(v>10 for v in vals),fallback_count=routes['F'],regression_count=routes['QR'],
        unknown_route_count=n-routes['F']-routes['QR'],
        fallback_fraction_of_planned=routes['F']/n if n else None,
        fallback_fraction_of_complete=routes['F']/len(good) if good else None)


def summarize_rp(rows):
    rows=list(rows);slots=[]
    for expected in expected_slots():
        matches=[r for r in rows if _slot(r)==_slot(expected)]
        slots.append(matches[0] if len(matches)==1 else None)
    weekly=_group(slots[:60]);fxslots=slots[60:];fx={}
    for period,row in zip(('original','early2015'),fxslots):
        complete=_usable(row) and _usable(row,'ordinary')
        threshold=.5*row['ordinary_relative_loss_pct'] if complete and row['ordinary_relative_loss_pct']<0 else None
        status=('UNDETERMINED' if not complete else 'NOT_APPLICABLE' if threshold is None else
                'SUPPORTED' if row['rp_relative_loss_pct']<=threshold else 'NOT_SUPPORTED')
        fx[period]=dict(status=status,complete=complete,ordinary_relative_loss_pct=row.get('ordinary_relative_loss_pct') if row else None,
            rp_relative_loss_pct=row.get('rp_relative_loss_pct') if row else None,half_gain_threshold_pct=threshold,
            route=row.get('route') if row else None)
    status3=('NOT_SUPPORTED' if any(p['status']=='NOT_SUPPORTED' for p in fx.values()) else
             'UNDETERMINED' if any(p['status']=='UNDETERMINED' for p in fx.values()) else
             'SUPPORTED' if any(p['status']=='SUPPORTED' for p in fx.values()) else 'NOT_APPLICABLE')
    n=weekly['eligible'];bad=weekly['adverse_gt10_count']
    status1='UNDETERMINED' if weekly['median_relative_loss_pct'] is None else 'SUPPORTED' if weekly['median_relative_loss_pct']<=1. else 'NOT_SUPPORTED'
    status2=('NOT_SUPPORTED' if n and bad/n>.05 else 'UNDETERMINED' if weekly['unavailable'] or not n else 'SUPPORTED')
    groups={}
    for family,selected in [('cftc',slots[26:60]),('nyfed',slots[:26]),('fx',slots[60:])]:groups[family]=_group(selected)
    detail={}
    for expected,row in zip(expected_slots(),slots):
        family=expected['family'];key=f"{family}-H{expected['horizon']}-W{expected['window']}-{expected['period']}"
        detail.setdefault(key,[]).append(row)
    return dict(experiment='G3',R1=status1,R2=status2,R3=status3,weekly=weekly,FX=dict(periods=fx),
        groups=groups,fallback_by_geometry={k:_group(v) for k,v in detail.items()},
        planned_geometry_cells=62,received_rows=len(rows),
        interpretation='Retrospective heuristic designed after prior results. Equal-cell normalized losses, no independent-series combined test or prospective protection guarantee; unavailable fits are never credited as successful fallback.')
