"""E5 port of the frozen panel alignment; no acquisition entry point.

The align_source function is copied unchanged from the earlier panel loader.
Only verified, already downloaded bytes are supplied by round2_panel_run.
"""
import csv,io,math
from datetime import date
import numpy as np


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
