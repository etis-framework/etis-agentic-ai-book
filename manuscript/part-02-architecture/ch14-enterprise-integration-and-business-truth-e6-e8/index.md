# Chapter 14 — Enterprise Integration and Business Truth (E6/E8)

*Part II: Enterprise Reference Architecture*

> **Engineering proposition:** An authorized request is not a completed refund. A guarded enterprise adapter can attempt an effect, but only appropriately scoped business records and provider evidence can establish what actually happened.

## Learning objectives

After this chapter, readers should be able to (1) separate authorization, integration dispatch, provider acceptance, and confirmed business effects; (2) design a versioned provider contract with explicit failure and idempotency semantics; (3) identify authoritative records for customer, order, payment, and refund facts; (4) reconcile lost acknowledgments without causing duplicate refunds; (5) validate provider callbacks rather than treating them as instant truth; and (6) construct tests that demonstrate integration boundaries under ordinary and adversarial failures.

## 14.1 From permission to external consequence

Figure 8.1 distinguishes the governed E6 adapter from E8 authoritative business facts and external payment effects. Chapter 13 established **trusted execution and authority (E5)**: independent authorization, protected payment credentials, durable intent, and the stable refund-operation identity `RF-1042`. The customer in `CASE-204` reports that a replacement never arrived and requests a **$500 refund**. **Design A** remains the deterministic baseline; **Design B** is the conditional production candidate with AI advice and independent review; **Design C** is a bounded, **read-only** investigative alternative, not an approved payment actor. None changes the route to an external financial effect.

**Enterprise integration (E6)** is the governed software interface that maps a permitted operation onto external provider protocols. **Authoritative business systems (E8)** are systems assigned the right to establish particular customer, order, payment, and refund facts. E8 is a *logical responsibility*, not one universal database; the actual payment provider may be the authority for the payment effect while an order system owns fulfillment facts. **Durable operational state (E7)** records locally known intentions and observations; it cannot turn a missing provider acknowledgment into a completed refund.

Figure 14.1 separates *who can authorize* from *who can transmit* and *which records can substantiate the outcome*. An implementation may colocate responsibilities, but must preserve independent permission checks, credential custody, provider access restrictions, and reliable evidence. The agent-controlled runtime has no direct payment route.

