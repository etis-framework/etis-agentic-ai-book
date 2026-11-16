# MCP and A2A: tracing protocol calls without crossing business authority

**Type:** conceptual teaching exercise tied to real existing tests. **Not an implemented MCP/A2A integration or conformance suite.** Read Chapter 19 §19.2 and Chapter 13 before this exercise; use the source diagrams in the Build 2–4 READMEs for the *implemented* modules. This diagram is an **architectural extension**, not a representation of an existing Python module.

## 1. Identify the actors correctly

- **Host application (E1/E2 controller and E3 orchestration):** owns the MCP client connection and approves which tools it may expose to model-directed selection. The language model is **not** the MCP client and never receives a provider API key.
- **MCP server:** offers a protocol-facing tool/resource interface. It may be an E4 read gateway, a narrowly scoped enterprise-owned E6 facade, or a third-party server outside the trusted perimeter. Calling it an MCP server does not make it trusted E5.
- **Independent E5 gate:** verifies each consequential request using authenticated principal/tenant, current business facts, approvals, policy, and operation identity. It owns the trusted E7 intent. Multiple tools/servers may share the same enforcement and key-management infrastructure rather than replicating policy.
- **Restricted E6 adapter and E8 provider:** only a trusted dispatch identity receives provider credentials and sends the independently approved operation. A server cannot pass through the agent's bearer token to bypass audience/authorization checks.
- **A2A peer agent:** may accept an E2-scoped task and return findings. Its Agent Card, task completion or message is an observation, not a finance grant or confirmed refund.

## 2. Conceptual path for CASE-204 (not runnable code)

```text
  Host: E1 admission + E2 owned workflow + E3 advisory agent
      | owns MCP client
      | tools/list  --> tool catalog --> eligibility filter before exposure
      | tools/call  --> recheck context, schema, purpose and authorization
      v
  MCP server (E4 read gateway OR optional E6 protocol facade)
      | untrusted proposed refund; cannot call payment provider directly
      v
  [INDEPENDENT E5 approval + shared policy enforcement]
      | durable RF-1042 intent in E7; protected credential service
      v
  Restricted E6 dispatcher --> E8 provider --> status-only reconciliation

  Optional A2A task: E2 --> external peer --> advisory result --> E2/E3
  (A2A status is neither E5 approval nor authoritative E8 result.)
```

An enterprise design may reject or omit a consequential MCP tool entirely, leaving E5 requests on its existing trusted non-MCP path. The protocol does not force a single deployment location for its server. A central authorization service may serve many tool facades; this is a **governance design choice**, not an MCP-provided credential broker.

## 3. Dynamic discovery is not authority

1. `tools/list` returns advertised available tools for the requesting client. The host then filters by approved server identity, current tenant/purpose, operation class, schemas and risk. Only eligible tools should be exposed to E3.
2. On an applicable list-change notification (with supported capability and subscription), the host re-lists tools and re-evaluates its own eligibility. Because notifications can be missed, freshness also requires suitable refresh on reconnection and before consequential decisions.
3. A newly advertised `issue_refund`, a changed description or `readOnlyHint`, or a valid MCP transport token is **not** independent approval. `tools/call` must be validated and routed through E5 for any possible effect.
4. The MCP server or third-party peer must not gain provider keys, use unvalidated token passthrough, choose arbitrary downstream URL targets, or rewrite UNKNOWN into FAILED.

## 4. Five falsification exercises

| Threat to simulate on paper | Expected control/observation | Closest runnable evidence (not MCP/A2A conformance) |
|---|---|---|
| New tool appears after `tools/list` refresh | Tool excluded until policy and tenant/case eligibility approve it | `build2/test_scope.py` (scoping) and `build1/test_advisory.py` (advisory output denial) |
| Compromised agent chooses `issue_refund` and has a valid identity token | E5 denies absent independently issued finance grant; no financial effect | `build3/test_gate.py::test_valid_agent_token_is_not_payment_approval`; `security/test_adversarial_cases.py` |
| Two MCP server facades share one E5 | Both must receive the same independent case-specific decision; no duplicate provider keys | `build3/service.py` gate; `build4/ledger.py` durable uniqueness (no multi-server integration test) |
| MCP tool call receives provider timeout | Preserve RF-1042 as UNKNOWN; status-only reconciliation, never fresh refund | `build4/test_provider.py::test_lost_ack_requires_authoritative_reconciliation` |
| A2A peer claims 'refund complete' | Treat peer task result as untrusted advice, reconcile only from E8 | `build1/test_advisory.py`, `build4/adapter.py` mock E8 lookup (no peer fixture) |

**Student deliverable:** draw the trust boundary, name the code modules and exact negative tests, explain two ways a protocol adapter could bypass E5 if deployed incorrectly, and distinguish three columns: *demonstrated locally*, *specified for deployment*, and *not implemented*. A design that labels any MCP server as automatically trusted fails the exercise.

## 5. Official references and scope

- [MCP 2026-07-28: Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) — method names and list-change semantics.
- [MCP 2026-07-28: Architecture](https://modelcontextprotocol.io/docs/learn/architecture) — host, client and server roles; use the pinned 2026-07-28 documentation when exact wire behavior matters.
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) — token passthrough and audience checks; living document.
- [A2A 1.0.0 specification](https://a2a-protocol.org/v1.0.0/specification/) — agent discovery and task communication.

Do not treat these specifications as proof of financial approval, credential separation, payment settlement or the ETIS-specific deployment pattern.
