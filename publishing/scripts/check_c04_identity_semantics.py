#!/usr/bin/env python3
"""Check reader-facing C04 proposal vs trusted payment identities (CAB-001 aligned)."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
paths={
 'ch08':'manuscript/part-02-architecture/ch08-from-requirements-to-a-reference-architecture/index.md',
 'ch11':'manuscript/part-02-architecture/ch11-agent-reasoning-and-proposal-contracts-e3/index.md',
 'appendix':'manuscript/backmatter/appendices.md',
}
text={name:(ROOT/path).read_text() for name,path in paths.items()}
required={
 'ch08':['CAB-001 C04 `operation_id`','`idempotency intent` requests duplicate-safe handling','Neither is `RF-1042`, a provider key, or financial permission','E5/E7 assigns and persists'],
 'ch11':['CAB-001 C04','proposed `operation_id`','`idempotency intent`','Neither is a provider key','E3 cannot mint'],
 'appendix':['Proposed `operation_id`','`idempotency intent`','Neither is RF-1042','provider idempotency key'],
}
errors=[f'{name}: missing {phrase}' for name,phrases in required.items() for phrase in phrases if phrase not in text[name]]
if errors: raise SystemExit('FAIL C04 identity semantics:\n'+'\n'.join(errors))
print('PASS C04 identity semantics: CAB-001 field names preserved; advisory and trusted IDs separated')
