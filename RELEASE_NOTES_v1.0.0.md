# Engineering Agentic AI Systems — First-Edition Companion v1.0.0

**Official companion to:** *Engineering Agentic AI Systems — Build, Secure, Verify, and Operate Trustworthy AI Agents*, ETIS Professional Computing Series, First Edition (2026), by William T. O’Connell, Ph.D.

**Paperback ISBN:** 979-8-9966760-6-4 · **Hardcover ISBN:** 979-8-9966760-7-1

## What is included

This release provides the source-matched, executable educational companion for the book's continuing fictional **CASE-204 $500 refund** and stable financial-operation identity **RF-1042**:

- **Builds 0–5 (Chapters 22–27):** deterministic refund baseline; bounded review-only advice; scoped identity/context; independently checked E5 request authorization; mock provider integration/reconciliation; durable E2 coordination and its explicitly limited fencing.
- **Chapters 28–31:** recovery decision exercises, valid-token/unauthorized-refund negative tests, read-only incident observation, and reproducible bounded assurance evidence.
- **Learning materials:** architecture SVG diagrams for implemented modules, chapter navigation, source-reading labs, executable tests, and clear expected negative outcomes.

All examples use **Python 3.10+ and the standard library only**. No API key, payment account, commercial provider, model subscription or package installation is required.

## Getting started (no Git required)

1. Open this GitHub Release and download **Assets → Source code (zip)** for **`v1.0.0`**.
2. Extract it, open a terminal in the extracted top-level folder, and follow [Getting Started](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/docs/GETTING_STARTED.md).
3. On **macOS/Linux**, run `python3 publishing/scripts/check_companion_release.py` for all ten suites. On **native Windows**, run `py -3 publishing/scripts/check_companion_release.py --portable` for Builds 0–2 and architecture checks. The full suite uses Unix-domain sockets and requires macOS/Linux.
4. Begin with [Build 0](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/examples/refund-reference-system/build0/README.md), then use the [guided learning path](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/examples/refund-reference-system/LEARNING_PATH.md) for Builds 1–5 and Chapters 28–31.

**Expected completion:** `PASS: all 10 local fixture suites and architecture/documentation check.` (or the clearly identified portable-subset PASS on Windows). Intentionally denied requests or UNKNOWN outcomes in individual demos are often correct security/recovery results, not installation failures.

## Engineering claims and boundaries

**AI proposes; engineers verify.** An E1 token does not authorize an E5 financial effect. C04 recommendations do not mint RF-1042. An uncertain provider response does not prove the refund failed; reconciliation queries mock business truth without resending the effect.

**This is not production-certified software.** The fixtures do not implement a live payment provider, a protected credential issuer, hardened same-host process separation, E5-side owner-epoch fencing, independent tamper-evident audit custody, or an implemented MCP/A2A stack. The evidence collector reports local test observations and exclusions, not external accreditation.

## Support and use

- [First-time setup and troubleshooting](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/docs/GETTING_STARTED.md)
- [Chapter-to-implementation map](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/docs/CHAPTER_MAP.md)
- [Errata and correction reports](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/ERRATA.md)
- [Responsible vulnerability reporting](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/SECURITY.md)
- [License and commercial book rights](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.0.0/RIGHTS.md)

The **`v1.0.0` tag is immutable** for edition-matched reproduction. Corrections, if any, will receive new version tags.
