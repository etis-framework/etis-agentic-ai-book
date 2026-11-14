# CASE-204 companion reference implementation

**This code is educational, not a real payment service.** Its E7 local operational record and simulated E8 provider record deliberately show why local knowledge differs from authoritative business truth. It uses fictional data and cannot send refunds. The book and this companion source are versioned in the same authoritative Git repository.

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
| 3 | 25 | Independent trusted consequential execution |
| 4 | 26 | Provider contract validation and authoritative reconciliation |
| 5 | 27 | Optional coordination, containment and operational hardening |

Each chapter identifies its executable checkpoint and corresponding test evidence. Later checkpoints do not supersede the independent Build 0 baseline.

The builds are teaching increments, **not a compulsory Design A → B → C migration**. Design C remains an optional bounded investigator. A professional reader should review each build's source, tests, figures and stated non-guarantees together.

## Directory layout

```text
examples/refund-reference-system/
├── README.md                 # This reader entry point
├── ARCHITECTURE.md           # E1–E9 maps for Builds 0–2
├── CONTRIBUTING.md           # Contribution and review workflow
├── ENGINEERING_STANDARD.md  # Normative requirements for Builds 0–5
├── TESTING.md                # Scenario-to-evidence matrix and assurance limits
├── build0/
    ├── README.md             # Executable exercises and observed evidence
    ├── refund.py             # Standard-library local simulator
    └── test_refund.py        # Isolated unittest evidence
├── build1/
    ├── README.md             # Bounded advisory exercises
    ├── contracts.py          # Typed C02/C04 data and strict validation
    ├── model_interface.py    # Injectable untrusted proposal port
    ├── advisory.py           # Deterministic advisor, no privileged effects
    ├── demo.py               # Offline, zero-payment demonstration
    └── test_advisory.py      # Denial, failure and no-effect tests
└── build2/
    ├── README.md             # Scoped identity/context exercises
    ├── identity.py           # Fixture assertion issuer/verifier
    ├── context.py            # E4 scoped catalog/provenance gate
    ├── pipeline.py           # Build 1 composition without effect API
    ├── demo.py               # Offline negative/positive scenarios
    └── test_scope.py         # Scope, failure and no-write tests
```

The canonical figure masters remain in `assets/shared-figures/sources/`; do not duplicate them inside code builds. The reference architecture is explained in Chapter 8 and the architectural-contract appendix.

**Start at the repository root:**

```sh
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

Consult `TESTING.md` for the verification matrix and `ENGINEERING_STANDARD.md` for the safeguards and acceptance criteria every later build must preserve. Then follow `build0/README.md` to reproduce a lost provider acknowledgment and examine the two separate SQLite stores. No `pip` install, real credentials, or live network connection is required.

## Version and publication policy

The development repository is the only editable code authority. Every published edition must identify its matching **immutable Git tag or source snapshot** with a tested release and errata trail. The publication plan is to make the book repository publicly readable, subject to a review that excludes restricted editorial content. If distribution needs require an examples-only archive, generate it from this single authoritative repository and its immutable edition tag rather than independently maintaining another implementation.

## Run Build 1 (Chapter 23)

Build 1 is now an independently runnable **untrusted advisory** checkpoint. Begin with [`build1/README.md`](build1/README.md); execute `python3 examples/refund-reference-system/build1/demo.py` and `python3 -m unittest discover -s examples/refund-reference-system/build1 -p 'test_*.py' -v`. It does not invoke Build 0, change E7/E8 or create RF-1042. Treat its `C04` proposals as review candidates, never approval. The optional model interface is tested with injected fakes; no live model or credentials are needed.

## Run Build 2 (Chapter 24)

Build 2 adds **fixture-only** E1 identity-assertion verification and an E4/C03 scoped context lookup before reusing the unmodified Build 1 adviser. Read [`build2/README.md`](build2/README.md) for exact runnable scenarios and the 13-test matrix; execute `python3 examples/refund-reference-system/build2/demo.py` from the repository root. The assertion key is public educational data, **not** a production credential or authenticated-identity guarantee. C04 advice remains untrusted; RF-1042, E7 and E8 are not touched.
