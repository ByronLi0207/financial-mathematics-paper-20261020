# F4.6 — Classical scalar Lévy inequality reference check

Checked 25 October 2026. Scope: Proposition 2 and its proof/source attribution. No manuscript, bibliography, results or Git mutation was made by this subtask.

## Editorial decision

**Use the user's permitted fallback:** remove the Sussman (2023) citation and retain the phrase **“the classical Lévy maximal inequality.”** A standard probability textbook with both the exact consulted edition and a directly verified page containing the required factor-two scalar endpoint inequality was not obtained in this bounded source search. Do not fill a page number from another paper's citation, a search snippet of a secondary paper, or a different inequality bearing Lévy's name.

This is a reference-selection limit, not a claim that the classical result lacks a textbook source. The existing supplement already gives the short first-crossing proof. That proof can remain self-contained and preserves the assumptions and the strict-tail convention at atoms.

## Required inequality and checked local context

The exact required result is

\[
\Pr\!\left(\max_{1\le h\le H}|S_h|>c\right)
\le 2\Pr(|S_H|>c),\qquad c\ge0,
\]

for independent real increments, each symmetric about zero; identical distributions and finite moments are not required. It is followed by the triangle-inequality inclusion for fixed starting position \(x\) and by a population absolute-endpoint quantile at level \(1-\alpha/2\).

Directly read owning text: `submission-v10/manuscript.tex`, Proposition 2 and its display; `submission-v10/supplement.tex`, Section S2, statement, first-crossing proof and conditional/empirical qualifications. The original Sussman entry is a 2023 functional-analysis article, *A strengthened Orlicz–Pettis theorem via Itô–Nisio*, rather than the requested standard probability textbook. This note does not assert that its cited proposition is false; it implements the user's requested change of attribution.

## Primary sources actually inspected

| Candidate | Original source and precise reading | Decision |
|---|---|---|
| Durrett, *Probability: Theory and Examples* | [Author-hosted PDF](https://math.duke.edu/~rtd/PTE/PTE5_011119.pdf). Direct HTTP reading succeeded after the web-open route timed out. Cover states “Version 5 January 11, 2019”; 490 physical pages. Read printed p.84 (physical p.92), Theorem 2.5.5 and its proof, and searched the extracted text for maximal-inequality locators. [Author's Duke publication record](https://scholars.duke.edu/publication/1632506) identifies the formal 2019 fifth edition. | The verified p.84 result is **Kolmogorov's variance bound**, with zero means and finite variances. It is not the required factor-two endpoint tail inequality. Do not cite this page for Proposition 2, and do not equate the author manuscript's pagination with the published edition. |
| Varadhan, independent-sums chapter | [Author-hosted original chapter PDF](https://math.nyu.edu/~varadhan/course/PROB.ch3.pdf). Read printed pp.61–63 (physical pp.11–13), specifically Lemma 3.8 and proof at pp.62–63. It bounds the maximum by \(\delta/(1-\delta)\) under uniform suffix-tail bounds at half the threshold. [AMS original book endmatter](https://www.ams.org/books/cln/007/cln007-endmatter.pdf) identifies *Probability Theory*, Courant Lecture Notes 7, copyright 2001, reprinted with corrections in 2012. | The accessible author chapter uses a different formulation and pagination; the precise relation to a particular printed edition's page was not verified. Do not cite its p.62 as the published-book page or silently substitute this lemma for the exact scalar symmetric inequality. |
| Gut, *Probability: A Graduate Course*, second edition | [Publisher's book record](https://link.springer.com/book/10.1007/978-1-4614-4708-5) directly verifies author, edition 2, copyright 2013 and DOI. The [publisher's Inequalities chapter](https://link.springer.com/chapter/10.1007/978-1-4614-4708-5_3) verifies chapter pp.119–155 but exposes only an abstract/subscription preview. The chapter PDF route did not provide the body. | Exact theorem page and text not directly read. This is a promising locator, but it is **not an accepted citation** for this revision. No theorem/page is inferred from citations in other papers. |
| Ledoux and Talagrand, *Probability in Banach Spaces* | [Author's books page](https://perso.math.univ-toulouse.fr/ledoux/books/) identifies 1991 publication, 2002 second printing and 2011 Classics printing. The original Springer chapter-PDF route `https://link.springer.com/content/pdf/10.1007/978-3-642-20212-4_2.pdf` did not provide a readable body. | No verified original theorem passage/page. Do not introduce the book as though the theorem had been checked. |

Search results from secondary papers, commercial mirrors, encyclopedias, solution repositories and forums were not used as theorem evidence. No unverified textbook citation is proposed.

## Concrete proposed main-text wording

Four sentences, followed by the unchanged mathematical bound:

> Let future real increments be independent and individually symmetric about zero, with partial sums \(S_h\). Fix a starting position \(x\), set \(B=|x|\), and let \(q\) be the population \((1-\alpha/2)\) quantile of \(|S_H|\). The triangle inequality and the classical Lévy maximal inequality imply the bound below. A conditional application requires these assumptions and the endpoint quantile under the law given issue-time information.

\[
\Pr\!\left(\max_{0\le h\le H}|x+S_h|>B+q\right)
\le\Pr\!\left(\max_h|S_h|>q\right)
\le2\Pr(|S_H|>q)\le\alpha.
\]

Keep the proof, lack of identical-law/moment requirements, strict events at atoms and empirical plug-in qualifications in the supplement. The excerpt does not add any empirical calibration claim.

For Proposition 1 the manuscript owner can use three sentences before the existing display:

> Suppose \(Y\ge B\) almost surely and the issue information contains \(B\). Projecting any forecast \(c\) to \(\max\{B,c\}\) weakly improves pinball loss for every outcome, with the gain shown below. The true conditional lower inverse quantile has strict exceedance probability at most \(\alpha\), including at atoms.

This keeps the floor and quantile claims intact; their derivation and discussion stay in Section S1.

## Application instructions for the manuscript owner

1. Remove `\citep{sussman2023}` from the main proposition. In supplementary Section S2 remove the phrase “see Sussman (2023), Proposition 3.4”; keep the classical attribution and first-crossing proof.
2. Remove the Sussman displayed reference if no remaining main/supplement citation uses it; synchronize any active bibliography source so it is not restored during a later rebuild.
3. Keep Proposition 2's independence and individual symmetry assumptions, the population endpoint quantile, the factor two, strict-tail convention and conditional-law caveat. Do not replace them with the finite-variance or suffix-tail premises of the rejected candidates.
4. After relocating proof/discussion, verify that the main propositions contain only the short statements and equations and that Supplement S1–S2 remain correctly referenced.

Only the two `notes/v12/` literature files are authored by this subtask. No financial data were downloaded, and no Claude/cross-model review was used.
