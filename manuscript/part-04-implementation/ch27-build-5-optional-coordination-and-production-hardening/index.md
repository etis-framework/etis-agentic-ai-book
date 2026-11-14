# Chapter 27 — Build 5: Optional Coordination and Production Hardening

Part IV: Progressive Reference Implementation

> **Engineering proposition:** Coordination can preserve bounded ownership and recover unfinished work, but it cannot authorize a financial effect. A lease is not an approval; a new worker is not entitled to create a new refund; and a stale worker must not be allowed to overwrite authoritative workflow state.

## Learning objectives

After completing this chapter, readers should be able to decide whether a single-controller workflow requires optional coordination; implement durable ownership with leases and monotonically increasing fencing epochs; preserve one initial consequential-operation attempt across crashes and replacements; distinguish locally fenced coordination from end-to-end enforcement at the execution boundary; test hostile, stale and concurrent workers; and specify the remaining controls and evidence needed for a real production deployment.

## 27.1 Why introduce a coordinator at all?

The running case remains **CASE-204**, a replacement complaint involving a proposed **$500 refund**. Its independently authorized consequential operation, **RF-1042**, is created by trusted execution, never by advisory reasoning or coordination. Builds 0–4 already establish a useful alternative without a distributed coordinator: a deterministic refund baseline, bounded advisory proposal, scoped context, separately evaluated financial approval, and controlled provider reconciliation. Those capabilities need not evolve toward a multiagent system.

Chapter 26 introduced the enterprise integration (E6) provider contract, durable operational state (E7), and simulated authoritative provider truth (E8). Its separate trusted-execution-and-authority (E5) process refuses a valid admission-and-identity (E1) assertion when transaction-specific finance approval is missing. This chapter asks a narrower question: **what changes when work can be owned and resumed by different workers?** Coordination and durable ownership (E2) supplies that answer. The E2 work-assignment contract (C02) is distinct from the advisory action-proposal contract (C04), trusted-action request (C05), and durable-operation and provider-observation contracts (C06–C08).

A single sequential controller is often the simplest adequate choice. Introduce an E2 coordinator when the business actually needs recoverable multi-worker processing, long-running parallel investigation, or controlled replacement of failed workers. Every extra worker and handoff adds failure modes: duplicated effort, expired leases, split-brain claims, stale decisions, unnecessary cost, and harder incident diagnosis. A workflow that gains no measurable throughput, latency, availability or serviceability benefit from coordination should probably keep the simpler topology.

Design A remains a deterministic alternative, Design B remains the conditional initial production candidate with bounded AI advice and independent review, and Design C remains optional bounded investigation. **Build 5 is a teaching checkpoint for coordination, not an autonomy level or mandatory production upgrade.**

## 27.2 The architecture: where ownership belongs

A coordinator does not possess the payment provider credential, approve a refund, or become the financial system of record. The fixture records the case, the fixed operation identifier, the current worker, lease expiration, epoch, workflow phase and last observed progress. The trusted E5 process still decides whether a specific transaction is authorized. The E7 operation ledger still owns payment intent and its state. The E6 adapter, not E2, owns the simulated provider call; E8 remains the independently recorded external outcome. Enterprise governance and assurance (E9) supplies accountable ownership, change control and tested containment rules.

![](assets/shared-figures/rendered/F27-01.png)

*Figure 27.1 — Optional coordination surrounds rather than replaces the financial boundary. The E2 lease and epoch govern local workflow ownership; E5 independently checks identity and finance approval; E7 persists intent before E6 sends to mock E8. The fixture does **not** claim that E5 or E6 currently validates the E2 epoch.*

The implementation reflects those logical contracts without inventing a nine-service deployment. `build5/coordinator.py` owns one SQLite work table and a transaction-scoped lease/epoch; `runner.py` chooses between a first `execute` request and later `reconcile` requests. Its only consequential interface is the existing Build 4 E5 socket client, invoked through a narrow injected callable. `demo.py` runs the actual Build 4 E5 subprocess with temporary fixture keys; `test_coordination.py` verifies concurrency, state transitions, stale-worker rejection and recovery. The source-level `build5/architecture.svg` is embedded in the build README, with actual file/module dependencies and explicit non-guarantees.

