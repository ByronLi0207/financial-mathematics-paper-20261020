# WP3 frozen retrospective learning-curve readout

All ten H/W units and all twenty selected conditional evaluation contrasts completed. The design was committed before the sole run at `b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a`; no numerical prediction, source clock, threshold, menu or solver was altered afterward. Both mandatory exact W2880 gates passed. Saved-trace independent audit reports zero ordinary differences and zero old-gate exact differences. Procedural completion is distinct from confirmation of every prediction.

## All four predictions, including non-identification

| H | Procedure | Predicted W interval (all-draw envelope) | Identified first downward root | Frozen classification |
|---:|---|---|---:|---|
| 6 | QR33 | [195.26477, 774.970497] | 572.336982 | FIRST_CUTPOINT_CONSISTENT |
| 6 | QR4 | [92.9067577, 749.765554] | NA | NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED |
| 24 | QR33 | [697.374177, 2767.75177] | 2463.64195 | FIRST_CUTPOINT_CONSISTENT |
| 24 | QR4 | [331.809849, 2677.73412] | 1341.31771 | FIRST_CUTPOINT_CONSISTENT |

Three identified roots lie in their fixed ranges. QR4/H6 already has a nonpositive delta at W360, so its first possible crossing is left-censored. This is compatible with the predicted interval but NOT_TESTABLE: a later conditional downward root cannot replace the unidentified first root. Therefore the predeclared all-four numerical confirmation is not met.

QR33/H24 and QR4/H24 become positive again at the largest W. Root consistency concerns a first cutpoint only and cannot support a rule that all larger windows or all conditional procedures win. Each W changes both the QR training window and the matched-F reference; the contrasts do not hold the F forecast fixed across W.

## Complete fixed-grid contrast and nominal DM table

All pairs use6625 identical origins, fixed validation10463–11902/evaluation11927–18551 and the original segment-refit24 clock. Values below are formatted directly from the complete scalar JSON; full precision remains in contrasts.csv/json. Delta is100*(mean QR loss−mean matched-F loss)/mean matched-F loss. The paired difference is QR−F; two-sided normal DM p-values use fixed Bartlett HAC. These are pointwise post-result diagnostics, not familywise inference or a selection rule.

| H | W | Procedure | Delta % | QR breaches | F breaches | HAC L | DM t | Nominal p |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 6 | 360 | QR33 | 3.04381868 | 539 | 356 | 10 | 1.16580001 | 0.243695313 |
| 6 | 360 | QR4 | -0.875405208 | 395 | 356 | 10 | -0.548569808 | 0.583300711 |
| 6 | 720 | QR33 | -2.11672715 | 531 | 332 | 10 | -0.615893179 | 0.537965023 |
| 6 | 720 | QR4 | 1.47647174 | 414 | 332 | 10 | 0.534859601 | 0.592746946 |
| 6 | 1440 | QR33 | -6.50767084 | 401 | 341 | 10 | -4.70812815 | 2.5000192e-06 |
| 6 | 1440 | QR4 | -3.28121084 | 355 | 341 | 10 | -3.79219001 | 0.000149324586 |
| 6 | 2880 | QR33 | -14.7667626 | 376 | 360 | 10 | -5.86567984 | 4.47296141e-09 |
| 6 | 2880 | QR4 | -4.28937065 | 399 | 360 | 10 | -2.57403538 | 0.0100519993 |
| 6 | 5760 | QR33 | -6.44069446 | 384 | 344 | 10 | -6.27703694 | 3.45086125e-10 |
| 6 | 5760 | QR4 | -4.89146931 | 424 | 344 | 10 | -2.36256476 | 0.0181489703 |
| 24 | 360 | QR33 | 24.3464522 | 1011 | 466 | 24 | 3.28662257 | 0.00101396635 |
| 24 | 360 | QR4 | 16.5902078 | 822 | 466 | 24 | 2.47285427 | 0.0134038788 |
| 24 | 720 | QR33 | 31.5039642 | 924 | 427 | 24 | 3.22275811 | 0.00126962723 |
| 24 | 720 | QR4 | 16.5131287 | 701 | 427 | 24 | 2.20194263 | 0.0276693612 |
| 24 | 1440 | QR33 | 9.23870896 | 650 | 331 | 24 | 1.27342828 | 0.202866108 |
| 24 | 1440 | QR4 | -2.62273757 | 465 | 331 | 24 | -0.85166156 | 0.394401962 |
| 24 | 2880 | QR33 | -3.7577698 | 531 | 357 | 24 | -0.504089464 | 0.61419851 |
| 24 | 2880 | QR4 | -2.89367181 | 508 | 357 | 24 | -0.49971273 | 0.617277368 |
| 24 | 5760 | QR33 | 1.8577089 | 608 | 361 | 24 | 0.236306132 | 0.813195129 |
| 24 | 5760 | QR4 | 0.158402594 | 526 | 361 | 24 | 0.0238885909 | 0.980941475 |

No additional coverage test, HLN statistic, lag search, bootstrap, model or financial period was added. A lower pinball loss does not establish target coverage or a financial decision-cost improvement. This is the previously studied FX period, not an unseen dealer, fresh holdout, or causal confirmation. All eighty candidate reports completed; the static auxiliary failure-container defect occurred zero times, and is separately retained as a scope MISMATCH rather than changed during the sealed run.

## Resource and identity boundary

Formal total wall time 629.7637939588167s includes ten separate natural experiment units. The maximum unit wall time was 206.27386266598478s; maximum worker RSS 94420992B; observed OS threads 1. The independent audit checked 190 saved trace blocks/2574900 numeric values and 20 paired HAC calculations without QR refits or new forecasts. All raw FX and private vectors stay in .scratch. The old QR4 archive lacks validation/floor/refit vectors; those historical values are not claimed compared.
