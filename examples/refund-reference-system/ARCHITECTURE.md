# Companion code architecture: logical contracts and actual modules

The textbook figures define the architecture and trust boundaries. Each working build README additionally includes a **source-level architecture drawing**, with terminology grounded in the E1–E9 responsibilities and C01–C09 contracts. These views distinguish Python modules and local test data from deployable services and enforceable protection boundaries.

- [Build 0 module architecture](build0/README.md#implementation-architecture): deterministic E5 fixture, E7 local record, E6/mock E8 interface
- [Build 1 module architecture](build1/README.md#implementation-architecture): E3 adviser, strict C04 contract, and excluded financial interfaces
- [Build 2 module architecture](build2/README.md#implementation-architecture): E1-like fixture scope, E4/C03-style gateway, and E3 advice

Later builds should add matching implementation diagrams without redefining the approved CAB-001 logical architecture. Source-level diagrams supplement, but do not replace, the chapter figures.

# Build 0 architectural scope (read with Chapter 22)

Build 0 illustrates selected E1–E9 logical responsibilities, **not nine production services**. Figure 22.1 shows trust boundaries and Figure 22.2 shows local operation-state transitions; their canonical SVG masters live in `assets/shared-figures/sources/`.

| Domain | Present educational mechanism | Not demonstrated |
|---|---|---|
| E1 | Fixed trusted case/principal inputs | Real authentication or delegation |
| E2 | Sequential CLI | Distributed ownership, leases and fencing |
| E3/E4 | Absent | No agent, retrieved context or model authority |
| E5 | `authorize()` deterministic fixture rule | Protected policy service, real human approval |
| E6 | In-process provider simulator | Network adapter, secrets and provider guarantees |
| E7 | `operations.sqlite3` local state | Authoritative financial truth |
| E8 | `provider.sqlite3` simulated provider | Real payment-provider effects |
| E9 | Automated fixture tests | Full production assurance |

C01, C02 and C05–C09 are illustrated only in a bounded, partial way; C03/C04 are absent. RF-1042 may be created only after the trusted policy check. A local UNKNOWN means the application does not know the provider outcome; it does not grant permission to retry under a new identity.

The scenario-to-observable-evidence matrix is in `TESTING.md`. The complete architecture is described in Chapter 8 and the book's appendix. Do not mistake this fixture for secure credential isolation, an authenticated service boundary, a tested idempotency contract, or production-ready concurrency.

## Important implementation boundary after the Chapter 22 hardening pass

Build 0 now atomically claims the local E7 `AUTHORIZED → DISPATCHED` transition using a conditional SQLite update. This prevents two *local* callers from winning the same state claim. It is **not** E2 distributed lease/epoch fencing, a protected E5 service, or an E6 provider-specific idempotency guarantee. A simulated provider-unavailable event intentionally leaves E7 `DISPATCHED` and mock E8 empty; only reconciliation or human investigation is permitted, never a blind resend. See `ENGINEERING_STANDARD.md` before adding Builds 1–5.

## Build 1 — advisory-only E3/C04 extension

The C02-like `WorkRequest` remains fixed fixture input (not authenticated E1). E3's `advise()` consumes one explicitly supplied E4-like `Evidence` value; neither retrieval nor its `verified` test bit provides production provenance. `Proposal` is an immutable, schema-checked **C04 untrusted proposal** with an `ADV-` proposal ID and a `TRACE-` correlation ID. Neither is the trusted RF-1042 financial operation identifier. E5 / C05 independently owns authorization and E7 / C06 owns durable consequential intent; Build 1 has no E5/E6/E7/E8 dependency or financial privilege. The optional `CandidateModel` interface returns raw data to a strict parser. A Python source-file boundary is not a hostile-runtime security boundary. Figure 23.1 and `build1/README.md` document the deliberate gaps and future owners.

## Build 2 — E1 identity and E4/C03 context before E3 advice

Chapter 24 / F24-01 separates issuer claims, verified **fixture** scope, scoped E4 catalog observation and untrusted E3/C04 recommendation. `build2/identity.py` verifies a canonical HMAC assertion with expiry and a fixed purpose; `context.py` applies tenant/case/source/classification/freshness checks through a controller-preselected C03-style query (not a literal E3->E4 invocation); `pipeline.py` adapts the result to the unchanged Build 1 `WorkRequest`/`Evidence`. No Build 0 payment imports or E7/E8 database writes appear. `TRACE-204` and `ADV-TRACE-204` remain advisory identifiers, not trusted RF-1042. A `VerifiedScope` instance and the signing key are **not** protected against hostile code running inside this Python process. Missing protections: real authentication and resource-policy enforcement (E1/E4 owners), isolated E5 authorization (Build 3), provider reconciliation (Build 4), and optional E2 fencing (Build 5). Inspect `build2/README.md`, the Figure 24 trio and `TESTING.md` before inferring assurance.
