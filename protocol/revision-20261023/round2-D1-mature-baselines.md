# D1 same-target mature baselines implementation plan

> For agentic workers: execute with superpowers:executing-plans; test each numerical unit before any financial fit.

**Goal:** Add fixed, post-result / exploratory FHS, GARCH-scaled peak-headroom POT and genuine leaf-distribution QRF on the original eight cells, preserving all failures and unfavorable results.

**Architecture:** Separate source-free numerical cores, synthetic tests, serial financial worker and generated manuscript integration. Read existing frozen F/QR forecasts rather than refitting old families. No new selection menu.

**Tech stack:** Existing Python 3.12.14; temporary uv arch 8.0.0 and scikit-learn 1.9.1; numpy 2.3.5/scipy 1.18.1; no system installation.

**Spec:** User-supplied revision-plan-v3-round2.md, D1, executed after E1–E10/D2/D3. This protocol is frozen before any D1 financial fit or outcome.

## Global constraints
- Same original source fingerprints, issue origins, H=6/24, W=720/2880 FX and W=52/260 Treasury, refit steps24/13.
- Original two primaries, original72 inference family and archived results unchanged; all new findings post-result / exploratory.
- One serial financial worker, one numeric thread; actual RSS <=2GiB, worker <=600s (540s guard,590s signal); no fallback, retry optimization, parameter search or dropped failures.
- No push, delete, software installation or changes outside this revision directory. Each complete cell requires every scheduled forecast.

## Review focus and fixed methods
1. **Mature information:** at refit r use a=r-H-W+1 through b=r-H for completed labels. Filter increments N[a+1:r+1]-N[a:r] use W+H-1 observations in the same position envelope N[a:r+1]. Record latest_label_end<=r; query state updates stop at actual t. Perturb future positions and valid future times, and require earlier reports and fit fingerprints identical.
2. **GARCH:** normalize increments by training RMS; zero/nonfinite RMS fails. Gaussian QMLE constant mean, GARCH(1,1), rescale=False, one arch fit(maxiter=300,ftol=1e-8), no retries. Require convergence_flag0, finite parameters, omega>0, alpha,beta>=0 and alpha+beta<=1+1e-10; disclose boundary estimates. Preserve all optimizer warnings. Freeze parameters and standardized residual pool per refit, filter observed increments between refits. Historical sigmas are in-sample at r, not historical issued forecasts.
3. **FHS:** M=2048 iid standardized residual draws with replacement, seed from SHA256 of source,H,W,r and fixed20261023. Same draws within a refit block. Recursively simulate native increments mu+sqrt(v)*z and GARCH variance, anchored at actual signed N_t. Target maximum absolute position includes h=0. Capacity=|N_t|+corrected rank ceil(19(M+1)/20) of simulated headrooms. No endpoint or square-root-of-H shortcut; no conditional coverage claim.
4. **Peak POT:** R_i=G_i/sigma_{i+1;r}; u is ascending order W-floor(.1W), strictly exceed R_i>u. Require >=20 excesses, m/W>.05, valid finite positive scale/support. Fit zero-location GPD by ONE Nelder-Mead run in (xi,log beta), initial(.1,log(mean excess)), maxiter3000,xatol=fatol=1e-8. Use continuous exponential limit for |xi|<1e-7 in likelihood and quantile; require xi>-.5 for the declared regularity gate. No alternate start, threshold or fallback. Quantile=u+beta/xi*(((m/W)/.05)^xi-1), continuous limit beta*log((m/W)/.05). Capacity=|N_t|+sigma_{t+1}*max(0,q). W52 is structurally NA (<20 strict exceedances). This is a GARCH-scaled peak-headroom POT adaptation, not literal McNeil–Frey return-innovation EVT. Anchor/drift/H-step volatility dependence remains; overlapping tail labels are dependent.
5. **QRF:** same33 causal features/training transform nearest=False and scale a_r. RandomForestRegressor(n_estimators=100,criterion=squared_error,bootstrap=True,max_samples=None,max_features=11,min_samples_leaf=5,min_samples_split=10,max_depth=10,n_jobs=1,random_state=20261023,oob_score=False,warm_start=False). Train response G/a_r. Apply fitted trees to ALL original W rows, weight each matching query-leaf member 1/(100*original leaf size), no bootstrap multiplicity. Weighted CDF left-inverse q.95 without interpolation/rank correction. Capacity=|N_t|+max(0,a_r*q). Do not use tree-mean quantiles or assert equality to sklearn predict under bootstrap.

## Files and checkable tasks
- [ ] Create test_round2_qrf.py first; record failing import, implement round2_qrf.py, record passing synthetic known-leaf, duplicate/zero-mass, constant/floor, determinism, bootstrap-definition and full future-perturbation tests.
- [ ] Create test_round2_filtered.py first; record failing import, implement round2_filtered.py, record passing manual variance/path/anchor, corrected rank, strict threshold/ties, W52 NA, exponential GPD limit and full future-perturbation tests.
- [ ] Implement round2_baselines_run.py serial cell workers, diagnostics, full/partial private traces and explicit failures. Run each of3methods×8cells once. No financial fits in subagents.
- [ ] For complete cells report native mean pinball, strict breaches and relative loss against frozenF/QR. Working-reference DM/HLN plus doubled bandwidth; separate 48-comparison Holm family reserves all method×cell×comparator slots, absent cells p=1 for adjustment only (display component as NA, not a successful null test). Preserve all48 rows; no pooled independence claim.
- [ ] Read back saved arrays independently to verify scores, maturity, coverage/failure counts and resource receipts. Integrate full eight-cell D1 outcomes into Section8 summary; details in appendix, main<=15pages including references.
- [ ] Run full named revision pytest suite with temporary uv; render every final page and visually inspect each; verify content/TeX/PDF/negative-result and original-hash consistency. Record full actual outputs in D1 CHANGELOG.

## Primary-source boundaries
FHS: Barone-Adesi/Giannopoulos/Vosper1999, DOI10.1002/(SICI)1096-9934(199908)19:5<583::AID-FUT5>3.0.CO;2-S; institutional https://susi.usi.ch/usi/documents/318043, read printedpp3–6 (iid standardized residuals, recursive paths). Constant mean and peak response here are fixed adaptations.
EVT: McNeil/Frey2000 DOI10.1016/S0927-5398(00)00012-8; author version https://statmath.wu.ac.at/~frey/publications/evt-garch.pdf, read sections2.1–2.3 and multi-period discussion. Original filters one-step return innovations and simulates sums; no theorem transfers to peak labels.
QRF: Meinshausen2006 JMLR7(35)983–999, https://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf, sections2–4, weights/CDF eq4–6 printedpp986–987. All original-row leaf weights; no time-series/fixed-window consistency claim.
Official runtime APIs: https://arch.readthedocs.io/en/latest/univariate/forecasting.html and https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html. Actual imported versions recorded in D1-001, not inferred from docs.
