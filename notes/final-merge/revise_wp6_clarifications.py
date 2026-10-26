"""Writing-only responses to sole-executor WP6 review perspectives."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[2]
main=ROOT/'submission-final/manuscript.tex';text=main.read_text()
changes=[
('''Supplement Section S10 lists every selected code and explains the eligibility rules; complete code-level exclusions remain linked there.''','''Supplement Section S10 lists every selected code and explains the eligibility rules; complete code-level exclusions remain linked there.
Full-sample eligibility makes this universe a retrospective comparison choice, rather than a universe that a forecaster could have selected prospectively.'''),
('''These comparisons extend the benchmark pattern to a separate reporting system while retaining substantial contract-level variation.''','''These comparisons extend the benchmark pattern to a separate reporting system while retaining substantial contract-level variation.
This older reference comparison differs from Section~\\ref{sec:history-mechanism}, whose new history predictions use fixed corrected-rank headroom and separately registered thresholds.'''),
('''The universe, validation period, evaluation dates, candidate menus and refit schedule remain inherited, confining the new computation to the registered extension.''','''The universe, validation period, evaluation dates, candidate menus and refit schedule remain inherited, confining the new computation to the registered extension.
Its protocol was locally committed before the new fits, while shorter-history outcomes were already known and external public preregistration remains unclaimed.
The candidate menus differ from the simulation discovery menus, making this a transported prediction check rather than a replication with identical procedures.'''),
('''These costs express hypothetical preferences rather than observed operating expenses, and Supplement Section S12 retains their normalization and complete-method results.''','''These costs express hypothetical preferences rather than observed operating expenses, and Supplement Section S12 retains their normalization and complete-method results.
Each contract uses its own historical headroom scale, so these normalized comparisons leave common-dollar costs and a common exposure measure unidentified.'''),
('''\\item Downloaded economic-date vintages omit historical first-release information, reporting delays and unrecorded within-interval excursions.''','''\\item Downloaded economic-date vintages omit historical first-release information and reporting delays, keeping the retrospective position clock distinct from public information availability.
Sampled net positions can miss within-interval excursions and gross dealer exposure; daily final records are observed timestamps rather than verified market closes.''')]
records=[]
for old,new in changes:
    if text.count(old)!=1:raise ValueError(old)
    text=text.replace(old,new);records.append(dict(kind='main_prose_clarification',old=old,new=new))
main.write_text(text)

supp=ROOT/'submission-final/supplement.tex';text=supp.read_text()
old=r'''The complete two-regression 72-cell tables remain unchanged in \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/0d2526cc69092c5158437a0509613bac5e86d47f/submission-jof/supplement.pdf}{v9 \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/EXTENDED_RESULTS.md}{the original full Supplement: Tables S26--S27}} and their native fields in the saved controlled simulation. All adverse, failed and unavailable statuses retain their original meanings. The preceding design and prediction outcomes refer to that entire grid, not a successful subset.'''
new=r'''The complete 72-cell records for each regression remain unchanged in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/results/revision-v8/wp3/summary.json}{saved controlled-simulation summary}, alongside the matched historical records. All adverse, failed and unavailable statuses retain their original meanings. The preceding design and prediction outcomes refer to that entire grid, not a successful subset. Original numerical fields, rather than a table number that changed across historical documents, identify these records.'''
assert text.count(old)==1;text=text.replace(old,new);records.append(dict(kind='resolve_nested_historical_table_link',old=old,new=new))
supp.write_text(text)

# Existing branch-relative result links are routed to exact files already in
# the consolidated branch. Original source documents remain unchanged.
links=[]
for p in [supp,ROOT/'submission-final/title-page.tex']:
    text=p.read_text()
    pattern=r'https://github\.com/ByronLi0207/financial-mathematics-paper-20261020/(blob|tree)/(revision-v(?:7-final|10b|11|12))(?=/|[}])'
    def route(m):
        value=m.group().replace('/'+m.group(2),'/final-jof');links.append(dict(source=str(p.relative_to(ROOT)),old=m.group(),new=value));return value
    text=re.sub(pattern,route,text);p.write_text(text)

p=ROOT/'submission-final/generated/final-cftc-extension.tex';text=p.read_text()
marker='The two tables show every new long-history conditional-versus-F comparison.'
extra='''A separate scalar implementation by the same executor verifies targets, scores, strict breaches, HAC diagnostics and maturity records. Its acceptance uses the registered absolute $10^{-10}$ plus relative $10^{-12}$ tolerance; integer identities and hashes are exact. Zero mismatches therefore denotes tolerance-based algorithm agreement, not byte-identical summation, another data acquisition, a second person or another finite-penalty solver fit. The complete audit and rounding discrepancies remain in the linked result readout.

'''
assert text.count(marker)==1;text=text.replace(marker,extra+marker);p.write_text(text);records.append(dict(kind='audit_independence_and_float_tolerance_qualification',added=extra))

record=dict(status='APPLIED',scientific_results_changed=False,protocols_changed=False,new_model_fits=0,changes=records,rerouted_links=links)
(ROOT/'notes/final-merge/wp6-writing-changes.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(changes=len(records),rerouted_links=len(links),new_model_fits=0)))
