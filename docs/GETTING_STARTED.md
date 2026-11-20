# Getting started — first-edition companion

[Home](../README.md) · [Companion](../examples/refund-reference-system/README.md) · [Chapter map](CHAPTER_MAP.md)

## Prerequisites

- Python 3.10+; tested locally with Python 3.13 during publication preparation. The GitHub workflow tests additional versions.
- Git and terminal. macOS/Linux `python3`; Windows `py -3` (or `python` if your installation uses that command).
- **No** pip dependencies, credentials, accounts, local model, internet service, or payment provider for the companion tests. Cloning requires network access; tests do not.

## Download the version that matches your book

```bash
git clone https://github.com/etis-framework/etis-agentic-ai-book.git
cd etis-agentic-ai-book
git fetch --tags
git checkout v1.0.0
```

`v1.0.0` will exist **only after the maintainer publishes the first-edition release**. Until then, use the current checkout and its tests; never claim the unreleased tag exists.

## Verify the companion

From the repository root:

```bash
python3 publishing/scripts/check_companion_release.py
```

Windows: `py -3 publishing/scripts/check_companion_release.py`.

The checker runs ten suites in this order: Builds 0–5; Chapter 28 reliability; Chapter 29 security; Chapter 30 operations; Chapter 31 assurance. Then it runs the architecture/companion-documentation checker. It exits nonzero when anything fails. For full printed-book production QA, see [`publishing/`](../publishing/README.md); that is a distinct toolchain and may require a generated Word file and image tools.

To inspect test names and assertions without the helper:

```bash
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

## First demonstration: UNKNOWN is not FAILED

On macOS/Linux, from the repository root, choose a **fresh** disposable path:

```bash
python3 examples/refund-reference-system/build0/refund.py prepare --directory /tmp/etis-book-example
python3 examples/refund-reference-system/build0/refund.py dispatch-lost-ack --directory /tmp/etis-book-example
python3 examples/refund-reference-system/build0/refund.py status --directory /tmp/etis-book-example
python3 examples/refund-reference-system/build0/refund.py reconcile --directory /tmp/etis-book-example
```

You should see an uncertain local state before reconciliation, although the simulated provider has confirmed **one** RF-1042 record. Use [Build 0's database inspection exercise](../examples/refund-reference-system/build0/README.md) to inspect E7 and mock E8 separately. On Windows, use a new writable directory such as `%TEMP%\etis-book-example` in Command Prompt and use `py -3` for Python. Choose a new path on subsequent runs. **Do not use any live financial system.**

## Continue the engineering progression

Follow [Builds 1–5](../examples/refund-reference-system/README.md) and then use the [Chapter map](CHAPTER_MAP.md) for the adversarial, reliability, incident, and evidence exercises. You do **not** need to run an AI model; Build 1's model interface uses injected local test doubles.

## Evidence collector

```bash
python3 examples/refund-reference-system/assurance/collect.py --output /tmp/etis-ch31-evidence.json
```

Use a **new output path every run**; the collector intentionally refuses to overwrite prior evidence. On Windows, use a writable path in your temp directory. Read [assurance scope and production gaps](../examples/refund-reference-system/assurance/README.md).

## Common problems

| Symptom | Action |
|---|---|
| `python3: command not found` | Use `py -3` on Windows or install Python 3.10+; check `python3 --version`. |
| Cannot check out `v1.0.0` | Confirm the [first-edition Release](https://github.com/etis-framework/etis-agentic-ai-book/releases) has been published; run `git fetch --tags`. |
| SQLite file already contains a demonstration | Use a fresh, disposable directory; exercises retain state intentionally. |
| Evidence path exists | Choose a different unique filename; collector will not overwrite. |
| Tests fail after edits | Return to the clean first-edition tag, then rerun. Report reproducible failures using [contribution guidance](../CONTRIBUTING.md). |
| `make check` requires DOCX | Use the companion checker here; manuscript production QA has different prerequisites. |

**Important limitation:** tests demonstrate educational fixture behavior only. There are no real credentials, provider calls, settlement proofs, protected audit logs, or production release authority in this code.
