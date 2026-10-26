# Public PR #5 v8 document snapshots

These eight immutable text/table fixtures are exact `git show` bytes from public commit `0f1f066843e0c49cf3e24bce7d72032dc189603d` (`revision-v8-goal`, PR #5). `manifest.json` records each original public Git blob ID, byte count and SHA-256. The fixtures contain no Git commit objects, history bundles, raw input data or new results.

`test_v8_main_numbers.py` and `notes/revision-v8/test_v8_supp_numbers.py` copy these documents into their existing temporary negative-control trees. Their historical assertions and original source/evidence guards remain unchanged. The v9 draft may change without being forced to repeat old v8 prose; new v9 document acceptance has its own checks.

The main checker continues checking the original protected figure paths in the repository; v9 figures must use new names. The old numeric checkers still require their original local historical Git objects. These public text fixtures do not supply or bypass those objects and do not make the whole original suite independently reproducible from a fresh public clone.

For a future manuscript version, add a separately named baseline with its own public source identity. Do not edit these fixtures to make a changed draft satisfy historical tests.
