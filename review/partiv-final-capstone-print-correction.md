# Parts I–IV final capstone and print integration correction

Scope: correct three findings from the 2026-11-14 final manuscript war-game. No architecture, source-code, build-specific READMEs, or Build 0–5 executable tests are altered.

1. Chapter 27 §27.9 now precedes the single chapter synthesis and Part V bridge. The capstone's three traces, learning claim and assurance limits are retained.
2. The Chapter 27 capstone evidence table receives `w:cantSplit` on each row and `w:tblHeader` on the header row, so pagination occurs only between complete data rows. The built-DOCX regression check verifies these actual XML properties.
3. The appendix combines repeated C04 identity/direction explanations without changing the original C04 field names or RF-1042 authorization semantics. The existing stringent `check_c04_identity_semantics.py` still passes unchanged.

## Executed checks on reconstructed final capstone source
- Chapter 27 acceptance: PASS.
- C04 identity semantics: PASS (unaltered guard).
- Part IV capstone and DOCX XML pagination: PASS.
- Chapter first references, professional perspectives, back matter and V12 allocations: PASS.
- Full DOCX generation, 74 figure references: PASS.
- LibreOffice 7x10 visual inspection: capstone table fits on one page; final chapter synthesis follows; no row fragment visible.
- Complete `make check`: NOT EXECUTED to completion for this patch; user must run locally.
- Native Word for Mac pagination and bibliographic claim/source audit: OPEN.

## Incremental installation
The installer allows pre-existing **uncommitted** source files when their contents exactly match the post-capstone patch bytes. It does not require a clean Git tree, reset Git, stage or commit anything. It requires a non-main development branch, verifies every input and target SHA-256 before writing, and creates no new working-tree files except the patch payload.
