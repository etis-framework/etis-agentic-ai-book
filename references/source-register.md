# Source and citation register — developed Chapters 1–31

**Status: developed Chapters 1–31 are covered by chapter-specific source/claim notes; final publication certification remains open.** This is a cumulative engineering register, not the reader bibliography. Coverage and verification depth vary by chapter: presence of a mapping does not certify a primary passage, edition/page, stable link, claim applicability or production guarantee. Historical working-pass headings below preserve the chronology of earlier citation reviews; they are not current coverage limits.

## Source hierarchy and use

Primary research supports specific research findings; foundational books support mechanisms and historical context; standards and official guidance support governance terminology and controls; vendor documentation supports only the documented behavior of that vendor's product or protocol. Do not use a vendor blog as proof of a general architectural guarantee. Cite source and version at the claim, not merely at the end of the book.

| Key | Source | Intended claim scope | Chapter/section | Verification before release |
|---|---|---|---|---|
| `gray_reuter_1992` | Gray & Reuter, *Transaction Processing* (1992) | ACID, logs, local transaction guarantees | Ch2 §2.2, worked trace | Exact chapter/page; confirm edition |
| `lamport_1978` | Lamport, CACM (1978), DOI 10.1145/359545.359563 | Ordering and limits of distributed observations | Ch2 §2.6 | Map narrowly to ordering, not payment semantics |
| `garcia_molina_salem_1987` | Garcia-Molina & Salem, *Sagas* (1987) | Long-lived transactions and compensating actions | Ch2 §2.6 | Verify compensation terminology and scope |
| `hohpe_woolf_2003` | Hohpe & Woolf, *Enterprise Integration Patterns* | Messaging, adapters, delivery and integration patterns | Ch2 §§2.5–2.7 | Exact pattern citations |
| `kleppmann_2017` | Kleppmann, *Designing Data-Intensive Applications* | Replication, delivery, durable state, failure modes | Ch1 worked example; Ch2 §2.6 | Specific chapter/page and guarantee conditions |
| `russell_norvig_2020` | Russell & Norvig, *Artificial Intelligence: A Modern Approach* | Search, planning, inference, agents | Ch1 terminology; Ch2 §§2.3–2.4 | Verify exact historical attributions |
| `lewis_2020` | Lewis et al., NeurIPS (2020) | Retrieval-augmented generation research | Ch2 §2.8 | Distinguish research result from enterprise design recommendation |
| `yao_2023` | Yao et al., ICLR (2023) | Reasoning-and-acting research pattern | Ch1 §1.4; Ch2 §2.9 | Verify evaluation and limitations |
| `schick_2023` | Schick et al., NeurIPS (2023) | Model-assisted tool use research | Ch1 §1.4; Ch2 §2.9 | Verify scope; not a security guarantee |
| `bass_clements_kazman_2021` | Bass, Clements & Kazman, *Software Architecture in Practice* | Quality attributes and architecture decisions | Ch1 quality attributes | Verify exact quality-attribute taxonomy |
| `beyer_2016` | Beyer et al., *Site Reliability Engineering* | Operations, reliability, service ownership | Ch1 and Ch2 §2.13 | Verify applicable chapters |
| `nist_ai_rmf_2023` | NIST AI 100-1 (2023) | AI risk management concepts | Ch1 governance; Ch2 §2.14 | Map named functions precisely |
| `nist_genai_profile_2024` | NIST AI 600-1 (2024) | Generative AI risk considerations | Ch1 and Ch2 §2.14 | Map specific risks and controls |
| `iso_42001_2023` | ISO/IEC 42001:2023 | AI management-system context | Ch2 §2.14 | Review licensed normative text; do not quote requirements from summary |
| `owasp_llm_2025` | OWASP GenAI Security Project | Prompt injection and tool misuse threat categories | Ch2 §2.11 and threat example | Pin exact edition and page before final citation |

## Editorial citation convention

Use readable author–year references in explanatory prose, e.g., **Gray and Reuter (1992)**, and maintain the stable bibliography key in this register. Before final publication, select one citation-rendering workflow and replace editorial references with linked, consistently formatted citations. A title in the bibliography is not evidence that every associated claim has been verified.

## Historical claim-level QA queue — Chapters 1–2

- [ ] Ch1: distinguish research findings about agents from recommended enterprise control design.
- [ ] Ch1: establish evidence for any quantitative business, latency, accuracy, or cost claim before adding it.
- [ ] Ch2: verify any priority claim such as “first,” “invented,” or “originated.”
- [ ] Ch2: check the exact semantics of ACID, idempotency, at-least-once delivery, and external effects.
- [ ] Ch2: ensure all diagrams express ownership and observations accurately.
- [ ] Chapters 1–2: confirm edition, authors, identifiers, and stable URLs against original publisher or standards body.
- [ ] Chapters 1–2: complete source-specific page or section references and editorial sign-off.

## V8 — new sources and verified bibliographic identification

| Key | Verified record | Scope | Chapters | Status / limitation |
|---|---|---|---|---|
| `van_der_aalst_2013` | Publisher DOI 10.1155/2013/507984 | BPM design, enactment, analysis | 2 §2.5; 3 §§3.1, 3.8 | Bibliographic identity and abstract verified; no page-level quotation audit |
| `parasuraman_sheridan_wickens_2000` | IEEE DOI 10.1109/3468.844354 | Four automation functions; human interaction | 3 §§3.4, 3.7 | Bibliographic identity and abstract verified; no claim that ETIS matrix is copied |
| `parasuraman_2000` | DOI 10.1080/001401300409125 | Human factors and oversight risks | 3 §3.7 | Bibliographic identity and abstract verified |
| `iso_29148_2018` | ISO official standard 72089 | Requirements engineering process and information items | 3 §3.2 | Official catalog verified; licensed normative text not examined |

## V8 — claim-level citation audit (Chapters 1–2)