The distinction between **logical subsystem**, **Python module**, **process**, and **trust boundary** matters. E2 and E5 are architectural responsibilities. The E2 code runs locally and E5 runs in a separate subprocess, but the demonstration creates both with one OS identity. A malicious process with the same file privileges could read fixture material. This is neither protected credential custody nor multi-site fencing. The architecture figure and tests establish exactly the smaller local claim described below.

## 27.3 Durable case ownership, leases and epochs

Build 5 initializes a single persistent coordination record for CASE-204 and records the immutable consequential-operation identifier RF-1042. An eligible worker may acquire the record when it is unowned or the previous lease has expired. A successful acquisition advances a strictly increasing **ownership epoch**. Within one SQLite `BEGIN IMMEDIATE` transaction, the coordinator checks the prior owner and expiration, updates the lease, and commits the new epoch. Concurrent acquisitions therefore cannot both win in this single SQLite database.

A worker presents its identity, epoch and expiration to every E2 mutation. A stale or expired token is refused, even if the caller still believes it owns the work. A heartbeat may extend a current lease while preserving its epoch; the previous lease token ceases to match after extension. The fixture injects integer time values to make expiration tests deterministic. Real deployment requires a trusted clock policy, bounded skew assumptions, durable store availability, operation-specific timeouts and audit of ownership transitions.

**Fencing is enforced where the protected mutation occurs.** Build 5 currently enforces fencing at **E2's own SQLite state transitions**. It does not transmit an E2 epoch to the existing Build 4 E5 API, and E5 does not consult the E2 owner table. Consequently, the fixture does **not** prove that a stale worker holding an otherwise valid finance grant could not send an E5 request. E5's independently validated approval and E7's one-time dispatch claim remain separate protections. In an actual multi-worker design, E5 must verify a current, authoritative workflow owner/epoch where relevant and reject a stale work instruction at the consequential boundary. A lease token checked only in an untrusted coordinator is not adequate end-to-end fencing.

The ownership record is a coordination aid, not a claim about payment settlement. If it says `CONFIRMED`, it means the runner observed E5's `CONFIRMED` response under its current lease. The authoritative refund evidence remains E7 and mock E8, subject to the actual provider contract. If the E2 record and E7/E8 disagree, operators reconcile against the trusted records rather than allowing E2 to overwrite them.

## 27.4 Commit one attempt before contacting E5

The central recovery hazard is not only two workers running simultaneously. It is the interval between **starting a consequential request and knowing its outcome**. A worker might persist a plan, send an approved operation, and crash before seeing the response. A replacement cannot infer that the provider call failed. Even if E7 has no matching row, a coordinator must not casually issue a new refund request after an ambiguous interruption.

Build 5 makes a deliberately conservative choice. Before making the first `execute` request to E5, it commits E2 state `EXECUTE_IN_FLIGHT`. This does not create RF-1042 and is not permission for a refund; it records that an execution call *may* have started. The runner then calls E5 using the original, separately approved request. If the response is missing, malformed, delayed or explicitly UNKNOWN, E2 records `NEEDS_RECONCILIATION`. A successor may use only the E5 `reconcile` action, never another `execute`. If the crash occurred **after E2 committed but before E5 was called**, the conservative behavior may require manual resolution of a case for which no payment was even attempted. That loss of automated progress is intentional: this teaching example favors no duplicated financial effect over optimistic recovery.

![](assets/shared-figures/rendered/F27-02.png)

*Figure 27.2 — One logical work attempt across an interrupted worker and an epoch-changing takeover. The successor is constrained to status-only reconciliation or escalation; a replacement epoch is not a new financial operation identity.*

