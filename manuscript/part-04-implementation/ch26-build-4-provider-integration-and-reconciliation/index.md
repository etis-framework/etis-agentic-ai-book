# Chapter 26 — Build 4: Provider Integration and Reconciliation

Part IV: Progressive Reference Implementation

> **Engineering proposition:** A financial adapter must express an actual provider's contract and its uncertainty, not conceal them. A local dispatch record proves intent, a successful transport call is not necessarily business truth, and an absent status response cannot authorize a new refund.

## Learning objectives

After completing this chapter, readers should be able to distinguish durable dispatch intent from externally confirmed payment; specify versioned provider capabilities, idempotency scope and status-lookup obligations; design a provider adapter with typed observations and explicit uncertainty; reconcile an acknowledged or lost-response refund without issuing a second instruction; test contradictory, missing and stale external evidence; and identify which guarantees still require a real provider contract, protected deployment and operational governance.

## 26.1 One unchanged refund, a new source of uncertainty

The recurring case is **CASE-204**, a customer's replacement complaint with a proposed **$500 refund**. A separately approved financial instruction creates a stable refund-operation identity, **RF-1042**. It does not create a new operation when a network call fails. Build 0 supplied a deterministic simulation with separate local and provider SQLite databases. Build 1 introduced review-only agent reasoning and an advisory action-proposal contract (C04). Build 2 constrained the admission-and-identity (E1) fixture assertion and context/retrieval (E4) query contract (C03). Build 3 moved transaction-specific approval behind a separate trusted-execution-and-authority (E5) process: a compromised investigator carrying a genuinely valid identity assertion could not mint RF-1042 without a distinct signed finance grant.

Build 3 deliberately used a simple simulated provider behind its E5-controlled path. **Build 4 does not weaken that gate.** It adds a provider-adapter contract to enterprise integration (E6), a separately recorded provider view of the effect in mock authoritative business truth (E8), and more explicit durable-operation state (E7) and reconciliation. These responsibilities correspond to the trusted-action request (C05), durable-operation handoff (C06), controlled integration (C07), and authoritative-status observation (C08) from the Chapter 8 reference architecture. Governance and assurance (E9) requires that each assertion be supported by test evidence. Coordination and ownership (E2) remains a single local controller: distributed leases and fencing are not implemented here.

This is another *teaching checkpoint*, not a maturity level or an argument for more autonomy. Designs A, B and C remain alternative enterprise arrangements. Design B—bounded advisory reasoning with independent review—remains the conditional initial production candidate. The provider boundary is equally important to a deterministic Design A, a hybrid Design B, or an optional bounded-investigator Design C.

## 26.2 Name the provider contract before writing an adapter

A payment adapter is not merely a wrapper that converts a dictionary to an HTTP request. Before authorizing a real instruction, engineers must establish what the provider actually guarantees: the definition of an operation identity, the account and tenant scope of its idempotency key, retention duration, how a duplicate request is treated, what constitutes an authoritative status lookup, which terminal states exist, which errors can occur after a commit, and which identifiers support reconciliation. The engineering contract must also specify amount units, currency, payment references, API versions, authentication, audit requirements, and provider-side authorization limits.

This edition's **Build 4 fixture** pins a deliberately simple contract: provider version `etis-fixture-provider-v1`; stable refund identity `RF-1042`; exact amount **50,000 integer cents** in USD; one provider-account-scoped uniqueness key; a documented fixture retention assumption of 86,400 seconds; and a status query keyed by that same operation identity. The `Capabilities` dataclass in `build4/provider_contracts.py` validates these assumptions before a workflow is constructed. The static fixture does **not** measure a commercial provider's retention window, demonstrate network authentication, or establish that its database behaves like a bank or processor. A real implementation must replace the values only after external contract and operational verification.

![](assets/shared-figures/rendered/F26-01.png)

