"""Keep every old result: compact PDF plus verbatim linked technical overflow."""
from pathlib import Path
import json,re,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];BASE='32ee58688bac260de322c31cb8945adbf3b53154'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def main():
 before=subprocess.check_output(['git','show',BASE+':submission-jof/supplement.tex'],cwd=ROOT);s=before.decode()
 snap=ROOT/'notes/revision-v9/wp5-supplement-before.tex'
 with snap.open('xb') as f:f.write(before)
 matches=list(re.finditer(r'\\section\{([^}]+)\}',s));parts={}
 for i,m in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else s.index(r'\end{document}')
  parts[m.group(1)]=s[m.start():end]
 wanted=['Complete preference frontier: full sample','Complete preference frontier: sparse sensitivity','Numerical implementation and inference conventions'];fragments=[parts[k] for k in wanted]
 assert all(r'\cite' not in x for x in fragments)
 extended=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array,graphicx,hyperref}
\hypersetup{hidelinks,breaklinks=true}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\setlength{\emergencystretch}{2em}
\renewcommand{\thesection}{E\arabic{section}}\renewcommand{\thetable}{E\arabic{table}}
\begin{document}
\begin{center}\Large\bfseries Complete preference frontiers and numerical conventions\end{center}
These sections are copied verbatim from the preceding Supplement. Every
frontier region, boundary tie and numerical convention remains present; the
separate PDF is a page-budget relocation, not a new analysis or edited result.
The compact Supplement links this file through the extended-results index.

