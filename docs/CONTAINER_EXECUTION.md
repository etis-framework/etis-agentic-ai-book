# Containerized companion execution — v1.1.0

[Home](../README.md) · [Getting started](GETTING_STARTED.md) · [Companion](../examples/refund-reference-system/README.md) · [Container acceptance](../containers/ACCEPTANCE.md)

## 1. Choose the correct workflow

The Docker workflow is an **alternative** to native Python, not a new agent architecture or a production deployment. It runs the existing Python standard-library examples and tests in Linux on a Docker host. The book's original Python commands and the native test runner remain supported. Use the v1.1.0 source release or a clean candidate checkout; old immutable tags do not contain this infrastructure.

| Workflow | Source | State | Network | Purpose |
|---|---|---|---|---|
| Native Python | Host checkout | Host files | No service required | Original book workflow |
| Disposable `companion` | Image-contained, read-only | Temporary `/tmp` only | None | Release-style verification and one-shot demos |
| Interactive `dev` | Editable host checkout at `/workspace` | Project volume `/state`; writable workspace | None by default | Learning, debugging and modifications |
| VS Code Dev Container | Same editable `dev` workspace | Same project volume | Bridge for optional IDE bootstrap | Interactive IDE development, not release verification |

**Trust boundary:** all six builds retain their existing process and responsibility boundaries. The same-user E5 subprocess and mock credentials are not hardened identity isolation. Docker does not establish independent financial authorization, protected E9 custody, E5-side owner fencing, live provider settlement, or production certification. Docker daemon/host administrators remain trusted. Only run trusted source; even unprivileged containers are not a guarantee against hostile code.

## 2. Install and verify Docker

