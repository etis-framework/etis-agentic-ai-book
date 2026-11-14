#!/usr/bin/env python3
"""Grounded Chapter 26/28 ↔ Build 4/5 code-contract regression gate."""
from pathlib import Path
import ast
root=Path(__file__).resolve().parents[2]
chapter=(root/'manuscript/part-05-reliability-security/ch28-distributed-failure-and-recoverable-effects/index.md').read_text()
coord=(root/'examples/refund-reference-system/build5/coordinator.py').read_text()
ledger=(root/'examples/refund-reference-system/build4/ledger.py').read_text()
tests=(root/'examples/refund-reference-system/build4/test_provider.py').read_text()
assert '`DurableCoordinator`' in chapter
assert '`CoordinatorStore`' not in chapter
assert 'class DurableCoordinator' in coord
ledger_ast=ast.parse(ledger)
assert {'history','_event','observe_unknown','confirm'}.issubset({n.name for c in ledger_ast.body if isinstance(c,ast.ClassDef) and c.name=='OperationalLedger' for n in c.body if isinstance(n,ast.FunctionDef)})
test_names={n.name for c in ast.parse(tests).body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef)}
assert {'test_reconciliation_conflict_preserves_prior_confirmation_history',
        'test_lost_ack_and_reconciliation_preserve_all_local_transitions'} <= test_names
print('Deep war-game code/reader contract: PASS')
