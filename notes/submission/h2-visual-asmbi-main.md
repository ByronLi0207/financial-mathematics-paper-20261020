# H2 ASMBI manuscript: direct page-by-page visual inspection

Overall verdict: **VISUAL_PASS_WITH_EDITORIAL_FINDINGS**. All 25 pages were directly viewed. No clipping, occlusion, missing math glyph or unreadable numeric column was observed. Known author-input placeholders and bibliography punctuation remain as findings below.

- PDF: `submission-package/ASMBI/manuscript.pdf`.
- PDF SHA-256: `385f69b90557e975586df35f6bf7c220518a63cf0b098c502f928ce18ac25166`; matches the H2 manifest.
- All 25 PNG SHA-256 values match the manifest.
- Actual product inspected: Free Format + AMA. This is not a claim that the original NJD template was reproduced unchanged.
- Every individual page image was returned by `tools.view_image`; page 19 was re-viewed with original detail. No contact sheet or extracted text substituted for viewing.
- Only this Markdown and companion JSON were written. Source, PDF, frozen numbers and results were not changed. No commit or subagent was created.

## Findings

| ID | Pages and location | Observation | Recommendation to parent |
|---|---|---|---|
| E01 | p1 below title; p15 author-input block | p1: `[AUTHOR INFORMATION TO BE COMPLETED]`; p15: `[TO BE COMPLETED BY AUTHOR]` for author information, ORCID, funding, competing interests. | Known author-input boundary; obtain actual values before submission. This is not a rendering defect. |
| E02 | p15 ref [4]; p16 refs [18]-[21] and [25] | [4]: `Delft University of Technology. : 2017.`; institutional-author space before period; [21]: `Historical compressed. : . Retrieved October 24, 2026.`; [25]: `Walter Vaughn J. ., eds.` | Clean bibliography-output punctuation without changing scientific numbers or adding unverified bibliographic facts. |

## Focus checks

- Numeric superscript citations are legible. References [1]-[31] are complete. This is a visual/format inspection, not a bibliographic fact audit or a complete journal-compliance audit.
- References end on p17. Tables 1-8 occur one per independent page on p18-25. Numeric columns, signs, percent signs, NA entries and notes are readable. Table 2 is smaller than body type but remains legible.
- Figures 1-6 preserve complete axes, legends, units and captions.
- WP2 on p7 remains one complete paragraph. The final `Supplement Section S39` reference is clear. The supplement-target content was outside this assigned task.

## Page evidence

