# Independent WP3 synthetic mathematical review

Status: PASS. This is an internal code review using synthetic fixtures, not an
independent financial replication or validation of prospective forecasts.
No financial NPZ, position source, panel outcome, or public financial summary
was opened. Production implementation files were read but not modified.

The standalone script `wp3-independent-oracle.py` exhausts all 729 configurations
of two observations with left/right/actual values in {0,1,2}. Its independent
indicator definition uses Fraction(19,20), checks every unique breakpoint and
interior interval midpoint, verifies the final endpoint is zero, verifies the
integer-event difference and dominance/crossing classification, and proves the
rational integral equals the rational pinball difference within each fixture.
The separately returned floating integral and loss difference are checked with
relative/absolute tolerance 1e-14.

The second oracle uses seed 20261023 and 100 synthetic 40-observation fixtures.
It verifies common-floor feasibility, exact median=F when KNN=F, and the convex
pinball bound against the average constituent loss, with absolute arithmetic
slack 1e-13. It does not assert improvement over the best constituent, conditional
quantile correctness, calibration, or general dominance beyond these fixtures.

The exact actual command, runtime versions, tested production fingerprints,
literal child stdout/stderr, exit code 0 and observed wall time are retained in
`wp3-independent-oracle-output.txt`. It records 729/100 passed cases.

Integration boundary: the orchestrator must independently admit the complete
origins, matching source/units/H/W/floors, constituent identity and panel public
summary reproduction. The array-only combination helper cannot determine these
metadata from equal-length vectors.

Script SHA-256: `15647706962caf152676d205ae5df9b3788aad0ce9bc79040611fa3531fd6c90`
Output SHA-256: `151577816c99c1bfa4bdf1890eee072a213555e1fe73ba59730c9da370f734b0`
