# WP7 final source audit

**Outcome: PASS within the source-only scope below. No missing/unused displayed reference, duplicate or invalid internal target, frozen-method-definition mismatch, or changed empirical table value was found.**

This independent check read current document JSON/standard TeX, public result summaries, frozen protocols, Python source text and local Git snapshots. Only this new audit note was written. No private array was opened, no model/financial computation was executed, and no source/result/document file was edited. Pure TeX regeneration and contextual aggregate-format regeneration ran in memory without output writes.

## Current documents and exact source coherence

Both current `.tex` files equal the full output of `v4_typeset.tex_document()` on their current JSON document, character for character. The checks used the actual rebuilt sources, not a remembered PDF identity.

| Document/source | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `3a13df3d818218b095f4a6a4c548221c1ce233ed4317e7a5b1784ca24095b28d` |
| `submission-jof/manuscript.tex` | `875516d3f7840e80f3b07de6783c68bc9efff248afff48ec280387d17c2bfab1` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `submission-jof/supplement.tex` | `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8` |

The current preview hashes were observed as main `0e538ae5dc16592ff30362151fb37005294187810ec240dbbc0305554cb52e9d` and Supplement `7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991`. These are identity observations only; this source audit does not substitute for the separate final visual checks.

## References: all displayed entries used; no missing explicit author–date route

- Main: **37 listed IDs, 37 unique, all 37 actually cited** in visible prose/table/caption text.
- Supplement: **25 listed IDs, 25 unique, all 25 actually cited** in its own visible text.
- Union: **41 IDs**; the **21 shared entries have identical reference HTML** in both documents.
- Explicit visible author–date/data-source contexts were read back and matched to the owning document list. No visible citation lacking an entry was found. Names in `_bindings`, `_source` or the reference list itself did not count as usage.
- Ambiguities were adjudicated: Lindsay (2020) is credited through the explicit Data sources paragraph, not through coauthorship of Wisniewski et al.; Gneiting (2011)/(2007) and Wisniewski (2020)/(2024) were matched by year. FR 2004 is a form identifier: the explicit Board of Governors March 2013/July 2024 instruction attribution correctly routes to `fr2004`.
- This is current citation routing, not fresh external-source retrieval or re-verification of bibliography metadata, publication facts or original-text reading scope. Previously stated version/access limitations remain.

One actual route per listed ID is below. Pointers are zero-based `section/block/field` in the named current JSON; table rows and figure captions are visible content. A dash means the entry is not listed in that document.

| Reference ID | Main actual route | Supplement actual route |
|---|---|---|
| `arjani2020` | `1/0/rows/3` | `14/19/html` |
| `avellaneda2008` | `9/4/html` | `—` |
| `barone1999` | `1/3/html` | `6/11/html` |
| `biau2011` | `1/3/html` | `—` |
| `boudoukh2004` | `1/0/rows/1` | `14/17/html` |
| `boyd2011` | `—` | `3/3/html` |
| `casgrain2023` | `—` | `4/7/html` |
| `christ1998` | `4/9/html` | `8/1/html` |
| `dataset` | `2/5/html` | `—` |
| `dm1995` | `4/7/html` | `15/1/html` |
| `duffie2023` | `0/0/html` | `14/22/html` |
| `ehm2016` | `1/0/rows/5` | `14/21/html` |
| `engle2004` | `1/0/rows/4` | `14/20/html` |
| `fr2004` | `2/1/html` | `—` |
| `gibbs2021` | `1/3/html` | `15/3/html` |
| `gneiting2007` | `6/2/html` | `—` |
| `gneiting2011` | `1/3/html` | `5/3/html` |
| `gw2006` | `4/7/html` | `15/26/html` |
| `hansch1998` | `0/0/html` | `—` |
| `henzi2022` | `—` | `4/7/html` |
| `hln1997` | `4/7/html` | `15/1/html` |
| `ho1981` | `0/0/html` | `—` |
| `holm1979` | `4/9/html` | `15/1/html` |
| `hoogen2017` | `1/2/html` | `—` |
| `hull1998` | `1/3/html` | `6/11/html` |
| `koenker1978` | `1/3/html` | `—` |
| `kupiec1995` | `4/9/html` | `15/6/html` |
| `liao2005` | `1/2/html` | `—` |
| `lyons1995` | `0/0/html` | `—` |
| `mcneilfrey2000` | `7/3/html` | `12/10/html` |
| `meinshausen2006` | `1/3/html` | `12/12/html` |
| `nw1987` | `4/7/html` | `15/1/html` |
| `nyfeddata` | `2/5/html` | `—` |
| `petrunia2019` | `1/0/rows/2` | `14/18/html` |
| `politis1994` | `—` | `2/5/html` |
| `sozen2026` | `1/3/html` | `—` |
| `sussman2023` | `3/25/html` | `—` |
| `wisniewski2020` | `1/0/rows/0` | `14/16/html` |
| `wisniewski2024` | `1/0/rows/0` | `14/16/html` |
| `xu2023` | `1/3/html` | `—` |
| `zhou2024` | `1/3/html` | `—` |

