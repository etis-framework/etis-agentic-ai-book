# Chapter 25 — transport resilience and figure semantics corrective review

## Scope and baseline

Incremental correction after the Chapter 25 Build 3, book-wide first-reference, and first post-war-game patches. No change to Build 0–2 executable code or CAB-001 contracts. The two service defects were reproducible in the earlier snapshot: an aborted requester could crash E5 on reply, and an incomplete request could block its single worker indefinitely.

## Changed assurance claims

- The E5 Unix-domain socket service now uses an absolute monotonic deadline of 0.75 seconds to read **one** bounded newline-delimited frame. An inbound byte does not extend that deadline. Malformed and incomplete input is denied before any authorization or durable intent, and recognized peer transport failures are contained per connection.
- An outbound reply can fail after a valid operation has committed; the service must continue, but the caller must treat its missing acknowledgment as **UNKNOWN** and reconcile. The service never retries the effect from the transport handler.
- A single-worker reference fixture is retained deliberately to keep concurrency and operation uniqueness inspectable. It is *not* an availability guarantee under sustained hostile connections: queued clients may time out, and actual deployments need independent process identities, controlled parallelism, backpressure, quotas, audit and service lifecycle management.
- Figure 25.1 now shows independent E5 authorization before `refund.prepare()` (E7 durable intent), before `refund.dispatch()` (E7 claim and simulated E6→mock E8 consequence). Figure 25.2 now shows a fixture grant entering the **client/harness**, then the client presenting it to E5; the finance actor does not directly call E5.

## Tests added to `build3/test_gate.py`

1. Aborted client after an unauthorized request leaves the E5 process serving subsequent clients.
2. Aborted client after a **valid authorized effect** leaves only one mock provider operation, with no replay dispatch.
3. Partial frame without newline expires within the service-side deadline and does not indefinitely block the next request.
4. Slow-trickle input does not reset the absolute deadline.
5. Oversized frame is rejected without an operation and subsequent requests still work.

## Six reader lenses

| Lens | Review question / disposition |
|---|---|
| Implementing engineer | Bounded request framing and specific socket error handling, with executable tests; no blanket exception swallowing of program defects |
| Enterprise architect | Figures now show actual ordering and independent grant's route; logical E-domains are not mistaken for isolated microservices |
| Advanced student | README links behavior, negative/positive tests, temporary fixtures and omitted production mechanisms to concrete source modules |
| Security/assurance | A genuine E1 token cannot replace approval; hostile client availability faults are bounded **per connection**, but no same-UID hostile-code protection or flood guarantee |
| SRE/operator | One broken peer no longer terminates E5; one partial frame cannot block forever; still need quotas, controlled concurrency, shutdown/restart observability |
| Business owner | CASE-204 and RF-1042 remain fixed; lost acknowledgments and external uncertainty never justify a new refund operation |

## Executed verification (development container)

- Build 0: 16 tests passed; Build 1: 15; Build 2: 13; Build 3: 18. **62 total**.
- Python compileall: passed.
- Chapter 25 acceptance: passed.
- Figure 25 geometry and source/render equality: passed; three figures inspected in standalone render, first two inspected in nine-page Word-compatible chapter preview.
- Companion diagram and documentation check: passed.
- Full-book DOCX generation and 68 figure references: passed.
- Full `make check`: attempted but terminated by execution limit during sequential test runs; not certified as one complete command. Other gates must be reported individually.
- Native Word for Mac 7×10 pagination and all-page print inspection: publication gate still open.

This review does not certify production payment, hostile host isolation, availability under sustained load, real provider semantics, or distributed idempotency.