- macOS: [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/); choose Apple Silicon or Intel.
- Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/); use WSL2/Linux containers, not Windows-container mode. Native Windows remains portable-only. Check institutional requirements for Docker Desktop licensing.
- Linux: [Docker Engine](https://docs.docker.com/engine/install/) plus [Compose V2 plugin](https://docs.docker.com/compose/install/linux/). Use an authorized daemon account; Docker access itself can confer substantial host privileges.

Start Docker and open a terminal. PowerShell, macOS Terminal and Linux shells can run the direct Compose commands below. Use an installed Compose V2-compatible CLI (`docker compose`, not the legacy `docker-compose` command).

```sh
docker --version
docker compose version
docker buildx version
docker info --format 'Architecture: {{.Architecture}} | OS: {{.OSType}}'
docker run --rm hello-world
```

`OSType` must be `linux`. Initial base-image downloads require network access. The actual companion verification, demos and default development service require no external network. No Kubernetes, paid model account, payment account, or host Python installation is needed. Docker Desktop's optional login is not required for the educational fixture; registry rate limits may apply.

## 3. First run — no Make or Git required

Obtain the v1.1.0 source ZIP from the [release list](https://github.com/etis-framework/etis-agentic-ai-book/releases), or use a clean candidate checkout during development. Extract it, open a terminal at the root containing `Dockerfile`, `compose.yaml`, `README.md`, `examples/` and `publishing/`, then run:

```sh
docker compose config --quiet
docker compose build companion
docker compose run --rm --no-deps -T companion
```

The default command checks the runtime's non-root identity, read-only root/source, network isolation, dropped capabilities and no-new-privileges. It then runs the new container-tool regressions, seven existing runner regressions, all ten fixture suites (at least 171 ordinary passing tests), architecture/documentation checks and active reader links. Expected final line begins `PASS: container runtime, tool regressions, companion suites and reader links.` Any failure returns nonzero. An intentionally denied or UNKNOWN demo is not necessarily a failed test. Do not infer production certification from any of these results.

After editing source, **rebuild** before verification; the verification image does not read the host workspace. `docker compose run --build --rm --no-deps -T companion` performs the build and run together. Do not infer source identity from a moving local image tag; record the clean source tag/commit and built image ID for release evidence. Separate checkouts with the same directory basename can share a Compose project name; set `COMPOSE_PROJECT_NAME` or use `docker compose -p <unique-project> ...` consistently for isolated projects.

### Direct Docker alternative (no Compose)

```sh
docker build --target verification -t etis-companion:verify .
docker run --rm --init --read-only --network none --cap-drop ALL --security-opt no-new-privileges:true --pids-limit 256 --tmpfs /tmp:rw,nosuid,nodev,mode=1777 etis-companion:verify
```

The `docker run` security flags are required by the verification preflight. Build the image from the intended version-pinned source; do not assume a previously built local tag is current. Plain `docker build` also selects the verification target. No ports, privileged mode or Docker socket are needed. Use Compose for interactive state management.

## 4. Run the six reference builds

Each command below launches a **new disposable container** from the built verification image. For Build 0 the wrapper performs all four steps together with fresh state. The other wrappers use the original demonstration CLIs and their exit status. The convenience targets use the same entry points.

| Chapter / build | Direct command after `docker compose build companion` | Make shortcut | Scenario |
|---|---|---|---|
| 22 / 0 | `docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 0` | `make docker-build0` | AUTHORIZED → UNKNOWN → CONFIRMED |
| 23 / 1 | `docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 1` | `make docker-build1` | Untrusted advisory |
| 24 / 2 | `docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 2` | `make docker-build2` | Scoped review-only advice |
| 25 / 3 | `docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 3` | `make docker-build3` | Independently approved fixture effect |
| 26 / 4 | `docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 4` | `make docker-build4` | Lost acknowledgment, reconciliation |
| 27 / 5 | `docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 5` | `make docker-build5` | E2 takeover and no replay |

You can also run the original commands directly, for example:

```sh
docker compose run --rm --no-deps -T companion python3 examples/refund-reference-system/build3/demo.py --scenario compromised
```

Build 3's compromised scenario deliberately exits 2 with DENIED and no mock effect. Do not suppress nonzero statuses in verification. To run a single suite, use the book's original unittest command after the Compose prefix. Full independent verification requires the default `companion` command, not a selected test or demo.

## 5. Interactive development and persistent exercises

The `dev` service uses the same pinned Trixie Slim foundation as verification, with Make, curl and libstdc++6. Git is intentionally host-side: run Git commands and use source-control tools on the host against the same checkout, not in the container. No Git is required for the source ZIP exercise route. Neither target includes pip or ensurepip; the companion needs only the standard library. It mounts the host checkout read/write; changes are real host file changes. Build and run only trusted code. Do not store real secrets or sensitive data in this checkout. Use the host editor or VS Code to edit, and use `docker compose exec` to run commands. For macOS/Linux, match the host user before building the first time:

```sh
export ETIS_DEV_UID="$(id -u)"
export ETIS_DEV_GID="$(id -g)"
docker compose up -d --build --no-deps dev
docker compose exec -T dev python3 containers/dev_probe.py
docker compose exec dev bash
```

On Windows PowerShell, omit the `export` commands; the default development UID/GID is 1000. Use the Linux-container file-sharing mechanism. The probe must pass before claiming the workspace and state are writable. Do not solve permission errors by running as root or `chmod 777` on the checkout. If IDs or checkout location change, use a new Compose project or back up/migrate state with appropriate permissions. Host-root Linux users should work under a non-root account.

Inside the development shell, use the book's commands exactly as written except choose a fresh persistent directory under `/state` for a multi-command walkthrough:

```sh
python3 examples/refund-reference-system/build0/refund.py prepare --directory /state/build0-run1
python3 examples/refund-reference-system/build0/refund.py dispatch-lost-ack --directory /state/build0-run1
python3 examples/refund-reference-system/build0/refund.py status --directory /state/build0-run1
python3 examples/refund-reference-system/build0/refund.py reconcile --directory /state/build0-run1
exit
```

Or prefix a command from the host with `docker compose exec -T dev`, for example:

```sh
docker compose exec -T dev python3 publishing/scripts/check_companion_release.py
```

The original `/tmp` paths are appropriate for transient work in a single running container. Do not expect `/tmp` to survive container stop/removal; use `/state` for persistence. The project-scoped `exercise-state` named volume survives `docker compose down` and ordinary recreation. Do not mount SQLite databases into a shared host filesystem for concurrent tests; use the Linux volume or `/tmp` instead. Always pick a new exercise directory for a new walkthrough; never reset state as a substitute for reconciliation.

Stop/remove containers while retaining the volume:

```sh
docker compose down
```

**Destructive and optional:** `docker compose down --volumes` removes that project's exercise-state volume. Back up any needed files first. Never use global Docker prune commands as ETIS cleanup. Exported host evidence under `.etis-local/` is not removed by Compose.

### VS Code Dev Containers (optional)

Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Open the checkout and choose **Dev Containers: Reopen in Container**. The configuration uses the `dev` service and non-root `etis` user; the IDE overlay allows bridge networking only for tooling installation. VS Code Server/extensions may require downloads. On macOS/Linux, launch VS Code from a terminal with the same `ETIS_DEV_UID` and `ETIS_DEV_GID` exports above (or use a consistent `.env` file containing only those numeric values). Do not start conflicting independent dev sessions against the same volume. Select `/usr/local/bin/python3` as the interpreter. The remote Git integration is disabled deliberately; use a separate local VS Code window or host terminal for Git status, diffs, commits, pulls and pushes. Do not mount a host Git binary, credential store, SSH agent or Docker socket to restore remote Git integration. Verify the actual Python editing, execution and debugging workflow; the development image has no pip or ensurepip. The IDE environment is mutable and not a release-verification environment. Use the separate default `companion` service for acceptance. A real VS Code attach/reopen check is a separate manual gate.

#### Select the container interpreter and debug Build 1

A checkout previously used for native macOS or Windows development may contain a host `.venv`. Its Python executable is not portable into Linux. VS Code may select it despite the configured default. Do not delete the host environment or create a new virtual environment in the container.

1. In the remote VS Code window, open a Python file. Click the interpreter in the bottom-right status bar (or run **Python: Select Interpreter** from the Command Palette).
2. Select the global Python 3.13.18 at `/usr/local/bin/python` (equivalently `/usr/local/bin/python3`). Do not select `.venv (broken)` or Create Virtual Environment. If environment creation is already running, cancel it and reload the window before selecting the existing interpreter.
3. In the integrated terminal, confirm `whoami` is `etis`, `pwd` is `/workspace`, and `python3 --version` reports Python 3.13.18. Run `python3 publishing/scripts/check_companion_release.py`.
4. Open `examples/refund-reference-system/build1/advisory.py` and set a breakpoint on the first executable statement inside `advise()`. Open `examples/refund-reference-system/build1/demo.py` as the active editor. Select **Run > Start Debugging**, then **Python Debugger > Python File** if prompted. The Microsoft Python Debugger extension must be available in the remote window; its bundled debugger does not require installing pip in this image.
5. Execution should pause in `advise()`. Inspect the `work`, `evidence` and `model` locals and call stack, then click Continue. Expect the bounded advisory JSON, no financial effects and authorization NOT_GRANTED.
6. Reopen the folder locally and then in the container again; confirm the interpreter selection and workspace persist. Use a separate host terminal for Git. Do not commit workstation-generated `.vscode/settings.json` merely to fix interpreter selection; doing so may alter native workflows.

If the status bar still shows `.venv (broken)`, repeat the explicit selection. If the debugger does not stop, verify `demo.py` is the active launch file, not the imported `advisory.py` module. Do not reinstall Git, pip or ensurepip to work around IDE configuration.

## 6. Export Chapter 31 assurance evidence

From the host, build the intended verification image first. The exporter emits JSON only after the real collector completes all seven registered local cases successfully and preserves `production_certified: false`. Never overwrite earlier evidence or retain a failed/partial export as a successful report.

On macOS/Linux with Make:

```sh
make docker-assurance
```

This creates a fresh `.etis-local/evidence/run-*/evidence.json`. Without Make on a POSIX shell:

```sh
docker compose build companion && mkdir -p .etis-local/evidence && (
  out=$(mktemp -d .etis-local/evidence/run-XXXXXX) || exit 1
  if docker compose run --rm --no-deps -T companion python3 containers/export_evidence.py > "$out/evidence.json" && test -s "$out/evidence.json"; then
    echo "Evidence: $out/evidence.json"
  else
    rm -f "$out/evidence.json"; rmdir "$out"; exit 1
  fi
)
```

On PowerShell (no host Python; explicit UTF-8 without BOM):

```powershell
docker compose build companion
if ($LASTEXITCODE -ne 0) { throw 'Image build failed' }
$dir = Join-Path '.etis-local/evidence' ([guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $dir -Force | Out-Null
$lines = docker compose run --rm --no-deps -T companion python3 containers/export_evidence.py
if ($LASTEXITCODE -ne 0 -or -not $lines) { throw 'Evidence export failed; no report saved' }
$json = $lines -join "`n"
$report = $json | ConvertFrom-Json -ErrorAction Stop
if ($report.overall_fixture_status -ne 'EXECUTED_PASS' -or $report.production_certified -ne $false) { throw 'Invalid report' }
[IO.File]::WriteAllText((Join-Path (Resolve-Path $dir).Path 'evidence.json'), $json + "`n", [Text.UTF8Encoding]::new($false))
```

These files contain bounded local observations, source digests and limitations, not payment records, protected audit custody or independent attestations. For an editable development experiment, use `docker compose exec -T dev python3 examples/refund-reference-system/assurance/collect.py --output /state/evidence-run1.json` and `docker compose cp dev:/state/evidence-run1.json ./.etis-local/evidence-run1.json` (create the destination directory first and select a fresh filename). Label that evidence as development output. A `docker compose cp` export does not upgrade its assurance status.

## 7. Make convenience targets (optional)

Make is not installed by Docker Desktop and is not required. Use the direct commands above on PowerShell or any host without Make.

| Target | Action |
|---|---|
| `make docker-build` | Build the compact verification image |
| `make docker-check` | Rebuild and run the complete offline verification |
| `make docker-build-dev` | Build the interactive image with host UID/GID defaults on POSIX |
| `make docker-up` | Build and start `dev`, matching POSIX host UID/GID by default |
| `make docker-shell` | Open a shell in running `dev` |
| `make docker-build0` … `make docker-build5` | Rebuild as needed and run each disposable demo |
| `make docker-assurance` | Build verification image and export a fresh successful report |
| `make docker-down` | Remove project containers/network; retain state |
| `make docker-clean` | Remove project containers/orphans; retain state, images and exported evidence |

The existing `make check-companion` and `make check` targets remain native. The container is **not** a manuscript publishing toolchain.

## 8. Reproducibility, image updates and limitations

Both Dockerfile targets share a Python 3.13.18 Trixie Slim multi-platform index digest, not an architecture-specific manifest. Docker resolves the appropriate AMD64 or ARM64 image. These pins intentionally do not float to newer Python or Debian layers; a maintainer must review security advisories, obtain new official index digests and rerun all native/container gates before updating them. An image pin is not a vulnerability scan, signature verification, SBOM, exact bit-for-bit build guarantee, or production hardening. The verification target copies only approved companion/QA inputs; the development image mounts the full checkout instead. Build locally; no bundled book image is published. See [rights](../RIGHTS.md).

| Symptom | Resolution |
|---|---|
| `docker: command not found` | Start/install Docker and configure its CLI path; on Mac check Docker Desktop's Advanced CLI installation setting. |
| Cannot connect to daemon | Start Docker Desktop/Engine, check `docker context ls` and `docker info`. |
| Windows mode reports `windows` | Switch Docker Desktop to Linux containers; native Windows still uses portable mode. |
| Pull/digest or registry error | Check connectivity, disk space, registry rate limits and pinned image availability. Never silently remove the digest. |
| `FAIL` runtime preflight | Use the default Compose verification service or the exact hardened `docker run` command. Do not bypass the guard. |
| Permission denied in dev | Match nonzero host UID/GID on POSIX, verify Docker Desktop file sharing, check volume ownership. Use a fresh project after backing up old state if IDs changed. |
| Existing demo state/evidence | Choose a unique directory or filename. Do not erase evidence to force green. |
| Changes not reflected in verification | Rebuild the `companion` image from the intended checkout. Use `dev` for interactive edits. |
| VS Code bootstrap cannot reach extensions | Use the optional IDE overlay, not the offline verification service. Keep network-enabled IDE work distinct from release evidence. |

Platform compatibility must be demonstrated, not inferred from image metadata or a successful image build. See [acceptance gates](../containers/ACCEPTANCE.md) and the release's actual CI/manual evidence.

See the [container security policy](../containers/SECURITY.md) for dependency and vulnerability governance.
