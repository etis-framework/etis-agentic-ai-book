# Chapter 25 — Build 3: Trusted Consequential Execution

Part IV: Progressive Reference Implementation

> **Engineering proposition:** A valid identity assertion can identify a bounded investigator without authorizing the investigator to issue a refund. Consequential effects require an independent, case-specific decision at trusted execution (E5), followed by durable intent and controlled dispatch. An in-process policy function is not a protected boundary.

## Learning objectives

After completing this chapter, readers should be able to distinguish authentication, resource scope and financial authorization; explain why even a signed advisory proposal is not business approval; build a bounded process-level enforcement boundary; validate case-specific approval before creating a durable refund operation; test a compromised investigator with a genuinely valid identity assertion; and identify which additional deployment and provider mechanisms remain necessary before a real $500 refund could be entrusted to software.

## 25.1 What the preceding builds have and have not proved

The recurring example is CASE-204, a customer complaint involving a proposed $500 refund. If independently authorized, trusted execution creates the stable consequential-operation identifier RF-1042. Build 0 established the deterministic shape of that financial operation. It checks a fixed policy, creates a durable local operation identity, atomically claims dispatch, and illustrates the separation between durable operational state (E7) and simulated authoritative payment truth (E8). Build 1 added a bounded agent-reasoning (E3) proposal under the advisory action-proposal contract (C04) that cannot invoke that payment path. Build 2 added a simulated admission-and-identity (E1) assertion and a scoped context/retrieval (E4) read under the context-query contract (C03) before the same review-only proposal. None of those exercises protected Build 0's payment functions from arbitrary Python executing as the same user. The Build 0 `authorize()` function receives a Boolean `approved` argument from trusted fixture code; calling it with `approved=True` is not proof of independent human or organizational approval.

Chapter 13 introduced trusted execution and authority (E5) as an independently governed responsibility, not merely a module named `trusted`. Chapter 16 distinguished logical boundaries from deployment isolation. Chapter 19 argued that a tool declaration or discovered API is not payment authority. Chapter 21 tied decisions to executable policy and evidence. Build 3 now makes that requirement testable across a separate service process. The question is not whether the model can recommend a refund. It is whether **the request can be denied at the consequential boundary even when the caller holds a valid identity assertion**.

The case remains CASE-204, tenant `retailer_a`, a possible $500 refund represented as exactly 50,000 cents. The trusted operation identity is RF-1042. Build 3 does not turn `ADV-TRACE-204`, `TRACE-204` or a customer statement into an operation identifier. Designs A/B/C remain alternative architectures; Design B remains a conditional initial production candidate, and Build 3 is not a requirement to advance to Design C.

## 25.2 Threat model: hijacked bounded investigator

Assume an attacker controls the bounded investigator's advisory request data and can submit requests through its permitted client interface. The attacker may carry a **genuinely valid Build 2 fixture identity assertion** scoped to CASE-204 and `EV-204`; may write convincing instructions or forged approval identifiers into C04 text; and may invoke the E5 request endpoint. It does not possess the separately issued, transaction-specific E5 approval grant. We test this adversary because a valid agent token proves neither a finance approver's decision nor an entitlement to use E6. Merely checking whether a Python file imports the payment module would not test the E5 boundary.

This exercise has a precise environmental limit. The E5 server runs in its **own operating-system process** and owns the only intended handles to the local E7 SQLite store and simulated E6/E8 adapter. The client communicates over a bounded Unix-domain socket. The instructor's harness starts both under the same OS user account and temporarily creates the fixture keys. That same-user arrangement is **not** a hardened hostile-runtime boundary: arbitrary host code with the same file permissions may read fixture files or bypass the toy socket service. Real deployment requires separate service identity, host/container access controls, key custody, authorization issuer isolation and incident controls. Consequently, the executable proof is an *independently evaluated request-path denial under the stated attacker capabilities*, not a claim of defense against full host compromise.

NIST SP 800-207 (2020) supplies broader resource-centric principles for authentication and access decisions; it does not specify or certify this fixture. OWASP agentic/GenAI guidance motivates compromised-agent and tool-misuse tests; our test result does not certify compliance with that guidance. The exact local grant design and operation contracts are ETIS educational constructs.

## 25.3 Map the modules to CAB-001 responsibilities

![](assets/shared-figures/rendered/F25-01.png)

