# Monte Carlo orchestration tests

The design was already committed as b7e548df39bc2d5dc0108a01ec8a7c2ccfbb99d4 at2026-10-24T00:37:44-07:00.

RED: `python -m unittest test_v8_mc -v` before v8_mc.py existed:6 tests,6 errors (ModuleNotFoundError:v8_mc). No financial files opened.

GREEN: same command after implementation:6 tests passed. Tests independently check exact completed-label geometry, infinity tie selection, full-menu failure, whole-cell failure despite a successful repetition, all-repetition/IQR aggregation, timing ladder independent of losses, and unassessable predictions when required cells are missing.

Calibration and DGP/oracle test logs are separate. The production runner uses four processes with one numerical-library thread each. Pilot and formal streams are separate; pilot outcomes are excluded from reported accuracy.
