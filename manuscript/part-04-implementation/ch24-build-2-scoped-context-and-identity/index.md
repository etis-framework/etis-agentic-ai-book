# Chapter 24 — Build 2: Scoped Context and Identity

*Part IV — Progressive Reference Implementation*

> **Engineering proposition.** A convincing recommendation is still an untrusted proposal. Before asking E3 to interpret evidence, the surrounding system must establish whose bounded work is being performed, which sources may be read, how the observations were obtained, and when they stop being sufficiently current. A valid identity assertion is not transaction-specific authorization.

## Learning objectives

By the end of this chapter, readers should be able to distinguish assertion integrity, identity authentication, context-access authorization and financial authorization; implement a scoped C03 retrieval gate; validate source provenance and freshness before invoking E3; reproduce cross-tenant, stale-source and forged-assertion denials; state exactly what a local cryptographic simulation does **not** prove; and defend the remaining requirements for independently protected E5 execution.

## 24.1 Why Build 1 is not enough

Chapter 22 established a deterministic CASE-204 refund fixture: a proposed $500 refund, a separately checked local E5 authorization decision, stable RF-1042 operation identity, E7 SQLite operational state and a separate mock E8 provider record. Chapter 23 added bounded E3 reasoning that produces a typed, untrusted C04 review proposal. Its evidence was explicitly supplied as a fixed `Evidence` object. A `verified=True` fixture bit was sufficient to make an educational example run; it was never a proof that a particular human, service or agent had access to the correct customer's information.

Consider an investigator that receives an apparently valid replacement-status message. Is it about CASE-204 or another customer's case? Does it belong to `retailer_a`? May this investigator use shipment evidence for the assigned purpose? Is the message a recent record, or an earlier cached observation? Does it merely report a customer's assertion, or establish a provider's financial truth? If these questions are deferred until after a model writes a recommendation, a well-formed C04 JSON proposal can give an undeserved appearance of assurance.

Build 2 therefore moves the evidence-handling boundary earlier. It adds a limited E1 fixture assertion, a scoped E4 context gateway, and a controlled adapter into the unchanged Build 1 adviser. The code is credential-free, deterministic and reproducible, but it is **not an enterprise identity system**. To keep E3 deterministic, the fixture controller preselects one E4 record on E3’s behalf: this illustrates C03’s input/output obligations, **not a literal E3-initiated retrieval call**. E2 admission, C01 work routing and C02 assignment remain deliberately simulated. The book's stronger authorization and malicious-agent enforcement obligations remain assigned to Chapter 25. The three architectural designs remain alternatives: Build 2 does not require adopting Design C, and Design B remains only a conditional initial production candidate.

## 24.2 The boundary and the owners

![Build 2 maps fixture assertion verification and scoped context into an untrusted C04 proposal, separate from the E5 financial path.](assets/shared-figures/rendered/F24-01.png)

*Figure 24.1 — Build 2 logical architecture. The fixture controller verifies E1 claims and preselects E4 context on E3’s behalf (a partial C03 illustration, not a new CAB-001 contract direction). E3 consumes only the gated observation; C04 remains advice. No new route to E5/E6/E7/E8 is created.*

| CAB-001 responsibility / contract | New executable representation | Deliberate non-guarantee |
|---|---|---|
| E1, C01 | `LocalAssertionAuthority` signs and verifies a bounded fixture assertion | No external IdP, identity proofing, delegated production credential or isolated issuer |
| E2, C02 | A fixed review work request and `TRACE-204` correlation | No durable distributed coordinator, lease or epoch fencing |
| E4, C03 | `FixtureCatalog`, `retrieve()`, source allowlist, classification, case/tenant lookup, observation age | No real retrieval service, signed originating record or authoritative business ledger |
| E3, C04 | Unmodified Build 1 `advise()` and immutable `Proposal` | No model authority, payment tool or approval grant |
| E5/E6, C05/C07 | Unchanged, separate Build 0 financial exercise | No protected authorization service or production payment adapter |
| E7/E8, C06/C08 | No write path in Build 2; Build 0 records remain independent | No transaction status or financial reconciliation in the advisory path |
| E9, C09 | Test results and observable rejection categories | No production audit trail, remote attestation or organization-wide monitoring |