*Figure 26.1 — Provider-boundary architecture. The untrusted request crosses the independent E5 decision process before E7 records RF-1042; the server-owned E6 adapter addresses a separately stored mock E8 provider record and returns typed observations for E7. The E3/C04 advisory path cannot call the provider or rewrite its status.*

The source architecture inside `build4/README.md` identifies the actual Python modules rather than pretending that every logical E-domain is a microservice. The new `provider_contracts.py` defines immutable `RefundCommand`, `Capabilities`, `ProviderObservation` and `ProviderPort` abstractions. `adapter.py` implements the simulated provider; `ledger.py` owns the local state machine; `workflow.py` sequences the validated financial operation; and `service.py` provides the separate E5 request entry. The client reuses the Build 3 socket transport. Production isolation of E5 and the approval issuer is not established when every fixture process shares the same OS account.

## 26.3 An operation has three distinct kinds of evidence

A refund request can be **authorized** without being sent; **dispatched** without an acknowledgment; and **externally confirmed** while its caller knows only that a response was lost. We preserve these distinctions in E7 rather than converting every transport exception into `FAILED`. E7's local SQLite `operations` row carries the stable operation ID, immutable case, tenant, amount and currency, status, a bounded observation category, and any validated provider reference. The independent mock E8 database uses a provider-side unique operation key. They are separate transactions and may temporarily disagree.

Build 4's ordered control path is intentionally small. After E5 validates the existing identity assertion and transaction grant, the workflow writes an `AUTHORIZED` durable intent. It then atomically changes precisely one operation from `AUTHORIZED` to `DISPATCHED` and commits that local claim **before** calling E6. If E6's simulated provider acknowledges a consistent commit, a validated `ProviderObservation` permits E7 to record `CONFIRMED`. If the mock provider commits but its response is lost, E7 remains `UNKNOWN` and reconciliation must use a **status lookup**. If the provider is unreachable before a known observation, E7 is also unresolved because the local caller cannot safely infer an external outcome from a timeout.

![](assets/shared-figures/rendered/F26-02.png)

*Figure 26.2 — Behavioral sequence for RF-1042. E5 approval precedes E7 intent; a unique local dispatch claim precedes E6 submission; mock E8 commits once; the acknowledgment may be lost; a read-only C08 status query supplies the evidence that resolves E7 UNKNOWN. No second refund command appears on the recovery path.*

The key distinction is **idempotency versus reconciliation**. A documented idempotency mechanism constrains the effect of duplicate instructions under a provider's particular scope and retention assumptions. Reconciliation asks what effect occurred and whether the enterprise has defensible evidence of it. Neither capability alone proves universal exactly-once execution. If the provider changes the idempotency window, key scope or lookup behavior, the adapter's assurance claim must be reviewed as a versioned change. Distributed-systems treatments of partial knowledge and durable records inform this separation (Gray and Reuter, 1992; Kleppmann, 2017); neither publication defines the contract of an unnamed payment provider.

## 26.4 The provider adapter is a controlled integration component

The adapter's command contract is fixed for this exercise: `case_id=CASE-204`, `tenant_id=retailer_a`, `operation_id=RF-1042`, `amount_cents=50000`, and `currency=USD`. Exact integer type checks reject `True` as an amount even though Python treats booleans as integers in some comparisons. The adapter validates a provider capability set and returns typed observations with an outcome, operation identity, provider reference where confirmed, source classification and contract version. A forged textual message such as “provider confirmed” cannot satisfy the type and value checks for a confirmed observation.

The simulated provider represents a stable operation key with a SQLite primary key. A second instruction carrying the same identity and *identical immutable attributes* cannot create a second mock effect. A conflicting amount or other immutable field raises a `ProviderConflict`; it cannot be silently accepted as a successful duplicate. This is not permission to send repeated instructions after uncertainty: the E7 compare-and-set prevents the application from claiming another dispatch once RF-1042 has left `AUTHORIZED`. The fixture therefore teaches two independent controls: server-side effect identity and local no-blind-retry discipline.

