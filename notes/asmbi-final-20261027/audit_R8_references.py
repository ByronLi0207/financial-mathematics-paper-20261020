from pathlib import Path
import datetime as dt, hashlib, json, re, runpy, subprocess
R=Path(__file__).resolve().parents[2]; N=Path(__file__).resolve().parent
helper=runpy.run_path(str(R/'notes/submission/build_asmbi_package.py'),run_name='R8_bibliography_reader')
bib=(R/'submission-final/references.bib').read_text()
assert bib==subprocess.check_output(['git','show','3dba6d9:submission-final/references.bib'],cwd=R,text=True)
entries={m[1]:helper['bib_fields'](bib[m.start():]) for m in re.finditer(r'@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,',bib)}
norm=lambda s:re.sub(r'[{}\s]','',s).lower()
old=json.loads((R/'notes/revision-v8/wp8-reference-audit.json').read_text())
recent=json.loads((R/'notes/submission/asmbi-recent-literature.json').read_text())
checks={}
for i,record in enumerate(old['references']):
    key=record['key']
    if key not in entries:continue
    compared=[]
    for field,value in record['current_auxiliary_bib_fields'].items():
        if field not in entries[key]:continue
        assert norm(entries[key][field]['value'])==norm(value),(key,field)
        compared.append(field)
    checks[key]=dict(source='notes/revision-v8/wp8-reference-audit.json',pointer='/references/'+str(i),
                     fields_compared=compared,primary_urls=record['primary_source_urls'],
                     reading_scope='Existing verified metadata; current source fields compared again, no fresh full-text review')
for i,record in enumerate(recent['records']):
    key=record['id']
    if key not in entries:continue
    compared=[]
    for field,value in record['bibtex_fields'].items():
        if field not in entries[key]:continue
        assert norm(entries[key][field]['value'])==norm(str(value)),(key,field)
        compared.append(field)
    checks[key]=dict(source='notes/submission/asmbi-recent-literature.json',pointer='/records/'+str(i),
                     fields_compared=compared,primary_urls=[record['official_url']],
                     reading_scope='Existing official Wiley metadata/abstract record; current fields compared again')
fresh={
 'hansen1992':({'author':'Hansen, B. E.','title':'Testing for parameter instability in linear models','year':'1992','journal':'Journal of Policy Modeling','volume':'14','number':'4','pages':'517--533','doi':'10.1016/0161-8938(92)90019-9'},
                ['https://www.sciencedirect.com/science/article/pii/0161893892900199','https://users.ssc.wisc.edu/~behansen/papers/jpm_92.html']),
 'hastie2009':({'author':'Hastie, T. and Tibshirani, R. and Friedman, J.','year':'2009','edition':'2','publisher':'Springer','doi':'10.1007/978-0-387-84858-7'},
                ['https://link.springer.com/book/10.1007/978-0-387-84858-7']),
 'mcs2011':({'author':'Hansen, Peter R. and Lunde, Asger and Nason, James M.','title':'The Model Confidence Set','year':'2011','journal':'Econometrica','volume':'79','number':'2','pages':'453--497','doi':'10.3982/ECTA5771'},
                ['https://onlinelibrary.wiley.com/doi/10.3982/ECTA5771','https://pure.au.dk/portal/da/publications/the-model-confidence-set/']),
 'avellaneda2008':({'author':'Avellaneda, Marco and Stoikov, Sasha','title':'High-frequency trading in a limit order book','year':'2008','journal':'Quantitative Finance','volume':'8','number':'3','pages':'217--224','doi':'10.1080/14697680701381228'},
                ['https://math.nyu.edu/inmemoriam/avellaneda/HighFrequencyTrading.pdf']),
 'cftcTFF':({'author':'Commodity Futures Trading Commission','title':'Historical compressed','url':'https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm'},
                ['https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm'])
}
for key,(fields,urls) in fresh.items():
    for field,value in fields.items():assert norm(entries[key][field]['value'])==norm(value),(key,field)
    checks[key]=dict(source='R8 live official/author metadata reads, 2026-10-27 UTC',
                     fields_compared=list(fields),primary_urls=urls,
                     reading_scope='Metadata only; no fresh method replication or entire-paper reading claimed')
assert set(checks)==set(entries),(set(entries)-set(checks))
build=json.loads((R/'submission-package/ASMBI/build-report.json').read_text())
style=[]
for name in ['manuscript','supplement']:
    info=build['outputs'][name]
    aux=(R/info['log']).with_suffix('.aux').read_text()
    cites=set(k for group in re.findall(r'\\citation\{([^}]+)\}',aux) for k in group.split(',') if k!='*')
    bbl=(R/'submission-package/ASMBI'/(name+'.bbl')).read_text()
    printed=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',bbl)
    assert len(printed)==len(set(printed))
    assert cites <= set(printed)
    assert set(printed) <= set(entries)
    log=(R/info['log']).read_text()
    assert not re.search(r'Citation.*undefined|There were undefined references',log,re.I)
    style.append(dict(document=name,printed=len(printed),cited=len(cites),missing=[],
                      style='Official unchanged Wiley AMA BST, consecutive superscript citation format'))
result=dict(status='PASS',checked_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            bibliography_entries=len(entries),mismatches=0,bibliography_unchanged_from_base=True,
            source_sha256=hashlib.sha256(bib.encode()).hexdigest(),references=checks,format_checks=style,
            boundary='Metadata and current field identity; previous source access limitations retained. No new financial analysis.')
(N/'R8-reference-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='references'},indent=2))
