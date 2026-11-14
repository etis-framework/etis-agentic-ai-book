# Back-matter maintenance and publication QA standard

**Every chapter addition or revision must assess the appendix, controlled glossary, bibliography, source register, index term register, working index, front matter, part openings, tables and cross-chapter navigation in the same patch.** The content should reflect all developed chapters without hard-coded “current chapter” coverage prose. Where a future chapter remains a stub, distinguish planned guidance from completed specifications.

## Required work with each chapter

1. Add or refine glossary terms if the chapter establishes or changes definitions; maintain alphabetical order and keep contrastive terms precise. Definitions must not imply stronger isolation, approval or provider guarantees than demonstrated.
2. Assess the C01–C09 appendix contract map and build notes for newly introduced responsibilities; keep E2 coordination ownership distinct from E7 persistence and E8 business truth. Use plain-print directional labels, not symbol/emoji arrows.
3. Update bibliography and `references/source-register.md` for new sources or refined claims; retain source-to-claim verification queues. Reference identity or a URL is **not** evidence that a precise claim has been verified against the source passage.
4. Update `metadata/index-term-register.json`, then the provisional working index, using canonical terms, aliases/see-also and chapter/section locators. Do not generate final page-number locators until print proofs and the text are frozen. Planned chapters get no fabricated locators.
5. Check front/part introductions, contents/status statements, source registers, glossary and back matter for stale “will”/“planned” statements; update when the chapter is actually developed.
6. Run `python3 publishing/scripts/check_backmatter_integrity.py`, `make check`, and `make book-docx`; inspect tables, print arrows and page breaks at 7×10 in Word. Preserve locked V12 budgets: appendix 6, glossary 5, bibliography 10, index 13 pages (targets, not authority to pad).

**Source of truth:** canonical CAB-001 architecture and actual example code/tests; glossary and index are reader aids. No fixed draft cutoff such as “through Chapter 27” belongs in permanent bibliography or glossary prose. Book-status registers may record current chapter completion and must advance with development.