**Citation placement policy:** Cite historical attribution, named research findings, standards, nontrivial technical mechanisms, and externally sourced frameworks at the relevant explanatory paragraph. The refund story, illustrative arithmetic, original ETIS prescriptions, and explicitly marked design hypotheses are authorial analysis and need not be artificially attributed. Avoid implying a source proves a stronger operational guarantee than it actually addresses.

| Chapter | Location | Citation added | Supported scope | Remaining QA |
|---|---|---|---|---|
| 1 | Introductory enterprise quality discussion | Bass et al. (2021); Beyer et al. (2016) | Quality attributes and operational disciplines | Edition/page audit |
| 1 | §1.4 | Russell & Norvig (2020); Yao et al. (2023); Schick et al. (2023) | Agents, planning, reasoning/action and tool-use research | Confirm research-specific wording |
| 1 | §1.6 | Gray & Reuter (1992); Kleppmann (2017) | Local vs distributed effects | Provider-specific contract must remain hypothetical |
| 1 | §1.7 | NIST AI 100-1; NIST AI 600-1 | External AI governance and risk context | Map exact NIST categories before final |
| 2 | §2.2 | Gray & Reuter (1992) | Transactions, logging, recovery | Edition/page audit |
| 2 | §§2.3–2.4 | Russell & Norvig (2020) | Knowledge reasoning, classical planning | Edition/page audit |
| 2 | §2.5 | van der Aalst (2013) | BPM and workflow relationship | Section-specific audit |
| 2 | §2.6 | Lamport (1978); Kleppmann (2017); Garcia-Molina & Salem (1987) | Distributed observations, saga compensation | No provider guarantee inferred |
| 2 | §2.8 | Lewis et al. (2020) | RAG research | Enterprise governance claims are ETIS analysis |
| 2 | §2.9 | OWASP living guidance; NIST AI 600-1 | Prompt-injection threat | Pin OWASP edition |
| 2 | §2.14 | NIST AI 100-1; ISO/IEC 42001 | Risk management and management-system context | Licensed normative text not reviewed |

**Additional source candidates for later verification, not yet cited as facts:** NIST AI 100-4 (if relevant to evaluation); RFC 9110 (HTTP idempotent method semantics, not provider business idempotency); OWASP Agentic AI guidance (pin version); vendor provider idempotency documentation (only for the selected implementation). This is a prioritized research queue, not a claim of verification.


## Chapter 4 — agent mechanisms and boundaries (November 2026)

No new bibliographic identities were required: each source cited in Chapter 4 already appears in the consolidated back-of-book bibliography. Chapter 4 reuses the existing author–year style and does not claim a source establishes ETIS-specific policy boundaries.

| Stable key | Claim and citation locus | Evidence status / limit |
|---|---|---|
| `russell_norvig_2020` | §4.1 operational agent definition; §4.5 non-LLM agents | Foundational secondary reference; exact edition/page audit remains a publication task |
| `yao_2023` | §§4.2, 4.5 interleaved reasoning/action research | Research mechanism only; no system-level security or correctness guarantees inferred |
| `schick_2023` | §4.2 learned tool-use research | Research mechanism only; no delegated authority guarantee inferred |
| `kleppmann_2017` | §4.6 incomplete distributed observations | Foundational distributed-systems context; payment-provider behavior remains hypothetical |
| `nist_ai_rmf_2023` | §4.8 risk-management context | NIST AI RMF 1.0, not a certification of this chapter's architecture |

**Publication gate:** Verify precise page/section for textbook claims and stable research URLs during final citation certification. This chapter introduces no unsupported quantitative industry benchmarks.

## Chapter 4 — November 2026 independent source recheck

| Key | Chapter 4 claim | Limit |
|---|---|---|
| `anthropic_agents_2024` | §§4.1, 4.2, 4.5: difference between predefined workflows and dynamically agent-selected steps | Vendor engineering guidance, not proof of safety |
| `openai_agents_2026` | §§4.1, 4.5: contemporary LLM-agent construction and tool control terminology | Vendor guide; verify pinned PDF edition before publication |
| `tau_bench_2024` | §4.8: final database state and repeated-run metric in agent evaluation | Benchmark result, not guarantee of production reliability |
| `owasp_agentic_2026` | §4.8: agent-specific threat categories | 2026 edition published 2025-12-09; threat taxonomy not compliance certificate |
| `mcp_2026` | §4.6: protocol capability versus business authority | July 2026 release summary; transport security ≠ refund entitlement |

Check future Ch12/13/19/29/31 references for controlled reuse. Exact page-level source certification remains a publication gate.

## Chapter 5 — business value and lifecycle economics

- NIST AI RMF 1.0 (2023), MAP 3: benchmarked benefits, costs, operating scope and oversight; used in §§5.1 and 5.7, not as a claim of measured results.
- FinOps Foundation Framework 2025 and Unit Economics capability: connect technology expense and fully loaded cost to business unit outcomes; used in §§5.3–5.4 and 5.8.
- Bass, Clements and Kazman (2021): architecture tradeoff discipline; Kleppmann (2017), Gray and Reuter (1992): distributed execution and transactional risks.
- Scenario assumptions in §5.5, economic equation, figures F05-01/F05-02, and acceptance criteria are original ETIS examples; not externally validated performance or vendor costs.

## Chapter 6 — uncertainty, authority, and enterprise trust (2026-11-11)

| Source key | Claim location | Evidence limit |
|---|---|---|
| `nist_ai_rmf_2023` | §§6.4, 6.7: governance, measure, oversight | Voluntary framework, not an approval of ETIS controls |
| `nist_genai_profile_2024` | §6.2: integrity, over-reliance | Relevant risks; four uncertainty categories are original ETIS |
| `owasp_agentic_2026` | §6.3: goal hijack, tool misuse, identity abuse | 2026 edition released 2025-12-09; not a compliance certificate |
| `parasuraman_sheridan_wickens_2000`, `parasuraman_2000` | §6.6: human oversight design | Human factors research, not prescriptive case approval software |
| `gray_reuter_1992`, `kleppmann_2017` | §6.5: distributed payment outcomes | Generic transaction semantics; provider contract not assumed |

