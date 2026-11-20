# Chapter 36 — Exercises, Reviews, and Adoption Roadmap

Part VII: Reference and Application

> **Engineering proposition:** An agentic-AI system earns authority through independently verified controls, credible operating evidence, and accountable decisions—not because an agent can produce a convincing plan or a demonstration appears successful. The final test is whether a team can defend what the system may do, what it must refuse, and how it behaves when evidence is incomplete.

## Learning objectives

After this chapter, the reader should be able to defend a bounded agentic architecture against a deterministic alternative; trace a consequential recommendation to independent authorization, durable intent, provider truth and review evidence; devise negative tests that falsify unsafe claims; decide whether to pause, reconcile, restore, or retire an ambiguous workflow; and present an accountable adoption recommendation whose technical and economic claims match the evidence available.

## 36.1 The integrated engineering review

Return to **CASE-204**, a customer case involving a possible **$500 refund**. An investigation may yield a recommendation, but the consequential operation **RF-1042** is a trusted financial effect controlled independently of the agent. **Design A** is the deterministic workflow. **Design B** adds bounded artificial-intelligence (AI) advice while leaving consequential authorization outside that advice. **Design C** optionally introduces specialist agents and bounded coordination; it does not grant those agents payment credentials. The six companion Python builds are independently executable teaching checkpoints, not a production service or a single fully composed runtime.

The nine logical responsibilities remain stable: admission and identity (E1); durable coordination and ownership (E2); advisory reasoning (E3); scoped context and provenance (E4); independent trusted execution (E5); restricted provider integration (E6); durable operational state (E7); authoritative provider and business truth (E8); and governance and assurance (E9). The nine contracts C01–C09 describe the handoffs among these responsibilities; Chapter 8 and Appendix A are the normative lookup, while Chapter 35 maps claims to available demonstrations. The labels are logical architecture identifiers, not proof of separate hosts, secret custody, or provider authorization.

The integrated review begins with *competing hypotheses*. A team may claim that Design C increases investigation quality; another may contend that Design B supplies enough decision support with less coordination risk; a third may prefer Design A because the workflow's uncertainty and cost do not justify a model. All three positions are plausible until supported by evidence. The obligation is not to prefer agents. It is to select the simplest adequate mechanism that satisfies the business objective and control constraints.

**Table 36.1 — Capstone review packet: the question that each artifact must answer**

| Artifact | Required engineering answer | Primary reference |
|---|---|---|
| Architecture decision record | Why A, B or C; what work stays deterministic; what autonomy is prohibited? | Chapters 7–8, 17; Figure 36.1 |
| Trust-boundary trace | Where does an untrusted recommendation stop and independent spending authority begin? | Chapters 13, 25, 29; Appendix A |
| Failure and recovery trace | What remains true after a lost acknowledgment, lease expiry or disputed outcome? | Chapters 26–28; Figure 36.2 |
| Evidence and operations packet | Which test falsifies the safety claim; who can contain and restore? | Chapters 30–33; Appendix C |
| Lifecycle decision | Is the cost per acceptable completed workflow credible, and when do we retire? | Chapter 34; Table 36.3 |

A reviewer must reject an artifact if it merely repeats a policy adjective such as *secure*, *robust* or *human-in-the-loop*. Require an enforceable decision point, specific input and failure case, observable denial or safe state, named evidence and owner, and a limitation statement. A model-generated audit summary is not independent audit custody.

![](assets/shared-figures/rendered/F36-01.png)

*Figure 36.1 — Integrated review chain: proposed agentic behavior is assessed against independent authority, adverse-case evidence, operational readiness and an accountable adoption gate. The chain is a review method, not an implemented release controller.*

## 36.2 Exercise A: choose the boundary before choosing the model

**Scenario.** The business asks for shorter refund resolution time. A product team proposes a supervisor that can dispatch specialist investigators, summarize records and call a payment tool. The evidence supplied includes a polished transcript and an average model response time. No measured acceptable-outcome rate, staff-review capacity, adversarial denial evidence or provider-reconciliation contract is supplied.

**Task.** Write a one-page architecture decision record comparing Designs A, B and C. State which work is deterministic, what E3 may propose, what E4 can retrieve, who owns E2 workflow state, and where E5 can independently deny. Specify a minimum pilot, a no-go condition and the observation that would reverse your choice. If selecting C, justify the additional coordination and ownership failure modes rather than citing agent count or a successful demonstration.

**Defensible answer criteria.** A conditional Design B pilot is reasonable when bounded advice offers an identifiable benefit and E5 remains independently controlled. Design A is equally defensible if measured benefit is insufficient; Design C requires evidence that specialists materially improve acceptable outcomes. None may grant the investigation supervisor provider credentials. The proposal's payment-tool shortcut is rejected even when faster. Source navigation: `examples/refund-reference-system/build1/README.md` and `build3/README.md` (paths under the companion root). Those builds demonstrate separate parts of the story, not an integrated release candidate.

