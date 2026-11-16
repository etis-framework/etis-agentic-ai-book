# References and bibliography

Selected research, standards and professional sources referenced in this volume. Chapter-level claim mappings and remaining passage-verification requirements are maintained separately in the editorial source register; the bibliography is a reader reference, not a certification of any particular implementation.

## Foundational systems engineering

- Bass, Len, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.
- Beyer, Betsy, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds. *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly Media, 2016. https://sre.google/sre-book/table-of-contents/
- Garcia-Molina, Hector, and Kenneth Salem. “Sagas.” *ACM SIGMOD Record* 16, no. 3 (1987): 249–259. https://doi.org/10.1145/38713.38742
- Gray, Jim, and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992.
- Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003.
- Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
- Fielding, Roy T., Mark Nottingham, and Julian Reschke, eds. *HTTP Semantics*. RFC 9110, June 2022. https://doi.org/10.17487/RFC9110. See §9.2.2 on HTTP-method idempotency; provider-specific payment guarantees require separate contract evidence.
- Lamport, Leslie. “Time, Clocks, and the Ordering of Events in a Distributed System.” *Communications of the ACM* 21, no. 7 (1978): 558–565. https://doi.org/10.1145/359545.359563

## Artificial intelligence and agent research

- Lewis, Patrick, et al. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *Advances in Neural Information Processing Systems* 33 (2020): 9459–9474.
- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th ed. Pearson, 2020.
- Schick, Timo, et al. “Toolformer: Language Models Can Teach Themselves to Use Tools.” *Advances in Neural Information Processing Systems* (2023). https://arxiv.org/abs/2302.04761
- Yao, Shunyu, et al. “ReAct: Synergizing Reasoning and Acting in Language Models.” *International Conference on Learning Representations* (2023). https://arxiv.org/abs/2210.03629

- Anthropic Engineering. “Building Effective Agents.” December 19, 2024. https://www.anthropic.com/research/building-effective-agents (Vendor engineering guidance.)
- OpenAI. *A Practical Guide to Building Agents*. January 15, 2026. https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf (Vendor engineering guide.)
- Yao, Shunyu, Noah Shinn, Pedram Razavi, and Karthik Narasimhan. “τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.” arXiv:2406.12045, 2024. https://arxiv.org/abs/2406.12045

- Fowler, Martin. “Microservice Trade-Offs.” July 1, 2015. https://martinfowler.com/articles/microservice-trade-offs.html (General distributed-service tradeoffs; not empirical agent benchmarking.)

## Governance and assurance

- National Institute of Standards and Technology. *Security and Privacy Controls for Information Systems and Organizations*. NIST Special Publication 800-53, Revision 5 (updated control catalog; verify edition at publication). https://doi.org/10.6028/NIST.SP.800-53r5. See AC-5 (separation of duties) and AC-6 (least privilege); controls are guidance, not proof of ETIS deployment compliance.
- Souppaya, Murugiah, Karen Scarfone, and Donna Dodson. *Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities*. NIST SP 800-218, February 2022. https://doi.org/10.6028/NIST.SP.800-218.

- International Organization for Standardization and International Electrotechnical Commission. *ISO/IEC 42001:2023 — Information Technology — Artificial Intelligence — Management System*. 2023.
- Rose, Scott, Oliver Borchert, Stu Mitchell, and Sean Connelly. *Zero Trust Architecture*. NIST Special Publication 800-207, August 2020. https://doi.org/10.6028/NIST.SP.800-207.
- Hu, Vincent C., David Ferraiolo, David R. Kuhn, et al. *Guide to Attribute Based Access Control (ABAC) Definition and Considerations*. NIST Special Publication 800-162, updated August 2, 2019. https://doi.org/10.6028/NIST.SP.800-162. (ABAC terminology and control attributes; no specific refund-policy guarantee.)
- National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1, 2023. https://doi.org/10.6028/NIST.AI.100-1
- National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1, 2024. https://doi.org/10.6028/NIST.AI.600-1
- OWASP Foundation. *OWASP GenAI Security Project*. Living resource; version must be pinned before final publication. https://genai.owasp.org/

- OWASP GenAI Security Project. *OWASP Top 10 for Agentic Applications for 2026*. December 9, 2025. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- Model Context Protocol. *Model Context Protocol Specification*, dated July 28, 2026. https://modelcontextprotocol.io/specification/2026-07-28 (Normative protocol scope; see authorization/security sections; not business policy enforcement.)
- A2A Protocol Community. *Agent2Agent (A2A) Protocol Specification*, released 1.0 series (version 1.0.0). https://a2a-protocol.org/v1.0.0/specification/ (Normative protocol description, not a certification of enterprise authorization or financial settlement.)
- National Institute of Standards and Technology. “Announcing the AI Agent Standards Initiative for Interoperable and Secure Innovation.” February 17, 2026. https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure

## Business processes, requirements, and human–automation interaction

- van der Aalst, Wil M. P. “Business Process Management: A Comprehensive Survey.” *ISRN Software Engineering* 2013, article 507984 (2013). https://doi.org/10.1155/2013/507984
- Parasuraman, Raja, Thomas B. Sheridan, and Christopher D. Wickens. “A Model for Types and Levels of Human Interaction with Automation.” *IEEE Transactions on Systems, Man, and Cybernetics — Part A* 30, no. 3 (2000): 286–297. https://doi.org/10.1109/3468.844354
- Parasuraman, Raja. “Designing Automation for Human Use: Empirical Studies and Quantitative Models.” *Ergonomics* 43, no. 7 (2000): 931–951. https://doi.org/10.1080/001401300409125
- ISO/IEC/IEEE. *ISO/IEC/IEEE 29148:2018: Systems and Software Engineering — Life Cycle Processes — Requirements Engineering*. 2nd ed. 2018. https://www.iso.org/standard/72089.html (Normative text requires licensed review.)

- FinOps Foundation. *FinOps Framework 2025*. https://www.finops.org/framework/ (accessed November 2026).
- FinOps Foundation. *Unit Economics*, FinOps Framework capability guidance. https://www.finops.org/framework/capabilities/unit-economics/ (accessed November 2026).