*Figure 25.1 — Architecture and placement. C04 advice crosses no financial authority boundary on its own. A distinct E5 service process validates E1 scope and a separate transaction-specific grant before E7 records the durable RF-1042 intent, E6 claims dispatch, and mock E8 records the simulated provider effect. The process boundary is demonstrable; same-user host isolation is not claimed.*

E1/C01 supplies a signed **fixture** identity assertion with issuer, subject, tenant, case, purpose and expiry. E4/C03 continues to provide source-limited, provenance-bearing contextual evidence in Build 2. E3/C04 continues to emit an untrusted review proposal. E2 remains a single-case local caller; there is no distributed coordinator lease or fencing epoch. E5 owns independent approval verification, the fixed authorization policy, and the consequential API surface. C05 governs the trusted-action request, C06 covers durable E7 operation intent, C07 governs controlled E6 dispatch, and C08 differentiates the E8 business-system observation. E6 remains the simulated payment-dispatch adapter retained from Build 0; E8 remains mock provider business truth. E7 holds the local, durable operation ledger, while E9 receives executable negative tests and development-stage review evidence. The chapter does not silently replace CAB-001's C05–C09 definitions with the names of Python files.

The new `build3/` source-level `architecture.svg` is embedded in its README. It maps the client, service, contract and fixture modules to these logical obligations. Read it alongside Figure 25.1: a module diagram answers *where is the code?*; the book figure answers *which responsibility controls the financial effect?* Neither proves an actual production authorization service without the implementation and deployment evidence.

## 25.4 The E5 request and approval contract

The client request is a bounded, versioned teaching envelope containing `action`, `case_id`, `tenant_id`, `amount_cents`, `agent_assertion`, `approval_grant`, and `simulate_outage`. The test-only outage flag is not an acceptable production financial API field. The server rejects unknown fields, wrong types, booleans disguised as monetary integers, excessive or malformed payloads, and mismatched tenant, case or amount. It validates the E1 assertion with its own verifier using the fixture key, not a caller-supplied `VerifiedScope` object. Critically, passing that identity check **does not** authorize a payment.

The independent approval artifact is a signed, canonical, time-bounded grant with the intended case, tenant, exact amount, policy version, finance approver, approval identifier and issued/expiry times. The grant is created by a separate **trusted demonstration harness**, not by a C04 adviser and not through an E5 `approve` endpoint. The E5 service independently checks its integrity, expiry and fixed authorization fields. A client-supplied `APP-204` string, a persuasive C04 explanation, and the operation ID RF-1042 are each rejected as substitutes for the approval grant. This deliberately separates **correlation**, **identity**, **business approval**, and **financial operation**.

The use of fixture HMACs makes the exercise credential-free and verifiable, not a production key-management design. The local issuer and verifier are under the same test user; a true approval issuer requires independent role and key custody, purpose and audience binding, authenticated reviewer decisions, grant cancellation/revocation, anti-replay and case-specific policy evaluation. Replaying an already consumed grant cannot create another refund in this fixture because E7 enforces a one-time operation claim; durable grant-use tracking and its multi-site consistency are additional production concerns. A stolen grant in a real system must not become a bearer capability without appropriate binding and revocation controls.

## 25.5 Independent execution, state and errors

![](assets/shared-figures/rendered/F25-02.png)

*Figure 25.2 — Behavioral sequence. A hijacked investigator with a valid identity assertion is denied without finance approval. The distinct finance-issuer lane identifies the **fixture grant origin**, not a production approval service or a separate direct IPC call; the demonstration harness assembles the independently issued grant into the client request to E5 (no direct finance-to-E5 call), after which E7 prepares RF-1042 before one controlled simulated dispatch.*

Inside `service.py`, the service owns its request parser and the only import of Build 0's `refund` module. The unprivileged `client.py` owns neither a payment adapter nor a grant issuer. On any identity or approval failure, the E5 process returns `DENIED` **before** initializing E7 or mock E8. That ordering matters: negative tests inspect the actual absence of both databases rather than merely accepting a message claiming that nothing happened.

Only after independent verification does E5 invoke the inherited deterministic `prepare()` operation. The local operation RF-1042 is immutable and scoped to CASE-204; `dispatch()` atomically claims its E7 transition before the simulated provider call. A second request—whether sequential or concurrent—cannot obtain another authorized dispatch of the same operation. The test suite checks that the provider fixture contains one refund, not merely that the endpoint returned one success. These guarantees are within the single service process, local SQLite constraints and one mock provider. There is no claim of exactly-once delivery across an arbitrary real payment network.

