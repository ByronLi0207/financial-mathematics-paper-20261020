"""D2 mechanism correction, with every simulated number read from saved output."""
import json
import math
from v3_revision import RESULT,para,sub,eq,table


def augment_ar_correction(content):
    path=RESULT/'round2/levy-ar-correction/simulation.json'
    if not path.exists():return
    record=json.loads(path.read_text());rows=record['results']
    primary=[r for r in rows if r['primary_design']]
    level=[r for r in primary if r['model']=='level']
    negative=[r for r in primary if r['model']=='increment']
    assert len(primary)==16 and len(level)==12 and len(negative)==4 and len(rows)==34
    f=lambda x:format(float(x),'.4g')
    pct=lambda r,key:f(100*r[key])
    worst=max(negative,key=lambda r:r['max_exceedance_rate'])
    corrected=('Corrected level-AR sensitivities give observed peak-breach rates of '+f(100*min(r['max_exceedance_rate'] for r in level))+'–'+f(100*max(r['max_exceedance_rate'] for r in level))+'%. Negative-increment AR reaches '+pct(worst,'max_exceedance_rate')+'%, an excess of '+f(worst['rate_minus_five_percentage_points'])+' percentage points with Monte Carlo SE '+pct(worst,'monte_carlo_standard_error')+' percentage points. These oracle-threshold mechanisms supply no empirical-coverage guarantee (Appendix J).')
    for block in content['sections'][7]['blocks']:
        if block.get('type')=='p' and block['html'].startswith('The plug-in reduces FX breach counts'):
            old=block['html'];start=old.index('The oracle-quantile simulations')
            block['html']=old[:start]+corrected
    appendix=next(s for s in content['sections'] if s['title'].startswith('Appendix J.'))
    for block in appendix['blocks']:
        if block.get('type')=='table' and block['caption'].startswith('Table J1.'):
            block['caption']=block['caption'].replace('Oracle-quantile simulation.','Original positive-increment-AR oracle-quantile simulation, retained unchanged.')
    primary_rows=[];secondary_rows=[]
    for r in rows:
        start={'stationary':'stationary','absolute95':'Abs95','signed95':'Signed95','zero':'zero'}[r['anchor']]
        if r['primary_design']:
            label=('Level/' if r['model']=='level' else 'Increment/')+('stat.' if start=='stationary' else start)
            primary_rows.append([label,str(r['horizon']),f(r['phi']),f(r['oracle_abs_endpoint_quantile']),str(r['max_exceedances']),pct(r,'max_exceedance_rate'),f(r['rate_minus_five_percentage_points']),pct(r,'monte_carlo_standard_error'),pct(r,'endpoint_exceedance_rate')])
        else:
            secondary_rows.append([str(r['horizon']),f(r['phi']),start,'marginal' if r['q_information']=='stationary_marginal_endpoint' else 'conditional',f(r['oracle_abs_endpoint_quantile']),str(r['max_exceedances']),pct(r,'max_exceedance_rate'),f(r['rate_minus_five_percentage_points'])])
    zero_upper=100*(-math.expm1(math.log(.05)/rows[0]['paths']))
    appendix['blocks'].extend([
        sub('Corrected level mean reversion and negative-increment sensitivities'),
        para('The fitted AR coefficient in the earlier replay describes position levels, not increments. Table J1 instead specifies a persistent increment process and remains an additional stress mechanism. The corrected level process below is closer to the fitted equation. Its centered Gaussian law and unit stationary variance are illustrative; they do not reproduce either financial source or its fitted intercept, innovation distribution and changing parameters.'),
        eq('N<sub>h</sub>=φN<sub>h−1</sub>+ε<sub>h</sub>,  ε<sub>h</sub>∼N(0,1−φ²),  Var(N<sub>h</sub>)=1 under stationarity.',r'N_h=\phi N_{h-1}+\varepsilon_h,\quad\varepsilon_h\overset{\mathrm{iid}}\sim\mathcal N(0,1-\phi^2),\quad\operatorname{Var}(N_h)=1\ \text{under stationarity}.'),
        para('Differencing a stationary level AR gives negatively correlated increments for positive φ, with the following reference correlation. This formula concerns the stationary random-start law; a fixed starting level changes conditional moments. A differenced level AR is not the negative-coefficient increment AR used as the second sensitivity family.'),
        eq('X<sub>h</sub>=N<sub>h</sub>−N<sub>h−1</sub>,  Var(X<sub>h</sub>)=2(1−φ),  ρ<sub>X</sub>(k)=−(1−φ)φ<super>k−1</super>/2,  k≥1.',r'X_h=N_h-N_{h-1},\quad\operatorname{Var}(X_h)=2(1-\phi),\quad\rho_X(k)=-\frac{1-\phi}{2}\phi^{k-1},\quad k\ge1.'),
        eq('D<sub>H</sub>=N<sub>H</sub>−N<sub>0</sub> ∼ N(0,2(1−φ<super>H</super>)) under stationarity.',r'D_H=N_H-N_0\sim\mathcal N\!\left(0,2(1-\phi^H)\right)\quad\text{under stationarity}.'),
        eq('D<sub>H</sub> | N<sub>0</sub>=x ∼ N((φ<super>H</super>−1)x,1−φ<super>2H</super>).',r'D_H\mid N_0=x\sim\mathcal N\!\left((\phi^H-1)x,1-\phi^{2H}\right).'),
        para('The primary level coefficients are 0.68, 0.85 and 0.98, with the original two horizons. Starts are either sampled from the stationary level distribution or fixed at its absolute-value 95th percentile. The same stationary-marginal endpoint threshold is held across starts, matching a population analogue of the paper’s whole-training endpoint pool. At a fixed tail start it is not the conditional endpoint quantile. Positive and negative fixed starts have the same absolute-peak law by Gaussian sign symmetry.'),
        eq('q<sub>H</sub><super>marg</super>=Φ<super>−1</super>(0.9875)√(2(1−φ<super>H</super>)),  L=|N<sub>0</sub>|+q<sub>H</sub><super>marg</super>.',r'q_H^{\mathrm{marg}}=\Phi^{-1}(0.9875)\sqrt{2(1-\phi^H)},\qquad L=|N_0|+q_H^{\mathrm{marg}}.'),
        para('The absolute-level 95th percentile uses the normal probability 0.975. Because a signed-level 95th percentile instead uses probability 0.95, every such alternative is retained separately in Table J4. For fixed starts, Table J4 also reports a different conditional-endpoint oracle threshold. It solves the folded-normal CDF using the displayed conditional mean and variance, and shares exactly the same paths with its marginal-threshold partner. Neither threshold restores independent increments or conditional zero-centered symmetry; neither is an oracle for the path maximum.'),
        table('Table J3. Corrected primary simulation cases. Each row uses 100000 independent paths and includes the issue position in the peak. Rate/SE/endpoint are percentages; Δ5 is percentage points from 5%. Level rows use the stationary-marginal endpoint quantile; increment rows use their own known endpoint quantile with a zero starting position. Stat. denotes a stationary random start; Abs95 is the absolute-level 95th percentile. End measures the absolute change from the issue position exceeding the endpoint threshold. All seeds and exact counts are retained in the correction CSV.', ['Process/start','H','AR','q','Hits','Peak %','Δ5 pp','SE %','End %'],primary_rows),
        para('All specified mean-reverting level cases have observed peak-breach rates below 5%, including some zero counts at fixed starts. Conservativeness here concerns only these mechanisms and thresholds. A large starting position can move toward zero in conditional mean, producing endpoint displacement without a larger absolute peak; innovations can still overshoot. Zero counts do not prove zero probability: for one prespecified 100000-path cell, the one-sided 95% binomial upper bound is '+f(zero_upper)+'%, without a simultaneous-family claim. A fixed-start marginal threshold remains distinct from conditional endpoint calibration.'),
        para('The negative-increment family keeps unit stationary increment variance, a zero starting position and coefficients −0.3 and −0.6; cumulative levels in that family are not stationary. The largest observed peak-breach rate is '+pct(worst,'max_exceedance_rate')+'% at H='+str(worst['horizon'])+' and increment coefficient '+f(worst['phi'])+'. Its '+f(worst['rate_minus_five_percentage_points'])+'-percentage-point excess is smaller than its '+pct(worst,'monte_carlo_standard_error')+'-percentage-point Monte Carlo SE. This observation is not evidence of a population violation of the 5% threshold, and dependence precludes a general Lévy guarantee regardless of the observed direction.'),
        table('Table J4. All prespecified anchor-definition and conditional-endpoint-oracle sensitivities. Each row has 100000 paths. Signed95 is the signed-level 95th percentile, while Abs95 is the absolute-level 95th percentile. Marginal/conditional thresholds on a given path cell share the same seed; these are not independent replications. Full seeds, endpoint rates, SE and exact parameters remain in simulation.csv.', ['H','φ','Start','Endpoint q','q','Hits','Peak %','Δ5 pp'],secondary_rows),
        para('All new paths use the prerecord of two independent random streams, fixed seeds and bounded batches. They use known population endpoint thresholds, so they do not test finite overlapping calibration pools, quantile estimation, non-Gaussian financial innovations or release-time availability. The original positive-increment table, empirical eight-cell L outputs and original primaries remain unchanged.'),
        para('An analytical horizon boundary, not an additional simulation, makes the limit concrete. For the zero-coefficient member of the stable level-AR family, let all levels, including the initial level, be independent standard normals. For every positive horizon the stationary-marginal endpoint displacement is normal with variance two, so its absolute endpoint oracle below is constant across horizons. Conditional on any finite starting value, the peak-breach probability is:'),
        eq('q=√2 Φ<super>−1</super>(0.9875);  Pr(max<sub>0≤h≤H</sub>|N<sub>h</sub>|&gt;|x|+q | N<sub>0</sub>=x)=1−[2Φ(|x|+q)−1]<super>H</super> →1.',r'q=\sqrt2\,\Phi^{-1}(0.9875),\qquad\Pr\!\left(\max_{0\le h\le H}|N_h|>|x|+q\mid N_0=x\right)=1-\left[2\Phi(|x|+q)-1\right]^H\longrightarrow1.'),
        para('The distribution function here is standard normal, and the displayed q is marginal rather than conditional. Bounded convergence gives the same unconditional limit under the stationary random start. Even the correct conditional endpoint threshold is finite and horizon-invariant at each fixed start, giving the same limit. Independent levels do not imply independent increments: adjacent increments share a level. This elementary example excludes a general guarantee uniform over stable level processes and horizons. It is neither a violation of the independent-increment inequality nor an adverse result for the specified positive-coefficient, finite-horizon simulation cells.')])