![Figure 14.1 — Trusted authorization controls the guarded adapter; authoritative records, not the agent or local dispatch log, establish external effects.](assets/shared-figures/rendered/F14-01.png){#fig:f14-01 width=5.75in}

An **adapter** is an integration component that translates internal operation contracts into a specific provider's protocol and translates provider responses into explicit evidence-bearing observations. A provider interface is not a trustworthy boundary merely because it has an SDK. The adapter is part of the trusted execution path, but does not independently invent a new authorization decision.

## 14.2 Specify the provider contract before implementing an SDK call

The internal operation contract remains stable across provider changes. It binds case, tenant, original payment reference, refund amount and currency, authorized action, `RF-1042`, authorization evidence, and contract version. The provider contract must then define *which fields the provider accepts and what their responses mean*. Illustrative names below are **not** a claim about any real payment provider's API. Provider-adapter and message-contract patterns are treated in Hohpe and Woolf (2003); this chapter does not assume a particular provider implements them.

| Contract concern | Required engineering decision |
|:--|:--|
| Identity and scope | Authenticate the adapter workload with E5-governed credentials; bind merchant/account, tenant, payment and permission scope. |
| Request mapping | Map `$500`, currency, original charge, merchant, and `RF-1042` without rounding, wrong-account routing, or agent-supplied identifiers. |
| Version/capability | Pin compatible API version, refund feature, idempotency scope, status lookup and webhook capabilities; reject unsupported contracts. |
| Deduplication | Document whether the provider honors a stable idempotency key, for which merchant, endpoint, parameters and retention period. |
| Response meaning | Distinguish transport receipt, accepted/queued, pending, completed, rejected and indeterminate outcomes. |
| Evidence | Preserve provider operation ID, request correlation, timestamps, version, status provenance and the raw response reference under retention rules. |

A **provider operation ID** is the provider's own identifier for a transaction; it may differ from `RF-1042`. Maintain a durable, checked mapping between the two. An **idempotency key** is a provider request-deduplication mechanism. It is **not a secret**, authentication credential, access token, or authorization grant. Its effect depends on the provider's documented scope, lifetime, and parameter-equality rules. It cannot replace local uniqueness controls or E5 authorization. Keep provider credentials outside model prompts, tools and logs; E6 obtains them through the protected path established in Chapter 13.

An **integration contract test** verifies that a local request becomes the intended external request and that each real provider response maps to a defensible local observation. Contract tests require provider-specific mocks or sandbox evidence; neither a successful HTTP exchange nor a passing schema validator proves a financial effect. A **compatibility adapter** may support provider versions, but it must fail closed on unknown response fields that affect financial semantics rather than quietly normalize them to `COMPLETED`.

## 14.3 Model the attempt and its uncertainty

**Dispatch** means that the integration path attempted to send a request. **Acceptance** means the provider acknowledged receipt or processing according to its contract. **Completion** means authoritative provider evidence establishes the effect specified by the contract; depending on the provider, settlement and availability to the customer can be separate later events. An HTTP `200` or `202`, an SDK return value, or a callback can represent any of these stages: the contract, not the numeric code alone, determines meaning. Gray and Reuter (1992) and Kleppmann (2017) distinguish local transaction evidence from distributed effects. RFC 9110 §9.2.2 (Fielding, Nottingham, and Reschke, 2022) defines HTTP-method idempotency; it does **not** establish payment-provider idempotency-key scope, refund deduplication, or settlement guarantees.

Figure 14.2 traces the most dangerous ordinary failure. The authorized `RF-1042` request reaches the payment provider, which may commit the $500 refund, but its acknowledgment is lost. The adapter records **UNKNOWN**, not `FAILED` or `COMPLETED`. It does not create a second operation identity or select a new idempotency key in an attempt to “be safe.”

![Figure 14.2 — An acknowledgment can be lost after a provider commits the refund; UNKNOWN blocks blind replay until authoritative reconciliation.](assets/shared-figures/rendered/F14-02.png){#fig:f14-02 width=5.75in}

A **timeout** means the caller did not observe an answer within a specified interval; it does *not* prove the provider did nothing. Connection failures before confirmed dispatch may still have ambiguous boundaries in a network stack. Likewise, `5xx` responses, dropped callbacks, and an internal process crash do not imply a safe retry. A local **transactional outbox**—a durable dispatch-intent record committed alongside authorized state—helps ensure work is not forgotten, but cannot atomically commit a local database and an external payment. Before any replay, the dispatcher must inspect whether its provider contract supports exact-key replay and whether the original attempt might have taken effect.

The minimum observable operation lifecycle is `AUTHORIZED_INTENT → DISPATCH_ATTEMPTED → {PROVIDER_PENDING, CONFIRMED, REJECTED, UNKNOWN}`. `REJECTED` requires authoritative evidence of rejection, not a local timeout. `CONFIRMED` requires the applicable provider evidence and business validation. Where provider results are eventually consistent, a `NOT_FOUND` immediately after dispatch is not definitive failure. A **terminal state** is one in which the provider contract and reconciliation policy agree that no further status transition relevant to the operation is expected; an `accepted` message is not necessarily terminal.

## 14.4 Define truth by question and source

A **system of record** is the designated authoritative source for a defined class of business facts. Authority is *fact-specific*: it does not transfer from the customer database to the payment provider, or from a cached search index to the refund ledger merely because one system has more recent-looking data.

| Question for CASE-204 | Primary authoritative evidence | What is insufficient |
|:--|:--|:--|
| Is this the correct customer and tenant? | Customer/account registry plus verified identity binding | A model summary or customer-supplied identifier alone |
| Did the replacement arrive? | Order and fulfillment/carrier records with event provenance and dispute rules | A cached retrieval excerpt or unverified message |
| Was the original payment captured, and what remains refundable? | Payment/ledger records and refund history for the original payment | Prior eligibility snapshot or proposal |
| Was **RF-1042** actually refunded? | Provider transaction/status evidence reconciled to the original charge, merchant, amount and provider ID | Local `SENT`, HTTP `202`, webhook receipt or model confidence |

**Provenance** identifies the source, capture time, version and transformation history of a fact. **Freshness** describes how recently that fact was known to hold; an old but authentic order row is not necessarily current eligibility. **Read-after-write consistency** means a confirmed write is visible to an immediately following read under the source's stated guarantee; not all provider status endpoints provide it. **Eventual consistency** means replicas or derived views may lag before converging. Consequently, an immediate absence of `RF-1042` from a report cannot cancel evidence that a payment provider accepted the operation.

Business truth is not a “last write wins” contest. E5's decision on eligibility must be revalidated as required before dispatch, using the authoritative facts and version controls established in Chapter 13. E6 then observes provider processing. E8's provider evidence resolves *whether an effect happened*, while fulfillment records resolve *what happened to the replacement*. If records conflict, preserve both and escalate to the accountable financial owner; do not silently select the record that helps a workflow complete.

## 14.5 Reconcile without creating a second refund

The E7 operation journal is authoritative about what the application has attempted and observed, including `UNKNOWN`; E8 business records and provider evidence are authoritative about the external refund outcome. A workflow status and an external business disposition are distinct records that must be reconciled, not competing versions of the same fact.

**Reconciliation** is the controlled comparison of locally recorded intent and observations against authoritative external evidence, resulting in an evidenced outcome or a documented unresolved exception. The reconciler is trusted, deterministic infrastructure, not an independent refund-authorizing agent. It uses the original `RF-1042`, original provider idempotency mapping and the original payment reference throughout.

Figure 14.3 is a decision procedure, not a promise that every provider exposes all necessary queries. The search first attempts exact provider-operation or key lookup, then checks the original payment's transaction history when contractually supported, and correlates amount, currency, merchant, customer/tenant binding and timestamps. Provider query failures, lag, inconclusive matches and conflicting records remain `UNKNOWN` and go to review. Only unambiguous evidence of the same effect justifies `CONFIRMED`.

![Figure 14.3 — Reconciliation requires a matching authoritative provider record or an explicitly documented exception; missing evidence is not permission to retry.](assets/shared-figures/rendered/F14-03.png){#fig:f14-03 width=5.75in}

A provider's authoritative *negative* result permits reattempt only if the provider contract proves that the prior request cannot later take effect and that an exact-key replay cannot duplicate a refund; otherwise retain `UNKNOWN` and escalate. If the provider cannot provide adequate deduplication or outcome lookup, engineering must explicitly choose a safer integration, human-controlled recovery, or an operational risk limit before production. Do not advertise “exactly once” across an uncoordinated local database and provider: the defensible objective is *at most one intended business effect*, supported by tested provider guarantees, durable identities and reconciliation.

A **webhook** is a provider-initiated notification to a configured endpoint. Validate its signature or authenticated channel, tenant/account, event identity, replay window, ordering and payload against trusted provider configuration. Store the evidence with restricted access, deduplicate event deliveries and check source versions. A signed callback can still be stale, misordered, or semantically nonterminal. Correlate it with `RF-1042` and verify against authoritative provider status when the risk and contract require. Never let a webhook's `success` string independently bypass E5 or overwrite a conflicting payment record.

## 14.6 Failure, security and acceptance tests

The engineering team should exercise outcomes that normal happy-path demos omit. Test ambiguous timeout *after* a simulated provider commit; timeout *before* dispatch; duplicate outbox delivery; reused key with different amount; expired provider key retention; wrong tenant/merchant or original charge; stale read-after-write result; duplicate, delayed, forged or out-of-order webhook; incompatible API version; credential revocation between authorization and call; provider lookup outage; conflicting refund-history records; and a replay attempt by an agent through a direct provider route. Assert that each preserves the original operation identity, rejects unauthorized paths and keeps unsupported outcome claims out of user-facing summaries.

For `CASE-204`, an acceptance record should contain the trusted approval/authorization and source versions; canonical `RF-1042` and mapped provider identity; request fingerprints without exposing credentials; dispatch attempts; raw provider evidence references; reconciliation disposition; and the accountable actor for any exception. An **evidence fingerprint** is a cryptographic digest used to detect alterations to a particular evidence object; it does not independently prove the underlying provider statement is true. Protect logs and retained payloads against payment-data leakage. A financial operation is not safely complete merely because the integration team's dashboard is green.

### Worked recovery check

Suppose the provider issued the $500 refund but the acknowledgment vanished. E7 records `UNKNOWN`; the reconciliation path queries the provider using the preserved identity and finds a transaction matching the original payment, merchant, amount, currency and `RF-1042` mapping. The financial owner verifies that the provider's status satisfies the contract's definition of completion. Only then is the outcome recorded as `CONFIRMED`. If the lookup instead says “not yet visible,” the outcome remains `UNKNOWN`, not `FAILED`. No agent is asked whether another refund “seems likely” to be safe.

## 14.7 Architecture decisions and chapter transition

Record the provider contract and version, authoritative source ownership by fact, idempotency scope and lifetime, accepted evidence for completion, read consistency limits, callback validation, financial exception owner, provider-switching conditions, and the maximum unresolved exposure the organization can tolerate. An **architecture decision record (ADR)** documents such a consequential choice and its rejected alternatives; the rationale and acceptance evidence matter more than a vendor diagram.

Chapter 15 develops **durable operational state and assurance (E7/E9)**: how those intents, observations, transitions, and evidence survive coordinator replacement and become observable to operators. Chapter 14's boundary remains: a durable local record explains what the system knows, while authoritative enterprise and provider facts determine what happened outside it.

## Chapter exercises

1. **Contract defense:** Draft the smallest versioned adapter contract for `RF-1042`. Identify which provider behaviors must be verified in a sandbox before allowing safe exact-key replay; distinguish the provider idempotency key from the protected authentication credential.
2. **Ambiguous outcome:** Draw the branch of Figure 14.3 in which status lookup returns `NOT_FOUND` under an eventually consistent provider. State the safe disposition and the evidence that would permit a later transition.
3. **Truth ownership:** For a contradictory delivery scan, order note, and provider refund status, assign each fact to its responsible system of record. Identify the human escalation owner and state what the AI may only recommend.
4. **Adversarial test:** Design a negative test that prevents Design C's read-only agent from reaching payment credentials or a callable refund route even when it fabricates a provider authorization token.

**Engineering checkpoint:** Before release, can an independent reviewer reconstruct one and only one requested $500 refund, distinguish every observation from its external effect, and show why no retry, callback, or agent assertion can authorize another payment?