The response categories deliberately distinguish `DENIED`, `CONFIRMED`, and `UNKNOWN`. An invalid request or absent approval is a denial with no new intent. An approved local fixture request may confirm the mock provider result. An injected outage or conflicting provider observation *after the durable E7 dispatch claim* returns `UNKNOWN`; the E7 record remains `DISPATCHED`, and subsequent attempts cannot initiate another dispatch; E5 continues to report uncertainty. This is an **unresolved operational state**, not proof that the external effect failed. Build 0's reconciliation lesson still applies. Chapter 26 will introduce provider-specific contract modeling and reconciliation without inventing a fresh operation identity.

The client also treats an interrupted or malformed service response as `ServiceUnavailable`, with explicit uncertainty. It does not silently resend a financial request. The service bounds JSON lines, closes client sockets and handles recognized invalid requests without leaking keys, database paths or customer content in responses. Build 3 applies a monotonic total request-framing deadline and bounded reads; a peer disconnect or a stalled/incomplete frame is contained at the connection boundary rather than terminating E5. The service remains single-worker, however: one malicious connection can occupy it for up to the bounded deadline, and bursts exceeding its capacity may queue or time out. The tests prove subsequent service after abort, incomplete frame, slow trickle and oversized input; they do not establish load capacity or availability under sustained attack. Production would additionally require concurrent admission with explicit worker/resource quotas and backpressure, per-principal controls, confidential and authenticated transport, safe structured audit trails, health monitoring, graceful shutdown and restart drills.

## 25.6 Run Build 3: credential-free positive and negative cases

From the edition-matched repository root, using Python 3.10 or newer, run the following commands independently. The `compromised` demonstration intentionally returns exit status 2; it is not a failed installation. The demonstration creates temporary fixture keys and databases and removes them on normal exit. No cloud account, LLM SDK or real payment credentials are required.

```sh
python3 examples/refund-reference-system/build3/demo.py \
  --scenario compromised
python3 examples/refund-reference-system/build3/demo.py \
  --scenario approved
python3 examples/refund-reference-system/build3/demo.py \
  --scenario tampered
python3 examples/refund-reference-system/build3/demo.py \
  --scenario outage
python3 -m unittest discover \
  -s examples/refund-reference-system/build3 \
  -p 'test_*.py' -v
```

The compromised case prints `DENIED` and reports that neither E7 nor mock E8 was created. The approved case prints `CONFIRMED` with RF-1042 and both local fixture files present. A tampered grant is denied. An outage returns `UNKNOWN` while preserving E7's unresolved dispatch. The tests additionally exercise valid-token denial, forged C04 authority strings, cross-tenant and malformed requests, expired or modified grants, a missing/forged identity assertion, concurrent replay, interrupted IPC, malformed JSON, and the independently confirmed one-effect limit. Runs of Builds 0, 1 and 2 remain separate; their tests and entry points do not depend on Build 3.

One intentionally revealing negative test submits a valid Build 2 token to E5 with no grant. The test first verifies that token against its fixture issuer and only then attempts the refund. E5 nevertheless rejects the request and does not create RF-1042. That is materially stronger than a test which passes a literal string called `VALID_TOKEN`, or one which only scans E3 source for imports. It directly tests **identity validity without transaction permission**.

## 25.7 Decision diagram and falsifiable evidence

![](assets/shared-figures/rendered/F25-03.png)

*Figure 25.3 — Decision representation. Schema, E1 fixture identity and independent E5 approval all gate operation creation. Every failure exits without RF-1042; an uncertain post-dispatch outcome requires reconciliation.*

The evidence matrix in `examples/refund-reference-system/TESTING.md` states, for each scenario, the request category, E7 record, mock E8 record, and what is—and is not—proven. Use the matrix rather than treating a successful test count as assurance by itself. A valid E1 token without approval must leave no operation, a tampered approval must fail before state creation, a reviewer-approved request must cause one fixture operation, and a dispatch interruption must retain uncertainty rather than authorize a retry. These are testable claims about this implementation; they are not assertions about any real payment provider.

