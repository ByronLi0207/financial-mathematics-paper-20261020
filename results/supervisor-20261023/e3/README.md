# E3: separating the ridge menu from the predictor specification

All eight expanded-menu 33-predictor QR cells and all40 validation candidates completed. These are post-result exploratory results; the archived original primaries remain the reported original comparisons.

The main finding is that the original Treasury deterioration largely disappears when its 33-predictor model can select lambda1 or10. Under a common menu, the two predictor specifications have similar mean losses. Therefore this experiment supports a restrictive-regularization-menu explanation for much of the original Treasury failure. It does not support attributing that failure to added predictors alone, and it does not establish statistical equivalence between the feature sets.

## Eight-cell aggregate comparison

Every percentage below compares against frozen F at the same source/H/W. QR4 is the previously completed four-predictor archive with its five-point menu. QR33 old is the archived original three-point menu. QR33 extended is the new five-point-menu run.

| Source | H | W | QR33 old loss change | QR4 loss change | QR33 extended loss change | QR33 extended selected lambda | QR33 extended vs QR4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Treasury | 6 | 52 | +83.354% | -2.589% | -3.244% | 10 | -0.672% |
| Treasury | 6 | 260 | +50.786% | +2.166% | +3.434% | 1 | +1.242% |
| Treasury | 24 | 52 | +227.411% | +5.955% | +4.340% | 10 | -1.524% |
| Treasury | 24 | 260 | +109.843% | +0.110% | -0.193% | 10 | -0.303% |
| FX | 6 | 720 | -2.117% | +1.476% | -2.117% | 0.01 | -3.541% |
| FX | 6 | 2880 | -14.767% | -4.289% | -14.767% | 0.01 | -10.947% |
| FX | 24 | 720 | +31.504% | +16.513% | +31.504% | 0.01 | +12.866% |
| FX | 24 | 2880 | -3.758% | -2.894% | -3.758% | 0.001 | -0.890% |

For the Treasury primary H6/W260, the original loss4159.673 versus frozen F2758.665 remains an archived +50.786% deterioration with54 versus28 breaches. E3 gives2853.403, or +3.434%, with32 breaches. QR4 gives2818.406, or +2.166%, also with32 breaches. The common-menu predictor comparison is +1.242% with DM normal p=.685 and HLN p=.691. Its E3-family Holm p is1.000. The original-to-expanded 33-predictor menu comparison reduces loss31.403%, raw DM p=.00556, E3-family Holm p=.145. Three Treasury cells still choose the upper endpoint10, so this menu is not evidence of a globally optimal penalty.

The four Treasury common-menu QR33-vs-QR4 raw DM p values are.142,.685,.0126,.857 in table order; their Holm-adjusted values are1.000,1.000,.301,1.000. Thus no feature-set contrast survives the declared28-comparison E3 adjustment. This absence of rejection is not an equivalence test.

For FX all four selected penalties remain unchanged. Every evaluation origin, peak, forecast capacity and per-origin pinball value equals the corresponding original33 archive exactly. In the H6/W2880 common-menu feature-set comparison, QR33 improves loss10.947% versus QR4, raw DM p=1.227e-7, Holm p=3.436e-6; doubling the HAC bandwidth gives raw p=3.145e-7. FX H24/W720 remains an adverse short-history result: +31.504% versus frozen F,924 breaches versus427. The extra menu points do not repair that result.

## Ordered primary accounting

`primary-decomposition.csv` provides the full display sequence ending at each **original** primary. FX is rolling F720 -> frozen F720 -> frozen F2880 -> QR4 extended -> QR33 extended -> QR33 original. Its last step is identical forecasts and losses. Treasury is frozen F260 -> QR4 extended -> QR33 extended -> QR33 original; the last step explicitly contracts the ridge menu back to the archived primary. The reverse-direction display of that last step negates only the paired mean/statistic, preserving its two-sided p value and its membership in the existing28-comparison family.

FX H6 step changes are +0.190%,+2.277%,-4.289%,-10.947%,0.000%; the resulting original total is -12.660%. Treasury H6 step changes are +2.166%,+1.242%,+45.779%; the resulting original total is +50.786%. These successive percentages multiply. The provided `percentage_points_of_initial_loss` values instead add exactly and are suitable waterfall-bar heights. In Treasury they are +2.166,+1.269,+47.352 points. This is an order-dependent accounting with a common tuning procedure, not a Shapley or causal decomposition.

## Files and verification

- `summary.csv` and `aggregate.json`: complete eight-cell means, selected penalties, original/common-menu comparisons, breach counts and resources.
- `validation-menu.csv`: all40 candidate statuses and scores; no failure was omitted.
- `convergence-summary.csv`:48 source/cell/phase/penalty summaries covering2476 accepted fits. Maximum iterations4023; every accepted residual, feasible-dual gap and training-label maturity condition passes the unchanged original criterion.
- `paired-dm.csv`:28 declared E3 comparisons, DM normal and HLN Student references, doubled-bandwidth sensitivity and separate28-comparison Holm adjustment. Four identical-loss menu comparisons have explicit status and null raw test statistics; adjustment uses p=1 for those declared comparisons.
- `primary-decomposition.csv`: all8 display steps, paired inference and additive waterfall contributions.
- `<cell>/result.json` and `<cell>/selection-before-evaluation.json`: full per-fit diagnostics and the selection frozen before evaluation.
- `verification.json`: independent scalar HAC reconciliation for all56 base/sensitivity calculations, exact FX reproduction and source-module hash checks.
- `executed-supervisor_e3.py`: the exact runner snapshot whose SHA-256 matches all8 execution receipts. The current root runner subsequently received one tested serialization correction for the solver's immutable failure-diagnostic mapping. All actual candidates completed, so this correction changes no measured result. No model, tolerance, menu, retry or fit was changed or rerun.

The sum of eight cell elapsed times is96.073s. Observed OS threads were1 in every cell; maximum RSS was72,368,128bytes. Every cell stayed below its predeclared3600s internal/3660s hard budget and1.5GiB internal/2GiB public memory ceilings. No numerical or resource failure occurred. This unexpectedly short observed runtime replaces the supervisor's unmeasured estimate; it is not an estimate for another environment.

The four-predictor archive is reused after all40 complete candidate records, exact-tie absence, strict original selection, evaluation origins/peaks, every stored pinball loss and every aggregate score were reconciled. This is verified archival reuse, not a fresh independent four-predictor rerun. Its code, JSON and trace hashes are retained in the eight cell results.

Private raw snapshots and per-origin traces are kept under the ignored task-owned `.scratch/supervisor-20261023/e3/` folder. Source redistribution rights were not expanded. Public artifacts contain only aggregate financial measures, scalar diagnostics and hashes; per-origin source values, capacities, peaks, losses and coefficients remain private. The original source modules and all original result files are unchanged.
