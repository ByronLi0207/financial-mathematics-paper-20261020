"""Freeze layout templates, replacing displayed data with saved-field tokens."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]

def block(text,label):return next(t for t in re.findall(r'\\begin\{table\}.*?\\end\{table\}',text,re.S) if '\\label{'+label+'}' in t)
def rows(text):return [s.strip() for s in text.split(r'\midrule',1)[1].split(r'\bottomrule',1)[0].split(r'\\') if s.strip()]

def main():
    source=(ROOT/'submission-final/manuscript.tex').read_text();records={r['id']:r for p in (ROOT/'notes/v7/evidence-parts').glob('*.json') for r in json.loads(p.read_text())};bindings={r['id']:r for r in json.loads((ROOT/'notes/v7/main-v7-numeric-bindings.json').read_text()) if r['location'].startswith('table:')};used={};templates={}
    def token(id):
        b=bindings[id];r=records[id];assert b['raw_value']==r['value'];used[id]=dict(r,source_sha256=hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest());return '@@'+id+('|' + b['format'] if b['format'] else '')+'@@'
    for label,key in [('tab:fx','table03-fx'),('tab:weekly','table04-weekly'),('tab:methods','table02-methods')]:templates[key]=block(source,label)
    maps={
    'table03-fx':[
      ['FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT','FX_LATE_PRIMARY_H6_ORIGIN_COUNT',('FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_LEFT','FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_RIGHT')],
      ['FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT','FX_LATE_MATCHED_H6_ORIGIN_COUNT',('FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT','FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT')],
      ['FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT','FX_EARLY_PRIMARY_H6_N',None],
      ['FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT','FX_EARLY_MATCHED_H6_N',('FX_EARLY_MATCHED_R0_STRICT_BREACH_COUNT','FX_EARLY_MATCHED_F_STRICT_BREACH_COUNT')],
      ['FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT','FX_ACI_H6_W2880_N',('FX_ACI_H6_W2880_QR_HITS','FX_ACI_H6_W2880_F_HITS')]],
    'table04-weekly':[
      ['PANEL_BILL_QR_H6_W260_LOSS_PERCENT',None],['PANEL_R6_BILL_W52_ANALOGUE_LOSS_PERCENT',None],
      ['PANEL_E5_QR33_MEDIAN',('PANEL_E5_QR33_LOSSES','PANEL_E5_PLANNED')],['PANEL_E5_QR4_MEDIAN',('PANEL_E5_QR4_LOSSES','PANEL_E5_PLANNED')],
      ['PANEL_E5_QR33_EXPANDED_MEDIAN',('PANEL_E5_QR33_EXPANDED_LOSSES','PANEL_E5_PLANNED')],['PANEL_E5_ORDINARY_I_MEDIAN',('PANEL_E5_ORDINARY_I_LOSSES','PANEL_E5_PLANNED')],
      ['PANEL_R6_R0_RETRO_MEDIAN','PANEL_R6_R0_RETRO_COMPLETE'],['PANEL_R6_R2_RETRO_MEDIAN','PANEL_R6_S1_COMPLETE']]}
    for key,mapping in maps.items():
        oldrows=rows(templates[key]);assert len(mapping)==len(oldrows);newrows=[]
        for old,fields in zip(oldrows,mapping):
            cells=[c.strip() for c in old.split('&')]
            for j,id in enumerate(fields,2):
                if id is None:continue
                if isinstance(id,tuple):
                    expected=' / '.join(bindings[x]['rendered'] for x in id);new=' / '.join(token(x) for x in id)
                else:
                    expected=bindings[id]['rendered'];new=token(id)
                    if cells[j].endswith(' groups'):expected+=' groups';new+=' groups'
                assert cells[j]==expected,(key,j,cells[j],expected);cells[j]=new
            newrows.append(' & '.join(cells)+r'\\')
        a,b=templates[key].split(r'\midrule',1);_,c=b.split(r'\bottomrule',1);templates[key]=a+r'\midrule'+'\n'+'\n'.join(newrows)+'\n'+r'\bottomrule'+c
    footnotes={
      'table03-fx':['META_FX_HOURLY_PRIMARY_CONTRAST_WINDOW','META_FX_HOURLY_PRIMARY_CONTRAST_HORIZON','META_FX_HOURLY_PRIMARY_CONTRAST_REFERENCE_WINDOW'],
      'table04-weekly':['PANEL_BILL_QR_H6_W260_QR_HITS','PANEL_BILL_QR_H6_W260_F_HITS','PANEL_BILL_QR_H6_W260_N','PANEL_R6_R2_RETRO_WORST']}
    for key,ids in footnotes.items():
        prefix,note=templates[key].split(r'\footnotesize',1)
        for id in ids:
            literal=bindings[id]['rendered'];pattern=r'(?<![\d.])'+re.escape(literal)+r'(?![\d.])';assert len(re.findall(pattern,note))==1,(key,id);note=re.sub(pattern,lambda m:token(id),note)
        templates[key]=prefix+r'\footnotesize'+note
    for literal,id in [(r'\{720,2880\}','META_FX_HOURLY_WINDOWS'),(r'\{52,260\}','META_NYFED_WEEKLY_WINDOWS')]:
        assert templates['table02-methods'].count(literal)==1;templates['table02-methods']=templates['table02-methods'].replace(literal,token(id))
    for literal,id in [('24','META_FX_HOURLY_REFIT_STEP'),('13','META_NYFED_WEEKLY_REFIT_STEP')]:
        prefix,note=templates['table02-methods'].split(r'\footnotesize',1);assert note.count(literal)==1;templates['table02-methods']=prefix+r'\footnotesize'+note.replace(literal,token(id))
    menu=[.001,.01,.1,1.,10.,'inf'];used['FINAL_CFTC_MENU']=dict(id='FINAL_CFTC_MENU',source='results/v10/cftc/manifest.json',format='json',pointer='/design/menus/QR33',value=menu,source_sha256=hashlib.sha256((ROOT/'results/v10/cftc/manifest.json').read_bytes()).hexdigest())
    literal=r'\{0.001,0.01,0.1,1,10,\infty\}';assert templates['table02-methods'].count(literal)==1;templates['table02-methods']=templates['table02-methods'].replace(literal,'@@FINAL_CFTC_MENU|mathset@@')
    for key,text in [('table05-mcs',(ROOT/'submission-final/generated/v10-mcs-main.tex').read_text()),('table06-cftc',block(source,'tab:cftc-mechanism'))]:
        a,b=text.split(r'\midrule',1);_,c=b.split(r'\bottomrule',1);templates[key]=a+r'\midrule'+'\n@@ROWS@@\n'+r'\bottomrule'+c
    result=dict(schema='final-saved-display-layouts-v1',prepared_from_manuscript_sha256=hashlib.sha256(source.encode()).hexdigest(),templates=templates,operands=used,scope='Layout/prose templates; every substituted result/setting is resolved to its exact preserved JSON/CSV field before formatting. Table01 reads saved descriptive summaries; table05 and06 render saved MCS/WP2 counts without recomputing tests.')
    out=ROOT/'notes/final-merge/wp7-display-spec.json'
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(templates=len(templates),bound_operands=len(used),output=str(out.relative_to(ROOT)))))

if __name__=='__main__':main()
