# ETIS — Deep adversarial integration war-game, Parts I–V (second pass)

**Input:** user-supplied post-Chapter-28 repository export with Git baseline `da8c31501a6cb3f83bc0caf4719f15bd11042be2`, plus the prior approved handoff patch applied to a working copy. **Not a fresh clone of the subsequent merge:** its per-file hashes are checked by the installer.

**Scope and method:** Inspect chapter bodies and headings, trace CAB-001/CASE-204/RF-1042 invariants, compare Chapter 26 and 28 claims against actual Build 4/5 modules, inspect seven test suites and the code/documentation evidence map, run source-level QA and targeted fault tests, and record each chapter’s adversarial question. This is deeper than the first static-only review but is **not** an assertion that every scholarly passage, every figure pixel or every possible attack has been verified.

## Confirmed findings and unresolved obligations

| ID | Severity / type | Evidence | Disposition |
|---|---|---|---|
| D-WG-01 | Major / confirmed editorial | Chapter 28 §28.7 refers to `CoordinatorStore` and `Coordinator`; neither is implemented in Build 5 (`DurableCoordinator` is). | Correct code-identifying prose and add a source-symbol preflight. |
| D-WG-02 | Major / confirmed evidence-loss | Build 4 `OperationalLedger.observe_unknown` replaces the current `observation` string after a previously `CONFIRMED` effect is contradicted. The old provider reference survives, but the original confirmation observation/source does not survive in the local state record. This hides an important sequence needed for recovery decisions. | Add transactionally recorded local E7 operation events; two adversarial tests preserve earlier confirmation and lost-ack chronology. It is NOT tamper-evident independent E9 audit. |
| D-WG-03 | High / known security limitation | A compromised same-UID worker and E2-to-E5 epoch bypass are outside the Build 5 security model. E5 never validates E2 ownership epochs. | Keep as explicit Chapter 29 attack and Chapter 31 negative verification obligations. No unverified finance code changes. |
| D-WG-04 | High / known operations gap | Local SQLite traces lack independently protected correlation, retention, tamper-resistance, operator authorization and live provider reconciliation. | Chapter 30 must add runbook/telemetry evidence, Chapter 31 must falsify claims against protected deployment boundaries. |
| D-WG-05 | Publication hold | Current archive supports source/figure-reference checks and LibreOffice development proofs, not native Word 7×10 integrated visual acceptance or independent exact citation verification. | Leave gate open and inspect full book before print. |
| D-WG-06 | QA execution limit | An uninterrupted `make check` started and passed static checks and Builds 0–2, but was stopped in the longer Build 3 suite within this runtime. | Run complete suite on Mac; do not assert full run passed. |

## Chapter-by-chapter adversarial judgement

| Chapter | Challenged proposition / source reviewed | Disposition |
|---:|---|---|
| 1 | Trustworthy-system thesis and promised reader path | No confirmed prose defect from this pass; Evidence-based claim; verify source-to-claim trace |
| 2 | Historical precedent versus analogy | No confirmed prose defect from this pass; Independent original-source passage and edition verification |
| 3 | Bounded business goal; Design A/B/C boundaries | No confirmed prose defect from this pass; Check no accidental autonomy endorsement |
| 4 | Agent definition and non-agent alternative | No confirmed prose defect from this pass; Business necessity vs technical fashion |
| 5 | Lifecycle costs and cost per acceptable outcome | No confirmed prose defect from this pass; No ROI without real baseline |
| 6 | Four uncertainties and authority | No confirmed prose defect from this pass; Distinguish model uncertainty and payment uncertainty |
| 7 | Acceptance obligations and judgement | No confirmed prose defect from this pass; Tests must be actionable, not philosophical |
| 8 | CAB-001 E1–E9 C01–C09 reference model | No confirmed prose defect from this pass; Figure and contract semantics vs later modules |
| 9 | Admission and identity distinct from payment grant | No confirmed prose defect from this pass; Service token cannot authorize RF-1042 |
| 10 | Durable owner and coordinator epochs | No confirmed prose defect from this pass; E2 fence must not imply E5 fence |
| 11 | Untrusted E3 proposal / C04 | No confirmed prose defect from this pass; Proposal identifiers cannot equal refund ID |
| 12 | E4 provenance/scope | No confirmed prose defect from this pass; Freshness cannot substitute E5 revalidation |
| 13 | Independent trusted E5 authority | No confirmed prose defect from this pass; Review is not OS privilege isolation |
| 14 | E6 adapter and E8 provider truth | No confirmed prose defect from this pass; No idempotency without actual contract |
| 15 | E7 durable state and E9 assurance | No confirmed prose defect from this pass; Current state is not the full evidence history |
| 16 | Logical protection zones vs physical deployment | No confirmed prose defect from this pass; Colocation does not imply isolation |
| 17 | Deterministic/hybrid/agentic choice | No confirmed prose defect from this pass; Design B conditional, not an autonomy ladder |
| 18 | Coordinator patterns and replacement | No confirmed prose defect from this pass; One logical owner not one permanent process |
| 19 | Tool adapter and effect isolation | No confirmed prose defect from this pass; Only independent E5/E6 authority controls money |
| 20 | State, memory, knowledge provenance | No confirmed prose defect from this pass; E4 memory not E8 financial truth |
| 21 | ADR and enforceable policy | No confirmed prose defect from this pass; Governance document not a permission boundary |
| 22 | Build 0 fixed deterministic refund | No confirmed prose defect from this pass; Single-host fixture not production payment |
| 23 | Build 1 bounded advisor | No confirmed prose defect from this pass; No financial import or credential |
| 24 | Build 2 signed fixture identity/scope | No confirmed prose defect from this pass; Same-process fixture not hostile isolation |
| 25 | Build 3 separate E5 process | No confirmed prose defect from this pass; Valid identity token still lacks finance grant |
| 26 | Build 4 E7/E8 uncertain outcome | **Corrected** in patch |
| 27 | Build 5 local E2 leases and takeover | No confirmed prose defect from this pass; E5 has no ownership epoch; fixture clocks injected |
| 28 | Logical zones, crash windows, read-only recovery | **Corrected** in patch |

