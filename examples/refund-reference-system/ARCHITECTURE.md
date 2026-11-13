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
