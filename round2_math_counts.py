"""Count manuscript mathematical remnants without deleting English prose or TeX commands."""
import json,re,subprocess
from pathlib import Path
from v3_revision import ROOT
patterns={
 'ceil(':r'(?<![\\\w])ceil\s*\(',
 'alpha=':r'(?<![\\\w])alpha\s*=',
 'mu(':r'(?<![\\\w])mu\s*\(',
 'phi(':r'(?<![\\\w])phi\s*\(',
 'ASCII_sum_operator':r'(?<![\\\w])sum(?=\s*(?:<sub>|[_({]|[A-Za-z]\s*(?:in\b|∈|=)))',
 'refit_r_subscript':r'<sub>[^<]*?(?<![A-Za-z\\])r(?=[,jB<\s])[^<]*</sub>|_(?:r(?![A-Za-z])|\{[^{}]*?(?<![A-Za-z\\])r(?=[,jB}\s])[^{}]*\})',
 'plain_English_sum_retained':r'(?<![\\\w])sum(?![A-Za-z])',
 'standard_TeX_sum_retained':r'\\sum(?![A-Za-z])'}
def collect(c):
 blocks=[b for s in c['sections'] for b in s['blocks']]
 return {'display_body_appendices':'\n'.join([c['abstract']]+[b.get('html','') for b in blocks]),'formal_equation_TeX':'\n'.join(b.get('latex','') for b in blocks)}
a=json.loads(subprocess.check_output(['git','show','6c419a0:manuscript/revision-v3/paper-content.json'],cwd=ROOT));b=json.loads((ROOT/'manuscript/revision-v3/paper-content.json').read_text())
for name,c in [('historical_6c419a0_before_math_repairs',a),('current_after',b)]:
 for scope,s in collect(c).items():
  counts={k:len(re.findall(p,s)) for k,p in patterns.items()};print(json.dumps(dict(version=name,scope=scope,counts=counts),ensure_ascii=False))
  if name=='current_after':assert all(counts[k]==0 for k in list(patterns)[:6])
s=(ROOT/'manuscript/revision-v3/main.tex').read_text();print(json.dumps(dict(version='current_after',scope='render_source_main_tex',counts={k:len(re.findall(p,s)) for k,p in patterns.items()}),ensure_ascii=False))
english_count=len(re.findall(patterns['plain_English_sum_retained'],collect(b)['display_body_appendices']))
print(f'{english_count} ordinary English sum phrases and standard LaTeX \\sum commands are valid prose/source and retained. A bare r in the finite perturbation bound is a radius, not a refit subscript. Historical counts are read from actual commit6c419a0, not inferred from reviewer estimates.')
