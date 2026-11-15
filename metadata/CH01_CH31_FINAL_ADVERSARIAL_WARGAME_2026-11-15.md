# Chapters 1–31 and companion reference system — final adversarial war-game

**Audit date:** 2026-11-15. **Examined source:** extracted title-integrated Chapter 31 snapshot (no `.git` directory). **Book identity:** *Engineering Agentic AI Systems: Build, Secure, Verify, and Operate Trustworthy AI Agents*. **Scope:** 31 developed chapters, seven part introductions (including future-part bridges), front/back matter, six Builds 0–5, four companion fixtures, figures, documentation, and publication gates. Chapters 32–36 are placeholders, not completed evidence.

## Executed checks and their limitations

- `make book-docx`: **PASS**; 86 referenced images resolved in the generated Word file.
- All **68 commands** configured in `make check` were executed to success on this snapshot, using **separately bounded runs** after an aggregate attempt was terminated by the execution-wrapper time limit. No uninterrupted aggregate `make check` exit code is claimed. After the documentation repairs below, the new 69th reader-evidence freshness check, companion documentation, back-matter publication check, and Word build also passed.
- **153 individual unittest cases passed** across ten suites: Build 0=16, Build 1=15, Build 2=13, Build 3=18, Build 4=27, Build 5=22, recovery=10, security=6, operations=14, assurance=12.
- `check_single_volume.py` and `check_finished_page_ledger.py`: **PASS on source/planned allocation**, 550-page target, not final finished-page measurement. Publishing figure checks and geometry gates passed; **native Word for Mac 7×10 actual-size figure/table pagination is still an independent human gate**.
- Companion module READMEs and SVGs were inventoried for all six builds and the security/operations/assurance fixtures. Chapter 28's pure reliability decision fixture explicitly relies on earlier real source-module diagrams, rather than falsely representing a new effectful runtime.
- Git merge state **not verified**: the provided working source is a TAR-derived snapshot without `.git`. The local author must confirm the commit on `main` and the title patch state before installing subsequent changes.

## Red-team findings corrected in this incremental editorial repair

| Finding | Risk if left unresolved | Correction |
|---|---|---|
| `TESTING.md` still said **109** cases after Chapter 31 | Falsely diminishes or misstates the evidence register | Updated to **153** current local regression cases, and explicitly scoped the claim to fixtures |
| `TESTING.md` said Chapters 29–31 did **not** exist or were merely planned | Contradicts completed security, operations and assurance code | Rewritten as implemented-local-versus-external-assurance distinction |
| Implementation evidence map forecast work in already developed Chapters 29–31 | Reader may mistake the fixture's actual verification state | Recast the handoff as executed evidence plus future production obligations |
| Companion root README heading said Chapters 28–30 but its table includes 31 | Broken reader journey and chapter navigation | Heading/body now correctly identify Chapters 28–31 |
| Part IV intro and Chapter 27 contain unresolved Markdown relative links to companion source | Digital-reader links resolve incorrectly relative to manuscript file location | Changed to explicit repository-root-relative code paths, legible in print and searchable in Git |
| Existing structural QA accepted these regressions | Future chapters could silently recreate stale guidance | Added a dedicated source link/freshness regression gate to `make check` |

## Six-lens adversarial findings

### 1. Implementing engineer — can I build and reproduce it?
**Pass within fixture scope.** Builds 0–5 progressively demonstrate deterministic effect gating, typed advice, identity/context, separately checked E5 request, provider contract/reconciliation, and optional coordination. Each build has source/module diagrams embedded in its README and its own executable tests. Later fixtures extend **the same** code rather than creating an uncontrolled Build 6. The published claim must remain six *progressive standalone increments*, not a single wired end-to-end multi-agent platform. Reader-facing source locations and obsolete documentation statements were corrected.

### 2. Enterprise architect — is the system, rather than the model, the unit of design?
**Pass with explicit scope boundary.** Logical E1–E9 responsibilities and C01–C09 contracts are not confused with one process per domain or independent physical failure zones. A Design A deterministic baseline, Design B bounded AI advice, and optional Design C bounded investigation do not automatically imply a linear upgrade path. The Chapter 8 and Appendix A definitions remain stable. Build 5 local epoch fencing is **not** validated independently by E5; extra agent autonomy cannot fix that gap.

