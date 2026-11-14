# Glossary

**Advisory correlation identifier:** A trace label connecting E3 work and C04 review evidence, not a trusted payment operation ID.

**Bounded advisory proposal:** A validated, untrusted C04 recommendation and supporting provenance/uncertainty, with no E5 payment permission.

**Consequential operation identity:** The E5/E7-controlled stable identifier RF-1042 in the CASE-204 fixture; never minted by E3 advice.

**UNKNOWN:** An operational state indicating the outcome of a possibly dispatched external effect is not yet authoritatively established; not equivalent to failure.

[Additional terms will be edited against the controlled terminology register before final pagination.]

**Fixture-verified scope (Build 2):** A locally validated educational identity assertion bound to tenant, case, purpose, source allowlist and expiry; not independently authenticated enterprise identity or payment authority.

**Scoped context observation:** E4/C03 selected evidence with source, classification, version and observation age checked against a bounded purpose; not authoritative E8 financial truth.

**ContextUnavailable:** A failed E4 fixture dependency, distinct from unauthorized scope and from E7's `UNKNOWN` payment outcome.


**Transaction-specific authorization grant (Build 3).** A separately issued, bounded approval artifact specifying the case, tenant, amount, approver, policy version and validity interval. In the ETIS fixture it is independently verified by E5, not inferred from E1 identity or E3/C04 advice. A signed local test grant is not equivalent to a production finance approval service.

**Request-path process boundary.** A distinct E5 service process and IPC endpoint that evaluate authorization independently of the calling adviser. It is not necessarily a security isolation boundary when both run as the same operating-system user with shared file permissions.
