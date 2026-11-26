# Getting started — first-edition companion

[Home](../README.md) · [Companion](../examples/refund-reference-system/README.md) · [Chapter map](CHAPTER_MAP.md)

## Prerequisites

- Python 3.10+; tested locally with Python 3.13 during publication preparation. The GitHub workflow tests additional versions.
- A terminal (Terminal on macOS/Linux; PowerShell or Command Prompt on Windows). **Git is optional** if you use the downloadable ZIP. Python commands use `python3` on macOS/Linux and `py -3` on Windows.
- **No** pip dependencies, credentials, accounts, local model, internet service, or payment provider for the companion tests. Cloning requires network access; tests do not.

## Platform support

| Environment | Supported verification | Command |
|---|---|---|
| macOS or Linux, Python 3.10+ | Full Builds 0–5, Chapters 28–31 and architecture checks | `python3 publishing/scripts/check_companion_release.py` |
| Windows, Python 3.10+ | Portable Builds 0–2 and architecture checks **only** | `py -3 publishing/scripts/check_companion_release.py --portable` |

Build 3's E5 reference service uses **Unix-domain sockets and POSIX socket permissions**, and later exercises depend on this path. The full companion is **not verified or supported on native Windows**. Windows users wanting all ten suites should use an appropriate Linux environment (for example WSL2); that environment must be verified independently. Do not interpret a portable-subset pass as a full companion pass. No paid services or dependencies are required for either command.

## Download the first-edition code

For corrected exercises select `v1.0.1` once published, substituting that tag and extracted folder version in the instructions below. Use `v1.0.0` for exact original-edition reproduction. See [maintenance notes](../RELEASE_NOTES_v1.0.1.md).

**Option A — easiest: ZIP download (no Git installation).**

1. Open [First-edition GitHub Releases](https://github.com/etis-framework/etis-agentic-ai-book/releases) and select **`v1.0.0`**.
2. Under **Assets**, select **Source code (zip)**. Do not use a ZIP of the moving `main` branch when following the printed edition.
3. Extract the ZIP to a folder you can find, such as Downloads. Open the extracted `etis-agentic-ai-book-1.0.0` folder (folder naming may vary slightly).
4. Open a terminal **in that folder**. On macOS, open Terminal, type `cd ` (with a trailing space), drag the extracted folder into the Terminal window, and press Enter. On Windows, open the extracted folder in File Explorer, click the address bar, type `powershell`, and press Enter. On Linux, use the file manager's *Open in Terminal* option or `cd` to that folder.
5. Confirm you are in the right place: the folder should contain `README.md`, `publishing/`, and `examples/`. The commands below are written for this **repository root**, not the `build0/` subfolder.

**Option B — Git users (clone the same edition):**

```bash
git clone https://github.com/etis-framework/etis-agentic-ai-book.git
cd etis-agentic-ai-book
git fetch --tags
git checkout v1.0.0
```

The immutable first-edition tag is created for the GitHub Release before the book launch. If you are reading this before the Release appears, use the current `main` checkout for exploration, but do not claim it is edition-pinned.

## Verify Python and run the companion tests

From the repository root, first check your installed Python version:

```bash
python3 --version
```

On Windows use `py -3 --version`. You need version 3.10 or newer. If the command is unavailable, install Python from [python.org](https://www.python.org/downloads/) and reopen the terminal.

On macOS/Linux, run:

```bash
python3 publishing/scripts/check_companion_release.py
```

Windows (portable subset **only**): `py -3 publishing/scripts/check_companion_release.py --portable`. On native Windows, the full command exits early with an explanation instead of reporting spurious Build 3 failures.

In full mode, the checker runs ten suites in this order: Builds 0–5; Chapter 28 reliability; Chapter 29 security; Chapter 30 operations; Chapter 31 assurance. In portable mode, it runs Builds 0–2 only. Both modes run the architecture/companion-documentation checker. It exits nonzero when anything fails. For full printed-book production QA, see [`publishing/`](../publishing/README.md); that is a distinct toolchain and may require a generated Word file and image tools.

**Expected full-run finish:** `PASS: all 10 local fixture suites and architecture/documentation check.` On native Windows, the portable command reports `PASS: portable Builds 0-2 and architecture/documentation check.` A test failure prints `FAIL` and exits nonzero; share the error, Python version, operating system, and tag when reporting a reproducible issue. The initial tests may print many `ok` lines—each is one successful unittest assertion group.

To inspect test names and assertions without the helper:

```bash
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

## First demonstration: UNKNOWN is not FAILED

On macOS/Linux, run these commands **one at a time**, from the repository root. Use a new disposable directory for each new walkthrough:

```bash
python3 examples/refund-reference-system/build0/refund.py prepare --directory /tmp/etis-book-example
python3 examples/refund-reference-system/build0/refund.py dispatch-lost-ack --directory /tmp/etis-book-example
python3 examples/refund-reference-system/build0/refund.py status --directory /tmp/etis-book-example
python3 examples/refund-reference-system/build0/refund.py reconcile --directory /tmp/etis-book-example
```

**What to expect:** `prepare` creates authorized local intent. `dispatch-lost-ack` prints a JSON result of `UNKNOWN` and exits successfully: the mock provider committed, but its acknowledgment was deliberately lost. Other negative demos can exit nonzero on purpose; an intentional denial is not necessarily an installation failure. Run `status` next: local E7 reports `UNKNOWN`, although the separate simulated provider E8 has one `CONFIRMED` refund. `reconcile` checks mock provider truth and returns `CONFIRMED` **without issuing another refund**. The Build 0 [step-by-step README](../examples/refund-reference-system/build0/README.md) explains how to inspect the separate SQLite files.

**On native Windows:** use PowerShell, substitute `py -3` for `python3`, and choose a fresh writable path such as `"${env:TEMP}\etis-book-example"` as the argument to `--directory`. PowerShell can pass that path directly. For a second run, pick another directory rather than reusing the saved state. No exercise contacts a live financial system.

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
| `python3: command not found` | Use `py -3` on Windows for the portable subset or install Python 3.10+; check `python3 --version`. |
| Full tests unsupported on native Windows | Run `py -3 publishing/scripts/check_companion_release.py --portable` for Builds 0–2; use macOS/Linux for all ten suites. |
| Cannot check out `v1.0.0` | Use the [first-edition Release](https://github.com/etis-framework/etis-agentic-ai-book/releases); Git users can run `git fetch --tags` before checkout. |
| SQLite file already contains a demonstration | Use a fresh, disposable directory; exercises retain state intentionally. |
| Evidence path exists | Choose a different unique filename; collector will not overwrite. |
| Tests fail after edits | Return to the clean first-edition tag, then rerun. Report reproducible failures using [contribution guidance](../CONTRIBUTING.md). |
| `make check` requires DOCX | Use the companion checker above; `make check` is for maintainers rebuilding the book. |

**Important limitation:** tests demonstrate educational fixture behavior only. There are no real credentials, provider calls, settlement proofs, protected audit logs, or production release authority in this code.
