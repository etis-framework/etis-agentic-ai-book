# Chapter-to-companion evidence map

[Home](../README.md) · [Companion](../examples/refund-reference-system/README.md) · [Detailed evidence map](../examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md)

This is a navigational map, **not** a substitute for CAB-001 E1–E9/C01–C09 or a production attestation. All tests use fictional CASE-204 / $500 / RF-1042.

| Chapter | Implementation | Test evidence | Boundary / known limit |
|---|---|---|---|
| 22 | [Build 0](../examples/refund-reference-system/build0/README.md) | `build0/test_refund.py` | E7 local record differs from simulated E8 provider truth |
| 23 | [Build 1](../examples/refund-reference-system/build1/README.md) | `build1/test_advisory.py` | Advisory output cannot authorize refund |
| 24 | [Build 2](../examples/refund-reference-system/build2/README.md) | `build2/test_scope.py` | Fixture identity/context not production credential custody |
| 25 | [Build 3](../examples/refund-reference-system/build3/README.md) | `build3/test_gate.py` | E5 independently checks case-specific approval; same-UID process not OS isolation |
| 26 | [Build 4](../examples/refund-reference-system/build4/README.md) | `build4/test_provider.py` | Mock E8 proof only; lost acknowledgments require read-only reconciliation |
| 27 | [Build 5](../examples/refund-reference-system/build5/README.md) | `build5/test_coordination.py` | E2 owner epoch not enforced independently by E5 |
| 28 | [Reliability](../examples/refund-reference-system/reliability/README.md) | `reliability/test_recovery_cases.py` | Unknown / absent status never authorizes retransmission |
| 29 | [Security](../examples/refund-reference-system/security/README.md) | `security/test_adversarial_cases.py` | Valid investigator assertion without finance approval creates no effect |
| 30 | [Operations](../examples/refund-reference-system/operations/README.md) | `operations/test_incident.py` | Incident observer is read-only; telemetry gaps remain visible |
| 31 | [Assurance](../examples/refund-reference-system/assurance/README.md) | `assurance/test_collect.py`, `assurance/collect.py` | Seven local claim cases, five explicit production gaps; not production-certified |

Every Build 0–5 README embeds its checked-in `architecture.svg`, which maps **actual source modules** to its teaching boundaries. Read [ARCHITECTURE.md](../examples/refund-reference-system/ARCHITECTURE.md), [ENGINEERING_STANDARD.md](../examples/refund-reference-system/ENGINEERING_STANDARD.md), and [PROTOCOL_BOUNDARY_STUDY.md](../examples/refund-reference-system/PROTOCOL_BOUNDARY_STUDY.md) before adapting examples for an enterprise system.

**No paid AI API or real payment account is needed**; conceptual protocol material is not a working MCP or A2A transport. All chapter code exercises remain distinct from the frozen textbook manuscript.
