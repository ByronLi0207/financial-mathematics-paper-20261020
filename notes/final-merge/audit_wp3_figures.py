"""Separate saved-source and artist readback, without importing the plotter."""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import argparse

ROOT=Path(__file__).resolve().parents[2]


def audit(folder):
    def read(path):return json.loads(Path(path).read_text())
    def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    points=read(folder/'points.json');receipt=read(folder/'render-receipt.json')
    old=read(ROOT/'results/revision-v9/wp4/render-v5/points.json')
    cftc=read(ROOT/'results/final-merge/wp2-cftc-mechanism/summary.json')['comparisons']
    failures=[];checks=0
    def need(value,label):
        nonlocal checks
        checks+=1
        if not value:failures.append(label)
    need(len(points)==482 and len({p['point_id'] for p in points})==482,'complete unique482 point census')
    index={p['point_id']:p for p in points}
    for p in old:
        q=index[p['point_id']]
        need(all(q[k]==v for k,v in p.items()),p['point_id']+' every inherited field')
    caches={};hashes={}
    for p in points:
        name=p['source_file']
        if name not in caches:caches[name]=read(ROOT/name);hashes[name]=sha(ROOT/name)
        need(p['source_sha256']==hashes[name],p['point_id']+' source SHA')
        row=caches[name]['comparisons'][p['source_index']] if p['family']=='cftc' else caches[name][p['source_index']]
        y=row[p['source_y_field']]
        need(y==p['relative_loss_percent'] and math.isfinite(y),p['point_id']+' exact source ordinate')
        c=Fraction(row['window'],row['horizon']+1)
        need(c==Fraction(p['c_fraction']) and float(c)==p['c'],p['point_id']+' exact history coordinate')
        need(p['method']==row['method'] and p['window']==row['window'] and p['horizon']==row['horizon'],p['point_id']+' method/window/horizon')
        if p['family']=='cftc':
            need(p['code']==row['code'] and p['status']=='COMPLETE',p['point_id']+' CFTC code/status')
            need(p['provenance_phase']==('NEW_W520' if p['window']==520 else 'ARCHIVED_W52_W260'),p['point_id']+' known versus new provenance')
    need({p['source_index'] for p in points if p['family']=='cftc'}==set(range(102)),'all102 CFTC rows, including adverse')
    need(Counter(p['method'] for p in points)=={'QR33':241,'QR4':241},'method census')
    offsets=0;artist_count=0
    for panel in receipt['panels']:
        expected={p['point_id'] for p in points if p['method']==panel['method']}
        need(set(panel['point_ids'])==expected and len(panel['point_ids'])==241,'panel full provenance census')
        seen=[]
        xl,yl=panel['xlim'],panel['ylim']
        if panel['full_range']:
            need(all(xl[0]<=index[i]['c']<=xl[1] and yl[0]<=index[i]['relative_loss_percent']<=yl[1] for i in expected),'full-range shows every point')
        for artist in panel['artists']:
            artist_count+=1
            need(len(artist['point_ids'])==len(artist['actual_offsets']),'artist identity/offset count')
            if artist['category']=='CFTC':need(artist['marker']=='p','CFTC distinct pentagon marker')
            if artist['kind']=='line':
                windows=[index[i]['window'] for i in artist['point_ids']]
                need(all(a<b for a,b in zip(windows,windows[1:])),'true W order in FX curve')
            for id,xy in zip(artist['point_ids'],artist['actual_offsets']):
                seen.append(id);offsets+=1;p=index[id]
                need(xy==[p['c'],p['relative_loss_percent']],id+' actual unjittered/unrounded offset')
        need(Counter(seen)==Counter({i:1 for i in expected}),'each point once in each repeated panel')
    need(len(receipt['panels'])==4 and sum(p['full_range'] for p in receipt['panels'])==2,'two full and two labelled detail panels')
    need('independent dealer source' in receipt['legend']['CFTC'].replace('\n',' '),'requested CFTC legend text')
    roots=read(ROOT/receipt['band_source'])
    need(sha(ROOT/receipt['band_source'])==receipt['band_sha256'],'original threshold source SHA')
    for method in ('QR33','QR4'):
        need(receipt['bands'][method]==roots['methods'][method]['intervals']['all_draw_envelope'],'unchanged fixed-grid envelope '+method)
    with (folder/'points.csv').open(newline='') as stream:rows=list(csv.DictReader(stream))
    need(len(rows)==482,'CSV census')
    for p,row in zip(points,rows):
        need(all(row[k]==('' if p.get(k) is None else str(p[k])) for k in row),'CSV/JSON exact field mapping')
    decision=read(folder/'decision-bindings.json')
    cost_scope=decision['cost_scope'];cost=read(ROOT/cost_scope['source'])['groups'][5]
    need(cost['primary']==cost_scope['primary']=='CFTC::QR33','cost range applies to full CFTC regression')
    need(cost['c']==cost_scope['fixed_exceedance_charge']==1,'exceedance charge fixed for the displayed cost range')
    formula=read(ROOT/cost_scope['original_design'])['design']['formula']
    need(formula==cost_scope['original_formula']=='kappa*mean(C-B)/mF + beta*mean(Y>C) + c*mean(max(Y-C,0))/mF','original coefficient-to-cost-term mapping')
    need(cost_scope['fixed_coefficient']=='c' and cost_scope['varied_coefficients']==['kappa','beta'],'varied reserve/breach, fixed exceedance coefficient roles')
    need('full CFTC regression' in next(b['text'] for b in decision['boxes'] if b['id']=='cost'),'cost model named in visible box')
    need('Exceedance charge is fixed' in next(b['text'] for b in decision['boxes'] if b['id']=='cost'),'correct cost coefficient role visible in the diagram')
    numeric=[]
    for b in decision['numbers']:
        path=ROOT/b['source'];raw=read(path)
        for part in b['pointer'].split('/')[1:]:raw=raw[int(part)] if isinstance(raw,list) else raw[part]
        need(raw==b['raw_value'] and sha(path)==b['sha256'],b['id']+' exact raw field/SHA')
        need(format(raw*b['scale'],b['format'])==b['display'],b['id']+' declared display conversion')
        numeric.append(b['display'])
    # The diagram's PDF text must contain exactly the bound numeric inventory.
    from pypdf import PdfReader
    pdf=PdfReader(folder/'decision-map.pdf');text='\n'.join(p.extract_text() for p in pdf.pages)
    need(len(pdf.pages)==1,'decision PDF one page')
    need(Counter(re.findall(r'\d+(?:\.\d+)?',text))==Counter(numeric),'PDF exact12 numeric tokens and multiplicities')
    for box in decision['boxes']:
        need(' '.join(box['text'].split()) in ' '.join(text.split()),box['id']+' actual PDF text')
    for file,digest in receipt['output_sha256'].items():need(sha(folder/file)==digest,'render artifact SHA '+file)
    result=dict(status='PASS' if not failures else 'MISMATCH',checked_utc=datetime.now(timezone.utc).isoformat(),
        checks=checks,mismatches=len(failures),failures=failures,points=482,inherited_points=380,cftc_points=102,
        actual_artist_offsets=offsets,artists=artist_count,diagram_numeric_bindings=len(numeric),
        new_model_fits=0,new_statistics=0,pixel_appearance='Requires separate actual visual inspection',
        scope='Independent source/pointer/CSV/actual artist/PDF text readback by the sole executor; no plotter import or new statistical result')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--render',type=Path,default=ROOT/'results/final-merge/wp3-figures');p.add_argument('--output',type=Path,default=ROOT/'notes/final-merge/wp3-figure-audit.json');a=p.parse_args();r=audit(a.render)
    with a.output.open('x') as stream:json.dump(r,stream,indent=2);stream.write('\n')
    print(json.dumps(r,indent=2));raise SystemExit(r['mismatches']!=0)