**Citation QA:** No new source identities were required. The chapter deliberately does not assert specific provider guarantees, calibrated confidence thresholds, or normative legal rules. Verify exact textbook pages and licensed standards before publication certification.


## Chapter 7 — requirements and traceability (Part I closure)

- ISO/IEC/IEEE 29148:2018 is cited as requirements-engineering context; the ETIS requirement IDs and tables are original examples, not claims of ISO-mandated templates. Existing bibliography key `iso_29148_2018` is reused.
- NIST AI RMF 1.0 (2023) and the Generative AI Profile (2024) are referenced for risk measurement and governance framing; no universal release acceptance thresholds are attributed to NIST.
- Gray and Reuter (1992) and Kleppmann (2017) ground distributed transactions and unknown external effect claims. Provider-specific idempotency guarantees remain explicitly illustrative.
- Original ETIS artifacts: AUTH-01, PAY-03, DATA-01, EV-02, POL-02, OPS-01, EVAL-01, CHG-01; Figures 7.1–7.2; exercise prompts and proposed gate outcomes. Publication citation-level precision remains a later gate.

## Parts I–II claim-location reconciliation — Chapters 8–16 (12 November 2026)

The entries below identify the **local manuscript citation and intended claim**, not proof that every sentence has been checked against the exact printed page. Original ETIS constructs (E1–E9, CASE-204, RF-1042, contract schemas, A/B/C comparisons, and L/M/H profiles) are authorial synthesis. A technical mechanism from a source never grants specific provider or regulatory guarantees.

| Chapter and claim location | Bibliography keys | Narrow supported scope | Provenance/verification and remaining action |
|---|---|---|---|
| Ch8 §8.2 architectural views | `bass_clements_kazman_2021` | Quality-attribute and architecture-view discipline | Publisher bibliographic record previously curated; verify relevant chapter/pages |
| Ch8 §8.4 contract/integration framing | `hohpe_woolf_2003` | Message and integration patterns | Established book; check named pattern chapters before print |
| Ch9 §9.2 identity and authorization distinction | `nist_sp800_207_2020` | Resource-focused authentication and authorization | Official NIST catalog/DOI verified 2026-11-12; not evidence of the ETIS schema |
| Ch10 §10.4 event ordering / coordination | `lamport_1978`, `kleppmann_2017` | Ordering of distributed events and consistency risks | Primary DOI previously curated; exact passage mapping remains |
| Ch11 §11.2 advisory tools and reasoning | `yao_2023`, `schick_2023` | Research on reasoning/action and tool use | Original research bibliography; no claim of protected execution |
| Ch12 §12.4 retrieval limitations | `lewis_2020` | Research basis of retrieval-augmented generation | Primary research; does not prove access-control enforcement |
| Ch13 closing source note, relating to §13.2 | `gray_reuter_1992`, `kleppmann_2017`, `nist_sp800_207_2020` | Transaction intent, distributed coordination, resource-level authorization | Source note retained rather than adding to chapter at word ceiling; exact claim-adjacent placement remains an editorial exception |
| Ch14 §14.2 adapter contract | `hohpe_woolf_2003` | Adapter / message-contract pattern | Book edition curated; provider API behavior is contract-specific |
| Ch14 §14.3 observations, HTTP semantics | `gray_reuter_1992`, `kleppmann_2017`, `rfc9110_2022` | Local/distributed effects and HTTP-method idempotency | RFC 9110 §9.2.2 verified against official RFC Editor; **not** refund-key semantics |
| Ch15 §15.3 outbox atomicity | `gray_reuter_1992`, `hohpe_woolf_2003` | Local transaction and asynchronous messaging principles | ETIS outbox sequence is original synthesis; exact pattern-level source audit remains |
| Ch15 §15.6 assurance/operations | `beyer_2016` | Operational readiness, observation and response | Book available from official SRE site; exact chapter mapping remains |
| Ch16 §16.3 isolation and zero trust | `nist_sp800_207_2020` | No implicit trust from network location | Official NIST catalog/DOI verified; ETIS L/M/H are not a NIST classification |

### Chapter 1–7 source review disposition

Chapter-specific mappings and bibliographic records for Chapters 1–7 appear in the earlier tables in this register. No newly confirmed absent entry was identified in this targeted reconciliation. The following checks **remain open** before the claim-level certification gate can close: verify all edition/page claims, historical priority statements, policy/standards versions, current OWASP and MCP documents, and whether Chapter 13's compact source note should be adjacent to its exact claim once the full manuscript is copyedited. Avoid growing Chapters 4 and 13 beyond their locked source-word ceilings.

### Citation acceptance policy

- Each non-original, nontrivial technical mechanism or named external standard must have a local, scoped citation and a matching bibliography entry and register row.
- Bibliographic identification, source existence, paraphrase support, source-page verification, and engineering validation are separate gates.
- RFC 9110 describes HTTP semantics only. A payment-provider key's scope, lifetime, deduplication or settlement semantics must be established from the selected provider's versioned contract and tested in sandbox.
- NIST zero-trust architectural guidance does not certify ETIS implementation or constitute a universal deployment policy.
- When the final word/page budget leaves no room, prefer moving or tightening existing source notes over adding unsourced assertions.

## Chapter 17 — pattern selection and architectural decisions (November 2026)

