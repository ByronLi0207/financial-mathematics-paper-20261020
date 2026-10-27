"""Apply the bounded H5 language revisions and record every replacement."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'submission-final/manuscript.tex'
old=p.read_text()
assert hashlib.sha256(old.encode()).hexdigest()=='ffa32c810cb296ea7e21240f75e235e7366374781c96ff177ba33c66fb9b75f6'
text=old
changes=[]

def change(before,after,reason,count=1):
    global text
    assert text.count(before)==count,(before,text.count(before))
    text=text.replace(before,after)
    changes.append(dict(before=before,after=after,reason=reason,occurrences=count))

change('hourly FX positions, weekly New York Fed positions and CFTC dealer positions, matching histories and update schedules.',
       'hourly foreign exchange (FX) positions, weekly New York Fed positions and Commodity Futures Trading Commission (CFTC) dealer positions, matching histories and update schedules.',
       'Expand the first abstract occurrences without changing the three findings.')
change('Second, in the initial weekly comparisons, historical rules beat regression in 34 of 48 New York Fed and 29 of 34 CFTC cases.',
       'Second, in the initial weekly comparisons, historical headroom beats full regression in 34 of 48 New York Fed cases; the better realized historical score wins 29 of 34 CFTC cases.',
       'C33: disclose the descriptive best-realized historical comparison, not an executable selector; C38: specify full regression.')
change('Longer validation improves regression medians in both reporting systems;',
       'Longer validation improves full regression medians in both reporting systems;',
       'C38: do not generalize the full-regression median finding to every four-feature screen.')
change('Our evidence covers hourly FX positions, their daily aggregates, New York Fed categories and CFTC dealer-category futures positions.',
       'Our evidence covers hourly foreign exchange (FX) positions, their daily aggregates, New York Fed categories and Commodity Futures Trading Commission (CFTC) dealer-category futures positions.',
       'Expand acronyms at their first occurrence in the main text as well as in the abstract.')
change('Second, longer validation improves weekly regression medians while leaving large losses on individual tasks.',
       'Second, longer validation improves weekly full regression medians while leaving large losses on individual tasks.',
       'C38: keep the second finding specific to the full regression.')
change('while extended validation reduces regression medians (Section~\\ref{sec:v12-low-frequency}).',
       'while extended validation reduces full regression medians (Section~\\ref{sec:v12-low-frequency}).',
       'Keep the introductory second finding consistent with the abstract and result table.')
change('MaxVaR studies the worst cumulative portfolio return under fixed holdings and diffusion assumptions',
       'MaxVaR studies the value at risk (VaR) of the worst cumulative portfolio return under fixed holdings and diffusion assumptions',
       'Expand VaR before the literature table uses the abbreviation.')
change('including PnL quantile forecasts','including profit and loss (PnL) quantile forecasts','Expand PnL on first use.')
change('longer validation reduces weekly regression medians in two reporting systems.',
       'longer validation reduces weekly full regression medians in two reporting systems.',
       'C38: align the literature-section synthesis with the full-regression result.')
change('Its 18,576 records retain source USD units;',
       'Its 18,576 records retain source US dollar (USD) units;',
       'Define the currency abbreviation; preserve the source unit and observation count.')
change('Local quantiles use neighboring historical states, with an increment-scaled variant.',
       'Local quantiles use the k nearest historical states (KNN), with an increment-scaled variant.',
       'Define the local-neighbor abbreviation before the method table.')
change('GARCH-standardized empirical innovations',
       'empirical innovations standardized by generalized autoregressive conditional heteroskedasticity (GARCH)',
       'Expand GARCH without changing the filtered-path specification.')
change('A headroom CAViaR recursion and calibration wrappers follow existing methods',
       'A headroom conditional autoregressive value at risk (CAViaR) recursion and calibration wrappers follow existing methods',
       'Expand CAViaR; retain the existing-method attribution.')
change('one paired HAC standard error of the winner\'s loss.',
       'one paired heteroskedasticity and autocorrelation consistent (HAC) standard error of the winner\'s loss.',
       'Expand HAC before later covariance and evidence-gate uses.')
change('Delayed projected ACI-style wrappers; headroom SAV; fixed forecast combinations',
       'Delayed projected adaptive conformal inference (ACI) wrappers; symmetric absolute value (SAV) headroom recursion; fixed forecast combinations',
       'Define the table abbreviations, retaining the same procedures.')
change('Each new analysis states its prediction thresholds before computation (Supplement Sections S36 and S38), with chronological records retained separately from the results.',
       'Later analyses retain prewritten thresholds and the available local and public timing records (Supplement Sections S36, S38 and S40). Original design-object availability is reported by round.',
       'C19: distinguish documented local/public timing and missing original objects from external registration.')
change('Together, the history and menu comparisons link conditional gains to history length and the availability of strong shrinkage.',
       'Within the tested configurations, the history and menu comparisons link conditional gains to history length and the availability of strong shrinkage.',
       'C25: restrict the learning-curve/menu interpretation to the tested configurations.')
change('The primary verdict is therefore partial support.',
       'Full regression has no prewritten high-region cell, leaving its high-history screen untestable. The primary verdict is therefore partial support.',
       'C27: make the missing QR33 high-region screen explicit in the main paragraph.')
change('\\subsection{Why does regression lose at low frequency?}',
       '\\subsection{Finite-menu loss decomposition and validation length}',
       'C35: a finite-menu diagnostic does not identify a general causal mechanism.')
change('This residual gap indicates limited incremental information within the tested feature set and finite menu.',
       'This gap describes the tested finite procedures; it does not establish that conditional information is absent.',
       'C35: retain the adverse finite-menu result without claiming that the features contain no information.')
change('Four-feature results and original CFTC failures remain available in Supplement Sections S36 and S38.',
       'The four-feature short-horizon New York Fed median-improvement screen fails. Its complete results and original CFTC failures remain available in Supplement Sections S36 and S38.',
       'C38: preserve the unsupported four-feature screen beside the full-regression finding.')
change('The simulation menu comparison also brings short-history regression closer to history, linking useful conditional reports to sufficient history, validation evidence and adequate shrinkage.',
       'The simulation menu comparison also brings short-history regression closer to history, linking these outcomes to the tested histories, validation windows and shrinkage menus.',
       'C25/C35: avoid a universal sufficient-history or causal interpretation.')
change('For RQ2, longer validation reduces full-regression medians',
       'For RQ2, longer validation reduces full regression medians',
       'Use the same full-regression method name in the abstract, findings and conclusion.')
change('\\item Weekly reports aggregate positions across dealers; related categories and the CFTC survivor universe do not provide independent dealer replications.',
       '\\item Weekly reports aggregate positions across dealers; related categories and the CFTC survivor universe do not provide independent dealer replications. Net-position peaks summarize exposure; gross portfolios, hedging arrangements and economic capital requirements remain unidentified.',
       'Domain-review boundary: these reported positions do not identify whole-book risk or economic capital.')
change('public TFF historical files','public Traders in Financial Futures (TFF) historical files','Expand the official data-series abbreviation.')

literature=json.loads((ROOT/'notes/submission/asmbi-recent-literature.json').read_text())['records']
paragraph='Recent financial applications in \\emph{Applied Stochastic Models in Business and Industry} study conditional quantiles and changing distributions. '
paragraph+=' '.join(x['context_sentence_en'] for x in literature)
paragraph+=' The present study instead evaluates sampled position peaks against matched historical controls.'
needle='\\begin{table}[htbp]\\centering\\footnotesize\n\\caption{Related studies:'
change(needle,paragraph+'\n\n'+needle,'Add three official-metadata/abstract-verified target-journal studies in a bounded literature context.')

items=[]
for x in literature:
    names=[]
    for a in x['authors']:
        initials=' '.join(part[0]+'.' for part in a['given'].split())
        names.append(a['family']+', '+initials)
    author=names[0]+' \\& '+names[1] if len(names)==2 else names[0] if len(names)==1 else ', '.join(names[:-1])+', \\& '+names[-1]
    label=x['authors'][0]['family']+(' \\& '+x['authors'][1]['family'] if len(names)==2 else ' et al.' if len(names)>2 else '')
    extent=x['pages'] or x['article_number']
    title=x['title'].replace('\u2013','--')
    items.append('\\bibitem['+label+'('+str(x['year'])+')]\u007b'+x['id']+'} '+author+' ('+str(x['year'])+'). '+title+'. \\emph{Applied Stochastic Models in Business and Industry}, \\emph{'+x['volume']+'}('+x['issue']+'), '+extent+'. \\url{https://doi.org/'+x['doi']+'}')
change('\\end{thebibliography}','\n\n'.join(items)+'\n\\end{thebibliography}','Add only the three verified official author/year/volume/issue/page-or-article-number/DOI records.')

assert text.count('Historical rules are hard to beat')==2
p.write_text(text)
bib=ROOT/'submission-final/references.bib'
prior=bib.read_text()
assert not any('{'+x['id']+',' in prior for x in literature)
bib.write_text(prior.rstrip()+'\n\n'+'\n\n'.join(x['bibtex'] for x in literature)+'\n')

cover=ROOT/'submission-final/cover-letter.tex';ct=cover.read_text()
before='Historical rules are hard to beat: matched FX gains depend on the reference, longer validation reduces weekly median losses, and illustrative cost rankings depend on reserve and breach charges.'
after='Matched FX gains depend on the reference; longer validation reduces weekly median losses yet leaves large adverse cases; illustrative cost rankings depend on reserve and breach charges.'
assert ct.count(before)==1;ct=ct.replace(before,after)
before='The manuscript addresses your journal\'s scope of ``stochastic modelling, data analysis and their applications in business, finance\'\' through matched empirical comparisons of historical rules and conditional quantile forecasts for sampled peak dealer positions. It applies existing forecasting and evaluation methods and retains the retrospective design and adverse-result qualifications.'
after='The paper fits your journal\'s scope of ``stochastic modelling, data analysis and their applications in business, finance\'\'. It compares mature conditional methods and historical reports for sampled dealer-position peaks, retaining adverse results and retrospective qualifications.'
assert ct.count(before)==1;cover.write_text(ct.replace(before,after))
changes += [dict(file='submission-final/cover-letter.tex',before=before,after=after,reason='Split the scope explanation and retain its exact official short quotation.'),dict(file='submission-final/cover-letter.tex',before='Historical rules are hard to beat: ...',after='Matched FX gains depend on the reference; ...',reason='Keep the same three findings and acknowledge large adverse cases; avoid repeating the paper slogan.')]

log=dict(created_utc=datetime.now(timezone.utc).isoformat(),source_before_sha256=hashlib.sha256(old.encode()).hexdigest(),source_after_sha256=hashlib.sha256(text.encode()).hexdigest(),replacement_groups=len(changes),changes=changes,new_reference_keys=[x['id'] for x in literature],new_reference_source='notes/submission/asmbi-recent-literature.json',scientific_results_changed=False)
(ROOT/'notes/submission/h5-edit-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in log.items() if k!='changes'},indent=2))