## 36.3 Exercise B: attack the most attractive shortcut

**Scenario.** A compromised investigation worker presents a syntactically valid service token, a persuasive $500 refund explanation, and an `approver` field inserted into an advisory payload. It attempts to create RF-1042 through a payment-adapter interface. An internal reviewer argues that authentication plus a human-looking field should be enough for a low-dollar refund.

**Task.** Trace the advisory action-proposal contract (C04) into the independent authorization decision (C05). Identify the earliest enforceable denial and list evidence necessary to refute the claim that a valid token carries transaction authority. Include a negative test for wrong tenant, wrong case, amount mismatch or expired approval; identify which guarantee cannot be established by a same-user fixture. Explain why E6 provider credentials cannot be present in the agent's reachable execution context.

**Defensible answer criteria.** Identity proves the presenting principal, not authority for this financial transaction. An E3-supplied `approver` string cannot create a trusted approval. E5 must authenticate its own grant issuer and evaluate tenant, case, amount, action, expiry and revocation policy before a trusted effect is claimed. The Build 3 subprocess fixture and `security/README.md` demonstrate local denial; they do **not** demonstrate independent production key custody or a network-isolated privileged payment service. A passing positive-path refund is not a substitute for a failing malicious-path test.

## 36.4 Exercise C: recover without producing a second effect

**Scenario.** After independent approval, E5 records durable intent for RF-1042 and sends the first provider request. Its acknowledgment is lost. Meanwhile the worker's E2 lease expires; a replacement coordinator becomes owner. The provider may have completed the refund, but local state says `UNKNOWN`. The new coordinator proposes retrying immediately under a fresh operation identifier.

**Task.** Construct a recovery decision record containing the original operation identifier, durable intent, prior dispatch claim, owner epoch, last trusted provider observation, pending inquiry and the authority for any future state transition. Decide whether to send, query, pause or escalate. Describe a crash-point test and show which record prevents two refunds from appearing as one successful workflow.

**Defensible answer criteria.** Preserve RF-1042 and reconcile its original provider operation through the read-only inquiry path before contemplating any new effect. A new coordinator may take over bounded investigation work but cannot erase the previous effect history. `UNKNOWN` means unresolved, not failed. Build 4 demonstrates a local ledger and mock provider inquiry; Build 5 demonstrates local ownership and fencing but **does not independently validate the current E2 ownership epoch inside E5**. A production design must close that gap with trusted current-owner validation and fenced consequential dispatch; no second provider operation is justified by the educational test alone.

![](assets/shared-figures/rendered/F36-02.png)

*Figure 36.2 — Recovery challenge decision: preserve original trusted intent, obtain authoritative provider evidence, and quarantine the route if the original outcome remains uncertain. A new lease or a rollback is never permission for a new refund.*

## 36.5 Exercise D: defend a release under attack and uncertainty

**Scenario.** A canary of the refund investigation workflow passes its ordinary unit tests. During adversarial testing, an investigator can submit a plausible but unauthorized action proposal; the E5 fixture denies it. In a separate failure injection, provider status remains unavailable after acknowledgment loss. An operations team can pause new admissions, but no independent production approval issuer, E5-side owner-epoch enforcement, live provider agreement or protected audit sink has been demonstrated.

**Task.** Assemble a release review: claim, evidence, unresolved limit, risk owner, stop trigger and restoration authority. Distinguish *deploying the learning fixture*, *running a constrained enterprise pilot* and *activating live financial effects*. Define the observable event that would suspend new financial work, the state that must be reconciled before resumption, and who signs the decision. Use the release manifest in Chapter 33 as a **proposed production artifact**, not a Python feature already present.

**Defensible answer criteria.** The local fixture may be suitable for training and preproduction assurance. It is not sufficient evidence for live money movement. The valid-token denial is positive evidence for one local control, while independent credentials, external provider reconciliation, custody, current-owner enforcement, and organizational authorization remain external prerequisites. Rollback may stop new routing, but cannot roll back a completed refund or safely replay an unknown one. Runbook 30-A covers incident response, Runbook 32-A governance suspension and restoration, and Runbook 33-A release intervention. These are illustrative operating procedures, not executable automation.

## 36.6 Exercise E: test the economics without pricing away safety

**Scenario.** A sponsor claims that Design C is cheaper because its model calls cost less per investigation. The proposal omits escalation labor, review queue delay, duplicate investigation, incident response, assurance work, recovery of unknown outcomes and the cost of retiring an unsafe service. The team has no measured acceptable-outcome denominator.

