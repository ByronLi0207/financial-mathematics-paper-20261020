# Fixed synthetic exposure recording

The registered design requires transition/exposure counts in training,
validation and evaluation. `v9_exposure.py` records them without reading
outcomes or selecting repetitions. A transition at retained level b changes
the law generating that level. A label at t crosses it when t < b <= t+H.
Forward transitions and the artificial last-to-first wraps are separate.
Future-label regime counts include overlapping-label multiplicity; unique
training level-span counts are labeled separately.

Two constructed tests cover a switch exactly at the first issue, a training
label crossing that switch, the artificial wrap, unchanged completed-label
training boundaries, both W values, and a no-break control.

- RED: temporary uv environment, `pytest -q test_v9_exposure.py`:
  2 failed, both `ModuleNotFoundError: v9_exposure`, before implementation.
- GREEN: same command after implementation: **2 passed in 0.09s**.
- Logs retained privately: `.scratch/v9/exposure-red-uv.txt` and
  `.scratch/v9/exposure-green.txt`.
- The first attempt with the bundled bare Python could not import pytest;
  it was an environment check, not an observed behavioral RED. Packages
  were then supplied by uv; system Python was unchanged.

All inputs were small artificial arrays. No financial diagnostic,
calibration, bootstrap, pilot or formal study was run by this check.
