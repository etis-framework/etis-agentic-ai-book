# Chapter 25 / Build 3 — six-lens technical and editorial review

**Baseline:** user-supplied `ETIS_CH25_BASELINE.tar.gz`, main SHA `6c435e70deae07f71a4c741e03f018c37cb22090`. This report records development gates, not independent publication certification. The authoritative CAB-001 document, repository's normative `ENGINEERING_STANDARD.md`, and V12 ledger remain controlling.

## Technical reading from front matter through Chapter 25

| Lens | Reviewed claim and potential contradiction | Change / disposition |
|---|---|---|
| Implementing engineer | Earlier Build 0 `approved=True` is a fixture argument, not a protected policy. Build 1/2 script-style imports share names (`contracts.py`, `demo.py`) and are not installable packages. | Build 3 keeps independent old entry points and loads Build 2's identity module explicitly in its demo/test harness to avoid incorrect module caching. E5 is a separate server process that owns Build 0's E7/E6 adapter imports. New module SVGs map the real code. |
| Enterprise architect | CAB-001's E1–E9 and C01–C09 are logical responsibilities, not mandated services or deployment maturity. No E2 distributed ownership or provider-specific idempotency is implied. | Chapter 25 maps E1/C01, E3/C04, E5/C05, E7/C06, E6/C07, E8/C08, and E9 with absent E2 fencing. Builds 0–5 remain pedagogical. Designs A/B/C remain alternatives; Design B remains conditional. |
| Advanced student | Token validity can be mistaken for business permission; test fixture data could appear to offer real identity assurance. | `test_gate.py` actually obtains a signed E1 fixture token and verifies it before submitting an unauthorized request, rather than relying on a literal `VALID_TOKEN` string. Distinct signed finance grant and separate response categories explained in chapter and README. |
| Security and assurance | Process isolation with the **same OS user** does not prevent hostile Python/host code from reading private fixture key files. HMAC approver token is not an externally authenticated human decision. | Attack-model scope explicitly limits investigator to its request API; code independently validates real fixture token and distinct signed grant server-side. Production gaps include separate UIDs, protected issuer keys, authorization/revocation, grant binding, replay ledger and adversarial execution tests in Ch29/31. A no-grant request creates no E7 or mock E8 file. This is *request-path enforcement*, not a hardened same-host sandbox. |
| SRE/operator | An outage after durable E7 claim may have uncertain external effects and must never be automatically resent; transport failure is not provider failure. | `UNKNOWN` and `ServiceUnavailable` preserve uncertainty; local duplicate dispatch is rejected, provider fixture state stays separate. Real provider reconciliation is deferred to Ch26, distributed lease fencing to optional Ch27; safe diagnostics and temporary resource cleanup tested. |
| Business owner | The build should not be a model-autonomy showcase or impose Design C. A financially consequential refund must remain subject to a business-approved, accountable decision. | CASE-204/$500/RF-1042 unchanged. Human/finance approval is separately modeled; Chapter 25's exercises compare operational cost/assurance of independent E5 versus an in-process control. Production audit/credential custody are not claimed. |

## Repository-wide navigation and terminology audit

- Updated Part IV introduction, appendix, glossary, index, source register, figure register, topic-traceability, companion root/architecture/testing/contribution/engineering-standard guides, and working book status. No reader-facing `STATUS: PLANNED` remains in Chapter 25.
- Re-established mandatory Build 0/1/2 source-module diagrams because the supplied Chapter 25 baseline did not contain `architecture.svg` in those directories; added Build 3's and embedded all four with relative README references. This is not a change to running source APIs or earlier tests.
- Sources distinguish NIST SP 800-207's resource-verification principles and OWASP's threat-motivation categories from the original ETIS HMAC fixture. Exact source-page/edition verification remains open.
- Figure F25-01 depicts architecture, F25-02 behavior, and F25-03 decisions separately. Source/render fingerprints and bounded small arrowhead geometry are tested; visually inspected PNGs and available Word-compatible Chapter 25 page render. **Native Word for Mac 7×10 final-print inspection remains open**.

## Code and negative-test conclusions

- Build 3 uses the standard library, strict framing/field-set checks, exact integer cents, monotonic authorization order, signed/expiring case-specific grant, independent E1 fixture verifier, distinct E7 and mock E8 SQLite files, socket lifecycle cleanup, duplicate-claim denial and outage uncertainty.
- `test_gate.py` tests valid E1 token without grant, fake `APP-204`/RF-1042/advisory identities, tamper/expiry/wrong-scope, wrong-tenant/case/amount/bool/extra fields, malformed JSON, invalid E1 assertion despite grant, one confirmed operation and replay refusal, six concurrent requests, provider outage and no resend, conflicting mock E8 state after E7 claim, and unavailable E5.
- The tester's temporary keys are generated at runtime; no real credentials or payment integrations are used or stored in Git. A hostile same-UID process could bypass fixture key custody; independent OS-level security would require a stronger test deployment.
- **No production release certification** is justified. Requirements not implemented include finance reviewer authentication, authorization grant revocation and use ledger, real E1/E4 access controls, OS-level privilege and key isolation, real E6 provider integration, E2 epoch fencing, and operational audit/incident containment.

## Measured development gates

- Chapter source words: ~2,650 (under source cap 3,500). Available Word-compatible chapter DOCX renders to **9 pages**, compared with the V12 **14-page** allocation; this is *not* a measured native Word for Mac finished-page certification.
- Figure suite: 3 canonical SVG masters plus published SVG/PNG renders; manual inspection of F25-01/02/03 and module diagrams; code-listing format validated.
- Unit tests: Build 0 **16**, Build 1 **15**, Build 2 **13**, Build 3 **13** (57 total); run separately to preserve module namespace and independent checkpoint behavior.
- Chapter 25 acceptance, arrow geometry, code listing layout, source words, ledger, companion documentation/access, conceptual continuity, Part I–III integration and source/register preflights evaluated separately. `make book-docx` and `check_figures.py --built` succeeded. Full `make check` was interrupted by the tool execution limit in an earlier run; this must not be described as a complete pass unless a subsequent full run finishes.

## Publication gates held open

Native Word for Mac 7×10 pagination and figure/caption print inspection; final book page count/ledger; exact references by edition and source-page; independent complete front-matter-through-chapter editorial approval; real E5 OS isolation and issuer/key security; provider contract testing; adversarial live-agent system verification (Ch29 and Ch31); final immutable edition tag and reproducibility audit.
