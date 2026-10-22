# Later long-short-game data: a metadata-only feasibility check

22 October2026. This follows a specific data citation in Al-Baghdadi et al., *Practical investment with the long-short game*, [PMLR128:209–228,2020](https://proceedings.mlr.press/v128/al-baghdadi20a.html). It is a new bounded lead in the existing source investigation, rather than a restart of generic dataset searches. No raw observations, CSV header, source portfolio result or forecast were acquired or evaluated.

## Primary route and actual access

The source's selected physical pp2,7–9 and19 describe a demo-account experiment and point to Al-Baghdadi and Lindsay's [*Aggregating Algorithm Long-Short Game Dataset*](https://www.kaggle.com/datasets/najimal/aggregating-algorithm-longshort-game-dataset). The ordinary web-reader route failed. Three ordinary public Kaggle metadata requests succeeded without credentials or permission changes: exact-reference search, dataset view, and complete file list. The sanitized [machine-readable record](longshort-data-feasibility-check.json) binds the URLs, response-byte hashes, saved times and fields actually inspected. No raw-file request was made.

The API identifies version1, updated11May2020, and labels its license **Unknown**. This does not establish a permissive redistribution grant or prove that analysis is prohibited. The description was empty in the inspected metadata. Empty column arrays supplied no CSV-header confirmation.

| Listed member | Listed member bytes | Conservative screen against current budgets |
|---|---:|---|
| `outcomes.csv` |90,662,779|Over26,214,400bytes|
| `predictions.csv` |2,225,962,855|Over26,214,400bytes and the104,857,600-byte total raw budget|

The complete list contains these two members. Their sum,2,316,625,634bytes, equals the dataset-view total. The search endpoint separately reported472,959,011bytes. The API size-field semantics were not independently verified, so these differing totals are retained explicitly rather than described as identical physical archive sizes or assumed compression measurements. The listed sizes trigger a conservative rejection at this task's budget screen; actual on-wire transfer and expanded raw bytes were not measured. No large download, software installation or partial-data forecast followed.

## Measurement and independence remain separate issues

The source describes100 demo-account clients during September2019–January2020,55 currency pairs, and derived expert positions/returns. That description is not an observation-level authentication of the current public CSVs. It differs from the real-client clustering paper's reported2015–2017 trades and from the accepted2014–2017 aggregate net-position snapshot. Shared authors and data-staging methods do not prove input equality, disjoint originators or independent dealer composition.

The investment construction normalizes each client's asset position vector by its total absolute size to form an expert decision. **If** a supplied file retained only these normalized decisions and returns, absolute position peaks would be unidentified: multiplying a client's positions by a positive constant leaves its normalized decision unchanged while changing its absolute position scale. This is a conditional mathematical observation about that transformation, not a claim that the uninspected `predictions.csv` definitely omits every scale field. Raw schema and any retained absolute units would need separate verification.

A demo-account record could support a separately specified study of those strategies or a carefully qualified illustration. It would not automatically validate real customer flows, actual dealer exposure or operational decision value. Public availability, a later date range and a common word such as *position* are insufficient to establish the compatible unseen-dealer validation missing from this paper.

## Disposition

Do not add this lead as a completed third financial source or replace an adverse result with it. The files are rejected at the conservative listed-size budget screen, reuse permission is unresolved, and neither raw measurement compatibility nor independent real-dealer provenance has been authenticated. A future small legitimate extract would still need its own version, schema, units, aggregation, availability timing and frozen design. No author contact or extract request was sent.

The broader [independent-source audit](independent-source-feasibility.md) remains accurate: a separately compiled Treasury aggregate was evaluated, but compatible independent dealer validation has not been acquired. This follow-up narrows one additional citation-chain lead; it does not establish that no suitable dataset exists elsewhere.
