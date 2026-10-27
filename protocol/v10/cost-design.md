# E4 fixed limit-cost design — before any cost means or regions

Use the saved reports only. No new forecast, model fit, data request, fitted cost coefficient or outcome-selected comparator. The chosen expanded-menu QR33 procedure is a fixed comparator, not the minimum-cost method. The daily archive has only its original narrow-menu QR33; its figure is explicitly identified separately.

Normalize reserve and excess amounts by matched F mean headroom within each source/period/H/W cell. A grid point beta represents a fixed breach charge of beta times that same mean headroom, so the fixed term is dimensionally consistent. Zero/nonpositive mean headroom gives unavailable, not a replacement denominator.

All complete E3 methods enter regardless of MCS membership. The primary plots display separate source-group win fractions across their planned comparison grids; individual source/H/W regions and the complete parameter inventory are retained. No favourable cross-source pooling, tuning or conditional-model selection follows the cost results.

The following machine settings are fixed before E4 computation.

```json
{
  "schema": "v10-cost-design-v1",
  "created_utc": "2026-10-24T23:45:53.195815+00:00",
  "mcs_index": "results/v10/mcs/input-index.json",
  "mcs_index_sha256": "ff717e8075fed88d07427a450eb27bc91b84e1a4ae2a0e0862605c2b85990ac2",
  "inventory": "notes/v10/loss-input-inventory.json",
  "inventory_sha256": "2f10465195e774540d9a49079de37d4e6a56d0e22be634241b1d2a315b08abb2",
  "comparison_count": 98,
  "method_scope": "All complete methods in committed E3 registry; retain all60knownNA; no MCS membership filtering.",
  "reference_id": "F",
  "grid": {
    "kappa": [
      0.01,
      0.025,
      0.05,
      0.1,
      0.2,
      0.5,
      1
    ],
    "beta": [
      0,
      0.01,
      0.05,
      0.1,
      0.25,
      0.5,
      1,
      2,
      5
    ],
    "c": [
      0.5,
      1,
      2
    ]
  },
  "primary_c": 1,
  "formula": "kappa*mean(C-B)/mF + beta*mean(Y>C) + c*mean(max(Y-C,0))/mF",
  "scale": "mF=mean(C_F-B), computed separately on each full comparison grid in source units; beta=b/mF, so actual fixed-breach amount is beta*mF. kappa and c are per-unit amounts.",
  "unavailable_rule": "Absent/changed/unequal target, origins or provided floor; invalid C<B or Y<B; nonfinite data; absentF or meanFheadroom<=0=>wholecomparisonUNAVAILABLE, no epsilon, intersection or partial method deletion.",
  "missing_floor": "Only QR4/Levy missing stored B identified by E0 floor_recovery metadata may recover it from exact matching frozenF trace; verify copied source bytes/SHA plus entire origin/target axes and all existing floor arrays equal. Do not create a current-floor estimate or modify E3 index.",
  "primary_method_by_group": {
    "FX original": "R6::R6_R1",
    "FX early2015": "R6::R6_R1",
    "Treasury bills": "R6::R6_R1",
    "Other NYFed panels": "R6::R6_R1",
    "Same-record dailyFX": "daily_FX::QR33",
    "CFTC": "CFTC::QR33"
  },
  "primary_absence": "Leave plotcomparisonunavailable, do not substitute best or another model.",
  "plot": "Six group facets (kappa,beta) at c=1, each shade is fraction of planned source/H/W comparisons in which fixed primary method is strictly cheaper thanF. Show full planned denominator and unknown bounds; all98per-cell regions in CSV. Related-cell fraction is descriptive; no pooled independence.",
  "ties": "Exact floating equality; cheaper iff difference<0. No threshold/tolerance chosen from outcomes.",
  "report": "All methods and all189parameterpoints percomparison in CSV with primitive amounts/strictbreaches, percell primary regions and source-summary figures. Keep original primary references distinct in method inventory; no new models or forecasts.",
  "interpretation": "Per-issued-report cost, not sum over overlapping holding periods, optimized policy, observed coefficients or common-dollar cross-market portfolio. The illustrative/not-observed-real-cost sentence appears once in Limitations.",
  "code_and_input_gate": "Commit implementation after artificialtests, seal all new costcode,protocol,index and exactprivateNPZ fingerprints before single actualcostrun. Exclusiveoutputs; no scientific retries or changes togrid.",
  "run_limit_seconds": 600
}
```
