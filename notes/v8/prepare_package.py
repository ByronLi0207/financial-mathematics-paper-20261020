"""v8 package metadata and deterministic source bundle; no financial replay."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'submission-jof'
TITLE='Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits'
KEYWORDS=['Peak net positions','Quantile forecasting','Historical benchmarks','Forecast comparison','Calibration','Dealer positions']
BASE='5e35dba21ea5ced708dad47cbee29fe12e4c6936'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def metadata():
    keyline='\\noindent\\textbf{Keywords:} '+'; '.join(KEYWORDS)+'.\\par\\medskip'
    p=PKG/'manuscript.tex';s=p.read_text();assert '\\textbf{Keywords:}' not in s
    s=s.replace('\\end{abstract}','\\end{abstract}\n\n'+keyline,1)
    assert 'figures/v8-endpoint-peak-example.pdf' not in s
    s=s.replace('figures/v7-endpoint-peak-example.pdf','figures/v8-endpoint-peak-example.pdf')
    old='\\paragraph{Code availability.} Code, saved results and version-specific reproduction instructions are available at \\url{https://github.com/ByronLi0207/financial-mathematics-paper-20261020}. This revision adds no new financial experiment. The completed results include adverse, failed and unavailable cases.'
    new='\\paragraph{Code availability.} Code, saved financial results and calibrated-simulation outputs are available at \\url{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v8}. The package README gives native document compilation; frozen protocols describe separate restricted-input replays. This revision adds no new financial forecast evaluation. The completed results include adverse, failed and unavailable cases.'
    assert old in s;s=s.replace(old,new);p.write_text(s)
    p=PKG/'title-page.tex';s=p.read_text();anchor='Running title: Historical Rules and Peak Limits\\par\\medskip'
    assert anchor in s and 'Keywords:' not in s
    s=s.replace(anchor,anchor+'\nKeywords: '+'; '.join(KEYWORDS)+'.\\par\\medskip')
    s=s.replace('https://github.com/ByronLi0207/financial-mathematics-paper-20261020}', 'https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v8}')
    p.write_text(s)
    p=PKG/'cover-letter.md';s=p.read_text()
    s=s.replace('The paper addresses comparative forecast evaluation, demanding simple benchmarks and the practical choice of position limits.','The manuscript fits Journal of Forecasting through comparative forecast evaluation, demanding historical benchmarks and practical validation of peak-position limits.')
    s=s.replace('A calibration adjustment retains the later FX gain with 329 versus 328 breaches,','A calibration adjustment retains the later 15.0% FX gain with 329 versus 328 breaches,')
    s=s.replace('Standard methods and elementary target properties support these comparisons; they are not presented as methodological contributions.','Standard forecasters and elementary target properties support these empirical comparisons.')
    s=s.replace('Author information and all required declarations remain marked for author completion before submission.','')
    p.write_text(s.replace('  ',' '))
    def latex_escape(text):
        text=re.sub(r'"([^"\n]+)"',lambda m:'``'+m.group(1)+"''",text)
        return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in text)
    letter='\\documentclass[11pt,a4paper]{article}\n\\usepackage[margin=25mm]{geometry}\n\\usepackage[T1]{fontenc}\n\\setlength{\\parindent}{0pt}\n\\setlength{\\parskip}{9pt}\n\\setlength{\\emergencystretch}{3em}\n\\pagestyle{empty}\n\\begin{document}\n'+ '\n\n'.join(latex_escape(p) for p in s.strip().split('\n\n'))+'\n\\end{document}\n'
    with (PKG/'cover-letter.tex').open('x') as f:f.write(letter)
    placeholders={}
    for name in ['manuscript.tex','title-page.tex','cover-letter.md']:
        original=subprocess.check_output(['git','show',BASE+':submission-jof/'+name],text=True)
        actual=(PKG/name).read_text();old=original.count('[TO BE COMPLETED BY AUTHOR]');new=actual.count('[TO BE COMPLETED BY AUTHOR]');assert old==new
        placeholders[name]={'baseline_count':old,'current_count':new}
    x={'title':TITLE,'running_title':'Historical Rules and Peak Limits','running_title_characters':len('Historical Rules and Peak Limits'),'keywords':KEYWORDS,'placeholder_counts':placeholders,'target_branch':'revision-v8','base':BASE,'created_utc':datetime.now(timezone.utc).isoformat()}
    with (ROOT/'notes/v8/package-metadata.json').open('x') as f:json.dump(x,f,indent=2);f.write('\n')
    print(json.dumps(x,indent=2))


def finalize():
    from pypdf import PdfReader
    receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'documents':{}}
    for name in ['manuscript','supplement','title-page','cover-letter']:
        tex=PKG/(name+'.tex');pdf=PKG/(name+'.pdf');reader=PdfReader(pdf)
        receipt['documents'][name]={'source_sha256':sha(tex),'pdf_sha256':sha(pdf),'producer':str(reader.metadata.get('/Producer','')),'pages':len(reader.pages),'command':f'/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic --keep-logs --outdir submission-jof submission-jof/{name}.tex','exit_code':0}
        if name!='cover-letter':shutil.copyfile(pdf,PKG/(name+'-preview.pdf'))
    assert receipt['documents']['manuscript']['pages']<=18
    assert receipt['documents']['title-page']['pages']==1 and receipt['documents']['cover-letter']['pages']==1
    for name,bind in [('manuscript',['../notes/v7/main-v7-numeric-bindings.json','../notes/v8/contribution-bindings.json','../notes/v8/writing-numeric-bindings.json','../notes/v8/mc-main-bindings.json']),('supplement',['../notes/v7/s5-supplement-bindings.json','../notes/v8/mc-supplement-bindings.json'])]:
        source=PKG/(name+'.tex');content=json.loads((PKG/(name+'-content.json')).read_text())
        content.update(schema='v8-latex-snapshot',title=TITLE,canonical_source=source.name,source_sha256=sha(source),latex=source.read_text(),source_bindings=bind)
        (PKG/(name+'-content.json')).write_text(json.dumps(content,indent=2)+'\n')
    (ROOT/'notes/v8/package-compilation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    members=['main.tex','manuscript.tex','supplement.tex','title-page.tex','cover-letter.tex','references.bib','README.md','AUTHOR-TODO.md','cover-letter.md','manuscript.pdf','supplement.pdf','title-page.pdf','cover-letter.pdf']
    members+=sorted(set(re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',(PKG/'manuscript.tex').read_text())))
    assert len([x for x in members if x.startswith('figures/')])==4
    with zipfile.ZipFile(PKG/'overleaf-package.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in members:
            data=(PKG/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,10,24,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    manifest={'zip':'submission-jof/overleaf-package.zip','zip_sha256':sha(PKG/'overleaf-package.zip'),'members':{name:sha(PKG/name) for name in members}}
    (ROOT/'notes/v8/package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'pages':{k:v['pages'] for k,v in receipt['documents'].items()},'zip_members':len(members),'zip_sha256':manifest['zip_sha256']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['metadata','finalize']);a=p.parse_args()
    metadata() if a.stage=='metadata' else finalize()
