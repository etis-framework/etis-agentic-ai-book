# Chapter 32 production QA status — 2026-11-15

**Development base:** supplied Git baseline `b5a5ef94c4db5963f5da75f047f6ed9f4dece107` (text record from clean `main`; no `.git` in source tar). The installer checks the local Git object and file-level SHA-256 before writing.

**Files:** Part VI introduction, Chapter 32, F32-01/02/03 source+rendered graphics, Part VI/back-matter navigation, register and glossary maintenance, source/figure traceability, Chapter 32 acceptance and scoped existing QA logic updates.

**Ch32 source:** 2,981 regex lexer words ≤ 3,000 cap. V12 planning stays 13 finished Chapter 32 pages, 38 Part VI pages, 550 planned total. Container standalone DOCX rendered 10 pages; native Mac full-volume pagination unverified. Three 1000×600 SVG masters and high-resolution PNG renders inspected; native Word figure print-size review open.

**Tests:** Existing Build 0–5: 111 total; reliability 10; security 6; operations 14; assurance 12 = **153 tests**, each suite passed in separate invocations. No effectful governance code added. `check_ch32_acceptance.py`, first-reference/editorial, back-matter, publishing identity, figure, source and V12 checks passed. The monolithic `make check` was interrupted by a tool timeout, not represented as completed green. The installation procedure requires the recipient to run it end-to-end.

**War-game:** See `review/ch32-six-lens-and-book-wide-war-game.md`; six perspectives, architectural continuity, negative cases and open evidence obligations. Production trust, source page certification and native Mac print signoff remain open.
