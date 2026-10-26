# WP5 independent gate review

Scope: instruction interpretation and public source/metadata verification only.
No raw FX values, private numerical arrays or original timestamps were opened.
No fit, label construction, loss, DM test or new financial calculation was run.
Only this note was written by this review. Indices below are zero-based and
inclusive. This is an independent same-model review, not a Claude review.

## Decision

**The original, fixed-parameter full-prefix backcast may proceed with an explicit
MISMATCH; it is not, by itself, an unauthorized replacement calculation. The
claim that it supplies a previously unscored, distinct third validation period
must fail.** The two judgments must not be collapsed into an unseen-period PASS.

I do not recommend blocking the original calculation solely because the plan's
historical-use assertion is false. This recommendation depends on retaining the
original mechanically determined prefix 3071–10438 and the originally selected
methods/parameters. It does not authorize another period, selected gaps,
retuning, extra models, a new dataset, or filling missing old-period tests.

The controlling texts support this distinction:

1. v8 lines109–110 request a backcast before the original 2015 validation,
   wherever the full history is available, using already frozen methods and
   parameters. The following sentence, “这段数据之前只作为训练历史，从未被评估过”,
   is a factual assertion about those data. It is not worded as “only if this
   period has never been scored, otherwise stop”.
2. Inherited v7 rule4, line23, expressly says: “如果证据与本指令的描述不一致，
   **以证据为准**，相应调整叙事，并在 CHANGELOG 里标注 `MISMATCH`”. It therefore
   supplies an explicit response to a wrong factual premise. Applying that
   response does not require preserving a false novelty claim.
3. Inherited v7 rule2, line14, prohibits inventing a replacement when a step
   cannot be done: “只有本指令里写明了‘备选方案’的步骤，才可以走备选方案继续；
   其他情况停在这一步……**不许自创替代方案。**” The prescribed backcast is still
   computationally possible on its original eligible prefix. Correcting its
   evidential interpretation changes neither its observations nor its methods.
   Searching for a new unscored interval, shrinking W/H, or switching source
   would instead be a replacement and is not permitted.
4. v8 line26 separately requires revising the central claim when new evidence
   weakens it. Neither this rule nor rule4 requires a scientific expectation to
   succeed before an honestly reported requested analysis can pass its
   procedural acceptance. WP5 line113 asks for the frozen design commit,
   results, a three-period summary, and a decision about the claim; it does not
   require favorable scores or independence of the three windows.

The sequential gate remains binding (v7 line13: “没有 PASS 不得进入下一步”).
Before execution there is no WP5 PASS. If the full-prefix analysis is performed,
the eventual record must separately state **procedural PASS / scientific
MISMATCH: no fresh third validation period**. The summary must be titled and
explained as three evaluation windows, two of which overlap, rather than as
three disjoint or independent periods. If “three periods” is retained as a
column caption, exact interval boundaries and overlap must accompany it so the
caption does not imply temporal disjointness.

## What the verified evidence establishes

The public R6 design, `protocol/supervisor-20261023/r6-design.md:29–32`, identifies
retro validation7535–8974, retro evaluation8999–10438, original
validation10463–11902 and original evaluation11927–18551.

R6 performs prefix scoring rather than merely fitting there:

- `supervisor_r6.py:279` calls `_scored(backend.segment(...), labels, ids)`.
- Lines299–308 construct the prefix origins and call that scoring operation for
  each fold and candidate before selecting R3.
- The public `private-archive-manifest.json:81129–81136` records completed
  retro H24/W720 files for origins911–934, including an NPZ of2579 bytes with
  SHA256 `25a04f71a2faa1dd842dd91bd1d7bef010547d37dd9ac6e522885c7db8faa486`.
  I opened only the manifest entry, not the archived NPZ or its numerical data.
- The existing audit's public group metadata identifies W2880 prefix scoring
  starting3071–3094, continuing in24-origin blocks at48-index spacing. Its H24
  target paths abut across those issue-origin gaps. This establishes target
  exposure; it does not mean a forecast at every intervening issue origin was
  previously scored. R3 failure in another group cannot erase completed scores.

The eligibility arithmetic in the source/design is
`168 + 2880 + 24 - 1 = 3071`. Keeping every requested target before original
validation10463 gives the last issue10438. Thus the full mechanically selected
prefix3071–10438 remains exactly the requested mature-history backcast range.
It contains the old evaluation8999–10438 (1440 issue origins) and numerous old
R3 scoring folds. It cannot be described as unseen.

