# E4 cost figure: display-only layout repair

The registered E4 cost run was already complete. This change does not invoke
the cost driver, input adapter, any forecast or any fit. It only rerenders
the saved aggregate display through `report_v10_cost.py`.

The original compact 2-row/3-column figure at 7.4 by 6.4 inches had colliding
beta tick labels and long panel titles. The final figure is 3 rows by 2
columns at 7.4 by 8.2 inches. Each panel title places the group name and
complete/planned count on separate lines. Tick labels omit only the leading
zero below one (`.01`, `.025`, `.05`, etc.); decimal points and all tick
values are retained. Ticks use 8-point text, axes and colorbar labels 8.5
points, and panel titles 9 points. The x-axis wording is shortened to
`Breach charge` without changing its beta definition.

## Rendering and inspection

The report function was loaded with `runpy` under a non-main name, assigned
a staging output directory `.scratch/v10/cost-layout-3x2`, and called only
on copies of `group-regions.json`, `summary.json`, and `manifest.json`.
The four staged report files replaced the authorized four final report
files after integrity checks. The saved wide backups in
`.scratch/v10/cost-wide-report/*.bak` were not changed.

The 180-dpi PNG was visually inspected. The one-page PDF was also rendered
with Poppler at 1080 pixels wide, representing 6 inches at 180 dpi, and
visually inspected. Titles, beta ticks, axis labels and the shared colorbar
are separate and readable at that width, with no clipping or overlap.
`pdfinfo` confirms a single page at 532.8 by 590.4 points (7.4 by 8.2 inches).
The display script also passes AST parsing. No tests or actual cost run
were performed for this layout-only change.

## Integrity

Both `report-values.json` and `report-note-zh.md` are byte-identical to their
previous versions. Every other file in `results/v10/cost` retains its prior
SHA256. All existing `.bak` fingerprints were checked before and after
replacement and are unchanged. Detailed before/after receipts are in
`.scratch/v10/cost-layout-3x2/layout-integrity.json`.

| Final file | SHA256 |
|---|---|
| cost-regions.pdf | 3ddcc2c1f710b61afae0b0068587286fddd4a7dd18f26854a4f2810577943a15 |
| cost-regions.png | 50ce81c2b3ac40175603ad6bc6adcd7e8fb6e168b52f5d07bce7b60858e71184 |
| report-values.json | 12383327e2cb8d08bfa8a23305b1586ff4be6ca52dddfcde72f7e858d65a28ea |
| report-note-zh.md | 3934a0d64cdd9a6dad8cf731ee2c4371ef59b0ea2699410e89b86844f9291192 |
| report_v10_cost.py | ff53c055c4b9b5e8338d3fd1e5ea834410470e59d624a24510055752a57fa92a |

The report's source hashes remain:

| Aggregate source | SHA256 |
|---|---|
| group-regions.json | 911804a20f8d471159ad402fecc1ca704e4ceb92fc9fce00656a15db7769406d |
| summary.json | 08534d91d5094c11dcd24d0f1d71b8d689b3af54fa5f3591993a7be6192aa823 |
| manifest.json | 0f3605b9664f973c25458ccfb77f1588c8a5bb6e3d31849dadf075c2fd434c15 |
