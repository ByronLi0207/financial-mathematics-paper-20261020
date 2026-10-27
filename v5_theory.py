"""Exact finite illustrations for stated properties; no financial estimation."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def pinball(y,c,tau):
 e=y-c;return tau*max(e,0)+(1-tau)*max(-e,0)

def distribution(atoms):
 d=defaultdict(F)
 for x,w in atoms:d[x]+=w
 return sorted(d.items())

def quantile(atoms,tau):
 mass=F(0)
 for x,w in distribution(atoms):
  mass+=w
  if mass>=tau:return x
 raise ValueError('Insufficient probability mass')

def signed_endpoint_example():
 atoms=[((x,x+y),wx*F(1,2)) for x,wx in [(0,F(23,25)),(-3,F(1,25)),(3,F(1,25))] for y in (-1,1)]
 signed=quantile([(p[-1],w) for p,w in atoms],F(39,40));absolute=quantile([(abs(p[-1]),w) for p,w in atoms],F(39,40))
 return {'signed_endpoint_quantile':signed,'absolute_endpoint_quantile':absolute,'peak_breach_at_signed_threshold':sum(w for p,w in atoms if max(map(abs,p))>signed)}

def constructions(paths,x,rank):
 B=abs(x);P=[max(map(abs,p)) for p in paths];a=[B+v-abs(p[0]) for p,v in zip(paths,P)];t=[max(abs(x+z-p[0]) for z in p) for p in paths]
 q=lambda values:sorted(values)[rank-1]
 return {'F':q(a),'S':q(t),'K':max(B,q(P)),'r_abs':max(abs(abs(p[0])-B) for p in paths),'r_signed':max(abs(p[0]-x) for p in paths)}

def theory_blocks():
 return [
 {'type':'subheading','text':'Proposition 1. Known-floor projection and strict coverage'},
 {'type':'p','html':'Let the forecast-origin information include B, let Y≥B almost surely, and let 0&lt;τ&lt;1. Project any issued report c to max(B,c). Its pinball loss is no larger at every possible Y. A true conditional lower inverse quantile q at level τ=1−α has strict breach probability at most α. Equality is not automatic: an atom at the quantile can make the probability smaller. The lower bound alone need not create an outcome atom; fitted reports do not inherit the population statement.'},
 {'type':'equation','html':'ρ<sub>τ</sub>(Y−c)−ρ<sub>τ</sub>(Y−max(B,c))=τ(B−c)<sub>+</sub>; &nbsp; Pr(Y&gt;q | ℱ<sub>t</sub>)≤α.',
  'latex':r'\rho_\tau(Y-c)-\rho_\tau(Y-\max\{B,c\})=\tau(B-c)_+,\qquad \Pr(Y>q\mid\mathcal F_t)\le\alpha.'},
 {'type':'p','html':'Proof. Below B both errors are nonnegative, so their loss difference is the displayed nonnegative quantity; otherwise the report is unchanged. For the conditional inverse quantile, F(q)≥τ, hence the strict-tail probability is at most α. An atom is a possible reason for strict inequality, not a necessary premise. Accordingly, the retained equality-based coverage tests are diagnostics of their stated nulls, not automatic tests of every valid upper quantile.'},
 {'type':'subheading','text':'Proposition 2. Classical endpoint-to-peak bound'},
 {'type':'p','html':'Let future real increments be independent and individually symmetric about zero. Write S<sub>h</sub> for their partial sums, S<sub>0</sub>=0, and fix an observed starting position x with B=|x|. No identical-distribution or finite-moment assumption is required. If q is the population (1−α/2) quantile of |S<sub>H</sub>|, the report B+q has strict peak-breach probability at most α. This is a direct scalar application of the classical Lévy maximal inequality, not a new inequality.'},
 {'type':'equation','html':'Pr(max<sub>0≤h≤H</sub>|x+S<sub>h</sub>|&gt;B+q)≤Pr(max<sub>h</sub>|S<sub>h</sub>|&gt;q)≤2Pr(|S<sub>H</sub>|&gt;q)≤α.',
  'latex':r'\Pr\!\left(\max_{0\le h\le H}|x+S_h|>B+q\right)\le\Pr\!\left(\max_h|S_h|>q\right)\le2\Pr(|S_H|>q)\le\alpha.'},
 {'type':'p','html':'Proof. The triangle inequality gives the first inclusion; Lévy’s maximal inequality and the inverse-quantile tail bound give the rest. For conditional coverage, independence and symmetry must hold conditional on origin information and q must be the corresponding conditional population quantile. The empirical plug-in L, overlapping historical labels and dependent mean-reverting data do not acquire that guarantee. A generic one-sided endpoint VaR is not the required absolute-displacement quantile. Supplement S15 gives an exact finite counterexample to that substitution; Supplement S11 retains the proof, original simulations and corrected sensitivities.'},
 {'type':'subheading','text':'Proposition 3. Common-pool construction distances'},
 {'type':'p','html':'Use one nonempty historical pool, one available order-statistic rank k, and peaks that include their starting observation. Let F add historical peak headroom to the current B, S translate each historical signed path to x, and K floor the historical-peak order statistic at B. Their differences obey the following deterministic bounds. The common pool and same rank are essential; these are neither forecast-accuracy nor coverage guarantees.'},
 {'type':'equation','html':'|F−K|≤r<sub>abs</sub>=max<sub>i</sub>||N<sub>i</sub>|−B|; &nbsp; |S−K|≤r<sub>signed</sub>=max<sub>i</sub>|N<sub>i</sub>−x|.',
  'latex':r'|F-K|\le r_{\rm abs}=\max_i\bigl||N_i|-B\bigr|,\qquad |S-K|\le r_{\rm signed}=\max_i|N_i-x|.'},
 {'type':'p','html':'Proof. For each historical row, compare the headroom construction and translated path maximum to max(B,P<sub>i</sub>). Projection and the reverse triangle inequality bound their differences by the two anchor distances. A fixed order statistic is nonexpansive for the maximum paired difference, and flooring commutes with that order statistic. Applying these facts yields the displayed bounds. Supplement S2 retains the rowwise derivation and examples where the same observed history permits opposite loss rankings.'}
 ]

def illustration_blocks():
 tau=F(19,20);prob=F(3,100);d=signed_endpoint_example()
 old=pinball(1,1,tau);new=pinball(1,2,tau)
 return [
 {'type':'p','html':f'Artificial marginal example. At each of two future observation times, the position is 1 with probability {prob} and 0 otherwise, starting from 0. Aligning the two positive events gives peak probability {prob}; making them disjoint gives {2*prob}. Each time marginal, including the endpoint, is identical across the two constructions. At quantile level {tau}, their peak quantiles are respectively 0 and 1. Thus endpoint or even all individual-time marginals do not identify the peak quantile without the temporal joint distribution.'},
 {'type':'p','html':f'Artificial endpoint-quantile substitution example. Independent increments have X₁=0 with probability {F(23,25)}, X₁=−3 or 3 each with probability {F(1,25)}, and X₂=−1 or 1 each with probability {F(1,2)}. At level {F(39,40)}, the signed endpoint quantile is {d["signed_endpoint_quantile"]}, whereas the absolute endpoint quantile is {d["absolute_endpoint_quantile"]}. Starting at 0, the sampled-peak probability above the signed threshold is {d["peak_breach_at_signed_threshold"]}, exceeding nominal {1-tau}. The increments satisfy independence and symmetry: the failure is the substitution of the wrong endpoint functional.'},
 {'type':'p','html':f'Artificial floor and horizon examples. A uniform outcome on [B,B+1] satisfies the floor but has no atom at B. For ordered true outcomes (1,1) and reports (2,1), a raise-only long-horizon repair gives (2,2). At τ={tau}, long-horizon pinball loss rises from {old} to {new}; the short report is unchanged. This rejects an unconditional guarantee for that raise-only repair, not for every monotone rearrangement.'}
 ]

def main():
 out=ROOT/'notes/revision-v5-novelty';out.mkdir(parents=True,exist_ok=True)
 d=signed_endpoint_example();co=[(0,F(97,100)),(1,F(3,100))];dis=[(0,F(94,100)),(1,F(6,100))]
 result={'type':'artificial exact examples; not empirical data','same_endpoint_marginal':{'positive_probability':str(F(3,100)),'tau':str(F(19,20)),'comonotone_peak_quantile':quantile(co,F(19,20)),'disjoint_peak_quantile':quantile(dis,F(19,20))},'one_sided_substitution':{k:str(v) if isinstance(v,F) else v for k,v in d.items()},'floor_coverage':{'atom_strict_hit':str(F(3,100)),'nominal_alpha':str(F(1,20))},'blocks':theory_blocks(),'examples':illustration_blocks()}
 (out/'theory-source.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Exact theory illustrations and canonical mathematical source written; no financial data accessed.')
if __name__=='__main__':main()
