# Publication pass 02 — six-lens, selective-path, and source-evidence review

**Scope and baseline:** complete 36-chapter, seven-part publication source after publication certification pass 01, with the pass 02 typography, biography, navigation, and status corrections. Source baseline was reconstructed from the supplied repository and guarded chapter/publication patches; the current remote `main` Git object was not independently retrieved. This is a structured manuscript/code audit, not a claim that six humans read every word independently.

## Observed print/proof evidence

- Preliminary LibreOffice physical proof: **452 pages at 7 × 10 inches**. This is a measured rendering, not a guarantee of identical pagination in Word for Mac. V12 remains a planning allocation, not physical certification.
- The half-title uses a two-line 25-pt centered title; the title page repeats the book title in a formal centered 25-pt treatment, a 14.5-pt italic subtitle, and a 12.5-pt byline. The series uses a 17-pt serif heading. Both page-specific ETIS imprints render near the physical page bottom rather than following the body text.
- The subject index contains **109** registered entries and the contents **51** entries. The proof's **255** `PAGEREF` fields resolve against **359** bookmarked chapter, part and section headings; their cached review displays were populated from physical PDF headings with no unresolved target. These fields must be refreshed and inspected again after the publisher's final layout and font substitution.
- **About the Author** opens on a separate final page, rather than following the last index item. The copyright lists print ISBNs as unassigned and makes no digital-edition claim.
- The manuscript has **99** resolved figure references. Every progressive Build 0–5 README retains a source architecture diagram, and the companion root exposes the implementation/evidence map.

## Six independent QA perspectives — findings and disposition

| Internal reviewer perspective | Challenge to the complete book | Finding and disposition |
|---|---|---|
| Implementing engineer | Starting at Ch. 8 and Ch. 35, can code claims be followed to actual modules and tests? | Exact entry points and Appendix B mapping are present. Build 5 does not assemble the earlier advisory/retrieval pipeline in one integrated runtime; retain this explicit limit. Existing negative fixtures pass in the development environment; they do not certify deployment isolation. |
| Enterprise architect | Do Designs A/B/C remain alternatives, and do E1–E9/C01–C09 describe responsibilities without inventing independent services? | No new competing architecture found in the targeted end-to-end trace from Chapters 1, 8, 17, 22–27 and 35–36. Physical isolation and E5-enforced owner-epoch checks remain deployment requirements, not delivered code. |
| Advanced student (internal only) | Can the seven-part progression teach a reader why the demonstrator changes at each Build rather than implying each level is production-ready? | Progressive build navigation and stand-alone definitions remain, including failure/uncertainty and approval distinctions. Review lens names belong in this internal report, not in an invented enterprise approval hierarchy. |
| Security and assurance | Does a valid identity credential, an injected `approver`, or a forged advisory recommendation reach privileged payment execution? | Chapter 29's negative scenario and Build 3/security tests retain the denial boundary. Missing key custody, real grant revocation and hostile-host isolation are explicitly open. A Chapter 29 grammatical ambiguity in the boundary description was corrected. |
| SRE/operations | Do unknown provider outcomes, stale worker ownership, quarantine, rollback and restoration remain internally consistent? | CASE-204 and RF-1042 preserve original-effect identity; `UNKNOWN` is never equated to a failed payment. Chapters 28, 30, 33 and 35–36 distinguish release rollback from financial outcome reconciliation. Live provider and E5 epoch integration remain unproven. |
| Business owner | Can a reader defend the financial benefit, authority and acceptable loss, without assuming cheap inference makes an unsafe system acceptable? | Chapters 5, 32–34 and 36 preserve outcome-level economics, human accountability and nonnegotiable effect controls. Hypothetical ROI is distinguished from measured enterprise results. |

## Eight nonsequential entry-path challenges

1. **Architecture-first:** Ch. 8 → Ch. 17 → Ch. 35 → Appendix A. Contract definitions, roles and physical-boundary caveats available.
2. **Build-first:** companion README → Builds 0–5 → Appendix B → Ch. 35. Runnable demos and limitations named; no Build 6 or false integrated-runtime claim.
3. **Security-first:** Ch. 9 → Ch. 25 → Ch. 29 → security fixtures → Ch. 31. Valid-token/no-grant attack remains a denial, not a transaction approval.
4. **Reliability-first:** Ch. 20 → Chs. 26, 28, 30 → reliability/operations fixtures. Unknown settlement and no-blind-retry invariant retained.
5. **Governance-first:** Ch. 21 → Chs. 31–33 → Ch. 36. Risk owner, technical authorization and release authority are separate.
6. **Economics-first:** Ch. 5 → Ch. 34 → Ch. 36. Conditional adoption and retire/replace options remain legitimate outcomes.
7. **Teaching-first:** Chs. 1–7 → Builds 0–2 → Ch. 35. First-use terminology and intermediate engineering decisions provide a teachable progression; this is not experimental validation of student comprehension.
8. **CASE-204 trace:** Chs. 8, 17, 22–29, 31–36. A $500 recommendation cannot create a second RF-1042 payment or bypass independent grant enforcement.

## Sources and citations: verified scope versus open gate

The reader bibliography contains **32** line-item references, the machine-readable BibTeX contains **32** records, including the NIST SP 800-53 Rev. 5 and SSDF SP 800-218 references previously missing from the machine-readable list, and the cumulative source register describes claim/section mappings throughout Chapters 1–36. Source availability is not equivalent to passage-level support. The review also examined the chapter-local source notes and guarded original ETIS recommendations. The following public identifiers were sampled against authoritative or publication sources:

- RFC 9110 (June 2022), especially §9.2.2, supports HTTP-method idempotency but **not** a provider-specific payment-deduplication guarantee.
- Lamport, *Communications of the ACM* 21(7), 1978, DOI 10.1145/359545.359563, supports ordering of distributed events, not automatic financial finality.
- The OWASP *Top 10 for Agentic Applications for 2026* is dated December 9, 2025; security categories do not themselves verify a deployed ETIS control.
- NIST AI RMF, the ISO standards, vendor agent guides and current protocol documents still require final passage/version checks where non-original claims depend on them.

**Unclosed citation gate:** This pass has not compared each original external paper or paid standard page-by-page with every manuscript claim, nor checked every bibliography URL/edition against the source of record. The register explicitly retains these publication obligations. A green local QA script cannot certify citation sufficiency or copyright permissions. The final publisher/technical proof must close this gate before release.

## Other residual print and production gates

- Word-for-Mac: refresh all field caches, inspect Roman front-matter references, then export and compare the complete 7×10 PDF. LibreOffice's `PAGEREF` rendering may present Roman-preface targets numerically; cached fields in the supplied DOCX use the physically observed labels. Fix any edition-specific discrepancy before printing.
- Inspect all figures and tables at final print size, not merely that the image file exists; review widows, repeated headers, spine and odd/even-page parity.
- Assign paperback/hardcover ISBNs, confirm edition/copyright/permissions and finalize cover/spine/retail metadata. No digital edition is represented.
- Preserve actual protected production authority, provider finality, independent credential custody, attestation, protected evidence and operations as **future deployment evidence**, never as fixture results.

**Disposition:** Pass 02 layout/source navigation changes are ready for guarded branch installation and Word-for-Mac proof. Final print and citation certification is **conditional**, not complete.
