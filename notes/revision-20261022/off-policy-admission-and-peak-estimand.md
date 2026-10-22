# Admission of a later off-policy decision study

22 October 2026. This companion makes one previously open route concrete. It adds no policy, simulator, financial sample, forecast, score, inference result or main-paper reference. The accepted 22-page / 26-reference manuscript remains unchanged. All examples below are analytical constructions, not financial observations or new research theorems.

## Primary source and actual reading

Nan Jiang and Lihong Li (2016), *Doubly Robust Off-policy Value Evaluation for Reinforcement Learning*, Proceedings of the 33rd International Conference on Machine Learning, PMLR 48:652–661. [Official metadata](https://proceedings.mlr.press/v48/jiang16.html); [official PDF](https://proceedings.mlr.press/v48/jiang16.pdf). The proceedings list the conference as 20–22 June 2016; no DOI is displayed in the consulted metadata. The normal PDF request on 22 October 2026, 18:14:23.057821–18:14:23.837029 UTC returned 422,940 bytes / ten physical pages, SHA-256 `8798c38e5fa642c646d074ffeac7c3ebe309b92ec7619d33eab687b758084278`. The source is private; download access is not treated as redistribution permission.

Root read the introduction, §§3.1–4.4 and selected §5 assumptions / §§6.1–6.2 evaluation descriptions, physical pp. 1–8. Physical pp. 3–4 were rendered and viewed to check importance ratios, independence and variance/CI statements. The detailed constrained-information algebra in §5, all plotted values, appendices and the separately linked supplement were not independently verified. Physical pp. 9–10 supplied reference locators only. A helper's selected pp.2–4 source locating and logical checks are not root reading time.

The source estimates expected finite-horizon policy return from state/action/reward trajectories. Its importance weights compare target and behavior action probabilities. It requires target-policy and fitted-value independence from evaluation observations for its stated unbiasedness construction; its averaging and CI discussion uses independent trajectories. The contextual-bandit discussion of correctly specified nuisance models must not be relabeled as an unconditional finite-sample guarantee for arbitrary estimated financial weights. Its simulation results are not dealer-inventory validation. These are selected-source conditions, not a certification of the source implementation or all proofs.

## What the current data do not identify

The current benchmark observes a source-reported inventory N and evaluates a report against its recorded sampled absolute peak. It contains no verified action log, pre-action execution state, behavior probabilities or policy-specific cost account. N might be one component of an adequate state; observing N alone does not establish that it is a sufficient Markov state or all information used in logged decisions.

For a simple one-step example, set N₀=0 and let the behavior rule always take action 0. Environment A maps action 0 to N₁=0 and action 1 to N₁=1. Environment B maps action 0 to N₁=0 and action 1 to N₁=2. The environments agree on every observed trajectory, even if behavior actions and their probabilities are later recorded perfectly. Under the target rule that takes action 1, however, the current-style peak max(|N₀|,|N₁|) equals 1 in A and 2 in B. Its quantiles differ at every probability level strictly between 0 and 1. A deliberately defined terminal return minus that peak also has different expectations.

This proves only nonidentification in this example's unrestricted model class. It does not rule out additional structural information. The target action has zero behavior support. Recording that zero more accurately cannot identify its response, and a fitted regression cannot distinguish A from B from those data alone. If a correct response for the unobserved action is supplied, it comes from added restrictions or evidence. The requirement that the target trajectory law be dominated by the behavior trajectory law is an applicability inference from importance weighting; it was not located as a separately stated overlap assumption in the selected Jiang–Li passages. Small but nonzero probabilities can still cause unusable variance.

A justified known-transition model is a different route. With transition and cost laws valid under both actions, one can propagate a fixed target rule without estimating action propensities from the behavior sample. A model fitted only to action 0 histories does not thereby become a known action 1 model. Prospective controlled evidence is another possible route. The benchmark does not establish any of them, but does not require all of them simultaneously.

## A path peak can be an evaluation object, with extra work

The source's expected-return estimand is not already the present peak quantile. Path dependence alone does not make an extension impossible. Suppose a valid policy/environment model and sufficient original decision state S are supplied. For a fixed issue information set I₀, declare the initial state or its conditional distribution; augment the state with time and the running absolute maximum:

```math
M_0=|N_0|,\qquad M_{h+1}=\max\{M_h,|N_{h+1}|\},
\qquad \widetilde S_h=(h,S_h,M_h).
```

Then M_H is the sampled peak including the issue value. With discount one, zero nonterminal rewards and terminal reward 1{M_H≤c}, expected return at a fixed threshold c is the target-policy peak CDF conditional on I₀. This is an elementary representation, conditional on a valid augmented transition/reward specification and the selected policy-evaluation method's assumptions. It creates no missing action support, release-time information or usable episodes.

Obtaining a peak quantile would require CDF estimation and inversion, rather than reading a quantile from one expected-return estimate:

```math
F_\pi(c\mid I_0)=\Pr_\pi(M_H\le c\mid I_0),\qquad
q_{\tau,\pi}(I_0)=\inf\{c:F_\pi(c\mid I_0)\ge\tau\}.
```

A correction-based estimate of a bounded terminal indicator need not itself lie in [0,1] or be monotone over c. Clipping, monotonic projection, a threshold search and inversion need their own stated statistical treatment; a pointwise mean CI is not automatically a simultaneous CDF band or a quantile guarantee. Atoms and the known issue floor must remain in the definition. Bounding the terminal reward alone does not bound importance-weighted estimates when action ratios are unbounded. None of these estimation steps is executed here.

For an exact illustration of the shape issue, take one initial state and two behavior actions, each with probability 1/2; the target always takes action 1. Let that action's true terminal peak be 1. At thresholds c₁=1/4 and c₂=3/4 the true target CDF is zero. Supply an evaluation-independent fitted CDF for action 1 with values 1/5 and 4/5, a legitimate but wrong CDF (for example, fitted mass 1/5 at 0, 3/5 at 1/2 and1/5 at 1). The one-step correction equals fitted value plus the action importance ratio times indicator-minus-fitted-value. On an action 1 log it therefore returns −1/5 and−4/5: negative and decreasing. On an action 0 log the ratio is zero and it returns 1/5 and 4/5. Averaging over behavior actions gives the correct zero at each threshold. Clipping each estimate into[0,1], however, gives positive expected values 1/10 and 2/5. This hand-computable construction has complete action support and bounded ratio 2; it demonstrates neither a failure of the stated pointwise unbiasedness nor an actual financial result. It shows why an automatically valid CDF and quantile cannot be inferred from that unbiasedness alone.

An economic study could instead define an expected fee-adjusted, inventory-sensitive decision cost directly, if that is the actual financial question. Its unit, observation clock, terminal liquidation and admissible actions would have to be fixed. A smaller passive forecasting score is not a measured improvement in that cost. Changing both the report and the action mechanism would otherwise mix prediction accuracy with a changed inventory-generating law.

## Concrete admission, and the present stopping decision

Before a later experiment, choose one estimand and one defensible identification route. A logged-policy route needs the pre-action information set, actions and their times, rewards/costs and next states, behavior probabilities or a justified way to estimate them, target support, and a trajectory/dependence argument. A model route needs independently defensible transition/cost assumptions and sensitivity to their violation. Both require a fully specified target decision rule and truthful information timing. A fitted/selected model or policy needs evaluation safeguards appropriate to its uncertainty; the cited logged-DR construction specifically separates policy/value fitting from its evaluation observations. When the true transition and reward laws are completely known, policy selection and exact evaluation in that model need not use separate logs. Adjacent overlapping financial windows do not become independent episodes by being renamed.

The present stopping decision is to retain the descriptive benchmark and its adverse findings. There is no legitimate action-response input here with which to run this extension. The [policy-generated inventory note](policy-generated-inventory-and-validation-boundary.md) and this admission memo identify a potential additional evidence axis; they do not upgrade originality, establish economic value, or replace compatible unseen validation. The next useful step is obtaining evidence for a selected new question, not attaching a doubly robust label to the current N-only record.
