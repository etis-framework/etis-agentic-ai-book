# Chapter 22 companion code and reader navigation — six-lens review

Status: **development QA passed; publication gates remain open**. Baseline: V3 Chapter 22 working tree plus new 360-page rendered manuscript provided November 13, 2026. Authoritative architecture: existing CAB-001, unchanged. This document is **internal** and is not part of the reader-facing manuscript.

## Reader discovery trace

- Preface: now identifies executable, source-controlled, tested examples as a distinguishing educational feature, without implying production certification.
- Introduction and *How to use this book*: identify the official `etis-framework/etis-agentic-ai-book` GitHub location, entry `examples/refund-reference-system/README.md`, and edition-tag expectations.
- Chapter 1: introduces implementation and test trajectory; Chapter 22: gives the first executable command and evidence expectations.
- Part IV: explains Builds 0–5 as teaching checkpoints, not a Design A → B → C obligation.
- Appendix: gives companion access path and contract navigation.
- Code README → build README / ARCHITECTURE / TESTING / CONTRIBUTING: reader can reproduce, interpret, challenge and extend without internal production files.

## Lens findings and dispositions

| Lens | Challenge | Decision/evidence |
|---|---|---|
| Implementing engineer | Can a reader execute without third-party dependencies? | Python stdlib `unittest`, `sqlite3`; README root-relative commands; ten passing tests. Code stays a deliberately small educational module, not falsely modularized services. |
| Enterprise architect | Does package structure suggest alternate or added E-domains? | No. Architectural README maps fixture responsibilities and absent E3/E4; C01–C09 remain reference contracts; E7 and simulated E8 separate. |
| Advanced student | Are source, tests, and outcomes explorable? | Build-specific walkthrough, `TESTING.md` matrix, state inspection, educational comments explaining authority and uncertainty. |
| Security/assurance | Can a token or a test bypass live E5 controls? | No live E1/E5/E6 boundary is asserted. `authorize` is a fixture, not protection against importing a Python function; principal/tenant/approval denial tests included; actual compromised-agent test remains planned for Chapters 29/31. |
| SRE/operations | Can a lost acknowledgment induce a duplicate? | Fixture rejects redispatch after UNKNOWN, preserves operation ID, independently queries provider mock; durable reopen test added. No claims for concurrency fencing, network guarantees, or live provider idempotency. |
| Business owner | Is source code a credible educational advantage? | Preface connects runnable, inspectable code to evidence-based judgments rather than claiming a certified payment platform. Design B remains conditional production candidate; Design C optional. |

## Open gates — do not close in this patch

1. Native Word for Mac actual printed pagination, style parity, 7×10 figure readibility and complete-book reflow.
2. Part I exceeds its approved 95-page allocation in prior measurement; source length checks are not page proof.
3. Exact source-edition/page-to-claim verification and publication metadata/rights.
4. No real payment provider, concurrency fencing, cryptographic identity or live approval semantics in Build 0. These are intentionally absent, not defects concealed by successful tests.
5. GitHub repository is private during development. Publication requires access/rights review, public publication decision execution, and immutable edition tags.

## Commands used for development verification

```sh
make book-docx
make check
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
python3 publishing/scripts/check_companion_code_quality.py
```

The complete `make check` and ten unit tests passed in the reconstructed repository snapshot. They **do not** attest to the live user's Git branch, native Microsoft Word pagination, external payment behavior, or production security.