**Authority remains a chain of independent decisions**, not one identity flag: the issuer asserts who is represented; the scope contract constrains a purpose and permitted sources; the context gateway makes a source usable for review; the E3/C04 result proposes an interpretation; and only an independently enforced E5 authorization may permit a consequential instruction. Neither source access nor claim integrity answers whether this $500 refund is eligible.

## 24.3 Scope is a contract, not a model instruction

The fixture assertion contains `subject`, `tenant_id`, `case_id`, `purpose`, `allowed_sources`, `issued_at`, `expires_at` and `issuer`. The issuer signs a canonical representation with HMAC-SHA-256. The verifier rejects malformed encodings, additional or missing fields, altered signatures, expired and not-yet-valid assertions, unacceptable lifetimes and inappropriate claim types. It produces an immutable `VerifiedScope` whose meaning is explicitly limited to the local exercise.

These limits implement the broader resource-focused identity/authorization distinction discussed by NIST SP 800-207 (2020); the ETIS fixture fields are our own teaching construct, not a NIST-issued credential design. The subject identifies the simulated reviewer or investigator. The purpose is `review_replacement_complaint`, not `issue_refund`. The allowlist contains `EV-204`, not E6 payment interfaces. These are deliberately narrow names: a principal cannot infer permission for another source because it has a valid signature. A successful integrity check proves that the bytes match the fixture key **under the assumptions of the exercise**; it does not prove that the individual holding the assertion is an authenticated enterprise principal, nor that the signing key is protected from an attacker running code in the same process.

The source includes a publicly visible example key to make the lesson executable without credentials. Consequently **anyone who can run arbitrary code with access to the fixture can create another syntactically valid assertion**. This is a deliberate teaching limitation, not hidden security. Real E1 would obtain a verified principal and bounded delegation from an independently governed identity provider, validate issuer and audience, restrict lifetime and replay, protect credentials and distribute revocation state. Real E4 must independently enforce access control, including when E3 is compromised. Neither interface should trust a model-produced claim about its own scope.

The `VerifiedScope` Python data class itself is also constructible. Only the `verify()` entry point gives a fixture-controlled assertion check; importing and constructing the data class is **not** proof of privilege separation. A production gateway must prevent callers from supplying self-declared verified objects at a privileged interface. Chapter 25 supplies the next protected execution boundary; production E1 and E4 identity enforcement remain a separately owned deployment requirement.

## 24.4 Context is selected and provenance-bearing, not authoritative money

The E4 fixture gateway looks up a catalog record using the verified tenant, case and permitted source identifier. A record contains the evidence version, `observed_at`, delivery status, bounded narrative, and `CASE_RESTRICTED` classification. The gateway checks that the catalog key agrees with the record identity and that the observation is no more than 300 seconds old and not dated in the future. Source absence, cross-tenant mismatch, unsupported classification, version drift and bad timestamps fail closed. An outage raises `ContextUnavailable`, distinct from `ScopeDenied`.

The resulting `ScopedEvidence` also records retrieval time, the selected principal, purpose and a literal provenance label. This is evidence about the educational retrieval path—not proof that a real shipment provider signed the assertion, or that all upstream data were correct. The narrative can include customer text and adversarial instructions. Those strings are relevant *data*, never policy, identity or a permission grant. The prompt-injection and tool-misuse threat motivations follow the OWASP GenAI and agentic threat guidance discussed earlier in the book; that guidance does not certify this implementation. E4 cannot turn an email, a search result or agent memory into E8 authoritative financial truth.

