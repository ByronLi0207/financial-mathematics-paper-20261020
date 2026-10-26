# WP6 final main-text and citation readback

Review date: 23 October 2026. Disposition: **PASS; no open substantive scientific or author–date routing finding in the captured source and generated JSONs.**

This is an independent read-only review of `v6_submission.py` and the actual generated `submission-jof/manuscript-content.json`, against the V5 snapshots and WP2–5 public aggregate scalars. It also checks both current documents' reference lists against actual visible author–date citations, including S16. It does not certify the subsequently typeset PDF, package, external reference metadata, or independent financial replication. No production module was imported, no compose/main or financial worker was executed by this reviewer, and no raw source, private NPZ, per-origin financial vector, or model output was opened. The only file written by this task is this note.

JSON pointers below are zero-based in the captured current documents. Provenance fields and reference entries themselves were excluded from citation credit. Table cells and figure captions were included. Existing algorithm shorthand is not treated as a missing author–date citation.

## Scientific and reader-facing findings

### Matched finite wrappers: correct 15.00% scope

Main `/sections/6/blocks/8/html` is the added evidence paragraph. Its displayed 15.00% refers to the **FX H6 W2880 ACI_QR versus ACI_F** public pair. Exact public values are:

| Scalar | ACI_QR | ACI_F |
|---|---:|---:|
| Native mean pinball loss | 393795.05776986334 | 463271.4662733057 |
| Strict breaches | 329/6625 | 328/6625 |
| Strict breach fraction | 0.04966037735849057 | 0.04950943396226415 |

The loss percentage is `-14.99691078803782`, displayed as 15.00% lower. The text explicitly says long-history short-horizon **matched** context and **finite projected delayed ACI-style wrappers**, then says the joint score–frequency result gives no conditional-coverage or canonical ACI guarantee. It does not replace the original rolling-F primary, claim an inherited ACI theorem, or use these observed frequencies as proof of calibration.

### Original primary, matched contribution and Murphy diagrams: separate identities

- Actual abstract: original FX primary reduction **12.660%**, followed by the separately named matched reduction **14.77%**, and matched breaches **360 to 376**. The original-primary percentage is the archived QR2880-minus-rolling_F720 scalar, not the matched F2880 percentage.
- Main `/sections/0/blocks/6/html`: the matched `-14.77%`, DM `-5.866`, Holm `2.86e-07` and breach comparison route to Tables 3 and 5. The distinct original FX primary routes to Figure 3; the original Treasury primary routes separately to Figure 4. The exact original-primary bridge now routes to Table 4.
- Main `/sections/6/blocks/2/html` still describes **both original-primary** Murphy curves as crossing; it does not relabel them as wrapped or matched comparisons.
- Main decision map `/sections/8/blocks/3/rows/0` expressly distinguishes original-primary crossing from the matched wrappers' separate diagnostics.

### Adverse and incomplete evidence: retained and correctly bounded

- **SAV:** public primary-context losses are FX 456696.2216696064 versus matched F 452692.9834478481, and Treasury 2892.2308802158063 versus matched F 2758.665342960289. “Does not beat matched F in either primary context” is correct.
- **Fixed combinations:** Treasury median is lower than matched F by 3.9812983393% and QR by 36.3210877040%, but has **28/277 = 0.1010830325** breaches. The main text explicitly names **matched F and QR**; it does not call these the median's only two constituents. FX mean and median are respectively **4.8725050864% / 4.2206875112% worse than QR**, so the statement that neither beats QR is correct.
- **States:** both the paragraph and decision row explicitly refer to the **original FX primary**, including its rolling-F control. All three FX observed group means are negative; all three Treasury means are positive. The text does not claim an advantage confined to the high state, significance in every group, a state-only GW rejection, or a switching policy. The decision row acknowledges imbalanced small Treasury groups.
- **Target levels:** the three available tau=.90 contrasts have the same signs as their own .95 named contrasts: FX primary `-9.2042887544%`, FX matched `-10.1459140785%`, Treasury primary `+25.4323374422%`; all reversal flags are false. Tau=.99 has three unavailable slots. The paragraph retains failed-validation/insufficient-tail causes; the separate decision row expressly says this check **does not cover shorter-history or longer-horizon targets**. It gives no evaluated .99 robustness claim.

