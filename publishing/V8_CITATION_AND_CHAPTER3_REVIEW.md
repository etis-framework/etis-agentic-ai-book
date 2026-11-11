# V8 editorial and engineering review — Chapters 1–3

## Scope and limits

V8 adds a substantive Chapter 3 with four original editable DOT figures and renders, in-text author–year references to Chapters 1–2, four additional scholarly/standards bibliography records, and a claim-to-source audit table. This patch does not certify every statement in the manuscript, resolve all historical priority questions, or imply that the full 36-chapter book is finished.

## Review lenses

- **Developing engineer:** vocabulary before identifiers; worked case; explicit decision table; stepwise exercises.
- **Architect:** distinguish process from agent, logical responsibilities from deployment, delegation from authority, and alternatives from prescriptions.
- **AI engineer:** bound model access, steps, outputs and tools; evaluate interpretation separately from system-level effects.
- **Security/privacy:** tenant scope, least privilege, untrusted content, independent enforcement, human escalation.
- **SRE/reliability:** UNKNOWN outcomes, stable operation identity, reconciliation, operator intervention and evidence.
- **Instructor:** objectives, four figures, worked example, exercises and review standard.
- **ETIS:** requirement → decision → control → verification → release → operational evidence.

## Citation integrity

Citations are deliberately in readable author–year prose because the current Pandoc build does not use `--citeproc` and does not yet link the BibTeX file. This avoids emitting raw citation syntax into the Word manuscript. The source register now tracks claim locations and known limitations. Bibliographic identification was checked for four new entries using scholarly/publisher/standards listings. Other existing V7 entries are not newly certified.

## Open gates

1. Finish page-level or section-level primary-source checking for Chapters 1–3.
2. Pin living OWASP guidance to an edition before publication.
3. Audit every rendered figure at final physical print size, not only raster dimensions.
4. Verify Word-for-Mac pagination and table readability in final trim.
5. Decide final citation style and automate citations consistently across all chapters.
6. Conduct independent technical and pedagogical peer review of Chapter 3.
