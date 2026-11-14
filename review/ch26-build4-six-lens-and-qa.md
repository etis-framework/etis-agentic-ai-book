# Chapter 26 / Build 4 — Six-Lens War-Game and QA Evidence

**Development state:** Chapter drafted and integrated, pending author native Word for Mac 7×10 inspection and external source/provider-contract verification. This is a **source and fixture QA result**, not certification of financial deployment or print publication.

## Exact version and invariants

Baseline: complete reconstructed Chapter 25 final transport-corrected source snapshot. CAB-001 E1–E9/C01–C09 remains canonical, not replaced by Python directory names. CASE-204 still means a proposed $500 refund; only independently authorized trusted execution may create RF-1042. Designs A/B/C remain alternatives; Design B remains a conditional initial production candidate. C04 advice cannot authorize payment or become C08 provider proof. The new fixture is **not** a commercial payment API and cannot transmit funds. Build 4 is an independently runnable checkpoint; Builds 0–3 retain runnable source and tests.

## Changes by engineering responsibility

- **E1/C01:** Build 2 HMAC fixture assertion remains independently validated *inside the Build 4 E5 process*. Token validity does not constitute finance approval. Provider command cannot be provided as an arbitrary `VerifiedScope` object.
- **E5/C05:** Reuses Build 3 grant verifier with a separate key; rejects valid-token/no-grant requests before any E7/E8 database creation. `reconcile` also requires a fresh-enough valid grant in this fixture. Production should assign independently governed, auditable read-only reconciliation authority rather than relying on repeated finance issuance; a one-minute fixture grant is not an operating recovery model.
- **E7/C06:** Exact integer-cents immutable RF-1042 operation; `AUTHORIZED` intent and atomic `DISPATCHED` claim committed before external mock call; separate local SQLite connection explicitly closed. Unknowns and contradictory proof cannot become a new dispatch.
- **Fault-injection scope:** The demo request explicitly exposes `lose_ack` and `outage_before_send` to reproduce failure cases. These are local test-only fields that must be removed from any production request contract and moved behind protected test harness controls.
- **E6/C07:** Versioned simulated provider adapter with `Capabilities`, typed request and `ProviderPort`. Case, tenant, USD, 50,000 cents and RF-1042 are enforced. Provider-account-scoped idempotency and one-day retention are illustrative declarations; the fixture does not simulate actual retention expiry or an external provider's availability.
- **E8/C08:** Separate provider SQLite database with unique operation key and read-only status lookup. `NOT_FOUND` does not prove payment failure. Confirmation requires a typed, matching provider reference; mismatch leaves local UNKNOWN.
- **E2/E9:** One local controller with fixture evidence; no multi-site fencing, independent approval issuer, real credentials, settlement, durable status scheduler or privacy-governed audit ledger.

## Six reader lenses

| Lens | Adversarial question | Evidence and resolution | Residual requirement |
|---|---|---|---|
| Implementing engineer | Can boolean money, wrong tenant, invalid adapter capabilities or duplicate execution cause an inconsistent payment? | Strict fixed commands; versioned capability validation; SQLite unique key; atomic E7 claim; 25 Build 4 negative/positive tests, including six parallel dispatch attempts | Real provider SDK/API integration and stronger static/type tooling |
| Enterprise architect | Do E5, E7, E6 and E8 map to real modules without inventing nine services? | F26-01, `build4/architecture.svg`, module responsibility table and CAB-001 contract traceability | Deployment and trust-zone diagrams for actual production identities |
| Advanced student | Can a reader distinguish provider idempotency from reconciliation and reproduce failure evidence? | F26-02 behavioral view, F26-03 decision view, README commands, lost-ack and missing-provider scenario table | Extend exercise to stale and delayed real provider queries |
| Security/assurance | Does valid E1 fixture token alone create RF-1042? Can a forged C04 approval reach E6? | End-to-end E5 subprocess denies unapproved valid token before creating either database; actual issuer fixture and independent signing key | OS principal isolation, key custody, audit, revocation, formal issuer governance |
| SRE/operator | Does an interruption kill E5, block forever, or blindly reissue after UNKNOWN? | Frame deadline; peer disconnect handling; lost-ack query; no-replay; recovery after subprocess restart; status-only reconciliation | Bounded status retries, monitoring, backpressure, operator escalation and multi-site fencing |
| Business owner | Can the book distinguish a proposed $500 refund from a settled customer payment? | Case/operation identity stays fixed, typed provider proof, no claim of real money or settlement; release decision exercises | Finance approval procedures, settlement evidence, customer communications |

