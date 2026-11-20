# Publication certification — Pass 3: editorial navigation and author credibility

> **Archived development-pass evidence — not the current publication status.** This dated report records the scope, limitations and decisions of its own engineering pass. Statements such as "not certified," "pending," and "open gate" are preserved as historical findings, not the status of the first-edition companion or the author-approved KDP interior. See [Release Policy](../RELEASE.md) for the current companion release procedure and [Pagination](PAGINATION.md) for print-layout source/approval boundaries.

## Scope and disposition

This pass strengthens the published author biography, materially improves subject indexing, and corrects print page-reference extraction. **It is an editorial/navigation correction pass, not final publication certification.** The user-provided November 15 Word build is the print-layout comparison baseline; exact merged `main` commit verification remains the guarded installer's responsibility.

## Corrections

1. About the Author is grounded in the current CV: two IBM CTO appointments, IBM Distinguished Engineer, database/parallel systems work at AT&T Bell Laboratories and NCR/Teradata, peer-reviewed SIGMOD/VLDB/ICDE contributions, 11 U.S. patents, IIT Ph.D., Loyola/Princeton/Toronto teaching, ETIS publications and governed educational review tooling. It explains how that background informs independent evidence and accountable systems rather than listing a résumé. No personal contact information is included.
2. The index register and Markdown are synchronized at **154 professional entries**, up from 109. Forty-five new reader-oriented lookup paths cover high-value practice questions (authority/identity, real versus simulated guarantees, uncertain provider effects, stale epochs, negative testing, review/governance, operations and economics). The new `PAGEREF` fields remain tied to chapter and section anchors; no static page numbers are committed to source.
3. Page-locator caching now reads the geometrically placed **footer folio** from the proof PDF instead of searching the first five extracted text lines, which can mistakenly return a body number. A strict resolver must map all references; missing folios block release. Word fields remain live; their visible caches must be refreshed after final Word-for-Mac pagination.
4. Added `check_publication_certification_pass_03.py` and `make check-publication-pass03` to enforce author credentials, alphabetical nonduplicate professional index, source locators and live Word references.
5. Removed the redundant website-only orphan from the end of the author page; the ETIS website is already present on the opening pages.

## Evidence in this development environment

- Word source build: passed; 36 chapters, 51 contents entries, **154 index entries**, 359 bookmarks, 300 Word `PAGEREF` fields.
- Strict cache-fill against preliminary 7×10 LibreOffice proof: 300/300 fields mapped; examples `Preface iii`, `Chapter 1 1`, `About the Author 447`.
- Publication Pass 02 and Pass 03, dynamic back-matter integrity, and figure-reference build checks passed after correction.
- Preliminary LibreOffice print proof: **453 physical pages**, and About the Author occupies the final page rather than leaving a one-line page. This is *not* the same layout result as the user's November 15 supplied Word document, whose extracted rendering reports **575 pages**. The 122-page divergence is a BLOCKING page-engine / version / layout reconciliation question, **not** evidence that the book shrank by 122 pages.
- The full `make check` advanced through static/editorial/companion-documentation gates and completed Builds 0–3 (62 tests) before being interrupted during Build 4 by the execution time limit. A full sequential pass is NOT established. Previous chapter certification logs cannot substitute for this final run.

## Six-lens and selective-path review — scoped observations, not an end-to-end certification

- **Implementing engineer:** new index paths lead to source/test crosswalk and actual companion build locations; document/build promises must be tested against source modules in the next code audit.
- **Enterprise architect:** designs A/B/C and E1–E9 remain navigable; logical controls must not be mistaken for physical isolation or production authorization.
- **Advanced student (internal QA only):** new topic aliases improve nonsequential learning; the persona itself is not a reader-facing authority.
- **Security/assurance:** explicit lookup paths for token-validity-versus-authority, forged approvals, tool abuse, and denial tests; no inference of production security certification.
- **SRE/operations:** stronger paths for unknown outcomes, stale leases, quarantine, recovery, and rollback-versus-reconciliation.
- **Business owner:** clearer entry points for cost per acceptable outcome, human staffing, stop decisions, risk and retirement.
- **Selective paths:** architecture, build, security, reliability, governance, economics, teaching, and CASE-204 traces received targeted navigation checks; a fresh complete independent reading of every chapter was not performed in this pass.

## Mandatory outstanding release gates (tracked, not waived)

1. Reconcile the **575-page native Word/upload observation vs 453-page LibreOffice reflow**, confirm 7×10 geometry, parity/blank pages, typography and the actual print page budget (V12 target 550, preferred 575; planning maximum 600; absolute 700). All TOC/index locators must be finalized against that exact edition proof.
2. Native Word-for-Mac whole-book refresh and print PDF: full section/figure/table walk including caption placement, repeated table headers, front Roman and body Arabic numbering, no orphaned author heading or trailing blank pages, and final contents/index locators.
3. Six-lens independent end-to-end manuscript war-game and eight selective entry paths, with severity/evidence/closure and unresolved risks.
4. Claim-by-claim bibliography and source-register verification (specific source, edition, page/section, date, permissions and attribution); remove any text that refers to private editorial verification instead of reader resources.
5. Complete Builds 0–5 execution, each README source diagram, security/operations/reliability/assurance fixtures and full 153-test regression on exact merged `main`. Check manuscript↔code claims and simulation-versus-production limitations both ways.
6. ISBNs and copyright permissions, cover/back/spine, print specifications, retailer description, edition/versioned Git tag, errata and release records.

No automated or simulated fixture is a substitute for production-system certification.
