# Chapters 1–25: reader-first reference editorial review

## Scope and provenance

Reviewed developed chapter Markdown against CAB-001's responsibility/contract naming and the already accepted CASE-204 / RF-1042 invariants. Chapters 26–36 are placeholders, not reviewed chapters. This editorial patch is a **transition over the previously installed Chapter 25 development patch**; it does not overwrite Build 3 implementation files, change provider behavior, or certify production isolation.

## Corrections applied

- Chapter 8: clarify nine *logical* responsibilities, the recurring case and the controlled operation identity.
- Chapter 10: locally name coordination and ownership (E2) before using the shorthand.
- Chapter 15: locally distinguish durable E7 state, authoritative E8 business truth, C04 proposals and RF-1042.
- Chapters 16, 17, 19, 20: remove opaque catalog shorthand from entry objectives while retaining the architectural obligations.
- Chapter 22: describe the recurring $500 refund in the learning objective, then introduce CASE-204 in the text.
- Chapters 23–25: replace unexplained E/C/operation IDs in objectives, explain local E/C identifiers in §23.1 / §24.1 / §25.1, and distinguish advisory provenance/signatures from financial approval.
- Added a standing reader-first reference standard and automated entry-point preflight; Makefile includes it in `make check`.

## Six-lens reading

- **Implementing engineer:** descriptions remain traceable to executable modules and typed contract names; no source code changed.
- **Enterprise architect:** E-domains remain logical responsibility names; Python process boundaries and CAB contracts are not conflated.
- **Advanced student:** objectives no longer demand that the reader decode E/C/RF identifiers before seeing the case and concepts.
- **Security/assurance:** signed proposals and valid identity assertions remain distinct from case-specific payment approval and protected E5 access.
- **SRE/operator:** E7 local operational knowledge and E8 authoritative financial truth remain separate; RF-1042 remains stable across UNKNOWN/reconciliation.
- **Business owner:** the $500 remedy and its decision rights are visible before opaque identifiers.

## Acceptance and unresolved gates

Automated preflight is intentionally lexical and does not claim to measure comprehension. Native Microsoft Word for Mac 7×10 pagination, page breaks, source-to-claim audit and final print acceptance remain independently open. Figure masters and code are not modified by this patch.
