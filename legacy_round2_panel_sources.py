"""Bounded official downloads and outcome-blind calendar eligibility."""
import csv,io,json,hashlib,urllib.request,urllib.error,math
from datetime import datetime,timezone,date
import numpy as np
from v3_revision import ROOT,RESULT,write_bytes,dump
OUT=RESULT/'round2/panel'

def align_source(raw,key,grid):
    text=raw.decode('utf-8-sig');reader=csv.DictReader(io.StringIO(text))
    if reader.fieldnames!=['As Of Date','Time Series','Value (millions)']:raise ValueError('unexpected CSV header')
    rows={}
    for r in reader:
        d=r['As Of Date'];date.fromisoformat(d)
        if d in rows:raise ValueError('duplicate economic date')
        if r['Time Series']!=key:raise ValueError('wrong series key')
        value=float(r['Value (millions)'])
        if not math.isfinite(value):raise ValueError('nonfinite source value')
        rows[d]=value
    missing=[d for d in grid if d not in rows]
    if missing:raise ValueError('missing required economic dates: '+str(len(missing)))
    x=np.array([rows[d] for d in grid]);return x,dict(raw_observations=len(rows),raw_first_date=min(rows),raw_last_date=max(rows),aligned_observations=len(grid),aligned_first_date=grid[0],aligned_last_date=grid[-1],missing_required_dates=0,spliced=False,imputed=False)

def fetch():
    protocol=json.loads((ROOT/'protocol/revision-20261023/round2-D3-panel.json').read_text());meta=json.loads((ROOT/'.scratch/round2/panel-metadata.json').read_text())['pd']['timeseries']
    grid=[r['As Of Date'] for r in csv.DictReader((ROOT/'data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv').open())];records=[]
    for candidate in protocol['candidate_series']:
        key=candidate['keyid'];url='https://markets.newyorkfed.org/api/pd/get/'+key+'.csv';record=dict(series_key=key,url=url,publisher='Federal Reserve Bank of New York',native_unit='USD millions',request_started_utc=datetime.now(timezone.utc).isoformat(),post_result=True,exploratory=True,metadata_records=[r for r in meta if r['keyid']==key],raw_redistribution='not included; acquisition code, URL and fingerprint supplied')
        try:
            with urllib.request.urlopen(url,timeout=45) as r:raw=r.read(1048577);record['http_status']=r.status
            if len(raw)>1048576:raise ValueError('response exceeds1MiB cap')
            record.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),downloaded_utc=datetime.now(timezone.utc).isoformat())
            destination=ROOT/'.scratch/round2/panel-data'/(key+'.csv');write_bytes(destination,raw);record['local_raw_path']=str(destination.relative_to(ROOT))
            _,facts=align_source(raw,key,grid);record.update(facts,status='ELIGIBLE')
        except Exception as e:
            record.update(status='SKIPPED',reason=type(e).__name__+': '+str(e),downloaded_utc=datetime.now(timezone.utc).isoformat())
        dump(OUT/'sources'/key/'provenance.json',record);records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='metadata_records'},ensure_ascii=False),flush=True)
    dump(OUT/'selection-manifest.json',dict(status='SELECTION_FROZEN_BEFORE_MODELS',completed_utc=datetime.now(timezone.utc).isoformat(),rule=protocol['selection_rule'],eligible=[r['series_key'] for r in records if r['status']=='ELIGIBLE'],skipped=[r for r in records if r['status']!='ELIGIBLE'],economic_grid_source='original immutable PDPOSGS-B dates',series=records,post_result=True,exploratory=True))
if __name__=='__main__':fetch()
