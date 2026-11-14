# Part IV — Progressive Reference Implementation

## The design becomes a falsifiable system

Parts I–III established why an enterprise cannot equate a fluent proposal with permission or a payment outcome, specified nine logical architectural responsibilities and nine cross-domain contracts, and compared implementation patterns. Part IV now asks whether those distinctions survive actual code, persistence, negative tests, and recovery. It is not a framework tutorial or a demonstration that a more autonomous agent is inherently better.

The running case is unchanged: **CASE-204**, an unresolved replacement complaint involving a possible **$500 refund**. When a refund operation is authorized, its stable identity is **RF-1042**. The enterprise must keep an agent's advisory proposal (C04) separate from the independently authorized and durably recorded financial intent (C05–C06). A local timeout cannot establish provider failure; **UNKNOWN is not FAILED**. The provider's authoritative payment result belongs to business truth (E8), not to model memory, workflow rhetoric, or a successful transport response.

## Six builds; one consistent contract

| Increment | What it demonstrates | What it does *not* imply |
|---|---|---|
| Chapter 22 — Build 0 | A deterministic baseline, isolated simulated provider, durable operation identity, independent rule check, denial and lost-acknowledgment tests | Production payment service, complete identity platform, or AI capability |
| Chapter 23 — Build 1 | Bounded advisory interpretation and a typed proposal | Model authorization of a payment |
| Chapter 24 — Build 2 | Scoped identity and context with provenance | Retrieved material as financial truth or new permission |
| Chapter 25 — Build 3 | Hardened independent trusted execution of a consequential effect | Agent-owned provider keys or bypass of policy checks |
| Chapter 26 — Build 4 | Provider adapter guarantees, uncertain outcomes, reconciliation | Exactly-once behavior without a documented provider contract |
| Chapter 27 — Build 5 | Optional coordination, containment, and production hardening | A required Design C deployment or mandatory multiagent architecture |

**Build increments are teaching milestones; Designs A, B, and C are competing business/architecture alternatives.** Design A is a deterministic workflow; Design B adds advisory AI with independent review and remains the **conditional initial production candidate** under the assumptions defended in Chapters 3 and 17; Design C is an optional bounded, read-only investigator pilot justified only by its own measurements. The presence of Build 5 does not mandate C. A team can stop at the least complex variant that satisfies its requirements and verification obligations.

## The reference architecture remains the control structure

The nine domains, not necessarily nine services, are **E1 admission and identity; E2 coordination and ownership; E3 agent reasoning; E4 context and retrieval; E5 trusted execution; E6 enterprise integration; E7 durable operational state; E8 authoritative business truth; and E9 governance and assurance**. Their C01–C09 contracts are defined in Chapter 8 and the architectural contract appendix. In Build 0, some responsibilities are represented by deliberate fixture boundaries or an explicit *absence*, not production modules: E3/E4 do not run; E1 uses fixed trusted inputs rather than live authentication; E2 uses a single sequential controller; E5 is a deterministic independent policy function; E6 is an isolated simulated provider interface; E7 and the mock E8 provider are separate stores; E9 begins with repeatable executable test results. No diagram should suggest these fixtures already satisfy production assurance.

Follow each increment by asking which **new capability** is justified, which **boundary** it changes, what **counterexample** would falsify it, and which **evidence** is required to proceed. Later Chapters 28–31 deliberately break the integrated system; Chapters 32–34 assign oversight, release and economic accountability. They do not relieve Build 0 of elementary negative testing.

## Running and examining the companion implementation

The runnable examples and automated tests accompany the book at **https://github.com/etis-framework/etis-agentic-ai-book**, beginning in **`examples/refund-reference-system/README.md`** (direct link: **https://github.com/etis-framework/etis-agentic-ai-book/tree/main/examples/refund-reference-system**). Use the source revision tagged for your edition. Chapter 22 gives the first complete run and evidence-inspection procedure, using Python's standard library with no real payment credentials or customer data. Chapter 23 adds a second independently executable, credential-free Build 1 advisory demonstration; `build1/README.md` explains its strict C04 proposal contract, negative tests and deliberate lack of financial authority. Later chapters explain their own build deltas, boundaries and evidence.

Examine each build's **code, diagrams, tests and assumptions together**. In particular, compare what the application's durable operational state (E7) knows with what the separate simulated provider record (E8) says occurred. A $500 payment may be confirmed by the mock provider while RF-1042 remains UNKNOWN locally because its acknowledgment was lost. Reconciliation—not a fresh refund request—resolves this discrepancy when sufficient provider evidence becomes available.

A passing test demonstrates only the specified teaching scenario; it does not prove a real provider's guarantees, security boundaries, concurrency or production readiness. Chapters 8–16 and the architectural-contract appendix explain the E1–E9 and C01–C09 responsibilities for readers without requiring any internal ETIS production files.

Build 2 (Chapter 24) introduces a deliberately simulated E1 assertion-verification step and an E4/C03 resource-scoped context gate before the same Build 1 C04 review proposal. Its publicly known fixture key and in-process records are **not** authentication, isolated data authorization or transaction-specific permission. Consult `build2/README.md` and the three Figure 24 representations before interpreting test results. Chapter 25 demonstrates independent E5 **request-path** denial of a compromised, valid-fixture-token investigator's unauthorized `$500` request; its same-user process demo is not production OS confinement.

Build 3 (Chapter 25) adds an independently running E5 request gate and verifies that an investigator bearing a **valid E1 fixture token** cannot initiate RF-1042 without a separate case-specific finance approval. The same-user process demo teaches the decision boundary but does not implement hardened OS privilege separation. Refer to `build3/README.md` and its embedded `architecture.svg` for source-module mapping, attack reproductions and explicit production gaps. Build 4 remains responsible for real provider contracts and reconciliation.
