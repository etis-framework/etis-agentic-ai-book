# Chapter 24 / Build 2 — Six-lens source and manuscript review

Baseline: uploaded `ETIS_CH24_BASELINE.tar.gz`, supplied after Chapter 23 merged. Review unit: front matter through Chapter 24, CAB-001 (approved logical domain and C01–C09 table), implementation Builds 0–2, Part IV bridge, source register, appendix and navigation. **Development review evidence, not publication certification.**

## Continuous reader-path findings and corrections in this patch

- Chapters 3, 8–16, 17–21 assign identities, context provenance and financial authority to different boundaries. Chapter 22 establishes CASE-204 $500 / trusted RF-1042 E7 vs mock E8; Chapter 23 establishes fixed fixture evidence, C04 correlation `TRACE-204` and review-only proposal `ADV-TRACE-204`. Chapter 24 reuses all names, money expressed as 50,000 cents and unchanged Build 1 code. No new E7 payment state, provider operation or implicit authorization appears.
- CAB-001 C01 runs E1→E2, C02 E2→E3, C03 E3→E4, C04 E3→E5. Build 2 simulates only E1 assertion checks and a **controller-prefetched** C03-style response *on behalf of* E3, then passes it to Build 1; manuscript and code README explicitly disclose the partial direction rather than depicting a new authoritative contract. The financial C04→E5 interface remains absent.
- Source status and reader navigation: Chapter 24 placeholder replaced; Part IV, companion README, architecture, testing, contribution guide, glossary, appendix, source register, topic traceability, index, and Chapter 23 forward reference updated in the same patch. Existing past-tense source register and earlier chapters may still include historical audit language; claim-page verification is pending.
- Figures F24-01 (logical architecture), F24-02 (behavior), F24-03 (decision) have separate editable SVG masters and generated SVG/PNG mirrors. The decision figure distinguishes malformed C04 output from identity/scope/context denial; dotted non-link to E5/E6 is explicitly blocked, not a permitted call. Rendered at 1725×1200 pixels from 5.75×4-inch masters for 7×10 print inspection.

## Six skeptical reviewer lenses

| Lens | Verified development observation | Residual production/publication obligation |
|---|---|---|
| Implementing engineer | Typed immutable dataclasses, exact claim fields, fixed purpose, HMAC canonical byte encoding, strict time and source checks, bounded catalog record, explicit `ScopeDenied`/`ContextUnavailable`, deterministic reuse of Build 1. Full tests run. | Separate package imports for future builds; service contracts, error taxonomy and integration environment beyond fixture |
| Enterprise architect | E1 claim integrity and E4/C03 retrieval prefetch are distinct; E3/C04 not trusted; Designs A/B/C still alternatives; one-process topology declared. | Explicit E2 ownership and actual C01/C02 task admission; real E3→E4 query enforcement in an appropriately protected service |
| Advanced student | Complete offline CLI, expected negative exit statuses, commands wrapped intentionally for printing, same case/source names across prose/tests/figures, follow-on exercises. | Native Word on target platform and broader classroom usability validation |
| Security/assurance | Tampered/expired/other-tenant/source-mismatched claims fail; public key does not establish authentication; valid token cannot grant E5 business authority through this call path. | A malicious runtime could forge local scope; Chapters 25/29/31 must test independent protected E5 denial with valid compromised-agent token and no RF-1042 creation |
| SRE/operator | E4 outage has distinct failure category, no blind payment retry; repeated advisory leaves test E7/E8 SQLite markers unchanged; diagnostic categories sanitize CLI output. | Durable request ownership, replay-safe real IdP, remote telemetry, incident runbooks and provider UNKNOWN reconciliation |
| Business owner | No new financial effects; context-review quality can be measured separately from refund outcomes; design claims remain conditional. | Real customer data governance, independent adjudication and measured cost per acceptable workflow against Design A |

## Verification results and gates

- Build 0 regression: **16/16 passed**, independently rerun in development workspace and after clean installer extraction.
- Build 1 regression: **15/15 passed**, independently rerun in development workspace and after clean installer extraction.
- Build 2 regression: **13/13 passed**; tampering, expiry, wrong tenant/case/source, future/stale/version, outage, injection, repeated no-write marker files, valid agent token and prohibited financial coupling.
- Chapter 24 manuscript: approximately 2,500 words; V12 allocation 14 finished 7×10 pages. Local DOCX chapter rendered 9 pages in LibreOffice; print proof from Word for Mac remains open.
- Three canonical figures generated, visually reviewed as individual images and after rendering in Chapter 24 DOCX; separate semantics and print legibility. Native printer proof still open.
- Whole-repository `make check`: **PASS (exit 0)** after final source edits. `make book-docx`: **PASS**, with embedded figure verification. `check_code_listing_layout.py`, `check_figures.py --built`, Chapter 24 acceptance, and V12 ledger: **PASS**. The single-volume budget is a planning gate, not proof of native Mac Word publication pagination. Repeat on the user's Mac before committing.
- Installer preflight and apply tested against a clean extraction of the uploaded baseline: **31 per-file SHA-256 guards PASS**; installed Build 0/1/2 tests **16+15+13 PASS**. Dirty Git tree and wrong before-hash correctly refused; TAR archive content verified.
- Chapter 24 print preview: **9 pages** under 14-page V12 allocation, in the local LibreOffice renderer; all 3 figure masters inspected individually and chapter page montage visually reviewed. The native Word for Mac pagination gate remains open.
- Source-page and edition verification, external identity-provider integration, release credentials, print accessibility/figures and formal production security review remain OPEN. No build is certified for real payments.
