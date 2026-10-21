# Research design progress: sampled inventory peaks

**Design draft in progress — topic provisional; no forecasting results.** Six hours (21,600 seconds) of active primary-literature reading were audited as completed at **02:38:58 UTC on 21 October 2026**. The approximately two-hour design stage remains in progress. This note records the current proposal, not a frozen protocol or completed study. All numerical settings below remain provisional, and no forecast outcomes have been inspected.

## Narrow question and financial object

The provisional question is whether historical additional-headroom labels predict a future sampled inventory peak better than historical increment ranges revalued at the current inventory state. The target is the maximum absolute USD net position across the current record and the next $H$ recorded observations:

\[
P_{t,H}=\max_{0\le h\le H}|N_{t+h}|,
\qquad G_{t,H}=P_{t,H}-|N_t|.
\]

The reported capacity must satisfy $C_t\ge|N_t|$. This is a recorded-position exposure target, not a cash requirement, collateral or margin buffer, counterfactual trading policy, or maximum over unobserved continuous hours. Gaps in the observation calendar are retained; $H$ denotes records rather than elapsed hours. Source units and retrospective availability do not establish a real-time release history.

## Proposed comparison

All methods would use the same completed historical origins and empirical quantile rule $Q_\tau$.

- **F, historical headroom:** $C_F=|N_t|+Q_\tau(G_{i,H})$. Each historical label retains its own origin state.
- **S, current-anchor extrema:** define historical increments $\Delta_{i,h}=N_{i+h}-N_i$, their minimum $a_i$ and maximum $b_i$, including $h=0$. Revalue the two extrema at today's state: $A_i(N_t)=\max(N_t+b_i,-N_t-a_i)$, then $C_S=Q_\tau(A_i(N_t))$. This construction needs two extrema, not the full interior path.
- **R, mechanical radius reference:** $D_{i,H}=\max_h|\Delta_{i,h}|$, with $C_R=|N_t|+Q_\tau(D_{i,H})$.
- **L, level reference:** $C_L=\max\{|N_t|,Q_\tau(P_{i,H})\}$.
- **P0, persistence reference:** $C_{P0}=|N_t|$.

F and S forecast the same response but pool historical states differently. Neither generally orders the other. Both are mechanically no larger than R under matched origins and ranks; that ordering cannot serve as an empirical discovery. L and P0 provide simple reference forecasts that must be allowed to outperform the proposed constructions.

## Proposed chronology and evaluation

The main settings under consideration are **$H=6$ recorded steps, $n=720$ completed origins and $\tau=0.95$**. The quantile rank is exactly $k=\lceil(n+1)\tau\rceil=685$: retain ties and use the kth smallest value without interpolation. The general procedure returns positive infinity when $k=n+1$, rather than substituting a sample maximum.

At issue index $t$, origin $i$ is eligible only when $i+H\le t$. The common calibration set would therefore be $\{t-H-n+1,\ldots,t-H\}$. The proposed chronological holdout begins in **2016** and continues through eligible later records. Forecasts would use only information available by issuance; subsequent holdout observations could enter later calibration only after their labels are complete. Settings and eligibility rules must be frozen before forecasting or scoring that holdout.

The proposed primary comparison is paired quantile-consistent loss for F versus S. Capacity, exceedance frequency and overrun severity would be reported separately. Peak and headroom errors are identical after translation and will not be counted as independent evidence. Overlapping labels and temporal dependence prevent an automatic independent-sample or conformal coverage interpretation. Uncertainty procedures, sensitivity settings and stopping rules remain design decisions; no statistical coverage, profitability or superiority claim is made.

## Existing financial precedents

[Wisniewski et al. (2020), *Application of Conformal Prediction Interval Estimations to Market Makers’ Net Positions*](https://proceedings.mlr.press/v128/wisniewski20a.html), already applies conformal prediction to market-maker net positions. The present draft changes the forecast response from the signed endpoint to a sampled absolute peak; it does not claim the first inventory application.

[Liao and Theodosopoulos (2005), arXiv:math/0506077v1](https://arxiv.org/abs/math/0506077v1), explicitly studies a quantile of lifetime maximum collateral-adjusted credit exposure under a Brownian model and marking policies. A financial quantile-of-maximum objective is therefore established prior work. This draft proposes neither a new calibration algorithm nor a new maximum-to-capacity principle.
