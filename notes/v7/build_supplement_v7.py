"""S5 document assembly only: read existing aggregates, format, and bind fields.

This module does not import any model, create data, fit a parameter, rerun a
simulation, or calculate a statistical test. Formatting saved scalars is the
only numeric operation. Every printed aggregate has its native source locator.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'notes/v7/supplement-v7-draft.tex'
BINDINGS = ROOT / 'notes/v7/s5-supplement-bindings.json'
URL = 'https://github.com/ByronLi0207/financial-mathematics-paper-20261020'
_json = {}
_csv = {}
bindings = []
source_hashes = {}
s2 = []
for part in sorted((ROOT / 'notes/v7/evidence-parts').glob('*.json')):
    data = json.loads(part.read_text())
    if isinstance(data, list):
        s2.extend(data)


def load(path):
    if path not in _json:
        raw = (ROOT / path).read_bytes()
        source_hashes[path] = hashlib.sha256(raw).hexdigest()
        _json[path] = json.loads(raw)
    return _json[path]


def rows(path):
    if path not in _csv:
        raw = (ROOT / path).read_bytes()
        source_hashes[path] = hashlib.sha256(raw).hexdigest()
        _csv[path] = list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
    return _csv[path]


def pointer(path, key):
    node = load(path)
    for word in key.strip('/').split('/'):
        word = word.replace('~1', '/').replace('~0', '~')
        node = node[int(word)] if isinstance(node, list) else node[word]
    return node


def esc(value):
    chars = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%',
             '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{',
             '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(chars.get(c, c) for c in str(value))


def record(source, fmt, key, value, display, location, where=None):
    item = dict(source=source, format=fmt, value=value, display=display,
                location=location)
    if fmt == 'json':
        item['pointer'] = key
        matches = [a['id'] for a in s2 if a.get('source') == source and a.get('pointer') == key]
    else:
        item.update(field=key, where=where)
        matches = [a['id'] for a in s2 if a.get('source') == source and
                   a.get('field') == key and a.get('where') == where]
    item['s2_ids'] = matches
    bindings.append(item)
    return display


def formatted(value, fmt):
    if value is None or value == '':
        return 'NA'
    if fmt == 'raw':
        return esc(value)
    if fmt == 'latex':
        return str(value)
    if fmt == 'frac':
        a, b = str(value).split('/')
        return r'\(\frac{' + a + '}{' + b + r'}\)'
    return format(float(value), fmt)


def j(source, key, fmt='.3f', location=''):
    value = pointer(source, key)
    return record(source, 'json', key, value, formatted(value, fmt), location)


def c(source, where, field, fmt='.3f', location=''):
    found = [x for x in rows(source) if all(x[k] == str(v) for k, v in where.items())]
    if len(found) != 1:
        raise ValueError((source, where, len(found)))
    value = found[0][field]
    return record(source, 'csv', field, value, formatted(value, fmt), location,
                  {k: str(v) for k, v in where.items()})


def pathlink(path, label=None):
    return r'\href{' + URL + '/blob/revision-v7-final/' + path + '}{' + esc(label or path) + '}'


def table(caption, columns, data, layout=None, size=r'\small'):
    layout = layout or ('l' + 'r' * (len(columns) - 1))
    result = [r'\begingroup', size, r'\setlength{\tabcolsep}{3pt}',
              r'\renewcommand{\arraystretch}{1.12}', r'\begin{longtable}{' + layout + '}',
              r'\caption{' + caption + r'}\\', r'\toprule',
              ' & '.join(columns) + r' \\', r'\midrule', r'\endfirsthead',
              r'\toprule', ' & '.join(columns) + r' \\', r'\midrule', r'\endhead',
              r'\bottomrule', r'\endfoot']
    result.extend(' & '.join(str(x) for x in row) + r' \\' for row in data)
    return '\n'.join(result + [r'\end{longtable}', r'\endgroup']) + '\n\n'


def page(title, label, body):
    return '\n\n'.join([r'\section{' + title + r'}\label{' + label + '}', body])


def proof_pages():
    formal = 'notes/revision-v5-novelty/theory-source.json'
    floor = j(formal, '/blocks/2/latex', 'latex', 'S1 floor identity')
    levy = j(formal, '/blocks/6/latex', 'latex', 'S2 Levy identity')
    one = r'''We forecast the sampled maximum of the absolute position, including
the observed issue position. Write \(B=|N_t|\) and let \(Y\ge B\) almost surely,
with \(B\) measurable at the forecast origin. For \(0<\tau<1\), the pinball score is
\(\rho_\tau(u)=\tau u_+ +(1-\tau)(-u)_+\). A lower inverse conditional quantile
is \(q_\tau=\inf\{c:F(c\mid\mathcal F_t)\ge\tau\}\).

\paragraph{Proposition 1: floor projection.}
Replacing a report \(c\) by \(\max(B,c)\) weakly reduces its score at every possible
outcome. At the population conditional quantile, the strict breach probability
is at most \(1-\tau\). These are distinct statements: projection applies to any
report; the tail qualification requires the true conditional quantile.
\[
''' + floor + r'''
\]
\paragraph{Proof.}
If \(c\ge B\), the replacement changes nothing. If \(c<B\), both errors
\(Y-c\) and \(Y-B\) are nonnegative, so their score difference is
\(\tau(B-c)\). This proves the pointwise identity without a density assumption.
Right continuity of the conditional distribution gives
\(F(q_\tau\mid\mathcal F_t)\ge\tau\), hence
\(\Pr(Y>q_\tau\mid\mathcal F_t)\le1-\tau\). An atom at the quantile can make
this strict; exact nominal hit frequency is not required for a valid upper
quantile. A fitted report does not automatically inherit this population claim.
\hfill\textit{QED}

\paragraph{Why the floor matters.}
The sampled maximum equals the current magnitude whenever the recorded future
path remains inside its current absolute-position band. This can create an atom
even when later signed observations are continuous. The existence of a floor
alone does not imply an atom: an outcome uniformly distributed above the floor
provides a counterexample. Equality-based coverage tests therefore diagnose
their stated equalities, rather than every possible valid upper-quantile report.

\paragraph{Endpoint marginals do not identify the peak.}
The exact artificial constructions in ''' + pathlink(formal, 'the formal example record') + r'''
hold each future-time marginal fixed while changing temporal dependence.
Comonotone and disjoint rare events then give different peak quantiles.
The example is a logical construction, not another financial dataset or an
estimated mechanism. Forecast evaluation must use the ordered path response
and the information available at its actual origin.

\paragraph{Takeaway.}
Known-floor projection is an elementary pointwise improvement. It does not
establish empirical calibration, identify the conditional distribution, or turn
a fitted endpoint forecast into a forecast of a path maximum.'''
    two = r'''\paragraph{Proposition 2: the classical endpoint bound.}
Let future real increments \(X_1,\ldots,X_H\) be independent and individually
symmetric about zero. Set \(S_0=0\), \(S_h=\sum_{j=1}^hX_j\), and fix a starting
position \(x\). Equal increment laws and finite moments are unnecessary.
For the population absolute-displacement quantile at level \(1-\alpha/2\),
\(q=\inf\{c:\Pr(|S_H|\le c)\ge1-\alpha/2\}\), the classical scalar maximal
inequality and the triangle inequality give
\[
''' + levy + r'''
\]
This is a direct application of the classical L\'evy inequality, not a new
maximal inequality. The existing source audit identifies Sussman (2023),
Proposition 3.4, and records the actual consulted source range.

\paragraph{Proof, including strict events and atoms.}
For \(c\ge0\), let \(\eta\) be the first index with \(|S_\eta|>c\). On
\(\{\eta=k,S_k>c\}\), the remaining sum \(R_k=S_H-S_k\) is independent of
the information through \(k\) and is symmetric. Therefore \(\Pr(R_k\ge0)\ge1/2\),
including a possible atom at zero, and that weak sign keeps \(S_H>c\).
On the corresponding negative crossing, \(R_k\le0\) keeps \(S_H<-c\), also
with probability at least one half. Summing over the disjoint crossing events
gives \(\Pr(\max_h|S_h|>c)\le2\Pr(|S_H|>c)\). The argument covers \(c=0\).
Finally, \(\max_{0\le h\le H}|x+S_h|\le |x|+\max_h|S_h|\), and right
continuity gives the required strict tail bound at \(q\). \hfill\textit{QED}

\paragraph{Conditional use and empirical implementation.}
For an observed random anchor, the same argument must hold under its
forecast-origin conditional law, with the corresponding conditional population
endpoint quantile. Conditional independence and zero symmetry cannot be inferred
from unconditional marginals. The empirical endpoint plug-in adds the current
floor to a historical absolute-displacement order statistic. Overlapping labels,
estimated quantiles and changing dependent histories provide no automatic
inheritance of this population bound or a pinball-risk ordering.

\paragraph{Two different failure mechanisms.}
Dependence can destroy the inequality: take \(X_1=Z\), \(X_2=-Z\), with
\(Z\in\{-1,1\}\) equally likely. The endpoint is zero, while the sampled
maximum is one. Separately, replacing the required absolute-displacement
quantile by a generic one-sided endpoint quantile can fail even for independent
symmetric increments. The exact finite example is preserved in the formal
example record. These logical counterexamples are separate from the Gaussian
Monte Carlo cases below; a nonviolating simulation does not prove a theorem
extension.

\paragraph{Takeaway.}
The bound supplies a clear population benchmark under explicit assumptions;
the empirical report remains a model to validate, not a coverage certificate.'''
    return page('Known-floor projection and strict quantile coverage', 'sup:floor', one) + page('Classical endpoint-to-peak bound', 'sup:levy', two)


def simulations():
    old = 'results/revision-20261023/round2/levy/simulation.json'
    corr = 'results/revision-20261023/round2/levy-ar-correction/simulation.json'
    def simrows(source, indices, corrected):
        answer = []
        for i in indices:
            x = load(source)['results'][i]; base = f'/results/{i}/'; loc = 'simulation ' + str(i)
            if corrected:
                family = ('L' if x['model']=='level' else 'I') + '/' + {'stationary':'Stat','absolute95':'Abs','signed95':'Sig','zero':'Zero'}[x['anchor']] + '/' + ('C' if x['q_information']=='conditional_endpoint_oracle' else 'M')
            else: family = 'I/Zero'
            fields = [j(source,base+'horizon','.0f',loc),j(source,base+'phi','.2f',loc),family,
                      j(source,base+'seed','.0f',loc),j(source,base+'oracle_abs_endpoint_quantile','.3f',loc),
                      j(source,base+'max_exceedances','.0f',loc),j(source,base+'max_exceedance_rate','.5f',loc),
                      j(source,base+'monte_carlo_standard_error','.5f',loc),j(source,base+'endpoint_exceedance_rate','.5f',loc)]
            answer.append(fields)
        return answer
    primary=[i for i,x in enumerate(load(corr)['results']) if x['primary_design']]
    secondary=[i for i,x in enumerate(load(corr)['results']) if not x['primary_design']]
    text=r'''These are the existing fixed-seed Gaussian experiments, not newly run
simulations or calibrated replicas of either financial source. Every reported
rate is a probability, not a percentage. The peak includes the initial level;
the endpoint event concerns absolute displacement from that initial level.
Each path cell has '''+j(corr,'/results/0/paths','.0f','simulation paths')+r''' paths.
L/Stat starts the level AR in stationarity; L/Abs fixes its absolute-level
tail anchor; L/Sig is the separate signed-level tail-anchor sensitivity.
I/Zero accumulates stationary AR increments from a zero position.
M denotes a stationary-marginal endpoint threshold; C denotes a distinct
fixed-start conditional endpoint oracle. Threshold partners sharing a seed use
the same paths, not independent repetitions.
'''
    text+=table('Original increment-AR simulation, unchanged. Serial persistence here concerns increments, not fitted position levels.',
                ['H',r'\(\phi\)','Process','Seed','q','Hits','Peak prob.','MC SE','End prob.'],
                simrows(old,range(len(load(old)['results'])),False),size=r'\scriptsize')
    text+=r'''The independent-increment rows satisfy the classical premise.
Positive increment coefficients violate independence without necessarily causing
a numerical breach of the bound. Their favourable rates are not a general
result for serial dependence.'''
    first=page('Monte Carlo mechanisms: original increment persistence', 'sup:simulation-original', text)
    text=r'''The corrected level process is
\(N_h=\phi N_{h-1}+\varepsilon_h\), with independent Gaussian innovations
of variance \(1-\phi^2\) and unit stationary level variance. Its stationary
increments have lag correlation
\(\rho_X(k)=-(1-\phi)\phi^{k-1}/2\), so this mechanism differs from a
positively persistent increment AR. The fitted financial coefficient describes
levels, making the level equation the relevant illustrative mechanism.
The negative-increment family is a separate sensitivity, with stationary
increments and nonstationary cumulative levels.
'''
    text+=table('All corrected primary cases. Mean-reverting level rates are conservative in these finite cases; the negative-increment result must also be retained.',
                ['H',r'\(\phi\)','Process','Seed','q','Hits','Peak prob.','MC SE','End prob.'],simrows(corr,primary,True),size=r'\scriptsize')
    text+=r'''All saved level cases have peak rates below the nominal threshold.
The largest negative-increment point estimate occurs at the longer horizon and
the more negative coefficient. Its rate is '''+j(corr,'/results/33/max_exceedance_rate','.5f','negative increment adverse rate')+r''',
with a saved excess of '''+j(corr,'/results/33/rate_minus_five_percentage_points','.3f','negative increment adverse excess')+r'''
percentage points and Monte Carlo SE '''+j(corr,'/results/33/monte_carlo_standard_error','.5f','negative increment adverse uncertainty')+r'''.
This is not demonstrated population failure. General dependence invalidates the
classical premise regardless of the observed direction. Zero observed counts
also do not establish zero population probability.'''
    second=page('Mean-reverting levels and negative-increment sensitivities','sup:simulation-primary',text)
    text=r'''For stationary random starts, absolute endpoint displacement has
variance \(2(1-\phi^H)\). At a fixed start \(x\), its conditional Gaussian
mean and variance are \((\phi^H-1)x\) and \(1-\phi^{2H}\). Thus holding the
stationary-marginal endpoint threshold across starts does not condition on a
large anchor. The conditional-oracle sensitivities below are distinct thresholds
on shared paths; neither is an oracle for the maximum.
'''
    text+=table('All secondary anchor and conditional-threshold sensitivities. Conditional and marginal endpoint calibration remain distinct.',
                ['H',r'\(\phi\)','Process','Seed','q','Hits','Peak prob.','MC SE','End prob.'],simrows(corr,secondary,True),size=r'\scriptsize')
    text+=r'''The complete correction contains '''+j('results/revision-20261023/round2/levy-ar-correction/independent-readback-portable.json','/threshold_rows','.0f','simulation inventory')+r''' threshold rows on '''+j('results/revision-20261023/round2/levy-ar-correction/independent-readback-portable.json','/unique_initialized_path_cells','.0f','simulation inventory')+r''' initialized path samples.
The retained CSV and portable readback provide exact endpoint moments,
deviations from the nominal probability, and the single-prespecified-row bound
for zero counts. None estimates financial innovation laws, changing fitted
parameters or empirical-quantile uncertainty.'''
    return first+second+page('All secondary simulation sensitivities','sup:simulation-secondary',text)


def empirical_levy():
    source='results/revision-20261023/round2/levy/summary.csv'
    paired='results/revision-20261023/round2/levy/paired-tests.csv';data=[]
    for x in rows(source):
        key={k:x[k] for k in ('source','horizon','window')};loc='empirical endpoint plug-in'
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',c(source,key,'horizon','.0f',loc)+'/'+c(source,key,'window','.0f',loc),c(paired,key|{'right_method':'frozen_F'},'relative_loss_percent','.2f',loc),c(paired,key|{'right_method':'QR'},'relative_loss_percent','.2f',loc),c(source,key,'strict_breach_count','.0f',loc)+'/'+c(paired,key|{'right_method':'frozen_F'},'reference_strict_breaches','.0f',loc)])
    body=r'''The endpoint plug-in uses each completed historical episode's
absolute endpoint displacement and adds its specified empirical quantile to
the actual current-position floor. It shares the historical rule's completed
origin pool and fixed refit schedule, with no fitted tuning parameter.
The operational empirical rank and overlapping financial history are distinct
from the known population quantile in the classical proposition. The report
therefore has to earn its financial coverage and score performance empirically.
'''+table('Every original-cell endpoint plug-in comparison. A population bound does not imply a lower empirical pinball score.', ['Source','H/W',r'L/F \(\Delta\%\)',r'L/QR \(\Delta\%\)','Hits L/F'],data)
    data=[]
    for x in rows(paired):
        key={'contrast_id':x['contrast_id']};loc='endpoint plug-in inference'
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',c(paired,key,'horizon','.0f',loc)+'/'+c(paired,key,'window','.0f',loc),'F' if x['right_method']=='frozen_F' else 'QR',c(paired,key,'dm_t','.3f',loc),c(paired,key,'dm_p','.4g',loc),c(paired,key,'hln_p','.4g',loc),c(paired,key,'holm_p','.4g',loc)])
    body+=table('All separate endpoint-plug-in working-reference contrasts. Adverse score comparisons remain alongside lower-breach reports.', ['Source','H/W','Ref.','DM t','DM p','HLN p','Holm p'],data,size=r'\scriptsize')
    body+=r'''The family and its doubled-bandwidth sensitivities are separate
from the original regression family. The complete tables keep every adverse
direction; no negative comparison is removed by describing the population
inequality as conservative. The linked records preserve source-native mean
error amounts and every numerical status.'''
    return page('Empirical endpoint plug-in: all original cells','sup:levy-empirical',body)


def ar_rank():
    source='results/revision-20261022/ar1-replay/ar1-paired.csv';summary='results/revision-20261022/ar1-replay/ar1-summary.csv';data=[]
    for x in rows(summary):
        key={k:x[k] for k in ('source','horizon','window')};where=key|{'right_method':'frozen_S'}
        row=[('FX' if x['source']=='fx_hourly' else 'Bills'),c(summary,key,'horizon','.0f','AR table'),c(summary,key,'window','.0f','AR table'),c(summary,key,'phi_mean','.3f','AR table'),c(source,where,'relative_mean_loss_difference_percent','.2f','AR vs S'),c(source,key|{'right_method':'QR'},'relative_mean_loss_difference_percent','.2f','AR vs QR'),c(source,where,'strict_breach_count_left','.0f','AR hits')+'/'+c(source,where,'strict_breach_count_right','.0f','S hits')];data.append(row)
    body=r'''At each original refit, estimate an intercept-bearing level recursion
on each unique mature adjacent transition once. Replaying a historical ordered
residual block from the current position gives the exact algebraic identity
\[
M_{i,h}(x)=N_{i+h}+\widehat\phi^{\,h}(x-N_i),\qquad M_{i,0}(x)=x.
\]
The empirical peak uses the same completed scenario origins, response rank,
floor and refit schedule as its matched historical controls. Finite negative or
above-unit coefficients were eligible, not clipped; all observed fitted
coefficients in the archived run happened to lie inside the unit interval.
Their descriptive means are not identified data-generating parameters.
'''+table('Complete original AR replay comparison. Lower scores can accompany more strict breaches.', ['Source','H','W',r'Mean \(\widehat\phi\)',r'AR/S \(\Delta\%\)',r'AR/QR \(\Delta\%\)','Hits AR/S'],data)
    body+=r'''The replay improves on original regression in every original Treasury
cell but loses in most FX cells. Its comparisons with the translated-path rule
have mixed directions, while strict breaches increase in every row above.
Sparse-grid and annual signs can reverse. The full paired, annual and fixed-grid
tables remain in '''+pathlink('results/revision-20261022/ar1-replay/README.md','the AR archive')+r'''.
These are post-result / exploratory same-data calculations, not independent
validation. Numerical readback checked the represented-input recursion and
saved summaries without validating the financial innovation law.'''
    ar=page('AR residual replay and its adverse comparisons','sup:ar',body)
    source='results/revision-20261022/rank-ablation/contrasts.csv';summary='results/revision-20261022/rank-ablation/summary.csv';original='results/revision-20261022/evaluation-summary.csv';data=[]
    for x in rows(summary):
        if x['method']!='I':continue
        key={k:x[k] for k in ('source','horizon','window')};loc='rank ablation'
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',c(summary,key|{'method':'I'},'horizon','.0f',loc),c(summary,key|{'method':'I'},'window','.0f',loc),c(source,key|{'contrast':'QR-minus-I'},'relative_mean_loss_difference_percent','.3f',loc),c(source,key|{'contrast':'I-minus-frozen_F'},'relative_mean_loss_difference_percent','.3f',loc),c(summary,key|{'method':'I'},'strict_breach_count','.0f',loc)+'/'+c(summary,key|{'method':'F'},'strict_breach_count','.0f',loc)+'/'+c(original,key|{'method':'QR'},'strict_breach_count','.0f',loc)])
    body=r'''The ordinary empirical quantile and the corrected empirical rule use
the same completed pool, refit times and issue floor. The former takes the
lower empirical pinball minimizer; the latter uses the specified add-one rank.
At integer probability-times-pool-size values, adjacent reports can be the two
endpoints of the same empirical minimizer interval. Calling the lower report a
uniquely optimal comparator would therefore be wrong. At the short weekly pool,
the noninteger rank distinction differs.
'''+table('Complete ordinary-rank ablation. Lower empirical reports increase breach occasions and need not improve score.', ['Source','H','W',r'QR/I \(\Delta\%\)',r'I/F \(\Delta\%\)','Hits I/F/QR'],data)
    body+=r'''The reconstructed historical summaries match the original controls.
The lower report increases strict hits and mean underprediction amount in every
cell, but its loss direction is mixed. Every Treasury regression remains worse
than the lower empirical report. This ablation isolates a rank convention on
the same viewed record; it neither supplies a fresh validation sample nor
establishes universal superiority of either finite-sample quantile endpoint.
Exact counts, annual splits and fixed-grid rows are linked in '''+pathlink('results/revision-20261022/rank-ablation/README.md','the complete rank archive')+'.'
    return ar+page('Ordinary quantile ranks and minimizer endpoints','sup:rank',body)


def preference():
    source='results/revision-20261022/preference-robustness/results.json';x=load(source);data=[]
    for i,row in enumerate(x['headline_comparisons']):
        base=f'/headline_comparisons/{i}/';ratio= j(source,base+'equality_alpha','frac','headline preference') if row['equality_alpha'] else 'none'
        data.append([esc(row['id']),j(source,base+'left/u_token','.2f','headline U'),j(source,base+'right/u_token','.2f','headline U'),j(source,base+'left/v_token','.2f','headline V'),j(source,base+'right/v_token','.2f','headline V'),ratio])
    body=r'''For a fixed report, changing the loss weight traces a line
\(R_a=aU+(1-a)V\), where \(U=\operatorname{mean}(P-C)_+\) and
\(V=\operatorname{mean}(C-P)_+\). These are passive error amounts over all
origins, not observed funding costs. Breach frequency averages an indicator and
need not rank reports like either amount. The following source-native monetary
values are never pooled across FX and weekly aggregates.
'''+table('The four fixed headline comparisons. The longer-horizon FX result is sensitive to error weights.', ['Comparison',r'\(U_L\)',r'\(U_R\)',r'\(V_L\)',r'\(V_R\)',r'Equality \(a\)'],data,layout='p{30mm}rrrrp{32mm}',size=r'\scriptsize')
    body+=r'''The equality column gives exact saved rational boundaries, not newly
estimated costs. The short-horizon FX primary reduces both mean error amounts;
its elementary-score curves can nevertheless cross because a Murphy diagram
varies the elementary score threshold, a different comparison from reweighting
these two unconditional amounts. The longer-horizon FX legacy pair reverses
near the loss-weight ratio reported in the main text. Actual decision costs
were not observed.

The complete frontiers below include every open region and every boundary tie.
The full and sparse samples remain separate, and feasible reports outside the
specified menu are not part of these menu-relative envelopes. All pairwise
relations, dominated labels and exact arithmetic are additionally preserved in
'''+pathlink('results/revision-20261022/preference-robustness/README.md','the preference archive')+'.'
    result=page('Fixed-report error preferences','sup:preference',body)
    for start in (0,8):
        data=[]
        for i in range(start,start+8):
            row=x['groups'][i];base=f'/groups/{i}/';label=('FX' if row['source']=='fx_hourly' else 'Bills')+' '+esc(row['sample'])+' H'+j(source,base+'horizon','.0f','frontier group')+'/W'+j(source,base+'window','.0f','frontier group')
            for k,reg in enumerate(row['frontier']['regions']):
                p=base+f'frontier/regions/{k}/';data.append([label,'open',j(source,p+'left','frac','full frontier region'),j(source,p+'right','frac','full frontier region'),esc(', '.join(reg['methods']))]);label=''
            for k,point in enumerate(row['frontier']['points']):
                p=base+f'frontier/points/{k}/';data.append(['','point',j(source,p+'alpha','frac','full frontier point'),'',esc(', '.join(point['methods']))])
        body=r'''Open intervals exclude their endpoints. Point rows retain all
ties, including ties at the extreme loss weights. Method codes here denote
the original fixed report menu; their definitions remain in the main methods
table. The sparse grid is a sensitivity on the same record, not independent
data.'''
        body+=table('Complete saved preference frontier, '+('full sample' if start==0 else 'fixed sparse grid')+'. Exact ties prevent an artificially unique winner.', ['Task','Kind',r'Left / point \(a\)',r'Right \(a\)','Minimizers'],data,layout='p{28mm}p{10mm}p{39mm}p{39mm}p{28mm}',size=r'\scriptsize')
        result+=page('Complete preference frontier: '+('full sample' if start==0 else 'sparse sensitivity'),'sup:frontier-'+str(start),body)
    return result


def panel():
    source='results/supervisor-20261023/e5/summary.csv';data=[]
    for x in rows(source):
        key={k:x[k] for k in ('series_key','horizon','window')};loc='complete panel'
        row=[esc(x['series_key']),c(source,key,'horizon','.0f',loc)+'/'+c(source,key,'window','.0f',loc),c(source,key,'F_mean_pinball','.1f',loc)+' / '+c(source,key,'F_strict_breach_count','.0f',loc)]
        for model in ('original_QR33','QR4_plus','QR33_plus','I'):
            row.append(c(source,key,model+'_percent_vs_F','.2f',loc)+' / '+c(source,key,model+'_strict_breach_count','.0f',loc))
        data.append(row)
    text=r'''Each cell compares the same peak target, completed-label pool,
origin sequence, fixed refit schedule and native monetary units. The original
full regression, smaller predictor regression, expanded-ridge full regression
and ordinary empirical report all remain visible. The additional series are
related weekly aggregates, not independent individual-dealer replications.
Changes in predictors and changes in the ridge menu are distinct interventions.
Every listed comparison is post-result / exploratory.

The historical column gives mean pinball loss and strict hits. Other columns
give saved percentage loss difference against that same historical rule and
strict hits; negative percentages favour the column method. Original QR33,
QR4 and expanded QR33 are distinct fitted procedures. I is the ordinary
empirical-quantile report, with the endpoint qualification in Section~\ref{sup:rank}.
'''
    d='results/supervisor-20261023/e5/descriptive-summary.json'
    text+=r'''Across the archived panel, expanded full-regression median excess
loss is '''+j(d,'/QR33_plus/median_percent_vs_F','.2f','panel median')+r''' percent,
compared with '''+j(d,'/original_QR33/median_percent_vs_F','.2f','old panel median')+r''' percent for the original menu. Expanded regression still loses in '''+j(d,'/QR33_plus/losing_to_F','.0f','panel adverse cells')+r''' cells.
This improvement does not erase the remaining failures or identify a causal
feature effect.'''
    result=page('Complete weekly panel: definitions and first half','sup:panel',text+table('Complete panel, first half. Additional regularization leaves substantial adverse cases.', ['Series','H/W','F loss/hits','QR33 \%/hits','QR4 \%/hits','QR33+ \%/hits','I \%/hits'],data[:24],layout='p{26mm}rrrrrr',size=r'\scriptsize'))
    text=r'''The second half follows the identical convention. All original
and expanded results remain unchanged. Cross-series dependence, aggregation
offsets, native-unit differences and overlapping economic positions preclude
treating these cells as independent replications. Forecasts are fitted
separately; observations and losses are not pooled into a single financial
population.'''
    text+=table('Complete panel, second half. The enlarged predictor menu is not uniformly better than historical rules.', ['Series','H/W','F loss/hits','QR33 \%/hits','QR4 \%/hits','QR33+ \%/hits','I \%/hits'],data[24:],layout='p{26mm}rrrrrr',size=r'\scriptsize')
    text+=r'''The independent saved-array arithmetic checks and selection-before-
evaluation records are linked from '''+pathlink('results/supervisor-20261023/e5/README.md','the E5 archive')+r'''. The original panel's entire candidate/status inventory remains in
'''+pathlink('results/revision-20261023/round2/panel/summary.csv','the original panel archive')+r''',
and the fitted expanded-menu predictions are not substitutes for unavailable
methods or independent dealer data.'''
    result+=page('Complete weekly panel: second half','sup:panel-second',text)
    source='results/revision-20261023/round2/panel/summary.csv';data=[]
    keys=list(dict.fromkeys(x['series_key'] for x in rows(source)))
    for key in keys:
        row=[esc(key)]
        for h,w in ((6,52),(6,260),(24,52),(24,260)):
            where={'series_key':key,'horizon':str(h),'window':str(w),'method':'Levy_L'};loc='complete panel endpoint plug-in'
            row.append(c(source,where,'percent_vs_frozen_F','.2f',loc)+'; '+c(source,where,'strict_breach_count','.0f',loc)+'/'+c(source,where,'breaches_frozen_F','.0f',loc))
        data.append(row)
    text=r'''The original added-panel endpoint plug-in was evaluated on the
same task grids as the historical and regression reports. Each entry gives
the saved loss percentage against the historical rule, followed by strict
hits for the endpoint plug-in and historical report. These are all related
aggregate tasks, not independent replications or source-pooled monetary losses.
'''+table('Every additional-panel endpoint-plug-in result. Fewer breaches do not guarantee a better score.', ['Series','H6/W52','H6/W260','H24/W52','H24/W260'],data,layout='p{30mm}rrrr',size=r'\scriptsize')
    text+=r'''The complete original panel CSV also preserves every original
regression candidate, selection result, native-unit mean error amount and
failure status. This table adds no refit or parameter selection and does not
extend the independent-increment population guarantee to these financial
series.'''
    return result+page('Complete added-panel endpoint-plug-in comparison','sup:panel-levy',text)


def selection():
    source='results/supervisor-20261023/r6/retro-summary.csv';data=[]
    for x in rows(source):
        if x['report']!='R0':continue
        key={k:x[k] for k in ('phase','source','series_key','horizon','window')};loc='earlier R0/R2'
        data.append([esc(x['series_key']),c(source,key|{'report':'R0'},'horizon','.0f',loc)+'/'+c(source,key|{'report':'R0'},'window','.0f',loc),c(source,key|{'report':'R0'},'percent_vs_F','.2f',loc),c(source,key|{'report':'R2'},'percent_vs_F','.2f',loc),c(source,key|{'report':'R0'},'strict_breach_count','.0f',loc)+'/'+c(source,key|{'report':'R2'},'strict_breach_count','.0f',loc),c(source,key|{'report':'F'},'strict_breach_count','.0f',loc)])
    assessment='results/supervisor-20261023/r6/assessment.json'
    text=r'''The earlier-period experiment applies the saved fixed selection rules
to familiar historical data. The bounded repository audit found no prior
evaluation role for these earlier origins; this is still retrospective, not
external or prospective validation. R0 denotes the fixed minimum-validation-
loss rule. R2 is the predesignated main one-standard-error selection rule,
not a result-dependent replacement chosen for its subsequent performance.
The rule design precedes its calculations but follows earlier research results.

R1 adds the ordinary empirical quantile to the finite regression candidates.
R2 compares each candidate's validation losses with the same best-mean
candidate, using the paired-difference Bartlett-HAC standard error. Candidates
within that tolerance qualify, and the fixed rule prefers the strongest
shrinkage, including the empirical report. This paired HAC tolerance is a
time-series adaptation of a one-standard-error preference, not the textbook
formula, a significance test or a noninferiority guarantee. It does not account
for the whole uncertainty from selecting the best candidate on that segment.

R3 applies the same preference to prespecified earlier rolling folds and the
outer validation segment, with origin-equal weighting and maturity gaps.
Its HAC pairs use actual source-index distances rather than compressing gaps.
Without an eligible earlier fold, the saved design makes it identical to R2;
this is not a numerical fallback. Earlier-period results were sealed before
the already-inspected-period calculations that could reuse those origins.
'''
    text+=table('Every earlier-period R0/R2 comparison. The one-standard-error rule misses the recorded success conditions.', ['Series','H/W','R0 \%','R2 \%','Hits R0/R2','Hits F'],data,layout='p{35mm}rrrrr',size=r'\scriptsize')
    text+=r'''All recorded success criteria are '''+j(assessment,'/S1/status','raw','R6 assessment')+r''',
'''+j(assessment,'/S2/status','raw','R6 assessment')+r''' and '''+j(assessment,'/S3/status','raw','R6 assessment')+r''', respectively.
R2's worst weekly excess is '''+j(assessment,'/S1/worst_percent_vs_F','.2f','R6 worst')+r''' percent,
and its weekly median is '''+j(assessment,'/S1/median_percent_vs_F','.2f','R6 median')+r''' percent.
The long-history FX gain also fails the prewritten retention criterion.
This adverse result remains a robustness finding rather than a contribution
claim. Complete inspected-period and all-rule rows remain linked in
'''+pathlink('results/supervisor-20261023/r6/README.md','the R6 archive')+'.'
    first=page('Earlier-period fixed selection rules','sup:selection',text)
    source='results/supervisor-20261023/r6/summary.csv';data=[]
    for x in rows(source):
        if x['status']=='COMPLETE':continue
        key={k:x[k] for k in ('phase','source','series_key','horizon','window','report')}
        for field in ('status','reason'):
            c(source,key,field,'raw','R6 failure inventory')
        data.append([esc(x['phase']),esc(x['series_key']),c(source,key,'horizon','.0f','R6 failure inventory')+'/'+c(source,key,'window','.0f','R6 failure inventory'),esc(x['report']),esc(x['status'])])
    text=r'''Required validation-candidate failure blocks the dependent rule;
it is neither retried nor replaced by a shorter mean. The complete noncomplete
report inventory is below. Every listed row has the saved reason
\texttt{REQUIRED\_VALIDATION\_CANDIDATE\_FAILED}. Those failures remain part of
the evidence even though other rules in the same task can complete.
'''+table('All noncomplete R6 report rows. Failed mandatory candidates remain failures.', ['Phase','Series','H/W','Rule','Status'],data,layout='lp{35mm}rrl')
    text+=r'''The Treasury earlier-period structural comparison uses a shorter
history than the original primary. It is explicitly an analogue, not an exact
earlier replication of the long-history primary. The source-native comparison
and its definition are preserved in
'''+pathlink('results/supervisor-20261023/r6/primary-replication.csv','the primary-structure table')+r'''.
All original primary values remain unchanged. Reclassifying the analogue as an
exact primary replication, or calling familiar retrospective FX data an unseen
dealer, would change the scientific claim without adding evidence.'''
    return first+page('Selection failures and replication boundaries','sup:selection-failures',text)


def wp2():
    source='results/revision-20261023/v6/wp2-summary.json';data=[]
    for i,x in enumerate(load(source)['method_rows']):
        p=f'/method_rows/{i}/';loc='WP2 inventory'
        complete=x['status']=='COMPLETE'
        if not complete:j(source,p+'reason','raw',loc)
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',j(source,p+'horizon','.0f',loc)+'/'+j(source,p+'window','.0f',loc),esc(x['method']),j(source,p+'scores/mean_loss','.2f',loc) if complete else 'NA',j(source,p+'scores/full_hits','.0f',loc) if complete else 'NA',j(source,p+'status','raw',loc)])
    body=r'''The finite delayed ACI-style wrapper adapts past strict hits after
their entire peak labels mature. Its score pool contains only completed residual
scores and uses the specified finite memory. The base-plus-score quantile is
projected onto the known floor. The adaptive alpha state is projected to the
current feasible range; the rank-zero convention issues the floor. Gamma was
selected by coverage distance, then pinball loss and the fixed tie rule, a
coverage-first selection criterion distinct from original regression fitting.
No canonical ACI theorem is imported to this modified procedure.

The headroom SAV method adapts a CAViaR recursion, rather than replicating a
return-VaR model. The completed headroom response is normalized by its
training-only scale; the recursive report is multiplied back by that same
scale and then floor-projected. Its fixed bounded optimizer and starts retain
all eligibility and convergence failures; a complete fit is not a proof of a
global optimum. Selection state carries across the unissued chronological gap.
'''+table('Complete delayed-wrapper and headroom-SAV inventory. Two long-horizon wrapper cells remain unavailable.', ['Source','H/W','Method','Mean loss','Hits','Status'],data,layout='lrlrrl',size=r'\scriptsize')
    body+=r'''The NA wrapper rows have the saved reason
\texttt{VALIDATION\_INELIGIBLE}; no test is substituted for the absent forecasts.
All losses are in each source's native units and must not be pooled.'''
    first=page('Finite delayed calibration and headroom SAV','sup:wp2',body)
    source='results/revision-20261023/v6/wp2-findings.json';data=[]
    for i,x in enumerate(load(source)['wrapped_pairs']):
        p=f'/wrapped_pairs/{i}/';loc='wrapped pairs'
        if x['status']=='COMPLETE':
            data.append(['FX' if x['source']=='fx_hourly' else 'Bills',j(source,p+'horizon','.0f',loc)+'/'+j(source,p+'window','.0f',loc),j(source,p+'qr_minus_f_loss_percent','.2f',loc),j(source,p+'qr_hits','.0f',loc)+'/'+j(source,p+'f_hits','.0f',loc),j(source,p+'qr_coverage_distance','.5f',loc),j(source,p+'f_coverage_distance','.5f',loc)])
        else:data.append(['FX' if x['source']=='fx_hourly' else 'Bills',j(source,p+'horizon','.0f',loc)+'/'+j(source,p+'window','.0f',loc),'NA','NA','NA','NA'])
    body=r'''Comparing wrapped regression with wrapped historical reports is a
different question from comparing either wrapper with its unwrapped base.
The following table retains every within-cell comparison. A lower coverage
distance measures closeness of empirical hits to the target probability, not
conditional coverage or lower monetary loss.
'''+table('Every paired wrapper comparison. Calibration adjustment preserves the long-history short-horizon FX score gain but does not produce universal dominance.', ['Source','H/W',r'QR/F \(\Delta\%\)','Hits QR/F','QR dist.','F dist.'],data,size=r'\small')
    comp='results/revision-20261023/v6/wp2-comparisons.json'
    body+=r'''The working-reference comparison inventory contains '''+j(comp,'/family_n','.0f','WP2 family')+r''' fixed slots,
with '''+j(comp,'/raw_na_count','.0f','WP2 raw NA')+r''' raw p values unavailable.
The reported Holm bookkeeping keeps those slots; mapping an NA component to a
bookkeeping value does not create an observed p value or validate failed
reference assumptions. HLN references remain separately identified.
'''
    body+=r'''Exact update equations, gamma candidates, selection freezes,
numerical receipts and all comparisons remain in
'''+pathlink('protocol/revision-v6/REPLAY.md','the v6 replay guide')+r''' and
'''+pathlink('results/revision-20261023/v6/wp2-summary.json','the complete WP2 inventory')+r'''.
The original primaries are not overwritten by these post-result / exploratory
extensions. The upper-horizon NA rows and adverse SAV comparisons remain
visible rather than becoming a favourable subset.'''
    return first+page('Wrapper comparisons, uncertainty and missing cells','sup:wp2-pairs',body)


def wp3():
    source='results/revision-20261023/v6/wp3-combinations.json';data=[]
    for i,x in enumerate(load(source)['method_rows']):
        if not x['original']:continue
        p=f'/method_rows/{i}/';loc='original combinations'
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',j(source,p+'horizon','.0f',loc)+'/'+j(source,p+'window','.0f',loc),'Mean' if x['method']=='MEAN_F_QR' else 'Median',j(source,p+'percent_vs_F','.2f',loc),j(source,p+'percent_vs_QR','.2f',loc),j(source,p+'scores/full_hits','.0f',loc)])
    body=r'''Fixed report combinations use the matched historical and original
regression reports at identical origins. Their arithmetic mean is untuned.
The median also requires the original selected plain local-quantile report;
neither a smaller predictor model nor the endpoint plug-in substitutes for
that missing constituent. Combining floor-respecting reports preserves the
floor, but does not guarantee a conditional quantile or a score below the
best constituent. Identical reports generate an NA equal-loss p value rather
than a manufactured significance result.
'''+table('All original-cell combination comparisons. A report combination can improve one constituent while losing to the other.', ['Source','H/W','Rule',r'vs F \(\%\)',r'vs QR \(\%\)','Hits'],data,size=r'\small')
    find='results/revision-20261023/v6/wp3-findings.json';data=[]
    for method in ('MEAN_F_QR','MEDIAN_F_QR_KNN'):
        p='/counts/'+method+'/';data.append(['Mean' if method=='MEAN_F_QR' else 'Median']+[j(find,p+field,'.0f','combination inventory') for field in ('total','complete','na','lower_than_both','lower_than_F','lower_than_QR','exactly_F')])
    body+=table('Complete combination counts including the added panel. Missing median constituents remain NA.', ['Rule','Total','Complete','NA','Below both','Below F','Below QR','Equal F'],data,size=r'\scriptsize')
    body+=r'''The added panel lacks the specified plain local-quantile
constituent, so all its median rows remain unavailable. Mean combinations are
complete, but lower loss than regression alone does not imply lower loss than
the historical rule. All panel-specific values and every comparison remain in
'''+pathlink(source,'the complete combination record')+'.'
    first=page('Untuned forecast combinations','sup:wp3',body)
    data=[]
    for i,x in enumerate(load(source)['murphy']):
        p=f'/murphy/{i}/';data.append(['FX' if x['source']=='fx_hourly' else 'Bills',esc(x['left_method']),esc(x['right_method']),j(source,p+'ranking','raw','combination Murphy'),j(source,p+'positive_breakpoints','.0f','combination Murphy'),j(source,p+'negative_breakpoints','.0f','combination Murphy')])
    body=r'''Elementary-score comparisons vary the score threshold while
keeping the quantile level fixed. Exact integer-event signs at every unique
breakpoint determine sample crossing before display interpolation. A picture
is not used to select favourable thresholds. These matched combination
contexts are distinct from the original FX primary with its shorter rolling
reference.
'''+table('Every combination Murphy comparison in the original-primary contexts. Crossing prevents threshold-uniform sample dominance.', ['Source','Left','Right','Ranking','Positive','Negative'],data,layout='lp{34mm}p{18mm}lrr',size=r'\scriptsize')
    body+=r'''The complete normal-DM comparison family has '''+j(source,'/family_n','.0f','WP3 family')+r''' slots,
of which '''+j(source,'/raw_na_count','.0f','WP3 raw NA')+r''' have NA raw p values.
The family adjustment is bookkeeping for those saved working references, not
error control over the complete historical analysis search. The inspected
record, overlapping labels, repeated fitting and related aggregate series
remain common to the methods. All original and adverse rows remain in
'''+pathlink('results/revision-20261023/v6/wp3-findings.json','the combination findings')+r'''.
Exact breakpoint signs support only the stated finite-sample score comparison;
they do not certify general forecast dominance, optimal funding, or a causal
benefit from acting on the limits.'''
    return first+page('Combination Murphy diagrams and comparison families','sup:wp3-murphy',body)


def wp4_wp5():
    source='results/revision-20261023/v6/wp4-states.json';data=[]
    for i,x in enumerate(load(source)['rows']):
        for k,g in enumerate(x['groups']):
            p=f'/rows/{i}/groups/{k}/';data.append(['FX' if x['source']=='fx_hourly' else 'Bills',esc(g['group']),j(source,p+'n','.0f','state group'),j(source,p+'mean_difference','.2f','state group'),j(source,p+'hac_se','.2f','state group')])
    body=r'''The states are low, middle and high issue-known RMS position-change
states, not price volatility or yield regimes. Cutpoints come only from the
training history. Reports and original primary means stay unchanged; the
diagnostic divides the already viewed evaluation record without estimating a
switching policy. Source-native group differences are not pooled.
'''+table('All three state groups for each original primary. The FX advantage remains negative in every group, while the weekly evidence remains adverse.', ['Source','State','n','QR minus reference','HAC SE'],data)
    data=[]
    for i,x in enumerate(load(source)['ranking']):
        p=f'/ranking/{i}/';data.append(['FX' if x['source']=='fx_hourly' else 'Bills',esc(x['test']),j(source,p+'raw_p','.6g','state references'),j(source,p+'holm_p','.6g','state references'),esc(x['status'])])
    body+=table('Complete state diagnostic reference family. A joint rejection need not identify a useful state rule.', ['Source','Diagnostic','Raw p','Holm p','Status'],data,layout='lp{35mm}rrl')
    body+=r'''These finite-instrument and group-mean HAC references require
unverified moment, dependence and covariance assumptions. A joint conditional-
moment rejection can be driven by an unconditional mean difference; it is not
evidence that a state-dependent trading or limit-selection policy works.
The source-level reconstruction and all cutpoints remain in
'''+pathlink(source,'the complete state record')+'.'
    first=page('Training-defined position-change states','sup:wp4',body)
    source='results/revision-20261023/v6/wp5-tau-summary.json';data=[]
    for i,x in enumerate(load(source)['rows']):
        p=f'/rows/{i}/';loc='target-level sensitivity';ok=x['status']=='OK'
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',j(source,p+'tau','.2f',loc),esc(x['reference_kind']),j(source,p+'mean_difference','.2f',loc) if ok else 'NA',j(source,p+'qr_scores/full_hits','.0f',loc) if ok else 'NA',j(source,p+'reference_scores/full_hits','.0f',loc) if ok and 'reference_scores' in x else (j(source,p+'control_scores/full_hits','.0f',loc) if ok and 'control_scores' in x else 'NA'),esc(x['status'])])
    body=r'''Changing the target quantile requires fitting the specified target-
level procedure; it is different from reweighting the errors of a fixed report.
The following saved sensitivities keep the original horizon and reference
structure. The weekly primary and matched reference coincide and count once.
All unavailable upper-target rows remain NA with
\texttt{VALIDATION\_INELIGIBLE}, rather than being replaced by a lower target
or a favourable subset. Absolute loss values across different quantile levels
measure different objectives.
'''+table('Complete target-level sensitivity. The lower-target directions recur, but upper-target evidence remains unavailable.', ['Source',r'\(\tau\)','Reference','Mean difference','QR hits','Ref. hits','Status'],data,layout='lrp{20mm}rrrl',size=r'\scriptsize')
    body+=r'''The complete family contains '''+j(source,'/family_n','.0f','WP5 inventory')+r''' slots,
with '''+j(source,'/raw_na_count','.0f','WP5 inventory')+r''' raw p values unavailable.
The existing selection freezes and chronological evaluation receipts remain
linked in '''+pathlink(source,'the target-level inventory')+r'''.
The saved lower-target directions do not establish robustness to an arbitrary
tail level, actual shortage costs, or a new economic decision rule. Failed
eligibility is a result of the specified procedure and remains part of the
paper's boundary.'''
    return first+page('Refitted target-level sensitivities','sup:wp5',body)


def coherence_evalues():
    source='results/revision-20261022/post-result-horizon.csv';data=[]
    for x in rows(source):
        if x['method']!='QR':continue
        key={k:x[k] for k in ('source','window','method')}
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',c(source,key,'window','.0f','coherence'),c(source,key,'origin_count','.0f','coherence'),c(source,key,'strict_crossing_count','.0f','coherence'),c(source,key,'target_order_violation_count','.0f','coherence')])
    body=r'''Realized peaks are ordered as the forecast horizon grows, but
independently fitted reports use horizon-specific completed responses and can
cross. The following exact strict comparisons keep all common issue origins.
Repairing a long-horizon report upward can worsen pinball loss; target ordering
alone does not identify a universally beneficial repair.
'''+table('Every original QR horizon-coherence comparison. Ordered targets do not force ordered fitted reports.', ['Source','W','Origins','Report crossings','Target violations'],data)
    source='results/revision-20261022/coverage-evalues/coverage-evalue-summary.csv';data=[]
    for x in rows(source):
        if x['adjusted_reference_threshold_crossed']!='True':continue
        key={k:x[k] for k in ('source','horizon','window','method')}
        data.append(['FX' if x['source']=='fx_hourly' else 'Bills',c(source,key,'horizon','.0f','evidence crossing')+'/'+c(source,key,'window','.0f','evidence crossing'),c(source,key,'k','.0f','evidence crossing')+'/'+c(source,key,'n','.0f','evidence crossing'),c(source,key,'evalue_display','raw','evidence crossing')])
    body+=r'''The late fixed-terminal conditional-hit diagnostic uses the null
\(E[I_t\mid\mathcal F_t]\le\alpha\), where \(I_t=1\{P_t>C_t\}\).
Within each globally anchored maturity phase, a fixed upper-probability
alternative supplies hit/no-hit factors with conditional expectation at most
one under the stated null. The procedure mixes whole products over its fixed
prior, then averages dependent phases. It does not multiply phases or select
their maximum. The fixed-family threshold does not restore retrospective
error control after viewed-sample diagnostic selection.
'''+table('Every threshold-crossing cell in the complete late diagnostic. A noncrossing elsewhere is not a calibration certificate.', ['Source','H/W','Hits/origins','Saved display value'],data)
    body+=r'''The complete summary and phase tables, exact rational identities,
all noncrossings and the interpretation boundaries remain in
'''+pathlink('results/revision-20261022/coverage-evalues/README.md','the e-value archive')+r'''.
This is a fixed-terminal diagnostic, not an anytime p value, optional-stopping
guarantee, new estimator, or independent validation. Score, breach amount,
frequency and conditional-hit evidence answer different questions.'''
    return page('Horizon coherence and late conditional-hit evidence','sup:coherence',body)


def implementation_reproduction():
    first=r'''\paragraph{Completed labels and update clocks.}
At a scheduled refit \(\kappa\), the latest completed response origin is
\(\kappa-H\). A history of \(W\) completed responses therefore uses
\(\{\kappa-H-W+1,\ldots,\kappa-H\}\), with every target ending by that refit.
Training transforms, scales, coefficients and historical pools are held until
the next scheduled refit. The current observed position may still change at
each forecast issue. Replacing that issue anchor by the refit anchor changes
the forecasting procedure.

\paragraph{Regression and local quantiles.}
The regression objective uses a training-normalized headroom response, an
unpenalized intercept and a ridge penalty on slopes. Projection is applied when
issuing the report and evaluating its validation score, not inside the fitted
training objective. Local methods use training-only standardized predictors,
fixed neighbour menus and duplicate-preserving order statistics. A selected
whole-pool local quantile is an exact historical identity, not a failed-fit
fallback. Scale-adjusted neighbours change responses as well as retrieval.

\paragraph{Numerical eligibility.}
The accepted solver records primal and dual residuals, objectives, feasibility
and their gap. Ill-conditioned, nonfinite, unsupported-rank or failed candidate
states remain failures under the specified whole-cell selection contract.
Changing the ridge menu changes the procedure even when feature definitions
stay fixed. A successful numerical certificate is separate from the financial
accuracy, economic relevance and inferential validity of a forecast.

\paragraph{Working-reference inference.}
Saved unconditional loss differences use the recorded Bartlett-HAC convention;
HLN and doubled-bandwidth sensitivities are labelled separately. Separate
families and later reporting partitions do not erase the wider selection
history. Coverage references distinguish full-grid Kupiec from the
transition-conditional Christoffersen joint likelihood, which conditions on
the initial hit. Small sparse grids and boundary likelihoods retain their
original status. Neither a nonrejection nor a small working-reference p value
proves conditional coverage or supplies selection-adjusted confirmation.

\paragraph{Common-pool construction distances.}
On one nonempty historical episode set, compare the historical headroom,
translated-path and historical-peak reports using the same available order
statistic. Each episode peak includes its starting observation. A translated
path changes each level by the same anchor difference, so its absolute peak
changes by at most that difference. Flooring is nonexpansive and commutes with
the fixed order statistic. The headroom construction has the corresponding
bound in the difference of anchor magnitudes. Thus
\[
|C^{\rm headroom}-C^{\rm peak}|\le\max_i\bigl||N_i|-B\bigr|,\qquad
|C^{\rm translated}-C^{\rm peak}|\le\max_i|N_i-x|.
\]
For a proof of the order-statistic step, paired coordinatewise differences
bounded by a radius imply that each empirical quantile lies below the other
plus that radius; reverse the roles for the second inequality. These
deterministic same-pool bounds do not order financial accuracy or coverage.
Changing historical rows on one side invalidates the common-pool argument.

\paragraph{Complete implementation evidence.}
Exact menus, numerical tolerances, failures and diagnostic tables remain in
'''+pathlink('EXTENDED_RESULTS.md','EXTENDED RESULTS')+r''' and the dated source archives.
This supplement describes the existing procedures; its document builder
imports no forecasting code and performs no new financial computation.'''
    second=r'''\paragraph{What is public.}
The repository provides editable sources, public aggregate results, original
design records, computational code and numerical verification evidence. Old
favourable and adverse outputs remain unchanged. The compact supplement links
the longer retained material instead of removing its rows. Exact source-field
bindings for every aggregate printed here accompany the document generator.

\paragraph{What public checking proves.}
The read-only conditional-archive entry point verifies the existing aggregate
inventory without raw observations. Document regeneration reads public
aggregates and formats their saved values. These checks establish internal
artifact consistency, not recomputed forecasting accuracy, a new sample,
independent scientific replication or journal acceptance.

\paragraph{Full financial replay requires compatible inputs.}
The original FX member and Treasury snapshot must match their recorded
fingerprints and source definitions before a separately authorized fresh
replay. Private per-origin forecasts, fitted traces and restricted FX
observations are not redistributed. Downloaded-vintage economic dates differ
from verified historical first-release availability. A current file with the
same series name is not automatically the accepted snapshot.

\paragraph{Version-specific entry points.}
The v7 merge preserves both source lines. The supervisor panel scripts retain
their original canonical paths and whole-file identity gates. Earlier panel
implementations remain as the explicitly named legacy scripts, with the same
original bytes. Historical execution contracts keep their original values and
dates; exact old-protocol replay should use its recorded source commit.
The existing prospective parameter binding is not silently reactivated or
rebound by this manuscript edit.

\paragraph{Resources and software.}
This revision reads existing local software and results. No package installation,
model fit, additional data acquisition, simulation rerun or parameter search
belongs to document assembly. The historical execution receipts report their
actual worker time, resident memory and observed threads separately from
requested budgets. Test execution uses an isolated copy of tracked inputs so
synthetic fixture writes do not alter the scientific archives.

\paragraph{Routes to complete evidence.}
The '''+pathlink('protocol/revision-v6/REPLAY.md','v6 replay guide')+r''',
'''+pathlink('results/revision-20261022/README.md','original conditional archive')+r''',
'''+pathlink('results/supervisor-20261023/r6/README.md','supervisor rule archive')+r''' and
'''+pathlink('EXTENDED_RESULTS.md','extended-results index')+r''' identify the
complete retained tables, failure inventories and longer technical discussions.
Missing compatible external validation and prospective first-release evaluation
remain research tasks, rather than claims created by these reproducibility
materials.'''
    return page('Numerical implementation and inference conventions','sup:implementation',first)+page('Reproduction, availability and retained extended results','sup:reproduction',second)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=OUT);parser.add_argument('--bindings',type=Path,default=BINDINGS);args=parser.parse_args()
    body=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array,hyperref}
\hypersetup{hidelinks,breaklinks=true}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{2em}
\renewcommand{\thesection}{S\arabic{section}}
\renewcommand{\thetable}{S\arabic{table}}
\title{Online Supplement to Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits}
\author{}
\date{}
\begin{document}
\maketitle
This compact supplement contains the existing mathematical proofs and the
complete principal adverse-result inventories, with links to unchanged longer
archives. It accompanies the v7 manuscript and does not add models, data,
statistical tests or parameter selection. All later diagnostics are identified
as post-result / exploratory; the two original primary comparisons retain
their values and roles.

Tables format saved native fields. Loss percentages are the existing relative
differences against the named reference; probabilities are labelled as such.
Different source-native monetary units are not pooled. NA and failed rows
remain distinct from complete results. The exact binding file and document
builder permit source-field readback without re-running any financial model.

The complete earlier supplement, full comparison families, all candidate
tables, annual and sparse sensitivities, numerical details and source guides
remain accessible through \href{'''+URL+r'''/blob/revision-v7-final/EXTENDED_RESULTS.md}{EXTENDED RESULTS}.
This index is an access route, not a substitute for compatible input data or
independent validation.
'''
    body+=proof_pages()+simulations()+empirical_levy()+ar_rank()+preference()+panel()+selection()+wp2()+wp3()+wp4_wp5()+coherence_evalues()+implementation_reproduction()+r'\end{document}'+'\n'
    args.output.write_text(body)
    report=dict(scope='S5 public-document assembly only; no model/simulation/test/data calculation',output=str(args.output.relative_to(ROOT)),bindings=bindings,source_sha256=source_hashes)
    args.bindings.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps(dict(output=str(args.output),source_files=len(source_hashes),field_bindings=len(bindings),characters=len(body),financial_computations=0,compilation_performed=False),indent=2))


if __name__=='__main__':
    main()
