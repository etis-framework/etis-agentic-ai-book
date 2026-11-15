# Glossary

Terms below describe the architecture and developed implementation. The definitions are governed by the corresponding chapters and the ETIS reference architecture; this reader reference does not introduce new authority or implementation requirements.

**Acceptable completed workflow.** Case outcome meeting a declared standard for business disposition, financial authorization, recoverability and supporting evidence; an unresolved UNKNOWN does not count as completed.
**Accountable governance decision.** A version- and scope-bound approval, denial, suspension or restoration made by an authorized human under an identifiable policy; neither an advisory suggestion nor an automatic financial grant.
**Action proposal (C04).** Typed untrusted request and supporting evidence from agent reasoning (E3); a proposal, even if signed or provenance-bearing, is not transaction authorization.
**Admission and identity (E1).** Authenticates and scopes incoming work under a principal, tenant, purpose and constraints; neither a verified token nor a capability listing grants a refund.
**Advisory correlation identifier.** Identifier linking a proposed action, trace and review evidence; distinct from the trusted financial operation RF-1042.
**Agent.** Goal-directed bounded software component that selects permitted steps; it need not use a large language model or have authority to cause external effects.
**Agentic AI system.** Complete arrangement of software, people, data, controls and operations around one or more agents; the model alone is not the system.
**Assurance claim.** Narrowly stated behavior tied to system version, scope, threat model, execution conditions and responsible reviewer; must be backed by relevant, disprovable evidence.
**Authentication.** Establishing and verifying the claimed identity of an actor; independent of business authorization.
**Authoritative business system (E8).** System whose records govern external business facts, such as the payment provider's actual refund status; differs from an application's E7 observations.
**Authorization.** Enforced decision permitting a particular operation under policy, identity, scope, business facts and approval; stronger than authentication.
**Bounded advisory reasoning (E3).** Evidence-based reasoning constrained to proposed actions and traceable outputs without independent execution authority.
**Bounded delegation.** Explicitly limited software discretion over allowed tools, data, steps, cost, duration and actions, with external enforcement and escalation.
**Break-glass authority.** Exceptionally scoped, logged emergency privilege; it cannot convert an unknown payment effect into permission to resend.
**Canary activation.** A bounded rollout to a restricted cohort with explicit stop conditions; the percentage of traffic alone is not a limit on consequential risk.
**Capability registry.** E2-managed catalog of available and eligible workers/capabilities; discovery is not authorization.
**CASE-204.** The recurring fictional customer case concerning a proposed $500 refund; not a real customer or provider transaction.
**Competing histories.** Concurrent E2 ownership, E7 local intent and E8 external-effect observations that must be correlated without assuming a cross-store atomic commit.
**Consequential effect.** External business-state change, such as an actual financial refund, requiring independently controlled execution and recovery.
**Context observation.** E4/C03 evidence carrying source, version, classification, age and scope; not automatically authoritative E8 truth.
**ContextUnavailable.** Build 2 context dependency failure; separate from unauthorized scope and from UNKNOWN financial effect.
**Coordination and ownership (E2).** Logical responsibility for work admission from E1, routing, leases, epochs, assignment and workflow progress; does not hold financial authority.
**Cost per acceptable completed workflow.** Total attributable lifecycle cost for a defined period and cohort divided by the number of acceptable completed outcomes; include failures, denials and review labor in the numerator.
**Crash point.** Boundary immediately before or after a durable write, dispatch or external effect at which process death can change what participants know; see Chapter 28.
**Credential custody.** Control of the creation, storage, use, rotation, revocation and audit of secrets or signing keys, enforced outside lower-trust agents; a source-code import boundary alone does not establish custody.
**Cross-domain contract (C01–C09).** Named, independently reviewable responsibility handoff; see the appendix's compact mapping and Chapter 8.
**Decision contract (C05).** Independently evidenced policy and approval decision involving trusted execution (E5) and governance/assurance (E9).
**Decision right.** Authority to decide a defined action within boundaries of role, tenant, policy, transaction and time, subject to separation of duties and revocation.
**Design A / B / C.** Design A is deterministic; Design B uses bounded AI advice under independent review and trusted execution; Design C adds optional bounded agent investigation without payment authority. These alternatives are not compulsory production maturity levels.
**Dispatch claim.** Durable, atomic pre-dispatch assertion of a single operation's right to attempt an effect; not evidence that the provider completed it.
**Durable operational state (E7).** Persisted local workflow and effect-intent records, transitions and observations; storage and recovery mechanisms under accountable logical ownership.
**Effect ambiguity.** State in which an external consequential action may have occurred but available trusted evidence does not prove its outcome; UNKNOWN is not FAILED.
**Enforcement boundary.** Code- or infrastructure-controlled point that rejects unauthorized operations independently of untrusted proposals; logical module lines alone do not establish isolation.
**Epoch (ownership).** Monotonically advancing ownership generation used to reject obsolete coordinators at a boundary that actually verifies it.
**Evidence bundle.** Versioned set of registered tests, results, source digests, exclusions and outstanding gates; a local fixture bundle does not prove independent production trust.
**Evidence provenance.** Traceable source, time, identity and transformation context necessary to judge whether information supports a decision.
**Execution-boundary fencing.** Verification at E5 or another independently protected consequential endpoint that an instruction belongs to the current authoritative owner/epoch; not implemented by Build 5's E2-local epoch.
**Failure/deployment boundary.** Actual execution, persistence, or communication separation across which components can fail independently; depends on topology, shared infrastructure, and recovery design rather than E-domain notation alone.
**Falsifier.** Test or observation which, if it occurs, defeats a declared assurance claim even when other tests pass.
**Fencing.** Enforcement that rejects actions from an outdated owner. E2-local fencing in Build 5 does not prove E5-enforced end-to-end fencing.
**Fixture-verified scope.** Local, signed or otherwise validated educational identity/scope assertion; not equivalent to a production identity provider or business approval.
**Governance policy version.** The identified rules effective for a consequential decision, recorded with its evidence and re-evaluated across material changes.
**Hijacked bounded investigator.** Agent or worker whose advisory execution is attacker-controlled despite a legitimate scoped E1 identity assertion; not automatically entitled to finance operations.
**Human intervention.** Enforceable hold, denial, quarantine or authorized restoration at the appropriate trusted boundary, not merely a message to an agent.
**Idempotency key.** Stable request identity used under a provider's documented scope and retention guarantee to suppress duplicate effects; not a blanket exactly-once guarantee.
**Incident disposition.** Evidence-qualified operational recommendation to quarantine, inquire, escalate or review an unresolved workflow; not permission to execute a refund.
**Incident observer.** Chapter 30 read-only fixture in `examples/refund-reference-system/operations/incident.py` that classifies synthetic signals and existing Build 4/5 state without issuing an effect; see `operations/test_incident.py`.
**Incremental cost per additional acceptable outcome.** Difference in total lifecycle cost between comparable designs divided by the difference in acceptable completed outcomes, with a shared cohort and acceptance definition.
**Independent request-path enforcement.** An E5 subprocess checks consequential requests independently of advisory calling code; same-UID fixtures do not imply complete security isolation.
**Lease.** Time-limited coordination claim; expiry enables reassignment but does not by itself stop stale workers from reaching privileged endpoints.
**Lifecycle retirement.** Controlled withdrawal of future capability while preserving mandated records, provider reconciliation, privileges revocation and ownership of outstanding effects.
**Logical responsibility and failure zone.** A visualization of responsibilities, contracts, and evidence ownership; not a prescribed process, machine, network, or independent failure domain.
**Mock provider.** Simulated external service and E8 record used for reproducible education, not real settlement or bank truth.
**Observability evidence gap.** Missing, delayed, duplicated or inconsistent telemetry that lowers confidence in reconstructed sequence without proving the absence of a consequential effect.
**Operation identity (RF-1042).** Stable, trusted ID for the separately authorized CASE-204 payment operation; distinct from E3 advisory correlation identifiers.
**Operational reconciliation (C08).** Read-only verification of the original operation against available authoritative provider evidence; unresolved results remain UNKNOWN.
**Production release gate.** Explicit, accountable approval condition for a defined deployment and risk; safety-critical gaps cannot be offset with performance improvements.
**Provider dispatch (C07).** Controlled E5/E6 instruction to an external provider, governed by provider-specific contracts and uncertainty handling.
**Provider idempotency scope.** Exact semantics, key namespace, duration and amount/payload treatment under which the provider suppresses repeated effects.
**RASR.** Reliability, availability, serviceability and recoverability; quality attributes needing stated measures, not an automatic guarantee. Broader ETIS quality attributes include security, privacy, cost and others.
**Recovery authority.** Separately authenticated, scoped permission to inquire, adjudicate or remediate an existing operation; status-only inquiry does not confer authorization for a new payment.
**Reference artifact.** A typed decision, contract, operation or evidence record with an identified owner, scope, falsifier and implementation/evidence boundary; see Chapter 35.
**Release candidate manifest.** A proposed independently protected record pinning versions, evaluation evidence, residual gaps, ownership and release scope; not provided as a Python schema.
**Release readiness.** Evidence that independently authorized controls, operators, incident response, recovery, monitoring and stop mechanisms can support the intended live scope.
**Responsibility boundary.** Architectural division establishing ownership of a decision, record, or action; does not alone prove a physically isolated fault or enforcement point.
**RF-1042.** See *Operation identity (RF-1042)*.
**Risk-adjusted decision.** Architecture and investment decision evaluating plausible impact and uncertainty only after non-negotiable safety, authority and compliance gates are satisfied.
**Rollback boundary.** The distinction between reverting software exposure for future work and preserving already committed or uncertain external business effects.
**Security falsifier.** Reproducible attack input and expected independent denial point, accompanied by checks for absent downstream effects within a stated test boundary.
**Service-level objective (SLO).** Explicitly scoped target for a service indicator, denominator and window; not a substitute for an independent financial correctness invariant.
**System of record.** Authoritative owner of a specified business fact; retrieved context or an AI-generated summary does not replace it.
**Transaction-specific approval grant.** Separately issued, case/tenant/amount/policy-bound artifact that E5 verifies; a signed local demonstration grant does not simulate real finance approval infrastructure.
**Trust/enforcement boundary.** Independently controlled check that can reject unauthorized actions at the receiving consequential interface; distinct from diagram grouping and physical deployment.
**UNKNOWN (external effect).** Application knows that an external effect may have occurred but lacks conclusive provider evidence; never equivalent to FAILED and never permission to create a second operation.
**Workflow.** Accountable process coordinating deterministic tasks, agent work, human decisions and recovery; not necessarily agentic.
**Workload identity.** Authenticated service or runtime principal used to obtain purpose-, audience- and time-bounded access; it is not transaction-specific business approval.
