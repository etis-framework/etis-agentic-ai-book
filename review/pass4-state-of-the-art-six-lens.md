# Certification Pass 4 — state-of-the-art engineering and six-lens war-game

**Audit baseline:** 2026-11-16 user-supplied `ETIS_PASS4_BASELINE.tar.gz` (no `.git` history). This is a source snapshot; the user's clean `main` claim is not an independently verified commit SHA. Patch hashes therefore protect each changed file rather than assume a Git parent.

**Scope:** all 36 manuscript source chapters, Parts I–VII, Appendix A–C, 99 referenced figures, companion Builds 0–5 and four reliability/security/operations/assurance fixture families, source register, bibliography, glossary, and index. Inspection combined a full-file structural/coverage inventory with deeper examination of selected design and implementation paths. This was **not** six independent human cover-to-cover line-by-line readings and is **not** production certification.

## State-of-the-art engineering coverage and decision

The vocabulary is assessed by the engineering problems it solves, not by keyword counts. Evidence classes: **mentioned**, **explained**, **architected**, **implemented in local fixture**, **locally verified**, **production evidence missing**.

| Concern | Existing manuscript navigation | Companion and test evidence | Pass 4 decision and limitation |
|---|---|---|---|
| Context assembly, scope and freshness | Ch12 §§12.3–12.8; Ch20; Ch24 | `build2/context.py`, `build2/identity.py`, `build2/test_scope.py` | **Strengthened:** explicit context selection/truncation and evidence-fidelity evaluation. Scope/staleness covered locally, not an enterprise retrieval platform. |
| Working, case and authoritative memory | Ch12 §§12.5–12.6; Ch20 | Build 2 bounded context; Build 4 durable state (different owner) | **Strengthened:** cross-task poisoned memory exercise. Persistent memory lifecycle **specified only**; no fixture store for cross-session retention or deletion. |
| Long-horizon trajectories and evaluation | Ch4 evaluation discussion; Ch17; Ch31 §§31.3–31.5; Ch36 | `assurance/collect.py`, `assurance/test_collect.py`; selected deterministic negative tests | **Strengthened:** intermediate harmful action, repeated-trial metrics, uncertainty. No quantitative model cohort, longitudinal benchmark or production statistical guarantee. |
| Identity and scoped delegated authority | Ch9–10, Ch13, Ch18, Ch29, Ch32 | `build2/test_scope.py`, `build3/test_gate.py`, `security/test_adversarial_cases.py` | **Substantially covered.** Valid token is not finance authority. Same-UID local subprocess ≠ protected production credential custody. |
| Tool and peer interoperability | Ch4, Ch18–19, Ch35; new Ch19 §19.2 | Read-only tool calls; no MCP or A2A implementation | **Strengthened:** version-pinned MCP vs A2A and trust handoffs. Protocol conformance and peer trust **intentionally outside executable scope**. |
| Agent adaptation and lifecycle | Ch10, Ch21, Ch33–34 | No autonomous self-modifying build | **Strengthened:** model, memory and tool version changes require governed release; self-modification remains **specified/out of scope**. |
| Runtime invariants and effect fencing | Ch13, Ch25–31, Ch35 | `build3/test_gate.py`, `build4/test_provider.py`, `build5/test_coordination.py` | **Strong local evidence, explicit gap:** E2 epoch is not independently checked by E5; provider is simulated. |
| Agentic observability and recoverability | Ch28–31; Ch33 | `operations/test_incident.py`, `reliability/test_recovery_cases.py`, Build 4 | **Strong local evidence.** No live payment provider, signed production audit trail or deployed SLO. |
| Multi-agent propagation and coordination | Ch18, Ch27–29 | Build 5 deterministic ownership/epoch tests | **Architected + locally verified in limited scope.** No full agent-to-agent protocol or end-to-end combined Build 1–5 runtime. |
| Multimodal and computer-use surfaces | Ch19 §19.2 | No computer-use fixture | **Boundary treatment included; implementation intentionally out of scope.** Future UI and physical-actuation claims need additional controls. |
| Agent simulation/digital twins | Ch22–31 simulated provider and failure exercises | Builds 0–5 plus failure, security and incident fixtures | **Implemented as educational simulation, not a validated enterprise digital twin.** |
| Cost per acceptable completion | Ch5, Ch17, Ch34; Ch36 | Fixture execution, not actual workforce/cost telemetry | **Architected.** Real ROI and lifecycle economics remain unmeasured. |

## Six internal adversarial review lenses