### 3. Advanced CS student — is the chapter self-contained and educational?
**Pass for source-preflight; native pedagogical inspection remains.** Chapter-local first-reference checks passed for 31 developed chapters, with reviewer perspective checks. Appendix B supplies a two-table navigation guide for Builds 0–5 and Chapters 28–31. Module READMEs differentiate intended learning objectives and non-guarantees; executable negative tests support evidence-driven instruction. A code walkthrough in native Word and an instructional pilot are still necessary before claiming classroom readability for every example.

### 4. Security and assurance — can a compromised agent create an unauthorized effect?
**Pass for the bounded negative tests.** An investigator with a valid fixture E1 token but no transaction-specific finance grant is denied by Build 3 E5; Chapter 29's actual subprocess tests deny forgery and transaction-scope mismatches, and check for absence of E7/E8 fixture effect. C04 advisory content cannot become a C05 approval or E6 credential. **Open:** independent key custody, hostile OS/host isolation, production delegated token revocation/rotation, E5 current-owner epoch enforcement, and protected E9 audit.

### 5. SRE and incident commander — is uncertainty handled safely?
**Pass in the modeled local failure/recovery cases.** A missing acknowledgment is `UNKNOWN`, not failed payment; only the original RF-1042 is reconciled, without second dispatch. Build 4 local transactional event history preserves prior confirmation even when later evidence conflicts. Build 5 coordinator recovers conservatively. The Chapter 30 read-only incident classifier cannot issue a financial command. **Open:** real provider finality and availability, monitored deployment failure domains, telemetry integrity, operational drills and support ownership beyond synthetic fixtures.

### 6. Business owner — does the system deliver value without invisible liability?
**Pass in conceptual risk/accountability framing; production economics and signoff remain pending.** CASE-204/RF-1042 retains the same $500 risk through the developed chapters. The manuscript rejects an agent's persuasive answer as refund permission and requires independent business authorization, evidence, and safe reconciliation. The current fixtures cannot substantiate a real payout service-level objective, payment cost or production ROI; Chapters 32–36 must finish governance/economic/deployment arguments before the single-volume book is publication-complete.

## Thematic drift and coverage assessment

- **Build:** Chapter 1–7 design logic, Chapter 8–21 architecture/patterns, Chapter 22–27 runnable checkpoints. No requirement that every workflow contain an agent.
- **Secure:** distinct admission, scoped context, untrusted proposals, trusted consequential execution, negative adversarial cases; no identity→finance-authority shortcut.
- **Verify:** tests, named counterexamples, source digests, claim/falsifier records and explicit evidence exclusions. A green fixture is never treated as production certification.
- **Operate:** durable original-operation identity, uncertainty, reconciliation, incident roles, escalation and independent business acceptance. Reliability is not reduced to 'agent responds'.

The current title and subtitle are technically supported **through Chapter 31**, without forced marketing slogans or misleading new code. **Five unfinished chapters (32–36)** remain an explicit barrier to claiming book-wide completion or a production-assured release.

## Remaining gates — NOT certified by this audit

1. Author's native Mac Word 7×10 actual-size figure, table, code-listing, and whole-book finished pagination inspection, including precise V12 accounting.
2. Bibliographic editions, chapter-specific claims, passage-level citation verification and rights for standards/figures.
3. Post-Chapter-31 source SHA and title patch merge state; source-integrity confirmation against the authoritative local Git checkout.
4. External E5 owner-epoch enforcement, issuer/key custody, real provider settlement/idempotency contract, protected E9 audit, representative AI-agent evaluation, real incident drills, and accountable production go/no-go.
5. Development and full six-lens review of Chapters 32–36, and final retail metadata, public release/tag and cover approval.

**Disposition:** Within the developed 31-chapter, educational-simulation scope, architecture and theme coherence are **accepted for continued book development**. Publication certification and production guarantees are **not** established. This report records tested commands and findings, not an unsupported claim of independent live-payment validation.
