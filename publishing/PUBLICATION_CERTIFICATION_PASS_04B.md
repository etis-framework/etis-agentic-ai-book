# Book certification Pass 4B — second independent technical and teaching pass

> **Archived development-pass evidence — not the current publication status.** This dated report records the scope, limitations and decisions of its own engineering pass. Statements such as "not certified," "pending," and "open gate" are preserved as historical findings, not the status of the first-edition companion or the author-approved KDP interior. See [Release Policy](../RELEASE.md) for the current companion release procedure and [Pagination](PAGINATION.md) for print-layout source/approval boundaries.

**Scope:** 36 chapters, seven parts, six Python builds, four supplemental test fixtures, seven internal review lenses, eight selective entry paths, current protocol sources and claim-specific provenance. See `review/pass4b-complete-book-teaching-and-source-audit.md` for the chapter-by-chapter and cross-lens record.

**Change classification:** educational documentation, nonbehavioral source comments, reader Appendix B navigation, bibliography/source-register normalization and automated guide checks. No architecture, figures, model interfaces, financial effect logic, or test behavior changed.

**Acceptance evidence:** `python3 publishing/scripts/check_pass4_teaching_and_sources.py`, `make check`, `make book-docx`, `make check-figures`, and patch preflight. Final source execution: `make check` exit 0 (153/153 ten-suite tests); `make book-docx` exit 0 (99 image references); `make check-figures` exit 0; educational acceptance exit 0; dual-baseline installer applied with exact hashes. These are simulated-source and structural results, not certification of deployment or native Word print proof.

**Disposition:** the manuscript and code remain educational, and the book is **NOT CERTIFIED FOR PRINT**. Open gates: native 7×10 Word proof/page-locator and figure/table review, exhaustive edition/passage-specific source confirmation (including licensed standards), commercial provider/credential/audit controls (not part of educational scope), fixed edition tag and publication metadata/ISBN/cover/spine.
