# Chapter 35 — six-lens and selective-path engineering review

Scope: Part VII introduction and Chapter 35 against the conversation's reconstructed pre-Chapter-35, pre–Part VII-audit source state. This is an adversarial documentary review of available source, not a claim that the remote merged `main` commit was independently fetched, that six external reviewers read the manuscript, or that production controls were certified. The earlier full-volume audit of Chapters 1–34 remains the baseline for cross-book issues.

## Independent internal lenses

| Lens | Failure challenge | Observed Chapter 35 response | Residual obligation |
|---|---|---|---|
| Implementing engineer | Reader searches for a field/class that exists only in a proposed schema | Table 35.2 names exact `build*/` modules and explicitly distinguishes proposed production envelope from executed fixtures | Verify each production API and schema separately |
| Enterprise architect | Logical domains are mistaken for physically independent security principals | §35.1 and Figure 35.1 state responsibility versus isolation; C01–C09 are logical contracts | Independent E5 credential and E2 epoch validation remain absent |
| Advanced student (internal QA only) | Reader begins with Build 5 and assumes full agent/context integration | §§35.1 and 35.4 explicitly disclose Build 5 does not compose the Build 1/2 advisory/retrieval runtime | Chapter 36 must test synthesis without inventing runtime composition |
| Security/assurance | Forged human authority or valid agent token becomes payment approval | Tables 35.1–35.3 trace no-grant rejection to Build 3/security tests and independent E5 control | Hostile-host custody/revocation remain unverified |
| SRE/operations | Lost provider reply or stale coordinator triggers double dispatch | Figure 35.2, §35.5 and exact Build 4/5/reliability entry points demand original-operation read-only reconciliation | Live provider status and E5 current-owner fencing unimplemented |
| Business owner | A local green test bundle becomes certification or a new refund is counted as success | Table 35.4 and §35.6 require claim scope, outcome proof and accountable evidence owner | Real provider settlement and release/financial approvals external |

## Selective reader routes

- **Architecture-first:** Chapter 8 → Appendix A → Chapter 35 Table 35.1 → Chapter 25. C04 advisory cannot become independent C05 authority.
- **Build-first:** Companion root README → builds 0–5 READMEs + `architecture.svg` → Chapter 35 Table 35.3 → implementation evidence map. All six diagrams referenced; Build 5 limited composition explicit.
- **Security-first:** Chapters 25 and 29 → Build 3 `test_gate.py` / security `test_adversarial_cases.py` → Chapter 35 §35.4. Valid-token no-grant denial remains falsifiable.
- **Reliability-first:** Chapters 26, 28, 30 → Build 4 ledger/provider tests and reliability fixtures → Chapter 35 Figure 35.2. UNKNOWN requires original-effect query, no blind replay.
- **Governance-first:** Chapters 31–33 → proposed governance/release records → Chapter 35 Table 35.2. No implied production automation.
- **Economics-first:** Chapter 34 → Chapter 35 §§35.5–35.6. A cheaper system without E5 or provider evidence is ineligible regardless of cost.
- **Teaching-first:** Chapters 22–27 → Chapter 35 exercises. Require distinction among logical specification, executed fixture and external evidence.
- **CASE-204 trace:** E1/E2/C01–02 → E3/E4/C03–04 advisory → E5/C05 independent decision → E7/C06 RF-1042 → E6/E8/C07 → C08 reconciliation → C09 review. Logical reference path, expressly not the Build 5 executed call graph.

## Cross-book findings and disposition

1. **Resolved in patch:** Part VII reader introduction described Chapters 35–36 as undeveloped; now anchors 35 and avoids reader-facing future development status.
2. **Resolved in patch:** Chapter 35 schema table now distinguishes existing fixture modules from proposed governance/production records.
3. **Resolved in patch:** New chapter has explicit source-to-test crosswalk, negative tests, and no second Python build program.
4. **Resolved in patch:** C09 description replaced an opaque E1–E8 range with explicit responsibility words to satisfy the standing single-volume rule.
5. **Retained limitation:** Build 5 neither executes C03/C04 through the refund route nor provides E5 current-owner epoch enforcement. Neither omission is papered over.
6. **Retained limitation:** Local fixture tests cannot certify live provider idempotency, issuer custody, financial reconciliation, policy lifecycle, canary deployment or response-team staffing.
7. **Publication gate:** Chapter 36 remains a placeholder; final complete-volume 7×10 pagination, independently checked source passages and native Word-for-Mac print proof are still required. The standalone Chapter 35 document was locally rendered at 7×10 and observed at nine pages against ten allocated, but this does not establish complete-book pagination.

**Disposition:** Chapter 35 is fit for guarded development-branch review after passing the listed automated checks. The full book is not publication-certified. No review lens or war-game vocabulary is introduced into the chapter's reader-facing text.