The outcomes remain distinct. An E5 `DENIED` during an initial execution is recorded as `DENIED` in E2 without inventing a provider effect. `UNKNOWN` remains unresolved. A later status-only reconciliation may produce `CONFIRMED` if E5 validates provider proof. If the reconciliation request is denied because its short-lived finance grant expired, Build 5 records `ESCALATED`—**not payment failure**. This preserves Chapter 26's explicit limitation: a real long-running recovery process needs an independently governed **read-only recovery authorization**, not indefinite replay of the original transaction approval. Build 5 does not silently create that permission.

## 27.5 A bounded decision procedure

The runner accepts the current E2 ownership token and selects exactly one of three outcomes: `execute` when its durable state is `READY`, `reconcile` when execution may have begun, or `none` when the workflow has reached a terminal or escalated state. For `execute`, it first commits E2 intent, then calls E5. On timeout, transport error or a purported confirmation lacking the correct CASE-204 / RF-1042 identifiers, the only safe claim is that the E5 result is unknown. There is no loop that asks an agent to improvise another payment command. The runner's action selection is deterministic and bounded; the agent's advisory proposal does not participate in the ownership algorithm.

![](assets/shared-figures/rendered/F27-03.png)

*Figure 27.3 — Decision controls for ownership and E5 action selection. A stale E2 lease cannot modify coordination state; first execution requires a durable E2 intent; all subsequent unresolved work uses E5 status-only reconciliation or escalation. E5 remains the independent financial authority.*

This arrangement avoids conflating three different ideas often all called “idempotency.” The E2 lease and epoch control **who may update a workflow record**. The E7 atomic dispatch claim controls **whether the local payment operation can start another send**. The mock E8 provider uniqueness constraint models **one provider-side effect per stable operation key**. Each guarantee has a different owner, failure scope and proof obligation. Passing one does not imply the others. A production deployment must validate all three at their actual trust boundaries, including any multi-site transitions and provider retention rules.

For hostile or malfunctioning workers, the E2 API rejects malformed worker identities, invalid clocks, stale epochs, expired leases, wrong state transitions and illegal result categories. The storage transaction closes its SQLite connection even after an exception. Competing workers are tested with parallel attempts against the same file. The demonstration does not claim resistance to a malicious same-UID actor rewriting the SQLite files, clock manipulation, sustained request flooding or compromised E5 credentials.

## 27.6 Reproduce the evidence

From the book repository root, open the Build 5 README and inspect its embedded architecture diagram. The example uses only Python 3.10+ standard-library dependencies and Unix sockets on macOS/Linux. There are no cloud credentials, real customer records, external LLMs or live payment services.

```sh
cd examples/refund-reference-system/build5
python3 demo.py --scenario approved
python3 demo.py --scenario denied
python3 demo.py --scenario lost-ack
python3 demo.py --scenario outage
python3 -m unittest discover -s . -p 'test_*.py' -v
```

In `approved`, E2 records one initial attempt, E5 independently validates the short-lived fixture finance approval, and E7/mock E8 confirm one RF-1042 effect. In `denied`, the investigator's otherwise valid identity assertion does not authorize financial execution. In `lost-ack`, the mock provider commits while E2/E7 initially remain uncertain; a new E2 worker takes over under a larger epoch and requests **reconciliation only**. In `outage`, no mock E8 record exists, but the worker still has no right to send again. Read the exact test assertions before using these results as release evidence.

The unit suite covers competing lease acquisitions, takeover fencing, renewal, wrong worker, stale and expired commits, invalid identity shape, one-time intent, crashes before an E5 call, unknown response categories, missing provider proof, denied reconciliation and actual subprocess integration. The tests use deterministic injected fixture time for E2, while the running E5 process checks its own short-lived grant using the real clock. These are test fixtures; there is no proof of trustworthy external time, shared consensus or actual hostile process isolation. The tests support a bounded educational result, not certification of a distributed coordinator.