### Source, dates and economic interpretation: preserved

Main Section 3 retains the original record dates, gap counts, maturity endpoints and economic-date/public-release distinction. It continues to call Treasury a downloaded-vintage replay, not a live as-released backtest. The new source wording further distinguishes attributed FX positions from an independently audited complete dealer book and the absolute signed Treasury aggregate from the sum of absolute dealer positions. The main introduction and limitations distinguish inventory motivation from identified changes in quotes, hedges, funding requirements or observed financial costs.

The actual budget paragraph `/sections/2/blocks/6/html` gives **FX validation/evaluation 1440/6625; W720/W2880; refits every24 records** and **Treasury 52/277; W52/W260; refits every13 records**, directly from the existing source specification. No new clock or pool definition is introduced by this text.

## Original scientific content preservation

Direct JSON equality checks against `v5-manuscript-before.json` passed for the existing scientific tables' `headers`, `rows` and `cell_html`:

| Stable block | Old label | Current label | Rows | Exact scientific fields |
|---|---|---|---:|---|
| `/sections/5/blocks/0` | Table3 | Table3 | 4 | unchanged |
| `/sections/5/blocks/2` | Table5 | Table4 | 3 | unchanged |
| `/sections/6/blocks/0` | Table4 | Table5 | 7 | unchanged |

All **four main figure objects** are exactly equal to the V5 snapshot, including captions and bindings. The **eight Table1 literature rows** and the **six original Table2 method rows** are also unchanged; Table2 has three additional method rows. The decision map is deliberately revised and is not an empirical-result table. Existing numerical claims outside those tables were read in context; the actual contribution, abstract, evidence and decision text was checked rather than inferred only from source replacement expressions.

An initial inventory loop expected the old declaration count and reached the deliberately removed AI-disclosure placeholder; that reviewer-loop indexing error was corrected by checking the intended stable blocks directly. It was not a document failure, and the final successful checks below do not depend on that loop.

## Final author–date routing: both current documents

**Main:37 listed IDs,37 actually cited; supplement:25 listed IDs,25 actually cited. Uncited lists are empty. No actual author–date citation was found without an entry in its own document.** The lists have **21 shared IDs and41 unique IDs**; every shared entry's reference HTML is exactly equal. There are no duplicate IDs in either list.

The V5 preflight's two concrete routing improvements are now present:

- Main `/sections/3/blocks/25/html` has the actual classical Lévy attribution **“(Sussman, 2023)”**. Sussman is not copied into the supplement merely to create an unused reference.
- Supplement `/sections/12/blocks/12/html` explicitly begins the QRF description with **Meinshausen (2006)**, and the supplement now lists the same existing main entry.

The following are actual new method citations, not inferred from algorithm names:

| Actual source | Current main route | Current supplement route |
|---|---|---|
| Gibbs and Candès (2021) | `/sections/1/blocks/3/html` | `/sections/15/blocks/3/html` |
| Engle and Manganelli (2004) | `/sections/1/blocks/3/html`; `/sections/4/blocks/10/html` | `/sections/15/blocks/3/html` |
| Giacomini and White (2006) | `/sections/4/blocks/8/html` | `/sections/15/blocks/26/html` |
| Diebold and Mariano (1995) | `/sections/4/blocks/8/html` (Diebold–Mariano) | `/sections/15/blocks/1/html` |
| Newey and West (1987) | `/sections/4/blocks/8/html` (Newey–West) | `/sections/15/blocks/1/html` |
| Harvey, Leybourne and Newbold (1997) | `/sections/4/blocks/8/html` | `/sections/15/blocks/1/html` |
| Holm (1979) | `/sections/4/blocks/10/html` | `/sections/15/blocks/1/html` |
| Kupiec (1995) | `/sections/4/blocks/10/html` | `/sections/15/blocks/6/html` |
| Christoffersen (1998) | `/sections/4/blocks/10/html` | `/sections/15/blocks/6/html` |
| Ehm et al. (2016) | `/sections/6/blocks/2/html` | `/sections/15/blocks/17/html` |

