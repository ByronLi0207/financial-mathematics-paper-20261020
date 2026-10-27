"""Read actual PDF figure invocation matrices and resulting printed type sizes."""
from pathlib import Path
import hashlib
import json
import math
import sys
from pypdf import PdfReader
from pypdf.generic import ContentStream

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
GROUPS=[('manuscript',['v9-endpoint-peak-example','v10-cftc-contract-changes',
                      'v10-menu-isolation','v10-cost-regions']),
        ('supplement',['v7-murphy-fx_hourly','v7-murphy-nyfed_weekly'])]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def multiply(x,y):
    a,b,c,d,e,f=x;g,h,i,j,k,l=y
    return [a*g+c*h,b*g+d*h,a*i+c*j,b*i+d*j,a*k+c*l+e,b*k+d*l+f]

def native_sizes(path):
    sizes=[]
    def visit(t,cm,tm,font,size):
        if t.strip():sizes.append(float(size)*math.hypot(cm[0],cm[1]))
    for page in PdfReader(path).pages:page.extract_text(visitor_text=visit)
    return sorted(set(sizes))

def main():
    directory=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'submission-v10'
    out=[]
    for document,stems in GROUPS:
        pdf=directory/f'{document}.pdf';reader=PdfReader(pdf);forms=[]
        for index,page in enumerate(reader.pages):
            matrix=[1,0,0,1,0,0];stack=[]
            resources=page['/Resources'].get('/XObject',{})
            for args,op in ContentStream(page.get_contents(),reader).operations:
                if op==b'q':stack.append(matrix[:])
                elif op==b'Q':matrix=stack.pop()
                elif op==b'cm':matrix=multiply(matrix,list(map(float,args)))
                elif op==b'Do':
                    obj=resources[args[0]].get_object()
                    if obj.get('/Subtype')!='/Form':continue
                    box=list(map(float,obj['/BBox']))
                    # All six figures are vector PDFs with native 6.25in width.
                    if abs(box[2]-box[0]-450)>1e-5:continue
                    local=list(map(float,obj.get('/Matrix',[1,0,0,1,0,0])))
                    actual=multiply(matrix,local)
                    forms.append(dict(page=index+1,xobject=str(args[0]),bbox=box,
                        actual_invocation_matrix=actual,actual_scale=math.hypot(actual[0],actual[1])))
        assert len(forms)==len(stems),(document,len(forms),len(stems))
        for stem,form in zip(stems,forms):
            source=ROOT/'submission-v10/figures'/f'{stem}.pdf';sizes=native_sizes(source)
            scale=form['actual_scale'];form.update(figure=stem,source_pdf_sha256=sha(source),
                native_font_sizes_pt=sizes,actual_font_sizes_pt=[x*scale for x in sizes],
                actual_minimum_font_pt=min(sizes)*scale,
                actual_minimum_non_subscript_font_pt=min(x for x in sizes if x>=8)*scale)
        out.append(dict(document=str(pdf.relative_to(ROOT)),sha256=sha(pdf),pages=len(reader.pages),figures=forms))
    result=dict(method='Actual page content-stream cm and Do matrices for each included vector figure; no nominal include-width inference.',
                documents=out)
    (HERE/'visual-qa/final-pdf-scale-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
