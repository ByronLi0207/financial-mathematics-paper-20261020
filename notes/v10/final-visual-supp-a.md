# E7 native-build Supplement visual QA: pages 1-17

**Scoped result: PASS, 17/17 pages individually opened.** This record covers visual quality of the first half only, not the remaining pages, main article, scientific claims or numerical accuracy.

Same-model internal visual review. Every individual PNG was opened with `tools.view_image`; no contact sheet or text extraction substituted for page inspection. Checked readability, margins, clipping, continued tables, equations, blank pages, and orphan headings/lines. No PDF, PNG or TeX was modified, no financial result was recalculated, and no shared UI/browser or cross-model review was used.

- PDF: `submission-v10/supplement.pdf`
- PDF SHA256 from final-native-build.json, also verified against the actual PDF: `8d67122b814b2b01410fceb0499c6c3aee92def0ccbd38603f68f2d21997cf0a`
- Native-build source ZIP SHA256: `bea59ba142898dc83a763419bc13cf50471bcf3a903e79013b7add73508af501`
- Reviewed UTC: `2026-10-25T00:18:07.356012+00:00`

No blocking visual defect was found. Table S8 starts with one data row on p5 and has a clear repeated title/head on p6. At the end of p17, the S28 moment-gate inline formula continues to p18; the coordinator was notified so the second reviewer can check the join. This reviewer did not open p18.

|Page|Status|Image SHA256|Observation|
|---:|---|---|---|
|1|PASS|`c90d8a97779023f351e6a5516fc47719359bab198dbcaeb8f404f436f4d377e5`|Title, introduction, S1 proof and displayed equation are legible. Margins and page number are clear; no clipping or orphan heading.|
|2|PASS|`498384e46ab2bdbf6a949787880e35d00e4a312db5e1afc5bdc849ba238d604a`|S2 long inequality and proof, S3 and Table S1 fit clearly. Table caption stays with its body; no overlaps.|
|3|PASS|`14dd6af9a6089afe0d837268c7d71eb689b634dd9a1685149be879174ca04e4e`|Dense Tables S2 and S3 retain readable headings and rows. Mathematical notation is clear; paragraph continues normally to p4.|
|4|PASS|`4fc3cc1a07e1c0391852664683d7bfe8b34ea87b371bd141c08c544ed8659a09`|Tables S4 and S5, S7 prose and recursion are complete. Columns align and margins remain clear.|
|5|PASS|`1e51f8c880bc4748b560b84fb34a06243233317d279788fb8e028bc76426c70d`|Tables S6 and S7 are clear. Table S8 starts with one data row before continuing to p6; its heading is not stranded without data.|
|6|PASS|`b555811332af7ad6366481e6eaa4a6c6c371c0e6c85e3f9bd5a12c3d78d85eba`|Table S8 repeats its continuation title and column heads. Long rational fractions fit without touching adjacent columns. S10/S11 and Table S9 start are readable.|
|7|PASS|`fcaeaf40dd2475d2cd45ad2e3cef4fec90a208232b30582c9c4d1f7515f7c3f4`|Table S9 continuation and Table S10 are complete. Long series IDs wrap within their own cells; S13 has following prose.|
|8|PASS|`4c33a1eb8ead7ce607343c51136db91929e31019ddd720524d6ef92b4fa18638`|Table S11, S14 prose and Table S12 start are legible. Continuation at the page bottom is clear, with no clipped rows.|
|9|PASS|`942abf8de138e602a609493aa66565e163284eb0d0c6e5c46e124bb9a22a35de`|Table S12 continuation, Table S13 and S16 prose are clear. Table S14 begins with readable rows and a clear continuation relationship.|
|10|PASS|`0d07e55ae4173e5d1f55ce469e7e3bbb929d1c51087d2673067742e8ba42ad50`|Table S14 continuation and Table S15 are readable, including NA statuses. S18 heading has following prose; nothing extends outside the margins.|
|11|PASS|`04353da5445e1a6caa776ee94f5d649cdd5f9315d94984ba42bbf329fbbff3c3`|Tables S16-S18 are readable, with complete column heads. Long method IDs stay in their columns; no clipping or overlaps.|
|12|PASS|`ed7f3602eee5107131d4c825874c6592a0ae7a4bfee73f628688e8a0616e64e5`|Tables S19-S21 and S20-S22 prose are clear. Math symbols and status fields remain readable; page number is unobstructed.|
|13|PASS|`93c564499051858d8be79d60f6f122e49ef27f4758498058936529758bfd2237`|Tables S22-S23 and S23 implementation conventions are legible. Displayed and inline formulas fit; the bottom paragraph continues normally.|
|14|PASS|`ae590dd7c7f2479e74245a40e8cb05f905baa7f0900d3da6d1660d528483fc88`|Common-pool inequalities, S24 generator and MCSE formulas are complete. Dense prose remains readable, with no text or symbol collisions.|
|15|PASS|`e6e57d7ca954cf965721a21dfcd6116773bd17108e5baadb994354da8876e961`|S25/Table S24 and S26 prose are clear. Penalty and breach columns have separation; the displayed path string stays within the line.|
|16|PASS|`0939a0370b4b184bba408c811ac9f4433fbb807e8a42c9596930196adfc7948e`|Tables S25-S26, displayed bandwidth formula and S27 prose are complete. No horizontal table clipping, blank content or orphan heading.|
|17|PASS|`e4b48e9bd6a79279a69bc7b9522875db523748121288323dfc759486da0f6e7c`|Dense Tables S27-S28 are readable; FAIL/NA and error reasons remain distinct. S28 has following prose. The final moment-gate inline formula continues to p18; coordinator notified for the second reviewer to confirm its continuation. No clipping on p17.|

All 17 image fingerprints match the corresponding supplement rendered_pages entries in final-native-build.json. The companion JSON binds every observation to its individual page image.
