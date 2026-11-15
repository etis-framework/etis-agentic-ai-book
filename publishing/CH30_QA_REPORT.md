# Chapter 30 development QA report

Baseline: exported main state reported at `960b4cb8bdc91360e71fa17305bbdcd72a71cbfe` (Chapter 29 PR #38). Installer independently SHA-256-checks every modified baseline file and checks Git HEAD/branch on author machine.

- Chapter source: 2,861 words at time of final broad inspection (rerun checker for final exact count); V12 cap 3,500, chapter allocation 16 of 550 planned finished pages.
- Figures: F30-01 architecture, F30-02 behavioral sequence, F30-03 deterministic decision; 1000×600 SVG masters, identical rendered SVGs, 1800 px PNGs. Individually visually inspected and the decision crossover corrected; geometry/source/raster gate in `check_ch30_acceptance.py` passed.
- Development proof: standalone Chapter 30 7×10 LibreOffice conversion; 10 pages at 504×720 pt. Page-table split was observed and corrected by `publishing/scripts/build.py` header/repeat and `cantSplit` logic. Full-book native Word for Mac visual/pagination approval **not executed**.
- New operations fixture: 14 tests passed; old Builds 0–5: 16+15+13+18+27+22 = 111; Ch28 recovery 10; Ch29 security 6, giving **141 tests** when all respective suites pass. This is a sum of independent suites, not a proof of a completed uninterrupted `make check` run.
- Dynamic back matter: 30 developed chapters, 61 glossary terms, 50 provisional index entries; alphabetical order and locator parity pass.
- V12: 485 chapter + 65 supporting = 550 allocated; Word-for-Mac final finished-page actuals not certified.
- Static checks: `check_ch30_acceptance.py`, backmatter integrity, single-volume source cap, figure checks and first-reference check passed after corrections. Existing parts citation/integration, companion reader/architecture and page ledger checks were run; the source-page certification and publication proof remain open.
- War-game: see `metadata/ch30-six-lens-war-game.md` for six lenses, book-wide tests, seven corrections, open production gaps and explicit scope limitations.
- **Remaining QA:** user must run uninterrupted native `make check` after guarded installation and inspect final 7×10 Word figures/tables, references and cumulative pagination. Any interrupted or tool-limited run is not represented as a full pass.

## Chapters 1–30 reader-independence integration addendum (2026-11-15)

See `metadata/ch01-ch30-reader-editorial-war-game.md` for the new six-lens review and the distinction between code evidence and production assurance. Chapter 30 now expands E/C names at first substantive use, locates its operational source/tests explicitly, expands local uncommon acronyms, and avoids the internal CAB label in reader prose. Its companion root README gives Chapter 28/29/30 source-to-test routes. Reader-facing Figure 28.1 subtitle was regenerated after the terminology change. Back matter, front matter, bibliography reading guide, glossary/index and future Chapter 31 handoff were updated. Run `publishing/scripts/check_reader_editorial_ch01_ch30.py`, existing acceptance checks, `make book-docx`, and `make check` on the author Mac; native print-size and source-page verification remain author gates.
