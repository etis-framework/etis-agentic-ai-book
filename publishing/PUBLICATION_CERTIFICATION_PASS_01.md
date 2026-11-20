# Engineering Agentic AI Systems — Publication certification pass 01

> **Archived development-pass evidence — not the current publication status.** This dated report records the scope, limitations and decisions of its own engineering pass. Statements such as "not certified," "pending," and "open gate" are preserved as historical findings, not the status of the first-edition companion or the author-approved KDP interior. See [Release Policy](../RELEASE.md) for the current companion release procedure and [Pagination](PAGINATION.md) for print-layout source/approval boundaries.

**Disposition: development publication revision ready for author/native-Word inspection; NOT final publication certified.**

## Scope and source precedence

The author biography was written from the supplied 2026 William T. O’Connell CV (authoritative for dates, roles, degrees and 11 patents), checked against the ETIS About the Author page. The *From Data Structures to Engineering Judgment* First Edition print sample establishes the opening sequence: half-title; ETIS Professional Computing Series statement; title/subtitle/byline; copyright; contents. It is a design precedent, not a source for current ISBNs.

## What this pass changes

- Complete author byline and concise substantive About the Author, emphasizing research, engineering, IBM Distinguished Engineer appointment, two CTO roles, Loyola, Princeton/Toronto teaching, 11 patents, and ETIS authorship. Personal contact details are deliberately omitted.
- Dedicated half-title, series statement, and formal title page. The approved title/subtitle remain unchanged.
- Print-navigation script generates a detailed contents page with **live Word page references**, not manually inserted guessed numbers. It adds a live page-index reference for each cataloged subject term; index entries remain alphabetized and source-registered.
- Subject index expanded from 75 to **109** grounded topics. Four internal review-role glossary entries and one reader-facing internal-role entry were removed. Index and TOC page locators must be refreshed in the final native Word proof.
- Publication metadata updated for author, 2026 first edition and ETIS Framework imprint; **ISBNs intentionally remain unassigned**.
- Legacy QA scripts are updated to check the completed 36-chapter status rather than an intermediate chapter-development text string.

## Measured proof and qualifications

- One full-volume LibreOffice rendition measured **451 physical 7×10 pages**, including preliminaries and back matter, below the 550-page V12 target and 700-page absolute limit. This is an indicative Linux rendering, *not* Word-for-Mac final pagination. Page numbers may shift when fields and print fonts are refreshed.
- The regenerated DOCX contains 36 chapter headings, 51 contents entries and 109 indexed terms with live Word page references. A later fix repaired the index heading bookmark discovered in the initial PDF; final native print proof must establish that all references resolve in the exported PDF.
- Publishing-identity, index/backmatter, author/front-matter, chapter-first-reference, reader-editorial, the Part IV capstone, and Chapters 1–36 acceptance checks reached their respective passing checks in the staged run. The combined `make check` did **not** complete uninterrupted within the execution environment; companion suites must be rerun on the exact merged main branch.
- **No claim** is made that the educational mock payment, ownership epochs, external authorization service, provider settlement, credential vault, immutable audit, or real incident controls are production certified.

## Outstanding final-release gates

1. Assign ISBNs and approve the legal notices, rights and permissions; approve optional dedication and acknowledgments separately.
2. Run `make book-docx`, open in Word for Mac, select all, update fields, save, export print PDF, and verify *all* page references and 7×10 geometry. Check Roman/Arabic preliminary numbering, even/odd blank pages and gutter.
3. Inspect 99 figures, all lengthy tables, code listings and captions in the **complete** print PDF at actual trim size. A programmatic page-count test is not visual signoff.
4. Validate the final source register and bibliography against cited primary-source editions and effective dates; independently verify live standards and high-impact assertions.
5. Run one full `make check` plus `make check-figures` on verified merged main and archive the exact command output and commit SHA.
6. Perform six-lens final reading and selective-path QA on the actual bound-volume proof, including CASE-204/RF-1042, independent authorization and all six build READMEs.
7. Finalize cover, spine, retail copy, title-page copyright/imprint, and author approvals only after locked final page count.

## Reproduction

```bash
make book-docx
python3 publishing/scripts/check_publication_certification_pass.py
make check
make check-figures
```

Word: **Cmd+A → update fields** (or select all and use the appropriate update-field action in Word for Mac); save and export a PDF. If fields do not refresh in a particular Word build, update each section's page-reference fields and rerun the page-reference audit. A PDF with `Error: Reference source not found` or unresolved dashes is **not** publishable.