We deliberately do not simulate a mutable, general-purpose payments API. For a real provider, engineers must characterize status freshness, the reliability of lookup under regional outages, ambiguous transport errors, reversals, chargebacks, currency precision, provider references, ledger consistency, partial refunds and settlement delay. A confirmed provider refund may still differ from final bank settlement. **No fixture result should be presented to a customer as proof of real funds returned.**

## 26.5 Reconciliation is observation, not another execution attempt

The provider lookup in `SQLiteFixtureProvider.lookup()` reads the mock E8 record without dispatching a command. The `RefundWorkflow.reconcile()` method first requires an existing E7 operation that had reached `DISPATCHED`, `UNKNOWN` or `CONFIRMED`; it cannot create a new RF-1042 row. It then obtains and validates a provider-status observation. Only a matching, provider-referenced `CONFIRMED` observation updates local state to `CONFIRMED`.

A missing provider record is returned as `NOT_FOUND`, **not** as evidence that the original operation definitively failed. A missing record can arise from lookup lag, regional inconsistency, request routing, retention expiry or a faulty query. Build 4 therefore leaves the operation UNKNOWN and escalates rather than sending a replacement command. Contradictory provider evidence likewise yields UNKNOWN rather than a convenient denial; if a previous confirmation is later contradicted, the operational record is marked unresolved for investigation, retaining its earlier reference as evidence of the discrepancy. This is an intentional conservative teaching rule.

![](assets/shared-figures/rendered/F26-03.png)

*Figure 26.3 — Decision path for unresolved effects. Check durable dispatch history, query authoritative provider status, validate identity/amount/version and confirm only on compatible proof. Missing, unavailable or conflicting evidence remains UNKNOWN and requires escalation. There is no branch from uncertainty to a new dispatch.*

The fixture also rechecks the original short-lived, case-specific E5 finance grant for its `reconcile` operation. Once the grant expires, delayed reconciliation needs fresh authorization; **production must distinguish read-only recovery permission from permission to issue a new refund**, with independently governed service/operator roles, revocation and audit. The fixture demonstrates that an expired grant cannot be replayed, not a complete long-running authorization design.

Operationally, a reconciliation worker should have a bounded retry-and-backoff policy **for status queries only**, a deadline, an escalation owner, safe diagnostics, and an audit trace. The present fixture performs a single lookup per request and does not implement a scheduler, durable queue, multi-region consistency or human adjudication interface. Readers must not confuse the absence of those modules with a recommendation to omit them in production.

## 26.6 Run the code and inspect the evidence

From the repository root, enter the Build 4 directory as shown below. Use Python 3.10 or later on macOS/Linux with Unix-domain sockets. No cloud account, external model, real keys or payment credentials are needed. Start with `examples/refund-reference-system/build4/README.md` and its embedded `architecture.svg`; inspect the source alongside the exact tests and documented limitations.

