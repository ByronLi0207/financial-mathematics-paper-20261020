# Additive main-manuscript number audit

This describes `check_main_numbers.py`, not a scientific analysis. The wrapper
calls the unchanged v8 guard and preserves every failure except the specific
located unbound occurrences and the specific new figure identity failure that
are independently verified below. It never grants a whole-document, paragraph,
equation, value-membership, or number-word-membership exemption.

Default binding file: `notes/revision-v9/wp5-main-context-bindings.json`.

```json
{
  "schema": "v9-main-context-bindings-1",
  "contexts": [
    {
      "id": "wp1-original-cutpoint",
      "file": "main",
      "text": "The diagnostic cutpoint is 106.5.",
      "bindings": [
        {
          "kind": "digit",
          "offset": 27,
          "literal": "106.5",
          "source": "results/revision-v9/wp1/breakeven.json",
          "source_sha256": "SHA256_OF_THE_WHOLE_SOURCE_FILE",
          "pointer": "/REPLACE_WITH_THE_ACTUAL_FIELD",
          "raw_value": 106.49618468616566,
          "display_operation": {"type": "format", "spec": ".4g"}
        }
      ]
    }
  ],
  "figures": []
}
```

The example is explanatory and is not an accepted binding. In particular, use
the actual source pointer and programmatically obtain the exact character
offset from the final source text; do not copy the illustrative offset above.
An exact context must occur once in the named current document. `file` is
`main` or `cover_letter`. Context IDs and bound occurrence positions must be
unique. Offsets count Python Unicode characters, not UTF-8 bytes. Changed or
missing contexts fail; the wrapper does not search for another equal number.

Each source path must be repository relative and remain inside the repository
after resolution. The entire source SHA256 and the native JSON value, including
its type, must agree. Use either `pointer` for one RFC6901 JSON pointer, or
`pointers` for an ordered list; in the latter case `raw_value` is the ordered
list of the independently read values. All expected source values remain
unrounded; formatting occurs only after source verification.

Supported presentation operations are deliberately limited:

| `display_operation` | Meaning |
| --- | --- |
| `{"type":"exact"}` | Exact native integer or text display. |
| `{"type":"format","spec":".4g"}` | Explicit finite-real formatting; `.1f`, `.3g`, `.4g`, and their signed forms use the same rule. |
| `{"type":"fraction"}` | Ordered pair of native integer counts displayed `numerator/denominator`. |
| `{"type":"length"}` | Length of the explicitly bound source array. |
| `{"type":"count_eq","equals":"FIRST_CUTPOINT_CONSISTENT","field":"/first_cutpoint_prediction"}` | Count exact matching values in an explicitly bound array; omit `field` when the array directly contains scalar statuses. |

For integer/count operations, `"as":"word"` converts an exact count from zero
through twenty to the corresponding lowercase English number word. It does
not accept manually supplied count labels. No arithmetic expression evaluation,
model fitting, hypothesis test, probability transformation, or generic
substring display rule is supported.

`kind:"digit"` binds one complete numeric token. `kind:"word"` binds one complete
number word. `kind:"numeric_fragment"` binds all complete numeric tokens inside
an exact source-derived display such as `47/48` or the complete mathematical
definition `W/(H+1)`. It is suitable for a formula only when the raw source value
is the exact full formula, not a coincidentally equal constant elsewhere. Any
other unlisted number in the context remains unclassified. The unchanged
legacy lexer treats an integer followed immediately by a sentence-ending dot
as a decimal token with an empty fractional part; the wrapper preserves that
token boundary and never accepts a partial token.

Number-word failures in the legacy report do not include columns. The wrapper
reconstructs the old failure's exact file/line/word/truncated-context signature
from the current document, requires a unique position, and resolves only that
position. Ambiguous signatures remain failures. The resulting v9 inventory
adds the verified column.

A new figure can be bound only with this identity receipt shape:

```json
{
  "path": "submission-jof/figures/v9-unified-history.pdf",
  "source": "results/revision-v9/wp4/render-v5/unified-history.pdf",
  "sha256": "694755e63727224177c36ccb9845d3c5378d26b7804ee44cd1c7c724bfe17cb3",
  "placement": {
    "source": "notes/revision-v9/wp4-final-placement-v5.json",
    "sha256": "ACTUAL_PLACEMENT_RECEIPT_SHA256"
  },
  "point_audit": {
    "source": "notes/revision-v9/wp4-independent-audit.json",
    "sha256": "ACTUAL_POINT_AUDIT_SHA256"
  },
  "visual_receipt": {
    "source": "notes/revision-v9/wp4-visual-QA.json",
    "sha256": "ACTUAL_VISUAL_RECEIPT_SHA256"
  }
}
```

The source and copied asset must both have the specified bytes; the placement
receipt must contain their exact unique pair. The machine audit must be PASS,
have zero differences/mismatches, and identify the same final directory and
PDF hash. The separate visual receipt must identify that directory, completed
raster observation and successful rendering. This resolves only
`UNBOUND_OR_CHANGED_FIGURE_SOURCE` for that exact path, never
`MISSING_CURRENT_FIGURE`. The numeric guard always keeps
`figure_values_verified_here:false`, `reference_metadata_verified_here:false`,
and `full_artifact_numeric_acceptance:false`: it verifies the identity of
separate evidence, not figure values, references, or PDF layout itself.

Legacy failures including `MISSING_CONTEXT`, percentage displays, table numeric
vectors, ordered rows, display mathematics, original source values/hashes and
historical proof integrity survive unchanged. The wrapper also pins the legacy
checker SHA256. The report retains all raw `legacy_failures`, lists the exact
resolved failures and evidence, and reports the remaining exhaustive current
document census. Acceptance requires zero remaining unclassified numeric and
number-word occurrences and zero failures; separate figure/reference/PDF/
supplement gates are still required.

Synthetic tests run with the existing cached runtime and temporary pytest:

```text
env UV_OFFLINE=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -q -p no:cacheprovider test_v9_main_numbers.py
.....................                                                    [100%]
21 passed in 0.07s
```

The tests were first observed failing because the wrapper did not exist, then
passed after implementation. They use constructed text/JSON and synthetic PDF
bytes; no financial data, arrays, forecast, statistical fit, or new scientific
calculation was executed. This is scaffold validation, not current-manuscript
acceptance; the authoring thread must supply real final contexts and run the
complete guard against the final current source.