| PDF page | Directly viewed | Image SHA-256 | Observation and verdict |
|---|---|---|---|
|1|Yes, complete page|`aa7d69090e284dd2e904fc453dedaf4dc78744f43fc52ccdbe207ff780859f73`|Title, abstract, keywords and RQ1-RQ3 are complete and legible. No clipping or overlap. Visible author placeholder below title: [AUTHOR INFORMATION TO BE COMPLETED]; see E01. **PASS_WITH_EDITORIAL_FINDING**|
|2|Yes, complete page|`6e9eb96c580520d28131360ba8d199d30954a3823e7bdcc3ed0029603d236252`|Figure 1 axis labels, USD millions unit, dates, line legend and caption are clear. Body and numeric superscript citations are legible with no clipping. **PASS**|
|3|Yes, complete page|`29ea54019ea4813271bd21ae2537e2d0dfca9fc3b046df76e676e17bdd85b7d6`|Related-literature numeric superscripts are legible. Target definitions, pinball loss, propositions and bottom probability formula are complete and unobscured. **PASS**|
|4|Yes, complete page|`c97ba69eee4f547f901c9498fd5f8115e2fa415a32992c210bfa514174353485`|Data and Forecasting methods text, superscript citations, H and tau symbols are complete. No clipping or broken section transition. **PASS**|
|5|Yes, complete page|`075cd2eed976aa9659437443e0edb5f5c8f79885a456fb073589a44fe467b04b`|Historical-rule and ridge-quantile formulas are legible. Wide regression formula stays within the page. Citations and section transition are complete. **PASS**|
|6|Yes, complete page|`d1144e89d2fda142eb977543424a3cae964536e178fd291be2b977b7c4a20e6e`|DM and HAC bandwidth formulas, Sections 6.1-6.2 and 7.1 are complete. Subscripts and superscripts are clear, with no clipping. **PASS**|
|7|Yes, complete page|`ca546f8b529122c3d1c28d525ea22fdc6a9309c84eba595900c789bee18c5d1e`|Figure 2 training-history axis, percentage loss axis and two-method legend are clear. The WP2 paragraph headed A fixed CFTC history-length extension is one continuous complete paragraph; its final Supplement Section S39 citation is legible. Counts, partial-support verdict and limitations remain visible. **PASS**|
|8|Yes, complete page|`e5969f146884a35c54270b54efebd767fff85411c5ff29ee7887e3de55291d80`|Sections 7.3, 7.3.1 and 7.3.2 and references to Tables 5/6, Figure 3 and Supplement Table S49 are legible. Bottom whitespace precedes a separate figure page; no clipped continuation. **PASS**|
|9|Yes, complete page|`467f072f431f6c4c3a1fc9220bdd466814e6e0bede686a81b53325d54c6b1bc8`|Figure 3 occupies a separate page. All 17 contract codes, 52/260-week panel titles, Relative loss change (%) axis, zero lines, unit caveats and caption are legible. **PASS**|
|10|Yes, complete page|`6759e30eb53f7b0b3b64d52b2d977f7cc467274cf6c9232ff691ac65f1cf0f9b`|Section 7.4 and Figure 4 panels are complete. Color/hatch/dot/cross legend, planned comparison index and percentage vertical axis are clear; caption and following text do not overlap. **PASS**|
|11|Yes, complete page|`9debc8cc2c44ff1fcfd50974af114276657b16811ffc3319589219d1ae3131b2`|Section 7.5 and Section 8 cost formula are legible, including math accents and indices. References to S47, S32, Figure 5 and Table 8 are visible. Formula stays inside page. **PASS**|
|12|Yes, complete page|`fc00b9ba4df9a5555d6bfe2ac86f82afed12031ded72e86d52a54d47c9d5581c`|Figure 5 six-panel page is complete. Kappa/beta axes, complete counts, 0-1 color bar and caption caveats are legible. No clipping or occlusion. **PASS**|
|13|Yes, complete page|`728aa290ec614b7acb5df8c770ee40b1bd9b60e554fde6c6b2ab3d999920236b`|Sections 9.1-9.2 and Figure 6 three panels are legible. Independent vertical scales are visible and explained in the caption. Body text and superscript citation are unobscured. **PASS**|
|14|Yes, complete page|`8c2bbaafae6a5b59561a31175d7e4bcfb6d676664cc134eb130824652be6cb37`|Limitations, Conclusion and start of Data and code availability are complete. Long Kaggle URL wraps within page; no clipping. **PASS**|
|15|Yes, complete page|`f5c95966664522966c36b635d79a52f130ea32653200b3282387d65451534219`|Data/code availability, author-input block and References [1]-[8] are complete. Four author-input placeholders remain (E01). Reference [4] has malformed punctuation . : 2017. (E02). **PASS_WITH_EDITORIAL_FINDING**|
|16|Yes, complete page|`0bcd96adc5b3bf435d8668d3a798ad12ab6e0217c6f8dd1fec6e5c33bbc681cf`|References [9]-[25], DOI strings and wrapped titles are legible and unclipped. Institutional-author space-before-period artifacts, reference [21] . : . and reference [25] J. ., are recorded in E02. **PASS_WITH_EDITORIAL_FINDING**|
|17|Yes, complete page|`914690966a9e4d7bd1c65f28b0c44872f27af1e7d2f7d7440d77d0a6887996fb`|References [26]-[31] are complete and legible, with intact numbering, book title and DOIs. References end on this page; bottom whitespace is intentional. **PASS**|
|18|Yes, complete page|`d60a63a09c23555c10793fc05195b389af697e543a98b60233f9c94c58040ea0`|Table 1 is on its own page after references. Study, Response, Data unit and Evaluation columns are complete, readable and within page. **PASS**|
|19|Yes, complete page|`8c228b52a5333e7cd5330ea828de534a4f77244e76d4fd25c10e1409ef47b0ee`|Table 2 is on its own page. Panels A/B, date columns, USD mn/Contracts, mean/SD/95th columns and notes are complete. Table type is visibly smaller than body type but numeric columns remain readable. Re-viewed with original detail; no overlap or clipping. **PASS**|
|20|Yes, complete page|`d310907ba89ebb68a7fee49a5c2470714a6dd947b5b856ef3fb45901abc327ac`|Table 3 is on its own page. Method/definition/executed-menu columns, six-point lambda menu and notes are complete and readable. **PASS**|
|21|Yes, complete page|`3a9d8c8212423beba06a1d81d7a7b4ac4172815bca3d57c764b44c21114d43c5`|Table 4 is on its own page. Loss change (%), Issues and Strict breaches numeric columns and comparison labels are readable. Multiline cells and notes do not collide. **PASS**|
|22|Yes, complete page|`3ff9a8f0a599da2085d96411d24e5960fd141a2c3b32d501bf2fc0b899f8622e`|Table 5 is on its own page. Procedure, percentage and higher-loss-cell columns and notes are complete and readable. **PASS**|
|23|Yes, complete page|`013cf064ee50f18dc4dcd3ae45947c098085057357c3df384512141f4f993fdd`|Table 6 is on its own page. All 17 contract rows and both five-column History 52/260 groups are readable, including signed numbers. Rightmost Calibrated regression column and full notes remain within page. **PASS**|
|24|Yes, complete page|`9eab361c08085aac48a9f12759cad6ae8b5cdd6c09c27619dd08414def0f7558`|Table 7 is on its own page. Validation 52/156 percentages, Limit selections and Horizon/History/Series headers are readable and notes are intact. **PASS**|
|25|Yes, complete page|`fd41be1089fb98f3f362758061a4ba5a71bd5903dde33aaa28288bf7399f876b`|Table 8 is on its own page. 90%/99% columns, signs and NA failed entries are intact. Notes preserve rejected post-failure repair and Supplement Section S38 reference. No clipping. **PASS**|

## Evidence boundary

This conclusion binds only to the PDF and 25 PNG SHA-256 values recorded above. Findings are for the parent workflow; this inspection did not repair any file. Any updated PDF/image version needs its own evidence and visual inspection.
