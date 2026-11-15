# Chapter 34 QA receipt — development environment

- Baseline: reconstructed Chapter 33 guarded patch source, representing Chapter 32 editorial-corrected repository; live `main` SHA is **not verified** in this environment. The guarded installer checks per-file SHA-256 against the user's actual merged branch.
- Chapter: 34, *Economics, Risk, and Lifecycle Decisions*; 2,666 regex source words; V12 allocation 12 finished pages.
- Rendered chapter: 7×10-inch standalone Word review, **10 pages**, including four tables and all three F34 figures. A standalone render does not measure final integrated Word-for-Mac pagination.
- Figure masters: F34-01/02/03 1000×600 SVG master matches rendered SVG, PNG raster 2000×1200. Visually inspected for arrows, text, readability, printed width and captions; user must perform native Word proof.
- Economic arithmetic: A→B 15,000/600 = $25; B→C 24,525/150 = $163.50. All prices, counts and business values intentionally hypothetical.
- Corpus QA: first-reference 34 chapters; release governance no developer-status leakage; 34 chapter reader editorial pass; appendix A/B/C publication and register synchronized; exact 11 companion source paths verified.
- Python suites: 153/153 passed (Builds 0–5, reliability, security, operations, assurance). `make book-docx` passed with 95 included image references. Slow editorial and companion checks individually passed; combined uninterrupted `make check` terminated by execution time limit, not claimed green.
- Open gates: native Mac Word print and full integrated page count; actual Git merged-`main` baseline hash; live economics evidence and real provider/authorization/audit/canary controls; exact external citation passages and editions.
- Detailed adversarial review: `review/ch34-six-lens-and-book-wide-war-game.md`.
