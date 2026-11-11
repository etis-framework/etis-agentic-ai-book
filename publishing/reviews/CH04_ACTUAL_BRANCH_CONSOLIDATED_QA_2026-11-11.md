# Chapter 4 — consolidated corrective review against uploaded repository archive

**Review date:** 11 November 2026. **Baseline:** user-supplied `etis-agentic-ai-book-current.tar.gz` (source Chapter 4 was *still a stub*; its `dist/` DOCX contained Chapter 4 but was not authoritative source). The working-copy source was built by applying the initial development patch and the later corrective overlay in that order, then replacing all three F04 figures with precise SVG source masters and updating the mechanical tests. A hash-checked installer supports both the actual uploaded source snapshot and the initial development-patch state previously shown in `git status`.

## Editorial dispositions and actual source edits

| Area | Disposition |
|---|---|
| Chapter 1 | Unchanged, read for continuity |
| Chapter 2 | Initial development patch's Figure 2.4 paragraph placement retained; no substantive rewrite |
| Chapter 3 | Unchanged, preserves Design B as initial production choice |
| Chapter 4 | Substantive manuscript from previous corrective overlay; classical versus modern agents, typed controller envelope, feedback, OWASP threats, τ-bench-style evaluations, initial Design B vs explored Design C; corrected OpenAI reading-list year 2025→2026 |
| Part I opener | Corrected obsolete “Chapters 3–7 planned” claim and normalized table chapter titles |
| Bibliography | Retains added Anthropic, OpenAI, τ-bench, OWASP Agentic, MCP sources in both book bibliography and BibTeX; source register updated |
| F04-01 | New editable SVG master with agent-only boundary, trusted controller/tool boundary, scoped objective, action proposal, read observation, and clear loop |
| F04-02 | New three-column diagram with actual alternative flow paths and feedback; NOT stacked stages; green absent |
| F04-03 | New independently bounded proposal, policy/approval, trusted dispatch, and distinct CONFIRMED versus UNKNOWN outcomes; green used solely for CONFIRMED |

## Figure standard and why two previous patches failed

`publishing/FIGURE_STANDARD_V9_MANDATORY.md` is normative. Earlier figures passed basic graph generation but not trustworthy design inspection; previously asserted figure QA was wrong. These figures have precisely positioned SVG masters at **5.75in final figure width** with editable vector content, Arial text, navy rounded outlines, blue process boxes, amber authority, and green only for provider-confirmed outcomes. Logical DOT references are preserved, but the SVG masters are intentionally authoritative for rendering to avoid Graphviz's uncontrolled label/edge crossing. `publishing/scripts/figures.py` already prioritizes an SVG master over the corresponding DOT master. Automated guards inspect the SVG and chapter-specific expected semantics. The DOCX built check uses **SHA-256 of each F04 PNG**, requiring exact embedded bytes to match generated assets. No generated `dist/` files should be committed.

## Executed automated and visual checks

- `make figures` — PASS after AppleDouble macOS `._*` metadata was removed from the temporary extract (these bogus `.svg` AppleDouble files otherwise break CairoSVG).
- `make check` — PASS (Ch01 3783/3900, Ch02 5269/5400, Ch03 4070/4300, **Ch04 2985/3000**; total allocated source 117800; 550 working page target, 575 preferred, 600 planning upper, 700 absolute maximum).
- `make book-docx`, `make check-figures`, `make qa` — PASS; build check explicitly rejects stale embedded Figure 4 assets.
- LibreOffice rendered `dist/etis-agentic-ai-book.docx` to PDF with **115 total pages**, with 7×10-inch pages and manuscript Ch04 images + captions visually inspected. F04-01 is on PDF page 62, F04-02 on page 65, F04-03 on page 68; no clipped labels or detached captions observed in the inspected pages. These are page numbers in the PDF file, not printed chapter pagination.
- Research-source landing pages cross-checked for Anthropic December 19 2024, OpenAI January 15 2026, τ-bench June 2024, OWASP 2026 edition released December 9 2025, and MCP July 28 2026. Full primary-document page-level verification is **not** certified.
- Chapter 1–3 prose was not re-authored; this is a controlled flow adjustment, not a new scientific independent peer review.

## Unresolved gates, explicitly not certified

1. The uploaded TAR snapshot and earlier git-status output disagree: upload had stub Chapter 4, while earlier working tree status showed uncommitted substantive Chapter 4. Local installer must pass a dry run before writing; it accepts only known pre-patch hashes (snapshot, first patch or previous corrective overlay where applicable), and refuses unknown changes. It does not alter Git history.
2. Native Microsoft Word for Mac 7×10-inch visual signoff **must be performed by the user** on the rebuilt manuscript; LibreOffice may paginate differently.
3. Full-book finished-page forecast remains provisional because Chapters 5–36 are placeholders. The current 115 pages must never be characterized as finished volume forecast.
4. Final copyediting, publication metadata, and primary-source page-level audit remain later publishing gates.

**Disposition:** Patch candidate; not frozen, not merged. Automated checks + inspected LibreOffice pages passed; Mac-native Word publishing signoff still pending.
