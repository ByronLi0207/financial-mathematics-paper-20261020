"""Draw only display curves; exact Murphy classification lives in wp3 JSON."""
from pathlib import Path
import json,hashlib
import numpy as np


def plot_page(canvas,panels,source):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    name='V6Times';font=Path('/System/Library/Fonts/Supplemental/Times New Roman.ttf')
    if not font.is_file():raise ValueError('EXISTING_FONT_UNAVAILABLE')
    if name not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont(name,str(font)))
    title='FX: H6, W2880' if source=='fx_hourly' else 'Treasury bills: H6, W260'
    def text(x,y,s,size=9,align='left'):
        canvas.setFillGray(0);canvas.setFont(name,size)
        getattr(canvas,{'left':'drawString','right':'drawRightString','center':'drawCentredString'}[align])(x,y,str(s))
    text(300,431,title+' - fixed report combinations',12,'center')
    factor=1000000. if source=='fx_hourly' else 1.
    xmin=min(float(p['theta'][0])/factor for p in panels);xmax=max(float(p['theta'][-1])/factor for p in panels)
    if xmax==xmin:xmax=xmin+1.
    ymax=max(.0001,max(float(np.max(np.abs(p['difference']))) for p in panels))*1.08
    for j,p in enumerate(panels):
        col=j%2;row=j//2;left=52+col*295;right=281+col*295;bottom=267-row*190;top=382-row*190
        xx=lambda v:left+(v-xmin)/(xmax-xmin)*(right-left)
        yy=lambda v:bottom+(v+ymax)/(2*ymax)*(top-bottom)
        canvas.setStrokeGray(.85);canvas.setLineWidth(.4)
        for value in np.linspace(-ymax,ymax,5):
            canvas.line(left,yy(value),right,yy(value));text(left-5,yy(value)-2.5,f'{value:.3f}',7,'right')
        canvas.setStrokeGray(.3);canvas.setLineWidth(.6);canvas.rect(left,bottom,right-left,top-bottom,stroke=1,fill=0)
        canvas.setDash(3,2);canvas.line(left,yy(0),right,yy(0));canvas.setDash()
        for value in np.linspace(xmin,xmax,4):
            x=xx(value);canvas.line(x,bottom,x,bottom-3);text(x,bottom-13,f'{value:,.1f}',7,'center')
        text((left+right)/2,bottom-27,'Threshold (USD millions)',8,'center')
        leftname='Mean(F, QR)' if p['left_method']=='MEAN_F_QR' else 'Median(F, QR, KNN)'
        text((left+right)/2,top+13,leftname+' minus '+p['right_method'],9,'center')
        ids=np.unique(np.linspace(0,len(p['theta'])-1,min(360,len(p['theta']))).astype(int))
        path=canvas.beginPath();path.moveTo(xx(float(p['theta'][ids[0]])/factor),yy(float(p['difference'][ids[0]])))
        # A subsampled step display does not determine the all-breakpoint signs.
        for before,k in zip(ids[:-1],ids[1:]):
            path.lineTo(xx(float(p['theta'][k])/factor),yy(float(p['difference'][before])))
            path.lineTo(xx(float(p['theta'][k])/factor),yy(float(p['difference'][k])))
        canvas.setStrokeGray(.05);canvas.setLineWidth(1.1);canvas.drawPath(path)
        text((left+right)/2,bottom-40,p['ranking'].replace('_',' ').lower(),8,'center')
    text(300,44,'Difference in mean elementary quantile score; negative values favor the combination.',8,'center')
    text(300,31,'Classification uses all unique breakpoints with integer event signs; display curves are subsampled.',7.8,'center')
    text(300,18,'Matched constituents in the original-primary source/window context. Post-result / exploratory.',7.8,'center')
    canvas.showPage()


def main():
    from reportlab.pdfgen.canvas import Canvas
    from v6_worker import ROOT,PUBLIC,PRIVATE,sha,write_json_new,Guard
    guard=Guard();guard();report= json.loads((PUBLIC/'wp3-combinations.json').read_text())
    path=PRIVATE/'wp3-murphy-curves.npz'
    if sha(path)!=report['private_curve_artifact']['sha256']:raise ValueError('CURVE_HASH_CHANGED')
    rows={r['slot_id']:r for r in report['murphy']};panels={s:[] for s in ('fx_hourly','nyfed_weekly')}
    with np.load(path,allow_pickle=False) as archive:
        for j,slot in enumerate(report['curve_order']):
            row=rows[slot];panels[row['source']].append(dict(**row,theta=np.array(archive[f'curve{j}_theta']),difference=np.array(archive[f'curve{j}_difference'])))
    out=PUBLIC/'figures';out.mkdir(parents=True,exist_ok=True);files=[]
    for source,data in panels.items():
        if len(data)!=4:raise ValueError('FOUR_FIXED_PANELS_REQUIRED')
        target=out/f'wp3-murphy-{source}.pdf'
        if target.exists():raise FileExistsError('FIGURE_ALREADY_EXISTS')
        canvas=Canvas(str(target),pagesize=(600,450));canvas.setTitle('Fixed combinations: '+source);canvas.setAuthor('')
        plot_page(canvas,data,source);canvas.save();files.append(dict(path=str(target.relative_to(ROOT)),sha256=sha(target),bytes=target.stat().st_size))
    guard();write_json_new(PUBLIC/'wp3-figure-bindings.json',dict(status='COMPLETE',source='wp3-combinations.json',source_sha256=sha(PUBLIC/'wp3-combinations.json'),private_curve_sha256=sha(path),
        plot_semantics='Subsampled display only. All-breakpoint integer classification and integral identity are in source report.',files=files,resources=guard.summary()))
    print(json.dumps(dict(status='COMPLETE',figure_count=len(files),files=files)))
if __name__=='__main__':main()
