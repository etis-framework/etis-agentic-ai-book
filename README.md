# Engineering Trustworthy Agentic AI Systems

**ETIS Professional Computing Series — book source repository scaffold**

This repository is the Markdown source of truth for a proposed 300–500-page, seven-part, 36-chapter professional computing book. It is a *working editorial repository*, not a complete manuscript or certified publication release.

## Authority and status

- **CAB-001:** approved technical architecture; preserved verbatim under `metadata/approved/`.
- **BP-001:** approved seven-part, 36-chapter publishing blueprint; preserved verbatim under `metadata/approved/`.
- **Chapters 1–2:** substantially revised Markdown drafts for review, incorporating the annotated Word comments; not yet publication-approved.
- **Chapters 3–36:** explicit stubs, not drafted content.
- **22 figures:** imported from G1.2 in SVG and PNG; visual design accepted but standalone semantic QA and final placement remain open.
- **Bibliography:** initial candidate sources; claim-level verification and citations remain outstanding.

## Start here

```bash
make check
make chapter CH=01 FORMAT=docx
make chapter CH=02 FORMAT=docx
make book-docx
make book-html
```

PDF generation is conditional on a LaTeX engine. `dist/` is generated and excluded from source control.

## Working principles

The book teaches agentic AI as an **evolution of enterprise computing**. It distinguishes an AI model, a goal-directed agent, an agentic workflow, and the complete engineered system. It explains inherited patterns, architectural alternatives, implementation mechanisms, failure and recovery, and verifiable evidence. It is intended for junior engineers to learn and build and experienced engineers to review and use.

## Repository boundaries

`manuscript/` contains chapter source; `assets/` shared graphics; `references/` bibliography and source verification; `examples/` running implementation; `metadata/` frozen baselines, catalogs and quality standards; `publishing/` build scripts; `archive/` prior Word drafts and review evidence. Keep shared diagrams authoritative in one location. Chapter-local `figures/` is for figures unique to that chapter.

## Known next actions

1. Review Chapters 1–2 for duplication and depth, and add verified claim-level citations.
2. Add teaching illustrations only when they materially improve the story and pass standalone-clarity QA.
3. Refine approved figure masters semantically before final manuscript placement.
4. Implement production-grade PDF layout, cross-reference/index processing, and full QA gates.
5. Expand later chapters only after the opening chapters and build system pass review.


## V5 production build (macOS)

From the repository root, install Python dependencies in a virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install python-docx
export PATH="$PWD/.venv/bin:$PATH"
make book-docx
make check
open dist/etis-agentic-ai-book.docx
```

In Word, select **References → Update Table → Update entire table** to populate the TOC. Review `publishing/PRODUCTION_QA_V5.md` before approving pagination.
