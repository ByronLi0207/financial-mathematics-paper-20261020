"""S7: format individually verified publication records, without BibTeX downloads."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def escape(value):
    value=str(value).replace("’","'").replace("–","--").replace("—","---")
    return value.replace("&",r"\&").replace("%",r"\%").replace("_",r"\_")


def titlecase(value):
    result=value.lower()
    if result:result=result[0].upper()+result[1:]
    result=re.sub(r"(:\s+)([a-z])",lambda m:m.group(1)+m.group(2).upper(),result)
    for name in ("MaxVaR","CAViaR","VaR","GARCH","U.S.","Treasury","FR 2004","ACSS","Orlicz","Pettis","Itô","Nisio"):
        result=re.sub(r"(?<![A-Za-z])"+re.escape(name)+r"(?![A-Za-z])",name,result,flags=re.I)
    return result


def authors(names):
    if len(names)==1:return escape(names[0])
    if len(names)==2:return escape(names[0])+r", \& "+escape(names[1])
    return ", ".join(map(escape,names[:-1]))+r", \& "+escape(names[-1])


def label(record):
    surnames=[escape(name.split(",")[0]) for name in record["authors"]]
    who=surnames[0] if len(surnames)==1 else r" \& ".join(surnames) if len(surnames)==2 else surnames[0]+" et al."
    return who+"("+record["year"]+")"


def main():
    records=[]
    for path in sorted((HERE/'reference-parts').glob('*.json')):records.extend(json.loads(path.read_text()))
    final=[]
    for record in records:
        if record['key']=='fr2004':
            for edition in record['editions']:
                r=dict(record);r.update(key='fr2004_'+edition['year'],year=edition['year'],month=edition['month'],
                    title=edition['title'],url=edition['url'],type='institutional_report');r.pop('editions');final.append(r)
        else:final.append(record)
    data_path=HERE/'main-v7-sections.json';data=json.loads(data_path.read_text())
    for section in data['sections']:
        for block in section['blocks']:
            if 'tex' in block:block['tex']=block['tex'].replace(r'\citep{fr2004}',r'\citep{fr2004_2013,fr2004_2024}')
    data_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    keys={key.strip() for match in re.findall(r'\\cite(?:p|t|alp)?\{([^}]+)\}',json.dumps(data)) for key in match.split(',')}
    bykey={r['key']:r for r in final};assert len(bykey)==len(final);assert keys==set(bykey),(sorted(keys-set(bykey)),sorted(set(bykey)-keys))
    final.sort(key=lambda r:(r['authors'][0].casefold(),r['year'],r['title']))
    bib=[];tex=[];audit=['# S7 reference verification','','Metadata are verified against the linked owning/publisher records; empty optional DOI fields are deliberately omitted. This is not a full-text-method replication claim.','','| Key | Status | Author/year/venue/volume/issue/pages | DOI | Evidence |','|---|---|---|---|---|']
    for r in final:
        assert r['status'] in ('verified','corrected','unverified') and r['evidence_urls']
        r['apa_title']=titlecase(r['title'])
        typ=r['type'];article=typ in ('article','journal_article');kind='article' if article else 'inproceedings' if typ in ('conference_paper','inproceedings') else 'phdthesis' if typ=='doctoral_thesis' else 'mastersthesis' if typ=='masters_thesis' else 'misc'
        bibnames=[]
        for name in r['authors']:
            if ',' not in name:bibnames.append('{'+name+'}')
            elif name.endswith(', Jr.'):
                surname,given=name[:-5].split(',',1);bibnames.append(surname+', Jr., '+given.strip())
            else:bibnames.append(name)
        fields={'author':' and '.join(bibnames),'title':r['apa_title'],'year':r['year']}
        if r.get('month'):fields['month']=r['month']
        for key in ('volume','issue','pages','doi','url'):
            if r.get(key):fields['number' if key=='issue' else key]=r[key]
        fields['journal' if article else 'booktitle' if typ in ('conference_paper','inproceedings') else 'institution']=r['venue']
        bib.append('@'+kind+'{'+r['key']+',\n'+',\n'.join('  '+key+' = {'+escape(value)+'}' for key,value in fields.items())+'\n}\n')
        head=authors(r['authors'])+' ('+escape(r['year'])+(', '+escape(r['month']) if r.get('month') else '')+'). '
        title=escape(r['apa_title'])
        if article or typ=='inproceedings':
            body=head+title+'. '+r'\emph{'+escape(r['venue'])+'}'
            if r.get('volume'):body+=', '+r'\emph{'+escape(r['volume'])+'}'
            if r.get('issue'):body+='('+escape(r['issue'])+')'
            if r.get('pages'):body+=', '+escape(r['pages'])
            body+='.'
        elif typ=='conference_paper':
            body=head+title+'. In '+r'\emph{'+escape(r['venue'])+'}'
            if r.get('volume'):body+=' (Proceedings of Machine Learning Research, Vol. '+escape(r['volume'])+', pp. '+escape(r['pages'])+').'
            else:body+='.'
        else:
            body=head+r'\emph{'+title+'}'
            if typ=='dataset':body+=(' (Version '+escape(r['version'])+')' if r.get('version') else '')+' [Data set].'
            elif typ in ('doctoral_thesis','masters_thesis'):body+=' ['+('Doctoral' if typ=='doctoral_thesis' else "Master's")+' thesis, '+escape(r['venue'])+'].'
            elif r.get('number'):body+=' ('+('Staff Report' if r['key']=='duffie2023' else 'Discussion Paper')+' No. '+escape(r['number'])+').'
            else:body+='.'
            if typ not in ('doctoral_thesis','masters_thesis'):body+=' '+escape(r['venue'])+'.'
        if r.get('doi'):body+=r' \url{https://doi.org/'+r['doi']+'}.'
        else:body+=r' \url{'+r['url']+'}.'
        if r.get('retrieved'):body+=' Retrieved '+escape(r['retrieved'])+'.'
        tex.append(r'\bibitem['+label(r)+']{'+r['key']+'} '+body+'\n')
        cells='; '.join(r['authors'])+'; '+'; '.join(str(r.get(key) or 'n.a.') for key in ('year','venue','volume','issue','pages'))
        audit.append('| '+r['key']+' | '+r['status']+' | '+cells.replace('|','/')+' | '+str(r.get('doi') or 'omitted: unverified / none supplied')+' | '+', '.join('[source]('+url+')' for url in r['evidence_urls'])+' |')
    (ROOT/'submission-jof/references.bib').write_text('\n'.join(bib))
    (HERE/'references-v7.tex').write_text(r'\begin{thebibliography}{99}'+'\n'+'\n'.join(tex)+r'\end{thebibliography}'+'\n')
    (HERE/'references-verified.json').write_text(json.dumps(final,indent=2,ensure_ascii=False)+'\n')
    (HERE/'reference-verification-table.md').write_text('\n'.join(audit)+'\n')
    availability=r'''\section*{Data and code availability}
\paragraph{Data availability.} The FX input is the specified version of the Kaggle Net Position Time Series Dataset. The owning metadata labels its license ``Data files \copyright\ Original Authors.'' This repository supplies the acquisition route and input fingerprint, but excludes raw FX observations and private per-issue prediction vectors. Obtain the source from \url{https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset} subject to the original rights holders' terms.

The New York Fed aggregates are available from its Primary Dealer Statistics service under the Bank's Terms of Use. The repository preserves the unchanged accepted Treasury snapshot with attribution and identifies study calculations separately. Copying or distributing that content remains subject to its source notices, attribution, modification labelling, continuing conditions and endorsement restrictions: \url{https://www.newyorkfed.org/privacy/termsofuse.html}. The code license does not replace those source conditions.

\paragraph{Code availability.} Code, saved results and version-specific reproduction instructions are available at \url{https://github.com/ByronLi0207/financial-mathematics-paper-20261020}. This revision adds no new financial experiment. The completed results include adverse, failed and unavailable cases.

\section*{Author-provided information}
Author information: [TO BE COMPLETED BY AUTHOR].\par
ORCID: [TO BE COMPLETED BY AUTHOR].\par
Funding: [TO BE COMPLETED BY AUTHOR].\par
Competing interests: [TO BE COMPLETED BY AUTHOR].\par
AI statement: [TO BE COMPLETED BY AUTHOR].
'''
    (HERE/'availability-v7.tex').write_text(availability)
    report=dict(status='PASS',cited_keys=len(keys),reference_entries=len(final),missing_references=[],unused_entries=[],
                verified=sum(r['status']=='verified' for r in final),corrected=sum(r['status']=='corrected' for r in final),
                unverified=sum(r['status']=='unverified' for r in final),dois_printed=sum(bool(r.get('doi')) for r in final),
                doi_omitted=sum(not r.get('doi') for r in final),author_fields_filled=0)
    (HERE/'s7-reference-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
