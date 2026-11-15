# Chapter 36 development QA report

## Verified in authoring environment

- Chapter 36 acceptance: **PASS**, 2,355 regex-counted words; eight sections, three tables, two figures.
- True 7×10 standalone DOCX proof: **8 pages** against V12 allocation of 9; visual eight-page contact sheet checked. This is standalone pagination, not a complete-book proof.
- Figures F36-01/F36-02: source SVG exactly matches rendered SVG; 1600×960 PNG included; both present in chapter and rendered proof.
- All 36 chapters present; no Chapter 36 placeholder; publisher title/subtitle unchanged.
- Chapter first-reference checker: **PASS, 36 chapters, zero reported lexical issues**.
- Reader editorial checker expanded to 36 chapters: **PASS, zero reported errors**.
- Back-matter register: **PASS, 36 developed chapters; 81 glossary terms, 75 indexed entries**.
- Figure reference QA: **PASS, 99 manuscript image references**.
- Full-book DOCX build: **PASS**, generated in development environment; not yet fully printed/inspected.
- Existing Python unittest suites: **153/153 passed**, comprising Build0 16, Build1 15, Build2 13, Build3 18, Build4 27, Build5 22, reliability 10, security 6, operations 14, assurance 12.
- Additional post-timeout editorial/citation/companion checks: individually **PASS**, with their own external/manual warnings retained.

## Execution distinctions

A monolithic `make check` was attempted but hit the execution-time ceiling after reaching `check_deep_wargame_code_contract.py`. Checks after that point were run individually. Do not claim a single uninterrupted full `make check` passed. The exact user-reported merged GitHub `main` SHA was not accessible from this reconstructed source archive; the installer hashes each changed baseline file and refuses mismatch.

## Outstanding final-volume certification

Native Word-for-Mac inspection of the complete bound 7×10 manuscript; full physical page total and V12 variance; source/edition passage verification; comprehensive figure/table/page-break and proofreader pass; final index page locators and fixed release tag; exact Git/CI status; and external production evidence are **open**. Passing educational tests is not production certification.

See `review/ch36-final-chapter-six-lens-war-game.md` for semantic findings, selective reading paths, and residual risks.