'''+ '\n\n'.join(fragments)+r'\end{document}'+'\n'
 target=ROOT/'submission-jof/extended-v9-technical.tex'
 with target.open('x') as f:f.write(extended)
 url='https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v8-goal/'
 bridge=(r'\section{Complete preference frontiers: linked full inventories}\label{sup:frontier-0}\label{sup:frontier-8}'+'\n\n'+r'The unchanged full-sample and fixed-sparse frontiers, including every open region and boundary tie, appear in the \href{'+url+r'submission-jof/extended-v9-technical.pdf}{complete linked technical PDF}. The identical editable sections and their original source-field tables are indexed in \href{'+url+r'EXTENDED_RESULTS.md}{EXTENDED RESULTS}. This relocation keeps every favorable, adverse and tied region while making room for the complete new prediction assessments below.'+'\n\n')
 old=fragments[0]+fragments[1];assert old in s;s=s.replace(old,bridge)
 implementation=fragments[2];prefix=implementation[:implementation.index(r'\paragraph{Regression and local quantiles.}')]
 brief=prefix+'\nThe unchanged normalization, solver-eligibility, working-reference inference and common-pool details appear in the '+r'\href{'+url+r'submission-jof/extended-v9-technical.pdf}{complete linked technical PDF}.'+' Their full source text is preserved verbatim, rather than replacing failed procedures or recalculating numerical results.\n\n'
 assert implementation in s;s=s.replace(implementation,brief)
 s=s.replace('The complete frontiers below include every open region and every boundary tie.','The complete linked frontiers include every open region and every boundary tie.')
 title='When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits'
 s=s.replace('Online Supplement to Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits','Online Supplement to '+title)
 old='v8 manuscript and adds the accepted frozen simulation, same-dealer daily\naggregation and fixed-parameter full-prefix backcast.'
 new='current manuscript and preserves the preceding controlled grid, same-dealer daily\naggregation and fixed-parameter full-prefix backcast. It also reports the post hoc\nhistory-coordinate discovery and the separately specified pre-run tests.'
 assert old in s;s=s.replace(old,new)
 d=json.loads((ROOT/'protocol/revision-v9/wp2-confirmatory.json').read_text());curves=json.loads((ROOT/'results/revision-v9/wp3/curve-predictions.json').read_text());clock=json.loads((ROOT/'protocol/revision-v9/wp3-learning-curve.json').read_text())
 values=lambda a:', '.join(format(x,'g') for x in a)
 spec=d['DGP_spec'];student=spec['student_t5'];regime=spec['regime_3to1'];jump=spec['compound_poisson'];df=student['df']
 text=r'\section{History-coordinate discovery and pre-run prediction tests}\label{sup:v9-history}'+'\n\n'
 text+=r'The post hoc discovery compares $W/p$, $W/((H+1)p)$ and $W/(H+1)$ on the earlier controlled grid; $p$ denotes the nominal coefficient count including the intercept. The in-sample classification tie selects $c=W/(H+1)$, which omits $p$. The bootstrap resamples repetition identifiers jointly across methods and conditions, fixes the selected coordinate, and retains every draw. Its endpoint envelopes condition on coordinate selection and the discovery grid rather than cover the entire search history. Multiple crossings remain visible, so a first downward crossing is not a permanent superiority threshold.'+'\n\n'
 text+=r'The new simulation uses $N_t=\phi N_{t-1}+\eta_t$, with $\phi\in\{'+values(d['phi'])+r'\}$, $W\in\{'+values(d['windows'])+r'\}$ and $H\in\{'+values(d['horizons'])+r'\}$. Each cell has '+str(d['repetitions'])+' repetition streams; '+str(d['burn_in'])+' burn-in observations precede '+str(d['retained_observations'])+r' retained observations. The following innovation laws are controlled stress conditions, not fitted replicas of either financial source:'+'\n\n'
 text+=r'\begin{itemize}'+'\n'
 text+=r'\item Student: $\eta_t=\sqrt{\frac{'+str(df-2)+'}{'+str(df)+r'}}T_t$, with independent $T_t\sim t_{'+str(df)+r'}$.'+'\n'
 siglow=regime['sigma_low'].replace('1/sqrt(5)',r'\frac{1}{\sqrt{5}}');sighigh=regime['sigma_high'].replace('3/sqrt(5)',r'\frac{3}{\sqrt{5}}')
 text+=r'\item Volatility switching: $\eta_t=\sigma_{S_t}Z_t$, $\sigma_0='+siglow+r'$, $\sigma_1='+sighigh+r'$, independent $Z_t\sim N(0,1)$, same-state transition probability '+str(regime['stay_probability'])+' and initial high-state probability '+str(regime['initial_state_probability_high'])+'. Transition follows the current-state innovation.'+'\n'
 magnitude=jump['jump_magnitude_in_Gaussian_SD'];rate=jump['count_rate'];norm=jump['scale'].split('sqrt(')[1].rstrip(')')
 text+=r'\item Symmetric jumps: $\eta_t=(Z_t+'+str(magnitude)+r'\sum_{j=1}^{K_t}U_{tj})/\sqrt{'+norm+r'}$, with independent $Z_t\sim N(0,1)$ and $K_t\sim\mathrm{Poisson}('+str(rate)+r')$. Independent unit signs have positive probability '+str(jump['positive_sign_probability'])+'.\n'
 text+=r'\end{itemize}'+'\n\n'
 text+=r'The seed entropy is '+str(d['master_entropy'])+r'; repetition, process and component indices select distinct streams. The original regression and four-predictor procedures retain their respective menus, candidate-eligibility rules and exact-tie conventions. Shared innovations across conditions support paired comparisons, not independent-cell significance claims. P1 requires strict losses in at least '+format(100*d['predictions']['P1']['minimum_fraction'],'.0f')+r'\% of cells with $c<r^\star/2$; P2 requires strict gains in at least '+format(100*d['predictions']['P2']['minimum_fraction'],'.0f')+r'\% of cells with $c>2r^\star$. P3 requires the smaller procedure to have no larger relative loss in every same-$c$ pair. The primary screen requires P1 and P2, while the separate universal P3 statement fails.'+'\n\n'
 text+=r'The FX study fixes validation origins '+str(clock['clock']['validation_origin_first'])+'--'+str(clock['clock']['validation_origin_last'])+' and evaluation origins '+str(clock['clock']['evaluation_origin_first'])+'--'+str(clock['clock']['evaluation_origin_last'])+r', with both horizons and every prescribed history evaluated on the same issue grid. Each matched reference uses its own corresponding $W$ and the same update clock. The available original scientific vectors, summaries and selected penalties agree exactly at the original longer-history checkpoint before the remaining histories run. Older absent parsimonious trace fields remain outside that historical comparison.'+'\n\n'
 text+=r'Cutpoints interpolate the relative-loss curve in raw $W$, not the logarithmic display coordinate. NA cannot be bridged, a left-censored possible crossing is untestable, and later conditional crossings cannot replace the first. The same previously studied financial period supplies the learning curve; this grid does not create an untouched holdout or unseen dealer. All counts, cutpoints, counterexamples and complete paired-loss diagnostics follow in the source-bound tables. The governing designs are linked as \href{'+url+r'protocol/revision-v9/wp2-confirmatory.md}{simulation protocol} and \href{'+url+r'protocol/revision-v9/wp3-learning-curve.md}{financial learning-curve protocol}.'+'\n\n'
 text+=r'\input{generated/v9-evidence-tables.tex}'+'\n\n'
 needle=r'\section{Reproduction, availability and retained extended results}'
 assert s.count(needle)==1;s=s.replace(needle,text+needle)
 # The source sections in the overflow file must retain every original character.
 assert all(x in extended for x in fragments)
 (ROOT/'submission-jof/supplement.tex').write_text(s)
 newindex='# Current v9 evidence and exact technical overflow\n\nThe [unified history figure](results/revision-v9/wp4/render-v5/unified-history.pdf), [all new simulation outcomes](results/revision-v9/wp2/README.md) and [all fixed-grid FX contrasts](results/revision-v9/wp3/README.md) accompany the partly supported history-length interpretation. The universal simplification prediction fails, an FX first cutpoint is left-censored, and both longer-horizon curves reverse at the largest history. The known FX period is reused; these are not independent unseen-dealer replications.\n\nTo keep the compact Supplement within its page budget, the complete unchanged full/sparse preference-frontier sections and full numerical conventions are copied verbatim into [extended-v9-technical.tex](submission-jof/extended-v9-technical.tex), with a [separate readable PDF](submission-jof/extended-v9-technical.pdf). Every frontier region, tie, adverse outcome and implementation qualification remains accessible. The exact relocation proof is [wp5-supplement-relocation.json](notes/revision-v9/wp5-supplement-relocation.json).\n\nThe earlier index below is preserved as historical guidance.\n\n---\n\n'
 p=ROOT/'EXTENDED_RESULTS.md';p.write_text(newindex+p.read_text())
 proof=dict(status='EXACT_RELOCATION_PENDING_COMPILE',before_commit=BASE,before_source_sha256=sha(before),extended_source=str(target.relative_to(ROOT)),extended_source_sha256=sha(extended.encode()),moved_sections=[dict(title=k,characters=len(x),sha256=sha(x.encode()),exact_substring_in_extended=x in extended) for k,x in zip(wanted,fragments)],old_result_files_changed=0,old_scientific_numbers_changed=0,compact_new_source_sha256=sha(s.encode()),new_tables_source='submission-jof/generated/v9-evidence-tables.tex',scope='verbatim scientific content relocation with visible compact-PDF links; final pagination/visual/number checks remain required')
 save(ROOT/'notes/revision-v9/wp5-supplement-relocation.json',proof)
 print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