The adapter `bounded_review()` checks the same CASE-204, `retailer_a`, evidence version and `$500` fixture scope expected by Build 1, constructs the original typed `WorkRequest` and `Evidence`, and passes them to the existing `advise()` function. This deliberately avoids revising Build 1 or repackaging its public interface. The additional E1/E4 checks are upstream and visible; Build 1's strict C04 parser and validator still apply downstream. The returned `ReviewResult` contains a proposal, source reference, principal, observation age and the label `UNTRUSTED_C04_NOT_AUTHORIZATION`. There is no payment operation key or credential in this result.

## 24.5 Request-to-result behavior

![Build 2 sequence from simulated assertion verification through source lookup and advisory response.](assets/shared-figures/rendered/F24-02.png)

*Figure 24.2 — Behavioral sequence. The assertion verifier and context gateway check independently before the E3 fixture runs. Denied or unavailable context terminates the request; it does not initiate a payment or update RF-1042.*

The successful path has four relevant decisions. First, check the assertion signature and its bounded validity interval. Second, check that the source is in the purpose-specific allowlist. Third, retrieve a matching catalog record and validate its classification, identity, version and observation age. Fourth, pass the resulting evidence into E3 for a **review-only** C04 proposal. A failure in any earlier step ends the path without invoking a privileged financial interface.

A context outage is not an E8 provider timeout. A stale source is not a failed refund. A valid C04 proposal does not change E7 to `AUTHORIZED`, `DISPATCHED`, `UNKNOWN` or `CONFIRMED`. Those state names belong to the separate consequential-operation path. In the original Build 0 failure exercise, an unknown provider outcome still requires reconciliation under RF-1042; adding scoped context neither resolves nor resets it.

## 24.6 Run the reproducible learning path

From the book's edition-specific immutable repository revision, using Python 3.10 or newer, run these commands at the repository root. The expected denial scenarios exit with code 2; use separate invocations when observing their output.

```sh
python3 examples/refund-reference-system/build2/demo.py
python3 examples/refund-reference-system/build2/demo.py \
  --scenario injected
python3 examples/refund-reference-system/build2/demo.py \
  --scenario cross-tenant
python3 examples/refund-reference-system/build2/demo.py \
  --scenario stale
python3 examples/refund-reference-system/build2/demo.py \
  --scenario forged
python3 examples/refund-reference-system/build2/demo.py \
  --scenario outage
python3 -m unittest discover \
  -s examples/refund-reference-system/build2 \
  -p 'test_*.py' -v
python3 -m unittest discover \
  -s examples/refund-reference-system/build1 \
  -p 'test_*.py' -v
python3 -m unittest discover \
  -s examples/refund-reference-system/build0 \
  -p 'test_*.py' -v
```

The default and `injected` cases print `ADVISORY_ONLY`, `RECOMMEND_REVIEW`, a source identifier, `financial_effects: 0` and `authorization: NOT_GRANTED`. The latter two fields describe the fixture's call graph; they are not an audited payment-provider statement. `cross-tenant`, `stale` and `forged` print `DENIED_OR_UNAVAILABLE` with `ScopeDenied`. `outage` prints the same outcome category with `ContextUnavailable`. Their nonzero exit status is an intentional negative demonstration, not a shell failure requiring retry. The new test suite also runs repeated review requests against two prepared SQLite marker files and verifies the bytes remain unchanged; unlike the isolated Build 0 tests, it does not execute a payment adapter.

These results are reproducible without installing a cloud SDK, creating an account or supplying secrets. An arbitrary local Python process could still import Build 0 and call its fixture functions. The source isolation and unchanged-database tests demonstrate **which path this program followed**, not the impossibility of malicious runtime access. The protected denial required in Chapter 25 is therefore stronger and remains mandatory.

## 24.7 Decision and failure semantics

![Build 2 scope and context decision tree distinguishing denial, unavailability, and review-only advice.](assets/shared-figures/rendered/F24-03.png)

*Figure 24.3 — Decision representation, separate from architectural placement and request sequence. Only a sufficiently scoped, fresh observation reaches E3; no branch grants a financial effect.*