1. **Implementing engineer:** Can follow source modules from Appendix B and `examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md`; must not confuse proposed context/memory or protocol designs with modules. This pass adds explicit nonimplementation language. **Residual:** no merged end-to-end Build 1–5 runtime.
2. **Enterprise architect:** Logical E1–E9/C01–C09 responsibilities remain separate from deployment topology. MCP/A2A can change the transport but not authorize `RF-1042`; system of record remains E8. **Residual:** deployment/independent E5 protections require site-specific design and proof.
3. **Advanced student (internal QA only):** Chapters 12, 19, 20 and 31 now give explicit self-contained problem statements and falsifiers. **Residual:** some optional advanced interfaces have no runnable code; this limitation must remain obvious.
4. **Security/assurance:** Challenge valid-token hijack, memory laundering, context injection, wrong-tenant retrieval, corrupted source, forged peer progress and stale E2 ownership. **Residual:** credentials, independent finance signer, A2A peer verification and production audit custody cannot be certified by fixtures.
5. **SRE/operations:** Trace unknown provider effect, worker replacement, safe stop, read-only reconciliation and release rollback. **Residual:** local tests do not establish live provider idempotency, operating SLO or 24×7 responder readiness.
6. **Business owner:** Evaluate Designs A/B/C against acceptable case outcomes, review work, unresolved-loss exposure and retirement. **Residual:** numerical economics remain illustrative, not measured ROI.

**Seventh currency challenge:** Official 2026 MCP transport revisions, A2A 1.0 and NIST's AI Agent Standards Initiative were checked for scope and publication date. The book now names protocol versions only as *examples*, avoiding claim that they certify enterprise business authorization. See the machine-readable source register for exact URLs and verification boundary.

## Eight selective reading journeys

| Reader entry path | Verified navigation | Adversarial question | Outcome |
|---|---|---|---|
| Architecture-first | Ch8 → Ch9–16 → Ch18–21 → App A/Ch35 | Does E5 own effect permission regardless of topology? | Yes; logical versus physical limitations retained. |
| Build-first | Ch22–27 → six README source diagrams → App B | Do tests reproduce claimed guarantees? | Local fixtures support scoped claims; no consolidated production platform. |
| Security-first | Ch9/13 → Ch25/29 → Ch31/32 | Does a valid agent token create a refund? | No; independent E5 denial tests; protected deployment still unproven. |
| Reliability-first | Ch15/26 → Ch28/30/33 | Can UNKNOWN become FAILED on timeout? | No; status inquiry and original operation identity preserved. |
| Governance-first | Ch21/29 → Ch32/33 → Ch36 | Can change approval be confused with financial approval? | No; Pass 4 clarifies learned/model/tool changes need release control. |
| Economics-first | Ch5/17 → Ch34/36 | Is model-call cost the outcome denominator? | No; acceptable-workflow lifecycle costing, measured data absent. |
| Teaching-first | Ch1–4 → Ch22–27 → Ch31/35/36 | Can a learner distinguish code, model, policy and actual effect? | Yes conceptually, with explicit limitations and runnable fixtures. |
| CASE-204/RF-1042 trace | Ch3/8 → Ch11–15 → Ch22–29 → Ch31–36 | Can advisory correlation mint a trusted refund? | No; E5 minted identity and E8 confirmation remain separated. |

## Publication positioning challenge

Retain **Engineering Agentic AI Systems** / **Build, Secure, Verify, and Operate Trustworthy AI Agents**. This accurately describes the architecture-first and executable-evidence strengths. A new “context engineering” or “multi-agent” title would overpromise breadth and underplay independently governed consequential action. Back-cover/retail review can describe bounded autonomy as a key differentiator without changing the established title or promising production-certified implementation.

## Findings register and release posture

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| P4-01 | Major | Context engineering and poisoning were implicit, with no explicit cross-task falsifier | Corrected in Ch12/20 and source/register; executable cross-session memory store intentionally absent. |
| P4-02 | Major | MCP/A2A roles and implementation limits were not separately explained | Corrected Ch19, citations and index; interoperability tests intentionally outside reference build scope. |
| P4-03 | Major | Long-horizon final success could obscure unsafe intermediate trajectory | Corrected Ch31 with metrics, sample/repeated-trial limitations; real dataset remains a production gate. |
| P4-04 | Moderate | Self-modifying or dynamically changing agents lacked an explicit release-control statement | Corrected Ch33; no automatic self-improvement mechanism introduced. |
| P4-05 | Publication blocker | Full native Word-for-Mac page parity, 575 versus ~453 preliminary proof discrepancy, exact TOC/index fields, entire figure/table print inspection | **Open; Pass 5**. V12 allocation checker does not measure final page count. |
| P4-06 | Source blocker | Full claim-to-edition/page verification across all references (including licensed standards) has not been independently completed | **Open; source/permissions gate**. Selected 2026 public protocol/initiative source identities verified only. |
| P4-07 | Production limitation | E5 current E2 epoch enforcement, real provider settlement, independent secrets/audit and integrated end-to-end runtime absent | **Open and disclosed; not falsely fixed by local tests**. |
| P4-08 | Publication blocker | ISBNs, cover/spine, fixed edition tag and signed final-release evidence | **Open; Pass 6**. |

**Disposition:** Pass 4 technical/editorial improvements are eligible for guarded integration after repository-wide regression. Final book state: **NOT CERTIFIED** for print or production. A fresh audit remains necessary after source changes and once the native Word print master is fixed. No internal six-lens role names were introduced into newly edited reader-facing sections.
