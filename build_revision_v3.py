"""Typeset the v3 source and PDF with existing libraries; never fit forecasts.

The PDF uses ReportLab mathematical Unicode and vector figure overlays. The
separate formal TeX source is supplied for later compilation. Current source
bytes have not been compiled under the user's no-installation instruction.
"""
from pathlib import Path
from copy import deepcopy
import csv,html,io,json,re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether,Flowable
from reportlab.pdfgen import canvas
from pypdf import PdfReader,PdfWriter,Transformation
from build_tex import build_source,conv,esc
from v3_revision import ROOT,OUT,RESULT,write,dump,plain,write_bytes
from v3_math_format import prepare_tex_math,restore_tex_math

def fonts():
    for n,f in [('V3','Times New Roman.ttf'),('V3B','Times New Roman Bold.ttf'),('V3I','Times New Roman Italic.ttf'),('V3BI','Times New Roman Bold Italic.ttf'),('V3Math','Arial Unicode.ttf')]:
        pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
    pdfmetrics.registerFontFamily('V3',normal='V3',bold='V3B',italic='V3I',boldItalic='V3BI')

def safe(s):
    # Use actual scripts where Unicode phonetic glyph coverage is incomplete.
    subs=dict(zip('₀₁₂₃₄₅₆₇₈₉ₜᵢₕ₊ₘ','0123456789tih+m'))
    chars=''.join(subs)
    s=re.sub('['+chars+']+(?:,['+chars+']+)*',lambda m:'<sub>'+''.join(subs.get(x,x) for x in m[0])+'</sub>',s)
    sups={'ᵐ':'m','ᵗ':'t','ʳ':'r'}
    s=re.sub('[ᵐᵗʳ]+',lambda m:'<super>'+''.join(sups[x] for x in m[0])+'</super>',s)
    # ReportLab defaults shift scripts by 50% of the parent size, which
    # collided with adjacent13-point body lines. Use conventional smaller
    # scripts and explicit modest shifts; mathematical content is unchanged.
    s=s.replace('<sub>', '<sub rise="22%" size="72%">').replace('<super>', '<super rise="35%" size="72%">')
    # Font fallback is based on actual glyph coverage, not a lossy replacement.
    face=pdfmetrics.getFont('V3').face
    return re.sub(r'([^<>]+)(?=<|$)',lambda m:''.join(ch if ord(ch) in face.charToGlyph else '<font name="V3Math">'+ch+'</font>' for ch in m[0]),s)

