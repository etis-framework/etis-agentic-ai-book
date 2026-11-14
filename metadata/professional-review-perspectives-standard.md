# Professional multi-perspective architectural review — editorial and engineering standard

**Purpose.** Readers should learn to examine architectural claims through the responsibilities of those who implement, design, secure, operate and sponsor a system. This is a **review technique**, not a new CAB-001 domain, cross-domain contract, organizational unit, approval grant or mandatory five-seat review board. A person may cover several responsibilities; specific authority still belongs to the organization's approved governance and decision rights.

## Reader-facing professional perspectives

- **Implementing engineer:** exact contracts, source implementation, validation, failure handling, tests, maintainability and reproducible evidence.
- **Enterprise architect:** E1–E9 responsibility and C01–C09 contract alignment, placement, topology, integration and tradeoffs.
- **Security and assurance:** identity versus business authorization, least privilege, privacy, hostile behavior, independent enforcement and evidence of denial.
- **SRE/operations:** availability, ownership, concurrency, unknown outcomes, telemetry, containment, recovery and incident readiness.
- **Business owner:** benefits and costs, correctness, financial exposure, human accountability, unacceptable outcomes and the approval/risk decision.

## Progressive editorial use

1. **Chapters 1–6:** introduce differing stakeholder questions only when the foundational topic makes them useful. Do not reproduce a role checklist.
2. **Chapter 7:** introduce professional review as requirements/evidence elicitation, distinct from actual release authority.
3. **Chapters 8–16:** apply relevant perspectives to derive and challenge responsibility, trust, deployment and contract boundaries. Emphasize Chapters 8, 13 and 16; do not insert a ritual five-role section in every E-domain chapter.
4. **Chapters 17–21:** use perspectives for alternatives, tradeoffs, architecture decision records and reversible decisions; emphasize Chapters 17 and 21.
5. **Chapters 22–27 and subsequent developed build chapters:** use an explicit, concise multi-perspective architecture review, followed by **separate reader exercises**. Each review must name a specific architectural claim, code/test evidence or remaining limitation. Do not present the classroom learner as an enterprise stakeholder.
6. **Parts V–VII:** use perspectives where they strengthen failure, assurance, operational governance, economic or reference decisions. No requirement for all five in every chapter.

## Separation from internal manuscript QA

Internal **six-lens war-game**: implementing engineer, enterprise architect, advanced student, security/assurance, SRE/operations and business owner. This includes the advanced student to assess pedagogy, accessibility and learning progression. It belongs in `review/` evidence, *not* reader-facing architecture-review role lists. Students perform professional review exercises; they are not presented as a separate enterprise design-approval authority.

## Review and quality gates

- Be precise about E/C responsibilities, CASE-204, RF-1042, Designs A/B/C and Builds 0–5. Do not treat a perspective or a review as an authorization.
- Check whether a perspective adds a **distinct question, risk, evidence demand or decision**; remove repetitions. Keep page allocations and front/back-matter navigation aligned.
- Every developed Part IV chapter must include a reader-facing professional review and separate exercises. Avoid the headings `six-lens` or `war-game` for those sections; those terms remain appropriate in internal review artifacts.
- Keep the professional roles separate from the six-lens internal QA record and the business's actual named accountable approvers. Run `python3 publishing/scripts/check_professional_review_perspectives.py` plus existing acceptance/first-reference/V12 checks. Automated checks are preflight, not semantic certification.
