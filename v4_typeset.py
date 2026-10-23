"""Deterministic standard-article TeX and separately typeset vector PDF previews."""
from pathlib import Path
from copy import deepcopy
import html,io,json,re
from v4_submission import ROOT,OUT,NOTE,dump,plain
from v3_math_format import prepare_tex_math,restore_tex_math,CATALOG
from build_tex import conv,esc

UNICODE={'κ':r'\kappa','ω':r'\omega','η':r'\eta','λ':r'\lambda','θ':r'\theta','α':r'\alpha','β':r'\beta','γ':r'\gamma','ν':r'\nu','δ':r'\delta','Φ':r'\Phi','∑':r'\sum','⌈':r'\lceil','⌉':r'\rceil','⌊':r'\lfloor','⌋':r'\rfloor','‖':r'\Vert','√':r'\sqrt{}','×':r'\times','∞':r'\infty','∣':r'\vert','∥':r'\Vert','ℝ':r'\mathbb R'}

def tconv(value):
 s=conv(str(value))
 for u,t in UNICODE.items():s=s.replace(u,r'\('+t+r'\)')
 for u,t in {'ₜ':'t','ᵢ':'i','ₕ':'h','₊':'+','₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}.items():s=s.replace(u,r'\textsubscript{'+t+'}')
 for u,t in {'ᵐ':'m','ᵗ':'t','ʳ':'r','⁶':'6','²':'2','⁻':'-'}.items():s=s.replace(u,r'\textsuperscript{'+t+'}')
 s=s.replace('Ñ',r'\(\widetilde N\)').replace('L̄',r'\(\overline L\)').replace('†',r'\(\dagger\)')
 s=s.replace('–','--').replace('—','---').replace('’',"'").replace('‘',"'").replace('“','``').replace('”',"''")
 return s

def math_prepare(d):
 c=deepcopy(d)
 extras={
 'ε<sub>s</sub>=N<sub>s+1</sub>−c−φN<sub>s</sub>':r'\varepsilon_s=N_{s+1}-c-\phi N_s',
 'Ñ<super>tr</super>':r'\widetilde N^{\rm tr}',
 'U=mean(P−C)<sub>+</sub>':r'U=\operatorname{mean}[(P-C)_+]',
 'V=mean(C−P)<sub>+</sub>':r'V=\operatorname{mean}[(C-P)_+]',
 'ρ=1/W':r'\rho=1/W','τ=19/20':r'\tau=19/20'}
 for sec in c['sections']:
  for b in sec['blocks']:
   if 'html' in b:b['inline_math']=b.get('inline_math',[])+[{'html':k,'latex':v} for k,v in (CATALOG|extras).items() if k in b['html'] and not any(x['html']==k for x in b.get('inline_math',[]))]
 return prepare_tex_math(c)

def tex_document(doc):
 c,bindings=math_prepare(doc)
 parts=[r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,graphicx,booktabs,array,longtable}
\usepackage[unicode,breaklinks=true,hidelinks]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{3pt}
\begin{document}
''',r'\begin{center}\Large\bfseries '+tconv(c['title'])+r'\end{center}'+'\n']
 if c['subtitle']:parts.append(tconv(c['subtitle'])+'\n\n')
 if c['abstract']:parts += ['\\begin{abstract}\n'+tconv(c['abstract'])+'\n\\end{abstract}\n',tconv('Keywords: quantile forecasting; sampled path maxima; net positions; forecast evaluation; calibration; model validation')+'\n\n']
 for sec in c['sections']:
  parts.append('\\section*{'+tconv(sec['title'])+'}\n')
  for b in sec['blocks']:
   typ=b['type']
   if typ=='p':parts.append(tconv(b['html'])+'\n\n')
   elif typ=='subheading':parts.append('\\subsection*{'+tconv(b['text'])+'}\n')
   elif typ=='equation':parts.append('\\[\n'+b['latex']+'\n\\]\n')
   elif typ=='table':
    n=len(b['headers']);w=.96/n
    if b['caption'].startswith('Table S26'):widths=[x/467*.94 for x in [24,30,26,35,112,80,80,80]]
    elif n==2:widths=[.23,.73]
    elif n==3:widths=[.18,.41,.37]
    elif n==7 and b['headers'][0]=='Comparison':widths=[.20,.08,.09,.09,.12,.19,.17]
    else:widths=[w]*n
    align=''.join('>{\\raggedright\\arraybackslash}p{'+f'{x:.3f}'+r'\linewidth}' for x in widths)
    parts += ['\\begingroup\\footnotesize\n\\begin{samepage}'+tconv(b['caption'])+'\\end{samepage}\n\\begin{longtable}{'+align+'}\n\\toprule\n', ' & '.join(tconv(str(x)) for x in b['headers'])+r' \\'+'\n\\midrule\n\\endhead\n']
    for row in b['rows']:parts.append(' & '.join(tconv(b.get('cell_html',{}).get(str(x),html.escape(str(x)))) for x in row)+r' \\'+'\n')
    parts.append('\\bottomrule\n\\end{longtable}\n\\endgroup\n')
   elif typ=='figure':
    f=c['figures'][b['index']];parts.append('\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=.96\\linewidth]{'+f['path']+'}\n\\caption*placeholder\n'+tconv(f['caption'])+'\n\\end{figure}\n')
 parts.append('\\section*{References}\n')
 for r in c['references']:parts.append(tconv(r['html'])+'\n\n')
 parts.append(('\\clearpage\n' if c['abstract'] else '')+'\\section*{Figure captions}\n')
 for f in c['figures']:parts.append(tconv(f['caption'])+'\n\n')
 parts.append('\\end{document}\n')
 return restore_tex_math(''.join(parts).replace('\\caption*placeholder\n',''),bindings)

def pdf_document(doc,target):
 from build_revision_v3 import fonts,safe,InlinePDF
 from reportlab.lib.styles import ParagraphStyle
 from reportlab.lib import colors
 from reportlab.lib.pagesizes import A4
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,PageBreak
 from pypdf import PdfReader,PdfWriter,Transformation
 fonts();W=467
 styles={
 'body':ParagraphStyle('body',fontName='V3',fontSize=10.2,leading=13.5,spaceAfter=5),
 'title':ParagraphStyle('title',fontName='V3B',fontSize=16,leading=19,spaceAfter=12),
 'section':ParagraphStyle('section',fontName='V3B',fontSize=12,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'sub':ParagraphStyle('sub',fontName='V3B',fontSize=10.3,leading=13,spaceBefore=7,spaceAfter=5,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='V3',fontSize=7.3,leading=9.3),
 'math':ParagraphStyle('math',fontName='V3Math',fontSize=9,leading=13,spaceBefore=5,spaceAfter=7),
 'ref':ParagraphStyle('ref',fontName='V3',fontSize=8.2,leading=10.5,spaceAfter=5),
 'tablecap':ParagraphStyle('tablecap',fontName='V3',fontSize=8.2,leading=10.5,spaceAfter=6,keepWithNext=True),
 'cap':ParagraphStyle('cap',fontName='V3',fontSize=8.2,leading=10.5,spaceAfter=6)}
 def P(text,style='body'):return Paragraph(safe(text),styles[style])
 story=[P(html.escape(doc['title']),'title'),P(html.escape(doc['subtitle']),'cap')]
 if doc['abstract']:story += [P('Abstract','sub'),P(doc['abstract']),P('Keywords: quantile forecasting; sampled path maxima; net positions; forecast evaluation; calibration; model validation','cap')]
 places=[]
 for s in doc['sections']:
  if s['title'].startswith('S14.') :story.append(PageBreak())
  story.append(P(html.escape(s['title']),'section'))
  for b in s['blocks']:
   typ=b['type']
   if typ=='p':story.append(P(b['html']))
   elif typ=='subheading':story.append(P(html.escape(b['text']),'sub'))
   elif typ=='equation':story.append(P(b['html'],'math'))
   elif typ=='table':
    n=len(b['headers'])
    if b['caption'].startswith('Table S26'):widths=[24,30,26,35,112,80,80,80]
    elif n==2:widths=[105,362]
    elif n==3:widths=[85,195,187]
    elif n==7 and b['headers'][0]=='Comparison':widths=[93,38,44,44,55,91,102]
    elif n==8 and b['headers'][0]=='Series key':widths=[100]+[367/7]*7
    else:widths=[W/n]*n
    cells=b.get('cell_html',{})
    data=[[P(cells.get(str(x),html.escape(str(x))),'cell') for x in row] for row in [b['headers'],*b['rows']]]
    table=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEABOVE',(0,0),(-1,0),.7,colors.black),('LINEBELOW',(0,0),(-1,0),.4,colors.black),('LINEBELOW',(0,-1),(-1,-1),.7,colors.black),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2)]))
    story += [P(html.escape(b['caption']),'tablecap'),table,Spacer(1,6)]
   elif typ=='figure':
    f=doc['figures'][b['index']];story.append(KeepTogether([InlinePDF(OUT/f['path'],places,width=W),P(html.escape(f['caption']),'cap')]))
 if doc['references']:
  story.append(P('References','section'));story.extend(P(r['html'],'ref') for r in doc['references'])
 if doc['figures']:
  if doc['abstract']:story.append(PageBreak())
  story.append(P('Figure captions','section'));story.extend(P(html.escape(f['caption']),'cap') for f in doc['figures'])
 def foot(c,d):
  c.setFont('V3',8);c.drawString(64,28,'Separate ReportLab preview; standard-article TeX supplied');c.drawRightString(A4[0]-64,28,str(d.page))
 stream=io.BytesIO();SimpleDocTemplate(stream,pagesize=A4,leftMargin=64,rightMargin=64,topMargin=48,bottomMargin=43,title=doc['title'],author='',pageCompression=1,invariant=1).build(story,onFirstPage=foot,onLaterPages=foot)
 reader=PdfReader(stream);writer=PdfWriter()
 for page in reader.pages:writer.add_page(page)
 for page,x,y,w,h,path in places:
  overlay=PdfReader(path).pages[0];sw=float(overlay.mediabox.width);sh=float(overlay.mediabox.height)
  writer.pages[page-1].merge_transformed_page(overlay,Transformation().scale(w/sw,h/sh).translate(x,y))
 writer.add_metadata({'/Title':doc['title'],'/Author':'','/Subject':'ReportLab preview; not native compiler PDF export'})
 with target.open('wb') as f:writer.write(f)
 return len(reader.pages)

def main():
 documents={name:json.loads((OUT/(name+'-content.json')).read_text()) for name in ('manuscript','supplement')}
 metrics={}
 for name,d in documents.items():
  (OUT/(name+'.tex')).write_text(tex_document(d))
  pages=pdf_document(d,OUT/(name+'-preview.pdf'))
  text=' '.join(plain(b.get('html',b.get('text',''))) for s in d['sections'] for b in s['blocks'] if b['type'] in ('p','subheading'))
  metrics[name]={'pages':pages,'prose_words_excluding_abstract_references_tables_captions':len(text.split()),'abstract_words':len(d['abstract'].split()),'main_tables':sum(b['type']=='table' for s in d['sections'] for b in s['blocks']),'figures':len(d['figures'])}
 dump((ROOT/'notes/revision-v5-novelty' if documents['manuscript'].get('_abstract_generator') else NOTE)/'document-metrics.json',metrics);print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
