#!/usr/bin/python3
"""Presentation-only relocation of saved text; no numerical analysis."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,shutil
R=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
text=(N/'supplement-before-R5-expanded.tex').read_text()
items=json.loads((N/'R5-old-section-inventory.json').read_text())['sections']
B={x['old_section']:text[x['start']:x['end']] for x in items}
URL='https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/EXTENDED_RESULTS.md'
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_text()==data:return
        shutil.copy2(path,path.with_name(path.name+'.'+stamp+'.bak'))
    path.write_text(data)
archive=R/'evidence/asmbi-final-20261027/supplement-expanded-before-condense.tex'
if archive.exists():assert archive.read_text()==text
else:write(archive,text)
old_index=N/'EXTENDED_RESULTS-before-R5.md'
if old_index.exists():original_index=old_index.read_text()
else:
    original_index=(R/'EXTENDED_RESULTS.md').read_text();write(old_index,original_index)
fence=chr(96)*3;tick=chr(96)
parts=['# ASMBI final: complete extended results\n\nThe compact supplement retains proofs, methods, source summaries and all saved decision outcomes. This index preserves the complete preceding supplement, including every cell, adverse result, failure and counterexample. Numbered blocks below belong to that preceding version, not the new supplement. No forecast, model fit, score or saved judgment was recomputed.\n\n[Exact expanded source](evidence/asmbi-final-20261027/supplement-expanded-before-condense.tex). SHA-256: '+tick+hashlib.sha256(text.encode()).hexdigest()+tick+'.\n\n']
for x in items:parts.append(f"- [Earlier S{x['old_section']}: {x['title']}](#asmbi-extended-s{x['old_section']:02})\n")
parts.append('\n## Earlier archive index\n\n'+original_index+'\n')
for x in items:
    number=x['old_section'];parts.append(f'\n<a id="asmbi-extended-s{number:02}"></a>\n\n## ASMBI extended S{number:02}: {x["title"]}\n\n'+fence+'latex\n'+B[number]+'\n'+fence+'\n')
write(R/'EXTENDED_RESULTS.md',''.join(parts))
mapping={1:1,2:1,3:4,4:4,5:4,6:5,7:2,8:2,9:9,10:9,11:6,12:6,13:6,14:6,15:6,16:2,17:5,18:2,19:9,20:5,21:11,22:2,23:2,24:4,25:5,26:5,27:4,28:4,29:4,30:3,31:8,32:9,33:9,34:11,35:7,36:11,37:8,38:10,39:7,40:12}
def content(number):
    body=B[number];m=re.match(r'\\section\{[^}]+\}\\label\{[^}]+\}',body);assert m,number
    body=body[m.end():].strip();body=re.sub(r'\\(?:clearpage|FloatBarrier)\s*$','',body).strip()
    return body
def intro(number):
    body=content(number)
    stops=[body.find(token) for token in (r'\begingroup',r'\begin{table}',r'\begin{center}',r'\begin{longtable}')]
    stops=[x for x in stops if x>=0]
    return body[:min(stops)].strip() if stops else body
def link(number,label='complete earlier results'):
    return r'\href{'+URL+f'#asmbi-extended-s{number:02}'+'}{'+label+'}'
def section(number,title,body):
    labels=[x['label'] for x in items if mapping[x['old_section']]==number and x['label']]
    return '\\section{'+title+'}'+''.join('\\label{'+x+'}' for x in labels)+'\n\n'+body.strip()+'\n\n\\FloatBarrier\n\n'
s1=content(1)+'\n\n'+content(2)
s2=content(23)+'\n\n'+intro(8)+'\n\n'+intro(7)+'\n\n'+intro(16)+'\n\n'+intro(18)+'\n\n'+intro(22)
s2=re.sub(r'Table S7 reports[^.]+\.',lambda m:'The full rank comparison is retained in '+link(8)+'.',s2)
s2=re.sub(r'Tables? S[0-9]+(?:--S[0-9]+)?[^.]*\.',lambda m:'The complete comparison is retained in the extended result archive.',s2)
data=(R/'submission-final/generated/v12-data-table.tex').read_text()
panel=data[data.index(r'\textit{Panel A.'):data.index(r'\par\vspace{7pt}')]
s3=r'''The source units and chronological samples are retained below. Monetary summaries and complete within-series statistics remain in Main Table 2; contract counts are not pooled with currency exposures.
\begin{table}[htbp]\centering
\caption{Sources, sample sizes and existing chronological splits.}\label{tab:supplement-data}
\begingroup\fontsize{7.5}{9}\selectfont\setlength{\tabcolsep}{2pt}
'''+panel+r'''\endgroup\end{table}

'''+content(30)
s3=s3[:s3.find('Two narrow official-format clarifications')].rstrip()+'\n\nThe complete ingestion chronology, exclusions and original failed preparation records remain in '+link(30)+'.'
s4=content(24);s4=s4[:s4.index(r'\paragraph{Candidate and procedure statuses.}')].rstrip()
s4+='\n\nOne declared candidate failed its numerical criterion; the fixed completed-candidate selector retained that failure and selected an eligible completed alternative. The original full-regression selector requires every declared candidate. '+link(24,'All candidate and procedure statuses')+' retain the complete numerical details.'
s4+='\n\n'+intro(3)+'\n\n'+intro(4)+'\n\n'+intro(5)
menu=content(29)
cut=menu.index(r'\begin{figure}') if r'\begin{figure}' in menu else len(menu)
menu=menu[:cut]
s4+='\n\n'+menu+'\n\n'+link(27,'The legacy calibrated simulation and every failed cell')+', '+link(28,'all stability and switching cases')+', and '+link(29,'all menu-isolation cells')+' remain unchanged.'
s5=content(25)+'\n\n'+intro(6)+'\n\n'+intro(20)+'\n\n'+intro(17)
s5+='\n\nThe fixed-prefix comparison overlaps the earlier inspected period. '+link(26,'Every full-prefix and overlapping-window result')+' remains available; these records are not an independent financial holdout.'
s6=intro(11)+'\n\n'+intro(14)+'\n\n'+intro(15)
s6+='\n\nThe expanded penalty menu reduces the earlier full-regression losses but does not satisfy all written improvement conditions. The earlier conservative selection also fails its protection, gain-retention and median-improvement conditions. '+link(11,'Both halves of the complete weekly panel')+', '+link(13,'every endpoint-plug-in comparison')+', and '+link(14,'all earlier selection outcomes')+' retain the adverse rows and unchanged denominators.'
s7=content(35)
wp2=content(39).split(r'\paragraph{Complete counterexample inventory.}')[0].rstrip()
s7+='\n\n'+wp2+'\n\n'+link(39,'Every saved CFTC counterexample, with its original signed loss change')+' remains alongside the complete source rows. Markets can appear under several screens; ties remain failures of strict ordering.'
s8=content(37);s8=s8.replace('Supplement Section S31',link(31,'the complete confidence-set archive'))
s9=intro(9)+'\n\n'+content(32)
diag=content(33);figures=re.findall(r'\\begin\{figure\}(?:\[[^]]*\])?.*?\\end\{figure\}',diag,re.S);assert len(figures)==2
s9+='\n\n'+''.join(figures)+'\n\n'+link(9,'All original fixed-report error amounts and weight crossings')+' and '+link(19,'all combination-score crossings')+' retain the complete comparisons.'
s10=content(38);a=s10.index(r'\paragraph{Post-failure solver check.}');b=s10.index(r'\paragraph{Longer validation in the New York Fed series.}');s10=s10[:a]+s10[b:]
s10=re.sub(r'\\begin\{table\}(?:\[[^]]*\])?.*?\\label\{tab:v13-validation\}.*?\\end\{table\}',lambda m:'The complete validation summary is in Main Table 7.\n',s10,flags=re.S)
s10=re.sub(r'\\begin\{figure\}(?:\[[^]]*\])?.*?\\end\{figure\}',lambda m:'The unchanged source-by-source validation plot is retained in '+link(38)+'.\n',s10,flags=re.S)
s10=s10.replace(r'Table~\ref{tab:v13-validation}','Main Table 7').replace(r'Figure~\ref{fig:v13-validation}',link(38,'The complete source-by-source plot'))
repair=content(38).split(r'\paragraph{Post-failure solver check.}',1)[1].split(r'\paragraph{Longer validation in the New York Fed series.}',1)[0].strip()
s11=repair+'\n\nThe original FX evaluation period was inspected before the conditional extension. Later written designs retain their own local-commit and public-upload chronology; public posting after calculation is not public preregistration. Complete audit and execution records remain in '+link(36)+', '+link(38)+', and '+link(39)+'.\n\nThe repository provides the code, protocols, saved aggregate results and source acquisition instructions. Financial replay still requires the documented compatible raw inputs and historical code; public summaries alone do not supply those inputs.'
full=(R/'submission-final/generated/submission-predictions.tex').read_text()
rows=[]
for m in re.finditer(r'% row_id: ([^\n]+)\n([^\n]+)',full):
    row_id,line=m.groups();cells=re.split(r'(?<!\\)&',line);assert len(cells)==6,(row_id,len(cells))
    rows.append({'row_id':row_id,'criterion_tex':cells[1].strip()+r'\par\emph{Threshold:} '+cells[2].strip(),'judgment':cells[4].strip().split(r'\par')[0].strip()})
assert len(rows)==36
compact=[r'\begin{longtable}{p{2.0cm}p{10.5cm}p{2.5cm}}',r'\caption{Every saved written prediction and decision. Full numerical outputs, exact status reasons and source bindings remain in the extended result archive.}\label{tab:submission-predictions}\\',r'\toprule Screen & Written criterion & Saved judgment\\\midrule\endfirsthead',r'\toprule Screen & Written criterion & Saved judgment\\\midrule\endhead']
for row in rows:
    label=row['row_id'].replace('.',r'.\allowbreak{}').replace('+',r'\ensuremath{+}').replace('_',r'\_')
    compact.append(r'\texttt{'+label+'} & '+row['criterion_tex']+' & '+row['judgment']+r' \\[3pt]')
compact.append(r'\bottomrule\end{longtable}')
s12='These decisions are copied from the saved register, including every unsupported and undetermined screen. Written-before-run status is distinct from external preregistration and prospective financial evaluation. The full threshold, numerical output, original status, timing record and source pointer for every row remain in '+link(40,'the complete six-column register')+'.\n\n{\\footnotesize\n'+'\n'.join(compact)+'\n}\n'
write(N/'R5-compact-register-bindings.json',json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
sections=[(1,'Peak properties and their proofs',s1),(2,'Forecast construction and comparison methods',s2),(3,'Sources, chronological samples and reporting dates',s3),(4,'Fixed simulation designs and retained failures',s4),(5,'FX aggregation and additional forecast comparisons',s5),(6,'Weekly historical rules retain their adverse comparisons',s6),(7,'History-length predictions have partial support',s7),(8,'Historical methods remain in most confidence sets',s8),(9,'Scores, breaches and specified limit costs',s9),(10,'Longer validation improves medians but leaves losses',s10),(11,'Numerical rejection and retrospective timing',s11),(12,'Written predictions and saved judgments',s12)]
def update_old_refs(body):
    body=re.sub(r'Supplement Sections? S\d+(?:(?:--| and |, )S?\d+)*',lambda m:'the extended result archive',body)
    body=re.sub(r'(?<!v9 )Tables? S\d+(?:(?:--| and |, )S?\d+)*',lambda m:'the original tables in the extended result archive',body)
    return body
preamble=text[:text.index(r'\begin{document}')]
opening=r'''\begin{document}
\maketitle
This supplement contains proofs, reproducible method definitions, source summaries and every saved decision. The complete preceding supplement, including all cell tables, failed numerical attempts and counterexamples, is preserved in \href{'''+URL+r'''}{EXTENDED RESULTS}. No financial analysis or saved result is changed by this shorter presentation.
\setcounter{tocdepth}{1}
\tableofcontents
\medskip
'''
new=preamble+opening+'\n'.join(section(i,title,update_old_refs(body)) for i,title,body in sections)+r'\end{document}'+'\n'
new=re.sub(r'\\(?:addtocounter|setcounter)\{(?:table|figure|section)\}\{[^}]+\}','',new)
write(R/'submission-final/supplement.tex',new)
write(N/'R5-section-map.json',json.dumps({'old_to_new_section':mapping,'new_sections':[{'number':i,'title':title} for i,title,_ in sections],'archived_source':str(archive.relative_to(R)),'archived_source_sha256':hashlib.sha256(text.encode()).hexdigest(),'complete_old_sections':len(items),'new_section_count':len(sections)},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'SOURCE_CONDENSED_PENDING_COMPILE','old_sections':len(items),'new_sections':len(sections),'all_old_sections_preserved_in_extended':True,'compact_register_rows':len(rows),'source_chars':len(new)},ensure_ascii=False))
