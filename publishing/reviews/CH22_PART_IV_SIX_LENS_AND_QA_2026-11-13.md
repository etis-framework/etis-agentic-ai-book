# Chapter 22 / Part IV integration — engineering review (2026-11-13)

**Decision: development patch prepared; NOT publication-certified.** The Part IV introduction, Chapter 22, executable Build 0, and F22-01/02 are new. CAB-001 and BP-001 remain unchanged. V12 chapter 22 allocation is **14 finished pages**; Part IV allocation **85** and single-volume target **550** remain unchanged.

## Six-lens war game (front matter → Parts I–III → Part IV / Chapter 22)

| Lens | Challenge | Disposition / evidence | Residual gate |
|---|---|---|---|
| Implementer | Is code executable without an agent SDK? Can a local record be confirmed without E8? | Standard library, two SQLite stores, six tests; failed or absent lookup never permits redispatch | Concurrency and recovery under process kill not production-certified |
| Enterprise architect | Have E1–E9 responsibilities and C01–C09 contracts been conflated with services or new authority? | Ch22 §22.2 maps active, absent and simulated duties; CAB unchanged; C04 explicitly absent | Field-level CAB contract audit for later builds |
| Advanced student | Does Build 0 imply a required A→B→C migration? Is the scenario still CASE-204? | Part opener explicitly separates builds from alternative designs; fixed $500 and RF-1042; B conditional, C optional | Classroom comprehension review |
| Security/assurance | Can untrusted reasoning or a valid agent credential issue a refund? | Build 0 has no agent, no credentials or live provider; denied tenant/principal/approval fixture tests; does NOT claim live secure E5 | Ch29/31 real compromised-agent denial scenario remains pinned |
| SRE/operations | What if provider commits but response is lost? | UNKNOWN retained, resend denied, stable RF-1042 query, matching mock E8 evidence required | Real provider guarantees, lease fencing, observability and crash injection |
| Business owner | Is automation value justified? | Baseline is a testable comparator, not ROI evidence or license to deploy; B remains conditional | Measured cost/value, approval, residual risk acceptance |

## Scope and claims

- `F22-01`: logical architecture, deliberately distinguish fixed E1/E2 inputs, E5 check, E7 local state, E6 adapter, simulated E8 truth, and E9 tests. The presentation does not depict an agent or credential path.
- `F22-02`: operation-state diagram, deliberately not the customer case lifecycle. No UNKNOWN→new dispatch transition.
- Original ETIS engineering exercises and fixture; cited Gray & Reuter, Kleppmann, RFC 9110 and NIST AI RMF are bounded to general source concepts, not payment guarantee or implementation certification.
- Manuscript-wide change impact: Part IV opener, chapter 22, frontmatter reader path, appendix book status, bibliography title range, source register, traceability, README, example README, QA scripts and Makefile. Source bibliography records unchanged because every cited source already appears. Future chapter placeholders remain unchanged.

## Executed QA / explicit unresolved gates

- `python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v`: **6 tests PASS** in temporary SQLite databases.
- `publishing/scripts/check_ch22_acceptance.py`: **PASS** for source markers, V12 invariants, editable 5.75-inch SVG source/render identity, 21pt+ SVG labels, 1800px PNGs and SHA-256 current Word embedding.
- `publishing/scripts/check_ch21_acceptance.py`, `publishing/scripts/check_figures.py --built`, `publishing/scripts/check_parts13_reader_paths.py`: **PASS** after regenerated full-book DOCX.
- Standalone Chapter 22 DOCX converted with LibreOffice: **7 pages**. This is a *standalone, non-native provisional measurement*, NOT native Word Mac 7x10 integrated finished chapter pagination. V12 14-page ceiling **not yet certified**.
- `make check` full regression: **NOT PASS / incomplete** in current sandbox; a run got through Chapter 21, but was terminated before Chapter 22 and the later whole-book gates. Must be rerun on Mac, and a completed exit 0 must be recorded.
- The uploaded/current Word document is a separate style/pagination baseline; source-built Word style parity is still an **OPEN P0**. **Part I 18-page overrun** and prior edition page variances remain **OPEN P0**. Exact source claim-to-page verification and native Word print-size figure inspection remain **OPEN**.

## Do not certify prematurely

All 59 figure references are structurally present in the source build; figure count and fingerprint are not visual publication review. Native Word two-page spread review is required for both figures and their captions, table wrapping, any clipped text, and Chapter 22 actual page count. Code does not supply live secrets, authenticate real principals, acquire an E2 lease, or provide production isolation. The Mac check must verify figures regenerate and no existing E/C or publication gate regresses.
