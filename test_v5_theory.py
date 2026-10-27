import importlib,importlib.util
from fractions import Fraction as F

def api():
 assert importlib.util.find_spec('v5_theory') is not None, 'the exact theory verification API must exist'
 return importlib.import_module('v5_theory')

def test_floor_projection_pointwise():
 m=api()
 for tau in (F(1,20),F(1,2),F(19,20)):
  for B in (0,2):
   for y in (B,B+1,B+9):
    for c in (-3,0,1,5,12):assert m.pinball(y,max(c,B),tau)<=m.pinball(y,c,tau)

def test_atom_quantile_has_strict_breach_below_alpha():
 m=api();dist=[(0,F(97,100)),(1,F(3,100))]
 q=m.quantile(dist,F(19,20));assert q==0
 assert sum(w for y,w in dist if y>q)==F(3,100)<F(1,20)

def test_same_endpoints_and_marginals_different_peak_quantiles():
 m=api();co=[((0,0,0),F(97,100)),((0,1,1),F(3,100))]
 dis=[((0,0,0),F(94,100)),((0,1,0),F(3,100)),((0,0,1),F(3,100))]
 for h in (1,2):assert m.distribution([(p[h],w) for p,w in co])==m.distribution([(p[h],w) for p,w in dis])
 assert m.quantile([(max(p),w) for p,w in co],F(19,20))==0
 assert m.quantile([(max(p),w) for p,w in dis],F(19,20))==1

def test_one_sided_endpoint_quantile_cannot_replace_absolute_quantile():
 m=api();d=m.signed_endpoint_example();assert d['signed_endpoint_quantile']==2;assert d['absolute_endpoint_quantile']==4;assert d['peak_breach_at_signed_threshold']==F(2,25)>F(1,20)

def test_common_pool_same_rank_construction_bounds():
 m=api()
 paths=[[-2,1,3],[0,-1,2],[4,2,-3],[1,7,2]]
 for x in (-5,0,2,9):
  for rank in range(1,len(paths)+1):
   d=m.constructions(paths,x,rank)
   assert abs(d['F']-d['K'])<=d['r_abs'];assert abs(d['S']-d['K'])<=d['r_signed']

def test_raise_only_monotonicization_can_increase_loss():
 m=api();tau=F(19,20)
 assert m.pinball(1,10,tau)>m.pinball(1,1,tau)
