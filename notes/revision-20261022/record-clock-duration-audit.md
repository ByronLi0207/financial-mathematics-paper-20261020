# What six and twenty-four records span on the stored clocks

22 October 2026. A post-result timing census of the existing accepted snapshots and the original frozen validation/evaluation origins. This clarifies the target's measurement; it introduces no accuracy comparison, fitted model, selection, removed origin or new source. The [prior check plan](record-clock-duration-check-plan.md), [original audit code](../../audit_record_clock.py) and [complete aggregate receipt](../../results/revision-20261022/record-clock-duration-verification.json) retain the calculation and identities.

| Source / segment | H records | All duration categories and their origin counts | Total origins |
| --- | ---: | --- | ---: |
| FX validation | 6 | 6 stored-clock hours: 1,368; 54 hours: 72 |1440 |
| FX validation |24 |24 stored-clock hours: 1,152; 72 hours: 288 |1440 |
| FX evaluation |6 |6 stored-clock hours: 6,289; 54 hours: 336 |6625 |
| FX evaluation |24 |24 stored-clock hours: 5,283; 72 hours: 1,342 |6625 |
| Treasury validation |6 |42 as-of calendar days: 52 |52 |
| Treasury validation |24 |168 as-of calendar days: 52 |52 |
| Treasury evaluation |6 |42 as-of calendar days: 277 |277 |
| Treasury evaluation |24 |168 as-of calendar days: 277 |277 |

Every one of the 16,788 source/segment/H label windows was checked by direct end-minus-issue subtraction and independently by summing its H adjacent stored timestamp differences. All equalities and declared origin counts matched. Both complete source snapshots were hashed before timestamp parsing and re-read unchanged afterward. The code uses only timestamp/date and series-identity fields; it does not parse monetary values or open forecast results.

The FX differences concern its stored naive clock. Historical timezone and daylight-saving conventions remain unverified, so these are not certified physical UTC elapsed hours. Likewise, calendar days between Treasury economic as-of dates are not a reconstruction of historical public-release times. All categories are retained. No category is used to identify a favorable regime, select a forecast, claim an independent subsample or assert a gap-specific accuracy effect.

A separate implementation parsed the same accepted time fields into NumPy datetime64 integer units, comparing integer endpoint differences with sliding-window sums of adjacent differences. All twelve aggregate rows and all 16,788 windows matched. This is an independent arithmetic implementation on the same sources, not another financial sample, model run or statistical replication.

Thus a fixed record target answers a different timing question from an uninterrupted fixed-clock target. In particular, calling the FX H24 result a 24-hour forecast would misstate 1,342 of 6,625 evaluation windows on the stored clock. Calling Treasury H6 a six-hour target would change its meaning much more. The standing manuscript already defines H as source records and notes variable FX durations; this census quantifies that qualification. It neither changes the response nor supplies unobserved inter-record positions, a funding horizon or a common cross-source economic effect. The loss averages weight issued origins equally, without an additional duration weight.

The measured process took 0.076 seconds and 37,781,504 bytes peak RSS. One OS thread was observed before and after; these two snapshots are not a continuous thread bound. The first monitoring attempt used a thread-count field unsupported by this macOS utility and stopped before source parsing; the successful run uses the repository's existing tested native thread-snapshot parser. No source or analytical result was changed to address that administrative failure.

The independently compiled Treasury source and its release, measurement and reuse limits remain documented in the [external-data record](../../results/revision-20261022/EXTERNAL_DATA.md). Raw observations are excluded. © 2026 Federal Reserve Bank of New York. Content from the New York Fed subject to the Terms of Use at newyorkfed.org.

Reproduce in the documented existing macOS/Python environment with the two hash-matching sources at their original task-relative paths:

```bash
mkdir -p state/revision-20261022
python3 -B audit_record_clock.py --output state/revision-20261022/my-record-clock-check-01.json
```

The output must be new. The checker refuses mismatching source bytes, changed snapshots and existing output files. It uses the standard library and the preserved repository resource parser; no installation is required. This command does not fit or score a financial forecast.
