# Simulated forecasting-methodology referee

Internal same-model simulated review.

1. **Benchmark fairness (Table 3; Evaluation design).** The 14.8% matched gain and 12.7% rolling-reference gain use different controls. Is every headline tied to the correct history and update schedule, including the separately wrapped comparison? Request explicit control labels wherever gains are summarized. **New data/experiment: no; clarify existing comparisons.**

2. **Inference and multiplicity (Table 5).** Treasury's DM p=0.00761 accompanies Holm p=0.32 over 72 contrasts; another family adjusts two main comparisons. Which family supports each claim? Request consistent working-reference language, with dependence and post-selection scope explicit. Multiplicity adjustment alone does not validate pinball HAC inference. **New data/experiment: no.**

3. **Data snooping and replication (Limitations; Table 3).** The earlier 2015 gain uses rules designed after original FX results were viewed. Does “recurring” mean within-record stability or independent confirmation? Request the former interpretation throughout. Stronger confirmation needs an additional dealer or prospective observations; the current chronology can be stated directly. **New data: required only for stronger confirmation.**

4. **Short validation (Table 4; Supplement “Earlier-period fixed selection rules”).** Weekly selection uses 52 validation origins, overlapping labels, 34 regression coefficients and a six-candidate menu. Why should one-standard-error selection be stable here? Its 181.4% worst-cell excess warrants a procedure-specific interpretation. Request clear validation size, paired-band definition and retention of all failures. **New experiment: unnecessary for that clarification; longer-validation evidence remains future work.**

5. **Mechanism identification (calibrated-simulation subsection; Supplement “Interpretation and limits”).** Seven hourly cells fail numerically, and frequency is bundled with validation length and volatility laws. Which proposed mechanism is actually identified? Request conclusions limited to completed stationary weekly comparisons; numerical failure is not poor forecast accuracy. **New experiment: required to separate bundled effects or resolve unavailable hourly performance, outside this revision.**
