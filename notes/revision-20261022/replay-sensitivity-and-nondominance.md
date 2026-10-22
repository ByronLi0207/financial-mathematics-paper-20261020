# Dynamic replay: sensitivity does not establish superiority

Direction check,22October2026. These are elementary real-arithmetic consequences of the already stated recursion, not a new estimator, calibration theorem or financial result. The separate eight-cell AR experiment remains unexecuted at the time this note is opened. No experiment specification is changed by this note.

At an issue x and a mature historical anchor N_i, write raw translation as

`S_i,h=N_(i+h)+(x-N_i)`

and fixed-coefficient ordered residual replay as

`A_i,h=N_(i+h)+phi^h*(x-N_i)`.

For any finite phi and H whose powers are finite, define `eta=max_(0<=h<=H)|phi^h-1|`. Direct subtraction gives `max_h|A_i,h-S_i,h|<=eta*|x-N_i|`. The maximum-absolute-path map is1-Lipschitz in the path sup norm. Therefore the corresponding scenario peaks differ by no more than that bound. If `D=eta*max_i|x-N_i|`, every paired scenario peak differs by at most D.

The same kth order statistic of two equally sized paired vectors differs by at most their largest coordinate difference: each coordinate of one vector is at most its partner plus D, so its kth order statistic is at most the other kth order statistic plus D; exchange the vectors for the reverse inequality. Thus the two same-rank peak reports satisfy `|C_AR-C_S|<=D`. Projection to their common known floor is also1-Lipschitz. This argument permits duplicate values and does not require independently sampled scenarios.

For fixed realized P, pinball loss at tau is Lipschitz in its report with constant `max(tau,1-tau)`. At tau19/20 the resulting per-issue loss difference is no larger in magnitude than `.95*D`. These are deterministic sensitivity bounds. They have no coverage level, probability distribution, causal interpretation or guaranteed sign. Floating implementations additionally have rounding error; the identity is not a literal finite-precision certificate for every extreme input.

Three implications matter for interpretation. Exact phi1 reproduces raw translation; a merely near-one estimate does not make the reports numerically identical. A small eta need not imply a small monetary difference when current and historical anchors are far apart. Conversely, a small observed score difference is not evidence that either model is an adequate conditional law.

Neither path rule universally dominates the other in peak or pinball loss. For a one-step example, set historical anchor0, next value1 and query x=1. Raw translation peaks at2; phi0 replay peaks at1. If the realized future peak is1, replay has zero loss and translation has excess-report loss. If the realized future peak is2, translation has zero loss and replay incurs shortage loss. Both future completions respect the known issue floor. This is an artificial logical example, not a fitted-model result, mechanism estimate or claim that phi0 is appropriate for either financial source.

The fitted comparison must consequently report the full loss/breach/unused-allowance tradeoff against the matched S rule. A lower report or an estimated coefficient below one is not itself an improvement. The closed experiment's adverse results, if any, cannot be repaired by asserting that historical residual order or a smaller propagation coefficient guarantees better risk forecasts.