def figures():
    directory=OUT/'figures';directory.mkdir(exist_ok=True)
    rows=list(csv.DictReader((ROOT/'results/revision-20261022/paired-comparisons.csv').open()))
    srcs=['fx_hourly','nyfed_weekly'];labels={'fx_hourly':'FX','nyfed_weekly':'Treasury'}
    def make(name,w,h,draw):
        b=io.BytesIO();c=canvas.Canvas(b,pagesize=(w,h),invariant=1);draw(c);c.showPage();c.save();p=directory/name
        if p.exists() and not (ROOT/'.git').exists():raise ValueError('invalid project')
        # Generated new files are backed up before an untracked overwrite.
        save_bytes(p,b.getvalue())
    def text(c,x,y,s,size=8):c.setFont('V3Math',size);c.setFillColor(colors.HexColor('#16324f'));c.drawString(x,y,str(s))
    def common(c):
        text(c,12,335,'Conditional loss relative to matched frozen F (%)',11)
        for col,source in enumerate(srcs):
            x=12+col*250;text(c,x,312,labels[source],10);text(c,x,294,'H / W / method',8);text(c,x+155,294,'Δ loss (%)',8)
            selected=[r for r in rows if r['source']==source and r['contrast_category']=='common_history' and r['right_method']=='frozen_F']
            for i,r in enumerate(selected):
                y=275-i*20;label=r['left_method'].replace('SCALED_KNN','Scaled KNN')
                text(c,x,y,r['horizon']+' / '+r['left_window']+' / '+label,7.7)
                v=float(r['relative_mean_loss_difference_percent']);text(c,x+168,y,f'{v:+.2f}',8)
            text(c,x,20,'All selected cells; lower loss favors the conditional report.',7)
    make('conditional-common-history.pdf',510,350,common)
    primary=[r for r in rows if r['declared_source_primary']=='True' or r['h24_legacy_contrast']=='True']
    order=['fx_hourly-h6-QR2880-minus-rolling_F720','fx_hourly-h24-QR2880-minus-rolling_S720','nyfed_weekly-h6-QR260-minus-frozen_F260'];primary=sorted(primary,key=lambda r:order.index(r['contrast_id']))
    def trade(c):
        text(c,12,218,'Declared comparisons: score and tail tradeoffs',11)
        names=['FX H6 primary','FX H24 legacy','Treasury H6 primary']
        for j,name in enumerate(names):text(c,158+j*112,193,name,8)
        for i,(field,title) in enumerate([('relative_mean_loss_difference_percent','Mean pinball loss change (%)'),('breaches','Breach-rate change (pp)'),('mean_positive_overrun_difference','Mean overrun difference'),('mean_unused_allowance_difference','Mean unused difference')]):
            y=164-i*34;text(c,12,y,title,8)
            for j,r in enumerate(primary):
                if field=='breaches':v=100*(int(r['strict_breach_count_left'])-int(r['strict_breach_count_right']))/int(r['origin_count'])
                else:v=float(r[field]);v=v/(1e6 if r['source']=='fx_hourly' and field!='relative_mean_loss_difference_percent' else 1)
                text(c,170+j*112,y,f'{v:+.3f}',9)
        text(c,12,15,'Overrun/unused differences: source-specific USD millions; source amounts stay separate.',7)
    make('conditional-primary-tradeoffs.pdf',510,235,trade)
    annual=list(csv.DictReader((ROOT/'results/revision-20261022/paired-annual.csv').open()))
    def years(c):
        text(c,12,238,'Every annual primary and legacy comparison',11)
        for col,ident in enumerate(order):
            x=12+col*168;text(c,x,215,['FX H6 primary','FX H24 legacy','Treasury H6 primary'][col],9)
            for j,r in enumerate(r for r in annual if r['contrast_id']==ident):
                text(c,x,192-j*24,r['calendar_year']+' (n='+r['origin_count']+')',7.8);text(c,x+87,192-j*24,f"{float(r['relative_mean_loss_difference_percent']):+.2f}%",8)
        text(c,12,15,'All years retained; the final issue-year groups are partial. These are within-record sensitivities.',7)
    make('conditional-annual-primary.pdf',510,255,years)
    for source in ('fx_hourly','nyfed_weekly'):
        p=RESULT/'inference'/('murphy-'+source+'.pdf')
        if not p.exists():continue
        # Keep every original path/tick drawing command. Replace exactly the
        # three text labels in a document copy; the result archive is untouched.
        from pypdf.generic import ContentStream
        reader=PdfReader(p);writer=PdfWriter();writer.add_page(reader.pages[0]);page=writer.pages[0]
        label='FX' if source=='fx_hourly' else 'Treasury'
        method='rolling_F' if source=='fx_hourly' else 'frozen_F'
        replacements={label+' primary: fixed tau = 0.95 elementary quantile scores',
          'Threshold theta (source-specific USD millions); vertical axis dimensionless mean score',method}
        stream=ContentStream(page.get_contents(),writer)
        retained=[];removed=[]
        for operands,operator in stream.operations:
            if operator==b'Tj' and str(operands[0]) in replacements:
                removed.append(str(operands[0]));continue
            retained.append((operands,operator))
        if set(removed)!=replacements or len(removed)!=3:raise ValueError('Murphy label scope changed')
        stream.operations=retained;page.replace_contents(stream)
        overlay=io.BytesIO();cv=canvas.Canvas(overlay,pagesize=(510,260),invariant=1)
        cv.setFont('V3Math',10);cv.drawString(42,240,label+' primary: fixed τ = 0.95 elementary quantile scores')
        cv.setFont('V3Math',8);cv.drawCentredString(270,13,'Threshold θ (source-specific USD millions); vertical axis dimensionless mean score')
        cv.setFillColor(colors.HexColor('#17609a'));cv.drawString(93,221,'Rolling F' if source=='fx_hourly' else 'Frozen F')
        cv.showPage();cv.save();page.merge_page(PdfReader(io.BytesIO(overlay.getvalue())).pages[0])
        out=io.BytesIO();writer.write(out)
        save_bytes(directory/p.name,out.getvalue())

def save_bytes(p,b):write_bytes(p,b)

