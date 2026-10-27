# F1 signed loss-decomposition figure design

Implementation: `report_v12_decomposition.py`. Scientific authority remains the frozen F1 protocol. This is a display adapter over public scalar `rows.json`; it does not fit, predict, select, score, create a statistical test, pool native-unit losses, or recalculate E/S/G.

Two vertical facets share an axis scale: full regression QR33 above four-feature QR4. Each facet keeps all90 planned source/H/W positions. Family order is CFTC, panel, bill, FX. Within family, H then W then the frozen protocol's source order determine positions before any results are read. The x axis uses sparse numeric position labels; `plot-data.csv` supplies every source ID, H/W, method, cell ID, original status, input row pointer and displayed field.

S uses blue `#0072B2` with diagonal hatching; G uses orange `#D55E00` with dot hatching. Positive components stack upwards and negative components downwards. Signed S is never clipped, and a black point shows the supplied actual E value, including cancellation between positive and negative stacks. The renderer copies E from `actual_excess_pct`; it does not replace it with a fresh sum. Both facets show a clear zero line and percent-of-matched-F units. No favorable selection, truncation, data-driven row ordering, inset exclusion or positive-only axis is used.

Unavailable planned slots are gray x markers on the zero line and have no bars or E point. They remain distinguishable from a complete zero-valued decomposition, which receives the black E point at0. Missing input rows, duplicate identities, numerical-invalid COMPLETE rows and every original failure/resource status remain in CSV and bindings. Unexpected experiment/tau/source/H/W identities cause an explicit error instead of silently disappearing from the planned inventory.

The main figure is6.4 by3.8 inches, with8-point or larger text, embedded TrueType fonts, two line-pattern keys in addition to color, and a300-dpi PNG beside the vector PDF. Family labels and two facet titles replace tiny repeated source codes. Both facets share the full displayed signed range; all complete bars and E markers are inside the axis limits. The black E point is visibly smaller than a bar and distinct from the gray missing x.

The explicitly invoked script writes `decomposition.pdf`, `decomposition.png`, `plot-data.csv`, and `figure-bindings.json`. It refuses to replace an existing set of figure outputs. Each of the540 S/G/E bindings identifies its180-method-cell position, supplied value/status, source `rows.json` SHA-256, and RFC6901 JSON pointer to the original field. Missing or duplicate slots have no fabricated field pointer; their input index/status list remains explicit. Bindings also record the protocol hash, figure dimensions/encodings, and output hashes. The CSV is the full source-to-position mapping.

Run only after F1 has produced its scalar rows, using the cached plotting environment:

```text
uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with matplotlib==3.11.2 python -B report_v12_decomposition.py --rows results/v12/decomposition/rows.json --output-dir results/v12/decomposition
```

Before delivery, the coordinating task should visually inspect the produced actual-result PDF/PNG and check all540 source bindings against the same rows SHA. No financial result has been rendered during implementation; only constructed scalar rows may be used for renderer checks in a temporary directory.

## Constructed-data verification before any F1 render

Initial RED: the toy API check failed with ModuleNotFoundError before the implementation existed. GREEN: constructed rows produced all180 planned mapping rows and540 bindings; every field pointer was checked against its input JSON value and SHA. Additional checks covered negative S, complete zero E, each original failure/resource status, missing rows, duplicate identities, invalid COMPLETE fields, wrong tau/source rejection, and refusal to overwrite prior figure artifacts. No fit, financial observations, financial result file or manuscript was used.

A constructed-data PDF/PNG was rendered in a temporary directory and the PNG was visually inspected. Both facets, signed stacks, E cancellation, unavailable x markers, family labels, sparse indices, hatching, legend, and 6.4-by3.8-inch layout were legible and unclipped. The PNG is1920 by1140 pixels. Actual-result visual inspection remains a separate post-F1 action for the coordinator.

Verified implementation SHA-256: `2941d9ad8c907395e5745c5f6461c67e9b947a9f6b40b4df37691701ff9344ec`. Matplotlib3.11.2 and NumPy2.3.5 were resolved from the existing offline uv cache. No system package installation or download occurred.
