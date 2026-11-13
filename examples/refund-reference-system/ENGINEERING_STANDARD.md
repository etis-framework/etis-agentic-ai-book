# Companion engineering standard — Builds 0–5

This is the **normative review checklist for the book's teaching code**. It does not claim that the code is certified for real payments. Implementers must preserve CAB-001, the approved E1–E9 responsibility boundaries and C01–C09 contracts; *physical modules are not themselves security boundaries*. Prefer simple, typed, inspectable code over framework-specific abstractions without learning value.

## Mandatory requirements for every build

1. **Authority is explicit.** E3/C04 produces untrusted advisory data. It may never call E6 payment facilities, mint RF-1042, or alter E7 authoritative operation state. Only a protected, independently authorized E5 path may cause a consequential command. A token proving agent identity is **not** transaction-specific business authorization. The local Build 0 function API is not a protected boundary.
2. **Contracts precede implementation.** Define input/output types, scope and provenance, validation, error categories, idempotency semantics, preconditions/postconditions, and ownership before adding a new capability. State which CAB-001 logical contract is represented and which contract obligations are absent.
3. **Money is exact and bounded.** Use integer minor units or an explicit decimal currency type with verified precision. Reject booleans, floats, negative amounts, invalid identity/scope and inconsistent requests at the trusted boundary. No user or model text is a policy source.
4. **State is recoverable.** E7 owns local workflow/operation knowledge; E8 owns authoritative business truth. Preserve stable operation ID, immutable intent, durable status, and source observation. A timeout, crash, lost acknowledgment or inconclusive lookup never becomes FAILED or permission to invent a new operation. Do not silently retry uncertain consequential requests.
5. **Concurrency has a declared boundary.** Use atomic local claims / uniqueness in a one-process fixture. For high-risk multi-worker operation, require durable coordinator ownership, lease/epoch fencing, E5 enforcement against stale owners, and provider contract assurance. Never suggest SQLite's atomic claim is equivalent to distributed fencing.
6. **Errors are deliberate.** Distinguish policy denial, invalid request, unavailable dependency, inconsistent provider response, and infrastructure failure. Keep diagnostic details safe for logs; do not leak credentials/PII. An infrastructure error after E7 dispatch is an UNKNOWN *operational outcome* even if the simulator does not yet persist a separate UNKNOWN state.
7. **Operational evidence is independent.** Report correlation/operation ID, structured decision records, provider observation provenance, policy version, actor/approval scope, timing, and reviewer actions at the appropriate production build. Do not manufacture evidence from model explanations. Build 0's CLI JSON is *not* an audit log or telemetry pipeline.
8. **Tests prove negative boundaries.** Add authorization denial, cross-tenant, compromised-agent, schema rejection, duplicate and concurrent dispatch, lost acknowledgment, provider absence/conflict, restart/reconciliation, failure injection, and operator containment when applicable. Tests must be deterministic, self-contained, and specify what they do not prove.
9. **Keep the teaching path executable.** Include a root README, build README, architecture map, testing/evidence matrix, prerequisites, exact commands, expected outcomes, safe cleanup, debugging hints, and a concise next-build delta. Tests, prose, figures and terminology change together.
10. **Publish reproducibly.** Python versions/dependencies must be documented and pinned when introduced; no live credentials in the repo; fail CI on static and dynamic checks. Every edition points to an immutable tag, not mutable `main`. Follow all chapter-level manuscript, figure, citation and page-budget QA gates.

## Build-specific control progression and acceptance criteria

| Checkpoint | New teaching capability | Release-critical negative check | Deliberate boundary |
|---|---|---|---|
| Build 0 / Ch22 | Fixed Design A baseline, local E5 fixture check, durable E7 SQLite intent, mock E8 independent record, reconciliation | Invalid/unauthorized input creates no intent; simultaneous dispatch claims only one E7 operation; failure remains unresolved | No real E1 authentication, service-isolated E5, payment provider, E2 ownership or distributed fencing |
| Build 1 / Ch23 | Bounded **advisory** reasoning/typed proposal; deterministic or model-assisted candidate behind the same contract | Proposal is not RF-1042; no E6 access; invalid/stale/adversarial proposal denied; deterministic baseline remains runnable | No escalation of model authority; Design C not required |
| Build 2 / Ch24 | Authenticated scope inputs and provenance-bearing E4 context, constrained C03/C04 | Cross-tenant, stale context, malicious retrieval instructions and forged advice cannot change permissions | Context remains untrusted relative to E5/E8 |
| Build 3 / Ch25 | Protected independent E5 enforcement and consequential interface control | Valid *agent token* plus unauthorized CASE-204 $500 request fails; E3/C04 cannot mint RF-1042 or reach E6 | Demonstrate real process/credential isolation appropriate to stated risk |
| Build 4 / Ch26 | Provider adapter contract, durable effects, idempotency and authoritative reconciliation | Fault injection including uncertain provider commit, retries, missing/conflicting data, and replay never creates an unauthorized second effect | Provider-specific guarantees must be documented/verified, not inferred |
| Build 5 / Ch27 | Optional bounded coordination, ownership fencing, operational containment and production hardening | Stale coordinator/worker, takeover, cancellation, revocation, and duplicate handoff are denied or safely reconciled | A and B remain valid production candidates; C is optional |

## File and code review rubric

For each change, reviewers inspect public API clarity, modular cohesion, naming/types, resource cleanup, transaction and race behavior, exceptions and CLI/API outcomes, state reconstruction, security scope, test design, documentation accuracy, and relative line-by-line agreement with the chapter. A `TODO` is acceptable only when it identifies **the missing mechanism, the owner/boundary, the consequence of omission, the chapter introducing it, and verification evidence**; it must not masquerade as an implemented control. A stub that would allow an unsafe effect by default is prohibited.

## Reviewer exercise

For each build ask: *Can I execute the exercise from a fresh clone? Can I identify who can authorize a refund? Can I reproduce a denied action and an unresolved outcome? Can I distinguish mock E8 truth from E7 local belief? Can I see what the next build adds without interpreting a model-generated explanation as proof?*