A strong exercise is to terminate Worker A just after it commits `EXECUTE_IN_FLIGHT` and before it calls E5. Predict E2, E7 and mock E8 states; then explain why Worker B must not initiate a new payment. A second exercise is to devise a deployment in which E5 atomically verifies the E2 epoch and its financial grant, including what happens when a lease expires during an external provider call. A third is to compare the extra operational cost of E2 coordination with retaining the Build 4 single-controller design for a mostly routine workload.

## 27.7 What must be hardened for a real enterprise?

A production-worthy architecture requires more than correct local algorithms. The E2 authoritative state store must enforce identity, transaction isolation, lease issuance, durable epochs, owner replacement and recovery after storage failures. If several hosts and regions participate, all consequential update paths must reject stale fencing epochs; assumptions about clock skew, partition behavior and quorum must be explicit. E5 must remain independently administered, with protected credentials, specific business approvals, audience/tenant/workflow checks and denial evidence. E6 must validate a real provider's idempotency and status-query guarantees, and E7 must preserve original operation identities and unknown effects. Observability must correlate E2 lease transitions with E5 decisions, E7 operation state and E8 observations without storing secrets or unnecessary customer data.

The current fixture deliberately omits multi-site consensus, protected worker identities, E5-enforced E2 epochs, durable status-query scheduling and backoff, queue admission quotas, service quotas, independent finance/recovery issuer, provider contract certification, secure audit infrastructure, human adjudication interface and production incident automation. These omissions are **not engineering recommendations**; they identify the platform, security, finance, operations and governance work that would have to be designed and verified before any real financial deployment. Detailed distributed-failure analysis follows in Chapter 28; adversarial behavior in Chapter 29; runtime monitoring in Chapter 30; system verification in Chapter 31; and accountable production governance in Chapters 32–34.

## 27.8 Multi-perspective architecture review and engineering practice

A trustworthy deployment decision must withstand review by professionals responsible for implementation, architecture, security, operations and business outcomes. These are complementary **review perspectives**, not new E-domains, a mandatory five-person board, or a substitute for actual delegated approval. Each concern must end in an owner, a test or an explicit residual-risk decision.

**Implementing engineer:** Prove there are no implicit resends, that SQLite transactions close correctly, and that malformed outcomes never become success. **Enterprise architect:** Trace E2 work ownership (C02) while preserving independently controlled trusted decisions, durable intent, provider dispatch and reconciliation (C05–C08). **Security and assurance:** Challenge same-user file access and the absence of E5-enforced ownership epochs; an E2 lease is not a financial grant. **SRE/operations:** Test worker death, lease expiration, slow E5 responses, stale updates and escalation after unresolved reconciliation; missing E7 evidence does not establish that a provider effect never happened. **Business owner:** Demand measurable performance and availability benefit before accepting coordination cost and identify accountability for unresolved CASE-204 outcomes.

1. **Explain:** Distinguish E2 ownership, E5 authority, E7 operation state and E8 authoritative provider proof in CASE-204.
2. **Trace:** Demonstrate a crash after E2 intent but before E5 transport. Explain the safe recovery path and its cost in stalled work.
3. **Threat-model:** Give a stale worker a valid finance grant. Identify why local E2 fencing alone cannot prove that E5 will reject the call.
4. **Design:** Specify a protected E5-side ownership-epoch verification contract that does not confer new financial authority and survives coordinator replacement.
5. **Verify:** Inject simultaneous lease acquisitions, expired approvals, bad IPC responses and contradictory E8 status. Define objective pass/hold evidence.
6. **Defend:** Choose Build 4's simpler sequential controller or Build 5's optional coordinator for a workload with measured reliability, throughput, staffing and recovery requirements.

**Release standard:** The result must keep a stable RF-1042, show no unauthorized or duplicated local dispatch under the stated fixture assumptions, reject stale coordination updates, preserve UNKNOWN after lost evidence, and document all missing production mechanisms and their accountable owners. A successful demo is not enough; an engineer must be able to point to the exact code path, test assertion, observed state and excluded assumptions.

