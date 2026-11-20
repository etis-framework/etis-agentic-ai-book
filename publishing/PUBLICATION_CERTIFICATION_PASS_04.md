# ETIS Publication Certification — Pass 4 technical and currency review

> **Archived development-pass evidence — not the current publication status.** This dated report records the scope, limitations and decisions of its own engineering pass. Statements such as "not certified," "pending," and "open gate" are preserved as historical findings, not the status of the first-edition companion or the author-approved KDP interior. See [Release Policy](../RELEASE.md) for the current companion release procedure and [Pagination](PAGINATION.md) for print-layout source/approval boundaries.

**Status: NOT CERTIFIED for final publication.** Date: 2026-11-16.

## Inputs and baseline

- User-provided `ETIS_PASS4_BASELINE.tar.gz`: full repository content with 36 manuscript chapters, 7 parts, 6 progressive build directories and four operations/security/reliability/assurance fixture directories. Archive excludes `.git`, so a Git commit SHA cannot be independently established from it.
- Source inventory: 36 developed chapters, 99 chapter image references, 34 prior bibliography entries (36 after this patch), 154 prior index entries (160 after this patch). Architectural source modules, tests and README source diagrams examined.
- Baseline `make book-docx`: completed and embedded all referenced manuscript images. Baseline `make check`: PASS **before edits**, including 153 Python unittest cases from 10 suites. This proves only the verified local fixture properties; code changes were not required or introduced in this pass.
- **Final edited-source rerun:** `make book-docx` PASS; complete uninterrupted `make check` PASS, including all 153 tests across ten Python suites, all chapter acceptance checks, source/back-matter preflights, V12 allocation checks and the new Pass 4 static gate. These runs were executed against the extracted source snapshot, **not the final merged Git SHA**; the installer and Mac PR gates must repeat them before merge. `make check` does not prove native Word pagination or production security.

## Acceptance scope

1. **Context/memory**: Chapters 12 and 20 distinguish evidence selection, provenance, memory poisoning and current authoritative truth. Persistent memory lifecycle remains specified only.
2. **Protocol**: Chapter 19 distinguishes MCP tool/resource exchange from A2A peer task exchange and makes both subject to independent enterprise authorization. No protocol client implemented in Builds 0–5.
3. **Evaluation**: Chapter 31 requires trajectory-level properties, repeated trials and conservative statistical interpretation. No empirical deployment claims.
4. **Lifecycle**: Chapter 33 makes agent/model/tool/memory adaptation a governed release change, not a self-granted permission.
5. **Publication integration**: bibliography, source register, glossary, index and topic traceability updated; new QA checker protects coverage and fixture navigation.
6. **Six internal lenses and eight selective paths**: documented in `review/pass4-state-of-the-art-six-lens.md`. Structured professional adversarial review, not independent human line-by-line readership study.

## External source identity verification

- Official MCP maintainers, 2026-07-28 release: https://blog.modelcontextprotocol.io/posts/2026-07-28/ (version/transport concepts; *not* E5 authorization).
- Official A2A Protocol community, 2026-03-12 v1.0 announcement: https://a2a-protocol.org/dev/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/ (agent task-exchange scope; *not* case-specific authorization).
- NIST CAISI AI Agent Standards Initiative, 2026-02-17: https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure (initiative context; *not* a conformance standard).

**Source risk:** Full edition/page claim verification, detailed A2A/MCP conformance sections, licensed standards, rights/permissions and final bibliography format still require independent final approval. These public-source checks are not certification of the full 36-chapter citation corpus.

## Persistent limitations and follow-on release gates

- The 7×10 V12 ledger is an allocation, not a measured native Word print proof. Resolve final page count, correct TOC/index page locators, actual-size diagrams, table breaks and running heads in Pass 5.
- Build 5 does not compose Builds 1–4 into a single end-to-end agent runtime. E2 epoch fencing is not enforced by independent E5, and the local subprocess, mock provider and assurance collector are not production security or settlement evidence.
- Record complete regression results on the final merged SHA; pin official companion repository edition tag. Final ISBNs, cover/spine, print rights and retail copy belong to Pass 6.

**Decision:** Accept targeted Pass 4 corrections only after its integrated QA passes. No title change, chapter 37 or Build 6. No claim that the book is publication-ready until Passes 5–6 close their evidence gates.
