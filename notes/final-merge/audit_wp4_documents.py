"""Count the current manuscript and verify relocated/new displayed fields."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'submission-final'
TOKEN=r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:\.\d+)?(?:/\d+)?"


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def expand(path,chain=()):
    path=path.resolve()
    if path in chain:raise ValueError('cyclic TeX input')
    if not path.is_relative_to(BASE):raise ValueError('input leaves final source tree')
    text=path.read_text()
    def sub(m):
        p=BASE/m.group(1)
        return expand(p if p.suffix else p.with_suffix('.tex'),chain+(path,))
    return re.sub(r'\\input\{([^}]+)\}',sub,text)


def prose(raw,exclude_tables=True):
    raw=re.sub(r'(?<!\\)%[^\n]*','',raw)
    if exclude_tables:raw=re.sub(r'\\begin\{(table|longtable)\}.*?\\end\{\1\}',' ',raw,flags=re.S)
    raw=re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$[^$]*\$',' ',raw,flags=re.S)
    raw=re.sub(r'\\(?:cite\w*|label|ref|eqref|url|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}',' ',raw)
    raw=re.sub(r'\\href\{[^}]*\}\{([^}]*)\}',r'\1',raw)
    raw=re.sub(r'\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?',' ',raw)
    raw=re.sub(r'\\[A-Za-z]+\*?(?:\[[^\]]*\])?',' ',raw)
    return raw.replace('{',' ').replace('}',' ')


def main_number_audit(text,summary):
    """Check actual current-main rows, not merely the supplemental display."""
    errors=[];checks=[]
    source=json.loads((ROOT/'notes/revision-v9/wp1-breakeven.json').read_text())
    for method,decimals in [('QR33',1),('QR4',1)]:
        value=source['methods'][method]['point']['r_star'];token=format(value,f'.{decimals}f')
        if '$'+token+'$' not in text:errors.append(dict(kind='DISCOVERY_DISPLAY',method=method,expected=token))
        checks.append(dict(source='notes/revision-v9/wp1-breakeven.json',pointer=f'/methods/{method}/point/r_star',value=value,display=token))
        for end in ('lower','upper'):
            value=source['methods'][method]['intervals']['all_draw_envelope'][end];token=format(value,'.2f')
            if '$'+token+'$' not in text:errors.append(dict(kind='INTERVAL_DISPLAY',method=method,end=end,expected=token))
            checks.append(dict(source='notes/revision-v9/wp1-breakeven.json',pointer=f'/methods/{method}/intervals/all_draw_envelope/{end}',value=value,display=token))
    block=next(t for t in re.findall(r'\\begin\{table\}.*?\\end\{table\}',text,re.S) if r'\label{tab:cftc-mechanism}' in t)
    rows=[line for line in block.splitlines() if re.match(r'^P[123] & ',line)]
    settings=[('P1_QR33','P1','Full regression','Supported'),('P1_QR4','P1','Four predictors','Supported'),
        ('P2_QR4','P2','Four predictors','Not supported'),('P2_QR33','P2','Full regression','Not testable'),
        ('P3_QR4','P3','Four predictors','Not supported')]
    if len(rows)!=5:errors.append(dict(kind='MAIN_PREDICTION_CENSUS',observed=len(rows)))
    for row,(key,name,method,status) in zip(rows,settings):
        cells=[c.strip() for c in re.sub(r'\\\\\s*$','',row).split('&')];r=summary['tests'][key]
        expected=r'$'+str(r['successes'])+'/'+str(r['planned'])+'$' if r['planned'] else 'NA'
        if len(cells)!=5 or cells[0]!=name or cells[1]!=method or cells[3]!=expected or cells[4]!=status:
            errors.append(dict(kind='MAIN_PREDICTION_ROW',key=key,expected_count=expected,expected_verdict=status,actual=cells))
        checks.append(dict(source='results/final-merge/wp2-cftc-mechanism/summary.json',pointer='/tests/'+key,value=r,displayed_count=expected,displayed_status=status))
    if summary['primary_verdict']!='PARTLY' or 'primary verdict is partial agreement' not in text:
        errors.append(dict(kind='MAIN_PRIMARY_VERDICT'))
    # Original inline parameter/results tables retain each scientific numeric
    # token. Only section-ID/URL prose changes are normalized away.
    baseline=(ROOT/'submission-v10/manuscript.tex').read_text()
    def numbers(table):
        lines='\n'.join(line for line in table.splitlines() if '&' in line)
        lines=re.sub(r'\\href\{[^}]*\}', '',lines);lines=re.sub(r'\bS\d+\b','SREF',lines)
        return re.findall(r'[-+]?\d+(?:\.\d+)?',lines)
    for label in ('tab:methods','tab:fx','tab:weekly'):
        old=next(t for t in re.findall(r'\\begin\{table\}.*?\\end\{table\}',baseline,re.S) if '\\label{'+label+'}' in t)
        new=next(t for t in re.findall(r'\\begin\{table\}.*?\\end\{table\}',text,re.S) if '\\label{'+label+'}' in t)
        if numbers(old)!=numbers(new):errors.append(dict(kind='ORIGINAL_INLINE_TABLE_NUMBERS',label=label,old=numbers(old),new=numbers(new)))
        checks.append(dict(original_table=label,numeric_tokens=len(numbers(old)),unchanged=numbers(old)==numbers(new)))
    return errors,checks


def audit(main_pdf,supp_pdf,main_log,supp_log):
    from pypdf import PdfReader
    raw=expand(BASE/'manuscript.tex');body=raw.split(r'\begin{document}',1)[1].split(r'\begin{thebibliography}',1)[0]
    matches=list(re.finditer(r'\\section\*?\{([^}]+)\}',body));sections=[]
    first=matches[0].start() if matches else len(body)
    sections.append(dict(section='Title, abstract and front matter',words=len(re.findall(TOKEN,prose(body[:first])))))
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(body)
        sections.append(dict(section=m.group(1),words=len(re.findall(TOKEN,prose(body[m.start():end])))))
    words=sum(r['words'] for r in sections)
    reader=PdfReader(main_pdf);pdftext='\n'.join(p.extract_text() for p in reader.pages)
    ref=re.search(r'(?m)^References\s*$',pdftext)
    if ref is None:raise ValueError('References boundary absent from compiled PDF')
    pdf_upper=len(re.findall(TOKEN,pdftext[:ref.start()]));source_upper=len(re.findall(TOKEN,body))
    counts=dict(main_words_excluding_tables_references=words,per_section_words=sections,
        conservative_source_tokens_including_table_tex=source_upper,
        pdf_words_before_references_including_tables_captions_axes=pdf_upper,
        main_pages=len(reader.pages),supplement_pages=len(PdfReader(supp_pdf).pages),
        main_tables=len(re.findall(r'\\begin\{table\}',raw)),main_figures=len(re.findall(r'\\begin\{figure\}',raw)))
    errors=[]
    for key,limit in [('main_words_excluding_tables_references',9000),('main_tables',6),('main_figures',4),('supplement_pages',30)]:
        if counts[key]>limit:errors.append(dict(kind='CAP',field=key,observed=counts[key],limit=limit))
    logs={}
    for name,path in [('main',main_log),('supplement',supp_log)]:
        text=path.read_text();bad=re.findall(r'Overfull[^\n]*|(?:Reference|Citation)[^\n]*undefined|Label[^\n]*multiply defined|^![^\n]*',text,re.M)
        logs[name]=dict(bad_diagnostics=bad,underfull_warning_count=text.count('Underfull'),sha256=sha(path))
        if bad:errors.append(dict(kind='LOG',target=name,diagnostics=bad))
    prep=json.loads((ROOT/'notes/final-merge/wp4-source-preparation.json').read_text());relocated=0
    original=(ROOT/'submission-v10/supplement.tex').read_text()
    for r in prep['section_mapping']:
        if r['retained_in_compact']:continue
        p=ROOT/r['exact_relocated_copy'];relocated+=1
        if sha(p)!=r['sha256'] or p.read_text() not in original:errors.append(dict(kind='RELOCATION',path=str(p)))
        if p.read_text().rstrip('\n') not in (ROOT/'EXTENDED_RESULTS.md').read_text():errors.append(dict(kind='EXTENDED_BODY',path=str(p)))
    # A's full analytic qualification source is an exact dependency, not a paraphrased proof.
    a=BASE/'generated/final-analytic-qualifications.tex';a_source=ROOT/'submission-jof/generated/v9-substantive-qualifications.tex'
    if a.read_bytes()!=a_source.read_bytes():errors.append(dict(kind='ANALYTIC_COPY'))
    summary=json.loads((ROOT/'results/final-merge/wp2-cftc-mechanism/summary.json').read_text())
    main_errors,main_checks=main_number_audit(raw,summary);errors.extend(main_errors)
    negative_control=raw.replace('$29/34$','$28/34$',1)
    negative_errors,_=main_number_audit(negative_control,summary)
    if not any(r['kind']=='MAIN_PREDICTION_ROW' for r in negative_errors):errors.append(dict(kind='NEGATIVE_CONTROL_DID_NOT_FAIL'))
    generated=(BASE/'generated/final-cftc-extension.tex').read_text();checked=0;row_count=0
    blocks=re.findall(r'\\label\{tab:final-cftc-(QR33|QR4)\}(.*?\\end\{longtable\})',generated,re.S)
    for method,block in blocks:
        lines=[line for line in block.splitlines() if re.match(r'^[0-9A-Z]{6} & ',line)]
        planned=[r for r in summary['comparisons'] if r['method']==method and r['window']==520]
        if len(lines)!=len(planned):errors.append(dict(kind='CFTC_ROWS',method=method))
        for line,row in zip(lines,planned):
            row_count+=1;actual=[x.strip() for x in re.sub(r'\\\\\s*$','',line).split('&')]
            f=lambda x:'NA' if x is None else format(x,'.6g')
            expected=[row['code'],f(row['reference_loss']),f(row['model_loss']),f(row['relative_loss_percent']),str(row['reference_breach_count'])+'/'+str(row['model_breach_count']),f(row['dm']['dm_t']),f(row['dm']['dm_p']),r'$\infty$' if row['selected_penalty']=='inf' else f(row['selected_penalty'])]
            checked+=len(expected)
            if actual!=expected:errors.append(dict(kind='CFTC_ROW_FIELD',code=row['code'],method=method,expected=expected,observed=actual))
    if row_count!=34:errors.append(dict(kind='CFTC_COMPLETE_CENSUS',rows=row_count))
    # Preserve exact historical table cells even though their prose references are updated.
    table_rows=0
    for name in ['v12-data-table.tex','v10-mcs-main.tex']:
        old=(ROOT/'submission-v10/generated'/name).read_text();new=(BASE/'generated'/name).read_text()
        select=lambda s:[line for line in s.splitlines() if '&' in line and '\\' in line]
        if select(old)!=select(new):errors.append(dict(kind='INHERITED_MAIN_TABLE_ROWS',file=name))
        table_rows+=len(select(old))
    return dict(status='PASS' if not errors else 'MISMATCH',mismatch_count=len(errors),mismatches=errors,
        counts=counts,logs=logs,exact_relocated_sections=relocated,analytic_source_byte_identical=True,
        cftc_long_history_rows=row_count,cftc_display_columns_checked=checked,
        main_numeric_bindings=main_checks,negative_control_in_memory_miscount_detected=any(r['kind']=='MAIN_PREDICTION_ROW' for r in negative_errors),
        original_main_table_lines_checked=table_rows,
        word_rule='English words and numeric tokens after TeX/math/citation cleanup; tables and bibliography excluded, headings and figure captions included. Also report conservative counts including table TeX and actual PDF table/figure text.',
        scope='Current source structure, source fields, exact relocations and native compile diagnostics only. Language acceptance, full-page visual QA and broader release checks have separate phase-specific receipts.',
        source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(BASE.rglob('*')) if p.is_file()},
        pdf_sha256=dict(main=sha(main_pdf),supplement=sha(supp_pdf)),new_model_fits=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--main-pdf',type=Path,required=True);p.add_argument('--supp-pdf',type=Path,required=True);p.add_argument('--main-log',type=Path,required=True);p.add_argument('--supp-log',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.main_pdf,a.supp_pdf,a.main_log,a.supp_log)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='source_sha256'},indent=2));raise SystemExit(r['mismatch_count']!=0)
