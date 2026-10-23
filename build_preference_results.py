"""Reweight fixed public reports; no observations, model fitting or tuning.

All rational results refer to the archived decimal summary fields. They do
not claim exact underlying sample arithmetic or a new quantile forecast.
"""
from __future__ import annotations
import argparse
import csv
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

from preference_frontier import LossComponents, compare_records, lower_envelope, mean_loss

ROOT=Path(__file__).resolve().parent
FREEZE=ROOT/'protocol/revision-20261022/preference-robustness-freeze.json'
BASE='results/revision-20261022/'
CORE={'QR','KNN','SCALED_KNN','frozen_F','frozen_S','frozen_K'}
METHODS=CORE|{'AR1_REPLAY','I'}
FILES=(('full',BASE+'evaluation-summary.csv',CORE),
       ('full',BASE+'ar1-replay/ar1-summary.csv',{'AR1_REPLAY'}),
       ('full',BASE+'rank-ablation/summary.csv',{'I'}),
       ('sparse',BASE+'evaluation-nonoverlap.csv',CORE),
       ('sparse',BASE+'ar1-replay/ar1-nonoverlap.csv',{'AR1_REPLAY'}),
       ('sparse',BASE+'rank-ablation/nonoverlap.csv',{'I'}))


def read_rows(path, methods, *, sparse=False):
    rows=[];seen=set()
    with Path(path).open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['method'] not in methods:continue
            source=row['source'];h=int(row['horizon']);w=int(row['window'])
            allowed={'fx_hourly':('USD',(720,2880),6625,{6:947,24:265}),
                     'nyfed_weekly':('USD millions',(52,260),277,{6:40,24:12})}
            if source not in allowed or h not in (6,24):raise ValueError('CELL_IDENTITY')
            unit,windows,n,grid=allowed[source]
            if w not in windows or row['native_unit']!=unit:raise ValueError('CELL_IDENTITY')
            if int(row['origin_count'])!=(grid[h] if sparse else n):raise ValueError('ORIGIN_COUNT')
            if row.get('status','COMPLETE')!='COMPLETE':raise ValueError('INCOMPLETE')
            c=LossComponents.from_tokens(row['mean_positive_overrun'],row['mean_unused_allowance'])
            stored=float(row['mean_pinball']);computed=float(mean_loss(c,Fraction(19,20)))
            if not math.isfinite(stored) or not math.isclose(stored,computed,rel_tol=1e-12,abs_tol=1e-9):
                raise ValueError('SCORE_IDENTITY')
            if not 0<=int(row['strict_breach_count'])<=int(row['origin_count']):raise ValueError('BREACH_COUNT')
            key=(source,h,w,row['method'])
            if key in seen:raise ValueError('DUPLICATE_CELL_METHOD')
            seen.add(key);rows.append(row)
    return rows


def record(row):
    return {'u_token':row['mean_positive_overrun'],
            'v_token':row['mean_unused_allowance'],
            'mean_pinball':row['mean_pinball'],
            'strict_breach_count':int(row['strict_breach_count'])}


def components(value):return LossComponents.from_tokens(value['u_token'],value['v_token'])


def rational_token(value):return f'{value.numerator}/{value.denominator}'


def comparison(left,right):
    c=compare_records(components(left),components(right))
    return {'relation':c.relation,'equality_alpha':None if c.equality_alpha is None else rational_token(c.equality_alpha)}


def group_result(key,rows):
    sample,source,h,w=key
    by_method={row['method']:record(row) for row in rows}
    if len(rows)!=8 or set(by_method)!=METHODS:raise ValueError('METHOD_INVENTORY')
    inputs={name:components(value) for name,value in by_method.items()}
    frontier=lower_envelope(inputs)
    pairs=[];dominated=set()
    for left,right in itertools.combinations(sorted(inputs),2):
        c=comparison(by_method[left],by_method[right])
        pairs.append({'left':left,'right':right,**c})
        if c['relation']=='left_dominates':dominated.add(right)
        if c['relation']=='right_dominates':dominated.add(left)
    at_095={name:mean_loss(value,Fraction(19,20)) for name,value in inputs.items()}
    best=min(at_095.values())
    return {'sample':sample,'source':source,'horizon':h,'window':w,
            'native_unit':rows[0]['native_unit'],'origin_count':int(rows[0]['origin_count']),
            'methods':by_method,
            'frontier':{'regions':[{'left':rational_token(r.left),'right':rational_token(r.right),'methods':list(r.methods)} for r in frontier.regions],
                        'points':[{'alpha':rational_token(p.alpha),'methods':list(p.methods)} for p in frontier.points]},
            'pairs':pairs,'dominated_methods':sorted(dominated),
            'winners_at_095':sorted(name for name,val in at_095.items() if val==best)}


def verify_freeze(root=ROOT):
    freeze=json.loads((root/FREEZE.relative_to(ROOT)).read_text())
    for entry in freeze['input_files']+freeze['implementation_files']+[freeze['design_file']]:
        raw=(root/entry['path']).read_bytes()
        if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:
            raise ValueError('FROZEN_FILE_IDENTITY: '+entry['path'])
    if {e['path'] for e in freeze['input_files']}!={path for _,path,_ in FILES}:
        raise ValueError('FROZEN_INPUT_INVENTORY')
    return freeze


def build_results(root=ROOT):
    verify_freeze(root)
    groups={}
    for sample,path,methods in FILES:
        for row in read_rows(root/path,methods,sparse=sample=='sparse'):
            key=(sample,row['source'],int(row['horizon']),int(row['window']))
            groups.setdefault(key,[]).append(row)
    expected={(sample,src,h,w) for sample in ('full','sparse')
              for src,windows in [('fx_hourly',(720,2880)),('nyfed_weekly',(52,260))]
              for h in (6,24) for w in windows}
    if set(groups)!=expected:raise ValueError('GROUP_INVENTORY')
    complete=[group_result(key,groups[key]) for key in sorted(groups)]
    original=read_rows(root/(BASE+'evaluation-summary.csv'),CORE|{'rolling_F','rolling_S'})
    indexed={(r['source'],int(r['horizon']),int(r['window']),r['method']):r for r in original}
    headlines=[]
    for name,src,h,lw,lm,rw,rm in [
            ('fx_h6_primary','fx_hourly',6,2880,'QR',720,'rolling_F'),
            ('fx_h6_matched','fx_hourly',6,2880,'QR',2880,'frozen_F'),
            ('fx_h24_legacy','fx_hourly',24,2880,'QR',720,'rolling_S'),
            ('treasury_h6_primary','nyfed_weekly',6,260,'QR',260,'frozen_F')]:
        left=record(indexed[(src,h,lw,lm)]);right=record(indexed[(src,h,rw,rm)])
        headlines.append({'id':name,'source':src,'horizon':h,
                          'left_method':lm,'left_window':lw,'right_method':rm,'right_window':rw,
                          'left':left,'right':right,**comparison(left,right)})
    verify_freeze(root)
    return {'schema_version':1,'status':'FIXED_REPORT_PREFERENCE_ANALYSIS',
            'scope':'Exact rational functions of saved decimal means; inspected sample; no new fits or operational costs.',
            'groups':complete,'headline_comparisons':headlines}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='New directory; existing paths are never overwritten')
    args=parser.parse_args()
    if args.output.exists():raise ValueError('OUTPUT_EXISTS')
    result=build_results()
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'groups':len(result['groups']),
                      'reports':sum(len(g['methods']) for g in result['groups']),
                      'pairs':sum(len(g['pairs']) for g in result['groups'])}))


if __name__=='__main__':main()
