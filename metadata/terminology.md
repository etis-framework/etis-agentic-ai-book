# Controlled terminology

- **AI model**: computational model providing capabilities such as classification, prediction, or language generation.
- **AI agent**: goal-directed software component selecting among permitted steps using reasoning or decision logic.
- **Agentic workflow**: coordinated business process that may include agents, deterministic tasks, and human approvals.
- **Agentic AI system**: full engineered system, not simply a model or agent.
- **Authority**: enforceable permission under authenticated identity, policy, scope, and business preconditions.
- **System of record**: authoritative business-state owner.
- **E1–E9**: logical architecture responsibility IDs; use full names in prose.
- **C01–C09**: interface/contract IDs governed by CAB-001.
- **Worker**: bounded task executor (deterministic, model-based, or hybrid); a worker need not be an AI agent.
- **Generalist agent**: agent assigned a broader permitted task family; not unrestricted authority.
- **Specialist agent**: agent assigned a narrower capability/tool surface, with explicit eligibility and contracts.
- **Coordination topology**: authoritative routing, ownership, acceptance and recovery arrangement (E2/E7).
- **Communication topology**: permitted message paths among coordinator and workers; peers cannot transfer authoritative ownership.
- **Capability registry**: platform-supported E2 discovery and readiness/identity catalog; not E7 state or independent access authorization.

First-use acronym rule: spell out before abbreviation (e.g., identity and access management (IAM)).
- **E2 coordination ownership**: work routing, lease/epoch authority and scheduling rules; E7 may persist E2's state but does not acquire E2 decision rights.
- **E7 durable state**: atomic persisted local intent, observations, transitions and workflow evidence; not an E8 provider truth source or an independent business approval.
- **E5 independent enforcement**: consequential authorization and controlled dispatch; a process boundary under the same OS identity is not full hostile-process isolation.
- **RF-1042 trusted payment operation**: E5-controlled stable ID, not a C04 advisory `operation_id`.
- **Working index**: alphabetical chapter/section navigation while manuscript is developing; final page locators require frozen print proofs.


Chapter 32: *decision right*, *accountable governance decision*, *human intervention*, *break-glass authority*, and *governance policy version* are specified governance concepts, not new companion implementation interfaces. Reviewers must distinguish release approval, case-bound finance approval and trusted provider dispatch.
