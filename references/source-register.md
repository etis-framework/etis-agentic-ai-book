# Source register — chapters 1–3

**Status: curated, not citation-certified.** V7 establishes chapter-level attribution and a claim-verification queue. Publication certification still requires checking exact passages, edition/page numbers, stable links, and whether each source actually supports each claim. The dates below describe publications, **not** a claim that the research landscape has been comprehensively checked through November 2026.

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