In an enterprise design, the confidence argument would be larger: independent E1 and finance-approval issuers, OS-level process and key isolation, credentialless E3, credential custody exclusively within E5/E6, continuous authentication and authorization, durable approval-use state, revocation, audit logs, E2 ownership fencing if distributed, provider idempotency specifications, adverse concurrency and crash tests, and verified production incident containment. Security evidence should specifically show what happens when the agent executes adversarial code rather than merely submits hostile input. Chapter 29 extends the hijacked-agent threat case; Chapter 31 evaluates system-level negative assurance evidence. Neither chapter should presume that Build 3's test harness supplies production guarantees.

## 25.8 Engineering judgment: when to deploy the gate

Consider an enterprise where advisory reasoning saves an investigator two minutes but every refund still requires an authorized payment decision. The marginal value of Build 3 is not an increase in model autonomy; it is a separately enforced financial decision that remains valid regardless of which model or investigator recommended the refund. That supports Design B's conditional suitability without requiring a Design C worker hierarchy. The engineering team still must budget approval service availability, key rotation, audit retention, denial review, recovery operations, and any latency introduced by an independent boundary. A simple rules-driven Design A can reuse the same trusted gate.

A release review should decline any proposal that relies on prompt instructions such as “do not call the payment API” as its only enforcement. Likewise, deploying `service.py` as another process under the same user, with readable grant keys, must not be represented as a defended security perimeter. The production decision hinges on the actual privilege and credential boundary, tested against the adversary that could reach it. Governance is architecture because permission must affect the executable financial path, not merely be recorded after the fact.

**Multi-perspective architecture review.** The **implementing engineer** demonstrates malformed-request containment, bounded IPC behavior and error-handling tests. The **enterprise architect** traces advisory C04 through the independently evaluated E5/C05 path and confirms there is no E3-to-E6 shortcut. **Security and assurance** challenge the valid-token attack and the shared-OS-identity fixture limitation. **SRE/operations** demand reproducible evidence for disconnects, stalled clients and UNKNOWN provider outcomes. The **business owner** identifies the accountable finance approver and weighs the operational cost of a protected execution service. A role may cover more than one perspective; none of these observations alone constitutes payment approval or production release.

## 25.9 Professional exercises and review standard

1. **Threat-model.** Let a compromised investigator hold a valid E1 assertion for CASE-204. Identify which claims remain true, which permission is missing, and what executable denial evidence you would require.
2. **Verify.** Run the negative grant and wrong-tenant tests. Inspect the E7/E8 files (or their absence) rather than only the response text. Explain why a string labeled `APP-204` is not a valid approval.
3. **Recover.** Inject a provider outage after the E7 dispatch claim. Explain why `DISPATCHED` must remain unresolved and why a second request with the same approval grant must fail.
4. **Deploy.** Propose an OS-level privilege split and credential distribution in which E3 cannot read the grant issuer's keys, E5's storage or E6 provider credentials. Define how to test host-level isolation.
5. **Defend.** Compare the incremental costs and protections of the Build 3 request boundary with simply importing Build 0's policy function into a model-driven agent. State which benefits the business owner can verify.

**Review standard:** Passing this chapter requires a clear distinction among proposal, identity, approval, durable intent and confirmed effect; a genuine valid-token denial at E5; and an explicit statement of the same-user fixture threat boundary. The source, tests, diagrams and claims should agree. A good demonstration does not itself authorize release of financial software.

## Sources and bridge to Chapter 26

NIST SP 800-207 (2020) informs independent, resource-centered trust evaluation; the textbook's CAB-001 and Chapters 9, 13–16, 19 and 21 supply the specific E1/E5/E6/E7/E8 design argument. Gray and Reuter (1992) and Kleppmann (2017) motivate the transaction, duplicate-claim and unknown-outcome treatment. OWASP GenAI and agentic guidance motivates the adversarial test surface, but does not certify this fixture. The implementation contracts and test expectations here are original ETIS teaching artifacts; the source register retains external claim-to-page and exact-edition verification as open publication gates.

Chapter 26 now asks what happens when the protected E5 decision crosses a **real provider contract boundary**: which idempotency and lookup guarantees actually exist, how UNKNOWN is reconciled, and what evidence would permit an operator to close or repair a financial operation. A stronger policy gate is necessary, but it cannot make an external network atomic with E7.
