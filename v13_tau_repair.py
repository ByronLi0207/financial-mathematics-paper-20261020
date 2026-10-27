"""Predeclared post-failure v13 solver repair; original objective/tolerances.

Financial inputs/selection do not enter this module. See the standalone G1
protocol. Variable rho requires n*rho*u in the original feasible-dual certificate.
"""
import math
import numpy as np
from conditional_quantile import (QuantileFit,QuantileFitError,_training_arrays,
    _real_option,_certificate,_immutable,DUAL_DENOMINATOR)

ATOL=1e-6
RTOL=1e-5
GAP_RTOL=1e-6
MAX_ITER=100000
FIT_EVENTS=[]


def _accepted(beta,iteration,primal,dual,ptol,dtol,cert):
    return QuantileFit(_immutable(beta,np.float64),iteration,
        cert['primal_objective'],cert['dual_objective'],cert['duality_gap'],
        primal,dual,ptol,dtol,cert['gap_tolerance'],
        _immutable(cert['weights'],np.float64),_immutable(cert['numbers'],np.int64),
        DUAL_DENOMINATOR,0,cert['integer_lower'],cert['integer_upper'])


def _options(X,y,tau,penalty):
    X,y=_training_arrays(X,y)
    tau=_real_option(tau,'tau'); penalty=_real_option(penalty,'penalty')
    if tau>=1: raise QuantileFitError('INVALID_OPTION',{'option':'tau'})
    return X,y,tau,penalty


def fit_adaptive_admm(X,y,tau=.99,penalty=.01,checkpoint=None):
    """Cold ADMM, 10x original cap, residual-balanced rho, same certificate."""
    X,y,tau,penalty=_options(X,y,tau,penalty)
    n,p=X.shape; initial_rho=1/n; rho=initial_rho
    regularizer=np.eye(p); regularizer[0,0]=0
    def operator_at(value):
        system=value*(X.T@X)+penalty*regularizer
        right=value*X.T
        operator=np.linalg.solve(system,right)
        error=float(np.linalg.norm(system@operator-right))
        if not np.isfinite(operator).all() or error>1e-9*(1+np.linalg.norm(right)):
            raise QuantileFitError('LINEAR_SOLVE_RESIDUAL')
        return operator
    operator=operator_at(rho)
    beta=np.zeros(p);beta[0]=float(np.quantile(y,tau,method='inverted_cdf'))
    residual=y-X@beta;scaled_dual=np.zeros(n)
    certificate=None; diagnostics={}; rho_updates=0
    for iteration in range(1,MAX_ITER+1):
        with np.errstate(over='raise',divide='raise',invalid='raise'):
            beta=operator@(y-residual-scaled_dual)
            prediction=X@beta
            value=y-prediction-scaled_dual
            previous=residual
            residual=np.maximum(value-tau/(n*rho),0)+np.minimum(value+(1-tau)/(n*rho),0)
            primal_vector=prediction+residual-y
            scaled_dual=scaled_dual+primal_vector
            primal_norm=float(np.linalg.norm(primal_vector))
            dual_norm=float(np.linalg.norm(rho*(X.T@(residual-previous))))
            ptol=float(math.sqrt(n)*ATOL+RTOL*max(np.linalg.norm(prediction),np.linalg.norm(residual),np.linalg.norm(y)))
            dtol=float(math.sqrt(p)*ATOL+RTOL*np.linalg.norm(rho*(X.T@scaled_dual)))
            diagnostics=dict(iterations=iteration,primal_residual=primal_norm,
                dual_residual=dual_norm,primal_tolerance=ptol,dual_tolerance=dtol,
                rho=rho,rho_updates=rho_updates)
            residuals_pass=primal_norm<=ptol and dual_norm<=dtol
            if residuals_pass or iteration==MAX_ITER:
                certificate=_certificate(X,y,beta,n*rho*scaled_dual,tau,penalty,GAP_RTOL)
            if residuals_pass and certificate['duality_gap']<=certificate['gap_tolerance']:
                FIT_EVENTS.append(dict(solver='adaptive-admm',**diagnostics))
                return _accepted(beta,iteration,primal_norm,dual_norm,ptol,dtol,certificate)
            if iteration%50==0:
                if checkpoint is not None:checkpoint(dict(iteration=iteration,solver='adaptive-admm',**{k:v for k,v in diagnostics.items() if k!='iterations'}))
                new=rho
                if primal_norm>10*dual_norm:new=min(1024*initial_rho,2*rho)
                elif dual_norm>10*primal_norm:new=max(initial_rho/1024,rho/2)
                if new!=rho:
                    scaled_dual*=rho/new;rho=new;operator=operator_at(rho);rho_updates+=1
    if certificate is not None:diagnostics.update({k:certificate[k] for k in ('primal_objective','dual_objective','duality_gap','gap_tolerance')})
    FIT_EVENTS.append(dict(solver='adaptive-admm',status='NONCONVERGENCE',**diagnostics))
    raise QuantileFitError('NONCONVERGENCE',diagnostics)


