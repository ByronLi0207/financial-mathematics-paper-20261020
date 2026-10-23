"""Draw the complete fixed-report preference frontier, without financial fits."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

COLORS={'QR':'#345995','KNN':'#16817A','SCALED_KNN':'#6B4C9A',
        'frozen_F':'#A17424','frozen_S':'#C25538','frozen_K':'#3D7044',
        'AR1_REPLAY':'#B04479','I':'#6E7785'}
LABEL={'QR':'QR','KNN':'NN','SCALED_KNN':'Sc','frozen_F':'F',
       'frozen_S':'S','frozen_K':'K','AR1_REPLAY':'AR','I':'I'}


def draw(result,output):
    if output.exists():raise ValueError('OUTPUT_EXISTS')
    data=json.loads(result.read_text())
    cells=sorted({(g['source'],g['horizon'],g['window']) for g in data['groups']})
    groups={(g['sample'],g['source'],g['horizon'],g['window']):g for g in data['groups']}
    c=canvas.Canvas(str(output),pagesize=(850,760),invariant=1)
    c.setTitle('Fixed-report preference frontiers');c.setAuthor('')
    c.setFillColor(HexColor('#182638'));c.setFont('Helvetica-Bold',19)
    c.drawString(38,721,'Which fixed report minimizes a stipulated loss?')
    c.setFont('Helvetica',10)
    c.drawString(38,699,'64 fixed reports in eight matched cells; full and existing H+1 sparse-grid summaries.')
    c.drawString(38,684,'J(alpha) = alpha x mean positive overrun + (1-alpha) x mean unused allowance')
    panels=[(175,277,0.,1.,'Entire preference range'),(492,318,.70,1.,'High-shortfall-weight detail')]
    top=620;bottom=127
    for x,width,low,high,title in panels:
        c.setFont('Helvetica-Bold',11);c.drawString(x,655,title)
        ticks=([0,.25,.5,.75,1] if low==0 else [.7,.8,.9,.95,1])
        for tick in ticks:
            tx=x+width*(tick-low)/(high-low)
            c.setStrokeColor(HexColor('#E1E5EB'));c.setLineWidth(.6);c.line(tx,bottom,tx,top+8)
            c.setFillColor(HexColor('#46566B'));c.setFont('Helvetica',8)
            c.drawCentredString(tx,top+17,f'{tick:g}')
        tx=x+width*(.95-low)/(high-low)
        c.setStrokeColor(HexColor('#182638'));c.setDash(2,2);c.line(tx,bottom,tx,top+8);c.setDash()
    for index,(source,h,w) in enumerate(cells):
        y=top-61*index
        c.setFillColor(HexColor('#182638'));c.setFont('Helvetica-Bold',11)
        c.drawString(38,y-5,'FX' if source=='fx_hourly' else 'Treasury')
        c.setFont('Helvetica',9);c.drawString(38,y-19,f'H{h} / W{w}')
        for sample,dy in [('full',0),('sparse',21)]:
            group=groups[(sample,source,h,w)]
            c.setFillColor(HexColor('#46566B'));c.setFont('Helvetica',8)
            c.drawRightString(164,y-dy-8,'Full' if sample=='full' else 'Sparse')
            for x,width,low,high,_ in panels:
                for region in group['frontier']['regions']:
                    left=max(low,float(Fraction(region['left'])));right=min(high,float(Fraction(region['right'])))
                    if right<=left:continue
                    x1=x+width*(left-low)/(high-low);x2=x+width*(right-low)/(high-low)
                    methods=region['methods'];height=15/len(methods)
                    for k,method in enumerate(methods):
                        c.setFillColor(HexColor(COLORS[method]));c.rect(x1,y-dy-15+k*height,x2-x1,height,fill=1,stroke=0)
                    label='='.join(LABEL[m] for m in methods)
                    if x2-x1>max(17,len(label)*5+5):
                        c.setFillColor(HexColor('#FFFFFF'));c.setFont('Helvetica-Bold',8)
                        c.drawCentredString((x1+x2)/2,y-dy-11,label)
        c.setStrokeColor(HexColor('#EDF0F4'));c.line(38,y-44,810,y-44)
    for i,method in enumerate(COLORS):
        x=38+i*96;c.setFillColor(HexColor(COLORS[method]));c.rect(x,90,11,11,fill=1,stroke=0)
        c.setFillColor(HexColor('#182638'));c.setFont('Helvetica',8)
        c.drawString(x+15,93,method.replace('frozen_','').replace('AR1_REPLAY','AR').replace('SCALED_KNN','Scaled NN'))
    c.setFont('Helvetica',9);c.setFillColor(HexColor('#46566B'))
    for y,text in [(66,'Dashed line: original alpha=.95 (19:1). Unlabeled thin segments and all boundary ties are retained in results.json.'),
                   (51,'Fixed .95 reports are not refitted for other preferences. Alpha=0/1 are limiting single-component objectives.'),
                   (36,'Inspected-sample descriptive sensitivity; no observed financing costs, independent grid or deployment selector.')]:
        c.drawString(38,y,text)
    c.showPage();c.save()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--result',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();draw(a.result,a.output)
