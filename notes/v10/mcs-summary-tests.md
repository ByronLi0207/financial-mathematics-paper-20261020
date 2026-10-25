# E3 pure MCS summary: artificial RED to GREEN

本模块依据已独立提交的 `protocol/v10/mcs-design.md`（`78ea93493379ab3a93459d28e1bab84200f01539`），仅处理 caller 提供的 registry 元数据和人工 membership receipts。不读取真实 loss/MCS results，不导入 arch、不运行 MCS/bootstrap，不改 E2 冻结代码或旧归档，不提交。报告脚本可以另作准备，但不运行。

## API and exact definitions

`summarize(records, registry_groups, design)` returns `groups_summary` (all six registered groups, including empty groups), `overall`, and one `cells` entry for every planned registry comparison. Registry identity may be nested under `identity` or given by its four named fields. Duplicate registry identities and out-of-plan result identities are rejected. Missing/duplicate result receipts remain explicit failed planned comparisons.

Successful statuses are exactly `COMPLETE`, `COMPLETE_IDENTICAL_LOSSES`, and `COMPLETE_SINGLE_METHOD`. The last two retain analytic-case counts and do not imply statistical discrimination among indistinguishable/single methods. Saved membership partitions, p-value completeness/range, exact-loss classes, and literal arch inclusion boundary are checked without recomputing any p-value. Invalid claimed-success receipts become `FAILED_INPUT` with original status and a summary-integrity reason; no inconvenient method is silently removed.

Procedure category is taken only from explicit registry `method_class`. No category is inferred from a name, selected infinity, equal forecast, or a `published_combination::` prefix. The following metrics remain distinct:

- `matched_FI_membership`: unfolded included set contains a matched historical F/I procedure.
- `literal_sole_FI`: exactly one unfolded distinct procedure survives and it is matched F/I.
- `sole_loss_class_FI`: exactly one surviving exact-loss class contains matched F/I; conditional labels can still be in that class.
- `historical_only`: the nonempty unfolded included set is entirely matched F/I.
- `rolling_F_membership`: an explicitly `other_historical` rolling-F procedure is included.
- `broad_FI_or_rolling_F_membership`: either matched F/I or that separately classified rolling-F group is included.

For each metric, the reducer exposes the observed successful count/fraction, successful denominator, planned denominator, and all-planned lower/upper counts and fractions. Failed comparisons are unknown, never favourable successes. If S successful out of P planned, and x successful comparisons meet a metric, the bounds are `[x/P, (x+P-S)/P]`.

Conditional exclusion is slot-weighted, not comparison-weighted. It exposes excluded slots among successful MCS comparisons, complete conditional slots in successful comparisons, unknown complete conditional slots in failed comparisons, total planned complete slots, and known-NA conditional slots separately. With x exclusions, S complete conditional slots in successful comparisons and U complete conditional slots in failed comparisons, the successful fraction is x/S and planned bounds are `[x/(S+U), (x+U)/(S+U)]`. Known prior NA enters neither statistical exclusion numerator nor complete-slot denominator. An unavailable method without an explicit class remains counted as unclassified NA; its class is not guessed.

Every successful cell retains full method metadata/classes, included/excluded IDs, native p-values, all `unique_loss_groups` with canonical `members`, surviving classes and separate conditional included/excluded lists. `methods` is accepted only as a legacy class-member key alias. No independent-source p-value pooling or family-wide across-cell guarantee is produced.

## Observed artificial tests

Tests were written first. The initial stdlib run observed16 test methods and18 failing assertions/subtests, all for the explicit absence of the pure implementation. The minimal implementation then passed all16 artificial tests.

Two additional hand-checked cases protect unequal conditional-procedure slot weights and real NumPy scalar conversion. The final pinned offline run selected only this test file:

```text
uv run --offline --no-project --no-env-file
  --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
  --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1
  --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow
  python -B -m pytest -q -p no:cacheprovider test_v10_mcs_summary.py

18 passed, 3 subtests passed in0.13s
exit0; no skip
```

The only stderr line was uv's informational `--no-project` warning. Root retains the combined/full-suite gate; this subtask did not run it.

The18 test methods cover six-group/all inventory; literal uniqueness versus equivalence-class uniqueness; two F/I members versus literal singleton; rolling versus matched historical membership; hand-calculated successful/planned bounds; NA separation; unequal conditional slot weights; missing and duplicate results; a claimed-success record silently dropping a registry method; corrupt partitions/p-values/equivalence inclusion; literal p=.10 boundary; exact identical losses; analytic single method and zero conditional denominator; explicit class overriding suggestive names; empty registry; invalid registry/result identities/classes; immutable input; native JSON values; and actual NumPy p-value/identity scalars. All fixtures are invented scalar membership receipts. These tests establish no empirical MCS result.
