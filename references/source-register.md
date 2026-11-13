# Source and citation register — developed Chapters 1–16

**Status: claim locations mapped; final publication certification remains open.** Earlier chapters were mapped through Chapter 7; this pass extends mapped, limited-scope attribution through Chapter 16. Publication certification still requires checking exact passages, edition/page numbers, stable links, and whether each source actually supports each claim. The dates below describe publications, **not** a claim that the research landscape has been comprehensively checked through November 2026.

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

## Claim-level QA queue

- [ ] Ch1: distinguish research findings about agents from recommended enterprise control design.
- [ ] Ch1: establish evidence for any quantitative business, latency, accuracy, or cost claim before adding it.
- [ ] Ch2: verify any priority claim such as “first,” “invented,” or “originated.”
- [ ] Ch2: check the exact semantics of ACID, idempotency, at-least-once delivery, and external effects.
- [ ] Ch2: ensure all diagrams express ownership and observations accurately.
- [ ] Both: confirm edition, authors, identifiers, and stable URLs against original publisher or standards body.
- [ ] Both: complete source-specific page or section references and editorial sign-off.

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

**Additional source candidates for later verification, not yet cited as facts:** NIST SP 800-53 Rev. 5 (least privilege, audit); NIST SP 800-218 SSDF (secure development); NIST AI 100-4 (if relevant to evaluation); RFC 9110 (HTTP idempotent method semantics, not provider business idempotency); OWASP Agentic AI guidance (pin version); vendor provider idempotency documentation (only for the selected implementation). This is a prioritized research queue, not a claim of verification.


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
