# Part II — Enterprise Reference Architecture

**Engineering thread — Secure by design.** The reference architecture identifies where agent recommendations stop and independently governed consequential authority begins. Controls must be testable across contracts, not inferred from an agent's reasoning or from a logical diagram.

## The problem this part prepares you to solve

Part I established the business obligations of a trustworthy agentic AI system. It did not establish that a credible refund recommendation is an authorized financial instruction. For `CASE-204`, the customer requests a $500 refund after a replacement does not arrive. An AI component may help interpret the complaint, but the retailer still must verify identity, consult authoritative payment records, apply current policy, record the responsible approval, execute through a controlled payment interface, and determine whether money was actually returned. The reference architecture must make those responsibilities separately identifiable, enforceable, testable, and operable.

The central design problem is not how many agents or services to deploy. It is **where a recommendation stops being advice and where independently authorized business action begins**. A model's recommendation may be useful even when it is wrong. Its generated output is therefore treated as untrusted *for authorization*: not necessarily hostile code, but a claim without permission to change enterprise state. Trusted execution is a separately governed software path that enforces identity, policy, approval, durable intent, and provider interaction. “Trusted” describes assigned responsibility and controls that still require verification; it is not a certification conveyed by a name or colored box.

The architecture must also account for incomplete knowledge. When a payment provider has processed operation `RF-1042` but its acknowledgment is lost, the local operation is `UNKNOWN`, not failed. The customer case may be `OUTCOME_UNKNOWN`, with a durable owner and reconciliation path. A fluent agent explanation cannot settle that state. This distinction is as essential to architecture as its normal, successful path.

## What you should be able to do after Part II

1. Derive a logical responsibility map from testable business and quality requirements rather than from a vendor or framework diagram.
2. Identify authenticated admission, scoped delegation, workflow ownership, evidence provenance, independent authorization, provider integration, authoritative records, durable state, and accountable assurance.
3. Distinguish generated recommendations, approved decisions, attempted operations, and externally confirmed effects, with clear contracts at each handoff.
4. Trace tenant isolation, denial, provider uncertainty, cancellation, recovery, audit, and human escalation across component boundaries.
5. Separate logical architecture from deployment topology, defending a simpler deployment when it preserves the necessary enforcement boundaries.
6. Produce a reviewable architecture package: responsibility ownership, contractual invariants, threat boundaries, failure paths, tests, and unresolved design assumptions.

## The target-state architecture and its progressive decomposition

Part I defined the obligations and acceptance evidence; Part II now develops a **target-state logical reference architecture**: a vendor-neutral arrangement of responsibilities, contracts, and enforceable authority boundaries against which implementations can be evaluated. *Target-state* describes the intended logical design, not an approved production deployment or a claim that the architecture has passed its tests. Chapter 8 establishes the integrated architecture and introduces its nine responsibility domains, E1–E9, in Figure 8.1 and Section 8.3. Chapters 9–15 then progressively engineer those domains and their interfaces; Chapter 16 examines deployment realizations of the same boundaries. The domains are neither a prescribed call sequence nor nine required microservices. E7 (durable operational state) and E9 (assurance and operations) span the system. Every chapter returns to the same `CASE-204` and `RF-1042` contracts, allowing readers to trace an obligation from its architectural location to a testable implementation mechanism.

## The nine-chapter learning path

| Chapter | Design question | Engineering result |
|---|---|---|
| **8. From Requirements to a Reference Architecture** | What responsibilities and boundaries follow from Chapter 7? | Three complementary views and a requirement-to-control trace |
| **9. Admission, identity and scoped work** | Who requests work and what scope can the system accept? | Authenticated case admission and delegation checks |
| **10. Coordination, registry and ownership** | Who owns a task while people, agents, and services change? | Durable work ownership and bounded handoffs |
| **11. Agent reasoning and proposal contracts** | What may reasoning produce, and how is it constrained? | Typed advisory proposal and tool-selection boundary |
| **12. Context, retrieval and memory** | Which information may the agent use, and with what authority? | Scoped, provenance-bearing context contract |
| **13. Trusted execution and authority** | Who can approve and initiate a consequential effect? | Independent enforcement and authorization contract |
| **14. Enterprise integration and business truth** | How are provider effects and authoritative records distinguished? | Adapter and system-of-record contracts |
| **15. Durable operational state and assurance** | How does the system preserve uncertainty, evidence, and recovery? | Persistent operation state and operational accountability |
| **16. Trust boundaries and deployment views** | How should logical controls be placed in real environments? | Deployment choices, isolation, and tradeoff review |

## One case, three alternatives, one unchanged authority boundary

Design A is the deterministic comparison baseline. Design B adds advisory AI and independent review; it is the **conditional initial production candidate** pending measurement and assurance. Design C allows a bounded agent to select read-only investigation steps; it remains a separately evaluated alternative, **not** a promotion to autonomous financial authority. The three approaches are competing choices, not sequential stages of one refund. None can bypass independent policy enforcement, durable intent, controlled integration, or reconciliation.

We retain `CASE-204`, the $500 requested refund, and `RF-1042` as a stable illustrative payment-operation identity throughout. The payment provider's actual idempotency and status-lookup guarantees must be verified for any real implementation. Logical domains E1–E9 name responsibilities, not nine mandatory microservices. Chapters 9–16 will work through these responsibilities without changing the case to make a diagram easier.

## How to study and review this part

For each diagram, identify the owner of a claim, who may convert it into an authorized decision, which record is authoritative, what happens under timeout or denial, and which test could falsify the proposed boundary. Treat the figure as an architectural hypothesis until code, configuration, fault injection, and an operator drill establish evidence. Part III will compare architectural patterns; Part IV will build the reference system; Parts V–VI will deliberately challenge it through security, reliability, operational, and governance tests.
