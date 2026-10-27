"""Build author-facing submission attachments; no scientific computations."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'submission-package/SHARED'
TEX='/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def backup(p):
    if p.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(p.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copyfile(p,p.with_name(p.name+'.'+stamp+'.bak'))

def save(p,text):
    backup(p);p.write_text(text)

def esc(text):
    pairs={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(pairs.get(c,c) for c in text)

def inline(text):
    links=[]
    def hold(m):
        links.append(r'\href{'+m[2].replace('%',r'\%')+'}{'+esc(m[1])+'}')
        return 'ZZLINK'+str(len(links)-1)+'ZZ'
    text=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',hold,text)
    text=text.replace('**','').replace('`','').replace('\u2013','--').replace('\u2014','---')
    text=esc(text)
    for i,link in enumerate(links):text=text.replace('ZZLINK'+str(i)+'ZZ',link)
    return text

PRE=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[unicode,hidelinks]{hyperref}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{3em}
\begin{document}
'''

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    declarations=r'''\section*{Author statements for submission}
\textbf{Manuscript:} Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits.

\textbf{Authors and order:} [TO BE COMPLETED BY AUTHOR].

\textbf{Affiliations and corresponding author:} [TO BE COMPLETED BY AUTHOR].

\textbf{ORCID identifiers:} [TO BE COMPLETED BY AUTHOR].

\textbf{Funding and grant identifiers:} [TO BE COMPLETED BY AUTHOR].

\textbf{Competing interests:} [TO BE COMPLETED BY AUTHOR].

\textbf{CRediT author contributions:} [TO BE COMPLETED BY AUTHOR: assign only applicable roles and identify the responsible authors].

\textbf{Permissions and ethics applicability:} [TO BE CONFIRMED BY AUTHOR].

\textbf{Data availability.} The financial sources and exact input identities are documented in the manuscript and reproduction guide. Obtain the FX dataset from its original Kaggle source subject to the rights holders' terms; raw FX observations and private prediction vectors are excluded. New York Fed and CFTC data are publicly accessible from the named official services, with source conditions and vintage limitations retained. [AUTHOR TO CONFIRM ACCESS RIGHTS AND ANY EDITORIAL SHARING EXCEPTION].

\textbf{Code availability.} Code, written protocols and public aggregate outputs are available in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/submission-final}{versioned submission-final repository}. Full financial replay additionally requires the exact original inputs and documented historical Git objects. [AUTHOR TO ADD ZENODO DOI AND CONFIRM SOFTWARE LICENSE].

\textbf{Existing versions and exclusive submission:} GitHub working versions are disclosed in the cover letter. [AUTHOR TO CONFIRM OTHER VERSIONS, ALL-AUTHOR APPROVAL AND EXCLUSIVE SUBMISSION].
'''
    save(OUT/'declarations.tex',PRE+declarations+'\n\\end{document}\n')
    md=(ROOT/'notes/submission/candidate-reviewers.md').read_text()
    rows=[line.split('|')[1:-1] for line in md.splitlines() if line.startswith('|')][2:]
    assert len(rows)==5
    sections=[r'\section*{Potential reviewers: author confirmation required}',
        'No candidate has been contacted. Institutional identity and subject expertise were checked against official pages. '
        'Availability, conflicts, institutional email and journal eligibility require the author\'s confirmation. '
        'Author names and affiliations: [TO BE COMPLETED BY AUTHOR].']
    for cells in rows:
        name,role,reason,evidence,email,conflict=[x.strip() for x in cells]
        sections += [r'\subsection*{'+inline(name)+'}',inline(role),inline(reason),inline(evidence),
            r'\textbf{Email:} '+inline(email)+r'. \textbf{Conflicts:} '+inline(conflict)+'.']
    sections += ['Giacomini and Koenker share UCL affiliations; Gneiting and Krueger share KIT affiliations and have coauthored work. '
                 'The author should consider institutional breadth and all relevant relationships before selecting any subset.']
    save(OUT/'suggested-reviewers.tex',PRE+'\n\n'.join(sections)+'\n\\end{document}\n')
    md=(ROOT/'notes/submission/author-qa.md').read_text()
    # Abbreviate commit identities in this reading copy; full hashes remain in Markdown.
    md=re.sub(r'\b([0-9a-f]{12})[0-9a-f]{28}\b',r'\1',md)
    parts=[]
    for paragraph in re.split(r'\n\s*\n',md):
        if paragraph.startswith('# '):parts.append(r'\section*{'+inline(paragraph[2:])+'}')
        elif paragraph.startswith('## '):parts.append(r'\subsection*{'+inline(paragraph[3:])+'}')
        else:parts.append(inline(paragraph.replace('\n',' ')))
    cjk_pre=PRE.replace(r'\usepackage[T1]{fontenc}',
        r'\usepackage{fontspec}'+'\n'+
        r'\setmainfont{Arial Unicode.ttf}[Path=/System/Library/Fonts/Supplemental/]'+'\n'+
        r'\XeTeXlinebreaklocale "zh"'+'\n'+r'\XeTeXlinebreakskip=0pt plus 1pt')
    save(OUT/'author-qa.tex',cjk_pre+'\n\n'.join(parts)+'\n\\end{document}\n')
    records=[]
    for name in ['declarations','suggested-reviewers','author-qa']:
        build=ROOT/'.scratch/submission/shared'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')/name
        build.mkdir(parents=True)
        command=[TEX,'-X','compile','-C',str(OUT/(name+'.tex')),'--outdir',str(build),'--keep-logs','--keep-intermediates']
        q=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (build/'console.txt').write_text(q.stdout);assert q.returncode==0,q.stdout
        log=(build/(name+'.log')).read_text()
        bad=re.findall(r'Overfull[^\n]*|(?:Reference|Citation)[^\n]*undefined|Missing character[^\n]*',log);assert not bad,bad
        pdf=OUT/(name+'.pdf');backup(pdf);shutil.copyfile(build/(name+'.pdf'),pdf)
        records.append(dict(name=name,tex_sha256=sha(OUT/(name+'.tex')),pdf_sha256=sha(pdf),pages=len(PdfReader(pdf).pages),command=command,log=str((build/'console.txt').relative_to(ROOT))))
        print(name,records[-1]['pages'],'pages',flush=True)
    path=ROOT/'notes/submission/shared-build.json';backup(path);path.write_text(json.dumps(records,indent=2)+'\n')

if __name__=='__main__':main()
