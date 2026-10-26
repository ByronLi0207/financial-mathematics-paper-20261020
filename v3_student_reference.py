"""Bounded independent numerical readback of retained Student-reference p values.

The production kernel uses an incomplete-beta continued fraction. This audit
integrates the Student density after x=sqrt(df)*tan(angle), using fixed
Gauss-Legendre quadrature. It loads no raw observations and fits no model.
Numerical agreement does not validate an asymptotic statistical reference.
"""
import sys,os
sys.dont_write_bytecode=True
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import argparse,csv,hashlib,json,math
from functools import lru_cache
from pathlib import Path
import numpy as np

@lru_cache(maxsize=4)
def nodes(order):
    if order not in (128,256):raise ValueError('audit quadrature orders128/256 only')
    return np.polynomial.legendre.leggauss(order)

def student_angle_tail(t,df,order):
    t=float(t)
    if not math.isfinite(t) or abs(t)>32 or not 1<=df<=10000 or int(df)!=df:raise ValueError('outside bounded reference-audit domain')
    z,w=nodes(order);lo=math.atan(abs(t)/math.sqrt(df));span=math.pi/2-lo
    angles=lo+(z+1)*span/2
    factor=math.exp(math.lgamma((df+1)/2)-math.lgamma(df/2)-.5*math.log(math.pi))
    return float(factor*span*np.dot(w,np.exp((df-1)*np.log(np.cos(angles)))))

def readback(rows):
    checks=[];skipped=[];seen=set()
    for row in rows:
        identity=row['contrast_id']
        if identity in seen:raise ValueError('duplicate contrast')
        seen.add(identity)
        if row['status']!='OK':
            if row['hln_t'] or row['hln_p']:raise ValueError('undefined row has reference statistic')
            skipped.append(identity);continue
        t=float(row['hln_t']);df=int(row['n'])-1;p=float(row['hln_p'])
        if not math.isfinite(p) or not 0<p<=1:raise ValueError('positive finite retained tail required')
        low=student_angle_tail(t,df,128);high=student_angle_tail(t,df,256)
        absolute=abs(high-p);relative=absolute/p;convergence=abs(high-low)/max(high,low)
        if absolute>1e-9 or relative>1e-8 or convergence>1e-8:raise AssertionError('reference disagreement: '+identity)
        checks.append(dict(contrast_id=identity,df=df,retained_hln_p=p,angle128_p=low,angle256_p=high,absolute_error=absolute,relative_error=relative,relative_quadrature_change=convergence))
    if not checks:raise ValueError('at least one defined row required')
    return dict(status='NUMERICAL_READBACK_AGREES',checked_rows=len(checks),skipped_rows=len(skipped),skipped_ids=skipped,max_absolute_error=max(x['absolute_error'] for x in checks),max_relative_error=max(x['relative_error'] for x in checks),max_relative_quadrature_change=max(x['relative_quadrature_change'] for x in checks),absolute_comparison_tolerance=1e-9,relative_comparison_tolerance=1e-8,quadrature_orders=[128,256],method='Student density under tangent substitution; independent of production beta continued fraction',scope='retained scalar p-value arithmetic only; no loss, HAC, forecast or asymptotic-validity recomputation',checks=checks)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,default=Path(__file__).resolve().parent/'results/revision-20261023/inference/dm.csv');args=parser.parse_args()
    raw=args.input.read_bytes();rows=list(csv.DictReader(raw.decode('utf8').splitlines()));result=readback(rows)
    result.update(input_sha256=hashlib.sha256(raw).hexdigest(),input_name=args.input.name)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
