"""Build the single v5 motivating-window vector figure from its frozen receipt.

The importing and layout functions never author a PDF. The caller must perform
the task's PDF-operation marker before invoking this script's main entry point.
No source selection, forecasting, fitting, fetching or archive edit occurs here.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'results/revision-20261023/v5-novelty/motivating-window-final.json'
SOURCE_SHA256='61a41d6d324499994d247cd527261d938d506d26bed03a6a4c804e25edf37812'
DEFAULT_OUTPUT=ROOT/'submission-jof/figures/endpoint-peak-example.pdf'
DEFAULT_RECEIPT=ROOT/'notes/revision-v5-novelty/figure-binding.json'
MONTHS=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')


def load_figure_data():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:
        raise ValueError('frozen motivating-window receipt hash differs')
    receipt=json.loads(raw);e=receipt['example']
    if (receipt['status']!='COMPLETE' or receipt['source_series_key']!='PDPOSGS-B'
            or receipt['native_unit']!='USD millions' or receipt['method']!='clean frozen F'):
        raise ValueError('illustration source or method identity differs')
    values=list(map(float,e['absolute_positions']))
    dates=[datetime.fromisoformat(s) for s in e['dates']]
    if len(values)!=e['horizon']+1 or len(dates)!=len(values):
        raise ValueError('illustration path count differs')
    if any(b<=a for a,b in zip(dates,dates[1:])):
        raise ValueError('illustration economic dates are not increasing')
    if not all(math.isfinite(v) and v>=0 for v in values):
        raise ValueError('invalid absolute position')
    if values!=[abs(float(v)) for v in e['positions']]:
        raise ValueError('absolute path disagrees with signed source path')
    data=dict(positions=values,date_labels=[f'{d.day:02d} {MONTHS[d.month-1]}' for d in dates],
        iso_dates=[d.date().isoformat() for d in dates],year_label=str(dates[0].year),
        report=float(e['report']),floor=float(e['floor']),peak=float(e['peak']),endpoint=float(e['endpoint_absolute']))
    figure_layout(data)  # validate the semantic identities, not just the hash
    bindings=[dict(plotted_variable=f'absolute_path[{i}]',source_pointer=f'/example/absolute_positions/{i}',
                   value=v) for i,v in enumerate(values)]
    bindings += [dict(plotted_variable=name,source_pointer='/example/'+pointer,value=data[name])
                 for name,pointer in (('report','report'),('floor','floor'),('peak','peak'),('endpoint','endpoint_absolute'))]
    binding=dict(source=str(SOURCE.relative_to(ROOT)),source_sha256=SOURCE_SHA256,
        source_raw_sha256=receipt['identity']['raw_source_sha256'],source_series_key=receipt['source_series_key'],
        native_unit=receipt['native_unit'],analysis_status=receipt['analysis_status'],
        date_binding=dict(source_pointer='/example/dates',economic_dates=e['dates'],display_labels=data['date_labels'],
                          meaning=e['dates_are']),
        scientific_bindings=bindings,selection_rule=e['selection_rule'],
        limitation=receipt['limitation'])
    return data,binding


def figure_layout(data):
    values=list(data['positions'])
    if not values or max(values)!=data['peak']:
        raise ValueError('sampled peak differs from plotted path')
    if (values[0]!=data['floor'] or values[-1]!=data['endpoint']
            or not data['endpoint']<=data['report']<data['peak']
            or data['floor']>data['report']):
        raise ValueError('endpoint, floor or report relation differs')
    lo=min(values+[data['floor'],data['report']]);hi=max(values+[data['report']])
    span=max(1.,hi-lo);rough=span/4;power=10**math.floor(math.log10(rough))
    step=min(v*power for v in (1,2,5,10) if v*power>=rough)
    lower=math.floor(lo/step)*step;upper=math.ceil(hi/step)*step
    if lower==upper:upper+=step
    left,right,bottom,top=54.,446.,53.,198.
    y=lambda v:bottom+(v-lower)/(upper-lower)*(top-bottom)
    points=[[left+i*(right-left)/(len(values)-1),y(v)] for i,v in enumerate(values)]
    ticks=[lower+i*step for i in range(round((upper-lower)/step)+1)]
    return dict(page_size=[467,240],plot_left=left,plot_right=right,plot_bottom=bottom,plot_top=top,
        y_lower=lower,y_upper=upper,y_step=step,y_ticks=ticks,
        tick_coordinates=[y(v) for v in ticks],point_coordinates=points,
        report_y=y(data['report']),floor_y=y(data['floor']),peak_index=values.index(data['peak']))


def _render(canvas,data,layout):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font=Path('/System/Library/Fonts/Supplemental/Times New Roman.ttf')
    if not font.is_file():raise ValueError('existing publication font unavailable')
    name='V5FigureTimes'
    if name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(name,str(font)))
    def text(x,y,s,size=8,align='left',gray=0.):
        canvas.setFont(name,size);canvas.setFillGray(gray)
        getattr(canvas,{'left':'drawString','right':'drawRightString','center':'drawCentredString'}[align])(x,y,str(s))
    def line(x1,y1,x2,y2,width=1,gray=0,dash=()):
        canvas.setStrokeGray(gray);canvas.setLineWidth(width);canvas.setDash(dash)
        canvas.line(x1,y1,x2,y2);canvas.setDash()
    left,right=layout['plot_left'],layout['plot_right']
    bottom,top=layout['plot_bottom'],layout['plot_top']
    # Line styles carry the distinction in grayscale; all text is embedded.
    for x,label,dash,gray in ((54,'Absolute sampled position',(),0),
                               (231,'Issued clean F',(5,3),.2),
                               (354,'Known floor',(1,2),.5)):
        line(x,226,x+19,226,1.2,gray,dash);text(x+24,223,label,8)
    text(left,210,'NYFed Treasury bills: absolute net position (USD millions)',8.3)
    for value,y in zip(layout['y_ticks'],layout['tick_coordinates'],strict=True):
        line(left,y,right,y,.35,.88)
        text(left-6,y-2.5,f'{value:,.0f}',7.8,align='right',gray=.15)
        line(left-3,y,left,y,.6,.3)
    line(left,bottom,right,bottom,.7,.25)
    line(left,bottom,left,top,.7,.25)
    line(left,layout['report_y'],right,layout['report_y'],1,.2,(5,3))
    line(left,layout['floor_y'],right,layout['floor_y'],.9,.5,(1,2))
    points=layout['point_coordinates']
    path=canvas.beginPath();path.moveTo(*points[0])
    for point in points[1:]:path.lineTo(*point)
    canvas.setStrokeGray(0);canvas.setLineWidth(1.4);canvas.setDash();canvas.drawPath(path)
    for x,y in points:
        canvas.setFillGray(0);canvas.setStrokeGray(0);canvas.circle(x,y,2,stroke=1,fill=1)
    # Open endpoint square and peak triangle remain distinguishable in print.
    x,y=points[-1];canvas.setFillGray(1);canvas.rect(x-2.5,y-2.5,5,5,stroke=1,fill=1)
    px,py=points[layout['peak_index']]
    triangle=canvas.beginPath();triangle.moveTo(px,py+3.5);triangle.lineTo(px-3.1,py-2)
    triangle.lineTo(px+3.1,py-2);triangle.close()
    canvas.setFillGray(0);canvas.drawPath(triangle,stroke=1,fill=1)
    for (x,_),label in zip(points,data['date_labels'],strict=True):
        line(x,bottom,x,bottom-3,.6,.25);text(x,bottom-15,label,7.4,align='center')
    text(left+7,layout['report_y']-10,f'Issued F {data["report"]:,.0f}',8)
    text(left+7,layout['floor_y']+7,f'Known floor / start {data["floor"]:,.0f}',8)
    text(px,py+11,f'Peak {data["peak"]:,.0f}',8,align='center')
    text(right-3,points[-1][1]-13,f'Endpoint {data["endpoint"]:,.0f}',8,align='right')
    text((left+right)/2,16,f'Economic dates in the downloaded vintage, {data["year_label"]}',8,align='center')


def build_figure(output=DEFAULT_OUTPUT,receipt_path=DEFAULT_RECEIPT):
    output,receipt_path=Path(output),Path(receipt_path)
    if output.exists() or receipt_path.exists():raise FileExistsError('new figure and binding paths required')
    for path in (output,receipt_path):
        if not path.parent.is_dir() or any(p.is_symlink() for p in (path,*path.parents)):
            raise ValueError('output parent absent or symlinked')
    data,binding=load_figure_data();layout=figure_layout(data)
    from reportlab.pdfgen.canvas import Canvas
    with output.open('xb') as stream:
        canvas=Canvas(stream,pagesize=tuple(layout['page_size']),invariant=1,pageCompression=1)
        canvas.setTitle('Sampled peak exceeds an issued historical report while the endpoint remains inside')
        canvas.setAuthor('');canvas.setSubject('Deterministically selected public NYFed economic-date illustration')
        _render(canvas,data,layout);canvas.showPage();canvas.save()
    raw=output.read_bytes()
    binding.update(figure_path=str(output.relative_to(ROOT)),figure_sha256=hashlib.sha256(raw).hexdigest(),
        figure_bytes=len(raw),pages=1,vector_only=True,grayscale=True,page_size_points=layout['page_size'],
        render_layout=layout,generator_path=str(Path(__file__).relative_to(ROOT)),
        generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with receipt_path.open('x') as stream:json.dump(binding,stream,indent=2,allow_nan=False);stream.write('\n')
    return binding


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DEFAULT_OUTPUT)
    parser.add_argument('--receipt',type=Path,default=DEFAULT_RECEIPT)
    args=parser.parse_args(argv)
    binding=build_figure(args.output,args.receipt)
    print(json.dumps({k:binding[k] for k in ('figure_path','figure_sha256','figure_bytes','pages')},indent=2))


if __name__=='__main__':main()
