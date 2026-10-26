"""Render saved aggregate display data as grayscale vector figures; never fit."""
from pathlib import Path
import csv,hashlib,json
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream,FloatObject
from reportlab.pdfgen import canvas
from build_revision_v3 import fonts
from v4_submission import ROOT,OUT,NOTE,dump

def main():
 fonts();out=OUT/'figures';out.mkdir(exist_ok=True);manifest=[]
 for p in (ROOT/'manuscript/revision-v3/figures').glob('*.pdf'):
  if p.name.startswith('murphy-'):continue
  r=PdfReader(p);w=PdfWriter()
  for page in r.pages:
   w.add_page(page);pg=w.pages[-1];cs=ContentStream(pg.get_contents(),w)
   for operands,operator in cs.operations:
    if operator in (b'rg',b'RG'):operands[:]=[FloatObject(0),FloatObject(0),FloatObject(0)]
   pg.replace_contents(cs)
  with (out/p.name).open('wb') as f:w.write(f)
  manifest.append({'output':str((out/p.name).relative_to(ROOT)),'source':str(p.relative_to(ROOT)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'operation':'vector-preserving black drawing; numbers unchanged'})
 for source,label in [('fx_hourly','FX'),('nyfed_weekly','Treasury')]:
  p=ROOT/'results/revision-20261023/inference'/('murphy-'+source+'-display.csv');rs=list(csv.DictReader(p.open()))
  x=[float(r['theta_USD_millions']) for r in rs];ys=[[float(r[k]) for r in rs] for k in ('left_elementary','right_elementary')]
  low,high=min(x),max(x);top=max(max(y) for y in ys)*1.08
  c=canvas.Canvas(str(out/('murphy-'+source+'.pdf')),pagesize=(510,255),invariant=1)
  def text(a,b,s,size=8):c.setFont('V3Math',size);c.setFillGray(0);c.drawString(a,b,s)
  text(42,236,label+' original primary: fixed τ = 0.95',10)
  for i in range(5):
   xx=48+i*437/4;v=low+(high-low)*i/4;text(xx-12,32,f'{v:.3g}',7)
   yy=52+i*164/4;value=top*i/4;text(3,yy-2,f'{value:.3f}',7);c.setStrokeGray(.85);c.setLineWidth(.4);c.line(46,yy,487,yy)
  c.setStrokeGray(0);c.setLineWidth(.6);c.line(46,52,487,52);c.line(46,52,46,216)
  for j,y in enumerate(ys):
   c.setStrokeGray(0 if j==0 else .3);c.setLineWidth(1.1);c.setDash([] if j==0 else [5,3])
   path=c.beginPath()
   for i,(xx,yy) in enumerate(zip(x,y)):
    fx=48+(xx-low)/(high-low)*437;fy=52+yy/top*164
    (path.moveTo if i==0 else path.lineTo)(fx,fy)
   c.drawPath(path)
   lx=285;ly=239-j*13;c.line(lx,ly,lx+22,ly);text(lx+27,ly-3,'QR' if j==0 else ('Rolling F' if source=='fx_hourly' else 'Frozen F'),8)
  c.setDash([]);text(113,12,'Threshold θ (source USD millions); mean elementary score',8)
  c.showPage();c.save()
  manifest.append({'output':str((out/('murphy-'+source+'.pdf')).relative_to(ROOT)),'source':str(p.relative_to(ROOT)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'operation':'all saved display rows; grayscale solid/dashed vector curves; no breakpoint test rerun'})
 dump(NOTE/'figure-bindings.json',manifest);print('Five grayscale vector figures; original source bytes untouched.')
if __name__=='__main__':main()
