# Chapter 25 post-Word war-game corrective review

Scope: follow-on incremental changes after the installed Chapter 25 Build 3 and first-reference editorial updates. This is **not** a production-security certification or a substitute for native Word for Mac inspection.

## Corrected high-priority findings

1. F25-01 now traces a single actual request path: investigator → `client.py` → `service.py` E5 validation → server-owned Build 0 fixture adapter → E7 local intent and mock E8 truth. Denial branches inside E5 before any local financial data access. No arrow permits a caller-to-adapter bypass.
2. F25-02 now separates the compromised E3 investigator from the **illustrative fixture** finance issuer. The grant-origin arrow represents a source of separately reviewed approval presented via the client request, *not a second direct IPC call or a production finance approval service*. Labels and type sizes are enlarged from the prior 16-point sequence annotations; source/render equality and arrowhead bounds are checked.
3. `build2/README.md` no longer calls Build 3 an independently protected E5 gate. The root, architecture, testing, build READMEs and engineering standard distinguish independent **request-path** checks from actual OS-level hostile-code isolation, protected keys or issuer identities.

## Corrected medium-priority findings

4. Root companion README's tree includes Build 3 source modules and checked-in `architecture.svg` in every Build 0–3 folder.
5. Companion Markdown introductions give local meaning to relevant E/C identifiers, CASE-204 and RF-1042 without repeating a full architectural glossary. Non-production guarantees and UNKNOWN remain explicit.
6. New `publishing/scripts/check_companion_architecture_docs.py` is integrated into `make check`; it checks embedded diagrams, root tree entries, first-use boundary wording, misleading phrases and broken local Markdown links. The Chapter 25 geometry check also verifies the corrected figures' essential semantic labels. These are mechanical regression checks, not semantic proof.

## Six reader lenses

- **Implementer:** F25-01 represents source call order; E5 denial precedes adapter import and database access; the Build 3 module names and paths correspond to source.
- **Enterprise architect:** CAB-001 E1/E3/E5/E6/E7/E8 are logical responsibilities, not deployment topology or an implicit permission grant.
- **Advanced student:** signed C04 advice and a valid E1 assertion are not independently reviewed finance approval; separate swimlane makes origin distinct.
- **Security/assurance:** client API can be denied with a valid identity token; shared OS-user fixture does **not** withstand arbitrary same-user host code; finance issuer is a fixture.
- **SRE/operations:** one stable RF-1042 operation, E7 versus simulated E8 truth, UNKNOWN and no-blind-retry remain unchanged.
- **Business owner:** approval of the proposed $500 CASE-204 refund is independent of model recommendation; verified financial effect is distinguished from request acceptance.

## Executed QA and residual gates

- `make book-docx`: passed, including built 68 figure references.
- Chapter 25 acceptance, Chapter 25 arrowhead/semantic geometry, and companion architecture/docs and companion code quality checks: passed.
- First-reference preflight: 25 developed chapters, zero automated issues.
- Builds 0, 1 and 2 passed in the recorded `make check` run (16+15+13); Build 3 separately passed 13 tests: total 57.
- V12 finished-page **allocation** ledger passed; the independent Chapter 25 DOCX→PDF preview displayed nine pages. The earlier uploaded combined Word-compatible rendering was twelve pages for Chapter 25; exact pagination is renderer-dependent. The allocation is fourteen.
- `make check` was stopped by the execution environment during Build 3 tests; **a complete end-to-end make check pass is not claimed**. The Mac must run it.
- Native Word for Mac figure print-size QA, whole-book pagination, source audits and release certification remain open. The installed patch's final reviewer should inspect F25-01 and F25-02 at 7 × 10 print scale.
