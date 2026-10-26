# Final consolidated JoF manuscript — final-jof

From the root of the complete `final-jof` repository checkout, using an **already available** Python environment with NumPy and Matplotlib, rebuild every main table and figure with one command:

```sh
python3 reproduce_final_displays.py --output final-display-rebuild
```

The output directory must be new. This entry formats saved public fields and draws saved plotting primitives; it performs no data acquisition, model fitting, loss/HAC/bootstrap rerun or new scientific summary. It creates six numbered table TeX files, four numbered PDF/PNG figures and exact bindings in `rebuild-receipt.json`. It also compares every main table's data cells with the current manuscript. The two-panel descriptive table is compared in full, including both panels. The three original inline tables bind 45 distinct saved setting/result operands through exact JSON pointers or unique CSV row selectors. The decomposition preserves 540 primitive bindings and all 482 records in the unified history display remain unchanged.

This command was actually exercised in an existing offline cached environment with NumPy 2.3.5 and Matplotlib 3.11.2. Six constructed contracts passed. Three rebuilt figure PDFs match the accepted bytes exactly; the decomposition differs only in PDF creation-date metadata and has identical rendered pixels and all 540 primitive bindings. `notes/final-merge/wp7-display-equivalence.json` records the comparison. No dependency was installed for this task. A fresh environment must already provide the documented dependencies; the entry never installs them.

## Editorial source files and compilation

`main.tex` is the article entry and inputs `manuscript.tex`. Compile `main.tex`, `supplement.tex`, `title-page.tex` and `cover-letter.tex` separately with an existing compatible LaTeX runtime. The task used the existing Tectonic runtime. `references.bib` is supplied for editing; the inline native bibliography is the compiler's owning source. `figure-legends.tex` is synchronized to the four current main captions.

The Overleaf ZIP is an editorial source package containing only these editable texts and their transitive table/figure dependencies. Its README explains the repository command above, but the ZIP is **not** a complete model-replay archive: saved-result rebuilds require the full repository checkout. Use the [versioned repository](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/final-jof) for results, protocols and build code. Run no older manuscript builders over `submission-final/`.

The combined paper reports PARTLY for the transported CFTC history predictions. Short-history counts pass; long-history and strict-improvement targets fail, and the full procedure has no eligible high-region cell. Negative, unavailable, censored and inspected-period outcomes remain explicit. These related aggregate markets are not independent dealer records; causal estimation-cost identification and a universal sufficient history bound remain unestablished.

## Raw-input replay is a different operation

The one-command display entry does **not** run this section. Raw replays require separately authorized computation, exact existing protocols, lawful source access and the pinned input vintage. Never rerun into a completed results directory, replace a failed result with a successful subset, truncate a different vintage to imitate a hash, or silently switch to a different member/frequency.

### FX — user-obtained rights-dependent input

1. Visit the [Kaggle Net Position Time Series Dataset](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset), select version 2, and review the owning rights notice.
2. Obtain only `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv`. If delivered in a ZIP, inspect its members and extract that file only; the full dataset collection is unnecessary.
3. Require 18,576 records, 1,286,391 bytes and SHA-256 `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`. On macOS, `shasum -a 256 /path/to/1hourNetPositionsKaggle.csv` prints the fingerprint.
4. Only after the rights and exact-byte checks, supply it at the path required by the specific legacy replay protocol. Preserve a mismatching existing file; this source package includes neither raw FX observations nor private forecast vectors. Source access does not itself establish redistribution permission.

### CFTC — exact retained official archives

1. Use the [CFTC Historical Compressed owning index](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm), the Traders in Financial Futures, futures-only text archives.
2. The study uses the 2006–2016 backcast and annual 2017–2026 files below. `data/cftc-tff/provenance.json` retains each original URL, acquisition times, bytes and SHA; the URLs below are copied exactly from that record, not newly guessed.
3. Verify each downloaded ZIP's complete bytes before any parse. In particular, the current-year archive may have changed since the pinned download; a new download with a different hash does not reproduce the retained vintage. Preserve it separately and report the mismatch.
4. Use the immutable CFTC source/eligibility design and the WP2 seal for any separately authorized replay. No acquisition, universe reranking, market substitution or model rerun was done to prepare these instructions.

