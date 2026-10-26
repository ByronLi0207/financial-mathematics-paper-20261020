"""Read-only numeric source/display/context checks; no scientific recomputation."""
from pathlib import Path
import csv,datetime,hashlib,importlib.util,json,re
ROOT=Path(__file__).resolve().parents[2]
def load(path):return json.loads((ROOT/path).read_text())
def pointer(node,path):
 for part in path.split('/')[1:]:node=node[int(part)] if isinstance(node,list) else node[part]
 return node
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def paragraphs(text):
 text=text.split(r'\begin{document}',1)[1].split(r'\begin{thebibliography}',1)[0]
 text=re.sub(r'\\begin\{(?:table|figure)\}.*?\\end\{(?:table|figure)\}','',text,flags=re.S)
 text=re.sub(r'\\(?:cite\w*|label|ref|eqref|url)\{[^}]*\}','',text)
 text=re.sub(r'\\href\{[^}]*\}','',text)
 return [p for p in re.split(r'\n\s*\n',text) if re.search(r'\d',p)]
def plain(s):return s.replace(r'\%','%').replace('$','').replace(r'\(','').replace(r'\)','')
def audit(text):
 ps=paragraphs(text);errors=[];checks=[]
 if len(ps)!=52:errors.append(dict(kind='NUMERIC_PARAGRAPH_CENSUS',expected=52,actual=len(ps)))
 if len(ps)!=52:return dict(status='MISMATCH',mismatches=errors)
 categories={}
 for i in range(52):categories[i]=dict(kind='SOURCE_CONTEXT',sources=[])
 def classify(ids,kind,sources):
  for i in ids:categories[i]=dict(kind=kind,sources=sources)
 classify([0,1,2,3,4,14,18,36,43],'MATHEMATICAL_DEFINITION_OR_EXISTING_FORMULA',['submission-v10/manuscript.tex','submission-final/generated/final-analytic-qualifications.tex'])
 classify([5,16,19,22,24,27,35,48,50,51],'STRUCTURAL_REFERENCE_OR_IDENTIFIER',['notes/final-merge/wp4-source-preparation.json','notes/final-merge/wp8-cross-reference-audit.json'])
 classify([12,28],'EXPANDED_TABLE_DEPENDENCY',['notes/final-merge/wp8-document-audit.json','notes/final-merge/wp7-display-equivalence.json'])
 classify([6,7,13,15,17],'FROZEN_METHOD_OR_SOURCE_METADATA',['protocol/revision-20261022/study-spec.json','protocol/final-merge/wp2-input-seal.json'])
 classify([8,25],'SAME_RECORD_DAILY_AGGREGATE',['results/revision-v8/wp4/readout-bindings.json','results/revision-v8/wp4/summary.json','results/revision-v8/wp4/contrasts.csv'])
 classify([9,10,11],'CFTC_SEALED_GEOMETRY_AND_METADATA',['protocol/final-merge/wp2-input-seal.json','results/v10/cftc/manifest.json'])
 classify([20],'MCS_REGISTERED_CONFIG',['results/v10/mcs/manifest.json'])
 classify([21,23,34,49],'RETAINED_B_NUMERICAL_CLAIMS',['notes/v7/evidence-parts/fx.json','submission-v10/manuscript.tex'])
 classify([26],'ORIGINAL_CFTC_COMPARATOR_SCOPE',['results/v10/cftc/predictions.json'])
 classify([29,30,31,32,33],'RETAINED_V12_SELECTED_FIELDS',['notes/v12/new-paper-number-bindings.json'])
 classify([37,38],'A_DISCOVERY_AND_CONFIRMATION_FIELDS',['notes/final-merge/evidence-bindings.json'])
 classify([39,40,41,42],'REGISTERED_NEW_CFTC_FIELDS',['protocol/final-merge/wp2-input-seal.json','results/final-merge/wp2-cftc-mechanism/summary.json'])
 classify([44,45,46,47],'FIXED_COST_GRID_SELECTED_FIELDS',['results/v10/cost/group-regions.json','results/v10/cost/manifest.json'])
 def check(i,path,ptr,display,formatter=None):
  value=pointer(load(path),ptr);observed=plain(ps[i]);expected=formatter(value) if formatter else str(value)
  same=expected==display;present=bool(re.search(r'(?<![\d.])'+re.escape(display)+r'(?!\d|\.\d)',observed))
  if not same or not present:errors.append(dict(paragraph=i,source=path,pointer=ptr,expected=expected,declared_display=display,present=present))
  checks.append(dict(paragraph=i,source=path,pointer=ptr,value=value,display=display,source_sha256=sha(path),correct_format=same,present_in_exact_context=present))
 # Basic counts and the unchanged reporting-design coordinates.
 spec='protocol/revision-20261022/study-spec.json'
 check(6,spec,'/sources/fx_hourly/record_count','18,576',lambda x:format(x,','));check(7,spec,'/sources/nyfed_weekly/record_count','706')
 check(13,spec,'/tau_numerator','19');check(13,spec,'/tau_denominator','20');check(15,spec,'/feature_count_without_intercept','33')
 daily='results/revision-v8/wp4/readout-bindings.json';check(8,daily,'/daily_metadata/n_daily','930');check(8,daily,'/periods/evaluation_count','501')
 seal='protocol/final-merge/wp2-input-seal.json';check(10,seal,'/source_geometry/0/N','877');check(39,seal,'/windows/2','520')
 # Legacy current prose: compare the actual source field, not a matching numeral elsewhere.
 specapi=importlib.util.spec_from_file_location('wp8_old_number_api',ROOT/'notes/v7/check_numbers_v7.py');api=importlib.util.module_from_spec(specapi);specapi.loader.exec_module(api)
 legacy={r['id']:r for name in ['metadata','fx','panel','theory'] for r in load('notes/v7/evidence-parts/'+name+'.json')}
 for i,key,fmt,display in [(21,'FX_LATE_SHORT_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT','.1f','31.5'),(21,'FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_LEFT','.0f','924'),(21,'FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_RIGHT','.0f','427'),(34,'FX_PREFERENCE_H24_REVERSAL_RATIO','.1f','20.6')]:
  row=legacy[key];value=api.source_value(row);formatted=format(float(value),fmt);present=display in plain(ps[i])
  if formatted!=display or not present:errors.append(dict(paragraph=i,id=key,expected=formatted,display=display,present=present))
  checks.append(dict(paragraph=i,id=key,source=row['source'],locator=row.get('pointer',row.get('where')),value=value,display=display,source_sha256=sha(row['source']),present_in_exact_context=present))
 # Two retained rounded statements are additionally locked to their inherited prose context.
 baseline=(ROOT/'submission-v10/manuscript.tex').read_text()
 for i,passage in [(23,'conservative selection choosing the intercept-only report in 17 of 26 earlier cells'),(49,r'The ordinary empirical quantile is up to 36.5\% worse than corrected headroom in the earlier weekly grid.')]:
  same=passage in ps[i] and passage in baseline
  if not same:errors.append(dict(paragraph=i,kind='BASELINE_CONTEXT_NOT_IDENTICAL'))
  checks.append(dict(paragraph=i,source='submission-v10/manuscript.tex',exact_source_passage=passage,source_sha256=sha('submission-v10/manuscript.tex'),same_in_context=same,limitation='Preserved baseline claim; underlying original-number guard and1186saved-field audit are separate.'))
 # Every v12 numeric manuscript addition uses its pre-existing field/format binding.
 v12=load('notes/v12/new-paper-number-bindings.json')['bindings'];v12_ids={r['id']:r for r in v12}
 mapping={29:['short_weekly_planned','gap_positive_count','selection_majority_count','short_actual_median','short_selection_median','short_gap_median'],30:['validation_short_length','validation_long_length','training_history_52','median_W52_V52','median_W52_V156'],31:['training_history_260','median_W260_V52','median_W260_V156'],32:['infinite_W52_V52','infinite_W52_V156','infinite_W260_V52','infinite_W260_V156','validation_eligible_contracts'],33:['tau_0.9','tau_0.99','tau_cftc_known_wins','tau_cftc_planned_comparisons','tau_cftc_required_wins']}
 for i,ids in mapping.items():
  for key in ids:
   row=v12_ids[key];value=pointer(load(row['source']),row['json_pointer']);display=row['display'];present=display in plain(ps[i])
   if value!=row['value'] or not present:errors.append(dict(paragraph=i,id=key,kind='V12_SOURCE_OR_CONTEXT',present=present))
   checks.append(dict(paragraph=i,id=key,source=row['source'],pointer=row['json_pointer'],value=value,display=display,source_sha256=sha(row['source']),present_in_exact_context=present))
 # Discovery crossings/intervals and synthetic confirmation counts.
 ledger={r['id']:r for r in load('notes/final-merge/evidence-bindings.json')}
 for key,fmt,display in [('E002','.1f','106.5'),('E003','.2f','27.89'),('E004','.2f','110.71'),('E005','.1f','27.3'),('E006','.2f','13.27'),('E007','.2f','107.11')]:
  row=ledger[key];check(37,row['source'],row['pointer'],display,lambda x,f=fmt:format(x,f))
 for key in ['E008','E009','E011','E012','E014','E015']:
  row=ledger[key];check(38,row['source'],row['pointer'],str(row['expected']))
 summary='results/final-merge/wp2-cftc-mechanism/summary.json'
 for i,fields in [(40,[('P1_QR33','successes'),('P1_QR33','planned'),('P1_QR4','successes'),('P1_QR4','planned')]),(41,[('P2_QR4','successes'),('P2_QR4','planned')]),(42,[('P3_QR4','successes'),('P3_QR4','planned')])]:
  for test,field in fields:check(i,summary,'/tests/'+test+'/'+field,str(pointer(load(summary),'/tests/'+test+'/'+field)))
 # Three stated cost examples refer to fixed full-CFTC-regression grid rows, never an optimized menu.
 for i,index,pair in [(45,1039,'(.1,.25)'),(46,1062,'(1,0)'),(47,1016,'(.01,5)')]:
  row=load('results/v10/cost/group-regions.json')[index];assert row['group_label']=='CFTC' and row['c']==1
  textvalue=str(row['wins'])+'/'+str(row['planned']);present=textvalue in plain(ps[i]) and pair in plain(ps[i])
  if not present:errors.append(dict(paragraph=i,kind='COST_GRID_CONTEXT',row=row))
  checks.append(dict(paragraph=i,source='results/v10/cost/group-regions.json',pointer='/'+str(index),source_sha256=sha('results/v10/cost/group-regions.json'),saved_row=row,display=textvalue,coefficient_pair=pair,present_in_exact_context=present))
 census=[dict(index=i,sha256=hashlib.sha256(p.encode()).hexdigest(),numeric_tokens=re.findall(r'[-+]?\d+(?:[.,]\d+)*(?:/\d+)?',p),classification=categories[i],full_paragraph=p) for i,p in enumerate(ps)]
 return dict(status='PASS' if not errors else 'MISMATCH',mismatch_count=len(errors),mismatches=errors,current_numeric_paragraphs=len(ps),contextual_field_checks=len(checks),checks=checks,census=census,scope='Census covers all52currentmain numeric paragraphs after omitting whole floats/citationkeys/URLs. Explicit empirical field bindings supplement1186legacy+50v12 saved-field checks. Mathematical constants/configuration/structural references are classified separately; main table fields, figures and inherited supplemental numbers retain their dedicated guards. No new fit, score, HAC or financial statistic computed.')
def main():
 text=(ROOT/'submission-final/manuscript.tex').read_text();r=audit(text)
 negative=audit(text.replace('It loses to matched historical headroom in $29$ comparisons','It loses to matched historical headroom in $28$ comparisons',1))
 r.update(actual_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),main_sha256=sha('submission-final/manuscript.tex'),negative_control_wrong_count_detected=negative['status']=='MISMATCH')
 if not r['negative_control_wrong_count_detected']:r['mismatches'].append(dict(kind='NEGATIVE_CONTROL_FAILED'));r['mismatch_count']+=1;r['status']='MISMATCH'
 (ROOT/'notes/final-merge/wp8-current-numeric-contexts.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['checks','census']},indent=2));raise SystemExit(r['status']!='PASS')
if __name__=='__main__':main()