**Task.** Present a sensitivity model comparing Designs A/B/C over the *same eligible workflow population*. Include the cost of human review, model and tool use, infrastructure, independent controls, failed or repeated work, provider reconciliation, operational response and governance. Model a capacity bottleneck and a downside scenario without inventing empirical rates. State the decision to pilot, restrict, scale, replace or retire, and the evidence that would cause revision.

**Table 36.2 — Decision evidence for an adoption recommendation**

| Gate | Acceptable evidence | Mandatory stop or qualification |
|---|---|---|
| Authority | Independent finance policy, approved scope, demonstrated denial | Any agent-controlled path around E5 is a no-go |
| Outcome | Measured acceptable resolutions, exclusions and counterfactual baseline | Model-call count is not an outcome denominator |
| Recovery | Original-operation state, provider observation, tested unknown handling | Unresolved `UNKNOWN` forbids blind replay |
| Operations | Containment authority, observed signals, restoration decision | A dashboard without response authority is insufficient |
| Economics | Comparable lifecycle unit cost, capacity, sensitivity and downside | Cheap inference cannot price away a missing hard control |

The **cost per acceptable completed workflow** (Chapter 34) is a decision metric only after the denominator and workload mix are defined. An economic estimate cannot make an unsafe authorization architecture acceptable. A lower-cost deterministic design may win; the book does not presume agent adoption. No companion build contains measured enterprise return on investment or real release telemetry.

## 36.7 Exercise F: assemble the final assurance case

The capstone submission is not a presentation about AI potential. It is a **reviewable engineering packet** that a second team could challenge. Table 36.3 defines the minimum acceptance rubric; it is an authorial evaluation aid, not an external certification standard.

**Table 36.3 — Capstone acceptance rubric**

| Dimension | Evidence required for a defensible submission | Unacceptable shortcut |
|---|---|---|
| Architecture and scope | Selected Design A/B/C, alternatives, contract owners and trust-boundary diagram | “Multi-agent” as the sole justification |
| Implementation | Exact source, README and test paths; executed-versus-specified labels | Claiming Build 5 is a composed production stack |
| Security | Unauthorized and valid-token-negative cases, independent financial gate | Treating identity or prompt rules as payment authority |
| Reliability | Unique operation, durable intent, status inquiry and unresolved-state control | New operation ID after an unknown acknowledgment |
| Operations and governance | Stop/restoration criteria, release evidence, named decision rights | Human signoff that bypasses technical enforcement |
| Value and adoption | Credible denominator, lifecycle cost, review capacity and retire trigger | Optimizing only inference spend |

The corresponding reader entry point is `examples/refund-reference-system/README.md`; its `IMPLEMENTATION_EVIDENCE_MAP.md` separates the build demonstrations. The focused evidence paths are `build3/README.md`, `build4/README.md`, `build5/README.md`, `security/README.md`, `reliability/README.md`, `operations/README.md` and `assurance/README.md`, all relative to the companion root. Appendix B collects these entry points, and Appendix C defines evidence limitations. Teams should rerun the tests, inspect actual source behavior and retain command outputs and version identifiers. A checkmark without the source version, test scope and observed result is not an assurance argument.

A satisfactory capstone also states what remains unproved: protected production identity and keys, issuer revocation, E5 current-owner enforcement, real provider settlement and idempotency behavior, distributed audit custody, measured economics, and live release or restoration drills. The educational fixtures are purposeful falsifiers, not production certification. Local tests support only the guarantees they actually exercise.

## 36.8 Adoption roadmap and final engineering judgment

Adoption proceeds through **bounded evaluation**, **production-hardened domain deployment**, and only then **reusable enterprise capability**, with independent decision gates between stages. During evaluation, compare Design A to B under representative cases, require a working denial story and quantify acceptable outcomes rather than novelty. Before consequential deployment, establish independently protected policy and provider credentials, durable recoverable state, operational ownership, evidence retention and a live incident plan. Reuse across domains only after contracts, tenancy, policy changes, monitoring and human-accountability responsibilities remain enforceable under scale and failure.

A decision to **defer or retire** is a legitimate engineering success when value is not demonstrated, controls cannot be implemented, review queues are unsustainable, or recovery obligations cannot be met. Retirement itself requires stopping admissions, resolving or preserving outstanding unknown effects, retaining auditable records and revoking capabilities—not just deleting a model endpoint. The responsible owner records the decision, supporting evidence, residual exposure and reentry conditions.

The closing principle is operational rather than rhetorical: **AI proposes; engineers verify.** Models can investigate and produce useful artifacts. Trust comes from bounded authority, independent enforcement, recoverable consequences, observable behavior, defensible evidence and accountable human governance. A convincing demonstration starts the engineering conversation; it does not finish the proof.
