"""Arithmetic readback of retained working-reference p values; no forecast fits."""
import math
from inference_tests import holm

def family_readback(rows):
    ids=[r['contrast_id'] for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('duplicate contrast identity')
    def pvalue(row,column):
        if row['status']=='IDENTICAL_LOSSES':return 1.
        if row['status']!='OK':raise ValueError('unidentified component test')
        p=float(row[column])
        if not math.isfinite(p) or not 0<=p<=1:raise ValueError('invalid component probability')
        return p
    base=holm([pvalue(r,'dm_p') for r in rows])
    doubled=holm([pvalue(r,'double_dm_p') for r in rows])
    for r,b in zip(rows,base):
        if not math.isclose(float(r['holm_p']),float(b),rel_tol=1e-13,abs_tol=1e-15):
            raise ValueError('stored Holm adjustment disagrees with retained inputs')
    def directions(adjusted):
        ids=dict(favorable=[],adverse=[],zero=[])
        for row,p in zip(rows,adjusted):
            difference=float(row['mean_difference'])
            if not math.isfinite(difference):raise ValueError('finite paired mean required')
            if p<.05:ids['favorable' if difference<0 else ('adverse' if difference>0 else 'zero')].append(row['contrast_id'])
        return {k:len(v) for k,v in ids.items()},ids
    bc,bi=directions(base);dc,di=directions(doubled)
    return dict(family_size=len(rows),base_below_05=int(sum(base<.05)),double_below_05=int(sum(doubled<.05)),base_direction_counts=bc,double_direction_counts=dc,base_direction_ids=bi,double_direction_ids=di,by_id={r['contrast_id']:dict(holm_p=float(b),double_holm_p=float(d)) for r,b,d in zip(rows,base,doubled)})
