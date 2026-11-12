# Chapter 16 — Trust Boundaries and Deployment Views

*Part II: Enterprise Reference Architecture*

> **Engineering proposition:** A reference architecture becomes deployable only when each logical authority boundary has a concrete enforcement point, a failure and recovery owner, and evidence that no shorter path bypasses it. Physical separation is a risk decision, not a substitute for authorization.

## Learning objectives

After this chapter, readers should be able to (1) map Figure 8.1's nine E-domains logical responsibilities onto physical deployments without equating domains with microservices; (2) select isolation strength from consequence and threat exposure rather than technology fashion; (3) prove agent-originated proposals cannot reach provider credentials or a consequential endpoint without E5; (4) locate state, ownership, integration and business truth across failures; (5) compare deployment alternatives for cost, latency, operability and residual risk; and (6) prepare an evidence-backed deployment decision record and release gate.

## 16.1 Return to the architecture, not to a new model

Figure 8.1 established a **target-state logical reference architecture** in four layers: admission (E1); coordination, bounded reasoning and governed context (E2/E3/E4); independent authorization and integration (E5/E6); and enterprise systems with authoritative business truth (E8). Durable state (E7) and assurance (E9) span the layers. Chapters 9–15 developed these responsibilities and the contracts between them. This final Part II chapter asks how a real installation enforces those same contracts. It does not introduce a tenth domain or substitute an infrastructure diagram for architectural reasoning.

The running case is unchanged: `CASE-204` requests a **$500 refund** for a missing replacement; `RF-1042` is the stable illustrative refund-operation identity. **Design A** is the deterministic comparison baseline, **Design B** the conditional initial production candidate with advisory AI and independent review, and **Design C** a separately evaluated **read-only** investigator. They are alternatives, not a sequence of escalating authority. None may grant a model, worker or coordinator the provider payment credential, decide a refund autonomously, or call an unguarded payment route. A deployment that makes any of those shortcuts possible does not implement Figure 8.1.

A **deployment view** maps logical responsibilities to actual processes, hosts, accounts, networks, data stores, credentials and operators. A **trust boundary** is a point at which authority or data changes protection domain and must be checked by an independently controlled mechanism. A container, process or network segment is a potential boundary; the claim is valid only if permissions, identity and bypass tests establish it. Figure 16.1 is a *mapping* of the canonical architecture, not a new logical architecture or a mandate to operate a particular number of services.

