from pathlib import Path
p=Path('submission-v10/manuscript.tex');s=p.read_text()
replacements={
'The Supplement proves both statements and compares population quantiles with their empirical plug-ins.':'Supplement Sections S1--S2 prove both statements and distinguish population quantiles from their empirical plug-ins; Sections S3--S5 give the bound simulations.',
'The Supplement lists every selected code and exclusion reason.':'Supplement Section S30 lists every selected code and explains the eligibility rules; complete code-level exclusions remain linked there.',
'The Supplement lists complete results and numerical or structural failures.':'Supplement Sections S7 and S11--S18 report benchmark results and failures; Section S34 links the complete legacy inventories.',
'Training-only transforms and fixed neighbor menus; Supplement':'Training-only transforms and fixed neighbor menus; Supplement Sections S8 and S23',
'Existing bounded specifications, complete failures included in Supplement':'Existing bounded specifications; results and complete failures linked from Supplement Sections S7 and S34',
'Quantile and normalization conventions are detailed in the Supplement; this table does not expand any executed menu.':'Quantile and normalization conventions are detailed in Supplement Sections S8 and S23; this table retains the executed menus.',
'The Supplement records comparison families, execution chronology and complete failure inventories.':'Supplement Sections S14--S17, S19, S23 and S29--S34 give comparison families, chronology and failure inventories.',
'The Supplement reports the training-defined state, target-level and overlapping full-prefix comparisons.':'Supplement Sections S20--S21 and S26 report the state, target-level and overlapping full-prefix comparisons (Tables S19--S21 and S25--S26).',
'The Supplement retains every completed loss and model failure.':'Supplement Sections S16--S18 retain the combination and headroom-recursion results, including completed losses and failures (Tables S14--S17).',
'The Supplement lists all panel and selection results.':'Supplement Sections S11--S15 list all panel and selection results (Tables S9--S13).',
'Every set, method p-value, equivalence class and prior unavailable method appears in the Supplement.':'Supplement Section S31 retains every set, method p-value, equivalence class and prior unavailable method.',
'(Supplementary Murphy diagrams)':'(Supplement Figures S1--S2, Section S33)',
'(the Supplementary diagnostics)':'(Supplement Table S46, Section S33)',
'The Supplement retains its diagnostics and all earlier simulation grids.':'Supplement Sections S27--S28 retain the earlier calibrated simulations and stability diagnostics (Tables S27--S32).',
'These are illustrative costs, not observed operating costs; the Supplement gives the normalization, fixed grid and complete-method results.':'These are illustrative costs, not observed operating costs; Supplement Section S32 gives the normalization, fixed grid and complete-method results.'
}
for old,new in replacements.items():assert old in s,old;s=s.replace(old,new)
p.write_text(s)
