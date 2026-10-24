# Read-only C2 chronology and comparator audit

This same-model code review checked the present implementation and retained scalar receipts. It did not fit a model, recompute financial outcomes, change a frozen file, establish an unseen replication or inspect a native Claude inbox.

## Scope and findings

- Actual frozen call chain: `conditional_study.py`, `conditional_features.py`, `conditional_quantile.py`, `study_core.py`, with `run_conditional_study.py` and `reproduce_conditional.py`. All16 files listed in the original executable freeze matched its recorded fingerprints in the scoped review.
- Target: `study_core.py:229` uses the maximum absolute level from issue through issue+H; headroom subtracts the observed issue magnitude. C2 uses the same label cache and final scoring kernel.
- Pools: `conditional_features.py:94` and `parsimonious_v3.py:34` use the same scheduled refit and W mature origins ending at refit−H. Every retained C2 refit tuple has latest_label_end equal to its refit. Eight complete cell receipts were read; FX has277 refits and Treasury22 per cell.
- Chronology: the original split/refit specification is read by C2 rather than replaced. At H24 the final validation labels end before the first evaluation issue. Refits restart from each phase's first issue under the same formula as the original implementation.
- Feature availability: C2 selects current magnitude, current signed level and short/long increment RMS from the existing causal feature builder. Feature values depend on current/past levels only. Standardization and response scales use only the mature training pool and remain frozen until the next scheduled refit.
- Matched comparison: `parsimonious_v3.py:84` selects archived QR and `frozen_F` by the same source/H/W key. It does not accidentally use rolling F. Summary origin counts agree. The new forecasts use the original solver and native-unit projected-report loss.
- Interpretation: all8 displayed C2 rows agree with the retained summaries. Loss improves against original QR in5/8 cells and against F in3/8. All Treasury selections remain at the expanded penalty menu's upper endpoint. The paper correctly treats this as a joint feature/menu sensitivity and retains the failed original primary.

## Two untriggered selection-rule differences

The original specification invalidates an entire cell if any candidate fails and chooses the larger parameter on an exact validation tie. C2's separately written post-result specification excludes individual failed candidates and uses menu order on a tie. All40 C2 candidates are COMPLETE, and each of the8 minima is unique; neither difference was triggered. These facts were already disclosed in the change log. A claim that the entire selection program is identical except for features/menu would be too broad.

## Evidence boundary

No consequential chronology or target/comparator mismatch was found in this scope. Code and aggregate receipts cannot independently establish exact per-origin source/target equality with the frozen replay; that stronger claim relies on the existing private trace reconciliation and provenance chain. The B5 replay receipt and original archive verification remain separate evidence. The scoped test module verifies features, future perturbation invariance and training transforms; it is not a fresh full-flow external replication.
