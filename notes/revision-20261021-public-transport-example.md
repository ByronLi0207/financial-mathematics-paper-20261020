# Research note: reanchoring a path does not establish its conditional law

21 October 2026. This is an analytical research note, not a new empirical result or a revised final manuscript. No fitted model, simulated sample or new evaluation record is used below.

The study compares historical native headrooms with inventory increments reanchored at the current signed position. Historical simulation and conditional risk modelling are mature ideas; see [Pritsker, FEDS2001-27](https://www.federalreserve.gov/pubs/feds/2001/200127/200127pap.pdf). The following elementary examples clarify the particular anchor assumption for a sampled inventory peak. They are not offered as a new forecasting algorithm.

## Definitions

Let H≥1, let the current level be x, and write B=|x|. For a historical path Z_0,...,Z_H, define

$$
 G=\max_{0\le h\le H}|Z_h|-|Z_0|,\qquad
 A_x=\max_{0\le h\le H}|x+Z_h-Z_0|.
$$

With q_tau denoting a lower population quantile, the two population capacities are

$$
 C_F(x)=B+q_\tau(G),\qquad C_S(x)=q_\tau(A_x).
$$

These are population counterparts of the empirical constructions. Their definition does not impose the finite study's corrected sample rank.

## A bounded example

Suppose inventory levels are IID and take −c or c with equal probability, c>0. Every actual peak equals c, and every native headroom equals zero. Thus C_F(x)=c for either possible current state.

For x=c, a historical path reanchors to a peak3c exactly when Z_0=−c and at least one subsequent Z_h=c. This has probability

$$
 w_H=\tfrac12(1-2^{-H}).
$$

Otherwise its reanchored peak is c. Consequently C_S(c)=3c whenever

$$
 \tau>1-w_H=\tfrac12+2^{-(H+1)}.
$$

The negative current state is symmetric. Matching the historical anchor exactly to x instead gives a peak c. Hence even exact agreement of **local** native and reanchored constructions cannot bound the **full-pool** reanchored construction.

The levels are IID; their increments are not IID or independent of their starting levels. A stationary marginal increment law is not sufficient to justify transporting that law to every current level. This example does not describe an observed dealer's policy.

## Continuous signed states and a nonzero headroom distribution

The same issue occurs with continuous signed inventory. Let levels be IID from an equal mixture of uniforms on

$$
 [-c-e,-c+e]\quad\text{and}\quad[c-e,c+e],\qquad0<e<c/2.
$$

Absolute levels are uniform on[c−e,c+e]. For g=2ea,0≤a≤1, integrating over the historical starting absolute level gives

$$
 F_G(g)=\int_0^{1-a}(u+a)^H\,du+a
 =a+\frac{1-a^{H+1}}{H+1}.
$$

The native headroom has probability mass1/(H+1) at zero, but its density is positive on0<g<2e. Since

$$
 F_G(e)=\frac12+\frac{1-2^{-(H+1)}}{H+1}\le\frac78,
$$

any fixed tau in(7/8,1) has a unique native headroom quantile g_F in(e,2e).

Consider current states B≥c, which have probability1/2. All actual future peaks satisfy P≤c+e, while C_F=B+g_F>c+e. The historical event with an opposite-sign anchor and a subsequent level of the current sign has probability w_H and produces A_x≥B+2c−2e. Because tau>1−w_H,

$$
 C_S(x)\ge B+2c-2e>B+2e>C_F(x)>P.
$$

With pinball loss rho_tau, every possible future realization in those states therefore satisfies

$$
 \rho_\tau(P-C_S)-\rho_\tau(P-C_F)
 =(1-\tau)(C_S-C_F)>0.
$$

This establishes a possible construction effect with continuous signed states and a regular positive upper quantile. The response still has its natural zero atom. It does not establish an overall ranking across all states. F itself overpredicts here and is explicitly not the conditional optimum: beating S does not make F optimal.

## Relation to a local historical comparator

For the same nonempty selected historical set J and the same valid order rank k, write r=max_{i in J}|N_i−x|. Reanchored headroom g_i(x)=max_h|x+N_{i+h}−N_i|−|x| is2-Lipschitz in x. Order statistics are1-Lipschitz in the coordinatewise maximum norm. Therefore

$$
 |C_F^J(x)-C_S^J(x)|\le2r.
$$

This deterministic bound permits ties, atoms and overlapping historical labels. It requires the **same set and rank**. It does not control the change from J to the entire historical pool, forecast error or coverage. Shrinking state distance alone also does not remove the estimation noise of a fixed number of neighbours.

Local empirical quantiles are a mature reference; [Biau and Patra, arXiv0908.2503v2](https://arxiv.org/abs/0908.2503v2) study a complete sequential nearest-neighbour aggregation strategy under explicit assumptions. The current finite rolling, delayed-label task is not that strategy and inherits no consistency theorem merely from using neighbours. [Wisniewski, Lindsay and Lindsay2020](https://proceedings.mlr.press/v128/wisniewski20a.html) already use inventory history, calendar features and conditional interval methods on the source dataset, for a next-hour signed endpoint rather than this multi-record absolute peak.

The examples motivate a carefully named conditional comparison. They do not identify the actual FX record's mechanism, establish a new method, validate a live risk limit, or alter the original frozen results. Any later extension on the already inspected evaluation record must remain explicitly exploratory.
