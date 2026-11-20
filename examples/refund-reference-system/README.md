# CASE-204 companion reference implementation

**This code is educational, not a real payment service.** Its durable operational state (E7) and simulated authoritative payment-provider record (E8) deliberately show why local knowledge differs from business truth. It uses fictional data and cannot send refunds. The book and this companion source are versioned in the same authoritative Git repository.

## Locate the book and work through the builds

**Official repository:** https://github.com/etis-framework/etis-agentic-ai-book
**Companion directory:** https://github.com/etis-framework/etis-agentic-ai-book/tree/main/examples/refund-reference-system
**Reader entry point:** `examples/refund-reference-system/README.md`

For the first printed edition, use the immutable **`v1.0.0`** Git tag once published (see the [release procedure](../../RELEASE.md)); `main` may advance. To run every companion suite without a manuscript build, use `python3 publishing/scripts/check_companion_release.py` from the repository root. See the [five-minute setup](../../docs/GETTING_STARTED.md).

| Build | Book chapter | Engineering lesson |
|---|---|---|
| 0 | 22 | Deterministic approval, local durable intent, simulated provider truth, UNKNOWN and reconciliation |
| 1 | 23 | Bounded advisory proposal (not transaction authorization) |
| 2 | 24 | Scoped identity and provenance-bearing context |
| 3 | 25 | Separate-process, independently checked trusted-execution request path (fixture) |
| 4 | 26 | Provider contract validation and authoritative reconciliation |
| 5 | 27 | Optional coordination, containment and operational hardening |

Each chapter identifies its executable checkpoint and corresponding test evidence. Later checkpoints do not supersede the independent Build 0 baseline.

The builds are teaching increments, **not a compulsory Design A → B → C migration**. Design C remains an optional bounded investigator. A professional reader should review each build's source, tests, figures and stated non-guarantees together.

## Chapter-to-implementation navigation (recovery, security and operations)

Chapters **28–31** use the same stable CASE-204/RF-1042 case and existing Builds 0–5, rather than introducing four new payment implementations. Open the indicated README before changing code:

| Chapter | Reader starting point | Executable verification | What the exercise must not claim |
|---|---|---|---|
| 28 — recovery | `reliability/README.md`; `build4/ledger.py`, `build4/workflow.py` | `reliability/test_recovery_cases.py` and `build4/test_provider.py` | A missing acknowledgment means payment failure or retry permission |
| 29 — security | `security/README.md`; `build3/service.py` | `security/test_adversarial_cases.py` | Valid E1 token means business approval or OS-isolated credential custody |
| 30 — incidents | `operations/README.md`; `operations/incident.py` | `operations/test_incident.py` | A synthetic provider status proves settlement, or an incident observer can issue an effect |
| 31 — assurance | `assurance/README.md`; `assurance/collect.py` | `assurance/test_collect.py` plus seven registered earlier methods | Green local fixture results equal real provider, independent credential or protected E9 certification |

All paths are relative to `examples/refund-reference-system/`. The Chapter 30 observer's read-only database queries and serialized `Finding` output are implemented in `operations/incident.py`. The simulated `provider_refunds` records originate in `build4/adapter.py`; historical `operation_events` are in `build4/ledger.py`. Test code deliberately constructs fixture records; the observer has no payment client or provider credentials. All three exercises should explicitly relate agent behavior (untrusted proposals, bounded delegation, stale agents and tool misuse) to deterministic independent control and operational accountability.

## Guided source-reading lab (recommended before changing code)

Start with [**Read the implementation as an engineer**](LEARNING_PATH.md) after the chapter overview. It supplies one source-to-test path for every build and the Chapter 28–31 fixtures, three guided falsification labs, observed-versus-proposed evidence distinctions, and a concise submission rubric. Follow **actual named functions and test assertions** rather than treating the green suite count as proof of production trust. It does not add code, a seventh build, or an unimplemented memory/protocol guarantee.

## Protocol boundary exercise — MCP and A2A (design-only)

