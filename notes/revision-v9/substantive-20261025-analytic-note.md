# Analytic qualifications for the history and horizon arguments

This note records new reasoning on the existing design. It neither re-estimates a forecast nor changes a stored result. The claims below concern the information conveyed by the experiments and the scope of an older horizon-repair sentence. They are elementary qualifications, not claims of a new general estimator or inequality.

## A. Which coordinates can the confirmation distinguish?

For a fixed method m with the declared positive coefficient count p_m, the candidate coordinates satisfy

\[
c=\frac{W}{H+1},\qquad b=\frac{W}{(H+1)p_m}=\frac{c}{p_m}.
\]

The discovery code first selects a coordinate using a pooled classifier, then estimates a separate curve and cutpoint for each method. The pooled classifier may distinguish the candidates because p_m differs between methods. The subsequent method-specific construction has a different invariance.

Positive constant scaling preserves the order and equality classes of abscissae. If a crossing is linearly interpolated between adjacent points (x_0,y_0),(x_1,y_1), its location is

\[
r=x_0+(x_1-x_0)\frac{y_0}{y_0-y_1}.
\]

Replacing every x by x/p_m replaces r by r/p_m. It leaves the crossing directions, number of crossings and censoring statuses unchanged. This argument applies separately to each existing resampling draw, so its endpoint interval scales in the same way. Zero and unbounded endpoints keep their statuses.

Consequently the method-specific screen regions are algebraically identical:

\[
b<r_b/2\iff c<r_c/2,
\qquad b>2r_b\iff c>2r_c.
\]

Likewise, a b-based interval mapped to history has the same endpoints as the c-based interval:

\[
(H+1)p_m[\ell_b,u_b]=(H+1)[\ell_c,u_c].
\]

Thus the later short/long-history screens and financial interval transfers have no design-based ability to choose between these normalizations when each method receives its own cutpoint. This is an exact-arithmetic property of the definitions; no alternate floating-point run or bitwise numerical equivalence is claimed. Numerical rounding at an exact boundary would not identify a complexity mechanism.

The accepted outcomes remain results about the prespecified procedures and history regions. They supply no additional discrimination of whether coefficient count belongs in this coordinate. This is stronger than observing a tied discovery classification score, and distinct from the failed universal simplification comparison.

Source links: `v9_posthoc.py` functions `metric_value`, `group_curve`, `describe_crossings`, `bootstrap_roots`, and the per-method loop in `main`; `v9_confirmation.py` screen predicates; the unchanged WP1 and WP3 protocols. Existing code and result archives are retained.

## B. The discovery cutpoint and the financial crossing are different objects

The discovery code pools a method's simulation cells across horizons and process settings before grouping and sorting by the selected coordinate. In the saved original-regression curve, the adjacent points defining the first crossing come from W720/H6 and W2880/H24. The stored cutpoint follows the frozen interpolation rule correctly, but its neighbors change both history and horizon.

This is a grid-summary cutpoint of the pooled display. It is not, by itself, the amount of history at which a fixed-horizon learning curve crosses zero. Nor does the absence of common coordinate values across the horizon grids demonstrate that the horizon normalization collapses distinct tasks onto one response curve.

A paper counterexample makes the identification issue explicit: a relative-loss function that depends on W alone, with positive values at the shorter histories and a negative value at the longest discovery history, can still generate the same type of crossing between those cross-horizon neighbors after sorting by c. The pooled crossing therefore does not isolate an effect of dividing history by horizon. This is an analytic possibility, not a fitted alternative DGP or a new reported experiment.

The financial curves instead keep a specified horizon and evaluation record fixed while changing W, with their own changing matched reference. Agreement with a band transferred from the pooled discovery summary is a conditional consistency check across these objects. The existing retrospective, censored and nonmonotone qualifications continue to apply. No separate horizon-specific discovery roots have been estimated here.

