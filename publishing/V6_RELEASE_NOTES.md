# V6 integrated revision — editorial and publishing review

This patch is an incremental update to the existing V5 source tree. It is not a finished 36-chapter manuscript.

## Editorial revisions

- Expanded copyright from a weak placeholder into a structured rights, bibliographic, permissions, and technical-notice page. Legal owner, ISBN, imprint, and publication data remain controlled blanks.
- Rewrote Preface to establish a mature enterprise engineering perspective: demonstration versus operational trust, historical inheritance, explicit delegation, evidence, and lifecycle responsibility.
- Rewrote Introduction around the production-launch questions that follow a successful AI demonstration; made RASR, security, privacy, performance, scalability, economics, maintainability, ethics, governance, and brand trust first-class architectural inputs.
- Expanded How to Use This Book and Part I opener; added Chapter 1 and 2 enterprise-obligations passages to establish continuity into later architecture and implementation.
- Rebuilt Figure 2.4 from DOT source with SVG/PNG output, explicit provider observation and operational state ownership.

## Publishing corrections and constraints

- The Contents page is now a visible 36-chapter/7-part **development outline**, not a broken field. Page numbers are intentionally absent until final pagination; this is a known open issue, not a completed page-numbered TOC.
- Word section metadata retains Roman preliminaries and Arabic page 1 at Chapter 1. Native Word for Mac must certify right-hand opening parity; LibreOffice rendering cannot prove it.
- No dedication or acknowledgments are assembled. Back matter retains controlled stubs, and 34 chapters remain stubs.

## QA evidence

- `make book-docx` completed on the staged source tree.
- `check.py` found 36 chapters and 29 SVG masters.
- `check_figures.py --built` verified 7 chapter figure references and embedded images.
- The generated Word file was rendered to PDF (83 pages) and the first fourteen pages were reviewed as a contact sheet; Contents was checked by extracted PDF text. Figure 2.4 PNG was visually inspected.
- This is a substantive editorial revision, **not** a full citation audit or final professional typesetting certification.

## Reader war game — remaining gates

- Junior engineer: Chapters 3–36 must supply progressive worked examples, definitions, and tests.
- Architect: map each quality attribute to scenarios, tradeoffs, interfaces, and evidence.
- Security and privacy: complete threat, data, retention, access, and appeal reviews.
- SRE/operations: verify failure modes, SLOs, unknown-outcome recovery, and incident readiness.
- Executive/business: quantify cost per successful outcome and residual risk acceptance.
- Editorial: final page-numbered TOC, historical references, index, recto verification, figure print QA, and publication metadata.
