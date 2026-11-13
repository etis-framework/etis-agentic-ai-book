# CASE-204 companion reference implementation

**This code is educational, not a real payment service.** It uses fictional data and cannot send refunds. The book and this companion source are versioned in the same authoritative Git repository.

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

**Development-checkout note:** Build 0 is the current executable checkpoint. Builds 1–5 are added and verified with their respective chapters; a directory or row in this table is not evidence that runnable code has already been released. The textbook describes the complete six-build learning sequence rather than editorial completion status.

The builds are teaching increments, **not a compulsory Design A → B → C migration**. Design C remains an optional bounded investigator. A professional reader should review each build's source, tests, figures and stated non-guarantees together.

## Directory layout

```text
examples/refund-reference-system/
├── README.md                 # This reader entry point
├── ARCHITECTURE.md           # E1–E9 mapped to actual Build 0 behavior
├── CONTRIBUTING.md           # Educational QA and review standard
└── build0/
    ├── README.md             # Executable exercises and observed evidence
    ├── refund.py             # Standard-library local simulator
    └── test_refund.py        # Isolated unittest evidence
```

The canonical figure masters remain in `assets/shared-figures/sources/`; do not duplicate them inside code builds. The reference architecture is explained in Chapter 8 and the architectural-contract appendix.

**Start at the repository root:**

```sh
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

Then follow `build0/README.md` to reproduce a lost provider acknowledgment and examine the two separate SQLite stores. No `pip` install, real credentials, or live network connection is required.

## Version and publication policy

The development repository is the only editable code authority. Every published edition must identify its matching **immutable Git tag or source snapshot** with a tested release and errata trail. The publication plan is to make the book repository publicly readable, subject to a review that excludes restricted editorial content. If distribution needs require an examples-only archive, generate it from this single authoritative repository and its immutable edition tag rather than independently maintaining another implementation.