For context, Viering and Loog distinguish learning curves for a fixed problem from averages over a distribution of problems in [Section 2.1 of their review](https://arxiv.org/pdf/2103.10948). Their definition does not validate this paper's coordinate; the present qualification follows directly from the local pooling and interpolation code.

## C. Equal completed-label pools do not imply equal total information footprints

The matched comparisons genuinely share the rolling pool of completed fitting labels and the refit clock. Conditional features additionally use issue-known raw lookback, and the regression's penalty selection uses its fixed validation segment. W counts mature response origins; it does not measure every raw observation consulted in feature construction or every observation used in tuning.

The comparison is consequently between forecasting procedures matched on specified dimensions. It does not isolate architecture from all other information choices merely by using the same W. This requires a wording correction, not the replacement of any result or a claim that the chronological design leaked future labels.

[Giacomini and White (2006)](https://doi.org/10.1111/j.1468-0262.2006.00718.x) treat estimation choices and data use as parts of the forecasting method. The relevant local evidence is `conditional_features.py`'s feature lookback and mature-pool construction, `conditional_study.py`'s fitting path, the historical F branch of `v8_mechanism_mc.py`, and the fixed validation stage of `run_v9_learning_curve.py`.

## D. Horizon sorting: aggregate loss and marginal loss

At a common issue origin, let the realized short- and long-horizon peaks satisfy y_s<=y_l. Suppose their already available reports cross: a>b. Use the same quantile level tau and common units, and score the equally weighted sum of the two horizon losses. Sorting reports into horizon order replaces (a,b) by (b,a).

Using rho_tau(y-c)=tau(y-c)+(c-y)_+, the original sum minus the sorted sum is

\[
\begin{aligned}
D={}&\rho_\tau(y_s-a)+\rho_\tau(y_l-b)
       -\rho_\tau(y_s-b)-\rho_\tau(y_l-a)\\
 ={}&(a-y_s)_+-(b-y_s)_+-(a-y_l)_++(b-y_l)_+\\
 ={}&\int_b^a[\mathbf1\{u>y_s\}-\mathbf1\{u>y_l\}]\,du\\
 ={}&\operatorname{length}([b,a]\cap[y_s,y_l])\ge0.
\end{aligned}
\]

The report transformation uses no future outcome; future outcomes occur only in the proof of its score property. If both reports respect the same observed floor B, sorting preserves that feasibility. The guarantee concerns aggregate equal-weight loss. It provides no horizon-by-horizon score guarantee, no arbitrary-weight or differently normalized score guarantee, and no guarantee for breach counts or conditional coverage.

The old Supplement correctly says that raising a long-horizon report can worsen its pinball loss. Its following statement that target ordering does not identify a universally beneficial repair is too broad if read as an aggregate-loss assertion. The original constructed-example source already restricts its counterexample to a raise-only repair (`notes/revision-v5-novelty/theory-source.json`). This note explicitly corrects the broader reading while preserving the protected old Supplement and every crossing count. No sorted forecasts or new empirical losses have been computed.

The related monotone-rearrangement literature is relevant background, with an important distinction. [Chernozhukov, Fernández-Val and Galichon, Proposition 4](https://arxiv.org/pdf/0704.3649) establish an Lp estimation-error improvement for a quantile curve rearranged over its probability index. That proposition is not the fixed-tau, cross-horizon samplewise pinball identity above; the identity has its own elementary proof.

## E. Which true quantile is ordered?

For nested peaks under the same issue-information law and quantile level, their conditional CDFs satisfy F_s(z)>=F_l(z). Taking the same lower-inverse selection therefore gives q^-_tau(H_s)<=q^-_tau(H_l), with atoms and flat intervals allowed. This is the convention already used in the Supplement.

The quantile functional can be set-valued. Choosing different members of the optimal intervals at different horizons can produce crossing optimal reports even when the distributions coincide. Crossing is thus a coherence diagnostic relative to the declared selection convention; it does not on its own establish marginal misspecification. [Ehm et al., Section 2.1](https://arxiv.org/pdf/1503.08195v2) explicitly define the potentially set-valued quantile functional; Section 2.2 gives the consistent scoring form. The main text should make its lower-inverse convention explicit when asserting ordering.

## Verification and scope

The identities in A and D were derived independently by the investigator and an independent same-model reviewer. Their assumptions and conclusions must be checked again in the manuscript integration. No random draw, fit, hypothesis test, bootstrap rerun, empirical loss recomputation or change to archived numbers is used. Existing numerical evidence remains exactly what it was; these qualifications change the permissible interpretation.