## Physical labels and internal cross-references

- Main tables occur exactly once in physical order **1–6**; Supplement tables exactly once in order **S1–S68**. Main figures are **1–4** with body placements `[0,1,2,3]`; Supplement figures are **S1–S7** with placements `[0,1,2,3,4,5,6]`. No missing, duplicate or out-of-range placement was found.
- Numbered-reference scan and semantic readback covered **88 main** and **90 Supplement** internal reference occurrences, including captions and descriptive/reference-bearing cells. All targets exist. Source-paper page/figure/table locators in S15 were treated as external original-source locators, not incorrectly checked against this paper's labels.
- The former routing defects are corrected: main Table 2 scopes original QR/KNN choices to S2 and routes additions to S16; main Table 6 says “Tables 3 and 5; Supplement S16,” not the unrelated old Table S16.
- Table 4 is the descriptive original-FX gain bridge; Table 5 is coverage diagnostics. Original-primary Figures 3–4 / S4–S5 remain distinct from fixed-combination Figures S6–S7.
- The final source-specific captions are correct: FX matched frozen F W2880 is distinct from original rolling F W720; Treasury matched F W260 is also the original-primary historical reference. The Treasury caption explicitly says the new plotted pairs are combination-versus-constituent comparisons, not the original QR-minus-F pair.

## Final method definitions against frozen code/protocol

- **ACI:** initial alpha .05; strict hits use the earlier issued wrapped report; completed base scores use the H-horizon peak minus its historical base report. At each issue newly mature feedback is consumed once in chronological order, each update adds gamma times (.05 minus the hit) and projects with the current pool size. An additional pre-issuance projection and exact ceiling rank use that same current size. Rank zero returns the known floor. The carried validation state is not described as reset at evaluation. This agrees with `v6_aci.py` and the WP2 protocol.
- **SAV units:** mature responses and H-lag shocks are divided by the positive refit response scale. The normalized recursion is restored to source units by multiplying by that same held scale before adding the issue floor. Current prose `C_t=B_t+a_kappa max(0,qtilde_t)` agrees with implemented `head=current.scale*previous; report=abs(position[t])+max(0,head)` because the scale is positive. No omitted scale factor remains.
- **GW/state normalizers:** a0 is the initial mature QR response scale; the driver reproduces it from the exact first pool and checks the archived first-fit identity. v0 is max(training short-RMS mean,1e−12), with no evaluation fit. Full-axis influence uses the group indicator, centered loss difference and group share; zeros outside the group remain on that axis. GW uses matured H-lag loss and issue-known short RMS, divided by those fixed normalizers, after H burn-in. Joint rejection is not asserted to imply a state effect. These definitions match `v6_states.py`, `v6_wp4.py` and the frozen WP4 protocol.
- Current ACI/SAV/inference/worker and states/WP4-driver source hashes were compared to their actual executable-freeze `files` entries; every checked source matches its frozen digest. This verifies the comparison was to the executed-code identities, not newly edited models.

## Empirical table preservation

| Comparison | Checked inventory | Result |
|---|---|---|
| Frozen v5 main snapshots → current main | Old Table 3 → current 3 (4 rows); old 4 → current 5 (7 rows); old 5 → current 4 (3 rows) | All 14 empirical rows and all headers exactly equal |
| Frozen v5 Supplement snapshot → current S1–S37 | 37 tables, 449 rows | Every header and complete row exactly equal |
| Last committed v6 document `5362e76` → current S38–S68 | 31 tables, 1,174 rows | Every complete row exactly equal, even before whitespace normalization; normalized mismatches = 0 |
| Current S16 numeric tables → current bound public inputs | All 31 tables through production `validate_block` contextual regeneration | PASS, no mismatch |