Read [**MCP/A2A boundary study**](PROTOCOL_BOUNDARY_STUDY.md) after the Build 3 authorization and Build 4 recovery labs. It maps a conceptual MCP client, untrusted tool listings, optional server facades, shared E5/credential enforcement and A2A peer tasks to the **actual** educational modules. It includes five falsification questions and identifies the real tests demonstrating transfer principles. **No MCP client, MCP server, A2A implementation, token-exchange service, or protocol-conformance test exists in Builds 0–5.**

## Directory layout

```text
examples/refund-reference-system/
├── README.md                 # Reader entry point
├── LEARNING_PATH.md          # Guided source, negative-test and evidence labs
├── ARCHITECTURE.md           # Architecture mappings across Builds 0–5
├── CONTRIBUTING.md           # Contribution and review workflow
├── ENGINEERING_STANDARD.md  # Engineering and review requirements
├── TESTING.md               # Evidence matrix and assurance limits
├── ASSURANCE_HANDOFF_CH28_CH31.md # Current tests vs future assurance claims
├── build0/
│   ├── README.md
│   ├── architecture.svg      # Actual source/module architecture
│   ├── refund.py
│   └── test_refund.py
├── build1/
│   ├── README.md
│   ├── architecture.svg
│   ├── contracts.py
│   ├── model_interface.py
│   ├── advisory.py
│   ├── demo.py
│   └── test_advisory.py
├── build2/
│   ├── README.md
│   ├── architecture.svg
│   ├── identity.py
│   ├── context.py
│   ├── pipeline.py
│   ├── demo.py
│   └── test_scope.py
├── build3/
│   ├── README.md
│   ├── architecture.svg
│   ├── contracts.py
│   ├── client.py
│   ├── service.py
│   ├── demo.py
│   └── test_gate.py
├── build4/
│   ├── README.md
│   ├── architecture.svg
│   ├── provider_contracts.py
│   ├── adapter.py
│   ├── ledger.py
│   ├── workflow.py
│   ├── service.py
│   ├── demo.py
│   └── test_provider.py
├── operations/             # Ch30 read-only incident observer and evidence tests
│   ├── README.md
│   ├── architecture.svg
│   ├── incident.py
│   └── test_incident.py
├── assurance/              # Ch31 evidence collector (not Build 6)
│   ├── README.md
│   ├── architecture.svg      # Actual collector and source/test dependencies
│   ├── collect.py
│   └── test_collect.py
├── security/               # Ch29 adversarial harness: real Build 3 E5 subprocess
│   ├── README.md
│   ├── architecture.svg      # Actual test/module architecture
│   └── test_adversarial_cases.py
├── build5/
│   ├── README.md
│   ├── architecture.svg
│   ├── coordinator.py
│   ├── runner.py
│   ├── demo.py
│   └── test_coordination.py
└── reliability/
    ├── README.md
    ├── recovery_cases.py
    └── test_recovery_cases.py
```

**Part IV synthesis:** [Implementation-to-evidence map](IMPLEMENTATION_EVIDENCE_MAP.md) traces all six build deltas, E1–E9/C01–C09, three consequential scenarios and production omissions. It explains why the Build 5 E2→Build 4 E5 runtime does not also run the Build 1/2 advisory/retrieval pipeline. The teaching progression is cumulative; the runnable checkpoints are only partly composed.

The canonical figure masters remain in `assets/shared-figures/sources/`; do not duplicate them inside code builds. The reference architecture is explained in Chapter 8 and the architectural-contract appendix.

**Start at the repository root:**

