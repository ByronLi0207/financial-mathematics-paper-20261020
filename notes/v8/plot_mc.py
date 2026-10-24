"""Render the frozen runner's plot from completed summary only.

The numerical run's isolated uv environment lacks optional matplotlib. This
postprocessor uses a second uv environment with matplotlib, without changing
the frozen simulation code, its dependencies, outputs, or any random draw.
Presentation adjustments enforce the same W-axis range in all three panels,
show isolated oracle points, label failed cells, and use print-size typography.
"""
import sys
from pathlib import Path
import inspect
import json
import hashlib
import textwrap

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import v8_mc


if __name__=='__main__':
    out=ROOT/'results/v8/mc'
    plan=json.loads((out/'run-plan.json').read_text())
    for name,sha in plan['code_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
    rows=json.loads((out/'summary.json').read_text())
    assert len(rows)==24
    for name in ('mc-main.pdf','mc-main.png','plotting-receipt.json'):
        if (out/name).exists():
            backup=ROOT/'.scratch/v8/retained-backups'/(name+'.bak')
            assert backup.exists() and backup.read_bytes()==(out/name).read_bytes(),'Back up existing output as .bak before replacement'
    source=inspect.getsource(v8_mc.report)
    plotting='import matplotlib\n'+textwrap.dedent(source.split('    import matplotlib\n',1)[1])
    plotting=plotting.replace('figsize=(11,3.1)','figsize=(6.3,2.5)')
    plotting=plotting.replace("'k--',label='Oracle'","'k--.',label='Oracle'")
    plotting=plotting.replace("ax.set_xscale('log');", "ax.set_xscale('log');ax.set_xlim(min(WINDOWS)*.8,max(WINDOWS)*1.2);")
    plotting=plotting.replace('fig.tight_layout();',"for d,ax in zip(DGPS,axes):\n    count=sum(z['status']!='COMPLETE' for z in rows if z['dgp']==d)\n    if count:ax.text(.5,.86,f'{count} of 8 cells failed',ha='center',transform=ax.transAxes,fontsize=8)\nfig.tight_layout();")
    import matplotlib
    matplotlib.rcParams.update({'font.size':9,'axes.titlesize':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8})
    exec(compile(plotting,'<frozen v8_mc.report plotting>','exec'),dict(rows=rows,OUT=out,DGPS=v8_mc.DGPS,WINDOWS=v8_mc.WINDOWS,np=np))
    import importlib.metadata
    from datetime import datetime,timezone
    receipt=dict(created_utc=datetime.now(timezone.utc).isoformat(),
        source='Plotting portion of frozen v8_mc.report; presentation-only adjustments',
        presentation_changes=['Common W-axis limits','Visible isolated oracle points','Failed-cell counts','Print-size typography'],
        frozen_runner_sha256=plan['code_sha256']['v8_mc.py'],summary_sha256=v8_mc.digest(out/'summary.json'),
        matplotlib=importlib.metadata.version('matplotlib'),numpy=np.__version__,
        numerical_run_repeated=False,
        reason='Numerical uv environment lacks optional matplotlib; plotting only in a separate temporary uv environment')
    with (out/'plotting-receipt.json').open('w') as f:json.dump(receipt,f,indent=2);f.write('\n')