| Claim / chapter location | Existing bibliography source | Supported scope / limitation |
|---|---|---|
| §17.1, human/software function allocation | Parasuraman, Sheridan, and Wickens (2000) | Separating acquisition, analysis, decision selection and action; does not define E1–E9 |
| §17.1, §17.3, architecture tradeoffs | Bass, Clements, and Kazman (2021) | Quality attributes and tradeoff analysis; not an approval of ETIS deployment |
| §17.2, agent definition | Russell and Norvig (2020) | General/classical agent mechanisms, not a claim that every LLM invocation is agentic |
| §17.2, workflow vs dynamic tool selection | Anthropic Engineering (2024); OpenAI (2026) | Vendor design guidance, not independent security or provider safety evidence |
| §17.4, outcome-level costs | FinOps Foundation Framework (2025) | Unit-economic discipline; the illustrative arithmetic and case thresholds are original ETIS |
| §17.6, evaluated tool trajectories | Yao et al. (2024), τ-bench | Repeated trials and end-state evaluation framing; not a production guarantee |

Figures F17-01/F17-02/F17-03, the design selection gate, CASE-204 experiment and conditional ADR are original ETIS synthesis. The sources do not certify this particular architecture. Exact edition/page verification remains a publication-level task. No new bibliography record is needed for Chapter 17.

## Chapter 3 — autonomy and process citation coverage

Chapter 3 uses `van_der_aalst_2013` for BPM context (§3.1), `iso_29148_2018` for requirements (§3.2), `parasuraman_sheridan_wickens_2000` for automation allocation (§3.4), and `gray_reuter_1992`/`kleppmann_2017` for external-effect uncertainty (§3.1/§3.8). These records identify supporting mechanisms, not approval of the original ETIS delegation envelope. Exact page support remains an open gate.

## Integration audit 1–17 — boundary between verified identity and verified claim

This pass confirms the existence of CAB-001's C01–C09 catalog and maps it to Chapter 8. It does **not** elevate the register's previously identified bibliography records to exact-page certification. The source register's existing publication-gate annotations remain binding. Where a chapter cites a standard or provider-independent work, the cited source supports the named mechanism or general design principle, not the ETIS logical architecture, a live payment-provider SLA, or an implemented assurance guarantee.

- Figure 4.2 illustrates **generic component arrangements**, not case Designs A/B/C. Figure 3.4 and Chapters 8/17 retain the case alternatives.
- C01–C09 originates in approved `metadata/approved/CAB-001.docx`, Table 3 (contract catalog), not an external normative standard.
- Exact edition/section validation for standards, vendor guides, and original technical works remains **open** where expressly recorded above. No new source verification is claimed here.

## Chapter 18 — coordination and delegation patterns (November 2026)

| Claim / chapter location | Existing bibliography source | Supported scope / limitation |
|---|---|---|
| §18.2, §18.5 architectural alternatives and costs | Bass, Clements, and Kazman (2021) | General quality-attribute tradeoff framing; does not prescribe ETIS topology |
| §18.4 epoch/fencing, duplicate work, external uncertainty | Kleppmann (2017) | Distributed consistency, concurrency and failure foundations; ETIS implementation is original synthesis |
| §18.4 distributed event ordering | Lamport (1978) | Event ordering foundations, not a lease implementation specification |
| §18.5 risk monitoring and governance | NIST AI RMF 1.0 (2023) | Broad risk governance framework; not a validation of CASE-204 controls |

Figures F18-01 and F18-02, the bounded delegation rules, coordinator/peer comparison, CASE-204 scenarios and injection matrix are original ETIS engineering synthesis. Source texts identify foundations, not approval of a specific payment architecture. Existing claim-level edition/page verification remains open.

## Chapter 18 V2 — reviewed claim-specific citations (2026-11-13)

| Chapter locus | Key / source | Precisely supported scope | Evidence limitation / publication gate |
|---|---|---|---|
| §18.2 | `bass_clements_kazman_2021` — *Software Architecture in Practice* | Tradeoffs among quality attributes, operational complexity and alternative designs | Not evidence that one agent pattern outperforms another; exact page mapping open |
| §18.2 | `fowler_microservice_tradeoffs_2015` — Fowler, *Microservice Trade-Offs* (2015) | Independent deployment benefits and distribution/operations costs of services | Analogous software-architecture cost only; not agent benchmarking or mandatory process-per-agent |
| §18.2, §18.5 | `finops_framework_2025`, `finops_unit_economics` — FinOps Foundation | Business-unit economics and measuring cost relative to completed value | No numeric CASE-204 cost or profitability claim |
| §18.5 | `hohpe_woolf_2003` — *Enterprise Integration Patterns* | Routing, messaging and delivery-pattern concepts | Does not prescribe ETIS peer authorization or E2 protocol |
| §18.4–18.5 | `kleppmann_2017` — *Designing Data-Intensive Applications* | Distributed failure, duplicate delivery, state and ordering limitations | No universal payment exactly-once or vendor idempotency guarantee |
| §18.4 / further reading | `lamport_1978` | Distributed event ordering | Does not define workflow ownership or authorize payments |
| §18.5–18.6 | `nist_ai_rmf_2023`, `owasp_agentic_2026` (contextual) | Risk management and agentic-system threat categories | ETIS negative-test matrix is original synthesis; no NIST/OWASP certification claimed |

**Bibliography reconciliation:** Fowler added to human bibliography and BibTeX. All other named citations reuse existing entries. Final publisher/edition/page-level checks remain open; do not imply full bibliographic claim certification.

## Chapter 19 — tools, adapters and effect isolation (2026-11-13)

