# Engineering Trustworthy Agentic AI Systems

**ETIS Professional Computing Series — authoritative Markdown manuscript repository**

This repository contains a **single bound 7×10-inch, seven-part, 36-chapter** professional computing textbook. Chapters **1–17** have substantive developed content; Chapters **18–36** remain placeholders. This is not a publication-certified edition.

**Locked V12 production plan:** 550 finished pages = 485 chapter pages plus 65 supporting pages. Preferred maximum 575; planning limit 600; absolute maximum 700. The source-of-truth ledger is `publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json`.

## Authority and current status

- **CAB-001:** approved E1–E9 architecture and C01–C09 interface catalog; authoritative Word baseline preserved in `metadata/approved/`.
- **BP-001:** approved seven-part, 36-chapter publishing blueprint; preserved in `metadata/approved/`.
- **Chapters 1–7:** Part I developed; **8–16:** Part II developed, including the canonical layered Figure 8.1; **17:** Part III opening chapter developed.
- **Chapters 18–36:** editorial stubs only; do not count them as completed chapter pages.
- **Figures:** the current chapter source references 49 figures, with their source masters under `assets/shared-figures/sources/`; automated source/render/Word checks and native print review are separate gates.
- **Citations:** consolidated bibliography and BibTeX plus `references/source-register.md` provide claim mappings; precise original source passages, standards versions and final citation rendering require publication-level verification.
- **Review evidence:** `publishing/evidence/PARTS1_3_INTEGRATION_CERTIFICATION_2026-11-13.md` records the through-Chapter-17 integration corrections and remaining acceptance gates.

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

## Current production actions

1. Confirm the Chapters 1–17 integration correction in native Word for Mac, including Chapter 3's documented one-page V12 allocation variance.
2. Continue Chapters 18–36 as separate protected branches, enforcing chapter-specific V12 budgets and V9 figure standards.
3. Maintain exact claim-to-source verification as a distinct publication gate; no citation-presence script establishes full bibliographic support.
4. Recalculate the finished-page forecast from rendered 7×10 evidence after each major Part boundary.
5. Complete author/imprint/ISBN, glossary, index, permissions and the full-book QA process before publication.

## Current production build (macOS)

Graphviz (`dot`) and Python with CairoSVG are required for fresh figure rendering. In the repository root, keep dependencies inside a virtual environment rather than installing them into Homebrew Python:

```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install cairosvg python-docx pillow
PATH="$PWD/.venv/bin:$PATH" make figures && PATH="$PWD/.venv/bin:$PATH" make book-docx && PATH="$PWD/.venv/bin:$PATH" make check && PATH="$PWD/.venv/bin:$PATH" make check-figures
open dist/etis-agentic-ai-book.docx
```

The integrated Word manuscript uses draft Contents text; do not claim a final dynamic table of contents, index, or publication pagination. Inspect figures and captions at final 7×10 print size in native Word for Mac. Every V9 figure master, rendered image, and embedded Word image must agree; CairoSVG is required for fresh PNG regeneration.
