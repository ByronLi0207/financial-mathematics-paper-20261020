"""Post-result inference helpers. NumPy plus standard library; no installation.

References/working assumptions and the predeclared bandwidth are recorded in
results/revision-20261023/inference-design.md. No original forecast is changed.
"""
import math
import numpy as np

def vector(x):
    x=np.asarray(x,dtype=float)
    if x.ndim!=1 or not len(x) or not np.isfinite(x).all():raise ValueError('finite nonempty vector required')
    return x

def beta_fraction(a,b,x):
    # Continued fraction (modified Lentz) for regularized incomplete beta.
    tiny=1e-300;c=1.;d=1-(a+b)*x/(a+1)
    if abs(d)<tiny:d=tiny
    d=1/d;h=d
    for m in range(1,10001):
        aa=m*(b-m)*x/((a+2*m-1)*(a+2*m))
        d=1+aa*d;c=1+aa/c
        if abs(d)<tiny:d=tiny
        if abs(c)<tiny:c=tiny
        d=1/d;h*=d*c
        aa=-(a+m)*(a+b+m)*x/((a+2*m)*(a+2*m+1))
        d=1+aa*d;c=1+aa/c
        if abs(d)<tiny:d=tiny
        if abs(c)<tiny:c=tiny
        d=1/d;delta=d*c;h*=delta
        if abs(delta-1)<3e-14:return h
    raise ArithmeticError('beta fraction did not converge')

def regularized_beta(x,a,b):
    if x<=0:return 0.
    if x>=1:return 1.
    front=math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)+a*math.log(x)+b*math.log1p(-x))
    if x<(a+1)/(a+b+2):return front*beta_fraction(a,b,x)/a
    return 1-front*beta_fraction(b,a,1-x)/b

def student_two_sided(t,df):
    if df<=0:raise ValueError('positive degrees of freedom required')
    return min(1.,max(0.,regularized_beta(df/(df+float(t)**2),df/2,.5)))

def chi_tail(x,df):
    if x<0 or df<=0:raise ValueError('invalid chi-square arguments')
    if df==1:return math.erfc(math.sqrt(x/2))
    if df==2:return math.exp(-x/2)
    if x==0:return 1.
    a=df/2;z=x/2;front=math.exp(-z+a*math.log(z)-math.lgamma(a))
    if z<a+1:
        term=1/a;total=term
        for n in range(1,10000):
            term*=z/(a+n);total+=term
            if abs(term)<abs(total)*1e-14:return max(0.,1-total*front)
    else:
        tiny=1e-300;b=z+1-a;c=1/tiny;d=1/b;h=d
        for n in range(1,10000):
            an=-n*(n-a);b+=2;d=an*d+b;c=b+an/c
            if abs(d)<tiny:d=tiny
            if abs(c)<tiny:c=tiny
            d=1/d;delta=d*c;h*=delta
            if abs(delta-1)<1e-14:return max(0.,min(1.,front*h))
    raise ArithmeticError('gamma did not converge')

def bandwidth(n,h):return min(n-1,max(h,int(4*(n/100)**(2/9))))

def hac(x,L):
    x=np.asarray(x,float)
    if x.ndim==1:x=x[:,None]
    n=len(x);u=x-x.mean(axis=0);v=u.T@u/n
    for k in range(1,L+1):
        gamma=u[k:].T@u[:-k]/n
        v+=(1-k/(L+1))*(gamma+gamma.T)
    return v

def dm_test(d,h,L=None):
    d=vector(d);n=len(d)
    if n<=h or h<1:raise ValueError('more observations than horizon required')
    L=bandwidth(n,h) if L is None else L
    if not h<=L<n:raise ValueError('bandwidth must be >=H and <n')
    mean=math.fsum(map(float,d))/n;v=float(hac(d,L)[0,0])
    out=dict(n=n,horizon=h,bandwidth=L,mean_difference=mean,lrv=v,dm_t=None,dm_p=None,hln_t=None,hln_p=None)
    if v<=0 or np.all(d==d[0]):
        out['status']='IDENTICAL_LOSSES' if np.all(d==0) else 'ZERO_LONG_RUN_VARIANCE';return out
    t=mean/math.sqrt(v/n);factor=math.sqrt((n+1-2*h+h*(h-1)/n)/n)
    out.update(status='OK',dm_t=t,dm_p=math.erfc(abs(t)/math.sqrt(2)),hln_t=t*factor,hln_p=student_two_sided(t*factor,n-1))
    return out

def log_bernoulli(k,n,p):
    if (k and p==0) or (n-k and p==1):return -math.inf
    return (k*math.log(p) if k else 0.)+((n-k)*math.log1p(-p) if n-k else 0.)