```sh
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

Consult `TESTING.md` for the verification matrix and `ENGINEERING_STANDARD.md` for the safeguards and acceptance criteria every later build must preserve. Then follow `build0/README.md` to reproduce a lost provider acknowledgment and examine the two separate SQLite stores. No `pip` install, real credentials, or live network connection is required.

## Version and publication policy

This Git repository is the single code authority. The first-edition companion release is **`v1.0.0`** once its tag is published, with a [release procedure](../../RELEASE.md), [changelog](../../CHANGELOG.md) and [errata process](../../ERRATA.md). Use the tagged source for printed-edition reproduction; `main` may evolve. No separate, independently maintained examples archive is authoritative.

## Run Build 1 (Chapter 23)

Build 1 is now an independently runnable **untrusted advisory** checkpoint. Begin with [`build1/README.md`](build1/README.md); execute `python3 examples/refund-reference-system/build1/demo.py` and `python3 -m unittest discover -s examples/refund-reference-system/build1 -p 'test_*.py' -v`. It does not invoke Build 0, change E7/E8 or create RF-1042. Treat its advisory action proposals (C04) as review candidates, never approval. The optional model interface is tested with injected fakes; no live model or credentials are needed.

## Run Build 2 (Chapter 24)

Build 2 adds **fixture-only** admission-and-identity (E1) assertion verification and a scoped context (E4) lookup via the context-query contract (C03) before reusing the unmodified Build 1 adviser. Read [`build2/README.md`](build2/README.md) for exact runnable scenarios and the 13-test matrix; execute `python3 examples/refund-reference-system/build2/demo.py` from the repository root. The assertion key is public educational data, **not** a production credential or authenticated-identity guarantee. C04 advice remains untrusted; RF-1042, E7 and E8 are not touched.

## Run Build 3 (Chapter 25)

Read [`build3/README.md`](build3/README.md) and its embedded source-architecture SVG first. Build 3 demonstrates a separate trusted-execution-and-authority (E5) process checking a **valid E1 fixture assertion AND independently issued transaction-specific signed approval** before it may create RF-1042 or call the simulated E6/E8 adapter. Run `python3 examples/refund-reference-system/build3/demo.py --scenario compromised` (expected denial/exit 2), then `--scenario approved` (one confirmed fixture operation). Tests use a fresh, locally generated fixture key; no real payment or credential service is involved. Same-user local processes are **not** an OS-level hostile-code isolation guarantee.

## Run Build 4 (Chapter 26)

Build 4 extends the **separately enforced E5 request path** with a versioned **E6/C07 provider adapter**, a mock **E8/C08 authoritative status lookup**, and an explicit **E7/C06 durable operation and reconciliation** path. Begin with [`build4/README.md`](build4/README.md) and its embedded source/module architecture. Run `python3 examples/refund-reference-system/build4/demo.py --scenario lost-ack` followed by the Build 4 tests. E8 may commit the single RF-1042 effect while E7 remains UNKNOWN until read-only reconciliation confirms the provider's record. These are fixture-provider guarantees only, not commercial processor promises, real security isolation or proof of final settlement.

## Run Build 5 (Chapter 27)

Build 5 adds optional local **coordination and durable ownership (E2)** to the still-independent Build 4 **trusted execution (E5)** boundary. Read [`build5/README.md`](build5/README.md) and its embedded source-architecture SVG, then run `python3 examples/refund-reference-system/build5/demo.py --scenario lost-ack`. An expired owner cannot mutate E2; a successor can reconcile but not reissue the $500 refund. **This is not end-to-end execution fencing:** E5 does not consume E2 lease epochs, and the demonstration uses the same local OS identity.

## Use the same tested evidence in Chapters 28–31

The [Chapter 28–31 assurance handoff](ASSURANCE_HANDOFF_CH28_CH31.md) maps exact Build 0–5 and recovery test methods to distributed failure, adversarial denial, operational readiness, and evaluation claims. **Chapters 29–31 now contain executable, bounded local fixtures.** The handoff distinguishes observed results from protected boundaries and independent production evidence that is still missing. It is not a new build and does not compose the checkpoints into one payment service.

### Chapter 29 security adversarial harness

[Security harness: valid-token denial and positive-control evidence](security/README.md) is a **non-progressive** test fixture against the actual Build 3 E5 subprocess, not Build 6 or a new payment implementation. It has a checked-in [module architecture SVG](security/architecture.svg), six negative/control tests, and explicit simulated-versus-real assurance limits.

## Chapter 31 — assurance is not Build 6

[`assurance/README.md`](assurance/README.md) embeds the collector's source/module `architecture.svg`, explains seven source-controlled cross-chapter test registrations and 12 fail-closed harness tests, and gives a reproducible versioned JSON evidence command. The collector does not call E5/E6, mutate E7 or contact E8; its tests invoke *existing* fixtures whose mock effects are isolated in temporary databases. Passing output explicitly marks production certification false and enumerates unimplemented/external controls.