class InlinePDF(Flowable):
    def __init__(self,path,placements,width=495):
        Flowable.__init__(self);self.path=path;self.placements=placements
        p=PdfReader(path).pages[0];self.sw=float(p.mediabox.width);self.sh=float(p.mediabox.height)
        self.width=width;self.height=width*self.sh/self.sw
    def draw(self):
        x,y=self.canv.absolutePosition(0,0);self.placements.append((self.canv.getPageNumber(),x,y,self.width,self.height,self.path))

def tex_source(content):
    c,math_bindings=prepare_tex_math(content)
    for s in c['sections']:s['blocks']=[b for b in s['blocks'] if b['type']!='figure']
    text=build_source(c)
    text=text.replace('\\usepackage{amsmath,amssymb,graphicx,booktabs,array}','\\usepackage{amsmath,amssymb,graphicx,booktabs,array,longtable}')
    # The existing converter supports formal equation TeX. Add numbered figures
    # close to their scientific discussions, rather than at document end only.
    for idx,title in [(0,'6. Results: FX'),(1,'7. Results: Treasury'),(2,'7. Results: Treasury'),(3,'8. Robustness'),(4,'8. Robustness')]:
        if idx>=len(c['figures']):continue
        marker='\\section*{'+title+'}'
        nextpos=text.find('\\section*{',text.find(marker)+len(marker))
        fig=c['figures'][idx]
        snippet='\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=0.98\\linewidth]{'+fig['path']+'}\n\\par\\smallskip\n{\\small\\raggedright '+esc(fig['caption'])+'\\par}\n\\end{figure}\n'
        text=text[:nextpos]+snippet+text[nextpos:]
    # Remove the final duplicated old-style figure appendix.
    start=text.find('\\clearpage\n\\begin{figure}[p]')
    if start>=0:text=text[:start]+'\\end{document}\n'
    # Original converter's inline Unicode set is extended for v3 notation.
    for a,b in [('κ',r'\(\kappa\)'),('ω',r'\(\omega\)'),('ₜ',r'\textsubscript{t}'),('ᵢ',r'\textsubscript{i}'),('ₕ',r'\textsubscript{h}'),('₊',r'\textsubscript{+}'),('⌈',r'\(\lceil\)'),('⌉',r'\(\rceil\)'),('∑',r'\(\sum\)'),('‖',r'\(\Vert\)')]:text=text.replace(a,b)
    for a,b in [('Ñ',r'\(\widetilde N\)'),('λ',r'\(\lambda\)'),('θ',r'\(\theta\)'),('η',r'\(\eta\)'),('⌊',r'\(\lfloor\)'),('⌋',r'\(\rfloor\)'),('ᵐ',r'\textsuperscript{m}'),('ᵗ',r'\textsuperscript{t}'),('ʳ',r'\textsuperscript{r}'),('–','--'),('—','---'),('’',"'"),('‘',"'"),('“','``'),('”',"''")]:text=text.replace(a,b)
    return restore_tex_math(text.replace('×',r'\(\times\)'),math_bindings)

