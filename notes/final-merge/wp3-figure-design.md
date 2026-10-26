# WP3 figure design

The mentor already specified a unified history plot plus a decision diagram.
The user opted out of questions and authorized execution. These implementation
choices are the executor's, not a new approval attributed to the user.

**Selected approach.** Extend A's existing four-panel figure, preserving its
380 provenance records and adding every one of the102 CFTC paired comparisons.
Two columns distinguish QR33 and QR4; a complete-range row retains every
outlier, and a clearly labelled detail row repeats the same records. CFTC uses
a distinct filled pentagon, with legend text "independent dealer source".
The caption and footnote immediately qualify this as an additional reporting
system of aggregate, potentially dependent markets. Known W52/W260 and the new
W520 computation are not conflated with a wholly untouched holdout. No jitter,
same-x pooling, favorable trimming, re-estimated threshold or new analysis.

A separate CFTC-only main figure would duplicate these points and consume the
main-figure budget. A new average curve would conceal market counterexamples.
Neither is used. The original two FX learning-curve line families and all
original simulation/panel/weekly points remain. The old crossing envelopes are
labelled as simulation summaries, not sufficient financial history boundaries.

**Decision diagram.** Begin with the matched historical benchmark. Three
parallel evidence boxes address history, the tested penalty menu and the stated
cost weights, then converge on local chronological comparison of scores,
breaches and stated charges. The diagram includes the failed high-history and
strict-improvement predictions and does not supply an untested replacement
policy. Numerical annotations bind to exact saved JSON pointers, including the
expanded-menu medians and the CFTC cost-grid range. Claims of universal shrinkage
monotonicity, a causal mechanism or realized operating savings are excluded.

**Artifact and verification plan.** Use the existing cached Matplotlib and
Poppler tools. Save vector PDFs and high-resolution PNGs, all point/source
bindings, actual artist offsets, diagram text/number bindings and artifact
hashes under a new results/final-merge/wp3-figures directory. A separate readback
checks every source ordinate and c coordinate, complete point census, bands,
full-range inclusion, exact artist offsets and diagram numeric pointers. Inspect
the actual PNGs and independent PDF rasterizations before WP3 acceptance.

For the later consolidated main manuscript, reserve at most four figure slots:
the endpoint/peak illustration, the unified history plot, the existing signed
loss decomposition, and the decision diagram. Retain the old standalone CFTC,
FX-history and cost-region figures in the inherited directories and move their
discussion/links to the Supplement or EXTENDED_RESULTS as the page budget
requires. No inherited artifact is deleted or overwritten.
