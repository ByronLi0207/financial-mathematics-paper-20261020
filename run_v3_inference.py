"""Execute the authorized post-result inference stages, in order, on B5 traces."""
import sys
sys.dont_write_bytecode=True
import os
for _n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[_n]='1'
import argparse,csv,json,math,time,resource
from pathlib import Path
import numpy as np
from inference_tests import dm_test,coverage_tests,dq_hac,holm,murphy
from v3_revision import ROOT,RESULT,dump,write,update_ledger
from run_study import RunGuard

OUT=RESULT/'inference'
ATTEMPT=ROOT/'.scratch/revision-20261022/replication-revision-v3-b5-full'
def rows(path):return list(csv.DictReader(path.open()))
def output(name,data):
    import io
    f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data);write(OUT/name,f.getvalue())
def traces():
    audit=json.loads((ATTEMPT/'numerical-audit/public/reproduction-comparison.json').read_text())
    assert audit['status']=='NUMERICAL_AUDIT_VERIFIED' and audit['exact_csv_byte_agreement']
    allv={}
    q=json.loads((ATTEMPT/'evaluation-queue.json').read_text())
    for cell in q['cells']:
        p=(ROOT/cell['receipt_path']).parent.parent/'private/numeric-traces.npz'
        with np.load(p,allow_pickle=False) as z:
            for name in z.files:
                if not name.endswith('_origins'):continue
                method=name[:-8]
                allv[cell['source'],cell['horizon'],cell['window'],method]={k:z[method+'_'+k].copy() for k in ('origins','capacity','peak','floor','pinball')}
    return allv