## 27.9 Part IV capstone: what the six builds actually prove

**The learning path is cumulative; the executable paths are only partly composed.** Build 0 demonstrates deterministic transaction handling. Build 1 separately runs an untrusted adviser. Build 2 connects scoped identity/context retrieval to that adviser. Build 3 enforces a financial request in a separate process. Build 4 adds a durable provider contract and read-only reconciliation. Build 5 runs optional E2 coordination against **the Build 4 E5 subprocess**, using a Build 2 *identity fixture*; it **does not call Build 1's advisory reasoning or Build 2's context retrieval in the same end-to-end refund runtime**. It does not operationally implement all nine E-domains or all nine contracts. The builds are independently runnable engineering checkpoints, not six deployed versions of one assembled system or a required Design A → B → C migration.

| Demonstration | Executed evidence | Not established |
|---|---|---|
| Advisory and scoped data | Build 1 E3/C04 proposal; Build 2 E1 fixture and E4/C03 retrieval before that proposal | A combined Build 5 advisory-to-payment pipeline or protected enterprise IAM |
| Trusted financial execution | Builds 3–5 E5 approval verification, E7 operation RF-1042, E6 adapter and mock E8 response | Production finance issuer, settlement, independent OS identities or real-provider guarantees |
| Optional ownership and recovery | Build 5 E2 leases/epochs, one execute intent and status-only takeover through Build 4 | E5-enforced E2 fencing, multi-site consensus or independently authorized long-term recovery |
| Governance and assurance | E9-relevant tests, contracts, review evidence and documented limitations | A running enterprise governance service or release certification |

**Three traces must remain distinct.** In an *approved* CASE-204 refund, the demonstrated Build 5 path begins with an assembled fixture request: E2 records intent, E5 validates a separate finance grant, E7 durably claims RF-1042, E6 dispatches once and mock E8 records the effect. In the *compromised-investigator* test, the valid E1 fixture identity alone is denied at E5 before any payment intent or effect. After a *lost acknowledgment*, the provider may already hold RF-1042 while E7 is UNKNOWN; the replacement E2 owner requests status-only reconciliation, never another dispatch. C01–C04 advisory admission/retrieval/proposal are architectural upstream responsibilities but are **not executed upstream of the Build 5 payment call**. C05–C09 are demonstrated only within their documented fixture scope. See the [companion implementation-to-evidence map](examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md) for contract-by-contract statuses, test cases and exact modules.

**Release decision exercise.** Would Design B without an E2 coordinator meet the retailer's measured needs more simply? If Build 5 were considered for live refunds, identify the owners and evidence for an independent identity and finance issuer (E1/E5), E5-enforced fencing (E2/E5), a real provider's idempotency and query contract (E6/E8), recoverable operational state (E7), and monitoring, incident handling and human recourse (E9). **Passing the educational tests is not permission to deploy.** Chapters 28–31 deliberately challenge these guarantees; Chapters 32–34 determine release governance and lifecycle responsibility.

**Sources and scope.** Lamport (1978), Gray and Reuter (1992), Kleppmann (2017) and van der Aalst (2013) support the inherited distributed coordination, transaction and workflow principles. The precise CASE-204 implementation, E2 local lease protocol and executable tests are original ETIS educational fixtures, not guarantees attributed to an external publication. Publication-level claim/page audit and real-system acceptance remain separate release gates.

## Chapter synthesis and transition to Part V

Optional coordination must earn its complexity through measured business and operational benefits. Build 5 adds durable E2-local ownership, epochs and conservative takeover, but neither grants financial authority nor completes every reference-architecture contract in a single runtime. Taken together, Builds 0–5 teach the engineering boundaries and evidence required to evaluate a trustworthy system—not permission to deploy their fixtures as a payment service. Part V begins in Chapter 28 by testing how these boundaries survive distributed failure and uncertain external effects.