| Archive | Bytes | SHA-256 | Owning route |
|---|---:|---|---|
| `fin_fut_txt_2006_2016.zip` | 3166765 | `c3a8d01765133a24ce9c082de88933816497d06f1b03eec8c53750bdd818f14b` | [official file](https://www.cftc.gov/files/dea/history/fin_fut_txt_2006_2016.zip) |
| `fut_fin_txt_2017.zip` | 395830 | `e6e2dd537efcc57cdd6cdcc4e45e567fd47e65d8afc8369d8383bf09195ae7f5` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2017.zip) |
| `fut_fin_txt_2018.zip` | 458570 | `6843d130a25a17c6248df67463810f02077ef4eeafdd629299d21c18f5125e40` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2018.zip) |
| `fut_fin_txt_2019.zip` | 454803 | `631b31880d513072aa50d63117c896184dd35db3cc8fcdd6debd80197ee7a661` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2019.zip) |
| `fut_fin_txt_2020.zip` | 430721 | `c90d98d94db708772d669f263fb8061c75f8a7f681ba231fb21247e5c9798e6b` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2020.zip) |
| `fut_fin_txt_2021.zip` | 466549 | `5c929991038c70ae2501661b6d442b9e784d3c29d3166ceac2e21b45ac93d56a` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2021.zip) |
| `fut_fin_txt_2022.zip` | 494559 | `94c9c1fdee9dfbe377a09923ddfe26b88d3460605dd076081f221ad367d88601` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2022.zip) |
| `fut_fin_txt_2023.zip` | 506931 | `43c3dbdd4d01fceefad5e457003751cdc0974c7cf46097b322e26e9e2fe44d7a` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2023.zip) |
| `fut_fin_txt_2024.zip` | 563591 | `3f00585741a7cf76c207df640951d644dd91ff22a1106b38ca37a2469c765637` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2024.zip) |
| `fut_fin_txt_2025.zip` | 627068 | `2ea0cda6395f7dd6501c27422be3763e1f2f5b41b768cfd36b871f092a07d438` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2025.zip) |
| `fut_fin_txt_2026.zip` | 596508 | `b9920b083356418e594da9a9903c5e0782984780c1af970d34f949e1b27d3559` | [official file](https://www.cftc.gov/files/dea/history/fut_fin_txt_2026.zip) |

### NYFed — downloaded vintage, source terms and legacy exception

The accepted Treasury input is the [unchanged attributed PDPOSGS-B snapshot](../data/nyfed-pdposgs-b-20261022/README.md): 706 observations, 23,315 bytes, SHA-256 `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb`. A current API response can extend or revise it. Other weekly categories retain their own metadata/fingerprints in the original protocols; matching a series label is insufficient.

NYFed source terms continue to apply. The inherited Treasury raw-delivery exception and the frozen specification's original no-raw field remain separately disclosed; this merge does not rewrite their historical mismatch. Downloaded economic-date records do not reconstruct historical first public releases. Public redistribution and the final tracked-file inventory are subject to the separate WP8 gate.

## Reproduction and author boundaries

A display rebuild, source compilation and passing fixture tests do not establish independent financial replication. Earlier full tests used a read-only local historical Git object directory for original provenance assertions; a fresh public clone does not thereby acquire that history. The exact exception is retained in `FINAL_MERGE_CHANGELOG.md` and `USER_DECISIONS_FINAL_MERGE.md`.

Author details, funding, competing interests, required journal declarations and reviewer nominations remain for the author. The five proposed reviewers and ten anticipated questions are in `notes/final-merge/`. No submission or contact has occurred. Existing `.bak` files are preserved outside this source package and listed for the author; none belongs in `submission-final/` or its Overleaf ZIP.
