# Pre–Part VII selective reading-path audit

**Reading-mode distinction:** A visitor starting at a chapter has not automatically learned definitions from earlier chapters. First-reference explanations, local figure captions, exact companion directory/README links and simulation limits are therefore checked at the entry point. A path is viable only if its cross-references work **without granting unimplemented behavior**.

| Entry path | Suggested order (chapters) | Reader challenge | Evidence / disposition |
|---|---|---|---|
| Architecture-first | 8 → 13 → 16 → 17 → 18 → 21 → 33 → Appendix A | Where are independent effect authority, coordination and policy boundaries? | E1–E9 / C01–C09 map and A/B/C choice; **viable with earlier chapter definitions and appendix map** |
| Build-first | 22 → 23 → 24 → 25 → 26 → 27 → Appendix B | Can each build be run and understood in isolation? | `build0/README.md` through `build5/README.md` plus checked-in `architecture.svg` diagrams; **viable**, with reminder Build 5 does not call Build 2 advice |
| Security-first | 13 → 16 → 25 → 29 → 31 → 32 → 33 | Does a *valid* investigator assertion mint a payment approval? | `build3/test_gate.py`, `security/test_adversarial_cases.py`, and no direct C04→E6. **Viable at fixture scope**; no production secret isolation |
| Reliability-first | 15 → 26 → 27 → 28 → 30 → 31 → 33 | Can UNKNOWN be reconciled without replay? | `build4/ledger.py`, `build5/test_coordination.py`, `reliability/test_recovery_cases.py`, `operations/test_incident.py`; **viable, C08 provider reality external** |
| Governance-first | 6 → 13 → 21 → 29 → 31 → 32 → 33 → 34 | Who may say yes/no/stop/resume and why? | Finance grant, release decision, incident suspension and policy owner distinct; **viable**, actual independent human approval issuer external |
| Economics-first | 5 → 17 → 31 → 32 → 33 → 34 | What is the denominator for acceptable work and what is measured? | Chapter 34 common-case costing and hypothetical tables; **viable** when proposals vs verified outcome and unknowns are preserved |
| Teaching-first | 1 → 4 → 7 → 8 → 22–27 → 28–31 → 34 | Can an advanced student reconstruct the argument and falsify it? | First-reference checks, progressive tests, negative evidence and exercises; **provisionally viable**, empirical learning QA not performed |
| CASE-204 trace | 3 → 8 → 13 → 22–27 → 28–33 → Appendix B | Is RF-1042 preserved as one original effect through uncertainty? | Build 0 original operation, Build 3 independent authorization, Build 4 status-only lookup, Build 5 E2 ownership; **viable**, not a single end-to-end autonomous runtime |

## Enforced path-entry standards for Part VII

1. Chapters 35–36 must let readers find exact contract fields, schema statuses, and executable versus illustrative examples directly, without searching whole repositories or relying on internal CAB IDs.
2. Every companion locator must identify the root `examples/refund-reference-system/`, a real relative file, and a runnable named test or command where applicable.
3. Negative test outcomes must be described as locally executable *fixture observations*, not compliance or production proof.
4. Every path must explain that a valid E1 identity and even E2 ownership are not E5 transaction authorization.
5. The exercises in Chapter 36 should include *at least* a stale-owner/unknown-effect incident, valid-token attack, unsafe ROI request, human-veto/release decision, and deterministic-versus-agentic selection defense.
6. The final book must remove placeholder editorial status from Part VII and avoid importing internal review-lens names into reader-facing text.
