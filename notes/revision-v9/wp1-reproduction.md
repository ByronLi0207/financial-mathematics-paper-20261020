# Reproducing the v9 WP1 saved-result description

Use the already available Python runtime and temporary dependencies. The actual run was offline; no software was installed into the system environment. The source study is not rerun. From the repository root, an absent, user-chosen output directory is required:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --no-project --no-env-file --with pytest --with arch --with scikit-learn --with matplotlib \
python -B v9_posthoc.py --output /path/to/new/output-directory
```

The frozen numerical versions are Python3.12.14, NumPy2.3.5, SciPy1.18.1 and scikit-learn1.9.1. The plot-only recovery used cached matplotlib3.11.2. A different numerical runtime, changed input bytes, missing pre-calculation design commit, nonconvergent classifier, incomplete final-report pairing or an existing output path stops the command. Downloading free-to-read original financial data is not required for this saved-result calculation.

The local design commit is checked in Git ancestry. A browser-content-only export without that local object cannot pass this ancestry check, even when all files are present; this is an acknowledged public replay limitation rather than a verified fresh-clone execution claim. The independent audit provides a saved-output check without importing the production analyzer. The completed v9 publication gate will report content identity and fresh-clone replay separately.

For the original run, `run_wp1_bounded.py` records the exact command, imposes a sub-ten-minute resource deadline, samples descendant RSS and thread counts, and preserves stdout and the return status. Its original omitted matplotlib dependency and consequent plotting failure are retained. Reading the already saved numeric JSON with `plot_initial` recovered the plot without another fit/bootstrap. The saved bootstrap file retains every draw, index vector and index hash. A complete reproduction should include matplotlib from the outset as above; this document does not claim that such a new complete run has already been executed.
