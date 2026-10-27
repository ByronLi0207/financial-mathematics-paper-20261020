# Reproducing the v13 manuscript

This is a draft pending the actual G4 clean-clone check. Do not describe it as tested.

The authoritative editable manuscript is `submission-v10/` on `revision-v13`. Use the current source files and transitive display dependencies; older prose builders overwrite later editing and must not be run. See `notes/v13/G4-reproduction-plan.md` for the proposed clean-clone sequence and input boundaries.

The planned numerical checks reconstruct all CFTC inputs from the eleven already saved official ZIPs, re-estimate all 204 contract/history/method cells behind the 170 Table 5 percentages, and independently re-estimate the original Treasury-bill primary and the preselected PDPOSCS-TOT H6/W52 panel cell. These are reproductions of existing computations, not changed models, menus or evaluations.

No download is needed. The panel CSV and private FX CSV must be supplied as pinned original raw bytes, not as prior numeric traces or prepared model caches. Their exact identities and the original procedure distinctions are listed in the detailed plan. All re-estimation outputs must use a new temporary directory.

Legacy experiment drivers and full historical tests retain original local Git-object prerequisites. The v13 check will call unchanged source-independent functions; it will report missing prerequisites instead of weakening guards. Retain version-specific `notes/v12/REPRODUCING.md` as a historical record.