def main():
    fonts();figures();c=json.loads((OUT/'paper-content.json').read_text())
    style={
      'body':ParagraphStyle('body',fontName='V3',fontSize=10,leading=13,spaceAfter=5),
      'title':ParagraphStyle('title',fontName='V3B',fontSize=17,leading=20,spaceAfter=10),
      'section':ParagraphStyle('section',fontName='V3B',fontSize=12,leading=15,spaceBefore=9,spaceAfter=5,keepWithNext=True),
      'sub':ParagraphStyle('sub',fontName='V3B',fontSize=10,leading=13,spaceBefore=7,spaceAfter=4,keepWithNext=True),
      'math':ParagraphStyle('math',fontName='V3Math',fontSize=9,leading=13,spaceBefore=5,spaceAfter=7),
      'cell':ParagraphStyle('cell',fontName='V3Math',fontSize=7.3,leading=9),
      'cap':ParagraphStyle('cap',fontName='V3',fontSize=8,leading=10,spaceAfter=5),
      'tablecap':ParagraphStyle('tablecap',fontName='V3',fontSize=8,leading=10,spaceAfter=5,keepWithNext=True),
      'ref':ParagraphStyle('ref',fontName='V3',fontSize=8,leading=10,spaceAfter=5)}
    def P(s,kind='body'):return Paragraph(safe(s),style[kind])
    story=[P(c['title'],'title'),P(c['subtitle'],'cap'),P(c['date'],'cap'),P('Abstract','sub'),P(c['abstract'])]
    placements=[];measure={'main_pages_including_references':None,'reproducibility_appendix_start':None,'inference_appendix_start':None};first=True
    def append_section(s):
        nonlocal first
        if s['title'].startswith('Appendix'):
            if first:
                story.extend([PageBreak(),P('References','section')]);story.extend(P(r['html'],'ref') for r in c['references']);first=False
            story.append(PageBreak())
        story.append(P(html.escape(s['title']),'section'))
        for b in s['blocks']:
            kind=b['type']
            if kind=='p':story.append(P(b['html']))
            elif kind=='subheading':story.append(P(html.escape(b['text']),'sub'))
            elif kind=='equation':story.append(P(b['html'],'math'))
            elif kind=='figure':
                f=c['figures'][b['index']];story.append(KeepTogether([InlinePDF(OUT/f['path'],placements),P(html.escape(f['caption']),'cap')]))
            elif kind=='table':
                n=len(b['headers']);width=495
                if b['caption'].startswith('Table I1.'):widths=[26,34,32,42,120,91,75,75]
                elif b['caption'].startswith('Table K1.'):widths=[125]+[(width-125)/(n-1)]*(n-1)
                elif n==7 and b['headers'][0]=='H':widths=[20,32,63,60,58,65,197]
                elif n==6 and b['headers'][0] in ('Comparison','Report'):widths=[150,45,75,75,75,75]
                elif n==2:widths=[110,385]
                elif n==3:widths=[85,205,205]
                else:widths=[width/n]*n
                cells=b.get('cell_html',{})
                data=[[P(cells.get(str(x),html.escape(str(x))),'cell') for x in row] for row in [b['headers'],*b['rows']]]
                t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
                t.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3)]))
                t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9eff4')),('LINEABOVE',(0,0),(-1,0),.6,colors.HexColor('#16324f')),('LINEBELOW',(0,0),(-1,0),.4,colors.HexColor('#16324f')),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#16324f')),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
                # This long panel follows its short appendix introduction at the
                # top of a fresh page. Let it split into that available space;
                # keeping the entire table with its caption wasted most of it.
                caption_kind='cap' if b['caption'].startswith('Table K1.') else 'tablecap'
                group=[P(html.escape(b['caption']),caption_kind),t,Spacer(1,7)]
                if b['caption'].startswith('Table D3.'):
                    story.append(KeepTogether(group))
                else:story.extend(group)
    for s in c['sections']:append_section(s)
    stream=io.BytesIO()
    class Document(SimpleDocTemplate):
        def afterFlowable(self,flow):
            if isinstance(flow,Paragraph):
                text=flow.getPlainText()
                if text.startswith('Appendix A.') and measure['main_pages_including_references'] is None:measure['main_pages_including_references']=self.page-1
                if text.startswith('Appendix G.'):measure['reproducibility_appendix_start']=self.page
                if text.startswith('Appendix H.'):measure['inference_appendix_start']=self.page
    def footer(cv,doc):cv.saveState();cv.setFont('V3',8);cv.drawCentredString(A4[0]/2,24,str(doc.page));cv.restoreState()
    doc=Document(stream,pagesize=A4,leftMargin=50,rightMargin=50,topMargin=44,bottomMargin=42,title=c['title'],author='')
    def deterministic_canvas(*args,**kwargs):
        kwargs['invariant']=1
        return canvas.Canvas(*args,**kwargs)
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=deterministic_canvas)
    writer=PdfWriter();reader=PdfReader(io.BytesIO(stream.getvalue()))
    for p in reader.pages:writer.add_page(p)
    for num,x,y,w,h,path in placements:
        fp=PdfReader(path).pages[0];transform=Transformation().scale(w/float(fp.mediabox.width),h/float(fp.mediabox.height)).translate(x,y)
        writer.pages[num-1].merge_transformed_page(fp,transform)
    writer.add_metadata({'/Title':c['title'],'/Author':'','/Subject':'v3 readability revision; ReportLab rendering, formal TeX supplied separately'})
    b=io.BytesIO();writer.write(b);save_bytes(OUT/'paper.pdf',b.getvalue());write(OUT/'main.tex',tex_source(c))
    measure.update(total_pages=len(reader.pages),renderer='ReportLab plus vector PDF overlays; current formal TeX source compilation deferred by user instruction',inline_vector_figures=len(placements),reproducibility_appendix_pages=(measure['inference_appendix_start'] or len(reader.pages)+1)-measure['reproducibility_appendix_start'])
    dump(RESULT/'rendering-summary.json',measure);print(json.dumps(measure))

if __name__=='__main__':main()
