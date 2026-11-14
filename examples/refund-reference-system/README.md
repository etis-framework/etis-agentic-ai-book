# CASE-204 companion reference implementation

**This code is educational, not a real payment service.** Its durable operational state (E7) and simulated authoritative payment-provider record (E8) deliberately show why local knowledge differs from business truth. It uses fictional data and cannot send refunds. The book and this companion source are versioned in the same authoritative Git repository.

## Locate the book and work through the builds

**Official repository:** https://github.com/etis-framework/etis-agentic-ai-book  
**Companion directory:** https://github.com/etis-framework/etis-agentic-ai-book/tree/main/examples/refund-reference-system  
**Reader entry point:** `examples/refund-reference-system/README.md`

The GitHub repository is private while the manuscript is in development and is intended to become public with the book. In the published edition, use the corresponding Git release/tag to reproduce the printed code exactly; `main` may have advanced.

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

## Directory layout

```text
examples/refund-reference-system/
├── README.md                 # Reader entry point
├── ARCHITECTURE.md           # Architecture mappings across Builds 0–5
├── CONTRIBUTING.md           # Contribution and review workflow
├── ENGINEERING_STANDARD.md  # Engineering and review requirements
├── TESTING.md               # Evidence matrix and assurance limits
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
    ├── README.md
    ├── architecture.svg
    ├── provider_contracts.py
    ├── adapter.py
    ├── ledger.py
    ├── workflow.py
    ├── service.py
    ├── demo.py
    └── test_provider.py
└── build5/
    ├── README.md
    ├── architecture.svg
    ├── coordinator.py
    ├── runner.py
    ├── demo.py
    └── test_coordination.py
```

**Part IV synthesis:** [Implementation-to-evidence map](IMPLEMENTATION_EVIDENCE_MAP.md) traces all six build deltas, E1–E9/C01–C09, three consequential scenarios and production omissions. It explains why the Build 5 E2→Build 4 E5 runtime does not also run the Build 1/2 advisory/retrieval pipeline. The teaching progression is cumulative; the runnable checkpoints are only partly composed.

The canonical figure masters remain in `assets/shared-figures/sources/`; do not duplicate them inside code builds. The reference architecture is explained in Chapter 8 and the architectural-contract appendix.

**Start at the repository root:**

```sh
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

Consult `TESTING.md` for the verification matrix and `ENGINEERING_STANDARD.md` for the safeguards and acceptance criteria every later build must preserve. Then follow `build0/README.md` to reproduce a lost provider acknowledgment and examine the two separate SQLite stores. No `pip` install, real credentials, or live network connection is required.

## Version and publication policy

The development repository is the only editable code authority. Every published edition must identify its matching **immutable Git tag or source snapshot** with a tested release and errata trail. The publication plan is to make the book repository publicly readable, subject to a review that excludes restricted editorial content. If distribution needs require an examples-only archive, generate it from this single authoritative repository and its immutable edition tag rather than independently maintaining another implementation.

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
