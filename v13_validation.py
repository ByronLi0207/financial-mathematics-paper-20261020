"""Pure geometry and fixed-denominator summaries for pre-specified v13 G2.

No source access, fitting, forecasting, outcome scoring, or file writing.
"""
from collections import Counter
import math
from statistics import median
from v12_decomposition import PANEL_SOURCE_KEYS

NYFED_KEYS=('PDPOSGS-B',*PANEL_SOURCE_KEYS)


def validation_geometry(horizon,length):
    if horizon not in (6,24) or length not in (52,156):
        raise ValueError('UNDECLARED_G2_GEOMETRY')
    return (329,380) if length==52 else (405-horizon-156,405-horizon-1)


def g2_cells(sources):
    owned=[s for s in sources if s['family'] in ('bill','panel')]
    if len(owned)!=13 or len({s['key'] for s in owned})!=13:
        raise ValueError('THIRTEEN_UNIQUE_NYFED_SOURCES_REQUIRED')
    owned.sort(key=lambda s:(s['family']!='bill',next((j for j,k in enumerate(PANEL_SOURCE_KEYS) if k==s['key']),100)))
    cells=[]
    for h in (6,24):
        for source in owned:
            for v in (52,156):
                va,vb=validation_geometry(h,v)
                cells.append(dict(experiment='G2',cell_id=f"G2-{source['family']}-{source['key']}-original-H{h}-W52-V{v}-tau0.95",
                    family=source['family'],source_key=source['key'],source_index=source.get('source_index'),
                    period='original',horizon=h,window=52,tau=.95,refit_step=13,
                    validation_first=va,validation_last=vb,validation_n=v,
                    evaluation_first=405,evaluation_last=681,evaluation_n=277,
                    short_scale=source['short_scale'],long_scale=source['long_scale'],
                    nominal_gap_seconds=source['nominal_gap_seconds'],source=source))
    return cells


def _usable(row):
    return bool(row is not None and row.get('status')=='COMPLETE'
        and isinstance(row.get('relative_loss_pct'),(float,int))
        and math.isfinite(row['relative_loss_pct'])
        and isinstance(row.get('reference_loss'),(float,int))
        and math.isfinite(row['reference_loss']) and row['reference_loss']>0
        and isinstance(row.get('actual_loss'),(float,int))
        and math.isfinite(row['actual_loss']) and row['actual_loss']>=0
        and row.get('selected_penalty') in (.001,.01,.1,1.,10.,'inf'))


def _and(statuses):
    if 'NOT_SUPPORTED' in statuses:return 'NOT_SUPPORTED'
    return 'SUPPORTED' if statuses and all(s=='SUPPORTED' for s in statuses) else 'UNDETERMINED'


def summarize_g2(rows):
    """Require all13 fixed source pairs; subset statistics remain descriptive."""
    rows=list(rows);out=dict(experiment='G2',primary_method='QR33',planned_method_cells=104,methods={})
    for method in ('QR33','QR4'):
        result=dict(by_horizon={})
        for h in (6,24):
            arms={};pairs=[];selected={}
            for v in (52,156):
                slots=[]
                for key in NYFED_KEYS:
                    matches=[r for r in rows if (r.get('method'),r.get('horizon'),r.get('window'),r.get('validation_n'),r.get('source_key'))==(method,h,52,v,key)]
                    row=matches[0] if len(matches)==1 else None
                    slots.append(row);selected[(v,key)]=row
                valid=[r for r in slots if _usable(r)]
                counts=Counter((r.get('status','MISSING_STATUS') if r else 'MISSING_OR_DUPLICATE') for r in slots)
                vals=[r['relative_loss_pct'] for r in valid]
                arms[str(v)]=dict(planned=13,complete=len(valid),unavailable=13-len(valid),
                    status_counts=dict(counts),median_relative_loss_pct=median(vals) if len(vals)==13 else None,
                    descriptive_complete_row_median_relative_loss_pct=median(vals) if vals else None,
                    known_infinity_count=sum(r['selected_penalty']=='inf' for r in valid))
            for key in NYFED_KEYS:
                a,b=selected[(52,key)],selected[(156,key)]
                if _usable(a) and _usable(b):pairs.append((key,a,b))
            mdiff=(arms['156']['median_relative_loss_pct']-arms['52']['median_relative_loss_pct']) if len(pairs)==13 else None
            inf={v:arms[v]['known_infinity_count'] if len(pairs)==13 else None for v in ('52','156')}
            desc=None
            if pairs:
                desc=dict(n=len(pairs),source_keys=[p[0] for p in pairs],
                    median_relative_loss_by_validation={'52':median(p[1]['relative_loss_pct'] for p in pairs),'156':median(p[2]['relative_loss_pct'] for p in pairs)},
                    median_difference_pct_points=median(p[2]['relative_loss_pct'] for p in pairs)-median(p[1]['relative_loss_pct'] for p in pairs),
                    median_paired_change_pct_points=median(p[2]['relative_loss_pct']-p[1]['relative_loss_pct'] for p in pairs),
                    interpretation='Incomplete-pair subsets are descriptive, never a replacement denominator.')
            result['by_horizon'][str(h)]=dict(horizon=h,planned_sources=13,complete_pair_count=len(pairs),
                arm_counts=arms,median_relative_loss_by_validation={v:arms[v]['median_relative_loss_pct'] for v in ('52','156')},
                median_difference_pct_points=mdiff,infinity_count_by_validation=inf,
                descriptive_complete_pairs=desc,
                V3='UNDETERMINED' if mdiff is None else 'SUPPORTED' if mdiff<=-5. else 'NOT_SUPPORTED',
                V4='UNDETERMINED' if len(pairs)!=13 else 'SUPPORTED' if inf['156']>inf['52'] else 'NOT_SUPPORTED')
        for criterion in ('V3','V4'):
            result[criterion]=_and([x[criterion] for x in result['by_horizon'].values()])
        out['methods'][method]=result
    out.update(V3=out['methods']['QR33']['V3'],V4=out['methods']['QR33']['V4'],
        interpretation='Retrospective equal-cell descriptive comparison; H6 long validation also shifts endpoint18weeks and refit phase. No causal length-only interpretation or independent-series pooled test.')
    return out
