# WP5 public aggregate readback

Status: PASS_PUBLIC_WP5_READBACK. Scope is public JSON/scalar CSV and source-text
comparison only. No raw source, private NPZ/vector, worker, solver or financial
experiment was opened/run. These checks establish consistency among recorded
public artifacts; they do not independently rehash private archives or validate
financial calibration/statistical reference assumptions.

## Six-slot inventory and .90 directions

The canonical result is `results/revision-20261023/v6/wp5-tau-summary.json`, bound
to the v2 execution freeze. It contains all 6 frozen slots, with 3 raw NA slots.
Each raw NA remains null while its Holm bookkeeping value is 1. Independent
scalar sorting/step-down recomputation reproduces every published Holm value.

| tau=.90 named comparison | Mean QR-minus-reference | Relative loss change at this same tau | Same-named .95 mean | raw DM p | Six-slot Holm p | Reversal |
|---|---:|---:|---:|---:|---:|---|
| FX QR2880 minus rolling F720 primary | -60715.4446999 | -9.2042887544% | -55929.1515488 | 2.7311753806e-13 | 1.3655876903e-12 | false |
| FX QR2880 minus frozen F2880 matched | -67628.1691375 | -10.1459140785% | -66848.0979581 | 1.1528309319e-21 | 6.9169855915e-21 | false |
| Treasury QR260 minus frozen F260 primary | +1175.0309142 | +25.4323374422% | +1401.0078518 | 0.0257338187 | 0.1029352748 | false |

Each .95 contrast ID, source/H/window/reference-method/reference-window and mean
was independently checked against the unchanged public paired-comparisons.csv.
The .90 signs are retained. Treasury's raw p below .05 does not survive this
six-slot adjustment. Absolute loss levels at .90 and .95 correspond to different
objectives; the sign check must not be described as a comparison of unchanged
absolute loss magnitudes across tau. Treasury primary/matched coincide and are
counted only once per tau.

## .99 is unavailable, not robustness evidence

FX passes the index-only tail screen, but the complete declared validation menu
is [.001 COMPLETE, .01 FAILED/NONCONVERGENCE, .1 COMPLETE]. Both completed
candidates retain all 1440 validation issues. The .01 candidate failed after
10000 iterations at refit 11543 (1080 issues previously issued), with duality gap
2.4574717201474914e-6 greater than tolerance 1.0727896235806312e-6. Its origin count
and mean loss remain null; its diagnostics are retained. The predeclared
any-candidate-failure rule makes the whole FX .99 cell ineligible despite the
other two completed candidates. No replacement lambda is selected.

Treasury .99 is NA before fitting: exact validation-tail count 13/25=.52 and
training-tail count 13/5=2.6 are both below 5. All three candidate statuses are
NOT_ATTEMPTED_TAIL_INFORMATION. Historical rank is available, so the reason is
the predeclared nominal-information screen, not unavailable rank or an observed
adverse performance. Both sources' .99 evaluation receipts contain no scores or
private accuracy artifact. All 3 .99 ranking slots remain raw NA, bookkeeping 1,
Holm 1 and reversal null. They support neither confirmation nor reversal of the
.95 conclusion, and cannot be presented as .99 robustness having passed.

## Technical recovery and scientific identity

An independent exact text normalization reconstructs v2 from v1 with exactly 5
changed lines: one wp5-v2 OUT/PRIVATE routing line, two executable-freeze filename
references and two MappingProxyType-diagnostics-to-dict conversions. There are
no other source changes. The numerical `v6_tau.py` fingerprint is identical in
both execution freezes and current bytes. The retained v1 worker still matches
its original execution-freeze fingerprint.

The two completed .95 control receipts and FX .90 validation receipt were
compared recursively after excluding resources, executable-freeze hash,
point95-control receipt hashes and private ZIP artifact metadata. Every
scientific field matches exactly, including all control capacity fingerprints,
validation menu metrics, selected lambda, and fit-diagnostic coefficient/dual
fingerprints. This statement does not claim ZIP-container byte identity or
independent reading of private arrays. Public receipt SHA-256 values for both
versions are retained in the companion JSON.

The public selection receipt binds all 4 validation receipts. Their recorded
starts follow both .95 controls; their ends precede selection freeze; all 4
evaluation starts follow selection freeze and bind its exact hash. This is a
public receipt-order check, not an independent trusted timestamp attestation.

The newly created canonical summary is explicitly v2-bound; the recovery design
records that no v1 summary existed. The transport failure and its original
artifacts remain historical evidence; fixing serialization did not relax a
numerical failure, drop a candidate, alter data/splits/solver settings or retry
with a favorable parameter.

Companion evidence: `wp5-public-readback.json` contains the compact row checks,
identity comparisons, whitelist counts, execution-order checks and current
public/source fingerprints. No financial result file or bound source/test was
modified by this readback.
