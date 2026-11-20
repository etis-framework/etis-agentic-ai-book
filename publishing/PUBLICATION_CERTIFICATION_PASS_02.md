# Publication certification pass 02 — front matter, print navigation and six-lens QA

> **Archived development-pass evidence — not the current publication status.** This dated report records the scope, limitations and decisions of its own engineering pass. Statements such as "not certified," "pending," and "open gate" are preserved as historical findings, not the status of the first-edition companion or the author-approved KDP interior. See [Release Policy](../RELEASE.md) for the current companion release procedure and [Pagination](PAGINATION.md) for print-layout source/approval boundaries.

## Changes made

- Matched the ETIS Professional Computing Series 2026 reference book's half-title, series/title hierarchy and bottom imprints, with an explicit production-stable series/title footer treatment.
- Removed digital-edition claims from the copyright and reader-facing companion discussion; unassigned print ISBNs remain visibly pending.
- Rewrote About the Author from the supplied current November 2026 CV and ETIS author page, emphasizing both senior IBM technical authority and the ETIS engineering perspective without listing private contact details.
- Increased contents child-entry font to 9 pt, main entries to 10 pt, and subject-index terms to 9 pt. Kept live `PAGEREF` anchors, filled the 255 cached page displays from the physical PDF, and forced About the Author onto its own page.
- Corrected obsolete current-status statements in internal traceability documentation, while leaving clearly labeled older review snapshots as historical evidence.
- Corrected a Chapter 29 sentence that inadvertently blurred the distinction between logical and physical enforcement zones.

## Measured QA and limitations

- **36 chapters**, **7 parts**, **99 manuscript figure references**, **109 subject-index terms**, **51 contents entries**, and **359 anchor bookmarks**.
- **452 physical pages** in one preliminary 7×10 LibreOffice proof. The number is descriptive, not a certified Word-for-Mac final count; V12's 550 total remains a target, not an attained count.
- **255 of 255 page-reference caches resolved** against the physical proof; the delivered Word review has readable page numbers, not dash placeholders. They are still Word fields and must be updated after any edition-specific reflow.
- **76 previously completed static/QA/script commands passed** in a parallel component run, with one pass-01 checker initially failing because the half-title is now intentionally two lines. The checker was corrected and reran green. The separately rerun Build 3 suite passed **18 tests**. Across the earlier full suite and component runs, all **10** companion suites passed; final release should rerun sequential `make check` on the publisher's Mac.
- `check_publication_certification_pass_02.py` and the pass-01 checker both pass after the corrections. First-reference audit reports 36 chapters and zero issues; back-matter coverage reports 76 glossary entries and 109 index terms.
- A structured six-lens and eight-selective-path review, plus a scoped external citation sample, is retained in `review/final-book-six-lens-publication-audit-02.md`. This is **not** six complete human line-by-line readings or a claim-level primary-source certification.

## Release blockers

1. Native Word-for-Mac 7×10 proof, including Roman preliminaries, final TOC/index page locators, tables/figures and physical page parity.
2. Exhaustive page/edition/section-specific reference and third-party permissions review; the existing source register documents outstanding checks.
3. Print ISBNs, publishing rights approvals, cover and spine dimensions, and final retailer metadata.
4. A complete sequential `make check` on the exact merged source and preservation of the output as a release evidence artifact.

This patch **does not certify** the simulated companion implementation for production financial work.