def coverage_tests(hits,p=.05):
    h=vector(hits)
    if not np.isin(h,[0,1]).all() or not 0<p<1:raise ValueError('binary hits and interior probability required')
    n=len(h);k=int(h.sum());rate=k/n
    uc=max(0.,2*(log_bernoulli(k,n,rate)-log_bernoulli(k,n,p)))
    counts=np.zeros((2,2),int)
    for a,b in zip(h[:-1],h[1:]):counts[int(a),int(b)]+=1
    out=dict(n=n,hits=k,rate=rate,pof_lr=uc,pof_p=chi_tail(uc,1),ind_lr=None,ind_p=None,cc_lr=None,cc_p=None,ind_status='UNIDENTIFIED_TRANSITION_ROW',boundary=bool((counts==0).any()))
    out.update({f'n{i}{j}':int(counts[i,j]) for i in range(2) for j in range(2)})
    n0,n1=counts.sum(axis=1)
    if n0 and n1:
        pi=float(counts[:,1].sum()/(n-1));ll0=log_bernoulli(int(counts[:,1].sum()),n-1,pi)
        ll1=sum(log_bernoulli(int(counts[i,1]),int(counts[i].sum()),float(counts[i,1]/counts[i].sum())) for i in range(2))
        ind=max(0.,2*(ll1-ll0));cc=uc+ind
        out.update(ind_lr=ind,ind_p=chi_tail(ind,1),cc_lr=cc,cc_p=chi_tail(cc,2),ind_status='BOUNDARY_REFERENCE' if out['boundary'] else 'OK')
    return out

def dq_hac(hits,capacity,h):
    hits=vector(hits);c=vector(capacity)
    if len(hits)!=len(c) or not np.isin(hits,[0,1]).all():raise ValueError('aligned binary hits required')
    lags=list(range(h+1,h+5));start=max(lags);x=hits-.05;n=len(hits)-start
    if n<10:return dict(status='TOO_SHORT',n=max(0,n),df=None,stat=None,p=None)
    level=c[start:];sd=float(level.std());level=(level-level.mean())/sd if sd else np.zeros_like(level)
    Z=np.column_stack([np.ones(n),*[x[start-len_lag:len(hits)-len_lag] for len_lag in lags],level])
    g=Z*x[start:,None];L=bandwidth(n,h);S=hac(g,L);q=Z.shape[1]
    if np.linalg.matrix_rank(Z)<q or np.linalg.matrix_rank(S)<q:return dict(status='RANK_DEFICIENT',n=n,df=q,stat=None,p=None,bandwidth=L)
    if not np.isfinite(S).all() or float(np.linalg.eigvalsh(S)[0])<=0:return dict(status='NONPOSITIVE_COVARIANCE',n=n,df=q,stat=None,p=None,bandwidth=L)
    stat=float(n*g.mean(axis=0)@np.linalg.solve(S,g.mean(axis=0)))
    if stat<0:return dict(status='NONPOSITIVE_COVARIANCE',n=n,df=q,stat=None,p=None,bandwidth=L)
    return dict(status='OK',n=n,df=q,stat=stat,p=chi_tail(stat,q),bandwidth=L)

def holm(pvalues):
    p=vector(pvalues)
    if np.any((p<0)|(p>1)):raise ValueError('probabilities required')
    order=np.argsort(p,kind='stable');out=np.zeros(len(p));running=0.
    for i,j in enumerate(order):running=max(running,(len(p)-i)*p[j]);out[j]=min(1.,running)
    return out

def elementary(x,y,theta,tau=.95):
    return ((float(y<x)-tau)*(float(theta<x)-float(theta<y)))

def murphy(a,b,y,tau=.95):
    a=vector(a);b=vector(b);y=vector(y)
    if not len(a)==len(b)==len(y):raise ValueError('aligned inputs required')
    theta=np.unique(np.concatenate([a,b,y]));sa=np.zeros(len(theta));sb=sa.copy()
    # Event accumulation gives the exact step diagram without n×threshold memory.
    for x,out in [(a,sa),(b,sb)]:
        delta=np.zeros(len(theta)+1)
        for xx,yy in zip(x,y):
            low,high=sorted((xx,yy));weight=(1-tau) if xx>yy else tau
            lo=int(np.searchsorted(theta,low));hi=int(np.searchsorted(theta,high))
            delta[lo]+=weight/len(y);delta[hi]-=weight/len(y)
        out[:]=np.cumsum(delta[:-1]);out[np.abs(out)<1e-14]=0.
    diff=sa-sb;tol=64*np.finfo(float).eps*max(1.,float(np.max(np.abs(sa))),float(np.max(np.abs(sb))))
    pos=bool(np.any(diff>tol));neg=bool(np.any(diff<-tol))
    ranking='CROSSING' if pos and neg else ('LEFT_DOMINATES_SAMPLE' if neg else ('RIGHT_DOMINATES_SAMPLE' if pos else 'EQUAL_SAMPLE'))
    loss=lambda x:tau*np.maximum(y-x,0)+(1-tau)*np.maximum(x-y,0)
    return dict(theta=theta,left=sa,right=sb,difference=diff,ranking=ranking,arithmetic_tolerance=tol,integral_difference=float(np.diff(theta)@diff[:-1]),pinball_difference=float(np.mean(loss(a)-loss(b))))
