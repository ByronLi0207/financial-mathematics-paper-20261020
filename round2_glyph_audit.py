"""Check every rendered paragraph fragment against its actual font cmap."""
import html,json,sys
from collections import Counter
from pathlib import Path
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from pypdf import PdfReader
from build_revision_v3 import fonts,safe
from v3_revision import ROOT

def main():
    fonts();c=json.loads((ROOT/'manuscript/revision-v3/paper-content.json').read_text());texts=[]
    def add(label,text,font):texts.append((label,str(text),font))
    for key in ['title','subtitle','date','abstract']:add(key,c[key],'V3B' if key=='title' else 'V3')
    for section in c['sections']:
        add(section['title'],html.escape(section['title']),'V3B')
        for j,b in enumerate(section['blocks']):
            label=section['title']+':'+str(j)
            if b['type'] in ['p','equation']:add(label,b['html'],'V3Math' if b['type']=='equation' else 'V3')
            elif b['type']=='subheading':add(label,html.escape(b['text']),'V3B')
            elif b['type']=='table':
                add(label+' caption',html.escape(b['caption']),'V3');overrides=b.get('cell_html',{})
                for ri,row in enumerate([b['headers'],*b['rows']]):
                    for ci,cell in enumerate(row):add(label+f'[{ri},{ci}]',overrides.get(str(cell),html.escape(str(cell))),'V3Math')
    for r in c['references']:add('reference '+r['id'],r['html'],'V3')
    for i,f in enumerate(c['figures']):add('figure caption '+str(i),html.escape(f['caption']),'V3')
    checked=0;unique=set();missing=[]
    for label,text,font in texts:
        p=Paragraph(safe(text),ParagraphStyle('audit',fontName=font,fontSize=10))
        for frag in p.frags:
            for ch in getattr(frag,'text',''):
                if ch.isspace():continue
                name=frag.fontName;checked+=1;unique.add((name,ch))
                if not pdfmetrics.getFont(name).face.charToGlyph.get(ord(ch),0):missing.append(dict(location=label,font=name,character=ch,codepoint=f'U+{ord(ch):04X}'))
    for f in c['figures']:
        path=ROOT/'manuscript/revision-v3'/f['path']
        for page in PdfReader(path).pages:
            for ch in page.extract_text():
                if ch.isspace():continue
                checked+=1;unique.add(('V3Math',ch))
                if not pdfmetrics.getFont('V3Math').face.charToGlyph.get(ord(ch),0):missing.append(dict(location=f['path'],font='V3Math',character=ch,codepoint=f'U+{ord(ch):04X}'))
    pages=PdfReader(ROOT/'manuscript/revision-v3/paper.pdf').pages;notation=[i+1 for i,p in enumerate(pages) if 'Notation. Distinct symbols' in p.extract_text()]
    print(json.dumps(dict(paragraphs_and_cells=len(texts),checked_character_occurrences=checked,distinct_font_character_pairs=len(unique),missing_glyphs=len(missing),missing=missing,notation_pages=notation,pdf_pages=len(pages),scope='actual ReportLab text fragments plus figure text cmap; visible placement separately inspected at150dpi'),ensure_ascii=False,indent=2))
    return bool(missing)
if __name__=='__main__':raise SystemExit(main())