A pure prefix preceding every old score would have to end by886; this cannot
coexist with earliest mature issue3071. Even excluding W720 and considering
only old W2880 scoring would require a last issue no later than3046. Hence a
new completely unscored prefix with the same full history is impossible. That
negative finding is decisive against the novelty/third-independent-period
claim, but does not make the original requested retrospective diagnostic
physically unavailable.

The old R6 design itself makes a closely relevant distinction at line11:
“若执行前发现相反的角色证据，保守停止‘未曾评估’声明并记录，不能迁移到一个
看结果后更好的时期。” This is supporting historical context, not authority
over v8. It explicitly stops the claim and prohibits period migration; it
does not instruct the reader to manufacture a new untouched dataset.

## Conditions before any WP5 run or PASS

1. Record the mismatch before any new scores. Preserve both the old two-window
   findings and all negative results. Do not advertise this as new external,
   independent, prospective, or previously unscored validation.
2. Commit a design under `protocol/revision-v8/` before execution, as required
   by v8 line24. It must fix the original full prefix, original selected
   parameter identities, full W/H and feature construction, refit timing,
   matured-label rule, both references, loss/breach/DM definitions, failure
   handling, and support/rejection criteria. Disclose later-period parameter
   selection and prior R3/retro inspection. No new period search is authorized.
3. Explicitly compare the meaning of the two references rather than interpreting
   an overlap as another independent replication. A favorable new prefix result
   can at most add a descriptive, previously inspected retrospective window;
   it cannot repair the absence of a new untouched sample.
4. In the three-window summary, retain NA where old archives lack the requested
   method/comparison. In particular, retro H24's five-point R0 selection is not
   original three-point QR33. Missing retro QR4 and old rolling DM entries must
   remain absent. Computing those missing old-window tests would require scope
   beyond this judgment, not a “numeric check”. State the asymmetric available
   comparisons plainly; do not present an all-method complete cross-period test.
5. The procedural gate can pass only after the requested new backcast outputs,
   exact archive-based summary, provenance, and honest claim revision exist.
   This note does not itself grant WP5 PASS or authorize WP6 now. An unmet
   actual output requirement or technical inability should be BLOCKED under
   the inherited sequential rule.

## Why I do not adopt the existing audit's blanket calculation stop

`wp5-period-parameter-audit.md` correctly establishes the historical-use
contradiction and the nonexistence of a completely unscored mature prefix. Its
instruction to stop any new financial backcast is an interpretation, not a
fact established by the metadata. Treating an unchanged requested computation
with corrected interpretation as a replacement would make v7 rule4 largely
inoperative whenever a mistaken premise affects scientific value. The more
specific and workable reconciliation is: keep the computation and its frozen
scope, reject the false independence/novelty premise, and lower the resulting
evidential claim. This is permission to do the original analysis honestly,
not permission to achieve an alternative scientific goal.

## Read-only verification commands and excerpts

Executed from the revision workspace; no result file was generated:

```sh
sed -n '1,110p' notes/revision-v8/wp5-period-parameter-audit.md
sed -n '110,230p' notes/revision-v8/wp5-period-parameter-audit.md
nl -ba supervisor_r6.py | sed -n '270,315p'
nl -ba results/supervisor-20261023/r6/private-archive-manifest.json | sed -n '81120,81143p'
nl -ba protocol/supervisor-20261023/r6-design.md | sed -n '8,65p'
```

Observed source excerpt:

```text
279 try: attempts[key]=_scored(backend.segment(candidate,ids,**kwargs),labels,ids)
301 for a,b in folds[:-1]:
304 item=attempt(candidate,ids)
305 fold_losses[candidate].append(None if item.get('status')=='FAILED' else item['scores'].pinball)
```

Observed manifest excerpt:

```text
81134 "path": ".scratch/r6-20261023/run/retro/retro-fx_hourly-h24-w720/0.001-911-934-w720-d24.npz",
81135 "bytes": 2579,
81136 "sha256": "25a04f71a2faa1dd842dd91bd1d7bef010547d37dd9ac6e522885c7db8faa486"
```

The v7 and v8 instruction files in the user-specified
`batch-oh4_2klg/` directory were read with `nl -ba ... | sed -n ...`:
v7 lines1–115 and v8 lines1–135. The controlling exact instruction excerpts and
their line numbers are quoted above. No absence of other external or deleted
historical scoring is asserted.