| Claim and location | Source | Supported scope / explicit limit |
|---|---|---|
| §19.2 HTTP-method idempotency | `rfc9110_2022` — Fielding, Nottingham, Reschke, RFC 9110 §9.2.2 | Method-level request semantics; not a payment provider's business-operation deduplication guarantee. RFC text checked against RFC Editor in Nov 2026. |
| §§19.3, 19.7 architectural isolation | `bass_clements_kazman_2021`; `nist_sp800_207_2020` | Quality-attribute tradeoffs and resource authorization principles; neither mandates ETIS E5 or nine services. |
| §19.3 distribution cost | `fowler_microservice_tradeoffs_2015` | General deployment/operations tradeoffs; not measured agent throughput or cost. |
| §§19.4–19.5 provider uncertainty | `gray_reuter_1992`; `kleppmann_2017`; `hohpe_woolf_2003` (further reading) | Transactions and distributed observations; no claim that any payment provider implements idempotency or query. |
| §19.6 agentic threat classes | `owasp_agentic_2026` | Tool misuse, identity/privilege and context risks; OWASP taxonomy is guidance, not certification. |

Figures F19-01/F19-02, adapter status mapping, CASE-204 example, negative tests and provider-agnostic contracts are original ETIS design synthesis. Claims about a specific provider's key scope, retention, credentials or reconciliation require its actual documentation and executable contract tests. Exact edition/page audit of textbooks remains an open publication gate.

## Chapter 20 — state, memory and knowledge design (2026-11-13)

| Claim / section | Source | Supported scope and limitation |
|---|---|---|
| §§20.1–20.3 classes, ownership, consistency, memory tradeoffs | `kleppmann_2017`; `bass_clements_kazman_2021` | General distributed data integrity, architectural quality attributes; neither defines ETIS E-domains |
| §20.3 retrieval augmented generation | `lewis_2020` | Retrieval augmentation as technique; not a guarantee of data authorization, freshness or truth |
| §20.4 revocation, data-use and governance | `nist_ai_rmf_2023`; `nist_sp800_207_2020` | Risk governance and resource-based access constraints; not literal retroactive deletion of prior model inference |
| §20.5 authoritative operational state and uncertainty | `gray_reuter_1992`; `kleppmann_2017` | Transaction boundaries, distributed state/failure; does not certify payment provider behavior or exactly-once execution |

Figures F20-01/F20-02, the five-way information classification, CASE-204 invalidation-and-fencing scenarios, and release tests are original ETIS synthesis. Exact edition and source-page support remains an open publication gate. The chapter introduces no new normative provider guarantee. Chapter 20 is a design-pattern decision: Chapter 12 remains the foundation for governed E4 retrieval; Chapter 15 owns durable E7 state; Chapter 26 now provides a fixture implementation of provider contracts and reconciliation; real-provider assurance and Chapter 28 recovery analysis remain future work.


## Chapter 21 — architecture decisions and governance as code (2026-11-13)

| Claim / section | Source already in bibliography | Supported scope and explicit limitation |
|---|---|---|
| §§21.1–21.2 choice/ADR alternatives | `bass_clements_kazman_2021` — *Software Architecture in Practice* | Architectural decisions, evaluation by quality attributes; ADR-021 is original ETIS example, not an external normative format |
| §§21.3–21.4 protected access/policy enforcement | `nist_sp800_207_2020` — NIST SP 800-207 | Access decisions and resources under zero trust principles; does not certify E5/E6 or define the ETIS contracts |
| §§21.4, 21.6 distributed intent and uncertainty | `gray_reuter_1992`; `kleppmann_2017` | Transactions, concurrent state and uncertain distributed effects; not specific provider deduplication or refund API guarantees |
| §21.5 approved change/risk measurement | `nist_ai_rmf_2023` — NIST AI RMF 1.0 | Risk-management governance framing; does not prescribe ETIS policy bundles or guarantee measured outcomes |

Figures F21-01/F21-02, ADR-021, POL-021, G21-01–G21-07 tests and the CASE-204 decision flow are original ETIS engineering synthesis. In-text references are locally claim-scoped. Exact edition, chapter and page checks remain mandatory for publication.

## Parts I–III holistic audit and verified source addition (2026-11-13)

The attached Word build covers developed Chapters 1–26, but none of Parts I–III has publication certification. Editorial linkage, exact source-page/edition checks, and Mac Word native pagination remain gates. Refer to `metadata/parts-01-03-six-lens-audit.md` for six reader paths, citation scope, risk dispositions, and measured 345-page LibreOffice review data.

| Source key | Official source confirmation | Specific claim scope | Limits / remaining checks |
|---|---|---|---|
| `nist_sp800_162_2019` | NIST CSRC official SP 800-162 updated 2019, DOI 10.6028/NIST.SP.800-162 | Ch21 §21.4 attributes used by policy decision points (subject, resource, action, environment) | Catalog/abstract verified; not a published ETIS payment authorization rule; exact passage audit still open |
| `nist_sp800_207_2020` | NIST CSRC official Aug 2020 SP 800-207 | Ch9/Ch21 resource-centered identity, protected enforcement | Does not certify ETIS architecture |
| `parasuraman_sheridan_wickens_2000` | IEEE journal, PubMed DOI 10.1109/3468.844354 | Ch3/Ch17 human-machine allocation of functions | Bibliographic identity and abstract verified; ETIS decision matrices are original |
| `anthropic_agents_2024` | Anthropic Engineering, Dec 19 2024 | Ch4/Ch17 model-driven workflow/agent patterns | Vendor guidance, not independent safety proof |
| `tau_bench_2024` | arXiv 2406.12045, Yao et al., 2024 | Ch4 repeated policy-compliance/end-state evaluation | Research benchmark, not provider assurance |
| `mcp_2026` | MCP project, July 28 2026 specification | Ch4/Ch19 tool protocol scope | MCP transport authorization cannot grant refund entitlement |

**Open citation work:** Confirm every quotation, edition, primary-source passage and normative claim; pin OWASP living revisions and provider-specific guarantees; avoid treating bibliographic matching as technical correctness. The official source URLs are embedded in the consolidated bibliography or maintained in this register.

## Chapter 22 — deterministic baseline (2026-11-13)

