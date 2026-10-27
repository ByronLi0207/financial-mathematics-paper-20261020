"""QA only: raster previews, CVD simulations, PDF font sizes and table samples."""
from pathlib import Path
import json
import re
import subprocess
from PIL import Image, ImageOps, ImageDraw
import numpy as np
from colorspacious import cspace_convert
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
QA=HERE/'visual-qa'
FIG=ROOT/'submission-v10/figures'
STEMS=['v9-endpoint-peak-example','v10-cftc-contract-changes','v10-menu-isolation',
       'v10-cost-regions','v7-murphy-fx_hourly','v7-murphy-nyfed_weekly']

def sheet(paths,target,columns=2,width=1000):
    tiles=[]
    for label,path in paths:
        im=Image.open(path).convert('RGB')
        im.thumbnail((width-30,900))
        tile=Image.new('RGB',(width,im.height+45),'white')
        ImageDraw.Draw(tile).text((15,10),label,fill='black')
        tile.paste(im,((width-im.width)//2,35))
        tiles.append(tile)
    row_heights=[max(t.height for t in tiles[i:i+columns]) for i in range(0,len(tiles),columns)]
    out=Image.new('RGB',(columns*width,sum(row_heights)), '#e2e2e2')
    y=0
    for i,h in enumerate(row_heights):
        for j,t in enumerate(tiles[i*columns:(i+1)*columns]):out.paste(t,(j*width,y))
        y+=h
    out.save(target)

def fonts(path):
    sizes=[]
    def visit(text,cm,tm,font,size):
        if text.strip():sizes.append(float(size)*(cm[0]*cm[0]+cm[1]*cm[1])**.5)
    for p in PdfReader(path).pages:p.extract_text(visitor_text=visit)
    return dict(min_pt=min(sizes),median_pt=float(np.median(sizes)),max_pt=max(sizes),text_runs=len(sizes))

def main():
    results={}
    print_width=(210-50)/25.4
    fractions=[.94,.97,.98,.98,.94,.94]
    for stem,fraction in zip(STEMS,fractions):
        source=FIG/f'{stem}.png'
        im=Image.open(source).convert('RGB');im.thumbnail((1200,1400))
        arr=np.asarray(im)/255.
        for mode in ['deuteranomaly','protanomaly','tritanomaly']:
            simulation=cspace_convert(arr,{'name':'sRGB1+CVD','cvd_type':mode,'severity':100},'sRGB1')
            Image.fromarray((np.clip(simulation,0,1)*255).astype('uint8')).save(QA/f'{stem}-{mode}.png')
        ImageOps.grayscale(im).save(QA/f'{stem}-grayscale.png')
        before=QA/'before'/f'{stem}.pdf'
        results[stem]=dict(after_pdf=fonts(FIG/f'{stem}.pdf'),before_pdf=fonts(before))
        actual_print_width=print_width if stem in STEMS[:4] else (210-40)/25.4
        for phase,pdf in [('before',before),('after',FIG/f'{stem}.pdf')]:
            page=PdfReader(pdf).pages[0]
            width=float(page.mediabox.width)/72
            scale=actual_print_width*fraction/width
            results[stem][phase+'_print_scale']=scale
            results[stem][phase+'_minimum_effective_font_pt']=results[stem][phase+'_pdf']['min_pt']*scale
        command=['/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm',
                 '-r','120','-singlefile','-png',str(before),str(QA/(stem+'-before'))]
        q=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        assert q.returncode==0,q.stdout
    sheet([(s,FIG/f'{s}.png') for s in STEMS],QA/'all-figures-after.png')
    sheet([(s,QA/f'{s}-before.png') for s in STEMS],QA/'all-figures-before.png')
    sheet([(s,QA/f'{s}-deuteranomaly.png') for s in STEMS],QA/'all-figures-deuteranomaly.png')
    sheet([(s,QA/f'{s}-protanomaly.png') for s in STEMS],QA/'all-figures-protanomaly.png')
    sheet([(s,QA/f'{s}-tritanomaly.png') for s in STEMS],QA/'all-figures-tritanomaly.png')
    sheet([(s,QA/f'{s}-grayscale.png') for s in STEMS],QA/'all-figures-grayscale.png')
    # A4, actual manuscript margins, and three unchanged display-table inputs.
    prefix=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,graphicx,booktabs,array}
\usepackage{caption,placeins}
\setlength{\parindent}{0pt}\setlength{\tabcolsep}{3pt}
\captionsetup{font=small,labelfont=bf}
\begin{document}
'''
    body='\n\\clearpage\n'.join('\\input{'+str(ROOT/'submission-v10/generated'/name)+'}'
        for name in ['v10-cftc-contracts.tex','v10-mcs-main.tex','v10-menu-main.tex'])
    path=QA/'tables.tex';path.write_text(prefix+body+'\n\\end{document}\n')
    command=['/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic','-X','compile',
             str(path),'--outdir',str(QA),'--keep-logs']
    q=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd=ROOT)
    (QA/'tables-build-console.txt').write_text(q.stdout)
    assert q.returncode==0,q.stdout
    results['table_sample']=fonts(QA/'tables.pdf')
    results['table_sample']['pages']=len(PdfReader(QA/'tables.pdf').pages)
    results['table_sample']['overfull']=re.findall(r'Overfull[^\n]*',q.stdout)
    command=['/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm',
             '-r','140','-png',str(QA/'tables.pdf'),str(QA/'table-sample')]
    q=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    assert q.returncode==0,q.stdout
    sheet([(p.name,p) for p in sorted(QA.glob('table-sample-*.png'))],QA/'tables-contact.png',columns=3,width=800)
    (QA/'render-font-qa.json').write_text(json.dumps(results,indent=2)+'\n')
    if (QA/'supplement-tables.pdf').exists():
        sheet([(p.name,p) for p in sorted(QA.glob('supp-table-*.png'))],QA/'supplement-tables-contact.png',columns=3,width=800)
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