![Figure 16.1 — One canonical nine E-domains architecture, mapped to physical protection zones. E7 and E9 span the zones; the only consequential path crosses independent E5 and governed E6.](assets/shared-figures/rendered/F16-01.png){#fig:f16-01 width=5.75in}

## 16.2 Map responsibilities and their enforcement owners

Begin with a **deployment responsibility matrix** rather than allocating boxes by team preference. Each row identifies a logical responsibility, where code runs, the identity it uses, who administers the policy, which persistent records it owns, which other zones it may reach, and how the boundary is tested. A shared host is possible; a shared unrestricted credential is not. In particular, E2's coordinator may route an authorized *request to consider* a refund, but does not own the power to execute it. E5 is an independently governed gate and credential-custody boundary, not a utility function that the agent can bypass.

| Domains | Typical placement | Essential non-bypass control |
|---|---|---|
| E1 | Enterprise ingress or admission service | Identity, tenant and purpose bound before work begins |
| E2/E3/E4 | Orchestration and constrained worker runtime | Scoped calls; advisory output only; no provider write route |
| E5 | Independently administered execution control | Effect-time policy and approval; protected credential custody |
| E6 | Governed integration adapter | Provider-specific contract, correlation, status and retry discipline |
| E7 | Durable workflow store and transition service | Versioned commits, operation uniqueness, lease/epoch fencing |
| E8 | Authoritative finance/order/case owners | Grounded facts and reconciliation; no AI-authored payment truth |
| E9 | Observability, audit and operational controls | Tamper-resistant evidence, independent alerting and hold authority |

This matrix does **not** require E5 and E6 to run as separate products. It does require that an E3-controlled identity cannot invoke an E6 payment method with the authority or credentials of E5. When a privileged library is co-located, the runtime must still show how model-controlled code and its transitive dependencies are prevented from exercising those privileges. If that cannot be enforced and tested, split the protection domains. Conversely, multiplying services while sharing unrestricted service accounts, writable policy files and network access is only *visual isolation*.

E7 is not merely a database behind E2. Its trusted transition authority must compare the expected workflow version and current ownership epoch before committing changes, and it must preserve the unique `RF-1042` intent and outbox linkage. E8 is not a copy of local workflow status. Actual provider effects and authoritative enterprise records must be reconciled through governed integration before a business completion claim is made. E9 observes each zone, but observation alone does not authorize a transition.

## 16.3 Choose isolation according to consequence

A **protection domain** is a runtime and administration boundary with its own enforceable permissions. Three example deployment profiles help make the trade-off explicit. They are risk patterns, not universal compliance tiers. NIST SP 800-207 (Rose et al., 2020) supports resource-focused enforcement without implicit trust from network location; the L/M/H deployment profiles are ETIS examples, not NIST-defined tiers.

**Profile L — bounded, low-consequence advisory work:** E2/E3/E4 may share an application process with E1, provided input scope and output contracts are enforced. There is no write-capable consequential path, and any later effect still requires an independently protected E5. This profile reduces overhead but does not authorize direct payment access simply because a case starts as advisory.

**Profile M — operationally meaningful but contained effects:** Put workers in a separate process with a constrained identity, minimal egress and resource limits, while a trusted service on the same host controls E5/E6. Separate process ownership and operating-system permissions must prevent credential access and direct adapter calls; host compromise or privileged operators remain correlated risks. The architecture remains acceptable only when the documented threat model and test evidence support those residual risks.

**Profile H — high-consequence or high-exposure workflows:** Use centrally governed or remotely isolated E5 and protected E6, independently administered secrets and policy, authenticated service-to-service invocation, restrictive network routes, and auditable approval. The agent zone has no direct payment-provider egress or key material. Network isolation is defense in depth; E5 must still validate case scope, balance, policy version, approval, operation identity and current eligibility when an effect is attempted.

Figure 16.2 contrasts isolation strength without implying that stronger separation eliminates software faults. Enforcement must survive an agent tool exploit, prompt injection, worker compromise, confused-deputy request, stale coordinator and misconfigured route. A **confused deputy** is a trusted component misused to exercise its authority on behalf of a caller lacking that authority. Test not only whether the intended call works, but whether every unintended path fails.

![Figure 16.2 — Risk-proportionate deployment alternatives retain the same E5/E6 consequence boundary; separation changes the strength and administration of that boundary.](assets/shared-figures/rendered/F16-02.png){#fig:f16-02 width=5.75in}

## 16.4 Make the consequential path the hardest path to bypass

For `CASE-204`, the deployed path begins with E1 binding principal, tenant and permissible work. E2 owns the workflow and may request an E3 recommendation using provenance-bearing E4 evidence. After any required human review, the trusted controller submits a structured request to E5. E5 rechecks current policy, authority, balance, approval and case scope and durably records the permitted operation. E6 obtains access to the protected payment capability and uses the stable `RF-1042` operation identity under the *verified provider contract*. **A payment idempotency key identifies an operation; it is not a security credential or an authorization token.** E5/E6 custody of actual provider credentials remains independent of model-originated code.

The provider may commit the effect yet drop the acknowledgment. At that point E7 records `UNKNOWN`; it does not infer `FAILED`, mint `RF-1043`, or issue a blind second payment. E6 uses a provider-supported inquiry or reconciliation process. E8's designated business-fact owners validate the resulting status and any required posting/settlement state before the workflow declares business completion. E9 records denial, dispatch, uncertainty, escalation and evidence. The provider's status semantics, idempotency retention and consistency windows are external facts to verify, not properties conferred by our diagram.

**Negative-path proof** is essential. Try E3-to-provider traffic; E3-to-E6 write calls; bypass of E5 by E2; direct use of a stolen or expired worker token; approval reuse on another tenant; policy change between review and dispatch; late messages from a fenced coordinator; and duplicate dispatch after a lost acknowledgment. Each attempt must fail closed or remain unresolved with an accountable owner. Simulate revocation and credential rotation while a request is in flight; an old approval or cached route must not silently survive changed authority. A security diagram without these tests is only a proposal.

## 16.5 Place durable state, reconciliation and operators deliberately

Availability zones and replicas improve resilience only when they preserve ownership and uniqueness semantics. E2 is horizontally replaceable, but one logical owner controls a workflow at a time. E7's state transaction, lease and epoch comparison, and operation journal must survive failover under the selected consistency guarantees. A **split brain** occurs when more than one coordinator believes it has authority over the same workflow. Epoch fencing rejects the stale coordinator at trusted state boundaries, but cannot undo a payment already initiated; the E5/E6 unique operation record and provider reconciliation remain necessary.

The **transactional outbox** from Chapter 15 commits an intended effect and its dispatch record with the workflow's authoritative state. Its consumer may deliver at least once; it must not equate delivery with exactly one external effect. Design provider calls around documented idempotency scope and expiration; when an outcome is ambiguous, suspend consequential retries until facts support the next action. Separate queues for advisory tasks and consequence dispatch if this helps keep a flood of model tasks from starving financial exception handling. Place provider status lookup, manual review and exception holds where accountable operations staff can reach them even during worker or coordinator outages.

Operational separation is also a deployment decision. E9 should receive logs and security events through independently controlled paths, with correlation on `CASE-204` and `RF-1042` but no credentials or unnecessary personal data in telemetry. Give operations an emergency *hold* capability that cannot itself make payments. Define accountable ownership for provider outages, reconciliation aging, tenant breaches and questionable financial outcomes. A regional outage test must show whether new dispatch is suspended, state restored, uncertain operations identified and no duplicate effect produced after recovery.

## 16.6 Evaluate alternatives as engineering decisions

A deployment design record should compare plausible alternatives against consequence, assurance and lifecycle economics. A smaller single-host deployment may be cheaper and easier to diagnose; a remotely separated execution boundary may provide stronger credential isolation and clearer segregation of duties, with network latency and operations cost. Neither option is automatically correct. The primary economic measure is the cost per **acceptable completed workflow**, including the cost of denial, reconciliation, investigation and support—not merely tokens or service instances.

| Decision dimension | Evidence to collect before approval |
|---|---|
| Authority and security | Threat model, privilege inventory, denied bypass tests, secret-custody review |
| Reliability and recovery | Failover, stale-epoch, outbox, unknown-effect and reconciliation fault tests |
| Business correctness | Provider contract verification, authoritative finance reconciliation, exposure aging |
| Operations and governance | On-call owner, runbook drill, retention, audit access, change/release approval |
| Efficiency | p95 end-to-end latency, resource contention, peak load, cost per acceptable completion |
| Adaptability | Versioned contracts, dependency replacement and portability of policy/state |

Record assumptions explicitly. A provider sandbox that acknowledges immediately does not prove production behavior after a partial commit. A cloud identity policy that passed inspection yesterday does not prove it remains enforced after a release. A release gate should run automated configuration and boundary checks, inspect the *deployed* identity/network/secret configuration, execute adversarial and crash tests, and obtain accountable human signoff on the residual risk. Deploy progressively and retain rollback or quarantine actions that do not require the model to cooperate.

Figure 16.3 traces the architectural contract through placement, enforcement and evidence. It is the final Part II view: it closes the loop to Figure 8.1 rather than replacing it with a fashionable infrastructure topology.

![Figure 16.3 — Part II closure: map each logical responsibility to deployment enforcement and independently reproducible acceptance evidence.](assets/shared-figures/rendered/F16-03.png){#fig:f16-03 width=5.75in}

## 16.7 Close Part II: one architecture, many implementations

The test of a coherent architecture is whether its invariants remain the same when we change a worker framework, model, deployment shape or provider. Across Chapters 8–16, E1 fixes who may initiate work; E2 fixes ownership; E3 remains advisory; E4 constrains evidence; E5 independently authorizes consequential action; E6 controls external integration; E7 makes recovery safe; E8 grounds business truth; and E9 makes the whole system inspectable and governable. **The nine domains are responsibilities, not nine products**, and the four layers of Figure 8.1 are boundaries to engineer, not a mandated call order.

For the $500 `CASE-204` request, A, B and C continue to differ in investigation, not payment authority. `RF-1042` remains the stable illustrative operation identity even if the coordinator dies or the payment outcome is temporarily unknown. The diagrammatic story is now complete: we can name the boundary, identify the component that enforces it, describe failure behavior, and demand test evidence. What remains is to choose patterns, build implementations, challenge them, and operate them responsibly. Part III begins that pattern-level work without promoting an architectural aspiration into a verified guarantee.

## Chapter exercises

1. **Deployment mapping:** Place nine E-domains on a single host and then across three isolated zones. Identify exactly which contracts and authority checks cannot change.
2. **Bypass audit:** Draw every possible network and credential path from E3 to the payment provider. Design a test that proves each unintended path is denied.
3. **Failure exercise:** The provider commits `RF-1042` but the response disappears as the coordinator fails over. Specify state, owner, evidence, permissible recovery and prohibited retries.
4. **Risk decision:** Compare Profile M and H for the $500 refund workflow using operational cost, latency, credential exposure, policy independence and residual risk. Defend a conditional selection.
5. **Part II architecture defense:** Return to Figure 8.1 and produce a one-page trace from `AUTH-01`, `PAY-03` and `OPS-01` to deployed enforcers, negative tests, evidence owners and release gates.

**Engineering checkpoint:** Can an independent reviewer trace every nine E-domains responsibility from Figure 8.1 to an actual deployed control, verify that no agent-controlled path bypasses E5, and reconstruct the external outcome of `RF-1042` without confusing a local observation with business truth?

**Sources and further reading:** NIST SP 800-207 (2020) informs zero-trust enforcement; NIST AI RMF (2023) informs governed AI risk treatment; Kleppmann (2017) informs distributed state and failure semantics; and Google SRE (Beyer et al., 2016) informs operational readiness. The L/M/H profiles and CASE-204 deployment contracts are ETIS engineering examples, not universal regulatory classifications.