| Claim location | Source / scope | Verification status |
|---|---|---|
| §22.1, §22.4 | Gray and Reuter (1992): local transaction/durable intent; Kleppmann (2017): distributed state, partial observations and failure | Foundational scope mapped; **exact edition/page passage audit OPEN** |
| §22.3 | Fielding, Nottingham, and Reschke (2022), RFC 9110 §9.2.2: HTTP-method idempotency, **not payment-provider idempotency-key semantics** | Section anchor identified; provider contract intentionally not asserted |
| §22.5 | NIST AI RMF 1.0 (2023): organizational risk management framing, not approval of an ETIS execution path | General scope mapped; claim-level primary passage audit OPEN |
| §§22.2–22.7 | ETIS original fixture code, figures, denial tests, and architectural synthesis | **Direct reproducibility tests mandatory**; no external source purported to certify real transactions |

**Carry-forward:** No new external bibliography titles are needed for Chapter 22: all four attributions already occur in `manuscript/backmatter/bibliography.md` and `references/bibliography.bib`. Future provider-specific guarantees require that provider's primary contract and tests. No finished-source claim-level certification is made.

## Chapter 23 claim and source audit queue

| Location | Referenced source or basis | Narrow claim | Publication gate |
|---|---|---|---|
| §23.1 | NIST AI 600-1 (2024), OWASP GenAI security guidance | Generative output/prompt-injection risk motivates untrusted proposal handling | Verify exact NIST category and pin OWASP version; no claim of endorsed ETIS architecture |
| §§23.2–23.6 | CAB-001 and source-controlled Build 0/1 code | E1–E9/C01–C09 mapping, strict parser, negative evidence | Compare each assertion to actual code/tests and edition tag |
| §23.7 | ETIS original analysis; cross-references Chapters 31/34 | Proposed adoption metrics and Design B conditional value | Must not imply empirical model improvement without measured study |

## Chapter 24 source and claim reconciliation (publication gate open)

| Chapter location | Supporting source | Precisely supported claim / limitation |
|---|---|---|
| §§24.2–24.3, 24.8 | NIST SP 800-207 (2020), `nist_sp800_207_2020` | Resource-centered authentication/authorization and no implicit trust; **does not** define the ETIS HMAC fixture or certify the Build 2 design |
| §§24.1, 24.4, 24.7 | OWASP GenAI guidance (living) and existing `owasp_agentic_2026` register | Retrieval/prompt-injection and identity/tool misuse threat classes; pin edition and check exact claims before publication |
| §§24.2–24.9 | CAB-001, `build2/identity.py`, `context.py`, `pipeline.py`, `test_scope.py` | Original ETIS architecture mapping, source contracts, fixture behavior and negative tests; requires reproducible tests and independent edition tag |

**Not claimed:** HMAC fixture identity proofing, real source attestations, protected business authorization, provider guarantees or source-page certification. No new bibliography title is introduced; claim-to-page checks stay open.

## Chapter 25 source-to-claim verification queue (publication gates open)

| Section | Basis | Supported claim and limit | Pending gate |
|---|---|---|---|
| §§25.1–25.4 | CAB-001 and original ETIS source, Ch13/16/19/21 | E5 independently gates a consequential request; proposed grant format is ETIS fixture, not a standard | CAB field audit and native Word print review |
| §§25.2–25.4 | NIST SP 800-207 (2020) | Resource-specific verification and no implicit trust; does not certify local same-user socket or HMAC demo | Exact source-page audit |
| §§25.2, 25.7 | OWASP agentic/GenAI guidance | Compromised-agent and tool-misuse motivations; no claim of compliance | Pin and inspect precise guidance edition |
| §§25.5–25.7 | Gray/Reuter (1992); Kleppmann (2017); `build3/test_gate.py` | Local intent, partial effects and unknown-outcome controls; test claims are fixture-specific | Source passage and executable evidence audit |

**Open:** final native Word 7×10 pagination, actual printed figures, reference editions and claim-to-page certification, OS security validation under an isolated E5 deployment, and real-provider guarantees. No new external bibliographic record is necessary.


## Chapter 26 source-to-claim and provider-contract boundary (2026-11-14)

- **Gray and Reuter (1992), Kleppmann (2017):** Use narrowly for durable local state, distributed observations, partial failure and uncertainty in §§26.3–26.5, not as evidence that a commercial payment provider grants idempotency, status consistency or final settlement. Exact source-page inspection remains open.
- **ETIS original artifacts:** CAB-001 E5/C05, E7/C06, E6/C07, E8/C08 mapping; `provider_contracts.py` fixture `Capabilities`/`RefundCommand`/`ProviderObservation`; adapter key identity, lost-ack and read-only query behavior; Figures F26-01/02/03; Build 4 regression tests. These are locally implemented hypotheses, **not externally supported provider capabilities**.
- **Publication evidence still required:** Pin the actual payment-provider API edition, idempotency-key scope and retention, provider-reference identity, status consistency, error taxonomy, settlement definition, security controls and audited sandbox/live tests. Include vendor-specific citations and correct all provenance claims before any claim of production integration.
- **Coverage:** Ch26 §§26.1–26.8; tests, architecture SVG, simulated non-guarantees and Chapter 27–31 handoff explicitly mapped.


## Chapter 27 source-to-claim and boundary register (publication gate open)

- **Lamport (1978); Kleppmann (2017):** logical event ordering, distributed uncertainty and limitations of single-node ownership; neither certifies the ETIS SQLite lease as a distributed consensus protocol.
- **Gray and Reuter (1992); van der Aalst (2013):** local durability and long-running workflow ownership; the exact epoch design and state machine are original ETIS teaching constructs. Edition/page passage inspection remains open.
- **CAB-001 and runnable code:** E2/C02 separate from E5/C05 and E7/C06, E6/C07 and E8/C08. `build5/coordinator.py`, `runner.py`, `test_coordination.py`, the actual Build 4 E5 service and F27-01/02/03 support only the narrow fixture assertions. E2 fences its own SQLite rows, not E5 execution by stale workers.
- **Open evidence:** real distributed state service, E5 current-epoch enforcement, independent finance issuer, protected service identities, audited reconciliation roles, provider-specific contract and final 7×10 Word/source-page certification.