def fit_clarabel(X,y,tau=.99,penalty=.01,checkpoint=None):
    """One cold convex solve, accepted only by unchanged external conditions."""
    import cvxpy as cp
    X,y,tau,penalty=_options(X,y,tau,penalty)
    n,p=X.shape
    if checkpoint is not None: checkpoint(dict(iteration=0,solver='clarabel-start'))
    beta=cp.Variable(p); plus=cp.Variable(n,nonneg=True);minus=cp.Variable(n,nonneg=True)
    equality=X@beta+plus-minus==y
    loss=(tau*cp.sum(plus)+(1-tau)*cp.sum(minus))/n
    objective=cp.Minimize(loss+penalty*cp.sum_squares(beta[1:])/2)
    problem=cp.Problem(objective,[equality])
    problem.solve(solver='CLARABEL',warm_start=False,verbose=False,max_iter=500,
        tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10,time_limit=30.)
    if checkpoint is not None: checkpoint(dict(iteration=int(problem.solver_stats.num_iters or 0),solver='clarabel-end'))
    if problem.status!=cp.OPTIMAL:raise QuantileFitError('CLARABEL_NOT_OPTIMAL',{'status':problem.status})
    b=np.asarray(beta.value,dtype=float).reshape(p)
    residual=np.asarray(plus.value-minus.value,dtype=float)
    prediction=X@b
    # Equality dual nu has raw weights=-n*nu. Original _certificate takes -weights.
    cert=_certificate(X,y,b,n*np.asarray(equality.dual_value,dtype=float),tau,penalty,GAP_RTOL)
    weights=cert['weights']
    moment=X.T@weights/n
    stationary=penalty*np.r_[0.,b[1:]]-moment
    primal_norm=float(np.linalg.norm(prediction+residual-y))
    dual_norm=float(np.linalg.norm(stationary))
    ptol=float(math.sqrt(n)*ATOL+RTOL*max(np.linalg.norm(prediction),np.linalg.norm(residual),np.linalg.norm(y)))
    dtol=float(math.sqrt(p)*ATOL+RTOL*np.linalg.norm(moment))
    diagnostics=dict(iterations=int(problem.solver_stats.num_iters or 0),
        primal_residual=primal_norm,dual_residual=dual_norm,primal_tolerance=ptol,
        dual_tolerance=dtol,duality_gap=cert['duality_gap'],gap_tolerance=cert['gap_tolerance'])
    if not (primal_norm<=ptol and dual_norm<=dtol and cert['duality_gap']<=cert['gap_tolerance']):
        raise QuantileFitError('CLARABEL_EXTERNAL_CERTIFICATE_FAILED',diagnostics)
    FIT_EVENTS.append(dict(solver='clarabel',**diagnostics))
    return _accepted(b,diagnostics['iterations'],primal_norm,dual_norm,ptol,dtol,cert)


def fit_repaired(X,y,tau=.99,penalty=.01,checkpoint=None):
    """The single declared ADMM->Clarabel sequence, never a model substitution."""
    X,y,tau,penalty=_options(X,y,tau,penalty)
    try:return fit_adaptive_admm(X,y,tau=tau,penalty=penalty,checkpoint=checkpoint)
    except QuantileFitError as exc:
        if exc.code!='NONCONVERGENCE': raise
    return fit_clarabel(X,y,tau=tau,penalty=penalty,checkpoint=checkpoint)