| Input or failure | Build 2 result | Engineering interpretation |
|---|---|---|
| Valid fixture assertion, permitted fresh `EV-204` | Review-only C04 proposal | Neither customer eligibility nor payment authority established |
| Signature tampered, expired or noncanonical | `ScopeDenied` | Reject identity assertion; never silently reconstruct scope from user text |
| Valid signature for other tenant or case | `ScopeDenied` | Authentication-like integrity is not resource authorization |
| Source not allowed, stale, mismatched or wrong version | `ScopeDenied` | Reacquire permitted, current evidence or escalate; do not guess |
| Context provider unavailable | `ContextUnavailable` | Preserve workflow ownership outside fixture; not a payment UNKNOWN |
| Narrative instructs immediate payment | Advisory data only | Negative result does not claim a live model is immune to prompt injection |
| Valid agent token proposes unauthorized `$500` refund | Review only, no E5 capability | Full independently protected refusal remains Chapter 25 acceptance criterion |

The actual tests inspect the strict contract and the negative cases, not just favorable output. For release assurance they still leave gaps: independently issued and revocable identity, authorization at every retrieval tool boundary, trusted provenance verification, replay resistance, privileged process separation, audit retention, distributed ownership and continuous operations evidence. Each missing mechanism has an architectural owner. E1 and E4 own identity/retrieval enforcement; E5 owns consequential authorization; E7/E8 own operational knowledge and business truth; E2 owns durable coordination; E9 owns verification and governance evidence. Builds 3–5 add selected mechanisms while production deployment requires its own risk-based controls and testing.

## 24.8 Six-lens engineering review

**Implementing engineer:** Locate the canonical JSON signature verification, strict field and timestamp checks, and unchanged Build 1 adapter; explain why a type-check alone is not cryptographic evidence. **Enterprise architect:** Trace C01, C02, C03, C04 and C05 boundaries without treating the fixture as nine services. **Advanced student:** Modify the source catalog to create stale, cross-tenant and malicious records, then reproduce deterministic rejection or review. **Security and assurance specialist:** Forge a seemingly valid agent identity by compromising the local fixture key; explain why E5 still needs an independent business authorization boundary in Chapter 25. **SRE/operator:** Distinguish `ContextUnavailable` from policy denial, and distinguish both from an unknown payment effect. **Business owner:** Determine whether provenance makes a recommendation more reviewable without claiming that source freshness guarantees refund fairness or customer eligibility.

A risk-based decision might accept this implementation as an offline teaching instrument. It would **not** authorize deploying the local HMAC issuer or in-process context gate to safeguard production payment credentials. A valid identity token cannot itself authorize the proposed $500 transfer. The engineering obligation is to demonstrate the missing enforcement, not conceal it behind a strong hash function or a fluent model explanation.

## 24.9 Exercises and transition

1. **Scope denial:** Issue a correctly signed assertion for a second tenant and demonstrate rejection. Explain which checks prevent accidental cross-tenant context access and which require independently protected E4 deployment.
2. **Provenance challenge:** Provide two delivery observations with different timestamps. Define the rule for choosing, reconciling or escalating rather than silently accepting the newest text as authoritative.
3. **Compromised key:** Create a new signed fixture assertion using the public demonstration key. Explain exactly why the HMAC check cannot prove real identity under local code compromise and why this does not authorize payment.
4. **Operational failure:** Inject context unavailability; identify the diagnostic evidence, who owns retry/recovery and which states must remain unchanged. Contrast with RF-1042 provider uncertainty from Build 0.
5. **Architectural defense:** Compare Designs A/B/C for an organization with reliable structured shipment records versus one with messy correspondence. State costs, review burden and negative-test obligations; do not treat the builds as autonomy maturity levels.

Build 2 makes an important engineering distinction executable: **context may inform a proposal only after scoped selection and review of its provenance; neither context nor an identity assertion grants authority over business effects**. Chapter 25 takes the deliberately harder step of protecting E5 from a compromised investigator holding a valid token. Chapter 26 then extends provider integration and authoritative reconciliation; Chapter 27 considers optional coordination and fencing where justified. Build 0 and Build 1 remain independently runnable controls throughout.