## Back-matter source and citation publication gate

The reader-facing bibliography intentionally avoids a fixed “developed through Chapter N” cutoff and must be updated with each chapter. Chapters 23–27 already have source/claim queues above; identification in the bibliography or register does **not** certify exact edition, pagination, applicability, or the provider-specific contractual guarantees asserted by a claim. Before a publication edition, audit every in-text attribution against primary source passages, confirm DOI/edition metadata, pin living security guidance (including OWASP) and authoritative protocol versions, and record unresolved source limitations. The current appendix/glossary/index revision introduces no new external publication claims; it clarifies CAB-001 and fixture behavior already defined in the manuscript.

## Chapter 28 distributed recovery claims (publication gate open)

- **Gray and Reuter (1992), Kleppmann (2017), Lamport (1978):** Background for transaction boundaries, distributed uncertainty and event ordering. These sources do not establish provider-specific idempotency guarantees or E5 epoch semantics. Verify exact page passages before publication.
- **van der Aalst (2013):** General workflow/recovery background; not a specification of CASE-204 finance authority.
- **Original ETIS repository evidence:** Ch28 §§28.1–28.9; Figures F28-01/02/03; Build 4 `workflow.py`, `ledger.py`, `adapter.py`, `test_*.py`; Build 5 `coordinator.py`, `runner.py`, `test_coordination.py`; pure Chapter 28 `reliability/recovery_cases.py` and `test_recovery_cases.py`. Exact simulated guarantees are defined by source and tests, not external standards.
- **Remaining source and release gates:** Actual vendor API edition, query consistency, idempotency key namespace/retention, settlement proof, service identity, E5 epoch validation, independent recovery operator privileges, Word-for-Mac 7×10 page measurement and claim-to-page verification. There is no new independently verified vendor guarantee or bibliographic record in Chapter 28.



### Post-Chapter 28 executable-assurance handoff (internal engineering evidence)

- `examples/refund-reference-system/ASSURANCE_HANDOFF_CH28_CH31.md` provides 18 existing, named unittest anchors across Builds 0–5 and the Chapter 28 pure recovery fixture. These are **source/test traceability anchors**, not external scholarly citations, commercial provider attestations, proof of native Word pagination, or a completed Chapter 29–31 verification program. The handoff's missing-evidence statements are binding future authoring checks.

## Chapter 29 — security and adversarial agent behavior (November 2026)

| Source / evidence | Chapter 29 use | Verification limitation |
|---|---|---|
| NIST SP 800-53 Rev. 5 | Least privilege, access-control separation and audit design concepts, §§29.2,29.6 | AC-5/AC-6 names checked against the public NIST Rev. 5 PDF; revision/edition and full section pinning remain publication tasks |
| NIST SP 800-218 SSDF | Secure development/negative verification lifecycle, §29.7 | Guidance is not a product certification |
| NIST AI RMF 1.0 | Risk-governance framing, §§29.3,29.6 | Risk framework, not refund authorization semantics |
| OWASP Agentic AI guidance | Untrusted tool output / prompt-injection threat-class background, §29.2 | Pin exact edition before final citation |
| ETIS Build 3 `service.py`, `contracts.py`, Ch29 security harness | Valid E1 assertion denial and separately approved control, §§29.4–29.7 | Same-UID fixture, fake keys and provider; no production OS isolation |

Publication gate: independently verify precise cited source sections, edition, and links; do not infer operational compliance.

## Chapter 30 — reliability, observability and incident response (publication gate open)

| Location | Basis | Supported claim / required limitation |
|---|---|---|
| §§30.1, 30.3–30.5 | Original ETIS operational SLO/incident rubric; CAB-001; Beyer et al., *Site Reliability Engineering* (2016), existing bibliography | Numeric SLOs are explicitly *illustrative*, not empirical performance; map actual denominators, ownership and business risk before use |
| §§30.2–30.4 | CAB-001 C01–C09, Kleppmann (2017), Gray and Reuter (1992); existing Build 4/5 source | Local event histories can conflict with E8; telemetry cannot certify external settlement or protected audit custody; exact external passage verification remains open |
| §§30.5–30.7 | ETIS original Runbook 30-A, `operations/incident.py`, 14 named local tests, Chapter 28/29 harness | Read-only recommendation and non-mutation apply only to fixture; no real E5 epoch enforcement, revocation, immutable external audit or real provider assurance |

**Publication source QA:** verify edition/passage specificity for existing cited works and incident policy against chosen enterprise/provider standards; do not infer provider guarantees from generic reliability sources. Native Word 7×10 and figure proofs remain open.

## Chapter 31 — verification and evidence source/claim register (publication gate open)

| Claim location | Existing source / original artifact | Narrow evidentiary scope | Outstanding source and production gate |
|---|---|---|---|
| §§31.1–31.2 | Original ETIS reference architecture; Chapter 8 and appendix | Separate advisory evidence, trusted E5 decision, E7 local intent and E8 external truth | Contract field audit against controlled catalog; no claim of nine physical services |
| §§31.3–31.4 | NIST AI RMF 1.0 (2023); NIST SP 800-207 (2020); original `assurance/collect.py` | Risk-governed evaluation and resource-centered enforcement are contextual principles; fixture registry and hash format are **ETIS constructions** | Verify exact source passages/editions; no NIST certification claim |
| §§31.3–31.5 | Gray & Reuter (1992), Kleppmann (2017); named Build 4/5, recovery, security and operations tests | Local transactional history, partial effects, bounded evidence, observed fixture non-effects | Actual provider settlement/status contract, protected identity and E9 evidence custody |
| §§31.5–31.7 | `assurance/README.md`, `collect.py`, `test_collect.py`; Figures F31-01/02/03 | Registered seven-method demonstration, 12 collector negative/contract tests and declared exclusions | Independent execution attestation, audit immutability, drift/red-team evaluation and live release rehearsal |

