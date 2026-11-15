# Pre–Part VII manuscript ↔ implementation audit

## Proof standard

An implemented claim needs **source + runnable test + observed bounded result + limitation**; a proposed enterprise mechanism must be labeled **specified only**. Never substitute an architecture diagram for a working authorization boundary or a passing simulator test for an external provider attestation.

| Book claim | Reader source anchor | Local executable evidence | What the code does **not** establish |
|---|---|---|---|
| Deterministic refund intent and once-only attempt (Ch22) | `build0/README.md`, `build0/refund.py` | `build0/test_refund.py` concurrency and lost-ack cases | Payment network settlement or distributed database durability |
| Typed non-effectful proposal (Ch23) | `build1/README.md`, `build1/advisory.py` | `build1/test_advisory.py` | Live model reliability or independent financial authorization |
| Signed scoped context and provenance (Ch24) | `build2/README.md`, `build2/identity.py`, `build2/context.py` | `build2/test_scope.py` | Enterprise issuer, real SSO revocation or full prompt-injection elimination |
| Separate-process E5 gate (Ch25/29) | `build3/README.md`, `build3/service.py` | `build3/test_gate.py`, `security/test_adversarial_cases.py` | Hostile-host/same-UID isolation, independent approval issuer or secrets governance |
| Typed provider and status-only reconciliation (Ch26/28) | `build4/README.md`, `build4/adapter.py`, `build4/ledger.py` | `build4/test_provider.py`, `reliability/test_recovery_cases.py` | Real C08 provider proof consistency/idempotency/settlement guarantee |
| Durable E2 ownership and takeover (Ch27/30) | `build5/README.md`, `build5/coordinator.py`, `build5/runner.py` | `build5/test_coordination.py` | E5-side owner-epoch validation, multi-site consistency |
| Read-only incident assessment (Ch30) | `operations/README.md`, `operations/incident.py` | `operations/test_incident.py` | Real incident command, deployed telemetry, revocation or provider access |
| Collected test evidence (Ch31) | `assurance/README.md`, `assurance/collect.py` | `assurance/test_collect.py` | Certified audit custody, organizational approval or regulated compliance |
| Governance/release/economics (Ch32–34) | Reader-facing tables, figures, Runbooks 32-A/33-A | Reuse above tests for bounded scenarios | Running financial approval governance, progressive release controller, cost collector or ROI dashboard |

## Reproducibility commands (run from repository root)

```sh
make check
make book-docx
make check-figures
python3 publishing/scripts/check_pre_part_vii_audit.py
```

For an independent test class, run `python3 -m unittest discover -s examples/refund-reference-system/<suite> -p 'test_*.py' -v` with `<suite>` chosen from `build0` … `build5`, `reliability`, `security`, `operations`, `assurance`.

**Baseline observation:** The previous Chapter 34 QA records show 153/153 passes across ten suites. This audit's own full `make check` attempt ended on the slow companion architecture documentation check after the chapter/editorial/static figure checks and did not establish a single uninterrupted pass. Its results must not be relabeled a current integrated regression PASS.