For the pre-existing entries, the main/supplement routes recorded in `citation-preflight.md` remain actual current text, apart from the reference-list sorting which changes `/references` indices. That prior inventory covers the original40 IDs; this review inspected all current visible year-bearing strings/table citations and separately required a concrete current-body match for every listed ID, checking author/year combinations rather than surname hits alone. Corporate/date-version and shared-surname cases were manually adjudicated:

- `fr2004` resolves to the main “Board of Governors, March2013 and July2024 instructions” citation; FR2004 is a form number.
- `dataset` is explicitly credited by **Lindsay (2020)** in the main data-source paragraph `/sections/2/blocks/5/html`; coauthorship in Wisniewski's paper is not the sole basis for crediting it.
- Gneiting (2011) and Gneiting, Balabdaoui and Raftery (2007) are separately cited; Wisniewski2020 and2024 are separately cited.
- The Ehm consulted-preprint2015 date, thesis cover/year distinctions, data dates, and the historical New York Fed announcement year are not treated as extra dangling author–date citations.
- Acronyms such as ADMM, QRF, HAC, DM, HLN and method labels in tables are not fabricated author–date citations.

The actual generated S16 contains **31 tables and1174 data rows**, plus two added figure blocks. This note checks its actual citation passages and the main synthesis; it does not independently re-audit every S16 scalar export or the typeset layout. Parent's separate scalar-admission and authoring checks cover those scopes.

## Captured fingerprints

```text
b8b5e5b16a1f4503346cfb434debf08b1772b60ee0d303db7026f003f0ebf584 v6_submission.py
ec01ca2414530fa88d2e3d1faa144174c4dcc65aa065e1ee8039c2ff8f7a2eb7 v6_supplement.py
b190d268dd9a089c56304112b3daea904365dc11d00d4e7130b7ebfe90cd643e submission-jof/manuscript-content.json
77ec81d9a422ea6ec036302dadbca8d7a159aa5243d8d89177caae615c2c6094 submission-jof/supplement-content.json
2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7 notes/revision-v6/v5-manuscript-before.json
6cef270b0958f6895ab091589289e9aed17fca46c1cdc30d5c0118d5fe206e8a notes/revision-v6/v5-supplement-before.json
7f0653c9181a434377e36d49ca9f6eae394eada2ed65702dc993b2ca044f9e9d notes/revision-v6/reference-additions.json
8841a9258bae71c4c162afc6c5efd91ff4fa2a323621db637b7f012cf1623972 results/revision-20261023/v6/wp2-findings.json
44beea32857e5f13233178e014c4ed4737918f523b61790e42d2c94ee763f98c results/revision-20261023/v6/wp2-summary.json
abe27d8f1ef08ba50680b6f3e1a9207f7271cdb4270f92437fbaa1746ad523e9 results/revision-20261023/v6/wp3-findings.json
1526d8aa656077445988271c76988c0a950cd95631946add3d8b8642629c7aaa results/revision-20261023/v6/wp3-combinations.json
63a89756ba5a97e9a4454701708ff12972e2d23cfd24c238b25b490a531e833d results/revision-20261023/v6/wp4-states.json
085d2dbf7a94a13f3b1557d966848cf5f58382fa4f330dc8e221235427c71501 results/revision-20261023/v6/wp5-tau-summary.json
```

## Verification evidence

Commands were public-document-only Python3 here-doc reads and static `ast.parse`, executed from the repository root; no production imports or file writes were performed by those checks. Literal final output:

```text
PASS:14 archived scientific table rows and4 main figure objects unchanged; old8 literature rows and6 method rows preserved.
PASS: generated15.00 paragraph, original-primary/matched scope, tau-scope fixes, Sussman and Meinshausen routes present.
PASS: main source AST valid; documents read only; no production module imported or main executed.
UNCITED submission-jof/manuscript-content.json []
UNCITED submission-jof/supplement-content.json []
REFERENCE_COUNTS 37 25 COMMON 21 UNION 41
COMMON_REFERENCE_CONSISTENCY PASS
MAIN_SUSSMAN_ROUTE ['/sections/3/blocks/25/html']
SUPP_MEINSHAUSEN_ROUTE ['/sections/12/blocks/12/html']
S16_TABLES 31 ROWS 1174
```

The source and two generated JSON hashes above were rechecked at note completion. Any later content change requires a targeted readback of the changed material; these observations do not certify unobserved future bytes.
