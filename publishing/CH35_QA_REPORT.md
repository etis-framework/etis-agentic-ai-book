# Chapter 35 development quality record

- Baseline: reconstructed conversation pre-Chapter-35 repository after the Chapter 32–34 patches and the pre-Part VII audit; exact newly merged GitHub main SHA was **not** independently verified in this environment. Guarded source-file hashes are therefore mandatory at installation.
- V12: Chapter 35 allocation 10 finished pages; standalone 7×10 Word/LibreOffice PDF rendering: **9 pages**. This does not certify native Mac Word pagination or final whole-book print pagination.
- Source length: **2,367 regex-counted words** against the existing 3,000-word chapter cap. Four structured reference tables; two source/rendered architecture/decision figures.
- Chapter 35 check: **PASS**; source-to-test paths include 32 Markdown occurrences, all resolved.
- Dynamic back matter: **PASS**, 35 developed chapters, 81 glossary terms and 72 index entries.
- Chapter first-reference and professional perspectives: **PASS**, through Chapter 35.
- Existing Chapter 34 acceptance and V12 ledger: **PASS** after development-status synchronization.
- Companions: ten separately executed Python suites, **153/153 PASS** (Builds 0–5, reliability, security, operations, assurance). These are educational simulation tests.
- Full-book DOCX generation: **PASS**. Figure checks: **97** manuscript image references resolve; built-image checker **PASS**.
- Pre-Part VII structural checker: **PASS**. Single-volume word-cap/opaque identifier checker: **PASS** after replacing an opaque range.
- Aggregate `make check`: **not an uninterrupted PASS**. First run found stale publishing identity assumption (updated); second was interrupted during slow tests. A later run exposed one opaque range in Chapter 35 (fixed). All those identified failures were individually rechecked and passed. Complete uninterrupted aggregate still required on Mac.
- Source/standards passages, native Word-for-Mac print proof, independently verified merged Git SHA, production authorization, signed release and real provider evidence: **NOT VERIFIED**.
- Six-lens and eight-path documentary assessment: `review/ch35-six-lens-and-selective-path-war-game.md`.