def item(allv,row,side):return allv[row['source'],int(row['horizon']),int(row[side+'_window']),row[side+'_method']]
def main(stage):
    OUT.mkdir(parents=True,exist_ok=True)
    for prior in {'B1':[],'B3':['B1'],'B2':['B1','B3'],'B4':['B1','B3','B2']}[stage]:
        assert (OUT/(prior+'-complete.json')).exists(),prior+' must complete first'
    started=time.monotonic();private=ROOT/'.scratch/v3-inference'/stage
    private.mkdir(parents=True,exist_ok=False)
    from datetime import datetime,timezone
    guard=RunGuard(started,datetime.now(timezone.utc).isoformat(),private,OUT,private)
    allv=traces();guard.arrays(allv);guard(stage=stage+'_start')
    comparisons=rows(ROOT/'results/revision-20261022/paired-comparisons.csv')
    if stage=='B1':
        data=[]
        for row in comparisons:
            if row['contrast_category']=='update_frequency':continue
            a=item(allv,row,'left');b=item(allv,row,'right');assert np.array_equal(a['origins'],b['origins'])
            diff=a['pinball']-b['pinball'];h=int(row['horizon']);z=dm_test(diff,h)
            assert z['mean_difference']==float(row['mean_pinball_difference'])
            z2=dm_test(diff,h,min(len(diff)-1,2*z['bandwidth']))
            data.append(dict(contrast_id=row['contrast_id'],source=row['source'],horizon=h,left_window=row['left_window'],left_method=row['left_method'],right_window=row['right_window'],right_method=row['right_method'],category=row['contrast_category'],primary=row['declared_source_primary'],legacy=row['h24_legacy_contrast'])|z|dict(double_bandwidth=z2['bandwidth'],double_dm_t=z2['dm_t'],double_dm_p=z2['dm_p'],double_hln_p=z2['hln_p']))
            guard(stage='dm_cell')
        assert len(data)==74
        output('dm.csv',data)
        update_ledger('B1','COMPLETE: inference_tests.py and run_v3_inference.py generate74 independent contrast identities (72 common-history F/S/K plus2 original FX comparisons); the required24 conditional-vs-F rows and two additional FX cases are in inference/dm.csv. Report Bartlett NW DM t/normal p, HLN t/Student p, bandwidth and doubled-bandwidth sensitivity. Degenerate identical losses have NA t/p. All tests are post-result/exploratory; fixed-window CPA assumptions and the approximate pinball use of HLN are explicit in inference-design.md. Nine independent known-answer tests passed using existing unittest; no dependency installed.')
    elif stage=='B3':
        data=[]
        for (s,h,w,m),a in allv.items():
            hits=(a['peak']>a['capacity']).astype(int);grid=np.arange(0,len(hits),h+1)
            z=coverage_tests(hits[grid]);dq=dq_hac(hits,a['capacity'],h)
            data.append(dict(source=s,horizon=h,window=w,method=m,grid_stride=h+1,first_origin=int(a['origins'][0]))|z|{'dq_'+k:v for k,v in dq.items()})
            guard(stage='coverage_cell')
        assert len(data)==90
        output('coverage.csv',data)
        update_ledger('B3','COMPLETE: inference/coverage.csv covers every90 retained report cell. Kupiec POF, Christoffersen transition independence and full-n-POF-plus-independence CC use the original H+1 grids (947/265 FX;40/12 Treasury). DQ-type full-sample HAC Wald uses matured lagged hits H+1..H+4 and known issued capacity. Missing transition rows or singular moment covariance produce NA plus reasons. Boundary/sparse-reference caveats, target atoms, shared training and post-result status are explicit. The supplementary e-values remain in Appendix D.')
    elif stage=='B2':
        data=[r for r in rows(OUT/'dm.csv') if r['category']=='common_history'];assert len(data)==72
        p=[float(r['dm_p']) if r['status']=='OK' else (1. if r['status']=='IDENTICAL_LOSSES' else None) for r in data]
        if any(x is None for x in p):raise ValueError('Unidentified non-identical test prevents complete Holm family')
        adj=holm(p)
        for r,pp,z in zip(data,p,adj):r.update(holm_family_size=72,holm_input_p=pp,holm_p=float(z),holm_note='conservative p1 for identical forecasts' if r['status']=='IDENTICAL_LOSSES' else 'normal-reference DM p')
        output('holm.csv',data)
        update_ledger('B2','COMPLETE: inference/holm.csv adjusts the entire fixed72 common-history F/S/K family, without shrinking the family or including duplicate Treasury-primary identities. Two full-pool KNN/F identities retain NA statistics and use conservative p1 solely for multiplicity bookkeeping. Original FX cross-window primary and legacy are outside this72-member family. No favorable comparison is selected.')
    elif stage=='B4':
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        primary=[r for r in comparisons if r['declared_source_primary']=='True'];assert len(primary)==2
        summaries=[]
        for row in primary:
            a=item(allv,row,'left');b=item(allv,row,'right');z=murphy(a['capacity'],b['capacity'],a['peak'])
            expected=float(row['mean_pinball_difference']);err=abs(z['integral_difference']-expected)
            assert err<1e-9*max(1,abs(expected)),('Murphy integral mismatch',err)
            # All breakpoints are checked privately; publish 201 aggregate grid scores.
            grid=np.linspace(z['theta'][0],z['theta'][-1],201);idx=np.searchsorted(z['theta'],grid,side='right')-1
            plotrows=[dict(theta_USD_millions=float(t/(1e6 if row['source']=='fx_hourly' else 1)),left_elementary=float(z['left'][i]),right_elementary=float(z['right'][i])) for t,i in zip(grid,idx)]
            output('murphy-'+row['source']+'-display.csv',plotrows)
            pdf=OUT/('murphy-'+row['source']+'.pdf')
            import io
            buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(510,260),invariant=1)
            c.setFont('Helvetica',10);c.drawString(42,240,('FX' if row['source']=='fx_hourly' else 'Treasury')+' primary: fixed tau = 0.95 elementary quantile scores')
            x0,y0,xw,yh=48,45,442,166;xmin=grid[0];xmax=grid[-1];ymax=max(float(z['left'].max()),float(z['right'].max()))*1.05
            c.setStrokeColor(colors.black);c.line(x0,y0,x0+xw,y0);c.line(x0,y0,x0,y0+yh)
            for key,color in [('left',colors.HexColor('#bd392f')),('right',colors.HexColor('#17609a'))]:
                yy=z[key][idx];path=c.beginPath()
                for j,(xx,v) in enumerate(zip(grid,yy)):
                    x=x0+(xx-xmin)/(xmax-xmin)*xw;y=y0+float(v)/ymax*yh
                    (path.moveTo if j==0 else path.lineTo)(x,y)
                c.setStrokeColor(color);c.setLineWidth(1.1);c.drawPath(path)
            c.setFillColor(colors.black);c.setFont('Helvetica',8)
            for f in [0,.25,.5,.75,1]:
                c.drawRightString(x0-5,y0+f*yh-3,f'{f*ymax:.3f}')
                c.drawCentredString(x0+f*xw,y0-13,f'{(xmin+f*(xmax-xmin))/(1e6 if row["source"]=="fx_hourly" else 1):.1f}')
            c.drawCentredString(270,13,'Threshold theta (source-specific USD millions); vertical axis dimensionless mean score')
            c.setFillColor(colors.HexColor('#bd392f'));c.drawString(53,221,'QR');c.setFillColor(colors.HexColor('#17609a'));c.drawString(93,221,row['right_method'])
            c.showPage();c.save()
            from build_revision_v3 import save_bytes
            save_bytes(pdf,buf.getvalue())
            summaries.append(dict(contrast_id=row['contrast_id'],source=row['source'],tau=.95,breakpoint_count=len(z['theta']),ranking=z['ranking'],arithmetic_tolerance=z['arithmetic_tolerance'],min_elementary_difference=float(z['difference'].min()),max_elementary_difference=float(z['difference'].max()),integral_difference=z['integral_difference'],archived_pinball_difference=expected,absolute_integral_error=err,display_grid_points=201))
            guard(stage='murphy_primary')
        output('murphy-summary.csv',summaries)
        update_ledger('B4','COMPLETE: two primary Murphy diagrams and201-point display CSVs are in inference/. Ranking is checked on every unique prediction/outcome breakpoint privately, not just the displayed grid; the integral reproduces the archived paired pinball loss. Raw breakpoints are not republished. Both sample rankings, including crossings, are retained in murphy-summary.csv. Fixed-tau score-class comparison is separated from archived varying-weight preference frontiers. Finite-record dominance is not population dominance or calibration.')
    guard(stage=stage+'_complete');dump(OUT/(stage+'-complete.json'),dict(stage=stage,status='COMPLETE',post_result=True,resources=guard.resources))
    print(json.dumps(dict(stage=stage,status='COMPLETE',resources=guard.resources)))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['B1','B3','B2','B4'],required=True);main(p.parse_args().stage)
