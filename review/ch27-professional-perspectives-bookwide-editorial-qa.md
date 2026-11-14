# Chapters 1–27 — Professional Review Perspectives Editorial War-Game

**Scope:** Incremental Chapter 27 branch patch, manuscript/editorial infrastructure only. Do not mistake reader-facing professional review perspectives for the internal six-lens manuscript assessment method.

## Editorial decision

Professional architectural review uses the responsibilities of implementing engineer, enterprise architect, security/assurance, SRE/operations, and business owner. These are **perspectives**, not E-domain additions, approval grants, a mandatory five-member committee, a substitute for authorized sign-off, or an alternative to architecture contracts. Students learn by doing the professional exercises; their comprehension is evaluated separately in ETIS's **internal** six-lens QA.

## Chapter-by-chapter disposition

| Chapter range | Action | Editorial rationale |
| --- | --- | --- |
| 1 | Contextual stakeholder questions ahead of first worked design review | Introduces the idea without formal checklist |
| 2–4 | Retain existing discussions and exercises | No need to force a role checklist into historical/agent definitions |
| 5 | Tie perspectives to business-pilot economics | Real cross-functional economic decision |
| 6 | Retain existing identity/authority and operator roles | Already clear without duplicate rubric |
| 7 | Introduce the explicit professional evidence-elicitation technique | Requirements and accountable decision rights |
| 8 | Short professional challenge of the canonical reference architecture | Reinforces architecture-derived evidence under strict word cap |
| 9–12 | Retain domain-specific contracts and reviews | Avoid generic boilerplate replacing domain reasoning |
| 13 | Retain detailed independent enforcement treatment | Chapter was already exactly at 3,000-word cap; introductory review technique and Chapter 16 provide needed bridge |
| 14–15 | Retain integration, business truth and operational state coverage | Existing domain-specific assurance obligations already explicit |
| 16 | Review placement and credential-isolation tradeoffs | Cross-functional deployment boundary |
| 17 | Review reversible ADR choices | Preserves alternatives and evidence |
| 18–20 | Retain existing patterns and tradeoffs | Relevant concerns present; no artificial rubric |
| 21 | Explicit perspectives and decision authority in ADR review | Governance is enforceable, not consensus by label |
| 22–27 | Normalize concise five-perspective professional architecture reviews; exercises separate | Eliminates internal “advanced student” reviewer and six-lens/war-game headings in reader-facing material |

## Six internal QA perspectives (not a reader-facing six-role board)

1. **Implementing engineer:** Edited prose preserves the source relationships, fixture limits, and code/test evidence; no Python code or build-specific architecture SVG changed.
2. **Enterprise architect:** CAB-001 E1–E9 and C01–C09 remain untouched. No new services or mandatory topologies are invented. E5 independent authority, E2 local fencing, E7/E8 truth separation remain intact.
3. **Advanced student (internal pedagogy QA):** Readers encounter the practice first in foundational questions, then requirements, reference architecture, ADRs and explicit build reviews. Student learning exercises remain in each build chapter, not an enterprise authority role.
4. **Security/assurance:** Perspectives never mint finance approval; local fixture keys/process isolation remain caveated. Security claims are tested against a compromised valid-token investigator rather than a diagram label.
5. **SRE/operations:** UNKNOWN, durable intent, no blind resend, ownership epochs and controlled reconciliation remain the operational acceptance questions.
6. **Business owner:** Conditional Design B choice, measured benefit, customer communication and actual financial approval retain accountable ownership; the review technique does not replace release approval.

## Verification and publication gates

- Added an executable editorial gate to `make check`. It confirms all developed chapter source files exist; the Part IV professional review appears in Chapters 22–27; the public build text does not name advanced students as an architecture approval role or expose internal six-lens/war-game section headings; and the reader navigation and editorial standard exist.
- Edited-chapter acceptance, first-reference and V12/single-volume word checks must pass without increasing caps. Chapter 8 has a particularly strict independent 3,000-word gate; Chapter 13 is at the cap and deliberately not expanded.
- Full DOCX rebuild and figure identity checks must pass; no figures, Python code or companion README diagrams are changed. Native Word for Mac print/pagination and authoritative external citation-page verification remain open publication tasks.
- **Risk:** An automated name/heading audit cannot judge if a professional concern is genuinely helpful; a future editor must still remove empty ritual review questions.

**Decision:** Editorial structure is appropriate for Part IV closing and future chapter development **subject to actual local `make check` and native Word review**. This is not a financial-production certification.
