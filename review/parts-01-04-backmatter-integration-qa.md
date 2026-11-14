# Parts I–IV back-matter integration and six-lens QA — corrective editorial patch

## Scope and baseline

Prepared against the reconstructed post-Chapter-27 professional-perspectives source snapshot, **not** a verified commit SHA from the user's merged `main`. The guarded installer requires exact baseline bytes on a clean dedicated branch. The uploaded Word artifact `etis-agentic-ai-book(20261114-181229).docx` established the initial defects.

## Corrected in the patch

- CAB-001 C01–C09 compact appendix map retains its field/authority semantics with print-safe plain text direction labels. Chapter 8 removes bidirectional pictographic glyphs.
- The document generator marks C01–C09 Word table rows as non-splittable, and keeps the header with its first row. This cannot substitute for actual native Word for Mac visual review.
- E2 logical ownership, E7 storage/persistence and E5 consequential enforcement are explicitly distinguished; E8 provider truth remains authoritative for financial effects.
- Reader appendix covers Builds 0–5, with explicit simulated-versus-real guarantees and the Build 5 limitation of E2-local, not E5 end-to-end, fencing.
- Glossary expanded to 45 alphabetic entries, with no visible editorial placeholder.
- Bibliography no longer freezes coverage at Chapter 22; older acceptance scripts no longer enforce that obsolete phrase. No external claim/page accuracy is newly asserted.
- 33 working subject locators are indexed alphabetically with a JSON term register and aliases; final page-number indexing is deferred until frozen proofs.
- `metadata/backmatter-maintenance-standard.md` specifies the chapter-by-chapter obligation; `check_backmatter_integrity.py` runs in `make check`.

## Six internal review lenses

- **Implementing engineer:** contract names, file paths and build READMEs remain traceable; no executable code modified.
- **Enterprise architect:** E2/E7 ownership and C04 advisory versus RF-1042 identities made explicit without changing CAB-001.
- **Advanced student:** glossary and alphabetic index now support non-linear reading; Chapter 35/36 still marked future.
- **Security and assurance:** signature/fixture identity cannot become business approval; host-UID and end-to-end fencing limits remain visible.
- **SRE/operations:** UNKNOWN means unresolved and status-only reconciliation never creates an additional financial instruction.
- **Business owner:** CASE-204 remains a proposed $500 refund subject to independent approval, evidence and escalation.

## QA evidence and open gates

- Dedicated dynamic back-matter check, first-reference, Chapter 8, C04 identity and conceptual continuity checks: run and observed passing during development.
- The full book DOCX was built with all 74 figure references. Full `make check` was attempted but exceeded the execution window. Other source/test gates should be rerun locally.
- A back-matter-only Word-compatible layout was rendered for an exploratory check; it is **not** a substitute for the actual book's print-pagination or typography.
- **Open:** actual native 7×10 Microsoft Word for Mac pagination and print-scale inspection of contract rows/glyphs, complete bibliography claim-to-primary-passage audit, living-source edition pinning, publisher/author/ISBN metadata, final index page locators, and actual Chapters 28–36.
- V12 locked budget remains 550 planned finished pages (appendix 6, glossary 5, bibliography 10, index 13); actual counts require native print proofs.

## Ongoing maintenance acceptance

Every future chapter patch MUST update back matter as substantively warranted and advance the index/source mappings; no permanent back matter text may assert a stale final chapter count. Existing acceptance scripts must test semantic invariants, not obsolete editorial chronology.