## War-game findings corrected during the build

1. **SQLite resource ownership:** Initial Build 4 tests generated Python 3.13 `ResourceWarning` because a transaction context alone does not close a SQLite connection. Added explicit `closing` context managers in adapter and ledger, and corrected inherited Build 0–3 tests' own connection lifetimes. All five suites pass with `PYTHONWARNINGS=error::ResourceWarning`; no warnings observed after the cleanup.
2. **Duplicate test inheritance:** The first Build 4 test class hierarchy inadvertently ran underlying tests twice. Refactored into separate fixture and process test classes. Added concurrency and restart-reconciliation cases; current suite has 25 independent tests.
3. **Figure 26.1:** Initial E9 assurance label overflowed its box. Replaced with a shorter, two-line label and visually verified the corrected source/rendered SVG.
4. **Figure 26.2:** Initial four-lane sequence used too-small type and an ambiguous direct E8-to-E5 final arrow. Rebuilt as a readable three-lane, seven-event behavioral view with explicit E7 claim, lost reply, status-only query, validated proof and final E7 transition. PDF preview inspected at 7×10.
5. **Build 4 source diagram:** Removed an incorrect demo-to-test dependency arrow and shortened the provider contract module label. Current diagram depicts separate executable entry points and actual module paths, not a fictional authorization issuer.
6. **Print-width lint:** First manuscript command block exceeded 68 columns. Rewrote the runbook using `cd examples/refund-reference-system/build4` and shorter commands, verified by book-wide listing check.
7. **Conflicting provider record:** Tests require a matching immutable amount/currency/case/version. A conflict after an E7 dispatch claim remains UNKNOWN, never a clean pre-effect DENIED; previously confirmed but newly contradictory provider evidence is flagged unresolved.

## Executed checks (available container environment)

- Python compilation: Build 4 modules compile. Demo scenarios `approved`, `denied`, `lost-ack`, `outage`: expected outcomes verified.
- Build 0 tests: 16 pass. Build 1: 15 pass. Build 2: 13 pass. Build 3: 18 pass. Build 4: **25 pass**. **Total 87.** All suites executed independently with resource warning checks; legacy test harness connections were corrected in this patch.
- Chapter 26 acceptance, F26 source master/PNG checks, diagram semantic/geometry gate, 26-chapter first-reference preflight, companion documentation/relative-link gate, code-listing width, reference architecture continuity, parts I–III integration, book-wide source-word caps, V12 550-page allocation ledger: pass when individually invoked.
- Complete `make check`: **did not complete under execution limit**; one initial run exposed a fixed 68-column listing failure, a subsequent run was terminated late, so a complete local Mac run remains necessary. Do not describe it as a passed single invocation.
- Full `make book-docx`: passed. Figure checker counted **71** current manuscript images; the three F26 PNGs were verified byte-for-byte inside built DOCX media.
- Standalone Chapter 26 Word-compatible preview: **9 pages at measured 7×10 trim** versus locked 14-page Chapter 26 allocation. This is a layout preview using the book's section dimensions/margins, not native Microsoft Word for Mac certification.
- Rendered figures: F26-01 architecture; F26-02 behavioral sequence; F26-03 decision process. Source masters and current PNGs inspected; no orphaned arrows or clipped diagram labels apparent in inspected preview. Manual print check remains mandatory.

## Publication and production hold conditions

1. Run `make check` to completion on the user's development Mac; run `make book-docx` and inspect Figures 26.1–26.3 in actual Word for Mac at 7×10 print size. Verify chapter and cumulative page forecast; do not equate a Markdown word count with finished pagination.
2. Review the exact external source passages, citation edition/year/page and current provider-specific documentation before any claim beyond the static fixture. No real-provider verification has been performed here.
3. Do not accept Build 4 as production code **for real payments**: deployment requires distinct OS identities, independently governed finance/reconciliation roles, protected credentials, provider auth, measured status and idempotency semantics, monitoring, distributed fencing, bounded status-query retries, incident readiness and compliance controls. A production-quality coding style does not create a production deployment guarantee.
4. Keep manuscript, code, tests, diagram sources/renders, companion README, cross-references, figures and evidence in **one chapter patch**. Publisher metadata and final whole-book pagination remain open.