**Interpretation:** “No confirmed prose defect” is not a proof of correctness. The chapter table identifies where an actual negative reviewer must concentrate in the next edition-specific source/figure pass. Chapter 26/28 and the linked Build 4/5 code received deeper source-to-source examination and executable test additions.

## Six-lens challenge record

| Lens | Specific falsification prompt | Evidence and result |
|---|---|---|
| Implementing engineer | Can I reproduce a provider confirmation later contradicted by provider truth, without losing the earlier observation? | **Previously no**: one mutable E7 observation. **Corrected** with transactional event records and two executable tests. |
| Enterprise architect | Does Chapter 28 point to real Build 5 classes, and does E2 ownership create financial authority? | Class names corrected; no E2→E5 epoch enforcement exists; CAB-001 responsibility separation retained. |
| Advanced student | Do physical failure domains follow automatically from logical zone boundaries? | Chapter 28 correctly denies this. Figure 28.1 still requires native print-size manual inspection. |
| Security / assurance | Can a valid investigator identity alone issue $500 RF-1042? Can a stolen finance grant or same-UID attacker reach E6? | No-grant denial tests exist. Full hostile-principal and stolen-grant denial are **unproved**, reserved for Ch29/31. |
| SRE / operations | Can an on-call engineer distinguish an earlier confirmation from a later contradictory status read? | **Corrected** local sequence retained; independent E9 audit, escalation, recovery role and runbook evidence remain Chapter 30 work. |
| Business owner | Can the system explain why `UNKNOWN` does not mean no refund, and why a new remedy requires fresh financial approval? | Chapter 28 decision narrative supports it; fixture provider does not establish real settlement. |

## Code and test applicability

- Builds 0–2: no source changes; existing baseline suites passed in the beginning of the interrupted aggregate `make check` run.
- Build 4: **27 tests passed** (25 existing + 2 new), including the contradictory-provider confirmation history and the lost-ack event chain.
- Source-to-code preflight, Chapter 28 acceptance, first-reference check, companion architecture checker and assurance handoff checker: **passed**.
- Builds 3 and 5: source reviewed; the complete uninterrupted aggregate test run was not certified in this runtime. The earlier baseline report recorded 18 and 22 passing tests, respectively, on the prior revision; a fresh Mac run is required.
- The Build 4 new events are inserted within the same SQLite transaction as each local state change, with sequence ordered by SQLite ID. Event data is readable by any actor with that database access; **never present it as secure, immutable, independent, timestamped, or externally replicated evidence**.
- The `build4/architecture.svg` label now identifies states plus local event history; it maps the **actual ledger module**, not a new service or new CAB domain. No running scenario identity, authority, or provider dispatch behavior changed.

## Remaining pre-Chapter-29 gates

1. Run an uninterrupted `make check` plus `make book-docx` on the Mac after applying the patch.
2. Manually inspect all developed figures in native Word at 7×10. Automated geometry and references cannot certify every visual label.
3. Independently verify external source-to-passage accuracy and editions rather than relying on citation-key checks.
4. Implement the Chapter 29 attack: valid stolen bounded-investigator E1 token, direct E6 attempt, no finance grant, independent E5 denial. Explicitly distinguish no-grant denial from stolen E5 finance credential and from same-UID compromise.
5. In Chapter 30 build independent protected event capture, UNKNOWN queue runbooks/roles, redaction, alerting, and an operational recovery drill with evidence; Chapter 31 must link release decision to runnable negative evidence.

**Decision:** This patch fixes two confirmed issues but does **not** declare full publication readiness. No Chapter 29 draft is introduced. Treat the second-pass war-game as **corrective action open pending Mac and human review**, not a final certification.
