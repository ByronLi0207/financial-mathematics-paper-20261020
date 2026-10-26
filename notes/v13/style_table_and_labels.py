"""v13 display-only formatting. Reads saved text/scalars; no forecast or score."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,shutil,datetime
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'submission-v10'
NOTES=ROOT/'notes/v13'
BEFORE=ROOT/'.scratch/v13/editorial-before/source'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def displayed(token):
    token=token.strip()
    m=re.fullmatch(r'\$([\d.]+)\\!\\times\\!10\^\{(-?\d+)\}\$',token)
    return Decimal(m[1])*(Decimal(10)**int(m[2])) if m else Decimal(token.replace(',',''))
def sig3(n):
    d=displayed(n);places=2-d.adjusted();return format(d,f',.{max(0,places)}f')

def table():
    p=DOC/'generated/v12-data-table.tex';s=p.read_text();start=s.index('Data & Mean & SD');old=[]
    for line in s[start:].splitlines():
        if '&' not in line or line.startswith('Data'):continue
        cells=[x.strip() for x in line.removesuffix('\\\\').split('&')]
        if len(cells)==10:old.append((cells[0],cells[1:]))
    assert len(old)==5
    rows=[('FX, hourly','Hourly','1 / 18,576','USD mn','2014-02 to 2017-01','2015-10 to 2015-12','2016-01 to 2017-01'),('FX, daily','Day end','1 / 930','USD mn','2014-02 to 2017-01','2015-02 to 2015-04','2015-05 to 2016-12'),('Treasury bills','Weekly','1 / 706','USD mn','2013-04 to 2026-10','2019-07 to 2020-07','2021-01 to 2026-04'),('NY Fed panel','Weekly','12 / 706','USD mn','2013-04 to 2026-10','2019-07 to 2020-07','2021-01 to 2026-04'),('CFTC panel','Weekly','17 / 877','Contracts','2010-01 to 2026-10','2020-08 to 2021-08','2021-09 to 2026-09')]
    lines=[r'\begin{table}[!htbp]',r'\centering',r'\caption{Data and matched six-record peak summaries.}\label{tab:v12-data}',r'\begingroup\fontsize{7.5}{9}\selectfont\setlength{\tabcolsep}{2pt}',r'\textit{Panel A. Sources, aligned samples and existing split dates}\\[3pt]',r'\begin{tabular}{@{}lllllll@{}}',r'\toprule',r'Data & Frequency & Series / records & Unit & Sample & Validation & Evaluation \\',r'\midrule']
    lines += [' & '.join(row)+r' \\' for row in rows]
    lines += [r'\bottomrule',r'\end{tabular}',r'\par\vspace{7pt}',r'\textit{Panel B. Within-series mean, sample SD and empirical 95th percentile}\\[3pt]',r'\begin{tabular}{@{}ll*{9}{r}@{}}',r'\toprule',r' & & \multicolumn{3}{c}{$|N|$} & \multicolumn{3}{c}{Peak $Y$} & \multicolumn{3}{c}{Headroom $Z$} \\',r'\cmidrule(lr){3-5}\cmidrule(lr){6-8}\cmidrule(lr){9-11}',r'Data & Unit & Mean & SD & 95th & Mean & SD & 95th & Mean & SD & 95th \\',r'\midrule']
    comparisons=[]
    for i,(name,tokens) in enumerate(old):
        shown=[sig3(t) for t in tokens]
        for j,(a,b) in enumerate(zip(tokens,shown)):
            assert displayed(a)==displayed(b),(name,j,a,b)
            comparisons.append(dict(row=name,column=j+1,before=a,after=b,numeric_equal=True))
        lines.append(' & '.join([name,rows[i][3],*shown])+r' \\')
    lines += [r'\bottomrule',r'\end{tabular}',r'\endgroup',r'\begin{minipage}{.98\linewidth}\footnotesize\emph{Notes.} Records are per series; complete $H=6$ peak counts are 18,570, 924, 700, 700 and 871, respectively, including the issue anchor. Earlier hourly FX validation spans 2015-04 to 2015-07 and evaluation spans 2015-07 to 2015-10; daily FX uses each nonempty source-naive day\textquotesingle s last record, and both FX periods had been inspected. SD uses $m-1$ and the empirical 95th percentile has rank $\lceil95m/100\rceil$; dollar values are in millions, panel entries are separate within-series medians without exposure pooling, and CFTC retains heterogeneous native contract counts.\end{minipage}',r'\end{table}']
    after='\n'.join(lines)+'\n';p.write_text(after)
    return dict(path=str(p.relative_to(ROOT)),before_sha256=sha(BEFORE/p.relative_to(DOC)),after_sha256=sha(p),statistics_compared=45,all_equal=True,cells=comparisons,panel_A=rows,date_format='YYYY-MM; earlier FX dates retained in note',complete_peak_counts=[18570,924,700,700,871])

def clean(s,file):
    edits=[];out=[];method=False
    for n,line in enumerate(s.splitlines(),1):
        if line.startswith('%'):out.append(line);continue
        if file=='manuscript.tex' and r'\label{tab:methods}' in line:method=True
        if method:
            out.append(line)
            if r'\end{table}' in line:method=False
            continue
        urls=[]
        def hold(m):
            urls.append(m[0]);return f'@@URL{len(urls)-1}@@'
        t=re.sub(r'\\(?:href|url)\{[^}]+\}',hold,line)
        t=t.replace(' (result codes QR33, QR4 and QR33+, respectively)','')
        t=t.replace('finite delayed ACI-style F/QR33','finite delayed calibration of historical headroom and full regression')
        t=t.replace('full and four-feature regression correspond to QR33 and QR4','the two regression variants retain their stated predictor sets')
        t=t.replace('Unchanged full method ID','Procedure and source context')
        replacements=[(r'\bregistered\b','pre-specified'),(r'\bfrozen\b','fixed'),(r'\bunverified\b','unestablished'),(r'\bunused allowance\b','mean overprediction'),(r'\breadbacks?\b','data record'),(r'\baudits?\b','reproduction'),(r'\barchived\b','saved'),(r'\barchives?\b','records'),(r'\bQR33\b','full regression'),(r'\bQR4\b','four-feature regression')]
        for pat,word in replacements:
            def sub(m):
                return word[0].upper()+word[1:] if m[0][0].isupper() and m[0].lower() not in ('qr33','qr4') else word
            t=re.sub(pat,sub,t,flags=re.I)
        for i,url in enumerate(urls):t=t.replace(f'@@URL{i}@@',url)
        if t!=line:edits.append(dict(file='submission-v10/'+file,line_before=n,before=line,after=t))
        out.append(t)
    return '\n'.join(out)+'\n',edits

def main():
    record=table();edits=[]
    inventory=json.loads((NOTES/'editorial-inventory.json').read_text())
    for name in inventory['inspected_tex']:
        if name=='generated/v12-data-table.tex':continue
        p=DOC/name;s=p.read_text();after,changes=clean(s,name)
        if changes:p.write_text(after);edits.extend(changes)
    output=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),table=record,visible_line_edits=edits,line_edit_count=len(edits),exceptions=['T1 font encoding is LaTeX syntax, not a response-design label.','QR4 in the main methods table is permitted.','Nonprinting provenance comments and URL argument bytes are preserved.'])
    (NOTES/'G1-formatting-check.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(table_statistics=45,all_equal=True,edited_lines=len(edits))))
if __name__=='__main__':main()
