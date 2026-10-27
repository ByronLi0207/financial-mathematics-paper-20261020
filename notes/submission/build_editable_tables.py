"""Extract unchanged canonical table environments into an editable table file."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil,subprocess
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2];DOC=ROOT/'submission-final';OUT=ROOT/'submission-package/SHARED'
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def expand(path):
    text=path.read_text()
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(DOC/(m[1]+('' if Path(m[1]).suffix else '.tex'))),text)

def backup(p):
    if p.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(p.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');shutil.copyfile(p,p.with_name(p.name+'.'+stamp+'.bak'))

def main():
    text=expand(DOC/'manuscript.tex');tables=re.findall(r'\\begin\{table\}(?:\[[^\]]*\])?.*?\\end\{table\}',text,re.S)
    assert len(tables)==8
    assert not any(re.search(r'\\cite[a-z]*\{',t) for t in tables)
    aux=(ROOT/'submission-package/ASMBI/manuscript.aux').read_text()
    labels=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}',aux))
    reference_bindings=[]
    def resolved(m):
        value=labels[m[1]];reference_bindings.append(dict(label=m[1],value=value,source='submission-package/ASMBI/manuscript.aux'));return value
    pre=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{amsmath,amssymb,graphicx,booktabs,array,caption}
\usepackage[unicode,hidelinks]{hyperref}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\setlength{\tabcolsep}{3pt}\setlength{\emergencystretch}{3em}
\captionsetup{font=small,labelfont=bf}
\begin{document}
'''
    body='\n\n\\clearpage\n\n'.join(re.sub(r'\\ref\{([^}]+)\}',resolved,re.sub(r'\\begin\{table\}(?:\[[^\]]*\])?',r'\\begin{table}[p]',t,count=1)) for t in tables)
    target=OUT/'editable-tables.tex';backup(target);target.write_text(pre+body+'\n\\end{document}\n')
    work=ROOT/'.scratch/submission/editable-tables'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');work.mkdir(parents=True)
    cmd=['/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic','-X','compile','-C',str(target),'--outdir',str(work),'--keep-logs','--keep-intermediates']
    q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(work/'console.txt').write_text(q.stdout);assert q.returncode==0,q.stdout
    log=(work/'editable-tables.log').read_text();bad=re.findall(r'Overfull[^\n]*|(?:Reference|Citation)[^\n]*undefined|Missing character[^\n]*',log);assert not bad,bad
    pdf=OUT/'editable-tables.pdf';backup(pdf);shutil.copyfile(work/'editable-tables.pdf',pdf);assert len(PdfReader(pdf).pages)==len(tables)
    record=dict(status='PASS',tables=[dict(number=i+1,label=re.search(r'\\label\{([^}]+)\}',t)[1],canonical_environment_sha256=sha(t.encode())) for i,t in enumerate(tables)],reference_bindings=reference_bindings,pages=len(tables),pdf_sha256=sha(pdf.read_bytes()),source_sha256=sha(target.read_bytes()),command=cmd,source_rule='Canonical environments in their original order; only float placement becomes page-only and external proposition references use their actual compiled numbers.')
    out=ROOT/'notes/submission/editable-tables.json';backup(out);out.write_text(json.dumps(record,indent=2)+'\n');print('Editable tables:',len(tables),'pages:',record['pages'])

if __name__=='__main__':main()