**Source discipline:** Retain existing bibliography records unless adding a claim requires new primary evidence. A claim-to-test link is not a substitute for independent source inspection; exact citations and edition/page certification remain OPEN.

## Chapters 28–31 — reader-bibliography reconciliation and release gate (2026-11-15)

The published bibliography holds **source entries only**, not chapter reading guides, simulated test inventories, status reports or release caveats. These belong in this controlled register, the chapter, `metadata/` QA records, or the relevant companion README. The Appendix B tables give stable reader navigation; Appendix C distinguishes local evidence from external assurance.

| Chapter | Already listed external sources requiring claim/passage review | Original ETIS material (not an externally certified guarantee) | Open publication task |
|---|---|---|---|
| 28 | Lamport (1978); Gray and Reuter (1992); Kleppmann (2017); van der Aalst (2013) | Failure classifier, CASE-204 recovery matrix, local Build 4/5 tests | Verify exact cited passages; establish provider-specific original-operation status contract |
| 29 | NIST SP 800-53 Rev. 5; NIST SP 800-218; AI RMF 1.0; OWASP agentic 2026 guidance | Build 3 adversarial valid-token denial fixture | Pin standard/guidance editions and control scope; validate real credential isolation and revocation |
| 30 | Beyer et al. (2016); Gray and Reuter (1992); Kleppmann (2017) | Illustrative SLOs, incident runbook, read-only operations fixture | Verify reliability claims against source passages and provider/enterprise operating policy; no measured SLO claim |
| 31 | AI RMF 1.0; NIST SP 800-207; Gray and Reuter (1992); Kleppmann (2017) | Claim matrix, seven-case local evidence collector, falsification exercises | Verify exact edition and passage applicability; independently attest production controls and agent evaluation |

No new external title is introduced by this **back-matter structural revision**. A new claim or newly introduced source in a later chapter must trigger a fresh primary-source review, source-register mapping and a properly formatted bibliography entry. Source existence is not evidence that an engineering guarantee has been independently verified.

## Chapter 32 — human oversight and accountable governance (publication source QA open)

| Claim location | Basis and appropriate scope | Required publication verification |
|---|---|---|
| §§32.1–32.3, 32.6 | Original ETIS reference architecture and Chapter 29 Build 3/security harness; transaction identity distinct from grant | Audit precise source/test names and externally protected E5/issuer identity; no production privilege assurance |
| §§32.4–32.5 | Original ETIS human governance design; NIST AI RMF 1.0 (2023) governance context and NIST SP 800-53 Rev. 5 access/separation concepts | Verify specific normative passages before attributing any described control to NIST; do not assert regulatory certification |
| §32.7 | Chapter 30 original Runbook 30-A and simulated `operations/` fixture | Validate actual enterprise incident command, protected E5/E6 disablement and C08 provider inquiry before production |
| §§32.8–32.10 | Original ETIS federated operating model and cost framework; Chapter 31 reproducible educational assurance | No empirical cost improvement or actual human approval/revocation fixture asserted; independent deployment evidence required |

Chapter 32 adds no new external empirical claims or invented citations. Before release, verify exact source passages, current source versions and authoritative provider/policy contracts. Figure 32.1–32.3 inspection and Word-for-Mac 7×10 pagination remain open.

## Chapter 33 — release engineering and operational readiness (November 2026)

- **Foundational source context:** Beyer et al. (2016), *Site Reliability Engineering*, informs service ownership, release engineering, operational safety and staged rollout as a professional discipline; the ETIS CASE-204 gates and stop criteria are authored examples, not measured production outcomes.
- **Supporting context:** NIST AI RMF 1.0 (2023) provides AI-risk governance framing; ISO/IEC 42001:2023 is management-system context only (licensed normative clauses not reproduced or certified); Kleppmann (2017) supports distributed-state and failure caution. Verify exact edition and claim-level section/page before final publication.
- **Authorial engineering prescriptions:** proposed release manifest, `PREPARED`/`APPROVED`/`LIMITED`/`PAUSED` states, financial canary stop conditions, and Runbook 33-A are ETIS designs, not features implemented by an external standard or companion demo.
- **Local evidence navigation:** Build 3 E5 denial, Build 4 original-operation ledger and status-only recovery, Build 5 E2 ownership, Chapter 29 security, Chapter 30 operations, Chapter 31 assurance. Signed releases, production rollback, live provider correctness and protected audit remain external.


## Chapter 34 — economics, risk and lifecycle decisions (November 2026)

| Claim / locus | Source and status | Important limitation |
|---|---|---|
| §34.1, §34.2 | Original ETIS outcome-denominator and lifecycle costing framework, consistent with Ch5, Ch16–17 and Ch32–33 | Not a measured commercial workflow or audited cost allocation |
| §34.3, Tables 34.2–34.3 | Original ETIS fully hypothetical economic scenarios and arithmetic | No performance, value, loss or causality observations; all values illustrative |
| §34.4 | NIST AI RMF 1.0 (2023), risk governance context (already in bibliography) | No NIST approval of E5 control, monetary estimate or release gate; exact passages require final verification |
| §§34.5–34.7 | Existing Builds 0–5, security, reliability, operations, assurance fixtures and companion READMEs | Tests establish bounded simulation evidence only; no real invoices, staffing telemetry, live provider, release policy or ROI tracking |

**Publication source gate:** verify edition/precise passage of the existing NIST AI RMF reference and provide real enterprise observations before making empirical or production claims. No new external bibliographic entry is asserted in this chapter.
