# Horizon sorting and the scope of score improvement

For a common issue and source, the realized sampled peak is ordered by horizon. Sorting crossed forecasts can therefore improve a precisely defined joint score, even though it can worsen one of the individual forecasts. This differs from raising the long-horizon forecast alone. The distinction qualifies the manuscript's discussion of coherence without changing any stored report, primary comparison or empirical result.

The underlying rearrangement idea is established. Chernozhukov, Fernández-Val and Galichon study monotone estimates, discrepancy reduction and inherited confidence-band events in [Cemmap CWP17/08](https://cemmap.ac.uk/wp-content/uploads/2020/08/CWP1708.pdf). The consulted body is dated 12 July 2008. The later [Biometrika record](https://doi.org/10.1093/biomet/asp030) has the title *Improving point and interval estimators of monotone functions by rearrangement*, volume 96(3), 559–575, published online 30 June 2009. Body equivalence is not assumed. The finite pinball calculation below is an elementary specialization, not a new estimator or theorem.

## Equal weights and a common score level

Let two realized targets satisfy `P1<=P2`, and let crossed finite reports be `a=C1>b=C2`. All four quantities use the same monetary unit. Write the common pinball loss as

```text
L_tau(P,C) = tau*(P-C) + (C-P)+,
x+ = max(x,0),  0<tau<1.
```

Sorting replaces `(a,b)` with `(b,a)`. The change in the sum, with the original loss first, is

```text
D = L_tau(P1,a)+L_tau(P2,b)-L_tau(P1,b)-L_tau(P2,a)
  = (a-P1)+-(b-P1)+-(a-P2)++(b-P2)+
  = max(0, min(a,P2)-max(b,P1)) >= 0.
```

The linear terms cancel because the two reports are merely exchanged. For `a>b`, the difference `(a-y)+-(b-y)+` equals the integral of `1{u>y}` from `b` to `a`. Subtracting that integral at `P2` from its value at `P1` gives the length of the overlap of `[b,a]` and `[P1,P2]`, which is the final expression. Ties and endpoints do not affect interval length. A crossing alone need not give a strict gain; for example, equal targets make this difference zero.

For an ordered finite vector `P1<=...<=Pm`, exchange any adjacent inverted pair of reports. Each exchange weakly reduces the two corresponding loss terms and leaves the rest unchanged. Finitely many exchanges sort the report vector, so

```text
sum_h L_tau(P_h,sorted(C)_h) <= sum_h L_tau(P_h,C_h).
```

This statement is pointwise in the realized targets and reports. It needs no independence, correct regression model or estimation theorem. It does require ordered targets, common units, equal horizon weights and the common score level used above. If all horizons share the same complete evaluation origins and denominators, summing over origins and taking means preserves it. Different horizon samples cannot simply be treated as those common origins.

The calculation also gives nonincrease of the equally weighted total positive overrun and total unused allowance across these horizons: the same identity holds at the endpoint forms `(P-C)+` and `(C-P)+`. These are aggregate arithmetic properties. They do not give improvements at each horizon, identify actual financial costs or establish a conditional distribution. A common known issue floor is preserved because sorting only permutes report values already above it.

## A single horizon and breach counts can worsen

At `tau=19/20`, take `P1=0`, `P2=21/20`, `a=3`, and `b=1`. These are compatible with a common issue floor of zero and a sampled path reaching its positive maximum only after the shorter horizon.

| Pinball loss | Original reports `(3,1)` | Sorted reports `(1,3)` |
| --- | ---: | ---: |
| Short horizon | 60/400 | 20/400 |
| Long horizon | 19/400 | 39/400 |
| Equal-weight sum | 79/400 | 59/400 |

The joint sum improves by `1/20`, while the long-horizon score worsens by `1/20`. The loss of a declared single-horizon primary consequently has no automatic improvement guarantee from sorting.

Even the number of breaches across horizons can increase. With `P1=2`, `P2=4`, and original reports `(3,1)`, only the second report breaches. Sorting gives `(1,3)`, under which both breach. The joint all-covered event is false in both cases, and total positive overrun still falls from 3 to 2. Breach frequency, joint coverage, total overrun and severity within a method's own breach group are distinct quantities.

Unequal horizon weights change the conclusion. For example, with `P1=P2=0`, reports `(2,1)`, `tau=19/20` and weights `(1,2)`, the weighted score rises from `1/5` to `1/4` after sorting. Nor is an arbitrary collection of score levels covered by the common-level statement. For two levels the exact difference becomes

```text
D = max(0,min(a,P2)-max(b,P1)) + (tau2-tau1)*(a-b).
```

Thus nondecreasing levels `tau2>=tau1` still suffice for this exchange, while arbitrary unequal levels do not. Cross-source report values lack the common units and common target ordering needed for this argument.

## What happens to existing coverage guarantees

Sorting preserves an already established joint one-sided upper-coverage event. For ordered targets,

```text
{P_h<=C_h for every h} is a subset of
{P_h<=sorted(C)_h for every h}.
```

For an adjacent crossed pair, original joint coverage gives `P1<=P2<=b<a`; both inequalities still hold after exchange. Repeating exchanges proves the inclusion for the full vector. Therefore a valid pre-existing joint upper-coverage probability bound is inherited. No independence premise is needed for this deterministic event inclusion. The rearrangement literature's confidence-band result similarly requires an appropriate original coverage statement; it does not obtain coverage from monotonicity alone.

Ordinary individual marginal coverage is different. As a logical example, let `P1=P2=1`, with a common floor zero. Let reports be `(0,2)` with probability 0.05, `(2,0)` with probability 0.05, and `(2,2)` with probability 0.90. Each original report has marginal upper coverage 0.95. After sorting, short-horizon coverage is 0.90 and long-horizon coverage is 1. These probabilities illustrate a mathematical distinction; they are not fitted to the financial records.

Under the stronger premise that each original report has the required conditional upper coverage at a common coverage level given the same information set, with both reports measurable in that set, sorting preserves that conditional lower bound. For a crossed pair, covering the larger ordered target below `b` also covers the smaller target below `b`, while replacing `b` by `a` cannot reduce long-horizon coverage. A common-information conditional statement is not supplied by ordinary marginal coverage.

The present financial comparisons establish neither of those original probabilistic premises. The pointwise loss argument therefore supplies no new 95% claim for their reports. For a nonnegative peak report C, the sampled event P_(t,H)<=C is exactly equivalent to N_(t+h) belonging to the constant symmetric interval [-C,C] at every included h. Such a band can be defined from the scalar report. It does not recover an original horizon-specific or asymmetric signed band, acquire a new probability-validity guarantee from sorting, or constrain unobserved inter-record positions.

## Sorting and one-sided lifting answer different questions

For a crossing `(a,b)`, sorting produces `(b,a)` and changes both horizons. Raising only the long report produces `(a,a)`. The latter's long-horizon loss difference has no fixed sign. In the first numerical example, that one-sided lift raises the joint loss from 79/400 to 99/400, whereas sorting lowers it to 59/400.

Projecting a report onto the known issue floor has another premise: `B_t<=P_(t,H)` is known. Moving a report below that floor up to the floor improves its individual pinball loss. A fitted short-horizon report is not such a known bound for the long-horizon outcome.

No forecast sorting, one-sided lift, new joint empirical score, model selection or revised primary is executed in this note. A later empirical comparison would need to declare its reporting operation, common origins, weights, score levels and individual-horizon tradeoffs. The existing unfavorable and favorable results retain their original definitions.

## Reading and arithmetic evidence

The consulted CWP17/08 PDF has 31 physical pages, 6,347,726 bytes and SHA-256 `5c742d8d257ba31e54c73774460d3be82874bdb3a24565e0637283bf3312041e`. Relevant selected reading covered physical pp.2–8,12–13 and25–28: edition identity, rearrangement/Lorentz discrepancy arguments, original confidence-event premises and selected proof passages. Physical p.6 was also rendered and read visually. Some empirical/table text was encountered during locating; this is not a complete 31-page, all-table or code reproduction claim. The PDF remains private reading material.

The exchange identity and the adverse individual-horizon example were checked independently. A separate exact `Fraction` calculation verified 945 artificial cases on a finite grid and the displayed fractional losses; the analytic derivation, rather than finite enumeration, establishes the general statement. Those checks used no financial source or stored forecast. Their scope is recorded in the task's verification state. This companion adds a mature-method interpretation, not a new empirical result or methodological priority claim.