```sh
cd examples/refund-reference-system/build4
python3 demo.py --scenario denied
python3 demo.py --scenario approved
python3 demo.py --scenario lost-ack
python3 demo.py --scenario outage
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The `denied` scenario uses a valid fixture identity assertion but lacks the separately approved finance grant: E5 denies it before creating either database. The `approved` scenario confirms one effect. In `lost-ack`, mock E8 commits once, E7 records UNKNOWN, and a read-only status query resolves RF-1042. In `outage`, dispatch intent is durable, but mock E8 has no matching record; the status query remains UNKNOWN and cannot authorize a resend. The request fields `lose_ack` and `outage_before_send` are **fixture-only fault injection hooks**, not permissions an untrusted caller should control in a real payment interface. A production integration must move these controls into a protected test environment and remove them from public request schemas. Each scenario uses isolated temporary files and a separate service subprocess. The tests further inject contradictory provider records, unusable capability contracts, wrong types and tenant, replayed calls, invalid reconciliation parameters, stalled frames and disconnected clients. Executable evidence describes these exact fixture cases, not an external security or provider certification.

A particularly useful reader exercise is to predict the state of both SQLite databases after a lost acknowledgment, and **only then** inspect the test results. The correct explanation must distinguish what E5 approved, what E7 recorded, what E8 observed and which evidence justified the final local transition. Another exercise is to replace the fixture provider with a `ProviderPort` implementation whose idempotency key expires before a status query becomes reliable. The safe architectural answer is to withhold automatic redispatch and require an operational escalation, not to assert a magical exactly-once guarantee.

## 26.7 War-game the failure and security assumptions

An implementing engineer must demonstrate that the typed command cannot silently change amount or currency, and that the provider adapter never receives an unverified advisory proposal. An enterprise architect must trace E5/C05 authorization, E7/C06 durable intent, E6/C07 adapter semantics, E8/C08 truth and E9 assurance without confusing logical domains with Python files. An advanced student should be able to explain why a `NOT_FOUND` lookup is not equivalent to a failed payment. A security reviewer should demonstrate that a valid E1 token alone cannot reach the E6 fixture and that the same-user process arrangement is not real isolation. An SRE must see bounded transport behavior, no blind effect retries, and escalation for missing or contradictory provider proof. A business owner must be able to ask who accepted the $500 exception, what payment evidence exists, and whether customer communication is justified.

The fixture intentionally does not include real provider credentials, end-to-end authentication, dedicated OS service identities, independent finance approval systems, credential rotation, provider contract certification, scheduled reconciliation, durable event/outbox workers, multi-worker lease fencing, rate limiting, production telemetry, immutable audit infrastructure or customer messaging. The omission is acceptable **only because it is explicit**: these are separate responsibilities, with owners and verification requirements, not hidden assumptions that a Python demo somehow satisfies. Chapter 27 considers optional coordination and hardening; Chapter 28 addresses distributed failure; Chapter 29 considers compromised agents; Chapter 30 operational reliability; Chapter 31 independent verification; and Chapters 32–34 business and release accountability.

## 26.8 Engineering practice and release judgment

1. **Explain.** For CASE-204, distinguish the C04 proposal, E5 approval, E7 RF-1042 intent, E6 dispatch and E8 confirmed effect. Identify the authority for each.
2. **Design.** Write a real-provider contract checklist covering idempotency scope and retention, version, operation identity, duplicate response, status query, currency/amount and error semantics.
3. **Trace.** Draw E7/E8 state after lost acknowledgment. Demonstrate why the recovery path reads rather than resends.
4. **Threat-model.** Assume the investigator has a valid identity token and a persuasive forged “approval” string. State which independently evaluated gate rejects the request and what the code proves.
5. **Test.** Add a contradictory-provider-reference scenario. State which local evidence remains trustworthy, which becomes uncertain, and whether a customer may be told that settlement completed.
6. **Defend.** Make a proceed, conditional-proceed or hold decision for a hypothetical provider that supports idempotent sends but offers no reliable status query after a timeout. Identify who owns the residual risk.

**Review standard:** A satisfactory engineering argument identifies the exact provider guarantees actually verified, records the original operation identity, separates evidence from inference and keeps unresolved effects visible to accountable operators. Passing the fixture tests is not proof that an external provider will honor the same semantics.

## Chapter synthesis and next boundary

Build 4 adds an explicit provider contract, typed external observations and read-only reconciliation **without adding agent authority**. It preserves the independently governed E5 gate established in Chapter 25 and the single stable RF-1042 operation identity. A local failure cannot be transformed into a safe new payment merely by obtaining another plausible response. Chapter 27 next examines whether optional coordination, ownership fencing and operational hardening would create measurable value, while the later reliability and assurance chapters test the remaining failure claims.

**Sources and boundaries.** Gray and Reuter (1992) and Kleppmann (2017) support the durable-state and distributed-uncertainty analysis; the provider protocol, local capability fixture and exact test outcomes are original ETIS educational artifacts. No external publication is cited as certifying this simulated payment provider. A production implementation requires a documented provider contract, independent security review and live-environment acceptance evidence.
