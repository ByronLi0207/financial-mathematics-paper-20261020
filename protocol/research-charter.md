# Research charter — 20 October 2026

## Requested outcome

An English working paper, reproducible small-scale analysis, and clear documentation in a new repository owned by ByronLi0207. The subject is financial engineering / financial mathematics, with room for economics and finance. The owner specifically asks for extensive reading before design, and for careful adaptation of an established method to a different problem rather than unsupported commentary.

## Schedule

All local times are America/Vancouver (PDT, UTC−07:00).

| Stage | Earliest scheduled time | Required work |
|---|---|---|
| Literature | 20 Oct 00:28:56–06:28:56 | Read and compare recent primary papers and foundations; verify assumptions, closest work, and data access. |
| Design | 20 Oct 06:28:56–08:28:56 | About two hours of research design after actual reading is sufficient; lock the question and analysis choices. |
| Analysis and writing | After 20 Oct 08:28:56 | Small, measured computations, appropriate checks, manuscript and replication package. |
| 24-hour checkpoint | 21 Oct 00:28:56 | Audit actual time and deliverables; report completion or explicit remaining gaps. |

This is a schedule, not a record of hours worked. Active work, agent work, parallel overlap and scheduler gaps must be accounted for separately. No timer substitutes for reading. If interruptions prevent the requested reading/design durations, record that honestly and do not skip the requirements to meet the checkpoint.

## Initial search lanes

1. Distributionally robust optimization, optimal transport and risk measures.
2. Dependent-data calibration, conformal risk forecasts, VaR/ES evaluation and sequential backtesting.
3. Public data provenance, computational feasibility, and reproducibility practice.

These are search lanes, not a chosen research topic. Literature screening should cover a broad candidate set, with a smaller set read deeply. Counts are evidence of coverage, not quotas to be filled with irrelevant papers.

## Candidate acceptance criteria

- Financial question and decision/estimand are explicit.
- The source method, its assumptions and guarantees are stated correctly.
- Nearest papers do not already answer the same question; any incremental contribution is described at its actual scale.
- A legitimate, reproducible small data source is available.
- The design can fail: a weak, null or adverse result is publishable within this working-paper project.
- Baselines, chronological evaluation, relevant dependence treatment, cost or calibration metrics, and sensitivity checks are fixed before holdout evaluation.
- The experiment fits a one-process, CPU-only budget and can be reproduced without paid services.

## Working-paper standard

Use a precise title and question, abstract based on observed results, introduction and contribution, related work, problem and assumptions, method, data and evaluation, results, limitations, conclusion, references and supporting replication instructions. This is a target structure; it does not imply that a manuscript exists or a venue will accept it.

Reproducibility practice is informed by the [AEA Data and Code Availability Policy](https://www.aeaweb.org/journals/data/data-code-policy), verified 20 October 2026, especially data provenance, computational code, README requirements and output mapping. This repository is not an AEA submission or a claim of compliance certification.

## Repository publication

Create `ByronLi0207/financial-mathematics-paper-20261020` as an independent working repository. Incrementally publish original notes, protocol, code and manuscript; do not publish third-party PDFs, private information, speculative results or unsupported claims. The broad repository name avoids committing to a topic before the reading stage.
