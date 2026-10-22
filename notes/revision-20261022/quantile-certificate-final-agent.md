# Final read-only rationale check: ridge quantile numerical certificate

22 October 2026. Scope: current `conditional_quantile.py` (SHA-256 `2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7`), its implementation note, and current main-paper Appendix C. No financial observations or prediction arrays, new dependency, numerical fit, new test, or repeat of the existing 16/156-test suites was used. No frozen code, result or manuscript was edited.

**Finding: no new material defect in the inspected certificate rationale.** The exact zero-sum construction already present in this implementation resolves the suggested unpenalized-intercept feasibility concern; replacing it conceptually with a floating near-zero sum would misdescribe the code.

For n training responses, write `X=[1,Z]`, coefficients `(b0,b)`, errors `e=y-b0*1-Z*b`, and primal objective `P=mean(rho_tau(e))+lambda*||b||^2/2`. The identity `rho_tau(e)=max_{tau-1<=nu<=tau} nu*e` gives the dual after minimizing over coefficients:

```
sum(nu)=0,
a=Z'nu/n,
D(nu)=nu'y/n-||a||^2/(2*lambda).
```

The intercept constraint is exact in this mathematical dual; the slope stationarity condition is `b=a/lambda`. With a feasible witness, the exact-arithmetic objective difference decomposes as

```
P-D = mean(rho_tau(e)-nu*e)
      + lambda*||b-a/lambda||^2/2.
```

The first term is `(tau-nu)*e` at nonnegative errors and `(nu-(tau-1))*(-e)` at negative errors. Both are nonnegative under the dual box. These are the signs, n-normalization and ridge factor used in `_certificate`; the intercept term vanishes because the witness has exact zero sum. The displayed primal and dual in Appendix C use the same normalized response and standardized slope design.

`_dual_projection` need not return the exact Euclidean projection of the current iterate to provide this witness. After bisection it truncates to a `2^-40` grid, uses inward integer bounds computed from the exact rational representation of the input binary float tau, and repairs/checks the integer sum with Python integers. Each numerator lies between approximately `-2^40` and `2^40`, so its float64 conversion is exact; division by `2^40` is also exact. The represented dyadic vector therefore satisfies the real-arithmetic box and zero-sum constraints exactly, including the unpenalized intercept constraint. This is not an approximate-sum argument.

The ADMM sign is consistent: the constraint is `X*beta+r-y=0`, scaled multiplier is u, and the quantile dual uses `nu=-n*rho*u`; at the chosen theoretical `rho=1/n` this motivates projecting `-u`. Exact correspondence to the current multiplier is not required for feasibility of the separately constructed dual witness. The beta normal system, asymmetric residual proximity thresholds and dual residual `rho*X'*(r-r_old)` have the corresponding signs and mean-loss normalization.

The numerical acceptance boundary is narrower than a formal real-arithmetic optimum enclosure. Matrix products, the primal and dual objective values, the Fenchel decomposition and the identity check are float64 evaluations. The returned positive decomposition is checked against `P-D` within the declared roundoff bound and against `gap_rtol*(1+abs(P))`, in addition to both ADMM residual conditions. Appendix C explicitly says the integer checksum applies to the represented witness while objective evaluations remain floating point, and that this is not interval-arithmetic certification or a statistical forecasting guarantee. That is an accurate account of the current implementation. Finite residual/gap checks do not establish conditional coverage, economic value, or universal accuracy for arbitrary ill-conditioned inputs, and the paper does not import those implications.

The fitter's tau and complementary `1-tau` follow its binary-float objective. The paper also discloses that final scoring obtains 19/20 and 1/20 separately, so no exact-identity claim between all floating training and scoring expressions is needed. No new numerical result or independent reconstruction of historical hidden coefficient vectors is asserted by this rationale review.
