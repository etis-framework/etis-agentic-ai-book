# ETIS Professional Series — chapter acceptance standard (V7)

Each completed chapter must pass **all** of these checks before being marked complete:

1. **Teaching:** explain why the subject matters, provide learning objectives, define unfamiliar terms on first use, build the argument in an intelligible sequence, and close with exercises that test judgment rather than recall alone.
2. **Technical rigor:** distinguish assumptions from guarantees, model behavior from system behavior, local state from external truth, and recommendation from authority. Include an adverse scenario and an alternative architecture where applicable.
3. **ETIS engineering evidence:** connect business requirement → decision → enforced control → verification → release/operations. Identify who owns each consequential decision.
4. **Quality and ethics:** address applicable reliability, availability, serviceability, recoverability, security, privacy, performance, cost, maintainability, fairness, and business trust requirements as measurable obligations.
5. **Sources:** use academic, standards-body, primary research, or credible industry engineering references; map significant sourced claims to exact source passages. Do not imply that a paper proves production safety or that a vendor capability is an enterprise guarantee.
6. **Figures:** diagrams have a reader-facing purpose, readable labels at print size, explicit trust/authority boundaries, correct arrow semantics, and a caption that can stand alone. Prefer meaningful names to E1–E9 or C01–C09 shorthand in teaching prose.
7. **Reference use:** headings and definitions support direct lookup; worked examples state inputs, assumptions, decisions, failure behavior, and verification evidence.
8. **Production QA:** chapter renders without clipping or overlap, figures are legible, tables fit the page, references resolve, and no editorial placeholders masquerade as finished content.

## Reader notation policy

Name a responsibility before introducing its code: **trusted execution (E5)** at first formal use, then **trusted execution** in prose. Keep codes in contracts, diagrams, cross-references, and the architecture appendix when they add precision. Do not expose internal production identifiers in reader-facing teaching material.
