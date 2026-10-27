# Legacy calibrated Monte Carlo: byte-preserved v8 import

Source checkout: `/Users/bingyouli/Research/论文/金融数学论文-v8-20261024`; branch `revision-v8`; HEAD `f151b830489917ab7abc5137f2ec6b4135f55d6e`.
Every imported source/destination byte count and SHA-256 is in `manifest.json`.
All 25 imported files were copied and compared as raw bytes. The source checkout was read only.
No experiment, fit, forecast, diagnosis, statistical test, aggregation or repair was run.

`summary.json` is the sole v9 native source for the new 24-row legacy table:
17 COMPLETE cells and seven FAILED D1 cells. Partial success never supplies a failed-cell median.
The complete replicate archive and all 300 worker logs remain in their original ZIP/index.
Original protocol, three MC modules and numeric bindings are retained under `source/` for provenance;
they are snapshots, not a promise that executing that subdirectory reproduces the original checkout.

D0 must be described as **constant-variance AR(1) levels, where the peak depends on the current position**.
The peak therefore carries conditional information. Any older narrative implying no conditional signal is not adopted.
Archive bytes, including historical wording, are preserved rather than rewritten.
D1 denotes the old FX-calibrated hourly design; seven of its eight required cells failed ADMM convergence.
D2 is the old weekly-calibrated design. These designs differ from PR5 WP3 and C2 in menus, clocks,
features, calibration, repetition/evaluation lengths and estimands; they must not be merged numerically.

The original `/Users/bingyouli/Research/论文/金融数学论文-v8-20261024/results/v8/mc/` and all protected branches/results remain untouched.