The old snapshots are `notes/revision-v6/v5-manuscript-before.json` and `v5-supplement-before.json`. The new-table baseline is the actual local committed `submission-jof/supplement-content.json` at `5362e76`; this is a preservation comparator, not a new public preregistration claim. Descriptive method/decision rows and captions are allowed prose edits and are not mislabeled as preserved empirical financial rows.

All seven public WP2–WP5 aggregate JSONs used by this synthesis were also byte-identical to the same committed v6 baseline. No financial outputs changed in this prose/caption revision.

## Source, protocol and result fingerprints

| File | SHA-256 |
|---|---|
| `v6_submission.py` | `e29b364d82c3a9bb9583cd517c92bf14534361a5bf6ae159b6766e976c58ee61` |
| `v6_supplement.py` | `e8e85e8d0d3b03c21349a21b3a71af7fa209eb2ffb54ec82cd33acffbbcd237b` |
| `v4_typeset.py` | `c632a2be466eb2b1ec8d5a76cb56da0edbd93dc6f8641ad41f87c674e06ac988` |
| `v4_numeric.py` | `553cfc10993f21098db0042708bc8c624c4b12a5567b67c11d811b0e84684146` |
| `v6_aci.py` | `e81005a25ca7b94dec86540981b890c945c280478b861e7416f7fb852f67b15a` |
| `v6_sav.py` | `a476828ee8818572a4b57e4b170ec4ee4ccecbef43c4babdf37138329ee586c1` |
| `v6_states.py` | `1c50807a3bd85906d9fcef971c9efa6e3784a712008635971e7b6ce1f9252d64` |
| `v6_wp4.py` | `3e322d7ec78d27fe499c5b8724206b5a522031ea3d29c4cc12b05e961acc575c` |
| `protocol/revision-v6/wp2-executable-freeze.json` | `c9fb8deff4a73ae3c9798de831d5d3a7a1d498b82789731460a09e4ebf1a3399` |
| `protocol/revision-v6/wp4-executable-freeze.json` | `91e0bc167c623d5fde73096395e5f387f17814efffa1f6f267d81b2e39d79ad3` |
| `protocol/revision-v6/common-contract.md` | `6795bc1e59d1b5e245c601ff55d77abbbb121bb2700affefa02a89b884a7f7e8` |
| `protocol/revision-v6/wp2-aci-sav.md` | `4d1115663011753ad85c41a9b5f6bf50b100e186d9a1c6d3c8b622fa996ac2e7` |
| `protocol/revision-v6/wp4-state-gw.md` | `e8a832e4a6c5cb17ac79d931d83a19836e597dcef713b4e5d26bc7cacb9b9259` |
| `results/revision-20261023/v6/wp2-summary.json` | `44beea32857e5f13233178e014c4ed4737918f523b61790e42d2c94ee763f98c` |
| `results/revision-20261023/v6/wp2-comparisons.json` | `37df0e0f87340cac9c0526484e123dba08fb914a795761f9ae9828fdfc6983fd` |
| `results/revision-20261023/v6/wp2-findings.json` | `8841a9258bae71c4c162afc6c5efd91ff4fa2a323621db637b7f012cf1623972` |
| `results/revision-20261023/v6/wp3-combinations.json` | `1526d8aa656077445988271c76988c0a950cd95631946add3d8b8642629c7aaa` |
| `results/revision-20261023/v6/wp3-findings.json` | `abe27d8f1ef08ba50680b6f3e1a9207f7271cdb4270f92437fbaa1746ad523e9` |
| `results/revision-20261023/v6/wp4-states.json` | `63a89756ba5a97e9a4454701708ff12972e2d23cfd24c238b25b490a531e833d` |
| `results/revision-20261023/v6/wp5-tau-summary.json` | `085d2dbf7a94a13f3b1557d966848cf5f58382fa4f330dc8e221235427c71501` |

## Limits

No independent financial replication, new external literature verification, private per-origin audit, fresh numerical model execution, entire-suite test claim or final PDF visual certification is made here. The check establishes source consistency, current citation/cross-reference routing, agreement of the final definitions with frozen implementations, and preservation of the displayed aggregate table values. Known author-supplied declaration/ORCID/funding/conflict placeholders are not invented or resolved by this verification.
