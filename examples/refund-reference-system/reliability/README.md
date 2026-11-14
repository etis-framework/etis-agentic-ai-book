# Chapter 28 — failure and recovery decision cases

This directory is a **separate pure educational fixture**, not Build 6, a payment client or a newly granted E5 recovery service. Run from the repository root:

```bash
python3 -m unittest discover -s examples/refund-reference-system/reliability -p 'test_*.py' -v
```

`recovery_cases.py` receives explicit, validated `Snapshot` values and classifies matching simulated E8 confirmations, ambiguous `NOT_FOUND`, outages and conflicts. `test_recovery_cases.py` exercises post-effect lost acknowledgment, E2 intent before E5 IPC, absent E7 operation, wrong proof, invalid types and forced escalation. No fixture action dispatches a refund, signs an approval, queries a real provider or updates E7. A decision of `CONFIRM` **does not** authorize E7 mutation in any production application: E5 recovery identity, proof provenance, amount/currency matching and finality must be evaluated independently. `NOT_FOUND` is not `FAILED`.

Use Build 4's tested `workflow.py`, `adapter.py`, `ledger.py` and Build 5's tested `coordinator.py` and `runner.py` for the executed local E5/E7/E8 demonstration; the pure Chapter 28 decision aid is intentionally not wired into these services. All provider behavior is simulated. See Chapter 28 Table 28.2 and `IMPLEMENTATION_EVIDENCE_MAP.md` for implemented versus specified boundaries. Existing Builds 0–5 retain their checked-in `architecture.svg` diagrams; this directory introduces **no additional build architecture**.
